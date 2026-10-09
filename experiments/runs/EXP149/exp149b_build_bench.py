"""EXP149 study (b) bench rebuild — GPT-2-BPE-safe 180-item bench (seed 149008).

Triggered by the pre-registered (p1)-fail branch: the parent S7-1 bench scored
0/180 single-token golds under GPT-2 BPE, so per pre-reg §5.1 the bench is
rebuilt by the EXP147 §5.1 procedure with a GPT-2-BPE-safe entity pool
(single-token golds under GPT-2 BPE BY CONSTRUCTION — every pool word verified
len(tokenizer.encode(' ' + word)) == 1). New construction seed 149008
(registered at execution; != 7101, != 149001). New pin recorded.

Templatic recipe identical to S7-1_build_bench_2026-10-05.py: 4 strata x 45,
gold >= 2x, surface-distinct, Law #7 exemplar disjointness. ZERO forwards.
"""
import json
import os
import random
import sys

EXP092_DIR = os.path.expanduser("~/workspace/SCBI/experiments/runs/EXP092_ibl")
sys.path.insert(0, EXP092_DIR)
import reference_implementation as ref  # noqa: E402 (committed, read-only)

RUN_DIR = os.path.dirname(os.path.abspath(__file__))
CONSTRUCTION_SEED = 149008  # registered at execution (b-rebuild)
N_PER_STRATUM = 45

# GPT-2-BPE-safe entity pool: 40 real words, each verified single-token under
# GPT-2 BPE with a leading space. Disjoint from exemplars {Wug,Dax,Pim,Zib,Kev,Mog}
# and from the relation vocabulary (friend/pet/toy/hat/car/book).
ENTITY_POOL = [
    "dog", "cat", "bird", "fish", "horse", "cow", "pig", "sheep",
    "wolf", "bear", "fox", "deer", "mouse", "frog", "snake", "tiger",
    "lion", "shark", "whale", "eagle", "owl", "ant", "bee", "crab",
    "duck", "goat", "hen", "ape", "bat", "rat", "man", "boy",
    "girl", "king", "queen", "monk", "chef", "clown", "pilot", "nurse",
]
EXEMPLAR_ENTITIES = {"Wug", "Dax", "Pim", "Zib", "Kev", "Mog"}
RELATIONS = ["friend", "pet", "toy", "hat", "car", "book"]


def build_stratum(rng, stratum, n):
    items = []
    if stratum == "transitive-2hop":
        for _ in range(n):
            a, b, c = rng.sample(ENTITY_POOL, 3)
            if rng.random() < 0.5:
                facts = [f"The {a} is taller than the {b}.",
                         f"The {b} is taller than the {c}."]
            else:
                facts = [f"The {c} is shorter than the {b}.",
                         f"The {b} is shorter than the {a}."]
            if rng.random() < 0.5:
                question, gold = "Who is the shortest?", c
            else:
                question, gold = "Who is the tallest?", a
            items.append((facts, question, gold))
    elif stratum == "transitive-3hop":
        for _ in range(n):
            a, b, c, d = rng.sample(ENTITY_POOL, 4)
            if rng.random() < 0.5:
                facts = [f"The {a} is taller than the {b}.",
                         f"The {b} is taller than the {c}.",
                         f"The {c} is taller than the {d}."]
            else:
                facts = [f"The {d} is shorter than the {c}.",
                         f"The {c} is shorter than the {b}.",
                         f"The {b} is shorter than the {a}."]
            if rng.random() < 0.5:
                question, gold = "Who is the shortest?", d
            else:
                question, gold = "Who is the tallest?", a
            items.append((facts, question, gold))
    elif stratum == "compositional-2hop":
        for _ in range(n):
            a, b, c = rng.sample(ENTITY_POOL, 3)
            r1, r2 = rng.sample(RELATIONS, 2)
            facts = [f"The {a}'s {r1} is the {b}.", f"The {b}'s {r2} is the {c}."]
            question = f"Who is the {a}'s {r1}'s {r2}?"
            gold = c
            items.append((facts, question, gold))
    elif stratum == "compositional-3hop":
        for _ in range(n):
            a, b, c, d = rng.sample(ENTITY_POOL, 4)
            r1, r2, r3 = rng.sample(RELATIONS, 3)
            facts = [f"The {a}'s {r1} is the {b}.", f"The {b}'s {r2} is the {c}.",
                     f"The {c}'s {r3} is the {d}."]
            question = f"Who is the {a}'s {r1}'s {r2}'s {r3}?"
            gold = d
            items.append((facts, question, gold))
    else:
        raise ValueError(stratum)
    return items


def main():
    assert not (set(ENTITY_POOL) & EXEMPLAR_ENTITIES), "Law #7: pool overlap"
    assert not (set(ENTITY_POOL) & set(RELATIONS)), "pool/relation overlap"
    assert len(ENTITY_POOL) == 40

    rng = random.Random(CONSTRUCTION_SEED)
    strata = ["transitive-2hop", "transitive-3hop",
              "compositional-2hop", "compositional-3hop"]
    raw = []
    for s in strata:
        raw.extend([(s,) + t for t in build_stratum(rng, s, N_PER_STRATUM)])

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
        rng = random.Random(CONSTRUCTION_SEED + attempt)
        raw = []
        for s in strata:
            raw.extend([(s,) + t for t in build_stratum(rng, s, N_PER_STRATUM)])

    bench = []
    for i, (s, facts, question, gold) in enumerate(raw):
        bench.append({
            "id": f"E149b-{i+1:03d}",
            "stratum": s,
            "facts": facts,
            "question": question,
            "gold": gold,
        })

    assert len(bench) == 180, len(bench)
    keys = [(tuple(it["facts"]), it["question"]) for it in bench]
    assert len(set(keys)) == 180, "surface collision"
    from collections import Counter
    sc = Counter(it["stratum"] for it in bench)
    assert all(sc[s] == 45 for s in strata), dict(sc)
    assert all(it["gold"] in ENTITY_POOL for it in bench)

    pin = ref.bench_sha256(bench)

    bench_path = os.path.join(RUN_DIR, "EXP149B_BENCH_2026-10-09.json")
    with open(bench_path, "w") as f:
        json.dump(bench, f, indent=1)
        f.write("\n")

    with open(bench_path) as f:
        bench2 = json.load(f)
    pin2 = ref.bench_sha256(bench2)
    assert pin == pin2, "pin mismatch on recompute"
    assert len(pin) == 64 and all(a == b for a, b in zip(pin, pin2))

    manifest = {
        "experiment": "EXP149", "study": "b (cross-family GPT-2-small)",
        "branch": "(p1)-fail rebuild (parent bench 0/180 single-token)",
        "construction_seed": CONSTRUCTION_SEED,
        "n": 180, "n_per_stratum": 45, "strata": dict(sc),
        "pin": pin, "bench_path": os.path.basename(bench_path),
        "entity_pool": "40 GPT-2-BPE-safe real words, single-token by construction",
        "exemplar_entities_disjoint": True,
        "gold_min_count": min(gold_counts.values()),
    }
    with open(os.path.join(RUN_DIR, "EXP149B_BENCH_MANIFEST_2026-10-09.json"),
              "w") as f:
        json.dump(manifest, f, indent=1)
        f.write("\n")

    print(f"bench: {bench_path}")
    print(f"pin: {pin}")
    print(f"strata: {dict(sc)}")
    print(f"gold min count: {min(gold_counts.values())}")


if __name__ == "__main__":
    main()
