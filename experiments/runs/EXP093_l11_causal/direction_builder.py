"""EXP093 direction builder — LOO maximum-average-cosine shared correction
directions v^(-i) from the archived EXP092 layer-11 embeddings.

Registered construction (draft §3.1, v0.2 — replaces the algebraically
degenerate v0.1 formula, preserved on record in the draft's §3.1 correction
note and NOT used here):

    h(i)      = layer-11 final-token embedding of item i      (60, 1024)
    c^(-i)(i) = mean{ h(k) : k != i, target(k) = target(i) }  (mean of 2)
    r_i       = c^(-i)(i) - h(i);  assert ||r_i|| > 1e-9  (else RUN-INVALID)
    u_i       = r_i / ||r_i||                            (unit LOO correction)
    v^(-i)    = normalize( (1/59) * sum_{j != i} u_j )    (no item-i leakage)

Why this is non-degenerate: the unnormalized mean sum_j[c(j)-h(j)] is
identically zero (residuals-from-class-means sum to zero, exactly, including
under LOO — the v0.1 defect). Per-item normalization before averaging breaks
the zero-sum; v^(-i) maximizes average cosine with the 60 LOO corrections.

numpy-only. The archived .npz is opened READ-ONLY. No torch, no weights.
"""

import json
import os
import sys

import numpy as np

R_MIN_ASSERT = 1e-9  # draft §3.1 / G2: ||r_i|| > 1e-9 else RUN-INVALID
N_ITEMS = 60
LAYER = 11

# Reviewer-verified registered measurements on the archived .npz (LOG-4340 /
# LOG-4342 addendum, float64). The build-time artifact asserts against these
# with the tolerances below (sanity: we are reading the right data).
REGISTERED = {
    "min_r_norm": 1.3352,
    "mean_pairwise_cosine_u": -0.0160,
    "prenorm_min": 0.0246,
    "prenorm_max": 0.0444,
    "max_pairwise_cosine_v": 0.9554,
}
BUILD_TOL = 1e-3


class RunInvalid(Exception):
    """Direction-construction failure -> RUN-INVALID (withheld, never a verdict)."""


def _labels_match(npz_labels, bench_targets):
    return [str(x) for x in npz_labels] == list(bench_targets)


def build_directions(layer11, labels, bench_targets=None):
    """Compute {r_i}, {u_i}, {v^(-i)} + coherence diagnostics.

    layer11: (60, 1024) float32/float64 array (layer-11 final-token states).
    labels: length-60 sequence of target-entity names, item order = bench order.
    bench_targets: optional length-60 sequence to assert item-order identity.

    Returns dict with keys: r, r_norms, u, v, min_r_norm, mean_pairwise_cosine_u,
    prenorm_norms, max_pairwise_cosine_v, all_unit_norm, r4_not_bit_identical.
    Raises RunInvalid on any G2 assertion failure.
    """
    if bench_targets is not None and not _labels_match(labels, bench_targets):
        raise RunInvalid(
            "G2 FAIL: .npz stored label vector does not match the bench "
            "target sequence (item-order assertion) — RUN-INVALID.")
    X = np.asarray(layer11, dtype=np.float64)
    if X.shape != (N_ITEMS, 1024):
        raise RunInvalid(
            f"G2 FAIL: layer-11 array shape {X.shape} != (60, 1024) — "
            "RUN-INVALID.")
    lab = np.array([str(x) for x in labels])
    if len(lab) != N_ITEMS:
        raise RunInvalid(
            f"G2 FAIL: {len(lab)} labels != 60 — RUN-INVALID.")

    r = np.zeros_like(X)
    for i in range(N_ITEMS):
        mask = (lab == lab[i])
        mask[i] = False
        proto = X[mask].mean(axis=0)   # mean of 2 (3 items per target, minus i)
        r[i] = proto - X[i]
    r_norms = np.linalg.norm(r, axis=1)
    if not np.all(r_norms > R_MIN_ASSERT):
        bad = np.nonzero(r_norms <= R_MIN_ASSERT)[0].tolist()
        raise RunInvalid(
            f"G2 FAIL: ||r_i|| <= 1e-9 for items {bad} — an item coincides "
            "with its LOO prototype; direction undefined — RUN-INVALID.")
    u = r / r_norms[:, None]

    v = np.zeros_like(u)
    prenorm_norms = np.zeros(N_ITEMS)
    for i in range(N_ITEMS):
        keep = np.ones(N_ITEMS, dtype=bool)
        keep[i] = False
        m = u[keep].mean(axis=0)          # (1/59) * sum_{j != i} u_j
        n = float(np.linalg.norm(m))
        prenorm_norms[i] = n
        if n == 0.0:
            raise RunInvalid(
                f"G2 FAIL: pre-normalization shared-direction norm is 0 for "
                f"item {i} — RUN-INVALID.")
        v[i] = m / n
    v_norms = np.linalg.norm(v, axis=1)
    if not np.allclose(v_norms, 1.0, rtol=0, atol=1e-9):
        raise RunInvalid(
            f"G2 FAIL: v^(-i) not unit-norm (min={v_norms.min()}, "
            f"max={v_norms.max()}) — RUN-INVALID.")

    # Coherence diagnostic (registered, reported, non-binding).
    iu = np.triu_indices(N_ITEMS, k=1)
    cos_u = (u[iu[0]] * u[iu[1]]).sum(axis=1)
    mean_cos_u = float(cos_u.mean())
    cos_v = (v[iu[0]] * v[iu[1]]).sum(axis=1)
    max_cos_v = float(cos_v.max())

    # R4 checkpoint (deferred recommendation, bundle-build): LOO must actually
    # vary the 60 directions — assert they are not all bit-identical.
    r4 = not np.all(v == v[0])
    if not r4:
        raise RunInvalid(
            "G2/R4 FAIL: all 60 v^(-i) are bit-identical — LOO construction "
            "degenerate — RUN-INVALID.")

    return {
        "r": r,
        "r_norms": r_norms,
        "u": u,
        "v": v,
        "min_r_norm": float(r_norms.min()),
        "mean_pairwise_cosine_u": mean_cos_u,
        "prenorm_norms": prenorm_norms,
        "prenorm_min": float(prenorm_norms.min()),
        "prenorm_max": float(prenorm_norms.max()),
        "max_pairwise_cosine_v": max_cos_v,
        "all_unit_norm": True,
        "r4_not_bit_identical": r4,
    }


def write_direction_verification(npz_path, bench_targets, out_path=None):
    """Build-time: execute the construction on the REAL archived .npz
    (read-only) and assert the registered measurements. Writes the
    verification artifact. Raises RunInvalid on mismatch."""
    z = np.load(npz_path, allow_pickle=True)
    layers = z["layers"]
    if layers.shape != (24, 60, 1024) or layers.dtype != np.float32:
        raise RunInvalid(
            f"G2 FAIL: .npz shape {layers.shape} dtype {layers.dtype} != "
            "(24, 60, 1024) float32 — RUN-INVALID.")
    d = build_directions(layers[LAYER], z["labels"], bench_targets)
    checks = {
        "min_r_norm": abs(d["min_r_norm"] - REGISTERED["min_r_norm"]),
        "mean_pairwise_cosine_u": abs(d["mean_pairwise_cosine_u"]
                                      - REGISTERED["mean_pairwise_cosine_u"]),
        "prenorm_min": abs(d["prenorm_min"] - REGISTERED["prenorm_min"]),
        "prenorm_max": abs(d["prenorm_max"] - REGISTERED["prenorm_max"]),
        "max_pairwise_cosine_v": abs(d["max_pairwise_cosine_v"]
                                     - REGISTERED["max_pairwise_cosine_v"]),
    }
    bad = {k: v for k, v in checks.items() if v > BUILD_TOL}
    artifact = {
        "experiment": "EXP093",
        "guard": "G2",
        "npz": os.path.basename(npz_path),
        "construction": "LOO maximum-average-cosine shared correction (v0.2)",
        "min_r_norm": d["min_r_norm"],
        "r_assert": f"60/60 ||r_i|| > {R_MIN_ASSERT}",
        "mean_pairwise_cosine_u": d["mean_pairwise_cosine_u"],
        "prenorm_norm_range": [d["prenorm_min"], d["prenorm_max"]],
        "max_pairwise_cosine_v": d["max_pairwise_cosine_v"],
        "all_v_unit_norm": d["all_unit_norm"],
        "r4_not_bit_identical": d["r4_not_bit_identical"],
        "registered": REGISTERED,
        "abs_deviations": checks,
        "gate": "PASS" if not bad else "FAIL",
    }
    if bad:
        raise RunInvalid(
            f"G2 build-time FAIL: registered-measurement deviations exceed "
            f"tol {BUILD_TOL}: {bad} — RUN-INVALID.")
    out_path = out_path or os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "direction_verification.json")
    with open(out_path, "w") as f:
        json.dump(artifact, f, indent=1, sort_keys=True)
    return artifact


def main(argv=None):
    """CLI: python3 direction_builder.py --out-dir <dir> [--npz <path>].

    Build-time execution of the G2 direction construction on the real
    archived .npz (read-only), asserting the registered measurements.
    Writes <out-dir>/direction_verification.json. numpy-only."""
    import argparse
    ap = argparse.ArgumentParser(
        description="EXP093 G2 direction builder (numpy-only, read-only .npz)")
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--npz", default=None,
                    help="override the archived .npz path")
    args = ap.parse_args(argv)

    import protocol_pin as pin  # same directory; numpy-only
    this_dir = os.path.dirname(os.path.abspath(__file__))
    exp092_dir = os.path.abspath(os.path.join(this_dir, "..", "EXP092_ibl"))
    sys.path.append(exp092_dir)
    import reference_implementation as ref  # canonical EXP092-B bench

    npz_path = args.npz or pin.npz_path()
    bench = ref.build_bench()
    bench_targets = [b["ent"] for b in bench]
    os.makedirs(args.out_dir, exist_ok=True)
    artifact = write_direction_verification(
        npz_path, bench_targets,
        out_path=os.path.join(args.out_dir, "direction_verification.json"))
    print(json.dumps({k: artifact[k] for k in (
        "gate", "min_r_norm", "mean_pairwise_cosine_u",
        "prenorm_norm_range", "max_pairwise_cosine_v",
        "r4_not_bit_identical")}, indent=1))
    print(f"[builder] wrote {args.out_dir}/direction_verification.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
