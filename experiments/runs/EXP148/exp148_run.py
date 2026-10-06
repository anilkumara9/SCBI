"""EXP148 full run — J7: WRITE/READ prompting discipline vs budget-matched CoT
(signed pre-reg EXP148_PREREG_2026-10-06.md, verification SIGN LOG-4956,
Step-0 dry-run PASS LOG-4957, CEO execution authorization).

Arms: B (baseline, T=15) -> guard (d) on FIRST-TOKEN accuracy; then C (CoT,
T=120), S (scratchpad, T=120). First-token scoring (§5.3): B = first normalized
token vs gold; C/S = first normalized token after LAST ANSWER: vs gold.
Greedy decoding, frozen Pythia-410m, Δθ=0. Resumable: skips (item, arm) pairs
already in the JSONL. Per-item flush+fsync. $0 CPU. ~46k generation forwards.
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
PROMPTS_PATH = os.path.expanduser(
    "~/workspace/SCBI/experiments/runs/EXP147/S7-1_PROMPTS_2026-10-05.json")
JSONL = os.path.join(RUN_DIR, "exp148_per_item.jsonl")
RUNLOG = os.path.join(RUN_DIR, "exp148_run_2026-10-06.log")
SUMMARY = os.path.join(RUN_DIR, "exp148_run_summary_2026-10-06.json")

TORCH_SEED = 148002  # registered at execution; distinct from dry-run 148001
WRITE_RE = re.compile(r'WRITE\(fact\d+,')
ANSWER_RE = re.compile(r"answer:", re.IGNORECASE)


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


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def normalize(s):
    s = s.lower()
    s = s.translate(str.maketrans("", "", string.punctuation))
    return " ".join(s.split())


def score_b(generation, gold):
    """First-token scoring, B arm (pre-reg §5.3.1)."""
    toks = normalize(generation).split()
    first = toks[0] if toks else ""
    return (1 if first == normalize(gold) else 0), first


def score_cs(generation, gold):
    """First-token scoring, C/S arms (pre-reg §5.3.2): first token after LAST answer marker."""
    matches = list(ANSWER_RE.finditer(generation))
    if not matches:
        return 0, ""
    after = generation[matches[-1].end():]
    toks = normalize(after).split()
    first = toks[0] if toks else ""
    return (1 if first == normalize(gold) else 0), first


def unit_test_u0():
    """(u0) zero-forward scoring-pipeline unit test — 9 synthetic cases."""
    cases = [
        (score_cs, "Some reasoning here. ANSWER: Alice", "Alice", 1, "alice",
         "cs-a standard ANSWER:"),
        (score_cs, "Some reasoning. answer: Bob", "Bob", 1, "bob",
         "cs-b lowercase answer:"),
        (score_cs, "First ANSWER: wrong. Second ANSWER: Carol", "Carol", 1,
         "carol", "cs-c multiple markers last-wins"),
        (score_cs, "Reasoning. ANSWER: Dave and then he went home", "Dave", 1,
         "dave", "cs-d trailing ramble"),
        (score_cs, "Just some text without any marker", "Eve", 0, "",
         "cs-e missing marker -> 0"),
        (score_cs, "ANSWER: Frank", "Grace", 0, "frank",
         "cs-f wrong name -> 0"),
        (score_b, "Alice went to the store", "Alice", 1, "alice",
         "b-a first token match"),
        (score_b, "The answer is Alice", "Alice", 0, "the",
         "b-b first token mismatch"),
        (score_b, "", "Alice", 0, "", "b-c empty generation -> 0"),
    ]
    failures = []
    for fn, gen, gold, exp_c, exp_f, label in cases:
        got_c, got_f = fn(gen, gold)
        if (got_c, got_f) != (exp_c, exp_f):
            failures.append({"case": label, "expected": (exp_c, exp_f),
                             "got": (got_c, got_f)})
    return failures


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
    torch.manual_seed(TORCH_SEED)
    summary = {"experiment": "EXP148", "log": "LOG-4958",
               "torch_seed": TORCH_SEED, "guards": {}}

    # ---- (u0) scoring-pipeline unit test: ZERO forwards ----
    failures = unit_test_u0()
    summary["guards"]["u0_scoring_pipeline"] = (len(failures) == 0)
    log(f"(u0) unit test: {9 - len(failures)}/9 cases pass")
    if failures:
        summary["outcome"] = "RUN-INVALID"
        summary["reason"] = "guard (u0): scoring-pipeline unit test failed"
        json.dump(summary, open(SUMMARY, "w"), indent=1)
        log("RUN-INVALID: guard (u0) — STOP")
        sys.exit(2)
    log("(u0) PASS")

    # ---- (b) model revision ----
    snap_dir = os.path.expanduser(
        "~/.cache/huggingface/hub/models--EleutherAI--pythia-410m/snapshots")
    revs = sorted(os.listdir(snap_dir))
    assert len(revs) == 1, f"expected 1 cached snapshot, got {revs}"
    actual_rev = revs[0]
    summary["guards"]["b_revision_match"] = (actual_rev == REVISION)
    log(f"(b) revision actual={actual_rev} match={summary['guards']['b_revision_match']}")
    if not summary["guards"]["b_revision_match"]:
        summary["outcome"] = "RUN-INVALID"
        summary["reason"] = "guard (b): revision mismatch"
        json.dump(summary, open(SUMMARY, "w"), indent=1)
        sys.exit(2)

    # ---- load ----
    log("loading tokenizer + model (eager, fp32, cpu)")
    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_ID, revision=actual_rev, local_files_only=True,
        trust_remote_code=False)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID, revision=actual_rev, local_files_only=True,
        torch_dtype=torch.float32, device_map="cpu",
        attn_implementation="eager", trust_remote_code=False)
    model.eval()
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token_id = tokenizer.eos_token_id
    import transformers as _tf
    import numpy as _np
    summary["env"] = {"torch": torch.__version__,
                      "transformers": _tf.__version__,
                      "numpy": _np.__version__,
                      "threads": torch.get_num_threads()}

    # ---- (a) pre-hash ----
    pre_hash = sha256_state_dict(model)
    summary["guards"]["a_prehash_match"] = (pre_hash == BACKBONE_PIN)
    log(f"(a) pre-hash match: {summary['guards']['a_prehash_match']}")
    assert summary["guards"]["a_prehash_match"], "(a) pre-hash mismatch"

    # ---- (c) bench pin ----
    with open(BENCH_PATH) as f:
        bench = json.load(f)
    pin = bench_sha256(bench)
    char_match = len(pin) == 64 and all(a == b for a, b in zip(pin, BENCH_PIN))
    summary["guards"]["c_bench_pin_match"] = (pin == BENCH_PIN and char_match)
    log(f"(c) bench pin match: {summary['guards']['c_bench_pin_match']} "
        f"({len(bench)} items)")
    assert summary["guards"]["c_bench_pin_match"], "(c) bench pin mismatch"

    # ---- exemplars: EXP147 file byte-identical ----
    assert os.path.exists(PROMPTS_PATH), f"prompts missing: {PROMPTS_PATH}"
    summary["prompts_sha256"] = sha256_file(PROMPTS_PATH)
    with open(PROMPTS_PATH) as f:
        prompts = json.load(f)
    log(f"exemplars reused byte-identical (sha256={summary['prompts_sha256'][:16]}...)")

    # Law #7
    bench_ents = set()
    for it in bench:
        for f_ in it["facts"]:
            bench_ents.update(w.strip(string.punctuation) for w in f_.split())
    ex_ents = set(prompts["exemplar_entities"])
    summary["guards"]["law7_disjoint"] = not (bench_ents & ex_ents)
    log(f"Law #7 disjointness: {summary['guards']['law7_disjoint']}")
    assert summary["guards"]["law7_disjoint"], "Law #7 overlap"

    done = load_done()
    log(f"resuming: {len(done)} (item, arm) pairs already done")

    def run_arm(arm):
        budget = prompts["arms"][arm]["budget_tokens"]
        scorer = score_b if arm == "B" else score_cs
        n_new = 0
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
            correct, first_tok = scorer(generation, it["gold"])
            n_new += int(len(new_ids))
            rec = {
                "item_id": it["id"], "stratum": it["stratum"], "arm": arm,
                "gold": it["gold"], "generation": generation,
                "first_token": first_tok, "correct": correct,
                "n_new_tokens": int(len(new_ids)),
                "n_prompt_tokens": int(inp["input_ids"].shape[1]),
            }
            with open(JSONL, "a") as f:
                f.write(json.dumps(rec) + "\n")
                f.flush()
                os.fsync(f.fileno())
            done.add(key)
        log(f"arm {arm} complete ({len(bench)} items, ~{n_new} new tokens this session)")
        return n_new

    # ---- arm B first (guard (d) on FIRST-TOKEN accuracy) ----
    run_arm("B")
    b_recs = [json.loads(l) for l in open(JSONL)
              if json.loads(l)["arm"] == "B"]
    assert len(b_recs) == 180, f"B arm incomplete: {len(b_recs)}/180"
    b_acc = sum(r["correct"] for r in b_recs) / len(b_recs)
    summary["b_first_token_accuracy"] = round(b_acc, 4)
    summary["guards"]["d_calibration"] = (0.2 <= b_acc <= 0.8)
    log(f"guard (d): B first-token accuracy = {b_acc:.4f} (bar [0.2, 0.8])")
    if not summary["guards"]["d_calibration"]:
        summary["outcome"] = "HELD"
        summary["reason"] = f"guard (d): B accuracy {b_acc:.4f} outside [0.2,0.8]"
        post_hash = sha256_state_dict(model)
        summary["guards"]["a_posthash_match"] = (post_hash == BACKBONE_PIN)
        json.dump(summary, open(SUMMARY, "w"), indent=1)
        log(f"HELD: guard (d)")
        return

    # ---- arms C and S ----
    run_arm("C")
    run_arm("S")

    # ---- guards (e), (f), (f'), (g) ----
    recs = [json.loads(l) for l in open(JSONL)]
    by_arm = {}
    for r in recs:
        by_arm.setdefault(r["arm"], []).append(r)
    for a in ("B", "C", "S"):
        assert len(by_arm.get(a, [])) == 180, f"arm {a} incomplete"
    mean_tok = {a: sum(r["n_new_tokens"] for r in rs) / len(rs)
                for a, rs in by_arm.items()}
    summary["mean_tokens"] = {a: round(v, 2) for a, v in mean_tok.items()}
    log(f"mean new tokens: {summary['mean_tokens']}")

    s_write = sum(1 for r in by_arm["S"] if WRITE_RE.search(r["generation"]))
    e_rate = s_write / len(by_arm["S"])
    summary["guards"]["e_discipline_rate"] = round(e_rate, 4)
    summary["guards"]["e_discipline_pass"] = e_rate >= 0.5
    log(f"guard (e): WRITE-span rate = {e_rate:.4f} (bar >= 0.5)")

    f_pass = (mean_tok["C"] > 2 * mean_tok["B"]
              and mean_tok["S"] > 2 * mean_tok["B"])
    summary["guards"]["f_compute_delivered"] = f_pass
    log(f"guard (f): C>2xB and S>2xB -> {f_pass}")

    ratio = mean_tok["S"] / mean_tok["C"] if mean_tok["C"] > 0 else float("inf")
    fp_pass = (2 / 3) <= ratio <= (3 / 2)
    summary["token_ratio_S_C"] = round(ratio, 4)
    summary["guards"]["fp_comparability"] = fp_pass
    log(f"guard (f'): S/C token ratio = {ratio:.4f} (bar [0.667, 1.5]) -> {fp_pass}")

    total_gen = sum(r["n_new_tokens"] for r in recs)
    total_enc = len(recs)
    summary["total_generation_forwards"] = total_gen
    summary["total_prompt_encodings"] = total_enc
    summary["guards"]["g_budget"] = total_gen <= 50000
    log(f"guard (g): {total_gen} generation forwards (cap 50000)")

    post_hash = sha256_state_dict(model)
    summary["guards"]["a_posthash_match"] = (post_hash == BACKBONE_PIN)
    log(f"(a) post-hash match: {summary['guards']['a_posthash_match']}")

    # B format-compliance descriptive (not a guard)
    b_single = sum(1 for r in by_arm["B"]
                   if len(normalize(r["generation"]).split()) <= 2)
    summary["b_format_compliance"] = {
        "fraction_short": round(b_single / len(by_arm["B"]), 4),
        "mean_new_tokens": round(mean_tok["B"], 2),
    }
    # per-stratum B accuracy (descriptive)
    from collections import defaultdict
    strat = defaultdict(lambda: [0, 0])
    for r in by_arm["B"]:
        strat[r["stratum"]][1] += 1
        strat[r["stratum"]][0] += r["correct"]
    summary["b_stratum_accuracy"] = {
        k: round(v[0] / v[1], 4) for k, v in sorted(strat.items())}

    summary["elapsed_hours"] = round((time.time() - t_start) / 3600, 2)
    json.dump(summary, open(SUMMARY, "w"), indent=1)

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
            summary["fp_note"] = "guard (f') tripped -> HELD (attribution compromised)"
    json.dump(summary, open(SUMMARY, "w"), indent=1)
    log(f"run complete: outcome={summary['outcome']} "
        f"elapsed={summary['elapsed_hours']}h forwards={total_gen}")


if __name__ == "__main__":
    main()
