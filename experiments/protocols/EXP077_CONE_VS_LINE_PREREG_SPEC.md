# EXP077 Protocol Specification: Cone-vs-Line Geometry — Is the Relational Concept Conical?

**PRE-REGISTERED (protocol; not yet executed) — SIGNED 2026-09-23**

**Status:** PRE-REGISTERED (protocol; not executed; adversarial review 2026-09-23 verdict
SIGN-WITH-FIXES — all 10 fixes applied 2026-09-23; re-verification 2026-09-23 verdict **SIGN**)
**Date:** 2026-09-23
**Author role:** Theory Agent
**Predecessor experiments:** EXP065/066 (boundary series — the null under test), EXP067 (QK/OV subspace, pre-registered, unexecuted), EXP070 (oracle ceiling, pre-registered, unexecuted), EXP075 (subspace bridge, pre-registered, unexecuted)
**Source idea:** `research/innovation/SPRINT_2026-09-23.md` New Idea 6 (sweep-driven proposals — ACCEPTED clean, no fixes required; flagged "preregister early, cheapest mechanism test")
**Governing standards:** `AGENTS.md` (14 Inviolable Laws), `STATISTICAL_PROTOCOL_V02.md`,
`theory/BOUNDARY_CLAIM_FORMALIZATION.md` (the I1 null under test), `research/literature/audit_2026-09-23.md`
(N1 verdict), `research/MATH_STANDARDS_CHARTER.md` (binding M1–M8)
**Sweep provenance (carried, not laundered):** refusal-as-cone evidence is 2026 practitioner
literature (algoverse-bias-steering project analysis, Aug 2026 — **LOW-confidence secondary
source**); QCRI "~11 refusal flavors" / ACE affine decomposition are **practitioner-doc claims
only, not verified against primary papers**; Anthropic circuit tracing (Mar 2025, `index`) is
consistent with subspace views. All three are hypotheses, not established results.
**Execution rule:** Strictly confirmatory. No direction, radius, α grid, seed, gate, or threshold
changes after execution begins without a new pre-registration. **Changed design = the next free
number at pre-registration time.**
(Numbering note: EXP076 is taken by the sprint's cross-model-transfer idea; this protocol takes
EXP077, the next free number at pre-registration time.)

---

## 1. Research question and hypotheses

$$\boxed{\textbf{Is the relational concept in the two-hop task \textit{conical} (a cone of
directions rescues) rather than a single \textit{line} (one direction rescues)?}}$$

**[HYPOTHESIS] H_cone:** The rescuing region is a cone around the concept direction: directions
within angular radius $\rho$ of the candidate direction rescue instances the single direction
misses (angular evidence), and/or rescue is a non-monotonic (peaked/threshold) function of
injection scale $\alpha$ (radial evidence), and/or removing the shared affine offset rescues
(affine evidence).

**[HYPOTHESIS] H_line:** The concept is line-narrow: the single direction $\hat{v}$ is the
rescuing object; angular deviations strictly lose rescues and rescue scales monotonically with
$\alpha$.

**Null $H_0$ (the standing boundary null I1):** raw cross-vocabulary cosine $\approx 0.7$ with
strictly zero causal transfer under static injection — and no geometric variation tested here
(radial scale, angular spread at $\rho = 30^\circ$, affine offset) changes that.

### 1.1 Scope of this experiment (mechanism test, not a method)

[INTERPRETATION] EXP077 is a **geometry-shape diagnostic** on the program's own headline null.
It does not propose conical steering as a method. Its logic is two-way falsification (the
reviewer's phrase): flat-zero across every geometric variation **kills** the cone/affine
hypothesis and strengthens the linear boundary verdict; a peaked $\alpha$-curve or angular
cone-wins **withdraws the blanket null** and replaces it with a geometry-conditional claim.
Either way the experiment pays — it is the cheapest mechanism test in the sprint
($\le 1{,}740$ forward passes, §9).

### 1.2 Logical structure: what each outcome licenses and does NOT license

| Outcome | LICENSES | DOES NOT LICENSE |
|---|---|---|
| **(a) CONE-WINS** (§8): angular McNemar $p<0.05$, $b>c$, cone beats control ($p_2<0.05$) — or non-monotonic $\alpha$-response — or offset-removal rescues | "The rescuing region extends beyond the single line — angularly (concept-specifically), radially, or affinely. The blanket boundary null I1 is **withdrawn in its blanket form**, replaced by a geometry-conditional claim: zero transfer under single-direction static injection at the tested scales does not imply zero transfer under geometrically richer injection." The firing sub-evidence (angular / radial / affine) is named in the ruling. | "The adaptive loop will work"; any novelty-tier movement (N1 stands); anything about conditional (gated) steering — the CAST-style gated variant is explicitly untested here (P5 territory, §11); other models, layers, radii, or $\alpha$ grids. |
| **(b) LINE-WINS** (§8): angular McNemar $p<0.05$, $c>b$ — or monotone-non-decreasing $\alpha$-response with significant rescue | "The concept is line-narrow at the tested geometry: angular deviation strictly loses rescues and/or rescue is monotone-non-decreasing with $\alpha$ over the tested grid. (A singleton upper set is consistent with, not proof of, monotonic scaling.) The cone/affine hypothesis is **rejected for this task**; I1 stands strengthened. If fired via the angular trigger, the $\alpha=1.0$ scale rescued where $\alpha=0.5$ did not — the boundary null's $\alpha$-scope is narrowed and must be re-characterized." | "No cone exists at other radii" — exactly one radius ($\rho=30^\circ$) was tested (A-cone-radius, §7); cross-model or cross-layer claims. |
| **(c) NEITHER** (§8): flat-zero across the $\alpha$ grid (Holm-adjusted), offset null, angular null | **Kill (unconditional geometry only).** "Radial scale, angular spread at $\rho=30^\circ$ (A-cone-radius), and affine offset at $\alpha=1.0$ jointly cannot explain the null. The $\rho=30^\circ$ unconditional cone hypothesis and the $\alpha=1.0$ offset hypothesis **die for this task** — cones at other angular radii are untested and survive this kill. The conditional (gated) variant is untested (§11) and is not killed by (c). The linear boundary verdict (I1) stands strengthened — the zero-transfer result survives best-practice unconditional geometric variation." | Conditionality claims (gated variant untested — named residual, §11); other radii; "geometry is irrelevant in general" (family-, model-, benchmark-restricted). |
| **(r) REPLICATION FAILURE** (§8): C3 vs C1 significant (two-sided $p<0.05$, $\Delta M \ne 0$ either direction) | "I1 failed to replicate on pythia-410m/layer-20 at $\alpha=0.5$ in this run — no geometry branch fires; the geometry question is moot when the null itself did not replicate. Re-scope under a new pre-registration." Report $\Delta M$, $(b,c)$, $p$, and this run's baseline accuracy alongside the historical EXP065/066 baselines (comparability rider per EXP075 branch (d)). | Anything about $H_{\mathrm{cone}}$/$H_{\mathrm{line}}$; any geometry claim. |
| **(d) INVALID** (§8): headroom/bridge gates fail or anti-cheat violation | "The measurement preconditions failed; **no conclusion about geometry may be drawn**." | Anything about $H_{\mathrm{cone}}$ / $H_{\mathrm{line}}$. |

---

## 2. Frozen model and SHA-256 guard

- **Model / tokenizer (in-scope):** `EleutherAI/pythia-410m` (identical to EXP066; the model on
  which the boundary null's 410m leg was established).
- **Architecture [FACT]:** GPT-NeoX; $d = 1024$; 24 layers. (Boundary formalization §2.)
- **Target layer:** $l^* = 20$ (83% depth, matching EXP066/067). Intervention
  $h \leftarrow h + \alpha u$ via forward hook at $l^*$, last-token position.
- **Intervention strengths:** $\alpha \in \{0.25, 0.5, 1.0, 2.0\}$ [ARBITRARY grid,
  pre-registered per the proposal; Law #9 — the response *curve* is the endpoint, so a single
  significant $\alpha$ is not cherry-picking]. Cone/control arms use $\alpha = 1.0$ fixed
  [ARBITRARY — one doubling above the null's $\alpha=0.5$, giving the line arm headroom while
  staying in the tested regime; pinned].
- **Expected SHA-256** (pre and post, over all parameters):
  `4c242d9ac702a4029a674eacee84e0517cb6f79d794661dc3a3102bca5ed48dd`
  (carried from EXP067 §2 — same model `EleutherAI/pythia-410m`; sanity check only).
  **Guard procedure:** SHA-256 over `state_dict()` tensors
  (sorted keys, CPU, float32 bytes) pre/post run; binding guard is the runtime pre/post match.
  $\boxed{\Delta\theta \equiv 0}$ non-negotiable (Law #6). No backward pass exists anywhere.

---

## 3. Formal mechanism

**Notation context (M1.1):** In *this* document, $h(x) \in \mathbb{R}^{1024}$ is the residual-stream
hidden state at layer $l^*=20$, last-token position, for item $x$; $\hat{v}, u_j, r \in
\mathbb{R}^{1024}$ are unit-norm intervention directions; $\alpha$ is the injection scale;
$\rho$ is the cone angular radius. "Rescue" always means the per-instance decision-change
indicator of §3.6 (M7.2 — never the metaphor).

### 3.1 Candidate direction $\hat{v}$ [DEFINITION]

$\hat{v} := B_{\mathrm{agg}}$, the aggregated contrast basis of the boundary series, reconstructed
from the archived support set (30 contrast pairs per vocabulary × 5 vocabularies — Anglo,
Biblical, Greek, Roman, Modern; 150 rel + 150 neu presentations), exactly per
`theory/BOUNDARY_CLAIM_FORMALIZATION.md` §2:

$$\hat{v}_k = \operatorname{normalize}\!\left(\frac{1}{30}\sum_{i=1}^{30}
\frac{\Delta h_i^{(k)}}{\|\Delta h_i^{(k)}\|}\right), \qquad
\hat{v} = \operatorname{normalize}\!\left(\sum_{k=1}^{5} \hat{v}_k\right).$$

[M4.1 shape check:] $\Delta h_i^{(k)}, \hat{v}_k, \hat{v} \in \mathbb{R}^{1024}$; all unit norm.
[M4.2 space check:] fit space = residual stream at $l^*=20$ (contrast differences of residual
states); application space = residual stream at $l^*=20$. **Same space — no transfer
assumption needed.** [M4.4:] every intervention direction below is unit-norm at injection;
$\alpha$ carries all scale.

### 3.2 Offset-removed direction $\hat{v}^{c}$ [DEFINITION]

Jorgensen-style global centring (old Idea 5 / EXP073 candidate — run jointly here, cited, no
duplicate experiment):

$$\mu = \frac{1}{300}\sum_{x \in \mathrm{support}} h(x), \qquad
\hat{v}^{c}_k = \operatorname{normalize}(\hat{v}_k - \mu), \qquad
\hat{v}^{c} = \operatorname{normalize}\!\left(\sum_{k=1}^{5} \hat{v}^{c}_k\right),$$

$\mu$ over all 300 support presentations (150 rel + 150 neu), layer 20, last token.
[M4.4:] subtraction then **renormalization to unit norm** before injecting at $\alpha = 1.0$ —
the amplification factor of renormalizing an offset-removed vector is logged, not hidden.
Per-vocabulary centring is **not** tested here (EXP073's territory — named residual, §11).

### 3.3 Cone sampling [DEFINITION]

Cone angular radius $\rho = 30^\circ$ [ARBITRARY — pinned; single radius per A-cone-radius,
§7]. $K = 8$ [ARBITRARY — pinned] cone directions:

$$u_j = \operatorname{normalize}\!\left(\hat{v}\cos\phi_j + w_j\sin\phi_j\right),
\qquad \phi_j = \rho\,\frac{j+1}{8}\;\; (j = 0..7),$$

i.e. $\phi_j \in \{3.75^\circ, 7.5^\circ, \dots, 30^\circ\}$ — evenly spaced radii from
near-axis to rim, sampling the cone interior-to-boundary. Each $w_j$ is a unit vector
orthogonal to $\hat{v}$ ($w_j \perp \hat{v}$, $\|w_j\|=1$), obtained by Gram–Schmidt
orthonormalization of a Gaussian draw with **pinned seed 7701** (Law #13).
[EXACT:] $\cos(u_j, \hat{v}) = \cos\phi_j$ by construction; $\min_j \phi_j = 3.75^\circ > 0$
so no cone direction coincides with $\hat{v}$ (M5.1 degenerate case excluded by construction).
Injection: $h \leftarrow h + 1.0 \cdot u_j$ at $l^*$, last token.

### 3.4 Control cone [DEFINITION]

$r \in \mathbb{R}^{1024}$: a unit vector drawn uniform on the sphere, **pinned seed 7702**,
independent of $\hat{v}$ (assert $\lvert\cos(r,\hat{v})\rvert < 0.5$ at build — a near-parallel
random draw would make the control a second cone arm). Control directions $q_j$ built by the
identical §3.3 construction with $r$ in place of $\hat{v}$ (same $\rho$, same $K$, seed 7702
for the orthogonal axes). Purpose: isolate the *attempts* confound — the cone arm gets 8
tries per item; the control gets 8 tries around a meaningless axis. [INTERPRETATION:] if the
$\hat{v}$-cone beats the line but not the control, the wins are attempts-alone, not geometry.
[DETERMINISM:] the $\lvert\cos(r,\hat{v})\rvert < 0.5$ build assert is a deterministic
function of pinned seed 7702 and the archived support data — no other randomness exists in
the construction path. It is verified at bundle construction (CPU, pre-runtime), never
discovered at execution time (reviewer's note, 2026-09-23).

### 3.5 Intervention

All conditions inject at $l^*=20$, last-token position, via forward hook; hook registered per
instance and removed after (no inter-instance state). Injection-vector norms asserted $> 0$ at
build time and persisted (F1 lesson — a silent-zero control must be impossible, not absent).

### 3.6 Per-instance rescue criteria [DEFINITION]

For item $x$, with C1 the unintervened baseline:

- $L(x) = \mathbf{1}[\text{C4 correct on } x \;\wedge\; \text{C1 incorrect on } x]$ — **line rescue**
  ($\hat{v}$ at $\alpha=1.0$).
- $K(x) = \mathbf{1}[(\exists j: u_j \text{ correct on } x) \;\wedge\; \text{C1 incorrect on } x]$
  — **cone rescue** (existential over the $K=8$ cone directions).
- $R(x) = \mathbf{1}[(\exists j: q_j \text{ correct on } x) \;\wedge\; \text{C1 incorrect on } x]$
  — **control rescue**.
- $A_\alpha(x) = \mathbf{1}[\text{C}(\alpha) \text{ correct on } x \;\wedge\; \text{C1 incorrect on } x]$
  for $\alpha \in \{0.25, 0.5, 1.0, 2.0\}$ — radial rescue indicators.
- $O(x) = \mathbf{1}[\text{C6 correct on } x \;\wedge\; \text{C1 incorrect on } x]$ — offset rescue.

Discordant counts: angular $(b, c) = (\sum_x K(x)(1-L(x)),\; \sum_x L(x)(1-K(x)))$;
control $(b_2, c_2) = (\sum_x K(x)(1-R(x)),\; \sum_x R(x)(1-K(x)))$.
[M5.1:] $b=c=0 \Rightarrow$ exact McNemar $p = 1.0$ (null — no branch fires on it).

### 3.7 Anti-cheat clause [DEFINITION]

1. Support items used for $\hat{v}$, $\mu$, and cone-axis construction are disjoint from
   benchmark items (id-disjointness asserted at runtime; violation = protocol violation).
2. No test label enters any construction — all directions are built from support data only.
3. **Any leakage** = invalid run per Law #8, never silently corrected under EXP077.

---

## 4. Conditions (10)

| # | Condition | Intervention |
|---|---|---|
| C1 | Unintervened baseline | none |
| C2 | $\hat{v}$ at $\alpha=0.25$ | $h \leftarrow h + 0.25\,\hat{v}$ |
| C3 | $\hat{v}$ at $\alpha=0.50$ (boundary-null replication) | $h \leftarrow h + 0.50\,\hat{v}$ |
| C4 | $\hat{v}$ at $\alpha=1.00$ (**line arm** of the angular test) | $h \leftarrow h + 1.00\,\hat{v}$ |
| C5 | $\hat{v}$ at $\alpha=2.00$ | $h \leftarrow h + 2.00\,\hat{v}$ |
| C6 | Offset-removed $\hat{v}^{c}$ at $\alpha=1.0$ (joint with old Idea 5) | $h \leftarrow h + 1.00\,\hat{v}^{c}$ |
| C7 | $B_{\mathrm{wrong}}$ at $\alpha=1.0$ (wrong-task negative control, EXP066) | specificity diagnostic — reported, never a branch trigger |
| C8 | Same-layer output bridge (positive control, EXP066 `make_bridge_vec`) | validity gate (§5) |
| C9 | **Cone arm:** best-of-$K$ ($K=8$) directions within $\rho=30^\circ$ of $\hat{v}$, $\alpha=1.0$ | per-item existential over $u_j$ (§3.3) |
| C10 | **Control arm:** best-of-$K$ ($K=8$) directions within $\rho=30^\circ$ of pinned random $r$, $\alpha=1.0$ | per-item existential over $q_j$ (§3.4) |

---

## 5. Benchmark, gates, and readiness

- **Benchmark:** the identical N=60 Planetary/Elemental 2-hop/3-hop suite from EXP065 (same
  items, same premise permutations). No new benchmark construction (Law #9).
- **Headroom gate:** run C1; require baseline accuracy $\in [40\%, 70\%]$ (program continuity,
  EXP067 §5). If outside: **HALT** → branch (d). Any recalibration = new pre-registration.
- **Bridge-validity gate:** C8 must show $\Delta M > 0$ with McNemar $p < 0.05$ (EXP066:
  $+13.33$pp, $p=0.0078$ on this model). If not: **INVALID** → branch (d) — setup broken or
  benchmark drifted; do not interpret C2–C7/C9/C10.
- **Continuity assertion (readiness):** the rebuilt per-vocabulary directions must reproduce
  the O1 phenomenon: mean $\cos(\hat{v}_1, \hat{v}_k) \ge 0.50$ [ARBITRARY continuity floor —
  well below the observed $\approx 0.69$, catching only gross reconstruction failure]. If the
  support archive is unloadable or the floor fails: **INVALID** → branch (d) with the reason
  named (we are not testing the direction the null was established on).
- **Analysis set:** all N=60 items with rescue-indicator coding (§3.6); items correct at
  baseline contribute $(0,0)$ pairs and do not affect $(b,c)$ or $p$.

---

## 6. Endpoints

- **Primary (confirmatory):** angular cone-vs-line — McNemar exact two-sided on $(b, c)$;
  conjunct: cone-vs-control McNemar exact two-sided on $(b_2, c_2)$.
- **Secondary (pre-registered):** the $\alpha$-response curve — McNemar exact two-sided per
  $\alpha$ vs C1; the curve shape (empty / upper-set / non-upper, §8) is the endpoint.
  Offset arm C6 vs C1 (McNemar exact two-sided). C7 specificity diagnostic (reported).
  C3 vs C1 as the boundary-null replication check ($\Delta M = 0$, $b=c=0$ expected) — a
significant deviation in either direction fires branch (r), never a geometry branch (§8).
- **Margin shifts:** recorded but **exploratory only** — O5 stands: the C7 control invalidates
  margin-shift significance as a causal endpoint.
- **Sensitivity (reported alongside any ruling):** the ruling's dependence on the
  [ARBITRARY] choices ($\rho=30^\circ$, $K=8$, $\alpha$ grid) is stated, not hidden; a second
  radius is a future protocol, not a post-hoc addition.

---

## 7. Assumptions (named, not smuggled)

- **[ASSUMPTION] A-cone-radius:** exactly one angular radius ($\rho = 30^\circ$) is tested. A
  true cone much narrower or wider than $30^\circ$ could be missed — branch (c)'s kill is
  licensed only at the tested radius. The single-radius choice is what makes this the cheapest
  mechanism test; radius sensitivity is a named follow-up, never a post-hoc addition.
- **[ASSUMPTION] A-headroom:** the 40–70% headroom window contains enough rescuable items for
  the paired tests to have power. With Holm gating over the four $\alpha$ tests, the smallest
  adjusted threshold is $0.05/4 = 0.0125$: $(b=8,c=0) \to p=0.0078 < 0.0125$ exact two-sided
  survives Holm; $(b=7,c=0) \to p=0.0156 > 0.0125$ does not. The minimum detectable pure-rescue
  signal is therefore **8 net items** — the test is powered for effects a mechanism claim needs,
  not for 1–2 item flickers.
- **[ASSUMPTION] A-reconstruction:** the archived support set reproduces the EXP066 contrast
  directions up to the §5 continuity floor. If the archive has drifted, the readiness
  assertion — not the decision tree — catches it.
- **[ASSUMPTION] A-bridge-space:** the output bridge is an unembedding-space direction applied
  to the residual stream (cross-space by design, EXP065/066 precedent — empirically validated
  there, $p=0.0020$/$0.0078$). It is a validity gate, not a mechanism claim.

---

## 8. Pre-registered decision tree

**Branch precedence** [DEFINITION] (EXP070 §8 precedent): (d) is evaluated first; then (r);
then (a); then (b); (c) is the residual. A fired higher-precedence branch suspends lower ones. Every
cell below lands in exactly one branch (M5.2).

**Radial shape** [DEFINITION]: $S_H = \{\alpha : \text{Holm-adjusted McNemar } p < 0.05
\text{ vs C1 and } \Delta M > 0\}$ (Holm over the four $\alpha$ tests — MAJOR-3. The curve
remains the endpoint and Law #9 is intact: no $\alpha$ is cherry-picked; only the trigger's
family-wise error is controlled).
- $S_H = \varnothing$ → **empty** (flat-zero).
- $S_H \ne \varnothing$ and $S_H = \{\alpha \ge \alpha^*\}$ for some $\alpha^*$ →
  **upper-set** (monotone-non-decreasing — line-consistent; a singleton upper set is
  consistent with, not proof of, monotonic scaling — MINOR-6).
- $S_H \ne \varnothing$ and not an upper set → **non-upper** (peaked/scattered —
  cone-consistent).
Boundary (M5.1): adjusted $p = 0.05$ exactly counts as null ($p < 0.05$ strict everywhere).

| # | Branch | Trigger (all on gates passing) | Pre-registered ruling |
|---|---|---|---|
| (d) | **INVALID** | Headroom gate fails, or C8 bridge fails ($\Delta M \le 0$ or $p \ge 0.05$), or continuity floor fails, or anti-cheat violation | Reportable invalid run. LICENSES: "preconditions failed; no conclusion about geometry." DOES NOT LICENSE: anything about $H_{\mathrm{cone}}$/$H_{\mathrm{line}}$. |
| (r) | **BOUNDARY-NULL REPLICATION FAILURE** | C3 vs C1: two-sided McNemar $p<0.05$ with $\Delta M \ne 0$ (significant rescue **or** significant corruption — I1 asserts $\Delta M \equiv 0$) | LICENSES: §1.2 (r) — "I1 failed to replicate on pythia-410m/layer-20 at $\alpha=0.5$ in this run." Report $\Delta M$, $(b,c)$, $p$, and this run's baseline accuracy alongside the historical EXP065/066 baselines (comparability rider per EXP075 branch (d)). **No geometry branch fires** — the geometry question is moot when the null itself did not replicate; re-scope under a new pre-registration. DOES NOT LICENSE: anything about $H_{\mathrm{cone}}$/$H_{\mathrm{line}}$. |
| (a) | **CONE-WINS** | (i) angular: McNemar $p<0.05$, $b>c$, **and** control McNemar $p_2<0.05$, $b_2>c_2$; **or** (ii) radial $S_H$ non-upper and nonempty; **or** (iii) offset C6 vs C1: $p<0.05$, $\Delta M>0$ | The firing sub-evidence (angular / radial / affine) is named. LICENSES: §1.2 (a) — blanket null withdrawn, geometry-conditional claim. DOES NOT LICENSE: §1.2 (a) right column. |
| (b) | **LINE-WINS** | (r) and (a) did not fire, **and** [(i) angular: McNemar $p<0.05$, $c>b$; **or** (ii) radial $S_H$ nonempty upper-set] | LICENSES: §1.2 (b) — cone/affine hypothesis rejected for this task; I1 strengthened; if fired via (i), the $\alpha$-scope of the null is narrowed. DOES NOT LICENSE: §1.2 (b) right column. |
| (c) | **NEITHER** | Residual: gates pass, (r), (a), and (b) did not fire — i.e. angular null (or $b>c$ significant but control failed: **attempts-alone**, named), radial $S_H=\varnothing$, offset null | **Kill (unconditional geometry only).** LICENSES: §1.2 (c) — the $\rho=30^\circ$ unconditional cone hypothesis and the $\alpha=1.0$ offset hypothesis die for this task; cones at other radii and the gated variant survive. I1 stands strengthened. DOES NOT LICENSE: §1.2 (c) right column. |

**Exhaustive-partition trace (M5.2):** cells = gates × C3{(sig→(r), null)} ×
angular{(b>c sig, c>b sig, null)} × control{(sig K>R, else)} × radial (Holm){(empty,
upper-nonempty, nonupper-nonempty)} × offset{(sig, null)}. Gates-fail → (d). C3 significant
(either direction) → (r), regardless of all other cells. Angular b>c sig + control sig →
(a)(i). Angular b>c sig + control else → (c) (attempts-alone, named). Radial $S_H$
nonupper-nonempty → (a)(ii) (precedence over (b)(i); suspended by (r) when C3 is significant
— $S_H=\{0.25\}$ alone with C3 null remains a legitimate (a)(ii) firing: a genuine
peaked-at-low-$\alpha$ curve with the boundary null intact). Offset sig → (a)(iii). Angular
c>b sig (with (r)/(a) unfired) → (b)(i). Radial $S_H$ upper-nonempty (with (r)/(a) unfired) →
(b)(ii). Remainder (C3 null, angular null, radial empty, offset null) → (c). Every cell lands
in exactly one branch; no executor discretion.
[M5.1 degenerate:] $b=c=0 \Rightarrow p=1.0$ → angular null.

**Multiplicity disclosure:** three sub-triggers feed branch (a), testing distinct
sub-hypotheses (angular / radial / affine). The angular trigger is conjunctive (both McNemar
$p<0.05$ required — FWER $\approx 0.0025$ under the null); the radial trigger is Holm-gated
($S_H$); the offset trigger is a single test. The licensed claims are motivation-grade
(withdraw/replace the blanket null), not confirmatory-efficacy claims (EXP075 disclosure
precedent).

---

## 9. Budget and compute plan (free-tier feasibility)

[DEFINITION] Primary compute metric: forward passes, worst-case, no caching.

| Phase | Forward passes (worst case) | Basis |
|---|---|---|
| Support presentations (300: 150 rel + 150 neu) | $300$ | builds $\hat{v}_k$, $\mu$ (§3.1–3.2; shared, not double-counted) |
| Test conditions C1–C8 | $480$ | $8 \times 60$ |
| Cone arm C9 | $480$ | $8 \times 60$ |
| Control arm C10 | $480$ | $8 \times 60$ |
| **Total** | **$\le 1{,}740$** | |
| Wall-clock, proposal-anchored [CONJECTURE] | $\approx 1.5$–$2$ h | T4, pythia-410m short sequences (sprint proposal rate: $\approx 450$ passes $\approx$ $<30$ min $\Rightarrow$ $\approx 15$ passes/min; $1{,}740$ passes $\approx$ $\approx 2$ h — actuals logged at execution) |

Fits comfortably in free-tier quota. Order of operations: (1) support build + continuity
assertion (CPU-light metadata + 300 GPU passes) → (2) C1 headroom gate → (3) C8 bridge gate
→ (4) full launch. Splittable across Kaggle sessions at the gate boundaries with all state
archived.

---

## 10. Reproducibility and hygiene (Law #13)

- **Seeds (pre-registered):** master `torch.manual_seed(20260923)`, NumPy `20260923`; cone
  orthogonal axes 7701; control direction + axes 7702. Each pinned seed (7701, 7702) is set
  immediately before its draws (or via a dedicated `torch.Generator` seeded with it), so no
  intervening RNG consumption can desynchronize the pinned constructions. No other randomness
  exists.
- **Archive (all persisted):** $\hat{v}_k$, $\hat{v}$, $\mu$, $\hat{v}^{c}$; the 8 cone axes
  $w_j$ and angles $\phi_j$; control $r$, $q_j$; per-instance correctness for C1–C10
  (EXP066 JSON schema); per-instance rescue indicators $L, K, R, A_\alpha, O$; support/
  benchmark id lists (disjointness audit); injection-vector norms (asserted $>0$);
  environment manifest; SHA-256 pre/post.
- **Hook isolation:** forward hook per instance, removed after; no inter-instance state.
- **No silent retuning:** any change to directions, $\rho$, $K$, $\alpha$ grid, gates, or
  seeds after execution begins is a protocol violation — the changed design takes the next
  free number at pre-registration time.

---

## 11. Non-goals (explicit)

- The CAST-style gated variant (fire $\hat{v}$ only when $\cos(h, \text{pattern}) > \tau$)
  is **not** tested — it is conditionality, P5's tournament territory. Named residual, not
  an oversight: branch (c)'s kill does not extend to it.
- Per-vocabulary centring is not tested (EXP073's territory).
- No second cone radius (A-cone-radius); no other models, layers, or $\alpha$ grids.
- This protocol does not move the novelty tier in any direction (N1 stands — conical/affine
  variants of known vectors are a known combination, honestly labeled).

---

## 12. What EXP077 does NOT test

- Whether a *learned* cone (rather than the fixed $\rho=30^\circ$ cone around $\hat{v}$)
  would rescue — the cone here is posited, not fit.
- The origin of the raw $\approx 0.7$ cosine (Q2 of the boundary formalization — template
  ablations are a separate protocol).
- Cross-model or cross-scale geometry (410m only).
- The adaptive loop, the verifier, or any target-free evaluator (EXP068/070 territory).

---

**Pre-registration checklist:** ☐ $\hat{v} = B_{\mathrm{agg}}$ reconstruction fixed (§3.1, continuity floor §5) ☐ offset direction fixed (§3.2) ☐ cone operationalization fixed ($\rho=30^\circ$, $K=8$, $\phi_j$ grid, seed 7701) ☐ control cone fixed (seed 7702) ☐ $\alpha$ grid fixed $\{0.25,0.5,1.0,2.0\}$ [ARBITRARY] ☐ 10 conditions fixed (§4) ☐ per-instance rescue criteria fixed (§3.6) ☐ headroom + bridge + continuity gates armed (§5) ☐ full decision tree recorded (§8, five branches, precedence (d)>(r)>(a)>(b)>(c), exhaustive partition traced incl. the C3-significant cell) ☐ replication-failure branch (r) armed (C3 significant in either direction → (r), supersedes all geometry branches) ☐ radial shape classified on Holm-adjusted $p$ ($S_H$); A-headroom minimum detectable pure-rescue signal = 8 net items ☐ kill criterion exact (flat-zero = all four Holm-adjusted McNemar $p \ge 0.05$ vs C1 + offset null + angular null → (c); C3-significant → (r) first) ☐ kill license carries the $\rho=30^\circ$/unconditional condition in the sentence (A-cone-radius; gated variant explicitly unkilled) ☐ sweep qualifiers carried unlaundered (LOW-confidence secondary source; practitioner-doc-only QCRI/ACE) ☐ multiplicity disclosure recorded (§8) ☐ RNG seed-ordering fixed (seeds set immediately before draws / dedicated generators) ☐ SHA-256 carried from EXP067 (`4c24…dd`, sanity check; binding guard = runtime pre/post match) ☐ budget $\le 1{,}740$ passes (wall-clock $\approx 1.5$–$2$ h [CONJECTURE], proposal-anchored) ☐ proposal-fidelity amendment appended to sprint P6 (Laws #4/#12) ☐ N1 framing intact
*No results exist under this protocol. Any deviation is a protocol violation, not a discovery.*
