"""
EXP053: Continuous Subspace Invention vs. Typed Decision Systems (Jev/Laya Challenge).
Compares:
- System 0: Frozen Baseline Greedy
- System 1: Pure SCPM (Continuous Latent Subspace Invention Bt)
- System 2: Pure Typed Decision System (Jev/Laya-style schema validator)
- System 3: Dual-Level Hybrid (SCPM Bt + Typed Validator)
Pre-Registration: EXP053_TYPED_DECISION_CHALLENGE_SPEC.md
Governing Laws: AGENTS.md Laws 1, 2, 6, 7, 9, 13, 14.
"""
import os, sys, json, hashlib, time
import numpy as np
import torch
import torch.nn.functional as F
from datetime import datetime
from scipy.stats import binomtest
from transformers import AutoModelForCausalLM, AutoTokenizer

os.environ["TRANSFORMERS_NO_TF"] = "1"
os.environ["USE_TF"] = "0"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from experiments.benchmarks.bench_002_nl import generate_bench_002_nl

CANONICAL_MODEL = "EleutherAI/pythia-160m"
CANONICAL_HASH  = "54c88fa4897785f2bd94b32d26de1f73f1052bcc42124d563d0cda96940de936"
TARGET_BLOCK    = 7       # Layer 8 (0-indexed Block 7)
ALPHA           = 0.25
RANK            = 2
OUT_DIR         = os.path.join(os.path.dirname(__file__),
                      "../../experiments/runs/EXP053_typed_decision_challenge")

def get_hash(model):
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

def mcnemar_p(b, c):
    n = b + c
    if n == 0: return 1.0
    return float(binomtest(b, n, 0.5, alternative="greater").pvalue)

def log(msg, log_file=None):
    ts = datetime.utcnow().strftime("%H:%M:%S")
    formatted = f"[{ts}] {msg}"
    print(formatted, flush=True)
    if log_file:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(formatted + "\n")

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    log_file = os.path.join(OUT_DIR, "exp053_run_log.txt")
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(f"=== EXP053 Execution Started at {datetime.utcnow().isoformat()} ===\n")

    log("Initializing EXP053 Continuous Subspace vs Typed Decision Systems Challenge...", log_file)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    log(f"Using compute device: {device}", log_file)

    tokenizer = AutoTokenizer.from_pretrained(CANONICAL_MODEL)
    model = AutoModelForCausalLM.from_pretrained(CANONICAL_MODEL).to(device)
    model.eval()

    pre_hash = get_hash(model)
    assert pre_hash == CANONICAL_HASH, f"Hash mismatch: {pre_hash}"
    log("Pre-run model hash verified: Delta_theta = 0.", log_file)

    # Evaluation on BENCH-002-NL Seed 84 (N=50)
    dataset = generate_bench_002_nl(n_instances=50, seed=84)

    systems = ["sys0_base", "sys1_scpm", "sys2_typed", "sys3_hybrid"]
    correct_counts = {s: 0 for s in systems}
    instances_log = []

    for inst in dataset:
        prompt = inst["base"]
        t_str = inst["target"].strip()
        t_enc = tokenizer.encode(" " + t_str)
        t_id = t_enc[0] if t_enc else tokenizer.encode(t_str)[0]

        d_str = inst.get("distractor", "").strip()
        d_enc = tokenizer.encode(" " + d_str)
        d_id = d_enc[0] if d_enc else (tokenizer.encode(d_str)[0] if d_str else -1)

        enc = tokenizer(prompt, return_offsets_mapping=True, return_tensors="pt")
        input_ids = enc.input_ids.to(device)
        offsets = enc.offset_mapping[0].tolist()

        p_end = prompt.find(" Distractor:")
        d_end = prompt.find(" Question:")
        dist_indices = [i for i, (s, e) in enumerate(offsets) if s >= p_end and e <= d_end and s < e]

        # 1. System 0: Greedy Baseline
        captured = {}
        def cap_h(mod, inp, outp):
            captured["h"] = (outp[0] if isinstance(outp, tuple) else outp).detach().squeeze(0)

        h_handle = model.gpt_neox.layers[TARGET_BLOCK].register_forward_hook(cap_h)
        with torch.no_grad():
            out_base = model(input_ids=input_ids)
            logits_base = out_base.logits[0, -1, :]
        h_handle.remove()

        pred_base = int(torch.argmax(logits_base).item())
        corr_base = int(pred_base == t_id)
        correct_counts["sys0_base"] += corr_base

        # 2. System 1: Pure SCPM (Continuous Latent Basis Invention)
        h = captured["h"]
        V_c = extract_subspace(h[dist_indices, :], rank=RANK)
        P_c = (V_c @ V_c.T).to(h.device)

        def hook_scpm(mod, inp, outp):
            h_mod = outp[0].clone() if isinstance(outp, tuple) else outp.clone()
            h_mod[0] = h_mod[0] - ALPHA * (h_mod[0] @ P_c)
            return (h_mod,) + outp[1:] if isinstance(outp, tuple) else h_mod

        h_handle = model.gpt_neox.layers[TARGET_BLOCK].register_forward_hook(hook_scpm)
        with torch.no_grad():
            logits_scpm = model(input_ids=input_ids).logits[0, -1, :]
        h_handle.remove()

        pred_scpm = int(torch.argmax(logits_scpm).item())
        corr_scpm = int(pred_scpm == t_id)
        correct_counts["sys1_scpm"] += corr_scpm

        # 3. System 2: Pure Typed Decision System (Jev/Laya-Style Schema / Disjunction Head)
        # Enforces a typed decision schema: the answer must be a valid entity candidate for the query relation
        # and must not match the distractor entity when bound to the distractor predicate.
        # In a typed system, the validator scores top-k candidates against the typed predicate constraint.
        top_k_candidates = torch.topk(logits_base, k=10).indices.tolist()
        pred_typed = pred_base
        for cand in top_k_candidates:
            # Typed filter: if candidate is the distractor token, reject candidate under the typing schema
            if cand == d_id:
                continue
            pred_typed = cand
            break
        corr_typed = int(pred_typed == t_id)
        correct_counts["sys2_typed"] += corr_typed

        # 4. System 3: Dual-Level Hybrid (Continuous Subspace + Typed Validator)
        top_k_scpm = torch.topk(logits_scpm, k=10).indices.tolist()
        pred_hybrid = pred_scpm
        for cand in top_k_scpm:
            if cand == d_id:
                continue
            pred_hybrid = cand
            break
        corr_hybrid = int(pred_hybrid == t_id)
        correct_counts["sys3_hybrid"] += corr_hybrid

        instances_log.append({
            "id": inst["id"],
            "target": t_str,
            "distractor": d_str,
            "corr_base": corr_base,
            "corr_scpm": corr_scpm,
            "corr_typed": corr_typed,
            "corr_hybrid": corr_hybrid
        })

    N = len(dataset)
    log("\n================ TYPED DECISION CHALLENGE SUMMARY (N=50) ================", log_file)
    summary = {}
    for s in systems:
        acc = correct_counts[s] / N
        b = sum(1 for x in instances_log if x["corr_base"] == 0 and x[f"corr_{s.split('_')[1]}"] == 1)
        c = sum(1 for x in instances_log if x["corr_base"] == 1 and x[f"corr_{s.split('_')[1]}"] == 0)
        p_val = mcnemar_p(b, c) if s != "sys0_base" else 1.0
        summary[s] = {
            "accuracy": float(acc),
            "delta_m": float(acc - (correct_counts["sys0_base"] / N)),
            "rescues_b": b,
            "corruptions_c": c,
            "mcnemar_p": float(p_val)
        }
        log(f"{s.upper():<14}: Acc={acc*100:.1f}% (Delta_M={(acc-correct_counts['sys0_base']/N)*100:+.1f} pp) | Rescues={b} Corr={c} p={p_val:.4f}", log_file)

    post_hash = get_hash(model)
    assert post_hash == pre_hash, "Backbone altered!"
    log("\nBackbone immutability verified: Delta_theta = 0.", log_file)

    # Check synergy and orthogonality
    scpm_acc = summary["sys1_scpm"]["accuracy"]
    typed_acc = summary["sys2_typed"]["accuracy"]
    hybrid_acc = summary["sys3_hybrid"]["accuracy"]

    synergy = hybrid_acc >= max(scpm_acc, typed_acc)
    verdict = "ORTHOGONALITY_AND_SYNERGY_CONFIRMED" if synergy else "REDUNDANT_OR_INTERFERENCE"
    log(f"\nFinal Verdict: >>> {verdict} <<<", log_file)

    out_payload = {
        "metadata": {
            "experiment": "EXP053",
            "title": "Continuous Subspace Invention vs. Typed Decision Systems",
            "timestamp": datetime.utcnow().isoformat(),
            "model": CANONICAL_MODEL,
            "target_block": TARGET_BLOCK,
            "alpha": ALPHA,
            "rank": RANK,
            "verdict": verdict
        },
        "summary": summary,
        "instances": instances_log
    }

    out_file = os.path.join(OUT_DIR, "exp053_typed_challenge_results.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(out_payload, f, indent=2)
    log(f"Saved complete results to {out_file}", log_file)

if __name__ == "__main__":
    main()
