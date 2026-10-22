#!/usr/bin/env python3
"""EXP139 Stage-1: kappa-hat contraction screen (CPU).
Executes EXACTLY per research/prereg/EXP139_S44_prereg_DRAFT_2026-10-03.md (SIGNED, LOG-4885).
CEO venue approval: Stage-1 CPU screen only (60 passes). $0 compute.
Exit codes: 0 = clean completion; 44 = RUN-INVALID (validity gate trip).
"""
import hashlib, json, math, os, sys, time
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

RUN_DIR = os.path.dirname(os.path.abspath(__file__))
os.makedirs(RUN_DIR, exist_ok=True)
LOGF = open(os.path.join(RUN_DIR, "stage1_run_log.txt"), "w")

def log(msg):
    line = "[%s] %s" % (time.strftime("%H:%M:%S"), msg)
    print(line, flush=True)
    LOGF.write(line + "\n"); LOGF.flush()

# ============ pre-reg §2 pinned constants ============
BACKBONE_PIN = "ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed"
BENCH_PIN = "eb304fa65a60b65ad87767d251084b256d0a79001a16b4fe8ebcd1b1f45589df"
HF_REVISION = "9879c9b5f8bea9051dcb0e68dff21493d67e9d4f"
MODEL_ID = "EleutherAI/pythia-410m"
D_HID = 1024
N_SCREEN = 20

torch.manual_seed(20261003)
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
    json.dump({"verdict": "RUN-INVALID", "reason": reason, "forwards": FWD_COUNT[0]},
              open(os.path.join(RUN_DIR, "stage1_verdict.json"), "w"), indent=1)
    LOGF.close()
    sys.exit(44)

# ============ model (pre-reg §2 verbatim) ============
log("loading model %s rev %s (float32, cpu, local_files_only)" % (MODEL_ID, HF_REVISION))
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, revision=HF_REVISION, local_files_only=True)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID, revision=HF_REVISION, local_files_only=True,
    torch_dtype=torch.float32, device_map="cpu")
model.eval()
pre_hash = sha256_state_dict(model)
log("backbone pre-hash: %s" % pre_hash)
if pre_hash != BACKBONE_PIN:
    run_invalid("(b) backbone pre-hash mismatch: got %s" % pre_hash)
log("(b) backbone pin PASS")

# ============ bench (verbatim port of run_exp135.py) ============
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

bench = build_bench()
assert len(bench) == 60, "bench len %d != 60" % len(bench)
bench_hash = hashlib.sha256(json.dumps(
    [{k: bench[i][k] for k in ("id", "prompt", "A", "C")} for i in range(len(bench))],
    sort_keys=True).encode()).hexdigest()
log("(a) bench len=60; bench sha256=%s" % bench_hash)
if bench_hash != BENCH_PIN:
    run_invalid("(a) bench sha256 mismatch: got %s" % bench_hash)
log("(a) bench pin PASS")

def make_views(it, src_ents):
    views = []
    for vk in VOCAB_KEYS:
        sub = dict(zip(src_ents, [SUPPORT_VOCABULARIES[vk][k] for k in it["idx"]]))
        prompt = it["prompt"]
        for old, new in sub.items():
            assert old in prompt, "substitution source missing: %s" % old
            prompt = prompt.replace(old, new)
        views.append({"prompt": prompt, "vk": vk,
                      "A": sub[it["A"]], "C": sub[it["C"]]})
    return views

def novel_src(it):
    base = NOVEL_VOCAB_PLANET if it["typ"] == "planet" else NOVEL_VOCAB_ELEMENT
    return [base[k] for k in it["idx"]]

screen_items = bench[:N_SCREEN]
screen_views = [make_views(it, novel_src(it))[0] for it in screen_items]  # view 0 = V1_Anglo

# committed baseline yhat for gate (c)
REC_PATH = os.path.expanduser("~/workspace/SCBI/experiments/runs/EXP135_eval/out/exp135_records.json")
committed = json.load(open(REC_PATH))
committed_yhat = [committed["cache_unintervened"][ii][0]["yhat"] for ii in range(N_SCREEN)]

# ============ operator + forward machinery (pre-reg §2) ============
W_E = model.gpt_neox.embed_in.weight.detach()
W_U = model.get_output_embeddings().weight.detach()
final_ln = model.gpt_neox.final_layer_norm

def tok1(s):
    ids = tokenizer.encode(" " + s)
    assert len(ids) == 1, "multi-token: %s -> %s" % (s, ids)
    return ids[0]

def R_of_h(h):
    """One re-entrant step. h: (1024,) float32 pre-LN residual state."""
    z = W_E.t() @ (W_U @ h)                      # Pi h, raw-logit weighting, no softmax
    inputs_embeds = z.view(1, 1, 1024)
    with torch.no_grad():
        out = model(inputs_embeds=inputs_embeds,
                    position_ids=torch.tensor([[0]]),
                    attention_mask=torch.tensor([[1]]),
                    output_hidden_states=True)
    count_fwd(1)
    return out.hidden_states[-1][0, 0, :].detach()

def baseline_forward(prompt):
    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    with torch.no_grad():
        out = model(input_ids=input_ids, output_hidden_states=True)
    count_fwd(1)
    h_last = out.hidden_states[-1][0, -1, :].detach()
    return input_ids, h_last, out.logits

def yhat_of(logits, t_target, t_foil):
    lv = logits[0, -1, :]
    return int(t_target) if float(lv[t_target]) >= float(lv[t_foil]) else int(t_foil)

# ============ Stage-1: 60 passes ============
log("Stage-1: 20 baseline + 40 R-evaluation passes")
h_list, yhat_list = [], []
for ii in range(N_SCREEN):
    v = screen_views[ii]
    input_ids, h_i, logits = baseline_forward(v["prompt"])
    h_list.append(h_i)
    yhat_list.append(yhat_of(logits, tok1(v["A"]), tok1(v["C"])))
    if (ii + 1) % 5 == 0:
        log("  baseline %d/20; forwards=%d" % (ii + 1, FWD_COUNT[0]))

# validity gate (c): recomputed baseline yhat matches committed yhat 20/20
match = sum(1 for a, b in zip(yhat_list, committed_yhat) if a == b)
log("(c) baseline yhat match: %d/20" % match)
if match != N_SCREEN:
    run_invalid("(c) baseline yhat mismatch: %d/20" % match)
log("(c) yhat fidelity PASS")

# perturbations: single generator, manual_seed(0), sequential draws
g = torch.Generator().manual_seed(0)
deltas = []
for ii in range(N_SCREEN):
    u = torch.randn(D_HID, generator=g)
    u = u / float(torch.norm(u))
    deltas.append(0.01 * float(torch.norm(h_list[ii])) * u)

# R evaluations
R_h, R_hd = [], []
for ii in range(N_SCREEN):
    R_h.append(R_of_h(h_list[ii]))
    R_hd.append(R_of_h(h_list[ii] + deltas[ii]))
    if (ii + 1) % 5 == 0:
        log("  R-eval %d/20; forwards=%d" % (ii + 1, FWD_COUNT[0]))
log("forwards total=%d (expected 60)" % FWD_COUNT[0])
if FWD_COUNT[0] != 60:
    run_invalid("forward budget: %d != 60" % FWD_COUNT[0])

# kappa-hat: 20 local + 190 cross ratios
local_ratios = []
for ii in range(N_SCREEN):
    num = float(torch.norm(R_hd[ii] - R_h[ii]))
    den = float(torch.norm(deltas[ii]))
    local_ratios.append(num / den)
cross_ratios = []
for i in range(N_SCREEN):
    for j in range(i + 1, N_SCREEN):
        den = float(torch.norm(h_list[i] - h_list[j]))
        assert den > 0, "duplicate h states"
        cross_ratios.append(float(torch.norm(R_h[i] - R_h[j])) / den)
all_ratios = local_ratios + cross_ratios
kappa_hat = max(all_ratios)
med = float(np.median(all_ratios))
q1, q3 = float(np.percentile(all_ratios, 25)), float(np.percentile(all_ratios, 75))
log("kappa_hat(max)=%.6f median=%.6f IQR=[%.6f, %.6f]" % (kappa_hat, med, q1, q3))
log("local ratios: min=%.6f max=%.6f" % (min(local_ratios), max(local_ratios)))
log("cross ratios: min=%.6f max=%.6f" % (min(cross_ratios), max(cross_ratios)))

# ============ artifacts (Law #8) ============
rec = {
    "experiment": "EXP139", "stage": 1, "log": "LOG-4885",
    "n_screen": N_SCREEN, "view": 0,
    "backbone_pre": pre_hash, "bench_sha256": bench_hash,
    "yhat_fidelity": "%d/20" % match,
    "kappa_hat": kappa_hat, "ratio_median": med, "ratio_IQR": [q1, q3],
    "local_ratios": local_ratios, "cross_ratios": cross_ratios,
    "h_norms": [float(torch.norm(h)) for h in h_list],
    "delta_norms": [float(torch.norm(d)) for d in deltas],
    "forwards": FWD_COUNT[0],
    "env": {"torch": torch.__version__},
}
json.dump(rec, open(os.path.join(RUN_DIR, "stage1_records.json"), "w"))

report_md = """# EXP139 Stage-1 Run Report (κ̂ contraction screen)

**Pre-reg:** `research/prereg/EXP139_S44_prereg_DRAFT_2026-10-03.md` (SIGNED, LOG-4885). CEO venue approval: Stage-1 CPU only.

## Validity gates
- (a) bench sha256: `{bench}` — PASS
- (b) backbone pre-hash: `{pin}` — PASS
- (c) baseline yhat fidelity: {match}/20 — PASS

## Results
- κ̂ (max of 20 local + 190 cross ratios): **{kappa:.6f}**
- median: {med:.6f}, IQR: [{q1:.6f}, {q3:.6f}]
- local ratios range: [{lmin:.6f}, {lmax:.6f}]
- cross ratios range: [{cmin:.6f}, {cmax:.6f}]
- forwards: {fwd} (budget 60)

## Bar comparison (pre-reg §3, §6 — quoted, not decided)
- κ̂ < 1 → contraction license SURVIVES → Stage-2 gate opens (needs CEO venue approval + founder GPU)
- κ̂ ≥ 1 → contraction license LOST → Stage 2 does NOT run → Stage-1b (venue per §4 pilot rule; NOT approved in this lane)
""".format(bench=bench_hash, pin=pre_hash, match=match, kappa=kappa_hat, med=med,
           q1=q1, q3=q3, lmin=min(local_ratios), lmax=max(local_ratios),
           cmin=min(cross_ratios), cmax=max(cross_ratios), fwd=FWD_COUNT[0])
open(os.path.join(RUN_DIR, "RUN_REPORT.md"), "w").write(report_md)

post_hash = sha256_state_dict(model)
log("backbone post-hash: %s" % post_hash)
log("Δθ=0 post %s" % ("PASS" if post_hash == BACKBONE_PIN else "MISMATCH"))
log("CLEAN COMPLETION exit 0")
LOGF.close()
