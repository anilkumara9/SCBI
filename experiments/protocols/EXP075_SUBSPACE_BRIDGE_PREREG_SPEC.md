# EXP075 Protocol Specification: Subspace-Restricted Bridge — Is the Subspace Right and the Direction Wrong?

**Status:** PRE-REGISTERED (protocol; not yet executed)
**Date:** 2026-09-23
**Author role:** Preregistration Agent (from Innovation Sprint Idea 7, `research/innovation/SPRINT_2026-09-23.md`)
**Predecessor experiments:** EXP065/EXP066 (boundary series; the static null and the bridge rescue)
**Governing standards:** `AGENTS.md` (14 Inviolable Laws), `STATISTICAL_PROTOCOL_V02.md`,
`experiments/protocols/EXP067_QKOV_SUBSPACE_PROCRUSTES_SPEC.md` (structural template),
`reports/adversarial_audit_exp065_exp066.md` (boundary facts this builds on)
**Execution rule:** Strictly confirmatory. No mechanism, subspace-construction, or threshold changes
after the energy gate without a new pre-registration.

---

## 1. Research question and hypotheses

$$\boxed{\textbf{Does the per-vocabulary contrast subspace } S = \mathrm{span}\{\hat{v}_1..\hat{v}_5\}
\textbf{ contain a causally efficacious direction — i.e., was the EXP065/066 null a }
\textit{direction-choice}\textbf{ failure inside } S\textbf{, rather than a subspace failure?}}$$

**[HYPOTHESIS] H_sub:** Restricting the known-working output bridge to $S$ preserves its rescue
effect: with $P_S$ the orthogonal projector onto $S$ and $\mathrm{bridge}(x)$ item-specific,
injecting $u_S(x) = \mathrm{normalize}(P_S(\mathrm{bridge}(x)))$ at $\alpha = 0.50$ yields
$\Delta M > 0$ with McNemar exact $p < 0.05$ on the N=60 headroom-calibrated benchmark,
while the full bridge (positive control) replicates its historical rescue. If supported, the
licensed reading is the per-item existential: *for each rescued item, $S$ contains an
item-specific direction that yields the rescue* — not a single global direction in $S$.

**Null $H_0$:** $P_S(\mathrm{bridge})$ yields $\Delta M \equiv 0$ ($b = c = 0$) while the full
bridge rescues — $S$ is causally irrelevant as a search space (the sprint's kill criterion).

**[INTERPRETATION] The logical structure.** The program's boundary result is a conjunction:
(a) raw cross-vocabulary cosine $\approx$ +0.70 [OBSERVATION], (b) static $B_{\mathrm{agg}}$
injection $\Delta M = 0$ [OBSERVATION], (c) output bridge rescues +13.3pp / +16.7pp
[OBSERVATION]. Note that $B_{\mathrm{agg}} = \mathrm{normalize}(\sum_k \hat{v}_k) \in S$
**by construction** — so the historical null already says "the mean direction *in* $S$
does not transfer." H_sub asks the strictly narrower question: does $S$ contain *some
other* direction that does? A "yes" does not overturn the boundary result; it *localizes*
it: the failure was direction choice within $S$, which is exactly the search problem the
EXP068 $\mathcal{G}/\mathcal{E}/\mathcal{S}/\mathcal{T}$ loop is built to solve
(`theory/LOOP_SPEC_DRAFT.md` §2.1: $\mathcal{G}_1$ candidates are aggregates of the same
$\hat{v}_k$, living in or near $S$). A "no" says the loop would be searching an empty room.

### 1.1 Scope of this experiment (boundary science, not novelty science)

[INTERPRETATION] EXP075 is a **boundary-characterization and loop-motivation experiment**,
not a novelty experiment. A positive C4 result would be a better-localized instance of
known steering mechanics — closest priors ReFT/LoReFT (Wu et al. 2024; learned low-rank
subspace interventions) and DAS (Geiger et al. 2024; learned rotations against
intervention objectives), per the sprint's prior-art delta: ours is a *constructed*
contrast-derived subspace tested with zero training, and no verified record projects a
known-working intervention into such a subspace to test for a causal direction. Its
outcome **cannot move the novelty needle**: the N1 verdict (`reports/novelty_report.md`)
stands. What a positive result *can* do is motivate EXP068: the loop's per-instance
search-within-$S$ problem would be non-vacuous in the oracle sense — any existence proof
here uses the test item's own target/foil (the treasure was found *with a map*), so this
motivates search, it does not validate it. This is a strictly weaker claim than validating
the loop. §7 licenses this distinction branch by branch.

---

## 2. Frozen model and SHA-256 guard

- **Model / tokenizer:** `EleutherAI/pythia-410m` (identical to EXP066/EXP067).
- **Architecture [FACT]:** GPT-NeoX; 405,081,600 params; $d = 1024$; 24 layers; 16 attention
  heads; head dim 64; rotary embeddings; parallel attention/MLP; untied output embeddings.
- **Target layer:** $l^* = 20$ (83% depth, matching EXP066/EXP067).
- **Intervention strength:** $\alpha = 0.50$ (program continuity with EXP065/066).
- **Expected SHA-256** (pre and post, over all parameters): `4c242d9ac702a4029a674eacee84e0517cb6f79d794661dc3a3102bca5ed48dd`
  (registered value from EXP067 §2; sanity check only).
- **Guard procedure:** compute SHA-256 over the concatenation of `state_dict()` tensors
  (sorted keys, CPU, float32 bytes) *before* subspace construction and *after* Stage B.
  On mismatch: **abort immediately**, log, report no results. $\boxed{\Delta\theta \equiv 0}$
  is non-negotiable (Law #6). The **binding** guard is the runtime pre/post match in the
  execution environment (EXP067 §2, E-4).

---

## 3. Formal mechanism

### 3.1 The contrast subspace $S$ [DEFINITION]

For vocabulary $k \in \{1..5\}$ (Anglo, Biblical, Greek, Roman, Modern), let $\hat{v}_k
\in \mathbb{R}^{1024}$ be the per-vocabulary residual-stream contrast direction at
$l^* = 20$, constructed **exactly per the EXP066 support procedure**
(`experiments/scripts/run_exp066_pythia410m_replication.py`) from the $5 \times 30$
support contrast pairs. Define

$$S := \mathrm{span}\{\hat{v}_1, \dots, \hat{v}_5\} \subset \mathbb{R}^{1024}, \qquad
Q_S \in \mathbb{R}^{1024 \times 5} \text{ from deterministic thin-QR.}$$

**No-peeking discipline (mechanical, not asserted):** the construction reads *only*
support-set artifacts (support contrast pairs; no test items, no test labels, no test
outcomes at any stage). The separation is structural, not only procedural: support
entities are person names (Anglo: Alice/Bob/Charlie/David/Emma; Biblical: Aaron/Caleb/
Gideon/Miriam/Reuben; Greek: Hector/Jason/Nestor/Paris/Priam; Roman: Marcus/Lucius/Titus/
Felix/Silas; Modern: Liam/Noah/Sora/Maya/Leila) while test entities are planets
(Mars/Venus/Jupiter/Saturn/Mercury) and elements (Iron/Gold/Silver/Bronze/Steel) —
verified in `experiments/scripts/run_exp066_pythia410m_replication.py`. Concretely, the
construction script maintains a path whitelist containing only the support artifact
directories: any attempt to open a path outside the whitelist (in particular any
test-benchmark path) raises a runtime assertion and aborts the run before any vector is
constructed. $S$ is therefore fixed before the first test item is seen.

**Rank guard (pre-registered, halt on violation):** compute the SVD of the
$1024 \times 5$ stack; require numerical rank 5 with $\sigma_{\min}/\sigma_{\max} >
10^{-6}$. If violated, **HALT** — a degenerate (effectively lower-dimensional) $S$
would make the test uninformative, and silently proceeding would be p-hacking-adjacent.
The halt is reportable per §7.2.

### 3.2 The output bridge [DEFINITION]

Identical to EXP066 `make_bridge_vec`: for test item $x$ with target $t_{\mathrm{target}}$
and foil $t_{\mathrm{foil}}$,

$$\mathrm{bridge}(x) := \mathrm{normalize}\big(E[t_{\mathrm{target}}] - E[t_{\mathrm{foil}}]\big),
\qquad E = \text{model.embed\_out.weight},$$

an **unembedding-space** direction injected at $l^*$. [INTERPRETATION] (audit Finding 4):
this is near-direct answer-logit steering; its historical success (+13.3pp, 8/26,
$p = 0.0078$ on EXP066; +16.7pp, 10/19, $p = 0.0020$ on EXP065) is a "causal access
exists at this layer" control, not support for the representation-synthesis theory.
Its role here is purely as the *known-working intervention* whose restriction we test.

### 3.3 Projections and renormalization [DEFINITION]

$$u_S(x) := \mathrm{normalize}\big(P_S\,\mathrm{bridge}(x)\big), \qquad
u_{S^\perp}(x) := \mathrm{normalize}\big(P_{S^\perp}\,\mathrm{bridge}(x)\big),$$
$$P_S = Q_S Q_S^T, \quad P_{S^\perp} = I_{1024} - Q_S Q_S^T.$$

Renormalization is load-bearing: $u_S$ and $u_{S^\perp}$ are unit-norm, so at fixed
$\alpha$ any difference from the full bridge is about *direction*, not intervention
energy. (Injecting the unnormalized $P_S(\mathrm{bridge})$ would confound "wrong
direction" with "weaker push" — the EXP067-bundle F1 lesson applied to controls.)

### 3.4 Energy gate (pre-registered validity gate on the test itself)

$$e := \frac{\|P_S\,\mathrm{bridge}(x)\|}{\|\mathrm{bridge}(x)\|} \quad
\text{(median over the N=60 benchmark items).}$$

**Gate:** require $e \ge 0.10$. If $e < 0.10$, **HALT** — the test is *uninformative*,
not failed: a null under a near-zero projection cannot distinguish "$S$ is causally
irrelevant" from "the intervention was too weak to test $S$." Per the sprint sketch,
this outcome mandates re-design, not a kill verdict. Report $e$ and the full
per-item energy distribution.

[ARBITRARY — sensitivity analysis required]: the 0.10 value keeps its [ARBITRARY] tag,
but is anchored at chance level: for a random unit vector in $\mathbb{R}^{1024}$,
$\mathbb{E}[\|P_S u\|^2] = 5/1024 \approx 0.0049$, i.e. $\mathbb{E}[e] \approx 0.07$.
The gate therefore demands that $S$ capture *more of the bridge than chance*; the 0.10
bar encodes "below ~10% retained energy, a null is uninterpretable." Report the ruling's
sensitivity at 0.05 and 0.15 alongside.

[INTERPRETATION] Mechanism disclaimer: the energy gate guards **null-interpretability
only** — it does not, and structurally cannot, screen the mechanism confound. The bridge
is unit-norm, but $u_S$ is **renormalized** to unit norm and injected at $\alpha = 0.50$:
at the gate floor $e = 0.10$, the retained 10% is injected at 10× its natural scale in
the bridge. Per audit Finding 4 (`reports/adversarial_audit_exp065_exp066.md`), the
bridge is near-direct answer-logit steering (KL 0.028 vs ~0.0002 for basis conditions —
only the bridge meaningfully moves the output distribution). If the retained residue
carries logit-steering power, a C4 rescue can fire **for the wrong reason** — via amplified
logit-steering, not via anything the loop's relational search would recognize. Branch (e)'s
license is weakened accordingly (§7.1): mechanism (relational vs. logit-steering) is
unidentified by this experiment.

### 3.5 Interventions

For test instance $x$ (last-token position, forward hook at $l^*$, hook removed after):

- **C4 (subspace-restricted bridge — the test):** $h \leftarrow h + \alpha\, u_S(x)$
- **C5 (complement-restricted bridge — the discriminant):** $h \leftarrow h + \alpha\, u_{S^\perp}(x)$
- **C3 (full bridge — positive control):** $h \leftarrow h + \alpha\, \mathrm{bridge}(x)$ (EXP066-identical)
- **C2 (static basis):** $h \leftarrow h + \alpha\, B_{\mathrm{agg}}$ (EXP066-identical)

---

## 4. The 7 conditions

| # | Condition | Intervention |
|---|---|---|
| C1 | Unintervened baseline | none |
| C2 | Static basis $B_{\mathrm{agg}}$ | §3.5 (EXP066-identical; expected null per boundary result) |
| C3 | **Full output bridge (positive control)** | §3.5 — must replicate historical rescue (§7.1c) |
| C4 | **Subspace-restricted bridge (EXP075 test)** | §3.5 — primary test condition |
| C5 | Complement-restricted bridge (discriminant) | §3.5 |
| C6 | $B_\perp$ | C2 pipeline with $B_{\mathrm{agg}}^\perp$ (seed 9876, inherited) |
| C7 | $B_{\mathrm{wrong}}$ | wrong-task basis (Paris-capital contrast, as EXP066) |

## 5. Benchmark and headroom

- **Benchmark:** the identical N=60 Planetary/Elemental 2-hop/3-hop suite from EXP065/066
  (same items, same premise permutations). No new benchmark construction (Law #9).
- **Headroom gate:** run C1 first; require baseline accuracy $\in [40\%, 70\%]$.
  If outside: **HALT**, do not proceed; any recalibration requires a new pre-registration.
  A headroom halt is reportable per §7.2, not a trigger for adjustment under EXP075.

## 6. Endpoints

- **Primary (confirmatory):** $\Delta M$ (percentage points) on paired decisions, each
  condition vs C1; McNemar exact test on $(b, c)$. **Success for a condition:**
  $\Delta M > 0$ **and** $p < 0.05$ (two-sided exact).
- **Secondary (exploratory):** rescues $b$, corruptions $c$; $\mathrm{KL}_{\mathrm{div}} < 0.50$
  guardrail (EXP067 precedent); energy ratio $e$ and its distribution; $\|P_S(\mathrm{bridge})\|$
  per item; rank diagnostics of $S$.
- **Margin shifts:** recorded but **exploratory only** — the O5/Wilcoxon lesson stands
  (audit Finding 3): the $B_{\mathrm{wrong}}$ control invalidates margin-shift significance
  as a causal endpoint ($p = 1.2\times10^{-8}$ with $b = c = 0$). Never confirmatory.

---

## 7. Falsification criterion and pre-registered decision tree

### 7.0 Canonical criterion (single source of truth)

$$\boxed{\begin{aligned}
&\textbf{If C4 yields } \Delta M > 0 \textbf{ (McNemar } p < 0.05\textbf{) with C3 valid and the energy gate passed,}\\
&\textbf{then H\_sub is SUPPORTED: for each rescued item, } S \textbf{ contains an item-specific}\\
&\textbf{direction } (u_S(x))\textbf{ that yields the rescue — not a single global direction in } S\text{.}\\
&\textbf{If C4 yields } \Delta M \equiv 0 \; (b = c = 0) \textbf{ while C3 yields } \Delta M > 0 \; (p < 0.05)\textbf{,}\\
&\textbf{then H\_sub is FALSIFIED: } S \textbf{ is causally irrelevant as a search space.}
\end{aligned}}$$

### 7.1 Full decision tree (pre-registered; every branch has a ruling; precedence (a)→(b)→(c)→(d)→(e)→(f)→(g), with (h)/(i) conditional on (f)/(g))

| # | Branch | Pre-registered ruling |
|---|---|---|
| (a) | **Energy gate fails** ($e < 0.10$) | **HALT — uninformative causal test, informative localization measurement.** The low $e$ *is* the localization evidence: the bridge's causal power lies almost entirely outside $S$. What is uninformative is specifically C4's causal test (a renormalized-noise injection cannot support a direction verdict). Report the $e$ distribution as evidentially non-empty. Re-design required (not a re-run under EXP075). |
| (b) | **Headroom gate fails** (baseline outside [40%, 70%]) | **HALT — benchmark miscalibrated.** Reportable; no conclusions. |
| (c) | **C3 positive control fails** ($\Delta M \le 0$ or $p \ge 0.05$) | **Invalid run.** The load-bearing control did not replicate; **no conclusion about H_sub may be drawn.** Diagnose (model hash, benchmark integrity, hook lifecycle) before any re-registration. Do not interpret C4/C5 in an invalid run. |
| (d) | **C2 rescues** ($\Delta M > 0$, $p < 0.05$) | **Boundary revision — supersedes (e)–(i).** The EXP065/066 static null failed to replicate. Report as a revision of the program's central boundary claim with full statistics, **including the historical EXP065/066 baseline accuracy alongside this run's baseline accuracy.** Comparability rider: the headroom band [40%,70%] is wide enough to admit incomparable runs — if the baselines differ substantially, the "boundary revision" reading is qualified accordingly (the numbers, not the adjective, carry the claim). The "direction within $S$" interpretation is moot if the mean direction in $S$ works. |
| (e) | **C4: $\Delta M > 0$, $p < 0.05$** (C3 valid) | **H_sub SUPPORTED — strongest loop motivation.** LICENSES: "for rescued items, $S$ contains an item-specific direction, constructible with label information, that rescues at the decision endpoint; the EXP068 loop's per-instance search-within-$S$ problem is non-vacuous in this oracle sense (EXP068's $\mathcal{G}_1$ candidates are aggregates of the same $\hat{v}_k$, hence elements of $S$ by construction). Mechanism (relational vs. logit-steering) unidentified — the energy gate guards null-interpretability only (§3.4). Label-free findability not established: contingent on EXP070's ceiling verdict and EXP068's own ρ-gate." DOES NOT LICENSE: loop validation (no search was performed); that a label-free search can find such directions (EXP068's own question; contingent on EXP070's ceiling verdict and EXP068's ρ-gate); a single global rescuing direction in $S$; novelty claims (N1 holds — §1.1); the identity of the best direction in $S$; any claim about other subspaces. |
| (f) | **C4: $b = c = 0$** ($\Delta M \equiv 0$), C3 valid | **H_sub FALSIFIED (kill).** LICENSES: "$S$, as constructed, is causally irrelevant as a search space; the EXP068 loop would be searching an empty room *in this operationalization*." DOES NOT LICENSE: "no subspace works" (only this $S$ tested); "the loop is dead in all forms" (a loop searching a different candidate family is a new pre-registration); any claim about $S$'s geometric (non-causal) properties. |
| (g) | **C4 partial** ($b > 0$ but $p \ge 0.05$; or $\Delta M < 0$) | **Mixed — neither support nor kill.** Report exact $(b, c, p, \Delta M)$. No motivation claim, no kill claim. |
| (h) | **C5 rescues** ($\Delta M > 0$, $p < 0.05$) **while C4 is (f)/(g)** | **Discriminant: wrong room.** The causal direction lives in $S^\perp$, not $S$. Strengthens (f)'s interpretation; if attached to (g), upgrades it toward (f). LICENSES: "the bridge's causal power is not in the contrast subspace." |
| (i) | **C4 and C5 both null, C3 valid** | **Non-localizable.** The bridge's causal power requires components in *both* $S$ and $S^\perp$ jointly (or neither separately at unit-norm). Report as a localization limit; neither (e) nor (f) fires. |

**Multiplicity disclosure:** branches (e), (f), and (h) each involve a McNemar test; no
family-wise error correction is applied. The operative multiplicity control is the
pre-registered precedence order (a)→(b)→(c)→(d)→(e)→(f)→(g), with (h)/(i) conditional —
the licensed claims are motivation-grade, not confirmatory-efficacy, claims.

### 7.2 Halt gates are reportable outcomes

EXP075 has three halt gates: the rank guard (§3.1), the energy gate (§3.4), and the
headroom gate (§5). **Any halt IS the published outcome** — a halted EXP075 is a result
(degenerate subspace / uninformative test / miscalibrated benchmark), not a non-result.
**Explicitly forbidden:** re-running with adjusted subspace construction, energy-bar,
or headroom handling under the EXP075 label. Any adjusted design takes the **next free
number at pre-registration time** (EXP070 minor-m1 precedent); see §9 for reservations.

## 8. Reproducibility and hygiene

- **Seeds (pre-registered):** `torch.manual_seed(20260923)`, NumPy `20260923`;
  $B_\perp$ seed 9876 (inherited). Thin-QR is deterministic (no seed needed).
- **Law #13 archiving:** $Q_S$ (1024×5), the five $\hat{v}_k$, $P_S(\mathrm{bridge})$ and
  $P_{S^\perp}(\mathrm{bridge})$ per item (unit-norm and pre-norm), energy ratios,
  rank diagnostics, and full per-instance records (prompt id, per-condition correct,
  KL) — the T-1 lesson: scalar summaries alone are insufficient for future analyses.
- **Hook isolation:** register forward hook per instance, remove after; assert handle
  lifecycle in logs; no inter-instance state.
- **Determinism:** `torch.use_deterministic_algorithms(True)` where supported; record
  environment manifest.
- **Budget:** 7 conditions × 60 items = **420 forward passes** (pythia-410m) ≈ **< 30 min
  on a Kaggle T4** (sprint estimate); subspace construction and projections are vector
  arithmetic (negligible). Fits comfortably in free-tier quota.

## 9. What EXP075 does NOT test, and numbering hygiene

- Which direction in $S$ is best (no search is performed — that is EXP068's job, contingent
  on its own pre-registration and on EXP070's ceiling verdict).
- Whether other subspaces (per-head OV subspaces, MLP-derived, learned) contain causal
  directions.
- The origin of the raw ~0.7 cosine (Q2 of the formalization doc; separate study).
- Any claim beyond pythia-410m / layer 20 / this benchmark family.
- **Finding-4 caveat [INTERPRETATION]:** the bridge is near-direct logit steering, not a
  relational direction. A C4 rescue therefore shows $S$ contains a direction with
  *causal efficacy at the decision endpoint* — which is exactly what H_sub claims and all
  any branch licenses. It does not by itself show the rescuing direction operates via
  relational (rather than logit-steering) mechanism. The loop-motivation reading of (e)
  is about the *search space containing a rescuing direction*, not about mechanism
  identity. This is the branch the adversarial reviewer should attack first.
- **Numbering:** changed designs take the next free number at pre-registration time.
  Reserved: EXP069 (sprint Idea 1, compositional factorization), EXP071 (sprint Idea 3,
  steerability diagnostic), EXP072/073/074 (sprint Ideas 4/5/6), EXP076 (sprint wildest
  credible: cross-model causal transfer). EXP070's changed-design rule likewise uses
  next-free-numbering (LOG-077, minor m1).

---

**Pre-registration checklist:** ☐ $S$ construction fixed (support-only, rank guard armed)
☐ energy gate armed ($e \ge 0.10$, sensitivity bands 5%/15%) ☐ $K$ n/a, $\alpha=0.50$ fixed
☐ seeds fixed ☐ headroom gate armed ☐ SHA-256 guard armed ☐ falsification criterion
recorded ☐ full decision tree recorded (§7.1, precedence stated) ☐ LICENSES /
DOES-NOT-LICENSE on every branch ☐ §1.1 boundary-science scope acknowledged
☐ numbering reservations recorded.
*No results exist under this protocol. Any deviation is a protocol violation, not a discovery.*
