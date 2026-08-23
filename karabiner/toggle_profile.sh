#!/bin/bash
CLI="/Library/Application Support/org.pqrs/Karabiner-Elements/bin/karabiner_cli"
CONFIG="$HOME/.config/karabiner/karabiner.json"

CURRENT=$(python3 -c "
import json
with open('$CONFIG') as f:
    d = json.load(f)
for p in d['profiles']:
    if p.get('selected', False):
        print(p['name'])
        break
")

if [ "$CURRENT" = "Default profile" ]; then
    "$CLI" --select-profile "Disabled"
else
    "$CLI" --select-profile "Default profile"
fi
