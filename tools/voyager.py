"""Layout data for the ZSA Voyager version of splitmac.

This mirrors keymap.py for the QMK firmware in qmk/. The firmware itself is
hand-written C (qmk/keyboards/zsa/voyager/keymaps/splitmac/keymap.c); this
file is only the source for the diagrams, so keep the two in step.

Key ids are positions, not key codes:

    L<row><col>  left hand, rows 0-3 top to bottom, col 0 = outer (pinky) key
    R<row><col>  right hand, rows 0-3 top to bottom, col 0 = inner (index) key
    LT0 / LT1    left thumb, outer / inner
    RT0 / RT1    right thumb, inner / outer

The `ghost` legend on each cap is the QWERTY key whose Karabiner rule the cap
reproduces, so the two sets of diagrams can be read side by side.
"""

from keymap import TRAINER_KEYS  # noqa: F401  (kept for the colour legend)

# Column stagger in key units, from keyboard.json in qmk_firmware.
LEFT_STAGGER = [0.5, 0.5, 0.25, 0.0, 0.25, 0.5]
RIGHT_STAGGER = [0.5, 0.25, 0.0, 0.25, 0.5, 0.5]

# ---------------------------------------------------------------------------
# Which QWERTY key (as the Karabiner rules name it) each Voyager cap stands for.
# "" means the cap has no laptop counterpart.
# ---------------------------------------------------------------------------

GHOST = {
    "L00": "`", "L01": "1", "L02": "2", "L03": "3", "L04": "4", "L05": "5",
    "L10": "tab", "L11": "Q", "L12": "W", "L13": "E", "L14": "R", "L15": "T",
    "L20": "caps", "L21": "A", "L22": "S", "L23": "D", "L24": "F", "L25": "G",
    "L30": "", "L31": "shift", "L32": "Z", "L33": "X", "L34": "C", "L35": "V",
    "LT0": "cmd", "LT1": "space",
    "R00": "6", "R01": "7", "R02": "8", "R03": "9", "R04": "0", "R05": "-",
    "R10": "U", "R11": "I", "R12": "O", "R13": "P", "R14": "[", "R15": "]",
    "R20": "J", "R21": "K", "R22": "L", "R23": ";", "R24": "'", "R25": "return",
    "R30": "M", "R31": ",", "R32": ".", "R33": "/", "R34": "shift", "R35": "",
    "RT0": "cmd", "RT1": "opt",
}

TRAINER = [
    "L00", "L01", "L02", "L03", "L04", "L05",
    "R00", "R01", "R02", "R03", "R04", "R05",
    "L10", "L20", "L30",
    "R15", "R25", "R35",
]

# --- base layer -------------------------------------------------------------
# key -> (main legend, sub legend, class)

BASE = {
    "L11": ("B", "", "alpha"), "L12": ("L", "", "alpha"),
    "L13": ("D", "", "alpha"), "L14": ("C", "", "alpha"),
    "L15": ("V", "", "alpha"),
    "L21": ("N", "⇧ shift", "mod"),
    "L22": ("R", "⌥ opt", "mod"),
    "L23": ("T", "⌘ cmd", "mod"),
    "L24": ("S", "№ num", "layer"),
    "L25": ("G", "⌃ ctrl", "mod"),
    "L31": ("Z", "", "alpha"), "L32": ("X", "", "alpha"),
    "L33": ("Q", "", "alpha"),
    "L34": ("M", "& sym", "layer"),
    "L35": ("W", "", "alpha"),
    "LT0": ("space", "", "mod"),
    "LT1": ("left\ngate", "hold", "gate"),

    "R10": ("J", "", "alpha"), "R11": ("F", "", "alpha"),
    "R12": ("O", "", "alpha"), "R13": ("U", "", "alpha"),
    "R14": (".", "⇧ esc", "alpha"),
    "R20": ("Y", "⌃ ctrl", "mod"),
    "R21": ("H", "→ nav", "layer"),
    "R22": ("A", "⌘ cmd", "mod"),
    "R23": ("E", "⌥ opt", "mod"),
    "R24": ("I", "⇧ shift", "mod"),
    "R30": ("K", "", "alpha"),
    "R31": ("P", "# sym", "layer"),
    "R32": (",", "⇧ ⌥C", "alpha"),
    "R33": ("_", "", "punct"),
    "R34": ("'", "", "punct"),
    "RT0": ("right\ngate", "hold", "gate"),
    "RT1": ("⌫ delete", "", "mod"),
}
for _k in TRAINER:
    BASE[_k] = ("Disabled", "", "trainer")

# --- hold layers ------------------------------------------------------------

NUM = {
    "R11": ("7", "", "punct"), "R12": ("8", "", "punct"), "R13": ("9", "", "punct"),
    "R21": ("0", "", "punct"), "R22": ("1", "", "punct"),
    "R23": ("2", "", "punct"), "R24": ("3", "", "punct"),
    "R31": ("4", "", "punct"), "R32": ("5", "", "punct"),
    "R33": ("6", "", "punct"), "R34": ("~", "", "punct"),
    "L24": ("hold", "S", "layer"),
    "LT1": ("hold", "left gate", "gate"),
}

SYM_RIGHT = {
    "R11": (";", "", "punct"), "R12": ("&", "", "punct"),
    "R13": ("$", "", "punct"), "R14": ("#", "", "punct"),
    "R21": ("[", "", "punct"), "R22": ("]", "", "punct"),
    "R23": ("(", "", "punct"), "R24": (")", "", "punct"),
    "R31": (":", "", "punct"), "R32": ("\\", "", "punct"),
    "R33": ("%", "", "punct"), "R34": ("?", "", "punct"),
    "L34": ("hold", "M", "layer"),
    "LT1": ("hold", "left gate", "gate"),
}

SYM_LEFT = {
    "L11": ("^", "", "punct"), "L12": ("*", "", "punct"),
    "L13": ("-", "", "punct"), "L14": ("|", "", "punct"),
    "L21": ("+", "", "punct"), "L22": ("!", "", "punct"),
    "L23": ("/", "", "punct"), "L24": ("=", "", "punct"),
    "L31": ("`", "", "punct"), "L32": ("<", "", "punct"),
    "L33": (">", "", "punct"), "L34": ("@", "", "punct"),
    "R31": ("hold", "P", "layer"),
    "RT0": ("hold", "right gate", "gate"),
}

NAV = {
    "L11": ("←", "", "punct"), "L12": ("↑", "", "punct"),
    "L13": ("↓", "", "punct"), "L14": ("→", "", "punct"),
    "L21": ("click", "", "punct"), "L22": ("tab", "", "punct"),
    "L23": ("esc", "", "punct"), "L24": ("⏎", "", "punct"),
    "L31": ("←×5", "", "punct"), "L32": ("↑×5", "", "punct"),
    "L33": ("↓×5", "", "punct"), "L34": ("→×5", "", "punct"),
    "R21": ("hold", "H", "layer"),
    "RT0": ("hold", "right gate", "gate"),
}

MODS = {
    "L21": ("⇧", "left", "mod"),
    "L22": ("⌥", "left", "mod"),
    "L23": ("⌘", "left", "mod"),
    "L24": ("№", "numbers", "layer"),
    "L25": ("⌃", "left", "mod"),
    "L34": ("&", "sym R", "layer"),
    "R20": ("⌃", "left", "mod"),
    "R21": ("→", "nav", "layer"),
    "R22": ("⌘", "left", "mod"),
    "R23": ("⌥", "left", "mod"),
    "R24": ("⇧", "right", "mod"),
    "R31": ("#", "sym L", "layer"),
    "LT1": ("hold", "left gate", "gate"),
    "RT0": ("hold", "right gate", "gate"),
}

PLAIN = {
    "L00": ("esc", "", "system"),
    "L01": ("1", "", "punct"), "L02": ("2", "", "punct"), "L03": ("3", "", "punct"),
    "L04": ("4", "", "punct"), "L05": ("5", "", "punct"),
    "L10": ("tab", "", "mod"),
    "L11": ("Q", "", "alpha"), "L12": ("W", "", "alpha"), "L13": ("E", "", "alpha"),
    "L14": ("R", "", "alpha"), "L15": ("T", "", "alpha"),
    "L20": ("⌃", "", "mod"),
    "L21": ("A", "", "alpha"), "L22": ("S", "", "alpha"), "L23": ("D", "", "alpha"),
    "L24": ("F", "", "alpha"), "L25": ("G", "", "alpha"),
    "L30": ("⇧", "", "mod"),
    "L31": ("Z", "", "alpha"), "L32": ("X", "", "alpha"), "L33": ("C", "", "alpha"),
    "L34": ("V", "", "alpha"), "L35": ("B", "", "alpha"),
    "LT0": ("⌘", "", "mod"), "LT1": ("space", "", "mod"),
    "R00": ("6", "", "punct"), "R01": ("7", "", "punct"), "R02": ("8", "", "punct"),
    "R03": ("9", "", "punct"), "R04": ("0", "", "punct"), "R05": ("-", "", "punct"),
    "R10": ("Y", "", "alpha"), "R11": ("U", "", "alpha"), "R12": ("I", "", "alpha"),
    "R13": ("O", "", "alpha"), "R14": ("P", "", "alpha"), "R15": ("\\", "", "punct"),
    "R20": ("H", "", "alpha"), "R21": ("J", "", "alpha"), "R22": ("K", "", "alpha"),
    "R23": ("L", "", "alpha"), "R24": (";", "", "punct"), "R25": ("'", "", "punct"),
    "R30": ("N", "", "alpha"), "R31": ("M", "", "alpha"), "R32": (",", "", "punct"),
    "R33": (".", "", "punct"), "R34": ("/", "", "punct"), "R35": ("⇧", "", "mod"),
    "RT0": ("⏎", "", "mod"), "RT1": ("⌫", "", "mod"),
}


def _with_disabled(keys):
    merged = {k: ("Disabled", "", "trainer") for k in TRAINER}
    merged.update(keys)
    return merged


LAYERS = [
    {
        "id": "voyager-base",
        "name": "Voyager · Base",
        "sub": "Same alphas as the laptop, with the right hand and the left bottom row back in their own columns.",
        "keys": BASE,
        "full": True,
    },
    {
        "id": "voyager-mods",
        "name": "Voyager · Hold gate + home-row mods",
        "sub": "Inner left thumb arms the left hand, inner right thumb arms the right. Then hold a key.",
        "keys": _with_disabled(MODS),
        "full": False,
    },
    {
        "id": "voyager-number",
        "name": "Voyager · Number layer",
        "sub": "left gate + hold S. Digits land on the right hand.",
        "keys": _with_disabled(NUM),
        "full": False,
    },
    {
        "id": "voyager-sym-left",
        "name": "Voyager · Symbol layer — left",
        "sub": "right gate + hold P. Math, brackets and shell glyphs.",
        "keys": _with_disabled(SYM_LEFT),
        "full": False,
    },
    {
        "id": "voyager-sym-right",
        "name": "Voyager · Symbol layer — right",
        "sub": "left gate + hold M. Pairs, punctuation and money.",
        "keys": _with_disabled(SYM_RIGHT),
        "full": False,
    },
    {
        "id": "voyager-nav",
        "name": "Voyager · Navigation layer",
        "sub": "right gate + hold H. Top row moves the caret, home row is click / tab / esc / return, bottom row jumps five.",
        "keys": _with_disabled(NAV),
        "full": False,
    },
    {
        "id": "voyager-plain",
        "name": "Voyager · Plain QWERTY",
        "sub": "Toggle with both top-corner keys together. Replaces the laptop's F6 profile switch.",
        "keys": PLAIN,
        "full": True,
    },
]
