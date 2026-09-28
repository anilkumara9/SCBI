#!/usr/bin/env bash
# reproduce_exp105.sh — one-command reproduction of the EXP105 Tier-0 + battery
# numbers from the committed research artifacts, using the kit's own machinery.
#
# Path A (no model needed — default): adapts the committed EXP105 Tier-0
# per-item records to the kit format and re-runs the kit battery on them.
# The reproduced worksheet must match reference/battery_worksheet.json:
#   KILL at step 9, dM_T=+0.2381, dM_R=0.0000, T-vs-R p=0.0625, O=0.571.
#
# Path B (model needed): python tier0.py --model-id <HF id> --out /tmp/t0.json
#   then  python battery.py --records /tmp/t0.json --out /tmp/batt.json
#   to run the full pipeline on your own model.
set -euo pipefail
KIT="$(cd "$(dirname "$0")" && pwd)"
cd "$KIT"

echo "=== [1/4] unit tests (must all PASS before bench contact) ==="
python3 tests/test_degeneracy.py

echo "=== [2/4] adapt committed EXP105 Tier-0 records to kit format ==="
python3 reference/adapt_exp105.py

echo "=== [3/4] re-run kit battery on EXP105 logits ==="
python3 battery.py --records reference/exp105_tier0_kitformat.json \
    --out reference/battery_reproduced.json

echo "=== [4/4] compare against the published EXP105 battery worksheet ==="
python3 - <<'EOF'
import json, sys
ref = json.load(open("reference/battery_worksheet.json"))
rep = json.load(open("reference/battery_reproduced.json"))["worksheet"]
checks = [
    ("verdict", ref["decision"]["verdict"], rep["decision"]["verdict"]),
    ("step", ref["decision"]["step"], rep["decision"]["step"]),
    ("n_pop", ref["n_pop"], rep["n_pop"]),
    ("dM_T", ref["dM_primary_tier0pop"]["T"], rep["dM_primary_tier0pop"]["T"]),
    ("dM_R", ref["dM_primary_tier0pop"]["R"], rep["dM_primary_tier0pop"]["R"]),
    ("p_TvsR", ref["contrasts"]["T-vs-R"]["p"], rep["contrasts"]["T-vs-R"]["p"]),
    ("O", ref["overlap_O"], rep["decision"]["evidence"]["O"]),
]
ok = True
for name, a, b in checks:
    same = (a == b) if not isinstance(a, float) else abs(a - b) < 1e-9
    print(("MATCH " if same else "DIFF  "), name, "ref=%s rep=%s" % (a, b))
    ok = ok and same
print("\nREPRODUCTION " + ("EXACT ✔" if ok else "FAILED ✘"))
sys.exit(0 if ok else 1)
EOF
