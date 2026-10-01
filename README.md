# splitmac

Split-keyboard ergonomics on a stock MacBook, in one Karabiner-Elements config.
The right hand moves a column over, the home row becomes modifiers and four hold
layers, and 30 keys you should stop reaching for are switched off.

The same keymap ships in two forms, and they are kept identical:

| | Where it runs | What it is |
| --- | --- | --- |
| [`karabiner/`](karabiner) | the MacBook's built-in keyboard | one `karabiner.json`, no firmware |
| [`qmk/`](qmk) | a [ZSA Voyager](https://www.zsa.io/voyager) | QMK firmware, so the layout travels with the board |

Learn it once on the laptop, plug in the split, same fingers do the same things.

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

Each layer is drawn twice: the MacBook deck first, then the Voyager. The small
grey legend in the corner of each cap is what is printed on the laptop key it
stands for; the big legend is what the key actually does.

---

### Base

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="img/base-dark.svg?v=4">
  <img alt="Base layer" src="img/base-light.svg?v=4">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="img/voyager-base-dark.svg?v=1">
  <img alt="Voyager base layer" src="img/voyager-base-light.svg?v=1">
</picture>

### Hold gate and home-row mods

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="img/mods-dark.svg?v=4">
  <img alt="Hold gate and home-row mods" src="img/mods-light.svg?v=4">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="img/voyager-mods-dark.svg?v=1">
  <img alt="Voyager hold gate and home-row mods" src="img/voyager-mods-light.svg?v=1">
</picture>

### Number layer

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="img/number-dark.svg?v=4">
  <img alt="Number layer" src="img/number-light.svg?v=4">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="img/voyager-number-dark.svg?v=1">
  <img alt="Voyager number layer" src="img/voyager-number-light.svg?v=1">
</picture>

### Symbol layer — left

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="img/sym-left-dark.svg?v=4">
  <img alt="Left symbol layer" src="img/sym-left-light.svg?v=4">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="img/voyager-sym-left-dark.svg?v=1">
  <img alt="Voyager left symbol layer" src="img/voyager-sym-left-light.svg?v=1">
</picture>

### Symbol layer — right

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="img/sym-right-dark.svg?v=4">
  <img alt="Right symbol layer" src="img/sym-right-light.svg?v=4">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="img/voyager-sym-right-dark.svg?v=1">
  <img alt="Voyager right symbol layer" src="img/voyager-sym-right-light.svg?v=1">
</picture>

### Navigation layer

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="img/nav-dark.svg?v=5">
  <img alt="Navigation layer" src="img/nav-light.svg?v=5">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="img/voyager-nav-dark.svg?v=1">
  <img alt="Voyager navigation layer" src="img/voyager-nav-light.svg?v=1">
</picture>

### Plain QWERTY (Voyager only)

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="img/voyager-plain-dark.svg?v=1">
  <img alt="Voyager plain QWERTY layer" src="img/voyager-plain-light.svg?v=1">
</picture>

There is also an [interactive version](keymap.html) of the laptop diagrams —
open it and press keys on your own keyboard to light up the matching cap, or
hold Space and a layer key to preview a layer live.

Inspired by [@getreuer's QMK keymap](https://github.com/getreuer/qmk-keymap),
which is the reference for what a well-documented personal keymap looks like.

---

## The idea

A laptop keyboard has no thumb cluster and no layer keys, so the usual QMK
tricks do not port over directly. This config works around that with three
moves:

1. **Everything worth reaching for moves onto the home row.** Numbers, symbols
   and arrows live on hold layers, not on the number row.
2. **Space and Right Command become gates.** Hold either one and that hand's
   home row turns into modifiers and layer keys. Let go and it is plain letters
   again — so there are no accidental mod-taps while typing at speed.
3. **The keys you should stop using are disabled.** The number row, `esc`,
   `tab`, `delete`, `caps lock`, `return`, Left Control, Left Option, the arrow
   cluster and the four alpha keys between the hands do not do their job any
   more.

The Voyager has real thumb keys, so it does not need any of the workarounds —
but it runs them anyway, so both boards feel identical.

## Base layer

The alphas are [Gallium v2](https://github.com/GalileoBlues/Gallium), the
row-staggered variant of Gallium — which is the right choice here, because a
laptop keyboard is a row-staggered keyboard. Gallium v2 exists precisely for
boards like this one, rather than the column-staggered splits most alt layouts
are tuned for.

As a 3×10 grid, one column per finger (this is also exactly how it sits on the
Voyager):

```
 B  L  D  C  V      J  F  O  U  .
 N  R  T  S  G      Y  H  A  E  I
 Z  X  Q  M  W      K  P  ,  _  '
```

On the laptop, those thirty letters land on these physical keys:

```
 Q  W  E  R  T      U  I  O  P  [
 A  S  D  F  G      J  K  L  ;  '
 ⇧  Z  X  C  V      M  ,  .  /  ⇧
```

Two things move to make the grid fit a MacBook:

* **The right hand sits one column to the right** of QWERTY home, so its index
  finger rests on `J` instead of `H`.
* **The left bottom row sits one column to the left**, so the `Z` column lands
  on Left Shift and the `'` column on Right Shift.

That leaves physical `Y`, `H`, `B` and `N` in the gap between the hands with
nothing to do, so they are disabled.

The rest of the base layer:

| Physical key | Types |
| --- | --- |
| Left Shift | `Z` |
| Right Shift | `'` |
| `/` | `_` |
| Left Command | `space` |
| Space | left gate: hold to arm the left hand's special keys, tap does nothing |
| Right Command | right gate: hold to arm the right hand's special keys, tap does nothing |
| Right Option | `delete` |
| Caps Lock / Return / Left Control / Left Option | disabled (types `HERROPERS`) |
| Shift + `[` (the `.` key) | `esc` |
| Shift + `.` (the `,` key) | `⌥C` |
| ⌘ + `C` (the `M` key) | nothing |
| ⌥ + `C` (the `M` key) | `⌃C` |

## Hold gate and home-row mods

There are two gates, one per side. Hold **Space** (left gate, `left_gate`) to arm
the left hand's special keys, or **Right Command** (right gate, `right_gate`) to
arm the right hand's. On the Voyager the gates are the two inner thumb keys.
Each gate only arms its own side: while the left gate is held, the right hand's
special keys are plain letters, and the other way round. Tapping a gate does
nothing.

```
 ·  ·  ·  ·  ·      ·  ·  ·  ·  ·
 ⇧  ⌥  ⌘  №  ⌃      ⌃  →  ⌘  ⌥  ⇧
 ·  ·  ·  &  ·      ·  #  ·  ·  ·
   left gate          right gate
```

| Key | Physical | Gate | Hold | Tap |
| --- | --- | --- | --- | --- |
| `N` | `A` | left | Left Shift | nothing |
| `R` | `S` | left | Left Option | `r` |
| `T` | `D` | left | Left Command | `t` |
| `S` | `F` | left | Number layer | `s` |
| `G` | `G` | left | Left Control | `g` |
| `M` | `C` | left | Symbol layer, right | `m` |
| `Y` | `J` | right | Left Control | `y` |
| `H` | `K` | right | Navigation layer | `h` |
| `A` | `L` | right | Left Command | `a` |
| `E` | `;` | right | Left Option | `e` |
| `I` | `'` | right | Right Shift | nothing |
| `P` | `,` | right | Symbol layer, left | `p` |

Command, Option and Control are always the **left-hand** modifier, whichever
side of the board you hold them on.

The gate is the whole trick. Home-row mods normally misfire during fast typing;
here they simply do not exist until you ask for them, and only one layer can be
active at a time — each layer key is conditioned on the other three being off.

**Every hold latches on key-down, so order never matters.** All twelve of them —
four layers and eight modifiers — fire from `to` the instant the key goes down.
The modifiers are held for as long as the key is; the layer keys set a variable
that `to_after_key_up` clears on release. `to_if_alone` types the letter if you
tap the key and press nothing else (the two Shifts have no tap). Hold the layer
first or the modifier first; the result is identical.

This is worth stating because the obvious way to write a layer key — a
`to_if_held_down` timer, optionally with a `to_delayed_action` — does not
compose. Both are cancelable by later key events, so whichever hold you started
first wins and the second one silently does nothing. Nothing here uses a timer.

One thing the gate cannot make order-free: it has to be held *first*. Conditions
are evaluated when a key goes down, so a layer or modifier key pressed before
its gate sees the gate variable as 0 and just types its letter.

Every layer is held with one hand and typed with the other, so the holding
hand's modifiers stay live while the layer is up:

| Layer (held with) | Modifiers still reachable |
| --- | --- |
| Number — left gate + `S` | `N` ⇧, `R` ⌥, `T` ⌘, `G` ⌃ |
| Symbol right — left gate + `M` | `N` ⇧, `R` ⌥, `T` ⌘, `G` ⌃ |
| Symbol left — right gate + `P` | `Y` ⌃, `A` ⌘, `E` ⌥, `I` ⇧ |
| Navigation — right gate + `H` | `Y` ⌃, `A` ⌘, `E` ⌥, `I` ⇧ |

The other hand's modifiers are typing layer glyphs and cannot also be
modifiers. So ⇧ + arrow is right gate + `H` + `I`, then the arrow, and ⌘ + digit
is left gate + `S` + `T`, then the digit.

## The layers

The grids use the same 3×10 layout as the base layer. `·` keeps its base-layer
meaning and `[X]` is the key you hold.

**Number** — left gate + hold `S`. Digits sit under the right hand, with `~` on
the `'` key (Right Shift on the laptop):

```
 ·  ·  ·  ·  ·      ·  7  8  9  ·
 ·  ·  · [S] ·      ·  0  1  2  3
 ·  ·  ·  ·  ·      ·  4  5  6  ~
```

**Symbol, left** — right gate + hold `P`. Held by the right hand, typed with the
left:

```
 ^  *  -  |  ·      ·  ·  ·  ·  ·
 +  !  /  =  ·      ·  ·  ·  ·  ·
 `  <  >  @  ·      · [P] ·  ·  ·
```

**Symbol, right** — left gate + hold `M`. Held by the left hand, typed with the
right:

```
 ·  ·  ·  ·  ·      ·  ;  &  $  #
 ·  ·  ·  ·  ·      ·  [  ]  (  )
 ·  ·  · [M] ·      ·  :  \  %  ?
```

**Navigation** — right gate + hold `H`. The top row moves the caret one step, the
home row is `left click` `tab` `esc` `return`, and the bottom row moves the
caret five at a time (five key events, 30 ms apart on the laptop, 15 ms on the
Voyager):

```
  ←     ↑     ↓     →     ·        ·  ·  ·  ·  ·
click  tab   esc    ⏎     ·        · [H] ·  ·  ·
  ←5    ↑5    ↓5    →5    ·        ·  ·  ·  ·  ·
```

The click is a real mouse button, so pointing with the trackpad and clicking
from the home row works.

## The disabled keys

Thirty keys are booby-trapped. They do not just do nothing — press one and
it types `HERROPERS`, loudly, in the middle of whatever you were writing:

`` ` `` `1` `2` `3` `4` `5` `6` `7` `8` `9` `0` `-` `=` `delete` `tab` `]` `\`
`esc` `control` `option` `caps lock` `return` `←` `→` `↑` `↓` and the `Y` / `H` / `B` / `N` positions.

On the Voyager the same trap covers the number row and the outer column on
each side.

Every one of them has a home-row replacement:

| Reach | Do this instead |
| --- | --- |
| Number row | left gate + hold `S` |
| `-` `=` `[` `]` `\` and friends | the two symbol layers |
| Arrow keys | right gate + hold `H` |
| `delete` | Right Option (outer right thumb on the Voyager) |
| `tab` | right gate + hold `H`, then `R` |
| `esc` | Shift + `.`, or right gate + hold `H`, then `T` |
| `return` | right gate + hold `H`, then `S` |
| `control` | left gate + hold `G`, or right gate + hold `Y` |
| `option` | left gate + hold `R`, or right gate + hold `E` |

It is a blunt instrument and it works. Delete the rule named
`Bad-habit trainer` once the habit is gone — or keep it forever, nobody is
judging.

## Function row and system keys

| Key | Action |
| --- | --- |
| `F3` | `⌘⇧⌃4` — screenshot a region to the clipboard |
| `F4` | Raycast (`⌥⌃⌘⇧` + `a`) |
| `F6` | Toggle the whole keymap on and off |
| `⌥` + `H/A/E/I` (physical `K/L/;/'`) | AeroSpace window focus (`⌥` + `h/a/e/i`) |
| `⌥` + `S` (physical `F`) | AeroSpace shrink window (`⌥` + `s` — `resize smart -50`) |
| `⌥` + physical `A` | Raycast |
| `⌥` + physical `S` | Mouseless |
| `⌥` + physical `E` | Homerow |
| `⌥` + physical `T` | `esc` |
| `⌘⌃⌥⇧` + physical `D` | Mouseless free-click (`⌘⌃⌥⇧` + `tab`) |

There is no Option key of its own any more, so `⌥` here means a gated home-row
Option (`R` or `E`).

The AeroSpace rule sits above the alpha remap and works. The last five rows are
in the config but sit below the alpha-remap rule, which already claims those
keys with any modifier held, so in practice they do not fire. Move them above
the remap rule if you want them.

`F6` runs [`toggle_profile.sh`](karabiner/toggle_profile.sh), which flips
Karabiner between the `Default profile` and a `Disabled` profile that contains
nothing but the toggle itself. Handy when someone else needs to use your laptop,
or when you need to type a password into a field that fights you.

## The Voyager version

The ZSA Voyager has the thumb cluster and the column stagger the laptop was
pretending to have, so the firmware is the same keymap with the pretending
removed:

* **The two offsets go away.** On the laptop the right hand sits one column
  right of QWERTY home and the left bottom row one column left of it. On the
  Voyager every hand sits in its own columns; the small grey legend on each cap
  shows which laptop key it stands for.
* **The thumbs are what the laptop's thumb keys did.** Left thumb: outer is
  `space` (physical Left Command), inner is the **left gate** (physical Space).
  Right thumb: inner is the **right gate** (physical Right Command), outer is
  `delete` (physical Right Option).
* **Everything else is the same.** Same alphas, same gated home-row mods, same
  four layers, same disabled keys (the number row and the outer columns type
  `HERROPERS`), same Shift + `.` → `esc` and Shift + `,` → `⌥C`.
* **F6 becomes a chord.** Press both top-corner keys together to toggle a plain
  QWERTY layer; the board lights dim white while it is on. F3 and F4 stay on the
  laptop's function row.

How the Karabiner rules were translated — gates, `to_if_alone` timing, rule
precedence, and which rules were left out — is written up in
[`qmk/keyboards/zsa/voyager/keymaps/splitmac/README.md`](qmk/keyboards/zsa/voyager/keymaps/splitmac/README.md).

The Voyager diagrams are [at the top](#base), under each laptop diagram.

## Repository layout

```
karabiner/   karabiner.json and the F6 profile-toggle script  (laptop version)
qmk/         QMK external userspace with keyboards/zsa/voyager/keymaps/splitmac  (Voyager version)
tools/       keymap.py + voyager.py hold the layout data; the render_*.py and
             build_html.py scripts generate everything in img/ and keymap.html
img/         generated layer diagrams, light and dark
keymap.html  generated interactive page for the laptop version
```

## Install

### Laptop (Karabiner)

Requires [Karabiner-Elements](https://karabiner-elements.pqrs.org/).

```sh
git clone git@github.com:noodleweapon/splitmac.git
cd splitmac

mkdir -p ~/.config/karabiner

# back up whatever you have now
cp ~/.config/karabiner/karabiner.json ~/.config/karabiner/karabiner.json.bak

cp karabiner/karabiner.json      ~/.config/karabiner/karabiner.json
cp karabiner/toggle_profile.sh   ~/.config/karabiner/toggle_profile.sh
chmod +x ~/.config/karabiner/toggle_profile.sh
```

Karabiner picks the file up as soon as it is written. One path in the config
points at this machine — the `F6` toggle script — so edit or drop that rule if
you do not want it.

> **Warning:** this replaces your entire Karabiner config, and the alpha layout
> means you cannot touch-type on the machine until you learn it. Keep the backup
> and remember that `F6` turns everything off.

Rule order in `karabiner.json` matters. Karabiner applies the first manipulator
that matches a key and stops there, so the disabled-key rule sits at the top and
wins on `Y`/`H`/`B`/`N`, and the alpha remap sits above the `⌥`-shortcut rules.

The shipped config also lists the ZSA Voyager under `devices` with
`"ignore": true`, so plugging in the split does not get it remapped twice.

### Voyager (QMK)

Requires a [QMK setup](https://docs.qmk.fm/newbs) with the `zsa/voyager`
keyboard (upstream QMK ≥ 0.30) and `dfu-util` for flashing.

```sh
qmk config user.overlay_dir="$(realpath qmk)"   # once, from the repo root
cd qmk
qmk compile -kb zsa/voyager -km splitmac         # writes zsa_voyager_splitmac.bin
qmk flash   -kb zsa/voyager -km splitmac         # press the Voyager's reset button when asked
```

The `.bin` can also be flashed from ZSA's Keymapp. If you run Karabiner with a
config other than the one in this repo, untick "Modify events" for the Voyager
in Karabiner-Elements → Devices first.

## Regenerating the diagrams

The layout data lives in [`tools/keymap.py`](tools/keymap.py) (laptop) and
[`tools/voyager.py`](tools/voyager.py) (Voyager) and everything else is
generated from it:

```sh
python3 tools/render_svg.py       # writes img/*.svg          (laptop layers)
python3 tools/render_voyager.py   # writes img/voyager-*.svg  (Voyager layers)
python3 tools/build_html.py       # writes keymap.html
```

The firmware in `qmk/` is hand-written C, so a layout change is made twice:
once in `keymap.c`, once in `voyager.py` for the diagram.

No dependencies beyond the standard library.

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
- [Karabiner-Elements](https://karabiner-elements.pqrs.org/) by Takayama Fumihiko
- [QMK](https://qmk.fm/) and [ZSA](https://www.zsa.io/) for the firmware and
  the Voyager
- [@getreuer's QMK keymap](https://github.com/getreuer/qmk-keymap) for the
  documentation format and the split-layout macro idea
- [Gallium](https://github.com/GalileoBlues/Gallium) by GalileoBlues — the
  alpha layout. This config uses v2, the row-staggered version

## License

MIT
