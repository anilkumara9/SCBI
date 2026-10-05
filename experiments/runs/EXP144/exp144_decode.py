"""EXP144 decode-arm scoring — per-layer LOO 1-NN + stratified null (S7-2 §3.3).

Verbatim port of the committed EXP092 scorer with the plan's D2/D3/D5
deviations: 12 layers (Bonferroni α=0.05/12), stratified-permutation seed
20261007 (pre-registered), 768 dims. No layer exclusion (the plan licenses
none — EXP092's layer-20 exclusion was EXP091-specific).

S7-2 §3.3 steps executed here: 1-NN scan (K=20, chance 0.05, B=1000), G4
null-spread asserts (S0.4), l* selection, S2 LM baseline (feeds the G4
baseline-reproduction refs for the decision loop).

numpy only (no weights touched).
"""

import json
import math
import os
import random
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import exp144_common as C  # noqa: E402

EMB = os.path.join(C.RUN_DIR, "exp144_embeddings.npz")
OUT = os.path.join(C.RUN_DIR, "exp144_decode_report.json")


def loo_1nn_accuracy(dist2, labels, assert_no_ties=True):
    n = dist2.shape[0]
    d = dist2.copy()
    np.fill_diagonal(d, np.inf)
    nearest = d.argmin(axis=1)
    if assert_no_ties:
        row_min = d[np.arange(n), nearest]
        n_at_min = (np.abs(d - row_min[:, None]) == 0).sum(axis=1)
        n_ties = int((n_at_min > 1).sum())
        if n_ties:
            raise C.RunInvalid(
                f"TIE FAIL: {n_ties}/{n} items have non-unique nearest "
                f"neighbors (exact float ties) — RUN-INVALID (§3).")
    pred = labels[nearest]
    return float((pred == labels).mean())


def permutation_null(dist2, label_ids, strata, B=C.PERM_B, seed=C.PERM_SEED):
    """Registered stratified scheme: permutation b shuffles labels within
    (domain x phrasing) strata via random.Random(seed + b); p=(1+ge)/(1+B)."""
    acc_obs = loo_1nn_accuracy(dist2, label_ids)
    null_accs = np.empty(B)
    for b in range(B):
        rng = random.Random(seed + b)
        perm = label_ids.copy()
        for idxs in strata:
            sub = [int(perm[i]) for i in idxs]
            rng.shuffle(sub)
            for i, s in zip(idxs, sub):
                perm[i] = s
        null_accs[b] = loo_1nn_accuracy(dist2, perm)
    ge = int((null_accs >= acc_obs).sum())
    return acc_obs, (1 + ge) / (1 + B), float(np.percentile(null_accs, 95)), \
        null_accs


def s2_lm_baseline(opt_logits):
    """S2: LM log-prob baseline from the two option logits (non-binding
    secondary). ALSO yields the raw-logit margin refs for G4
    baseline-reproduction in the decision loop."""
    L = np.asarray(opt_logits, dtype=np.float64)
    m = L.max(axis=1, keepdims=True)
    log_z = m + np.log(np.exp(L - m).sum(axis=1, keepdims=True))
    logp = L - log_z
    correct = logp[:, 0] > logp[:, 1]
    raw_margin = L[:, 0] - L[:, 1]
    return {
        "accuracy": float(correct.mean()),
        "n_correct": int(correct.sum()),
        "mean_logprob_margin_target_minus_foil": float(
            (logp[:, 0] - logp[:, 1]).mean()),
        # G4 refs (raw-logit margins, mirroring EXP093's G4_MARGIN_REF):
        "mean_raw_logit_margin": float(raw_margin.mean()),
        "n_correct_raw": int((raw_margin > 0.0).sum()),
    }


def main():
    z = np.load(EMB, allow_pickle=True)
    layers = z["layers"]
    assert layers.shape[0] == C.N_LAYERS and layers.shape[1] == C.N_ITEMS, \
        layers.shape
    labels_raw = [str(x) for x in z["labels"]]
    phrasing = [str(x) for x in z["phrasing"]]
    domain = [str(x) for x in z["domain"]]
    opt_logits = z["opt_logits"]

    uniq = sorted(set(labels_raw))
    assert len(uniq) == 20, f"K={len(uniq)} != 20"
    lid = {u: i for i, u in enumerate(uniq)}
    label_ids = np.array([lid[u] for u in labels_raw], dtype=int)
    strata = {}
    for i, (d, p) in enumerate(zip(domain, phrasing)):
        strata.setdefault((str(d), str(p)), []).append(i)
    strata = list(strata.values())
    assert sum(len(s) for s in strata) == C.N_ITEMS and len(strata) == 4

    layer_stats = []
    for l in range(C.N_LAYERS):
        X = layers[l].astype(np.float64)
        d2 = ((X[:, None, :] - X[None, :, :]) ** 2).sum(-1)
        acc, p, q95, null = permutation_null(d2, label_ids, strata)
        spread = float(null.max() - null.min())
        if spread == 0.0:  # S0.4: null-spread non-zero (deaf instrument)
            raise C.RunInvalid(
                f"S0.4/G4 FAIL: layer {l} null distribution has zero spread "
                f"— RUN-INVALID.")
        layer_stats.append({
            "layer": l, "accuracy": acc, "p": p, "q95": q95,
            "effect": acc - q95, "null_spread": spread,
        })
        print(f"[decode] layer {l:2d}: acc={acc:.4f} p={p:.4g} "
              f"q95={q95:.4f} effect={acc - q95:+.4f}", flush=True)

    # S7-2 §3.3 step 4: l* = argmax(acc - q95) over layers passing BOTH bars.
    passing = [s for s in layer_stats
               if s["p"] < C.ALPHA_B and s["effect"] >= C.EFFECT_BAR]
    decode_plus_d1 = len(passing) > 0
    l_star = max(passing, key=lambda s: s["effect"])["layer"] \
        if decode_plus_d1 else None
    print(f"[decode] D1 (≥1 layer p<{C.ALPHA_B:.6f} & effect≥0.10): "
          f"{'PASS' if decode_plus_d1 else 'FAIL'}; "
          f"l*={l_star}; passing={[s['layer'] for s in passing]}", flush=True)

    s2 = s2_lm_baseline(opt_logits)
    print(f"[decode] S2: acc={s2['accuracy']:.4f} ({s2['n_correct']}/60); "
          f"mean raw-logit margin={s2['mean_raw_logit_margin']:.6f}",
          flush=True)

    report = {
        "experiment": "EXP144",
        "arm": "decode",
        "n_layers": C.N_LAYERS, "n_items": C.N_ITEMS, "n_classes": 20,
        "alpha_bonferroni": C.ALPHA_B, "effect_bar": C.EFFECT_BAR,
        "perm_B": C.PERM_B, "perm_seed": C.PERM_SEED,
        "layers": layer_stats,
        "D1": decode_plus_d1,
        "l_star": l_star,
        "passing_layers": [s["layer"] for s in passing],
        "S2": s2,
    }
    with open(OUT, "w") as f:
        json.dump(report, f, indent=1)
    print(f"[decode] wrote {OUT}", flush=True)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except C.RunInvalid as e:
        print(f"RUN-INVALID: {e}", flush=True)
        sys.exit(3)
