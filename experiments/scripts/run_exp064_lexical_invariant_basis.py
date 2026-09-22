"""
EXP064: Lexical-Invariant Internal-State Basis Construction.
Preregistered Confirmatory Protocol.

Core Question:
Can SCBI construct an internal basis from multiple lexical realizations
of the same computation such that the resulting basis transfers to an unseen vocabulary?

Governing Standards:
- AGENTS.md 14 Inviolable Laws (Law 6: Frozen Backbone Delta theta = 0, Law 7: Zero Data Leakage)
- STATISTICAL_PROTOCOL_V02.md
- Protocol Spec: experiments/protocols/EXP064_LEXICAL_INVARIANT_INTERNAL_BASIS_SPEC.md
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
    out_dir = os.path.join("experiments", "runs", "EXP064_lexical_invariant_basis")
    os.makedirs(out_dir, exist_ok=True)
    log_path = os.path.join(out_dir, "exp064_run_log.txt")
    log_file = open(log_path, "w", encoding="utf-8")

    log("="*75, log_file)
    log("EXP064: Lexical-Invariant Internal-State Basis Construction", log_file)
    log("Preregistered Protocol: EXP064_LEXICAL_INVARIANT_INTERNAL_BASIS_SPEC.md", log_file)
    log("="*75, log_file)

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
    # 1. Multi-Vocabulary Support Set Construction (K=5 Vocabularies)
    # -------------------------------------------------------------
    log("\n[1] Constructing Multi-Vocabulary Support Set (N_base=30, K=5 vocabularies)...", log_file)

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
    assert len(triples_indices) == 15
    assert len(quads_indices) == 15

    # Build support instances per vocabulary
    support_data_by_vocab = {v_key: [] for v_key in support_vocabularies}
    N_base = 30

    for v_key, ents in support_vocabularies.items():
        # 15 2-hop
        for i, (iA, iB, iC) in enumerate(triples_indices):
            A, B, C = ents[iA], ents[iB], ents[iC]
            target_first = (i % 2 == 0)
            q_opts = f"{A} or {C}" if target_first else f"{C} or {A}"
            p_rel = f"Premise: {A} outranks {B}. {B} outranks {C}. Question: Who is higher in rank, {q_opts}? Answer:"
            p_neu = f"Premise: {A} is next to {B}. {B} is next to {C}. Question: Who is higher in rank, {q_opts}? Answer:"
            support_data_by_vocab[v_key].append({
                "base_id": f"base_2hop_{i}",
                "vocab": v_key,
                "prompt_rel": p_rel,
                "prompt_neutral": p_neu,
                "target": A,
                "foil": C,
                "target_token": " " + A,
                "foil_token": " " + C,
                "target_first": target_first,
                "hop": 2
            })
        # 15 3-hop
        for i, (iA, iB, iC, iD) in enumerate(quads_indices):
            A, B, C, D = ents[iA], ents[iB], ents[iC], ents[iD]
            target_first = (i % 2 == 0)
            q_opts = f"{A} or {D}" if target_first else f"{D} or {A}"
            p_rel = f"Premise: {A} outranks {B}. {B} outranks {C}. {C} outranks {D}. Question: Who is higher in rank, {q_opts}? Answer:"
            p_neu = f"Premise: {A} is next to {B}. {B} is next to {C}. {C} is next to {D}. Question: Who is higher in rank, {q_opts}? Answer:"
            support_data_by_vocab[v_key].append({
                "base_id": f"base_3hop_{i}",
                "vocab": v_key,
                "prompt_rel": p_rel,
                "prompt_neutral": p_neu,
                "target": A,
                "foil": D,
                "target_token": " " + A,
                "foil_token": " " + D,
                "target_first": target_first,
                "hop": 3
            })

    log(f"Constructed {len(support_vocabularies)} vocabularies x {N_base} support instances = {len(support_vocabularies)*N_base} total realizations.", log_file)
    log("Effective experimental unit locked: N_base = 30 support base instances (augmentations do not increase degrees of freedom).", log_file)

    # -------------------------------------------------------------
    # 2. Extract Internal Hidden States at Layer 10 (Locked Layer)
    # -------------------------------------------------------------
    target_layer = 10
    layer_module = model.gpt_neox.layers[target_layer]
    log(f"\n[2] Extracting internal hidden states at Layer {target_layer} across all vocabularies...", log_file)

    delta_h_by_vocab = {v_key: [] for v_key in support_vocabularies}

    for v_key, instances in support_data_by_vocab.items():
        for item in instances:
            inp_rel = tokenizer.encode(item["prompt_rel"], return_tensors="pt").to(device)
            inp_neu = tokenizer.encode(item["prompt_neutral"], return_tensors="pt").to(device)
            with torch.no_grad():
                out_rel = model(input_ids=inp_rel, output_hidden_states=True)
                out_neu = model(input_ids=inp_neu, output_hidden_states=True)
            h_rel = out_rel.hidden_states[target_layer + 1][0, -1, :].detach().cpu()
            h_neu = out_neu.hidden_states[target_layer + 1][0, -1, :].detach().cpu()
            delta_h = h_rel - h_neu
            delta_h_by_vocab[v_key].append(delta_h)
        delta_h_by_vocab[v_key] = torch.stack(delta_h_by_vocab[v_key]) # [30, 768]

    # Compute per-vocabulary normalized mean directions (v_k)
    v_hat_by_vocab = {}
    for v_key, dH in delta_h_by_vocab.items():
        norms = torch.norm(dH, dim=1, keepdim=True) + 1e-12
        normalized_dH = dH / norms
        mean_v = normalized_dH.mean(dim=0)
        v_hat = mean_v / (torch.norm(mean_v) + 1e-12)
        v_hat_by_vocab[v_key] = v_hat

    # -------------------------------------------------------------
    # 3. Pre-Intervention Representation-Alignment Diagnostic
    # -------------------------------------------------------------
    log("\n" + "="*75, log_file)
    log("[3] PRE-INTERVENTION DIAGNOSTIC: CROSS-VOCABULARY REPRESENTATION ALIGNMENT", log_file)
    log("="*75, log_file)

    vocab_keys = list(support_vocabularies.keys())
    K = len(vocab_keys)
    cosine_matrix = np.zeros((K, K))

    for i in range(K):
        for j in range(K):
            v_i = v_hat_by_vocab[vocab_keys[i]]
            v_j = v_hat_by_vocab[vocab_keys[j]]
            cos_sim = float(torch.dot(v_i, v_j).item())
            cosine_matrix[i, j] = cos_sim

    log(f"Pairwise Directional Cosine Matrix across K={K} support vocabularies:", log_file)
    header = f"{'':<14} | " + " | ".join([f"{k[:9]:<9}" for k in vocab_keys])
    log(header, log_file)
    log("-" * len(header), log_file)
    for i in range(K):
        row_str = f"{vocab_keys[i]:<14} | " + " | ".join([f"{cosine_matrix[i, j]:>+9.4f}" for j in range(K)])
        log(row_str, log_file)

    # Extract off-diagonal cosine values
    off_diag_cosines = []
    for i in range(K):
        for j in range(i + 1, K):
            off_diag_cosines.append(cosine_matrix[i, j])

    mean_off_diag = float(np.mean(off_diag_cosines))
    std_off_diag = float(np.std(off_diag_cosines))
    min_off_diag = float(np.min(off_diag_cosines))
    max_off_diag = float(np.max(off_diag_cosines))

    # Empirical random null distribution in R^768
    torch.manual_seed(42)
    rand_samples_1 = torch.randn(10000, 768)
    rand_samples_1 /= torch.norm(rand_samples_1, dim=1, keepdim=True)
    rand_samples_2 = torch.randn(10000, 768)
    rand_samples_2 /= torch.norm(rand_samples_2, dim=1, keepdim=True)
    rand_null_cosines = (rand_samples_1 * rand_samples_2).sum(dim=1).numpy()
    null_mean = float(np.mean(rand_null_cosines))
    null_std = float(np.std(rand_null_cosines))

    t_stat, p_alignment = stats.ttest_1samp(off_diag_cosines, 0.0)

    log(f"\nEmpirical Random Null Distribution (R^768): mean = {null_mean:+.6f}, std = {null_std:.6f}", log_file)
    log(f"Observed Off-Diagonal Cosines (n={len(off_diag_cosines)} pairs):", log_file)
    log(f"  Mean Cosine:  {mean_off_diag:>+6.4f} +/- {std_off_diag:.4f}", log_file)
    log(f"  Range:        [{min_off_diag:>+6.4f}, {max_off_diag:>+6.4f}]", log_file)
    log(f"  t-statistic:  {t_stat:.4f} (p = {p_alignment:.6e})", log_file)

    # Adjudicate Level A
    level_A_passed = bool(mean_off_diag > 0.20 and p_alignment < 0.001)
    log(f"\nPre-Intervention Alignment Thresholds:", log_file)
    log(f"  Strong Alignment (>= 0.40):         {'MET' if mean_off_diag >= 0.40 else 'NOT MET'}", log_file)
    log(f"  Moderate Alignment (0.15 - 0.40):   {'MET' if 0.15 <= mean_off_diag < 0.40 else 'NOT MET'}", log_file)
    log(f"  Orthogonal Disconnect (< 0.10):     {'MET' if mean_off_diag < 0.10 else 'NOT MET'}", log_file)
    log(f"LEVEL A CLASSIFICATION (Cross-Vocabulary Alignment): {'PASSED' if level_A_passed else 'FAILED'}", log_file)

    # -------------------------------------------------------------
    # 4. Candidate Internal Basis Constructions
    # -------------------------------------------------------------
    log("\n" + "="*75, log_file)
    log("[4] CONSTRUCTING CANDIDATE INTERNAL BASIS FAMILIES & CONTROLS", log_file)
    log("="*75, log_file)

    candidate_bases = {}

    # A. B_single-SVD: SVD on V1_Anglo contrasts
    dH_v1 = delta_h_by_vocab["V1_Anglo"] # [30, 768]
    _, _, Vh_v1 = torch.linalg.svd(dH_v1, full_matrices=False)
    b_single_svd = Vh_v1[0, :].clone()
    b_single_svd /= torch.norm(b_single_svd)
    candidate_bases["B_single_SVD"] = b_single_svd

    # B. B_single-centroid: Exact EXP063 winning centroid basis on V1_Anglo
    b_single_cent = v_hat_by_vocab["V1_Anglo"].clone()
    candidate_bases["B_single_centroid"] = b_single_cent

    # C. B_pool: SVD on all pooled contrasts across all K=5 vocabularies (150 contrasts)
    all_dH = torch.cat([delta_h_by_vocab[k] for k in vocab_keys], dim=0) # [150, 768]
    _, _, Vh_pool = torch.linalg.svd(all_dH, full_matrices=False)
    b_pool = Vh_pool[0, :].clone()
    b_pool /= torch.norm(b_pool)
    candidate_bases["B_pool"] = b_pool

    # D. B_agg: Per-vocabulary normalized aggregation
    sum_v = torch.stack(list(v_hat_by_vocab.values())).sum(dim=0)
    b_agg = sum_v / (torch.norm(sum_v) + 1e-12)
    candidate_bases["B_agg"] = b_agg

    # E. B_perp: Orthonormal vector in ker(B_agg^T)
    torch.manual_seed(9876)
    r_orth = torch.randn(768)
    r_orth -= b_agg * torch.dot(b_agg, r_orth)
    r_orth /= torch.norm(r_orth)
    assert abs(float(torch.dot(b_agg, r_orth).item())) < 1e-6
    candidate_bases["B_perp"] = r_orth

    # F. B_wrong-task: Internal contrast from unrelated Level 0 factual recall
    p_wrong_rel = "Fact: Paris is the capital of France. Question: What is the capital of France, Paris or London? Answer:"
    p_wrong_neu = "Fact: Paris is near London. Question: What is the capital of France, Paris or London? Answer:"
    with torch.no_grad():
        out_wr_rel = model(input_ids=tokenizer.encode(p_wrong_rel, return_tensors="pt").to(device), output_hidden_states=True)
        out_wr_neu = model(input_ids=tokenizer.encode(p_wrong_neu, return_tensors="pt").to(device), output_hidden_states=True)
    dH_wrong = out_wr_rel.hidden_states[target_layer + 1][0, -1, :].detach().cpu() - out_wr_neu.hidden_states[target_layer + 1][0, -1, :].detach().cpu()
    b_wrong = dH_wrong / (torch.norm(dH_wrong) + 1e-12)
    candidate_bases["B_wrong_task"] = b_wrong

    # G. B_random: 5-seed random null distribution
    K_rand = 5
    rand_bases = []
    for k_seed in range(K_rand):
        torch.manual_seed(5000 + k_seed * 43)
        r = torch.randn(768)
        r /= torch.norm(r)
        rand_bases.append(r)

    # Geometry checks: Cosines between candidate bases
    log(f"Basis Vector Geometry & Similarities:", log_file)
    log(f"  cos(B_single_SVD, B_pool):         {float(torch.dot(b_single_svd, b_pool).item()):>+7.4f}", log_file)
    log(f"  cos(B_single_centroid, B_agg):     {float(torch.dot(b_single_cent, b_agg).item()):>+7.4f}", log_file)
    log(f"  cos(B_pool, B_agg):                {float(torch.dot(b_pool, b_agg).item()):>+7.4f}", log_file)
    log(f"  cos(B_agg, B_perp):                {float(torch.dot(b_agg, r_orth).item()):>+7.4f} (strictly zero check)", log_file)
    log(f"  cos(B_agg, B_wrong_task):          {float(torch.dot(b_agg, b_wrong).item()):>+7.4f}", log_file)

    # -------------------------------------------------------------
    # 5. Held-Out Confirmatory Dataset (N=60, Unseen Vocabulary)
    # -------------------------------------------------------------
    log("\n" + "="*75, log_file)
    log("[5] CONSTRUCTING HELD-OUT CONFIRMATORY DATASET (N=60 INDEPENDENT INSTANCES)", log_file)
    log("="*75, log_file)

    novel_vocab_planet = ["Mars", "Venus", "Jupiter", "Saturn", "Mercury"]
    novel_vocab_element = ["Iron", "Gold", "Silver", "Bronze", "Steel"]

    heldout_test_data = []

    # 30 instances on Planetary entities (15 2-hop, 15 3-hop)
    for i, (iA, iB, iC) in enumerate(triples_indices):
        A, B, C = novel_vocab_planet[iA], novel_vocab_planet[iB], novel_vocab_planet[iC]
        target_first = (i % 2 == 1) # Alternating order
        q_opts = f"{A} or {C}" if target_first else f"{C} or {A}"
        p = f"Premise: {A} outranks {B}. {B} outranks {C}. Question: Who is higher in rank, {q_opts}? Answer:"
        heldout_test_data.append({
            "id": f"novel_planet_2hop_{i}",
            "domain": "Planetary",
            "prompt": p,
            "target": A,
            "foil": C,
            "target_token": " " + A,
            "foil_token": " " + C,
            "target_first": target_first,
            "hop": 2
        })
    for i, (iA, iB, iC, iD) in enumerate(quads_indices):
        A, B, C, D = novel_vocab_planet[iA], novel_vocab_planet[iB], novel_vocab_planet[iC], novel_vocab_planet[iD]
        target_first = (i % 2 == 1)
        q_opts = f"{A} or {D}" if target_first else f"{D} or {A}"
        p = f"Premise: {A} outranks {B}. {B} outranks {C}. {C} outranks {D}. Question: Who is higher in rank, {q_opts}? Answer:"
        heldout_test_data.append({
            "id": f"novel_planet_3hop_{i}",
            "domain": "Planetary",
            "prompt": p,
            "target": A,
            "foil": D,
            "target_token": " " + A,
            "foil_token": " " + D,
            "target_first": target_first,
            "hop": 3
        })

    # 30 instances on Elemental entities (15 2-hop, 15 3-hop)
    for i, (iA, iB, iC) in enumerate(triples_indices):
        A, B, C = novel_vocab_element[iA], novel_vocab_element[iB], novel_vocab_element[iC]
        target_first = (i % 2 == 0)
        q_opts = f"{A} or {C}" if target_first else f"{C} or {A}"
        p = f"Premise: {A} outranks {B}. {B} outranks {C}. Question: Who is higher in rank, {q_opts}? Answer:"
        heldout_test_data.append({
            "id": f"novel_element_2hop_{i}",
            "domain": "Elemental",
            "prompt": p,
            "target": A,
            "foil": C,
            "target_token": " " + A,
            "foil_token": " " + C,
            "target_first": target_first,
            "hop": 2
        })
    for i, (iA, iB, iC, iD) in enumerate(quads_indices):
        A, B, C, D = novel_vocab_element[iA], novel_vocab_element[iB], novel_vocab_element[iC], novel_vocab_element[iD]
        target_first = (i % 2 == 0)
        q_opts = f"{A} or {D}" if target_first else f"{D} or {A}"
        p = f"Premise: {A} outranks {B}. {B} outranks {C}. {C} outranks {D}. Question: Who is higher in rank, {q_opts}? Answer:"
        heldout_test_data.append({
            "id": f"novel_element_3hop_{i}",
            "domain": "Elemental",
            "prompt": p,
            "target": A,
            "foil": D,
            "target_token": " " + A,
            "foil_token": " " + D,
            "target_first": target_first,
            "hop": 3
        })

    assert len(heldout_test_data) == 60, f"Expected 60 heldout test instances, got {len(heldout_test_data)}"
    log(f"Generated N={len(heldout_test_data)} independent confirmatory held-out instances on unseen vocabulary (Planetary + Elemental).", log_file)

    # -------------------------------------------------------------
    # 6. Baseline Evaluation on Held-Out Test Set (N=60)
    # -------------------------------------------------------------
    log("\n" + "="*75, log_file)
    log("[6] BASELINE EVALUATION ON HELD-OUT UNSEEN VOCABULARY (N=60)", log_file)
    log("="*75, log_file)

    test_base_correct = []
    test_h_base = []

    for item in heldout_test_data:
        inp_ids = tokenizer.encode(item["prompt"], return_tensors="pt").to(device)
        t_tok = tokenizer.encode(item["target_token"])[0]
        f_tok = tokenizer.encode(item["foil_token"])[0]
        with torch.no_grad():
            out = model(input_ids=inp_ids, output_hidden_states=True)
        t_logit = float(out.logits[0, -1, t_tok].item())
        f_logit = float(out.logits[0, -1, f_tok].item())
        test_base_correct.append(bool(t_logit > f_logit))
        test_h_base.append(out.hidden_states[target_layer + 1][0, -1, :].detach().cpu())

    test_base_acc = float(np.mean(test_base_correct))
    log(f"Baseline Novel Vocabulary Accuracy: {test_base_acc*100:.2f}% ({sum(test_base_correct)}/60)", log_file)

    # -------------------------------------------------------------
    # 7. Evaluation of the 8 Mandatory Comparative Conditions (N=60)
    # -------------------------------------------------------------
    log("\n" + "="*75, log_file)
    log("[7] EVALUATING THE 8 MANDATORY COMPARATIVE CONDITIONS ON NOVEL VOCABULARY", log_file)
    log("="*75, log_file)

    alpha_lock = 0.50 # Standard locked intervention strength (matches EXP063)

    def eval_condition(cond_name, hook_fn_generator, prompt_fn=None, target_fn=None, foil_fn=None):
        mod_correct = []
        d_logits_t = []
        d_logits_f = []
        d_H_list = []
        kl_list = []
        top10_overlaps = []
        
        curr_base_correct = []

        for idx, item in enumerate(heldout_test_data):
            p_text = prompt_fn(item, idx) if prompt_fn else item["prompt"]
            t_str = target_fn(item, idx) if target_fn else item["target_token"]
            f_str = foil_fn(item, idx) if foil_fn else item["foil_token"]

            inp_ids = tokenizer.encode(p_text, return_tensors="pt").to(device)
            t_tok = tokenizer.encode(t_str)[0]
            f_tok = tokenizer.encode(f_str)[0]

            with torch.no_grad():
                out_b = model(input_ids=inp_ids, output_hidden_states=True)
            l_b = out_b.logits[0, -1, :]
            probs_b = F.softmax(l_b, dim=-1)
            t_l_b = float(l_b[t_tok].item())
            f_l_b = float(l_b[f_tok].item())
            top10_b = set(torch.topk(l_b, k=10).indices.tolist())
            h_b = out_b.hidden_states[target_layer + 1][0, -1, :].detach().cpu()
            curr_base_correct.append(bool(t_l_b > f_l_b))

            # Intervened forward pass
            hook = hook_fn_generator(idx, item, t_tok, f_tok)
            handle = layer_module.register_forward_hook(hook)
            with torch.no_grad():
                out_m = model(input_ids=inp_ids, output_hidden_states=True)
            handle.remove()

            l_m = out_m.logits[0, -1, :]
            probs_m = F.softmax(l_m, dim=-1)
            t_l_m = float(l_m[t_tok].item())
            f_l_m = float(l_m[f_tok].item())
            top10_m = set(torch.topk(l_m, k=10).indices.tolist())
            h_m = out_m.hidden_states[target_layer + 1][0, -1, :].detach().cpu()

            mod_correct.append(bool(t_l_m > f_l_m))
            d_logits_t.append(t_l_m - t_l_b)
            d_logits_f.append(f_l_m - f_l_b)
            d_H_list.append(float(torch.norm(h_m - h_b).item()))
            kl_list.append(compute_kl(probs_b, probs_m))
            top10_overlaps.append(len(top10_b.intersection(top10_m)) / 10.0)

        b, c, delta_m, p_val = compute_paired_stats(curr_base_correct, mod_correct)
        res = {
            "name": cond_name,
            "acc_base": float(np.mean(curr_base_correct)),
            "acc_mod": float(np.mean(mod_correct)),
            "delta_m": float(delta_m),
            "rescues_b": b,
            "corruptions_c": c,
            "exact_p": float(p_val),
            "delta_logit_target": float(np.mean(d_logits_t)),
            "delta_logit_foil": float(np.mean(d_logits_f)),
            "delta_margin": float(np.mean(np.array(d_logits_t) - np.array(d_logits_f))),
            "delta_H": float(np.mean(d_H_list)),
            "kl_div": float(np.mean(kl_list)),
            "top10_overlap": float(np.mean(top10_overlaps))
        }
        return res

    def make_vector_injection_hook(vec):
        v = vec.to(device).view(1, 1, -1)
        def hook(module, inp, outp):
            h = outp[0] if isinstance(outp, tuple) else outp
            h_mod = h + alpha_lock * v
            if isinstance(outp, tuple):
                return (h_mod,) + outp[1:]
            return h_mod
        return hook

    condition_results = {}

    # Condition 1: B_single_SVD
    log("Evaluating Condition 1: B_single_SVD...", log_file)
    condition_results["B_single_SVD"] = eval_condition(
        "B_single_SVD",
        lambda idx, item, tt, ft: make_vector_injection_hook(candidate_bases["B_single_SVD"])
    )

    # Condition 2: B_single_centroid (EXP063 winning basis)
    log("Evaluating Condition 2: B_single_centroid (EXP063 Internal Basis)...", log_file)
    condition_results["B_single_centroid"] = eval_condition(
        "B_single_centroid",
        lambda idx, item, tt, ft: make_vector_injection_hook(candidate_bases["B_single_centroid"])
    )

    # Condition 3: B_pool (Pooled Multi-Vocab SVD)
    log("Evaluating Condition 3: B_pool (Pooled Multi-Vocab SVD)...", log_file)
    condition_results["B_pool"] = eval_condition(
        "B_pool",
        lambda idx, item, tt, ft: make_vector_injection_hook(candidate_bases["B_pool"])
    )

    # Condition 4: B_agg (Normalized Multi-Vocab Aggregation)
    log("Evaluating Condition 4: B_agg (Normalized Multi-Vocab Aggregation)...", log_file)
    condition_results["B_agg"] = eval_condition(
        "B_agg",
        lambda idx, item, tt, ft: make_vector_injection_hook(candidate_bases["B_agg"])
    )

    # Condition 5: B_random (5-seed random null distribution)
    log("Evaluating Condition 5: B_random (5-Seed Random Null)...", log_file)
    rand_runs = []
    for k_s, r_vec in enumerate(rand_bases):
        r_res = eval_condition(
            f"B_random_seed_{k_s}",
            lambda idx, item, tt, ft: make_vector_injection_hook(r_vec)
        )
        rand_runs.append(r_res)
    mean_rand_dm = float(np.mean([r["delta_m"] for r in rand_runs]))
    mean_rand_b = float(np.mean([r["rescues_b"] for r in rand_runs]))
    mean_rand_c = float(np.mean([r["corruptions_c"] for r in rand_runs]))
    mean_rand_acc = float(np.mean([r["acc_mod"] for r in rand_runs]))
    mean_rand_dH = float(np.mean([r["delta_H"] for r in rand_runs]))
    condition_results["B_random"] = {
        "name": "B_random (5-Seed Mean)",
        "acc_base": test_base_acc,
        "acc_mod": mean_rand_acc,
        "delta_m": mean_rand_dm,
        "rescues_b": mean_rand_b,
        "corruptions_c": mean_rand_c,
        "exact_p": 1.0 if mean_rand_b == mean_rand_c else float(stats.binomtest(int(round(min(mean_rand_b, mean_rand_c))), int(round(mean_rand_b + mean_rand_c)), 0.5).pvalue),
        "delta_logit_target": float(np.mean([r["delta_logit_target"] for r in rand_runs])),
        "delta_logit_foil": float(np.mean([r["delta_logit_foil"] for r in rand_runs])),
        "delta_margin": float(np.mean([r["delta_margin"] for r in rand_runs])),
        "delta_H": mean_rand_dH,
        "kl_div": float(np.mean([r["kl_div"] for r in rand_runs])),
        "top10_overlap": float(np.mean([r["top10_overlap"] for r in rand_runs]))
    }

    # Condition 6: B_perp (Orthogonal Complement)
    log("Evaluating Condition 6: B_perp (Orthogonal Complement)...", log_file)
    condition_results["B_perp"] = eval_condition(
        "B_perp",
        lambda idx, item, tt, ft: make_vector_injection_hook(candidate_bases["B_perp"])
    )

    # Condition 7: B_wrong_task (Internal Basis from Unrelated Task)
    log("Evaluating Condition 7: B_wrong_task (Unrelated Lexical Recall)...", log_file)
    condition_results["B_wrong_task"] = eval_condition(
        "B_wrong_task",
        lambda idx, item, tt, ft: make_vector_injection_hook(candidate_bases["B_wrong_task"])
    )

    # Condition 8: Same-Layer Output Bridge Control (v_output at Layer 10)
    log("Evaluating Condition 8: Same-Layer Output Bridge Control (v_output at Layer 10)...", log_file)
    def make_same_layer_output_bridge_hook(tt, ft):
        w_diff = model.embed_out.weight[tt, :] - model.embed_out.weight[ft, :]
        v_out = w_diff / (torch.norm(w_diff) + 1e-8)
        v_out = v_out.to(device).view(1, 1, -1)
        def hook(module, inp, outp):
            h = outp[0] if isinstance(outp, tuple) else outp
            h_mod = h + alpha_lock * v_out
            if isinstance(outp, tuple):
                return (h_mod,) + outp[1:]
            return h_mod
        return hook

    condition_results["Same_Layer_Output_Bridge"] = eval_condition(
        "Same_Layer_Output_Bridge",
        lambda idx, item, tt, ft: make_same_layer_output_bridge_hook(tt, ft)
    )

    # -------------------------------------------------------------
    # 8. Counterfactual Specificity Controls on Novel Vocabulary
    # -------------------------------------------------------------
    log("\n" + "="*75, log_file)
    log("[8] EVALUATING COUNTERFACTUAL SPECIFICITY CONTROLS FOR B_agg", log_file)
    log("="*75, log_file)

    # Control A: Premise Reversal (C < B < A)
    log("Evaluating Specificity Control: Premise Reversal...", log_file)
    def rev_prompt(item, idx):
        p = item["prompt"]
        t = item["target"]
        f = item["foil"]
        return p.replace(t, "___TMP___").replace(f, t).replace("___TMP___", f)

    condition_results["B_agg_Premise_Reversal"] = eval_condition(
        "B_agg_Premise_Reversal",
        lambda idx, item, tt, ft: make_vector_injection_hook(candidate_bases["B_agg"]),
        prompt_fn=rev_prompt,
        target_fn=lambda item, idx: item["foil_token"],
        foil_fn=lambda item, idx: item["target_token"]
    )

    # Control B: Query Polarity Reversal ("Who is lower in rank?")
    log("Evaluating Specificity Control: Query Polarity Reversal...", log_file)
    def pol_prompt(item, idx):
        return item["prompt"].replace("Who is higher in rank", "Who is lower in rank")

    condition_results["B_agg_Polarity_Reversal"] = eval_condition(
        "B_agg_Polarity_Reversal",
        lambda idx, item, tt, ft: make_vector_injection_hook(candidate_bases["B_agg"]),
        prompt_fn=pol_prompt,
        target_fn=lambda item, idx: item["foil_token"],
        foil_fn=lambda item, idx: item["target_token"]
    )

    # Also evaluate single centroid under premise reversal for comparison
    condition_results["B_single_Premise_Reversal"] = eval_condition(
        "B_single_Premise_Reversal",
        lambda idx, item, tt, ft: make_vector_injection_hook(candidate_bases["B_single_centroid"]),
        prompt_fn=rev_prompt,
        target_fn=lambda item, idx: item["foil_token"],
        foil_fn=lambda item, idx: item["target_token"]
    )

    # -------------------------------------------------------------
    # 9. Summary Table & Epistemological Adjudication
    # -------------------------------------------------------------
    log("\n" + "="*85, log_file)
    log("EXP064 SUMMARY OF RESULTS: NOVEL VOCABULARY CAUSAL TRANSFER (N=60)", log_file)
    log("="*85, log_file)

    log(f"{'Condition':<28} | {'Acc Base':<8} | {'Acc Mod':<8} | {'Delta_M':<9} | {'b (res)':<7} | {'c (crp)':<7} | {'Exact p':<8} | {'Delta_Marg':<10} | {'D_KL':<7}", log_file)
    log("-" * 110, log_file)
    for c_key, r in condition_results.items():
        log(f"{r['name']:<28} | {r['acc_base']*100:>7.1f}% | {r['acc_mod']*100:>7.1f}% | {r['delta_m']*100:>+8.1f}% | {r['rescues_b']:>7} | {r['corruptions_c']:>7} | {r['exact_p']:>8.4f} | {r['delta_margin']:>+10.4f} | {r['kl_div']:>7.4f}", log_file)

    # Statistical Tests for Hypotheses
    d_m_agg = condition_results["B_agg"]["delta_m"]
    p_agg = condition_results["B_agg"]["exact_p"]
    d_m_single_cent = condition_results["B_single_centroid"]["delta_m"]
    d_m_single_svd = condition_results["B_single_SVD"]["delta_m"]
    d_m_pool = condition_results["B_pool"]["delta_m"]
    d_m_bridge = condition_results["Same_Layer_Output_Bridge"]["delta_m"]

    # Level B Check
    level_B_passed = bool(d_m_agg > 0 and p_agg < 0.05 and d_m_agg > d_m_single_cent and d_m_agg > d_m_single_svd)
    
    # Level C Check
    rev_dm = condition_results["B_agg_Premise_Reversal"]["delta_m"]
    pol_dm = condition_results["B_agg_Polarity_Reversal"]["delta_m"]
    level_C_passed = bool(level_B_passed and rev_dm >= 0.0 and pol_dm <= 0.0 and d_m_agg >= d_m_bridge)

    log("\n" + "="*85, log_file)
    log("EPISTEMOLOGICAL CLAIM ADJUDICATION (LEVELS A, B, C)", log_file)
    log("="*85, log_file)
    log(f"Level A (Cross-Vocabulary Alignment):      {'PASSED' if level_A_passed else 'FAILED'} (mean cosine = {mean_off_diag:>+6.4f}, p = {p_alignment:.2e})", log_file)
    log(f"Level B (Cross-Vocabulary Causal Transfer): {'PASSED' if level_B_passed else 'FAILED'} (B_agg Delta_M = {d_m_agg*100:+.1f}pp, p = {p_agg:.4f} vs B_single {d_m_single_cent*100:+.1f}pp)", log_file)
    log(f"Level C (Lexically Invariant Control):      {'PASSED' if level_C_passed else 'FAILED'}", log_file)

    # Scientific Fork Decision
    log("\n" + "="*85, log_file)
    log("PRE-REGISTERED SCIENTIFIC FORK DECISION FOR EXP065", log_file)
    log("="*85, log_file)
    if level_B_passed:
        fork_decision = "Outcome 1: Cross-Vocabulary Basis Aggregation Succeeded. EXP065 targets specificity, multi-hop depth, and circuit mechanics."
    else:
        fork_decision = "Outcome 2: Cross-Vocabulary Linear Aggregation Failed (Delta_M <= 0 or not superior to single-vocab). EXP065 formalizes a Temporary Coordinate Alignment Operator (A_k: h_k -> h_tilde_k -> B)."
    log(fork_decision, log_file)

    # Post-experiment parameter immutability check
    post_hash = get_hash(model)
    log(f"\nPost-experiment parameter SHA-256: {post_hash}", log_file)
    assert post_hash == expected_hash, f"CRITICAL: Model weights changed! Expected {expected_hash}, got {post_hash}"
    log("VERIFIED: Model parameters remained strictly frozen throughout experiment (Delta theta = 0).", log_file)

    # Save structured JSON
    results_json = {
        "experiment": "EXP064",
        "model": model_name,
        "pre_hash": pre_hash,
        "post_hash": post_hash,
        "layer": target_layer,
        "operator": "O2_injection",
        "alpha": alpha_lock,
        "sample_size_heldout": len(heldout_test_data),
        "effective_units": N_base,
        "support_vocabularies": list(support_vocabularies.keys()),
        "pre_intervention_alignment": {
            "cosine_matrix": cosine_matrix.tolist(),
            "mean_off_diagonal": mean_off_diag,
            "std_off_diagonal": std_off_diag,
            "min_off_diagonal": min_off_diag,
            "max_off_diagonal": max_off_diag,
            "null_mean": null_mean,
            "null_std": null_std,
            "t_stat": float(t_stat),
            "p_value": float(p_alignment),
            "level_A_passed": level_A_passed
        },
        "condition_results": condition_results,
        "epistemological_status": {
            "level_A_passed": level_A_passed,
            "level_B_passed": level_B_passed,
            "level_C_passed": level_C_passed,
            "fork_decision": fork_decision
        }
    }

    json_path = os.path.join(out_dir, "exp064_results.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results_json, f, indent=2)
    log(f"\nStructured results written to: {json_path}", log_file)
    log_file.close()

if __name__ == "__main__":
    main()
