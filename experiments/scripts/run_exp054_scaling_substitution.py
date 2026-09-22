"""
EXP054: Parameter Scaling Substitution Test.
Investigates whether temporary cognitive basis computation (Bt) on a smaller model
can substitute for permanent parameter scaling:
Pythia-70M + Bt vs Pythia-160M
Pythia-160M + Bt vs Pythia-410M
Pre-Registration: EXP054_SCALING_SUBSTITUTION_SPEC.md
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

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from experiments.benchmarks.bench_002_nl import generate_bench_002_nl

OUT_DIR = os.path.join(os.path.dirname(__file__),
              "../../experiments/runs/EXP054_scaling_substitution")

# Models to evaluate
MODEL_CONFIGS = {
    "pythia-70m": {
        "name": "EleutherAI/pythia-70m",
        "params_m": 70,
        "target_block": 3,   # Block 3 / 6 (Layer 4)
        "alpha": 0.25,
        "rank": 2
    },
    "pythia-160m": {
        "name": "EleutherAI/pythia-160m",
        "params_m": 160,
        "target_block": 7,   # Block 7 / 12 (Layer 8)
        "alpha": 0.25,
        "rank": 2
    },
    "pythia-410m": {
        "name": "EleutherAI/pythia-410m",
        "params_m": 410,
        "target_block": 14,  # Block 14 / 24 (Layer 15)
        "alpha": 0.25,
        "rank": 2
    }
}

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

def log(msg, log_file=None):
    ts = datetime.utcnow().strftime("%H:%M:%S")
    formatted = f"[{ts}] {msg}"
    print(formatted, flush=True)
    if log_file:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(formatted + "\n")

def evaluate_model_family(model_key, cfg, dataset, device, log_file):
    log(f"\n--- Loading and Evaluating Model: {cfg['name']} ({cfg['params_m']}M params) ---", log_file)
    tokenizer = AutoTokenizer.from_pretrained(cfg["name"])
    model = AutoModelForCausalLM.from_pretrained(cfg["name"]).to(device)
    model.eval()

    pre_hash = get_hash(model)
    log(f"Pre-run hash: {pre_hash}", log_file)

    base_corr = 0
    scpm_corr = 0
    b_count = 0
    c_count = 0
    inst_records = []
    target_block = cfg["target_block"]
    alpha = cfg["alpha"]
    rank = cfg["rank"]

    for inst in dataset:
        prompt = inst["base"]
        t_str = inst["target"].strip()
        t_enc = tokenizer.encode(" " + t_str)
        t_id = t_enc[0] if t_enc else tokenizer.encode(t_str)[0]

        enc = tokenizer(prompt, return_offsets_mapping=True, return_tensors="pt")
        input_ids = enc.input_ids.to(device)
        offsets = enc.offset_mapping[0].tolist()

        p_end = prompt.find(" Distractor:")
        d_end = prompt.find(" Question:")
        dist_indices = [i for i, (s, e) in enumerate(offsets) if s >= p_end and e <= d_end and s < e]

        # 1. Base forward pass
        captured = {}
        def cap_h(mod, inp, outp):
            captured["h"] = (outp[0] if isinstance(outp, tuple) else outp).detach().squeeze(0)

        h_handle = model.gpt_neox.layers[target_block].register_forward_hook(cap_h)
        with torch.no_grad():
            logits_base = model(input_ids=input_ids).logits[0, -1, :]
        h_handle.remove()

        pred_base = int(torch.argmax(logits_base).item())
        corr_base = int(pred_base == t_id)
        base_corr += corr_base

        # 2. SCPM forward pass
        h = captured["h"]
        V_c = extract_subspace(h[dist_indices, :], rank=rank)
        P_c = (V_c @ V_c.T).to(h.device)

        def hook_scpm(mod, inp, outp):
            h_mod = outp[0].clone() if isinstance(outp, tuple) else outp.clone()
            h_mod[0] = h_mod[0] - alpha * (h_mod[0] @ P_c)
            return (h_mod,) + outp[1:] if isinstance(outp, tuple) else h_mod

        h_handle = model.gpt_neox.layers[target_block].register_forward_hook(hook_scpm)
        with torch.no_grad():
            logits_scpm = model(input_ids=input_ids).logits[0, -1, :]
        h_handle.remove()

        pred_scpm = int(torch.argmax(logits_scpm).item())
        corr_scpm = int(pred_scpm == t_id)
        scpm_corr += corr_scpm

        is_rescue = int(corr_base == 0 and corr_scpm == 1)
        is_corruption = int(corr_base == 1 and corr_scpm == 0)
        b_count += is_rescue
        c_count += is_corruption

        inst_records.append({
            "id": inst["id"],
            "corr_base": corr_base,
            "corr_scpm": corr_scpm,
            "is_rescue": is_rescue,
            "is_corruption": is_corruption
        })

    post_hash = get_hash(model)
    assert post_hash == pre_hash, f"Backbone altered for {cfg['name']}!"

    N = len(dataset)
    acc_base = base_corr / N
    acc_scpm = scpm_corr / N
    p_val = mcnemar_p(b_count, c_count)

    log(f"[{model_key}] Base: {acc_base*100:.1f}%, SCPM: {acc_scpm*100:.1f}% (Delta_M={(acc_scpm-acc_base)*100:+.1f} pp)", log_file)
    log(f"[{model_key}] Rescues: {b_count}, Corruptions: {c_count}, McNemar p: {p_val:.4f}", log_file)

    # Free memory
    del model
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    return {
        "params_m": cfg["params_m"],
        "acc_base": float(acc_base),
        "acc_scpm": float(acc_scpm),
        "delta_m": float(acc_scpm - acc_base),
        "rescues_b": b_count,
        "corruptions_c": c_count,
        "mcnemar_p": float(p_val),
        "hash_invariant": True
    }

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    log_file = os.path.join(OUT_DIR, "exp054_run_log.txt")
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(f"=== EXP054 Execution Started at {datetime.utcnow().isoformat()} ===\n")

    log("Initializing EXP054 Parameter Scaling Substitution Test...", log_file)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    log(f"Using compute device: {device}", log_file)

    dataset = generate_bench_002_nl(n_instances=50, seed=84)

    results = {}
    for k, cfg in MODEL_CONFIGS.items():
        try:
            results[k] = evaluate_model_family(k, cfg, dataset, device, log_file)
        except Exception as e:
            log(f"Warning: Failed to evaluate {k}: {e}", log_file)

    # Evaluate substitution hypothesis
    log("\n================ SCALING SUBSTITUTION AUDIT ================", log_file)
    if "pythia-160m" in results and "pythia-410m" in results:
        scpm_160 = results["pythia-160m"]["acc_scpm"]
        base_410 = results["pythia-410m"]["acc_base"]
        log(f"Pythia-160M + SCPM (160M params): {scpm_160*100:.1f}%", log_file)
        log(f"Pythia-410M Base   (410M params): {base_410*100:.1f}%", log_file)
        sub_gap = scpm_160 - base_410
        log(f"Substitution Margin: {sub_gap*100:+.1f} pp", log_file)
        if sub_gap >= -0.02:
            verdict = "SCALING_SUBSTITUTION_SUPPORTED"
            log(f"Result: Pythia-160M + SCPM successfully matches/exceeds Pythia-410M base capacity!", log_file)
        else:
            verdict = "SCALING_SUBSTITUTION_FALSIFIED"
            log(f"Result: Pythia-160M + SCPM does not match Pythia-410M base capacity.", log_file)
    else:
        verdict = "PARTIAL_EVALUATION"

    out_payload = {
        "metadata": {
            "experiment": "EXP054",
            "title": "Parameter Scaling Substitution Test",
            "timestamp": datetime.utcnow().isoformat(),
            "verdict": verdict
        },
        "models": results
    }

    out_file = os.path.join(OUT_DIR, "exp054_scaling_results.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(out_payload, f, indent=2)
    log(f"Saved complete results to {out_file}", log_file)

if __name__ == "__main__":
    main()
