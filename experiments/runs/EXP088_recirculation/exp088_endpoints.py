#!/usr/bin/env python3
"""EXP088 endpoint arithmetic (F4 primary statistics + verdict table).

Pure standard library. CPU. Deterministic (no RNG anywhere).

Implements the signed protocol's F4 primary statistics exactly:

  - paired 2x2 tables for correctness lists on the same items,
  - McNemar EXACT one-sided p (H1: first arm better than second),
    integer-exact via math.comb (no scipy on the build machine),
  - Tango (1998) score two-sided 95% CI for the difference of two paired
    proportions, on the paired D->S-vs-S->D difference (the section G1b /
    EXP077 convention named by F4),
  - the binding section G1b sub-threshold mapping (F5):
        L > delta_min          -> Supported
        U < delta_min          -> Not supported (contrast dead)
        otherwise              -> Inconclusive (held, never culled)
    with delta_min = 0.05 (the protocol's CONTINUE bar; MDE 10pp = 2*delta_min),
  - the F6 per-alpha curve adjudication (gain(alpha) pinned as the
    primary-contrast difference at alpha; classes: monotone_increasing /
    flat / cap_supports / other),
  - the Stage-B verdict precedence (documented reconciliation in
    adjudicate(); the B4-vs-F5 tension is flagged, not silently resolved),
  - the F7 Stage-A INVALID gate arithmetic (mean per-pair perplexity
    reduction vs the corpus noise floor).

Tango implementation: ported from experiments/runs/K2_routing_bypass/
k2_endpoints.py (the program-vetted Tango (1998) score interval: constrained
MLE q~ under p12 - p21 = delta, bisection on the score statistic). Ported,
not imported, per the EXP084 duplication-with-attribution precedent.
Re-validated by this bundle's evaluator tests (containment of d_hat,
arm-swap symmetry, reduction to the McNemar score at delta = 0,
degenerate-table behaviour).
"""

import math

# --- Pinned F4/F5 constants ---------------------------------------------------
ALPHA = 0.05            # primary significance bar (one-sided McNemar p <= 0.05)
CI_LEVEL = 0.95         # two-sided Tango CI level
DELTA_MIN = 0.05        # section G1b relevance threshold (5pp); CONTINUE bar
N_ITEMS = 60            # Stage-B probe size
ALPHA_LEAK = 0.10       # pinned primary leak coefficient (F4)
STAGE_B_ALPHAS = (0.07, 0.10, 0.15)   # pinned alpha sweep (Stage B)


# ----------------------------------------------------------------------------
# Normal quantile (Acklam's approximation; deterministic, ~1e-9 accuracy)
# Ported verbatim from k2_endpoints.py.
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
# Paired tables + McNemar exact one-sided
# ----------------------------------------------------------------------------

def paired_table(x_correct, y_correct):
    """Paired 2x2 table for (x, y) correctness lists on the same items.

    n11: x right, y right.  n12: x wrong, y right (y rescues over x).
    n21: x right, y wrong (y loses vs x).  n22: both wrong.
    d_hat = P(y right) - P(x right) = (n12 - n21) / n.
    McNemar orientation: b = n12 (y rescues), c = n21 (y loses).
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
    if n == 0:
        raise ValueError("empty paired table")
    return {"n11": n11, "n12": n12, "n21": n21, "n22": n22, "n": n,
            "d_hat": (n12 - n21) / n, "b": n12, "c": n21}


def mcnemar_exact_one_sided_greater(b, c):
    """Exact one-sided McNemar p for H1: y better than x.

    b = #{x wrong, y right} (y rescues); c = #{x right, y wrong} (y loses).
    p = P(Bin(b + c, 0.5) >= b). Integer-exact via math.comb.
    b = c = 0 -> 1.0 (no discordant pairs; the EXP077 M5.1 convention).
    """
    s = b + c
    if s == 0:
        return 1.0
    return sum(math.comb(s, k) for k in range(b, s + 1)) / (2 ** s)


# ----------------------------------------------------------------------------
# Tango (1998) score CI for the difference of two paired proportions.
# Ported from k2_endpoints.py (see module docstring).
# ----------------------------------------------------------------------------

def _tango_q(n11, n12, n21, n22, delta):
    """Constrained MLE q~ = p~12 + p~21 under p12 - p21 = delta.

    Derivation (K2): multinomial log-likelihood in (q, p11) with
    p12 = (q+delta)/2, p21 = (q-delta)/2, p22 = 1 - p11 - q gives the
    quadratic  n q^2 - (s + d*delta) q - delta*(m*delta - d) = 0
    (s = n12+n21 discordant, d = n12-n21, m = n11+n22 concordant).
    At delta = 0 this reduces to q~ = s/n and the score statistic reduces
    to the McNemar score (n12-n21)/sqrt(n12+n21).
    The root is clamped to the feasible [|delta|, 1].
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
    statistic (Z is strictly decreasing in delta). Degenerate tables yield
    a non-degenerate interval (score-interval behaviour); the all-concordant
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


def paired_contrast_stats(x_correct, y_correct, alpha=0.05, label=""):
    """Full paired-contrast record: table, McNemar exact one-sided p, Tango CI.

    x = reference arm, y = challenger arm; H1: y better than x.
    Returns dict with n, n11..n22, b, c, d_hat, mcnemar_p_one_sided,
    tango_L, tango_U.
    """
    t = paired_table(x_correct, y_correct)
    lo, hi = tango_ci(t["n11"], t["n12"], t["n21"], t["n22"], alpha=alpha)
    return {"label": label, "n": t["n"], "n11": t["n11"], "n12": t["n12"],
            "n21": t["n21"], "n22": t["n22"], "b": t["b"], "c": t["c"],
            "d_hat": t["d_hat"],
            "mcnemar_p_one_sided": mcnemar_exact_one_sided_greater(t["b"], t["c"]),
            "tango_L": lo, "tango_U": hi}


# ----------------------------------------------------------------------------
# Binding section G1b sub-threshold mapping (F5)
# ----------------------------------------------------------------------------

def g1b_map(tango_L, tango_U, delta_min=DELTA_MIN):
    """Map a two-sided Tango CI to the binding section G1b outcome.

    L > delta_min -> "Supported"; U < delta_min -> "Not supported"
    (contrast dead); otherwise -> "Inconclusive" (held, never culled).
    """
    if tango_L > delta_min:
        return "Supported"
    if tango_U < delta_min:
        return "Not supported"
    return "Inconclusive"


# ----------------------------------------------------------------------------
# F6 per-alpha curve adjudication
# ----------------------------------------------------------------------------

def gain_curve_class(g007, g010, g015):
    """Classify the per-alpha gain curve (F6, pinned adjudication rule).

    gain(alpha) is pinned as the PRIMARY-CONTRAST difference at alpha:
        gain(alpha) = acc(D->S, alpha) - acc(S->D, alpha).
    (Protocol: "gain(0.15) <= gain(0.10) on the primary contrast".)

    Returns one of:
      "monotone_increasing" -- gain(0.07) < gain(0.10) < gain(0.15), strict.
          F6: -> PIVOT (B2, perturbation-magnitude account).
      "flat" -- all three gains exactly equal.
          F6: neutral (the primary contrast rules).
      "cap_supports" -- cap-shaped (rises then falls, at least one strict
          step: gain(0.07) <= gain(0.10) and gain(0.15) <= gain(0.10) with a
          strict inequality somewhere) OR alpha=0.15-harms while
          alpha=0.10-helps (gain(0.15) < 0 and gain(0.10) > 0).
          F6/B3: supports the belief-state account (secondary support only;
          no Supported-licensing power per the EXP085-F5 precedent).
      "other" -- none of the above; neutral (the primary contrast rules).
    """
    gains = (g007, g010, g015)
    if g007 < g010 < g015:
        return "monotone_increasing"
    if g007 == g010 == g015:
        return "flat"
    cap = (g007 <= g010 and g015 <= g010 and (g007 < g010 or g015 < g010))
    harms_helps = (g015 < 0.0 and g010 > 0.0)
    if cap or harms_helps:
        return "cap_supports"
    return "other"


# ----------------------------------------------------------------------------
# F7 Stage-A INVALID gate arithmetic
# ----------------------------------------------------------------------------

def stage_a_gate(pair_deltas, eps):
    """Apply the F7 feasibility gate.

    pair_deltas: dict {(s, d): mean perplexity-reduction Δppl} for the 9
        grid pairs. eps: corpus noise floor from the two no-recirculation
        repeat runs (pinned default 0 if unmeasurable — identical repeats
        give exactly 0.0).
    A pair passes iff its Δppl is STRICTLY greater than eps
    ("strictly-positive Δppl beyond the corpus noise floor").

    Returns (ok, selected, margin_runner_up, passing):
      ok=False -> no pair passed -> INVALID (do not proceed to Stage B).
      ok=True  -> selected = (s*, d*) = argmax Δppl; margin_runner_up = the
                 argmax's margin over the runner-up (pinned: logged).
    Exact ties for the argmax raise ValueError (loud halt — a silent
    tie-break would be an invented rule; ties are measure-zero for
    continuous perplexity differences).
    """
    passing = {pair: d for pair, d in pair_deltas.items() if d > eps}
    if not passing:
        return (False, None, None, {})
    best = max(passing.values())
    winners = [pair for pair, d in passing.items() if d == best]
    if len(winners) > 1:
        raise ValueError(
            f"Stage-A argmax tie among {winners} at Δppl={best:.6f}: "
            "the signed protocol pins no tie-break; halting loud.")
    selected = winners[0]
    rest = [d for pair, d in passing.items() if pair != selected]
    margin = best - max(rest) if rest else best
    return (True, selected, margin, passing)


# ----------------------------------------------------------------------------
# Stage-B verdict adjudication
# ----------------------------------------------------------------------------

def adjudicate(primary, secondary, arm_beats_baseline, curve_class):
    """Apply the Stage-B verdict table in binding precedence order.

    Args:
        primary: paired_contrast_stats dict for D->S vs S->D at alpha=0.10
            (x = S->D, y = D->S; H1: D->S better). Carries mcnemar_p_one_sided,
            tango_L, tango_U, d_hat.
        secondary: paired_contrast_stats dict for D->S vs RAND at alpha=0.10
            (x = RAND, y = D->S). d_hat > 0 means D->S point-beats RAND.
        arm_beats_baseline: dict {arm_name: bool} — whether each
            recirculation arm (D->S, S->D, RAND) at alpha=0.10 beats the
            no-recirculation baseline by paired McNemar exact one-sided
            p <= 0.05 (arm > baseline).
        curve_class: gain_curve_class() output for the per-alpha gains.

    Precedence (binding):
      1. CONTINUE iff primary Supported (LCI > 0.05) AND D->S point-beats
         RAND AND the per-alpha curve is not monotone-increasing.
         (B2 override: a monotone-increasing gain curve is the
         perturbation-magnitude signature -> PIVOT even when the primary
         contrast clears, recorded explicitly.)
      2. KILL iff primary Not supported (Tango U < 0.05 — contrast dead) OR
         D->S does not point-beat RAND (d_hat <= 0).
      3. PIVOT iff the curve is monotone-increasing (B2/F6), or
         (primary Inconclusive AND some recirculation arm beats baseline)
         — "recirculation helps but direction doesn't matter".
      4. HELD otherwise (CIs straddle; underpowered — no N increase
         pre-registered).

    RECONCILIATION NOTE (flagged for the Law #14 bundle review): the
    verdict bullets' "KILL if Δ <= 0 (LCI <= 0)" and breaking point B4's
    literal "S->D >= D->S -> KILL" are read THROUGH the binding F5/section-G1b
    mapping: KILL on the primary prong fires only when the contrast is dead
    (U < delta_min). A non-positive point estimate whose CI still reaches
    delta_min is Inconclusive -> HELD/PIVOT, never KILL ("held, never
    culled"; "0 < LCI <= 0.05 is held, not killed"). This is the only
    reading under which the binding mapping, the HELD-on-straddle rule,
    and KILL-on-dead-contrast are simultaneously satisfiable. The B4-literal
    reading (any d_hat <= 0 -> KILL) is NOT implemented; the reviewer
    adjudicates.

    Returns (verdict_label, evidentiary, detail).
    Evidentiary vocabulary: the mentor-adopted standard (Supported /
    Not supported / Inconclusive / Underdetermined / Refuted).
    """
    L, U = primary["tango_L"], primary["tango_U"]
    outcome = g1b_map(L, U)
    d_rand = secondary["d_hat"]
    b2_override = (curve_class == "monotone_increasing")

    # 1. CONTINUE — with the B2/F6 monotone-curve override to PIVOT.
    if outcome == "Supported" and d_rand > 0.0 and not b2_override:
        return ("CONTINUE", "Supported",
                f"primary Supported (Tango LCI={L:.4f} > {DELTA_MIN}); "
                f"D->S point-beats RAND (Δ={d_rand:+.4f}); curve={curve_class} "
                "(B3/neutral — no B2 override)")
    # 2. KILL — contrast dead, or the no-information arm wins the point.
    if outcome == "Not supported" or d_rand <= 0.0:
        why = []
        if outcome == "Not supported":
            why.append(f"primary contrast dead (Tango U={U:.4f} < {DELTA_MIN})")
        if d_rand <= 0.0:
            why.append(f"D->S does not point-beat RAND (Δ={d_rand:+.4f})")
        return ("KILL", "Not supported", "; ".join(why))
    # 3. PIVOT — B2 monotone curve, or helps-but-direction-unresolved.
    helps = any(arm_beats_baseline.values())
    if b2_override:
        return ("PIVOT", "Inconclusive",
                "per-alpha gain monotone-increasing in alpha (B2/F6: "
                "perturbation-magnitude signature, not belief-state); "
                "characterize as perturbation/compute effect")
    if outcome == "Inconclusive" and helps:
        beaters = sorted(a for a, b in arm_beats_baseline.items() if b)
        return ("PIVOT", "Inconclusive",
                f"primary Inconclusive (Tango [{L:.4f},{U:.4f}] straddles) but "
                f"recirculation helps ({'+'.join(beaters)} beat baseline "
                "at p<=0.05): direction doesn't matter -> "
                "perturbation/compute characterization")
    # 4. HELD — underpowered; no N increase pre-registered.
    return ("HELD", "Inconclusive",
            f"primary Inconclusive (Tango [{L:.4f},{U:.4f}]); no arm beats "
            "baseline; held per the power gate (no N increase pre-registered)")
