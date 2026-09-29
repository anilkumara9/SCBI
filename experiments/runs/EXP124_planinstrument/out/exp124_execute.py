#!/usr/bin/env python3
"""EXP124 (H21/PLAN-INSTRUMENT) execution lane — LOG-4670 pre-assigned.
Pre-registration: research/prereg/EXP_PREREG_H21_PLANINSTRUMENT_2026-09-29.md
(signed: Law #14 SIGN-WITH-FIXES LOG-4668, FIX-1/2/3 byte-verified LOG-4669).
$0 CPU. Frozen backbone (Delta theta = 0). Zero training. No improvisation —
the script implements the pre-reg exactly; the falsification-tree order (§5)
is mirrored in code; the metric is read only AFTER all guards pass (Law #9).
Law #7: bench ground truth (tuple[0]) is used ONLY at metric time.
Defect classes pinned: executor-computed p-values only; raw records
hash-pinned before the verdict; FIX-1 label-pin discipline; no reuse of
EXP117's §3.7; the [-3:] identity pin; single-token entities (H18);
per-item G1 as construction-time filter only (EXP121 class-6).
"""
import json, math, hashlib, os, sys, time

OUTDIR = os.path.expanduser("~/workspace/SCBI/experiments/runs/EXP124_planinstrument/out")
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
TAIL_TOKENS = [32, 37741, 27]  # '?', 'ĠAnswer', ':'
PROBE_ITEMS = [0, 1, 2, 5, 6, 7, 8, 9, 10, 11]  # items 3-4 excluded (planner exemplars)
SEED = 0
RNG_SEED = 20260929  # random-variant draw (EXP120 convention)
G1_FLOOR = 0.01

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

# ---------------- §3.3 planner spec — T2-P2 byte-verbatim (H19 §3.3) ----------------
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
    build_prompts: t2p2_parts + final join), applied to this bench — the
    reference EXP121 used for the same byte-identity check."""
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
    """§3.3 pinned (EXP113 §3.4): first-occurrence positions of 1.–4.;
    each marker in position order → substring to next marker in position order
    (or end), stripped; drop empties and exact duplicates → L in position order."""
    markers = ["1.", "2.", "3.", "4."]
    first_pos = {m: output.find(m) for m in markers}
    occ = sorted((p, m) for m, p in first_pos.items() if p != -1)
    L, seen = [], set()
    for order, (p, m) in enumerate(occ):
        start = p + len(m)
        end = occ[order + 1][0] if order + 1 < len(occ) else len(output)
        o = output[start:end].strip()
        if o and o not in seen:
            seen.add(o)
            L.append(o)
    return L

# ---------------- §3.4 choice extraction — pinned mechanical rule ----------------
def extract_choice(F, E1, E2):
    """Final-outline first-entity-mention rule, leftmost-longest, case-sensitive.
    Returns 'A-FIRST' | 'C-FIRST' | None (choice-invalid)."""
    matches = []
    for which, name in (("E1", E1), ("E2", E2)):
        start = 0
        while True:
            p = F.find(name, start)
            if p == -1:
                break
            matches.append((p, len(name), which))
            start = p + 1
    if not matches:
        return None
    best = min(matches, key=lambda m: (m[0], -m[1]))  # leftmost, then longest
    return "A-FIRST" if best[2] == "E1" else "C-FIRST"

# ---------------- §3.5 phrasing-swap (involutive, meaning-preserving) ----------------
def swap_templates(tpl):
    """Build the 4 forward/reverse premise template pairs from the tuple
    entities; return (forward, reverse) keyed by which form the bench premise
    takes. Raises ValueError if the premise matches no template (construction bug)."""
    A, B, C = tpl[0], tpl[1], tpl[2]
    D = tpl[3] if len(tpl) > 3 else None
    if len(tpl) == 3:
        fwd = {
            "o": "Premise: %s outranks %s. %s outranks %s." % (A, B, B, C),
            "l": "Premise: %s is lower than %s. %s is lower than %s." % (B, A, C, B),
        }
        rev = {
            "o": "Premise: %s outranks %s. %s outranks %s." % (B, C, A, B),
            "l": "Premise: %s is lower than %s. %s is lower than %s." % (C, B, B, A),
        }
    else:
        fwd = {
            "o": "Premise: %s outranks %s. %s outranks %s. %s outranks %s." % (A, B, B, C, C, D),
            "l": "Premise: %s is lower than %s. %s is lower than %s. %s is lower than %s." % (B, A, C, B, D, C),
        }
        rev = {
            "o": "Premise: %s outranks %s. %s outranks %s. %s outranks %s." % (C, D, B, C, A, B),
            "l": "Premise: %s is lower than %s. %s is lower than %s. %s is lower than %s." % (D, C, C, B, B, A),
        }
    return fwd, rev

def swap_premise(premise, tpl):
    """Pinned phrasing-swap §3.5: forward <-> reverse, word family fixed."""
    fwd, rev = swap_templates(tpl)
    for fam in ("o", "l"):
        if premise == fwd[fam]:
            return rev[fam]
        if premise == rev[fam]:
            return fwd[fam]
    raise ValueError("premise matches no pinned template (construction bug)")

def premise_is_a_first(premise, tpl):
    """The bench's own phrasing field says forward forms are A-first; the swap
    must flip the form. Independent check: forward template <=> A-first."""
    fwd, rev = swap_templates(tpl)
    for fam in ("o", "l"):
        if premise == fwd[fam]:
            return True
        if premise == rev[fam]:
            return False
    raise ValueError("premise matches no pinned template (construction bug)")

# ---------------- model-contact raw records (module-level so finalize can
# persist them on EVERY exit path — defect class 2) ----------------
GENERATIONS = []   # raw planner generation records
FORWARDS = []      # raw forward records (variant + choice arms)
# ---------------- main ----------------
def main():
    import torch, transformers
    import numpy as np
    run = {"verdict": None, "gates": {}, "phases": {}, "items": []}
    gen_exceptions = {"count": 0}
    fwd_exceptions = {"count": 0}

    # --- environment manifest (Law #13) ---
    torch.manual_seed(SEED); np.random.seed(SEED)
    torch.set_num_threads(2)
    import sklearn
    manifest = {
        "torch": torch.__version__, "transformers": transformers.__version__,
        "numpy": np.__version__, "sklearn": sklearn.__version__,
        "snapshot": SNAP,
        "torch_num_threads_set": 2, "torch_num_threads_readback": torch.get_num_threads(),
        "seeds": {"torch": SEED, "numpy": SEED, "random_arm_rng": RNG_SEED},
        "device": "cpu", "dtype": "float32", "device_map": "cpu",
        "generation": {"do_sample": False, "max_new_tokens": 160},
    }
    log("ENV: " + json.dumps(manifest))
    worksheet = {"experiment": "EXP124", "hypothesis": "H21/PLAN-INSTRUMENT", "lane": "LOG-4670",
                 "prereg": "research/prereg/EXP_PREREG_H21_PLANINSTRUMENT_2026-09-29.md (LOG-4668 SIGN-WITH-FIXES, LOG-4669 FIX-1/2/3 byte-verified)",
                 "environment": manifest,
                 "pins": {"npz": NPZ_PIN, "embeddings_bytes": EMB_BYTES_PIN,
                          "ids_bytes": IDS_BYTES_PIN, "bench": BENCH_PIN,
                          "backbone_pin_expected": WEIGHTS_PIN,
                          "question_suffix_tail_tokens": TAIL_TOKENS}}

    def finalize():
        """Persist whatever raw records exist; called on EVERY exit path
        (defect class 2: artifacts must exist before any verdict is read)."""
        with open(os.path.join(OUTDIR, "exp124_console.log"), "w") as f:
            f.write("\n".join(log_lines) + "\n")
        with open(os.path.join(OUTDIR, "exp124_generations.json"), "w") as f:
            json.dump(GENERATIONS, f)
        with open(os.path.join(OUTDIR, "exp124_forwards.json"), "w") as f:
            json.dump(FORWARDS, f)
        with open(os.path.join(OUTDIR, "exp124_run.json"), "w") as f:
            json.dump(run, f, indent=1)
        with open(os.path.join(OUTDIR, "exp124_worksheet.json"), "w") as f:
            json.dump(worksheet, f, indent=1)
        pins = {n: sha256_file(os.path.join(OUTDIR, n)) for n in
                ("exp124_console.log", "exp124_generations.json",
                 "exp124_forwards.json", "exp124_run.json", "exp124_worksheet.json")}
        with open(os.path.join(OUTDIR, "exp124_artifact_pins.json"), "w") as f:
            json.dump(pins, f, indent=1)
        log("artifact pins: " + json.dumps(pins))

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

    # --- §3.1 bench build + provenance pin + schema + decomposition assertions ---
    sys.path.insert(0, BUILDER_DIR)
    import build_exp107_bench as b
    bench = b.build_bench()
    assert len(bench) == 60, "bench len != 60"
    canon = json.dumps(bench, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    assert sha256_bytes(canon.encode("utf-8")) == BENCH_PIN, "bench pin MISMATCH"
    bench_ids = np.array([it["id"] for it in bench])
    assert (bench_ids == ids).all(), "bench ids vs npz ids mismatch"
    phr = [it["phrasing"] for it in bench]
    assert phr.count("A-first") == 30 and phr.count("C-first") == 30, "phrasing 30/30 broken"
    for it in bench:
        assert all(k in it for k in ("prompt", "premise", "tuple", "phrasing", "id")), "schema key missing"
        assert len(it["tuple"]) >= 2, "tuple len < 2"
        assert it["prompt"] == it["premise"] + QUESTION_SUFFIX, "decomposition assertion failed (§3.5)"
    log("bench pin OK: 60 items; schema + decomposition + phrasing 30/30 pass (§3.1/§3.5)")

    # --- archived EXP112 readout column + pinned token ids (§3.6, defect class 6) ---
    arch = json.load(open(EXP112_PER_ITEM))
    assert len(arch) == 60, "archived readout column len != 60"
    arch_readout = {r["id"]: r["readout"] for r in arch}
    arch_t = {r["id"]: (r["t1"], r["t2"]) for r in arch}
    log("archived EXP112 readout column loaded: 60 records")

    # --- tokenizer (tokenizer-only; NOT model contact) ---
    tok = transformers.AutoTokenizer.from_pretrained(SNAP, local_files_only=True, trust_remote_code=False)
    if tok.pad_token_id is None:
        tok.pad_token_id = tok.eos_token_id

    # --- token-id pin check vs EXP112 archive (defect class 6: pin carries over) ---
    items = []
    for it in bench:
        E1, E2 = it["tuple"][0], it["tuple"][-1]
        assert E1 != E2, "E1 == E2 on item %s" % it["id"]
        i1 = tok.encode(" " + E1); i2 = tok.encode(" " + E2)
        assert len(i1) == 1 and len(i2) == 1, "BPE single-token pin drift on item %s" % it["id"]
        t1, t2 = i1[0], i2[0]
        at1, at2 = arch_t[it["id"]]
        if not (t1 == at1 and t2 == at2):
            run["verdict"] = "RUN-INVALID (token-id drift vs EXP112 worksheet pin on item %s)" % it["id"]
            finalize(); return
        items.append({"id": it["id"], "prompt": it["prompt"], "premise": it["premise"],
                      "tuple": it["tuple"], "phrasing": it["phrasing"],
                      "E1": E1, "E2": E2, "t1": t1, "t2": t2})
    log("token-id pin check vs EXP112 archive: 60/60 single-token, ids match")

    # --- §3.5 variant construction (construction time; no model contact, no RNG) ---
    for t, rec in enumerate(items):
        try:
            swapped = swap_premise(rec["premise"], rec["tuple"])
        except ValueError as e:
            run["verdict"] = "RUN-INVALID (variant construction bug on item %d: %s)" % (t, e)
            finalize(); return
        # involution check: SWAP(SWAP(P)) == P
        try:
            if swap_premise(swapped, rec["tuple"]) != rec["premise"]:
                run["verdict"] = "RUN-INVALID (SWAP involution failed on item %d)" % t
                finalize(); return
        except ValueError as e:
            run["verdict"] = "RUN-INVALID (SWAP involution construction bug on item %d: %s)" % (t, e)
            finalize(); return
        v_own = rec["prompt"]                      # == premise + QUESTION_SUFFIX (asserted)
        v_other = swapped + QUESTION_SUFFIX
        # variant labels: forward template form == A-first (verified vs bench field)
        own_a_first = premise_is_a_first(rec["premise"], rec["tuple"])
        assert own_a_first == (rec["phrasing"] == "A-first"), "phrasing-label inconsistency item %d" % t
        if rec["phrasing"] == "A-first":
            v_a, v_c = v_own, v_other
        else:
            v_a, v_c = v_other, v_own
        rec.update({"V_own": v_own, "V_other": v_other, "V_A": v_a, "V_C": v_c,
                    "v_own_sha256": sha256_bytes(v_own.encode()),
                    "v_other_sha256": sha256_bytes(v_other.encode())})
    run["gates"]["variant_construction"] = {"swaps": 60, "involution": "60/60 pass",
                                            "labels": "V_A/V_C assigned, bench-phrasing consistent"}
    log("variant construction OK: 60/60 premises template-matched; SWAP involution 60/60; labels consistent")

    # --- Phase-0pre (§3.7): tokenizer-only [-3:] on all 120 variant contexts ---
    for t, rec in enumerate(items):
        for vname in ("V_A", "V_C"):
            tail = tok(rec[vname], return_tensors="pt")["input_ids"][0].tolist()[-3:]
            if tail != TAIL_TOKENS:
                run["verdict"] = ("RUN-INVALID (Phase-0pre: [-3:] tail mismatch on item %d variant %s: "
                                  "%s != %s; identity surface exists)" % (t, vname, tail, TAIL_TOKENS))
                finalize(); return
    run["phases"]["phase0pre"] = {"variant_contexts": 120, "identity": "120/120 pass"}
    log("Phase-0pre: [-3:] identity holds on 120/120 variant contexts (no model contact)")

    # --- backbone load + §3.1 pre-contact hash (Law #6) ---
    model = transformers.AutoModelForCausalLM.from_pretrained(
        SNAP, local_files_only=True, trust_remote_code=False,
        device_map="cpu", torch_dtype=torch.float32)
    model.eval()
    h_pre = state_dict_hash(model)
    log("backbone hash BEFORE: %s... (expect %s...)" % (h_pre[:16], WEIGHTS_PIN[:16]))
    if h_pre != WEIGHTS_PIN:
        run["verdict"] = "RUN-INVALID (backbone pin mismatch BEFORE; Law #6 quarantine)"
        finalize(); return
    worksheet["pins"]["backbone_pre"] = h_pre

    # --- §3.3 planner prompts + byte-identity check vs reference ---
    prompts = [planner_prompt(t, bench) for t in range(60)]
    mism = sum(1 for t in range(60) if prompts[t] != ref_t2p2(t, bench))
    worksheet["planner_prompt_byte_identity_mismatches"] = mism
    log("planner prompt byte-identity vs EXP113 T2-P2 reference: %d/60 mismatches" % mism)
    if mism > 0:
        run["verdict"] = "RUN-INVALID (planner prompt byte-identity apparatus bug)"
        finalize(); return

    # --- model-contact helpers ---
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
            gen_exceptions["count"] += 1
            text, exc = "", repr(e)
        rec = {"item_idx": t, "id": items[t]["id"],
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
            fwd_exceptions["count"] += 1
            side, tie, mass, exc = None, None, -1.0, repr(e)
            logits = None
        rec = {"arm": arm, "item_idx": t, "id": rec_item["id"],
               "context_sha256": sha256_bytes(context.encode("utf-8")),
               "readout_side": side, "readout_tie": tie, "mass": mass,
               "exception": exc,
               "logit_t1": None if logits is None else float(logits[t1]),
               "logit_t2": None if logits is None else float(logits[t2])}
        FORWARDS.append(rec)
        return rec

    def choice_of(output, rec_item):
        """§3.4 pinned choice extraction."""
        L = extract_outlines(output)
        if len(L) < 2:
            return None, L
        return extract_choice(L[-1], rec_item["E1"], rec_item["E2"]), L

    # --- Phase-0a (§3.7): planner choice-validity on 10 probe items ---
    n_cv0 = 0
    phase0a = {"probe_items": PROBE_ITEMS, "details": []}
    for t in PROBE_ITEMS:
        rec = generate(t, prompts[t])
        choice, L = choice_of(rec["output"], items[t]) if rec["exception"] is None else (None, [])
        cv = choice is not None
        n_cv0 += cv
        phase0a["details"].append({"item": t, "id": items[t]["id"], "choice": choice,
                                  "n_outlines": len(L), "choice_valid": cv})
    run["phases"]["phase0a"] = phase0a
    run["gates"]["phase0a"] = {"choice_valid": n_cv0, "of": 10}
    log("Phase-0a: planner choice-validity %d/10" % n_cv0)
    if n_cv0 < 8:
        run["verdict"] = "RUN-INVALID (Phase-0a: choice-valid %d/10 < 8; elicitation failure)" % n_cv0
        finalize(); return

    # --- Phase-0b (§3.7): variant discriminability + channel G1 ---
    n_diff = 0
    mA = mC = 0.0
    phase0b = {"probe_items": PROBE_ITEMS, "details": []}
    for t in PROBE_ITEMS:
        rec_item = items[t]
        fa = forward("probe_A", t, rec_item["V_A"], rec_item)
        fc = forward("probe_C", t, rec_item["V_C"], rec_item)
        if fa["mass"] < G1_FLOOR or fc["mass"] < G1_FLOOR:
            run["verdict"] = "RUN-INVALID (Phase-0b: channel G1 degenerate on probe item %d)" % t
            finalize(); return
        diff = (fa["readout_side"] != fc["readout_side"])
        n_diff += diff
        mA += fa["mass"]; mC += fc["mass"]
        phase0b["details"].append({"item": t, "id": rec_item["id"],
                                  "side_A": fa["readout_side"], "side_C": fc["readout_side"],
                                  "differ": bool(diff), "mass_A": fa["mass"], "mass_C": fc["mass"]})
    mA /= len(PROBE_ITEMS); mC /= len(PROBE_ITEMS)
    run["phases"]["phase0b"] = phase0b
    run["gates"]["phase0b"] = {"differing_items": n_diff, "of": 10, "M_A": mA, "M_C": mC}
    log("Phase-0b: discriminability %d/10 differ; M_A=%.5f M_C=%.5f" % (n_diff, mA, mC))
    if n_diff < 3:
        run["verdict"] = "RUN-INVALID (Phase-0b: variant discriminability %d/10 < 3)" % n_diff
        finalize(); return
    if mA < G1_FLOOR or mC < G1_FLOOR:
        run["verdict"] = "RUN-INVALID (Phase-0b: channel G1 below floor)"
        finalize(); return
    # --- full run (§3.8): 60 planner generations + choice extraction (fresh) ---
    n_valid = 0
    n_a = n_c = 0
    choices = []  # per item: 'A-FIRST' | 'C-FIRST' | None
    for t in range(60):
        rec = generate(t, prompts[t])
        choice, L = choice_of(rec["output"], items[t]) if rec["exception"] is None else (None, [])
        choices.append(choice)
        cv = choice is not None
        n_valid += cv
        n_a += (choice == "A-FIRST"); n_c += (choice == "C-FIRST")
        run["items"].append({"item_idx": t, "id": items[t]["id"], "choice": choice,
                             "n_outlines": len(L), "choice_valid": cv})
    run["gates"]["full_run"] = {"n_valid": n_valid, "of": 60,
                                "A-FIRST": n_a, "C-FIRST": n_c,
                                "gen_exceptions": gen_exceptions["count"]}
    log("full run: 60/60 generations; choice-valid %d/60 (A-FIRST=%d, C-FIRST=%d); gen exceptions %d"
        % (n_valid, n_a, n_c, gen_exceptions["count"]))
    if gen_exceptions["count"] > 6:  # >10% of the 60 generation contacts
        run["verdict"] = "RUN-INVALID (>10%% per-contact exceptions on generations: %d)" % gen_exceptions["count"]
        finalize(); return

    # --- choice-information gate (a): each phrasing chosen >= 12 ---
    if n_a < 12 or n_c < 12:
        run["verdict"] = ("RUN-INVALID (choice-information gate: A-FIRST=%d C-FIRST=%d; "
                          "each must be >= 12; decision-inert control)" % (n_a, n_c))
        finalize(); return
    log("choice-information gate PASS: A-FIRST=%d C-FIRST=%d (both >= 12)" % (n_a, n_c))

    # --- 120 variant forwards (§3.8) + per-item G1 invariant ---
    vrec = {}  # (t, 'A'|'C') -> forward record
    for t in range(60):
        rec_item = items[t]
        fa = forward("variant_A", t, rec_item["V_A"], rec_item)
        fc = forward("variant_C", t, rec_item["V_C"], rec_item)
        vrec[(t, "A")] = fa; vrec[(t, "C")] = fc
        if fa["mass"] < G1_FLOOR or fc["mass"] < G1_FLOOR or fa["exception"] or fc["exception"]:
            run["verdict"] = ("RUN-INVALID (full-run G1 invariant: degenerate forward on item %d "
                              "(mass_A=%s, mass_C=%s))" % (t, fa["mass"], fc["mass"]))
            finalize(); return
    log("120 variant forwards complete; per-item G1 invariant holds on all 120")

    # --- backbone pin (post, Law #6) ---
    h_post = state_dict_hash(model)
    log("backbone hash AFTER: %s... (expect %s...)" % (h_post[:16], WEIGHTS_PIN[:16]))
    if h_post != WEIGHTS_PIN:
        run["verdict"] = "RUN-INVALID (backbone pin mismatch AFTER; Law #6 quarantine)"
        finalize(); return
    worksheet["pins"]["backbone_post"] = h_post

    # --- baseline-reproduction integrity check: V_own readouts vs EXP112 archived 60/60 ---
    mism = 0
    for t in range(60):
        rec_item = items[t]
        own = vrec[(t, "A")] if rec_item["phrasing"] == "A-first" else vrec[(t, "C")]
        got = "E1" if own["readout_side"] == "E1" else "E2"
        want = arch_readout[rec_item["id"]]
        if got != want:
            mism += 1
            log("  reproduction mismatch item %d id=%s: got %s want %s" % (t, rec_item["id"], got, want))
    run["gates"]["baseline_reproduction"] = {"matches": 60 - mism, "of": 60}
    log("baseline reproduction: V_own readouts vs EXP112 archived: %d/60 match" % (60 - mism))
    if mism > 0:
        run["verdict"] = "RUN-INVALID (baseline reproduction %d/60 != 60/60; apparatus drift)" % (60 - mism)
        finalize(); return

    # --- 60 choice-arm forwards (§3.8) + determinism cross-check ---
    crec = {}  # t -> choice-arm forward record (choice-valid items only)
    for t in range(60):
        if choices[t] is None:
            continue
        rec_item = items[t]
        arm_key = "A" if choices[t] == "A-FIRST" else "C"
        ch = forward("choice", t, rec_item["V_%s" % arm_key], rec_item)
        crec[t] = ch
        vr = vrec[(t, arm_key)]
        if ch["mass"] < G1_FLOOR or ch["exception"]:
            run["verdict"] = "RUN-INVALID (choice-arm degenerate forward on item %d)" % t
            finalize(); return
        if not (ch["logit_t1"] == vr["logit_t1"] and ch["logit_t2"] == vr["logit_t2"]):
            run["verdict"] = ("RUN-INVALID (determinism cross-check failed on item %d: choice-forward "
                              "logits differ from variant forward)" % t)
            finalize(); return
    log("choice-arm forwards complete: %d/%d; determinism cross-check byte-identical on all" % (len(crec), n_valid))

    # --- raw records persisted + hash-pinned BEFORE any verdict (defect class 2) ---
    finalize()
    for n in ("exp124_generations.json", "exp124_forwards.json"):
        assert os.path.exists(os.path.join(OUTDIR, n)), "artifact-existence gate: %s missing" % n
    log("raw records persisted: %d generations, %d forwards; hash-pinned before verdict"
        % (len(GENERATIONS), len(FORWARDS)))
    assert len(GENERATIONS) == 70 and len(FORWARDS) == 20 + 120 + n_valid, \
        "raw-record count gate failed (%d, %d)" % (len(GENERATIONS), len(FORWARDS))

    # --- metric read (Law #7: ground truth only here; Law #9: after all guards) ---
    rng = np.random.default_rng(RNG_SEED)
    table = []  # per choice-valid item: (choice_correct, random_correct)
    random_draws = {}
    for t in range(60):
        u = rng.random()
        variant = "A" if u < 0.5 else "C"
        random_draws[t] = {"u": float(u), "variant": variant}
    for t in range(60):
        if choices[t] is None:
            continue
        rec_item = items[t]
        target = rec_item["E1"]  # tuple[0]; Law #7 — metric time only
        arm_key = "A" if choices[t] == "A-FIRST" else "C"
        ch_side = crec[t]["readout_side"]
        choice_ent = rec_item["E1"] if ch_side == "E1" else rec_item["E2"]
        choice_correct = (choice_ent == target)
        rv = vrec[(t, random_draws[t]["variant"])]
        rand_ent = rec_item["E1"] if rv["readout_side"] == "E1" else rec_item["E2"]
        random_correct = (rand_ent == target)
        table.append({"item_idx": t, "id": rec_item["id"], "choice": choices[t],
                      "random_variant": random_draws[t]["variant"],
                      "choice_correct": bool(choice_correct),
                      "random_correct": bool(random_correct)})
    b = sum(1 for r in table if r["choice_correct"] and not r["random_correct"])
    c = sum(1 for r in table if not r["choice_correct"] and r["random_correct"])
    d = b + c

    # --- deterministic re-read x2 (pinned pure function of raw logs; byte-identical) ---
    def analyze(gens, fwds):
        G = {r["item_idx"]: r for r in gens}
        out = []
        for it in run["items"]:
            t = it["item_idx"]
            g = G[t]
            ch, L = choice_of(g["output"], items[t]) if g["exception"] is None else (None, [])
            out.append({"item_idx": t, "choice": ch, "n_outlines": len(L)})
        return json.dumps(out, sort_keys=True)
    reread1 = analyze(GENERATIONS, FORWARDS)
    reread2 = analyze(GENERATIONS, FORWARDS)
    assert reread1 == reread2, "deterministic re-read mismatch"
    # cross-check re-read reproduces the live choices byte-identically
    live = json.dumps([{"item_idx": it["item_idx"], "choice": it["choice"],
                        "n_outlines": it["n_outlines"]} for it in run["items"]], sort_keys=True)
    assert reread1 == live, "re-read vs live-run choice mismatch"
    log("deterministic re-read x2: byte-identical; matches live run")

    # --- executor-computed McNemar one-sided exact p (defect class 1) ---
    p, dd = mcnemar_one_sided(b, c)
    assert dd == d
    log("MCNEMAR_ONE_SIDED_P = %.10f (b=%d, c=%d, d=%d)" % (p, b, c, d))
    run["metric"] = {"b": b, "c": c, "d": d, "p_one_sided": p,
                     "decision_table": table, "random_draws": {str(k): v for k, v in random_draws.items()}}
    worksheet["pins"].update({"generations_pin": sha256_file(os.path.join(OUTDIR, "exp124_generations.json")),
                              "forwards_pin": sha256_file(os.path.join(OUTDIR, "exp124_forwards.json"))})

    # --- §4 decision bars ---
    if p < 0.05 and d >= 10:
        run["verdict"] = "CONTINUE"
    elif p >= 0.05 and d >= 40:
        run["verdict"] = "KILL"
    else:
        run["verdict"] = "HELD"
    log("VERDICT = %s (b=%d, c=%d, d=%d, p=%.10f)" % (run["verdict"], b, c, d, p))
    worksheet["verdict"] = run["verdict"]
    worksheet["verdict_reason"] = ("p<0.05 & d>=10 -> CONTINUE; p>=0.05 & d>=40 -> KILL; else HELD "
                                   "(incl. p<0.05 & d<10 gap-fill)")
    # re-persist run + worksheet with the verdict (raw records unchanged)
    with open(os.path.join(OUTDIR, "exp124_run.json"), "w") as f:
        json.dump(run, f, indent=1)
    with open(os.path.join(OUTDIR, "exp124_worksheet.json"), "w") as f:
        json.dump(worksheet, f, indent=1)
    pins = json.load(open(os.path.join(OUTDIR, "exp124_artifact_pins.json")))
    for n in ("exp124_run.json", "exp124_worksheet.json"):
        pins[n] = sha256_file(os.path.join(OUTDIR, n))
    with open(os.path.join(OUTDIR, "exp124_artifact_pins.json"), "w") as f:
        json.dump(pins, f, indent=1)
    with open(os.path.join(OUTDIR, "exp124_stdout.log"), "w") as f:
        f.write("\n".join(log_lines) + "\n")
    log("done: verdict %s" % run["verdict"])

if __name__ == "__main__":
    main()
