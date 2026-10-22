# Law #14 Independent Review — EXP135 B2/EVAL Pre-registration Draft

**Artifact:** `research/prereg/EXP135_PREREG_EVAL_2026-09-30.md` (DRAFT)
**Reviewer:** independent Law #14 lane (LOG-4840 pre-assigned, CEO). No prior involvement in the draft.
**Verdict:** **SIGN-WITH-FIXES** — six required fixes (F1–F6), two advisories (A1–A2). No blocking defect in the hypothesis, decision table, or mathematical core.
**Date:** 2026-09-30

---

## What was read in full

- The draft (`EXP135_PREREG_EVAL_2026-09-30.md`), all 9 sections.
- LOG-4839 (draft record, staleness re-diff, ρ\* normalization correction).
- `theory/LOOP_SPEC_DRAFT.md` — §1.1 (tuning grid), §2.2 (E-step scores, view precondition fix S2), §2.3 (selection tie-break).
- `~/workspace/SCBI/AGENTS.md` (the 14 laws, epistemic labels).
- Independent spot-checks: full-log grep for E-validity executions (clean), Spearman-hit disambiguation, numerical verification of the §3.5 derivation.

---

## Verified PASS (no fix needed)

**P1 — Decision table exact and exhaustive.** CONTINUE (ρ̄\* ≥ 0.7 ∧ p < 0.05), KILL (ρ̄\* ≤ 0.3), HELD (else), RUN-INVALID (any §3.7 guard). Precedence RUN-INVALID > KILL > CONTINUE > HELD correctly handles exact-boundary data (ρ̄\* = 0.3 → KILL; ρ̄\* = 0.7 ∧ p < 0.05 → CONTINUE). The KILL bar carries no p-conjunct — correct, absence of signal is the kill. The CONTINUE p-conjunct is nearly redundant (ρ̄\* ≥ 0.7 is ~8.4σ under H0) but harmless and explicit.

**P2 — ρ\* normalization correctly derived and applied.** Independently verified numerically: with causal ranks [1, 5.5×8] and score ranks a permutation of 1..9, tie-corrected Spearman ρ_i = (5−k_i)×0.1369306… (draft: 0.136931, correct to 6dp), ρ_max = 0.5477. The drafting correction was mathematically necessary — the sprint's unnormalized ρ ≥ 0.7 CONTINUE bar is unachievable — and is correctly applied. Bar semantics verified: ρ̄\* ≥ 0.7 ⟺ bridge mean score-rank ≤ 2.2; ρ̄\* ≤ 0.3 ⟺ ≥ 3.8.

**P3 — LOOP_SPEC §2.2 citation faithful.** C_cons, M̃, S_E formulas match the signed spec verbatim; m=5; the view precondition (fix S2) is correctly cited including the Law #8 exclusion rule; the λ grid {0.5, 0.7, 0.9} matches §1.1. The spec's tie-break ("higher C_cons, then lower index") genuinely exists — §2.3, line 206 — so the draft's "the spec's rule" is not invented. (Its *application* to the ranking statistic is the problem — see F1.)

**P4 — No circularity.** The scores are target-free: ŷ_j ranges over {t_target, t_foil} (the option set, never the correctness label); M_j is full-vocabulary top-1 minus top-2; μ_M/σ_M come from unintervened D_sup forwards. The causal ranking is registered from licensed results (EXP077 +10pp; EXP131 randoms ΔM=0). The scores cannot see the causal labels. Law #7 holds for the primary and secondary scores.

**P5 — Worth-it gate holds (all 7 points).** Exact question, mechanical decision, cheapest test (3,750 forwards — the "~1h" corrected to "~2h" honestly), mathematical license (signed spec + bridge anchor + label-free rank statistics), quantitative prediction (ρ̄\* ≥ 0.7), breaking point (ρ̄\* ≤ 0.3), non-resurrection (§6), summit filter, falsification-first (KILL is the prior, easy to earn).

**P6 — Non-resurrection audit sound.** Independently re-verified: E-validity stands as [CONJECTURE] since the LOG-3842 sign-off; no execution in the log tests label-free E-step ranking; the log's Spearman hits are unrelated (EXP083/084 evaluator-monotonicity, curvature correlations, other candidate-ranking contexts). The killed families all test causal efficacy of directions — a different claim class from evaluator rankability. The §H7 bridge disclosure (§1.2) is honest: causal *efficacy* (+10pp, p=0.03125) is undisputed and is the anchor; autonomous *mechanism* is explicitly out of scope.

**P7 — Breaking-point coverage (structure).** (a) Δθ=0, (b) bridge pin, (c) bench pin, (d) view-precondition exclusions, (e) degeneracy (the blind-tap lesson), (f) budget audit, (g) readout-sensitivity positive control — the (g)/(h) control is correctly mandatory post-rehabilitation. Exit-44 discipline consistent throughout.

**P8 — Law #11 labeling.** [HYPOTHESIS]/[FACT]/[ASSUMPTION]/[INTERPRETATION]/[CONJECTURE] placed correctly; the 8-randoms inertness is honestly labeled [ASSUMPTION] with its failure mode recorded in §8.

---

## Required fixes

### F1 — Tie-break bias: randomize score-rank ties (statistical defect)

**Problem.** §3.5 breaks score-rank ties by "the spec's rule: higher C_cons, then lower candidate index." The bridge is candidate C1 (lowest index), so under *any* score degeneracy the bridge deterministically receives score-rank 1 → ρ\*_i = +1.0 per degenerate item. This (a) contradicts §3.5's null distribution (k_i uniform on {1..9}), which holds only if ties are measure-zero, and (b) biases the endpoint pro-CONTINUE: guard (e) trips only at ≥30/60 degenerate items, but 18+ degenerate items contributing +1.0 each suffice to push a true-null ρ̄\* above the 0.3 KILL bar (d/60 with genuine signal 0). A total apparatus failure mode (blind tap → all scores degenerate) would read as ρ̄\* = 1.0 → false CONTINUE, caught only if (e)/(g) trip first.

**Fix.** Break score-rank ties by a seeded random permutation (pinned seed, e.g. 135033, specified in the draft) for the ranking statistic. Document the distinction: the spec's tie-break (§2.3) governs the loop's *selection* step; the ranking test pre-registers its own tie-break. Under H0 this makes the uniform null EXACT and makes degenerate items contribute E[ρ\*_i] = 0 (noise, not bias).

### F2 — Exclusions must parameterize the endpoint, null, and budget

**Problem.** Guard (d) permits up to 6 view-precondition exclusions, but three quantities assume n=60 exactly: (a) §3.5 defines ρ̄\* = (1/60)Σρ\*_i; (b) §3.5's permutation null draws 60 uniforms; (c) §3.7(f) pins the budget at "3,750 ± 0" = 9×60×5 + 300 + 750. With e>0 exclusions, all three are wrong (intervention forwards = 9×(60−e)×5; cached passes = 5×(60−e)).

**Fix.** Determine e from the bench metadata BEFORE any forwards. Parameterize with n = 60−e: ρ̄\* = (1/n)Σ_{included}; null draws n uniforms per replicate; budget(f) = 9·n·5 + 5·n + 750 + N_g (see F3). The 0.7/0.3 bars are scale-free and apply unchanged. (e > 6 → RUN-INVALID per (d), already specified.)

### F3 — (g) control forwards unaccounted; probe underspecified

**Problem.** §3.7(g) mandates the readout-sensitivity control, but (f)'s "3,750 ± 0" budget has no room for its forwards — the (g) forwards would themselves trip (f) ("any unaccounted forward → RUN-INVALID"). Additionally, (g) does not specify the probe norm or its position in the run order.

**Fix.** Specify: N_g (number of (g) forwards), the probe norm (pin one: ‖δ‖ = 16.0 per the EXP133 (h) precedent, or = B — state which), (g)'s position (before the first intervention forward, per the EXP131/133 pattern), and add N_g to the (f) budget.

### F4 — Seed hygiene

**Problem.** (a) §3.7(g) claims "seed 135008, independent draw" — but 135008 is the C2–C9 randoms' seed (§3.2). A draw from the same seed/stream may coincide with a candidate; "independent" is false as written. (b) The three "(independent stream)" claims (135031 global/bench, 135008 randoms, 135031 permutation null) assert a separation mechanism the draft never specifies — if the executor uses one global RNG, the streams are merely sequential, not independent.

**Fix.** (a) Assign (g) a distinct seed (e.g., 135009) with explicit stream separation. (b) Specify the stream-separation mechanism for every named stream (e.g., `np.random.default_rng(SEED)` per stream, or `SeedSequence(135031).spawn(k)`), so the executor's implementation is checkable against the draft.

### F5 — Exploratory "probe-decodability delta" undefined; Law #7 risk

**Problem.** §3.3 lists "probe-decodability delta" as EXPLORATORY with no definition anywhere (sprint doc mentions it once, undefined). A decodability probe is typically trained on labels — if this one is, it violates §3.1's "bench ground-truth labels are used nowhere."

**Fix.** Define the score precisely, including its label-contact status. If it requires bench labels: either (i) amend the Law #7 section to explicitly fence it as label-contacting exploratory (with contamination controls), or (ii) drop it. An undefined quantity has no place in a pre-registration.

### F6 — Fresh-randoms inertness needs a label-free breaking point

**Problem.** §3.4's [ASSUMPTION] (the 8 fresh randoms are inert like their licensed predecessors) is honestly labeled and its failure mode is recorded in §8 — but the failure is load-bearing and *asymmetric*: a secretly-efficacious random that S_E correctly ranks high would LOWER ρ̄\* (the registered ranking calls it inert), producing a FALSE KILL of the E-step — the worst error for a falsification-first program. This is checkable label-free from already-computed quantities: for each fresh random, compare ŷ_j(random) against the cached unintervened decisions.

**Fix.** Pre-register an inertness gate: for each fresh random, the fraction of its 300 (item,view) pairs where ŷ differs from the cached unintervened decision must not exceed a pre-registered threshold X% (under true inertness the expectation is 0; justify the allowance for borderline argmax cases); trip → RUN-INVALID (the registered causal ranking is invalid for this candidate set). Require the §3.7(f) cached passes to record full decisions (not just margins) to enable this.

---

## Advisories (non-blocking)

**A1 — λ_c = 0.7 provenance.** §3.3's "the provisional default per EXP068's T3 tuning order" — EXP068 never executed, so there is no T3 tuning order; 0.7 is the grid midpoint chosen as provisional primary. Clarify the sentence. (Pre-registering 0.7 as primary with 0.5/0.9 as no-weight diagnostics is sound under Law #9.)

**A2 — α transparency.** §3.2 reads α "from LOG-128 at bundle build." Quote the expected numeric α in the draft alongside the executor-verified-from-record procedure. Minor.

---

## Disposition

Upon the drafter applying F1–F6 (and optionally A1–A2), the pre-registration should return for independent fix-verification against this review, then proceed to CEO launch decision. The hypothesis, decision table, normalization, and non-resurrection audit are sound — the fixes are all in the apparatus/statistical specification, none in the science.

**Review file:** `research/reviews/LAW14_REVIEW_EXP135_EVAL_PREREG_2026-09-30.md` (this file)
**Log:** LOG-4840 (appended below)
