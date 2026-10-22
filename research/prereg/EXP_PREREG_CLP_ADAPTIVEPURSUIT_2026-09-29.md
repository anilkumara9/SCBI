# Pre-registration: CLP — Closed-Loop Adaptive Pursuit in the Frozen Pythia-410m Residual Stream

**Lane:** LOG-4711 (pre-assigned). **Family:** C of the paradigm-break
sprint (LOG-4693). **Gate:** LOG-4710 (PASS, conditional). **License:**
EXP127 (LOG-4698, bound CONTINUE — median R = 8.240640 ≥ 3, median
σ₁/σ₂ = 1.557689 ≥ 1.5 at the L20→L24 span: the dynamics-matched
amplifier exists *somewhere*, and its leading direction v_1 is a
measured object); EXP086 Stage A (LOG-331) (Henrici He = 0.7332–
0.8343, mean 0.7689 — non-normality is the existence condition for a
direction worth re-targeting toward).

**$0 CPU. Δθ=0 by construction.** This pre-registration licenses a
$0 CPU pilot only — **it is not a capability claim and no steering
is licensed by it.** The pilot measures *control efficiency*
(feedback gain per unit norm), not steering; it is the $0 gate for
the GPU closed-loop line (CLLC/EXP086-B), not a competitor to it.
A KILL here retires the adaptive-pursuit premise on $0 and is
recorded as adverse evidence against the GPU closed-loop line's
premise — it does **not** unlicense already-signed GPU bundles
(licenses are per-experiment; evidence updates priors).
Draft only; licenses nothing until the launch chain (independent
Law #14 review — whose channel-vs-dose ruling is the pre-launch
tripwire — → fix-verification → CEO launch decision → execution
under a minted number).

**Pre-reg decision record (prompt-set caveat, gate §3):** the decision
set is the 10 verbatim EXP107-bench prompts, canonical-order first 10
(ids `exp107_{flip,ctrl}_exp077_planet_2hop_{0..9}`) — the same
decision set as EXP127 and EXP128, so the three dynamics measurements
are directly comparable. **No larger prompt set is licensed by this
pre-reg.** Generality beyond the 10 pinned prompts is barred (§10).
The prompt count a future gate would target, if one is ever
commissioned, is named here for transparency (n=60, bench-disjoint),
but measuring it needs a new gate — it is not licensed here.

---

## 0. The breaking point (read first)

Conjunctive. Any miss → **apparatus-void, hypothesis UNTESTED**
(Law #9 ordering: guards → backbone pin → forward batches →
validity-check evaluation (budget audit + sensing-discipline assert
+ correction-rule pin) → raw-record hash-pin → displacement metric
→ decision):

(a) **Δθ=0** — backbone LOG-331 parameter hash
    `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed`
    pinned before the first forward and re-pinned after the last
    forward; any mismatch → apparatus-void.
(b) **Norm-budget matching** — the budget is the *component
    structure* (pinned, §3.3; FIX-4, Law #14 LOG-4712):
    ‖δ₁‖ = ‖c‖ = ‖δ_open‖ = B/2, ‖δ_single‖ = B, each within
    float32 tolerance of the recorded B. The executor audits the
    component structure per arm per item from the raw records;
    the injected norms (‖δ₂‖ = ‖δ₁+c‖, ‖δ₁+δ_open‖,
    ‖δ_single‖) are recorded per (item, arm) as observations —
    they satisfy ‖·‖ ≤ B by the triangle inequality, so the loop
    arm can never win on dose. Any arm violating the component
    structure → apparatus-void (the ratio would measure the
    budget, not the feedback). This is the dose-fence made
    mechanical (launch condition 1).
(c) **ε-discipline (learned from EXP128)** — the loop's sensing step
    may NOT assume the finite-difference linear regime at ε=1e-3
    that EXP128's breaking point killed (1/12 within 25%). This
    protocol uses gate §6(c) option (i): **exact-JVP/adjoint sensing
    via autograd** — EXP127's Law-#14-licensed apparatus, never
    finite differences. The executor asserts the *absence* of any
    finite-difference sensing term (no ‖g(y+δ)−g(y)‖/‖δ‖ used as a
    sensing input anywhere); the closed-loop correction uses the
    measured displacement d₁ and the exact local adjoint only
    (§3.5). Any finite-difference sensing detected in the executor
    → apparatus-void. The executor's sensing-discipline assert is
    the §3.5 whitelist/blacklist enumeration (FIX-3): d̂₁ direction
    whitelisted, finite-difference gain ratios blacklisted. EXP128 killed a *sensing instrument*, not
    feedback — its failure does not transfer here because its
    apparatus is absent from this protocol (launch condition 2).
(d) **Frozen correction rule** — the map d₁ → correction is the
    protocol's §3.4 formula, identical for all items; any per-item
    tuning of the tuner → apparatus-void (Law #4; launch
    condition 4).
(e) **No training, no weight mutation** — pure forwards through a
    frozen model in eval mode (`model.eval()`, `torch.no_grad()`
    for the forward passes; autograd used *only* for
    Jacobian-vector / vector-Jacobian products at frozen weights,
    never for a backward pass into parameters); the executor
    contains no optimizer and no loss.

[DEFINITION] The decision statistic is the **feedback-gain ratio**:

    r_i = (‖d₂,i‖ / B) / max(‖d_sum,i‖ / B, ‖d_single,i‖ / B),  i = 1…10

where d₂,i is the readout-site displacement of the closed-loop
2-step arm, d_sum,i of the open-loop 2-step sum arm, d_single,i of
the single-shot arm, and B the pinned total norm budget. The
registered decision statistic is the **median of r_i over the 10
items** — paired per item, continuous, executor-computed. No
p-value is computed, quoted, or needed: the bars are ratio
properties of the measurement, pre-registered in the gate (§2).
Decision-statistic flips (EXP107 bench) are recorded as
[OBSERVATION] only; no bar reads them (EXP094's zero-flip floor
makes flips a degenerate primary metric — a bar on a metric that
sits at zero is not a bar).

## 1. Hypothesis (one falsifiable sentence)

[HYPOTHESIS] In the frozen Pythia-410m, state-feedback re-targeting
of a perturbation — computing the second step from the measured
trajectory response d₁ to the first — moves the final-token residual
further per unit norm (median r ≥ 2 over the 10 pinned prompts)
than any norm-matched open-loop injection spending the same budget;
if the loop buys no displacement the budget didn't already buy
(median r ≤ 1.2), the adaptive-pursuit premise is dead on $0.

### 1.1 Why this experiment exists

[INTERPRETATION] Every dead injection in the program's history was
open-loop: inject a fixed direction once, read once (EXP077's cones,
EXP093's shared direction, EXP094's 120 L11 arms, the S5-2 dose
sweeps, EXP095/96/97). The frontier's working form is closed-loop
(Activation-LQR: u_t = −Kx_t, recomputed from the evolving state,
tracking-error bounds, no training). "Closed-loop" in a frozen
deterministic model means **sequential sense-act forwards within one
evaluation**: forward with δ₁, measure d₁ at the readout site,
compute δ₂ = δ₁ + correction(d₁) under a rule frozen in the
pre-reg (no adaptive tuning of the tuner — Law #4), forward again
with δ₂, measure d₂. The second perturbation is a *function of
measured state*, not a pre-registered constant. That is the whole
difference from every dead lane, and it is the only difference this
family is allowed to claim. The discriminant — the per-norm ratio of
feedback vs norm-matched open-loop — was never measured by any
killed lane, so Law #4 licenses it as a new channel, not a tweak —
*conditional* on the norm-matching proof (§3.4, breaking point (b))
and on Law #14 affirming adaptation ≠ dose at review (§1.2).

### 1.2 The channel-vs-dose distinction (for Law #14's ruling)

[OPEN → for Law #14 to rule] The dossier's own tripwire: if the
pre-reg arrived with semantic directions + feedback + no norm
control, it would be EXP077/EXP094 with a bolt-on and must never
launch. The pre-reg's position is that the norm-budget matching
(breaking point (b)) makes the dose-fence mechanical — every arm
spends exactly B, so the ratio cannot be read as "a bigger push" —
and that the injected directions are dynamics-sensed, not semantic
(§3.3; launch condition 3). If Law #14 rules adaptation = dose, the
family never launches (pre-launch kill, recorded; gate §2).

## 2. Exact question and the decision it changes

[QUESTION] Does state-feedback re-targeting of an injection move
the residual further per unit norm than any open-loop injection
the program has tried, at matched norm budget?

| Median per-item ratio r (closed-loop / best open-loop arm) | Decision |
|---|---|
| **≥ 2** | **CONTINUE** — feedback has causal value per unit norm in a frozen model; the $0 gate for the GPU closed-loop line (CLLC/EXP086-B) passes. |
| **≤ 1.2** | **KILL** — the adaptive-pursuit premise on $0; the loop adds nothing the push didn't already do. Recorded as adverse evidence against the GPU closed-loop line's premise; does not unlicense signed bundles. |
| **(1.2, 2)** | **HELD** — recorded, no re-test without a new gate. |
| **Saturation:** median ‖d₂−d₁‖/‖d₁‖ ≤ 0.1 (the correction buys no displacement regardless of rule) | **KILL** — feedback cannot buy displacement the dynamics won't sell (EXP128's threshold intuition realized). |
| **Law #14 rules adaptation = dose** | **Never launches** — pre-launch kill, recorded. |

The open-loop *sum* arm specifically tests the dose-in-disguise
reading: if the closed-loop arm matches the open-loop sum
(median ‖d₂‖/‖d_sum‖ ≤ 1.2) while both beat the single shot, the
"feedback" was just a second push — KILL, and the correction rule
is recorded as dose in disguise (gate §8, reading (5)). The bars
are Law #4 — verbatim from the gate (LOG-4710 §2); no
recalibration, no cross-experiment comparisons.

## 3. Method

### 3.1 Injection site and the rest-of-model map

[DEFINITION] Injection at **L20** — the output of block 19,
final-token position (the EXP127 amplifier site; the
dossier-licensed dynamics-matched span). The readout site is
x_{24,last}, the final-token residual at the input to the
unembedding (post-final-LayerNorm) — the same readout site every
prior injection experiment used. For injection y_{20}, the
rest-of-model map g runs blocks 20…23 forward to x_{24,last}.

### 3.2 Decision set

The 10 verbatim EXP107-bench prompts, canonical-order first 10, ids
`exp107_{flip,ctrl}_exp077_planet_2hop_{0..9}` — EXP127's and
EXP128's decision set. Prompts enter verbatim; no labels are used
anywhere.

### 3.3 Perturbations: dynamics-sensed directions only (launch condition 3)

No semantic, task, or concept direction enters this protocol —
EXP077/EXP093/EXP094 are the kills this avoids resurrecting.

- **v̂₁,i** — the per-prompt leading right singular vector estimate
  of the frozen L20→L24 propagator, from EXP127's power-iteration
  apparatus. Expected artifact: `experiments/runs/EXP127_tga/out/exp127_vectors.npz`
  (EXP127 report artifact table: "v₁ per prompt + 64 direct uⱼ per prompt,
  float32"), SHA-256
  `9b527c026d0ee307192725429f655e628f403505343dc018de3cfe15db6113dc`
  (FIX-5, Law #14 LOG-4712). The executor re-pins before the first
  forward and verifies BOTH (i) the artifact hash matches, and (ii)
  per-prompt id alignment: all 10 decision-set ids
  `exp107_{flip,ctrl}_exp077_planet_2hop_{0..9}` are present as
  `v1__<prompt_id>` keys — a directory hash match alone is not
  alignment. Hash mismatch or id misalignment → apparatus-void.
  Dynamics-sensed: it is the direction the model's *own* dynamics
  maximally amplify, measured at the L20→L24 span (median
  R = 8.240640).
- **v̂₂,i** — EXP127's pinned second singular vector estimate
  (σ₁/σ₂ = 1.557689 ≥ 1.5: a distinguished second direction
  exists). Used only as the pre-registered non-adaptive second
  direction of the open-loop sum arm — the honest "second push"
  control.
- **Budget B** — pinned absolute norm in residual-space L2, tied
  to the L20 residual-norm scale (FIX-2, Law #14 LOG-4712): B =
  0.01 × median ‖y_{20,last}‖ over the 10 pinned prompts. The 1%
  fraction is pre-registered, not executor-chosen; the absolute
  B is computed by the executor from the base forwards and
  recorded in the worksheet BEFORE the first perturbed forward,
  and the executor asserts the recorded B there. The fixed
  fraction removes the degree of freedom the saturation branch
  is sensitive to: B can be neither ≫ the residual norm (which
  would force the saturation KILL) nor → 0 (which would force
  noise). Identical across all arms, items, and draws.
  δ₁,i = (B/2)·v̂₁,i. Breaking point (b) audits every arm to the
  recorded B (component structure, §3.4).

#### 3.3.1 Erratum (LOG-4714): v̂₂,i derivation provenance

[CORRECTION — provenance only; no design change.] EXP127's run-dir
artifact `experiments/runs/EXP127_tga/out/exp127_vectors.npz` holds
only `v1__` + `urand__` keys (verified at LOG-4713; the "pinned second
singular vector estimate" named in §3.3 above has no stored artifact).
v̂₂,i is therefore DERIVED at execution time — not re-pinned — by the
following deterministic procedure, using the same frozen L20→L24
propagator and the Law-#14-licensed exact-JVP apparatus EXP127 used:

- **Seed pinned:** `20260929_4714`, via `torch.Generator().manual_seed`.
- **Procedure (per prompt, once, BEFORE the first perturbed forward):**
  orthogonalized power iteration on the deflated operator — iterate

  q_{k+1} ∝ (I − v̂₁,i v̂₁,iᵀ) MᵀM q_k, normalized to unit norm,

  with q_0 drawn from the pinned generator; a fixed iteration count K
  (same K for every prompt, recorded in the worksheet) — equivalently,
  power iteration on M₂ = M − σ̂₁û₁v̂₁,iᵀ, the propagator deflated
  against the re-pinned leading right singular vector. MᵀM is applied
  via the exact JVP/VJP apparatus licensed by EXP127.
- **Orthogonality assert:** |v̂₂,iᵀ v̂₁,i| < 1e-6; miss →
  apparatus-void.
- **Recording:** v̂₂,i written to the worksheet under keys
  `v2__<prompt_id>` for the 10 pinned decision-set ids, and their
  SHA-256 folded into the §3.8 raw-record hash-pin. Law #4 provenance
  is satisfied: deterministic given the pinned seed, the pinned EXP127
  apparatus, and the frozen backbone.
- The open-loop sum arm (§3.4) then uses δ₁ + δ₂ with δ₂ along v̂₂,i,
  norm-matched per breaking point (b).

No other section changed; the seven Law #14 fixes (LOG-4712/4713) are
byte-frozen.

### 3.4 Arms (norm-budget-matched; the dose-fence made mechanical)

Total budget B per arm, per item. All norms Euclidean (L2) on the
1024-dim final-token residual.

- **Closed-loop 2-step (the loop):** forward with δ₁,i = (B/2)·v̂₁,i
  at L20; measure d₁,i = g(y_{20}+δ₁,i) − g(y_{20}) at x_{24,last};
  compute the correction c_i = (B/2)·ŵ_i under the **frozen
  correction rule** (§3.5); forward again with
  δ₂,i = δ₁,i + c_i at L20 (fresh forward from the unperturbed
  base — the "second act"); measure d₂,i. ‖δ₁,i‖ + ‖c_i‖ = B
  exactly.
- **Open-loop 2-step sum (the dose-in-disguise control):** forward
  with δ₁,i + δ_open,i where δ_open,i = (B/2)·v̂₂,i is
  pre-registered (no feedback — v̂₂ is fixed before any forward);
  total norm B; measure d_sum,i. If the loop's correction were
  "just a second push," this arm matches it.
- **Single shot (the best-open-loop reference):** forward with
  δ_single,i = B·v̂₁,i (the full budget in the best pre-registered
  dynamics-sensed direction); measure d_single,i.

Norm audit (FIX-4): the executor audits the *component structure*
— ‖δ₁‖, ‖c‖, ‖δ_open‖ (each B/2 within float32 tolerance of the
recorded B), ‖δ_single‖ (= B) — per (item, arm), and records the
injected norms ‖δ₂‖ = ‖δ₁+c‖, ‖δ₁+δ_open‖, ‖δ_single‖ as
observations; any deviation from the pinned component structure
beyond float32 tolerance → apparatus-void (breaking point (b)
keyed to components, not to the injected norms — "every arm spends
exactly B" is ambiguous for the loop arm as written, where
‖δ₂‖ ≤ B by the triangle inequality).

### 3.5 Sensing and the frozen correction rule (launch conditions 2, 4)

**Sensing instrument: exact-JVP/adjoint via autograd** —
EXP127's Law-#14-licensed apparatus. The executor uses
Jacobian-vector and vector-Jacobian products of the frozen
L20→L24 map at frozen weights; **no finite-difference sensing
appears anywhere in the protocol** — EXP128's killed apparatus
(1/12 within 25% at ε=1e-3) is absent, so its failure does not
transfer (gate §6(c), option (i)). The measured displacement d₁
is a direct finite displacement (forward difference of two
forwards), never a linearity claim; the correction rule invokes
no linear-regime assumption.

**Frozen correction rule** (pre-registered, identical for all
items — Law #4; launch condition 4): let d̂₁ = d₁/‖d₁‖ and let
M be the exact L20→L24 Jacobian at the base point; then

    ŵ = Mᵀd̂₁ / ‖Mᵀd̂₁‖   (adjoint re-targeting: the injection
                          direction that maximally amplifies
                          along the measured response direction)

    c = (B/2)·ŵ

with the guard: if ‖Mᵀd̂₁‖ = 0 (pathological), ŵ falls back to
v̂₁ (executor-logged; the item is flagged, not dropped — the
ratio is computed on the recorded values). The rule is a closed
form of measured state plus the exact local adjoint — no
per-item tuning, no learned parameters, no adaptation of the
tuner. Any per-item rule modification by the executor →
apparatus-void (breaking point (d)).

**Sensing-discipline assert, enumerated (FIX-3, Law #14
LOG-4712) — the executor's mechanically checkable assert:**
WHITELISTED — the finite-displacement *direction*
d̂₁ = d₁/‖d₁‖ as the feedback input to the frozen correction
rule; the measured displacement d₁ used as a direction only,
never as a linearity claim or an amplification estimate.
BLACKLISTED — any finite-difference *gain ratio* ‖Δ‖/‖δ‖
used as an amplification estimate or as an input to the
sensing step; any use of a finite-difference ratio as a
linearity or gain claim about the residual map. The feedback
signal d₁ *is* a finite displacement — that is what the
whitelist covers; the blacklist is what breaking point (c)
polices.

### 3.6 Guards and environment

- Backbone: frozen Pythia-410m, `AutoModelForCausalLM` (the EXP126
  loader lesson — LOG-331 is computed on the causal-LM state
  dict), `model.eval()`, CPU, float32. Autograd enabled *only*
  for JVP/VJP sensing at frozen weights; no backward pass into
  parameters; no optimizer, no loss, no weight mutation.
- Environment pinned in the manifest: torch 2.14.0+cpu,
  transformers 5.17.0, numpy 2.5.3 (established env); threads
  pinned and read back.
- Δθ=0: LOG-331 pin
  `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed`
  before the first forward and after the last; mismatch →
  apparatus-void.
- Cost: 10 items × 5 forwards (1 base + 2 loop + 1 open-loop sum
  + 1 single) = **50 forwards** + ~10 VJPs for the adjoint sensing
  (FIX-6, Law #14 LOG-4712 — the "10 × 3 × 2 = 60" formula
  overcounted the estimator-required forwards) ≈ ~2h CPU, **$0**.
  No training, no labels, no GPU.

### 3.7 What is NOT measured here

- No semantic-direction arms (EXP077/EXP094 territory — barred).
- No decision-statistic bars — flips are [OBSERVATION] only
  (defect class (a) discipline: the continuous ratio is the
  registered statistic).
- No generation, no decoding, no content read — only L2 norms of
  trajectory differences at the decision site. The
  generation-channel terminal rule (EXP115/116/123) is unengaged.
- No ε/2 linearity check — there is no finite-difference
  estimator in this protocol; EXP128's gate does not apply as an
  instrument check (its lesson is carried as breaking point (c),
  the sensing-discipline assert).

### 3.8 Raw-record hash-pin specification (defect class (b))

Before the ratio computation — and before any decision branch —
the executor hash-pins (SHA-256) the following raw artifacts. A
ratio minted without this pin → apparatus-void:

- per (item, arm) records: δ vectors (seeds/metadata for v̂₁/v̂₂
  re-pinning, the measured d₁ vectors, the computed correction
  vectors c, the final δ₂ vectors), per-arm norm audit values;
- per (item, arm) displacement vectors and norms
  (d₂, d_sum, d_single) at x_{24,last};
- the adjoint-sensing diagnostics (‖Mᵀd̂₁‖ per item, fallback
  flags);
- the environment manifest (versions, thread count read back,
  backbone LOG-331 pin values pre/post, v̂₁/v̂₂ artifact hashes);
- the append-only console log.

The pin is computed immediately after the validity checks pass
and before the median ratio is computed; the SHA-256 values are
recorded in the worksheet before the decision statistic exists.

## 4. Decision bars with statistical license

The decision statistic is the median over the 10 items of the
per-item feedback-gain ratio r_i (§0). Bars (Law #4, verbatim
from the gate):

- **CONTINUE:** median r **≥ 2** — feedback has causal value per
  unit norm; the $0 gate for the GPU closed-loop line passes.
- **KILL:** median r **≤ 1.2** — the loop adds nothing the push
  didn't already do; the adaptive-pursuit premise on $0 is dead.
  Recorded as adverse evidence against the GPU closed-loop
  line's premise; does not unlicense signed bundles.
- **KILL (saturation):** median ‖d₂−d₁‖/‖d₁‖ **≤ 0.1** — the
  correction buys no displacement regardless of rule; feedback
  cannot buy displacement the dynamics won't sell.
- **KILL (dose in disguise):** median ‖d₂‖/‖d_sum‖ **≤ 1.2**
  while the loop beats the single shot — the "feedback" was a
  second push; the correction rule is recorded as dose in
  disguise.
- **HELD:** median r **∈ (1.2, 2)** — recorded, no re-test
  without a new gate.

**Evaluation precedence (FIX-1, Law #14 LOG-4712):** the two premise
KILL branches — saturation and dose-in-disguise — are evaluated
FIRST; they test the family premise ("feedback bought displacement")
directly. A procedure that wins on the first push alone does not
license the feedback premise. The median-r bars (CONTINUE ≥ 2,
KILL ≤ 1.2, HELD) apply only if neither premise-KILL fires. This
resolves the co-fire corner where ‖d₁‖ ≥ 2× the best open-loop arm
while d₂ ≈ d₁ (both the ≥2 ratio and the ≤0.1 saturation statistic
hold — opposite verdicts, no precedence without this rule).

Statistical license: the bars are ratio properties of the
measurement itself, pre-registered in the gate (§2) — no p-value
is computed or needed (defect class (a): the median ratio is
executor-computed, never handwritten). The gate's quantitative
prediction bands (from program records only): null (loop adds
nothing) → r ≤ 1.2; CLP hypothesis → r ≥ 2, the smallest ratio
that cannot be explained by "the correction happened to add norm
in a good direction" (the open-loop sum arm controls exactly
that).

## 5. Falsification decision tree

All numbers executor-produced. Law #9 ordering: guards →
backbone pin → forward batches (batch order free across
items/arms; the loop arm's sense→act sequence — forward-1 →
measure d₁ → compute c → forward-2 from the unperturbed base —
is fixed, FIX-7) → validity-check evaluation (norm-budget audit
+ sensing-discipline assert + correction-rule pin) →
raw-record hash-pin → displacement metric → decision.

| Tree node | Required result |
|---|---|
| Bench provenance: 10 verbatim EXP107 prompts, ids `exp107_{flip,ctrl}_exp077_planet_2hop_{0..9}` | **PASS** — ids pinned, verbatim vs EXP107 bench |
| v̂ artifact re-pin: `exp127_vectors.npz` SHA-256 `9b527c…13dc` + all 10 decision-set ids present as `v1__<prompt_id>` keys | **PASS** — per-prompt id alignment (FIX-5); hash mismatch or id misalignment → apparatus-void |
| Norm budget: component structure ‖δ₁‖=‖c‖=‖δ_open‖=B/2, ‖δ_single‖=B per item (float32 tolerance), audited from raw records | **PASS** — breaking point (b) keyed to components (FIX-4); violation → apparatus-void before hash-pin |
| Sensing discipline: §3.5 whitelist/blacklist assert (d̂₁ direction allowed; finite-difference gain ratios barred) | **PASS** — breaking point (c) (FIX-3); violation → apparatus-void |
| Correction rule: protocol §3.5 formula, identical all items | **PASS** — breaking point (d); per-item tuning → apparatus-void |
| Backbone LOG-331 pin (pre) | **PASS** — `ec276abe…` |
| 50 forwards + ~10 VJPs for adjoint sensing (FIX-6); batch order free across items/arms, loop-arm sense→act sequence fixed (FIX-7) | **DONE** — exit code 0 |
| Backbone LOG-331 pin (post) | **PASS** — identical; Δθ=0 |
| Raw records hash-pinned before verdict (§3.8) | **PASS** — defect class (b) |
| Evaluation precedence: saturation and dose-in-disguise KILLs evaluated FIRST; median-r bars apply only if neither fires | **PASS** — premise-KILLs take precedence (FIX-1) |
| **Median per-item ratio r** | **§4 bars** — CONTINUE / KILL / KILL(saturation) / KILL(dose-in-disguise) / HELD |

Any tree node miss → apparatus-void, hypothesis UNTESTED, no
ratio minted.

## 6. What this protocol explicitly does NOT do

- **No semantic directions.** No concept vector, bridge direction,
  task normal, or label-informed construction enters any arm
  (EXP077/EXP094 kills honored; Law #4 channel discipline).
- **No dose tweak.** The norm-matching (breaking point (b)) is the
  mechanical proof that direction-adaptation ≠ dose; the open-loop
  sum arm is the control that would catch a dose reading.
- **No generation.** Nothing is generated, decoded, or elicited;
  no text is read. The generation-channel terminal rule is
  unengaged (for Law #14's ruling, §1.2).
- **No labels.** There is no label, target, or supervision anywhere.
- **No probe, no head, no training.** Nothing is fitted.
- **No logit channel.** No logit readout is used (defect class (e),
  stated explicitly).
- **No bench.** The 10 prompts are a decision set, not a bench —
  single-token entity assertion is N/A (defect class (f), stated
  explicitly). No treatment arms exist beyond the three registered
  ones — per-item G1 is N/A (defect class (g), stated explicitly).
- **No finite differences.** EXP128's killed apparatus is absent
  from this protocol (breaking point (c)).
- **No cross-field comparisons.** The ratio stands alone;
  generality beyond Pythia-410m and the 10 pinned prompts is
  barred.

## 7. Cost and honesty

50 forwards + ~10 VJPs ≈ **~2h CPU, $0**. No training, no
labels, no GPU. The honest reading either way: a ≥2× ratio is the
first licensed evidence that dynamics-first feedback control has
causal value per unit norm in a frozen model — the $0 gate the
GPU closed-loop line needs; a KILL retires the adaptive-pursuit
premise on $0 as a publishable boundary fact (feedback does not
beat the push at this scale).

**Honest frame (verbatim):** this is a control-efficiency
question, not a capability claim — capability scoreboard stays at
zero; a CLP KILL is adverse evidence against the GPU closed-loop
line's premise but does not unlicense signed bundles; no
injection here is autonomous steering.

## 8. What CLP does NOT claim

- Not a capability. The ratio never becomes a steering claim —
  feedback gain refines *how* to push; the GPU injection program
  is a separate pre-registration.
- Not generality. One model (Pythia-410m), one decision set (10
  prompts), one site (L20 → x_{24,last}).
- Not a mechanism account. The ratio measures feedback gain; it
  does not explain *why* the adjoint re-targeting works or fails.
- Not a resurrection. EXP077, EXP093, EXP094, S5-2, EXP095/96/97,
  G1, EXP115/116/123, EXP125 (H22), EXP126 (H23) stay dead; TGA
  (EXP127) stays CONTINUE'd and is not re-gated; DSF (EXP128)
  stays UNTESTED — CLP assumes nothing about the field.
- Novelty: N1 — Known Combination (§7.1.6 of the program record).

## 9. Deviations from the dossier and the gate (complete list)

1. **Dossier §3.C → gate §3 → this pre-reg §3.4/3.5:** the
   dossier's sketch ("inject δ₁ at L20, read displacement at L24,
   re-target δ₂ = δ₁ + correction") left the correction rule and
   the sensing instrument open; the gate froze the
   norm-budget-matched arms and named the three sensing options;
   this pre-reg pins option (i) exact-JVP/adjoint sensing with
   the §3.5 formula. Reason: EXP128 killed finite-difference
   sensing at ε=1e-3, and EXP127's exact-JVP apparatus is the
   only Law-#14-licensed sensing instrument in the program.
2. **Dossier "displacement-per-norm ≥ 2×, McNemar on flips" →
   gate §2:** flips demoted to [OBSERVATION] (EXP094's zero-flip
   floor); the continuous median ratio r is the binding statistic.
   The gate's formulation is binding (Law #4).
3. **Dossier left the open-loop controls as "fixed-δ and δ₁+δ₂
   open-loop sum" → gate §3 → this pre-reg §3.4:** the open-loop
   sum uses the pinned v̂₂ (not an arbitrary fixed δ₂) so the
   "second push" is the strongest honest dose control the
   dynamics measurements license.
4. No other deviations. The gate's design assertions, bars,
   breaking point, and seventh item are honored verbatim.

## 10. Boundary

- This pre-reg licenses a $0 CPU pilot only. **No GPU contact,
  no steering claim, no autonomous capability** is licensed.
- No generality beyond frozen Pythia-410m and the 10 pinned
  EXP107 prompts is licensed.
- The ratio is one scalar per item at the L20 → x_{24,last}
  span only — it says nothing about other spans, positions, or
  read sites.
- If any breaking-point item fails, the apparatus is void — no
  smaller-ε rescue, no post-hoc regime argument, no rule
  re-tuning.
- The seventh-item record (gate §7) stands: the constraining
  kills are snapshot-instrument, semantic-direction, or
  content-readout results; none ever measured feedback gain;
  CLP is unfollowed in this form and never killed. H17, S5, H12,
  bench re-reading, EXP117/118/119/121/123/124 reruns,
  entity-name generation, H22's generality, H23's identity
  interpretation, the TGA program (CONTINUE'd), and the DSF
  soft-spot premise (UNTESTED) stay dead (or untouched, as
  marked).
