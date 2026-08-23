"""Single source of truth for the godlike-keymap layout.

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
# system   app launchers, screenshots, profile toggle
# dead     untouched pass-through key

TRAINER_KEYS = [
    "grave_accent_and_tilde", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
    "hyphen", "equal_sign", "delete_or_backspace", "tab", "close_bracket",
    "backslash", "escape", "left_control", "y", "h", "b",
    "left_arrow", "right_arrow", "__updown",
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
    "open_bracket": ("-", "", "punct"),

    "a": ("N", "", "alpha"),
    "s": ("R", "⌥ opt", "mod"),
    "d": ("T", "⌘ cmd", "mod"),
    "f": ("S", "№ num", "layer"),
    "g": ("G", "", "alpha"),
    "j": ("Y", "", "alpha"),
    "k": ("H", "→ nav", "layer"),
    "l": ("A", "⌘ cmd", "mod"),
    "semicolon": ("E", "⌥ opt", "mod"),
    "quote": ("I", "", "alpha"),

    "z": ("X", "", "alpha"),   "x": ("Q", "", "alpha"),
    "c": ("M", "& sym", "layer"),
    "v": ("W", "", "alpha"),
    "n": ("Z", "", "alpha"),   "m": ("K", "", "alpha"),
    "comma": ("P", "# sym", "layer"),
    "period": (",", "⇧ ⌥C", "alpha"),
    "slash": (".", "⇧ esc", "alpha"),

    # gates
    "caps_lock": ("hold =\nlayers", "tap: nothing", "gate"),
    "return_or_enter": ("hold =\nlayers", "tap: nothing", "gate"),

    # modifiers & thumbs
    "left_shift": ("'", "", "punct"),
    "right_shift": (";", "", "punct"),
    "left_option": ("control", "", "mod"),
    "left_command": ("⇧ shift", "tap: return", "mod"),
    "right_command": ("⌫ delete", "", "mod"),
    "right_option": ("⇧ shift", "tap: tab", "mod"),
    "spacebar": ("space", "", "dead"),
    "fn": ("fn", "", "dead"),
    "touch_id": ("⏻", "", "dead"),

    # function row
    "f3": ("⌘⇧⌃ 4", "clip shot", "system"),
    "f4": ("Raycast", "", "system"),
    "f5": ("Screen\nprompt", "", "system"),
    "f6": ("toggle\nkeymap", "on / off", "system"),
}

_MEDIA = {
    "f1": "☀−", "f2": "☀+", "f7": "⏮", "f8": "⏯",
    "f9": "⏭", "f10": "mute", "f11": "vol −", "f12": "vol +",
}
for _k, _legend in _MEDIA.items():
    BASE[_k] = (_legend, "", "dead")

for _k in TRAINER_KEYS:
    BASE[_k] = ("HERRO\nPERS", "", "trainer")

# --- hold layers ------------------------------------------------------------

NUM = {
    "i": ("7", "", "punct"), "o": ("8", "", "punct"), "p": ("9", "", "punct"),
    "k": ("0", "", "punct"), "l": ("1", "", "punct"),
    "semicolon": ("2", "", "punct"), "quote": ("3", "", "punct"),
    "m": ("4", "", "punct"), "comma": ("5", "", "punct"), "period": ("6", "", "punct"),
    "f": ("hold", "S", "layer"),
}

SYM_RIGHT = {
    "i": (";", "", "punct"), "o": ("&", "", "punct"),
    "p": ("$", "", "punct"), "open_bracket": ("#", "", "punct"),
    "k": ("[", "", "punct"), "l": ("]", "", "punct"),
    "semicolon": ("(", "", "punct"), "quote": (")", "", "punct"),
    "m": (":", "", "punct"), "comma": ("\\", "", "punct"),
    "period": ("%", "", "punct"), "slash": ("?", "", "punct"),
    "c": ("hold", "M", "layer"),
}

SYM_LEFT = {
    "q": ("^", "", "punct"), "w": ("<", "", "punct"),
    "e": (">", "", "punct"), "r": ("|", "", "punct"),
    "a": ("+", "", "punct"), "s": ("!", "", "punct"),
    "d": ("/", "", "punct"), "f": ("=", "", "punct"),
    "z": ("`", "", "punct"), "x": ("~", "", "punct"),
    "c": ("*", "", "punct"), "v": ("@", "", "punct"),
    "comma": ("hold", "P", "layer"),
}

NAV = {
    "a": ("←", "", "punct"), "s": ("↑", "", "punct"),
    "d": ("↓", "", "punct"), "f": ("→", "", "punct"),
    "z": ("←×5", "", "punct"), "x": ("↑×5", "", "punct"),
    "c": ("↓×5", "", "punct"), "v": ("→×5", "", "punct"),
    "k": ("hold", "H", "layer"),
}

MODS = {
    "s": ("⌥", "left", "mod"),
    "d": ("⌘", "left", "mod"),
    "l": ("⌘", "right", "mod"),
    "semicolon": ("⌥", "right", "mod"),
    "f": ("№", "numbers", "layer"),
    "k": ("→", "nav", "layer"),
    "c": ("&", "sym R", "layer"),
    "comma": ("#", "sym L", "layer"),
    "caps_lock": ("hold", "arms all of it", "gate"),
    "return_or_enter": ("hold", "arms all of it", "gate"),
}

LAYERS = [
    {
        "id": "base",
        "name": "Base",
        "sub": "Hands‑Down‑family alphas. Right hand sits one column right of QWERTY home.",
        "keys": BASE,
        "full": True,
    },
    {
        "id": "mods",
        "name": "Hold gate + home-row mods",
        "sub": "Hold caps or return to arm. Then hold a home-row key for its modifier or layer.",
        "keys": MODS,
        "full": False,
    },
    {
        "id": "number",
        "name": "Number layer",
        "sub": "caps/return + hold S (physical F). Digits land on the right hand.",
        "keys": NUM,
        "full": False,
    },
    {
        "id": "sym-left",
        "name": "Symbol layer — left",
        "sub": "caps/return + hold P (physical comma). Math, brackets and shell glyphs.",
        "keys": SYM_LEFT,
        "full": False,
    },
    {
        "id": "sym-right",
        "name": "Symbol layer — right",
        "sub": "caps/return + hold M (physical C). Pairs, punctuation and money.",
        "keys": SYM_RIGHT,
        "full": False,
    },
    {
        "id": "nav",
        "name": "Navigation layer",
        "sub": "caps/return + hold H (physical K). Bottom row jumps five at a time.",
        "keys": NAV,
        "full": False,
    },
]
