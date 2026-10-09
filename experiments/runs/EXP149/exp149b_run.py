"""EXP149 study (b) full run — cross-family prompting-discipline generality, GPT-2-small.

Signed pre-reg EXP149_PREREG_DRAFT_2026-10-09.md (Law #14 SIGN-WITH-FIXES
repaired; CEO sign + execution authorization LOG-4968). (p1)-fail rebuild
branch taken: parent bench 0/180 single-token -> rebuilt GPT-2-BPE-safe bench
(pin a3e6f63229ae9cf727ce289abdcd890de48b97c98c0c828fe7ca87981eddd99e),
(p1) re-verified 180/180.

Arms: B (T=15), C/S (T=120) budget-matched. First-token scoring (§5.3).
Greedy, frozen GPT-2-small, Δθ=0. $0 CPU. Resumable JSONL.
"""
import hashlib
import json
import os
import random
import re
import string
import sys
import time

RUN_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(RUN_DIR, "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO_ROOT, "experiments", "runs", "EXP092_ibl"))
from reference_implementation import bench_sha256  # noqa: E402

VENV_PY = os.path.expanduser("~/workspace/.exp149-venv/bin/python")
if sys.executable != VENV_PY and "torch" not in sys.modules:
    pass  # run under the venv python

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_ID = "gpt2"
CACHE_DIR = os.path.expanduser(
    "~/workspace/SCBI/experiments/runs/EXP145/hf_cache")
REVISION = "607a30d783dfa663caf39e06633721c8d4cfcd7e"
BENCH_PIN = "a3e6f63229ae9cf727ce289abdcd890de48b97c98c0c828fe7ca87981eddd99e"

BENCH_PATH = os.path.join(RUN_DIR, "EXP149B_BENCH_2026-10-09.json")
PROMPTS_PATH = os.path.expanduser(
    "~/workspace/SCBI/experiments/runs/EXP147/S7-1_PROMPTS_2026-10-05.json")
JSONL = os.path.join(RUN_DIR, "exp149b_per_item.jsonl")
RUNLOG = os.path.join(RUN_DIR, "exp149b_run.log")
SUMMARY = os.path.join(RUN_DIR, "exp149b_run_summary.json")
PILOT_STATE = os.path.join(RUN_DIR, "exp149b_pilot_state.json")

TORCH_SEED = 149007  # registered at execution
B_PILOT_SEED = 149005  # (p2) 20-item B subset
S_PILOT_SEED = 149006  # (p3) 20-item S subset
WRITE_RE = re.compile(r'WRITE\(fact\d+,')
ANSWER_RE = re.compile(r"answer:", re.IGNORECASE)


def log(msg):
    line = "[run-b] %s" % msg
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
    toks = normalize(generation).split()
    first = toks[0] if toks else ""
    return (1 if first == normalize(gold) else 0), first


def score_cs(generation, gold):
    matches = list(ANSWER_RE.finditer(generation))
    if not matches:
        return 0, ""
    after = generation[matches[-1].end():]
    toks = normalize(after).split()
    first = toks[0] if toks else ""
    return (1 if first == normalize(gold) else 0), first


def unit_test_u0():
    cases = [
        (score_cs, "Some reasoning here. ANSWER: dog", "dog", 1, "dog",
         "cs-a standard ANSWER:"),
        (score_cs, "Some reasoning. answer: cat", "cat", 1, "cat",
         "cs-b lowercase answer:"),
        (score_cs, "First ANSWER: wrong. Second ANSWER: bird", "bird", 1,
         "bird", "cs-c multiple markers last-wins"),
        (score_cs, "Reasoning. ANSWER: fish and then it swam", "fish", 1,
         "fish", "cs-d trailing ramble"),
        (score_cs, "Just some text without any marker", "horse", 0, "",
         "cs-e missing marker -> 0"),
        (score_cs, "ANSWER: cow", "pig", 0, "cow",
         "cs-f wrong name -> 0"),
        (score_b, "dog went to the barn", "dog", 1, "dog",
         "b-a first token match"),
        (score_b, "The answer is cat", "cat", 0, "the",
         "b-b first token mismatch"),
        (score_b, "", "bird", 0, "", "b-c empty generation -> 0"),
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


def fresh_subset(bench, k, seed):
    rng = random.Random(seed)
    idx = rng.sample(range(len(bench)), k)
    return [bench[i] for i in idx]


def main():
    t_start = time.time()
    torch.manual_seed(TORCH_SEED)
    summary = {"experiment": "EXP149", "study": "b",
               "log": "LOG-4968", "torch_seed": TORCH_SEED, "guards": {}}

    # ---- (u0) zero-forward scoring unit test ----
    failures = unit_test_u0()
    summary["guards"]["u0_scoring_pipeline"] = (len(failures) == 0)
    log(f"(u0) unit test: {9 - len(failures)}/9 pass")
    if failures:
        summary["outcome"] = "RUN-INVALID"
        json.dump(summary, open(SUMMARY, "w"), indent=1)
        sys.exit(2)
    log("(u0) PASS")

    # ---- (b) model revision from local cache ----
    snap_dir = os.path.join(CACHE_DIR, "models--gpt2", "snapshots")
    revs = sorted(os.listdir(snap_dir))
    assert len(revs) == 1, f"expected 1 cached snapshot, got {revs}"
    actual_rev = revs[0]
    summary["guards"]["b_revision_match"] = (actual_rev == REVISION)
    log(f"(b) revision actual={actual_rev} match={summary['guards']['b_revision_match']}")
    if not summary["guards"]["b_revision_match"]:
        summary["outcome"] = "RUN-INVALID"
        json.dump(summary, open(SUMMARY, "w"), indent=1)
        sys.exit(2)

    # ---- load ----
    os.environ.setdefault("HF_HUB_OFFLINE", "1")
    os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
    log("loading GPT-2 tokenizer + model (eager, fp32, cpu, local_files_only)")
    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_ID, revision=actual_rev, local_files_only=True,
        trust_remote_code=False, cache_dir=CACHE_DIR)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID, revision=actual_rev, local_files_only=True,
        torch_dtype=torch.float32, device_map="cpu",
        attn_implementation="eager", trust_remote_code=False,
        cache_dir=CACHE_DIR)
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
    summary["pre_hash"] = pre_hash
    log(f"(a) pre-hash recorded: {pre_hash[:16]}...")

    # ---- (c) bench pin (rebuilt bench) ----
    with open(BENCH_PATH) as f:
        bench = json.load(f)
    pin = bench_sha256(bench)
    char_match = len(pin) == 64 and all(a == b for a, b in zip(pin, BENCH_PIN))
    summary["guards"]["c_bench_pin_match"] = (pin == BENCH_PIN and char_match)
    summary["bench_pin"] = pin
    log(f"(c) bench pin match: {summary['guards']['c_bench_pin_match']} "
        f"({len(bench)} items)")
    assert summary["guards"]["c_bench_pin_match"], "(c) bench pin mismatch"

    # ---- exemplars byte-identical; Law #7 ----
    assert os.path.exists(PROMPTS_PATH), f"prompts missing: {PROMPTS_PATH}"
    summary["prompts_sha256"] = sha256_file(PROMPTS_PATH)
    with open(PROMPTS_PATH) as f:
        prompts = json.load(f)
    bench_ents = set()
    for it in bench:
        for f_ in it["facts"]:
            bench_ents.update(w.strip(string.punctuation) for w in f_.split())
    ex_ents = set(prompts["exemplar_entities"])
    summary["guards"]["law7_disjoint"] = not (bench_ents & ex_ents)
    log(f"Law #7 disjointness: {summary['guards']['law7_disjoint']}")
    assert summary["guards"]["law7_disjoint"], "Law #7 overlap"

    def gen(item, arm):
        prompt = build_prompt(prompts, arm, item)
        inp = tokenizer(prompt, return_tensors="pt")
        with torch.no_grad():
            out = model.generate(
                inp["input_ids"],
                max_new_tokens=prompts["arms"][arm]["budget_tokens"],
                do_sample=False, pad_token_id=tokenizer.eos_token_id)
        new_ids = out[0][inp["input_ids"].shape[1]:]
        generation = tokenizer.decode(new_ids, skip_special_tokens=True)
        return generation, int(len(new_ids))

    # ---- (p2) calibration portability: B arm, fresh 20-item subset ----
    # (pilot results persist in PILOT_STATE so a relaunch resumes, not re-runs)
    pilot_state = {}
    if os.path.exists(PILOT_STATE):
        with open(PILOT_STATE) as f:
            pilot_state = json.load(f)
    if "p2" in pilot_state:
        p2_acc = pilot_state["p2"]["acc"]
        p2_tok = pilot_state["p2"]["tok"]
        log(f"(p2) resumed from pilot state: acc={p2_acc:.4f}")
    else:
        p2_items = fresh_subset(bench, 20, B_PILOT_SEED)
        p2_corr = 0
        p2_tok = 0
        for it in p2_items:
            generation, n_new = gen(it, "B")
            c, _ = score_b(generation, it["gold"])
            p2_corr += c
            p2_tok += n_new
        p2_acc = p2_corr / 20
        pilot_state["p2"] = {"acc": p2_acc, "tok": p2_tok,
                             "seed": B_PILOT_SEED}
        with open(PILOT_STATE, "w") as f:
            json.dump(pilot_state, f, indent=1)
    summary["guards"]["p2_calibration"] = round(p2_acc, 4)
    summary["guards"]["p2_pass"] = (0.2 <= p2_acc <= 0.8)
    log(f"(p2) B accuracy on 20-item subset = {p2_acc:.4f} (bar [0.2,0.8]) "
        f"-> {'PASS' if summary['guards']['p2_pass'] else 'STOP/HELD'}")

    # ---- (p3) delivery portability: S arm, fresh 20-item pilot ----
    if "p3" in pilot_state:
        p3_rate = pilot_state["p3"]["rate"]
        p3_tok = pilot_state["p3"]["tok"]
        log(f"(p3) resumed from pilot state: rate={p3_rate:.4f}")
    else:
        p3_items = fresh_subset(bench, 20, S_PILOT_SEED)
        p3_write = 0
        p3_tok = 0
        for it in p3_items:
            generation, n_new = gen(it, "S")
            if WRITE_RE.search(generation):
                p3_write += 1
            p3_tok += n_new
        p3_rate = p3_write / 20
        pilot_state["p3"] = {"rate": p3_rate, "tok": p3_tok,
                             "seed": S_PILOT_SEED}
        with open(PILOT_STATE, "w") as f:
            json.dump(pilot_state, f, indent=1)
    summary["guards"]["p3_delivery"] = round(p3_rate, 4)
    summary["guards"]["p3_pass"] = p3_rate >= 0.50
    log(f"(p3) WRITE-span rate on 20-item S pilot = {p3_rate:.4f} (bar >= 0.50) "
        f"-> {'PASS' if summary['guards']['p3_pass'] else 'STOP/HELD'}")
    summary["portability_pilot_forwards"] = p2_tok + p3_tok
    log(f"portability pilot forwards: {p2_tok + p3_tok} (design ~2,700)")

    if not (summary["guards"]["p2_pass"] and summary["guards"]["p3_pass"]):
        summary["outcome"] = "HELD"
        summary["reason"] = ("portability gate trip "
                             f"(p2={summary['guards']['p2_pass']}, "
                             f"p3={summary['guards']['p3_pass']}) — measurement "
                             "boundary, licenses nothing, kills nothing (Law #4)")
        post_hash = sha256_state_dict(model)
        summary["guards"]["a_posthash_match"] = (post_hash == pre_hash)
        summary["elapsed_hours"] = round((time.time() - t_start) / 3600, 2)
        json.dump(summary, open(SUMMARY, "w"), indent=1)
        log("HELD: portability gate — STOP at design cost")
        return

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
            generation, n_tok = gen(it, arm)
            correct, first_tok = scorer(generation, it["gold"])
            n_new += n_tok
            rec = {
                "item_id": it["id"], "stratum": it["stratum"], "arm": arm,
                "gold": it["gold"], "generation": generation,
                "first_token": first_tok, "correct": correct,
                "n_new_tokens": n_tok,
            }
            with open(JSONL, "a") as f:
                f.write(json.dumps(rec) + "\n")
                f.flush()
                os.fsync(f.fileno())
            done.add(key)
        log(f"arm {arm} complete ({len(bench)} items)")
        return n_new

    run_arm("B")
    b_recs = [json.loads(l) for l in open(JSONL)
              if json.loads(l)["arm"] == "B"]
    assert len(b_recs) == 180, f"B arm incomplete: {len(b_recs)}/180"
    b_acc = sum(r["correct"] for r in b_recs) / len(b_recs)
    summary["b_first_token_accuracy"] = round(b_acc, 4)
    summary["guards"]["d_calibration"] = (0.2 <= b_acc <= 0.8)
    log(f"guard (d): B accuracy = {b_acc:.4f} (bar [0.2,0.8]) pooled")
    if not summary["guards"]["d_calibration"]:
        summary["outcome"] = "HELD"
        summary["reason"] = f"guard (d): B accuracy {b_acc:.4f} outside [0.2,0.8]"
        post_hash = sha256_state_dict(model)
        summary["guards"]["a_posthash_match"] = (post_hash == pre_hash)
        summary["elapsed_hours"] = round((time.time() - t_start) / 3600, 2)
        json.dump(summary, open(SUMMARY, "w"), indent=1)
        log("HELD: guard (d)")
        return

    run_arm("C")
    run_arm("S")

    recs = [json.loads(l) for l in open(JSONL)]
    by_arm = {}
    for r in recs:
        by_arm.setdefault(r["arm"], []).append(r)
    for a in ("B", "C", "S"):
        assert len(by_arm.get(a, [])) == 180, f"arm {a} incomplete"
    mean_tok = {a: sum(r["n_new_tokens"] for r in rs) / len(rs)
                for a, rs in by_arm.items()}
    summary["mean_tokens"] = {a: round(v, 2) for a, v in mean_tok.items()}

    s_write = sum(1 for r in by_arm["S"] if WRITE_RE.search(r["generation"]))
    e_rate = s_write / len(by_arm["S"])
    summary["guards"]["e_discipline_rate"] = round(e_rate, 4)
    summary["guards"]["e_discipline_pass"] = e_rate >= 0.5

    f_pass = (mean_tok["C"] > 2 * mean_tok["B"]
              and mean_tok["S"] > 2 * mean_tok["B"])
    summary["guards"]["f_compute_delivered"] = f_pass
    ratio = mean_tok["S"] / mean_tok["C"] if mean_tok["C"] > 0 else float("inf")
    fp_pass = (2 / 3) <= ratio <= (3 / 2)
    summary["token_ratio_S_C"] = round(ratio, 4)
    summary["guards"]["fp_comparability"] = fp_pass

    total_gen = sum(r["n_new_tokens"] for r in recs) + p2_tok + p3_tok
    summary["total_generation_forwards"] = total_gen
    summary["guards"]["g_budget"] = total_gen <= 50000
    log(f"guard (g): {total_gen} forwards (cap 50000, incl. portability pilots)")

    post_hash = sha256_state_dict(model)
    summary["guards"]["a_posthash_match"] = (post_hash == pre_hash)
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
        summary["reason"] = "guard (a): Δθ≠0 (post-hash mismatch)"
    else:
        summary["outcome"] = "PROCEED_TO_VERDICT"
        if not fp_pass:
            summary["fp_note"] = "guard (f') tripped -> HELD (attribution compromised)"
    json.dump(summary, open(SUMMARY, "w"), indent=1)
    log(f"run complete: outcome={summary['outcome']} "
        f"elapsed={summary['elapsed_hours']}h forwards={total_gen}")


if __name__ == "__main__":
    main()
