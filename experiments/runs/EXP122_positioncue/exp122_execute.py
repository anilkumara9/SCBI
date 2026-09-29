#!/usr/bin/env python3
"""EXP122 execution (H16/POSITION-CUE) — LOG-4653.

Executes the signed pre-registration
research/prereg/EXP_PREREG_H16_POSITIONCUE_2026-09-29.md exactly (Law #14 SIGN,
four fixes byte-verified, LOG-4652). Stage A: bench-3 construction gates (the
breaking point). Stage B: 60 fresh layer-20 extractions, pinned H5 head
protocol, binding bars. $0 CPU. No generation. No signed artifact modified.
"""
import hashlib, json, math, os, sys, time

import numpy as np
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

RUN_DIR = os.path.expanduser("~/workspace/SCBI/experiments/runs/EXP122_positioncue")
OUT = os.path.join(RUN_DIR, "out")
os.makedirs(OUT, exist_ok=True)
sys.path.insert(0, RUN_DIR)
from build_exp122_bench import (build_bench, verify_cells, canonical_json,
                                bench_sha256, gate_gc1, gate_gc2, gate_gc3,
                                gate_position_scramble)

LOGF = open(os.path.join(OUT, "exp122_console.log"), "w")
def log(s):
    print(s, flush=True); LOGF.write(s + "\n"); LOGF.flush()

SNAP = os.path.expanduser("~/workspace/.exp086_weights/pythia-410m")
WEIGHTS_PIN = "ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed"
SEED = 20260929
SITE = 20

t0 = time.time()
# --- Pins: environment -------------------------------------------------
torch.manual_seed(0); np.random.seed(0)
log(f"ENV torch={torch.__version__} transformers={__import__('transformers').__version__} "
    f"sklearn={__import__('sklearn').__version__} numpy={np.__version__}")
assert torch.__version__ == "2.14.0+cpu", "torch pin drift"
assert __import__('transformers').__version__ == "5.17.0", "transformers pin drift"
assert np.__version__ == "2.5.3", "numpy pin drift"
assert __import__('sklearn').__version__ == "1.9.1", "sklearn pin drift"
torch.set_num_threads(2)
thr_set, thr_read = 2, torch.get_num_threads()
log(f"threads set={thr_set} read_back={thr_read}")
assert thr_read == 2, "thread count not honoured"

def state_dict_hash(model):
    sha = hashlib.sha256()
    for k in sorted(model.state_dict().keys()):
        sha.update(np.asarray(model.state_dict()[k].detach().cpu(),
                              dtype=np.float32).tobytes())
    return sha.hexdigest()

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def binom_one_sided(k, n):
    """Exact one-sided P(X >= k | n, 0.5), executor-computed (math.comb)."""
    return sum(math.comb(n, i) for i in range(k, n + 1)) / 2 ** n

def binom_two_sided(k, n):
    """Exact two-sided p (doubling the smaller tail), executor-computed."""
    import math as _m
    one = binom_one_sided(k, n)
    lo = sum(_m.comb(n, i) for i in range(0, n - k + 1)) / 2 ** n
    return min(1.0, 2 * min(one, lo))

# --- Stage A: bench-3 construction (the breaking point) -----------------
log("STAGE A: bench-3 construction gates")
bench = build_bench()
v = verify_cells(bench)
log(f"design-time assertions OK: n={v['n']} pin={v['pin']}")
g1 = gate_gc1(bench)
log(f"G-C1 pure-template detector: {g1['score']}/60 pass={g1['pass']}")
gp = gate_position_scramble(bench)
log(f"position-scramble gate: {gp['score']}/60 pass={gp['pass']}")
g2 = gate_gc2(bench)
log(f"G-C2 entity-rank correlation: {g2['pearson']:+.4f} (|.|={g2['abs_pearson']:.4f}) pass={g2['pass']}")
g3 = gate_gc3()
log(f"G-C3 decomposition pin: suffix_byte_exact={g3['suffix_byte_exact']} "
    f"deterministic={g3['deterministic']} pass={g3['pass']}")
construction_ok = (v['n'] == 60 and g1['pass'] and gp['pass']
                   and g2['pass'] and g3['pass'])
if not construction_ok:
    log("RUN-INVALID (construction): a section 3.2 gate failed — no head trained, "
        "no metric read (pre-reg section 0 breaking point)")
    json.dump({"verdict": "RUN-INVALID",
               "branch": "construction-fate: section 3.2 gate failure",
               "gates": {"design": {k: (str(val) if not isinstance(val, (int, float, bool, str, type(None))) else val)
                                     for k, val in v.items()},
                         "G-C1": g1, "position-scramble": gp,
                         "G-C2": g2, "G-C3": g3}},
              open(os.path.join(OUT, "exp122_result.json"), "w"), indent=2)
    sys.exit(45)

# Persist bench records before any model contact / verdict (record-keeping gate).
canon_path = os.path.join(OUT, "exp122_bench3_canonical.json")
with open(canon_path, "wb") as f:
    f.write(canonical_json(bench))
per_item_path = os.path.join(OUT, "exp122_per_item.json")
with open(per_item_path, "w") as f:
    json.dump(bench, f, indent=1, sort_keys=True)
pin = bench_sha256(bench)
h_a, h_b = sha256_file(canon_path), sha256_file(canon_path)
assert h_a == h_b == pin, "canonical JSON not byte-stable"
log(f"bench-3 canonical pin {pin} persisted; re-parse x2 byte-identical")

# --- Backbone load + pre-extraction hash --------------------------------
log("loading tokenizer + frozen model...")
tokenizer = AutoTokenizer.from_pretrained(SNAP, local_files_only=True)
try:
    model = AutoModelForCausalLM.from_pretrained(SNAP, local_files_only=True,
                                                 torch_dtype=torch.float32,
                                                 device_map="cpu")
    log("device_map='cpu' accepted")
except Exception as e:
    model = AutoModelForCausalLM.from_pretrained(SNAP, local_files_only=True,
                                                 torch_dtype=torch.float32)
    log(f"device_map='cpu' dropped (CPU-only no-op, EXP111-recorded behavior): {type(e).__name__}")
model.eval(); model.requires_grad_(False)
pre = state_dict_hash(model)
log(f"backbone pre-extraction hash: {pre[:16]}... match={pre == WEIGHTS_PIN}")
if pre != WEIGHTS_PIN:
    log("RUN-INVALID: backbone hash mismatch (Law #6)"); sys.exit(43)

# --- Stage B: 60 fresh layer-20 extractions (premises only) --------------
ids = [b["id"] for b in bench]
prem_by_id = {b["id"]: b["premise"] for b in bench}
rec_by_id = {b["id"]: b for b in bench}
for b in bench:
    assert b["premise"] == b["prompt"][:b["prompt"].index(" Question:")]
# Labels: y=1 iff tuple[0] in D1 (animals) — the builder's construction
# docstring plus the independent per-item pin in verify_cells (Law #7).
y = np.array([rec_by_id[i]["y"] for i in ids], dtype=int)
texts = [prem_by_id[i] for i in ids]
log("extracting bench-3 (60 passes, premise-only, hidden_states[20])...")
embs = np.zeros((60, model.config.hidden_size), dtype=np.float32)
with torch.no_grad():
    for i, t in enumerate(texts):
        tid = torch.tensor([tokenizer.encode(t, add_special_tokens=False)],
                           dtype=torch.long)
        out = model(tid, output_hidden_states=True)
        embs[i, :] = (out.hidden_states[SITE][0, -1, :]
                      .detach().cpu().to(torch.float32).numpy())
        if (i + 1) % 20 == 0:
            log(f"  {i + 1}/60")
assert embs.shape == (60, 1024) and embs.dtype == np.float32
assert np.isfinite(embs).all(), "non-finite embedding values"

post = state_dict_hash(model)
log(f"backbone post-extraction hash: {post[:16]}... match={post == WEIGHTS_PIN} (Δθ=0)")
if post != WEIGHTS_PIN:
    log("RUN-INVALID: post-extraction backbone drift"); sys.exit(44)

npz_path = os.path.join(OUT, "exp122_embeddings.npz")
np.savez(npz_path, embeddings=embs, ids=np.array(ids, dtype=str))
loaded = np.load(npz_path)
assert list(loaded["ids"]) == ids and len(ids) == 60, "npz/id mismatch"
assert set(loaded["ids"]) == set(rec_by_id), "bench/per-item ID mismatch"
log("npz ids byte-match per-item records (60/60)")

# --- Split (H5 section 3.3 pinned verbatim) -------------------------------
key = np.array([f"{rec_by_id[i]['phrasing']}_{rec_by_id[i]['flipped']}" for i in ids])
flipped = np.array([bool(rec_by_id[i]["flipped"]) for i in ids])
idx = np.arange(60)
tr, te = train_test_split(idx, test_size=0.5, random_state=SEED, stratify=key)
ov = set(ids[i] for i in tr) & set(ids[i] for i in te)
assert not ov, "train/test ID overlap → RUN-INVALID (Law #7)"
from collections import Counter
cell_counts = Counter(key[te])
NF = int((~flipped[te]).sum()); NT = int(flipped[te].sum())
log(f"split: train n={len(tr)} test n={len(te)} overlap=0; "
    f"per-cell test counts={dict(sorted(cell_counts.items()))}; N_F={NF} N_T={NT}")
assert NF == 15 and NT == 15, "pinned N_F/N_T denominators violated"
train_ids_path = os.path.join(OUT, "exp122_train_ids.json")
test_ids_path = os.path.join(OUT, "exp122_test_ids.json")
json.dump([ids[i] for i in tr], open(train_ids_path, "w"))
json.dump([ids[i] for i in te], open(test_ids_path, "w"))

# --- Head training (H5 section 3.3 pinned verbatim; Law #7 no tuning) -----
clf = LogisticRegression(penalty="l2", C=1.0, solver="lbfgs",
                         max_iter=1000, random_state=SEED)
clf.fit(embs[tr], y[tr])
pred = clf.predict(embs[te])
# Determinism pass: re-fit from the same npz → byte-identical predictions.
clf2 = LogisticRegression(penalty="l2", C=1.0, solver="lbfgs",
                          max_iter=1000, random_state=SEED)
clf2.fit(embs[tr], y[tr])
pred2 = clf2.predict(embs[te])
assert np.array_equal(pred, pred2), "determinism re-fit mismatch → RUN-INVALID"
log("determinism re-fit pass: byte-identical test predictions")
head_hash = hashlib.sha256(
    np.ascontiguousarray(clf.coef_, dtype=np.float64).tobytes() +
    np.ascontiguousarray(clf.intercept_, dtype=np.float64).tobytes()).hexdigest()
log(f"head weight hash: {head_hash[:16]}... norm={float(np.linalg.norm(clf.coef_)):.6f}")
head_path = os.path.join(OUT, "exp122_head_params.npz")
np.savez(head_path, coef_=clf.coef_, intercept_=clf.intercept_)

# --- Artifact-existence gate (section 3.7): ALL records pinned BEFORE verdict
artifacts = {
    "builder_script": os.path.join(RUN_DIR, "build_exp122_bench.py"),
    "canonical_json": canon_path,
    "per_item_json": per_item_path,
    "embeddings_npz": npz_path,
    "train_ids": train_ids_path,
    "test_ids": test_ids_path,
    "head_params": head_path,
}
artifact_hashes = {}
for name, path in artifacts.items():
    ok = os.path.isfile(path)
    artifact_hashes[name] = sha256_file(path) if ok else None
    log(f"artifact {name}: {'present ' + artifact_hashes[name][:16] + '...' if ok else 'MISSING'}")
if any(h is None for h in artifact_hashes.values()):
    log("RUN-INVALID (incomplete record): section 3.7 artifact-existence gate failed")
    sys.exit(46)

# --- Evaluation (n=30 held-out; Law #9 registered metrics) ----------------
acc = float((pred == y[te]).mean())
accF = float((pred[~flipped[te]] == y[te][~flipped[te]]).mean())
accT = float((pred[flipped[te]] == y[te][flipped[te]]).mean())
G = accF - accT
correct = int((pred == y[te]).sum())
per_cell = {str(k): float((pred[key[te] == k] == y[te][key[te] == k]).mean())
            for k in sorted(set(key[te]))}
train_acc = float(clf.score(embs[tr], y[tr]))
# Executor-computed p-values (defect class (a): never handwritten).
p_one = binom_one_sided(correct, 30)
p_two = binom_two_sided(correct, 30)
log(f"test: {correct}/30 = {acc:.4f}; acc(F)={accF:.4f} (N_F={NF}); "
    f"acc(T)={accT:.4f} (N_T={NT}); G={G:+.4f}")
log(f"executor-computed p: one-sided={p_one:.7f} two-sided={p_two:.7f}")
log(f"per-cell (descriptive): {per_cell}; train acc (sanity): {train_acc:.4f}")

# --- Binding bars (pre-reg section 4 verbatim; G kill-test takes precedence)
if G >= 0.30:
    verdict, branch = ("KILL", "G >= 0.30 → identity-readout interpretation KILLED; "
                       "EXP111/EXP120 bench observations stand (Law #8); two-bench "
                       "CONTINUE reclassified as position-detector correlation (Law #11)")
elif acc >= 20/30 and G < 0.30:
    verdict, branch = ("CONTINUE", "overall >= 20/30 with G < 0.30 → "
                       "identity readout survives position decorrelation "
                       "(decodability only, pre-reg section 7)")
elif correct == 19 and G < 0.30:
    verdict, branch = ("HELD", "overall = 19/30 with G < 0.30 → underpowered zone; "
                       "no rerun, no larger-N rescue")
else:
    verdict, branch = ("KILL", "overall <= 18/30 with G < 0.30 → no identity readout "
                       "on bench 3; EXP111/EXP120 observations stand (Law #8); two-bench "
                       "CONTINUE reclassified as position-detector correlation (Law #11)")
log(f"VERDICT: {verdict}")
log(f"branch: {branch}")

result = {
    "experiment": "EXP122", "hypothesis": "H16/POSITION-CUE", "lane": "LOG-4653",
    "env": {"torch": torch.__version__,
            "transformers": __import__('transformers').__version__,
            "sklearn": __import__('sklearn').__version__,
            "numpy": np.__version__,
            "threads_set": thr_set, "threads_read": thr_read,
            "torch_seed": 0, "numpy_seed": 0, "split_seed": SEED},
    "backbone": {"snapshot": SNAP, "pin": WEIGHTS_PIN,
                 "pre_hash": pre, "post_hash": post, "dtheta0": pre == post == WEIGHTS_PIN},
    "bench3": {"pin": pin, "n": 60,
               "gates": {"design_time": {
                             "n": v["n"],
                             "cells": {f"{p}/{w}": c
                                       for (p, w), c in v["cells"].items()},
                             "pin": v["pin"]},
                         "G-C1": g1, "position_scramble": gp,
                         "G-C2": g2, "G-C3": g3},
               "reparse_x2_byte_identical": True},
    "extraction": {"site": f"hidden_states[{SITE}]", "final_token": True,
                   "dtype": "float32", "cpu_only": True, "n_passes": 60,
                   "input": "premise only (no question, no option list)"},
    "split": {"test_size": 0.5, "stratify": "f\"{phrasing}_{flipped}\"",
              "train_n": 30, "test_n": 30, "overlap": 0,
              "per_cell_test_counts": dict(sorted(cell_counts.items())),
              "N_F": NF, "N_T": NT,
              "train_ids": [ids[i] for i in tr], "test_ids": [ids[i] for i in te]},
    "head": {"spec": "LogisticRegression(penalty='l2', C=1.0, solver='lbfgs', "
                     "max_iter=1000, random_state=20260929)",
             "determinism_refit_byte_identical": True,
             "weight_hash": head_hash,
             "weight_norm": float(np.linalg.norm(clf.coef_)),
             "train_accuracy_sanity": train_acc},
    "artifact_hashes": artifact_hashes,
    "evaluation": {"correct": correct, "n": 30, "accuracy": acc,
                   "acc_flipped_False": accF, "acc_flipped_True": accT,
                   "G": G, "per_cell_descriptive": per_cell,
                   "p_one_sided_exact": p_one, "p_two_sided_exact": p_two,
                   "p_computed_by": "executor (math.comb)"},
    "verdict": verdict, "falsification_branch": branch,
    "wall_seconds": round(time.time() - t0, 1),
}
with open(os.path.join(OUT, "exp122_result.json"), "w") as f:
    json.dump(result, f, indent=2)
log("saved exp122_result.json (worksheet: all raw records above)")
log(f"wall {time.time() - t0:.1f}s; $0 CPU; no generation; no signed artifact modified")
