// keypointer.swift — scrolling and pointer steps from the keyboard.
//
// Two jobs, one daemon, because both are Karabiner reporting keys over UDP and
// something having to integrate them.
//
// Scrolling: Karabiner's own `mouse_key` wheel is a line-based USB wheel, and
// macOS applies its own acceleration on top — the runaway ramp you cannot tune
// away. This posts *pixel* deltas instead, the way a trackpad does, so the
// speed is exactly what the config says and nothing amplifies it. Pixel deltas
// also buy what line events never had: rubber-banding at a document's edge and
// a coast after release.
//
// Pointer steps: hold a direction and tap a digit, and the pointer moves that
// many cells that way. A cell is about a character, so the digit reads as "how
// far" in the same units as the text you are aiming at.
//
// The protocol is one word per event, over UDP:
//
//   u1 d0 l1 r0    scroll, direction then 1 for down and 0 for up
//   Fu1 Fd0        the same direction from a fast key, `scroll_fast` times over
//   U1 D0 L1 R0    step direction held, same shape in upper case
//   n8             a digit tapped: step now, by 8 cells, 0 meaning half a cell
//
//   swiftc -O tools/keypointer.swift -o tools/keypointer
//   tools/keypointer             # run it
//   tools/keypointer --watch     # print the velocity, phase and steps
//   tools/keypointer --selftest  # ramp, momentum and step maths, no hardware
//
// Posting events needs Accessibility. Config: keypointer.json next to the
// binary, or ~/.config/karabiner/keypointer.json, or --config PATH.

import CoreGraphics
import Foundation

// MARK: - Config

struct Config: Decodable {
    let port: UInt16?
    let base_speed: Double?      // px/s the instant a key goes down
    let max_speed: Double?       // px/s once the ramp is finished
    let ramp_ms: Double?         // how long to get there
    let momentum: Bool?          // coast after release
    let momentum_decay: Double?  // velocity kept per tick while coasting
    let natural: Bool?           // true = content follows the key, trackpad style
    let tick_hz: Double?
    let scroll_fast: Double?     // multiplier for the fast scroll keys
    let step_curve: Double?      // how much 9 outruns a linear nine cells
    let cell_width: Double?      // px per cell across, about a character
    let cell_height: Double?     // px per cell down, about a line

    var udpPort: UInt16 { port ?? 45455 }
    var cell: CGSize { CGSize(width: cell_width ?? 8, height: cell_height ?? 16) }
    var scrollFast: Double { scroll_fast ?? 3 }
    var stepCurve: Double { step_curve ?? 4 }
    var base: Double { base_speed ?? 140 }
    var top: Double { max_speed ?? 1600 }
    var ramp: Double { (ramp_ms ?? 550) / 1000 }
    var coasts: Bool { momentum ?? true }
    var decay: Double { momentum_decay ?? 0.93 }
    var sign: Double { (natural ?? false) ? -1 : 1 }
    var tick: Double { 1.0 / (tick_hz ?? 120) }
}

/// How many cells a digit is worth. The low digits stay near their own value,
/// because that is where you are placing the pointer precisely, and the curve
/// only opens up at the top: with `step_curve` at 4, 9 is worth five times a
/// linear nine, so one key covers a screen and another covers a character.
/// 0 is the nudge: half a cell, for when one is already too far.
func cells(forDigit digit: Int, _ config: Config) -> Double {
    guard digit != 0 else { return 0.5 }
    let n = Double(digit)
    let reach = (n - 1) / 8                       // 0 at 1, 1 at 9
    return n * (1 + config.stepCurve * reach * reach)
}

/// Where a step of `digit` cells lands, given the directions currently held.
func step(digit: Int, left: Bool, right: Bool, up: Bool, down: Bool,
          from point: CGPoint, _ config: Config) -> CGPoint {
    let cells = cells(forDigit: digit, config)
    let dx = (right ? 1.0 : 0) - (left ? 1.0 : 0)
    let dy = (down ? 1.0 : 0) - (up ? 1.0 : 0)
    return CGPoint(x: point.x + dx * cells * config.cell.width,
                   y: point.y + dy * cells * config.cell.height)
}

func clamp(_ p: CGPoint) -> CGPoint {
    var count: UInt32 = 0
    CGGetActiveDisplayList(0, nil, &count)
    var ids = [CGDirectDisplayID](repeating: 0, count: Int(count))
    CGGetActiveDisplayList(count, &ids, &count)
    let desktop = ids.map(CGDisplayBounds).reduce(CGRect.null) { $0.union($1) }
    guard !desktop.isNull else { return p }
    return CGPoint(x: min(max(p.x, desktop.minX), desktop.maxX - 1),
                   y: min(max(p.y, desktop.minY), desktop.maxY - 1))
}

// Ease-in from `base` to `top`: a tap stays a nudge, a hold builds to a glide.
// Quadratic rather than linear so the first tenth of a second is gentle, which
// is the whole complaint about the system's own acceleration.
func speed(heldFor seconds: Double, _ config: Config) -> Double {
    guard config.ramp > 0 else { return config.top }
    let t = min(seconds / config.ramp, 1)
    return config.base + (config.top - config.base) * t * t
}

// MARK: - Keys over UDP

final class Keys {
    private let lock = NSLock()
    private var held: Set<Character> = []            // scroll keys, lower case
    private var fast: Set<Character> = []           // of those, the ones on a fast key
    private var stepping: Set<Character> = []        // step directions, upper case
    private var pendingDigits: [Int] = []
    private var since: [Character: Date] = [:]

    func listen(port: UInt16) {
        let fd = socket(AF_INET, SOCK_DGRAM, 0)
        var addr = sockaddr_in()
        addr.sin_family = sa_family_t(AF_INET)
        addr.sin_port = port.bigEndian
        addr.sin_addr.s_addr = INADDR_LOOPBACK.bigEndian  // loopback only
        let bound = withUnsafePointer(to: &addr) {
            bind(fd, UnsafeRawPointer($0).assumingMemoryBound(to: sockaddr.self),
                 socklen_t(MemoryLayout<sockaddr_in>.size))
        }
        guard fd >= 0, bound == 0 else {
            FileHandle.standardError.write("cannot bind UDP \(port)\n".data(using: .utf8)!)
            exit(1)
        }
        Thread.detachNewThread { [self] in
            var buf = [UInt8](repeating: 0, count: 16)
            while true {
                let n = recv(fd, &buf, buf.count, 0)
                guard n >= 2 else { continue }
                let word = String(decoding: buf[0..<n], as: UTF8.self)
                guard var kind = word.first else { continue }
                var quick = false
                if kind == "F" {                    // fast scroll: F, direction, state
                    guard word.count >= 3, let dir = word.dropFirst().first else { continue }
                    kind = dir
                    quick = true
                }
                if kind == "n" {
                    guard let digit = Int(word.dropFirst()), (0...9).contains(digit) else { continue }
                    lock.lock(); pendingDigits.append(digit); lock.unlock()
                    continue
                }
                let down = word.dropFirst(quick ? 2 : 1).first == "1"
                if "UDLR".contains(kind) {
                    lock.lock()
                    if down { stepping.insert(kind) } else { stepping.remove(kind) }
                    lock.unlock()
                    continue
                }
                guard "udlr".contains(kind) else { continue }
                lock.lock()
                if down {
                    if !held.contains(kind) { since[kind] = Date() }
                    held.insert(kind)
                    if quick { fast.insert(kind) }
                } else {
                    held.remove(kind)
                    fast.remove(kind)
                    since[kind] = nil
                }
                lock.unlock()
            }
        }
    }

    /// Pixels per second on each axis, ramped by how long each key has been down.
    func velocity(_ config: Config, now: Date = Date()) -> (x: Double, y: Double) {
        lock.lock(); defer { lock.unlock() }
        func axis(_ positive: Character, _ negative: Character) -> Double {
            var v = 0.0
            for (dir, factor) in [(positive, 1.0), (negative, -1.0)] where held.contains(dir) {
                let heldFor = since[dir].map { now.timeIntervalSince($0) } ?? 0
                let rate = fast.contains(dir) ? config.scrollFast : 1
                v += factor * speed(heldFor: heldFor, config) * rate
            }
            return v
        }
        return (axis("r", "l"), axis("u", "d"))
    }

    /// Digits tapped since the last tick, with the directions held at read
    /// time. A digit with no direction held does nothing — the direction keys
    /// are a prefix, not a mode.
    func drainSteps() -> [(digit: Int, left: Bool, right: Bool, up: Bool, down: Bool)] {
        lock.lock(); defer { lock.unlock() }
        let digits = pendingDigits
        pendingDigits = []
        let (l, r, u, d) = (stepping.contains("L"), stepping.contains("R"),
                            stepping.contains("U"), stepping.contains("D"))
        guard l || r || u || d else { return [] }
        return digits.map { (digit: $0, left: l, right: r, up: u, down: d) }
    }
}

// MARK: - Posting the scroll

// A trackpad's scroll events carry a phase, and apps lean on it: `began` starts
// a gesture, `ended` releases the rubber band, and the momentum phases are what
// make a flick coast. None of these are in Swift's CGEventField enum, so they
// go in by raw field number.
private let fieldIsContinuous = CGEventField(rawValue: 88)!
private let fieldScrollPhase = CGEventField(rawValue: 99)!
private let fieldMomentumPhase = CGEventField(rawValue: 123)!

enum Phase: Int64 {
    case none = 0, began = 1, changed = 2, ended = 4
}

enum Momentum: Int64 {
    case none = 0, begin = 1, `continue` = 2, end = 3
}

func postScroll(dx: Int32, dy: Int32, phase: Phase, momentum: Momentum) {
    guard let event = CGEvent(scrollWheelEvent2Source: nil, units: .pixel,
                              wheelCount: 2, wheel1: dy, wheel2: dx, wheel3: 0)
    else { return }
    event.setIntegerValueField(fieldIsContinuous, value: 1)
    event.setIntegerValueField(fieldScrollPhase, value: phase.rawValue)
    event.setIntegerValueField(fieldMomentumPhase, value: momentum.rawValue)
    event.post(tap: .cghidEventTap)
}

// MARK: - Checks

func selftest() {
    let cfg = Config(port: nil, base_speed: 140, max_speed: 1600, ramp_ms: 550,
                     momentum: true, momentum_decay: 0.93, natural: false, tick_hz: 120, scroll_fast: 3, step_curve: 4,
                     cell_width: 8, cell_height: 16)

    // The ramp starts at base, ends at top, and never overshoots in between.
    precondition(abs(speed(heldFor: 0, cfg) - cfg.base) < 0.001, "a tap is the base speed")
    precondition(abs(speed(heldFor: cfg.ramp, cfg) - cfg.top) < 0.001, "the ramp reaches the top")
    precondition(abs(speed(heldFor: 10, cfg) - cfg.top) < 0.001, "and stays there")
    var last = 0.0
    for i in 0...100 {
        let v = speed(heldFor: cfg.ramp * Double(i) / 100, cfg)
        precondition(v >= last - 0.001 && v <= cfg.top + 0.001, "monotone, no overshoot: \(v)")
        last = v
    }
    // Gentle early: a tenth of the ramp should still be near the base speed,
    // which is what a linear ramp gets wrong.
    precondition(speed(heldFor: cfg.ramp * 0.1, cfg) < cfg.base + (cfg.top - cfg.base) * 0.02,
                 "the first tenth stays gentle")

    // Sub-pixel accumulation must not lose distance: at the base speed a 120Hz
    // tick is barely over one pixel, so truncating every frame would drift.
    var carry = 0.0
    var posted = 0
    for _ in 0..<120 {
        carry += cfg.base * cfg.tick
        let whole = carry.rounded(.towardZero)
        posted += Int(whole)
        carry -= whole
    }
    precondition(abs(Double(posted) - cfg.base) <= 1,
                 "a second at base speed scrolls base pixels, not \(posted)")

    // Coasting has to stop, and stop soon: 0.93 a tick from the top speed is
    // about a third of a second of glide.
    var v = cfg.top * cfg.tick
    var ticks = 0
    var distance = 0.0
    while abs(v) >= 1 {
        distance += v
        v *= cfg.decay
        ticks += 1
        precondition(ticks < 1000, "momentum terminates")
    }
    precondition(ticks < 60, "the coast is under half a second: \(ticks) ticks")
    precondition(distance < 250, "and under 250px: \(distance)")

    // The digit curve: 1 is one cell, 9 is five times a linear nine, and the
    // low digits stay close to their own value.
    precondition(abs(cells(forDigit: 1, cfg) - 1) < 0.001, "1 is one cell")
    precondition(abs(cells(forDigit: 9, cfg) - 45) < 0.001,
                 "9 is five nines: \(cells(forDigit: 9, cfg))")
    for digit in 2...3 {
        let value = cells(forDigit: digit, cfg)
        precondition(value >= Double(digit) && value < Double(digit) * 1.3,
                     "\(digit) stays near \(digit): \(value)")
    }
    var previous = 0.0
    for digit in 1...9 {
        let value = cells(forDigit: digit, cfg)
        precondition(value > previous, "the curve climbs: \(digit) -> \(value)")
        previous = value
    }
    precondition(cells(forDigit: 0, cfg) == 0.5, "0 is still the nudge")

    // A step is that many cells, in whatever directions are held.
    let origin = CGPoint(x: 500, y: 500)
    let leftUp = step(digit: 8, left: true, right: false, up: true, down: false,
                      from: origin, cfg)
    let eight = cells(forDigit: 8, cfg)
    precondition(abs(leftUp.x - (500 - eight * cfg.cell.width)) < 0.001
                 && abs(leftUp.y - (500 - eight * cfg.cell.height)) < 0.001,
                 "hold left and up, tap 8: the same cells each way: \(leftUp)")
    let nudge = step(digit: 0, left: false, right: true, up: false, down: false, from: origin, cfg)

    precondition(abs(nudge.x - (500 + 0.5 * cfg.cell.width)) < 0.001, "0 is half a cell: \(nudge)")
    precondition(nudge.x > 500, "and still moves: \(nudge)")
    let cancelled = step(digit: 5, left: true, right: true, up: true, down: true,
                         from: origin, cfg)
    precondition(cancelled == origin, "opposite directions cancel: \(cancelled)")
    let one = step(digit: 1, left: false, right: false, up: false, down: true, from: origin, cfg)
    precondition(abs(one.y - (500 + cfg.cell.height)) < 0.001,
                 "one cell down is about a line: \(one)")

    print("selftest ok")
}

// MARK: - Run

func loadConfig(_ explicit: String?) -> Config {
    let exeDir = URL(fileURLWithPath: CommandLine.arguments[0])
        .resolvingSymlinksInPath().deletingLastPathComponent()
    let candidates = [
        explicit.map { URL(fileURLWithPath: $0) },
        exeDir.appendingPathComponent("keyscroll.json"),
        FileManager.default.homeDirectoryForCurrentUser
            .appendingPathComponent(".config/karabiner/keyscroll.json"),
    ].compactMap { $0 }
    for url in candidates {
        guard let data = try? Data(contentsOf: url) else { continue }
        if let cfg = try? JSONDecoder().decode(Config.self, from: data) { return cfg }
        FileHandle.standardError.write("bad config \(url.path)\n".data(using: .utf8)!)
        exit(1)
    }
    return Config(port: nil, base_speed: nil, max_speed: nil, ramp_ms: nil,
                  momentum: nil, momentum_decay: nil, natural: nil, tick_hz: nil,
                  scroll_fast: nil, step_curve: nil, cell_width: nil, cell_height: nil)
}

let args = CommandLine.arguments
if args.contains("--selftest") { selftest(); exit(0) }

let watch = args.contains("--watch")
let config = loadConfig(args.firstIndex(of: "--config").flatMap {
    args.indices.contains($0 + 1) ? args[$0 + 1] : nil
})

let keys = Keys()
keys.listen(port: config.udpPort)

var carry = (x: 0.0, y: 0.0)          // sub-pixel remainder
var coast = (x: 0.0, y: 0.0)          // px per tick while coasting
var scrolling = false                 // mid-gesture, so the next event is `changed`
var coasting = false

print("keypointer on udp \(config.udpPort): \(Int(config.base))-\(Int(config.top))px/s "
    + "over \(Int(config.ramp * 1000))ms, momentum \(config.coasts ? "on" : "off")")

Timer.scheduledTimer(withTimeInterval: config.tick, repeats: true) { _ in
    for s in keys.drainSteps() {
        guard let from = CGEvent(source: nil)?.location else { continue }
        let to = clamp(step(digit: s.digit, left: s.left, right: s.right,
                            up: s.up, down: s.down, from: from, config))
        CGWarpMouseCursorPosition(to)
        // A button down means this is a drag, and apps track those by their own
        // event type rather than by `mouseMoved`.
        let leftDown = CGEventSource.buttonState(.combinedSessionState, button: .left)
        let rightDown = CGEventSource.buttonState(.combinedSessionState, button: .right)
        let (kind, button): (CGEventType, CGMouseButton) =
            leftDown ? (.leftMouseDragged, .left)
            : rightDown ? (.rightMouseDragged, .right)
            : (.mouseMoved, .left)
        CGEvent(mouseEventSource: nil, mouseType: kind,
                mouseCursorPosition: to, mouseButton: button)?.post(tap: .cghidEventTap)
        if watch {
            print(String(format: "step %d cells -> %.0f,%.0f", s.digit == 0 ? 10 : s.digit, to.x, to.y))
            fflush(Foundation.stdout)
        }
    }

    let v = keys.velocity(config)
    let holding = v.x != 0 || v.y != 0

    var step = (x: 0.0, y: 0.0)
    var momentum = Momentum.none

    if holding {
        // Held keys cancel any coast: pressing again takes control back.
        coast = (0, 0)
        coasting = false
        step = (v.x * config.tick, v.y * config.tick)
    } else if coasting {
        coast = (coast.x * config.decay, coast.y * config.decay)
        step = coast
        momentum = .continue
        if abs(coast.x) < 1 && abs(coast.y) < 1 {
            coasting = false
            postScroll(dx: 0, dy: 0, phase: .none, momentum: .end)
            carry = (0, 0)
            if watch { print("coast ended"); fflush(Foundation.stdout) }
            return
        }
    } else if scrolling {
        // Keys just came up: close the gesture, then hand over to momentum.
        scrolling = false
        postScroll(dx: 0, dy: 0, phase: .ended, momentum: .none)
        if config.coasts && (abs(coast.x) >= 1 || abs(coast.y) >= 1) {
            coasting = true
            postScroll(dx: 0, dy: 0, phase: .none, momentum: .begin)
        }
        carry = (0, 0)
        if watch { print("released"); fflush(Foundation.stdout) }
        return
    } else {
        return
    }

    // Whole pixels out, remainder kept: at the base speed one tick is barely
    // more than a pixel, and truncating each frame would quietly lose distance.
    carry = (carry.x + step.x * config.sign, carry.y + step.y * config.sign)
    let whole = (x: carry.x.rounded(.towardZero), y: carry.y.rounded(.towardZero))
    carry = (carry.x - whole.x, carry.y - whole.y)

    if holding {
        coast = step        // remember the last velocity to coast from
    }
    guard whole.x != 0 || whole.y != 0 else { return }

    let phase: Phase = momentum == .none ? (scrolling ? .changed : .began) : .none
    if momentum == .none { scrolling = true }
    postScroll(dx: Int32(whole.x), dy: Int32(whole.y), phase: phase, momentum: momentum)

    if watch {
        print(String(format: "v %7.1f,%7.1f  step %+3.0f,%+3.0f  phase %d momentum %d",
                     v.x, v.y, whole.x, whole.y, phase.rawValue, momentum.rawValue))
        fflush(Foundation.stdout)
    }
}
RunLoop.main.run()
