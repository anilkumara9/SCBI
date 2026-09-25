#!/usr/bin/env python3
"""EXP087 statistics: the translation-signature estimators and endpoints.

All registered quantities (§2):
  μ̂            mean per-item C2 margin shift Δm_i (apparatus envelope)
  min Δm_i     strict-positivity check (R1)
  P            predicted rescue set {i : m0,i < 0 < m0,i + Δm_i}
  Hamming      |P Δ observed rescues| (R2 — the primary endpoint)
  C3 ⊆ C2      boundary-band subset (R3)
  corr(Δm,c)   one-sided partial-replication test (R4)
  4σ flag      LayerNorm-saturation diagnostic (§3 guard ii; §8 item 4)

The one-sided p-value for Pearson's r uses the exact t-distribution
(t = r√((n−2)/(1−r²)), one-sided p = P(T > t)) via the regularized
incomplete beta function — deterministic, no scipy dependency.
"""

import math

import exp087_guards as G


# ---------------------------------------------------------------------------
# Basic estimators
# ---------------------------------------------------------------------------

def mean(xs):
    xs = list(xs)
    if not xs:
        raise G.BundleError("statistics: empty input to mean()")
    return sum(xs) / len(xs)


def sample_std(xs):
    """Sample standard deviation (ddof=1)."""
    xs = list(xs)
    n = len(xs)
    if n < 2:
        raise G.BundleError("statistics: need >= 2 points for sample_std()")
    m = mean(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (n - 1))


def mu_hat(dm_c2):
    """The μ̂ estimator: mean over the N=60 FIXED benchmark items."""
    return mean(dm_c2)


def envelope_check(mu):
    """R5 apparatus envelope: μ̂ ∈ [0.649, 0.849]."""
    return G.ENVELOPE_LO <= mu <= G.ENVELOPE_HI


def strict_positivity(dm_c2):
    """R1 quantitative arm: min_i Δm_i > 0."""
    return min(dm_c2) > 0


# ---------------------------------------------------------------------------
# Rescue-set identity (R2 — the primary endpoint)
# ---------------------------------------------------------------------------

def predicted_rescue_set(records):
    """P = {i : m0,i < 0 < m0,i + Δm_i} — parameter-free prediction from
    the C1+C2 logs. records: list of dicts with 'm0', 'dm_c2'."""
    return {i for i, r in enumerate(records)
            if r["m0"] < 0 < r["m0"] + r["dm_c2"]}


def observed_rescues(records, arm_correct_key):
    """{i : base wrong and <arm> correct}, from the logged decisions."""
    return {i for i, r in enumerate(records)
            if not r["base_correct"] and r[arm_correct_key]}


def hamming_distance(set_a, set_b):
    return len(set_a.symmetric_difference(set_b))


def subset_check(sub, sup):
    """R3: rescued_C3 ⊆ rescued_C2. Returns (holds, violators)."""
    viol = sorted(sub - sup)
    return (len(viol) == 0, viol)


# ---------------------------------------------------------------------------
# McNemar cells (§3 guard iii; archived b=8, c=0 for C2)
# ---------------------------------------------------------------------------

def mcnemar_cells(base_correct, mod_correct):
    """b = base-wrong→mod-correct (rescues); c = base-correct→mod-wrong
    (corruptions)."""
    b = sum(1 for x, y in zip(base_correct, mod_correct) if not x and y)
    c = sum(1 for x, y in zip(base_correct, mod_correct) if x and not y)
    return b, c


# ---------------------------------------------------------------------------
# Pearson correlation + exact one-sided t p-value (R4)
# ---------------------------------------------------------------------------

def pearson_r(xs, ys):
    xs, ys = list(xs), list(ys)
    if len(xs) != len(ys) or len(xs) < 3:
        raise G.BundleError("statistics: pearson_r needs >= 3 paired points")
    n = len(xs)
    mx, my = mean(xs), mean(ys)
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    if sxx == 0 or syy == 0:
        raise G.BundleError("statistics: pearson_r undefined (zero variance)")
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    r = sxy / math.sqrt(sxx * syy)
    return max(-1.0, min(1.0, r))


def _ibeta_cf(a, b, x):
    """Continued fraction for the incomplete beta function
    (Numerical Recipes betacf)."""
    MAXIT, EPS, FPMIN = 200, 3e-14, 1e-300
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < FPMIN:
        d = FPMIN
    d = 1.0 / d
    h = d
    for m in range(1, MAXIT + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < FPMIN:
            d = FPMIN
        c = 1.0 + aa / c
        if abs(c) < FPMIN:
            c = FPMIN
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < FPMIN:
            d = FPMIN
        c = 1.0 + aa / c
        if abs(c) < FPMIN:
            c = FPMIN
        d = 1.0 / d
        delt = d * c
        h *= delt
        if abs(delt - 1.0) < EPS:
            break
    return h


def ibeta_reg(a, b, x):
    """Regularized incomplete beta function I_x(a, b)."""
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    if not (a > 0 and b > 0):
        raise G.BundleError("statistics: ibeta_reg needs a, b > 0")
    lbeta = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
    if x < (a + 1.0) / (a + b + 2.0):
        bt = math.exp(lbeta + a * math.log(x) + b * math.log(1.0 - x))
        return bt * _ibeta_cf(a, b, x) / a
    bt = math.exp(lbeta + a * math.log(x) + b * math.log(1.0 - x))
    return 1.0 - bt * _ibeta_cf(b, a, 1.0 - x) / b


def corr_one_sided_pvalue(r, n):
    """One-sided p-value for H1: corr > 0, via the t-distribution:
    t = r√((n−2)/(1−r²)), p = P(T_df > t), df = n−2."""
    if n < 4:
        raise G.BundleError("statistics: need n >= 4 for corr p-value")
    if r >= 1.0:
        return 0.0
    if r <= -1.0:
        return 1.0
    df = n - 2
    t = r * math.sqrt(df / (1.0 - r * r))
    if t <= 0.0:
        # p >= 0.5 for non-positive t (computed exactly for completeness)
        x = df / (df + t * t)
        return 1.0 - 0.5 * ibeta_reg(df / 2.0, 0.5, x)
    x = df / (df + t * t)
    return 0.5 * ibeta_reg(df / 2.0, 0.5, x)


def corr_replication_test(dm_c2, c_vals):
    """R4: PASS = one-sided p < 0.05 for corr(Δm_i, c_i) > 0.
    Any other outcome — including a non-significant positive corr —
    is a break (→ CONTINUE). Returns (r, p_one_sided, passes)."""
    r = pearson_r(dm_c2, c_vals)
    p = corr_one_sided_pvalue(r, len(dm_c2))
    return r, p, (p < G.CORR_P_BAR)


# ---------------------------------------------------------------------------
# LayerNorm-saturation diagnostic (§3 guard ii; §8 item 4 resolution)
# ---------------------------------------------------------------------------

def layernorm_saturation_flag(dm_c2):
    """Flag items with |Δm_i − μ̂| > 4σ̂_ε (σ̂_ε = sample std, ddof=1).

    DIAGNOSTIC ONLY: feeds the breaking-point analysis; it does not alter
    any verdict row by itself (§8 item 4 resolution — see BUILD_NOTES.md).
    Returns (flagged_indices, mu, sigma)."""
    dm = list(dm_c2)
    mu = mean(dm)
    sigma = sample_std(dm)
    flagged = [i for i, v in enumerate(dm) if abs(v - mu) > 4.0 * sigma]
    return flagged, mu, sigma
