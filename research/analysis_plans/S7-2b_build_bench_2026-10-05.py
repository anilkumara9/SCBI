"""S7-2b delta bench builder — Triton -> Neptune swap for GPT-2 BPE portability.

Derivation script for the S7-2b pre-registration (CPU-only planning work:
string ops + tokenizer encode; zero model forward passes; no weights touched).

Method: verbatim replication of the COMMITTED EXP092 bench-builder procedure
(reference_implementation.py, read-only import), with EXACTLY ONE documented
change: PLANET_VOCAB[8] "Triton" -> "Neptune". Rationale for Neptune:
  (a) single-token under GPT-2 BPE (verified by the G1' check below);
  (b) thematic coherence — Triton is Neptune's moon, preserving the Planetary
      domain's astronomical character (Neptune is a major planet like the
      other vocab entries);
  (c) no substring collisions with any other entity (word-boundary safe).
Screened alternatives that FAILED single-token: Uranus, Eris, Haumea,
Makemake, Callisto, Ganymede, Enceladus, Rhea, Dione, Iapetus, Oberon,
Umbriel, Charon, Phobos, Deimos, Nereid, Proteus. Also passing: Pluto,
Ceres, Ariel (rejected on thematic grounds — see (b)).

The tuple arrays, phrasing rule (FIX 1), option-order rule (FIX 2), prompt
templates, and canonical serialization are UNCHANGED — only surface strings
containing "Triton" (8 in-prompt occurrences across the 60 items) change.
"""

import hashlib
import json
import os
import re
import sys

EXP092_DIR = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "..", "SCBI",
    "experiments", "runs", "EXP092_ibl"))
# Fallback: resolve relative to this file's workspace location.
if not os.path.isdir(EXP092_DIR):
    EXP092_DIR = os.path.expanduser(
        "~/workspace/SCBI/experiments/runs/EXP092_ibl")
sys.path.insert(0, EXP092_DIR)
import reference_implementation as ref  # noqa: E402  (committed, read-only)

# --- THE SINGLE DELTA (documented) -------------------------------------------
# Committed: ["Mars","Venus","Jupiter","Saturn","Mercury","Europa","Titan",
#             "Io","Triton","Miranda"]  (index 8 = "Triton")
# S7-2b:     index 8 = "Neptune". Everything else byte-identical.
REPLACED = "Triton"
REPLACEMENT = "Neptune"
PLANET_VOCAB_S72B = [n if n != REPLACED else REPLACEMENT
                     for n in ref.PLANET_VOCAB]
assert PLANET_VOCAB_S72B[8] == "Neptune" and len(PLANET_VOCAB_S72B) == 10
assert sorted(set(PLANET_VOCAB_S72B)) == sorted(PLANET_VOCAB_S72B), \
    "duplicate entity introduced"
assert REPLACEMENT not in ref.ELEMENT_VOCAB

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
TOKENIZER_DIR = os.path.expanduser(
    "~/workspace/SCBI/experiments/runs/EXP144/hf_cache/"
    "models--gpt2/snapshots/607a30d783dfa663caf39e06633721c8d4cfcd7e")


def build_bench_s72b():
    """Verbatim copy of ref.build_bench() with the single vocab delta.

    All tuple arrays, phrasing rule, option-order rule, and templates are
    copied unchanged from the committed procedure; only `vocab` differs.
    """
    bench = []
    blocks = [
        ("Planetary", "planet", PLANET_VOCAB_S72B,
         ref.TRIPLES_PLANET, ref.QUADS_PLANET),
        ("Elemental", "element", ref.ELEMENT_VOCAB,
         ref.TRIPLES_ELEMENT, ref.QUADS_ELEMENT),
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
                phrasing = ref._phrasing(domain, i)
                a_first = (phrasing == "A-first")
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
    assert len(bench) == ref.N_BENCH
    return bench


def premise_entities_s72b(item):
    """Verbatim copy of ref._premise_entities with the delta vocab."""
    vocab = PLANET_VOCAB_S72B if item["domain"] == "Planetary" \
        else ref.ELEMENT_VOCAB
    return {vocab[k] for k in item["tuple"]}


def oracle_expected_accuracy_s72b(bench):
    """Verbatim copy of ref.oracle_expected_accuracy with delta vocab."""
    n = len(bench)
    ents = [premise_entities_s72b(b) for b in bench]
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


def g1prime_cover(tokenizer, bench):
    """EXACT replication of the EXP144 G1' offset-mapping cover logic.

    Returns (n_occurrences, n_single_token, per_entity_table). Bar: 240/240.
    """
    def word_pattern(name):
        return re.compile(r"\b" + re.escape(name) + r"\b")

    table = {}
    for b in bench:
        prompt = b["prompt"]
        enc = tokenizer(prompt, add_special_tokens=False,
                        return_offsets_mapping=True)
        ids = list(enc["input_ids"])
        offsets = [(int(s), int(e)) for s, e in enc["offset_mapping"]]
        pieces = tokenizer.convert_ids_to_tokens(ids)
        for name in (b["A"], b["C"]):
            if name not in table:
                table[name] = {"occurrences": 0, "single_token": 0,
                               "token_ids_seen": set(), "failing": []}
            for m in word_pattern(name).finditer(prompt):
                s, e = m.span()
                table[name]["occurrences"] += 1
                covering = [i for i, (os_, oe_) in enumerate(offsets)
                            if os_ < e and oe_ > s]
                ok = False
                if len(covering) == 1:
                    i = covering[0]
                    os_, oe_ = offsets[i]
                    text = pieces[i].replace("Ġ", "").replace("▁", "")
                    if text == name and os_ <= s and oe_ >= e:
                        ok = True
                        table[name]["token_ids_seen"].add(int(ids[i]))
                if ok:
                    table[name]["single_token"] += 1
                else:
                    table[name]["failing"].append(
                        (b["id"], [pieces[i] for i in covering]))
    n_occ = sum(t["occurrences"] for t in table.values())
    n_single = sum(t["single_token"] for t in table.values())
    return n_occ, n_single, table


def main():
    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_DIR,
                                              local_files_only=True)

    bench = build_bench_s72b()

    # 1. Structural identity vs the committed bench (only surface strings differ)
    ref_bench = ref.build_bench()
    assert len(bench) == len(ref_bench) == 60
    n_triton_orig = sum(b["prompt"].count("Triton") for b in ref_bench)
    n_triton_new = sum(b["prompt"].count("Triton") for b in bench)
    n_neptune_new = sum(b["prompt"].count("Neptune") for b in bench)
    assert n_triton_orig > 0 and n_triton_new == 0, "Triton not fully swapped"
    changed = [b["id"] for a, b in zip(ref_bench, bench)
               if a["prompt"] != b["prompt"]]
    for a, b in zip(ref_bench, bench):
        assert a["id"] == b["id"] and a["tuple"] == b["tuple"] \
            and a["phrasing"] == b["phrasing"] and a["domain"] == b["domain"], \
            "non-surface structural drift"
        assert b["prompt"] == a["prompt"].replace("Triton", "Neptune"), \
            f"surface drift beyond the swap in {b['id']}"
    print(f"items changed by the swap: {len(changed)} "
          f"(Triton occurrences in original prompts: {n_triton_orig})")

    # 2. G0 (reads bench items only — runs verbatim on the delta bench)
    g0 = ref.verify_g0(bench)
    print("G0 PASS:", {k: (v if k != "strata" else v) for k, v in g0.items()
                       if k != "pin"})

    # 3. G1' — the gate that killed EXP144 — must now read 240/240
    n_occ, n_single, table = g1prime_cover(tokenizer, bench)
    bad = {n: t for n, t in table.items()
           if t["single_token"] < t["occurrences"]}
    print(f"G1' cover: {n_single}/{n_occ} (bar 240/240); "
          f"failing entities: {sorted(bad)}")
    assert n_occ == 240 and n_single == 240 and not bad, \
        f"G1' STILL FAILING: {sorted(bad)}"
    neptune_ids = sorted(table["Neptune"]["token_ids_seen"])
    print(f"Neptune token id(s) under GPT-2 BPE: {neptune_ids}")

    # 4. Canonical pin (same serialization as the committed procedure)
    pin = ref.bench_sha256(bench)
    assert len(pin) == 64 and all(c in "0123456789abcdef" for c in pin)
    print("delta bench pin:", pin)

    # 5. G2 oracle diagnostic on the delta bench (delta vocab).
    # A 1:1 name swap at fixed indices preserves all set-overlap structure,
    # so the oracle must reproduce the committed values bit-for-bit.
    obs, p = ref.stratified_permutation_p(
        bench, oracle_expected_accuracy_s72b, ref.PERM_B_ORACLE)
    print(f"G2 oracle on delta bench: accuracy={obs:.6f}, p={p:.6f} "
          f"(committed: 0.060715, p=0.531247)")
    assert abs(obs - 0.06071548821548822) < 1e-9, "oracle drifted"
    assert abs(p - 0.5312468753124687) < 1e-9, "oracle p drifted"
    assert p >= 0.05, "G2 gate FAIL"

    # 6. Balance verification (documented)
    from collections import Counter
    tc = Counter((b["domain"], b["ent"]) for b in bench)
    assert len(tc) == 20 and all(v == 3 for v in tc.values())
    ph = Counter(b["phrasing"] for b in bench)
    assert ph["A-first"] == 30 and ph["C-first"] == 30
    print("balance: 60 items, 20 entities x3 as target, 30/30 phrasing")

    # 7. Write pinned artifacts
    bench_path = os.path.join(OUT_DIR, "S7-2b_BENCH_2026-10-05.json")
    with open(bench_path, "w") as f:
        json.dump(bench, f, sort_keys=True, separators=(",", ":"),
                  ensure_ascii=True)
    g0_out = dict(g0)
    g0_out["strata"] = {f"{d}/{p}": v for (d, p), v in g0["strata"].items()}
    manifest = {
        "derivation": "S7-2b_build_bench_2026-10-05.py",
        "delta_vs_committed": "PLANET_VOCAB[8]: 'Triton' -> 'Neptune' "
                              "(single documented change)",
        "replacement": REPLACEMENT,
        "replacement_token_ids_gpt2_bpe": neptune_ids,
        "bench_sha256": pin,
        "n_items": 60,
        "g0": g0_out,
        "g1prime": f"{n_single}/{n_occ}",
        "g2_oracle_accuracy": obs,
        "g2_permutation_p": p,
        "derived_from_committed_pin":
            "9be8162633fe19aa2a924440d8ba158c1cc4e734c1f2a554a01a27e459f47fc4",
        "tokenizer": "gpt2 @ 607a30d783dfa663caf39e06633721c8d4cfcd7e "
                     "(tokenizer files only; no weights)",
        "date": "2026-10-05",
    }
    manifest_path = os.path.join(OUT_DIR, "S7-2b_BENCH_MANIFEST_2026-10-05.json")
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=1, sort_keys=True)
    # character-by-character self-verification of the pin
    assert ref.bench_sha256(json.load(open(bench_path))) == pin
    print(f"wrote {bench_path}")
    print(f"wrote {manifest_path}")
    print("PIN (character-verified):", pin)


if __name__ == "__main__":
    main()
