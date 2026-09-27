"""EXP094 verdict rescore: score the recorded per-item CSV with the frozen bundle.

Timeline (honest provenance, LOG-4375):
  1. The licensed real run completed all 244 passes, all guards, and wrote
     per_item_records.csv (180 rows) + constructor_manifest_run.json — then
     crashed AFTER the CSV write on a variable-name typo in the final
     score_experiment call (NameError: 'mean_abs_cosine', run_exp094.py:359;
     evidenced by exp094_stdout.log's internal sequence). The margins are
     genuine recorded data; the crash is genuine.
  2. The recovery script committed with the run had its OWN bug
     (int(item_id) on string IDs) and never successfully ran — Law #14
     review LOG-4374 OVERTURNED the claimed verdict: the reported numbers
     (dM_T=-0.0333, 8 flips, p=0.6250) had no auditable provenance.
  3. This repair (LOG-4375) fixes the item-ID handling (string keys; items
     are NOT renumbered) and executes the rescore: it reads the recorded
     margins, the recorded delivery_pass flag, and the recorded mean
     pairwise |cosine| from the committed CSV/manifest, and calls the
     frozen bundle's score_experiment on exactly those inputs. No pass is
     recomputed; no margin is regenerated — only the pre-registered
     decision-table scoring is applied to recorded data.

Exit 0 = report written; exit 1 = inputs inconsistent.
"""

import csv
import json
import os
import sys

BUNDLE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BUNDLE_DIR)
REPO_ROOT = os.path.abspath(os.path.join(BUNDLE_DIR, "..", "..", ".."))
EXP093_DIR = os.path.join(REPO_ROOT, "experiments", "runs", "EXP093_l11_causal")
sys.path.append(EXP093_DIR)

import numpy as np

from score_exp094 import score_experiment
from test_g7_audit import sha256_file
import importlib.util

OUT_DIR = os.path.join(BUNDLE_DIR, "out")


def main():
    csv_path = os.path.join(OUT_DIR, "per_item_records.csv")
    manifest_path = os.path.join(OUT_DIR, "constructor_manifest_run.json")
    frozen_path = os.path.join(BUNDLE_DIR, "constructor_manifest.json")

    # Consistency: the run manifest must reference the frozen constructor.
    frozen = json.load(open(frozen_path))
    run_m = json.load(open(manifest_path))
    fm = run_m["frozen_manifest"]
    assert fm["constructor_sha256"] == frozen["constructor_sha256"], \
        "constructor mismatch"
    assert fm["g7_verdict"] == "PASS", "G7 not PASS"

    margins = {"B": {}, "T": {}, "R": {}}
    strata = {}
    with open(csv_path) as f:
        for row in csv.DictReader(f):
            # LOG-4375 fix: item IDs are strings (e.g. 'exp092_planetary_2hop_0');
            # keep string keys — do NOT renumber items.
            i = row["item_id"]
            margins[row["arm"]][i] = float(row["margin"])
            strata[i] = row["stratum"]
    assert all(len(v) == 60 for v in margins.values()), \
        f"incomplete arms: {[len(v) for v in margins.values()]}"

    idx = sorted(strata)
    mB = np.array([margins["B"][i] for i in idx])
    mT = np.array([margins["T"][i] for i in idx])
    mR = np.array([margins["R"][i] for i in idx])
    phrasing = np.array([strata[i] for i in idx])

    report = score_experiment(
        mB, mT, mR, phrasing,
        delivery_pass=bool(run_m["delivery_pass"]),
        mean_abs_cosine=float(run_m["mean_pairwise_abs_cosine"]),
    )
    report["mode"] = "real"
    report["recovery"] = {
        "kind": "rescore-from-recorded-margins",
        "reason": "executor crashed on a variable-name typo AFTER all passes, "
                  "guards, and CSV write completed; no pass was recomputed",
        "repair_history": [
            "LOG-4373: recovery script committed but never ran (int() on "
            "string item IDs -> ValueError); claimed statistics had no "
            "auditable provenance.",
            "LOG-4374: Law #14 review OVERTURNED the verdict (false "
            "statistics, false recovery story, missing report artifact).",
            "LOG-4375: item-ID bug fixed (string keys, no renumbering); "
            "rescore executed against the committed CSV with the frozen "
            "scorer; exp094_report.json produced and committed.",
        ],
        "inputs": {
            "per_item_records.csv_sha256": sha256_file(csv_path),
            "constructor_manifest_run.json_sha256": sha256_file(
                manifest_path),
            "constructor_sha256": frozen["constructor_sha256"],
        },
        "guards_observed_in_run_log": [
            "G7.1 frozen constructor + audit PASS",
            "G0 bench pin pass",
            "G1' 240/240 real-tokenizer cover pass",
            "Δθ=0 pre-run hash == LOG-331 pin",
            "G5 per-item band 60/60 + execution probe PASS",
            "degeneracy gate 0.7923 < 0.95 bar",
            "Δθ=0 post-run hash OK",
        ],
    }
    report["run_meta"] = {
        "mode": "real",
        "layer": 11,
        "n_passes": 244,
        "constructor_sha256": frozen["constructor_sha256"],
        "P0_sha256": frozen["P0_sha256"],
        "R_SEED": 94094,
    }

    out_path = os.path.join(OUT_DIR, "exp094_report.json")
    with open(out_path, "w") as f:
        json.dump(report, f, indent=2)
    agg = report["stratum_table"]["agg__TB"]
    print(f"ΔM_T={agg['delta']:+.4f} "
          f"T-vs-R p={report['stratum_table']['agg__TR']['mcnemar_p']:.4g}")
    print(f"AUTHORITATIVE VERDICT: {report['verdict']} "
          f"(decision step {report['decision_step']})")
    print(f"report: {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
