"""
EXP060: Relational Capability Ladder and Intervention-Ceiling Decomposition.
Tests Base vs. Privileged Oracle vs. Autonomous SCPM across 6 levels of relational complexity:
- Level 0: Lexical In-Context Recall (A -> B)
- Level 1: Direct Relational Mapping (1-hop: A > B)
- Level 2: 2-Hop Transitive Deduction (Clean Chain with Surface Permutations)
- Level 3: 3-Hop Transitive Deduction (Deep Chain: A > B > C > D)
- Level 4: Distractor-Resistant Transitivity (Interleaved Distractor Relations)
- Level 5: Compositional Transfer Across Disjoint Vocabulary

Governing Standard: AGENTS.md Laws 1, 2, 6, 7, 9, 11, 13, 14.
Pre-Registration: EXP060_CAPABILITY_LADDER_SPEC.md
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
from experiments.benchmarks.bench_007_capability_ladder import generate_bench_007_capability_ladder

CANONICAL_MODEL = "EleutherAI/pythia-160m"
CANONICAL_HASH  = "54c88fa4897785f2bd94b32d26de1f73f1052bcc42124d563d0cda96940de936"
TARGET_BLOCK    = 7       # Layer 8 (0-indexed Block 7)
ALPHA           = 0.25
OUT_DIR         = os.path.join(os.path.dirname(__file__), "../../experiments/runs/EXP060_capability_ladder")

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
    log_file = os.path.join(OUT_DIR, "exp060_run_log.txt")
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(f"=== EXP060 Execution Started at {datetime.now(timezone.utc).isoformat()} ===\n")

    log("Initializing EXP060 Relational Capability Ladder...", log_file)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    log(f"Using compute device: {device}", log_file)

    tokenizer = AutoTokenizer.from_pretrained(CANONICAL_MODEL)
    model = AutoModelForCausalLM.from_pretrained(CANONICAL_MODEL).to(device)
    model.eval()

    pre_hash = get_hash(model)
    log(f"Pre-run model SHA-256: {pre_hash}", log_file)
    assert pre_hash == CANONICAL_HASH, f"Model parameter hash mismatch: {pre_hash}"
    log("Verified frozen model parameter immutability.", log_file)

    dataset = generate_bench_007_capability_ladder()
    log(f"Loaded {len(dataset)} total benchmark instances across 6 levels.", log_file)

    # Pre-extract prompt activations for all instances to enable leave-one-out Oracle construction
    log("Extracting base layer 7 prompt activations across all levels...", log_file)
    act_cache = {}
    for inst in dataset:
        iid = inst["id"]
        enc = tokenizer(inst["prompt"], return_tensors="pt")
        inp_ids = enc.input_ids.to(device)
        
        cap = {}
        def hook_fn(mod, inp, outp):
            cap["h"] = (outp[0] if isinstance(outp, tuple) else outp).detach().squeeze(0)
        
        handle = model.gpt_neox.layers[TARGET_BLOCK].register_forward_hook(hook_fn)
        with torch.no_grad():
            out = model(input_ids=inp_ids)
        handle.remove()
        
        h_seq = cap["h"] # [seq_len, d_model]
        logits = out.logits[0, -1, :]
        log_probs = F.log_softmax(logits, dim=-1)
        
        t_tok = tokenizer.encode(inst["target_token"])[0]
        f_tok = tokenizer.encode(inst["foil_token"])[0]
        
        base_correct = bool(logits[t_tok] > logits[f_tok])
        base_margin = float((logits[t_tok] - logits[f_tok]).item())
        base_log_p = float(log_probs[t_tok].item())
        
        act_cache[iid] = {
            "h_seq": h_seq,
            "h_last": h_seq[-1, :],
            "t_tok": t_tok,
            "f_tok": f_tok,
            "base_correct": base_correct,
            "base_margin": base_margin,
            "base_log_p": base_log_p
        }

    # Evaluate each level independently
    level_results = {}
    total_rescues_oracle = 0
    total_corruptions_oracle = 0
    total_rescues_auto = 0
    total_corruptions_auto = 0

    for level in range(6):
        level_items = [d for d in dataset if d["level"] == level]
        lvl_name = level_items[0]["level_name"]
        log(f"\n{'='*70}\nEVALUATING LEVEL {level}: {lvl_name} (N={len(level_items)})\n{'='*70}", log_file)

        # -------------------------------------------------------------
        # 1. Oracle Privileged Intervention:
        # For each instance i, construct Oracle direction from all other
        # instances j != i in Level k using ground-truth target vs foil contrast
        # -------------------------------------------------------------
        oracle_eval = []
        auto_eval = []
        base_eval = []

        for inst in level_items:
            iid = inst["id"]
            c = act_cache[iid]
            base_eval.append({
                "id": iid,
                "correct": c["base_correct"],
                "margin": c["base_margin"],
                "log_p": c["base_log_p"],
                "target_queried_first": inst["target_queried_first"],
                "surface_reversed": inst["surface_reversed"]
            })

            # --- PRIVILEGED ORACLE DIRECTION (Leave-One-Out) ---
            # Aggregate privileged contrast difference vectors across other instances j != i
            other_items = [d for d in level_items if d["id"] != iid]
            diff_vecs = []
            for oj in other_items:
                oj_c = act_cache[oj["id"]]
                # Unembedding difference vector for ground-truth target vs foil
                w_diff = model.embed_out.weight[oj_c["t_tok"], :] - model.embed_out.weight[oj_c["f_tok"], :]
                diff_vecs.append(w_diff)
            
            if diff_vecs:
                mean_v = torch.stack(diff_vecs).mean(dim=0)
                v_oracle = mean_v / (torch.norm(mean_v) + 1e-8)
            else:
                v_oracle = torch.randn(model.config.hidden_size, device=device)
                v_oracle = v_oracle / torch.norm(v_oracle)

            # --- PRIVILEGED ORACLE INTERVENTION ---
            # Evaluates privileged directions with ground-truth target access:
            # 1. Direct unembedding difference (W_U[target] - W_U[foil])
            # 2. Direct embedding difference (W_E[target] - W_E[foil])
            # 3. Leave-one-out relational representation contrast
            w_u_diff = model.embed_out.weight[c["t_tok"], :] - model.embed_out.weight[c["f_tok"], :]
            v_u = w_u_diff / (torch.norm(w_u_diff) + 1e-8)
            
            w_e_diff = model.gpt_neox.embed_in.weight[c["t_tok"], :] - model.gpt_neox.embed_in.weight[c["f_tok"], :]
            v_e = w_e_diff / (torch.norm(w_e_diff) + 1e-8)

            other_items = [d for d in level_items if d["id"] != iid]
            loo_diffs = []
            for oj in other_items:
                oj_c = act_cache[oj["id"]]
                sign = 1.0 if oj["target_queried_first"] else -1.0
                loo_diffs.append(sign * oj_c["h_last"])
            if loo_diffs:
                mean_loo = torch.stack(loo_diffs).mean(dim=0)
                v_loo = mean_loo / (torch.norm(mean_loo) + 1e-8)
            else:
                v_loo = v_u

            oracle_candidates = [v_u, v_e, v_loo]
            best_orc_cand = None
            best_orc_log_p = -1e9
            best_orc_out = None

            for cand_v in oracle_candidates:
                cand_norm = cand_v / (torch.norm(cand_v) + 1e-8)
                def test_orc_hook(mod, inp, outp):
                    h = outp[0] if isinstance(outp, tuple) else outp
                    h_mod = h.clone()
                    h_mod[:, -1, :] = h_mod[:, -1, :] + ALPHA * cand_norm
                    return (h_mod,) + outp[1:] if isinstance(outp, tuple) else h_mod

                h_handle = model.gpt_neox.layers[TARGET_BLOCK].register_forward_hook(test_orc_hook)
                with torch.no_grad():
                    out_test = model(input_ids=inp_ids)
                h_handle.remove()

                t_logits = out_test.logits[0, -1, :]
                t_log_probs = F.log_softmax(t_logits, dim=-1)
                t_lp = float(t_log_probs[c["t_tok"]].item())
                if t_lp > best_orc_log_p:
                    best_orc_log_p = t_lp
                    best_orc_cand = cand_norm
                    best_orc_out = out_test

            orc_logits = best_orc_out.logits[0, -1, :]
            orc_log_probs = F.log_softmax(orc_logits, dim=-1)
            orc_correct = bool(orc_logits[c["t_tok"]] > orc_logits[c["f_tok"]])
            orc_margin = float((orc_logits[c["t_tok"]] - orc_logits[c["f_tok"]]).item())
            orc_log_p = float(orc_log_probs[c["t_tok"]].item())

            oracle_eval.append({
                "id": iid,
                "correct": orc_correct,
                "margin": orc_margin,
                "log_p": orc_log_p,
                "rescued": (not c["base_correct"]) and orc_correct,
                "corrupted": c["base_correct"] and (not orc_correct)
            })

            # --- AUTONOMOUS SCPM (Zero Labels, Unguided) ---
            # Candidates derived strictly from prompt hidden activations:
            # Cand 1: SVD / PCA of prompt token trajectory
            h_seq = c["h_seq"]
            h_centered = h_seq - h_seq.mean(dim=0, keepdim=True)
            try:
                _, _, Vh = torch.linalg.svd(h_centered, full_matrices=False)
                v_svd = Vh[0, :].to(device)
            except Exception:
                v_svd = torch.zeros(model.config.hidden_size, device=device)

            # Cand 2: Endpoint dynamic difference (h[-1] - h[0])
            v_dyn = h_seq[-1, :] - h_seq[0, :]
            v_dyn = v_dyn / (torch.norm(v_dyn) + 1e-8)

            # Cand 3: Local context curvature (h[-1] - h[-2])
            v_curv = h_seq[-1, :] - h_seq[-2, :]
            v_curv = v_curv / (torch.norm(v_curv) + 1e-8)

            # Cand 4: Null / Identity
            v_null = torch.zeros(model.config.hidden_size, device=device)

            candidates = [v_svd, v_dyn, v_curv, v_null]
            cand_scores = []

            for cand_v in candidates:
                if torch.norm(cand_v) == 0:
                    cand_scores.append(-999.0)
                    continue
                cand_norm = cand_v / (torch.norm(cand_v) + 1e-8)
                
                def test_hook(mod, inp, outp):
                    h = outp[0] if isinstance(outp, tuple) else outp
                    h_mod = h.clone()
                    h_mod[:, -1, :] = h_mod[:, -1, :] + ALPHA * cand_norm
                    return (h_mod,) + outp[1:] if isinstance(outp, tuple) else h_mod

                h_sub = model.gpt_neox.layers[TARGET_BLOCK].register_forward_hook(test_hook)
                with torch.no_grad():
                    out_test = model(input_ids=inp_ids)
                h_sub.remove()

                t_logits = out_test.logits[0, -1, :]
                top2 = torch.topk(t_logits, k=2).values
                # Grounded self-consistency margin utility (confidence separation)
                margin_util = float((top2[0] - top2[1]).item())
                cand_scores.append(margin_util)

            best_idx = int(np.argmax(cand_scores))
            best_cand = candidates[best_idx]
            if torch.norm(best_cand) > 0:
                best_cand = best_cand / (torch.norm(best_cand) + 1e-8)

            def auto_hook(mod, inp, outp):
                h = outp[0] if isinstance(outp, tuple) else outp
                h_mod = h.clone()
                if torch.norm(best_cand) > 0:
                    h_mod[:, -1, :] = h_mod[:, -1, :] + ALPHA * best_cand
                    return (h_mod,) + outp[1:] if isinstance(outp, tuple) else h_mod
                return outp

            h_auto = model.gpt_neox.layers[TARGET_BLOCK].register_forward_hook(auto_hook)
            with torch.no_grad():
                out_auto = model(input_ids=inp_ids)
            h_auto.remove()

            auto_logits = out_auto.logits[0, -1, :]
            auto_log_probs = F.log_softmax(auto_logits, dim=-1)
            auto_correct = bool(auto_logits[c["t_tok"]] > auto_logits[c["f_tok"]])
            auto_margin = float((auto_logits[c["t_tok"]] - auto_logits[c["f_tok"]]).item())
            auto_log_p = float(auto_log_probs[c["t_tok"]].item())

            auto_eval.append({
                "id": iid,
                "selected_candidate": best_idx,
                "correct": auto_correct,
                "margin": auto_margin,
                "log_p": auto_log_p,
                "rescued": (not c["base_correct"]) and auto_correct,
                "corrupted": c["base_correct"] and (not auto_correct)
            })

        # --- LEVEL STATISTICS ---
        n_inst = len(level_items)
        base_acc = sum(1 for x in base_eval if x["correct"]) / n_inst
        orc_acc = sum(1 for x in oracle_eval if x["correct"]) / n_inst
        auto_acc = sum(1 for x in auto_eval if x["correct"]) / n_inst

        orc_rescues = sum(1 for x in oracle_eval if x["rescued"])
        orc_corruptions = sum(1 for x in oracle_eval if x["corrupted"])
        auto_rescues = sum(1 for x in auto_eval if x["rescued"])
        auto_corruptions = sum(1 for x in auto_eval if x["corrupted"])

        total_rescues_oracle += orc_rescues
        total_corruptions_oracle += orc_corruptions
        total_rescues_auto += auto_rescues
        total_corruptions_auto += auto_corruptions

        delta_orc = (orc_acc - base_acc) * 100.0
        delta_auto = (auto_acc - base_acc) * 100.0
        
        # RDG = M(oracle) - M(autonomous)
        # Interpretable ONLY if delta_orc > 0
        if delta_orc > 0:
            rdg_val = (orc_acc - auto_acc) * 100.0
            rdg_str = f"{rdg_val:+.1f} pp"
        else:
            rdg_val = None
            rdg_str = "NON_INTERPRETABLE (Oracle <= Base)"

        p_orc = mcnemar_p(orc_rescues, orc_corruptions)
        p_auto = mcnemar_p(auto_rescues, auto_corruptions)

        delta_log_p_orc = np.mean([o["log_p"] - b["log_p"] for o, b in zip(oracle_eval, base_eval)])
        delta_log_p_auto = np.mean([a["log_p"] - b["log_p"] for a, b in zip(auto_eval, base_eval)])

        # Positional Heuristic Breakdown: Target Queried First vs Second
        base_first_acc = np.mean([b["correct"] for b in base_eval if b["target_queried_first"]])
        base_second_acc = np.mean([b["correct"] for b in base_eval if not b["target_queried_first"]])

        # Surface Order Permutation Breakdown (for Levels with surface permutations)
        has_permutations = any(b["surface_reversed"] for b in base_eval)
        if has_permutations:
            canon_acc = np.mean([b["correct"] for b in base_eval if not b["surface_reversed"]])
            rev_acc = np.mean([b["correct"] for b in base_eval if b["surface_reversed"]])
            perm_str = f"Canonical Order: {canon_acc*100:.1f}% | Reversed Premise Order: {rev_acc*100:.1f}%"
        else:
            perm_str = "N/A (Standard ordering)"

        # Adjudicate Diagnostic Tree
        if delta_orc <= 0:
            verdict = "REPRESENTATION_INTERVENTION_CEILING (Latent computation absent or unsteerable)"
        elif delta_orc > 0 and delta_auto <= 0:
            verdict = "AUTONOMOUS_DISCOVERY_BOTTLENECK (Computation recoverable via Oracle, SCPM fails discovery)"
        elif delta_auto > 0 and p_auto < 0.05:
            verdict = "AUTONOMOUS_CAPABILITY_CONFIRMED (Both recoverable and discoverable)"
        else:
            verdict = "WEAK_EFFECT_OR_INCONCLUSIVE"

        log(f"Level {level} Summary ({lvl_name}):", log_file)
        log(f"  Base Accuracy:       {base_acc*100:.1f}%", log_file)
        log(f"  Oracle Accuracy:     {orc_acc*100:.1f}% (Delta_M = {delta_orc:+.1f} pp, b={orc_rescues}, c={orc_corruptions}, p={p_orc:.4f})", log_file)
        log(f"  Autonomous Accuracy: {auto_acc*100:.1f}% (Delta_M = {delta_auto:+.1f} pp, b={auto_rescues}, c={auto_corruptions}, p={p_auto:.4f})", log_file)
        log(f"  Representation Discovery Gap (RDG): {rdg_str}", log_file)
        log(f"  Mean Delta Log-P:    Oracle={delta_log_p_orc:+.4f} | Auto={delta_log_p_auto:+.4f}", log_file)
        log(f"  Target First Acc:    {base_first_acc*100:.1f}% | Target Second Acc: {base_second_acc*100:.1f}%", log_file)
        log(f"  Permutation Test:    {perm_str}", log_file)
        log(f"  Diagnostic Verdict:  {verdict}", log_file)

        level_results[level] = {
            "level": level,
            "level_name": lvl_name,
            "n_instances": n_inst,
            "base_acc": base_acc,
            "oracle_acc": orc_acc,
            "delta_m_oracle": delta_orc,
            "auto_acc": auto_acc,
            "delta_m_auto": delta_auto,
            "rdg": rdg_val,
            "oracle_rescues": orc_rescues,
            "oracle_corruptions": orc_corruptions,
            "oracle_p": p_orc,
            "auto_rescues": auto_rescues,
            "auto_corruptions": auto_corruptions,
            "auto_p": p_auto,
            "delta_log_p_oracle": float(delta_log_p_orc),
            "delta_log_p_auto": float(delta_log_p_auto),
            "base_target_first_acc": float(base_first_acc),
            "base_target_second_acc": float(base_second_acc),
            "surface_permutation_analysis": perm_str,
            "diagnostic_verdict": verdict
        }

    # Verify model immutability
    post_hash = get_hash(model)
    log(f"\nPost-run model SHA-256: {post_hash}", log_file)
    assert post_hash == CANONICAL_HASH, f"CRITICAL: Post-run hash corrupted: {post_hash}"
    log("Delta_theta = 0 confirmed post-experiment.", log_file)

    # Compile Final Ledger
    out_payload = {
        "experiment_id": "EXP060",
        "date": datetime.now(timezone.utc).isoformat(),
        "model": CANONICAL_MODEL,
        "canonical_hash": CANONICAL_HASH,
        "delta_theta": 0,
        "target_block": TARGET_BLOCK,
        "alpha": ALPHA,
        "n_total_instances": len(dataset),
        "total_rescues_oracle": total_rescues_oracle,
        "total_corruptions_oracle": total_corruptions_oracle,
        "total_rescues_auto": total_rescues_auto,
        "total_corruptions_auto": total_corruptions_auto,
        "level_breakdown": level_results
    }

    out_json = os.path.join(OUT_DIR, "exp060_results.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(out_payload, f, indent=2)

    log(f"\nEXP060 execution completed. Full results saved to: {out_json}", log_file)

if __name__ == "__main__":
    main()
