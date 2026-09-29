"""EXP095 scorer — per-alpha contrast statistics (MECHANICAL ONLY).

Pre-reg: research/innovation/S5-1_PREREG_DRAFT_v2_2026-09-28.md §2.4
(statistics), §5 item 5 (135-cell stratum table), §5 item 6 (decision-table
worksheet, steps 0-2 evidence + per-alpha stats).

This scorer implements ONLY the mechanical read-out. It does NOT walk the
§3 decision table (steps 3-6 belong to the separate verdict lane). The
statistical functions (McNemar exact doubling, Tango CI, paired contrasts)
are imported VERBATIM from EXP094's frozen scorer (score_exp094.py) — the
licensed statistical machinery, not reimplemented.

Conventions (pre-reg §2.4):
  - McNemar exact, doubling convention, per alpha: T(a)-vs-B, Bw(a)-vs-B,
    T(a)-vs-Bw(a) (the last is diagnostic-only, F13 — computed, no role).
  - DELTA_BAR = 0.10; ALPHA_disc = 0.01 (T-vs-B discovery, Bonferroni over
    5 alpha); ALPHA_guard = 0.05 (discriminant/guard contrasts).
  - Correctness: margin > 0 (strict). Tie gate per alpha: ties/180 > 5%
    -> that alpha RUN-INVALID (excluded; no verdict licensed there).
  - 135 cells = 3 strata x 5 alpha x 3 contrasts, machine-written.

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


_score094 = _load_module("exp095_score094",
                         os.path.join(EXP094_DIR, "score_exp094.py"))

# Verbatim licensed machinery (EXP094 scorer — frozen).
mcnemar_exact_p = _score094.mcnemar_exact_p
tango_ci_paired = _score094.tango_ci_paired
contrast_stats = _score094.contrast_stats

N_ITEMS = 60
DELTA_BAR = 0.10
ALPHA_DISC = 0.01
ALPHA_GUARD = 0.05
TIE_RATE_BAR = 0.05
MOVEMENT_GATE = 6
DEGENERACY_BAR = 0.95
ALPHAS = (0.25, 0.5, 1.0, 2.0, 4.0)


class RunInvalid(Exception):
    """Guard/statistical failure -> RUN-INVALID (withheld, never a verdict)."""


def score_alpha(margins_B, margins_Ta, margins_Bwa, phrasing, alpha):
    """Mechanical per-alpha scoring. Returns (table_9_cells, secondaries).

    Raises RunInvalid on the tie-gate breach (>5% of 180 rows) or malformed
    input. Pure statistics — no verdict language.
    """
    import numpy as np
    mB = np.asarray(margins_B, dtype=np.float64)
    mT = np.asarray(margins_Ta, dtype=np.float64)
    mW = np.asarray(margins_Bwa, dtype=np.float64)
    ph = np.array([str(x) for x in phrasing])
    if not (len(mB) == len(mT) == len(mW) == len(ph) == N_ITEMS):
        raise RunInvalid(
            f"scorer input length mismatch at alpha={alpha}: "
            f"{len(mB)}/{len(mT)}/{len(mW)}/{len(ph)} != 60 — RUN-INVALID.")

    ties = int((mB == 0.0).sum() + (mT == 0.0).sum() + (mW == 0.0).sum())
    tie_rate = ties / (3 * N_ITEMS)
    if tie_rate > TIE_RATE_BAR:
        raise RunInvalid(
            f"alpha={alpha}: tie rate {tie_rate:.3f} ({ties}/180) > 5% — "
            "that alpha RUN-INVALID (pre-reg §2.4 tie gate).")

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
            f"alpha={alpha}: phrasing strata malformed "
            f"(A={len(strata['A'])}, C={len(strata['C'])}) — RUN-INVALID.")

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
        "alpha": alpha,
        "n_B_correct": int(cB.sum()),
        "n_T_correct": int(cT.sum()),
        "n_W_correct": int(cW.sum()),
        "mean_margin_shift_T": float((mT - mB).mean()),
        "mean_margin_shift_W": float((mW - mB).mean()),
        "flip_ledger_TB": flips(cT, cB),
        "flip_ledger_WB": flips(cW, cB),
        "tie_count": ties,
        "tie_rate": float(tie_rate),
    }
    return table, secondaries
