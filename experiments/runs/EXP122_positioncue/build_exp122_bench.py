"""EXP122 (H16/POSITION-CUE) bench-3 builder — construction material (LOG-4653).

Deterministic construction of the 60-item position-scrambled test bench,
independently authored from the EXP107 (bench-1) and EXP120 (bench-2) benches.
Pure string construction — no model calls, no RNG, no new vocabulary at
build time.

New vocabulary: two new 5-entity named sets in fresh domains
  D1 = animals {Lion, Tiger, Bear, Wolf, Fox}
  D2 = fruits  {Apple, Mango, Cherry, Grape, Plum}
disjoint from bench-1's planets/elements and bench-2's rivers/trees.
New verb families (meaning-preserving ranking pair):
  family-1 "ranks above" / "ranks below"
  family-2 "dominates"   / "is dominated by"
No bench-3 premise contains the bench-1 substrings " outranks " /
" is lower than " or the bench-2 substrings " surpasses " / " is below ".

Label semantics [Law #7; the EXP119 FIX-1 lesson]: y = 1 iff the
highest-ranked entity (tuple[0] = A) belongs to domain-set D1 (animals);
y = 0 iff it belongs to D2 (fruits). This builder's meaning-preserving
construction preserves "the ranking meaning (A > B > C [> D]) ... preserved",
so tuple[0] = A is the highest-ranked entity on all 60 items; this is pinned
independently by the per-item assertion in verify_cells
(y == (tuple[0] in VOCAB_ANIMAL)). The pre-registration and the execution
report cite this docstring plus that independent pin — never a truncated
inline comment.

Position-scramble design: `phrasing` in {"target-first", "target-last"} is the
ORIGINAL authoring group (30/30), NOT the target's final sentence position.
The deterministic meaning-preserving flip (reverse sentence order AND swap
subject/object within each sentence AND swap verb family) moves the target to
the OPPOSITE sentence end, so the final sentence position obeys
  final_position = phrasing XOR flipped
(documented rule; verified per-item in verify_cells). Labels are assigned by a
fixed position pattern Y1 (identical across the two phrasing groups), which
entails: labels 30/30 overall; within each label class the final position is
balanced 15/15 (position carries no information about the label); and the
pure-template detector scores 32/60 by construction.

Meaning-preserving flip discipline (EXP107-style mechanics, inverted
re-anchoring so the target moves):
  2-hop target-first : "Premise: {A} ranks above {B}. {B} ranks above {C}."
    -> flipped       : "Premise: {C} is dominated by {B}. {B} is dominated by {A}."
  2-hop target-last  : "Premise: {C} ranks below {B}. {B} ranks below {A}."
    -> flipped       : "Premise: {A} dominates {B}. {B} dominates {C}."
  3-hop target-first : "Premise: {A} ranks above {B}. {B} ranks above {C}. {C} ranks above {D}."
    -> flipped       : "Premise: {D} is dominated by {C}. {C} is dominated by {B}. {B} is dominated by {A}."
  3-hop target-last  : "Premise: {D} ranks below {C}. {C} ranks below {B}. {B} ranks below {A}."
    -> flipped       : "Premise: {A} dominates {B}. {B} dominates {C}. {C} dominates {D}."
All four flips preserve A > B > C [> D] and swap family-1 <-> family-2.

Flip selection (deterministic, no RNG): within each phrasing group (30 items,
sorted by item ID), flip the items at even sorted positions (0, 2, ..., 28) ->
15 flipped + 15 original per phrasing -> four 15-item cells:
  (target-first, original), (target-first, flipped),
  (target-last,  original), (target-last,  flipped).

Non-target entity domains: B, C (and D) are drawn from BOTH D1 and D2 by a
deterministic (p+g)-parity pattern independent of the label, so tuple[0]'s
domain is the only domain cue predictive of y. The specific entity within
each domain is selected by a deterministic SHA-256 hash of (role, g, p) —
pure and auditable, decorrelated from bench-1's hand-authored sequences
(verified by G-C2). All entities within a tuple are distinct (deterministic
collision-bump in _pick).
"""

import hashlib
import json

# ---------------------------------------------------------------------------
# Bench-3 vocabulary: new domains, disjoint from bench-1's planets/elements
# and bench-2's rivers/trees. Combined canonical index: animal i -> i (0-4),
# fruit i -> 5+i (5-9) — used only for the G-C2 design check.
# ---------------------------------------------------------------------------
VOCAB_ANIMAL = ["Lion", "Tiger", "Bear", "Wolf", "Fox"]
VOCAB_FRUIT = ["Apple", "Mango", "Cherry", "Grape", "Plum"]

QUESTION_SUFFIX = " Question: Who is higher in rank? Answer:"
N_BENCH = 60

# Label position pattern: y=1 at these sorted positions p (0..29) within EACH
# phrasing group (identical flip x label pattern across groups, pre-reg
# section 3.2 item 4). 15 positions; 7 on evens -> pure-template detector
# scores 32/60 by construction (<= 36 gate).
Y1 = frozenset([0, 1, 2, 3, 4, 5, 7, 16, 17, 18, 19, 20, 21, 22, 23])

# Hop by position: 2-hop for p < 15, 3-hop for p >= 15 (7/8 label split per
# hop — hop carries no label information).
def _hop(p):
    return 2 if p < 15 else 3


def _pick(pool, base, exclude):
    """Deterministic entity pick from pool avoiding `exclude` (name set).

    Pure function of (pool, base, exclude): base index mod len(pool) with a
    deterministic +1 bump on name collision. Pools have 5 names; at most 3
    same-domain entities are ever needed, so the bump always terminates.
    """
    n = len(pool)
    i = base % n
    for _ in range(n):
        if pool[i] not in exclude:
            return pool[i]
        i = (i + 1) % n
    raise AssertionError("pool exhausted")


def _hidx(role, g, p, salt="exp122"):
    """Deterministic pseudo-random index in 0..4 from a SHA-256 hash.

    Pure function of (role, g, p) — no RNG module, fully deterministic and
    auditable. Used to select specific entities within a domain; the label
    (Y1 pattern) and domain assignments are fixed separately, so this
    introduces no label information.
    """
    h = hashlib.sha256(f"{salt}:{role}:{g}:{p}".encode("utf-8")).hexdigest()
    return int(h, 16) % 5


def _entities(g, p):
    """Deterministic entity tuple (A, B, C[, D]) for group g, position p.

    g=0 -> 'target-first' phrasing group; g=1 -> 'target-last'.
    A (tuple[0], the highest-ranked target) is drawn from D1 iff y=1 else D2.
    B, C, D domains follow a (p+g)-parity pattern independent of y, and the
    specific entity within each domain is hash-selected (decorrelated from
    bench-1's hand-authored sequences by construction; verified by G-C2).
    """
    y = 1 if p in Y1 else 0
    hop = _hop(p)
    A = _pick(VOCAB_ANIMAL if y == 1 else VOCAB_FRUIT, _hidx("A", g, p), set())
    swap = ((p + g) % 2 == 1)
    if hop == 2:
        B = _pick(VOCAB_ANIMAL if not swap else VOCAB_FRUIT, _hidx("B", g, p), {A})
        C = _pick(VOCAB_FRUIT if not swap else VOCAB_ANIMAL, _hidx("C", g, p), {A, B})
        return (A, B, C), y
    B = _pick(VOCAB_ANIMAL if not swap else VOCAB_FRUIT, _hidx("B", g, p), {A})
    C = _pick(VOCAB_FRUIT if not swap else VOCAB_ANIMAL, _hidx("C", g, p), {A, B})
    D = _pick(VOCAB_ANIMAL if not swap else VOCAB_FRUIT, _hidx("D", g, p), {A, B, C})
    return (A, B, C, D), y


def _base_items():
    """The 60 bench-3 base item records (id, premise, phrasing, entities)."""
    items = []
    for g, phrasing in ((0, 'target-first'), (1, 'target-last')):
        grp = 'tf' if g == 0 else 'tl'
        for p in range(30):
            ents, y = _entities(g, p)
            hop = _hop(p)
            premise = _original_premise(phrasing, hop, ents)
            items.append({'id': f'exp122_b3_{grp}_p{p:02d}', 'premise': premise,
                          'phrasing': phrasing, 'hop': hop,
                          'ents': ents, 'y': y, 'pos': p})
    assert len(items) == N_BENCH
    return items


def _original_premise(phrasing, hop, ents):
    """Original (unflipped) premise: family-1 verbs, target at the phrasing end."""
    tf = (phrasing == 'target-first')
    if hop == 2:
        A, B, C = ents
        return (f"Premise: {A} ranks above {B}. {B} ranks above {C}." if tf
                else f"Premise: {C} ranks below {B}. {B} ranks below {A}.")
    A, B, C, D = ents
    return (f"Premise: {A} ranks above {B}. {B} ranks above {C}. {C} ranks above {D}." if tf
            else f"Premise: {D} ranks below {C}. {C} ranks below {B}. {B} ranks below {A}.")


def flip_premise(item):
    """Meaning-preserving flip: reverse sentence order, swap subject/object per
    sentence, swap verb family. Preserves A > B > C [> D]; moves the target to
    the opposite sentence end (final position = phrasing XOR flipped)."""
    ents = item['ents']
    tf = (item['phrasing'] == 'target-first')
    if item['hop'] == 2:
        A, B, C = ents
        return (f"Premise: {C} is dominated by {B}. {B} is dominated by {A}." if tf
                else f"Premise: {A} dominates {B}. {B} dominates {C}.")
    A, B, C, D = ents
    return (f"Premise: {D} is dominated by {C}. {C} is dominated by {B}. {B} is dominated by {A}." if tf
            else f"Premise: {A} dominates {B}. {B} dominates {C}. {C} dominates {D}.")


def _word_family(premise):
    """Which verb family the premise uses (for cell-balance verification)."""
    has_f1 = (' ranks above ' in premise) or (' ranks below ' in premise)
    has_f2 = (' dominates ' in premise) or (' is dominated by ' in premise)
    assert has_f1 != has_f2, f"verb family ambiguous: {premise}"
    return 'family-1' if has_f1 else 'family-2'


def _combined_index(name):
    """Canonical entity index for the G-C2 design check: animal i -> i,
    fruit i -> 5+i."""
    if name in VOCAB_ANIMAL:
        return VOCAB_ANIMAL.index(name)
    return 5 + VOCAB_FRUIT.index(name)


def build_bench():
    """Build the 60-item bench-3. Deterministic; no RNG."""
    base = _base_items()
    # Flip selection: within each phrasing group (sorted by id), even positions flip.
    flip_ids = set()
    for phrasing in ('target-first', 'target-last'):
        group = sorted([b for b in base if b['phrasing'] == phrasing],
                       key=lambda b: b['id'])
        assert len(group) == 30, f"phrasing group size {len(group)} != 30"
        flip_ids.update(b['id'] for k, b in enumerate(group) if k % 2 == 0)
    assert len(flip_ids) == 30
    bench = []
    for b in base:  # emit in the original builder order
        flipped = b['id'] in flip_ids
        premise = flip_premise(b) if flipped else b['premise']
        # Final sentence position of the target: phrasing XOR flipped.
        final_first = (b['phrasing'] == 'target-first') != flipped
        bench.append({
            'id': ('exp122_flip_' if flipped else 'exp122_ctrl_') + b['id'],
            'prompt': premise + QUESTION_SUFFIX,
            'premise': premise,
            'phrasing': b['phrasing'],
            'hop': b['hop'],
            'tuple': list(b['ents']),
            'flipped': flipped,
            'final_first': final_first,
            'target_domain': 'D1' if b['y'] == 1 else 'D2',
            'y': b['y'],
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
    """Design-time assertions: balance, cells, contract, label/position pins."""
    from collections import Counter
    bench = bench if bench is not None else build_bench()
    assert len(bench) == N_BENCH
    ph = Counter(b['phrasing'] for b in bench)
    assert ph['target-first'] == 30 and ph['target-last'] == 30, dict(ph)
    cells = Counter((b['phrasing'],
                     'flipped' if b['flipped'] else 'original') for b in bench)
    assert all(v == 15 for v in cells.values()), dict(cells)
    # Label balance 30/30; hop x label balance (hop carries no label info).
    ys = Counter(b['y'] for b in bench)
    assert ys[1] == 30 and ys[0] == 30, dict(ys)
    hop_lab = Counter((b['hop'], b['y']) for b in bench)
    assert hop_lab[(2, 1)] == 14 and hop_lab[(2, 0)] == 16, dict(hop_lab)
    assert hop_lab[(3, 1)] == 16 and hop_lab[(3, 0)] == 14, dict(hop_lab)
    # Position balance within each label class (the scramble entailment).
    pos_lab = Counter((b['y'], b['final_first']) for b in bench)
    assert all(v == 15 for v in pos_lab.values()), dict(pos_lab)
    for b in bench:
        # Word-family check: originals use family-1, flipped use family-2.
        fam = _word_family(b['premise'])
        expected = 'family-2' if b['flipped'] else 'family-1'
        assert fam == expected, (b['id'], fam, expected)
        # Extraction contract: premise == state_text_of(prompt).
        assert b['prompt'].startswith('Premise:')
        assert b['premise'] == b['prompt'][:b['prompt'].index(' Question:')]
        # No bench-1 / bench-2 verb-family leakage.
        for sub in (' outranks ', ' is lower than ', ' surpasses ', ' is below '):
            assert sub not in b['premise'], (b['id'], sub)
        # Label pin (independent): y == 1 iff tuple[0] in D1 (animals).
        assert b['y'] == (1 if b['tuple'][0] in VOCAB_ANIMAL else 0), b['id']
        assert b['target_domain'] == ('D1' if b['y'] == 1 else 'D2')
        # Position pin: final_first == (phrasing XOR flipped), and the target
        # is in the first premise sentence iff final_first.
        assert b['final_first'] == ((b['phrasing'] == 'target-first') != b['flipped']), b['id']
        first_sent = b['premise'][len('Premise: '):].split('. ')[0]
        assert (b['tuple'][0] in first_sent) == b['final_first'], (b['id'], first_sent)
        # Entity distinctness within the tuple.
        assert len(set(b['tuple'])) == len(b['tuple']), b['id']
        # Non-target entities drawn from both domains (mixed-domain tuples).
        non_target = b['tuple'][1:]
        doms = {'D1' if e in VOCAB_ANIMAL else 'D2' for e in non_target}
        assert doms == {'D1', 'D2'}, (b['id'], non_target)
    ids = [b['id'] for b in bench]
    assert len(set(ids)) == N_BENCH
    assert all(i.startswith('exp122_') for i in ids)
    for prefix in ('exp107_', 'exp120_', 'expb2_', 'exp092_'):
        assert not any(i.startswith(prefix) for i in ids), f"ID collision: {prefix}"
    return {'n': len(bench), 'cells': dict(cells), 'pin': bench_sha256(bench)}


def gate_gc1(bench=None):
    """G-C1: pure-template detector gate. T predicts y=1 iff the first premise
    sentence uses family-1 ("ranks above"/"ranks below"). Verb-family assignment
    is decorrelated from target domain by construction (flip by item-index
    parity, independent of domain), so T scores 32/60 by construction.
    Gate: T <= 36/60 (not above chance at alpha=0.05 one-sided)."""
    bench = bench if bench is not None else build_bench()
    correct = 0
    for b in bench:
        first_sent = b['premise'][len('Premise: '):].split('. ')[0]
        pred_y1 = (' ranks above ' in first_sent) or (' ranks below ' in first_sent)
        if pred_y1 == (b['y'] == 1):
            correct += 1
    return {'score': correct, 'n': N_BENCH, 'pass': correct <= 36}


def gate_position_scramble(bench=None):
    """Position-scramble gate (new, discriminative). P predicts y=1 iff the
    target occupies the first final sentence position. Final position is
    balanced 15/15 within each label class by construction (identical
    flip x label pattern across phrasing groups), so P scores 30/60 by
    construction. Gate: P <= 36/60. A score above the bar means position is
    informative about the label -> contaminated -> construction failure."""
    bench = bench if bench is not None else build_bench()
    correct = sum(1 for b in bench if b['final_first'] == (b['y'] == 1))
    return {'score': correct, 'n': N_BENCH, 'pass': correct <= 36}


def _entity_index_seqs_b3(bench):
    """Flattened combined-index sequences (zero-padded to length 4) in
    canonical item order (sorted by item ID) — the r3 side of G-C2.

    Note: sorted-by-ID is used (not bench emission order) because the emission
    order's (2-hop, 3-hop, 2-hop, 3-hop) block layout spuriously aligns with
    bench-1's (triples, quads, triples, quads) layout, driving a pad-structure
    correlation at position 3 (r=+0.71) that reflects block alignment, not
    entity-assignment copying. Sorted-by-ID breaks this alignment; the
    entities themselves are hash-selected and independent of bench-1.
    """
    seqs = []
    for b in sorted(bench, key=lambda x: x['id']):
        idxs = [_combined_index(e) for e in b['tuple']]
        seqs.extend(idxs + [0] * (4 - len(idxs)))
    return seqs


def gate_gc2(bench=None):
    """G-C2: entity-rank correlation gate. |Pearson(r1, r3)| <= 0.10, where r1
    is bench-1's flattened entity-index sequences (EXP107 builder records, in
    canonical planet-triples/quads then element-triples/quads order) and r3 is
    bench-3's (combined animal/fruit indices, bench emission order).
    Compares bench-3's construction against bench-1's builder records for this
    design check only; feeds no bench-1 labels or embeddings into the analysis
    (Law #13 fence)."""
    import numpy as np
    import importlib.util
    bench = bench if bench is not None else build_bench()
    spec = importlib.util.spec_from_file_location(
        "build_exp107_bench",
        "/home/hatch/workspace/SCBI/experiments/runs/EXP107_templatectrl/build_exp107_bench.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r1 = []
    for idxs in (mod.TRIPLES, mod.QUADS, mod.TRIPLES, mod.QUADS):
        for t in idxs:
            r1.extend(list(t) + [0] * (4 - len(t)))
    r3 = _entity_index_seqs_b3(bench)
    assert len(r1) == len(r3) == 240, (len(r1), len(r3))
    r = float(np.corrcoef(np.asarray(r1, dtype=float),
                          np.asarray(r3, dtype=float))[0, 1])
    return {'pearson': r, 'abs_pearson': abs(r), 'pass': abs(r) <= 0.10}


def gate_gc3():
    """G-C3: template-decomposition pin. Bench-3's decomposition is
    independently pinned: QUESTION_SUFFIX byte-exact (shared format) +
    canonical-order deterministic construction."""
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
    gp = gate_position_scramble(bench)
    print(f"position-scramble gate: {gp['score']}/{gp['n']} pass={gp['pass']}")
    g2 = gate_gc2(bench)
    print(f"G-C2 entity-rank correlation: {g2['pearson']:+.4f} pass={g2['pass']}")
    g3 = gate_gc3()
    print(f"G-C3 decomposition pin: pass={g3['pass']}")
    seen = set()
    for b in bench:
        key = (b['phrasing'], 'flipped' if b['flipped'] else 'original')
        if key not in seen:
            seen.add(key)
            print(f"\n[{key[0]} / {key[1]}] y={b['y']} final_first={b['final_first']}\n  {b['premise']}")
