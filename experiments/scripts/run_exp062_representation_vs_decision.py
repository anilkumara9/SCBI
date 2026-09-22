"""
EXP062: Representation-vs-Decision Disambiguation.
Preregistered Falsification Benchmark & Hierarchical Causal Audit.

Evaluates whether the SCBI vector encodes an abstract relational computation
or is merely an output decision direction tied to surface tokens.

Governing Standard: AGENTS.md Laws 1, 2, 6, 7, 8, 9, 11, 13, 14.
Protocol Specification: experiments/protocols/EXP062_REPRESENTATION_VS_DECISION_SPEC.md
"""

import os
import sys
import json
import hashlib
import math
import numpy as np
import torch
import torch.nn.functional as F
from scipy import stats
from transformers import AutoModelForCausalLM, AutoTokenizer

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def compute_model_hash(model):
    sha = hashlib.sha256()
    for p in model.parameters():
        sha.update(p.detach().cpu().numpy().tobytes())
    return sha.hexdigest()

def compute_kl(p_base, p_mod):
    p_base = torch.clamp(p_base, min=1e-12)
    p_mod = torch.clamp(p_mod, min=1e-12)
    return float(torch.sum(p_base * (torch.log(p_base) - torch.log(p_mod))).item())

def compute_paired_stats(base_correct, mod_correct):
    b = 0  # base wrong, mod correct
    c = 0  # base correct, mod wrong
    for bc, mc in zip(base_correct, mod_correct):
        if not bc and mc:
            b += 1
        elif bc and not mc:
            c += 1
    if b + c == 0:
        p_val = 1.0
    else:
        res = stats.binomtest(min(b, c), b + c, 0.5, alternative="two-sided")
        p_val = float(res.pvalue)
    delta_m = (b - c) / len(base_correct)
    return b, c, delta_m, p_val

def log(msg, log_file=None):
    print(msg)
    if log_file:
        log_file.write(msg + "\n")
        log_file.flush()

def main():
    out_dir = os.path.join("experiments", "runs", "EXP062_representation_vs_decision")
    os.makedirs(out_dir, exist_ok=True)
    log_path = os.path.join(out_dir, "exp062_run_log.txt")
    log_file = open(log_path, "w", encoding="utf-8")

    log("==================================================================", log_file)
    log("EXP062: Representation-vs-Decision Disambiguation Benchmark", log_file)
    log("Pre-registered Falsification Protocol: EXP062_REPRESENTATION_VS_DECISION_SPEC.md", log_file)
    log("==================================================================", log_file)

    model_name = "EleutherAI/pythia-160m"
    log(f"Loading model & tokenizer: {model_name}...", log_file)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    model.eval()

    pre_hash = compute_model_hash(model)
    log(f"Pre-experiment parameter SHA-256: {pre_hash}", log_file)
    expected_hash = "54c88fa4897785f2bd94b32d26de1f73f1052bcc42124d563d0cda96940de936"
    assert pre_hash == expected_hash, f"Hash mismatch: expected {expected_hash}, got {pre_hash}"

    # Load BENCH-007
    sys.path.append(os.path.abspath("experiments/benchmarks"))
    # pyrefly: ignore [missing-import]
    from bench_007_capability_ladder import generate_bench_007_capability_ladder
    all_instances = generate_bench_007_capability_ladder()
    
    # Levels 2 & 3 (N=60)
    l23_instances = [inst for inst in all_instances if inst["level"] in (2, 3)]
    # Level 5 (N=30) for cross-domain transfer
    l5_instances = [inst for inst in all_instances if inst["level"] == 5]
    
    log(f"Loaded {len(l23_instances)} transitive instances (Levels 2 & 3) and {len(l5_instances)} Level 5 instances.", log_file)

    device = torch.device("cpu")
    model.to(device)
    target_layer = 7
    layer_module = model.gpt_neox.layers[target_layer]
    alpha = 0.50

    # 1. Evaluate baseline and extract primary vectors for L23 instances
    log("\nEvaluating unintervened baseline on Levels 2 & 3...", log_file)
    base_records = []
    primary_vectors = []

    for inst in l23_instances:
        inp_ids = tokenizer.encode(inst["prompt"], return_tensors="pt").to(device)
        t_tok = tokenizer.encode(inst["target_token"])[0]
        f_tok = tokenizer.encode(inst["foil_token"])[0]
        
        with torch.no_grad():
            out = model(input_ids=inp_ids)
        logits = out.logits[0, -1, :]
        probs = F.softmax(logits, dim=-1)
        
        t_logit = float(logits[t_tok].item())
        f_logit = float(logits[f_tok].item())
        margin = t_logit - f_logit
        correct = bool(t_logit > f_logit)
        top10 = torch.topk(logits, k=10).indices.tolist()

        # Extract contrast vector: v = normalize(W_U[t] - W_U[f])
        w_u_diff = model.embed_out.weight[t_tok, :] - model.embed_out.weight[f_tok, :]
        v_primary = w_u_diff / (torch.norm(w_u_diff) + 1e-8)
        primary_vectors.append(v_primary.detach().clone())

        base_records.append({
            "id": inst["id"],
            "level": inst["level"],
            "prompt": inst["prompt"],
            "target": inst["target"],
            "foil": inst["foil"],
            "target_token": inst["target_token"],
            "foil_token": inst["foil_token"],
            "t_tok": t_tok,
            "f_tok": f_tok,
            "t_logit": t_logit,
            "f_logit": f_logit,
            "margin": margin,
            "correct": correct,
            "probs": probs.detach().clone(),
            "top10": top10
        })

    base_acc = np.mean([r["correct"] for r in base_records])
    log(f"Baseline Levels 2 & 3 Accuracy: {base_acc*100:.1f}% ({sum(r['correct'] for r in base_records)}/60)", log_file)

    # -------------------------------------------------------------
    # 2. Compute Representation Similarity Matrix (Identity Baseline)
    # -------------------------------------------------------------
    log("\nComputing Representation Similarity Matrix (Identity Baseline)...", log_file)
    
    # Pair groupings:
    # S_base: pairs of instances with identical entity names and query target
    # S_ent: pairs of instances with disjoint entity names
    # S_rand: random unit vectors in R^768
    sim_base = []
    sim_ent = []
    sim_rand = []

    for i in range(len(l23_instances)):
        for j in range(i + 1, len(l23_instances)):
            c_val = float(F.cosine_similarity(primary_vectors[i].unsqueeze(0), primary_vectors[j].unsqueeze(0)).item())
            # Check if same entities
            if (l23_instances[i]["target"] == l23_instances[j]["target"] and 
                l23_instances[i]["foil"] == l23_instances[j]["foil"]):
                sim_base.append(c_val)
            else:
                sim_ent.append(c_val)
    
    torch.manual_seed(42)
    for _ in range(1000):
        r1 = torch.randn(768)
        r2 = torch.randn(768)
        r1 /= torch.norm(r1)
        r2 /= torch.norm(r2)
        sim_rand.append(float(F.cosine_similarity(r1.unsqueeze(0), r2.unsqueeze(0)).item()))

    # S_inv: Relation-inverted pairs (A > B > C vs C > B > A with same entities)
    # Construct inverted vectors
    inverted_instances = []
    sim_inv = []
    for inst in l23_instances:
        # Swap target and foil
        t_tok = tokenizer.encode(inst["target_token"])[0]
        f_tok = tokenizer.encode(inst["foil_token"])[0]
        w_u_inv = model.embed_out.weight[f_tok, :] - model.embed_out.weight[t_tok, :]
        v_inv = w_u_inv / (torch.norm(w_u_inv) + 1e-8)
        c_inv = float(F.cosine_similarity((model.embed_out.weight[t_tok, :] - model.embed_out.weight[f_tok, :]).unsqueeze(0), (model.embed_out.weight[f_tok, :] - model.embed_out.weight[t_tok, :]).unsqueeze(0)).item())
        sim_inv.append(c_inv)

    mean_s_base = float(np.mean(sim_base)) if sim_base else 1.0
    mean_s_ent = float(np.mean(sim_ent))
    mean_s_inv = float(np.mean(sim_inv))
    mean_s_rand = float(np.mean(sim_rand))
    std_s_rand = float(np.std(sim_rand))

    log(f"Identity Baseline Cosine Similarities:", log_file)
    log(f"  Same Target/Foil Pairs (S_base): {mean_s_base:.4f}", log_file)
    log(f"  Disjoint Entity Pairs (S_ent):   {mean_s_ent:.4f}", log_file)
    log(f"  Inverted Relation Pairs (S_inv): {mean_s_inv:.4f}", log_file)
    log(f"  Random Gaussian Pairs (S_rand):  {mean_s_rand:.4f} +/- {std_s_rand:.4f}", log_file)
    log(f"  Criterion S_ent > S_rand: {mean_s_ent > mean_s_rand} (Diff = {mean_s_ent - mean_s_rand:.4f})", log_file)

    # -------------------------------------------------------------
    # 3. Execution of the 10 Diagnostic Conditions
    # -------------------------------------------------------------
    # Helper execution function
    def evaluate_condition(name, prompt_fn, target_fn, foil_fn, vector_fn, instances):
        mod_correct = []
        delta_logits_t = []
        delta_logits_f = []
        kl_divs = []
        top10_overlaps = []
        
        for idx, inst in enumerate(instances):
            p_text = prompt_fn(inst, idx)
            t_str = target_fn(inst, idx)
            f_str = foil_fn(inst, idx)
            v_vec = vector_fn(inst, idx)
            
            inp_ids = tokenizer.encode(p_text, return_tensors="pt").to(device)
            t_tok = tokenizer.encode(t_str)[0]
            f_tok = tokenizer.encode(f_str)[0]
            
            # Base pass for this prompt
            with torch.no_grad():
                out_base = model(input_ids=inp_ids)
            l_base = out_base.logits[0, -1, :]
            probs_base = F.softmax(l_base, dim=-1)
            t_logit_base = float(l_base[t_tok].item())
            f_logit_base = float(l_base[f_tok].item())
            base_corr = bool(t_logit_base > f_logit_base)
            top10_base = set(torch.topk(l_base, k=10).indices.tolist())

            # Intervened pass
            def hook_fn(module, inp, outp):
                h = outp[0] if isinstance(outp, tuple) else outp
                h_mod = h + alpha * v_vec.to(h.device).view(1, 1, -1)
                if isinstance(outp, tuple):
                    return (h_mod,) + outp[1:]
                return h_mod
            
            handle = layer_module.register_forward_hook(hook_fn)
            with torch.no_grad():
                out_mod = model(input_ids=inp_ids)
            handle.remove()
            
            l_mod = out_mod.logits[0, -1, :]
            probs_mod = F.softmax(l_mod, dim=-1)
            t_logit_mod = float(l_mod[t_tok].item())
            f_logit_mod = float(l_mod[f_tok].item())
            mod_corr = bool(t_logit_mod > f_logit_mod)
            top10_mod = set(torch.topk(l_mod, k=10).indices.tolist())

            mod_correct.append(mod_corr)
            delta_logits_t.append(t_logit_mod - t_logit_base)
            delta_logits_f.append(f_logit_mod - f_logit_base)
            kl_divs.append(compute_kl(probs_base, probs_mod))
            top10_overlaps.append(len(top10_base.intersection(top10_mod)) / 10.0)

        # Baseline correct for this specific prompt set
        # Re-evaluate base_correct
        prompt_base_correct = []
        for idx, inst in enumerate(instances):
            p_text = prompt_fn(inst, idx)
            t_str = target_fn(inst, idx)
            f_str = foil_fn(inst, idx)
            inp_ids = tokenizer.encode(p_text, return_tensors="pt").to(device)
            t_tok = tokenizer.encode(t_str)[0]
            f_tok = tokenizer.encode(f_str)[0]
            with torch.no_grad():
                out_b = model(input_ids=inp_ids)
            prompt_base_correct.append(bool(out_b.logits[0, -1, t_tok] > out_b.logits[0, -1, f_tok]))

        b, c, delta_m, p_val = compute_paired_stats(prompt_base_correct, mod_correct)
        acc_base = np.mean(prompt_base_correct)
        acc_mod = np.mean(mod_correct)
        mean_dt = float(np.mean(delta_logits_t))
        mean_df = float(np.mean(delta_logits_f))
        mean_margin = float(np.mean(np.array(delta_logits_t) - np.array(delta_logits_f)))
        mean_kl = float(np.mean(kl_divs))
        mean_top10 = float(np.mean(top10_overlaps))

        return {
            "name": name,
            "acc_base": float(acc_base),
            "acc_mod": float(acc_mod),
            "delta_m": float(delta_m),
            "rescues_b": b,
            "corruptions_c": c,
            "exact_p": float(p_val),
            "delta_logit_target": mean_dt,
            "delta_logit_foil": mean_df,
            "delta_margin": mean_margin,
            "kl_div": mean_kl,
            "top10_overlap": mean_top10
        }

    results = {}

    # Mean relational vector across all 60 instances
    mean_v_rel = torch.stack(primary_vectors).mean(dim=0)
    mean_v_rel /= (torch.norm(mean_v_rel) + 1e-8)

    # Condition 1: Target/Foil Relabeling (Abstract (A) vs (B) options)
    log("\nTesting Condition 1: Target/Foil Relabeling ((A) vs (B))...", log_file)
    def c1_prompt(inst, idx):
        # Change prompt: Question: Who is higher in rank, (A) {A} or (B) {C}? Answer: (
        t = inst["target"]
        f = inst["foil"]
        first = inst["target_queried_first"]
        opts = f"(A) {t} or (B) {f}" if first else f"(A) {f} or (B) {t}"
        base_p = inst["prompt"]
        q_pos = base_p.find("Question:")
        prem = base_p[:q_pos].strip()
        return f"{prem} Question: Who is higher in rank, {opts}? Answer: ("
    def c1_target(inst, idx):
        return "A" if inst["target_queried_first"] else "B"
    def c1_foil(inst, idx):
        return "B" if inst["target_queried_first"] else "A"
    def c1_vector(inst, idx):
        return primary_vectors[idx]

    results["1_Target_Foil_Relabeling"] = evaluate_condition(
        "1_Target_Foil_Relabeling", c1_prompt, c1_target, c1_foil, c1_vector, l23_instances
    )

    # Condition 2: Entity-Name Permutation (David, Elena, Felix...)
    log("Testing Condition 2: Entity-Name Permutation (Disjoint Names)...", log_file)
    name_map = {
        "Alice": "David",
        "Bob": "Elena",
        "Charlie": "Felix",
        "David": "Grace",
        "Emma": "Henry"
    }
    def c2_prompt(inst, idx):
        p = inst["prompt"]
        for orig, new_n in name_map.items():
            p = p.replace(orig, new_n)
        return p
    def c2_target(inst, idx):
        return " " + name_map[inst["target"]]
    def c2_foil(inst, idx):
        return " " + name_map[inst["foil"]]
    def c2_vector(inst, idx):
        # We test cross-instance transfer of the source vector v_i to novel names!
        return primary_vectors[idx]

    results["2_Entity_Permutation_Transfer"] = evaluate_condition(
        "2_Entity_Permutation_Transfer", c2_prompt, c2_target, c2_foil, c2_vector, l23_instances
    )

    # Condition 3: Vocabulary / Synonym Substitution ("is higher than")
    log("Testing Condition 3: Vocabulary Substitution ('outranks' -> 'is higher than')...", log_file)
    def c3_prompt(inst, idx):
        p = inst["prompt"]
        p = p.replace("outranks", "is higher than")
        p = p.replace("is lower than", "ranks below")
        return p
    def c3_target(inst, idx):
        return inst["target_token"]
    def c3_foil(inst, idx):
        return inst["foil_token"]
    def c3_vector(inst, idx):
        return primary_vectors[idx]

    results["3_Vocabulary_Substitution"] = evaluate_condition(
        "3_Vocabulary_Substitution", c3_prompt, c3_target, c3_foil, c3_vector, l23_instances
    )

    # Condition 4: Premise Reordering (B > C, A > B)
    log("Testing Condition 4: Premise Reordering (Swapping Clause Order)...", log_file)
    def c4_prompt(inst, idx):
        p = inst["prompt"]
        # Split into premise clauses
        if inst["level"] == 2:
            # Format: Premise: P1. P2. Question...
            parts = p.split(". ")
            if len(parts) >= 3 and "Question:" in parts[2]:
                p1 = parts[0]
                p2 = parts[1]
                rest = ". ".join(parts[2:])
                return f"{p1.split(':')[0]}: {p2}. {p1.split(':')[1].strip()}. {rest}"
        return p
    def c4_target(inst, idx):
        return inst["target_token"]
    def c4_foil(inst, idx):
        return inst["foil_token"]
    def c4_vector(inst, idx):
        return primary_vectors[idx]

    results["4_Premise_Reordering"] = evaluate_condition(
        "4_Premise_Reordering", c4_prompt, c4_target, c4_foil, c4_vector, l23_instances
    )

    # Condition 5: Query Polarity Reversal (Who is lower in rank?)
    log("Testing Condition 5: Query Polarity Reversal (Who is lower in rank?)...", log_file)
    def c5_prompt(inst, idx):
        p = inst["prompt"]
        return p.replace("Who is higher in rank", "Who is lower in rank")
    def c5_target(inst, idx):
        # Polarity inverted: foil is now target!
        return inst["foil_token"]
    def c5_foil(inst, idx):
        # Target is now foil!
        return inst["target_token"]
    def c5_vector(inst, idx):
        # Apply the original vector v_i (which pushes toward original target)
        return primary_vectors[idx]

    results["5_Query_Polarity_Reversal"] = evaluate_condition(
        "5_Query_Polarity_Reversal", c5_prompt, c5_target, c5_foil, c5_vector, l23_instances
    )

    # Condition 6: Random Matched-Norm Output Direction
    log("Testing Condition 6: Random Matched-Norm Direction...", log_file)
    torch.manual_seed(100)
    rand_vecs = [torch.randn(768) for _ in range(len(l23_instances))]
    for rv in rand_vecs:
        rv /= torch.norm(rv)
    def c6_prompt(inst, idx):
        return inst["prompt"]
    def c6_target(inst, idx):
        return inst["target_token"]
    def c6_foil(inst, idx):
        return inst["foil_token"]
    def c6_vector(inst, idx):
        return rand_vecs[idx]

    results["6_Random_Matched_Norm"] = evaluate_condition(
        "6_Random_Matched_Norm", c6_prompt, c6_target, c6_foil, c6_vector, l23_instances
    )

    # Condition 7: Isolated Unembedding Contrast (Non-Relational Context)
    log("Testing Condition 7: Isolated Unembedding Contrast...", log_file)
    def c7_prompt(inst, idx):
        return f"Context: The chosen option is either{inst['target_token']} or{inst['foil_token']}. The selection is"
    def c7_target(inst, idx):
        return inst["target_token"]
    def c7_foil(inst, idx):
        return inst["foil_token"]
    def c7_vector(inst, idx):
        return primary_vectors[idx]

    results["7_Isolated_Unembedding_Contrast"] = evaluate_condition(
        "7_Isolated_Unembedding_Contrast", c7_prompt, c7_target, c7_foil, c7_vector, l23_instances
    )

    # Condition 8: Within-Task Cross-Instance Swap (Instance j applied to instance i)
    log("Testing Condition 8: Within-Task Cross-Instance Swap (Instance j -> i)...", log_file)
    def c8_prompt(inst, idx):
        return inst["prompt"]
    def c8_target(inst, idx):
        return inst["target_token"]
    def c8_foil(inst, idx):
        return inst["foil_token"]
    def c8_vector(inst, idx):
        # Shift index by 7 so entities almost always differ
        j = (idx + 7) % len(l23_instances)
        return primary_vectors[j]

    results["8_Cross_Instance_Swap"] = evaluate_condition(
        "8_Cross_Instance_Swap", c8_prompt, c8_target, c8_foil, c8_vector, l23_instances
    )

    # Condition 9: Mean Relational Vector Across Instances
    log("Testing Condition 9: Mean Relational Vector Transfer...", log_file)
    def c9_prompt(inst, idx):
        return inst["prompt"]
    def c9_target(inst, idx):
        return inst["target_token"]
    def c9_foil(inst, idx):
        return inst["foil_token"]
    def c9_vector(inst, idx):
        return mean_v_rel

    results["9_Mean_Relational_Vector"] = evaluate_condition(
        "9_Mean_Relational_Vector", c9_prompt, c9_target, c9_foil, c9_vector, l23_instances
    )

    # Condition 10: Cross-Domain Transfer (Human Relational Vector -> Planetary Domain)
    log("Testing Condition 10: Cross-Domain Transfer (Human -> Planetary L5)...", log_file)
    def c10_prompt(inst, idx):
        return inst["prompt"]
    def c10_target(inst, idx):
        return inst["target_token"]
    def c10_foil(inst, idx):
        return inst["foil_token"]
    def c10_vector(inst, idx):
        return mean_v_rel

    results["10_Cross_Domain_Planetary_Transfer"] = evaluate_condition(
        "10_Cross_Domain_Planetary_Transfer", c10_prompt, c10_target, c10_foil, c10_vector, l5_instances
    )

    # Condition 11: Relation-Inverted Negative Control (C > B > A with same entities)
    log("Testing Condition 11: Relation-Inverted Negative Control...", log_file)
    def c11_prompt(inst, idx):
        # Create relation-inverted prompt:
        # If original was Alice outranks Bob. Bob outranks Charlie. Who is higher in rank?
        # Inverted: Charlie outranks Bob. Bob outranks Alice. Who is higher in rank?
        p = inst["prompt"]
        t = inst["target"]
        f = inst["foil"]
        # Swap t and f in the premise
        p_inv = p.replace(t, "___TEMP___").replace(f, t).replace("___TEMP___", f)
        return p_inv
    def c11_target(inst, idx):
        # Under C > B > A, the true higher entity is foil!
        return inst["foil_token"]
    def c11_foil(inst, idx):
        return inst["target_token"]
    def c11_vector(inst, idx):
        # Apply the original canonical vector v_i (which pushes toward original target)
        return primary_vectors[idx]

    results["11_Relation_Inverted_Control"] = evaluate_condition(
        "11_Relation_Inverted_Control", c11_prompt, c11_target, c11_foil, c11_vector, l23_instances
    )

    # Invariance Verification
    post_hash = compute_model_hash(model)
    log(f"\nPost-experiment parameter SHA-256: {post_hash}", log_file)
    assert post_hash == expected_hash, f"Immutability violated! Pre: {pre_hash}, Post: {post_hash}"
    log("Verification Confirmed: Delta_theta === 0 strictly preserved.", log_file)

    # Print Scorecard
    log("\n" + "="*80, log_file)
    log("EXP062 COMPLETE SCORECARD ACROSS 11 DIAGNOSTIC CONDITIONS", log_file)
    log("="*80, log_file)
    header = f"{'Condition':<35} | {'Base':<6} | {'Mod':<6} | {'Delta_M':<8} | {'b':<3} | {'c':<3} | {'Exact p':<8} | {'Delta_Margin':<12} | {'KL':<6}"
    log(header, log_file)
    log("-" * len(header), log_file)

    for c_name, res in results.items():
        row = (
            f"{c_name:<35} | "
            f"{res['acc_base']*100:>5.1f}% | "
            f"{res['acc_mod']*100:>5.1f}% | "
            f"{res['delta_m']*100:>+6.1f}pp | "
            f"{res['rescues_b']:>3} | "
            f"{res['corruptions_c']:>3} | "
            f"{res['exact_p']:>8.4f} | "
            f"{res['delta_margin']:>+12.4f} | "
            f"{res['kl_div']:>6.4f}"
        )
        log(row, log_file)

    # Package output json
    final_output = {
        "experiment_id": "EXP062",
        "date": "2026-09-21",
        "model": model_name,
        "pre_hash": pre_hash,
        "post_hash": post_hash,
        "identity_baseline": {
            "mean_s_base": mean_s_base,
            "mean_s_ent": mean_s_ent,
            "mean_s_inv": mean_s_inv,
            "mean_s_rand": mean_s_rand,
            "std_s_rand": std_s_rand,
            "ent_exceeds_rand": bool(mean_s_ent > mean_s_rand)
        },
        "conditions": results
    }

    results_path = os.path.join(out_dir, "exp062_results.json")
    with open(results_path, "w", encoding="utf-8") as f:
        json.dump(final_output, f, indent=2)
    log(f"\nSaved raw data ledger to: {results_path}", log_file)

    log_file.close()

if __name__ == "__main__":
    main()
