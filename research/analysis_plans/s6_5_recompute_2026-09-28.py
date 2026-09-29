#!/usr/bin/env python3
"""S6-5 pooled power audit — recomputation script (2026-09-28).

Recomputes flip counts from the EXP095/EXP096 primary CSVs (nothing trusted
from the executors' arithmetic), verifies a sample of the S5-2 (LOG-4392)
zero-event bounds, and computes exact Clopper-Pearson bounds for all pools.

Conventions (same as S5-2 / LOG-4392):
  - exact one-sided 95% upper: smallest p with P(X <= k | n, p) = 0.05
      (for k = 0 this is the closed form 1 - 0.05**(1/n))
  - CP two-sided upper: smallest p with P(X <= k | n, p) = 0.025
      (for k = 0 this is 1 - 0.025**(1/n))
  - rule-of-three 3/n shown for k = 0 only (S5-2 continuity)

Pure stdlib (math.comb bisection). Read-only on records.
"""
import csv
import json
import math

ALPHA = 0.05

# ----------------------------------------------------------------------------
# Binomial CDF + Clopper-Pearson upper via bisection
# ----------------------------------------------------------------------------

def binom_cdf_le(k, n, p):
    """P(X <= k) for X ~ Binomial(n, p)."""
    if p <= 0.0:
        return 1.0
    if p >= 1.0:
        return 1.0 if k >= n else 0.0
    q = 1.0 - p
    # iterate terms downward-safe: sum i=0..k
    total = 0.0
    # use log-free direct computation; n <= ~1500, k <= ~12: fine
    for i in range(0, k + 1):
        total += math.comb(n, i) * (p ** i) * (q ** (n - i))
    return total


def cp_upper(k, n, tail):
    """Smallest p in [0,1] with P(X <= k | n, p) = tail (bisection)."""
    assert 0 <= k <= n
    lo, hi = 0.0, 1.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if binom_cdf_le(k, n, mid) > tail:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def bounds(k, n):
    one_sided = cp_upper(k, n, ALPHA)
    two_sided = cp_upper(k, n, ALPHA / 2)
    # closed-form check for k=0
    if k == 0:
        assert abs(one_sided - (1 - ALPHA ** (1 / n))) < 1e-9
        assert abs(two_sided - (1 - (ALPHA / 2) ** (1 / n))) < 1e-9
    return {
        "k": k, "n": n,
        "rate": k / n,
        "exact_1sided_95": one_sided,
        "cp_2sided_upper": two_sided,
        "rule_of_three": (3 / n) if k == 0 else None,
    }

# ----------------------------------------------------------------------------
# Recompute flip counts from primary CSVs
# ----------------------------------------------------------------------------

def load(path):
    with open(path) as f:
        return list(csv.DictReader(f))

exp095 = load("/home/hatch/workspace/SCBI/experiments/runs/EXP095_alpha_sweep/out/per_item_records.csv")
exp096 = load("/home/hatch/workspace/SCBI/experiments/runs/EXP096_headroom_gated/out/per_item_records.csv")

print(f"EXP095 rows: {len(exp095)} | EXP096 rows: {len(exp096)}")

# EXP095: flip = correct_top1 differs from B for same item (B has alpha='n/a')
b95 = {r["item_id"]: int(r["correct_top1"]) for r in exp095 if r["arm"] == "B"}
assert len(b95) == 60
flips95 = {}
for r in exp095:
    if r["arm"] == "B":
        continue
    key = (r["alpha"], r["arm"])
    flips95.setdefault(key, {"n": 0, "flips": 0})
    flips95[key]["n"] += 1
    if int(r["correct_top1"]) != b95[r["item_id"]]:
        flips95[key]["flips"] += 1

print("\nEXP095 flips vs B (recomputed):")
for key in sorted(flips95):
    print(f"  alpha={key[0]} arm={key[1]}: {flips95[key]['flips']}/{flips95[key]['n']}")

t95 = sum(v["flips"] for k, v in flips95.items() if k[1] == "T")
n95t = sum(v["n"] for k, v in flips95.items() if k[1] == "T")
w95 = sum(v["flips"] for k, v in flips95.items() if k[1] == "B_wrong")
n95w = sum(v["n"] for k, v in flips95.items() if k[1] == "B_wrong")
assert (t95, n95t) == (2, 300), f"EXP095 T mismatch: {(t95, n95t)} (verdict: 2/300)"
assert (w95, n95w) == (2, 300), f"EXP095 B_wrong mismatch: {(w95, n95w)} (verdict: 2/300)"
print(f"EXP095 T-only: {t95}/{n95t} | all-injection: {t95 + w95}/{n95t + n95w}  [VERIFIED vs LOG-4400]")

# EXP096: arms are 'T(8.0)' and 'B_wrong(8.0)'; B has 60 rows, gated arms 21 each
b96 = {r["item_id"]: int(r["correct_top1"]) for r in exp096 if r["arm"] == "B"}
assert len(b96) == 60
flips96 = {}
for r in exp096:
    if r["arm"] == "B":
        continue
    arm = "T" if r["arm"].startswith("T(") else "B_wrong"
    flips96.setdefault(arm, {"n": 0, "flips": 0})
    flips96[arm]["n"] += 1
    if int(r["correct_top1"]) != b96[r["item_id"]]:
        flips96[arm]["flips"] += 1

print("\nEXP096 flips vs B (recomputed):")
for arm in ("T", "B_wrong"):
    print(f"  {arm}: {flips96[arm]['flips']}/{flips96[arm]['n']}")
assert (flips96["T"]["flips"], flips96["T"]["n"]) == (3, 21), "EXP096 T mismatch (verdict: 3/21)"
assert (flips96["B_wrong"]["flips"], flips96["B_wrong"]["n"]) == (3, 21), "EXP096 B_wrong mismatch"
print("EXP096 T-only: 3/21 | all-injection: 6/42  [VERIFIED vs LOG-4407]")

# ----------------------------------------------------------------------------
# S5-2 verification sample (committed statistics from LOG-4392)
# ----------------------------------------------------------------------------
print("\n--- S5-2 verification sample ---")
for k, n, label in [(0, 60, "per-arm 0/60"), (0, 120, "EXP094 agg 0/120"),
                    (0, 540, "Bench A 0/540"), (0, 180, "Bench B 0/180"),
                    (0, 780, "grand 0/780")]:
    b = bounds(k, n)
    print(f"  {label}: 1-sided={b['exact_1sided_95']*100:.2f}% "
          f"(LOG-4392: {[4.87,2.47,0.55,1.65,0.38][[(0,60),(0,120),(0,540),(0,180),(0,780)].index((k,n))]}%)")

# ----------------------------------------------------------------------------
# Pools
# ----------------------------------------------------------------------------
pools = {
    # new per-experiment
    "EXP095_T_only": (t95, n95t),
    "EXP095_all_injection": (t95 + w95, n95t + n95w),
    "EXP096_T_only_gated": (flips96["T"]["flips"], flips96["T"]["n"]),
    "EXP096_all_injection_gated": (flips96["T"]["flips"] + flips96["B_wrong"]["flips"],
                                   flips96["T"]["n"] + flips96["B_wrong"]["n"]),
    # static per-item family: EXP094 (LOG-4375/4376: T 0/60, T+R 0/120)
    "family_peritem_T_only": (0 + t95 + flips96["T"]["flips"],
                              60 + n95t + flips96["T"]["n"]),
    "family_peritem_all_injection": (0 + t95 + w95 + flips96["T"]["flips"] + flips96["B_wrong"]["flips"],
                                     120 + n95t + n95w + flips96["T"]["n"] + flips96["B_wrong"]["n"]),
    # Bench B extended (pythia-410m L11, EXP092-B): EXP093 0/60 (shared-dir) + EXP094 0/120
    "benchB_L11_extended": (0 + 0 + t95 + w95 + flips96["T"]["flips"] + flips96["B_wrong"]["flips"],
                            60 + 120 + n95t + n95w + flips96["T"]["n"] + flips96["B_wrong"]["n"]),
    # grand extended: S5-2 0/780 + new injection cells
    "grand_extended": (0 + t95 + w95 + flips96["T"]["flips"] + flips96["B_wrong"]["flips"],
                       780 + n95t + n95w + flips96["T"]["n"] + flips96["B_wrong"]["n"]),
}

results = {}
print("\n--- Pools (exact 1-sided 95% upper | CP 2-sided upper | observed rate) ---")
for name, (k, n) in pools.items():
    b = bounds(k, n)
    results[name] = b
    print(f"  {name}: {k}/{n} -> "
          f"1-sided {b['exact_1sided_95']*100:.2f}% | "
          f"CP-2s {b['cp_2sided_upper']*100:.2f}% | "
          f"obs {b['rate']*100:.2f}%")

with open("/home/hatch/workspace/SCBI/research/analysis_plans/s6_5_bounds_2026-09-28.json", "w") as f:
    json.dump({"pools": results,
               "exp095_flips": {f"{a}/{arm}": v for (a, arm), v in flips95.items()},
               "exp096_flips": flips96}, f, indent=2)
print("\nWrote research/analysis_plans/s6_5_bounds_2026-09-28.json")
