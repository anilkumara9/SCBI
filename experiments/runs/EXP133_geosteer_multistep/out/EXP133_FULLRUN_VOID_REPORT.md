# EXP133 full run — APPARATUS-VOID report (breaking point (d) tripped, no forwards executed)

**Experiment:** EXP133 (GEOSTEER geodesic multistep CPU pilot, re-execution under pre-reg as amended).
**Lane:** LOG-4803 (CEO pre-assigned). **Date:** 2026-09-30. **$0 CPU.**
**Verdict: APPARATUS-VOID** (breaking point (d) tripped). Hypothesis UNTESTED.
Zero injection forwards executed. No full-run records exist; no records hash.
Executor: `../run_exp133.py` (exit 44). Full stdout: `exp133_full_stdout.log`.

This is the SECOND void of EXP133. The first (LOG-4799, `EXP133_APPARATUS_VOID_REPORT.md`)
tripped breaking point (b) on the unsatisfiable npz-key clause; Amendment B licensed
deterministic v2/B_agg recovery and the CEO re-cleared (LOG-4802). This run tripped a
*different* breaking point — (d), the norm-budget equality assert.

## Breaking-point results (full 10-prompt run)

**(a) Backbone LOG-331 pin — PRE PASS, POST NOT REACHED.**
Pre: `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed` — exact match.
The run stopped before any injection forward, so no post pin was taken.

**(b1) v1 re-pin — PASS.** `exp127_vectors.npz` SHA-256
`9b527c026d0ee307192725429f655e628f403505343dc018de3cfe15db6113dc`, 10/10 id alignment.

**(b2) v2 reproduction — NOT REACHED** (run stopped at §5, before the §7 derivation).

**(b3) B_agg reconstruction — PASS.** Deterministic EXP077 support-set reconstruction
(300 presentations) reproduced SHA-256
`d3556d83751634a2fc5114d56c4ee246bb1b296293d2adcde40a369da1600ae1` —
**bit-identical** to EXP131's `pins.bagg_reconstruction`.

**(d) Norm-budget equality — TRIPPED → APPARATUS-VOID.**
- Independently recomputed on CPU (10-prompt bench median): **B = 0.50578363**
- Verbatim LOG-4766 value (Kaggle T4 GPU): **B = 0.50578119**
- Relative difference: **4.832e-06 > 1e-6 tolerance** → executor called apparatus-void (exit 44),
  per the signed pre-reg §0(d): "mismatch → apparatus-void, bench/backbone drift."

## Diagnosis: tolerance defect, NOT apparatus drift [OBSERVATION + INTERPRETATION]

Three independent exact-match pins rule out bench/backbone drift:
1. Backbone weights hash — exact match (bit-identical parameters).
2. Bench hash `e91b302f…` — exact match (bit-identical prompts/tokenization).
3. B_agg reconstruction over 300 full model forwards — **bit-identical** hash.

A follow-up diagnostic (independent script, `/tmp/diag_b.py`) reproduced B = 0.50578363
**with and without** `torch.use_deterministic_algorithms(True)`, and confirmed the model
loads in float32. The 4.83e-06 relative gap is therefore genuine cross-device floating-point
numerics: EXP131's verbatim value was computed on a T4 GPU (torch 2.10.0+cu128, cuBLAS/cuDNN
kernels); this pilot runs on CPU (torch 2.14.0+cpu). Twenty transformer blocks of
differently-ordered reductions accumulate ~5e-6 relative — **tighter than the pre-reg's
1e-6 tolerance.**

**Defect class:** the same as the first void — a breaking-point condition validated against
*logic* (two Law #14 reviews + fix verification) but never against *reality* (no one checked
that a CPU recompute reproduces the GPU value to 1e-6). The tolerance is unsatisfiable on
CPU; it does not detect drift (the hash pins already do that, exactly).

## What was NOT done (per the single-lane fence)

- No v2 derivation, no geodesic walks, no ĉ VJPs, no injection forwards, no metrics,
  no decision-table evaluation. The §2 table's "any breaking-point miss → apparatus-void"
  row is the raw verdict; no re-interpretation was attempted.
- The executor enforced the trip itself (exit 44); the lane did not override it.

## Smoke-test record (same executor, 1 prompt — all mechanical checks PASS)

`exp133_smoke_stdout.log`, `exp133_smoke_records.json` (+ `.sha256`), `exp133_smoke_report.json`:
- All breaking points reachable in 1-prompt mode passed, including v2 run-twice
  bit-identity (both runs SHA-256 `3499eb0e…5665f4`), unit-norm/orthogonality asserts,
  B_agg hash gate, 25/25 tangent-step norm audits at α±1e-6, one-shot arm at B±1e-6,
  B_agg-path null-control, backbone pre/post pins.
- Machinery verdict on 1 prompt (NOT the experiment verdict): KILL, decision-orthogonal
  (ΔM_geo=0, ĉ_geo=0.0643 < 0.1). The 10-prompt verdict was never reached.

## Recommended CEO dispositions (not this lane's mandate)

1. **Amendment C candidate:** relax breaking point (d)'s equality tolerance from 1e-6 to
   1e-4 relative, with the measured cross-device numerics (4.83e-06) as justification.
   The downstream science is unaffected — the executor already uses the verbatim
   registered B = 0.50578119 (Law #2); the tolerance only gates proceeding. 1e-4 still
   detects real drift (wrong weights/prompts shift norms by orders of magnitude more),
   and the exact hash pins remain the primary drift detectors.
2. **Checklist addition:** breaking points with *numerical* tolerances must be validated
   against a real execution (or a documented reproducibility bound), not just reviewed
   for logical form — the same lesson as Amendment B's §5, extended from artifact
   *contents* to artifact *numerics*.
3. On re-clearance, re-execution resumes from the current executor unchanged
   (the (d) tolerance is its only unsatisfiable condition on CPU).
