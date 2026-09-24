#!/usr/bin/env python3
"""K1 readout-tilt falsification executor -- LOG-213.

Frozen plan: research/analysis_plans/K1_READOUT_TILT_PLAN_LOG205_REV1_2026-09-23.md
Works plan section 10 steps 1-8 verbatim. $0 CPU: zero forward passes --
read-only weight-tensor reads plus archived records only. GPU stays dark.
There is no forward-pass invocation of the model on inputs anywhere in this
script (G5); a self-inspection below asserts that mechanically.
"""

import hashlib
import json
import math
import os
import re
import sys

import numpy as np
import torch
import transformers

# ---------------------------------------------------------------------------
# G5 self-inspection: no forward-pass invocation of the model on inputs.
# Allowed accessors (model.get_output_embeddings().weight, model.state_dict(),
# model.eval()) all have a dot between the name and the parenthesis.
# ---------------------------------------------------------------------------
_SRC = open(os.path.abspath(__file__), "r", encoding="utf-8").read()
_BAD = []
for _ln, _line in enumerate(_SRC.splitlines(), 1):
    _code = _line.split("#", 1)[0]
    if re.search(r"(?<![\w\"'.])model\s*\(", _code):
        _BAD.append((_ln, _line.strip()))
assert not _BAD, f"G5 FATAL: model forward-pass call candidates found: {_BAD}"
print("[G5] self-inspection passed: no model forward-pass invocation present.", flush=True)

# ---------------------------------------------------------------------------
# 0. Environment pin (plan section 8 table) -- exact assertions
# ---------------------------------------------------------------------------
assert torch.__version__ == "2.14.0+cpu", f"torch version mismatch: {torch.__version__}"
assert transformers.__version__ == "5.17.0", f"transformers version mismatch: {transformers.__version__}"
assert np.__version__ == "2.5.3", f"numpy version mismatch: {np.__version__}"
print(f"[ENV] torch={torch.__version__} transformers={transformers.__version__} numpy={np.__version__}", flush=True)

SCBI = os.path.expanduser("~/workspace/SCBI")
SNAP_160M = "50f5173d932e8e61f858120bcb800b97af589f46"
SNAP_410M = "9879c9b5f8bea9051dcb0e68dff21493d67e9d4f"

# ---------------------------------------------------------------------------
# Verbatim get_hash functions.
# (a) run_exp077.py ll. 166-172 (sorted state_dict keys, CPU float32 bytes) --
#     the function that produced the EXP077 smoke archive's pre_hash.
# (b) run_exp065_temporary_coordinate_alignment.py ll. 33-38 and
#     run_exp066_pythia410m_replication.py ll. 34-38 (model.parameters() order,
#     raw dtype bytes) -- the functions that produced the EXP065 and EXP066
#     archives' pre_hash values.
# DISCOVERED PLAN DEFECT (documented, not silently fixed): plan section 6 A3 /
# section 7 G3 name only function (a) as "the verbatim get_hash" for the
# archived cross-check, but the EXP065/EXP066 archives were hashed with
# function (b). Comparing (a)-digests against (b)-digests is not a cross-check
# at all -- it is the LOG-123/126 ordering-convention artifact class, already
# root-caused in the program (research_log.md LOG-128: sorted vs unsorted key
# ordering, weights byte-identical). The guard's intent is unambiguous:
# the loaded weights must be byte-identical to the weights each archived run
# hashed. That is verified by reproducing each archive's digest with the
# verbatim function that produced it. A literal (a)-only comparison yields a
# false FATAL on byte-identical weights. This correction is a measurement-method
# repair to faithfully implement the guard's stated intent (Delta theta = 0);
# it changes no endpoint, environment, or margin, and is flagged for Law #14.
# ---------------------------------------------------------------------------
def get_hash(model):
    """SHA-256 binding guard (protocol section 2): SHA-256 over the concatenation of
    state_dict() tensors (sorted keys, CPU, float32 bytes)."""
    sha = hashlib.sha256()
    for key in sorted(model.state_dict().keys()):
        sha.update(model.state_dict()[key].detach().cpu().to(torch.float32).numpy().tobytes())
    return sha.hexdigest()

def get_hash_params_order(model):
    """Verbatim get_hash of the EXP065 runner (ll. 33-38) and EXP066 runner
    (ll. 34-38): SHA-256 over model.parameters() in iteration order, raw
    dtype bytes (no float32 conversion, no key sorting)."""
    sha = hashlib.sha256()
    for p in model.parameters():
        sha.update(p.detach().cpu().numpy().tobytes())
    return sha.hexdigest()

# ---------------------------------------------------------------------------
# 1. Load run-pinned snapshots read-only (plan section 8)
# ---------------------------------------------------------------------------
from transformers import AutoModelForCausalLM, AutoTokenizer

def load_pinned(repo_id, snapshot):
    model = AutoModelForCausalLM.from_pretrained(
        repo_id,
        revision=snapshot,
        local_files_only=True,
        trust_remote_code=False,
        torch_dtype=torch.float32,
    )
    model.eval()
    tok = AutoTokenizer.from_pretrained(repo_id, revision=snapshot, local_files_only=True,
                                        trust_remote_code=False)
    return model, tok

print("[LOAD] pythia-160m ...", flush=True)
model160, tok160 = load_pinned("EleutherAI/pythia-160m", SNAP_160M)
print("[LOAD] pythia-410m ...", flush=True)
model410, tok410 = load_pinned("EleutherAI/pythia-410m", SNAP_410M)

# ---------------------------------------------------------------------------
# G3. Delta-theta=0 hash gate: pre/post via verbatim get_hash + archived cross-check
# Full archived pre_hash values from the primary JSONs (plan section 8 pins).
# ---------------------------------------------------------------------------
ARCH = {
    "EXP065": os.path.join(SCBI, "experiments/runs/EXP065_coordinate_alignment/exp065_results.json"),
    "EXP066": os.path.join(SCBI, "experiments/runs/EXP066_pythia410m_replication/exp066_replication_results.json"),
    "EXP077": os.path.join(SCBI, "experiments/runs/EXP077_cone_vs_line/exp077_results.json"),
    "EXP066_PERITEM": os.path.join(SCBI, "experiments/runs/EXP066_pythia410m_replication/exp066_instance_evaluations.json"),
    "EXP077_SMOKE_PERITEM": os.path.join(SCBI, "experiments/runs/EXP077_cone_vs_line/exp077_instance_records.json"),
}
arch065 = json.load(open(ARCH["EXP065"]))
arch066 = json.load(open(ARCH["EXP066"]))
arch077 = json.load(open(ARCH["EXP077"]))

pre160 = get_hash(model160)
pre410 = get_hash(model410)
# G3 cross-checks, each archive against its runner's VERBATIM hash function
# (see the discovered-defect note above). Archived pre==post asserted first.
assert arch065["pre_hash"] == arch065["post_hash"], "G3 FATAL: EXP065 archived pre!=post"
assert arch066["pre_hash"] == arch066["post_hash"], "G3 FATAL: EXP066 archived pre!=post"
assert arch077["pre_hash"] == arch077["post_hash"], "G3 FATAL: EXP077 archived pre!=post"
pre160_params = get_hash_params_order(model160)
pre410_params = get_hash_params_order(model410)
assert pre160_params == arch065["pre_hash"], (
    f"G3 FATAL: pythia-160m weights differ from the EXP065 archived run.\n"
    f"  computed(params-order)={pre160_params}\n  archived={arch065['pre_hash']}")
assert pre410_params == arch066["pre_hash"], (
    f"G3 FATAL: pythia-410m weights differ from the EXP066 archived run.\n"
    f"  computed(params-order)={pre410_params}\n  archived={arch066['pre_hash']}")
assert pre410 == arch077["pre_hash"], (
    f"G3 FATAL: pythia-410m weights differ from the EXP077 smoke archived run.\n"
    f"  computed(sorted)={pre410}\n  archived={arch077['pre_hash']}")
print(f"[G3] pythia-160m params-order hash OK: {pre160_params[:12]}... == archived EXP065 pre==post", flush=True)
print(f"[G3] pythia-410m params-order hash OK: {pre410_params[:12]}... == archived EXP066 pre==post", flush=True)
print(f"[G3] pythia-410m sorted hash OK: {pre410[:12]}... == archived EXP077 smoke pre==post", flush=True)
print("[G3] Delta theta = 0 confirmed on all three archived runs (runner-verbatim functions).", flush=True)

# ---------------------------------------------------------------------------
# 2. Verbatim ports of runner item-construction code (plan section 2, A1)
# ---------------------------------------------------------------------------
# Shared constants, byte-verbatim from the runners:
#   EXP065 ll. 106-118 (triples/quads); EXP066 ll. 108-117 (identical);
#   EXP077 ll. 149-159 (TRIPLES_INDICES/QUADS_INDICES, NOVEL_VOCAB_* ll. 149-150).
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

def build_exp065_066_items():
    """Verbatim port of EXP065 (run_exp065_temporary_coordinate_alignment.py
    test-instance blocks, ll. 236-345) and EXP066
    (run_exp066_pythia410m_replication.py, ll. 229-345): the four test blocks
    (planet 2-hop, planet 3-hop, element 2-hop, element 3-hop); the target is
    always the head entity (A) and the foil the tail (C/D); target_token /
    foil_token carry the leading space per runner ll. 258-259 etc."""
    items = []
    # Block 1: Planetary 2-hop (true_target, true_foil = A, C)
    for i, (iA, iB, iC) in enumerate(TRIPLES_INDICES):
        A, B, C = NOVEL_VOCAB_PLANET[iA], NOVEL_VOCAB_PLANET[iB], NOVEL_VOCAB_PLANET[iC]
        target_first = (i % 2 == 1)
        q_opts = f"{A} or {C}" if target_first else f"{C} or {A}"
        is_rev = (i >= 8)
        if not is_rev:
            p = f"Premise: {A} outranks {B}. {B} outranks {C}. Question: Who is higher in rank, {q_opts}? Answer:"
            true_target, true_foil = A, C
        else:
            p = f"Premise: {C} is lower than {B}. {B} is lower than {A}. Question: Who is higher in rank, {q_opts}? Answer:"
            true_target, true_foil = A, C
        items.append({"target_token": " " + true_target, "foil_token": " " + true_foil,
                      "prompt": p, "domain": "Planetary"})
    # Block 1: Planetary 3-hop (true_target, true_foil = A, D)
    for i, (iA, iB, iC, iD) in enumerate(QUADS_INDICES):
        A, B, C, D = (NOVEL_VOCAB_PLANET[iA], NOVEL_VOCAB_PLANET[iB],
                      NOVEL_VOCAB_PLANET[iC], NOVEL_VOCAB_PLANET[iD])
        target_first = (i % 2 == 1)
        q_opts = f"{A} or {D}" if target_first else f"{D} or {A}"
        is_rev = (i >= 8)
        if not is_rev:
            p = f"Premise: {A} outranks {B}. {B} outranks {C}. {C} outranks {D}. Question: Who is higher in rank, {q_opts}? Answer:"
            true_target, true_foil = A, D
        else:
            p = f"Premise: {D} is lower than {C}. {C} is lower than {B}. {B} is lower than {A}. Question: Who is higher in rank, {q_opts}? Answer:"
            true_target, true_foil = A, D
        items.append({"target_token": " " + true_target, "foil_token": " " + true_foil,
                      "prompt": p, "domain": "Planetary"})
    # Block 2: Elemental 2-hop (true_target, true_foil = A, C)
    for i, (iA, iB, iC) in enumerate(TRIPLES_INDICES):
        A, B, C = NOVEL_VOCAB_ELEMENT[iA], NOVEL_VOCAB_ELEMENT[iB], NOVEL_VOCAB_ELEMENT[iC]
        target_first = (i % 2 == 0)
        q_opts = f"{A} or {C}" if target_first else f"{C} or {A}"
        is_rev = (i >= 7)
        if not is_rev:
            p = f"Premise: {A} outranks {B}. {B} outranks {C}. Question: Who is higher in rank, {q_opts}? Answer:"
            true_target, true_foil = A, C
        else:
            p = f"Premise: {C} is lower than {B}. {B} is lower than {A}. Question: Who is higher in rank, {q_opts}? Answer:"
            true_target, true_foil = A, C
        items.append({"target_token": " " + true_target, "foil_token": " " + true_foil,
                      "prompt": p, "domain": "Elemental"})
    # Block 2: Elemental 3-hop (true_target, true_foil = A, D)
    for i, (iA, iB, iC, iD) in enumerate(QUADS_INDICES):
        A, B, C, D = (NOVEL_VOCAB_ELEMENT[iA], NOVEL_VOCAB_ELEMENT[iB],
                      NOVEL_VOCAB_ELEMENT[iC], NOVEL_VOCAB_ELEMENT[iD])
        target_first = (i % 2 == 0)
        q_opts = f"{A} or {D}" if target_first else f"{D} or {A}"
        is_rev = (i >= 7)
        if not is_rev:
            p = f"Premise: {A} outranks {B}. {B} outranks {C}. {C} outranks {D}. Question: Who is higher in rank, {q_opts}? Answer:"
            true_target, true_foil = A, D
        else:
            p = f"Premise: {D} is lower than {C}. {C} is lower than {B}. {B} is lower than {A}. Question: Who is higher in rank, {q_opts}? Answer:"
            true_target, true_foil = A, D
        items.append({"target_token": " " + true_target, "foil_token": " " + true_foil,
                      "prompt": p, "domain": "Elemental"})
    assert len(items) == 60
    return items

def build_exp077_items():
    """Verbatim port of EXP077 benchmark construction (run_exp077.py ll. 591-638):
    A=target, C=foil per l. 588; four blocks planet_2hop, planet_3hop,
    element_2hop, element_3hop. Returns (A, C) label strings without leading
    space; the runner encodes via tokenizer.encode(" " + label)[0] (l. 725)."""
    items = []
    for i, (iA, iB, iC) in enumerate(TRIPLES_INDICES):
        A, B, C = NOVEL_VOCAB_PLANET[iA], NOVEL_VOCAB_PLANET[iB], NOVEL_VOCAB_PLANET[iC]
        items.append({"A": A, "C": C, "domain": "Planetary"})
    for i, (iA, iB, iC, iD) in enumerate(QUADS_INDICES):
        A, B, C, D_ent = (NOVEL_VOCAB_PLANET[iA], NOVEL_VOCAB_PLANET[iB],
                          NOVEL_VOCAB_PLANET[iC], NOVEL_VOCAB_PLANET[iD])
        items.append({"A": A, "C": D_ent, "domain": "Planetary"})
    for i, (iA, iB, iC) in enumerate(TRIPLES_INDICES):
        A, B, C = NOVEL_VOCAB_ELEMENT[iA], NOVEL_VOCAB_ELEMENT[iB], NOVEL_VOCAB_ELEMENT[iC]
        items.append({"A": A, "C": C, "domain": "Elemental"})
    for i, (iA, iB, iC, iD) in enumerate(QUADS_INDICES):
        A, B, C, D_ent = (NOVEL_VOCAB_ELEMENT[iA], NOVEL_VOCAB_ELEMENT[iB],
                          NOVEL_VOCAB_ELEMENT[iC], NOVEL_VOCAB_ELEMENT[iD])
        items.append({"A": A, "C": D_ent, "domain": "Elemental"})
    assert len(items) == 60
    return items

items065_066 = build_exp065_066_items()
items077 = build_exp077_items()

# ---- G2: label cross-check vs archived per-item records (FATAL on mismatch) ----
rec066 = json.load(open(ARCH["EXP066_PERITEM"]))
assert len(rec066) == 60, f"G2 FATAL: EXP066 per-item record count {len(rec066)} != 60"
ordered066 = [f"pythia410m_planet_2hop_{i}" for i in range(15)] + \
             [f"pythia410m_planet_3hop_{i}" for i in range(15)] + \
             [f"pythia410m_element_2hop_{i}" for i in range(15)] + \
             [f"pythia410m_element_3hop_{i}" for i in range(15)]
for idx, key in enumerate(ordered066):
    rec = rec066[key]
    rb = items065_066[idx]
    # Plan section 2 cross-check source for EXP066: the archived prompts
    # (the records carry no target_token/foil_token fields -- prompts only).
    # The prompt strings embed the item construction verbatim.
    assert rec["prompt"] == rb["prompt"], f"G2 FATAL: EXP066 prompt mismatch at {key}"
print("[G2] EXP065/066: 60/60 items byte-consistent with exp066_instance_evaluations.json prompts.", flush=True)
# EXP065 has no per-item archive; byte-identity of the four runners' item
# definitions (60/60) is the LOG-197-established FACT cited in plan section 2.
print("[G2] EXP065: no per-item archive exists; construction constants byte-verbatim from runner (LOG-197 byte-identity FACT).", flush=True)

rec077 = json.load(open(ARCH["EXP077_SMOKE_PERITEM"]))
assert len(rec077) == 60, f"G2 FATAL: EXP077 smoke per-item record count {len(rec077)} != 60"
# DISCOVERED ARCHIVE FACT (documented, not hidden): the smoke archive's bench
# is NOT the ported run_exp077.py bench. The records are entity-grouped with
# exactly 6 items per entity (Marsx6, Venusx6, ..., Steelx6), while the ported
# bench (run_exp077.py ll. 591-638, the plan's section 2 pin) yields
# Marsx21/Ironx21/Venusx7/Goldx7/Jupiterx2/Silverx2 and no Saturn/Mercury/
# Bronze/Steel targets at all. The plan's section 2 premise ("LOG-197
# established the four runners' item definitions are byte-identical 60/60")
# is factually falsified for the SMOKE archive by the archive itself; the
# smoke's (target, foil) pairs are not archived (records carry ent/typ only),
# so the smoke bench is not reconstructible from archived records.
# Scoped G2 resolution (disclosed deviation, flagged for Law #14): G2's intent
# is to validate the labels feeding endpoint (a). All PRIMARY runs' labels
# are validated (EXP065/066 60/60 vs archived prompts; EXP077-official labels
# come from the frozen bench port, the plan's pin -- no in-repo per-item
# records exist for the official run). The smoke is "labeled secondary only"
# (plan section 1.1) and feeds no verdict cell in section 7's table; its (a)
# endpoint is therefore NOT computed (labels not archived -- never filled by
# assumption). The smoke contributes (b)/(c2) only, which are order-independent
# counts. This anomaly is reported as a discovered fact, not a guard failure
# of the primary battery.
smoke_ents = [rec["ent"] for rec in rec077]
smoke_typs = [rec["typ"] for rec in rec077]
from collections import Counter as _Counter
smoke_ent_counts = dict(_Counter(smoke_ents))
ported_targets = [it["A"] for it in items077]
ported_target_counts = dict(_Counter(ported_targets))
print(f"[G2] EXP077 smoke bench: archive ent counts = {smoke_ent_counts}", flush=True)
print(f"[G2] EXP077 smoke bench: ported bench target counts = {ported_target_counts}", flush=True)
print("[G2] CONCLUSION: smoke bench differs from the ported construction; smoke (a) not computed (labels not archived).", flush=True)
SMOKE_A_COMPUTABLE = False

# ---- Token ids: tokenizer.encode(" " + label)[0] exactly as the runners call it ----
ids065_066 = [(tok160.encode(it["target_token"])[0], tok160.encode(it["foil_token"])[0]) for it in items065_066]
ids066_410 = [(tok410.encode(it["target_token"])[0], tok410.encode(it["foil_token"])[0]) for it in items065_066]
ids077 = [(tok410.encode(" " + it["A"])[0], tok410.encode(" " + it["C"])[0]) for it in items077]
for name, ids in [("EXP065", ids065_066), ("EXP066", ids066_410), ("EXP077", ids077)]:
    for i, (t, f) in enumerate(ids):
        assert t != f, f"G2 FATAL: {name} item {i}: target==foil token id {t}"
print("[IDS] all 60x3 items: target != foil token id; encode(' '+label)[0] verbatim.", flush=True)

# ---------------------------------------------------------------------------
# 3. Endpoint (a): per-item c_i = cos(b_hat_i, w_hat_{t_i}) (plan section 3)
# b_hat_i = normalize(E_run[t_i] - E_run[f_i]) -- LOG-197-verified construction,
# scale-free (alpha drops out of the cosine).
# ---------------------------------------------------------------------------
def compute_endpoint_a(E, ids, alpha):
    c_list, bhat_list, normdiff_list, wt_norm_list, wf_norm_list = [], [], [], [], []
    for (t_id, f_id) in ids:
        wt = E[t_id, :]; wf = E[f_id, :]
        assert float(torch.norm(wt).item()) > 0 and float(torch.norm(wf).item()) > 0
        diff = wt - wf
        nd = float(torch.norm(diff).item())
        assert nd > 0
        b_hat = diff / nd
        w_hat = wt / float(torch.norm(wt).item())
        c_list.append(float((b_hat @ w_hat).item()))
        bhat_list.append(b_hat)
        normdiff_list.append(nd)
        wt_norm_list.append(float(torch.norm(wt).item()))
        wf_norm_list.append(float(torch.norm(wf).item()))
    return (np.array(c_list), bhat_list, np.array(normdiff_list),
            np.array(wt_norm_list), np.array(wf_norm_list))

E160 = model160.get_output_embeddings().weight.detach().cpu()
E410 = model410.get_output_embeddings().weight.detach().cpu()
assert E160.shape[1] == 768 and E410.shape[1] == 1024, "run-pin dimension mismatch"

c065, bh065, nd065, wtn065, wfn065 = compute_endpoint_a(E160, ids065_066, 1.0)
c066, bh066, nd066, wtn066, wfn066 = compute_endpoint_a(E410, ids066_410, 1.0)
# EXP077-official (a): the plan pins the official bench to the run_exp077.py
# port (section 2). No in-repo per-item records exist for the official GPU run,
# so the frozen port is the plan's prescribed label source.
c077off, bh077off, nd077off, wtn077off, wfn077off = compute_endpoint_a(E410, ids077, 0.5)

# ---- G1: bridge-identity re-verification (independent numpy float64 path) ----
E410_np = E410.numpy().astype(np.float64)
E160_np = E160.numpy().astype(np.float64)
def g1_check(ids, bhat_list, E_np, run):
    worst = 0.0
    for (t_id, f_id), b_torch in zip(ids, bhat_list):
        d = E_np[t_id] - E_np[f_id]
        b_np = d / np.linalg.norm(d)
        cosv = float(np.dot(b_np, b_torch.numpy().astype(np.float64)))
        worst = max(worst, abs(1.0 - abs(cosv)))
    assert worst <= 1e-6, f"G1 FATAL: {run} bridge-identity deviation {worst} > 1e-6"
    return worst
g1_065 = g1_check(ids065_066, bh065, E160_np, "EXP065")
g1_066 = g1_check(ids066_410, bh066, E410_np, "EXP066")
g1_077 = g1_check(ids077, bh077off, E410_np, "EXP077-official")
print(f"[G1] bridge-identity guard passed (max |1-|cos||: 065={g1_065:.2e} 066={g1_066:.2e} 077off={g1_077:.2e}).", flush=True)

# A8: report min_i ||W_U[t_i] - W_U[f_i]||_2 across all items x runs
min_nd = float(min(nd065.min(), nd066.min(), nd077off.min()))
assert min_nd > 0, "A8 FATAL: degenerate difference row (zero norm)"
print(f"[A8] min_i ||W_U[t_i]-W_U[f_i]||_2 across all items x runs = {min_nd:.6f} (>0, non-degenerate).", flush=True)

# ---------------------------------------------------------------------------
# Exact Clopper-Pearson 95% CI (plan section 3)
# ---------------------------------------------------------------------------
from scipy.stats import beta
def clopper_pearson(k, n, alpha=0.05):
    lo = float(beta.ppf(alpha / 2, k, n - k + 1)) if k > 0 else 0.0
    hi = float(beta.ppf(1 - alpha / 2, k + 1, n - k)) if k < n else 1.0
    return lo, hi

# Probative check of the CI implementation against the registered bars:
# >=39/60 must give lower CI > 0.5; 38/60 must not; <=21/60 must give upper < 0.5; 22/60 must not.
lo39, _ = clopper_pearson(39, 60); lo38, _ = clopper_pearson(38, 60)
_, hi21 = clopper_pearson(21, 60); _, hi22 = clopper_pearson(22, 60)
assert lo39 > 0.5 and not (lo38 > 0.5), "CP bar self-check failed (kill bar)"
assert hi21 < 0.5 and not (hi22 < 0.5), "CP bar self-check failed (ruled-out bar)"
print(f"[CI] bar self-check: CP(39/60) lo={lo39:.4f}>0.5; CP(38/60) lo={lo38:.4f}<=0.5; "
      f"CP(21/60) hi={hi21:.4f}<0.5; CP(22/60) hi={hi22:.4f}>=0.5.", flush=True)

def endpoint_a_stats(c):
    n = len(c)
    k = int(np.sum(c >= 0.9))
    p_hat = k / n
    lo, hi = clopper_pearson(k, n)
    if lo > 0.5:
        decision = "KILL"
    elif hi < 0.5:
        decision = "RULED-OUT"
    else:
        decision = "NEUTRAL"
    hist, edges = np.histogram(c, bins=10, range=(-1.0, 1.0))
    return {"c": c, "mean": float(np.mean(c)), "median": float(np.median(c)),
            "min": float(np.min(c)), "max": float(np.max(c)), "std": float(np.std(c)),
            "k": k, "n": n, "p_hat": p_hat, "ci_lo": lo, "ci_hi": hi,
            "decision": decision, "hist_counts": hist.tolist(),
            "hist_edges": edges.tolist()}

s065 = endpoint_a_stats(c065)
s066 = endpoint_a_stats(c066)
s077off = endpoint_a_stats(c077off)
for name, s in [("EXP065", s065), ("EXP066", s066), ("EXP077-official", s077off)]:
    print(f"[A] {name}: k={s['k']}/60 c>=0.9, p_hat={s['p_hat']:.4f}, "
          f"CP95=[{s['ci_lo']:.4f},{s['ci_hi']:.4f}], mean={s['mean']:.4f}, "
          f"min={s['min']:.4f}, max={s['max']:.4f} -> {s['decision']}", flush=True)
print("[A] EXP077-smoke: (a) NOT computed -- smoke bench labels not archived "
      "(see G2 discovery note); smoke is labeled secondary only.", flush=True)

# EXP066 vs EXP077-official c_i identity: byte-identical items + same pinned
# matrix -> deterministic equality; reported as OBSERVATION (not a guard).
max_abs_diff = float(np.max(np.abs(c066 - c077off)))
print(f"[OBS] max|c_i(EXP066)-c_i(EXP077-official)| = {max_abs_diff:.3e} "
      f"(expected 0: same pinned matrix, byte-identical items).", flush=True)

# ---------------------------------------------------------------------------
# 4. Endpoint (b): archived (b,c) + recompute from per-item records (plan sec 4)
# Reading kept verbatim per Law #4 (diagnostic ONLY; never fires the kill):
#   f >= r/2 strengthens a tilt verdict;
#   f ~= 0 with r > 0 (lower 95% CI of DeltaM > delta_min) weakens it;
# LOG-212 standing correction noted, not applied (plan section 4).
# ---------------------------------------------------------------------------
def bc_from_records(base, mod):
    b = sum(1 for x, y in zip(base, mod) if (not x) and y)
    c = sum(1 for x, y in zip(base, mod) if x and (not y))
    return b, c

# EXP066 per-item recompute
keys066 = ordered066
base066 = [bool(rec066[k]["base_correct"]) for k in keys066]
mod066 = [bool(rec066[k]["Same_Layer_Output_Bridge_correct"]) for k in keys066]
b066_re, c066_re = bc_from_records(base066, mod066)
sb066 = arch066["stage_B_conditions"]["Same_Layer_Output_Bridge"]
assert (b066_re, c066_re) == (sb066["rescues_b"], sb066["corruptions_c"]), \
    f"(b) archive-integrity mismatch EXP066: recomputed {(b066_re, c066_re)} vs archived {(sb066['rescues_b'], sb066['corruptions_c'])}"
print(f"[B] EXP066 recomputed (b,c)={b066_re, c066_re} matches archived aggregates.", flush=True)

# EXP077 smoke per-item recompute (C1 = baseline per run_exp077.py l.802; C8 = bridge)
base077s = [bool(rec["correct"]["C1"]) for rec in rec077]
mod077s = [bool(rec["correct"]["C8_bridge"]) for rec in rec077]
b077s_re, c077s_re = bc_from_records(base077s, mod077s)
sb077s = arch077["stage_B_conditions"]["C8_bridge"]
assert (b077s_re, c077s_re) == (sb077s["b"], sb077s["c"]), \
    f"(b) archive-integrity mismatch EXP077 smoke: recomputed {(b077s_re, c077s_re)} vs archived {(sb077s['b'], sb077s['c'])}"
print(f"[B] EXP077 smoke recomputed (b,c)={b077s_re, c077s_re} matches archived aggregates.", flush=True)

sb065 = arch065["stage_B_confirmatory_results"]["Same_Layer_Output_Bridge"]
# EXP065 has no per-item correctness archive (aggregates only): (10, 0) [FACT].

def b_reading(run, r, f, lower_ci, delta_min=0.05):
    if f >= r / 2 and r > 0:
        return "strengthens (adopted mapping, verbatim)"
    if f == 0 and r > 0 and lower_ci > delta_min:
        return "weakens (adopted mapping, verbatim)"
    return "neutral"

# Archived lower 95% Tango CIs of DeltaM per plan section 1.1 [FACT - records]
b065 = {"run": "EXP065", "r": sb065["rescues_b"], "f": sb065["corruptions_c"],
        "delta_m": sb065["delta_m"], "lower_ci": 0.0931,
        "recomputed": None}
b066 = {"run": "EXP066", "r": sb066["rescues_b"], "f": sb066["corruptions_c"],
        "delta_m": sb066["delta_m"], "lower_ci": 0.0651,
        "recomputed": (b066_re, c066_re)}
b077off = {"run": "EXP077-official", "r": 6, "f": 0, "delta_m": 0.10,
           "lower_ci": 0.0338, "recomputed": None,
           "source": "research_log.md LOG-128 (official GPU record; notebook mirror pending)"}
b077smo = {"run": "EXP077-smoke", "r": sb077s["b"], "f": sb077s["c"],
           "delta_m": sb077s["delta_m"], "lower_ci": 0.1444,
           "recomputed": (b077s_re, c077s_re), "source": "exp077_results.json (labeled secondary)"}
for b in (b065, b066, b077off, b077smo):
    b["reading"] = b_reading(b["run"], b["r"], b["f"], b["lower_ci"])
    print(f"[B] {b['run']}: r={b['r']} f={b['f']} dM={b['delta_m']:.4f} "
          f"lowerCI={b['lower_ci']:.4f} -> {b['reading']}", flush=True)

# ---------------------------------------------------------------------------
# 5. Endpoint (c2): swapped-scoring identity (plan section 5.3) -- G4 FATAL
# With roles swapped under strict-> binary scoring, correct_swap = NOT correct_orig
# (absent exact ties); then (b_swap, c_swap) == (c_orig, b_orig) and
# DeltaM_swap == -DeltaM_orig EXACTLY under both hypotheses (plan section 5.1).
# Integrity check only -- licenses no claim about tilt vs mechanism.
# ---------------------------------------------------------------------------
def c2_identity(base, mod, run):
    b, c = bc_from_records(base, mod)
    base_sw = [not x for x in base]
    mod_sw = [not x for x in mod]
    b_swap, c_swap = bc_from_records(base_sw, mod_sw)
    assert (b_swap, c_swap) == (c, b), (
        f"G4 FATAL ({run}): swapped (b,c)={(b_swap, c_swap)} != (c_orig,b_orig)={(c, b)}")
    # Exact integer form of the DeltaM identity: with correct_swap = NOT correct_orig
    # per item (absent ties), b_swap - c_swap = c - b = -(b - c) as integers, and
    # DeltaM = (b - c)/n, so DeltaM_swap = -DeltaM_orig exactly over the rationals.
    # (A naive float comparison of mean() values can differ by 1 ulp from summation
    # order; the integer identity is the exact statement of plan section 5.1.)
    assert (b_swap - c_swap) == -(b - c), (
        f"G4 FATAL ({run}): (b_swap-c_swap)={(b_swap - c_swap)} != {-(b - c)}")
    n = len(base)
    dm = (b - c) / n
    dm_swap = (b_swap - c_swap) / n
    return {"b_orig": b, "c_orig": c, "b_swap": b_swap, "c_swap": c_swap,
            "dm_orig": dm, "dm_swap": dm_swap}

c2_066 = c2_identity(base066, mod066, "EXP066")
c2_077s = c2_identity(base077s, mod077s, "EXP077-smoke")
print(f"[C2] EXP066 identity holds: (b_swap,c_swap)={(c2_066['b_swap'], c2_066['c_swap'])} "
      f"== (c_orig,b_orig)={(c2_066['c_orig'], c2_066['b_orig'])}; dM_swap={c2_066['dm_swap']:.4f}.", flush=True)
print(f"[C2] EXP077-smoke identity holds: (b_swap,c_swap)={(c2_077s['b_swap'], c2_077s['c_swap'])} "
      f"== (c_orig,b_orig)={(c2_077s['c_orig'], c2_077s['b_orig'])}; dM_swap={c2_077s['dm_swap']:.4f}.", flush=True)
print("[C2] EXP065: no per-item correctness archive; identity is the plan-5.1 arithmetic consequence of aggregates (10,0).", flush=True)

# ---------------------------------------------------------------------------
# 6. D1: archived logit-shift sign signature + ratio diagnostic (plan sec 5.4)
# r_obs = DeltaL_t/|DeltaL_f| vs r_pred = mean_i(dLhat_{t,i}/|dLhat_{f,i}|),
# dLhat_{t,i} = alpha_run (b_hat_i . W_U[t_i]) from weights alone.
# Reading: |r_obs - r_pred|/r_pred <= 0.5 [ARBITRARY] strengthens; else neutral.
# Cannot fire the kill. No archived per-item shifts for EXP077 -> n/a.
# ---------------------------------------------------------------------------
def d1_ratio(bhat_list, E, ids, alpha, run):
    num, den = [], []
    for (t_id, f_id), b_hat in zip(ids, bhat_list):
        dl_t = alpha * float((b_hat @ E[t_id, :]).item())
        dl_f = alpha * float((b_hat @ E[f_id, :]).item())
        num.append(dl_t); den.append(abs(dl_f))
    r_pred = float(np.mean(np.array(num) / np.array(den)))
    return r_pred

d065_t, d065_f = sb065["delta_logit_target"], sb065["delta_logit_foil"]
d066_t, d066_f = sb066["delta_logit_target"], sb066["delta_logit_foil"]
r_obs_065 = d065_t / abs(d065_f)
r_obs_066 = d066_t / abs(d066_f)
r_pred_065 = d1_ratio(bh065, E160, ids065_066, 1.0, "EXP065")
r_pred_066 = d1_ratio(bh066, E410, ids066_410, 1.0, "EXP066")
def d1_reading(r_obs, r_pred):
    rel = abs(r_obs - r_pred) / r_pred
    return rel, ("strengthens" if rel <= 0.5 else "neutral")
rel065, rd065 = d1_reading(r_obs_065, r_pred_065)
rel066, rd066 = d1_reading(r_obs_066, r_pred_066)
print(f"[D1] EXP065: archived dL_t={d065_t:+.4f} dL_f={d065_f:+.4f} (target-up/foil-down sign signature); "
      f"r_obs={r_obs_065:.4f} r_pred={r_pred_065:.4f} rel={rel065:.3f} -> {rd065}", flush=True)
print(f"[D1] EXP066: archived dL_t={d066_t:+.4f} dL_f={d066_f:+.4f} (target-up/foil-down sign signature); "
      f"r_obs={r_obs_066:.4f} r_pred={r_pred_066:.4f} rel={rel066:.3f} -> {rd066}", flush=True)
print("[D1] EXP077 (official + smoke): no archived logit shifts; ratio diagnostic not applicable.", flush=True)

# ---------------------------------------------------------------------------
# Post-hash (G3 completion): weights must be byte-identical after all reads
# ---------------------------------------------------------------------------
post160 = get_hash(model160)
post410 = get_hash(model410)
post160_params = get_hash_params_order(model160)
post410_params = get_hash_params_order(model410)
assert post160 == pre160, "G3 FATAL: pythia-160m weights changed during execution"
assert post410 == pre410, "G3 FATAL: pythia-410m weights changed during execution"
assert post160_params == pre160_params, "G3 FATAL: pythia-160m weights changed during execution (params-order)"
assert post410_params == pre410_params, "G3 FATAL: pythia-410m weights changed during execution (params-order)"
print("[G3] post-hashes match pre-hashes (both conventions): Delta theta = 0 confirmed.", flush=True)

# ---------------------------------------------------------------------------
# 7. Verdicts (plan section 7 table, filled verbatim)
# ---------------------------------------------------------------------------
def per_run_verdict(a_decision, b_read, guards_pass):
    if not guards_pass:
        return "Refuted"
    if a_decision == "KILL":
        return "Supported"
    if a_decision == "RULED-OUT":
        return "Not supported"
    return "Inconclusive"

guards_pass = True  # G1-G5 all passed above (FATAL asserts would have halted)
v065 = per_run_verdict(s065["decision"], b065["reading"], guards_pass)
v066 = per_run_verdict(s066["decision"], b066["reading"], guards_pass)
v077off = per_run_verdict(s077off["decision"], b077off["reading"], guards_pass)

primary = [("EXP065", v065), ("EXP066", v066), ("EXP077-official", v077off)]
if any(v == "Supported" for _, v in primary):
    program_verdict = "K1-CONFIRMED"
elif all(v == "Not supported" for _, v in primary):
    program_verdict = "K1-EXONERATED"
else:
    program_verdict = "Inconclusive"

print("=" * 78)
print("K1 PER-RUN VERDICTS (plan section 7):")
for name, v in primary:
    print(f"  {name}: {v}")
print("  EXP077-smoke: secondary only -- (a) not computed (labels not archived); "
      "(b)/(c2) reported as labeled-secondary diagnostics")
print(f"EXP070 cells: Underdetermined (no verified vectors; excluded)")
print(f"PROGRAM-LEVEL: {program_verdict}")
print("=" * 78)

# ---------------------------------------------------------------------------
# Machine-readable twin JSON (plan section 10 step 7)
# ---------------------------------------------------------------------------
twin = {
    "log": "LOG-213",
    "plan": "K1_READOUT_TILT_PLAN_LOG205_REV1_2026-09-23.md",
    "environment": {
        "venv": "/home/hatch/workspace/.venv_smoke",
        "torch": torch.__version__, "transformers": transformers.__version__,
        "numpy": np.__version__, "scipy": __import__("scipy").__version__,
        "forward_passes": 0,
        "seeds": "deterministic; no RNG consumed",
    },
    "snapshots": {"pythia-160m": SNAP_160M, "pythia-410m": SNAP_410M},
    "delta_theta_0": {
        "note": "each archive cross-checked against its runner's verbatim hash function "
                "(plan A3 named only run_exp077's function; EXP065/066 archives used the "
                "parameters()-order function -- LOG-123/126 convention-artifact class; "
                "see report for the discovered-defect disclosure)",
        "pythia-160m": {"pre_hash_sorted": pre160, "post_hash_sorted": post160,
                        "pre_hash_params_order": pre160_params, "post_hash_params_order": post160_params,
                        "archived_exp065_pre_hash": arch065["pre_hash"],
                        "match": pre160_params == arch065["pre_hash"]},
        "pythia-410m": {"pre_hash_sorted": pre410, "post_hash_sorted": post410,
                        "pre_hash_params_order": pre410_params, "post_hash_params_order": post410_params,
                        "archived_exp066_pre_hash": arch066["pre_hash"],
                        "archived_exp077_pre_hash": arch077["pre_hash"],
                        "match_exp066": pre410_params == arch066["pre_hash"],
                        "match_exp077": pre410 == arch077["pre_hash"]},
    },
    "guards": {
        "G1_bridge_identity": {"pass": True, "max_dev_065": g1_065, "max_dev_066": g1_066, "max_dev_077": g1_077, "bar": "<=1e-6"},
        "G2_label_crosscheck": {"pass": True, "exp066": "60/60 byte-consistent (archived prompts; records carry no token fields)",
                                "exp077_official": "no in-repo per-item records; frozen bench port is the plan's pin",
                                "exp077_smoke": "DISCOVERY: smoke bench differs from ported construction "
                                "(archive: 6 items/entity; ported: Marsx21/Ironx21/...); smoke (a) not computed; "
                                "scoped G2 -- see report",
                                "exp065": "no per-item archive; LOG-197 byte-identity FACT"},
        "G3_delta_theta": {"pass": True,
            "method": "each archive cross-checked against its runner's verbatim hash function "
                      "(EXP065/066: parameters()-order, raw bytes; EXP077 smoke: sorted state_dict, float32). "
                      "Plan A3 named only run_exp077's function -- discovered defect, disclosed in report."},
        "G4_c2_identity": {"pass": True, "exp066": c2_066, "exp077_smoke": c2_077s,
                           "exp065": "no per-item records; arithmetic consequence of aggregates"},
        "G5_no_forward_pass": {"pass": True, "method": "source self-inspection; no invocation of the model on inputs"},
    },
    "A8_min_diffrow_norm": min_nd,
    "endpoint_a": {
        "EXP065": {k: (v.tolist() if isinstance(v, np.ndarray) else v) for k, v in s065.items()},
        "EXP066": {k: (v.tolist() if isinstance(v, np.ndarray) else v) for k, v in s066.items()},
        "EXP077_official": {k: (v.tolist() if isinstance(v, np.ndarray) else v) for k, v in s077off.items()},
        "EXP077_smoke": "not computed -- smoke bench (target, foil) labels not archived; "
                        "smoke bench differs from the ported construction (G2 discovery note)",
        "exp066_vs_exp077official_max_abs_diff": max_abs_diff,
        "bars": {"kill_needs": "lower CP95 > 0.5 (>=39/60)", "ruled_out_needs": "upper CP95 < 0.5 (<=21/60)"},
    },
    "endpoint_b": {"EXP065": b065, "EXP066": b066, "EXP077_official": b077off, "EXP077_smoke": b077smo,
                   "note": "diagnostic only; (b) never fires the kill (plan sec 4); LOG-212 standing correction noted, not applied"},
    "D1": {
        "EXP065": {"archived_dL_t": d065_t, "archived_dL_f": d065_f, "r_obs": r_obs_065,
                   "r_pred": r_pred_065, "rel_diff": rel065, "reading": rd065},
        "EXP066": {"archived_dL_t": d066_t, "archived_dL_f": d066_f, "r_obs": r_obs_066,
                   "r_pred": r_pred_066, "rel_diff": rel066, "reading": rd066},
        "EXP077": "not applicable (no archived logit shifts)",
        "tolerance": "|r_obs-r_pred|/r_pred <= 0.5 [ARBITRARY]",
    },
    "verdicts": {
        "per_run": {"EXP065": v065, "EXP066": v066, "EXP077_official": v077off,
                    "EXP077_smoke": "secondary only -- no (a) verdict (labels not archived)",
                    "EXP070": "Underdetermined"},
        "program": program_verdict,
    },
}
twin_path = os.path.join(SCBI, "research/analysis_plans/K1_RESULTS_LOG213_2026-09-23.json")
json.dump(twin, open(twin_path, "w"), indent=2)
print(f"[OUT] wrote {twin_path}", flush=True)
print("K1 EXECUTION COMPLETE -- no exceptions, no guard failures.", flush=True)
