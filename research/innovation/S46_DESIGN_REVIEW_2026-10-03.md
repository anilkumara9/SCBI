# Law #14 Review — S4-6 (J2) Metacognitive Self-Modeling Design (S46_DESIGN_2026-10-03.md)

**Reviewer:** Independent Scientific Mentor & Adversarial Reviewer (no hand in the design)
**Date:** 2026-10-03
**Document reviewed:** `~/workspace/SCBI/research/innovation/S46_DESIGN_2026-10-03.md` (exact file; 203 lines)
**Design-lane verdict under review:** CONDITIONAL RUN
**Review verdict:** **APPROVE-WITH-CONDITIONS** (conditions §9; execution additionally needs CEO approval per the design's own launch chain)

This review is of the design document only. It licenses nothing to run, mints no experiment number, and touches no signed artifact.

---

## 0. Reading note

I read the full design, plus: `TESTA_CALIBRATION_2026-10-03.md` (full), `EXP140_stage1/RUN_REPORT.md` (full), LOG-4680 (EXP125 kill record), backlog row 24, and independently verified the three primary prior-art citations (Kadavath via arXiv API; Self-Refine via arXiv API; Huang et al. via six independent secondary sources — arXiv API was rate-limited at review time). Kamoi and Xu remain REPORTED-via-secondary, as the design itself labels them.

---

## 1. The load-bearing distinction — STATED INACCURATELY, SUFFICIENT ON CORRECTED GROUNDS (CONDITION C1)

**Finding:** The design's stated distinction between â_self and EXP125's killed object is factually wrong, but the distinction on correct grounds is sufficient. This is a condition, not a REJECT — the design invites this ruling explicitly (§6.v, §9.3), and I rule: **the stated distinction is insufficient; the corrected distinction is sufficient.**

**What the design claims (§1, §6.v):** EXP125 killed "*verbalized* self-report: the model *saying* how confident it is (28/60 on fresh bench 4)"; â_self is a "*distributional* readout" and therefore a different object.

**What LOG-4680 actually records:** EXP125 (H22/HONESTY-GEN4) killed "the frozen backbone's **first-token logit-readout self-report**" — fidelity 28/60 between the logit-readout and the registered cosine-argmax decision statistic. EXP125 was *also* a distributional/logit-level readout, not generated words. The design's "verbalized vs distributional" framing mischaracterizes the killed object. A non-resurrection audit that rests on a false premise about the killed lane cannot stand as written.

**Why the conclusion nevertheless holds on correct grounds:**
1. **Different property.** EXP125 tested *honesty*-self-report fidelity (was the process honest?); S4-6 tests *correctness*-self-prediction informativeness (is the answer right?). These are different constructs — a model could lack honesty-fidelity while carrying correctness information, or vice versa.
2. **Different ground truth.** EXP125 validated against an internal decision statistic (cosine-argmax); S4-6 validates against external bench labels. The validation objects differ.
3. **EXP125's kill was bench-specific.** LOG-4680 explicitly reclassifies it per Law #8/Law #11 ("EXP112's bench-1 HELD (41/60) stands... reclassified bench-specific"). A bench-specific honesty-fidelity kill cannot logically extend to a correctness-informativeness question on this bench.
4. **Independent empirical anchor.** Kadavath et al. (2022, verified real — see §8) provides an existence proof that P(True)-style self-evaluation carries information at scale, an anchor EXP125 never had.

**Ruling:** The design must correct §1 and §6(v) to characterize EXP125 accurately (first-token logit-readout honesty self-report, fidelity 28/60 vs a decision statistic, bench-specific kill) and rest the non-resurrection on grounds 1–4 above. The design's honesty in naming this a REJECT ground is to its credit; the ground is not triggered because the corrected distinction is substantive.

---

## 2. The TESTA confrontation — HONEST ENGAGEMENT

**Finding:** §4.2 makes three concrete claims for why â_self might survive the margin's inversion (separate forward pass/separate question; judgment vs sharpness; counterfactual leverage via order-swap revision), then admits the exact failure mode — "the model may simply re-derive its biased answer when judging, in which case â_self is the bias wearing a second hat. That is exactly what G2/G3 test." Like the S4-5 design's confrontation, the honest-limit paragraph is what makes this genuine rather than just-so. This passes.

- **Is the True/False constant-order claim sound?** TESTA's mechanism was a first-listed *answer-option* bias. In the self-eval, the choice is True (A) vs False (B) in constant order — the bias, if it re-derives as a general first-option lean, inflates â_self uniformly rather than differentially. A uniform inflation is exactly what G1 (variance gate: std > 0.01, non-constant) and G2 (I-screen: information about correctness) are built to catch. The design does not claim the self-eval is bias-free; it claims the bias would have to re-derive in a new form, and names the instruments that detect it. Honest.
- **Are G2/G3 capable of catching bias re-derivation?** Yes. If â_self re-derives the biased policy, it carries no correctness information → G2 null → KILL before revision. If it inherits TESTA's inversion → G3 inverted → KILL family. The instruments match the admitted pathology.

---

## 3. The I-screen — SOUND

**Finding:** Mutual information via 4-bin equal-frequency discretization of â_self, Miller-Madow bias correction, permutation test (100,000 permutations) for significance, null (p ≥ 0.05) → KILL before revision. This is a sound instrument:

- The permutation test calibrates significance correctly regardless of the estimator's small-sample bias — with n=60 and 4 bins (~15 items/bin), the Miller-Madow correction plus permutation testing is the right pairing.
- The "≈ 0" bar (p ≥ 0.05) is the standard null-hypothesis-testing bar, pre-registered. Power at n=60 is limited, but the design's honest prior is LOW and the I-screen is deliberately built to kill cheaply — the stringency is a design choice, stated, not a defect.
- **Ordering (kill before revision) is right.** There is no point testing discrepancy-driven revision if the self-model carries no correctness information. The I-screen is the backlog's load-bearing element (LOG-288), and the design honors it.

---

## 4. The revision protocol — WELL-CONTROLLED, TWO UNDERSPECIFICATIONS (CONDITION C2)

**Finding:** The discrepancy trigger (â_self_i < τ_rev = 0.5, pre-registered design parameter) with the order-swap revision framing is well-specified, and the control kit is the design's strongest methodological element: revise-all isolates the trigger from reframing; random-trigger (same-size subset, seed pinned) isolates the trigger's information from resampling. This directly incorporates EXP140's resampling lesson (random-branch 76.7% beat min-F selection 70.0%) and Huang et al.'s prompt-artifact critique. The controls are fair.

**Two underspecifications the pre-reg must close:**
- **(a) Revision decoding not pinned.** §2 says "regenerate the answer under the order-swapped framing" but does not state greedy vs sampled decoding. The baseline ŷ_i is greedy (B0); for the revision comparison to be clean, the revision decode must be pinned (greedy, matching baseline) in the pre-reg. An executing lane must not improvise this.
- **(b) Trigger-rate floor missing.** If â_self < 0.5 fires on very few items, ΔM_trig is underpowered or undefined. The design mentions a "trigger-rate diagnostic" (§8) but a diagnostic is not a gate. The pre-reg must state the minimum triggered-item count for the revision test to be valid and the VOID rule if it is not met.

Neither is a structural flaw; both are pre-reg-stage closures.

---

## 5. The bars — JOINTLY NON-VACUOUS; PIVOT IS REACHABLE

**Finding:** I walked the case table against the stated precedence KILL (any) > PIVOT > CONTINUE > HELD:

- KILL (self-model): I-screen null. KILL (calibration): G3 inverted. KILL (revision): ΔM_trig ≤ ΔM_rand.
- **PIVOT is reachable** (contrast the S4-5 review, which found PIVOT unreachable there): PIVOT requires I-screen passes AND ΔM_trig ≤ 0. KILL (revision) requires ΔM_trig ≤ ΔM_rand. When ΔM_rand < ΔM_trig ≤ 0 (e.g., random revision hurts more than triggered revision, but triggered revision still doesn't help), PIVOT fires without KILL (revision) tripping first. Non-empty region — the branch is live. The design learned from the S4-5 review's F1.
- CONTINUE (+8pp with LCI > 0.05 AND > ΔM_rand at p < 0.05) matches the S4-4/S4-5 precedent bar — consistent, not inflated.
- HELD covers the intermediate regions (0 < ΔM_trig < +8pp; LCI straddles 0.05; numerical superiority with p ≥ 0.05).
- One implicit condition worth stating in pre-reg: PIVOT (and any Stage-2 verdict) requires Stage 2 to have run, which requires G1–G3 all passing — G2-pass/G3-null stands the family down per the EXP140 precedent (§3 gate logic). The design's §3 states this; the pre-reg should keep the gate logic and the verdict table explicitly linked.

---

## 6. Non-resurrection audit — CLEAN EXCEPT (v) AS CORRECTED IN §1

**Finding:**
- (i) Killed static-geometry: clean — no direction injected, no steering, no geometric claim. ✓
- (ii) REJECTED EXP135 sprint: clean — different signal (self-prediction vs pair-flip statistics), nothing computed on EXP135's records; the Law #2 exemption (no record-grounded predictions → nothing to accompany) is stated explicitly for checking. ✓
- (iii) EXP114 POE: clean — order-swap is a revision framing, not a vote; selection of what to revise is by trigger, never majority. ✓
- (iv) Stood-down G/E/S loop: clean — not a loop component. ✓
- (v) EXP125: **incorrect as stated, correct on the grounds in §1** — condition C1. ✓ (after correction)
- (vi) S4-5/EXP140: clean — different signal family (metacognitive judgment about a fixed answer vs trajectory-integrated surprise density); EXP140's G3-null does not transfer because the informativeness question is re-tested from scratch. ✓
- (vii) S4-1/S4-8: clean. ✓

---

## 7. Stage-1 costing and gate binding — CREDIBLE

**Finding:** 120 passes (~30 min CPU) is credible against the EXP139 (60/60) and EXP140 (240+240 in ~1h) precedents. G1 (variance: std > 0.01, non-constant — catches the Xu et al. self-bias confound where the model rates everything highly), G2 (I-screen — the backlog's load-bearing bar), G3 (TESTA-mirrored calibration with inversion → KILL) are all genuinely binding: G2-null kills before revision spend; G3-inverted kills the family; G3-null stands it down. No path from a failed gate to Stage 2 exists on this design's authority.

The EXP140 B0-record reuse option (§3) is legitimate — the records are committed, deterministic, byte-identical on re-run per EXP140's gate (c) — and the design leaves the reuse-vs-regenerate choice to the pre-reg with the budget held constant either way. Acceptable at the design stage.

---

## 8. Prior art — VERIFIED (TWO AT API LEVEL, ONE VIA SECONDARIES; TWO REMAIN REPORTED)

**Finding:**
- **Kadavath et al. 2022 (arXiv:2207.05221): VERIFIED real** via arXiv API — "Language Models (Mostly) Know What They Know" (2022-07-11). The design's characterization is accurate: P(True) self-evaluation of own samples, a partially distinct skill from answering (one-shot "is this true?" performs worse), calibration format-dependent and scale-sensitive, RLHF policies miscalibrated, P(IK) head required training. The stated distinctions from S4-6 (scale 52B → 410M; trained head → training-free; no discrepancy-driven revision) are correct.
- **Self-Refine (arXiv:2303.17651): VERIFIED real** via arXiv API — "Self-Refine: Iterative Refinement with Self-Feedback", Madaan et al. (2023-03-30). Characterization accurate: generate → self-feedback → refine loop, one frozen model, ~20% average improvement across 7 tasks. The distinctions (free-form critique vs discrepancy-triggered revision with matched resampling controls; generative tasks vs decision rescue with binding bars) are correct.
- **Huang et al. (arXiv:2310.01798): VERIFIED real** via six independent secondary sources (arXiv API returned "Rate exceeded" at review time) — "Large Language Models Cannot Self-Correct Reasoning Yet", ICLR 2024. Characterization accurate: intrinsic self-correction fails and often degrades reasoning without external feedback; part of Self-Refine's gains traced to prompt-design artifacts. The design's response (discrepancy trigger gated on a prior I-screen, conceding Huang's point by construction) is the right posture.
- **Kamoi et al. (TACL 2024): REPORTED via secondary only** — not independently verified by me; the design already flags full-text verification as pre-reg follow-up. Consistent with the design's labeling.
- **Xu et al. (arXiv:2402.11436): REPORTED via secondary only** — not independently verified by me; flagged as follow-up, consistent with the design's labeling.
- **Novelty read N1 (known combination)** is honest: P(True)-style self-evaluation and self-refinement loops both have prior art; the differentiators (discrepancy-triggered rather than blanket revision, falsification-first I-screen killing before revision, pre-registered calibration gate on this bench/backbone) are genuine but compositional. The design claims none of the prior art's territory.

---

## 9. Verdict: APPROVE-WITH-CONDITIONS

Stage-1 CPU pilot may run after these conditions are closed in the pre-registration draft, plus CEO approval per the design's launch chain:

- **C1 — Correct the EXP125 characterization.** §1 and §6(v): EXP125 killed a first-token logit-readout honesty self-report (fidelity 28/60 vs the registered cosine-argmax decision statistic, LOG-4680), not "verbalized" self-report. The "verbalized vs distributional" framing must not stand. Rest the non-resurrection on the correct grounds: (a) different property (honesty-fidelity vs correctness-informativeness), (b) different ground truth (decision statistic vs bench labels), (c) EXP125's kill was bench-specific per LOG-4680/Law #8, (d) Kadavath et al. provides an independent empirical anchor EXP125 never had. Per §1 of this review, the corrected distinction is sufficient — this is not a REJECT ground once corrected.
- **C2 — Pin the revision mechanics.** The pre-reg must (a) pin the revision decoding (greedy, matching the baseline ŷ_i) so the executing lane improvises nothing, and (b) state the minimum triggered-item count for the revision test to be valid, with the VOID rule if the trigger fires too rarely.
- **C3 — Prior-art follow-up.** Full-text verification of Kamoi (TACL 2024) and Xu (ACL 2024, arXiv:2402.11436) at pre-reg stage, as the design already flags. Nothing is marked verified that is not.

**What this review does NOT do:** it does not license execution (CEO approval still required), mint an experiment number, or approve Stage 2 (strictly gated on G1–G3 all passing in the licensed direction, plus signed pre-registration, CEO GPU clearance, and founder Kaggle slot).

---

## 10. Summary

The S4-6 design is honest, falsification-first, and worth executing conditionally. Its one real defect is the mischaracterization of EXP125's killed object (§1/C1): EXP125 killed a logit-level honesty self-report, not "verbalized" confidence, so the design's stated verbalized-vs-distributional distinction collapses — but the distinction on correct grounds (honesty-fidelity vs correctness-informativeness, different ground truths, bench-specific kill, Kadavath anchor) is substantive, and the design is corrected rather than rejected. The TESTA confrontation is honest with named breaking instruments; the I-screen (4-bin MI + Miller-Madow + permutation test) is sound and correctly ordered before revision; the revision control kit (revise-all + random-trigger) is the design's strongest element, incorporating EXP140's resampling lesson; PIVOT is reachable (the S4-5 F1 lesson was learned); the +8pp bar matches precedent; Stage-1 costing is credible and all three gates bind. Three conditions (C1–C3) must be closed in the pre-registration draft before Stage 1 runs; none is a reason to reject. Prior art: Kadavath and Self-Refine verified real via arXiv API with accurate characterization; Huang et al. verified real via six independent secondaries (arXiv API rate-limited); Kamoi and Xu remain REPORTED-via-secondary as the design labels them.
