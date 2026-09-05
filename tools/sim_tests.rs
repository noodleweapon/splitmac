//! Behaviour tests for splitmac.kbd, run through kanata's own simulation
//! harness — no keyboard, no driver, no root.
//!
//!     sh tools/sim_test.sh
//!
//! Each case is (what it is, simulated input, expected output).  Input is
//! `d:` down, `u:` up, `t:` milliseconds, in *physical* key names.  Output is
//! what kanata would send to the OS.

use super::*;

static CFG: &str = include_str!("splitmac.kbd");

const HERROPERS: &str = "dn:LShift dn:H up:H up:LShift dn:LShift dn:E up:E up:LShift \
dn:LShift dn:R up:R up:LShift dn:LShift dn:R up:R up:LShift dn:LShift dn:O up:O up:LShift \
dn:LShift dn:P up:P up:LShift dn:LShift dn:E up:E up:LShift dn:LShift dn:R up:R up:LShift \
dn:LShift dn:S up:S up:LShift";

#[test]
fn splitmac() {
    let cases: &[(&str, &str, &str)] = &[
        // ---- base layer ------------------------------------------------
        ("q types b", "d:q t:20 u:q t:20", "dn:B up:B"),
        ("j types y", "d:j t:20 u:j t:20", "dn:Y up:Y"),
        ("/ types .", "d:/ t:20 u:/ t:20", "dn:Dot up:Dot"),
        ("left shift types z", "d:lsft t:20 u:lsft t:20", "dn:Z up:Z"),

        // ---- the magic key ---------------------------------------------
        ("r then magic gives l", "d:s t:20 u:s t:20 d:[ t:20 u:[ t:20",
         "dn:R up:R dn:L up:L"),
        ("magic chains: r [ [ [ [ = rlmcs",
         "d:s t:10 u:s t:10 d:[ t:10 u:[ t:10 d:[ t:10 u:[ t:10 d:[ t:10 u:[ t:10 d:[ t:10 u:[ t:10",
         "dn:R up:R dn:L up:L dn:M up:M dn:C up:C dn:S up:S"),
        ("magic after a space does nothing", "d:spc t:20 u:spc t:20 d:[ t:20 u:[ t:20",
         "dn:Space up:Space"),

        // ---- the trainer -----------------------------------------------
        ("the number row is trapped", "d:1 t:200 u:1 t:20", HERROPERS),

        // ---- gate, mods, layers ----------------------------------------
        ("gate + hold F, then I = 7",
         "d:caps t:20 d:f t:250 d:i t:20 u:i t:20 u:f t:20 u:caps t:20", "dn:Kb7 up:Kb7"),
        ("gate + tap F = s", "d:caps t:20 d:f t:50 u:f t:20 u:caps t:20", "dn:S up:S"),
        ("number layer keeps the left hand's Command",
         "d:caps t:20 d:f t:250 d:d t:250 d:l t:20 u:l t:20 u:d t:20 u:f t:20 u:caps t:20",
         "dn:LGui dn:Kb1 up:Kb1 up:LGui"),
        ("gate + hold D = Command",
         "d:caps t:20 d:d t:250 d:s t:20 u:s t:20 u:d t:20 u:caps t:20",
         "dn:LGui dn:R up:R up:LGui"),
        ("gate + tap D = t", "d:caps t:20 d:d t:50 u:d t:20 u:caps t:20", "dn:T up:T"),
        ("nav layer: N = left",
         "d:caps t:20 d:k t:250 d:a t:20 u:a t:20 u:k t:20 u:caps t:20", "dn:Left up:Left"),
        ("nav layer: shift = five lefts",
         "d:caps t:20 d:k t:250 d:lsft t:250 u:lsft t:20 u:k t:20 u:caps t:20",
         "dn:Left up:Left dn:Left up:Left dn:Left up:Left dn:Left up:Left dn:Left up:Left"),
        ("left symbol layer: Z = <",
         "d:caps t:20 d:, t:250 d:z t:20 u:z t:20 u:, t:20 u:caps t:20",
         "dn:LShift dn:Comma up:LShift up:Comma"),
        ("right symbol layer: H = [",
         "d:caps t:20 d:c t:250 d:k t:20 u:k t:20 u:c t:20 u:caps t:20",
         "dn:LBracket up:LBracket"),

        // ---- thumbs and the shift overrides ----------------------------
        ("tap left Command = return", "d:lmet t:50 u:lmet t:20", "dn:Enter up:Enter"),
        ("hold left Command = shift", "d:lmet t:250 d:q t:20 u:q t:20 u:lmet t:20",
         "dn:LShift dn:B up:B up:LShift"),
        ("shift + / = esc", "d:lmet t:250 d:/ t:20 u:/ t:20 u:lmet t:20",
         "dn:LShift up:LShift dn:Escape up:Escape dn:LShift up:LShift"),
        ("shift + . = option-c", "d:lmet t:250 d:. t:20 u:. t:20 u:lmet t:20",
         "dn:LShift up:LShift dn:LAlt dn:C up:LAlt up:C dn:LShift up:LShift"),
        ("tap right Option = tab", "d:ralt t:50 u:ralt t:20", "dn:Tab up:Tab"),
        ("right Command = delete", "d:rmet t:20 u:rmet t:20", "dn:BSpace up:BSpace"),
        ("left Option = Control", "d:lalt t:20 u:lalt t:20", "dn:LCtrl up:LCtrl"),

        // ---- option shortcuts and the swallowed Command-M ---------------
        ("option + A = AeroSpace focus E",
         "d:caps t:20 d:s t:250 d:l t:20 u:l t:20 u:s t:20 u:caps t:20",
         "dn:LAlt dn:E up:E up:LAlt"),
        ("option + M = Control-C",
         "d:caps t:20 d:s t:250 d:c t:20 u:c t:20 u:s t:20 u:caps t:20",
         "dn:LAlt up:LAlt dn:LCtrl dn:C up:LCtrl up:C dn:LAlt up:LAlt"),
        ("Command + M is swallowed, not a minimised window",
         "d:caps t:20 d:d t:250 d:c t:20 u:c t:20 u:d t:20 u:caps t:20", "dn:LGui up:LGui"),

        // ---- the off switch ---------------------------------------------
        ("F6 turns the keymap off", "d:f6 t:20 u:f6 t:20 d:q t:20 u:q t:20", "dn:Q up:Q"),
        ("F6 again turns it back on",
         "d:f6 t:20 u:f6 t:20 d:f6 t:20 u:f6 t:20 d:q t:20 u:q t:20", "dn:B up:B"),
    ];

    let mut failures = vec![];
    for (name, sim, want) in cases {
        let got = simulate(CFG, sim).to_ascii().no_time();
        if got != *want {
            failures.push(format!("{name}\n     want: {want}\n     got:  {got}"));
        }
    }
    assert!(failures.is_empty(), "\n  {}\n", failures.join("\n  "));
    println!("{} cases pass", cases.len());
}
