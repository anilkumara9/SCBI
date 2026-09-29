"""EXP097 scorer — per-ratio contrast statistics (MECHANICAL ONLY).

Licensed protocol: research/innovation/S6-1_PREREG_DRAFT_v2_2026-09-28.md
(binding Law #14 ACCEPT-WITH-FIXES: LOG-4411; v2 repair: LOG-4412; delta
re-verification SIGN: LOG-4413; CEO execution clearance: LOG-4414; S6-1
minted as EXP097).

This scorer implements ONLY the mechanical read-out. It does NOT walk the
§3 decision table (steps 3-7 belong to the separate verdict lane). The
statistical functions (McNemar exact doubling, Tango CI, paired contrasts)
are imported VERBATIM from EXP094's frozen scorer (score_exp094.py) — the
licensed statistical machinery, not reimplemented.

Conventions (protocol §2.4):
  - McNemar exact, doubling convention, over the 60 EXP092-B items (ungated):
    per ratio r in {1.5, 3.0}: T(r)-vs-B, B_wrong(r)-vs-B,
    T(r)-vs-B_wrong(r) [diagnostic-only, Law #9 hygiene].
  - Delivery exclusions: per (ratio, arm), items out of the G5 band are
    excluded from THAT arm's contrasts. T-vs-B uses the T-arm mask;
    B_wrong-vs-B uses the B_wrong-arm mask; T-vs-B_wrong uses their
    intersection. Masks are computed by the executor (§3 step 1 rule).
  - DELTA_BAR = 0.10; ALPHA_disc = 0.01 (protocol §2.4). Movement gate:
    >= 6 flips. Correctness: margin > 0 (strict).
  - Tie gate per ratio: ties/180 > 5% -> that ratio RUN-INVALID (§2.4).
  - Coherence gate per ratio: zero-variance decisions on any injection arm
    -> that ratio RUN-INVALID (§2.4). Both gates are REPORTED here as flags;
    the executor computes the machine-written regime routing.
  - 54 cells = 3 strata x 2 ratios x 3 contrasts, each with dM + McNemar
    b/c/p + Tango CI, machine-written (§5 item 6). Strata over the bench:
    agg (60), A-first (30), C-first (30) — bench pin, fixed before inspection.

numpy-only.
"""

import os
import sys

BUNDLE_DIR = os.path.dirname(os.path.abspath(__file__))
EXP094_DIR = os.path.join(os.path.dirname(BUNDLE_DIR), "EXP094_peritem_l11")


def _load_module(name, path):
    import importlib.util
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


_score094 = _load_module("exp097_score094",
                         os.path.join(EXP094_DIR, "score_exp094.py"))

# Verbatim licensed machinery (EXP094 scorer — frozen).
mcnemar_exact_p = _score094.mcnemar_exact_p
tango_ci_paired = _score094.tango_ci_paired
contrast_stats = _score094.contrast_stats

N_ITEMS = 60
DELTA_BAR = 0.10
ALPHA_DISC = 0.01
TIE_RATE_BAR = 0.05
TIE_DENOMINATOR = 180  # 60 items x 3 arms (B, T, B_wrong) per ratio
MOVEMENT_GATE = 6


class RunInvalid(Exception):
    """Guard/statistical failure -> RUN-INVALID (withheld, never a verdict)."""


def _cell(st):
    return {
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


def score_ratio(ratio_label, margins_B, margins_T, margins_W, phrasing,
                mask_T, mask_W):
    """Mechanical per-ratio scoring. Returns (table, sec).

    All margin vectors are length-60 over the bench order. mask_T / mask_W
    are boolean length-60 arrays: True = item included in that arm's
    contrasts (in-band delivery). T-vs-B uses mask_T; B_wrong-vs-B uses
    mask_W; T-vs-B_wrong uses mask_T & mask_W.

    sec reports: gate flags (tie count/rate, zero-variance flags per
    injection arm), flip counts per contrast (for the liveness instrument),
    flip ledgers, mean margin shifts. Pure statistics — no verdict language.
    """
    import numpy as np
    mB = np.asarray(margins_B, dtype=np.float64)
    mT = np.asarray(margins_T, dtype=np.float64)
    mW = np.asarray(margins_W, dtype=np.float64)
    ph = np.array([str(x) for x in phrasing])
    t_ok = np.asarray(mask_T, dtype=bool)
    w_ok = np.asarray(mask_W, dtype=bool)
    if not (len(mB) == len(mT) == len(mW) == len(ph) == len(t_ok) ==
            len(w_ok) == N_ITEMS):
        raise RunInvalid(
            f"scorer input length mismatch for ratio {ratio_label} — "
            "RUN-INVALID.")

    # --- tie gate inputs (over all 180 rows; fixed protocol denominator) ---
    ties = int((mB == 0.0).sum() + (mT == 0.0).sum() + (mW == 0.0).sum())
    tie_rate = ties / TIE_DENOMINATOR
    tie_gate_fires = tie_rate > TIE_RATE_BAR

    # --- coherence gate inputs (zero-variance on any injection arm) ---
    zv_T = bool((mT == mT[0]).all())
    zv_W = bool((mW == mW[0]).all())
    zv_B = bool((mB == mB[0]).all())  # B zero-variance -> foundation HOLD
    coherence_gate_fires = zv_T or zv_W

    cB = mB > 0.0
    cT = mT > 0.0
    cW = mW > 0.0
    strata = {
        "agg": np.arange(N_ITEMS),
        "A": np.nonzero(ph == "A-first")[0],
        "C": np.nonzero(ph == "C-first")[0],
    }
    if len(strata["A"]) != 30 or len(strata["C"]) != 30:
        raise RunInvalid(
            f"phrasing strata malformed (A={len(strata['A'])}, "
            f"C={len(strata['C'])}, expected 30/30) — RUN-INVALID.")

    table = {}
    for sname, idx in strata.items():
        i_tb = idx[t_ok[idx]]
        i_wb = idx[w_ok[idx]]
        i_tw = idx[(t_ok & w_ok)[idx]]
        if len(i_tb) == 0 or len(i_wb) == 0:
            raise RunInvalid(
                f"delivery exclusion emptied a primary contrast "
                f"({ratio_label}, {sname}) — RUN-INVALID.")
        table[f"{sname}__TB"] = _cell(contrast_stats(cT[i_tb], cB[i_tb]))
        table[f"{sname}__WB"] = _cell(contrast_stats(cW[i_wb], cB[i_wb]))
        if len(i_tw) == 0:
            # Practically unreachable (<=2 exclusions/arm keeps >=56 in the
            # intersection); a neutral cell rather than a crash.
            table[f"{sname}__TW"] = {
                "n": 0, "acc_X": float("nan"), "acc_Y": float("nan"),
                "delta": 0.0, "mcnemar_b": 0, "mcnemar_c": 0,
                "mcnemar_p": 1.0, "tango_ci_lo": 0.0, "tango_ci_hi": 0.0,
            }
        else:
            table[f"{sname}__TW"] = _cell(contrast_stats(cT[i_tw], cW[i_tw]))

    def flips(x_corr, y_corr):
        return {
            "x_to_right": [int(i) for i in np.nonzero(~y_corr & x_corr)[0]],
            "x_to_wrong": [int(i) for i in np.nonzero(y_corr & ~x_corr)[0]],
        }

    # Liveness-instrument inputs: flips over the included items per contrast.
    tb_b = table["agg__TB"]["mcnemar_b"] + table["agg__TB"]["mcnemar_c"]
    wb_b = table["agg__WB"]["mcnemar_b"] + table["agg__WB"]["mcnemar_c"]

    sec = {
        "ratio": ratio_label,
        "tie_count": ties,
        "tie_rate": float(tie_rate),
        "tie_gate_fires": bool(tie_gate_fires),
        "zero_variance_T": bool(zv_T),
        "zero_variance_W": bool(zv_W),
        "zero_variance_B": bool(zv_B),
        "coherence_gate_fires": bool(coherence_gate_fires),
        "n_included_T": int(t_ok.sum()),
        "n_included_W": int(w_ok.sum()),
        "n_B_correct": int(cB.sum()),
        "n_T_correct": int(cT[t_ok].sum()),
        "n_W_correct": int(cW[w_ok].sum()),
        "flips_T_vs_B": int(tb_b),
        "flips_W_vs_B": int(wb_b),
        "mean_margin_shift_T": (float((mT[t_ok] - mB[t_ok]).mean())
                                if t_ok.any() else float("nan")),
        "mean_margin_shift_W": (float((mW[w_ok] - mB[w_ok]).mean())
                                if w_ok.any() else float("nan")),
        "flip_ledger_TB": flips(cT[t_ok], cB[t_ok]),
        "flip_ledger_WB": flips(cW[w_ok], cB[w_ok]),
    }
    return table, sec
