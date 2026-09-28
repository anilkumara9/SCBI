"""EXP103 mechanical scorer (uninterpreted).

Reads the experiment's per-item CSVs and emits machine-computed counts:
per-cell accuracies, deltas, exact two-sided McNemar p-values, Tango CIs,
coverage, flips, and the mechanical readout fields. No scientific verdict.

Statistical arithmetic is imported VERBATIM from EXP094's frozen scorer
(score_exp094.py) — the same functions, unchanged.
"""


import csv
import json
import os
import sys

BUNDLE_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(BUNDLE_DIR, "..", "..", ".."))
EXP094_DIR = os.path.join(REPO_ROOT, "experiments", "runs", "EXP094_peritem_l11")


def _load_module(name, path):
    import importlib.util
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


_score094 = _load_module("exp103_score094",
                         os.path.join(EXP094_DIR, "score_exp094.py"))

# Verbatim licensed machinery (EXP094 scorer — frozen).
mcnemar_exact_p = _score094.mcnemar_exact_p
tango_ci_paired = _score094.tango_ci_paired
contrast_stats = _score094.contrast_stats

import numpy as np  # noqa: E402


class RunInvalid(Exception):
    """Guard failure -> RUN-INVALID (withheld, never a verdict)."""


def load_csv(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def compute(records, delivery, gate):
    """Mechanical computation over the full 60-item paired set.

    records: rows of per_item_records.csv (item_id, stratum, arm, margin, ...)
    delivery: rows of per_item_delivery.csv (item_id, arm, fired,
              excluded_from_contrasts, ...)
    gate: rows of per_item_gate.csv (item_id, fired, ...)
    Returns (cells, readout) with 9 cells = 3 strata x 3 contrasts.
    """
    # bench order (first-seen in the records file); item_ids are strings
    # like 'exp092_planetary_2hop_7', never cast to int.
    items = list(dict.fromkeys(r["item_id"] for r in records))
    n = len(items)
    assert n == 60, f"expected 60 items, got {n}"

    by_arm = {}
    for arm in ("B", "gated-T", "gated-R"):
        rows = {r["item_id"]: r for r in records if r["arm"] == arm}
        assert len(rows) == 60, f"arm {arm} has {len(rows)} rows"
        by_arm[arm] = rows

    deliv = {(r["item_id"], r["arm"]): r for r in delivery}
    gate_r = {r["item_id"]: r for r in gate}
    assert len(gate_r) == 60

    def fvec(arm, key):
        return np.array([float(by_arm[arm][i][key]) for i in items])

    mB = fvec("B", "margin")
    cB = (mB > 0)
    mT = fvec("gated-T", "margin")
    mR = fvec("gated-R", "margin")
    cT = (mT > 0)
    cR = (mR > 0)

    # delivery exclusions (fired rows only; <=2 per arm enforced by runner)
    excl_T = np.array([deliv[(i, "gated-T")]["excluded_from_contrasts"] == "y"
                      for i in items])
    excl_R = np.array([deliv[(i, "gated-R")]["excluded_from_contrasts"] == "y"
                      for i in items])

    # strata
    stratum = {r["item_id"]: r["stratum"] for r in records if r["arm"] == "B"}
    strata = {
        "agg": np.ones(60, dtype=bool),
        "a_first": np.array([stratum[i] == "A-first" for i in items]),
        "c_first": np.array([stratum[i] == "C-first" for i in items]),
    }

    contrasts = [
        ("gated-T_vs_B", cT, cB, ~excl_T, "discovery"),
        ("gated-R_vs_B", cR, cB, ~excl_R, "discovery"),
        ("gated-T_vs_gated-R", cT, cR, ~(excl_T | excl_R), "diagnostic"),
    ]

    cells = []
    for cname, cX, cY, base_mask, kind in contrasts:
        for sname, smask in strata.items():
            mask = base_mask & smask
            idx = np.where(mask)[0]
            if len(idx) == 0:
                raise RunInvalid(
                    f"delivery exclusion emptied contrast {cname} "
                    f"({sname}) — RUN-INVALID.")
            st = contrast_stats(cX[mask], cY[mask])
            st["contrast"] = cname
            st["kind"] = kind
            st["stratum"] = sname
            st["tango_ci"] = list(st["tango_ci"])
            cells.append(st)

    # flips vs B mapped to original item indices (on post-exclusion sets)
    def flip_ids(cX, cY, mask):
        return [items[i] for i in np.where(mask)[0]
                if bool(cX[i]) != bool(cY[i])]

    t_ids = flip_ids(cT, cB, ~excl_T)
    r_ids = flip_ids(cR, cB, ~excl_R)

    # coverage from the gate file
    fired = np.array([gate_r[i]["fired"] == "1" for i in items])
    coverage = float(fired.mean())

    # gate-integrity audit (independent of the runner): re-derive
    # fired ⟺ mass_L20_max >= tau from the persisted CSV on all 60 rows.
    # F2-class fence: the gate's own mass is the ONLY attention column;
    # no other attention quantity is derived or cited (§4.3).
    audit_consistent = all(
        (gate_r[i]["fired"] == "1") ==
        (float(gate_r[i]["mass_L20_max"]) >= float(gate_r[i]["tau"]))
        for i in items)

    # sanity gates (protocol literal: ties/60 > 5% per arm)
    sanity = {}
    for arm in ("gated-T", "gated-R"):
        m = fvec(arm, "margin")
        t = int((m == 0.0).sum())
        sanity[arm] = {
            "ties": t,
            "ties_over_60": t / 60.0,
            "run_invalid_ties": (t / 60.0) > 0.05,
            "zero_variance": bool(np.all(m == m[0])),
        }

    readout = {
        "n_items": n,
        "coverage": coverage,
        "n_fired": int(fired.sum()),
        "gate_integrity_audit": {
            "fired_iff_L20max_ge_tau_60_of_60": bool(audit_consistent),
        },
        "gated_T_flips_vs_B": len(t_ids),
        "gated_T_flip_ids": t_ids,
        "gated_R_flips_vs_B": len(r_ids),
        "gated_R_flip_ids": r_ids,
        "sanity": sanity,
    }
    return cells, readout


def main():
    outdir = os.path.join(BUNDLE_DIR, "out")
    records = load_csv(os.path.join(outdir, "per_item_records.csv"))
    delivery = load_csv(os.path.join(outdir, "per_item_delivery.csv"))
    gate = load_csv(os.path.join(outdir, "per_item_gate.csv"))
    cells, readout = compute(records, delivery, gate)
    json.dump(cells, open(os.path.join(outdir, "stratum_table.json"), "w"),
              indent=2)
    json.dump(readout, open(os.path.join(outdir, "mechanical_readout.json"),
                            "w"), indent=2)
    print(json.dumps(readout, indent=2))


if __name__ == "__main__":
    main()
