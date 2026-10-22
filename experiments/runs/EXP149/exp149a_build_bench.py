"""EXP149 study (a) bench builder — fresh 760-item multi-hop bench (seed 149001).

Templatic construction per the EXP147/148 §5.1 recipe (S7-1_build_bench_2026-10-05.py):
closed 40-name entity pool, every gold a single entity NAME appearing >=2x,
entity-disjoint exemplars (Law #7). Strata: {transitive, compositional} x
{2-hop, 3-hop} x 190 items = 760. ZERO model forwards (string ops only).

Registered constants: CONSTRUCTION_SEED = 149001 (new, != 7101).
Pin: SHA-256 over canonical serialization (reference_implementation.bench_sha256).
"""
import json
import os
import random
import sys

EXP092_DIR = os.path.expanduser("~/workspace/SCBI/experiments/runs/EXP092_ibl")
sys.path.insert(0, EXP092_DIR)
import reference_implementation as ref  # noqa: E402 (committed, read-only)

RUN_DIR = os.path.dirname(os.path.abspath(__file__))
CONSTRUCTION_SEED = 149001  # registered at execution; != 7101
N_PER_STRATUM = 190

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
            "id": f"E149a-{i+1:04d}",
            "stratum": s,
            "facts": facts,
            "question": question,
            "gold": gold,
        })

    assert len(bench) == 760, len(bench)
    keys = [(tuple(it["facts"]), it["question"]) for it in bench]
    assert len(set(keys)) == 760, "surface collision"
    from collections import Counter
    sc = Counter(it["stratum"] for it in bench)
    assert all(sc[s] == 190 for s in strata), dict(sc)
    assert all(it["gold"] in ENTITY_POOL for it in bench)

    pin = ref.bench_sha256(bench)

    bench_path = os.path.join(RUN_DIR, "EXP149A_BENCH_2026-10-09.json")
    with open(bench_path, "w") as f:
        json.dump(bench, f, indent=1)
        f.write("\n")

    with open(bench_path) as f:
        bench2 = json.load(f)
    pin2 = ref.bench_sha256(bench2)
    assert pin == pin2, "pin mismatch on recompute"
    assert len(pin) == 64 and all(a == b for a, b in zip(pin, pin2))

    manifest = {
        "experiment": "EXP149", "study": "a (hop dose-response)",
        "construction_seed": CONSTRUCTION_SEED,
        "n": 760, "n_per_stratum": 190, "strata": dict(sc),
        "pin": pin, "bench_path": os.path.basename(bench_path),
        "entity_pool_size": 40, "exemplar_entities_disjoint": True,
        "gold_min_count": min(gold_counts.values()),
        "g0d_note": "single entity NAME per gold (EXP148 §5.1 recipe)",
    }
    with open(os.path.join(RUN_DIR, "EXP149A_BENCH_MANIFEST_2026-10-09.json"),
              "w") as f:
        json.dump(manifest, f, indent=1)
        f.write("\n")

    print(f"bench: {bench_path}")
    print(f"pin: {pin}")
    print(f"strata: {dict(sc)}")
    print(f"gold min count: {min(gold_counts.values())}")


if __name__ == "__main__":
    main()
