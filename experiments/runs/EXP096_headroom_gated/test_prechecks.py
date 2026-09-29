"""EXP096 pre-execution checks — all must PASS before any model run.

Run with the isolated venv python BEFORE invoking run_exp096.py.
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

# --- gate reproduction (protocol §2.1.1 / §3 step-0(iii)) ---
from run_exp096 import APPENDIX_A, TAU_8  # noqa: E402

margins_B, strata_B, correct_B = {}, {}, {}
with open(os.path.join(EXP094_DIR, "out", "per_item_records.csv"),
          newline="") as f:
    for row in csv.DictReader(f):
        if row["arm"] == "B":
            margins_B[row["item_id"]] = float(row["margin"])
            strata_B[row["item_id"]] = row["stratum"]
            correct_B[row["item_id"]] = int(row["correct_top1"])
recomputed = sorted(i for i, m in margins_B.items() if abs(m) <= TAU_8)
check("|G| == 21", len(recomputed) == 21, f"got {len(recomputed)}")
check("G == Appendix A (member-for-member)", recomputed == sorted(APPENDIX_A))
check("A-first/C-first == 13/8",
      sum(1 for i in APPENDIX_A if strata_B[i] == "A-first") == 13 and
      sum(1 for i in APPENDIX_A if strata_B[i] == "C-first") == 8)
check("wrong/right == 5/16",
      sum(1 for i in APPENDIX_A if correct_B[i] == 0) == 5)

# --- band / tripwire / budget arithmetic (protocol §2.2 / §2.4 / §2.3) ---
check("alpha=8.0 target 0.3792 in [0.2844, 0.4740]",
      0.2844 <= 8 * 0.0474 <= 0.4740, f"{8 * 0.0474}")
check("over-coverage tripwire 0.5*0.90 == 0.45", 0.5 * TAU_8 == 0.45)
check("under-coverage tripwire 1.25*0.90 == 1.125", 1.25 * TAU_8 == 1.125)
check("budget 162 <= 400 hard cap", 60 + 60 + 21 + 21 == 162)

# --- statistical machinery unit tests (frozen EXP094 scorer) ---
sys.path.append(EXP094_DIR)
score094 = __import__("score_exp094")
check("McNemar b=6,c=0 -> 0.03125",
      abs(score094.mcnemar_exact_p(6, 0) - 0.03125) < 1e-12)
check("McNemar b=5,c=0 -> 0.0625 (positive infeasibility)",
      abs(score094.mcnemar_exact_p(5, 0) - 0.0625) < 1e-12)
st = score094.contrast_stats(np.ones(21, bool), np.ones(21, bool))
check("constant input -> p=1.0 (fails safe toward KILL)",
      st["mcnemar_p"] == 1.0 and st["delta"] == 0.0)
st2 = score094.contrast_stats(np.zeros(21, bool), np.zeros(21, bool))
check("all-wrong constant -> p=1.0, delta=0.0",
      st2["mcnemar_p"] == 1.0 and st2["delta"] == 0.0)
ci = score094.tango_ci_paired(0, 0, 21, 0)  # no discordant, 21 concordant
check("Tango CI on constant -> [0,0]", ci[0] == 0.0 and ci[1] == 0.0)

# --- scorer integration on the frozen gate ---
score096 = __import__("score_exp096")
mB = np.array([margins_B[i] for i in APPENDIX_A])
ph = [strata_B[i] for i in APPENDIX_A]
tbl, sec = score096.score_gated(mB, mB, mB, ph)  # B-vs-B sanity
check("gated scorer: 9 cells (protocol '27' is arithmetic shorthand)",
      len(tbl) == 9, f"got {len(tbl)}")
check("gated scorer B-vs-B -> all p=1.0",
      all(v["mcnemar_p"] == 1.0 for v in tbl.values()))
check("gated scorer tie gate counts 42 rows", sec["tie_count"] == 0)

print()
if failures:
    print(f"PRECHECKS FAILED: {failures}")
    sys.exit(1)
print(f"ALL {18 - len(failures)} PRECHECKS PASS — execution authorized by LOG-4405.")
