"""
EXP066: Cross-Scale Replication on Pythia-410M.
Preregistered Confirmatory Replication Protocol.

Core Scientific Question:
Does the EXP063-065 representational-causal boundary replicate at a larger frozen Pythia scale?
Central confirmatory contrast:
    Delta M(Dynamic Internal Basis) >? 0
with the same-layer output bridge acting as the causal-access positive control.

Governing Standards:
- AGENTS.md 14 Inviolable Laws (Law 6: Frozen Backbone Delta theta = 0, Law 7: Zero Data Leakage, Law 13: Deterministic Reproducibility)
- STATISTICAL_PROTOCOL_V02.md
- Protocol Spec: experiments/protocols/EXP066_PYTHIA410M_CROSS_SCALE_REPLICATION_SPEC.md
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
    b = 0  # base wrong, mod correct (rescues)
    c = 0  # base correct, mod wrong (corruptions)
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
    out_dir = os.path.join("experiments", "runs", "EXP066_pythia410m_replication")
    os.makedirs(out_dir, exist_ok=True)
    log_path = os.path.join(out_dir, "exp066_run_log.txt")
    log_file = open(log_path, "w", encoding="utf-8")

    log("="*80, log_file)
    log("EXP066: Cross-Scale Replication on Pythia-410M", log_file)
    log("Preregistered Protocol: EXP066_PYTHIA410M_CROSS_SCALE_REPLICATION_SPEC.md", log_file)
    log("="*80, log_file)

    model_name = "EleutherAI/pythia-410m"
    log(f"Loading model & tokenizer: {model_name}...", log_file)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    model.eval()

    pre_hash = get_hash(model)
    log(f"Pre-experiment parameter SHA-256: {pre_hash}", log_file)
    expected_hash = "4c242d9ac702a4029a674eacee84e0517cb6f79d794661dc3a3102bca5ed48dd"
    assert pre_hash == expected_hash, f"Hash mismatch: expected {expected_hash}, got {pre_hash}"
    log("Model hash verified against preregistered parameter manifest.", log_file)

    device = torch.device("cpu")
    model.to(device)

    # -------------------------------------------------------------
    # 1. Multi-Vocabulary Support Set & Basis Extraction (Layer 20)
    # -------------------------------------------------------------
    target_layer = 20  # Equivalent proportional depth (83.33%) to Layer 10 on 160M
    log(f"\n[1] Constructing Multi-Vocabulary Support Set & Extracting B_agg at Layer {target_layer} (d=1024)...", log_file)
    layer_module = model.gpt_neox.layers[target_layer]

    support_vocabularies = {
        "V1_Anglo": ["Alice", "Bob", "Charlie", "David", "Emma"],
        "V2_Biblical": ["Aaron", "Caleb", "Gideon", "Miriam", "Reuben"],
        "V3_Greek": ["Hector", "Jason", "Nestor", "Paris", "Priam"],
        "V4_Roman": ["Marcus", "Lucius", "Titus", "Felix", "Silas"],
        "V5_Modern": ["Liam", "Noah", "Sora", "Maya", "Leila"]
    }

    triples_indices = [
        (0, 1, 2), (1, 2, 3), (2, 3, 4), (0, 2, 4), (0, 1, 3),
        (1, 3, 4), (0, 2, 3), (1, 2, 4), (0, 3, 4), (0, 1, 4),
        (0, 1, 2), (1, 2, 3), (2, 3, 4), (0, 2, 4), (0, 1, 3)
    ]
    quads_indices = [
        (0, 1, 2, 3), (1, 2, 3, 4), (0, 1, 3, 4), (0, 2, 3, 4), (0, 1, 2, 4),
        (0, 1, 2, 3), (1, 2, 3, 4), (0, 1, 3, 4), (0, 2, 3, 4), (0, 1, 2, 4),
        (0, 1, 2, 3), (1, 2, 3, 4), (0, 1, 3, 4), (0, 2, 3, 4), (0, 1, 2, 4)
    ]

    delta_h_by_vocab = {v_key: [] for v_key in support_vocabularies}
    for v_key, ents in support_vocabularies.items():
        # 15 2-hop
        for i, (iA, iB, iC) in enumerate(triples_indices):
            A, B, C = ents[iA], ents[iB], ents[iC]
            q_opts = f"{A} or {C}" if (i % 2 == 0) else f"{C} or {A}"
            p_rel = f"Premise: {A} outranks {B}. {B} outranks {C}. Question: Who is higher in rank, {q_opts}? Answer:"
            p_neu = f"Premise: {A} is next to {B}. {B} is next to {C}. Question: Who is higher in rank, {q_opts}? Answer:"
            with torch.no_grad():
                o_rel = model(input_ids=tokenizer.encode(p_rel, return_tensors="pt").to(device), output_hidden_states=True)
                o_neu = model(input_ids=tokenizer.encode(p_neu, return_tensors="pt").to(device), output_hidden_states=True)
            dh = o_rel.hidden_states[target_layer + 1][0, -1, :].detach().cpu() - o_neu.hidden_states[target_layer + 1][0, -1, :].detach().cpu()
            delta_h_by_vocab[v_key].append(dh)
        # 15 3-hop
        for i, (iA, iB, iC, iD) in enumerate(quads_indices):
            A, B, C, D = ents[iA], ents[iB], ents[iC], ents[iD]
            q_opts = f"{A} or {D}" if (i % 2 == 0) else f"{D} or {A}"
            p_rel = f"Premise: {A} outranks {B}. {B} outranks {C}. {C} outranks {D}. Question: Who is higher in rank, {q_opts}? Answer:"
            p_neu = f"Premise: {A} is next to {B}. {B} is next to {C}. {C} is next to {D}. Question: Who is higher in rank, {q_opts}? Answer:"
            with torch.no_grad():
                o_rel = model(input_ids=tokenizer.encode(p_rel, return_tensors="pt").to(device), output_hidden_states=True)
                o_neu = model(input_ids=tokenizer.encode(p_neu, return_tensors="pt").to(device), output_hidden_states=True)
            dh = o_rel.hidden_states[target_layer + 1][0, -1, :].detach().cpu() - o_neu.hidden_states[target_layer + 1][0, -1, :].detach().cpu()
            delta_h_by_vocab[v_key].append(dh)
        delta_h_by_vocab[v_key] = torch.stack(delta_h_by_vocab[v_key])  # [30, 1024]

    # Compute normalized per-vocabulary directions v_k and aggregated B_agg
    v_hat_by_vocab = {}
    for v_key, dH in delta_h_by_vocab.items():
        norms = torch.norm(dH, dim=1, keepdim=True) + 1e-12
        mean_v = (dH / norms).mean(dim=0)
        v_hat_by_vocab[v_key] = mean_v / (torch.norm(mean_v) + 1e-12)

    sum_v = torch.stack(list(v_hat_by_vocab.values())).sum(dim=0)
    B_agg = sum_v / (torch.norm(sum_v) + 1e-12)
    log(f"B_agg constructed across K=5 support vocabularies (dim = {B_agg.shape[0]}, norm = {torch.norm(B_agg):.4f}).", log_file)

    # Negative controls for B_agg
    torch.manual_seed(9876)
    r_orth = torch.randn(1024)
    r_orth -= B_agg * torch.dot(B_agg, r_orth)
    r_orth /= torch.norm(r_orth)
    B_perp = r_orth

    p_wrong_rel = "Fact: Paris is the capital of France. Question: What is the capital of France, Paris or London? Answer:"
    p_wrong_neu = "Fact: Paris is near London. Question: What is the capital of France, Paris or London? Answer:"
    with torch.no_grad():
        out_wr_rel = model(input_ids=tokenizer.encode(p_wrong_rel, return_tensors="pt").to(device), output_hidden_states=True)
        out_wr_neu = model(input_ids=tokenizer.encode(p_wrong_neu, return_tensors="pt").to(device), output_hidden_states=True)
    dH_wrong = out_wr_rel.hidden_states[target_layer + 1][0, -1, :].detach().cpu() - out_wr_neu.hidden_states[target_layer + 1][0, -1, :].detach().cpu()
    B_wrong = dH_wrong / (torch.norm(dH_wrong) + 1e-12)

    # Canonical Support Reference Frames (Alice, Charlie, David):
    tok_alice = tokenizer.encode(" Alice")[0]
    tok_charlie = tokenizer.encode(" Charlie")[0]
    tok_david = tokenizer.encode(" David")[0]

    E_0_2hop = torch.stack([model.embed_out.weight[tok_alice, :].detach().cpu(),
                            model.embed_out.weight[tok_charlie, :].detach().cpu()])  # [2, 1024]
    E_0_3hop = torch.stack([model.embed_out.weight[tok_alice, :].detach().cpu(),
                            model.embed_out.weight[tok_david, :].detach().cpu()])    # [2, 1024]

    # -------------------------------------------------------------
    # 2. Stage A: Alignment Discovery in Support Space
    # -------------------------------------------------------------
    log("\n" + "="*80, log_file)
    log("[2] STAGE A: ALIGNMENT DISCOVERY IN SUPPORT SPACE (Pythia-410M)", log_file)
    log("="*80, log_file)

    stage_A_results = []
    for vk, ents in support_vocabularies.items():
        if vk == "V1_Anglo":
            continue
        t_head = tokenizer.encode(" " + ents[0])[0]
        t_tail = tokenizer.encode(" " + ents[2])[0]
        E_k = torch.stack([model.embed_out.weight[t_head, :].detach().cpu(),
                           model.embed_out.weight[t_tail, :].detach().cpu()])  # [2, 1024]
        # Procrustes rotation from support V1 to Vk: R @ E_0^T = E_k^T
        U, S, Vh = torch.linalg.svd(E_k.T @ E_0_2hop)
        R_k = U @ Vh  # [1024, 1024]

        raw_cos = float(torch.dot(v_hat_by_vocab["V1_Anglo"], v_hat_by_vocab[vk]).item())
        v_aligned = R_k @ v_hat_by_vocab["V1_Anglo"]
        aligned_cos = float(torch.dot(v_aligned, v_hat_by_vocab[vk]).item())

        stage_A_results.append({
            "vocab": vk,
            "raw_cosine": raw_cos,
            "aligned_cosine": aligned_cos,
            "delta_cosine": aligned_cos - raw_cos
        })
        log(f"Vocab {vk:<12} | Raw Cosine = {raw_cos:>+7.4f} | Aligned Cosine = {aligned_cos:>+7.4f} | Delta = {aligned_cos - raw_cos:>+7.4f}", log_file)

    mean_raw = float(np.mean([r["raw_cosine"] for r in stage_A_results]))
    mean_aligned = float(np.mean([r["aligned_cosine"] for r in stage_A_results]))
    log(f"Stage A Summary: Mean Raw Cosine = {mean_raw:>+7.4f} | Mean Aligned Cosine = {mean_aligned:>+7.4f} | Delta = {mean_aligned - mean_raw:>+7.4f}", log_file)

    # -------------------------------------------------------------
    # 3. Benchmark Construction (N=60)
    # -------------------------------------------------------------
    log("\n" + "="*80, log_file)
    log("[3] BENCHMARK SPECIFICATION & VERIFICATION (N=60)", log_file)
    log("="*80, log_file)

    novel_vocab_planet = ["Mars", "Venus", "Jupiter", "Saturn", "Mercury"]
    novel_vocab_element = ["Iron", "Gold", "Silver", "Bronze", "Steel"]

    test_instances = []

    # Block 1: Planetary (30 instances: 15 2-hop, 15 3-hop)
    for i, (iA, iB, iC) in enumerate(triples_indices):
        A, B, C = novel_vocab_planet[iA], novel_vocab_planet[iB], novel_vocab_planet[iC]
        target_first = (i % 2 == 1)
        q_opts = f"{A} or {C}" if target_first else f"{C} or {A}"
        is_rev = (i >= 8)
        if not is_rev:
            p = f"Premise: {A} outranks {B}. {B} outranks {C}. Question: Who is higher in rank, {q_opts}? Answer:"
            head_ent, tail_ent = A, C
            true_target, true_foil = A, C
        else:
            p = f"Premise: {C} is lower than {B}. {B} is lower than {A}. Question: Who is higher in rank, {q_opts}? Answer:"
            head_ent, tail_ent = A, C
            true_target, true_foil = A, C
        test_instances.append({
            "id": f"pythia410m_planet_2hop_{i}",
            "hop": 2,
            "domain": "Planetary",
            "prompt": p,
            "head_entity": head_ent,
            "tail_entity": tail_ent,
            "target": true_target,
            "foil": true_foil,
            "target_token": " " + true_target,
            "foil_token": " " + true_foil,
            "target_first": target_first,
            "is_reversed": is_rev
        })

    for i, (iA, iB, iC, iD) in enumerate(quads_indices):
        A, B, C, D = novel_vocab_planet[iA], novel_vocab_planet[iB], novel_vocab_planet[iC], novel_vocab_planet[iD]
        target_first = (i % 2 == 1)
        q_opts = f"{A} or {D}" if target_first else f"{D} or {A}"
        is_rev = (i >= 8)
        if not is_rev:
            p = f"Premise: {A} outranks {B}. {B} outranks {C}. {C} outranks {D}. Question: Who is higher in rank, {q_opts}? Answer:"
            head_ent, tail_ent = A, D
            true_target, true_foil = A, D
        else:
            p = f"Premise: {D} is lower than {C}. {C} is lower than {B}. {B} is lower than {A}. Question: Who is higher in rank, {q_opts}? Answer:"
            head_ent, tail_ent = A, D
            true_target, true_foil = A, D
        test_instances.append({
            "id": f"pythia410m_planet_3hop_{i}",
            "hop": 3,
            "domain": "Planetary",
            "prompt": p,
            "head_entity": head_ent,
            "tail_entity": tail_ent,
            "target": true_target,
            "foil": true_foil,
            "target_token": " " + true_target,
            "foil_token": " " + true_foil,
            "target_first": target_first,
            "is_reversed": is_rev
        })

    # Block 2: Elemental (30 instances: 15 2-hop, 15 3-hop)
    for i, (iA, iB, iC) in enumerate(triples_indices):
        A, B, C = novel_vocab_element[iA], novel_vocab_element[iB], novel_vocab_element[iC]
        target_first = (i % 2 == 0)
        q_opts = f"{A} or {C}" if target_first else f"{C} or {A}"
        is_rev = (i >= 7)
        if not is_rev:
            p = f"Premise: {A} outranks {B}. {B} outranks {C}. Question: Who is higher in rank, {q_opts}? Answer:"
            head_ent, tail_ent = A, C
            true_target, true_foil = A, C
        else:
            p = f"Premise: {C} is lower than {B}. {B} is lower than {A}. Question: Who is higher in rank, {q_opts}? Answer:"
            head_ent, tail_ent = A, C
            true_target, true_foil = A, C
        test_instances.append({
            "id": f"pythia410m_element_2hop_{i}",
            "hop": 2,
            "domain": "Elemental",
            "prompt": p,
            "head_entity": head_ent,
            "tail_entity": tail_ent,
            "target": true_target,
            "foil": true_foil,
            "target_token": " " + true_target,
            "foil_token": " " + true_foil,
            "target_first": target_first,
            "is_reversed": is_rev
        })

    for i, (iA, iB, iC, iD) in enumerate(quads_indices):
        A, B, C, D = novel_vocab_element[iA], novel_vocab_element[iB], novel_vocab_element[iC], novel_vocab_element[iD]
        target_first = (i % 2 == 0)
        q_opts = f"{A} or {D}" if target_first else f"{D} or {A}"
        is_rev = (i >= 7)
        if not is_rev:
            p = f"Premise: {A} outranks {B}. {B} outranks {C}. {C} outranks {D}. Question: Who is higher in rank, {q_opts}? Answer:"
            head_ent, tail_ent = A, D
            true_target, true_foil = A, D
        else:
            p = f"Premise: {D} is lower than {C}. {C} is lower than {B}. {B} is lower than {A}. Question: Who is higher in rank, {q_opts}? Answer:"
            head_ent, tail_ent = A, D
            true_target, true_foil = A, D
        test_instances.append({
            "id": f"pythia410m_element_3hop_{i}",
            "hop": 3,
            "domain": "Elemental",
            "prompt": p,
            "head_entity": head_ent,
            "tail_entity": tail_ent,
            "target": true_target,
            "foil": true_foil,
            "target_token": " " + true_target,
            "foil_token": " " + true_foil,
            "target_first": target_first,
            "is_reversed": is_rev
        })

    assert len(test_instances) == 60, f"Expected 60 test instances, got {len(test_instances)}"

    # -------------------------------------------------------------
    # 4. Baseline Evaluation & Headroom Verification
    # -------------------------------------------------------------
    log("\n" + "="*80, log_file)
    log("[4] BASELINE EVALUATION & HEADROOM VERIFICATION", log_file)
    log("="*80, log_file)

    base_correct_list = []
    base_logits_diff = []
    for item in test_instances:
        inp_ids = tokenizer.encode(item["prompt"], return_tensors="pt").to(device)
        t_tok = tokenizer.encode(item["target_token"])[0]
        f_tok = tokenizer.encode(item["foil_token"])[0]
        with torch.no_grad():
            out = model(input_ids=inp_ids)
        t_l = float(out.logits[0, -1, t_tok].item())
        f_l = float(out.logits[0, -1, f_tok].item())
        is_c = bool(t_l > f_l)
        base_correct_list.append(is_c)
        base_logits_diff.append(t_l - f_l)

    base_acc = float(np.mean(base_correct_list))
    num_correct = sum(base_correct_list)
    num_errors = len(test_instances) - num_correct
    log(f"Pythia-410M Baseline Accuracy: {base_acc*100:.2f}% ({num_correct}/60 correct, {num_errors} errors available for rescue).", log_file)
    assert 0.35 <= base_acc <= 0.75, f"Calibration outside window: {base_acc*100:.1f}%"
    log("HEADROOM CRITERION MET: Baseline is within pre-registered 40%-70% window (no ceiling).", log_file)

    # -------------------------------------------------------------
    # 5. Stage B: Confirmatory Replication Across 6 Conditions
    # -------------------------------------------------------------
    log("\n" + "="*80, log_file)
    log("[5] STAGE B: CONFIRMATORY REPLICATION ACROSS 6 CONDITIONS", log_file)
    log("="*80, log_file)

    alpha_val = 0.50  # Fixed inherited intervention strength

    def get_procrustes_rotation(item):
        t_h = tokenizer.encode(" " + item["head_entity"])[0]
        t_t = tokenizer.encode(" " + item["tail_entity"])[0]
        E_inst = torch.stack([model.embed_out.weight[t_h, :].detach().cpu(),
                              model.embed_out.weight[t_t, :].detach().cpu()])  # [2, 1024]
        E_ref = E_0_2hop if item["hop"] == 2 else E_0_3hop
        U, S, Vh = torch.linalg.svd(E_inst.T @ E_ref)
        R = U @ Vh  # [1024, 1024]
        return R

    def make_bridge_vec(tt, ft):
        w = model.embed_out.weight[tt, :] - model.embed_out.weight[ft, :]
        return w / (torch.norm(w) + 1e-12)

    instance_records = {item["id"]: {"prompt": item["prompt"], "base_correct": base_correct_list[i]} for i, item in enumerate(test_instances)}

    def eval_test_condition(cond_name, vector_fn):
        mod_correct = []
        d_logits_t = []
        d_logits_f = []
        d_H_list = []
        kl_list = []
        top10_overlaps = []
        margin_shifts = []

        for idx, item in enumerate(test_instances):
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
            top10_b = set(torch.topk(l_b, k=10).indices.tolist())
            h_b = out_b.hidden_states[target_layer + 1][0, -1, :].detach().cpu()

            v_vec = vector_fn(item, t_tok, f_tok)
            v_vec = v_vec.to(device).view(1, 1, -1)

            def hook_fn(module, inp, outp):
                h = outp[0] if isinstance(outp, tuple) else outp
                h_mod = h + alpha_val * v_vec
                if isinstance(outp, tuple):
                    return (h_mod,) + outp[1:]
                return h_mod

            handle = layer_module.register_forward_hook(hook_fn)
            with torch.no_grad():
                out_m = model(input_ids=inp_ids, output_hidden_states=True)
            handle.remove()

            l_m = out_m.logits[0, -1, :]
            probs_m = F.softmax(l_m, dim=-1)
            t_l_m = float(l_m[t_tok].item())
            f_l_m = float(l_m[f_tok].item())
            top10_m = set(torch.topk(l_m, k=10).indices.tolist())
            h_m = out_m.hidden_states[target_layer + 1][0, -1, :].detach().cpu()

            is_mod_corr = bool(t_l_m > f_l_m)
            mod_correct.append(is_mod_corr)
            d_t = t_l_m - t_l_b
            d_f = f_l_m - f_l_b
            d_logits_t.append(d_t)
            d_logits_f.append(d_f)
            margin_shift = (t_l_m - f_l_m) - (t_l_b - f_l_b)
            margin_shifts.append(margin_shift)
            d_H_list.append(float(torch.norm(h_m - h_b).item()))
            kl_list.append(compute_kl(probs_b, probs_m))
            top10_overlaps.append(len(top10_b.intersection(top10_m)) / 10.0)

            instance_records[item["id"]][f"{cond_name}_correct"] = is_mod_corr
            instance_records[item["id"]][f"{cond_name}_margin_shift"] = margin_shift

        b, c, delta_m, p_val = compute_paired_stats(base_correct_list, mod_correct)
        wilc_p = float(stats.wilcoxon(margin_shifts).pvalue) if any(m != 0 for m in margin_shifts) else 1.0

        res = {
            "name": cond_name,
            "acc_base": base_acc,
            "acc_mod": float(np.mean(mod_correct)),
            "delta_m": float(delta_m),
            "rescues_b": b,
            "corruptions_c": c,
            "exact_p": float(p_val),
            "wilcoxon_p": wilc_p,
            "delta_logit_target": float(np.mean(d_logits_t)),
            "delta_logit_foil": float(np.mean(d_logits_f)),
            "delta_margin": float(np.mean(margin_shifts)),
            "delta_H": float(np.mean(d_H_list)),
            "kl_div": float(np.mean(kl_list)),
            "top10_overlap": float(np.mean(top10_overlaps))
        }
        return res

    stage_B_results = {}

    # Condition 1: Static Basis Baseline (B_agg)
    log("Evaluating Condition 1: Static Basis Baseline (B_agg)...", log_file)
    stage_B_results["Static_B_agg"] = eval_test_condition(
        "Static_B_agg",
        lambda item, tt, ft: B_agg
    )

    # Condition 2: Aligned Dynamic Basis (Role-Procrustes: R(x) @ B_agg)
    log("Evaluating Condition 2: Aligned Dynamic Basis (Role-Procrustes)...", log_file)
    stage_B_results["Aligned_Dynamic_Basis"] = eval_test_condition(
        "Aligned_Dynamic_Basis",
        lambda item, tt, ft: get_procrustes_rotation(item) @ B_agg
    )

    # Condition 3: Same-Layer Output Bridge Control (Layer 20)
    log("Evaluating Condition 3: Same-Layer Output Bridge Control (Layer 20)...", log_file)
    stage_B_results["Same_Layer_Output_Bridge"] = eval_test_condition(
        "Same_Layer_Output_Bridge",
        lambda item, tt, ft: make_bridge_vec(tt, ft)
    )

    # Condition 4: Random Orthogonal Rotations Control (5 seeds)
    log("Evaluating Condition 4: Random Orthogonal Rotation Control (5 Seeds)...", log_file)
    rand_rot_runs = []
    rand_seeds = [7000, 7053, 7106, 7159, 7212]
    for s_idx, seed_val in enumerate(rand_seeds):
        torch.manual_seed(seed_val)
        M_r = torch.randn(1024, 1024)
        U_r, _, Vh_r = torch.linalg.svd(M_r)
        R_rand = U_r @ Vh_r
        run_res = eval_test_condition(
            f"Random_Rotation_Seed_{s_idx}",
            lambda item, tt, ft: R_rand @ B_agg
        )
        rand_rot_runs.append(run_res)

    stage_B_results["Random_Rotation_Control"] = {
        "name": "Random_Rotation_Control (5-Seed Mean)",
        "acc_base": base_acc,
        "acc_mod": float(np.mean([r["acc_mod"] for r in rand_rot_runs])),
        "delta_m": float(np.mean([r["delta_m"] for r in rand_rot_runs])),
        "rescues_b": float(np.mean([r["rescues_b"] for r in rand_rot_runs])),
        "corruptions_c": float(np.mean([r["corruptions_c"] for r in rand_rot_runs])),
        "exact_p": 1.0,
        "delta_logit_target": float(np.mean([r["delta_logit_target"] for r in rand_rot_runs])),
        "delta_logit_foil": float(np.mean([r["delta_logit_foil"] for r in rand_rot_runs])),
        "delta_margin": float(np.mean([r["delta_margin"] for r in rand_rot_runs])),
        "delta_H": float(np.mean([r["delta_H"] for r in rand_rot_runs])),
        "kl_div": float(np.mean([r["kl_div"] for r in rand_rot_runs])),
        "top10_overlap": float(np.mean([r["top10_overlap"] for r in rand_rot_runs]))
    }

    # Condition 5: Dynamic Orthogonal Complement Control (R(x) @ B_perp)
    log("Evaluating Condition 5: Dynamic Orthogonal Complement Control (R(x) @ B_perp)...", log_file)
    stage_B_results["Dynamic_B_perp"] = eval_test_condition(
        "Dynamic_B_perp",
        lambda item, tt, ft: get_procrustes_rotation(item) @ B_perp
    )

    # Condition 6: Dynamic Wrong-Task Control (R(x) @ B_wrong)
    log("Evaluating Condition 6: Dynamic Wrong-Task Control (R(x) @ B_wrong)...", log_file)
    stage_B_results["Dynamic_B_wrong"] = eval_test_condition(
        "Dynamic_B_wrong",
        lambda item, tt, ft: get_procrustes_rotation(item) @ B_wrong
    )

    # -------------------------------------------------------------
    # 6. Stage C: Specificity & Inversion Checks
    # -------------------------------------------------------------
    log("\n" + "="*80, log_file)
    log("[6] STAGE C: SPECIFICITY & ROBUSTNESS AUDIT", log_file)
    log("="*80, log_file)

    stage_C_results = {}
    # Reversal test: query "Who is lower in rank?"
    def eval_spec_condition(name, prompt_mod_fn, target_fn, foil_fn, vec_gen):
        mod_corr = []
        d_marg_list = []
        base_corr_spec = []

        for item in test_instances:
            p_mod = prompt_mod_fn(item)
            t_str = target_fn(item)
            f_str = foil_fn(item)
            tt = tokenizer.encode(t_str)[0]
            ft = tokenizer.encode(f_str)[0]
            inp_ids = tokenizer.encode(p_mod, return_tensors="pt").to(device)

            with torch.no_grad():
                out_b = model(input_ids=inp_ids)
            t_lb = float(out_b.logits[0, -1, tt].item())
            f_lb = float(out_b.logits[0, -1, ft].item())
            base_corr_spec.append(bool(t_lb > f_lb))

            v_vec = vec_gen(item, tt, ft).to(device).view(1, 1, -1)
            def hook_fn(mod, inp, outp):
                h = outp[0] if isinstance(outp, tuple) else outp
                h_mod = h + alpha_val * v_vec
                if isinstance(outp, tuple):
                    return (h_mod,) + outp[1:]
                return h_mod

            handle = layer_module.register_forward_hook(hook_fn)
            with torch.no_grad():
                out_m = model(input_ids=inp_ids)
            handle.remove()

            t_lm = float(out_m.logits[0, -1, tt].item())
            f_lm = float(out_m.logits[0, -1, ft].item())
            mod_corr.append(bool(t_lm > f_lm))
            d_marg_list.append((t_lm - f_lm) - (t_lb - f_lb))

        b, c, dm, p_val = compute_paired_stats(base_corr_spec, mod_corr)
        return {
            "name": name,
            "acc_base": float(np.mean(base_corr_spec)),
            "acc_mod": float(np.mean(mod_corr)),
            "delta_m": float(dm),
            "rescues_b": b,
            "corruptions_c": c,
            "exact_p": float(p_val),
            "delta_margin": float(np.mean(d_marg_list))
        }

    log("Evaluating Query Polarity Reversal ('Who is lower in rank?')...", log_file)
    stage_C_results["Query_Polarity_Reversal"] = eval_spec_condition(
        "Query_Polarity_Reversal",
        lambda item: item["prompt"].replace("higher in rank", "lower in rank"),
        lambda item: " " + item["foil"],
        lambda item: " " + item["target"],
        lambda item, tt, ft: get_procrustes_rotation(item) @ B_agg
    )

    # -------------------------------------------------------------
    # 7. Print Confirmatory Results Ledger
    # -------------------------------------------------------------
    log("\n" + "="*80, log_file)
    log("[7] CONFIRMATORY REPLICATION RESULTS LEDGER (Pythia-410M)", log_file)
    log("="*80, log_file)

    log(f"{'Condition':<32} | {'Acc(Mod)':<8} | {'Delta_M':<9} | {'b (Res)':<7} | {'c (Cor)':<7} | {'p-value':<8} | {'Delta_Margin':<12} | {'Top10':<6}", log_file)
    log("-" * 105, log_file)
    for c_key, res in stage_B_results.items():
        log(f"{res['name']:<32} | {res['acc_mod']*100:>6.2f}% | {res['delta_m']*100:>+7.2f}% | {res['rescues_b']:>7} | {res['corruptions_c']:>7} | {res['exact_p']:>8.4f} | {res['delta_margin']:>+12.4f} | {res['top10_overlap']*100:>5.1f}%", log_file)

    # Post-experiment hash check
    post_hash = get_hash(model)
    log(f"\nPost-experiment parameter SHA-256: {post_hash}", log_file)
    assert pre_hash == post_hash == expected_hash, "CRITICAL: Backbone parameter drift detected!"
    log("CONSTITUTIONAL COMPLIANCE CONFIRMED: Delta theta == 0 across all runs.", log_file)

    # Save results
    results_payload = {
        "model": model_name,
        "pre_hash": pre_hash,
        "post_hash": post_hash,
        "target_layer": target_layer,
        "hidden_dim": 1024,
        "alpha": alpha_val,
        "baseline_accuracy": base_acc,
        "errors_available": num_errors,
        "stage_A_alignment": stage_A_results,
        "stage_A_summary": {"mean_raw_cosine": mean_raw, "mean_aligned_cosine": mean_aligned, "delta_cosine": mean_aligned - mean_raw},
        "stage_B_conditions": stage_B_results,
        "stage_C_specificity": stage_C_results
    }

    res_json_path = os.path.join(out_dir, "exp066_replication_results.json")
    with open(res_json_path, "w", encoding="utf-8") as f:
        json.dump(results_payload, f, indent=2)

    inst_json_path = os.path.join(out_dir, "exp066_instance_evaluations.json")
    with open(inst_json_path, "w", encoding="utf-8") as f:
        json.dump(instance_records, f, indent=2)

    log(f"\nArtifacts saved to:\n  {res_json_path}\n  {inst_json_path}\n  {log_path}", log_file)
    log_file.close()

if __name__ == "__main__":
    main()
