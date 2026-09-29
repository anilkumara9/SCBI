# Pre-registration: TGA — Transient-Growth Amplification of the Frozen Pythia-410m Layer Propagator

**Lane:** LOG-4695 (pre-assigned). **Family:** A of the paradigm-break
sprint (LOG-4693). **Gate:** LOG-4694 (PASS). **License (dossier):**
`research/analysis_plans/G1_REPORT_2026-09-23.md` (Henrici He = 0.7332–
0.8343, mean 0.7689, across 48 attention O/V projection components
(24 O direct + 24 V fused-interleaved) in 24 layers — the unfollowed
lead since 2026-09-23).

**$0 CPU. Δθ=0 by construction.** This pre-registration licenses a
measurement only — **no injection is licensed by it.** Any injection
along the measured direction v_1 needs its own pre-registration, its
own bars, and the ĉ decision-orthogonality gate (§8). Draft only;
licenses nothing until the launch chain (Law #14 review → fix-
verification → CEO launch decision → execution under a minted number).

**Pre-reg decision record (span-placement caveat, gate §3):** the
primary span is L20→L24 — the injection-relevant span of every prior
injection experiment (EXP077 injected at L20, read at L24) — so v_1 is
compared apples-to-apples with the dead semantic directions. **No
fallback span is licensed by this pre-reg.** R < 2 at the
injection-relevant span kills the dynamics-matched injection program
outright; a different span's amplifier would not serve an L20
injection. The span a future gate would target, if one is ever
commissioned, is named here for transparency (L12→L16, the mid-span
region), but measuring it needs a new gate — it is not licensed here.
Span-placement risk is a design decision, not a verdict factor.

---

## 0. The breaking point (read first)

Conjunctive. Any miss → **apparatus-void, hypothesis UNTESTED, no R
minted** (Law #9 ordering: guards → backbone pin → convergence →
null arms → Δθ=0 re-pin → R → decision):

(a) **Δθ=0** — backbone LOG-331 parameter hash
    `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed`
    pinned before the first JVP and re-pinned after the last;
    any mismatch → apparatus-void.
(b) **Convergence before reading** — the §3.4 power-iteration
    convergence criteria for σ_1 AND for the deflated σ_2 both met on
    ≥ 8/10 prompts before any R is read; fewer converged → apparatus-
    void (the instrument failed), never a verdict. No reading from
    unconverged iterates. The verdict medians are computed over the
    decision set = prompts on which *both* σ_1 and σ_2 converged
    (n_d ≥ 8 required; fewer → apparatus-void).
(c) **Same-Jacobian, same-budget null** — the Hutchinson σ̄
    estimator (K=64) AND the matched-budget direct random-direction
    arm (K=64) computed on the *same* M with the *same* autograd
    budget on every prompt; either missing → apparatus-void.
(d) **No training, no weight mutation** — pure autograd
    Jacobian-vector products through a frozen model in eval mode; the
    executor contains no optimizer, no loss, no backward pass into
    weights.

[DEFINITION] The decision statistic is the **median R over the
decision set** (prompts on which *both* σ_1 and σ_2 converged;
n_d ≥ 8 required, else apparatus-void per (b)), where
R = σ_max(M)/σ̄(M) per prompt. For even n_d (e.g., 8), the median is
executor-computed as the average of the two middle order statistics;
for odd n_d, it is the middle order statistic. The median σ_1/σ_2 is
computed over the same decision set.

## 1. Hypothesis (one falsifiable sentence)

[HYPOTHESIS] The frozen Pythia-410m L20→L24 residual-stream propagator
M = ∂x_{24,last}/∂x_{20,last} possesses a distinguished maximally-
amplified direction v_1 — the leading right singular vector — whose
transient gain dwarfs the gain along random directions, quantified by
a median gain ratio R ≥ 3 across 10 bench prompts.

### 1.1 Why this experiment exists

[INTERPRETATION] The program's 120-experiment negative is not "frozen
models can't be steered" but "frozen models can't be steered **by
snapshot instruments**" (dossier §1). Every dead injection pushed
along *semantic* directions (concept vectors, bridge directions, task
normals) — directions the model's *dynamics* were never consulted
about. EXP086 Stage A measured Henrici non-normality He = 0.7332–
0.8343 across 48 attention O/V projection components (24 O direct
+ 24 V fused-interleaved) in 24 layers (CPU, read-only, Δθ=0,
LOG-331): the layer dynamics are strongly non-normal, and in
non-normal dynamics perturbations can be transiently amplified by
factors ≫ 1 over a finite layer span even when every eigenvalue is
stable ([THEOREM] Kreiss Matrix Theorem). The dynamics' own
maximally-amplified direction — the leading right singular vector
v_1 of the layer-to-layer propagator — was never measured and never
injected along in program history. The 2026-09-25 summit sprint
ranked this pilot #2 with the kill rule pre-drafted; it was never
executed (LOG-4694: unfollowed, not killed). This pre-registration is
its signed form.

## 2. Exact question and the decision it changes

**Exact question:** Does the frozen L20→L24 propagator contain a
distinguished amplified direction — median R ≥ 3, with the amplifier
concentrated on a single leading singular direction (median
σ_1/σ_2 ≥ 1.5) — that could serve as the first dynamics-matched
injection direction since the static family closed?

| Median R (decision set, n_d ≥ 8) | Median σ_1/σ_2 (same decision set) | Decision |
|---|---|---|
| ≥ 3 | ≥ 1.5 | **CONTINUE** — licenses a signed GPU injection-test pre-reg along v_1 vs matched-norm random directions vs B_agg (the EXP077 dead direction), minting a new experiment number. First licensed injection direction since the static family closed. |
| ≥ 3 | < 1.5 | **KILL** — the amplifier exists but has no v_1 to inject along; a uniformly amplified subspace is not an instrument. The distinguished-direction claim dies. |
| 2 ≤ R < 3 | any | **HELD** — ambiguous zone between "the precedent's amplifier" (×1.8, S3-8 LOG-225) and "a dynamics-matched amplifier." No GPU. A re-test needs a new gate, not a repeat. |
| < 2 | any | **KILL** — the whole dynamics-matched program stands down **pre-GPU**. He≈0.77 was decorative for control purposes. |

[DEFINITION] The R ≥ 3 decision is a **ratio bar, not a p-value**
(defect class 1): no p-value is computed, quoted, or needed — the
verdict is read from the executor-computed median R against the
registered bars. No handwritten numbers enter the decision.

Downstream injection-stage gates (named now for the GPU pre-reg that
a CONTINUE would license — **not decided here**): ĉ < 0.1 → KILL at
injection (ĉ = alignment of v_1 with the decision statistic — the
amplified direction is decision-orthogonal); no rank-trend of
injection effect across singular ranks → KILL.

## 3. Method

### 3.1 Prompts [PROPOSITION]

- Verbatim EXP107 bench, 60 items. The 10 prompts are the **canonical-
  order first 10 items** (deterministic — no RNG selection; ids
  recorded in the environment manifest). Prompts only; **no labels
  anywhere** (Law #7 clean by construction).
- No generation, no readout, no head training, no decode probe. The
  only model contact is autograd JVPs/VJPs through the frozen span.

### 3.2 Frozen model discipline [PROPOSITION]

- Backbone: Pythia-410m from the pinned local weights
  (`~/workspace/.exp086_weights/pythia-410m`), `model.eval()`,
  float32, CPU, 2 threads (read back).
- LOG-331 parameter hash pinned before the first JVP and re-pinned
  after the last (breaking point (a)). No optimizer, no loss, no
  backward pass into weights; parameter tensors carry
  `requires_grad=False`.
- Seeds pinned (20260929 + prompt index) for all random draws;
  environment manifest (torch/transformers/numpy versions) recorded.

### 3.3 The Jacobian: the frozen final-token map [DEFINITION]

M = ∂x_{24,last}/∂x_{20,last} is the Jacobian of the **final-token
map** f: ℝ^1024 → ℝ^1024 defined as follows:

- One base forward pass per prompt (grad enabled only through the
  computation graph; no weight updates).
- x_{20,last}: the residual stream at the **input of block 20**,
  last token position.
- x_{24,last}: the residual stream at the **input of block 24**
  (output of block 23), last token position.
- **Clamped-context linearization** [ASSUMPTION]: all keys and
  values at all positions are clamped to their base-pass values;
  only the block-20 input residual at the last token varies. f is
  then a deterministic differentiable map of that 1024-vector; its
  Jacobian M is taken by autograd (JVP: `torch.autograd.functional.
  jvp`; VJP: `torch.autograd.functional.vjp`).

[OPEN] The cross-position question — how last-token perturbations
propagate *across* positions (the map with KVs unfrozen) — is **not**
measured here. This is the standard final-token-map linearization
and a deliberate design decision: the downstream comparison is with
final-token readouts (all prior injection experiments), and the
cross-position Jacobian is a different object with a different
budget. Named in §10 as a design decision, not a verdict factor.

### 3.4 Power iteration for σ_max [PROPOSITION]

- Randomized power iteration on MᵀM via autograd products only —
  **M is never materialized** (1024×1024 dense is storable, but the
  no-materialization rule keeps the pilot honest at larger spans).
- Iterate: v^{(k+1)} = MᵀMv^{(k)}/‖MᵀMv^{(k)}‖, each iterate costing
  1 JVP (Mv) + 1 VJP (Mᵀw).
- Initialization: seeded isotropic random unit vector (no semantic
  content — the start vector must carry no task signal).
- [DEFINITION] Convergence criterion: relative change in the
  Rayleigh quotient ρ_k = ‖Mv^{(k)}‖² below **1e-6 over 5
  consecutive iterates AND ≥ 20 iterations minimum**. R is read
  **only** from converged iterates (Law #9 analog).
- σ_max = sqrt(ρ_final). Per prompt; the median is taken over the decision set (§0).
- Deflated σ_2: after v_1 converges, a second power iteration with
  every iterate projected orthogonal to v_1, convergence criterion
  1e-4 relative over 5 iterates AND ≥ 10 iterations (coarser — the
  decision threshold 1.5 needs less precision). σ_2 = sqrt(ρ_final).
  Ratio σ_1/σ_2 per prompt; the median is taken over the same decision set (§0).

### 3.5 The random-direction null [PROPOSITION]

Two arms on the **same M with the same autograd budget**
(breaking point (c)):

- **Hutchinson arm:** σ̄(M) = sqrt(Tr(MᵀM)/1024), Tr estimated by
  Hutchinson with K=64 Rademacher draws per prompt (each draw: 1
  JVP + 1 VJP). Seeded; deterministic.
- **Direct arm (cross-check + downstream bridge):** K=64 seeded
  isotropic random unit vectors u_j; median ‖Mu_j‖. Expected to
  agree with σ̄ to ~15% under the null estimator (|median − σ̄|/
  σ̄ ≤ 0.15 is a diagnostic trip, recorded, **not verdict-
  bearing** — it checks estimator bias). This arm is also the
  bridge to the downstream injection design (v_1 vs matched-norm
  random injection).

### 3.6 Budget [PROPOSITION]

- Counting rule: each autograd JVP or VJP through the 4-block span
  counts as 1 product. Hard cap **700 products/prompt** (σ_1 power
  iteration + deflated σ_2 + Hutchinson K=64 + direct K=64),
  ≤ 7000 products total. Typical run expected ~350–550/prompt,
  ~1–2 CPU-hours, $0.
- [DEVIATION from the gate memo §3] The gate's "300–500 JVPs"
  predated full costing of the σ_2 deflation arm (the auxiliary
  distinguished-direction KILL). The honest budget with all four
  arms is stated here; the kill bars are unchanged. This is a
  budget correction, not a design change.

### 3.7 Record-keeping gate (the defect-class-2 lesson) [PROPOSITION]

Before any verdict is read: the JVP convergence traces, the σ_1/σ_2
estimates, the per-arm autograd product counts (σ_1 power iteration,
deflated σ_2, Hutchinson, direct — auditable against the §3.6 budget
cap), the v_1/v_random vectors, the prompt ids, the LOG-331
pre/post pins, and the environment manifest are written to disk and
**SHA-256 hash-pinned**. The median R is computed only after the
pins exist (Law #9 ordering: guards → pin → convergence → null →
R → decision).

### 3.8 Law #7 posture [PROPOSITION]

No labels enter anywhere: no bench labels, no task targets, no
verifier. The prompts are content carriers for the base forward pass
only. The distinguisher is pure linear algebra on the frozen
propagator.

## 4. Decision bars with statistical license

Verbatim from the gate (Law #4 — no recalibration):

| Condition | Verdict | License |
|---|---|---|
| median R ≥ 3 AND median σ_1/σ_2 ≥ 1.5 | **CONTINUE** | dynamics-matched injection program licensed for a GPU gate (new number, new pre-reg) |
| median R ≥ 3 AND median σ_1/σ_2 < 1.5 | **KILL** | amplifier exists but has no v_1; a uniformly amplified subspace is not an instrument |
| 2 ≤ median R < 3 | **HELD** | ambiguous zone; no GPU; re-test needs a new gate |
| median R < 2 | **KILL** | whole dynamics-matched program stands down pre-GPU; He≈0.77 decorative |

Quantitative anchoring (gate §5, program records only — no
fabricated literature numbers):

- **Null (decorative non-normality / effectively normal dynamics):**
  median R ∈ [1, 1.5]. For normal M, σ_max/σ̄ = |λ|_max/RMS(|λ|) ≈ 1
  on a flat spectrum — the ratio cannot hide.
- **Precedent zone:** ×1.8 downstream gain (S3-8, LOG-225 — a
  *different mechanism*). R ∈ [1.5, 2.5) reproduces "an amplifier
  like the one already measured," not a new one — hence the HELD
  band. The CONTINUE bar (R ≥ 3) is set strictly above the ×1.8
  precedent so a CONTINUE means a genuinely stronger,
  dynamics-matched amplifier.
- **TGA hypothesis (load-bearing non-normality):** median R ≥ 3. The
  Kreiss bound permits ≫ 1 under He≈0.77 without giving a number.

[THEOREM] (variational SVD characterization): max_{‖δ‖=1} ‖Mδ‖ =
σ_max(M) exactly — the pilot measures the *largest possible* linear
gain of the frozen span; no direction class can beat v_1 by
construction.
[THEOREM] (Kreiss Matrix Theorem): for non-normal A,
sup_k ‖A^k‖ ≥ ρ_ε(A)/ε — transient growth ≫ 1 is possible with all
eigenvalues stable; non-normality is the *existence condition* for a
usable directional amplifier.

## 5. Falsification decision tree

All numbers executor-produced; tree walked in code order:

| Tree node | Required outcome |
|---|---|
| Backbone LOG-331 pin (pre) | match `ec276abe3902fab0…` |
| Prompt set: verbatim EXP107 bench, canonical first 10, ids pinned | PASS |
| σ_1 power iteration: convergence criterion met | ≥ 8/10 prompts converged; fewer → **apparatus-void** |
| Hutchinson σ̄ (K=64, same M, same budget) | present on every converged prompt; missing → **apparatus-void** |
| Direct random arm (K=64, same M) | present; missing → **apparatus-void** |
| Deflated σ_2: convergence criterion met | ≥ 8/10 prompts; fewer → **apparatus-void** |
| Raw records hash-pinned (traces, vectors, ids, pins, manifest) | PASS |
| Backbone LOG-331 pin (post) | identical; mismatch → **apparatus-void** |
| **median R** (over the decision set, n_d ≥ 8) | read only now — apply §4 bars |
| **median σ_1/σ_2** (over the same decision set) | read only now — apply §4 auxiliary |

## 6. What this protocol explicitly does NOT do

1. **No injection is licensed.** The measured v_1 vectors are
   recorded as raw artifacts; using them as injection directions
   needs a new pre-registration with its own bars and the ĉ
   decision-orthogonality gate (§8).
2. No cross-position Jacobian (pinned in §3.3 as a design decision).
3. No semantic direction anywhere: no concept vectors, no bridge
   directions, no task normals, no decode probes, no trained heads.
4. No bench construction, no labels, no logit channel (defect-class
   (e)/(f)/(g) and Law #7 are N/A by design, stated explicitly).
5. No other layer span (span-placement resolution in the header).
6. No post-hoc hypothesis rewording (Law #4): the bars bind as
   written; a surprising σ_1/σ_2 pattern is recorded as
   [OBSERVATION], never re-barred.

## 7. Cost and honesty

- ~1–2 CPU-hours, $0, no GPU contact, no labels, no training.
- A KILL here is a publishable boundary fact: the dynamics have no
  distinguished amplified direction at the measured span — the
  non-normality is decorative for control purposes.
- A CONTINUE licenses a GPU injection test — it is **not** a steering
  claim and does **not** move the capability scoreboard (still zero
  positive signals for autonomous steering).

## 8. What TGA does NOT claim

- R ≥ 3 does not claim v_1 steers anything; it claims the dynamics
  contain a usable directional amplifier worth testing. Steering is
  claimed only by a future injection experiment with its own bars.
- R does not characterize the model's "thoughts," "intent," or
  consciousness. It is a linear-algebraic property of a frozen map.
- The Kreiss bound gives an *existence condition*, not a predicted
  number; the R ≥ 3 bar comes from the program's own ×1.8 precedent,
  not from the theorem.
- No generality beyond Pythia-410m L20→L24 and the 10 pinned prompts.

## 9. Deviations from the gate memo and dossier (complete list)

1. **Budget (§3.6):** gate estimated 300–500 JVPs total; full costing
   of all four arms (σ_1 + deflated σ_2 + Hutchinson K=64 + direct
   K=64) gives a hard cap of 700 products/prompt, ≤ 7000 total.
   Budget correction; bars unchanged.
2. **σ_2 convergence (§3.4):** gate did not specify the deflation
   convergence; pinned here as 1e-4 relative over 5 iterates, ≥ 10
   iterations (coarser than σ_1's 1e-6/20 — the 1.5 threshold needs
   less precision).
3. **Jacobian clamp discipline (§3.3):** gate said "final-token map
   linearization"; pinned here as clamped-context (all KVs clamped
   to base-pass values, only the block-20 input residual at the last
   token varies).
4. **Prompt selection (§3.1):** gate said "fixed 10 prompts from the
   verbatim EXP107 bench"; pinned here as canonical-order first 10.
5. **Direct-arm trip (§3.5):** the |median − σ̄|/σ̄ ≤ 0.15 agreement
   trip is diagnostic-only, not verdict-bearing (gate was silent).
6. **Span fallback (header):** gate asked the pre-reg to name the
   fallback span; named as L12→L16 for a *future* gate — **not
   licensed here**. No fallback measurement is permitted under this
   pre-reg.
7. **Downstream gates (§2):** the ĉ < 0.1 and rank-trend KILL gates
   are named for the GPU pre-reg a CONTINUE would license; they are
   not decided here.

No other deviation: bars, breaking point, convergence criterion for
σ_1, K=64 null arms, Δθ=0 pins, and the seventh-item record are
carried verbatim from the gate.

## 10. Boundary

- The clamped-context linearization is a design decision: it defines
  the object the program can compare against its own injection
  history. The unfrozen-context (cross-position) Jacobian is a
  different experiment with a different budget.
- The 10-prompt median is a pilot statistic, not a population claim;
  the prompts are fixed, not sampled — no inference beyond the pinned
  set is licensed.
- If the direct-arm trip fires (>15% disagreement), the verdict
  still binds on R — the trip is a disclosed estimator-health
  observation for the Law #14 review and the execution report.
- A CONTINUE does not license GPU execution — it licenses the *GPU
  pre-registration* for the injection test, which carries its own
  Law #14 review, its own bars, and the ĉ decision-orthogonality
  gate.
- Novelty: N1 — Known Combination (unchanged).
- Seventh-item record (restated from the gate): the constraining
  kills — EXP077's cone kills (semantic concept direction at L20,
  ΔM=0), EXP094's L11 inertness (120 semantic injection arms, zero
  flips), S5-2's 4.87% per-arm bound (semantic/static directions),
  S5-3's never-decodable PIVOT (decode-probe rooms, not injection),
  G1's QK-subspace KILL (a mechanism *account* on QK/OV projector
  energies of semantic vectors — the propagator M is the full
  residual update, a different object), EXP086 Stage B (licensed,
  GPU-gated, never executed — not a constraining kill; the 9-25
  novelty audit explicitly differentiates TGA's task-agnostic
  propagator SVD from its task-informed decision normal as
  complementary) — the constraining kills are all snapshot-instrument
  or semantic-direction results; **none measured or injected along
  the dynamics' own leading singular vector v_1**. The 2026-09-25 TGA proposal was
  ranked #2 with the kill rule pre-drafted and the log records
  "$0 CPU; no experiments executed" — **unfollowed, not killed** —
  so this pre-registration re-activates an unfollowed pilot rather
  than resurrecting a killed hypothesis. H17, S5, H12, bench
  re-reading, EXP117/118/119/121/123/124 reruns, entity-name
  generation, H22's generality, H23's identity interpretation stay
  dead and untouched.

---

*Draft only — licenses nothing. Next in the launch chain: independent
Law #14 review → fix-verification → CEO launch decision → execution
under a minted experiment number.*
