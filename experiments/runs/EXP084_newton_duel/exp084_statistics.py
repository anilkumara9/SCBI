"""EXP084 statistics: exact Wilcoxon signed-rank and Hodges-Lehmann CI.

All tests are pre-registered in signed §5:
- Sensitivity precondition (F2, binding): one-sided Wilcoxon (ΔM_a − ΔM_c) > 0
  at p ≤ 0.10. Fail -> INVALID/UNINFORMATIVE-PROXY, never KILL.
- Arm contrasts (a)-(d): one-sided Wilcoxon p ≤ 0.05.
- KILL effect-size prong (F10): two-sided 95% Hodges-Lehmann CI for the
  median difference; KILL requires CI upper < +0.01 margin units.

Exactness: the Wilcoxon signed-rank null distribution is computed by exact DP
(subset-sum over ranks), not a normal approximation. Valid for n ≤ 24 with
no ties in |d_i| (the runner's margin gains are continuous; the evaluator
tests use tie-free fixtures). Zero differences are LOUD-HALTED by the
runner's pre-validation (`assert_testable_differences`, LOG-266 binding —
fail loud, never silently drop, never tie-break) before they ever reach the
Wilcoxon/HL internals; the drop path in `wilcoxon_signed_rank_greater` below
is defense-in-depth for direct callers only. n_eff < 6 raises ValueError
(exact table too coarse to be decision-relevant at the pre-registered bars).
"""

import math

KILL_BAR = 0.01  # margin units; HL CI upper must be < this for KILL (§7, F10)


class NonTestableDataError(ValueError):
    """Loud halt: paired differences are not testable by the exact methods.

    Raised when a contrast's differences contain a zero (exact Wilcoxon/HL
    silently drop zeros) or a tie in |d_i| (exact rank DP assumes distinct
    ranks). The signed protocol is silent on tie-breaking; per the LOG-266
    binding stage-2 condition the loop fails LOUD here — never silently
    drops, never applies a randomized or ad-hoc tie-break. Ties are
    measure-zero for continuous margin gains, so this halt indicates a
    degenerate apparatus, not a statistical subtlety.
    """


def assert_testable_differences(diffs, label="contrast"):
    """Fail loud unless `diffs` are testable by the exact Wilcoxon/HL.

    Raises NonTestableDataError if any difference is exactly zero or any
    two |d_i| tie. Deterministic: no tie-breaking is ever applied.
    Returns the number of (nonzero, untied) differences.
    """
    diffs = list(diffs)
    if any(d == 0.0 for d in diffs):
        raise NonTestableDataError(
            f"{label}: zero difference(s) present — exact Wilcoxon/HL would "
            "silently drop them; halting loud instead (LOG-266 binding)."
        )
    abs_d = [abs(d) for d in diffs]
    if len(set(abs_d)) != len(abs_d):
        raise NonTestableDataError(
            f"{label}: tie in |d_i| detected — exact rank DP requires "
            "distinct ranks; halting loud instead of tie-breaking."
        )
    return len(diffs)


def assert_no_ties(xs, label="sample"):
    """Fail loud if `xs` contains any tied values (Spearman exact table).

    The exact Spearman D-distribution assumes untied ranks (protocol uses
    continuous |κ̂_dir| and margin gains; ties are measure-zero).
    """
    xs = list(xs)
    if len(set(xs)) != len(xs):
        raise NonTestableDataError(
            f"{label}: tied values detected — exact Spearman null table "
            "requires untied ranks; halting loud instead of tie-breaking."
        )
    return len(xs)


def median(xs):
    """Sample median. Deterministic: even n averages the two middle values."""
    s = sorted(xs)
    n = len(s)
    if n == 0:
        raise ValueError("median of empty sample")
    mid = n // 2
    if n % 2 == 1:
        return s[mid]
    return (s[mid - 1] + s[mid]) / 2.0


def _wilcoxon_null_dist(n):
    """Exact null distribution of W+ (sum of positive ranks) for n items.

    Returns list `dp` where dp[s] = #{sign assignments with W+ == s}.
    DP: for each rank r=1..n, dp_new[s] += dp[s] + dp[s-r].
    """
    max_s = n * (n + 1) // 2
    dp = [0] * (max_s + 1)
    dp[0] = 1
    for r in range(1, n + 1):
        new = [0] * (max_s + 1)
        for s in range(max_s + 1):
            v = dp[s]
            if v:
                new[s] += v
                if s + r <= max_s:
                    new[s + r] += v
        dp = new
    return dp


def wilcoxon_signed_rank_greater(x, y):
    """One-sided exact Wilcoxon signed-rank p-value for H1: median(x-y) > 0.

    Args:
        x, y: paired sequences (e.g. ΔM_a, ΔM_c for the F2 precondition).

    Returns:
        (p_value, w_plus, n_eff). p = P_null(W+ >= w_obs).
        Ties in |d| raise ValueError (exact DP assumes distinct ranks; use
        tie-free data). Note: the runner pre-validates via
        assert_testable_differences (zeros loud-halt, LOG-266 binding), so
        the zero-drop path below is defense-in-depth for direct callers only.

    Raises:
        ValueError: if n_eff < 6 or a tie in |d_i| is detected.
    """
    if len(x) != len(y):
        raise ValueError("x and y must be paired (same length)")
    diffs = [xi - yi for xi, yi in zip(x, y)]
    nz = [d for d in diffs if d != 0.0]
    n_eff = len(nz)
    if n_eff < 6:
        raise ValueError(f"n_eff={n_eff} < 6: exact Wilcoxon not decision-relevant")
    abs_d = [abs(d) for d in nz]
    if len(set(abs_d)) != n_eff:
        raise ValueError("tie in |d_i| detected: exact rank DP not applicable")
    order = sorted(range(n_eff), key=lambda i: abs_d[i])
    w_plus = sum(r + 1 for r in range(n_eff) if nz[order[r]] > 0)
    dp = _wilcoxon_null_dist(n_eff)
    total = 1 << n_eff
    p = sum(dp[s] for s in range(w_plus, len(dp))) / total
    return p, w_plus, n_eff


def hodges_lehmann_ci(x, y, alpha=0.05):
    """Two-sided (1-alpha) Hodges-Lehmann CI for median(x - y).

    Walsh averages w_ij = (d_i + d_j)/2 for i <= j, sorted; the CI is
    [w_(c+1), w_(m-c)] (1-indexed) = [walsh[c], walsh[m-c-1]] (0-indexed),
    where c is the alpha/2 lower critical value of the exact Wilcoxon
    signed-rank null distribution (P(W+ <= c) <= alpha/2). These are the
    exact test-inversion endpoints (LOG-266 Fix 1: the code previously used
    [walsh[c+1], walsh[m-c-2]], one order statistic too narrow per side —
    anti-fail-safe for the KILL prong).

    Returns:
        (lo, hi, hl_estimator). hl_estimator is the median Walsh average.

    Raises:
        ValueError: on ties in |d_i| or n_eff < 6 (same as Wilcoxon).
    """
    if len(x) != len(y):
        raise ValueError("x and y must be paired (same length)")
    diffs = [xi - yi for xi, yi in zip(x, y)]
    nz = [d for d in diffs if d != 0.0]
    n_eff = len(nz)
    if n_eff < 6:
        raise ValueError(f"n_eff={n_eff} < 6")
    abs_d = [abs(d) for d in nz]
    if len(set(abs_d)) != n_eff:
        raise ValueError("tie in |d_i| detected")
    # Walsh averages
    walsh = []
    for i in range(n_eff):
        for j in range(i, n_eff):
            walsh.append((nz[i] + nz[j]) / 2.0)
    walsh.sort()
    m = len(walsh)
    # critical value c: largest c with P(W+ <= c) <= alpha/2
    dp = _wilcoxon_null_dist(n_eff)
    total = 1 << n_eff
    cum = 0
    c = -1
    for s in range(len(dp)):
        cum += dp[s]
        if cum / total <= alpha / 2:
            c = s
        else:
            break
    # Exact test-inversion endpoints: [walsh[c], walsh[m-c-1]] (0-indexed).
    # Degenerate guard: c == -1 (P(W+ <= 0) > alpha/2, possible at n_eff=6)
    # means the exact interval is [min, max] of the Walsh averages.
    lo = walsh[c] if c >= 0 else walsh[0]
    hi = walsh[m - c - 1] if c >= 0 else walsh[m - 1]
    hl = walsh[m // 2] if m % 2 == 1 else (walsh[m // 2 - 1] + walsh[m // 2]) / 2.0
    return lo, hi, hl


def kill_effect_prong(x, y, bar=KILL_BAR):
    """KILL effect-size prong (F10): True iff HL 95% CI upper < bar.

    x = ΔM_b (Newton gains), y = ΔM_d (GD-costfair gains) over the defined set.
    Returns (fires, ci_lo, ci_hi).
    """
    lo, hi, _ = hodges_lehmann_ci(x, y, alpha=0.05)
    return (hi < bar), lo, hi
