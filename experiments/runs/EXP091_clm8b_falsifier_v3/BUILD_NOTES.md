# EXP091 execution bundle — BUILD NOTES

**Bundle:** `experiments/runs/EXP091_clm8b_falsifier_v3/`
**Signed protocol:** `experiments/protocols/EXP091_CLM8B_ADAPTATION_V3_PREREG_SIGNED.md`
(SHA-256 `747bb6a5722e8478f57b645cad93b9fd54902271bd3f8a64da9a4e24236f417b`; the
runner refuses to run if this digest does not match.)
**Status:** BUILT + TESTED (47/47 unit tests PASS, numpy-only). Real execution
NOT run (awaits independent bundle review + CEO execution clearance).

## Lineage

EXP090 (`experiments/protocols/EXP090_CLM8B_ADAPTATION_V2_PREREG_SIGNED.md`,
immutable) is SUPERSEDED-BY-EXP091 for execution purposes: its real execution
(LOG-354) exited RUN-INVALID at the G1 bare-word single-token gate ('Mars' →
2 tokens bare; 7/10 entities multi-token bare). EXP090 remains on the record;
its bundle modules were adapted here with ONE design change: G1 → G1'
(in-context single-token verification) plus the §0 action-text coupling it
constrains. Everything else — question, bar, §7.1 tree, G2/G3/G4, Law #7,
Law #13 pins, refusal gates, scope fence — is identical.

## Files

| File | Purpose |
|---|---|
| `benchmark_exp091.py` | N=60 benchmark builder: verbatim port of the EXP090 builder (byte-identical output to the LOG-345-reviewed EXP089 builder — pinned by `test_bench_matches_exp089_builder_byte_identical`) + `state_text_of()` (premise-only state text, §6) + `action_text_of()` (the §0 coupling: `" "+name`, the entity's natural single-token BPE form) + `assert_archive_hash()` (the §6 PROVENANCE PIN) + `assert_phrasing_balance()` (G3) + **G1' machinery**: `verify_g1_prime(tokenizer)` (executes a tokenizer over all 60 built prompts — offset-mapping cover check; every A/C occurrence must be covered by exactly one token; fails loud), `write_g1prime_verification()` (records the build-time artifact), `check_g1prime_artifact()` (re-verifies the artifact: present, 240/240, bound to the current bench hash). Adds only the `phrasing` provenance field. EXP077's support-prompt anti-cheat assert intentionally NOT ported. The EXP089 byte-reproduction guard is STRUCK and does NOT exist here. Caveat 6 (load-bearing): no "exactly the bench EXP077 ran" claim. |
| `g1prime_verification.json` | Build-time G1' verification artifact: the real Pythia (GPT-NeoX) tokenizer executed over all 60 built prompts (offset-mapping cover check), 2026-09-25 — **240/240 A/C occurrences single-token**; per-entity counts Mars 42, Venus 14, Jupiter 8, Saturn 16, Mercury 40, Iron 42, Gold 14, Silver 8, Bronze 16, Steel 40; token ids ĠMars[13648], ĠVenus[36210], ĠJupiter[34434], ĠSaturn[38876], ĠMercury[36091], ĠIron[17826], ĠGold[7284], ĠSilver[16309], ĠBronze[49134], ĠSteel[19727] — character-identical to the signed-protocol §6 table. Bound to the bench via `bench_sha256`. |
| `extract_state_embeddings.py` | Frozen Pythia-410m layer-20 final-token hidden-state extraction (CPU, read-only, `device_map="cpu"` pinned literally). torch/transformers imported lazily. Enforces G1' at two points: (i) `verify_g1_prime(tokenizer)` over all 60 built prompts at extraction startup, BEFORE any weight access; (ii) `guard_g1_prime_action_texts()` asserts `encode(" "+A)` / `encode(" "+C)` single-token for all 10 entities (the embedded material). Action texts embedded as `" "+A` / `" "+C` (§0 coupling). G2 (state_dict SHA-256 pre/post vs LOG-331 hash), G3 (30/30), §6 provenance pin (BEFORE weight access, both modes). `--mock` is numpy-only and re-verifies the build-time G1' artifact instead of executing the tokenizer. |
| `score_exp091.py` | Pure-numpy cosine scoring + §7.1 TOTAL decision tree + G4 instrument gate + exact binomial upper tail. Logic BYTE-IDENTICAL to the EXP090 scorer (only names changed). Ties break toward C (foil), counted. Report stamped with execution mode (`"mock"|"real"|"unknown"`). |
| `run_exp091.py` | CLI entry. Refuses: unsigned/mismatched protocol (digest guard vs `747bb6a5…`), forbidden flags (`--train/--gpu/--cuda/--finetune/…`), real run without `--ceo-clearance`. `--mock` = synthetic end-to-end. Exit codes: 0 ran, 2 refused, 3 RUN-INVALID. |
| `test_exp091.py` | 47 unit tests, ALL PASS (see §Tests). |
| `requirements.txt` | Full CPU dependency list incl. `accelerate>=1.0.0` — the LOG-331 deviation fix is pinned at BUILD time this time (EXP090 needed it added post-hoc after its launch crashed). |
| `manifest.json` | Machine-readable build record (hashes, G1' verification record, budget, lineage). |

## Tests (47/47 PASS, `python3 -m unittest test_exp091`)

- §6 bench contract (carried): byte-identical to the EXP089 builder; deterministic; struck guard absent; archive pin passes/refuses; provenance pin fires in mock; 30/30 phrasing; state text excludes question/options.
- **G1' (NEW, the design change):** `verify_g1_prime` passes 240/240 via the fake tokenizer; per-entity counts pinned to the registered §6 table (Mars 42 … Steel 40); NEGATIVE: multi-token span → RUN-INVALID; NEGATIVE: unstable token id → RUN-INVALID; `action_text_of` = spaced form; action-text guard passes/fails correctly; build-time artifact present, 240/240, verdict SATISFIED, `bench_sha256`-bound, token ids character-identical to the protocol table; tampered artifact → RUN-INVALID; stale (bench-mismatched) artifact → RUN-INVALID; `--mock` requires a valid artifact (no embeddings written on failure).
- Verdict boundaries: 38/60 → CONTINUE; 39/60, 60/60 → CONTINUE; 37/60, 30/60, 0/60 → KILL; split-at-0.5 / opposite-tilts / split-below-half → PIVOT.
- Bar sharpness: P(X≥38)=0.0259469… (0.0260 at 3dp); P(X≥37)=0.0462.
- G4: deaf instrument → RUN-INVALID; healthy passes. Ties → foil, counted.
- G1-legacy / G2 / G3 guard logic; runner refusals (no clearance → 2; forbidden flags → 2; digest guard passes); `--mock` end-to-end → full report; mode stamp mock/unknown.

## Design note (honest record)

During testing, the implementer's own negative-path test caught a real bundle
bug: `extract_mock` called `check_g1prime_artifact()` without wrapping the
benchmark module's `RunInvalid` into the extraction module's `RunInvalid` —
the runner's `except RunInvalid` would not have caught it, turning a guarded
RUN-INVALID into an uncaught traceback (exit ≠ 3). Fixed by wrapping, mirroring
the existing `guard_archive_provenance()` pattern; the test now passes. This is
exactly why the negative-path tests exist.

## Real-execution command (after independent bundle review + CEO clearance)

```bash
cd experiments/runs/EXP091_clm8b_falsifier_v3
python3 run_exp091.py --out-dir out --ceo-clearance
```

Requires: CPU torch + transformers + accelerate installed (see
requirements.txt); the LOG-331 snapshot at
`experiments/runs/EXP086_amplifier/weights/pythia-410m/` (present, 911 MB
safetensors, NOT modified by this bundle). Budget: $0, ~1–2 h CPU.
No GPU contact. No known blockers: the G1' contract is verified satisfiable
by real-tokenizer execution (240/240).
