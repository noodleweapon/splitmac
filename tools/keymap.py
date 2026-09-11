"""Single source of truth for the splitmac layout.

Everything downstream (the SVG renderer, the interactive page) reads its data
from here so the diagrams can never drift away from karabiner.json.

Geometry follows a US MacBook Air (M2/M3/M4) Magic Keyboard: six rows, every
row 14.5u wide, full-height function row with Touch ID, inverted-T arrows.
"""

# ---------------------------------------------------------------------------
# Physical keyboard geometry.  Each key is (id, label, width_in_units).
# `id` is the Karabiner key_code of the *physical* key.
# ---------------------------------------------------------------------------

ROWS = [
    [  # function row
        ("escape", "esc", 1.5),
        ("f1", "F1", 1.0), ("f2", "F2", 1.0), ("f3", "F3", 1.0), ("f4", "F4", 1.0),
        ("f5", "F5", 1.0), ("f6", "F6", 1.0), ("f7", "F7", 1.0), ("f8", "F8", 1.0),
        ("f9", "F9", 1.0), ("f10", "F10", 1.0), ("f11", "F11", 1.0), ("f12", "F12", 1.0),
        ("touch_id", "⏻", 1.0),
    ],
    [
        ("grave_accent_and_tilde", "`", 1.0),
        ("1", "1", 1.0), ("2", "2", 1.0), ("3", "3", 1.0), ("4", "4", 1.0),
        ("5", "5", 1.0), ("6", "6", 1.0), ("7", "7", 1.0), ("8", "8", 1.0),
        ("9", "9", 1.0), ("0", "0", 1.0),
        ("hyphen", "-", 1.0), ("equal_sign", "=", 1.0),
        ("delete_or_backspace", "delete", 1.5),
    ],
    [
        ("tab", "tab", 1.5),
        ("q", "Q", 1.0), ("w", "W", 1.0), ("e", "E", 1.0), ("r", "R", 1.0),
        ("t", "T", 1.0), ("y", "Y", 1.0), ("u", "U", 1.0), ("i", "I", 1.0),
        ("o", "O", 1.0), ("p", "P", 1.0),
        ("open_bracket", "[", 1.0), ("close_bracket", "]", 1.0),
        ("backslash", "\\", 1.0),
    ],
    [
        ("caps_lock", "caps", 1.75),
        ("a", "A", 1.0), ("s", "S", 1.0), ("d", "D", 1.0), ("f", "F", 1.0),
        ("g", "G", 1.0), ("h", "H", 1.0), ("j", "J", 1.0), ("k", "K", 1.0),
        ("l", "L", 1.0), ("semicolon", ";", 1.0), ("quote", "'", 1.0),
        ("return_or_enter", "return", 1.75),
    ],
    [
        ("left_shift", "shift", 2.25),
        ("z", "Z", 1.0), ("x", "X", 1.0), ("c", "C", 1.0), ("v", "V", 1.0),
        ("b", "B", 1.0), ("n", "N", 1.0), ("m", "M", 1.0),
        ("comma", ",", 1.0), ("period", ".", 1.0), ("slash", "/", 1.0),
        ("right_shift", "shift", 2.25),
    ],
    [
        ("fn", "fn", 1.0),
        ("left_control", "control", 1.0),
        ("left_option", "option", 1.25),
        ("left_command", "command", 1.25),
        ("spacebar", "", 4.75),
        ("right_command", "command", 1.25),
        ("right_option", "option", 1.0),
        ("left_arrow", "←", 1.0),
        ("__updown", "", 1.0),          # split cell: up over down
        ("right_arrow", "→", 1.0),
    ],
]

ROW_WIDTH = 14.5

# ---------------------------------------------------------------------------
# Semantic classes -> colour roles used by the renderers.
# ---------------------------------------------------------------------------
# alpha    letters produced by the base layout
# punct    punctuation / digits produced by a layer
# trainer  bad-habit trainer: the key is deliberately booby-trapped
# gate     Caps Lock / Return, which arm the hold layers
# layer    a key that holds down into a layer
# mod      modifier behaviour (tap/hold, remapped modifiers)
# magic    the magic key: emits the letter that follows the last one typed
# system   app launchers, screenshots, profile toggle
# dead     untouched pass-through key

TRAINER_KEYS = [
    "grave_accent_and_tilde", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
    "hyphen", "equal_sign", "delete_or_backspace", "tab", "close_bracket",
    "backslash", "escape", "left_control", "y", "h", "b", "n",
]

# --- base layer -------------------------------------------------------------
# key -> (main legend, sub legend, class)

BASE = {
    # alphas: right hand sits one column to the right of QWERTY home
    "q": ("B", "", "alpha"),   "w": ("L", "", "alpha"),
    "e": ("D", "", "alpha"),   "r": ("C", "", "alpha"),
    "t": ("V", "", "alpha"),
    "u": ("J", "", "alpha"),   "i": ("F", "", "alpha"),
    "o": ("O", "", "alpha"),   "p": ("U", "", "alpha"),
    "open_bracket": ("✦", "magic", "magic"),

    "a": ("N", "& sym", "layer"),
    "s": ("R", "⌥ opt", "mod"),
    "d": ("T", "⌘ cmd", "mod"),
    "f": ("S", "№ num", "layer"),
    "g": ("G", "", "alpha"),
    "j": ("Y", "", "alpha"),
    "k": ("H", "→ nav", "layer"),
    "l": ("A", "⌘ cmd", "mod"),
    "semicolon": ("E", "⌥ opt", "mod"),
    "quote": ("I", "# sym", "layer"),

    "z": ("X", "", "alpha"),   "x": ("Q", "", "alpha"),
    "c": ("M", "", "alpha"),
    "v": ("W", "", "alpha"),
    "m": ("K", "", "alpha"),
    "comma": ("P", "", "alpha"),
    "period": (",", "⇧ ⌥C", "alpha"),
    "slash": (".", "⇧ esc", "alpha"),

    # gates
    "caps_lock": ("⇧ shift", "tap: esc", "mod"),
    "return_or_enter": ("⇧ shift", "tap: return", "mod"),

    # modifiers & thumbs
    "left_shift": ("Z", "", "alpha"),
    "right_shift": ("'", "", "punct"),
    "left_option": ("control", "", "mod"),
    "left_command": ("no-op", "", "dead"),
    "right_command": ("⌫ delete", "", "mod"),
    "right_option": ("no-op", "", "dead"),
    "spacebar": ("space", "", "dead"),
    "fn": ("fn", "", "dead"),
    "touch_id": ("⏻", "", "dead"),

    # function row
    "f3": ("⌘⇧⌃ 4", "clip shot", "system"),
    "f4": ("Raycast", "", "system"),
    "f6": ("toggle\nkeymap", "on / off", "system"),
}

_MEDIA = {
    "f1": "☀−", "f2": "☀+", "f5": "mic", "f7": "⏮", "f8": "⏯",
    "f9": "⏭", "f10": "mute", "f11": "vol −", "f12": "vol +",
}
for _k, _legend in _MEDIA.items():
    BASE[_k] = (_legend, "", "dead")

# The keycap legend says "Disabled"; what the key actually emits is the word
# HERROPERS, which is the point of the rule.
for _k in TRAINER_KEYS:
    BASE[_k] = ("Disabled", "", "trainer")

# The arrows are off the trainer list too: they move the mouse pointer.
BASE["left_arrow"] = ("◀ mouse", "", "system")
BASE["right_arrow"] = ("mouse ▶", "", "system")
BASE["__updown"] = ("mouse\n▲ ▼", "", "system")

# 1 is off the trainer list: it types "reply in <cursor's digit> sentences".
BASE["1"] = ("reply in\n_ sentences", "macro", "system")
BASE["2"] = ("explain what\nis meant by", "macro", "system")

# --- hold layers ------------------------------------------------------------

NUM = {
    "i": ("7", "", "punct"), "o": ("8", "", "punct"), "p": ("9", "", "punct"),
    "open_bracket": ("~", "", "punct"),
    "k": ("0", "", "punct"), "l": ("1", "", "punct"),
    "semicolon": ("2", "", "punct"), "quote": ("3", "", "punct"),
    "comma": ("4", "", "punct"), "period": ("5", "", "punct"),
    "slash": ("6", "", "punct"),
    "f": ("hold", "S", "layer"),
}

SYM_RIGHT = {
    "i": (";", "", "punct"), "o": ("&", "", "punct"),
    "p": ("$", "", "punct"), "open_bracket": ("#", "", "punct"),
    "k": ("[", "", "punct"), "l": ("]", "", "punct"),
    "semicolon": ("(", "", "punct"), "quote": (")", "", "punct"),
    "comma": (":", "", "punct"), "period": ("\\", "", "punct"),
    "slash": ("%", "", "punct"), "right_shift": ("?", "", "punct"),
    "a": ("hold", "N", "layer"),
}

SYM_LEFT = {
    "q": ("^", "", "punct"), "w": ("*", "", "punct"),
    "e": ("-", "", "punct"), "r": ("|", "", "punct"),
    "a": ("+", "", "punct"), "s": ("!", "", "punct"),
    "d": ("/", "", "punct"), "f": ("=", "", "punct"),
    "left_shift": ("`", "", "punct"), "z": ("<", "", "punct"),
    "x": (">", "", "punct"), "c": ("@", "", "punct"),
    "quote": ("hold", "I", "layer"),
}

NAV = {
    "e": ("⇥ tab", "", "punct"), "b": ("~", "", "punct"),
    "a": ("←", "", "punct"), "s": ("↑", "", "punct"),
    "d": ("↓", "", "punct"), "f": ("→", "", "punct"),
    "left_shift": ("←×5", "", "punct"), "z": ("↑×5", "", "punct"),
    "x": ("↓×5", "", "punct"), "c": ("→×5", "", "punct"),
    "k": ("hold", "H", "layer"),
}

# Cells a digit is worth on the step curve in tools/keypointer.json.
STEP_CELLS = {0: "½", 1: "1", 2: "2.1", 3: "3.8", 4: "6.3",
              5: "10", 6: "15.4", 7: "22.8", 8: "32.5", 9: "45"}
_STEP_DIGITS = [("k", 0), ("l", 1), ("semicolon", 2), ("quote", 3), ("comma", 4),
                ("period", 5), ("slash", 6), ("i", 7), ("o", 8), ("p", 9)]

STEP = {
    "a": ("◀", "hold", "layer"), "s": ("▲", "hold", "layer"),
    "d": ("▼", "hold", "layer"), "f": ("▶", "hold", "layer"),
    "left_shift": ("◀", "drag", "magic"), "z": ("▲", "drag", "magic"),
    "x": ("▼", "drag", "magic"), "c": ("▶", "drag", "magic"),
}
STEP.update({key: (str(digit),
                   STEP_CELLS[digit] + (" cell" if STEP_CELLS[digit] in ("½", "1") else " cells"),
                   "punct")
             for key, digit in _STEP_DIGITS})

SCROLL = {
    "k": ("◀", "scroll", "system"), "l": ("▼", "scroll", "system"),
    "semicolon": ("▲", "scroll", "system"), "quote": ("▶", "scroll", "system"),
    "comma": ("◀", "×3", "magic"), "period": ("▼", "×3", "magic"),
    "slash": ("▲", "×3", "magic"), "right_shift": ("▶", "×3", "magic"),
    "z": ("page\n▲", "", "punct"), "x": ("page\n▼", "", "punct"),
}

MODS = {
    "s": ("⌥", "left", "mod"),
    "d": ("⌘", "left", "mod"),
    "l": ("⌘", "left", "mod"),
    "semicolon": ("⌥", "left", "mod"),
    "spacebar": ("_", "", "punct"),
    "f": ("№", "numbers", "layer"),
    "k": ("→", "nav", "layer"),
    "a": ("&", "sym R", "layer"),
    "quote": ("#", "sym L", "layer"),
}

def _with_disabled(keys):
    """Every layer shows the disabled keys — they are dead on all of them."""
    merged = {k: ("Disabled", "", "trainer") for k in TRAINER_KEYS}
    merged.update(keys)
    return merged


LAYERS = [
    {
        "id": "base",
        "name": "Base",
        "sub": "Gallium v2, the row-staggered variant. Right hand sits one column right of QWERTY home.",
        "keys": BASE,
        "full": True,
    },
    {
        "id": "mods",
        "name": "Hold gate + home-row mods",
        "sub": "Press either gate to arm. Then hold a home-row key for its modifier or layer.",
        "keys": _with_disabled(MODS),
        "full": False,
    },
    {
        "id": "number",
        "name": "Number layer",
        "sub": "gate + hold S (physical F). Digits land on the right hand.",
        "keys": _with_disabled(NUM),
        "full": False,
    },
    {
        "id": "sym-left",
        "name": "Symbol layer — left",
        "sub": "gate + hold I (physical '). Math, brackets and shell glyphs.",
        "keys": _with_disabled(SYM_LEFT),
        "full": False,
    },
    {
        "id": "sym-right",
        "name": "Symbol layer — right",
        "sub": "gate + hold N (physical A). Pairs, punctuation and money.",
        "keys": _with_disabled(SYM_RIGHT),
        "full": False,
    },
    {
        "id": "step",
        "name": "Pointer steps",
        "sub": "Right gate. Hold a direction on N/R/T/S — or Z/X/Q/M to drag — then tap a digit for that many cells.",
        "keys": _with_disabled(STEP),
        "full": False,
        "gate": "right",
    },
    {
        "id": "scroll",
        "name": "Scroll",
        "sub": "Left gate. H/A/E/I scroll, P/,/./' do the same three times over, X/Q page.",
        "keys": _with_disabled(SCROLL),
        "full": False,
        "gate": "left",
    },
    {
        "id": "nav",
        "name": "Navigation layer",
        "sub": "gate + hold H (physical K). Bottom row jumps five at a time.",
        "keys": _with_disabled(NAV),
        "full": False,
    },
]
