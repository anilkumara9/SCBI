"""EXP092 (IBL) reference implementation — CITED BY the pre-registration draft v2.1.

This is the canonical bench builder + oracle/permutation reference for the
G0 (bench provenance) and G2 (null-calibration) guards. The signed protocol's
§2 bench hash pin and §6 G0/G2 gates are defined against THIS implementation's
exact outputs. Any bundle builder must reproduce its bench byte-for-byte
(modulo the canonical serialization) or RUN-INVALID.

Registered spec (see EXP092_IBL_PREREG_DRAFT_V2.md §2, §4, §6, §8):
  - Item schema: {"id","prompt","A","C","ent","typ","hop","domain","phrasing","tuple"}
  - Canonical serialization: json.dumps(bench, sort_keys=True,
      separators=(",", ":"), ensure_ascii=True).encode("utf-8"); pin = SHA-256.
  - Phrasing rule (FIX 1, corrected): planetary A-first iff block index i even;
      elemental A-first iff i odd. (i is 0-based within each 15-item block.)
  - Option-order rule (FIX 2): question options list the target first iff the
      item is A-first: q_opts = "A or F" if a_first else "F or A".
  - Prompt templates: verbatim EXP091 (outranks / is lower than forms).
  - Oracle: analytic expected-accuracy LOO 1-NN by max premise-entity overlap
      (deterministic; no RNG). Premise entities derived from tuple + vocab.
  - Permutation null: labels shuffled within (domain x phrasing) strata via
      random.Random(PERM_SEED + b) per permutation b; p = (1+ge)/(1+B).
"""

import hashlib
import json
import random

# ---------------------------------------------------------------------------
# Registered constants
# ---------------------------------------------------------------------------
PLANET_VOCAB = ["Mars", "Venus", "Jupiter", "Saturn", "Mercury",
                "Europa", "Titan", "Io", "Triton", "Miranda"]
ELEMENT_VOCAB = ["Iron", "Gold", "Silver", "Bronze", "Steel",
                 "Tin", "Lead", "Silicon", "Carbon", "Crystal"]

# Appendix A tuple arrays (seed-1022 deterministic assignment, registered verbatim).
TRIPLES_PLANET = [
    (1, 6, 7), (7, 5, 0), (0, 9, 6), (8, 2, 0), (3, 7, 0),
    (2, 5, 4), (3, 5, 4), (2, 0, 9), (6, 0, 5), (6, 2, 7),
    (0, 2, 1), (5, 0, 9), (9, 7, 4), (5, 8, 2), (4, 1, 9),
]
QUADS_PLANET = [
    (5, 1, 4, 2), (0, 7, 5, 6), (2, 5, 4, 3), (3, 2, 9, 4), (9, 4, 2, 5),
    (6, 2, 9, 0), (1, 4, 9, 6), (8, 7, 3, 4), (4, 3, 6, 9), (4, 1, 5, 0),
    (7, 5, 2, 6), (7, 9, 4, 8), (8, 6, 2, 3), (9, 3, 1, 6), (1, 3, 2, 5),
]
TRIPLES_ELEMENT = [
    (5, 0, 2), (9, 7, 8), (1, 8, 7), (9, 2, 8), (3, 0, 6),
    (2, 1, 5), (1, 3, 5), (6, 8, 4), (8, 4, 2), (4, 5, 6),
    (5, 7, 4), (0, 2, 6), (8, 9, 2), (7, 4, 2), (4, 5, 1),
]
QUADS_ELEMENT = [
    (6, 0, 1, 7), (4, 1, 9, 2), (3, 0, 1, 8), (0, 2, 9, 5), (9, 8, 5, 6),
    (5, 1, 2, 8), (6, 2, 0, 4), (3, 5, 1, 4), (7, 2, 6, 5), (2, 0, 3, 4),
    (1, 0, 6, 4), (0, 6, 4, 5), (7, 2, 4, 9), (2, 5, 3, 6), (8, 1, 7, 0),
]

N_BENCH = 60
PERM_SEED = 9207          # registered RNG seed for the permutation null
PERM_B_ORACLE = 10000     # G2 diagnostic permutations
PERM_B_REAL = 1000        # §4 real-statistic permutations per layer

# §4 strata table (registered).
STRATA_TABLE = {
    ("Planetary", "A-first"): 16, ("Planetary", "C-first"): 14,
    ("Elemental", "A-first"): 14, ("Elemental", "C-first"): 16,
}


# ---------------------------------------------------------------------------
# Bench builder (canonical)
# ---------------------------------------------------------------------------
def _phrasing(domain, i):
    """FIX 1 (corrected) parity rule: planetary A-first iff i even;
    elemental A-first iff i odd. i is 0-based within the 15-item block."""
    if domain == "Planetary":
        return "A-first" if (i % 2 == 0) else "C-first"
    return "A-first" if (i % 2 == 1) else "C-first"


def build_bench():
    """Build the 60-item EXP092-B bench. Deterministic; no RNG."""
    bench = []
    blocks = [
        ("Planetary", "planet", PLANET_VOCAB, TRIPLES_PLANET, QUADS_PLANET),
        ("Elemental", "element", ELEMENT_VOCAB, TRIPLES_ELEMENT, QUADS_ELEMENT),
    ]
    for domain, typ, vocab, triples, quads in blocks:
        for kind, arr, hop in (("2hop", triples, 2), ("3hop", quads, 3)):
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
                phrasing = _phrasing(domain, i)
                a_first = (phrasing == "A-first")
                # FIX 2: option-order rule — target first iff A-first.
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
                    "id": f"exp092_{domain.lower()}_{kind}_{i}",
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
    assert len(bench) == N_BENCH
    return bench


def canonical_json(bench):
    """Registered canonical serialization (FIX 2)."""
    return json.dumps(bench, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("utf-8")


def bench_sha256(bench=None):
    """Registered bench pin (FIX 2): SHA-256 of the canonical serialization."""
    bench = bench if bench is not None else build_bench()
    return hashlib.sha256(canonical_json(bench)).hexdigest()


# ---------------------------------------------------------------------------
# G0: bench-provenance assertions
# ---------------------------------------------------------------------------
class BenchInvalid(Exception):
    pass


def verify_g0(bench=None, expected_pin=None):
    """G0 refusal gate: uniqueness, balance, strata, pin. Raises on failure."""
    bench = bench if bench is not None else build_bench()
    assert len(bench) == N_BENCH, f"G0 FAIL: n={len(bench)} != 60"
    keys = [(b["domain"], tuple(b["tuple"])) for b in bench]
    assert len(set(keys)) == N_BENCH, "G0 FAIL: duplicate (domain,tuple)"
    from collections import Counter
    tc = Counter((b["domain"], b["ent"]) for b in bench)
    assert len(tc) == 20 and all(v == 3 for v in tc.values()), \
        f"G0 FAIL: target balance {dict(tc)}"
    ph = Counter((b["domain"], b["phrasing"]) for b in bench)
    assert dict(ph) == STRATA_TABLE, f"G0 FAIL: strata {dict(ph)}"
    n_a = sum(1 for b in bench if b["phrasing"] == "A-first")
    assert n_a == 30, f"G0 FAIL: A-first={n_a} != 30"
    pin = bench_sha256(bench)
    if expected_pin is not None and pin != expected_pin:
        raise BenchInvalid(f"G0 FAIL: pin {pin} != registered {expected_pin}")
    return {"n": len(bench), "unique_tuples": len(set(keys)),
            "strata": dict(ph), "pin": pin}


# ---------------------------------------------------------------------------
# G2: entity-set oracle (analytic expected accuracy) + stratified permutation
# ---------------------------------------------------------------------------
def _premise_entities(item):
    vocab = PLANET_VOCAB if item["domain"] == "Planetary" else ELEMENT_VOCAB
    return {vocab[k] for k in item["tuple"]}


def oracle_expected_accuracy(bench):
    """Entity-set oracle: LOO 1-NN by max premise-entity overlap.
    Ties broken uniformly at random -> analytic expected accuracy.
    Deterministic; no RNG."""
    n = len(bench)
    ents = [_premise_entities(b) for b in bench]
    labels = [b["ent"] for b in bench]
    total = 0.0
    for i in range(n):
        Si, yi = ents[i], labels[i]
        best, hit, cands = -1, 0, 0
        for j in range(n):
            if j == i:
                continue
            ov = len(Si & ents[j])
            if ov > best:
                best, hit, cands = ov, 0, 0
            if ov == best:
                cands += 1
                if labels[j] == yi:
                    hit += 1
        total += hit / cands
    return total / n


def stratified_permutation_p(bench, stat_fn, B, seed=PERM_SEED):
    """Stratified permutation null: permute labels within (domain x phrasing).
    Permutation b uses random.Random(seed + b). p = (1+ge)/(1+B)."""
    obs = stat_fn(bench)
    labels = [b["ent"] for b in bench]
    strata = {}
    for i, b in enumerate(bench):
        strata.setdefault((b["domain"], b["phrasing"]), []).append(i)
    ge = 0
    for b in range(B):
        rng = random.Random(seed + b)
        pl = labels[:]
        for idxs in strata.values():
            sub = [pl[i] for i in idxs]
            rng.shuffle(sub)
            for i, s in zip(idxs, sub):
                pl[i] = s
        b2 = [dict(item, ent=lab) for item, lab in zip(bench, pl)]
        if stat_fn(b2) >= obs:
            ge += 1
    return obs, (1 + ge) / (1 + B)


def g2_diagnostic(bench=None):
    """G2 build-time refusal gate: oracle must NOT be significant (p >= 0.05)."""
    bench = bench if bench is not None else build_bench()
    obs, p = stratified_permutation_p(bench, oracle_expected_accuracy,
                                      PERM_B_ORACLE)
    return {"oracle_accuracy": obs, "permutation_p": p,
            "B": PERM_B_ORACLE, "seed": PERM_SEED,
            "gate": "PASS" if p >= 0.05 else "FAIL"}


if __name__ == "__main__":
    bench = build_bench()
    g0 = verify_g0(bench)
    g0_print = dict(g0)
    g0_print["strata"] = {f"{d}/{p}": v for (d, p), v in g0["strata"].items()}
    print("G0:", json.dumps(g0_print, indent=1, sort_keys=True))
    g2 = g2_diagnostic(bench)
    print("G2:", json.dumps(g2, indent=1, sort_keys=True))
