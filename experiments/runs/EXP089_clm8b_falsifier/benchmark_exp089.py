"""EXP089 benchmark builder — VERBATIM port of the EXP077 N=60 benchmark.

Provenance: ported verbatim from
    experiments/runs/exp077/run_exp077.py  (benchmark block, §3 of main())
which was itself ported verbatim from experiments/runs/exp078/run_exp078.py §2
(MAJOR-3 repair; Law #9: no new benchmark construction).

The ONLY additions vs the source block:
  - a "phrasing" field per item ("A-first" for the `{A} outranks {B}...` form,
    i<8 planet / i<7 element; "C-first" for the `{C} is lower than {B}...`
    form) — required by signed-protocol §6 G3 and §7.1. This follows EXP077's
    own practice ("Item dicts keep this runner's schema ... plus provenance
    fields").
  - `state_text_of(prompt)`: the protocol-§6 state text = substring of `prompt`
    from "Premise:" up to (excluding) " Question:". The question and option
    list are EXCLUDED by construction.

The anti-cheat support-prompt assert from EXP077 is intentionally NOT ported:
EXP089 uses no support prompts (documented in BUILD_NOTES.md).
"""

import json
import os

# ---------------------------------------------------------------------------
# Constants — VERBATIM from experiments/runs/exp077/run_exp077.py (lines ~126-160)
# ---------------------------------------------------------------------------
N_BENCH = 60

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

# Signed-protocol §4 recorded artifact hashes (EXP077_cone_vs_line/, read-only).
ARTIFACT_HASHES = {
    "exp077_instance_records.json":
        "47281cd3dc243369be0aa5be2345663b752cdb4a329a16a37f08da5717230585",
    "exp077_results.json":
        "c0d5c28d075fe74488fd1e33b93b730907577e41e1b53959d61be7d2d8bb90f7",
    "exp077_vectors.pt":
        "8793e4d0baea844f9ae6afbec7970770d161b3f827bc234d3597286b66810cb9",
    "exp077_run_log.txt":
        "49a20b96f45b54189a8f6c9ed1463418f9b2d29e572ab1e2bd19ab7daa1b1ad3",
}

SIGNED_PROTOCOL_DIGEST = (
    "87f2c47b7cbcec3db98cd88d7240b95ce7f49af9039aa0ae4ec251a2714c24cb"
)


def _repo_root():
    # Bundle lives at experiments/runs/EXP089_clm8b_falsifier/; repo root is 3 up.
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))


def artifacts_dir():
    return os.path.join(_repo_root(), "experiments", "runs", "EXP077_cone_vs_line")


def signed_protocol_path():
    return os.path.join(
        _repo_root(), "experiments", "protocols",
        "EXP089_CLM8B_ADAPTATION_PREREG_SIGNED.md")


# ---------------------------------------------------------------------------
# Benchmark — VERBATIM port of the EXP077 benchmark block.
# ---------------------------------------------------------------------------
def build_benchmark():
    """Build the N=60 Planetary/Elemental 2-hop/3-hop benchmark.

    Identical items, premise permutations, vocab lists, index arrays, and
    seeds as EXP077 (which is EXP065/066-identical). Adds only the "phrasing"
    provenance field required by signed-protocol §6 G3 / §7.1.
    """
    bench = []
    for i, (iA, iB, iC) in enumerate(TRIPLES_INDICES):
        A, B, C = NOVEL_VOCAB_PLANET[iA], NOVEL_VOCAB_PLANET[iB], NOVEL_VOCAB_PLANET[iC]
        target_first = (i % 2 == 1)
        q_opts = f"{A} or {C}" if target_first else f"{C} or {A}"
        if i < 8:
            p = f"Premise: {A} outranks {B}. {B} outranks {C}. Question: Who is higher in rank, {q_opts}? Answer:"
            phrasing = "A-first"
        else:
            p = f"Premise: {C} is lower than {B}. {B} is lower than {A}. Question: Who is higher in rank, {q_opts}? Answer:"
            phrasing = "C-first"
        bench.append({"id": f"exp077_planet_2hop_{i}", "prompt": p, "A": A, "C": C,
                      "ent": A, "typ": "planet", "hop": 2, "domain": "Planetary",
                      "phrasing": phrasing})
    for i, (iA, iB, iC, iD) in enumerate(QUADS_INDICES):
        A, B, C, D_ent = (NOVEL_VOCAB_PLANET[iA], NOVEL_VOCAB_PLANET[iB],
                          NOVEL_VOCAB_PLANET[iC], NOVEL_VOCAB_PLANET[iD])
        target_first = (i % 2 == 1)
        q_opts = f"{A} or {D_ent}" if target_first else f"{D_ent} or {A}"
        if i < 8:
            p = (f"Premise: {A} outranks {B}. {B} outranks {C}. {C} outranks {D_ent}. "
                 f"Question: Who is higher in rank, {q_opts}? Answer:")
            phrasing = "A-first"
        else:
            p = (f"Premise: {D_ent} is lower than {C}. {C} is lower than {B}. "
                 f"{B} is lower than {A}. Question: Who is higher in rank, {q_opts}? Answer:")
            phrasing = "C-first"
        bench.append({"id": f"exp077_planet_3hop_{i}", "prompt": p, "A": A, "C": D_ent,
                      "ent": A, "typ": "planet", "hop": 3, "domain": "Planetary",
                      "phrasing": phrasing})
    for i, (iA, iB, iC) in enumerate(TRIPLES_INDICES):
        A, B, C = NOVEL_VOCAB_ELEMENT[iA], NOVEL_VOCAB_ELEMENT[iB], NOVEL_VOCAB_ELEMENT[iC]
        target_first = (i % 2 == 0)
        q_opts = f"{A} or {C}" if target_first else f"{C} or {A}"
        if i < 7:
            p = f"Premise: {A} outranks {B}. {B} outranks {C}. Question: Who is higher in rank, {q_opts}? Answer:"
            phrasing = "A-first"
        else:
            p = f"Premise: {C} is lower than {B}. {B} is lower than {A}. Question: Who is higher in rank, {q_opts}? Answer:"
            phrasing = "C-first"
        bench.append({"id": f"exp077_element_2hop_{i}", "prompt": p, "A": A, "C": C,
                      "ent": A, "typ": "element", "hop": 2, "domain": "Elemental",
                      "phrasing": phrasing})
    for i, (iA, iB, iC, iD) in enumerate(QUADS_INDICES):
        A, B, C, D_ent = (NOVEL_VOCAB_ELEMENT[iA], NOVEL_VOCAB_ELEMENT[iB],
                          NOVEL_VOCAB_ELEMENT[iC], NOVEL_VOCAB_ELEMENT[iD])
        target_first = (i % 2 == 0)
        q_opts = f"{A} or {D_ent}" if target_first else f"{D_ent} or {A}"
        if i < 7:
            p = (f"Premise: {A} outranks {B}. {B} outranks {C}. {C} outranks {D_ent}. "
                 f"Question: Who is higher in rank, {q_opts}? Answer:")
            phrasing = "A-first"
        else:
            p = (f"Premise: {D_ent} is lower than {C}. {C} is lower than {B}. "
                 f"{B} is lower than {A}. Question: Who is higher in rank, {q_opts}? Answer:")
            phrasing = "C-first"
        bench.append({"id": f"exp077_element_3hop_{i}", "prompt": p, "A": A, "C": D_ent,
                      "ent": A, "typ": "element", "hop": 3, "domain": "Elemental",
                      "phrasing": phrasing})
    assert len(bench) == N_BENCH, f"Expected {N_BENCH} benchmark items, got {len(bench)}"
    return bench


def state_text_of(prompt):
    """Signed-protocol §6 state text: premise sentences only.

    Substring of `prompt` from "Premise:" up to (excluding) " Question:".
    The question and option list are EXCLUDED by construction.
    """
    assert prompt.startswith("Premise:"), "prompt does not start with 'Premise:'"
    cut = prompt.index(" Question:")
    return prompt[:cut]


def verify_against_instance_records(bench):
    """Assert the (ent, typ) sequence matches exp077_instance_records.json
    byte-for-value (signed-protocol §6). Returns the records on success."""
    path = os.path.join(artifacts_dir(), "exp077_instance_records.json")
    with open(path) as f:
        records = json.load(f)
    assert len(records) == len(bench) == N_BENCH, "record/bench length mismatch"
    for b, r in zip(bench, records):
        assert (b["ent"], b["typ"]) == (r["ent"], r["typ"]), (
            f"(ent, typ) mismatch: bench {(b['ent'], b['typ'])} vs "
            f"records {(r['ent'], r['typ'])}")
    return records


def assert_phrasing_balance(bench):
    """Signed-protocol §6 G3: exactly 30 A-first / 30 C-first items."""
    n_a = sum(1 for b in bench if b["phrasing"] == "A-first")
    n_c = sum(1 for b in bench if b["phrasing"] == "C-first")
    assert n_a == 30 and n_c == 30, (
        f"G3 FAIL: phrasing balance {n_a}/30 A-first, {n_c}/30 C-first")
    return n_a, n_c
