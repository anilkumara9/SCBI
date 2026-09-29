#!/usr/bin/env python3
"""EXP111 (H5/LFH-TD) execution — signed pre-reg EXP_PREREG_H5_LFHTD_2026-09-29.md.
Primary analysis only: archived EXP107 embeddings, zero backbone contact.
"""
import hashlib, json, os, sys
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

OUT = os.path.expanduser("~/workspace/SCBI/experiments/runs/EXP111_lfhtd/out")
os.makedirs(OUT, exist_ok=True)
NPZ = os.path.expanduser("~/workspace/SCBI/experiments/runs/EXP107_templatectrl/out/exp107_test_embeddings.npz")
PITEM = os.path.expanduser("~/workspace/SCBI/experiments/runs/EXP107_templatectrl/out/exp107_per_item.json")
SEED = 20260929
log_lines = []
def log(s):
    log_lines.append(s); print(s, flush=True)

log(f"ENV sklearn={__import__('sklearn').__version__} numpy={np.__version__}")

# --- 1. Artifact hash verification (pre-reg §3.2 pins) ---
with open(NPZ, "rb") as f:
    npz_bytes = f.read()
h_npz = hashlib.sha256(npz_bytes).hexdigest()
data = np.load(NPZ)
emb = data["embeddings"]; ids = data["ids"]
h_emb = hashlib.sha256(emb.tobytes()).hexdigest()
h_ids = hashlib.sha256(ids.tobytes()).hexdigest()
PIN_NPZ = "6cf4a8a726a2b6e4623f57d0287d95879866f77e789bcc3789fb693cf2af6a76"
PIN_EMB = "9b6e8afb091ba1edbb0311ba1d3414d34a65942c3fdecb4533b69720f2a99123"
PIN_IDS = "3669e102222719d66f61daca46ae1ac34e844e398ae433743a5b37bfc5075cb9"
log(f"hash npz: {h_npz} {'OK' if h_npz==PIN_NPZ else 'MISMATCH'}")
log(f"hash embeddings: {h_emb} {'OK' if h_emb==PIN_EMB else 'MISMATCH'}")
log(f"hash ids: {h_ids} {'OK' if h_ids==PIN_IDS else 'MISMATCH'}")
log(f"embeddings shape={emb.shape} dtype={emb.dtype}; ids shape={ids.shape}")
if not (h_npz==PIN_NPZ and h_emb==PIN_EMB and h_ids==PIN_IDS):
    log("RUN-INVALID: artifact hash mismatch — apparatus drift. HALTING."); sys.exit(2)

# --- 2. Per-item metadata join ---
with open(PITEM) as f:
    per_item = json.load(f)
ids_list = [str(x) for x in ids]
rec_by_id = {str(r["id"]): r for r in per_item}
assert len(rec_by_id) == len(per_item), "duplicate ids in per-item json"
missing = [i for i in ids_list if i not in rec_by_id]
assert not missing, f"ids missing from per-item json: {missing[:5]}"
y = np.array([int(rec_by_id[i]["y"]) for i in ids_list])
phrasing = [str(rec_by_id[i]["phrasing"]) for i in ids_list]
flipped = np.array([bool(rec_by_id[i]["flipped"]) for i in ids_list])
log(f"metadata joined: {len(ids_list)} items; y=1 count={int(y.sum())}")

# --- 3. Stratified 30/30 split (pinned: seed 20260929, key f"{{phrasing}}_{{flipped}}") ---
key = np.array([f"{p}_{f}" for p, f in zip(phrasing, flipped)])
idx = np.arange(len(ids_list))
tr, te = train_test_split(idx, test_size=0.5, random_state=SEED, stratify=key)
train_ids = [ids_list[i] for i in tr]; test_ids = [ids_list[i] for i in te]
overlap = set(train_ids) & set(test_ids)
log(f"train n={len(tr)}, test n={len(te)}, ID overlap={len(overlap)}")
if overlap:
    log("RUN-INVALID: train/test ID overlap. HALTING."); sys.exit(2)
from collections import Counter
test_cells = Counter(key[te]); train_cells = Counter(key[tr])
log(f"test per-cell counts: {dict(sorted(test_cells.items()))}")
log(f"train per-cell counts: {dict(sorted(train_cells.items()))}")
N_F = int((~flipped[te]).sum()); N_T = int(flipped[te].sum())
log(f"N_F (flipped=False test)={N_F}, N_T (flipped=True test)={N_T}")
assert len(tr)==30 and len(te)==30 and N_F==15 and N_T==15, "split counts off-pin"

# --- 4. Train head (pinned spec, Law #7: no tuning) ---
Xtr, ytr = emb[tr], y[tr]
Xte, yte = emb[te], y[te]
clf = LogisticRegression(penalty='l2', C=1.0, solver='lbfgs', max_iter=1000, random_state=SEED)
clf.fit(Xtr, ytr)
pred1 = clf.predict(Xte)
# determinism pass: re-fit from the same artifact, assert byte-identical predictions
clf2 = LogisticRegression(penalty='l2', C=1.0, solver='lbfgs', max_iter=1000, random_state=SEED)
clf2.fit(Xtr, ytr)
pred2 = clf2.predict(Xte)
det_ok = np.array_equal(pred1, pred2)
log(f"determinism pass: byte-identical predictions={det_ok}")
if not det_ok:
    log("RUN-INVALID: determinism re-fit mismatch. HALTING."); sys.exit(2)
h_w = hashlib.sha256(clf.coef_.tobytes() + clf.intercept_.tobytes()).hexdigest()
log(f"head weight hash: {h_w}")
log(f"head weight norm (L2 of coef): {float(np.linalg.norm(clf.coef_)):.6f}")
log(f"train accuracy (sanity): {float((clf.predict(Xtr)==ytr).mean()):.4f}")

# --- 5. Evaluation: overall accuracy + G signature ---
acc = float((pred1 == yte).mean())
correct = int((pred1 == yte).sum())
f_mask = ~flipped[te]; t_mask = flipped[te]
acc_F = float((pred1[f_mask] == yte[f_mask]).mean())
acc_T = float((pred1[t_mask] == yte[t_mask]).mean())
G = acc_F - acc_T
log(f"test accuracy: {correct}/30 = {acc:.4f}")
log(f"acc(flipped=False, N_F={N_F}): {acc_F:.4f}; acc(flipped=True, N_T={N_T}): {acc_T:.4f}")
log(f"G = {G:.4f} (threshold 0.30)")
# per-cell descriptives
for k in sorted(test_cells):
    m = (key[te] == k)
    log(f"  cell {k}: {(pred1[m]==yte[m]).mean():.4f} ({int((pred1[m]==yte[m]).sum())}/{int(m.sum())})")

# --- 6. Registered decision bars (verbatim) ---
if G >= 0.30:
    verdict = "KILL (template-detector signature G>=0.30; transfer reading dead)"
elif acc*30 >= 20:
    verdict = "CONTINUE (autonomous output-side transfer; re-licenses GPU head-training under decorrelated-bench discipline; secondary per-layer analysis licensed)"
elif correct == 19:
    verdict = "HELD (underpowered; no rescue)"
else:
    verdict = "KILL (no transfer on the decorrelated bench; output-side readout room retired as template-artifact-only)"
log(f"VERDICT: {verdict}")

# --- 7. Save ---
out = {
  "env": {"sklearn": __import__('sklearn').__version__, "numpy": np.__version__},
  "hashes": {"npz": h_npz, "embeddings": h_emb, "ids": h_ids, "head_weights": h_w},
  "split": {"seed": SEED, "train_ids": train_ids, "test_ids": test_ids,
            "test_cells": dict(test_cells), "train_cells": dict(train_cells),
            "N_F": N_F, "N_T": N_T, "disjoint": True},
  "head": {"spec": "LogisticRegression(penalty='l2', C=1.0, solver='lbfgs', max_iter=1000, random_state=20260929)",
           "weight_l2_norm": float(np.linalg.norm(clf.coef_)),
           "determinism_byte_identical": True},
  "results": {"test_correct": correct, "test_n": 30, "accuracy": acc,
              "acc_flipped_False": acc_F, "acc_flipped_True": acc_T, "G": G},
  "verdict": verdict,
}
with open(os.path.join(OUT, "exp111_result.json"), "w") as f:
    json.dump(out, f, indent=2)
with open(os.path.join(OUT, "exp111_execution_log.txt"), "w") as f:
    f.write("\n".join(log_lines) + "\n")
np.save(os.path.join(OUT, "exp111_test_predictions.npy"), pred1)
log("saved exp111_result.json, exp111_execution_log.txt, exp111_test_predictions.npy")
