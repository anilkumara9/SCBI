#!/usr/bin/env python3
"""EXP088 Stage-B probe set (F11 pin).

The signed protocol pins the probe set as the EXP077 60-record archive
verbatim (experiments/runs/EXP077_cone_vs_line/exp077_instance_records.json,
sha256 47281cd3...0585, 60 records, established LOG-306/LOG-307), "with
fixed indices; any deviation loudly logged per the EXP084-D1 convention;
or the program's standard probe — decided at build, registered before
running".

The archive carries NO prompt strings (records hold item/ent/typ/correct/
rescue_indicators only) — the same D1-class gap EXP084's stage-2 review
adjudicated — AND its item set differs from the EXP077 section-3 builder's
(archive: uniform 6/entity, grouped; §3 port: skewed Mars×21/Iron×21…).
The multisets differ, so this is not a reordering and the archive's exact
prompts are unrecoverable (LOG-320 F4). The bundle's probe is therefore the
protocol's licensed fallback ("the program's standard probe — decided at
build, registered before running"): 60 fixed synthetic 2/3-hop MCQ items
(verbatim port of the EXP077 section 3 builder from
experiments/runs/exp077/run_exp077.py via EXP084's build_benchmark, WITH
the A/C fields EXP077's decision rule needs), fixed indices 0..59,
deterministic, outcome-independent (EXP077 was a null; accuracy was never
its endpoint). The deviation is loudly logged by load_probe_set and
manifest-recorded in every run record — never silent.

Decision rule (verbatim EXP077 section 4): at the answer position,
toks_A = tokenizer.encode(" " + A)[0], toks_C = tokenizer.encode(" " + C)[0];
chosen = A iff logit[toks_A] > logit[toks_C] else C; correct iff chosen == A
(A = the higher-ranked entity = the correct answer).

Pure standard library (the rebuild needs no tokenizer).
"""

import hashlib
import json
import os

# --- F11 pin -----------------------------------------------------------------
RECORDS_REL = os.path.join("..", "EXP077_cone_vs_line",
                           "exp077_instance_records.json")
RECORDS_SHA256 = ("47281cd3dc243369be0aa5be2345663b752cdb4a329a16a37f08da5717230585")
N_ITEMS = 60


class ProbeSetError(RuntimeError):
    """Probe-set preflight failure (missing/unverifiable records file)."""


# --- Verbatim EXP077 section 3 benchmark builder ------------------------------
# Ported from experiments/runs/exp077/run_exp077.py (N_BENCH=60 block),
# itself ported verbatim from experiments/runs/exp078/run_exp078.py section 2
# (Law #9: no new benchmark construction). Constants and all four loops
# reproduced exactly. Item dicts keep EXP077's schema ("prompt"/"A"/"C" with
# A=target, C=foil) plus provenance fields ("ent"/"typ" for the archive
# alignment audit).
_BENCH_PLANETS = ["Mars", "Venus", "Jupiter", "Saturn", "Mercury"]
_BENCH_ELEMENTS = ["Iron", "Gold", "Silver", "Bronze", "Steel"]
_BENCH_TRIPLES = [
    (0, 1, 2), (1, 2, 3), (2, 3, 4), (0, 2, 4), (0, 1, 3),
    (1, 3, 4), (0, 2, 3), (1, 2, 4), (0, 3, 4), (0, 1, 4),
    (0, 1, 2), (1, 2, 3), (2, 3, 4), (0, 2, 4), (0, 1, 3),
]
_BENCH_QUADS = [
    (0, 1, 2, 3), (1, 2, 3, 4), (0, 1, 3, 4), (0, 2, 3, 4), (0, 1, 2, 4),
    (0, 1, 2, 3), (1, 2, 3, 4), (0, 1, 3, 4), (0, 2, 3, 4), (0, 1, 2, 4),
    (0, 1, 2, 3), (1, 2, 3, 4), (0, 1, 3, 4), (0, 2, 3, 4), (0, 1, 2, 4),
]


def build_benchmark():
    """Rebuild the 60 EXP077 bench prompts verbatim (EXP084-D1 convention).

    Returns 60 dicts {id, prompt, A, C, ent, typ, hop, domain}.
    A = correct answer (higher-ranked entity); C = foil.
    """
    bench = []
    for i, (iA, iB, iC) in enumerate(_BENCH_TRIPLES):
        A, B, C = (_BENCH_PLANETS[iA], _BENCH_PLANETS[iB], _BENCH_PLANETS[iC])
        target_first = (i % 2 == 1)
        q_opts = f"{A} or {C}" if target_first else f"{C} or {A}"
        if i < 8:
            p = (f"Premise: {A} outranks {B}. {B} outranks {C}. "
                 f"Question: Who is higher in rank, {q_opts}? Answer:")
        else:
            p = (f"Premise: {C} is lower than {B}. {B} is lower than {A}. "
                 f"Question: Who is higher in rank, {q_opts}? Answer:")
        bench.append({"id": f"exp077_planet_2hop_{i}", "prompt": p,
                      "A": A, "C": C, "ent": A, "typ": "planet",
                      "hop": 2, "domain": "Planetary"})
    for i, (iA, iB, iC, iD) in enumerate(_BENCH_QUADS):
        A, B, C, D_ent = (_BENCH_PLANETS[iA], _BENCH_PLANETS[iB],
                          _BENCH_PLANETS[iC], _BENCH_PLANETS[iD])
        target_first = (i % 2 == 1)
        q_opts = f"{A} or {D_ent}" if target_first else f"{D_ent} or {A}"
        if i < 8:
            p = (f"Premise: {A} outranks {B}. {B} outranks {C}. "
                 f"{C} outranks {D_ent}. "
                 f"Question: Who is higher in rank, {q_opts}? Answer:")
        else:
            p = (f"Premise: {D_ent} is lower than {C}. {C} is lower than {B}. "
                 f"{B} is lower than {A}. "
                 f"Question: Who is higher in rank, {q_opts}? Answer:")
        bench.append({"id": f"exp077_planet_3hop_{i}", "prompt": p,
                      "A": A, "C": D_ent, "ent": A, "typ": "planet",
                      "hop": 3, "domain": "Planetary"})
    for i, (iA, iB, iC) in enumerate(_BENCH_TRIPLES):
        A, B, C = (_BENCH_ELEMENTS[iA], _BENCH_ELEMENTS[iB],
                   _BENCH_ELEMENTS[iC])
        target_first = (i % 2 == 0)
        q_opts = f"{A} or {C}" if target_first else f"{C} or {A}"
        if i < 7:
            p = (f"Premise: {A} outranks {B}. {B} outranks {C}. "
                 f"Question: Who is higher in rank, {q_opts}? Answer:")
        else:
            p = (f"Premise: {C} is lower than {B}. {B} is lower than {A}. "
                 f"Question: Who is higher in rank, {q_opts}? Answer:")
        bench.append({"id": f"exp077_element_2hop_{i}", "prompt": p,
                      "A": A, "C": C, "ent": A, "typ": "element",
                      "hop": 2, "domain": "Elemental"})
    for i, (iA, iB, iC, iD) in enumerate(_BENCH_QUADS):
        A, B, C, D_ent = (_BENCH_ELEMENTS[iA], _BENCH_ELEMENTS[iB],
                          _BENCH_ELEMENTS[iC], _BENCH_ELEMENTS[iD])
        target_first = (i % 2 == 0)
        q_opts = f"{A} or {D_ent}" if target_first else f"{D_ent} or {A}"
        if i < 7:
            p = (f"Premise: {A} outranks {B}. {B} outranks {C}. "
                 f"{C} outranks {D_ent}. "
                 f"Question: Who is higher in rank, {q_opts}? Answer:")
        else:
            p = (f"Premise: {D_ent} is lower than {C}. {C} is lower than {B}. "
                 f"{B} is lower than {A}. "
                 f"Question: Who is higher in rank, {q_opts}? Answer:")
        bench.append({"id": f"exp077_element_3hop_{i}", "prompt": p,
                      "A": A, "C": D_ent, "ent": A, "typ": "element",
                      "hop": 3, "domain": "Elemental"})
    assert len(bench) == N_ITEMS, f"expected 60 bench items, got {len(bench)}"
    return bench


def decide_from_logits(logit_A, logit_C, A, C):
    """EXP077 section 4 decision rule: A iff logit_A > logit_C else C.

    Returns (chosen, correct). Tie -> C (foil), verbatim EXP077 convention.
    """
    chosen = A if logit_A > logit_C else C
    return chosen, (chosen == A)


def load_probe_set(records_path, log):
    """Probe-set preflight (F11 pin + EXP084-D1 deviation convention).

    Verifies the pinned EXP077 instance-records file (sha256 vs the F11
    pin — binding integrity check), builds the 60-item standard probe, and
    returns the fixed probe set (indices 0..59).

    The archive carries no prompt strings AND its item set differs from
    the EXP077 section-3 builder's (uniform 6/entity vs skewed), so the
    probe is the protocol's licensed fallback — the program's standard
    probe, decided at build, registered before running: 60 fixed synthetic
    2/3-hop MCQ items (verbatim §3 port, fixed indices 0..59),
    deterministic and outcome-independent (EXP077 was a null). The
    deviation is loudly logged here and manifest-recorded by the runner.
    """
    if not os.path.exists(records_path):
        raise ProbeSetError(
            f"probe-set records file missing: {records_path} "
            "(F11 pin cannot be verified; fail loud)")
    with open(records_path, "rb") as f:
        sha = hashlib.sha256(f.read()).hexdigest()
    if sha != RECORDS_SHA256:
        raise ProbeSetError(
            f"probe-set records sha256 {sha} != F11 pin {RECORDS_SHA256}")
    records = json.load(open(records_path))
    if len(records) != N_ITEMS:
        raise ProbeSetError(
            f"records file holds {len(records)} records, F11 pins 60")
    bench = build_benchmark()

    def _align(lo, hi):
        return sum(1 for i in range(lo, hi)
                   if records[i].get("ent") == bench[i]["ent"]
                   and records[i].get("typ") == bench[i]["typ"])
    a60 = _align(0, N_ITEMS)
    log(f"probe-set records sha256 verified vs F11 pin ({sha[:16]}...)")
    log(f"PROBE-SET DEVIATION (LOG-320 F4): rebuilt (ent,typ) matches "
        f"archived records at {a60}/60 indices; the archive's item SET "
        "differs from the §3 builder's (uniform 6/entity vs skewed "
        "Mars×21/Iron×21…) and carries no prompt strings, so the probe "
        "is the protocol's licensed fallback — the program's standard "
        "probe, decided at build, registered before running (60 fixed "
        "synthetic 2/3-hop MCQ items, outcome-independent).")
    return {"items": bench, "alignment_60": a60, "records_sha": sha}
