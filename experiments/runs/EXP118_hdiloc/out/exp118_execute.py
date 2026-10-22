#!/usr/bin/env python3
"""EXP118 (H13/HDI-LOC) execution lane. LOG-4619 pre-assigned.
Executes EXACTLY per ~/workspace/SCBI/research/prereg/EXP_PREREG_H13_HDILOC_2026-09-29.md
(independent Law #14 review LOG-4617 SIGN-WITH-FIXES; four fixes byte-verified LOG-4618).
$0 CPU. No generation. No training. Read-only on all signed artifacts.

Falsification-tree order is mirrored in code; the metric is read only AFTER
all guards/pins pass (Law #9). Any gate failure -> RUN-INVALID/HALT, no metric.
"""
import json, hashlib, sys, os, time
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
EXP112_PER_ITEM = os.path.expanduser("~/workspace/SCBI/experiments/runs/EXP112_hdildr/out/exp112_per_item.json")
EARLY_SITES = list(range(0, 9))     # hidden_states indices 0..8
LATE_SITES = list(range(16, 25))    # hidden_states indices 16..24 (24 = final layer output)
SITES = EARLY_SITES + LATE_SITES
SEED = 0
FID_PIN = (41, 60)  # pre-run consistency pin: archived readout fidelity exactly 41/60

OUT = os.path.expanduser("~/workspace/SCBI/experiments/runs/EXP118_hdiloc/out")
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
torch.manual_seed(SEED); np.random.seed(SEED)
torch.set_num_threads(2)
import transformers, sklearn
manifest = {
    "torch": torch.__version__, "transformers": transformers.__version__,
    "numpy": np.__version__, "sklearn": sklearn.__version__,
    "snapshot": SNAP,
    "layer_sites": {"early": EARLY_SITES, "late": LATE_SITES},
    "torch_num_threads_set": 2, "torch_num_threads_readback": torch.get_num_threads(),
    "seeds": {"torch": SEED, "numpy": SEED},
    "device": "cpu", "dtype": "float32",
}
log("ENV: " + json.dumps(manifest))

# ---------------- 1. archive pins (before any use) ----------------
log("checking npz archive pins...")
with open(NPZ_PATH, "rb") as f:
    npz_bytes = f.read()
assert sha256_bytes(npz_bytes) == NPZ_PIN, f"npz pin MISMATCH: {sha256_bytes(npz_bytes)}"
d = np.load(NPZ_PATH, allow_pickle=True)
emb = np.ascontiguousarray(d["embeddings"]); ids = np.ascontiguousarray(d["ids"])
assert sha256_bytes(emb.tobytes()) == EMB_BYTES_PIN, "embeddings-bytes pin MISMATCH"
assert sha256_bytes(ids.tobytes()) == IDS_BYTES_PIN, "ids-bytes pin MISMATCH"
log(f"npz pins OK: embeddings {emb.shape} float32, ids {ids.shape}")

# ---------------- 2. bench rebuild + provenance pin ----------------
sys.path.insert(0, BUILDER_DIR)
import build_exp107_bench as b
bench = b.build_bench()
assert len(bench) == 60, f"bench len {len(bench)}"
canon = json.dumps(bench, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
bhash = sha256_bytes(canon.encode("utf-8"))
assert bhash == BENCH_PIN, f"bench pin MISMATCH: {bhash}"
bench_ids = np.array([it["id"] for it in bench])
assert (bench_ids == ids).all(), "bench ids vs npz ids mismatch"
log("bench pin OK: 60 items, canonical-JSON sha256 matches; bench ids == npz ids 60/60")

# ---------------- 2b. archived EXP112 decision/readout columns ----------------
with open(EXP112_PER_ITEM, "r") as f:
    arch = json.load(f)
assert len(arch) == 60, f"archived per-item len {len(arch)}"
for a, it in zip(arch, bench):
    assert a["id"] == it["id"], "archived id order mismatch vs bench"
log("archived EXP112 per-item file: 60 records, id order matches bench exactly")

# ---------------- 3. backbone load + pre-forwards hash ----------------
from transformers import AutoTokenizer, AutoModelForCausalLM
tok = AutoTokenizer.from_pretrained(SNAP, local_files_only=True)
model = AutoModelForCausalLM.from_pretrained(
    SNAP, local_files_only=True, device_map="cpu", torch_dtype=torch.float32,
    output_hidden_states=True, output_attentions=False)
model.eval()
h_pre = state_dict_hash(model)
log(f"backbone hash BEFORE forwards: {h_pre}")
if h_pre != WEIGHTS_PIN:
    log("RUN-INVALID: backbone hash mismatch before forwards (Law #6). Quarantine. No metric exists.")
    sys.exit(42)
log("backbone pin OK (LOG-331)")
final_ln = model.gpt_neox.final_layer_norm  # GPTNeoXForCausalLM in transformers 5.17.0: gpt_neox submodule
lm_head_w = model.lm_head.weight  # (vocab, 1024), no bias on Pythia-410m
log(f"lens components: final_ln={type(final_ln).__name__}, lm_head {tuple(lm_head_w.shape)}")

# ---------------- 4. single-token BPE re-assertion against archived t1/t2 ----------------
items = []
for a, it in zip(arch, bench):
    E1, E2 = it["tuple"][0], it["tuple"][-1]
    t1_ids = tok.encode(" " + E1); t2_ids = tok.encode(" " + E2)
    if not (len(t1_ids) == 1 and len(t2_ids) == 1 and t1_ids[0] == a["t1"] and t2_ids[0] == a["t2"]):
        log(f"RUN-INVALID: single-token BPE re-assertion failed on item {it['id']}: "
            f"' {E1}' -> {t1_ids} (archived {a['t1']}), ' {E2}' -> {t2_ids} (archived {a['t2']}). "
            f"Items NOT silently dropped.")
        sys.exit(43)
    items.append({"id": it["id"], "prompt": it["prompt"], "E1": E1, "E2": E2,
                  "t1": a["t1"], "t2": a["t2"],
                  "decision": a["decision"], "readout_arch": a["readout"]})
log("single-token BPE re-assertion: 120/120 option texts exactly one token, match archived t1/t2")

# ---------------- 5. 60 forwards, logit lens at all 18 sites ----------------
def lens_readouts(h_stack, t1, t2):
    """h_stack: (18, 1024) float32 residual states at the final position.
    Logit lens per the pre-reg §3.3: logits_L = LayerNorm_f(h_L) @ W_U.
    In this transformers version the captured hidden_states[24] is ALREADY the
    final-layer-normed state (the capture decorator ties hs[-1] to
    last_hidden_state, which GPTNeoXModel normalizes internally) — applying the
    norm again would double-normalize and break the §3.2 consistency pin
    (lens@L24 must BE the model's output logits). Hence: for L=24 the lens is
    lm_head(h) with no additional norm; for L<=23 the lens applies
    final_layer_norm first. Verified: lm_head(hs[24]) == out.logits to 4.4e-06
    (float32 rounding); double-norm deviates by ~3.1.
    Returns (readouts dict site->E1/E2, masses dict site->mass)."""
    with torch.no_grad():
        H = torch.from_numpy(h_stack)                    # (18, 1024)
        # L24 is already final-layer-normed by the model; L<=23 need the norm applied.
        logits = torch.empty((len(SITES), lm_head_w.shape[0]), dtype=torch.float64)
        for j, L in enumerate(SITES):
            h = H[j:j+1]
            if L == 24:
                lg = (h @ lm_head_w.t())
            else:
                lg = (final_ln(h) @ lm_head_w.t())
            logits[j] = lg.to(torch.float64)
        logits = logits.numpy()                          # (18, vocab)
    readouts, masses = {}, {}
    for j, L in enumerate(SITES):
        lg = logits[j]
        if lg[t1] == lg[t2]:
            r, tie = "E2", True
        else:
            r, tie = ("E1" if lg[t1] > lg[t2] else "E2"), False
        mx = lg.max(); ex = np.exp(lg - mx); sm = ex / ex.sum()
        mass = float(sm[t1] + sm[t2])
        readouts[L] = (r, tie); masses[L] = mass
    return readouts, masses

log("running 60 logit-lens forwards (18 sites each)...")
per_item = []
with torch.no_grad():
    for i, rec in enumerate(items):
        inp = tok(rec["prompt"], return_tensors="pt")
        out = model(**inp)
        hs = out.hidden_states
        assert len(hs) == 25, f"hidden_states tuple len {len(hs)} != 25"
        # final position only
        h_stack = np.stack([np.asarray(hs[L][0, -1, :].detach().cpu(), dtype=np.float32) for L in SITES])
        readouts, masses = lens_readouts(h_stack, rec["t1"], rec["t2"])
        row = {"id": rec["id"], "decision": rec["decision"], "readout_arch": rec["readout_arch"],
               "readout": {}, "readout_tie": {}, "mass": {}}
        for L in SITES:
            r, tie = readouts[L]
            row["readout"][str(L)] = r
            row["readout_tie"][str(L)] = tie
            row["mass"][str(L)] = masses[L]
        per_item.append(row)
        if (i + 1) % 15 == 0:
            log(f"  {i + 1}/60 forwards done")
log("60 forwards complete: 1080 logit-lens readouts")

# ---------------- 5b. consistency pin: lens at L24 == archived readout, fidelity == 41/60 ----------------
mismatch = [(r["id"], r["readout_arch"], r["readout"]["24"]) for r in per_item
            if r["readout"]["24"] != r["readout_arch"]]
if mismatch:
    log(f"HALT: consistency-pin failure — {len(mismatch)}/60 lens-L24 readouts differ from the archived readout column. First: {mismatch[0]}")
    sys.exit(48)
agree_L24 = sum(1 for r in per_item if r["readout"]["24"] == r["decision"])
if (agree_L24, 60) != FID_PIN:
    log(f"HALT: consistency-pin failure — recomputed fidelity {agree_L24}/60 != 41/60 (archive drift).")
    sys.exit(49)
log(f"consistency pin OK: lens@L24 readouts byte-identical to archived column 60/60; fidelity {agree_L24}/60 == 41/60 exactly")

# ---------------- 6. backbone hash AFTER all forwards ----------------
h_post = state_dict_hash(model)
log(f"backbone hash AFTER forwards: {h_post}")
if h_post != WEIGHTS_PIN:
    log("RUN-INVALID: backbone hash mismatch after forwards (Law #6). Quarantine. No metric exists.")
    sys.exit(45)
log("backbone pin still OK after forwards (Delta theta = 0)")

# ---------------- 7. per-site degeneracy + run-validity rule BEFORE any metric ----------------
degenerate = {}
for L in SITES:
    mean_mass = float(np.mean([r["mass"][str(L)] for r in per_item]))
    degenerate[L] = mean_mass < 0.01
    log(f"site L{L}: mean mass on (t1,t2) = {mean_mass:.6f} -> {'DEGENERATE' if degenerate[L] else 'non-degenerate'}")
nd_early = sum(1 for L in EARLY_SITES if not degenerate[L])
nd_late = sum(1 for L in LATE_SITES if not degenerate[L])
log(f"non-degenerate sites: early window {nd_early}/9, late window {nd_late}/9")
if nd_early < 5 or nd_late < 5:
    log("RUN-INVALID: < 5 non-degenerate sites in a window (logit-lens apparatus failure). NOT a verdict.")
    sys.exit(46)
log("run-validity rule passed: >= 5 non-degenerate sites per window. Metric may now be read.")

# ---------------- 8. per-site fidelity + registered contrast (Law #9: read exactly once) ----------------
fid = {}
for L in SITES:
    agree = sum(1 for r in per_item if r["readout"][str(L)] == r["decision"])
    fid[L] = agree / 60
    log(f"site L{L}: fidelity {agree}/60 = {agree/60:.4f} {'(degenerate, excluded)' if degenerate[L] else ''}")
late_fids = [fid[L] for L in LATE_SITES if not degenerate[L]]
early_fids = [fid[L] for L in EARLY_SITES if not degenerate[L]]
late_mean = float(np.mean(late_fids)); early_mean = float(np.mean(early_fids))
C = late_mean - early_mean
log(f"late-window fidelity mean (non-degenerate {len(late_fids)} sites) = {late_mean:.4f}")
log(f"early-window fidelity mean (non-degenerate {len(early_fids)} sites) = {early_mean:.4f}")
log(f"CONTRAST C = {late_mean:.4f} - {early_mean:.4f} = {C:.4f}")

if C >= 0.10 and late_mean >= 0.65:
    verdict = "CONTINUE"; why = "late-layer localization is real (C>=0.10 and late-window fidelity >= 0.65)"
elif abs(C) < 0.05:
    verdict = "KILL"; why = "signal diffuse across the measured profile — no layer foothold"
elif C <= -0.10:
    verdict = "KILL"; why = "reverse concentration — late-locality hypothesis falsified"
else:
    verdict = "HELD"; why = "indeterminate (HELD zone); licenses nothing, retires nothing, no re-runs"
log(f"VERDICT: {verdict} — {why}")

# ---------------- 9. artifacts ----------------
with open(os.path.join(OUT, "exp118_per_item.json"), "w") as f:
    json.dump(per_item, f, indent=1)
worksheet = {
    "experiment": "EXP118", "hypothesis": "H13/HDI-LOC", "lane": "LOG-4619",
    "environment": manifest,
    "pins": {"npz": NPZ_PIN, "embeddings_bytes": EMB_BYTES_PIN, "ids_bytes": IDS_BYTES_PIN,
             "bench": BENCH_PIN, "backbone_pre": h_pre, "backbone_post": h_post},
    "consistency_pin": {"lens_L24_vs_archived_readout": "60/60 byte-identical",
                        "fidelity_L24": f"{agree_L24}/60", "expected": "41/60", "result": "PASS"},
    "degeneracy": {str(L): {"mean_mass": float(np.mean([r['mass'][str(L)] for r in per_item])),
                            "degenerate": degenerate[L]} for L in SITES},
    "nondegenerate_sites": {"early": nd_early, "late": nd_late},
    "per_site_fidelity": {str(L): fid[L] for L in SITES},
    "window_means": {"late": late_mean, "early": early_mean},
    "contrast_C": C,
    "verdict": verdict, "verdict_reason": why,
}
with open(os.path.join(OUT, "exp118_worksheet.json"), "w") as f:
    json.dump(worksheet, f, indent=1)
log("artifacts written: exp118_per_item.json, exp118_worksheet.json")
print(f"RESULT_JSON:{json.dumps({'C': C, 'late_mean': late_mean, 'early_mean': early_mean, 'verdict': verdict, 'nd_early': nd_early, 'nd_late': nd_late})}")
