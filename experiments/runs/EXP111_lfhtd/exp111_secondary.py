#!/usr/bin/env python3
"""EXP111 secondary (H5 §6): per-layer trained-head transfer search, layers 4/8/12/16.
DESCRIPTIVE-ONLY, licenses no verdict. Same bench items by ID, same seeds/bars as primary.
Pre-reg environment pin: torch==2.14.0+cpu, transformers==5.17.0, threads set+read-back.
Backbone-contact discipline: LOG-331 pin verified before AND after extraction (Δθ=0).
"""
import hashlib, json, os, sys
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

OUT = os.path.expanduser("~/workspace/SCBI/experiments/runs/EXP111_lfhtd/out")
os.makedirs(OUT, exist_ok=True)
LOGF = open(os.path.join(OUT, "exp111_secondary_log.txt"), "w")
def log(s):
    print(s, flush=True); LOGF.write(s + "\n"); LOGF.flush()

SNAP = os.path.expanduser("~/workspace/.exp086_weights/pythia-410m")
WEIGHTS_PIN = "ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed"
SEED = 20260929
LAYERS = [4, 8, 12, 16]

log(f"ENV torch={torch.__version__} transformers={__import__('transformers').__version__} "
    f"sklearn={__import__('sklearn').__version__} numpy={np.__version__}")
torch.set_num_threads(2)
thr_set, thr_read = 2, torch.get_num_threads()
log(f"threads set={thr_set} read_back={thr_read}")
assert thr_read == 2, "thread count not honoured"

def state_dict_hash(model):
    sha = hashlib.sha256()
    for k in sorted(model.state_dict().keys()):
        sha.update(np.asarray(model.state_dict()[k].detach().cpu(), dtype=np.float32).tobytes())
    return sha.hexdigest()

log("loading tokenizer + frozen model...")
tokenizer = AutoTokenizer.from_pretrained(SNAP, local_files_only=True)
model = AutoModelForCausalLM.from_pretrained(SNAP, local_files_only=True,
                                             torch_dtype=torch.float32)
model.eval(); model.requires_grad_(False)
pre = state_dict_hash(model)
log(f"G1 pre hash: {pre} match={pre == WEIGHTS_PIN}")
if pre != WEIGHTS_PIN:
    log("RUN-INVALID: backbone hash mismatch (Law #6)"); sys.exit(43)

# Rebuild the exact EXP107 bench; extraction input = premise (state_text_of(prompt)).
sys.path.insert(0, os.path.expanduser("~/workspace/SCBI/experiments/runs/EXP107_templatectrl"))
from build_exp107_bench import build_bench, verify_cells
bench = build_bench()
v = verify_cells(bench)
log(f"bench verified: n={v['n']} pin={v['pin']}")
prem_by_id = {b["id"]: b["prompt"][:b["prompt"].index(" Question:")] for b in bench}
meta_by_id = {b["id"]: (b["phrasing"], b["flipped"]) for b in bench}
ids = [str(x) for x in np.load(os.path.expanduser(
    "~/workspace/SCBI/experiments/runs/EXP107_templatectrl/out/exp107_test_embeddings.npz"))["ids"]]
assert set(ids) == set(prem_by_id) and len(ids) == 60, "bench/np ID mismatch"
per_item = json.load(open(os.path.expanduser(
    "~/workspace/SCBI/experiments/runs/EXP107_templatectrl/out/exp107_per_item.json")))
rec_by_id = {str(r["id"]): r for r in per_item}
y = np.array([int(rec_by_id[i]["y"]) for i in ids])
texts = [prem_by_id[i] for i in ids]
key = np.array([f"{rec_by_id[i]['phrasing']}_{rec_by_id[i]['flipped']}" for i in ids])
flipped = np.array([bool(rec_by_id[i]["flipped"]) for i in ids])
idx = np.arange(60)
tr, te = train_test_split(idx, test_size=0.5, random_state=SEED, stratify=key)
ov = set(ids[i] for i in tr) & set(ids[i] for i in te)
assert not ov, "split overlap"
f_mask = ~flipped[te]; t_mask = flipped[te]

def extract(texts, site):
    embs = np.zeros((len(texts), model.config.hidden_size), dtype=np.float32)
    with torch.no_grad():
        for i, t in enumerate(texts):
            tid = torch.tensor([tokenizer.encode(t, add_special_tokens=False)], dtype=torch.long)
            out = model(tid, output_hidden_states=True)
            embs[i, :] = out.hidden_states[site][0, -1, :].detach().cpu().to(torch.float32).numpy()
    return embs

res = {}
for site in LAYERS:
    log(f"extracting layer {site} (60 passes)...")
    E = extract(texts, site)
    assert E.shape == (60, 1024) and E.dtype == np.float32 and np.isfinite(E).all()
    Xtr, ytr, Xte, yte = E[tr], y[tr], E[te], y[te]
    clf = LogisticRegression(penalty="l2", C=1.0, solver="lbfgs",
                             max_iter=1000, random_state=SEED)
    clf.fit(Xtr, ytr)
    pred = clf.predict(Xte)
    acc = float((pred == yte).mean())
    accF = float((pred[f_mask] == yte[f_mask]).mean())
    accT = float((pred[t_mask] == yte[t_mask]).mean())
    G = accF - accT
    res[site] = {"accuracy": acc, "correct": int((pred == yte).sum()), "n": 30,
                 "acc_flipped_False": accF, "acc_flipped_True": accT, "G": G}
    log(f"  layer {site}: {res[site]['correct']}/30 = {acc:.4f}, G={G:.4f} (DESCRIPTIVE-ONLY)")

post = state_dict_hash(model)
log(f"G1 post hash: {post} match={post == WEIGHTS_PIN} (Δθ=0)")
if post != WEIGHTS_PIN:
    log("RUN-INVALID: post-extraction backbone drift"); sys.exit(44)

payload = {
  "env": {"torch": torch.__version__, "transformers": __import__('transformers').__version__,
          "sklearn": __import__('sklearn').__version__, "numpy": np.__version__,
          "threads_set": thr_set, "threads_read": thr_read, "seed": SEED},
  "backbone": {"pre_hash": pre, "post_hash": post, "pin": WEIGHTS_PIN, "dtheta0": True},
  "bench_pin": v["pin"], "layers": res,
  "note": "DESCRIPTIVE-ONLY — licenses no verdict (pre-reg §6).",
}
with open(os.path.join(OUT, "exp111_secondary_result.json"), "w") as f:
    json.dump(payload, f, indent=2)
log("saved exp111_secondary_result.json")
