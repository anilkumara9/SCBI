# Operational Specification of the SCBI G/E/S/T Loop (DRAFT)

**Author role:** Theory Agent
**Date:** 2026-09-23
**Status:** Draft — first operational spec; precedes any EXP068 pre-registration
**Governing docs:** `theory/README_DEFINITIONS.md` (source of truth; §86 notation, §91 tuple),
`AGENTS.md` §5 (labels), `theory/BOUNDARY_CLAIM_FORMALIZATION.md` (H1, O1–O5),
`research/literature/audit_2026-09-23.md` (N1 verdict; PPLM §2.23, Self-Refine §2.24),
`experiments/protocols/EXP067_QKOV_SUBSPACE_PROCRUSTES_SPEC.md` §9 (loop spin-out)

---

## 0. Why this document exists

[FACT] Phase 1 closed with a signed finding: the only potentially-novel component of SCBI —
the dynamic per-instance **Generate / Evaluate / Select / Terminate** loop over candidate
representation bases — has never been tested, and no operational specification of it existed
in any form (Wave 2 review §5; EXP067 §9). This document is that specification. It turns the
slogan "self-consistency evaluator over bases" into an algorithm with inputs, outputs,
mathematical form, and budget — or marks exactly where it cannot.

[DEFINITION] The loop instantiates the abstract SCBI tuple
$\mathcal{S} = (f_\theta, x, z_0, B_0, G, S, C, A, R, U, T)$
(`theory/README_DEFINITIONS.md` §91) for **per-instance** adaptation (§74):
$B^* = B^*(x)$, temporary within one inference episode (§41), discarded afterwards.

**Notation disambiguation** (per Definitions §87): $\mathcal{C}_t$ = candidate set (§18);
$C_{\mathrm{cons}}(B)$ = consistency score (§27); $S_E(B)$ = evaluator score (§21).
$\mathcal{G},\mathcal{E},\mathcal{S},\mathcal{T}$ denote the four loop operators.

**Implementability self-assessment (post-corrections, 2026-09-23).** As first drafted,
this spec's implementability was LOW (adversarial review, Phase 2: undefined $B_0$,
underspecified view construction, unstated tuning objectives, double-dipped
$\rho$-gate). With S1–S4 fixed on paper — $B_0 := B_{\mathrm{agg}}$ and $z_0$ defined
(§1), entity-frame substitution specified with an explicit benchmark precondition
(§2.2), tuning objectives stated for all ten hyperparameters (§1.1), and the support
split separating tuning from gating (§1) — the spec is now honestly rated
**MEDIUM**: an implementation agent can code every operator without inventing missing
definitions. What keeps it from HIGH is scientific risk, not missing specification:
whether $C_{\mathrm{cons}}$ correlates with rescue success ([CONJECTURE], gated by
$\rho$ on $\mathcal{D}_{\mathrm{gate}}$) and whether the blind-spot limit (OQ3/F4) is
fundamental. Those are for EXP068 to discover, not for this document to assume.

---

## 1. Setting and information boundary

[DEFINITION] **Task setting (primary):** the N=60 Planetary/Elemental relational benchmark
family from EXP065/066 — 2-hop/3-hop relational items with a correct target token
$t_{\mathrm{target}}$ and foil $t_{\mathrm{foil}}$ at a fixed answer position.
Target layer $l^*$ (EXP065: $l^*=10$ pythia-160m; EXP066: $l^*=20$ pythia-410m);
intervention $h \leftarrow h + \alpha u$ via forward hook at $l^*$, last-token position.

[DEFINITION] **Information boundary** (Definitions §35): at test time the loop may access
$x$, all activations/outputs of $f_\theta$, and a **support set** $\mathcal{D}_{\mathrm{sup}}$
(disjoint from test; the 5×30 support contrast pairs of EXP065/066). It may **not** access
test labels $y$ (Law #7; Definitions §80). Hyperparameters
$(K, m, T_{\max}, \lambda_c, \lambda_m, \tau_{\min}, \delta, \sigma, D_{\min}, \alpha)$
are fixed on $\mathcal{D}_{\mathrm{tune}}$ only, via the objectives in §1.1
(Laws #7, #9).

[DEFINITION] **Support split (anti-double-dipping; fix S3, 2026-09-23).** Before any
tuning, $\mathcal{D}_{\mathrm{sup}}$ is partitioned once, by fixed seed, into disjoint
stratified subsets: $\mathcal{D}_{\mathrm{tune}}$ (20 pairs/vocabulary, 100 pairs) and
$\mathcal{D}_{\mathrm{gate}}$ (10 pairs/vocabulary, 50 pairs). All hyperparameters
(§1.1) are fixed using $\mathcal{D}_{\mathrm{tune}}$ only. The evaluator-validity gate
$\rho$ (§4.3b) is measured on $\mathcal{D}_{\mathrm{gate}}$ only, which no tuning step
may access. A "valid evaluator" verdict is therefore discovered by measurement on
held-out support data, not manufactured by tuning.

[DEFINITION] **Initial incumbent and state (fix S1/S6, 2026-09-23).**
$B_0 := B_{\mathrm{agg}} = \mathrm{normalize}(\sum_{k=1}^{5} \hat{v}_k)$ — the static
aggregated contrast basis of EXP064–066 — evaluated with the same intervention
strength $\alpha$ (§2.2 computes $S_E(B_0; x)$ exactly as for any candidate:
$h \leftarrow h + \alpha B_0$ over the $m$ views). **Justification**
[INTERPRETATION]: the loop exists to improve on the static CAA-equivalent mechanism
(falsifier F3); initializing the incumbent at $B_{\mathrm{agg}}$ makes the
$t=0$ acceptance rule conservative by construction — a candidate is accepted only if
it strictly beats the static baseline by margin $\delta$. The unintervened model is
*not* a valid incumbent: $S_E$ is defined over interventions, and comparing against
"no intervention" would conflate *any steering* with *better steering*.
[DEFINITION] $z_0 := (0, \{\})$ — iteration counter zero, empty score history.

[DEFINITION] **Representation object:** $B \in \mathcal{B}$ is, in this spec, a single unit
direction $u \in \mathbb{R}^d$ ($k=1$). Matrix-valued bases ($k>1$) are a documented
**variant** (Definitions §57, §89 — silent promotion from vector to matrix is forbidden).

---

## 1.1 Hyperparameter tuning objectives (fix S4, 2026-09-23; all on $\mathcal{D}_{\mathrm{tune}}$ only)

Each hyperparameter is fixed by grid search on $\mathcal{D}_{\mathrm{tune}}$ under a
stated objective; the selected value is frozen before the $\rho$-gate is ever
computed on $\mathcal{D}_{\mathrm{gate}}$. Grids are coarse by design (compute
budget); the selection rule is deterministic (argmax; ties broken toward the
smaller/simpler value). All objectives may use $\mathcal{D}_{\mathrm{tune}}$
labels (hyperparameter validity, Definitions §80 — permitted); $\mathcal{D}_{\mathrm{gate}}$
is never touched during tuning. Full grid results are archived per Law #13.

| Hyperparameter | Grid | Tuning objective (on $\mathcal{D}_{\mathrm{tune}}$) | Selection rule |
|---|---|---|---|
| $K$ (candidates) | {4, 8, 12} | mean candidate diversity $\bar{D}(\mathcal{C}_0)$ at fixed $\sigma$ | smallest $K$ within 10% of max $\bar{D}$ (budget parsimony) |
| $m$ (views) | {5} — fixed | — | fixed at 5 = number of support vocabularies; tuning it would change the view semantics, so it is not tuned |
| $T_{\max}$ | {3, 5, 8} | mean $\Delta S_E = S_E(B_T) - S_E(B_0)$ over tune instances, others fixed | smallest $T_{\max}$ within 5% of max mean $\Delta S_E$ |
| $\lambda_c, \lambda_m$ ($\lambda_c+\lambda_m=1$) | $\lambda_c \in$ {0.5, 0.7, 0.9} | $\rho_{\mathrm{tune}} = \mathrm{corr}(S_E(B), \mathbf{1}[\mathrm{rescue}])$ over tune candidates | argmax $\rho_{\mathrm{tune}}$ (ties → larger $\lambda_c$, consistency-first) |
| $\tau_{\min}$ | {0.25, 0.5, 0.75} quantiles of $S_E(B_0)$ on tune | gate pass-rate stability: fraction of tune instances with $\ge 1$ candidate clearing the bar | median (0.5 quantile); documented, not optimized |
| $\delta$ | {0.0, 0.02, 0.05} | accepted-improvement reliability: $\mathrm{corr}(S_E\text{-gain}, \mathrm{rescue})$ on tune acceptances | smallest $\delta$ with non-negative correlation (ties → 0.02) |
| $\sigma$ (perturb scale) | {0.05, 0.1, 0.2} | mean $\bar{D}(\mathcal{C}_t)$ for $t \ge 1$ at fixed $K$ | argmax (ties → 0.1) |
| $D_{\min}$ | {0.1, 0.2, 0.3} | resample-trigger rate in [5%, 25%] on tune (guard neither dead nor hyperactive) | value with trigger rate closest to 15% |
| $\alpha$ (strength) | {0.25, 0.5, 0.75} | mean $\Delta M$ of static $B_{\mathrm{agg}}$ injection on tune | argmax mean $\Delta M$ (ties → 0.5, program continuity with EXP065/066) |

---

## 2. Operator definitions

### 2.1 $\mathcal{G}$ — Candidate generation

[DEFINITION]
$$\mathcal{C}_t = \mathcal{G}(x, z_t, B_t), \qquad |\mathcal{C}_t| = K,$$
each $B_t^{(i)} \in \mathcal{B}$ a unit direction with a defined intervention role
$h \leftarrow h + \alpha B_t^{(i)}$ (Definitions §15).

**Primary generator $\mathcal{G}_1$ (bootstrap-resampled contrast aggregation), used at $t=0$:**
1. From the support contrast pairs $\{\Delta h_j^{(k)}\}$ ($k=1..5$ vocabularies, $j=1..30$),
   draw $K$ bootstrap resamples (sampling pairs with replacement, stratified by vocabulary).
2. For resample $i$: $\hat{v}^{(i)} = \mathrm{normalize}\big(\sum_{k} w_k^{(i)} \hat{v}_k^{(i)}\big)$,
   where $\hat{v}_k^{(i)}$ is the resampled per-vocabulary mean direction and
   $w^{(i)} \sim \mathrm{Dirichlet}(1,\dots,1)$ a random vocabulary-weight vector
   (this spans per-vocab directions, leave-some-out aggregates, and $B_{\mathrm{agg}}$-like means).
3. Output $\mathcal{C}_0 = \{\hat{v}^{(1)}, \dots, \hat{v}^{(K)}\}$.

**Refinement generator $\mathcal{G}_2$ (local perturbation), used at $t \geq 1$:**
$$\mathcal{C}_t = \{B_t\} \cup
\big\{\mathrm{normalize}(B_t + \varepsilon_i)\big\}_{i=1}^{K-2} \cup \{\hat{v}^{\mathrm{fresh}}\},$$
$\varepsilon_i \sim \mathcal{N}(0, \sigma^2 I_d)$, $\sigma$ fixed on $\mathcal{D}_{\mathrm{tune}}$ (§1.1);
$\hat{v}^{\mathrm{fresh}}$ one fresh $\mathcal{G}_1$ draw (prevents premature collapse).

[DEFINITION] **Candidate diversity** (Definitions §20):
$D(\mathcal{C}_t) = 1 - \mathrm{mean}_{i<j}\cos(B_t^{(i)}, B_t^{(j)})$.
If $D(\mathcal{C}_t) < D_{\min}$ (support-fixed), the draw is rejected and resampled once;
persistent low diversity is logged as representation-collapse risk (Definitions §69–70).

**Budget:** $\mathcal{G}$ costs no forward passes (vector arithmetic on cached support
$\Delta h$'s only).

### 2.2 $\mathcal{E}$ — Candidate evaluation ("self-consistency over bases," operationalized)

[DEFINITION] For candidate $B$ and instance $x$, construct $m$ **views**
$x_1, \dots, x_m$: the same relational query re-instantiated under each of the $m=5$
support entity vocabularies (entity-frame substitution; relation and template fixed).
Views are input-space perturbations **external** to $\mathcal{G}$'s proposal distribution.

For each view $j$, run $f_\theta(x_j; B)$ (intervention $h \leftarrow h + \alpha B$ at $l^*$)
and record the induced decision
$$\hat{y}_j(B) = \arg\max_{t \in \{t_{\mathrm{target}}, t_{\mathrm{foil}}\}}
\mathrm{logit}_t\big(f_\theta(x_j; B)\big)$$
at the answer position, and the self-margin
$$M_j(B) = \max_t \mathrm{logit}_t - \mathrm{secondmax}_t \mathrm{logit}_t$$
(top-1 minus top-2 over the full vocabulary — **target-free**).

[DEFINITION] **View construction (entity-frame substitution), specified (fix S2, 2026-09-23).**
Let test item $x$ carry template $\tau(x)$ and ordered entity-slot filling
$(e_1, \dots, e_s)$ with slot types $(\sigma_1, \dots, \sigma_s)$ (e.g. [PLANET],
[ELEMENT] for the Planetary/Elemental domains). Each support vocabulary $V_j$
($j = 1..5$: Anglo, Biblical, Greek, Roman, Modern) provides a typed lexicon
$\mathcal{L}_j$; the **slot-index-aligned entity map** $\varphi_j$ sends $e_i$ to
the $V_j$ entity occupying the same slot role in the support construction. The view is
$$x_j := \tau(x)\,[e_i \mapsto \varphi_j(e_i)\ \forall i],$$
i.e. identical template wording, identical slot types and relational roles,
identical answer position and target/foil token sets — only the entity lexicon
changes. **Precondition:** the benchmark must expose
$(\tau(x), \{(e_i, \sigma_i)\}_{i=1}^{s})$ per item. This holds by construction
for the 150 support items (built per-vocabulary from shared templates in
EXP065/066); for the N=60 test items it is a **benchmark-construction
requirement** — added to the EXP068 readiness checklist (§8). A test item whose
template/slot signature is unavailable is **excluded** from loop evaluation and
logged (Law #8); its views are never improvised.

[DEFINITION] **Consistency score:**
$$C_{\mathrm{cons}}(B; x) =
\frac{2}{m(m-1)} \sum_{1 \le j < \ell \le m}
\mathbf{1}\big[\hat{y}_j(B) = \hat{y}_\ell(B)\big] \in [0,1].$$

[DEFINITION] **Evaluator score:**
$$S_E(B; x) = \lambda_c \cdot C_{\mathrm{cons}}(B; x)
+ \lambda_m \cdot \tilde{M}(B; x), \qquad
\tilde{M}(B; x) = \mathrm{clip}\!\left(
\frac{\bar{M}(B; x) - \mu_M}{\sigma_M},\, 0,\, 1\right),$$
$\bar{M}$ the mean self-margin over views; $\mu_M, \sigma_M$ the baseline (unintervened)
margin mean/std on $\mathcal{D}_{\mathrm{sup}}$; $\lambda_c, \lambda_m \ge 0$,
$\lambda_c + \lambda_m = 1$, fixed on $\mathcal{D}_{\mathrm{tune}}$ (§1.1).

**Why this form** [INTERPRETATION]: $C_{\mathrm{cons}}$ rewards bases that induce the
*same* decision across vocabulary instantiations (the relational structure SCBI claims to
exploit); $\tilde{M}$ rewards bases that move the model decisively rather than noisily.
Neither term uses test labels. The eight self-consistency questions (Definitions §26)
are answered in §6 below.

**Budget:** $K \cdot m$ forward passes per iteration (plus $m$ unintervened baseline
passes once per instance, cached).

### 2.3 $\mathcal{S}$ — Selection and acceptance

[DEFINITION]
$$B_t^* = \arg\max_{B \in \mathcal{C}_t} S_E(B; x)
\quad \text{(ties broken by higher } C_{\mathrm{cons}}\text{, then lower index).}$$

[DEFINITION] **Acceptance rule** (Definitions §28):
$$A(B_t^*, B_t) = 1 \iff S_E(B_t^*) > S_E(B_t) + \delta,$$
$\delta \ge 0$ support-fixed improvement margin. If $A=0$, the candidate is **rejected**,
recorded in the run log (Law #8 — rejected candidates are never silently deleted), and
$B_{t+1} = B_t$.

[DEFINITION] **Representation update** (Definitions §30): replacement,
$B_{t+1} = B_t^*$ on acceptance. **State update** (Definitions §31):
$z_{t+1} = (t+1,\; \{S_E \text{ history}\})$; $z_{t+1} = z_t$ carries no learned parameters.

### 2.4 $\mathcal{T}$ — Termination

[DEFINITION] Stop at the smallest $t$ with any of:
- (i) $t = T_{\max}$ (support-fixed, default 5);
- (ii) two consecutive iterations with $A = 0$ (no accepted improvement);
- (iii) $\max_{B \in \mathcal{C}_t} S_E(B) < \tau_{\min}$ (no candidate clears the bar;
  support-fixed).

Final: $B^* = B_T$, $\hat{y} = f_\theta(x; B^*, z_T)$, temporary objects discarded
(Definitions §40–42).

### 2.5 Per-instance budget (pre-registered)

[DEFINITION] Primary compute metric (Definitions §48–49): forward passes per instance
$$F(x) \le m \cdot \big(1 + K \cdot (T(x)+1)\big), \qquad T(x) \le T_{\max},$$
i.e. worst case $5 \cdot (1 + 8 \cdot 6) = 245$ passes/instance at $K=8, m=5, T_{\max}=5$;
typical far lower under rule (ii). No backward passes anywhere in the loop.

---

## 3. $\Delta\theta = 0$ by construction

[PROPOSITION] No execution of the loop in §2 modifies $\theta$.

*Proof by construction.* Enumerate every mutation the loop performs:
1. $\mathcal{G}$: pure vector arithmetic on cached support activations → writes only
   Python-level candidate objects in $\mathcal{C}_t$.
2. $\mathcal{E}$: forward evaluations $f_\theta(x_j; B)$ with $\theta$ passed as a fixed
   argument; `torch.no_grad()` context; no `.backward()` call exists in the loop.
3. Intervention $h \leftarrow h + \alpha B$: a forward-hook **activation** edit;
   hook handles are removed after each instance (no persistent state).
4. $\mathcal{S}/\mathcal{T}$: selection among Python objects; updates write only to
   $(B_t, z_t)$, which are temporary by §1.
No optimizer is constructed; no parameter tensor has `requires_grad=True`; no assignment
targets any $\theta_\ell$. Hence $\theta_t = \theta_0\ \forall t$, i.e. $\Delta\theta \equiv 0$.
∎

[DEFINITION] **Runtime guard** (Law #6, #13): SHA-256 of `model.state_dict()` recorded
pre-loop and post-loop per instance; mismatch aborts the run as a protocol violation.
This mirrors the EXP065/066 guard.

**Precision on the PPLM comparison** [FACT]: PPLM *also* satisfies $\Delta\theta = 0$
(its gradients update hidden states $H_t$, not parameters). "We freeze $\theta$" is
therefore **not** a differentiator against PPLM and must never be presented as one.
The differentiators are stated in §4.

---

## 4. Differentiator analysis

### 4.1 vs PPLM (Dathathri et al., ICLR 2020)

| Axis | PPLM | SCBI loop (this spec) |
|---|---|---|
| Evaluator | **External**: separately trained attribute classifier (needs attribute labels) | **Internal**: frozen model itself, via $C_{\mathrm{cons}}$ over induced decisions (no external model, no attribute labels) |
| Search mechanics | Gradient ascent on hidden-state trajectories + KL-regularized re-forward (backward passes required) | **Gradient-free** generate–evaluate–select over candidates (forward passes only) |
| Search object | Full hidden-state trajectory $H_t$ | Compact basis/direction $B$ (+ temporary state $z_t$) |
| $\Delta\theta$ | $=0$ | $=0$ (shared; not a differentiator) |

[INTERPRETATION] The remaining distinction — internal self-consistency evaluator over
basis-valued objects — is exactly the audit's "unvalidated formulation distinction"
(§3.3). This spec makes it testable; it does not make it true.

### 4.2 vs Self-Refine (Madaan et al., NeurIPS 2023)

| Axis | Self-Refine | SCBI loop (this spec) |
|---|---|---|
| Search object | Text outputs $y$ | Representation bases $B$ |
| Evaluator form | Natural-language self-critique against a rubric | Decision-agreement score $C_{\mathrm{cons}}$ over perturbed views + self-margin |
| Loop structure | Refine a single trajectory | Explicit **selection over a candidate set** $\mathcal{C}_t$ with accept/reject |
| Documented limit | Gains plateau after 2–3 iterations; self-critique blind spots | Unknown — this is what EXP068 must measure |

### 4.3 The blind-spot falsifier-risk, addressed head-on

[FACT] (audit §2.24) Self-Refine's documented limitation — self-critique shares the
generator's blind spots, gains plateau — is the direct falsifier-risk for $\mathcal{E}$:
**an internal evaluator that cannot see its own errors cannot select better bases.**

Mitigations built into this spec (partial; honestly labeled):
- (a) **Evaluator/generator separation — representation-level only (corrected S5, 2026-09-23)**
  [DEFINITION]: $\mathcal{G}$ proposes in *direction space* (aggregates of support
  contrast vectors); $\mathcal{E}$ scores in *induced-decision space* (decisions the
  candidate induces across vocabulary-instantiated views). This is a
  **representation-level separation, not independence**: $\mathcal{G}_1$'s candidates
  are built from exactly the same five support vocabularies that define
  $\mathcal{E}$'s views — the data dependence is shared. What is separated is the
  *use* of that data (vector aggregation vs. decision agreement). If the five support
  vocabularies share a systematic bias, $\mathcal{G}$ and $\mathcal{E}$ inherit it
  jointly — which is precisely the blind-spot failure mode this mitigation was claimed
  to address. Honest statement: this mitigates *proposal-distribution* blindness (a
  direction $\mathcal{G}$ cannot propose is still scored against views $\mathcal{G}$
  did not condition on); it does **not** mitigate *shared-data* blindness. The latter
  is falsifier F4's territory, not this bullet's.
- (b) **Pre-registered validity gate** [DEFINITION]: on $\mathcal{D}_{\mathrm{gate}}$
  (labeled, disjoint from test *and* from $\mathcal{D}_{\mathrm{tune}}$ — see §1
  support split), measure
  $\rho = \mathrm{corr}\big(S_E(B),\, \mathbf{1}[\text{rescue}]\big)$ over candidate bases.
  If $\rho \le 0$, $\mathcal{E}$ is **invalid** and the loop may not proceed to test
  (this is falsifier F1 in §5). Because $\mathcal{D}_{\mathrm{gate}}$ was never used
  in tuning (§1.1), $\rho$ is a measurement of $\mathcal{E}$'s validity, not an echo
  of its tuning.
- (c) **Named residual risk** [CONJECTURE]: cross-vocabulary perturbation breaks the
  *systematicity* of the frozen model's errors often enough for $C_{\mathrm{cons}}$ to
  discriminate. If errors are systematic across all $m$ views (same wrong decision
  everywhere), then $C_{\mathrm{cons}}$ is maximized by bases that *preserve* the error,
  and no target-free $\mathcal{E}$ of this form can identify the right basis. EXP068
  must include the diagnostic: baseline decision-consistency across views on support
  errors. High baseline consistency + zero rescue ⇒ blind-spot failure confirmed (F4).
- (d) **The O5 tension, stated explicitly (fix S7, 2026-09-23)** [NOTE]: the program's
  O5 invalidated per-instance logit-margin shifts as *evidence of task-relevant causal
  effect* (the $B_{\mathrm{wrong}}$ control is significant at $p = 1.2\times10^{-8}$
  with $b = c = 0$). $S_E$ nevertheless contains the self-margin term $\tilde{M}$
  (§2.2). The distinction is narrow and load-bearing: $\tilde{M}$ is **not** used as a
  causal endpoint — no claim of the form "margins moved, therefore the basis works"
  appears in this spec. It is a *selection heuristic inside* $\mathcal{E}$ (prefer
  decisive over noisy moves), and its only license is the $\rho$-gate: if $\tilde{M}$
  does not contribute to correlation with actual rescues on $\mathcal{D}_{\mathrm{gate}}$,
  $\mathcal{E}$ fails F1 and the margin term goes down with it. A compromised
  $\rho$-gate plus a margin component is exactly how a confounded "valid" verdict gets
  manufactured — which is why the S3 split-support fix is a **prerequisite** for
  $\tilde{M}$'s inclusion, not optional hygiene.

---

## 5. Falsifiability (pre-stated kill criteria for $H_{\mathrm{loop}}$)

[HYPOTHESIS] $H_{\mathrm{loop}}$: *Per-instance $\mathcal{G}/\mathcal{E}/\mathcal{S}/\mathcal{T}$
selection over basis candidates, with $\Delta\theta=0$ and target-free $\mathcal{E}$,
yields $\Delta M > 0$ (McNemar $p<0.05$) on the headroom-calibrated benchmark **and**
beats compute-matched static-CAA and output-level self-consistency baselines.*

Any of the following **falsifies $H_{\mathrm{loop}}$ as specified** (Law #4 — no
post-hoc redefinition):
- **F1 — Invalid evaluator:** support-set $\rho \le 0$ (§4.3b). The loop cannot beat
  random selection; $\mathcal{E}$ as specified is uninformative.
- **F2 — Collapse to static:** $\cos(B^*(x), B_{\mathrm{agg}}) > 0.95$ on $>80\%$ of
  test instances. The loop merely re-discovers the static CAA direction; no per-instance
  adaptation is occurring.
- **F3 — No gain over known mechanism:** $\Delta M_{\mathrm{loop}} \le \Delta M_{\mathrm{static\text{-}CAA}}$
  (paired McNemar, $p \ge 0.05$ for the difference) at matched compute. The loop adds
  nothing beyond the N0 mechanism.
- **F4 — Blind-spot confirmation:** mean $C_{\mathrm{cons}}(B^*) \ge 0.8$ while
  $\Delta M_{\mathrm{loop}} \le 0$. High self-consistency, no accuracy gain — the
  Self-Refine failure mode reproduced at the representation level.
- **F5 — Dominated by output-level search:** compute-matched Best-of-N / self-consistency
  over outputs achieves $\Delta M$ significantly greater than the loop's. Representation-level
  search adds nothing over output-level search.

**Positive criterion** (all required): $\Delta M_{\mathrm{loop}} > 0$, McNemar $p < 0.05$;
beats static-CAA and output-level self-consistency at matched $F$; support-set $\rho > 0$
pre-registered and confirmed; F2/F4 diagnostics negative.

---

## 6. The eight self-consistency questions (Definitions §26), answered

1. **Entities compared:** induced decisions $\hat{y}_j(B)$ across $m$ vocabulary-instantiated
   views of the same relational query. 2. **Agreement:** pairwise decision-match rate
   $C_{\mathrm{cons}} \in [0,1]$. 3. **Why agreement→correctness:** [CONJECTURE] a basis
   capturing true relational structure routes all instantiations to the same answer; a
   scrambled basis scrambles decisions (cf. O2: scrambled basis ⇒ $\cos \approx 0$ ⇒ no
   coherent steering). Requires support-set calibration (§4.3b). 4. **Can wrong be
   consistent?** Yes — F4 names this; the $\tilde{M}$ term and $\rho$-gate are the
   defenses. 5. **Can correct be inconsistent?** Yes — if baseline decisions are split
   across vocabularies; such instances bound achievable $C_{\mathrm{cons}}$. 6. **Target
   independence:** $S_E$ uses only induced decisions and margins; no $y$. (Support-set
   calibration uses labels solely for hyperparameter validity, never at test time.)
   7. **Compute:** §2.5. 8. **Prior existence:** Wang et al. (2023) over outputs; ToT over
   thoughts; this spec's claimed distinction is the *basis-valued* search object with a
   *decision-agreement* objective — [CONJECTURE], untested.

---

## 7. Open questions (not disguised as definitions)

- **[OPEN] OQ1:** The $S_E = \lambda_c C_{\mathrm{cons}} + \lambda_m \tilde{M}$ form is a
  design choice. Whether cross-vocabulary decision agreement correlates with correctness
  is [CONJECTURE]; only the $\rho$-gate can promote it.
- **[OPEN] OQ2:** Whether single-direction $B$ ($k=1$) suffices, or the loop needs
  matrix-valued bases (Definitions §57 Variant). Silent promotion is forbidden (§89).
- **[OPEN] OQ3:** The blind-spot problem may be fundamental rather than incidental: if
  the frozen model's errors are systematic across all views, *any* target-free internal
  $\mathcal{E}$ is uninformative. A formal statement of this limit is future theory work.
- **[OPEN] OQ4:** $\mathcal{G}_1$ resamples the same 150 support contrast pairs; candidate
  diversity may be too low for genuine search. $D(\mathcal{C}_t)$ diagnostics in EXP068
  must report the effective candidate count.
- **[OPEN] OQ5:** Layer $l^*$ and strength $\alpha$ are fixed here; per-instance
  $(\alpha, l^*)$ selection would enlarge the search space and the budget.

---

## 8. EXP068 readiness checklist

A future EXP068 pre-registration may be written **only** when every box can be checked:

- ☐ Benchmark: N=60 Planetary/Elemental (or expanded) with 40–70% headroom verified
- ☐ Support/test split: $\mathcal{D}_{\mathrm{sup}}$ disjoint from test; all of
  $(K, m, T_{\max}, \lambda_c, \lambda_m, \tau_{\min}, \delta, \sigma, D_{\min}, \alpha)$
  frozen on $\mathcal{D}_{\mathrm{tune}}$ per §1.1 objectives (Law #9); full grid results archived
- ☐ Tuning record: §1.1 table executed; selected values frozen before $\mathcal{D}_{\mathrm{gate}}$ is touched
- ☐ $\rho$-gate: $\mathrm{corr}(S_E, \mathrm{rescue}) > 0$ measured on $\mathcal{D}_{\mathrm{gate}}$
  (never used in tuning) pre-registered as a go/no-go gate before test evaluation
- ☐ View-construction precondition: every test item exposes $(\tau(x), \{(e_i,\sigma_i)\})$;
  items without it are excluded and logged, never improvised (§2.2)
- ☐ Controls (7): unintervened baseline; static $B_{\mathrm{agg}}$ (CAA-equivalent);
  random-selection loop ablation ($\mathcal{G}/\mathcal{S}/\mathcal{T}$ with random
  $\mathcal{E}$ — isolates the evaluator's contribution); output bridge (positive
  control); compute-matched Best-of-N / self-consistency over outputs; $B_\perp$;
  $B_{\mathrm{wrong}}$
- ☐ Primary endpoint: $\Delta M > 0$, McNemar $p < 0.05$; secondary: F2/F4 diagnostics,
  $D(\mathcal{C}_t)$ trace, per-instance $F(x)$ accounting
- ☐ Falsifiers F1–F5 pre-registered verbatim; halt/branch decision tree as in EXP067 §7
- ☐ SHA-256 $\Delta\theta=0$ guard per instance (Law #13)
- ☐ **Vector archiving**: all $B_t^{(i)}$, $S_E$ scores, and $\hat{y}_j(B)$ stored per
  instance (Law #13 lesson from T-1 — scalar-only logs are insufficient)
- ☐ Compute budget: per-instance $F(x)$ formula (§2.5); wall-clock estimated on GPU
  hardware (CPU-only execution of the full loop is not recommended — see below)
- ☐ Compute estimate: worst-case $245$ fwd passes/instance × 60 instances
  $= 14{,}700$ passes (pythia-160m); at ~0.5 s/pass on GPU ≈ 2 h; expected far less
  under termination rule (ii). [CONJECTURE] pending hardware measurement —
  measure $F$ on 5 pilot instances before full launch

---

*End of draft. This spec constrains the experiment (Definitions §102); the experiment
may not redefine the spec.*
