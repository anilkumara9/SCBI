# EXP091 — Independent Bundle Review: SIGN

**Reviewer:** Independent Law #14 Reviewer (reports DIRECTLY to the founder; verdict binding, not overridable by the CEO).
**Date:** 2026-09-25. **Logged:** LOG-359.
**Target:** `experiments/runs/EXP091_clm8b_falsifier_v3/` (bundle build LOG-358; builder claims 47/47 tests, G1' 240/240).
**Signed protocol:** `experiments/protocols/EXP091_CLM8B_ADAPTATION_V3_PREREG_SIGNED.md`.
**Draft review:** `experiments/protocols/REVIEWS/EXP091_LAW14_REVIEW_2026-09-25.md` (SIGN, LOG-356) — this review covers the BUNDLE, not the draft.

---

## Verdict: SIGN

The bundle faithfully implements the signed protocol. Clear for the CEO's execution-clearance decision. No fixes required. No further experiment number triggered.

---

## 1. Signed-protocol digest — MATCH

Recomputed SHA-256 of the signed protocol myself before anything else:

`747bb6a5722e8478f57b645cad93b9fd54902271bd3f8a64da9a4e24236f417b`

Character-identical to the registered digest. The runner's `SIGNED_PROTOCOL_DIGEST` constant matches. `git diff HEAD` on the signed file is empty (committed at `40ef66e`, LOG-357). The protocol the bundle was built against is the protocol that was reviewed and signed.

## 2. G1' implementation — verified by independent execution (the §8 standing rule)

I executed the real Pythia (GPT-NeoX) tokenizer myself
(`/home/hatch/workspace/.venv-exp077/bin/python`, snapshot
`experiments/runs/EXP086_amplifier/weights/pythia-410m/`, read-only) through the
bundle's own `verify_g1_prime()` over all 60 built prompts:

- **240/240** A/C occurrences each covered by exactly one token.
- Per-entity counts identical to the signed-protocol §6 table: Mars 42, Venus 14,
  Jupiter 8, Saturn 16, Mercury 40, Iron 42, Gold 14, Silver 8, Bronze 16, Steel 40.
- Token ids character-identical to the table: ĠMars[13648], ĠVenus[36210],
  ĠJupiter[34434], ĠSaturn[38876], ĠMercury[36091], ĠIron[17826], ĠGold[7284],
  ĠSilver[16309], ĠBronze[49134], ĠSteel[19727].

The implementation is correct, not merely the numbers: the offset-mapping cover
check requires exactly one token to overlap each whole-word entity occurrence,
that token's span to contain the entity's character span, its text (modulo the
BPE space marker) to equal the entity name, and the token id to be stable across
occurrences. Any violation raises `RunInvalid` (RUN-INVALID, never silent).

Enforcement points confirmed in `extract_state_embeddings.py`:
- (i) `verify_g1_prime(tokenizer)` runs at extraction startup **before any weight
  access** (model load happens after the G1'(i) log line);
- (ii) `guard_g1_prime_action_texts()` asserts `encode(" "+A)` / `encode(" "+C)`
  single-token for all 10 entities before the extraction loop;
- `--mock` re-verifies the build-time artifact (`check_g1prime_artifact()`):
  present, internally consistent (240/240), verdict SATISFIED, and bound to the
  current bench via `bench_sha256`. I recomputed `bench_sha256()` myself:
  `0a07b35d…0ccfe` — matches the recorded artifact. Tampered artifact → RUN-INVALID;
  stale (bench-mismatched) artifact → RUN-INVALID; both covered by passing tests.

## 3. Action-text coupling — implemented as accepted

`action_text_of(name)` returns `" "+name` (the spaced single-token BPE form).
I verified independently that `tokenizer.encode(" "+name)` yields exactly one
token whose id equals the in-prompt covering token's id for all 10 entities —
the guard constrains exactly the embedded material, which is what the LOG-356
ruling required. The extraction loop embeds `action_text_of(b["A"])` /
`action_text_of(b["C"])` — no bare-form embedding path exists in the real pipeline.

## 4. Scoring logic — byte-identical to EXP090 modulo names

Diffed `score_exp091.py` against `EXP090_clm8b_falsifier_v2/score_exp090.py`
after mechanical name substitution (`exp091→exp090`, `EXP091→EXP090`): the only
remaining differences are docstring lines (protocol filename V3 vs V2; the
byte-identicality claim paragraph, which EXP090's scorer cannot contain). All
executable logic is identical: bar 38/60 (P=0.0259469… = 0.0260 at 3dp, matching
§7), the §7.1 TOTAL tree (≥38 + both splits strictly >0.5 → CONTINUE; ≤37 →
KILL; else PIVOT), G4 `max−min < 1e-4` → RUN-INVALID, ties break toward the foil
and are counted, per-item margin distribution reported.

## 5. Guards, pins, refusal gates — all present as registered

- **Law #13:** `model.eval()` explicit before extraction, `torch.no_grad()`
  around ALL extraction, `requires_grad_(False)` on all parameters,
  `device_map="cpu"` literal in `from_pretrained`. ✓
- **G2:** state_dict SHA-256 pre AND post extraction vs the LOG-331 hash
  `ec276abe…e0ed`; mismatch → RUN-INVALID. (This exact code passed the
  pre-extraction hash check against the real snapshot at LOG-354.) ✓
- **G3:** `assert_phrasing_balance` → exactly 30/30 on the real builder. ✓
- **§6 provenance pin:** archive SHA-256 asserted before any weight access in
  both modes; I recomputed the archive hash myself: `47281cd3…0585` — matches. ✓
- **Refusals** (`run_exp091.py`): unsigned/mismatched protocol digest → exit 2;
  forbidden flags (`--train/--gpu/--cuda/--finetune/…`) → exit 2; real run
  without `--ceo-clearance` → exit 2. Exit codes 0/2/3 as registered. ✓
- **Mode stamp:** report carries `"mode": "mock"|"real"|"unknown"`; mock
  hardcodes `"mock"`; the F1 LOG-345 requirement is satisfied. ✓
- **Budget/scope:** CPU-only, no GPU flags, `local_files_only=True`, snapshot
  on disk — no network weight downloads. ✓

## 6. Test suite — re-run independently: 47/47 PASS

`python3 -m unittest test_exp091` → `Ran 47 tests … OK` (numpy-only).
`--mock` smoke test via `run_exp091.py` runs end-to-end: verdict KILL on random
mock embeddings (n=26/60 — expected), report stamped `"mode": "mock"`.

The G1' negative paths are genuinely exercised: multi-token span → RUN-INVALID,
unstable token id → RUN-INVALID, tampered/stale artifact → RUN-INVALID, mock
with invalid artifact → RUN-INVALID before any embedding is written. Per-entity
counts are pinned to the registered §6 table in code, so bench drift breaks the
build loudly.

**Builder's honest build note verified:** `extract_mock` previously called
`check_g1prime_artifact()` without wrapping the benchmark module's `RunInvalid`,
which would have escaped the runner's `except RunInvalid` as an uncaught
traceback (exit ≠ 3). The fix (wrapping, mirroring `guard_archive_provenance()`)
is correct and complete — `test_mock_requires_valid_g1prime_artifact` passes,
and the same wrap pattern is applied consistently to the archive pin.

## 7. Integrity — no leakage, nothing else modified

- **requirements.txt** pins `accelerate>=1.0.0` at build time (the LOG-331
  deviation that killed EXP090's launch is fixed here, not post-hoc). Remaining
  deps (numpy, torch CPU, transformers, safetensors) cover every import in the
  bundle (torch/transformers lazy). No missing dependency. The venv the CEO
  will use already has accelerate 1.15.0 installed — verified importable.
- **EXP090 bundle unmodified:** all six files' SHA-256 match its own manifest's
  `file_sha256` record. The EXP091 build touched nothing outside its own directory.
- **EXP077 artifacts unmodified:** archive hash recomputed `47281cd3…0585` —
  character-identical to the §6 pin.
- **No EXP089/EXP090 logic leakage:** the only cross-references are
  lineage/provenance documentation (the port chain) and the explicitly struck
  byte-reproduction guard. The legacy bare-word `check_single_token_entity`
  is retained as explicitly-documented dead code for unit-test lineage coverage
  only — not on any execution path (see O1).

## 8. Observations (not fixes)

- **O1:** `check_single_token_entity` (the legacy bare-word G1 that killed
  EXP090's execution) remains in `extract_state_embeddings.py`, used only by
  unit tests. It is clearly docstringed as legacy, but a future cleanup should
  remove it: a bare-word single-token check sitting next to the G1' machinery
  is a confusion vector for the next reader, even though it cannot fire.
- **O2:** `safetensors` in requirements.txt is not directly imported by bundle
  modules (transitive via transformers) — harmless superset, no action needed.
- **O3:** The §6 budget line ("180 short forward passes") is arithmetically
  correct: 60 state + 60 A + 60 C.

---

**License state:** the bundle licenses nothing on its own. Launch chain
position: signed pre-registration (LOG-357) → bundle build (LOG-358) →
independent bundle review (this review, LOG-359, SIGN) → **CEO execution
clearance** → real execution (`python3 run_exp091.py --out-dir out
--ceo-clearance`, CPU-only, $0). No GPU clearance is required or granted.
$0 CPU; all review reads were read-only — no weights, artifacts, or signed
files modified; the only files written are this review and the LOG-359 entry.
