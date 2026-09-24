# SCBI Innovation Sprint 3 — Direction Review Candidates (2026-09-23)

**Role:** track-10 Architecture Inventor (unconstrained brainstormer; SCPM name and
architecture not protected), working with track-4 Literature discipline.
**CEO directive:** "Direction Review + Innovation Sprint 3." **Track:** CPU-only
ideation — $0, no GPU, no experiments run, no weights touched, no signed artifact
modified. This track does not touch the LOG-197 audit chain.
**Epistemic standard:** every load-bearing claim carries double labeling —
FACT / INFERENCE / HYPOTHESIS / SPECULATION (mentor canonical layer) + the repo
10-label standard (AGENTS.md §5). `[OBSERVATION]` = measured. `[CONJECTURE]` =
plausible, untested. Nothing below is a result until a kill criterion fires or
fails to fire. **Novelty default:** N1 (Known Combination) unless the audit in (b)
earns better. Anything UNVERIFIED is marked UNVERIFIED, never used rhetorically.
**Experiment numbers:** none assigned — candidates are proposals, numbered only
if/when pre-registered.

## Reading discharged (before writing)

- `research/synthesis/SYNTHESIS_A_J_REV2_2026-09-23.md` — §F (C1–C6, E7,
  E8-conditional; not duplicated), §D1 (prior-art map: CAA, PPLM, Self-Refine,
  DEER, STARS, LTPO, Meta-Reasoner, LatentMAS, NoisyCoconut, ∇-Reasoner, RISER,
  Activation-LQR, SVF[UNVERIFIED]), §D2 (boundary conditions 1–5), §H (kill
  trigger + bridge battery K1–K3), §J (3-stage roadmap), Appendix V (verification
  statuses).
- `research/innovation/SPRINT_2026-09-23.md` (P1–P7, New Ideas 1–7, cut list) and
  `SPRINT2_2026-09-23.md` (G1/G2, C-A/C-B/C-C, M1–M3, D1–D3, kill list, foundations
  track) — the graveyard was searched; dead ideas stay dead (deltas recorded in
  §"Graveyard check").
- `research/MENTORSHIP_DIRECTIVE.md` — the boxed standard, P1–P4, the three
  evidentiary levels (L1 ≠ L2 ≠ L3, never silently crossed), the five permitted
  verdicts (Supported / Not supported / Inconclusive / Underdetermined / Refuted).
- `research/synthesis/CLUSTER_A_2026-09-23.md` — open slots: adaptive/closed-loop
  control, verifier bottleneck, latent collaboration; the Law #7 bridge challenge;
  the bypass-vs-routing discriminator.

## Standing facts (not relitigated)

- [OBSERVATION] Five static-geometry rooms dead (EXP065/066/077/078): raw
  cross-vocab cosine ≈0.7 with zero causal transfer under static injection.
- [OBSERVATION] The output bridge rescues (+10 to +23pp) everywhere, always
  label-informed (Law #7 caveat standing; K1–K3 battery pending).
- [OBSERVATION] G1 Refuted the §3.3 QK null-space sentence; mechanism is
  readout-misalignment-or-unknown [CONJECTURE].
- [FACT] Program compute figure: ~22 forward passes/s on pythia-410m (2×T4),
  per Sprint 2. All T4-hour estimates below derive from it: hours = passes / 22 / 3600.
- [FACT] Statistical bar: δ_min = 0.05 (binding stats revision); verdicts per the
  five permitted categories only; p ≥ 0.05 alone is never a falsifier.

## Global rules (apply to every candidate)

1. **No candidate earns GPU without pre-registered kill criteria and a Law
   #14-signed plan** — stated per candidate in (e). The pilot gate in (e) must
   pass first.
2. Endpoints are decision changes only (margin endpoints invalidated, A9).
3. The §F1 conditionality probe (§D2 condition 4) is the L2 operationalization:
   wherever a candidate claims adaptivity, a permuted/adaptive-ablated arm must be
   named that kills the gain if the adaptivity is decorative.
4. Changed burden of proof (§D2): a positive result predicted by 2026 prior art
   (LTPO, LatentMAS, NoisyCoconut, Meta-Reasoner) at matched compute is a
   replication, not a novelty result.

## The six candidates

| # | Candidate | Open problem attacked | Mentor-list lineage |
|---|---|---|---|
| S3-1 | ARP — Attention-Response Profile verifier | verifier bottleneck | verifier/controller separation |
| S3-2 | LOM — Library of Operators, per-instance mixing | cross-task transfer; autonomous representation discovery | adaptive routing between representations; dynamic basis invention |
| S3-3 | DUG — Doubt-gated escalation (layer-disagreement signal) | adaptive compute allocation | cognitive resource allocation; "discover when computation is insufficient" |
| S3-4 | SAH — Stability-hysteresis α control | closed-loop/adaptive; verifier bottleneck (cheat detection) | closed-loop control, setpoint-free |
| S3-5 | ACG — Adaptive computational graphs (conditional micro-intervention DAGs) | autonomous representation discovery | temporary computational graphs; counterfactual latent computation |
| S3-6 | AAR — Adversarial attack-survival selection | verifier bottleneck | verifying/falsifying own hypotheses |

---

## S3-1. ARP — Attention-Response Profile verifier (a target-free causal fingerprint)

### (a) MECHANISM SKETCH

**Objects** [DEFINITION]. Frozen model M (pythia-410m, L = 32 layers); intervention
layer l* (L20); candidate intervention δ ∈ ℝ^d (a steering direction); item x;
answer position p.

**Operators** [DEFINITION]. For δ applied at (l*, p) with strength α, define the
*layer response profile*
R(δ; x) = (r_{l*}(δ), …, r_L(δ)) ∈ ℝ^{L−l*+1},
r_l(δ) = ‖h_l(x;δ) − h_l(x;0)‖₂ / ‖h_l(x;0)‖₂,
the normalized downstream activation displacement per layer; and the *attention
engagement*
e_l(δ) = ‖A_l(x;δ) − A_l(x;0)‖_F / ‖A_l(x;0)‖_F,
the normalized change in the attention pattern at layer l. The *causal
fingerprint* of δ on x is the pair F(δ;x) = (R(δ;x), (e_l(δ))_l).

**What evolves** [HYPOTHESIS]/[HYPOTHESIS]. Nothing persistent: the fingerprint is
measured per candidate per item from forward passes; the temporary state is the
selected δ*(x), discarded after the item. Δθ=0 [FACT]/[PROPOSITION]: fingerprints
are read from activations; no parameter is mutated.

**The verifier rule (target-free)** [HYPOTHESIS]/[HYPOTHESIS]. Given a candidate
pool {δ_j} (all target-free constructions), select
δ*(x) = argmax_j  Σ_{l>l*} e_l(δ_j) / (1 + Var_l(R(δ_j;x))).
[CONJECTURE]/[CONJECTURE]: causally-real interventions produce fingerprints that
are *front-loaded and attention-engaging* (large e_l in early downstream layers,
decaying displacement); readout cheats produce *flat, attention-silent* profiles
(R ≈ constant across layers, e_l ≈ 0 — the vector rides the residual stream
untouched to the unembedding). The exact functional form is pre-registered at
preregistration time; the form above is the pilot's.

### (b) NOVELTY AUDIT

- **Family C (self-consistency, ToT, Self-Refine, LLM-Monkeys, rStar-Math):** all
  evaluate *outputs* (agreement, reward, selection). ARP evaluates the *internal
  response* to an intervention. No Family C member measures layer response
  profiles. Boundary is clean.
- **ρ-gate / Sprint P3 (target-free steerability diagnostic):** cross-view
  *decision* agreement across input views. ARP is single-view and internal —
  orthogonal measurement, different object.
- **A-LQR / CLLC (Family E / §E C1):** tracking error against a *setpoint*.
  ARP is setpoint-free and comparative across candidates.
- **G1 per-head table:** weight-only, static, per-head. ARP is live,
  per-item, per-candidate, activation-based.
- **∇-Reasoner / PPLM (Families D, C):** gradient-based. ARP is gradient-free.
- **Margin-shift:** invalidated as an endpoint (A9); ARP never reads margins —
  only activation/attention deltas.
- **Honest tier: N1** [INFERENCE]/[INTERPRETATION] (downstream-effect measurement +
  unsupervised selection = known combination). Promotion path: N2-adjacent only if
  the fingerprint *discriminates causal from cheat across intervention families* —
  that would be a new measurement primitive, not just a new combination.

### (c) UNIQUE SUPPORT (boxed standard, box 1)

[All three required jointly; HYPOTHESIS]/[HYPOTHESIS]: (i) on archived EXP065/066/077
interventions — bridge (known causal) vs B_agg/B_wrong (known inert) — the
fingerprint distance separates the classes (permutation test, p < 0.05); (ii) a
verifier selecting by the ARP rule beats *random selection* over a candidate pool
at matched compute (lower 95% CI for ΔM_ARP − ΔM_random > δ_min); (iii) the
§F1-style conditionality cell: permuted fingerprints (same marginals, broken
item-linkage) kill the selection gain — the measurements are load-bearing.
No reviewed competitor predicts (i): output-agreement verifiers (self-consistency,
Self-Refine's critic) predict nothing about internal response profiles; margin
readouts are invalidated.

### (d) KILLER (boxed standard, box 2)

- **Pilot gate ($0, archived):** permutation test on fingerprint distance between
  bridge profiles and B_agg/B_wrong profiles: p ≥ 0.05 → the fingerprint carries
  no causal signal → verdict **Not supported**; ARP is withdrawn as a verifier
  (survives only as a diagnostic measurement if it separates *something*
  pre-registered, else fully withdrawn).
- **Live kill:** 95% CI for (ΔM_ARP-selected − ΔM_random-selected) rules out
  δ_min (U < 0.05) at matched compute → **Not supported** for the verifier claim.
- CI overlapping δ_min → **Inconclusive** (underpowered), held for a powered
  re-test, never culled on this cell.

### (e) CHEAPEST DISCRIMINATING EXPERIMENT

- **Stage 0 ($0 GPU):** compute (R, E) for archived interventions from EXP065/066/077
  artifacts — CPU only. **Feasibility check first:** verify per-layer attention
  snapshots exist in the archive; Sprint N3's feasibility note warns archives may
  hold only aggregate tables — if snapshots are absent, Stage 0b = 240 live passes
  (60 items × 4 conditions {B_agg, bridge, B_wrong, B_perp}) ≈ 240/22 ≈ 11 s ≈
  **0.003 T4-h**.
- **Stage 1 (evaluator test):** candidate pool K = 8 target-free directions per item;
  profile each (60 × 8 = 480 passes) + selection test vs random-selected (60 × 2 =
  120) = **600 passes ≈ 27 s ≈ 0.008 T4-h**.
- **No GPU without kill criteria and a Law #14-signed plan** — the pilot gate
  (Stage-0 separation, p < 0.05) must pass before Stage 1 is built.

### (f) EVIDENTIARY LEVEL

**L2** (as a verifier component) [INFERENCE]/[INTERPRETATION]. Why not L1: the
endpoint is *selection quality* (beats random/permuted selection at matched
compute), never a raw rescue number — a headline ΔM alone is explicitly
inadmissible as support. Why not L3: no new capability is claimed; the task is
unchanged. The permuted-fingerprint cell is the §D2-condition-4 operationalization:
the evaluator's measurements must be load-bearing within the episode, otherwise
it is open-loop selection with extra steps.

---

## S3-2. LOM — Library of Operators with per-instance mixing (cross-task operator retrieval)

### (a) MECHANISM SKETCH

**Objects** [DEFINITION]. Donor task families T_1..T_M (M = 4 pre-registered, e.g.
1-hop capital, 1-hop birthplace, 2-hop with disjoint entities — entity-disjoint
from the test benchmark); library L = {b_1, …, b_M}, each
b_m = normalize(mean of contrast directions within donor family m), constructed
label-informed on **donor items only** (Law #7 clean at test: test items never
contribute to the library).

**Operators** [DEFINITION]. Per test item x, with live residual h_{l*}(x) at L20:
mixing weights w_j(x) = softmax(⟨ĥ_{l*}(x), b̂_j⟩ / τ), τ pre-registered
temperature, hats = normalized. Intervention:
h_{l*} ← h_{l*} + α Σ_j w_j(x)·b_j, α pre-registered.
*Operator retrieval* = selecting **which basis to apply** from live-state
similarity; contrast *state retrieval* (SVF-KNN [UNVERIFIED]): steering toward
retrieved **states**' centroid. The retrieved object differs (operator vs state)
and the application differs (weighted mixture vs centroid-steering).

**What evolves** [HYPOTHESIS]/[HYPOTHESIS]. The per-item weight vector w(x)
(temporary, discarded after the item). Δθ=0 [FACT]/[PROPOSITION]: the library is
fixed vectors; weights are a runtime softmax; no parameter mutation.

**Claim** [HYPOTHESIS]/[HYPOTHESIS]. Cross-task relational structure is reusable at
the *operator* level, and the frozen model can route to the right operator per
instance without labels — "adaptive routing between representations" (mentor
list) made target-free. This is the cross-task-transfer open problem attacked
directly: donor *tasks*, not donor items.

### (b) NOVELTY AUDIT

- **SVF-KNN (Sprint New Idea 1; SVF primary UNVERIFIED per §D1 — cited as sweep
  note only):** retrieves nearest-neighbor *states* from a bank, steers toward
  their centroid. LOM retrieves *operators* and applies a per-instance weighted
  mixture. Different retrieved object, different application, different claim
  (routing-to-tool vs moving-toward-state).
- **RISER (Findings of ACL 2026, verified):** a *trained* RL router composes
  reasoning vectors — the trained-component lane, excluded from core SCBI by Law
  #6. LOM is training-free, similarity-routed; RISER is the forced "what does the
  trained router buy" comparator, not an equivalence threat.
- **CAST (ICLR 2025):** gates *one* vector on/off via condition similarity. LOM
  mixes across a *multi-task library* — gating vs mixing, one task vs many.
- **Sprint1 P1 (compositional factorization):** fixed sum v(R1)+v(R2) for 2-hop.
  LOM's weights are per-instance and cross-task; P1 is fixed and within-task.
- **C-A donor bridge (Sprint2; §E E8-conditional):** donor *items*, same relation,
  single centroid. LOM: donor *tasks*, multiple bases, per-instance mixing.
- **Honest tier: N1** [INFERENCE]/[INTERPRETATION]. Anti-collapse guard: if mixing
  weights go one-hot on the home task, LOM reduces to C-A — the entropy diagnostic
  in (c) is the pre-registered guard against this reduction.

### (c) UNIQUE SUPPORT (boxed standard, box 1)

[All four required jointly; HYPOTHESIS]/[HYPOTHESIS]: (i) routing is *used*:
mean item-mixing-entropy H(w) > 0.5·log M (pre-registered; anti-collapse guard);
(ii) LOM beats the best-single-library-basis at matched compute (lower 95% CI >
δ_min) — the library adds value over picking the best donor task; (iii) LOM beats
*uniform mixing* (w_j = 1/M) — the §F1 adaptive-ablation for routers: the
per-instance weights do work; (iv) the argmax basis per item correlates with the
item's relation type above chance — the routing is *correct*, not merely variable.
No competitor predicts (iii)+(iv) jointly: SVF-KNN has no per-instance operator
mixing; CAST has no library; RISER's router is trained.

### (d) KILLER (boxed standard, box 2)

- Mean H(w) ≤ 0.2·log M → routing collapses to decoration → **Not supported** as
  adaptive routing (demote: survives only as "best-basis selection" if (ii) holds
  alone — recorded as a demotion, not a rescue).
- 95% CI for (ΔM_LOM − ΔM_best-single) rules out δ_min (U < 0.05) →
  **Not supported** — the library adds nothing over the best donor task.
- 95% CI for (ΔM_LOM − ΔM_uniform-mix) rules out δ_min → per-instance weights are
  decoration → **Not supported** for the adaptivity claim.
- CI overlapping δ_min on any cell → **Inconclusive**, held for a powered re-test.

### (e) CHEAPEST DISCRIMINATING EXPERIMENT

- **Library construction (one-time, amortized):** 4 families × 20 donor items =
  **80 passes ≈ 4 s ≈ 0.001 T4-h** (donor items are support, not test).
- **Pilot:** N = 60 headroom items × 7 conditions {C1 unintervened; C2 best-single
  donor basis; C3 uniform mix; C4 per-instance mix (primary); C5 B_agg; C6 B_wrong;
  C7 output bridge} = **420 passes ≈ 19 s ≈ 0.005 T4-h**.
- **Pilot gate:** each donor basis must be individually non-harmful on a 20-item
  donor-validation split (pre-registered exclusion: a basis flipping correct→wrong
  at >10% is dropped before the mixing test — a harmful library member poisons
  the mix).
- **No GPU without kill criteria and a Law #14-signed plan** — stated.

### (f) EVIDENTIARY LEVEL

**L2** [INFERENCE]/[INTERPRETATION]. Why not L1: the primary comparisons are LOM vs
best-single-basis and vs uniform-mix *at matched compute* — a raw rescue gain over
baseline is explicitly insufficient (that cell is C-A's L1 territory). The
per-instance weight vector w(x) is the input-dependent computation the L2 bar
requires. Why not L3: no new capability is claimed; the task family is the same
2-hop benchmark (no chance-bar, no Stage-3 discovery bar). Silent-crossing guard:
headline ΔM is reported alongside the ablation deltas; the L2 verdict rides on
(ii)+(iii) only.

---

## S3-3. DUG — Doubt-gated escalation (layer-disagreement as the doubt signal)

### (a) MECHANISM SKETCH

**Objects** [DEFINITION]. One forward pass per item x. Logit lens: unembedding
applied to a mid-layer residual, a standard interpretability operator [FACT].

**Operators** [DEFINITION]. *Doubt scalar*
d(x) = H(softmax(z_L)) + λ·D_layer(x),
where H is the answer-distribution entropy at the final layer and
D_layer(x) = 1 − cos( readout(h_{l_mid}), readout(h_L) ) — the *disagreement
between a mid-layer logit-lens readout and the final readout* (l_mid
pre-registered, e.g. L10/410m). Budget rule: if d(x) < τ (pre-registered
threshold), answer directly (1F); else escalate to the heavy mechanism
(pre-registered: the program's current best per-instance candidate, ~4F/item).

**What evolves** [HYPOTHESIS]/[HYPOTHESIS]. The per-item budget allocation
(temporary). Δθ=0 [FACT]/[PROPOSITION]: doubt is read from activations, never
trained.

**Claim** [HYPOTHESIS]/[HYPOTHESIS]. Internal readout disagreement marks "existing
computation insufficient" — the escalation trigger the directive's capability
list asks for ("discovering when existing computation is insufficient and
escalating"). Note the inversion vs DEER (Family F): DEER *exits early* on
confidence (compute ↓); DUG *escalates* on doubt (compute ↑ where needed). The
claimed new piece is the *layer-disagreement signal*, not gating per se.

### (b) NOVELTY AUDIT

- **DEER (Family F, forced baseline):** confidence-gated early *exit* — opposite
  direction (reduction vs escalation), different signal (confidence vs
  disagreement).
- **EAGER (Cohere, Oct 2025, index):** entropy-gated *generation branching* at
  high-entropy tokens *during* generation. DUG gates *post-hoc intervention
  budget* on *readout disagreement*, not entropy — different signal, different
  gated object. The Sprint N5 EAGER arm varies steering *strength* α by entropy;
  DUG varies *whether to intervene at all* by disagreement.
- **ASR (§E C4):** bandit-learned strategy policy, policy scope [INCOMPLETE].
  DUG is a fixed-threshold escalator with a named signal — simpler, and the
  layer-disagreement doubt signal is not in ASR's spec.
- **Honest tier: N1** [INFERENCE]/[INTERPRETATION] (gating is old; the combination
  of escalation-direction + disagreement-signal is the bid).

### (c) UNIQUE SUPPORT (boxed standard, box 1)

[HYPOTHESIS]/[HYPOTHESIS]: (i) AUC(d(x), rescuable(x)) > 0.6 pre-registered —
measured on archived headroom items ($0; feasibility: needs mid-layer residual
snapshots for the logit lens, else Stage 0b); (ii) doubt-gated escalation beats
*uniform-heavy* (escalate-all) at **matched total FLOPs** — the §F1
adaptive-ablation: the allocation does work; (iii) ablating the D_layer term
(entropy-only doubt) removes the AUC gain — the disagreement signal does work,
not just entropy. No competitor predicts (iii): entropy-gating baselines
(EAGER/DEER) predict entropy suffices.

### (d) KILLER (boxed standard, box 2)

- AUC(d, rescuable) ≤ 0.55 (chance band) → the doubt signal is noise →
  **Not supported**.
- 95% CI for (ΔM_gated − ΔM_uniform-heavy) rules out δ_min at matched total FLOPs
  → allocation buys nothing → **Not supported** (demote: "escalation helps,
  gating doesn't" survives only as L1 engineering if escalate-all beats baseline
  — recorded as a demotion).
- CI overlapping δ_min → **Inconclusive**, held.

### (e) CHEAPEST DISCRIMINATING EXPERIMENT

- **Stage 0 ($0):** AUC analysis on archived EXP065/066/077 logits + residuals.
  Feasibility check: mid-layer residual snapshots required for the logit lens; if
  absent, Stage 0b = 60 live passes (1F/item doubt probe) ≈ 3 s.
- **Pilot:** N = 60: doubt probe 60×1F = 60; gated subset (~30% = 18 items) × 4F =
  72; uniform-heavy 60×4F = 240; total ≈ **372 passes ≈ 17 s ≈ 0.005 T4-h**.
- **Pilot gate:** Stage-0 AUC must clear 0.6 before any GPU spend.
- **No GPU without kill criteria and a Law #14-signed plan** — stated.

### (f) EVIDENTIARY LEVEL

**L2** [INFERENCE]/[INTERPRETATION] — adaptive compute allocation is the track-3 /
§I-condition-2 bar: per-item compute correlates with difficulty at fixed total
budget, and ablating the adaptivity (uniform-heavy) destroys the gain. L1
("escalation improves scores") is explicitly *not* the claim; the verdict rides
on the matched-FLOPs ablation (ii). Cannot be L3: no new capability, same task.
This is the candidate most directly disciplined against silent level-crossing:
any headline gain without the ablation win is reported as L1 engineering only.

---

## S3-4. SAH — Stability-hysteresis α control (setpoint-free 1-D closed loop)

### (a) MECHANISM SKETCH

**Objects** [DEFINITION]. Fixed direction v̂ (any candidate basis); scalar strength
α on a pre-registered grid G = {0.125, 0.25, 0.5, 1.0, 2.0, 4.0}; decision function
D(α) = argmax f(x; α·v̂).

**Operators** [DEFINITION]. A *stable flip* at α_k ∈ G iff D(α_k) ≠ D(0) **and**
D(α_k) = D(α_{k+1}) — the flipped decision persists one grid step further
(hysteresis). An *unstable flip* iff D(α_k) ≠ D(0) but the decision does not
persist (the marginal regime — the B_wrong signature). Control rule:
α*(x) = smallest α_k admitting a stable flip; if none, abstain (α* = 0).

**What evolves** [HYPOTHESIS]/[HYPOTHESIS]. The scalar α_t per item (temporary).
Δθ=0 [FACT]/[PROPOSITION]: scalar search over forward passes; no parameter
mutation.

**Claim** [HYPOTHESIS]/[HYPOTHESIS]. Each instance has its own distance-to-boundary
in the intervention direction; the corpus's fixed α undershoots some items and
overshoots others (overshoot = margin-cheat regime). Stable flips mark genuine
state changes; unstable flips mark readout tilts. This is a 1-D closed loop —
measure (decision at α_k), control (advance α), stop on the stability criterion —
with **no setpoint, no Jacobian, no evaluator model**. The stopping rule *is* the
evaluator, and it doubles as a cheat detector.

**Boundary vs Sprint2 D3** (per-instance (α,l*,p) placement search, DEMOTED):
D3 searches a 3-D grid using the loop's unvalidated E. SAH searches 1-D (α only),
the stopping rule is its own evaluator (no external E), and it carries the
stable/unstable cheat-detection signature D3 lacks. The D3 delta is cited, not
buried.

### (b) NOVELTY AUDIT

- **A-LQR / CLLC (Family E / §E C1):** feedback gains toward a *setpoint* via
  Jacobians. SAH is setpoint-free, gradient-free, scalar — the feedback signal is
  decision stability, not tracking error. Different control object entirely.
- **Corpus fixed-α standard:** every program experiment fixes α; per-instance α
  adaptation is untested.
- **Margin endpoints (invalidated, A9):** SAH never reads margins — only argmax
  decisions across the grid.
- **Honest tier: N1** [INFERENCE]/[INTERPRETATION] (1-D adaptive control is
  classical; the application to steering strength with the stability signature is
  the combination).

### (c) UNIQUE SUPPORT (boxed standard, box 1)

[HYPOTHESIS]/[HYPOTHESIS]: (i) on archived flips — bridge vs B_wrong — the
stable-flip rate is significantly higher for the bridge (the signature
discriminates causal from cheat; $0 diagnostic; feasibility: EXP077 ran a partial
α-grid {0.25, 0.5, 1.0, 2.0}); (ii) SAH-selected α* is non-inferior to
*oracle-fixed-α* (best α chosen post-hoc per item, labels used — the ceiling):
ΔM_SAH ≥ ΔM_oracle-α − δ_min (non-inferiority), **and** SAH beats random-α
selection (lower 95% CI > δ_min) — the target-free control does real work; the
grid evaluations are reused for all comparators, so (ii) costs no extra passes;
(iii) the §F1 conditionality cell: randomly permuted α* assignments kill the gain.

### (d) KILLER (boxed standard, box 2)

- Stable-flip rate ≈ 0 on headroom items (nothing is stably flippable with the
  tested directions) → the control has no operating range → **Not supported**.
- 95% CI for (ΔM_SAH − ΔM_random-α) rules out δ_min → the stability rule adds
  nothing over random strength → **Not supported**.
- Bridge and B_wrong show identical stable-flip rates on the archive → the
  cheat-detection signature is void → the diagnostic half is **Not supported**
  (withdrawn as measurement).
- CI overlapping δ_min → **Inconclusive**, held.

### (e) CHEAPEST DISCRIMINATING EXPERIMENT

- **Stage 0 ($0):** stable/unstable classification of archived EXP077 α-sweep
  flips (bridge vs B_wrong separation).
- **Pilot:** N = 60 × 6 grid values = **360 passes ≈ 16 s ≈ 0.005 T4-h**. The grid
  *is* the data: oracle-α, random-α, and permuted-α* comparators are computed
  post-hoc from the same 360 evaluations — the experiment is its own control set.
- **Pilot gate:** Stage-0 signature check (bridge vs B_wrong stable-flip
  separation) must show p < 0.1 before GPU.
- **No GPU without kill criteria and a Law #14-signed plan** — stated.

### (f) EVIDENTIARY LEVEL

**L2** [INFERENCE]/[INTERPRETATION] — per-instance control of intervention strength
with a target-free stopping rule; the L1/L2 discriminator is (ii)+(iii): beating
random-α and the permutation cell. A headline "SAH rescues Xpp" alone is L1 and
explicitly insufficient. Cannot be L3: same task, no new capability. The
cheat-detection half is a diagnostic instrument (L1-enabler), not a capability —
labeled as such.

---

## S3-5. ACG — Adaptive computational graphs (conditional micro-intervention DAGs)

### (a) MECHANISM SKETCH

**Objects** [DEFINITION]. Micro-intervention library P = {μ_1, μ_2, μ_3}
(pre-registered, all **target-free**, none expected to rescue alone):
μ_1 = premise-attention bias (add small constant to attention logits of
premise-entity positions — a routing nudge, not a direction);
μ_2 = LayerNorm-scale perturbation at l* (residual × (1+ε), ε pre-registered —
scale-sensitivity probe);
μ_3 = noise injection at l* (tests robustness).
These are *diagnostic probes*, not steering vectors.

**Operators** [DEFINITION]. The DAG protocol (fixed, pre-registered): apply μ_1;
edge μ_1 → μ_2 fires iff the decision changed after μ_1; edge μ_1 → μ_3 fires iff
it did not; μ_2 → μ_3 fires iff the decision after μ_2 differs from after μ_1.
The *computational graph* G(x) = the traversed path (ordered applied probes +
branch points). The topology is per-instance: different items traverse different
paths.

**What evolves** [HYPOTHESIS]/[HYPOTHESIS]. The active path (temporary, discarded).
Δθ=0 [FACT]/[PROPOSITION]: all probes are activation edits; the protocol is fixed
code.

**Claim** [HYPOTHESIS]/[HYPOTHESIS]. The *sequence and conditionality* of
micro-interventions carries information the individual probes don't — the model's
response to probe j determines probe k, making the computation input-dependent in
a way fixed pipelines aren't. This is "temporary computational graphs" (mentor
list) executed by re-feeding residuals: no external interpreter (vs TTPS), no
text (vs ToT), no parallel branches (vs CLB), no fixed 2-step pipeline (vs C-C).

### (b) NOVELTY AUDIT

- **TTPS (§E C3):** external interpreter executing synthesized programs. ACG has
  no interpreter — the "program" is the traversed probe path, executed by the
  model's own forward passes. Different substrate, different claim.
- **ToT (Family C):** text-level tree search over reasoning steps. ACG is latent,
  serial-conditional, not tree search.
- **CLB (§E C6):** intra-pass parallel branches + merge operator. ACG is
  inter-pass serial + conditional chaining — opposite structure.
- **C-C bridge-amplified CoT (Sprint2):** fixed 2-step bridge cascade across
  generation steps. ACG's topology is per-instance (paths vary); probes are
  target-free diagnostics, not bridges.
- **Sprint1 P1 (compositional factorization):** fixed additive composition. ACG is
  conditional, not additive.
- **Honest tier: N1** [INFERENCE]/[INTERPRETATION].

### (c) UNIQUE SUPPORT (boxed standard, box 1)

[HYPOTHESIS]/[HYPOTHESIS]: (i) path diversity: ≥3 distinct traversed paths each
taken by ≥10% of items (pre-registered) — the graph is actually adaptive, not a
fixed pipeline in disguise; (ii) the full conditional DAG beats the *best fixed
probe order* (same probes, fixed sequence) at matched compute (lower 95% CI >
δ_min) — the conditionality does work; (iii) the §F1 probe: permuted conditioning
(random branch decisions, same marginals) kills the gain — the *decisions* are
load-bearing, not the extra passes. No competitor predicts (ii)+(iii): fixed
pipelines (C-C) predict (ii) fails; parallel methods (CLB) predict nothing about
serial conditionality.

### (d) KILLER (boxed standard, box 2)

- Path collapse: ≥90% of items traverse one path → the "graph" is a fixed pipeline
  in disguise → **Not supported** as adaptive computation.
- 95% CI for (ΔM_DAG − ΔM_fixed-order) rules out δ_min → conditionality adds
  nothing → **Not supported**.
- Permuted-conditioning matches full DAG → branch decisions are decoration →
  **Not supported**.
- CI overlapping δ_min → **Inconclusive**, held.

### (e) CHEAPEST DISCRIMINATING EXPERIMENT

- N = 60. Conditions: C1 unintervened (60×1 = 60); C2 full conditional DAG
  (60 × ≤4F = 240); C3 best fixed probe order (60 × 3F = 180); C4
  permuted-conditioning (60 × ≤4F = 240); C5 output bridge (60). Total ≈
  **780 passes ≈ 35 s ≈ 0.01 T4-h**.
- **Pilot gate:** each probe individually non-harmful on a 20-item pre-check
  (pre-registered exclusion: a probe flipping correct→wrong at >10% is dropped —
  a harmful probe poisons the conditional logic).
- **No GPU without kill criteria and a Law #14-signed plan** — stated.

### (f) EVIDENTIARY LEVEL

**L2** [INFERENCE]/[INTERPRETATION] — the claim is a new *strategy*
(input-dependent computation paths), discriminated by (ii)+(iii) at matched
compute. L1 ("more passes help") is explicitly excluded by the fixed-order
comparator. **L3 is not claimed**; the path is stated, not taken: L3 only if
traversed paths compose novel procedures per the §J Stage-3 discovery bar
(D1–D4) — future work, not this candidate.

---

## S3-6. AAR — Adversarial attack-survival selection (falsification as the verifier)

### (a) MECHANISM SKETCH

**Objects** [DEFINITION]. Two frozen roles (same weights, prompt-role framing):
generator G (answers x) and critic C (proposes a *counterfactual attack*: a
minimal premise perturbation x′ — entity/relation word swap from a fixed,
target-free perturbation set — designed to flip G's answer).

**Operators** [DEFINITION]. Protocol (K = 2 rounds, pre-registered): round r:
a_r = G(x_r); C proposes x′_r; a′_r = G(x′_r); if a′_r ≠ a_r (attack succeeds),
G re-answers with (x, x′_r, a′_r) in context → x_{r+1}. *Attack survival* =
invariance of the answer under K rounds of counterfactual attack. Terminal rule
(pre-registered): the surviving answer is returned; if none survives, fall back
to a_1 (logged).

**What evolves** [HYPOTHESIS]/[HYPOTHESIS]. The attack history (temporary).
Δθ=0 [FACT]/[PROPOSITION]: roles are prompts; perturbations are text edits; no
parameter mutation.

**Claim** [HYPOTHESIS]/[HYPOTHESIS]. Answers surviving adversarial counterfactual
attack are more accurate than answers selected cooperatively — **falsification is
a stronger verifier than confirmation**. Channel note (boundary vs LCMIC §E C5):
AAR defaults to the *text channel* (the critic sees only G's answers, never
residuals); a latent-channel variant is explicitly excluded as LCMIC territory
(§F3 adjudicates channel claims).

### (b) NOVELTY AUDIT

- **Self-Refine (Family C):** cooperative critique ("improve this"). AAR's
  critic objective is inverted: *break* the answer. Adversarial vs cooperative
  is the mechanism distinction.
- **Debate / MoA:** parallel cooperative agents. AAR is serial adversarial.
- **AVI (ICLR 2026, verified):** *trained* verifier guiding correction. AAR's
  critic is the *same frozen model* — no trained component (the open lane:
  "target-free evaluators (every strong 2026 E is trained)").
- **Kill-list "naive self-critique loops" (Sprint2, KILLED):** that kill requires
  any loop proposal to name its error signal and beat the known failure mode.
  AAR names its signal (attack survival) and carries cooperative Self-Refine as a
  forced comparator — it complies with the kill-list's condition rather than
  ignoring it.
- **Honest tier: N1** [INFERENCE]/[INTERPRETATION].

### (c) UNIQUE SUPPORT (boxed standard, box 1)

[HYPOTHESIS]/[HYPOTHESIS]: (i) the critic discriminates: attack success rate on
*wrong* answers > on *right* answers (labels used only for this diagnostic, never
by the protocol); (ii) AAR beats *cooperative Self-Refine* at matched compute
(AAR ≈ 5–7F/item vs Self-Refine at 5F) with lower 95% CI > δ_min — the
adversarial-vs-cooperative discriminator; (iii) AAR beats best-of-5 at matched
compute — survival is not just sampling. No competitor predicts (ii): cooperative
methods predict AAR ≤ Self-Refine; sampling baselines predict (iii) fails.

### (d) KILLER (boxed standard, box 2)

- Critic's attack success ≈ equal on right and wrong answers → attacks are
  vacuous, the critic cannot discriminate → **Not supported**.
- 95% CI for (ΔM_AAR − ΔM_self-refine) rules out δ_min → adversarial adds nothing
  over cooperative → **Not supported** (reduces to expensive self-consistency).
- Degenerate protocol: survival ≈ 100% (nothing ever attacked — perturbation set
  too weak) or ≈ 0% (everything flips — set too strong) → **Inconclusive**
  (miscalibrated, not a mechanism verdict) — one pre-registered recalibration of
  the perturbation set; a second degenerate run → **Not supported**.

### (e) CHEAPEST DISCRIMINATING EXPERIMENT

- N = 60. Per item worst-case: G 1F + C 1F + G(x′) 1F + re-answer 1F + round 2
  (C 1F + G(x′_2) 1F + re-answer 1F) = 7F; typical ≈ 5F (early survival). Budget:
  AAR 60×7 = 420; Self-Refine matched 60×5 = 300; best-of-5 60×5 = 300; total ≈
  **1,020 passes ≈ 46 s ≈ 0.013 T4-h**.
- **Pilot gate:** the perturbation set must show 20–80% attack success on a 20-item
  calibration split (the non-degeneracy band) before the full run.
- **No GPU without kill criteria and a Law #14-signed plan** — stated.

### (f) EVIDENTIARY LEVEL

**L2** [INFERENCE]/[INTERPRETATION] — a new selection strategy (adversarial
survival vs cooperative refinement), discriminated at matched compute. L1 ("more
passes help") is excluded by the best-of-5 comparator. Cannot be L3: same task
family, no chance-bar. The named error signal (attack survival) is what keeps
this candidate on the right side of the self-critique kill listing — stated
explicitly so no future reader mistakes it for the killed variant.

---

## Graveyard check (deltas for the culled and the adjacent)

Searched: Sprint 1 cut list, Sprint 2 kill list (§"The kill list"), §F candidates.
Each candidate above carries its delta inline in (b); summary:

- S3-1 vs Sprint P3 (cross-view agreement diagnostic): different object (internal
  response vs cross-view decisions). vs G1: live per-candidate vs weight-only static.
- S3-2 vs C-A/E8 (donor items, same relation, single centroid): donor *tasks*,
  multi-basis, per-instance mixing. vs SVF-KNN [UNVERIFIED]: operator retrieval vs
  state retrieval. vs RISER: training-free vs trained router.
- S3-3 vs DEER: escalation vs exit. vs EAGER: disagreement-gated budget vs
  entropy-gated generation branching. vs ASR: fixed-threshold escalator vs
  bandit policy.
- S3-4 vs Sprint2 D3 (DEMOTED (α,l*,p) search with unvalidated E): 1-D,
  self-evaluating via the stability signature; D3's delta cited in (a).
- S3-5 vs TTPS: no external interpreter. vs C-C: per-instance topology vs fixed
  2-step pipeline. vs CLB: serial-conditional vs parallel-merge.
- S3-6 vs kill-listed naive self-critique: names its error signal (attack
  survival), carries the known-failure baseline as forced comparator — complies
  with the kill condition.
- None revives: PPLM+internal-evaluator (thin delta), learned soft prefixes,
  7B scaling, GSM8K scope creep, ITI probes, per-token B_agg compounding, margin
  endpoints, label-informed bridge as method. All stay dead.

## Ranking (ceiling × feasibility)

| # | Candidate | Ceiling | Feasibility | Product | Pilot cost |
|---|---|---|---|---|---|
| S3-1 | ARP verifier | 9 | 8 | 72 | $0 archived (+0.008 T4-h live) |
| S3-4 | SAH α-hysteresis | 8 | 9 | 72 | $0 archived (+0.005 T4-h live) |
| S3-3 | DUG doubt-gating | 7 | 9 | 63 | $0 archived (+0.005 T4-h live) |
| S3-2 | LOM operator library | 8 | 7 | 56 | 0.006 T4-h |
| S3-6 | AAR attack-survival | 7 | 7 | 49 | 0.013 T4-h |
| S3-5 | ACG conditional DAGs | 7 | 6 | 42 | 0.01 T4-h |

[INFERENCE]/[INTERPRETATION]: S3-1 and S3-4 rank first because their pilot gates
are $0 archived-data diagnostics — they can die before spending a single forward
pass, which is the cheapest falsification in this sprint. S3-3's $0 AUC gate is
the same shape. All six pilots total ≈ 0.05 T4-h — under four minutes of the
free tier.

## Recommended sequence (CEO decision)

1. **Immediate ($0):** S3-1 Stage 0 (fingerprint separation on archive), S3-4
   Stage 0 (stable/unstable classification of EXP077 α-sweeps), S3-3 Stage 0
   (doubt AUC on archived logits) — all three are CPU-only re-analyses; run the
   feasibility checks (do the archives hold per-layer snapshots? mid-layer
   residuals? full α-sweep ledgers?) first, per Sprint N3's feasibility lesson.
2. **First GPU (minutes):** whichever $0 gate passes → its Stage 1 pilot.
3. **Then:** S3-2 (library build + mixing test), S3-6 (calibration → full run),
   S3-5 (probe pre-check → DAG test).
4. Every step: pre-registration at the EXP067/068 standard → Law #14 adversarial
   review → CEO GPU clearance. No exceptions.

*End of Sprint 3 candidates. No numbers were invented; no results are claimed.
Every candidate is a [HYPOTHESIS] awaiting its kill criterion. The next step for
any candidate the CEO green-lights: pre-registration (number assigned at that
time), then adversarial review (Law #14), then GPU.*
