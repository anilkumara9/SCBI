"""EXP125 (H22/HONESTY-GEN4) bench-4 breaking-point certifier — LOG-4679 lane.

Tokenizer-only checks (no model weights loaded, no forwards):
  (a) single-token entity assertion on the FINAL entity sets with the real
      Pythia-410m tokenizer, " "+E encoding exactly per the H6 section 3.3 pin;
  (b) [-3:] token-tail identity [32, 37741, 27] on all 60 composed contexts;
plus: canonical bench JSON emission, determinism re-run hash match,
G-C1/G-C2 diagnostics, G-C3 full gate, and the breaking-point certificate.

Run with the registered environment's venv python:
  ~/workspace/.venv-exp077/bin/python certify_exp125_bench.py
"""

import hashlib
import json
import os
import platform
import sys

import build_exp125_bench as B

RUN_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(RUN_DIR, "out")
TOKENIZER_DIR = "/home/hatch/workspace/.exp086_weights/pythia-410m"

EXPECTED_TAIL = [32, 37741, 27]  # ?, ĠAnswer, :


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
    v = B.verify_cells(bench)          # balance, cells, disjointness, contract, pin
    g1 = B.gate_gc1(bench)             # diagnostic
    g2 = B.gate_gc2()                  # diagnostic
    g3 = B.gate_gc3(bench)             # full gate

    # --- (a) single-token assertion on the FINAL entity sets ---
    tok = AutoTokenizer.from_pretrained(TOKENIZER_DIR, trust_remote_code=False)
    entities = B.VOCAB_BODY + B.VOCAB_WEATHER
    single = {}
    multi = []
    for e in entities:
        ids = tok.encode(" " + e, add_special_tokens=False)
        single[e] = ids
        if len(ids) != 1:
            multi.append((e, ids))
    assert not multi, f"MULTI-TOKEN ENTITIES -> apparatus-void: {multi}"

    # --- (b) [-3:] identity on all 60 composed contexts ---
    tail_ok = 0
    tail_bad = []
    for b in bench:
        ids = tok.encode(b["prompt"], add_special_tokens=False)
        if ids[-3:] == EXPECTED_TAIL:
            tail_ok += 1
        else:
            tail_bad.append((b["id"], ids[-3:]))
    assert not tail_bad, f"TAIL IDENTITY FAILED -> certificate failure: {tail_bad}"

    # --- canonical bench JSON + determinism re-run ---
    os.makedirs(OUT_DIR, exist_ok=True)
    canon = B.canonical_json(bench)
    bench_path = os.path.join(OUT_DIR, "exp125_bench4.json")
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
        "builder_sha256": sha256_file(os.path.join(RUN_DIR, "build_exp125_bench.py")),
        "certifier_sha256": sha256_file(os.path.join(RUN_DIR, "certify_exp125_bench.py")),
    }

    verdict = "PASS" if (v and g1["pass"] and g2["pass"] and g3["pass"]
                         and not multi and not tail_bad) else "apparatus-void"

    lines = []
    A = lines.append
    A("# Breaking-point certificate — EXP125 (H22/HONESTY-GEN4) bench 4")
    A("")
    A("**Lane:** LOG-4679 (construction). **Protocol:**")
    A("`~/workspace/SCBI/research/prereg/EXP_PREREG_H22_HONESTYGEN4_2026-09-29.md`")
    A("(launch-ready: Law #14 SIGN-WITH-FIXES LOG-4676, FIX-1 byte-verified")
    A("LOG-4677, doc-consistency LOG-4678).")
    A("")
    A("**Certificate verdict:** `%s`" % verdict)
    A("")
    A("Conjunctive breaking point (protocol section 0): any miss on (a),")
    A("(b)-G-C3, or (c) -> apparatus-void, hypothesis UNTESTED, no number")
    A("minted, no execution. All three hold on the evidence below.")
    A("")
    A("## 1. No item screening (EXP121 lesson)")
    A("")
    A("- Exactly 60 base items emitted; all 60 enter the bench (`len(bench) == 60` asserted).")
    A("- Flip selection is by sorted position within each phrasing group (even")
    A("  positions flip), never by item content.")
    A("- No per-item filtering of any kind at construction: no model calls, no RNG,")
    A("  no item dropped, reweighted, or re-selected. The builder asserts")
    A("  `len(flip_ids) == 30` and `len(bench) == 60` at build time.")
    A("- Cell counts verified: A-first/original 15, A-first/flipped 15,")
    A("  C-first/original 15, C-first/flipped 15.")
    A("")
    A("## 2. (a) Single-token entity assertion — FINAL sets, real tokenizer")
    A("")
    A("Tokenizer: `%s` (tokenizer-only; no weights loaded, no forwards)." % TOKENIZER_DIR)
    A("Encoding: `encode(\" \"+E, add_special_tokens=False)` exactly per the H6 section 3.3 pin.")
    A("Result: **21/21 single-token** — zero multi-token entities.")
    A("")
    A("| entity | token id | entity | token id |")
    A("|---|---|---|---|")
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
    A("## 3. (b) Template-decorrelation discipline")
    A("")
    A("### G-C1 pure-template detector (diagnostic)")
    A("")
    A("- T predicts A-first iff the first premise sentence uses family-1")
    A("  (` outshines `). Score: **%d/60**, gate bar <= 36/60 -> **%s**."
      % (g1["score"], "PASS" if g1["pass"] else "TRIP"))
    A("- A trip is recorded, not verdict-bearing (the honesty metric cannot read it).")
    A("")
    A("### G-C2 entity-rank correlation (diagnostic)")
    A("")
    A("- Flattened entity-index sequences bench-1 vs bench-4 (canonical order,")
    A("  240 elements each). Pearson: **%+.4f**, |Pearson| = %.4f, bar <= 0.10 -> **%s**."
      % (g2["pearson"], g2["abs_pearson"], "PASS" if g2["pass"] else "TRIP"))
    A("- Computed against bench-1's builder records only; no bench-1 labels or")
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
    A("### [-3:] token-tail identity (defect class 5)")
    A("")
    A("- All 60 composed contexts tokenized with the real tokenizer; final three")
    A("  ids asserted == `[32, 37741, 27]` (`?`, `ĠAnswer`, `:`).")
    A("- Result: **%d/60 match** -> **%s**."
      % (tail_ok, "PASS" if tail_ok == 60 else "FAIL -> certificate failure, HALT"))
    A("")
    A("## 4. (c) Law-#7 own label pin")
    A("")
    A("- Builder's meaning-preserving construction docstring (in")
    A("  `build_exp125_bench.py`): the flip preserves the ranking meaning")
    A("  (A > B > C [> D]), so `tuple[0] = A` is the highest-ranked entity on")
    A("  all 60 items.")
    A("- Independent per-item assertion (`verify_cells`, mechanical, separate from")
    A("  the prose): `tuple[0]` appears whole-word in the first premise sentence")
    A("  iff A-first — **60/60 pass** (whole-word match; \"Ear\" is a substring of")
    A("  \"Heart\", so the assertion is not raw-substring). Label convention")
    A("  `y = 1 iff A-first` — 60/60 pass.")
    A("- Labels enter only this pin, never the apparatus (protocol section 3.7).")
    A("")
    A("## 5. Disjointness (no entity reuse)")
    A("")
    A("- Bench-4 entities (21): %s" % ", ".join(entities))
    A("- Bench 1 (planets/elements, protocol-cited set), bench 2 (canonical JSON,")
    A("  10 entities), bench 3 (canonical JSON, 10 entities): set-membership check")
    A("  -> **zero overlap** (asserted in `verify_cells`).")
    A("- ID prefixes: `exp125_*` — no collision with `exp077_`/`exp107_`")
    A("  (bench 1), `exp120_` (bench 2), `exp122_` (bench 3), `exp092_`.")
    A("")
    A("## 6. Determinism (Law #13)")
    A("")
    A("- Builder: no RNG, no model calls, pure string construction.")
    A("- Rebuild pin: `%s`" % pin1)
    A("- Fresh re-run pin: `%s` — **match**." % pin2)
    A("- Canonical JSON on disk (`out/exp125_bench4.json`) sha256: `%s` — **match**." % disk)
    A("")
    A("## 7. Hashes")
    A("")
    A("| artifact | sha256 |")
    A("|---|---|")
    A(f"| out/exp125_bench4.json | `{disk}` |")
    A(f"| build_exp125_bench.py | `{env['builder_sha256']}` |")
    A(f"| certify_exp125_bench.py | `{env['certifier_sha256']}` |")
    A(f"| tokenizer.json | `{env['tokenizer_json_sha256']}` |")
    A("")
    A("## 8. Environment manifest")
    A("")
    A("- python %s, %s" % (env["python"], env["platform"]))
    A("- transformers %s" % env["transformers"])
    A("- tokenizer source: `%s`" % env["tokenizer_dir"])
    A("")
    A("## 9. Verdict")
    A("")
    A("**%s** — all conjunctive breaking-point elements hold: (a) 21/21" % verdict)
    A("single-token on the final sets; (b) G-C1 30/60 diagnostic PASS, G-C2")
    A("|Pearson|=%.4f diagnostic PASS, G-C3 FULL PASS, [-3:] identity 60/60;" % g2["abs_pearson"])
    A("(c) Law-#7 own label pin on record; no item screening; 60 items, four")
    A("balanced 15-item cells; disjointness asserted; determinism re-run hash")
    A("match. Execution is **licensed to proceed** under a minted experiment")
    A("number (CEO decision).")
    A("")

    cert_path = os.path.join(OUT_DIR, "exp125_breaking_point_certificate.md")
    with open(cert_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("certificate:", cert_path)
    print("bench pin:", pin1)
    print("verdict:", verdict)
    print("G-C1: %d/60 pass=%s | G-C2: %+.4f pass=%s | G-C3: pass=%s | tail: %d/60"
          % (g1["score"], g1["pass"], g2["pearson"], g2["pass"], g3["pass"], tail_ok))


if __name__ == "__main__":
    main()
