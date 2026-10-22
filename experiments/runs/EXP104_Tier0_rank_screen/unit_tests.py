# unit_tests.py — §4 degeneracy tests on SYNTHETIC data (no model contact).
# Must ALL pass before the Tier-0 machinery touches the bench.
import sys, math, json
sys.path.insert(0, "/home/hatch/workspace/SCBI/experiments/runs/EXP104_Tier0_rank_screen")

BUNDLE = "/home/hatch/workspace/SCBI/experiments/runs/EXP104_Tier0_rank_screen"
results = {}

# ---- machinery under test (same functions run_tier0.py will use) ----
def correct_rank(logits8, correct_idx):
    """1-based rank of the correct option; ties broken by option-index order."""
    order = sorted(range(8), key=lambda j: (-logits8[j], j))
    return order.index(correct_idx) + 1

def mask_argmax(logits8, mask_idx):
    m = list(logits8)
    m[mask_idx] = -1e9
    best = max(range(8), key=lambda j: (m[j], -j))  # argmax, ties -> lowest index
    return best

def mcnemar_exact(b, c):
    """Two-sided exact McNemar via doubled one-sided binomial tail."""
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    # P(X <= k), X ~ Binomial(n, 0.5), via hand recurrence
    p0 = 0.5 ** n
    pk, s = p0, p0
    for i in range(1, k + 1):
        pk = pk * (n - i + 1) / i
        s += pk
    return min(1.0, 2.0 * s)

def binom_cdf_hand(k, n, p=0.5):
    pk = (1 - p) ** n
    s = pk
    for i in range(1, k + 1):
        pk = pk * (n - i + 1) / i * (p / (1 - p))
        s += pk
    return s

# (a) constant-logit input -> rank returns the option-index tie-break
r = correct_rank([0.0] * 8, 5)
results["a_const_logit_tiebreak"] = {"rank": r, "expected": 6, "pass": r == 6}

# (b) masking a non-top-1 token never changes argmax on fixed logits
logits = [3.0, 1.0, 2.0, 0.5, -1.0, 4.0, 0.1, 0.2]  # top-1 = idx 5
base = mask_argmax(logits, -1) if False else max(range(8), key=lambda j: (logits[j], -j))
ok_b = all(mask_argmax(logits, j) == base for j in range(8) if j != 5)
results["b_mask_nontop1_nochange"] = {"base": base, "pass": bool(ok_b)}

# (c) masking top-1 promotes the previous runner-up on fixed logits
promoted = mask_argmax(logits, 5)
results["c_mask_top1_promotes_runnerup"] = {"promoted": promoted, "expected": 0, "pass": promoted == 0}

# (d) b=c=0 -> McNemar p=1.0 is a valid null, not an error
p00 = mcnemar_exact(0, 0)
results["d_b0_c0_p1"] = {"p": p00, "pass": p00 == 1.0}

# (e) empty failed set -> Tier-0 vacuous -> KILL (premise) routing
def tier0_route(failed_ranks, n_pop, acc, tie_rate):
    if len(failed_ranks) == 0:
        return "KILL-premise-vacuous"  # §4(e)
    import statistics
    med = statistics.median(failed_ranks)
    if med > 5:
        return "KILL-premise"
    if n_pop < 12:
        return "UNDERDETERMINED"
    if not (0.25 <= acc <= 0.75):
        return "HOLD-sanity"
    if tie_rate > 0.25:
        return "HOLD-tieguard"
    return "TIER0-PASSED"
results["e_empty_failed_vacuous"] = {"route": tier0_route([], 0, 0.5, 0.0),
                                     "pass": tier0_route([], 0, 0.5, 0.0) == "KILL-premise-vacuous"}
# routing spot checks
assert tier0_route([6, 7, 8], 0, 0.5, 0.0) == "KILL-premise"
assert tier0_route([1, 2, 3], 5, 0.5, 0.0) == "UNDERDETERMINED"
assert tier0_route([1, 2] * 8, 16, 0.9, 0.0) == "HOLD-sanity"
assert tier0_route([1, 2] * 8, 16, 0.5, 0.3) == "HOLD-tieguard"
assert tier0_route([1, 2] * 8, 16, 0.5, 0.0) == "TIER0-PASSED"
results["e_routing_spotchecks"] = {"pass": True}

# (f) McNemar-exact cross-check on the FULL (b,c) grid vs hand recurrence + scipy
try:
    from scipy.stats import binomtest
    have_scipy = True
except ImportError:
    have_scipy = False
mismatch_hand, mismatch_scipy, worst = 0, 0, 0.0
for b in range(0, 11):
    for c in range(0, 11):
        mine = mcnemar_exact(b, c)
        ref = min(1.0, 2.0 * binom_cdf_hand(min(b, c), b + c))
        if abs(mine - ref) > 1e-12:
            mismatch_hand += 1
        if have_scipy and (b + c) > 0:
            sp = binomtest(min(b, c), b + c, 0.5, alternative="two-sided").pvalue
            # scipy uses the min-likelihood two-sided: document, don't require equality
            worst = max(worst, abs(mine - sp))
results["f_mcnemar_grid"] = {
    "grid": "b,c in 0..10 (121 cells)",
    "mismatches_vs_hand_recurrence": mismatch_hand,
    "have_scipy": have_scipy,
    "max_abs_diff_vs_scipy_two_sided": worst,
    "note": "scipy two-sided is min-likelihood, not doubling; difference is definitional, documented",
    "pass": mismatch_hand == 0,
}
# pre-registered feasibility anchors
results["f_anchors"] = {
    "b6_c0": mcnemar_exact(6, 0),   # expect 0.03125
    "b5_c0": mcnemar_exact(5, 0),   # expect 0.0625
    "pass": abs(mcnemar_exact(6, 0) - 0.03125) < 1e-12 and abs(mcnemar_exact(5, 0) - 0.0625) < 1e-12,
}

allpass = all(v["pass"] for v in results.values())
print(json.dumps(results, indent=1))
print("ALL SIX:", "PASS" if allpass else "FAIL")
json.dump(results, open(BUNDLE + "/unit_tests.json", "w"), indent=1)
sys.exit(0 if allpass else 1)
