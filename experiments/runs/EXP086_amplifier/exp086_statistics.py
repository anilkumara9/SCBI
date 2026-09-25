#!/usr/bin/env python3
"""EXP086 statistics: exact one-sided McNemar, Tango 95% CI for the paired
difference of proportions, ĉ / exceedance, and the signed ledger (§7).

All functions are pure-Python (stdlib only) and deterministic. They operate
on integer count tables and float vectors — no model, no weights, no torch.

- mcnemar_exact_one_sided(n10, n01): exact binomial one-sided p for the
  paired comparison (§7 primary test).
- tango_ci(n10, n01, n00, n11): Tango (1998) score 95% CI for
  Delta = p10 - p01, by exact inversion of the score test with constrained
  MLEs under H0: Delta = delta0 (solved in closed form via a quadratic;
  endpoints found by bisection). Raises NonTestableDataError when the
  discordant count is 0 (never silently returns a degenerate interval).
- c_hat(alphas), exceedance(alphas): §2 D6 diagnostic + §7 kill-first prong.
- signed_ledger(baseline_correct, arm_correct): per-arm (b, c) =
  (wrong->right, right->wrong) vs baseline + anti-steerable fraction
  c/(b+c) (§7 P3 demand). The flag is a REPORTING rule (loud in the detail
  string); it never changes the verdict by itself.
"""

import math

import exp086_guards as G

Z95 = G.Z_95


# ---------------------------------------------------------------------------
# Exact one-sided McNemar (§7)
# ---------------------------------------------------------------------------

def mcnemar_exact_one_sided(n10, n01):
    """One-sided exact McNemar p-value.

    n10 = #{A correct, B correct=0} (v̂_1-only wins), n01 = #{A wrong, B right}
    for the arm-pair (A=v̂_1, B=v̂_rand) at the primary norm. H0: no
    directional difference; H1: A better than B. Exact:
        p = sum_{k=n10}^{n} C(n,k) 2^{-n},  n = n10 + n01.
    Raises NonTestableDataError if n == 0 (no discordant pairs).
    """
    n10, n01 = int(n10), int(n01)
    if n10 < 0 or n01 < 0:
        raise ValueError(f"counts must be non-negative (got {n10}, {n01})")
    n = n10 + n01
    if n == 0:
        raise G.NonTestableDataError(
            "McNemar: zero discordant pairs — the comparison is not testable "
            "(loud halt; the apparatus/headroom guards should have fired first)."
        )
    p = 0.0
    for k in range(n10, n + 1):
        p += math.comb(n, k) * (0.5 ** n)
    return min(1.0, p)


# ---------------------------------------------------------------------------
# Tango 95% CI for the paired difference Delta = p10 - p01
# ---------------------------------------------------------------------------

def _constrained_mle(delta0, n10, n01, nc):
    """Constrained MLEs (p10~, p01~) under p10 - p01 = delta0.

    Maximizes l = n10 log p10 + n01 log p01 + nc log(1 - p10 - p01),
    nc = n00 + n11, with t = p01, p10 = t + delta0, pc = 1 - 2t - delta0.
    dl/dt = 0 gives the quadratic (derivation in BUILD_NOTES §6):
        2n t^2 - [n10(1-u) + n01(1-3u) - 2 nc u] t - n01 u (1-u) = 0,
    u = delta0, n = n10 + n01 + nc. The admissible root has
    0 <= t <= 1, 0 <= t+u <= 1, 1 - 2t - u >= 0.
    Returns (p10_tilde, p01_tilde). Raises NonTestableDataError if no
    admissible root exists for this delta0.
    """
    n = n10 + n01 + nc
    u = float(delta0)
    if not (-1.0 < u < 1.0):
        raise G.NonTestableDataError(f"Tango: delta0={u} outside (-1, 1)")
    a = 2.0 * n
    b = -(n10 * (1.0 - u) + n01 * (1.0 - 3.0 * u) - 2.0 * nc * u)
    c = -n01 * u * (1.0 - u)
    disc = b * b - 4.0 * a * c
    if disc < 0:
        raise G.NonTestableDataError(
            f"Tango: negative discriminant at delta0={u} (disc={disc})"
        )
    sq = math.sqrt(disc)
    best = None
    for sgn in (1.0, -1.0):
        t = (-b + sgn * sq) / (2.0 * a)
        p01 = t
        p10 = t + u
        pc = 1.0 - 2.0 * t - u
        if -1e-12 <= p01 <= 1.0 + 1e-12 and -1e-12 <= p10 <= 1.0 + 1e-12 \
                and pc >= -1e-12:
            p01 = min(1.0, max(0.0, p01))
            p10 = min(1.0, max(0.0, p10))
            best = (p10, p01)
            break
    if best is None:
        raise G.NonTestableDataError(
            f"Tango: no admissible constrained MLE at delta0={u}"
        )
    return best


def _tango_score(delta0, n10, n01, n00, n11):
    """Tango score statistic T(delta0) for H0: Delta = delta0."""
    n = n10 + n01 + n00 + n11
    nc = n00 + n11
    p10t, p01t = _constrained_mle(delta0, n10, n01, nc)
    ph10 = n10 / n
    ph01 = n01 / n
    var = (p10t + p01t - (p10t - p01t) ** 2) / n
    if var <= 0:
        raise G.NonTestableDataError(
            f"Tango: non-positive score variance at delta0={delta0}"
        )
    return (ph10 - ph01 - delta0) / math.sqrt(var)


def tango_ci(n10, n01, n00, n11, z=Z95, tol=1e-10):
    """Tango 95% CI for Delta = p10 - p01 by score-test inversion.

    Returns (lo, hi) with T(lo) = +z, T(hi) = -z (T decreasing in delta0).
    Bisection on [-1+eps, 1-eps]; endpoints are bracketed outward from the
    point estimate until the score crosses +/-z. Raises NonTestableDataError
    on degenerate inputs (e.g. zero discordant pairs).
    """
    for v, nm in ((n10, "n10"), (n01, "n01"), (n00, "n00"), (n11, "n11")):
        if int(v) < 0:
            raise ValueError(f"{nm} must be non-negative")
    n10, n01, n00, n11 = int(n10), int(n01), int(n00), int(n11)
    n = n10 + n01 + n00 + n11
    if n == 0:
        raise G.NonTestableDataError("Tango: empty table")
    if n10 + n01 == 0:
        raise G.NonTestableDataError(
            "Tango: zero discordant pairs — difference not testable "
            "(loud halt; guards should have fired first)."
        )
    ph = n10 / n - n01 / n  # point estimate

    def T(u):
        return _tango_score(u, n10, n01, n00, n11)

    eps = 1e-9

    def find_endpoint(target, side):
        # side=-1: lower (T = +z); side=+1: upper (T = -z). T decreasing.
        lo, hi = (-1.0 + eps, 1.0 - eps)
        # bracket: step outward from the point estimate
        if side == -1:
            a, b = ph, ph
            ta = T(a)
            step = 0.05
            while ta < target and a > -1.0 + eps:
                a = max(-1.0 + eps, a - step)
                ta = T(a)
                step *= 1.5
            # now T(a) >= target >= T(b)=T(ph) (T(ph) has sign of -ph...);
            # ensure bracket: T(a) >= target and T(b) <= target
            b = ph
            if not (T(a) >= target >= T(b)):
                # fallback: full-range bracket
                a, b = -1.0 + eps, 1.0 - eps
        else:
            a, b = ph, ph
            tb = T(b)
            step = 0.05
            while tb > -target and b < 1.0 - eps:
                b = min(1.0 - eps, b + step)
                tb = T(b)
                step *= 1.5
            a = ph
            if not (T(a) >= -target >= T(b)):
                a, b = -1.0 + eps, 1.0 - eps
        want = target if side == -1 else -target
        for _ in range(200):
            m = 0.5 * (a + b)
            tm = T(m)
            if abs(tm - want) < 1e-12:
                return m
            if tm > want:
                a = m
            else:
                b = m
            if b - a < tol:
                return 0.5 * (a + b)
        return 0.5 * (a + b)

    lo = find_endpoint(z, -1)
    hi = find_endpoint(z, +1)
    if lo > hi:  # numerical safety; never silently swap semantics
        raise G.NonTestableDataError(
            f"Tango: inverted endpoints (lo={lo} > hi={hi}) — numerical failure"
        )
    return lo, hi


# ---------------------------------------------------------------------------
# ĉ diagnostic + exceedance (§2 D6, §7 V5/V10)
# ---------------------------------------------------------------------------

def c_hat(alphas):
    """ĉ = mean_i |<v̂_1(x_i), n̂(x_i)>| over unit vectors (D6)."""
    alphas = list(alphas)
    if not alphas:
        raise G.NonTestableDataError("c_hat: empty input")
    return sum(abs(a) for a in alphas) / len(alphas)


def exceedance(alphas, bar=G.CHAT_BAR):
    """E = P(|<v̂_1, n̂>| > 0.1): fraction of items above the bar."""
    alphas = list(alphas)
    if not alphas:
        raise G.NonTestableDataError("exceedance: empty input")
    return sum(1 for a in alphas if abs(a) > bar) / len(alphas)


# ---------------------------------------------------------------------------
# Signed ledger (§7 P3 demand)
# ---------------------------------------------------------------------------

ANTI_STEERABLE_FLAG_FRAC = 0.2  # reporting flag bar (NOT a verdict bar)


def signed_ledger(baseline_correct, arm_correct):
    """Per-arm (b, c) = (wrong->right, right->wrong) vs the baseline.

    baseline_correct, arm_correct: equal-length 0/1 (or bool) sequences.
    Returns dict with b, c, n_changed, anti_steerable_frac = c/(b+c)
    (None if b+c == 0), and the reporting flag (frac > 0.2).

    [INTERPRETATION] The flag is a reporting rule: "a v̂_1 win driven by
    c > 0 elsewhere is flagged in the ledger even if Delta > 0" (§7). It is
    recorded in the run detail string; it does NOT alter the verdict.
    """
    if len(baseline_correct) != len(arm_correct):
        raise ValueError("baseline/arm correctness lengths differ")
    b = sum(1 for x, y in zip(baseline_correct, arm_correct) if not x and y)
    c = sum(1 for x, y in zip(baseline_correct, arm_correct) if x and not y)
    n_changed = b + c
    frac = (c / n_changed) if n_changed else None
    return {
        "b_wrong_to_right": b,
        "c_right_to_wrong": c,
        "n_changed": n_changed,
        "anti_steerable_frac": frac,
        "flagged": (frac is not None and frac > ANTI_STEERABLE_FLAG_FRAC),
    }
