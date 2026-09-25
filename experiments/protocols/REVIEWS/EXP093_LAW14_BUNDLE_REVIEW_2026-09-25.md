# Independent Law #14 Bundle Review — EXP093 (Layer-11 Causal Transfer)

**Reviewer:** Independent Scientific Mentor / Adversarial Reviewer (reports to the founder; binding).
**Date:** 2026-09-25. **Target:** `experiments/runs/EXP093_l11_causal/` (build at LOG-4344, commit `259d3d8`).
**Signed protocol:** `experiments/protocols/EXP093_L11_CAUSAL_PREREG_SIGNED.md`.
**Draft review:** LOG-4340 SIGN-WITH-FIXES + LOG-4342 SIGN addendum (this file's directory).

## Verdict: SIGN-WITH-FIXES (binding)

The bundle faithfully implements the signed protocol and the launch chain is airtight — with **one** load-bearing fix required (F1, below). Everything else verified clean by execution.

## Verified by execution

**1. Signed-protocol digest guard — VERIFIED.** Recomputed SHA-256 over the signed file with the 64-char self-digest value blanked (per the header's signature-block rule): `3e0f269b9f2c5170d2b6ed37b2bd03f39f8eeb344914e8bb1f904709ad13db93` — exact match. The runner's `assert_signed_protocol()` implements the same blanking rule (marker `**SHA-256 (this signed file):** \`` + 64 hex + backtick). The suite's tamper test (byte flipped in a *copy*, path monkeypatched — the real signed file never touched) refuses with "mismatch" — re-ran green as part of 21/21.

**2. Direction builder fidelity — VERIFIED.** Ran `direction_builder.py` against the archived `exp092_embeddings.npz` (read-only): gate PASS; min ‖r‖=1.3352027 (registered 1.3352), mean cos u=−0.0159921 (registered −0.0160), prenorm [0.0245809, 0.0444373] (registered [0.0246, 0.0444]), max cos v=0.9553621 (registered 0.9554); 60/60 ‖r_i‖>1e-9; all 60 v unit-norm; R4 not-bit-identical. Grep confirms the v0.1 degenerate construction (LOO mean of prototype residuals, identically zero) is **absent** — v0.2 max-average-cosine construction is what's implemented.

**3. Launch-chain gates — VERIFIED.** Real mode without `--ceo-clearance` → exit 2, REFUSAL on stderr, before any guard and before any weight access (probe executed). `--gpu` → exit 2 (forbidden flag). `--mock` → runs (exit 0), torch never imported. `direction_builder.py`'s CLI is numpy-only / read-only `.npz` — cannot touch weights, so no clearance gate is required there (correct). `inject.py` is library-only (no `__main__`, no weight-loading code — no `from_pretrained`/`torch.load` anywhere in the bundle except the gated `run_conditions_real`). The only weight-touching path is behind signature + clearance.

**4. Guards — VERIFIED, all implemented and ordered.** G0 (bench pin `9be81626…` via EXP092's canonical builder), G1 (Δθ=0 pre/post, pin `ec276abe…`), G1′ (bench-pin byte-identity assertion + real-tokenizer offset-mapping re-execution before weight access in real mode), G2 (direction provenance: recompute from `.npz`, label item-order assertion, ‖r_i‖>1e-9, unit norms), G3 (mode stamp), G4 (36/60 + margin tol 1e-4 on −0.0018, threads pinned and asserted), G5 (single-item probe: (i) rel 1e-6, (ii) abs 1e-9, (iii) disabled-hook logit bit-match). Guard order in `main()`: signature → clearance → G0 → G1′ → G2 → conditions → G4 → scoring; G1 pre/post brackets the real run.

**On the builder's three flagged items — all ACCEPTABLE, none a defect:**
- (a) THREAD_PIN=2 is an assumption (EXP092 had no thread metadata): the protocol §6 G4 *registers* "pins torch intra-op thread count to the EXP092 extraction value, records it in the run meta, and asserts it before condition B" — the bundle implements exactly this, and a mismatch is RUN-INVALID (fail-safe), never silent.
- (b) G4 after 60×B before P/N: the draft does not order B vs P/N; fail-fast is the compute-cheap choice. Acceptable.
- (c) G5 probe once on item 0 pre-loop: the protocol §6 G5 registers "on a single-item probe" — exact match.

**5. Decision tree — VERIFIED on all six scenarios (independent synthetic data).** CONTINUE (Δ=+0.20, p=0.00049, strict mono) → CONTINUE. Aggregate-fails + C-first bars → PIVOT(c). Aggregate-fails + A-first-only bars → PIVOT(a). Significant-but-sub-threshold (NvB p=0.0156, Δ=+0.017) → PIVOT(b). Nothing significant → KILL. 12/180 ties → RUN-INVALID. PIVOT-arm precedence (c before a) is a reasonable tiebreak for the protocol-unspecified both-strata-pass case; documented in the scorer docstring — non-blocking observation, not a defect.

**6. Tie rule — VERIFIED.** `correct = margin > 0` (strict); exact 0.0 scored incorrect and counted; >5% → RUN-INVALID. Matches §5 ("correct iff logit(target) > logit(foil)").

**7. Test suites — re-ran independently: 21/21 OK, smoke 17/17 PASS, torch never imported.**

**8. No real execution — VERIFIED.** Zero forward passes on the frozen model during build; weights untouched; `.npz` opened read-only.

## Required fix

**F1 — Δ bar computed with float subtraction misclassifies the exactly-at-bar case.** `stratum_stats` computes `delta = acc_P - acc_B` where accuracies are float means. For the exactly-at-bar outcome (nP−nB = 6 on n=60, i.e. true Δ = 0.10): `42/60 − 36/60 = 0.09999999999999998 < 0.10` — the `>= 0.10` bar FAILS, although the protocol's registered rule ("Δ ≥ 0.10", §5) is mathematically met. Verified: `(42-36)/60 = 0.1 >= 0.10` is True. Same hair on the strata (3/30). The defect is one-directional (it can only demote an exact-bar CONTINUE, never promote a below-bar one), but it is a genuine verdict-integrity deviation at a reachable boundary.

**Fix:** compute delta from integer count differences before dividing, e.g. `delta = (int(P.sum()) - int(B.sum())) / len(idx)` in `stratum_stats` (and the same for `delta_N`). This makes the exactly-at-bar case classify per the protocol. Re-run the six scenario probes after the fix; the at-bar case must CONTINUE (given p<0.05 and strict mono).

**Conditions for SIGN:** apply F1, re-run the 21/21 + 17/17 suites and the reviewer's six-scenario probe set (available in this review's working notes). Re-verification is then a check, not a re-adjudication.

## Non-blocking observations

- (O1) PIVOT-arm precedence for the both-strata-pass case (c before a) is undocumented in the protocol but reasonable and documented in code. A future erratum could register it; not required for SIGN.
- (O2) The monotone comparison `acc_P > acc_B > acc_N` is float-safe (same-denominator fractions preserve order). No change needed.

## Constraints honored

$0 CPU; read-only on weights, signed files, and EXP092 artifacts. No bundle, protocol, or review files modified by this review. No real execution performed.
