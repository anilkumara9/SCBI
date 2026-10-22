"""EXP150 bench builder — fresh 760-item bench (seed 150001).

Strata: transitive-2hop, transitive-3hop (recipe carried verbatim from the
EXP147/148/149a §5.1 recipe), hardened-compositional-2hop,
hardened-compositional-3hop (distractor-chain procedure per the registered
EXP150 design §5; validity constraints (v1)-(v4) asserted at construction).

ZERO model forwards (string ops only). The Pythia tokenizer is loaded from
the local snapshot OFFLINE for the registered (v2) single-token check — a
computation, not a forward.

Registered constants: CONSTRUCTION_SEED = 150001 (new; != 149001).
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
CONSTRUCTION_SEED = 150001  # registered at execution; != 149001
N_PER_STRATUM = 190

ENTITY_POOL = [
    "Zorp", "Blip", "Fweep", "Quix", "Vorn", "Jalp", "Trun", "Plix",
    "Sarn", "Wex", "Yub", "Krad", "Lomit", "Nax", "Prub", "Qel",
    "Rint", "Stov", "Tunk", "Ulf", "Vram", "Xob", "Yent", "Zarn",
    "Blix", "Crun", "Drup", "Flib", "Grax", "Hont", "Jurb", "Klap",
    "Miv", "Nox", "Olp", "Pruv", "Quib", "Ralv", "Slun", "Tiv",
]
EXEMPLAR_ENTITIES = {"Wug", "Dax", "Pim", "Zib", "Kev", "Mog"}

RELATIONS_T = ["friend", "pet", "toy", "hat", "car", "book"]  # unused (kept for parity)
RELATIONS_HC = ["hat", "friend", "pet", "car", "book"]  # registered §5


def build_transitive(rng, h, n):
    # Carried verbatim from the EXP147/148 §5.1 recipe (EXP149a builder).
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


def build_hardened(rng, h, n):
    # Registered distractor-chain procedure (EXP150 design §5).
    items = []
    for _ in range(n):
        ents = rng.sample(ENTITY_POOL, 2 * h + 1)
        H = ents[0]
        Q = ents[1:1 + h]            # queried chain nodes Q1..Qh
        D = ents[1 + h:1 + 2 * h]    # distractor chain nodes D1..Dh
        Rp1 = rng.choice(RELATIONS_HC)
        R1 = rng.choice([r for r in RELATIONS_HC if r != Rp1])  # constraint 4
        R = [R1] + [rng.choice(RELATIONS_HC) for _ in range(h - 1)]
        Rp = [Rp1] + [rng.choice(RELATIONS_HC) for _ in range(h - 1)]
        qchain = [H] + Q
        dchain = [H] + D
        facts = []
        subj_rel = {}  # (subject, relation) -> object; (v3) mechanical check
        for j in range(h):
            k1, v1 = (qchain[j], R[j]), qchain[j + 1]
            k2, v2 = (dchain[j], Rp[j]), dchain[j + 1]
            assert k1 not in subj_rel and k2 not in subj_rel, \
                "(v3) subject-relation collision"
            subj_rel[k1] = v1
            subj_rel[k2] = v2
            facts.append(f"{qchain[j]}'s {R[j]} is {qchain[j+1]}.")
            facts.append(f"{dchain[j]}'s {Rp[j]} is {dchain[j+1]}.")
        rng.shuffle(facts)  # positional reading fails
        question = "Who is " + H + "".join(f"'s {r}" for r in R) + "?"
        gold = Q[-1]
        assert gold != D[-1], "(v1) terminal collision"
        # (v3): following the queried relation sequence from H lands on gold,
        # and no second reading yields it (subj_rel keys are unique).
        node = H
        for r in R:
            node = subj_rel[(node, r)]
        assert node == gold, "(v3) determinacy walk failed"
        items.append((facts, question, gold))
    return items


def build_stratum(rng, stratum, n):
    if stratum == "transitive-2hop":
        return build_transitive(rng, 2, n)
    if stratum == "transitive-3hop":
        return build_transitive(rng, 3, n)
    if stratum == "hardened-compositional-2hop":
        return build_hardened(rng, 2, n)
    if stratum == "hardened-compositional-3hop":
        return build_hardened(rng, 3, n)
    raise ValueError(stratum)


def check_single_token_pool():
    # (v2): every pool entity (every gold is drawn from the pool) is a
    # single token under the Pythia tokenizer — offline, zero forwards.
    # Registered convention (EXP149 (p1) lesson): ' ' + word, i.e. the gold
    # as it appears in generation (leading space).
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

    # (v2) construction-time check (offline tokenizer, zero forwards).
    # Registered convention (EXP149 (p1) lesson): ' ' + word.
    v2 = check_single_token_pool()
    print(f"(v2) single-token check: {v2['n_single']}/40 pool entities "
          f"single-token; example: {v2['example']}")

    # REGISTERED FALLBACK (execution brief + pre-reg §6.3 spirit):
    # (v2)-literal ("every gold a single token under the Pythia tokenizer")
    # FAILS — all 40 closed-pool entities are 2 BPE tokens under Pythia
    # (e.g. ' Zorp' -> ['ĠZ', 'orp']). (v4) pins the closed 40-entity pool
    # ("sample H from the 40-entity pool"), so (v2)-literal and (v4) are
    # JOINTLY UNSATISFIABLE on the registered model — no pool subset and no
    # model change can satisfy both. Per the execution brief ("if any
    # validity constraint fails, the registered fallback is transitive-only
    # — do not force a bad template"), the hardened-compositional secondary
    # is NOT built. The transitive primary (verdict-bearing) is unaffected:
    # its carried recipe has no (v2) constraint, scoring is
    # whitespace-token-based, and the model demonstrably emits these names
    # (EXP149a diagnostic: transitive B = 0.3105/0.3316 on this pool+model).
    # The (v2)/(v4) tension is recorded here as a bench-construction finding
    # for the design record. build_hardened() is retained above as the
    # registered-but-not-built procedure.
    hardened_dropped = True
    print("FALLBACK: (v2) fails literally -> hardened-compositional secondary "
          "NOT built; transitive-only bench (primary unaffected).")

    rng = random.Random(CONSTRUCTION_SEED)
    strata = ["transitive-2hop", "transitive-3hop"]
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
            "id": f"E150-{i+1:04d}",
            "stratum": s,
            "facts": facts,
            "question": question,
            "gold": gold,
        })

    assert len(bench) == 380, len(bench)
    # semantic surface uniqueness: (sorted facts, question)
    keys = [(tuple(sorted(it["facts"])), it["question"]) for it in bench]
    assert len(set(keys)) == 380, "surface collision"
    from collections import Counter
    sc = Counter(it["stratum"] for it in bench)
    assert all(sc[s] == 190 for s in strata), dict(sc)
    assert all(it["gold"] in ENTITY_POOL for it in bench)

    pin = ref.bench_sha256(bench)

    bench_path = os.path.join(RUN_DIR, "EXP150_BENCH_2026-10-09.json")
    with open(bench_path, "w") as f:
        json.dump(bench, f, indent=1)
        f.write("\n")

    with open(bench_path) as f:
        bench2 = json.load(f)
    pin2 = ref.bench_sha256(bench2)
    assert pin == pin2, "pin mismatch on recompute"
    assert len(pin) == 64 and all(a == b for a, b in zip(pin, pin2))

    manifest = {
        "experiment": "EXP150",
        "construction_seed": CONSTRUCTION_SEED,
        "n": 380, "n_per_stratum": 190, "strata": dict(sc),
        "pin": pin, "bench_path": os.path.basename(bench_path),
        "entity_pool_size": 40, "exemplar_entities_disjoint": True,
        "gold_min_count": min(gold_counts.values()),
        "v2_check": (f"{v2['n_single']}/40 single-token "
                     f"(' '+word, Pythia BPE, offline); example {v2['example']}"),
        "hardened_secondary": "NOT BUILT (registered fallback): (v2)-literal "
            "fails (all 40 pool entities 2 BPE tokens) and (v4) pins the "
            "closed 40-entity pool - jointly unsatisfiable on Pythia-410m; "
            "transitive-only per execution brief; build_hardened() retained "
            "as the registered-but-not-built procedure",
        "hardened_dropped": hardened_dropped,
        "gold_note": "single entity NAME per gold (EXP148 §5.1 recipe, v4)",
    }
    with open(os.path.join(RUN_DIR, "EXP150_BENCH_MANIFEST_2026-10-09.json"),
              "w") as f:
        json.dump(manifest, f, indent=1)
        f.write("\n")

    print(f"bench: {bench_path}")
    print(f"pin: {pin}")
    print(f"strata: {dict(sc)}")
    print(f"gold min count: {min(gold_counts.values())}")
    # sample transitive items for the log
    t2 = [it for it in bench if it["stratum"] == "transitive-2hop"][:2]
    for it in t2:
        print(f"  sample {it['id']}: facts={it['facts']}")
        print(f"    Q: {it['question']} -> {it['gold']}")


if __name__ == "__main__":
    main()
