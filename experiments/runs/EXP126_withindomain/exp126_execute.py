#!/usr/bin/env python3
"""EXP126 (H23/WITHIN-DOMAIN) executor — Law-#9 ordered, Law-#14 SIGN LOG-4686.
Signed protocol: EXP_PREREG_H23_WITHINDOMAIN_2026-09-29.md (no fixes).
Construction certificate: PASS (LOG-4687). Bench 5 pin:
444e40260b4c71c512db72db2c5d2555b31ffbbd8db2eedcf8a3a46fddbb0e8a
$0 CPU. Delta-theta = 0 (LOG-331 pin before/after). Metric read ONLY after all guards pass.
"""
import hashlib, json, math, os, sys, time, warnings

import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

WEIGHTS_DIR = os.path.expanduser("~/workspace/.exp086_weights/pythia-410m")
WEIGHTS_PIN = "ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed"  # LOG-331
PROTOCOL_PATH = os.path.expanduser("~/workspace/SCBI/research/prereg/EXP_PREREG_H23_WITHINDOMAIN_2026-09-29.md")
BENCH_PIN = "444e40260b4c71c512db72db2c5d2555b31ffbbd8db2eedcf8a3a46fddbb0e8a"
BENCH_PATH = os.path.expanduser("~/workspace/SCBI/experiments/runs/EXP126_withindomain/out/exp126_bench5.json")
SITE = 20
SEED = 20260929
RUN_DIR = os.path.expanduser("~/workspace/SCBI/experiments/runs/EXP126_withindomain")
OUT = os.path.join(RUN_DIR, "out")
os.makedirs(OUT, exist_ok=True)
LOGF = os.path.join(OUT, "exp126_console.log")

def log(msg):
    line = "[%s] %s" % (time.strftime("%H:%M:%S"), msg)
    print(line, flush=True)
    with open(LOGF, "a") as f:
        f.write(line + "\n")

def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()

def backbone_pin(model):
    """Canonical LOG-331 method: sha256 over sorted state_dict keys, float32 bytes."""
    sha = hashlib.sha256()
    sd = model.state_dict()
    for k in sorted(sd.keys()):
        sha.update(np.asarray(sd[k].detach().cpu(), dtype=np.float32).tobytes())
    return sha.hexdigest()

def binom_sf_exact(k, n):
    """Exact one-sided P(X >= k | n, 0.5) via integer arithmetic."""
    num = sum(math.comb(n, i) for i in range(k, n + 1))
    return num / float(2 ** n)

def runinvalid(reason):
    log("RUN-INVALID: %s" % reason)
    ws = {"verdict": "RUN-INVALID", "reason": reason}
    with open(os.path.join(OUT, "exp126_worksheet.json"), "w") as f:
        json.dump(ws, f, indent=1)
    sys.exit(3)

# ============ TREE: protocol + bench provenance pins (before any model contact) ============
log("EXP126 (H23/WITHIN-DOMAIN) execution — Law #9 ordered")
proto_hash = sha256_file(PROTOCOL_PATH)
log("protocol sha256: %s" % proto_hash)
bench_hash = sha256_file(BENCH_PATH)
log("bench sha256:    %s" % bench_hash)
if bench_hash != BENCH_PIN:
    runinvalid("bench hash mismatch vs LOG-4679 certificate pin")

with open(BENCH_PATH) as f:
    bench = json.load(f)
items = bench if isinstance(bench, list) else bench["items"]
log("bench items: %d" % len(items))
if len(items) != 60:
    runinvalid("len(bench) != 60")

# schema + structure spot-checks (certified, re-verified at execution)
ids = [it["id"] for it in items]
assert len(set(ids)) == 60, "id collision"
assert all(i.startswith("expb5_") for i in ids), "id namespace"
labels = [int(it["y"]) for it in items]
assert sum(labels) == 30, "label balance"
phrases = [it["phrasing"] for it in items]
assert phrases.count("target-first") == 30 and phrases.count("target-last") == 30, "phrasing balance"
flips = [bool(it["flipped"]) for it in items]
assert sum(flips) == 30, "flip balance"
assert all(it["y"] == (1 if it["tuple"][0] in
    {"Cat","Dog","Bear","Wolf","Fox"} else 0) for it in items), "law-7 pin"
S1 = {"Cat", "Dog", "Bear", "Wolf", "Fox"}
S2 = {"Lion", "Tiger", "Horse", "Cow", "Pig"}
ALL14 = S1 | S2 | {"Rat", "Bat", "Bird", "Fish"}
cells = {}
for it in items:
    cells.setdefault((it["phrasing"], it["flipped"]), []).append(it)
assert all(len(v) == 15 for v in cells.values()), "four 15-item cells"
premises = [it["premise"] for it in items]
assert all(it["prompt"] == it["premise"] + " Question: Who is higher in rank? Answer:"
            for it in items), "extraction contract"
log("bench schema checks: ids 60/60 unique, labels 30/30, phrasing 30/30, flips 30/30, law-7 60/60")

# ============ TREE: backbone pin (pre) ============
torch.manual_seed(0); np.random.seed(0)
torch.set_num_threads(2)
threads = torch.get_num_threads()
tok = AutoTokenizer.from_pretrained(WEIGHTS_DIR, local_files_only=True,
                                      trust_remote_code=False)
# NOTE: AutoModelForCausalLM is REQUIRED: the LOG-331 pin was computed on the
# full causal-LM state dict (includes embed_out.weight); AutoModel's state dict
# excludes it and produces a different hash.
model = AutoModelForCausalLM.from_pretrained(WEIGHTS_DIR, local_files_only=True,
                                             trust_remote_code=False,
                                             device_map="cpu",
                                             torch_dtype=torch.float32)
model.eval()
pin_pre = backbone_pin(model)
log("backbone pin (pre): %s" % pin_pre)
if pin_pre != WEIGHTS_PIN:
    runinvalid("backbone pin mismatch vs LOG-331 (pre)")
log("backbone pin OK (LOG-331). Delta-theta guard armed.")

# ============ TREE: 60 fresh layer-20 premise extractions ============
log("running 60 premise layer-20 extractions...")
embs = []
with torch.no_grad():
    for rec in items:
        inp = tok(rec["premise"], return_tensors="pt")
        out = model(**inp, output_hidden_states=True)
        h = out.hidden_states[SITE][0, -1, :].detach().cpu().to(torch.float32).numpy()
        embs.append(h)
X = np.stack(embs).astype(np.float32)
log("extractions complete: X=%s" % (X.shape,))

pin_post = backbone_pin(model)
log("backbone pin (post): %s" % pin_post)
if pin_post != WEIGHTS_PIN:
    runinvalid("backbone pin drift vs LOG-331 (post) — Δθ≠0")
log("Δθ=0 confirmed (pins identical, LOG-331)")

# block-off (a): bench hash recorded before extraction == hash after
bench_hash_after = sha256_file(BENCH_PATH)
if bench_hash_after != BENCH_PIN:
    runinvalid("bench mutated during extraction")
log("bench hash stable across extraction")

# ============ artifact-existence gate: persist raw records BEFORE verdict ============
head_X = X.copy()
train_idx, test_idx = train_test_split(
    np.arange(60), test_size=0.5, random_state=SEED,
    stratify=np.array([f"{p}_{f}" for p, f in zip(phrases, flips)]))
train_idx = np.sort(train_idx); test_idx = np.sort(test_idx)
overlap = set(train_idx.tolist()) & set(test_idx.tolist())
if overlap:
    runinvalid("train/test ID overlap (Law #7)")
assert len(train_idx) == 30 and len(test_idx) == 30
train_ids = [ids[i] for i in train_idx]; test_ids = [ids[i] for i in test_idx]
y_all = np.array(labels)
ytr, yte = y_all[train_idx], y_all[test_idx]
N_F = int(sum(1 for i in test_idx if not flips[i]))
N_T = int(sum(1 for i in test_idx if flips[i]))
log("split: train=30 test=30 N_F=%d N_T=%d; disjoint OK" % (N_F, N_T))
if not (N_F == 15 and N_T == 15):
    runinvalid("split cell encoding mismatch (expected N_F=N_T=15)")

with warnings.catch_warnings():
    warnings.simplefilter("always")
    head = LogisticRegression(penalty="l2", C=1.0, solver="lbfgs",
                              max_iter=1000, random_state=SEED)
    head.fit(X[train_idx], ytr)
convg = getattr(head, "n_iter_", None)
log("head fit done (lbfgs n_iter=%s)" % (list(convg) if convg is not None else None))

# determinism re-fit pass (block-off (c))
head2 = LogisticRegression(penalty="l2", C=1.0, solver="lbfgs",
                           max_iter=1000, random_state=SEED)
head2.fit(X[train_idx], ytr)
pred1 = head.predict(X[test_idx]); pred2 = head2.predict(X[test_idx])
if not np.array_equal(pred1, pred2):
    runinvalid("determinism re-fit predictions differ")
log("determinism re-fit: byte-identical predictions OK")

# persist artifacts pre-verdict
emb_npz = os.path.join(OUT, "exp126_embeddings.npz")
np.savez(emb_npz, embeddings=X, ids=np.array(ids, dtype=object))
head_w = os.path.join(OUT, "exp126_head_weights.npz")
np.savez(head_w, coef=head.coef_.astype(np.float64),
         intercept=head.intercept_.astype(np.float64))
ids_json = os.path.join(OUT, "exp126_split_ids.json")
with open(ids_json, "w") as f:
    json.dump({"train_ids": train_ids, "test_ids": test_ids,
               "N_F": N_F, "N_T": N_T, "seed": SEED}, f, indent=1)
hashes = {k: sha256_file(p) for k, p in
          [("embeddings_npz", emb_npz), ("head_weights_npz", head_w),
           ("split_ids", ids_json), ("bench_json", BENCH_PATH)]}
for k, v in hashes.items():
    log("pinned (pre-verdict) %s: %s" % (k, v))

# ============ TREE: guards passed → read the metric (Law #9) ============
pred = pred1
acc = float(np.mean(pred == yte))
acc_F = float(np.mean(pred[[i for i, t in enumerate(test_idx) if not flips[t]]] ==
                        yte[[i for i, t in enumerate(test_idx) if not flips[t]]]))
acc_T = float(np.mean(pred[[i for i, t in enumerate(test_idx) if flips[t]]] ==
                        yte[[i for i, t in enumerate(test_idx) if flips[t]]]))
G = acc_F - acc_T
k = int(np.sum(pred == yte))
p_one_sided = binom_sf_exact(k, 30)
log("METRIC: test acc %d/30 = %.4f, acc(F)=%.4f, acc(T)=%.4f, G=%.4f, P(X>=%d|30,0.5)=%.10f"
    % (k, acc, acc_F, acc_T, G, k, p_one_sided))
train_acc = float(head.score(X[train_idx], ytr))
w_norm = float(np.linalg.norm(head.coef_))
log("descriptive: train acc=%.4f, ||w||=%.4f" % (train_acc, w_norm))
per_cell = {}
for key in sorted(cells.keys()):
    cell_test = [i for i, t in enumerate(test_idx) if (phrases[t], flips[t]) == key]
    per_cell[str(key)] = "%d/%d" % (int(np.sum(pred[cell_test] == yte[cell_test])), len(cell_test))
log("per-cell test acc: %s" % per_cell)

# ============ verdict (registered bars, Law #4) ============
if G >= 0.30:
    verdict, basis = "KILL", "G>=0.30 (word-family detector signature; takes precedence)"
elif k >= 20 and G < 0.30:
    verdict, basis = "CONTINUE", "acc>=20/30 AND G<0.30"
elif k == 19 and G < 0.30:
    verdict, basis = "HELD", "acc=19/30 with G<0.30 (underpowered; no rescue)"
else:
    verdict, basis = "KILL", "acc<=18/30 with G<0.30 (no identity readout on bench 5)"
log("VERDICT: %s — %s" % (verdict, basis))

ws = {
    "experiment": "EXP126", "hypothesis": "H23",
    "protocol": PROTOCOL_PATH, "protocol_sha256": proto_hash,
    "bench_sha256": BENCH_PIN, "certificate": "PASS LOG-4687",
    "backbone_pin_pre": pin_pre, "backbone_pin_post": pin_post,
    "delta_theta": 0, "site": "layer-20 final token",
    "env": {"torch": torch.__version__, "threads": threads,
            "seeds": {"torch": 0, "numpy": 0}},
    "split": {"seed": SEED, "train_n": 30, "test_n": 30, "N_F": N_F, "N_T": N_T},
    "head": {"penalty": "l2", "C": 1.0, "solver": "lbfgs",
             "max_iter": 1000, "random_state": SEED,
             "n_iter": (list(convg) if convg is not None else None),
             "weight_norm": w_norm, "train_acc": train_acc},
    "metric": {"test_correct": k, "test_n": 30, "accuracy": acc,
               "acc_flipped_false": acc_F, "acc_flipped_true": acc_T,
               "G": G, "one_sided_p_ge": p_one_sided,
               "per_cell_test": per_cell},
    "bars": {"CONTINUE": "acc>=20/30 AND G<0.30",
             "KILL": "G>=0.30 OR acc<=18/30",
             "HELD": "acc=19/30 with G<0.30"},
    "artifacts": hashes,
    "verdict": verdict, "verdict_basis": basis,
}
with open(os.path.join(OUT, "exp126_worksheet.json"), "w") as f:
    json.dump(ws, f, indent=1)
ws_hash = sha256_file(os.path.join(OUT, "exp126_worksheet.json"))
log("worksheet written, sha256: %s" % ws_hash)
log("DONE")
