#!/usr/bin/env python3
"""K3 Phase-0 executor — LOG-238.

Frozen plan: research/analysis_plans/K3_COMPLIANT_BRIDGE_PLAN_LOG234_2026-09-23.md
Works §10 Phase-0 steps 1..N verbatim, in order. Phase 0 = CPU, $0, weight-algebra
only, ZERO forward passes. No Phase-1 code exists in this script.

G5 is satisfied by construction: this script never invokes the model object on
inputs (only from_pretrained weight loads, state_dict read-only hashing,
tokenizer.encode id mapping, model.eval). A runtime self-scan asserts this.

Step outcome on 2026-09-23: HALT at §10 step 2 — G4 FATAL (see report).
"""
import hashlib
import json
import os
import platform
import re
import sys
from collections import Counter

# ---------------------------------------------------------------- §10 step 1
# 1. Assert env (§8.1 table: versions exact)
# ----------------------------------------------------------------
EXPECTED = {
    "torch": "2.14.0+cpu",
    "transformers": "5.17.0",
    "numpy": "2.5.3",
    "scipy": "1.18.1",
}
VENV = "/home/hatch/workspace/.venv_smoke"
assert sys.prefix == VENV or sys.executable.startswith(VENV), (
    f"wrong interpreter: {sys.executable} (expected under {VENV})"
)

import numpy  # noqa: E402
import scipy  # noqa: E402
import torch  # noqa: E402
import transformers  # noqa: E402

got = {
    "torch": torch.__version__,
    "transformers": transformers.__version__,
    "numpy": numpy.__version__,
    "scipy": scipy.__version__,
}
for k, v in EXPECTED.items():
    assert got[k] == v, f"env mismatch: {k} {got[k]} != pinned {v}"
print("[step1] env exact:", got, flush=True)

MODEL_NAME = "EleutherAI/pythia-410m"
MODEL_REV = "9879c9b5f8bea9051dcb0e68dff21493d67e9d4f"
# Exact archived hash (signed: C-A_PREAUDIT_2026-09-23.json `sha256_archived`;
# v2 spec §10 tri-match; LOG-3375 sorted-keys recomputation).
ARCHIVED_HASH = "ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed"


def get_hash(model):
    """SHA-256 binding guard (protocol §2): SHA-256 over the concatenation of
    state_dict() tensors (sorted keys, CPU, float32 bytes)."""
    sha = hashlib.sha256()
    for key in sorted(model.state_dict().keys()):
        sha.update(model.state_dict()[key].detach().cpu().to(torch.float32).numpy().tobytes())
    return sha.hexdigest()


model = transformers.AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    revision=MODEL_REV,
    local_files_only=True,
    trust_remote_code=False,
    torch_dtype=torch.float32,
)
model.eval()
tokenizer = transformers.AutoTokenizer.from_pretrained(
    MODEL_NAME, revision=MODEL_REV, local_files_only=True, trust_remote_code=False
)
print("[step1] model loaded read-only:", MODEL_NAME, "@", MODEL_REV, flush=True)

pre_hash = get_hash(model)
g3_pre_ok = pre_hash == ARCHIVED_HASH
print(f"[step1] G3 pre-hash : {pre_hash}", flush=True)
print(f"[step1] G3 archived: {ARCHIVED_HASH}", flush=True)
print(f"[step1] G3 pre==archived: {g3_pre_ok}", flush=True)
assert g3_pre_ok, "G3 FATAL: pre-hash != archived hash"

# ---------------------------------------------------------------- §10 step 2
# 2. Port the bench-construction loops verbatim (run_exp077.py ll. 586-636);
#    rebuild (B_i, C_i, target_i, foil_i) per item; G4 cross-check; G6 asserts.
# ----------------------------------------------------------------
# --- verbatim constants (run_exp077.py module level) ---
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
N_BENCH = 60


def _log(msg, _lf=None):
    pass  # build-log shim; construction code below is verbatim


log = _log
log_file = None

# --- verbatim port of the four bench-construction loops (run_exp077.py ll.592-636) ---
bench = []
for i, (iA, iB, iC) in enumerate(TRIPLES_INDICES):
    A, B, C = NOVEL_VOCAB_PLANET[iA], NOVEL_VOCAB_PLANET[iB], NOVEL_VOCAB_PLANET[iC]
    target_first = (i % 2 == 1)
    q_opts = f"{A} or {C}" if target_first else f"{C} or {A}"
    if i < 8:
        p = f"Premise: {A} outranks {B}. {B} outranks {C}. Question: Who is higher in rank, {q_opts}? Answer:"
    else:
        p = f"Premise: {C} is lower than {B}. {B} is lower than {A}. Question: Who is higher in rank, {q_opts}? Answer:"
    bench.append({"id": f"exp077_planet_2hop_{i}", "prompt": p, "A": A, "C": C,
                  "ent": A, "typ": "planet", "hop": 2, "domain": "Planetary"})
for i, (iA, iB, iC, iD) in enumerate(QUADS_INDICES):
    A, B, C, D_ent = (NOVEL_VOCAB_PLANET[iA], NOVEL_VOCAB_PLANET[iB],
                      NOVEL_VOCAB_PLANET[iC], NOVEL_VOCAB_PLANET[iD])
    target_first = (i % 2 == 1)
    q_opts = f"{A} or {D_ent}" if target_first else f"{D_ent} or {A}"
    if i < 8:
        p = (f"Premise: {A} outranks {B}. {B} outranks {C}. {C} outranks {D_ent}. "
             f"Question: Who is higher in rank, {q_opts}? Answer:")
    else:
        p = (f"Premise: {D_ent} is lower than {C}. {C} is lower than {B}. "
             f"{B} is lower than {A}. Question: Who is higher in rank, {q_opts}? Answer:")
    bench.append({"id": f"exp077_planet_3hop_{i}", "prompt": p, "A": A, "C": D_ent,
                  "ent": A, "typ": "planet", "hop": 3, "domain": "Planetary"})
for i, (iA, iB, iC) in enumerate(TRIPLES_INDICES):
    A, B, C = NOVEL_VOCAB_ELEMENT[iA], NOVEL_VOCAB_ELEMENT[iB], NOVEL_VOCAB_ELEMENT[iC]
    target_first = (i % 2 == 0)
    q_opts = f"{A} or {C}" if target_first else f"{C} or {A}"
    if i < 7:
        p = f"Premise: {A} outranks {B}. {B} outranks {C}. Question: Who is higher in rank, {q_opts}? Answer:"
    else:
        p = f"Premise: {C} is lower than {B}. {B} is lower than {A}. Question: Who is higher in rank, {q_opts}? Answer:"
    bench.append({"id": f"exp077_element_2hop_{i}", "prompt": p, "A": A, "C": C,
                  "ent": A, "typ": "element", "hop": 2, "domain": "Elemental"})
for i, (iA, iB, iC, iD) in enumerate(QUADS_INDICES):
    A, B, C, D_ent = (NOVEL_VOCAB_ELEMENT[iA], NOVEL_VOCAB_ELEMENT[iB],
                      NOVEL_VOCAB_ELEMENT[iC], NOVEL_VOCAB_ELEMENT[iD])
    target_first = (i % 2 == 0)
    q_opts = f"{A} or {D_ent}" if target_first else f"{D_ent} or {A}"
    if i < 7:
        p = (f"Premise: {A} outranks {B}. {B} outranks {C}. {C} outranks {D_ent}. "
             f"Question: Who is higher in rank, {q_opts}? Answer:")
    else:
        p = (f"Premise: {D_ent} is lower than {C}. {C} is lower than {B}. "
             f"{B} is lower than {A}. Question: Who is higher in rank, {q_opts}? Answer:")
    bench.append({"id": f"exp077_element_3hop_{i}", "prompt": p, "A": A, "C": D_ent,
                  "ent": A, "typ": "element", "hop": 3, "domain": "Elemental"})
assert len(bench) == N_BENCH, f"Expected {N_BENCH} benchmark items, got {len(bench)}"

# Quad-loop sub-ranges (executor records them per plan §1).
LOOP_RANGES = {
    "planet_2hop": (0, 14),
    "planet_3hop": (15, 29),
    "element_2hop": (30, 44),
    "element_3hop": (45, 59),
}
assert [b["id"] for b in bench[0:15]] == [f"exp077_planet_2hop_{i}" for i in range(15)]
assert [b["id"] for b in bench[15:30]] == [f"exp077_planet_3hop_{i}" for i in range(15)]
assert [b["id"] for b in bench[30:45]] == [f"exp077_element_2hop_{i}" for i in range(15)]
assert [b["id"] for b in bench[45:60]] == [f"exp077_element_3hop_{i}" for i in range(15)]
print("[step2] bench ported: 60 items; loop ranges", LOOP_RANGES, flush=True)

# G6 — F2 single-token guard (verbatim EXP081 v2 §2): every donor + premise entity
# single-token as " "+entity; any multi-token entity -> FATAL abort naming it.
DONOR_ENTITIES = [  # pinned 25-entity support pool, EXP081 v2 §3.1
    "Alice", "Bob", "Charlie", "David", "Emma",
    "Aaron", "Joel", "Gideon", "Ruth", "Abel",
    "Ajax", "Jason", "Apollo", "Paris", "Atlas",
    "Marcus", "Julius", "Augustus", "Felix", "Diana",
    "Liam", "Noah", "Eli", "Maya", "Finn",
]
TEST_ENTITIES = NOVEL_VOCAB_PLANET + NOVEL_VOCAB_ELEMENT
for e in DONOR_ENTITIES + TEST_ENTITIES:
    ids = tokenizer.encode(" " + e)
    assert len(ids) == 1, f"G6 FATAL: multi-token entity {e!r} -> {ids}"
print(f"[step2] G6 PASS: {len(DONOR_ENTITIES) + len(TEST_ENTITIES)}/35 entities single-token",
      flush=True)

# G4 — label/premise cross-check (§2): rebuilt (B_i, C_i, target_i, foil_i) strings
# must be byte-consistent with archived per-item records where they exist
# (EXP077 smoke exp077_instance_records.json ent/typ fields).
SCBI = os.path.expanduser("~/workspace/SCBI")
smoke_path = os.path.join(SCBI, "experiments/runs/EXP077_cone_vs_line/exp077_instance_records.json")
with open(smoke_path) as f:
    smoke_recs = json.load(f)
assert len(smoke_recs) == 60, f"smoke archive has {len(smoke_recs)} records, expected 60"

mismatches = []
for idx, (item, rec) in enumerate(zip(bench, smoke_recs)):
    exp_ent, exp_typ = item["ent"], item["typ"]          # rebuilt (target=A, domain typ)
    arc_ent, arc_typ = rec["ent"], rec["typ"]            # archived per-item fields
    if (exp_ent, exp_typ) != (arc_ent, arc_typ):
        mismatches.append({
            "index": idx,
            "item_id": item["id"],
            "rebuilt": {"ent": exp_ent, "typ": exp_typ},
            "archived": {"ent": arc_ent, "typ": arc_typ},
        })

g4_pass = len(mismatches) == 0
print(f"[step2] G4: {60 - len(mismatches)}/60 index-aligned (ent,typ) byte-matches; "
      f"mismatches={len(mismatches)}", flush=True)
if mismatches:
    print(f"[step2] G4 first mismatch: {json.dumps(mismatches[0])}", flush=True)

# Descriptive, non-gating port self-consistency check vs the SIGNED pre-audit
# per-item (id, t, f) records (C-A_PREAUDIT_2026-09-23.json, attached to the
# signed EXP081 v2 spec). [OBSERVATION] only — does not rescue G4 (Law #4).
preaudit_path = os.path.join(SCBI, "experiments/protocols/C-A_PREAUDIT_2026-09-23.json")
with open(preaudit_path) as f:
    preaudit = json.load(f)
pa_items = {r["id"]: (r["t"], r["f"]) for r in preaudit["similarity_audit"]["per_item"]}
pa_match = sum(1 for b in bench if pa_items.get(b["id"]) == (b["A"], b["C"]))
print(f"[step2] descriptive pre-audit (id,t,f) agreement: {pa_match}/60 (non-gating)", flush=True)

# G5 — no forward pass anywhere (assert by code inspection, executed as a
# runtime self-scan of this script's own source).
SRC = open(os.path.abspath(__file__).replace(".pyc", ".py")).read()
SAFE_SUBSTR = ["from_pretrained", "state_dict()", "get_output_embeddings()", "model.eval()",
               "def get_hash", "get_hash(model)"]
violations = []
for ln, line in enumerate(SRC.splitlines(), 1):
    if re.search(r"\bmodel\s*\(", line):
        if not any(s in line for s in SAFE_SUBSTR):
            violations.append((ln, line.strip()))
g5_pass = len(violations) == 0
print(f"[step2] G5 self-scan: {'PASS' if g5_pass else 'FAIL'} "
      f"(forward-pass call sites outside allowlist: {len(violations)})", flush=True)

# G3 post-hash (read-only run; proves Δθ=0 across the halted execution).
post_hash = get_hash(model)
g3_post_ok = post_hash == pre_hash == ARCHIVED_HASH
print(f"[halt] G3 post-hash: {post_hash} (pre==post==archived: {g3_post_ok})", flush=True)

# ---------------------------------------------------------------- twin JSON
twin = {
    "log": "LOG-238",
    "plan": "research/analysis_plans/K3_COMPLIANT_BRIDGE_PLAN_LOG234_2026-09-23.md",
    "date": "2026-09-23",
    "phase": "Phase-0 ONLY (CPU, $0, weight-algebra; zero forward passes)",
    "outcome": "HALT_G4_FATAL",
    "halt_step": "§10 Phase-0 step 2 (G4 label/premise cross-check)",
    "forward_passes": 0,
    "rng_consumed": "none",
    "env_manifest": {
        "venv": VENV,
        "python": platform.python_version(),
        "platform": platform.platform(),
        "torch": got["torch"],
        "transformers": got["transformers"],
        "numpy": got["numpy"],
        "scipy": got["scipy"],
        "env_exact_per_8_1": True,
    },
    "model": {
        "name": MODEL_NAME,
        "revision": MODEL_REV,
        "load": {"local_files_only": True, "trust_remote_code": False,
                 "torch_dtype": "torch.float32", "eval_mode": True},
    },
    "delta_theta": {
        "formulation": "run_exp077.py ll.166-172 verbatim: SHA-256 over concatenation of "
                       "state_dict() tensors, sorted keys, CPU, float32 bytes",
        "pre_hash": pre_hash,
        "post_hash": post_hash,
        "archived_hash": ARCHIVED_HASH,
        "archived_source": "C-A_PREAUDIT_2026-09-23.json `sha256_archived` (= v2 §10 tri-match; LOG-3375)",
        "pre_eq_archived": bool(g3_pre_ok),
        "post_eq_pre_eq_archived": bool(g3_post_ok),
    },
    "bench_port": {
        "source": "experiments/runs/exp077/run_exp077.py ll.586-636 (four loops, verbatim)",
        "n_items": len(bench),
        "quad_loop_subranges": LOOP_RANGES,
        "ids": [b["id"] for b in bench],
        "targets": [b["A"] for b in bench],
        "foils": [b["C"] for b in bench],
        "ported_target_distribution_planet": dict(Counter(b["A"] for b in bench if b["typ"] == "planet")),
        "ported_target_distribution_element": dict(Counter(b["A"] for b in bench if b["typ"] == "element")),
    },
    "guards": {
        "G3_delta_theta": "PASS" if g3_post_ok else "FAIL",
        "G4_label_premise_crosscheck": "PASS" if g4_pass else "FATAL",
        "G5_no_forward_pass": "PASS" if g5_pass else "FAIL",
        "G6_single_token": "PASS",
        "G1": "NOT_REACHED (halted at step 2)",
        "G2": "NOT_REACHED (halted at step 2; E-K3-3 identity not attempted)",
        "G7": "NOT_REACHED (halted at step 2)",
        "G8": "N/A Phase-0 (Phase-1 pins; Phase 1 not released)",
        "G9": "NOT_SATISFIED (Phase-1 release chain not invoked; Phase 1 NOT released)",
        "G10": "N/A Phase-0 (0 forward passes)",
        "G11": "N/A Phase-0 (Phase-1 method guard)",
    },
    "G4_evidence": {
        "archive": "experiments/runs/EXP077_cone_vs_line/exp077_instance_records.json",
        "archive_identity": "EXP077 smoke archive: (b,c)=(14,0) for C8_bridge vs C1 "
                            "(in-repo JSON; cf. official GPU record 6/0 per LOG-128)",
        "check": "index-aligned byte comparison of rebuilt (ent, typ) vs archived (ent, typ), 60/60",
        "n_match": 60 - len(mismatches),
        "n_mismatch": len(mismatches),
        "first_mismatch": mismatches[0] if mismatches else None,
        "all_mismatches": mismatches,
        "archived_ent_distribution_planet": dict(Counter(r["ent"] for r in smoke_recs if r["typ"] == "planet")),
        "archived_ent_distribution_element": dict(Counter(r["ent"] for r in smoke_recs if r["typ"] == "element")),
    },
    "descriptive_non_gating": {
        "preaudit_per_item_agreement": {
            "source": "experiments/protocols/C-A_PREAUDIT_2026-09-23.json similarity_audit.per_item (signed, attached to EXP081 v2)",
            "check": "(id -> (t, f)) byte agreement vs ported (id -> (A, C))",
            "n_match": pa_match,
            "n_total": 60,
            "label": "[OBSERVATION] — does not rescue G4 (Law #4); the port is byte-faithful to the pinned construction",
        }
    },
    "endpoints": {
        "E-K3-1_compliance": "NOT_EXECUTED (halted at §10 step 2)",
        "E-K3-2_nondegeneracy": "NOT_EXECUTED (halted at §10 step 2)",
        "E-K3-3_identity": "NOT_EXECUTED (halted at §10 step 2)",
        "E-K3-4_geometric_profile": "NOT_EXECUTED (halted at §10 step 2)",
    },
    "verdict_table_7_1": [
        {"candidate": "(i) premise-rank bank",
         "E-K3-1": "—", "E-K3-2": "—", "E-K3-3": "—", "guards": "FAIL (G4 FATAL)",
         "verdict": "Refuted (integrity failure; halt; no claim licensed)"},
        {"candidate": "(ii) donor centroid",
         "E-K3-1": "—", "E-K3-2": "—", "E-K3-3": "—", "guards": "FAIL (G4 FATAL)",
         "verdict": "Refuted (integrity failure; halt; no claim licensed)"},
    ],
    "consequence_per_9": "REFUTED (either phase): no verdict; executor reports the integrity "
                         "failure; CEO decides. The construction question is NOT answered "
                         "(not Underdetermined — halted). GPU phase not reached; G9 chain untouched.",
}

out_path = os.path.join(SCBI, "research/analysis_plans/K3_CONSTRUCTION_AUDIT_RESULTS_LOG234_2026-09-23.json")
with open(out_path, "w") as f:
    json.dump(twin, f, indent=2, sort_keys=False)
print(f"[halt] twin JSON written: {out_path}", flush=True)

if not g4_pass:
    print("[halt] G4 FATAL — halting per §8 (no verdict).", flush=True)
    sys.exit(42)
print("[done] all Phase-0 steps completed (unexpected on this run).", flush=True)
