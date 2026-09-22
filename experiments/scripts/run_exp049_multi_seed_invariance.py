"""
EXP049: Strict Multi-Seed & Split Invariance Audit for G_contrastive on Pythia-160M.
Tests Seeds 42, 168, 256, 512 (N=50 each, Pooled N=200) on BENCH-002-NL.
Pre-Registration: EXP049_MULTI_SEED_INVARIANCE_SPEC.md
Governing Laws: AGENTS.md Laws 1, 2, 6, 7, 9, 13, 14.
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

# --- PROTOCOL LOCKS ---
CANONICAL_MODEL    = "EleutherAI/pythia-160m"
CANONICAL_HASH     = "54c88fa4897785f2bd94b32d26de1f73f1052bcc42124d563d0cda96940de936"
SEEDS              = [42, 168, 256, 512]
N_PER_SEED         = 50
TARGET_BLOCK       = 7       # 0-indexed Block 7 = Layer 8
RANK               = 2
ALPHA              = 0.25
OUT_DIR            = os.path.join(os.path.dirname(__file__),
                         "../../experiments/runs/EXP049_multi_seed_invariance")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

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

def bootstrap_ci(deltas, n_boot=10000, alpha=0.05):
    rng = np.random.default_rng(42)
    deltas = np.array(deltas, dtype=float)
    boot_means = [rng.choice(deltas, size=len(deltas), replace=True).mean() for _ in range(n_boot)]
    low = np.percentile(boot_means, 100 * (alpha / 2))
    high = np.percentile(boot_means, 100 * (1 - alpha / 2))
    return float(low), float(high)

def log(msg, log_file=None):
    ts = datetime.utcnow().strftime("%H:%M:%S")
    formatted = f"[{ts}] {msg}"
    print(formatted, flush=True)
    if log_file:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(formatted + "\n")

def evaluate_instance(model, tokenizer, inst, target_block, alpha, rank, device):
    prompt = inst["base"]
    t_str = inst["target"].strip()
    t_enc = tokenizer.encode(" " + t_str)
    t_id = t_enc[0] if t_enc else tokenizer.encode(t_str)[0]

    enc = tokenizer(prompt, return_offsets_mapping=True, return_tensors="pt")
    input_ids = enc.input_ids.to(device)
    offsets = enc.offset_mapping[0].tolist()

    p_end = prompt.index(" Distractor:")
    d_end = prompt.index(" Question:")
    dist_indices = [i for i, (s, e) in enumerate(offsets) if s >= p_end and e <= d_end and s < e]
    if not dist_indices:
        raise ValueError("Empty distractor span")

    captured = {}
    def cap_h(mod, inp, outp):
        captured["h"] = (outp[0] if isinstance(outp, tuple) else outp).detach().squeeze(0)

    hook_handle = model.gpt_neox.layers[target_block].register_forward_hook(cap_h)
    with torch.no_grad():
        out_base = model(input_ids=input_ids)
        logits_base = out_base.logits[0, -1, :]
    hook_handle.remove()

    pred_base = int(torch.argmax(logits_base).item())
    corr_base = int(pred_base == t_id)
    lp_base   = float(torch.log(torch.clamp(F.softmax(logits_base, -1)[t_id], min=1e-12)).item())

    # 1. Canonical G_contrastive
    h = captured["h"]
    V_c = extract_subspace(h[dist_indices, :], rank=rank)
    P_c = (V_c @ V_c.T).to(h.device)

    def hook_g(mod, inp, outp):
        h_mod = outp[0].clone() if isinstance(outp, tuple) else outp.clone()
        h_mod[0] = h_mod[0] - alpha * (h_mod[0] @ P_c)
        return (h_mod,) + outp[1:] if isinstance(outp, tuple) else h_mod

    hook_handle = model.gpt_neox.layers[target_block].register_forward_hook(hook_g)
    with torch.no_grad():
        out_g = model(input_ids=input_ids)
        logits_g = out_g.logits[0, -1, :]
    hook_handle.remove()

    pred_g = int(torch.argmax(logits_g).item())
    corr_g = int(pred_g == t_id)
    lp_g   = float(torch.log(torch.clamp(F.softmax(logits_g, -1)[t_id], min=1e-12)).item())

    # 2. Negative Control: Random Subspace
    torch.manual_seed(hash(inst["id"]) % (2**31 - 1))
    rand_mat = torch.randn(h.shape[-1], rank, device=h.device)
    Q, _ = torch.linalg.qr(rand_mat)
    V_rand = Q[:, :rank]
    P_rand = (V_rand @ V_rand.T).to(h.device)

    def hook_rand(mod, inp, outp):
        h_mod = outp[0].clone() if isinstance(outp, tuple) else outp.clone()
        h_mod[0] = h_mod[0] - alpha * (h_mod[0] @ P_rand)
        return (h_mod,) + outp[1:] if isinstance(outp, tuple) else h_mod

    hook_handle = model.gpt_neox.layers[target_block].register_forward_hook(hook_rand)
    with torch.no_grad():
        out_rand = model(input_ids=input_ids)
        logits_rand = out_rand.logits[0, -1, :]
    hook_handle.remove()

    pred_rand = int(torch.argmax(logits_rand).item())
    corr_rand = int(pred_rand == t_id)

    return {
        "id": inst["id"],
        "target_token": t_str,
        "target_id": t_id,
        "corr_base": corr_base,
        "corr_g": corr_g,
        "corr_rand": corr_rand,
        "pred_base": pred_base,
        "pred_g": pred_g,
        "pred_rand": pred_rand,
        "lp_base": lp_base,
        "lp_g": lp_g,
        "delta_lp": lp_g - lp_base,
        "is_rescue": int(corr_base == 0 and corr_g == 1),
        "is_corruption": int(corr_base == 1 and corr_g == 0),
    }

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    log_file = os.path.join(OUT_DIR, "exp049_run_log.txt")
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(f"=== EXP049 Execution Started at {datetime.utcnow().isoformat()} ===\n")

    log("Initializing EXP049 Multi-Seed Invariance Audit...", log_file)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    log(f"Using compute device: {device}", log_file)

    tokenizer = AutoTokenizer.from_pretrained(CANONICAL_MODEL)
    model = AutoModelForCausalLM.from_pretrained(CANONICAL_MODEL).to(device)
    model.eval()

    log("Verifying pre-run model parameter hash...", log_file)
    pre_hash = get_hash(model)
    log(f"Pre-hash:  {pre_hash}", log_file)
    log(f"Canonical: {CANONICAL_HASH}", log_file)
    assert pre_hash == CANONICAL_HASH, f"Hash mismatch! {pre_hash} != {CANONICAL_HASH}"
    log("Pre-run hash match confirmed (Delta_theta = 0).", log_file)

    results_by_seed = {}
    pooled_deltas = []
    pooled_b = 0
    pooled_c = 0
    pooled_base_corr = 0
    pooled_g_corr = 0
    pooled_rand_corr = 0
    all_instances = []

    for seed in SEEDS:
        log(f"\n--- Running Seed {seed} (N={N_PER_SEED}) ---", log_file)
        bench = generate_bench_002_nl(n_instances=N_PER_SEED, seed=seed)
        seed_instances = []
        b_count = 0
        c_count = 0
        base_correct = 0
        g_correct = 0
        rand_correct = 0
        seed_deltas = []

        for inst in bench:
            res = evaluate_instance(model, tokenizer, inst, TARGET_BLOCK, ALPHA, RANK, device)
            res["seed"] = seed
            seed_instances.append(res)
            all_instances.append(res)

            base_correct += res["corr_base"]
            g_correct    += res["corr_g"]
            rand_correct += res["corr_rand"]
            b_count      += res["is_rescue"]
            c_count      += res["is_corruption"]
            delta_acc    = res["corr_g"] - res["corr_base"]
            seed_deltas.append(delta_acc)
            pooled_deltas.append(delta_acc)

        p_mcnemar = mcnemar_p(b_count, c_count)
        ci_low, ci_high = bootstrap_ci(seed_deltas)
        acc_base = base_correct / N_PER_SEED
        acc_g    = g_correct / N_PER_SEED
        acc_rand = rand_correct / N_PER_SEED
        delta_m  = acc_g - acc_base

        pooled_base_corr += base_correct
        pooled_g_corr    += g_correct
        pooled_rand_corr += rand_correct
        pooled_b         += b_count
        pooled_c         += c_count

        results_by_seed[str(seed)] = {
            "seed": seed,
            "n": N_PER_SEED,
            "acc_base": float(acc_base),
            "acc_g": float(acc_g),
            "acc_rand": float(acc_rand),
            "delta_m": float(delta_m),
            "rescues_b": b_count,
            "corruptions_c": c_count,
            "mcnemar_p": float(p_mcnemar),
            "ci_95": [float(ci_low), float(ci_high)]
        }

        log(f"Seed {seed} Result: Base={acc_base*100:.1f}%, G_contrastive={acc_g*100:.1f}% (Delta_M={delta_m*100:+.1f} pp)", log_file)
        log(f"                Rand={acc_rand*100:.1f}%, Rescues={b_count}, Corruptions={c_count}, p={p_mcnemar:.5f}, 95% CI=[{ci_low*100:+.1f}, {ci_high*100:+.1f}]", log_file)

    # Pooled analysis
    total_n = len(pooled_deltas)
    pooled_acc_base = pooled_base_corr / total_n
    pooled_acc_g    = pooled_g_corr / total_n
    pooled_acc_rand = pooled_rand_corr / total_n
    pooled_delta_m  = pooled_acc_g - pooled_acc_base
    pooled_p        = mcnemar_p(pooled_b, pooled_c)
    p_ci_low, p_ci_high = bootstrap_ci(pooled_deltas)

    log("\n================ POOLED AUDIT SUMMARY (N=200) ================", log_file)
    log(f"Pooled Baseline:      {pooled_acc_base*100:.2f}% ({pooled_base_corr}/{total_n})", log_file)
    log(f"Pooled G_contrastive: {pooled_acc_g*100:.2f}% ({pooled_g_corr}/{total_n})", log_file)
    log(f"Pooled Random Ctrl:   {pooled_acc_rand*100:.2f}% ({pooled_rand_corr}/{total_n})", log_file)
    log(f"Pooled Delta M:       {pooled_delta_m*100:+.2f} pp", log_file)
    log(f"Total Rescues (b):    {pooled_b}", log_file)
    log(f"Total Corruptions (c):{pooled_c}", log_file)
    log(f"Pooled McNemar p:     {pooled_p:.6e}", log_file)
    log(f"Pooled 95% CI:        [{p_ci_low*100:+.2f}, {p_ci_high*100:+.2f}] pp", log_file)

    log("\nVerifying post-run model parameter hash...", log_file)
    post_hash = get_hash(model)
    log(f"Post-hash: {post_hash}", log_file)
    assert post_hash == pre_hash, f"Immutability violation! Post-hash {post_hash} != Pre-hash {pre_hash}"
    log("Backbone immutability verified: Delta_theta = 0.", log_file)

    # Success / Falsification evaluation against pre-registered criteria
    criteria_passed = (
        pooled_delta_m >= 0.08 and
        pooled_p < 0.01 and
        p_ci_low > 0.0 and
        pooled_b >= 3 * max(1, pooled_c) and
        pooled_acc_g > pooled_acc_rand
    )
    verdict = "INVARIANCE_CONFIRMED" if criteria_passed else "FALSIFIED_OR_WEAK"
    log(f"\nFinal Pre-Registered Audit Verdict: >>> {verdict} <<<", log_file)

    final_payload = {
        "metadata": {
            "experiment": "EXP049",
            "title": "Strict Multi-Seed & Split Invariance Audit",
            "timestamp": datetime.utcnow().isoformat(),
            "model": CANONICAL_MODEL,
            "pre_hash": pre_hash,
            "post_hash": post_hash,
            "hash_invariant": bool(pre_hash == post_hash == CANONICAL_HASH),
            "target_block": TARGET_BLOCK,
            "alpha": ALPHA,
            "rank": RANK,
            "seeds": SEEDS,
            "n_per_seed": N_PER_SEED,
            "total_n": total_n,
            "verdict": verdict
        },
        "per_seed": results_by_seed,
        "pooled": {
            "acc_base": float(pooled_acc_base),
            "acc_g": float(pooled_acc_g),
            "acc_rand": float(pooled_acc_rand),
            "delta_m": float(pooled_delta_m),
            "rescues_b": pooled_b,
            "corruptions_c": pooled_c,
            "mcnemar_p": float(pooled_p),
            "ci_95": [float(p_ci_low), float(p_ci_high)],
            "criteria_passed": bool(criteria_passed)
        },
        "instances": all_instances
    }

    out_file = os.path.join(OUT_DIR, "exp049_multi_seed_results.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(final_payload, f, indent=2)
    log(f"Saved complete results to {out_file}", log_file)

if __name__ == "__main__":
    main()
