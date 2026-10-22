"""EXP120 (H15/LFH-GEN2) bench-2 builder — construction material (LOG-4633).

Deterministic construction of the 60-item second template-decorrelated test bench,
independently authored from the EXP107 bench. Pure string construction —
no model calls, no RNG, no new vocabulary at build time.

New vocabulary: two new 5-entity named sets in new domains
(rivers: Nile/Amazon/Yangtze/Ganges/Thames; trees: Oak/Pine/Birch/Cedar/Maple),
disjoint from the EXP107 bench's planets/elements. New verb families
(family-1 "surpasses", family-2 "is below") — a meaning-preserving pair that
expresses ranking; no bench-2 premise contains the EXP107 substrings
" outranks " or " is lower than ".

Meaning-preserving flip discipline (mirror of the EXP107 builder's rule):
  reverse the premise sentence order AND swap the verb family
  ("surpasses" <-> "is below"), re-anchoring subject/object so the
  ranking meaning (A > B > C [> D]) ... preserved, and the target's sentence
  position (first sentence for A-first, last for C-first) is preserved.

  2-hop A-first : "Premise: {A} surpasses {B}. {B} surpasses {C}."
              -> "Premise: {B} is below {A}. {C} is below {B}."
  2-hop C-first : "Premise: {C} is below {B}. {B} is below {A}."
              -> "Premise: {B} surpasses {C}. {A} surpasses {B}."
  3-hop A-first : "Premise: {A} surpasses {B}. {B} surpasses {C}. {C} surpasses {D}."
              -> "Premise: {B} is below {A}. {C} is below {B}. {D} is below {C}."
  3-hop C-first : "Premise: {D} is below {C}. {C} is below {B}. {B} is below {A}."
              -> "Premise: {C} surpasses {D}. {B} surpasses {C}. {A} surpasses {B}."

Flip selection (deterministic, no RNG): within each phrasing group (30 items,
sorted by item ID), flip the items at even sorted positions (0, 2, ..., 28) ->
15 flipped + 15 original per phrasing -> four 15-item cells:
  (A-first, original-words), (A-first, flipped-words),
  (C-first, original-words), (C-first, flipped-words).

Label semantics [Law #7; the EXP119 FIX-1 lesson]: this builder's
meaning-preserving construction preserves "the ranking meaning
(A > B > C [> D]) ... preserved", so tuple[0] = A is the highest-ranked
entity on all 60 items; this is pinned independently by the per-item
assertion in verify_cells (tuple[0] in the first premise sentence iff
A-first). The pre-registration and the execution report cite this
docstring plus that independent pin — never a truncated inline comment.

Honest limitation (mirroring the EXP107 registration): the flip also moves the
target from sentence-subject to sentence-object position, so a collapsed score
kills the generality reading under EITHER a word-template cue or a
subject-position cue; the test does not identify which surface cue the head
used. It discriminates "shared-construction artifact" from "target-position
readout surviving meaning-preserving rephrasing" — and that is the question.
"""

import hashlib
import json

# ---------------------------------------------------------------------------
# Bench-2 vocabulary: new domains, disjoint from the EXP107 bench's
# {Mars, Venus, Jupiter, Saturn, Mercury, Iron, Gold, Silver, Bronze, Steel}.
# ---------------------------------------------------------------------------
VOCAB_RIVER = ["Nile", "Amazon", "Yangtze", "Ganges", "Thames"]
VOCAB_TREE = ["Oak", "Pine", "Birch", "Cedar", "Maple"]

# Entity-index sequences: hand-authored via the deterministic affine
# re-indexing x -> (4*x + 1) mod 5 applied to tuple-reversed EXP107
# sequences. Verified |Pearson| = 0.0475 <= 0.10 vs the EXP107 builder
# records as a design check only (Law #13 fence: feeds no bench-1 labels
# or embeddings into the analysis).
TRIPLES_B2 = [
    (4, 0, 1),
    (3, 4, 0),
    (2, 3, 4),
    (2, 4, 1),
    (3, 0, 1),
    (2, 3, 0),
    (3, 4, 1),
    (2, 4, 0),
    (2, 3, 1),
    (2, 0, 1),
    (4, 0, 1),
    (3, 4, 0),
    (2, 3, 4),
    (2, 4, 1),
    (3, 0, 1),
]
QUADS_B2 = [
    (3, 4, 0, 1),
    (2, 3, 4, 0),
    (2, 3, 0, 1),
    (2, 3, 4, 1),
    (2, 4, 0, 1),
    (3, 4, 0, 1),
    (2, 3, 4, 0),
    (2, 3, 0, 1),
    (2, 3, 4, 1),
    (2, 4, 0, 1),
    (3, 4, 0, 1),
    (2, 3, 4, 0),
    (2, 3, 0, 1),
    (2, 3, 4, 1),
    (2, 4, 0, 1),
]

# New verb families (meaning-preserving ranking pair).
FAM1 = "surpasses"      # family-1: "{A} surpasses {B}"  (A > B)
FAM2 = "is below"       # family-2: "{B} is below {A}"   (A > B)

QUESTION_SUFFIX = " Question: Who is higher in rank? Answer:"
N_BENCH = 60


def _base_items():
    """The 60 bench-2 base item records (id, premise, phrasing, entities)."""
    items = []
    for vocab, triples, quads, dom, thr in (
            (VOCAB_RIVER, TRIPLES_B2, QUADS_B2, 'river', 8),
            (VOCAB_TREE, TRIPLES_B2, QUADS_B2, 'tree', 7)):
        for i, (iA, iB, iC) in enumerate(triples):
            A, B, C = vocab[iA], vocab[iB], vocab[iC]
            a_first = i < thr
            premise = (f"Premise: {A} surpasses {B}. {B} surpasses {C}." if a_first
                       else f"Premise: {C} is below {B}. {B} is below {A}.")
            items.append({'id': f'exp120_{dom}_2hop_{i}', 'premise': premise,
                          'phrasing': 'A-first' if a_first else 'C-first',
                          'domain': dom, 'hop': 2,
                          'ents': (A, B, C), 'src_index': i})
        for i, (iA, iB, iC, iD) in enumerate(quads):
            A, B, C, D = vocab[iA], vocab[iB], vocab[iC], vocab[iD]
            a_first = i < thr
            premise = (f"Premise: {A} surpasses {B}. {B} surpasses {C}. {C} surpasses {D}." if a_first
                       else f"Premise: {D} is below {C}. {C} is below {B}. {B} is below {A}.")
            items.append({'id': f'exp120_{dom}_3hop_{i}', 'premise': premise,
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
        return (f"Premise: {B} is below {A}. {C} is below {B}." if a_first
                else f"Premise: {B} surpasses {C}. {A} surpasses {B}.")
    A, B, C, D = ents
    return (f"Premise: {B} is below {A}. {C} is below {B}. {D} is below {C}." if a_first
            else f"Premise: {C} surpasses {D}. {B} surpasses {C}. {A} surpasses {B}.")


def _word_family(premise):
    """Which verb family the premise uses (for cell-balance verification)."""
    if ' surpasses ' in premise:
        assert ' is below ' not in premise
        return 'surpasses'
    assert ' is below ' in premise
    return 'below'


def build_bench():
    """Build the 60-item bench-2. Deterministic; no RNG."""
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
            'id': ('exp120_flip_' if flipped else 'exp120_ctrl_') + b['id'],
            'prompt': premise + QUESTION_SUFFIX,
            'premise': premise,
            'phrasing': b['phrasing'],
            'domain': b['domain'],
            'hop': b['hop'],
            'tuple': list(b['ents']),
            'flipped': flipped,
            'y': 1 if b['phrasing'] == 'A-first' else 0,
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
        expected = ('below' if a_first else 'surpasses') if b['flipped'] \
            else ('surpasses' if a_first else 'below')
        assert fam == expected, (b['id'], fam, expected)
        # Extraction contract: premise == state_text_of(prompt).
        assert b['prompt'].startswith('Premise:')
        assert b['premise'] == b['prompt'][:b['prompt'].index(' Question:')]
        # No bench-1 verb-family leakage.
        assert ' outranks ' not in b['premise'] and ' is lower than ' not in b['premise']
        # Label pin (independent): tuple[0] (the target) in first premise
        # sentence iff A-first.
        first_sent = b['premise'][len('Premise: '):].split('. ')[0]
        tgt = b['tuple'][0]
        assert (tgt in first_sent) == a_first, (b['id'], first_sent, tgt)
        # Label convention: y = 1 iff A-first.
        assert b['y'] == (1 if a_first else 0)
    ids = [b['id'] for b in bench]
    assert len(set(ids)) == N_BENCH
    assert not any(i.startswith('exp107_') for i in ids), "bench-1 ID collision"
    assert not any(i.startswith('exp092_') for i in ids), "train/test ID collision"
    return {'n': len(bench), 'cells': dict(cells), 'pin': bench_sha256(bench)}


def gate_gc1(bench=None):
    """G-C1: pure-template detector gate. T predicts A-first iff the first
    premise sentence uses bench-2's family-1 ("surpasses"). By the flip
    discipline T scores 30/60 by construction. Gate: T <= 36/60
    (not above chance at alpha=0.05 one-sided: P(X>=37|60,0.5) ~= 0.047)."""
    bench = bench if bench is not None else build_bench()
    correct = 0
    for b in bench:
        first_sent = b['premise'][len('Premise: '):].split('. ')[0]
        pred_a_first = ' surpasses ' in first_sent
        if pred_a_first == (b['phrasing'] == 'A-first'):
            correct += 1
    return {'score': correct, 'n': N_BENCH, 'pass': correct <= 36}


def _entity_index_seqs(triples, quads):
    """Flattened vocabulary-index sequences, zero-padded to length 4, in
    canonical builder emission order (river triples, river quads, tree
    triples, tree quads)."""
    seqs = []
    for idxs in (triples, quads, triples, quads):
        for t in idxs:
            seqs.extend(list(t) + [0] * (4 - len(t)))
    return seqs


def gate_gc2():
    """G-C2: entity-rank correlation gate. |Pearson(r1, r2)| <= 0.10, where
    r1/r2 are the flattened entity-index sequences of bench 1 / bench 2 in
    canonical item order. Compares bench-2's construction against bench-1's
    builder records for this design check only; feeds no bench-1 labels or
    embeddings into the analysis (Law #13 fence)."""
    import numpy as np
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "build_exp107_bench",
        "/home/hatch/workspace/SCBI/experiments/runs/EXP107_templatectrl/build_exp107_bench.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r1 = _entity_index_seqs(mod.TRIPLES, mod.QUADS)
    r2 = _entity_index_seqs(TRIPLES_B2, QUADS_B2)
    r = float(np.corrcoef(np.asarray(r1, dtype=float),
                          np.asarray(r2, dtype=float))[0, 1])
    return {'pearson': r, 'abs_pearson': abs(r), 'pass': abs(r) <= 0.10}


def gate_gc3():
    """G-C3: template-decomposition pin. Bench-2's decomposition is
    independently pinned: QUESTION_SUFFIX byte-exact (shared format with
    the EXP107 builder) + canonical-order deterministic construction."""
    ok = QUESTION_SUFFIX == " Question: Who is higher in rank? Answer:"
    det = bench_sha256(build_bench()) == bench_sha256(build_bench())
    return {'suffix_byte_exact': ok, 'deterministic': det, 'pass': ok and det}


if __name__ == '__main__':
    bench = build_bench()
    v = verify_cells(bench)
    print("cells:", json.dumps({f"{p}/{w}": c for (p, w), c in v['cells'].items()},
                               indent=1, sort_keys=True))
    print("pin:", v['pin'])
    g1 = gate_gc1(bench)
    print(f"G-C1 pure-template detector: {g1['score']}/{g1['n']} pass={g1['pass']}")
    g2 = gate_gc2()
    print(f"G-C2 entity-rank correlation: {g2['pearson']:+.4f} pass={g2['pass']}")
    g3 = gate_gc3()
    print(f"G-C3 decomposition pin: pass={g3['pass']}")
    # Show one example per cell.
    seen = set()
    for b in bench:
        key = (b['phrasing'], 'flipped' if b['flipped'] else 'original')
        if key not in seen:
            seen.add(key)
            print(f"\n[{key[0]} / {key[1]}] {b['id']}\n  {b['premise']}")
