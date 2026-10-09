"""EXP151 bench builder — fresh 760-item transitive-only bench (seed 151001).

Strata: transitive-2hop, transitive-3hop (recipe carried verbatim from the
EXP147/148/149a §5.1 recipe). Hardened-compositional is EXCLUDED by
design-record (LOG-4973/§5.1: (v2)-literal and (v4) jointly unsatisfiable on
Pythia-410m — reconciliation is a deferred, unlicensed lane).

ZERO model forwards (string ops only). The Pythia tokenizer is loaded from
the local snapshot OFFLINE for the registered pool-tokenizability audit —
a computation, not a forward.

Registered constants: CONSTRUCTION_SEED = 151001 (new; != 149001, != 150001).
Subset seeds: dry-run 151012 (= 151001+11), pilot 151023 (= 151001+23) —
the registered A2 seed-derivation rule (no execution-time choice).
Pin: SHA-256 over canonical serialization (reference_implementation.bench_sha256).
"""
import json
import os
import random
import sys

EXP092_DIR = os.path.expanduser("~/workspace/SCBI/experiments/runs/EXP092_ibl")
sys.path.insert(0, EXP092_DIR)
import reference_implementation as ref  # noqa: E402 (committed, read-only)

os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

RUN_DIR = os.path.dirname(os.path.abspath(__file__))
CONSTRUCTION_SEED = 151001  # registered at design; != 149001, != 150001
DRYRUN_SEED = 151012        # = 151001 + 11 (registered A2 rule)
PILOT_SEED = 151023         # = 151001 + 23 (registered A2 rule)
N_PER_STRATUM = 380

ENTITY_POOL = [
    "Zorp", "Blip", "Fweep", "Quix", "Vorn", "Jalp", "Trun", "Plix",
    "Sarn", "Wex", "Yub", "Krad", "Lomit", "Nax", "Prub", "Qel",
    "Rint", "Stov", "Tunk", "Ulf", "Vram", "Xob", "Yent", "Zarn",
    "Blix", "Crun", "Drup", "Flib", "Grax", "Hont", "Jurb", "Klap",
    "Miv", "Nox", "Olp", "Pruv", "Quib", "Ralv", "Slun", "Tiv",
]
EXEMPLAR_ENTITIES = {"Wug", "Dax", "Pim", "Zib", "Kev", "Mog"}


def build_transitive(rng, h, n):
    # Carried verbatim from the EXP147/148 §5.1 recipe (EXP149a/EXP150 builder).
    items = []
    for _ in range(n):
        ents = rng.sample(ENTITY_POOL, h + 1)  # ents[0] > ... > ents[h]
        if rng.random() < 0.5:
            facts = [f"{ents[i]} is taller than {ents[i+1]}."
                     for i in range(h)]
        else:
            facts = [f"{ents[h-i]} is shorter than {ents[h-i-1]}."
                     for i in range(h)]
        if rng.random() < 0.5:
            question, gold = "Who is the shortest?", ents[h]
        else:
            question, gold = "Who is the tallest?", ents[0]
        items.append((facts, question, gold))
    return items


def check_single_token_pool():
    # Pool-tokenizability audit (offline tokenizer, zero forwards):
    # records how many of the 40 closed-pool entities are a single token
    # under the Pythia tokenizer (' '+word convention). Descriptive only —
    # the transitive recipe's whitespace-token scoring has no (v2) constraint
    # (Law #9: this is construction-time metadata, not a validity gate).
    from transformers import AutoTokenizer
    cache = os.path.expanduser("~/.cache/huggingface")
    snap = os.path.join(cache, "hub", "models--EleutherAI--pythia-410m",
                        "snapshots")
    revs = sorted(os.listdir(snap))
    assert len(revs) == 1, f"expected 1 cached snapshot, got {revs}"
    tok = AutoTokenizer.from_pretrained(
        os.path.join(snap, revs[0]), local_files_only=True,
        trust_remote_code=False)
    bad = [e for e in ENTITY_POOL
           if len(tok.encode(" " + e, add_special_tokens=False)) != 1]
    ex = ENTITY_POOL[0]
    example = (f"' {ex}' -> "
               f"{tok.convert_ids_to_tokens(tok.encode(' ' + ex, add_special_tokens=False))}")
    return {"n_single": len(ENTITY_POOL) - len(bad),
            "n_multi": len(bad), "example": example,
            "all_multi": len(bad) == len(ENTITY_POOL)}


def main():
    assert not (set(ENTITY_POOL) & EXEMPLAR_ENTITIES), "Law #7: pool overlap"
    assert len(ENTITY_POOL) == 40

    # Pool-tokenizability audit (offline, zero forwards — construction
    # metadata only; NOT a validity gate: the transitive recipe has no (v2)
    # constraint; scoring is whitespace-token-based).
    v2 = check_single_token_pool()
    print(f"tokenizability audit: {v2['n_single']}/40 pool entities "
          f"single-token; example: {v2['example']}")
    # Design-record (LOG-4973): hardened-compositional EXCLUDED — (v2)-literal
    # and (v4) are jointly unsatisfiable on Pythia-410m. No hardened strata
    # are built; their reconciliation is a deferred, unlicensed lane.
    print("DESIGN-RECORD: hardened-compositional EXCLUDED (see manifest).")

    rng = random.Random(CONSTRUCTION_SEED)
    strata = ["transitive-2hop", "transitive-3hop"]
    raw = []
    for s in strata:
        h = 2 if s.endswith("2hop") else 3
        raw.extend([(s,) + t for t in build_transitive(rng, h, N_PER_STRATUM)])

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
            h = 2 if s.endswith("2hop") else 3
            raw.extend([(s,) + t for t in build_transitive(rng, h,
                                                          N_PER_STRATUM)])

    bench = []
    for i, (s, facts, question, gold) in enumerate(raw):
        bench.append({
            "id": f"E151-{i+1:04d}",
            "stratum": s,
            "facts": facts,
            "question": question,
            "gold": gold,
        })

    assert len(bench) == 760, len(bench)
    # semantic surface uniqueness: (sorted facts, question)
    keys = [(tuple(sorted(it["facts"])), it["question"]) for it in bench]
    assert len(set(keys)) == 760, "surface collision"
    from collections import Counter
    sc = Counter(it["stratum"] for it in bench)
    assert all(sc[s] == 380 for s in strata), dict(sc)
    assert all(it["gold"] in ENTITY_POOL for it in bench)

    pin = ref.bench_sha256(bench)

    bench_path = os.path.join(RUN_DIR, "EXP151_BENCH_2026-10-09.json")
    with open(bench_path, "w") as f:
        json.dump(bench, f, indent=1)
        f.write("\n")

    with open(bench_path) as f:
        bench2 = json.load(f)
    pin2 = ref.bench_sha256(bench2)
    assert pin == pin2, "pin mismatch on recompute"
    assert len(pin) == 64 and all(a == b for a, b in zip(pin, pin2))

    manifest = {
        "experiment": "EXP151",
        "construction_seed": CONSTRUCTION_SEED,
        "dryrun_subset_seed": DRYRUN_SEED,
        "pilot_subset_seed": PILOT_SEED,
        "n": 760, "n_per_stratum": 380, "strata": dict(sc),
        "pin": pin, "bench_path": os.path.basename(bench_path),
        "entity_pool_size": 40, "exemplar_entities_disjoint": True,
        "gold_min_count": min(gold_counts.values()),
        "tokenizability_audit": (f"{v2['n_single']}/40 single-token "
                                 f"(' '+word, Pythia BPE, offline); example {v2['example']} — "
                                 f"metadata only, not a gate"),
        "hardened_compositional": "EXCLUDED by design-record (LOG-4973): "
            "(v2)-literal and (v4) jointly unsatisfiable on Pythia-410m; "
            "reconciliation is a deferred, unlicensed lane",
        "gold_note": "single entity NAME per gold (EXP148 §5.1 recipe)",
    }
    with open(os.path.join(RUN_DIR, "EXP151_BENCH_MANIFEST_2026-10-09.json"),
              "w") as f:
        json.dump(manifest, f, indent=1)
        f.write("\n")

    print(f"bench: {bench_path}")
    print(f"pin: {pin}")
    print(f"strata: {dict(sc)}")
    print(f"gold min count: {min(gold_counts.values())}")
    t2 = [it for it in bench if it["stratum"] == "transitive-2hop"][:2]
    for it in t2:
        print(f"  sample {it['id']}: facts={it['facts']}")
        print(f"    Q: {it['question']} -> {it['gold']}")


if __name__ == "__main__":
    main()
