# Law #14 Adversarial Review — R1 RCPA (Relational Cross-Position Amplification)

*Reviewer: Standing Research Lead, acting as Law #14 adversarial reviewer. 2026-09-24. CPU only, $0. No weights touched. No signed artifacts edited.*

**Documents reviewed in full:** `research/proposals/AMBITION_SPRINT_SYNTHESIS_2026-09-24.md` (§1 R1 section) and `research/proposals/AMBITION_SPRINT_EXPDESIGN_2026-09-24.md` (Part A toolkit + §A.4 skeleton, referenced as the governing design law).

**Candidate under review (as proposed):** per instance, r = h_L(ans_pos) − h_L(q_pos) (final-layer hidden states at answer vs. question position; positions only, zero labels). Inject h_L(ans) ← h_L(ans) + α·r̂ vs matched-norm random-direction control. 120 passes (2/item × 60 items × 1 α ≈ 0.0015 T4-h). Endpoint: flip-rate(r̂) vs flip-rate(random), McNemar + δ_min=0.05. Kill-first check ($0): cos(r̂_i, r̂_j) across items — near-static r̂ dies as a re-skin before the flip test.

## VERDICT: SIGN-WITH-FIXES

R1's core is sound: the question is precise, the kill is cheap and genuinely capable of firing, the construction is label-free, and the anti-re-skin check is the right instinct. **Twelve findings below — all fixable at pre-registration, none fatal to the candidate.** No finding warrants REJECT: every defect is a completeness or interpretation-hygiene gap, not a structural flaw in the falsification logic. R1 is promotable to signed pre-registration drafting once F1–F12 are discharged in the pre-registration document, which must itself pass a Law #14 re-review of the skeleton (§A.4.6) before any runner is built.

**What survives untouched:** Q1's precision; the differential-prediction structure (r̂ moves / static must not); the Law #7 construction (positions, not labels); the kill-first economics; the N1 (Known Combination) default and Underdetermined status.

---

## FINDINGS

### F1 [REQUIRED] — The kill criterion is a point estimate; upgrade to the CI-exclusion form

**Failure.** As stated — "flip-rate(r̂) ≤ flip-rate(random)" — the kill fires on a point-estimate comparison. At N=60 with sparse flips, a point estimate ≤ is noise-tolerant mush: it can fire on luck and, worse, it cannot distinguish "dead" from "underpowered." The packet's own §A.4 defines KILL_gross as: the two-sided 95% CI for the candidate−null contrast excludes the mechanism's own claimed minimum effect δ_claim. R1's Q4 *does* claim δ_min=0.05 as its quantitative prediction — so the machinery exists but is not applied.

**Remedy.** Pre-register the full three-row verdict table on the paired difference Δ = flip-rate(r̂) − flip-rate(random), McNemar paired structure, Tango two-sided 95% CI (program standard):
- **KILL:** two-sided 95% CI for Δ lies entirely below +0.05 (excludes the packet's own claimed effect) — the KILL_gross form. The b=c=0 flat outcome fires this cleanly.
- **HELD:** CI straddles +0.05, or sub-claim directional signal — priced powered follow-up, never CONTINUE.
- **CONTINUE:** point estimate Δ ≥ +0.05 AND one-sided McNemar p ≤ 0.05 in the r̂ direction (MDE anchor documented: b=6,c=0 → p=0.03125 at N=60).
Pin one- vs two-sided McNemar use per row. The point-estimate comparison survives only as a necessary screen, never as the verdict.

### F2 [REQUIRED] — α is unpinned; a free α is a significance-shopping license

**Failure.** "× 1 α" with no numeric value. If the pilot runs at an unpinned α and returns null, nothing stops the proponent from re-running at a new α — exactly the move cull item 18 (re-running signed batteries with tweaked bars) exists to kill.

**Remedy.** Pin α=1.0, anchored to EXP077's α=1 offset precedent on the same probe family (r̂ is unit-norm, so α is directly the injection norm). Pre-register: null at α=1.0 is a KILL, not a license to scan α. Any α variation is a new Law #15 packet.

### F3 [REQUIRED] — The pass inventory is incomplete; the 0.0015 T4-h claim is arithmetically honest but structurally short

**Failure.** Q3 budgets "2 forward passes/item (inject r̂, inject random)." Three omissions:
(a) **The r̂-computation pass.** r must be read from a clean forward pass (h_L at ans_pos and q_pos) unless archived final-layer hidden states with per-position resolution exist and are licensed. If live: 3 passes/item × 60 = 180 + smoke ≤12 = 192 > the 150-pass kill-pilot ceiling (§A.2). The packet never states which.
(b) **Smoke overhead.** §A.2.5: smoke passes count toward the 150 ceiling. Unmentioned in Q3.
(c) **Identity arm.** §A.3.4 mandates the α=0 arm reproducing the archived baseline ($0 via cache validation). Absent from Q3.

**Remedy.** Pre-registration must pick one: (i) *preferred* — verify the archived smoke records contain per-position final-layer hidden states for the 60 items, license them, compute r̂ $0 on CPU (pass inventory: 120 + ≤12 smoke + $0 identity = ≤132 ≤ 150 ✓); or (ii) re-budget to 192 passes (≈0.0024 T4-h) with explicit CEO clearance for the tier exception. The 120/79200 = 0.0015 arithmetic is confirmed honest for the stated 120 passes — the fix is completing the inventory, not the division.

### F4 [REQUIRED] — The position-identification rule is unpinned; Law #7 airtightness depends on it

**Failure.** "Positions only, zero labels" is asserted but the rule that *finds* ans_pos and q_pos is never stated. The Law #7 claim is only as airtight as this rule: a per-item rule that inspects correctness (e.g., "the position where the correct option's logit peaks") would be label leakage wearing a position mask.

**Remedy.** Pin the structural rule, e.g.: ans_pos = final token position of the pinned prompt template; q_pos = last token of the question span per the pinned template tokenizer mapping. Pre-register the prohibition: no position-selection rule may inspect correctness labels, target/foil strings, or benchmark metadata. Positions are template structure — known a priori, identical for every item.

### F5 [REQUIRED] — The static-ness check has no numeric threshold

**Failure.** "If r̂ is near-static, it is a re-skin and dies" — with no definition of near-static. An unpinned pre-filter is reviewer discretion, not a kill criterion. (Realistic failure mode it guards: r dominated by the systematic position-embedding difference between q_pos and ans_pos — constant across items — which would make r̂ a static direction in disguise. The check is the right instinct; it needs a number.)

**Remedy.** Pin a threshold with a chance-level anchor. Chance anchor: for random unit vectors in d=1024 (Pythia-410m hidden size), pairwise cos ∼ N(0, 1/1024) — anything above ~0.1 is already far above chance. Suggested bar: mean pairwise cos(r̂_i, r̂_j) > 0.5 → RE-SKIN KILL (dominant common component; the killed static family already covers it). The pre-registration pins the exact number; 0.5 is defensible, not mandatory.

### F6 [REQUIRED] — Degenerate near-zero r is unguarded

**Failure.** r̂ = r/‖r‖. If h_L(ans_pos) ≈ h_L(q_pos) on an item, r is near-zero and normalization amplifies noise — the "relational" arm becomes a noise arm on those items, biasing the pilot toward a mushy null rather than a clean kill.

**Remedy.** Pre-register a norm-floor guard: items with ‖r‖ below a pinned floor (e.g., the 5th percentile of ‖r‖ on a $0 CPU calibration over the 60 items, computed from the same archived/live states) are excluded *before* the flip test, with the exclusion count reported. Exclusion floors are §A.4 guards, not post-hoc trimming.

### F7 [REQUIRED] — The flip outcome is undefined

**Failure.** "Flip-rate" — flips relative to what, in which direction? McNemar needs a paired binary outcome per item per arm, and the packet's "wrong→right" framing needs a baseline to define "wrong."

**Remedy.** Define: outcome(i, arm) = 1 iff item i was wrong at baseline AND right under the arm, else 0. Baseline = the archived smoke records' per-item decisions (licensed $0 per §A.2.2; the identity arm validates the archive bit-for-bit). McNemar's b/c then count discordant (r̂-only vs random-only) wrong→right flips. Items right at baseline are structural zeros — handled, not subsetted.

### F8 [REQUIRED] — Demote "predicts EXP077's null as a theorem" to conjecture with explicit premises; record the layer confound

**Failure (mathematical).** The packet's theorem sketch claims: if the readout depends on cross-position comparisons with relational gradient ∇_rel, then any within-position static direction v satisfies ⟨v, ∇_rel⟩ ≈ 0 *to first order*. This is false as stated. Counter-derivation: let the relational feature be d = h_a − h_q with ∇_rel := ∂f/∂d. A within-position injection v at the answer position changes d by +v, so the first-order effect is ⟨∇_rel, v⟩ — zero only under the *additional premise* that the static v is orthogonal to the instance's relational gradient. That premise is precisely what is at issue; the sketch assumes its conclusion. (The charitable statistical reading — instance-varying ∇_rel isotropic around fixed v — is a conjecture needing its own premise, not a theorem.)

**Failure (experimental).** Even repaired, the differential has a confound: EXP077 injected at **layer 20**; R1 injects at **h_L (final layer)**. Two axes change at once (relational structure × layer). A positive R1 result would not isolate which axis mattered.

**Remedy.** (i) Relabel the EXP077-null prediction [CONJECTURE] with the missing premise stated explicitly (orthogonality of static v to ∇_rel, or the isotropy premise). The candidate does not need the theorem — the differential prediction (r̂ moves / static must not) is testable as stated. (ii) Pre-register the layer confound in the interpretation plan: on CONTINUE, the powered pilot **must** carry a static-direction-at-h_L arm (the EXP077-style arm transplanted to the final layer) to disentangle layer from relationality. Not required in the kill pilot — kill pilots kill; interpretation is priced into CONTINUE.

### F9 [REQUIRED] — The rescaling confound: r̂ is positively aligned with h_L(ans) itself

**Failure.** r = h_a − h_q contains +h_a, so ⟨r̂, ĥ_a⟩ > 0 mechanically — the injection h_a + α·r̂ partially *rescales* h_a. A positive R1 result could therefore be a scalar-rescaling effect, which is B.4's territory (its arm S exists precisely for this), not evidence for relational content. The random-direction control does not cover this: random vectors are orthogonal to ĥ_a in expectation, so "r̂ > random" does not exclude "r̂ = rescaling."

**Remedy.** (i) $0 CPU diagnostic, reported with the pilot: mean ⟨r̂, ĥ_a⟩ over items (the rescaling fraction). (ii) Pre-registered interpretation rule: if R1 returns CONTINUE *and* the rescaling fraction is large (pin: > 0.5), the powered pilot must include B.4's scalar-rescale arm (×1.1 of the final residual at matched norm) as a competing explanation — a CONTINUE without it is misattribution. For the kill pilot itself, the diagnostic is report-only.

### F10 [CONDITIONAL PASS] — Mandatory-battery gaps: sign-flip and permuted-r̂ arms deferred, exemption granted

**Assessment.** §A.3.2(b) (sign-flipped direction) and §A.3.3 (permuted/inter-item controls) nominally apply to every directional intervention. R1's Q3 carries neither. The question is whether the *kill* needs them. It does not:
- The kill question — "does r̂ carry decision-moving content beyond norm?" — is answered by r̂ vs matched-norm random. A norm/energy artifact dies to the random arm.
- Sign-flip ("is the effect sign-sensitive?") and permuted-r̂ ("is the effect item-specific, or a generic property of r̂-vectors?") discriminate *among positive explanations*. They are interpretation instruments, needed only if the pilot returns CONTINUE.

**Remedy (exemption granted, conditional).** The pre-registration may defer both arms **iff** it names them as *mandatory powered-stage arms on CONTINUE*: sign-flip arm (directionality — if r̂ and −r̂ move decisions equally, the effect is magnitude-at-position, not relational content) and permuted-r̂ arm (item j's r̂ on item i — if permuted ≡ matched, the vector carries no item-specific relational information). Deferral without this pre-commitment is denied.

### F11 [REQUIRED] — State the K2-fork independence explicitly (G1 disposition)

**Assessment.** G1's row-4 strand kills the position-masking attribution approach. R1 never asks the routing question — it is a whole-trajectory/output-side instrument, exactly the class G1's recommended guard re-scopes toward. R1's verdict table is therefore invariant under all three K2 fork outcomes:
- K2 supports routing contrast → R1 proceeds (relational readout is a different question).
- K2 supports final-position-local → R1's output-side premise is strengthened; verdict table unchanged.
- K2 row-4 strands → R1 proceeds **unaffected**; it is the licensed kind of exit.

**Remedy.** The pre-registration states: queue position behind K2 is GPU-sequencing on the user's Kaggle node, not logical dependency. R1 may be pre-registered before K2 executes.

### F12 [RECORDED] — No curvature-diagnostic dependency; no unmeasured quantities

**Confirmed.** R1's endpoint (discrete flip-rate), construction (r̂ from hidden states), and math license (relational-gradient conjecture) require no κ̂, no ε, no Hessian, no off-ray quantities of any kind. The LOG-248 identifiability result is irrelevant to R1 — its bound lives on the S3-9 ray; R1 never leaves the measured positions. Required inputs: h_L states (F3: archived or 1 live pass/item), α (F2: pinned), positions (F4: structural). Nothing else. The G2 guard does not touch R1.

---

## GUARDS DISPOSITION (LOG-250 §4, as they touch R1)

- **G1:** discharged for R1 — see F11. R1 is fork-robust by construction.
- **G2:** does not touch R1 — see F12.
- **G3:** does not touch R1 (CLLC-internal).
- **G4:** does not touch R1's science. Noted: the SVF record-correction proposal remains user-gated and unapplied; R1's novelty posture (N1 default, Underdetermined) does not depend on SVF either way.

## PROMOTION PATH (what happens next if the fixes are applied)

1. Pre-registration draft incorporating F1–F11, as a new dated protocol document (new experiment number per Law #4 — this review does not assign it).
2. Law #14 re-review of the pre-registration **skeleton** (§A.4.6) before any runner is built.
3. CEO GPU clearance; implementation agent builds the bundle (evaluator test suite per §A.2.6, startup smoke test per §A.2.5).
4. Queue position: behind K2 on the user's Kaggle node (sequencing only — F11).
5. Execution → verdict table (F1) → logged verdict. On CONTINUE: the powered pilot is pre-committed to carry the sign-flip arm, permuted-r̂ arm, static-at-h_L arm (F8), and conditional scalar-rescale arm (F9).

**What this review licenses:** R1's promotion to pre-registration drafting, conditional on F1–F11. **Does not license:** GPU execution; any efficacy, capability, or H-level claim; any change to signed artifacts; any α value other than the pinned one; any use of the bridge as a mechanism arm (Law #7 audit stands).

*— Law #14 reviewer, LOG-251, 2026-09-24.*
