# EXP090 execution bundle — BUILD NOTES

**Bundle:** `experiments/runs/EXP090_clm8b_falsifier_v2/`
**Signed protocol:** `experiments/protocols/EXP090_CLM8B_ADAPTATION_V2_PREREG_SIGNED.md`
(SHA-256 `440dd6a53ab88a199c88a57e629768aa9414cc1f9d907b33e2ab6019aa79c0ab`; the
runner refuses to run if this digest does not match.)
**Status:** BUILT + TESTED (36/36 unit tests PASS, numpy-only). Real execution
NOT run (awaits independent bundle review + CEO execution clearance).

## Lineage

EXP089 (`experiments/protocols/EXP089_CLM8B_ADAPTATION_PREREG_SIGNED.md`,
immutable) is SUPERSEDED-BY-EXP090 for execution purposes: its §6 executor
contract (byte-for-value `(ent, typ)` reproduction of the smoke archive) was
ruled CONFIRMED UNSATISFIABLE by binding independent review (LOG-345). EXP089
remains on the record; its bundle modules were adapted here with ONE change:
the §6 bench contract. Everything else — question, bar, guards, decision
tree, scope fence — is identical.

## Files

| File | Purpose |
|---|---|
| `benchmark_exp090.py` | N=60 benchmark builder: verbatim port of the repaired EXP077 benchmark block (byte-identical output to the LOG-345-reviewed EXP089 builder — pinned by `test_bench_matches_exp089_builder_byte_identical`) + `state_text_of()` (premise-only state text, §6) + `assert_archive_hash()` (the §6 PROVENANCE PIN: SHA-256 of `exp077_instance_records.json` must equal `47281cd3…0585`; mismatch → RUN-INVALID) + `assert_phrasing_balance()` (G3). Adds only the `phrasing` provenance field. EXP077's support-prompt anti-cheat assert intentionally NOT ported (EXP090 uses no support prompts). The EXP089 byte-reproduction guard is STRUCK and does NOT exist in this module (`test_struck_guard_absent` pins its absence). Caveat 6 (load-bearing): no "exactly the bench EXP077 ran" claim. |
| `extract_state_embeddings.py` | Frozen Pythia-410m layer-20 final-token hidden-state extraction (CPU, read-only, `device_map="cpu"` pinned literally). torch/transformers imported lazily. Enforces G1 (single-token assert, EXP075 guard), G2 (state_dict SHA-256 pre/post vs LOG-331 hash `ec276abe…e0ed`, Δθ=0), G3 (30/30 phrasing), and the §6 provenance pin (asserted BEFORE any weight access, in BOTH mock and real modes — it is a file check, so mock makes no weaker claim). `--mock` produces seeded synthetic unit vectors (never touches weights). |
| `score_exp090.py` | Pure-numpy cosine scoring + §7.1 TOTAL decision tree + G4 instrument gate + exact binomial upper tail. Ties (exact float equality) break toward C (foil), counted. Report stamped with execution mode (`"mock"|"real"|"unknown"`, carried forward from LOG-345 F1). |
| `run_exp090.py` | CLI entry. Refuses: unsigned/mismatched protocol (digest guard vs `440dd6a5…`), forbidden flags (`--train/--gpu/--cuda/--finetune/…`), real run without `--ceo-clearance`. `--mock` = synthetic end-to-end. Exit codes: 0 ran, 2 refused, 3 RUN-INVALID. |
| `test_exp090.py` | 36 unit tests, ALL PASS (see §Tests). |
| `manifest.json` | Machine-readable build record (hashes, budget, lineage). |

## Tests (36/36 PASS, `python3 -m unittest test_exp090`)

- §6 bench contract (NEW): builder output byte-identical to the LOG-345-reviewed EXP089 builder; two builds byte-identical (determinism); struck byte-reproduction guard absent; archive provenance pin passes on the real archive (`47281cd3…0585`); pin REFUSES on a tampered archive (RUN-INVALID, no embeddings written); phrasing balance exactly 30/30; state text excludes question/options.
- Verdict boundaries: 38/60 clean → CONTINUE; 39/60 → CONTINUE; 60/60 → CONTINUE; 37/60 → KILL; 30/60 → KILL; 0/60 → KILL; 38/60 with a split at exactly 0.5 → PIVOT; 38/60 opposite tilts → PIVOT; 40/60 with a split <0.5 → PIVOT.
- Bar sharpness: exact P(X≥38)=0.0259469… (registers as 0.0260 at 3dp per protocol §7); P(X≥37)=0.0462; independently recomputed via math.comb.
- G4: all-120-identical cosines → RUN-INVALID (never KILL); healthy spread passes.
- Ties: exact tie → foil chosen, tie counted.
- G1: multi-token entity → RUN-INVALID; single-token passes.
- G2: hash-mismatch → RUN-INVALID; match path passes (monkeypatched); determinism + key-order stability verified.
- Runner: refuses without `--ceo-clearance` (exit 2); refuses `--gpu/--train/--cuda/--finetune` (exit 2); signed-protocol digest guard passes; `--mock` end-to-end produces a full report.

## Design note (honest record)

During adaptation, the implementer caught a transcription bug of its own:
the 3-hop items were first written with `"C": C` instead of the verbatim
`"C": D_ent` (caught by the byte-identity check against the EXP089 builder,
fixed before testing). This is exactly why the byte-identity test exists.

## Real-execution command (after independent bundle review + CEO clearance)

```bash
cd experiments/runs/EXP090_clm8b_falsifier_v2
python3 run_exp090.py --out-dir out --ceo-clearance
```

Requires: CPU torch + transformers installed; the LOG-331 snapshot at
`experiments/runs/EXP086_amplifier/weights/pythia-410m/` (present, 911 MB
safetensors, NOT modified by this bundle). Budget: $0, ~1–2 h CPU.
No GPU contact. No known blockers: the §6 contract is satisfiable.
