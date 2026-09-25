# CLLC-vs-Baselines Matched Compute/Information Accounting — Draft v1

**Status:** DRAFT for Law #14 review. Not signed, not a pre-registration.
**Date:** 2026-09-24. **Author:** prior-art verification agent (parent-assigned).
**Cost:** $0, CPU only. **Scope:** resolves LOG-250 guard G3 — the (C)>(B2)-but-(C)<(D)
efficiency cell had no operationalized "strictly less information/compute" and would
otherwise be decided by reviewer discretion.
**Source-of-truth grounding:** arm definitions from
`research/theory/CLLC_FORMALIZATION_2026-09-23.md` §8 (EXP-CLLC-01 skeleton, draft);
prior-art facts from arXiv:2604.19018 (Activation-LQR, primary source fetched
2026-09-24) and arXiv:2602.01654 (Steering Vector Fields, primary source fetched
2026-09-24); LOG-249's three-attribute novelty boundary.

All numbers below are formulas, not measurements. No invented figures.
Epistemic labels per repo §5 follow each substantive claim.

---

## 1. What "matched compute" means operationally

### 1.1 The unit: forward-pass-equivalent (FPE) per instance [DEFINITION]

1 FPE = one full frozen forward pass of the test model at the experiment's
batching. Derived quantities, by standard autodiff ratios [ASSUMPTION — to be
calibrated empirically per harness; report the calibration]:
- 1 Jacobian–vector product (JVP) ≈ 1 FPE
- 1 vector–Jacobian product / backward pass (VJP) ≈ 2 FPE
- Vector additions, norm rescalings, scalar probes ≈ 0 FPE (negligible)

### 1.2 Per-arm FPE ledger (formulas; fill at pre-registration)

| Arm | Passes / autodiff per instance | FPE (formula) | Online vs amortized |
|---|---|---|---|
| (A) best fixed open-loop | 1 forward (fixed v̂, α*) | 1 | online |
| (B) open-loop multi-layer sequence | 1 forward (precomputed multi-layer injection) | 1 | online |
| (B2) adaptive open-loop | 1 probe forward (margin probe) + 1 forward (per-instance α_i injection) | 2 | online |
| (C) CLLC Jacobian-free feedback | 1 probe forward (records the r=1 margin probe at each layer = the margin trajectory) + 1 forward with per-layer corrections | 2 | online; per-layer corrections ≈ 0 FPE |
| (C8) CLLC rank-8 | as (C) with rank-8 probe (8 dims × L layers) | 2 | online |
| (D) Activation-LQR | 1 forward (trajectory) + layer-wise Jacobians (per instance) + LQR gain solve | 1 + (JVP/VJP ledger) + (Riccati solve) | online; see §2.3 |
| (E) negative control (permuted probe) | 1 probe forward (permuted) + 1 forward | 2 | online |

**Amortized accounting (separate from online, per the §G1b two-number rule):**
one-time per-task costs — P4 calibration (≈800 passes), per-task gain/reference
precomputation, any A-LQR setpoint-signal construction, and each arm's
controller-tuning cost — are logged as amortized FPE and reported alongside
online FPE, never folded into it. In particular: (C)'s scalar gain k is tuned
on CPU from archived (margin, injection) pairs per the formalization §7 —
the archived-pair count and the CPU-only status go in (C)'s amortized row;
(B2)'s α_i rule is computed online from the probe (no tuning cost) —
if any offline fitting is introduced for α_i it goes in (B2)'s amortized row.
No arm may carry hidden tuning compute in its online FPE. [FIX-LOG-285: tuning-cost pinning]

### 1.3 When arms are "compute-matched" [DEFINITION]

Arms X and Y are *compute-matched* iff
FPE_X / FPE_Y ∈ [1−τ, 1+τ], with τ = 0.25 pre-registered (reviewable).
If |FPE_X/FPE_Y − 1| > τ, the comparison is reported as
**asymmetric** and the efficiency ratio below is the primary instrument,
not the raw ΔM comparison. Exact boundary (ratio = 1±τ) is read as
**asymmetric** — the safe direction: no silent parity at the tolerance edge.
[FIX-LOG-285: boundary rule pinned; τ retained as a candidate for ratification,
with the rationale that every planned exact-parity pair sits at ratio 1.0, so τ
only absorbs harness calibration error and rejects 1-vs-2 FPE classes and
(D)-class asymmetries.]

**Explicit residual-asymmetry rule for (D)** (per the §8 skeleton's instruction
to "report any residual information/compute asymmetry explicitly rather than
hiding it"): because (D) computes layer-wise Jacobians per instance, exact FPE
parity with (C) may be infeasible. The pre-registration must then publish
ρ = FPE_D / FPE_C and fall back to §4's efficiency verdicts. "Matched compute"
for (C)-vs-(D) therefore means **ρ-parity OR efficiency dominance (η ≥ η*)** —
either leg suffices, and neither may be silently assumed.
[FIX-LOG-285: "min(ρ-parity, efficiency dominance)" was not an operational
definition; replaced with an explicit OR.]

---

## 2. What "matched information" means operationally

### 2.1 Information ledger per arm [DEFINITION]

Each arm declares what it may know, **separately for online and amortized**
(the §G1b two-number rule applies to information, not just compute —
[FIX-LOG-285]: without this, (D) could be run with cached Jacobians online
and the layer-wise Jacobian cost would hide in the amortized column while
online information claimed "none"). Information is ordered by a partial order;
strictly-less-information requires ≤ on all axes and < on at least one.

| Axis | (B2) | (C)/(C8) | (D) Activation-LQR |
|---|---|---|---|
| Observation of current state (online) | 1 scalar (single pre-pass margin probe) | margin trajectory: r=1 scalar per layer = L scalars ((C)); r=8 → 8L scalars ((C8)) | full residual stream, every layer, every step |
| Observation (amortized) | — | archived (margin, injection) pairs for the k line-search (count logged) | cached Jacobians/gains IF the cached-(D) variant is used; setpoint-signal construction |
| Model Jacobians (online) | none | **none** (this is the narrowed novelty attribute) | full layer-wise Jacobians **iff** (D) is the faithful-online variant; none if cached |
| Model Jacobians (amortized) | none | none | full layer-wise Jacobians iff (D) is the cached variant |
| Dynamics model | none | none (no learned dynamics; feedback law is static gain on observed error) | LTV linearization built from the Jacobians |
| Reference / setpoint | per-instance α_i from the margin probe (label-free, frozen-model-internal) | reference margin trajectory m*_ℓ (output-bridge direction's induced trajectory OR mean correct-answer trajectory; label-informed at definition time only, never per test item — Law #7 inherits) | relational reference per §2.2 (NOT the paper's semantic setpoint — see the off-label note) |
| Controller form | open-loop gain on probe | u_ℓ = −k(m_ℓ − m*_ℓ) style static feedback on the r-dim observed error | LQR feedback controller from Riccati solve on the LTV model |

**Probe pin** [FIX-LOG-285]: "1 probe forward" in §1.2 means one full forward
that records the r-dim probe at every layer — the margin trajectory the §7 law
needs — not one scalar per instance. (B2) genuinely observes 1 scalar; (C)
observes L; (C8) observes 8L. This observation-info difference is part of what
the feedback treatment *is* (the law needs the trajectory), and it is made
explicit here rather than hidden inside "scalar probe".

**(D) implementation-variant pin** [FIX-LOG-285]: the pre-registration must
declare, before launch, whether (D) is the **faithful-online** variant
(per-instance layer-wise Jacobians online, per LOG-277's primary-source
reading of the A-LQR paper) or a **cached** variant (Jacobians/gains computed
once per task, amortized). The variant changes FPE_D by orders of magnitude
and flips the Jacobian axis of this ledger; it may not be chosen post-hoc.

### 2.2 Parity constraints for the (C)-vs-(D) contrast

To isolate *the controller* from *the setpoint*, both (C) and (D) receive the
**same reference construction** on the relational task (the §H7/§E-box rule:
output-bridge-induced trajectory or mean correct-answer trajectory, per
whichever the §H battery licenses). Setpoint construction is logged as
**shared information**; it may not be counted as a (C) advantage.

**Off-label note** [FIX-LOG-285]: the shared construction substitutes the
relational reference for A-LQR's published semantic (toxicity/truthfulness-style)
setpoint. (D) is therefore **A-LQR's closed-loop Jacobian controller machinery
with the relational reference substituted** — not the published A-LQR system.
A (C) win over (D) licenses a claim about the *controller difference* on the
relational task, never superiority to the published A-LQR system.

**Attribution logic for (C)-vs-(B2)** [FIX-LOG-285]: (C) observes the margin
trajectory (L scalars) where (B2) observes 1 scalar. If a (C) win were driven
by richer observation rather than feedback, the (E) negative control must catch
it: (E) destroys observation information (permuted probe) at the same FPE=2,
so (E) > (A) fires the HALT row. (E) ≈ (A) is what licenses attributing a
(C) win to the feedback law rather than to probe information.

### 2.3 The (D) cost reality [OBSERVATION from primary source + arithmetic]

The A-LQR abstract describes Jacobians computed "at different reachable
activations within the exact same transformer layer" with "exceptionally high
correlations" — i.e., their implementation recomputes Jacobians online.
A layer-wise full Jacobian at hidden size d requires ~d JVPs per layer
(≈ d·L JVPs total per instance at L layers) or equivalent backward passes.
This is the structural reason the §8 skeleton says (D) is "matched on budget
as closely as its formulation permits": FPE_D ≫ FPE_C is the *expected*
outcome, and the comparison is therefore an efficiency contest, not an
FPE-parity contest. [INTERPRETATION]

---

## 3. "Competitive" operationalized (resolves G3)

**Primary endpoint:** decision-flip rescue rate vs arm (A). Statistics per
program standard: McNemar exact test, Tango 95% CI on the paired difference,
δ_min = 0.05 (binding stats revision — no verdict on p-value alone).

Let Δ̂(X,Y) = ΔM_X − ΔM_Y with two-sided 95% CI [L, U].

| Verdict label | Operational rule | Meaning |
|---|---|---|
| (C) **beats** (B2) | L(Δ̂(C,B2)) > δ_min | feedback adds value beyond cheap per-instance adaptivity |
| (C) **indistinguishable** from (B2) | CI covers 0 and U(Δ̂(C,B2)) < δ_min | no licensed feedback claim; arm (C) is dead weight |
| (C) **dominated** by (B2) | U(Δ̂(C,B2)) < −δ_min | feedback machinery actively hurts |
| Underpowered | CI covers 0 and U ≥ δ_min | **Inconclusive** — hold for powered re-test; never a license (asymmetric verdict rule) |
| Sub-threshold positive | CI strictly inside (0, δ_min) (L > 0, U < δ_min) | real but below the binding minimum: **no licensed feedback claim**; CONTINUE open-loop adaptivity only, KILL the feedback claim (mirrors §8's "CONTINUE adaptivity as open-loop") |
| Sub-threshold negative | CI strictly inside (−δ_min, 0) (L > −δ_min, U < 0) | symmetric: no licensed claim; CONTINUE open-loop adaptivity only |
| Boundary | exact equalities (U = δ_min with CI covering 0 → Underpowered; U = −δ_min with CI covering 0 → no cell fires → hold as Inconclusive; L = δ_min exactly → not beats → hold) | at an exact boundary the threshold is unresolvable: **never a license** — hold, do not fire the adjacent CONTINUE-with-claim |

**Efficiency ratio** (for the (C)-vs-(D) cell): η = (ΔM_C / FPE_C) / (ΔM_D / FPE_D).
Pre-registered threshold η* = 1.0:
- η ≥ 1.0 → (C) is at least as compute-efficient as the existing closed-loop controller.
- η < 1.0 → (C) is cheaper-but-weaker — no novelty license (the §8 kill rule).

**η guards** [FIX-LOG-285]:
- η is computed **only when both ΔM_C and ΔM_D are licensed positive**
  (L(Δ̂(C,A)) > 0 and L(Δ̂(D,A)) > 0 at minimum). **Degenerate-contest rule:**
  if (D) itself shows no licensed effect on the relational task
  (L(Δ̂(D,A)) ≤ 0 — realistic, since A-LQR's verified tasks are behavior
  steering, not relational reasoning), the (C)-vs-(D) efficiency comparison is
  **suspended and reported only**: beating a non-working baseline licenses
  nothing, and η is degenerate (division by ≈0).
- η is reported **with the component CIs** (Tango intervals on ΔM_C, ΔM_D);
  a verdict on the η point estimate alone is not licensed — if the η-relevant
  intervals cannot resolve the η* threshold, the efficiency cell is Inconclusive.
- **Leniency note:** at the expected ρ ≫ 1, η ≥ 1.0 is a weak floor
  (e.g. ρ = 20 needs only ΔM_C ≥ ΔM_D/20). η ≥ η* licenses **CONTINUE as an
  efficiency investigation only** — it never licenses the novelty claim itself.
  A claim-grade efficiency result needs a stricter, separately pre-registered
  bar. η* = 1.0 stays a candidate for ratification, not a ratified bar.

### 3.1 The full between-the-arms decision table (no reviewer discretion)

| Cell | Rule | Verdict |
|---|---|---|
| (C) ≤ (A) at **injection-matched** budget (U(Δ̂(C,A)) ≤ 0; "budget" = the §8 skeleton's post-hoc Σ_ℓ‖u_ℓ‖² equalization, NOT FPE — the FPE asymmetry FPE_C/FPE_A = 2.0 is disclosed, not hidden) | §8 kill rule | **KILL** CLLC-as-feedback |
| (C) > (B) but not beating (B2) (U(Δ̂(C,B2)) < δ_min) | §8 kill rule | **KILL** feedback machinery — do not overclaim vs weak open-loop baselines; CONTINUE adaptivity as open-loop only |
| (C) sub-threshold vs (B2) (CI strictly inside (0,δ_min), or boundary no-cell outcomes of §3) | §3 catch-all | **KILL** the feedback claim; CONTINUE adaptivity as open-loop only — no licensed feedback claim |
| (C) beats (B2) AND (C) ≥ (D) at matched info/compute (L(Δ̂(C,D)) ≥ 0 with ρ ∈ [1−τ,1+τ] or η ≥ η*) | §8 continue rule | **meaningful control-method result** — CONTINUE to deeper investigation |
| (C) beats (B2) BUT (C) < (D) (U(Δ̂(C,D)) < 0) | efficiency cell | CONTINUE as an efficiency result **iff** (C) uses strictly less info/compute than (D) (ρ > 1+τ — exact boundary ρ = 1+τ reads asymmetric; the info-order strictness is automatic by construction on the Jacobian axis for the faithful-online (D) variant, so the operative gate is ρ) **and** η ≥ η* with η licensed under the §3 guards; otherwise **KILL** the novelty claim |
| (B) > (A) with (C) ≈ (B) (CI covers 0) | §8 pivot rule | **PIVOT** to open-loop multi-layer |
| (E) > (A) (L(Δ̂(E,A)) > 0) | §8 halt rule | **HALT** — budget confound; feedback claims suspended; redesign |

**"Strictly less information/compute" is now defined:** FPE_C < FPE_D beyond τ
(i.e. ρ > 1+τ; the §2.1 information order's strictness on the Jacobian axis is
automatic by construction for the faithful-online (D) variant, so it does no
independent gate work — recorded here explicitly rather than left as a
vacuous conjunct [FIX-LOG-285]). The shared-reference rule (§2.2) is what
carries the information-isolation work for the (C)-vs-(D) cell.
"Competitive" is now defined: the CI rules of §3 plus η ≥ η* where applicable
(η under the §3 guards).

---

## 4. What this draft deliberately does NOT do

- No FPE numbers for (D)'s Jacobian ledger (depends on the paper's online-Jacobian
  implementation, which we have not executed — code repo NOT fetched; §5).
- No τ commitment beyond the draft proposal (τ = 0.25 is a placeholder for
  Law #14 to ratify or replace).
- No setpoint-construction choice (bridge-induced vs mean-correct-answer) —
  that is §H7's jurisdiction, not this draft's.
- Does not license registration: CLLC remains conditional on K2's P2 gate
  (§8 skeleton trigger) plus Law #14 review of this accounting plus the
  SVF/A-LQR verifications recorded in LOG-277.

## 5. Open items for Law #14

1. Ratify or replace τ = 0.25 and η* = 1.0 (rationale recorded in §1.3/§3).
2. Confirm the FPE calibration (§1.1 ratios) on the actual harness before signing.
3. Confirm (D)'s per-instance Jacobian cost empirically or from the repo
   (repo URL from the paper's abstract: https://github.com/trustworthyrobotics/lqr-activation-steering — NOT fetched; liveness UNVERIFIED).
4. Confirm the probe-label hygiene for (B2)/(C): the margin probe must be
   label-free (frozen-model-internal); any label leakage collapses (B2)/(C)
   into the Law #7 demotion.
5. Pin the (D) implementation variant (faithful-online vs cached, §2.1) and the
   probe's layer coverage (§2.1 pin) in the §8 skeleton before registration —
   neither may be chosen post-hoc. [FIX-LOG-285]
6. Decision-table feasibility algebra (EXP079 lesson, LOG-138): the
   pre-registration must show, from N, δ_min, and the endpoint's CI geometry,
   that the **beats** cell is algebraically reachable — otherwise the trial is
   futile by construction and must not launch. [FIX-LOG-285]
