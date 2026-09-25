# S4 — I1 Formalization (advanced mathematical treatment) + J-tier summit supplement
## 2026-09-24 — LOG-287 (I1 formalization) / LOG-288 (J-tier)

**Standing directives executed this wave:** (1) Founder's address (2026-09-24):
the summit is superhuman intelligence — conscious-level cognition; judge
candidates by whether they could change the computational strategy itself;
bring more ideas; keep falsification-first discipline. (2) Founder's order
(2026-09-24): advanced mathematical treatment for every candidate — definitions,
theorems/conjectures with proofs or proof sketches, quantitative predictions,
explicit breaking points; hand-waving is a defect. Applies to the I1 wave and
everything after. Both acknowledged in LOG-287/288.
**Epistemic standard:** [FACT] / [CONJECTURE] / [PROPOSITION] / [DEFINITION] per
AGENTS.md §5. N1 default. No numbers invented; no experiments run; $0; Δθ=0.

---

# PART A — I1: Cross-context binding repair, formalized

## A1. Definitions [DEFINITION]

- **M**: frozen autoregressive transformer, L layers, hidden dim d, parameters
  θ fixed (Δθ = 0).
- **Item x**: 2-hop query with surface entity e₀, relation r₁, latent
  intermediate entity e₁, relation r₂, answer e₂.
- **P(x) ⊂ [T]**: entity-slot positions in x where e₁ should be bound
  (pre-registered rule: positions of e₀'s mention plus tokens immediately
  following r₁'s surface form; exact tokenization rule fixed at formal pre-reg).
- **Probe q(x)**: single-hop prompt "Q: What is r₁ of e₀? A:" — a clean context
  isolating hop 1.
- **h_l(p; c) ∈ ℝᵈ**: residual stream at layer l, position p, context c.
- **Clean binding** b* := h_{l*}(p_ans; q(x)), p_ans = probe answer position.
- **Composed binding** b̂ := mean_{p ∈ P(x)} h_{l*}(p; x).
- **Degradation coefficient** ρ(x) := cos(b̂, b*) ∈ [−1, 1].
- **Transplant operator** T_Π: (T_Πh)_{l*}(p) = Πb* for p ∈ P(x), identity
  elsewhere. Primary Π = I (no fitting); secondary arm Π = affine map fit on
  support only (pre-registered; never fit on test).

## A2. Noisy-channel model (information theory) [CONJECTURE]

Let E₁ be the true intermediate entity (r.v. over the entity vocabulary).
Composition acts as a noisy channel on the binding:

> **Channel conjecture.** b̂ = A·b* + η for unknown linear degradation A and
> noise η, hence by the data-processing inequality [FACT]
> I(E₁; b̂) ≤ I(E₁; b*).

Transplant is *channel substitution*: replace the degraded observation b̂ with
the cleaner b*. The decision error is bounded below by the Bayes error given
the binding the downstream computation actually sees; if I(E₁; b̂) is the
bottleneck, substitution reduces error. This is the information-theoretic
license: we are not "adding knowledge" (the model already computed b* in the
probe) but *replacing a degraded channel output with a cleaner one*.

**Decodability screen (formal, $0 given activations).** Build entity centroids
{μ_e} from probe bindings b* on support items (nearest-centroid decoder D).
Measure held-out probe decodability acc* = P(D(b*) = e₁) vs composed
decodability acĉ = P(D(b̂) = e₁).

> **Prediction P-A1.** acĉ ≤ acc* − δ_dec, δ_dec = 0.15 pre-registered.
> If acĉ ≥ acc* − δ_dec, the binding is not degraded in the
> linearly-decodable sense → premise dead at $0 (nonlinear-decodability
> escape pre-registered as a *limitation*, never as a rescue).

## A3. Dynamical-systems / control license [PROPOSITION + CONJECTURE]

The suffix of the forward pass (layers l*…L) is a deterministic discrete-time
dynamical system:

> h_{l+1} = F_l(h_l),  F := F_{L−1} ∘ ⋯ ∘ F_{l*}.

Transplant is an **impulsive control input** at time l*:
h_{l*} ↦ h_{l*} + Δ, with Δ = Πb* − b̂ supported on P(x).

> **Sensitivity proposition.** Let L_l be the (empirical, finite-difference)
> Lipschitz constant of F_l. Then ‖F(h+Δ) − F(h)‖ ≤ (∏_l L_l)·‖Δ‖.
> *Proof sketch.* Chain the per-layer Lipschitz bounds; composition of
> L_l-Lipschitz maps is (∏L_l)-Lipschitz. ∎

**Apparatus check (pre-registered).** On the pilot, measure the logit-gap
sensitivity s(x) = ‖∂(logit(e₂) − logit(foil))/∂h_{l*}‖·‖Δ(x)‖ by finite
differences. If s(x) is below the empirical decision threshold for >70% of
items, the impulse *cannot* move decisions → the apparatus is dead (as
opposed to the hypothesis being wrong — the distinction is pre-registered).

**P1-bound compliance.** This is a single open-loop impulse, not a feedback
loop, so P1's δ ≤ 2ε feedback bound does not directly apply — but its spirit
is honored quantitatively: we compute the impulse response s(x) *before*
claiming any gain, and require predicted movable mass to clear δ_min.

## A4. No-free-lunch lemma (justifies the $0 screen as necessary, not heuristic)

> **Lemma.** If b̂ = b* exactly (ρ = 1), transplant T_I is the identity map and
> ΔM = 0 necessarily.
> *Proof.* T_I replaces h_{l*}(p) with b* = b̂ = h_{l*}(p) on P(x); the
> trajectory is unchanged; the output is unchanged. ∎
>
> **Corollary.** Any transplant rescue (ΔM > 0) implies ρ < 1 on rescued items:
> degradation existed. The cosine screen is therefore a *necessary-condition*
> gate — not a heuristic filter.

## A5. Quantitative predictions

- **P-A2 (screen).** ρ̄ := E[ρ(x)] over failed headroom items with
  probe-verified hop-1 correct: predict ρ̄ < 0.85. If ρ̄ ≥ 0.85 → KILL at $0.
- **P-A3 (rescue).** Transplant ΔM ≥ +8pp, lower exact 95% CI > δ_min = 0.05,
  on the ρ-low subset (ρ(x) < 0.85).
- **P-A4 (dose-response — the anti-nonspecificity signature).** Per-item gain
  negatively correlated with ρ(x): Spearman r_s < 0, p < 0.05. A nonspecific
  perturbation account predicts no such dose-response.

## A6. Breaking points (pre-registered)

- **B1.** ρ̄ ≥ 0.85 → no degradation → KILL, no GPU.
- **B2.** acĉ ≥ acc* − 0.15 → KILL in the linearly-decodable sense.
- **B3.** Shuffled-entity transplant (b* from e₁' ≠ e₁) rescues equally:
  ΔM_shuffled ≥ ΔM_transplant − 5pp → effect is nonspecific perturbation →
  KILL the binding-repair family.
- **B4.** Rescue concentrates on items where the probe hop-1 was WRONG →
  the probe, not the binding, is the story → PIVOT (repair the probe
  construction; transplant shelved).
- **B5.** Apparatus check fails (s(x) below threshold on >70% items) →
  INVALID apparatus, not a hypothesis verdict; re-design the impulse
  (layer/position), do not claim a null.

## A7. Cost

Screen: probe passes (60 × 2 if unarchived ≈ 120 passes ≈ 6s) + CPU
cosine/decodability. GPU test only if screens pass: 60 × 5 arms
(C1 unintervened / C2 transplant / C3 shuffled-transplant / C4
transplant-at-wrong-layer discriminant / C5 bridge positive) ≈ 300 passes
≈ <1 min T4. Total <0.01 T4-h.

## A8. What this formalization buys (and what it doesn't)

It buys: (i) the $0 screen as a *theorem-backed* necessary condition (Lemma),
not a heuristic; (ii) an information-theoretic statement of what transplant
*is* (channel substitution — new operation class, not direction search);
(iii) a control-theoretic apparatus check separating "impulse too weak" from
"hypothesis wrong"; (iv) a dose-response signature no nonspecific account can
mimic. It does not buy: any claim above L1 (this is inference repair —
explicitly L1-aimed; no silent crossing), or novelty above N1.

---

# PART B — J-tier: summit-aimed candidates (Founder's address)

*Judged by: "could this, if true, move a frozen model toward qualitatively new,
conscious-level cognition?" L2-aimed (change the computational strategy).
Falsification-first discipline unchanged: every J carries a Law #15 card and a
formal kill criterion. Demotion note: I2/I4 stay queued as the cheapest
falsifications (rigor is how we climb) but are now explicitly labeled L1-aimed;
the J-tier is the L2-aimed summit tier. No silent level-crossing in either
direction.*

## J1. Re-entrant attractor dynamics [CONJECTURE] — L2

**Formal sketch.** Define the re-entrance operator
R(h) := F_{0..k}(Π h_L), where Π: ℝᵈ → ℝᵈ is a *fixed* projection
(pre-registered: Π = W_E W_Uᵀ, the embedding/unembedding transpose pair — no
training, no fitting) mapping the final residual back into an early-layer
input space, and F_{0..k} is the frozen prefix. Iterate h^{(t+1)} = R(h^{(t)}),
h^{(0)} = h_L(x).
> **Claim.** If R is a contraction (empirical Lipschitz κ̂ < 1 by finite
> differences), Banach's fixed-point theorem [FACT] guarantees a unique
> attractor h∞ = lim h^{(t)}.
**Mechanism hypothesis.** The attractor's decoded answer is more accurate than
the single-pass answer: the frozen feedforward net implements *recurrent
attractor computation* at inference time — iterative settling, a qualitatively
new computation (L2), not a better readout (L1).
**Law #15.** (1) Does re-entrant iteration converge, and does the attractor
outperform the single pass? Endpoint: ΔM attractor-vs-single-pass, N=60.
(2) KILL/CONTINUE on the re-entrance family. (3) Cheapest: κ̂ screen on 20
items (≈40 passes); κ̂ ≥ 1 → contraction license lost → do not run full test
(PIVOT to bounded-T trial, pre-registered). Full: T ≤ 8 iters × 60 items ≈ 480
passes ≈ <1 min. (4) License: Banach [THEOREM] + contraction conjecture;
predicts κ̂ < 1 and ΔM_attractor ≥ +8pp (LCI > 0.05). Breaking point: κ̂ ≥ 1
with ΔM ≤ 0 → re-entrance buys nothing → KILL.
**Belief change.** "A feedforward LLM can only compute feedforward functions"
→ "a frozen feedforward net can implement recurrent attractor computation."
**Delta.** vs Sprint2 C-B (fixed point in *unembedding-difference* space):
J1 iterates the *full residual state* through re-entrant layers — different
object, different claim.

## J2. Metacognitive self-modeling [CONJECTURE] — L2

**Formal sketch.** Self-prediction pass with prompt:
"Before answering, predict: will you answer correctly? State YES/NO, then
predict your exact answer." Extract (â_self, conf_self). Discrepancy
D(x) = 1[â_self ≠ â_actual]. Necessary condition (information theory):
I(â_self; correctness) > 0 — measurable on 60 × 2 passes, $0-ish.
**Mechanism hypothesis.** D predicts failure
(P(fail|D=1) ≥ P(fail|D=0) + 0.2, pre-registered), and discrepancy-triggered
revision (re-answer with (â_self, â_actual, D) in context, ≤2 rounds) rescues:
the model carries a *usable self-model* — the first rung of the
consciousness-prerequisite ladder (self-modeling), operationalized as
inference-time computation.
**Law #15.** (1) Does the frozen model model itself usefully on 2-hop items,
and does discrepancy-driven revision rescue? (2) KILL/CONTINUE on the
metacognition family. (3) Cheapest: I-screen first (120 passes); I ≈ 0 →
KILL before any revision test. Revision: 60 × 3 ≈ 180 passes. (4) License:
[CONJECTURE] self-prediction signal exists; predicts I > 0.1 bits and
revision ΔM ≥ +8pp (LCI > 0.05). Breaking point: I ≈ 0 → the model cannot
model itself here → KILL; revision ΔM ≤ 0 despite I > 0 → signal exists but
not actionable → PIVOT (the signal becomes a *diagnostic*, cf. DUG lineage).
**Belief change.** Self-modeling — on every serious list of consciousness
prerequisites — exhibited usefully by a frozen model at inference time.

## J3. Spectral phase transition (random-matrix-theory lens) [CONJECTURE] — L2-aimed, observational first

**Formal sketch.** At each layer l, form the empirical covariance Σ_l of the
residual over positions (n positions, dim d). Compare its eigenvalue spectrum
to the Marchenko–Pastur null [FACT — RMT]: eigenvalues outside the MP bulk
are *signal* (coherent low-rank computation); inside = noise bulk. Define the
transition layer l_c = first l where the signal-eigenvalue count jumps by the
pre-registered rule (≥3 new outliers sustained 2 layers).
**Mechanism hypothesis.** Correct reasoning = emergence of a coherent
low-rank component (a *phase transition* in the residual stream —
statistical-physics framing of cognition); failed items lack the transition.
**Law #15.** (1) Does the signal-eigenvalue count differ between correct and
failed items (permutation test, p < 0.05)? (2) KILL/CONTINUE on the
spectral-lens family — observational only; the *intervention* (amplify the top
signal-PC at l_c — spectral, not directional) is licensed ONLY if the
observational claim holds. (3) Cheapest: the observational test IS cheap —
60 passes capturing per-layer spectra (archive-feasibility known-negative per
LOG-243's lesson, so live pilot from the start; no wasted $0 attempt).
(4) License: MP law [THEOREM] + coherence-emergence conjecture; predicts
signal-count(failed) < signal-count(correct) − 2 (medians). Breaking point:
permutation p ≥ 0.05 → the RMT lens sees nothing → KILL; intervention never
attempted (pre-registered sequencing).
**Belief change.** Reasoning as a *phase transition* — a physics-level
description of when computation becomes coherent.

## J4. Free-energy branch selection [CONJECTURE] — L2

**Formal sketch.** Branch the forward pass at l* into K copies with a
pre-registered structured-perturbation set (the S3-5 μ-probe set as branch
generators — diagnostic probes, not steering vectors). Complete each branch →
(answer a_k, rationale r_k). Select
k* = argmin_k F_k,  F_k := −log p_θ(r_k | x) + λ|r_k|
(the frozen model's own surprise + complexity penalty — the free-energy
principle as a *target-free evaluator*).
**Mechanism hypothesis.** Free-energy selection beats random-branch selection
and the single-pass baseline: the program's central open wound (every strong
2026 evaluator is trained; AVI showed self-correction fails without a reliable
error signal) closed by a *principled, training-free* selector.
**Law #15.** (1) Does free-energy selection over branched trajectories rescue
decisions? Endpoints: ΔM_FE vs single-pass; ΔM_FE vs random-branch.
(2) KILL/CONTINUE on the free-energy-selector family. (3) Cheapest:
K=4 branches × 60 items ≈ 240 passes + selection ≈ <1 min; forced comparator
self-consistency at matched tokens (Sprint2 forced baseline) rides free.
(4) License: free-energy principle [CONJECTURE as mechanism]; predicts
ΔM_FE ≥ +8pp (LCI > 0.05) AND ΔM_FE > ΔM_random-branch (paired p < 0.05).
Breaking point: ΔM_FE ≤ ΔM_random-branch → the selector carries no signal →
KILL; ΔM_FE ≤ 0 → branches contain nothing worth selecting → KILL the
branching family too.
**Belief change.** A candidate law of biological intelligence (free-energy
minimization) operationalized as inference-time computation in a frozen LLM.
**Delta.** vs self-consistency (vote → principled selection); vs E7/DPRS
(readout perturbations + internal E → full-trajectory branches + free-energy
selector); vs S3-1 ARP (causal fingerprint → surprise-based selector).

## J-tier ranking (falsifiability × summit-relevance)

| Rank | ID | Why this order |
|---|---|---|
| 1 | J1 attractor | Contraction is $0-measurable before any GPU; cleanest kill (κ̂ ≥ 1 + ΔM ≤ 0); most radical computation change (recurrence from feedforward) |
| 2 | J4 free-energy | Attacks the program's central wound (target-free evaluator); forced SC comparator built in; kill is decisive |
| 3 | J2 metacognition | Most summit-direct (self-modeling); but revision could collapse to prompt engineering — the I-screen is the load-bearing gate |
| 4 | J3 spectral | Most ambitious lens; weakest intervention license — correctly sequenced as observational-first; intervention never attempted on a null |

## Culled summit-aimed sketches (ruthlessness log)

- **Gödelian self-reference probe** ("can the model reason about its own
  reasoning?"): culled — no statable kill criterion; philosophical, not
  experimental.
- **Integrated information Φ as a signal**: culled — Φ is intractable;
  proxies are disputed; fails the founder's own no-hand-waving order.

---

*End of S4. I1 is now formally specified with a theorem-backed $0 screen, an
information-theoretic license, a control-theoretic apparatus check, and five
pre-registered breaking points. The J-tier gives the summit four falsifiable
shots. No numbers invented; nothing executed; Δθ=0 throughout.*
