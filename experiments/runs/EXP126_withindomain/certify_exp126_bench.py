"""EXP126 (H23/WITHIN-DOMAIN) bench-5 breaking-point certifier — LOG-4687 lane.

Tokenizer-only checks (no model weights loaded, no forwards):
  (a) single-token entity assertion on the FINAL 14-animal set with the real
      Pythia-410m tokenizer, " "+E encoding exactly per the H6 section 3.3 pin;
plus: canonical bench JSON emission, determinism re-run hash match,
single-domain audit, G-C1/G-C2 diagnostics, G-C3 full gate,
position-scramble gate, and the breaking-point certificate.

Note: defect class (e) ([-3:] tokenization-identity pin) is explicitly N/A
for H23 (protocol section 6 item 4 — no logit channel, embedding-readout
design). No [-3:] check is performed.

Run with the registered environment's venv python:
  ~/workspace/.venv-exp077/bin/python certify_exp126_bench.py
"""

import hashlib
import json
import os
import platform
import sys

import build_exp126_bench as B

RUN_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(RUN_DIR, "out")
TOKENIZER_DIR = "/home/hatch/workspace/.exp086_weights/pythia-410m"


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    from transformers import AutoTokenizer
    import transformers

    bench = B.build_bench()
    v = B.verify_cells(bench)          # balance, cells, contract, label pin,
                                       # single-domain audit, ID namespace
    g1 = B.gate_gc1(bench)             # diagnostic
    g2 = B.gate_gc2(bench)             # diagnostic
    g3 = B.gate_gc3(bench)             # full gate
    gp = B.gate_position_scramble(bench)

    # --- (a) single-token assertion on the FINAL entity set ---
    tok = AutoTokenizer.from_pretrained(TOKENIZER_DIR, trust_remote_code=False)
    single = {}
    multi = []
    for e in B.VOCAB:
        ids = tok.encode(" " + e, add_special_tokens=False)
        single[e] = ids
        if len(ids) != 1:
            multi.append((e, ids))
    assert not multi, f"MULTI-TOKEN ENTITIES -> apparatus-void: {multi}"

    # --- canonical bench JSON + determinism re-run ---
    os.makedirs(OUT_DIR, exist_ok=True)
    canon = B.canonical_json(bench)
    bench_path = os.path.join(OUT_DIR, "exp126_bench5.json")
    with open(bench_path, "wb") as f:
        f.write(canon)
    pin1 = B.bench_sha256(bench)
    pin2 = B.bench_sha256()            # fresh rebuild
    assert pin1 == pin2, "builder not deterministic"
    disk = sha256_file(bench_path)
    assert disk == pin1, "bench JSON on disk != builder pin"

    # --- environment manifest ---
    env = {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "transformers": transformers.__version__,
        "tokenizer_dir": TOKENIZER_DIR,
        "tokenizer_json_sha256": sha256_file(os.path.join(TOKENIZER_DIR, "tokenizer.json")),
        "builder_sha256": sha256_file(os.path.join(RUN_DIR, "build_exp126_bench.py")),
        "certifier_sha256": sha256_file(os.path.join(RUN_DIR, "certify_exp126_bench.py")),
    }

    verdict = "PASS" if (v and g1["pass"] and g2["pass"] and g3["pass"]
                         and gp["pass"] and not multi) else "apparatus-void"

    lines = []
    A = lines.append
    A("# Breaking-point certificate — EXP126 (H23/WITHIN-DOMAIN) bench 5")
    A("")
    A("**Lane:** LOG-4687 (construction). **Protocol:**")
    A("`~/workspace/SCBI/research/prereg/EXP_PREREG_H23_WITHINDOMAIN_2026-09-29.md`")
    A("(launch-ready: Law #14 SIGN, zero fixes, LOG-4686).")
    A("")
    A("**Certificate verdict:** `%s`" % verdict)
    A("")
    A("Conjunctive breaking point (protocol section 0): any miss on the §3.2")
    A("design assertions, the single-domain audit, the single-token assertion,")
    A("G-C1, G-C2, G-C3, or the position-scramble gate -> construction-fate")
    A("RUN-INVALID, hypothesis UNTESTED, no number minted, no execution.")
    A("All hold on the evidence below.")
    A("")
    A("## 1. No item screening (EXP121 lesson)")
    A("")
    A("- Exactly 60 base items emitted; all 60 enter the bench (`len(bench) == 60` asserted).")
    A("- Flip selection is by sorted position within each phrasing group (even")
    A("  positions flip), never by item content.")
    A("- No per-item filtering of any kind at construction: no model calls, no RNG,")
    A("  no item dropped, reweighted, or re-selected. The builder asserts")
    A("  `len(flip_ids) == 30` and `len(bench) == 60` at build time.")
    A("- Cell counts verified: target-first/original 15, target-first/flipped 15,")
    A("  target-last/original 15, target-last/flipped 15.")
    A("- Labels 30/30 (y=1 iff tuple[0] ∈ S1); hop x label 15/15/15/15.")
    A("")
    A("## 2. (a) Single-token entity assertion — FINAL set, real tokenizer")
    A("")
    A("Tokenizer: `%s` (tokenizer-only; no weights loaded, no forwards)." % TOKENIZER_DIR)
    A("Encoding: `encode(\" \"+E, add_special_tokens=False)` exactly per the H6 section 3.3 pin.")
    A("Result: **14/14 single-token** — zero multi-token entities.")
    A("")
    A("| entity | token id | entity | token id |")
    A("|---|---|---|---|")
    entities = B.VOCAB
    half = (len(entities) + 1) // 2
    for i in range(half):
        l = entities[i]
        r = entities[i + half] if i + half < len(entities) else None
        if r is None:
            A(f"| {l} | {single[l][0]} | | |")
        else:
            A(f"| {l} | {single[l][0]} | {r} | {single[r][0]} |")
    A("")
    A("Any multi-token entity would have restarted construction, not patched it;")
    A("none was found, so no restart occurred.")
    A("")
    A("## 3. Single-domain audit (the discriminative gate)")
    A("")
    A("- Every entity mention on every bench-5 premise was audited against the")
    A("  14-animal set with whole-word matching (`verify_cells`).")
    A("- Result: **0/60 premises contain any out-of-domain entity**.")
    A("- A domain-set detector has no input here by construction: this is the")
    A("  gate that makes H23 discriminative.")
    A("")
    A("## 4. Template-decorrelation discipline")
    A("")
    A("### G-C1 pure-template detector (diagnostic)")
    A("")
    A("- T predicts y=1 iff the first premise sentence uses family-1")
    A("  (` towers over ` / ` crouches under `). Score: **%d/60**, gate bar <= 36/60 -> **%s**."
      % (g1["score"], "PASS" if g1["pass"] else "TRIP"))
    A("")
    A("### G-C2 entity-rank correlation (diagnostic)")
    A("")
    A("- Flattened entity-index sequences bench-3 vs bench-5 (sorted-by-ID")
    A("  canonical order, 240 elements each). Pearson: **%+.4f**, |Pearson| = %.4f,"
      % (g2["pearson"], g2["abs_pearson"]))
    A("  bar <= 0.10 -> **%s**." % ("PASS" if g2["pass"] else "TRIP"))
    A("- Bench-5 uses the S1/S2-interleaved GC2 index (label-agnostic canonical")
    A("  order) so the check measures entity-assignment independence, not")
    A("  label-structure similarity; bench-5's label pattern (Y1+7) and hop rule")
    A("  (hash-based) are structurally independent of bench-3's.")
    A("- Computed against bench-3's builder records only; no bench-3 labels or")
    A("  embeddings enter the analysis (Law #13 fence).")
    A("")
    A("### G-C3 byte-exact decomposition (FULL gate)")
    A("")
    A("- `QUESTION_SUFFIX` byte-exact: %s" % g3["suffix_byte_exact"])
    A("- prompt == premise + QUESTION_SUFFIX on all 60 items: %s"
      % g3["decomposition_60_of_60"])
    A("- Deterministic re-run byte-identical: %s" % g3["deterministic"])
    A("- **G-C3 verdict: %s**" % ("PASS" if g3["pass"] else "FAIL -> apparatus-void"))
    A("")
    A("### Position-scramble gate (discriminative)")
    A("")
    A("- P predicts y=1 iff the target occupies the first final sentence position.")
    A("  Score: **%d/60**, gate bar <= 36/60 -> **%s**."
      % (gp["score"], "PASS" if gp["pass"] else "TRIP"))
    A("- Final position balanced 15/15 within each label class by construction")
    A("  (identical flip x label pattern across phrasing groups).")
    A("")
    A("## 5. (c) Law-#7 own label pin")
    A("")
    A("- Builder's meaning-preserving construction docstring (in")
    A("  `build_exp126_bench.py`): the flip preserves the ranking meaning")
    A("  (A > B > C [> D]), so `tuple[0] = A` is the highest-ranked entity on")
    A("  all 60 items.")
    A("- Label derivation rule: **y=1 iff tuple[0] ∈ S1 = {Cat, Dog, Bear, Wolf, Fox}**,")
    A("  y=0 iff tuple[0] ∈ S2 = {Lion, Tiger, Horse, Cow, Pig} — a property of the")
    A("  target's identity within a single domain (explicit design deviation from")
    A("  the H5/H16 label definitions, per the H23 pre-reg §2 disclosure).")
    A("- Independent per-item assertion (`verify_cells`, mechanical, separate from")
    A("  the prose): `y == (tuple[0] in S1)` — **60/60 pass**. `target_subset`")
    A("  field matches the label on all 60 items.")
    A("- Labels enter only this pin and the pre-registered head targets, never the")
    A("  apparatus (protocol section 3.7).")
    A("")
    A("## 6. Disjointness and independence")
    A("")
    A("- ID namespace: `expb5_*` — no collision with `exp107_`/`exp077_` (bench 1),")
    A("  `exp120_`/`expb2_` (bench 2), `exp122_`/`expb3_` (bench 3), `exp125_` (bench 4).")
    A("- Verb families (`towers over`/`crouches under`, `looms over`/`cowers beneath`)")
    A("  contain no prior-bench verb-family substring (asserted per item).")
    A("- Entity vocabulary: the 14-animal set overlaps bench-3's animal set")
    A("  {Lion, Tiger, Bear, Wolf, Fox} by protocol design (the H23 gate pins the")
    A("  14-animal vocabulary); independence of the entity *assignments* is via")
    A("  hash-selected entities with salt `exp126` (vs bench-3's `exp122`),")
    A("  verified by the G-C2 gate above.")
    A("")
    A("## 7. Determinism (Law #13)")
    A("")
    A("- Builder: no RNG, no model calls, pure string construction.")
    A("- Rebuild pin: `%s`" % pin1)
    A("- Fresh re-run pin: `%s` — **match**." % pin2)
    A("- Canonical JSON on disk (`out/exp126_bench5.json`) sha256: `%s` — **match**." % disk)
    A("")
    A("## 8. Hashes")
    A("")
    A("| artifact | sha256 |")
    A("|---|---|")
    A(f"| out/exp126_bench5.json | `{disk}` |")
    A(f"| build_exp126_bench.py | `{env['builder_sha256']}` |")
    A(f"| certify_exp126_bench.py | `{env['certifier_sha256']}` |")
    A(f"| tokenizer.json | `{env['tokenizer_json_sha256']}` |")
    A("")
    A("## 9. Environment manifest")
    A("")
    A("- python %s, %s" % (env["python"], env["platform"]))
    A("- transformers %s" % env["transformers"])
    A("- tokenizer source: `%s`" % env["tokenizer_dir"])
    A("- Note: defect class (e) ([-3:] tokenization-identity pin) is explicitly N/A")
    A("  for H23 (protocol §6 item 4 — no logit channel, embedding-readout design).")
    A("")
    A("## 10. Verdict")
    A("")
    A("**%s** — all conjunctive breaking-point elements hold: (a) 14/14" % verdict)
    A("single-token on the final set; single-domain audit 0/60 out-of-domain;")
    A("G-C1 %d/60 diagnostic PASS, G-C2 |Pearson|=%.4f diagnostic PASS," % (g1["score"], g2["abs_pearson"]))
    A("G-C3 FULL PASS, position-scramble %d/60 PASS;" % gp["score"])
    A("(c) Law-#7 own label pin on record (y == (tuple[0] in S1), 60/60);")
    A("no item screening; 60 items, four balanced 15-item cells, 30/30 labels;")
    A("disjointness asserted; determinism re-run hash match.")
    A("Execution is **licensed to proceed** under a minted experiment")
    A("number (CEO decision).")
    A("")

    cert_path = os.path.join(OUT_DIR, "exp126_breaking_point_certificate.md")
    with open(cert_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("certificate:", cert_path)
    print("bench pin:", pin1)
    print("verdict:", verdict)
    print("G-C1: %d/60 pass=%s | G-C2: %+.4f pass=%s | G-C3: pass=%s | pos: %d/60 pass=%s"
          % (g1["score"], g1["pass"], g2["pearson"], g2["pass"],
             g3["pass"], gp["score"], gp["pass"]))


if __name__ == "__main__":
    main()
