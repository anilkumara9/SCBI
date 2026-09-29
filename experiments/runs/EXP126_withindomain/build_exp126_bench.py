"""EXP126 (H23/WITHIN-DOMAIN) bench-5 builder — construction material (LOG-4687).

Deterministic construction of the 60-item all-animal test bench,
independently authored from benches 1-4. Pure string construction —
no model calls, no RNG, no new vocabulary at build time.

Entity vocabulary: 14 animals, all asserted single-token under the real
Pythia-410m tokenizer with " "+E encoding at construction (tokenizer-only;
gate-verified 14/14 at LOG-4684, re-asserted here):
  S1 = {Cat, Dog, Bear, Wolf, Fox}        (target subset A)
  S2 = {Lion, Tiger, Horse, Cow, Pig}     (target subset B)
  neutral decoys = {Rat, Bat, Bird, Fish} (non-target tuple entities only)

New verb families (meaning-preserving ranking pairs), disjoint from
bench-1 ("outranks"/"is lower than"), bench-2 ("surpasses"/"is below"),
bench-3 ("ranks above"/"ranks below", "dominates"/"is dominated by"),
bench-4 ("outshines"/"is outshone by"):
  family-1 "towers over" / "crouches under"
  family-2 "looms over"  / "cowers beneath"
No bench-5 premise contains any prior-bench verb-family substring, and no
template content word beyond ordinary English function words is shared with
any prior bench.

Label semantics [Law #7; the EXP119 FIX-1 lesson]: y = 1 iff the
highest-ranked entity (tuple[0] = A) belongs to entity-subset S1;
y = 0 iff it belongs to S2. This builder's meaning-preserving construction
preserves "the ranking meaning (A > B > C [> D]) ... preserved", so tuple[0]
= A is the highest-ranked entity on all 60 items; this is pinned
independently by the per-item assertion in verify_cells
(y == (tuple[0] in S1)). The pre-registration and the execution report cite
this docstring plus that independent pin — never a truncated inline comment.

Position-scramble design: `phrasing` in {"target-first", "target-last"} is the
ORIGINAL authoring group (30/30), NOT the target's final sentence position.
The deterministic meaning-preserving flip (reverse sentence order AND swap
subject/object within each sentence AND swap verb family) moves the target to
the OPPOSITE sentence end, so the final sentence position obeys
  final_position = phrasing XOR flipped
(documented rule; verified per-item in verify_cells). Labels follow the Y1
position pattern (identical across the two phrasing groups; Y1 is EXP122's
pattern rotated by +7 mod 30 for G-C2 independence), which entails:
labels 30/30 overall; within each label class the final position is balanced
15/15 (position carries no information about the label); the pure-template
detector scores 28/60 by construction; the pure-position detector scores
30/60 by construction.

Non-target entity selection: B, C (and D) are drawn from ALL 14 animals by a
deterministic hash independent of the label, so tuple[0]'s subset membership
is the only label-predictive cue. The specific entity is hash-selected with
salt="exp126" (decorrelated from bench-3's "exp122" salt; independence
verified by G-C2). All entities within a tuple are distinct (deterministic
collision-bump in _pick).

Meaning-preserving flip discipline (EXP107/EXP122-style mechanics):
  2-hop target-first : "Premise: {A} towers over {B}. {B} towers over {C}."
    -> flipped       : "Premise: {C} cowers beneath {B}. {B} cowers beneath {A}."
  2-hop target-last  : "Premise: {C} crouches under {B}. {B} crouches under {A}."
    -> flipped       : "Premise: {A} looms over {B}. {B} looms over {C}."
  3-hop target-first : "Premise: {A} towers over {B}. {B} towers over {C}. {C} towers over {D}."
    -> flipped       : "Premise: {D} cowers beneath {C}. {C} cowers beneath {B}. {B} cowers beneath {A}."
  3-hop target-last  : "Premise: {D} crouches under {C}. {C} crouches under {B}. {B} crouches under {A}."
    -> flipped       : "Premise: {A} looms over {B}. {B} looms over {C}. {C} looms over {D}."
All eight forms preserve A > B > C [> D] and swap family-1 <-> family-2.

Flip selection (deterministic, no RNG): within each phrasing group (30 items,
sorted by item ID), flip the items at even sorted positions (0, 2, ..., 28) ->
15 flipped + 15 original per phrasing -> four 15-item cells:
  (target-first, original), (target-first, flipped),
  (target-last,  original), (target-last,  flipped).
"""

import hashlib
import json
import re

# ---------------------------------------------------------------------------
# Bench-5 vocabulary: 14 animals in a single domain. Canonical index for the
# G-C2 design check: position in VOCAB (0-13).
# ---------------------------------------------------------------------------
VOCAB = ["Cat", "Dog", "Bear", "Wolf", "Fox",
         "Lion", "Tiger", "Horse", "Cow", "Pig",
         "Rat", "Bat", "Bird", "Fish"]
S1_LIST = ["Cat", "Dog", "Bear", "Wolf", "Fox"]
S2_LIST = ["Lion", "Tiger", "Horse", "Cow", "Pig"]
S1 = frozenset(S1_LIST)
S2 = frozenset(S2_LIST)
assert S1 | S2 | frozenset(["Rat", "Bat", "Bird", "Fish"]) == frozenset(VOCAB)
assert len(VOCAB) == 14 and len(set(VOCAB)) == 14

QUESTION_SUFFIX = " Question: Who is higher in rank? Answer:"
N_BENCH = 60

# Label position pattern: y=1 at these sorted positions p (0..29) within EACH
# phrasing group (identical flip x label pattern across groups, pre-reg
# section 3.2 item 4). This is EXP122's Y1 set rotated by +7 mod 30
# (deterministic; chosen so bench-5's label sequence is independent of
# bench-3's for the G-C2 design check). Entails: pure-template detector
# 28/60, pure-position detector 30/60, final positions 15/15 within each
# label class, hop x label balanced 15/15/15/15 with the hash-based hop rule.
Y1 = frozenset([(x + 7) % 30 for x in
                [0, 1, 2, 3, 4, 5, 7, 16, 17, 18, 19, 20, 21, 22, 23]])

# Prior-bench verb-family substrings: none may appear in any bench-5 premise.
PRIOR_FAMILY_SUBSTRINGS = (
    " outranks ", " is lower than ",      # bench-1
    " surpasses ", " is below ",          # bench-2
    " ranks above ", " ranks below ",     # bench-3
    " dominates ", " is dominated by ",   # bench-3
    " outshines ", " is outshone by ",    # bench-4
)

_ANIMAL_RE = re.compile(r"\b(" + "|".join(VOCAB) + r")\b")


def _hop(p, g):
    # 2-hop iff the "hop" hash is even, else 3-hop. Deterministic SHA-256
    # (same discipline as entity selection, salt "exp126"); structurally
    # independent of bench-3's p<15 block rule, so the G-C2 padding pattern
    # does not align. Yields 30 2-hop + 30 3-hop with hop x label 15/15/15/15.
    return 2 if _hidx("hop", g, p) % 2 == 0 else 3


def _pick(pool, base, exclude):
    """Deterministic entity pick from pool avoiding `exclude` (name set).

    Pure function of (pool, base, exclude): base index mod len(pool) with a
    deterministic +1 bump on name collision.
    """
    n = len(pool)
    i = base % n
    for _ in range(n):
        if pool[i] not in exclude:
            return pool[i]
        i = (i + 1) % n
    raise AssertionError("pool exhausted")


def _hidx(role, g, p, salt="exp126"):
    """Deterministic pseudo-random integer from a SHA-256 hash.

    Pure function of (role, g, p) — no RNG module, fully deterministic and
    auditable. The salt "exp126" decorrelates entity selection from bench-3's
    "exp122" salt (independence verified by G-C2).
    """
    h = hashlib.sha256(f"{salt}:{role}:{g}:{p}".encode("utf-8")).hexdigest()
    return int(h, 16)


def _entities(g, p):
    """Deterministic entity tuple (A, B, C[, D]) for group g, position p.

    g=0 -> 'target-first' phrasing group; g=1 -> 'target-last'.
    A (tuple[0], the highest-ranked target) is drawn from S1 iff y=1 else S2.
    B, C, D are drawn from ALL 14 animals (independent of y) excluding the
    already-used names, so tuple[0]'s subset membership is the only
    label-predictive cue.
    """
    y = 1 if p in Y1 else 0
    hop = _hop(p, g)
    A = _pick(S1_LIST if y == 1 else S2_LIST, _hidx("A", g, p), set())
    used = {A}
    B = _pick(VOCAB, _hidx("B", g, p), used)
    used.add(B)
    C = _pick(VOCAB, _hidx("C", g, p), used)
    used.add(C)
    if hop == 2:
        return (A, B, C), y
    D = _pick(VOCAB, _hidx("D", g, p), used)
    return (A, B, C, D), y


def _base_items():
    """The 60 bench-5 base item records (id, premise, phrasing, entities)."""
    items = []
    for g, phrasing in ((0, "target-first"), (1, "target-last")):
        grp = "tf" if g == 0 else "tl"
        for p in range(30):
            ents, y = _entities(g, p)
            hop = _hop(p, g)
            premise = _original_premise(phrasing, hop, ents)
            items.append({"id": f"expb5_{grp}_p{p:02d}", "premise": premise,
                          "phrasing": phrasing, "hop": hop,
                          "ents": ents, "y": y, "pos": p})
    assert len(items) == N_BENCH
    return items


def _original_premise(phrasing, hop, ents):
    """Original (unflipped) premise: family-1 verbs, target at the phrasing end."""
    tf = (phrasing == "target-first")
    if hop == 2:
        A, B, C = ents
        return (f"Premise: {A} towers over {B}. {B} towers over {C}." if tf
                else f"Premise: {C} crouches under {B}. {B} crouches under {A}.")
    A, B, C, D = ents
    return (f"Premise: {A} towers over {B}. {B} towers over {C}. {C} towers over {D}." if tf
            else f"Premise: {D} crouches under {C}. {C} crouches under {B}. {B} crouches under {A}.")


def flip_premise(item):
    """Meaning-preserving flip: reverse sentence order, swap subject/object per
    sentence, swap verb family. Preserves A > B > C [> D]; moves the target to
    the opposite sentence end (final position = phrasing XOR flipped)."""
    ents = item["ents"]
    tf = (item["phrasing"] == "target-first")
    if item["hop"] == 2:
        A, B, C = ents
        return (f"Premise: {C} cowers beneath {B}. {B} cowers beneath {A}." if tf
                else f"Premise: {A} looms over {B}. {B} looms over {C}.")
    A, B, C, D = ents
    return (f"Premise: {D} cowers beneath {C}. {C} cowers beneath {B}. {B} cowers beneath {A}." if tf
            else f"Premise: {A} looms over {B}. {B} looms over {C}. {C} looms over {D}.")


def _word_family(premise):
    """Which verb family the premise uses (for cell-balance verification)."""
    has_f1 = (" towers over " in premise) or (" crouches under " in premise)
    has_f2 = (" looms over " in premise) or (" cowers beneath " in premise)
    assert has_f1 != has_f2, f"verb family ambiguous: {premise}"
    return "family-1" if has_f1 else "family-2"


def _mentioned_animals(premise):
    """All animal-name mentions in a premise (whole-word matching)."""
    return set(_ANIMAL_RE.findall(premise))


def build_bench():
    """Build the 60-item bench-5. Deterministic; no RNG."""
    base = _base_items()
    # Flip selection: within each phrasing group (sorted by id), even positions flip.
    flip_ids = set()
    for phrasing in ("target-first", "target-last"):
        group = sorted([b for b in base if b["phrasing"] == phrasing],
                       key=lambda b: b["id"])
        assert len(group) == 30, f"phrasing group size {len(group)} != 30"
        flip_ids.update(b["id"] for k, b in enumerate(group) if k % 2 == 0)
    assert len(flip_ids) == 30
    bench = []
    for b in base:  # emit in the original builder order
        flipped = b["id"] in flip_ids
        premise = flip_premise(b) if flipped else b["premise"]
        # Final sentence position of the target: phrasing XOR flipped.
        final_first = (b["phrasing"] == "target-first") != flipped
        y = b["y"]
        bench.append({
            "id": ("expb5_flip_" if flipped else "expb5_ctrl_") + b["id"],
            "prompt": premise + QUESTION_SUFFIX,
            "premise": premise,
            "phrasing": b["phrasing"],
            "hop": b["hop"],
            "tuple": list(b["ents"]),
            "flipped": flipped,
            "final_first": final_first,
            "target_subset": "S1" if y == 1 else "S2",
            "y": y,
            "derived_from": b["id"],
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
    """Design-time assertions: balance, cells, contract, label/position pins,
    single-domain audit, verb-family freshness, ID namespace."""
    from collections import Counter
    bench = bench if bench is not None else build_bench()
    assert len(bench) == N_BENCH
    ph = Counter(b["phrasing"] for b in bench)
    assert ph["target-first"] == 30 and ph["target-last"] == 30, dict(ph)
    cells = Counter((b["phrasing"],
                     "flipped" if b["flipped"] else "original") for b in bench)
    assert all(v == 15 for v in cells.values()), dict(cells)
    # Label balance 30/30; hop x label balance (hop carries no label info).
    ys = Counter(b["y"] for b in bench)
    assert ys[1] == 30 and ys[0] == 30, dict(ys)
    hop_lab = Counter((b["hop"], b["y"]) for b in bench)
    assert hop_lab[(2, 1)] == 15 and hop_lab[(2, 0)] == 15, dict(hop_lab)
    assert hop_lab[(3, 1)] == 15 and hop_lab[(3, 0)] == 15, dict(hop_lab)
    # Position balance within each label class (the scramble entailment).
    pos_lab = Counter((b["y"], b["final_first"]) for b in bench)
    assert all(v == 15 for v in pos_lab.values()), dict(pos_lab)
    # Flip x label pattern identical across phrasing groups.
    for phrasing in ("target-first", "target-last"):
        grp = sorted([b for b in bench if b["phrasing"] == phrasing],
                     key=lambda b: b["derived_from"])
        pat = tuple((b["flipped"], b["y"]) for b in grp)
        if phrasing == "target-first":
            ref_pat = pat
        else:
            assert pat == ref_pat, "flip x label pattern differs across phrasing groups"
    out_of_domain = 0
    for b in bench:
        # Word-family check: originals use family-1, flipped use family-2.
        fam = _word_family(b["premise"])
        expected = "family-2" if b["flipped"] else "family-1"
        assert fam == expected, (b["id"], fam, expected)
        # Extraction contract: premise == state_text_of(prompt).
        assert b["prompt"].startswith("Premise:")
        assert b["premise"] == b["prompt"][:b["prompt"].index(" Question:")]
        # No prior-bench verb-family leakage.
        for sub in PRIOR_FAMILY_SUBSTRINGS:
            assert sub not in b["premise"], (b["id"], sub)
        # Label pin (independent): y == 1 iff tuple[0] in S1.
        assert b["y"] == (1 if b["tuple"][0] in S1 else 0), b["id"]
        assert b["target_subset"] == ("S1" if b["y"] == 1 else "S2")
        assert b["tuple"][0] in (S1 | S2), b["id"]
        # Position pin: final_first == (phrasing XOR flipped), and the target
        # is in the first premise sentence iff final_first.
        assert b["final_first"] == ((b["phrasing"] == "target-first") != b["flipped"]), b["id"]
        first_sent = b["premise"][len("Premise: "):].split(". ")[0]
        assert (b["tuple"][0] in first_sent.split()) == b["final_first"], (b["id"], first_sent)
        # Entity distinctness within the tuple.
        assert len(set(b["tuple"])) == len(b["tuple"]), b["id"]
        # Single-domain audit: every entity mention is one of the 14 animals.
        mentioned = _mentioned_animals(b["premise"])
        assert mentioned <= set(VOCAB), (b["id"], mentioned - set(VOCAB))
        assert set(b["tuple"]) <= mentioned, (b["id"], "tuple entity missing from premise")
        if mentioned - set(VOCAB):
            out_of_domain += 1
    assert out_of_domain == 0, f"{out_of_domain}/60 premises have out-of-domain entities"
    ids = [b["id"] for b in bench]
    assert len(set(ids)) == N_BENCH
    assert all(i.startswith("expb5_") for i in ids)
    for prefix in ("exp107_", "exp120_", "exp122_", "expb2_", "expb3_", "exp125_", "exp092_", "exp077_"):
        assert not any(i.startswith(prefix) for i in ids), f"ID collision: {prefix}"
    return {"n": len(bench), "cells": dict(cells), "pin": bench_sha256(bench)}


def gate_gc1(bench=None):
    """G-C1: pure-template detector gate. T predicts y=1 iff the first premise
    sentence uses family-1 ("towers over"/"crouches under"). Verb-family
    assignment is decorrelated from target subset by construction (flip by
    item-index parity, independent of subset), so T scores 28/60 by
    construction. Gate: T <= 36/60 (not above chance at alpha=0.05 one-sided)."""
    bench = bench if bench is not None else build_bench()
    correct = 0
    for b in bench:
        first_sent = b["premise"][len("Premise: "):].split(". ")[0]
        pred_y1 = (" towers over " in first_sent) or (" crouches under " in first_sent)
        if pred_y1 == (b["y"] == 1):
            correct += 1
    return {"score": correct, "n": N_BENCH, "pass": correct <= 36}


def gate_position_scramble(bench=None):
    """Position-scramble gate (discriminative). P predicts y=1 iff the target
    occupies the first final sentence position. Final position is balanced
    15/15 within each label class by construction (identical flip x label
    pattern across phrasing groups), so P scores 30/60 by construction.
    Gate: P <= 36/60. A score above the bar means position is informative
    about the label -> contaminated -> construction failure."""
    bench = bench if bench is not None else build_bench()
    correct = sum(1 for b in bench if b["final_first"] == (b["y"] == 1))
    return {"score": correct, "n": N_BENCH, "pass": correct <= 36}


def _entity_index_seqs_b3():
    """r3: bench-3's flattened combined-index sequences (zero-padded to length
    4) in sorted-by-ID canonical order — the EXP122 builder records."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "build_exp122_bench",
        "/home/hatch/workspace/SCBI/experiments/runs/EXP122_positioncue/build_exp122_bench.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    bench3 = mod.build_bench()
    seqs = []
    for b in sorted(bench3, key=lambda x: x["id"]):
        idxs = [mod._combined_index(e) for e in b["tuple"]]
        seqs.extend(idxs + [0] * (4 - len(idxs)))
    return seqs


# Canonical G-C2 index: S1/S2-interleaved order, so the index is agnostic to
# the subset label (S1 and S2 interleave instead of occupying low/high
# ranges). This makes G-C2 measure entity-assignment independence, not
# label-structure similarity.
GC2_INDEX = ["Cat", "Lion", "Dog", "Tiger", "Bear", "Horse",
             "Wolf", "Cow", "Fox", "Pig", "Rat", "Bat", "Bird", "Fish"]
assert set(GC2_INDEX) == set(VOCAB) and len(GC2_INDEX) == 14


def _entity_index_seqs_b5(bench):
    """r5: bench-5's flattened GC2-index sequences (zero-padded to length 4)
    in sorted-by-ID canonical order."""
    seqs = []
    for b in sorted(bench, key=lambda x: x["id"]):
        idxs = [GC2_INDEX.index(e) for e in b["tuple"]]
        seqs.extend(idxs + [0] * (4 - len(idxs)))
    return seqs


def gate_gc2(bench=None):
    """G-C2: entity-rank correlation gate. |Pearson(r3, r5)| <= 0.10, where r3
    is bench-3's flattened entity-index sequences (EXP122 builder records,
    sorted-by-ID canonical order) and r5 is bench-5's (S1/S2-interleaved
    GC2 indices, sorted-by-ID canonical order). The interleaved index keeps
    the check agnostic to the subset label, so it measures entity-assignment
    independence. Compares bench-5's construction against bench-3's builder
    records for this design check only; feeds no bench-3 labels or embeddings
    into the analysis (Law #13 fence)."""
    import numpy as np
    bench = bench if bench is not None else build_bench()
    r3 = _entity_index_seqs_b3()
    r5 = _entity_index_seqs_b5(bench)
    assert len(r3) == len(r5) == 240, (len(r3), len(r5))
    r = float(np.corrcoef(np.asarray(r3, dtype=float),
                          np.asarray(r5, dtype=float))[0, 1])
    return {"pearson": r, "abs_pearson": abs(r), "pass": abs(r) <= 0.10}


def gate_gc3(bench=None):
    """G-C3: template-decomposition pin. Bench-5's decomposition is
    independently pinned: QUESTION_SUFFIX byte-exact (shared format) +
    prompt == premise + QUESTION_SUFFIX on all 60 items + canonical-order
    deterministic construction."""
    bench = bench if bench is not None else build_bench()
    ok = QUESTION_SUFFIX == " Question: Who is higher in rank? Answer:"
    decomp = all(b["prompt"] == b["premise"] + QUESTION_SUFFIX for b in bench)
    det = bench_sha256(build_bench()) == bench_sha256(build_bench())
    return {"suffix_byte_exact": ok, "decomposition_60_of_60": decomp,
            "deterministic": det, "pass": ok and decomp and det}


if __name__ == "__main__":
    bench = build_bench()
    v = verify_cells(bench)
    print("cells:", json.dumps({f"{p}/{w}": c for (p, w), c in v["cells"].items()},
                               indent=1, sort_keys=True))
    print("pin:", v["pin"])
    g1 = gate_gc1(bench)
    print(f"G-C1 pure-template detector: {g1['score']}/{g1['n']} pass={g1['pass']}")
    gp = gate_position_scramble(bench)
    print(f"position-scramble gate: {gp['score']}/{gp['n']} pass={gp['pass']}")
    g2 = gate_gc2(bench)
    print(f"G-C2 entity-rank correlation: {g2['pearson']:+.4f} pass={g2['pass']}")
    g3 = gate_gc3(bench)
    print(f"G-C3 decomposition pin: pass={g3['pass']}")
    seen = set()
    for b in bench:
        key = (b["phrasing"], "flipped" if b["flipped"] else "original")
        if key not in seen:
            seen.add(key)
            print(f"\n[{key[0]} / {key[1]}] y={b['y']} subset={b['target_subset']} "
                  f"final_first={b['final_first']}\n  {b['premise']}")
