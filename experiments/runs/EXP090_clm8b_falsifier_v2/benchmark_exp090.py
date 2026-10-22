"""EXP090 benchmark builder — VERBATIM port of the EXP077 N=60 benchmark.

Provenance: ported verbatim from
    experiments/runs/exp077/run_exp077.py  (benchmark block, §3 of main())
which was itself ported verbatim from experiments/runs/exp078/run_exp078.py §2
(MAJOR-3 repair; Law #9: no new benchmark construction).
Adapted from experiments/runs/EXP089_clm8b_falsifier/benchmark_exp089.py
(EXP089 SUPERSEDED-BY-EXP090 for execution; modules reused).

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
EXP090 uses no support prompts (documented in BUILD_NOTES.md).

§6 BENCH CONTRACT (the single design change vs EXP089):
EXP090 defines its benchmark as the deterministic output of this verbatim
port. The EXP089 byte-for-value (ent, typ) reproduction guard is STRUCK as
unsatisfiable (LOG-344/345 — binding). Instead, the archive
`exp077_instance_records.json` is pinned as the PROVENANCE record:
`assert_archive_hash()` asserts its SHA-256 equals the §6-recorded hash
(47281cd3…0585); mismatch → RUN-INVALID. Caveat 6 (load-bearing, verbatim in
the signed protocol): any claim of the form "this is exactly the bench
EXP077 ran" is UNLICENSED.
"""

import hashlib
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

# Signed-protocol §6 provenance pin: the archive is pinned as the provenance
# record the construction descends from (NOT as the item source — caveat 6).
ARCHIVE_PROVENANCE_HASH = ARTIFACT_HASHES["exp077_instance_records.json"]

SIGNED_PROTOCOL_DIGEST = (
    "440dd6a53ab88a199c88a57e629768aa9414cc1f9d907b33e2ab6019aa79c0ab"
)


class RunInvalid(Exception):
    """Raised when a signed-protocol guard fires → RUN-INVALID (withheld)."""


def _repo_root():
    # Bundle lives at experiments/runs/EXP090_clm8b_falsifier_v2/; repo root is 3 up.
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))


def artifacts_dir():
    return os.path.join(_repo_root(), "experiments", "runs", "EXP077_cone_vs_line")


def signed_protocol_path():
    return os.path.join(
        _repo_root(), "experiments", "protocols",
        "EXP090_CLM8B_ADAPTATION_V2_PREREG_SIGNED.md")


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


def assert_archive_hash():
    """Signed-protocol §6 provenance pin (replaces the STRUCK byte-match guard).

    Asserts the SHA-256 of exp077_instance_records.json equals the
    §6-recorded hash. The archive is pinned as the provenance record the
    construction descends from — NOT as the item source (caveat 6).
    Mismatch → RUN-INVALID (signed protocol §8).
    """
    path = os.path.join(artifacts_dir(), "exp077_instance_records.json")
    sha = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            sha.update(chunk)
    got = sha.hexdigest()
    if got != ARCHIVE_PROVENANCE_HASH:
        raise RunInvalid(
            f"§6 provenance pin FAIL: exp077_instance_records.json SHA-256 "
            f"{got} != recorded {ARCHIVE_PROVENANCE_HASH} — RUN-INVALID.")
    return got


def assert_phrasing_balance(bench):
    """Signed-protocol §6 G3: exactly 30 A-first / 30 C-first items."""
    n_a = sum(1 for b in bench if b["phrasing"] == "A-first")
    n_c = sum(1 for b in bench if b["phrasing"] == "C-first")
    assert n_a == 30 and n_c == 30, (
        f"G3 FAIL: phrasing balance {n_a}/30 A-first, {n_c}/30 C-first")
    return n_a, n_c
