# splitmac

Split-keyboard ergonomics on a stock MacBook, in one [kanata](https://github.com/jtroo/kanata) config.
The right hand moves a column over, the home row becomes modifiers and four hold
layers, and 26 keys you should stop reaching for are switched off.

No firmware. No external keyboard. One `.kbd` file.

<table>
  <tr>
    <td>
      <a href="https://www.pcbway.com/">
        <img alt="Sponsored by PCBWay" src="img/pcbway.png" width="400">
      </a>
    </td>
    <td>
      This project is sponsored by <a href="https://www.pcbway.com/">PCBWay</a>,
      a one-stop shop for PCB prototyping, assembly, CNC machining and 3D
      printing. If you want to turn a keymap like this one into a real split
      board, they are a good place to have it made — see
      <a href="#sponsor">Sponsor</a> below for what they offer.
    </td>
  </tr>
</table>

The small grey legend in the corner of each cap is what is physically printed on
it. The big legend is what the key actually does.

---

### Base

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="img/base-dark.svg">
  <img alt="Base layer" src="img/base-light.svg">
</picture>

### Hold gate and home-row mods

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="img/mods-dark.svg">
  <img alt="Hold gate and home-row mods" src="img/mods-light.svg">
</picture>

### Number layer

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="img/number-dark.svg">
  <img alt="Number layer" src="img/number-light.svg">
</picture>

### Symbol layer — left

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="img/sym-left-dark.svg">
  <img alt="Left symbol layer" src="img/sym-left-light.svg">
</picture>

### Symbol layer — right

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="img/sym-right-dark.svg">
  <img alt="Right symbol layer" src="img/sym-right-light.svg">
</picture>

### Navigation layer

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="img/nav-dark.svg">
  <img alt="Navigation layer" src="img/nav-light.svg">
</picture>

There is also an [interactive version](keymap.html) — open it and press keys on
your own keyboard to light up the matching cap, or hold Caps Lock and a layer
key to preview a layer live.

Inspired by [@getreuer's QMK keymap](https://github.com/getreuer/qmk-keymap),
which is the reference for what a well-documented personal keymap looks like.

---

## The idea

A laptop keyboard has no thumb cluster and no layer keys, so the usual QMK
tricks do not port over directly. This config works around that with three
moves:

1. **Everything worth reaching for moves onto the home row.** Numbers, symbols
   and arrows live on hold layers, not on the number row.
2. **Caps Lock and Return become a gate.** Hold either one and the home row
   turns into modifiers and layer keys. Let go and it is plain letters again —
   so there are no accidental mod-taps while typing at speed.
3. **The keys you should stop using are disabled.** The number row, `esc`,
   `tab`, `delete`, the arrow cluster and the three worst reaches on the alpha
   block do not do their job any more.

## Base layer

The alphas are [Gallium v2](https://github.com/GalileoBlues/Gallium), the
row-staggered variant of Gallium — which is the right choice here, because a
laptop keyboard is a row-staggered keyboard. Gallium v2 exists precisely for
boards like this one, rather than the column-staggered splits most alt layouts
are tuned for.

Fitting a 3×10 layout onto a MacBook means the top two rows of the right hand
sit **one column to the right** of where QWERTY puts them, which is what leaves
`Y`, `H` and `B` with nothing to do:

```
      B  L  D  C  V        J  F  O  U  ✦
      N  R  T  S  G        Y  H  A  E  I
   Z  X  Q  M  W              K  P  ,  .
```

That leading `Z` is **Left Shift** — the bottom row is one key short of a home
for it, so it moves onto the shift key and the old `Z` position (physical `N`)
is disabled too.

Punctuation that is normally shifted moves down to the shift keys themselves:

| Physical key | Types |
| --- | --- |
| Left Shift | `Z` |
| Right Shift | `'` |
| Left Command | tap `return`, hold `shift` |
| Right Option | tap `tab`, hold `shift` (left) |
| Right Command | `delete` |
| Left Option | `control` |
| Caps Lock / Return | hold to arm the layers, tap does nothing |
| Shift + `/` | `esc` |
| Shift + `.` | `⌥C` |

## The magic key

The `[` key has no letter of its own. It is a **magic key**: it emits whatever
should come after the letter you just typed. Thirteen of the layout's most
awkward bigrams are folded into one key that is always in the same place.

| You typed | `[` gives you | Bigram |
| --- | --- | --- |
| `p` | `y` | `py` — copy, type, happy |
| `s` | `c` | `sc` — scale, discuss |
| `u` | `e` | `ue` — value, queue |
| `r` | `l` | `rl` — world, early |
| `o` | `a` | `oa` — road, broad |
| `g` | `s` | `gs` — things, logs |
| `w` | `s` | `ws` — news, shows |
| `h` | `y` | `hy` — why, hyper |
| `t` | `m` | `tm` — batman, postman |
| `l` | `m` | `lm` — film, calm |
| `c` | `s` | `cs` — physics, basics |
| `m` | `c` | `mc` |
| `y` | `p` | `yp` — type, crypt |

After anything else — a digit, a symbol, a space, a fresh document — `[` does
nothing at all. Holding shift while you press it capitalises the letter, the
same way shift works on every other key here.

Each press feeds its own output back in, so the key chains: `r` `[` `[` `[` `[`
types `rlmcs`. Two of the pairs point at each other — `p`/`y` and `s`/`c` — so
repeated presses there simply alternate.

It reads the letter that *came out*, not the key you hit. That is one
`switch` on kanata's output history:

```lisp
(defalias
  magic (switch
    ((key-history p 1)) y break
    ((key-history s 1)) c break
    ;; ...
    () XX break))
```

`key-history` is the history of what kanata *emitted*, so there is no
bookkeeping to keep in sync — the key works after a tapped home-row mod, after
a layer glyph, after the trainer, and it chains for free because its own output
lands in the same history.

The hyphen and underscore that used to sit on this key are gone with it. `-`
moved to the left symbol layer; `_` and `~` moved to the number layer, on Right
Shift and on the magic key itself.

## Hold gate and home-row mods

Hold **Caps Lock** or **Return** to arm the gate — a `layer-while-held` onto
the `gate` layer. While it is held, four home-row keys become modifiers and
four become layer keys:

| Home-row key | Physical | Hold |
| --- | --- | --- |
| `T` | `D` | Left Command |
| `A` | `L` | Left Command |
| `R` | `S` | Left Option |
| `E` | `;` | Left Option |
| `S` | `F` | Number layer |
| `H` | `K` | Navigation layer |
| `M` | `C` | Symbol layer, right |
| `P` | `,` | Symbol layer, left |

Every one of them sends the **left-hand** modifier — Left Command, Left Option,
Left Shift — whichever side of the board you hold it on. Nothing on this board
emits a right-hand modifier any more, so apps that tell the two sides apart
only ever see the left one.

The gate is the whole trick. Home-row mods normally misfire during fast typing;
here they do not exist at all until you ask for them, because the eight mod and
layer keys are only defined inside the `gate` layer. Outside it they are eight
plain letters and there is nothing to misfire.

All eight are written the same way:

```lisp
(defalias
  m-t  (tap-hold-press $tap $hold t lmet)                       ;; Command
  l-s  (tap-hold-press $tap $hold s (layer-while-held num)))    ;; layer
```

`tap-hold-press` resolves to the hold the instant any other key goes down, so a
modifier or a layer is there as soon as you need it and never waits out a
timer; the 200 ms timeout only decides an *idle* hold. Tap it and you get the
letter. Hold the layer first or the modifier first — the result is identical.

One thing the gate cannot make order-free: it has to be held *first*. The mod
and layer keys live in the `gate` layer, so a key pressed before Caps Lock is
still an ordinary letter.

Each layer also borrows some home-row keys for its own glyphs, which shadows the
modifier on those keys. One pair always survives:

| Layer (held with) | Modifiers still reachable |
| --- | --- |
| Number — physical `F` | Left Command `D`, Left Option `S` |
| Symbol right — physical `C` | Left Command `D`, Left Option `S` |
| Symbol left — physical `,` | Left Command `L`, Left Option `;` |
| Navigation — physical `K` | Left Command `L`, Left Option `;` |

In every case the surviving pair is on the same hand that holds the layer, which
takes some getting used to. The other hand's Command and Option are typing layer
glyphs and cannot also be modifiers.

## The layers

**Number** — gate + hold `S`. Digits sit under the right hand, with `~` on the
magic key and `_` on Right Shift:

```
   7  8  9  ~     F O U ✦
   0  1  2  3     H A E I
      4  5  6  _     K P , . '
```

**Symbol, left** — gate + hold `P`. Held by the right hand, typed with the left:

```
   ^  *  -  |     B L D C
   +  !  /  =     N R T S
`  <  >  @        Z X Q M
```

**Symbol, right** — gate + hold `M`. Held by the left hand, typed with the right:

```
   ;  &  $  #     F O U ✦
   [  ]  (  )     H A E I
      :  \  %  ?     P , . '
```

**Navigation** — gate + hold `H`. Home row moves the caret one step, the row
below moves it five at a time (five key events at 30 ms each):

```
   ←  ↑  ↓  →       N R T S
←5 ↑5 ↓5 →5         Z X Q M
```

## The disabled keys

Twenty-six keys are booby-trapped. They do not just do nothing — press one and
it types `HERROPERS`, loudly, in the middle of whatever you were writing:

`` ` `` `1` `2` `3` `4` `5` `6` `7` `8` `9` `0` `-` `=` `delete` `tab` `]` `\`
`esc` `control` `←` `→` `↑` `↓` and the `Y` / `H` / `B` / `N` positions.

Every one of them has a home-row replacement:

| Reach | Do this instead |
| --- | --- |
| Number row | gate + hold `S` |
| `-` `=` `[` `]` `\` and friends | the two symbol layers |
| Arrow keys | gate + hold `H` |
| `delete` | Right Command |
| `tab` | tap Right Option |
| `esc` | Shift + `/` |
| `return` | tap Left Command |

It is a blunt instrument and it works. Delete the `@herr` entries at the bottom
of the base layer once the habit is gone — or keep them forever, nobody is
judging.

## Function row and system keys

| Key | Action |
| --- | --- |
| `F3` | `⌘⇧⌃4` — screenshot a region to the clipboard |
| `F4` | Raycast (`⌥⌃⌘⇧` + `a`) |
| `F6` | Toggle the whole keymap on and off |
| `⌥` + `A` | Raycast |
| `⌥` + `S` | Mouseless |
| `⌥` + `E` | Homerow |
| `⌥` + `T` | `esc` |
| `⌥` + `J/K/L/;` | AeroSpace window focus (`⌥` + `h/a/e/i`) |
| `⌥` + `F` | AeroSpace shrink window (`⌥` + `s` — `resize smart -50`) |
| `⌘⌃⌥⇧` + `D` | Mouseless free-click (`⌘⌃⌥⇧` + `tab`) |

`F6` switches to the `off` layer, where every key is `use-defsrc` — itself —
and `F6` switches back. Handy when someone else needs to use your laptop, or
when you need to type a password into a field that fights you.

If something goes properly wrong, `Control` + `Space` + `Escape` on the
*physical* keys is kanata's emergency exit and stops the process outright.

## Install

Two pieces: **kanata**, and the
[Karabiner VirtualHIDDevice](https://github.com/pqrs-org/Karabiner-DriverKit-VirtualHIDDevice)
driver that kanata grabs the keyboard through — which is also why kanata runs
as root on macOS.

**1. The driver.** Install Karabiner-Elements (it ships the driver and keeps
the daemon alive) or the standalone `.pkg` from the driver's release page, then
activate it and switch it on in *System Settings › General › Login Items &
Extensions › Driver Extensions*:

```sh
sudo /Applications/.Karabiner-VirtualHIDDevice-Manager.app/Contents/MacOS/Karabiner-VirtualHIDDevice-Manager forceActivate
sudo launchctl list | grep org.pqrs   # daemon should be listed
```

**2. kanata.** Driver v8 support is not in a tagged release yet, so build HEAD:

```sh
brew install --HEAD kanata
```

**3. The config.**

```sh
git clone git@github.com:noodleweapon/splitmac.git
cd splitmac
mkdir -p ~/.config/kanata
cp kanata/splitmac.kbd ~/.config/kanata/kanata.kbd
kanata --cfg ~/.config/kanata/kanata.kbd --check
sudo kanata --cfg ~/.config/kanata/kanata.kbd
```

The first run is the one that asks for permissions: add the kanata binary under
*Privacy & Security › Input Monitoring* and *› Accessibility*, then run it
again. To start it at boot instead:

```sh
sudo cp kanata/com.splitmac.kanata.plist /Library/LaunchDaemons/
sudo sed -i '' "s|/Users/YOU|$HOME|" /Library/LaunchDaemons/com.splitmac.kanata.plist
sudo chown root:wheel /Library/LaunchDaemons/com.splitmac.kanata.plist
sudo launchctl bootstrap system /Library/LaunchDaemons/com.splitmac.kanata.plist
```

It logs to `/var/log/kanata.log`. `sudo launchctl bootout system/com.splitmac.kanata`
stops it again.

> **Warning:** this replaces your entire keyboard, and the alpha layout means
> you cannot touch-type on the machine until you learn it. `F6` turns
> everything off; `Control` + `Space` + `Escape` on the physical keys kills
> kanata outright.

Run kanata **or** Karabiner-Elements, not both — they both seize the keyboard.
Keeping Karabiner-Elements installed but quit is fine, and is the easiest way
to keep the driver maintained.

The config grabs `Apple Internal Keyboard / Trackpad` and nothing else, so an
external keyboard stays exactly as it was. `kanata -l` lists the names if
yours differs.

Precedence here is the layer stack, not rule order. A layer's own entries win,
anything it does not define falls through to `base`, and the trainer lives in
`base` — so `Y`/`H`/`B`/`N` stay trapped inside every layer. The `⌥` and `⇧`
shortcuts are `defoverridesv2` entries, which match on what kanata is about to
*output*: they are written in the letters this layout types, so `(lalt y)` is
physical `J`. The two `⇧` rules list the symbol layers as excluded, because
`<` and `>` are shift+comma and shift+period and would otherwise trip them.

## Regenerating the diagrams

The layout data lives in [`tools/keymap.py`](tools/keymap.py) and everything
else is generated from it:

```sh
python3 tools/render_svg.py     # writes img/*.svg
python3 tools/build_html.py     # writes keymap.html
```

No dependencies beyond the standard library.

## Testing the keymap

`--check` only proves the config parses. For behaviour there is
[`tools/sim_tests.rs`](tools/sim_tests.rs), which drives kanata's own
simulation harness — the alphas, the gate, all four layers, the magic key and
every override, with no keyboard involved:

```sh
sh tools/sim_test.sh
```

It clones kanata, drops the test in and runs it, so it needs `cargo`.

## Sponsor

<a href="https://www.pcbway.com/">
  <img alt="PCBWay" src="img/pcbway.png" width="320">
</a>

[PCBWay](https://www.pcbway.com/) sponsors this project. They are a one-stop
shop for turning a hardware idea into a physical thing: PCB prototyping and
small-batch fabrication, PCB assembly, CNC machining, sheet metal, injection
moulding and 3D printing (resin, nylon, and metal), all ordered from one
account with an instant online quote.

Why they are a good fit for a keyboard project:

- **Cheap, fast prototypes.** A handful of 2-layer boards costs a few dollars
  and ships in days, so a keymap idea can become a real split board without a
  big commitment.
- **One order, every part.** Plates, cases and the PCB itself can all come from
  the same order — CNC-cut aluminium or 3D-printed cases alongside the boards.
- **Assembly included.** Hand-soldering a hundred hot-swap sockets is optional;
  PCBWay can populate the boards for you.
- **Real humans in support.** Every order is checked by an engineer before it
  goes to fabrication, and the DFM feedback comes back quickly.

If you use them, say hello from `splitmac`.

## Credits

- [PCBWay](https://www.pcbway.com/) for sponsoring the project
- [kanata](https://github.com/jtroo/kanata) by jtroo — the engine
- [Karabiner-DriverKit-VirtualHIDDevice](https://github.com/pqrs-org/Karabiner-DriverKit-VirtualHIDDevice)
  by Takayama Fumihiko — the virtual keyboard kanata writes through
- [@getreuer's QMK keymap](https://github.com/getreuer/qmk-keymap) for the
  documentation format
- [Gallium](https://github.com/GalileoBlues/Gallium) by GalileoBlues — the
  alpha layout. This config uses v2, the row-staggered version

## License

MIT
