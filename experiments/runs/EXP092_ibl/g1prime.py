"""EXP092 G1' tokenizer guard — real-tokenizer offset-mapping cover check.

Signed protocol §6 G1': every A/C occurrence in every constructed prompt must
be covered by exactly one token, VERIFIED BY EXECUTING THE REAL TOKENIZER —
never by word-commonness reasoning (§8 standing rule).

Two enforcement points (same pattern as EXP091):
  (i)  at extraction startup, the real tokenizer runs over all 60 built
       prompts (offset-mapping cover check) and fails loud on any entity
       span that is not single-token;
  (ii) the build-time verification artifact (g1prime_verification.json,
       produced by executing the real tokenizer at build time) is
       re-verified in mock mode, bound to the bench pin.

Any multi-token entity occurrence -> RUN-INVALID. Items are NOT silently
dropped (the registered bar requires exactly N=60).
"""

import json
import os
import re

import reference_implementation as ref
from protocol_pin import BENCH_PIN

ARTIFACT_NAME = "g1prime_verification.json"
EXPECTED_OCCURRENCES = 240  # registered: 240/240 A/C occurrences single-token


class RunInvalid(Exception):
    """G1' failure -> RUN-INVALID (withheld, never a verdict)."""


def _word_pattern(name):
    return re.compile(r"\b" + re.escape(name) + r"\b")


def verify_g1_prime(tokenizer, bench=None):
    """Execute the real tokenizer over all prompts; return per-entity table.

    table[name] = {"occurrences": int, "single_token": int, "token_id": int|None}
    Raises RunInvalid on any occurrence not covered by exactly one token
    whose surface form equals the entity name, or on unstable token ids.
    """
    bench = bench if bench is not None else ref.build_bench()
    entities = sorted({b["A"] for b in bench} | {b["C"] for b in bench})
    table = {name: {"occurrences": 0, "single_token": 0, "token_id": None}
             for name in entities}
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
                    text = pieces[i].lstrip("\u0120").lstrip("▁")
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
            f"{f['item']}/{f['role']}/{f['entity']}@{f['span']}→"
            f"{f['covering_tokens']}" for f in failures[:8])
        raise RunInvalid(
            f"G1' FAIL: {len(failures)} A/C occurrence(s) not covered by "
            f"exactly one token (e.g. {detail}) — RUN-INVALID (items are NOT "
            f"silently dropped).")
    return table


def write_g1prime_artifact(tokenizer, path=None):
    """Build-time: execute the real tokenizer and record the artifact."""
    bench = ref.build_bench()
    table = verify_g1_prime(tokenizer, bench)
    n_occ = sum(v["occurrences"] for v in table.values())
    n_single = sum(v["single_token"] for v in table.values())
    artifact = {
        "experiment": "EXP092",
        "guard": "G1'",
        "bench_pin": ref.bench_sha256(bench),
        "n_occurrences": n_occ,
        "n_single_token": n_single,
        "expected_occurrences": EXPECTED_OCCURRENCES,
        "per_entity": table,
    }
    if n_occ != EXPECTED_OCCURRENCES or n_single != EXPECTED_OCCURRENCES:
        raise RunInvalid(
            f"G1' build-time FAIL: {n_single}/{n_occ} single-token, expected "
            f"{EXPECTED_OCCURRENCES}/{EXPECTED_OCCURRENCES} — RUN-INVALID.")
    path = path or os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                ARTIFACT_NAME)
    with open(path, "w") as f:
        json.dump(artifact, f, indent=1, sort_keys=True)
    return artifact


def check_g1prime_artifact(path=None):
    """Re-verify the build-time artifact: present, 240/240, bound to the
    current builder output via the bench pin. Raises RunInvalid on any
    mismatch (tampered or stale artifact refuses)."""
    path = path or os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                ARTIFACT_NAME)
    if not os.path.isfile(path):
        raise RunInvalid(
            f"G1' FAIL: build-time verification artifact not found at {path} "
            "— RUN-INVALID.")
    with open(path) as f:
        artifact = json.load(f)
    if artifact.get("bench_pin") != BENCH_PIN:
        raise RunInvalid(
            f"G1' FAIL: artifact bench pin {artifact.get('bench_pin')} != "
            f"registered {BENCH_PIN} — stale artifact; RUN-INVALID.")
    current_pin = ref.bench_sha256()
    if artifact.get("bench_pin") != current_pin:
        raise RunInvalid(
            "G1' FAIL: artifact pin does not match current builder output — "
            "stale artifact; RUN-INVALID.")
    if (artifact.get("n_single_token") != EXPECTED_OCCURRENCES
            or artifact.get("n_occurrences") != EXPECTED_OCCURRENCES):
        raise RunInvalid(
            f"G1' FAIL: artifact records "
            f"{artifact.get('n_single_token')}/{artifact.get('n_occurrences')} "
            f"single-token, expected {EXPECTED_OCCURRENCES}/"
            f"{EXPECTED_OCCURRENCES} — RUN-INVALID.")
    return artifact
