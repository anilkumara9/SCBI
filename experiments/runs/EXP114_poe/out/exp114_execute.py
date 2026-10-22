#!/usr/bin/env python3
"""EXP114 (H8/POE: positional-order ensembling) execution lane. LOG-4591 pre-assigned.
Executes EXACTLY per ~/workspace/SCBI/research/prereg/EXP_PREREG_H8_POE_2026-09-29.md.
$0 CPU. Zero generation. No training. Read-only on all signed artifacts.

Falsification-tree order is mirrored in code; the metric is read only AFTER
all gates pass (Law #9). Any gate failure -> RUN-INVALID/HALT, no metric.
"""
import json, hashlib, sys, os, time, random
import numpy as np
import torch

# ---------------- Law #13 pins ----------------
SNAP = os.path.expanduser("~/workspace/.exp086_weights/pythia-410m")
WEIGHTS_PIN = "ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed"  # LOG-331
NPZ_PIN = "6cf4a8a726a2b6e4623f57d0287d95879866f77e789bcc3789fb693cf2af6a76"
EMB_BYTES_PIN = "9b6e8afb091ba1edbb0311ba1d3414d34a65942c3fdecb4533b69720f2a99123"
IDS_BYTES_PIN = "3669e102222719d66f61daca46ae1ac34e844e398ae433743a5b37bfc5075cb9"
BENCH_PIN = "e91b302f41f641c74e56957e526efcd4866bac62d134e157defe0a4cdd49e4f5"
NPZ_PATH = os.path.expanduser("~/workspace/SCBI/experiments/runs/EXP107_templatectrl/out/exp107_test_embeddings.npz")
BUILDER_DIR = os.path.expanduser("~/workspace/SCBI/experiments/runs/EXP107_templatectrl")
ORDER_SEED = 20260929
K = 5

OUT = os.path.expanduser("~/workspace/SCBI/experiments/runs/EXP114_poe/out")
os.makedirs(OUT, exist_ok=True)

def log(msg):
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)

def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()

def state_dict_hash(model):
    """Canonical LOG-331 method: sha256 over sorted state_dict keys, float32 bytes."""
    sha = hashlib.sha256()
    sd = model.state_dict()
    for k in sorted(sd.keys()):
        sha.update(np.asarray(sd[k].detach().cpu(), dtype=np.float32).tobytes())
    return sha.hexdigest()

# ---------------- environment manifest ----------------
torch.manual_seed(0); np.random.seed(0)
torch.set_num_threads(2)
import transformers
manifest = {
    "torch": torch.__version__, "transformers": transformers.__version__,
    "numpy": np.__version__,
    "snapshot": SNAP, "order_seed": ORDER_SEED, "K": K,
    "torch_num_threads_set": 2, "torch_num_threads_readback": torch.get_num_threads(),
    "seeds": {"torch": 0, "numpy": 0},
    "device": "cpu", "dtype": "float32",
}
log("ENV: " + json.dumps(manifest))

# ---------------- 1. archive pins (before any use) ----------------
log("checking npz archive pins...")
with open(NPZ_PATH, "rb") as f:
    npz_bytes = f.read()
if sha256_bytes(npz_bytes) != NPZ_PIN:
    log("RUN-INVALID: npz file pin mismatch")
    sys.exit(41)
d = np.load(NPZ_PATH, allow_pickle=True)
emb = np.ascontiguousarray(d["embeddings"]); ids = np.ascontiguousarray(d["ids"])
if sha256_bytes(emb.tobytes()) != EMB_BYTES_PIN:
    log("RUN-INVALID: embeddings-bytes pin mismatch")
    sys.exit(41)
if sha256_bytes(ids.tobytes()) != IDS_BYTES_PIN:
    log("RUN-INVALID: ids-bytes pin mismatch")
    sys.exit(41)
if emb.shape != (60, 1024) or emb.dtype != np.float32:
    log(f"RUN-INVALID: bad emb array {emb.shape} {emb.dtype}")
    sys.exit(41)
log("npz pins OK: embeddings (60, 1024) float32, ids (60,)")

# ---------------- 2. bench rebuild + provenance pin ----------------
sys.path.insert(0, BUILDER_DIR)
import build_exp107_bench as b
bench = b.build_bench()
if len(bench) != 60:
    log(f"RUN-INVALID: bench len {len(bench)} != 60")
    sys.exit(41)
canon = json.dumps(bench, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
bhash = sha256_bytes(canon.encode("utf-8"))
if bhash != BENCH_PIN:
    # Pre-reg tree labels this HALT; the CEO launch lane instruction (LOG-4590)
    # directs RUN-INVALID. Both mean no metric exists; recorded as RUN-INVALID.
    log("RUN-INVALID: bench provenance pin MISMATCH (lane instruction override of HALT label)")
    sys.exit(42)
log("bench pin OK: 60 items, canonical-JSON sha256 matches e91b302f...4f5")
bench_ids = np.array([it["id"] for it in bench])
if not (bench_ids == ids).all():
    log("RUN-INVALID: bench ids vs npz ids mismatch")
    sys.exit(41)
log("bench ids == npz ids: 60/60")
QS = b.QUESTION_SUFFIX
assert QS == " Question: Who is higher in rank? Answer:", "QUESTION_SUFFIX drift"
log("QUESTION_SUFFIX byte-exact: OK")

# ---------------- 3. backbone load + pre-forwards hash ----------------
from transformers import AutoTokenizer, AutoModelForCausalLM
tok = AutoTokenizer.from_pretrained(SNAP, local_files_only=True)
model = AutoModelForCausalLM.from_pretrained(
    SNAP, local_files_only=True, device_map="cpu", torch_dtype=torch.float32)
model.eval()
h_pre = state_dict_hash(model)
log(f"backbone hash BEFORE forwards: {h_pre}")
if h_pre != WEIGHTS_PIN:
    log("RUN-INVALID: backbone hash mismatch before forwards (Law #6). No metric exists.")
    sys.exit(42)
log("backbone pin OK (LOG-331)")

# ---------------- 4. single-token BPE assertion (ALL 120 entity texts) ----------------
items = []
for it in bench:
    E1, E2 = it["tuple"][0], it["tuple"][-1]
    t1_ids = tok.encode(" " + E1); t2_ids = tok.encode(" " + E2)
    if not (len(t1_ids) == 1 and len(t2_ids) == 1):
        log(f"RUN-INVALID: single-token BPE assertion failed on item {it['id']}: "
            f"' {E1}' -> {t1_ids}, ' {E2}' -> {t2_ids}. Items NOT silently dropped.")
        sys.exit(43)
    items.append({"id": it["id"], "premise": it["premise"], "E1": E1, "E2": E2,
                  "t1": t1_ids[0], "t2": t2_ids[0],
                  "phrasing": it["phrasing"], "flipped": it["flipped"],
                  "y": 1 if it["phrasing"] == "A-first" else 0})
log("single-token BPE assertion: 120/120 entity texts exactly one token")

# ---------------- 5. order generation (K=5 i.i.d. bits, pinned RNG) ----------------
rng = random.Random(ORDER_SEED)
for rec in items:  # canonical bench order, sequential draws
    rec["orders"] = [rng.randint(0, 1) for _ in range(K)]
degenerate = sum(1 for rec in items if sum(rec["orders"]) in (0, K))
log(f"order patterns drawn (seed {ORDER_SEED}); degenerate 5-0 compositions: {degenerate}/60")

def build_prompt(rec, o):
    first, second = (rec["E1"], rec["E2"]) if o == 0 else (rec["E2"], rec["E1"])
    return rec["premise"] + " Options: " + first + ", " + second + "." + QS

# ---------------- 6. 360 forwards (300 ensemble + 60 baseline), zero generation ----------------
def readout_logits(prompt):
    inp = tok(prompt, return_tensors="pt")
    with torch.no_grad():
        out = model(**inp)
    lg = out.logits[0, -1, :].detach().cpu().to(torch.float64)
    return float(lg[rec_t1]), float(lg[rec_t2])

results = []
n_fwd = 0
t0 = time.time()
for idx, rec in enumerate(items):
    rec_t1, rec_t2 = rec["t1"], rec["t2"]
    order_logits = []
    for o in rec["orders"]:
        l1, l2 = readout_logits(build_prompt(rec, o))
        order_logits.append((o, l1, l2))
        n_fwd += 1
    l1b, l2b = readout_logits(build_prompt(rec, 0))
    n_fwd += 1
    # ensemble decision: argmax over mean logits, tie-break -> E2
    m1 = sum(p[1] for p in order_logits) / K
    m2 = sum(p[2] for p in order_logits) / K
    if m1 == m2:
        pred_ens = rec["E2"]
    elif m1 > m2:
        pred_ens = rec["E1"]
    else:
        pred_ens = rec["E2"]
    if l1b == l2b:
        pred_base = rec["E2"]
    elif l1b > l2b:
        pred_base = rec["E1"]
    else:
        pred_base = rec["E2"]
    pred_ens_y = 1 if pred_ens == rec["E1"] else 0
    pred_base_y = 1 if pred_base == rec["E1"] else 0
    results.append({
        "id": rec["id"], "y": rec["y"], "phrasing": rec["phrasing"], "flipped": rec["flipped"],
        "orders": rec["orders"],
        "order_logits": [[o, l1, l2] for o, l1, l2 in order_logits],
        "baseline_logits": [l1b, l2b],
        "pred_ens": pred_ens, "pred_base": pred_base,
        "pred_ens_y": pred_ens_y, "pred_base_y": pred_base_y,
        "correct_ens": 1 if pred_ens_y == rec["y"] else 0,
        "correct_base": 1 if pred_base_y == rec["y"] else 0,
    })
    if (idx + 1) % 15 == 0:
        log(f"forwards progress: {n_fwd}/360 ({idx+1}/60 items, {time.time()-t0:.0f}s elapsed)")
log(f"all {n_fwd} forwards complete in {time.time()-t0:.0f}s (zero generation)")

# ---------------- 7. backbone pin re-check (after last forward) ----------------
h_post = state_dict_hash(model)
log(f"backbone hash AFTER forwards: {h_post}")
if h_post != WEIGHTS_PIN:
    log("RUN-INVALID: backbone hash drifted during forwards. No metric exists.")
    sys.exit(42)
log("backbone pin re-check OK (Δθ=0)")

# ---------------- 8. paired McNemar (metric read only now, Law #9) ----------------
b = sum(1 for r in results if r["correct_base"] == 0 and r["correct_ens"] == 1)
c = sum(1 for r in results if r["correct_base"] == 1 and r["correct_ens"] == 0)
n = b + c
acc_ens = sum(r["correct_ens"] for r in results) / 60
acc_base = sum(r["correct_base"] for r in results) / 60
if n == 0:
    p_val = None
    verdict = "KILL"
    reason = "b=c=0 degenerate table: ensemble and baseline agree on all 60 items; net=0 -> KILL (registered)"
else:
    from math import comb
    p_val = sum(comb(n, k) for k in range(b, n + 1)) / 2**n
    if p_val <= 0.05 and b > c:
        verdict = "CONTINUE"
        reason = f"paired exact McNemar one-sided p={p_val:.6g} <= 0.05, b={b} > c={c} -> CONTINUE"
    elif (b - c) > 0 and p_val > 0.05:
        verdict = "HELD"
        reason = f"net (b-c)={b-c} > 0 but p={p_val:.6g} > 0.05 -> HELD (underpowered)"
    else:
        verdict = "KILL"
        reason = f"net (b-c)={b-c} <= 0 -> KILL"
log(f"McNemar: b={b} c={c} n={n} p={p_val}")
log(f"acc_ens={acc_ens:.4f} acc_base={acc_base:.4f}")
log(f"VERDICT: {verdict} — {reason}")

# per-cell descriptive (no decision branch reads these)
from collections import defaultdict
cells = defaultdict(list)
for r in results:
    cells[(r["phrasing"], "flipped" if r["flipped"] else "original")].append(r)
cell_desc = {}
for k, rs in cells.items():
    cell_desc[f"{k[0]}/{k[1]}"] = {
        "n": len(rs),
        "acc_ens": sum(r["correct_ens"] for r in rs) / len(rs),
        "acc_base": sum(r["correct_base"] for r in rs) / len(rs),
    }

out_data = {
    "manifest": manifest,
    "pins": {"npz": NPZ_PIN, "emb_bytes": EMB_BYTES_PIN, "ids_bytes": IDS_BYTES_PIN,
             "bench": BENCH_PIN, "backbone_pre": h_pre, "backbone_post": h_post},
    "order_seed": ORDER_SEED, "K": K,
    "degenerate_5_0_compositions": degenerate,
    "mcnemar": {"b": b, "c": c, "n": n, "p_one_sided": p_val,
                "acc_ens": acc_ens, "acc_base": acc_base},
    "per_cell_descriptive": cell_desc,
    "verdict": verdict, "verdict_reason": reason,
    "per_item": results,
}
with open(os.path.join(OUT, "exp114_result.json"), "w") as f:
    json.dump(out_data, f, indent=1)
log("wrote exp114_result.json")

# ---------------- worksheet ----------------
worksheet = {
    "experiment": "EXP114", "hypothesis": "H8/POE", "log": "LOG-4591",
    "manifest": manifest,
    "order_patterns": {r["id"]: r["orders"] for r in results},
    "pins": out_data["pins"],
    "verdict": verdict,
}
with open(os.path.join(OUT, "exp114_worksheet.json"), "w") as f:
    json.dump(worksheet, f, indent=1)
log("wrote exp114_worksheet.json")
log("DONE")
