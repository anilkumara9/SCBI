"""EXP098 scorer — per-contrast statistics (MECHANICAL ONLY).

Licensed protocol: research/innovation/S6-2_PREREG_DRAFT_v2_2026-09-28.md
(binding Law #14 ACCEPT-WITH-FIXES: LOG-4418; v2 repair: LOG-4419;
independent delta re-verification SIGN: LOG-4420; CEO execution clearance:
LOG-4421; S6-2 minted as EXP098).

This scorer implements ONLY the mechanical read-out. It does NOT walk the
§3 decision table (steps 3-8 belong to the separate verdict lane). The
statistical functions (McNemar exact doubling, Tango CI, paired contrasts)
are imported VERBATIM from EXP094's frozen scorer (score_exp094.py) — the
licensed statistical machinery, not reimplemented.

Conventions (protocol §2.4):
  - McNemar exact, doubling convention, over the 60 EXP092-B items:
    joint-vs-B [discovery], L11-only-vs-B, L20-only-vs-B, W-joint-vs-B,
    joint-vs-W-joint [diagnostic-only, Law #9 hygiene].
  - Delivery exclusions: per (layer, arm) cell, items out of the G5 band are
    excluded from THAT arm's contrasts. Joint-vs-B uses the intersection of
    the (11, Joint) and (20, Joint) masks; W-joint-vs-B the intersection of
    the (11, W-joint) and (20, W-joint) masks; joint-vs-W-joint the
    intersection of all four. Masks are computed by the executor
    (§3 step 1 rule).
  - DELTA_BAR = 0.10; ALPHA_disc = 0.01 (protocol §2.4). Movement gate:
    >= 6 flips. Correctness: margin > 0 (strict).
  - Tie gate: ties/300 > 5% on any arm -> that arm RUN-INVALID (§2.4; the
    300 is the protocol's fixed denominator; the gate is evaluated per arm).
  - Coherence gate: zero-variance decisions on any injection arm -> that
    arm RUN-INVALID (§2.4). Both gates are REPORTED here as flags; the
    executor computes the machine-written regime routing.
  - 15 cells = 3 strata x 5 contrasts, each with dM + McNemar b/c/p +
    Tango CI, machine-written (§5 item 7). Strata over the bench: agg (60),
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


_score094 = _load_module("exp098_score094",
                         os.path.join(EXP094_DIR, "score_exp094.py"))

# Verbatim licensed machinery (EXP094 scorer — frozen).
mcnemar_exact_p = _score094.mcnemar_exact_p
tango_ci_paired = _score094.tango_ci_paired
contrast_stats = _score094.contrast_stats

N_ITEMS = 60
DELTA_BAR = 0.10
ALPHA_DISC = 0.01
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


def score_all(margins_B, margins_L11, margins_L20, margins_J,
              margins_W, phrasing,
              mask_L11, mask_L20, mask_J, mask_W):
    """Mechanical scoring for EXP098. Returns (table, sec).

    All margin vectors are length-60 over the bench order. Masks are boolean
    length-60 arrays: True = item included in that arm's contrasts
    (in-band delivery per §3 step 1).
      mask_L11: (11, L11-only) cell; mask_L20: (20, L20-only) cell;
      mask_J: intersection of (11, Joint) and (20, Joint) cells;
      mask_W: intersection of (11, W-joint) and (20, W-joint) cells.

    sec reports: gate flags (tie counts/rates, zero-variance flags per
    injection arm), flip counts per contrast (for the liveness instrument
    and the decision table), flip ledgers, mean margin shifts. Pure
    statistics — no verdict language.
    """
    import numpy as np
    mB = np.asarray(margins_B, dtype=np.float64)
    mA = {k: np.asarray(v, dtype=np.float64) for k, v in
          (("L11", margins_L11), ("L20", margins_L20),
           ("J", margins_J), ("W", margins_W))}
    masks = {k: np.asarray(v, dtype=bool) for k, v in
             (("L11", mask_L11), ("L20", mask_L20),
              ("J", mask_J), ("W", mask_W))}
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
    tie_gate_arms = [k for k in ("L11", "L20", "J", "W")
                     if tie_counts[k] / TIE_DENOMINATOR > TIE_RATE_BAR]

    # --- coherence gate inputs (zero-variance on any injection arm) ---
    zv = {k: bool((mA[k] == mA[k][0]).all()) for k in mA}
    zv["B"] = bool((mB == mB[0]).all())  # B zero-variance -> foundation HOLD
    coherence_arms = [k for k in ("L11", "L20", "J", "W") if zv[k]]

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
        ("JB", "J", "B", "J", None),      # joint-vs-B [discovery]
        ("L11B", "L11", "B", "L11", None),  # L11-only-vs-B [premise]
        ("L20B", "L20", "B", "L20", None),  # L20-only-vs-B [premise]
        ("WB", "W", "B", "W", None),      # W-joint-vs-B [control]
        ("JW", "J", "W", "J", "W"),        # joint-vs-W-joint [diagnostic]
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
        "zero_variance": {k: bool(zv[k]) for k in ("L11", "L20", "J", "W", "B")},
        "coherence_arms": coherence_arms,  # per-arm RUN-INVALID routing input
        "n_included": {k: int(masks[k].sum()) for k in masks},
        "n_correct": {"B": int(cB.sum())},
        "flips_vs_B": {},
        "flip_ledgers": {},
        "mean_margin_shift": {},
    }
    for k, cname in (("L11", "L11B"), ("L20", "L20B"),
                     ("J", "JB"), ("W", "WB")):
        sec["n_correct"][k] = int(cA[k][masks[k]].sum())
        sec["flips_vs_B"][k] = n_flips(cname)
        sec["flip_ledgers"][k] = flips(cA[k][masks[k]], cB[masks[k]])
        sec["mean_margin_shift"][k] = float(
            (mA[k][masks[k]] - mB[masks[k]]).mean()
            if masks[k].any() else float("nan"))
    # joint-vs-W-joint diagnostic (intersection mask)
    jw_use = np.nonzero(masks["J"] & masks["W"])[0]
    sec["flips_J_vs_W"] = n_flips("JW")
    sec["flip_ledger_JW"] = flips(cA["J"][jw_use], cA["W"][jw_use])
    return table, sec
