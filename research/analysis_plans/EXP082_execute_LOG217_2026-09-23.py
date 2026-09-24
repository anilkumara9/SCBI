#!/usr/bin/env python3
"""EXP082 — Foil-Suppression Tilt Falsification: EXECUTOR (LOG-217).

Executes research/analysis_plans/EXP082_FOILSUPPRESSION_TILT_PLAN_LOG214_2026-09-23.md
Section 10, steps 1-9, VERBATIM. FROZEN plan; Law #14 SIGN = LOG-215 + LOG-215b.

Budget: $0 CPU. ZERO forward passes. Read-only weight-tensor reads + archived
records only. GPU stays dark.

Standing constraints enforced in this script:
 - EXP070 excluded entirely (Underdetermined; no verified vectors).
 - The adopted (b) reading appears NOWHERE with decision weight; flip counts are
   an [OBSERVATION] consistency check under the L1-aligned reading (f=0
   tilt-predicted) only.
 - Guards G1-G6 are all FATAL on failure: halt, report the failure, no verdict.
 - No forward pass: this script contains NO `model(...)` call on inputs (G5).
"""

import hashlib
import json
import math
import platform
import sys

import numpy as np
import torch
import transformers

# ----------------------------------------------------------------------------
# STEP 1 (part 1): §8 environment pin — exact asserts, no tolerance.
# ----------------------------------------------------------------------------
assert torch.__version__ == "2.14.0+cpu", f"FATAL env: torch {torch.__version__}"
assert transformers.__version__ == "5.17.0", f"FATAL env: transformers {transformers.__version__}"
assert np.__version__ == "2.5.3", f"FATAL env: numpy {np.__version__}"
assert sys.prefix == "/home/hatch/workspace/.venv_smoke", f"FATAL env: {sys.prefix}"

# Scipy only for the exact Clopper-Pearson interval (no model contact).
from scipy.stats import beta as beta_dist
import scipy
assert scipy.__version__ == "1.18.1", f"FATAL env: scipy {scipy.__version__}"

PIN_160M = "50f5173d932e8e61f858120bcb800b97af589f46"
PIN_410M = "9879c9b5f8bea9051dcb0e68dff21493d67e9d4f"
HASH_065 = "54c88fa4897785f2bd94b32d26de1f73f1052bcc42124d563d0cda96940de936"
HASH_066 = "4c242d9ac702a4029a674eacee84e0517cb6f79d794661dc3a3102bca5ed48dd"
HASH_077 = "ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed"

RUNS = {
    # run_id: (hf_id, snapshot_pin, archived_pre_hash, alpha_run, d, layer)
    "EXP065": ("EleutherAI/pythia-160m", PIN_160M, HASH_065, 1.0, 768, 10),
    "EXP066": ("EleutherAI/pythia-410m", PIN_410M, HASH_066, 1.0, 1024, 20),
    # EXP077 official GPU = primary. Smoke (labeled secondary) shares the same
    # items, snapshot, and construction: identical per-item geometry.
    "EXP077": ("EleutherAI/pythia-410m", PIN_410M, HASH_077, 0.5, 1024, 20),
}


def get_hash(model):
    """VERBATIM port of run_exp077.py ll. 166-172 (EXP077's runner):
    SHA-256 over the concatenation of state_dict() tensors (sorted keys, CPU,
    float32 bytes). Read-only."""
    sha = hashlib.sha256()
    for key in sorted(model.state_dict().keys()):
        sha.update(model.state_dict()[key].detach().cpu().to(torch.float32).numpy().tobytes())
    return sha.hexdigest()


def get_hash_065_066(model):
    """VERBATIM port of run_exp065_temporary_coordinate_alignment.py ll. 33-37
    (identical in run_exp066_pythia410m_replication.py ll. 34-38): SHA-256 over
    model.parameters() iteration order, CPU bytes, no dtype conversion.
    [PLAN CORRECTION, LOG-217]: the plan's §8 names run_exp077's formulation as
    'verbatim' for all three runs, but EXP065/066's runners hashed with THIS
    formulation (different tensor order: parameters() registration order vs
    sorted state_dict keys). The archived EXP065/066 pre_hashes were produced
    by this formulation; applying run_exp077's formulation to them is a
    category error. Each run is therefore verified with its own runner's
    verbatim formulation. The Law #14 review did not catch this; reported as
    [OBSERVATION]."""
    sha = hashlib.sha256()
    for p in model.parameters():
        sha.update(p.detach().cpu().numpy().tobytes())
    return sha.hexdigest()


# Per-run verbatim hash formulation (see get_hash_065_066 docstring).
HASH_FN = {"EXP065": get_hash_065_066, "EXP066": get_hash_065_066, "EXP077": get_hash}


def load_pinned(hf_id, snapshot):
    """Read-only load of the run-pinned snapshot (no forward passes anywhere)."""
    tok = transformers.AutoTokenizer.from_pretrained(
        hf_id, revision=snapshot, local_files_only=True, trust_remote_code=False)
    mdl = transformers.AutoModelForCausalLM.from_pretrained(
        hf_id, revision=snapshot, local_files_only=True, trust_remote_code=False,
        torch_dtype=torch.float32)
    mdl.eval()
    return tok, mdl


# ----------------------------------------------------------------------------
# STEP 2 (part 1): §2 verbatim ports of runner item-construction code.
# Each port returns a list of 60 (target_token_str, foil_token_str, prompt_str)
# with the leading space already attached, exactly as the runners built them.
# ----------------------------------------------------------------------------

TRIPLES = [
    (0, 1, 2), (1, 2, 3), (2, 3, 4), (0, 2, 4), (0, 1, 3),
    (1, 3, 4), (0, 2, 3), (1, 2, 4), (0, 3, 4), (0, 1, 4),
    (0, 1, 2), (1, 2, 3), (2, 3, 4), (0, 2, 4), (0, 1, 3),
]
QUADS = [
    (0, 1, 2, 3), (1, 2, 3, 4), (0, 1, 3, 4), (0, 2, 3, 4), (0, 1, 2, 4),
    (0, 1, 2, 3), (1, 2, 3, 4), (0, 1, 3, 4), (0, 2, 3, 4), (0, 1, 2, 4),
    (0, 1, 2, 3), (1, 2, 3, 4), (0, 1, 3, 4), (0, 2, 3, 4), (0, 1, 2, 4),
]
PLANET = ["Mars", "Venus", "Jupiter", "Saturn", "Mercury"]
ELEMENT = ["Iron", "Gold", "Silver", "Bronze", "Steel"]


def port_065():
    # run_exp065_temporary_coordinate_alignment.py §3 (ll. 106-115, 227-344):
    # planet: is_rev=(i>=8), target_first=(i%2==1); element: is_rev=(i>=7),
    # target_first=(i%2==0). true_target/true_foil = (A,C) 2-hop, (A,D) 3-hop;
    # "target_token": " "+true_target, "foil_token": " "+true_foil.
    items = []
    for i, (iA, iB, iC) in enumerate(TRIPLES):
        A, B, C = PLANET[iA], PLANET[iB], PLANET[iC]
        target_first = (i % 2 == 1)
        q_opts = f"{A} or {C}" if target_first else f"{C} or {A}"
        if i < 8:
            p = f"Premise: {A} outranks {B}. {B} outranks {C}. Question: Who is higher in rank, {q_opts}? Answer:"
        else:
            p = f"Premise: {C} is lower than {B}. {B} is lower than {A}. Question: Who is higher in rank, {q_opts}? Answer:"
        items.append((" " + A, " " + C, p))
    for i, (iA, iB, iC, iD) in enumerate(QUADS):
        A, B, C, D = PLANET[iA], PLANET[iB], PLANET[iC], PLANET[iD]
        target_first = (i % 2 == 1)
        q_opts = f"{A} or {D}" if target_first else f"{D} or {A}"
        if i < 8:
            p = f"Premise: {A} outranks {B}. {B} outranks {C}. {C} outranks {D}. Question: Who is higher in rank, {q_opts}? Answer:"
        else:
            p = f"Premise: {D} is lower than {C}. {C} is lower than {B}. {B} is lower than {A}. Question: Who is higher in rank, {q_opts}? Answer:"
        items.append((" " + A, " " + D, p))
    for i, (iA, iB, iC) in enumerate(TRIPLES):
        A, B, C = ELEMENT[iA], ELEMENT[iB], ELEMENT[iC]
        target_first = (i % 2 == 0)
        q_opts = f"{A} or {C}" if target_first else f"{C} or {A}"
        if i < 7:
            p = f"Premise: {A} outranks {B}. {B} outranks {C}. Question: Who is higher in rank, {q_opts}? Answer:"
        else:
            p = f"Premise: {C} is lower than {B}. {B} is lower than {A}. Question: Who is higher in rank, {q_opts}? Answer:"
        items.append((" " + A, " " + C, p))
    for i, (iA, iB, iC, iD) in enumerate(QUADS):
        A, B, C, D = ELEMENT[iA], ELEMENT[iB], ELEMENT[iC], ELEMENT[iD]
        target_first = (i % 2 == 0)
        q_opts = f"{A} or {D}" if target_first else f"{D} or {A}"
        if i < 7:
            p = f"Premise: {A} outranks {B}. {B} outranks {C}. {C} outranks {D}. Question: Who is higher in rank, {q_opts}? Answer:"
        else:
            p = f"Premise: {D} is lower than {C}. {C} is lower than {B}. {B} is lower than {A}. Question: Who is higher in rank, {q_opts}? Answer:"
        items.append((" " + A, " " + D, p))
    return items


def port_066():
    # run_exp066_pythia410m_replication.py §3 (ll. 108-113, 223-344): same
    # structure as EXP065 (planet is_rev=(i>=8)/target_first odd;
    # element is_rev=(i>=7)/target_first even).
    return port_065()


def port_077():
    # run_exp077.py §3 benchmark (ll. 149-162, 586-636): bench dicts keep this
    # runner's schema ("prompt"/"A"/"C" with A=target, C=foil per l. 588).
    # Token encoding per ll. 725-727: tokenizer.encode(" "+item["A"])[0] etc.
    items = []
    for i, (iA, iB, iC) in enumerate(TRIPLES):
        A, B, C = PLANET[iA], PLANET[iB], PLANET[iC]
        target_first = (i % 2 == 1)
        q_opts = f"{A} or {C}" if target_first else f"{C} or {A}"
        if i < 8:
            p = f"Premise: {A} outranks {B}. {B} outranks {C}. Question: Who is higher in rank, {q_opts}? Answer:"
        else:
            p = f"Premise: {C} is lower than {B}. {B} is lower than {A}. Question: Who is higher in rank, {q_opts}? Answer:"
        items.append((" " + A, " " + C, p))
    for i, (iA, iB, iC, iD) in enumerate(QUADS):
        A, B, C, D = PLANET[iA], PLANET[iB], PLANET[iC], PLANET[iD]
        target_first = (i % 2 == 1)
        q_opts = f"{A} or {D}" if target_first else f"{D} or {A}"
        if i < 8:
            p = (f"Premise: {A} outranks {B}. {B} outranks {C}. {C} outranks {D}. "
                 f"Question: Who is higher in rank, {q_opts}? Answer:")
        else:
            p = (f"Premise: {D} is lower than {C}. {C} is lower than {B}. "
                 f"{B} is lower than {A}. Question: Who is higher in rank, {q_opts}? Answer:")
        items.append((" " + A, " " + D, p))
    for i, (iA, iB, iC) in enumerate(TRIPLES):
        A, B, C = ELEMENT[iA], ELEMENT[iB], ELEMENT[iC]
        target_first = (i % 2 == 0)
        q_opts = f"{A} or {C}" if target_first else f"{C} or {A}"
        if i < 7:
            p = f"Premise: {A} outranks {B}. {B} outranks {C}. Question: Who is higher in rank, {q_opts}? Answer:"
        else:
            p = f"Premise: {C} is lower than {B}. {B} is lower than {A}. Question: Who is higher in rank, {q_opts}? Answer:"
        items.append((" " + A, " " + C, p))
    for i, (iA, iB, iC, iD) in enumerate(QUADS):
        A, B, C, D = ELEMENT[iA], ELEMENT[iB], ELEMENT[iC], ELEMENT[iD]
        target_first = (i % 2 == 0)
        q_opts = f"{A} or {D}" if target_first else f"{D} or {A}"
        if i < 7:
            p = (f"Premise: {A} outranks {B}. {B} outranks {C}. {C} outranks {D}. "
                 f"Question: Who is higher in rank, {q_opts}? Answer:")
        else:
            p = (f"Premise: {D} is lower than {C}. {C} is lower than {B}. "
                 f"{B} is lower than {A}. Question: Who is higher in rank, {q_opts}? Answer:")
        items.append((" " + A, " " + D, p))
    return items


# Verbatim transcription guard (G1 support): the runners' own bridge formula,
# ported from run_exp065 ll. 485-487 / run_exp066 ll. 391-393 / run_exp077
# ll. 720-728:  w = E[tt,:] - E[ft,:]; w/(torch.norm(w)+1e-12).
def make_bridge_vec_runner(E, tt, ft):
    w = E[tt, :] - E[ft, :]
    return w / (torch.norm(w) + 1e-12)


def cp95(k, n):
    """Exact Clopper-Pearson 95% CI for k/n (beta-quantile form)."""
    if k == 0:
        lo = 0.0
    else:
        lo = float(beta_dist.ppf(0.025, k, n - k + 1))
    if k == n:
        hi = 1.0
    else:
        hi = float(beta_dist.ppf(0.975, k + 1, n - k))
    return lo, hi


# Sanity verification of the plan's verified kill bars (recomputed, not trusted).
assert cp95(39, 60)[0] > 0.5, "bar check: 39/60 must fire"
assert cp95(38, 60)[0] <= 0.5, "bar check: 38/60 must not fire"
assert cp95(21, 60)[1] < 0.5, "bar check: 21/60 must rule out"
assert cp95(22, 60)[1] >= 0.5, "bar check: 22/60 must not rule out"

# --- STEP 2 (part 2): build the three ports; guard transcription by demanding
# the three independent runner-code ports agree byte-for-byte (LOG-197
# established the four runners' item definitions are byte-identical 60/60).
items_by_run = {"EXP065": port_065(), "EXP066": port_066(), "EXP077": port_077()}
for rid, its in items_by_run.items():
    assert len(its) == 60, f"FATAL: {rid} port produced {len(its)} items, expected 60"
assert items_by_run["EXP065"] == items_by_run["EXP066"] == items_by_run["EXP077"], \
    "FATAL (G1-support): runner item ports disagree byte-for-byte"

# --- G2: label cross-check vs archived per-item records. ---
# G2-official (FATAL on mismatch): the official item definitions used by all
# endpoints. EXP066's port is byte-checked against archived prompts; the
# three-port byte agreement above chains EXP065 and EXP077-official to it.
ARCH066 = json.load(open(
    "experiments/runs/EXP066_pythia410m_replication/exp066_instance_evaluations.json"))
keys066 = list(ARCH066.keys())
assert len(keys066) == 60, "FATAL (G2): archived EXP066 records not 60"
for i, (t_str, f_str, p) in enumerate(items_by_run["EXP066"]):
    arch_p = ARCH066[keys066[i]]["prompt"]
    assert p == arch_p, f"FATAL (G2): EXP066 item {i} prompt mismatch vs archived record"
g2_066 = "60/60 byte-identical"
g2_065 = "via byte-identity chain (independent ports agree; EXP066 byte-verified)"

# G2-smoke: the plan (§2) premised that the smoke archive's ent/typ records are
# byte-consistent with the official bench port. That premise FAILS on the
# actual archive: the smoke records are entity-grouped (6 items per entity per
# domain) while the official runner construction yields a 21/7/2/0/0 target
# distribution. The smoke's per-item (target, foil) labels are unrecoverable
# (no prompts or per-item vectors archived). This is recorded as an
# [OBSERVATION] of a plan-premise defect, NOT a guard failure on the endpoint
# inputs: the smoke is labeled secondary only, contributes no endpoints, and
# its flip counts carry zero decision weight (§10.6). The endpoint-input
# labels (official chain) are verified above.
ARCH077SMOKE = json.load(open(
    "experiments/runs/EXP077_cone_vs_line/exp077_instance_records.json"))
assert len(ARCH077SMOKE) == 60, "FATAL (G2): archived EXP077 smoke records not 60"
smoke_ent = [r["ent"] for r in ARCH077SMOKE]
official_targets = [t.strip() for (t, f, p) in items_by_run["EXP077"]]
smoke_bench_matches_official = (smoke_ent == official_targets)
g2_077 = ("[OBSERVATION] plan-premise defect: smoke records entity-grouped "
          f"(6/entity/domain), official bench target distribution differs; "
          f"byte-match={smoke_bench_matches_official}; smoke per-item labels "
          "unrecoverable; smoke contributes flip counts (14,0) as labeled-"
          "secondary observation only, zero decision weight")
assert not smoke_bench_matches_official  # pin the observed defect state

print("STEP 2 done: G2", g2_065, "|", g2_066)

# ----------------------------------------------------------------------------
# STEP 1 (part 2): load run-pinned snapshots read-only; G3 hash gate; G6 sanity.
# ----------------------------------------------------------------------------
results = {}
models = {}
for rid, (hf_id, pin, arch_hash, alpha_run, dim, layer) in RUNS.items():
    tok, mdl = load_pinned(hf_id, pin)
    hash_fn = HASH_FN[rid]
    pre_hash = hash_fn(mdl)  # G3: Δθ=0 pre, with the run's own runner formulation
    assert pre_hash == arch_hash, f"FATAL (G3): {rid} pre_hash mismatch vs archived"
    E = mdl.get_output_embeddings().weight.detach().cpu().to(torch.float32)
    assert E.shape[1] == dim, f"FATAL: {rid} d mismatch {E.shape[1]} != {dim}"
    models[rid] = (tok, mdl, E, alpha_run)

    items = items_by_run[rid]
    t_ids = [tok.encode(t)[0] for (t, f, p) in items]
    f_ids = [tok.encode(f)[0] for (t, f, p) in items]

    # G6 sanity asserts (grounds A8's diagnostic).
    WU = E
    w_t = WU[t_ids, :]
    w_f = WU[f_ids, :]
    assert all(ti != fi for ti, fi in zip(t_ids, f_ids)), f"FATAL (G6): {rid} t_i == f_i"
    assert (torch.linalg.norm(w_t, dim=1) > 0).all(), f"FATAL (G6): {rid} zero-norm target row"
    assert (torch.linalg.norm(w_f, dim=1) > 0).all(), f"FATAL (G6): {rid} zero-norm foil row"

    # --- G1 bridge-identity guard: vectorized rebuild vs verbatim runner
    # formula (make_bridge_vec_runner), independent code paths; require
    # |cos| >= 1 - 1e-6 on all 60 items.
    b_batch = (w_t - w_f)
    b_batch = b_batch / (torch.linalg.norm(b_batch, dim=1, keepdim=True) + 1e-12)
    for i in range(60):
        b_runner = make_bridge_vec_runner(E, t_ids[i], f_ids[i])
        c = float(torch.dot(b_batch[i], b_runner))
        assert abs(c) >= 1 - 1e-6, f"FATAL (G1): {rid} item {i} |cos|={c}"
    g1 = "60/60 |cos| >= 1-1e-6 (vectorized vs runner-formula)"

    # --- STEP 3: endpoint (f): d_i = cos(-b̂_i, ŵ_{f_i}). ---
    n_t = torch.linalg.norm(w_t, dim=1, keepdim=True)
    n_f = torch.linalg.norm(w_f, dim=1, keepdim=True)
    what_t = w_t / n_t
    what_f = w_f / n_f
    d = (-b_batch * what_f).sum(dim=1)            # cos(-b̂, ŵ_f)
    # --- STEP 4: (a)-contrast: c_i = cos(b̂_i, ŵ_{t_i}). ---
    c = (b_batch * what_t).sum(dim=1)              # cos(b̂, ŵ_t)
    # --- STEP 5: joint geometry. ---
    cos_theta = (what_t * what_f).sum(dim=1)       # cosθ between rows
    d_np = d.numpy(); c_np = c.numpy(); ct_np = cos_theta.numpy()
    n = 60
    k_f = int((d_np >= 0.9).sum()); lo_f, hi_f = cp95(k_f, n)
    k_a = int((c_np >= 0.9).sum()); lo_a, hi_a = cp95(k_a, n)
    f_fire = lo_f > 0.5; f_out = hi_f < 0.5
    a_fire = lo_a > 0.5; a_out = hi_a < 0.5
    both = (d_np >= 0.9) & (c_np >= 0.9)
    both_idx = [int(i) for i in np.flatnonzero(both)]
    N_bothfire = int(both.sum())
    # G4: joint-lemma check on every both-fire item (cosθ <= -0.62 + 1e-6).
    for i in both_idx:
        assert ct_np[i] <= -0.62 + 1e-6, \
            f"FATAL (G4): {rid} both-fire item {i} cosθ={ct_np[i]} > -0.62: joint lemma refuted"
    anti_frac = float((ct_np <= -0.62).mean())  # [OBSERVATION] §10.5

    # --- STEP 6: archived flip counts (zero decision weight; §10.6). ---
    # --- STEP 7: D2 foil-shift diagnostic (report-only). ---
    dhat_f = alpha_run * (b_batch * w_f).sum(dim=1).numpy()  # L1-predicted Δℓ_{f,i}

    # --- A8: min over items of ‖W_U[t_i] - W_U[f_i]‖₂. ---
    a8_min = float(torch.linalg.norm(w_t - w_f, dim=1).min())

    post_hash = hash_fn(mdl)  # G3: Δθ=0 post
    assert post_hash == arch_hash, f"FATAL (G3): {rid} post_hash mismatch"
    assert post_hash == pre_hash, f"FATAL (G3): {rid} pre != post (Δθ ≠ 0)"

    results[rid] = dict(
        hf_id=hf_id, snapshot=pin, alpha_run=alpha_run, d=dim, layer=layer, N=60,
        t_ids=t_ids, f_ids=f_ids,
        d_arr=d_np.tolist(), c_arr=c_np.tolist(), cos_theta_arr=ct_np.tolist(),
        d_mean=float(d_np.mean()), d_median=float(np.median(d_np)),
        d_min=float(d_np.min()), d_max=float(d_np.max()),
        c_mean=float(c_np.mean()), c_median=float(np.median(c_np)),
        c_min=float(c_np.min()), c_max=float(c_np.max()),
        k_f=k_f, p_hat_f=k_f / n, cp95_f=[lo_f, hi_f],
        k_a=k_a, p_hat_a=k_a / n, cp95_a=[lo_a, hi_a],
        f_fires=bool(f_fire), f_ruled_out=bool(f_out),
        a_fires=bool(a_fire), a_ruled_out=bool(a_out),
        both_fire_idx=both_idx, N_bothfire=N_bothfire,
        anti_aligned_frac=anti_frac,
        dhat_f_arr=dhat_f.tolist(),
        A8_min_norm=float(a8_min),
        g1=g1, g2={"EXP065": g2_065, "EXP066": g2_066, "EXP077": g2_077}[rid],
        pre_hash=pre_hash, post_hash=post_hash, hash_match_archived=True,
        hash_formulation={"EXP065": "run_exp065 ll.33-37 (model.parameters() order)",
                          "EXP066": "run_exp066 ll.34-38 (model.parameters() order)",
                          "EXP077": "run_exp077 ll.166-172 (sorted state_dict, float32)"}[rid],
    )
    print(f"STEP 1-7 {rid}: G3 Δθ=0 {pre_hash[:12]}… ok | G1 {g1.split('(')[0].strip()} | "
          f"(f): k={k_f}/60 CI[{lo_f:.4f},{hi_f:.4f}] fire={f_fire} out={f_out} | "
          f"(a): k={k_a}/60 CI[{lo_a:.4f},{hi_a:.4f}] fire={a_fire} out={a_out} | "
          f"N_bothfire={N_bothfire} | A8_min={a8_min:.4f}")

# STEP 6 (archived flip counts; [OBSERVATION], zero decision weight).
FLIPS = {
    # EXP065: exp065_results.json -> stage_B_confirmatory_results.Same_Layer_Output_Bridge
    "EXP065": (10, 0, "exp065_results.json"),
    # EXP066: exp066_replication_results.json -> stage_B_conditions.Same_Layer_Output_Bridge
    "EXP066": (8, 0, "exp066_replication_results.json"),
    # EXP077 official GPU: LOG-197 E4 pin (b=6, c=0), research_log.md LOG-128
    "EXP077": (6, 0, "LOG-128 official GPU (notebook mirror)"),
    # EXP077 smoke: labeled secondary, exp077_results.json -> stage_B_conditions.C8_bridge
    "EXP077-smoke": (14, 0, "exp077_results.json (labeled secondary)"),
}
r65 = json.load(open("experiments/runs/EXP065_coordinate_alignment/exp065_results.json"))
assert (r65["stage_B_confirmatory_results"]["Same_Layer_Output_Bridge"]["rescues_b"],
        r65["stage_B_confirmatory_results"]["Same_Layer_Output_Bridge"]["corruptions_c"]) == (10, 0)
r66 = json.load(open("experiments/runs/EXP066_pythia410m_replication/exp066_replication_results.json"))
assert (r66["stage_B_conditions"]["Same_Layer_Output_Bridge"]["rescues_b"],
        r66["stage_B_conditions"]["Same_Layer_Output_Bridge"]["corruptions_c"]) == (8, 0)
r77s = json.load(open("experiments/runs/EXP077_cone_vs_line/exp077_results.json"))
assert (r77s["stage_B_conditions"]["C8_bridge"]["b"],
        r77s["stage_B_conditions"]["C8_bridge"]["c"]) == (14, 0)

# STEP 7 (part 2): D2 archived aggregate shifts [REPORT-ONLY].
AGG = {
    "EXP065": (r65["stage_B_confirmatory_results"]["Same_Layer_Output_Bridge"]["delta_logit_target"],
               r65["stage_B_confirmatory_results"]["Same_Layer_Output_Bridge"]["delta_logit_foil"]),
    "EXP066": (r66["stage_B_conditions"]["Same_Layer_Output_Bridge"]["delta_logit_target"],
               r66["stage_B_conditions"]["Same_Layer_Output_Bridge"]["delta_logit_foil"]),
    "EXP077": (None, None),  # no archived logit shifts — recorded unavailable
}

# --- §7 per-run verdict mapping (filled verbatim from the plan table). ---
def per_run_verdict(r):
    ff, fo, af, ao = r["f_fires"], r["f_ruled_out"], r["a_fires"], r["a_ruled_out"]
    assert not (ff and fo) and not (af and ao), "unreachable"
    if ff and ao:
        return "Supported — pure foil-suppression tilt"
    if ff and not af and not ao:
        return "Supported — foil-suppression tilt (target-boost not ruled out)"
    if ff and af:
        if r["N_bothfire"] == 0:
            return "Supported — antipodal-axis readout tilt [Inconclusive-on-antipodal: both majority cells fired on disjoint item sets; antipodal reading NOT licensed]"
        return "Supported — antipodal-axis readout tilt (boost ≡ suppression; joint lemma verified per both-fire item)"
    if fo:
        return "Not supported — foil-suppression reading killed ((a) cell recorded)"
    return "Inconclusive"

for rid in RUNS:
    results[rid]["verdict"] = per_run_verdict(results[rid])
    print(f"STEP 7 verdict {rid}: {results[rid]['verdict']}")

# EXP070: Underdetermined (excluded by plan §1.1/A4).
results["EXP070"] = {"verdict": "Underdetermined",
                     "note": "no verified exp070_vectors record; excluded from all endpoints"}

# Program-level aggregation (pre-registered, §7).
primary = [results[r]["verdict"] for r in RUNS]
n_supported = sum(v.startswith("Supported") for v in primary)
n_notsup = sum(v.startswith("Not supported") for v in primary)
if n_supported >= 1:
    program_verdict = "EXP082-SUPPORTED (foil-suppression tilt)"
elif n_notsup == 3:
    program_verdict = "EXP082-EXONERATED (foil-suppression Not supported)"
else:
    program_verdict = "EXP082-Inconclusive"
print("PROGRAM VERDICT:", program_verdict)

# ----------------------------------------------------------------------------
# STEP 8: machine-readable twin JSON.
# ----------------------------------------------------------------------------
twin = {
    "experiment": "EXP082",
    "log": "LOG-217 (executor); plan LOG-214; Law#14 SIGN LOG-215 + LOG-215b",
    "date": "2026-09-23",
    "budget": "$0 CPU; 0 forward passes; read-only weight reads + archived records",
    "env": {
        "venv": "/home/hatch/workspace/.venv_smoke",
        "torch": torch.__version__, "transformers": transformers.__version__,
        "numpy": np.__version__, "scipy": scipy.__version__,
        "python": sys.version.split()[0], "platform": platform.platform(),
    },
    "forward_passes": 0,
    "rng_consumed": False,
    "guards": {"G1": "pass", "G2": "pass (official chain; smoke archive premised-defect recorded as observation)",
               "G3": "pass (pre==post==archived; per-runner verbatim hash formulation — see hash_formulation; plan's single-formulation pin corrected LOG-217)",
               "G4": "pass (checked per both-fire item; no violations)",
               "G5": "no model(...) call on inputs (code inspection)",
               "G6": "pass"},
    "g2_detail": {"EXP065": g2_065, "EXP066": g2_066, "EXP077": g2_077},
    "runs": results,
    "flip_counts_observation_zero_weight": FLIPS,
    "d2_archived_aggregate_shifts": AGG,
    "verdicts": {r: results[r]["verdict"] for r in list(RUNS) + ["EXP070"]},
    "program_verdict": program_verdict,
}
with open("research/analysis_plans/EXP082_RESULTS_LOG217_2026-09-23.json", "w") as fh:
    json.dump(twin, fh)
print("STEP 8 done: twin JSON written")

# ----------------------------------------------------------------------------
# STEP 9 is the markdown report (written next by the operator, not here).
# ----------------------------------------------------------------------------
print("STEP 9: report to be written separately")
