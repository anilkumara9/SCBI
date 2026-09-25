#!/usr/bin/env python3
"""EXP087 benchmark construction — verbatim port of the EXP065/066 60-item
2-hop/3-hop relational set (K1_execute_LOG213_2026-09-23.py ll. 160-260).

The benchmark is EXP066-identical (protocol §3). item["target_token"] /
item["foil_token"] carry the leading space per the runners; token ids are
derived at execution time via tokenizer.encode(" " + label)[0].

The pinned item order O (protocol §8 item 2, resolved LOG-314):
  O = [pythia410m_planet_2hop_0..14, pythia410m_planet_3hop_0..14,
       pythia410m_element_2hop_0..14, pythia410m_element_3hop_0..14]
"""

import hashlib
import json
import os

# Byte-verbatim from K1_execute_LOG213_2026-09-23.py (EXP065 ll. 106-118,
# EXP066 ll. 108-117, EXP077 ll. 149-150).
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


def build_items():
    """Verbatim port of build_exp065_066_items(). Returns 60 dicts."""
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


def order_O():
    """The pinned item order O (§8 item 2): 60 verbatim instance keys."""
    keys = []
    for i in range(15):
        keys.append(f"pythia410m_planet_2hop_{i}")
    for i in range(15):
        keys.append(f"pythia410m_planet_3hop_{i}")
    for i in range(15):
        keys.append(f"pythia410m_element_2hop_{i}")
    for i in range(15):
        keys.append(f"pythia410m_element_3hop_{i}")
    assert len(keys) == 60 and len(set(keys)) == 60
    return keys


def prompt_sha256(prompt):
    """SHA-256 over the UTF-8 bytes of the prompt string, byte-verbatim,
    no normalization (§8 item 2 pinned hash function)."""
    return hashlib.sha256(prompt.encode("utf-8")).hexdigest()


def g2_byte_identity_check(archive_path):
    """K1's G2 guard, re-implemented: the EXP066 archive's insertion order
    must equal O, and every rebuilt prompt must match the archived prompt
    byte-verbatim. Raises AssertionError (FATAL) on any mismatch.

    This is the constructible half of the pinned join (§8 item 2).
    """
    items = build_items()
    O = order_O()
    with open(archive_path, "r", encoding="utf-8") as f:
        archive = json.load(f)
    arch_keys = list(archive.keys())
    assert len(arch_keys) == 60, f"G2 FATAL: archive has {len(arch_keys)} keys, expected 60"
    assert arch_keys == O, "G2 FATAL: archive insertion order != pinned O"
    for j, key in enumerate(O):
        assert archive[key]["prompt"] == items[j]["prompt"], (
            f"G2 FATAL: prompt mismatch at O[{j}] = {key}")
    return True


def default_archive_path():
    here = os.path.dirname(os.path.abspath(__file__))
    scbi = os.path.abspath(os.path.join(here, "..", "..", ".."))
    return os.path.join(
        scbi, "experiments", "runs", "EXP066_pythia410m_replication",
        "exp066_instance_evaluations.json")
