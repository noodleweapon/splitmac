// splitmac for the ZSA Voyager.
//
// This is the QMK version of the splitmac Karabiner-Elements profile in
// ../../../../../../karabiner/karabiner.json. Every rule in that profile is
// reproduced with the same first-matching-rule precedence Karabiner applies,
// except for the ones that need keys the Voyager does not have (F3/F4/F6) and
// the Option-shortcut rules that the layout remap already consumes on the
// laptop. See README.md for the full table.
//
// Terminology:
//   "physical X"  = the key in the position of X on a standard QWERTY board,
//                   which is how the Karabiner rules are written. On the laptop
//                   the right hand rests one column to the right, and the left
//                   bottom row one column to the left, of where they sit on the
//                   Voyager; the keymap below already undoes both offsets.
//   "gate"        = a hold-only thumb key. Left gate (physical spacebar) arms
//                   the left-hand specials, right gate (physical right ⌘) arms
//                   the right-hand specials. Tapping a gate does nothing.

#include QMK_KEYBOARD_H

// LAYOUT_LR: the Voyager's LAYOUT macro with the two halves written as two
// blocks, left hand first, so each layer reads like the physical board.
// clang-format off
#define LAYOUT_LR(                                     \
    k00, k01, k02, k03, k04, k05,                      \
    k10, k11, k12, k13, k14, k15,                      \
    k20, k21, k22, k23, k24, k25,                      \
    k30, k31, k32, k33, k34, k35,                      \
                             k40, k41,                 \
                                                       \
                         k50, k51, k52, k53, k54, k55, \
                         k60, k61, k62, k63, k64, k65, \
                         k70, k71, k72, k73, k74, k75, \
                         k80, k81, k82, k83, k84, k85, \
                    k90, k91)                          \
    LAYOUT(k00, k01, k02, k03, k04, k05,   k50, k51, k52, k53, k54, k55, \
           k10, k11, k12, k13, k14, k15,   k60, k61, k62, k63, k64, k65, \
           k20, k21, k22, k23, k24, k25,   k70, k71, k72, k73, k74, k75, \
           k30, k31, k32, k33, k34, k35,   k80, k81, k82, k83, k84, k85, \
                               k40, k41,   k90, k91)
// clang-format on

enum layers {
  BASE,
  RSYM,   // Hold physical C (types m) with left gate: right-hand symbols.
  LSYM,   // Hold physical , (types p) with right gate: left-hand symbols.
  NUM,    // Hold physical F (types s) with left gate: right-hand numbers.
  ARROW,  // Hold physical K (types h) with right gate: left-hand arrows.
  PLAIN,  // Plain QWERTY, toggled with both top-corner keys (was F6).
};

enum custom_keycodes {
  TRAIN = SAFE_RANGE,  // Bad-habit trainer: types HERROPERS.
  TRN_L,               // Same as TRAIN, but distinct so it can be in a combo.
  TRN_R,               // Same as TRAIN, but distinct so it can be in a combo.
  LGATE,               // Left gate (physical spacebar). Hold only.
  RGATE,               // Right gate (physical right ⌘). Hold only.
  // Gated home-row mods: hold with gate = modifier, otherwise = letter.
  GM_A,     // n   | left gate: Left Shift (no tap)
  GM_S,     // r   | left gate: Left Option, tap r
  GM_D,     // t   | left gate: Left Command, tap t
  GM_G,     // g   | left gate: Left Control, tap g
  GM_J,     // y   | right gate: Left Control, tap y
  GM_L,     // a   | right gate: Left Command, tap a
  GM_SCLN,  // e   | right gate: Left Option, tap e
  GM_QUOT,  // i   | right gate: Right Shift (no tap)
  // Gated layer keys: hold with gate = layer, otherwise = letter.
  GL_F,     // s   | left gate: NUM, tap s
  GL_C,     // m   | left gate: RSYM, tap m   (also ⌘+key = nothing, ⌥+key = ⌃C)
  GL_K,     // h   | right gate: ARROW, tap h
  GL_COMM,  // p   | right gate: LSYM, tap p
  // Shift-overridden keys.
  DOT_ESC,  // .   | with Shift: Escape        (physical [)
  COMM_AC,  // ,   | with Shift: Option+C      (physical .)
  // Arrow layer: five arrow taps at once.
  AR5_L,
  AR5_U,
  AR5_D,
  AR5_R,
};

// clang-format off
const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {
  [BASE] = LAYOUT_LR(
    TRN_L  , TRAIN  , TRAIN  , TRAIN  , TRAIN  , TRAIN  ,
    TRAIN  , KC_B   , KC_L   , KC_D   , KC_C   , KC_V   ,
    TRAIN  , GM_A   , GM_S   , GM_D   , GL_F   , GM_G   ,
    TRAIN  , KC_Z   , KC_X   , KC_Q   , GL_C   , KC_W   ,
                                                 KC_SPC , LGATE  ,

                      TRAIN  , TRAIN  , TRAIN  , TRAIN  , TRAIN  , TRN_R  ,
                      KC_J   , KC_F   , KC_O   , KC_U   , DOT_ESC, TRAIN  ,
                      GM_J   , GL_K   , GM_L   , GM_SCLN, GM_QUOT, TRAIN  ,
                      KC_K   , GL_COMM, COMM_AC, KC_UNDS, KC_QUOT, TRAIN  ,
             RGATE  , KC_BSPC
  ),

  [RSYM] = LAYOUT_LR(  // Hold m-key (physical C) with left gate.
    _______, _______, _______, _______, _______, _______,
    _______, _______, _______, _______, _______, _______,
    _______, _______, _______, _______, _______, _______,
    _______, _______, _______, _______, _______, _______,
                                                 _______, _______,

                      _______, _______, _______, _______, _______, _______,
                      _______, KC_SCLN, KC_AMPR, KC_DLR , KC_HASH, _______,
                      _______, KC_LBRC, KC_RBRC, KC_LPRN, KC_RPRN, _______,
                      _______, KC_COLN, KC_BSLS, KC_PERC, KC_QUES, _______,
             _______, _______
  ),

  [LSYM] = LAYOUT_LR(  // Hold p-key (physical ,) with right gate.
    _______, _______, _______, _______, _______, _______,
    _______, KC_CIRC, KC_ASTR, KC_MINS, KC_PIPE, _______,
    _______, KC_PLUS, KC_EXLM, KC_SLSH, KC_EQL , _______,
    _______, KC_GRV , KC_LABK, KC_RABK, KC_AT  , _______,
                                                 _______, _______,

                      _______, _______, _______, _______, _______, _______,
                      _______, _______, _______, _______, _______, _______,
                      _______, _______, _______, _______, _______, _______,
                      _______, _______, _______, _______, _______, _______,
             _______, _______
  ),

  [NUM] = LAYOUT_LR(  // Hold s-key (physical F) with left gate.
    _______, _______, _______, _______, _______, _______,
    _______, _______, _______, _______, _______, _______,
    _______, _______, _______, _______, _______, _______,
    _______, _______, _______, _______, _______, _______,
                                                 _______, _______,

                      _______, _______, _______, _______, _______, _______,
                      _______, KC_7   , KC_8   , KC_9   , _______, _______,
                      _______, KC_0   , KC_1   , KC_2   , KC_3   , _______,
                      _______, KC_4   , KC_5   , KC_6   , KC_TILD, _______,
             _______, _______
  ),

  [ARROW] = LAYOUT_LR(  // Hold h-key (physical K) with right gate.
    _______, _______, _______, _______, _______, _______,
    _______, KC_LEFT, KC_UP  , KC_DOWN, KC_RGHT, _______,
    _______, MS_BTN1, KC_TAB , KC_ESC , KC_ENT , _______,
    _______, AR5_L  , AR5_U  , AR5_D  , AR5_R  , _______,
                                                 _______, _______,

                      _______, _______, _______, _______, _______, _______,
                      _______, _______, _______, _______, _______, _______,
                      _______, _______, _______, _______, _______, _______,
                      _______, _______, _______, _______, _______, _______,
             _______, _______
  ),

  [PLAIN] = LAYOUT_LR(  // Plain QWERTY (Karabiner "Disabled" profile).
    KC_ESC , KC_1   , KC_2   , KC_3   , KC_4   , KC_5   ,
    KC_TAB , KC_Q   , KC_W   , KC_E   , KC_R   , KC_T   ,
    KC_LCTL, KC_A   , KC_S   , KC_D   , KC_F   , KC_G   ,
    KC_LSFT, KC_Z   , KC_X   , KC_C   , KC_V   , KC_B   ,
                                                 KC_LGUI, KC_SPC ,

                      KC_6   , KC_7   , KC_8   , KC_9   , KC_0   , KC_MINS,
                      KC_Y   , KC_U   , KC_I   , KC_O   , KC_P   , KC_BSLS,
                      KC_H   , KC_J   , KC_K   , KC_L   , KC_SCLN, KC_QUOT,
                      KC_N   , KC_M   , KC_COMM, KC_DOT , KC_SLSH, KC_RSFT,
             KC_ENT , KC_BSPC
  ),
};
// clang-format on

// Both top-corner keys together toggle plain QWERTY (replaces Karabiner's F6).
const uint16_t PROGMEM plain_combo[] = {TRN_L, TRN_R, COMBO_END};
combo_t key_combos[] = {
    COMBO(plain_combo, TG(PLAIN)),
};

///////////////////////////////////////////////////////////////////////////////
// Gates and gated keys.
///////////////////////////////////////////////////////////////////////////////

enum { GATE_L = 1 << 0, GATE_R = 1 << 1 };
#define NO_LAYER 0xFF
#define SPECIAL_LAYERS \
  ((1UL << RSYM) | (1UL << LSYM) | (1UL << NUM) | (1UL << ARROW))

typedef struct {
  uint16_t keycode;  // Custom keycode in the keymap.
  uint16_t plain;    // Letter typed when the key is not armed by its gate.
  uint16_t alone;    // Letter typed when armed and tapped alone (KC_NO: none).
  uint8_t gate;      // Which gate arms this key.
  uint8_t mod;       // Modifier held while armed (KC_NO for layer keys).
  uint8_t layer;     // Layer held while armed (NO_LAYER for modifier keys).
} gated_key_t;

static const gated_key_t gated_keys[] = {
    // Left hand, armed by the left gate (physical spacebar).
    {GM_A, KC_N, KC_NO, GATE_L, KC_LSFT, NO_LAYER},
    {GM_S, KC_R, KC_R, GATE_L, KC_LALT, NO_LAYER},
    {GM_D, KC_T, KC_T, GATE_L, KC_LGUI, NO_LAYER},
    {GL_F, KC_S, KC_S, GATE_L, KC_NO, NUM},
    {GM_G, KC_G, KC_G, GATE_L, KC_LCTL, NO_LAYER},
    {GL_C, KC_M, KC_M, GATE_L, KC_NO, RSYM},
    // Right hand, armed by the right gate (physical right ⌘).
    {GM_J, KC_Y, KC_Y, GATE_R, KC_LCTL, NO_LAYER},
    {GL_K, KC_H, KC_H, GATE_R, KC_NO, ARROW},
    {GM_L, KC_A, KC_A, GATE_R, KC_LGUI, NO_LAYER},
    {GM_SCLN, KC_E, KC_E, GATE_R, KC_LALT, NO_LAYER},
    {GM_QUOT, KC_I, KC_NO, GATE_R, KC_RSFT, NO_LAYER},
    {GL_COMM, KC_P, KC_P, GATE_R, KC_NO, LSYM},
};
#define NUM_GATED_KEYS (sizeof(gated_keys) / sizeof(*gated_keys))

enum { MODE_NONE, MODE_PLAIN, MODE_SPECIAL, MODE_SWALLOWED };

typedef struct {
  uint8_t mode;
  uint16_t timer;
  uint16_t press_id;
} gated_state_t;

static gated_state_t gated_state[NUM_GATED_KEYS];
static uint8_t gates = 0;
// Incremented on every key press. Used to detect "pressed alone", like
// Karabiner's to_if_alone: no other key may be pressed in between.
static uint16_t press_counter = 0;

// Taps `keycode` with the current `mask` modifiers temporarily removed. This
// is how Karabiner handles `from.modifiers.mandatory`: the mandatory modifier
// is consumed and does not appear in the output.
static void tap_without_mods(uint16_t keycode, uint8_t mask) {
  const uint8_t saved = get_mods() & mask;
  del_mods(saved);
  send_keyboard_report();
  tap_code16(keycode);
  add_mods(saved);
  send_keyboard_report();
}

static bool process_gated_key(uint16_t keycode, keyrecord_t* record) {
  for (uint8_t i = 0; i < NUM_GATED_KEYS; ++i) {
    const gated_key_t* k = &gated_keys[i];
    if (k->keycode != keycode) {
      continue;
    }
    gated_state_t* st = &gated_state[i];

    if (record->event.pressed) {
      // Karabiner rules "Disable Command-C on remapped M key" and "Map Alt+C
      // to Control+C" come before the layer rule, so they win on this key.
      if (keycode == GL_C) {
        const uint8_t mods = get_mods();
        if (mods != 0 && (mods & ~MOD_MASK_GUI) == 0) {
          st->mode = MODE_SWALLOWED;  // ⌘ + m-key => nothing.
          return false;
        }
        if (mods != 0 && (mods & ~MOD_MASK_ALT) == 0) {
          tap_without_mods(C(KC_C), MOD_MASK_ALT);  // ⌥ + m-key => ⌃C.
          st->mode = MODE_SWALLOWED;
          return false;
        }
      }

      bool armed = (gates & k->gate) != 0;
      // A layer key only activates when no other special layer is active.
      if (k->layer != NO_LAYER && (layer_state & SPECIAL_LAYERS) != 0) {
        armed = false;
      }

      if (armed) {
        st->mode = MODE_SPECIAL;
        st->timer = timer_read();
        st->press_id = press_counter;
        if (k->layer != NO_LAYER) {
          layer_on(k->layer);
        } else {
          register_code(k->mod);
        }
      } else {
        st->mode = MODE_PLAIN;
        register_code(k->plain);
      }
    } else {
      switch (st->mode) {
        case MODE_PLAIN:
          unregister_code(k->plain);
          break;
        case MODE_SPECIAL:
          if (k->layer != NO_LAYER) {
            layer_off(k->layer);
          } else {
            unregister_code(k->mod);
          }
          if (k->alone != KC_NO && st->press_id == press_counter &&
              timer_elapsed(st->timer) < ALONE_TIMEOUT_MS) {
            tap_code(k->alone);
          }
          break;
        default:
          break;
      }
      st->mode = MODE_NONE;
    }
    return false;
  }
  return true;
}

///////////////////////////////////////////////////////////////////////////////
// Other custom keys.
///////////////////////////////////////////////////////////////////////////////

static void tap_arrow_5x(uint16_t arrow) {
  for (uint8_t i = 0; i < 5; ++i) {
    tap_code_delay(arrow, ARROW5_DELAY_MS);
  }
}

// Shift-overridden key: without Shift it is `normal` (held like a regular
// key); with Shift held, Shift is consumed and `shifted` is tapped instead.
static bool process_shift_override(keyrecord_t* record, uint16_t normal,
                                   uint16_t shifted, bool* used_override) {
  if (record->event.pressed) {
    if ((get_mods() & MOD_MASK_SHIFT) != 0) {
      *used_override = true;
      tap_without_mods(shifted, MOD_MASK_SHIFT);
    } else {
      *used_override = false;
      register_code(normal);
    }
  } else if (!*used_override) {
    unregister_code(normal);
  }
  return false;
}

bool process_record_user(uint16_t keycode, keyrecord_t* record) {
  static bool dot_esc_override = false;
  static bool comm_ac_override = false;

  if (record->event.pressed) {
    ++press_counter;
  }

  if (!process_gated_key(keycode, record)) {
    return false;
  }

  switch (keycode) {
    case LGATE:
      gates = record->event.pressed ? (gates | GATE_L) : (gates & ~GATE_L);
      return false;
    case RGATE:
      gates = record->event.pressed ? (gates | GATE_R) : (gates & ~GATE_R);
      return false;

    case TRAIN:
    case TRN_L:
    case TRN_R:
      if (record->event.pressed) {
        SEND_STRING("HERROPERS");
      }
      return false;

    case DOT_ESC:
      return process_shift_override(record, KC_DOT, KC_ESC, &dot_esc_override);
    case COMM_AC:
      return process_shift_override(record, KC_COMM, A(KC_C), &comm_ac_override);

    case AR5_L:
      if (record->event.pressed) tap_arrow_5x(KC_LEFT);
      return false;
    case AR5_U:
      if (record->event.pressed) tap_arrow_5x(KC_UP);
      return false;
    case AR5_D:
      if (record->event.pressed) tap_arrow_5x(KC_DOWN);
      return false;
    case AR5_R:
      if (record->event.pressed) tap_arrow_5x(KC_RGHT);
      return false;
  }
  return true;
}

///////////////////////////////////////////////////////////////////////////////
// RGB: show which mode the board is in.
///////////////////////////////////////////////////////////////////////////////

#ifdef RGB_MATRIX_ENABLE
bool rgb_matrix_indicators_advanced_user(uint8_t led_min, uint8_t led_max) {
  if (layer_state_is(PLAIN)) {
    for (uint8_t i = led_min; i < led_max; ++i) {
      rgb_matrix_set_color(i, 40, 40, 40);  // Dim white = plain QWERTY.
    }
  }
  return false;
}
#endif  // RGB_MATRIX_ENABLE
