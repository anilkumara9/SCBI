# Law #14 Adversarial Review — R2 (Newton-vs-gradient duel) candidate packet

**Reviewer:** Independent Law #14 Reviewer (binding; outside lab hierarchy)
**Date:** 2026-09-24
**Packet reviewed:**
- `research/proposals/AMBITION_SPRINT_SYNTHESIS_2026-09-24.md` — R2 section (Q1–Q4, kill criterion, unique support)
- `research/proposals/AMBITION_SPRINT_EXPDESIGN_2026-09-24.md` — X2 section (arms, KILL/CONTINUE, pass inventory) + Appendix §A.3 (negative-control battery)

**Verdict: SIGN-WITH-FIXES** — 10 findings (F1 structural; F2–F9 required; F10 minor). None REJECT-grade: the duel *concept* is sound and worth repairing; the arm *specification* is not. R2 is promotable to pre-registration drafting once F1–F10 are discharged, with a Law #14 re-review of the skeleton before any runner is built.

---

## F1 [REQUIRED — structural]: the Newton arm is vacuous as specified; the KILL criterion fires tautologically

The packet specifies two central-difference probes **along g** for the Hv product, then a "Newton step at norm ρ using Ĥ⁻¹g from the two probes" (X2 Arms (b); Q3).

Two probes along a single direction yield exactly one Hessian-vector product, Hĝ — curvature information *only* along the gradient direction. The only Newton-type step computable from rank-1 directional curvature is the scalar-curvature step α*·g with α* = −‖g‖²/(gᵀHg): **parallel to the gradient by construction**. The packet then mandates equal-L2-norm rescaling to ρ. Rescaling α*·g to norm ρ yields ρ·ĝ — bit-identical to arm (a), the GD step.

Consequences, all verified against the packet text:
- As specified, median(ΔM_Newton − ΔM_GD) ≡ 0 *by construction*. The KILL criterion (median ≤ 0, two-sided p ≥ 0.10, |median| < 0.01) fires tautologically. The "second-order family" would be killed by an identity, not an experiment.
- The CONTINUE gate's "Newton > random" prong collapses to "GD > random".

Minimum honest repairs (pre-registration must pick one):
- **(a, recommended)** Drop equal-norm for the Newton arm: let it keep its curvature-derived natural step length α*‖g‖. The duel becomes GD-at-fixed-ρ vs Newton-at-natural-length — i.e., *does curvature-derived step-length selection beat a fixed-norm gradient step?* This is the actual Newton advantage, the cheapest non-vacuous duel, and it restores the F4 theorem license. Q1's matching clause must be rewritten accordingly.
- **(b)** Keep equal norm but buy a genuine Newton direction: k>1 Hv products → small Krylov/Lanczos subspace direction distinct from g. Re-price the pass budget.
- **(c)** Specify a different Hessian approximation (diagonal, etc.) with its own mathematical license.

## F2 [REQUIRED]: KILL fires on a dead apparatus — no sensitivity precondition

CONTINUE requires Newton > random (p ≤ 0.05), but KILL (Newton ≡ GD) requires nothing about whether either arm moves the proxy at all. If the top-2 margin proxy is flat/unresponsive to activation perturbations at the chosen site, GD ≡ random ≡ noise, Newton ≡ GD, |median| < 0.01 — and the second-order family dies on a dead apparatus. This is the failure mode the §A.3 battery's item 4 (identity/apparatus arm) exists to prevent, and the same class of guard was required in EXP083's review (LOG-251).

**Fix:** pre-register GD > random (one-sided, pilot bar p ≤ 0.10) as a *sensitivity precondition* for the KILL verdict. Precondition fails → INVALID/UNINFORMATIVE-PROXY, never KILL. (This makes arm (c) load-bearing — see F6.)

## F3 [REQUIRED]: the family-kill overreaches — three unclosed escape hatches

The flagship is *raw, undamped* Newton with a *finite-difference* Hessian from 2 probes, *single step*, on a *non-convex* landscape (an LLM's activation-margin surface). A loss is consistent with all of:
- **(a)** Indefinite/ill-conditioned local H — the regime where damped Newton / Levenberg-Marquardt / trust-region methods exist. Raw Newton failing on non-convex problems is textbook, not news.
- **(b)** Finite-difference noise — exact Hv via double-backprop/autodiff costs ~2–3× a gradient pass with no finite-difference noise at all. The packet tests "finite-difference second-order at 2 probes" and claims to kill "second-order".
- **(c)** Quasi-Newton (curvature accumulated across steps) — a multi-step family member a single-step flagship cannot represent.

"Five Newton steps will never be cheaper than five GD steps" closes none of these: (a)–(c) are about *per-step quality*, not step count.

**Fix:** scope the KILL to the tested flagship — "cheap finite-difference undamped single-step Newton" — and state explicitly that damped / quasi-Newton / exact-Hv variants are NOT killed by this pilot (each needs its own Law #15 packet). Alternatively close the hatches by design — but that is a different, more expensive pilot.

## F4 [REQUIRED]: the cited theorem does not license the prediction under the experimental contrast

Q4 cites [THEOREM] "for a quadratic objective, Newton converges in one step while GD needs O(κ(H)) steps" → prediction "Newton's margin gain ≥ GD's, gap growing in measured condition number." One-step convergence requires the *unit* Newton step −H⁻¹g. The experiment norm-rescales the step to ρ, destroying exactly the cited property. Under equal-norm rescaling the theorem predicts nothing about the contrast; the prediction is a [CONJECTURE] about directional quality, not a theorem consequence.

**Fix:** repair (a) of F1 (natural step length) restores the license; otherwise demote the epistemic label to [CONJECTURE] and rewrite the prediction.

## F5 [REQUIRED]: the cost-fair duel is missing — the "never cheaper" argument is circular

Newton costs 3 passes/step (2 probes + step) vs GD's 1. The contrast is 1 Newton step vs 1 GD step *at equal norm* — but Newton's classical justification is *fewer, better-scaled steps*. The cost-fair duel at the door is 3-pass Newton vs 3-pass GD (e.g., three GD steps). The packet kills the family for losing a per-step-norm comparison whose terms exclude the family's raison d'être (step-count reduction), then cites per-step cost as the reason.

**Fix:** add the pass-matched GD arm (3 GD steps, 3 passes) as the primary cost-fair contrast. The equal-norm directional duel may remain as a secondary screen with its kill scope narrowed to directional quality only.

## F6 [REQUIRED]: pass inventory is short in two places

- Arm (c), the random-direction step (1 pass/item), is listed in Arms but absent from the "24×5 = 120" inventory. True forward-pass count: **6/item → 144 passes**.
- The gradient g is unbudgeted. Hv via central differences of *gradients* needs two backward passes (≈2× forward cost each); the initial g needs one more. Hidden cost ≈ 5 forward-equivalents/item atop the forward inventory — the 0.0015 T4-h claim is understated by roughly 2×. (If forward-mode/JVP is intended instead, the packet must say so — it says finite differences.)

**Fix:** honest inventory — 144 forward passes + backward costs disclosed in forward-equivalents, with CEO clearance for the overage — or drop/merge an arm.

## F7 [REQUIRED]: "measured κ" is a misnomer; too-flat vs too-noisy is undeterminable as designed

Two probes along g yield one Rayleigh quotient ĝᵀHĝ — *directional* curvature, not the condition number κ = λmax/λmin (which needs extremal eigenvalues). The Q4 prediction "gap growing in the measured condition number" references an unmeasurable quantity. Further, the packet claims "the experiment distinguishes which" (too-flat vs too-noisy). With a single finite-difference spacing h there is no noise-floor estimate: "small estimated curvature" and "curvature estimate drowned in noise" are indistinguishable.

**Fix:** rename to directional curvature κ̂_dir; pre-register only the too-flat rule (κ̂_dir ≈ 0 → second order negligible, consistent with the LOG-248 κR² bound); mark too-noisy UNDETERMINED absent a replication probe at a second h (cheap: +2 probes/item — or explicitly decline and record the limitation).

## F8 [REQUIRED-CLARIFICATION]: three unpinned quantities — ρ, site, seeds

- **ρ** (norm budget): value and selection rule unpinned. Both arms are scale-sensitive (saturation/overshoot vs noise floor). Pin ρ with rationale (e.g., anchored to the S3-9 α-grid or a $0 sweep).
- **Site:** "same site" is never pinned to a layer/position. Program history (EXP077 L20 vs R1 h_L — a LOG-251 F8 finding) shows layer choice changes outcomes. Pin layer + position with rationale.
- **Seeds:** the random arm (c) and any stochasticity need a pinned seed scheme (cf. EXP083's 20260924+i).

## F9 [REQUIRED]: verdict table incomplete

X2 has KILL and CONTINUE only. Missing rows, all reachable: (i) Newton > GD but ≡ random → HELD (step-noise, not curvature — neither kill nor continue licensed); (ii) GD ≡ random → INVALID per F2 (apparatus dead); (iii) underpowered straddle (p ∈ (0.05, 0.10), |median| ≥ 0.01) → HELD. The packet's own appendix standard ("pilots KILL or HOLD") is not met.

## F10 [MINOR]: N=24 and the KILL-by-default asymmetry

At N=24 the KILL's non-significance prong (two-sided p ≥ 0.10) is satisfiable by low power alone; the |median| < 0.01 margin-units prong does the real work but is uncalibrated (no justification that 0.01 margin units is below decision-relevance). Recommend making the effect-size prong binding with pre-registered calibration, or an explicit underpowered-HELD rule. Not blocking.

---

## What survives

The duel *concept* — a cheap, pre-registered second-order screen converting the LOG-248 curvature bound from a defensive weapon into an offensive one — is sound and worth repairing. The Law #7 posture is clean: the top-2 margin proxy comes from the model's own logits; no labels touch construction, selection, or scoring (§A.3.1, §A.3 items 1+5 satisfied). The kill-first instinct is right; the machinery needs the ten fixes above.

## Promotion path

Pre-registration drafting discharging F1–F10 → Law #14 re-review of the skeleton → implementation bundle → queue. F1's arm redesign is the load-bearing fix (recommended repair (a): natural Newton step length, Q1 matching rewritten); F2/F3/F9 reshape the verdict table and kill scope; F6 re-prices the pilot.

*Logged as LOG-260 in reports/research_log.md. $0 spent, CPU only, no weights touched, no signed artifacts edited.*
