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
  <source media="(prefers-color-scheme: dark)" srcset="img/base-dark.svg?v=6">
  <img alt="Base layer" src="img/base-light.svg?v=6">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="img/voyager-base-dark.svg?v=2">
  <img alt="Voyager base layer" src="img/voyager-base-light.svg?v=2">
</picture>

### Number layer

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="img/number-dark.svg?v=6">
  <img alt="Number layer" src="img/number-light.svg?v=6">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="img/voyager-number-dark.svg?v=2">
  <img alt="Voyager number layer" src="img/voyager-number-light.svg?v=2">
</picture>

### Symbol layer — left

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="img/sym-left-dark.svg?v=6">
  <img alt="Left symbol layer" src="img/sym-left-light.svg?v=6">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="img/voyager-sym-left-dark.svg?v=2">
  <img alt="Voyager left symbol layer" src="img/voyager-sym-left-light.svg?v=2">
</picture>

### Symbol layer — right

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="img/sym-right-dark.svg?v=6">
  <img alt="Right symbol layer" src="img/sym-right-light.svg?v=6">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="img/voyager-sym-right-dark.svg?v=2">
  <img alt="Voyager right symbol layer" src="img/voyager-sym-right-light.svg?v=2">
</picture>

### Navigation layer

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="img/nav-dark.svg?v=6">
  <img alt="Navigation layer" src="img/nav-light.svg?v=6">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="img/voyager-nav-dark.svg?v=2">
  <img alt="Voyager navigation layer" src="img/voyager-nav-light.svg?v=2">
</picture>

### Plain QWERTY (Voyager only)

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="img/voyager-plain-dark.svg?v=2">
  <img alt="Voyager plain QWERTY layer" src="img/voyager-plain-light.svg?v=2">
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
