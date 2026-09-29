"""EXP095 stratum sideband — mean-margin-shift + flip ledgers per (a,stratum,contrast).

Mechanical companion to stratum_table_135.json (pre-reg §5 item 5 sideband).
Recomputed from out/per_item_records.csv (frozen records); numpy-only.
"""

import csv
import json
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
ALPHAS = (0.25, 0.5, 1.0, 2.0, 4.0)

rows = {}
with open(os.path.join(OUT, "per_item_records.csv"), newline="") as f:
    for r in csv.DictReader(f):
        rows.setdefault(r["item_id"], {})[(r["alpha"], r["arm"])] = r

item_ids = sorted(rows)
assert len(item_ids) == 60
assert all(set(rows[i]) >= {("n/a", "B")} for i in item_ids)

mB, ph = {}, {}
for i in item_ids:
    rb = rows[i][("n/a", "B")]
    mB[i] = float(rb["margin"])
    ph[i] = rb["stratum"]

sideband = {}
for a in ALPHAS:
    for sname, sel in (("agg", item_ids),
                       ("A", [i for i in item_ids if ph[i] == "A-first"]),
                       ("C", [i for i in item_ids if ph[i] == "C-first"])):
        for cname, arm in (("TB", "T"), ("WB", "B_wrong"), ("TW", None)):
            if arm is not None:
                mX = [float(rows[i][(str(a), arm)]["margin"]) for i in sel]
                mY = [mB[i] for i in sel]
                shift = [x - y for x, y in zip(mX, mY)]
                cx = [x > 0.0 for x in mX]
                cy = [y > 0.0 for y in mY]
            else:
                mT = [float(rows[i][(str(a), "T")]["margin"]) for i in sel]
                mW = [float(rows[i][(str(a), "B_wrong")]["margin"]) for i in sel]
                shift = [t - w for t, w in zip(mT, mW)]
                cx = [t > 0.0 for t in mT]
                cy = [w > 0.0 for w in mW]
            import numpy as np
            flips_to_right = [i for i, (x, y) in zip(sel, zip(cx, cy))
                              if x and not y]
            flips_to_wrong = [i for i, (x, y) in zip(sel, zip(cx, cy))
                              if (not x) and y]
            sideband[f"a{a}__{sname}__{cname}"] = {
                "n": len(sel),
                "mean_margin_shift": float(np.mean(shift)),
                "flip_to_right_idx": flips_to_right,
                "flip_to_wrong_idx": flips_to_wrong,
            }

with open(os.path.join(OUT, "stratum_sideband.json"), "w") as f:
    json.dump(sideband, f, indent=2)
print(f"sideband cells: {len(sideband)} (expected 45)")
