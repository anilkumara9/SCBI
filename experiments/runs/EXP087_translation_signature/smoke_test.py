#!/usr/bin/env python3
"""EXP087 CPU smoke test — fast pre-flight checks (no weights, no GPU).

Verifies: imports, pins, benchmark construction, the refusal gate on the
--execute path, and a tiny synthetic analyze run. For the full suite, run
test_exp087.py and mock_harness.py.
"""

import json
import os
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import exp087_benchmark as B
import exp087_guards as G

HERE = os.path.dirname(os.path.abspath(__file__))
SCBI = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
CHECKS = []


def check(name, cond, detail=""):
    CHECKS.append(name)
    print(("PASS " if cond else "FAIL ") + name + (f" ({detail})" if detail and not cond else ""))
    if not cond:
        raise SystemExit(f"SMOKE FAILED: {name} {detail}")


def main():
    check("imports", True)
    check("pins", G.MODEL_ID == "EleutherAI/pythia-410m" and G.N_ITEMS == 60)
    check("crash_guard", G.crash_guard(SCBI) is True)
    items = B.build_items()
    check("benchmark_60", len(items) == 60)
    check("O_60", len(B.order_O()) == 60)
    check("envelope", G.ENVELOPE_LO == 0.649 and G.ENVELOPE_HI == 0.849)

    # --execute without flags must refuse with exit 2 (no weights touched).
    r = subprocess.run([sys.executable, os.path.join(HERE, "run_exp087.py"),
                        "--execute"], capture_output=True, text=True, timeout=60)
    check("execute_refuses", r.returncode == 2, f"rc={r.returncode}")

    # --analyze on a tiny synthetic log (2 items would fail the N=60 gate;
    # here we only check the CLI wiring rejects bad input loudly).
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump({"records": []}, f)
        bad = f.name
    r = subprocess.run([sys.executable, os.path.join(HERE, "run_exp087.py"),
                        "--analyze", "--per-item", bad],
                       capture_output=True, text=True, timeout=60)
    check("analyze_rejects_bad", r.returncode != 0, f"rc={r.returncode}")
    os.unlink(bad)

    # mock mode runs the harness (fast subset is fine; full harness in CI).
    print(f"\nSMOKE: {len(CHECKS)}/{len(CHECKS)} pass")


if __name__ == "__main__":
    main()
