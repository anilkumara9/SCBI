"""EXP083 (R1 RCPA kill pilot) — endpoint arithmetic.

Pure standard library. CPU. Deterministic (no RNG anywhere).
Implements the signed protocol experiments/protocols/EXP083_RCPA_PREREG_SPEC.md
(LOG-257 SIGN) exactly:

  - flip outcomes: outcome(i, arm) = 1 iff wrong at baseline AND right under
    the arm (§4, F7); items right at baseline are structural zeros —
    handled, not subsetted.
  - paired 2x2 table over flip indicators (A_g vs A_r); McNemar orientation:
    b = A_r-only flips (n12), c = A_g-only flips (n21);
    Delta = flip-rate(A_r) - flip-rate(A_g) = (b - c) / N.
  - exact ONE-SIDED McNemar p via the binomial upper tail
    P(Bin(b+c, 0.5) >= b) — the protocol's CONTINUE conjunct
    ("exact one-sided McNemar (binomial) p <= 0.05 in the A_r direction";
    MDE anchor b=6, c=0 -> 0.015625). NOT the two-sided min-likelihood
    form used in K2 — one-sided is pinned here by name.
  - Tango (1998) score two-sided 95% CI for the paired difference
    (program standard), computed from the constrained-MLE score statistic
    (tango_score_z) — the same machinery validated for K2. The evaluator
    test suite reproduces the protocol's canonical table from this code,
    not from trusted library values:
      one-sided 95% upper  0.043147 at N=60 (flat b=c=0)
      two-sided 95%        [-0.0602, +0.0602] at N=60
      one-sided 95% upper  0.045315 at N_final=57 (KILL_flat canonical, R1)
      two-sided 95%        [-0.0631, +0.0631] at N_final=57
      0.056902 (b=c=1 boundary check)
      one-sided McNemar p  0.015625 at b=6, c=0 (MDE anchor)
  - the §8 verdict table with the M1 verdict-precedence order:
    INVALID (i) pre-run SHA-256 vs pinned expected -> (ii) identity arm vs
    archived C1 bit-for-bit -> (iii) guard computation faults;
    then RE-SKIN / KILL_gross / KILL_flat / CONTINUE / HELD.

Epistemic note: every number in the canonical table is computed here, not
cited; test_exp083.py asserts the values to 6dp/4dp from this code path.
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
# Flip outcomes + paired table (EXP083 §4)
# ----------------------------------------------------------------------------

def flip_indicators(baseline_correct, arm_correct):
    """Per-item flip indicator: 1 iff wrong at baseline AND right under arm.

    Items right at baseline are structural zeros (F7) — handled, not
    subsetted. Returns a list of ints in {0, 1}.
    """
    if len(baseline_correct) != len(arm_correct):
        raise ValueError("baseline and arm lists must have equal length")
    return [1 if ((not b) and a) else 0
            for b, a in zip(baseline_correct, arm_correct)]


def paired_flip_table(g_flips, r_flips):
    """Paired 2x2 table over flip indicators: x = A_g flips, y = A_r flips.

    Returns dict with n11 (both flip), n12 (A_r only), n21 (A_g only),
    n22 (neither), n, d_hat = (n12 - n21) / n, and the McNemar orientation
    b = n12 (A_r-only flips), c = n21 (A_g-only flips).
    """
    if len(g_flips) != len(r_flips):
        raise ValueError("paired flip lists must have equal length")
    n11 = n12 = n21 = n22 = 0
    for g, r in zip(g_flips, r_flips):
        if g and r:
            n11 += 1
        elif (not g) and r:
            n12 += 1
        elif g and (not r):
            n21 += 1
        else:
            n22 += 1
    n = n11 + n12 + n21 + n22
    return {"n11": n11, "n12": n12, "n21": n21, "n22": n22, "n": n,
            "d_hat": (n12 - n21) / n if n else 0.0,
            "b": n12, "c": n21}


def mcnemar_one_sided_p(b, c):
    """Exact one-sided McNemar p in the A_r direction.

    P(Bin(b + c, 0.5) >= b) — the binomial upper tail. b = A_r-only flips,
    c = A_g-only flips. b + c = 0 -> 1.0 (no discordant evidence either
    way; the protocol's b=c=0 worlds are handled by the KILL_flat/HELD
    rows, never by this p-value). Integer-exact: compares integer
    binomial sums against 2**s, no float pmf.

    Canonical anchor (§8, F1 correction): b=6, c=0 -> 1/64 = 0.015625
    (the reviewer's 0.03125 is the two-sided value — corrected in §8).
    """
    s = b + c
    if s == 0:
        return 1.0
    return sum(math.comb(s, k) for k in range(b, s + 1)) / (2 ** s)


# ----------------------------------------------------------------------------
# Tango (1998) score CI for the difference of two paired proportions
# (same validated machinery as the K2 bundle)
# ----------------------------------------------------------------------------

def _tango_q(n11, n12, n21, n22, delta):
    """Constrained MLE q~ = p~12 + p~21 under p12 - p21 = delta.

    Quadratic: n q^2 - (s + d*delta) q - delta*(m*delta - d) = 0
    (s = n12+n21 discordant, d = n12-n21, m = n11+n22 concordant).
    Root clamped to the feasible [|delta|, 1] (boundary MLE).
    """
    n = n11 + n12 + n21 + n22
    s = n12 + n21
    d = n12 - n21
    m = n11 + n22
    disc = (s + d * delta) ** 2 + 4.0 * n * delta * (m * delta - d)
    if disc < 0.0:
        disc = 0.0
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
        return math.inf if (d_hat - delta) > 0 else (-math.inf if (d_hat - delta) < 0 else 0.0)
    return (d_hat - delta) / math.sqrt(var)


def tango_ci(n11, n12, n21, n22, alpha=0.05):
    """Tango (score) two-sided CI for the paired difference delta.

    Returns (L, U) with L <= d_hat <= U, by bisection on the score
    statistic (Z strictly decreasing in delta). Deterministic.
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
    """Tango (score) one-sided 95% upper bound for the paired difference.

    U_1s solves Z(delta) = -z_0.95 (z = 1.6449) on [d_hat, 1] using the
    SAME constrained-MLE score statistic — one interval family, not two.
    Used ONLY for the KILL_flat functional bar (§8, R1).
    """
    n = n11 + n12 + n21 + n22
    if n == 0:
        raise ValueError("empty table")
    z = _phi_inv(0.95)
    d_hat = (n12 - n21) / n

    def f_hi(delta):
        return tango_score_z(n11, n12, n21, n22, delta) + z

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


def flip_contrast_stats(g_flips, r_flips, alpha=0.05, label=""):
    """Full paired-flip contrast record: table, one-sided McNemar p, Tango CI."""
    t = paired_flip_table(g_flips, r_flips)
    lo, hi = tango_ci(t["n11"], t["n12"], t["n21"], t["n22"], alpha=alpha)
    return {"label": label, "n": t["n"], "n11": t["n11"], "n12": t["n12"],
            "n21": t["n21"], "n22": t["n22"],
            "b": t["b"], "c": t["c"],
            "d_hat": t["d_hat"],
            "mcnemar_p_1s": mcnemar_one_sided_p(t["b"], t["c"]),
            "tango_L": lo, "tango_U": hi, "alpha": alpha,
            "tango_U_1s": tango_one_sided_upper(t["n11"], t["n12"],
                                               t["n21"], t["n22"])}


# ----------------------------------------------------------------------------
# Verdict table (EXP083 §8) — with the M1 verdict-precedence order
# ----------------------------------------------------------------------------

# Permitted evidentiary verdicts (program standard).
SUPPORTED = "Supported"
NOT_SUPPORTED = "Not supported"
INCONCLUSIVE = "Inconclusive"
UNDERDETERMINED = "Underdetermined"
REFUTED = "Refuted"

# EXP083 §8 row labels.
RE_SKIN_KILL = "RE-SKIN KILL"
KILL = "KILL"
HELD = "HELD"
CONTINUE = "CONTINUE"
INVALID = "INVALID"


def adjudicate_verdict(sha_prerun_ok, identity_ok, guard_fault,
                       g_static_fired, g_static_value,
                       g_norm_n_excluded, g_norm_floor,
                       g_flips, r_flips, delta_min=0.05):
    """Map EXP083 §8's verdict table to a row + evidentiary verdict.

    Inputs:
      sha_prerun_ok      (i) pre-run SHA-256 == pinned expected hash
      identity_ok        (ii) identity arm == archived C1 bit-for-bit
      guard_fault        (iii) None, or a cause string for a G-norm/G-static
                         computation fault
      g_static_fired     G-static bar fired (mean pairwise cos > 0.5)
      g_static_value     the G-static statistic (reported either way)
      g_norm_n_excluded  G-norm exclusion count (reported)
      g_norm_floor       G-norm floor value (reported)
      g_flips, r_flips   per-item flip indicators over the INCLUDED items
                         (exclusions already removed)
      delta_min          0.05 (the packet's claimed effect, Q4)

    Verdict precedence (M1, §8 header — evaluated in this order):
      INVALID (i) -> (ii) -> (iii) preempt everything;
      then RE-SKIN (on a validated apparatus only);
      then KILL_gross, KILL_flat, CONTINUE;
      then HELD (the catch-all: straddle / underpowered-flat / sub-claim).

    Row-vs-row reading (documented in BUILD_NOTES.md): CONTINUE's conjuncts
    are sufficient for CONTINUE — a significant positive directional result
    (one-sided McNemar p <= 0.05 at Delta >= 0.05) is not demoted to HELD by
    a straddling two-sided CI. This is forced by the MDE anchor
    (b=6, c=0 -> CONTINUE by §8's own pin).
    """
    n = len(g_flips)
    if len(r_flips) != n:
        raise ValueError("g_flips and r_flips must have equal length")
    n_final = n

    rec = {"delta_min": delta_min, "n_final": n_final,
           "g_static_value": g_static_value,
           "g_static_fired": bool(g_static_fired),
           "g_norm_n_excluded": g_norm_n_excluded,
           "g_norm_floor": g_norm_floor}

    # ---- INVALID precedence (i) -> (ii) -> (iii) ----
    if not sha_prerun_ok:
        rec.update(row=INVALID, row_detail="INVALID(i): pre-run SHA-256 != expected "
                   "pinned hash 4c242d...dd — wrong model downloaded (R3)",
                   verdict=UNDERDETERMINED, license="none")
        return rec
    if not identity_ok:
        rec.update(row=INVALID, row_detail="INVALID(ii): identity arm != archived C1 "
                   "bit-for-bit — apparatus failure",
                   verdict=UNDERDETERMINED, license="none")
        return rec
    if guard_fault is not None:
        rec.update(row=INVALID, row_detail="INVALID(iii): guard computation fault — "
                   + str(guard_fault), verdict=UNDERDETERMINED, license="none")
        return rec

    # ---- validated apparatus from here on ----
    st = flip_contrast_stats(g_flips, r_flips, label="r_vs_g")
    rec["contrast"] = st
    b, c = st["b"], st["c"]
    d_hat = st["d_hat"]
    p_1s = st["mcnemar_p_1s"]
    L, U = st["tango_L"], st["tango_U"]
    U_1s = st["tango_U_1s"]

    # ---- RE-SKIN: fires only on a validated apparatus (M1) ----
    if g_static_fired:
        rec.update(row=RE_SKIN_KILL,
                   row_detail="RE-SKIN KILL: mean pairwise cos(r_i, r_j) = %.4f > 0.5 "
                   "— r is a static direction in disguise; killed family (a) covers it. "
                   "Flip arms not run." % g_static_value,
                   verdict=NOT_SUPPORTED,
                   license="none — relational-readout family killed as operationalized")
        return rec

    # ---- KILL_gross: two-sided 95% Tango CI entirely below +0.05 ----
    # CI computed at observed N_final on the included items (M2).
    if U < delta_min:
        rec.update(row=KILL, row_detail="KILL_gross: two-sided 95%% Tango CI "
                   "(%.4f, %.4f) entirely below +0.05 — excludes the packet's "
                   "own claimed effect" % (L, U),
                   verdict=NOT_SUPPORTED,
                   license="none — H_rel killed at the kill-pilot bar")
        return rec

    # ---- KILL_flat: b = c = 0 and one-sided 95% upper < 0.05 ----
    if b == 0 and c == 0:
        if U_1s < delta_min:
            rec.update(row=KILL, row_detail="KILL_flat: b=c=0 with one-sided 95%% "
                       "Tango upper %.6f < 0.05 at N_final=%d (functional bar, R1)"
                       % (U_1s, n_final),
                       verdict=NOT_SUPPORTED,
                       license="none — H_rel killed (gross miss)")
            return rec
        # flat but underpowered — reachable only at N_final <= 51
        rec.update(row=HELD, row_detail="HELD: b=c=0 with one-sided 95%% Tango upper "
                   "%.6f >= 0.05 at N_final=%d — flat but underpowered"
                   % (U_1s, n_final),
                   verdict=INCONCLUSIVE,
                   license="priced powered follow-up only (never CONTINUE)")
        return rec

    # ---- CONTINUE: all four conjuncts ----
    if d_hat >= delta_min and p_1s <= 0.05:
        rec.update(row=CONTINUE,
                   row_detail="CONTINUE: Delta=%.4f >= 0.05 and exact one-sided "
                   "McNemar p=%.6f <= 0.05 in the A_r direction; G-static passed; "
                   "G-norm exclusions reported (%d)" % (d_hat, p_1s, g_norm_n_excluded),
                   verdict=INCONCLUSIVE,
                   license="powered pilot ONLY (new Law #15 packet, new pre-registration, "
                   "§9 arms mandatory) — never a capability claim")
        return rec

    # ---- HELD catch-all ----
    if L <= delta_min <= U:
        detail = ("HELD: two-sided 95%% Tango CI (%.4f, %.4f) straddles +0.05"
                  % (L, U))
    elif d_hat > 0 and 0.05 < p_1s <= 0.20:
        detail = ("HELD: sub-claim directional signal — Delta=%.4f > 0 with "
                  "one-sided p=%.4f in (0.05, 0.20]" % (d_hat, p_1s))
    else:
        detail = ("HELD: no kill row and no CONTINUE row fired "
                  "(Delta=%.4f, one-sided p=%.4f, CI=(%.4f, %.4f))"
                  % (d_hat, p_1s, L, U))
    rec.update(row=HELD, row_detail=detail, verdict=INCONCLUSIVE,
               license="priced powered follow-up only (never CONTINUE)")
    return rec
