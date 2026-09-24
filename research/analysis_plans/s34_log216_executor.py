"""S3-4 cone-arm-only flip-stability characterization — LOG-216.

Reads archived EXP077 per-instance records (no weights, no forward passes, $0 CPU).
Classifies the cone arm's alpha-grid flip trajectory per the SAH candidate's
pre-registered definitions (SPRINT3_CANDIDATES_2026-09-23.md, S3-4 section).

Classification (pre-registered from the candidate; MEASURED ON CORRECTNESS,
which the archive records, NOT on raw decisions D(alpha) which it does not):
  D(alpha_k) = argmax decision; archive records correct/incorrect only.
  flip(k)  := correct(alpha_k) != correct(C1).  A correctness flip implies a
             decision flip (sufficient, not necessary: wrong->wrong flips are
             invisible in this archive — flips are a LOWER BOUND on decision flips).
  stable flip at k in {0.25, 0.5, 1.0} := flip(k) AND correct(alpha_{k+1}) == correct(alpha_k)
  unstable flip at k in {0.25, 0.5, 1.0} := flip(k) AND correct(alpha_{k+1}) != correct(alpha_k)
  at alpha = 2.0: flip => indeterminate-persistence (no alpha_{k+1} exists).
  alpha*(x) = smallest alpha_k with a stable flip; 0 (abstain) if none.

Writes machine-readable JSON twin next to the report.
Deterministic: no RNG, no seeds needed.
"""
import json
import math
from pathlib import Path

BASE = Path("/home/hatch/workspace/SCBI")
SRC = BASE / "experiments/runs/EXP077_cone_vs_line/exp077_instance_records.json"
OUT_JSON = BASE / "research/analysis_plans/S34_CONEARM_ANALYSIS_LOG216_2026-09-23.json"

ALPHAS = [0.25, 0.5, 1.0, 2.0]
ARM_KEYS = {0.25: "C2_a025", 0.5: "C3_a050", 1.0: "C4_a100", 2.0: "C5_a200"}
RESCUE_KEYS = {0.25: "A_alpha_0.25", 0.5: "A_alpha_0.5", 1.0: "A_alpha_1", 2.0: "A_alpha_2"}


def wilson_ci(x, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p = x / n
    denom = 1 + z * z / n
    c = p + z * z / (2 * n)
    m = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (max(0.0, (c - m) / denom), min(1.0, (c + m) / denom))


with open(SRC) as f:
    records = json.load(f)

assert len(records) == 60, f"expected 60 items, got {len(records)}"

per_item = []
rescue_mismatch = 0
for rec in records:
    c0 = bool(rec["correct"]["C1"])
    traj = {a: bool(rec["correct"][ARM_KEYS[a]]) for a in ALPHAS}
    flips = {a: (traj[a] != c0) for a in ALPHAS}
    cls = {}  # alpha -> classification
    stable_alphas, unstable_alphas = [], []
    for i, a in enumerate(ALPHAS):
        if not flips[a]:
            cls[str(a)] = "no_flip"
            continue
        if i < len(ALPHAS) - 1:
            nxt = ALPHAS[i + 1]
            if traj[nxt] == traj[a]:  # persists one grid step
                cls[str(a)] = "stable"
                stable_alphas.append(a)
            else:
                cls[str(a)] = "unstable"
                unstable_alphas.append(a)
        else:
            cls[str(a)] = "indeterminate_persistence"
    has_stable = len(stable_alphas) > 0
    has_unstable = len(unstable_alphas) > 0
    indeterminate = cls["2.0"] == "indeterminate_persistence"
    any_flip = any(flips.values())
    alpha_star = min(stable_alphas) if has_stable else 0
    # direction of stable flips relative to baseline correctness
    stable_dirs = []
    for a in stable_alphas:
        stable_dirs.append("rescue" if (not c0 and traj[a]) else ("damage" if (c0 and not traj[a]) else "other"))
    headroom = not c0  # baseline wrong => room to rescue
    # consistency check: archived rescue flags vs computed correctness flips
    flags = rec.get("rescue_indicators", {})
    for a in ALPHAS:
        flag = bool(flags.get(RESCUE_KEYS[a], 0))
        implied_rescue = flips[a] and (not c0) and traj[a]
        if flag != implied_rescue:
            rescue_mismatch += 1
    per_item.append({
        "item": rec["item"],
        "ent": rec["ent"],
        "typ": rec["typ"],
        "baseline_C1_correct": c0,
        "headroom": headroom,
        "cone_correct": {str(a): traj[a] for a in ALPHAS},
        "flip": {str(a): flips[a] for a in ALPHAS},
        "classification": cls,
        "stable_alphas": stable_alphas,
        "stable_flip_directions": stable_dirs,
        "unstable_alphas": unstable_alphas,
        "indeterminate_persistence_at_2.0": indeterminate,
        "any_flip": any_flip,
        "alpha_star": alpha_star,
        "abstain": alpha_star == 0,
    })

n = len(per_item)
n_stable = sum(1 for p in per_item if p["stable_alphas"])
n_unstable_only = sum(1 for p in per_item if p["unstable_alphas"] and not p["stable_alphas"])
n_indet_only = sum(1 for p in per_item if p["indeterminate_persistence_at_2.0"]
                   and not p["stable_alphas"] and not p["unstable_alphas"])
n_noflip = sum(1 for p in per_item if not p["any_flip"])

per_alpha = {}
for i, a in enumerate(ALPHAS):
    flipped = sum(1 for p in per_item if p["flip"][str(a)])
    stable = sum(1 for p in per_item if a in p["stable_alphas"])
    unstable = sum(1 for p in per_item if a in p["unstable_alphas"])
    per_alpha[str(a)] = {"flip_count": flipped, "stable_count": stable,
                         "unstable_count": unstable if i < 3 else None,
                         "indeterminate_count": (1 if False else None)}

alpha_star_dist = {}
for a in ALPHAS:
    alpha_star_dist[str(a)] = sum(1 for p in per_item if p["alpha_star"] == a)
abstentions = sum(1 for p in per_item if p["abstain"])

# killer-box check: stable-flip rate on headroom items
headroom_items = [p for p in per_item if p["headroom"]]
n_headroom = len(headroom_items)
n_hr_stable = sum(1 for p in headroom_items if p["stable_alphas"])
n_hr_stable_rescue = sum(1 for p in headroom_items
                         if any(d == "rescue" for d in p["stable_flip_directions"]))
n_nonheadroom = n - n_headroom
n_nh_stable = sum(1 for p in per_item if not p["headroom"] and p["stable_alphas"])
n_nh_stable_damage = sum(1 for p in per_item if not p["headroom"]
                         and any(d == "damage" for d in p["stable_flip_directions"]))

aggregates = {
    "n_items": n,
    "stable_flip_items": n_stable,
    "stable_flip_rate": n_stable / n,
    "stable_flip_rate_wilson95": list(wilson_ci(n_stable, n)),
    "unstable_flip_items_any": sum(1 for p in per_item if p["unstable_alphas"]),
    "unstable_only_items": n_unstable_only,
    "unstable_only_rate": n_unstable_only / n,
    "indeterminate_only_items": n_indet_only,
    "no_flip_items": n_noflip,
    "no_flip_rate": n_noflip / n,
    "per_alpha": per_alpha,
    "alpha_star_distribution": alpha_star_dist,
    "abstentions": abstentions,
    "abstention_rate": abstentions / n,
    "headroom": {
        "n_headroom_items": n_headroom,
        "n_nonheadroom_items": n_nonheadroom,
        "stable_flip_rate_headroom": (n_hr_stable / n_headroom) if n_headroom else None,
        "stable_flip_rate_headroom_wilson95": (list(wilson_ci(n_hr_stable, n_headroom))
                                               if n_headroom else None),
        "n_headroom_stable_items": n_hr_stable,
        "n_headroom_stable_rescue_items": n_hr_stable_rescue,
        "stable_flip_rate_nonheadroom": (n_nh_stable / n_nonheadroom) if n_nonheadroom else None,
        "n_nonheadroom_stable_damage_items": n_nh_stable_damage,
    },
    "rescue_flag_consistency": {
        "mismatches_flag_vs_computed_rescue": rescue_mismatch,
        "checked_cells": n * len(ALPHAS),
        "note": "A_alpha_* flag vs (flip AND baseline-wrong AND now-correct).",
    },
    "corroboration": {
        "source": "exp077_results.json radial aggregate (same grid)",
        "delta_M": [0.0, 0.0, 0.016666666666666666, 0.016666666666666666],
        "p_values": [1.0, 1.0, 1.0, 1.0],
    },
}

twin = {
    "analysis": "S3-4 cone-arm-only flip-stability characterization (REDUCED; not the full Stage-0 gate)",
    "log": "LOG-216",
    "date": "2026-09-23",
    "source": str(SRC),
    "n_items": n,
    "alpha_grid": ALPHAS,
    "baseline_arm": "C1",
    "cone_arm_keys": ARM_KEYS,
    "definitions": {
        "flip": "correct(alpha_k) != correct(C1); a correctness flip implies a decision flip "
                "(sufficient, not necessary: wrong->wrong decision flips are invisible)",
        "stable_flip": "flip(alpha_k) AND correct(alpha_{k+1}) == correct(alpha_k), k in {0.25,0.5,1.0}",
        "unstable_flip": "flip(alpha_k) AND correct(alpha_{k+1}) != correct(alpha_k), k in {0.25,0.5,1.0}",
        "indeterminate_persistence": "flip at alpha=2.0 (no alpha_{k+1}; stability unassessable)",
        "alpha_star": "smallest alpha with a stable flip; 0 = abstain",
        "headroom": "baseline C1 = wrong (room for a rescue flip)",
        "caution": "Archive records correctness, not decisions D(alpha) = argmax f(x; alpha*v). "
                   "All counts are lower bounds on true decision-flip activity.",
    },
    "per_item": per_item,
    "aggregates": aggregates,
    "limits": [
        "Bridge-vs-B_wrong stable-flip separation (SAH Stage-0 gate, p<0.1) NOT computable: "
        "per-alpha per-instance outcomes for C7_Bwrong/C8_bridge are absent from the archive.",
        "Binary outcomes only: no margins, no logits, no per-item decision labels; "
        "wrong->wrong decision flips are unobservable.",
        "This analysis does not license the GPU pilot gate; it is a characterization only.",
        "Reduced scope only: cone arm (C2-C5) vs baseline C1. C6_offset/C9_cone/C10_control excluded.",
    ],
}

with open(OUT_JSON, "w") as f:
    json.dump(twin, f, indent=1)

print("wrote", OUT_JSON)
print(json.dumps(aggregates, indent=1))
