"""
EXP047: Active Inference Causal Micro-Probing Benchmark.

Pre-Registered Confirmatory Protocol (experiments/protocols/EXP047_ACTIVE_MICRO_PROBE_SPEC.md):
- Architecture: EleutherAI/pythia-160m (12 layers, d_model=768).
- Action Space: A = {R, Empty} (Internal Reorganization vs. Abstain / Direct Forward Pass).
  * Action Empty: Direct unsteered forward pass. C(Empty) = 1.00.
  * Action R: Full internal reorganization (audited Layer 8 operator G* at alpha=0.25). C(R) = 1.05.
- Active Micro-Probe Mechanism:
  * Layer l* = 8.
  * Micro-probe scale: epsilon = 0.05 (rho = 0.20 * alpha = 0.05).
  * Observable causal response metrics:
    - Delta M_12: differential top-2 logit margin expansion
    - d_disp: trajectory strain ||h_L(eps) - h_L(0)|| / ||h_L(0)||
    - kappa: local controllability ratio Delta M_12 / (d_disp + 1e-4)
    - Delta H_vocab: predictive entropy shift H(z_eps) - H(z_0)
- Commit / Rollback Policy:
  * Commit (R): If kappa > tau_commit and Delta H_vocab <= 0 -> Scale to full alpha=0.25 (C = 1.67).
  * Rollback (Empty): Otherwise -> Revert to unperturbed baseline state (C = 1.33).
- Dataset Splits:
  * D_calib: N=30 (15 BENCH-002 Seed 123 + 15 BENCH-004 Seed 250) -> Lock tau_commit.
  * D_test:  N=100 (50 BENCH-002 Seed 84 + 50 BENCH-004 Seed 350) -> Held-Out Confirmatory Benchmark.
- Evaluated Policies:
  1. pi_always_empty
  2. pi_always_R
  3. pi_passive_diag (EXP046 static diagnostic)
  4. pi_active_probe (Commit / Rollback based on micro-probe kappa)
  5. pi_oracle (Instance-optimal counterfactual upper bound)

Invariance Verification: Pre/post parameter SHA-256 hash verified (Delta theta = 0).
Output Ledger: experiments/runs/EXP047_active_probing/exp047_active_probing_results.json
"""

import os
import sys
import time
import json
import math
import hashlib
import numpy as np
import torch
import torch.nn.functional as F
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from transformers import AutoModelForCausalLM, AutoTokenizer

os.environ["TRANSFORMERS_NO_TF"] = "1"
os.environ["USE_TF"] = "0"
sys.path.append(r"c:\Users\Anilkumar\OneDrive\Desktop\SCPM")
from experiments.benchmarks.bench_002_nl import generate_bench_002_nl
from experiments.benchmarks.bench_004_transfer import generate_bench_004_transfer

def log(msg):
    print(msg, flush=True)

def get_param_hash(model):
    h = hashlib.sha256()
    for p in model.parameters():
        h.update(p.detach().cpu().numpy().tobytes())
    return h.hexdigest()

def extract_subspace(X, rank=2):
    X_cent = X - torch.mean(X, dim=0, keepdim=True)
    if X_cent.shape[0] < rank:
        rank = max(1, X_cent.shape[0])
    _, _, Vh = torch.linalg.svd(X_cent, full_matrices=False)
    return Vh[:rank, :].T

def mcnemar_exact(b, c):
    n = b + c
    if n == 0:
        return 1.0
    p_val = 0.0
    for k in range(b, n + 1):
        p_val += math.comb(n, k) * (0.5 ** n)
    return p_val

def bootstrap_ci(diffs, n_boot=2000, ci=0.95):
    rng = np.random.default_rng(42)
    means = [np.mean(rng.choice(diffs, size=len(diffs), replace=True)) for _ in range(n_boot)]
    alpha = (1 - ci) / 2
    return float(np.percentile(means, 100 * alpha)), float(np.percentile(means, 100 * (1 - alpha)))

# ----------------------------------------------------------------------------
# Observable Extraction & Multi-Pass Evaluation Functions
# ----------------------------------------------------------------------------
def evaluate_instance_probing(model, tokenizer, prompt, target_token, target_block=7, l4_block=3, l6_block=5, epsilon=0.05, alpha=0.25):
    enc = tokenizer(prompt, return_tensors="pt")
    input_ids = enc.input_ids
    
    t_str = target_token.strip()
    t_enc = tokenizer.encode(" " + t_str)
    t_id = t_enc[0] if t_enc else tokenizer.encode(t_str)[0]

    # ------------------------------------------------------------------------
    # Pass 1: Baseline unperturbed forward pass
    # ------------------------------------------------------------------------
    captured_base = {}
    def cap_4(mod, inp, outp): captured_base["h4"] = (outp[0] if isinstance(outp, tuple) else outp).detach().squeeze(0)
    def cap_6(mod, inp, outp): captured_base["h6"] = (outp[0] if isinstance(outp, tuple) else outp).detach().squeeze(0)
    def cap_8(mod, inp, outp): captured_base["h8"] = (outp[0] if isinstance(outp, tuple) else outp).detach().squeeze(0)
    def cap_12(mod, inp, outp): captured_base["h12"] = (outp[0] if isinstance(outp, tuple) else outp).detach().squeeze(0)

    h4_h = model.gpt_neox.layers[l4_block].register_forward_hook(cap_4)
    h6_h = model.gpt_neox.layers[l6_block].register_forward_hook(cap_6)
    h8_h = model.gpt_neox.layers[target_block].register_forward_hook(cap_8)
    h12_h = model.gpt_neox.layers[11].register_forward_hook(cap_12)

    with torch.no_grad():
        out_base = model(input_ids=input_ids, output_attentions=True)
        logits_base = out_base.logits[0, -1, :]
        attn_8 = out_base.attentions[target_block][0]
    h4_h.remove(); h6_h.remove(); h8_h.remove(); h12_h.remove()

    pred_base = torch.argmax(logits_base).item()
    corr_base = int(pred_base == t_id)

    # Compute baseline observables
    top2_base, _ = torch.topk(logits_base, k=2)
    m12_base = float((top2_base[0] - top2_base[1]).item())
    p_base = F.softmax(logits_base, dim=-1)
    h_vocab_base = float((-torch.sum(p_base * torch.log(p_base + 1e-12))).item())

    # Passive observables (for comparison with EXP046)
    last_attn = attn_8[:, -1, :]
    head_entropies = -torch.sum(last_attn * torch.log(last_attn + 1e-12), dim=-1)
    sigma_h_attn = float(torch.std(head_entropies).item())

    h4_all = captured_base["h4"]
    if h4_all.shape[0] > 1:
        _, S4, _ = torch.linalg.svd(h4_all - torch.mean(h4_all, dim=0, keepdim=True), full_matrices=False)
        pr_min = float((torch.sum(S4**2)**2 / torch.sum(S4**4)).item())
    else:
        pr_min = 1.0
    cos_drift = float(F.cosine_similarity(captured_base["h4"][-1, :].unsqueeze(0), captured_base["h8"][-1, :].unsqueeze(0)).item())

    passive_features = [m12_base, h_vocab_base, sigma_h_attn, pr_min, cos_drift]

    # Construct Operator G* (ortho velocity flow projector P3)
    diff_8_6 = captured_base["h8"] - captured_base["h6"]
    V4 = extract_subspace(captured_base["h4"], rank=2)
    ortho = diff_8_6 - (diff_8_6 @ (V4 @ V4.T))
    V3 = extract_subspace(ortho, rank=2)
    P3 = V3 @ V3.T

    # ------------------------------------------------------------------------
    # Pass 2: Reversible Micro-Probe Forward Pass (epsilon = 0.05)
    # ------------------------------------------------------------------------
    captured_probe = {}
    def cap_probe_12(mod, inp, outp): captured_probe["h12"] = (outp[0] if isinstance(outp, tuple) else outp).detach().squeeze(0)

    def hook_probe(mod, inp, outp):
        h = outp[0].clone() if isinstance(outp, tuple) else outp.clone()
        h[0] = h[0] - epsilon * (h[0] @ P3)
        return (h,) + outp[1:] if isinstance(outp, tuple) else h

    hp_8 = model.gpt_neox.layers[target_block].register_forward_hook(hook_probe)
    hp_12 = model.gpt_neox.layers[11].register_forward_hook(cap_probe_12)
    with torch.no_grad():
        out_probe = model(input_ids=input_ids)
        logits_probe = out_probe.logits[0, -1, :]
    hp_8.remove(); hp_12.remove()

    top2_probe, _ = torch.topk(logits_probe, k=2)
    m12_probe = float((top2_probe[0] - top2_probe[1]).item())
    delta_m12 = m12_probe - m12_base

    h12_base_vec = captured_base["h12"][-1, :]
    h12_probe_vec = captured_probe["h12"][-1, :]
    d_disp = float((torch.norm(h12_probe_vec - h12_base_vec) / (torch.norm(h12_base_vec) + 1e-6)).item())
    kappa = delta_m12 / (d_disp + 1e-4)

    p_probe = F.softmax(logits_probe, dim=-1)
    h_vocab_probe = float((-torch.sum(p_probe * torch.log(p_probe + 1e-12))).item())
    delta_h_vocab = h_vocab_probe - h_vocab_base

    probe_observables = {
        "m12_base": m12_base,
        "m12_probe": m12_probe,
        "delta_m12": delta_m12,
        "d_disp": d_disp,
        "kappa": kappa,
        "delta_h_vocab": delta_h_vocab
    }

    # ------------------------------------------------------------------------
    # Pass 3: Full Intervention Pass (alpha = 0.25) for Action R evaluation
    # ------------------------------------------------------------------------
    def hook_r(mod, inp, outp):
        h = outp[0].clone() if isinstance(outp, tuple) else outp.clone()
        h[0] = h[0] - alpha * (h[0] @ P3)
        return (h,) + outp[1:] if isinstance(outp, tuple) else h

    hr_8 = model.gpt_neox.layers[target_block].register_forward_hook(hook_r)
    with torch.no_grad():
        out_r = model(input_ids=input_ids)
        logits_r = out_r.logits[0, -1, :]
    hr_8.remove()

    pred_r = torch.argmax(logits_r).item()
    corr_r = int(pred_r == t_id)
    is_corrupt_r = int(corr_base == 1 and corr_r == 0)
    is_rescued_r = int(corr_base == 0 and corr_r == 1)

    return {
        "t_id": t_id,
        "corr_base": corr_base,
        "corr_r": corr_r,
        "is_corrupt_r": is_corrupt_r,
        "is_rescued_r": is_rescued_r,
        "probe_observables": probe_observables,
        "passive_features": passive_features
    }

# ----------------------------------------------------------------------------
# Main Protocol Execution
# ----------------------------------------------------------------------------
def run_exp047():
    log("==========================================================================")
    log("EXP047: Active Inference Causal Micro-Probing Benchmark")
    log("==========================================================================")

    model_name = "EleutherAI/pythia-160m"
    target_block = 7 # Layer 8
    alpha = 0.25
    epsilon = 0.05

    log(f"Loading model: {model_name}...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    model.eval()

    pre_hash = get_param_hash(model)
    log(f"Pre-experiment parameter SHA-256: {pre_hash}")

    # Dataset Construction
    log("\nAssembling Calibration and Mixed Confirmatory Benchmarks...")
    calib_b2 = generate_bench_002_nl(n_instances=15, seed=123)
    calib_b4 = generate_bench_004_transfer(n_instances=15, seed=250)
    d_calib = calib_b2 + calib_b4
    log(f"Split 1: D_calib (N={len(d_calib)}, 15 BENCH-002 + 15 BENCH-004)")

    test_b2 = generate_bench_002_nl(n_instances=50, seed=84)
    test_b4 = generate_bench_004_transfer(n_instances=50, seed=350)
    d_test = test_b2 + test_b4
    log(f"Split 2: D_test  (N={len(d_test)}, 50 BENCH-002 + 50 BENCH-004)")

    # ------------------------------------------------------------------------
    # Step 1: Calibration & Gating Threshold Locking on D_calib (N=30)
    # ------------------------------------------------------------------------
    log("\n==========================================================================")
    log("Step 1: Running Active Micro-Probing on D_calib (N=30) to Lock tau_commit")
    log("==========================================================================")

    calib_records = []
    X_calib_passive = []
    y_calib_viable = []

    for idx, inst in enumerate(d_calib):
        prompt = inst["base"]
        target = inst["target"].strip() if "target" in inst else inst["target_token"].strip()
        res = evaluate_instance_probing(model, tokenizer, prompt, target, target_block=target_block, epsilon=epsilon, alpha=alpha)
        calib_records.append(res)
        X_calib_passive.append(res["passive_features"])
        # Viable if R rescues failure or preserves correct without corruption
        u_base = res["corr_base"] - 0.05 * 1.00
        u_r = res["corr_r"] - 0.05 * 1.05 - 1.00 * res["is_corrupt_r"]
        viable = int(u_r > u_base)
        y_calib_viable.append(viable)

    # Fit EXP046 passive logistic classifier on calibration split for reference
    clf_passive = LogisticRegression()
    clf_passive.fit(np.array(X_calib_passive), np.array(y_calib_viable))

    # Grid search for optimal tau_commit on calibration split
    kappas = [r["probe_observables"]["kappa"] for r in calib_records]
    candidate_taus = np.linspace(np.percentile(kappas, 10), np.percentile(kappas, 90), 30)

    best_tau = 0.0
    best_u_calib = -999.0

    for tau in candidate_taus:
        u_total = 0.0
        for r in calib_records:
            k = r["probe_observables"]["kappa"]
            dH = r["probe_observables"]["delta_h_vocab"]
            if k > tau and dH <= 0.0: # Commit
                c_cost = 1.67
                u = r["corr_r"] - 0.05 * c_cost - 1.00 * r["is_corrupt_r"]
            else: # Rollback
                c_cost = 1.33
                u = r["corr_base"] - 0.05 * c_cost
            u_total += u
        mean_u = u_total / len(calib_records)
        if mean_u > best_u_calib:
            best_u_calib = mean_u
            best_tau = float(tau)

    log(f">>> CALIBRATION COMPLETED <<<")
    log(f"Locked tau_commit: {best_tau:.4f} (Optimal Calibration Mean Utility: {best_u_calib:+.4f})")

    calib_manifest = {
        "locked_tau_commit": best_tau,
        "calib_best_utility": best_u_calib,
        "n_calib": len(d_calib)
    }
    manifest_hash = hashlib.sha256(json.dumps(calib_manifest, sort_keys=True).encode("utf-8")).hexdigest()
    log(f"Calibration Manifest SHA-256: {manifest_hash}")

    # ------------------------------------------------------------------------
    # Step 2: Confirmatory Evaluation on Held-Out D_test (N=100)
    # ------------------------------------------------------------------------
    log("\n==========================================================================")
    log("Step 2: Held-Out Confirmatory Benchmark on D_test (N=100, Seed 84/350)")
    log("==========================================================================")

    test_records = []
    y_test_viable = []
    kappas_test = []
    delta_m12_test = []
    passive_p_viable = []
    passive_delta_z = []

    # Policy tallies
    correct_empty = 0
    correct_r = 0
    correct_passive = 0
    correct_probe = 0
    correct_oracle = 0

    corrupt_empty = 0
    corrupt_r = 0
    corrupt_passive = 0
    corrupt_probe = 0
    corrupt_oracle = 0

    u_empty_list = []
    u_r_list = []
    u_passive_list = []
    u_probe_list = []
    u_oracle_list = []

    probe_commits = 0
    probe_rollbacks = 0

    for idx, inst in enumerate(d_test):
        prompt = inst["base"]
        target = inst["target"].strip() if "target" in inst else inst["target_token"].strip()
        res = evaluate_instance_probing(model, tokenizer, prompt, target, target_block=target_block, epsilon=epsilon, alpha=alpha)
        test_records.append(res)

        corr_base = res["corr_base"]
        corr_r = res["corr_r"]
        is_corrupt_r = res["is_corrupt_r"]

        # Utility of always-empty
        u_empty = corr_base - 0.05 * 1.00
        # Utility of always-R
        u_r = corr_r - 0.05 * 1.05 - 1.00 * is_corrupt_r

        viable = int(u_r > u_empty)
        y_test_viable.append(viable)

        k = res["probe_observables"]["kappa"]
        dm12 = res["probe_observables"]["delta_m12"]
        dH = res["probe_observables"]["delta_h_vocab"]
        kappas_test.append(k)
        delta_m12_test.append(dm12)

        # Passive prediction
        x_pass = np.array([res["passive_features"]])
        p_pass = float(clf_passive.predict_proba(x_pass)[0, 1])
        passive_p_viable.append(p_pass)
        passive_delta_z.append(res["passive_features"][0])

        # 1. pi_always_empty
        correct_empty += corr_base
        u_empty_list.append(u_empty)

        # 2. pi_always_R
        correct_r += corr_r
        corrupt_r += is_corrupt_r
        u_r_list.append(u_r)

        # 3. pi_passive_diag: commit if p_pass > 0.5
        if p_pass > 0.5:
            correct_passive += corr_r
            corrupt_passive += is_corrupt_r
            u_passive = corr_r - 0.05 * 1.05 - 1.00 * is_corrupt_r
        else:
            correct_passive += corr_base
            u_passive = corr_base - 0.05 * 1.00
        u_passive_list.append(u_passive)

        # 4. pi_active_probe: Commit if k > best_tau and dH <= 0
        if k > best_tau and dH <= 0.0:
            probe_commits += 1
            c_cost = 1.67
            correct_probe += corr_r
            corrupt_probe += is_corrupt_r
            u_pr = corr_r - 0.05 * c_cost - 1.00 * is_corrupt_r
        else:
            probe_rollbacks += 1
            c_cost = 1.33
            correct_probe += corr_base
            u_pr = corr_base - 0.05 * c_cost
        u_probe_list.append(u_pr)

        # 5. pi_oracle: max(u_empty, u_r)
        if u_r > u_empty:
            correct_oracle += corr_r
            corrupt_oracle += is_corrupt_r
            u_oracle = u_r
        else:
            correct_oracle += corr_base
            u_oracle = u_empty
        u_oracle_list.append(u_oracle)

    N = len(d_test)
    acc_empty = correct_empty / N
    acc_r = correct_r / N
    acc_passive = correct_passive / N
    acc_probe = correct_probe / N
    acc_oracle = correct_oracle / N

    mean_u_empty = float(np.mean(u_empty_list))
    mean_u_r = float(np.mean(u_r_list))
    mean_u_passive = float(np.mean(u_passive_list))
    mean_u_probe = float(np.mean(u_probe_list))
    mean_u_oracle = float(np.mean(u_oracle_list))

    # ROC-AUC analysis
    y_test_viable = np.array(y_test_viable)
    n_viable = int(np.sum(y_test_viable))
    log(f"\nTest Ground Truth: {n_viable}/{N} instances have U_R > U_empty.")

    if n_viable > 0 and n_viable < N:
        auc_kappa = float(roc_auc_score(y_test_viable, kappas_test))
        auc_delta_m = float(roc_auc_score(y_test_viable, delta_m12_test))
        auc_passive_p = float(roc_auc_score(y_test_viable, passive_p_viable))
        auc_passive_dz = float(roc_auc_score(y_test_viable, passive_delta_z))
    else:
        auc_kappa = 0.50
        auc_delta_m = 0.50
        auc_passive_p = 0.50
        auc_passive_dz = 0.50

    # McNemar test between pi_probe and pi_empty
    b_pr = sum(1 for r, u in zip(test_records, u_probe_list) if r["corr_base"] == 0 and r["corr_r"] == 1 and r["probe_observables"]["kappa"] > best_tau and r["probe_observables"]["delta_h_vocab"] <= 0.0)
    c_pr = sum(1 for r, u in zip(test_records, u_probe_list) if r["corr_base"] == 1 and r["corr_r"] == 0 and r["probe_observables"]["kappa"] > best_tau and r["probe_observables"]["delta_h_vocab"] <= 0.0)
    p_mcnemar = mcnemar_exact(b_pr, c_pr)

    diff_u = np.array(u_probe_list) - np.array(u_empty_list)
    ci_u_low, ci_u_high = bootstrap_ci(diff_u)

    log("\n==========================================================================")
    log("CONFIRMATORY POLICY SCORECARD (N=100)")
    log("==========================================================================")
    log(f"1. pi_always_empty:      Accuracy = {acc_empty*100:.2f}%, Corruptions = {corrupt_empty}, Mean Utility = {mean_u_empty:+.4f}")
    log(f"2. pi_always_R:          Accuracy = {acc_r*100:.2f}%, Corruptions = {corrupt_r}, Mean Utility = {mean_u_r:+.4f}")
    log(f"3. pi_passive_diag:      Accuracy = {acc_passive*100:.2f}%, Corruptions = {corrupt_passive}, Mean Utility = {mean_u_passive:+.4f}")
    log(f"4. pi_active_probe:      Accuracy = {acc_probe*100:.2f}%, Corruptions = {corrupt_probe}, Mean Utility = {mean_u_probe:+.4f}")
    log(f"   [Probe Details]       Commits: {probe_commits}/{N} ({probe_commits/N*100:.1f}%), Rollbacks: {probe_rollbacks}/{N} ({probe_rollbacks/N*100:.1f}%)")
    log(f"5. pi_oracle:            Accuracy = {acc_oracle*100:.2f}%, Corruptions = {corrupt_oracle}, Mean Utility = {mean_u_oracle:+.4f}")

    log("\n==========================================================================")
    log("DISCRIMINATIVE AUC COMPARISON (Predicting U_R > U_empty)")
    log("==========================================================================")
    log(f"Active Micro-Probe Local Controllability (kappa): AUC = {auc_kappa:.4f}")
    log(f"Active Micro-Probe Margin Expansion (Delta M_12): AUC = {auc_delta_m:.4f}")
    log(f"Passive Pre-Intervention Logistic Score (EXP046): AUC = {auc_passive_p:.4f}")
    log(f"Passive Pre-Intervention Logit Gap (Delta z_top2): AUC = {auc_passive_dz:.4f}")

    log("\n==========================================================================")
    log("STATISTICAL INFERENCE (pi_probe vs. pi_empty)")
    log("==========================================================================")
    log(f"Rescues (b): {b_pr}, Corruptions (c): {c_pr}, Exact McNemar p: {p_mcnemar:.4f}")
    log(f"Net Utility Difference: {mean_u_probe - mean_u_empty:+.4f} (95% CI: [{ci_u_low:+.4f}, {ci_u_high:+.4f}])")

    # Post-experiment parameter verification
    post_hash = get_param_hash(model)
    log(f"\nPost-experiment parameter SHA-256: {post_hash}")
    assert pre_hash == post_hash, "CRITICAL ERROR: Backbone weights modified during inference!"
    log("[VERIFIED] Parameter invariance confirmed (Delta theta == 0).")

    # Outcome resolution
    if auc_kappa >= 0.70 and mean_u_probe > mean_u_empty and corrupt_probe == 0 and p_mcnemar <= 0.05:
        outcome = "Outcome 1: Active Inference Confirmed"
    elif auc_kappa >= 0.65 and mean_u_probe > mean_u_empty and corrupt_probe == 0:
        outcome = "Outcome 2: Safe Selective Control (Partial Efficacy)"
    elif probe_rollbacks >= 95 and corrupt_probe == 0:
        outcome = "Outcome 3: Conservative Inertia (Under-Triggering)"
    else:
        outcome = "Outcome 4: Active Probing Refuted"

    log(f"\n==========================================================================")
    log(f"TRI-STATE / FALSIFICATION RESOLUTION: {outcome}")
    log(f"==========================================================================")

    # Save ledger
    run_dir = r"c:\Users\Anilkumar\OneDrive\Desktop\SCPM\experiments\runs\EXP047_active_probing"
    os.makedirs(run_dir, exist_ok=True)
    out_path = os.path.join(run_dir, "exp047_active_probing_results.json")

    results_data = {
        "experiment_id": "EXP047",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "model": model_name,
        "pre_hash": pre_hash,
        "post_hash": post_hash,
        "hash_invariant": bool(pre_hash == post_hash),
        "calibration_manifest": calib_manifest,
        "manifest_hash": manifest_hash,
        "sample_size_test": N,
        "n_viable_test": n_viable,
        "scorecard": {
            "pi_always_empty": {"accuracy": acc_empty, "corruptions": corrupt_empty, "mean_utility": mean_u_empty},
            "pi_always_r": {"accuracy": acc_r, "corruptions": corrupt_r, "mean_utility": mean_u_r},
            "pi_passive_diag": {"accuracy": acc_passive, "corruptions": corrupt_passive, "mean_utility": mean_u_passive},
            "pi_active_probe": {
                "accuracy": acc_probe,
                "corruptions": corrupt_probe,
                "mean_utility": mean_u_probe,
                "commits": probe_commits,
                "rollbacks": probe_rollbacks,
                "commit_rate": probe_commits / N
            },
            "pi_oracle": {"accuracy": acc_oracle, "corruptions": corrupt_oracle, "mean_utility": mean_u_oracle}
        },
        "auc_metrics": {
            "auc_kappa": auc_kappa,
            "auc_delta_m12": auc_delta_m,
            "auc_passive_score": auc_passive_p,
            "auc_passive_delta_z": auc_passive_dz
        },
        "statistical_tests": {
            "mcnemar_b": b_pr,
            "mcnemar_c": c_pr,
            "mcnemar_p": p_mcnemar,
            "delta_utility": mean_u_probe - mean_u_empty,
            "ci_95": [ci_u_low, ci_u_high]
        },
        "tri_state_outcome": outcome
    }

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results_data, f, indent=2)
    log(f"Results sealed in: {out_path}")

if __name__ == "__main__":
    run_exp047()
