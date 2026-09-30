#!/usr/bin/env python3
"""EXP137 (B3/TGA-DECODE) executor.

Executes EXACTLY per research/prereg/EXP137_PREREG_TGADECODE_2026-09-30.md.
$0 CPU, zero new forwards, two npz loads.
Any §3.5 breaking-point trip -> RUN-INVALID, exit 44. Never a verdict.
"""
import hashlib
import json
import random
import sys
import time

import numpy as np

RUN_DIR = "/home/hatch/workspace/SCBI/experiments/runs/EXP137_tgadecode"
OUT_DIR = RUN_DIR + "/out"
A1_PATH = "/home/hatch/workspace/SCBI/experiments/runs/EXP127_tga/out/exp127_vectors.npz"
A2_PATH = "/home/hatch/workspace/SCBI/experiments/runs/EXP092_ibl/out/exp092_embeddings.npz"
A1_PIN = "9b527c026d0ee307192725429f655e628f403505343dc018de3cfe15db6113dc"
A2_PIN = "9219bd0dd961524e26a7bb570cbc1e67e7fb245f58271415c5cf174dceb95fae"
BENCH_PIN = "9be8162633fe19aa2a924440d8ba158c1cc4e734c1f2a554a01a27e459f47fc4"
EXIT_RUN_INVALID = 44

results = {"breaking_points": {}, "checks": {}}


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def bp_trip(bp_id, reason):
    """Record a breaking-point trip and exit RUN-INVALID."""
    results["breaking_points"][bp_id] = {"tripped": True, "reason": reason}
    results["status"] = "RUN-INVALID"
    write_report()
    print(f"BREAKING POINT ({bp_id}) TRIPPED: {reason}", file=sys.stderr)
    sys.exit(EXIT_RUN_INVALID)


def bp_pass(bp_id, detail=""):
    results["breaking_points"][bp_id] = {"tripped": False, "detail": detail}


def knn_loo_accuracy(scalars, labels):
    """1-NN leave-one-out accuracy on 1-D scalars. Asserts zero exact ties."""
    n = len(scalars)
    D = np.abs(scalars[:, None] - scalars[None, :])
    np.fill_diagonal(D, np.inf)
    dmin = D.min(axis=1)
    # exact-tie assert: the row minimum must be unique per row
    tie_rows = [i for i in range(n) if np.sum(D[i] == dmin[i]) != 1]
    if tie_rows:
        bp_trip("f", f"exact 1-NN distance ties on rows {tie_rows}")
    nn = D.argmin(axis=1)
    correct = int(np.sum(labels[nn] == labels))
    return correct / n, nn


def main():
    t0 = time.time()

    # ---- (a) direction-archive integrity ----
    if sha256_file(A1_PATH) != A1_PIN:
        bp_trip("a", "A1 SHA-256 mismatch")
    a1 = np.load(A1_PATH)
    v1_keys = sorted(k for k in a1.files if k.startswith("v1__"))
    if len(v1_keys) != 10:
        bp_trip("a", f"expected 10 v1__ keys, found {len(v1_keys)}")
    bp_pass("a", f"SHA ok, {len(v1_keys)} v1__ keys")

    V = np.stack([a1[k].astype(np.float64) for k in v1_keys])  # (10, 1024)
    if np.any(~np.isfinite(V)):
        bp_trip("a", "non-finite values in A1 vectors")
    norms = np.linalg.norm(V, axis=1)
    if np.any(norms == 0):
        bp_trip("a", "zero-norm v1 vector")

    # ---- canonical direction (sign-aligned mean) ----
    dots = V @ V[0]
    signs = np.where(dots == 0.0, 1.0, np.sign(dots))
    mean_vec = (signs[:, None] * V).mean(axis=0)
    v1hat = mean_vec / np.linalg.norm(mean_vec)

    # ---- (b) coherence gate ----
    Vn = V / norms[:, None]
    cosmat = np.abs(Vn @ Vn.T)
    iu = np.triu_indices(10, 1)
    coherence = float(cosmat[iu].mean())
    results["checks"]["coherence_mean_abs_cosine"] = coherence
    results["checks"]["coherence_min_abs_cosine"] = float(cosmat[iu].min())
    results["checks"]["canonical_norm"] = float(np.linalg.norm(mean_vec))
    if coherence < 0.99:
        bp_trip("b", f"coherence {coherence:.6f} < 0.99")
    bp_pass("b", f"coherence {coherence:.6f} >= 0.99")

    # ---- (c) embedding-archive integrity ----
    if sha256_file(A2_PATH) != A2_PIN:
        bp_trip("c", "A2 SHA-256 mismatch")
    a2 = np.load(A2_PATH, allow_pickle=True)
    layers = a2["layers"]
    if layers.shape != (24, 60, 1024):
        bp_trip("c", f"layers shape {layers.shape} != (24, 60, 1024)")
    bp_pass("c", "SHA ok, layers shape (24, 60, 1024)")

    ids = np.array([str(x) for x in a2["ids"]])
    labels = np.array([str(x) for x in a2["labels"]])
    domain = np.array([str(x) for x in a2["domain"]])
    phrasing = np.array([str(x) for x in a2["phrasing"]])

    # ---- (d) bench alignment ----
    strata_order = [("Planetary", "A-first"), ("Planetary", "C-first"),
                    ("Elemental", "A-first"), ("Elemental", "C-first")]
    stratum_idx = []
    counts = []
    for d, p in strata_order:
        idx = [i for i in range(60) if domain[i] == d and phrasing[i] == p]
        stratum_idx.append(idx)
        counts.append(len(idx))
    if counts != [16, 14, 14, 16]:
        bp_trip("d", f"stratum counts {counts} != [16, 14, 14, 16]")
    if len(set(ids)) != 60:
        bp_trip("d", f"{len(set(ids))} unique ids != 60")
    if len(set(labels)) != 20:
        bp_trip("d", f"{len(set(labels))} unique labels != 20  -> see (g)")
    # bench-pin spot check: rebuild canonical bench, verify pin, check spot ids
    sys.path.insert(0, "/home/hatch/workspace/SCBI/experiments/runs/EXP092_ibl")
    import reference_implementation as ri
    bench = ri.build_bench()
    if ri.bench_sha256() != BENCH_PIN:
        bp_trip("d", "rebuilt EXP092-B bench pin mismatch")
    bench_ids = {it["id"] for it in bench}
    if set(ids) != bench_ids:
        bp_trip("d", "A2 ids != EXP092-B bench id set")
    spot = [0, 15, 30, 45, 59]  # deterministic spot selection (A2 advisory)
    spot_ids = [ids[i] for i in spot]
    if not all(s in bench_ids for s in spot_ids):
        bp_trip("d", f"spot ids {spot_ids} not all in bench")
    bp_pass("d", f"strata {counts}, 60 ids == bench ids, spot {spot} ok")
    results["checks"]["spot_ids"] = spot_ids

    # ---- (g) label count ----
    if len(set(labels)) != 20:
        bp_trip("g", "label count != 20")
    bp_pass("g", "20 unique labels")

    # ---- projection: layers[19] = input of block 20 = v1hat native space ----
    # EXP127: v1hat lives in hs[20] = input of transformer block 20.
    # EXP092 archive: layers[l] = hidden_states[l+1] = output of 0-indexed block l.
    # Input of block 20 = output of block 19 = archived layers[19]. (pre-reg §0, draft corr. 1)
    H = layers[19].astype(np.float64)  # (60, 1024)
    scalars = H @ v1hat  # (60,)
    # A1 advisory (NaN/Inf guard): apparatus-integrity assert; trip -> RUN-INVALID
    if not np.all(np.isfinite(scalars)):
        bp_trip("a", "non-finite values in v1hat-projected scalars")
    results["checks"]["scalars_finite"] = True

    # ---- (e) degeneracy ----
    if float(np.var(scalars)) == 0.0:
        bp_trip("e", "zero variance in projected scalars")
    bp_pass("e", f"variance {float(np.var(scalars)):.3e} > 0")

    # ---- primary: 1-NN LOO (ties assert inside) ----
    acc, nn = knn_loo_accuracy(scalars, labels)
    bp_pass("f", "zero exact distance ties across 60 queries")
    results["primary"] = {"accuracy": acc, "correct": int(round(acc * 60)), "n": 60}
    results["per_item"] = {
        "nn_index": nn.tolist(),
        "predicted_label": labels[nn].tolist(),
        "true_label": labels.tolist(),
        "correct": (labels[nn] == labels).tolist(),
    }

    # ---- stratified permutation null, B=10,000 ----
    B = 10000
    ge = 0
    perm_accs = np.empty(B)
    lab = labels  # permuted within strata
    for b in range(B):
        rng = random.Random(137001 + b)
        perm = np.empty(60, dtype=object)
        for idx in stratum_idx:
            pool = [lab[i] for i in idx]
            rng.shuffle(pool)
            for i, v in zip(idx, pool):
                perm[i] = v
        Dp = np.abs(scalars[:, None] - scalars[None, :])
        np.fill_diagonal(Dp, np.inf)
        nnp = Dp.argmin(axis=1)
        ab = float(np.mean(perm[nnp] == perm))
        perm_accs[b] = ab
        if ab >= acc:
            ge += 1
    p = (1 + ge) / (1 + B)
    results["null"] = {
        "B": B, "seed_base": 137001,
        "p_value": p, "n_ge": ge,
        "q95": float(np.quantile(perm_accs, 0.95)),
        "null_mean": float(perm_accs.mean()),
    }

    # ---- S1: full-vector 1-NN at layers[19] (non-binding) ----
    Df = np.linalg.norm(H[:, None, :] - H[None, :, :], axis=2)
    np.fill_diagonal(Df, np.inf)
    nnf = Df.argmin(axis=1)
    s1 = float(np.mean(labels[nnf] == labels))
    results["secondary"] = {"S1_full_vector_layers19": s1}

    # ---- S2: 8 random-direction 1-D controls (non-binding) ----
    rng2 = np.random.default_rng(137002)
    s2 = []
    for _ in range(8):
        u = rng2.standard_normal(1024)
        u /= np.linalg.norm(u)
        sc = H @ u
        acc_u, _ = knn_loo_accuracy(sc, labels)
        s2.append(acc_u)
    results["secondary"]["S2_random_directions"] = s2
    results["secondary"]["S2_seed"] = 137002

    results["status"] = "EXECUTED"
    results["elapsed_s"] = round(time.time() - t0, 1)
    write_report()
    print(json.dumps({"accuracy": acc, "p": p, "status": "EXECUTED"}))


def write_report():
    with open(OUT_DIR + "/exp137_report.json", "w") as f:
        json.dump(results, f, indent=2)


if __name__ == "__main__":
    main()
