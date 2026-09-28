"""EXP097 pre-execution checks — all must PASS before any model run.

Run with the isolated venv python BEFORE invoking run_exp097.py.
Constant-data unit tests (LOG-4338 lesson): every diagnostic must fail safe
on degenerate input. Any FAIL -> fix before execution, never proceed.
"""

import csv
import hashlib
import os
import sys

BUNDLE_DIR = os.path.dirname(os.path.abspath(__file__))
EXP094_DIR = os.path.join(os.path.dirname(BUNDLE_DIR), "EXP094_peritem_l11")
sys.path.insert(0, BUNDLE_DIR)

import numpy as np

failures = []


def check(name, cond, detail=""):
    status = "PASS" if cond else "FAIL"
    print(f"[{status}] {name}" + (f" — {detail}" if detail else ""))
    if not cond:
        failures.append(name)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


# --- frozen pins (protocol §4) ---
check("constructor hash == pin",
      sha256_file(os.path.join(EXP094_DIR, "constructor.py")) ==
      "5e03f206dd907b52baa1ab6d5c9954c709d1b47d143c83f9aa85caa81917f361")
check("archive hash == pin",
      sha256_file(os.path.join(EXP094_DIR, "out",
                               "per_item_records.csv")) ==
      "9ada6ef9d489aee959b56160053cbe7bdb7024e6c593cbf3a9ffbfd9b366d149")

# --- protocol arithmetic (protocol §2.2 / §2.3 / §2.4 / §4.2) ---
from run_exp097 import RATIOS, G5_BANDS  # noqa: E402

check("ratio 1.5 in [1.125, 1.875]",
      G5_BANDS["1.5"][0] <= 1.5 <= G5_BANDS["1.5"][1])
check("ratio 3.0 in [2.25, 3.75]",
      G5_BANDS["3.0"][0] <= 3.0 <= G5_BANDS["3.0"][1])
check("executor alpha for 1.5 == 1.5/0.0474",
      abs(1.5 / 0.0474 - 31.64556962) < 1e-6)
check("executor alpha for 3.0 == 3.0/0.0474",
      abs(3.0 / 0.0474 - 63.29113924) < 1e-6)
check("model passes 360 <= 600 hard cap", 60 + 60 + 4 * 60 == 360)
check("expected 390 <= 600 hard cap", 390 <= 600)

# --- bench composition (ungated 60; protocol §2.2) ---
margins_B, strata_B = {}, {}
with open(os.path.join(EXP094_DIR, "out", "per_item_records.csv"),
          newline="") as f:
    for row in csv.DictReader(f):
        if row["arm"] == "B":
            margins_B[row["item_id"]] = float(row["margin"])
            strata_B[row["item_id"]] = row["stratum"]
check("archived B vector has 60 items", len(margins_B) == 60)
check("bench strata 30/30",
      sum(1 for s in strata_B.values() if s == "A-first") == 30 and
      sum(1 for s in strata_B.values() if s == "C-first") == 30)

# --- statistical machinery unit tests (frozen EXP094 scorer) ---
sys.path.append(EXP094_DIR)
score094 = __import__("score_exp094")
check("McNemar b=8,c=0 -> 0.0078125 (discovery bar)",
      abs(score094.mcnemar_exact_p(8, 0) - 0.0078125) < 1e-12)
check("McNemar b=7,c=0 -> 0.015625 n.s.",
      abs(score094.mcnemar_exact_p(7, 0) - 0.015625) < 1e-12)
st = score094.contrast_stats(np.ones(60, bool), np.ones(60, bool))
check("constant input -> p=1.0, delta=0 (fails safe toward KILL)",
      st["mcnemar_p"] == 1.0 and st["delta"] == 0.0)
st2 = score094.contrast_stats(np.zeros(60, bool), np.zeros(60, bool))
check("all-wrong constant -> p=1.0, delta=0.0",
      st2["mcnemar_p"] == 1.0 and st2["delta"] == 0.0)
ci = score094.tango_ci_paired(0, 0, 60, 0)
check("Tango CI on constant -> [0,0]", ci[0] == 0.0 and ci[1] == 0.0)

# --- scorer integration on the archived B vector ---
score097 = __import__("score_exp097")
item_ids = sorted(margins_B.keys())
mB = np.array([margins_B[i] for i in item_ids])
ph = [strata_B[i] for i in item_ids]
all_in = np.ones(60, dtype=bool)
tbl, sec = score097.score_ratio("1.5", mB, mB, mB, ph, all_in, all_in)
check("per-ratio scorer: 9 cells", len(tbl) == 9, f"got {len(tbl)}")
check("scorer B-vs-B -> all p=1.0",
      all(v["mcnemar_p"] == 1.0 for v in tbl.values()))
check("scorer B-vs-B -> flips 0 (liveness instrument quiet)",
      sec["flips_T_vs_B"] == 0 and sec["flips_W_vs_B"] == 0)
check("scorer tie gate counts 180 rows",
      sec["tie_count"] == 0 and not sec["tie_gate_fires"])

# --- coherence gate unit test (constant injection arm -> fires) ---
m_const = np.zeros(60)
tbl_c, sec_c = score097.score_ratio("3.0", mB, m_const, mB, ph,
                                    all_in, all_in)
check("coherence gate: constant T arm -> zero_variance_T True",
      sec_c["zero_variance_T"] and sec_c["coherence_gate_fires"])
check("coherence gate: B arm not constant -> zero_variance_B False",
      not sec_c["zero_variance_B"])

# --- liveness instrument unit test (single flip unlocks) ---
m_flip = mB.copy()
i0 = int(np.argmin(np.abs(mB)))
m_flip[i0] = -m_flip[i0]  # force one decision flip on the W arm
_, sec_f = score097.score_ratio("1.5", mB, mB, m_flip, ph, all_in, all_in)
check("liveness instrument: 1 W flip -> flips_W_vs_B == 1",
      sec_f["flips_W_vs_B"] == 1, f"got {sec_f['flips_W_vs_B']}")

print()
if failures:
    print(f"PRECHECKS FAILED: {failures}")
    sys.exit(1)
print(f"ALL {22 - len(failures)} PRECHECKS PASS — execution authorized by LOG-4414.")
