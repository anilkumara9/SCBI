"""EXP145 direction build — LOO maximum-average-cosine shared correction.

Verbatim port of the committed EXP093 `direction_builder.py` v0.2
construction, parameterized: (60, 768) at l* (not (60,1024) at layer 11).
numpy-only, read-only on the EXP145 embeddings .npz. No torch, no weights.

Construction (registered v0.2; per-item normalization breaks the v0.1
zero-sum — non-degenerate [FACT]):
    h(i)      = l* final-token embedding of item i            (60, 768)
    c^(-i)(i) = mean{ h(k) : k != i, target(k) = target(i) }  (mean of 2)
    r_i       = c^(-i)(i) - h(i);  assert ||r_i|| > 1e-9  (S0.4)
    u_i       = r_i / ||r_i||                            (unit LOO correction)
    v^(-i)    = normalize( (1/59) * sum_{j != i} u_j )    (no item-i leakage)

D2 gate: mean_i cos(v^(-i), u_i) >= 0.70 (the paper's C2 bar).
"""

import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import exp145_common as C  # noqa: E402

EMB = os.path.join(C.RUN_DIR, "exp145_embeddings.npz")
DECODE = os.path.join(C.RUN_DIR, "exp145_decode_report.json")
OUT = os.path.join(C.RUN_DIR, "exp145_directions.npz")
OUT_JSON = os.path.join(C.RUN_DIR, "exp145_direction_verification.json")
COS_BAR = 0.70  # D2 (S7-2 §3.3: the paper's C2 bar)


def build_directions(X, labels):
    """Compute {r_i}, {u_i}, {v^(-i)} + coherence diagnostics.
    X: (60, 768) float64 array (l* final-token states). Raises RunInvalid."""
    X = np.asarray(X, dtype=np.float64)
    if X.shape != (C.N_ITEMS, 768):
        raise C.RunInvalid(f"G2 FAIL: l* array shape {X.shape} != (60, 768).")
    lab = np.array([str(x) for x in labels])
    if len(lab) != C.N_ITEMS:
        raise C.RunInvalid(f"G2 FAIL: {len(lab)} labels != 60.")

    r = np.zeros_like(X)
    for i in range(C.N_ITEMS):
        mask = (lab == lab[i])
        mask[i] = False
        proto = X[mask].mean(axis=0)   # mean of 2 (3 items per target, minus i)
        r[i] = proto - X[i]
    r_norms = np.linalg.norm(r, axis=1)
    if not np.all(r_norms > C.R_MIN_ASSERT):  # S0.4
        bad = np.nonzero(r_norms <= C.R_MIN_ASSERT)[0].tolist()
        raise C.RunInvalid(
            f"S0.4 FAIL: ||r_i|| <= 1e-9 for items {bad} — RUN-INVALID.")
    u = r / r_norms[:, None]

    v = np.zeros_like(u)
    prenorm_norms = np.zeros(C.N_ITEMS)
    for i in range(C.N_ITEMS):
        keep = np.ones(C.N_ITEMS, dtype=bool)
        keep[i] = False
        m = u[keep].mean(axis=0)
        n = float(np.linalg.norm(m))
        prenorm_norms[i] = n
        if n == 0.0:
            raise C.RunInvalid(
                f"G2 FAIL: pre-normalization shared-direction norm is 0 for "
                f"item {i} — RUN-INVALID.")
        v[i] = m / n
    v_norms = np.linalg.norm(v, axis=1)
    if not np.allclose(v_norms, 1.0, rtol=0, atol=1e-9):
        raise C.RunInvalid(
            f"G2 FAIL: v^(-i) not unit-norm (min={v_norms.min()}, "
            f"max={v_norms.max()}) — RUN-INVALID.")

    if np.all(v == v[0]):  # R4: LOO must actually vary the 60 directions
        raise C.RunInvalid(
            "G2/R4 FAIL: all 60 v^(-i) bit-identical — LOO degenerate.")

    # D2: achieved average cosine (THE 0.7 bar input).
    mean_cos = float(np.einsum("ij,ij->i", v, u).mean())

    # Coherence diagnostics (registered, reported, non-binding).
    iu = np.triu_indices(C.N_ITEMS, k=1)
    mean_cos_u = float((u[iu[0]] * u[iu[1]]).sum(axis=1).mean())
    max_cos_v = float((v[iu[0]] * v[iu[1]]).sum(axis=1).max())

    return {
        "r_norms": r_norms, "u": u, "v": v,
        "min_r_norm": float(r_norms.min()),
        "mean_pairwise_cosine_u": mean_cos_u,
        "prenorm_min": float(prenorm_norms.min()),
        "prenorm_max": float(prenorm_norms.max()),
        "max_pairwise_cosine_v": max_cos_v,
        "mean_cosine": mean_cos,
    }


def main():
    with open(DECODE) as f:
        dec = json.load(f)
    if not dec["D1"] or dec["l_star"] is None:
        raise C.Inconclusive(
            "D1 FAIL: no layer passed both decode bars — the intervention "
            "arm is not licensed (S7-2 §3.4).")
    l_star = int(dec["l_star"])

    z = np.load(EMB, allow_pickle=True)
    d = build_directions(z["layers"][l_star], z["labels"])
    d2_pass = d["mean_cosine"] >= COS_BAR
    print(f"[directions] l*={l_star}: min||r_i||={d['min_r_norm']:.4f}, "
          f"mean_cos_u={d['mean_pairwise_cosine_u']:+.4f}, "
          f"prenorm=[{d['prenorm_min']:.4f},{d['prenorm_max']:.4f}], "
          f"max_cos_v={d['max_pairwise_cosine_v']:.4f}", flush=True)
    print(f"[directions] D2 mean_i cos(v^(-i),u_i) = {d['mean_cosine']:.4f} "
          f"(bar {COS_BAR}) → {'PASS' if d2_pass else 'FAIL'}", flush=True)

    np.savez(OUT, v=d["v"], u=d["u"], r_norms=d["r_norms"])
    artifact = {
        "experiment": "EXP145",
        "guard": "G2/S0.4/D2",
        "l_star": l_star,
        "construction": "LOO maximum-average-cosine shared correction (v0.2, "
                        "verbatim port)",
        "min_r_norm": d["min_r_norm"],
        "r_assert": f"60/60 ||r_i|| > {C.R_MIN_ASSERT}",
        "mean_pairwise_cosine_u": d["mean_pairwise_cosine_u"],
        "prenorm_norm_range": [d["prenorm_min"], d["prenorm_max"]],
        "max_pairwise_cosine_v": d["max_pairwise_cosine_v"],
        "all_v_unit_norm": True,
        "r4_not_bit_identical": True,
        "D2_mean_cosine": d["mean_cosine"],
        "D2_bar": COS_BAR,
        "D2": "PASS" if d2_pass else "FAIL",
    }
    with open(OUT_JSON, "w") as f:
        json.dump(artifact, f, indent=1)
    print(f"[directions] wrote {OUT} + {OUT_JSON}", flush=True)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except C.RunInvalid as e:
        print(f"RUN-INVALID: {e}", flush=True)
        sys.exit(3)
    except C.Inconclusive as e:
        print(f"INCONCLUSIVE: {e}", flush=True)
        sys.exit(4)
