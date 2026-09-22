"""
EXP050: Cross-Task & Generalization Transfer Battery for SCBI.
Evaluates G_contrastive across:
- Task T1: Distractor Suppression (BENCH-002-NL, Seed 84, N=50)
- Task T2: Order & Framing Permutation (BENCH-003-TEMPLATES, Seed 250, N=50)
- Task T3: Unseen Domain Transfer (BENCH-004-TRANSFER, Seed 350, N=50)
Pre-Registration: EXP050_CROSS_TASK_GENERALIZATION_SPEC.md
Governing Laws: AGENTS.md Laws 1, 2, 6, 7, 9, 11, 13, 14.
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
from experiments.benchmarks.bench_003_templates import generate_bench_003_templates
from experiments.benchmarks.bench_004_transfer import generate_bench_004_transfer

CANONICAL_MODEL = "EleutherAI/pythia-160m"
CANONICAL_HASH  = "54c88fa4897785f2bd94b32d26de1f73f1052bcc42124d563d0cda96940de936"
TARGET_BLOCK    = 7       # Layer 8 (0-indexed Block 7)
RANK            = 2
ALPHA           = 0.25
OUT_DIR         = os.path.join(os.path.dirname(__file__),
                      "../../experiments/runs/EXP050_cross_task_generalization")

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

def evaluate_instance(model, tokenizer, inst, task_id, target_block, alpha, rank, device):
    prompt = inst["base"]
    t_str = inst["target"].strip()
    t_enc = tokenizer.encode(" " + t_str)
    t_id = t_enc[0] if t_enc else tokenizer.encode(t_str)[0]

    enc = tokenizer(prompt, return_offsets_mapping=True, return_tensors="pt")
    input_ids = enc.input_ids.to(device)
    offsets = enc.offset_mapping[0].tolist()

    # Find distractor token indices depending on task benchmark structure
    if "distractor_evidence_text" in inst:
        dist_text = inst["distractor_evidence_text"]
        p_start = prompt.find(dist_text)
        if p_start != -1:
            p_end = p_start + len(dist_text)
            dist_indices = [i for i, (s, e) in enumerate(offsets) if s >= p_start and e <= p_end and s < e]
        else:
            dist_indices = []
    else:
        # Standard BENCH-002-NL format
        p_end = prompt.find(" Distractor:")
        d_end = prompt.find(" Question:")
        if p_end != -1 and d_end != -1:
            dist_indices = [i for i, (s, e) in enumerate(offsets) if s >= p_end and e <= d_end and s < e]
        else:
            dist_indices = []

    if not dist_indices:
        # Fallback: token matching for distractor token
        d_str = inst["distractor"].strip()
        d_enc = tokenizer.encode(" " + d_str)
        d_id = d_enc[0] if d_enc else tokenizer.encode(d_str)[0]
        dist_indices = [i for i, t in enumerate(input_ids[0].tolist()) if t == d_id]

    if not dist_indices:
        raise ValueError(f"Could not locate distractor span in prompt: {prompt[:50]}...")

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

    # G_contrastive intervention
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

    # Random subspace control
    torch.manual_seed(hash(str(inst["id"]) + task_id) % (2**31 - 1))
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
        "task": task_id,
        "corr_base": corr_base,
        "corr_g": corr_g,
        "corr_rand": corr_rand,
        "pred_base": pred_base,
        "pred_g": pred_g,
        "pred_rand": pred_rand,
        "delta_lp": lp_g - lp_base,
        "is_rescue": int(corr_base == 0 and corr_g == 1),
        "is_corruption": int(corr_base == 1 and corr_g == 0)
    }

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    log_file = os.path.join(OUT_DIR, "exp050_run_log.txt")
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(f"=== EXP050 Execution Started at {datetime.utcnow().isoformat()} ===\n")

    log("Initializing EXP050 Cross-Task Generalization Battery...", log_file)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    log(f"Using compute device: {device}", log_file)

    tokenizer = AutoTokenizer.from_pretrained(CANONICAL_MODEL)
    model = AutoModelForCausalLM.from_pretrained(CANONICAL_MODEL).to(device)
    model.eval()

    log("Verifying pre-run model parameter hash...", log_file)
    pre_hash = get_hash(model)
    log(f"Pre-hash:  {pre_hash}", log_file)
    assert pre_hash == CANONICAL_HASH, f"Hash mismatch! {pre_hash} != {CANONICAL_HASH}"
    log("Pre-run hash match confirmed (Delta_theta = 0).", log_file)

    tasks = {
        "T1_distractor_suppression": generate_bench_002_nl(n_instances=50, seed=84),
        "T2_template_permutation": generate_bench_003_templates(n_instances=50, seed=250),
        "T3_domain_transfer": generate_bench_004_transfer(n_instances=50, seed=350)
    }

    results_by_task = {}
    all_instances = []

    for task_name, dataset in tasks.items():
        log(f"\n--- Evaluating Task: {task_name} (N={len(dataset)}) ---", log_file)
        base_corr = 0
        g_corr = 0
        rand_corr = 0
        b_count = 0
        c_count = 0
        deltas = []

        for inst in dataset:
            res = evaluate_instance(model, tokenizer, inst, task_name, TARGET_BLOCK, ALPHA, RANK, device)
            all_instances.append(res)
            base_corr += res["corr_base"]
            g_corr    += res["corr_g"]
            rand_corr += res["corr_rand"]
            b_count   += res["is_rescue"]
            c_count   += res["is_corruption"]
            deltas.append(res["corr_g"] - res["corr_base"])

        n = len(dataset)
        acc_base = base_corr / n
        acc_g    = g_corr / n
        acc_rand = rand_corr / n
        delta_m  = acc_g - acc_base
        p_mcnemar = mcnemar_p(b_count, c_count)
        ci_low, ci_high = bootstrap_ci(deltas)

        results_by_task[task_name] = {
            "n": n,
            "acc_base": float(acc_base),
            "acc_g": float(acc_g),
            "acc_rand": float(acc_rand),
            "delta_m": float(delta_m),
            "rescues_b": b_count,
            "corruptions_c": c_count,
            "mcnemar_p": float(p_mcnemar),
            "ci_95": [float(ci_low), float(ci_high)]
        }

        log(f"[{task_name}] Base={acc_base*100:.1f}%, G_contrastive={acc_g*100:.1f}% (Delta_M={delta_m*100:+.1f} pp)", log_file)
        log(f"                Rand={acc_rand*100:.1f}%, Rescues={b_count}, Corruptions={c_count}, p={p_mcnemar:.5f}, 95% CI=[{ci_low*100:+.1f}, {ci_high*100:+.1f}]", log_file)

    log("\nVerifying post-run model parameter hash...", log_file)
    post_hash = get_hash(model)
    log(f"Post-hash: {post_hash}", log_file)
    assert post_hash == pre_hash, f"Immutability violation! Post-hash {post_hash} != Pre-hash {pre_hash}"
    log("Backbone immutability verified: Delta_theta = 0.", log_file)

    # Generalization verdict
    positive_tasks = sum(1 for t, res in results_by_task.items() if res["delta_m"] > 0 and res["mcnemar_p"] < 0.05)
    mean_delta = np.mean([res["delta_m"] for res in results_by_task.values()])
    verdict = "GENERALIZATION_CONFIRMED" if (positive_tasks >= 2 and mean_delta >= 0.05) else "TASK_SPECIFIC_OR_LIMITED"
    log(f"\nFinal Generalization Verdict: >>> {verdict} <<<", log_file)

    final_payload = {
        "metadata": {
            "experiment": "EXP050",
            "title": "Cross-Task & Generalization Transfer Battery",
            "timestamp": datetime.utcnow().isoformat(),
            "model": CANONICAL_MODEL,
            "hash_invariant": bool(pre_hash == post_hash == CANONICAL_HASH),
            "target_block": TARGET_BLOCK,
            "alpha": ALPHA,
            "rank": RANK,
            "verdict": verdict
        },
        "tasks": results_by_task,
        "instances": all_instances
    }

    out_file = os.path.join(OUT_DIR, "exp050_cross_task_results.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(final_payload, f, indent=2)
    log(f"Saved complete results to {out_file}", log_file)

if __name__ == "__main__":
    main()
