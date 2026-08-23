#!/usr/bin/env python3
"""Build the interactive keymap page from the layout data in keymap.py.

    python3 tools/build_html.py     # writes keymap.html
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from keymap import ROWS, ROW_WIDTH, LAYERS  # noqa: E402

# Karabiner key_code -> DOM KeyboardEvent.code, so the page can light up the
# cap you are physically pressing.
CODES = {
    "escape": "Escape", "f1": "F1", "f2": "F2", "f3": "F3", "f4": "F4",
    "f5": "F5", "f6": "F6", "f7": "F7", "f8": "F8", "f9": "F9",
    "f10": "F10", "f11": "F11", "f12": "F12",
    "grave_accent_and_tilde": "Backquote",
    "1": "Digit1", "2": "Digit2", "3": "Digit3", "4": "Digit4", "5": "Digit5",
    "6": "Digit6", "7": "Digit7", "8": "Digit8", "9": "Digit9", "0": "Digit0",
    "hyphen": "Minus", "equal_sign": "Equal",
    "delete_or_backspace": "Backspace", "tab": "Tab",
    "open_bracket": "BracketLeft", "close_bracket": "BracketRight",
    "backslash": "Backslash", "caps_lock": "CapsLock",
    "semicolon": "Semicolon", "quote": "Quote",
    "return_or_enter": "Enter", "left_shift": "ShiftLeft",
    "comma": "Comma", "period": "Period", "slash": "Slash",
    "right_shift": "ShiftRight", "fn": "Fn",
    "left_control": "ControlLeft", "left_option": "AltLeft",
    "left_command": "MetaLeft", "spacebar": "Space",
    "right_command": "MetaRight", "right_option": "AltRight",
    "left_arrow": "ArrowLeft", "right_arrow": "ArrowRight",
    "up_arrow": "ArrowUp", "down_arrow": "ArrowDown",
}
for _c in "abcdefghijklmnopqrstuvwxyz":
    CODES[_c] = "Key" + _c.upper()

# Which physical key holds each layer, for the live "hold to preview" mode.
LAYER_HOLD = {"number": "f", "sym-left": "comma", "sym-right": "c", "nav": "k"}

DATA = {
    "rows": [[{"id": k, "cap": lab, "w": w, "code": CODES.get(k, "")}
              for k, lab, w in row] for row in ROWS],
    "rowWidth": ROW_WIDTH,
    "layers": [{"id": l["id"], "name": l["name"], "sub": l["sub"], "full": l["full"],
                "hold": LAYER_HOLD.get(l["id"], ""),
                "keys": {k: {"main": v[0], "sub": v[1], "cls": v[2]}
                         for k, v in l["keys"].items()}}
               for l in LAYERS],
}

TEMPLATE = r"""<title>splitmac</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Chivo:wght@700;900&family=JetBrains+Mono:wght@400;500;700&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap">
<style>
:root {
  --bg: #e9e9e7;
  --bg-raise: #f6f6f5;
  --fg: #16171b;
  --fg-dim: #5c5d67;
  --fg-faint: #8b8c96;
  --rule: #cfcfcc;
  --rule-soft: #dedeDB;

  /* the deck stays dark in both themes — it is a MacBook, after all */
  --chassis: #cdcdca;
  --chassis-edge: #b6b6b2;
  --deck: #17181c;
  --cap: #232429;
  --cap-edge: #34353d;
  --cap-lip: #101116;
  --ghost: #6b6c78;
  --sub: #9a9ba6;

  --c-alpha-bg: #232429;   --c-alpha-fg: #f3f3f6;
  --c-punct-bg: #16304c;   --c-punct-fg: #8ecbff;
  --c-trainer-bg: #000000; --c-trainer-fg: #63636b;
  --c-gate-bg: #17392f;    --c-gate-fg: #8ff0cd;
  --c-layer-bg: #372450;   --c-layer-fg: #d3aaff;
  --c-mod-bg: #48320f;     --c-mod-fg: #ffcf7a;
  --c-system-bg: #10383a;  --c-system-fg: #7fe6e0;
  --c-dead-bg: #1b1c20;    --c-dead-fg: #55565f;

  --shadow: 0 24px 60px -28px rgba(10, 12, 20, .45);
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg: #0a0b0d;
    --bg-raise: #121317;
    --fg: #eef0f4;
    --fg-dim: #9b9da8;
    --fg-faint: #6e707b;
    --rule: #24262c;
    --rule-soft: #1a1c21;
    --chassis: #1c1d22;
    --chassis-edge: #2b2d34;
    --deck: #0f1013;
    --shadow: 0 24px 70px -30px rgba(0, 0, 0, .9);
  }
}
:root[data-theme="dark"] {
  --bg: #0a0b0d;
  --bg-raise: #121317;
  --fg: #eef0f4;
  --fg-dim: #9b9da8;
  --fg-faint: #6e707b;
  --rule: #24262c;
  --rule-soft: #1a1c21;
  --chassis: #1c1d22;
  --chassis-edge: #2b2d34;
  --deck: #0f1013;
  --shadow: 0 24px 70px -30px rgba(0, 0, 0, .9);
}

* { box-sizing: border-box; }

body {
  margin: 0;
  background: var(--bg);
  color: var(--fg);
  font-family: "Source Serif 4", Georgia, serif;
  font-size: 17px;
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
}

.wrap {
  max-width: 1180px;
  margin: 0 auto;
  padding: 0 28px 96px;
  display: flex;
  flex-direction: column;
  gap: 42px;
}

/* ---------- masthead ---------- */

header { padding-top: 64px; display: flex; flex-direction: column; gap: 18px; }

.eyebrow {
  font-family: "JetBrains Mono", ui-monospace, monospace;
  font-size: 11px;
  letter-spacing: .18em;
  text-transform: uppercase;
  color: var(--fg-faint);
}

h1 {
  font-family: Chivo, "Helvetica Neue", Arial, sans-serif;
  font-weight: 900;
  font-size: clamp(42px, 8vw, 88px);
  line-height: .92;
  letter-spacing: -.035em;
  margin: 0;
  text-wrap: balance;
}

.standfirst {
  max-width: 60ch;
  font-size: 20px;
  color: var(--fg-dim);
  margin: 0;
}

.meta {
  display: flex;
  flex-wrap: wrap;
  gap: 10px 26px;
  font-family: "JetBrains Mono", ui-monospace, monospace;
  font-size: 12px;
  color: var(--fg-faint);
  border-top: 1px solid var(--rule);
  padding-top: 16px;
}
.meta a { color: var(--fg-dim); text-decoration-color: var(--rule); }
.meta a:hover { color: var(--fg); }

/* ---------- layer switcher ---------- */

.switch {
  position: sticky;
  top: 0;
  z-index: 20;
  background: color-mix(in srgb, var(--bg) 88%, transparent);
  backdrop-filter: blur(14px);
  border-bottom: 1px solid var(--rule);
  margin: 0 -28px;
  padding: 10px 28px;
  display: flex;
  gap: 6px;
  overflow-x: auto;
  scrollbar-width: none;
}
.switch::-webkit-scrollbar { display: none; }

.tab {
  flex: 0 0 auto;
  appearance: none;
  border: 1px solid transparent;
  background: none;
  color: var(--fg-dim);
  font-family: "JetBrains Mono", ui-monospace, monospace;
  font-size: 12px;
  letter-spacing: .04em;
  padding: 7px 13px;
  border-radius: 7px;
  cursor: pointer;
  white-space: nowrap;
  transition: background .12s, color .12s, border-color .12s;
}
.tab:hover { color: var(--fg); background: var(--rule-soft); }
.tab[aria-selected="true"] {
  color: var(--fg);
  border-color: var(--rule);
  background: var(--bg-raise);
}
.tab:focus-visible { outline: 2px solid var(--c-layer-fg); outline-offset: 2px; }

/* ---------- the keyboard ---------- */

.stage { display: flex; flex-direction: column; gap: 20px; }

.stage-head { display: flex; flex-direction: column; gap: 4px; }
.stage-head h2 {
  font-family: Chivo, sans-serif;
  font-weight: 900;
  font-size: 30px;
  letter-spacing: -.02em;
  margin: 0;
}
.stage-head p { margin: 0; color: var(--fg-dim); max-width: 68ch; }

.chassis {
  background: linear-gradient(180deg, var(--chassis) 0%, var(--chassis-edge) 100%);
  border: 1px solid var(--chassis-edge);
  border-radius: 20px;
  padding: 18px;
  box-shadow: var(--shadow);
  overflow-x: auto;
}
.deck {
  background: var(--deck);
  border-radius: 11px;
  padding: 22px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  min-width: 940px;
}
.krow { display: flex; gap: 6px; }

.key {
  position: relative;
  height: 62px;
  border-radius: 8px;
  background: var(--cap-bg, var(--c-dead-bg));
  border: 1px solid var(--cap-edge);
  box-shadow: 0 2px 0 var(--cap-lip);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1px;
  padding: 4px 3px 5px;
  color: var(--cap-fg, var(--c-dead-fg));
  transition: background .16s, color .16s, transform .06s, box-shadow .06s;
}
.krow.fnrow .key { height: 44px; }

.key .cap-ghost {
  position: absolute;
  top: 4px;
  right: 5px;
  font-family: "JetBrains Mono", ui-monospace, monospace;
  font-size: 8.5px;
  color: var(--ghost);
  letter-spacing: .02em;
  pointer-events: none;
}
.key .legend {
  font-family: "JetBrains Mono", ui-monospace, monospace;
  font-weight: 700;
  font-size: 16px;
  line-height: 1.12;
  text-align: center;
  white-space: pre-line;
}
.key .legend.small { font-size: 10.5px; font-weight: 500; letter-spacing: -.01em; }
.key .legend.tiny  { font-size: 9px;   font-weight: 500; }
.key .sub {
  font-family: "JetBrains Mono", ui-monospace, monospace;
  font-size: 8.5px;
  color: var(--sub);
  text-align: center;
  line-height: 1.1;
}

.key.down {
  transform: translateY(2px);
  box-shadow: 0 0 0 1px var(--cap-fg, var(--c-dead-fg)),
              0 0 22px -4px var(--cap-fg, var(--c-dead-fg));
}

.split { display: flex; flex-direction: column; gap: 2px; }
.split .key { height: 30px; border-radius: 5px; }
.krow .split .key .legend { font-size: 11px; }
.krow .split .key .legend.tiny,
.krow .split .key .legend.small { font-size: 8px; line-height: 1.05; }
.krow .split .key .cap-ghost { top: 2px; right: 3px; }

/* ---------- readout ---------- */

.readout {
  display: flex;
  align-items: baseline;
  gap: 14px;
  flex-wrap: wrap;
  min-height: 26px;
  font-family: "JetBrains Mono", ui-monospace, monospace;
  font-size: 13px;
  color: var(--fg-dim);
}
.readout .pk {
  border: 1px solid var(--rule);
  border-radius: 5px;
  padding: 1px 7px;
  color: var(--fg);
  background: var(--bg-raise);
}
.readout .arrow { color: var(--fg-faint); }
.readout strong { color: var(--fg); font-weight: 700; }
.readout .hint { color: var(--fg-faint); font-style: italic; font-family: "Source Serif 4", serif; }

/* ---------- legend + prose ---------- */

.legend-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px 18px;
  font-family: "JetBrains Mono", ui-monospace, monospace;
  font-size: 11px;
  color: var(--fg-dim);
  border-top: 1px solid var(--rule);
  padding-top: 16px;
}
.swatch { display: inline-flex; align-items: center; gap: 7px; }
.swatch i {
  width: 11px; height: 11px; border-radius: 3px; display: block;
  border: 1px solid var(--cap-edge);
}

section.prose { display: flex; flex-direction: column; gap: 14px; }
section.prose h3 {
  font-family: Chivo, sans-serif;
  font-weight: 700;
  font-size: 13px;
  letter-spacing: .14em;
  text-transform: uppercase;
  color: var(--fg-faint);
  margin: 0;
  border-top: 1px solid var(--rule);
  padding-top: 22px;
}
section.prose p { margin: 0; max-width: 68ch; }
section.prose code {
  font-family: "JetBrains Mono", ui-monospace, monospace;
  font-size: .86em;
  background: var(--rule-soft);
  border: 1px solid var(--rule);
  border-radius: 4px;
  padding: 1px 5px;
}

.cols { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 26px; }

table { border-collapse: collapse; width: 100%; font-size: 15px; }
th, td { text-align: left; padding: 7px 12px 7px 0; border-bottom: 1px solid var(--rule-soft); }
th {
  font-family: "JetBrains Mono", ui-monospace, monospace;
  font-size: 10px; letter-spacing: .12em; text-transform: uppercase;
  color: var(--fg-faint); font-weight: 500;
}
td:first-child {
  font-family: "JetBrains Mono", ui-monospace, monospace;
  font-size: 13px; color: var(--fg); white-space: nowrap;
}

footer {
  border-top: 1px solid var(--rule);
  padding-top: 20px;
  font-family: "JetBrains Mono", ui-monospace, monospace;
  font-size: 12px;
  color: var(--fg-faint);
  display: flex;
  flex-wrap: wrap;
  gap: 8px 22px;
}
footer a { color: var(--fg-dim); }

@media (prefers-reduced-motion: reduce) {
  * { transition: none !important; animation: none !important; }
}
@media (max-width: 720px) {
  .wrap { padding: 0 16px 64px; }
  .switch { margin: 0 -16px; padding: 10px 16px; }
  header { padding-top: 40px; }
}
</style>

<div class="wrap">

<header>
  <div class="eyebrow">Karabiner-Elements · MacBook Air · US layout</div>
  <h1>splitmac</h1>
  <p class="standfirst">Split-keyboard ergonomics on a stock MacBook: the right
  hand moves a column over, the home row becomes modifiers and four layers, and
  twenty-five keys you should stop reaching for are switched off.</p>
  <div class="meta">
    <span>No firmware</span>
    <span>No external board</span>
    <span>One karabiner.json</span>
    <a href="https://github.com/noodleweapon/splitmac">github.com/noodleweapon/splitmac</a>
  </div>
</header>

<div class="switch" role="tablist" aria-label="Keymap layers" id="tabs"></div>

<div class="stage">
  <div class="stage-head">
    <h2 id="layer-name"></h2>
    <p id="layer-sub"></p>
  </div>

  <div class="chassis">
    <div class="deck" id="deck"></div>
  </div>

  <div class="readout" id="readout">
    <span class="hint">Press keys on your own keyboard — the matching cap lights up.
    Hold Caps Lock or Return, then hold S, P, M or H to preview a layer live.</span>
  </div>

  <div class="legend-row" id="legend"></div>
</div>

<div class="cols">
  <section class="prose">
    <h3>Why a gate</h3>
    <p>Home-row mods misfire when you type fast — the roll from <code>t</code> to
    <code>h</code> becomes a stray Command press. Here they simply do not exist
    until you hold Caps Lock or Return. Let go and the home row is eight plain
    letters again.</p>
    <p>Only one layer can be live at a time: every layer key is conditioned on the
    other three being off, so a fumbled two-key hold does nothing rather than
    something surprising.</p>
  </section>

  <section class="prose">
    <h3>The trainer</h3>
    <p>The number row, <code>esc</code>, <code>tab</code>, <code>delete</code>, the
    arrow cluster and the <code>Y</code>/<code>H</code>/<code>B</code> positions all
    type <code>HERROPERS</code>. It is deliberately embarrassing. Every trapped key
    has a home-row replacement, and after about a week you stop reaching.</p>
    <p>Delete the rule named <em>Bad-habit trainer</em> when the habit is gone. Or
    keep it. Nobody is judging.</p>
  </section>
</div>

<section class="prose">
  <h3>Thumbs and modifiers</h3>
  <table>
    <thead><tr><th>Physical key</th><th>Does</th></tr></thead>
    <tbody>
      <tr><td>Left Shift</td><td>types <code>'</code></td></tr>
      <tr><td>Right Shift</td><td>types <code>;</code></td></tr>
      <tr><td>Left Command</td><td>tap = Return, hold = Shift</td></tr>
      <tr><td>Right Option</td><td>tap = Tab, hold = Shift</td></tr>
      <tr><td>Right Command</td><td>Delete</td></tr>
      <tr><td>Left Option</td><td>Control</td></tr>
      <tr><td>Caps Lock / Return</td><td>hold arms the layers; tap does nothing</td></tr>
      <tr><td>Shift + <code>/</code></td><td>Escape</td></tr>
      <tr><td>F6</td><td>toggles the entire keymap off and on</td></tr>
    </tbody>
  </table>
</section>

<footer>
  <span>Layout data generated from karabiner.json</span>
  <a href="https://github.com/getreuer/qmk-keymap">Reference: @getreuer's QMK keymap</a>
  <a href="https://karabiner-elements.pqrs.org/">Karabiner-Elements</a>
  <a href="https://github.com/GalileoBlues/Gallium">Gallium v2 by GalileoBlues</a>
</footer>

</div>

<script>
const DATA = __DATA__;

const U = 66, GAP = 6;
const CLASSES = [
  ["alpha", "base letters"], ["punct", "punctuation & digits"],
  ["layer", "layer key"], ["mod", "modifier"],
  ["gate", "hold gate"], ["system", "app / system"],
  ["trainer", "disabled — types HERROPERS"],
];

const deck = document.getElementById("deck");
const tabs = document.getElementById("tabs");
const readout = document.getElementById("readout");
const nameEl = document.getElementById("layer-name");
const subEl = document.getElementById("layer-sub");

const cells = new Map();   // key id -> element
const byCode = new Map();  // KeyboardEvent.code -> key id

// ---- build the board -------------------------------------------------------

DATA.rows.forEach((row, r) => {
  const el = document.createElement("div");
  el.className = "krow" + (r === 0 ? " fnrow" : "");
  row.forEach(k => {
    if (k.id === "__updown") {
      const box = document.createElement("div");
      box.className = "split";
      box.style.width = (k.w * U - GAP) + "px";
      ["up_arrow", "down_arrow"].forEach(id => box.appendChild(makeKey(
        { id, cap: id === "up_arrow" ? "↑" : "↓", w: k.w }, true)));
      el.appendChild(box);
      return;
    }
    el.appendChild(makeKey(k, false));
  });
  deck.appendChild(el);
});

function makeKey(k, inSplit) {
  const el = document.createElement("div");
  el.className = "key";
  if (!inSplit) el.style.width = (k.w * U - GAP) + "px";
  el.dataset.id = k.id;

  const ghost = document.createElement("span");
  ghost.className = "cap-ghost";
  ghost.textContent = k.cap || "";
  el.appendChild(ghost);

  const legend = document.createElement("span");
  legend.className = "legend";
  el.appendChild(legend);

  const sub = document.createElement("span");
  sub.className = "sub";
  el.appendChild(sub);

  cells.set(k.id, el);
  const code = k.code || (k.id === "up_arrow" ? "ArrowUp" : k.id === "down_arrow" ? "ArrowDown" : "");
  if (code) byCode.set(code, k.id);
  return el;
}

// ---- paint a layer ---------------------------------------------------------

let current = DATA.layers[0];

function paint(layer) {
  current = layer;
  nameEl.textContent = layer.name;
  subEl.textContent = layer.sub;
  cells.forEach((el, id) => {
    const e = layer.keys[id];
    const cls = e ? e.cls : "dead";
    el.style.setProperty("--cap-bg", `var(--c-${cls}-bg)`);
    el.style.setProperty("--cap-fg", `var(--c-${cls}-fg)`);
    const legend = el.querySelector(".legend");
    const sub = el.querySelector(".sub");
    const main = e ? e.main : "";
    legend.textContent = main;
    legend.className = "legend" +
      (main.length <= 3 && !main.includes("\n") ? "" :
       main.length <= 9 && !main.includes("\n") ? " small" : " tiny");
    sub.textContent = e ? e.sub : "";
  });
  [...tabs.children].forEach(b =>
    b.setAttribute("aria-selected", String(b.dataset.layer === layer.id)));
}

DATA.layers.forEach(l => {
  const b = document.createElement("button");
  b.className = "tab";
  b.setAttribute("role", "tab");
  b.dataset.layer = l.id;
  b.textContent = l.name;
  b.addEventListener("click", () => { pinned = l; paint(l); });
  tabs.appendChild(b);
});

// ---- legend ----------------------------------------------------------------

const legendRow = document.getElementById("legend");
CLASSES.forEach(([cls, label]) => {
  const s = document.createElement("span");
  s.className = "swatch";
  s.innerHTML = `<i style="background:var(--c-${cls}-bg);box-shadow:inset 0 0 0 1px var(--c-${cls}-fg)"></i>${label}`;
  legendRow.appendChild(s);
});

// ---- live keyboard ---------------------------------------------------------

let pinned = DATA.layers[0];
let gate = false;
const held = new Set();
const layerByHold = {};
DATA.layers.forEach(l => { if (l.hold) layerByHold[l.hold] = l; });

const base = DATA.layers[0];
const GLYPH = { number: "S", "sym-left": "P", "sym-right": "M", nav: "H" };

function describe(id) {
  const e = current.keys[id] || base.keys[id];
  if (!e) return null;
  return e;
}

function report(id) {
  const cap = cells.get(id)?.querySelector(".cap-ghost")?.textContent || id;
  const e = describe(id);
  if (!e) { readout.innerHTML = `<span class="pk">${cap}</span> <span class="arrow">is untouched</span>`; return; }
  const main = (e.main || "").replace(/\n/g, " ");
  let html = `<span class="pk">${cap}</span><span class="arrow">&rarr;</span><strong>${main}</strong>`;
  if (e.sub) html += `<span class="arrow">·</span><span>${e.sub}</span>`;
  readout.innerHTML = html;
}

function resolve() {
  if (gate) {
    for (const h of held) {
      if (layerByHold[h]) return layerByHold[h];
    }
    return DATA.layers.find(l => l.id === "mods") || pinned;
  }
  return pinned;
}

addEventListener("keydown", ev => {
  const id = byCode.get(ev.code);
  if (ev.code === "Tab" || ev.metaKey || ev.ctrlKey) return;  // leave the browser alone
  if (!id) return;
  ev.preventDefault();
  held.add(id);
  cells.get(id)?.classList.add("down");
  if (id === "caps_lock" || id === "return_or_enter") gate = true;
  paint(resolve());
  report(id);
});

addEventListener("keyup", ev => {
  const id = byCode.get(ev.code);
  if (!id) return;
  held.delete(id);
  cells.get(id)?.classList.remove("down");
  if (id === "caps_lock" || id === "return_or_enter") gate = false;
  paint(resolve());
});

addEventListener("blur", () => {
  held.clear();
  gate = false;
  cells.forEach(el => el.classList.remove("down"));
  paint(pinned);
});

cells.forEach((el, id) => {
  el.addEventListener("pointerenter", () => report(id));
});

paint(pinned);
</script>
"""


def main():
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out = os.path.join(here, "keymap.html")
    with open(out, "w") as f:
        f.write(TEMPLATE.replace("__DATA__", json.dumps(DATA, ensure_ascii=False)))
    print("wrote", os.path.relpath(out, here))


if __name__ == "__main__":
    main()
