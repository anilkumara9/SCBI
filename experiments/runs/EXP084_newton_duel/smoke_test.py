#!/usr/bin/env python3
"""EXP084 startup smoke test (Law #14 gate at bundle stage).

Budget: ≤12 passes by precedent (§6) — this smoke test uses ZERO model
passes (it never touches weights or the GPU node). It verifies:
  1. All bundle modules import cleanly.
  2. The signed pins are present (KAPPA_FLOOR, seeds, budgets, model hash).
  3. The exact Spearman null tables exist for n=12..19 (needed by the
     dose-response conjunct) and sum to n!. Tables n=20..24 are NOT
     precomputed (GPU-node build artifacts; see BUILD_NOTES §1).
  4. The runner refuses execution without CEO GPU clearance.
  5. The C table generator source is present (reproducibility).
  6. The mock-model end-to-end harness (mock_harness.py): the entire
     run_full_loop orchestration — all five arms, guard logic, pass-budget
     accounting, tie/table loud halts, verdict adjudication — on synthetic
     activations, zero model passes, zero torch.

Run: python3 smoke_test.py — exit 0 iff all smoke checks pass.
"""

import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

ok = True


def smoke(name, cond, detail=""):
    global ok
    print(("SMOKE-OK  " if cond else "SMOKE-FAIL ") + name
          + ("" if cond else f" :: {detail}"))
    ok = ok and cond


# 1. imports
try:
    import exp084_guards as G
    import exp084_rng as R
    import exp084_statistics as S
    import exp084_spearman as SP
    import run_exp084 as RUN
    smoke("imports", True)
except Exception as e:
    smoke("imports", False, str(e))
    print("SMOKE RESULT: FAIL")
    sys.exit(1)

# 2. signed pins
smoke("pin KAPPA_FLOOR=1e-6", G.KAPPA_FLOOR == 1e-6)
smoke("pin MIN_DEFINED_ITEMS=12", G.MIN_DEFINED_ITEMS == 12)
smoke("pin MASTER_SEED=20260924", R.MASTER_SEED == 20260924)
smoke("pin FWD_BUDGET=240", RUN.FWD_BUDGET == 240)
smoke("pin BWD_BUDGET=72", RUN.BWD_BUDGET == 72)
smoke("pin model id", RUN.MODEL_ID == "EleutherAI/pythia-410m")
smoke("pin sha256", RUN.PINNED_SHA256 ==
      "4c242d9ac702a4029a674eacee84e0517cb6f79d794661dc3a3102bca5ed48dd")
smoke("pin LAYER_INDEX=20", RUN.LAYER_INDEX == 20)
smoke("pin RHO=1.0", RUN.RHO == 1.0)
smoke("pin DELTA=0.1", RUN.DELTA == 0.1)

# 3. Spearman tables n=12..19 present and valid
tables_dir = os.path.join(HERE, "exp084_spearman_tables")
for n in range(12, 20):
    p = os.path.join(tables_dir, f"spearman_null_n{n}.json")
    exists = os.path.exists(p)
    valid = False
    if exists:
        try:
            rec = json.load(open(p))
            valid = (rec["n"] == n and rec["d_max"] == n * (n * n - 1) // 3
                     and sum(rec["counts"]) == math.factorial(n))
        except Exception:
            valid = False
    smoke(f"spearman table n={n} valid", exists and valid,
          "missing or corrupt" if not (exists and valid) else "")
# n=20..24: not precomputed (see BUILD_NOTES §1 gap)

# 4. runner refuses execution
try:
    RUN.main()
    smoke("runner refuses (no clearance)", False, "main() did not raise")
except RuntimeError:
    smoke("runner refuses (no clearance)", True)

# 5. C generator source present
smoke("C generator source present",
      os.path.exists(os.path.join(HERE, "tools", "gen_spearman_null.c")))
smoke("table build script present",
      os.path.exists(os.path.join(HERE, "tools", "build_spearman_tables.py")))
smoke("GPU table build script present (n=20..24, NTT+Ryser)",
      os.path.exists(os.path.join(HERE, "tools", "build_spearman_tables_gpu.py")))

# 6. mock-model end-to-end harness (zero model passes, zero torch).
#    Runs the entire run_exp084.run_full_loop orchestration on synthetic
#    activation landscapes: all arms, guard logic (INVALID i/ii/iii/iv),
#    pass-budget accounting, tie/table loud halts, verdict adjudication.
try:
    import tempfile
    import mock_harness as MH
    with tempfile.TemporaryDirectory() as _td:
        _mh = MH.run_all(_td)
    for _name, _ok, _detail in _mh:
        smoke(f"mock: {_name}", _ok, _detail)
except Exception as e:
    smoke("mock harness", False, f"{type(e).__name__}: {e}")

print("SMOKE RESULT: " + ("PASS" if ok else "FAIL"))
sys.exit(0 if ok else 1)
