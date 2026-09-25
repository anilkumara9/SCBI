# Independent Law #14 Bundle Review — EXP092 (IBL) execution bundle

**Reviewer:** Independent Law #14 Reviewer (reporting directly to the founder; binding).
**Date:** 2026-09-25.
**Target:** `experiments/runs/EXP092_ibl/` as committed at `38c48a2` (LOG-4328).
**Signed protocol:** `experiments/protocols/EXP092_IBL_PREREG_SIGNED.md`
(digest `75e744ad9bae98cc86c0443823bd27b197a9c17fc106ba984e5870cf1bdb347c` —
recomputed by this review: **exact match**; protocol untouched).
**Prior:** binding SIGN of the v2.1 draft at LOG-4325.
**Verdict:** **SIGN-WITH-FIXES** — one load-bearing fix (narrow, mechanical).
The bundle may proceed to CEO clearance once the fix is applied and
re-verified by this office.

---

## 0. Bottom line

The bundle faithfully implements the signed protocol. Every guard is real —
this review triggered each one and watched it fire. Both test-bug fixes
disclosed at build time are legitimate (they strengthen the tests; details in
§4). The S1 estimator matches its registration. The exact-tie rule is sane.
The §5 decision tree is TOTAL and byte-faithful to the protocol. The bench,
pins, and tree constants cannot be silently altered at runtime.

One real defect: the extraction module's standalone CLI
(`extract_layer_embeddings.py --out-dir X [--snapshot S]`) executes the full
60-forward-pass real extraction with **no CEO-clearance gate** — this review
demonstrated the bypass reaches the weight-loading stage (it failed only on a
deliberately bogus snapshot path; with the real path it would run). The
signed protocol's launch chain states execution requires CEO clearance; the
bundle's designated runner (`run_exp092.py`) enforces it, but the module CLI
is a second, ungated entry point. FIX 1 closes it.

---

## 1. Test suites re-run by this review (not trusted)

- `test_exp092.py`: **49/49 OK** (`Ran 49 tests ... OK`, ~5.4s, numpy-only +
  fake tokenizer; no weights touched).
- `smoke_test.py`: **11/11 PASS** (0 model passes; includes signed-protocol
  digest guard, G0/G2/G1′ artifact checks, refusal without clearance,
  `--gpu` refusal, mock end-to-end with `perm_b=20`, G4 zero-spread refusal).
- No pytest in the build venv; both suites run as plain scripts. Counts
  confirmed by this review's own execution.

## 2. Guard audit — each guard triggered, each fired

| Guard | Trigger by this review | Result |
|---|---|---|
| G0 bench pin | tampered bench (prompt string altered) via `guard_g0_bench` | **RUN-INVALID fired** |
| G0 wrong pin | (covered by `test_g0_refuses_on_wrong_pin`, passing) | fired |
| G1 Δθ=0 | synthetic dict vs real LOG-331 pin (`test_g1_hash_mismatch_refuses`) | **RUN-INVALID fired** |
| G1 pass branch | pin patched to synthetic hash (only way to exercise pass without the real snapshot) | returns hash, pin restored |
| G1′ before weights | code order in `extract_real`: tokenizer → `verify_g1_prime` (offset-mapping cover) → model load | **confirmed before any weight access** |
| G1′ negatives | multi-token span / unstable token id (`test_negative_*`) | fired |
| G2 artifact | missing artifact / stale pin (`test_g2_missing_artifact_refuses`, `test_stale_artifact_pin_mismatch_refuses`) | fired |
| G3 phrasing | imbalanced bench (`test_g3_refuses_on_imbalance`) | fired |
| G4 zero spread | smoke test "G4 zero-spread refuses" | **fired** |
| Exact-tie | `test_exact_tie_run_invalid` | **RUN-INVALID fired** |
| Signed-protocol digest | monkeypatched digest → `assert_signed_protocol()` | **REFUSED (exit-2 path)**; restored → passes |
| Layer-20 → PIVOT | `test_pivot_layer20_only`, `test_pivot_layer20_subthreshold` | PIVOT, never CONTINUE |

## 3. Decision tree fidelity (§5)

`adjudicate()` in `score_exp092.py` implements the registered tree exactly:
- S = {l ≠ 20 : p_l < α_B AND (a_l − q95_l) ≥ 0.10} → CONTINUE,
  l* = argmax effect. Tests: `test_continue`, `test_continue_picks_max_effect`,
  `test_effect_bar_sharpness` (bar boundary) — all pass.
- S = ∅, no layer significant → KILL (`test_kill`).
- S = ∅, some layer significant (sub-threshold or layer-20-only) → PIVOT
  (`test_pivot_subthreshold`, `test_pivot_layer20_only`,
  `test_pivot_layer20_subthreshold`). The tree is TOTAL; layer 20 can never
  route to CONTINUE.

## 4. The two disclosed test-bug fixes — scrutinized, both legitimate

**Fix A — G1 pass-branch test rewritten to patch the pin.**
The original test ran a synthetic dict against the real LOG-331 pin, which
can only fail. The rewrite patches `WEIGHTS_PIN` to the synthetic dict's own
hash, exercises the pass branch (returns the hash), and restores the pin in a
`finally`. This is legitimate: a unit test can only verify the *comparison
logic*; the real-pin verification happens at real extraction (untestable
without the 1.6GB snapshot). The mismatch branch is separately covered
(`test_g1_hash_mismatch_refuses`). The fix does not weaken any check.

**Fix B — scheme-fidelity test rewritten to use the same statistic in both
arms.** The original compared `score_exp092.permutation_null` against
`reference_implementation.stratified_permutation_p` while the two arms used
*different* tie-break statistics (the §5 discrepancy this office noted at
LOG-4323: analytic expected accuracy vs Monte-Carlo tie draws) — a confounded
comparison. The rewrite drives both arms with the same argmin 1-NN statistic
on one distance matrix, isolating the RNG scheme
(`random.Random(9207+b)`, within-strata shuffle, p=(1+ge)/(1+B)).
This review additionally verified by code inspection that the reference
implementation's `stratified_permutation_p` (lines 209–229) uses exactly the
registered scheme, and the test asserts p-value agreement to 6 decimals. The
tie-break convention is separately pinned in the signed protocol §8
(analytic expected accuracy) and in the G2 reference code. Legitimate —
methodologically the *correct* comparison.

## 5. S1 estimator (Ross kNN-MI after PCA≤20)

` s1_mi()` in `score_exp092.py`: centers + SVD-projects to ≤20 dims,
k=3 nearest-neighbor distances (self excluded via partition index k),
m_i = points within ε_i (self included), N_{y_i} = same-label counts,
MI = ψ(n) − ⟨ψ(N_y)⟩ + ψ(k) − ⟨ψ(m)⟩ in nats → bits. The digamma uses the
standard recurrence-to-8 + asymptotic series (accurate ~1e-10). This matches
the registered "KSG kNN-MI after PCA≤20" (PCA to 20 dims, k=3). Sanity:
`test_s1_signal_positive` (clustered signal → positive MI) and
`test_s1_finite` (noise → finite) both pass. S1 is non-binding per §7; the
implementation is honest and matches its registration. No defect.

## 6. Exact-tie RUN-INVALID rate risk

The tie rule asserts zero *exact float* ties in squared Euclidean nearest-
neighbor distances (`np.abs(d − row_min) == 0`, diagonal excluded as inf).
For 60 distinct float32 embedding vectors from a real model, exact distance
ties between distinct items are measure-zero events. The failure direction is
fail-safe (RUN-INVALID, never a false verdict). On the mock pipeline the run
completes without spurious invalidation. **Sane; no spurious-invalidation
risk on real float embeddings.**

## 7. CLI audit

`run_exp092.py` (the licensed entry point):
- no `--mock`, no `--ceo-clearance` → **exit 2** ("real execution requires
  --ceo-clearance"). Verified by this review's smoke re-run.
- `--gpu` / `--cuda` / `--train` / `--finetune` / `--lr` / `--mutate-weights`
  etc. → **exit 2** (forbidden-flag scan before argparse). Verified.
- `--mock` → exit 0, report stamped `mode="mock"`. Verified.
- `score_exp092.py` standalone CLI reads an embeddings file only — no model
  passes, no clearance needed. Its `decide_from_embeddings` defaults to the
  registered `PERM_B=1000` (the `perm_b` parameter is exercised only in
  tests/smoke); the report records `perm_B`. No defect.
- **DEFECT (FIX 1):** `extract_layer_embeddings.py` has a standalone
  `main()` CLI (`--out-dir`, `--mock`, `--snapshot`) with **no clearance
  gate**. This review demonstrated the bypass:
  `python extract_layer_embeddings.py --out-dir /tmp/exp092_bypass_probe
  --snapshot /nonexistent_snapshot_xyz` → proceeded past every gate until the
  snapshot check (`RUN-INVALID: snapshot directory not found`) — i.e., there
  is no clearance refusal anywhere on this path. With the real snapshot path
  it would load the model and execute all 60 forward passes. All protocol
  guards (G0/G1/G1′/G2/G3) still fire on this path and it is read-only and
  deterministic, so no verdict can be corrupted — but the signed protocol's
  launch chain ("execution requires independent bundle review + CEO
  clearance") is not enforced on this entry point.

## 8. Runtime immutability of bench, pins, decision tree

- **Bench:** built deterministically by `ref.build_bench()` (seed-1022);
  `guard_g0_bench()` asserts the registered pin
  `9be81626…f47fc4` over the registered canonical serialization at every
  extraction startup. No CLI flag or env var alters the bench. Tampering →
  RUN-INVALID (demonstrated, §2).
- **Pins:** `SIGNED_PROTOCOL_DIGEST`, `BENCH_PIN`, `WEIGHTS_PIN` are module
  constants in `protocol_pin.py`; no override path exists.
- **Decision tree:** `ALPHA_B`, `EFFECT_BAR`, `PERM_B`, `PERM_SEED`,
  `EXCLUDED_LAYER` are module constants in `score_exp092.py`; the only
  parameter (`perm_b`) defaults to the registered value on every real path.
- **`--snapshot` override** is fail-safe: G1 hashes the loaded `state_dict`
  against the LOG-331 pin, so any non-identical snapshot → RUN-INVALID. It
  cannot silently substitute weights.

---

## 9. Binding ruling: SIGN-WITH-FIXES

**FIX 1 (load-bearing, mechanical):** the standalone real-extraction path in
`extract_layer_embeddings.py::main()` must enforce the launch chain — require
`--ceo-clearance` for non-mock extraction and refuse with exit 2 otherwise,
mirroring `run_exp092.py` (or, equivalently, restrict the standalone CLI to
`--mock` only and document `run_exp092.py` as the sole licensed entry point).
The fix must be covered by a CLI test (real-mode without clearance → exit 2)
and re-verified by this office. Rationale: the signed protocol licenses
execution only after CEO clearance; a bundle entry point that executes 60
model passes without it does not implement the licensed launch chain.

No other fixes required. The bundle is otherwise sound: guards real,
protocol untouched, tests green, secondaries honest, tree faithful.

**Advisory (non-blocking):** consider removing the `--snapshot` override from
the licensed CLI surface or logging its value prominently in the extraction
meta — it is currently fail-safe via G1 but is the one remaining
operator-controlled degree of freedom on the real path.

This ruling does not touch: EXP091's ADOPTED KILL (LOG-361/362), the LOG-204
bridge demotion, the H1 closure (LOG-4317), the LOG-4321 weights-integrity
resolution, or any other program result.

**Reviewer:** Independent Law #14 Reviewer. **Binding on the program.**
**LOG-4329.** Committed locally (no push — pushes need the founder's token).

---

## Addendum — Re-verification of LOG-4329 FIX 1 (LOG-4331): **SIGN**

**Reviewer:** Independent Law #14 Reviewer (reporting directly to the founder; binding).
**Date:** 2026-09-25.
**Target:** `experiments/runs/EXP092_ibl/extract_layer_embeddings.py` as committed at `bf9e1ab` (LOG-4330).

The single load-bearing fix from the LOG-4329 SIGN-WITH-FIXES ruling was re-verified **by execution, not by trust**:

1. **Bypass probe re-run (the exact probe from §7):** `python extract_layer_embeddings.py --out-dir /tmp/exp092_bypass_probe --snapshot /nonexistent_snapshot_xyz` (no clearance) → **exit 2**, `REFUSAL: real extraction requires --ceo-clearance (CEO). Use --mock for synthetic tests.` on stderr. The refusal fires in `main()` before any guard and before any weight access — the weight-loading stage is never reached. **Bypass CLOSED.**
2. **Clearance gate is real, not decorative:** same probe with `--ceo-clearance` → proceeds past the clearance check, then **exit 3** (`RUN-INVALID: snapshot directory not found`) — the next gate working as designed. The flag genuinely gates the real path.
3. **Mock path intact:** `--mock` without clearance → **exit 0**, embeddings written. The fix did not kill the legitimate mock path.
4. **Test suites re-run independently:** `test_exp092.py` **52/52 OK** (49 prior + 3 new `TestExtractionCliClearance`); `smoke_test.py` **11/11 PASS**, zero failures. Counts confirmed, not trusted.
5. **Signed protocol untouched:** digest recomputed = `75e744ad9bae98cc86c0443823bd27b197a9c17fc106ba984e5870cf1bdb347c` — exact match.
6. **Mirroring vs mock-only — ruled SOUND.** The fix agent's rationale (BUILD_NOTES.md §LOG-4329 FIX 1): the standalone module CLI is a legitimate cleared-execution path (the CEO may invoke extraction directly); a mock-only restriction would have killed a licensed path; one consistent clearance mechanism across both entry points is less error-prone than two different ones. This office agrees: the refusal wording is byte-identical to `run_exp092.py`, the gate placement is identical (first check in `main()`, before any guard/weight access), and the semantics are identical (exit-2 refusal). No new risk is introduced beyond what the licensed runner already carries. **Non-blocking observation:** any future change to clearance semantics must be applied to both entry points; if they ever diverge, the module CLI should be removed rather than re-gated.

### Binding verdict: **SIGN**

FIX 1 is verified. The EXP092 bundle now implements the signed protocol's launch chain on every entry point. **The bundle is cleared for CEO execution clearance.** Next in the launch chain: CEO clearance → real CPU extraction (~1.5 CPU-h).

Untouched by this ruling: EXP091's ADOPTED KILL (LOG-361/362), the LOG-204 bridge demotion, the H1 closure (LOG-4317), the LOG-4321 weights-integrity resolution, or any other program result.

**Reviewer:** Independent Law #14 Reviewer. **Binding on the program.**
**LOG-4331.** Committed locally (no push — pushes need the founder's token).
