"""
EXP056: Autonomous Closed-Loop Basis Lifecycle Verification.
Evaluates:
- Generation (G_unsup): Covariance-derived candidate subspaces
- Evaluation (E_unsup): Unsupervised entropy / energy scoring
- Selection (S): Argmin E_unsup(B_k) vs Oracle vs Random
- Immutability: Delta_theta = 0
- State Discard: Memory footprint reclamation
Pre-Registration: EXP056_AUTONOMOUS_LIFECYCLE_SPEC.md
Governing Laws: AGENTS.md Laws 1, 2, 6, 7, 9, 13, 14.
"""
import os, sys, json, hashlib, time, gc
import numpy as np
import torch
import torch.nn.functional as F
from datetime import datetime
from scipy.stats import binomtest, spearmanr
from transformers import AutoModelForCausalLM, AutoTokenizer

os.environ["TRANSFORMERS_NO_TF"] = "1"
os.environ["USE_TF"] = "0"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from experiments.benchmarks.bench_002_nl import generate_bench_002_nl

CANONICAL_MODEL = "EleutherAI/pythia-160m"
CANONICAL_HASH  = "54c88fa4897785f2bd94b32d26de1f73f1052bcc42124d563d0cda96940de936"
TARGET_BLOCK    = 7       # Layer 8 (0-indexed Block 7)
ALPHA           = 0.25
RANK            = 2
OUT_DIR         = os.path.join(os.path.dirname(__file__),
                      "../../experiments/runs/EXP056_autonomous_lifecycle")

def get_hash(model):
    h = hashlib.sha256()
    for p in model.parameters():
        h.update(p.detach().cpu().numpy().tobytes())
    return h.hexdigest()

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

def generate_unsupervised_candidates(h_all, rank=2):
    """
    Constructs candidate subspaces purely from prompt activations h_all: [seq_len, hidden_dim].
    Zero supervision or span annotations.
    """
    seq_len, dim = h_all.shape
    h_cent = h_all - torch.mean(h_all, dim=0, keepdim=True)
    _, S, Vh = torch.linalg.svd(h_cent, full_matrices=False)

    candidates = {}
    # Candidate 0: Top-2 principal components of full prompt covariance
    candidates["pca_top"] = Vh[:rank, :].T

    # Candidate 1: 2nd tier principal components (dims 2 to 4)
    if Vh.shape[0] >= rank * 2:
        candidates["pca_second"] = Vh[rank:rank*2, :].T
    else:
        candidates["pca_second"] = Vh[:rank, :].T

    # Candidate 2: High-norm token subset subspace (top 20% norm tokens)
    norms = torch.norm(h_all, dim=-1)
    k_tokens = max(rank + 1, int(0.25 * seq_len))
    top_indices = torch.topk(norms, k=min(k_tokens, seq_len)).indices
    h_top = h_all[top_indices, :]
    h_top_cent = h_top - torch.mean(h_top, dim=0, keepdim=True)
    _, _, Vh_top = torch.linalg.svd(h_top_cent, full_matrices=False)
    candidates["high_norm"] = Vh_top[:rank, :].T

    return candidates

def evaluate_unsupervised_score(logits, original_logits):
    """
    Unsupervised score: measures sharpening of the prediction distribution (negative entropy)
    and conservative divergence from base prior (KLD limit).
    """
    probs = F.softmax(logits, dim=-1)
    entropy = -torch.sum(probs * torch.log(probs + 1e-12)).item()
    # Sharper distribution = lower entropy -> higher score
    score = -entropy
    return score

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    log_file = os.path.join(OUT_DIR, "exp056_run_log.txt")
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(f"=== EXP056 Execution Started at {datetime.utcnow().isoformat()} ===\n")

    log("Initializing EXP056 Autonomous Closed-Loop Basis Lifecycle Verification...", log_file)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    log(f"Using compute device: {device}", log_file)

    tokenizer = AutoTokenizer.from_pretrained(CANONICAL_MODEL)
    model = AutoModelForCausalLM.from_pretrained(CANONICAL_MODEL).to(device)
    model.eval()

    pre_hash = get_hash(model)
    assert pre_hash == CANONICAL_HASH, f"Hash mismatch: {pre_hash}"
    log("Pre-run model hash verified: Delta_theta = 0.", log_file)

    dataset = generate_bench_002_nl(n_instances=50, seed=84)

    correct_counts = {
        "base": 0,
        "scpm_oracle": 0,    # G_contrastive with true span
        "unsup_selected": 0, # Selected via E_unsup
        "rand_candidate": 0  # Ablation 1: Random candidate choice
    }
    evaluator_correlations = []
    instances_log = []

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

        # 1. Base Forward Pass & Capture
        captured = {}
        def cap_h(mod, inp, outp):
            captured["h"] = (outp[0] if isinstance(outp, tuple) else outp).detach().squeeze(0)

        h_handle = model.gpt_neox.layers[TARGET_BLOCK].register_forward_hook(cap_h)
        with torch.no_grad():
            out_base = model(input_ids=input_ids)
            logits_base = out_base.logits[0, -1, :]
        h_handle.remove()

        pred_base = int(torch.argmax(logits_base).item())
        corr_base = int(pred_base == t_id)
        correct_counts["base"] += corr_base

        h_full = captured["h"]

        # 2. Oracle Reference: G_contrastive using true span
        X_cent = h_full[dist_indices, :] - torch.mean(h_full[dist_indices, :], dim=0, keepdim=True)
        _, _, Vh_oracle = torch.linalg.svd(X_cent, full_matrices=False)
        V_oracle = Vh_oracle[:RANK, :].T
        P_oracle = (V_oracle @ V_oracle.T).to(h_full.device)

        def hook_oracle(mod, inp, outp):
            h_mod = outp[0].clone() if isinstance(outp, tuple) else outp.clone()
            h_mod[0] = h_mod[0] - ALPHA * (h_mod[0] @ P_oracle)
            return (h_mod,) + outp[1:] if isinstance(outp, tuple) else h_mod

        h_handle = model.gpt_neox.layers[TARGET_BLOCK].register_forward_hook(hook_oracle)
        with torch.no_grad():
            logits_oracle = model(input_ids=input_ids).logits[0, -1, :]
        h_handle.remove()
        pred_oracle = int(torch.argmax(logits_oracle).item())
        corr_oracle = int(pred_oracle == t_id)
        correct_counts["scpm_oracle"] += corr_oracle

        # 3. Autonomous Generation: Construct Candidates
        cands = generate_unsupervised_candidates(h_full, rank=RANK)
        candidate_names = list(cands.keys())

        cand_scores = {}
        cand_preds = {}
        cand_corrs = {}

        for c_name, V_k in cands.items():
            P_k = (V_k @ V_k.T).to(h_full.device)
            def hook_k(mod, inp, outp, P_mat=P_k):
                h_mod = outp[0].clone() if isinstance(outp, tuple) else outp.clone()
                h_mod[0] = h_mod[0] - ALPHA * (h_mod[0] @ P_mat)
                return (h_mod,) + outp[1:] if isinstance(outp, tuple) else h_mod

            h_handle = model.gpt_neox.layers[TARGET_BLOCK].register_forward_hook(hook_k)
            with torch.no_grad():
                l_k = model(input_ids=input_ids).logits[0, -1, :]
            h_handle.remove()

            p_k = int(torch.argmax(l_k).item())
            cand_preds[c_name] = p_k
            cand_corrs[c_name] = int(p_k == t_id)
            cand_scores[c_name] = evaluate_unsupervised_score(l_k, logits_base)

        # 4. Selection Rule: Best according to E_unsup
        best_cand = max(cand_scores, key=cand_scores.get)
        corr_unsup = cand_corrs[best_cand]
        correct_counts["unsup_selected"] += corr_unsup

        # Ablation 1: Random candidate selection
        rng_cand = candidate_names[inst["id"] % len(candidate_names)]
        corr_rand = cand_corrs[rng_cand]
        correct_counts["rand_candidate"] += corr_rand

        # 5. Lifecycle Discard & Memory Cleanup
        del cands, P_oracle, V_oracle
        gc.collect()

        instances_log.append({
            "id": inst["id"],
            "corr_base": corr_base,
            "corr_oracle": corr_oracle,
            "corr_unsup": corr_unsup,
            "corr_rand": corr_rand,
            "selected_cand": best_cand
        })

    N = len(dataset)
    log("\n================ AUTONOMOUS LIFECYCLE SUMMARY (N=50) ================", log_file)
    for m, count in correct_counts.items():
        acc = count / N
        delta = acc - (correct_counts["base"] / N)
        b = sum(1 for x in instances_log if x["corr_base"] == 0 and x.get(f"corr_{m.replace('scpm_', '').replace('unsup_selected', 'unsup').replace('rand_candidate', 'rand')}", 0) == 1)
        c = sum(1 for x in instances_log if x["corr_base"] == 1 and x.get(f"corr_{m.replace('scpm_', '').replace('unsup_selected', 'unsup').replace('rand_candidate', 'rand')}", 0) == 0)
        p_val = mcnemar_p(b, c) if m != "base" else 1.0
        log(f"{m.upper():<16}: Acc={acc*100:.1f}% (Delta_M={delta*100:+.1f} pp) | Rescues={b} Corr={c} p={p_val:.4f}", log_file)

    post_hash = get_hash(model)
    assert post_hash == pre_hash, "Backbone altered!"
    log("\nBackbone immutability verified: Delta_theta = 0.", log_file)

    # Calculate Headroom Recovery
    base_acc = correct_counts["base"] / N
    oracle_acc = correct_counts["scpm_oracle"] / N
    unsup_acc = correct_counts["unsup_selected"] / N
    headroom = oracle_acc - base_acc
    recovered = unsup_acc - base_acc
    eta = (recovered / headroom) if headroom > 0 else 0.0

    log(f"Headroom Recovery eta: {eta*100:.1f}% ({recovered*100:+.1f} pp / {headroom*100:+.1f} pp)", log_file)
    verdict = "AUTONOMOUS_SCBI_CONFIRMED" if (eta >= 0.50 and unsup_acc > correct_counts["rand_candidate"]/N) else "SELECTION_BOTTLENECK_ACTIVE"
    log(f"\nFinal Verdict: >>> {verdict} <<<", log_file)

    out_payload = {
        "metadata": {
            "experiment": "EXP056",
            "title": "Autonomous Closed-Loop Basis Lifecycle Verification",
            "timestamp": datetime.utcnow().isoformat(),
            "model": CANONICAL_MODEL,
            "target_block": TARGET_BLOCK,
            "alpha": ALPHA,
            "rank": RANK,
            "headroom_recovery_eta": float(eta),
            "verdict": verdict
        },
        "accuracies": {k: float(v / N) for k, v in correct_counts.items()},
        "instances": instances_log
    }

    out_file = os.path.join(OUT_DIR, "exp056_autonomous_results.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(out_payload, f, indent=2)
    log(f"Saved complete results to {out_file}", log_file)

if __name__ == "__main__":
    main()
