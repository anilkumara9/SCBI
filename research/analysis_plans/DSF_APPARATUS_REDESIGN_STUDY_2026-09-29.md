# DSF Apparatus-Redesign Study — LOG-4736 (2026-09-29)

**Lane:** LOG-4736 (pre-assigned). **Status:** design study only — $0 CPU,
no model contact, no experiment executed, no license minted. This study
either earns or declines a future worth-it gate; it licenses nothing.

**Family:** B (DSF) — currently UNTESTED (EXP128 RUN-INVALID, apparatus-void).
**Constraining rule:** no ε retuning is licensed. Any return requires a
genuinely new apparatus, not parameter tweaking.

---

## 0. Recommendation (read first)

**(a) Commission a formal worth-it gate — CONDITIONED on reframing.**

The ε-free apparatus developed below (exact autograd directional
derivatives, §2) is genuinely new, defeats EXP128's failure class
structurally (§1), and can carry killing bars (§5). A gate is earned.

**The condition is load-bearing:** the apparatus must be gated as a
**dynamics-characterization measurement (EXP127-class)**, NOT as
Family B's original targeting map. The exact derivative characterizes
the infinitesimal regime, which EXP128's data places 3+ orders of
magnitude below any feasible injection budget (§3c). Family B's
original mission — the layer-targeting map for injection — stays
UNTESTED and unlicensed; this apparatus does not revive it. A gate
that promises targeting would be a bait-and-switch on the family's
mission and must be rejected at gate review.

A gate memo skeleton is in §6. An alternative targeting-path (Path 2,
finite-budget response field) is analyzed and deferred in §6.3.

---

## 1. Diagnosis: why EXP128's finite difference measured saturation, not the propagator norm

### 1.1 The data

[OBSERVATION] (EXP128 report §2.1, executor-produced): on 11/12
linearity-check points, S(ε/2) ≈ 1.5–2.4× S(ε). The numerator
‖g_l(y_l+δ) − g_l(y_l)‖ is ≈ 0.008–0.011 at BOTH ε = 1e-3 and ε/2 —
constant to ~10% while the budget halved. The sole PASS (item 0, L23,
rel = 0.2349) is the readout-adjacent site: one block + LayerNorm, the
shortest span in the check set. The check fails at every site spanning
≥ 2 blocks.

[DEFINITION] For site l and unit direction u, define the response
function h_l(t) = g_l(y_l + t·u), t ≥ 0, where g_l is the full
rest-of-model map (blocks l…23, attention recomputed — EXP128 did NOT
clamp context). Then S(ε) = ‖h_l(ε) − h_l(0)‖/ε.

### 1.2 The structural fact: Pythia is C^∞ — there are no kinks

[FACT] Pythia-410m's forward map is composed of GELU, softmax, and
LayerNorm — all C^∞ on their domains (the only singularities are
LayerNorm zero-variance inputs, a measure-zero set never attained in
practice). Hence h_l(t) is a SMOOTH function of t. There is no
ReLU-style kink to "cross."

[INTERPRETATION] A smooth h_l that is flat on [5e-4, 1e-3] (the data:
numerator constant across the halving) must have a **knee** at some
t* < 5e-4: rapid rise on (0, t*), then saturation. The linear regime —
where h_l(t) − h_l(0) ≈ h_l'(0)·t — ends at t*. EXP128's ε = 1e-3 sat
*above* the knee on 11/12 points: the finite difference measured the
saturated jump, not the derivative.

### 1.3 The mechanism: dense transition thresholds shrunk by the dynamics' own amplification

[INTERPRETATION] What creates knees at t* < 5e-4? Two smooth-but-sharp
transition types, both dense in a 19-block span:

1. **Attention-logit gaps.** In each head, attention mass sits on the
   argmax logit; the runner-up trails by a gap γ. A perturbation that
   shifts the top logit by ~γ reroutes attention mass — a smooth but
   threshold-like jump of size O(‖value vectors‖). Trained transformers
   routinely have small γ (sharp but contested distributions).
2. **GELU transition regions.** GELU(x) = x·Φ(x) transitions over an
   O(1) pre-activation window; pushing a pre-activation through that
   window changes the neuron's contribution by O(1).

A perturbation δ at layer l reaches block m amplified by the
layer-to-layer gain G_{l→m}. It crosses a transition when
G_{l→m}·‖δ‖ ~ (transition scale). With ~10^4–10^5 such transitions in
the span and per-block gains > 1, the nearest knee along a generic
direction lies far below 1e-3. Each crossing contributes a jump; the
sum of jumps is roughly ε-independent over the saturation window
(halving ε removes only the knees in (ε/2, ε] — a small fraction), so
the numerator is constant and S doubles. This matches the data,
including the prompt-invariance of the numerator (~0.01 across items
at L5–L17: the jump scale is set by value-vector norms, a model
property, not prompt content).

[INTERPRETATION] **The apparatus was doomed by the phenomenon it
hunted.** EXP127 measured σ₁ ≈ 9.4–10.1 per 4-block span
(clamped-context): the dynamics transiently amplify ~10× per 4
blocks. That same amplification shrinks the linear regime: a 1e-3
perturbation reaches O(1) transition scale within a handful of blocks.
The non-normality (He ≈ 0.77, EXP086) that motivated DSF guarantees
the finite-difference apparatus cannot see the linear propagator at
any feasible ε — the linear regime is narrower than the instrument's
resolution by construction, not by bad luck.

[OBSERVATION] Consistency check: L23's S(ε) ∈ [3.0, 7.4] (single
block + LN — one attention layer's worth of gaps, insufficient depth
for the saturation to dominate) vs the deep-layer S(ε) ≈ 8–11
(saturated jumps, not the ~2× linear gain EXP127's σ̄ ≈ 1.17/4-blocks
would predict over 19 blocks: 1.04^19 ≈ 2.1). The deep-layer numbers
exceed the linear prediction ~5× — they are jumps, not gains.

**One-sentence diagnosis:** EXP128's ε=1e-3 finite difference
measured amplification-driven transition saturation — the
perturbation crosses dense attention-logit-gap and GELU-transition
thresholds (whose t-scale is shrunk by the very transient
amplification DSF was hunting) long before ε, so the response
numerator is ε-independent and S(ε/2) ≈ 2·S(ε); the estimand was the
saturated jump, never the propagator norm.

---

## 2. The candidate apparatus: exact autograd directional derivatives

### 2.1 Definition

[DEFINITION] For site l, prompt y_l, and fixed unit probe direction
u, define the exact directional gain

    S_l^*(u) = ‖ Dg_l(y_l) · u ‖₂,

computed by forward-mode automatic differentiation
(`torch.autograd.functional.jvp(g_l, (y_l,), (u,))`) through the FULL
rest-of-model map (attention recomputed — the same map EXP128
measured, unclamped). No ε enters. The field is {S_l^*(u)}_{l=0..23}.

JVP (forward-mode) is the faithful choice: the estimand is the norm of
a vector response to one direction. VJP would require a scalar
objective and computes a different object (2·Dgᵀ(Dg·u) for the
squared-norm scalar — related, not identical).

### 2.2 Proof that this is genuinely a different apparatus, not ε→0 in disguise

[THEOREM] (forward-mode AD exactness) For a C^1 map f,
`jvp(f, (y,), (u,))` returns Df(y)·u exactly, up to floating-point
roundoff — by the chain rule applied to the executed computation
graph. It is not a difference quotient; no discretization parameter
exists in its definition.

[PROOF-OF-DIFFERENCE] EXP128's estimator S_l(ε) satisfies
lim_{ε→0} S_l(ε) = S_l^*(u) for each fixed probe (g_l is C^1). EXP128
measured S_l(ε) at ε = 1e-3 and required S_l(ε) ≈ S_l^* via the
linearity check; the data refuted the approximation (saturation
remainder dominated). The JVP apparatus computes **the limit object
S_l^* directly** — the very quantity EXP128's estimator was trying to
approximate. The failure mode "the remainder dominates the estimate"
is not avoided by tuning; it is **inexpressible** in AD, which has no
remainder term. An apparatus with no ε cannot be "ε retuning in
disguise": retuning varies a parameter the new apparatus does not
possess. ∎

The shared limit object is why this is the *same scientific question*
(layer-wise directional sensitivity); the disjoint sensing primitive
(chain rule vs difference quotient) is why it is a *different
apparatus* and not EXP128 resurrected.

### 2.3 The EXP128-vs-EXP127 distinction (non-redundancy)

EXP127 measured σ₁(M) = max_{‖u‖=1} ‖Mu‖ — the **direction-free
worst case**, on the clamped-context L20→L24 span, via power
iteration. The DSF-JVP measures ‖Dg_l·u‖ for a **fixed probe u**, on
the full map, at **24 layers**. Different objects:

| | EXP127 | DSF-JVP (proposed) |
|---|---|---|
| Direction | maximized over (the dynamics' own) | fixed probe u |
| Span | one (L20→L24, clamped) | 24 layers (full map) |
| Output | scalar R = σ₁/σ̄ | field {S_l^*} over depth |
| Question | "what amplifies most?" | "where is this direction amplified?" |

Neither's numbers determine the other's. The JVP field is the
exact-derivative analog of EXP128's ratio — not a re-run of EXP127.
The layer dimension (where along depth amplification lives) is
information no licensed experiment has produced.

---

## 3. Where the apparatus breaks (honest)

**(a) Differentiability — vacuous.** [FACT] GELU/softmax/LayerNorm are
C^∞; the map is differentiable everywhere attained. The "activation
kink" failure class from the brief applies to ReLU nets, not Pythia.
This is NOT the breaking point.

**(b) Numerical — guarded by a convergence diagnostic.** A float32 JVP
through 19 blocks compounds roundoff (~1e-7/block → ~1e-6 relative).
The honest breaking point: a **multi-ε convergence diagnostic** in
float64 — compute F(ε) = ‖g(y+εu)−g(y)‖/ε at ε ∈ {1e-6, 1e-7, 1e-8}
and require F(ε) → JVP value as ε decreases. Single-ε agreement is
insufficient (even 1e-7 may sit above a knee — the knee structure is
dense). Non-convergence → apparatus-void (the AD graph is suspect),
never a verdict. This diagnostic is verdict-immaterial; it guards the
instrument.

**(c) Relevance — the deep break.** [INTERPRETATION] The JVP exactly
measures the *infinitesimal* gain. But §1 shows the linear regime ends
below 5e-4, while any feasible injection budget is ~0.1–0.3 (EXP131's
B = 1% of ‖y‖). The derivative characterizes a regime **3+ orders of
magnitude below any intervention**. As a TARGETING map (which layer to
inject at), the JVP field is the wrong object: the layer maximizing
infinitesimal gain need not maximize finite-budget response, and the
saturated regime — where injection actually operates — is invisible to
it. **As a DYNAMICS CHARACTERIZATION (EXP127-class: "what does the
frozen dynamics look like?"), it is the right object** — EXP127's
R = 8.24 is precedent that infinitesimal characterizations are
publishable boundary facts. The gate must license the latter framing
and forbid the former; §0's condition.

**(d) Bar calibration — the gate's hardest job.** EXP128's Gini ≥ 0.4
bar assumed the field would be flat under the null. But the null
isn't flat: earlier layers span more blocks, so even "boring" dynamics
produce a smooth readout-decreasing profile. Anchored to EXP127
(σ̄ ≈ 1.17/4-blocks → per-block ~1.04): the random-direction exact
field should run ~1.04 (L23) to ~2.1–2.6 (L0) — smooth, low Gini
(≲ 0.2 by the EXP128 bar's own scale). A soft spot is a SPIKE above
this profile. The study therefore requires the gate to carry a
**null-contrast design**: the decision statistic is the concentration
of the *semantic-probe* field against the *isotropic* field measured
on the same layers (same apparatus, same prompts) — e.g.,
ΔGini = Gini_sem − Gini_iso ≥ registered margin, or max studentized
residual of the semantic field against the smooth-profile null ≥
registered threshold. Without a registered null, the Gini bar is
uncalibrated and the gate must not be signed. This requirement is
stated here; the numbers are the gate memo's job.

**(e) Redundancy vs EXP131's ĉ gate.** The JVP gain ‖Dg_l·u‖ is large
iff u aligns with the propagator's leading right-singular vectors —
the layer-wise decomposition of the alignment question EXP131's ĉ
gate asks globally. Partial overlap, not redundancy: ĉ is one number
at one span for v₁; the JVP field is 24 layers × probe directions.
The gate must not re-ask "does v₁ align" — it asks "where does
direction-u's gain concentrate."

---

## 4. Worth-it gate reasoning (applied to the recommendation)

1. **Exact question.** Does the exact (autograd-JVP) directional gain
   of frozen Pythia-410m's layer-to-readout map, evaluated along
   fixed probe directions, concentrate at specific layers beyond the
   smooth null profile — i.e., do direction-specific soft spots exist
   in the infinitesimal dynamics?
2. **Decision changed.** Whether Family B has ANY licensed measurement
   path. Currently UNTESTED with no licensed return. A signed gate
   commissions a new experiment number (EXP132-class); a declined
   gate keeps DSF stood down, honestly.
3. **Cheapest test.** This study: $0, no model contact. Cheapest
   empirical test if gated: ~24 layers × 10 prompts × (1 semantic +
   K isotropic) JVPs ≈ 2–3k JVPs ≈ 1–2 CPU-hours, $0 — same order as
   EXP128's forward budget.
4. **Mathematical license.** [THEOREM] forward-mode AD computes
   Dg(y)·u exactly for C^1 maps (§2.2); the object is the ε→0 limit of
   EXP128's estimator, so it is the same scientific quantity with the
   saturation failure structurally inexpressible. **Breaks where:**
   (i) nondifferentiability — vacuous for GELU nets; (ii) numerical —
   guarded by the multi-ε convergence diagnostic (§3b);
   (iii) relevance — infinitesimal regime only; the license covers
   dynamics characterization, NOT targeting (§3c).
5. **Quantitative prediction.** Anchored to program records only:
   null (dynamically homogeneous-ish, EXP129-class r ≈ 1.000005
   spirit): the isotropic exact field follows the smooth
   readout-decreasing profile (~1.04→~2.1 from EXP127's σ̄ ≈ 1.17
   anchor), Gini ≲ 0.2, and the semantic-probe field matches it
   (ΔGini ≈ 0). Alternative (soft spots): the semantic field spikes
   at ≥1 layer with ΔGini ≥ registered margin (proposed: 0.2, half
   EXP128's bar — gate to confirm against split-half stability).
   EXP127's R = 8.24 bounds the upside: per-layer directional gains
   cannot exceed the span's σ₁-scale without contradicting it.
6. **Breaking point.** (i) Multi-ε convergence diagnostic fails →
   apparatus-void. (ii) ΔGini ≤ margin → KILL the soft-spot premise
   (fields identical up to the null). (iii) Isotropic field itself
   spiky (Gini_iso ≥ 0.4) → KILL as *direction-specific* premise
   (folds into dynamics characterization — the concentration is a
   dynamics property, not a soft spot). (iv) Any targeting claim in
   the pre-reg → gate REJECT (§3c).
7. **Seventh item — constraining kills, and why this is not EXP128
   resurrected.** EXP128 RUN-INVALID: the killed object was the
   *finite-difference sensing primitive* at fixed ε — the new
   apparatus contains zero finite differences (different primitive,
   proven disjoint in §2.2), different bars (null-contrasted Gini, not
   raw Gini ≥ 0.4), different license (characterization, not
   targeting). EXP129 KILL: no loop anywhere — pure measurement, the
   feedback mechanism doesn't transfer. Static-family kills
   (EXP077/EXP094, S5-2's 4.87% bound): those fence semantic
   directions as *injection instruments* and *decision effects*; this
   is a *gain measurement* in which probe directions are diagnostic,
   and no decision is read. EXP130 REJECT: no generation, no
   elicitation — the channel is unengaged. No licensed experiment has
   measured layer-wise exact directional gains; the question is
   unfollowed, not killed.

---

## 5. Falsifiability check

**The design can be killed — three executable killing bars** (§4.6):
ΔGini ≤ margin (no direction-specific structure); Gini_iso ≥ 0.4
(concentration is generic dynamics, not a soft spot); convergence
diagnostic failure (apparatus-void, hypothesis UNTESTED — the honest
void, not a rescue). A design study that couldn't name its killer
would decline the gate; this one names three. The falsifiability
requirement is met.

---

## 6. Recommendation and gate-memo skeleton

### 6.1 Recommendation

**(a) Commission a formal worth-it gate** for an ε-free
directional-gain field experiment (EXP132-class number at minting),
subject to the §0 reframing condition: the gate memo must state in
its §1 that the experiment is a **dynamics-characterization
measurement**, must carry **no targeting claim**, and must include the
null-contrast bar design (§3d) and the multi-ε convergence diagnostic
(§3b) as breaking points. A gate memo missing any of these is
returned, not signed.

### 6.2 Gate-memo skeleton (for the gate lane)

1. Exact question (§4.1 verbatim).
2. Estimand: {S_l^*(u)} for u ∈ {1 semantic probe set (registered:
   which vectors, pinned hashes) + K isotropic controls}, l = 0…23,
   10 verbatim EXP107 prompts (EXP127's decision set, comparability).
3. Apparatus: full-map forward-mode JVP, float32; Δθ=0 (LOG-331
   pre/post); protocol-hash lock; no ε anywhere in the executor
   (grep-verifiable).
4. Breaking points: multi-ε convergence diagnostic (float64,
   ε ∈ {1e-6, 1e-7, 1e-8}, convergence to JVP required) →
   apparatus-void; budget/sanity guards per Law #9.
5. Decision statistic: ΔGini = Gini_sem − Gini_iso with registered
   margin (proposed 0.2; gate to justify against split-half
   stability of the isotropic field); spike-detection secondary.
6. Bars: ΔGini ≥ margin → CONTINUE (soft spots exist as a dynamics
   fact); ΔGini ≤ 0 → KILL; Gini_iso ≥ 0.4 → KILL-as-premise
   (folds to characterization); margin zone → HELD.
7. Law #9 ordering: guards → backbone pin → JVP batches →
   convergence-diagnostic evaluation → raw-record hash-pin →
   metric (ΔGini) → decision.
8. Cost/honesty: ~2–3k JVPs, 1–2 CPU-hours, $0; characterization
   only; scoreboard untouched; no generality beyond Pythia-410m and
   the 10 prompts.
9. Seventh item: §4.7 verbatim.

### 6.3 Alternative considered and deferred: Path 2 (finite-budget response field)

[INTERPRETATION] The targeting mission could instead be served by
measuring the **finite-budget response** ‖g_l(y_l+δ)−g_l(y_l)‖ at the
*actual injection budget* B (~0.1–0.3) — the quantity targeting
literally needs, with no linearity claim (so EXP128's killer check is
inapplicable: there is no linear-regime claim to check). This is
*not* ε-retuning: the estimand (saturated finite-budget response),
the claim (budget-specific targeting prior, disclosed as such), and
the bars (stability-gated ranking, no linearity gate) all differ from
EXP128. **Deferred because:** (i) it sits uncomfortably close to the
barred move and would need Law #14 to rule explicitly that the
estimand change makes it a new experiment; (ii) jump-dominated
responses need stability bars the program hasn't designed; (iii) the
ε-free path (Path 1) is cleaner, cheaper to gate, and its failure
modes are fully characterized here. Path 2 stays open as a future
gate candidate with its own worth-it reasoning — it is not licensed
by this study.

---

## 7. Boundary

- This study mints no experiment number, signs no protocol, and
  licenses no execution. The next step is a **gate lane**, not an
  execution lane.
- Family B's original mission (targeting map for injection) is
  **not revived** by this study — it remains UNTESTED with no
  licensed path. Path 1 answers a different (characterization)
  question; Path 2 is deferred.
- No model was contacted in this lane; every number cited is from
  program records (EXP127/128/129 reports, LOG-331).
- The mechanism in §1.3 (attention-logit-gap crossing as the
  dominant knee source) is [INTERPRETATION]/[CONJECTURE] built on
  [OBSERVATION]s — the diagnosis the new apparatus must defeat
  (saturation below 5e-4) is data; the micro-mechanism is inference.
  The apparatus defeats the data-level failure regardless of which
  micro-mechanism dominates, because AD has no ε.
- Novelty: N1 — Known Combination (unchanged).

---

*End of study. Lane: LOG-4736. Recommendation: (a) — commission the
gate, conditioned on the §0 reframing.*
