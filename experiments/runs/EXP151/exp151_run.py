"""EXP151 full run — transitive-only hop dose-response on frozen Pythia-410m.

Signed pre-reg EXP151_PREREG_DRAFT_2026-10-09.md (Law #14 SIGN-WITH-FIXES
repaired; CEO sign + execution authorization LOG-4982). Fresh transitive-only
bench (EXP151_BENCH_2026-10-09.json, pin
643622d5a4c79675a764ef25098fff4f10a46a849c142206e78bbf7c1f80bd17) —
the hardened-compositional secondary was NOT built (registered fallback:
(v2)-literal fails on Pythia BPE for all 40 closed-pool entities while (v4)
pins the pool; jointly unsatisfiable — see bench manifest).

Sequence: (u0) -> (b) revision -> load -> (a) pre-hash -> (c) bench pin ->
Law #7/exemplars -> (h) throughput probe -> stratified dry-run (d-T2)/(d-T3)
-> C+S pilot -> registered power rule (bench-size STOP/HELD) -> full run
(B all, then C+S with d_block1 keying after each level's first 20 C+S) ->
guards (e)/(f)/(f')/(g) + (a) post-hash -> PROCEED_TO_VERDICT
(exp151_verdict.py fills the §4 table).

Greedy, Δθ=0, $0 CPU. Resumable JSONL. No n-raise (superseded, Fix E3).
No 4-hop (not re-registered).
"""
import hashlib
import json
import math
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

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_ID = "EleutherAI/pythia-410m"
CACHE_DIR = os.path.expanduser("~/.cache/huggingface")
REVISION = "9879c9b5f8bea9051dcb0e68dff21493d67e9d4f"
BACKBONE_PIN = "ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed"
BENCH_PIN = "643622d5a4c79675a764ef25098fff4f10a46a849c142206e78bbf7c1f80bd17"

BENCH_PATH = os.path.join(RUN_DIR, "EXP151_BENCH_2026-10-09.json")
PROMPTS_PATH = os.path.expanduser(
    "~/workspace/SCBI/experiments/runs/EXP147/S7-1_PROMPTS_2026-10-05.json")
JSONL = os.path.join(RUN_DIR, "exp151_per_item.jsonl")
STEP0_JSONL = os.path.join(RUN_DIR, "exp151_step0_records.jsonl")
RUNLOG = os.path.join(RUN_DIR, "exp151_run.log")
SUMMARY = os.path.join(RUN_DIR, "exp151_run_summary.json")

TORCH_SEED = 151031  # registered at execution
DRYRUN_SEEDS = {"transitive-2hop": 151012,   # ≠ construction 151001,
                "transitive-3hop": 151012}   # ≠ each other
PILOT_SEED = 151023  # C+S pilot, ≠ construction, ≠ dry-run seeds

LEVELS = ["transitive-2hop", "transitive-3hop"]
N_PER_LEVEL = 380
WRITE_RE = re.compile(r'WRITE\(fact\d+,')
ANSWER_RE = re.compile(r"answer:", re.IGNORECASE)


def log(msg):
    line = "[run-151] %s" % msg
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
        (score_cs, "Some reasoning here. ANSWER: Zorp", "Zorp", 1, "zorp",
         "cs-a standard ANSWER:"),
        (score_cs, "Some reasoning. answer: Blip", "Blip", 1, "blip",
         "cs-b lowercase answer:"),
        (score_cs, "First ANSWER: wrong. Second ANSWER: Fweep", "Fweep", 1,
         "fweep", "cs-c multiple markers last-wins"),
        (score_cs, "Reasoning. ANSWER: Quix and then more", "Quix", 1,
         "quix", "cs-d trailing ramble"),
        (score_cs, "Just some text without any marker", "Vorn", 0, "",
         "cs-e missing marker -> 0"),
        (score_cs, "ANSWER: Jalp", "Trun", 0, "jalp",
         "cs-f wrong name -> 0"),
        (score_b, "Zorp went home", "Zorp", 1, "zorp",
         "b-a first token match"),
        (score_b, "The answer is Blip", "Blip", 0, "the",
         "b-b first token mismatch"),
        (score_b, "", "Fweep", 0, "", "b-c empty generation -> 0"),
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


def fresh_subset(items, k, seed):
    rng = random.Random(seed)
    idx = rng.sample(range(len(items)), k)
    return [items[i] for i in idx]


def wald_power(d, n):
    """Registered Wald-formula power for δ=+0.10, one-sided α=0.05."""
    se = math.sqrt(max(d - 0.01, 1e-9) * (2.0 / n))
    z = 0.10 / se - 1.645
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0))), se


def dump_summary(summary):
    with open(SUMMARY, "w") as f:
        json.dump(summary, f, indent=1)
        f.write("\n")


def main():
    t_start = time.time()
    torch.manual_seed(TORCH_SEED)
    summary = {"experiment": "EXP151", "log": "LOG-4982",
               "torch_seed": TORCH_SEED, "guards": {},
               "dryrun_seeds": DRYRUN_SEEDS, "pilot_seed": PILOT_SEED,
               "bench": "transitive-only (hardened secondary NOT built; "
                        "registered fallback — see manifest)"}

    # ---- (u0) ----
    failures = unit_test_u0()
    summary["guards"]["u0_scoring_pipeline"] = (len(failures) == 0)
    log(f"(u0) unit test: {9 - len(failures)}/9 pass")
    if failures:
        summary["outcome"] = "RUN-INVALID"
        dump_summary(summary)
        sys.exit(2)
    log("(u0) PASS")

    # ---- (b) revision ----
    snap_dir = os.path.join(CACHE_DIR, "hub",
                            "models--EleutherAI--pythia-410m", "snapshots")
    revs = sorted(os.listdir(snap_dir))
    assert len(revs) == 1, f"expected 1 cached snapshot, got {revs}"
    actual_rev = revs[0]
    summary["guards"]["b_revision_match"] = (actual_rev == REVISION)
    log(f"(b) revision match: {summary['guards']['b_revision_match']}")
    if not summary["guards"]["b_revision_match"]:
        summary["outcome"] = "RUN-INVALID"
        dump_summary(summary)
        sys.exit(2)

    # ---- load ----
    SNAPSHOT_PATH = os.path.join(
        CACHE_DIR, "hub", "models--EleutherAI--pythia-410m", "snapshots",
        actual_rev)
    os.environ.setdefault("HF_HUB_OFFLINE", "1")
    os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
    log("loading Pythia-410m tokenizer + model (eager, fp32, cpu, local snapshot)")
    tokenizer = AutoTokenizer.from_pretrained(
        SNAPSHOT_PATH, local_files_only=True, trust_remote_code=False)
    model = AutoModelForCausalLM.from_pretrained(
        SNAPSHOT_PATH, local_files_only=True,
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

    def gen(item, arm, budget=None):
        b = budget if budget is not None else prompts["arms"][arm]["budget_tokens"]
        prompt = build_prompt(prompts, arm, item)
        inp = tokenizer(prompt, return_tensors="pt")
        with torch.no_grad():
            out = model.generate(
                inp["input_ids"], max_new_tokens=b,
                do_sample=False, pad_token_id=tokenizer.eos_token_id)
        new_ids = out[0][inp["input_ids"].shape[1]:]
        generation = tokenizer.decode(new_ids, skip_special_tokens=True)
        return generation, int(len(new_ids))

    # ---- (h) throughput probe ----
    probe_prompt = "The quick brown fox jumps over the lazy dog. " * 10
    inp = tokenizer(probe_prompt, return_tensors="pt")
    t0 = time.time()
    with torch.no_grad():
        out = model.generate(inp["input_ids"], max_new_tokens=50,
                             do_sample=False,
                             pad_token_id=tokenizer.eos_token_id)
    probe_secs = time.time() - t0
    sec_per_tok = probe_secs / 50.0
    design_new = 760 * (15 + 120 + 120) + 40 * 15 + 20 * 240  
    proj_h = design_new * sec_per_tok / 3600.0
    summary["throughput_probe"] = {"sec_per_token": round(sec_per_tok, 4),
                                   "projected_design_hours": round(proj_h, 2),
                                   "design_forwards": design_new}
    summary["guards"]["h_compute_gate"] = proj_h <= 72.0
    summary["guards"]["g_design_assert"] = design_new <= 200000
    log(f"(h) probe: {sec_per_tok:.3f}s/tok; transitive-only design "
        f"{design_new} forwards projects {proj_h:.2f}h (cap 72h) -> "
        f"{'PASS' if proj_h <= 72 else 'INCONCLUSIVE'}; "
        f"(g) design {design_new} ≤ 200000 -> "
        f"{'PASS' if design_new <= 200000 else 'FAIL'}")
    if proj_h > 72.0:
        summary["outcome"] = "INCONCLUSIVE"
        summary["reason"] = "guard (h): compute-infeasible"
        summary["elapsed_hours"] = round((time.time() - t_start) / 3600, 2)
        dump_summary(summary)
        log("INCONCLUSIVE: guard (h)")
        return

    by_level = {lvl: [it for it in bench if it["stratum"] == lvl]
                for lvl in LEVELS}
    assert all(len(v) == N_PER_LEVEL for v in by_level.values())

    def step0_record(rec):
        with open(STEP0_JSONL, "a") as f:
            f.write(json.dumps(rec) + "\n")

    # ---- (d_s) stratified dry-run gate: 20 fresh items/stratum, B only ----
    dry_acc = {}
    dry_tok = 0
    for lvl in LEVELS:
        items = fresh_subset(by_level[lvl], 20, DRYRUN_SEEDS[lvl])
        corr = 0
        for it in items:
            generation, n_new = gen(it, "B")
            c, first = score_b(generation, it["gold"])
            corr += c
            dry_tok += n_new
            step0_record({"phase": "dryrun", "stratum": lvl,
                          "item_id": it["id"], "arm": "B",
                          "correct": c, "first_token": first,
                          "n_new_tokens": n_new})
        acc = corr / 20
        dry_acc[lvl] = acc
        log(f"(d) dry-run {lvl}: B accuracy = {acc:.4f} (bar [0.2,0.8])")
    summary["dryrun"] = {"b_accuracy": {k: round(v, 4)
                                        for k, v in dry_acc.items()},
                         "forwards": dry_tok}
    d_pass = all(0.2 <= v <= 0.8 for v in dry_acc.values())
    summary["guards"]["ds_stratified_gate"] = d_pass
    if not d_pass:
        tripped = [k for k, v in dry_acc.items() if not (0.2 <= v <= 0.8)]
        summary["outcome"] = "HELD"
        summary["reason"] = (f"stratified dry-run gate (d_s): {tripped} "
                             f"B accuracy {dry_acc} — primary unmeasurable; "
                             "STOP at design cost")
        summary["elapsed_hours"] = round((time.time() - t_start) / 3600, 2)
        dump_summary(summary)
        log(f"HELD: stratified dry-run gate tripped on {tripped}")
        return
    log("(d_s) stratified dry-run gate PASS (both transitive strata)")

    # ---- C+S pilot: 20 items from the transitive strata, C and S arms ----
    transitive_all = by_level["transitive-2hop"] + by_level["transitive-3hop"]
    pilot_items = fresh_subset(transitive_all, 20, PILOT_SEED)
    pilot_recs = []
    pilot_tok = 0
    for it in pilot_items:
        for arm in ("C", "S"):
            generation, n_new = gen(it, arm)
            c, first = score_cs(generation, it["gold"])
            pilot_recs.append((it["id"], arm, c))
            pilot_tok += n_new
            step0_record({"phase": "pilot", "stratum": it["stratum"],
                          "item_id": it["id"], "arm": arm,
                          "correct": c, "first_token": first,
                          "n_new_tokens": n_new})
    by_id = {}
    for iid, arm, c in pilot_recs:
        by_id.setdefault(iid, {})[arm] = c
    b_p = sum(1 for v in by_id.values() if v["C"] != v["S"])
    d_pilot = b_p / 20.0
    summary["pilot"] = {"d_pilot": round(d_pilot, 4),
                        "discordant": f"{b_p}/20",
                        "forwards": pilot_tok}
    log(f"C+S pilot: d_pilot = {d_pilot:.4f} (discordant {b_p}/20)")

    # ---- registered Step-0 power rule (bench-size STOP/HELD; no n-raise) ----
    power, se = wald_power(d_pilot, N_PER_LEVEL)
    summary["power_rule"] = {"d_src": round(d_pilot, 4),
                             "power": round(power, 4),
                             "se_theta": round(se, 4),
                             "n_per_level": N_PER_LEVEL,
                             "band_floor": 0.74}
    log(f"Step-0 power: Φ(0.10/{se:.4f} − 1.645) = {power:.3f} "
        f"(band [0.74, 0.88], floor 0.74)")
    if power < 0.74:
        summary["outcome"] = "HELD"
        summary["reason"] = (f"bench-size rule: Step-0 registered power "
                             f"{power:.3f} < 0.74 (band floor) — bench cannot "
                             f"supply even the design's own power bar; STOP "
                             f"at design cost (computation, not choice)")
        summary["elapsed_hours"] = round((time.time() - t_start) / 3600, 2)
        dump_summary(summary)
        log("HELD: bench-size power rule")
        return
    log("Step-0 power rule PASS — proceeding to full run")

    # ---- full run ----
    done = load_done()
    log(f"resuming: {len(done)} (item, arm) pairs already done")

    def run_item_arm(it, arm):
        generation, n_tok = gen(it, arm)
        scorer = score_b if arm == "B" else score_cs
        correct, first_tok = scorer(generation, it["gold"])
        rec = {"item_id": it["id"], "stratum": it["stratum"], "arm": arm,
               "gold": it["gold"], "generation": generation,
               "first_token": first_tok, "correct": correct,
               "n_new_tokens": n_tok}
        with open(JSONL, "a") as f:
            f.write(json.dumps(rec) + "\n")
            f.flush()
            os.fsync(f.fileno())
        done.add((it["id"], arm))
        return n_tok

    for lvl in LEVELS:
        for it in by_level[lvl]:
            if (it["id"], "B") not in done:
                run_item_arm(it, "B")
        log(f"B arm complete for {lvl} ({N_PER_LEVEL} items)")

    # C+S with d_block1 keying after each level's first 20 C+S pairs.
    # Execution-lane mechanical choice (documented): per-level 20-item
    # blocks (consistent with the 20-item pilot); the combined check uses
    # d_src = max(block d's) — fails-safe (conservative).
    block_d = {}

    def cs_pairs_for(ids):
        cs = {i: {} for i in ids}
        with open(JSONL) as f:
            for line in f:
                r = json.loads(line)
                if r["item_id"] in cs and r["arm"] in ("C", "S"):
                    cs[r["item_id"]][r["arm"]] = r["correct"]
        return cs

    for lvl in LEVELS:
        items = by_level[lvl]
        for it in items:
            for arm in ("C", "S"):
                if (it["id"], arm) not in done:
                    run_item_arm(it, arm)
            # after each level's first 20 C+S pairs complete, key the block
            n_cs_done = sum(1 for i2 in items[:20]
                            for a in ("C", "S") if (i2["id"], a) in done)
            if n_cs_done == 40 and lvl not in block_d:
                cs = cs_pairs_for({i2["id"] for i2 in items[:20]})
                b_h = sum(1 for v in cs.values()
                          if len(v) == 2 and v["C"] != v["S"])
                d_b = b_h / 20.0
                block_d[lvl] = d_b
                d_src = max(block_d.values())
                p_b, _ = wald_power(d_src, N_PER_LEVEL)
                log(f"d_block1[{lvl}] = {d_b:.4f}; combined d_src = "
                    f"{d_src:.4f} -> power {p_b:.3f}")
                if p_b < 0.74:
                    summary["block_keying"] = {
                        k: round(v, 4) for k, v in block_d.items()}
                    summary["outcome"] = "HELD"
                    summary["reason"] = (
                        f"d_block1 keying: registered power {p_b:.3f} < 0.74 "
                        f"(band floor) — STOP the full run at this point "
                        f"(computation, not choice)")
                    summary["elapsed_hours"] = round(
                        (time.time() - t_start) / 3600, 2)
                    dump_summary(summary)
                    log("HELD: d_block1 keying")
                    return
        log(f"C/S complete for {lvl} ({N_PER_LEVEL} items)")
    summary["block_keying"] = {k: round(v, 4) for k, v in block_d.items()}
    log(f"d_block1 keying PASS: {summary['block_keying']}")

    # ---- guards (e), (f), (f'), (g); (a) post-hash ----
    recs = [json.loads(l) for l in open(JSONL)]
    mean_tok = {}
    e_rates = {}
    fp = {}
    for lvl in LEVELS:
        ids = {it["id"] for it in by_level[lvl]}
        by_arm = {}
        for r in recs:
            if r["item_id"] in ids:
                by_arm.setdefault(r["arm"], []).append(r)
        for a in ("B", "C", "S"):
            assert len(by_arm.get(a, [])) == N_PER_LEVEL, \
                f"{lvl}/{a} incomplete: {len(by_arm.get(a, []))}/{N_PER_LEVEL}"
        mt = {a: sum(r["n_new_tokens"] for r in rs) / len(rs)
              for a, rs in by_arm.items()}
        mean_tok[lvl] = mt
        sw = sum(1 for r in by_arm["S"] if WRITE_RE.search(r["generation"]))
        e_rates[lvl] = sw / len(by_arm["S"])
        fp[lvl] = (mt["S"] / mt["C"]) if mt["C"] > 0 else float("inf")
    summary["mean_tokens_per_level"] = {
        k: {a: round(v, 2) for a, v in v.items()}
        for k, v in mean_tok.items()}
    summary["guards"]["e_discipline_rate"] = {k: round(v, 4)
                                              for k, v in e_rates.items()}
    e_pass = all(v >= 0.5 for v in e_rates.values())
    summary["guards"]["e_discipline_pass"] = e_pass
    f_pass = all(mt["C"] > 2 * mt["B"] and mt["S"] > 2 * mt["B"]
                 for mt in mean_tok.values())
    summary["guards"]["f_compute_delivered"] = f_pass
    fp_pass = all((2 / 3) <= r <= (3 / 2) for r in fp.values())
    summary["token_ratio_S_C"] = {k: round(v, 4) for k, v in fp.items()}
    summary["guards"]["fp_budget_matched_per_level"] = fp_pass

    total_gen = (sum(r["n_new_tokens"] for r in recs) + dry_tok + pilot_tok)
    summary["total_generation_forwards"] = total_gen
    summary["guards"]["g_budget"] = total_gen <= 200000
    log(f"guard (g): {total_gen} forwards realized (cap 200000, "
        f"incl. dry-run {dry_tok} + pilot {pilot_tok})")

    post_hash = sha256_state_dict(model)
    summary["guards"]["a_posthash_match"] = (post_hash == BACKBONE_PIN)
    log(f"(a) post-hash match: {summary['guards']['a_posthash_match']}")
    summary["elapsed_hours"] = round((time.time() - t_start) / 3600, 2)
    dump_summary(summary)

    if not e_pass:
        summary["outcome"] = "RUN-INVALID"
        summary["reason"] = "guard (e): discipline not delivered"
    elif not f_pass:
        summary["outcome"] = "RUN-INVALID"
        summary["reason"] = "guard (f): compute not delivered"
    elif not summary["guards"]["g_budget"]:
        summary["outcome"] = "RUN-INVALID"
        summary["reason"] = "guard (g): budget exceeded"
    elif not summary["guards"]["a_posthash_match"]:
        summary["outcome"] = "RUN-INVALID"
        summary["reason"] = "guard (a): Δθ≠0"
    else:
        summary["outcome"] = "PROCEED_TO_VERDICT"
        if not fp_pass:
            summary["fp_note"] = ("guard (f') tripped -> HELD "
                                  "(attribution compromised)")
    dump_summary(summary)
    log(f"run complete: outcome={summary['outcome']} "
        f"elapsed={summary['elapsed_hours']}h forwards={total_gen}")


if __name__ == "__main__":
    main()
