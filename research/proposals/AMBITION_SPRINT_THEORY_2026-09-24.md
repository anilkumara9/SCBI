# AMBITION SPRINT — Theory/Mechanism-Design Candidates (LOG-250)

*Theory specialist deliverable, 2026-09-24. CPU design only, $0, no GPU, no weights touched, no signed artifact modified.*
*Epistemic layer (mentor canonical): [FACT] / [INFERENCE] / [HYPOTHESIS] / [SPECULATION].*
*Verdict vocabulary: Supported / Not supported / Inconclusive / Underdetermined / Refuted only. δ_min = 0.05 (binding). Endpoints are decision changes (accuracy flips); margin endpoints invalidated (A9).*
*Compute figure [FACT, Sprint-2]: ~22 forward passes/s on pythia-410m (2×T4). T4-h = passes / 22 / 3600.*

## 0. Standing context (not relitigated)

- **Frozen-backbone law:** θ_after = θ_before. Inference-time computation only.
- **Killed (never re-skinned):** (a) static direction injection — 0.0pp incl. cones/offsets/radial grids, Pythia-410m/L20 (EXP077); (b) QK-null-space mechanism — refuted by G1; (c) Procrustes cross-vocab claims — retracted, raw cosine ~0.7 with zero causal transfer (EXP065/066); (d) the bridge normalize(E[target]−E[foil]) — label-informed rescue, demoted, Law #7; (e) persistent readout tilt — not supported, 0/180 at bar (K1); (f) adaptive-loop oracle ceiling — +0pp static (EXP070).
- **Live signals:** output-side is where the only positive lives (EXP077 bridge rescue +10pp, p=0.03125 — label-informed); K3 Phase-0 downstream transformation gain ×1.8 as pure mechanism signal (g_P=1.922505, g_D=1.061783); LOG-248 theorem — feedback-vs-open-loop gap δ ≤ 2ε (sup-norm affine error), δ ≤ κR² (curvature): feedback adds value only via nonlinearity correction, per-instance adaptation, or model-error replanning; K1 exoneration leaves the **relational (t−f) direction** as the live mechanism reading.
- **Queue (not duplicated):** K2 routing-bypass, CLLC Jacobian-free closed-loop control, Sprint-3 pilots (S3-1…S3-9 per CANDIDATE_BACKLOG.md), K3 Phase-1 causal rescue screen, EXP080/081, curvature diagnostic.
- **H-map:** H1 dynamic representation control (C1 CLLC, E7 DPRS), H2 ephemeral computational workspace (C2 ELM — cross-pass addressable latent RAM, model-generated keys, added buffer), H3 test-time program synthesis (C3 TTPS), H4 adaptive cognitive routing (C4 ASR), H5 latent cooperation (C5 LCMIC).

## Design rule applied to every candidate below

Each candidate (i) answers a question no live experiment answers, (ii) carries a **kill-first diagnostic** — a cheap measurement that can execute the kill *before* any capability test, so a dead idea dies under $0.10 T4-h, (iii) states a quantitative breaking point, not a vibe, and (iv) names the killed family it is most likely to be confused with and the structural difference.

---

## M1 — OSAI: Output-Side Attractor Iteration (self-consistent belief fixed points)

### 1. Precise question
Does the frozen model's *own* output-side dynamics possess attracting fixed points — **self-consistent belief states** — whose argmax decisions differ from (and beat) the one-pass readout, with zero labels and zero injected directions?

**Construction [DEFINITION].** Let h₀ be the final-layer hidden state at the answer position for instance x. Define the mean-field self-consistency map
Φ(h) = E_{t ∼ softmax(W_U·LN(h)/τ)} [ H(x ⊕ t) ],
where H(x⊕t) is the final hidden state when context x is extended by token t (expectation truncated to top-k=8, label-free). Iterate h_{t+1} = (1−λ)h_t + λΦ(h_t), λ∈(0,1]. A fixed point h* = Φ(h*) is a **self-consistent belief state**: the model's expected next state equals its current state.

### 2. Decision it changes
**KILL** the attractor-dynamics family if the map is non-contractive (no attractor exists) or fixed points are decision-neutral; **CONTINUE** to a pre-registered capability experiment only if attractors exist AND fixed-point decisions beat one-pass decisions by ≥ δ_min on a pilot.

### 3. Cheapest falsifying test
- **Kill-first diagnostic (contraction):** finite-difference Lipschitz estimate L̂ of Φ on 40 items × 20 probe pairs; each Φ eval = 9 passes (1 + top-8). 40×20×9 = 7,200 passes ≈ **0.091 T4-h**. Kill rule: L̂ ≥ 1 → **KILL** (no attractor; idea dead).
- **Capability phase (only if L̂ < 1):** iterate to convergence (≤15 iters × 9 passes) on 60 items; endpoint = accuracy(h*) vs accuracy(h₀), McNemar + δ_min=0.05. 8,100 passes ≈ **0.102 T4-h**.
- **Total pilot ≤ 0.20 T4-h; kill achievable at 0.091 T4-h.**

### 4. Mathematical license
- **[THEOREM] (Banach).** If Φ is L-Lipschitz with L < 1 in the whitened norm on a basin, iterates converge to a unique fixed point at rate L^t. The diagnostic measures exactly this L.
- **[CONJECTURE → quantitative prediction].** If decision errors concentrate near the boundary (uncertain items, small one-pass top1−top2 gap), the self-consistent fixed point resolves boundary items toward the model's globally consistent belief; predicted: accuracy(h*) − accuracy(h₀) ≥ δ_min on the low-gap stratum, ~0 elsewhere.
- **Breaking point:** L̂ ≥ 1 kills the existence claim; accuracy(h*) ≤ accuracy(h₀) + δ_min kills the capability claim. Both are measured, not argued.

### 5. Unique support / what kills it
- **Uniquely supports over competitors:** convergence to a *decision-better fixed point generated by the model's own dynamics* — no static direction (vs killed (a)), no candidate pool or oracle (vs EXP070/H-001), no token-space refinement loop (vs Self-Refine prior art, which predicts greedy token edits, not an activation-space fixed point with a contraction certificate). H-002's relationality is about *input* counterfactuals; OSAI is about *belief-state* dynamics. S3-4 (SAH) controls α on injections; OSAI injects nothing.
- **Kills it:** L̂ ≥ 1 (divergence/oscillation — the honest prior, since residual+LayerNorm blocks are usually expansive); or fixed-point accuracy ≤ baseline.

### 6. Not a re-skin
- Vs killed **(a) static injection**: no fixed direction exists anywhere in OSAI — the trajectory is generated per-instance by Φ; injection site is output-side, not L20-concept-side.
- Vs killed **(f) EXP070 oracle ceiling**: no labels, no oracle, no candidate pool — the "selector" is the Banach fixed point itself.
- Vs killed **(e) readout tilt**: no persistent additive shift; the update h_{t+1}−h_t is state-dependent and vanishes at the fixed point by construction.

---

## M2 — JPI: Per-Instance Maximum-Gain Direction via Jacobian Power Iteration

### 1. Precise question
K3 Phase-0 proved a ×1.8 downstream amplification *exists* as mechanism signal. Can we **deliberately exploit** it — compute, per instance, the direction of maximum downstream gain from the model's own Jacobian (label-free) and move *decisions* with it, beating a matched-norm random-direction control?

**Construction [DEFINITION].** For instance x, J(x) = ∂z/∂h_ℓ (logits w.r.t. layer-ℓ hidden state at answer position). Compute top right singular vector v̂₁ by power iteration using vector-Jacobian products (reverse-mode autograd, one backward ≈ 2 forward-pass cost; no labels — VJPs of the model's own logits). Inject h_ℓ ← h_ℓ + ε·v̂₁ vs control h_ℓ ← h_ℓ + ε·v̂_rand, matched norm. Also compute the label-free decision normal n̂ = ∇_{h_ℓ}(z_top1 − z_top2) by one VJP.

### 2. Decision it changes
**KILL** the gain-exploitation family if the max-gain direction is decision-orthogonal (breaking point below) or fails to beat the random control; **CONTINUE** only if per-instance analytic max-gain direction flips wrong→right at ≥ δ_min above control.

### 3. Cheapest falsifying test
- **Kill-first diagnostic (decision-orthogonality):** ĉ = mean|⟨v̂₁, n̂⟩| over 60 items. Same passes as power iteration (12 iters × 2 + 1 VJP + 2 forward ≈ 27 pass-equiv/item). Kill rule: ĉ < 0.1 → **KILL** before any flip test — gain without decision relevance is noise amplification.
- **Flip test:** wrong→right flip rate(JPI) vs flip rate(random), McNemar + δ_min=0.05.
- **Total ≈ 60 × 27 = 1,620 pass-equiv ≈ 0.02 T4-h.**

### 4. Mathematical license
- **[THEOREM] (SVD / power iteration).** v̂₁ maximizes ‖J·u‖ over unit u — downstream logit displacement σ₁·ε is *maximal*; no other unit direction moves the logits more. Power iteration converges at rate |σ₂/σ₁|^t (diagnosable from the iteration itself).
- **[CONJECTURE → quantitative prediction].** IF ĉ ≥ 0.1 on a measurable item fraction, THEN flip-rate(JPI) − flip-rate(random) ≥ δ_min=0.05 — the gain has a decision-relevant component and JPI harvests it.
- **Breaking point:** ĉ < 0.1 — sharp, pre-registered, measured before the flip test. A second breaking point: σ₁/σ₂ ≈ 1 (flat spectrum — no distinguished max-gain direction exists; power iteration cannot find what isn't there).

### 5. Unique support / what kills it
- **Uniquely supports:** a *per-instance, analytically computed* (not selected, not static) direction with *maximal downstream displacement* beating random control. H-001 *selects among* fixed candidate pools; JPI computes the direction — no pool. CLLC is explicitly *Jacobian-free* closed-loop control; JPI is Jacobian-based *open-loop* per-instance — different license, different failure mode. S3-9 asks whether g(α) is linear; JPI asks whether the max-gain direction is *decision-useful* — S3-9's answer doesn't determine JPI's.
- **Kills it:** ĉ < 0.1 (decision-orthogonal gain); flat singular spectrum; flip-rate ≤ control + δ_min.

### 6. Not a re-skin
- Vs killed **(a) static injection**: v̂₁ is per-instance, computed from J(x) — there is no fixed direction; EXP077's family (fixed v at L20) is literally a *degenerate special case* JPI generalizes away from.
- Vs killed **(d) the bridge**: zero label information — VJPs are taken of the model's own logits/gap; no target/foil identity enters. Law #7 clean by construction.
- Vs killed **(f) EXP070**: no oracle selection among candidates; the direction is derived, not chosen.

---

## M3 — RCPA: Relational Cross-Position Amplification (the EXP077-null explainer)

### 1. Precise question
EXP077 killed *within-position* static injection (ΔM=0, p=1.0 everywhere). K1's exoneration left the **relational (t−f) direction** as the live mechanism reading. Is the transferable signal **relational across positions** — i.e., does a per-instance cross-position vector at the output side move decisions where every within-position direction failed?

**Construction [DEFINITION].** Per instance, r = h_L(ans_pos) − h_L(q_pos) (final-layer hidden states at answer vs. question position; positions only, **zero labels**). Inject h_L(ans) ← h_L(ans) + α·r̂ vs random-direction control at matched norm. α grid small (3 values).

### 2. Decision it changes
**KILL** the relational-readout family if r̂ moves decisions no more than random; **CONTINUE** if r̂ flips wrong→right at ≥ δ_min above control — and note the double duty: the same result *explains* EXP077's null as a theorem (below), which is the LOG-219 "every death owes a candidate" payment for the static-geometry death that K2 (routing-bypass) does not pay.

### 3. Cheapest falsifying test
2 forward passes/item (inject r̂, inject random) × 60 items × 1 α (pilot α fixed at the median effective norm from S3-8's decomposition) = **120 passes ≈ 0.0015 T4-h** — the cheapest pilot in the sprint. Endpoint: flip-rate(r̂) vs flip-rate(random), McNemar + δ_min=0.05.

### 4. Mathematical license
- **[CONJECTURE → theorem sketch].** Suppose the decision-relevant feature is relational: the readout depends on comparisons across positions, with relational gradient ∇_rel. Then any within-position static direction v satisfies ⟨v, ∇_rel⟩ ≈ 0 *to first order* — predicting EXP077's ΔM=0/p=1.0 as a structural consequence, not bad luck. This turns the program's most expensive null into a *prediction* of the new theory.
- **[Quantitative prediction].** flip-rate(α·r̂) − flip-rate(random) ≥ δ_min=0.05, while the EXP077 within-position family stays at 0 — a *differential* prediction: one experiment, two opposite outcomes, both pre-registered.
- **Breaking point:** flip-rate(r̂) ≤ flip-rate(random) kills RCPA *and* returns EXP077's null to unexplained status (honest cost recorded).

### 5. Unique support / what kills it
- **Uniquely supports over competitors:** RCPA is the *only* candidate that simultaneously predicts the old null (within-position must fail) and its own positive (cross-position relational must move) — a differential no competitor makes. H-002's relationality is about *input counterfactuals* (x⁺/x⁻ transforms); RCPA's is about *cross-position activation geometry*. S3-7 (spoiler-suppression) asks about token *identity* on rescued items; RCPA asks about *decision movement* from a label-free vector. S3-8 decomposed the *bridge's* margin shift; RCPA tests a *different, label-free* vector on decisions.
- **Kills it:** r̂ ≤ random on flips. Also kills it: r̂ ≈ a static direction across items (cos(r̂_i, r̂_j) high — then it's just static injection re-skinned, and the within-position null would be contradicted rather than explained; check this *first*, $0 on the same passes).

### 6. Not a re-skin
- Vs killed **(a) static injection**: killed family injected *within-position, instance-independent* directions; RCPA injects a *per-instance cross-position relational* vector — the killed family is RCPA's *control arm*, and the theory predicts the control must fail. A re-skin would predict the old family works; RCPA predicts it can't.
- Vs killed **(d) the bridge**: the bridge is normalize(E[target]−E[foil]) — *label*-informed (target/foil identity). r = h(ans_pos) − h(q_pos) uses only *positions* — no label enters; Law #7 clean.
- Vs killed **(c) Procrustes**: no cross-vocabulary mapping is claimed or used; everything is within one model's activation space.

---

## M4 — EAR: Ephemeral Attention Registers (within-pass, circuit-addressed scratch memory)

### 1. Precise question
Do *named, frozen* attention heads implement causally verifiable **write** (content→scratch position) and **read** (scratch→answer position) operations, composable into a within-pass scratch memory — with ablation-verified fidelity, not prompt-engineering hope?

**Construction [DEFINITION].** Append S scratch (filler) tokens. **Write:** patch a computed vector w (instance-derived, e.g., an intermediate result) into scratch position s's residual stream. **Read:** the model's own frozen heads move content to the answer position. Identify write/read heads causally: score heads by attention mass on the write/read patterns (60 passes), then verify by ablation — ablating read heads must destroy the use of written content; writing *random* content must not help.

### 2. Decision it changes
**KILL** the circuit-addressed-memory family if no head beats the random-head write control (attention too diffuse) or ablation doesn't matter; **CONTINUE** only if identified write→read composition beats both controls by ≥ δ_min on a 2-hop task (needs intermediate state: A→B, B→C lookup).

### 3. Cheapest falsifying test
- **Kill-first diagnostic (head scan):** 60 passes scoring write-pattern attention mass per head ≈ **0.0008 T4-h**. Kill rule: best head's write fidelity ≤ random-head control → **KILL** (no addressing circuit exists).
- **Causal composition test (only if scan passes):** 4 arms (computed-write/read-intact, random-write/read-intact, computed-write/read-ablated, no-scratch) × 60 items = 240 passes ≈ **0.003 T4-h**.
- **Total pilot ≈ 0.004 T4-h.**

### 4. Mathematical license
- **[CONJECTURE] (attention-as-addressing).** A head with attention entropy H < h̄ concentrated on the write pattern implements a noisy write with fidelity f_write ≥ 1−ε(H); read fidelity f_read similarly from value-projection alignment. Both quantities are *measured* in the scan, not assumed.
- **[PROPOSITION] (composition).** k-hop scratch fidelity ≥ Π_i f_i under independent-hop errors — predicts the *degradation curve* with hops, a quantitative signature (fidelity must fall multiplicatively, not cliff).
- **Breaking point:** scan finds no head above random control; or ablation of read heads changes nothing (the "memory" was decorative); or fidelity doesn't follow the multiplicative curve (composition claim false even if single-hop works).

### 5. Unique support / what kills it
- **Uniquely supports over competitors:** *named circuits* (head indices), *ablation-verified* addressing, within a *single* forward pass, using the residual stream itself as memory. H2/C2 ELM is **cross-pass** with model-generated keys and an **added** 0.5MB buffer across T passes — EAR is within-pass, no added buffer, addressing by frozen heads not generated keys. S3-5 ACG searches DAGs of micro-interventions; EAR tests one specific composed circuit with a predicted degradation curve. H4/ASR routes *strategies*; EAR routes *data*. CoT/prompting relies on learned behavior; EAR verifies the circuit.
- **Kills it:** diffuse attention (no head above control); ablation-indifference; non-multiplicative degradation.

### 6. Not a re-skin
- Vs killed **(a) static injection**: nothing static is added and nothing is hoped-for — content is *instance-computed*, the addressing circuits are *identified*, and the ablation arms are the falsifier. Static injection has no ablation control; EAR's claim *is* the ablation result.
- Vs killed **(d) bridge / (e) tilt**: no labeled direction, no persistent shift — writes are per-instance transient activations, purged after the pass (Δθ=0, Δactivation=0 post-pass).
- Vs prompting/CoT (not killed, but prior art): token-space scratch relies on the model's learned scratch-use behavior; EAR's scratch is activation-space with circuit-level verification — the changed-burden-of-proof comparator is CoT at matched compute, and the *ablation* result is what CoT cannot produce.

---

## M5 — LRI: Layer-Recycling Iteration (frozen block as a recurrent map)

### 1. Precise question
What happens if we stop treating the frozen stack as feedforward and **iterate a single frozen block as a recurrent map** h_{t+1} = B(h_t)? Does it converge to an attractor (a *new* computational object the feedforward pass never visits), and does that attractor's readout differ from — or beat — the one-pass output?

### 2. Decision it changes
**KILL** fast: the honest prior is that residual+LayerNorm blocks are *expansive*, so the kill-first diagnostic is designed to execute in 400 passes; **CONTINUE** only on the surprise outcome (measured contraction), which would be a genuine discovery about transformer block geometry regardless of capability.

### 3. Cheapest falsifying test
- **Kill-first diagnostic (Lipschitz):** finite-difference estimate L̂ of block B (L20, then final block) on 200 nearby state pairs × 2 passes = **400 passes ≈ 0.005 T4-h**. Kill rule: L̂ ≥ 1 → **KILL** — no attractor exists; idea dead for half a cent of compute.
- **Capability phase (only on surprise L̂ < 1):** iterate to convergence (≤20 iters) on 60 items; endpoint = accuracy(attractor) vs accuracy(one-pass), McNemar + δ_min=0.05. ≈ 1,200 passes ≈ 0.015 T4-h.

### 4. Mathematical license
- **[THEOREM] (Banach).** L < 1 ⇒ unique attracting fixed point, convergence at rate L^t. The diagnostic measures L directly — the theorem does the rest.
- **[CONJECTURE → quantitative prediction].** [SPECULATION] Residual blocks are expansive (L̂ ≥ 1 expected) — the test is *priced as a kill*: the value is the cheap, definitive measurement, and the surprise branch (L̂ < 1) would license a new compute-graph primitive (inference-time recurrence from frozen blocks).
- **Breaking point:** L̂ ≥ 1 — measured, pre-registered, executed before any capability claim can form (anti-theory-preservation by construction).

### 5. Unique support / what kills it
- **Uniquely supports over competitors:** a *structural* claim about the compute graph (recurrence vs feedforward) — no competitor touches graph structure. CLLC does closed-loop *control of injections*; LRI changes the *graph* and injects nothing. S3-4 SAH does α-control on injection magnitude; LRI has no injection. M1 (OSAI) iterates a *belief-dynamics* map Φ built from the predictive distribution; M5 iterates a *frozen transformer block* — different objects, different licenses (contraction of Φ vs Lipschitz of B), different diagnostics.
- **Kills it:** L̂ ≥ 1 (the expected outcome — a kill is the plan, not a disappointment); attractor accuracy ≤ baseline on the surprise branch.

### 6. Not a re-skin
- Vs killed **(a) static injection**: LRI adds *nothing* to the residual stream — it re-applies a frozen nonlinear map. There is no direction, no α, no injection site.
- Vs killed **(f) EXP070 adaptive loop**: EXP070 tested oracle *selection among static injections*; LRI has no candidates, no oracle, no labels — the loop is the block itself.
- Vs killed **(e) readout tilt**: no readout manipulation at all — the experiment lives entirely in mid-network iteration dynamics.

---

## Comparative table

| ID | Candidate | Question in one line | Kill-first diagnostic (cost) | Full pilot cost | Breaking point | Nearest queue/H neighbor & difference |
|---|---|---|---|---|---|---|
| M1 | OSAI | Do self-consistent belief fixed points exist output-side and beat one-pass? | Contraction L̂ of Φ (0.091 T4-h) | 0.20 T4-h | L̂ ≥ 1; fixed-pt acc ≤ baseline | Self-Refine: token-space greedy edits vs activation-space fixed point + contraction certificate |
| M2 | JPI | Can the per-instance max-gain direction move decisions? | Decision-orthogonality ĉ (incl. in 0.02) | 0.02 T4-h | ĉ < 0.1; flat spectrum; flips ≤ control | CLLC: Jacobian-free closed-loop vs Jacobian-based open-loop per-instance; H-001: selection among pools vs analytic computation |
| M3 | RCPA | Is the transferable signal cross-position relational? | Static-ness check cos(r̂ᵢ,r̂ⱼ) ($0 on same passes) | 0.0015 T4-h | flips(r̂) ≤ flips(random) | S3-8: decomposed bridge's margin; M3 tests label-free vector on decisions. K2: routing-bypass vs relational-readout |
| M4 | EAR | Do frozen heads implement ablation-verified read/write scratch memory? | Head write-fidelity scan (0.0008 T4-h) | 0.004 T4-h | no head > random control; ablation-indifference | H2/C2 ELM: cross-pass + added buffer + generated keys vs within-pass + residual stream + frozen-head addressing |
| M5 | LRI | Does iterating a frozen block converge to a useful attractor? | Block Lipschitz L̂ (0.005 T4-h) | 0.02 T4-h (surprise branch) | L̂ ≥ 1 (expected kill) | M1: belief-map iteration vs block iteration — different map, license, diagnostic |

**Total kill-first diagnostics for all five: ≈ 0.12 T4-h (~20 min on 2×T4). Full pilots (only survivors): ≈ 0.25 T4-h.**

## Sequencing recommendation (theory only — CEO/Lead decide)

1. **M3 first** — cheapest (0.0015 T4-h), pays the LOG-219 debt for EXP077's death, and its differential prediction (within-position must fail / cross-position must move) is the sharpest in the set.
2. **M5 second** — the kill is the plan (0.005 T4-h); a 5-minute measurement that either buries recurrence or opens a new primitive.
3. **M4 third** — 0.004 T4-h; circuit-level claim with ablation falsifier; H2-adjacent but structurally distinct.
4. **M2 fourth** — 0.02 T4-h; deliberately exploits the ×1.8 (K3 Phase-0's mechanism signal) rather than merely characterizing it (S3-9).
5. **M1 last** — most expensive (0.20 T4-h) but the only one positing a genuinely new dynamical object (self-consistent belief fixed point); run only if the sprint wants the high-variance bet.

## Honest limitations (pre-registered against myself)

- [INFERENCE] All five default to novelty tier **N1** (Known Combination) until a kill criterion fires or fails — ambition sprint or not, the changed burden of proof applies: any positive a 2026 occupant predicts at matched compute (Self-Refine, A-LQR, LTPO, Meta-Reasoner, LatentMAS) is replication, and each pilot names its forced comparator.
- [INFERENCE] M1's Φ expectation truncation (top-8) is an approximation whose error is *not* bounded in this note — a Law #14 reviewer should demand the truncation-error analysis before SIGN.
- [INFERENCE] M2's VJP-per-iteration cost assumes backward ≈ 2× forward; if the executor's autograd is slower, re-cost before clearance.
- [HYPOTHESIS] M3's "EXP077-null as theorem" sketch is a first-order argument; second-order relational readouts could still admit within-position projections — the differential prediction is the test, not the sketch.
- None of these touch the killed families' *claims*: where a killed family appears, it appears as a **control arm** (M3) or not at all.

*— Theory specialist, LOG-250, 2026-09-24.*
