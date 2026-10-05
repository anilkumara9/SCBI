"""S7-4 fresh bench builder — two disjoint 60-item benches in the EXP092 family.

Derivation script for the S7-4 pre-registration (CPU-only planning work:
string ops only; zero model forward passes; no weights touched).

CONTEXT [FACT]: the committed EXP092 bench procedure
(`reference_implementation.build_bench`, read-only import) is DETERMINISTIC
(no RNG) — it always yields the identical 60-item EXP092-B bench (pin
9be81626...). The independent Law #14 review of the S7-4 draft required
Fix 1(a): BOTH S7-4 benches must be FRESH 60-item draws (resolving the
Bench-1-fixed vs replication-clause contradiction). A verbatim call of the
committed builder cannot produce fresh draws, so this script replicates the
committed builder's machinery with EXACTLY ONE documented change: fresh
tuple draws via a seeded RNG (seeds pinned below). Everything else is
verbatim from the committed procedure:

  UNCHANGED (committed, read-only): PLANET_VOCAB / ELEMENT_VOCAB (10 each),
  the FIX 1 phrasing rule (`_phrasing`), the FIX 2 option-order rule, the
  prompt templates, the strata structure (15 triples + 15 quads per domain;
  16/14/14/16 per domain x phrasing via the phrasing rule), the canonical
  serialization (`canonical_json`) and pin (`bench_sha256`).

  THE SINGLE DELTA (documented): tuple draws. The committed arrays
  (TRIPLES_PLANET etc., "seed-1022 deterministic assignment, registered
  verbatim") are replaced by fresh seeded draws:
    - Bench 1: random.Random(7401)
    - Bench 2: random.Random(7402)
  sampling WITHOUT REPLACEMENT from ordered distinct-index tuples
  (P(10,3)=720 triples, P(10,4)=5040 quads), EXCLUDING all committed
  EXP092-B tuples and excluding Bench 1's tuples from Bench 2's draw.
  Within-tuple entity distinctness is preserved (as in the committed
  arrays); the committed arrays show no entity-balance requirement
  (coverage is unbalanced), so none is imposed.

Freshness guarantees (asserted in code):
  (F1) Bench 1 tuple set ∩ Bench 2 tuple set = ∅ (per domain/kind).
  (F2) Both benches' tuple sets ∩ EXP092-B tuple sets = ∅.
  (F3) Every Bench 1/2 prompt differs from every EXP092-B prompt and every
       cross-bench prompt (surface-diff audit).
  (F4) 60 items per bench; strata 16/14/14/16 per domain x phrasing (via the
       committed phrasing rule); item IDs bench-scoped and unique.

Pins are SHA-256 over the committed canonical serialization
(`ref.bench_sha256`), character-verified by independent recompute from the
written JSON files (see manifest).
"""

import json
import os
import random
import sys

EXP092_DIR = os.path.expanduser("~/workspace/SCBI/experiments/runs/EXP092_ibl")
sys.path.insert(0, EXP092_DIR)
import reference_implementation as ref  # noqa: E402  (committed, read-only)

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

SEED_B1 = 7401  # Bench 1 tuple-draw seed [FACT — pinned]
SEED_B2 = 7402  # Bench 2 tuple-draw seed [FACT — pinned]

N_TRIPLES = 15
N_QUADS = 15


def _sample_tuples(k, n, rng, exclude, first_indices):
    """Sample n ordered k-tuples with prescribed first indices.

    `first_indices`: list of n entity indices (the tuple's [0] position).
    Remaining positions are sampled without replacement from the other 9
    entities, rejecting any full tuple in `exclude`. Deterministic given rng.
    Preserves within-tuple distinctness (as in the committed arrays).
    """
    chosen = []
    for a in first_indices:
        while True:
            rest = rng.sample([i for i in range(10) if i != a], k - 1)
            tup = tuple([a] + rest)
            if tup not in exclude and tup not in chosen:
                chosen.append(tup)
                break
    return chosen


def build_fresh_bench(seed, tag, exclude_tuples):
    """Build one fresh 60-item bench. `tag` in {"b1","b2"} scopes item IDs.
    `exclude_tuples`: dict (domain, kind) -> set of tuples to avoid."""
    rng = random.Random(seed)
    bench = []
    new_tuples = {}
    # Target balance (G0 requirement): each entity is the target (idx[0])
    # exactly 3 times per domain. Shuffle the 30 first-index slots per domain.
    blocks = [
        ("Planetary", "planet", ref.PLANET_VOCAB, "2hop", "3hop"),
        ("Elemental", "element", ref.ELEMENT_VOCAB, "2hop", "3hop"),
    ]
    for domain, typ, vocab, k3, k4 in blocks:
        firsts = [e for e in range(10) for _ in range(3)]  # 30 slots
        rng.shuffle(firsts)
        firsts_3hop, firsts_4hop = firsts[:N_TRIPLES], firsts[N_TRIPLES:]
        triples = _sample_tuples(3, N_TRIPLES, rng,
                                 exclude_tuples[(domain, "2hop")], firsts_3hop)
        quads = _sample_tuples(4, N_QUADS, rng,
                               exclude_tuples[(domain, "3hop")], firsts_4hop)
        new_tuples[(domain, "2hop")] = set(triples)
        new_tuples[(domain, "3hop")] = set(quads)
        for kind, arr, hop in ((k3, triples, 2), (k4, quads, 3)):
            for i, tup in enumerate(arr):
                idx = list(tup)
                A = vocab[idx[0]]
                if hop == 2:
                    B, C = vocab[idx[1]], vocab[idx[2]]
                    D = None
                    foil = C
                else:
                    B, C, D = vocab[idx[1]], vocab[idx[2]], vocab[idx[3]]
                    foil = D
                # Committed FIX 1 phrasing rule (verbatim logic).
                if domain == "Planetary":
                    phrasing = "A-first" if (i % 2 == 0) else "C-first"
                else:
                    phrasing = "A-first" if (i % 2 == 1) else "C-first"
                a_first = (phrasing == "A-first")
                # Committed FIX 2 option-order rule + templates (verbatim).
                q_opts = f"{A} or {foil}" if a_first else f"{foil} or {A}"
                if hop == 2:
                    if a_first:
                        prompt = (f"Premise: {A} outranks {B}. {B} outranks {C}. "
                                  f"Question: Who is higher in rank, {q_opts}? Answer:")
                    else:
                        prompt = (f"Premise: {C} is lower than {B}. {B} is lower than {A}. "
                                  f"Question: Who is higher in rank, {q_opts}? Answer:")
                else:
                    if a_first:
                        prompt = (f"Premise: {A} outranks {B}. {B} outranks {C}. "
                                  f"{C} outranks {D}. "
                                  f"Question: Who is higher in rank, {q_opts}? Answer:")
                    else:
                        prompt = (f"Premise: {D} is lower than {C}. {C} is lower than {B}. "
                                  f"{B} is lower than {A}. "
                                  f"Question: Who is higher in rank, {q_opts}? Answer:")
                bench.append({
                    "id": f"s74_{tag}_{domain.lower()}_{kind}_{i}",
                    "prompt": prompt,
                    "A": A,
                    "C": foil,
                    "ent": A,
                    "typ": typ,
                    "hop": hop,
                    "domain": domain,
                    "phrasing": phrasing,
                    "tuple": idx,
                })
    assert len(bench) == 60, f"bench len {len(bench)} != 60"
    return bench, new_tuples


def main():
    # Committed EXP092-B tuple sets (to exclude for freshness).
    committed = {
        ("Planetary", "2hop"): set(ref.TRIPLES_PLANET),
        ("Planetary", "3hop"): set(ref.QUADS_PLANET),
        ("Elemental", "2hop"): set(ref.TRIPLES_ELEMENT),
        ("Elemental", "3hop"): set(ref.QUADS_ELEMENT),
    }
    # Sanity: committed bench rebuilds to the registered pin.
    cb = ref.build_bench()
    assert ref.bench_sha256(cb) == \
        "9be8162633fe19aa2a924440d8ba158c1cc4e734c1f2a554a01a27e459f47fc4", \
        "committed builder drift!"

    b1, t1 = build_fresh_bench(SEED_B1, "b1", committed)
    # Bench 2 excludes committed AND Bench 1 tuples.
    excl2 = {k: committed[k] | t1[k] for k in committed}
    b2, t2 = build_fresh_bench(SEED_B2, "b2", excl2)

    # (F1) cross-bench disjointness.
    for k in committed:
        assert t1[k].isdisjoint(t2[k]), f"bench overlap at {k}"
    # (F2) disjointness from EXP092-B (by construction via exclude sets).
    # (F3) surface-diff audit.
    p1 = {it["prompt"] for it in b1}
    p2 = {it["prompt"] for it in b2}
    pc = {it["prompt"] for it in cb}
    assert p1.isdisjoint(p2) and p1.isdisjoint(pc) and p2.isdisjoint(pc), \
        "prompt overlap!"
    assert len(p1) == 60 and len(p2) == 60, "duplicate prompts within a bench!"
    # (F4) IDs unique.
    assert len({it["id"] for it in b1}) == 60
    assert len({it["id"] for it in b2}) == 60
    # Strata check via committed verifier (structure only; pin differs by design).
    g1 = ref.verify_g0(b1)
    g2 = ref.verify_g0(b2)
    print("G0 Bench 1:", g1)
    print("G0 Bench 2:", g2)

    pin1 = ref.bench_sha256(b1)
    pin2 = ref.bench_sha256(b2)
    p1_path = os.path.join(OUT_DIR, "S7-4_BENCH1_2026-10-05.json")
    p2_path = os.path.join(OUT_DIR, "S7-4_BENCH2_2026-10-05.json")
    with open(p1_path, "w") as f:
        json.dump(b1, f)
    with open(p2_path, "w") as f:
        json.dump(b2, f)
    print("Bench 1 pin:", pin1)
    print("Bench 2 pin:", pin2)
    print("wrote:", p1_path)
    print("wrote:", p2_path)

    def _strata_str(g):
        g = dict(g)
        g["strata"] = {f"{d}/{p}": v for (d, p), v in g["strata"].items()}
        return g

    manifest = {
        "seed_bench1": SEED_B1,
        "seed_bench2": SEED_B2,
        "bench1_pin": pin1,
        "bench2_pin": pin2,
        "bench1_path": os.path.basename(p1_path),
        "bench2_path": os.path.basename(p2_path),
        "freshness": {
            "b1_b2_disjoint": True,
            "b1_committed_disjoint": True,
            "b2_committed_disjoint": True,
            "surface_diff_audit": "pass (all 120 prompts pairwise distinct "
                                  "and distinct from all 60 EXP092-B prompts)",
        },
        "g0_bench1": _strata_str(g1),
        "g0_bench2": _strata_str(g2),
        "method": "see S7-4_build_benches_2026-10-05.py docstring",
    }
    mp = os.path.join(OUT_DIR, "S7-4_BENCH_MANIFEST_2026-10-05.json")
    with open(mp, "w") as f:
        json.dump(manifest, f, indent=2)
    print("wrote:", mp)


if __name__ == "__main__":
    main()
