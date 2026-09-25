"""EXP091 benchmark builder — VERBATIM port of the EXP090 N=60 benchmark.

Provenance: ported verbatim from
    experiments/runs/EXP090_clm8b_falsifier_v2/benchmark_exp090.py
which was ported verbatim from experiments/runs/exp077/run_exp077.py
(benchmark block, §3 of main()) via experiments/runs/exp078/run_exp078.py §2
(MAJOR-3 repair; Law #9: no new benchmark construction), adapted through
experiments/runs/EXP089_clm8b_falsifier/benchmark_exp089.py.
(EXP089 SUPERSEDED-BY-EXP090 for execution; EXP090 SUPERSEDED-BY-EXP091 for
execution. All signed protocols immutable.)

The ONLY additions vs the EXP090 source block:
  - a "phrasing" field per item (carried from EXP090) — required by
    signed-protocol §6 G3 and §7.1.
  - `state_text_of(prompt)`: protocol-§6 state text (carried from EXP090).
  - G1' (signed protocol §6 — THE design change vs EXP090): in-context
    single-token verification. `verify_g1_prime(tokenizer)` executes the real
    tokenizer over all 60 built prompts (offset-mapping cover check) and
    raises RunInvalid if any A/C occurrence is not covered by exactly one
    token. `action_text_of(name)` = " " + name is the embedded material the
    guard constrains (the §0 action-text coupling, accepted by Law #14 at
    LOG-356: the bare form was never coherently embeddable).

The anti-cheat support-prompt assert from EXP077 is intentionally NOT ported:
EXP091 uses no support prompts (documented in BUILD_NOTES.md).

§6 BENCH CONTRACT (carried from EXP090):
EXP091 defines its benchmark as the deterministic output of this verbatim
port. The archive `exp077_instance_records.json` is pinned as the PROVENANCE
record: `assert_archive_hash()` asserts its SHA-256 equals the §6-recorded
hash (47281cd3…0585); mismatch → RUN-INVALID. Caveat 6 (load-bearing, verbatim
in the signed protocol): any claim of the form "this is exactly the bench
EXP077 ran" is UNLICENSED.
"""

import hashlib
import json
import os
import re

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

ALL_ENTITIES = NOVEL_VOCAB_PLANET + NOVEL_VOCAB_ELEMENT

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
    "747bb6a5722e8478f57b645cad93b9fd54902271bd3f8a64da9a4e24236f417b"
)

# G1' build-time verification artifact (written at build time by executing
# the real tokenizer; re-verified by --mock runs).
G1PRIME_VERIFICATION_FILENAME = "g1prime_verification.json"


class RunInvalid(Exception):
    """Raised when a signed-protocol guard fires → RUN-INVALID (withheld)."""


def _repo_root():
    # Bundle lives at experiments/runs/EXP091_clm8b_falsifier_v3/; repo root is 3 up.
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))


def _bundle_dir():
    return os.path.dirname(os.path.abspath(__file__))


def artifacts_dir():
    return os.path.join(_repo_root(), "experiments", "runs", "EXP077_cone_vs_line")


def signed_protocol_path():
    return os.path.join(
        _repo_root(), "experiments", "protocols",
        "EXP091_CLM8B_ADAPTATION_V3_PREREG_SIGNED.md")


# ---------------------------------------------------------------------------
# Benchmark — VERBATIM port of the EXP090 benchmark block.
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


def action_text_of(name):
    """Signed-protocol §6 action texts: the entity's natural single-token BPE form.

    The §0 action-text coupling (accepted by Law #14 at LOG-356): GPT-NeoX
    BPE represents these entities as single tokens only in spaced form
    ("ĠMars"); the bare form fragments ("Mars" → 2 tokens), which is what
    killed EXP090's execution at the old G1 gate. The spaced form is the same
    lexical item in its natural BPE form — the identical token id that appears
    at every in-prompt occurrence, by BPE determinism.
    """
    return " " + name


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


def bench_sha256(bench=None):
    """Deterministic hash of the built benchmark (for G1' artifact binding)."""
    bench = bench if bench is not None else build_benchmark()
    return hashlib.sha256(
        json.dumps(bench, sort_keys=True).encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# G1' — in-context single-token verification (signed protocol §6).
#
# The tokenizer interface: tokenizer(text, add_special_tokens=False,
# return_offsets_mapping=True) -> mapping with "input_ids" and
# "offset_mapping"; tokenizer.convert_ids_to_tokens(ids) -> [str].
# This is the HuggingFace fast-tokenizer interface; unit tests use a fake
# implementing the same interface (numpy-only, no weights).
# ---------------------------------------------------------------------------
_WORD_RE_CACHE = {}


def _word_pattern(name):
    if name not in _WORD_RE_CACHE:
        _WORD_RE_CACHE[name] = re.compile(
            r"(?<![A-Za-z])" + re.escape(name) + r"(?![A-Za-z])")
    return _WORD_RE_CACHE[name]


def verify_g1_prime(tokenizer):
    """G1': every A/C occurrence in every built prompt must be covered by
    exactly one token — VERIFIED BY EXECUTING THE TOKENIZER (never by
    word-commonness reasoning; §8 standing rule).

    Offset-mapping cover check: for each whole-word occurrence of A and C in
    each prompt, the occurrence's character span must lie within exactly one
    token, and that token's text (modulo the BPE space marker) must equal the
    entity name. Any violation → RunInvalid (RUN-INVALID; items are NOT
    silently dropped — the registered bar requires exactly N=60).

    Returns the per-entity verification table:
      {"Mars": {"occurrences": 42, "single_token": 42, "token_id": 13648}, ...}
    """
    bench = build_benchmark()
    table = {name: {"occurrences": 0, "single_token": 0, "token_id": None}
             for name in ALL_ENTITIES}
    failures = []
    for b in bench:
        prompt = b["prompt"]
        enc = tokenizer(prompt, add_special_tokens=False,
                        return_offsets_mapping=True)
        ids = list(enc["input_ids"])
        offsets = [(int(s), int(e)) for s, e in enc["offset_mapping"]]
        pieces = tokenizer.convert_ids_to_tokens(ids)
        for role, name in (("target", b["A"]), ("foil", b["C"])):
            for m in _word_pattern(name).finditer(prompt):
                s, e = m.span()
                table[name]["occurrences"] += 1
                covering = [i for i, (os_, oe_) in enumerate(offsets)
                            if os_ < e and oe_ > s]
                ok = False
                if len(covering) == 1:
                    i = covering[0]
                    os_, oe_ = offsets[i]
                    text = pieces[i].lstrip("Ġ").lstrip("▁")
                    if text == name and os_ <= s and oe_ >= e:
                        ok = True
                        if table[name]["token_id"] is None:
                            table[name]["token_id"] = int(ids[i])
                        elif table[name]["token_id"] != int(ids[i]):
                            ok = False  # same surface form, different token id
                if ok:
                    table[name]["single_token"] += 1
                else:
                    failures.append(
                        {"item": b["id"], "role": role, "entity": name,
                         "span": (s, e),
                         "covering_tokens": [pieces[i] for i in covering]})
    if failures:
        detail = "; ".join(
            f"{f['item']}/{f['role']}/{f['entity']}@{f['span']}→{f['covering_tokens']}"
            for f in failures[:8])
        raise RunInvalid(
            f"G1' FAIL: {len(failures)} A/C occurrence(s) not covered by "
            f"exactly one token (e.g. {detail}) — RUN-INVALID (items are NOT "
            f"silently dropped).")
    return table


def write_g1prime_verification(tokenizer, path=None):
    """Build-time G1' enforcement: execute the real tokenizer over all 60
    built prompts and record the verification artifact. Fails loud
    (RunInvalid) if any entity span is multi-token."""
    table = verify_g1_prime(tokenizer)
    total_occ = sum(v["occurrences"] for v in table.values())
    total_single = sum(v["single_token"] for v in table.values())
    artifact = {
        "experiment": "EXP091",
        "guard": "G1' (in-context single-token verification; signed protocol §6)",
        "n_prompts": N_BENCH,
        "occurrences_total": total_occ,
        "occurrences_single_token": total_single,
        "verdict": "G1' SATISFIED" if total_single == total_occ else "G1' FAILED",
        "per_entity": table,
        "bench_sha256": bench_sha256(),
        "note": ("Produced by EXECUTING the real tokenizer over the built "
                 "prompts (offset-mapping cover check) — never by "
                 "word-commonness reasoning (§8 standing rule)."),
    }
    path = path or os.path.join(_bundle_dir(), G1PRIME_VERIFICATION_FILENAME)
    with open(path, "w") as f:
        json.dump(artifact, f, indent=2)
    return artifact


def check_g1prime_artifact(path=None):
    """Re-verify the recorded build-time G1' artifact against the current
    builder output. Used by --mock (tokenizer-free): the artifact is the
    build-time real-tokenizer execution; mock asserts it is present,
    internally consistent (240/240), and bound to the current bench hash.
    Tampered/stale artifact → RunInvalid."""
    path = path or os.path.join(_bundle_dir(), G1PRIME_VERIFICATION_FILENAME)
    try:
        with open(path) as f:
            artifact = json.load(f)
    except (OSError, ValueError) as e:
        raise RunInvalid(
            f"G1' FAIL: build-time verification artifact unreadable at {path}: "
            f"{e} — RUN-INVALID.")
    total = artifact.get("occurrences_total")
    single = artifact.get("occurrences_single_token")
    if not (isinstance(total, int) and isinstance(single, int)
            and total == single and total == 240):
        raise RunInvalid(
            f"G1' FAIL: verification artifact inconsistent "
            f"(total={total}, single_token={single}; expected 240/240) — "
            f"RUN-INVALID.")
    if artifact.get("bench_sha256") != bench_sha256():
        raise RunInvalid(
            "G1' FAIL: verification artifact bench_sha256 does not match the "
            "current builder output — the bench changed after verification. "
            "RUN-INVALID.")
    if artifact.get("verdict") != "G1' SATISFIED":
        raise RunInvalid(
            f"G1' FAIL: verification artifact verdict is "
            f"{artifact.get('verdict')!r}, not \"G1' SATISFIED\" — RUN-INVALID.")
    return artifact
