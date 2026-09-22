"""
run_exp014_stage1_headroom.py: EXP014 Stage 1 Oracle Headroom Sweep
Tests less-destructive representation transformation operators on frozen GPT-2 (124M).

Pre-Registered Design:
- Model: GPT-2 (124M), frozen parameters verified via SHA-256 (Delta_theta = 0)
- Benchmark: BENCH-002-NL (N=100, seed 42)
- Fixed candidate generator: Layer 10 (block 9), K=4 temporal quartiles, rank r=2 SVD
- 2 Scopes: S_query (query token only) vs S_all (all tokens)
- 5 Alphas: {0.05, 0.10, 0.25, 0.50, 1.00}
- Baseline Control: alpha = 0 (Identity)
- Multiple-comparison family: 10 nontrivial configurations with Holm FWER correction
- Exact paired binary contingency table & binomial tests vs Identity
"""
import os
import sys
import json
import time
import hashlib
import argparse
import numpy as np
import torch
import torch.nn.functional as F
from scipy import stats
from transformers import AutoTokenizer, AutoModelForCausalLM

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from experiments.benchmarks.bench_002_nl import generate_bench_002_nl

def get_param_hash(model):
    h = hashlib.sha256()
    for p in model.parameters():
        h.update(p.detach().cpu().numpy().tobytes())
    return h.hexdigest()

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

def bootstrap_ci(vals, n_boot=2000, seed=42):
    rng = np.random.RandomState(seed)
    n = len(vals)
    if n == 0:
        return 0.0, 0.0
    boot_means = [np.mean(rng.choice(vals, size=n, replace=True)) for _ in range(n_boot)]
    return float(np.percentile(boot_means, 2.5)), float(np.percentile(boot_means, 97.5))

def holm_adjust(p_vals):
    """Applies Holm-Bonferroni step-down FWER adjustment."""
    m = len(p_vals)
    indexed = sorted(enumerate(p_vals), key=lambda x: x[1])
    adjusted = [0.0] * m
    running_max = 0.0
    for rank, (orig_idx, p) in enumerate(indexed):
        # Step-down multiplier: (m - rank)
        adj_p = min(1.0, (m - rank) * p)
        running_max = max(running_max, adj_p)
        adjusted[orig_idx] = running_max
    return adjusted

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n_instances", type=int, default=100)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    print("=" * 80)
    print("EXP014 STAGE 1: LESS-DESTRUCTIVE OPERATORS — ORACLE HEADROOM SWEEP")
    print(f"Configurations: 2 Scopes x 5 Alphas = 10 Multiple-Comparison Family (N={args.n_instances})")
    print("=" * 80)
    
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    start_time = time.time()
    
    # 1. Load Model & Tokenizer
    tokenizer = AutoTokenizer.from_pretrained("gpt2")
    model = AutoModelForCausalLM.from_pretrained("gpt2")
    model.eval()
    
    pre_hash = get_param_hash(model)
    print(f"[REPRODUCIBILITY] Pre-run GPT-2 Parameter Hash (SHA-256): {pre_hash}")
    
    # 2. Load BENCH-002-NL Dataset
    dataset = generate_bench_002_nl(n_instances=args.n_instances, seed=args.seed)
    print(f"[DATASET] Loaded {len(dataset)} benchmark instances.")
    
    layer_idx = 10
    block_idx = layer_idx - 1 # block 9
    rank = 2
    scopes = ["query", "all"]
    alphas = [0.05, 0.10, 0.25, 0.50, 1.00]
    
    # Tracking containers
    identity_correct = []
    identity_pref = []
    
    # Key: (scope, alpha) -> list of instance results dicts
    config_records = {(s, a): [] for s in scopes for a in alphas}
    
    total_forwards = 0
    
    print("\nStarting execution across N=100 instances...")
    for idx, inst in enumerate(dataset):
        base_text = inst["base"]
        target_token = inst["target_token"]
        distractor_token = inst["distractor_token"]
        
        target_id = tokenizer.encode(target_token)[0]
        dist_id = tokenizer.encode(distractor_token)[0]
        inputs_base = tokenizer(base_text, return_tensors="pt")
        
        # 1. Unmodified Baseline (Identity: alpha=0)
        with torch.no_grad():
            out_base = model(**inputs_base, output_hidden_states=True)
            total_forwards += 1
            
        base_logits = out_base.logits[0, -1]
        base_probs = F.softmax(base_logits, dim=-1)
        base_pred_id = torch.argmax(base_logits).item()
        base_corr = (base_pred_id == target_id)
        base_p_target = base_probs[target_id].item()
        base_p_dist = base_probs[dist_id].item()
        base_pr = (base_p_target > base_p_dist)
        
        identity_correct.append(base_corr)
        identity_pref.append(base_pr)
        
        # 2. Generate K=4 Temporal Quartile Candidates at Layer 10
        h_l = out_base.hidden_states[layer_idx][0] # [seq_len, 768]
        cand_V_list = generate_label_free_candidates(h_l, rank=rank)
        
        # 3. Sweep across 2 Scopes x 5 Alphas
        for scope in scopes:
            for alpha in alphas:
                cand_corrs = []
                cand_prefs = []
                cand_p_targets = []
                
                for V in cand_V_list:
                    def hook_fn(module, input, output):
                        h = output[0].clone()
                        if scope == "query":
                            # Modify ONLY the final-token representation in the residual stream
                            h[:, -1, :] = h[:, -1, :] - alpha * torch.matmul(torch.matmul(h[:, -1, :], V), V.T)
                        else: # "all"
                            # Modify all sequence tokens
                            h = h - alpha * torch.matmul(torch.matmul(h, V), V.T)
                        return (h, *output[1:])
                    
                    handle = model.transformer.h[block_idx].register_forward_hook(hook_fn)
                    with torch.no_grad():
                        o_cand = model(**inputs_base)
                        total_forwards += 1
                    handle.remove()
                    
                    cand_logits = o_cand.logits[0, -1]
                    cand_probs = F.softmax(cand_logits, dim=-1)
                    cand_pred_id = torch.argmax(cand_logits).item()
                    
                    c_corr = (cand_pred_id == target_id)
                    c_pt = cand_probs[target_id].item()
                    c_pd = cand_probs[dist_id].item()
                    c_pr = (c_pt > c_pd)
                    
                    cand_corrs.append(c_corr)
                    cand_prefs.append(c_pr)
                    cand_p_targets.append(c_pt)
                    
                # Oracle: any candidate correct
                oracle_corr = any(cand_corrs)
                oracle_pr = any(cand_prefs)
                
                # Random selection (seed-controlled choice)
                rk = np.random.randint(0, len(cand_corrs))
                rand_corr = cand_corrs[rk]
                rand_pr = cand_prefs[rk]
                
                # Expected random (analytical mean over 4 candidates)
                exp_rand_corr = float(np.mean(cand_corrs))
                
                config_records[(scope, alpha)].append({
                    "inst_idx": idx,
                    "cand_corrs": cand_corrs,
                    "cand_prefs": cand_prefs,
                    "oracle_corr": oracle_corr,
                    "oracle_pref": oracle_pr,
                    "rand_corr": rand_corr,
                    "rand_pref": rand_pr,
                    "exp_rand_corr": exp_rand_corr
                })
                
        if (idx + 1) % 10 == 0 or idx == len(dataset) - 1:
            print(f"Processed {idx + 1}/{len(dataset)} instances... ({time.time() - start_time:.1f}s)")
            
    # 4. Post-run parameter verification
    post_hash = get_param_hash(model)
    checksums_match = (pre_hash == post_hash)
    print(f"\n[REPRODUCIBILITY] Post-run GPT-2 Parameter Hash: {post_hash}")
    print(f"[REPRODUCIBILITY] Parameter Checksum Match (Delta_theta = 0): {checksums_match}")
    assert checksums_match, "CRITICAL ERROR: Foundation model parameters modified!"
    
    elapsed_time = time.time() - start_time
    print(f"Total Forward Passes: {total_forwards} in {elapsed_time:.1f}s ({elapsed_time/len(dataset):.2f}s/inst)")
    
    # 5. Statistical Multiplicity Analysis across 10 Configurations
    id_arr = np.array(identity_correct, dtype=int)
    m_id = float(np.mean(id_arr))
    pref_id = float(np.mean(identity_pref))
    print("\n" + "=" * 100)
    print(f"EXP014 STAGE 1 HEADROOM SWEEP RESULTS (Identity Baseline M_ID = {m_id:.3f}, Pref_ID = {pref_id:.3f})")
    print("=" * 100)
    print(f"{'Config':<18} | {'Scope':<8} | {'Alpha':<6} | {'M_Oracle':<9} | {'M_Random':<9} | {'Delta_Or':<10} | {'95% Boot CI':<16} | {'b (win)':<7} | {'c (loss)':<8} | {'p_raw':<8} | {'p_Holm':<8}")
    print("-" * 125)
    
    raw_p_values = []
    config_keys = [(s, a) for s in scopes for a in alphas]
    summary_data = []
    
    for (scope, alpha) in config_keys:
        recs = config_records[(scope, alpha)]
        or_arr = np.array([r["oracle_corr"] for r in recs], dtype=int)
        rd_arr = np.array([r["rand_corr"] for r in recs], dtype=int)
        
        m_or = float(np.mean(or_arr))
        m_rd = float(np.mean(rd_arr))
        diffs = or_arr - id_arr
        delta_or = float(np.mean(diffs))
        ci_delta = bootstrap_ci(diffs)
        
        # Paired contingency table vs Identity:
        # b: Oracle=1, Identity=0 (positive headroom instances)
        # c: Oracle=0, Identity=1 (regressed instances)
        b = int(np.sum((or_arr == 1) & (id_arr == 0)))
        c = int(np.sum((or_arr == 0) & (id_arr == 1)))
        
        n_disc = b + c
        if n_disc > 0:
            p_raw = float(stats.binomtest(b, n_disc, p=0.5, alternative="greater").pvalue)
        else:
            p_raw = 1.0
            
        raw_p_values.append(p_raw)
        summary_data.append({
            "scope": scope,
            "alpha": alpha,
            "m_oracle": m_or,
            "m_random": m_rd,
            "delta_oracle": delta_or,
            "ci_delta": ci_delta,
            "b_win": b,
            "c_loss": c,
            "p_raw": p_raw,
            "pref_oracle": float(np.mean([r["oracle_pref"] for r in recs])),
            "pref_random": float(np.mean([r["rand_pref"] for r in recs]))
        })
        
    # Apply Holm adjustment
    holm_p_values = holm_adjust(raw_p_values)
    for i in range(len(summary_data)):
        summary_data[i]["p_holm"] = holm_p_values[i]
        
    # Print results table
    stage1_passes = []
    for d in summary_data:
        cfg_name = f"{d['scope']}_a{d['alpha']:.2f}"
        ci_str = f"[{d['ci_delta'][0]:+.2f}, {d['ci_delta'][1]:+.2f}]"
        sig_flag = " *** PASS ***" if (d['delta_oracle'] > 0 and d['ci_delta'][0] > 0 and d['p_holm'] < 0.05) else ""
        if sig_flag:
            stage1_passes.append(cfg_name)
        print(f"{cfg_name:<18} | {d['scope']:<8} | {d['alpha']:<6.2f} | {d['m_oracle']:<9.3f} | {d['m_random']:<9.3f} | {d['delta_oracle']:<+10.3f} | {ci_str:<16} | {d['b_win']:<7} | {d['c_loss']:<8} | {d['p_raw']:<8.4f} | {d['p_holm']:<8.4f}{sig_flag}")

    print("\n" + "=" * 80)
    print("STAGE 1 GATE 1 VERDICT")
    print("=" * 80)
    if len(stage1_passes) > 0:
        print(f"[VERDICT] STAGE 1 PASSED! Winning configurations with statistically validated positive headroom: {stage1_passes}")
        print("These configurations qualify to advance to Stage 2 (Relational Evaluator Selection).")
    else:
        print("[VERDICT] STAGE 1 FAILED: No configuration achieved Holm-adjusted positive Oracle headroom above Identity (0.650).")
        print("The current temporal-quartile SVD candidate directions do not provide Top-1 improvement over frozen GPT-2, even under soft continuous attenuation or query-only localization.")
        
    # Save results payload
    os.makedirs("experiments/runs/EXP014_headroom", exist_ok=True)
    out_file = "experiments/runs/EXP014_headroom/exp014_stage1_results.json"
    payload = {
        "metadata": {
            "protocol": "EXP014 Stage 1",
            "model": "gpt2 (124M)",
            "pre_hash": pre_hash,
            "post_hash": post_hash,
            "checksums_match": checksums_match,
            "n_instances": len(dataset),
            "layer": layer_idx,
            "rank": rank,
            "m_identity": m_id,
            "pref_identity": pref_id,
            "total_forwards": total_forwards,
            "wall_clock_seconds": elapsed_time
        },
        "configurations": summary_data,
        "stage1_passes": stage1_passes
    }
    with open(out_file, "w") as f:
        json.dump(payload, f, indent=2)
    print(f"\n[OUTPUT] Saved complete EXP014 Stage 1 results payload to: {out_file}")

if __name__ == "__main__":
    main()
