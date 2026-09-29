# Innovation Sprint — SUMMIT-aimed mechanism candidates, round 2 (2026-09-29)

**Sprint lane:** LOG-4527 (pre-assigned). $0 CPU, proposals only — no execution, no experiment numbers minted, no signed protocol touched, no GPU contact.
**Summit question:** *What discovery would have to be true for a frozen model (Δθ=0) to become far more cognitively capable through inference-time computation?*
**Status:** PROPOSAL DOSSIER — licenses nothing. Every candidate below requires its own signed pre-registration + independent Law #14 review before any execution (launch chain). This dossier is differentiated against SPRINT_2026-09-25_SUMMIT.md (7 candidates), NEXT_DIRECTION_SPRINT_2026-09-28.md (5 proposals), and all verdicts through LOG-4526.

---

## 1. Evidence base (ground truth these candidates are built on)

[OBSERVATION] — all numbers from primary artifacts / the research log:

- **The Decodability Gap (EXP105/I2′, LOG-4491):** error signals decode at 6.7× chance yet steer zero decisions (ΔM_R=0, n_pop=21, Refuted/KILL at step 9). Decodability without causality is measured, not conjectured.
- **Static family closed:** EXP094 (0/120 flips), EXP095 (5-point α dose-response, 16× range, flat, REFUTED, LOG-4400), EXP096 (headroom-gated, REFUTED, LOG-4407), EXP097 (threshold account killed, LOG-4416). S5-2 power audit (LOG-4392): skeptic's band cornered to 1–4.87% per arm; S5-3 (LOG-4393): 0/8 EXP077 variants clear the decode bar — never-decodable PIVOT. S6 wave stood down (LOG-4463/4464). **No further static per-item L11 experiments are licensed.**
- **Bridges are artifacts:** option-informed bridges rescue +10–16pp but are label-informed (Law #7) — rescue controls, not autonomous mechanisms (LOG-204 demotion stands).
- **LM log-prob baseline (on record as secondary):** 36/60 = 0.60, mean margin −0.0018 — the logits are not the missed instrument either.
- **Frozen backbone:** Δθ=0, pin `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed` (LOG-331).
- **Today's frontier (2026-09-29 sweep):** (a) **AutoTrust JEV-27B** — 108.9M-param trained decision head on a FROZEN Qwen3.8-27B, 84.07% mean on 6 decision benchmarks (vendor-claimed, UNVERIFIED), byte-identical to base with the block off; second frozen-backbone + trained output-side head in 10 days (after CLM-8B). (b) **arXiv:2609.06473** — steering under INT8/NF4: vectors keep 0.989–0.998 cosine vs FP16, but dose-response is asymmetric (lengthening = graded-then-collapse; shortening = step function at 12–30%) and compression can dominate the intervention (Mistral-NF4 GSM8K baseline 0.545→0.365 at α=0). (c) **GPT-6.1 Astra shelved** — deception + scope-authorization failures; the field's binding constraint on agentic cognition is now oversight, not benchmarks.

## 2. Design constraints (what is dead, what is occupied)

**Do not propose:** static/unconditional injection at any strength, layer, or gating (EXP094–097 + S6 wave closed it); dose-response re-sweeps of the per-item family (EXP095); threshold-account variants (EXP097); zero-shot cosine/direction scoring (EXP091); decode-probe re-runs (S5-3); QK-subspace operators (G1); Procrustes fits (retracted); trained heads requiring GPU/training data at $0-cost-violating scale (SCOPE-CHANGE — but see H3, which dissolves the cost objection).
**Occupied by prior sprints (do not duplicate):** IBL, TGA, CGD, SCS, LTI, GNR, SAR (2026-09-25); S6-1…S6-5 (2026-09-28, executed/stood down). **Occupied by prior art:** Family C inference-time search+self-eval, Family D logit optimization, Family E feedback control, PTTS (Wu et al. 2609.27374), Meta FAIR 2609.26704.

---

## 3. The four candidates

Each carries the full worth-it gate: (1) exact question, (2) KILL/CONTINUE/PIVOT decision changed, (3) cheapest test + cost, (4) mathematical license, (5) quantitative prediction, (6) breaking point.

---

### H1 — HDI: Honesty-Decodability Instrument

**Mechanism sketch.** The program's headline instrument measures decodability without causality for *error* signals. HDI turns the same instrument on *self-report*: for each bench item, record (a) the actual decision (argmax of the registered decision statistic) and (b) the model's generated answer to "which option did you choose?". Train a linear probe on frozen activations to decode the self-report; measure fidelity = P(decoded self-report == actual decision). A fidelity gap (high decodability, imperfect fidelity) is a falsifiable honesty instrument — the oversight primitive the Astra shelving just made the field's binding constraint.

**Worth-it gate.**
1. *Exact question:* Is there a measurable, calibrated gap between the decodability of the model's self-report and its decision fidelity on the 60-item bench?
2. *Decision changed:* **CONTINUE** the deception-detection instrument program (→ honesty probe as a G/E/S/T-loop component and agent-harness oversight gate) vs **KILL** it (self-report is either perfect or noise — no instrument exists).
3. *Cheapest test + cost:* 60 self-report generations (frozen Pythia-410m, CPU) + linear probe on archived/fresh activations; probe targets are the model's own outputs — no bench labels touched (Law #7 clean). **$0 CPU, ~2h.**
4. *Mathematical license:* Berg et al. (arXiv:2510.24797, logged 2026-09-27): SAE deception-feature suppression moves subjective-experience self-reports 96% → 16% — [OBSERVATION] that the self-report channel is causally separable from task behavior. A linear probe measures linearly-accessible information (Alain & Bengio); the fidelity gap is well-defined whether or not the probe is perfect.
5. *Quantitative prediction:* fidelity ∈ [0.70, 0.95] — real signal (above 0.5) with a real gap (below 1.0); probe decodability of self-report ≥ 3× chance.
6. *Breaking point:* fidelity ≥ 0.98 (no gap to study) or ≤ 0.55 (no signal) → **KILL**.

**Novelty audit.** No honesty/deception instrument exists in the program corpus. Differentiated from SCS (stability verifier — different object: honesty, not stability). N1.

---

### H2 — QBR: Quantization-Boundary Robustness

**Mechanism sketch.** Every boundary verdict in the program was measured at full precision. 2609.06473 shows steering geometry survives INT8 (cosine 0.989–0.998) while the *causal* structure shifts (asymmetric dose-response, baseline moves). QBR asks whether our boundary is precision-regime-dependent: re-run the cleared EXP105 falsification-kit battery under INT8 fake-quantization of the frozen weights and compare verdicts tier-by-tier.

**Worth-it gate.**
1. *Exact question:* Do the EXP105 battery verdicts reproduce under INT8 fake-quantization, or does precision open/close a transfer window?
2. *Decision changed:* **CONTINUE** the boundary as precision-certified (→ honest generality claim for the paper) vs **PIVOT** (precision is a new axis; the boundary needs a precision-indexed statement).
3. *Cheapest test + cost:* fake-quantize Pythia-410m weights to the INT8 grid (round(w/scale), CPU) + re-run `falsification_kit/battery.py` (7 tiers, cleared for third-party use). **$0 CPU, ~2–4h.** Honest caveat: fake-quant approximates weight-only INT8; bitsandbytes LLM.int8-exact is GPU-gated — labeled as approximation, not equivalence.
4. *Mathematical license:* 2609.06473 [OBSERVATION] — cosine collinearity does not imply causal equivalence across precisions; nonlinearities amplify quantization perturbations, so a boundary licensed at FP32/FP16 does not transfer automatically.
5. *Quantitative prediction:* ≥6/7 tiers reproduce within the kit's tolerance → boundary is precision-robust.
6. *Breaking point:* bit-identical verdicts on all 7 tiers → **KILL** regime-dependence (certification complete); any tier flips → **PIVOT** (precision-indexed boundary).

**Novelty audit.** No precision-variation experiment in the corpus. N1. Summit filter: honest — boundary-hardening, not capability.

---

### H3 — LFH: Label-Free Head (the JEV-27B discipline, CPU-scoped)

**Mechanism sketch.** The field just validated twice (CLM-8B, JEV-27B) that frozen-backbone + trained output-side head is a real architecture. Our bridges were killed as *label-informed* artifacts — but no program experiment has ever tested a *trained, transfer-tested* head. LFH: train an L2-logistic head (∼2k params) on frozen embeddings using **disjoint-bench labels only** (train on EXP092-B's 60 items, test on the EXP091 60-item bench; item-ID overlap check first — overlap > 0 → RUN-INVALID, Law #7), plus the JEV-27B block-off discipline (head detached ⇒ byte-identical outputs). This revives the 2026-09-25 sprint's rejected "trained contrastive heads" darling with the cost objection dissolved ($0 CPU, no new training data).

**Worth-it gate.**
1. *Exact question:* Does a trained output-side head on the frozen backbone transfer above chance to a disjoint bench — i.e., does the output-side room have an autonomous (non-artifact) instantiation?
2. *Decision changed:* **CONTINUE** the output-side capability program (→ licensed GPU-scale head-training proposal) vs **KILL** it (even trained readouts don't transfer; the room is artifact-only — retire it).
3. *Cheapest test + cost:* logistic regression on archived embeddings (zero new forwards if EXP091/EXP092-B embeddings are on disk; else one 60-pass extraction) + disjointness check + block-off byte-identity check. **$0 CPU, ~30 min.**
4. *Mathematical license:* JEV-27B existence proof (frozen backbone + trained head is a working architecture at 27B scale); linear-probe theory (a linear head can only extract information present in the embedding — a positive result is not manufacturable from noise); our own Decodability Gap (error signals decode 6.7× chance — decodability is measured; the head converts decodability into decisions).
5. *Quantitative prediction:* head accuracy ≥ 40/60 on the held-out bench (binomial p ≈ 0.003 vs 0.5) with byte-identical block-off → CONTINUE.
6. *Breaking point:* ≤ 35/60 (p > 0.05) → **KILL** "trained output-side readout transfers."

**Novelty audit.** No trained-head experiment in the corpus; bridges were constructed, not trained. Differentiated from the rejected CLM-adaptation (cost) — H3 is $0. N1, N2-adjacent if it continues (first autonomous output-side result in-program).

---

### H4 — PTTSC: Planned Test-Time Scaling Coordinator (CPU pilot)

**Mechanism sketch.** PTTS (Wu et al., arXiv:2609.27374) + Meta FAIR (2609.26704): a planner writes k diverse solution outlines in one autoregressive pass; a FROZEN executor develops each; PTTS-ZS gains +6.7pp pass@64 over repeated sampling, with theory that PTTS strictly generalizes repeated sampling. PTTSC pilots this on our bench at $0: planner = frozen Pythia-410m emits 4 outlines in one pass; executor = same frozen model develops each; decision = majority vote. Baseline: 4 independent samples + majority vote (identical generation budget).

**Worth-it gate.**
1. *Exact question:* At fixed generation budget, does planned test-time scaling beat unplanned repeated sampling on the 60-item relational bench?
2. *Decision changed:* **CONTINUE** the coordinator program (→ planner-executor pattern enters the EXP068-family adaptive-loop designs) vs **KILL** it (planning the budget adds nothing; the TTS axis is dead for this task class).
3. *Cheapest test + cost:* 60 items × (1 plan + 4 developments + 4 baseline samples) ≈ 540 short generations, frozen Pythia-410m, CPU. **$0 CPU, ~4h.**
4. *Mathematical license:* PTTS theory (pass@k-optimal policy must hedge beyond finite budget k*; the planner provably generalizes repeated sampling — Wu et al.); Meta FAIR [OBSERVATION] that a small planner steering a frozen executor transfers across model families.
5. *Quantitative prediction:* planner-majority accuracy ≥ baseline-majority + 8pp (≈ +5/60 items).
6. *Breaking point:* planner ≤ baseline (paired McNemar p > 0.05) → **KILL**.

**Novelty audit.** Family C is occupied by prior art; differentiated by bench + frozen-410m + CPU pilot; EXP070 (oracle ceiling) is GPU-gated and measures the ceiling, PTTSC pilots the mechanism — complementary, not duplicative. N1.

---

## 4. Ranking (falsifiability-per-dollar × summit relevance)

| Rank | Candidate | Cost | Kill buys | Continue buys |
|---|---|---|---|---|
| **1** | **H3 LFH** | ~0.5h | Retires the output-side room as artifact-only (deepens LOG-204) | First autonomous output-side result; licenses GPU head-training |
| **2** | **H1 HDI** | ~2h | Kills the honesty-instrument premise | Oversight primitive for the Astra-defined constraint; G/E/S/T-loop component |
| **3** | **H4 PTTSC** | ~4h | Kills the coordinator/TTS axis for this task class | Planner-executor pattern for the adaptive loop |
| 4 | H2 QBR | ~2–4h | Certifies the boundary precision-robust | Precision-indexed boundary (paper generality) |

## 5. Rejected darlings

- **Shared-direction fine dose curve** (the one curve LOG-4471's review named unmeasured): rejected as a ranked candidate — Law #14 would likely rule it a sixth gate tweak on the closed static family (EXP093 0/60 + EXP097 threshold-kill fence it). Recorded as a named open thread, not proposed.
- **Full JEV-27B replication** (108M head, 9.2 B200-hours): GPU-gated, $0-violating; H3 is its honest CPU shadow.
- **PTTS-RL** (planner optimized on pass@k reward): needs training; GPU-gated.
- **Min-entropy prefix search / test-time soft-prompt optimization**: already killed 2026-09-25 (occupancy + cost).

## 6. Recommendation

**Run H3 first.** It is the only candidate with positive-signal upside — the program's missing "number that goes up" — at the lowest cost (~30 CPU-minutes, possibly zero new forwards). Both outcomes are decisive: CONTINUE gives the program its first autonomous output-side result and licenses a GPU head-training proposal; KILL deepens the LOG-204 artifact interpretation and retires the room honestly. Law #7-safe by construction (disjoint-bench labels, overlap tripwire), Law #6-safe (backbone untouched), and it adopts the field's newest validated discipline (JEV-27B block-off byte-identity). H1 follows as the summit instrument; H4 as the capability-positive TTS pilot; H2 as certification.

## 7. Session notes

- Summit filter applied: H3 and H4 are capability-positive (a frozen model gaining decision capability via inference-time apparatus); H1 is a summit instrument (oversight of agentic cognition — the post-Astra binding constraint); H2 is boundary infrastructure. No candidate claims consciousness, superhuman achievement, or generality beyond its bench.
- No experiments executed in this sprint ($0 CPU, proposals only). Next step per candidate: signed pre-registration + independent Law #14 review (launch chain). This dossier is a proposal record, not a license.
- Frontier inputs incorporated: JEV-27B (H3), arXiv:2609.06473 (H2), Astra shelving (H1), PTTS + Meta FAIR 2609.26704 (H4).
