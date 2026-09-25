#!/usr/bin/env python3
"""EXP087 verdict adjudication — the registered falsification table (§2)
with binding precedence.

Precedence (binding):
  1. APPARATUS (RUN-INVALID, mechanism verdict withheld, rerun required):
     R5 envelope breach [binding at-signing remap, LOG-324 — NOT CONTINUE];
     headroom-gate violation; pinned-join failure; §3-guard-(iii)
     gross-apparatus (c >= GROSS_CORRUPTION_BAR); Δθ=0/determinism guard
     failure.  Any ONE fires → RUN-INVALID, remaining rows not evaluated.
  2. MECHANISM (CONTINUE — the pure-translation model is dead):
     R1 (any Δm_i ≤ 0, or any C2 corruption c > 0);
     R2 (Hamming(P, observed rescues) ≠ 0);
     R3 (a C3 rescue of a C2-resistant item);
     R4 (corr replication: any outcome other than one-sided p < 0.05).
     First break in R1..R4 order is reported; all breaks are recorded.
  3. KILL: all five rows hold exactly → the bridge's decision effect is
     closed-form explained; mechanism candidacy closed.

The R5 row carries the at-signing re-mapping (CEO option (a), LOG-324):
μ̂ outside [0.649, 0.849] → RUN-INVALID. The retained draft body's
"(table left as LOG-306 signed it)" / CONTINUE mapping is superseded
(ERRATUM, LOG-329 E87-4 — highest severity).

Verdict strings: "KILL" | "CONTINUE" | "RUN-INVALID".
"""

import exp087_guards as G
import exp087_statistics as S


def adjudicate(records, c_vals):
    """Run the full falsification table.

    records: list of 60 dicts with keys:
      'm0' (C1 base margin), 'dm_c2', 'dm_c3',
      'base_correct', 'c2_correct', 'c3_correct' (bools).
    c_vals: list of 60 floats, c[j] paired with records[j] in O order
      (the caller must have applied the pinned join).

    Returns a dict report with 'verdict' and per-row results.
    """
    if len(records) != G.N_ITEMS:
        raise G.BundleError(
            f"verdicts: {len(records)} records, expected {G.N_ITEMS}")
    if len(c_vals) != G.N_ITEMS:
        raise G.BundleError(
            f"verdicts: {len(c_vals)} c values, expected {G.N_ITEMS}")

    report = {"n": G.N_ITEMS, "rows": {}, "diagnostics": {}}
    rows = report["rows"]

    dm2 = [r["dm_c2"] for r in records]
    dm3 = [r["dm_c3"] for r in records]
    base = [r["base_correct"] for r in records]
    c2ok = [r["c2_correct"] for r in records]
    c3ok = [r["c3_correct"] for r in records]

    mu = S.mu_hat(dm2)
    report["mu_hat"] = mu
    report["diagnostics"]["min_dm_c2"] = min(dm2)
    report["diagnostics"]["max_dm_c2"] = max(dm2)

    # ---- 1. APPARATUS (RUN-INVALID) -------------------------------------
    # R5: envelope — binding at-signing remap (LOG-324), NOT CONTINUE.
    rows["R5_envelope"] = {
        "prediction": f"mu_hat in [{G.ENVELOPE_LO}, {G.ENVELOPE_HI}]",
        "observed": mu,
        "holds": S.envelope_check(mu),
        "on_break": "RUN-INVALID",
    }
    if not rows["R5_envelope"]["holds"]:
        report["verdict"] = "RUN-INVALID"
        report["verdict_row"] = "R5_envelope"
        report["verdict_note"] = (
            "mu_hat outside the between-configuration envelope "
            f"[{G.ENVELOPE_LO}, {G.ENVELOPE_HI}]: almost certainly apparatus "
            "failure (mis-constructed bridge, wrong readout extraction); "
            "mechanism verdict WITHHELD, rerun required (LOG-324).")
        return report

    # Headroom gate (carried over from EXP066, §3).
    base_acc = sum(base) / len(base)
    report["diagnostics"]["base_accuracy"] = base_acc
    headroom_ok = G.HEADROOM_LO <= base_acc <= G.HEADROOM_HI
    rows["headroom_gate"] = {
        "prediction": f"base accuracy in [{G.HEADROOM_LO}, {G.HEADROOM_HI}]",
        "observed": base_acc,
        "holds": headroom_ok,
        "on_break": "RUN-INVALID",
    }
    if not headroom_ok:
        report["verdict"] = "RUN-INVALID"
        report["verdict_row"] = "headroom_gate"
        report["verdict_note"] = (
            "base accuracy outside the registered headroom gate: the run is "
            "not in the registered benchmark regime (apparatus).")
        return report

    # §3 guard (iii) gross-apparatus — BUILD-LANE RESOLUTION (flagged for
    # independent review; see BUILD_NOTES.md). Registered R1 handles
    # c in {1,2,3} → CONTINUE; c >= bar is apparatus, not mechanism.
    b, c = S.mcnemar_cells(base, c2ok)
    report["diagnostics"]["mcnemar_b"] = b
    report["diagnostics"]["mcnemar_c"] = c
    report["diagnostics"]["mcnemar_archived"] = [G.ARCH_B, G.ARCH_C]
    gross = c >= G.GROSS_CORRUPTION_BAR
    rows["guard_iii_gross"] = {
        "prediction": f"C2 corruptions c < {G.GROSS_CORRUPTION_BAR} "
                      f"(archived c={G.ARCH_C})",
        "observed": c,
        "holds": not gross,
        "on_break": "RUN-INVALID",
        "note": ("build-lane resolution: threshold not in the signed "
                 "protocol; flagged for independent review"),
    }
    if gross:
        report["verdict"] = "RUN-INVALID"
        report["verdict_row"] = "guard_iii_gross"
        report["verdict_note"] = (
            f"{c} C2 corruptions (>= {G.GROSS_CORRUPTION_BAR}): the C2 arm "
            "cannot be the registered bridge under any "
            "translation-compatible noise (apparatus).")
        return report

    # ---- 2. MECHANISM ROWS (CONTINUE on any break) -----------------------
    breaks = []

    # R1: strict positivity + no corruption.
    min_dm = min(dm2)
    r1_pos = S.strict_positivity(dm2)
    rows["R1_positivity"] = {
        "prediction": "min_i dm_c2 > 0",
        "observed": min_dm,
        "holds": r1_pos,
        "on_break": "CONTINUE",
    }
    if not r1_pos:
        breaks.append("R1_positivity")
    rows["R1_corruption"] = {
        "prediction": "C2 corruptions c = 0",
        "observed": c,
        "holds": c == 0,
        "on_break": "CONTINUE",
    }
    if c > 0:
        breaks.append("R1_corruption")

    # R2: rescue-set identity (the primary endpoint).
    P = S.predicted_rescue_set(records)
    O2 = S.observed_rescues(records, "c2_correct")
    ham = S.hamming_distance(P, O2)
    rows["R2_identity"] = {
        "prediction": "rescued_C2 == P exactly (Hamming = 0)",
        "observed": ham,
        "holds": ham == 0,
        "on_break": "CONTINUE",
        "n_predicted": len(P),
        "n_observed": len(O2),
    }
    if ham != 0:
        breaks.append("R2_identity")

    # R3: boundary-band subset.
    O3 = S.observed_rescues(records, "c3_correct")
    holds_r3, viol = S.subset_check(O3, O2)
    rows["R3_subset"] = {
        "prediction": "rescued_C3 ⊆ rescued_C2",
        "observed": f"{len(O3)} C3 rescues, violators={viol}",
        "holds": holds_r3,
        "on_break": "CONTINUE",
    }
    if not holds_r3:
        breaks.append("R3_subset")

    # R4: corr partial replication.
    r, p, passes = S.corr_replication_test(dm2, c_vals)
    rows["R4_corr"] = {
        "prediction": "corr(dm_c2, c_i) > 0, one-sided p < 0.05",
        "observed": {"r": r, "p_one_sided": p},
        "holds": passes,
        "on_break": "CONTINUE",
    }
    report["diagnostics"]["corr_r"] = r
    report["diagnostics"]["corr_p_one_sided"] = p
    if not passes:
        breaks.append("R4_corr")

    # LayerNorm-saturation diagnostic (§3 guard ii; §8 item 4): recorded,
    # feeds the breaking-point analysis, never a verdict by itself.
    flagged, mu_f, sig = S.layernorm_saturation_flag(dm2)
    report["diagnostics"]["layernorm_4sigma_flagged"] = flagged
    report["diagnostics"]["layernorm_note"] = (
        "diagnostic only — does not alter any verdict row")

    if breaks:
        report["verdict"] = "CONTINUE"
        report["verdict_row"] = breaks[0]
        report["all_breaks"] = breaks
        report["verdict_note"] = (
            "the pure-translation model is dead; non-translation structure "
            "exists — the mechanism hunt re-opens on the output side "
            "(Law #7 boundary: CONTINUE does NOT license the bridge as a "
            "positive control for autonomous steering).")
        return report

    # ---- 3. KILL ---------------------------------------------------------
    report["verdict"] = "KILL"
    report["verdict_row"] = "all_rows_hold"
    report["verdict_note"] = (
        "all five rows hold exactly: the bridge's decision effect is "
        "closed-form explained (uniform t−f margin translation); no "
        "item-specific mechanism; the bridge becomes a calibrated "
        "translation instrument, nothing more.")
    return report
