"""EXP092 scoring — per-layer 1-NN leave-one-out + stratified permutation null.

Signed protocol: experiments/protocols/EXP092_IBL_PREREG_SIGNED.md
(§3 statistic; §4 null; §5 TOTAL decision tree; §6 G4 instrument gate;
§7 secondaries S1/S2 — pre-registered, non-binding).

Pipeline:
  1. Load layers (24, 60, dim) + labels + phrasing + domain + option logits.
  2. Per layer: pairwise Euclidean distance matrix -> LOO 1-NN accuracy a_l
     (K=20 labels; chance 0.05). Exact distance ties -> RUN-INVALID (§3:
     the bundle asserts zero ties).
  3. G4 instrument-health gate: for each layer, the permutation-null
     distribution's spread must be non-zero; zero spread -> RUN-INVALID
     (a deaf instrument yields no verdict, never KILL).
  4. Stratified permutation null (B=1,000/layer, labels permuted within
     (domain x phrasing) strata via random.Random(9207+b)): p_l, q95_l.
  5. §5 TOTAL decision tree with Bonferroni alpha_B = 0.05/24 and the
     10pp effect bar.
  6. Secondaries (reported, never decision-driving): S1 (KSG mixed kNN-MI
     after PCA<=20, Ross 2014), S2 (LM log-prob baseline from option logits).

Pure numpy (+ stdlib random for the registered RNG scheme) — no torch.
"""

import argparse
import json
import math
import os
import random
import sys

import numpy as np

N_ITEMS = 60
N_LAYERS = 24
N_CLASSES = 20
ALPHA_B = 0.05 / 24        # Bonferroni (signed §4)
EFFECT_BAR = 0.10          # 10pp (signed §5)
PERM_B = 1000              # signed §4
PERM_SEED = 9207           # registered RNG seed (same as reference impl)
EXCLUDED_LAYER = 20        # EXP091 already read layer 20 (§5: PIVOT, not CONTINUE)
S1_PCA_DIMS = 20           # signed §7 S1
S1_K = 3                   # kNN-MI neighbor count


class RunInvalid(Exception):
    """Guard failure -> RUN-INVALID (withheld, never a verdict)."""


def loo_1nn_accuracy(dist2, labels, assert_no_ties=True):
    """Leave-one-out 1-NN accuracy from a squared-distance matrix.

    dist2: (n, n) pairwise squared Euclidean distances.
    labels: (n,) integer label ids.
    Returns (accuracy, n_ties). If assert_no_ties and any item's nearest
    neighbor is not unique (exact float tie), raises RunInvalid (§3).
    """
    n = dist2.shape[0]
    d = dist2.copy()
    np.fill_diagonal(d, np.inf)          # leave-one-out
    nearest = d.argmin(axis=1)
    if assert_no_ties:
        # exact-tie check: more than one candidate attains the row minimum
        row_min = d[np.arange(n), nearest]
        n_at_min = (np.abs(d - row_min[:, None]) == 0).sum(axis=1)
        n_ties = int((n_at_min > 1).sum())
        if n_ties:
            raise RunInvalid(
                f"TIE FAIL: {n_ties}/{n} items have non-unique nearest "
                f"neighbors (exact float ties) — RUN-INVALID (§3).")
    else:
        n_ties = 0
    pred = labels[nearest]
    return float((pred == labels).mean()), n_ties


def strata_indices(domain, phrasing):
    """Registered §4 strata: (domain x phrasing) index lists."""
    strata = {}
    for i, (d, p) in enumerate(zip(domain, phrasing)):
        strata.setdefault((str(d), str(p)), []).append(i)
    return list(strata.values())


def permutation_null(dist2, label_ids, strata, B=PERM_B, seed=PERM_SEED,
                   assert_no_ties=True):
    """Stratified permutation null for the 1-NN LOO accuracy.

    Registered scheme (reference_implementation.stratified_permutation_p):
    permutation b shuffles labels within strata via random.Random(seed + b);
    p = (1 + #{acc_b >= acc_obs}) / (1 + B); q95 = 95th percentile.
    Returns (acc_obs, p, q95, null_dist).

    assert_no_ties: the registered §3 rule asserts zero exact distance ties
    (RUN-INVALID). It may be relaxed only in tests probing the permutation
    scheme itself on synthetic integer-valued distances.
    """
    acc_obs, _ = loo_1nn_accuracy(dist2, label_ids,
                                  assert_no_ties=assert_no_ties)
    null_accs = np.empty(B)
    for b in range(B):
        rng = random.Random(seed + b)
        perm = label_ids.copy()
        for idxs in strata:
            sub = [int(perm[i]) for i in idxs]
            rng.shuffle(sub)
            for i, s in zip(idxs, sub):
                perm[i] = s
        null_accs[b], _ = loo_1nn_accuracy(dist2, perm,
                                           assert_no_ties=assert_no_ties)
    ge = int((null_accs >= acc_obs).sum())
    p = (1 + ge) / (1 + B)
    q95 = float(np.percentile(null_accs, 95))
    return acc_obs, p, q95, null_accs


def adjudicate(layer_stats):
    """Apply the §5 TOTAL decision tree. Pure function (fully testable).

    layer_stats: list of 24 dicts {accuracy, p, q95} (layer index = position).
    Returns (verdict, detail_dict).
    """
    assert len(layer_stats) == N_LAYERS
    sig = [s["p"] < ALPHA_B for s in layer_stats]
    effect = [s["accuracy"] - s["q95"] for s in layer_stats]
    S = [l for l in range(N_LAYERS)
         if l != EXCLUDED_LAYER and sig[l] and effect[l] >= EFFECT_BAR]
    if S:
        l_star = max(S, key=lambda l: effect[l])
        return "CONTINUE", {
            "l_star": l_star,
            "effect": effect[l_star],
            "accuracy": layer_stats[l_star]["accuracy"],
            "p": layer_stats[l_star]["p"],
        }
    if not any(sig):
        return "KILL", {}
    # S empty but some layer significant: sub-threshold effect and/or the
    # layer-20-only case -> PIVOT (honest ambiguity, no re-targeting).
    sig_layers = [l for l in range(N_LAYERS) if sig[l]]
    return "PIVOT", {"significant_layers": sig_layers,
                     "effects": {l: effect[l] for l in sig_layers}}


def _pca_project(X, n_dims):
    """Center + SVD projection to n_dims components (numpy only)."""
    Xc = X - X.mean(axis=0)
    U, s, _ = np.linalg.svd(Xc, full_matrices=False)
    k = min(n_dims, U.shape[1])
    return (U[:, :k] * s[:k])


def _digamma(x):
    """Digamma via the asymptotic/recurrence expansion (no scipy)."""
    # recurrence to x >= 8, then asymptotic series
    r = 0.0
    while x < 8:
        r -= 1.0 / x
        x += 1.0
    inv = 1.0 / x
    inv2 = inv * inv
    return r + math.log(x) - 0.5 * inv - inv2 / 12.0 + inv2 * inv2 / 120.0


def s1_mi(X, label_ids, k=S1_K, n_dims=S1_PCA_DIMS):
    """S1 implementation (Ross 2014 mixed estimator). Returns float bits."""
    Z = _pca_project(np.asarray(X, dtype=np.float64), n_dims)
    n = Z.shape[0]
    labels = np.asarray(label_ids)
    # pairwise distances
    d2 = ((Z[:, None, :] - Z[None, :, :]) ** 2).sum(-1)
    d = np.sqrt(np.maximum(d2, 0.0))
    # k-th nearest neighbor distance (excluding self): partition index k
    # (index 0 is self at distance 0)
    part = np.partition(d, k, axis=1)
    eps = part[:, k]
    # m_i: points within eps (includes self)
    m = (d <= eps[:, None]).sum(axis=1).astype(float)
    # N_{y_i}
    _, inv = np.unique(labels, return_inverse=True)
    counts = np.bincount(inv).astype(float)
    Ny = counts[inv]
    psi = np.vectorize(_digamma)
    mi = (_digamma(n) - psi(Ny).mean() + _digamma(k) - psi(m).mean())
    return float(mi / math.log(2.0))  # nats -> bits


def s2_lm_baseline(opt_logits):
    """S2: LM log-prob baseline. opt_logits: (n, 2) [target, foil] logits.

    Accuracy of argmax over the two options + mean log-prob margin for the
    target. Non-binding secondary (signed §7)."""
    opt_logits = np.asarray(opt_logits, dtype=np.float64)
    # log-softmax over the two options
    m = opt_logits.max(axis=1, keepdims=True)
    log_z = m + np.log(np.exp(opt_logits - m).sum(axis=1, keepdims=True))
    logp = opt_logits - log_z
    correct = logp[:, 0] > logp[:, 1]
    return {
        "accuracy": float(correct.mean()),
        "n_correct": int(correct.sum()),
        "mean_logprob_margin_target_minus_foil": float(
            (logp[:, 0] - logp[:, 1]).mean()),
    }


def decide_from_embeddings(emb_path, perm_b=PERM_B):
    """Full scoring pass over an embeddings bundle. Returns the report dict."""
    z = np.load(emb_path, allow_pickle=True)
    layers = z["layers"]                      # (24, 60, dim)
    labels_raw = [str(x) for x in z["labels"]]
    phrasing = [str(x) for x in z["phrasing"]]
    domain = [str(x) for x in z["domain"]]
    opt_logits = z["opt_logits"]
    assert layers.shape[0] == N_LAYERS and layers.shape[1] == N_ITEMS, \
        f"layers shape {layers.shape} != ({N_LAYERS}, {N_ITEMS})"
    assert len(labels_raw) == N_ITEMS

    # integer label ids (K=20)
    uniq = sorted(set(labels_raw))
    assert len(uniq) == N_CLASSES, f"K={len(uniq)} != {N_CLASSES}"
    lid = {u: i for i, u in enumerate(uniq)}
    label_ids = np.array([lid[u] for u in labels_raw], dtype=int)
    strata = strata_indices(domain, phrasing)
    assert sum(len(s) for s in strata) == N_ITEMS and len(strata) == 4, \
        "strata malformed"

    layer_stats = []
    for l in range(N_LAYERS):
        X = layers[l].astype(np.float64)
        d2 = ((X[:, None, :] - X[None, :, :]) ** 2).sum(-1)
        acc_obs, p, q95, null_dist = permutation_null(
            d2, label_ids, strata, B=perm_b)
        # G4: the null distribution must have non-zero spread — a deaf
        # instrument yields RUN-INVALID, never a verdict (§6).
        spread = float(null_dist.max() - null_dist.min())
        if spread == 0.0:
            raise RunInvalid(
                f"G4 FAIL: layer {l} null distribution has zero spread "
                f"(instrument degenerate) — RUN-INVALID (withheld, not a "
                f"verdict).")
        s1 = s1_mi(X, label_ids)
        layer_stats.append({
            "layer": l, "accuracy": acc_obs, "p": p, "q95": q95,
            "effect": acc_obs - q95, "null_spread": spread, "S1_mi_bits": s1,
        })

    verdict, detail = adjudicate(layer_stats)
    s2 = s2_lm_baseline(opt_logits)
    return {
        "verdict": verdict,
        "verdict_detail": detail,
        "alpha_bonferroni": ALPHA_B,
        "effect_bar": EFFECT_BAR,
        "perm_B": perm_b,
        "n_layers": N_LAYERS,
        "n_items": N_ITEMS,
        "n_classes": N_CLASSES,
        "layers": layer_stats,
        "S2": s2,
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description="EXP092 per-layer 1-NN scoring")
    ap.add_argument("--embeddings", required=True,
                    help="path to exp092_embeddings.npz")
    ap.add_argument("--out-dir", required=True)
    args = ap.parse_args(argv)
    try:
        report = decide_from_embeddings(args.embeddings)
    except RunInvalid as e:
        print(f"RUN-INVALID: {e}", file=sys.stderr)
        return 3
    # Mode stamp (Law #14 F1, carried forward from EXP091): the extraction
    # meta colocated with the embeddings bundle; absent meta -> "unknown".
    meta_path = os.path.join(os.path.dirname(os.path.abspath(args.embeddings)),
                             "exp092_extraction_meta.json")
    mode = "unknown"
    if os.path.isfile(meta_path):
        try:
            with open(meta_path) as f:
                mode = json.load(f).get("mode", "unknown")
        except (OSError, ValueError):
            mode = "unknown"
    report["mode"] = mode
    os.makedirs(args.out_dir, exist_ok=True)
    out_path = os.path.join(args.out_dir, "exp092_report.json")
    with open(out_path, "w") as f:
        json.dump(report, f, indent=2)
    r = report
    best = max(r["layers"], key=lambda s: s["accuracy"])
    print(f"best layer: {best['layer']} acc={best['accuracy']:.4f} "
          f"p={best['p']:.4g} effect={best['effect']:+.4f}")
    print(f"AUTHORITATIVE VERDICT: {r['verdict']} (mode={r['mode']})")
    print(f"report written: {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
