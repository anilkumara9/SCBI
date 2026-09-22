"""
run_exp015b_confirmatory_benchmark.py: EXP015 Phase B Confirmatory Benchmark
Evaluates the locked candidate generator (G4: Sparse Feature Dictionary Atoms)
against the Baseline Control (G0: Temporal Quartiles) and Identity Baseline (alpha=0)
across the full confirmatory benchmark BENCH-002-NL (N=100, seed=42) on frozen GPT-2 (124M).

Frozen Invariants:
- Backbone: GPT-2 (124M), frozen SHA-256 parameter hashing pre- and post-run (Delta_theta = 0)
- Layer: Layer 10 (block 9 output)
- Operator: P_alpha with alpha = 0.25 (all-token scope)
- Baseline Reference: Identity (alpha = 0, M_Identity = 0.650)
- Endpoints: Top-1 Exact Match (M_LM) and Contrastive Distractor Preference (M_contrast)
- Statistical Tests: Exact paired binary McNemar/binomial test on (b, c) discordant pairs vs Identity,
  95% cluster bootstrap CI on Delta M_Oracle.
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
from scbi.generators.activation_cluster import (
    generate_g0_temporal,
    generate_g4_sparse,
    compute_candidate_quality
)

def get_param_hash(model):
    h = hashlib.sha256()
    for p in model.parameters():
        h.update(p.detach().cpu().numpy().tobytes())
    return h.hexdigest()

def bootstrap_ci(vals, n_boot=2000, seed=42):
    rng = np.random.RandomState(seed)
    n = len(vals)
    if n == 0:
        return 0.0, 0.0
    boot_means = [np.mean(rng.choice(vals, size=n, replace=True)) for _ in range(n_boot)]
    return float(np.percentile(boot_means, 2.5)), float(np.percentile(boot_means, 97.5))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n_instances", type=int, default=100)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    print("=" * 90)
    print("EXP015-B: CONFIRMATORY BENCHMARK — SPARSE FEATURE DICTIONARY VS. TEMPORAL BASELINE")
    print(f"Model: Frozen GPT-2 (124M) | Layer 10 | P_alpha (alpha=0.25) | N={args.n_instances}, Seed={args.seed}")
    print("=" * 90)
    
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    start_time = time.time()
    
    # 1. Load Model & Tokenizer
    tokenizer = AutoTokenizer.from_pretrained("gpt2")
    model = AutoModelForCausalLM.from_pretrained("gpt2")
    model.eval()
    
    pre_hash = get_param_hash(model)
    print(f"[REPRODUCIBILITY] Pre-run GPT-2 Parameter Hash (SHA-256): {pre_hash}")
    
    # 2. Load BENCH-002-NL Confirmatory Dataset (Seed 42)
    dataset = generate_bench_002_nl(n_instances=args.n_instances, seed=args.seed)
    print(f"[DATASET] Loaded {len(dataset)} confirmatory benchmark instances.")
    
    layer_idx = 10
    block_idx = layer_idx - 1 # block 9
    alpha = 0.25 # Locked optimal intervention strength
    rank = 2
    K = 4
    
    # Tracking containers
    identity_correct = []
    identity_pref = []
    
    # Track G4 (Primary Locked Generator) and G0 (Matched Baseline Control)
    tracked_generators = {
        "G4_sparse": generate_g4_sparse,
        "G0_temporal": generate_g0_temporal
    }
    
    records = {g_name: {
        "oracle_corr": [],
        "rand_corr": [],
        "oracle_pref": [],
        "rand_pref": [],
        "locality": [],
        "diversity": [],
        "stability": []
    } for g_name in tracked_generators}
    
    total_forwards = 0
    
    print(f"\nStarting confirmatory execution across N={len(dataset)} instances...")
    
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
        for g_name, g_fn in tracked_generators.items():
            cand_V_list = g_fn(h_l, rank=rank, K=K)
            q_metrics = compute_candidate_quality(h_l, cand_V_list, rank=rank)
            
            records[g_name]["locality"].append(q_metrics["locality"])
            records[g_name]["diversity"].append(q_metrics["diversity"])
            records[g_name]["stability"].append(q_metrics["stability"])
            
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
            
            # Seed-consistent random selection
            rk = np.random.randint(0, len(cand_corrs))
            rand_c = cand_corrs[rk]
            rand_p = cand_prefs[rk]
            
            records[g_name]["oracle_corr"].append(oracle_c)
            records[g_name]["rand_corr"].append(rand_c)
            records[g_name]["oracle_pref"].append(oracle_p)
            records[g_name]["rand_pref"].append(rand_p)
            
        if (idx + 1) % 10 == 0 or idx == len(dataset) - 1:
            print(f"Processed {idx + 1}/{len(dataset)} confirmatory instances... ({time.time() - start_time:.1f}s)")
            
    # 3. Post-run Parameter Checksum Verification
    post_hash = get_param_hash(model)
    checksums_match = (pre_hash == post_hash)
    print(f"\n[REPRODUCIBILITY] Post-run Parameter Hash: {post_hash}")
    print(f"[REPRODUCIBILITY] Parameter Checksum Match (Delta_theta = 0): {checksums_match}")
    assert checksums_match, "CRITICAL ERROR: Foundation model parameters modified!"
    
    elapsed_time = time.time() - start_time
    id_arr = np.array(identity_correct, dtype=int)
    m_id = float(np.mean(id_arr))
    pref_id = float(np.mean(identity_pref))
    
    print("\n" + "=" * 105)
    print(f"EXP015-B CONFIRMATORY BENCHMARK RESULTS (N={len(dataset)}, Identity Baseline M_ID = {m_id:.3f}, Pref_ID = {pref_id:.3f})")
    print("=" * 105)
    print(f"{'Generator':<16} | {'M_Oracle':<9} | {'M_Random':<9} | {'Delta(Or-ID)':<13} | {'95% Boot CI':<16} | {'b (win)':<7} | {'c (loss)':<8} | {'Exact p':<8} | {'Spread':<8} | {'Pref_Or':<8}")
    print("-" * 115)
    
    summary_b = {}
    
    for g_name in tracked_generators:
        recs = records[g_name]
        or_arr = np.array(recs["oracle_corr"], dtype=int)
        rd_arr = np.array(recs["rand_corr"], dtype=int)
        
        m_or = float(np.mean(or_arr))
        m_rd = float(np.mean(rd_arr))
        diffs = or_arr - id_arr
        delta_or = float(np.mean(diffs))
        ci_delta = bootstrap_ci(diffs)
        spread = m_or - m_rd
        p_or = float(np.mean(recs["oracle_pref"]))
        
        # Paired contingency table vs Identity:
        # b: Oracle=1, Identity=0 (positive headroom instances)
        # c: Oracle=0, Identity=1 (regressed instances)
        b = int(np.sum((or_arr == 1) & (id_arr == 0)))
        c = int(np.sum((or_arr == 0) & (id_arr == 1)))
        
        n_disc = b + c
        if n_disc > 0:
            p_exact = float(stats.binomtest(b, n_disc, p=0.5, alternative="greater").pvalue)
        else:
            p_exact = 1.0
            
        ci_str = f"[{ci_delta[0]:+.2f}, {ci_delta[1]:+.2f}]"
        sig_flag = " *** PASS ***" if (delta_or > 0 and ci_delta[0] > 0 and p_exact < 0.05) else ""
        
        summary_b[g_name] = {
            "m_oracle": m_or,
            "m_random": m_rd,
            "delta_oracle": delta_or,
            "ci_delta": ci_delta,
            "b_win": b,
            "c_loss": c,
            "p_exact": p_exact,
            "spread": spread,
            "pref_oracle": p_or,
            "locality": float(np.mean(recs["locality"])),
            "diversity": float(np.mean(recs["diversity"])),
            "stability": float(np.mean(recs["stability"])),
            "passed": bool(delta_or > 0 and ci_delta[0] > 0 and p_exact < 0.05)
        }
        print(f"{g_name:<16} | {m_or:<9.3f} | {m_rd:<9.3f} | {delta_or:<+13.3f} | {ci_str:<16} | {b:<7} | {c:<8} | {p_exact:<8.4f} | {spread:<+8.3f} | {p_or:<8.3f}{sig_flag}")
        
    print("\n" + "=" * 90)
    print("EXP015-B GATE 1 DECISION RULE VERDICT")
    print("=" * 90)
    primary_gen = "G4_sparse"
    if summary_b[primary_gen]["passed"]:
        print(f"[VERDICT] GATE 1 PASSED for {primary_gen}!")
        print(f"Delta Oracle over Identity: {summary_b[primary_gen]['delta_oracle']:+.3f}, Exact p = {summary_b[primary_gen]['p_exact']:.4f}")
        print("This qualifies G4_sparse to advance to Stage 2 (E_CF Selection Test).")
    else:
        print(f"[VERDICT] GATE 1 FAILED for {primary_gen} (Delta = {summary_b[primary_gen]['delta_oracle']:+.3f}, p = {summary_b[primary_gen]['p_exact']:.4f}, CI = [{summary_b[primary_gen]['ci_delta'][0]:+.2f}, {summary_b[primary_gen]['ci_delta'][1]:+.2f}]).")
        
    # Save results payload
    os.makedirs("experiments/runs/EXP015_locality", exist_ok=True)
    out_file = "experiments/runs/EXP015_locality/exp015b_confirmatory_results.json"
    payload = {
        "metadata": {
            "protocol": "EXP015 Phase B",
            "model": "gpt2 (124M)",
            "pre_hash": pre_hash,
            "post_hash": post_hash,
            "checksums_match": checksums_match,
            "n_instances": len(dataset),
            "seed": args.seed,
            "layer": layer_idx,
            "alpha": alpha,
            "rank": rank,
            "m_identity": m_id,
            "pref_identity": pref_id,
            "total_forwards": total_forwards,
            "wall_clock_seconds": elapsed_time
        },
        "results": summary_b
    }
    with open(out_file, "w") as f:
        json.dump(payload, f, indent=2)
    print(f"\nSaved complete EXP015-B confirmatory results to: {out_file}")

if __name__ == "__main__":
    main()
