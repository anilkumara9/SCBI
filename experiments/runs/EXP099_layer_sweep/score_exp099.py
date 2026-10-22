"""EXP099 scorer — per-contrast statistics (MECHANICAL ONLY).

Licensed protocol: research/innovation/S6-4_PREREG_DRAFT_v2_2026-09-28.md
(binding chain: LOG-4424 (v1) -> LOG-4425 (Law #14 ACCEPT-WITH-FIXES, F1-F9)
-> LOG-4426 (v2 repair) -> LOG-4427 (delta SIGN) -> LOG-4428 (CEO clearance;
S6-4 minted as EXP099). This executor follows the licensed protocol EXACTLY;
any deviation is a STOP + new experiment number.

This scorer implements ONLY the mechanical read-out. It does NOT walk the
§3 decision table (steps 3-8 belong to the separate verdict lane). The
statistical functions (McNemar exact doubling, Tango CI, paired contrasts)
are imported VERBATIM from EXP094's frozen scorer (score_exp094.py) — the
licensed statistical machinery, not reimplemented.

Conventions (protocol §2.4):
  - McNemar exact, doubling convention, over the 60 EXP092-B items:
    L20-only-vs-B [consistency anchor — NOT a discovery contrast],
    L8-only-vs-B [discovery], W20-vs-B, W8-vs-B,
    L8-only-vs-W8 [diagnostic-only — Law #9 hygiene].
  - b = wrong->right (arm right, B wrong); c = right->wrong (arm wrong,
    B right) — EXP094's convention.
  - Delivery exclusions: per (layer, arm) cell, items out of the G5 band are
    excluded from THAT arm's contrasts. L8-only-vs-W8 uses the intersection
    of the (8, L8-only) and (8, W8) masks. Masks are computed by the executor
    (§3 step 1 rule). Count-bars apply to the post-exclusion paired set
    (F4).
  - DELTA_BAR = 0.10; per-layer ALPHA = 0.005. Movement gate: >= 6 flips
    (necessary but not sufficient — §4.2). Correctness: margin > 0 (strict).
  - Tie gate: ties_arm/300 > 5% on any arm -> that arm RUN-INVALID (§2.4;
    the 300 is the protocol's fixed denominator; evaluated per arm).
  - Coherence gate: zero-variance decisions on any injection arm -> that
    arm RUN-INVALID (§2.4). Both gates are REPORTED here as flags; the
    executor computes the machine-written regime routing.
  - 15 cells = 3 strata x 5 contrasts, each with dM + McNemar b/c/p +
    Tango CI, machine-written (§5 item 8). Strata over the bench: agg (60),
    A-first (30), C-first (30) — bench pin, fixed before inspection.

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


_score094 = _load_module("exp099_score094",
                         os.path.join(EXP094_DIR, "score_exp094.py"))

# Verbatim licensed machinery (EXP094 scorer — frozen).
mcnemar_exact_p = _score094.mcnemar_exact_p
tango_ci_paired = _score094.tango_ci_paired
contrast_stats = _score094.contrast_stats

N_ITEMS = 60
DELTA_BAR = 0.10
ALPHA_LAYER = 0.005
TIE_RATE_BAR = 0.05
TIE_DENOMINATOR = 300  # protocol §2.4 fixed denominator (60 items x 5 arms)
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


def score_all(margins_B, margins_L20, margins_L8, margins_W20, margins_W8,
              phrasing, mask_L20, mask_L8, mask_W20, mask_W8):
    """Mechanical scoring for EXP099. Returns (table, sec).

    All margin vectors are length-60 over the bench order. Masks are boolean
    length-60 arrays: True = item included in that arm's contrasts
    (in-band delivery per §3 step 1).
      mask_L20: (20, L20-only) cell; mask_L8: (8, L8-only) cell;
      mask_W20: (20, W20) cell; mask_W8: (8, W8) cell.

    sec reports: gate flags (tie counts/rates, zero-variance flags per
    injection arm), flip counts per contrast (for the anchor count check,
    the liveness instrument, and the decision table), flip ledgers, mean
    margin shifts. Pure statistics — no verdict language.
    """
    import numpy as np
    mB = np.asarray(margins_B, dtype=np.float64)
    mA = {k: np.asarray(v, dtype=np.float64) for k, v in
          (("L20", margins_L20), ("L8", margins_L8),
           ("W20", margins_W20), ("W8", margins_W8))}
    masks = {k: np.asarray(v, dtype=bool) for k, v in
             (("L20", mask_L20), ("L8", mask_L8),
              ("W20", mask_W20), ("W8", mask_W8))}
    ph = np.array([str(x) for x in phrasing])
    if not (len(mB) == len(ph) == N_ITEMS):
        raise RunInvalid("scorer input length mismatch (B/phrasing) — "
                         "RUN-INVALID.")
    for k in mA:
        if not (len(mA[k]) == len(masks[k]) == N_ITEMS):
            raise RunInvalid(f"scorer input length mismatch (arm {k}) — "
                             "RUN-INVALID.")

    # --- tie gate inputs (fixed protocol denominator 300) ---
    tie_counts = {k: int((mA[k] == 0.0).sum()) for k in mA}
    tie_counts["B"] = int((mB == 0.0).sum())
    tie_total = sum(tie_counts.values())
    tie_rate_global = tie_total / TIE_DENOMINATOR
    # Literal protocol reading (§2.4): per arm, ties_arm/300 > 5%.
    tie_gate_arms = [k for k in ("L20", "L8", "W20", "W8")
                     if tie_counts[k] / TIE_DENOMINATOR > TIE_RATE_BAR]

    # --- coherence gate inputs (zero-variance on any injection arm) ---
    zv = {k: bool((mA[k] == mA[k][0]).all()) for k in mA}
    zv["B"] = bool((mB == mB[0]).all())  # B zero-variance -> foundation HOLD
    coherence_arms = [k for k in ("L20", "L8", "W20", "W8") if zv[k]]

    cB = mB > 0.0
    cA = {k: mA[k] > 0.0 for k in mA}
    strata = {
        "agg": np.arange(N_ITEMS),
        "A": np.nonzero(ph == "A-first")[0],
        "C": np.nonzero(ph == "C-first")[0],
    }
    if len(strata["A"]) != 30 or len(strata["C"]) != 30:
        raise RunInvalid(
            f"phrasing strata malformed (A={len(strata['A'])}, "
            f"C={len(strata['C'])}, expected 30/30) — RUN-INVALID.")

    # Contrasts: (name, X-arm key, Y-arm key, mask key for X, mask key for Y)
    contrasts = [
        ("L20B", "L20", "B", "L20", None),  # L20-only-vs-B [anchor]
        ("L8B", "L8", "B", "L8", None),     # L8-only-vs-B [discovery]
        ("W20B", "W20", "B", "W20", None),  # W20-vs-B [control]
        ("W8B", "W8", "B", "W8", None),     # W8-vs-B [control]
        ("L8W8", "L8", "W8", "L8", "W8"),   # L8-only-vs-W8 [diagnostic-only]
    ]

    table = {}
    for sname, idx in strata.items():
        for cname, xk, yk, xmk, ymk in contrasts:
            xmask = masks[xmk][idx]
            if ymk is None:
                use = idx[xmask]
            else:
                use = idx[(masks[xmk] & masks[ymk])[idx]]
            if len(use) == 0:
                raise RunInvalid(
                    f"delivery exclusion emptied contrast {cname} "
                    f"({sname}) — RUN-INVALID.")
            X = cA[xk][use] if xk != "B" else cB[use]
            Y = cB[use] if yk == "B" else cA[yk][use]
            table[f"{sname}__{cname}"] = _cell(contrast_stats(X, Y))

    def flips(x_corr, y_corr):
        return {
            "x_to_right": [int(i) for i in np.nonzero(~y_corr & x_corr)[0]],
            "x_to_wrong": [int(i) for i in np.nonzero(y_corr & ~x_corr)[0]],
        }

    def n_flips(cname):
        st = table[f"agg__{cname}"]
        return int(st["mcnemar_b"] + st["mcnemar_c"])

    sec = {
        "tie_counts": tie_counts,
        "tie_total": int(tie_total),
        "tie_rate_global": float(tie_rate_global),
        "tie_gate_arms": tie_gate_arms,   # per-arm: ties_arm/300 > 5%
        "zero_variance": {k: bool(zv[k]) for k in ("L20", "L8", "W20", "W8", "B")},
        "coherence_arms": coherence_arms,  # per-arm RUN-INVALID routing input
        "n_included": {k: int(masks[k].sum()) for k in masks},
        "n_correct": {"B": int(cB.sum())},
        "flips_vs_B": {},
        "flip_ledgers": {},
        "mean_margin_shift": {},
    }
    for k, cname in (("L20", "L20B"), ("L8", "L8B"),
                     ("W20", "W20B"), ("W8", "W8B")):
        sec["n_correct"][k] = int(cA[k][masks[k]].sum())
        sec["flips_vs_B"][k] = n_flips(cname)
        sec["flip_ledgers"][k] = flips(cA[k][masks[k]], cB[masks[k]])
        sec["mean_margin_shift"][k] = float(
            (mA[k][masks[k]] - mB[masks[k]]).mean()
            if masks[k].any() else float("nan"))
    # L8-only-vs-W8 diagnostic (intersection mask)
    l8w8_use = np.nonzero(masks["L8"] & masks["W8"])[0]
    sec["flips_L8_vs_W8"] = n_flips("L8W8")
    sec["flip_ledger_L8W8"] = flips(cA["L8"][l8w8_use], cA["W8"][l8w8_use])
    return table, sec
