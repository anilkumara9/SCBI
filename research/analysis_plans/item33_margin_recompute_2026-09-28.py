"""ITEM-33 margin recomputation (LOG-4472 lane).
Recomputes the per-item 1-NN decode margin from EXP092 primaries
(embeddings npz) and documents why EXP093's per-item injection margin
shifts are unrecoverable. Deterministic (numpy only, no randomness).
"""
import json
import hashlib
import numpy as np

NPZ = "/home/hatch/workspace/SCBI/experiments/runs/EXP092_ibl/out/exp092_embeddings.npz"
L_STAR = 11  # EXP092 verdict_detail.l_star (out/exp092_report.json)

d = np.load(NPZ)
layers, ids, labels = d["layers"], d["ids"], d["labels"]
H = layers[L_STAR].astype(np.float64)
n = H.shape[0]
D2 = ((H[:, None, :] - H[None, :, :]) ** 2).sum(-1)
np.fill_diagonal(D2, np.inf)
D = np.sqrt(D2)

margins, same_min, diff_min = np.zeros(n), np.zeros(n), np.zeros(n)
for i in range(n):
    s = D[i][labels == labels[i]]
    f = D[i][labels != labels[i]]
    same_min[i], diff_min[i] = s.min(), f.min()
    margins[i] = f.min() - s.min()

order = np.argsort(margins)[::-1]
i33 = 33
res = {
    "item33_index": i33,
    "item33_id": str(ids[i33]),
    "layer": L_STAR,
    "item33_margin": float(margins[i33]),
    "item33_same_class_min_dist": float(same_min[i33]),
    "item33_diff_class_min_dist": float(diff_min[i33]),
    "item33_rank_of_60": int(np.where(order == i33)[0][0]) + 1,
    "top5": [(int(i), float(margins[i])) for i in order[:5]],
    "v82_L391_claim": "1.013; same-class 2.106 vs. different-class 3.119; 2nd of 60",
    "match": bool(
        abs(margins[i33] - 1.013) < 5e-4
        and abs(same_min[i33] - 2.106) < 5e-4
        and abs(diff_min[i33] - 3.119) < 5e-4
    ),
    "provenance": {
        "primaries": NPZ,
        "npz_sha256": hashlib.sha256(open(NPZ, "rb").read()).hexdigest(),
        "script": "research/analysis_plans/item33_margin_recompute_2026-09-28.py",
        "exp093_injection_shifts_recoverable": False,
        "exp093_reason": (
            "run_exp093.py computed per-item margin arrays mB/mP/mN in memory "
            "but persisted only aggregates (exp093_report.json secondaries: "
            "mean_margin_shift_P=0.005951849619547526, "
            "mean_margin_shift_N=-0.007636133829752604). No per-item margin "
            "CSV/NPZ/JSON exists anywhere in the EXP093 bundle or repo. "
            "Recovery requires a 180-pass model re-run (new experiment, GPU)."
        ),
    },
}
with open("/home/hatch/workspace/SCBI/research/analysis_plans/item33_margin_recompute_results_2026-09-28.json", "w") as f:
    json.dump(res, f, indent=2)
print(json.dumps({k: v for k, v in res.items() if k != "provenance"}, indent=2))
print("match:", res["match"])
