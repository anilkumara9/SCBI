# Pre-registration: TGA v₁ Injection Test — Dynamics-Matched Injection in the Frozen Pythia-410m

**Lane:** LOG-4724 (pre-assigned). **License:** EXP127 (TGA) CONTINUE,
bound at LOG-4698/LOG-4699 (BIND-WITH-CAVEAT): median R = 8.240640
(per-prompt [8.0019, 8.5294]), median σ₁/σ₂ = 1.557689 (per-prompt
[1.5302, 1.5881]), decision set n_d = 10, all ten prompts converged.
The licensed consequence (bound): "only a separately pre-registered
GPU injection test along v₁, with matched random controls, dead B_agg
control, decision-orthogonality gate ĉ, singular-rank trend gate."

**GPU-GATED.** This pre-registration licenses a GPU execution only —
it is not a CPU pilot and it licenses **no GPU contact by itself**.
Execution waits on the user's hardware and the founder's GPU queue.
Draft only; licenses nothing until the launch chain (independent
Law #14 review → fix-verification → CEO launch decision → execution
under an experiment number minted at the CEO launch decision).

**$0 CPU at drafting. Δθ=0 by construction.** This draft is a
steering *test*, not a steering claim. The capability scoreboard
stays at zero until and unless this test returns a bound positive.

**Pre-reg decision record (direction-provenance caveat):** v₁ is
re-pinned exactly from EXP127's hash-pinned artifact
`exp127_vectors.npz` (SHA-256
`9b527c026d0ee307192725429f655e628f403505343dc018de3cfe15db6113dc`,
per-prompt keys `v1__<prompt_id>`, 10/10 id alignment required).
**No finite-difference reconstruction of v₁ is permitted** — the
finite-difference sensing apparatus died at EXP128 (1/12 within 25%,
RUN-INVALID apparatus-void), and this protocol contains no
finite-difference term anywhere. The injected direction is the
EXP127 direction, not an approximation of it.

---

## 0. The breaking point (read first)

Conjunctive. Any miss → **apparatus-void or RUN-INVALID as stated,
hypothesis UNTESTED** (Law #9 ordering: guards → backbone pin →
artifact re-pins → budget computation and record → ĉ gate → forward batches (injections) →
validity-check evaluation → raw-record hash-pin → metric → decision):

(a) **Δθ=0** — backbone LOG-331 parameter hash
    `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed`
    (sorted `state_dict` keys, float32, tensor bytes — the
    EXP077/EXP084/EXP108 canonical convention) pinned before the
    first GPU forward and re-pinned after the last; any mismatch →
    apparatus-void.
(b) **v₁ re-pin** — `exp127_vectors.npz` SHA-256 matches the
    pinned value AND all 10 per-prompt ids align as
    `v1__<prompt_id>`; miss → apparatus-void (the injected
    direction is not the EXP127 direction).
(c) **No finite differences** — the executor asserts no
    finite-difference term (‖Δ‖/‖δ‖ or any δ-perturbation
    sensing) exists anywhere in the injection pipeline; the
    injection is exact-vector addition at x_{20,last}. Any
    finite-difference sensing input → apparatus-void (EXP128
    constraint, §7).
(d) **Norm-budget matching** — every injection arm spends exactly
    B (‖δ‖ = B, float32 tolerance 1e-6 relative); any arm with a
    different injected norm → apparatus-void (the verdict would
    measure the budget, not the direction — the dose-fence made
    mechanical, EXP129 FIX-4 discipline).
(e) **B_agg null-control holds** — the dead B_agg arm must
    replicate EXP077's ΔM = 0; if the B_agg arm moves any
    decision, → **RUN-INVALID (apparatus drift)** — the bench or
    backbone is not what EXP077 measured, and no verdict may be
    read. The dead control guards the apparatus, not the verdict.
(f) **No training, no weight mutation** — pure forwards through
    a frozen model in eval mode; the executor contains no
    optimizer, no loss, no backward pass into weights. The ĉ
    computation uses exact autograd VJPs (EXP127's Law-#14-
    licensed apparatus) — a backward *through the frozen graph*,
    never into weights.

[DEFINITION] ĉ (decision-orthogonality): for prompt i, let M_i be
the clamped-context final-token-map Jacobian (EXP127's object).
Let g_i = ∇_{x_{20,last}} margin_i be the exact-autograd VJP of
the registered cosine margin (score(E1) − score(E2), the H1/H6
§3.3 statistic) with respect to x_{20,last}, computed on the base
(no-injection) forward. ĉ_i = |⟨v̂₁,i, ĝ_i⟩| with
ĝ_i = g_i/‖g_i‖. The gate statistic is the mean over the 10
prompts. If ‖g_i‖ < 1e-12 on a prompt, that prompt is excluded
from the ĉ mean with the exclusion recorded; ≥ 3 exclusions →
apparatus-void. **ĉ < 0.1 → KILL at injection** (EXP127 §8):
the amplified direction is decision-orthogonal — an amplifier of
nothing the task cares about.

## 1. Hypothesis (one falsifiable sentence)

[HYPOTHESIS] On the frozen Pythia-410m, one-shot injection of a
fixed norm-matched perturbation along v̂₁ (the dynamics' own
leading singular direction, EXP127) at x_{20,last} moves the
registered cosine decision statistic's decisions where
matched-norm random-direction injections and the dead B_agg
control move nothing — quantified by a margin-displacement ratio
≥ 2× vs the best random arm (paired per item) AND decision flips
that the random and B_agg arms do not produce.

### 1.1 Why this experiment exists

[INTERPRETATION] The program's 120-experiment negative is "frozen
models can't be steered **by snapshot instruments**" (LOG-4693).
Every dead injection pushed along *semantic* directions — concept
vectors, bridge directions, task normals (EXP077: ΔM = 0 at L20;
EXP094: zero flips across 120 arms at L11; S5-2: per-arm ≤ 4.87%
bound on semantic/static directions) — directions the model's
*dynamics* were never consulted about. EXP127 measured the
dynamics' own maximally-amplified direction: median R = 8.240640
(v̂₁ amplifies ≈8× more than average random directions), median
σ₁/σ₂ = 1.557689 (a distinguished leading direction, not a flat
spectrum). **No injection in program history has ever been along
v₁.** Under Law #4, v₁ is a new direction class
(dynamics-matched), not a dose tweak of the killed semantic
directions — the semantic-direction kills do not fence it (§7).
This is the first licensed injection direction since the static
family closed. It is a test, not a claim.

## 2. Exact question and the decision it changes

[QUESTION] Does injecting the task signal along v₁ (the dynamics'
own leading direction) move decisions where semantic-direction
injection moved nothing?

| Condition (all executor-produced) | Decision |
|---|---|
| **ĉ ≥ 0.1 AND margin-displacement ratio (v₁ vs best random) ≥ 2× paired AND ΔM_v1 > 0 with McNemar(v₁, best-random) one-sided p ≤ 0.05 (best-random pinned in §3.7) AND rank-trend holds (σ₁ > σ₂ > random) AND B_agg null-control holds (ΔM_Bagg = 0)** | **CONTINUE** — the first bound positive steering signal in program history. v₁ is a licensed steering direction; the GPU dynamics program continues. |
| **ĉ < 0.1** | **KILL** — decision-orthogonal amplifier (EXP127 §8 gate). The dynamics amplify, but nothing the task cares about. |
| **ΔM_v1 = 0 (or ΔM_v1 = ΔM_random)** | **KILL** — v₁ is inert like the semantic directions; the dynamics-matched injection program stands down. |
| **Flat rank trend** (injection effect does not rank-order with singular rank) | **KILL** — the effect is not the amplifier's; it is dose or noise wearing v₁'s name. |
| **Margin ratio ≥ 2× but ΔM_v1 = 0** | **HELD** — the amplifier moves the residual but not the decision; recorded, no re-test without a new gate. |
| **B_agg arm moves any decision** | **RUN-INVALID** — apparatus drift (breaking point (e)); hypothesis UNTESTED. |
| **Any breaking-point miss** | **apparatus-void / RUN-INVALID as stated** — hypothesis UNTESTED. |

The ĉ gate and the KILL branches are evaluated first (EXP129
FIX-1 precedence discipline); the CONTINUE bars apply only if no
KILL branch fires.

## 3. Method

### 3.1 Prompts (pinned)

- Verbatim EXP107 bench, 60 items. The 10 injection prompts are
  the **canonical-order first 10** (deterministic — no RNG
  selection): ids `exp107_{flip,ctrl}_exp077_planet_2hop_{0..9}`
  — the same decision set as EXP127/EXP128/EXP129, so the three
  dynamics measurements are directly comparable. Prompts only;
  **no labels anywhere in direction construction** (Law #7
  clean — v̂₁ comes from EXP127's label-free power iteration).
- Labels (`tuple[0]`) are used **at metric time only** (Law #7):
  decision flips are scored against the bench labels; no label
  enters any injection direction.

### 3.2 Frozen backbone (GPU)

- Backbone: Pythia-410m from the pinned local weights
  (`~/workspace/.exp086_weights/pythia-410m`), `model.eval()`,
  float32, GPU (device pinned in the worksheet), deterministic
  flags set (`torch.use_deterministic_algorithms` where
  supported; cuDNN benchmark off).
- LOG-331 parameter hash pinned before the first GPU forward
  and re-pinned after the last (breaking point (a)). No
  optimizer, no loss, no backward pass into weights; parameter
  tensors carry `requires_grad=False` (the ĉ VJP runs with
  grad enabled on the *activation* graph only).
- Seeds pinned (`20260929_4724` + prompt/arm offsets) for all
  random-direction draws; environment manifest recorded.
- Loader: `AutoModelForCausalLM` (the EXP126 loader lesson —
  LOG-331 was computed on the causal-LM state dict).

### 3.3 Direction re-pins (breaking point (b))

- **v̂₁,i**: from `exp127_vectors.npz`
  (`9b527c026d0ee307192725429f655e628f403505343dc018de3cfe15db6113dc`),
  keys `v1__<prompt_id>`, 10/10 id alignment; SHA-256 verified
  before the first injection forward.
- **v̂₂,i**: derived per the LOG-4714 erratum (seeded deflated
  power iteration, seed `20260929_4714`, **fixed iteration count
  K=40**, exact JVP/VJP
  apparatus); orthogonality |v̂₂ᵀv̂₁| < 1e-6 asserted.
- **B̂_agg**: the EXP077 dead bridge direction, re-derived
  deterministically from the archived support set per EXP077's
  §3.1–3.2 reconstruction (v̂ = B_agg; `run_exp077.py` §"Reconstruct
  v_hat_k, v_hat (=B_agg), mu, v_hat^c"). Its SHA-256 is recorded
  in the worksheet before the first injection forward; the
  direction is norm-matched to B. [NOTE] No B_agg artifact hash
  exists in program records, so no hash is invented here (Law
  #2) — the provenance is the deterministic reconstruction, and
  the worksheet hash is the pin.
- **Random directions**: K = 8 seeded isotropic unit vectors per
  prompt (`torch.Generator`, seeds `20260929_4724 +
  prompt_idx*100 + j`, j ∈ {0..7}), norm-matched to B.

### 3.4 Injection budget (breaking point (d))

- B = 0.01 × median ‖y_{20,last}‖ over the 10 pinned prompts
  (the EXP129 FIX-2 scale-relative rule — 1% of the base
  residual norm; no absolute number is invented, Law #2). The
  absolute B is computed from base forwards and recorded in the
  worksheet **before** the first injection forward.
- Injection: x_{20,last} ← x_{20,last} + δ with ‖δ‖ = B for
  every arm (v̂₁, v̂₂, each random draw, B̂_agg). Component
  audit: injected norms recorded per (item, arm) from raw
  records; any ‖δ‖ ≠ B within float32 tolerance → apparatus-void.
- The injection site is x_{20,last} — the input of block 20,
  last token position — the EXP127 span's input and the
  injection site of every prior injection experiment
  (EXP077 injected at L20, read at L24): apples-to-apples with
  the dead semantic directions.

### 3.5 Arms (per prompt)

- **Base:** no injection — the reference decisions.
- **v̂₁ arm:** δ = B·v̂₁,i.
- **v̂₂ arm:** δ = B·v̂₂,i (rank-trend gate).
- **Random arms:** δ = B·u_j, j ∈ {0..7} (matched-norm null).
- **B_agg arm:** δ = B·B̂_agg (the dead control — ΔM = 0
  expected; breaking point (e)).
- Total per prompt: 1 base + 1 v̂₁ + 1 v̂₂ + 8 random + 1 B_agg
  = 12 forwards; 10 prompts → **120 forwards** + ĉ VJPs (~10) —
  minutes on a T4, $0.

### 3.6 Readout — the registered cosine decision statistic

- The decision pipeline is the registered H1/H6 §3.3 recipe,
  verbatim: candidate entities E1 = `tuple[0]`, E2 =
  `tuple[-1]`; option texts `" " + E`; the executor asserts
  `encode(" "+E)` is exactly one token on the real Pythia
  tokenizer for every item (failure → RUN-INVALID, items NOT
  silently dropped); option embeddings = frozen layer-20
  final-token hidden state of the single-token option text;
  `score(E) = cosine(state_emb, option_emb)`; decision =
  argmax(score(E1), score(E2)); ties → E2; **margin** =
  `|cos(E1) − cos(E2)|`.
- The injection is inserted at x_{20,last} during the item's
  forward; everything else in the H6 pipeline is identical.
  **No logit channel, no generation, no decode probe, no
  trained head** — the readout is the registered statistic.
- Per (item, arm): decision, margin. **ΔM** = decision flip vs
  the base arm. Margin displacement = |margin_arm −
  margin_base|.

### 3.7 Decision bars with statistical license

- **ĉ gate:** mean ĉ over the 10 prompts; ĉ < 0.1 → **KILL**
  (decision-orthogonal amplifier).
- **Primary (continuous):** per-item margin-displacement ratio
  r_i = |margin_{v1,i} − margin_{base,i}| / max_j
  |margin_{rand_j,i} − margin_{base,i}|; the decision statistic
  is the **median r_i** (executor-computed). Bar: median r ≥ 2
  (the EXP129 bar family — a paired, continuous discriminant).
  Zero-denominator branch: if the denominator is 0 (all 8 random
  arms move the margin by exactly 0 on item i) — 0/0 → r_i = 1;
  x/0 (x > 0) → r_i = +∞. Denominator-zero items are disclosed
  as a diagnostic in the report.
- **Primary (decisions):** ΔM_v1 = flips on the v₁ arm;
  McNemar one-sided exact v₁ vs best-random arm,
  p ≤ 0.05 (the H4/H14/H19 program standard).
  [DEFINITION] **best-random** = the single random arm j* with
  the most flips across all 10 items (ties → lowest j). The
  paired table compares v₁'s vs j*'s per-item decisions.
  A-priori one-sided exact critical table (n = discordant
  pairs, (b,c) = (pairs favoring v₁, pairs favoring j*),
  p = P(X≥b|n,0.5)): n=5: (5,0) → 0.0312; n=6: (6,0) → 0.0156;
  n=7: (7,0) → 0.0078; n=8: (7,1) → 0.0352; n=9: (8,1) → 0.0195;
  n=10: (9,1) → 0.0107. n ≤ 4: significance unreachable
  (floor p > 0.05).
- **Rank-trend gate:** margin displacement must rank-order
  with singular rank: disp(v̂₁) > disp(v̂₂) > median
  disp(random) on ≥ 8/10 prompts; flat → **KILL**.
- **B_agg null-control:** ΔM_Bagg = 0 required; any flip →
  **RUN-INVALID** (apparatus drift), never a verdict.
- CONTINUE requires ALL of: ĉ ≥ 0.1, median r ≥ 2,
  ΔM_v1 > 0 with McNemar p ≤ 0.05, rank-trend holds,
  ΔM_Bagg = 0. A margin gain without flips is HELD, never
  CONTINUE — the question is about decisions.

### 3.8 Raw-record hash-pin specification (defect class (b))

Before the decision statistic is computed — and before any
decision branch — the executor hash-pins (SHA-256): per
(item, arm) injection records (direction key, injected norm,
decision, margin, displacement), the ĉ per-prompt values and
exclusions, the v̂₁/v̂₂/B_agg re-pin records (hashes, id
alignment, orthogonality asserts), the budget audit (B value,
per-arm norm records), the environment manifest (versions,
device, thread counts, backbone LOG-331 pre/post pins), and
the append-only console log. A metric minted without the pin →
apparatus-void.

### 3.9 Guards and what is NOT measured here

- **No semantic-direction arms** (EXP077/EXP094 territory —
  barred; the dead semantic directions appear only as the
  B_agg null-control, not as verdict arms).
- **No feedback loop** (EXP129 territory — barred; this is
  one-shot injection, no sensing, no re-targeting).
- **No finite differences** (EXP128 territory — barred; the
  injection is exact-vector addition, the ĉ gate is exact VJP).
- **No generation, no decode probe, no trained head.**
- **No cross-span injection** (span-placement resolution in
  the header — L20→L24 only).
- **No post-hoc re-barring** (Law #4): the bars bind as
  written.

## 4. Falsification decision tree

All numbers executor-produced; tree walked in code order:

| Tree node | Required outcome |
|---|---|
| Backbone LOG-331 pin (pre) | match `ec276abe3902fab0…` |
| Artifact re-pins: v̂₁ (hash + 10/10 ids), v̂₂ (orthogonality), B̂_agg (reconstruction hash) | **PASS** — miss → apparatus-void |
| Budget: absolute B computed and recorded; per-arm ‖δ‖ = B | **PASS** — miss → apparatus-void |
| ĉ gate: mean ĉ over ≤ 10 prompts (≥ 3 exclusions → apparatus-void) | **ĉ ≥ 0.1** — miss → **KILL** |
| 120 injection forwards + ~10 ĉ VJPs; batch order free across items | **DONE** — exit code 0 |
| Backbone LOG-331 pin (post) | identical; mismatch → apparatus-void |
| B_agg null-control: ΔM_Bagg | **= 0** — any flip → **RUN-INVALID** |
| Raw-record hash-pin | **PASS** — defect class (b) |
| **Median margin-displacement ratio r** | **≥ 2** — miss → KILL or HELD per §2 |
| **ΔM_v1 + McNemar(v₁, best-random)** | **ΔM_v1 > 0 AND p ≤ 0.05** (best-random §3.7) — miss → KILL |
| **Rank trend** (v̂₁ > v̂₂ > random on ≥ 8/10) | **PASS** — flat → **KILL** |

## 5. Law #9 ordering

guards → backbone pin → artifact re-pins (v̂₁/v̂₂/B_agg) →
budget computation and record → ĉ gate → forward batches
(injections, any batch order) → validity-check evaluation
(norm audit + B_agg null-control + re-pin) → raw-record
hash-pin → metric (median r, ΔM, McNemar, rank trend) →
decision.

## 6. Cost and honesty

- ~120 forwards + ~10 ĉ VJPs + ~800 autograd products for the
  v̂₂ deflated power iteration (K=40 × 2 products × 10 prompts) —
  minutes on a single T4, $0.
- A KILL here is a publishable boundary fact: the dynamics'
  own leading direction is inert (or decision-orthogonal) at
  the injection scale — the non-normality is decorative for
  control purposes, and the dynamics-matched injection program
  stands down.
- A CONTINUE is the program's first bound positive steering
  signal — and is tagged exactly that: a bound positive on
  Pythia-410m L20→L24 and the 10 pinned prompts, never
  "steering works," never consciousness, never generality.

## 7. Cost, honesty, and what constrains this protocol

**The constraining kills (never-resurrect audit).**
EXP077's cone kills (unconditional 30° cone / α=1 offset of a
*semantic* concept direction at L20, ΔM=0); EXP094's L11
inertness (120 injection arms along *semantic* directions,
zero flips); EXP093's shared-direction inertness; S5-2's 4.87%
per-arm bound (*semantic/static* directions, decision
effects); S5-3's never-decodable PIVOT (decode probes, not
injection); G1's QK-subspace KILL (a mechanism *account* on
QK/OV projector energies of semantic vectors — the propagator
M is the full residual update, a different object);
EXP115/116/123's generation-channel deaths (this protocol
never reads generated content); EXP125's H22 KILL; EXP126's
H23 KILL (the entity-identity interpretation is retired — this
protocol's readout is the registered cosine statistic, and its
domain-set-detector caveat is inherited, not re-litigated);
the LOG-4693 death of the static-snapshot instrument paradigm.
**EXP128's RUN-INVALID** (apparatus-void): finite-difference
sensing at ε=1e-3 measures nonlinearity, not the propagator
norm — this protocol contains no finite-difference term
(breaking point (c)); v₁ is re-pinned exactly, not
reconstructed. **EXP129's KILL** (median r = 1.000005):
feedback re-targeting adds nothing — this protocol is
one-shot injection with no loop, so EXP129's mechanism does
not transfer (and EXP129's KILL is adverse evidence against
closed-loop designs, not against one-shot injection). **None
of these kills was along v₁** — under Law #4, v₁ is a new
direction class (dynamics-matched), not a dose tweak, and the
semantic-direction kills do not fence it. If the injection
along v₁ is inert, it joins the dead directions honestly.

**The EXP127 license boundary.** EXP127's CONTINUE licenses
this pre-registration, not an injection. This pre-reg licenses
a GPU execution only after its own Law #14 review,
fix-verification, and CEO launch decision. The ĉ and
rank-trend gates are the §8-named executioners — they are
decided here, not deferred.

## 8. What this protocol does NOT claim

- Not a steering claim. A CONTINUE is a bound positive on one
  model, one span, ten prompts — the scoreboard moves only
  when the bound verdict lands.
- Not reasoning, not cognition. v₁ is a linear-algebraic
  property of a frozen map; moving a decision along it is a
  control fact, not a thought.
- Not generality. Pythia-410m, L20→L24, the 10 pinned prompts.
- Not a mechanism account. The verdict says v₁ steers (or
  doesn't); it does not explain *why* the dynamics amplify it.
- Not a resurrection. Every constraining kill is named in §7;
  none is revived. EXP127 stays CONTINUE'd and is not
  re-gated; EXP128 stays UNTESTED; EXP129 stays KILLed.
- Novelty: N1 — Known Combination.

## 9. Deviations (complete list)

1. None from the EXP127 license (LOG-4699): the four licensed
   elements (matched random controls, dead B_agg control,
   ĉ gate, rank-trend gate) are all protocol-level spec
   (§3.3, §3.5, §0, §3.7).
2. The B_agg provenance is deterministic reconstruction from
   the archived support set (§3.3) rather than a hash-pinned
   artifact — no B_agg hash exists in program records, and no
   hash is invented (Law #2); the worksheet records the
   reconstruction hash at execution.
3. Budget B follows the EXP129 FIX-2 scale-relative rule
   (1% of median ‖y_{20,last}‖) rather than an absolute norm —
   the honest reading under Law #2.

*Draft only — licenses nothing. Next in the launch chain:
independent Law #14 review → fix-verification → CEO launch
decision → GPU execution (user hardware, founder queue) under
a minted experiment number.*
