# EXP068 Protocol Specification: Per-Instance G/E/S/T Loop over Basis Candidates

**Status:** PRE-REGISTERED (protocol; not yet executed)
**Date:** 2026-09-23
**Author role:** Theory + Preregistration Agent
**Predecessor experiments:** EXP063–EXP067 (boundary series; EXP067 pre-registered, unexecuted)
**Governing standards:** `AGENTS.md` (14 Inviolable Laws), `STATISTICAL_PROTOCOL_V02.md`,
`theory/LOOP_SPEC_DRAFT.md` (signed operational spec — constraining basis for this protocol),
`theory/BOUNDARY_CLAIM_FORMALIZATION.md`, `research/literature/audit_2026-09-23.md` (N1 verdict)
**Execution rule:** Strictly confirmatory. No operator, hyperparameter, gate, or threshold changes
after the ρ-gate is computed without a new pre-registration. **Changed design = EXP069.**

---

## 1. Research question and hypotheses

$$\boxed{\textbf{Does per-instance inference-time \textit{selection} over basis candidates
(frozen } \theta, \Delta\theta = 0\textbf{) beat the static CAA-equivalent injection on
headroom-verified reversal tasks?}}$$

**[HYPOTHESIS] H_loop:** Per-instance $\mathcal{G}/\mathcal{E}/\mathcal{S}/\mathcal{T}$
selection over basis candidates, with $\Delta\theta=0$ and a target-free evaluator
$\mathcal{E}$, yields $\Delta M > 0$ (McNemar exact $p < 0.05$) on the headroom-calibrated
benchmark **and** beats the static CAA-equivalent injection **and** beats compute-matched
output-level search. (Conjunctive; all three required. Carried verbatim from
`theory/LOOP_SPEC_DRAFT.md` §5.)

**Null $H_0$:** $\Delta M_{\mathrm{loop}} \le 0$ ($p \ge 0.05$), or the loop fails to beat
either the static or the output-level baseline.

**[NOTE — operationalization gap, Law #4]** H_loop is carried verbatim from
`theory/LOOP_SPEC_DRAFT.md` §5, and its third conjunct says the loop "**beats**
compute-matched output-level search." This protocol operationalizes that conjunct in the
positive criterion (§10) as "beats-or-ties (F5 not triggered)" — i.e., the loop is *not
significantly dominated*. "Not significantly dominated" $\neq$ "beats": the verbatim
hypothesis is stronger than the operational criterion. This softening is pre-registered
here, not made silently; the §11 branch-(e) reporting rule (fix D2) applies "beats
output-level search" language only when the C3-vs-C7 McNemar $p < 0.05$ favors C3, and
"not dominated by compute-matched output-level search (F5 not triggered)" otherwise.

### 1.1 Scope of this experiment (boundary science; honest novelty framing)

[INTERPRETATION] EXP068 is a **boundary-characterization experiment with a mechanism test
inside it**, not a novelty experiment. The program's assessed novelty tier is **N1 — Known
Combination** (`reports/novelty_report.md`): the static injection tested in EXP064–066 is
operator-equivalent to Contrastive Activation Addition (Rimsky et al., 2023). The loop's
formulation distinction — an *internal self-consistency evaluator over basis-valued search
objects*, gradient-free, $\Delta\theta=0$ — is the only component with any novelty-relevant
claim, and it is currently **[CONJECTURE]**, unscored pending demonstration.

A positive EXP068 result therefore licenses **"a better-validated mechanism"**, not a
novelty-tier jump: it would show that per-instance selection over candidate bases produces
causal transfer gains where static CAA injection does not, under the pre-registered
conditions. It would **not** license N2 ("novel method") language, "invention" claims beyond
what the measurements show (see §14), or any claim that the loop discovers representations
ex nihilo — the candidates are aggregates/perturbations of support contrast directions
(§3.1), and the protocol tests *selection among them*, nothing more.

---

## 2. Frozen model and SHA-256 guard

- **Model / tokenizer (in-scope):** `EleutherAI/pythia-160m` (identical to EXP065).
- **Architecture [FACT]:** GPT-NeoX; 162,322,944 params; $d = 768$; 12 layers; 12 attention heads;
  head dim $d_h = 64$; rotary embeddings; parallel attention/MLP; untied output embeddings.
- **Target layer:** $l^* = 10$ (83% depth, matching EXP065). Intervention $h \leftarrow h + \alpha u$
  via forward hook at $l^*$, last-token position.
- **Out-of-scope pilot:** `EleutherAI/pythia-410m`, $l^* = 20$, may be run only with results
  labeled `OUT-OF-SCOPE PILOT — NO PROTOCOL RULING` (scope discipline per the EXP067 bundle
  review). Budget scaling for 410m is stated as [ESTIMATE — unmeasured] in §12.
- **Expected SHA-256:** `[TO BE REGISTERED at first execution — computed in the execution
  environment]`. This protocol cannot register the value here (no GPU/torch on the drafting
  machine); the value is recorded at first execution before any intervention runs.
- **Guard procedure [FACT-level requirement]:** SHA-256 over the concatenation of
  `model.state_dict()` tensors (sorted keys, CPU, float32 bytes) computed (i) before tuning,
  (ii) before the ρ-gate, (iii) before the test phase, and (iv) after the test phase.
  **Per-instance binding** (loop spec §3): hash recorded pre-loop and post-loop per test
  instance; any mismatch aborts the run as a protocol violation. The **binding** guard is the
  runtime pre/post match; a registered value, once recorded, is a sanity check only (E-4
  distinction, EXP067 §2). $\boxed{\Delta\theta \equiv 0}$ is non-negotiable (Law #6).

---

## 3. Formal mechanism (carried over from the signed loop spec)

[DEFINITION] The loop instantiates the SCBI tuple per-instance: $B^*(x)$ temporary within one
inference episode, discarded afterwards; no backward pass anywhere; $B_0 := B_{\mathrm{agg}}
= \mathrm{normalize}(\sum_{k=1}^{5} \hat{v}_k)$ (the static aggregated contrast basis of
EXP064–066) as the conservative incumbent; $z_0 := (0, \{\})$. All operator definitions
($\mathcal{G}_1$ bootstrap-resampled contrast aggregation at $t=0$; $\mathcal{G}_2$ local
perturbation at $t \ge 1$; $\mathcal{E}$ via $m=5$ entity-frame-substituted views with
$C_{\mathrm{cons}}$ + clipped self-margin $\tilde{M}$; $\mathcal{S}$ argmax with acceptance
rule $S_E(B_t^*) > S_E(B_t) + \delta$; $\mathcal{T}$ at $T_{\max}$ / two consecutive rejections /
no candidate clearing $\tau_{\min}$) are **inherited verbatim** from `theory/LOOP_SPEC_DRAFT.md`
§§1–2.5. This protocol pins the implementation choices the spec left to pre-registration:

### 3.1 Hyperparameter freezing (operationalization of LOOP_SPEC_DRAFT §1.1)

[DEFINITION] All ten hyperparameters are frozen by **coordinate-wise** search on
$\mathcal{D}_{\mathrm{tune}}$ only. The actual execution order is fixed here (correcting the
first draft, which listed $\delta$ last while the shared-trajectory batch necessarily selects
it earlier):
$$\alpha \to K \to \sigma \to D_{\min} \to [\text{shared batch: } T_{\max},\, \delta] \to
(\lambda_c,\lambda_m) \to \tau_{\min},$$
each step evaluated with not-yet-tuned coordinates at provisional defaults
$(\alpha{=}0.5,\ K{=}8,\ \sigma{=}0.1,\ D_{\min}{=}0.2,\ T_{\max}{=}5,\ \lambda_c{=}0.7,\
\tau_{\min}{=}\text{median},\ \delta{=}0.02)$, using the objectives, grids, and deterministic
selection rules of LOOP_SPEC_DRAFT §1.1 ($m=5$ fixed, not tuned). The shared batch uses the
by-then-tuned $(\alpha, K, \sigma, D_{\min})$ with provisional $(\lambda_c{=}0.7,\
\tau_{\min}{=}\text{median},\ \delta{=}0.02)$; the $(\lambda_c,\lambda_m)$ step uses the frozen
$(T_{\max}, \delta)$; the $\tau_{\min}$ step uses all other coordinates frozen.
Coordinate-wise (not joint) search is the only compute-feasible reading of §1.1; it is
pre-registered here, not invented at execution. Coordinate interactions — in particular
$\delta$ selected under provisional $\lambda_c$ — are a named limitation of the design, not a
post-hoc excuse.

[DEFINITION] **Shared-trajectory optimization (pre-registered):** $T_{\max} \in \{3,5,8\}$ and
$\delta \in \{0, 0.02, 0.05\}$ are selected from a **single** set of recorded loop trajectories
on a fixed 20-item subset of $\mathcal{D}_{\mathrm{tune}}$ (fixed seed, run once at $T_{\max}=8$
with provisional $\lambda_c = 0.7$ and provisional $\delta = 0.02$ acceptance), as follows.
$T_{\max}$ **by truncation:** each recorded trajectory is truncated at $t=3,5,8$ and its
objective applied — **exact**, because $T_{\max}$ is a pure stop cap and trajectory prefixes
are invariant under it. $\delta$ **by recomputation:** acceptances are recomputed offline under
each $\delta$ value (no new forward passes) — **[APPROXIMATION]:** the recorded trajectories
were generated under the provisional $\delta = 0.02$ acceptance path; wherever a counterfactual
$\delta'$ flips an acceptance decision, $B_{t+1}$ changes and $\mathcal{G}_2$'s subsequent
candidate sets diverge from the recorded history. The bias direction is unknown. Its influence
is bounded by pre-registration: $\delta$ affects only the acceptance threshold, the grid has
3 values, and $\delta$ is frozen before the ρ-gate. The first draft's claim that recomputation
is "legitimate because the loop records the full $S_E$ history" is **withdrawn for $\delta$**
(it holds for $T_{\max}$ only); honesty, not compute, is the issue (Law #11).

[DEFINITION] **Tuning budget cap:** total tuning forward passes $\le 15{,}000$ [ARBITRARY —
accounting required]. Estimated cost under this design: $T_{\max}$/$\delta$ shared runs
($20 \times 365 = 7{,}300$) + $\lambda$ selection ($\approx 4{,}800$) + $\tau_{\min}$
($500$) + $\alpha$ ($100$) + $K$/$\sigma$/$D_{\min}$ ($\approx 0$ forwards) $\approx 12{,}700$.
If the cap binds, tuning stops and best-found values freeze (documented as budget-limited).
Full per-step accounting is archived per Law #13.

### 3.2 Leakage hardenings (applied; were non-blocking in Phase 2 review §8.3)

- [DEFINITION] **$\mathcal{G}_1$ draws exclusively from $\mathcal{D}_{\mathrm{tune}}$ at all
  times** — during tuning, during the ρ-gate, during the transfer probe (§4b), and during the
  test phase. $\mathcal{D}_{\mathrm{gate}}$ is quarantined after the gate: neither its vectors
  nor its labels are used thereafter. (The Phase 2 review §8.3(i) gate-time fix is extended to
  the test phase here — not as "the conservative reading" of that fix but as a
  **disambiguation of a loop-spec ambiguity**: LOOP_SPEC_DRAFT §2.1 says "support contrast
  pairs ($k=1..5$, $j=1..30$)" without specifying the post-S3-split resampling source.
  Rationale for the chosen reading: it keeps the $\mathcal{D}_{\mathrm{gate}}$ quarantine
  auditable, it makes the gate and test generator-distributions identical (so the ρ-gate's
  validation applies cleanly), and it is a *harder* test for the loop. **Conceded cost:**
  test-phase candidates are weaker than the spec's 150-pair resampling, so the tested object
  is the $\mathcal{D}_{\mathrm{tune}}$-restricted loop variant — a critic may note this, and
  it is conceded here rather than left to be discovered.)
- [DEFINITION] **Margin-normalization parameters $\mu_M, \sigma_M$ are computed on
  $\mathcal{D}_{\mathrm{tune}}$ only** (not full $\mathcal{D}_{\mathrm{sup}}$; Phase 2 review
  §8.3(ii)).
- [DEFINITION] **Any use of $\mathcal{D}_{\mathrm{gate}}$ outside the ρ-gate measurement, or
  any tuning access to test labels, invalidates the run** (Law #7). The leakage audit is part
  of the run record.

### 3.3 View-construction precondition (LOOP_SPEC_DRAFT §2.2)

[DEFINITION] Every test item must expose $(\tau(x), \{(e_i, \sigma_i)\}_{i=1}^{s})$ (template +
typed entity slots); views $x_j := \tau(x)[e_i \mapsto \varphi_j(e_i)]$ use the
slot-index-aligned map into each of the 5 support vocabularies. A test item whose
template/slot signature is unavailable is **excluded from loop evaluation and logged**
(Law #8); its views are never improvised. Excluded items are reported with the run.

---

## 4. The ρ-gate (FIRST gate; §4.3b of the loop spec, operationalized)

[DEFINITION] **Purpose:** measure whether the evaluator $\mathcal{E}$ — specifically the
$S_E = \lambda_c C_{\mathrm{cons}} + \lambda_m \tilde{M}$ form with frozen hyperparameters —
carries information about real rescue success, on data no tuning step has touched. The gate
is computed **after** hyperparameter freezing and **before** any test-phase evaluation.

[DEFINITION] **Rescue indicator (G1).** For candidate $B$ on item $x$ with true label $y$:
$$\mathbf{1}[\mathrm{rescue}(B;x)] := \mathbf{1}[\hat{y}(B;x) = y \;\land\;
\hat{y}(\emptyset;x) \neq y],$$
i.e. TRUE rescue: intervened-correct where unintervened-wrong, with $\hat{y}(\emptyset;x)$ the
unintervened decision on $x$. Measuring it costs one additional unintervened forward pass per
item (budgeted in §12: +50 for the gate, +15 for the transfer probe; the $K{\cdot}m{+}K{+}m$
term does not cover it). This definition is used identically in the ρ-gate, the transfer
probe (§4b), and the G3 diagnostic.

[DEFINITION] **Procedure.** For each of the 50 items $x \in \mathcal{D}_{\mathrm{gate}}$:
(i) draw $K$ candidates via $\mathcal{G}_1$ (resampling $\mathcal{D}_{\mathrm{tune}}$ only, §3.2);
(ii) compute $S_E(B;x)$ for each candidate over the $m=5$ views; (iii) measure the true rescue indicator $\mathbf{1}[\mathrm{rescue}]$ (G1 definition above)
for each candidate by intervened forward pass, using $\mathcal{D}_{\mathrm{gate}}$ labels
(permitted: validity measurement, not test time; Law #7).
$B_0$ is **excluded** from the gate candidate set — the gate tests $\mathcal{E}$'s ability to
discriminate *among candidates*, which is its actual job inside the loop; including the known
incumbent would anchor the correlation artifactually. The loop's $\mathcal{S}/\mathcal{T}$
are **not** exercised in the gate (the gate measures $\mathcal{E}$, not the loop).

[DEFINITION] **Primary analysis (pre-registered):** per-instance top-$S_E$ candidate,
$n = 50$ independent pairs $(S_E(B^\star(x)), \mathbf{1}[\mathrm{rescue}])$.
Test statistic: point-biserial $\hat\rho$. **GO iff $\hat\rho > 0$ AND one-sided exact
permutation $p < 0.05$.** Exploratory: candidate-level $\hat\rho$ over all $50 \times K$
pairs (reported with the clustering caveat — candidates within an instance are dependent).
**Range-restriction note (M4):** the primary analysis conditions on the per-instance argmax,
which attenuates $\hat\rho$ — conservative for a gate, stated here; the candidate-level
analysis is the less-attenuated complement.

[DEFINITION] **Permutation-test parameters (pinned, Law #13; closes M5.3 MINOR).** The
one-sided $p$ is the Monte Carlo approximation to the exact permutation p-value with
**$B = 9{,}999$** random label permutations, plus-one convention
$p = (1 + \#\{\hat\rho_{\mathrm{perm}} \ge \hat\rho_{\mathrm{obs}}\})/(1 + B)$, and fixed seed
**`perm_seed = 68026`** [ARBITRARY — any fixed value; recorded here; the seed and the realized
$p$ are archived in the gate record per Law #13]. Rationale in one line: at the $p = 0.05$
decision boundary the Monte Carlo standard error is
$\sqrt{0.05 \cdot 0.95 / 9999} \approx 0.0022$ — tight enough that the estimate is stable at
the boundary — and the pinned seed makes the realized ruling deterministic and exactly
reproducible, so no rerun can flip the verdict.

[DEFINITION] **Degenerate-gate rule (pre-registered; mirrors §4b; closes the ρ-gate
partition gap, M5.2).** If the rescue indicator $\mathbf{1}[\mathrm{rescue}]$ has zero variance
on $\mathcal{D}_{\mathrm{gate}}$ — i.e. all 50 gate items are rescued by their top-$S_E$
candidates, or none is — the point-biserial $\hat\rho$ and its permutation $p$ are undefined
(NaN; NaN comparisons evaluate False, so the GO rule above would pass the gate vacuously).
The gate is then **inconclusive**: **HALT**, reported exactly as branch (a) with the degenerate
case named ("ρ-gate degenerate — rescue indicator constant on $\mathcal{D}_{\mathrm{gate}}$;
evaluator unscreened"). A degenerate gate must NOT pass and must NOT be silently dropped — a
vacuous pass would license the test phase on an evaluator the gate measured nothing about.
Report: $\hat\rho$ and $p$ recorded as undefined, plus the zero-variance indicator record and
the gate rescue base rate. Motivation: this is expected-scale, not pathological — e.g. at
rescue base rate 0.9, P(all 50 gate items rescued) $\approx$ 0.005; the G2 low-information flag
already anticipates sparse rescue, and a constant indicator is its limiting case.

**Justification of the threshold:** the $\hat\rho > 0$ requirement is inherited from the loop
spec's F1 ($\rho \le 0 \Rightarrow$ invalid). The $p < 0.05$ requirement is [CONVENTIONAL]
significance practice, and at $n=50$ it is non-degenerate: one-sided $p < 0.05$ implies
$\hat\rho \gtrsim 0.235$, i.e. the gate simultaneously imposes a moderate effect-size floor —
a positive-but-noise correlation cannot license the test phase. $\hat\rho$ is reported with
a 95% CI regardless of outcome.

[DEFINITION] **Rescue base-rate reporting (G2).** The gate record reports the gate items'
baseline accuracy (unintervened) and the rescuable fraction
$\mathbf{1}[\hat{y}(\emptyset;x) \neq y]$. If the rescuable fraction is below 10%, the gate
outcome is **flagged low-information** — reported, not a halt: the test phase remains the
arbiter. Rationale: sparse $\mathbf{1}[\mathrm{rescue}]$ makes $\hat\rho$ unstable; a pass on
a low-information gate licenses the test phase weakly, and the report must say so.

[DEFINITION] **$B_0$-relative $\Delta$-diagnostic (exploratory, not gating; +300 passes, §12).**
$B_0$ is excluded from the gate candidate set (above), but the loop also uses $\mathcal{E}$ to
compare candidates against the incumbent (acceptance rule $S_E(B_t^*) > S_E(B_t) + \delta$,
$B_0 = B_{\mathrm{agg}}$), and that comparison is never validated by the gate. Companion
diagnostic: per gate instance compute $S_E(B_0;x)$ over the $m$ views and
$\mathbf{1}[\mathrm{rescue}(B_0;x)]$ (6 additional forward passes per gate item), and report
$\mathrm{corr}(\Delta S_E, \Delta\mathrm{rescue})$ with $\Delta$ taken relative to $B_0$.
This tests the acceptance rule's premise on held-out data; it gates nothing (the incumbent
comparison is also tested in the test phase via F3).

[DEFINITION] **Halt semantics.** If the gate fails: **HALT — $\mathcal{E}$ invalid.** No test
phase runs. No silent fallback to the margin heuristic (dropping $\tilde{M}$ / setting
$\lambda_m = 0$ post-hoc and re-gating is a **design change = EXP069**, explicitly forbidden).
The halt is a **reportable outcome** (§11 branch (a)): "$\mathcal{E}$ uninformative on held-out
support data; H_loop untestable under this evaluator" — not a non-result. Archive the full
gate record (per-item $S_E$, rescue indicators, $\hat\rho$, CI, $p$).

---

## 4b. The transfer probe (SECOND gate; required by adversarial review T1)

[DEFINITION] **Purpose (the transfer hole).** The ρ-gate (§4) validates $\mathcal{E}$ on
$\mathcal{D}_{\mathrm{gate}}$: 50 **support-distribution** items (support vocabularies
V1–V5). The test phase runs the loop on **novel-vocabulary** items (planets/elements). The
gate establishes "agreement across support views tracks rescue on support-vocabulary items";
the test phase needs "agreement across support views tracks rescue on novel-vocabulary
items." Without a check, transfer failure presents as: gate passes, then C3
$\Delta M \le 0$ on test items — and branch (d) would license the **structural** reading
("the dissociation is structural, not operator-quality") when the correct reading is
"$\mathcal{E}$ doesn't transfer" — a verdict on the instrument, not the loop hypothesis.
A labeled [ASSUMPTION] does not close this hole (Law #4). This probe is the protocol-level
check.

[DEFINITION] **$\mathcal{D}_{\mathrm{xfer}}$.** Before any test-phase execution, 15 items are
carved from the N=60 test suite by fixed pre-registered seed (`carve_seed = 68024`
[ARBITRARY — any fixed value; recorded here]) and permanently excluded from the confirmatory
set afterward. **The test phase runs on the remaining N=45.** The carved items are
novel-vocabulary relational items exposing $(\tau, \mathrm{slots}, t_{\mathrm{target}},
t_{\mathrm{foil}})$ per §3.3; labels are used for probe measurement only — validity
measurement, not test time (the Law #7 logic of the gate).

[DEFINITION] **Procedure.** Identical to the §4 gate on the 15 probe items: (i) $K$ candidates
via $\mathcal{G}_1$ from $\mathcal{D}_{\mathrm{tune}}$ only; (ii) $S_E$ over $m=5$ views;
(iii) true rescue indicators $\mathbf{1}[\mathrm{rescue}]$ under the §4 (G1) definition;
per-instance top-$S_E$ candidate; point-biserial $\hat\rho_{\mathrm{xfer}}$; one-sided exact
permutation $p$.

[DEFINITION] **Halt rule (pre-registered).** **HALT iff $\hat\rho_{\mathrm{xfer}} \le 0$ or
one-sided $p \ge 0.20$.** Rationale (pre-registered): the probe is a *degradation screen*,
not a second confirmatory gate. The arithmetic is principled, not arbitrary: at $n=15$,
one-sided $p = 0.20$ corresponds to $t \approx 0.87$ (df=13), i.e. $\hat\rho \lesssim 0.235$ —
**exactly the gate's effect-size floor**, re-expressed at reduced $n$. The probe therefore
applies the *same* effect-size standard as the gate instead of demanding
$\hat\rho \gtrsim 0.44$ (which $p < 0.05$ at $n=15$ would require, halting valid-but-noisy
transfers). **Pre-registered risk (stated DGP).** Monte Carlo under a biserial-normal DGP —
$R \sim \mathrm{Bernoulli}(b)$,
$S = \rho(R-b)/\sqrt{b(1-b)} + \sqrt{1-\rho^2}\,\varepsilon$ with
$\varepsilon \sim \mathcal{N}(0,1)$ independent (population point-biserial correlation
exactly $\rho$ — the protocol's natural reading of "true $\rho$"), $n=15$, one-sided
permutation test on the point-biserial $\hat\rho$ with the halt rule above including the
degenerate-probe rule below (12,000 reps, 499 random permutations per rep): P(false halt)
$\approx$ 10–12% at true $\rho = 0.5$ and $\approx$ 3–5% at true $\rho = 0.6$, across base
rates $b \in \{0.3, 0.5, 0.7\}$ (degenerate probes, counted as halts, contribute $\le 0.5\%$
at these base rates). Sensitivity to true $\rho = 0$ is $80\%$ by construction (P(pass |
$\rho = 0$) = P(one-sided $p < 0.20$) $= 0.20$; independent MC: 0.805). Cross-validated:
independent Monte Carlo in the adversarial review (report §14.2) gives 10–13.5% / 3–5%
under latent-normal DGPs at the same base rates. **DGP sensitivity (named):** the original
draft's 18%/10% belonged to an unstated DGP and could not be reproduced — those numbers are
replaced here, not silently kept. Under a latent-normal DGP that correlates $S$ with the
latent $Z$ instead ($\rho_{SZ} = 0.5/0.6$), the same halt rule false-halts $\approx$ 22–26%
/ $\approx$ 12–16%: a larger cost, honestly disclosed. The disclosure stands or falls with
the stated DGP above; any re-derivation must state its own.
A halt is a reportable outcome ("$\mathcal{E}$ does not transfer"), not a wasted run.

[DEFINITION] **Degenerate-probe rule (pre-registered).** If the probe rescue indicator
$\mathbf{1}[\mathrm{rescue}]$ has zero variance on $\mathcal{D}_{\mathrm{xfer}}$ — i.e. all
15 probe items are rescued by their top-$S_E$ candidates, or none is — the point-biserial
$\hat\rho_{\mathrm{xfer}}$ and its one-sided permutation $p$ are undefined (NaN; NaN
comparisons evaluate False, so the halt rule above would pass the probe vacuously). The
probe is then **inconclusive**: **HALT** with an (a2)-style reportable outcome ("transfer
unscreened — probe degenerate"), reported exactly as branch (a2) with the degenerate case
named. A degenerate probe must NOT pass and must NOT be silently dropped — a vacuous pass
would resurrect the transfer confound the probe was built to kill (T1), after which branch
(d) could fire with its structural reading. Motivation: this is expected-scale, not
pathological — at rescue base rate 0.9, P(all 15 probe items rescued) $\approx$ 0.21. The
ρ-gate's analogous degeneracy is softened by its G2 low-information flag; the probe carries
no base-rate screening, so the rule must live here. The run record reports the probe rescue
base rate alongside any degenerate outcome.

[DEFINITION] **Order of phases:** tuning (§3.1) → ρ-gate (§4) → transfer probe (§4b) →
headroom gate on the 45 (§7) → test phase on the 45 (§§6–11).

[DEFINITION] **Branch (a2)** (see §11): transfer-probe HALT. The canonical falsification
(branch (d)) and its structural interpretation are **conditional on probe passage** — the (d)
rider states this explicitly.

---

## 5. Support split and quarantine

[DEFINITION] **Item structure (verified, not assumed; T4).** Tune/gate items are the support
pairs' $p_{\mathrm{rel}}$ relational prompts ("Premise: A outranks B… Question: Who is higher in
rank…?") with the structure $(\tau, \{(e_i,\sigma_i)\}, t_{\mathrm{target}}, t_{\mathrm{foil}})$
(template, typed entity slots, target/foil tokens) and a determinate correct answer; the
$p_{\mathrm{neu}}$ prompts are construction scaffolding for $\Delta h$ only. Verified against
`run_exp065_temporary_coordinate_alignment.py` (support-item construction), not assumed from the
loop spec's "holds by construction." An implementer must not reverse-engineer EXP065 to
discover what $x \in \mathcal{D}_{\mathrm{gate}}$ *is*. If any tuning objective or
gate/probe measurement cannot be computed on support items as constructed, that is a protocol
defect to fix now (this pre-registration asserts computability), not at execution.

[DEFINITION] Before any tuning, $\mathcal{D}_{\mathrm{sup}}$ (the 150 support contrast pairs,
$5 \times 30$) is partitioned once, by fixed seed, into disjoint stratified subsets:
$\mathcal{D}_{\mathrm{tune}}$ (20 pairs/vocabulary, 100 pairs) and $\mathcal{D}_{\mathrm{gate}}$
(10 pairs/vocabulary, 50 pairs) — per LOOP_SPEC_DRAFT §1.

| Data | Permitted uses | Forbidden uses |
|---|---|---|
| $\mathcal{D}_{\mathrm{tune}}$ (+ labels) | all hyperparameter tuning (§3.1); $\mathcal{G}_1$ resampling (always); $\mu_M,\sigma_M$ fitting | — |
| $\mathcal{D}_{\mathrm{gate}}$ (+ labels) | **ρ-gate measurement only** (§4) | tuning; $\mathcal{G}_1$ resampling; any post-gate use (quarantined) |
| $\mathcal{D}_{\mathrm{xfer}}$ (+ labels, 15 items) | **transfer-probe measurement only** (§4b) | test-phase evaluation (permanently excluded after the probe) |
| Test items (N=45 confirmatory) | loop evaluation; all conditions | label access by $\mathcal{G}$ or $\mathcal{E}$ at any time (Law #7) |

---

## 6. Conditions (8)

| # | Condition | Intervention / procedure |
|---|---|---|
| C1 | Unintervened baseline | none |
| C2 | Static $B_{\mathrm{agg}}$ (CAA-equivalent benchmark) | $h \leftarrow h + \alpha B_{\mathrm{agg}}$, $\alpha$ tuned (§3.1), else 0.5 |
| C3 | **Loop-selected per-instance direction (EXP068 mechanism)** | full $\mathcal{G}/\mathcal{E}/\mathcal{S}/\mathcal{T}$ per §§3–4; final $B^*(x)$ injected at strength $\alpha$ |
| C4 | Random-selection loop ablation | computes $S_E$ **identically** to C3 (same candidate sets, same forward passes) but selects uniform-random over $\mathcal{C}_t$ (seed-fixed), **ignoring** the computed scores — isolates the evaluator's *selection* contribution at identical compute ("any loop works" killer). The wasted compute is the price of a clean attribution control (cf. the EXP067 bundle review's F1 lesson: a control must never silently do less than its label claims). |
| C5 | Static $B_\perp$ | specificity control (seed 9876, inherited) |
| C6 | Static $B_{\mathrm{wrong}}$ | wrong-task control (Paris-capital contrast, as EXP066) |
| C7 | Compute-matched output-level search | per-instance Best-of-$N(x)$: $N(x) = F(x)$ (the loop's actual forward count on that instance), temperature $0.7$ [ARBITRARY], BoN sampling seed $68025$ [ARBITRARY — pre-registered, Law #13]; per-sample vote $:= \arg\max_{t \in \{t_{\mathrm{target}}, t_{\mathrm{foil}}\}} \mathrm{logit}_t$ (restricted two-token decision, matching the primary endpoint — defined even when the sample's top-1 token is neither); majority vote over the $N(x)$ per-sample decisions; ties $\to$ unintervened decision |
| C8 | Same-layer output bridge (positive control) | identical to EXP066 `make_bridge_vec` |

**[NOTE] on C7 budget-matching (honest bias direction):** $N(x) = F(x)$ matches the loop's
realized per-instance forward count exactly. But in *decision-sample* terms the matching is
**generous to BoN**: BoN gets $F(x)$ decision samples while the loop's $F(x)$ includes
non-decision $\mathcal{E}$ passes — so F5 is biased **conservatively against the loop**. This
is pre-registered and intended (A-budget, §9). The first draft's "C7 can never be accused of a
compute advantage in either direction" was an overclaim and is **withdrawn**. Temperature
$0.7$ is [ARBITRARY — sensitivity analysis required]; the per-sample vote, majority-vote
rule, and tie-break are pre-registered.

---

## 7. Benchmark and headroom gate

- **Benchmark:** the identical N=60 Planetary/Elemental 2-hop/3-hop suite from EXP065 (same
  items, same premise permutations). No new benchmark construction (Law #9).
- **Headroom gate:** run C1 on the 45 confirmatory items ($\mathcal{D}_{\mathrm{xfer}}$ carved
  in §4b before any test-phase execution); require baseline accuracy $\in [40\%, 70\%]$ on the
  carved 45-set (inherited from EXP067 §5 — program continuity; the recalibration is explicitly
  on the confirmatory set). If outside: **HALT**; any recalibration requires a new
  pre-registration. A headroom halt is reportable (§11 branch (b)), not adjustable under EXP068.

---

## 8. Endpoints

- **Primary (confirmatory):** $\Delta M$ (percentage points) on paired decisions, C3 vs C1;
  McNemar exact two-sided test on $(b, c)$. **Success:** $\Delta M > 0$ **and** $p < 0.05$.
- **Secondary (pre-registered):** C3 vs C2 (beats static-CAA; paired McNemar, $p < 0.05$
  required); C3 vs C7 (beats output-level search at matched $F$; paired McNemar on the
  (loop, BoN) decision pairs, $p < 0.05$ required for the F5 ruling); C3 vs C4 (attribution:
  $p \ge 0.05$ or $\Delta M_{\mathrm{loop}} \le \Delta M_{\mathrm{rand}}$ ⇒ **no *demonstrated*
  $\Delta M$ contribution** of the evaluator beyond search — a non-significant difference is
  a failure to demonstrate, not a proof of absence; the full $(b,c)$ decomposition for C3 vs
  C4 is reported, since equal net $\Delta M$ can hide different risk profiles); rescues $b$ / corruptions $c$; $\mathrm{KL}_{\mathrm{div}} < 0.50$
  guardrail (inherited, exploratory); per-instance $F(x)$ accounting; $D(\mathcal{C}_t)$
  trace (effective candidate count — OQ4); F2/F4 diagnostics (§10).
- **Margin shifts:** recorded but **exploratory only** — audit Finding 3 / O5 stands: the
  $B_{\mathrm{wrong}}$ control invalidates margin-shift significance as a causal endpoint.
  The self-margin term $\tilde{M}$ inside $S_E$ is a *selection heuristic*, licensed solely by
  the ρ-gate (§4.3(d) of the loop spec) — never reported as confirmatory evidence.

---

## 9. Assumptions (named, not smuggled)

- **[ASSUMPTION] A-eval:** cross-view decision agreement $C_{\mathrm{cons}}$ (and the
  $S_E$ composite) tracks real rescue success. This is the loop's analogue of EXP067's
  A-uniform: it is **tested by the ρ-gate** (§4), not assumed blindly. A passed gate
  supports A-eval on $\mathcal{D}_{\mathrm{gate}}$.
- **[ASSUMPTION] A-eval-transfer:** an evaluator validated on $\mathcal{D}_{\mathrm{gate}}$
  (support-distribution items) remains valid on the test items (novel-vocabulary relational
  items). **Tested by the transfer probe (§4b)** — the probe screens the
  support→novel-vocabulary transfer that the gate cannot establish. Residual risk (named):
  the probe is a degradation screen, not a proof of transfer.
- **[ASSUMPTION] A-view:** entity-frame substitution ($\varphi_j$) preserves the relational
  query across vocabularies. Implicitly tested by the gate (broken views ⇒ noisy $S_E$ ⇒
  gate failure); residual risk named here.
- **[ASSUMPTION] A-budget:** per-instance $F(x)$ is the right compute-matching unit for C7.
  Pre-registered in §6; alternatives (fixed-$N$) noted as variants for future work.

---

## 10. Kill criteria F1–F5 (pre-registered; F1 halts, F2–F5 are falsification triggers; Law #4)

**F1 — Invalid evaluator:** ρ-gate fails ($\hat\rho \le 0$ or one-sided permutation
$p \ge 0.05$, or degenerate zero-variance gate → inconclusive, §4). ⇒ HALT before test (§4);
the loop may not proceed.

**F2 — Collapse to static:** $\cos(B^*(x), B_{\mathrm{agg}}) > 0.95$ on $> 80\%$ of test
instances. ⇒ The loop re-discovers the static CAA direction; no per-instance adaptation is
occurring. Thresholds [ARBITRARY — sensitivity analysis required]; inherited from the loop spec.
**Report the full $\cos(B^*(x), B_{\mathrm{agg}})$ distribution** (the [ARBITRARY] tags promise
sensitivity analysis — the data is delivered here).

**F3 — No gain over the known mechanism:** paired McNemar C3-vs-C2 gives $p \ge 0.05$ or
$\Delta M_{\mathrm{loop}} \le \Delta M_{\mathrm{static}}$. ⇒ The loop adds nothing beyond the
N0 mechanism. **Attribution rider (pre-registered):** if additionally C3-vs-C4 gives
$p \ge 0.05$ or $\Delta M_{\mathrm{loop}} \le \Delta M_{\mathrm{rand}}$, there is **no
*demonstrated* $\Delta M$ contribution** of the evaluator beyond search — a non-significant
difference is a failure to demonstrate, not a proof of absence; the full $(b,c)$
decomposition for C3 vs C4 is reported ("gain without attribution", §11 branch (f)).

**F4 — Shared blind-spot confirmation:** mean $C_{\mathrm{cons}}(B^*) \ge 0.8$ while
$\Delta M_{\mathrm{loop}} \le 0$. ⇒ High self-consistency with no accuracy gain: the
Self-Refine failure mode reproduced at the representation level. The $0.8$ threshold is
[ARBITRARY — sensitivity analysis required]; inherited from the loop spec. **Precedence (K4):**
F4's condition is essentially a subset of branch (d)'s; when both fire, **(d) is the canonical
ruling** and F4 is reported as the *diagnostic characterization* of the (d) outcome. Overlap
stated honestly: with $\lambda_c$ tuned high, $C_{\mathrm{cons}}(B^*) \ge 0.8$ is expected
*by construction*, so F4 ≈ (d) + "the loop did what it was told." **Report the
$C_{\mathrm{cons}}(B^*)$ distribution regardless** (sensitivity-analysis data).

**F5 — Dominated by output-level search:** $\Delta M_{\mathrm{BoN}} > \Delta M_{\mathrm{loop}}$
**and** paired McNemar on (loop, BoN) decisions gives $p < 0.05$. ⇒ Representation-level
search adds nothing over output-level search at matched compute. "Significantly greater" is
operationalized as this exact test ([CONVENTIONAL] $\alpha = 0.05$).

**Positive criterion (conjunctive — all required):** $\Delta M_{\mathrm{loop}} > 0$,
McNemar $p < 0.05$ (C3 vs C1); C3 beats C2 ($p < 0.05$); C3 beats-or-ties C7 (F5 not
triggered); ρ-gate passed; transfer probe passed (§4b); F2 and F4 diagnostics negative.

---

## 11. Pre-registered decision tree

**Branch precedence (pre-registered, Law #4):** (a)/(a2) → (b) → (c) → (d) → (g) → (f) → (e).
Gates and halts are evaluated first; the canonical falsification (d) is checked before the
comparative (g), the mixed (f), and the success (e) branches. Co-firing branches are resolved
by this order — no post-hoc branch assignment.

| # | Branch | Pre-registered ruling — LICENSES / DOES NOT LICENSE |
|---|---|---|
| (a) | **ρ-gate HALT** ($\hat\rho \le 0$ or $p \ge 0.05$; or degenerate zero-variance gate → inconclusive, §4) | $\mathcal{E}$ **invalid** on held-out support data (non-degenerate case). H_loop is **untestable under this evaluator** — neither falsified nor confirmed. LICENSES: "the $S_E$ form as specified carries no measurable signal about rescue." For the degenerate case the gate is **inconclusive, not invalid**: "the gate measured nothing about $S_E$'s signal — rescue indicator constant on $\mathcal{D}_{\mathrm{gate}}$; evaluator unscreened." DOES NOT LICENSE: "the loop fails" (the loop never ran); "no evaluator could work" (only this $S_E$ form was tested). Report $\hat\rho$, 95% CI, $p$, per-item gate data (for the degenerate case: $\hat\rho$, $p$ recorded as undefined, plus the zero-variance indicator record and the gate rescue base rate). |
| (a2) | **Transfer-probe HALT** ($\hat\rho_{\mathrm{xfer}} \le 0$ or one-sided $p \ge 0.20$; or degenerate zero-variance probe → inconclusive, §4b) | $\mathcal{E}$ **does not transfer** to the test distribution. H_loop is **untestable under this evaluator on this distribution** — neither falsified nor confirmed. LICENSES: "$S_E$ validated on support-distribution items carries no measurable signal on novel-vocabulary items." DOES NOT LICENSE: "the loop fails" (the test phase never ran); "no evaluator could transfer" (only this $S_E$ form tested). Report $\hat\rho_{\mathrm{xfer}}$, $p$, and the per-item probe record (for the degenerate case: record $\hat\rho_{\mathrm{xfer}}$ and $p$ as undefined, and report the zero-variance indicator record and the probe rescue base rate). |
| (b) | **Headroom halt** (baseline outside [40%, 70%]) | **Invalid run** — benchmark miscalibrated. No conclusion about H_loop. Diagnose before any re-registration. |
| (c) | **C8 positive control fails** (bridge: $\Delta M \le 0$ or $p \ge 0.05$) | **Invalid run** — setup broken or benchmark drifted. **No conclusion about H_loop may be drawn**; do not interpret C3 in an invalid run (EXP067 §7.1 branch (b) discipline). |
| (d) | **Canonical falsification:** gate passed, C8 valid, C3 $\Delta M \le 0$ or $p \ge 0.05$ (C3 vs C1) | **H_loop FALSIFIED as specified.** LICENSES: "per-instance selection over basis candidates with this $\mathcal{E}$ yields no causal transfer gain on this benchmark." **Precondition: transfer probe passed.** The
structural interpretation below is licensed *only* because the transfer confound was screened
(§4b); had the probe halted, (a2) — not (d) — would have fired. DOES NOT LICENSE:
"representation-level adaptation is impossible" (only this loop operationalization was
tested); any novelty claim. |
| (e) | **Loop success (all positive-criterion conjuncts hold)** | **H_loop CONFIRMED as specified.** LICENSES (conditional, D2): "per-instance $S_E$-guided
selection yields causal transfer gains over static CAA injection, under these pre-registered
conditions, with $\Delta\theta=0$" — and "beats compute-matched output-level search" **only
if** the C3-vs-C7 McNemar $p < 0.05$ favors C3; otherwise "not dominated by compute-matched
output-level search (F5 not triggered); $\Delta M_{\mathrm{BoN}}$ vs $\Delta M_{\mathrm{loop}}$
reported." DOES NOT LICENSE: N2/novelty-tier movement (framing per §1.1: a better-validated
mechanism); "invention" beyond selection among support-derived candidates (§14);
generalization beyond pythia-160m / $l^*=10$ / this benchmark family. |
| (f) | **Mixed / ambiguous:** (f1) C3 beats C1 but not C2 (F3); (f2) C3 beats C2 but C3 $\approx$ C4 — gain without attribution; (f3) F2 collapse with $\Delta M > 0$ — gain attributable to the static direction, not adaptation; (f4) F4 blind-spot pattern — characterized under (d)+F4 | H_loop **not confirmed**; report the exact failure mode with full statistics. (f1) LICENSES:
"per-instance selection yields gains over baseline fully accounted for by the static CAA
direction; no evidence of adaptation benefit." DOES NOT LICENSE: "the loop is useless" (it
matched static; the failure is *adaptation*, not *steering*). (f2) LICENSES: "no demonstrated
evaluator contribution to $\Delta M$" (a non-significant C3-vs-C4 difference is a failure to
demonstrate, not a proof of absence). (f3) LICENSES: "the loop re-discovers CAA; per-instance
adaptation is not occurring." Each sub-branch is a distinct publishable negative result (Law #8). |
| (g) | **F5 triggers** (C7 dominates C3, $p < 0.05$) | H_loop **not confirmed as specified** (the positive criterion is conjunctive). LICENSES: "at matched compute, output-level search dominates representation-level search here." DOES NOT LICENSE: "the loop's evaluator is invalid" (ρ-gate may have passed — the failure is comparative, not absolute). |

**[INTERPRETATION] of branch (d):** the falsification would show that even a validity-gated,
per-instance selection loop cannot extract causal transfer from cross-vocabulary contrast
structure at this scale — strengthening the boundary claim toward "the dissociation is
structural, not operator-quality" (cf. EXP067 §7.0). **Precondition: transfer probe passed —
the structural reading is licensed only because the transfer confound was screened (§4b).**
The program then pivots to *where* the
causal chain breaks, not to better search.

---

## 12. Budget and compute plan (free-tier feasibility)

[DEFINITION] Primary compute metric: forward passes per instance,
$F(x) \le m \cdot (1 + K \cdot (T(x)+1))$ (loop spec §2.5).

| Phase | Worst-case bound | Basis |
|---|---|---|
| Tuning (§3.1) | $\le 15{,}000$ passes | pre-registered cap [ARBITRARY] |
| ρ-gate (§4) | $\approx 2{,}700$ passes | $50 \times (K{\cdot}m + K + m)$ at $K{=}8$ (= 2,650) + 50 unintervened rescue-baseline passes (G1) |
| G3 $B_0$-diagnostic (§4) | $+300$ passes | $50 \times 6$ ($S_E(B_0)$ over 5 views + 1 rescue pass per gate item) |
| Transfer probe (§4b) | $\approx 810$ passes | $15 \times 53$ (= 795) + 15 unintervened rescue-baseline passes |
| Test: C3 loop | $\le 24{,}525$ passes | $45 \times 5(1{+}12{\cdot}9)$ at grid maxima ($K{=}12, T_{\max}{=}8$); **$\le 11{,}025$ at defaults** ($K{=}8, T_{\max}{=}5$) |
| Test: C4 random loop | $\le 24{,}525$ passes | identical to C3 (computes $S_E$, selects random — truly compute-matched, §6 K1) |
| Test: C7 BoN | $\le 24{,}525$ passes | $N(x) = F(x)$ per instance |
| Test: C1, C2, C5, C6, C8 | $225$ passes | $5 \times 45$ single forwards |
| **Total worst case** | **$\approx 93{,}000$ passes** | sum at grid maxima |

**Wall-clock [CONJECTURE — pending hardware measurement]:** at $\approx 0.5$ s/pass on a
free-tier T4 (pythia-160m), worst case $\approx 13$ h; **expected a small fraction of that**
(termination rule (ii) ends most instances far below $T_{\max}$; tuned $K$/$T_{\max}$ are
unlikely to sit at grid maxima). The run is splittable across Kaggle sessions (30 h/week
free quota); phase boundaries (tuning → gate → probe → headroom → test) are natural
checkpoints with all state archived. **Pilot requirement:** measure per-pass wall-clock and
$F(x)$ distribution on 5 pilot instances before full launch; rescale the estimate from
measurement, not from this table.

**pythia-410m scaling [ESTIMATE — unmeasured]:** $\approx 2.5\times$ parameters suggests
$\approx 2$–$3\times$ wall-clock at equal pass counts, but attention/IO scaling is not
modeled here — a 410m run requires its own 5-instance pilot measurement before any full
launch, and remains OUT-OF-SCOPE for protocol rulings.

---

## 13. Reproducibility and hygiene (Law #13; the T-1 lesson)

- **Seeds (pre-registered):** `torch.manual_seed(68023)`, NumPy `68023` [ARBITRARY — any fixed
  value; recorded here]; C4 random-selection seed $68023$; C7 BoN sampling seed $68025$
  [ARBITRARY — recorded here]; $\mathcal{G}_1$ bootstrap / Dirichlet seeds derived
  deterministically per instance; $\mathcal{G}_2$ perturbation seeds derived per $(x, t)$; C5
  $B_\perp$ seed 9876 (inherited); support-split seed fixed and recorded at partition time;
  $\mathcal{D}_{\mathrm{xfer}}$ carve seed $68024$ [ARBITRARY — recorded here].
- **Vector archiving (Law #13):** per test instance archive — all candidate directions
  $\{B_t^{(i)}\}$, all $S_E$ scores, all per-view decisions $\hat{y}_j(B)$, the selected
  $B^*(x)$, $F(x)$, and the full $z_T$ history — plus the gate record (per-item $S_E$,
  rescue indicators, $\hat\rho$, CI, $p$), the transfer-probe record (per-item $S_E$, rescue
  indicators, $\hat\rho_{\mathrm{xfer}}$, $p$) — **gate and probe $\hat\rho$ values are
  reported side-by-side in all outcomes** (tracks degradation even when both pass; recommended
  R1) — and the complete tuning grids with per-step
  accounting. Scalar-only logs are insufficient (T-1 lesson); everything needed to recompute
  any reported number is stored under `experiments/runs/EXP068_loop/`.
- **Hook isolation:** register forward hook per instance, remove after; no inter-instance state
  (temporary $B_t, z_t$ wiped between episodes); `torch.no_grad()` throughout; no optimizer
  constructed (loop spec §3 proof-by-construction).
- **Run record:** environment manifest, model SHA-256 values (§2), excluded items (§3.3),
  rejected candidates (Law #8 — never silently deleted), halt diagnostics if any gate halts.

---

## 14. Non-goals (explicit)

- No claim that the loop "invents" representations: the protocol tests **selection among
  support-derived candidates**. The word "invention" appears in this protocol only in the
  program name and in this prohibition.
- No novelty-tier claim: a positive result is a better-validated mechanism (§1.1), not N2.
- No $\Delta\theta \ne 0$ variant: any parameter update is a different experiment, not EXP068.
- No matrix-valued bases ($k > 1$): silent promotion from vector to matrix is forbidden
  (Definitions §89); the $k=1$ restriction is pre-registered.
- No per-instance $(\alpha, l^*)$ search (loop spec OQ5): fixed $\alpha$, fixed $l^*=10$.
- No post-hoc redefinition of $\mathcal{E}$, the gate threshold, or any kill trigger (Law #4).
  A failed gate, a failed loop, or a failed baseline is a **result**, not a prompt to adjust
  and re-run under EXP068.

---

**Pre-registration checklist:** ☐ support split (100/50, fixed seed) defined ☐ tuning procedure,
actual execution order, defaults, shared-trajectory rule ($T_{\max}$ exact / $\delta$
[APPROXIMATION]), and 15k cap recorded ☐ $\mathcal{G}_1$ D_tune-only
and $\mu_M/\sigma_M$ D_tune-only pinned ☐ ρ-gate procedure, rescue definition, threshold
($\hat\rho>0$, one-sided permutation $p<0.05$, $n=50$), base-rate reporting, $B_0$
$\Delta$-diagnostic, and halt semantics recorded ☐ transfer probe (15 carved items, fixed
seed 68024, halt rule $\hat\rho_{\mathrm{xfer}} \le 0$ or $p \ge 0.20$, branch (a2)) recorded
☐ headroom gate on the 45 confirmatory items ☐ A-eval / A-eval-transfer / A-view
named (A-eval-transfer tested by the probe) ☐ 8 conditions fixed (C4 truly compute-matched;
C7 seed/vote/bias-direction) ☐ SHA-256 guard armed (value TBD at execution)
☐ F1–F5 triggers recorded (F1 halts; F2–F5 falsification triggers) ☐ full decision tree with
precedence, branch (a2), (d) rider, and license statements recorded (§11)
☐ budget table and pilot requirement recorded ☐ Law #13 archiving specified (gate/probe
$\hat\rho$ side-by-side) ☐ §1.1 novelty framing acknowledged ☐ tweak-and-rerun forbidden
(changed design = EXP069).
*No results exist under this protocol. Any deviation is a protocol violation, not a discovery.*
