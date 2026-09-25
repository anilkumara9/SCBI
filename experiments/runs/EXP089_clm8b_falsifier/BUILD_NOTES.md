# EXP089 execution bundle — BUILD NOTES

**Bundle:** `experiments/runs/EXP089_clm8b_falsifier/`
**Signed protocol:** `experiments/protocols/EXP089_CLM8B_ADAPTATION_PREREG_SIGNED.md`
(SHA-256 `87f2c47b7cbcec3db98cd88d7240b95ce7f49af9039aa0ae4ec251a2714c24cb`; the
runner refuses to run if this digest does not match.)
**Status:** BUILT + TESTED (28/28 unit tests PASS, numpy-only). Real execution
NOT run (awaits independent bundle review + CEO execution clearance).

## Files

| File | Purpose |
|---|---|
| `benchmark_exp089.py` | N=60 benchmark builder ported VERBATIM from `experiments/runs/exp077/run_exp077.py` (§3 block; same vocab lists, index arrays, prompt templates) + `state_text_of()` (premise-only state text, §6) + `verify_against_instance_records()` + `assert_phrasing_balance()` (G3). Adds only the `phrasing` provenance field ("A-first"/"C-first") required by §6 G3/§7.1, following EXP077's own "plus provenance fields" practice. EXP077's support-prompt anti-cheat assert intentionally NOT ported (EXP089 uses no support prompts). |
| `extract_state_embeddings.py` | Frozen Pythia-410m layer-20 final-token hidden-state extraction (CPU, read-only). torch/transformers imported lazily. Enforces G1 (single-token assert, EXP075 guard), G2 (state_dict SHA-256 pre/post vs LOG-331 hash `ec276abe…e0ed`, Δθ=0), G3 (30/30 phrasing). `--mock` produces seeded synthetic unit vectors (never touches weights). |
| `score_exp089.py` | Pure-numpy cosine scoring + §7.1 TOTAL decision tree + G4 instrument gate + exact binomial upper tail. Ties (exact float equality) break toward C (foil), counted. |
| `run_exp089.py` | CLI entry. Refuses: unsigned/mismatched protocol (digest guard), forbidden flags (`--train/--gpu/--cuda/--finetune/…`), real run without `--ceo-clearance`. `--mock` = synthetic end-to-end. Exit codes: 0 ran, 2 refused, 3 RUN-INVALID. |
| `test_exp089.py` | 28 unit tests, ALL PASS (see §Tests). |
| `manifest.json` | Machine-readable build record (hashes, budget, blockers). |

## Tests (28/28 PASS, `python3 -m unittest test_exp089`)

- Benchmark: length 60; phrasing balance exactly 30/30; state text excludes question/options.
- Verdict boundaries: 38/60 clean → CONTINUE; 39/60 → CONTINUE; 60/60 → CONTINUE; 37/60 → KILL; 30/60 → KILL; 0/60 → KILL; 38/60 with a split at exactly 0.5 → PIVOT; 38/60 opposite tilts → PIVOT; 40/60 with a split <0.5 → PIVOT.
- Bar sharpness: exact P(X≥38)=0.0259469… (registers as 0.0260 at 3dp per protocol §7); P(X≥37)=0.0462; independently recomputed via math.comb.
- G4: all-120-identical cosines → RUN-INVALID (never KILL); healthy spread passes.
- Ties: exact tie → foil chosen, tie counted.
- G1: multi-token entity → RUN-INVALID; single-token passes.
- G2: hash-mismatch → RUN-INVALID; match path passes (monkeypatched); determinism + key-order stability verified.
- Runner: refuses without `--ceo-clearance` (exit 2); refuses `--gpu/--train/--cuda/--finetune` (exit 2); signed-protocol digest guard passes; `--mock` end-to-end produces a full report.

## ⚠️ KNOWN BLOCKER (protocol-level) — real execution will exit RUN-INVALID

The signed protocol §6 requires the ported builder's (ent, typ) sequence to match
`exp077_instance_records.json` byte-for-value, else RUN-INVALID. **This check
cannot pass with the current repo state**, and the bundle faithfully implements
the refusal:

- Repo builder (repaired, EXP078-port): `(Mars,planet), (Venus,planet), (Jupiter,planet), …`
- Smoke archive: `(Mars,planet)×6, (Venus,planet)×6, …` — 12/60 (ent,typ) matches; first mismatch at index 1.
- Forensics: the archive was produced by the pre-repair benchmark builder. The original zip (`286c9576…`) is superseded and not on disk; the on-disk zip (`936dbce4…`) embeds the repaired runner (`ea740625…`, byte-identical bench block to the repo). No retained code reproduces the archive's prompts (which were never archived — `instance_records.json` stores only ent/typ/correct flags).
- This is the already-adjudicated LOG-3994 (CEO: pin the SMOKE bench) / LOG-4238 (G4 FATAL on the same mismatch) provenance break, independently reproduced by this bundle's guard.

**What this means:** the bundle is correct and complete, but REAL execution is
blocked until CEO/Mentor adjudication — e.g. a new experiment number pinning a
reconstructible bench, or recovery of the smoke-bench prompts. Mock mode
deliberately skips the archive byte-match (documented in code; mock makes no
archive claim) so the scoring pipeline remains smoke-testable.

## Real-execution command (after independent bundle review + CEO clearance)

```bash
cd experiments/runs/EXP089_clm8b_falsifier
python3 run_exp089.py --out-dir out --ceo-clearance
```

Requires: CPU torch + transformers installed; the LOG-331 snapshot at
`experiments/runs/EXP086_amplifier/weights/pythia-410m/` (present, 911 MB
safetensors, NOT modified by this bundle). Budget: $0, ~1–2 h CPU.
Expected first outcome under current repo state: RUN-INVALID (see blocker).
