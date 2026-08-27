<a href="https://www.pcbway.com/">
  <img alt="Sponsored by PCBWay" src="img/pcbway.png" width="240">
</a>

This project is sponsored by [PCBWay](https://www.pcbway.com/), a one-stop shop
for PCB prototyping, assembly, CNC machining and 3D printing. If you want to
turn a keymap like this one into a real split board, they are a good place to
have it made — see [Sponsor](#sponsor) below for what they offer.

---

# splitmac

Split-keyboard ergonomics on a stock MacBook, in one Karabiner-Elements config.
The right hand moves a column over, the home row becomes modifiers and four hold
layers, and 26 keys you should stop reaching for are switched off.

No firmware. No external keyboard. One `karabiner.json`.

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
      B  L  D  C  V        J  F  O  U  -
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
| Right Option | tap `tab`, hold `shift` |
| Right Command | `delete` |
| Left Option | `control` |
| Caps Lock / Return | hold to arm the layers, tap does nothing |
| Shift + `/` | `esc` |
| Shift + `.` | `⌥C` |

## Hold gate and home-row mods

Hold **Caps Lock** or **Return** to arm the gate (`hold_mods_enabled`). While it
is held, four home-row keys become modifiers and four become layer keys:

| Home-row key | Physical | Hold |
| --- | --- | --- |
| `T` | `D` | Left Command |
| `A` | `L` | Right Command |
| `R` | `S` | Left Option |
| `E` | `;` | Right Option |
| `S` | `F` | Number layer |
| `H` | `K` | Navigation layer |
| `M` | `C` | Symbol layer, right |
| `P` | `,` | Symbol layer, left |

The gate is the whole trick. Home-row mods normally misfire during fast typing;
here they simply do not exist until you ask for them, and only one layer can be
active at a time — each layer key is conditioned on the other three being off.

**Every hold latches on key-down, so order never matters.** All eight of them —
four layers, two Commands, two Options — are written the same way: `to` sets the
modifier or the layer variable the instant the key goes down, `to_if_alone`
emits the letter if you tap it and press nothing else, `to_after_key_up` clears
it on release. Hold the layer first or the modifier first; the result is
identical.

This is worth stating because the obvious way to write a layer key — a
`to_if_held_down` timer, optionally with a `to_delayed_action` — does not
compose. Both are cancelable by later key events, so whichever hold you started
first wins and the second one silently does nothing. Nothing here uses a timer.

One thing the gate cannot make order-free: it has to be held *first*. Conditions
are evaluated when a key goes down, so a layer or modifier key pressed before
Caps Lock sees `hold_mods_enabled` as 0 and just types its letter.

Each layer also borrows some home-row keys for its own glyphs, which shadows the
modifier on those keys. One pair always survives:

| Layer (held with) | Modifiers still reachable |
| --- | --- |
| Number — physical `F` | Left Command `D`, Left Option `S` |
| Symbol right — physical `C` | Left Command `D`, Left Option `S` |
| Symbol left — physical `,` | Right Command `L`, Right Option `;` |
| Navigation — physical `K` | Right Command `L`, Right Option `;` |

In every case the surviving pair is on the same hand that holds the layer, which
takes some getting used to. The other hand's Command and Option are typing layer
glyphs and cannot also be modifiers.

## The layers

**Number** — gate + hold `S`. Digits sit under the right hand:

```
   7  8  9        F O U
   0  1  2  3     H A E I
      4  5  6     K P , .
```

**Symbol, left** — gate + hold `P`. Held by the right hand, typed with the left:

```
   ^  <  >  |     B L D C
   +  !  /  =     N R T S
`  ~  *  @        Z X Q M
```

**Symbol, right** — gate + hold `M`. Held by the left hand, typed with the right:

```
   ;  &  $  #     F O U -
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

It is a blunt instrument and it works. Delete the rule named
`Bad-habit trainer` once the habit is gone — or keep it forever, nobody is
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

`F6` runs [`toggle_profile.sh`](karabiner/toggle_profile.sh), which flips
Karabiner between the `Default profile` and a `Disabled` profile that contains
nothing but the toggle itself. Handy when someone else needs to use your laptop,
or when you need to type a password into a field that fights you.

## Install

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

Rule order in `karabiner.json` matters. Karabiner chains manipulators, so each
rule sees the output of the ones above it — the disabled-key rule runs first so
it wins on `Y`/`H`/`B`/`N`, and `Left Option => Left Control` runs last so the
`⌥`+letter shortcuts above it still match.

## Regenerating the diagrams

The layout data lives in [`tools/keymap.py`](tools/keymap.py) and everything
else is generated from it:

```sh
python3 tools/render_svg.py     # writes img/*.svg
python3 tools/build_html.py     # writes keymap.html
```

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
- [@getreuer's QMK keymap](https://github.com/getreuer/qmk-keymap) for the
  documentation format
- [Gallium](https://github.com/GalileoBlues/Gallium) by GalileoBlues — the
  alpha layout. This config uses v2, the row-staggered version

## License

MIT
