#!/usr/bin/env python3
"""
EXP117 (H11/PTTSC-GEN) execution lane — LOG-4609.
Pre-registration: research/prereg/EXP_PREREG_H11_PTTSCGEN_2026-09-29.md (signed, Law #14 SIGN-WITH-FIXES, fixes byte-verified LOG-4608).
$0 CPU. Frozen backbone. Zero training. No improvisation — the script below implements the pre-reg byte-exactly.
"""
import json, math, hashlib, os, sys, time, traceback

OUTDIR = os.path.expanduser("~/workspace/SCBI/experiments/runs/EXP117_pttscgen/out")
os.makedirs(OUTDIR, exist_ok=True)

# ---------- environment manifest ----------
import torch
import transformers
import numpy as np
try:
    import accelerate
    ACCELERATE_VER = accelerate.__version__
except ImportError:
    ACCELERATE_VER = "NOT AVAILABLE (device_map=default-cpu)"

ENV = {
    "torch": torch.__version__,
    "transformers": transformers.__version__,
    "numpy": np.__version__,
    "accelerate": ACCELERATE_VER,
}
torch.manual_seed(0)
np.random.seed(0)
torch.set_num_threads(2)
THREADS = torch.get_num_threads()

BENCH_PROVENANCE_PIN = "47281cd3dc243369be0aa5be2345663b752cdb4a329a16a37f08da5717230585"
BACKBONE_PIN = "ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed"
BACKBONE_DIR = os.path.expanduser("~/workspace/.exp086_weights/pythia-410m")

PROBE_ITEMS = [0, 1, 2, 5, 6, 7, 8, 9, 10, 11]  # items 3-4 excluded (planner exemplars)

TAIL = ("Plan: Before answering, write 4 distinct numbered solution outlines "
        "(1. 2. 3. 4.), each a different approach to answering the question. "
        "Each outline must be 40 words or fewer. Do not give the final answer yet.")
OUTLINES = (
    "1. Restate the question's ordering constraint in my own words.\n"
    "2. Check each premise statement against the two candidate entities.\n"
    "3. Eliminate the entity contradicted by any premise.\n"
    "4. Name the remaining entity as the answer.")
EXEMPLAR_OUTLINES = [
    "1. Restate the question's ordering constraint in my own words.",
    "2. Check each premise statement against the two candidate entities.",
    "3. Eliminate the entity contradicted by any premise.",
    "4. Name the remaining entity as the answer.",
]
EXEMPLAR_FOLDED = set(o.strip().casefold() for o in EXEMPLAR_OUTLINES)
# Diagnostic only (does not fire any gate): marker-stripped exemplar content,
# to detect the verbatim-content recitation mode that the literal §3.7 definition
# (comparison against marker-prefixed lines) cannot see, because extraction strips
# markers. Reported as a diagnostic alongside the literal gate counts.
EXEMPLAR_CONTENT_FOLDED = set(
    o.split(".", 1)[1].strip().casefold() for o in EXEMPLAR_OUTLINES)

def recites_single(o):
    """Phase 0a pinned literal definition (§3.7): exact match vs pinned exemplar lines."""
    return o.strip().casefold() in EXEMPLAR_FOLDED

def recites_content_single(o):
    """Diagnostic: exact match vs marker-stripped exemplar content."""
    return o.strip().casefold() in EXEMPLAR_CONTENT_FOLDED

def block(i, bench):
    return bench[i]["prompt"] + "\n\n" + TAIL + "\n" + OUTLINES

def planner_prompt(t, bench):
    return block(3, bench) + "\n\n" + block(4, bench) + "\n\n" + bench[t]["prompt"] + "\n\n" + TAIL

def executor_prompt(item, k, outline_text):
    return (item["prompt"] + "\n\n" +
            "Outline %d: %s" % (k, outline_text) + "\n\n" +
            "Develop the outline above into a final answer. Reply with the name of the higher-ranked entity and nothing else.\n\n" +
            "The higher-ranked entity is:")

def baseline_prompt(item):
    return (item["prompt"] + "\n\n" +
            "Reply with the name of the higher-ranked entity and nothing else.\n\n" +
            "The higher-ranked entity is:")

# ---------- reference implementation of EXP113's T2-P2 construction (from exp113_run.py lines 68-122, signed execution script) ----------
def ref_exp113_t2p2(t, bench):
    T2_P1_TAIL = ("\n\nPlan: Before answering, write 4 distinct numbered solution outlines "
                  "(1. 2. 3. 4.), each a different approach to answering the question. "
                  "Each outline must be 40 words or fewer. Do not give the final answer yet.")
    EXEMPLAR_OUTLINES_REF = (
        "1. Restate the question's ordering constraint in my own words.\n"
        "2. Check each premise statement against the two candidate entities.\n"
        "3. Eliminate the entity contradicted by any premise.\n"
        "4. Name the remaining entity as the answer.")
    parts = []
    for ei in (3, 4):
        parts.append(bench[ei]["prompt"] + T2_P1_TAIL + "\n" + EXEMPLAR_OUTLINES_REF)
    return "\n\n".join(parts) + "\n\n" + bench[t]["prompt"] + T2_P1_TAIL

# ---------- helpers ----------
def sha256_of_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def backbone_hash(model):
    sd = model.state_dict()
    h = hashlib.sha256()
    for k in sorted(sd.keys()):
        t = sd[k].detach().to(torch.float32).contiguous()
        h.update(t.cpu().numpy().tobytes())
    return h.hexdigest()

def extract_outlines(output):
    """H4 §3.3 verbatim."""
    markers = ["1.", "2.", "3.", "4."]
    first_pos = {}
    for m in markers:
        idx = output.find(m)
        first_pos[m] = idx
    # positions in occurrence order
    occ = sorted((p, m) for m, p in first_pos.items() if p != -1)
    outlines = {}
    for order, (p, m) in enumerate(occ):
        start = p + len(m)
        if order + 1 < len(occ):
            end = occ[order + 1][0]
        else:
            end = len(output)
        outlines[m] = output[start:end].strip()
    res = []
    for m in markers:
        res.append(outlines.get(m, ""))
    # drop empties and exact duplicates
    seen = set()
    uniq = []
    for o in res:
        if o and o not in seen:
            seen.add(o)
            uniq.append(o)
    return uniq

def parse_entity(generated_text, ent_a, ent_c):
    """§3.6 verbatim."""
    t = generated_text.strip().rstrip(".,;:!?").strip()
    low = t.casefold()
    if low == ent_a.casefold():
        return ent_a
    if low == ent_c.casefold():
        return ent_c
    return None

def recites(outlines):
    """Phase 0a pinned literal definition (§3.7): exact match vs marker-prefixed exemplar lines."""
    n_rec = 0
    for o in outlines:
        if recites_single(o):
            n_rec += 1
    return n_rec

def recites_content_count(outlines):
    """Diagnostic only (does not fire the gate): verbatim-content recitation vs marker-stripped exemplar content."""
    n = 0
    for o in outlines:
        if recites_content_single(o):
            n += 1
    return n

def token_overlap(o, ex):
    ot = set(o.casefold().split())
    et = set(ex.casefold().split())
    if not ot or not et:
        return 0.0
    return len(ot & et) / max(len(ot), len(et))

def mcnemar_one_sided(b, c):
    n = b + c
    if n == 0:
        return 1.0, 0
    p = sum(math.comb(n, i) for i in range(b, n + 1)) / (2 ** n)
    return p, n

log_lines = []
def log(msg):
    line = "[%s] %s" % (time.strftime("%H:%M:%S"), msg)
    log_lines.append(line)
    print(line, flush=True)

GENERATIONS = []

def generate(model, tok, prompt, max_new_tokens):
    inp = tok(prompt, return_tensors="pt")
    with torch.no_grad():
        out = model.generate(inp["input_ids"], max_new_tokens=max_new_tokens,
                             do_sample=False, pad_token_id=tok.eos_token_id)
    gen_ids = out[0][inp["input_ids"].shape[1]:]
    return tok.decode(gen_ids, skip_special_tokens=True)

# ---------- main ----------
def main():
    worksheet = {"env": ENV, "threads": THREADS, "seeds": {"torch": 0, "numpy": 0},
                 "pins": {"bench_provenance": BENCH_PROVENANCE_PIN, "backbone": BACKBONE_PIN}}
    run = {"verdict": None, "gates": {}, "phases": {}, "items": []}

    # --- bench ---
    t0 = time.time()
    prov = sha256_of_file(os.path.expanduser(
        "~/workspace/SCBI/experiments/runs/EXP077_cone_vs_line/exp077_instance_records.json"))
    log("bench provenance sha256: %s... (expect %s...)" % (prov[:16], BENCH_PROVENANCE_PIN[:16]))
    if prov != BENCH_PROVENANCE_PIN:
        run["verdict"] = "RUN-INVALID (bench provenance pin mismatch)"
        finalize(run, worksheet); return

    sys.path.insert(0, os.path.expanduser("~/workspace/SCBI/experiments/runs/EXP089_clm8b_falsifier"))
    import benchmark_exp089
    bench = benchmark_exp089.build_benchmark()
    assert len(bench) == 60, "bench len != 60"
    log("bench built: len=%d" % len(bench))

    # --- model ---
    log("loading tokenizer + model from %s" % BACKBONE_DIR)
    tok = transformers.AutoTokenizer.from_pretrained(BACKBONE_DIR, trust_remote_code=False)
    if tok.pad_token_id is None:
        tok.pad_token_id = tok.eos_token_id
    load_kwargs = {"torch_dtype": torch.float32, "trust_remote_code": False}
    if ACCELERATE_VER != "NOT AVAILABLE (device_map=default-cpu)":
        load_kwargs["device_map"] = "cpu"
    model = transformers.AutoModelForCausalLM.from_pretrained(BACKBONE_DIR, **load_kwargs)
    model.eval()
    device_map = "cpu" if "device_map" in load_kwargs else "default-cpu"
    worksheet["device_map"] = device_map

    h_pre = backbone_hash(model)
    log("backbone hash BEFORE: %s... (expect %s...)" % (h_pre[:16], BACKBONE_PIN[:16]))
    if h_pre != BACKBONE_PIN:
        run["verdict"] = "RUN-INVALID (backbone pin mismatch BEFORE; quarantine)"
        finalize(run, worksheet); return

    # --- planner prompts + byte-identity check vs EXP113 reference ---
    prompts = [planner_prompt(t, bench) for t in range(60)]
    mism = 0
    for t in range(60):
        if prompts[t] != ref_exp113_t2p2(t, bench):
            mism += 1
            if mism == 1:
                log("BYTE MISMATCH at item %d" % t)
    worksheet["planner_prompt_byte_identity_mismatches"] = mism
    log("planner prompt byte-identity vs EXP113 T2-P2 reference: %d/60 mismatches" % mism)
    if mism > 0:
        run["verdict"] = "RUN-INVALID (planner prompt byte-identity apparatus bug)"
        finalize(run, worksheet); return

    global GENERATIONS
    GENERATIONS.clear()  # raw records
    def gen_record(arm, item_idx, prompt_text, output_text, n_new, exception):
        rec = {"arm": arm, "item_idx": item_idx, "prompt_sha256": hashlib.sha256(prompt_text.encode()).hexdigest(),
               "output": output_text, "n_new_tokens": n_new, "exception": exception}
        GENERATIONS.append(rec)
        return rec

    exceptions_total = 0

    def safe_generate(arm, item_idx, prompt_text, max_new):
        nonlocal exceptions_total
        try:
            out = generate(model, tok, prompt_text, max_new)
            return gen_record(arm, item_idx, prompt_text, out, max_new, None)
        except Exception as e:
            exceptions_total += 1
            return gen_record(arm, item_idx, prompt_text, "", max_new, repr(e))

    # --- Phase 0a: recitation check ---
    log("Phase 0a: recitation check on 10 probe items")
    recited_items = 0
    phase0a_details = []
    max_overlaps = []
    for t in PROBE_ITEMS:
        rec = safe_generate("phase0a_planner", t, prompts[t], 160)
        outlines = extract_outlines(rec["output"])
        n_rec = recites(outlines)
        n_rec_content = recites_content_count(outlines)
        is_rec = n_rec >= 2
        recited_items += int(is_rec)
        phase0a_details.append({"item": t, "n_outlines": len(outlines), "n_recited_literal": n_rec,
                                "n_recited_content_diagnostic": n_rec_content, "recited": is_rec})
        for o in outlines:
            mo = max(token_overlap(o, ex) for ex in EXEMPLAR_OUTLINES)
            max_overlaps.append(mo)
    diag_overlap = sum(max_overlaps) / len(max_overlaps) if max_overlaps else 0.0
    run["phases"]["phase0a"] = {"recited_items": recited_items, "denominator": 10,
                                "details": phase0a_details,
                                "diagnostic_mean_max_token_overlap": diag_overlap}
    log("Phase 0a: recited items (literal §3.7 definition) = %d/10 (gate: >=6 -> RUN-INVALID); diag mean max overlap = %.4f" % (recited_items, diag_overlap))
    n_content_recited_items = sum(1 for d in phase0a_details if d["n_recited_content_diagnostic"] >= 2)
    log("Phase 0a DIAGNOSTIC: items with >=2 content-level verbatim recitations = %d/10 (does NOT fire the gate; reports the marker-strip blind spot)" % n_content_recited_items)
    run["phases"]["phase0a"]["content_recited_items_diagnostic"] = n_content_recited_items
    if recited_items >= 6:
        run["verdict"] = "RUN-INVALID (Phase 0a: planner recites exemplars, not planning)"
        finalize(run, worksheet); return

    # --- Phase 0b: decision-channel mini-gate ---
    log("Phase 0b: decision-channel mini-gate on 10 probe items")
    n_pars0 = 0
    parsed_vals = []
    for t in PROBE_ITEMS:
        rec = safe_generate("phase0b_baseline", t, baseline_prompt(bench[t]), 16)
        v = parse_entity(rec["output"], bench[t]["A"], bench[t]["C"])
        if v is not None:
            n_pars0 += 1
            parsed_vals.append(v.casefold())
    distinct = len(set(parsed_vals))
    minority = min(parsed_vals.count(v) for v in set(parsed_vals)) if set(parsed_vals) else 0
    run["phases"]["phase0b"] = {"parseable": n_pars0, "denominator": 10,
                                "distinct": distinct, "minority": minority}
    log("Phase 0b: parseable = %d/10 (gate: <8 -> RUN-INVALID); distinct=%d, minority=%d (gate: <2 distinct or minority<2 -> RUN-INVALID)" % (n_pars0, distinct, minority))
    if n_pars0 < 8 or distinct < 2 or minority < 2:
        run["verdict"] = "RUN-INVALID (Phase 0b: no generation decision channel on this bench/shape)"
        finalize(run, worksheet); return

    # --- Full run ---
    log("Phase 0 passed; full run on 60 items")
    n_planner_gens = 60
    n_executor_gens = 0
    n_baseline_gens = 60
    per_item = []
    for t in range(60):
        item = bench[t]
        prec = safe_generate("planner", t, prompts[t], 160)
        outlines = extract_outlines(prec["output"])
        planner_valid = len(outlines) >= 2
        exec_votes = []
        exec_pars = 0
        for k, o in enumerate(outlines):
            erec = safe_generate("executor", t, executor_prompt(item, k + 1, o), 16)
            n_executor_gens += 1
            v = parse_entity(erec["output"], item["A"], item["C"])
            if v is not None:
                exec_pars += 1
                exec_votes.append(v.casefold())
        brec = safe_generate("baseline", t, baseline_prompt(item), 16)
        bv = parse_entity(brec["output"], item["A"], item["C"])
        valid = planner_valid and exec_pars >= 2 and bv is not None
        # pipeline decision: majority of parseable executor votes; even-split tie -> foil (bench "C")
        pipe_dec = None
        if exec_pars:
            a_count = sum(1 for v in exec_votes if v == item["A"].casefold())
            c_count = len(exec_votes) - a_count
            if a_count > c_count:
                pipe_dec = "A"
            elif c_count > a_count:
                pipe_dec = "C"
            else:
                pipe_dec = "C"  # foil tie-break (conservative)
        base_dec = None
        if bv is not None:
            base_dec = "A" if bv == item["A"].casefold() else "C"
        target = "A"
        per_item.append({
            "item": t, "id": item["id"],
            "n_outlines": len(outlines), "planner_valid": planner_valid,
            "exec_parseable": exec_pars, "n_executor_gens": len(outlines),
            "baseline_parseable": bv is not None, "valid": valid,
            "pipeline_decision": pipe_dec, "baseline_decision": base_dec,
            "pipeline_correct": (pipe_dec == target) if (valid and pipe_dec) else None,
            "baseline_correct": (base_dec == target) if (valid and base_dec) else None,
        })
    run["generation_counts"] = {"planner": n_planner_gens, "executor": n_executor_gens, "baseline": n_baseline_gens}
    total_gens = n_planner_gens + n_executor_gens + n_baseline_gens + 20
    log("full run: %d generations total (+20 phase0); exceptions=%d" % (total_gens, exceptions_total))
    if exceptions_total > 0.10 * total_gens:
        run["verdict"] = "RUN-INVALID (>10%% per-generation exceptions; apparatus bug)"
        finalize(run, worksheet); return

    # --- backbone pin after ---
    h_post = backbone_hash(model)
    log("backbone hash AFTER: %s... (expect %s...)" % (h_post[:16], BACKBONE_PIN[:16]))
    if h_post != BACKBONE_PIN:
        run["verdict"] = "RUN-INVALID (backbone pin mismatch AFTER; quarantine)"
        finalize(run, worksheet); return
    log("Δθ=0 confirmed")

    # --- deterministic re-parse ×2 ---
    def parse_table():
        rows = []
        for rec in GENERATIONS:
            arm = rec["arm"]
            rows.append((rec["item_idx"], arm, rec["output"]))
        return rows
    p1 = parse_table(); p2 = parse_table()
    worksheet["reparse_byte_identical"] = (p1 == p2)
    log("deterministic re-parse x2 byte-identical: %s" % (p1 == p2))
    if p1 != p2:
        run["verdict"] = "RUN-INVALID (re-parse mismatch; apparatus bug)"
        finalize(run, worksheet); return

    # --- validity + elicitation gate ---
    valid_items = [it for it in per_item if it["valid"]]
    n_valid = len(valid_items)
    run["n_valid"] = n_valid
    log("n_valid = %d/60 (gate: <48 -> RUN-INVALID)" % n_valid)
    if n_valid < 48:
        run["verdict"] = "RUN-INVALID (elicitation-failure gate: n_valid=%d < 48)" % n_valid
        finalize(run, worksheet); return

    # --- paired McNemar on valid items ---
    b = sum(1 for it in valid_items if it["pipeline_correct"] and not it["baseline_correct"])
    c = sum(1 for it in valid_items if not it["pipeline_correct"] and it["baseline_correct"])
    p_val, n_pairs = mcnemar_one_sided(b, c)
    net = b - c
    run["mcnemar"] = {"b": b, "c": c, "n": n_pairs, "net": net, "one_sided_p": p_val}
    log("McNemar: b=%d (fixes), c=%d (breaks), n=%d, net=%+d, one-sided p=%.8f" % (b, c, n_pairs, net, p_val))
    if p_val <= 0.05 and b > c:
        run["verdict"] = "CONTINUE (McNemar one-sided p=%.5f <= 0.05, b=%d > c=%d)" % (p_val, b, c)
    elif net <= 0:
        run["verdict"] = "KILL (net b-c=%d <= 0)" % net
    else:
        run["verdict"] = "HELD (net=%d > 0 but p=%.5f > 0.05)" % (net, p_val)

    finalize(run, worksheet)

def finalize(run, worksheet):
    run["exceptions_total_note"] = "see generations records"
    run["worksheet"] = worksheet
    run["completed_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    with open(os.path.join(OUTDIR, "exp117_result.json"), "w") as f:
        json.dump(run, f, indent=2)
    with open(os.path.join(OUTDIR, "exp117_generations.json"), "w") as f:
        json.dump({"generations": GENERATIONS}, f, indent=1)
    log("FINAL VERDICT: %s" % run["verdict"])
    with open(os.path.join(OUTDIR, "exp117_stdout.log"), "w") as f:
        f.write("\n".join(log_lines) + "\n")

if __name__ == "__main__":
    t_start = time.time()
    main()
    print("wall time: %.1f min" % ((time.time() - t_start) / 60.0), flush=True)
