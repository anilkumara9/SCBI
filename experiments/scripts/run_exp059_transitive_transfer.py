"""
EXP059: Transitive Relational Transfer Across Disjoint Surface Domains.
Tests whether an inference-time discovered intervention encodes an abstract relational structure
(strict transitive ordering: A > B and B > C => A > C) and transfers zero-shot across
deliberately disjoint surface vocabularies without parameter updates (Delta_theta = 0).
Pre-Registration: EXP059_TRANSITIVE_RELATION_TRANSFER_SPEC.md
Governing Standard: AGENTS.md Laws 1, 2, 6, 7, 9, 13, 14.
"""
import os, sys, json, hashlib, time
import numpy as np
import torch
import torch.nn.functional as F
from datetime import datetime, timezone
from scipy.stats import binomtest
from transformers import AutoModelForCausalLM, AutoTokenizer

os.environ["TRANSFORMERS_NO_TF"] = "1"
os.environ["USE_TF"] = "0"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from experiments.benchmarks.bench_006_transitive_relations import generate_bench_006_transitive

CANONICAL_MODEL = "EleutherAI/pythia-160m"
CANONICAL_HASH  = "54c88fa4897785f2bd94b32d26de1f73f1052bcc42124d563d0cda96940de936"
TARGET_BLOCK    = 7       # Layer 8 (0-indexed Block 7)
ALPHA           = 0.25
OUT_DIR         = os.path.join(os.path.dirname(__file__), "../../experiments/runs/EXP059_transitive_transfer")

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
    ts = datetime.now(timezone.utc).strftime("%H:%M:%S")
    formatted = f"[{ts}] {msg}"
    print(formatted, flush=True)
    if log_file:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(formatted + "\n")

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    log_file = os.path.join(OUT_DIR, "exp059_run_log.txt")
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(f"=== EXP059 Execution Started at {datetime.now(timezone.utc).isoformat()} ===\n")

    log("Initializing EXP059 Transitive Relational Transfer...", log_file)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    log(f"Using compute device: {device}", log_file)

    tokenizer = AutoTokenizer.from_pretrained(CANONICAL_MODEL)
    model = AutoModelForCausalLM.from_pretrained(CANONICAL_MODEL).to(device)
    model.eval()

    pre_hash = get_hash(model)
    assert pre_hash == CANONICAL_HASH, f"Hash mismatch: {pre_hash}"
    log("Pre-run model hash verified: Delta_theta = 0.", log_file)

    dataset = generate_bench_006_transitive()
    log(f"Loaded {len(dataset)} instances across 5 domains in BENCH-006.", log_file)

    # 1. PHASE 1: DISCOVERY & SELECTION ON DOMAIN 0 (SOCIAL)
    disc_data = [d for d in dataset if d["domain"] == "domain0_discovery_social"]
    disc_valid = [d for d in disc_data if d["is_valid_transitive"]]
    disc_control = [d for d in disc_data if not d["is_valid_transitive"]]

    log(f"Phase 1: Generating candidate interventions from Domain 0 ({len(disc_valid)} valid, {len(disc_control)} control)...", log_file)

    # Capture unperturbed activations on Discovery items
    act_records = []
    for inst in disc_valid:
        enc = tokenizer(inst["prompt"], return_tensors="pt")
        inp_ids = enc.input_ids.to(device)
        cap = {}
        def hook_fn(mod, inp, outp):
            cap["h"] = (outp[0] if isinstance(outp, tuple) else outp).detach().squeeze(0)
        handle = model.gpt_neox.layers[TARGET_BLOCK].register_forward_hook(hook_fn)
        with torch.no_grad():
            out = model(input_ids=inp_ids)
        handle.remove()
        act_records.append((cap["h"], inst))

    # Candidate 1: Contrastive Mean Direction Vector v_caa = mean(h_target) - mean(h_foil)
    t_acts, f_acts = [], []
    for h_seq, inst in act_records:
        t_tok = tokenizer.encode(inst["target_token"])[0]
        f_tok = tokenizer.encode(inst["foil_token"])[0]
        # Query token representation at final position
        h_last = h_seq[-1, :]
        if inst["task_type"] == "transitive_forward":
            t_acts.append(h_last)
        else:
            f_acts.append(h_last)

    if t_acts and f_acts:
        mean_t = torch.stack(t_acts).mean(dim=0)
        mean_f = torch.stack(f_acts).mean(dim=0)
        v_diff = mean_t - mean_f
        v_diff = v_diff / (torch.norm(v_diff) + 1e-8)
    else:
        v_diff = torch.randn(model.config.hidden_size, device=device)
        v_diff = v_diff / torch.norm(v_diff)

    # Candidate 2: Subspace Projection (Top 2 SVD components of forward activation differences)
    diffs = torch.stack([h[-1, :] - h[0, :] for h, _ in act_records])
    _, _, Vh = torch.linalg.svd(diffs - diffs.mean(dim=0, keepdim=True), full_matrices=False)
    V_subspace = Vh[:2, :].T
    P_subspace = (V_subspace @ V_subspace.T).to(device)

    # Candidate 3: Soft Conceptor Operator (Jaeger 2014)
    # C = R (R + lambda^-2 I)^-1 where R = 1/N sum(h h^T)
    H_mat = torch.stack([h[-1, :] for h, _ in act_records])
    R_cov = (H_mat.T @ H_mat) / H_mat.shape[0]
    lam_inv2 = 1.0 / (8.0 ** 2)
    C_conceptor = R_cov @ torch.linalg.inv(R_cov + lam_inv2 * torch.eye(R_cov.shape[0], device=device))

    candidates = {
        "contrastive_vector": ("vector", v_diff),
        "subspace_projection": ("matrix", P_subspace),
        "soft_conceptor": ("matrix", C_conceptor)
    }

    # Evaluate candidates on Domain 0 using Grounded Margin Utility
    log("Evaluating candidates on Domain 0 grounded margin utility...", log_file)
    cand_margins = {}

    for c_name, (c_kind, c_op) in candidates.items():
        margins = []
        for inst in disc_valid:
            enc = tokenizer(inst["prompt"], return_tensors="pt")
            inp_ids = enc.input_ids.to(device)
            t_id = tokenizer.encode(inst["target_token"])[0]
            f_id = tokenizer.encode(inst["foil_token"])[0]

            def make_hook(kind=c_kind, op=c_op):
                def h_hook(mod, inp, outp):
                    h = outp[0].clone() if isinstance(outp, tuple) else outp.clone()
                    if kind == "vector":
                        h[0, -1, :] = h[0, -1, :] + ALPHA * op
                    elif kind == "matrix":
                        h[0, -1, :] = h[0, -1, :] + ALPHA * (h[0, -1, :] @ op)
                    return (h,) + outp[1:] if isinstance(outp, tuple) else h
                return h_hook

            h_handle = model.gpt_neox.layers[TARGET_BLOCK].register_forward_hook(make_hook())
            with torch.no_grad():
                l_c = model(input_ids=inp_ids).logits[0, -1, :]
            h_handle.remove()

            margin = (l_c[t_id] - l_c[f_id]).item()
            margins.append(margin)
        cand_margins[c_name] = float(np.mean(margins))
        log(f"Candidate '{c_name}': Mean Valid Margin = {cand_margins[c_name]:+.3f}", log_file)

    best_cand_name = max(cand_margins, key=cand_margins.get)
    best_kind, best_op = candidates[best_cand_name]
    log(f"Selected winning intervention for transfer: '{best_cand_name}' (Margin = {cand_margins[best_cand_name]:+.3f})", log_file)

    # 2. PHASE 2 & 3: EVALUATION ACROSS ALL DOMAINS & CAUSAL NECESSITY CONTROLS
    # Prepare Causal Necessity Perturbations (H4)
    if best_kind == "vector":
        # Scrambled reversed
        op_rev = -best_op
        # Random orthogonal vector
        rnd = torch.randn_like(best_op)
        op_orth = rnd - (rnd @ best_op) * best_op
        op_orth = op_orth / (torch.norm(op_orth) + 1e-8)
    else:
        op_rev = -best_op
        Q, _ = torch.linalg.qr(torch.randn_like(best_op))
        op_orth = (Q[:, :2] @ Q[:, :2].T).to(device)

    conditions = ["base", "selected_transfer", "causal_reversed", "causal_orthogonal"]
    results_by_domain = {}
    all_instances_log = []

    for dom in ["domain0_discovery_social", "domain1_heldout_names", "domain2_biochemical", "domain3_industrial", "domain4_symbolic"]:
        results_by_domain[dom] = {
            "valid": {c: {"correct": 0, "total": 0, "margins": []} for c in conditions},
            "control": {c: {"margins": []} for c in conditions}
        }

    for inst in dataset:
        dom = inst["domain"]
        is_valid = inst["is_valid_transitive"]
        prompt = inst["prompt"]
        t_id = tokenizer.encode(inst["target_token"])[0]
        f_id = tokenizer.encode(inst["foil_token"])[0]

        enc = tokenizer(prompt, return_tensors="pt")
        inp_ids = enc.input_ids.to(device)

        cond_outputs = {}

        # 1. Base Unperturbed
        with torch.no_grad():
            l_base = model(input_ids=inp_ids).logits[0, -1, :]
        cond_outputs["base"] = l_base

        # 2. Selected Transfer Intervention
        def hook_sel(mod, inp, outp):
            h = outp[0].clone() if isinstance(outp, tuple) else outp.clone()
            if best_kind == "vector":
                h[0, -1, :] = h[0, -1, :] + ALPHA * best_op
            else:
                h[0, -1, :] = h[0, -1, :] + ALPHA * (h[0, -1, :] @ best_op)
            return (h,) + outp[1:] if isinstance(outp, tuple) else h

        h_handle = model.gpt_neox.layers[TARGET_BLOCK].register_forward_hook(hook_sel)
        with torch.no_grad():
            l_sel = model(input_ids=inp_ids).logits[0, -1, :]
        h_handle.remove()
        cond_outputs["selected_transfer"] = l_sel

        # 3. Causal Necessity: Reversed
        def hook_rev(mod, inp, outp):
            h = outp[0].clone() if isinstance(outp, tuple) else outp.clone()
            if best_kind == "vector":
                h[0, -1, :] = h[0, -1, :] + ALPHA * op_rev
            else:
                h[0, -1, :] = h[0, -1, :] + ALPHA * (h[0, -1, :] @ op_rev)
            return (h,) + outp[1:] if isinstance(outp, tuple) else h

        h_handle = model.gpt_neox.layers[TARGET_BLOCK].register_forward_hook(hook_rev)
        with torch.no_grad():
            l_rev = model(input_ids=inp_ids).logits[0, -1, :]
        h_handle.remove()
        cond_outputs["causal_reversed"] = l_rev

        # 4. Causal Necessity: Orthogonal
        def hook_orth(mod, inp, outp):
            h = outp[0].clone() if isinstance(outp, tuple) else outp.clone()
            if best_kind == "vector":
                h[0, -1, :] = h[0, -1, :] + ALPHA * op_orth
            else:
                h[0, -1, :] = h[0, -1, :] + ALPHA * (h[0, -1, :] @ op_orth)
            return (h,) + outp[1:] if isinstance(outp, tuple) else h

        h_handle = model.gpt_neox.layers[TARGET_BLOCK].register_forward_hook(hook_orth)
        with torch.no_grad():
            l_orth = model(input_ids=inp_ids).logits[0, -1, :]
        h_handle.remove()
        cond_outputs["causal_orthogonal"] = l_orth

        # Log Metrics
        inst_res = {"id": inst["id"], "domain": dom, "is_valid": is_valid}
        for cond_name, l_out in cond_outputs.items():
            margin = (l_out[t_id] - l_out[f_id]).item()
            is_correct = int(margin > 0) # Target preferred over foil
            inst_res[f"{cond_name}_margin"] = margin
            inst_res[f"{cond_name}_pref"] = is_correct

            if is_valid:
                results_by_domain[dom]["valid"][cond_name]["correct"] += is_correct
                results_by_domain[dom]["valid"][cond_name]["total"] += 1
                results_by_domain[dom]["valid"][cond_name]["margins"].append(margin)
            else:
                results_by_domain[dom]["control"][cond_name]["margins"].append(margin)

        all_instances_log.append(inst_res)

    # 3. HYPOTHESIS TESTING & STATISTICAL AUDIT
    log("\n================ EXP059 TRANSITIVE TRANSFER RESULTS SUMMARY ================", log_file)

    # H1: Causal Intervention on Discovery Domain
    d0_valid = results_by_domain["domain0_discovery_social"]["valid"]
    acc_base_d0 = d0_valid["base"]["correct"] / d0_valid["base"]["total"]
    acc_sel_d0  = d0_valid["selected_transfer"]["correct"] / d0_valid["selected_transfer"]["total"]
    delta_d0    = (acc_sel_d0 - acc_base_d0) * 100.0
    log(f"\n[Domain 0 - Discovery Split] Base: {acc_base_d0*100:.1f}%, Selected: {acc_sel_d0*100:.1f}% (Delta_M = {delta_d0:+.1f} pp)", log_file)

    # H3: Transfer to Disjoint Domains
    heldout_doms = ["domain1_heldout_names", "domain2_biochemical", "domain3_industrial", "domain4_symbolic"]
    heldout_base_corr, heldout_sel_corr, heldout_total = 0, 0, 0
    heldout_rev_corr, heldout_orth_corr = 0, 0

    log("\n--- Breakdown Across Held-Out Disjoint Domains ---", log_file)
    for dom in heldout_doms:
        v = results_by_domain[dom]["valid"]
        n_tot = v["base"]["total"]
        acc_b = v["base"]["correct"] / n_tot
        acc_s = v["selected_transfer"]["correct"] / n_tot
        acc_r = v["causal_reversed"]["correct"] / n_tot
        acc_o = v["causal_orthogonal"]["correct"] / n_tot
        d_m = (acc_s - acc_b) * 100.0

        heldout_base_corr += v["base"]["correct"]
        heldout_sel_corr  += v["selected_transfer"]["correct"]
        heldout_rev_corr  += v["causal_reversed"]["correct"]
        heldout_orth_corr += v["causal_orthogonal"]["correct"]
        heldout_total     += n_tot

        log(f"{dom:<24}: Base={acc_b*100:.1f}%, Transferred={acc_s*100:.1f}% (Delta={d_m:+.1f} pp) | Rev={acc_r*100:.1f}%, Orth={acc_o*100:.1f}%", log_file)

    acc_heldout_base = heldout_base_corr / heldout_total
    acc_heldout_sel  = heldout_sel_corr / heldout_total
    acc_heldout_rev  = heldout_rev_corr / heldout_total
    acc_heldout_orth = heldout_orth_corr / heldout_total
    delta_heldout    = (acc_heldout_sel - acc_heldout_base) * 100.0

    # Paired McNemar on Held-Out Items
    heldout_valid_insts = [x for x in all_instances_log if x["domain"] in heldout_doms and x["is_valid"]]
    b_heldout = sum(1 for x in heldout_valid_insts if x["base_pref"] == 0 and x["selected_transfer_pref"] == 1)
    c_heldout = sum(1 for x in heldout_valid_insts if x["base_pref"] == 1 and x["selected_transfer_pref"] == 0)
    p_transfer = mcnemar_p(b_heldout, c_heldout)

    tau = (delta_heldout / delta_d0) if delta_d0 > 0 else 0.0

    log(f"\n[Aggregate Held-Out Disjoint Domains (N={heldout_total})]", log_file)
    log(f"Base Accuracy:           {acc_heldout_base*100:.1f}% ({heldout_base_corr}/{heldout_total})", log_file)
    log(f"Transferred Intervention:{acc_heldout_sel*100:.1f}% ({heldout_sel_corr}/{heldout_total}) [Delta_M = {delta_heldout:+.1f} pp, Rescues={b_heldout}, Corr={c_heldout}, p={p_transfer:.4f}]", log_file)
    log(f"Causal Reversed Control: {acc_heldout_rev*100:.1f}% ({heldout_rev_corr}/{heldout_total})", log_file)
    log(f"Causal Orthogonal Control:{acc_heldout_orth*100:.1f}% ({heldout_orth_corr}/{heldout_total})", log_file)
    log(f"Headroom Retention Ratio (tau): {tau*100:.1f}%", log_file)

    # H2: Relation Specificity (Valid Transitive vs. Invalid Common Target)
    valid_margin_delta = np.mean([x["selected_transfer_margin"] - x["base_margin"] for x in heldout_valid_insts])
    ctrl_insts = [x for x in all_instances_log if x["domain"] in heldout_doms and not x["is_valid"]]
    ctrl_margin_delta = np.mean([x["selected_transfer_margin"] - x["base_margin"] for x in ctrl_insts])
    specificity_gap = valid_margin_delta - ctrl_margin_delta
    log(f"\n[H2 Relation Specificity] Valid Margin Delta: {valid_margin_delta:+.3f} | Control Margin Delta: {ctrl_margin_delta:+.3f} | Specificity Gap: {specificity_gap:+.3f}", log_file)

    # Evaluate Inviolable Laws: Model hash immutability
    post_hash = get_hash(model)
    assert post_hash == pre_hash, "Backbone altered!"
    log("\nBackbone immutability verified: Delta_theta = 0.", log_file)

    # Preregistered Hypothesis Adjudication
    h1_passed = bool(delta_d0 > 0)
    h2_passed = bool(specificity_gap > 0.05)
    h3_passed = bool(delta_heldout > 0 and p_transfer < 0.05 and tau >= 0.30)
    h4_passed = bool(acc_heldout_sel > max(acc_heldout_rev, acc_heldout_orth))
    h5_passed = bool(acc_heldout_sel > acc_heldout_base)

    log("\n--- Hypothesis Falsification Ledger ---", log_file)
    log(f"H1 (Causal Intervention on Discovery):  {'CONFIRMED' if h1_passed else 'FALSIFIED'} (Delta_d0 = {delta_d0:+.1f} pp)", log_file)
    log(f"H2 (Relation Specificity vs Controls):  {'CONFIRMED' if h2_passed else 'FALSIFIED'} (Gap = {specificity_gap:+.3f})", log_file)
    log(f"H3 (Surface Invariance on Disjoint):    {'CONFIRMED' if h3_passed else 'FALSIFIED'} (Delta_heldout = {delta_heldout:+.1f} pp, tau = {tau*100:.1f}%, p = {p_transfer:.4f})", log_file)
    log(f"H4 (Causal Necessity under Perturb):    {'CONFIRMED' if h4_passed else 'FALSIFIED'} (Transferred {acc_heldout_sel*100:.1f}% vs Rev {acc_heldout_rev*100:.1f}% / Orth {acc_heldout_orth*100:.1f}%)", log_file)
    log(f"H5 (Reusability on Held-Out):           {'CONFIRMED' if h5_passed else 'FALSIFIED'}", log_file)

    if h1_passed and h2_passed and h3_passed and h4_passed:
        verdict = "RELATION_LEVEL_TRANSFER_SUPPORTED"
    elif h1_passed and not h3_passed:
        verdict = "SURFACE_BOUND_ACTIVATION_GEOMETRY"
    elif not h1_passed:
        verdict = "TRANSITIVE_INTERVENTION_INEFFECTIVE"
    else:
        verdict = "NON_SPECIFIC_PERTURBATION"

    log(f"\nFinal Pre-Registered Audit Verdict: >>> {verdict} <<<", log_file)

    final_payload = {
        "metadata": {
            "experiment": "EXP059",
            "title": "Transitive Relational Transfer Across Disjoint Surface Domains",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "model": CANONICAL_MODEL,
            "target_block": TARGET_BLOCK,
            "alpha": ALPHA,
            "selected_operator": best_cand_name,
            "verdict": verdict,
            "hypotheses": {
                "H1_causal_intervention": h1_passed,
                "H2_relation_specificity": h2_passed,
                "H3_surface_invariance": h3_passed,
                "H4_causal_necessity": h4_passed,
                "H5_reusability": h5_passed
            },
            "retention_ratio_tau": float(tau)
        },
        "discovery_domain": {
            "base_acc": float(acc_base_d0),
            "selected_acc": float(acc_sel_d0),
            "delta_pp": float(delta_d0)
        },
        "heldout_aggregate": {
            "base_acc": float(acc_heldout_base),
            "selected_acc": float(acc_heldout_sel),
            "reversed_acc": float(acc_heldout_rev),
            "orthogonal_acc": float(acc_heldout_orth),
            "delta_pp": float(delta_heldout),
            "rescues": int(b_heldout),
            "corruptions": int(c_heldout),
            "p_mcnemar": float(p_transfer)
        },
        "domain_breakdown": {d: {
            "valid_base": results_by_domain[d]["valid"]["base"]["correct"] / results_by_domain[d]["valid"]["base"]["total"],
            "valid_selected": results_by_domain[d]["valid"]["selected_transfer"]["correct"] / results_by_domain[d]["valid"]["selected_transfer"]["total"]
        } for d in results_by_domain}
    }

    out_file = os.path.join(OUT_DIR, "exp059_transfer_results.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(final_payload, f, indent=2)
    log(f"Saved complete audit results to {out_file}", log_file)

if __name__ == "__main__":
    main()
