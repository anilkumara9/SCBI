"""
audit_exp013_mcnemar.py: Exact Paired Binary Contingency Audit for EXP013
Computes exact instance-level paired outcomes:
  b = #(E_CF = 1, Random = 0)
  c = #(E_CF = 0, Random = 1)
  a = #(E_CF = 1, Random = 1)
  d = #(E_CF = 0, Random = 0)
Performs exact McNemar / binomial test:
  scipy.stats.binomtest(b, b + c, p=0.5, alternative='greater')
Saves full instance-by-instance records to disk for auditability.
"""
import os
import sys
import json
import time
import argparse
import numpy as np
import torch
import torch.nn.functional as F
from scipy import stats
from transformers import AutoTokenizer, AutoModelForCausalLM

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from experiments.benchmarks.bench_002_nl import generate_bench_002_nl

def js_divergence(p, q):
    m = 0.5 * (p + q)
    kl_pm = F.kl_div(m.log(), p, reduction="sum")
    kl_qm = F.kl_div(m.log(), q, reduction="sum")
    return (0.5 * (kl_pm + kl_qm)).item()

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

def run_mcnemar_audit(layers=[10], n_instances=100, seed=42):
    print("=" * 80)
    print(f"EXP013 EXACT PAIRED BINARY CONTINGENCY AUDIT (Layers: {layers}, N={n_instances}, Seed={seed})")
    print("=" * 80)
    
    np.random.seed(seed)
    torch.manual_seed(seed)
    
    tokenizer = AutoTokenizer.from_pretrained("gpt2")
    model = AutoModelForCausalLM.from_pretrained("gpt2")
    model.eval()
    
    dataset = generate_bench_002_nl(n_instances=n_instances, seed=42)
    print(f"Loaded {len(dataset)} benchmark instances.")
    
    layer_audit = {l: [] for l in layers}
    all_pooled_candidates = []
    
    t0 = time.time()
    
    for idx, inst in enumerate(dataset):
        base_text = inst["base"]
        pos_text = inst["pos"]
        neg_text = inst["neg"]
        target_token = inst["target_token"]
        distractor_token = inst["distractor_token"]
        
        target_id = tokenizer.encode(target_token)[0]
        dist_id = tokenizer.encode(distractor_token)[0]
        
        inputs_base = tokenizer(base_text, return_tensors="pt")
        inputs_pos = tokenizer(pos_text, return_tensors="pt")
        inputs_neg = tokenizer(neg_text, return_tensors="pt")
        
        with torch.no_grad():
            out_base = model(**inputs_base, output_hidden_states=True)
            
        base_logits = out_base.logits[0, -1]
        base_probs = F.softmax(base_logits, dim=-1)
        base_pred_id = torch.argmax(base_logits).item()
        base_correct = (base_pred_id == target_id)
        base_pref = (base_probs[target_id].item() > base_probs[dist_id].item())
        
        inst_pooled = []
        
        for l in layers:
            h_l = out_base.hidden_states[l][0]
            cand_V_list = generate_label_free_candidates(h_l, rank=2)
            
            cand_evals = []
            for ck_i, V in enumerate(cand_V_list):
                def hook_fn(module, input, output):
                    h = output[0].clone()
                    h_proj = h - torch.matmul(torch.matmul(h, V), V.T)
                    return (h_proj, *output[1:])
                
                handle = model.transformer.h[l - 1].register_forward_hook(hook_fn)
                with torch.no_grad():
                    o_b = model(**inputs_base)
                    o_p = model(**inputs_pos)
                    o_n = model(**inputs_neg)
                handle.remove()
                
                qb = F.softmax(o_b.logits[0, -1], dim=-1)
                qp = F.softmax(o_p.logits[0, -1], dim=-1)
                qn = F.softmax(o_n.logits[0, -1], dim=-1)
                
                pred_id = torch.argmax(o_b.logits[0, -1]).item()
                is_correct = (pred_id == target_id)
                prefers_target = (qb[target_id].item() > qb[dist_id].item())
                
                d_pos = js_divergence(qb, qp)
                d_neg = js_divergence(qb, qn)
                e_cf = d_pos - 0.5 * d_neg
                
                cand_evals.append({
                    "k": ck_i,
                    "is_correct": is_correct,
                    "prefers_target": prefers_target,
                    "e_cf": e_cf,
                    "p_target": qb[target_id].item()
                })
                
                inst_pooled.append({
                    "layer": l,
                    "k": ck_i,
                    "is_correct": is_correct,
                    "prefers_target": prefers_target,
                    "e_cf": e_cf
                })
            
            rand_k = np.random.randint(0, len(cand_evals))
            rand_correct = cand_evals[rand_k]["is_correct"]
            rand_pref = cand_evals[rand_k]["prefers_target"]
            
            best_ecf_k = int(np.argmin([c["e_cf"] for c in cand_evals]))
            ecf_correct = cand_evals[best_ecf_k]["is_correct"]
            ecf_pref = cand_evals[best_ecf_k]["prefers_target"]
            
            oracle_correct = any([c["is_correct"] for c in cand_evals])
            oracle_pref = any([c["prefers_target"] for c in cand_evals])
            p_rand_correct = float(np.mean([c["is_correct"] for c in cand_evals]))
            
            layer_audit[l].append({
                "inst_idx": idx,
                "identity_correct": base_correct,
                "rand_k": rand_k,
                "rand_correct": rand_correct,
                "p_rand_correct": p_rand_correct,
                "best_ecf_k": best_ecf_k,
                "ecf_correct": ecf_correct,
                "oracle_correct": oracle_correct,
                "identity_pref": base_pref,
                "rand_pref": rand_pref,
                "ecf_pref": ecf_pref,
                "oracle_pref": oracle_pref,
                "cand_correct_list": [c["is_correct"] for c in cand_evals],
                "cand_ecf_list": [c["e_cf"] for c in cand_evals]
            })
            
        all_pooled_candidates.append(inst_pooled)
        if (idx + 1) % 10 == 0 or idx == len(dataset) - 1:
            print(f"Processed {idx + 1}/{len(dataset)} instances... ({time.time() - t0:.1f}s)")
            
    print(f"\nExecution finished in {time.time() - t0:.2f} s.")
    
    results = {}
    for l in layers:
        records = layer_audit[l]
        ecf_arr = np.array([r["ecf_correct"] for r in records], dtype=int)
        rand_arr = np.array([r["rand_correct"] for r in records], dtype=int)
        id_arr = np.array([r["identity_correct"] for r in records], dtype=int)
        or_arr = np.array([r["oracle_correct"] for r in records], dtype=int)
        
        a = int(np.sum((ecf_arr == 1) & (rand_arr == 1)))
        b = int(np.sum((ecf_arr == 1) & (rand_arr == 0)))
        c = int(np.sum((ecf_arr == 0) & (rand_arr == 1)))
        d = int(np.sum((ecf_arr == 0) & (rand_arr == 0)))
        
        n_discordant = b + c
        
        if n_discordant > 0:
            binom_res_greater = stats.binomtest(b, n_discordant, p=0.5, alternative="greater")
            p_exact_greater = float(binom_res_greater.pvalue)
            binom_res_two = stats.binomtest(b, n_discordant, p=0.5, alternative="two-sided")
            p_exact_two = float(binom_res_two.pvalue)
        else:
            p_exact_greater = 1.0
            p_exact_two = 1.0
            
        diffs = ecf_arr - rand_arr
        delta_m = float(np.mean(diffs))
        ci_delta = bootstrap_ci(diffs)
        
        p_rand_arr = np.array([r["p_rand_correct"] for r in records], dtype=float)
        delta_expected = float(np.mean(ecf_arr - p_rand_arr))
        
        print("\n" + "=" * 60)
        print(f"EXACT CONTINGENCY AUDIT: LAYER {l}")
        print("=" * 60)
        print(f"Marginals: Identity={np.mean(id_arr):.3f} | Random={np.mean(rand_arr):.3f} | E_CF={np.mean(ecf_arr):.3f} | Oracle={np.mean(or_arr):.3f}")
        print(f"Effect Size Delta M: {delta_m:+.3f} (95% Bootstrap CI: [{ci_delta[0]:+.3f}, {ci_delta[1]:+.3f}])")
        print(f"Delta against Expected Random: {delta_expected:+.3f}")
        print("\n2x2 Paired Contingency Table (E_CF vs Random):")
        print(f"                   Random = 1    Random = 0    Total")
        print(f"  E_CF = 1        a = {a:<10} b = {b:<10} {a+b}")
        print(f"  E_CF = 0        c = {c:<10} d = {d:<10} {c+d}")
        print(f"  Total           {a+c:<14} {b+d:<14} {len(records)}")
        print(f"\nDiscordant pairs: n_disc = b + c = {n_discordant} (b={b}, c={c})")
        print(f"Exact McNemar / Binomial p-value (greater):   p = {p_exact_greater:.5f}")
        print(f"Exact McNemar / Binomial p-value (two-sided): p = {p_exact_two:.5f}")
        
        results[f"layer_{l}"] = {
            "m_identity": float(np.mean(id_arr)),
            "m_random": float(np.mean(rand_arr)),
            "m_ecf": float(np.mean(ecf_arr)),
            "m_oracle": float(np.mean(or_arr)),
            "delta_m": delta_m,
            "ci_delta": ci_delta,
            "contingency_table": {"a": a, "b": b, "c": c, "d": d},
            "n_discordant": n_discordant,
            "p_mcnemar_exact_greater": p_exact_greater,
            "p_mcnemar_exact_two_sided": p_exact_two,
            "records": records
        }
        
    if len(layers) == 5:
        print("\n" + "=" * 60)
        print("EXACT CONTINGENCY AUDIT: DESIGN B (POOLED |C|=20)")
        print("=" * 60)
        b_rand = []
        b_ecf = []
        b_oracle = []
        for inst_cands in all_pooled_candidates:
            rk = np.random.randint(0, len(inst_cands))
            b_rand.append(inst_cands[rk]["is_correct"])
            bcf_k = int(np.argmin([c["e_cf"] for c in inst_cands]))
            b_ecf.append(inst_cands[bcf_k]["is_correct"])
            b_oracle.append(any([c["is_correct"] for c in inst_cands]))
            
        b_rand_arr = np.array(b_rand, dtype=int)
        b_ecf_arr = np.array(b_ecf, dtype=int)
        
        ba = int(np.sum((b_ecf_arr == 1) & (b_rand_arr == 1)))
        bb = int(np.sum((b_ecf_arr == 1) & (b_rand_arr == 0)))
        bc = int(np.sum((b_ecf_arr == 0) & (b_rand_arr == 1)))
        bd = int(np.sum((b_ecf_arr == 0) & (b_rand_arr == 0)))
        
        b_n_disc = bb + bc
        if b_n_disc > 0:
            b_p_greater = float(stats.binomtest(bb, b_n_disc, p=0.5, alternative="greater").pvalue)
            b_p_two = float(stats.binomtest(bb, b_n_disc, p=0.5, alternative="two-sided").pvalue)
        else:
            b_p_greater = 1.0
            b_p_two = 1.0
            
        b_diffs = b_ecf_arr - b_rand_arr
        b_delta = float(np.mean(b_diffs))
        b_ci = bootstrap_ci(b_diffs)
        
        print(f"Marginals: Random={np.mean(b_rand_arr):.3f} | E_CF={np.mean(b_ecf_arr):.3f} | Oracle={np.mean(b_oracle):.3f}")
        print(f"Effect Size Delta M: {b_delta:+.3f} (95% Bootstrap CI: [{b_ci[0]:+.3f}, {b_ci[1]:+.3f}])")
        print("\n2x2 Paired Contingency Table (Design B):")
        print(f"                   Random = 1    Random = 0    Total")
        print(f"  E_CF = 1        a = {ba:<10} b = {bb:<10} {ba+bb}")
        print(f"  E_CF = 0        c = {bc:<10} d = {bd:<10} {bc+bd}")
        print(f"  Total           {ba+bc:<14} {bb+bd:<14} {len(dataset)}")
        print(f"\nDiscordant pairs: n_disc = b + c = {b_n_disc} (b={bb}, c={bc})")
        print(f"Exact McNemar / Binomial p-value (greater):   p = {b_p_greater:.5f}")
        print(f"Exact McNemar / Binomial p-value (two-sided): p = {b_p_two:.5f}")
        
        results["design_b"] = {
            "m_random": float(np.mean(b_rand_arr)),
            "m_ecf": float(np.mean(b_ecf_arr)),
            "m_oracle": float(np.mean(b_oracle)),
            "delta_m": b_delta,
            "ci_delta": b_ci,
            "contingency_table": {"a": ba, "b": bb, "c": bc, "d": bd},
            "n_discordant": b_n_disc,
            "p_mcnemar_exact_greater": b_p_greater,
            "p_mcnemar_exact_two_sided": b_p_two
        }
        
    out_path = "experiments/runs/EXP013_pretrained/exp013_mcnemar_audit.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved McNemar audit report to: {out_path}")
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--layers", nargs="+", type=int, default=[10])
    parser.add_argument("--n_instances", type=int, default=100)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    run_mcnemar_audit(layers=args.layers, n_instances=args.n_instances, seed=args.seed)
