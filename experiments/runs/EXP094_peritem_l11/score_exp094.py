"""EXP094 scorer — statistics and the §3 TOTAL decision table.

Pre-reg: research/innovation/S4-9_PREREG_DRAFT_2026-09-27.md §2.3 (statistics),
§3 (decision table, binding evaluation order), §5 item 5 (nine-cell stratum
table), §5 item 6 (decision-table worksheet).

Statistics (pre-reg §2.3):
  - McNemar exact (two-sided, doubling convention) on paired decisions:
    T-vs-B, R-vs-B (each arm vs the item's own baseline), T-vs-R (paired
    directly, not vs baseline).
  - ΔM_T = (nT - nB)/n, ΔM_R = (nR - nB)/n — integer-count differences
    (EXP093 F1 lesson: compute from counts before dividing).
  - Tango (1998) 95% score CIs on the paired differences.
  - DELTA_BAR = 0.10, ALPHA = 0.05 — verbatim bars, no post-hoc movement.

Decision table (pre-reg §3, first match wins — F1 repair):
  1. Delivery probe FAILS -> Inconclusive (procedure invalid; never a verdict)
  2. {d_i} degenerate (mean pairwise |cosine| >= 0.95) -> Underdetermined
     (never KILL on a powerless test — R4 rule)
  3. Movement: (b+c on T-vs-B) + (b+c on R-vs-B) < 6 -> Refuted (KILL family:
     inertness is not a sharedness artifact)
  4. Specificity: T-vs-R McNemar p >= 0.05 AND overlapping Tango CIs
     (CI of the T-vs-B paired difference vs CI of the R-vs-B paired
     difference) -> Refuted (KILL specificity: nonspecific perturbation)
  5. Licensed positive: ΔM_T > 0.10 AND T-vs-R p < 0.05 AND stratum-consistent
     (ΔM_T > 0 in aggregate, A-first, AND C-first — strict) -> Supported
     (CONTINUE, bench-scoped to EXP092-B)
  6. Otherwise -> Not supported (PIVOT), with named sub-cases:
     (b) ΔM_T < -0.10 AND T-vs-R p < 0.05 — consistent wrong-direction
         steering: a causal channel exists, mis-signed; EXP095 material.
     (c) T-vs-R significant (p < 0.05) but stratum-inconsistent —
         underlicensed; conditional design is EXP095 material.
     (a) null T-vs-R specificity (p >= 0.05) with sign-heterogeneous movement
         (flips in both directions on T-vs-B, or mixed stratum ΔM_T signs) —
         global per-item claim dead; conditional design is EXP095 material.
     (general) none of (a)/(b)/(c) fires — PIVOT, sub-case unassigned.

Five permitted verdicts: Supported / Not supported / Inconclusive /
Underdetermined / Refuted. No banned language.

Tie rule (EXP093 S2 procedure, cited by reference §5 item 1): correct iff
margin > 0 (strict); exact margin == 0 scored INCORRECT and logged. Tie rate
> 5% of the 180 decision item-conditions (3 arms x 60) -> RUN-INVALID.

numpy-only.
"""

import math

import numpy as np

N_ITEMS = 60
DELTA_BAR = 0.10
ALPHA = 0.05
TIE_RATE_BAR = 0.05
MOVEMENT_GATE = 6
DEGENERACY_BAR = 0.95
Z_975 = 1.959963984540054  # Normal 97.5% quantile (Tango 95% CI)


class RunInvalid(Exception):
    """Guard/statistical failure -> RUN-INVALID (withheld, never a verdict)."""


# ---------------------------------------------------------------------------
# McNemar exact (two-sided, doubling convention) — EXP093 procedure, reused.
# ---------------------------------------------------------------------------

def mcnemar_exact_p(b, c):
    """b = discordant pairs favoring the first-named condition; c = favoring
    the second. Under H0, b ~ Binomial(b + c, 0.5). n = 0 -> p = 1.0."""
    n = int(b) + int(c)
    if n == 0:
        return 1.0
    k = min(int(b), int(c))
    tail = sum(math.comb(n, j) for j in range(k + 1)) * (0.5 ** n)
    return min(1.0, 2.0 * tail)


# ---------------------------------------------------------------------------
# Tango (1998) score CI for the paired difference theta = p10 - p01.
#
# Inverts the score test: CI = {delta0 : |T(delta0)| <= z_975}, where T uses
# the constrained MLE (p10~, p01~) under p10 - p01 = delta0. The constrained
# MLE is found by profiling t = p01 over [max(0,-delta0), (1-delta0)/2];
# the profile log-likelihood is concave in t (concave function over a convex
# slice), so golden-section search is exact. numpy-only.
# ---------------------------------------------------------------------------

def _tango_score_abs(delta0, n10, n01, n11, n00):
    n = n10 + n01 + n11 + n00
    theta_hat = (n10 - n01) / n
    lo = max(0.0, -delta0)
    hi = (1.0 - delta0) / 2.0
    if hi < lo - 1e-15:
        return float("inf")

    def negloglik(t):
        p01 = t
        p10 = t + delta0
        s = 1.0 - p10 - p01
        if s < 0.0:
            return float("inf")
        if n11 + n00 > 0:
            p11 = s * n11 / (n11 + n00)
            p00 = s * n00 / (n11 + n00)
        else:
            # No concordant pairs observed: all mass must sit on the
            # discordant cells, so s must be 0 (t forced to (1-delta0)/2).
            if s > 1e-12:
                return float("inf")
            p11 = 0.0
            p00 = 0.0
        ll = 0.0
        for cnt, p in ((n11, p11), (n10, p10), (n01, p01), (n00, p00)):
            if cnt > 0:
                if p <= 0.0:
                    return float("inf")
                ll += cnt * math.log(p)
        return -ll

    # Golden-section search (concave profile -> unimodal).
    gr = (math.sqrt(5.0) - 1.0) / 2.0
    a, b = lo, hi
    c = b - gr * (b - a)
    d = a + gr * (b - a)
    fc, fd = negloglik(c), negloglik(d)
    for _ in range(200):
        if fc < fd:
            b, fd = d, fc
            d = c
            c = b - gr * (b - a)
            fc = negloglik(c)
        else:
            a, fc = c, fd
            c = d
            d = a + gr * (b - a)
            fd = negloglik(d)
        if abs(b - a) < 1e-13:
            break
    t_star = (a + b) / 2.0
    p01t = t_star
    p10t = t_star + delta0
    var = (p10t + p01t - (p10t - p01t) ** 2) / n
    if var <= 0.0:
        return 0.0 if theta_hat == delta0 else float("inf")
    return abs((theta_hat - delta0) / math.sqrt(var))


def tango_ci_paired(n10, n01, n11, n00, alpha=ALPHA):
    """Tango 95% score CI for theta = p10 - p01 from a paired 2x2 table.

    n10 = first-named correct & second-named wrong (favors first);
    n01 = first-named wrong & second-named correct (favors second);
    n11 = both correct; n00 = both wrong.
    Returns (lo, hi). Bisection on the score statistic; endpoints where the
    score p-value equals alpha. Degenerate no-discordant case -> (0, 0).
    """
    n = n10 + n01 + n11 + n00
    if n == 0:
        raise RunInvalid("tango_ci_paired: empty table.")
    theta_hat = (n10 - n01) / n
    if n10 == 0 and n01 == 0:
        return (0.0, 0.0)

    def score(d):
        return _tango_score_abs(d, n10, n01, n11, n00)

    z = Z_975  # alpha = 0.05 two-sided
    # Lower endpoint in [-1, theta_hat].
    if score(-1.0) < z:
        lo = -1.0
    else:
        a, b = -1.0, theta_hat
        for _ in range(200):
            m = (a + b) / 2.0
            if score(m) <= z:
                b = m
            else:
                a = m
        lo = (a + b) / 2.0
    # Upper endpoint in [theta_hat, 1].
    if score(1.0) < z:
        hi = 1.0
    else:
        a, b = theta_hat, 1.0
        for _ in range(200):
            m = (a + b) / 2.0
            if score(m) <= z:
                a = m
            else:
                b = m
        hi = (a + b) / 2.0
    return (float(lo), float(hi))


def _ci_overlap(ci1, ci2):
    return ci1[0] <= ci2[1] and ci2[0] <= ci1[1]


# ---------------------------------------------------------------------------
# Contrast statistics.
# ---------------------------------------------------------------------------

def contrast_stats(correct_X, correct_Y):
    """Paired contrast of arm X vs arm Y (boolean arrays, length n).

    Returns dict with delta (integer-count difference / n), McNemar b/c/p
    (b favors X, c favors Y), and the Tango 95% CI for pX - pY.
    """
    X = np.asarray(correct_X, dtype=bool)
    Y = np.asarray(correct_Y, dtype=bool)
    n = len(X)
    nX = int(X.sum())
    nY = int(Y.sum())
    b = int((X & ~Y).sum())   # X right, Y wrong — favors X
    c = int((~X & Y).sum())   # X wrong, Y right — favors Y
    n11 = int((X & Y).sum())
    n00 = int((~X & ~Y).sum())
    return {
        "n": n,
        "acc_X": float(nX / n),
        "acc_Y": float(nY / n),
        "delta": (nX - nY) / n,
        "mcnemar_b": b,
        "mcnemar_c": c,
        "mcnemar_p": mcnemar_exact_p(b, c),
        "tango_ci": tango_ci_paired(b, c, n11, n00),
    }


# ---------------------------------------------------------------------------
# Decision table (pre-reg §3, binding order).
# ---------------------------------------------------------------------------

def decide(delivery_pass, mean_abs_cosine, cells):
    """Apply the §3 decision table. cells: dict with keys
    ('agg'|'A'|'C', 'TB'|'RB'|'TR') -> contrast_stats dict.

    Returns (verdict, step, worksheet) with the five permitted verdicts.
    """
    ws = []  # decision-table worksheet: step -> condition evidence

    def note(step, cond, evidence):
        ws.append({"step": step, "condition": cond, "evidence": evidence})

    # Step 1 — delivery.
    note(1, "G5-style probe FAILS -> Inconclusive",
         f"delivery_pass={delivery_pass}")
    if not delivery_pass:
        return "Inconclusive", 1, ws

    # Step 2 — degeneracy.
    note(2, "mean pairwise |cosine| >= 0.95 -> Underdetermined",
         f"mean_abs_cosine={mean_abs_cosine:.4f}")
    if mean_abs_cosine >= DEGENERACY_BAR:
        return "Underdetermined", 2, ws

    TB = cells[("agg", "TB")]
    RB = cells[("agg", "RB")]
    TR = cells[("agg", "TR")]

    # Step 3 — movement gate.
    movement = (TB["mcnemar_b"] + TB["mcnemar_c"]
                + RB["mcnemar_b"] + RB["mcnemar_c"])
    note(3, f"movement (b+c TB + b+c RB) < {MOVEMENT_GATE} -> Refuted "
            "(KILL family)", f"movement={movement}")
    if movement < MOVEMENT_GATE:
        return "Refuted", 3, ws

    # Step 4 — specificity.
    overlap = _ci_overlap(TB["tango_ci"], RB["tango_ci"])
    note(4, "T-vs-R p >= 0.05 AND overlapping Tango CIs (TB vs RB) -> "
            "Refuted (KILL specificity)",
         f"p_TR={TR['mcnemar_p']:.4g}, CI_TB={TB['tango_ci']}, "
         f"CI_RB={RB['tango_ci']}, overlap={overlap}")
    if TR["mcnemar_p"] >= ALPHA and overlap:
        return "Refuted", 4, ws

    # Step 5 — licensed positive.
    dT_agg = cells[("agg", "TB")]["delta"]
    dT_A = cells[("A", "TB")]["delta"]
    dT_C = cells[("C", "TB")]["delta"]
    stratum_consistent = dT_agg > 0 and dT_A > 0 and dT_C > 0
    note(5, "dM_T > 0.10 AND T-vs-R p < 0.05 AND stratum-consistent "
            "(dM_T > 0 in agg, A-first, C-first) -> Supported",
         f"dM_T_agg={dT_agg:+.4f}, dM_T_A={dT_A:+.4f}, dM_T_C={dT_C:+.4f}, "
         f"p_TR={TR['mcnemar_p']:.4g}, consistent={stratum_consistent}")
    if dT_agg > DELTA_BAR and TR["mcnemar_p"] < ALPHA and stratum_consistent:
        return "Supported", 5, ws

    # Step 6 — PIVOT sub-cases.
    sub = None
    if dT_agg < -DELTA_BAR and TR["mcnemar_p"] < ALPHA:
        sub = "(b) consistent wrong-direction steering"
    elif TR["mcnemar_p"] < ALPHA:
        sub = "(c) T-vs-R significant but stratum-inconsistent"
    else:
        signs = {np.sign(dT_agg), np.sign(dT_A), np.sign(dT_C)} - {0.0}
        hetero = ((TB["mcnemar_b"] > 0 and TB["mcnemar_c"] > 0)
                  or len(signs) > 1)
        if hetero:
            sub = "(a) sign-heterogeneous movement, null specificity"
        else:
            sub = "(general) no named sub-case fires"
    note(6, f"otherwise -> Not supported (PIVOT) {sub}",
         f"dM_T_agg={dT_agg:+.4f}, p_TR={TR['mcnemar_p']:.4g}")
    return "Not supported", 6, ws


# ---------------------------------------------------------------------------
# Full scoring pass.
# ---------------------------------------------------------------------------

def score_experiment(margins_B, margins_T, margins_R, phrasing,
                     delivery_pass, mean_abs_cosine):
    """Full scoring from per-item logit margins (target − foil).

    Returns the report dict: 9-cell stratum table, decision-table worksheet,
    verdict, secondaries. Raises RunInvalid on tie-rate breach or malformed
    input.
    """
    mB = np.asarray(margins_B, dtype=np.float64)
    mT = np.asarray(margins_T, dtype=np.float64)
    mR = np.asarray(margins_R, dtype=np.float64)
    ph = np.array([str(x) for x in phrasing])
    if not (len(mB) == len(mT) == len(mR) == len(ph) == N_ITEMS):
        raise RunInvalid(
            f"scorer input length mismatch: {len(mB)}/{len(mT)}/{len(mR)}/"
            f"{len(ph)} != 60 — RUN-INVALID.")

    ties = int((mB == 0.0).sum() + (mT == 0.0).sum() + (mR == 0.0).sum())
    tie_rate = ties / (3 * N_ITEMS)
    if tie_rate > TIE_RATE_BAR:
        raise RunInvalid(
            f"tie rate {tie_rate:.3f} ({ties}/180 decision item-conditions) "
            f"> 5% — degenerate measurement — RUN-INVALID.")

    cB = mB > 0.0
    cT = mT > 0.0
    cR = mR > 0.0
    strata = {
        "agg": np.arange(N_ITEMS),
        "A": np.nonzero(ph == "A-first")[0],
        "C": np.nonzero(ph == "C-first")[0],
    }
    if len(strata["A"]) != 30 or len(strata["C"]) != 30:
        raise RunInvalid(
            f"phrasing strata malformed: A-first={len(strata['A'])}, "
            f"C-first={len(strata['C'])} (expected 30/30) — RUN-INVALID.")

    cells = {}
    for sname, idx in strata.items():
        cells[(sname, "TB")] = contrast_stats(cT[idx], cB[idx])
        cells[(sname, "RB")] = contrast_stats(cR[idx], cB[idx])
        cells[(sname, "TR")] = contrast_stats(cT[idx], cR[idx])

    verdict, step, worksheet = decide(delivery_pass, mean_abs_cosine, cells)

    stratum_table = {}
    for (sname, contrast), st in cells.items():
        stratum_table[f"{sname}__{contrast}"] = {
            "n": st["n"],
            "acc_X": st["acc_X"],
            "acc_Y": st["acc_Y"],
            "delta": st["delta"],
            "mcnemar_b": st["mcnemar_b"],
            "mcnemar_c": st["mcnemar_c"],
            "mcnemar_p": st["mcnemar_p"],
            "tango_ci_lo": st["tango_ci"][0],
            "tango_ci_hi": st["tango_ci"][1],
        }

    secondaries = {
        "mean_margin_shift_T": float((mT - mB).mean()),
        "mean_margin_shift_R": float((mR - mB).mean()),
        "flip_ledger": {
            "B_wrong_to_T_right": [int(i) for i in np.nonzero(~cB & cT)[0]],
            "B_right_to_T_wrong": [int(i) for i in np.nonzero(cB & ~cT)[0]],
            "B_wrong_to_R_right": [int(i) for i in np.nonzero(~cB & cR)[0]],
            "B_right_to_R_wrong": [int(i) for i in np.nonzero(cB & ~cR)[0]],
        },
        "tie_count": ties,
        "tie_rate": float(tie_rate),
        "baseline_acc_B": float(cB.mean()),
        "n_B_correct": int(cB.sum()),
    }
    return {
        "verdict": verdict,
        "decision_step": step,
        "decision_worksheet": worksheet,
        "stratum_table": stratum_table,
        "secondaries": secondaries,
        "bars": {"delta_bar": DELTA_BAR, "alpha": ALPHA,
                 "movement_gate": MOVEMENT_GATE,
                 "degeneracy_bar": DEGENERACY_BAR},
        "n": N_ITEMS,
    }
