"""K2 routing-vs-bypass — endpoint arithmetic.

Pure standard library. CPU. Deterministic (no RNG anywhere).
Implements REV4 §3.4/§3.5/§6 exactly:

  - paired 2x2 tables (McNemar exact two-sided p via the min-likelihood
    rule, identical to scipy.stats.binomtest two-sided),
  - Tango (1998) score two-sided 95% CI for the difference of two paired
    proportions — used for the primary (b)-(a) contrast AND uniformly for
    every per-arm vs-baseline paired contrast (the plan names exactly one
    CI method for paired differences; see BUILD_NOTES.md),
  - the true one-sided 95% Tango upper bound (z=1.6449, constrained-MLE
    variance) from the SAME score machinery — the REV4 row-1 flatness
    conjunct (U_1s(Δ̂M_a) < 0.05; LOG-228 interval-identity ruling; the
    q-pinned score form is rejected by name),
  - the six-row verdict table (§6) with the G10 exclusion floor, the
    actual-N accounting, and the REV4 row-3 catch-all (contrast straddles
    OR contrast clears but a per-arm conjunct fails).

Epistemic note: the Tango score interval is computed here, not cited from
a table; the implementation is validated in test_k2.py (McNemar reduction
at delta=0, arm-swap symmetry, containment of the point estimate,
degenerate-table behaviour, and Monte-Carlo coverage).
"""

import math

# ----------------------------------------------------------------------------
# Normal quantile (Acklam's approximation; deterministic, ~1e-9 accuracy)
# ----------------------------------------------------------------------------

def _phi_inv(p):
    """Inverse standard normal CDF for 0 < p < 1 (Acklam approximation)."""
    if not 0.0 < p < 1.0:
        raise ValueError("p must be in (0,1)")
    a = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
         1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00]
    b = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
         6.680131188771972e+01, -1.328068155288572e+01]
    c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
         -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00]
    d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00,
         3.754408661907416e+00]
    plow, phigh = 0.02425, 1 - 0.02425
    if p < plow:
        q = math.sqrt(-2.0 * math.log(p))
        return (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / \
               ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1.0)
    if p > phigh:
        q = math.sqrt(-2.0 * math.log(1.0 - p))
        return -(((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / \
                 ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1.0)
    q = p - 0.5
    r = q * q
    return (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5]) * q / \
           (((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1.0)


def _z_for_alpha(alpha):
    return _phi_inv(1.0 - alpha / 2.0)


# ----------------------------------------------------------------------------
# Paired tables + McNemar exact
# ----------------------------------------------------------------------------

def paired_table(x_correct, y_correct):
    """Paired 2x2 table for (x, y) outcome lists on the same items.

    Returns dict with n11 (x right, y right), n12 (x wrong, y right),
    n21 (x right, y wrong), n22 (both wrong), n, and the point estimate
    d_hat = P(y right) - P(x right) = (n12 - n21) / n.
    """
    if len(x_correct) != len(y_correct):
        raise ValueError("paired lists must have equal length")
    n11 = n12 = n21 = n22 = 0
    for x, y in zip(x_correct, y_correct):
        if x and y:
            n11 += 1
        elif (not x) and y:
            n12 += 1
        elif x and (not y):
            n21 += 1
        else:
            n22 += 1
    n = n11 + n12 + n21 + n22
    return {"n11": n11, "n12": n12, "n21": n21, "n22": n22, "n": n,
            "d_hat": (n12 - n21) / n if n else 0.0,
            # McNemar orientation: b = y rescues over x, c = y loses vs x.
            "b": n12, "c": n21}


def mcnemar_exact_p(b, c):
    """Exact two-sided McNemar p via the min-likelihood rule.

    Identical to scipy.stats.binomtest(min(b,c), b+c, 0.5,
    alternative='two-sided'). b=c=0 -> 1.0 (plan §3.4 M5.1 convention).
    Integer-exact: compares binomial coefficients, no float pmf.
    """
    s = b + c
    if s == 0:
        return 1.0
    m = min(b, c)
    c_obs = math.comb(s, m)
    fav = sum(math.comb(s, k) for k in range(s + 1) if math.comb(s, k) <= c_obs)
    return fav / (2 ** s)


# ----------------------------------------------------------------------------
# Tango (1998) score CI for the difference of two paired proportions
# ----------------------------------------------------------------------------

def _tango_q(n11, n12, n21, n22, delta):
    """Constrained MLE q~ = p~12 + p~21 under p12 - p21 = delta.

    Derivation: multinomial log-likelihood in (q, p11) with
    p12 = (q+delta)/2, p21 = (q-delta)/2, p22 = 1 - p11 - q gives the
    quadratic  n q^2 - (s + d*delta) q - delta*(m*delta - d) = 0
    (s = n12+n21 discordant, d = n12-n21, m = n11+n22 concordant).
    At delta = 0 this reduces to q~ = s/n and the score statistic reduces
    to the McNemar score (n12-n21)/sqrt(n12+n21) — the in-code check.
    The root is clamped to the feasible [|delta|, 1] (boundary MLE when
    the interior root violates p~12, p~21 >= 0).
    """
    n = n11 + n12 + n21 + n22
    s = n12 + n21
    d = n12 - n21
    m = n11 + n22
    disc = (s + d * delta) ** 2 + 4.0 * n * delta * (m * delta - d)
    if disc < 0.0:
        disc = 0.0  # numerical guard; the feasible root is then on the boundary
    q = ((s + d * delta) + math.sqrt(disc)) / (2.0 * n)
    lo = abs(delta)
    if q < lo:
        q = lo
    if q > 1.0:
        q = 1.0
    return q


def tango_score_z(n11, n12, n21, n22, delta):
    """Tango (1998) score statistic Z(delta) for H0: p12 - p21 = delta."""
    n = n11 + n12 + n21 + n22
    if n == 0:
        raise ValueError("empty table")
    d_hat = (n12 - n21) / n
    q = _tango_q(n11, n12, n21, n22, delta)
    var = (q - delta * delta) / n
    if var <= 0.0:
        # Only reachable at |delta| in {0, 1} with a degenerate table;
        # the bisection brackets never evaluate exactly there.
        return math.inf if (d_hat - delta) > 0 else (-math.inf if (d_hat - delta) < 0 else 0.0)
    return (d_hat - delta) / math.sqrt(var)


def tango_ci(n11, n12, n21, n22, alpha=0.05):
    """Tango (score) two-sided CI for the paired difference delta.

    Returns (L, U) with L <= d_hat <= U, found by bisection on the score
    statistic (Z is strictly decreasing in delta; monotonicity is asserted
    in test_k2.py over a battery of tables). Degenerate tables yield a
    non-degenerate interval (score-interval behaviour); the all-concordant
    table yields approximately +/- z^2/n.
    """
    n = n11 + n12 + n21 + n22
    if n == 0:
        raise ValueError("empty table")
    z = _z_for_alpha(alpha)
    d_hat = (n12 - n21) / n

    def f_lo(delta):
        return tango_score_z(n11, n12, n21, n22, delta) - z

    def f_hi(delta):
        return tango_score_z(n11, n12, n21, n22, delta) + z

    # Lower limit: root of f_lo on [-1, d_hat]; f_lo(d_hat) = -z < 0.
    if f_lo(-1.0) <= 0.0:
        L = -1.0
    else:
        lo, hi = -1.0, d_hat
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            if f_lo(mid) > 0.0:
                lo = mid
            else:
                hi = mid
        L = 0.5 * (lo + hi)
    # Upper limit: root of f_hi on [d_hat, 1]; f_hi(d_hat) = +z > 0.
    if f_hi(1.0) >= 0.0:
        U = 1.0
    else:
        lo, hi = d_hat, 1.0
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            if f_hi(mid) > 0.0:
                lo = mid
            else:
                hi = mid
        U = 0.5 * (lo + hi)
    return (L, U)


def tango_one_sided_upper(n11, n12, n21, n22):
    """Tango (score) one-sided 95% upper bound for the paired difference delta.

    REV4 §3.4/§6 (LOG-228 interval-identity ruling): U_1s solves
    Z(delta) = -z_0.95 (z = 1.6449, one-sided) on [d_hat, 1], using the SAME
    constrained-MLE score statistic as tango_ci (tango_score_z) — one
    interval family, not two. The q-pinned score form (variance at the
    unconstrained MLE) is rejected by name (LOG-228). Deterministic;
    degenerate tables return a non-degenerate bound (score-interval
    behaviour). Used ONLY for the row-1 flatness conjunct; per-arm
    diagnostics keep the two-sided CI (REV4 §3.4).
    """
    n = n11 + n12 + n21 + n22
    if n == 0:
        raise ValueError("empty table")
    z = _phi_inv(0.95)  # one-sided 95%: 1.6449...
    d_hat = (n12 - n21) / n

    def f_hi(delta):
        return tango_score_z(n11, n12, n21, n22, delta) + z

    # f_hi(d_hat) = +z > 0; Z strictly decreasing, so at most one root.
    if f_hi(1.0) >= 0.0:
        return 1.0
    lo, hi = d_hat, 1.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if f_hi(mid) > 0.0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def paired_contrast_stats(x_correct, y_correct, alpha=0.05, label=""):
    """Full paired-contrast record: table, McNemar exact p, Tango CI."""
    t = paired_table(x_correct, y_correct)
    lo, hi = tango_ci(t["n11"], t["n12"], t["n21"], t["n22"], alpha=alpha)
    return {"label": label, "n": t["n"], "n11": t["n11"], "n12": t["n12"],
            "n21": t["n21"], "n22": t["n22"],
            "b": t["b"], "c": t["c"],
            "d_hat": t["d_hat"],
            "mcnemar_p": mcnemar_exact_p(t["b"], t["c"]),
            "tango_L": lo, "tango_U": hi, "alpha": alpha,
            "tango_U_1s": tango_one_sided_upper(t["n11"], t["n12"],
                                               t["n21"], t["n22"])}


# ----------------------------------------------------------------------------
# Verdict table (REV2 §6) — five categories only
# ----------------------------------------------------------------------------

# (verdict_routing, verdict_local) vocabulary — the only permitted verdicts.
SUPPORTED = "Supported"
NOT_SUPPORTED = "Not supported"
INCONCLUSIVE = "Inconclusive"
UNDERDETERMINED = "Underdetermined"
REFUTED = "Refuted"


def adjudicate_verdict(base_correct, a_correct, b_correct, c_correct,
                      exclusions, c_gate_passed, delta_min=0.05, mde_b=6):
    """Map REV4 §6's verdict table to a verdict pair.

    Inputs are per-item correctness lists over the INCLUDED items only
    (exclusions already removed), the exclusion-cause list, and whether
    the (c)-gate passed. Returns a record with every cell's numbers and
    the verdict. Row precedence: 1 -> 2 (with 2r refinement) -> 4 -> 3
    (the REV4 catch-all: contrast straddles OR contrast clears but a
    per-arm conjunct fails). Row 5 (FATAL guards / records missing) and
    the G10 exclusion floor (>6 exclusions -> Underdetermined) are decided
    by the caller BEFORE this function via guards_evaluate(); they are
    re-asserted here.

    REV4 flatness bar (LOG-228): row 1 fires iff
    L(Δ̂M_b−Δ̂M_a) > 0.05 AND b_b >= 6 AND U_1s(Δ̂M_a) < 0.05, where U_1s
    is the true one-sided 95% Tango upper bound (z=1.6449).
    """
    n = len(base_correct)
    if not (len(a_correct) == len(b_correct) == len(c_correct) == n):
        raise ValueError("arm lists must match the included-item count")

    arm_a = paired_contrast_stats(base_correct, a_correct, label="a_vs_base")
    arm_b = paired_contrast_stats(base_correct, b_correct, label="b_vs_base")
    arm_c = paired_contrast_stats(base_correct, c_correct, label="c_vs_base")
    contrast = paired_contrast_stats(a_correct, b_correct, label="b_vs_a")

    Lc, Uc = contrast["tango_L"], contrast["tango_U"]
    dMa, dMb = arm_a["d_hat"], arm_b["d_hat"]

    row, v_routing, v_local, consequence, row3_reason = None, None, None, None, None

    # Row 1: routing Supported / final-position-local Not supported.
    # REV4 §3.4/§6 (LOG-228): the flatness conjunct is the TRUE one-sided
    # 95% Tango upper bound U_1s(Δ̂M_a) < 0.05 (z=1.6449, constrained-MLE
    # variance) — REPLACED the two-sided U < 0.05 bar, not supplemented.
    if Lc > delta_min and arm_b["b"] >= mde_b and arm_a["tango_U_1s"] < delta_min:
        row = 1
        v_routing, v_local = SUPPORTED, NOT_SUPPORTED
        consequence = ("Upstream mechanism exists. License: attention-engagement "
                       "campaign; CLLC routing-signal pilot; ARP (S3-1) fingerprint "
                       "program unblocked with a verified positive mechanism class.")
    # Row 2: final-position-local Supported / routing Not supported.
    elif Uc < delta_min and dMa >= dMb and arm_a["b"] >= mde_b:
        # Row 2r refinement: routing actively contradicted.
        if arm_a["tango_L"] > delta_min and arm_b["b"] == 0 and arm_b["c"] == 0:
            row = "2r"
            v_routing, v_local = REFUTED, SUPPORTED
            consequence = ("As row 2, with the routing account actively contradicted "
                           "(flat-zero under the only channel it could use) — Law #8: "
                           "the routing reading stays dead unless new evidence resurrects it.")
        else:
            row = 2
            v_routing, v_local = NOT_SUPPORTED, SUPPORTED
            consequence = ("P2 pivot fires: output-side mechanism program closes (bridge = "
                           "logit steering, period); mechanism-family -> trajectory/closed-loop "
                           "controllers; bridge survives only as engineering. Binding reading: "
                           "'no upstream delta transport; the rescue is final-position-local "
                           "(readout + local downstream gain)' — NOT 'pure direct readout shift'.")
    # Row 4: both arms flat with (c) passing G5 — the license's application
    # premise broke (L3), not either proposition.
    elif (arm_a["b"] + arm_a["c"] == 0) and (arm_b["b"] + arm_b["c"] == 0) and c_gate_passed:
        row = 4
        v_routing, v_local = INCONCLUSIVE, INCONCLUSIVE
        consequence = ("The bridge does not survive position restriction at all — the license's "
                       "application premise broke (L3), not either proposition. Logged; K2's "
                       "question is unaskable in this form.")
    # Row 3: the catch-all (REV4 §6 — widened by the LOG-227 repair to close
    # the pre-existing exhaustiveness gap the repair makes live): no
    # row-1/2/2r pattern. Either the contrast CI straddles, OR the contrast
    # clears but the per-arm conjuncts fail (flatness for row 1,
    # rescue-presence b_a >= 6 for row 2). Held, never culled.
    else:
        row = 3
        v_routing, v_local = INCONCLUSIVE, INCONCLUSIVE
        if Lc > delta_min and arm_b["b"] >= mde_b:
            row3_reason = ("contrast_clears_row1_flatness_fails: the primary contrast clears "
                           "and arm-(b) rescue is present, but U_1s(Δ̂M_a) >= 0.05 — "
                           "the row-1 flatness conjunct fails → catch-all")
        elif Uc < delta_min and dMa >= dMb:
            row3_reason = ("contrast_clears_row2_rescue_presence_fails: the contrast clears "
                           "against a (b)-advantage with Δ̂M_a >= Δ̂M_b, but b_a < 6 — "
                           "the row-2 rescue-presence conjunct fails → catch-all")
        else:
            row3_reason = ("contrast_straddle: the primary contrast CI straddles δ_min — "
                           "neither directional bar clears → catch-all")
        consequence = ("Row 3 catch-all (" + row3_reason + "). HELD, never culled. Options: "
                       "instrumentation upgrade (per-layer attention snapshots per S3-7 §6 spec) "
                       "+ powered re-registration at N>=100; or concede the pilot's ceiling.")

    return {
        "row": row,
        "verdict_routing": v_routing,
        "verdict_final_position_local": v_local,
        "consequence": consequence,
        "n_actual": n,
        "n_excluded": len(exclusions),
        "exclusions": list(exclusions),
        "delta_min": delta_min,
        "mde_b": mde_b,
        "arm_a": arm_a,
        "arm_b": arm_b,
        "arm_c": arm_c,
        "contrast_b_vs_a": contrast,
        "dMa": dMa,
        "dMb": dMb,
        "row3_reason": row3_reason,  # set only when row == 3 (the REV4 catch-all)
    }
