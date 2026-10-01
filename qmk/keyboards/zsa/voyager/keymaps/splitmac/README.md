# splitmac for the ZSA Voyager

The firmware version of splitmac. Same alphas, same gates, same four hold
layers as the Karabiner profile in [`karabiner/`](../../../../../../karabiner),
reproduced in QMK with Karabiner's first-matching-rule precedence.

The layer diagrams are in the [top-level README](../../../../../../README.md#the-voyager-version).

## Build and flash

Needs a [QMK setup](https://docs.qmk.fm/newbs) whose `qmk_firmware` has the
`zsa/voyager` keyboard (upstream QMK ≥ 0.30). The `qmk/` directory is an
[External Userspace](https://docs.qmk.fm/newbs_external_userspace): point QMK at
it once, then build.

```sh
qmk config user.overlay_dir="$(realpath qmk)"   # from the splitmac repo root
cd qmk
qmk compile -kb zsa/voyager -km splitmac         # writes zsa_voyager_splitmac.bin
qmk flash   -kb zsa/voyager -km splitmac         # press the Voyager's reset button when asked
```

`qmk flash` uses `dfu-util` (`brew install dfu-util`). The `.bin` can also be
flashed with ZSA's Keymapp.

**Turn Karabiner off for the Voyager.** If Karabiner keeps modifying the
Voyager, every key is remapped twice (`b` becomes `HERROPERS`, Space becomes a
gate that types nothing, and so on). The shipped `karabiner.json` already lists
the Voyager (vendor `12951`, product `6519`) under `devices` with
`"ignore": true` in both profiles; if you use your own config, untick
"Modify events" for the Voyager in Karabiner-Elements → Devices.

## Files

| File | What it is |
| --- | --- |
| `keymap.c` | Layers, gates, gated mod/layer keys, shift overrides, the trainer macro |
| `config.h` | `ALONE_TIMEOUT_MS` (Karabiner's 200 ms `to_if_alone`), macro delays |
| `rules.mk` | LTO on, unused QMK features off |

## How the Karabiner rules became firmware

* **Gates.** `LGATE` / `RGATE` set a flag while held and do nothing on tap, like
  the `set_variable` manipulators on Space and Right Command.
* **Gated keys.** One table (`gated_keys[]`) lists every home-row key with its
  letter, its gate, and the modifier or layer it holds. On press, if the gate is
  down (and, for layer keys, no other layer is active), the modifier is
  registered or the layer turned on *immediately*, matching Karabiner's `to`.
  On release the modifier or layer is dropped, and the letter is tapped only if
  no other key was pressed in between and less than 200 ms passed
  (`to_if_alone`). Without the gate the key is a plain letter with normal key
  repeat.
* **Rule precedence.** Karabiner's "⌘ + m-key does nothing" and
  "⌥ + m-key sends ⌃C" rules come before the layer rule, so `GL_C` checks the
  modifier state first. Shift + `.`-key → Escape and Shift + `,`-key → ⌥C are
  handled the same way Karabiner handles a mandatory modifier: Shift is removed
  from the report, the replacement is tapped, Shift is restored.
* **Trainer.** `TRAIN` keys send `HERROPERS` on press.
* **Nav layer ×5 keys.** Five `tap_code_delay` calls, 15 ms apart.
* **Position offsets.** Karabiner rules name laptop keys, where the right hand
  sits one column right of QWERTY home and the left bottom row one column left.
  The Voyager keymap undoes both, so every finger lands where it would on the
  laptop. The ghost legend on the Voyager diagrams shows the laptop key each cap
  stands for.

## Not carried over

* **F3** (region screenshot), **F4** (Raycast) — the Voyager has no function
  row; they stay on the laptop's own keys.
* **F6** (toggle the keymap off) — there is no plain-QWERTY layer on the
  Voyager.
* **⌥ + T / A / S / E shortcuts, MOUSELESS FREE** — these Karabiner rules sit
  below the "Keyboard layout remap" rule, which already matches those keys with
  any modifier, so they are not reachable on the laptop either. If you want
  them on the Voyager, add cases to `process_record_user`.
* **AeroSpace `⌥ + K/L/;/'` → `⌥ + h/a/e/i`** — a no-op in firmware, because
  those caps already type h/a/e/i.
