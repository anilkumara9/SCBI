# EXP135 Post-E-Step Selection-Architecture Sprint — Worth-It Gate (Design)

**Status:** DRAFT design. Licenses nothing. No experiment number minted, no protocol written, no code, no model runs, no GPU contact, no signed artifact touched, no commits. $0 compute.
**Design lane:** CEO pre-assigned (EXP135 ruling, 2026-10-03). **Governing laws:** Law #2 (no invented numbers — every constant below is pinned or computed-from-record), Law #4 (no post-hoc shifts — bars are binding), Law #6 (Δθ=0), Law #7 (labels never touch any candidate score), Law #9 (metrics before inspection), Law #11 (observation vs interpretation), Law #13 (deterministic reproducibility), Law #15 (this document IS the worth-it gate).
**Launch chain:** independent Law #14 review of this exact file → CEO approval → Phase-1 execution lane (analysis only) → Phase-2 decision → (if CONTINUE) new experiment number for integration.
**Epistemological labels** per `AGENTS.md` §5 used throughout.

---

## 0. CEO ruling and scope

**[FACT]** EXP135 (binding KILL, LOG-4846, 2026-09-30) retired the G/E/S loop's E-step as designed: the signed label-free evaluator S_E cannot rank the known-causal bridge above 8 matched randoms (ρ̄\* = −0.0041667, bridge mean rank 5.017/9 ≈ uniform, permutation p = 0.530275). The Friday cull (LOG-4879) escalated the resulting architecture question to the CEO with three options; the CEO ruled **option (a): a post-E-step selection-architecture innovation sprint, worth-it-gated**. This document is the gate. If it fails — by its own bars, or by honest verdict of this design lane — the G/E/S loop family stands down per option (b)/(c) and the EXP135 death-debt is paid by redirect, not by sprint.

**Scope:** this sprint designs and tests a *selection statistic* — a label-free function that ranks candidate intervention directions by causal efficacy. It does NOT generate candidates, does NOT inject novel directions, does NOT re-test any killed causal hypothesis. Phase 1 is pure analysis of committed artifacts (zero new forwards). Phase 2 (if licensed) is a small CPU forward run with pre-registered adversarial anchors. Integration of a surviving statistic into the loop as an E-step replacement is a *follow-on* requiring a new experiment number — explicitly out of scope here.

---

## 1. Exact question

**[HYPOTHESIS]** Does the calibration-signed flip statistic S(B) — which scores each candidate direction by (intervention-flipped pairs at below-median baseline margin) minus (intervention-flipped pairs at above-median baseline margin), using only the frozen model's own confidence as the label-free correctness proxy — separate the known-causal bridge from matched inert randoms (Phase 1, committed records) and assign opposite signs to the bridge and its adversarial foil (Phase 2, pre-registered anchors), thereby supplying the label-free selection signal the G/E/S loop's E-step failed to deliver?

---

## 2. Decision changed

**What changes:** the architectural status of the G/E/S loop family — currently retired-as-designed (LOG-4879). A surviving selection statistic re-opens the loop architecture with a licensed E-step replacement; a failed one closes the selection question and redirects the program.

| Branch | Trip condition | Reading |
|---|---|---|
| CONTINUE | Phase-1 Test A **and** Test B pass **and** Phase-2 bars met (S(bridge) > 0, S(foil-bridge) < 0, separation from randoms — §8) | A label-free selection statistic exists. Licenses a follow-on experiment (new number) integrating S as the loop's E-step replacement and testing end-to-end selection on G-step candidates. |
| KILL | Test A fails (calibration license void) **or** Test B fails (statistic dead on arrival) **or** Phase-2 foil signing fails (S(foil) ≥ 0) | No label-free selection statistic in this family. The loop family stays retired; EXP135 debt paid via option (b) redirect (J-tier S4-4–S4-7, HELD follow-ups). |
| PIVOT | Phase-1 passes but Phase-2 shows S detects *movement* not *efficacy* (e.g., foil also scores positive) | Re-scope S from *ranker* to *filter*: use it to drop inert candidates (a real, if smaller, win — the loop's candidate budget is finite), paired with a different efficacy signal; or pivot the selection question to S4-5's free-energy line (§5.iv). |
| HELD | Phase-1 passes but Phase-2 proves infeasible or uninterpretable | Conjecture stays open, licenses nothing, kills nothing. |

Precedence: KILL > PIVOT > CONTINUE > HELD. (KILL conditions are checked first; a failed license voids everything downstream.)

---

## 3. Cheapest $0 test

**Phase 1 — zero new forwards.** Everything computes from committed artifacts:
- `experiments/runs/EXP135_eval/out/exp135_records.json` — per (candidate, item, view) ŷ+margins for C1–C9 (60 items × 5 views = 300 pairs each) **plus** `cache_unintervened` (unintervened ŷ⁰, m⁰ per pair). [FACT — structure verified 2026-10-03.]
- `experiments/runs/EXP135_eval/out/exp135_per_item.csv` — per-item bridge ranks (cross-check).
- The 6 McNemar-b item IDs (licensed: baseline-wrong/bridge-right, EXP077 GPU record LOG-128; recoverable from `experiments/runs/EXP077_cone_vs_line/exp077_instance_records.json` by selecting baseline-wrong/bridge-right items, cross-checked against the LOG-128 McNemar table).

**Test A — the calibration license (the real gate).** [ASSUMPTION under test] The frozen model's margin is a calibrated confidence proxy: P(baseline correct | m⁰) strictly increasing in m⁰. **Procedure:** per-item mean unintervened margin m̄⁰ (60 values, from the committed cache); one-sided permutation test of m̄⁰(6 licensed wrong-baseline items) < m̄⁰(other 54 items). **Bar:** p < 0.05 in the predicted direction. **Cost:** ~0 CPU (permutations on 60 numbers). **Reading:** this is a *labeled instrument check* — the 6 items are licensed facts from the EXP077 GPU record (labels were used in that licensed context, not here); no candidate score in this sprint ever sees labels (Law #7 preserved for all selection). Flagged for Law #14 review of the Law #7 boundary.
- **Fallback:** if the 6 item IDs prove unrecoverable, Test A runs as a labeled instrument check on the unintervened cache using bench labels *only* to validate the margin–correctness relationship — explicitly flagged, never touching selection. The executing lane must document which source was used.

**Test B — statistic sanity (necessary, not sufficient).** Compute S(B) (§4) for all 9 EXP135 candidates from the committed records. **Bars (binding):** S(bridge) > max S(randoms) **and** S(bridge) ≥ +8 (effect-size floor against degenerate tiny separations). **Cost:** ~0 CPU. **Reading:** KILL iff failed — if the one known-efficacious direction doesn't separate from randoms on the proposed statistic, the statistic is dead on arrival. **Honest limitation (stated now, not discovered later):** Test B is confounded by flip count (the bridge flips more pairs than randoms per guard (h): random flips 2,1,1,2,0,1,1,1) — it *cannot* distinguish "calibration-signed efficacy" from "raw flip count." Phase 1 can KILL but cannot CONFIRM. Confirmation requires Phase 2's adversarial anchor.

**Pre-registered contingency:** EXP135 guard (e) found 29/60 items with degenerate *scores* (48.3% zero-variance). If >40% of pairs tie exactly at the median margin m̃, Test B uses a rank-based median split (split at median *rank*, ties broken by the pre-registered EXP135 tie-break seed stream) — specified here, not improvised later.

---

## 4. Mathematical license

### 4.1 Why the E-step failed — structurally, not by tuning

**[INTERPRETATION]** The signed evaluator S_E(B;x) = λ_c·C_cons(B;x) + λ_m·M̃(B;x) (LOOP_SPEC_DRAFT §2.2) measures *stability* (cross-view decision agreement) and *decisiveness* (normalized margin) of the intervention's outputs. Both are functions of the output distribution **invariant under swapping "correct" and "incorrect"**: a direction that consistently flips decisions to the *wrong* answer scores identically to one that flips to the *right* answer (same C_cons, same M̃). But causal efficacy e(B) = P(ŷ(B)=y\*) − P(ŷ(∅)=y\*) is precisely the *sign* of the effect relative to ground truth. **S_E has no channel carrying that sign.** No λ reweighting can create information absent from its inputs. [FACT] EXP135's secondaries confirm it isn't tuning: S_E(0.5) ρ̄\*=0.1083, S_E(0.9) ρ̄\*=0.1542 — all far below any bar, all measuring the same sign-less quantities.

### 4.2 The only available channel

**[THEOREM — informal, the license]** Per (item, view) pair, the label-free observables are (ŷ(∅), m⁰, ŷ(B), m¹). Efficacy is defined via y\*. The *only* joint distribution linking observables to y\* without labels is the baseline model's own P(y\* | ŷ(∅), m⁰) — its accuracy (56.67% > chance [FACT, EXP077]) and its calibration. **Any label-free efficacy ranker must use the baseline as its reference; there is no other source of correctness information in the system.** This is not a clever choice — it is the uniquely available channel. The sprint's statistic is therefore not "another hand-tuned score" but the *canonical* label-free construction: sign each observed flip by the baseline's confidence at the flipped pair.

### 4.3 The statistic

For candidate B, let m̃ = median m⁰ over all 300 pairs (pre-registered split point; ≤ goes low):

$$S(B) = \#\{\text{pairs}: \hat{y}_j(B) \neq \hat{y}_j(\emptyset)\ \land\ m^0_j \leq \tilde{m}\} \;-\; \#\{\text{pairs}: \hat{y}_j(B) \neq \hat{y}_j(\emptyset)\ \land\ m^0_j > \tilde{m}\}.$$

**License derivation.** For a flipped pair, contribution +1 iff m⁰ ≤ m̃. E[contribution] = 2·P(m⁰≤m̃ | flip) − 1. Decompose by flip quality: P(m⁰≤m̃|flip) = q_g·π + q_b·(1−π), where π = P(good flip | flip), q_g = P(m⁰≤m̃ | good flip), q_b = P(m⁰≤m̃ | bad flip). Under the calibration assumption, good flips (baseline was wrong) sit at lower m⁰ than bad flips (baseline was right) ⟹ **q_g > q_b** ⟹ E[S(B)] is strictly increasing in π, and π increases in net efficacy. The *sign* of S(B) (relative to the flip-count baseline) tracks net efficacy: efficacious → positive, adversarial → negative, inert → ~0.

**The threshold-crossing confound (named, not hidden).** [INTERPRETATION] Flips mechanically occur where the intervention's logit shift exceeds m⁰ — i.e., disproportionately at low m⁰ *for every flipping direction*. This biases S(B) positive in proportion to flip count for all candidates. The *discriminative* content is therefore not "flips are at low margin" (tautological) but the *gap* q_g − q_b — which Phase 1 cannot measure (one positive anchor) and Phase 2 measures directly via the foil-bridge (§8). If q_g ≈ q_b, the sprint dies in Phase 2 by its own bar.

### 4.4 Quantitative predictions and breaking points

**Phase 1 predictions:**
- Test A: mean m̄⁰(6 licensed wrong items) < mean m̄⁰(other 54), one-sided permutation p < 0.05.
- Test B: S(bridge) ≥ +8 with S(bridge) > max S(randoms); randoms |S| ≤ 3 (0–2 flips each per guard (h), signed by margin).

**Breaking points (binding):**
- Test A p ≥ 0.05 → **KILL**: the calibration license is void on this bench — no margin-based label-free selector can work here. (Note: this would also weaken S4-5's premise — see §5.iv.)
- Test B S(bridge) ≤ max S(randoms), or S(bridge) < +8 → **KILL**: statistic dead on arrival.
- Phase 2 S(foil-bridge) ≥ 0 → **KILL**: the signing is broken — the statistic cannot distinguish efficacious from adversarial directions.
- Phase 2 S(bridge) ≤ 0 → **KILL**: license void.

---

## 5. Non-resurrection audit

**(i) vs the killed static-geometry lanes (EXP077, EXP092/093/094, S5-2/S5-3, EXP095/096).** Those were *mechanism* experiments: "does static direction X cause decision flips when injected?" This sprint is *selection*: "can a label-free statistic rank directions of *known* (in)efficacy?" It uses the killed lanes' *results as test data* (bridge = positive anchor per LOG-128; randoms/cones = inert anchors) without re-testing their hypotheses. No static-geometry causal claim is revived; every kill stands. The sprint proposes **zero** new injection directions and **zero** new causal claims.

**(ii) vs the dead E-step ranker (EXP135).** EXP135 killed the *specific* statistic S_E (stability/decisiveness scores). This sprint tests a *different statistic family* under a *different license* (calibration-signed flips vs output-stability) — and §4.1 *explains* S_E's failure structurally (correct/incorrect-swap invariance) rather than re-tuning it. It does not re-run S_E, tune λ, reuse C_cons/M̃ as ranking signals, or dispute the KILL. The E-step *as designed* stays dead; what is proposed is a *replacement*, not a resurrection.

**(iii) vs the stood-down S6 L11-rescue.** S6 was a *mechanism rescue* (static geometry at layer 11). This sprint touches no layer-11 claim, no static-geometry causal claim, and operates on layer-20 records. Different object (selection vs mechanism), different question, different evidence.

**(iv) vs S4-5 free-energy branch selection (QUEUED, J-tier).** S4-5 selects among *output trajectories* (branches) via free energy; this sprint selects among *intervention directions* via calibration-signed flips. Complementary, not duplicative — they attack different selection objects. Interaction noted honestly: both rely on the premise that the model's internal signals (confidence/free energy) carry correctness information. If this sprint's Test A (calibration) fails, S4-5's premise is weakened too — Test A is informative for S4-5 regardless of outcome. The lanes should coordinate, not compete; neither's result is assumed by the other.

---

## 6. Spotlight relation

**Borrowed (framing, not mechanism):**
1. *Selection as first-class architecture.* Spotlight's learned addressing **is** a selection architecture (which memory cells to touch per token); the E-step was a failed selection architecture (which candidates to keep). The sprint takes seriously that selection deserves its own architectural design with its own license — not a hand-tuned score bolted onto a loop.
2. *The adaptivity moral.* Hand-designed static scores (S_E) underperform mechanisms that condition on the system's own state. S(B) conditions on the model's own confidence landscape — the closest label-free analog of "addressing by learned relevance": relevance here is the model's uncertainty, and it is *measured*, not learned.
3. *Separation of concerns.* Spotlight separates memory (stored) from the intelligence module (computes). Analogously, this sprint separates the *selection signal* (baseline confidence — a property of the model+bench) from the *candidate geometry* (directions) — the E-step's error was scoring geometry-adjacent outputs instead of the selection-relevant signal.

**Deliberately NOT borrowed:**
1. *Writable memory.* Irrelevant — we rank fixed candidates; there is no memory to write and no growth to manage.
2. *Learned addressing trained on next-token loss.* We have **no training signal for efficacy** — that absence *is* the problem. S(B) is a *derived* statistic with an explicit falsifiable license, not a learned one. (If Phase 2 succeeds, a *learned* selector trained with S(B) as a reward signal is a legitimate Phase-3 direction — noted, not pursued.)
3. *All vendor performance claims* (134K–144K tok/s, Turing-completeness, MNIST agreement, "infinite memory at constant cost): unverified vendor claims, irrelevant to our question. Nothing in this design depends on any of them.
4. *The "intelligence module" concept.* Our computation is the frozen Pythia backbone (Δθ=0); we are not building new modules.

---

## 7. Summit filter

**Plain statement:** this sprint does not directly advance machine cognition. It repairs *infrastructure*. The G/E/S loop is the program's architectural bet for inference-time capability growth — a generate-evaluate-select cycle is a primitive form of a model improving its own processing — and it is currently dead for lack of selection. A working label-free selector is **necessary but not sufficient** for that bet: without it the loop cannot search autonomously; with it, the loop can select among interventions without human labels, which is a precondition for any recursive self-improvement story at Δθ=0.

**If the sprint KILLs**, that is summit-informative too: it bounds what label-free selection can achieve with the model's own signals, redirecting the program toward (a) the J-tier summit candidates (S4-4–S4-7), or (b) architectures with *explicit* selection machinery (Spotlight-like learned addressing over writable memory) rather than hand-designed scores over frozen geometry. **Either verdict moves the program.** A null here is not a shrug — it is priced information about the selection bottleneck.

---

## 8. Phase-2 sketch (design-level only — no protocol, no experiment number)

*If Phase 1 passes both tests*, Phase 2 commissions a small CPU forward run (~3,000 forwards ≈ 0.8× EXP135's 3,751; unintervened cache reused from committed records — $0) adding discriminating anchors:
- **Foil-bridge** (−bridge, α=0.5, layer 20): the adversarial anchor. Same |Δ| as the bridge (threshold confound cancels in the difference), opposite sign predicted: S(foil) < 0 < S(bridge).
- **Strong-bridge** (bridge, α=1.0): tests margin-signing across the margin range (flips higher-m⁰ items; signing must hold, not just flip count).
- **8 fresh matched randoms** (new seed): inert anchors, |S| small.
- (Optional, if cheap: 2–3 EXP077 cone variants as additional inert anchors from committed vectors.)

**Phase-2 bars (binding):** S(bridge) > 0 **and** S(foil-bridge) < 0 **and** |S(randoms)| < min(|S(bridge)|, |S(foil)|). KILL iff S(foil) ≥ 0 or S(bridge) ≤ 0. The foil is the confound-breaker: it flips ~as much as the bridge (same mechanics) but its flips should concentrate at *high* m⁰ (it can only overturn confident correct-baseline decisions... more precisely, its good/bad flip composition is inverted relative to the bridge — the signing must detect this).

---

## 9. Risks and honest limitations

1. **n=1.** Phase 1 has one positive anchor (the bridge). It can KILL but cannot CONFIRM — stated in §3, not discovered later.
2. **Calibration fragility.** The entire license rests on P(correct|m⁰) increasing in m⁰ on this bench. EXP135's 48.3% score-degeneracy (guard (e)) hints margins may be ill-behaved; Test A exists precisely to check this before anything else.
3. **Threshold confound.** §4.3 names it; Phase 2's foil breaks it; Phase 1 cannot.
4. **Label-adjacent Test A.** Uses licensed facts (the 6 McNemar-b items), not raw labels, for instrument validation; fallback path flagged for Law #14 review of the Law #7 boundary.
5. **Scope discipline.** This sprint validates a *statistic*, not a loop. Integration is a separate future experiment. No claim about G-step candidates, other benches/backbones, or the summit is licensed by this sprint under any branch.

---

## 10. Design-lane verdict: **CONDITIONAL RUN**

**RUN Phase 1** (Test A + Test B, $0, zero new forwards, minutes of CPU): the gate is honest — Test A is a *real* falsifier of the load-bearing assumption (not a tautology), the costs are negligible, and the information value is high in both branches (a KILL here teaches the program that model confidence is uninformative on this bench, which also prices S4-5's premise).

**Phase 2 only if Phase 1 passes both bars** — it is the actual test of the signing, and it must not run on a failed license.

**DO NOT RUN anything beyond Phase 2's pre-registered anchors** on this design's authority. If Phase 2 CONTINUEs, the follow-on (E-step replacement integration) needs its own worth-it gate and experiment number.

*The E-step died because it scored stability when it needed to score efficacy. The only label-free signature of efficacy is the model's own uncertainty. This sprint tests whether that signature is real — cheaply, falsifiably, and with the confounds named up front.*
