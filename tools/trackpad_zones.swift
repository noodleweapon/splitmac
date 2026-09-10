// trackpad_zones.swift — trackpad zones as Karabiner variables, with haptics.
//
// A stripped-down replacement for Karabiner-MultitouchExtension. That app only
// publishes finger counts per half/quarter of the pad; this one takes a list of
// rectangles and sets a Karabiner variable while a finger sits inside one, so a
// patch of the pad can arm a layer the same way a key does.
// Entering a zone ticks the Force Touch actuator and leaving it ticks again,
// because an invisible target with no feedback is unusable.
//
//   swiftc -O tools/trackpad_zones.swift -o tools/trackpad_zones
//   tools/trackpad_zones --watch        # calibrate: print contacts and zone hits
//   tools/trackpad_zones                # run: feed variables to karabiner_cli
//   tools/trackpad_zones --haptic-test  # fire every actuation ID, pick by feel
//   tools/trackpad_zones --selftest     # zone math only, no hardware
//
// Needs Input Monitoring permission, same as the real extension. Without it
// the process starts fine and no contact frames ever arrive — `--watch` shows
// an empty screen, which is the symptom.
//
// Config: trackpad_zones.json next to the binary, or
// ~/.config/karabiner/trackpad_zones.json, or --config PATH.

import CoreGraphics
import Foundation

// MARK: - Config

struct Zone: Decodable {
    let name: String
    let x: Double         // % from the left edge to the zone's left side
    let y: Double         // % from the top edge to the zone's top side
    let width: Double     // % of the pad's width
    let height: Double    // % of the pad's height
    let variable: String? // Karabiner variable to raise while a finger is inside
    let haptic: Bool?     // tick on enter and exit; default true
    let block_click: Bool?  // swallow clicks landing in here

    var buzzes: Bool { haptic ?? (variable != nil) }
    var blocksClicks: Bool { block_click ?? false }
}

struct Config: Decodable {
    let zones: [Zone]
    let release_delay_ms: Int?     // hysteresis, so a sloppy lift does not drop the zone
    let palm_threshold: Double?    // contact size above which a touch is ignored; 0 = off
    let min_pressure: Double?      // force needed to arm a zone; 0 = any touch
    let hysteresis: Double?        // % added to the radius once inside, kills edge chatter

    let haptic_enter_id: Int32?    // actuation ID fired on entry; 0 = silent
    let haptic_exit_id: Int32?     // actuation ID fired on exit; 0 = silent
    let haptic_args: [Double]?     // trailing MTActuatorActuate args, see hapticArgs

    var releaseDelay: TimeInterval { Double(release_delay_ms ?? 250) / 1000 }
    var palmSize: Double { palm_threshold ?? 0 }
    // Measured on this pad: `pressure` tracks force monotonically, 0-9 pairing
    // with a 0.50 median contact size and 90+ with 1.45. A firm press in the
    // zone rides 60-96 while a hand resting elsewhere sits around 35, so a
    // threshold in between answers to a deliberate press but not to a brush.
    // `size` cannot do this job — it only spans 0.5 to 1.9 in total.
    var minPressure: Double { min_pressure ?? 0 }
    var stickiness: Double { hysteresis ?? 1.5 }
    var enterID: Int32 { haptic_enter_id ?? 3 }
    var exitID: Int32 { haptic_exit_id ?? 3 }
    // MTActuatorActuate takes three more arguments after the actuation ID and
    // none of them are documented. Every combination is accepted (KERN_SUCCESS)
    // and 0,0,0 is what every tool passes, so they are a knob to feel out, not
    // a spec to follow: if one of them scales intensity, this is where to find
    // out. Order is (UInt32, Float, Float).
    var hapticArgs: (UInt32, Float, Float) {
        let a = haptic_args ?? []
        return (UInt32(a.count > 0 ? max(0, a[0]) : 0),
                Float(a.count > 1 ? a[1] : 0),
                Float(a.count > 2 ? a[2] : 0))
    }
    var variables: [String] { Array(Set(zones.compactMap { $0.variable })).sorted() }
}

// `grown` pushes every side of the rectangle out by that many percent for a
// finger already inside, so a contact jittering on the boundary does not chatter
// the variable (and the haptic) on and off.
func inside(_ z: Zone, x: Double, y: Double, grown: Double = 0) -> Bool {
    let g = grown / 100
    return x >= z.x / 100 - g && x <= (z.x + z.width) / 100 + g
        && y >= z.y / 100 - g && y <= (z.y + z.height) / 100 + g
}

// MARK: - MultitouchSupport

// The private framework hands back an array of C structs. Rather than mirror
// the whole 96-byte layout, read the four fields that matter by offset.
private let contactStride = 96
private let offState = 20, offX = 32, offY = 36
private let offSize = 48, offPressure = 52

struct Contact {
    let touching: Bool  // state 4 = on the surface; 1-3 and 5-7 are hover
    let x: Double       // 0 left .. 1 right
    let y: Double       // 0 top .. 1 bottom (framework reports bottom-up; flipped here)
    let size: Double
    let pressure: Double  // force, near enough; see Config.minPressure
}

func readContacts(_ base: UnsafeMutableRawPointer?, _ count: Int32) -> [Contact] {
    guard let base, count > 0 else { return [] }
    return (0..<Int(count)).map { i in
        let p = base.advanced(by: i * contactStride)
        return Contact(
            touching: p.loadUnaligned(fromByteOffset: offState, as: Int32.self) == 4,
            x: Double(p.loadUnaligned(fromByteOffset: offX, as: Float.self)),
            y: 1.0 - Double(p.loadUnaligned(fromByteOffset: offY, as: Float.self)),
            size: Double(p.loadUnaligned(fromByteOffset: offSize, as: Float.self)),
            pressure: Double(p.loadUnaligned(fromByteOffset: offPressure, as: Float.self)))
    }
}

typealias MTDeviceRef = UnsafeMutableRawPointer
typealias MTContactCallback = @convention(c) (MTDeviceRef?, UnsafeMutableRawPointer?, Int32, Double, Int32) -> Int32

struct Multitouch {
    typealias CreateList = @convention(c) () -> Unmanaged<CFMutableArray>?
    typealias Register = @convention(c) (MTDeviceRef, MTContactCallback) -> Void
    typealias Start = @convention(c) (MTDeviceRef, Int32) -> Void
    typealias GetDeviceID = @convention(c) (MTDeviceRef, UnsafeMutablePointer<UInt64>) -> Int32
    typealias ActuatorCreate = @convention(c) (UInt64) -> Unmanaged<CFTypeRef>?
    typealias ActuatorOpen = @convention(c) (CFTypeRef) -> Int32
    typealias Actuate = @convention(c) (CFTypeRef, Int32, UInt32, Float, Float) -> Int32

    let handle: UnsafeMutableRawPointer
    let createList: CreateList
    let register: Register
    let start: Start

    init?() {
        guard let lib = dlopen(
            "/System/Library/PrivateFrameworks/MultitouchSupport.framework/MultitouchSupport",
            RTLD_LAZY) else { return nil }
        handle = lib
        guard let c = Multitouch.sym(lib, "MTDeviceCreateList", CreateList.self),
              let r = Multitouch.sym(lib, "MTRegisterContactFrameCallback", Register.self),
              let s = Multitouch.sym(lib, "MTDeviceStart", Start.self) else { return nil }
        (createList, register, start) = (c, r, s)
    }

    static func sym<T>(_ lib: UnsafeMutableRawPointer, _ name: String, _ type: T.Type) -> T? {
        guard let s = dlsym(lib, name) else { return nil }
        return unsafeBitCast(s, to: type)
    }

    func devices() -> [MTDeviceRef] {
        guard let list = createList()?.takeUnretainedValue() else { return [] }
        return (0..<CFArrayGetCount(list)).compactMap {
            UnsafeMutableRawPointer(mutating: CFArrayGetValueAtIndex(list, $0))
        }
    }

    // The actuator is addressed by the multitouch device ID. Not the IOKit
    // registry entry ID the real extension uses for its own bookkeeping —
    // MTActuatorCreateFromDeviceID returns null for that one.
    func deviceID(of device: MTDeviceRef) -> UInt64? {
        guard let get = Multitouch.sym(handle, "MTDeviceGetDeviceID", GetDeviceID.self)
        else { return nil }
        var id: UInt64 = 0
        guard get(device, &id) == KERN_SUCCESS, id != 0 else { return nil }
        return id
    }
}

// MARK: - Haptics

final class Haptic {
    private let ref: CFTypeRef
    private let actuate: Multitouch.Actuate
    private let lock = NSLock()
    var args: (UInt32, Float, Float) = (0, 0, 0)

    // Actuation IDs the trackpad accepts. 1-6 are click weights, 15/16 are the
    // heavier and softer ends; which one feels right is taste, so --haptic-test
    // fires them all in order.
    static let knownIDs: [Int32] = [1, 2, 3, 4, 5, 6, 15, 16]

    init?(_ mt: Multitouch, device: MTDeviceRef) {
        guard let deviceID = mt.deviceID(of: device),
              let create = Multitouch.sym(mt.handle, "MTActuatorCreateFromDeviceID", Multitouch.ActuatorCreate.self),
              let open = Multitouch.sym(mt.handle, "MTActuatorOpen", Multitouch.ActuatorOpen.self),
              let act = Multitouch.sym(mt.handle, "MTActuatorActuate", Multitouch.Actuate.self),
              let handle = create(deviceID)?.takeRetainedValue()
        else { return nil }
        guard open(handle) == KERN_SUCCESS else { return nil }
        ref = handle
        actuate = act
    }

    func tick(_ actuationID: Int32) {
        guard actuationID != 0 else { return }
        lock.lock()
        _ = actuate(ref, actuationID, args.0, args.1, args.2)
        lock.unlock()
    }
}

// MARK: - State shared between the framework's callback thread and the tick

final class Zones {
    private let lock = NSLock()
    private var hitNow: Set<String> = []       // variables currently held
    private var insideNow: Set<String> = []    // zone names currently held
    private var lastHit: [String: Date] = [:]
    private var lastContacts: [Contact] = []
    private var blockingNow = false

    let config: Config
    // Called once per zone as a finger enters (true) or leaves (false) it.
    var onEdge: ((Zone, Bool) -> Void)?

    init(_ config: Config) { self.config = config }

    func ingest(_ contacts: [Contact], now: Date = Date()) {
        lock.lock()
        let wasInside = insideNow
        var zonesHit: Set<String> = []
        for c in contacts where c.touching {
            if config.palmSize > 0 && c.size > config.palmSize { continue }
            for z in config.zones {
                let held = wasInside.contains(z.name)
                // Press to arm, then half the force keeps it: the point is to
                // rest the finger there once the gate is open.
                if c.pressure < (held ? config.minPressure / 2 : config.minPressure) { continue }
                if inside(z, x: c.x, y: c.y, grown: held ? config.stickiness : 0) {
                    zonesHit.insert(z.name)
                }
            }
        }
        insideNow = zonesHit
        hitNow = Set(config.zones.filter { zonesHit.contains($0.name) }.compactMap { $0.variable })

        // Blocking needs every touching contact to be inside a blocking zone:
        // one finger parked in the region must not freeze a click made with
        // another finger outside it.
        let blockers = config.zones.filter { $0.blocksClicks }
        let live = contacts.filter { $0.touching }
        blockingNow = !blockers.isEmpty && !live.isEmpty && live.allSatisfy { c in
            blockers.contains { inside($0, x: c.x, y: c.y) }
        }
        for v in hitNow { lastHit[v] = now }
        lastContacts = contacts
        lock.unlock()

        // Outside the lock: the actuator call is a few microseconds, but the
        // callback thread is the one delivering contact frames.
        guard let onEdge else { return }
        for z in config.zones where z.buzzes {
            let now = zonesHit.contains(z.name), before = wasInside.contains(z.name)
            if now != before { onEdge(z, now) }
        }
    }

    // Held variables stay up for release_delay_ms after the finger leaves. The
    // haptic does not wait for that — the tick reports the finger, not the gate.
    func current(now: Date = Date()) -> [String: Int] {
        lock.lock(); defer { lock.unlock() }
        var out: [String: Int] = [:]
        for v in config.variables {
            let held = hitNow.contains(v)
                || (lastHit[v].map { now.timeIntervalSince($0) < config.releaseDelay } ?? false)
            out[v] = held ? 1 : 0
        }
        return out
    }

    func contacts() -> [Contact] {
        lock.lock(); defer { lock.unlock() }
        return lastContacts
    }

    func blockingClicks() -> Bool {
        lock.lock(); defer { lock.unlock() }
        return blockingNow
    }
}

// MARK: - Output

// karabiner_cli reads one JSON object per line and pokes the same variables the
// multitouch extension uses, so ordinary variable_if/variable_unless works.
final class VariableSink {
    private let stdin: FileHandle?
    private var last: [String: Int] = [:]
    private let printOnly: Bool

    init(printOnly: Bool) {
        self.printOnly = printOnly
        guard !printOnly else { stdin = nil; return }
        let p = Process()
        p.executableURL = URL(fileURLWithPath:
            "/Library/Application Support/org.pqrs/Karabiner-Elements/bin/karabiner_cli")
        p.arguments = ["--set-variables-from-stdin"]
        let pipe = Pipe()
        p.standardInput = pipe
        do { try p.run() } catch {
            FileHandle.standardError.write("cannot start karabiner_cli: \(error)\n".data(using: .utf8)!)
            exit(1)
        }
        stdin = pipe.fileHandleForWriting
    }

    func publish(_ values: [String: Int]) {
        guard values != last else { return }
        last = values
        let body = values.keys.sorted().map { "\"\($0)\":\(values[$0]!)" }.joined(separator: ",")
        let line = "{\(body)}\n"
        if printOnly { print(line, terminator: ""); fflush(Foundation.stdout) }
        else { stdin?.write(line.data(using: .utf8)!) }
    }
}

// MARK: - Click blocking

// Dropping the event at the HID tap stops the click from doing anything. It
// does not stop the click from being *felt*: the driver actuates when force
// crosses the threshold, upstream of this, and nothing here can reach that.
// System Settings has the only levers for the feel (Silent Clicking, or a
// firmer click threshold).
func startClickBlocker() -> Bool {
    let events: [CGEventType] = [.leftMouseDown, .leftMouseUp, .rightMouseDown, .rightMouseUp]
    // NSEvent's pressure/force-click stage events have no CGEventType case.
    let pressureEvent: UInt32 = 34
    let mask = events.reduce(UInt64(1) << pressureEvent) { $0 | (1 << $1.rawValue) }

    let callback: CGEventTapCallBack = { proxy, type, event, _ in
        if type == .tapDisabledByTimeout || type == .tapDisabledByUserInput {
            if let tap = clickTap { CGEvent.tapEnable(tap: tap, enable: true) }
            return Unmanaged.passUnretained(event)
        }
        return zones.blockingClicks() ? nil : Unmanaged.passUnretained(event)
    }

    guard let tap = CGEvent.tapCreate(tap: .cghidEventTap,
                                      place: .headInsertEventTap,
                                      options: .defaultTap,
                                      eventsOfInterest: CGEventMask(mask),
                                      callback: callback,
                                      userInfo: nil) else { return false }
    clickTap = tap
    CFRunLoopAddSource(CFRunLoopGetMain(),
                       CFMachPortCreateRunLoopSource(nil, tap, 0),
                       .commonModes)
    return true
}

// MARK: - Wiring

func loadConfig(_ explicit: String?) -> Config {
    let exeDir = URL(fileURLWithPath: CommandLine.arguments[0])
        .resolvingSymlinksInPath().deletingLastPathComponent()
    let candidates = [
        explicit.map { URL(fileURLWithPath: $0) },
        exeDir.appendingPathComponent("trackpad_zones.json"),
        FileManager.default.homeDirectoryForCurrentUser
            .appendingPathComponent(".config/karabiner/trackpad_zones.json"),
    ].compactMap { $0 }

    for url in candidates {
        guard let data = try? Data(contentsOf: url) else { continue }
        do { return try JSONDecoder().decode(Config.self, from: data) } catch {
            FileHandle.standardError.write("bad config \(url.path): \(error)\n".data(using: .utf8)!)
            exit(1)
        }
    }
    FileHandle.standardError.write("no config found: \(candidates.map(\.path))\n".data(using: .utf8)!)
    exit(1)
}

func selftest() {
    let cfg = Config(
        zones: [Zone(name: "a", x: 25, y: 0, width: 50, height: 5,
                     variable: "gate", haptic: nil, block_click: nil),
                Zone(name: "b", x: 80, y: 0, width: 10, height: 5,
                     variable: "shift", haptic: nil, block_click: nil),
                Zone(name: "top", x: 0, y: 0, width: 100, height: 20,
                     variable: nil, haptic: nil, block_click: true)],
        release_delay_ms: 250, palm_threshold: 4.0, min_pressure: 55,
        hysteresis: 1.5, haptic_enter_id: 3, haptic_exit_id: 3, haptic_args: [0, 0.5])
    let gate = cfg.zones[0], shift = cfg.zones[1]

    precondition(inside(gate, x: 0.50, y: 0.00), "middle of the top edge hits")
    precondition(inside(gate, x: 0.25, y: 0.05), "the far corner still counts as inside")
    precondition(!inside(gate, x: 0.24, y: 0.00), "left of the rectangle misses")
    precondition(!inside(gate, x: 0.76, y: 0.00), "right of the rectangle misses")
    precondition(!inside(gate, x: 0.50, y: 0.06), "below the rectangle misses")
    precondition(!inside(shift, x: 0.50, y: 0.00), "a different rectangle is unaffected")
    precondition(inside(gate, x: 0.50, y: 0.06, grown: 1.5), "hysteresis holds on")

    // Clicks are blocked only when every touching contact is in a blocking
    // zone, so a finger parked up top cannot freeze a click made lower down.
    let blocker = Zones(cfg)
    blocker.ingest([Contact(touching: true, x: 0.50, y: 0.10, size: 1.0, pressure: 90)])
    precondition(blocker.blockingClicks(), "a contact in the top 20% blocks clicks")
    blocker.ingest([Contact(touching: true, x: 0.50, y: 0.10, size: 1.0, pressure: 90),
                    Contact(touching: true, x: 0.50, y: 0.60, size: 1.0, pressure: 90)])
    precondition(!blocker.blockingClicks(), "a second contact below it does not")
    blocker.ingest([])
    precondition(!blocker.blockingClicks(), "no contacts, no blocking")

    precondition(cfg.hapticArgs == (0, 0.5, 0), "short args list pads with zeros")

    // A touch in one zone must not raise the other zone's variable, must decay
    // after the release delay, and a palm-sized contact must not count at all.
    let z = Zones(cfg)
    var edges: [String] = []
    z.onEdge = { zone, entered in edges.append("\(entered ? "+" : "-")\(zone.name)") }
    let t0 = Date()

    // A finger merely resting in the zone is not enough.
    z.ingest([Contact(touching: true, x: 0.50, y: 0.0, size: 1.0, pressure: 35)], now: t0)
    precondition(z.current(now: t0)["gate"] == 0, "a light touch does not arm")
    precondition(edges.isEmpty, "a light touch fires no edge: \(edges)")

    z.ingest([Contact(touching: true, x: 0.50, y: 0.0, size: 1.4, pressure: 70)], now: t0)
    precondition(z.current(now: t0) == ["gate": 1, "shift": 0], "only the touched zone is up")
    precondition(edges == ["+a"], "entering fires one edge: \(edges)")

    // Easing off keeps it: half the force holds what a full press armed.
    z.ingest([Contact(touching: true, x: 0.50, y: 0.0, size: 1.0, pressure: 30)], now: t0)
    precondition(edges == ["+a"], "easing off does not drop it: \(edges)")

    // Boundary chatter: 6% down is below the rectangle but inside the grown one.
    z.ingest([Contact(touching: true, x: 0.50, y: 0.06, size: 1.4, pressure: 70)], now: t0)
    precondition(edges == ["+a"], "hysteresis suppresses the chatter: \(edges)")

    z.ingest([], now: t0)
    precondition(edges == ["+a", "-a"], "leaving fires one edge: \(edges)")
    precondition(z.current(now: t0.addingTimeInterval(0.1))["gate"] == 1, "still held during the delay")
    precondition(z.current(now: t0.addingTimeInterval(0.3))["gate"] == 0, "released after the delay")

    z.ingest([Contact(touching: true, x: 0.50, y: 0.0, size: 5.0, pressure: 70)], now: t0)
    precondition(z.current(now: t0.addingTimeInterval(0.3))["gate"] == 0, "palm-sized contact ignored")

    z.ingest([Contact(touching: false, x: 0.50, y: 0.0, size: 1.4, pressure: 70)], now: t0)
    precondition(z.current(now: t0.addingTimeInterval(0.3))["gate"] == 0, "hovering contact ignored")
    precondition(edges == ["+a", "-a"], "ignored contacts fire no edges: \(edges)")

    print("selftest ok")
}

// ponytail: globals, because the C callback has nowhere to carry context.
nonisolated(unsafe) var zones: Zones!
nonisolated(unsafe) var sanityWarned = false
nonisolated(unsafe) var clickTap: CFMachPort?

let contactCallback: MTContactCallback = { _, data, count, _, _ in
    let contacts = readContacts(data, count)
    // A wrong struct stride is the one failure mode that looks like bad
    // calibration, so say it out loud instead of publishing nonsense.
    if !sanityWarned, let c = contacts.first, c.x < -0.1 || c.x > 1.1 || c.y < -0.1 || c.y > 1.1 {
        sanityWarned = true
        FileHandle.standardError.write(
            "contact at (\(c.x), \(c.y)) is outside the pad: MultitouchSupport layout changed?\n"
                .data(using: .utf8)!)
    }
    zones.ingest(contacts)
    return 0
}

let args = CommandLine.arguments
if args.contains("--selftest") { selftest(); exit(0) }

let watch = args.contains("--watch")
let hapticTest = args.contains("--haptic-test")
func flag(_ name: String) -> String? {
    args.firstIndex(of: name).flatMap { args.indices.contains($0 + 1) ? args[$0 + 1] : nil }
}
let configPath = flag("--config")
// Overrides for feeling out the undocumented arguments without editing config.
let argsOverride = flag("--haptic-args").map { spec -> (UInt32, Float, Float) in
    let n = spec.split(separator: ",").map { Double($0) ?? 0 }
    return (UInt32(n.count > 0 ? max(0, n[0]) : 0),
            Float(n.count > 1 ? n[1] : 0),
            Float(n.count > 2 ? n[2] : 0))
}
let idOverride = flag("--id").flatMap { Int32($0) }

guard let mt = Multitouch() else {
    FileHandle.standardError.write("cannot load MultitouchSupport\n".data(using: .utf8)!)
    exit(1)
}
let devices = mt.devices()
guard let pad = devices.first else {
    FileHandle.standardError.write("no multitouch devices\n".data(using: .utf8)!)
    exit(1)
}
let haptic = Haptic(mt, device: pad)

if hapticTest {
    guard let haptic else {
        FileHandle.standardError.write("no actuator on this trackpad\n".data(using: .utf8)!)
        exit(1)
    }
    haptic.args = argsOverride ?? (0, 0, 0)
    for id in idOverride.map({ [$0] }) ?? Haptic.knownIDs {
        print("actuation ID \(id) args \(haptic.args)")
        fflush(Foundation.stdout)
        haptic.tick(id)
        Thread.sleep(forTimeInterval: 0.8)
    }
    exit(0)
}

zones = Zones(loadConfig(configPath))
if let haptic {
    haptic.args = argsOverride ?? zones.config.hapticArgs
    zones.onEdge = { [config = zones.config] _, entered in
        haptic.tick(entered ? config.enterID : config.exitID)
    }
} else {
    FileHandle.standardError.write("no actuator on this trackpad, running without haptics\n"
        .data(using: .utf8)!)
}

if zones.config.zones.contains(where: { $0.blocksClicks }) && !startClickBlocker() {
    // The tap needs Accessibility, which is a separate grant from the Input
    // Monitoring the contact frames need.
    FileHandle.standardError.write(("cannot create the event tap: grant Accessibility to "
        + "this binary in System Settings > Privacy & Security > Accessibility. "
        + "Zones still work, clicks are not blocked.\n").data(using: .utf8)!)
}

for d in devices {
    mt.register(d, contactCallback)
    mt.start(d, 0)
}

let sink = watch ? nil : VariableSink(printOnly: args.contains("--print"))
if watch {
    print("zones: " + zones.config.zones.map {
        "\($0.name)@\(Int($0.x))-\(Int($0.x + $0.width))% x \(Int($0.y))-\(Int($0.y + $0.height))% -> \($0.variable ?? "clicks blocked")"
    }.joined(separator: "  "))
}

Timer.scheduledTimer(withTimeInterval: 0.02, repeats: true) { _ in
    let values = zones.current()
    if watch {
        let touching = zones.contacts().filter(\.touching)
        guard !touching.isEmpty || values.values.contains(1) else { return }
        let fingers = touching.map {
            String(format: "%3.0f%%,%3.0f%% size %.2f pressure %.1f",
                   $0.x * 100, $0.y * 100, $0.size, $0.pressure)
        }.joined(separator: " | ")
        let up = values.filter { $0.value > 0 }.keys.sorted().joined(separator: ",")
        let blocked = zones.blockingClicks() ? "  [clicks blocked]" : ""
        print("\(fingers)   \(up.isEmpty ? "-" : up)\(blocked)")
        fflush(Foundation.stdout)
    } else {
        sink?.publish(values)
    }
}
RunLoop.main.run()
