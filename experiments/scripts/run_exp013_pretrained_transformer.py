"""
EXP013: Pretrained Transformer Representation Search & Evaluator Transfer Study
Executes full Phase B confirmatory evaluation on GPT-2 (124M) and BENCH-002-NL.

Evaluates:
- Primary Analysis (Design A): Layer-by-layer across L in {2, 4, 6, 8, 10}
- Secondary Analysis (Design B): Pooled model-level search C = {(l, k)}
- Complete Evaluation Ladder:
  Identity Baseline -> Random Projection -> Random Selection -> E_energy -> E_CF -> Oracle Ceiling
- Rigorous compute accounting: N_forward, N_tokens, candidate evaluations, wall-clock time
"""
import time
import json
import hashlib
import os
import sys
import argparse
import torch
import torch.nn.functional as F
import numpy as np
from scipy import stats
from transformers import AutoTokenizer, AutoModelForCausalLM
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from experiments.benchmarks.bench_002_nl import generate_bench_002_nl

def get_param_hash(model):
    h = hashlib.sha256()
    for p in model.parameters():
        h.update(p.detach().cpu().numpy().tobytes())
    return h.hexdigest()

def js_divergence(p, q):
    """Calculates Jensen-Shannon divergence in nats across vocabulary."""
    m = 0.5 * (p + q)
    kl_pm = F.kl_div(m.log(), p, reduction="sum")
    kl_qm = F.kl_div(m.log(), q, reduction="sum")
    return (0.5 * (kl_pm + kl_qm)).item()

def bootstrap_ci(vals, n_boot=2000, seed=42):
    rng = np.random.RandomState(seed)
    n = len(vals)
    if n == 0:
        return 0.0, 0.0
    boot_means = [np.mean(rng.choice(vals, size=n, replace=True)) for _ in range(n_boot)]
    return float(np.percentile(boot_means, 2.5)), float(np.percentile(boot_means, 97.5))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n_instances", type=int, default=100, help="Number of benchmark instances")
    args = parser.parse_args()

    print("=" * 80)
    print(f"EXP013: PRETRAINED TRANSFORMER REPRESENTATION SEARCH & EVALUATOR TRANSFER (N={args.n_instances})")
    print("=" * 80)
    start_time = time.time()
    
    # 1. Load Model & Tokenizer
    tokenizer = AutoTokenizer.from_pretrained("gpt2")
    model = AutoModelForCausalLM.from_pretrained("gpt2")
    model.eval()
    
    pre_hash = get_param_hash(model)
    print(f"[REPRODUCIBILITY] Pre-run GPT-2 Parameter Hash (SHA-256): {pre_hash}")
    
    # 2. Load BENCH-002-NL Dataset
    dataset = generate_bench_002_nl(n_instances=args.n_instances, seed=42)
    print(f"[DATASET] Loaded BENCH-002-NL: N={len(dataset)} instances across 5 relational domains.")
    
    layers = [2, 4, 6, 8, 10]
    rank = 2
    total_forwards = 0
    total_tokens = 0
    candidate_eval_count = 0
    
    # Store results per layer and overall
    layer_results = {l: {
        "identity": [],
        "fixed_k1": [],
        "random_proj": [],
        "random_select": [],
        "energy": [],
        "ecf": [],
        "oracle": [],
        "identity_pref": [],
        "fixed_k1_pref": [],
        "random_proj_pref": [],
        "random_select_pref": [],
        "energy_pref": [],
        "ecf_pref": [],
        "oracle_pref": [],
        "prob_target_id": [],
        "prob_target_ecf": [],
        "prob_target_oracle": [],
        "is_disc_top1": [],
        "is_disc_pref": [],
        "pairwise_r_top1": [],
        "pairwise_r_pref": [],
        "candidate_diversity": []
    } for l in layers}
    
    all_candidates_pooled = [] # For Design B
    
    print("\nStarting execution across N=100 instances and L={2, 4, 6, 8, 10}...")
    
    for idx, inst in enumerate(dataset):
        base_text = inst["base"]
        pos_text = inst["pos"]
        neg_text = inst["neg"]
        target_token = inst["target_token"]
        
        target_id = tokenizer.encode(target_token)[0]
        distractor_token = inst["distractor_token"]
        dist_id = tokenizer.encode(distractor_token)[0]
        
        inputs_base = tokenizer(base_text, return_tensors="pt")
        inputs_pos = tokenizer(pos_text, return_tensors="pt")
        inputs_neg = tokenizer(neg_text, return_tensors="pt")
        
        seq_len = inputs_base["input_ids"].shape[1]
        total_tokens += seq_len * 3
        
        # Base forward pass (Identity)
        with torch.no_grad():
            out_base = model(**inputs_base, output_hidden_states=True)
            total_forwards += 1
            
        base_logits = out_base.logits[0, -1]
        base_probs = F.softmax(base_logits, dim=-1)
        base_pred_id = torch.argmax(base_logits).item()
        base_correct = (base_pred_id == target_id)
        prob_target_base = base_probs[target_id].item()
        
        # 2. Strict Label-Free Candidate Generator (Zero Semantic Segmentation / Zero Labels)
        # Slices hidden states into K=4 equal temporal quartiles: B_k = [(k-1)*T/4 : k*T/4]
        def generate_label_free_candidates(h, rank=2):
            seq_len = h.shape[0]
            q_size = seq_len // 4
            cands = []
            for k in range(4):
                start = k * q_size
                end = (k + 1) * q_size if k < 3 else seq_len
                slice_h = h[start:end]
                if slice_h.shape[0] < rank:
                    v, _ = torch.linalg.qr(torch.randn(h.shape[1], rank))
                else:
                    v = torch.linalg.svd(slice_h, full_matrices=False).Vh[:rank].T
                cands.append(v)
            return cands
            
        inst_pooled_candidates = []
        
        for l in layers:
            # Explicit layer index mapping: hidden_states[l] matches output of transformer block l-1
            h_l = out_base.hidden_states[l][0] # [seq_len, 768]
            
            # 1. Random Orthogonal Control V_rand
            q_rand, _ = torch.linalg.qr(torch.randn(768, rank))
            V_rand = q_rand
            
            # 2. Label-free SVD Candidate Subspaces (V1, V2, V3, V4)
            cand_V_list = generate_label_free_candidates(h_l, rank=rank)
            candidate_eval_count += len(cand_V_list) + 1
            
            # 3. Normalized Candidate Diversity Metric: D(Pi, Pj) = ||Pi - Pj||_F / sqrt(2*r)
            divs = []
            for ca in range(len(cand_V_list)):
                for cb in range(ca + 1, len(cand_V_list)):
                    Va = cand_V_list[ca]
                    Vb = cand_V_list[cb]
                    # Compute ||Va Va^T - Vb Vb^T||_F = sqrt(2*r - 2*||Va^T Vb||_F^2)
                    overlap = torch.norm(Va.T @ Vb).item()**2
                    frob_dist = np.sqrt(max(2 * rank - 2 * overlap, 0.0))
                    norm_dist = frob_dist / np.sqrt(2 * rank)
                    divs.append(norm_dist)
            mean_cand_div = float(np.mean(divs))
            min_cand_div = float(np.min(divs))
            max_cand_div = float(np.max(divs))
            layer_results[l]["candidate_diversity"].append(mean_cand_div)
            
            # Non-materialized Forward hook evaluator helper (Primary Scope: All-Token Intervention)
            def evaluate_projection_V(V):
                def hook_fn(module, input, output):
                    h = output[0].clone()
                    # Non-materialized projection: H_proj = H - (H @ V) @ V^T
                    h_proj = h - torch.matmul(torch.matmul(h, V), V.T)
                    return (h_proj, *output[1:])
                
                handle = model.transformer.h[l - 1].register_forward_hook(hook_fn)
                with torch.no_grad():
                    o_b = model(**inputs_base)
                    o_p = model(**inputs_pos)
                    o_n = model(**inputs_neg)
                handle.remove()
                
                nonlocal total_forwards
                total_forwards += 3
                
                qb = F.softmax(o_b.logits[0, -1], dim=-1)
                qp = F.softmax(o_p.logits[0, -1], dim=-1)
                qn = F.softmax(o_n.logits[0, -1], dim=-1)
                
                pred_id = torch.argmax(o_b.logits[0, -1]).item()
                is_correct = (pred_id == target_id)
                p_target = qb[target_id].item()
                p_dist = qb[dist_id].item()
                prefers_target = (p_target > p_dist)
                
                d_pos = js_divergence(qb, qp)
                d_neg = js_divergence(qb, qn)
                e_cf = d_pos - 0.5 * d_neg
                
                # Directional NLL (Secondary Diagnostic)
                nll_b = -torch.log(qb[target_id] + 1e-12).item()
                nll_p = -torch.log(qp[target_id] + 1e-12).item()
                nll_n = -torch.log(qn[target_id] + 1e-12).item()
                dnll_pos = nll_p - nll_b
                dnll_neg = nll_n - nll_b
                
                # Energy score (energy removed)
                removed_energy = torch.norm(torch.matmul(h_l, V)).item() / max(torch.norm(h_l).item(), 1e-8)
                
                return {
                    "is_correct": is_correct,
                    "prefers_target": prefers_target,
                    "p_target": p_target,
                    "p_dist": p_dist,
                    "e_cf": e_cf,
                    "dnll_pos": dnll_pos,
                    "dnll_neg": dnll_neg,
                    "e_energy": removed_energy
                }
            
            # Evaluate Random Projection Control
            res_rand_proj = evaluate_projection_V(V_rand)
            layer_results[l]["random_proj"].append(res_rand_proj["is_correct"])
            layer_results[l]["random_proj_pref"].append(res_rand_proj["prefers_target"])
            
            # Evaluate K=4 Label-Free SVD candidates
            cand_evals = [evaluate_projection_V(V) for V in cand_V_list]
            
            # Record ladder selections:
            # 1. Identity
            base_pref = (base_probs[target_id].item() > base_probs[dist_id].item())
            layer_results[l]["identity"].append(base_correct)
            layer_results[l]["identity_pref"].append(base_pref)
            layer_results[l]["prob_target_id"].append(prob_target_base)
            
            # 2. Fixed Candidate Baseline (k=1: fixed first temporal quartile)
            layer_results[l]["fixed_k1"].append(cand_evals[0]["is_correct"])
            layer_results[l]["fixed_k1_pref"].append(cand_evals[0]["prefers_target"])
            
            # 3. Random Candidate Selection
            rng_k = np.random.randint(0, len(cand_V_list))
            layer_results[l]["random_select"].append(cand_evals[rng_k]["is_correct"])
            layer_results[l]["random_select_pref"].append(cand_evals[rng_k]["prefers_target"])
            
            # 3. Intrinsic Energy Selection (minimize reconstruction loss)
            best_energy_k = int(np.argmin([ce["e_energy"] for ce in cand_evals]))
            layer_results[l]["energy"].append(cand_evals[best_energy_k]["is_correct"])
            layer_results[l]["energy_pref"].append(cand_evals[best_energy_k]["prefers_target"])
            
            # 4. E_CF Selection (minimize E_CF: high stability under pos, high sensitivity under neg)
            best_ecf_k = int(np.argmin([ce["e_cf"] for ce in cand_evals]))
            layer_results[l]["ecf"].append(cand_evals[best_ecf_k]["is_correct"])
            layer_results[l]["ecf_pref"].append(cand_evals[best_ecf_k]["prefers_target"])
            layer_results[l]["prob_target_ecf"].append(cand_evals[best_ecf_k]["p_target"])
            
            # 5. Oracle Ceiling (argmax over correctness and preference)
            any_correct = any([ce["is_correct"] for ce in cand_evals])
            any_pref = any([ce["prefers_target"] for ce in cand_evals])
            layer_results[l]["oracle"].append(any_correct)
            layer_results[l]["oracle_pref"].append(any_pref)
            best_oracle_k = int(np.argmax([ce["p_target"] for ce in cand_evals]))
            # Record Discriminatory Indicators & Pairwise Ranking Ri
            is_disc_top1 = (len(set([ce["is_correct"] for ce in cand_evals])) > 1)
            is_disc_pref = (len(set([ce["prefers_target"] for ce in cand_evals])) > 1)
            layer_results[l]["is_disc_top1"].append(is_disc_top1)
            layer_results[l]["is_disc_pref"].append(is_disc_pref)
            
            if is_disc_top1:
                pairs_t = []
                for ca in range(len(cand_evals)):
                    for cb in range(len(cand_evals)):
                        if cand_evals[ca]["is_correct"] and not cand_evals[cb]["is_correct"]:
                            pairs_t.append(1.0 if cand_evals[ca]["e_cf"] < cand_evals[cb]["e_cf"] else (0.5 if cand_evals[ca]["e_cf"] == cand_evals[cb]["e_cf"] else 0.0))
                layer_results[l]["pairwise_r_top1"].append(float(np.mean(pairs_t)))
                
            if is_disc_pref:
                pairs_p = []
                for ca in range(len(cand_evals)):
                    for cb in range(len(cand_evals)):
                        if cand_evals[ca]["prefers_target"] and not cand_evals[cb]["prefers_target"]:
                            pairs_p.append(1.0 if cand_evals[ca]["e_cf"] < cand_evals[cb]["e_cf"] else (0.5 if cand_evals[ca]["e_cf"] == cand_evals[cb]["e_cf"] else 0.0))
                layer_results[l]["pairwise_r_pref"].append(float(np.mean(pairs_p)))
            
            # For Design B (Pooled Search)
            for ck_i, ce in enumerate(cand_evals):
                inst_pooled_candidates.append({
                    "layer": l,
                    "k": ck_i,
                    "is_correct": ce["is_correct"],
                    "prefers_target": ce["prefers_target"],
                    "e_energy": ce["e_energy"],
                    "e_cf": ce["e_cf"],
                    "p_target": ce["p_target"]
                })
                
        all_candidates_pooled.append(inst_pooled_candidates)
        
        if (idx + 1) % 10 == 0 or idx == len(dataset) - 1:
            print(f"Processed {idx + 1}/{len(dataset)} instances... ({time.time() - start_time:.1f}s)")

    # 3. Post-Run Verification of Frozen Model
    post_hash = get_param_hash(model)
    checksums_match = (pre_hash == post_hash)
    print(f"\n[REPRODUCIBILITY] Post-run GPT-2 Parameter Hash: {post_hash}")
    print(f"[REPRODUCIBILITY] Parameter Cheksum Match (Delta_theta = 0): {checksums_match}")
    assert checksums_match, "CRITICAL ERROR: Backbone model weights modified during inference!"
    
    elapsed_time = time.time() - start_time
    
    # 4. Statistical Analysis & Reporting
    print("\n" + "=" * 80)
    print("PRIMARY CONFIRMATORY ANALYSIS (DESIGN A: LAYER-BY-LAYER)")
    print("=" * 80)
    print(f"{'Layer':<6} | {'Identity':<9} | {'RandProj':<9} | {'RandSelect':<10} | {'E_energy':<9} | {'E_CF':<9} | {'Oracle':<8} | {'Delta(ECF-R)':<12} | {'p-value':<8}")
    print("-" * 90)
    
    summary_design_a = {}
    
    for l in layers:
        m_id = np.mean(layer_results[l]["identity"])
        m_k1 = np.mean(layer_results[l]["fixed_k1"])
        m_rp = np.mean(layer_results[l]["random_proj"])
        m_rs = np.mean(layer_results[l]["random_select"])
        m_en = np.mean(layer_results[l]["energy"])
        m_cf = np.mean(layer_results[l]["ecf"])
        m_or = np.mean(layer_results[l]["oracle"])
        delta = m_cf - m_rs
        
        pref_id = np.mean(layer_results[l]["identity_pref"])
        pref_k1 = np.mean(layer_results[l]["fixed_k1_pref"])
        pref_rp = np.mean(layer_results[l]["random_proj_pref"])
        pref_rs = np.mean(layer_results[l]["random_select_pref"])
        pref_en = np.mean(layer_results[l]["energy_pref"])
        pref_cf = np.mean(layer_results[l]["ecf_pref"])
        pref_or = np.mean(layer_results[l]["oracle_pref"])
        delta_pref = pref_cf - pref_rs
        
        diffs = np.array(layer_results[l]["ecf"], dtype=float) - np.array(layer_results[l]["random_select"], dtype=float)
        diffs_pref = np.array(layer_results[l]["ecf_pref"], dtype=float) - np.array(layer_results[l]["random_select_pref"], dtype=float)
        
        if np.all(diffs == 0):
            p_val = 1.0
        else:
            try:
                p_val = stats.wilcoxon(layer_results[l]["ecf"], layer_results[l]["random_select"], alternative="greater").pvalue
            except Exception:
                p_val = 1.0
                
        if np.all(diffs_pref == 0):
            p_val_pref = 1.0
        else:
            try:
                p_val_pref = stats.wilcoxon(layer_results[l]["ecf_pref"], layer_results[l]["random_select_pref"], alternative="greater").pvalue
            except Exception:
                p_val_pref = 1.0
                
        ci_rs = bootstrap_ci(layer_results[l]["random_select"])
        ci_cf = bootstrap_ci(layer_results[l]["ecf"])
        ci_delta = bootstrap_ci(diffs)
        
        n_disc_top1 = int(np.sum(layer_results[l]["is_disc_top1"]))
        n_disc_pref = int(np.sum(layer_results[l]["is_disc_pref"]))
        mean_r_top1 = float(np.mean(layer_results[l]["pairwise_r_top1"])) if len(layer_results[l]["pairwise_r_top1"]) > 0 else 0.5
        mean_r_pref = float(np.mean(layer_results[l]["pairwise_r_pref"])) if len(layer_results[l]["pairwise_r_pref"]) > 0 else 0.5
        ci_r_pref = bootstrap_ci(layer_results[l]["pairwise_r_pref"]) if len(layer_results[l]["pairwise_r_pref"]) > 0 else (0.5, 0.5)
        
        print(f"L={l:<4} (Top1)| ID={m_id:.3f} | K1={m_k1:.3f} | RandProj={m_rp:.3f} | RandSel={m_rs:.3f} | Energy={m_en:.3f} | E_CF={m_cf:.3f} | Oracle={m_or:.3f} | Delta={delta:+.3f} | p={p_val:.4f} (N_disc={n_disc_top1})")
        print(f"L={l:<4} (Pref)| ID={pref_id:.3f} | K1={pref_k1:.3f} | RandProj={pref_rp:.3f} | RandSel={pref_rs:.3f} | Energy={pref_en:.3f} | E_CF={pref_cf:.3f} | Oracle={pref_or:.3f} | Delta={delta_pref:+.3f} | p={p_val_pref:.4f} (N_disc={n_disc_pref}, R_pref={mean_r_pref:.3f})")
        
        summary_design_a[l] = {
            "n_total": len(dataset),
            "n_disc_top1": n_disc_top1,
            "n_disc_pref": n_disc_pref,
            "primary_endpoint_delta": float(delta),
            "primary_endpoint_delta_ci": ci_delta,
            "primary_endpoint_wilcoxon_p": float(p_val),
            "m_identity": float(m_id),
            "m_fixed_k1": float(m_k1),
            "m_rand_proj": float(m_rp),
            "m_rand_select": float(m_rs),
            "m_rand_select_ci": ci_rs,
            "m_energy": float(m_en),
            "m_ecf": float(m_cf),
            "m_ecf_ci": ci_cf,
            "m_oracle": float(m_or),
            "pref_identity": float(pref_id),
            "pref_fixed_k1": float(pref_k1),
            "pref_rand_proj": float(pref_rp),
            "pref_rand_select": float(pref_rs),
            "pref_energy": float(pref_en),
            "pref_ecf": float(pref_cf),
            "pref_oracle": float(pref_or),
            "delta_pref": float(delta_pref),
            "wilcoxon_p_pref": float(p_val_pref),
            "pairwise_r_top1": mean_r_top1,
            "pairwise_r_pref": mean_r_pref,
            "pairwise_r_pref_ci": ci_r_pref,
            "mean_candidate_diversity": float(np.mean(layer_results[l]["candidate_diversity"]))
        }

    # 5. Secondary Analysis (Design B: Model-Level Pooled Search Space)
    print("\n" + "=" * 80)
    print("SECONDARY ANALYSIS (DESIGN B: MODEL-LEVEL POOLED SEARCH SPACE |C| = 5x4 = 20)")
    print("=" * 80)
    
    b_rand_select = []
    b_energy_select = []
    b_ecf_select = []
    b_oracle_select = []
    
    b_rand_pref = []
    b_energy_pref = []
    b_ecf_pref = []
    b_oracle_pref = []
    
    for inst_cands in all_candidates_pooled:
        rk = np.random.randint(0, len(inst_cands))
        b_rand_select.append(inst_cands[rk]["is_correct"])
        b_rand_pref.append(inst_cands[rk]["prefers_target"])
        
        be_k = int(np.argmin([c["e_energy"] for c in inst_cands]))
        b_energy_select.append(inst_cands[be_k]["is_correct"])
        b_energy_pref.append(inst_cands[be_k]["prefers_target"])
        
        bcf_k = int(np.argmin([c["e_cf"] for c in inst_cands]))
        b_ecf_select.append(inst_cands[bcf_k]["is_correct"])
        b_ecf_pref.append(inst_cands[bcf_k]["prefers_target"])
        
        b_oracle_select.append(any([c["is_correct"] for c in inst_cands]))
        b_oracle_pref.append(any([c["prefers_target"] for c in inst_cands]))
        
    m_b_id = np.mean(layer_results[layers[0]]["identity"])
    m_b_rs = np.mean(b_rand_select)
    m_b_en = np.mean(b_energy_select)
    m_b_cf = np.mean(b_ecf_select)
    m_b_or = np.mean(b_oracle_select)
    delta_b = m_b_cf - m_b_rs
    
    try:
        p_val_b = stats.wilcoxon(b_ecf_select, b_rand_select, alternative="greater").pvalue
    except Exception:
        p_val_b = 1.0
        
    print(f"Identity Baseline:      {m_b_id:.3f}")
    print(f"Random Selection (|C|): {m_b_rs:.3f}")
    print(f"Energy Selection:       {m_b_en:.3f}")
    print(f"E_CF Selection:         {m_b_cf:.3f}")
    print(f"Oracle Ceiling (|C|):   {m_b_or:.3f}")
    print(f"Delta (E_CF - Random):  {delta_b:+.3f} (Wilcoxon p = {p_val_b:.4f})")
    
    # 6. Compute Accounting
    print("\n" + "=" * 80)
    print("COMPUTE ACCOUNTING AUDIT")
    print("=" * 80)
    print(f"Total Forward Passes (N_forward):     {total_forwards}")
    print(f"Total Processed Tokens (N_tokens):     {total_tokens}")
    print(f"Total Candidate Projections Evaluated: {candidate_eval_count}")
    print(f"Wall-Clock Execution Time:             {elapsed_time:.2f} s ({elapsed_time/60:.2f} min)")
    print(f"Average Latency per Instance:          {elapsed_time/len(dataset):.2f} s")
    
    # 7. Save Artifacts
    results_payload = {
        "metadata": {
            "protocol": "EXP013",
            "model": "gpt2 (124M)",
            "pre_hash": pre_hash,
            "post_hash": post_hash,
            "checksums_match": checksums_match,
            "dataset": "BENCH-002-NL",
            "n_instances": len(dataset),
            "layers": layers,
            "rank": rank,
            "compute": {
                "total_forwards": total_forwards,
                "total_tokens": total_tokens,
                "candidate_eval_count": candidate_eval_count,
                "wall_clock_seconds": elapsed_time
            }
        },
        "design_a": summary_design_a,
        "design_b": {
            "m_identity": float(m_b_id),
            "m_rand_select": float(m_b_rs),
            "m_energy": float(m_b_en),
            "m_ecf": float(m_b_cf),
            "m_oracle": float(m_b_or),
            "delta": float(delta_b),
            "p_value": float(p_val_b)
        }
    }
    
    os.makedirs("experiments/runs/EXP013_pretrained", exist_ok=True)
    out_file = "experiments/runs/EXP013_pretrained/exp013_results.json"
    with open(out_file, "w") as f:
        json.dump(results_payload, f, indent=2)
    print(f"\n[OUTPUT] Saved complete EXP013 results payload to: {out_file}")

if __name__ == "__main__":
    main()
