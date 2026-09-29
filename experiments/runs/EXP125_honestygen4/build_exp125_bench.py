"""EXP125 (H22/HONESTY-GEN4) bench-4 builder — construction material (LOG-4679).

Deterministic construction of the 60-item fourth template-decorrelated bench,
independently authored from benches 1 (EXP107: planets/elements), 2 (EXP120:
rivers/trees), and 3 (EXP122: animals/fruits/cities). Pure string
construction — no model calls, no RNG, no new vocabulary at build time.

New vocabulary: two new named sets in new domains
(body parts: Heart/Lung/Liver/Bone/Brain/Eye/Ear/Hand/Foot/Rib/Skin;
weather: Rain/Snow/Storm/Wind/Ice/Frost/Cloud/Thunder/Mist/Dew),
disjoint from every prior bench's entity set (asserted by set-membership
check in verify_cells). New verb families (family-1 "outshines", family-2
"is outshone by") — a meaning-preserving pair that expresses ranking; no
bench-4 premise contains any prior bench's verb-family substring
(" outranks ", " is lower than ", " surpasses ", " is below ",
" dominates ", " is dominated by ").

Entity-index sequences: hand-authored via deterministic affine re-indexing
applied to the EXP107 builder's tuple-reversed base patterns —
body: x -> (2*x + 5) mod 11; weather: x -> (3*x + 5) mod 10.
Design check only: |Pearson| vs the EXP107 builder records = 0.0198 <= 0.10
(G-C2 diagnostic; feeds no bench-1 labels or embeddings into any analysis).

Meaning-preserving flip discipline (mirror of the EXP107/EXP120 builders):
  reverse the premise sentence order AND swap the verb family
  ("outshines" <-> "is outshone by"), re-anchoring subject/object so the
  ranking meaning (A > B > C [> D]) is preserved, and the target's sentence
  position (first sentence for A-first, last for C-first) is preserved.

  2-hop A-first : "Premise: {A} outshines {B}. {B} outshines {C}."
              -> "Premise: {B} is outshone by {A}. {C} is outshone by {B}."
  2-hop C-first : "Premise: {C} is outshone by {B}. {B} is outshone by {A}."
              -> "Premise: {B} outshines {C}. {A} outshines {B}."
  3-hop A-first : "Premise: {A} outshines {B}. {B} outshines {C}. {C} outshines {D}."
              -> "Premise: {B} is outshone by {A}. {C} is outshone by {B}. {D} is outshone by {C}."
  3-hop C-first : "Premise: {D} is outshone by {C}. {C} is outshone by {B}. {B} is outshone by {A}."
              -> "Premise: {C} outshines {D}. {B} outshines {C}. {A} outshines {B}."

Flip selection (deterministic, no RNG): within each phrasing group (30 items,
sorted by item ID), flip the items at even sorted positions (0, 2, ..., 28) ->
15 flipped + 15 original per phrasing -> four 15-item cells:
  (A-first, original-words), (A-first, flipped-words),
  (C-first, original-words), (C-first, flipped-words).

No item screening: exactly 60 base items are emitted and all 60 enter the
bench; flip selection is by sorted position, never by item content; no item
is filtered, dropped, or reweighted at construction (the EXP121 lesson).

Label semantics [Law #7; the FIX-1 discipline]: this builder's
meaning-preserving construction preserves "the ranking meaning
(A > B > C [> D]) ... preserved", so tuple[0] = A is the highest-ranked
entity on all 60 items; this is pinned independently by the per-item
assertion in verify_cells (tuple[0] in the first premise sentence, whole-word
match, iff A-first). The pre-registration and the execution report cite this
docstring plus that independent pin — never a truncated inline comment.
Labels enter only the pin, never the apparatus.

Honest limitation (mirroring the EXP107/EXP120 registrations): the flip also
moves the target from sentence-subject to sentence-object position, so a
collapsed score kills the generality reading under EITHER a word-template cue
or a subject-position cue; the test does not identify which surface cue is
used. It discriminates "shared-construction artifact" from "readout surviving
meaning-preserving rephrasing" — and that is the question.
"""

import hashlib
import json

# ---------------------------------------------------------------------------
# Bench-4 vocabulary: new domains, disjoint from bench 1
# {Mars, Venus, Jupiter, Saturn, Mercury, Iron, Gold, Silver, Bronze, Steel},
# bench 2 {Nile, Amazon, Yangtze, Ganges, Thames, Oak, Pine, Birch, Cedar,
# Maple}, and bench 3 {Apple, Bear, Cherry, Fox, Grape, Lion, Mango, Plum,
# Tiger, Wolf} (asserted by set-membership in verify_cells).
# ---------------------------------------------------------------------------
VOCAB_BODY = ["Heart", "Lung", "Liver", "Bone", "Brain", "Eye", "Ear",
              "Hand", "Foot", "Rib", "Skin"]
VOCAB_WEATHER = ["Rain", "Snow", "Storm", "Wind", "Ice", "Frost", "Cloud",
                 "Thunder", "Mist", "Dew"]

# Hand-authored index sequences: EXP107 base patterns remapped by the
# deterministic affine maps body: x -> (2*x + 5) mod 11 and
# weather: x -> (3*x + 5) mod 10.
BODY_TRIPLES = [
    (5, 7, 9),
    (7, 9, 0),
    (9, 0, 2),
    (5, 9, 2),
    (5, 7, 0),
    (7, 0, 2),
    (5, 9, 0),
    (7, 9, 2),
    (5, 0, 2),
    (5, 7, 2),
    (5, 7, 9),
    (7, 9, 0),
    (9, 0, 2),
    (5, 9, 2),
    (5, 7, 0),
]
BODY_QUADS = [
    (5, 7, 9, 0),
    (7, 9, 0, 2),
    (5, 7, 0, 2),
    (5, 9, 0, 2),
    (5, 7, 9, 2),
    (5, 7, 9, 0),
    (7, 9, 0, 2),
    (5, 7, 0, 2),
    (5, 9, 0, 2),
    (5, 7, 9, 2),
    (5, 7, 9, 0),
    (7, 9, 0, 2),
    (5, 7, 0, 2),
    (5, 9, 0, 2),
    (5, 7, 9, 2),
]
WEATHER_TRIPLES = [
    (5, 8, 1),
    (8, 1, 4),
    (1, 4, 7),
    (5, 1, 7),
    (5, 8, 4),
    (8, 4, 7),
    (5, 1, 4),
    (8, 1, 7),
    (5, 4, 7),
    (5, 8, 7),
    (5, 8, 1),
    (8, 1, 4),
    (1, 4, 7),
    (5, 1, 7),
    (5, 8, 4),
]
WEATHER_QUADS = [
    (5, 8, 1, 4),
    (8, 1, 4, 7),
    (5, 8, 4, 7),
    (5, 1, 4, 7),
    (5, 8, 1, 7),
    (5, 8, 1, 4),
    (8, 1, 4, 7),
    (5, 8, 4, 7),
    (5, 1, 4, 7),
    (5, 8, 1, 7),
    (5, 8, 1, 4),
    (8, 1, 4, 7),
    (5, 8, 4, 7),
    (5, 1, 4, 7),
    (5, 8, 1, 7),
]

# New verb families (meaning-preserving ranking pair).
FAM1 = "outshines"        # family-1: "{A} outshines {B}"  (A > B)
FAM2 = "is outshone by"   # family-2: "{B} is outshone by {A}"  (A > B)

# Prior-bench verb-family substrings: none may appear in any bench-4 premise.
PRIOR_FAMILY_SUBSTRINGS = (
    " outranks ", " is lower than ",      # bench 1 (EXP107)
    " surpasses ", " is below ",          # bench 2 (EXP120)
    " dominates ", " is dominated by ",   # bench 3 (EXP122)
)

# Prior-bench entity names for the disjointness assertion.
BENCH1_ENTITIES = {"Mars", "Venus", "Jupiter", "Saturn", "Mercury",
                   "Iron", "Gold", "Silver", "Bronze", "Steel"}

QUESTION_SUFFIX = " Question: Who is higher in rank? Answer:"
N_BENCH = 60


def _base_items():
    """The 60 bench-4 base item records (id, premise, phrasing, entities)."""
    items = []
    for vocab, triples, quads, dom, thr in (
            (VOCAB_BODY, BODY_TRIPLES, BODY_QUADS, 'body', 8),
            (VOCAB_WEATHER, WEATHER_TRIPLES, WEATHER_QUADS, 'weather', 7)):
        for i, (iA, iB, iC) in enumerate(triples):
            A, B, C = vocab[iA], vocab[iB], vocab[iC]
            a_first = i < thr
            premise = (f"Premise: {A} outshines {B}. {B} outshines {C}." if a_first
                       else f"Premise: {C} is outshone by {B}. {B} is outshone by {A}.")
            items.append({'id': f'exp125_{dom}_2hop_{i}', 'premise': premise,
                          'phrasing': 'A-first' if a_first else 'C-first',
                          'domain': dom, 'hop': 2,
                          'ents': (A, B, C), 'src_index': i})
        for i, (iA, iB, iC, iD) in enumerate(quads):
            A, B, C, D = vocab[iA], vocab[iB], vocab[iC], vocab[iD]
            a_first = i < thr
            premise = (f"Premise: {A} outshines {B}. {B} outshines {C}. {C} outshines {D}." if a_first
                       else f"Premise: {D} is outshone by {C}. {C} is outshone by {B}. {B} is outshone by {A}.")
            items.append({'id': f'exp125_{dom}_3hop_{i}', 'premise': premise,
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
        return (f"Premise: {B} is outshone by {A}. {C} is outshone by {B}." if a_first
                else f"Premise: {B} outshines {C}. {A} outshines {B}.")
    A, B, C, D = ents
    return (f"Premise: {B} is outshone by {A}. {C} is outshone by {B}. {D} is outshone by {C}." if a_first
            else f"Premise: {C} outshines {D}. {B} outshines {C}. {A} outshines {B}.")


def _word_family(premise):
    """Which verb family the premise uses (for cell-balance verification)."""
    if ' outshines ' in premise:
        assert ' is outshone by ' not in premise
        return 'outshines'
    assert ' is outshone by ' in premise
    return 'outshone'


def build_bench():
    """Build the 60-item bench-4. Deterministic; no RNG; no model calls."""
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
            'id': ('exp125_flip_' if flipped else 'exp125_ctrl_') + b['id'],
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


def _bench2_entities():
    ents = set()
    b2 = json.load(open('/home/hatch/workspace/SCBI/experiments/runs/'
                        'EXP120_lfhgen2/out/exp120_bench2_canonical.json'))
    for it in b2:
        ents.update(it['tuple'])
    return ents


def _bench3_entities():
    ents = set()
    b3 = json.load(open('/home/hatch/workspace/SCBI/experiments/runs/'
                        'EXP122_positioncue/out/exp122_bench3_canonical.json'))
    for it in b3:
        ents.update(it['tuple'])
    return ents


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
    # Disjointness: bench-4 entities touch no prior bench's entity set.
    bench4_ents = set(VOCAB_BODY) | set(VOCAB_WEATHER)
    overlap = (bench4_ents & BENCH1_ENTITIES) | (bench4_ents & _bench2_entities()) \
        | (bench4_ents & _bench3_entities())
    assert not overlap, f"entity reuse vs prior benches: {sorted(overlap)}"
    # Per-item checks.
    for b in bench:
        # All tuple entities are bench-4 entities.
        assert set(b['tuple']) <= bench4_ents, (b['id'], b['tuple'])
        fam = _word_family(b['premise'])
        a_first = (b['phrasing'] == 'A-first')
        expected = ('outshone' if a_first else 'outshines') if b['flipped'] \
            else ('outshines' if a_first else 'outshone')
        assert fam == expected, (b['id'], fam, expected)
        # Extraction contract: premise == state_text_of(prompt).
        assert b['prompt'].startswith('Premise:')
        assert b['premise'] == b['prompt'][:b['prompt'].index(' Question:')]
        # G-C3: prompt decomposes byte-exactly into premise + QUESTION_SUFFIX.
        assert b['prompt'] == b['premise'] + QUESTION_SUFFIX, b['id']
        # No prior-bench verb-family leakage.
        for s in PRIOR_FAMILY_SUBSTRINGS:
            assert s not in b['premise'], (b['id'], s)
        # Label pin (independent, whole-word): tuple[0] (the target) in the
        # first premise sentence iff A-first. ("Ear" is a substring of
        # "Heart", so the match is whole-word, not raw substring.)
        first_sent = b['premise'][len('Premise: '):].split('. ')[0]
        tgt = b['tuple'][0]
        padded = ' ' + first_sent + ' '
        assert ((' ' + tgt + ' ') in padded) == a_first, (b['id'], first_sent, tgt)
        # Label convention: y = 1 iff A-first.
        assert b['y'] == (1 if a_first else 0)
    ids = [b['id'] for b in bench]
    assert len(set(ids)) == N_BENCH
    assert not any(i.startswith('exp077_') for i in ids), "bench-1 ID collision"
    assert not any(i.startswith('exp107_') for i in ids), "bench-1 ID collision"
    assert not any(i.startswith('exp120_') for i in ids), "bench-2 ID collision"
    assert not any(i.startswith('exp122_') for i in ids), "bench-3 ID collision"
    assert not any(i.startswith('exp092_') for i in ids), "train/test ID collision"
    return {'n': len(bench), 'cells': dict(cells), 'pin': bench_sha256(bench)}


def gate_gc1(bench=None):
    """G-C1: pure-template detector gate. T predicts A-first iff the first
    premise sentence uses bench-4's family-1 ("outshines"). By the flip
    discipline T scores 30/60 by construction. Gate: T <= 36/60
    (not above chance at alpha=0.05 one-sided: P(X>=37|60,0.5) ~= 0.047).
    Diagnostic only."""
    bench = bench if bench is not None else build_bench()
    correct = 0
    for b in bench:
        first_sent = b['premise'][len('Premise: '):].split('. ')[0]
        pred_a_first = ' outshines ' in first_sent
        if pred_a_first == (b['phrasing'] == 'A-first'):
            correct += 1
    return {'score': correct, 'n': N_BENCH, 'pass': correct <= 36}


def _entity_index_seqs_b4():
    """Flattened vocabulary-index sequences, zero-padded to length 4, in
    canonical builder emission order (body triples, body quads, weather
    triples, weather quads)."""
    seqs = []
    for idxs in (BODY_TRIPLES, BODY_QUADS, WEATHER_TRIPLES, WEATHER_QUADS):
        for t in idxs:
            seqs.extend(list(t) + [0] * (4 - len(t)))
    return seqs


def gate_gc2():
    """G-C2: entity-rank correlation gate. |Pearson(r1, r2)| <= 0.10, where
    r1/r2 are the flattened entity-index sequences of bench 1 / bench 4 in
    canonical item order. Compares bench-4's construction against bench-1's
    builder records for this design check only; feeds no bench-1 labels or
    embeddings into the analysis (Law #13 fence). Diagnostic only."""
    import numpy as np
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "build_exp107_bench",
        "/home/hatch/workspace/SCBI/experiments/runs/EXP107_templatectrl/build_exp107_bench.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    def flat_b1(triples, quads):
        s = []
        for idxs in (triples, quads, triples, quads):
            for t in idxs:
                s.extend(list(t) + [0] * (4 - len(t)))
        return s

    r1 = np.asarray(flat_b1(mod.TRIPLES, mod.QUADS), dtype=float)
    r2 = np.asarray(_entity_index_seqs_b4(), dtype=float)
    assert len(r1) == len(r2) == 240
    r = float(np.corrcoef(r1, r2)[0, 1])
    return {'pearson': r, 'abs_pearson': abs(r), 'pass': abs(r) <= 0.10}


def gate_gc3(bench=None):
    """G-C3: template-decomposition pin. Byte-exact decomposition of every
    item (prompt == premise + QUESTION_SUFFIX) plus QUESTION_SUFFIX byte
    pin plus canonical-order deterministic construction. Full gate: any
    failure -> construction dies."""
    bench = bench if bench is not None else build_bench()
    ok_suffix = QUESTION_SUFFIX == " Question: Who is higher in rank? Answer:"
    ok_decomp = all(b['prompt'] == b['premise'] + QUESTION_SUFFIX for b in bench)
    ok_det = bench_sha256(build_bench()) == bench_sha256(build_bench())
    return {'suffix_byte_exact': ok_suffix, 'decomposition_60_of_60': ok_decomp,
            'deterministic': ok_det, 'pass': ok_suffix and ok_decomp and ok_det}


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
    g3 = gate_gc3(bench)
    print(f"G-C3 decomposition pin: pass={g3['pass']}")
    # Show one example per cell.
    seen = set()
    for b in bench:
        key = (b['phrasing'], 'flipped' if b['flipped'] else 'original')
        if key not in seen:
            seen.add(key)
            print(f"\n[{key[0]} / {key[1]}] {b['id']}\n  {b['premise']}")
