# Pre-registration: DSF — Dynamical Sensitivity-Field Mapping of the Frozen Pythia-410m Layer-to-Readout Propagator

**Lane:** LOG-4703 (pre-assigned). **Family:** B of the paradigm-break
sprint (LOG-4693). **Gate:** LOG-4702 (PASS). **License:** EXP086 Stage A (LOG-331) (Henrici He = 0.7332–
0.8343, mean 0.7689, across 48 attention O/V projection components —
the unfollowed lead since 2026-09-23); EXP127 (LOG-4698, bound
CONTINUE — median R = 8.240640 ≥ 3, median σ₁/σ₂ = 1.557689 ≥ 1.5 at
the L20→L24 span: the dynamics-matched amplifier exists *somewhere*;
DSF asks *where sensitivity lives layer-wise*).

**$0 CPU. Δθ=0 by construction.** This pre-registration licenses a
measurement only — **no injection is licensed by it.** The field is the
targeting map for EXP127's downstream v_1 injection test and for
Family C's closed loop; it never becomes a steering claim by itself.
Any injection along any layer of the field needs its own
pre-registration, its own bars, and its own gates. Draft only;
licenses nothing until the launch chain (Law #14 review → fix-
verification → CEO launch decision → execution under a minted number).

**Pre-reg decision record (prompt-set caveat, gate §3):** the decision
set is the 10 verbatim EXP107-bench prompts, canonical-order first 10
(ids `exp107_{flip,ctrl}_exp077_planet_2hop_{0..9}`) — the same
decision set as EXP127, so the two measurements are directly
comparable. **No larger prompt set is licensed by this pre-reg.**
A field minted here is the layer-wise sensitivity structure of *this*
decision set; generality beyond the 10 pinned prompts is barred
(§10). The prompt count a future gate would target, if one is ever
commissioned, is named here for transparency (n=60, bench-disjoint),
but measuring it needs a new gate — it is not licensed here.

---

## 0. The breaking point (read first)

Conjunctive. Any miss → **apparatus-void, hypothesis UNTESTED, no
field minted** (Law #9 ordering: guards → backbone pin → forward
batches (field forwards + ε/2-check forwards, either batch order) →
linearity-check evaluation → raw-record hash-pin → Gini → decision):

(a) **Δθ=0** — backbone LOG-331 parameter hash
    `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed`
    pinned before the first forward and re-pinned after the last
    forward; any mismatch → apparatus-void.
(b) **Linear regime** — the ε/2 linearity check on the pinned subset
    (3 items × 4 layers, 12 check points; §3.6): require
    |S(ε/2) − S(ε)|/S(ε) ≤ 0.25 on ≥ 10 of the 12 check points
    (≥ 80%, executor-computed; 10 is the ceiling of 9.6); fewer →
    apparatus-void (the finite difference is measuring nonlinearity,
    not the propagator norm). No post-hoc ε retuning — a failed
    check is apparatus-void, never a smaller ε.
(c) **Same δ budget per layer** — ‖δ‖ = ε (pinned, §3.3) identical
    across all layers, items, and draws; any layer receiving a
    different budget → apparatus-void (the Gini would measure the
    budget, not the field).
(d) **No training, no weight mutation** — pure forwards through a
    frozen model in eval mode (`model.eval()`, `torch.no_grad()`); the
    executor contains no optimizer, no loss, no backward pass into
    weights.

[DEFINITION] The decision statistic is the **layer-Gini coefficient**
of the 24-element field {S_l}, l = 0…23, plus the top-3 concentration
set: the three layers with largest S_l (deterministic tie-break:
lowest layer index first). Gini is the standard concentration
coefficient:

    G = Σ_i Σ_j |S_i − S_j| / (2 · n² · S̄),  n = 24

computed by the executor (defect class (a)). G = 0 means perfectly
uniform; G → 1 means all sensitivity in one layer. The Gini-and-top-3
pair is the registered decision statistic — no p-value is computed,
quoted, or needed: the bars are concentration properties of the
field, pre-registered in the dossier (§3.B) and the gate (§2).

## 1. Hypothesis (one falsifiable sentence)

[HYPOTHESIS] The frozen Pythia-410m's layer-to-readout dynamical
sensitivity field {S_l}, l = 0…23 — the finite-difference estimator
of the layer-to-readout propagator norm ‖∂x_{24,last}/∂x_l‖ at the
final-token decision site — has localized structure (layer-Gini ≥ 0.4
with top-3 concentration outside the readout-adjacent span), giving a
dynamics-matched layer-targeting prior for the v_1 injection test;
if the field is uniform (Gini < 0.2), the "soft spot" premise is dead
and the model is dynamically homogeneous layer-wise.

### 1.1 Why this experiment exists

[INTERPRETATION] The program has measured *information*
(decodability) and *influence* (injection flips) but never
*sensitivity* — the third quantity a dynamical view needs first.
EXP127 CONTINUE'd (LOG-4698, bound): the frozen L20→L24 propagator
possesses a distinguished maximally-amplified direction v_1 with
median gain ratio R = 8.24 over random directions. The amplifier
exists *somewhere* — but DSF asks the question EXP127 could not:
where does sensitivity live layer-wise? If the non-normality
EXP086 measured (He ≈ 0.77, never followed up) is load-bearing, the
field should concentrate where the dynamics are most non-normal
(Kreiss intuition); if it is decorative, the field is flat and
dynamics-matched targeting has nothing to aim at. The 2026-09-28
sprint absorbed bandwidth into the S6 wave and never ranked a
sensitivity map; the 2026-09-29 paradigm-break sprint ranked it
Family B ("the map the loop needs"), and the gate (LOG-4702)
licensed this pre-registration. This is its signed form.

### 1.2 The generation-channel distinction (for Law #14's ruling)

[OPEN → for Law #14 to rule] The generation channel is dead *as a
measurement of content* (EXP115/116/123: P2/P5/P4 elicitation-as-
readout all terminal). DSF is **not generation-as-measurement**: it
generates nothing, decodes nothing, and reads no text. The protocol
perturbs the internal residual stream and measures L2 trajectory
divergence at the decision site — a finite-difference propagator
measurement. Per the dossier (§3.B), Law #14 must rule on this
distinction at review: the pre-reg's position is that the terminal
rule is unengaged because no content is ever read or elicited
(only norms of trajectory differences), and the Law-#7 argument
(§3.5) is that the isotropic δ carries no semantic content by
construction. If Law #14 rules otherwise, the pre-reg is returned,
not executed.

## 2. Exact question and the decision it changes

[QUESTION] Does the frozen Pythia-410m's dynamical sensitivity field
have localized structure (soft spots) or is it uniform across layers?

| Layer-Gini of {S_l} | Decision |
|---|---|
| **≥ 0.4** AND top-3 concentration layers **not all in {L21, L22, L23}** | **CONTINUE** — the field is structured with usable soft spots; it becomes the targeting map for the GPU v_1 injection test (EXP127's downstream pre-reg) and for Family C's closed-loop pursuit. |
| **≥ 0.4** but top-3 concentration **all in {L21, L22, L23}** | **KILL as independent family** — folds into Family A as a targeting note (the readout-adjacent span is already instrumented; DSF adds nothing independent). |
| **[0.2, 0.4)** | **HELD** — ambiguous structure; recorded, no re-test without a new gate. |
| **< 0.2** | **KILL** — the "soft spot" premise is dead: the model is dynamically homogeneous layer-wise, and dynamics-matched targeting has nothing to aim at. (The EXP127-licensed v_1 injection test still proceeds — it is licensed by EXP127's CONTINUE independently — but without a layer-targeting prior.) |

The top-3-concentration sub-bar is the dossier's pre-registered guard
against a trivial "the last layer is sensitive" CONTINUE (dossier
§3.B breaking point). The bars are Law #4 — verbatim from the gate
(LOG-4702 §2); no recalibration, no cross-field comparisons.

## 3. Method

### 3.1 Injection sites and the rest-of-model map

[DEFINITION] Pythia-410m has 24 transformer blocks (block indices
0…23). Injection sites are the residual-stream states:

- **L0** = post-embedding residual (input to block 0), final-token
  position;
- **Ll** = output of block (l−1), l = 1…23, final-token position;
- **Readout site** = x_{24,last}, the final-token residual at the
  input to the unembedding (post-final-LayerNorm), the same readout
  site every prior injection experiment used.

For site l, the rest-of-model map g_l runs blocks l…23 forward from
the (possibly perturbed) residual y_l to x_{24,last}. The site index
set is {L0…L23} (24 elements); the readout-adjacent span is
{L21, L22, L23}. {L21, L22, L23} denotes the three injection sites
nearest the readout under this §3.1 block-input indexing (the gate's
x_21/x_22/x_23 notation is superseded; no bar change).

### 3.2 Decision set

The 10 verbatim EXP107-bench prompts, canonical-order first 10, ids
`exp107_{flip,ctrl}_exp077_planet_2hop_{0..9}` — EXP127's decision
set. Prompts enter verbatim; no labels are used anywhere.

### 3.3 Perturbation definition

δ = ε·u, where:

- **ε = 1e-3**, absolute, in residual-space L2 norm — identical across
  ALL layers, items, and draws (breaking point (c)). The ε/2
  linearity check (§3.6), not the absolute value, is the arbiter of
  regime validity; a failed check → apparatus-void, never a retuned ε.
- **u** = isotropic unit vector in ℝ^1024: drawn from N(0, I_1024)
  via `torch.Generator` (`generator.manual_seed(per_triple_seed)`,
  torch 2.14.0+cpu) and normalized to unit L2 norm. Fresh draw per
  (item, layer, draw) from the seeded generator: base seed
  **20260929**; per-triple stream seed = `20260929 + item_idx·10^6 +
  layer·10^3 + draw` with draw indices 0-based (d ∈ {0, 1, 2, 3})
  (executor-computed, deterministic, Law #13). K = **4** draws per
  (item, layer). If S(ε) = 0 at a linearity-check point, that point
  counts as failed.

### 3.4 Field estimator

For each (item i, layer l, draw d):

    ratio_{l,i,d} = ‖ g_l(y_l + δ_{l,i,d}) − g_l(y_l) ‖₂ / ‖δ_{l,i,d}‖₂

The field element is the mean over the 40 (item × draw) samples:

    S_l = (1/40) Σ_{i=1..10} Σ_{d=1..4} ratio_{l,i,d}

S_l estimates the mean-random-direction gain (Frobenius-norm-related,
a lower bound on the spectral norm σ_1), not the spectral norm
itself; it is in the same layer-to-readout gain family EXP127's power
iteration measured at L20, not the same estimator.

All norms are Euclidean (L2) on the 1024-dim final-token residual.
Only the final-token trajectory is measured — **full-sequence
divergence is barred** (it confounds with other positions' content;
gate §3).

[OBSERVATION] The executor additionally records per-layer standard
errors over the 40 samples and a split-half (draws {0,1} vs {2,3})
Gini-stability diagnostic; no bar reads either — estimator health
only.

### 3.5 Law-#7 content-cleanliness argument

[ASSUMPTION → recorded] The isotropic δ is task-agnostic by
construction:

1. u carries no semantic content — it is a random direction in
   residual space, uncorrelated with any prompt, entity, or label;
   the seed discipline is public and content-independent.
2. The protocol never decodes, never reads generated text, and never
   computes any content-dependent statistic — only L2 norms of
   trajectory differences at the decision site. No label enters the
   apparatus (there are no labels anywhere in the protocol).
3. The generation-channel terminal rule (EXP115/116/123) covers
   *elicitation-as-readout* — DSF elicits nothing and reads no
   content, so the rule is unengaged (for Law #14's ruling, §1.2).

### 3.6 Linearity check (breaking point (b))

On a pinned subset — items {0, 4, 9} (canonical order) × layers
{L5, L11, L17, L23}, 12 check points — run the ε/2 arm (δ/2, same
seeds and draw indices) and reuse the main field's S(ε) at those
points. Require |S(ε/2) − S(ε)|/S(ε) ≤ 0.25 on ≥ 10 of the 12 check
points (≥ 80%, executor-computed). Fewer → apparatus-void. The ε/2
arm costs 3 × 4 × 4 = 48 forwards.

### 3.7 Guards and environment

- Backbone: frozen Pythia-410m, `AutoModelForCausalLM` (the EXP126
  loader lesson — LOG-331 is computed on the causal-LM state dict),
  `model.eval()`, `torch.no_grad()`, CPU, float32.
- Environment pinned in the manifest: torch 2.14.0+cpu,
  transformers 5.17.0, numpy 2.5.3, sklearn 1.9.1 (established env);
  threads pinned and read back.
- Δθ=0: LOG-331 pin
  `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed`
  before the first forward and after the last; mismatch →
  apparatus-void.
- Cost: 10 × 24 × 4 × 2 = **1920 forwards** (≈ 1–2h CPU, $0) +
  48 ε/2-check forwards. No autograd, no training, no labels.

### 3.8 What is NOT measured here

- No position-wise sensitivity (final-token site only).
- No content-conditioned sensitivity (isotropic δ only).
- No injection, no steering, no decision metric — the field is a
  propagator-norm measurement, not an intervention claim
  (S5-2's 4.87% bound constrains decision effects along
  semantic/static directions; it does not fence a gain-norm field —
  gate §4).

### 3.9 Raw-record hash-pin specification (defect class (b))

Before the Gini computation — and before any decision branch — the
executor hash-pins (SHA-256) the following raw artifacts. A Gini
minted without this pin → apparatus-void:

- per (item, layer, draw) finite-difference ratio records (field and
  ε/2 arms), with the associated δ seeds and δ-vector RNG metadata
  (§3.3);
- per-layer field elements S_l, l = 0…23, with per-layer standard
  errors (see §3.4 [OBSERVATION]);
- the S(ε/2) linearity-check values and the per-check-point
  pass/fail flags (§3.6);
- the environment manifest (torch/transformers/numpy/sklearn
  versions, thread count read back, backbone LOG-331 pin values
  pre/post);
- the append-only console log.

The pin is computed immediately after the linearity-check evaluation
passes and before the Gini is computed; the SHA-256 values are
recorded in the worksheet before the decision statistic exists.

## 4. Decision bars with statistical license

The decision statistic is the layer-Gini of {S_l} plus the top-3
concentration set (§0). Bars (Law #4, verbatim from the gate):

- **CONTINUE:** Gini **≥ 0.4** AND top-3 concentration layers **not
  all in {L21, L22, L23}** — structured field with usable soft
  spots; becomes the targeting map for the v_1 injection test and
  Family C's closed loop.
- **KILL as independent family:** Gini **≥ 0.4** but top-3 all
  readout-adjacent — folds into Family A as a targeting note.
- **HELD:** Gini **∈ [0.2, 0.4)** — ambiguous; recorded, no re-test
  without a new gate.
- **KILL:** Gini **< 0.2** — the soft-spot premise is dead; the
  model is dynamically homogeneous layer-wise. (EXP127's v_1
  injection test still proceeds independently, but without a
  layer-targeting prior.)

Statistical license: the bars are concentration properties of the
field itself, pre-registered in the dossier (§3.B) — no p-value is
computed or needed (defect class (a): the Gini is
executor-computed, never handwritten). The gate's quantitative
prediction bands (from program records only): decorative
non-normality → Gini < 0.2; load-bearing non-normality →
Gini ≥ 0.4 with top-3 in the mid-to-late band.

## 5. Falsification decision tree

All numbers executor-produced. Law #9 ordering: guards → backbone
pin → forward batches (field forwards + ε/2-check forwards, either
batch order) → linearity-check evaluation → raw-record hash-pin →
Gini → decision.

| Tree node | Required result |
|---|---|
| Bench provenance: 10 verbatim EXP107 prompts, ids `exp107_{flip,ctrl}_exp077_planet_2hop_{0..9}` | **PASS** — ids pinned, verbatim vs EXP107 bench |
| δ budget: ‖δ‖ = 1e-3 on all layers/items/draws (audited from raw records) | **PASS** — breaking point (c) |
| Backbone LOG-331 pin (pre) | **PASS** — `ec276abe…` |
| 1920 field forwards + 48 ε/2-check forwards (either batch order) | **DONE** — exit code 0 |
| ε/2 linearity-check evaluation (S(ε) reused from the field): ≥ 10/12 points within 25% | **PASS** — breaking point (b); check failure → apparatus-void before hash-pin |
| Backbone LOG-331 pin (post) | **PASS** — identical; Δθ=0 |
| Raw records hash-pinned before verdict (§3.9) | **PASS** — defect class (b) |
| **layer-Gini + top-3** | **§4 bars** — CONTINUE / KILL-as-family / HELD / KILL |

Any tree node miss → apparatus-void, hypothesis UNTESTED, no field
minted.

## 6. What this protocol explicitly does NOT do

- **No generation.** Nothing is generated, decoded, or elicited —
  perturbations are internal residual injections measured within a
  single forward pass. The generation-channel terminal rule is
  unengaged (for Law #14's ruling, §1.2).
- **No labels.** There is no label, target, or supervision anywhere.
- **No probe, no head, no training.** Nothing is fitted; the head-
  training family is untouched.
- **No logit channel.** [-3:] is N/A — no logit readout is used
  (defect class (e), stated explicitly).
- **No bench.** The 10 prompts are a decision set, not a bench —
  single-token entity assertion is N/A (defect class (f), stated
  explicitly). No treatment arms exist — per-item G1 is N/A (defect
  class (g), stated explicitly).
- **No injection.** No steering direction is applied to any decision;
  no decision metric is read.
- **No cross-field comparisons.** The field stands alone; generality
  beyond Pythia-410m and the 10 pinned prompts is barred.

## 7. Cost and honesty

1920 field forwards + 48 linearity-check forwards ≈ **1968
forwards**, ~1–2h CPU, **$0**. No autograd, no training, no labels,
no GPU. The honest reading either way: a structured field is the
targeting map the v_1 injection test and Family C need; a uniform
field is a publishable boundary fact (He ≈ 0.77 is decorative for
control purposes). The capability scoreboard stays at zero —
**still zero positive signals for autonomous steering.**

## 8. What DSF does NOT claim

- Not a capability. The field never becomes a steering claim by
  itself — a structured field refines *where* to inject; the
  injection test is a separate pre-registration.
- Not generality. One model (Pythia-410m), one decision set (10
  prompts), one site (final token).
- Not a mechanism account. The field measures sensitivity; it does
  not explain *why* sensitivity concentrates.
- A uniform-field KILL kills only the soft-spot premise — **not**
  the TGA program (EXP127's v_1 injection test is independently
  licensed), not non-normality as a descriptive fact.
- Novelty: N1 — Known Combination (§7.1.6 of the program record).

## 9. Deviations from the dossier and the gate (complete list)

1. **Dossier §3.B → gate §3:** the dossier's sketch compared two
   *completions* under a counterfactual prompt perturbation; the
   gate (and this pre-reg) use the **internal residual-perturbation
   finite difference** measured within a single forward pass.
   Reason: no generation occurs, so the Law-#7 story is cleaner and
   the generation-channel terminal rule is definitively unengaged.
   The decision-relevant trajectory (final token at x_{24,last}) is
   unchanged.
2. **Dossier "top-3 ≥ 50% of total S" → gate "Gini ≥ 0.4 AND
   top-3 not all readout-adjacent":** the gate's formulation is the
   binding one (Law #4); the dossier's top-3-share sketch is
   superseded.
3. **Dossier left K, ε, and the check subset open → gate pins:**
   K=4 draws, ε=1e-3 absolute, linearity check on items {0,4,9} ×
   layers {L5,L11,L17,L23} with the 25%/≥80% bar.
4. No other deviations. The gate's design assertions, bars, and
   breaking point are honored verbatim.

## 10. Boundary

- This pre-reg licenses a measurement only. **No injection along
  any layer of the field is licensed** — the v_1 injection test
  needs its own signed pre-registration.
- No generality beyond frozen Pythia-410m and the 10 pinned
  EXP107 prompts is licensed.
- The field is one scalar per layer at the final-token site only —
  it says nothing about position-wise sensitivity, content-
  conditioned sensitivity, or other read sites.
- The top-3 tie-break (lowest layer index) is a bookkeeping rule,
  not a scientific claim.
- If the ε/2 check fails, the apparatus is void — no smaller-ε
  rescue, no post-hoc regime argument.
- The seventh-item record (gate §7) stands: the constraining kills
  are snapshot-instrument, semantic-direction, or content-readout
  results; none ever measured layer-wise dynamical sensitivity;
  DSF is unfollowed and unproposed-before, never killed. H17, S5,
  H12, bench re-reading, EXP117/118/119/121/123/124 reruns,
  entity-name generation, H22's generality, H23's identity
  interpretation, and the TGA program stay dead (or, for TGA,
  CONTINUE'd and untouched).
