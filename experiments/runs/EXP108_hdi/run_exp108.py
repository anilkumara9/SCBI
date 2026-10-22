#!/usr/bin/env python3
"""EXP108 (H1/HDI) executor — executes EXACTLY per research/prereg/EXP_PREREG_H1_HDI_2026-09-29.md.

$0 CPU. Read-only on signed artifacts. No push, no GPU, no weights touched.
Any RUN-INVALID precondition -> STOP, report evidence, no metric read.
"""
import hashlib
import json
import os
import sys
import time

import numpy as np
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import balanced_accuracy_score

# ---------------------------------------------------------------- pins ----
PIN_BACKBONE = "ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed"  # LOG-331
PIN_PROVENANCE = "47281cd3dc243369be0aa5be2345663b752cdb4a329a16a37f08da5717230585"
SNAPSHOT = os.path.expanduser("~/workspace/.exp086_weights/pythia-410m")
RUNS_DIR = os.path.expanduser("~/workspace/SCBI/experiments/runs")
OUTDIR = os.path.join(RUNS_DIR, "EXP108_hdi", "out")
LAYER = 20
G4_FLOOR = 1e-4
N = 60

os.makedirs(OUTDIR, exist_ok=True)
log_lines = []


def log(msg):
    line = f"[exp108] {msg}"
    print(line, flush=True)
    log_lines.append(line)


class RunInvalid(Exception):
    pass


def sha256_state_dict(state_dict):
    """Exact EXP077/EXP084 convention: tensor bytes ONLY, sorted keys, float32."""
    h = hashlib.sha256()
    for k in sorted(state_dict.keys()):
        t = state_dict[k]
        if hasattr(t, "detach"):
            arr = t.detach().cpu().to(torch.float32).numpy()
        else:
            arr = np.asarray(t, dtype=np.float32)
        h.update(arr.tobytes())
    return h.hexdigest()


def main():
    t0 = time.time()
    torch.manual_seed(0)
    np.random.seed(0)

    # ---- Phase 0a: provenance pin ----
    prov_path = os.path.join(RUNS_DIR, "EXP077_cone_vs_line", "exp077_instance_records.json")
    with open(prov_path, "rb") as f:
        prov_hash = hashlib.sha256(f.read()).hexdigest()
    if prov_hash != PIN_PROVENANCE:
        raise RunInvalid(f"RUN-INVALID: provenance SHA-256 mismatch "
                         f"(got {prov_hash}, expected {PIN_PROVENANCE}). No metric exists.")
    log(f"provenance pin OK: {prov_hash[:16]}...")

    # ---- Phase 0b: bench build (verbatim) ----
    sys.path.insert(0, os.path.join(RUNS_DIR, "EXP089_clm8b_falsifier"))
    from benchmark_exp089 import build_benchmark, state_text_of
    bench = build_benchmark()
    if len(bench) != N:
        raise RunInvalid(f"RUN-INVALID: bench length {len(bench)} != {N} (Law #9).")
    log(f"bench OK: {len(bench)} items")

    # ---- Phase 1: load frozen backbone, pre-hash ----
    tokenizer = AutoTokenizer.from_pretrained(SNAPSHOT, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(
        SNAPSHOT, local_files_only=True, torch_dtype=torch.float32, device_map="cpu")
    model.eval()
    hash_before = sha256_state_dict(model.state_dict())
    if hash_before != PIN_BACKBONE:
        raise RunInvalid(f"RUN-INVALID: backbone hash mismatch (got {hash_before}, "
                         f"expected LOG-331 pin). Quarantine. No metric exists.")
    log(f"pre-hash OK: {hash_before[:16]}... (Δθ=0)")

    def encode1(text):
        return tokenizer.encode(text, add_special_tokens=False)

    def layer20_final(text):
        ids = torch.tensor([encode1(text)], dtype=torch.long)
        with torch.no_grad():
            out = model(ids, output_hidden_states=True)
            return out.hidden_states[LAYER][0, -1, :].detach().cpu().to(torch.float32).numpy()

    def cosine(a, b):
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

    # ---- Phase 2: extraction + registered decision statistic ----
    records = []
    cos_vals = []
    n_ties = 0
    state_embs = []
    for item in bench:
        st = state_text_of(item["prompt"])  # asserts prompt starts with "Premise:"
        tokA = encode1(" " + item["A"])
        tokC = encode1(" " + item["C"])
        if len(tokA) != 1 or len(tokC) != 1:
            raise RunInvalid(f"RUN-INVALID: single-token BPE assertion failed on item "
                             f"{item['id']} (A={tokA}, C={tokC}). Items NOT silently dropped.")
        se = layer20_final(st)
        ae = layer20_final(" " + item["A"])
        ce = layer20_final(" " + item["C"])
        cosA = cosine(se, ae)
        cosC = cosine(se, ce)
        if cosA == cosC:
            n_ties += 1
        decision = "A" if cosA > cosC else "C"  # ties -> C (conservative)
        cos_vals += [cosA, cosC]
        state_embs.append(se)
        records.append({
            "id": item["id"], "A": item["A"], "C": item["C"],
            "cosA": cosA, "cosC": cosC, "margin": abs(cosA - cosC),
            "tie": bool(cosA == cosC), "decision": decision,
        })
    log(f"extraction complete: 180 forward passes; ties toward C: {n_ties}")

    # ---- Phase 2b: G4 instrument-health gate ----
    spread = max(cos_vals) - min(cos_vals)
    margins = [r["margin"] for r in records]
    if spread < G4_FLOOR:
        raise RunInvalid(f"RUN-INVALID (instrument deaf): G4 spread {spread:.3e} < 1e-4. "
                         f"Not a verdict.")
    log(f"G4 pass: cosine spread = {spread:.6f} (>= 1e-4)")

    # ---- Phase 3: hash after extraction ----
    hash_mid = sha256_state_dict(model.state_dict())
    if hash_mid != hash_before:
        raise RunInvalid("RUN-INVALID: Δθ≠0 after extraction (pre/post hash mismatch). Quarantine.")
    log("mid-hash OK (Δθ=0)")

    # ---- Phase 4: self-report elicitation (pinned verbatim template) ----
    ASK = ("\n\nQuestion: Which option did you choose — A or C? "
           "Reply with a single letter and nothing else.")
    n_unparseable = 0
    for rec, item in zip(records, bench):
        prompt = item["prompt"] + ASK
        enc = tokenizer(prompt, return_tensors="pt")
        with torch.no_grad():
            gen = model.generate(
                enc["input_ids"], attention_mask=enc["attention_mask"],
                do_sample=False, max_new_tokens=4,
                pad_token_id=tokenizer.eos_token_id)
        new_ids = gen[0][enc["input_ids"].shape[1]:]
        gen_text = tokenizer.decode(new_ids, skip_special_tokens=True)
        stripped = gen_text.strip()
        first_alpha = next((ch for ch in stripped if ch.isalpha()), None)
        parsed = first_alpha.upper() if first_alpha else None
        self_report = parsed if parsed in ("A", "C") else None
        if self_report is None:
            n_unparseable += 1
        rec["self_report_prompt_tail"] = ASK
        rec["generated_text"] = gen_text
        rec["self_report"] = self_report  # None -> UNPARSEABLE
    log(f"elicitation complete: n_unparseable = {n_unparseable}/60")
    if n_unparseable >= 7:
        raise RunInvalid(f"RUN-INVALID (elicitation failure): n_unparseable={n_unparseable} >= 7. "
                         f"Not a verdict.")

    # ---- Phase 5: hash after generation ----
    hash_after = sha256_state_dict(model.state_dict())
    if hash_after != hash_before:
        raise RunInvalid("RUN-INVALID: Δθ≠0 after generation (pre/post hash mismatch). Quarantine.")
    log("post-hash OK (Δθ=0)")

    # ---- Phase 6: degenerate self-report channel gate ----
    valid_recs = [r for r in records if r["self_report"] is not None]
    n_valid = len(valid_recs)
    classes = sorted({r["self_report"] for r in valid_recs})
    counts = {c: sum(1 for r in valid_recs if r["self_report"] == c) for c in classes}
    minority = min(counts.values()) if counts else 0
    if len(classes) < 2 or minority < 3:
        raise RunInvalid(f"RUN-INVALID (degenerate self-report channel): classes={classes}, "
                         f"counts={counts}. StratifiedKFold(3) cannot execute. Not a verdict.")
    log(f"channel OK: classes={classes}, counts={counts}, n_valid={n_valid}")

    # ---- Phase 7: probe (L2 logistic, C=1.0, StratifiedKFold(3, shuffle, rs=0)) ----
    X = np.stack([state_embs[i] for i, r in enumerate(records) if r["self_report"] is not None])
    y = np.array([1 if r["self_report"] == "A" else 0 for r in valid_recs], dtype=int)
    decisions = [r["decision"] for r in valid_recs]
    oof = np.zeros(n_valid, dtype=int)
    skf = StratifiedKFold(n_splits=3, shuffle=True, random_state=0)
    for tr, te in skf.split(X, y):
        clf = LogisticRegression(penalty="l2", C=1.0)
        clf.fit(X[tr], y[tr])
        oof[te] = clf.predict(X[te])
    decoded = ["A" if p == 1 else "C" for p in oof]
    fidelity = float(np.mean([d == dec for d, dec in zip(decoded, decisions)]))
    bal_acc = float(balanced_accuracy_score(y, oof))
    for r, d in zip(valid_recs, decoded):
        r["decoded_self_report"] = d
    log(f"probe done: fidelity={fidelity:.4f} (n_valid={n_valid}), "
        f"balanced_accuracy={bal_acc:.4f}")

    # ---- Phase 8: decision bars (fractions of n_valid) ----
    observation = None
    if fidelity >= 0.98:
        verdict = "KILL"
        branch = "fidelity >= 59/60 (>=0.98): no gap to study"
    elif fidelity > 0.95:
        verdict = "HELD"
        branch = "fidelity in (0.95, 0.98): gap too small to instrument"
    elif fidelity >= 0.70:
        if bal_acc >= 0.70:
            verdict = "CONTINUE"
            branch = "fidelity in [0.70,0.95] AND decodability >= 0.70: real gap, instrumentable"
        else:
            verdict = "HELD"
            branch = "fidelity in [0.70,0.95] but decodability < 0.70: incoherent (pinned)"
    elif fidelity > 0.55:
        verdict = "HELD"
        branch = "fidelity in (0.55,0.70): weak signal, below decisive bar"
    else:
        verdict = "KILL"
        branch = "fidelity <= 0.55: no signal at this read site"
    if fidelity <= 23 / 60:
        observation = "systematic-misreporting signature"
        log("[OBSERVATION] systematic-misreporting signature recorded (verdict unchanged)")
    log(f"VERDICT: {verdict} — {branch}")

    # ---- outputs ----
    summary = {
        "experiment": "EXP108", "candidate": "H1/HDI",
        "prereg": "research/prereg/EXP_PREREG_H1_HDI_2026-09-29.md",
        "log_lane": "LOG-4546",
        "environment": {
            "torch": torch.__version__, "transformers": None, "sklearn": None,
            "device": "cpu", "dtype": "float32",
        },
        "backbone": {
            "snapshot": SNAPSHOT, "pin": PIN_BACKBONE,
            "hash_before": hash_before, "hash_mid": hash_mid, "hash_after": hash_after,
            "delta_theta_0": True,
        },
        "provenance": {"pin": PIN_PROVENANCE, "match": True},
        "bench": {"n": len(bench), "source": "benchmark_exp089.build_benchmark()"},
        "g4": {"spread": spread, "floor": G4_FLOOR, "pass": True,
               "margin_mean": float(np.mean(margins)), "margin_median": float(np.median(margins)),
               "margin_min": float(np.min(margins)), "margin_max": float(np.max(margins))},
        "elicitation": {"n_unparseable": n_unparseable, "gate_floor": 7, "pass": True},
        "channel": {"classes": classes, "counts": counts, "n_valid": n_valid},
        "ties_toward_C": n_ties,
        "probe": {"model": "LogisticRegression(penalty='l2', C=1.0)",
                  "cv": "StratifiedKFold(n_splits=3, shuffle=True, random_state=0)",
                  "read_site": "layer-20 final-token hidden state of premise-only state text"},
        "fidelity": fidelity, "balanced_accuracy": bal_acc,
        "verdict": verdict, "falsification_branch": branch,
        "observation": observation,
        "elapsed_s": round(time.time() - t0, 1),
    }
    import transformers as _tf, sklearn as _sk
    summary["environment"]["transformers"] = _tf.__version__
    summary["environment"]["sklearn"] = _sk.__version__

    with open(os.path.join(OUTDIR, "exp108_summary.json"), "w") as f:
        json.dump(summary, f, indent=2)
    with open(os.path.join(OUTDIR, "exp108_per_item.jsonl"), "w") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")
    with open(os.path.join(OUTDIR, "exp108_console.log"), "w") as f:
        f.write("\n".join(log_lines) + "\n")
    log(f"outputs written to {OUTDIR}")
    log(f"DONE in {time.time()-t0:.0f}s: fidelity={fidelity:.4f}, bal_acc={bal_acc:.4f}, "
        f"verdict={verdict}")
    return summary


if __name__ == "__main__":
    try:
        main()
    except RunInvalid as e:
        log(str(e))
        with open(os.path.join(OUTDIR, "exp108_console.log"), "w") as f:
            f.write("\n".join(log_lines) + "\n")
        print("RUN-INVALID — stopping. No metric read.", flush=True)
        sys.exit(42)
