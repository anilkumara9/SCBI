# Pre-registration: DGF — ε-Free Directional-Gain Field of the Frozen Pythia-410m Layer-to-Readout Map

**Lane:** LOG-4738 (pre-assigned). **Family:** B (DSF) — currently UNTESTED (EXP128 RUN-INVALID, apparatus-void). **Gate:** LOG-4737 (PASS-conditional; memo `research/strategy/DGF_GATE_2026-09-29.md`). **Design-study basis:** LOG-4736, `research/analysis_plans/DSF_APPARATUS_REDESIGN_STUDY_2026-09-29.md`.

**$0 CPU. Δθ=0 by construction.** This pre-registration licenses a **dynamics-characterization measurement only (EXP127-class)** — **no targeting claim is licensed by it.** Any injection-targeting use of the measured field needs its own experiment number, its own worth-it reasoning, and its own bars. **Draft only; licenses nothing** until the launch chain (Law #14 review → fix-verification → CEO launch decision → execution under a minted number, EXP132-class).

**The five gate conditions (LOG-4737 §9) are carried verbatim below:**
1. **Condition 1** — §1/§7: licensed as dynamics characterization only; any targeting claim → Law #14 REJECT.
2. **Condition 2** — §4: null-contrast design, ΔGini = Gini_sem − Gini_iso, margin 0.2, registered verbatim — no raw-Gini bar.
3. **Condition 3** — §0(b)/§3.3: multi-ε float64 convergence diagnostic (ε ∈ {1e-6, 1e-7, 1e-8}, F(ε) → JVP required) is the breaking point — non-convergence → apparatus-void, never a verdict.
4. **Condition 4** — §3.1: semantic probe set registered by provenance (EXP077's archived support set, deterministic reconstruction recipe) with the derived-vector SHA-256 recorded pre-JVP — no floating probe selection.
5. **Condition 5** — §7: novelty N1 — Known Combination.

---

## 0. The breaking point (read first)

Conjunctive. Any miss → **apparatus-void, hypothesis UNTESTED, no ΔGini minted** (Law #9 ordering: guards → backbone pin → probe/hash pins → convergence diagnostic → JVP batches → validity checks → raw-record hash-pin → metric (ΔGini) → decision):

(a) **Δθ=0** — backbone LOG-331 parameter hash
    `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed`
    pinned before the first JVP and re-pinned after the last;
    any mismatch → apparatus-void.
(b) **Convergence before reading** — the §3.3 multi-ε float64
    convergence diagnostic passed on ≥ 8/10 prompts (diagnostic
    subset: probes × layers {0, 11, 23} per prompt; a prompt with any
    failing diagnostic is excluded from the decision set, with
    disclosure; fewer than 8 diagnostic-passing prompts →
    apparatus-void — the instrument failed, never a verdict).
(c) **Registered probes only** — the semantic probe vectors are the
    deterministic reconstruction of EXP077's archived support set
    (§3.1); their SHA-256 is recorded in the environment manifest
    before the first JVP; any floating or hand-selected probe →
    apparatus-void. [CONDITION 4]
(d) **No ε in the executor** — the sensing primitive is forward-mode
    AD (`torch.autograd.functional.jvp`) exclusively; no finite
    difference appears anywhere (grep-verifiable at review). The
    ε-values in §3.3 exist only inside the convergence *diagnostic*,
    which is verdict-immaterial.
(e) **No training, no weight mutation** — pure autograd JVPs through
    a frozen model in eval mode; the executor contains no optimizer,
    no loss, no backward pass into weights.

[DEFINITION] The decision statistic is the **median ΔGini over the
decision set** (diagnostic-passing prompts, n_d ≥ 8 required, else
apparatus-void per (b)), where per prompt i:
ΔGini_i = Gini_sem_i − Ḡini_iso_i (§4), with Ḡini_iso_i the
per-probe-median of the 8 isotropic Gini coefficients Gini_iso_ij
(probe-symmetric null; E[ΔGini] = 0 under H0 by symmetry). For even
n_d the median is
executor-computed as the average of the two middle order statistics;
for odd n_d it is the middle order statistic. The median Ḡini_iso
(per-probe-median of 8 Gini_iso_ij, then median over the decision
set) is the KILL-as-premise check (§5).
No p-value is computed, quoted, or needed — the verdict is read from
the executor-computed median against the registered bars.

## 1. Hypothesis (one falsifiable sentence)

[HYPOTHESIS] The exact (autograd-JVP) directional gain of frozen
Pythia-410m's full layer-to-readout map, evaluated along fixed
semantic probe directions, concentrates at specific layers beyond the
smooth isotropic null profile — i.e., direction-specific soft spots
exist in the infinitesimal dynamics — quantified by median ΔGini ≥
0.2 across 10 bench prompts.

### 1.1 Why this experiment exists

[INTERPRETATION] Family B's original mission — the layer-targeting
map for injection — stays UNTESTED and unlicensed; this apparatus
does not revive it (LOG-4736 §0, gate LOG-4737). What this experiment
licenses is a dynamics-characterization measurement (EXP127-class):
the layer dimension of directional gain, which no licensed experiment
has produced. EXP128 asked the same scientific question with a finite-
difference instrument; its linearity check (1/12 within 25% of
required 10/12) proved the instrument measured amplification-driven
transition saturation, not the propagator norm — the estimand was the
saturated jump, never the derivative (LOG-4736 §1: the linear regime
ends below t* ≈ 5e-4, *by construction*, shrunk by the very transient
amplification DSF hunted). The JVP apparatus computes S_l^* =
lim_{ε→0} S_l(ε) directly — the very quantity EXP128's estimator was
trying to approximate — and the saturation-remainder failure mode is
inexpressible in AD, which has no remainder term.

### 1.2 Characterization-only framing [CONDITION 1]

[ASSUMPTION] The JVP exactly measures the *infinitesimal* gain. The
linear regime ends below 5e-4; any feasible injection budget is
~0.1–0.3 (EXP131's B = 1% of ‖y‖). The derivative characterizes a
regime 3+ orders of magnitude below any intervention. As a TARGETING
map (which layer to inject at), the JVP field is the wrong object:
the layer maximizing infinitesimal gain need not maximize finite-
budget response, and the saturated regime — where injection actually
operates — is invisible to it. **The license covers dynamics
characterization only.** EXP127's R = 8.24 is precedent that
infinitesimal characterizations are publishable boundary facts. Any
targeting claim built on the measured field → Law #14 REJECT at
review of the downstream pre-registration. A CONTINUE here licenses
further characterization — it is **not** a targeting claim, **not**
a steering claim, and does **not** move the capability scoreboard
(still zero positive signals for autonomous steering).

## 2. Exact question and the decision it changes

**Exact question:** Does the exact-JVP directional-gain field
‖Dg_l·u‖ (fixed probe directions u, all 24 layers, zero finite
differences, no ε) concentrate on a small layer set (high Gini)
distinct from the isotropic null — a dynamics-characterization
measurement?

| Median ΔGini (decision set, n_d ≥ 8) | Median Ḡini_iso (per-probe-median, same decision set) | Decision |
|---|---|---|
| ≥ 0.2 | < 0.4 | **CONTINUE** — direction-specific soft spots exist as a dynamics fact (characterization only) |
| ≤ 0 | any | **KILL** — the soft-spot premise dies for the registered probe direction; fields identical up to the null |
| any | ≥ 0.4 | **KILL-as-premise** — concentration is a generic dynamics property, not a direction-specific soft spot (folds to characterization) |
| 0 < median ΔGini < 0.2 | < 0.4 | **HELD** — ambiguous; no re-run without a new gate |

[DEFINITION] The median ΔGini ≥ 0.2 decision is a **ratio-free bar,
not a p-value** (defect class 1): no p-value is computed, quoted, or
needed — the verdict is read from the executor-computed median
ΔGini against the registered bars. No handwritten numbers enter the
decision.

Quantitative anchoring (gate §5, program records only — no
fabricated literature numbers):

- **Null (dynamically homogeneous-ish):** the isotropic exact field
  follows the smooth readout-decreasing profile — anchored to
  EXP127's σ̄ ≈ 1.17/4-blocks → per-block ~1.04 → the random-
  direction exact field runs ~1.04 (L23) to ~2.1–2.6 (L0) — smooth,
  low Gini (≲ 0.2 by the EXP128 bar's own scale). The semantic-probe
  field matches it: **ΔGini ≈ 0 → KILL**.
- **Alternative (soft spots):** the semantic field spikes at ≥1
  layer with **ΔGini ≥ registered margin 0.2** (half EXP128's bar)
  → CONTINUE.
- EXP127's R = 8.24 bounds the upside: per-layer directional gains
  cannot exceed the span's σ₁-scale without contradicting it.

[THEOREM] (forward-mode AD exactness): for a C^1 map f,
`jvp(f, (y,), (u,))` returns Df(y)·u exactly, up to floating-point
roundoff, by the chain rule on the executed computation graph. It is
not a difference quotient; no discretization parameter exists in its
definition.
[DEFINITION] (EXP127-class license scope): a CONTINUE licenses
further characterization only — the bars bind as written; a
surprising Gini pattern is recorded as [OBSERVATION], never
re-barred (Law #4).

## 3. Method

### 3.1 Prompts and probe directions [PROPOSITION]

- Verbatim EXP107 bench, 60 items. The 10 prompts are the
  **canonical-order first 10 items** (deterministic — no RNG
  selection; ids, EXP127's pinned decision set, for comparability:
  `exp107_flip_exp077_planet_2hop_0`,
  `exp107_ctrl_exp077_planet_2hop_1`,
  `exp107_flip_exp077_planet_2hop_2`,
  `exp107_ctrl_exp077_planet_2hop_3`,
  `exp107_flip_exp077_planet_2hop_4`,
  `exp107_ctrl_exp077_planet_2hop_5`,
  `exp107_flip_exp077_planet_2hop_6`,
  `exp107_ctrl_exp077_planet_2hop_7`,
  `exp107_ctrl_exp077_planet_2hop_8`,
  `exp107_flip_exp077_planet_2hop_9` — EXP127 report per-prompt
  table rows 66–75). Prompts only; **no labels anywhere** (Law #7
  clean by construction).
- **Semantic probe:** a single unit probe vector per prompt,
  derived deterministically from EXP077's archived support set per
  its §3.1–3.2 reconstruction recipe (the same Law #2-honest recipe
  used for EXP131's B_agg control — no artifact hash exists in
  program records; none invented). The derivation is read-only on
  archived files; the derived probes' SHA-256 is computed and
  recorded in the environment manifest **before the first JVP**
  (breaking point (c)). [CONDITION 4]
- **Isotropic controls:** K=8 seeded isotropic random unit vectors
  per prompt (seed 20260929 + prompt index — program convention);
  same-JVP, same-budget, computed on every prompt.

### 3.2 Frozen model discipline [PROPOSITION]

- Backbone: Pythia-410m from the pinned local weights
  (`~/workspace/.exp086_weights/pythia-410m`), `model.eval()`,
  float32 (JVP batches) / float64 (diagnostic, §3.3), CPU.
- LOG-331 parameter hash pinned before the first JVP and re-pinned
  after the last (breaking point (a)). No optimizer, no loss, no
  backward pass into weights; parameter tensors carry
  `requires_grad=False`.
- Environment manifest (torch/transformers/numpy versions, probe
  SHA-256, prompt ids, seeds) recorded pre-JVP.

### 3.3 The map, the JVP field, and the convergence diagnostic [DEFINITION]

- g_l is the **full rest-of-model map** from layer-l residual
  stream (final token) to the readout tensor — attention recomputed,
  context unclamped (the same map EXP128 measured). The readout
  tensor is x_{24,last}, the final-layer last-token residual —
  the codomain of EXP128's layer-to-readout sensitivity field
  (‖∂x_{24,last}/∂x_l‖).
- The field value: S_l^*(u) = ‖ Dg_l(y_l)·u ‖₂ via
  `torch.autograd.functional.jvp(g_l, (y_l,), (u,))`, float32,
  for l = 0…23, u ∈ {semantic probe, 8 isotropic controls}, all
  10 prompts.
- **Multi-ε convergence diagnostic (float64, verdict-immaterial)**
  [CONDITION 3]: on every prompt, for every probe, at the
  registered diagnostic layers {0, 11, 23} (shallow/mid/deep),
  compute F(ε) = ‖g_l(y_l+εu) − g_l(y_l)‖/ε at
  ε ∈ {1e-6, 1e-7, 1e-8} and require
  max_{ε} |F(ε) − JVP|/JVP ≤ 0.25 at all three diagnostic points.
  Non-convergence → that prompt is excluded from the decision set
  (disclosed); fewer than 8 diagnostic-passing prompts →
  **apparatus-void**, never a verdict. Pythia is C^∞, so
  differentiability is vacuous; this numerical diagnostic is the
  real breaking point. The diagnostic tolerance 0.25 is proposed
  here; the Law #14 review may tighten it before signing.
- The per-(prompt, layer, probe) JVP values are the raw records;
  the F(ε) diagnostic values are the instrument-health records.

### 3.4 The null-contrast decision statistic [DEFINITION] [CONDITION 2]

- Per prompt i: the **semantic field**
  {S_l^*(u_sem)}_{l=0..23} and, for each isotropic probe j, the
  **probe-j isotropic field** {S_l^*(u_j)}_{l=0..23}.
- Gini_sem_i = Gini coefficient over the 24 semantic-field values;
  Gini_iso_ij = Gini coefficient over the 24 values of the probe-j
  isotropic field; Ḡini_iso_i = median_j(Gini_iso_ij) over the 8
  seeded probes (standard Gini, executor-computed; no hand
  computation). [FIX-1 rationale: the median-of-8 *field* would
  suppress probe noise and bias E[ΔGini|H0] > 0 by an uncalibrated
  amount; per-probe Ginis give exact H0-symmetry (E[ΔGini] = 0
  under H0) at zero extra compute. Gate Condition 2's *design*
  (null-contrast ΔGini = Gini_sem − Gini_iso, margin 0.2, no
  raw-Gini bar) is preserved verbatim; only the null's aggregation
  is refined.]
- ΔGini_i = Gini_sem_i − Ḡini_iso_i. Decision statistic: median
  ΔGini over the decision set (§0). KILL-as-premise statistic:
  median Ḡini_iso over the decision set.
- **No raw-Gini bar exists anywhere** — without the registered
  null, the Gini bar would be uncalibrated (gate LOG-4737 §5).
- Spike-detection is recorded as a disclosed secondary
  [OBSERVATION], not verdict-bearing.
- Degenerate field: an all-zero field on any prompt (Gini 0/0) →
  apparatus-void for that prompt, disclosed.

### 3.5 Budget [PROPOSITION]

- Counting rule: each autograd JVP through the rest-of-model map
  counts as 1 product; each diagnostic F(ε) evaluation counts as 3
  forwards ≈ 1.5 products. Per-prompt expected ≈ 216 JVPs + 81
  diagnostic forward-sets ≈ 460 product-equivalents; total ≤ 40000
  products. Hard cap **1000 products/prompt** (the exact counts are
  deterministic, so the cap is a bug-catcher, not a target — still
  >2× headroom). Typical run expected ~250–350 JVP-equivalents/
  prompt, ~1–2 CPU-hours, $0.

### 3.6 Record-keeping gate (the defect-class-2 lesson) [PROPOSITION]

**Validity-check set (registered; the Law #9 "validity" step)**
[PROPOSITION]: (a) probe unit-norm audit — |‖u‖ − 1| ≤ 1e-6 for
the semantic probe and all 8 isotropic probes, computed pre-JVP;
(b) JVP-output finiteness — no NaN/Inf in any S_l^*(u); any
occurrence → apparatus-void for that prompt, disclosed; (c)
seed/pin audit — isotropic seeds = 20260929 + prompt index, and
the probe SHA-256 matches the manifest. All failures →
apparatus-void, disclosed. No new quantities — these are checks on
already-registered objects.

Before any verdict is read: the per-(prompt, layer, probe) JVP
values, the F(ε) diagnostic traces, the probe SHA-256, the prompt
ids, the LOG-331 pre/post pins, the per-arm product counts
(auditable against the §3.5 budget cap), and the environment
manifest are written to disk and **SHA-256 hash-pinned**. The
median ΔGini is computed only after the pins exist (Law #9
ordering: guards → pin → probe pins → diagnostic → JVP batches →
validity → hash-pin → metric → decision).

### 3.7 Law #7 posture [PROPOSITION]

No labels enter anywhere: no bench labels, no task targets, no
verifier. The prompts are content carriers for the base forward pass
only. The probe directions are read-only archive derivations. No
decision is read — the only model contact is the gain measurement.

## 4. Decision bars with statistical license

Verbatim from the gate (Law #4 — no recalibration):

| Condition | Verdict | License |
|---|---|---|
| median ΔGini ≥ 0.2 AND median Ḡini_iso < 0.4 | **CONTINUE** | direction-specific soft spots exist as a dynamics fact (characterization only) |
| median ΔGini ≤ 0 | **KILL** | the soft-spot premise dies for the registered probe direction — fields identical up to the null |
| median Ḡini_iso ≥ 0.4 | **KILL-as-premise** | concentration is a generic dynamics property, not a direction-specific soft spot |
| 0 < median ΔGini < 0.2 AND median Ḡini_iso < 0.4 | **HELD** | ambiguous; no re-run without a new gate |
| convergence diagnostic < 8/10 prompts | **apparatus-void** | hypothesis UNTESTED; the instrument failed |

## 5. Falsification decision tree

All numbers executor-produced; tree walked in code order:

| Tree node | Required outcome |
|---|---|
| Backbone LOG-331 pin (pre) | match `ec276abe3902fab0…` |
| Prompt set: verbatim EXP107 bench, canonical first 10, ids pinned | PASS |
| Probe provenance: EXP077 support-set recipe, SHA-256 recorded pre-JVP | PASS |
| Multi-ε convergence diagnostic (§3.3) | ≥ 8/10 prompts pass; fewer → **apparatus-void** |
| Isotropic controls (K=8, seeded, same map) | present on every decision-set prompt; missing → **apparatus-void** |
| JVP batches (24 layers × 9 probes, all decision-set prompts) | present; missing → **apparatus-void** |
| Raw records hash-pinned (values, traces, ids, pins, manifest) | PASS |
| Backbone LOG-331 pin (post) | identical; mismatch → **apparatus-void** |
| **median ΔGini** (over the decision set, n_d ≥ 8) | read only now — apply §4 bars |
| **median Ḡini_iso** (per-probe-median of 8 Gini_iso_ij, then median over the decision set) | read only now — apply §4 KILL-as-premise check |

## 6. What this protocol explicitly does NOT do

1. **No targeting claim is licensed.** Using the measured field as
   an injection-targeting map needs a new experiment number, new
   worth-it reasoning, and new bars; any targeting claim in this
   lane's future report → the pre-reg's Law #14 REJECT.
2. No finite difference is used as a sensing primitive or enters
   any verdict-bearing quantity. The sole ε-bearing computation is
   the verdict-immaterial convergence diagnostic (§3.3); it is
   grep-auditable as diagnostic-only (its outputs gate the decision
   set; they never enter ΔGini, the bars, or the tree).
3. No semantic direction used as an *injection instrument*; probe
   directions are diagnostic in a gain measurement, and no decision
   is read.
4. No bench construction, no labels, no logit channel (defect-class
   (e)/(f)/(g) and Law #7 are N/A by design, stated explicitly).
5. No loop, no adaptation, no dose escalation (EXP129's KILL does
   not transfer — there is no loop to kill).
6. No other layer span (all 24 layers measured; no span selection).
7. No post-hoc hypothesis rewording (Law #4): the bars bind as
   written; a surprising ΔGini pattern is recorded as
   [OBSERVATION], never re-barred.

## 7. Cost, honesty, and novelty

- ~1–2 CPU-hours, $0, no GPU contact, no labels, no training.
- A KILL here is a publishable boundary fact: the infinitesimal
  dynamics have no direction-specific soft spots at any layer
  along the registered probe direction — concentration, if any, is
  a generic dynamics property.
- A CONTINUE licenses further characterization — it is **not** a
  targeting claim, **not** a steering claim, and does **not** move
  the capability scoreboard (still zero positive signals for
  autonomous steering).
- No generality beyond Pythia-410m, the full-map linearization,
  and the 10 pinned prompts.
- **Novelty: N1 — Known Combination** (unchanged). [CONDITION 5]

## 8. Seventh item: the constraining kills, and why this is not a resurrection

**The constraining kill is EXP128's RUN-INVALID.** The killed object
was the *finite-difference sensing primitive* at fixed ε (1/12
linearity points within 25% — the instrument measured saturation,
not the propagator norm). This protocol's apparatus:

- contains **zero finite differences** — the sensing primitive
  (chain rule) is proven disjoint from the killed one (EXP128's
  S_l(ε) → S_l^*(u) as ε→0; the JVP computes the limit object
  directly — the saturation-remainder failure is inexpressible in
  AD);
- carries **different bars** (null-contrasted ΔGini, not raw Gini ≥
  0.4);
- carries a **different license** (dynamics characterization, not
  the targeting map).

**Different estimand license, different instrument, different
verdict architecture** — it is not EXP128 resurrected. No ε
retuning was attempted or licensed anywhere: ε does not exist in
the executor (it appears only in the verdict-immaterial convergence
diagnostic).

Other constraining kills do not fence this lane: EXP129 KILL (no
loop anywhere — pure measurement; the feedback mechanism doesn't
transfer); static-family kills (EXP077's cone kills, EXP094's L11
inertness, S5-2's 4.87% bound — those fence semantic directions as
*injection instruments* and *decision effects*; here probe
directions are diagnostic in a *gain measurement*, and **no
decision is read**); EXP130 REJECT (no generation, no elicitation —
the channel is unengaged); EXP131 (licensed, founder-hardware-gated
— complementary: ĉ is one number at one span for v₁; the DGF field
is 24 layers × probe directions; this protocol does not re-ask "does
v₁ align"). No licensed experiment has measured layer-wise exact
directional gains; the question is unfollowed, not killed.

---

*Draft only — licenses nothing. Next in the launch chain: independent
Law #14 review → fix-verification → CEO launch decision → execution
under a minted experiment number (EXP132-class).*
