"""EXP093 scorer — statistics and the §5 TOTAL decision tree.

Primary (decision-driving, draft §4.1):
  Δ = acc(P) - acc(B) on the phrasing-balanced aggregate (n = 60)
  McNemar exact test (two-sided, doubling convention) on paired P-vs-B
  outcomes; α = 0.05; no multiplicity correction on the primary.
  Monotonicity: strict acc(P) > acc(B) > acc(N).
  CONTINUE bars (all three): Δ >= 0.10 and p < 0.05 and strict monotonicity.

Stratified (§4.2): per stratum (A-first n=30; C-first n=30): Δ_s, McNemar
nominal p_s, within-stratum monotonicity. Nominal p-values (multiplicity
noted, not corrected).

Secondaries (§4.3, reported, non-binding): N-vs-B McNemar; mean margin
shifts; flip ledger.

Decision tree (§5 TOTAL):
  CONTINUE — aggregate: Δ >= 0.10 and p < 0.05 and strict P > B > N.
  KILL     — every McNemar p (aggregate, A-first, C-first; P-vs-B) >= 0.05.
  PIVOT(a) — aggregate fails CONTINUE; A-first meets all three bars while
             C-first does not → phrasing-conditioned mechanisms.
  PIVOT(b) — some McNemar p < 0.05 (P-vs-B or N-vs-B) but the 10pp bar or
             monotonicity fails → mechanism forensics.
  PIVOT(c) — C-first meets all three bars while the aggregate fails
             CONTINUE → mechanism forensics.
  RUN-INVALID — any guard failure; tie rate > 5% of item-conditions; etc.

Evaluation order: CONTINUE → PIVOT(c) → PIVOT(a) → PIVOT(b) → KILL.
(Per draft F3/F4: significant N-vs-B with non-significant P-vs-B routes to
PIVOT(b) forensics, never to KILL; C-first-only significance never to KILL.)

Tie rule (draft §3.2 / F9): correct iff logit(target) > logit(foil) — strict
inequality; exact ties are scored INCORRECT and logged. Tie rate > 5% of the
180 item-conditions → RUN-INVALID (degenerate measurement).

numpy-only.
"""

import math

import numpy as np

N_ITEMS = 60
DELTA_BAR = 0.10
ALPHA = 0.05
TIE_RATE_BAR = 0.05  # >5% of item-conditions -> RUN-INVALID


class RunInvalid(Exception):
    """Guard/statistical failure -> RUN-INVALID (withheld, never a verdict)."""


def mcnemar_exact_p(b, c):
    """Exact McNemar two-sided p-value (doubling convention).

    b = # items wrong under B but right under P (discordant, P favors);
    c = # items right under B but wrong under P (discordant, B favors).
    Under H0, b ~ Binomial(b + c, 0.5); p = 2 * min(one-sided tails),
    capped at 1. n = b + c = 0 -> p = 1.0 (no discordant pairs).
    """
    n = int(b) + int(c)
    if n == 0:
        return 1.0
    k = min(int(b), int(c))
    tail = sum(math.comb(n, j) for j in range(k + 1)) * (0.5 ** n)
    return min(1.0, 2.0 * tail)


def _acc(correct):
    correct = np.asarray(correct, dtype=bool)
    return float(correct.mean()), int(correct.sum())


def stratum_stats(correct_B, correct_P, correct_N, idx):
    """Aggregate statistics for a stratum (or the full set)."""
    idx = np.asarray(idx)
    B = np.asarray(correct_B, dtype=bool)[idx]
    P = np.asarray(correct_P, dtype=bool)[idx]
    N = np.asarray(correct_N, dtype=bool)[idx]
    acc_B, nB = _acc(B)
    acc_P, nP = _acc(P)
    acc_N, nN = _acc(N)
    b = int((~B & P).sum())   # B wrong -> P right
    c = int((B & ~P).sum())   # B right -> P wrong
    p = mcnemar_exact_p(b, c)
    # N-vs-B secondary (non-binding)
    b_n = int((~B & N).sum())
    c_n = int((B & ~N).sum())
    p_n = mcnemar_exact_p(b_n, c_n)
    # F1 (LOG-4345): compute delta from integer count differences BEFORE
    # dividing. acc_P - acc_B on float means gives 0.09999999999999998 at
    # the exactly-at-bar case (nP-nB=6, n=60), which would misroute a
    # CONTINUE-worthy outcome. (nP-nB)/n is exactly 0.1.
    delta = (nP - nB) / len(idx)
    mono = bool(acc_P > acc_B > acc_N)
    return {
        "n": int(len(idx)),
        "acc_B": acc_B, "acc_P": acc_P, "acc_N": acc_N,
        "delta": delta,
        "mcnemar_b": b, "mcnemar_c": c, "mcnemar_p": p,
        "mcnemar_NvB_b": b_n, "mcnemar_NvB_c": c_n, "mcnemar_NvB_p": p_n,
        "delta_N": (nN - nB) / len(idx),
        "monotone": mono,
        "bars": bool(delta >= DELTA_BAR and p < ALPHA and mono),
    }


def decide(agg, strat_A, strat_C):
    """Apply the §5 TOTAL decision tree. Returns (verdict, detail).

    Each argument is a stratum_stats dict. Evaluation order:
    CONTINUE → PIVOT(c) → PIVOT(a) → PIVOT(b) → KILL.
    """
    agg_continue = bool(agg["delta"] >= DELTA_BAR and agg["mcnemar_p"] < ALPHA
                        and agg["monotone"])
    if agg_continue:
        verdict = "CONTINUE"
    elif strat_C["bars"]:
        verdict = "PIVOT(c)"
    elif strat_A["bars"] and not strat_C["bars"]:
        verdict = "PIVOT(a)"
    elif (agg["mcnemar_p"] < ALPHA or strat_A["mcnemar_p"] < ALPHA
          or strat_C["mcnemar_p"] < ALPHA or agg["mcnemar_NvB_p"] < ALPHA
          or strat_A["mcnemar_NvB_p"] < ALPHA
          or strat_C["mcnemar_NvB_p"] < ALPHA):
        verdict = "PIVOT(b)"
    else:
        verdict = "KILL"
    detail = {
        "aggregate": {k: agg[k] for k in (
            "n", "acc_B", "acc_P", "acc_N", "delta", "mcnemar_b",
            "mcnemar_c", "mcnemar_p", "mcnemar_NvB_p", "delta_N",
            "monotone", "bars")},
        "A_first": {k: strat_A[k] for k in (
            "n", "acc_B", "acc_P", "acc_N", "delta", "mcnemar_b",
            "mcnemar_c", "mcnemar_p", "mcnemar_NvB_p", "delta_N",
            "monotone", "bars")},
        "C_first": {k: strat_C[k] for k in (
            "n", "acc_B", "acc_P", "acc_N", "delta", "mcnemar_b",
            "mcnemar_c", "mcnemar_p", "mcnemar_NvB_p", "delta_N",
            "monotone", "bars")},
        "bars": {"delta_bar": DELTA_BAR, "alpha": ALPHA},
    }
    return verdict, detail


def score_conditions(margins_B, margins_P, margins_N, phrasing):
    """Full scoring pass from per-item logit margins (target − foil).

    margins_*: length-60 arrays of float margins per condition.
    phrasing: length-60 array of "A-first"/"C-first".
    Returns the report dict (verdict + detail + secondaries).

    Tie rule: correct iff margin > 0 (strict); exact margin == 0 is scored
    INCORRECT and counted as a tie. Tie rate > 5% of the 180
    item-conditions → RUN-INVALID.
    """
    mB = np.asarray(margins_B, dtype=np.float64)
    mP = np.asarray(margins_P, dtype=np.float64)
    mN = np.asarray(margins_N, dtype=np.float64)
    ph = np.array([str(x) for x in phrasing])
    if not (len(mB) == len(mP) == len(mN) == len(ph) == N_ITEMS):
        raise RunInvalid(
            f"scorer input length mismatch: "
            f"{len(mB)}/{len(mP)}/{len(mN)}/{len(ph)} != 60 — RUN-INVALID.")

    ties = int(((mB == 0.0).sum() + (mP == 0.0).sum() + (mN == 0.0).sum()))
    tie_rate = ties / (3 * N_ITEMS)
    if tie_rate > TIE_RATE_BAR:
        raise RunInvalid(
            f"tie rate {tie_rate:.3f} ({ties}/180 item-conditions) > 5% — "
            "degenerate measurement — RUN-INVALID.")

    cB = mB > 0.0
    cP = mP > 0.0
    cN = mN > 0.0
    all_idx = np.arange(N_ITEMS)
    idx_A = np.nonzero(ph == "A-first")[0]
    idx_C = np.nonzero(ph == "C-first")[0]
    if len(idx_A) != 30 or len(idx_C) != 30:
        raise RunInvalid(
            f"phrasing strata malformed: A-first={len(idx_A)}, "
            f"C-first={len(idx_C)} (expected 30/30) — RUN-INVALID.")

    agg = stratum_stats(cB, cP, cN, all_idx)
    sA = stratum_stats(cB, cP, cN, idx_A)
    sC = stratum_stats(cB, cP, cN, idx_C)
    verdict, detail = decide(agg, sA, sC)

    # Secondaries (§4.3, reported, non-binding).
    secondaries = {
        "mean_margin_shift_P": float((mP - mB).mean()),
        "mean_margin_shift_N": float((mN - mB).mean()),
        "flip_ledger": {
            # item indices that flip under each condition (vs baseline)
            "B_wrong_to_P_right": [int(i) for i in np.nonzero(~cB & cP)[0]],
            "B_right_to_P_wrong": [int(i) for i in np.nonzero(cB & ~cP)[0]],
            "B_wrong_to_N_right": [int(i) for i in np.nonzero(~cB & cN)[0]],
            "B_right_to_N_wrong": [int(i) for i in np.nonzero(cB & ~cN)[0]],
        },
        "tie_count": ties,
        "tie_rate": float(tie_rate),
    }
    return {
        "verdict": verdict,
        "verdict_detail": detail,
        "secondaries": secondaries,
        "n": N_ITEMS,
    }
