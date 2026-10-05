"""EXP147 main run — S7-1: in-context writable memory (signed plan).

Arms: B (baseline, T=15) -> guard (d); then C (CoT, T=120), S (scratchpad,
T=120). Greedy decoding, frozen Pythia-410m, Δθ=0. Resumable: skips
(item, arm) pairs already in the JSONL. Per-item flush+fsync (EXP143 lesson).
$0 CPU.
"""
import hashlib
import json
import os
import re
import string
import sys
import time

RUN_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(RUN_DIR, "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO_ROOT, "experiments", "runs", "EXP092_ibl"))
from reference_implementation import bench_sha256  # noqa: E402

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_ID = "EleutherAI/pythia-410m"
REVISION = "9879c9b5f8bea9051dcb0e68dff21493d67e9d4f"
BACKBONE_PIN = "ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed"
BENCH_PIN = "2b055b53127a241b72338a82373c3efc7b666256e25d8c584d45989278c14dcf"

BENCH_PATH = os.path.expanduser(
    "~/workspace/SCBI/research/analysis_plans/S7-1_BENCH_2026-10-05.json")
PROMPTS_PATH = os.path.join(RUN_DIR, "S7-1_PROMPTS_2026-10-05.json")
JSONL = os.path.join(RUN_DIR, "exp147_per_item.jsonl")
RUNLOG = os.path.join(RUN_DIR, "exp147_run_2026-10-05.log")
SUMMARY = os.path.join(RUN_DIR, "exp147_run_summary_2026-10-05.json")

WRITE_RE = re.compile(r'WRITE\(fact\d+,')


def log(msg):
    line = "[run] %s" % msg
    print(line, flush=True)
    with open(RUNLOG, "a") as f:
        f.write(line + "\n")


def sha256_state_dict(model):
    h = hashlib.sha256()
    for k in sorted(model.state_dict().keys()):
        t = model.state_dict()[k].detach().cpu()
        if t.dtype != torch.float32:
            t = t.float()
        h.update(t.numpy().tobytes())
    return h.hexdigest()


def normalize(s):
    s = s.lower()
    s = s.translate(str.maketrans("", "", string.punctuation))
    return " ".join(s.split())


def score_generation(arm, generation, gold):
    """Registered scoring §5.3. Returns (correct, extracted)."""
    if arm in ("C", "S"):
        if "ANSWER:" not in generation:
            return 0, ""
        extracted = generation.rsplit("ANSWER:", 1)[1]
    else:
        extracted = generation
    return (1 if normalize(extracted) == normalize(gold) else 0), extracted.strip()


def build_prompt(prompts, arm, item):
    t = prompts["arms"][arm]["template"]
    shots = "".join(prompts["shots"][arm])
    facts = " ".join(item["facts"])
    return t.replace("{shots}", shots).replace("{facts}", facts).replace(
        "{question}", item["question"])


def load_done():
    done = set()
    if os.path.exists(JSONL):
        with open(JSONL) as f:
            for line in f:
                line = line.strip()
                if line:
                    r = json.loads(line)
                    done.add((r["item_id"], r["arm"]))
    return done


def main():
    t_start = time.time()
    torch.manual_seed(147002)
    log("loading model")
    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_ID, revision=REVISION, local_files_only=True,
        trust_remote_code=False)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID, revision=REVISION, local_files_only=True,
        torch_dtype=torch.float32, device_map="cpu",
        attn_implementation="eager", trust_remote_code=False)
    model.eval()
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token_id = tokenizer.eos_token_id

    pre_hash = sha256_state_dict(model)
    assert pre_hash == BACKBONE_PIN, f"(a) pre-hash mismatch: {pre_hash}"
    log("(a) pre-hash PASS")

    with open(BENCH_PATH) as f:
        bench = json.load(f)
    assert bench_sha256(bench) == BENCH_PIN, "(c) bench pin mismatch"
    log(f"(c) bench pin PASS ({len(bench)} items)")
    with open(PROMPTS_PATH) as f:
        prompts = json.load(f)

    # Law #7: exemplar entities disjoint from bench entities (re-assert)
    bench_ents = set()
    for it in bench:
        for f_ in it["facts"]:
            bench_ents.update(w.strip(string.punctuation) for w in f_.split())
    ex_ents = set(prompts["exemplar_entities"])
    assert not (bench_ents & ex_ents), "Law #7: exemplar/bench entity overlap"
    log("Law #7 exemplar/bench entity disjointness PASS")

    done = load_done()
    log(f"resuming: {len(done)} (item, arm) pairs already done")

    def run_arm(arm):
        budget = prompts["arms"][arm]["budget_tokens"]
        for it in bench:
            key = (it["id"], arm)
            if key in done:
                continue
            prompt = build_prompt(prompts, arm, it)
            inp = tokenizer(prompt, return_tensors="pt")
            with torch.no_grad():
                out = model.generate(
                    inp["input_ids"], max_new_tokens=budget,
                    do_sample=False, pad_token_id=tokenizer.eos_token_id)
            new_ids = out[0][inp["input_ids"].shape[1]:]
            generation = tokenizer.decode(new_ids, skip_special_tokens=True)
            correct, extracted = score_generation(arm, generation, it["gold"])
            rec = {
                "item_id": it["id"], "stratum": it["stratum"], "arm": arm,
                "gold": it["gold"], "generation": generation,
                "extracted": extracted, "correct": correct,
                "n_new_tokens": int(len(new_ids)),
                "n_prompt_tokens": int(inp["input_ids"].shape[1]),
            }
            with open(JSONL, "a") as f:
                f.write(json.dumps(rec) + "\n")
                f.flush()
                os.fsync(f.fileno())
            done.add(key)
        log(f"arm {arm} complete ({len(bench)} items)")

    # ---- arm B first (guard (d) calibration) ----
    run_arm("B")
    b_recs = [json.loads(l) for l in open(JSONL)
              if json.loads(l)["arm"] == "B"]
    b_acc = sum(r["correct"] for r in b_recs) / len(b_recs)
    log(f"guard (d): B accuracy = {b_acc:.4f} (bar [0.2, 0.8])")
    summary = {"b_accuracy": b_acc, "guards": {}}
    if not (0.2 <= b_acc <= 0.8):
        summary["guards"]["d_calibration"] = False
        summary["outcome"] = "HELD"
        summary["reason"] = f"guard (d): B accuracy {b_acc:.4f} outside [0.2,0.8]"
        post_hash = sha256_state_dict(model)
        summary["backbone_post_hash"] = post_hash
        summary["guards"]["a_posthash_match"] = (post_hash == BACKBONE_PIN)
        json.dump(summary, open(SUMMARY, "w"), indent=1)
        log(f"HELD: guard (d) — B accuracy {b_acc:.4f}")
        return
    summary["guards"]["d_calibration"] = True

    # ---- arms C and S ----
    run_arm("C")
    run_arm("S")

    # ---- guards (e), (f), (f'), (g) ----
    recs = [json.loads(l) for l in open(JSONL)]
    by_arm = {}
    for r in recs:
        by_arm.setdefault(r["arm"], []).append(r)
    mean_tok = {a: sum(r["n_new_tokens"] for r in rs) / len(rs)
                for a, rs in by_arm.items()}
    log(f"mean new tokens: { {a: round(v,1) for a,v in mean_tok.items()} }")

    # (e) discipline delivered
    s_write = sum(1 for r in by_arm["S"] if WRITE_RE.search(r["generation"]))
    e_rate = s_write / len(by_arm["S"])
    summary["guards"]["e_discipline_rate"] = round(e_rate, 4)
    summary["guards"]["e_discipline_pass"] = e_rate >= 0.5
    log(f"guard (e): WRITE-span rate = {e_rate:.4f} (bar >= 0.5)")

    # (f) compute delivered
    f_pass = (mean_tok["C"] > 2 * mean_tok["B"]
              and mean_tok["S"] > 2 * mean_tok["B"])
    summary["guards"]["f_compute_delivered"] = f_pass
    log(f"guard (f): C>2xB and S>2xB -> {f_pass}")

    # (f') budget-match comparability
    ratio = mean_tok["S"] / mean_tok["C"] if mean_tok["C"] > 0 else float("inf")
    fp_pass = (2/3) <= ratio <= (3/2)
    summary["mean_tokens"] = {a: round(v, 2) for a, v in mean_tok.items()}
    summary["token_ratio_S_C"] = round(ratio, 4)
    summary["guards"]["fp_comparability"] = fp_pass
    log(f"guard (f'): S/C token ratio = {ratio:.4f} (bar [0.667, 1.5]) -> {fp_pass}")

    # (g) budget audit
    total_gen = sum(r["n_new_tokens"] for r in recs)
    total_enc = sum(1 for _ in recs)  # one prompt-encoding forward per record
    summary["total_generation_forwards"] = total_gen
    summary["total_prompt_encodings"] = total_enc
    summary["guards"]["g_budget"] = total_gen <= 50000
    log(f"guard (g): {total_gen} generation forwards (cap 50000)")

    # (a) post-hash
    post_hash = sha256_state_dict(model)
    summary["backbone_post_hash"] = post_hash
    summary["guards"]["a_posthash_match"] = (post_hash == BACKBONE_PIN)
    log(f"(a) post-hash match: {summary['guards']['a_posthash_match']}")

    # B format-compliance descriptive report (advisory ii — not a guard)
    b_single = sum(1 for r in by_arm["B"]
                   if len(normalize(r["generation"]).split()) <= 2)
    summary["b_format_compliance"] = {
        "fraction_short": round(b_single / len(by_arm["B"]), 4),
        "mean_new_tokens": round(mean_tok["B"], 2),
    }

    summary["elapsed_hours"] = round((time.time() - t_start) / 3600, 2)
    json.dump(summary, open(SUMMARY, "w"), indent=1)

    # Verdict routing per §4 precedence
    if not summary["guards"]["e_discipline_pass"]:
        summary["outcome"] = "RUN-INVALID"
        summary["reason"] = "guard (e): discipline not delivered"
    elif not summary["guards"]["f_compute_delivered"]:
        summary["outcome"] = "RUN-INVALID"
        summary["reason"] = "guard (f): compute not delivered"
    elif not summary["guards"]["g_budget"]:
        summary["outcome"] = "RUN-INVALID"
        summary["reason"] = "guard (g): budget exceeded"
    elif not summary["guards"]["a_posthash_match"]:
        summary["outcome"] = "RUN-INVALID"
        summary["reason"] = "guard (a): post-hash mismatch"
    else:
        summary["outcome"] = "PROCEED_TO_VERDICT"
        if not fp_pass:
            summary["fp_note"] = ("guard (f') tripped -> HELD "
                                  "(attribution compromised)")
    json.dump(summary, open(SUMMARY, "w"), indent=1)
    log(f"run complete: outcome={summary['outcome']} "
        f"elapsed={summary['elapsed_hours']}h")


if __name__ == "__main__":
    main()
