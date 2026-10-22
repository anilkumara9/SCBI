# S6 Dynamic-Gating Rescue Program — Stand-Down Recommendation (2026-09-28)

*Status: RECOMMENDATION — not a protocol, not a draft, not executable. No experiment number minted. No pilot authorized. $0 compute; no model executed; no weights touched; no signed artifact modified.*

*Licensing chain: LOG-4448 (EXP101 verdict: Refuted) → LOG-4455 (EXP102 verdict: PIVOT-untestable) → LOG-4460 (CEO clearance, EXP103 minted; terminality claim: "no fifth externally-computed attention-gate variant, ever, under this license") → LOG-4461 (EXP103 mechanical execution, CEO-recovered record) → LOG-4462 (EXP103 binding verdict: **Refuted**, step-6 Gated KILL; {mean,max}×{L11,L20} 4/4 closed; surviving license narrows to "self-computed gates and beyond," each its own pre-registration and Law #14 review) → this lane (S6-4 innovation-design, completion-triggered chaining from LOG-4462).*

*All values below are from LOG-4400/4407/4409/4416/4423/4429/4432/4434/4440/4441/4447/4448/4454/4455/4461/4462, the EXP094–103 verdict reviews (`experiments/protocols/REVIEWS/`), and the frozen archives unless otherwise cited. No number is invented.*

---

## 0. The worth-it gate (binding on this lane)

This lane was charged with designing the next cheapest falsifying experiment within the surviving license — self-computed gates or a fundamentally different gating surface — or, if no design clears the worth-it gate, saying so. The gate requires five answers. They are given here, in order, before any design is proposed — because the answers are what kill the designs.

### (1) The exact question

Is there a CPU-testable ($0, Δθ=0, frozen Pythia-410m, EXP092-B) **self-computed-gate** design — or any fundamentally different gating surface — that is simultaneously:

(a) **genuinely self-computed**, i.e. not a repackaged externally-computed read (the LOG-4460 terminality claim bars "a fifth tweak of this family, ever, under this license," and the S6-3 drafts define the distinction: the gate must be computed *by* the model, not computed *from* the model's state by us);
(b) **principled-thresholded**, i.e. the firing rule carries a warrant comparable to the F5-adjudicated τ = 2×-uniform constant (LOG-4436), not a guessed number;
(c) **hypothesis-licensed**, i.e. some license-bearing observation in the program record motivates this gate over any other (the standard every S6 wave met: EXP098's L20 movement licensed the L20 read; EXP101's max firing licensed the max aggregation; LOG-4443's endorsed convention licensed the ordering);
(d) **interpretable**, i.e. a CONTINUE would mean something about steering, not about prompt compliance, label leakage, or decision-proxying (Law #7).

### (2) The decision it would change

**KILL:** self-gated movement < 6 flips at coverage ≥ 10% with the matched control sub-threshold → the self-gating family dies with the externally-computed one; the L11 direction's rescue program closes entirely. **CONTINUE:** ≥6 directional flips, McNemar-exact (doubling) p < 0.01, control flat, stratum-consistent, coverage ≥ 10% → the first conditional causal signal under self-conditioning; the program's next lane is the self-conditioning program. **PIVOT:** gate uninterpretable, collapsed, vacuous, or control-moved.

### (3) The cheapest falsifying test

Four candidate designs were constructed — the complete set this lane could devise under the hard constraints. Each is given with its killing attack. All four die.

**Candidate P — prompt-instructed self-gate.** Two-pass design: pass 1 asks the model a gating question appended to the prompt ("Rate entity relevance: RELEVANT or IRRELEVANT"); the model's discrete relevance token gates L11 injection @ 0.38 in pass 2; matched random control under the identical gate; 60 items; the S6-3d decision table mirrored.
*Killing attacks:* (i) Pythia-410m is a **base model, not instruction-tuned** — the relevance token is prompt-continuation noise, not a judgment; the gate's firing behavior is unpredictable and most likely degenerate (step 2b/2c) or uninterpretable. ~240 passes to discover base-model non-compliance. (ii) The "self" is illusory: we choose the question, the verbalizer, the parse rule — every design degree of freedom is ours; the no-peeking bright line cannot be drawn around a verbalizer choice that has no principled warrant. (iii) The prompt change **re-baselines the bench** — the EXP092-B pin, the 60/60 B-agreement foundation, and the entire LOG-4407/F5 license chain were adjudicated for the pinned prompt; this becomes a prompting study, not a steering study. (iv) A CONTINUE would mean "injection moves decisions where a base model emitted the RELEVANT token" — uninterpretable as steering (criterion (d) fails). **Verdict on P: fails (b), (c), (d). Dead.**

**Candidate E — output-uncertainty gate (entropy / margin).** Fire iff the B-pass output distribution's entropy ≥ τ_H (or top-1/top-2 margin ≤ τ_m); same arms and table.
*Killing attacks:* (i) **No principled threshold exists.** τ = 2×-uniform had a uniformity rationale (fire when the span attracts disproportionate attention vs the E/N baseline); entropy has no natural baseline and no adjudicated constant — any τ_H is a guess, and F5 re-opens with nothing to stand on (criterion (b) fails). (ii) **No hypothesis license.** No program observation links output uncertainty to where the task direction applies — unlike the attention family, which had EXP098's L20 movement and a relevance intuition. "Fire where the model is uncertain" is a guess (criterion (c) fails; the user's standing "don't blindly research" order bars it). (iii) It is arguably externally-computed-from-state with a new signal — permitted by the letter of the terminality claim (which names attention gates) but not by its spirit; a Law #14 review would demand the (b) and (c) answers this lane cannot give. **Verdict on E: fails (b), (c). Dead.** Mechanically cheapest (no hooks needed) — and still not worth running.

**Candidate C — activation-magnitude gate (residual norm / head-output norm at the span).** Fire iff some internal scalar ≥ threshold.
*Killing attack:* this is externally computed *from* the model's state by us — a fifth externally-computed gate with a different read. The LOG-4460 terminality claim bars it directly. **Verdict on C: fails (a). Dead by binding verdict.**

**Candidate B — probe-based gate.** Train a linear probe on frozen activations to predict a gating label.
*Killing attack:* the only available labels are answer correctness (→ the gate is a near-decision proxy **by construction**; Law #7 at full force; the LOG-197 bridge-leakage precedent demotes label-informed directions to rescue controls, not mechanism claims) or prior firing vectors (→ outcome-tuned; peeking). **Verdict on B: fails (d) structurally. Dead.**

### (4) Mathematical license — with quantitative prediction and breaking point

The McNemar/counting algebra carries mechanically to any candidate (N=60, α=0.01, ≥8 directional flips for p<0.01, ≥6 movement gate, 10% tripwire — all aggregation- and gate-independent, re-proved at LOG-4457/4459). **But the algebra is not the license.** Every S6 wave's license had two halves: the counting half (carried) and the *gate* half (why this signal, why this threshold — F5, no-peeking, the license record). For all four candidates the gate half is missing:

- P: parse rule and verbalizer are guesses; no license-bearing observation.
- E: threshold is a guess; no license-bearing observation.
- C: barred by binding terminality.
- B: barred by the leakage precedent.

A quantitative prediction ("≥6 flips") without a licensed gate is numerology, not science. The breaking point each candidate would need — "the threshold family / verbalizer / probe labels are wrong" — is un-testable within the design because the gate choice itself is unlicensed. **No candidate carries a complete mathematical license. The worth-it gate does not clear.**

### (5) Why self-computed gates were the next-cheapest surface — and why that is not enough

"Self-computed gates and beyond" is the **verdict's named surviving category** (LOG-4448, LOG-4455, LOG-4460, LOG-4462). A named category is not a design. The S6-3 family succeeded because each wave was licensed by an *observation* (EXP098's L20 movement; EXP101's max firing; LOG-4443's endorsed convention). For self-computed gates, this lane verified by search: **the category is empty** — "self-computed" appears in the program record only as named future work and scope-fence language (S6-3 v2 §1 summit filter: "A self-computed gate is future work, not this design"; S6-3d v2 §7). No prototype, no measurement, no threshold, no observation anywhere in EXP094–103 motivates any specific self-computed design. "The verdict didn't bar it" is not a license to run it.

---

## 1. The positive case for stand-down (not just the absence of a design)

The stand-down is not merely "we couldn't think of anything." The program's steering hypothesis has been falsified in every form it was given:

- **Static family:** EXP094 (inertness, 0/120), EXP095 (α-grid {0,0,0,1,1}, all p=1.0), EXP096 (headroom-gated α=8.0, 3 flips p=1.0) → Refuted; EXP097 (super-license {1.5,3.0}) → PIVOT (fragility — random outmoves task).
- **Dynamic externally-computed gating:** EXP100 (L11-mean, 0/60 → untestable), EXP101 (L11-max, 16/60, 1 flip → Refuted), EXP102 (L20-mean, 1/60 → untestable), EXP103 (L20-max, 55/60, 3 mixed flips p=1.0 → Refuted). Family closed 4/4; terminality engaged.
- **Composition:** EXP098 → PIVOT (premise — composition not supported).
- **Layer sweep:** EXP099 → PIVOT (fragility).
- **Pooled bound:** S6-5 — 5/381 task-direction decision flips → one-sided 95% upper bound **2.74%** on the task-direction flip rate.

The rational update after 4/4 gate closure is not "try a fifth gate family on the same direction" — it is **the direction is the problem, not the gate**. Ten experiments, ~2,000 CPU passes, every rescue dead or uninterpretable. The L11 per-item task direction does not move decisions under any gating tried, and no licensed reason exists to believe an unlicensed gate would differ. Continuing to gate the same dead direction is the sunk-cost fallacy with a lab coat on.

---

## 2. Recommendation (scoped)

**Stand down the S6 L11-direction rescue program — all of it, not just the gate family.** No further experiment that injects the killed per-item L11 task direction (static, gated, composed, or otherwise) is recommended on the CPU lanes. This recommendation is scoped to the S6 rescue program; it alters no EXP094–103 verdict, closes no other workstream, and touches no signed artifact.

**Redirect (for the CEO, not this lane):**
1. **The summit lane is the GPU queue** — K2 → EXP083 → EXP084 → EXP086 Stage B → EXP088 → EXP087 (adaptive-loop / relational program, parked on the founder's Kaggle). That program tests *mechanisms*, not rescues of a dead direction. Nothing in this recommendation touches it.
2. **CPU redirect options** (no new steering runs): the v83 paper revision (EXP095–103 postdate v82; the wall now has its far side and its gate-family closure — the citable boundary infrastructure the founder asked for); the commissioned legendary-paper gap analysis (outstanding); the GitHub push cycle (LOG-4393 onward unpushed); archival of the S6 family record.
3. **Re-opening conditions (pre-registered honestly):** this stand-down re-opens if and only if (i) a *license-bearing observation* for a specific self-computed gate appears in the program record (a measurement, not a category name); or (ii) a new direction family (not the killed L11 per-item direction) earns its own license; or (iii) the founder orders otherwise. "A new idea" without (i) or (ii) does not re-open it.

**Death-debt accounting (LOG-219):** this lane IS the death-debt payment for EXP103's null — the candidate was constructed (four designs), each was falsified on paper with its killing attack, and the workstream closes with the debt paid in analysis rather than in passes.

**Naming note:** the "S6-4" designation is taken (layer-sweep packet → EXP099; `research/innovation/S6-4_PREREG_DRAFT_2026-09-28.md` exists). This lane's task brief reused the label; no file was written under it. Any future self-gate design that ever clears the worth-it gate needs a fresh designation (S6-6 / S7-series).

---

*Recommendation written 2026-09-28 by the S6-4 innovation-design lane. $0 compute; no model runs; no weights touched. No pilot authorized; no experiment number minted; no clearance taken; no dispatch made. Lane stopping.*
