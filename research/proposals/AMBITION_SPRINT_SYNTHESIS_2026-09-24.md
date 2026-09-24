# AMBITION SPRINT — Coordinator Synthesis (LOG-250)

*2026-09-24. Coordinator: Standing Research Lead (sprint dispatch). Four specialists worked in parallel:*
- *Theory/mechanism design → `AMBITION_SPRINT_THEORY_2026-09-24.md` (5 candidates, M1–M5)*
- *Literature/adjacent-fields → `AMBITION_SPRINT_LITERATURE_2026-09-24.md` (5 candidates: TNA, TTLRA, PWAR, EOC, RHMPC)*
- *Experiment design → `AMBITION_SPRINT_EXPDESIGN_2026-09-24.md` (cheap-kill toolkit + 2 candidates X1, X2 + 5 class designs B.1–B.5)*
- *Adversarial review → `AMBITION_SPRINT_ADVERSARIAL_2026-09-24.md` (16-entry cull list, survival criteria, 3 live-bet stress tests, 12 Law #14 traps)*

*Standing facts for this sprint: θ_after = θ_before; $0, CPU design only, no weights touched, no signed artifacts edited; program-measured throughput 22 fwd/s @ Pythia-410m on 2×T4 → T4-h ≈ passes/79200; δ_min = 0.05; pilots KILL or HOLD, never license capability claims.*

## §1. Ranked candidates (7) — each with a complete Law #15 packet

Coordinator merges applied (structural duplicates across specialists): **M5 (LRI) + X1 (residual recurrence) + TTLRA (looped refinement)** merge into one *frozen-map iteration lane* (same kill diagnostic — the cheapest, X1's); **M2 (JPI) + TNA** merge into one *dynamical-amplifier lane* (TNA supplies the license and the $0 first stage; JPI supplies the per-instance decision-orthogonality gate). Merges are documented, not hidden — the specialist files retain the full separate packets.

---

### R1 — RCPA: Relational Cross-Position Amplification (the EXP077-null explainer) [M3, theory]

**Q1 (precise question):** EXP077 killed *within-position* static injection (ΔM=0, p=1.0 everywhere). K1's exoneration left the relational (t−f) direction as the live mechanism reading. Is the transferable signal **relational across positions** — does a per-instance cross-position vector at the output side move decisions where every within-position direction failed? Construction: per instance, r = h_L(ans_pos) − h_L(q_pos) (final-layer hidden states at answer vs. question position; positions only, **zero labels**). Inject h_L(ans) ← h_L(ans) + α·r̂ vs matched-norm random-direction control.

**Q2 (decision):** **KILL** the relational-readout family if r̂ moves decisions no more than random; **CONTINUE** to a powered pilot only if r̂ flips wrong→right at ≥ δ_min above control. Double duty: the same result *explains* EXP077's null as a theorem (below) — the LOG-219 "every death owes a candidate" payment for the static-geometry death that K2 (routing-bypass) does not pay.

**Q3 (cheapest test):** 2 forward passes/item (inject r̂, inject random) × 60 items × 1 α = **120 passes ≈ 0.0015 T4-h**. Endpoint: flip-rate(r̂) vs flip-rate(random), McNemar + δ_min=0.05. **Kill-first check ($0, same passes):** cos(r̂_i, r̂_j) across items — if r̂ is near-static, it is a re-skin and dies before the flip test.

**Q4 (math license):** [CONJECTURE → theorem sketch] If the decision-relevant feature is relational — the readout depends on comparisons across positions, with relational gradient ∇_rel — then any within-position static direction v satisfies ⟨v, ∇_rel⟩ ≈ 0 *to first order*, **predicting EXP077's ΔM=0/p=1.0 as a structural consequence, not bad luck.** Quantitative prediction: flip-rate(α·r̂) − flip-rate(random) ≥ δ_min=0.05, while the EXP077 within-position family stays at 0 — a *differential* prediction: one experiment, two opposite outcomes, both pre-registered. **Breaking point:** flip-rate(r̂) ≤ flip-rate(random) kills RCPA *and* returns EXP077's null to unexplained status (honest cost recorded).

**Unique support:** the *only* candidate that simultaneously predicts the old null (within-position must fail) and its own positive (cross-position relational must move) — no competitor makes this differential. **What kills it:** r̂ ≤ random on flips; or r̂ ≈ static across items.

**Not a re-skin:** killed family (a) injected *within-position, instance-independent* directions; RCPA injects a *per-instance cross-position relational* vector — the killed family is RCPA's *control arm*, and the theory predicts the control must fail. A re-skin would predict the old family works; RCPA predicts it can't. Vs killed (d) the bridge: bridge is normalize(E[target]−E[foil]) — *label*-informed; r = h(ans_pos) − h(q_pos) uses only *positions* — Law #7 clean. Vs killed (c) Procrustes: no cross-vocabulary mapping; within one model's activation space.

---

### R2 — X2: Newton-vs-gradient duel (second-order feedback family, flagship test) [exp-design]

**Q1:** Does a single Newton correction beat a single gradient correction (equal L2 norm, same site, label-free margin-proxy objective) on per-item margins? Construction: at the injection site, take one optimizer-style activation correction maximizing the label-free top-2 margin proxy — gradient step vs Newton step (−Ĥ⁻¹g, Hessian-vector product via central finite differences).

**Q2:** **KILL** the second-order feedback family if Newton ≡ GD; **CONTINUE** to a curvature-spectrum study only if Newton wins directionally. The duel is designed so that five Newton steps will never be cheaper than five GD steps — if the flagship loses here, there is no point pricing the family.

**Q3:** 120 passes — per item (N=24): 1 baseline + 1 GD step + 2 finite-difference probes + 1 Newton step = 5 passes; 24×5 = **120 ≈ 0.0015 T4-h**. The pass-count asymmetry (Newton costs 3 passes to GD's 1) is deliberate: the contrast is per-step *quality* at equal norm.

**Q4:** [THEOREM] For a quadratic objective, Newton converges in one step while GD needs O(κ(H)) steps (κ = Hessian condition number) → prediction: Newton's margin gain ≥ GD's, gap growing in measured condition number. [INTERPRETATION] If Newton ≤ GD, the curvature is either too small to matter (the κR² regime of the P1 bound — second order is provably negligible) or too noisy to exploit — both kill the family's premise, and the probes themselves estimate κ to say *which*. **Breaking point:** one-sided Wilcoxon (Newton − GD) on margins, p ≤ 0.05 for CONTINUE; median(ΔM_Newton − ΔM_GD) ≤ 0 with two-sided p ≥ 0.10 → **KILL the second-order family**, reporting measured κ as the useful negative result.

**Unique support:** converts the program's standing curvature bound (δ ≤ κR², LOG-248) from a defensive weapon into an offensive one — either Newton wins and the bound's regime is shown exploitable, or Newton loses and the bound is empirically confirmed as the ceiling. **What kills it:** Newton ≤ GD; or Newton ≤ random-direction step (then the win is step-noise, not curvature).

**Not a re-skin:** no static direction (both steps are per-instance computed); no labels (margin-proxy from the model's own activations); the killed (f) oracle-loop family selected among candidates — here the correction is derived, not chosen.

---

### R3 — Dynamical-amplifier lane: TNA + JPI merged (singular-vector-aligned injection) [literature + theory]

**Q1:** K3 Phase-0 proved a ×1.8 downstream amplification *exists* as mechanism signal. Is it *exploitable by design* — do perturbations aligned with the leading right singular vectors of the downstream Jacobian product produce strictly larger decision-flip rates per unit norm than semantic-contrast or random directions? And per instance, does the analytically computed max-gain direction carry decision-relevant content (not just noise amplification)?

**Q2:** **KILL** the dynamical-amplifier family if gain is rank-indifferent (flat across singular ranks) or the max-gain direction is decision-orthogonal; **CONTINUE** only if singular-rank orders the gain AND the direction beats random control on flips.

**Q3 (two-stage, cheapest first):** Stage A (**$0 CPU, weight-only**): Henrici non-normality index per layer, He = (‖J_l‖_F² − Σ|λ_i|²)^{1/2}/‖J_l‖_F — if every layer is near-normal (He ≈ 0), the license evaporates before GPU. Stage B (live pilot): 60 items × {top-singular-vector δ, random-unit δ, semantic B_agg δ} × 2 norms = **360 passes ≈ 0.0045 T4-h**. JPI's decision-orthogonality gate (ĉ = mean|⟨v̂₁, n̂⟩|, n̂ = label-free decision normal) is measured on the same passes: ĉ < 0.1 → **KILL before any flip claim** — gain without decision relevance is noise amplification.

**Q4:** [THEOREM] (Kreiss Matrix Theorem) For non-normal A, sup_k ‖A^k‖ ≥ ρ_ε(A)/ε — transient growth ≫ 1 is possible with all eigenvalues stable; eigenvalue analysis cannot see it. [THEOREM] (SVD/power iteration) v̂₁ maximizes ‖J·u‖ — downstream logit displacement σ₁·ε is *maximal*; no other unit direction moves the logits more. Prediction: flip-rate-per-norm(top-singular) ≥ 1.5× flip-rate-per-norm(random) at matched ‖δ‖₂ (bar set below the observed ×1.8 to be fair to the phenomenon); gain rank-orders with singular rank. **Breaking point:** flat gain across singular ranks (p ≥ 0.1 for rank trend) with ΔM_top-singular ≤ ΔM_random; or Stage-A He ≈ 0; or ĉ < 0.1 (decision-orthogonal gain); or flat singular spectrum σ₁/σ₂ ≈ 1 (no distinguished direction exists).

**Unique support:** the first mathematical home for the observed ×1.8 downstream gain (S3-8) — only TNA predicts *which* perturbations amplify (singular-rank ordering); the linear-gain story predicts rank-indifference; routing predicts α-dependence but not singular-rank dependence. **What kills it:** rank-indifferent gain; orthogonality; near-normal layers.

**Not a re-skin:** killed family (a) is *semantic* static geometry (contrast/cone/offset/Procrustes, ΔM = 0); no killed experiment ever measured or injected along singular vectors of the layer-transition Jacobian. G1 killed the *QK-subspace* weight-energy story — a different object from the *dynamical* amplification of the full nonlinear map. Vs killed (d) the bridge: zero label information — VJPs/SVDs of the model's own logits/Jacobian; Law #7 clean by construction. JPI's explicit note: EXP077's fixed-v-at-L20 family is literally a *degenerate special case* JPI generalizes away from — per-instance, computed, no fixed direction.

---

### R4 — EOC: Edge-of-chaos per-item gain scheduling [literature]

**Q1:** Does per-item gain scheduling toward λ̂ ≈ 0 change 2-hop decisions beyond fixed-gain baselines — is distance-to-criticality a usable per-item control signal? Construction: per item, estimate finite-time Lyapunov proxy λ̂(x) = log(‖Δh_L‖/‖Δh_0‖)/L from two nearby forward passes (x, x+ε); schedule the frozen model's intrinsic global gain g(x) (attention softmax temperature τ and/or residual-stream scale — runtime scalars, Δθ = 0) to push λ̂ toward 0.

**Q2:** **KILL** criticality-scheduling if the scheduler ≤ best fixed gain or gain shows no |λ̂| dose-response; **CONTINUE** to a pre-registered (diagnostic, gain-actuator) sweep only on the dose-response signature.

**Q3:** 60 items × (2 diagnostic passes + 3 gain settings) = **300 passes ≈ 0.0038 T4-h**. Worth-it gate inside the pilot: if the manipulation check fails (λ̂ doesn't move), stop — no further spend.

**Q4:** [THEOREM-level in random nets] (Poole et al. 2016 [UNVERIFIED-WEB]) — signal-propagation depth scales are maximal at criticality. Prediction: gain concentrates on items with |λ̂_baseline| ≫ 0 (far-from-critical items); items already near λ̂ ≈ 0 gain ~0 — the **dose-response on |λ̂| is non-negotiable**. **Breaking point (sharpest in the sprint):** scheduled-g ΔM ≤ fixed-best-g ΔM, or gain uncorrelated with |λ̂_baseline| (Spearman p ≥ 0.1) → the criticality story is decorative → KILL. Diagnostic-invalid branch: λ̂ unmeasurable/unstable across seeds → KILL the candidate, not the theory.

**Unique support:** only EOC predicts the |λ̂|-dose-response; fixed-temperature predicts uniform effects; PWAR predicts entropy-dispersion response — the two are *discriminable by which diagnostic predicts the gain*, and a combined pilot can test both signatures on the same 60 items (design efficiency). **What kills it:** scheduler ≤ best fixed gain; no dose-response; unstable λ̂.

**Not a re-skin:** no killed experiment touched global gain as a *scheduled, per-item, criticality-targeted* mechanism (global temperature as a static baseline is standard; the per-item λ̂-diagnostic scheduling is the mechanism). No vector added, no direction, no candidate pool. Distinct from S3-4 (SAH), which controls *intervention* α with hysteresis — different object (intervention strength vs intrinsic dynamics).

---

### R5 — EAR: Ephemeral Attention Registers (within-pass, circuit-addressed scratch memory) [theory, M4]

**Q1:** Do *named, frozen* attention heads implement causally verifiable **write** (content→scratch position) and **read** (scratch→answer position) operations, composable into a within-pass scratch memory — with ablation-verified fidelity, not prompt-engineering hope? Construction: append S scratch (filler) tokens; patch an instance-computed vector w into scratch position s's residual stream (write); the model's own frozen heads move content to the answer position (read). Identify write/read heads causally: score heads by attention mass on write/read patterns, verify by ablation.

**Q2:** **KILL** the circuit-addressed-memory family if no head beats the random-head write control (attention too diffuse) or ablation doesn't matter; **CONTINUE** only if identified write→read composition beats both controls by ≥ δ_min on a 2-hop task.

**Q3 (kill-first):** head scan — 60 passes scoring write-pattern attention mass per head ≈ **0.0008 T4-h**. Kill rule: best head's write fidelity ≤ random-head control → **KILL** (no addressing circuit exists). Composition test (only if scan passes): 4 arms × 60 items = 240 passes ≈ 0.003 T4-h. **Total pilot ≈ 0.004 T4-h.**

**Q4:** [CONJECTURE] (attention-as-addressing) A head with attention entropy H < h̄ concentrated on the write pattern implements a noisy write with fidelity f_write ≥ 1−ε(H); read fidelity similarly — both *measured* in the scan, not assumed. [PROPOSITION] (composition) k-hop scratch fidelity ≥ Π_i f_i under independent-hop errors — predicts the *degradation curve* with hops, a quantitative signature (fidelity must fall multiplicatively, not cliff). **Breaking point:** no head above random control; or ablation of read heads changes nothing (the "memory" was decorative); or fidelity doesn't follow the multiplicative curve (composition false even if single-hop works).

**Unique support:** *named circuits* (head indices), *ablation-verified* addressing, within a *single* forward pass, using the residual stream itself as memory. H2/C2 ELM is **cross-pass** with model-generated keys and an **added** buffer across T passes — EAR is within-pass, no added buffer, addressing by frozen heads not generated keys. The *ablation* result is what CoT/prompting cannot produce. **What kills it:** diffuse attention; ablation-indifference; non-multiplicative degradation.

**Not a re-skin:** vs killed (a) static injection — nothing static is added; content is *instance-computed*, addressing circuits *identified*, ablation arms are the falsifier. Vs killed (d)/(e): no labeled direction, no persistent shift — writes are per-instance transient activations, purged after the pass (Δθ=0, Δactivation=0 post-pass). Vs prompting/CoT: token-space scratch relies on learned behavior; EAR's scratch is activation-space with circuit-level verification.

---

### R6 — Frozen-map iteration lane (X1 + M5/LRI + TTLRA merged) [exp-design + theory + literature]

**Q1:** What happens if the frozen stack is treated as recurrent — iterate a frozen map h_{t+1} = F(h_t) at inference time? Does iteration change decisions beyond matched-compute baselines, or does the mechanism kill itself by its own math? Three merged constructions: **X1** x_{k+1} = E + α·r(x_k) (α label-free scalar, α=0.1 pilot); **M5/LRI** h_{t+1} = B(h_t) for a frozen layer block B; **TTLRA** K-fold iteration of block [l1,l2] as attractor settling. Merge rationale: same kill diagnostic (contraction/Lipschitz), same honest prior (divergence), same decision rule — run the cheapest; variants that survive the diagnostic earn their own packets.

**Q2:** **KILL** fast — the honest prior is that residual+LayerNorm maps are *expansive*, so the kill-first diagnostic is designed to execute in ≤400 passes; **CONTINUE** only on the surprise outcome (measured contraction + monotone margin gain), which would be a genuine discovery about transformer geometry regardless of capability. Decision flips without monotone gain = instability → PIVOT to instability characterization, never CONTINUE.

**Q3 (cheapest first):** X1 pilot — 60 passes (30 items × baseline + 1 recurrence pass, cache reuse) ≈ **0.0008 T4-h**, the cheapest pilot in the program; α chosen by a $0 CPU contraction diagnostic on archived residuals. M5's block-Lipschitz diagnostic: 200 pairs × 2 passes = 400 ≈ 0.005 T4-h. TTLRA's K-sweep with settling-curve check: 240 passes ≈ 0.003 T4-h (only if the contraction diagnostic surprises). **Sequence: contraction diagnostic ($0 CPU) → X1 60-pass pilot → survivors only.**

**Q4:** [THEOREM] (Banach) If the iterated map is L-Lipschitz with L < 1 on the visited set, unique attracting fixed point, convergence at rate L^t — the diagnostic measures L; the theorem does the rest. [PROPOSITION] If L ≥ 1, divergence or 2-cycles — prediction: unbounded displacement or oscillation → kills the "stable capability gain" claim. **Breaking point (the only surviving branch):** monotone margin gain with ‖x_{k+1} − x_k‖ strictly decreasing — pre-registered as one-sided Wilcoxon p ≤ 0.05 AND median displacement contraction ratio < 0.9. Every other outcome is KILL or PIVOT-to-instability. TTLRA adds the settling signature: ‖h^{(k+1)}−h^{(k)}‖₂ decays geometrically AND flips concentrate on near-boundary items; flips uncorrelated with baseline margin → it's noise → PIVOT, not CONTINUE.

**Unique support:** a *structural* claim about the compute graph (recurrence vs feedforward) — no competitor touches graph structure. CLLC does closed-loop *control of injections*; this changes the *graph* and injects nothing. X1's surviving branch (monotone gain + contraction) is a signature no killed family can fake (static injection can't produce step-2 ≠ step-1; tilt can't produce contraction). **What kills it:** L̂ ≥ 1 (the expected outcome — a kill is the plan, not a disappointment); flat step-2 (McNemar b=c=0 AND Wilcoxon p ≥ 0.10 AND displacement inside the CPU-predicted contraction envelope); oscillating/diverging displacement.

**Not a re-skin:** vs killed (a) — nothing added to the residual stream (LRI/TTLRA) or only a scaled copy of the model's own residual (X1); no direction, no α-grid search over semantic space, no injection site in the killed sense. Vs killed (f) EXP070 — no candidates, no oracle, no labels; the loop is the block itself. Vs killed (e) tilt — no readout manipulation; the experiment lives in mid-network iteration dynamics.

---

### R7 — OSAI: Output-Side Attractor Iteration (self-consistent belief fixed points) [theory, M1]

**Q1:** Does the frozen model's *own* output-side dynamics possess attracting fixed points — **self-consistent belief states** — whose argmax decisions differ from (and beat) the one-pass readout, with zero labels and zero injected directions? Construction: h₀ = final-layer hidden state at answer position; mean-field self-consistency map Φ(h) = E_{t ∼ softmax(W_U·LN(h)/τ)}[H(x ⊕ t)] (top-8 truncated, label-free); iterate h_{t+1} = (1−λ)h_t + λΦ(h_t). A fixed point h* = Φ(h*) is a self-consistent belief state.

**Q2:** **KILL** the attractor-dynamics family if the map is non-contractive (no attractor) or fixed points are decision-neutral; **CONTINUE** only if attractors exist AND fixed-point decisions beat one-pass by ≥ δ_min on a pilot.

**Q3 (most expensive in the sprint — run last):** kill-first contraction diagnostic: finite-difference Lipschitz estimate L̂ of Φ on 40 items × 20 probe pairs × 9 passes (1 + top-8) = 7,200 passes ≈ **0.091 T4-h**. Kill rule: L̂ ≥ 1 → **KILL**. Capability phase (only if L̂ < 1): iterate to convergence (≤15 iters × 9 passes) on 60 items ≈ 0.102 T4-h. **Total pilot ≤ 0.20 T4-h.**

**Q4:** [THEOREM] (Banach) L < 1 ⇒ unique fixed point, convergence at rate L^t. [CONJECTURE → quantitative] If decision errors concentrate near the boundary (small top1−top2 gap), the self-consistent fixed point resolves boundary items toward the model's globally consistent belief: accuracy(h*) − accuracy(h₀) ≥ δ_min on the low-gap stratum, ~0 elsewhere. **Breaking point:** L̂ ≥ 1 (divergence/oscillation — the honest prior); or fixed-point accuracy ≤ baseline.

**Unique support:** convergence to a *decision-better fixed point generated by the model's own dynamics* — no static direction (vs killed (a)), no candidate pool or oracle (vs EXP070), no token-space refinement (vs Self-Refine — greedy token edits, not an activation-space fixed point with a contraction certificate). **What kills it:** L̂ ≥ 1; fixed-point accuracy ≤ baseline.

**Not a re-skin:** vs killed (a) — no fixed direction exists anywhere; the trajectory is per-instance, generated by Φ, at the output side not L20-concept-side. Vs killed (f) — no labels, no oracle, no candidate pool; the "selector" is the Banach fixed point. Vs killed (e) — no persistent additive shift; h_{t+1}−h_t is state-dependent and vanishes at the fixed point by construction.

**Honest limitation (pre-registered):** the top-8 truncation error of Φ is *not* bounded in the theory note — Law #14 must demand the truncation-error analysis before SIGN. This is the high-variance bet: most expensive, weakest near-term value; run only after R1–R6 have reported.

---

## §2. HELD (not culled, not queued — parked with the parking reason)

- **PWAR — precision-weighted attention rescaling** (predictive-coding precision; 0.0045 T4-h). *Parked because:* weakest mathematical license in the sprint (analogical — Friston's precision claim is about cortex, not transformers). Not killed: it touches a surface no program intervention has touched (attention patterns, not residual content) and its breaking point is sharp (uniform-head ablation keeps the gain → it was temperature all along). **Parking rule:** runs only piggybacked on EOC's pilot (the literature specialist showed the two are mutually discriminating on shared 60-item data: entropy-dispersion vs |λ̂| dose-response). A standalone PWAR pilot is not licensed.
- **RHMPC — receding-horizon MPC with the frozen model as its own world model** (0.0068 T4-h, most expensive pilot in the literature set). *Parked because:* the H=1 ablation is likely to retain the gain (the scorer does the work, not the planning — the literature specialist's own breaking point), which would make it an expensive rerank experiment. Not killed: the "model as its own world model + receding horizon" combination is genuinely absent from the §D1 map and the queue. **Parking rule:** runs only after R1–R6 report; if any cheaper lane survives, RHMPC's planning question is re-asked against the survivor's mechanism, not from scratch.

## §3. CULL LIST — rejected ideas with one-line reasons (first-class deliverable)

*Adversarial reviewer's 16 (citations = recorded verdicts) + literature specialist's 6 drafted-and-cut (queue/graveyard hygiene). Deduplicated where they coincide.*

**A. Re-skins of killed families (dead causal channel — new sourcing doesn't change the operator):**
1. Wider static search (more cone angles, finer α grids, offsets, layers, multi-vector sums, per-head variants) → KILLED by EXP077: 0.0pp across cones/offsets/grids, ΔM=0, p=1.0 throughout.
2. Procrustes 2.0 (better regularization, more anchors) → KILLED and retracted: rank-2 unembedding fit on full-rank directions is mathematically unsound; ledger claims contradicted primary artifacts.
3. QK-subspace targeting → KILLED by G1: exact inversion of the premise (failed direction QK-visible at Ē_QK=0.390; working bridge mid-null at 0.356).
4. Tilt 2.0 (persistent tilt across layers/items) → KILLED by K1 (0/180 at bar) and EXP082 (foil-suppression 0/60) — dead in both directions.
5. Self-generated task vectors (novel sourcing, same operator) → same operator as killed static injection; new sourcing doesn't change the operator class — kill-license violation (mentor P3).
6. Autonomous unsupervised steering (cluster centroids as directions) → EXP077's verdict attaches to the *injection family*, not the derivation method; a cleverer derivation doesn't survive a dead causal channel.
7. Scale the static program to 7B → Sprint-3 graveyard: 7B scaling stays dead; re-skin at a size the free tier cannot serve.

**B. Label-leakage / Law #7 violations:**
8. The bridge, but smarter (whitened/denoised normalize(E[target]−E[foil]) as mechanism) → LOG-204 demotion: label-informed rescue control, not a mechanism; rebranding smuggles leakage.
9. Oracle loops (feed correct answer's embedding back) → KILLED by EXP070 (+0pp) and label leakage: any "gain" is the label, not the loop.
10. Test-set-fitted directions (fit on eval labels, report rescue on same items) → Law #7: no held-out, no claim.

**C. Frozen-backbone / program-identity violations:**
11. Fine-tune a little (LoRA/adapters) → violates Law #6 and θ_after = θ_before; a different research program, not SCBI.
12. Paid-API verifier in the loop → $0 standing law: no paid compute, no exceptions; also external-label dependency.
13. Program-synthesis verifier (capability lives in the external executor) → on the 2-hop testbed collapses to CoT-with-a-checker; violates the mechanism-level (P1) framing.

**D. No falsifying test / untestable:**
14. Curvature from the ray (bound off-ray curvature from the S3-9 1-D α grid) → KILLED by the LOG-248 impossibility result: adversarial bump construction proves exact ray-match to all orders with arbitrarily large off-ray δ — a theorem, not a hunch.

**E. Novelty/claim violations:**
15. Inter-instance latent exchange → explicitly retracted in the REV synthesis; novelty inflation beyond N1.
16. CoT/Self-Refine wrapper = new capability → silent level crossing (L1≠L2≠L3); frontier scoreboard already lists these as *competitor* systems; SCBI has zero capability entries.
17. Gradient steering as autonomous discovery (PPLM-style, pitched as "discovery") → LOG-247: externally specified direction = inference-time activation control, never autonomous cognition.

**F. Process violations:**
18. Re-run K2/EXP080/081/K3 with tweaked bars, no new number → Law #4: design changes take new experiment numbers; re-running signed batteries with moved bars is significance-shopping.

**G. Queue duplicates / overlaps (not killed — merged or returned, recorded so the graveyard stays clean):**
19. SAE/transcoder feature steering → already queued (Sprint 1 New Idea 4); not duplicated.
20. Hopfield/associative trace memory → overlaps S3-2 LOM (library-of-operators retrieval) in mechanism spirit.
21. TTT-style activation gradients (one-VJP test-time directions) → already queued as D2 (demoted); occupied by the ∇-Reasoner prior.
22. Gated working-memory maintenance (re-inject maintained vector every layer) → overlaps M1 multi-layer bridge cascade in operator structure.

*Cull-list size: 22 distinct entries (16 adversarial + 6 literature). None may enter the queue without a new falsifying test that the cited kill does not already cover.*

---

## §4. Guards carried out of the sprint (adversarial stress-tests — CEO decisions required)

These are not candidate results; they are defects in the *live queue* the adversarial reviewer found. Each needs a CEO/Lead decision, not more theory.

**G1 — K2 row-4 strand (most dangerous unguarded trap).** If K2 returns "both restricted arms flat with (c) passing G5," the verdict table prices it as Inconclusive, but its consequence ("K2's question is unaskable in this form") names **no licensed next instrument and no decision rule**. The generic remedy (powered re-registration at N≥100) would re-ask a question whose application premise (L3) broke — more N cannot fix a broken premise. In one row, the P2 pivot can't fire *and* the upstream hunt can't be licensed: the program's two licensed futures both die with no pre-registered exit. **Recommended guard:** pre-register now, before K2 executes, that row 4 → the position-masking attribution approach is **stood down, not re-registered** (Law #8: the negative result is retained as the finding), and the program re-scopes to whole-trajectory instruments that never ask the routing question (CLLC-style closed-loop control). Consolation that *is* guarded: Sprint-3 verifiers retain the bridge as a causal-but-unlocalizable positive class — their $0 Stage-0 gates don't need K2's attribution answer.

**G2 — Curvature diagnostic has no pre-registered interpretation rule.** The 150-pass diagnostic (queued behind K2) has no κ̂ vacuity/abort threshold, no covering protocol over schedule space, no Law #14 pre-registration of the diagnostic itself — yet it sits in the queue "priced" as if it will instantiate P1's bound. The LOG-248 caveats are written but not rule-bound: if κ̂ comes back huge the bound is vacuous; if measured at the nominal point it's [CONJECTURE]-grade (LOG-248's adversarial bump); if S3-9 returns nonlinear the diagnostic answers a dead question. **Recommended guard:** no GPU until the diagnostic has its own pre-registered interpretation rule (abort/vacuity thresholds, covering protocol, S3-9-near-linearity precondition), reviewed under Law #14. Until then it is a queued *proposal*, not a queued *measurement*.

**G3 — CLLC's efficiency cell is undecidable as written.** The (C)>(B2)-but-(C)<(D) cell ("CONTINUE as efficiency result *only if* (C) uses strictly less information/compute than (D)") has no operationalized definition of "strictly less" — a between-the-arms outcome would be decided by reviewer discretion. **Recommended guard:** before EXP-CLLC-01 is signed, operationalize "strictly less" (e.g., total forward-pass-equivalents including JVP costs, counted by the executor) and pre-register the threshold. (Also: the faster kill-shot needs no GPU — if Jacobian-vector products on this architecture cost ≪ one forward pass, the Jacobian-free economy is vacuous and the narrowed novelty collapses to N0-redundant without running the battery.)

**G4 — Record mischaracterization proposed for correction (user sign-off required).** The literature specialist found that `research/innovation/PARADIGM_AUDIT_2026-09-23.md` (A1) labels Steering Vector Fields "**verified-live** per the field sweep" and asserts content ("offline field + training-free KNN baseline beats static CAA") — this **contradicts** the adopted REV2 synthesis (§D1/§J, mentor ADOPT gate LOG-195), which marks SVF **UNVERIFIED** with *no content claim*. Full-repo grep confirms no arXiv ID/author/venue for SVF exists anywhere in the records. **Proposed correction:** the audit's "verified-live" label is unsupported by the retrieval record; binding status = REV2 (UNVERIFIED). Related: Sprint 1 New Idea 1's "implement SVF's KNN steering" must cite SVF as unverified inspiration until the V-record re-fetch rule is satisfied. **Not applied** — corrections to signed artifacts are proposed, never applied, until the user signs off (per repo law). The SVF "KNN baseline beats static CAA" content claim is **Underdetermined** and unusable as a baseline/foil until the primary source is retrieved.

---

## §5. Coordinator's sequencing and promotion recommendation

**Recommended GPU execution order (all behind K2 and the user's Kaggle runs; all require Law #14 SIGN + signed pre-registration first — nothing here is licensed to execute):**
1. **R1 RCPA** (0.0015 T4-h) → 2. **R2 Newton-duel** (0.0015 T4-h) → 3. **R3 Stage-A $0 CPU Henrici screen; Stage-B pilot** (0.0045 T4-h) → 4. **R4 EOC** (0.0038 T4-h, with PWAR piggybacked) → 5. **R5 EAR** (0.004 T4-h) → 6. **R6 X1 pilot** (0.0008 T4-h; M5/TTLRA only on surprise) → 7. **R7 OSAI** (0.091 T4-h; only if the sprint wants the high-variance bet).

**Promotion recommendation: R1 RCPA → QUEUED.** Reasons: (i) cheapest tier with the sharpest kill (flip-rate vs random, McNemar + δ_min); (ii) strongest license in the set — the only candidate that *predicts an existing null as a theorem* (EXP077's ΔM=0 becomes a structural consequence, not bad luck), paying the LOG-219 "every death owes a candidate" debt; (iii) label-free by construction (positions only — passes the LOG-204 Law #7 antibody that killed the bridge); (iv) output-side, where the only positive transfer signal lives; (v) built-in anti-re-skin check (cos(r̂_i,r̂_j) static-ness check on the same passes). If killed, it strengthens the boundary at 0.0015 T4-h; if it survives, it opens the relational-readout lane — a genuinely new mechanism class for the program. QUEUED means promotable to Law #14 review and signed pre-registration — not licensed to execute.

**Honest posture:** all seven default to novelty tier N1 (Known Combination) until a kill criterion fires or fails — the changed burden of proof applies (any positive a 2026 occupant predicts at matched compute is replication). All seven are currently **Underdetermined** (untested); the sprint produced *priced, falsifiable questions*, not answers. Total kill-first diagnostics for R1–R6: ≈ 0.018 T4-h (~1.5 min on 2×T4). The entire ranked slate, killed-first, costs less than one K2 run.

*— Sprint coordinator, LOG-250, 2026-09-24. $0 spent, CPU only, no weights touched, no signed artifacts edited.*
