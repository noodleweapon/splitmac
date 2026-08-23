#!/usr/bin/env python3
"""Render each layer of the keymap as a MacBook Air shaped SVG.

    python3 tools/render_svg.py            # writes img/*.svg

Two files come out per layer, `-light` and `-dark`, so the README can serve the
right one with <picture>.
"""

import os
import sys
from xml.sax.saxutils import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from keymap import ROWS, ROW_WIDTH, LAYERS  # noqa: E402

U = 66            # one key unit, px
GAP = 6           # gap between keycaps
PAD = 34          # padding inside the deck
DECK_PAD = 20     # chassis border around the deck
HEADER = 92       # title block above the keyboard

THEMES = {
    "light": dict(
        page="#f4f4f2", chassis="#d8d8d5", chassis_edge="#bdbdb9", deck="#1b1b1f",
        cap="#2c2c31", cap_edge="#3d3d44", text="#f2f2f4", sub="#8f8f9b",
        title="#17171a", subtitle="#5f5f6a",
        alpha="#2c2c31", punct="#1e3a5f", trainer="#000000", gate="#1f3d33",
        layer="#3d2a52", mod="#4a3410", system="#123a3c", dead="#232327",
        alpha_t="#f2f2f4", punct_t="#8ecbff", trainer_t="#63636b", gate_t="#8ff0cd",
        layer_t="#d3aaff", mod_t="#ffcf7a", system_t="#7fe6e0", dead_t="#5a5a63",
        ghost="#55555e",
    ),
    "dark": dict(
        page="#0d0d10", chassis="#1e1e22", chassis_edge="#2c2c32", deck="#0a0a0c",
        cap="#1f1f24", cap_edge="#33333b", text="#ececf0", sub="#7e7e8a",
        title="#f2f2f5", subtitle="#9a9aa6",
        alpha="#1f1f24", punct="#15293f", trainer="#000000", gate="#152e26",
        layer="#2c1f3c", mod="#372709", system="#0d2b2d", dead="#161619",
        alpha_t="#ececf0", punct_t="#7cc0f8", trainer_t="#5c5c64", gate_t="#79dfbc",
        layer_t="#c39cf5", mod_t="#f0be6b", system_t="#6fd8d2", dead_t="#4c4c55",
        ghost="#4a4a53",
    ),
}


def key_rows_px():
    """Yield (row_index, key_id, label, x, y, w, h) in px for every key."""
    for r, row in enumerate(ROWS):
        x = PAD
        y = PAD + r * (U + GAP)
        h = U * 0.72 if r == 0 else U
        if r > 0:
            y = PAD + 0.72 * U + GAP + (r - 1) * (U + GAP)
        for kid, label, w in row:
            yield r, kid, label, x, y, w * U - GAP, h
            x += w * U


def board_size():
    w = ROW_WIDTH * U - GAP + 2 * PAD
    h = PAD * 2 + 0.72 * U + GAP + 5 * (U + GAP) - GAP
    return w, h


def rounded(x, y, w, h, r, fill, stroke=None, sw=1):
    s = f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" fill="{fill}"'
    if stroke:
        s += f' stroke="{stroke}" stroke-width="{sw}"'
    return s + "/>"


def fit(s, size, avail, floor=8.0):
    """Shrink font size until the string plausibly fits `avail` px."""
    while size > floor and len(s) * size * 0.55 > avail:
        size -= 0.5
    return size


def text(x, y, s, fill, size, weight=500, anchor="middle", opacity=1.0, family=None):
    fam = family or "-apple-system, BlinkMacSystemFont, 'SF Pro Text', 'Helvetica Neue', Arial, sans-serif"
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{fill}" font-size="{size}" '
            f'font-weight="{weight}" text-anchor="{anchor}" opacity="{opacity}" '
            f'font-family="{fam}">{escape(s)}</text>')


def render(layer, theme_name):
    t = THEMES[theme_name]
    bw, bh = board_size()
    W = bw + 2 * DECK_PAD + 40
    H = bh + 2 * DECK_PAD + HEADER + 40
    ox, oy = 20 + DECK_PAD, HEADER + 20 + DECK_PAD

    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.0f}" height="{H:.0f}" '
           f'viewBox="0 0 {W:.0f} {H:.0f}" role="img" '
           f'aria-label="{escape(layer["name"])} layer of the splitmac">']
    out.append(f'<rect width="{W:.0f}" height="{H:.0f}" fill="{t["page"]}"/>')

    # title block
    out.append(text(20 + DECK_PAD + 4, 46, layer["name"], t["title"], 30, 700, "start"))
    out.append(text(20 + DECK_PAD + 4, 72, layer["sub"], t["subtitle"], 15, 400, "start"))

    # laptop chassis + recessed deck
    out.append(rounded(20, HEADER + 20, bw + 2 * DECK_PAD, bh + 2 * DECK_PAD, 22,
                       t["chassis"], t["chassis_edge"], 1.5))
    out.append(rounded(ox, oy, bw, bh, 12, t["deck"]))

    keys = layer["keys"]
    dim = not layer["full"]

    for r, kid, label, x, y, w, h in key_rows_px():
        X, Y = ox + x, oy + y
        entry = keys.get(kid)

        if kid == "__updown":
            # inverted-T: up over down inside one unit
            half = (h - 2) / 2
            for j, (arrow, sub_id) in enumerate((("↑", "up_arrow"), ("↓", "down_arrow"))):
                e = keys.get(sub_id)
                cls = e[2] if e else ("trainer" if not dim else "dead")
                fill = t[cls] if (e or not dim) else t["dead"]
                fg = t[cls + "_t"] if (e or not dim) else t["dead_t"]
                yy = Y + j * (half + 2)
                out.append(rounded(X, yy, w, half, 5, fill, t["cap_edge"], 1))
                out.append(text(X + w / 2, yy + half / 2 + 5, arrow, fg, 13, 600))
            continue

        if entry:
            main, sub, cls = entry
        elif dim:
            main, sub, cls = "", "", "dead"
        else:
            main, sub, cls = label, "", "dead"

        fill = t[cls]
        fg = t[cls + "_t"]
        out.append(rounded(X, Y, w, h, 8, fill, t["cap_edge"], 1))

        # ghost legend: what is physically printed on the MacBook keycap
        if label and (dim or cls != "dead" or True):
            out.append(text(X + w - 6, Y + 14, label, t["ghost"], 10, 500, "end", 0.85))

        if not main:
            continue

        lines = main.split("\n")
        size = 20 if len(lines) == 1 and len(lines[0]) <= 2 else (
            13 if len(lines) == 1 and len(lines[0]) <= 7 else 11)
        weight = 700 if len(lines) == 1 and len(lines[0]) <= 2 else 600
        size = min(fit(ln, size, w - 10) for ln in lines)
        cy = Y + h / 2 + (5 if not sub else -1)
        cy -= (len(lines) - 1) * (size + 1) / 2
        for i, ln in enumerate(lines):
            out.append(text(X + w / 2, cy + i * (size + 1), ln, fg, size, weight))
        if sub:
            out.append(text(X + w / 2, Y + h - 9, sub, t["sub"], fit(sub, 9.5, w - 6, 6.5), 500))

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
