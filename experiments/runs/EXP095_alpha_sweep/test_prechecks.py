"""EXP095 pre-run unit checks — deterministic machinery, no model passes.

Checks (from S5-1 §F8, licensed by LOG-4398):
  U1. McNemar exact on constant input -> p=1 (the EXP094 lesson).
  U2. McNemar exact b=8, c=0 -> p=0.0078125 (doubling convention).
  U3. score_alpha tie gate: >5% ties over 180 rows -> RunInvalid.
  U4. mean_pairwise_abs_cosine on identical unit directions -> 1.0.
  U5. build_per_item_direction with a==b -> degenerate_zero True (the F7
      zero-norm route the executor turns into HOLD).
  U6. G7.1 constructor re-hash equals the frozen pin (gate input).
  U7. Delivery-band algebra: alpha*0.0474 lands inside §2.2 bands.
Exit 0 iff all pass.
"""

import math
import os
import sys

BUNDLE = os.path.dirname(os.path.abspath(__file__))
EXP094 = os.path.join(os.path.dirname(BUNDLE), "EXP094_peritem_l11")
sys.path.insert(0, BUNDLE)
sys.path.append(EXP094)

import numpy as np

import constructor as C
from test_g7_audit import sha256_file

CONSTRUCTOR_PIN = ("5e03f206dd907b52baa1ab6d5c9954c709d1b47d143c83f9aa85caa"
                   "81917f361")

failures = []


def check(name, cond, detail=""):
    print(("PASS" if cond else "FAIL"), name, detail)
    if not cond:
        failures.append(name)


# U1
from score_exp095 import mcnemar_exact_p, contrast_stats
p = mcnemar_exact_p(0, 0)
check("U1 mcnemar(0,0)=1", p == 1.0, f"p={p}")

# U2
p = mcnemar_exact_p(8, 0)
check("U2 mcnemar(8,0)=0.0078125", abs(p - 0.0078125) < 1e-12, f"p={p}")
p2 = mcnemar_exact_p(0, 8)
check("U2' symmetry mcnemar(0,8)", abs(p2 - 0.0078125) < 1e-12, f"p={p2}")

# U3 — tie gate: 10 ties out of 180 -> RunInvalid
from score_exp095 import score_alpha, RunInvalid as ScorerRunInvalid
rng = np.random.default_rng(0)
mB = rng.normal(size=60)
mT = rng.normal(size=60)
mW = rng.normal(size=60)
mB[:4] = 0.0
mT[:3] = 0.0
mW[:3] = 0.0  # 10 ties -> 10/180 > 5%
try:
    score_alpha(mB, mT, mW, ["A-first"] * 30 + ["C-first"] * 30, 1.0)
    check("U3 tie-gate raises", False, "no exception")
except ScorerRunInvalid as e:
    check("U3 tie-gate raises", "RUN-INVALID" in str(e), str(e)[:60])

# U3' — 9 ties out of 180 passes the gate
mB3 = rng.normal(size=60)
mB3[:3] = 0.0  # 3+3+3 = 9 ties -> 5.0% not > 5%
tbl, sec = score_alpha(mB3, mT, mW, ["A-first"] * 30 + ["C-first"] * 30, 1.0)
check("U3' 9 ties passes", len(tbl) == 9, f"cells={len(tbl)}")

# U4
from run_exp095 import mean_pairwise_abs_cosine
U = np.tile(np.array([1.0, 0.0, 0.0]), (5, 1))
check("U4 degeneracy identical=1.0",
      abs(mean_pairwise_abs_cosine(U) - 1.0) < 1e-12)

# U5 — zero-norm route
a = np.ones(64)
d, info = C.build_per_item_direction(a, a, 3.0)
check("U5 zero-norm degenerate flag", info["degenerate_zero"] is True,
      f"r_norm={info['r_norm']}")
check("U5 zero-norm vector", float(np.linalg.norm(d)) == 0.0)

# U6
live = sha256_file(os.path.join(EXP094, "constructor.py"))
check("U6 constructor pin", live == CONSTRUCTOR_PIN, live[:16] + "…")

# U7 — band algebra
bands = {0.25: (0.00889, 0.01481), 0.5: (0.01778, 0.02963),
         1.0: (0.0355, 0.0593), 2.0: (0.0711, 0.1185),
         4.0: (0.1422, 0.2370)}
for alpha, (lo, hi) in bands.items():
    r = alpha * C.NORM_RATIO
    check(f"U7 band a={alpha}", lo <= r <= hi, f"target={r:.6f}")

print("ALL PASS" if not failures else f"FAILURES: {failures}")
sys.exit(1 if failures else 0)
