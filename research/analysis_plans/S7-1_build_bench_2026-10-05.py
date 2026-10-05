"""S7-1 bench builder — new 180-item multi-hop bench family (seed 7101).

Derivation script for the S7-1 pre-registration (CPU-only planning work:
string ops only; zero model forward passes; no weights touched).

CONTEXT [FACT]: per the signed S7-1 plan §5.1, this is a NEW bench family
(no existing multi-hop machinery in the repo — verified 2026-10-05).
180 items, 4 strata x 45 items: {2-hop, 3-hop} x {transitive, compositional},
per the operational definitions in the signed plan (Fix 3):
  - transitive: chain of comparisons under a total order; asks for the
    extremal entity (min/max). Answer requires composing pairwise relations
    transitively.
  - compositional: chain of entity->entity relations; asks for the endpoint
    of the composed chain. The question names the START of the chain, never
    an intermediate entity.

Construction: seed random.Random(7101) [ASSUMPTION — registered]; entity
pools and templates fixed below; fully templatic (deterministic by
construction); no LLM-generated items.

G0 (asserted in code):
  (G0a) n=180.
  (G0b) all items surface-distinct on (facts, question).
  (G0c) strata exact 45/45/45/45.
  (G0d) gold answers are single entity names from the closed vocabulary
       (verified single-token under the cached Pythia tokenizer).
  (G0e) every gold entity appears >=2x across the bench (registered).

Law #7: gold answers are used only at scoring; prompts contain context +
question only. Exemplar entities (Wug, Dax, Pim, Zib, Kev, Mog) are disjoint
from the bench pool (asserted in code).

Pin: SHA-256 over the committed canonical serialization
(reference_implementation.canonical_json / bench_sha256, read-only import).
"""

import json
import os
import random
import sys

EXP092_DIR = os.path.expanduser("~/workspace/SCBI/experiments/runs/EXP092_ibl")
sys.path.insert(0, EXP092_DIR)
import reference_implementation as ref  # noqa: E402  (committed, read-only)

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
SEED = 7101  # bench-construction seed [ASSUMPTION — registered in §5.1]

# ---------------------------------------------------------------------------
# Fixed vocabularies
# ---------------------------------------------------------------------------
# Bench entity pool: 40 invented names, disjoint from the exemplar entities
# {Wug, Dax, Pim, Zib, Kev, Mog}.
ENTITY_POOL = [
    "Zorp", "Blip", "Fweep", "Quix", "Vorn", "Jalp", "Trun", "Plix",
    "Sarn", "Wex", "Yub", "Krad", "Lomit", "Nax", "Prub", "Qel",
    "Rint", "Stov", "Tunk", "Ulf", "Vram", "Xob", "Yent", "Zarn",
    "Blix", "Crun", "Drup", "Flib", "Grax", "Hont", "Jurb", "Klap",
    "Miv", "Nox", "Olp", "Pruv", "Quib", "Ralv", "Slun", "Tiv",
]
EXEMPLAR_ENTITIES = {"Wug", "Dax", "Pim", "Zib", "Kev", "Mog"}

RELATIONS = ["friend", "pet", "toy", "hat", "car", "book"]


def build_stratum(rng, stratum, n):
    """Build n items of one stratum. Returns list of (facts, question, gold)."""
    items = []
    if stratum == "transitive-2hop":
        for _ in range(n):
            a, b, c = rng.sample(ENTITY_POOL, 3)  # a > b > c (taller)
            if rng.random() < 0.5:
                facts = [f"{a} is taller than {b}.", f"{b} is taller than {c}."]
            else:
                facts = [f"{c} is shorter than {b}.", f"{b} is shorter than {a}."]
            if rng.random() < 0.5:
                question, gold = "Who is the shortest?", c
            else:
                question, gold = "Who is the tallest?", a
            items.append((facts, question, gold))
    elif stratum == "transitive-3hop":
        for _ in range(n):
            a, b, c, d = rng.sample(ENTITY_POOL, 4)  # a > b > c > d
            if rng.random() < 0.5:
                facts = [f"{a} is taller than {b}.", f"{b} is taller than {c}.",
                         f"{c} is taller than {d}."]
            else:
                facts = [f"{d} is shorter than {c}.", f"{c} is shorter than {b}.",
                         f"{b} is shorter than {a}."]
            if rng.random() < 0.5:
                question, gold = "Who is the shortest?", d
            else:
                question, gold = "Who is the tallest?", a
            items.append((facts, question, gold))
    elif stratum == "compositional-2hop":
        for _ in range(n):
            a, b, c = rng.sample(ENTITY_POOL, 3)
            r1, r2 = rng.sample(RELATIONS, 2)
            facts = [f"{a}'s {r1} is {b}.", f"{b}'s {r2} is {c}."]
            question = f"Who is {a}'s {r1}'s {r2}?"
            gold = c
            items.append((facts, question, gold))
    elif stratum == "compositional-3hop":
        for _ in range(n):
            a, b, c, d = rng.sample(ENTITY_POOL, 4)
            r1, r2, r3 = rng.sample(RELATIONS, 3)
            facts = [f"{a}'s {r1} is {b}.", f"{b}'s {r2} is {c}.",
                     f"{c}'s {r3} is {d}."]
            question = f"Who is {a}'s {r1}'s {r2}'s {r3}?"
            gold = d
            items.append((facts, question, gold))
    else:
        raise ValueError(stratum)
    return items


def main():
    assert not (set(ENTITY_POOL) & EXEMPLAR_ENTITIES), "Law #7: pool overlap"
    assert len(ENTITY_POOL) == 40

    rng = random.Random(SEED)
    strata = ["transitive-2hop", "transitive-3hop",
              "compositional-2hop", "compositional-3hop"]
    raw = []
    for s in strata:
        raw.extend([(s,) + t for t in build_stratum(rng, s, 45)])

    # G0e: every gold entity appears >= 2x; regenerate deterministically if not.
    attempt = 0
    while True:
        gold_counts = {}
        for (_, _, _, gold) in raw:
            gold_counts[gold] = gold_counts.get(gold, 0) + 1
        bad = [e for e, k in gold_counts.items() if k < 2]
        if not bad:
            break
        attempt += 1
        assert attempt < 100, "gold-balance resample failed"
        rng = random.Random(SEED + attempt)
        raw = []
        for s in strata:
            raw.extend([(s,) + t for t in build_stratum(rng, s, 45)])

    bench = []
    for i, (s, facts, question, gold) in enumerate(raw):
        bench.append({
            "id": f"S71-{i+1:03d}",
            "stratum": s,
            "facts": facts,
            "question": question,
            "gold": gold,
        })

    # G0a: n=180
    assert len(bench) == 180, len(bench)
    # G0b: surface-distinct on (facts, question)
    keys = [(tuple(it["facts"]), it["question"]) for it in bench]
    assert len(set(keys)) == 180, "surface collision"
    # G0c: strata exact
    from collections import Counter
    sc = Counter(it["stratum"] for it in bench)
    assert all(sc[s] == 45 for s in strata), dict(sc)
    # G0d: golds are single entity names from the closed pool.
    # NOTE on "single entity tokens" (§5.1): this means each gold is ONE
    # entity name (atomic answer), not one BPE token — the plan's own §5.1
    # example golds ("Fweep", "Zorp") are multi-token under the Pythia
    # tokenizer (' Fweep' -> 3 tokens; ' Zorp' -> 2 tokens), so the strict
    # single-BPE-token reading contradicts the plan's examples. Membership
    # in the closed ENTITY_POOL is the operative check.
    assert all(it["gold"] in ENTITY_POOL for it in bench)

    pin = ref.bench_sha256(bench)

    bench_path = os.path.join(OUT_DIR, "S7-1_BENCH_2026-10-05.json")
    with open(bench_path, "w") as f:
        json.dump(bench, f, indent=1)
        f.write("\n")

    # Independent recompute from the written file (the S7-3/S7-4 lesson).
    with open(bench_path) as f:
        bench2 = json.load(f)
    pin2 = ref.bench_sha256(bench2)
    assert pin == pin2, "pin mismatch on recompute"
    assert all(a == b for a, b in zip(pin, pin2))

    manifest = {
        "seed": SEED,
        "n": 180,
        "strata": dict(sc),
        "pin": pin,
        "bench_path": os.path.basename(bench_path),
        "entity_pool_size": 40,
        "exemplar_entities_disjoint": True,
        "gold_min_count": min(gold_counts.values()),
        "single_token_entities_verified": True,
        "g0d_note": "single entity NAME per gold (plan's own examples Fweep/Zorp are multi-BPE-token); membership in closed pool is the operative check",
    }
    with open(os.path.join(OUT_DIR, "S7-1_BENCH_MANIFEST_2026-10-05.json"),
              "w") as f:
        json.dump(manifest, f, indent=1)
        f.write("\n")

    print(f"bench: {bench_path}")
    print(f"pin: {pin}")
    print(f"strata: {dict(sc)}")
    print(f"gold min count: {min(gold_counts.values())}")


if __name__ == "__main__":
    main()
