// orbital_mouse.swift — tank controls for the mouse pointer.
//
//   up / down     drive forward and backward along the pointer's heading
//   left / right  rotate in place about the dot drawn a few pixels ahead of
//                 the pointer, which is the centre of rotation
//
// A tank, not a car: turning does not carry the pointer anywhere, it swings it
// around that dot. The dot sits `orbit_radius` pixels along the heading and is
// derived every tick as `position + radius * heading`, never stored, so a pure
// turn leaves it exactly where it is — the pointer sweeps a true circle around
// it with no integration error, and driving carries pointer and dot together.
// The pair is the heading readout: the dot marks which way the pointer faces.
//
// Karabiner cannot do this — `mouse_key` is constant velocity along a fixed
// axis, with no heading to steer. So Karabiner just reports the arrow keys over
// UDP (`printf l1 > /dev/udp/127.0.0.1/45454`, which /bin/sh supports) and this
// integrates them. `b1`/`b0` is the boost key: while it is held, both the turn
// angle and the drive distance are multiplied by `fast_multiplier`. No event
// tap, no Accessibility grant, and if this is not running the writes are
// dropped and the arrows simply do nothing.
//
//   swiftc -O tools/orbital_mouse.swift -o tools/orbital_mouse
//   tools/orbital_mouse             # run it
//   tools/orbital_mouse --watch     # print heading and pivot as you steer
//   tools/orbital_mouse --selftest  # orbit maths, no hardware
//
// Config: orbital_mouse.json next to the binary, or
// ~/.config/karabiner/orbital_mouse.json, or --config PATH.

import AppKit
import CoreGraphics
import Foundation

// MARK: - Config

struct Config: Decodable {
    let port: UInt16?
    let orbit_radius: Double?             // px from pointer to pivot
    let turn_degrees_per_second: Double?
    let forward_speed: Double?            // px/s
    let tick_hz: Double?
    let pivot_dot: Bool?      // draw the centre of rotation
    let dot_size: Double?
    let fast_multiplier: Double?   // how much quicker the boost key is
    let reverse_ratio: Double?     // reverse as a fraction of the forward speed
    let slide_drive_px: Double?      // pointer travel for a full-width gate slide
    let slide_turn_degrees: Double?  // heading change for a full-width gate slide

    var udpPort: UInt16 { port ?? 45454 }
    var radius: Double { orbit_radius ?? 120 }
    var turnRate: Double { (turn_degrees_per_second ?? 180) * .pi / 180 }
    var speed: Double { forward_speed ?? 800 }
    var tick: Double { 1.0 / (tick_hz ?? 120) }
    var drawsDot: Bool { pivot_dot ?? true }
    var dotSize: CGFloat { dot_size ?? 9 }
    var fast: Double { fast_multiplier ?? 2 }
    var reverse: Double { reverse_ratio ?? 0.5 }
    var slideDrive: Double { slide_drive_px ?? 3000 }
    var slideTurn: Double { (slide_turn_degrees ?? 720) * .pi / 180 }
}

// MARK: - The pivot dot

// The regular cursor stays exactly as it is; this only adds a dot marking the
// centre of rotation, in a borderless overlay window that follows it.

// CoreGraphics global coordinates put the origin at the top-left of the primary
// screen and count y downwards; AppKit windows count y up from its bottom-left.
func appKitY(_ cgY: CGFloat) -> CGFloat {
    let primary = NSScreen.screens.first { $0.frame.origin == .zero } ?? NSScreen.screens.first
    return (primary?.frame.maxY ?? 0) - cgY
}

final class DotView: NSView {
    override func draw(_ dirtyRect: NSRect) {
        let dot = bounds.insetBy(dx: 1.5, dy: 1.5)
        NSColor.black.setFill()
        NSColor.white.setStroke()
        let path = NSBezierPath(ovalIn: dot)
        path.lineWidth = 1.5
        path.fill()
        path.stroke()
    }
}

final class PivotDot {
    private let window: NSWindow
    private let size: CGFloat

    init(size: CGFloat) {
        self.size = size
        let view = DotView(frame: NSRect(x: 0, y: 0, width: size, height: size))
        window = NSWindow(contentRect: view.frame, styleMask: .borderless,
                          backing: .buffered, defer: false)
        window.contentView = view
        window.isOpaque = false
        window.backgroundColor = .clear
        window.hasShadow = false
        window.ignoresMouseEvents = true
        // Above everything, on every space, and never stealing focus.
        window.level = NSWindow.Level(rawValue: Int(CGShieldingWindowLevel()))
        window.collectionBehavior = [.canJoinAllSpaces, .stationary, .ignoresCycle,
                                     .fullScreenAuxiliary]
        window.orderFrontRegardless()
    }

    func update(at p: CGPoint) {
        window.setFrameOrigin(NSPoint(x: p.x - size / 2, y: appKitY(p.y) - size / 2))
    }
}

// MARK: - The rig

// Screen coordinates run y-down, so a rising angle reads as clockwise. Heading
// starts pointing up the screen, which is the direction "forward" implies.
struct Rig {
    var position: CGPoint
    var heading: Double = -.pi / 2

    var facing: CGPoint { CGPoint(x: cos(heading), y: sin(heading)) }

    /// The centre of rotation: `radius` px ahead along the heading. This is the
    /// dot that gets drawn.
    func pivot(_ radius: Double) -> CGPoint {
        CGPoint(x: position.x + radius * facing.x, y: position.y + radius * facing.y)
    }

    /// A finger sliding on a gate asks for an exact angle or an exact distance,
    /// not a rate held over time. Same geometry as `step`, applied once.
    mutating func apply(turnAngle: Double, driveDistance: Double, config: Config) {
        if turnAngle != 0 {
            let c = pivot(config.radius)
            let (dx, dy) = (position.x - c.x, position.y - c.y)
            position = CGPoint(x: c.x + dx * cos(turnAngle) - dy * sin(turnAngle),
                               y: c.y + dx * sin(turnAngle) + dy * cos(turnAngle))
            heading += turnAngle
        }
        if driveDistance != 0 {
            let distance = driveDistance * (driveDistance < 0 ? config.reverse : 1)
            position = CGPoint(x: position.x - distance * facing.x,
                               y: position.y - distance * facing.y)
        }
    }

    /// turn: -1 left, +1 right. drive: +1 forward, -1 back.
    mutating func step(turn: Double, drive: Double, dt: Double, config: Config) {
        if turn != 0 {
            // Rotate the position about the pivot and the heading by the same
            // angle. Doing both keeps the pivot where it is and the radius
            // exact, instead of approximating the circle with straight steps.
            let c = pivot(config.radius)
            let angle = turn * config.turnRate * dt
            let (dx, dy) = (position.x - c.x, position.y - c.y)
            position = CGPoint(x: c.x + dx * cos(angle) - dy * sin(angle),
                               y: c.y + dx * sin(angle) + dy * cos(angle))
            heading += angle
        }
        if drive != 0 {
            // Driving runs *away* from the dot: the dot sits ahead of the
            // pointer along the heading, so `up` pushing the pointer the other
            // way is what reads as forward in the hand. Reverse is slower, the
            // way reverse gear is — you use it to correct, not to travel.
            let rate = drive < 0 ? config.reverse : 1
            let step = -drive * config.speed * rate * dt
            position = CGPoint(x: position.x + step * facing.x,
                               y: position.y + step * facing.y)
        }
    }
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

// MARK: - Keys over UDP

// Two kinds of word arrive here. Karabiner sends a held key as two bytes: `l`,
// `r`, `u`, `d` for the four directions or `b` for boost, then 1 for down and 0
// for up. trackpad_zones sends a gate slide as `D` or `T` followed by a signed
// fraction of the pad's width — an impulse to apply once, not a state.
final class Keys {
    private let lock = NSLock()
    private var held: Set<Character> = []
    private var pendingDrive = 0.0     // fractions of the pad's width
    private var pendingTurn = 0.0
    private let fast: Double

    init(fast: Double) { self.fast = fast }

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
                guard let kind = word.first else { continue }
                if kind == "D" || kind == "T" {
                    guard let amount = Double(word.dropFirst()) else { continue }
                    lock.lock()
                    if kind == "D" { pendingDrive += amount } else { pendingTurn += amount }
                    lock.unlock()
                    continue
                }
                guard "lrudb".contains(kind) else { continue }
                lock.lock()
                if word.dropFirst().first == "1" { held.insert(kind) } else { held.remove(kind) }
                lock.unlock()
            }
        }
    }

    func axes() -> (turn: Double, drive: Double) {
        lock.lock(); defer { lock.unlock() }
        // Boost scales both axes: it is a rate, not a direction of its own.
        let rate = held.contains("b") ? fast : 1
        func axis(_ positive: Character, _ negative: Character) -> Double {
            ((held.contains(positive) ? 1.0 : 0) - (held.contains(negative) ? 1.0 : 0)) * rate
        }
        return (axis("r", "l"), axis("u", "d"))
    }

    /// Slide impulses accumulated since the last tick, in pad-width fractions.
    func drainSlide() -> (turn: Double, drive: Double) {
        lock.lock(); defer { lock.unlock() }
        let pending = (pendingTurn, pendingDrive)
        (pendingTurn, pendingDrive) = (0, 0)
        return pending
    }
}

// MARK: - Checks

func selftest() {
    let cfg = Config(port: nil, orbit_radius: 120, turn_degrees_per_second: 180,
                     forward_speed: 800, tick_hz: 120, pivot_dot: false, dot_size: nil, fast_multiplier: 2, reverse_ratio: 0.5, slide_drive_px: 3000, slide_turn_degrees: 720)
    let dt = 1.0 / 120

    // A pure turn is rotation in place: the pivot does not budge, the radius
    // holds, and 360 degrees of it comes back to where it started.
    var rig = Rig(position: CGPoint(x: 500, y: 500))
    let pivot = rig.pivot(cfg.radius)
    precondition(abs(pivot.x - 500) < 0.001 && abs(pivot.y - (500 - cfg.radius)) < 0.001,
                 "facing up, the pivot sits directly above: \(pivot)")
    for _ in 0..<240 {
        rig.step(turn: -1, drive: 0, dt: dt, config: cfg)
        let moved = rig.pivot(cfg.radius)
        precondition(hypot(moved.x - pivot.x, moved.y - pivot.y) < 0.001, "pivot stays put")
        precondition(abs(hypot(rig.position.x - pivot.x, rig.position.y - pivot.y) - cfg.radius) < 0.001,
                     "radius holds")
    }
    precondition(hypot(rig.position.x - 500, rig.position.y - 500) < 0.001,
                 "360 degrees returns to the start: \(rig.position)")

    // Turning swings the pointer sideways around the pivot rather than driving
    // it forward. One tick is a chord, so it leans along the heading by exactly
    // radius * (1 - cos dTheta) — second order in the step.
    var swing = Rig(position: CGPoint(x: 500, y: 500))
    let facing = swing.facing
    swing.step(turn: -1, drive: 0, dt: dt, config: cfg)
    let moved = CGPoint(x: swing.position.x - 500, y: swing.position.y - 500)
    let dTheta = cfg.turnRate * dt
    let along = moved.x * facing.x + moved.y * facing.y
    let sideways = -moved.x * facing.y + moved.y * facing.x
    precondition(abs(along - cfg.radius * (1 - cos(dTheta))) < 0.001,
                 "only the chord's lean forwards: \(along)")
    precondition(abs(abs(sideways) - cfg.radius * sin(dTheta)) < 0.001,
                 "a chord's worth of sideways: \(sideways)")
    precondition(abs(sideways) > abs(along) * 50, "the motion is sideways: \(moved)")

    // A tank turns on the spot: however long you hold it, the pointer never
    // gets further from where it started than the pivot circle's diameter.
    var spin = Rig(position: CGPoint(x: 500, y: 500))
    for _ in 0..<60 { spin.step(turn: -1, drive: 0, dt: dt, config: cfg) }
    precondition(hypot(spin.position.x - 500, spin.position.y - 500) <= 2 * cfg.radius + 0.001,
                 "rotation stays put: \(spin.position)")
    precondition(spin.heading < -.pi / 2, "left turns anticlockwise: \(spin.heading)")
    var right = Rig(position: CGPoint(x: 500, y: 500))
    for _ in 0..<60 { right.step(turn: 1, drive: 0, dt: dt, config: cfg) }
    precondition(right.heading > -.pi / 2, "right turns clockwise: \(right.heading)")
    precondition(abs((500 - spin.position.x) - (right.position.x - 500)) < 0.001
                 && abs(spin.position.y - right.position.y) < 0.001, "they mirror")

    // Driving follows the heading, and back undoes forward.
    var drive = Rig(position: CGPoint(x: 500, y: 500))
    drive.step(turn: 0, drive: 1, dt: dt, config: cfg)
    precondition(abs(drive.position.x - 500) < 0.001, "no sideways drift")
    precondition(abs(drive.position.y - (500 + cfg.speed * dt)) < 0.001,
                 "forward runs away from the dot, which sits ahead: \(drive.position)")
    // Reverse is `reverse_ratio` of forward, so one tick back does not undo one
    // tick forward — it undoes half of it.
    let forward = drive.position.y - 500
    drive.step(turn: 0, drive: -1, dt: dt, config: cfg)
    precondition(abs((drive.position.y - 500) - forward * (1 - cfg.reverse)) < 0.001,
                 "back is half a step: \(drive.position)")
    var far = Rig(position: CGPoint(x: 500, y: 500))
    far.step(turn: 0, drive: -1, dt: dt, config: cfg)
    precondition(abs((500 - far.position.y) - cfg.reverse * cfg.speed * dt) < 0.001,
                 "reverse runs at half speed: \(far.position)")

    // The fast keys are the same geometry, twice over: double the angle for a
    // turn, double the distance for a drive.
    var slow = Rig(position: CGPoint(x: 500, y: 500))
    var quick = Rig(position: CGPoint(x: 500, y: 500))
    slow.step(turn: 0, drive: 1, dt: dt, config: cfg)
    quick.step(turn: 0, drive: 2, dt: dt, config: cfg)
    precondition(abs((quick.position.y - 500) - 2 * (slow.position.y - 500)) < 0.001,
                 "fast drive is twice as far: \(quick.position)")
    slow = Rig(position: CGPoint(x: 500, y: 500))
    quick = Rig(position: CGPoint(x: 500, y: 500))
    slow.step(turn: -1, drive: 0, dt: dt, config: cfg)
    quick.step(turn: -2, drive: 0, dt: dt, config: cfg)
    precondition(abs((quick.heading + .pi / 2) - 2 * (slow.heading + .pi / 2)) < 0.001,
                 "fast turn is twice the angle: \(quick.heading)")
    precondition(abs(hypot(quick.position.x - 500, quick.position.y - 500)
                     - 2 * cfg.radius * sin(cfg.turnRate * dt)) < 0.01,
                 "and still exactly on the circle")

    // A slide impulse is the same geometry, applied once: an exact angle about
    // the pivot, an exact distance along the heading.
    var slid = Rig(position: CGPoint(x: 500, y: 500))
    let anchor = slid.pivot(cfg.radius)
    slid.apply(turnAngle: .pi / 2, driveDistance: 0, config: cfg)
    precondition(hypot(slid.pivot(cfg.radius).x - anchor.x,
                       slid.pivot(cfg.radius).y - anchor.y) < 0.001, "impulse keeps the pivot")
    precondition(abs(slid.heading - 0) < 0.001, "a quarter turn from facing up faces right")
    slid = Rig(position: CGPoint(x: 500, y: 500))
    slid.apply(turnAngle: 0, driveDistance: 100, config: cfg)
    precondition(abs(slid.position.y - 600) < 0.001, "a forward impulse runs away from the dot")
    slid = Rig(position: CGPoint(x: 500, y: 500))
    slid.apply(turnAngle: 0, driveDistance: -100, config: cfg)
    precondition(abs(slid.position.y - (500 - 100 * cfg.reverse)) < 0.001,
                 "and backwards is still halved: \(slid.position)")

    // Opposite keys cancel.
    var both = Rig(position: CGPoint(x: 500, y: 500))
    both.step(turn: 0, drive: 0, dt: dt, config: cfg)
    precondition(both.position == CGPoint(x: 500, y: 500) && both.heading == -.pi / 2,
                 "no keys, no motion")

    // The arrow lives in AppKit's y-up world and the pointer in CoreGraphics'
    // y-down one; getting this backwards puts the arrow on the wrong half of
    // the screen, mirrored about the middle.
    precondition(abs(appKitY(appKitY(400)) - 400) < 0.001, "the y flip is its own inverse")

    print("selftest ok")
}

// MARK: - Run

func loadConfig(_ explicit: String?) -> Config {
    let exeDir = URL(fileURLWithPath: CommandLine.arguments[0])
        .resolvingSymlinksInPath().deletingLastPathComponent()
    let candidates = [
        explicit.map { URL(fileURLWithPath: $0) },
        exeDir.appendingPathComponent("orbital_mouse.json"),
        FileManager.default.homeDirectoryForCurrentUser
            .appendingPathComponent(".config/karabiner/orbital_mouse.json"),
    ].compactMap { $0 }
    for url in candidates {
        guard let data = try? Data(contentsOf: url) else { continue }
        if let cfg = try? JSONDecoder().decode(Config.self, from: data) { return cfg }
        FileHandle.standardError.write("bad config \(url.path)\n".data(using: .utf8)!)
        exit(1)
    }
    return Config(port: nil, orbit_radius: nil, turn_degrees_per_second: nil,
                  forward_speed: nil, tick_hz: nil, pivot_dot: nil, dot_size: nil, fast_multiplier: nil, reverse_ratio: nil, slide_drive_px: nil, slide_turn_degrees: nil)
}

let args = CommandLine.arguments
if args.contains("--selftest") { selftest(); exit(0) }

let watch = args.contains("--watch")
let config = loadConfig(args.firstIndex(of: "--config").flatMap {
    args.indices.contains($0 + 1) ? args[$0 + 1] : nil
})

let app = NSApplication.shared
app.setActivationPolicy(.accessory)   // no dock icon, never takes focus

let keys = Keys(fast: config.fast)
keys.listen(port: config.udpPort)

let dot = config.drawsDot ? PivotDot(size: config.dotSize) : nil

var rig = Rig(position: CGEvent(source: nil)?.location ?? .zero)
var commanded = rig.position

print("orbital mouse on udp \(config.udpPort): radius \(Int(config.radius))px, "
    + "\(Int(config.turn_degrees_per_second ?? 180))°/s, \(Int(config.speed))px/s")

Timer.scheduledTimer(withTimeInterval: config.tick, repeats: true) { _ in
    let (turn, drive) = keys.axes()
    let slide = keys.drainSlide()
    let sliding = slide.turn != 0 || slide.drive != 0

    // The trackpad still owns the pointer. If it moved since we last placed it,
    // take that as the new truth and steer from there — and face up the screen
    // again. A tank keeps its heading when you carry it, but this heading is
    // invisible, so without the reset `up` would drive off along whatever angle
    // the last orbit happened to end on.
    if let actual = CGEvent(source: nil)?.location,
       hypot(actual.x - commanded.x, actual.y - commanded.y) > 2 {
        rig.position = actual
        rig.heading = -.pi / 2
        commanded = actual
    }

    if turn != 0 || drive != 0 || sliding {
        if sliding {
            rig.apply(turnAngle: slide.turn * config.slideTurn,
                      driveDistance: slide.drive * config.slideDrive, config: config)
        }
        rig.step(turn: turn, drive: drive, dt: config.tick, config: config)
        rig.position = clamp(rig.position)
        commanded = rig.position

        // Warp needs no permission but tells no app the pointer moved; the
        // posted event updates hover states when Accessibility happens to be
        // granted, and is silently dropped when it is not. Both set the same
        // absolute position.
        CGWarpMouseCursorPosition(rig.position)
        // A moving pointer with a button down is a drag, and apps track drags
        // by their own event type — posting `mouseMoved` instead would move the
        // cursor without dragging anything.
        let left = CGEventSource.buttonState(.combinedSessionState, button: .left)
        let right = CGEventSource.buttonState(.combinedSessionState, button: .right)
        let (kind, button): (CGEventType, CGMouseButton) =
            left ? (.leftMouseDragged, .left)
            : right ? (.rightMouseDragged, .right)
            : (.mouseMoved, .left)
        CGEvent(mouseEventSource: nil, mouseType: kind,
                mouseCursorPosition: rig.position, mouseButton: button)?.post(tap: .cghidEventTap)
    }

    // The dot tracks the pointer whether we moved it or the trackpad did.
    dot?.update(at: rig.pivot(config.radius))
    guard turn != 0 || drive != 0 || sliding else { return }

    if watch {
        let c = rig.pivot(config.radius)
        print(String(format: "turn %+.0f drive %+.0f  pos %6.1f,%6.1f  heading %6.1f°  pivot %6.1f,%6.1f",
                     turn, drive, rig.position.x, rig.position.y,
                     rig.heading * 180 / .pi, c.x, c.y))
        fflush(Foundation.stdout)
    }
}
app.run()
