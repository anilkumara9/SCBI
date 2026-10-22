# Law #14 Review — S4-5 (J4) Free-Energy Branch Selection Design (S45_DESIGN_2026-10-03.md)

**Reviewer:** Independent Scientific Mentor & Adversarial Reviewer (no hand in the design)
**Date:** 2026-10-03
**Document reviewed:** `~/workspace/SCBI/research/innovation/S45_DESIGN_2026-10-03.md` (exact file)
**Design-lane verdict under review:** CONDITIONAL RUN
**Review verdict:** **APPROVE-WITH-CONDITIONS** (conditions §9; execution additionally needs CEO approval per the design's own launch chain)

This review is of the design document only. It licenses nothing to run, mints no experiment number, and touches no signed artifact.

---

## 1. The free-energy estimator — SOUND AS SPECIFIED, WITH A LOAD-BEARING CHOICE AND A BACKSTOP

**Finding:** F_k = per-token mean NLL over rationale tokens only, prompt and answer token excluded, λ-free, is a well-formed, verifiable definition. Teacher-forced forward passes make it fully computable at $0 CPU; the per-token normalization genuinely removes an invented free parameter (the S4 sketch's `λ|r_k|` is dropped for an operational reason, not hidden elsewhere).

- **Prompt exclusion is required, not optional:** B0/B1/B2/B3 prompts differ in option order (B1 is the order-swap by construction); including prompt tokens would contaminate the cross-branch comparison. Correct call.
- **Answer-token exclusion is the design's one load-bearing judgment.** Its stated rationale — keeping F "a pure trajectory signal, outside the margin's decision-local territory" — is a coherent operationalization (the margin m⁰ is computed at the answer token; excluding it removes the shared token). But it is not obviously the *most informative* token: the rationale exists to lead to the answer, and the answer token's surprise under each branch's conditioning is likely the single most decision-relevant measurement. The design hedges correctly: full-trajectory F (answer token included) is a **pre-registered secondary diagnostic**, so the judgment is recoverable rather than buried. This is honest handling, not hand-waving — but it is the weakest joint in §2, and the pre-reg must report both numbers side by side (see condition C4).
- **The greedy-vs-sampled asymmetry is admitted, not laundered:** B2/B3 at τ=0.7 have higher F by construction (§4.3), so min-F selection may collapse toward the deterministic branches. The design does not patch this; selection frequency per branch is a reported diagnostic and the ΔM bars self-correct (collapse → ΔM_FE ≈ 0 → KILL). That is the falsification-first move, and it is the right one.
- One mechanical truth the design doesn't state but doesn't need: teacher-forced NLL on the model's *own* greedy output (B0/B1) is a self-consistency measure — informative only as cross-item and cross-branch *variation*. That is exactly how the selector uses it (argmin across branches), so the use is licensed; no condition needed.

## 2. The TESTA confrontation — HONEST ENGAGEMENT, NOT A JUST-SO STORY

**Finding:** §4.2 makes three concrete claims for why F might survive the margin's inversion (trajectory-integrated vs decision-local; density vs gap; counterfactual framing comparison vs single-pass sharpness), then **admits the exact failure mode** — "if fluency = bias, F inherits the inversion — and min-F selection would be *worse* than random. That is exactly what G3 tests." A just-so story would have stopped at the three differences; the honest-limit paragraph is what makes this engagement genuine. The license is labeled [CONJECTURE] and the breaking instrument is named. This passes.

- **Is G3 capable of catching the inheritance?** Yes. G3 tests the sign channel directly: Spearman(F̄, per-item accuracy) one-sided in the licensed direction plus a TESTA-style partition (100,000-permutation, mirroring TESTA's own procedure — seed 20261003 in TESTA). Significant inversion → KILL the selector family outright, *before any GPU spend*. That is the correct instrument for the admitted pathology.
- One soft spot: the calibration instrument is **mean**-F (deliberately, to stay "not selection-adjacent"), while the selector uses **min**-F. A signal can be mean-calibrated yet min-anti-calibrated. The design's secondary diagnostic (same tests on min_k F_k) observes this, but states no consequence. Stage-2's ΔM bars (ΔM_FE ≤ ΔM_random → KILL selector) are the binding backstop — see condition C5 to say so explicitly in the pre-reg.

## 3. The calibration gate and the Law #7 firewall — SOUND, CONSERVATIVE

**Finding:** the procedure is a faithful mirror of TESTA's R3/C2 with the sign flipped, and the gate logic is conservative in the right direction:

- C1 and C2 must **both** pass for G3 to license Stage 2; inversion on **either** kills the family. Requiring both is stricter than a Bonferroni-style correction for the passing branch; killing on either is the aggressive falsification posture. The one-sided tests in the licensed direction for passing, with wrong-direction-significant results killing, make the pair effectively two-sided with asymmetric consequences — no p-hacking surface beyond what the bars themselves license (and the bars are pre-registered).
- **Law #7 intact:** labels touch only per-item correctness computation for the instrument; "no branch score, no selection, no ranking, no gate threshold sees labels" holds — G1/G2 use no labels, and G3's thresholds (p<0.05, direction) are fixed, never tuned on labels. Using mean-F rather than min-F as the instrument is a genuine firewall refinement, not a loophole.
- Minor deferral (condition C1): the permutation seed is "pinned in pre-reg" rather than pinned here. Acceptable at the design stage — the design is the worth-it gate, not the protocol — but the pre-reg must pin it.

## 4. Branch generators — WELL-FORMED; S3-5 STALENESS CLAIM VERIFIED

**Finding:** the B0/B1/B2/B3 set is well-formed for the question asked. B1 (order-swap framing counterfactual) is the principled response to TESTA's position-bias mechanism — it turns the known bias into a branch the selector can exploit. B0 as the greedy anchor shares the rationale template with the elicitation, so ΔM_FE isolates *selection*, not elicitation (the design says this plainly in §2).

- **The S3-5 staleness claim checks out.** S3-5 (ACG) and S3-6 (AAR) were culled in the LOG-4353 Friday cull; the backlog's Graveyard section records the cull with the stated reason (three days as IDEA rows with no kill criterion). The design's documented deviation — re-specifying branching at the prompt/decoding level instead of reviving "branch at l* with the S3-5 μ-probe set" — is a genuine correction, and the design treats mid-layer branching as a *separate design, not a fallback*. No culled lane is revived.
- Deferral (condition C1): B2/B3's "two fixed seeds (design parameters)" are named as design parameters but **not pinned** in the design. For a Law #13 reproducibility claim these must be pinned in the pre-reg before Stage 1 runs.

## 5. The bars — JOINTLY NON-VACUOUS, HONEST

**Finding:** KILL (selector: ΔM_FE ≤ ΔM_random) / KILL (branching: ΔM_FE ≤ 0) / CONTINUE (ΔM_FE ≥ +8pp with paired LCI > 0.05 **and** ΔM_FE > ΔM_random at one-sided p < 0.05) / HELD (0 < ΔM_FE < +8pp, or LCI straddles 0.05) / PIVOT (calibration passes but Stage-2 kills the selector → diagnostic re-scope). I walked the full case table:

- Every region of (ΔM_FE, ΔM_random, LCI) space maps to exactly one verdict under the stated precedence (KILL > PIVOT > CONTINUE > HELD). ΔM_FE ≥ +8pp with LCI straddling 0.05 → HELD; ΔM_FE > ΔM_random with ΔM_FE < +8pp → HELD; ΔM_FE ≥ +8pp but ΔM_FE ≤ ΔM_random → KILL (precedence) — harsh but consistent: a gain that doesn't beat branching diversity is not the candidate's claim. No verdict gap found (compare S4-4's review, which found two).
- **The +8pp bar is honest.** On n=60 it is ≈5 net items with the entire paired Newcombe CI above +5pp — the same stringency the S4-4 review accepted as "a real capability bar, not a reach, not a gimme." It is the backlog row's Law #15 prediction, pre-registered here; pre-registration is what the law requires, not any particular number.
- The kill bars are the backlog row's own (verified in CANDIDATE_BACKLOG.md row 23: "ΔM_FE ≤ ΔM_random-branch → selector carries no signal → KILL; ΔM_FE ≤ 0 → KILL branching too"). The design does not soften its row.

## 6. Non-resurrection audit — CLEAN

**Finding:** every distinction is substantive, none is rhetorical:

- (i) Killed static-geometry lanes injected fixed *directions* and made causal claims about geometry. S4-5 injects no direction, steers nothing, makes no geometric claim — it generates trajectories and selects by a distributional statistic. Different object, different claim. Every kill stands.
- (ii) The REJECTED EXP135 sprint: S4-5's selection object is trajectories (not directions) and its signal is trajectory surprise density (not pair-flip statistics S(B)). The review's killer — S(bridge) ≡ 0 on the committed EXP135 records plus the Law #2 conflation of EXP077's GPU flips with EXP135's records — **cannot transfer**: S4-5 computes nothing on EXP135's records; its statistic is computed on trajectories it generates. The design explicitly adopts EXP135's §4.1 lesson (sign-less scores cannot rank efficacy) as a *gate requirement* (G3). This is the correct way to inherit a lesson without inheriting the corpse.
- (iii) EXP114 POE: order-swap here is a branch generator, selection is by free energy, never by vote — and the forced self-consistency comparator exists precisely to check S4-5 against the voting it disavows. POE's kill stands untouched.
- (iv) The stood-down G/E/S loop: S4-5 is not a loop component — no E-candidates, no E-step, no loop re-licensing. Standalone selection architecture. Clean.
- (v) EXP125: F is computed from *logits*, never from verbalized confidence. Clean.
- (vi) S4-1/S4-8: no competitor masking, no rank manipulation. Clean.

## 7. Stage-1 CPU pilot — COSTING CREDIBLE, GATES GENUINELY BINDING

**Finding:** ~240 generations (≤48 rationale tokens) + ~300 forward passes at ~1h CPU is credible arithmetic against the H-wave precedent (108 generations in 20.9 min CPU — that is the EXP109 report at LOG-4552; the design cites LOG-4553, which is a misattribution of the LOG number — minor, see C2). The forward-pass cost claim is supported by the EXP139 Stage-1 CPU precedent (60/60 passes). The estimate is right to a factor of ~2, which is the correct precision for a gate design.

- **G1 (diversity, ≥2 distinct answers on ≥25% of items)** and **G2 (median F-spread ≥ 0.05 nats/token)** are pinned as design parameters in the design itself — good, no deferral. G2 is a soft gate (the τ=0.7 stochastic branches will almost surely clear it), but that is its job: it guards against selector vacuity, not rigor.
- **G3 is the load-bearing gate**, and it is genuinely binding: null → no GPU; significant inversion → KILL the selector family. There is no path from a failed G3 to Stage 2 on this design's authority. The bench pin (`eb304fa6…45589df`) and backbone pin (`ec276abe…38e0ed`) match the TESTA file and the EXP139 Stage-1 record — verified.

## 8. Verdict on CONDITIONAL RUN — CONFIRMED

**Finding:** the design-lane's CONDITIONAL RUN is the right verdict; DO NOT RUN would require a structural flaw, and none of the seven points above surfaces one. The worth-it gate is priced correctly: the honest prior is *against* the signal (§9.1 says so), the entire calibration burden TESTA imposed is discharged at $0 *before any GPU contact*, and the most likely outcome (a clean kill of the free-energy-selector family, either at G3 or at the Stage-2 ΔM bars) is itself the summit-tier-relevant deliverable — it closes the program's only remaining candidate for a training-free, target-free evaluator.

---

## 9. Verdict: APPROVE-WITH-CONDITIONS

Stage-1 CPU pilot may run after these conditions are closed in the pre-registration draft, plus CEO approval per the design's launch chain:

- **C1 — Pin the seeds.** The pre-reg must pin: (a) the two fixed sampling seeds for B2/B3, (b) the permutation-test seed for C2 (currently "pinned in pre-reg" — pin it), (c) the random-branch comparator seed (`20261003` is stated; keep it). Law #13 requires no seed to be chosen at runtime.
- **C2 — Citation correction.** The "108 generations in 20.9 min" H-wave precedent is the EXP109 report at **LOG-4552**, not LOG-4553 (which is the H2 QBR pre-reg draft). Cite it correctly. Minor, but Law #2 applies to LOG numbers too.
- **C3 — Prior-art verification.** Verify the remaining cited items at pre-reg stage alongside the full-text follow-ups the design already flags (§8). I verified FREIA (arXiv:2605.04065) independently: it is real, and the design's characterization (free-energy principle as an RL *reward* under policy optimization) is accurate — the stated distinction (FREIA trains; S4-5 is inference-only, Δθ=0) is correct. **UNCHECKED by me:** Minimum Bayes Risk decoding (Jinnai et al., arXiv:2311.05263), Freitag et al. (arXiv:2111.09388), CycleVLA (arXiv:2601.02295). Mark UNVERIFIED until the pre-reg lane checks them.
- **C4 — Degenerate-branch handling + dual reporting.** The pre-reg must (a) pin R_max = 48 tokens for Stage 1 and state the handling for degenerate branches (empty rationale → F undefined; identical branches → F-spread 0) so the executing lane improvises nothing; (b) report the primary F (answer token excluded) and the secondary full-trajectory F side by side, since answer-token exclusion is the design's weakest judgment.
- **C5 — State the min-F consequence.** The pre-reg must state explicitly: if the secondary min_k-F calibration diagnostic inverts while mean-F passes G3, the binding consequence is Stage-2's KILL-selector bar (ΔM_FE ≤ ΔM_random) — mean-calibration is not a selection license. This closes the instrument/selector gap noted in §2 of this review.

**What this review does NOT do:** it does not license execution (CEO approval still required), mint an experiment number, or approve Stage 2 (strictly gated on G1–G3 all passing in the licensed direction).

---

## 10. Summary

The S4-5 design is honest, falsification-first, and worth executing conditionally. Its estimator is well-formed and verifiable with the answer-token exclusion hedged by a pre-registered secondary diagnostic; its TESTA confrontation admits the exact failure mode and gates on the instrument that detects it; the calibration procedure mirrors TESTA with a Law #7 firewall that is genuinely intact; the branch set is well-formed and B1 turns the known position bias into an exploitable branch; the bars are jointly non-vacuous and the +8pp CONTINUE bar is as stringent as the S4-4 precedent; the non-resurrection audit is substantive on all six lines (the EXP135 REJECT's killer cannot transfer, and the design correctly inherits EXP135's sign-less-score lesson as a gate); the Stage-1 costing is credible and G1–G3 are genuinely binding. Five conditions (C1–C5) must be closed in the pre-registration draft before Stage 1 runs; none is a reason to reject. Two minor corrections noted: the H-wave precedent is LOG-4552 not LOG-4553, and three of four prior-art citations remain UNCHECKED pending pre-reg verification (FREIA verified real and accurately characterized).
