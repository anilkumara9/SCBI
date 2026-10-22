# Innovation Sprint — SUMMIT-aimed mechanism candidates, ROUND 2 (2026-09-29)

**Sprint lane:** LOG-4562 (pre-assigned). $0 CPU, proposals only — no execution, no experiment numbers minted, no signed protocol touched, no GPU contact.
**Summit question:** *What discovery would have to be true for a frozen model (Δθ=0) to become far more cognitively capable through inference-time computation?*
**Status:** PROPOSAL DOSSIER — licenses nothing. Every candidate below requires its own signed pre-registration + independent Law #14 review before any execution (launch chain). This dossier is differentiated against SPRINT_2026-09-29_SUMMIT.md (round 1: H1–H4), SPRINT_2026-09-25_SUMMIT.md, NEXT_DIRECTION_SPRINT_2026-09-28.md, and all verdicts through LOG-4561.

---

## 1. Evidence base (ground truth these candidates are built on)

[OBSERVATION] — all numbers from primary artifacts / the research log:

- **Round 1 fully executed (LOG-4552–4558):**
  - **EXP106 (H3/LFH):** 60/60, p=8.67×10⁻¹⁹ → registered CONTINUE.
  - **EXP107 (template-control kill-test):** 34/60, p=0.1831, with the exact template-detector signature (30/30 original-word cells, 4/30 flipped-word cells) → **KILL the EXP106 transfer reading.** Lesson: any readout-head or decoding claim must carry a template-control kill-test in the pre-registration, or it is unfalsifiable decoration.
  - **EXP108 (H1/HDI):** RUN-INVALID — elicitation failure. All 60 self-reports unparseable; base Pythia-410m emitted the repetition sequence `\n\nQuestion:` (token IDs `[187,187,23433,27]`) — it continued the document pattern instead of answering.
  - **EXP109 (H4/PTTSC):** RUN-INVALID — elicitation failure. Planner arm: 18/20 items produced zero numbered outlines (repetition attractor: "Plan: Write a list of the possible answers to the question."); baseline arm: 80/80 samples unparseable. n_valid=0.
  - **EXP110 (H2/QBR):** CERTIFIED-WITH-NOTE (6/7 tiers, structural tiers intact) — the EXP105 battery's binding KILL-at-step-9 verdict is precision-certified under weight-only INT8 fake-quantization. Precision-robustness is now a [OBSERVATION], not a new question.
- **The durable methodological finding:** base Pythia-410m does not reliably execute instruction-style generation prompts under frozen CPU protocols. Any candidate requiring structured generation must either be rejected or carry a validated elicitation design with a Law #14-grade degeneracy guard. Logit readout (fixed-position option log-probs, no autoregressive decoding) remains fully licensed.
- **The Decodability Gap (EXP105/I2′, LOG-4491):** error signals decode at 6.7× chance yet steer zero decisions (ΔM_R=0, n_pop=21, Refuted/KILL at step 9). Certified precision-robust (EXP110).
- **Static family closed:** EXP094 (0/120 flips), EXP095 (5-point α dose-response flat, REFUTED), EXP096 (headroom-gated, REFUTED), EXP097 (threshold account killed). No further static per-item experiments licensed.
- **Bridges are artifacts:** option-informed bridges rescue +10–16pp but are label-informed (Law #7) — rescue controls, not autonomous mechanisms.
- **Frozen backbone:** Δθ=0, pin `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed` (LOG-331). Independent verdict review: EXP107 BIND, EXP108 QUALIFY, EXP109 BIND, EXP110 BIND (LOG-4559).
- **EXP107 bench:** 60 items in four balanced 15-item cells (A-first/C-first × original/flipped word families), template-decorrelated by deterministic string rewriting; raw embeddings archived at `experiments/runs/EXP107_templatectrl/out/exp107_test_embeddings.npz`.

## 2. Design constraints (what is dead, what is occupied)

**Do not propose:** static/unconditional injection at any strength, layer, or gating (S4/S5/I2′ closed); dose-response re-sweeps (EXP095); threshold-account variants (EXP097); zero-shot cosine/direction scoring (EXP091); decode-probe re-runs (S5-3); QK-subspace operators (G1); Procrustes fits (retracted); trained heads on template-correlated benches without a template kill-test (EXP106→EXP107); any generation-dependent protocol without a validated elicitation design (EXP108/EXP109); precision-robustness re-measurements (EXP110 certified — a known property).
**Occupied by prior sprints (do not duplicate):** IBL, TGA, CGD, SCS, LTI, GNR, SAR (2026-09-25); S6-1…S6-5 (2026-09-28); H1–H4 (round 1, 2026-09-29).
**Occupied by prior art:** Family C inference-time search+self-eval, Family D logit optimization, Family E feedback control, PTTS (Wu et al. 2609.27374), Meta FAIR 2609.26704, JEV-27B / CLM-8B (frozen-backbone + trained head), 2609.06473 (steering under compression — adopted, LOG-4528).

---

## 3. The four candidates

Each carries the full worth-it gate: (1) exact question, (2) KILL/CONTINUE/PIVOT decision changed, (3) cheapest test + cost, (4) mathematical license, (5) quantitative prediction, (6) breaking point. Every candidate also carries a built-in adversarial kill-test and an honesty fence.

---

### H5 — LFH-TD: Label-Free Head on the Template-Decorrelated Bench

**Mechanism sketch.** EXP106's 60/60 died because the bench carried a template cue; EXP107 built the template-decorrelated bench where a pure template detector scores ~30/60. LFH-TD is the honest successor: train an L2-logistic head on frozen embeddings using **only the EXP107 bench items with template-decorrelated labels** (disjoint split within the bench; zero template-label correlation in train and test by construction), with the JEV-27B block-off byte-identity discipline and the Law #14 fixes from round 1 (C=1.0, frozen Pythia-410m layer 20, Law #7 on every selection decision). The EXP107 cell structure is the **built-in kill-test**: per-cell accuracy must not show the template-detector signature (high on original-word cells, at-chance on flipped-word cells) — if it does, the transfer reading is dead, no rerun.

**Worth-it gate.**
1. *Exact question:* Does a trained linear head on the frozen backbone transfer above chance when trained and evaluated on a bench where word-template cues are decorrelated from labels?
2. *Decision changed:* **CONTINUE** the output-side capability program (→ first autonomous output-side result; licenses GPU head-training) vs **KILL** it (even trained readouts don't transfer on a template-decorrelated bench; the room is template-artifact-only — retire it).
3. *Cheapest test + cost:* logistic regression on archived `exp107_test_embeddings.npz` (possibly zero new forwards) + disjointness check + block-off byte-identity + per-cell kill-test read. **$0 CPU, ~1h.**
4. *Mathematical license:* linear-probe theory (Alain & Bengio — a linear head can only extract information present in the embedding; a positive is not manufacturable from noise); EXP107 [OBSERVATION] that the bench is template-decorrelated (pure template detector ≈ 30/60). Any above-chance result cannot be template detection.
5. *Quantitative prediction:* head accuracy ≥ 40/60 on the held-out decorrelated split (binomial p ≈ 0.003 vs 0.5) with byte-identical block-off AND no template-detector signature across the four cells → CONTINUE.
6. *Breaking point:* ≤ 35/60 (p > 0.05) OR template-detector signature present → **KILL** "trained output-side readout transfers."

**Novelty audit.** No trained-head experiment on a template-decorrelated bench exists in the corpus. N1.

---

### H6 — HDI-LR: Honesty-Decodability Instrument, Logit-Readout Form

**Mechanism sketch.** H1/EXP108 died at the generation layer, not the hypothesis layer. HDI-LR re-asks the honesty question without any generation: decision = argmax of the registered decision statistic; self-report = argmax over the two **first-token entity-name logits** after a self-report prompt (no autoregressive decoding — only the position-0 logits are read). Fidelity = P(self-report readout == decision). Pre-registered **degeneracy guard** (Law #14-grade): total probability mass on the two entity names at the readout position must exceed a pinned threshold (e.g., ≥ 1% of top-1 probability); else RUN-INVALID — a flat readout cannot speak. This is a NEW hypothesis with a different apparatus, not a retry of H1.

**Worth-it gate.**
1. *Exact question:* At fixed first-token logit readout, is there a measurable, calibrated gap between the decodability of the model's self-report and its fidelity to the decision statistic?
2. *Decision changed:* **CONTINUE** the honesty-instrument program (→ oversight primitive for the post-Astra binding constraint; G/E/S/T-loop component) vs **KILL** it (self-report is either perfect or noise at logit level — no instrument exists).
3. *Cheapest test + cost:* 60 self-report forward passes (frozen Pythia-410m, CPU) reading only first-token logits + the archived decision statistics. No bench labels touch the apparatus beyond the pre-registered use (Law #7 clean). **$0 CPU, ~2h.**
4. *Mathematical license:* Berg et al. (arXiv:2510.24797, logged 2026-09-27): SAE deception-feature suppression moves self-reports 96% → 16% — [OBSERVATION] that the self-report channel is causally separable from task behavior. First-token logit readout is the standard linear-probe-equivalent for next-token choice; the fidelity gap is well-defined whether or not the readout is perfect.
5. *Quantitative prediction:* fidelity ∈ [0.60, 0.95] (real signal with a real gap) and self-report decodability ≥ 2× chance → CONTINUE.
6. *Breaking point:* fidelity ≥ 0.98 (no gap to study), ≤ 0.55 (no signal), or degeneracy guard fires → **KILL** (or RUN-INVALID respectively, pre-registered).

**Novelty audit.** No logit-readout honesty instrument in the corpus. N1. Differentiated from EXP108 by apparatus (readout vs generation) — not a duplicate lane.

---

### H7 — EVALID: Elicitation Validation Instrument (the apparatus question)

**Mechanism sketch.** EXP108/EXP109 retired *unvalidated* generation protocols — but the program still doesn't know whether ANY protocol produces parseable structured output from base Pythia-410m. H7 is a bounded apparatus experiment: K pinned elicitation protocols (e.g., few-shot-format-completion, constrained single-token-slot, numbered-list priming, repetition-penalty decoding) × 60 bench items, scored by pre-registered parseability rules. **Law #14-grade degeneracy guard:** repetition-attractor blocklist (including the EXP108 `[187,187,23433,27]` sequence and the EXP109 planner-loop phrase), per-protocol n_valid reported; the run is about the *protocol*, not the answers.

**Worth-it gate.**
1. *Exact question:* Does any of K pinned elicitation protocols produce ≥80% parseable structured outputs from frozen base Pythia-410m under CPU protocols?
2. *Decision changed:* **CONTINUE** (a protocol clears the bar → licensed elicitation for H1/H4 revival as NEW hypotheses with a validated protocol) vs **KILL** (best protocol <50% parseable → base model is ungenerable under CPU protocols; generation-based lines retired; all future work is logit-readout-only).
3. *Cheapest test + cost:* K=4–6 protocols × 60 short generations + pre-registered regex scoring. **$0 CPU, ~3h.**
4. *Mathematical license:* negative — the measurement is descriptive, but the decision it changes is load-bearing for the whole program's apparatus posture. The bar (≥80% parseable) is set so that a CONTINUE actually licenses downstream protocols; the breaking point (<50%) is set so that a KILL is honest, not a matter of taste.
5. *Quantitative prediction:* best protocol ≥ 80% parseable → CONTINUE.
6. *Breaking point:* best protocol < 50% parseable → **KILL** generation-based experimentation on this backbone.

**Novelty audit.** Apparatus validation, not capability. N1. Honest framing: this is infrastructure; it unlocks lines rather than advancing the summit directly.

---

### H8 — POE: Positional-Order Ensembling (test-time augmentation, zero generation)

**Mechanism sketch.** Positional bias (first/last-option preference) is a known error source in multiple-choice readouts. POE is test-time scaling with no generation and no template trap: for each bench item, present the options in K random orders, read the option log-probs at the fixed decision position each time, average the logits across orders, and take argmax. Baseline: single canonical order. This is genuine inference-time computation (K× forward passes) on the frozen backbone, randomized so no template or position cue can be the signal.

**Worth-it gate.**
1. *Exact question:* At fixed frozen backbone, does averaging option logits over randomized presentation orders beat a single-order readout on the 60-item bench?
2. *Decision changed:* **CONTINUE** the test-time-scaling axis (→ order-ensembling enters the EXP068-family adaptive-loop designs) vs **KILL** it (presentation averaging adds nothing; the TTA axis is dead for this task class).
3. *Cheapest test + cost:* 60 items × K=5 orders × 2-option logit readouts = 600 forward passes, frozen Pythia-410m, CPU, zero generation. **$0 CPU, ~2h.**
4. *Mathematical license:* variance reduction by ensembling — if per-order errors are not perfectly correlated (positional bias rotates across orders), the averaged statistic has strictly lower variance around the position-invariant component (Condorcet/ensemble logic; standard). Paired McNemar (order-ensemble vs single-order) is the registered test.
5. *Quantitative prediction:* ensemble accuracy ≥ single-order + 3/60 items (≈ +5pp; paired McNemar one-sided p ≤ 0.05).
6. *Breaking point:* ensemble ≤ single-order (paired p > 0.05) → **KILL** positional-order ensembling.

**Novelty audit.** Positional-bias ensembling is known in the literature (known combination with our bench/apparatus); N1. Summit filter: honest capability pilot — inference-time computation buying accuracy from a frozen model.

---

## 4. Ranking (falsifiability-per-dollar × summit relevance)

| Rank | Candidate | Cost | Kill buys | Continue buys |
|---|---|---|---|---|
| **1** | **H5 LFH-TD** | ~1h | Retires the output-side room as template-artifact-only (deepens EXP107) | First autonomous output-side result; licenses GPU head-training |
| **2** | **H6 HDI-LR** | ~2h | Kills the honesty-instrument premise at logit level | Oversight primitive for the post-Astra binding constraint |
| **3** | **H7 EVALID** | ~3h | Retires generation-based lines on this backbone honestly | Licensed elicitation protocol; H1/H4 revived as new hypotheses |
| **4** | **H8 POE** | ~2h | Kills the presentation-ensembling TTA axis | Order-ensembling for the adaptive loop |

## 5. Killed at the gate (recorded, not resurrected)

- **Direct H1/H4 revival ("try a better prompt").** Generation degeneracy is a measured [OBSERVATION] (EXP108/109), not a tuning failure. A retry without a validated protocol fails the worth-it gate's "cheapest test" (there is no cheap distinguishing test — any prompt is a new unvalidated apparatus). Revival is gated on H7-CONTINUE only.
- **Multi-token self-consistency voting.** Requires parseable generation → gated on H7. Killed as a standalone candidate; not forgotten.
- **Per-layer trained-head transfer search.** Contingent on H5-CONTINUE; folded as a secondary registered analysis of H5 rather than a standalone lane (avoids a premature 12-layer × 60-item matrix before the room is known to exist).
- **Logit-lens causal probes of intermediate layers.** This is static per-item geometry by another name — the closed family (EXP094–097, S6). Killed.
- **True-INT8 / bitsandbytes-exact precision follow-up.** GPU-gated; the honest ceiling was already named in EXP110. Killed as a CPU candidate.
- **Readout head on the EXP106 bench with "careful templates."** EXP107 proved the decorrelated bench exists — use it. Proposing on the correlated bench again fails the gate's falsifiability (no kill-test available there). Killed.

## 6. Recommendation

**Run H5 first.** It is the only candidate with positive-signal upside — the program's missing "number that goes up" — at the lowest cost, on archived embeddings, with the EXP107 kill-test pre-installed. Both outcomes are decisive: CONTINUE gives the first autonomous output-side result and licenses the GPU head-training proposal; KILL retires the room honestly and deepens the EXP107 interpretation. Law #7-safe by construction (decorrelated bench, disjoint splits), Law #6-safe (backbone untouched), and it cannot repeat EXP106's failure mode by design. H6 follows as the summit instrument in logit-readout form; H7 as the apparatus decision the whole generation program is waiting on; H8 as the honest test-time-scaling pilot.

## 7. Session notes

- Summit filter applied: H5 and H8 are capability-positive (frozen model gaining decision capability via inference-time apparatus — H5 via trained readout, H8 via test-time computation); H6 is a summit instrument (oversight of agentic cognition — the post-Astra binding constraint); H7 is apparatus infrastructure (honest about it). No candidate claims consciousness, superhuman achievement, or generality beyond its bench.
- Today's three lessons are load-bearing in every candidate: (a) H5's kill-test is the EXP107 instrument itself; H6/H8 require zero generation; H7 is the apparatus question generation left behind; (b) no candidate touches precision (EXP110 closed it); (c) H1/H4 are NOT revived — they are succeeded by H6/H7 under new apparatuses.
- No experiments executed in this sprint ($0 CPU, proposals only). Next step per candidate: signed pre-registration + independent Law #14 review (launch chain). This dossier is a proposal record, not a license.
- Epistemological labeling per AGENTS.md §5 used throughout ([OBSERVATION], [HYPOTHESIS], [INTERPRETATION] where interpretations appear).
