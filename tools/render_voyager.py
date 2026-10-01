#!/usr/bin/env python3
"""Render each layer of the Voyager keymap as an SVG.

    python3 tools/render_voyager.py        # writes img/voyager-*.svg

Same colour roles and themes as render_svg.py, drawn on a column-staggered
split instead of a laptop deck. Data comes from voyager.py.
"""

import os
import sys
from xml.sax.saxutils import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render_svg import THEMES, U, GAP, rounded, text, fit  # noqa: E402
from voyager import LAYERS, GHOST, LEFT_STAGGER, RIGHT_STAGGER  # noqa: E402

PAD = 28          # padding inside each half's deck
DECK_PAD = 14     # case border around each deck
HALF_GAP = 70     # space between the two halves
HEADER = 92       # title block above the keyboard
THUMB_DROP = 0.55 # how far below the bottom row the thumb keys sit, in units


def half_keys(side):
    """Yield (key_id, x, y, w, h) in px, relative to the half's deck origin."""
    stagger = LEFT_STAGGER if side == "L" else RIGHT_STAGGER
    for r in range(4):
        for c in range(6):
            x = PAD + c * U
            y = PAD + (r + stagger[c]) * U
            yield f"{side}{r}{c}", x, y, U - GAP, U - GAP
    # Thumb keys sit under the inner two columns, stepping down toward the gap.
    base_y = PAD + (4 + THUMB_DROP) * U
    if side == "L":
        yield "LT0", PAD + 4 * U, base_y, U - GAP, U - GAP
        yield "LT1", PAD + 5 * U + 4, base_y + 0.25 * U, U + 8, U - GAP
    else:
        yield "RT0", PAD - 12, base_y + 0.25 * U, U + 8, U - GAP
        yield "RT1", PAD + 1 * U, base_y, U - GAP, U - GAP


def half_size():
    w = 6 * U - GAP + 2 * PAD
    h = PAD * 2 + (4 + THUMB_DROP + 1.25) * U - GAP
    return w, h


def draw_key(out, t, kid, X, Y, w, h, entry, dim):
    if entry:
        main, sub, cls = entry
    else:
        main, sub, cls = "", "", "dead"

    out.append(rounded(X, Y, w, h, 8, t[cls], t["cap_edge"], 1))

    ghost = GHOST.get(kid, "")
    if ghost:
        out.append(text(X + w - 6, Y + 14, ghost, t["ghost"], 10, 500, "end", 0.85))

    if not main:
        return
    lines = main.split("\n")
    size = 20 if len(lines) == 1 and len(lines[0]) <= 2 else (
        13 if len(lines) == 1 and len(lines[0]) <= 7 else 11)
    weight = 700 if len(lines) == 1 and len(lines[0]) <= 2 else 600
    size = min(fit(ln, size, w - 10) for ln in lines)
    cy = Y + h / 2 + (5 if not sub else -1)
    cy -= (len(lines) - 1) * (size + 1) / 2
    for i, ln in enumerate(lines):
        out.append(text(X + w / 2, cy + i * (size + 1), ln, t[cls + "_t"], size, weight))
    if sub:
        out.append(text(X + w / 2, Y + h - 9, sub, t["sub"], fit(sub, 9.5, w - 6, 6.5), 500))


def render(layer, theme_name):
    t = THEMES[theme_name]
    hw, hh = half_size()
    W = 2 * (hw + 2 * DECK_PAD) + HALF_GAP + 40
    H = hh + 2 * DECK_PAD + HEADER + 40

    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.0f}" height="{H:.0f}" '
           f'viewBox="0 0 {W:.0f} {H:.0f}" role="img" '
           f'aria-label="{escape(layer["name"])} layer of splitmac on the ZSA Voyager">']
    out.append(f'<rect width="{W:.0f}" height="{H:.0f}" fill="{t["page"]}"/>')
    out.append(text(20 + DECK_PAD + 4, 46, layer["name"], t["title"], 30, 700, "start"))
    out.append(text(20 + DECK_PAD + 4, 72, layer["sub"], t["subtitle"], 15, 400, "start"))

    keys = layer["keys"]
    dim = not layer["full"]

    for i, side in enumerate(("L", "R")):
        cx = 20 + i * (hw + 2 * DECK_PAD + HALF_GAP)
        cy = HEADER + 20
        out.append(rounded(cx, cy, hw + 2 * DECK_PAD, hh + 2 * DECK_PAD, 18,
                           t["chassis"], t["chassis_edge"], 1.5))
        out.append(rounded(cx + DECK_PAD, cy + DECK_PAD, hw, hh, 10, t["deck"]))
        for kid, x, y, w, h in half_keys(side):
            entry = keys.get(kid)
            if entry is None and not dim:
                entry = ("", "", "dead")
            draw_key(out, t, kid, cx + DECK_PAD + x, cy + DECK_PAD + y, w, h, entry, dim)

    out.append("</svg>")
    return "\n".join(out)


def main():
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    outdir = os.path.join(here, "img")
    os.makedirs(outdir, exist_ok=True)
    for layer in LAYERS:
        for theme in THEMES:
            path = os.path.join(outdir, f'{layer["id"]}-{theme}.svg')
            with open(path, "w") as f:
                f.write(render(layer, theme))
            print("wrote", os.path.relpath(path, here))


if __name__ == "__main__":
    main()
