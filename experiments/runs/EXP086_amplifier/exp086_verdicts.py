#!/usr/bin/env python3
"""EXP086 verdict adjudication: the signed §9 verdict table, evaluated in
EXACT pre-registered order.

Order (binding): INVALID V1-V4 -> KILL V5, V6 -> CONTINUE V7 -> HELD V7b
(evaluated after V7, before V8) -> PIVOT V8 -> HELD V9, V10, V11, V12.

Precedence notes (binding readings; flagged in BUILD_NOTES for Law #14):
  * V5 (kill-first diagnostic) is evaluated BEFORE V7, so a ĉ-kill preempts
    a primary win that would otherwise CONTINUE ("evaluated in order", §9).
  * V6 (primary gain excluded) is evaluated before the HELD rows, including
    V11 (rank undefined). §6.4's "fail-safe, never KILL" governs the rank
    test itself, not the independent primary-gain exclusion.
  * Rows whose conjuncts reference Δ_rank are inapplicable when rank_valid
    is False; control falls through to V11 (HELD), never to a rank-based
    CONTINUE/PIVOT.
  * Stage-2 gate: primary win (V7's first two conjuncts) REQUIRES stage-2 to
    have run (§4: "runs only if the primary win criterion fires"). A primary
    win with stage2_ran=False is an execution-process defect -> loud halt
    (InvalidRunError), never a silent HELD.

adjudicate(results) -> (verdict, evidentiary, detail).
verdict in {INVALID, KILL, CONTINUE, PIVOT, HELD}; detail names the row.
Evidentiary labels follow the program's adopted standard
(Supported / Not supported / Inconclusive / Underdetermined / Refuted).
"""

import exp086_guards as G

DELTA_MIN = G.DELTA_MIN
ALPHA = G.MCNEMAR_ALPHA


def _primary_win(r):
    """V7's first two conjuncts: LCI(Δ) > 0.05 AND one-sided McNemar p ≤ 0.05."""
    return (r["delta_lci"] > DELTA_MIN) and (r["mcnemar_p"] <= ALPHA)


def adjudicate(r):
    """Apply the §9 verdict table. r: results dict (see module docstring).

    Required keys: delta_theta_ok, n_wrong_baseline, frac_aborted,
    apparatus_ok, c_hat, exceedance, delta_lci, delta_uci, delta_point,
    mcnemar_p, rank_valid, delta_rank_lci, delta_rank_uci, delta_rank_point,
    stage2_ran, delta_perm_lci (None if stage-2 did not run).
    """
    need = ("delta_theta_ok", "n_wrong_baseline", "frac_aborted",
            "apparatus_ok", "c_hat", "exceedance", "delta_lci", "delta_uci",
            "delta_point", "mcnemar_p", "rank_valid", "delta_rank_lci",
            "delta_rank_uci", "delta_rank_point", "stage2_ran", "delta_perm_lci")
    missing = [k for k in need if k not in r]
    if missing:
        raise KeyError(f"adjudicate: missing result keys {missing} (loud halt)")

    pw = _primary_win(r)

    # ---- INVALID (apparatus/probe failures; fail-safe, never scientific) ----
    if not r["delta_theta_ok"]:
        return ("INVALID", "Underdetermined",
                "V1: Δθ != 0 (state_dict hash mismatch).")
    if r["n_wrong_baseline"] < G.HEADROOM_MIN:
        return ("INVALID", "Underdetermined",
                f"V2: {r['n_wrong_baseline']} wrong-at-baseline < "
                f"{G.HEADROOM_MIN} (infeasible probe).")
    if r["frac_aborted"] > G.MAX_ABORT_FRAC:
        return ("INVALID", "Underdetermined",
                f"V3: {r['frac_aborted']:.2%} items power-iteration "
                "non-converged (>50%) — UNDEFINED-LANDSCAPE.")
    if not r["apparatus_ok"]:
        return ("INVALID", "Underdetermined",
                "V4: apparatus check failed (proxy-unresponsive apparatus).")

    # ---- KILL (family dead) ----
    if r["c_hat"] < G.CHAT_BAR and r["exceedance"] < G.EXCEEDANCE_BAR:
        return ("KILL", "Refuted",
                f"V5 kill-first: ĉ={r['c_hat']:.4f} < {G.CHAT_BAR} and "
                f"E={r['exceedance']:.3f} < {G.EXCEEDANCE_BAR:.0%} — gain "
                "without decision relevance is noise amplification.")
    if r["delta_uci"] < DELTA_MIN:
        return ("KILL", "Refuted",
                f"V6: 95% Tango CI for Δ=({r['delta_lci']:.4f}, "
                f"{r['delta_uci']:.4f}) entirely below +{DELTA_MIN} "
                "(primary gain excluded).")

    # ---- rank-dependent rows need a defined rank test ----
    rv = bool(r["rank_valid"])

    # Stage-2 process gate (loud halt, never a silent verdict)
    if pw and rv and r["delta_rank_lci"] > 0 and not r["stage2_ran"]:
        raise G.InvalidRunError(
            "adjudicate: primary win + rank conjunct met but Stage-2 did not "
            "run — execution-process defect (§4: Stage-2 runs iff the primary "
            "win criterion fires). Loud halt; no verdict emitted."
        )

    # ---- CONTINUE (all conjuncts) ----
    if (pw and rv and r["delta_rank_lci"] > 0 and r["stage2_ran"]
            and r["delta_perm_lci"] is not None and r["delta_perm_lci"] > 0):
        return ("CONTINUE", "Supported",
                f"V7: LCI(Δ)={r['delta_lci']:.4f} > {DELTA_MIN}, McNemar "
                f"p={r['mcnemar_p']:.4g} ≤ {ALPHA}, "
                f"LCI(Δ_rank)={r['delta_rank_lci']:.4f} > 0, "
                f"Stage-2 LCI(Δ_perm)={r['delta_perm_lci']:.4f} > 0 — "
                "licenses full-scale follow-up of the dynamical-amplifier "
                "family at L1.")

    # ---- V7b (after V7, before V8): primary win + rank win + permuted fail --
    if (pw and rv and r["delta_rank_lci"] > 0 and r["stage2_ran"]
            and (r["delta_perm_lci"] is None or r["delta_perm_lci"] <= 0)):
        return ("HELD", "Inconclusive",
                "V7b: primary win + rank win, but Stage-2 permuted conjunct "
                "not met (LCI(Δ_perm) ≤ 0) — gain is not item-specific; the "
                "direction-noise reading. Do not CONTINUE.")

    # ---- PIVOT (effect real, family signature failed) ----
    if (pw and rv and r["delta_rank_uci"] < DELTA_MIN
            and r["delta_rank_point"] <= 0):
        return ("PIVOT", "Not supported",
                f"V8: primary win but rank gradient excluded "
                f"(CI(Δ_rank)=({r['delta_rank_lci']:.4f}, "
                f"{r['delta_rank_uci']:.4f}) entirely below +{DELTA_MIN}, "
                "point ≤ 0) — re-scope to the max-displacement-direction "
                "reading; the dynamical-amplifier family's discriminating "
                "signature failed.")

    # ---- HELD ----
    if (pw and rv and r["delta_rank_lci"] <= 0 <= r["delta_rank_uci"]
            and not (r["delta_rank_uci"] < DELTA_MIN
                     and r["delta_rank_point"] <= 0)):
        return ("HELD", "Inconclusive",
                f"V9: primary win but rank straddles "
                f"(CI(Δ_rank)=({r['delta_rank_lci']:.4f}, "
                f"{r['delta_rank_uci']:.4f}) crosses 0, not excluded) — win "
                "without the mechanism signature is not CONTINUE.")
    if r["c_hat"] < G.CHAT_BAR and r["exceedance"] >= G.EXCEEDANCE_BAR:
        return ("HELD", "Inconclusive",
                f"V10: ĉ={r['c_hat']:.4f} < {G.CHAT_BAR} with "
                f"E={r['exceedance']:.3f} ≥ {G.EXCEEDANCE_BAR:.0%} — re-scope "
                "to conditional variant (the mean masked a decision-useful "
                "minority).")
    if not rv:
        return ("HELD", "Inconclusive",
                "V11: σ̂₁/σ̂₃ < 1.2 — rank test UNDEFINED → HELD "
                "(fail-safe, never KILL).")
    if r["delta_lci"] <= DELTA_MIN:
        return ("HELD", "Inconclusive",
                f"V12: primary straddles "
                f"(CI(Δ)=({r['delta_lci']:.4f}, {r['delta_uci']:.4f}) crosses "
                f"+{DELTA_MIN}, not excluded by V6).")

    # ---- fall-through: table has no row for this input combination ----
    return ("HELD", "Inconclusive",
            "UNCLASSIFIED: no §9 row matched this input combination — the "
            "pre-registered table is incomplete for this input. HELD by "
            "fail-safe default (never CONTINUE/KILL on an unlisted case). "
            "Flagged for protocol review.")
