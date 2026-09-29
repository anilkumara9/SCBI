"""EXP107 template-control bench builder — pre-registration design material (LOG-4535).

Deterministic construction of the 60-item template-decorrelated test bench that
decouples the surface template from the phrasing label. Pure string rewriting
of the registered EXP091/EXP077 item records — no model calls, no RNG, no new
vocabulary.

Rephrasing rule (closed vocabulary, meaning-preserving):
  reverse the premise sentence order AND swap the verb family
  ("outranks" <-> "is lower than"), re-anchoring subject/object so the
  ranking meaning (A > B > C [> D]) and the target's sentence position
  (first for A-first, last for C-first) are preserved.

  2-hop A-first : "Premise: {A} outranks {B}. {B} outranks {C}."
              -> "Premise: {B} is lower than {A}. {C} is lower than {B}."
  2-hop C-first : "Premise: {C} is lower than {B}. {B} is lower than {A}."
              -> "Premise: {B} outranks {C}. {A} outranks {B}."
  3-hop A-first : "Premise: {A} outranks {B}. {B} outranks {C}. {C} outranks {D}."
              -> "Premise: {B} is lower than {A}. {C} is lower than {B}. {D} is lower than {C}."
  3-hop C-first : "Premise: {D} is lower than {C}. {C} is lower than {B}. {B} is lower than {A}."
              -> "Premise: {C} outranks {D}. {B} outranks {C}. {A} outranks {B}."

Flip selection (deterministic, no RNG): within each phrasing group (30 items,
sorted by item ID), flip the items at even sorted positions (0, 2, ..., 28) ->
15 flipped + 15 original per phrasing -> four 15-item cells:
  (A-first, original-words), (A-first, flipped-words),
  (C-first, original-words), (C-first, flipped-words).

Honest limitation (registered): the flip also moves the target from
sentence-subject to sentence-object position, so a collapsed score kills the
EXP106 transfer reading under EITHER a word-template cue or a
subject-position cue; the test does not identify which surface cue the head
used. It discriminates "shared-construction artifact" from "target-position
readout surviving meaning-preserving rephrasing" — and that is the question.
"""

import hashlib
import json

# ---------------------------------------------------------------------------
# EXP091/EXP077 bench records, verbatim from the EXP106 executor's
# build_test_premises() (repaired EXP077 builder logic). Registered source.
# ---------------------------------------------------------------------------
NOVEL_VOCAB_PLANET = ["Mars", "Venus", "Jupiter", "Saturn", "Mercury"]
NOVEL_VOCAB_ELEMENT = ["Iron", "Gold", "Silver", "Bronze", "Steel"]
TRIPLES = [(0, 1, 2), (1, 2, 3), (2, 3, 4), (0, 2, 4), (0, 1, 3), (1, 3, 4),
           (0, 2, 3), (1, 2, 4), (0, 3, 4), (0, 1, 4),
           (0, 1, 2), (1, 2, 3), (2, 3, 4), (0, 2, 4), (0, 1, 3)]
QUADS = [(0, 1, 2, 3), (1, 2, 3, 4), (0, 1, 3, 4), (0, 2, 3, 4), (0, 1, 2, 4),
         (0, 1, 2, 3), (1, 2, 3, 4), (0, 1, 3, 4), (0, 2, 3, 4), (0, 1, 2, 4),
         (0, 1, 2, 3), (1, 2, 3, 4), (0, 1, 3, 4), (0, 2, 3, 4), (0, 1, 2, 4)]

QUESTION_SUFFIX = " Question: Who is higher in rank? Answer:"
N_BENCH = 60


def _base_items():
    """The 60 EXP091 item records (id, premise, phrasing, entities)."""
    items = []
    for vocab, triples, quads, dom, thr in (
            (NOVEL_VOCAB_PLANET, TRIPLES, QUADS, 'planet', 8),
            (NOVEL_VOCAB_ELEMENT, TRIPLES, QUADS, 'element', 7)):
        for i, (iA, iB, iC) in enumerate(triples):
            A, B, C = vocab[iA], vocab[iB], vocab[iC]
            a_first = i < thr
            premise = (f"Premise: {A} outranks {B}. {B} outranks {C}." if a_first
                       else f"Premise: {C} is lower than {B}. {B} is lower than {A}.")
            items.append({'id': f'exp077_{dom}_2hop_{i}', 'premise': premise,
                          'phrasing': 'A-first' if a_first else 'C-first',
                          'domain': dom, 'hop': 2,
                          'ents': (A, B, C), 'src_index': i})
        for i, (iA, iB, iC, iD) in enumerate(quads):
            A, B, C, D = vocab[iA], vocab[iB], vocab[iC], vocab[iD]
            a_first = i < thr
            premise = (f"Premise: {A} outranks {B}. {B} outranks {C}. {C} outranks {D}." if a_first
                       else f"Premise: {D} is lower than {C}. {C} is lower than {B}. {B} is lower than {A}.")
            items.append({'id': f'exp077_{dom}_3hop_{i}', 'premise': premise,
                          'phrasing': 'A-first' if a_first else 'C-first',
                          'domain': dom, 'hop': 3,
                          'ents': (A, B, C, D), 'src_index': i})
    assert len(items) == N_BENCH
    return items


def flip_premise(item):
    """Meaning-preserving template flip: reverse sentence order, swap verb family."""
    ents = item['ents']
    a_first = (item['phrasing'] == 'A-first')
    if item['hop'] == 2:
        A, B, C = ents
        return (f"Premise: {B} is lower than {A}. {C} is lower than {B}." if a_first
                else f"Premise: {B} outranks {C}. {A} outranks {B}.")
    A, B, C, D = ents
    return (f"Premise: {B} is lower than {A}. {C} is lower than {B}. {D} is lower than {C}." if a_first
            else f"Premise: {C} outranks {D}. {B} outranks {C}. {A} outranks {B}.")


def _word_family(premise):
    """Which verb family the premise uses (for cell-balance verification)."""
    if ' outranks ' in premise:
        assert ' is lower than ' not in premise
        return 'outranks'
    assert ' is lower than ' in premise
    return 'lower-than'


def build_bench():
    """Build the 60-item decorrelated bench. Deterministic; no RNG."""
    base = _base_items()
    # Flip selection: within each phrasing group (sorted by id), even positions flip.
    flip_ids = set()
    for phrasing in ('A-first', 'C-first'):
        group = sorted([b for b in base if b['phrasing'] == phrasing],
                       key=lambda b: b['id'])
        assert len(group) == 30, f"phrasing group size {len(group)} != 30"
        flip_ids.update(b['id'] for k, b in enumerate(group) if k % 2 == 0)
    assert len(flip_ids) == 30
    bench = []
    for b in base:  # emit in the original builder order
        flipped = b['id'] in flip_ids
        premise = flip_premise(b) if flipped else b['premise']
        bench.append({
            'id': ('exp107_flip_' if flipped else 'exp107_ctrl_') + b['id'],
            'prompt': premise + QUESTION_SUFFIX,
            'premise': premise,
            'phrasing': b['phrasing'],
            'domain': b['domain'],
            'hop': b['hop'],
            'tuple': list(b['ents']),
            'flipped': flipped,
            'derived_from': b['id'],
        })
    assert len(bench) == N_BENCH
    return bench


def canonical_json(bench):
    return json.dumps(bench, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("utf-8")


def bench_sha256(bench=None):
    bench = bench if bench is not None else build_bench()
    return hashlib.sha256(canonical_json(bench)).hexdigest()


def verify_cells(bench=None):
    """Design-time assertions: balance, cell counts, disjointness, contract."""
    from collections import Counter
    bench = bench if bench is not None else build_bench()
    assert len(bench) == N_BENCH
    ph = Counter(b['phrasing'] for b in bench)
    assert ph['A-first'] == 30 and ph['C-first'] == 30, dict(ph)
    cells = Counter((b['phrasing'],
                     'flipped' if b['flipped'] else 'original') for b in bench)
    assert all(v == 15 for v in cells.values()), dict(cells)
    # Word-family check: flipped items must use the OPPOSITE family from originals.
    for b in bench:
        fam = _word_family(b['premise'])
        a_first = (b['phrasing'] == 'A-first')
        expected = ('lower-than' if a_first else 'outranks') if b['flipped'] \
            else ('outranks' if a_first else 'lower-than')
        assert fam == expected, (b['id'], fam, expected)
        # Extraction contract: premise == state_text_of(prompt).
        assert b['prompt'].startswith('Premise:')
        assert b['premise'] == b['prompt'][:b['prompt'].index(' Question:')]
        # Label semantics: target (tuple[0]) in first premise sentence iff A-first.
        first_sent = b['premise'][len('Premise: '):].split('. ')[0]
        tgt = b['tuple'][0]
        assert (tgt in first_sent) == a_first, (b['id'], first_sent, tgt)
    ids = [b['id'] for b in bench]
    assert len(set(ids)) == N_BENCH and all(i.startswith('exp107_') for i in ids)
    assert not any(i.startswith('exp092_') for i in ids), "train/test ID collision"
    return {'n': len(bench), 'cells': dict(cells), 'pin': bench_sha256(bench)}


if __name__ == '__main__':
    bench = build_bench()
    v = verify_cells(bench)
    print("cells:", json.dumps({f"{p}/{w}": c for (p, w), c in v['cells'].items()},
                               indent=1, sort_keys=True))
    print("pin:", v['pin'])
    # Show one example per cell.
    seen = set()
    for b in bench:
        key = (b['phrasing'], 'flipped' if b['flipped'] else 'original')
        if key not in seen:
            seen.add(key)
            print(f"\n[{key[0]} / {key[1]}] {b['id']}\n  {b['premise']}")
