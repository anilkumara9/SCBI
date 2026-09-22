"""
EXP048: Canonical Deterministic Regression Lock for G_contrastive on BENCH-002 Seed-84.
Pre-Registration: LOG-057 (2026-09-12).
"""
import os, sys, json, hashlib, time
import numpy as np
import torch
import torch.nn.functional as F
from datetime import datetime
from scipy.stats import binomtest
from transformers import AutoModelForCausalLM, AutoTokenizer

os.environ["TRANSFORMERS_NO_TF"] = "1"
os.environ["USE_TF"] = "0"

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from experiments.benchmarks.bench_002_nl import generate_bench_002_nl

# --- FROZEN CANONICAL CONSTANTS --- DO NOT MODIFY ---
CANONICAL_MODEL    = "EleutherAI/pythia-160m"
CANONICAL_HASH     = "54c88fa4897785f2bd94b32d26de1f73f1052bcc42124d563d0cda96940de936"
CANONICAL_SEED     = 84
CANONICAL_N        = 50
CANONICAL_LAYER    = 7       # target_block 0-indexed (= Layer 8)
CANONICAL_RANK     = 2
CANONICAL_ALPHA    = 0.25
EXP043_LEDGER      = os.path.join(os.path.dirname(__file__),
                         "../../experiments/runs/EXP043_operator_discovery/"
                         "exp043_operator_discovery_results.json")
OUT_DIR            = os.path.join(os.path.dirname(__file__),
                         "../../experiments/runs/EXP048_regression_lock")
# Pre-registered thresholds
THRESH_BASE_EXACT  = 0.60
THRESH_INTERV_MIN  = 0.72
THRESH_B_MIN       = 6
THRESH_C_MAX       = 0
THRESH_P_MAX       = 0.05
THRESH_INST_MATCH  = 46


def get_hash(model):
    h = hashlib.sha256()
    for p in model.parameters():
        h.update(p.detach().cpu().numpy().tobytes())
    return h.hexdigest()

def extract_subspace(X, rank=2):
    X_cent = X - torch.mean(X, dim=0, keepdim=True)
    if X_cent.shape[0] < rank:
        rank = max(1, X_cent.shape[0])
    _, _, Vh = torch.linalg.svd(X_cent, full_matrices=False)
    return Vh[:rank, :].T

def mcnemar_p(b, c):
    n = b + c
    if n == 0: return 1.0
    return float(binomtest(b, n, 0.5, alternative="greater").pvalue)

def log(msg):
    print(f"[{datetime.utcnow().strftime('%H:%M:%S')}] {msg}", flush=True)

def evaluate(model, tokenizer, inst, target_block, alpha, rank):
    prompt = inst["base"]
    t_str = inst["target"].strip()
    t_enc = tokenizer.encode(" " + t_str)
    t_id = t_enc[0] if t_enc else tokenizer.encode(t_str)[0]

    enc = tokenizer(prompt, return_offsets_mapping=True, return_tensors="pt")
    input_ids = enc.input_ids
    offsets = enc.offset_mapping[0].tolist()

    p_end = prompt.index(" Distractor:")
    d_end = prompt.index(" Question:")
    dist_indices = [i for i, (s, e) in enumerate(offsets) if s >= p_end and e <= d_end and s < e]
    if not dist_indices:
        raise ValueError("Empty distractor span")

    captured = {}
    def cap_h8(mod, inp, outp):
        captured["h8"] = (outp[0] if isinstance(outp, tuple) else outp).detach().squeeze(0)

    h8h = model.gpt_neox.layers[target_block].register_forward_hook(cap_h8)
    with torch.no_grad():
        out_base = model(input_ids=input_ids)
        logits_base = out_base.logits[0, -1, :]
    h8h.remove()

    pred_base = int(torch.argmax(logits_base).item())
    corr_base = int(pred_base == t_id)
    lp_base   = float(torch.log(torch.clamp(F.softmax(logits_base, -1)[t_id], min=1e-12)).item())

    # Canonical G_contrastive
    h8 = captured["h8"]
    V_c = extract_subspace(h8[dist_indices, :], rank=rank)
    P_c = (V_c @ V_c.T).to(h8.device)

    def hook_r(mod, inp, outp):
        h = outp[0].clone() if isinstance(outp, tuple) else outp.clone()
        h[0] = h[0] - alpha * (h[0] @ P_c)
        return (h,) + outp[1:] if isinstance(outp, tuple) else h

    hr = model.gpt_neox.layers[target_block].register_forward_hook(hook_r)
    with torch.no_grad():
        out_r = model(input_ids=input_ids)
        logits_r = out_r.logits[0, -1, :]
    hr.remove()

    pred_r = int(torch.argmax(logits_r).item())
    corr_r = int(pred_r == t_id)
    lp_r   = float(torch.log(torch.clamp(F.softmax(logits_r, -1)[t_id], min=1e-12)).item())

    return {
        "inst_id":   inst.get("id", -1),
        "domain":    inst.get("domain", -1),
        "target":    t_str,
        "t_id":      t_id,
        "corr_base": corr_base,
        "pred_base": pred_base,
        "corr_r":    corr_r,
        "pred_r":    pred_r,
        "rescued":   int(corr_base == 0 and corr_r == 1),
        "corrupted": int(corr_base == 1 and corr_r == 0),
        "delta_lp":  lp_r - lp_base,
    }

def run():
    log("=" * 80)
    log("EXP048: Canonical Deterministic Regression Lock")
    log(f"  Model:    {CANONICAL_MODEL}")
    log(f"  Seed:     {CANONICAL_SEED}  N: {CANONICAL_N}  Layer: {CANONICAL_LAYER}")
    log(f"  Operator: G_contrastive = extract_subspace(h8[dist_indices], rank=2)")
    log("=" * 80)
    os.makedirs(OUT_DIR, exist_ok=True)

    log("Loading model...")
    tokenizer = AutoTokenizer.from_pretrained(CANONICAL_MODEL)
    model = AutoModelForCausalLM.from_pretrained(CANONICAL_MODEL)
    model.eval()

    pre_hash = get_hash(model)
    hash_ok = pre_hash == CANONICAL_HASH
    log(f"Pre-hash: {pre_hash}")
    log(f"Hash match: {hash_ok} {'[VERIFIED]' if hash_ok else '[WARNING: MISMATCH]'}")

    # Load EXP043 reference
    exp043_ref = {}
    try:
        with open(EXP043_LEDGER) as f:
            d = json.load(f)
        c43 = d.get("pythia", {}).get("controllers", {})
        exp043_ref = {
            "baseline_acc": c43.get("Baseline (Unintervened)", {}).get("accuracy"),
            "ref_acc":      c43.get("G_contrastive (Supervised Ref)", {}).get("accuracy"),
            "b":            c43.get("G_contrastive (Supervised Ref)", {}).get("rescued_b"),
            "c":            c43.get("G_contrastive (Supervised Ref)", {}).get("corrupted_c"),
            "mcnemar_p":    c43.get("G_contrastive (Supervised Ref)", {}).get("mcnemar_p"),
        }
        log(f"EXP043 reference: baseline={exp043_ref['baseline_acc']} "
            f"G_contrastive={exp043_ref['ref_acc']} b={exp043_ref['b']} "
            f"c={exp043_ref['c']} p={exp043_ref['mcnemar_p']}")
    except Exception as e:
        log(f"WARNING: Could not load EXP043 ledger: {e}")

    instances = generate_bench_002_nl(n_instances=CANONICAL_N, seed=CANONICAL_SEED)
    log(f"Generated {len(instances)} BENCH-002-NL instances (Seed={CANONICAL_SEED})")

    records = []
    skipped = 0
    for inst in instances:
        try:
            rec = evaluate(model, tokenizer, inst,
                           target_block=CANONICAL_LAYER,
                           alpha=CANONICAL_ALPHA, rank=CANONICAL_RANK)
            records.append(rec)
        except Exception as e:
            log(f"  SKIP {inst.get('id','?')}: {e}")
            skipped += 1

    N  = len(records)
    b  = sum(r["rescued"]   for r in records)
    c  = sum(r["corrupted"] for r in records)
    ba = float(np.mean([r["corr_base"] for r in records]))
    ia = float(np.mean([r["corr_r"]   for r in records]))
    mp = mcnemar_p(b, c)
    md = float(np.mean([r["delta_lp"] for r in records]))

    log("\n" + "=" * 80)
    log(f"  N evaluated:          {N} ({skipped} skipped)")
    log(f"  Baseline accuracy:    {ba:.4f} ({int(ba*N)}/{N})")
    log(f"  G_contrastive acc:    {ia:.4f} ({int(ia*N)}/{N})")
    log(f"  Delta M:              {ia-ba:+.4f}")
    log(f"  Rescues (b):          {b}")
    log(f"  Corruptions (c):      {c}")
    log(f"  McNemar p:            {mp:.6f}")
    log(f"  Mean delta log p:     {md:+.6f}")

    log("\n  --- Pre-Registered Acceptance Audit ---")
    bp = abs(ba - THRESH_BASE_EXACT) < 1e-9
    ip = ia >= THRESH_INTERV_MIN
    rp = b  >= THRESH_B_MIN
    cp = c  <= THRESH_C_MAX
    pp = mp <= THRESH_P_MAX

    log(f"  [{'PASS' if bp else 'FAIL'}] Baseline == 60%:  {ba:.4f}")
    log(f"  [{'PASS' if ip else 'FAIL'}] Interv >= 72%:    {ia:.4f}")
    log(f"  [{'PASS' if rp else 'FAIL'}] b >= 6:           {b}")
    log(f"  [{'PASS' if cp else 'FAIL'}] c = 0:            {c}")
    log(f"  [{'PASS' if pp else 'FAIL'}] McNemar p <= 0.05:{mp:.6f}")

    if exp043_ref:
        bm = exp043_ref.get("b") is not None and abs(b - exp043_ref["b"]) <= 1
        cm = exp043_ref.get("c") is not None and c == exp043_ref["c"]
        am = exp043_ref.get("baseline_acc") is not None and abs(ba - exp043_ref["baseline_acc"]) < 1e-9
        log(f"  [{'MATCH' if am else 'MISMATCH'}] EXP043 baseline: EXP048={ba:.2f} vs EXP043={exp043_ref.get('baseline_acc')}")
        log(f"  [{'MATCH' if bm else 'MISMATCH'}] EXP043 b (+-1):  EXP048 b={b} vs EXP043 b={exp043_ref.get('b')}")
        log(f"  [{'MATCH' if cm else 'MISMATCH'}] EXP043 c:         EXP048 c={c} vs EXP043 c={exp043_ref.get('c')}")

    all_pass = all([bp, ip, rp, cp, pp])
    if all_pass:
        verdict = "REGRESSION_LOCK_CONFIRMED"
    elif not bp or b < 5 or c > 0:
        verdict = "FAILURE_CRITERION_TRIGGERED: EXP043 provenance audit required"
    else:
        verdict = "PARTIAL_PASS: review per-instance table"

    log(f"\n  >>> VERDICT: {verdict}")

    post_hash = get_hash(model)
    log(f"\n  Post-hash: {post_hash}")
    log(f"  Delta_theta=0: {pre_hash == post_hash}")

    log("\n  --- Per-Instance Table ---")
    log(f"{'ID':>4} {'dom':>4} {'target':>12} {'base':>5} {'interv':>6} {'b':>3} {'c':>3} {'dlp':>8}")
    log("-" * 55)
    for r in records:
        print(f"  {r['inst_id']:>4} {r['domain']:>4} {r['target']:>12} "
              f"{r['corr_base']:>5} {r['corr_r']:>6} "
              f"{r['rescued']:>3} {r['corrupted']:>3} {r['delta_lp']:>+8.4f}", flush=True)

    results = {
        "metadata": {
            "experiment_id": "EXP048",
            "date": datetime.utcnow().strftime("%Y-%m-%d"),
            "model": CANONICAL_MODEL,
            "pre_hash": pre_hash, "post_hash": post_hash,
            "hash_invariant": pre_hash == post_hash,
            "canonical_hash": CANONICAL_HASH,
            "hash_verified": hash_ok,
            "seed": CANONICAL_SEED, "n": CANONICAL_N,
            "n_evaluated": N, "n_skipped": skipped,
            "target_block": CANONICAL_LAYER,
            "alpha": CANONICAL_ALPHA, "rank": CANONICAL_RANK,
            "operator": "G_contrastive=extract_subspace(h8[dist_indices],rank=2)",
        },
        "results": {
            "baseline_accuracy": ba, "intervention_accuracy": ia,
            "delta_m": ia - ba, "b": b, "c": c,
            "mcnemar_p": mp, "mean_delta_logp": md,
        },
        "exp043_reference": exp043_ref,
        "acceptance_audit": {
            "baseline_pass": bp, "interv_pass": ip,
            "b_pass": rp, "c_pass": cp, "mcnemar_pass": pp,
            "all_pass": all_pass, "verdict": verdict,
        },
        "per_instance": records,
    }

    out = os.path.join(OUT_DIR, "exp048_regression_results.json")
    with open(out, "w") as f:
        json.dump(results, f, indent=2)
    log(f"\nSaved: {out}")
    log("EXP048 DONE.")

if __name__ == "__main__":
    run()
