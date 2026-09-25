# CLLC Falsification Decision-Tree Skeleton — Draft v1

**Status:** DRAFT — LOG-290 F1–F19 repairs applied 2026-09-24; pending Law #14 re-verification. Not signed, not a pre-registration.
**Date:** 2026-09-24. **Author:** Law #14 reviewer (LOG-281 wave 2, founder 24/7 order).
**Cost:** $0, CPU only.
**Purpose:** a self-contained KILL/CONTINUE/PIVOT/HALT decision tree for
EXP-CLLC-01 with exact numeric bars, derived from the LOG-281-fixed
`CLLC_ACCOUNTING_DRAFT_2026-09-24.md`. The pre-registration adopts this tree
verbatim or records every deviation with rationale.
**Constraint:** registration is conditional on K2's P2 gate firing; this file
licenses nothing until then.
**Classification guard:** any positive CLLC result initially means
**activation control, not autonomous cognition** (per §8 skeleton); re-entry
to the broader SCBI cognitive-control hypothesis needs a later experiment
removing the externally specified direction/reference.

---

## 0. Parameters (all pending Law #14 ratification unless marked binding)

| Symbol | Value | Status |
|---|---|---|
| δ_min (minimum licensed effect) | 0.05 | binding per program stats revision |
| τ (compute-match tolerance) | 0.25 | candidate — ratify or replace |
| η* (efficiency floor) | 1.0 | candidate — ratify or replace |
| CI level | 95% Tango on paired difference; McNemar exact | program standard |

**Feasibility-algebra requirement** (EXP079 lesson, LOG-138): the
pre-registration must show from N, δ_min, and the endpoint's CI geometry that
the BEATS cell is algebraically reachable. A trial whose beats cell is
infeasible by construction does not launch.

---

## 1. Primary endpoint and verdict cells

Primary endpoint: decision-flip rescue rate vs arm (A); Δ̂(X,Y) = ΔM_X − ΔM_Y,
two-sided 95% CI [L, U]. No verdict on p-value alone (δ_min binding).

| Verdict cell | Exact trigger |
|---|---|
| BEATS | L(Δ̂) > δ_min |
| INDISTINGUISHABLE | CI covers 0 AND U < δ_min |
| DOMINATED | U < −δ_min |
| UNDERPOWERED (Inconclusive — hold, never license) | CI covers 0 AND U ≥ δ_min |
| SUB-THRESHOLD POSITIVE (no licensed feedback claim) | L > 0 AND U < δ_min |
| SUB-THRESHOLD NEGATIVE (no licensed feedback claim) | L > −δ_min AND U < 0 |
| THRESHOLD-STRADDLE POSITIVE (Inconclusive — hold, never license, never kill) | L > 0 AND L ≤ δ_min AND U ≥ δ_min — straddles the minimum-effect bar; powered re-test [F1] |
| THRESHOLD-STRADDLE NEGATIVE (Inconclusive — hold, never license, never kill) | U < 0 AND U ≥ −δ_min AND L ≤ −δ_min — straddles the negative minimum-effect bar; powered re-test [F1] |
| BOUNDARY (never a license — hold) | exact equalities: U = δ_min with CI covering 0 → UNDERPOWERED; L = δ_min → not BEATS → hold; ρ = 1±τ exactly → asymmetric [F12]; measure-zero CI edges → hold: {0 < L < δ_min, U = δ_min}, {L = −δ_min, U < 0}, {L < −δ_min, U = −δ_min} [F17] |

---

## 2. Decision rows (between-the-arms; §8 skeleton + LOG-281 fixes; LOG-290 F1–F19 repairs applied)

Rows R4–R6 (the (C)-vs-(D) legs) live in the §2.1 sub-table; the main table
below carries the remaining rows.

| # | Trigger (exact) | Verdict |
|---|---|---|
| R1 | U(Δ̂(C,A)) ≤ 0 at **injection-matched** budget (Σ_ℓ‖u_ℓ‖² equalized post-hoc; FPE_C/FPE_A = 2.0 disclosed) | **KILL** CLLC-as-feedback |
| R2 | U(Δ̂(C,B2)) < δ_min (licensed below-bar evidence vs B2) [F11] | **KILL** feedback machinery — no overclaim vs weak open-loop baselines; CONTINUE adaptivity as open-loop only |
| R3 | SUB-THRESHOLD POSITIVE or SUB-THRESHOLD NEGATIVE cell of §1 vs (B2) — licensed evidence that *effect* < δ_min with licensed sign [F9] | **KILL** the feedback claim; CONTINUE adaptivity as open-loop only |
| R7 | (B) > (A) licensed (L(Δ̂(B,A)) > δ_min) with (C) ≈ (B) (INDISTINGUISHABLE cell) | **PIVOT** to open-loop multi-layer |
| R8 | L(Δ̂(E,A)) > 0 | **HALT** — budget confound; all feedback claims suspended; redesign |
| R9 (guard) | L(Δ̂(D,A)) ≤ 0 (comparator (D) shows no licensed effect on the relational task) | **suspend** the (C,D) task-comparison and efficiency legs alike — §2.1 does not evaluate; report only; η degenerate — beating a non-working baseline licenses nothing [F18] |
| R10 | CI(Δ̂(C,B)) entirely below 0 (U < 0) [F19] | **KILL** the feedback claim (feedback actively harmful vs non-adaptive multi-layer open-loop); R7's PIVOT direction applies if L(Δ̂(B,A)) > δ_min |
| R0 | any outcome in UNDERPOWERED / THRESHOLD-STRADDLE / BOUNDARY cells, or any outcome firing no other row [F16] | **HOLD** — no verdict licensed, no verdict killed; triggers the powered re-test protocol |

R9 residual verdict [F4]: R9 suspends *only* the (C,D) clauses of the §2.1
rows. The (A)/(B2)/(B)/(E) rows (R8, R1, R2, R3, R7, R10) evaluate normally
and their verdicts stand as fired. If L(Δ̂(C,B2)) > δ_min holds while R9
fires → **CONTINUE deeper investigation on the (B2) leg only; no (D)-relative
claim licensed**.

R8 detection bar [F15]: the bar is L(Δ̂(E,A)) > 0, not δ_min. For a negative
control, *any* licensed-positive (E)-vs-(A) difference indicates a
budget/probe-information confound, so the control uses the detection bar, not
the minimum-effect bar.

R3 deviation note [F9]: the accounting draft's decision-table row fires KILL
on "sub-threshold or boundary no-cell outcomes of §3" vs (B2). This tree
deviates: exact-boundary equalities → hold as Inconclusive, because a KILL is
itself a licensed verdict and fence data licenses neither direction. The
accounting draft carries the same latent conflict (its §1 "never a license —
hold" vs its decision-table KILL) and should be conformed; this draft is not
the venue for that edit.

### 2.1 (C)-vs-(D) sub-table — every row requires L(Δ̂(C,B2)) > δ_min licensed AND R9 not fired [F2/F3]

| # | Trigger (exact) | Verdict |
|---|---|---|
| R4 | L(Δ̂(C,D)) ≥ 0 AND (ρ ∈ (1−τ,1+τ) OR η ≥ η* licensed under the guards) [F3, F12] | **CONTINUE** to deeper investigation — meaningful control-method result |
| R4a | L(Δ̂(C,D)) ≥ 0 AND ρ > 1+τ AND η ≥ η* NOT licensed under the guards [F2(i)] | **CONTINUE** deeper investigation on the method result; efficiency/novelty claim held inconclusive, reported only |
| R4b | L(Δ̂(C,D)) ≥ 0 AND ρ < 1−τ AND η ≥ η* NOT licensed under the guards [F2(ii)] | **KILL** the novelty claim (the cheap-Jacobian-free story is falsified by the cost ordering at no task edge); CONTINUE the (B2)-leg investigation only |
| R4c | (C,D) task comparison inconclusive — neither L(Δ̂(C,D)) ≥ 0 nor U(Δ̂(C,D)) < 0 licensed — any ρ [F2(iii)] | **CONTINUE** on the (B2) leg; the (D)-relative claim held inconclusive, reported only |
| R5 | U(Δ̂(C,D)) < 0 (efficiency cell) AND ρ > 1+τ AND η ≥ η* (η licensed under the guards) | **CONTINUE as an efficiency investigation only** — never licenses the novelty claim |
| R6 | U(Δ̂(C,D)) < 0 AND (ρ ≤ 1+τ OR η ≥ η* NOT licensed under the guards) | **KILL** the novelty claim (no better at no lower cost — not a contribution) |

Coverage note: the six rows are total over the 3×3
(task-comparison × ρ-class) grid — every cell fires exactly one row (R4's
η-disjunct covers {L ≥ 0, ρ < 1−τ, η licensed}; R4b covers the η-unlicensed
remainder of that cell). [F2]

**η guards [F6, F10]:** η = (ΔM_C/FPE_C)/(ΔM_D/FPE_D), computed only when both
ΔM_C and ΔM_D are licensed positive (L(Δ̂(C,A)) > 0 and L(Δ̂(D,A)) > 0 at
minimum). Composition: the licensed "η ≥ η*" decision requires L_boot(η) ≥
η*, where the 95% interval is a paired bootstrap over instances — resample
instances with replacement and recompute ΔM̂_C, ΔM̂_D jointly from the same
replicate, FPE_C/FPE_D held at calibrated values within a replicate.
Rationale: ΔM_C and ΔM_D both subtract arm (A)'s rate on the same instances,
so their sampling errors are correlated; naive independence-based composition
of the component Tango CIs is invalid and unlicensed. (Fieller's construction
with estimated covariance is an acceptable alternative if derived.)
FPE-calibration uncertainty propagates multiplicatively into η: the
pre-registration must publish the FPE calibration CI and show the η verdict
unchanged across it (sensitivity analysis); if the verdict is not robust, the
efficiency cell is held Inconclusive. A verdict on the η point estimate alone
is unlicensed. If the η-relevant intervals cannot resolve the η* threshold,
the efficiency cell is Inconclusive: with U(Δ̂(C,D)) < 0 licensed, R6's KILL
rests on the licensed task comparison (the η clause only blocks rescue); with
no licensed (C,D) task comparison, hold per R4c. At the expected ρ ≫ 1, η* =
1.0 is a weak floor (licenses CONTINUE-investigation only).

**"Matched compute" (definition) [F8]:** "matched compute" := (ρ ∈
(1−τ,1+τ)) ∨ (η ≥ η* licensed under the guards). Either leg suffices; neither
may be silently assumed. Disagreement case: parity holds but η < η* licensed
(e.g. ρ near 1+τ with ΔM_C ≈ ΔM_D) — the parity leg licenses only the weaker
CONTINUE-investigation verdict (R4), never an efficiency license.

**R9 suspension-bar justification [F7]:** the degeneracy is denominator ≈ 0,
not sub-threshold effect. When L(Δ̂(D,A)) ≤ 0, ΔM_D is statistically
indistinguishable from zero, so η's denominator has unbounded relative
error — the comparison is degenerate, not merely unfavorable. L(Δ̂(D,A)) > 0
is the CI test that the denominator is bounded away from zero: the
mathematically targeted bar. The δ_min bar would be wrong here — it would
suspend legitimate comparisons against weak-but-working controllers (e.g.
licensed ΔM_D = 0.03 < δ_min = 0.05, a non-degenerate denominator). Boundary
L = 0 → suspend (safe direction). Guard composition: R9 blocks exact
degeneracy (ΔM_D unlicensed-positive); the η CI-aware guard blocks
near-degeneracy (ΔM_D licensed but tiny → the component intervals cannot
resolve the η* threshold → the efficiency cell is Inconclusive).

**(D) competence anti-gaming pin [F14]:** R9 is a safe harbor for a
deliberately weak (D) — nothing in the variant pin, shared reference, or
amortized-tuning ledger requires (D) to be *competent*. The pre-registration
must therefore (a) validate (D) on a task where A-LQR machinery is verified to
work (behavior steering per the primary source, arXiv:2604.19018 — i.e. show
the implemented (D) reproduces a licensed steering effect on its home turf)
or (b) document (D)'s tuning protocol with the same care as (C)'s
amortized-tuning ledger. The R9 suspension verdict must distinguish
"suspended: (D) validated but ineffective on the relational task (off-label —
the informative outcome)" from "suspended: (D) unvalidated — the (C,D) leg is
missing and any CONTINUE verdict is weakened accordingly". Δ̂(D,A) is
computed on the same pre-registered analysis population as the primary
endpoint.

R9 scope note [F18]: the suspension covers the (C,D) task-comparison and
efficiency legs alike. This is broader than the accounting draft's "efficiency
comparison" phrasing — the tree's broader scope is correct (suspending only
the ratio while letting R4's task leg license "meaningful control-method
result" off a dead comparator would be the degenerate win the guard exists
to prevent); the accounting draft should be conformed.

**(D) scope guard:** (D) is A-LQR's closed-loop Jacobian controller machinery
with the relational reference substituted for the published semantic setpoint
(off-label use; A-LQR's verified tasks are behavior steering). A (C) win
licenses a *controller-difference* claim on the relational task, never
superiority to the published A-LQR system.

**"Strictly less info/compute" (for R5) [F13]:** ρ > 1+τ. The info-order
strictness on the Jacobian axis is automatic by construction for the
faithful-online (D) variant only; if the pre-registration pins the cached
(D) variant, it must re-derive the information order for the cached variant
before R5 can fire. Shared reference construction (§2.2 of the accounting
draft) carries the information-isolation work; (D)'s implementation variant
(faithful-online vs cached) pinned at pre-registration, never post-hoc.

### 2.2 Total evaluation order [F5]

Evaluate in this order; the first row whose trigger fires determines the
verdict (a later row may also have its trigger satisfied, but its verdict is
superseded):
1. R8 (design validity — a confounded design preempts substantive verdicts; R8∧R1 → HALT).
2. R1 (substantive kill vs A; R1∧(§2.1 rows) → KILL — the feedback claim is dead regardless of the B2 comparison, e.g. U(C,A) ≤ 0 with L(C,B2) > δ_min when B2 ≪ A).
3. R2 / R3 / R7 / R10 (B2/B legs; R7∧R2 can co-fire compatibly — both point to open-loop).
4. R9 (guard): if fired, suspends the (C,D) clauses of §2.1; residual verdict per the R9 pin above. R8/R1/R2/R3/R7/R10 verdicts stand as fired regardless of R9.
5. §2.1 rows (R4–R6 family).
6. R0 (catch-all): fires only when no other row's trigger holds → HOLD.

### 2.3 Repair record (LOG-290, F1–F19 → locations)

- F1: §1 — THRESHOLD-STRADDLE POSITIVE/NEGATIVE cells added (Inconclusive — hold, never license, never kill).
- F2: §2.1 — R4a/R4b/R4c added; the 3×3 (task-comparison × ρ-class) grid is total (see coverage note).
- F3: §2.1 R4 — "OR η ≥ η* licensed under the guards" disjunct restored (accounting-draft continue condition).
- F4: §2 R9 row + R9 residual-verdict pin (suspension covers only the (C,D) clauses).
- F5: §2.2 — total evaluation order pinned; R8∧R1 and R1∧R4-family conflicts resolved; R7∧R2 compatibility stated.
- F6: §2.1 η guards — paired-bootstrap CI composition specified (shared-(A) correlation); FPE-calibration sensitivity analysis required.
- F7: §2.1 — R9 suspension-bar justification written down (denominator-≈-0 degeneracy boundary; δ_min over-suspends).
- F8: §2.1 — "matched compute" OR-definition; disagreement case pinned.
- F9: §2 R3 — narrowed to the two SUB-THRESHOLD cells; deviation from the accounting draft recorded.
- F10: §2.1 η guards — η-unresolvable clause restored; reconciled with R6 (KILL rests on the licensed task comparison) and R4c (hold).
- F11: §2 R2 — "(licensed below-bar evidence vs B2)".
- F12: open-interval ρ ∈ (1−τ,1+τ); exact ρ = 1±τ → asymmetric (§1, §2.1). The accounting draft §1.3 closed-interval notation still carries the tension — conformed here only.
- F13: §2.1 — info-order strictness made variant-conditional (faithful-online only; cached variant must re-derive).
- F14: §2.1 — (D) competence anti-gaming pin; two suspension flavors distinguished.
- F15: §2 R8 — detection-bar justification (negative control uses the detection bar).
- F16: §2 R0 — HOLD catch-all; rows total as a mechanical procedure.
- F17: §1 BOUNDARY row — measure-zero CI edges pinned to hold.
- F18: §2.1 — R9 scope "task-comparison and efficiency legs alike"; deviation from the accounting draft's narrower phrasing recorded.
- F19: §2 R10 — (C,B) licensed-negative cell mapped (KILL feedback; R7 PIVOT direction if (B) > (A)).
- R6 parenthetical (fold-in): "no better at no lower cost — not a contribution".

---

## 3. What this skeleton does not do

- Does not set N, the substrate, or the (D) implementation variant — those are
  pre-registration decisions (with the feasibility-algebra requirement).
- Does not license registration (K2 P2 gate not fired), any GPU execution, or
  any capability claim (forced baselines per ROS §1 still required for any
  capability claim; any positive CLLC result = activation control only).
- τ and η* remain candidates; δ_min = 0.05 binding.
