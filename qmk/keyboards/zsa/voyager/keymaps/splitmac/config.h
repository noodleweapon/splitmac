#pragma once

// Mirrors Karabiner's basic.to_if_alone_timeout_milliseconds.
#define ALONE_TIMEOUT_MS 200

// Slow macros down slightly so apps don't drop or reorder fast key events.
#define TAP_CODE_DELAY 5

// Delay between the 5 repeated arrow taps in the arrow layer (Karabiner used
// hold_down_milliseconds = 30 between them).
#define ARROW5_DELAY_MS 15

// The PLAIN-QWERTY toggle combo (both top-corner keys) is resolved against
// layer 0 so that it also works for toggling back from the PLAIN layer.
#define COMBO_ONLY_FROM_LAYER 0
#define COMBO_TERM 60
