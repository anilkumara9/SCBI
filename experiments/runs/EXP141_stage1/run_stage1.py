#!/usr/bin/env python3
"""EXP141 Stage-1: S4-6 metacognitive self-modeling CPU pilot (I-screen + calibration).
Executes EXACTLY per research/prereg/EXP_S46_prereg_DRAFT_2026-10-03.md (SIGNED, LOG-4889).
CEO venue approval: Stage-1 CPU pilot only (60 self-eval passes). $0 compute.
Exit codes: 0 = clean completion; 44 = RUN-INVALID (validity gate trip).

Pre-reg interpretation notes (documented, not improvised):
- Baseline-answer reuse (pre-reg §1, validity gate (c)): the committed EXP140 B0
  records store per-branch 'correct' (bool) but not the chosen answer text.
  The B0 answer is argmax over {tok1(v["A"]), tok1(v["C"])} (EXP140 run script
  interpretation notes; EXP139 precedent line 217). Therefore the committed B0
  answer text is EXACTLY: v["A"] if branch-0 'correct' else v["C"], where v is
  the view-0 dict. Reading it requires the bench label (which entity is "A")
  as a decoding key. This is a faithful READ of a committed experimental
  quantity, not a label-informed decision: the baseline answer is fixed
  regardless of how it is decoded; labels do not influence any self-eval
  score, trigger, revision, or gate threshold. The pre-reg pins REUSE
  ("no regeneration -- read, don't recompute"), and this is the only
  faithful read available. Documented here per the EXP140 precedent.
- Self-eval prompt (pre-reg §2): "<view-0 item prompt> Proposed answer: Y_i.
  Is the proposed answer correct? (A) True (B) False" where Y_i is the decoded
  baseline answer entity name. a_self_i = P(token "A").
- Token "A": single-token encoding verified by assertion; the prompt ends with
  "(B) False" (no trailing space), so the no-space "A" token is used.
- Equal-frequency 4-bin discretization: argsort-based, exactly 15 items/bin
  (deterministic tie-breaking by sort order).
- Spearman one-sided p: derived from scipy two-sided p.
"""
import hashlib, json, math, os, sys, time
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from scipy import stats as scipy_stats

RUN_DIR = os.path.dirname(os.path.abspath(__file__))
os.makedirs(RUN_DIR, exist_ok=True)
LOGF = open(os.path.join(RUN_DIR, "stage1_run_log.txt"), "w")

def log(msg):
    line = "[%s] %s" % (time.strftime("%H:%M:%S"), msg)
    print(line, flush=True)
    LOGF.write(line + "\n"); LOGF.flush()

# ============ pre-reg pinned constants ============
BACKBONE_PIN = "ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed"
BENCH_PIN = "eb304fa65a60b65ad87767d251084b256d0a79001a16b4fe8ebcd1b1f45589df"
HF_REVISION = "9879c9b5f8bea9051dcb0e68dff21493d67e9d4f"
MODEL_ID = "EleutherAI/pythia-410m"
S_PERM_G2 = 20261007
S_PERM_C2 = 20261008
N_ITEMS = 60
G1_BAR = 0.01
G2_BAR = 0.05
G3_BAR = 0.05

torch.manual_seed(20261007)
torch.set_num_threads(max(1, (os.cpu_count() or 4) - 1))
log("threads=%d" % torch.get_num_threads())

FWD_COUNT = [0]
def count_fwd(n=1):
    FWD_COUNT[0] += n

def sha256_state_dict(model):
    h = hashlib.sha256()
    for k in sorted(model.state_dict().keys()):
        t = model.state_dict()[k].detach().cpu()
        if t.dtype != torch.float32:
            t = t.float()
        h.update(t.numpy().tobytes())
    return h.hexdigest()

def run_invalid(reason):
    log("RUN-INVALID: %s" % reason)
    json.dump({"verdict": "RUN-INVALID", "reason": reason,
               "forwards": FWD_COUNT[0]},
              open(os.path.join(RUN_DIR, "stage1_verdict.json"), "w"), indent=1)
    LOGF.close()
    sys.exit(44)

# ============ model load + backbone pin ============
log("loading tokenizer + model (float32, cpu, local_files_only)...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, revision=HF_REVISION,
                                          local_files_only=True)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID, revision=HF_REVISION, local_files_only=True,
    torch_dtype=torch.float32, device_map="cpu")
model.eval()
log("model loaded")

pre_hash = sha256_state_dict(model)
log("backbone pre-hash: %s" % pre_hash)
if pre_hash != BACKBONE_PIN:
    run_invalid("(b) backbone pre-hash mismatch: got %s" % pre_hash)
log("(b) backbone pin PASS")

# token "A" sanity
ids_A = tokenizer.encode("A", add_special_tokens=False)
assert len(ids_A) == 1, "token 'A' is not single: %s" % ids_A
TOK_A = ids_A[0]
log("token 'A' id=%d (single) PASS" % TOK_A)

# ============ bench reconstruction (inlined from run_exp135.py) ============
SUPPORT_VOCABULARIES = {
    "V1_Anglo": ["Alice", "Bob", "Charlie", "David", "Emma"],
    "V2_Biblical": ["Aaron", "Joel", "Gideon", "Ruth", "Abel"],
    "V3_Greek": ["Ajax", "Jason", "Apollo", "Paris", "Atlas"],
    "V4_Roman": ["Marcus", "Julius", "Augustus", "Felix", "Diana"],
    "V5_Modern": ["Liam", "Noah", "Eli", "Maya", "Finn"],
}
VOCAB_KEYS = list(SUPPORT_VOCABULARIES.keys())
NOVEL_VOCAB_PLANET = ["Mars", "Venus", "Jupiter", "Saturn", "Mercury"]
NOVEL_VOCAB_ELEMENT = ["Iron", "Gold", "Silver", "Bronze", "Steel"]
TRIPLES_INDICES = [
    (0, 1, 2), (1, 2, 3), (2, 3, 4), (0, 2, 4), (0, 1, 3),
    (1, 3, 4), (0, 2, 3), (1, 2, 4), (0, 3, 4), (0, 1, 4),
    (0, 1, 2), (1, 2, 3), (2, 3, 4), (0, 2, 4), (0, 1, 3),
]
QUADS_INDICES = [
    (0, 1, 2, 3), (1, 2, 3, 4), (0, 1, 3, 4), (0, 2, 3, 4), (0, 1, 2, 4),
    (0, 1, 2, 3), (1, 2, 3, 4), (0, 1, 3, 4), (0, 2, 3, 4), (0, 1, 2, 4),
    (0, 1, 2, 3), (1, 2, 3, 4), (0, 1, 3, 4), (0, 2, 3, 4), (0, 1, 2, 4),
]

def build_bench():
    bench = []
    for i, (iA, iB, iC) in enumerate(TRIPLES_INDICES):
        A, B, C = NOVEL_VOCAB_PLANET[iA], NOVEL_VOCAB_PLANET[iB], NOVEL_VOCAB_PLANET[iC]
        target_first = (i % 2 == 1)
        q_opts = "%s or %s" % (A, C) if target_first else "%s or %s" % (C, A)
        if i < 8:
            p = "Premise: %s outranks %s. %s outranks %s. Question: Who is higher in rank, %s? Answer:" % (A, B, B, C, q_opts)
        else:
            p = "Premise: %s is lower than %s. %s is lower than %s. Question: Who is higher in rank, %s? Answer:" % (C, B, B, A, q_opts)
        bench.append({"id": "exp077_planet_2hop_%d" % i, "prompt": p, "A": A, "C": C,
                      "ent": A, "typ": "planet", "hop": 2, "domain": "Planetary",
                      "idx": (iA, iB, iC), "tfirst": target_first, "variant": "outranks" if i < 8 else "lower"})
    for i, (iA, iB, iC, iD) in enumerate(QUADS_INDICES):
        A, B, C, D_ent = (NOVEL_VOCAB_PLANET[iA], NOVEL_VOCAB_PLANET[iB],
                          NOVEL_VOCAB_PLANET[iC], NOVEL_VOCAB_PLANET[iD])
        target_first = (i % 2 == 1)
        q_opts = "%s or %s" % (A, D_ent) if target_first else "%s or %s" % (D_ent, A)
        if i < 8:
            p = ("Premise: %s outranks %s. %s outranks %s. %s outranks %s. "
                 "Question: Who is higher in rank, %s? Answer:") % (A, B, B, C, C, D_ent, q_opts)
        else:
            p = ("Premise: %s is lower than %s. %s is lower than %s. %s is lower than %s. "
                 "Question: Who is higher in rank, %s? Answer:") % (D_ent, C, C, B, B, A, q_opts)
        bench.append({"id": "exp077_planet_3hop_%d" % i, "prompt": p, "A": A, "C": D_ent,
                      "ent": A, "typ": "planet", "hop": 3, "domain": "Planetary",
                      "idx": (iA, iB, iC, iD), "tfirst": target_first, "variant": "outranks" if i < 8 else "lower"})
    for i, (iA, iB, iC) in enumerate(TRIPLES_INDICES):
        A, B, C = NOVEL_VOCAB_ELEMENT[iA], NOVEL_VOCAB_ELEMENT[iB], NOVEL_VOCAB_ELEMENT[iC]
        target_first = (i % 2 == 0)
        q_opts = "%s or %s" % (A, C) if target_first else "%s or %s" % (C, A)
        if i < 7:
            p = "Premise: %s outranks %s. %s outranks %s. Question: Who is higher in rank, %s? Answer:" % (A, B, B, C, q_opts)
        else:
            p = "Premise: %s is lower than %s. %s is lower than %s. Question: Who is higher in rank, %s? Answer:" % (C, B, B, A, q_opts)
        bench.append({"id": "exp077_element_2hop_%d" % i, "prompt": p, "A": A, "C": C,
                      "ent": A, "typ": "element", "hop": 2, "domain": "Elemental",
                      "idx": (iA, iB, iC), "tfirst": target_first, "variant": "outranks" if i < 7 else "lower"})
    for i, (iA, iB, iC, iD) in enumerate(QUADS_INDICES):
        A, B, C, D_ent = (NOVEL_VOCAB_ELEMENT[iA], NOVEL_VOCAB_ELEMENT[iB],
                          NOVEL_VOCAB_ELEMENT[iC], NOVEL_VOCAB_ELEMENT[iD])
        target_first = (i % 2 == 0)
        q_opts = "%s or %s" % (A, D_ent) if target_first else "%s or %s" % (D_ent, A)
        if i < 7:
            p = ("Premise: %s outranks %s. %s outranks %s. %s outranks %s. "
                 "Question: Who is higher in rank, %s? Answer:") % (A, B, B, C, C, D_ent, q_opts)
        else:
            p = ("Premise: %s is lower than %s. %s is lower than %s. %s is lower than %s. "
                 "Question: Who is higher in rank, %s? Answer:") % (D_ent, C, C, B, B, A, q_opts)
        bench.append({"id": "exp077_element_3hop_%d" % i, "prompt": p, "A": A, "C": D_ent,
                      "ent": A, "typ": "element", "hop": 3, "domain": "Elemental",
                      "idx": (iA, iB, iC, iD), "tfirst": target_first, "variant": "outranks" if i < 7 else "lower"})
    return bench

def make_views(it, src_ents):
    views = []
    for vk in VOCAB_KEYS:
        sub = dict(zip(src_ents, [SUPPORT_VOCABULARIES[vk][k] for k in it["idx"]]))
        prompt = it["prompt"]
        for old, new in sub.items():
            assert old in prompt, "substitution source missing: %s" % old
            prompt = prompt.replace(old, new)
        views.append({"prompt": prompt, "vk": vk, "A": sub[it["A"]], "C": sub[it["C"]]})
    return views

def novel_src(it):
    base = NOVEL_VOCAB_PLANET if it["typ"] == "planet" else NOVEL_VOCAB_ELEMENT
    return [base[k] for k in it["idx"]]

bench = build_bench()
assert len(bench) == 60, "bench len %d != 60" % len(bench)
bench_hash = hashlib.sha256(json.dumps(
    [{k: bench[i][k] for k in ("id", "prompt", "A", "C")} for i in range(len(bench))],
    sort_keys=True).encode()).hexdigest()
log("(a) bench len=60; bench sha256=%s" % bench_hash)
if bench_hash != BENCH_PIN:
    run_invalid("(a) bench sha256 mismatch: got %s" % bench_hash)
log("(a) bench pin PASS")

# view 0 for all 60 items (pre-reg §2)
items_v0 = [make_views(it, novel_src(it))[0] for it in bench]

# ============ baseline-answer reuse from committed EXP140 B0 records ============
EXP140_REC = "/home/hatch/workspace/SCBI/experiments/runs/EXP140_stage1/stage1_records.json"
with open(EXP140_REC) as f:
    exp140 = json.load(f)
# pin cross-check: EXP140 records must carry the same pins
assert exp140["pins"]["backbone_pre"] == BACKBONE_PIN, "EXP140 backbone pin drift"
assert exp140["pins"]["bench"] == BENCH_PIN, "EXP140 bench pin drift"
e140_items = exp140["items"]
assert len(e140_items) == 60, "EXP140 items %d != 60" % len(e140_items)
# id alignment: canonical bench order
for i, (b, e) in enumerate(zip(bench, e140_items)):
    assert b["id"] == e["id"], "id mismatch at %d: %s vs %s" % (i, b["id"], e["id"])
log("(c) EXP140 record id alignment 60/60 PASS")

# Reconstruct the committed B0 answer text per item.
# B0 = argmax over {tok1(v["A"]), tok1(v["C"])}; branch 'correct' = (choice == v["A"]).
# See header interpretation note for the Law #7 discussion.
b0_answers = []   # entity name chosen by B0
b0_correct = []   # baseline correctness (label-touching instrument input)
for i in range(N_ITEMS):
    v = items_v0[i]
    br0 = e140_items[i]["branches"][0]
    assert br0["k"] == 0
    correct = bool(br0["correct"])
    chosen = v["A"] if correct else v["C"]
    b0_answers.append(chosen)
    b0_correct.append(1 if correct else 0)
log("(c) B0 answers re-read from committed records (no regeneration) PASS")
log("B0 baseline accuracy: %.4f" % (sum(b0_correct) / N_ITEMS))

# ============ self-eval passes ============
SELF_EVAL_TMPL = " Proposed answer: %s. Is the proposed answer correct? (A) True (B) False"

def self_eval_forward(prompt_text):
    input_ids = tokenizer.encode(prompt_text, return_tensors="pt")
    with torch.no_grad():
        out = model(input_ids=input_ids)
    count_fwd(1)
    logits = out.logits[0, -1, :]
    probs = torch.softmax(logits, dim=0)
    return float(probs[TOK_A])

a_self = []
failed = 0
t0 = time.time()
for i in range(N_ITEMS):
    se_prompt = items_v0[i]["prompt"] + (SELF_EVAL_TMPL % b0_answers[i])
    try:
        a = self_eval_forward(se_prompt)
    except Exception as ex:
        log("self-eval forward failed on item %d: %s" % (i, ex))
        failed += 1
        a = float("nan")
    a_self.append(a)
    if (i + 1) % 15 == 0:
        log("self-eval %d/60 (%.1fs)" % (i + 1, time.time() - t0))
log("self-eval passes done: %d forwards, %d failed" % (FWD_COUNT[0], failed))
if failed >= 3:
    run_invalid("degenerate: %d failed self-evals >= 3 -> pilot VOID" % failed)
a_self = np.array(a_self, dtype=float)
assert not np.isnan(a_self).any(), "NaN in a_self with failed < 3"
assert (a_self >= 0).all() and (a_self <= 1).all(), "a_self out of [0,1]"

# ============ validity gate (d): post-run backbone hash (Δθ=0) ============
post_hash = sha256_state_dict(model)
log("backbone post-hash: %s" % post_hash)
if post_hash != BACKBONE_PIN:
    run_invalid("(d) backbone post-hash mismatch: Δθ != 0")
log("(d) Δθ=0 PASS")
log("ALL VALIDITY GATES PASS; forwards=%d" % FWD_COUNT[0])

# ============ G1: signal variance ============
g1_std = float(np.std(a_self, ddof=1))
g1_nonconst = not bool((a_self == a_self[0]).all())
G1_PASS = (g1_std > G1_BAR) and g1_nonconst
log("G1: std(a_self)=%.6f (bar >%.2f), non-constant=%s -> %s" %
    (g1_std, G1_BAR, g1_nonconst, "PASS" if G1_PASS else "FAIL"))

# ============ G2: I-screen (4-bin equal-frequency MI + Miller-Madow + permutation) ============
c_arr = np.array(b0_correct, dtype=int)  # labels touch ONLY this instrument + G3
# equal-frequency 4-bin discretization (argsort-based, exactly 15/bin, deterministic)
order = np.argsort(a_self, kind="mergesort")
bins = np.empty(N_ITEMS, dtype=int)
bins[order] = np.arange(N_ITEMS) // 15
assert set(bins.tolist()) == {0, 1, 2, 3} and all((bins == b).sum() == 15 for b in range(4))

def mi_naive(bins, c):
    n = len(bins); tot = 0.0
    for b in range(4):
        for cc in (0, 1):
            n_bc = int(((bins == b) & (c == cc)).sum())
            if n_bc == 0:
                continue
            p_bc = n_bc / n
            p_b = (bins == b).sum() / n
            p_c = (c == cc).sum() / n
            tot += p_bc * math.log(p_bc / (p_b * p_c))
    return tot

I_obs = mi_naive(bins, c_arr) + 0.025  # Miller-Madow: (4-1)(2-1)/(2*60)
rng = np.random.default_rng(S_PERM_G2)
n_perm = 100000
ge = 0
for _ in range(n_perm):
    cp = rng.permutation(c_arr)
    if mi_naive(bins, cp) + 0.025 >= I_obs:
        ge += 1
p_g2 = ge / n_perm
G2_PASS = p_g2 < G2_BAR
log("G2: I_obs=%.6f nats (MM-corrected), perm p=%.5f (bar <%.2f) -> %s%s" %
    (I_obs, p_g2, G2_BAR, "PASS" if G2_PASS else "NULL",
     " -> KILL SELF-MODEL FAMILY" if not G2_PASS else ""))

# ============ G3: calibration (TESTA-mirrored; labels touch ONLY this instrument) ============
# C1: Spearman(a_self, correctness), one-sided positive
rho, p_two = scipy_stats.spearmanr(a_self, c_arr)
p_c1 = p_two / 2.0 if rho > 0 else 1.0 - p_two / 2.0
p_c1_inv = 1.0 - p_two / 2.0 if rho < 0 else p_two / 2.0  # wrong-direction (negative)
C1_PASS = p_c1 < G3_BAR
C1_INV = (rho < 0) and (p_c1_inv < G3_BAR)
log("C1: Spearman rho=%.4f, one-sided p(licensed,+)=%.5f -> %s%s" %
    (rho, p_c1, "PASS" if C1_PASS else "null", "; INVERTED" if C1_INV else ""))

# C2: partition mean(a_self|wrong) < mean(a_self|right), one-sided permutation
wrong_mask = c_arr == 0
right_mask = c_arr == 1
n_wrong, n_right = int(wrong_mask.sum()), int(right_mask.sum())
D_obs = float(a_self[wrong_mask].mean() - a_self[right_mask].mean())
rng2 = np.random.default_rng(S_PERM_C2)
le = 0  # P(perm D <= D_obs): licensed direction
ge2 = 0  # P(perm D >= D_obs): inverted direction
for _ in range(n_perm):
    cp = rng2.permutation(c_arr)
    Dp = float(a_self[cp == 0].mean() - a_self[cp == 1].mean())
    if Dp <= D_obs:
        le += 1
    if Dp >= D_obs:
        ge2 += 1
p_c2 = le / n_perm
p_c2_inv = ge2 / n_perm
C2_PASS = p_c2 < G3_BAR
C2_INV = p_c2_inv < G3_BAR
log("C2: n_wrong=%d n_right=%d D_obs=%.6f, one-sided p(licensed)=%.5f -> %s%s" %
    (n_wrong, n_right, D_obs, p_c2, "PASS" if C2_PASS else "null",
     "; INVERTED" if C2_INV else ""))

if C1_INV or C2_INV:
    G3_READING = "KILL-CALIBRATION"
elif C1_PASS and C2_PASS:
    G3_READING = "PASS"
else:
    G3_READING = "NULL"
log("G3 reading: %s" % G3_READING)

# ============ secondary diagnostic (reported, not binding): AUC + DeLong CI ============
def auc_delong(y, s):
    # Hanley-McNeil / DeLong AUC with 95% CI
    y = np.asarray(y); s = np.asarray(s)
    pos = s[y == 1]; neg = s[y == 0]
    n1, n0 = len(pos), len(neg)
    auc = (sum(1 for a in pos for b in neg if a > b) +
           0.5 * sum(1 for a in pos for b in neg if a == b)) / (n1 * n0)
    # DeLong variance
    V10 = np.array([ (sum(1 for b in neg if a > b) + 0.5 * sum(1 for b in neg if a == b)) / n0 for a in pos ])
    V01 = np.array([ (sum(1 for a in pos if a > b) + 0.5 * sum(1 for a in pos if a == b)) / n1 for b in neg ])
    S10 = V10.var(ddof=1); S01 = V01.var(ddof=1)
    var_auc = S10 / n1 + S01 / n0
    se = math.sqrt(max(var_auc, 0))
    return auc, auc - 1.96 * se, auc + 1.96 * se

auc, auc_lo, auc_hi = auc_delong(c_arr, a_self)
log("AUC(a_self -> correctness)=%.4f [%.4f, %.4f]" % (auc, auc_lo, auc_hi))

# ============ gate reading per falsification tree (Stage-1 only) ============
if not G1_PASS:
    READING = "HELD (a): G1 fails — signal degenerate"
elif not G2_PASS:
    READING = "KILL (self-model): G2 null — no correctness information"
elif G3_READING == "KILL-CALIBRATION":
    READING = "KILL (calibration): G3 inverted — anti-signal"
elif G3_READING == "NULL":
    READING = "HELD (b): G3 null — signal absent, not anti-informative; no GPU"
else:
    READING = "GATES PASS: G1+G2+G3 in licensed direction — Stage-2 gate OPENS (needs CEO GPU clearance + founder slot)"
log("STAGE-1 READING: %s" % READING)

# ============ write records ============
records = {
    "experiment": "EXP141",
    "prereg": "research/prereg/EXP_S46_prereg_DRAFT_2026-10-03.md (SIGNED, LOG-4889)",
    "pins": {"backbone_pre": pre_hash, "backbone_post": post_hash,
             "bench": bench_hash, "hf_revision": HF_REVISION,
             "model": MODEL_ID, "dtype": "float32"},
    "seeds": {"S_PERM_G2": S_PERM_G2, "S_PERM_C2": S_PERM_C2},
    "counts": {"forwards": FWD_COUNT[0], "failed_selfevals": failed},
    "a_self": [float(x) for x in a_self],
    "b0_correct": b0_correct,
    "b0_answers": b0_answers,
    "gates": {
        "G1": {"std": g1_std, "non_constant": g1_nonconst, "bar": G1_BAR, "pass": bool(G1_PASS)},
        "G2": {"I_obs_nats": I_obs, "perm_p": p_g2, "perms": n_perm, "bar": G2_BAR,
               "pass": bool(G2_PASS)},
        "G3": {"C1": {"rho": float(rho), "p_licensed": float(p_c1), "p_inv": float(p_c1_inv),
                      "pass": bool(C1_PASS), "inverted": bool(C1_INV)},
               "C2": {"n_wrong": n_wrong, "n_right": n_right, "D_obs": float(D_obs),
                      "p_licensed": float(p_c2), "p_inv": float(p_c2_inv),
                      "pass": bool(C2_PASS), "inverted": bool(C2_INV)},
               "reading": G3_READING},
    },
    "secondary": {"auc": float(auc), "auc_ci95": [float(auc_lo), float(auc_hi)]},
    "gate_reading": READING,
    "items": [
        {"item": i, "id": bench[i]["id"], "a_self": float(a_self[i]),
         "b0_correct": b0_correct[i], "b0_answer": b0_answers[i],
         "bin": int(bins[i])}
        for i in range(N_ITEMS)
    ],
}
json.dump(records, open(os.path.join(RUN_DIR, "stage1_records.json"), "w"), indent=1)
json.dump({"verdict": "COMPLETE", "gate_reading": READING,
           "forwards": FWD_COUNT[0]},
          open(os.path.join(RUN_DIR, "stage1_verdict.json"), "w"), indent=1)
log("records written; DONE")
LOGF.close()
