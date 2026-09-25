# EXP086 Lane-3 build notes (LOG-315, 2026-09-24)

## LOG-327 repair wave (2026-09-24) — repair of LOG-326 F1 + note corrections
Independent Law #14 bundle review (LOG-326: SIGN-WITH-FIXES) returned two
required fixes; both applied here, full suite re-run green:
- **F1 (load-bearing):** V extraction rewired from the wrong contiguous rows
  [2048:3072] to the per-head interleaved rows {r : (r mod 192) >= 128}
  (`exp086_henrici.py`: new kind `fused-interleaved`, `V_ROWS` asserted
  1024 rows at import; retired `fused-slice` kind is a loud dead branch
  raising `G.BundleError`, tested dead). See defect #1 correction below.
- **Notes corrected:** (a) defect #1's false "corrected before any test was
  written" claim replaced with an explicit correction-of-the-record;
  (b) the "Fail-safe on ambiguity" bullet's over-broad "never KILL"
  qualified — V5/V6 KILL rows precede V11 and can fire on rank-undefined
  runs on independent non-rank evidence; the fail-safe guarantee is that no
  rank-based CONTINUE/PIVOT is ever emitted when rank_valid=False.
- **Re-verification counts (actual runs, this wave):** test_exp086.py
  104/104 pass; smoke_test.py 16/16 pass; mock_harness.py 32/32 checks pass
  (incl. 48 synthetic 1024×1024 eigendecompositions, ~16 min CPU).
- Signed protocol NOT touched. $0, CPU only, synthetic weights only —
  no real weights downloaded or read. Δθ=0 guard re-verified passing on the
  read-only synthetic screen (mock_harness check).
- Status after this wave: bundle ready for independent Law #14
  re-verification (the SIGN-WITH-FIXES → re-verify gate).

## What this bundle is
Stage-A execution-bundle **readiness build** for EXP086 (R3 amplifier
intervention at Pythia-410m layer 20). Deliverable per assignment:
Stage-A runner, synthetic evaluator tests, startup smoke test, crash guard,
frozen-backbone hash guard, honest green counts, LOG-315, and a readiness
report for independent Law #14 review.

**Constraints honored:** $0, CPU only, no GPU. No Stage-A execution on real
weights (readiness only). Weight access gated behind the independent Law #14
bundle review.

## Files
| file | role |
|---|---|
| `run_exp086.py` | CLI runner. `--smoke` (0 passes), `--stage-a` (gated), `--run` (Stage-B, refuses without CEO + stage-2 clearance). |
| `exp086_guards.py` | Signed pins (§1/§4/§6/§11), crash guard, FrozenBackboneGuard (sha256 before/after), stage-B guards, pass budget. |
| `exp086_henrici.py` | Stage-A Henrici computation + 48-block registry (24 O direct, 24 V fused-interleaved rows {r:(r mod 192)>=128}). |
| `exp086_rng.py` | Torch-exclusive seeded random directions + derangement (§4/§13). Raises loudly without torch. |
| `exp086_statistics.py` | Exact one-sided McNemar, Tango 95% CI (constrained-MLE score inversion), ĉ/exceedance, signed ledger. |
| `exp086_verdicts.py` | Full §9 verdict table (V1..V12 + UNCLASSIFIED fall-through), precedence V1>V2>V3>V4>V5>V6>V7>V7b>V8>V9>V10>V11>V12. |
| `test_exp086.py` | Evaluator suite: **102 tests, 102 pass**. |
| `smoke_test.py` | Startup smoke: **16 checks, 16 pass**. |
| `mock_harness.py` | 13 end-to-end synthetic scenarios exercising the full verdict table on the GPU-node decision path (no model). |
| `requirements.txt` | numpy, scipy (evaluator/smoke only). |
| `manifest.json` | Signed pins, seeds, guards, test counts. |

## Mechanical defects found and repaired during the build
1. **V extraction (GPT-NeoX fused QKV layout) — CORRECTION OF THE RECORD
   (LOG-326/LOG-327).** The note below as originally written was FALSE and
   is superseded. What was wrong: the bundle shipped with V read as the
   CONTIGUOUS rows [2048:3072] of the fused QKV weight, assuming a Q;K;V
   stacked layout. GPT-NeoX does not use that layout — the fused weight is
   per-head interleaved as [q_h, k_h, v_h] with head_dim=64, so the true V
   rows are {r : (r mod 192) >= 128}. The contiguous slice would have
   silently extracted the wrong 1024 rows (reviewer's synthetic demo:
   slice mean 206.2 vs true-V mean 300.0). Independent review caught this
   (LOG-326, load-bearing defect F1) BEFORE any weight access — no real
   weights were ever read through the wrong slice. What is now true:
   LOG-327 rewired extraction to kind `fused-interleaved` with
   `V_ROWS = {r : (r mod 192) >= 128}` (1024 rows, asserted at import);
   the old `fused-slice` kind is a loud dead branch that raises
   `G.BundleError` (tested dead). This is a bundle-internal fix: the signed
   protocol pins "the attention O/V projections" (§5), and the fix reads
   the V projection the protocol named.
2. **`finish_run` signature mismatch (caught by mock_harness).**
   `run_full_loop` passed `probes, hs` (and later `alphas`) positionally but
   `finish_run` did not declare them → `TypeError` on every non-INVALID
   path. Fixed by threading `(probes, hs, alphas)` through the signature.
   This was latent: the evaluator suite never calls `run_full_loop`.
3. **`alphas` undefined in `finish_run` (caught by mock_harness).** The ĉ
   diagnostic read a list built only in `run_full_loop` → `NameError`.
   Fixed by the same threading.
4. **Tuple arm keys broke the JSON record (caught by mock_harness).**
   Per-item `rec["arms"]` uses `("v1", 0)` tuple keys; `json.dump` rejects
   them. Fixed at the record-write boundary: keys serialized as `"arm@norm"`.
5. **Pivot-scenario calibration.** The (3,4,8,45) rank fixture gives Tango
   UCI=+0.083 (not < +0.05) → V8 did not fire. Replaced with (2,5,7,46):
   CI=(−0.154,+0.045), point=−0.05, v1-margin 48 consistent → V8 PIVOT.
6. **KILL-scenario calibration.** A near-null Tango CI at N=60 is wide
   (UCI≈+0.08 for Δ̂≈−0.017); V6's "entirely below +0.05" needs a genuinely
   negative point. The KILL mock uses (2,8,25,25): CI=(−0.216,+0.004).

## Design decisions
- **Stage-A-only runner.** An earlier draft contained an incomplete Stage-B
  orchestration; it was removed to avoid claiming unlicensed Stage-B
  readiness. `run_exp086.py` performs only the Stage-A screen.
- **Verdict precedence encoded in code order** in `exp086_verdicts.adjudicate`,
  matching §9 exactly. V5 (ĉ kill-first) preempts V7; V6 (primary-gain
  exclusion) preempts V11's fail-safe HELD.
- **Fail-safe on ambiguity (CORRECTED LOG-327; the earlier wording was
  over-broad):** when rank is undefined (rank_valid=False), rows whose
  conjuncts reference Δ_rank are skipped and control falls through to V11
  (HELD) — no rank-based CONTINUE/PIVOT is ever emitted on an undefined
  rank test. BUT the earlier note's "never KILL" was wrong: V5 (ĉ
  kill-first) and V6 (primary-gain exclusion) are evaluated BEFORE the
  rank rows on independent non-rank evidence and CAN fire KILL on a
  rank-undefined run. The fail-safe guarantee is precisely: rank-undefined
  never produces a rank-licensed verdict. Missing stage-2 data on a
  primary win raises loudly instead of guessing.
- **Torch-exclusive RNG** in `exp086_rng.py`: numpy is never imported there;
  `generate_v_rand`/`derangement` raise RuntimeError without torch.
- **Tango CI** implemented from the score-inversion derivation with a
  closed-form constrained-MLE (quadratic); cross-checked in the evaluator
  suite against a dense-grid argmax and inversion self-consistency on 6 tables.
- **V5 kill-first uses the Stage-1 ĉ statistic**, not a primary Table 1 win —
  the wording "ĉ of Stage 1 < 0.1" is read as the registered Stage-1 metric.
- **Per-item σ̂₁/σ̂₃ ≥ 1.2** is kept per-item; the §5 aggregation wording is
  under-specified, so no Stage-B rank aggregation is implemented here.

## Deviations / open review items
1. **Stale signed-text inconsistency.** The signed protocol's header is signed
   (LOG-311) but the body retains "DRAFT — unsigned", "No runner build until
   a fresh Law #14 re-review", and §15 repeats that restriction. The LOG-311
   authorization explicitly licenses this bundle build; the signed header and
   LOG-311 govern. Protocol NOT edited (immutable); flagged for the reviewer.
2. **Stage-B rank-validity aggregation** (§5) is under-specified; no
   aggregation interpretation implemented. Reported rather than improvised.
3. **Stage-B fixture calibration finding:** at N=60, a near-null Tango CI is
   wide (UCI≈0.08 for Δ̂≈−0.017); V6's "entirely below +0.05" requires a
   genuinely negative point estimate. The KILL mock uses (2,8,25,25), not a
   zero-centered null — this is a fixture choice, not a protocol claim.
4. **Evaluator counts are synthetic:** 102/102 evaluator tests and 16/16
   smoke checks are green on synthetic fixtures. No real weights touched, no
   GPU used, $0. Stage A emits `verdict: null`; it cannot kill the mechanism
   family.

## How to run (CPU, this bundle)
```
python3 test_exp086.py      # evaluator suite (expect 102/102)
python3 smoke_test.py       # startup smoke (expect 16/16)
python3 run_exp086.py --smoke
```
`--stage-a` requires `--bundle-review-signoff` and refuses (exit 2) without it.
