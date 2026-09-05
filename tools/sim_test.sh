#!/bin/sh
# Run tools/sim_tests.rs against kanata's simulation harness.  Needs cargo.
#
# The harness is test-only code inside kanata, so this clones kanata, drops the
# test and the config in beside its own sim tests, and runs it.
set -e

here=$(cd "$(dirname "$0")/.." && pwd)
src=${KANATA_SRC:-/tmp/splitmac-kanata-src}

[ -d "$src" ] || git clone --depth 1 https://github.com/jtroo/kanata "$src"

tests=$src/src/tests/sim_tests
cp "$here/tools/sim_tests.rs" "$tests/splitmac_tests.rs"
cp "$here/kanata/splitmac.kbd" "$tests/splitmac.kbd"
grep -q splitmac_tests "$tests/mod.rs" ||
	printf 'mod splitmac_tests;\n' >>"$tests/mod.rs"

cd "$src"
cargo test --features simulated_output splitmac -- --nocapture
