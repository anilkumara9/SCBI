#!/usr/bin/env python3
"""S5-3 paired decode probes — the eight killed EXP077 variants (Gap 4 family).

Question (S5-3, licensed LOG-4391): for the eight killed EXP077 variants, were
their coordinates decodable-but-causally-inert, or did the variants never encode
the target information?

Licensed procedure — EXP092's signed decode protocol, applied per variant with
NO improvisation (functions imported verbatim from score_exp092.py):
  * representation: 1-D coordinates z_i = d_v . h_i, where h_i are the
    EXP092-B layer-20 final-token embeddings (layer index 20 = EXP077's
    target_layer=20; same frozen Pythia-410m backbone, same layer, same dim).
    The 1-D projection is the direction's "coordinate" of each item.
  * statistic: leave-one-out 1-NN accuracy from the squared 1-D distance matrix.
  * null: B=1,000 stratified (domain x phrasing) label permutations,
    random.Random(9207+b) — the registered RNG scheme.
  * tie guard (§3): any exact float nearest-neighbor tie -> RUN-INVALID.
  * G4 instrument gate (§6): zero null spread -> RUN-INVALID (withheld, never a verdict).
  * bar: Bonferroni p < 0.05/8 (8 variants) AND (accuracy - null q95) >= 0.10.

Decision table (S5-3):
  clears bar -> "decodable-yet-inert" / CONTINUE (wall is causal, not informational)
  fails bar  -> "never-decodable"     / PIVOT   (the tested geometric room was empty)

Variant -> direction map (from archived exp077_vectors.pt):
  V1 radial a=0.25            : v_hat
  V2 radial a=0.5             : v_hat
  V3 radial a=1.0             : v_hat
  V4 radial a=2.0             : v_hat
  V5 angular  (cone C9)       : v_hat  (cone center; cone = {u : angle(u,v_hat) <= 30 deg})
  V6 control  (C10)           : r_vec  (control-cone center; pinned random ~ orth to v_hat)
  V7 offset   (C6)            : v_hat_c (offset-removed direction, exactly as archived)
  V8 replication (C3 vs C1)   : v_hat
Scale-invariance lemma (used, not tuned): 1-NN neighbor ordering on 1-D
projections is invariant to positive rescaling, so alpha is decode-irrelevant;
V1-V4 and V8 share one probe direction. The cone arm's per-item best-of-8
selection has no single archived vector; its center v_hat is the principled
arm-level direction (it is also the "line" in the cone-vs-line endpoint).

Diagnostics (non-licensed, non-decision-driving, labeled as such):
  D1 instrument positive control: a label-built synthetic direction that spreads
     the 20 classes along the line by construction; the 1-D 1-NN machinery MUST
     clear the bar on it, else the instrument is deaf and verdicts are withheld.
  D2 negative control is V6 itself (r_vec ~ random direction; expect ~chance).

Reproducibility: pure numpy + stdlib random; all RNG seeds fixed; every input
artifact sha256-hashed and recorded in the results JSON. $0 GPU. CPU only.

Usage: ~/workspace/.venv-exp077/bin/python s5_3_decode_probes_2026-09-28.py
Outputs (same directory):
  s5_3_coordinates_2026-09-28.json  (per-variant full 1-D coordinates, 60 floats each)
  s5_3_results_2026-09-28.json      (hashes, per-variant stats, verdicts)
"""

import hashlib
import json
import os
import sys

import numpy as np

# Licensed functions, imported verbatim — not reimplemented.
sys.path.insert(0, os.path.expanduser("~/workspace/SCBI/experiments/runs/EXP092_ibl"))
from score_exp092 import (  # noqa: E402
    loo_1nn_accuracy,
    permutation_null,
    strata_indices,
    RunInvalid,
)

SCBI = os.path.expanduser("~/workspace/SCBI")
VEC_PATH = os.path.join(SCBI, "experiments/runs/EXP077_cone_vs_line/exp077_vectors.pt")
EMB_PATH = os.path.join(SCBI, "experiments/runs/EXP092_ibl/out/exp092_embeddings.npz")
SCORER_PATH = os.path.join(SCBI, "experiments/runs/EXP092_ibl/score_exp092.py")
OUT_DIR = os.path.join(SCBI, "research/analysis_plans")

N_ITEMS = 60
N_CLASSES = 20
LAYER = 20            # EXP077 target_layer=20; EXP092 index-20 = "layer 20"
PERM_B = 1000
PERM_SEED = 9207
ALPHA_B = 0.05 / 8    # Bonferroni over the 8 S5-3 variants (licensed: 0.05/m)
EFFECT_BAR = 0.10     # 10pp (licensed)

VARIANTS = [
    ("V1_radial_a0.25",  "v_hat",   "radial arm a=0.25 (C2); direction v_hat"),
    ("V2_radial_a0.5",   "v_hat",   "radial arm a=0.5  (C3); direction v_hat"),
    ("V3_radial_a1.0",   "v_hat",   "radial arm a=1.0  (C4); direction v_hat"),
    ("V4_radial_a2.0",   "v_hat",   "radial arm a=2.0  (C5); direction v_hat"),
    ("V5_angular_cone",   "v_hat",   "angular arm (C9); cone center v_hat"),
    ("V6_control",        "r_vec",   "control arm (C10); control-cone center r"),
    ("V7_offset",         "v_hat_c", "offset arm (C6); offset-removed v_hat^c"),
    ("V8_replication",    "v_hat",   "replication (C3 vs C1, a=0.5); direction v_hat"),
]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    hashes = {
        "exp077_vectors.pt": sha256(VEC_PATH),
        "exp092_embeddings.npz": sha256(EMB_PATH),
        "score_exp092.py": sha256(SCORER_PATH),
        "this_script": sha256(os.path.abspath(__file__)),
    }

    # ---- load EXP077 directions (torch needed only for the .pt container) ----
    import torch  # local import: only used as an archive reader, no model, no GPU

    vecs = torch.load(VEC_PATH, map_location="cpu", weights_only=False)

    def arr(k):
        return np.asarray(vecs[k], dtype=np.float64)

    dirs = {"v_hat": arr("v_hat"), "v_hat_c": arr("v_hat_c"), "r_vec": arr("r_vec")}
    for k, d in dirs.items():
        assert d.shape == (1024,), (k, d.shape)
        assert abs(np.linalg.norm(d) - 1.0) < 1e-6, (k, np.linalg.norm(d))

    # mapping sanity checks (assertions, not tuned thresholds)
    v_hat, v_hat_c, r_vec = dirs["v_hat"], dirs["v_hat_c"], dirs["r_vec"]
    u = np.asarray(vecs["u_list"], dtype=np.float64)
    assert u.shape == (8, 1024)
    cone_cos = (u @ v_hat)  # unit norms
    assert np.all(cone_cos >= np.cos(np.deg2rad(30)) - 1e-6), cone_cos.min()
    assert abs(v_hat @ r_vec) < 0.10, v_hat @ r_vec  # control ~ random vs v_hat
    assert abs(v_hat @ v_hat_c) < 1.0 - 1e-9  # distinct directions

    # ---- load EXP092-B bench (layer 20, labels, strata) ----
    z = np.load(EMB_PATH, allow_pickle=True)
    X = np.asarray(z["layers"][LAYER], dtype=np.float64)
    assert X.shape == (N_ITEMS, 1024), X.shape
    labels_raw = [str(x) for x in z["labels"]]
    uniq = sorted(set(labels_raw))
    assert len(uniq) == N_CLASSES, len(uniq)
    lid = {u_: i for i, u_ in enumerate(uniq)}
    label_ids = np.array([lid[u_] for u_ in labels_raw], dtype=int)
    strata = strata_indices([str(x) for x in z["domain"]],
                            [str(x) for x in z["phrasing"]])
    assert sum(len(s) for s in strata) == N_ITEMS and len(strata) == 4

    # ---- D1: instrument positive control (diagnostic, non-licensed) ----
    grand = X.mean(axis=0)
    synth = np.zeros(1024)
    for c in range(N_CLASSES):
        mu_c = X[label_ids == c].mean(axis=0)
        synth += (c - (N_CLASSES - 1) / 2.0) * (mu_c - grand)
    synth /= np.linalg.norm(synth)
    zc = X @ synth
    d2c = (zc[:, None] - zc[None, :]) ** 2
    acc_c, p_c, q95_c, null_c = permutation_null(
        d2c, label_ids, strata, B=PERM_B, seed=PERM_SEED)
    spread_c = float(null_c.max() - null_c.min())
    d1_pass = (p_c < ALPHA_B) and (acc_c - q95_c >= EFFECT_BAR) and spread_c > 0
    print(f"D1 positive control: acc={acc_c:.4f} p={p_c:.6f} q95={q95_c:.4f} "
          f"effect={acc_c - q95_c:+.4f} spread={spread_c:.4f} -> "
          f"{'LIVE' if d1_pass else 'DEAF'}")
    if not d1_pass:
        print("INSTRUMENT DEAF — verdicts withheld (RUN-INVALID).")
        sys.exit(2)

    # ---- licensed per-variant probes ----
    coordinates = {}
    results = []
    for name, dkey, note in VARIANTS:
        d = dirs[dkey]
        zi = X @ d                      # full 1-D coordinates (preserved)
        coordinates[name] = [float(v) for v in zi]
        d2 = (zi[:, None] - zi[None, :]) ** 2
        acc, p, q95, null_dist = permutation_null(
            d2, label_ids, strata, B=PERM_B, seed=PERM_SEED)
        spread = float(null_dist.max() - null_dist.min())
        if spread == 0.0:               # G4 gate (licensed §6)
            raise RunInvalid(f"G4 FAIL: {name} null spread is zero — RUN-INVALID.")
        effect = acc - q95
        clears = (p < ALPHA_B) and (effect >= EFFECT_BAR)
        verdict = ("decodable-yet-inert / CONTINUE" if clears
                   else "never-decodable / PIVOT")
        results.append({
            "variant": name, "direction": dkey, "note": note,
            "n_items": N_ITEMS, "n_classes": N_CLASSES,
            "accuracy": acc, "p_value": p, "null_q95": q95,
            "effect_acc_minus_q95": effect, "null_spread": spread,
            "alpha_bonferroni": ALPHA_B, "effect_bar": EFFECT_BAR,
            "clears_bar": bool(clears), "verdict": verdict,
        })
        print(f"{name:16s} [{dkey:7s}] acc={acc:.4f} p={p:.6f} q95={q95:.4f} "
              f"effect={effect:+.4f} -> {verdict}")

    out = {
        "lane": "S5-3",
        "date": "2026-09-28",
        "question": "decodable-yet-inert vs never-decodable for the eight killed EXP077 variants",
        "procedure": "EXP092 licensed: LOO 1-NN on 1-D variant-direction coordinates "
                     "of EXP092-B layer-20 embeddings; B=1000 stratified "
                     "(domain x phrasing) permutations, seed 9207; tie guard; G4 gate; "
                     "Bonferroni 0.05/8; 10pp effect bar",
        "input_hashes_sha256": hashes,
        "direction_cosine_checks": {
            "cos(v_hat, r_vec)": float(v_hat @ r_vec),
            "cos(v_hat, v_hat_c)": float(v_hat @ v_hat_c),
            "min_cos(u_j, v_hat)": float(cone_cos.min()),
        },
        "instrument_positive_control_D1": {
            "accuracy": acc_c, "p_value": p_c, "null_q95": q95_c,
            "effect": acc_c - q95_c, "live": True,
            "note": "diagnostic only; label-built direction, not decision-driving",
        },
        "variants": results,
    }
    with open(os.path.join(OUT_DIR, "s5_3_results_2026-09-28.json"), "w") as f:
        json.dump(out, f, indent=2)
    with open(os.path.join(OUT_DIR, "s5_3_coordinates_2026-09-28.json"), "w") as f:
        json.dump({"coordinates_z_per_variant": coordinates,
                   "layer": LAYER, "n_items": N_ITEMS}, f)

    n_cont = sum(r["clears_bar"] for r in results)
    print(f"\nS5-3: {n_cont}/8 variants clear the bar. "
          f"{'CONTINUE' if n_cont else 'PIVOT'} reading for the Gap-4 family.")


if __name__ == "__main__":
    main()
