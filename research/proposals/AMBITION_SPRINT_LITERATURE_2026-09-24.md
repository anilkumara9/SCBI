# SCBI AMBITION SPRINT — Literature / Adjacent-Fields Candidates (2026-09-24)

**Role:** Literature / Adjacent-Fields specialist, LOG-250 dispatch
**Governing laws:** Frozen backbone (θ_after = θ_before); $0 free-tier compute only; falsification discipline; Law #15 worth-it gate; five permitted verdicts (Supported / Not supported / Inconclusive / Underdetermined / Refuted); evidentiary levels L1 ≠ L2 ≠ L3 never silently crossed.
**Epistemic standard:** repo 10-label standard. `[OBSERVATION]` = measured. `[CONJECTURE]` = plausible, untested. `[FACT]` = established record. Field priors below are cited from training knowledge, **not** live-verified: `browser.search` returned HTTP 401 (upstream credential expired) at 2026-09-24 ~11:12 IST, so no 2024–2026 web verification was possible in this pass. Every literature-derived claim is tagged `[UNVERIFIED-WEB]` and must pass the program's V-record re-fetch rule before any citation in a signed artifact.
**Compute basis:** [FACT] ~22 forward passes/s on pythia-410m (2×T4), per Sprint 2/3 records. T4-hours = passes / 22 / 3600. All costs $0 (Kaggle free tier).

## §0. What was mined, what was excluded, and why

**Mined fields:** control theory beyond LQR (MPC, non-normal/pseudospectral dynamics), neuroscience (attractor working memory, predictive coding precision, edge-of-chaos), dynamical systems (transient amplification, bifurcations), test-time recurrence (DEQ/universal-transformer lineage, used at test time only), in-context-learning theory, program synthesis (considered, rejected — see below), mechanistic interpretability (SAE/transcoder steering — already queued as Sprint 1 New Idea 4, not duplicated).

**Hard exclusions (per-prior reasoning, recorded so the graveyard stays clean):**
- *Static steering / direction injection (any sourcing):* KILLED family (EXP065/066/077/078, ΔM = 0.0pp). A "self-generated task vector" variant was drafted and **cut**: same operator (add a static vector), new sourcing does not change the operator class — re-proposing it would violate the kill-license discipline (mentor P3).
- *Gradient-constructed test-time directions (TTT-style activation gradients, one-VJP):* already queued as D2 (demoted) and occupied by ∇-Reasoner prior. Not duplicated.
- *SAE/transcoder feature steering:* queued as Sprint 1 New Idea 4 (Gemma Scope 2). Not duplicated.
- *Hopfield/associative trace memory:* overlaps S3-2 LOM (library-of-operators retrieval) in mechanism spirit (retrieval-based per-instance composition). Not duplicated.
- *Program-synthesis / external symbolic executor as verifier:* rejected — on the 2-hop multiple-choice testbed it collapses to "write the composition explicitly," i.e. CoT with a checker; the capability would live in the external executor, violating the program's mechanism-level (P1) framing. Revisit only if the testbed changes.
- *Working-memory gated maintenance (re-inject a maintained vector every layer):* overlaps M1 (multi-layer bridge cascade) in operator structure. Not duplicated.

**Five candidates survive.** All are [CONJECTURE]/Underdetermined (untested) with priced pilots. None touches a killed operator or a queued candidate (exclusion argued per candidate).

---

## Candidate 1 — TNA: Transient amplification via non-normal residual dynamics

### 1. Source field + prior
**Dynamical systems / hydrodynamic stability: non-normal operators and pseudospectra.** Trefethen & Embree, *Spectra and Pseudospectra* (2005) `[UNVERIFIED-WEB]`; transient growth in non-normal linear systems (Schmid 2007, Annu. Rev. Fluid Mech.) `[UNVERIFIED-WEB]`. Core fact: for a *non-normal* matrix A (AA* ≠ A*A), perturbations can be amplified by factors ≫ 1 over finite time even when all eigenvalues are stable (|λ| < 1) — eigenvalue analysis misses it; the right object is the ε-pseudospectrum and the Kreiss Matrix Theorem: sup_{k≥0} ‖A^k‖ ≥ ρ_ε(A)/ε, where ρ_ε is the pseudospectral radius.

### 2. Translation (precise)
The residual stream's layer-to-layer map h_{l+1} = F_l(h_l), linearized at the operating point (Jacobian J_l = ∂F_l/∂h_l), is a product of non-normal operators (attention + MLP blocks are generically non-normal: [CONJECTURE]). A small injected perturbation δ at layer l* evolves as δ_{l+1} ≈ J_l δ_l. **Mechanism:** *design* interventions to align with the leading right singular vectors of the downstream Jacobian product Π_{l>l*} J_l — the maximal-transient-growth directions — rather than with semantic contrast directions (killed family). The ×1.8 downstream gain measured in S3-8 [OBSERVATION: L1 explains ~57%; mean residual +0.3225; g ≈ 1.8 on EXP066 rescued items] is the first sighting of exactly this phenomenon and currently has no mathematical home; TNA gives it one. The intervention content is *dynamically* privileged, not semantically privileged.

### 3. Exclusion reasoning
- **Not killed:** the killed family is *semantic* static geometry (contrast/cone/offset/Procrustes directions, ΔM = 0). No killed experiment ever measured, or injected along, singular vectors of the layer-transition Jacobian. G1 killed the *QK-subspace* energy story (weight projectors), a different object from the *dynamical* amplification of the full nonlinear map.
- **Not queued:** S3-8 *measured* the ×1.8 gain but proposed no mechanism for it; S3-9 asks whether g(α) is linear vs routing-like but stays phenomenological; ARP (S3-1) measures response profiles but does not construct maximal-growth directions; A-LQR uses Jacobian *feedback to a setpoint*, not open-loop transient-growth alignment. No queue item does pseudospectral analysis.

### 4. Law #15 packet
1. **Precise question:** Does aligning an injected perturbation with the leading right singular vectors of the downstream Jacobian product produce strictly larger decision-flip rates per unit perturbation norm than semantic-contrast or random directions — i.e., is the ×1.8 downstream gain exploitable as a *designed* amplifier? Measurand: ΔM (decision flips, exact McNemar) per ‖δ‖₂, N=60, pythia-410m L20 injection.
2. **Decision:** KILL / CONTINUE. KILL (threshold below) retires the "dynamical amplifier" mechanism family and forces the ×1.8 gain to be re-explained as routing (S3-9's question) or readout; CONTINUE (gain ≥ bar) promotes TNA to a QUEUED Phase-2 mechanism with a pre-registered singular-vector intervention experiment.
3. **Cheapest test:** two-stage. Stage A ($0 CPU, weight-only): Henrici non-normality index per layer, He = (‖J_l‖_F² − Σ|λ_i|²)^{1/2}/‖J_l‖_F, on archived-or-fresh Jacobians — if every layer is near-normal (He ≈ 0), the license evaporates before GPU. Stage B (live pilot): 60 items × {top-singular-vector δ, random-unit δ, semantic B_agg δ} × 2 norms = 360 passes ≈ **0.0045 T4-h**. Discriminant arm: random δ must be included so "any perturbation amplifies" is separable from "singular alignment amplifies."
4. **Mathematical license:** Kreiss Matrix Theorem (theorem) → quantitative prediction: maximal transient growth G_max = sup_k ‖ΠJ‖ over k downstream layers satisfies G_max ≥ ρ_ε/ε for the measured ε-pseudospectrum; pilot prediction: flip-rate-per-norm(top-singular) ≥ 1.5× flip-rate-per-norm(random) at matched ‖δ‖₂ (bar set below the observed ×1.8 so the test is fair to the phenomenon). **Breaking point:** if measured G_max < 1.2× over the full (α, singular-rank) grid while the output bridge still rescues on the same items, transient amplification cannot carry the ×1.8 signal — TNA is dead as the mechanism, whatever the theory says in fluids.
- **Unique support vs competitors:** only TNA predicts *which* perturbations amplify (singular-vector alignment rank-orders the gain); the linear-gain story (S3-9's flat-g hypothesis) predicts rank-indifference; routing predicts α-dependence but not singular-rank dependence. The rank-ordered gain curve is the discriminating signature.
- **What kills it:** flat gain across singular ranks (p ≥ 0.1 for rank trend) with ΔM_top-singular ≤ ΔM_random at matched norm; or Stage-A He ≈ 0 across layers 20–32.

**Verdict: Underdetermined** (untested). Priced pilot: $0 CPU + 0.0045 T4-h.

---

## Candidate 2 — TTLRA: Test-time looped refinement / attractor settling

### 1. Source field + prior
**Neuroscience attractor networks + ML test-time recurrence.** Hopfield (1982) content-addressable/attractor dynamics `[UNVERIFIED-WEB]`; prefrontal working-memory maintenance via recurrent attractor settling (Wang 2001) `[UNVERIFIED-WEB]`; ML lineage: Universal Transformer (Dehghani et al. 2019, recurrent depth) and Deep Equilibrium Models (Bai et al. 2019, fixed-point iteration of a layer) `[UNVERIFIED-WEB]` — both train the recurrence; here the recurrence is applied **at test time only to a frozen model**, which neither prior does.

### 2. Translation (precise)
Pick a layer block [l1, l2] (e.g. 18–22). At inference time, replace the single forward application with K-fold iteration: h^{(k+1)} = F_{[l1,l2]}(h^{(k)}), h^{(0)} = h_{l1}, then continue the forward pass from h^{(K)}. Δθ = 0 [PROPOSITION]: no parameter is mutated; the recurrence is temporary computational state, squarely inside the canonical objective (B_t changing during inference). **Mechanism:** attractor-like denoising/settling of the relational representation — iterated application of a contractive-ish map moves h toward the basin's fixed point, cleaning up the compositional binding before the answer position is read. This is *qualitatively new computation* (P1): the model performs iterative inference it was never trained to do.

### 3. Exclusion reasoning
- **Not killed:** no killed experiment iterated a layer block; killed items are one-shot static injections and oracle static loops.
- **Not queued:** C-B (self-bridge fixed-point iteration) iterates *intervention strength* in bridge space — different object (scalar α dynamics vs activation dynamics); DEER is early *exit* (less compute), this is *more* compute in a loop; Self-Refine iterates at text level; D3 searches placement (α, l*, p), not recurrent depth. The G/E/S/T loop spec iterates generate→evaluate→select over candidates; TTLRA iterates the *representation itself* with no evaluator.

### 4. Law #15 packet
1. **Precise question:** Does K-fold test-time iteration of a frozen layer block change 2-hop decisions beyond what matched-compute baselines achieve — i.e., does attractor settling exist as usable inference-time computation? Measurand: ΔM vs K ∈ {0,1,2,3}, N=60; manipulation check: ‖h^{(k+1)} − h^{(k)}‖₂ decay curve (geometric decay = settling signature).
2. **Decision:** KILL / CONTINUE. KILL retires test-time recurrence as a mechanism family (and weakens any "iterative inference" framing of future loops); CONTINUE (ΔM > 0 with settling signature) queues a pre-registered block/layer/K sweep as a Phase-4 autonomous-computation primitive.
3. **Cheapest test:** 60 items × 4 K-values = 240 passes ≈ **0.003 T4-h**, against the *forced* matched-compute baseline (self-consistency at equal forward passes — Sprint 3 global rule 4). No new code beyond a forward hook; no weights touched.
4. **Mathematical license:** Banach fixed-point theorem (theorem — *if* F is a contraction with Lipschitz L < 1 on the visited set, iteration converges geometrically to a unique fixed point) + denoising-autoencoder theory (Bengio et al.: iterated application moves samples toward high-density regions) [both UNVERIFIED-WEB as cited] → prediction: ‖h^{(k+1)}−h^{(k)}‖₂ decays ≈ geometrically, and decision flips concentrate on near-boundary baseline items (margin < threshold), because settling moves representations across the boundary only where they start near it. **Breaking point:** if K = 1..3 yields ΔM ≤ 0 (McNemar p ≥ 0.05) while the matched-compute self-consistency baseline is ≥ 0 too, or if the displacement curve oscillates/diverges (no contraction on the visited set), attractor settling is not a usable mechanism here — kill it, no "more K" rescue (that would be sunk-cost continuation, mentor P2).
- **Unique support vs competitors:** only TTLRA predicts the geometric settling curve *coupled* with near-boundary flip concentration; self-consistency predicts flips ∝ sampling noise (no displacement signature); bridge rescue predicts flips ∝ bridge alignment (no K-dependence). Ablation: K=1 vs K=3 must show the dose-response; a flat K-curve with K=1 > 0 is just a one-step perturbation, not settling.
- **What kills it:** ΔM ≤ 0 at all K with verified non-divergent iteration; or flips uncorrelated with baseline margin (kills the settling story even if ΔM > 0 — then it's noise, PIVOT to noise-injection framing, not CONTINUE).

**Verdict: Underdetermined** (untested). Priced pilot: 0.003 T4-h.

---

## Candidate 3 — RHMPC: Receding-horizon planning with the frozen model as its own world model

### 1. Source field + prior
**Control theory beyond LQR: Model Predictive Control.** Rawlings, Mayne & Diehl, *Model Predictive Control: Theory, Computation, and Design* (2nd ed.) `[UNVERIFIED-WEB]`; Mayne et al. (2000) stability of receding-horizon control `[UNVERIFIED-WEB]`. MPC: at each step, solve a finite-horizon constrained trajectory-optimization problem using a dynamics model, execute the first action, replan. Unlike LQR (linear feedback to a fixed setpoint — our Activation-LQR prior), MPC handles nonlinear dynamics, constraints, and re-plans from the *current* state every step.

### 2. Translation (precise)
At the answer position, treat the frozen LLM as its own dynamics model: plan H tokens ahead over a beam of B candidate first-tokens (roll out H−1 continuation tokens per candidate with the frozen model), score each length-H trajectory with a **target-free** scorer (ρ-gate cross-view agreement, or ARP-style fingerprint — *composing* with queued verifiers, not duplicating them), execute the best trajectory's first token, then **replan** from the new state. Δθ = 0; the temporary state is the plan, discarded per token. **Mechanism:** receding-horizon correction of myopic greedy decoding — the model uses its own forward dynamics to look ahead, a qualitatively different computation from sampling (self-consistency) or steering.

### 3. Exclusion reasoning
- **Not killed:** nothing killed involves multi-step lookahead; killed items are single-shot injections.
- **Not queued / not prior-covered:** Activation-LQR is linear setpoint feedback (no planning, no horizon); Meta-Reasoner is bandits-over-strategies with trained components; D1 is adaptive *search* in output space (no dynamics model, no receding horizon, no replan step — the replan-from-current-state is MPC's load-bearing distinction); Self-Refine critiques text (no trajectory optimization); DEER exits early (no lookahead). The "model as its own world model + receding horizon" combination is absent from the §D1 map and the sprint queues.

### 4. Law #15 packet
1. **Precise question:** Does H-step receding-horizon planning change the chosen answer token beyond matched-compute sampling — i.e., does lookahead buy decisions that sampling at equal FLOPs does not? Measurand: ΔM (RHMPC vs greedy), plus first-token switch rate attributable to lookahead; N=60, H=2, B=4.
2. **Decision:** KILL / CONTINUE. KILL retires planning-as-mechanism (any future "planner" proposal must beat this null); CONTINUE queues a pre-registered (H, B, scorer) sweep as a Phase-4 primitive.
3. **Cheapest test:** 60 items × (1 + B×H) = 60 × 9 = 540 passes ≈ **0.0068 T4-h**, vs the forced matched-compute self-consistency baseline (Sprint 3 global rule 4) and the H=1 ablation (greedy + scorer = pure rerank, no lookahead).
4. **Mathematical license:** MPC stability/near-optimality theory (Mayne et al. 2000 — receding-horizon with terminal cost approximates infinite-horizon optimal control) [UNVERIFIED-WEB] → prediction (conjecture-level in this translation): gains concentrate on items where greedy top-1 ≠ planned best-first-token (the "myopia set"); switch-rate × win-rate on the myopia set > 0. **Breaking point:** if the H=1 ablation retains ≥ 80% of the H=2 gain, lookahead is decorative — the scorer is doing the work, not the planning (Sprint 3 global rule 2: adaptivity must not be decorative). If ΔM ≤ 0 vs matched-compute self-consistency, planning adds nothing over sampling — kill.
- **Unique support vs competitors:** only RHMPC predicts the myopia-set concentration *and* the H-ablation gradient (gain strictly increasing in H, vanishing at H=1); a pure-rerank story predicts the H=1 ablation keeps everything; self-consistency predicts no first-token-switch structure.
- **What kills it:** H=1 ablation retains the gain; or ΔM ≤ 0 vs matched self-consistency; or switches concentrate off the myopia set (then it's scorer noise, not planning).

**Verdict: Underdetermined** (untested). Priced pilot: 0.0068 T4-h.

---

## Candidate 4 — PWAR: Precision-weighted attention rescaling

### 1. Source field + prior
**Neuroscience predictive coding: precision-weighting of prediction errors.** Friston's predictive-coding / active-inference framework; Feldman & Friston (2010), "Attention, uncertainty, and free-energy" `[UNVERIFIED-WEB]`: attention *is* precision control — the brain up-weights (sharpens) prediction errors assigned high precision and down-weights noisy ones. Computational analogue: per-head, per-position modulation of attention sharpness by a local uncertainty estimate.

### 2. Translation (precise)
At test time, for each head h at the answer-relevant positions, compute a local uncertainty estimate u_h(x) (e.g., predictive entropy of that head's OV-projected output over a fixed probe vocabulary — target-free, no labels), and rescale attention logits: A_h ← softmax((QKᵀ/√d) · π_h), π_h = f(1/u_h) (sharpen where the head is confident, flatten where uncertain). Δθ = 0 [PROPOSITION]: only runtime attention *patterns* are modulated; no residual-stream content is added — this touches a surface no program intervention has ever touched. **Mechanism:** uncertainty-gated routing — the model's own confidence re-allocates its attention budget per item.

### 3. Exclusion reasoning
- **Not killed:** killed injections add *vectors* to the residual stream; PWAR adds nothing anywhere — it rescales routing weights. EXP082 exonerated logit-level foil suppression; this is neither target- nor foil-directed.
- **Not queued:** ARP (S3-1) *measures* attention engagement as a verifier signal but never modulates it; SAH modulates *intervention* α; nothing in the queue modulates attention patterns themselves. D3 searches (α, l*, p) placement of vector injections — different surface entirely.

### 4. Law #15 packet
1. **Precise question:** Does per-head precision rescaling of attention change 2-hop decisions beyond global temperature scaling — i.e., is there a *head-specific* precision signal, or is any gain just temperature? Measurand: ΔM for {baseline, global-τ grid (discriminant), PWAR}, N=60.
2. **Decision:** KILL / CONTINUE / PIVOT. KILL if PWAR ≤ global-τ (no head-specific signal — retire precision as a mechanism); PIVOT to "temperature scheduling" if global-τ alone wins (weaker, but honest, claim); CONTINUE if PWAR > global-τ with the predicted profile (below).
3. **Cheapest test:** 60 items × 6 conditions (baseline, 2 global-τ, 3 PWAR variants) = 360 passes ≈ **0.0045 T4-h**. Attention-hook only; no weights touched.
4. **Mathematical license:** predictive-coding precision theory (conjecture-level in translation — the Friston claim is about cortex, not transformers; the license here is *analogical*, flagged as the weakest license in this packet) → quantitative prediction: per-item gain correlates with pre-intervention *dispersion* of head entropies (bimodal head-confidence items gain most; uniform-entropy items gain ~0); PWAR − global-τ ΔM > 0. **Breaking point:** if the uniform-head ablation (same π for all heads) retains the full PWAR gain, the precision story is dead — it was temperature all along (PIVOT, not CONTINUE). If per-item gain is uncorrelated with entropy dispersion (Spearman p ≥ 0.1), the mechanism's signature is absent — KILL.
- **Unique support vs competitors:** only PWAR predicts the entropy-dispersion dose-response *and* head-specificity (lesion the top-precision heads → gain collapses; lesion random heads → gain survives); global temperature predicts neither.
- **What kills it:** PWAR ≤ global-τ at matched compute; or gain without the dispersion signature; or head-lesion indifference.

**Verdict: Underdetermined** (untested). Priced pilot: 0.0045 T4-h. (Honest flag: weakest mathematical license of the five — analogical, not theorem-backed. The pilot is cheap enough that the weak license is acceptable; a negative result is still informative because it retires the attention-modulation surface.)

---

## Candidate 5 — EOC: Edge-of-chaos per-item gain scheduling

### 1. Source field + prior
**Dynamical systems / theoretical neuroscience: computation at the edge of chaos.** Bertschinger & Natschläger (2004), "Real-time computation at the edge of chaos in recurrent neural networks" `[UNVERIFIED-WEB]`; Poole et al. (2016), "Exponential expressivity in deep neural networks through transient chaos" `[UNVERIFIED-WEB]`: information propagation and computational capacity are maximized near the critical boundary between ordered and chaotic dynamics (Lyapunov exponent λ ≈ 0).

### 2. Translation (precise)
The frozen LLM's layer map has an *intrinsic* global gain g (implemented as attention softmax temperature τ and/or residual-stream scale — runtime scalars, Δθ = 0). Per item, estimate distance-to-criticality with a cheap diagnostic: two nearby forward passes (x, x + ε) → local divergence rate λ̂(x) = log(‖Δh_L‖/‖Δh_0‖)/L (finite-time Lyapunov proxy). Then schedule g(x) to push λ̂ toward 0 (edge of chaos) for that item. **Mechanism:** per-item dynamical-regime scheduling — the model is kept at maximal expressivity per input, a qualitatively different intervention surface from content injection (no vector, no direction, no candidate pool).

### 3. Exclusion reasoning
- **Not killed:** no killed experiment touched global gain/temperature as a *scheduled, per-item, criticality-targeted* mechanism. (Global temperature as a *baseline* is standard; the per-item λ̂-diagnostic scheduling is the mechanism.)
- **Not queued:** SAH (S3-4) controls *intervention* α with hysteresis — different object (intervention strength vs intrinsic dynamics); D3 searches injection placement; TTLRA (Candidate 2) iterates a block rather than tuning gain. No queue item estimates Lyapunov exponents or targets criticality.

### 4. Law #15 packet
1. **Precise question:** Does per-item gain scheduling toward λ̂ ≈ 0 change 2-hop decisions beyond fixed-gain baselines — i.e., is distance-to-criticality a usable per-item control signal? Measurand: ΔM for {baseline g, fixed alternative g's, λ̂-scheduled g(x)}, N=60; manipulation check: λ̂ distribution before/after scheduling (must compress toward 0).
2. **Decision:** KILL / CONTINUE. KILL retires criticality-scheduling (and weakens "dynamical regime" talk program-wide); CONTINUE queues a pre-registered (diagnostic, gain-actuator) sweep.
3. **Cheapest test:** 60 items × (2 diagnostic passes + 3 gain settings) = 300 passes ≈ **0.0038 T4-h**. If the manipulation check fails (λ̂ doesn't move), stop — no further spend (worth-it gate).
4. **Mathematical license:** edge-of-chaos expressivity results (theorem-level in random nets: Poole et al. — depth scales for signal propagation are maximal at criticality) [UNVERIFIED-WEB] → prediction: gain concentrates on items with |λ̂_baseline| ≫ 0 (far-from-critical items); items already near λ̂ ≈ 0 gain ~0 (dose-response on |λ̂|). **Breaking point:** if scheduled-g ΔM ≤ fixed-best-g ΔM (the scheduler adds nothing over the best constant), or if gain is uncorrelated with |λ̂_baseline| (Spearman p ≥ 0.1), the criticality story is decorative — KILL. (Note: this is the sharpest breaking point in the packet — the dose-response on |λ̂| is non-negotiable.)
- **Unique support vs competitors:** only EOC predicts the |λ̂|-dose-response; fixed-temperature predicts uniform effects; PWAR (Candidate 4) predicts entropy-dispersion response — the two candidates are *discriminable* by which diagnostic predicts the gain, and a combined pilot can test both signatures on the same 60 items (design efficiency noted for the Research Lead).
- **What kills it:** scheduler ≤ best fixed gain; or no |λ̂| dose-response; or λ̂ unmeasurable/unstable across seeds (diagnostic invalid → KILL the candidate, not the theory).

**Verdict: Underdetermined** (untested). Priced pilot: 0.0038 T4-h.

---

## §6. Prior-art corrections from this pass

### 6a. Steering Vector Fields (Feb 2026) — verification: NOT achieved, stays UNVERIFIED
`browser.search` was unavailable (HTTP 401, upstream credential expired, 2026-09-24 ~11:12 IST), so no primary-source retrieval was possible. **SVF remains UNVERIFIED** per the adopted synthesis (SYNTHESIS_A_J_REV2 §D1: "primary source not retrieved… No content claim is made"). No arXiv identifier, author list, or venue exists anywhere in the repo records (full-repo grep, 2026-09-24).

### 6b. Record mischaracterization found: PARADIGM_AUDIT overclaims SVF status
`research/innovation/PARADIGM_AUDIT_2026-09-23.md` (A1) states SVF is "**verified-live** per the field sweep" and asserts content ("offline field + training-free KNN baseline beats static CAA"). This **contradicts** the adopted REV2 synthesis (§D1, §J — the document that passed the mentor's ADOPT gate, LOG-195), which explicitly marks SVF unverified with *no content claim*. The audit's "verified-live" label is therefore **unsupported by the retrieval record** and should not be cited downstream; the binding status is the REV2 one (UNVERIFIED, no content claim). Related: Sprint 1 New Idea 1's plan to "implement SVF's KNN steering" inherits this — its pre-registration must cite SVF as unverified inspiration, not as established prior art, until the V-record re-fetch rule is satisfied. (No signed artifact was edited; this correction is proposed, per repo law.)
**Verdict on the SVF content claim ("KNN baseline beats static CAA"): Underdetermined** — no retrievable primary source in-repo; the claim is not usable as a baseline or a foil until verified.

### 6c. No other mischaracterizations found in this pass
Spot-checked: the killed-list entries, the §D1 prior map, and the Sprint 2/3 queue boundaries are consistent with the ledger excerpts reviewed. (The known EXP082 verdict-vs-artifact conflict is the standing Research Lead's task, not re-litigated here.)

---

## §7. Queue-fit summary

| # | Candidate | Adjacent field | Killed? | Queued? | Verdict | Pilot cost (T4-h) |
|---|---|---|---|---|---|---|
| 1 | TNA — transient amplification (singular-vector interventions) | Non-normal dynamics / pseudospectra | No (semantic family only) | No | Underdetermined | 0.0045 (+$0 CPU) |
| 2 | TTLRA — test-time looped refinement / attractor settling | Attractor networks + test-time recurrence | No | No (C-B is α-iteration) | Underdetermined | 0.0030 |
| 3 | RHMPC — receding-horizon planning, model as world model | MPC (beyond LQR) | No | No (D1 has no dynamics/replan) | Underdetermined | 0.0068 |
| 4 | PWAR — precision-weighted attention rescaling | Predictive coding (precision) | No | No (new surface: attention patterns) | Underdetermined | 0.0045 |
| 5 | EOC — edge-of-chaos per-item gain scheduling | Edge-of-chaos / Lyapunov | No | No (SAH is intervention-α) | Underdetermined | 0.0038 |

**Total if all five pilots ran: ≈ 0.023 T4-h (~60 s of 2×T4) + $0 CPU — the entire packet costs about a minute of free-tier GPU.** Recommended order (cheapest falsification first): TNA Stage-A ($0 CPU Henrici screen) → EOC (sharpest breaking point) → TTLRA → PWAR → RHMPC. Candidates 4 and 5 can share one 60-item pilot (both predict per-item gain from different diagnostics — entropy dispersion vs |λ̂| — making them mutually discriminating on shared data).

**Standing caveats carried forward, not re-argued:** Δθ=0 throughout (all five are runtime-computation only); Law #7 target-free compliance holds for all five by construction (no labels at test time); Law #14 adversarial review + pre-registration required before any pilot runs; Sprint 3 global rules apply (decision endpoints only, forced matched-compute baselines, no decorative adaptivity).
