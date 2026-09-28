# Law #14 Adversarial Review — S6-2 Pre-registration DRAFT v1 (Multi-Layer Composition)

*Reviewer: Independent Scientific Mentor & Adversarial Reviewer (fresh; did not write the packet, the draft, or any earlier review).*
*Date: 2026-09-28. Read-only review: no edits to the draft, $0 compute, no model executed, no weights touched.*
*Reviewed: `research/innovation/S6-2_PREREG_DRAFT_2026-09-28.md` (DRAFT v1, UNSIGNED, logged LOG-4417).*
*Packet: `research/innovation/NEXT_DIRECTION_SPRINT_2026-09-28.md` §S6-2 (LOG-4408, ranked #2).*
*Closure respected: LOG-4407 (EXP096 verdict) + LOG-4416 (EXP097 verdict — PIVOT fragility; static per-item L11 family closed; multi-layer compositions explicitly open).*

## Verdict: ACCEPT-WITH-FIXES (binding)

**Decisive reason.** The draft's hardest problem — earning a license for co-injection under LOG-4407's bar ("no further static per-item L11 experiments") — is solved honestly. The license-by-difference holds: two intervention nodes with eight nonlinear transformer blocks between them, a superposition null with an interaction probe, and verdicts no single-layer battery could produce. The additive-superposition null is genuinely licensed by the first-order perturbation theory EXP093's signed pre-reg actually contains (verified: §License, "to first order, Δm ≈ α⟨∇ₕm, v⟩" — and the L11-only arm captures the full downstream effect including propagation, so Δm_joint ≈ Δm_11 + Δm_20 holds at first order exactly). The three defects found are all in clarity and disclosure precision, not in the decision machinery — hence fixes, not rejection.

## What held under attack

**Risk 1 — Material difference ("bigger δ" under a new name).** All three counters survive:
(a) The W-joint control is valid: per-layer norm-tied random co-injection matches the joint's total perturbation magnitude per layer. If "bigger δ" were the story, W-joint would move with the joint; step 5 (joint ≥6 AND W-joint ≥6 → fragility PIVOT) and step 7's W-joint-flatness conjunct price this out correctly.
(b) The §2.5 decomposition is game-resistant in the safe direction. Proof (verified by this lane): under exact additive superposition, every joint-flipped item is necessarily nearly-moved by ≥1 arm — because if both |Δm_A| < 0.5·|m_B| with the correct sign, their sum cannot reach |m_B|; if either arm pushes the wrong way, the other must exceed |m_B| to flip. Therefore the 50% "nearly moved" threshold is not arbitrary: it is the sharp maximum threshold preserving the no-false-interaction-candidate guarantee. A higher threshold would manufacture false interaction-candidates; a lower one only biases toward the weaker (additive-crossing) claim. The classifier cannot manufacture a genuine-interaction CONTINUE from saturated input (adversarial case → all additive-explained → weaker CONTINUE). Its one undisclosed bias — genuine interaction that merely amplifies an already-nearly-moved arm classifies as additive-explained — is conservative (toward the weaker claim) and therefore safe. Noted as observation, not defect.
(c) The causal-graph argument is structural fact: no single-layer injection replicates two intervention nodes with nonlinear propagation between them.

**Risk 2 — L20 direction construction (degeneracy gate / HOLD path).** The tripwires are the right ones, not KILL-dodgers. If the L20 direction set is near-identical across items (≥0.95), the second intervention is not a per-item direction at all — the composition question cannot be asked, and Underdetermined is the honest verdict; a KILL there would manufacture a finding from a powerless test. The gate values are reasonable (L11 precedent 0.7923 sits far below 0.95; >2 zero-norms → HOLD is a sane tripwire). The zero-vector edge is correctly ordered: perturbation_ratio = 0 falls outside every delivery band → delivery HOLD (step 1) fires before the degeneracy gate is ever computed.

**Risk 3 — "Nearly moved" 50% threshold.** Principled, not gerrymandered — see the sharp-threshold proof above. Frozen pre-run, disclosed, descriptive-only (alters no verdict), degenerate-input behavior analyzed correctly (§4.1 item 7).

**The per-layer 0.38 cap.** The right choice, honestly fenced. Above 0.38 per-layer the question would become S6-1's (super-license fragility), not composition's — EXP097 already closed that territory as nonspecific noise. The cap keeps the composition claim inside the license it tests; "other per-layer ratios remain follow-up material" is the correct fence, not a dodge.

**Step-4 named L20-only observation.** Not smuggling. EXP077 tested geometric variants at L20, never the per-item task direction — a positive would be genuinely novel, not a resurrection. It requires p < 0.01 (not just ≥6 flips), routes the composition verdict to PIVOT regardless, and "re-licenses a dedicated follow-up" rather than claiming one. The asymmetric handling of L11-only (PIVOT with no named positive — correctly, since that would tension the closure) is exactly right.

**Decision-table completeness.** Walked for unmapped regions: foundation→HOLD, delivery→HOLD/Inconclusive, degeneracy→Underdetermined, frozen→Underdetermined, premise-fail→PIVOT, joint+control→PIVOT, flat-joint-live→KILL, full-conjunction→CONTINUE, else→PIVOT with named sub-cases (near-miss, sign-heterogeneity). The W-joint≥6/joint<6 case routes to step-6 KILL — correct (directional joint more inert than noise strengthens, not weakens, the KILL). No unmapped region; no improvisation room.

**L11-only premise arm vs LOG-4407.** Compliant. The bar forbids standalone static per-item L11 experiments aimed at the killed question; a premise check inside a materially-different experiment — which routes to PIVOT (never to re-opening L11) on a positive — is not a violation.

## Binding fixes (F1–F3)

- **F1 (§3 arm-routing rule): Strata enumeration.** §2.2 names "30 A-first / 30 C-first strata" (two sub-strata); the quantitative prediction (§0), step 7, §2.4, and §5 item 7 require "all three strata". The program convention (S6-1 v2 §0/§3: aggregate / A-first / C-first) resolves this, but the draft inherits it only implicitly. Fix: state explicitly in the arm-routing rule that the three strata are (aggregate / A-first / C-first), per the S6-1 v2 precedent.
- **F2 (§2.4): Family-wise disclosure undercounts discovery claims.** "One discovery test at 0.01 → 1% family-wise" covers only the joint-vs-B contrast. The step-4 named L20-only observation ("reported as a licensed single-layer L20 positive" at p < 0.01) is a second conditional discovery claim. The two claims are mutually exclusive (L20-positive requires premise-fail → PIVOT, which precludes the joint CONTINUE), but the union bound is still ≈2%, not 1%. Fix: disclose ≈2% family-wise across the two conditional discovery claims (or explicitly argue the mutual-exclusivity structure — either is acceptable, the current 1% is not).
- **F3 (§3 step 1): Delivery-probe scope.** "G5 probe per (layer, i, arm)" does not state that only injected (layer, arm) cells are probed — i.e. (11, L11-only), (20, L20-only), (11, Joint), (20, Joint), (11, W-joint), (20, W-joint). A non-injected cell has undefined perturbation_ratio; misread literally, every non-injected cell would trip the >2-out-of-band HOLD. Fix: enumerate the six probed cells explicitly.

## Independently recomputed (from first principles, not trusted)

- McNemar doubling b=8,c=0 → p = 2·(1/2)⁸ = **0.0078125** < 0.01 ✓ (discovery bar needs ≥8 directional flips; the ≥6 movement gate is necessary-but-insufficient, as stated)
- b=7,c=0 → p = **0.015625**, n.s. ✓
- Adversarial b=60,c=0 → p = 2⁻⁵⁹ ≈ **1.73×10⁻¹⁸** ✓ (matches §4.1 item 1)
- Delivery bands: 0.38×0.75 = **0.285**, 0.38×1.25 = **0.475** ✓
- Norm-tie assertions: 60 items × 2 layers = **120** ✓
- Budget: 300 + 60 = 360 expected ≤ 500 hard cap ✓
- "Eight nonlinear blocks between intervention nodes": layers 12–19 = **8** ✓
- EXP096 B_wrong at α=8.0: 3/21 flips ✓ (LOG-4407); ratio 0.3792 ≈ 0.38 ✓
- Constructor file `experiments/runs/EXP094_peritem_l11/constructor.py` exists (hash assertion is the executor's step-0 job)

## Non-binding observations (for the repair lane's judgment, not verdict conditions)

1. The §2.5 classifier's conservative bias (interaction-that-amplifies classifies as additive-explained) could be disclosed in one sentence; it strengthens, not weakens, the honesty case.
2. The L20 degeneracy gate's temporal order (pre-run from the construction manifest vs in-table at step 2) is unspecified; either is honest, but pre-run evaluation would save 300 passes on a degenerate construction.
3. "Spend beyond 360 requires a logged, pre-cleared exception" does not name the clearing authority (presumably CEO); the 500 hard cap being absolute makes this minor.

## Next per pipeline

Repair lane applies F1–F3 → new draft version (v1 preserved, append-only errata) → independent delta re-verification → CEO execution clearance. No pilot authorized; no GPU contact.
