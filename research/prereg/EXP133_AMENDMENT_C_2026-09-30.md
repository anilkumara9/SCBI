# Amendment DRAFT C: Breaking point (d) — tolerance recalibration for cross-device fp numerics (EXP133)

**Lane:** LOG-4804 (CEO pre-assigned). **Status: DRAFT — licenses nothing.** This is a narrow
amendment draft to the CEO-SIGNED pre-reg
`research/prereg/EXP_PREREG_GEOSTEER_MULTISTEP_2026-09-30.md` (signed LOG-4798, as amended
by Amendment B, Law #14 SIGN LOG-4801). It amends ONLY breaking point (d) — the
norm-budget equality tolerance. It licenses no execution; EXP133 re-execution requires
independent review of this amendment + fresh CEO clearance.

**$0 CPU scope.** Paper only; no model forwards were run to produce this draft.

---

## §1 — What tripped and why [FACT]

EXP133 re-execution went APPARATUS-VOID on breaking point (d) (LOG-4803):
the executor's norm-budget equality assert — independently recomputed
B = 0.01 × median ‖y_{20,last}‖ == verbatim 0.50578119 within 1e-6 relative —
tripped on the full 10-prompt run (exit 44) before any injection forward:

- Independently recomputed on CPU (lab VM, torch 2.14.0+cpu, float32): **B = 0.50578363**
- Verbatim LOG-4766 value (Kaggle T4 GPU, torch 2.10.0+cu128): **B = 0.50578119**
- Relative difference: **4.832e-06 > 1e-6 tolerance** → apparatus-void per §0(d).

**Diagnosis [OBSERVATION]:** tolerance defect, NOT drift. Three independent exact-match
pins rule out bench/backbone drift: backbone weights hash exact, bench hash exact, and the
300-forward B_agg reconstruction bit-identical (`d3556d83…`). A follow-up diagnostic
reproduced B = 0.50578363 **with and without** `torch.use_deterministic_algorithms(True)`
(model confirmed float32): the 4.83e-06 gap is genuine cross-device floating-point
numerics — ~20 transformer blocks of differently-ordered reductions between cuBLAS/cuDNN
(GPU) and CPU kernels. The 1e-6 tolerance is unsatisfiable on CPU for a GPU-measured
reference value.

**Defect class [INTERPRETATION]:** the same class as the first void (LOG-4799) — a
breaking-point condition validated against *logic* (two Law #14 reviews + fix verification)
but never against *reality* (no one checked that a CPU recompute reproduces the GPU value
to 1e-6). The tolerance does not detect drift on CPU; the exact hash pins already do that.

## §2 — Amended breaking point (d)

**Strikes** "asserts equality with 0.50578119 within 1e-6 relative" in §0(d).
**Replaces** with: "asserts equality with 0.50578119 within **1e-4 relative**."

**Measured justification [OBSERVATION]:**
1. The observed cross-device gap is 4.83e-06 relative — the new 1e-4 bound sits more
   than an order of magnitude above measured fp noise, so a correct CPU apparatus
   passes with wide margin.
2. 1e-4 still detects real drift: a wrong bench or backbone shifts the 10-prompt median
   norm by orders of magnitude more than 1e-4 (different prompts/weights change ‖y‖ at
   the percent level or worse, not the 1e-4 level).
3. The **dose itself is unaffected**: the executor injects the verbatim registered
   B = 0.50578119 (Law #2 — NOT recomputed as a new number). The tolerance governs only
   the drift-detector check, never the injected dose.
4. The per-step tangent audits (‖t_k‖ = B/5 ± 1e-6, ∑‖t_k‖ = B ± 1e-6) are **unchanged**:
   they are exact by construction (t_k = α·Π_k(u), α = B/5 in the same arithmetic) and
   remain satisfiable at 1e-6. Only the cross-device equality check — CPU recompute vs
   GPU-measured reference — moves to 1e-4. The dose fence (EXP129 FIX-4 discipline) is
   not weakened.

**Everything the (d) clause does besides the tolerance number is unchanged:**
recompute B = 0.01 × median ‖y_{20,last}‖ per the EXP129 FIX-2 rule, recorded before the
first injection forward; mismatch → apparatus-void, bench/backbone drift.

## §3 — Verification discipline for the amended check

1. The executor records both the recomputed B and the verbatim B with their relative
   difference in the run records (before the first injection forward).
2. The 1e-4 assert fires before any injection forward, exactly as the 1e-6 assert did —
   a trip still voids the run with zero forwards executed (the LOG-4803 behavior is
   preserved, only the bound moves).
3. The exact hash pins (backbone LOG-331, bench, npz, B_agg reconstruction) remain the
   primary drift detectors; the (d) equality check is secondary, as before.

## §4 — Everything else unchanged

The decision table (§2), the hypothesis (§1), the budget B, breaking points
(a), (b) as amended by Amendment B, (c), (e), (f), (g), the arms (§3.5), the readout
(§3.6), the ĉ_geo definition, and the records discipline (§3.8) are all untouched.
No science changes; no new quantities; no re-interpretation of any prior verdict.

## §5 — Law #14 review-checklist addition

Append to the checklist paragraph added by Amendment B §5:

> **Numerical breaking-point tolerances must be validated against real execution on the
> target device** — not merely reviewed for logical form. The defect class that voided
> EXP133 twice (LOG-4799: artifact *contents* assumed but never inventoried; LOG-4803:
> a 1e-6 cross-device equality tolerance never checked against a real CPU recompute)
> survives logic review because logic review cannot see the apparatus. Any breaking
> point that asserts a numerical bound must cite either (i) a measured bound from the
> target device, or (ii) an explicit margin argument over a measured noise floor —
> never a round number chosen for tidiness.
