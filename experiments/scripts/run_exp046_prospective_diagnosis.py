"""
EXP046: Prospective Failure Mode Diagnosis & Adaptive Computation Allocation Benchmark.

Pre-Registered Confirmatory Protocol (experiments/protocols/EXP046_PROSPECTIVE_DIAGNOSIS_SPEC.md):
- Architecture: EleutherAI/pythia-160m (12 layers, d_model=768).
- Discrete Action Space:
    * Action R: Internal Reorganization (audited safe Layer 8 toolbox G_3 ortho). Cost C(R) = 1.05.
    * Action S: External BM25 Retrieval over K=500 factual corpus. Cost C(S) = 2.00.
    * Action Empty: Unsteered Baseline Forward Pass. Cost C(Empty) = 1.00.
- Numerically Locked Utility Function:
    U(a | x) = Correct(a | x) - 0.05 * C(a) - 1.00 * 1[Corrupted(a | x)]
- Dataset Splits:
    * D_calib: N=30 (15 BENCH-002 Seed 123 + 15 BENCH-004 Seed 250) -> Fit & Freeze Diagnostic D_phi.
    * D_test:  N=100 (50 BENCH-002 Seed 84 + 50 BENCH-004 Seed 350) -> Held-Out Confirmatory Benchmark.
- Feature Ablation Hierarchy:
    * D_full:   [Delta z_top2, H_vocab, sigma_H(A_8), PR_min, d_drift]
    * D_output: [Delta z_top2, H_vocab]
    * D_geom:   [PR_min, d_drift]
    * D_attn:   [sigma_H(A_8)]

Evaluated Policies:
  1. pi_always_empty
  2. pi_always_R
  3. pi_always_S
  4. pi_diagnostic (Full, Output, Geom, Attn)
  5. pi_oracle (Retrospective instance-optimal allocation)

Invariance Verification: Pre/post parameter SHA-256 hash verified (Delta theta = 0).
Output Ledger: experiments/runs/EXP046_prospective_diagnosis/exp046_prospective_diagnosis_results.json
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

# ----------------------------------------------------------------------------
# BM25 Lexical Retriever & Corpus Construction
# ----------------------------------------------------------------------------
class SimpleBM25:
    def __init__(self, corpus):
        self.corpus = corpus
        self.doc_len = [len(doc.lower().split()) for doc in corpus]
        self.avg_doc_len = sum(self.doc_len) / len(self.doc_len) if self.doc_len else 1.0
        self.df = {}
        for doc in corpus:
            words = set(doc.lower().split())
            for w in words:
                self.df[w] = self.df.get(w, 0) + 1
        self.N = len(corpus)

    def retrieve(self, query, top_k=1):
        q_words = query.lower().split()
        scores = []
        k1 = 1.5
        b = 0.75
        for i, doc in enumerate(self.corpus):
            doc_words = doc.lower().split()
            score = 0.0
            for w in q_words:
                if w in self.df:
                    idf = math.log((self.N - self.df[w] + 0.5) / (self.df[w] + 0.5) + 1.0)
                    tf = doc_words.count(w)
                    denom = tf + k1 * (1.0 - b + b * (self.doc_len[i] / self.avg_doc_len))
                    score += idf * (tf * (k1 + 1.0)) / (denom + 1e-12)
            scores.append((score, doc))
        scores.sort(key=lambda x: x[0], reverse=True)
        return [doc for _, doc in scores[:top_k]]

def build_knowledge_corpus(all_instances):
    # Construct K=500 factual corpus
    corpus = []
    # 1. Clean factual assertions from premises
    for inst in all_instances:
        if "target_evidence_text" in inst:
            corpus.append(f"Fact: {inst['target_evidence_text']}.")
        elif "premise" in inst:
            corpus.append(f"Fact: {inst['premise']}")
    # 2. Add distractor facts to test retrieval robustness
    for inst in all_instances:
        if "distractor_evidence_text" in inst:
            corpus.append(f"Notice: {inst['distractor_evidence_text']}.")
    # 3. Add encyclopedic filler trivia
    filler = [
        "The Eiffel Tower is located in Paris, France.",
        "Mitochondria are the powerhouses of biological cells.",
        "Jupiter is the largest planet in the Solar System.",
        "Photosynthesis converts sunlight into chemical energy.",
        "Shakespeare wrote Hamlet in the early seventeenth century.",
        "The speed of light in vacuum is approximately 299,792 kilometers per second.",
        "Water boils at 100 degrees Celsius under standard atmospheric pressure.",
        "The Pacific Ocean is the deepest and largest of Earth's oceanic divisions."
    ]
    while len(corpus) < 500:
        corpus.extend(filler)
    return corpus[:500]

# ----------------------------------------------------------------------------
# Pre-Intervention Label-Free Observables Extraction
# ----------------------------------------------------------------------------
def extract_label_free_observables(prompt, model, tokenizer, target_block=7, l4_block=3, l6_block=5):
    enc = tokenizer(prompt, return_tensors="pt")
    input_ids = enc.input_ids

    captured = {}
    def cap_4(mod, inp, outp): captured["h4"] = (outp[0] if isinstance(outp, tuple) else outp).detach().squeeze(0)
    def cap_6(mod, inp, outp): captured["h6"] = (outp[0] if isinstance(outp, tuple) else outp).detach().squeeze(0)
    def cap_8(mod, inp, outp): captured["h8"] = (outp[0] if isinstance(outp, tuple) else outp).detach().squeeze(0)

    h4 = model.gpt_neox.layers[l4_block].register_forward_hook(cap_4)
    h6 = model.gpt_neox.layers[l6_block].register_forward_hook(cap_6)
    h8 = model.gpt_neox.layers[target_block].register_forward_hook(cap_8)

    with torch.no_grad():
        out = model(input_ids=input_ids, output_attentions=True)
        logits = out.logits[0, -1, :] # [vocab_size]
        attn_8 = out.attentions[target_block][0] # [num_heads, seq_len, seq_len]

    h4.remove(); h6.remove(); h8.remove()

    h_4 = captured["h4"][-1, :]
    h_8 = captured["h8"][-1, :]

    # 1. Output-only features
    top_logits, _ = torch.topk(logits, k=2)
    delta_z_top2 = float((top_logits[0] - top_logits[1]).item())
    probs = F.softmax(logits, dim=-1)
    h_vocab = float((-torch.sum(probs * torch.log(probs + 1e-12))).item())

    # 2. Attention features
    last_attn = attn_8[:, -1, :] # [num_heads, seq_len]
    head_entropies = -torch.sum(last_attn * torch.log(last_attn + 1e-12), dim=-1) # [num_heads]
    sigma_h_attn = float(torch.std(head_entropies).item())

    # 3. Geometric features
    # Participation ratio of Layer 4 representations across tokens
    h4_all = captured["h4"]
    if h4_all.shape[0] > 1:
        _, S4, _ = torch.linalg.svd(h4_all - torch.mean(h4_all, dim=0, keepdim=True), full_matrices=False)
        pr_min = float((torch.sum(S4**2)**2 / torch.sum(S4**4)).item())
    else:
        pr_min = 1.0

    # Directional drift between h4 and h8
    cos_drift = float(F.cosine_similarity(h_4.unsqueeze(0), h_8.unsqueeze(0)).item())

    features = {
        "delta_z_top2": delta_z_top2,
        "h_vocab": h_vocab,
        "sigma_h_attn": sigma_h_attn,
        "pr_min": pr_min,
        "cos_drift": cos_drift
    }
    return features, input_ids

# ----------------------------------------------------------------------------
# Actions: Reorganize (R) and Retrieve (S)
# ----------------------------------------------------------------------------
def execute_reorganization(model, input_ids, target_block=7, l4_block=3, l6_block=5, alpha=0.25):
    # Audited safe G3 (ortho velocity flow) operator
    captured = {}
    def cap_4(mod, inp, outp): captured["h4"] = (outp[0] if isinstance(outp, tuple) else outp).detach().squeeze(0)
    def cap_6(mod, inp, outp): captured["h6"] = (outp[0] if isinstance(outp, tuple) else outp).detach().squeeze(0)
    def cap_8(mod, inp, outp): captured["h8"] = (outp[0] if isinstance(outp, tuple) else outp).detach().squeeze(0)

    h4 = model.gpt_neox.layers[l4_block].register_forward_hook(cap_4)
    h6 = model.gpt_neox.layers[l6_block].register_forward_hook(cap_6)
    h8 = model.gpt_neox.layers[target_block].register_forward_hook(cap_8)
    with torch.no_grad():
        model(input_ids=input_ids)
    h4.remove(); h6.remove(); h8.remove()

    diff_8_6 = captured["h8"] - captured["h6"]
    V4 = extract_subspace(captured["h4"], rank=2)
    ortho = diff_8_6 - (diff_8_6 @ (V4 @ V4.T))
    V3 = extract_subspace(ortho, rank=2)
    P3 = V3 @ V3.T

    def hook_r(mod, inp, outp):
        h = outp[0].clone() if isinstance(outp, tuple) else outp.clone()
        h[0] = h[0] - alpha * (h[0] @ P3)
        return (h,) + outp[1:] if isinstance(outp, tuple) else h

    hndl = model.gpt_neox.layers[target_block].register_forward_hook(hook_r)
    with torch.no_grad():
        out_r = model(input_ids=input_ids)
        pred_r = torch.argmax(out_r.logits[0, -1, :]).item()
    hndl.remove()
    return pred_r

def execute_retrieval(model, tokenizer, prompt, retriever):
    # Retrieve top-1 relevant passage
    retrieved_doc = retriever.retrieve(prompt, top_k=1)[0]
    augmented_prompt = f"[Reference Context: {retrieved_doc}]\n{prompt}"
    enc = tokenizer(augmented_prompt, return_tensors="pt")
    with torch.no_grad():
        out_s = model(input_ids=enc.input_ids)
        pred_s = torch.argmax(out_s.logits[0, -1, :]).item()
    return pred_s

# ----------------------------------------------------------------------------
# Main Protocol Execution
# ----------------------------------------------------------------------------
def run_exp046():
    log("==========================================================================")
    log("EXP046: Prospective Failure Mode Diagnosis & Adaptive Computation Benchmark")
    log("==========================================================================")

    model_name = "EleutherAI/pythia-160m"
    target_block = 7

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

    # Construct BM25 Corpus
    log("\nBuilding K=500 BM25 Knowledge Corpus...")
    corpus = build_knowledge_corpus(d_calib + d_test)
    retriever = SimpleBM25(corpus)
    log(f"Corpus indexed with {len(corpus)} reference passages.")

    # ------------------------------------------------------------------------
    # Step 1: Fit & Freeze Diagnostic on D_calib (N=30)
    # ------------------------------------------------------------------------
    log("\n==========================================================================")
    log("Step 1: Diagnostic Feature Extraction & Calibration Fitting on D_calib (N=30)")
    log("==========================================================================")

    X_calib = []
    y_calib_R_viable = []

    for inst in d_calib:
        prompt = inst["base"]
        target = inst["target"].strip() if "target" in inst else inst["target_token"].strip()
        t_id = tokenizer.encode(" " + target)[0] if tokenizer.encode(" " + target) else tokenizer.encode(target)[0]

        feat, input_ids = extract_label_free_observables(prompt, model, tokenizer, target_block=target_block)
        X_calib.append([
            feat["delta_z_top2"], feat["h_vocab"], feat["sigma_h_attn"],
            feat["pr_min"], feat["cos_drift"]
        ])

        with torch.no_grad():
            out_base = model(input_ids=input_ids)
            base_pred = torch.argmax(out_base.logits[0, -1, :]).item()

        pred_r = execute_reorganization(model, input_ids, target_block=target_block)

        # R is viable if baseline is wrong and R rescues it, or baseline correct and R doesn't corrupt
        is_base_correct = (base_pred == t_id)
        is_r_correct = (pred_r == t_id)
        r_viable = (not is_base_correct and is_r_correct)
        y_calib_R_viable.append(1 if r_viable else 0)

    X_calib = np.array(X_calib)
    y_calib = np.array(y_calib_R_viable)

    # Fit Full Diagnostic Classifier
    clf_full = LogisticRegression()
    clf_full.fit(X_calib, y_calib)

    # Fit Ablation Models
    clf_output = LogisticRegression().fit(X_calib[:, :2], y_calib)
    clf_geom   = LogisticRegression().fit(X_calib[:, 3:], y_calib)
    clf_attn   = LogisticRegression().fit(X_calib[:, 2:3], y_calib)

    # Compute & Log Calibration Manifest
    calib_manifest = {
        "coef_full": clf_full.coef_.tolist(),
        "intercept_full": clf_full.intercept_.tolist(),
        "calib_r_viable_rate": float(np.mean(y_calib))
    }
    manifest_hash = hashlib.sha256(json.dumps(calib_manifest, sort_keys=True).encode("utf-8")).hexdigest()
    log(f"\n>>> DIAGNOSTIC MODEL FITTED & FROZEN <<<")
    log(f"Diagnostic Manifest SHA-256: {manifest_hash}")
    log(f"Coefficients (Full): delta_z: {clf_full.coef_[0][0]:.4f}, H_vocab: {clf_full.coef_[0][1]:.4f}, sigma_attn: {clf_full.coef_[0][2]:.4f}, PR_min: {clf_full.coef_[0][3]:.4f}, cos_drift: {clf_full.coef_[0][4]:.4f}")

    # ------------------------------------------------------------------------
    # Step 2: Held-Out Confirmatory Benchmark on D_test (N=100)
    # ------------------------------------------------------------------------
    log("\n==========================================================================")
    log("Step 2: Held-Out Confirmatory Benchmark on D_test (N=100, Seed 84/350)")
    log("==========================================================================")

    records = []
    y_test_R_viable = []
    y_scores_full = []
    y_scores_output = []
    y_scores_geom = []
    y_scores_attn = []

    for idx, inst in enumerate(d_test):
        prompt = inst["base"]
        target = inst["target"].strip() if "target" in inst else inst["target_token"].strip()
        t_id = tokenizer.encode(" " + target)[0] if tokenizer.encode(" " + target) else tokenizer.encode(target)[0]

        feat, input_ids = extract_label_free_observables(prompt, model, tokenizer, target_block=target_block)
        x_vec = np.array([[feat["delta_z_top2"], feat["h_vocab"], feat["sigma_h_attn"], feat["pr_min"], feat["cos_drift"]]])

        # 1. Base Forward Pass (Action Empty)
        with torch.no_grad():
            out_base = model(input_ids=input_ids)
            pred_empty = torch.argmax(out_base.logits[0, -1, :]).item()
        corr_empty = int(pred_empty == t_id)

        # 2. Reorganize Action (Action R)
        pred_r = execute_reorganization(model, input_ids, target_block=target_block)
        corr_r = int(pred_r == t_id)
        is_corrupt_r = int(corr_empty == 1 and corr_r == 0)

        # 3. Retrieve Action (Action S)
        pred_s = execute_retrieval(model, tokenizer, prompt, retriever)
        corr_s = int(pred_s == t_id)
        is_corrupt_s = int(corr_empty == 1 and corr_s == 0)

        # Calculate exact numerical utilities
        # U(a) = Correct - 0.05 * C(a) - 1.00 * Corrupted
        u_empty = corr_empty - 0.05 * 1.00
        u_r     = corr_r     - 0.05 * 1.05 - 1.00 * is_corrupt_r
        u_s     = corr_s     - 0.05 * 2.00 - 1.00 * is_corrupt_s

        # Oracle Action
        utilities = {"Empty": u_empty, "R": u_r, "S": u_s}
        a_oracle = max(utilities, key=utilities.get)

        # Diagnostic Predictions
        p_r_full = float(clf_full.predict_proba(x_vec)[0, 1])
        p_r_output = float(clf_output.predict_proba(x_vec[:, :2])[0, 1])
        p_r_geom = float(clf_geom.predict_proba(x_vec[:, 3:])[0, 1])
        p_r_attn = float(clf_attn.predict_proba(x_vec[:, 2:3])[0, 1])

        y_scores_full.append(p_r_full)
        y_scores_output.append(p_r_output)
        y_scores_geom.append(p_r_geom)
        y_scores_attn.append(p_r_attn)

        # Decision rule for diagnostic policy
        # Pre-registered rule:
        # If p_r >= 0.50 -> R
        # Elif p_r < 0.35 and H_vocab > 2.0 -> S
        # Else -> Empty
        if p_r_full >= 0.50:
            a_diag = "R"
        elif p_r_full < 0.35 and feat["h_vocab"] > 2.0:
            a_diag = "S"
        else:
            a_diag = "Empty"

        # Truth for R viability: did R rescue an error without corruption?
        r_rescued = (corr_empty == 0 and corr_r == 1)
        y_test_R_viable.append(1 if r_rescued else 0)

        records.append({
            "idx": idx,
            "corr_empty": corr_empty,
            "corr_r": corr_r,
            "corr_s": corr_s,
            "u_empty": round(u_empty, 4),
            "u_r": round(u_r, 4),
            "u_s": round(u_s, 4),
            "a_oracle": a_oracle,
            "a_diag": a_diag,
            "u_diag": round(utilities[a_diag], 4),
            "u_oracle": round(utilities[a_oracle], 4)
        })

    post_hash = get_param_hash(model)
    log(f"\nPost-experiment parameter SHA-256: {post_hash}")
    assert pre_hash == post_hash, f"CRITICAL: Parameter hash mismatch! Delta theta != 0 ({pre_hash} vs {post_hash})"
    log(">>> IMMUTABLE PARAMETER INVARIANCE CONFIRMED: Delta theta == 0 <<<")

    # ------------------------------------------------------------------------
    # Scorecard & Policy Comparisons
    # ------------------------------------------------------------------------
    N = len(records)
    mean_u_empty = float(np.mean([r["u_empty"] for r in records]))
    mean_u_r     = float(np.mean([r["u_r"] for r in records]))
    mean_u_s     = float(np.mean([r["u_s"] for r in records]))
    mean_u_diag  = float(np.mean([r["u_diag"] for r in records]))
    mean_u_oracle = float(np.mean([r["u_oracle"] for r in records]))

    acc_empty = float(np.mean([r["corr_empty"] for r in records]))
    acc_r     = float(np.mean([r["corr_r"] for r in records]))
    acc_s     = float(np.mean([r["corr_s"] for r in records]))
    acc_diag  = float(np.mean([r["corr_r"] if r["a_diag"]=="R" else (r["corr_s"] if r["a_diag"]=="S" else r["corr_empty"]) for r in records]))
    acc_oracle = float(np.mean([r["corr_r"] if r["a_oracle"]=="R" else (r["corr_s"] if r["a_oracle"]=="S" else r["corr_empty"]) for r in records]))

    corrupt_r = sum(1 for r in records if r["corr_empty"] == 1 and r["corr_r"] == 0)
    corrupt_s = sum(1 for r in records if r["corr_empty"] == 1 and r["corr_s"] == 0)
    corrupt_diag = sum(1 for r in records if r["corr_empty"] == 1 and (
        (r["a_diag"] == "R" and r["corr_r"] == 0) or (r["a_diag"] == "S" and r["corr_s"] == 0)
    ))

    # ROC-AUC across feature ablation hierarchy
    auc_full = float(roc_auc_score(y_test_R_viable, y_scores_full)) if sum(y_test_R_viable) > 0 else 0.5
    auc_output = float(roc_auc_score(y_test_R_viable, y_scores_output)) if sum(y_test_R_viable) > 0 else 0.5
    auc_geom = float(roc_auc_score(y_test_R_viable, y_scores_geom)) if sum(y_test_R_viable) > 0 else 0.5
    auc_attn = float(roc_auc_score(y_test_R_viable, y_scores_attn)) if sum(y_test_R_viable) > 0 else 0.5

    log("\n==========================================================================")
    log("Confirmatory Results & Policy Comparison (N=100)")
    log("==========================================================================")
    log(f"{'Policy':20s} | {'Accuracy':8s} | {'Mean Net Utility':16s} | {'Corruptions (c)':15s}")
    log("-" * 68)
    log(f"{'pi_always_empty':20s} | {acc_empty*100:6.2f}% | {mean_u_empty:+16.4f} | {0:15d}")
    log(f"{'pi_always_R':20s} | {acc_r*100:6.2f}% | {mean_u_r:+16.4f} | {corrupt_r:15d}")
    log(f"{'pi_always_S':20s} | {acc_s*100:6.2f}% | {mean_u_s:+16.4f} | {corrupt_s:15d}")
    log(f"{'pi_diagnostic':20s} | {acc_diag*100:6.2f}% | {mean_u_diag:+16.4f} | {corrupt_diag:15d}")
    log(f"{'pi_oracle':20s} | {acc_oracle*100:6.2f}% | {mean_u_oracle:+16.4f} | {0:15d}")

    log("\n--- Feature Ablation Hierarchy (ROC-AUC for Predicting R-Viability) ---")
    log(f"D_full   (All 5 features):         AUC = {auc_full:.4f}")
    log(f"D_output (Top2 Gap + Vocab Ent):   AUC = {auc_output:.4f}")
    log(f"D_geom   (PR_min + Cos Drift):     AUC = {auc_geom:.4f}")
    log(f"D_attn   (Head Ent Dispersion):    AUC = {auc_attn:.4f}")

    # Resolution of Hypotheses
    h_select_confirmed = (mean_u_diag > max(mean_u_empty, mean_u_r, mean_u_s))
    h_roc_confirmed = (auc_full >= 0.75)

    log("\n==========================================================================")
    log("Falsification Hierarchy Resolution")
    log("==========================================================================")
    log(f"Hypothesis 1 (Utility Superiority: mean_u_diag > max(blind)): {h_select_confirmed} ({mean_u_diag:+.4f} vs max_blind={max(mean_u_empty, mean_u_r, mean_u_s):+.4f})")
    log(f"Hypothesis 2 (Discrimination AUC >= 0.75):                  {h_roc_confirmed} (AUC={auc_full:.4f})")

    if h_select_confirmed and h_roc_confirmed:
        resolution = "OUTCOME_1_PROSPECTIVE_DIAGNOSIS_AND_UTILITY_GAIN_CONFIRMED"
        verdict = "CONFIRMED: The frozen diagnostic policy achieved strictly superior net utility over all blind computation policies and discriminated representation-access viability with AUC >= 0.75."
    elif h_select_confirmed:
        resolution = "OUTCOME_2_UTILITY_GAIN_CONFIRMED_MODERATE_AUC"
        verdict = "PARTIALLY CONFIRMED: Diagnostic action allocation achieved superior net utility over blind policies, though discrimination AUC was below 0.75."
    elif h_roc_confirmed:
        resolution = "OUTCOME_3_AUC_CONFIRMED_UTILITY_INSUFFICIENT"
        verdict = "PARTIALLY CONFIRMED: High diagnostic discrimination AUC, but net utility did not surpass the best blind policy under the locked cost/risk equation."
    else:
        resolution = "OUTCOME_4_PROSPECTIVE_DIAGNOSIS_REFUTED"
        verdict = "REFUTED: Neither utility superiority nor discrimination threshold was achieved."

    log(f"\nTRI-STATE RESOLUTION: {resolution}")
    log(f"VERDICT: {verdict}\n")

    # Serialize results to JSON
    out_dir = r"c:\Users\Anilkumar\OneDrive\Desktop\SCPM\experiments\runs\EXP046_prospective_diagnosis"
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "exp046_prospective_diagnosis_results.json")

    payload = {
        "experiment_id": "EXP046",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "model_name": model_name,
        "pre_param_hash": pre_hash,
        "post_param_hash": post_hash,
        "diagnostic_manifest_hash": manifest_hash,
        "sample_size": N,
        "metrics": {
            "pi_always_empty": {"accuracy": acc_empty, "mean_utility": mean_u_empty, "corruptions": 0},
            "pi_always_R":     {"accuracy": acc_r,     "mean_utility": mean_u_r,     "corruptions": corrupt_r},
            "pi_always_S":     {"accuracy": acc_s,     "mean_utility": mean_u_s,     "corruptions": corrupt_s},
            "pi_diagnostic":   {"accuracy": acc_diag,  "mean_utility": mean_u_diag,  "corruptions": corrupt_diag},
            "pi_oracle":       {"accuracy": acc_oracle, "mean_utility": mean_u_oracle, "corruptions": 0}
        },
        "ablation_auc": {
            "D_full": auc_full,
            "D_output": auc_output,
            "D_geom": auc_geom,
            "D_attn": auc_attn
        },
        "hypothesis_resolutions": {
            "H_select_utility_superiority": h_select_confirmed,
            "H_ROC_discrimination": h_roc_confirmed
        },
        "resolution": resolution,
        "verdict": verdict
    }

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    log(f"Results serialized to: {out_file}")

if __name__ == "__main__":
    run_exp046()
