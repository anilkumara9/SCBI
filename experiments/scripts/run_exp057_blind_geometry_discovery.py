"""
EXP057: Blind Task-Geometry Discovery.
Tests whether SCPM can autonomously infer task-relevant representation geometry
without token spans, distractor locations, target locations, or structural annotations.
Pre-Registration: EXP057_BLIND_GEOMETRY_DISCOVERY_SPEC.md
Governing Laws: AGENTS.md Laws 1, 2, 6, 7, 9, 13, 14.
"""
import os, sys, json, hashlib, time, gc
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
from experiments.benchmarks.bench_005_hidden_geometry import generate_bench_005_hidden_geometry

CANONICAL_MODEL = "EleutherAI/pythia-160m"
CANONICAL_HASH  = "54c88fa4897785f2bd94b32d26de1f73f1052bcc42124d563d0cda96940de936"
TARGET_BLOCK    = 7       # Layer 8 (0-indexed Block 7)
ALPHA           = 0.25
RANK            = 2
OUT_DIR         = os.path.join(os.path.dirname(__file__),
                      "../../experiments/runs/EXP057_blind_discovery")

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

def generate_geometry_hypotheses(h_all, rank=2):
    """
    Constructs 6 candidate structural representation hypotheses purely from prompt activations.
    Zero spans, zero labels, zero metadata.
    """
    seq_len, dim = h_all.shape
    candidates = {}

    # 1. HIERARCHICAL: Position-weighted depth decay (earlier tokens weighted exponentially higher)
    weights = torch.exp(-torch.arange(seq_len, device=h_all.device, dtype=torch.float32) / float(seq_len)).unsqueeze(-1)
    h_hier = (h_all * weights) - torch.mean(h_all * weights, dim=0, keepdim=True)
    _, _, Vh_hier = torch.linalg.svd(h_hier, full_matrices=False)
    candidates["hierarchy"] = Vh_hier[:rank, :].T

    # 2. TEMPORAL: Sequential token transition differences (Delta h_t = h_t - h_{t-1})
    if seq_len > 2:
        diffs = h_all[1:, :] - h_all[:-1, :]
        diffs_cent = diffs - torch.mean(diffs, dim=0, keepdim=True)
        _, _, Vh_temp = torch.linalg.svd(diffs_cent, full_matrices=False)
        candidates["temporal"] = Vh_temp[:rank, :].T
    else:
        candidates["temporal"] = Vh_hier[:rank, :].T

    # 3. CAUSAL: Asymmetric query-context contrast direction
    # Compares final query tokens (last 20%) against antecedent context tokens
    split_pt = max(1, int(0.8 * seq_len))
    h_ctx = torch.mean(h_all[:split_pt, :], dim=0, keepdim=True)
    h_qry = torch.mean(h_all[split_pt:, :], dim=0, keepdim=True)
    v_causal = h_qry - h_ctx
    v_causal = v_causal / (torch.norm(v_causal) + 1e-8)
    # Complete to rank-2 subspace via orthogonal projection
    rem = h_all - (h_all @ v_causal.T) @ v_causal
    _, _, Vh_causal = torch.linalg.svd(rem, full_matrices=False)
    v2 = Vh_causal[:1, :].T
    candidates["causal"] = torch.cat([v_causal.T, v2], dim=-1)

    # 4. INTERACTION: Cross-token covariance of highest-variance token pairs
    norms = torch.norm(h_all - torch.mean(h_all, dim=0, keepdim=True), dim=-1)
    top_indices = torch.topk(norms, k=min(max(4, rank*2), seq_len)).indices
    h_top = h_all[top_indices, :]
    cov_int = torch.cov(h_top.T)
    _, V_int = torch.linalg.eigh(cov_int)
    candidates["interaction"] = V_int[:, -rank:]

    # 5. EXCLUSION: Subspace orthogonal to the prompt centroid (set difference)
    centroid = torch.mean(h_all, dim=0, keepdim=True)
    centroid_unit = centroid / (torch.norm(centroid) + 1e-8)
    h_orth = h_all - (h_all @ centroid_unit.T) @ centroid_unit
    _, _, Vh_excl = torch.linalg.svd(h_orth, full_matrices=False)
    candidates["exclusion"] = Vh_excl[:rank, :].T

    # 6. DISTRACTOR (Contrastive): Top SVD components of high-norm residual cluster
    h_cent = h_all - torch.mean(h_all, dim=0, keepdim=True)
    _, _, Vh_dist = torch.linalg.svd(h_cent, full_matrices=False)
    candidates["distractor"] = Vh_dist[:rank, :].T

    return candidates

def evaluate_intrinsic_sharpening(logits):
    """Computes distribution sharpening score (negative entropy)."""
    probs = F.softmax(logits, dim=-1)
    entropy = -torch.sum(probs * torch.log(probs + 1e-12)).item()
    return -entropy

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    log_file = os.path.join(OUT_DIR, "exp057_run_log.txt")
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(f"=== EXP057 Execution Started at {datetime.utcnow().isoformat()} ===\n")

    log("Initializing EXP057 Blind Task-Geometry Discovery...", log_file)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    log(f"Using compute device: {device}", log_file)

    tokenizer = AutoTokenizer.from_pretrained(CANONICAL_MODEL)
    model = AutoModelForCausalLM.from_pretrained(CANONICAL_MODEL).to(device)
    model.eval()

    pre_hash = get_hash(model)
    assert pre_hash == CANONICAL_HASH, f"Hash mismatch: {pre_hash}"
    log("Pre-run model hash verified: Delta_theta = 0.", log_file)

    dataset = generate_bench_005_hidden_geometry(n_per_geometry=20, seed=500)
    N = len(dataset)
    log(f"Generated {N} instances across 6 hidden geometries in BENCH-005.", log_file)

    methods = ["base", "rand_basis", "prompt_pca", "scpm_autonomous", "oracle_span"]
    correct_counts = {m: 0 for m in methods}
    geom_breakdown = {g: {m: 0 for m in methods} for g in ["hierarchy", "temporal", "causal", "interaction", "exclusion", "distractor"]}
    geom_totals = {g: 0 for g in geom_breakdown}
    geometry_matches = 0
    instances_log = []

    for inst in dataset:
        geom = inst["geometry"]
        geom_totals[geom] += 1
        prompt = inst["base"]
        t_str = inst["target"].strip()
        t_enc = tokenizer.encode(" " + t_str)
        t_id = t_enc[0] if t_enc else tokenizer.encode(t_str)[0]

        enc = tokenizer(prompt, return_offsets_mapping=True, return_tensors="pt")
        input_ids = enc.input_ids.to(device)

        # 1. Base Forward Pass
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
        geom_breakdown[geom]["base"] += corr_base
        base_score = evaluate_intrinsic_sharpening(logits_base)

        h_full = captured["h"]

        # 2. Control 1: Random Basis
        torch.manual_seed(hash(str(inst["id"])) % (2**31 - 1))
        Q, _ = torch.linalg.qr(torch.randn(h_full.shape[-1], RANK, device=h_full.device))
        V_rand = Q[:, :RANK]
        P_rand = (V_rand @ V_rand.T).to(h_full.device)

        def hook_rand(mod, inp, outp):
            h = outp[0].clone() if isinstance(outp, tuple) else outp.clone()
            h[0] = h[0] - ALPHA * (h[0] @ P_rand)
            return (h,) + outp[1:] if isinstance(outp, tuple) else h

        h_handle = model.gpt_neox.layers[TARGET_BLOCK].register_forward_hook(hook_rand)
        with torch.no_grad():
            logits_rand = model(input_ids=input_ids).logits[0, -1, :]
        h_handle.remove()
        pred_rand = int(torch.argmax(logits_rand).item())
        corr_rand = int(pred_rand == t_id)
        correct_counts["rand_basis"] += corr_rand
        geom_breakdown[geom]["rand_basis"] += corr_rand

        # 3. Control 2: Blind Prompt PCA (top 2 principal components of entire sequence)
        h_cent = h_full - torch.mean(h_full, dim=0, keepdim=True)
        _, _, Vh_pca = torch.linalg.svd(h_cent, full_matrices=False)
        V_pca = Vh_pca[:RANK, :].T
        P_pca = (V_pca @ V_pca.T).to(h_full.device)

        def hook_pca(mod, inp, outp):
            h = outp[0].clone() if isinstance(outp, tuple) else outp.clone()
            h[0] = h[0] - ALPHA * (h[0] @ P_pca)
            return (h,) + outp[1:] if isinstance(outp, tuple) else h

        h_handle = model.gpt_neox.layers[TARGET_BLOCK].register_forward_hook(hook_pca)
        with torch.no_grad():
            logits_pca = model(input_ids=input_ids).logits[0, -1, :]
        h_handle.remove()
        pred_pca = int(torch.argmax(logits_pca).item())
        corr_pca = int(pred_pca == t_id)
        correct_counts["prompt_pca"] += corr_pca
        geom_breakdown[geom]["prompt_pca"] += corr_pca

        # 4. SCPM Autonomous Hypothesis Lifecycle
        # Step 1: Generate hypotheses
        hypotheses = generate_geometry_hypotheses(h_full, rank=RANK)
        candidate_scores = {}
        candidate_preds = {}
        candidate_logits = {}

        # Step 2-4: Intervene & Counterfactually Evaluate
        for h_type, V_k in hypotheses.items():
            P_k = (V_k @ V_k.T).to(h_full.device)
            def hook_k(mod, inp, outp, P_mat=P_k):
                h = outp[0].clone() if isinstance(outp, tuple) else outp.clone()
                h[0] = h[0] - ALPHA * (h[0] @ P_mat)
                return (h,) + outp[1:] if isinstance(outp, tuple) else h

            h_handle = model.gpt_neox.layers[TARGET_BLOCK].register_forward_hook(hook_k)
            with torch.no_grad():
                l_k = model(input_ids=input_ids).logits[0, -1, :]
            h_handle.remove()

            candidate_logits[h_type] = l_k
            candidate_preds[h_type] = int(torch.argmax(l_k).item())
            candidate_scores[h_type] = evaluate_intrinsic_sharpening(l_k)

        # Step 5: Reject hypotheses that degrade entropy below base
        viable = {k: s for k, s in candidate_scores.items() if s >= base_score - 0.05}
        if not viable:
            viable = candidate_scores

        # Step 6: Refine top candidate via Gram-Schmidt alignment
        best_type = max(viable, key=viable.get)
        V_best = hypotheses[best_type]
        # 1-step alignment with top PCA direction
        V_aligned, _ = torch.linalg.qr(V_best + 0.1 * V_pca)
        P_auto = (V_aligned @ V_aligned.T).to(h_full.device)

        def hook_auto(mod, inp, outp):
            h = outp[0].clone() if isinstance(outp, tuple) else outp.clone()
            h[0] = h[0] - ALPHA * (h[0] @ P_auto)
            return (h,) + outp[1:] if isinstance(outp, tuple) else h

        h_handle = model.gpt_neox.layers[TARGET_BLOCK].register_forward_hook(hook_auto)
        with torch.no_grad():
            logits_auto = model(input_ids=input_ids).logits[0, -1, :]
        h_handle.remove()
        pred_auto = int(torch.argmax(logits_auto).item())
        corr_auto = int(pred_auto == t_id)
        correct_counts["scpm_autonomous"] += corr_auto
        geom_breakdown[geom]["scpm_autonomous"] += corr_auto

        if best_type == geom:
            geometry_matches += 1

        # 5. Privileged Oracle Span Reference (Contrastive distractor span)
        d_str = inst["distractor"].strip()
        offsets = enc.offset_mapping[0].tolist()
        d_pos = prompt.find(d_str)
        if d_pos != -1:
            prev_delim = max(prompt.rfind(". ", 0, d_pos), prompt.rfind("; ", 0, d_pos))
            clause_start = prev_delim + 2 if prev_delim != -1 else 0
            next_delim = prompt.find(". ", d_pos)
            q_delim = prompt.find(" Question:", d_pos)
            delims = [x for x in [next_delim, q_delim] if x != -1]
            clause_end = min(delims) if delims else len(prompt)
            d_indices = [i for i, (s, e) in enumerate(offsets) if s >= clause_start and e <= clause_end and s < e]
        else:
            d_indices = []

        if len(d_indices) < 2 and d_pos != -1:
            # Fallback: include surrounding tokens around distractor
            d_tok_idx = [i for i, (s, e) in enumerate(offsets) if s <= d_pos < e or (s >= d_pos and e <= d_pos + len(d_str))]
            if d_tok_idx:
                mid = d_tok_idx[0]
                d_indices = list(range(max(0, mid - 2), min(len(offsets), mid + 3)))

        if len(d_indices) >= 2:
            h_dist = h_full[d_indices, :]
            h_dist_cent = h_dist - torch.mean(h_dist, dim=0, keepdim=True)
            _, _, Vh_oracle = torch.linalg.svd(h_dist_cent, full_matrices=False)
            V_oracle = Vh_oracle[:RANK, :].T
            P_oracle = (V_oracle @ V_oracle.T).to(h_full.device)

            def hook_oracle(mod, inp, outp):
                h = outp[0].clone() if isinstance(outp, tuple) else outp.clone()
                h[0] = h[0] - ALPHA * (h[0] @ P_oracle)
                return (h,) + outp[1:] if isinstance(outp, tuple) else h

            h_handle = model.gpt_neox.layers[TARGET_BLOCK].register_forward_hook(hook_oracle)
            with torch.no_grad():
                logits_oracle = model(input_ids=input_ids).logits[0, -1, :]
            h_handle.remove()
            pred_oracle = int(torch.argmax(logits_oracle).item())
            corr_oracle = int(pred_oracle == t_id)
        else:
            corr_oracle = corr_base

        correct_counts["oracle_span"] += corr_oracle
        geom_breakdown[geom]["oracle_span"] += corr_oracle

        # Step 8: Complete Discard & State Cleanup
        del hypotheses, P_auto, P_rand, P_pca, candidate_logits
        gc.collect()

        instances_log.append({
            "id": inst["id"],
            "geometry": geom,
            "selected_geometry": best_type,
            "corr_base": corr_base,
            "corr_rand": corr_rand,
            "corr_pca": corr_pca,
            "corr_auto": corr_auto,
            "corr_oracle": corr_oracle
        })

    # Summary & Metric Calculations
    acc_base   = correct_counts["base"] / N
    acc_rand   = correct_counts["rand_basis"] / N
    acc_pca    = correct_counts["prompt_pca"] / N
    acc_auto   = correct_counts["scpm_autonomous"] / N
    acc_oracle = correct_counts["oracle_span"] / N

    rdg = (acc_oracle - acc_auto) * 100.0
    delta_auto = (acc_auto - acc_base) * 100.0
    b_auto = sum(1 for x in instances_log if x["corr_base"] == 0 and x["corr_auto"] == 1)
    c_auto = sum(1 for x in instances_log if x["corr_base"] == 1 and x["corr_auto"] == 0)
    p_mcnemar = mcnemar_p(b_auto, c_auto)
    geom_match_rate = (geometry_matches / N) * 100.0

    log("\n================ EXP057 BLIND GEOMETRY DISCOVERY SUMMARY (N=120) ================", log_file)
    log(f"Base Accuracy:            {acc_base*100:.1f}% ({correct_counts['base']}/{N})", log_file)
    log(f"Random Basis (Ctrl 1):    {acc_rand*100:.1f}% ({correct_counts['rand_basis']}/{N})", log_file)
    log(f"Prompt PCA   (Ctrl 2):    {acc_pca*100:.1f}% ({correct_counts['prompt_pca']}/{N})", log_file)
    log(f"SCPM Autonomous (Blind):  {acc_auto*100:.1f}% ({correct_counts['scpm_autonomous']}/{N}) [Delta_M={delta_auto:+.1f} pp, Rescues={b_auto}, Corr={c_auto}, p={p_mcnemar:.4f}]", log_file)
    log(f"Oracle Span Reference:    {acc_oracle*100:.1f}% ({correct_counts['oracle_span']}/{N})", log_file)
    log(f"Representation Discovery Gap (RDG): {rdg:.1f} percentage points", log_file)
    log(f"Geometry Inference Match Rate:     {geom_match_rate:.1f}% (Chance expectation = 16.7%)", log_file)

    log("\n--- Breakdown by Geometry (N=20 each) ---", log_file)
    for g, counts in geom_breakdown.items():
        g_n = geom_totals[g]
        log(f"{g.upper():<12}: Base={counts['base']/g_n*100:.1f}%, PCA={counts['prompt_pca']/g_n*100:.1f}%, Auto={counts['scpm_autonomous']/g_n*100:.1f}%, Oracle={counts['oracle_span']/g_n*100:.1f}%", log_file)

    post_hash = get_hash(model)
    assert post_hash == pre_hash, "Backbone altered!"
    log("\nBackbone immutability verified: Delta_theta = 0.", log_file)

    criteria_passed = (
        acc_auto > max(acc_rand, acc_pca) and
        p_mcnemar < 0.05 and
        rdg < 10.0 and
        geom_match_rate > 20.0
    )
    verdict = "AUTONOMOUS_DISCOVERY_SUPPORTED" if criteria_passed else "DISCOVERY_BOTTLENECK_PERSISTS"
    log(f"\nFinal Audit Verdict: >>> {verdict} <<<", log_file)

    final_payload = {
        "metadata": {
            "experiment": "EXP057",
            "title": "Blind Task-Geometry Discovery",
            "timestamp": datetime.utcnow().isoformat(),
            "model": CANONICAL_MODEL,
            "target_block": TARGET_BLOCK,
            "alpha": ALPHA,
            "rank": RANK,
            "total_instances": N,
            "rdg_percentage_points": float(rdg),
            "geom_match_rate": float(geom_match_rate),
            "verdict": verdict
        },
        "accuracies": {m: float(correct_counts[m] / N) for m in methods},
        "breakdown": geom_breakdown,
        "instances": instances_log
    }

    out_file = os.path.join(OUT_DIR, "exp057_discovery_results.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(final_payload, f, indent=2)
    log(f"Saved complete results to {out_file}", log_file)

if __name__ == "__main__":
    main()
