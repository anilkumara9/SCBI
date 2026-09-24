"""
K2 — Routing-vs-Bypass Discriminator: execution bundle (LOG-226, Track-4).
Pre-registered protocol (SIGNED, LOG-224c):
    research/analysis_plans/K2_ROUTING_BYPASS_PLAN_LOG223_REV2_2026-09-23.md

================================================================================
DO NOT EXECUTE on GPU before CEO GPU clearance.
================================================================================
This bundle runs in two phases:
  Phase 0 (CPU, always runs): tokenizer pin (checklist B, LOG-224c Ruling 6),
      CPU identity dry run (pre-execution gate A, LOG-224c Ruling 7),
      benchmark reconstruction + G2 cross-check, entity masks (G8),
      G10 disjointness + exclusion floor, archived baseline load.
  Phase 1 (GPU): runs ONLY with --ceo-gpu-clearance. 180 forward passes
      (60 items x 3 arms) on pythia-410m/L20/alpha=0.5, smoke bench.

K2-P = exactly 180 passes: (a) final-token-only injection,
(b) premise-entity-position injection, (c) all-positions positive control.
Baseline correctness is ARCHIVED (smoke bench C1) — zero re-baselining passes.

Construction base: experiments/runs/exp077/run_exp077.py (§3 constants for the
benchmark; §4 C8 `make_bridge_vec` verbatim for the bridge vector).
Bridge vectors are built by CONSTRUCTION-IDENTITY (REV2 G1) — no per-item
vector archive exists (LOG-224b retraction); identity is licensed by
deterministic reconstruction + the live (c)-gate, graded [INFERENCE].

Guards (REV2 §4, numbering binding): G1 construction-identity, G2 label
cross-check, G3 Delta theta = 0 (sha256 pre/post), G4 no-forward-pass-
except-licensed (exactly 3*N_actual), G5 (c)-reproduction gate (b_c >= 6
else INVALID -> Underdetermined), G6 EXP070 excluded, G7 Law #7 provenance
note, G8 entity-mapping, G9 LayerNorm-scale diagnostic (diagnostic only),
G10 disjointness + exclusion floor (>6 -> Underdetermined).

Governing standards: AGENTS.md 14 Inviolable Laws (Law 6: Delta theta = 0;
Law 7: zero leakage; Law 8: halts are reportable; Law 11: epistemic labels;
Law 13: archiving), Law #15 (seeded, hashed, smoke-tested, logged +
evaluator tests).
"""

import os
import sys
import json
import math
import argparse
import hashlib

import numpy as np

# Local bundle modules (pure stdlib; importable without torch).
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from k2_endpoints import (paired_contrast_stats, adjudicate_verdict, SUPPORTED,
                          NOT_SUPPORTED, INCONCLUSIVE, UNDERDETERMINED, REFUTED)
from k2_guards import (g1_invalid_check, g4_pass_count_check, g5_c_gate_check,
                       g10_exclusion_floor_check, gate_a_evaluate,
                       checklist_b_record, g3_delta_theta_check,
                       guards_evaluate, N_ITEMS, C_GATE_MDE_B,
                       G1_INVALID_FAILURES, NORM_REL_TOL, DELTA_MIN)

# ----------------------------------------------------------------------------
# Configuration (REV2 §3.1/§3.2 — frozen)
# ----------------------------------------------------------------------------
MODEL_NAME = "EleutherAI/pythia-410m"
D = 1024
N_LAYERS = 24
TARGET_LAYER = 20          # l* = 20, same hook site as the archived runs
ALPHA = 0.50               # per-position injection scale (EXP066's calibrated alpha)
N_BENCH = 60
N_ARMS = 3
PASSES_PER_PIN = 180       # 60 items x 3 arms (G4 binds to 3 * N_actual)

SEED_TORCH = 20260923
SEED_NUMPY = 20260923

# Pinned archives (read-only inputs; nothing else is touched).
ARCH_DIR = os.path.join("experiments", "runs", "EXP077_cone_vs_line")
ARCH_RECORDS = os.path.join(ARCH_DIR, "exp077_instance_records.json")
ARCH_RESULTS = os.path.join(ARCH_DIR, "exp077_results.json")
ARCH_VECTORS = os.path.join(ARCH_DIR, "exp077_vectors.pt")

# Rescue anchor (reviewer-verified, exp077_results.json -> bridge_gate) [FACT].
ANCHOR = {"delta_m": 0.23333333333333334, "b": 14, "c": 0,
          "p": 0.0001220703125, "baseline_acc": 0.60}

# Build-time reference tokenizer pin (observed 2026-09-23; warn-only reference).
PINNED_HF_REVISION = "9879c9b5f8bea9051dcb0e68dff21493d67e9d4f"

# ----------------------------------------------------------------------------
# Benchmark construction — ported VERBATIM from
# experiments/runs/exp077/run_exp077.py §3 (constants + builder).
# The smoke bench records (exp077_instance_records.json) were written by this
# same builder; G2 cross-checks ent/typ per index against the archive.
# ----------------------------------------------------------------------------
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


def build_benchmark():
    """The EXP065/066/077-identical N=60 suite, ported verbatim (see §3 above)."""
    bench = []
    for i, (iA, iB, iC) in enumerate(TRIPLES_INDICES):
        A, B, C = NOVEL_VOCAB_PLANET[iA], NOVEL_VOCAB_PLANET[iB], NOVEL_VOCAB_PLANET[iC]
        target_first = (i % 2 == 1)
        q_opts = f"{A} or {C}" if target_first else f"{C} or {A}"
        if i < 8:
            p = f"Premise: {A} outranks {B}. {B} outranks {C}. Question: Who is higher in rank, {q_opts}? Answer:"
        else:
            p = f"Premise: {C} is lower than {B}. {B} is lower than {A}. Question: Who is higher in rank, {q_opts}? Answer:"
        bench.append({"id": f"k2_planet_2hop_{i}", "prompt": p, "A": A, "C": C,
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
        bench.append({"id": f"k2_planet_3hop_{i}", "prompt": p, "A": A, "C": D_ent,
                      "ent": A, "typ": "planet", "hop": 3, "domain": "Planetary"})
    for i, (iA, iB, iC) in enumerate(TRIPLES_INDICES):
        A, B, C = NOVEL_VOCAB_ELEMENT[iA], NOVEL_VOCAB_ELEMENT[iB], NOVEL_VOCAB_ELEMENT[iC]
        target_first = (i % 2 == 0)
        q_opts = f"{A} or {C}" if target_first else f"{C} or {A}"
        if i < 7:
            p = f"Premise: {A} outranks {B}. {B} outranks {C}. Question: Who is higher in rank, {q_opts}? Answer:"
        else:
            p = f"Premise: {C} is lower than {B}. {B} is lower than {A}. Question: Who is higher in rank, {q_opts}? Answer:"
        bench.append({"id": f"k2_element_2hop_{i}", "prompt": p, "A": A, "C": C,
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
        bench.append({"id": f"k2_element_3hop_{i}", "prompt": p, "A": A, "C": D_ent,
                      "ent": A, "typ": "element", "hop": 3, "domain": "Elemental"})
    assert len(bench) == N_BENCH, f"expected {N_BENCH} items, got {len(bench)}"
    return bench


# ----------------------------------------------------------------------------
# Small utilities
# ----------------------------------------------------------------------------

def log(msg, log_file=None):
    print(msg, flush=True)
    if log_file:
        log_file.write(msg + "\n")
        log_file.flush()


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def get_hash(model):
    """REV2 G3: SHA-256 over sorted state_dict keys (CPU, float32 bytes)."""
    import torch
    sha = hashlib.sha256()
    for key in sorted(model.state_dict().keys()):
        sha.update(model.state_dict()[key].detach().cpu().to(torch.float32).numpy().tobytes())
    return sha.hexdigest()


# ----------------------------------------------------------------------------
# Ruling 6 — tokenizer pin (LOG-224c): sha256 of the resolved tokenizer
# payload as loaded + the exact HF commit SHA, logged at vector-build time.
# Checksum scheme (documented for reproducibility): for each existing file in
# the fixed ordered list below, feed filename + b"\x00" + file bytes.
# A missing log is a RECORDED DEVIATION, not an INVALID.
# ----------------------------------------------------------------------------
TOKENIZER_PAYLOAD_FILES = ["tokenizer.json", "tokenizer_config.json",
                           "special_tokens_map.json", "vocab.json",
                           "merges.txt", "added_tokens.json"]


def resolve_tokenizer_pin(model_name):
    """Returns (checksum_hex|None, revision|None). Never raises."""
    snap_dir = None
    try:
        from huggingface_hub import snapshot_download
        snap_dir = snapshot_download(
            repo_id=model_name,
            allow_patterns=["tokenizer.json", "tokenizer_config.json",
                            "special_tokens_map.json", "vocab.json",
                            "merges.txt", "added_tokens.json"])
    except Exception:
        snap_dir = None
    if snap_dir is None:
        # Fallback: scan the local HF cache for the model snapshots.
        try:
            cache_root = os.path.join(os.path.expanduser("~"), ".cache", "huggingface", "hub",
                                      "models--" + model_name.replace("/", "--"), "snapshots")
            cands = [os.path.join(cache_root, d) for d in sorted(os.listdir(cache_root))]
            cands = [d for d in cands
                     if os.path.isfile(os.path.join(d, "tokenizer.json"))]
            snap_dir = cands[-1] if cands else None
        except Exception:
            snap_dir = None
    if snap_dir is None:
        return None, None
    revision = os.path.basename(os.path.normpath(snap_dir))
    if not (len(revision) == 40 and all(c in "0123456789abcdef" for c in revision)):
        revision = None
    sha = hashlib.sha256()
    found = False
    for fname in TOKENIZER_PAYLOAD_FILES:
        fpath = os.path.join(snap_dir, fname)
        if os.path.isfile(fpath):
            found = True
            sha.update(fname.encode("utf-8") + b"\x00")
            with open(fpath, "rb") as f:
                for chunk in iter(lambda: f.read(1 << 20), b""):
                    sha.update(chunk)
    if not found:
        return None, revision
    return sha.hexdigest(), revision


# ----------------------------------------------------------------------------
# G8 entity masks (REV2 §3.2, G8): head/tail entity strings -> token positions.
#
# Conservative reading (documented, not improvised — see BUILD_NOTES.md):
# arm (b) injects at ALL token positions where the head entity string (the
# item record's `ent`, cross-checked = reconstructed target A) or the tail
# entity string (the reconstructed foil C) occurs in the prompt — premise
# and question occurrences alike. The lemma (REV2 §5 L1(iii)) licenses any
# P subset of {positions < p_last}; "mapped to token positions" describes
# string->position mapping; a premise-only narrowing would be an unlicensed
# weakening of the arm. Multi-token entities -> all their tokens. Positions
# are found via the pinned tokenizer's offset mapping against the exact
# ids used for the forward pass (asserted equal).
# ----------------------------------------------------------------------------

def build_entity_mask(tokenizer, prompt, head_str, tail_str):
    """Returns (mask_positions, mapping_record). Raises on unmappable."""
    enc = tokenizer(prompt, return_offsets_mapping=True)
    ids = enc["input_ids"]
    offsets = enc["offset_mapping"]
    if list(ids) != tokenizer.encode(prompt):
        raise RuntimeError(
            "FATAL (G8 construction): offset-mapping tokenization != encode() "
            "tokenization for a prompt — the mask would misalign with the "
            "forward pass. Halting, not silently proceeding.")
    positions = set()
    per_entity = {}
    for label, s in (("head", head_str), ("tail", tail_str)):
        needle = " " + s  # every template occurrence is space-preceded
        spans = []
        start = 0
        while True:
            j = prompt.find(needle, start)
            if j < 0:
                break
            spans.append((j + 1, j + 1 + len(s)))  # entity chars proper
            start = j + 1
        tok_idx = []
        for (cs, ce) in spans:
            hit = False
            for ti, (os_, oe) in enumerate(offsets):
                if os_ < ce and oe > cs:
                    positions.add(ti)
                    tok_idx.append(ti)
                    hit = True
            if not hit:
                raise ValueError(
                    f"G8 unmappable: entity '{s}' occurrence at chars [{cs},{ce}) "
                    f"maps to no token.")
        if not spans:
            raise ValueError(f"G8 unmappable: entity string '{s}' not found in prompt.")
        per_entity[label] = {"string": s, "char_spans": spans, "token_positions": sorted(tok_idx)}
    mask = sorted(positions)
    if not mask:
        raise ValueError("G8 unmappable: empty entity mask.")
    return mask, per_entity


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="K2 routing-vs-bypass (REV2, LOG-226)")
    parser.add_argument("--ceo-gpu-clearance", action="store_true",
                        help="REQUIRED for Phase 1 (GPU). Without it, only the CPU "
                             "pre-execution phase runs and the bundle exits before "
                             "any GPU pass. DO NOT EXECUTE on GPU before CEO GPU clearance.")
    parser.add_argument("--allow-cpu", action="store_true",
                        help="override the CUDA-required guard on CPU-only machines "
                             "(strongly discouraged: 180 forward passes on CPU).")
    parser.add_argument("--out-dir", default=os.path.join("experiments", "runs", "K2_routing_bypass"),
                        help="output directory for run artifacts")
    args = parser.parse_args()

    out_dir = args.out_dir
    os.makedirs(out_dir, exist_ok=True)
    log_path = os.path.join(out_dir, "k2_run_log.txt")
    log_file = open(log_path, "w", encoding="utf-8")

    BANNER = ("=" * 78 + "\n"
              "K2 ROUTING-VS-BYPASS — DO NOT EXECUTE on GPU before CEO GPU clearance.\n" +
              "=" * 78)
    log(BANNER, log_file)
    log("Pre-registered protocol (SIGNED, LOG-224c): "
        "research/analysis_plans/K2_ROUTING_BYPASS_PLAN_LOG223_REV2_2026-09-23.md", log_file)
    log(f"Model: {MODEL_NAME} | d={D} | target_layer={TARGET_LAYER} | alpha={ALPHA} | "
        f"K2-P = {PASSES_PER_PIN} passes (60 items x 3 arms)", log_file)

    import torch
    torch.manual_seed(SEED_TORCH)
    np.random.seed(SEED_NUMPY)
    try:
        torch.use_deterministic_algorithms(True)
        log("torch.use_deterministic_algorithms(True) enabled.", log_file)
    except Exception as e:
        log(f"WARNING: deterministic algorithms unavailable ({e}); continuing.", log_file)

    # -------------------------------------------------------------
    # Phase 0 — CPU pre-execution.
    # -------------------------------------------------------------
    log("\n[Phase 0] CPU pre-execution ...", log_file)
    from transformers import AutoModelForCausalLM, AutoTokenizer

    log("Loading tokenizer (CPU) ...", log_file)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    # Ruling 6 / checklist B: tokenizer pin at vector-build time.
    tok_checksum, hf_revision = resolve_tokenizer_pin(MODEL_NAME)
    checklist_b = checklist_b_record(tok_checksum, hf_revision)
    log(f"Checklist B (tokenizer pin): status={checklist_b['status']}; "
        f"sha256={tok_checksum}; revision={hf_revision}", log_file)
    if checklist_b["status"] != "complete":
        log("NOTE: " + checklist_b["note"], log_file)
    # Reference pin observed at build time (BUILD_NOTES.md): warn, do not gate.
    if hf_revision is not None and hf_revision != PINNED_HF_REVISION:
        log(f"[OBSERVATION] tokenizer revision {hf_revision} differs from the "
            f"build-time reference pin {PINNED_HF_REVISION}; logged, not gated.",
            log_file)

    log("Loading model on CPU (float32) for the identity dry run ...", log_file)
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, torch_dtype=torch.float32)
    model.eval()

    pre_hash = get_hash(model)
    log(f"Pre-experiment parameter SHA-256 (G3 pre): {pre_hash}", log_file)

    # Pinned archives (read-only).
    for ap in (ARCH_RECORDS, ARCH_RESULTS, ARCH_VECTORS):
        if not os.path.isfile(ap):
            log(f"FATAL: pinned archive missing: {ap}", log_file)
            log_file.close()
            raise SystemExit(f"pinned archive missing: {ap}")
    arch_hashes = {os.path.basename(p): sha256_file(p)
                   for p in (ARCH_RECORDS, ARCH_RESULTS, ARCH_VECTORS)}
    log(f"Pinned archive sha256: {json.dumps(arch_hashes)}", log_file)
    with open(ARCH_RECORDS, encoding="utf-8") as f:
        records = json.load(f)
    with open(ARCH_RESULTS, encoding="utf-8") as f:
        arch_results = json.load(f)
    logged_norms = [arch_results["injection_vector_norms"][f"C8_bridge_item{i}"]
                    for i in range(N_BENCH)]
    log(f"Run-logged C8 norms: {len(logged_norms)} per-item norms loaded "
        f"(all ~= {ALPHA}; the weak fingerprint per REV2 F1).", log_file)

    # Benchmark reconstruction + G2 cross-check.
    bench = build_benchmark()
    exclusions = []   # list of {"item": i, "cause": ...}; counted, never silent
    g1_item_failures = 0
    if len(records) != N_BENCH:
        log(f"FATAL: records count {len(records)} != {N_BENCH} — records missing.", log_file)
        log_file.close()
        raise SystemExit("records missing")
    for i, (rec, it) in enumerate(zip(records, bench)):
        if rec.get("ent") != it["ent"] or rec.get("typ") != it["typ"]:
            exclusions.append({"item": i, "cause": "G2 label cross-check: record ent/typ "
                               f"({rec.get('ent')}/{rec.get('typ')}) != reconstructed "
                               f"({it['ent']}/{it['typ']})"})
        if "C1" not in rec.get("correct", {}):
            log(f"FATAL: record {i} missing C1 baseline — records missing.", log_file)
            log_file.close()
            raise SystemExit("records missing")
    log(f"G2 cross-check: {N_BENCH - len(exclusions)}/{N_BENCH} items aligned "
        f"(record ent/typ == reconstructed).", log_file)

    # Gate A — CPU identity dry run (Ruling 7), BEFORE any GPU pass.
    log("\n[Gate A] CPU identity dry run (two independent rebuilds) ...", log_file)
    from k2_vectors import gate_a_run
    gate_a = gate_a_run(model, tokenizer, bench, logged_norms, tol=NORM_REL_TOL,
                        tokenizer_checksum=tok_checksum, hf_revision=hf_revision)
    log(f"Gate A verdict: {gate_a['verdict']} — {gate_a['message']}", log_file)
    log(f"  byte_identity_ok={gate_a['byte_identity_ok']} "
        f"(mismatched_items={gate_a['mismatched_items']})", log_file)
    log(f"  norm_match_ok={gate_a['norm_match_ok']} (tol={NORM_REL_TOL})", log_file)
    log(f"  epistemic grade: {gate_a['epistemic_grade']}", log_file)
    # G1(d): identity chain record — E1+E2 source link + run-log F1 record.
    log("G1(d) identity chain: E1+E2 source link — C8 = EXP066 `make_bridge_vec` "
        "verbatim (in this runner source, build_bridge_vectors_primary); "
        "EXP077 run-log F1 record: 'C8 bridge vectors: 60 per-item unembedding "
        "directions, min norm=0.5000 (all > 0).'", log_file)
    if gate_a["verdict"] != "PASS":
        preexec = {"phase": "pre-execution", "outcome": "GATE_A_FAIL",
                   "gate_a": gate_a, "checklist_b": checklist_b,
                   "gpu_clearance": "BLOCKED with cause — no GPU pass executed."}
        with open(os.path.join(out_dir, "k2_preexec_report.json"), "w", encoding="utf-8") as f:
            json.dump(preexec, f, indent=2)
        log("=" * 78, log_file)
        log("PRE-EXECUTION GATE A FAILED — GPU clearance BLOCKED with cause. "
            "No GPU pass executed. Report k2_preexec_report.json.", log_file)
        log("=" * 78, log_file)
        log_file.close()
        raise SystemExit("gate A failed")

    # G8 entity masks + G10 disjointness (pre-GPU).
    log("\n[G8/G10] entity-position masks (pinned tokenizer, pre-GPU) ...", log_file)
    masks, mask_records = {}, {}
    for i, it in enumerate(bench):
        if any(e["item"] == i for e in exclusions):
            continue
        try:
            mask, per_entity = build_entity_mask(tokenizer, it["prompt"], it["A"], it["C"])
        except (ValueError, RuntimeError) as e:
            exclusions.append({"item": i, "cause": f"G8 entity-mapping: {e}"})
            continue
        seq_len = len(tokenizer.encode(it["prompt"]))
        if (seq_len - 1) in mask:
            exclusions.append({"item": i, "cause": "G10 disjointness: entity token span "
                               "includes the final sequence position; arms (a)/(b) would "
                               "coincide on this item"})
            continue
        masks[i] = mask
        mask_records[i] = {"mask": mask, "per_entity": per_entity, "seq_len": seq_len,
                           "final_position": seq_len - 1}
        log(f"  item {i}: mask={mask} "
            f"(head='{it['A']}' {per_entity['head']['token_positions']}, "
            f"tail='{it['C']}' {per_entity['tail']['token_positions']})", log_file)

    floor_status, floor_msg = g10_exclusion_floor_check(exclusions)
    log(f"G10 exclusion floor: {floor_status} — {floor_msg}", log_file)
    for e in exclusions:
        log(f"  excluded item {e['item']}: {e['cause']}", log_file)
    n_actual = N_BENCH - len(exclusions)

    # Archived baseline (C1) — no re-baselining passes.
    included = [i for i in range(N_BENCH) if not any(e["item"] == i for e in exclusions)]
    base_correct = [bool(records[i]["correct"]["C1"]) for i in included]
    log(f"Baseline (archived smoke C1): {sum(base_correct)}/{n_actual} = "
        f"{sum(base_correct)/n_actual:.4f} on included items.", log_file)

    # G7 Law #7 provenance note (logged; also in the results payload).
    log("G7 (Law #7 provenance): the bridge is the archived label-informed vector "
        "normalize(E[target]-E[foil]) used AS A MECHANISTIC PROBE. K2 probes where "
        "the rescue travels; it draws no autonomous-mechanism claim from the "
        "label-informed construction — that question is K3's, untouched here.", log_file)
    log("G6: EXP070 excluded — no EXP070 records, artifacts, or vectors used anywhere "
        "in this bundle.", log_file)

    preexec_report = {
        "phase": "pre-execution",
        "outcome": "PREEXEC_PASS" if floor_status == "proceed" else "UNDERDETERMINED_G10",
        "model": MODEL_NAME,
        "target_layer": TARGET_LAYER,
        "alpha": ALPHA,
        "seeds": {"torch": SEED_TORCH, "numpy": SEED_NUMPY},
        "arch_hashes": arch_hashes,
        "pre_hash_G3": pre_hash,
        "gate_a": {k: v for k, v in gate_a.items()
                   if k not in ("per_item_digests_primary",)},
        "checklist_b": checklist_b,
        "n_exclusions": len(exclusions),
        "exclusions": exclusions,
        "g10_floor": {"status": floor_status, "message": floor_msg},
        "n_actual": n_actual,
        "baseline_archived_acc": sum(base_correct) / n_actual if n_actual else None,
        "anchor": ANCHOR,
        "g7_provenance": ("label-informed probe; no autonomous-mechanism claim; "
                          "that question is K3's"),
        "g6_exp070_excluded": True,
    }
    with open(os.path.join(out_dir, "k2_preexec_report.json"), "w", encoding="utf-8") as f:
        json.dump(preexec_report, f, indent=2)
    log(f"Pre-execution report written: k2_preexec_report.json", log_file)

    if floor_status == "Underdetermined":
        log("=" * 78, log_file)
        log("G10 EXCLUSION FLOOR BREACHED — run is Underdetermined with cause. "
            "No GPU pass executed.", log_file)
        log("=" * 78, log_file)
        log_file.close()
        raise SystemExit("G10 floor breached")

    # -------------------------------------------------------------
    # Clearance gate: Phase 1 runs ONLY with --ceo-gpu-clearance.
    # -------------------------------------------------------------
    if not args.ceo_gpu_clearance:
        log("\n" + "=" * 78, log_file)
        log("PRE-EXECUTION COMPLETE. GPU phase NOT started.", log_file)
        log("DO NOT EXECUTE on GPU before CEO GPU clearance.", log_file)
        log("Re-run with --ceo-gpu-clearance once clearance is granted.", log_file)
        log("=" * 78, log_file)
        log_file.close()
        print("=" * 78)
        print("DO NOT EXECUTE on GPU before CEO GPU clearance.")
        print("Pre-execution complete; no GPU pass executed. Awaiting CEO GPU clearance.")
        print("=" * 78)
        return

    # -------------------------------------------------------------
    # Phase 1 — GPU.
    # -------------------------------------------------------------
    log("\n[Phase 1] GPU execution (--ceo-gpu-clearance supplied) ...", log_file)
    if not torch.cuda.is_available():
        if not args.allow_cpu:
            msg = ("FATAL: no CUDA GPU detected. K2 requires a GPU (180 forward "
                   "passes). Enable a GPU runtime -- Kaggle: right panel -> "
                   "Accelerator: GPU T4 x2 (new accounts need phone verification "
                   "first); Colab: Runtime -> Change runtime type -> T4 GPU -- "
                   "then re-run. Override ONLY with --allow-cpu (strongly discouraged).")
            log(msg, log_file)
            log_file.close()
            raise SystemExit(msg)
        log("WARNING: --allow-cpu override accepted on a CPU-only machine.", log_file)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    log(f"Device: {device}", log_file)
    model.to(device)
    layer_module = model.gpt_neox.layers[TARGET_LAYER]

    env_manifest = {
        "torch": torch.__version__,
        "cuda_available": torch.cuda.is_available(),
        "cuda_device": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        "device": str(device),
        "model": MODEL_NAME,
        "protocol_scope": "K2-P (pythia-410m, layer 20, alpha=0.5)",
    }
    try:
        import transformers
        env_manifest["transformers"] = transformers.__version__
    except Exception:
        pass
    log(f"Environment manifest: {json.dumps(env_manifest)}", log_file)

    # Bridge vectors: the gate-A-verified primary rebuild, moved per pass.
    from k2_vectors import build_bridge_vectors_primary
    vecs, _E, token_map = build_bridge_vectors_primary(
        model, tokenizer, [bench[i] for i in included])
    # G1(a) re-assert at GPU time: norms still match (cheap, zero passes).
    for i_incl, v in enumerate(vecs):
        _n = float(torch.norm(v).item())
        assert abs(_n - logged_norms[included[i_incl]]) / logged_norms[included[i_incl]] <= NORM_REL_TOL

    n_passes = [0]  # G4 licensed-pass counter (closure over eval)

    def eval_item(prompt, tA_id, tC_id, vec, mask_positions, want_hidden=False):
        """One forward pass with per-position masked additive injection.

        vec: alpha-scaled bridge direction (CPU tensor); added at the target
        layer's output at `mask_positions` (list of int). Decision read at
        the final token exactly as the archived runs (argmax over {tA, tC}).
        """
        inp = tokenizer.encode(prompt, return_tensors="pt").to(device)
        v = vec.to(device)
        m = torch.tensor(mask_positions, dtype=torch.long, device=device)

        def hook_fn(module, inputs, output):
            x = output[0] if isinstance(output, tuple) else output
            x = x.clone()
            x[0, m, :] = x[0, m, :] + v
            return (x,) + tuple(output[1:]) if isinstance(output, tuple) else x

        hook = layer_module.register_forward_hook(hook_fn)
        try:
            with torch.no_grad():
                out = model(input_ids=inp, output_hidden_states=want_hidden)
        finally:
            hook.remove()
        n_passes[0] += 1
        logits = out.logits[0, -1, :].detach().cpu()
        chosen_is_A = bool(logits[tA_id] > logits[tC_id])
        top5_vals, top5_ids = torch.topk(logits, 5)
        hidden_norms = None
        if want_hidden:
            h = out.hidden_states[-1][0, :, :].detach().cpu()
            hidden_norms = [float(torch.norm(h[p, :]).item()) for p in range(h.shape[0])]
        return chosen_is_A, top5_ids.tolist(), top5_vals.tolist(), hidden_norms

    arm_names = {"a": "FINAL-ONLY (a)", "b": "ENTITY-ONLY (b)", "c": "ALL-POSITIONS (c)"}
    arm_correct, top5_archive, g9_norms = {}, {}, {}
    used_masks = {}
    for arm in ("a", "b", "c"):
        log(f"\n[Arm {arm_names[arm]}] ...", log_file)
        correct, tops, hnorms, umasks = [], [], [], []
        for j, i in enumerate(included):
            it = bench[i]
            tA_id = token_map[j]["t_id"]
            tC_id = token_map[j]["f_id"]
            seq_len = mask_records[i]["seq_len"]
            if arm == "a":
                mask = [seq_len - 1]                      # final token only
            elif arm == "b":
                mask = masks[i]                           # premise-entity positions
            else:
                mask = list(range(seq_len))               # all positions (broadcast)
            umasks.append(mask)
            want_hidden = arm in ("a", "b")               # G9 diagnostic, zero extra passes
            ok, t5_ids, t5_vals, hn = eval_item(it["prompt"], tA_id, tC_id,
                                               vecs[j], mask, want_hidden=want_hidden)
            correct.append(ok)
            tops.append({"item": i, "top5_ids": t5_ids, "top5_logits": t5_vals})
            if hn is not None:
                hnorms.append({"item": i, "final_layer_residual_norms": hn})
            if (j + 1) % 15 == 0:
                log(f"  arm {arm}: {j + 1}/{n_actual} items", log_file)
        arm_correct[arm] = correct
        top5_archive[arm] = tops
        used_masks[arm] = umasks
        if hnorms:
            g9_norms[arm] = hnorms
        log(f"Arm {arm}: accuracy {sum(correct)}/{n_actual} = "
            f"{sum(correct)/n_actual:.4f}", log_file)

    # G4: no-forward-pass-except-licensed.
    g4_ok, g4_expected = g4_pass_count_check(n_passes[0], n_actual)
    log(f"G4 pass count: {n_passes[0]} (licensed: {g4_expected}) -> "
        f"{'OK' if g4_ok else 'VIOLATED'}", log_file)

    # Per-arm paired stats vs archived baseline.
    stats_a = paired_contrast_stats(base_correct, arm_correct["a"], label="a_vs_base")
    stats_b = paired_contrast_stats(base_correct, arm_correct["b"], label="b_vs_base")
    stats_c = paired_contrast_stats(base_correct, arm_correct["c"], label="c_vs_base")
    for s_ in (stats_a, stats_b, stats_c):
        log(f"{s_['label']}: dM={s_['d_hat']*100:+.2f}pp (b={s_['b']}, c={s_['c']}), "
            f"McNemar p={s_['mcnemar_p']:.6f}, Tango 95% CI=({s_['tango_L']:.4f}, {s_['tango_U']:.4f})",
            log_file)

    # G5: (c)-reproduction gate — FATAL if it fails.
    g5_ok = g5_c_gate_check(stats_c["b"])
    log(f"G5 (c)-gate: b_c={stats_c['b']} (floor {C_GATE_MDE_B}) -> "
        f"{'PASS' if g5_ok else 'FAIL — INVALID'}", log_file)

    # G9 diagnostic (diagnostic, never a gate).
    # Purpose per REV2: "if a (b)-vs-(a) difference rides on broad position
    # effects, the G9 ratio diagnoses it." Adopted operationalization (flagged
    # in BUILD_NOTES.md): within each injected pass, the localization ratio
    #   G9 = mean(per-position final-layer residual norm at injected positions)
    #        / mean(per-position final-layer residual norm at non-injected positions).
    # G9 >> 1 -> the injection's footprint is localized at the injection
    # sites; G9 ~= 1 -> the footprint is broad (rides on position-general
    # effects). Recorded as [OBSERVATION]; the verdict never depends on it.
    g9_record = {"note": "diagnostic only — recorded as [OBSERVATION], never a post-hoc gate",
                 "definition": "localization_ratio = mean(norm[injected]) / mean(norm[non-injected])"}
    if "a" in g9_norms and "b" in g9_norms:
        per_item = []
        for arm in ("a", "b"):
            for k, rec in enumerate(g9_norms[arm]):
                i = rec["item"]
                norms = rec["final_layer_residual_norms"]
                inj = set(used_masks[arm][k])
                non = [p for p in range(len(norms)) if p not in inj]
                mean_inj = float(np.mean([norms[p] for p in sorted(inj)]))
                mean_non = float(np.mean([norms[p] for p in non])) if non else float("nan")
                ratio = (mean_inj / mean_non) if (non and mean_non > 0) else float("nan")
                per_item.append({"item": i, "arm": arm,
                                 "localization_ratio": ratio,
                                 "mean_norm_injected": mean_inj,
                                 "mean_norm_non_injected": mean_non})
        g9_record["per_item"] = per_item
        for arm in ("a", "b"):
            rs = [r["localization_ratio"] for r in per_item
                  if r["arm"] == arm and not math.isnan(r["localization_ratio"])]
            g9_record[f"median_localization_ratio_arm_{arm}"] = (
                float(np.median(rs)) if rs else float("nan"))
        # Broad-effect rescues: items rescued by (b) whose footprint is not
        # localized at the entity positions (ratio < 1.25).
        broad = [r["item"] for r in per_item if r["arm"] == "b"
                 and not math.isnan(r["localization_ratio"])
                 and r["localization_ratio"] < 1.25]
        rescued_b = [included[k] for k in range(n_actual)
                     if arm_correct["b"][k] and not base_correct[k]]
        broad_rescues = sorted(set(broad) & set(rescued_b))
        g9_record["broad_effect_rescues_b"] = broad_rescues
        g9_record["reading"] = (
            "[OBSERVATION]: median G9 localization ratio arm-(a)=%.3f, arm-(b)=%.3f; "
            "%d of %d (b)-rescues show a broad (non-localized) footprint "
            "(ratio<1.25). Recorded as a covariate; the verdict is read with "
            "this caveat, never gated on it."
            % (g9_record["median_localization_ratio_arm_a"],
               g9_record["median_localization_ratio_arm_b"],
               len(broad_rescues), len(rescued_b)))
        log(g9_record["reading"], log_file)

    # G3 post.
    post_hash = get_hash(model)
    g3_ok, g3_msg = g3_delta_theta_check(pre_hash, post_hash)
    log(f"Post-experiment parameter SHA-256 (G3 post): {post_hash}", log_file)
    log(f"G3: {g3_msg}", log_file)

    # Row-5 pre-adjudication (FATAL guards).
    guard_record = {
        "g1_invalid": g1_invalid_check(g1_item_failures),
        "g3_pre_post_match": g3_ok,
        "g4_pass_count_ok": g4_ok,
        "g4_expected": g4_expected,
        "g4_got": n_passes[0],
        "g5_c_gate_passed": g5_ok,
        "b_c": stats_c["b"],
        "records_missing": False,
        "exclusions": exclusions,
    }
    underdet, cause = guards_evaluate(guard_record)
    if underdet:
        log("=" * 78, log_file)
        log(f"ROW 5 — {cause}", log_file)
        log("=" * 78, log_file)
        verdict = {"row": 5, "verdict_routing": UNDERDETERMINED,
                   "verdict_final_position_local": UNDERDETERMINED,
                   "consequence": cause + " Fix cause; re-run under a new LOG. "
                                  "Nothing is filled by assumption.",
                   "n_actual": n_actual, "n_excluded": len(exclusions),
                   "exclusions": exclusions}
    else:
        v = adjudicate_verdict(base_correct, arm_correct["a"], arm_correct["b"],
                               arm_correct["c"], exclusions, c_gate_passed=g5_ok)
        verdict = v
        log("=" * 78, log_file)
        log(f"Verdict (runner display; evaluate_k2.py is authoritative): "
            f"row {v['row']}", log_file)
        log(f"  routing: {v['verdict_routing']}; final-position-local: "
            f"{v['verdict_final_position_local']}", log_file)
        log(f"  contrast (b)-(a): d={v['contrast_b_vs_a']['d_hat']:+.4f}, "
            f"Tango 95% CI=({v['contrast_b_vs_a']['tango_L']:.4f}, "
            f"{v['contrast_b_vs_a']['tango_U']:.4f})", log_file)
        log("=" * 78, log_file)

    # Instance records (Law #13).
    instance_records = []
    for j, i in enumerate(included):
        it = bench[i]
        instance_records.append({
            "item": i, "ent": it["ent"], "typ": it["typ"], "A": it["A"], "C": it["C"],
            "baseline_C1": bool(base_correct[j]),
            "correct": {"a": bool(arm_correct["a"][j]),
                        "b": bool(arm_correct["b"][j]),
                        "c": bool(arm_correct["c"][j])},
            "entity_mask_b": masks[i],
            "excluded": False,
        })
    for e in exclusions:
        instance_records.append({"item": e["item"], "excluded": True, "cause": e["cause"]})
    instance_records.sort(key=lambda r: r["item"])

    results_payload = {
        "experiment": "K2_routing_bypass",
        "log": "LOG-226",
        "protocol": "research/analysis_plans/K2_ROUTING_BYPASS_PLAN_LOG223_REV2_2026-09-23.md (SIGNED LOG-224c)",
        "outcome": "COMPLETED" if not underdet else "UNDERDETERMINED",
        "model": MODEL_NAME,
        "target_layer": TARGET_LAYER,
        "alpha": ALPHA,
        "hidden_dim": D,
        "seeds": {"torch": SEED_TORCH, "numpy": SEED_NUMPY},
        "pre_hash": pre_hash,
        "post_hash": post_hash,
        "g3_pre_post_match": g3_ok,
        "arch_hashes": arch_hashes,
        "anchor": ANCHOR,
        "n_actual": n_actual,
        "n_excluded": len(exclusions),
        "exclusions": exclusions,
        "n_passes": n_passes[0],
        "g4": {"ok": g4_ok, "expected": g4_expected, "got": n_passes[0]},
        "g5_c_gate": {"b_c": stats_c["b"], "floor": C_GATE_MDE_B, "passed": g5_ok},
        "gate_a": {k: v for k, v in gate_a.items() if k != "per_item_digests_primary"},
        "checklist_b": checklist_b,
        "baseline_archived_acc": sum(base_correct) / n_actual,
        "arm_stats": {"a": stats_a, "b": stats_b, "c": stats_c},
        "verdict": verdict,
        "verdict_note": "Runner display only; evaluate_k2.py is authoritative for the ruling.",
        "top5_archive": top5_archive,
        "g9_diagnostic": g9_record,
        "g7_provenance": ("label-informed probe; no autonomous-mechanism claim; "
                          "that question is K3's"),
        "g6_exp070_excluded": True,
        "env_manifest": env_manifest,
        "epistemic_grades": {
            "bridge_vector_identity": "[INFERENCE] (deterministic reconstruction) — never [FACT]",
            "verdict": "[INTERPRETATION] of [OBSERVATION] per the pre-registered table",
        },
    }
    with open(os.path.join(out_dir, "k2_results.json"), "w", encoding="utf-8") as f:
        json.dump(results_payload, f, indent=2)
    with open(os.path.join(out_dir, "k2_instance_records.json"), "w", encoding="utf-8") as f:
        json.dump(instance_records, f, indent=2)

    runtime_manifest = {
        "bundle": "K2_routing_bypass (LOG-226)",
        "model_pin": MODEL_NAME,
        "tokenizer_pin": {"sha256": tok_checksum, "hf_revision": hf_revision,
                          "checklist_b": checklist_b},
        "seeds": {"torch": SEED_TORCH, "numpy": SEED_NUMPY},
        "environment": env_manifest,
        "archive_hashes": arch_hashes,
        "pre_hash": pre_hash,
        "post_hash": post_hash,
        "clearance": "CEO GPU clearance supplied via --ceo-gpu-clearance",
    }
    with open(os.path.join(out_dir, "k2_runtime_manifest.json"), "w", encoding="utf-8") as f:
        json.dump(runtime_manifest, f, indent=2)

    log(f"\nArtifacts written to {out_dir}/: k2_results.json, k2_instance_records.json, "
        f"k2_preexec_report.json, k2_runtime_manifest.json", log_file)
    log("Next: run evaluate_k2.py on k2_results.json for the authoritative ruling.", log_file)
    log("=" * 78, log_file)
    log("K2 COMPLETED. Cell-2 verdicts (if any) are provisional-pending the "
        "official-bench replication (REV2 §7).", log_file)
    log("=" * 78, log_file)
    log_file.close()


if __name__ == "__main__":
    main()
