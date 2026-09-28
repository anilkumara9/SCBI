"""EXP096 scorer — gated contrast statistics (MECHANICAL ONLY).

Signed pre-reg: research/innovation/S5-4_PREREG_DRAFT_v2_2026-09-28.md §2.4
(statistics), §5 item 5 (27-cell stratum table), §5 item 6 (decision-table
worksheet).

This scorer implements ONLY the mechanical read-out. It does NOT walk the
§3 decision table (steps 3-6 belong to the separate verdict lane). The
statistical functions (McNemar exact doubling, Tango CI, paired contrasts)
are imported VERBATIM from EXP094's frozen scorer (score_exp094.py) — the
licensed statistical machinery, not reimplemented.

Conventions (pre-reg §2.4):
  - McNemar exact, doubling convention, over the frozen gated set G (|G|=21):
    T(8.0)-vs-B, B_wrong(8.0)-vs-B, T(8.0)-vs-B_wrong(8.0) [diagnostic-only,
    Law #9 hygiene — computed, no decision role].
  - DELTA_BAR = 0.10; ALPHA_disc = 0.05 — single primary contrast, no
    Bonferroni. Movement gate: >= 6 flips (b=6,c=0 -> p=0.03125).
  - Correctness: margin > 0 (strict). Tie gate: ties/42 > 5% -> RUN-INVALID.
  - 9 cells = 3 strata x 3 contrasts, machine-written. (The protocol's §5
    item 5 says "27 cells" — arithmetic shorthand; actual coverage is 9
    contrast cells, each with ΔM + McNemar b/c/p + Tango CI. Disclosed in
    the execution log, cf. EXP095's LOG-4399 caveat #1.) Strata over G:
    agg (21), A-first (13), C-first (8) — per frozen Appendix A.
  - Stratum bars relaxed: per-stratum ΔM reported; step-6a heterogeneity
    veto belongs to the verdict lane, not this scorer.

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


_score094 = _load_module("exp096_score094",
                         os.path.join(EXP094_DIR, "score_exp094.py"))

# Verbatim licensed machinery (EXP094 scorer — frozen).
mcnemar_exact_p = _score094.mcnemar_exact_p
tango_ci_paired = _score094.tango_ci_paired
contrast_stats = _score094.contrast_stats

N_GATED = 21
N_A_FIRST = 13
N_C_FIRST = 8
DELTA_BAR = 0.10
ALPHA_DISC = 0.05
TIE_RATE_BAR = 0.05
MOVEMENT_GATE = 6


class RunInvalid(Exception):
    """Guard/statistical failure -> RUN-INVALID (withheld, never a verdict)."""


def score_gated(margins_B_g, margins_T_g, margins_W_g, phrasing_g):
    """Mechanical gated scoring over the frozen set G. Returns (table, sec).

    All inputs are length-21 vectors over the frozen Appendix-A member order.
    Raises RunInvalid on the tie-gate breach (>5% of 42 rows) or malformed
    input. Pure statistics — no verdict language.
    """
    import numpy as np
    mB = np.asarray(margins_B_g, dtype=np.float64)
    mT = np.asarray(margins_T_g, dtype=np.float64)
    mW = np.asarray(margins_W_g, dtype=np.float64)
    ph = np.array([str(x) for x in phrasing_g])
    if not (len(mB) == len(mT) == len(mW) == len(ph) == N_GATED):
        raise RunInvalid(
            f"scorer input length mismatch: "
            f"{len(mB)}/{len(mT)}/{len(mW)}/{len(ph)} != {N_GATED} — "
            "RUN-INVALID.")

    ties = int((mB == 0.0).sum() + (mT == 0.0).sum() + (mW == 0.0).sum())
    tie_rate = ties / (2 * N_GATED)
    if tie_rate > TIE_RATE_BAR:
        raise RunInvalid(
            f"gated tie rate {tie_rate:.3f} ({ties}/42) > 5% — RUN-INVALID "
            "(pre-reg §2.4 tie gate).")

    cB = mB > 0.0
    cT = mT > 0.0
    cW = mW > 0.0
    strata = {
        "agg": np.arange(N_GATED),
        "A": np.nonzero(ph == "A-first")[0],
        "C": np.nonzero(ph == "C-first")[0],
    }
    if len(strata["A"]) != N_A_FIRST or len(strata["C"]) != N_C_FIRST:
        raise RunInvalid(
            f"gated phrasing strata malformed "
            f"(A={len(strata['A'])}, C={len(strata['C'])}, "
            f"expected {N_A_FIRST}/{N_C_FIRST}) — RUN-INVALID.")

    cells = {}
    for sname, idx in strata.items():
        cells[(sname, "TB")] = contrast_stats(cT[idx], cB[idx])
        cells[(sname, "WB")] = contrast_stats(cW[idx], cB[idx])
        cells[(sname, "TW")] = contrast_stats(cT[idx], cW[idx])

    table = {}
    for (sname, contrast), st in cells.items():
        table[f"{sname}__{contrast}"] = {
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

    def flips(x_corr, y_corr):
        return {
            "x_to_right": [int(i) for i in np.nonzero(~y_corr & x_corr)[0]],
            "x_to_wrong": [int(i) for i in np.nonzero(y_corr & ~x_corr)[0]],
        }

    secondaries = {
        "n_B_correct": int(cB.sum()),
        "n_T_correct": int(cT.sum()),
        "n_W_correct": int(cW.sum()),
        "mean_margin_shift_T": float((mT - mB).mean()),
        "mean_margin_shift_W": float((mW - mB).mean()),
        "max_abs_margin_shift_T": float(np.abs(mT - mB).max()),
        "flip_ledger_TB": flips(cT, cB),
        "flip_ledger_WB": flips(cW, cB),
        "tie_count": ties,
        "tie_rate": float(tie_rate),
    }
    return table, secondaries
