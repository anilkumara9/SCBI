# Law #14 independent execution review — EXP131 re-execution attempt 2 (CPU)

**Reviewer:** independent lane, LOG-4831 (pre-assigned by the CEO). No prior
involvement in the detector insertion or the attempt-2 run.

**Verdict: SIGN** — no blocking findings, no advisories. The KILL stands and
is binding on acceptance of this review.

## Verdict under review

EXP131 attempt 2 (CPU) — **KILL** (LOG-4830): ĉ = 0.03742 < 0.1 (0
exclusions), ΔM_v1 = 0 (zero flips, 11 arms × 10 prompts), median
margin-displacement ratio = 0.5592, McNemar one-sided p = 1.0, rank-trend
4/10 FAIL, ΔM_Bagg = 0. Distinguishing claim vs the voided attempt-1 GPU
run: (h) PASS (r = 1.0000001), (d2) PASS (rel 4.83e-06), median r = 0.5592
(not the 1.0 blind-tap signature).

## 1. Delivery verification — PASS (the crux)

Independently verified from the records, nothing on authority:

- Breaking point (h): console log line 18–19 — `r = 1.0000001 ∈ [0.99, 1.01]`,
  PASS. Injection provably reaches the readout tap.
- All 110 injection-arm margin displacements in `exp131_records.json` are
  **nonzero** (min 1.27e-08, max 1.32e-05). Attempt-1's blind-tap signature
  (all-zero displacements) is absent.
- The degenerate-branch signature is absent: all 10 per-item r values are
  distinct ([1.2041, 0.7160, 1.0445, 0.2911, 1.5741, 0.2889, 1.0309, 0.4024,
  0.3006, 0.1684]); none is exactly 1.0; median = 0.5591674452378468
  matches the report. These are real measured ratios, not 0/0 → 1.0
  artifacts.
- Breaking point (d2): console log line 16–17 — rel = 4.832e-06 ≤ 1e-4,
  PASS; reproduces LOG-4803's cross-device measurement.

The readout measured an injected state on every arm. Delivery is genuine.

## 2. Detector-insertion confinement — PASS

`git diff` of `run_exp131.py` vs the LOG-4820 executor (commit `eadbb17`):
**12 insertions, 0 deletions** — exactly the Amendment-F drift-detector
block. Placement verified in the file: after the `budget B` log line and
before the §5b (h) header, matching the Amendment-F named insertion point.
No other executor change; clearance conditions hold.

## 3. Amendment compliance — PASS

- Amendment E (venue GPU→CPU): `env.device = 'cpu'` recorded in the
  records (LOG-4825 advisory A1 honored — the actual device is recorded per
  pre-reg §3.2, not asserted).
- Amendment F (d2): reference constant `0.50578119` applied verbatim in the
  code; band 1e-4 enforced; exit-44 apparatus-void routing present.
- Breaking points enforced and passed: (a) protocol pin `d85205f4…`;
  backbone LOG-331 pin `ec276abe…` pre AND post (Δθ=0); v1 re-pinned
  `9b527c02…` 10/10 ids; B_agg reconstruction `d3556d83…`; bench pin
  `e91b302f…`; budget B_cpu = 0.50578363; norm-budget audit 110/110 within
  1e-6; sensing-discipline assert; v2 derivation 10/10 |v2·v1| ~1e-9;
  (d2) PASS; (h) PASS. No trip unreported.

## 4. Decision-table application — PASS (KILL over-determined)

Against the signed pre-reg §2 table (ĉ-first precedence, KILL branches
evaluated before CONTINUE):

- ĉ = 0.03741588660651928, verified by independent recomputation from
  `c_hat_per_prompt` (exact match, 10/10 prompts, 0 exclusions, max 0.0634
  < 0.1) → **first KILL row fires** (ĉ < 0.1 → decision-orthogonal
  amplifier).
- ΔM_v1 = 0: independently counted 0 flips over all 110 injection-arm
  pairs → **second KILL row fires**.
- Rank-trend 4/10 < 8/10 bar → **third KILL row fires** (flat trend).
  Correctly read as a KILL-conjunct failure, not a void — the rank-trend
  gate is a KILL row in §2, and the KILL already fired on the ĉ gate first.
- CONTINUE requires ALL of ĉ ≥ 0.1, median r ≥ 2, ΔM_v1 > 0 with McNemar
  p ≤ 0.05, rank-trend holds, ΔM_Bagg = 0 — every conjunct independently
  fails (ĉ = 0.0374; median r = 0.5592; ΔM_v1 = 0; b = c = 0 → p = 1.0;
  rank-trend false). No CONTINUE corner arguably applies.
- HELD requires margin ratio ≥ 2× with ΔM_v1 = 0 — measured 0.5592, so
  HELD does not apply.
- PIVOT/INCONCLUSIVE: no corner of §2 arguably applies; ĉ-first precedence
  (EXP129 FIX-1 discipline) correctly honored.
- ΔM_Bagg = 0 — the null control holds; no RUN-INVALID.

The KILL is over-determined three independent ways. The arithmetic was
spot-checked on the records, not trusted from the report.

## 5. Record integrity — PASS

- `exp131_records.json` sha256 `867b123f0afadf335af5c2e2bcec3c274993b70157067aa1c88989e525ef581f`
  recomputed from disk — matches the LOG-4830 pin exactly.
- Attempt-1 (voided GPU) records archived distinctly in
  `out/attempt1_voided_gpu/` (console, records, records.sha256, report) —
  not overwritten by attempt 2.
- Attempt-2 records are distinct and hash-pinned.

## 6. Scope honesty — PASS

The verdict closes exactly the hypothesis the pre-reg registered: a
one-shot injection test along v₁ with matched random controls, dead B_agg
control, ĉ gate, and singular-rank trend gate. "One-shot TGA-v₁ injection
is decision-orthogonal at the injection scale" is that hypothesis, no
more. It implies nothing about multistep/geodesic steering (EXP133's
separate, binding KILL) and nothing about the amplifier's existence
(EXP127's CONTINUE measurement stands — the dynamics amplify; the task
doesn't care). No overclaim.

## Disposition

Upon CEO acceptance, the EXP131 attempt-2 KILL is **binding**: one-shot
TGA-v₁ injection steers zero decisions at the injection scale with
verified delivery (ΔM_v1 = 0, ĉ = 0.0374 < 0.1, McNemar p = 1.0, median
r = 0.5592). The one-shot hypothesis — the last open thread from the
attempt-1 suspension — is closed.
