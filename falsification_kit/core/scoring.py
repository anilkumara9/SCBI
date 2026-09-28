"""Decodability Gap falsification kit — core scoring machinery.

Ports the EXP105 machinery (exp105_lib.py + run_battery_exp105.py decision
table) into a model-agnostic, dependency-light form. The functions here are
the SAME algorithms exercised by tests/test_degeneracy.py, and the same
algorithms imported by tier0.py and battery.py, so the tested machinery is
the run machinery (no drift).

Conventions (frozen — do not "improve"):
- k = 8 candidates per item.
- correct_rank: rank 1..8 of the correct candidate by logit descending;
  float32 exact-equality ties broken by ASCENDING token id.
- Masking operator: set the masked candidate's logit to -1e9, then re-argmax.
- McNemar-exact: two-sided binomial, b=c=0 -> p=1.0 (valid null).
- Tier-0 and battery bar orders are binding; see tier0_verdict() and
  battery_decision().
"""
import math
import random
import statistics

K = 8
MASK_LOGIT = -1e9
R_SEED = 20260928          # pinned BEFORE any battery computation
ALPHA_PRIMARY = 0.05       # primary T-vs-R McNemar
ALPHA_BONF = 0.0125        # other contrasts, Bonferroni
DELTA_BAR = 0.10           # CONTINUE needs dM_T > 0.10
FLAT_BAND = 0.05           # |dM| < 0.05 counts as flat
O_GATE = 0.5               # F arm non-diagnostic when overlap O > 0.5


def correct_rank(logits8, correct_idx, token_ids8):
    """Rank (1..8) of the correct candidate by logit desc; float32-exact
    equality ties broken by ASCENDING token id."""
    assert len(logits8) == K and len(token_ids8) == K
    order = sorted(range(K), key=lambda j: (-logits8[j], token_ids8[j]))
    return order.index(correct_idx) + 1


def top1_decision(logits8, token_ids8):
    """Argmax over the 8 candidate logits with ascending-token-id tie-break."""
    assert len(logits8) == K and len(token_ids8) == K
    return max(range(K), key=lambda j: (logits8[j], -token_ids8[j]))


def masked_argmax(logits8, mask_idx, token_ids8):
    """Mask one candidate (logit -> -1e9) and re-argmax."""
    masked = list(logits8)
    masked[mask_idx] = MASK_LOGIT
    return top1_decision(masked, token_ids8)


def mcnemar_exact(b, c):
    """Two-sided exact McNemar p = 2 * P(Bin(b+c, 0.5) <= min(b,c)), cap 1.0.
    Anchors: b=6,c=0 -> 0.03125; b=5,c=0 -> 0.0625; b=c=0 -> 1.0."""
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    tail = sum(math.comb(n, i) for i in range(k + 1)) / (2 ** n)
    return min(1.0, 2.0 * tail)


def tango_ci(b, c, d, alpha=0.05):
    """Tango (1998) score CI for paired difference delta=(b-c)/n, 95%.

    Constrained MLE of theta=(p12+p21)/2 under H0: p12-p21=delta via direct
    bounded maximization of the (concave) log-likelihood; handles boundary
    cases (b=0 or c=0) via the 0*log0:=0 convention. Falls back to
    Newcombe-Wilson when scipy is unavailable.
    """
    try:
        from scipy.stats import chi2
        from scipy.optimize import brentq, minimize_scalar
    except ImportError:
        return _newcombe_interval(b, c, d, alpha)
    z2 = float(chi2.ppf(1 - alpha, 1))
    try:
        return _tango_interval(float(b), float(c), float(d), z2, brentq,
                               minimize_scalar)
    except Exception:
        return _newcombe_interval(b, c, d, alpha)


def _tango_interval(b, c, d, z2, brentq, minimize_scalar):
    n = b + c + d
    if n == 0:
        return (float("nan"), float("nan"))

    def nll(theta, delta):
        # negative log-likelihood of the constrained trinomial
        p12 = theta + delta / 2.0
        p21 = theta - delta / 2.0
        p22 = 1.0 - 2.0 * theta
        if p12 < 0 or p21 < 0 or p22 < 0:
            return float("inf")
        ll = 0.0
        for x, p in ((b, p12), (c, p21), (d, p22)):
            if x > 0:
                if p <= 0:
                    return float("inf")
                ll += x * math.log(p)
        return -ll

    def score2(delta):
        lo = max(0.0, -delta / 2.0) + 1e-12
        hi = min(0.5, (1.0 - abs(delta)) / 2.0) - 1e-12
        if hi <= lo:
            return float("inf")
        res = minimize_scalar(lambda t: nll(t, delta), bounds=(lo, hi),
                              method="bounded")
        th = res.x
        p12 = th + delta / 2.0
        p21 = th - delta / 2.0
        # score statistic
        num = (b - c - n * delta) ** 2
        var = n * (p12 + p21 - (p12 - p21) ** 2)
        if var <= 0:
            return float("inf")
        return num / var

    dhat = (b - c) / n
    lo = brentq(lambda dlt: score2(dlt) - z2, -1.0 + 1e-9, dhat)
    hi = brentq(lambda dlt: score2(dlt) - z2, dhat, 1.0 - 1e-9)
    return (lo, hi)


def _newcombe_interval(b, c, d, alpha=0.05):
    """Newcombe-Wilson fallback for the paired difference (no scipy needed)."""
    import math as _m
    n = b + c + d
    if n == 0:
        return (float("nan"), float("nan"))
    z = 1.96 if abs(alpha - 0.05) < 1e-9 else 2.576
    p1 = (b + d) / n
    p2 = (c + d) / n

    def wilson(p):
        den = 1 + z * z / n
        ctr = (p + z * z / (2 * n)) / den
        half = z * _m.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
        return (ctr - half, ctr + half)

    l1, u1 = wilson(p1)
    l2, u2 = wilson(p2)
    delta = p1 - p2
    lo = delta - _m.sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2)
    hi = delta + _m.sqrt((u1 - p1) ** 2 + (p2 - l2) ** 2)
    return (lo, hi)


def token_id_rank_of_correct(correct_idx, token_ids8):
    """Descriptive diagnostic: rank of the correct candidate's token id among
    the 8 candidate token ids, ascending. Expect ~uniform 1..8 on a healthy
    bench; a skewed distribution is a bench-instrument warning."""
    ordered = sorted(range(K), key=lambda j: token_ids8[j])
    return ordered.index(correct_idx) + 1


def tier0_verdict(baseline_acc, failed_ranks, tie_rate):
    """Binding Tier-0 bar order (first match wins):
    1. baseline < 0.25        -> LINE-CLOSED
    2. empty failed set       -> KILL (premise vacuous)
    3. median failed rank > 5 -> KILL (premise)
    4. n_pop < 12             -> UNDERDETERMINED
    5. baseline > 0.75 or tie-guard > 0.25 -> HOLD
    6. else                   -> TIER-0 PASSED
    n_pop = #{failed items with correct_rank <= 5} (the suppressible
    population the battery operates on)."""
    if baseline_acc < 0.25:
        return "LINE-CLOSED"
    if len(failed_ranks) == 0:
        return "KILL"
    med = statistics.median(failed_ranks)
    if med > 5:
        return "KILL"
    n_pop = sum(1 for r in failed_ranks if r <= 5)
    if n_pop < 12:
        return "UNDERDETERMINED"
    if baseline_acc > 0.75 or tie_rate > 0.25:
        return "HOLD"
    return "TIER-0 PASSED"


def battery_arms(logits8, token_ids8, top1_idx, correct_idx, foil_idx, rng):
    """Apply the four pre-registered arms. Returns dict arm -> top-1 idx.
    B: none (baseline). T: mask baseline top-1. F: mask structural foil.
    R: mask uniformly random candidate excluding baseline top-1 AND correct."""
    arms = {"B": top1_decision(logits8, token_ids8)}
    arms["T"] = masked_argmax(logits8, top1_idx, token_ids8)
    arms["F"] = masked_argmax(logits8, foil_idx, token_ids8)
    eligible = [i for i in range(K) if i != top1_idx and i != correct_idx]
    r_mask = rng.choice(eligible)
    arms["R"] = masked_argmax(logits8, r_mask, token_ids8)
    return arms, r_mask


def battery_decision(pop_records):
    """Run the pre-registered decision table on Tier-0-population battery
    records. Each record: dict with 'arms_correct' {B,T,F,R: bool},
    'foil_is_top1' bool, 'r_mask_idx' int.

    Returns (verdict, step, evidence). Steps 1-5 are Tier-0-carried.
    """
    pop = [r for r in pop_records]
    n_pop = len(pop)

    def dM(arm):
        return sum(r["arms_correct"][arm] - r["arms_correct"]["B"]
                   for r in pop) / n_pop if n_pop else 0.0

    dM_T, dM_F, dM_R = dM("T"), dM("F"), dM("R")

    def pair(ax, ay):
        b = sum(1 for r in pop
                if r["arms_correct"][ax] and not r["arms_correct"][ay])
        c = sum(1 for r in pop
                if not r["arms_correct"][ax] and r["arms_correct"][ay])
        d = n_pop - b - c
        return {"b": b, "c": c, "d": d, "p": mcnemar_exact(b, c),
                "tango95": tango_ci(b, c, d)}

    contrasts = {
        "T-vs-B": pair("T", "B"),
        "F-vs-B": pair("F", "B"),
        "R-vs-B": pair("R", "B"),
        "T-vs-R": pair("T", "R"),   # PRIMARY BINDING at ALPHA=0.05
        "T-vs-F": pair("T", "F"),
    }

    O = (sum(1 for r in pop if r["foil_is_top1"]) / n_pop) if n_pop else float("nan")
    p_TR = contrasts["T-vs-R"]["p"]
    p_FB = contrasts["F-vs-B"]["p"]

    ev6 = (dM_T <= 0) and (dM_F > 0) and (p_FB < ALPHA_BONF)
    ev7 = (dM_T > DELTA_BAR) and (p_TR < ALPHA_PRIMARY) and (abs(dM_R) < FLAT_BAND)
    ev8 = (not ev7) and (dM_F > 0) and (p_FB < ALPHA_BONF) and (O <= O_GATE)
    ev9 = (dM_T > 0) and (p_TR >= ALPHA_PRIMARY)
    ev10 = all(abs(x) < FLAT_BAND for x in (dM_T, dM_F, dM_R))

    evidence = {"step6_cond": ev6, "step7_cond": ev7, "step8_cond": ev8,
                "step9_cond": ev9, "step10_cond": ev10,
                "O": O, "O_le_0.5": (O <= O_GATE) if O == O else False,
                "n_pop": n_pop, "dM_T": dM_T, "dM_F": dM_F, "dM_R": dM_R}
    if ev6:
        verdict, step = "PIVOT", 6
    elif ev7:
        verdict, step = "CONTINUE", 7
    elif ev8:
        verdict, step = "PIVOT", 8
    elif ev9:
        verdict, step = "KILL", 9
    elif ev10:
        verdict, step = "KILL", 10
    else:
        verdict, step = "PIVOT", 11
    return verdict, step, evidence, contrasts
