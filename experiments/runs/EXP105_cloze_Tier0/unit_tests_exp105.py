# unit_tests_exp105.py — the seven S4-8' v2 sec 5 degeneracy unit tests (a)-(g)
# re-run on the cloze rank/mask/McNemar machinery BEFORE bench contact.
# All must PASS or the run HALTs.
import sys
import math
import torch

sys.path.insert(0, "/home/hatch/workspace/SCBI/experiments/runs/EXP105_cloze_Tier0")
from exp105_lib import (correct_rank, top1_decision, masked_argmax,
                        mcnemar_exact, token_id_rank_of_correct, tier0_verdict)

results = []


def check(name, cond, detail=""):
    results.append({"test": name, "pass": bool(cond), "detail": detail})
    print(("PASS" if cond else "FAIL"), name, detail, flush=True)
    if not cond:
        raise SystemExit(f"UNIT TEST FAILED: {name} — HALT per v2 sec 5")


def f32(xs):
    """Faithful float32 round-trip: what the run script actually compares."""
    return torch.tensor(xs, dtype=torch.float32).tolist()


TIDS = [5000, 100, 8000, 42, 9999, 7, 31337, 1234]

# (a) constant-logit input -> rank function returns the ascending-token-id tie-break.
#     token ids sorted ascending: 7(i5), 42(i3), 100(i1), 1234(i7), 5000(i0),
#     8000(i2), 9999(i4), 31337(i6). Correct idx 3 (token 42) -> rank 2.
lg = f32([0.0] * 8)
check("(a) constant logits -> token-id tie-break rank",
      correct_rank(lg, 3, TIDS) == 2,
      f"rank={correct_rank(lg, 3, TIDS)}")
check("(a2) constant logits -> top-1 is smallest token id",
      top1_decision(lg, TIDS) == 5,
      f"top1={top1_decision(lg, TIDS)}")

# (g, cloze-specific) synthetic all-equal-logit item: r_i = rank by token-id
# order for the correct token — the tie-break path is exercised, not assumed.
lg = f32([2.5] * 8)
for ci in range(8):
    expected = sorted(range(8), key=lambda j: TIDS[j]).index(ci) + 1
    got = correct_rank(lg, ci, TIDS)
    check(f"(g) tie-break path correct_idx={ci}", got == expected,
          f"rank={got} expected={expected}")

# token-id tie-break differs from EXP104's index tie-break when token ids are unsorted:
# tie for top between idx 0 (token 9000) and idx 1 (token 100) -> idx 1 wins by token id.
lg = f32([5.0, 5.0, 1.0, 0.5, -1.0, 2.0, 3.0, 4.0])
check("(g2) token-id tie-break beats index tie-break",
      top1_decision(lg, [9000, 100, 42, 7, 1, 55, 66, 77]) == 1)

# (b) masking a non-top-1 candidate never changes argmax on fixed logits.
lg = f32([1.0, 5.0, 2.0, 4.0, 3.0, 0.5, -1.0, 2.5])
base = top1_decision(lg, TIDS)
assert base == 1, "test fixture sanity"
for j in range(8):
    if j == base:
        continue
    check(f"(b) mask non-top1 idx={j} preserves argmax",
          masked_argmax(lg, j, TIDS) == base)

# (c) masking top-1 promotes the previous runner-up on fixed logits.
check("(c) mask top-1 promotes runner-up",
      masked_argmax(lg, 1, TIDS) == 3,
      f"promoted={masked_argmax(lg, 1, TIDS)}")

# (d) b=c=0 -> McNemar p=1.0 is a valid null, not an error.
check("(d) b=c=0 -> p=1.0", mcnemar_exact(0, 0) == 1.0)

# (e) empty failed set -> Tier-0 vacuous -> KILL (premise).
check("(e) empty failed set -> KILL",
      tier0_verdict(1.0, [], 0.0) == "KILL")

# (f) McNemar-exact cross-checked against scipy.stats.binomtest (two-sided)
#     on the full (b,c) grid 0..10. Mismatches void the statistics machinery.
from scipy.stats import binomtest
worst = 0.0
for b in range(11):
    for c in range(11):
        n = b + c
        ref = 1.0 if n == 0 else binomtest(min(b, c), n, 0.5,
                                          alternative="two-sided").pvalue
        got = mcnemar_exact(b, c)
        worst = max(worst, abs(got - ref))
check("(f) mcnemar_exact == scipy binomtest on (b,c) in [0,10]^2",
      worst < 1e-12, f"max|diff|={worst:.2e}")

# Pre-reg feasibility anchors from v2 sec 5.
check("(f2) b=6,c=0 -> p=0.03125", abs(mcnemar_exact(6, 0) - 0.03125) < 1e-15)
check("(f3) b=5,c=0 -> p=0.0625", abs(mcnemar_exact(5, 0) - 0.0625) < 1e-15)

# Bar-order sanity: the v2 amendment split (LINE-CLOSED first, KILL second).
check("(ord1) acc=0.10 -> LINE-CLOSED", tier0_verdict(0.10, [2, 3, 2], 0.0) == "LINE-CLOSED")
check("(ord2) acc=0.50, med=6 -> KILL", tier0_verdict(0.50, [6, 7, 6, 8, 6], 0.0) == "KILL")
check("(ord3) acc=0.90 -> UNDERDETERMINED (n_pop=9<12 before HOLD)",
      tier0_verdict(0.90, [2, 3, 2, 4, 2, 3, 2, 4, 3], 0.0) == "UNDERDETERMINED")
check("(ord4) acc=0.80 -> HOLD", tier0_verdict(0.80, [2]*12, 0.0) == "HOLD")
check("(ord5) tie 0.30 -> HOLD", tier0_verdict(0.50, [2]*12, 0.30) == "HOLD")
check("(ord6) clean -> TIER-0 PASSED", tier0_verdict(0.40, [2]*12, 0.0) == "TIER-0 PASSED")

# token-id-rank diagnostic helper sanity.
check("(diag) token_id_rank_of_correct", token_id_rank_of_correct(3, TIDS) == 2)

print(f"\nALL {len(results)} UNIT TESTS PASSED", flush=True)
import json
json.dump(results, open("/home/hatch/workspace/SCBI/experiments/runs/EXP105_cloze_Tier0/unit_tests_exp105.json", "w"), indent=1)
