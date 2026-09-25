# EXP090 — Independent Law #14 Bundle Review: SIGN

**Reviewer:** Independent Law #14 Bundle Reviewer (reports DIRECTLY to the founder; verdict binding, not overridable by the CEO).
**Date:** 2026-09-25. **Logged:** LOG-352.
**Target:** `experiments/runs/EXP090_clm8b_falsifier_v2/` (built LOG-351, CPU, $0 GPU).
**Signed protocol:** `experiments/protocols/EXP090_CLM8B_ADAPTATION_V2_PREREG_SIGNED.md`
— SHA-256 recomputed by the reviewer: `440dd6a53ab88a199c88a57e629768aa9414cc1f9d907b33e2ab6019aa79c0ab`,
byte-identical to the LOG-350 record. **Signed file untouched; immutable.**

---

## Verdict: SIGN

The bundle faithfully implements the signed protocol. It is clear for the CEO's
execution-clearance decision. No fix required. No change to endpoint, verdict,
cost, or mapping — **no new experiment number triggered**. Real execution remains
NOT licensed until the CEO grants execution clearance (CPU-only per the signed
protocol; no GPU clearance is required or granted).

---

## 1. Faithfulness verification (all independently executed, nothing on trust)

- **Test reruns (reviewer's own executions):** `python3 -m unittest test_exp090` →
  **36/36 PASS** (0.058s, numpy-only). No weights touched.
- **§6 repaired bench contract:**
  - Builder output byte-identical to the LOG-345-reviewed EXP089 builder
    (test `test_bench_matches_exp089_builder_byte_identical` passed on my
    rerun — the lineage pin holds).
  - Two independent builds byte-identical (determinism) — passed on my rerun.
  - The EXP089 byte-for-value `(ent, typ)` reproduction guard is **absent from
    code** (test `test_struck_guard_absent` passed; the phrase appears only in
    docstrings/comments describing the striking — not resurrected).
  - Archive provenance pin: `assert_archive_hash()` passes on the real archive
    (`47281cd3dc243369be0aa5be2345663b752cdb4a329a16a37f08da5717230585`,
    character-identical to the §6 record) and refuses on a tampered archive
    (RUN-INVALID, no embeddings written) — both passed on my rerun; the pin
    also guards the mock pipeline before any embedding is written.
  - G3: reviewer's own run of `build_benchmark()` → exactly **30 A-first /
    30 C-first**; `state_text_of` excludes question/option list on all 60 items.
- **Guards:** G1 single-token assert (multi-token → RUN-INVALID; items not
  silently dropped); G2 state-dict hash algorithm byte-identical replica of
  EXP077's `get_hash()` (sorted keys → CPU → float32 → tobytes → SHA-256),
  enforced pre AND post extraction; G4 instrument-deafness (`max−min < 1e-4`
  over 120 cosines → RUN-INVALID, never KILL) — all test-confirmed on my rerun.
- **§7.1 TOTAL decision tree:** `n < 38 → KILL`; `n ≥ 38 AND acc_Afirst > 0.5
  AND acc_Cfirst > 0.5 → CONTINUE`; else → PIVOT. Boundary tests (38/60 clean
  → CONTINUE, 37/60 → KILL, split-at-exactly-0.5 → PIVOT, opposite tilts →
  PIVOT, one-split-below-half at 40/60 → PIVOT) all pass. Tree is total.
- **Bar sharpness:** independently recomputed via `math.comb` in the test and
  by the reviewer: P(X≥38)=0.0259469… (registers 0.0260 at 3dp, as §7 states);
  P(X≥37)=0.0462. The bar is sharp.
- **Tie rule:** exact float equality → toward C (foil), counted. Matches §6.
- **Law #13 pins:** `model.eval()` explicit before extraction;
  `torch.no_grad()` around ALL extraction; `requires_grad_(False)` on all
  parameters; `device_map="cpu"` pinned literally (LOG-345 F2 carried
  forward). Present in code, not relied on as HF defaults. Matches §6.
- **Refusal gates:** signed-protocol digest guard vs `440dd6a5…` enforced at
  startup (mismatch → refusal); forbidden flags (`--train/--gpu/--cuda/
  --finetune/…`) refused pre-parse (exit 2); real run without
  `--ceo-clearance` refused (exit 2). All test-confirmed on my rerun.
- **Mode stamp (LOG-345 F1 carried forward):** report carries
  `"mode": "mock"|"real"|"unknown"` — a mock-run verdict is distinguishable
  on disk from a real-run verdict. Test-confirmed in all three cases.
- **Law #7:** state text pinned to premise sentences; both option names appear
  in the premise exactly once each (1:1 balance) — verified on the built bench
  (sample 3-hop item: foil `Saturn` present in the premise text).

## 2. Lineage-reuse attack (EXP089 → EXP090 adaptation)

- **Digest guard:** the runner's `SIGNED_PROTOCOL_DIGEST` is `440dd6a5…
  01b` (EXP090) — repo-wide grep finds no reference to the EXP089 digest
  `87f2c47b…` in any code file. The EXP089 digest appears only in
  BUILD_NOTES.md/manifest.json lineage documentation, which is correct.
- **Bench contract:** no byte-reproduction guard exists in the EXP090 modules
  (only the provenance pin). No EXP089-ism leaks the old contract.
- **3-hop transcription bug:** the builder's self-caught bug (`"C": C` vs
  `"C": D_ent`) is genuinely fixed — both 3-hop loops append `"C": D_ent`;
  the 2-hop loops correctly append `"C": C`. Verified by source inspection
  and by the byte-identity pin against the reviewed EXP089 builder.
- **Report/embedding filenames and keys:** all `exp090_*` (`exp090_report.json`,
  `exp090_embeddings.npz`, `exp090_extraction_meta.json`,
  `exp090_extraction_log.txt`). No `exp089_*` artifact name anywhere in code.
- **Manifest:** experiment/bundle/protocol fields all name EXP090; digest
  fields match the recomputed values; `real_execution_licensed: false` is
  honest; `known_blocker: null` is correct — the §6 contract is satisfiable.

## 3. Observations (not fixes; for the record)

- O1: `extract_mock` skips G2 (no weights in mock mode) but asserts the §6
  provenance pin — documented in the extraction meta. Acceptable; the guard
  *logic* is unit-tested with monkeypatched inputs.
- O2: `extract_state_embeddings.py:main` accepts `--snapshot` override; the
  override path still enforces the G2 hash check, so a wrong snapshot fails
  closed. Acceptable.
- O3: In mock mode all 120 entities are synthetic, so the G1 "single-token"
  claim in the mock meta refers to abstract tokens — documented as such.
  Real-mode G1 runs against the actual tokenizer. Acceptable.
- O4: The `__pycache__` directory in the bundle is build residue; harmless,
  not part of the registered bundle.

## 4. License state

The bundle is **clear for the CEO's execution-clearance decision**. Real
execution remains NOT licensed until that clearance is granted. On clearance,
the real-execution command is:

```bash
cd experiments/runs/EXP090_clm8b_falsifier_v2
python3 run_exp090.py --out-dir out --ceo-clearance
```

Budget $0, ~1–2h CPU, no GPU contact. The §6 contract is satisfiable — no
known blockers. $0 CPU; no weights or EXP077 artifacts were modified by this
review (all reads read-only; hashes re-verified).
