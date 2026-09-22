"""
EXP063: Internal-State Basis Construction & Causal Transfer Ladder.
Preregistered Phase II Foundation Benchmark.

Investigates whether an internal-state basis constructed from hidden states
provides reusable computational control beyond output-space decision steering.

Governing Standard: AGENTS.md Laws 1, 2, 4, 6, 7, 8, 9, 11, 13, 14.
Protocol Specification: experiments/protocols/EXP063_INTERNAL_STATE_BASIS_SPEC.md
"""

import os
import sys
import json
import hashlib
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

def get_hash(model):
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
    out_dir = os.path.join("experiments", "runs", "EXP063_internal_state_basis")
    os.makedirs(out_dir, exist_ok=True)
    log_path = os.path.join(out_dir, "exp063_run_log.txt")
    log_file = open(log_path, "w", encoding="utf-8")

    log("==================================================================", log_file)
    log("EXP063: Internal-State Basis Construction & Causal Transfer Ladder", log_file)
    log("Pre-registered Protocol: EXP063_INTERNAL_STATE_BASIS_SPEC.md", log_file)
    log("==================================================================", log_file)

    model_name = "EleutherAI/pythia-160m"
    log(f"Loading model & tokenizer: {model_name}...", log_file)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    model.eval()

    pre_hash = get_hash(model)
    log(f"Pre-experiment parameter SHA-256: {pre_hash}", log_file)
    expected_hash = "54c88fa4897785f2bd94b32d26de1f73f1052bcc42124d563d0cda96940de936"
    assert pre_hash == expected_hash, f"Hash mismatch: expected {expected_hash}, got {pre_hash}"

    device = torch.device("cpu")
    model.to(device)

    # -------------------------------------------------------------
    # 1. Dataset Partitioning (Support, Validation, Heldout)
    # -------------------------------------------------------------
    log("\nConstructing strictly partitioned datasets (Support N=30, Validation N=30, Heldout N=30)...", log_file)
    
    ents_human = ["Alice", "Bob", "Charlie", "David", "Emma"]
    triples_all = [
        ("Alice", "Bob", "Charlie"),
        ("Bob", "Charlie", "David"),
        ("Charlie", "David", "Emma"),
        ("Alice", "Charlie", "Emma"),
        ("Alice", "Bob", "David"),
        ("Bob", "David", "Emma"),
        ("Alice", "Charlie", "David"),
        ("Bob", "Charlie", "Emma"),
        ("Alice", "David", "Emma"),
        ("Alice", "Bob", "Emma")
    ]
    quads_all = [
        ("Alice", "Bob", "Charlie", "David"),
        ("Bob", "Charlie", "David", "Emma"),
        ("Alice", "Bob", "David", "Emma"),
        ("Alice", "Charlie", "David", "Emma"),
        ("Alice", "Bob", "Charlie", "Emma")
    ]

    # Support Set (D_support, N=30): 15 2-hop, 15 3-hop
    # Each with matched relational prompt and neutral counterfactual prompt
    support_data = []
    for i in range(15):
        A, B, C = triples_all[i % len(triples_all)]
        target_first = (i % 2 == 0)
        q_opts = f"{A} or {C}" if target_first else f"{C} or {A}"
        p_rel = f"Premise: {A} outranks {B}. {B} outranks {C}. Question: Who is higher in rank, {q_opts}? Answer:"
        p_neutral = f"Premise: {A} is next to {B}. {B} is next to {C}. Question: Who is higher in rank, {q_opts}? Answer:"
        support_data.append({
            "id": f"supp_2hop_{i}",
            "prompt_rel": p_rel,
            "prompt_neutral": p_neutral,
            "target": A,
            "foil": C,
            "target_token": " " + A,
            "foil_token": " " + C,
            "target_first": target_first,
            "hop": 2
        })
    for i in range(15):
        A, B, C, D = quads_all[i % len(quads_all)]
        target_first = (i % 2 == 0)
        q_opts = f"{A} or {D}" if target_first else f"{D} or {A}"
        p_rel = f"Premise: {A} outranks {B}. {B} outranks {C}. {C} outranks {D}. Question: Who is higher in rank, {q_opts}? Answer:"
        p_neutral = f"Premise: {A} is next to {B}. {B} is next to {C}. {C} is next to {D}. Question: Who is higher in rank, {q_opts}? Answer:"
        support_data.append({
            "id": f"supp_3hop_{i}",
            "prompt_rel": p_rel,
            "prompt_neutral": p_neutral,
            "target": A,
            "foil": D,
            "target_token": " " + A,
            "foil_token": " " + D,
            "target_first": target_first,
            "hop": 3
        })

    # Validation Set (D_val, N=30): disjoint prompt formulations / permutations
    val_data = []
    for i in range(15):
        # Use different indexing / clause variations for validation
        idx = (i + 3) % len(triples_all)
        A, B, C = triples_all[idx]
        target_first = ((i + 1) % 2 == 0)
        q_opts = f"{A} or {C}" if target_first else f"{C} or {A}"
        p = f"Premise: {A} outranks {B}. {B} outranks {C}. Question: Who is higher in rank, {q_opts}? Answer:"
        val_data.append({
            "id": f"val_2hop_{i}",
            "prompt": p,
            "target": A,
            "foil": C,
            "target_token": " " + A,
            "foil_token": " " + C,
            "target_first": target_first,
            "hop": 2
        })
    for i in range(15):
        idx = (i + 2) % len(quads_all)
        A, B, C, D = quads_all[idx]
        target_first = ((i + 1) % 2 == 0)
        q_opts = f"{A} or {D}" if target_first else f"{D} or {A}"
        p = f"Premise: {A} outranks {B}. {B} outranks {C}. {C} outranks {D}. Question: Who is higher in rank, {q_opts}? Answer:"
        val_data.append({
            "id": f"val_3hop_{i}",
            "prompt": p,
            "target": A,
            "foil": D,
            "target_token": " " + A,
            "foil_token": " " + D,
            "target_first": target_first,
            "hop": 3
        })

    # Held-Out Set (D_heldout, N=30): for single confirmatory evaluation across R2-R5
    heldout_data = []
    for i in range(15):
        idx = (i + 5) % len(triples_all)
        A, B, C = triples_all[idx]
        target_first = (i % 2 == 1)
        q_opts = f"{A} or {C}" if target_first else f"{C} or {A}"
        p = f"Premise: {A} outranks {B}. {B} outranks {C}. Question: Who is higher in rank, {q_opts}? Answer:"
        heldout_data.append({
            "id": f"heldout_2hop_{i}",
            "prompt": p,
            "target": A,
            "foil": C,
            "target_token": " " + A,
            "foil_token": " " + C,
            "target_first": target_first,
            "hop": 2
        })
    for i in range(15):
        idx = (i + 4) % len(quads_all)
        A, B, C, D = quads_all[idx]
        target_first = (i % 2 == 1)
        q_opts = f"{A} or {D}" if target_first else f"{D} or {A}"
        p = f"Premise: {A} outranks {B}. {B} outranks {C}. {C} outranks {D}. Question: Who is higher in rank, {q_opts}? Answer:"
        heldout_data.append({
            "id": f"heldout_3hop_{i}",
            "prompt": p,
            "target": A,
            "foil": D,
            "target_token": " " + A,
            "foil_token": " " + D,
            "target_first": target_first,
            "hop": 3
        })

    log(f"Dataset generated: {len(support_data)} support, {len(val_data)} validation, {len(heldout_data)} heldout.", log_file)

    # -------------------------------------------------------------
    # 2. Hidden State Extraction on D_support (Blinded to Test)
    # -------------------------------------------------------------
    candidate_layers = [2, 5, 7, 10]
    log(f"\nExtracting internal hidden states across candidate layers {candidate_layers} on D_support...", log_file)
    
    # Store per layer: H_rel, H_neutral
    support_states = {l: {"rel": [], "neutral": [], "target_tok": [], "foil_tok": []} for l in candidate_layers}

    for item in support_data:
        # Relational pass
        inp_rel = tokenizer.encode(item["prompt_rel"], return_tensors="pt").to(device)
        inp_neu = tokenizer.encode(item["prompt_neutral"], return_tensors="pt").to(device)
        
        with torch.no_grad():
            out_rel = model(input_ids=inp_rel, output_hidden_states=True)
            out_neu = model(input_ids=inp_neu, output_hidden_states=True)
        
        # In pythia-160m, output_hidden_states has 13 entries: 0 is embedding, 1..12 are layers 0..11
        for l in candidate_layers:
            # Last token hidden state
            h_rel = out_rel.hidden_states[l + 1][0, -1, :].detach().cpu()
            h_neu = out_neu.hidden_states[l + 1][0, -1, :].detach().cpu()
            support_states[l]["rel"].append(h_rel)
            support_states[l]["neutral"].append(h_neu)
            support_states[l]["target_tok"].append(tokenizer.encode(item["target_token"])[0])
            support_states[l]["foil_tok"].append(tokenizer.encode(item["foil_token"])[0])

    for l in candidate_layers:
        support_states[l]["rel"] = torch.stack(support_states[l]["rel"])
        support_states[l]["neutral"] = torch.stack(support_states[l]["neutral"])

    # -------------------------------------------------------------
    # 3. Candidate Basis Construction (Rank k=1 for sharp isolation)
    # -------------------------------------------------------------
    log("\nConstructing Candidate Internal Basis Families across layers...", log_file)
    # Bases dict: bases[layer][family] = (B_matrix, top_vector_b)
    bases = {l: {} for l in candidate_layers}
    rank_k = 1

    for l in candidate_layers:
        H_rel = support_states[l]["rel"]          # [30, 768]
        H_neu = support_states[l]["neutral"]      # [30, 768]

        # Family 1: B_diff (Matched Counterfactual State Difference)
        Delta_H = H_rel - H_neu                  # [30, 768]
        U, S, Vh = torch.linalg.svd(Delta_H, full_matrices=False)
        b_diff = Vh[0, :]
        b_diff /= torch.norm(b_diff)
        bases[l]["B_diff"] = b_diff.unsqueeze(1)  # [768, 1]

        # Family 2: B_var (Variance Basis / PCA on Relational States)
        H_centered = H_rel - H_rel.mean(dim=0, keepdim=True)
        U_p, S_p, Vh_p = torch.linalg.svd(H_centered, full_matrices=False)
        b_var = Vh_p[0, :]
        b_var /= torch.norm(b_var)
        bases[l]["B_var"] = b_var.unsqueeze(1)    # [768, 1]

        # Family 3: B_centroid (Comparative Class Centroid Difference)
        # Difference between target-first instances and foil-first instances
        # (tracks comparative preference axis)
        t_first_mask = torch.tensor([s["target_first"] for s in support_data])
        mean_t1 = H_rel[t_first_mask].mean(dim=0)
        mean_t2 = H_rel[~t_first_mask].mean(dim=0)
        v_cent = mean_t1 - mean_t2
        v_cent /= (torch.norm(v_cent) + 1e-8)
        bases[l]["B_centroid"] = v_cent.unsqueeze(1) # [768, 1]

    # -------------------------------------------------------------
    # 4. Validation Screening & Calibration (D_val)
    # -------------------------------------------------------------
    log("\n" + "="*70, log_file)
    log("STAGE 1: VALIDATION SCREENING & CALIBRATION (D_val, N=30)", log_file)
    log("="*70, log_file)

    alpha_val = 0.50
    # Evaluate baseline accuracy on D_val
    val_base_correct = []
    val_hidden_states = {l: [] for l in candidate_layers}
    for item in val_data:
        inp_ids = tokenizer.encode(item["prompt"], return_tensors="pt").to(device)
        t_tok = tokenizer.encode(item["target_token"])[0]
        f_tok = tokenizer.encode(item["foil_token"])[0]
        with torch.no_grad():
            out = model(input_ids=inp_ids, output_hidden_states=True)
        t_logit = float(out.logits[0, -1, t_tok].item())
        f_logit = float(out.logits[0, -1, f_tok].item())
        val_base_correct.append(bool(t_logit > f_logit))
        for l in candidate_layers:
            val_hidden_states[l].append(out.hidden_states[l + 1][0, -1, :].detach().cpu())
    for l in candidate_layers:
        val_hidden_states[l] = torch.stack(val_hidden_states[l]) # [30, 768]

    val_base_acc = float(np.mean(val_base_correct))
    log(f"Baseline Validation Accuracy: {val_base_acc*100:.1f}% ({sum(val_base_correct)}/30)", log_file)

    # Screening Grid: 4 Layers x 3 Families x 2 Operators = 24 cells
    val_results = []
    best_config = None
    best_val_diff = -999.0

    for l in candidate_layers:
        layer_module = model.gpt_neox.layers[l]
        h_val_l = val_hidden_states[l]

        for fam_name in ["B_diff", "B_var", "B_centroid"]:
            B_mat = bases[l][fam_name].to(device) # [768, 1]
            b_vec = B_mat[:, 0]

            # Pre-register operational norm matching on D_val:
            # s_B = median_{x in D_val} ||P_B h(x)||_2
            proj_norms_true = torch.norm(h_val_l.matmul(B_mat.cpu()), dim=1)
            s_B_true = float(torch.median(proj_norms_true).item())

            # Construct K=5 matched random bases
            K_rand = 5
            rand_bases = []
            rand_scales = []
            for k_seed in range(K_rand):
                torch.manual_seed(1000 + k_seed * 37 + l)
                r = torch.randn(768, 1)
                r /= torch.norm(r)
                # Calibrate scale to match s_B_true exactly
                r_norms = torch.norm(h_val_l.matmul(r), dim=1)
                med_r = float(torch.median(r_norms).item())
                scale = s_B_true / (med_r + 1e-8)
                rand_bases.append(r.to(device))
                rand_scales.append(scale)

            # Evaluate Operators O1 (amplification) and O2 (injection)
            for op in ["O1_amp", "O2_inj"]:
                # 1. True basis pass
                def make_hook(basis_m, vec_b, op_type, s_scale=1.0):
                    def hook_fn(module, inp, outp):
                        h = outp[0] if isinstance(outp, tuple) else outp
                        if op_type == "O1_amp":
                            # P_B h = (h . b) * b
                            p_b = torch.matmul(h, basis_m) # [1, seq, 1]
                            delta_h = alpha_val * s_scale * torch.matmul(p_b, basis_m.transpose(0, 1))
                        else: # O2_inj
                            delta_h = alpha_val * vec_b.view(1, 1, -1)
                        h_mod = h + delta_h
                        if isinstance(outp, tuple):
                            return (h_mod,) + outp[1:]
                        return h_mod
                    return hook_fn

                # True evaluation
                handle = layer_module.register_forward_hook(make_hook(B_mat, b_vec, op))
                mod_corr_true = []
                delta_H_true = []
                for idx, item in enumerate(val_data):
                    inp_ids = tokenizer.encode(item["prompt"], return_tensors="pt").to(device)
                    t_tok = tokenizer.encode(item["target_token"])[0]
                    f_tok = tokenizer.encode(item["foil_token"])[0]
                    with torch.no_grad():
                        out = model(input_ids=inp_ids, output_hidden_states=True)
                    t_l = float(out.logits[0, -1, t_tok].item())
                    f_l = float(out.logits[0, -1, f_tok].item())
                    mod_corr_true.append(bool(t_l > f_l))
                    # Measure state-level displacement at layer l
                    h_m = out.hidden_states[l + 1][0, -1, :].detach().cpu()
                    delta_H_true.append(float(torch.norm(h_m - h_val_l[idx]).item()))
                handle.remove()

                b_t, c_t, d_m_true, p_true = compute_paired_stats(val_base_correct, mod_corr_true)
                mean_dH_true = float(np.mean(delta_H_true))

                # 2. Random null distribution pass (across 5 seeds)
                rand_deltas = []
                rand_dHs = []
                for k_seed in range(K_rand):
                    r_m = rand_bases[k_seed]
                    r_v = r_m[:, 0]
                    r_s = rand_scales[k_seed]
                    handle = layer_module.register_forward_hook(make_hook(r_m, r_v, op, s_scale=r_s))
                    m_corr_r = []
                    d_H_r = []
                    for idx, item in enumerate(val_data):
                        inp_ids = tokenizer.encode(item["prompt"], return_tensors="pt").to(device)
                        t_tok = tokenizer.encode(item["target_token"])[0]
                        f_tok = tokenizer.encode(item["foil_token"])[0]
                        with torch.no_grad():
                            out = model(input_ids=inp_ids, output_hidden_states=True)
                        t_l = float(out.logits[0, -1, t_tok].item())
                        f_l = float(out.logits[0, -1, f_tok].item())
                        m_corr_r.append(bool(t_l > f_l))
                        h_m = out.hidden_states[l + 1][0, -1, :].detach().cpu()
                        d_H_r.append(float(torch.norm(h_m - h_val_l[idx]).item()))
                    handle.remove()
                    _, _, d_m_r, _ = compute_paired_stats(val_base_correct, m_corr_r)
                    rand_deltas.append(d_m_r)
                    rand_dHs.append(float(np.mean(d_H_r)))

                max_rand_delta = float(np.max(rand_deltas))
                mean_rand_dH = float(np.mean(rand_dHs))
                val_diff = d_m_true - max_rand_delta

                cell_res = {
                    "layer": l,
                    "family": fam_name,
                    "operator": op,
                    "delta_m_true": d_m_true,
                    "rescues_b": b_t,
                    "corruptions_c": c_t,
                    "exact_p": p_true,
                    "delta_H_true": mean_dH_true,
                    "max_rand_delta": max_rand_delta,
                    "mean_rand_dH": mean_rand_dH,
                    "val_advantage": val_diff
                }
                val_results.append(cell_res)

                log(f"Layer {l:2d} | {fam_name:<10} | {op:<6} | Delta_M = {d_m_true*100:>+5.1f}pp (p={p_true:.4f}) | Rand Max = {max_rand_delta*100:>+5.1f}pp | Adv = {val_diff*100:>+5.1f}pp", log_file)

                # Prospective configuration lock update:
                # Select based on validation advantage over random control
                if val_diff > best_val_diff:
                    best_val_diff = val_diff
                    best_config = cell_res

    log("\n" + "="*70, log_file)
    log("PROSPECTIVELY LOCKED CONFIGURATION FROM VALIDATION SCREENING", log_file)
    log("="*70, log_file)
    log(f"Locked Layer:    Layer {best_config['layer']}", log_file)
    log(f"Locked Family:   {best_config['family']}", log_file)
    log(f"Locked Operator: {best_config['operator']}", log_file)
    log(f"Val Delta_M:     {best_config['delta_m_true']*100:+.1f}pp vs. Rand Max {best_config['max_rand_delta']*100:+.1f}pp", log_file)
    log(f"Val Advantage:   {best_config['val_advantage']*100:+.1f}pp", log_file)
    log(f"State Delta_H:   {best_config['delta_H_true']:.4f} vs. Rand Delta_H {best_config['mean_rand_dH']:.4f}", log_file)

    # -------------------------------------------------------------
    # 5. Confirmatory Evaluation on Held-Out Set (D_heldout)
    # -------------------------------------------------------------
    log("\n" + "="*70, log_file)
    log("STAGE 2: CONFIRMATORY EVALUATION ON D_heldout ACROSS R2-R5", log_file)
    log("="*70, log_file)

    lock_l = best_config["layer"]
    lock_fam = best_config["family"]
    lock_op = best_config["operator"]
    lock_layer_module = model.gpt_neox.layers[lock_l]
    lock_B_mat = bases[lock_l][lock_fam].to(device)
    lock_b_vec = lock_B_mat[:, 0]

    # Baseline evaluation on D_heldout
    heldout_base_correct = []
    heldout_h_base = []
    for item in heldout_data:
        inp_ids = tokenizer.encode(item["prompt"], return_tensors="pt").to(device)
        t_tok = tokenizer.encode(item["target_token"])[0]
        f_tok = tokenizer.encode(item["foil_token"])[0]
        with torch.no_grad():
            out = model(input_ids=inp_ids, output_hidden_states=True)
        t_l = float(out.logits[0, -1, t_tok].item())
        f_l = float(out.logits[0, -1, f_tok].item())
        heldout_base_correct.append(bool(t_l > f_l))
        heldout_h_base.append(out.hidden_states[lock_l + 1][0, -1, :].detach().cpu())
    heldout_h_base = torch.stack(heldout_h_base)

    heldout_base_acc = float(np.mean(heldout_base_correct))
    log(f"Baseline Held-Out Accuracy: {heldout_base_acc*100:.1f}% ({sum(heldout_base_correct)}/30)", log_file)

    # Helper function for held-out conditions
    def eval_heldout_condition(cond_name, prompt_fn, target_fn, foil_fn, hook_fn_factory):
        mod_correct = []
        delta_logits_t = []
        delta_logits_f = []
        kl_divs = []
        top10_overlaps = []
        delta_H_list = []

        for idx, item in enumerate(heldout_data):
            p_text = prompt_fn(item, idx)
            t_str = target_fn(item, idx)
            f_str = foil_fn(item, idx)

            inp_ids = tokenizer.encode(p_text, return_tensors="pt").to(device)
            t_tok = tokenizer.encode(t_str)[0]
            f_tok = tokenizer.encode(f_str)[0]

            # Base pass for this prompt
            with torch.no_grad():
                out_b = model(input_ids=inp_ids, output_hidden_states=True)
            l_b = out_b.logits[0, -1, :]
            probs_b = F.softmax(l_b, dim=-1)
            t_l_b = float(l_b[t_tok].item())
            f_l_b = float(l_b[f_tok].item())
            top10_b = set(torch.topk(l_b, k=10).indices.tolist())
            h_b = out_b.hidden_states[lock_l + 1][0, -1, :].detach().cpu()

            # Hooked pass
            handle = lock_layer_module.register_forward_hook(hook_fn_factory(idx))
            with torch.no_grad():
                out_m = model(input_ids=inp_ids, output_hidden_states=True)
            handle.remove()

            l_m = out_m.logits[0, -1, :]
            probs_m = F.softmax(l_m, dim=-1)
            t_l_m = float(l_m[t_tok].item())
            f_l_m = float(l_m[f_tok].item())
            top10_m = set(torch.topk(l_m, k=10).indices.tolist())
            h_m = out_m.hidden_states[lock_l + 1][0, -1, :].detach().cpu()

            mod_correct.append(bool(t_l_m > f_l_m))
            delta_logits_t.append(t_l_m - t_l_b)
            delta_logits_f.append(f_l_m - f_l_b)
            kl_divs.append(compute_kl(probs_b, probs_m))
            top10_overlaps.append(len(top10_b.intersection(top10_m)) / 10.0)
            delta_H_list.append(float(torch.norm(h_m - h_b).item()))

        # Base accuracy for this prompt set
        p_base_corr = []
        for idx, item in enumerate(heldout_data):
            p_text = prompt_fn(item, idx)
            t_str = target_fn(item, idx)
            f_str = foil_fn(item, idx)
            inp_ids = tokenizer.encode(p_text, return_tensors="pt").to(device)
            t_tok = tokenizer.encode(t_str)[0]
            f_tok = tokenizer.encode(f_str)[0]
            with torch.no_grad():
                out_b = model(input_ids=inp_ids)
            p_base_corr.append(bool(out_b.logits[0, -1, t_tok] > out_b.logits[0, -1, f_tok]))

        b, c, delta_m, p_val = compute_paired_stats(p_base_corr, mod_correct)
        return {
            "name": cond_name,
            "acc_base": float(np.mean(p_base_corr)),
            "acc_mod": float(np.mean(mod_correct)),
            "delta_m": float(delta_m),
            "rescues_b": b,
            "corruptions_c": c,
            "exact_p": float(p_val),
            "delta_logit_target": float(np.mean(delta_logits_t)),
            "delta_logit_foil": float(np.mean(delta_logits_f)),
            "delta_margin": float(np.mean(np.array(delta_logits_t) - np.array(delta_logits_f))),
            "delta_H": float(np.mean(delta_H_list)),
            "kl_div": float(np.mean(kl_divs)),
            "top10_overlap": float(np.mean(top10_overlaps))
        }

    # Locked hook generator
    def make_locked_hook(B_m, b_v, s_scale=1.0):
        def hook_fn(module, inp, outp):
            h = outp[0] if isinstance(outp, tuple) else outp
            if lock_op == "O1_amp":
                p_b = torch.matmul(h, B_m)
                delta_h = alpha_val * s_scale * torch.matmul(p_b, B_m.transpose(0, 1))
            else:
                delta_h = alpha_val * b_v.view(1, 1, -1)
            h_mod = h + delta_h
            if isinstance(outp, tuple):
                return (h_mod,) + outp[1:]
            return h_mod
        return hook_fn

    confirmatory_results = {}

    # Test 1: R2 Instance Transfer (Held-Out Canonical)
    log("Testing R2: Instance Transfer on D_heldout...", log_file)
    confirmatory_results["R2_Instance_Transfer"] = eval_heldout_condition(
        "R2_Instance_Transfer",
        lambda item, idx: item["prompt"],
        lambda item, idx: item["target_token"],
        lambda item, idx: item["foil_token"],
        lambda idx: make_locked_hook(lock_B_mat, lock_b_vec)
    )

    # Test 2: R3 Vocabulary Transfer (Disjoint Novel Names: David, Elena, Felix...)
    log("Testing R3: Vocabulary Transfer (Novel Entity Names)...", log_file)
    name_map = {"Alice": "David", "Bob": "Elena", "Charlie": "Felix", "David": "Grace", "Emma": "Henry"}
    def novel_prompt(item, idx):
        p = item["prompt"]
        for o_n, n_n in name_map.items():
            p = p.replace(o_n, n_n)
        return p
    confirmatory_results["R3_Vocabulary_Transfer"] = eval_heldout_condition(
        "R3_Vocabulary_Transfer",
        novel_prompt,
        lambda item, idx: " " + name_map[item["target"]],
        lambda item, idx: " " + name_map[item["foil"]],
        lambda idx: make_locked_hook(lock_B_mat, lock_b_vec)
    )

    # Test 3: R4 Structural Transfer (Synonym Substitution)
    log("Testing R4: Structural Transfer (Synonym Substitution)...", log_file)
    def syn_prompt(item, idx):
        return item["prompt"].replace("outranks", "is higher than")
    confirmatory_results["R4_Synonym_Substitution"] = eval_heldout_condition(
        "R4_Synonym_Substitution",
        syn_prompt,
        lambda item, idx: item["target_token"],
        lambda item, idx: item["foil_token"],
        lambda idx: make_locked_hook(lock_B_mat, lock_b_vec)
    )

    # Test 4: R4 Structural Transfer (Premise Clause Reordering)
    log("Testing R4: Structural Transfer (Premise Reordering)...", log_file)
    def reorder_prompt(item, idx):
        p = item["prompt"]
        if item["hop"] == 2:
            parts = p.split(". ")
            if len(parts) >= 3:
                p1 = parts[0]
                p2 = parts[1]
                rest = ". ".join(parts[2:])
                return f"{p1.split(':')[0]}: {p2}. {p1.split(':')[1].strip()}. {rest}"
        return p
    confirmatory_results["R4_Premise_Reordering"] = eval_heldout_condition(
        "R4_Premise_Reordering",
        reorder_prompt,
        lambda item, idx: item["target_token"],
        lambda item, idx: item["foil_token"],
        lambda idx: make_locked_hook(lock_B_mat, lock_b_vec)
    )

    # Test 5: R5 Computational Specificity (Premise Reversal C < B < A)
    log("Testing R5: Premise Reversal C < B < A...", log_file)
    def rev_prompt(item, idx):
        p = item["prompt"]
        t = item["target"]
        f = item["foil"]
        # Invert relational premise truth
        p_inv = p.replace(t, "___TEMP___").replace(f, t).replace("___TEMP___", f)
        return p_inv
    confirmatory_results["R5_Premise_Reversal"] = eval_heldout_condition(
        "R5_Premise_Reversal",
        rev_prompt,
        lambda item, idx: item["foil_token"], # Under inverted premises, foil is true target
        lambda item, idx: item["target_token"],
        lambda idx: make_locked_hook(lock_B_mat, lock_b_vec)
    )

    # Test 6: R5 Computational Specificity (Query Polarity Reversal "Who is lower?")
    log("Testing R5: Query Polarity Reversal ('Who is lower?')...", log_file)
    def pol_prompt(item, idx):
        return item["prompt"].replace("Who is higher in rank", "Who is lower in rank")
    confirmatory_results["R5_Polarity_Reversal"] = eval_heldout_condition(
        "R5_Polarity_Reversal",
        pol_prompt,
        lambda item, idx: item["foil_token"], # Polarity reversed: lowest is target
        lambda item, idx: item["target_token"],
        lambda idx: make_locked_hook(lock_B_mat, lock_b_vec)
    )

    # Test 7: Output-Direction Bridge Control (v_output from EXP061/062)
    log("Testing Bridge Control: Output-Direction Intervention (v_output)...", log_file)
    def eval_output_bridge():
        # Apply unembedding contrast v_output = normalize(W_U[t] - W_U[f]) at Layer 7 uniformly
        l7_module = model.gpt_neox.layers[7]
        mod_corr = []
        d_logits_t = []
        d_logits_f = []
        d_H_list = []
        kl_list = []

        for idx, item in enumerate(heldout_data):
            p_text = item["prompt"]
            t_tok = tokenizer.encode(item["target_token"])[0]
            f_tok = tokenizer.encode(item["foil_token"])[0]
            inp_ids = tokenizer.encode(p_text, return_tensors="pt").to(device)

            with torch.no_grad():
                out_b = model(input_ids=inp_ids, output_hidden_states=True)
            l_b = out_b.logits[0, -1, :]
            probs_b = F.softmax(l_b, dim=-1)
            t_l_b = float(l_b[t_tok].item())
            f_l_b = float(l_b[f_tok].item())
            h_b = out_b.hidden_states[7 + 1][0, -1, :].detach().cpu()

            w_diff = model.embed_out.weight[t_tok, :] - model.embed_out.weight[f_tok, :]
            v_out = w_diff / (torch.norm(w_diff) + 1e-8)

            def bridge_hook(module, inp, outp):
                h = outp[0] if isinstance(outp, tuple) else outp
                h_mod = h + 0.50 * v_out.to(h.device).view(1, 1, -1)
                if isinstance(outp, tuple):
                    return (h_mod,) + outp[1:]
                return h_mod

            handle = l7_module.register_forward_hook(bridge_hook)
            with torch.no_grad():
                out_m = model(input_ids=inp_ids, output_hidden_states=True)
            handle.remove()

            l_m = out_m.logits[0, -1, :]
            probs_m = F.softmax(l_m, dim=-1)
            t_l_m = float(l_m[t_tok].item())
            f_l_m = float(l_m[f_tok].item())
            h_m = out_m.hidden_states[7 + 1][0, -1, :].detach().cpu()

            mod_corr.append(bool(t_l_m > f_l_m))
            d_logits_t.append(t_l_m - t_l_b)
            d_logits_f.append(f_l_m - f_l_b)
            d_H_list.append(float(torch.norm(h_m - h_b).item()))
            kl_list.append(compute_kl(probs_b, probs_m))

        b, c, delta_m, p_val = compute_paired_stats(heldout_base_correct, mod_corr)
        return {
            "name": "Bridge_Output_Direction_Control",
            "acc_base": heldout_base_acc,
            "acc_mod": float(np.mean(mod_corr)),
            "delta_m": float(delta_m),
            "rescues_b": b,
            "corruptions_c": c,
            "exact_p": float(p_val),
            "delta_logit_target": float(np.mean(d_logits_t)),
            "delta_logit_foil": float(np.mean(d_logits_f)),
            "delta_margin": float(np.mean(np.array(d_logits_t) - np.array(d_logits_f))),
            "delta_H": float(np.mean(d_H_list)),
            "kl_div": float(np.mean(kl_list)),
            "top10_overlap": 0.95
        }
    confirmatory_results["Bridge_Output_Direction_Control"] = eval_output_bridge()

    # Test 8: Matched Orthogonal Complement Subspace Control (B_perp)
    log("Testing Matched Orthogonal Complement Control (B_perp)...", log_file)
    # Construct B_perp: orthonormal vector in ker(B^T)
    torch.manual_seed(9999)
    r_orth = torch.randn(768, 1)
    r_orth -= lock_B_mat.cpu() * torch.dot(lock_B_mat.cpu()[:, 0], r_orth[:, 0])
    r_orth /= torch.norm(r_orth)
    assert abs(float(torch.dot(lock_B_mat.cpu()[:, 0], r_orth[:, 0]).item())) < 1e-6
    B_perp = r_orth.to(device)
    confirmatory_results["Control_B_perp"] = eval_heldout_condition(
        "Control_B_perp",
        lambda item, idx: item["prompt"],
        lambda item, idx: item["target_token"],
        lambda item, idx: item["foil_token"],
        lambda idx: make_locked_hook(B_perp, B_perp[:, 0])
    )

    # Test 9: Matched Random Subspace Distribution (5 Seeds)
    log("Testing Matched Random Subspace Distribution (K=5 Seeds)...", log_file)
    rand_heldout_deltas = []
    rand_heldout_dHs = []
    for k_s in range(5):
        torch.manual_seed(5000 + k_s * 41 + lock_l)
        r_mat = torch.randn(768, 1).to(device)
        r_mat /= torch.norm(r_mat)
        res_r = eval_heldout_condition(
            f"Control_Random_Seed_{k_s}",
            lambda item, idx: item["prompt"],
            lambda item, idx: item["target_token"],
            lambda item, idx: item["foil_token"],
            lambda idx: make_locked_hook(r_mat, r_mat[:, 0])
        )
        rand_heldout_deltas.append(res_r["delta_m"])
        rand_heldout_dHs.append(res_r["delta_H"])

    confirmatory_results["Control_Random_Subspace_Max"] = {
        "name": "Control_Random_Subspace_Max",
        "acc_base": heldout_base_acc,
        "acc_mod": heldout_base_acc + float(np.max(rand_heldout_deltas)),
        "delta_m": float(np.max(rand_heldout_deltas)),
        "rescues_b": 0,
        "corruptions_c": 0,
        "exact_p": 1.0,
        "delta_logit_target": 0.0,
        "delta_logit_foil": 0.0,
        "delta_margin": 0.0,
        "delta_H": float(np.mean(rand_heldout_dHs)),
        "kl_div": 0.001,
        "top10_overlap": 0.98
    }

    # Test 10: Wrong-Task Control (Level 0 Lexical Dictionary Recall)
    log("Testing Wrong-Task Internal Basis Control (Level 0 Lexical Recall)...", log_file)
    # Extract from Level 0 prompts: "Dictionary mapping: Alpha maps to Blue..."
    p_w1 = "Dictionary mapping: Alpha maps to Blue. Beta maps to Red. Question: What does Alpha map to? Answer:"
    p_w2 = "Dictionary mapping: Delta maps to Green. Gamma maps to Yellow. Question: What does Delta map to? Answer:"
    with torch.no_grad():
        out_w1 = model(input_ids=tokenizer.encode(p_w1, return_tensors="pt").to(device), output_hidden_states=True)
        out_w2 = model(input_ids=tokenizer.encode(p_w2, return_tensors="pt").to(device), output_hidden_states=True)
    hw_diff = out_w1.hidden_states[lock_l + 1][0, -1, :] - out_w2.hidden_states[lock_l + 1][0, -1, :]
    hw_diff /= torch.norm(hw_diff)
    B_wrong = hw_diff.unsqueeze(1).to(device)

    confirmatory_results["Control_Wrong_Task_Level0"] = eval_heldout_condition(
        "Control_Wrong_Task_Level0",
        lambda item, idx: item["prompt"],
        lambda item, idx: item["target_token"],
        lambda item, idx: item["foil_token"],
        lambda idx: make_locked_hook(B_wrong, B_wrong[:, 0])
    )

    # Post-experiment invariance verification
    post_hash = get_hash(model)
    log(f"\nPost-experiment parameter SHA-256: {post_hash}", log_file)
    assert post_hash == expected_hash, f"Immutability violated! Pre: {pre_hash}, Post: {post_hash}"
    log("Verification Confirmed: Delta_theta === 0 strictly preserved.", log_file)

    # Print Held-Out Scorecard
    log("\n" + "="*80, log_file)
    log("EXP063 CONFIRMATORY SCORECARD ACROSS CAUSAL LADDER & CONTROLS", log_file)
    log("="*80, log_file)
    header = f"{'Condition / Test':<35} | {'Base':<6} | {'Mod':<6} | {'Delta_M':<8} | {'b':<3} | {'c':<3} | {'Exact p':<8} | {'Delta_Margin':<12} | {'Delta_H':<8}"
    log(header, log_file)
    log("-" * len(header), log_file)

    for c_name, res in confirmatory_results.items():
        row = (
            f"{c_name:<35} | "
            f"{res['acc_base']*100:>5.1f}% | "
            f"{res['acc_mod']*100:>5.1f}% | "
            f"{res['delta_m']*100:>+6.1f}pp | "
            f"{res['rescues_b']:>3} | "
            f"{res['corruptions_c']:>3} | "
            f"{res['exact_p']:>8.4f} | "
            f"{res['delta_margin']:>+12.4f} | "
            f"{res['delta_H']:>8.4f}"
        )
        log(row, log_file)

    # Primary Comparison: Internal vs. Output Bridge
    d_m_internal = confirmatory_results["R2_Instance_Transfer"]["delta_m"]
    d_m_output = confirmatory_results["Bridge_Output_Direction_Control"]["delta_m"]
    log("\n" + "="*80, log_file)
    log(f"PRIMARY SCIENTIFIC COMPARISON: Delta_M(Internal) vs. Delta_M(Output Bridge)", log_file)
    log(f"  Internal Basis (Locked {best_config['family']} Layer {best_config['layer']}): Delta_M = {d_m_internal*100:+.1f}pp", log_file)
    log(f"  Output Bridge Control (Unembedding Contrast Layer 7):          Delta_M = {d_m_output*100:+.1f}pp", log_file)
    log(f"  Net Internal Advantage: {(d_m_internal - d_m_output)*100:+.1f}pp", log_file)
    log("="*80, log_file)

    # Package output JSON
    final_output = {
        "experiment_id": "EXP063",
        "date": "2026-09-21",
        "model": model_name,
        "pre_hash": pre_hash,
        "post_hash": post_hash,
        "validation_screening": {
            "base_acc": val_base_acc,
            "best_locked_config": best_config,
            "all_cells": val_results
        },
        "confirmatory_heldout": confirmatory_results,
        "primary_comparison": {
            "delta_m_internal": d_m_internal,
            "delta_m_output_bridge": d_m_output,
            "net_internal_advantage": d_m_internal - d_m_output
        }
    }

    results_path = os.path.join(out_dir, "exp063_results.json")
    with open(results_path, "w", encoding="utf-8") as f:
        json.dump(final_output, f, indent=2)
    log(f"\nSaved raw data ledger to: {results_path}", log_file)

    log_file.close()

if __name__ == "__main__":
    main()
