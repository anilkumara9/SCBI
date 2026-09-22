"""
run_exp015a_generator_characterization.py: EXP015 Phase A Generator Characterization
Compares 4 candidate generator families on a fixed development set (N=20) on frozen GPT-2:
- G0: Temporal-quartile SVD (EXP014 baseline control)
- G1: Activation-clustered subspaces (cosine similarity agglomerative clustering)
- G2: Global PCA covariance directions
- G4: Sparse feature dictionary atoms
Measures candidate quality (Locality, Diversity, Stability) and descriptive Oracle headroom.
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
from transformers import AutoTokenizer, AutoModelForCausalLM

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from experiments.benchmarks.bench_002_nl import generate_bench_002_nl
from scbi.generators.activation_cluster import (
    generate_g0_temporal,
    generate_g1_clusters,
    generate_g2_pca,
    generate_g4_sparse,
    compute_candidate_quality
)

def get_param_hash(model):
    h = hashlib.sha256()
    for p in model.parameters():
        h.update(p.detach().cpu().numpy().tobytes())
    return h.hexdigest()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n_dev", type=int, default=20, help="Number of development instances")
    parser.add_argument("--dev_seed", type=int, default=123, help="Seed for development instances")
    args = parser.parse_args()

    print("=" * 85)
    print(f"EXP015-A: CANDIDATE GENERATOR CHARACTERIZATION (N={args.n_dev}, Seed={args.dev_seed})")
    print("=" * 85)
    
    start_time = time.time()
    
    # 1. Load Model & Tokenizer
    tokenizer = AutoTokenizer.from_pretrained("gpt2")
    model = AutoModelForCausalLM.from_pretrained("gpt2")
    model.eval()
    
    pre_hash = get_param_hash(model)
    print(f"[REPRODUCIBILITY] Pre-run GPT-2 Parameter Hash: {pre_hash}")
    
    # 2. Load Development Dataset (Independent Seed)
    dataset = generate_bench_002_nl(n_instances=args.n_dev, seed=args.dev_seed)
    print(f"[DATASET] Loaded {len(dataset)} development instances.")
    
    layer_idx = 10
    block_idx = layer_idx - 1 # block 9
    alpha = 0.25 # Locked optimal intervention strength from EXP014
    rank = 2
    K = 4
    
    generators = {
        "G0_temporal": generate_g0_temporal,
        "G1_clusters": generate_g1_clusters,
        "G2_pca": generate_g2_pca,
        "G4_sparse": generate_g4_sparse
    }
    
    gen_results = {g_name: {
        "oracle_corr": [],
        "rand_corr": [],
        "oracle_pref": [],
        "rand_pref": [],
        "locality": [],
        "diversity": [],
        "stability": []
    } for g_name in generators}
    
    identity_correct = []
    identity_pref = []
    
    total_forwards = 0
    
    print(f"\nEvaluating candidate generators at Layer {layer_idx} (alpha={alpha}, rank={rank}, K={K})...")
    
    for idx, inst in enumerate(dataset):
        base_text = inst["base"]
        target_token = inst["target_token"]
        distractor_token = inst["distractor_token"]
        
        target_id = tokenizer.encode(target_token)[0]
        dist_id = tokenizer.encode(distractor_token)[0]
        inputs_base = tokenizer(base_text, return_tensors="pt")
        
        # 1. Identity Baseline
        with torch.no_grad():
            out_base = model(**inputs_base, output_hidden_states=True)
            total_forwards += 1
            
        base_logits = out_base.logits[0, -1]
        base_probs = F.softmax(base_logits, dim=-1)
        base_pred_id = torch.argmax(base_logits).item()
        base_corr = (base_pred_id == target_id)
        base_pr = (base_probs[target_id].item() > base_probs[dist_id].item())
        
        identity_correct.append(base_corr)
        identity_pref.append(base_pr)
        
        h_l = out_base.hidden_states[layer_idx][0] # [seq_len, d_model]
        
        # 2. Evaluate Each Generator
        for g_name, g_fn in generators.items():
            cand_V_list = g_fn(h_l, rank=rank, K=K)
            q_metrics = compute_candidate_quality(h_l, cand_V_list, rank=rank)
            
            gen_results[g_name]["locality"].append(q_metrics["locality"])
            gen_results[g_name]["diversity"].append(q_metrics["diversity"])
            gen_results[g_name]["stability"].append(q_metrics["stability"])
            
            cand_corrs = []
            cand_prefs = []
            
            for V in cand_V_list:
                def hook_fn(module, input, output):
                    h = output[0].clone()
                    h_proj = h - alpha * torch.matmul(torch.matmul(h, V), V.T)
                    return (h_proj, *output[1:])
                    
                handle = model.transformer.h[block_idx].register_forward_hook(hook_fn)
                with torch.no_grad():
                    o_cand = model(**inputs_base)
                    total_forwards += 1
                handle.remove()
                
                c_logits = o_cand.logits[0, -1]
                c_probs = F.softmax(c_logits, dim=-1)
                c_pred_id = torch.argmax(c_logits).item()
                c_corr = (c_pred_id == target_id)
                c_pr = (c_probs[target_id].item() > c_probs[dist_id].item())
                
                cand_corrs.append(c_corr)
                cand_prefs.append(c_pr)
                
            oracle_c = any(cand_corrs)
            oracle_p = any(cand_prefs)
            
            # Random choice (analytical or sample)
            rk = np.random.randint(0, len(cand_corrs))
            rand_c = cand_corrs[rk]
            rand_p = cand_prefs[rk]
            
            gen_results[g_name]["oracle_corr"].append(oracle_c)
            gen_results[g_name]["rand_corr"].append(rand_c)
            gen_results[g_name]["oracle_pref"].append(oracle_p)
            gen_results[g_name]["rand_pref"].append(rand_p)
            
        if (idx + 1) % 5 == 0 or idx == len(dataset) - 1:
            print(f"Processed {idx + 1}/{len(dataset)} development instances... ({time.time() - start_time:.1f}s)")
            
    # 3. Verify Parameter Immutability
    post_hash = get_param_hash(model)
    checksums_match = (pre_hash == post_hash)
    print(f"\n[REPRODUCIBILITY] Post-run Parameter Hash: {post_hash}")
    print(f"[REPRODUCIBILITY] Parameter Checksum Match: {checksums_match}")
    assert checksums_match, "CRITICAL ERROR: Model parameters modified!"
    
    elapsed_time = time.time() - start_time
    m_id = float(np.mean(identity_correct))
    pref_id = float(np.mean(identity_pref))
    
    print("\n" + "=" * 105)
    print(f"EXP015-A GENERATOR CHARACTERIZATION SUMMARY (N_dev={args.n_dev}, M_Identity = {m_id:.3f}, Pref_Identity = {pref_id:.3f})")
    print("=" * 105)
    print(f"{'Generator':<16} | {'M_Oracle':<9} | {'M_Random':<9} | {'Delta(Or-ID)':<13} | {'Spread(Or-Rand)':<16} | {'Pref_Or':<8} | {'Locality':<9} | {'Diversity':<10} | {'Stability':<9}")
    print("-" * 115)
    
    summary = {}
    for g_name in generators:
        res = gen_results[g_name]
        m_or = float(np.mean(res["oracle_corr"]))
        m_rd = float(np.mean(res["rand_corr"]))
        d_or = m_or - m_id
        spread = m_or - m_rd
        p_or = float(np.mean(res["oracle_pref"]))
        loc = float(np.mean(res["locality"]))
        div = float(np.mean(res["diversity"]))
        stab = float(np.mean(res["stability"]))
        
        summary[g_name] = {
            "m_oracle": m_or,
            "m_random": m_rd,
            "delta_oracle": d_or,
            "spread": spread,
            "pref_oracle": p_or,
            "locality": loc,
            "diversity": div,
            "stability": stab
        }
        print(f"{g_name:<16} | {m_or:<9.3f} | {m_rd:<9.3f} | {d_or:<+13.3f} | {spread:<+16.3f} | {p_or:<8.3f} | {loc:<9.3f} | {div:<10.3f} | {stab:<9.3f}")
        
    # Rank generators by Oracle Headroom and Spread
    best_gen = max(generators.keys(), key=lambda g: (summary[g]["delta_oracle"], summary[g]["spread"]))
    print("\n" + "=" * 80)
    print(f"[DECISION] Most Promising Candidate Generator Family: {best_gen}")
    print(f"Delta Oracle over Identity: {summary[best_gen]['delta_oracle']:+.3f}, Candidate Spread: {summary[best_gen]['spread']:+.3f}")
    print("=" * 80)
    
    # Save results payload
    os.makedirs("experiments/runs/EXP015_locality", exist_ok=True)
    out_file = "experiments/runs/EXP015_locality/exp015a_characterization_results.json"
    payload = {
        "metadata": {
            "protocol": "EXP015 Phase A",
            "model": "gpt2 (124M)",
            "pre_hash": pre_hash,
            "post_hash": post_hash,
            "checksums_match": checksums_match,
            "n_dev": args.n_dev,
            "dev_seed": args.dev_seed,
            "layer": layer_idx,
            "alpha": alpha,
            "rank": rank,
            "m_identity": m_id,
            "pref_identity": pref_id,
            "total_forwards": total_forwards,
            "wall_clock_seconds": elapsed_time
        },
        "generators": summary,
        "recommended_generator": best_gen
    }
    with open(out_file, "w") as f:
        json.dump(payload, f, indent=2)
    print(f"\nSaved EXP015-A characterization results to: {out_file}")

if __name__ == "__main__":
    main()
