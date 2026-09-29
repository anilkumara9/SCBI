#!/usr/bin/env python3
"""EXP121 (H19/PTTSC-SUFFIX) execution lane — LOG-4644 pre-assigned.
Pre-registration: research/prereg/EXP_PREREG_H19_PTTSCSUFFIX_2026-09-29.md
(signed: Law #14 SIGN-WITH-FIXES LOG-4642, FIX-1 byte-verified LOG-4643).
$0 CPU. Frozen backbone (Delta theta = 0). Zero training. No improvisation —
the script implements the pre-reg exactly; the falsification-tree order is
mirrored in code; the metric is read only AFTER all guards pass (Law #9).
Law #7: bench ground truth (tuple[0]) is used ONLY at metric time.
Defect classes pinned: executor-computed p-values only; raw records
hash-pinned before the verdict; FIX-1 label-pin discipline; no reuse of
EXP117's §3.7; the [-3:] identity pin.
"""
import json, math, hashlib, os, sys, time

OUTDIR = os.path.expanduser("~/workspace/SCBI/experiments/runs/EXP121_pttscsuffix/out")
os.makedirs(OUTDIR, exist_ok=True)
SCRIPT_PATH = os.path.abspath(__file__)

# ---------------- Law #13 pins (§3.1) ----------------
SNAP = os.path.expanduser("~/workspace/.exp086_weights/pythia-410m")
WEIGHTS_PIN = "ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed"  # LOG-331
NPZ_PIN = "6cf4a8a726a2b6e4623f57d0287d95879866f77e789bcc3789fb693cf2af6a76"
EMB_BYTES_PIN = "9b6e8afb091ba1edbb0311ba1d3414d34a65942c3fdecb4533b69720f2a99123"
IDS_BYTES_PIN = "3669e102222719d66f61daca46ae1ac34e844e398ae433743a5b37bfc5075cb9"
BENCH_PIN = "e91b302f41f641c74e56957e526efcd4866bac62d134e157defe0a4cdd49e4f5"
NPZ_PATH = os.path.expanduser("~/workspace/SCBI/experiments/runs/EXP107_templatectrl/out/exp107_test_embeddings.npz")
BUILDER_DIR = os.path.expanduser("~/workspace/SCBI/experiments/runs/EXP107_templatectrl")
EXP112_PER_ITEM = os.path.expanduser("~/workspace/SCBI/experiments/runs/EXP112_hdildr/out/exp112_per_item.json")
QUESTION_SUFFIX = " Question: Who is higher in rank? Answer:"
PROBE_ITEMS = [0, 1, 2, 5, 6, 7, 8, 9, 10, 11]  # items 3-4 excluded (planner exemplars)
SEED = 0

log_lines = []
def log(msg):
    line = "[%s] %s" % (time.strftime("%H:%M:%S"), msg)
    log_lines.append(line)
    print(line, flush=True)

def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()

def sha256_file(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def state_dict_hash(model):
    """Canonical LOG-331 method: sha256 over sorted state_dict keys, float32 bytes."""
    import numpy as np
    sha = hashlib.sha256()
    sd = model.state_dict()
    for k in sorted(sd.keys()):
        sha.update(np.asarray(sd[k].detach().cpu(), dtype=np.float32).tobytes())
    return sha.hexdigest()

def mcnemar_one_sided(b, c):
    n = b + c
    if n == 0:
        return 1.0, 0
    p = sum(math.comb(n, i) for i in range(b, n + 1)) / (2 ** n)
    return p, n

# ---------------- §3.3 planner spec (T2-P2, H14 §3.3 <- H11 §3.3 <- H7 §3.3) ----------------
TAIL = ("Plan: Before answering, write 4 distinct numbered solution outlines "
        "(1. 2. 3. 4.), each a different approach to answering the question. "
        "Each outline must be 40 words or fewer. Do not give the final answer yet.")
OUTLINES = (
    "1. Restate the question's ordering constraint in my own words.\n"
    "2. Check each premise statement against the two candidate entities.\n"
    "3. Eliminate the entity contradicted by any premise.\n"
    "4. Name the remaining entity as the answer.")

def block(i, bench):
    return bench[i]["prompt"] + "\n\n" + TAIL + "\n" + OUTLINES

def planner_prompt(t, bench):
    return block(3, bench) + "\n\n" + block(4, bench) + "\n\n" + bench[t]["prompt"] + "\n\n" + TAIL

def ref_t2p2(t, bench):
    """Independent reference: EXP113's signed T2-P2 construction (exp113_run.py,
    build_prompts: t2p2_parts + final join), applied to this bench."""
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

def extract_outlines(output):
    """H4 §3.3 verbatim: first-occurrence markers, preamble discarded, missing
    marker -> empty, drop empties and exact duplicates."""
    markers = ["1.", "2.", "3.", "4."]
    first_pos = {}
    for m in markers:
        first_pos[m] = output.find(m)
    occ = sorted((p, m) for m, p in first_pos.items() if p != -1)
    outlines = {}
    for order, (p, m) in enumerate(occ):
        start = p + len(m)
        end = occ[order + 1][0] if order + 1 < len(occ) else len(output)
        outlines[m] = output[start:end].strip()
    res = [outlines.get(m, "") for m in markers]
    seen, uniq = set(), []
    for o in res:
        if o and o not in seen:
            seen.add(o)
            uniq.append(o)
    return uniq

# Corrected recitation diagnostic (§3.7, diagnostic only — NOT a gate):
_EXEMPLAR_LINES = [l for l in OUTLINES.split("\n") if l.strip()]
EXEMPLAR_CONTENT_FOLDED = set(l.split(".", 1)[1].strip().casefold() for l in _EXEMPLAR_LINES)

def recites_content_count(outlines):
    return sum(1 for o in outlines if o.strip().casefold() in EXEMPLAR_CONTENT_FOLDED)

# ---------------- §3.4 plan-INSERTED context (placement (A)) / §3.5 baseline ----------------
def plan_block(outlines):
    return "Plan:\n" + "\n".join("%d. %s" % (i + 1, o) for i, o in enumerate(outlines))

def context_plan(item, outlines):
    """Placement (A): plan block inserted between premise and question tail.
    Code-equivalent pinned form: PROMPT.replace(QUESTION_SUFFIX, " " + PLAN_BLOCK
    + QUESTION_SUFFIX, 1)."""
    prompt = item["prompt"]
    pb = plan_block(outlines)
    n_occ = prompt.count(QUESTION_SUFFIX)
    assert n_occ == 1, "QUESTION_SUFFIX occurs %d times (expected exactly 1)" % n_occ
    return prompt.replace(QUESTION_SUFFIX, " " + pb + QUESTION_SUFFIX, 1)

def context_base(item):
    return item["prompt"]

# ---------------- model-contact raw records (module-level so finalize can
# persist them on EVERY exit path — defect class 2) ----------------
GENERATIONS = []   # raw planner generation records
FORWARDS = []      # raw forward records (both arms)

# ---------------- main ----------------
def main():
    import torch, transformers
    import numpy as np
    run = {"verdict": None, "gates": {}, "phases": {}, "items": []}

    # --- environment manifest (Law #13) ---
    torch.manual_seed(SEED); np.random.seed(SEED)
    torch.set_num_threads(2)
    import sklearn
    manifest = {
        "torch": torch.__version__, "transformers": transformers.__version__,
        "numpy": np.__version__, "sklearn": sklearn.__version__,
        "snapshot": SNAP,
        "torch_num_threads_set": 2, "torch_num_threads_readback": torch.get_num_threads(),
        "seeds": {"torch": SEED, "numpy": SEED},
        "device": "cpu", "dtype": "float32", "device_map": "cpu",
        "generation": {"do_sample": False, "max_new_tokens": 160},
    }
    log("ENV: " + json.dumps(manifest))
    worksheet = {"experiment": "EXP121", "hypothesis": "H19/PTTSC-SUFFIX", "lane": "LOG-4644",
                 "environment": manifest,
                 "pins": {"npz": NPZ_PIN, "embeddings_bytes": EMB_BYTES_PIN,
                          "ids_bytes": IDS_BYTES_PIN, "bench": BENCH_PIN,
                          "backbone_pin_expected": WEIGHTS_PIN}}

    # --- §3.1 archive pins (before any use) ---
    with open(NPZ_PATH, "rb") as f:
        npz_bytes = f.read()
    assert sha256_bytes(npz_bytes) == NPZ_PIN, "npz pin MISMATCH"
    d = np.load(NPZ_PATH, allow_pickle=True)
    emb = np.ascontiguousarray(d["embeddings"]); ids = np.ascontiguousarray(d["ids"])
    assert sha256_bytes(emb.tobytes()) == EMB_BYTES_PIN, "embeddings-bytes pin MISMATCH"
    assert sha256_bytes(ids.tobytes()) == IDS_BYTES_PIN, "ids-bytes pin MISMATCH"
    assert emb.shape == (60, 1024) and emb.dtype == np.float32
    log("npz pins OK")

    # --- §3.1 bench build + provenance pin + schema assertion ---
    sys.path.insert(0, BUILDER_DIR)
    import build_exp107_bench as b
    bench = b.build_bench()
    assert len(bench) == 60, "bench len != 60"
    canon = json.dumps(bench, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    assert sha256_bytes(canon.encode("utf-8")) == BENCH_PIN, "bench pin MISMATCH"
    bench_ids = np.array([it["id"] for it in bench])
    assert (bench_ids == ids).all(), "bench ids vs npz ids mismatch"
    for it in bench:
        assert all(k in it for k in ("prompt", "premise", "tuple", "phrasing", "id")), "schema key missing"
        assert len(it["tuple"]) >= 2, "tuple len < 2"
        assert it["prompt"] == it["premise"] + QUESTION_SUFFIX, "decomposition assertion failed (§3.1/§3.4)"
    log("bench pin OK: 60 items; schema + decomposition assertion pass (§3.1/§3.4)")

    # --- archived EXP112 readout column + pinned token ids ---
    arch = json.load(open(EXP112_PER_ITEM))
    assert len(arch) == 60, "archived readout column len != 60"
    arch_readout = {r["id"]: r["readout"] for r in arch}
    arch_t = {r["id"]: (r["t1"], r["t2"]) for r in arch}
    log("archived EXP112 readout column loaded: 60 records")

    # --- tokenizer (tokenizer-only; NOT model contact) + §3.6 BPE re-assertion ---
    tok = transformers.AutoTokenizer.from_pretrained(SNAP, local_files_only=True, trust_remote_code=False)
    if tok.pad_token_id is None:
        tok.pad_token_id = tok.eos_token_id
    items = []
    for it in bench:
        E1, E2 = it["tuple"][0], it["tuple"][-1]
        i1 = tok.encode(" " + E1); i2 = tok.encode(" " + E2)
        if not (len(i1) == 1 and len(i2) == 1):
            run["verdict"] = "RUN-INVALID (BPE single-token assertion failed on item %s)" % it["id"]
            finalize(run, worksheet); return
        t1, t2 = i1[0], i2[0]
        at1, at2 = arch_t[it["id"]]
        if not (t1 == at1 and t2 == at2):
            run["verdict"] = "RUN-INVALID (token-id drift vs EXP112 worksheet pin on item %s)" % it["id"]
            finalize(run, worksheet); return
        items.append({"id": it["id"], "prompt": it["prompt"], "premise": it["premise"],
                      "tuple": it["tuple"], "E1": E1, "E2": E2, "t1": t1, "t2": t2})
    log("BPE single-token re-assertion: 120/120; token ids match EXP112 worksheet pins")

    # --- Phase 0-pre (§3.7): tokenizer-only [-3:] identity pre-check, NO model contact ---
    # Deterministic placeholder plan block (text-level check; content irrelevant).
    PLACEHOLDER_OUTLINES = ["Placeholder outline one.", "Placeholder outline two.",
                           "Placeholder outline three."]
    def context_plan_placeholder(item):
        pb = plan_block(PLACEHOLDER_OUTLINES)
        assert item["prompt"].count(QUESTION_SUFFIX) == 1
        return item["prompt"].replace(QUESTION_SUFFIX, " " + pb + QUESTION_SUFFIX, 1)
    log("Phase 0-pre: tokenizer-only [-3:] identity pre-check on 60 items (no model contact)")
    precheck = {"placeholder_plan_block": plan_block(PLACEHOLDER_OUTLINES), "details": []}
    for t in range(60):
        ctx_plan = context_plan_placeholder(items[t])
        ctx_base = context_base(items[t])
        tail_plan = tok(ctx_plan, return_tensors="pt")["input_ids"][0].tolist()[-3:]
        tail_base = tok(ctx_base, return_tensors="pt")["input_ids"][0].tolist()[-3:]
        ok = tail_plan == tail_base
        precheck["details"].append({"item": t, "id": items[t]["id"],
                                    "tail_plan": tail_plan, "tail_base": tail_base,
                                    "identity": ok})
        if not ok:
            precheck["failed_on_item"] = t
            run["phases"]["phase0_precheck"] = precheck
            run["verdict"] = ("RUN-INVALID (Phase 0-pre: tokenization identity mismatch on item %d: "
                              "plan-tail %s vs base-tail %s; composition unlicensed)" % (t, tail_plan, tail_base))
            persist_precheck(precheck)
            finalize(run, worksheet); return
    precheck["identity_count"] = 60
    run["phases"]["phase0_precheck"] = precheck
    log("Phase 0-pre: [-3:] identity holds on 60/60 items; composition licensed (mechanical pin)")
    persist_precheck(precheck)

    # --- backbone load + §3.1 pre-contact hash (Law #6) ---
    model = transformers.AutoModelForCausalLM.from_pretrained(
        SNAP, local_files_only=True, trust_remote_code=False,
        device_map="cpu", torch_dtype=torch.float32)
    model.eval()
    h_pre = state_dict_hash(model)
    log("backbone hash BEFORE: %s... (expect %s...)" % (h_pre[:16], WEIGHTS_PIN[:16]))
    if h_pre != WEIGHTS_PIN:
        run["verdict"] = "RUN-INVALID (backbone pin mismatch BEFORE; Law #6 quarantine)"
        finalize(run, worksheet); return
    worksheet["pins"]["backbone_pre"] = h_pre

    # --- §3.3 planner prompts + byte-identity check vs EXP113 reference ---
    prompts = [planner_prompt(t, bench) for t in range(60)]
    mism = sum(1 for t in range(60) if prompts[t] != ref_t2p2(t, bench))
    worksheet["planner_prompt_byte_identity_mismatches"] = mism
    log("planner prompt byte-identity vs EXP113 T2-P2 reference: %d/60 mismatches" % mism)
    if mism > 0:
        run["verdict"] = "RUN-INVALID (planner prompt byte-identity apparatus bug)"
        finalize(run, worksheet); return

    # --- model-contact helpers ---
    exceptions = {"count": 0}

    def generate(t, prompt_text):
        inp = tok(prompt_text, return_tensors="pt")
        try:
            with torch.no_grad():
                out = model.generate(inp["input_ids"], max_new_tokens=160,
                                     do_sample=False, pad_token_id=tok.eos_token_id)
            gen_ids = out[0][inp["input_ids"].shape[1]:]
            text = tok.decode(gen_ids, skip_special_tokens=True)
            exc = None
        except Exception as e:
            exceptions["count"] += 1
            text, exc = "", repr(e)
        rec = {"item_idx": t,
               "prompt_sha256": sha256_bytes(prompt_text.encode("utf-8")),
               "output": text, "exception": exc}
        GENERATIONS.append(rec)
        return rec

    def forward(arm, t, context, rec_item):
        try:
            inp = tok(context, return_tensors="pt")
            with torch.no_grad():
                out = model(**inp)
            logits = out.logits[0, -1, :].to(torch.float64).numpy()
            t1, t2 = rec_item["t1"], rec_item["t2"]
            mx = logits.max(); ex = np.exp(logits - mx); sm = ex / ex.sum()
            mass = float(sm[t1] + sm[t2])
            if logits[t1] == logits[t2]:
                side, tie = "E2", True
            else:
                side, tie = ("E1" if logits[t1] > logits[t2] else "E2"), False
            exc = None
        except Exception as e:
            exceptions["count"] += 1
            side, tie, mass, exc = None, None, -1.0, repr(e)
            logits = None
        rec = {"arm": arm, "item_idx": t,
               "context_sha256": sha256_bytes(context.encode("utf-8")),
               "readout_side": side, "readout_tie": tie, "mass": mass,
               "exception": exc,
               "logit_t1": None if logits is None else float(logits[t1]),
               "logit_t2": None if logits is None else float(logits[t2])}
        FORWARDS.append(rec)
        return rec

    # --- Phase 0a (§3.7): planner bench-transfer check on 10 probe items ---
    log("Phase 0a: planner bench-transfer check on 10 probe items")
    phase0a = {"probe_items": PROBE_ITEMS, "details": []}
    n_planner_valid_0 = 0
    for t in PROBE_ITEMS:
        rec = generate(t, prompts[t])
        outlines = extract_outlines(rec["output"])
        planner_valid = len(outlines) >= 2
        n_planner_valid_0 += int(planner_valid)
        n_rec_content = recites_content_count(outlines)
        phase0a["details"].append({"item": t, "n_outlines": len(outlines),
                                  "planner_valid": planner_valid,
                                  "n_recited_content_diagnostic": n_rec_content})
    phase0a["planner_valid_count"] = n_planner_valid_0
    phase0a["content_recited_items_diagnostic"] = sum(
        1 for dd in phase0a["details"] if dd["n_recited_content_diagnostic"] >= 2)
    run["phases"]["phase0a"] = phase0a
    log("Phase 0a: planner-valid = %d/10 (gate: <8 -> RUN-INVALID)" % n_planner_valid_0)
    log("Phase 0a DIAGNOSTIC (not a gate): items with >=2 content-level recitations = %d/10" %
        phase0a["content_recited_items_diagnostic"])
    if n_planner_valid_0 < 8:
        run["verdict"] = "RUN-INVALID (Phase 0a: planner does not transfer to the EXP107 bench)"
        finalize(run, worksheet); return

    # --- Phase 0b (§3.7): logit slot with plan insertion on 10 probe items ---
    # The [-3:] pin was licensed by the Phase 0-pre mechanical check; here it is
    # re-armed on the REAL plan texts (per item, mismatch -> RUN-INVALID immediately).
    log("Phase 0b: logit slot with plan insertion on 10 probe items")
    phase0b = {"details": []}
    n_valid_0 = 0
    for t in PROBE_ITEMS:
        rec_item = items[t]
        d0 = phase0a["details"][PROBE_ITEMS.index(t)]
        if not d0["planner_valid"]:
            phase0b["details"].append({"item": t, "planner_valid": False, "valid": False,
                                      "note": "planner-invalid; plan context not constructible"})
            continue
        outlines = extract_outlines([g for g in GENERATIONS if g["item_idx"] == t][0]["output"])
        ctx_plan = context_plan(rec_item, outlines)
        ctx_base = context_base(rec_item)
        assert rec_item["premise"] + QUESTION_SUFFIX == rec_item["prompt"]  # §3.4 decomposition
        n_tok = len(tok(ctx_plan, return_tensors="pt")["input_ids"][0])
        assert n_tok < 2048, "context exceeds 2048 tokens"
        tail_plan = tok(ctx_plan, return_tensors="pt")["input_ids"][0].tolist()[-3:]
        tail_base = tok(ctx_base, return_tensors="pt")["input_ids"][0].tolist()[-3:]
        if tail_plan != tail_base:
            run["phases"]["phase0b"] = phase0b
            run["verdict"] = ("RUN-INVALID (Phase 0b: tokenization mismatch on item %d (real plan text): "
                              "plan-tail %s vs base-tail %s)" % (t, tail_plan, tail_base))
            finalize(run, worksheet); return
        fr_plan = forward("plan", t, ctx_plan, rec_item)
        fr_base = forward("base", t, ctx_base, rec_item)
        g1_plan = fr_plan["mass"] >= 0.01
        g1_base = fr_base["mass"] >= 0.01
        valid = g1_plan and g1_base
        n_valid_0 += int(valid)
        phase0b["details"].append({"item": t, "planner_valid": True,
                                  "tokenization_identity": True, "n_tokens_plan": n_tok,
                                  "mass_plan": fr_plan["mass"], "mass_base": fr_base["mass"],
                                  "g1_plan": g1_plan, "g1_base": g1_base, "valid": valid})
    phase0b["valid_count"] = n_valid_0
    run["phases"]["phase0b"] = phase0b
    log("Phase 0b: valid = %d/10 (gate: <8 -> RUN-INVALID)" % n_valid_0)
    if n_valid_0 < 8:
        run["verdict"] = "RUN-INVALID (Phase 0b: logit decision slot does not function with plan insertion)"
        finalize(run, worksheet); return

    # --- Full run (§3.8): 60 planner generations + 120 forwards (fresh; Phase-0 records are diagnostics only) ---
    log("Phase 0 passed; full run on 60 items (fresh records)")
    GENERATIONS.clear(); FORWARDS.clear(); exceptions["count"] = 0
    plans = {}   # t -> outlines (only for planner-valid items)
    for t in range(60):
        rec = generate(t, prompts[t])
        outlines = extract_outlines(rec["output"])
        if len(outlines) >= 2:
            plans[t] = outlines
        if (t + 1) % 10 == 0:
            log("full run: %d/60 planner generations complete" % (t + 1))
    per_item = []
    for t in range(60):
        rec_item = items[t]
        planner_valid = t in plans
        if planner_valid:
            ctx_plan = context_plan(rec_item, plans[t])
            fr_plan = forward("plan", t, ctx_plan, rec_item)
            g1_plan = fr_plan["mass"] >= 0.01
        else:
            fr_plan, g1_plan = None, False
        fr_base = forward("base", t, context_base(rec_item), rec_item)
        g1_base = fr_base["mass"] >= 0.01
        valid = planner_valid and g1_plan and g1_base
        per_item.append({"item": t, "id": rec_item["id"],
                         "planner_valid": planner_valid,
                         "g1_plan": g1_plan, "g1_base": g1_base,
                         "readout_plan": fr_plan["readout_side"] if fr_plan else None,
                         "readout_base": fr_base["readout_side"],
                         "mass_plan": fr_plan["mass"] if fr_plan else None,
                         "mass_base": fr_base["mass"],
                         "valid": valid})
        if (t + 1) % 20 == 0:
            log("full run: %d/60 item forwards complete" % (t + 1))
    run["items"] = per_item  # per-item table available to the report on every exit path
    total_contacts = 60 + 120
    log("full run: 60 planner gens + 120 forwards; exceptions=%d" % exceptions["count"])
    if exceptions["count"] > 0.10 * total_contacts:
        run["verdict"] = "RUN-INVALID (>10%% per-contact exceptions; apparatus bug)"
        finalize(run, worksheet); return

    # --- backbone hash AFTER (Law #6) ---
    h_post = state_dict_hash(model)
    log("backbone hash AFTER: %s... (expect %s...)" % (h_post[:16], WEIGHTS_PIN[:16]))
    if h_post != WEIGHTS_PIN:
        run["verdict"] = "RUN-INVALID (backbone pin mismatch AFTER; Law #6 quarantine)"
        finalize(run, worksheet); return
    worksheet["pins"]["backbone_post"] = h_post
    log("Delta theta = 0 confirmed")

    # --- baseline-reproduction integrity check (§3.8): 60/60 vs archived readout ---
    mism_repro = sum(1 for it in per_item if it["readout_base"] != arch_readout[it["id"]])
    run["baseline_reproduction_mismatches"] = mism_repro
    log("baseline reproduction vs EXP112 archived readout: %d/60 mismatches" % mism_repro)
    if mism_repro > 0:
        run["verdict"] = "RUN-INVALID (baseline reproduction != 60/60; apparatus drift)"
        finalize(run, worksheet); return

    # --- deterministic re-read x2 (pinned pure function of raw forward logs) ---
    def derive_table(fwd_records):
        tbl = {}
        for r in fwd_records:
            tbl[(r["arm"], r["item_idx"])] = r["readout_side"]
        return json.dumps(sorted(tbl.items()), sort_keys=True)
    rt1 = derive_table(FORWARDS); rt2 = derive_table(FORWARDS)
    worksheet["reparse_byte_identical"] = (rt1 == rt2)
    log("deterministic re-read x2 byte-identical: %s" % (rt1 == rt2))
    if rt1 != rt2:
        run["verdict"] = "RUN-INVALID (re-read mismatch; apparatus bug)"
        finalize(run, worksheet); return

    # --- baseline-arm variation gate (§3.8) ---
    base_readouts = [it["readout_base"] for it in per_item]
    distinct = len(set(base_readouts))
    minority = min(base_readouts.count(s) for s in set(base_readouts)) if set(base_readouts) else 0
    run["baseline_variation"] = {"distinct": distinct, "minority": minority}
    log("baseline-arm variation: distinct=%d minority=%d (gate: <2 distinct or minority<3 -> RUN-INVALID)"
        % (distinct, minority))
    if not (distinct >= 2 and minority >= 3):
        run["verdict"] = "RUN-INVALID (baseline channel not discriminating)"
        finalize(run, worksheet); return

    # --- elicitation-failure gate: n_valid >= 48/60 ---
    valid_items = [it for it in per_item if it["valid"]]
    n_valid = len(valid_items)
    run["n_valid"] = n_valid
    log("n_valid = %d/60 (gate: <48 -> RUN-INVALID)" % n_valid)
    if n_valid < 48:
        run["verdict"] = "RUN-INVALID (elicitation-failure gate: n_valid=%d < 48)" % n_valid
        finalize(run, worksheet); return

    # --- record-keeping: handled canonically in finalize() (defect class 2):
    # raw artifacts are persisted + hash-pinned on every exit path before the
    # verdict is written. No separate inline persist needed here. ---

    # --- paired McNemar one-sided on (b, c), correctness vs tuple[0] (Law #7: metric time only) ---
    b = c = 0
    for it in valid_items:
        target = items[it["item"]]["tuple"][0]   # Law #7: ground truth ONLY at metric time
        plan_entity = items[it["item"]]["E1"] if it["readout_plan"] == "E1" else items[it["item"]]["E2"]
        base_entity = items[it["item"]]["E1"] if it["readout_base"] == "E1" else items[it["item"]]["E2"]
        plan_correct = plan_entity == target
        base_correct = base_entity == target
        it["pipeline_correct"] = plan_correct
        it["baseline_correct"] = base_correct
        if plan_correct and not base_correct:
            b += 1
        elif base_correct and not plan_correct:
            c += 1
    p_val, n_pairs = mcnemar_one_sided(b, c)   # executor-computed; the script prints it (defect class 1)
    net = b - c
    run["mcnemar"] = {"b": b, "c": c, "n": n_pairs, "net": net, "one_sided_p": p_val}
    run["items"] = per_item
    log("McNemar: b=%d (plan fixes), c=%d (plan breaks), n=%d, net=%+d, one-sided p=%.8f [executor-computed]"
        % (b, c, n_pairs, net, p_val))
    if p_val <= 0.05 and b > c:
        run["verdict"] = "CONTINUE (McNemar one-sided p=%.5f <= 0.05, b=%d > c=%d)" % (p_val, b, c)
    elif net <= 0:
        run["verdict"] = "KILL (net b-c=%d <= 0)" % net
    else:
        run["verdict"] = "HELD (net=%d > 0 but p=%.5f > 0.05)" % (net, p_val)

    finalize(run, worksheet)

def persist_precheck(precheck):
    """Persist the Phase 0-pre tokenizer pre-check record (no model contact yet)."""
    path = os.path.join(OUTDIR, "exp121_precheck.json")
    with open(path, "w") as f:
        json.dump(precheck, f, indent=2, default=str)

def persist_raw_artifacts(generations, forwards, precheck, per_item):
    """Record-keeping gate (defect class 2): persist all raw records before the verdict."""
    paths = {}
    for name, obj in (("generations", generations), ("forwards", forwards),
                      ("precheck", precheck), ("per_item", per_item)):
        path = os.path.join(OUTDIR, "exp121_%s.json" % name)
        with open(path, "w") as f:
            json.dump(obj, f, indent=2, default=str)
        paths[name] = path
    # the execute script itself is a raw artifact
    paths["execute_script"] = os.path.join(OUTDIR, "exp121_execute.py")
    with open(paths["execute_script"], "w") as f:
        with open(SCRIPT_PATH) as src:
            f.write(src.read())
    return paths

def finalize(run, worksheet):
    # Record-keeping backstop (defect class 2): persist + hash-pin ALL raw
    # records on EVERY exit path, before the verdict is written. A missing
    # artifact forces RUN-INVALID (the verdict is never written unbacked).
    raw = {"generations": GENERATIONS, "forwards": FORWARDS}
    pre = run.get("phases", {}).get("phase0_precheck")
    if pre is not None:
        raw["precheck"] = pre
    if run.get("items"):
        raw["per_item"] = run["items"]
    hashes = {}
    for name, obj in raw.items():
        path = os.path.join(OUTDIR, "exp121_%s.json" % name)
        with open(path, "w") as f:
            json.dump(obj, f, indent=2, default=str)
        hashes[name] = sha256_file(path)
        if not os.path.exists(path) or os.path.getsize(path) == 0:
            run["verdict"] = "RUN-INVALID (record-keeping gate: artifact %s missing/empty)" % name
    script_copy = os.path.join(OUTDIR, "exp121_execute.py")
    with open(script_copy, "w") as f:
        with open(SCRIPT_PATH) as src:
            f.write(src.read())
    hashes["execute_script"] = sha256_file(script_copy)
    worksheet["artifact_hashes"] = hashes
    run["worksheet"] = worksheet
    run["completed_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    with open(os.path.join(OUTDIR, "exp121_result.json"), "w") as f:
        json.dump(run, f, indent=2, default=str)
    with open(os.path.join(OUTDIR, "exp121_stdout.log"), "w") as f:
        f.write("\n".join(log_lines) + "\n")
    log("FINAL VERDICT: %s" % run["verdict"])

if __name__ == "__main__":
    t_start = time.time()
    main()
    print("wall time: %.1f min" % ((time.time() - t_start) / 60.0), flush=True)
