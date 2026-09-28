"""Decodability Gap falsification kit — the seven degeneracy unit tests (a)–(g).

These are the S4-8' pre-registration §5 tests, ported from the EXP105
unit_tests_exp105.py to run standalone on core/scoring.py. They exercise the
rank / top-1 / masking / McNemar / bar-order machinery BEFORE any bench
contact. All must PASS or the run HALTs.

Run:  python tests/test_degeneracy.py        (from the kit root)
      python -m pytest tests/                (if pytest is installed)

numpy is used only for a faithful float32 round-trip; scipy is used only for
the McNemar cross-check (f). core/scoring.py itself is pure stdlib.
"""
import os
import sys

KIT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, KIT_ROOT)

from core.scoring import (
    correct_rank, top1_decision, masked_argmax, mcnemar_exact,
    token_id_rank_of_correct, tier0_verdict,
)

results = []


def check(name, cond, detail=""):
    results.append({"test": name, "pass": bool(cond), "detail": detail})
    print(("PASS" if cond else "FAIL"), name, detail, flush=True)
    if not cond:
        raise SystemExit("UNIT TEST FAILED: %s — HALT" % name)


def f32(xs):
    """Faithful float32 round-trip: what the run scripts actually compare."""
    import numpy as np
    return np.asarray(xs, dtype=np.float32).astype(float).tolist()


TIDS = [5000, 100, 8000, 42, 9999, 7, 31337, 1234]

# (a) constant-logit input -> rank function returns the ascending-token-id
#     tie-break. token ids ascending: 7(i5), 42(i3), 100(i1), 1234(i7),
#     5000(i0), 8000(i2), 9999(i4), 31337(i6). Correct idx 3 (token 42) -> 2.
lg = f32([0.0] * 8)
check("(a) constant logits -> token-id tie-break rank",
      correct_rank(lg, 3, TIDS) == 2,
      "rank=%s" % correct_rank(lg, 3, TIDS))
check("(a2) constant logits -> top-1 is smallest token id",
      top1_decision(lg, TIDS) == 5,
      "top1=%s" % top1_decision(lg, TIDS))

# (g, cloze-specific) synthetic all-equal-logit item: the tie-break path is
# exercised for every correct position, not assumed.
lg = f32([2.5] * 8)
for ci in range(8):
    expected = sorted(range(8), key=lambda j: TIDS[j]).index(ci) + 1
    got = correct_rank(lg, ci, TIDS)
    check("(g) tie-break path correct_idx=%d" % ci, got == expected,
          "rank=%s expected=%s" % (got, expected))

# token-id tie-break differs from index tie-break when token ids are unsorted.
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
    check("(b) mask non-top1 idx=%d preserves argmax" % j,
          masked_argmax(lg, j, TIDS) == base)

# (c) masking top-1 promotes the previous runner-up on fixed logits.
check("(c) mask top-1 promotes runner-up",
      masked_argmax(lg, 1, TIDS) == 3,
      "promoted=%s" % masked_argmax(lg, 1, TIDS))

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
      worst < 1e-12, "max|diff|=%.2e" % worst)

# Pre-registered feasibility anchors.
check("(f2) b=6,c=0 -> p=0.03125", abs(mcnemar_exact(6, 0) - 0.03125) < 1e-15)
check("(f3) b=5,c=0 -> p=0.0625", abs(mcnemar_exact(5, 0) - 0.0625) < 1e-15)

# Bar-order sanity.
check("(ord1) acc=0.10 -> LINE-CLOSED",
      tier0_verdict(0.10, [2, 3, 2], 0.0) == "LINE-CLOSED")
check("(ord2) acc=0.50, med=6 -> KILL",
      tier0_verdict(0.50, [6, 7, 6, 8, 6], 0.0) == "KILL")
check("(ord3) acc=0.90 -> UNDERDETERMINED (n_pop=9<12 before HOLD)",
      tier0_verdict(0.90, [2, 3, 2, 4, 2, 3, 2, 4, 3], 0.0) == "UNDERDETERMINED")
check("(ord4) acc=0.80 -> HOLD",
      tier0_verdict(0.80, [2] * 12, 0.0) == "HOLD")
check("(ord5) tie 0.30 -> HOLD",
      tier0_verdict(0.50, [2] * 12, 0.30) == "HOLD")
check("(ord6) clean -> TIER-0 PASSED",
      tier0_verdict(0.40, [2] * 12, 0.0) == "TIER-0 PASSED")

# token-id-rank diagnostic helper sanity.
check("(diag) token_id_rank_of_correct",
      token_id_rank_of_correct(3, TIDS) == 2)

print("\nALL %d UNIT TESTS PASSED" % len(results), flush=True)
