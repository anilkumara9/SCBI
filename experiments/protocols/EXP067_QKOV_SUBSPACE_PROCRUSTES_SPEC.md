# EXP067 Protocol Specification: Attention-Head QK/OV Subspace Procrustes Projection

**Status:** PRE-REGISTERED (protocol; not yet executed)
**Date:** 2026-09-23
**Author role:** Theory Agent
**Predecessor experiments:** EXP063–EXP066 (boundary series)
**Governing standards:** `AGENTS.md` (14 Inviolable Laws), `STATISTICAL_PROTOCOL_V02.md`,
`theory/proofs/procrustes_failure_analysis.md`, `theory/BOUNDARY_CLAIM_FORMALIZATION.md`
**Execution rule:** Strictly confirmatory. No mechanism or hyperparameter changes after Stage A gate
without a new pre-registration.

---

## 1. Research question and hypotheses

$$\boxed{\textbf{Does a \textit{sound} Procrustes alignment operator enable causal transfer
of cross-vocabulary relational bases where the unsound EXP065/066 operator could not?}}$$

**[HYPOTHESIS] H1:** A Procrustes rotation that is (a) fit in the *same* space as the intervention
(per-head attention OV output subspaces, not unembedding→residual) and (b) *full-rank-constrained*
(rank ≥ subspace dimension, explicit identity on the orthogonal complement) produces
$\Delta M > 0$ with McNemar exact $p < 0.05$ on the N=60 headroom-calibrated benchmark.

**Null $H_0$:** $\Delta M = 0$ ($p \ge 0.05$) for the soundly-aligned condition.

### 1.1 Scope of this experiment (boundary science, not novelty science)

[INTERPRETATION] EXP067 is a **boundary-characterization experiment**, not a novelty experiment
(Wave 2 adversarial review §5). Its research question — "does operator soundness change the
Stage B null?" — is legitimate boundary science: it determines whether the I1 dissociation
(raw geometric similarity without causal transfer) survives a fair, sound-operator test. Its
outcome **cannot move the novelty needle in either direction**: a positive C3 result would be a
better-executed instance of an N0 mechanism (algorithmically equivalent to CAA; cf.
`reports/novelty_report.md`); a null result confirms the boundary. The per-instance
$\mathcal{G}/\mathcal{E}/\mathcal{S}/\mathcal{T}$ loop — the only component with any
novelty-relevant claim — is explicitly out of scope here (see §9) and requires a separate future
protocol contingent on an operational loop specification, which does not currently exist.

### 1.2 Defects being fixed (traceability to audit)

| # | EXP065/066 defect (audit Finding 2) | EXP067 fix (this protocol) |
|---|---|---|
| D1 | Rank-2 fit ($r \le 2 \ll d$); Lemma: rotation arbitrary on $(d-r)$-dim complement → scramble | Full-rank fit: $m = 80$ anchors $\ge d_h = 64$; runtime rank + spectral-gap verification (§5) |
| D2 | Fit on unembedding rows, applied to residual-stream directions (A-cross, unvalidated) | Fit **and** applied inside the per-head OV output subspace $S_h = \mathrm{col}(W_O^{(h)})$ |
| D3 | Per-instance 2-anchor rotation $R(x)$ (the rank-deficiency made per-instance fit hopeless) | Per-vocabulary-pair rotation fit once from anchors at inference time (still $\Delta\theta=0$) |
| D4 | No gate on whether alignment was achieved before testing causality | Stage A gate: halt if no head shows alignment gain on held-out support data (§6) |

---

## 2. Frozen model and SHA-256 guard

- **Model / tokenizer:** `EleutherAI/pythia-410m` (identical to EXP066).
- **Architecture [FACT]:** GPT-NeoX; 405,081,600 params; $d = 1024$; 24 layers; **16 attention heads**;
  head dim $d_h = 64$; rotary embeddings; parallel attention/MLP; untied output embeddings.
- **Target layer:** $l^* = 20$ (83% depth, matching EXP066).
- **Expected SHA-256** (pre and post, over all parameters): `4c242d9ac702a4029a674eacee84e0517cb6f79d794661dc3a3102bca5ed48dd`.
- **Guard procedure [FACT-level requirement]:** compute SHA-256 over the concatenation of
  `state_dict()` tensors (sorted keys, CPU, float32 bytes) *before* Stage A and *after* Stage B.
  On mismatch: **abort immediately**, log, report no results. $\boxed{\Delta\theta \equiv 0}$ is
  non-negotiable (Law #6).
- **Binding-vs-sanity distinction (E-4):** the **binding** guard is the runtime pre/post match
  computed in the execution environment. The registered value above (computed 2026-09-23 in the
  original environment) is a sanity check, not an independent abort trigger — environment
  differences in tokenizer/config handling must not produce false aborts.

---

## 3. Formal mechanism

### 3.1 Per-head OV subspace [DEFINITION]

For head $h \in \{1..16\}$ at layer $l^*$, let $W_O^{(h)} \in \mathbb{R}^{d \times d_h}$ be its output
projection block. Define the head output subspace

$$S_h := \mathrm{col}(W_O^{(h)}) \subset \mathbb{R}^d, \qquad \dim S_h = d_h = 64,$$

with orthonormal basis $Q_h \in \mathbb{R}^{d \times 64}$ from a (pre-registered, deterministic)
thin-QR of $W_O^{(h)}$. The head's contribution to the residual stream,
$o_h = W_O^{(h)} z_h$, satisfies $o_h \in S_h$ by construction — this is the space the
intervention will act in.

### 3.2 Anchors (same-space correspondences) [DEFINITION]

Pre-register 16 anchor prompt templates $\{T_j\}_{j=1}^{16}$, disjoint from all test benchmark
prompts. For vocabulary $V$ with entity set $E(V)$ and head $h$:

$$a_{h}(V, e, T_j) := \text{head-}h\text{ output vector } o_h \text{ when processing } T_j(e)
\quad \in S_h.$$

Anchor *pairs* for the ordered vocabulary pair $(V_a \to V_b)$ match entities by **role**
(head-role / tail-role slots, as in EXP065 §2):

$$\mathcal{P}_h^{(a \to b)} = \big\{\big(Q_h^T a_h(V_a, e_i, T_j),\; Q_h^T a_h(V_b, e'_i, T_j)\big)\big\}_{i,j},$$

with $m = 80$ pairs (5 entities $\times$ 16 templates; role-matched). Both elements live in
$\mathbb{R}^{64} = $ subspace coordinates of $S_h$.

**[ASSUMPTION] A-anchor:** role-matched head-output vectors across vocabularies are valid
correspondences for the relational frame. Weaker than A-cross (same space, full rank); tested by
the Stage A gate rather than assumed.

**[ASSUMPTION] A-uniform (named per Wave 2 review E-3):** the vocabulary-renaming rotation
estimated from entity-frame anchors acts uniformly on *relational* directions in $S_h$. This is
the surviving cousin of A-cross: same-space fixed the *space* defect, but the *object* mismatch
(fit object $\ne$ apply object) remains. It is not assumed blindly — the Stage A gate (§3.5)
computes the alignment gain $g_h$ on held-out **relational** directions $\tilde{v}_k^{(h)}$, so the
gate is A-uniform's empirical test. If the gate halts, A-uniform is rejected on support data.

### 3.3 Full-rank subspace Procrustes [DEFINITION]

Stack pairs into $\tilde{A}, \tilde{B} \in \mathbb{R}^{m \times 64}$ ($m = 80$). Fit

$$\tilde{M}_h = \tilde{B}^T \tilde{A} \in \mathbb{R}^{64 \times 64}, \qquad
\tilde{U}\tilde{\Sigma}\tilde{V}^T = \mathrm{SVD}(\tilde{M}_h), \qquad
\tilde{R}_h = \tilde{U}\tilde{V}^T \in O(64).$$

**Runtime guards (pre-registered, abort on violation):**
- $\mathrm{rank}(\tilde{M}_h) = 64$ (else: rank-deficient → abort; this is the D1 tripwire).
- Spectral gap $\tilde{\sigma}_{64} / \tilde{\sigma}_1 > 10^{-6}$ (else: near-degenerate → abort).

Lift to the residual stream with **explicit identity on the complement** (the anti-scramble fix):

$$\boxed{R_h \;=\; Q_h \tilde{R}_h Q_h^T \;+\; (I_d - Q_h Q_h^T)} \qquad R_h \in O(d).$$

**[FACT]:** $R_h$ is a genuine rotation, fully determined by the task data (no arbitrary
complement), reducing to $\tilde{R}_h$ on $S_h$ and the identity elsewhere.

### 3.4 Intervention

Let $B_{\mathrm{agg}}$ be the aggregated contrast basis (constructed exactly as in EXP065/066,
$\alpha = 0.50$ inherited). For test instance $x$ with novel vocabulary $V_{\mathrm{test}}$,
with $\tilde{R}_h^{(\mathrm{supp} \to V_{\mathrm{test}})}$ fit per §3.3 from anchors (support frame →
test-vocabulary frame, **blind to test labels/options/answers** — entity tokens only, cf. Law #7):

- **C3 (aligned dynamic basis):** $h \leftarrow h + \alpha \sum_{h \in H^*} Q_h(\tilde{R}_h - I_{64})Q_h^T B_{\mathrm{agg}}$
- **C2 (static basis):** $h \leftarrow h + \alpha \sum_{h \in H^*} Q_h Q_h^T B_{\mathrm{agg}}$ (head-projected, no rotation). Note (E-5): C2 is **not** EXP066's historical static condition (full $B_{\mathrm{agg}}$); the C2-vs-C3 contrast cleanly isolates the rotation effect *within head subspaces*, but any comparison of C2 against the EXP066 static null must note the changed intervention.

### 3.5 Head selection $H^*$ (pre-registered, support-data only)

On **held-out support vocabulary pairs** (never test data), per head compute the alignment gain

$$g_h = \tfrac{1}{4}\sum_{k=2}^{5}\Big[\cos\big(\tilde{R}_h^{(1\to k)}\tilde{v}_1^{(h)},\, \tilde{v}_k^{(h)}\big)
- \cos\big(\tilde{v}_1^{(h)},\, \tilde{v}_k^{(h)}\big)\Big], \quad
\tilde{v}_k^{(h)} = Q_h^T \hat{v}_k.$$

Select $H^* = $ top $K = 4$ heads with $g_h > 0$. **Stage A gate:** if no head satisfies $g_h > 0$,
**HALT** — do not run Stage B. Per §7.1, this halt is a **reportable outcome** ("A-anchor/A-uniform
rejected on support data; H1 untestable under this operationalization"), not a non-result; write
the full per-head $g_h$ table to the run directory and report it.

---

## 4. The 7 mandated conditions

| # | Condition | Intervention |
|---|---|---|
| C1 | Unintervened baseline | none |
| C2 | Static basis (head-projected) | §3.4 C2 |
| C3 | **Aligned dynamic basis (EXP067 mechanism)** | §3.4 C3 — primary test condition |
| C4 | Same-layer output bridge (positive control) | identical to EXP066 `make_bridge_vec` |
| C5 | Random rotations × 5 seeds | $R_h$ with $\tilde{R}_h \sim \mathrm{Haar}(O(64))$, seeds $\{11,22,33,44,55\}$, averaged |
| C6 | Dynamic $B_\perp$ | C3 pipeline with $B_{\mathrm{agg}}^\perp$ |
| C7 | Dynamic $B_{\mathrm{wrong}}$ | C3 pipeline with wrong-task basis (Paris-capital contrast, as EXP066) |

## 5. Benchmark and headroom

- **Benchmark:** the identical N=60 Planetary/Elemental 2-hop/3-hop suite ported from EXP065/066
  (same items, same premise permutations). No new benchmark construction (Law #9: no post-hoc tuning).
- **Headroom gate:** run C1 first; require baseline accuracy $\in [40\%, 70\%]$.
  If outside: **HALT**, do not proceed; any recalibration requires a new pre-registration.
  A headroom halt is a reportable outcome per §7.2 (benchmark miscalibrated), not a trigger for
  adjustment under the EXP067 label.

## 6. Endpoints

- **Primary (confirmatory):** $\Delta M$ (percentage points) on paired decisions, C3 vs C1;
  McNemar exact test on $(b, c)$. **Success:** $\Delta M > 0$ **and** $p < 0.05$.
- **Secondary (exploratory):** rescues $b$, corruptions $c$; $\mathrm{KL}_{\mathrm{div}} < 0.50$ guardrail;
  $\|\Delta H\|$ norm; per-head $g_h$ table.
- **Margin shifts:** recorded but **exploratory only** — audit Finding 3 stands: the C7 control
  invalidates margin-shift significance as a causal endpoint. Never reported as confirmatory evidence.

## 7. Falsification criterion and pre-registered decision tree

### 7.0 Canonical criterion (single source of truth; cf. `theory/BOUNDARY_CLAIM_FORMALIZATION.md` §3.3, which quotes this box verbatim)

$$\boxed{\textbf{If C3 yields } \Delta M = 0 \textbf{ (McNemar } p \ge 0.05,\ b = 0\textbf{)}
\textbf{ while C4 yields } \Delta M > 0 \textbf{ (}p < 0.05\textbf{, } \ge 5 \textbf{ rescues),}
\textbf{ then H1 is FALSIFIED.}}$$

**[INTERPRETATION] of that outcome:** the representational–causal dissociation is a structural
property of the architecture at this scale, not an artifact of alignment-operator quality; the
research program pivots to characterizing *where* the causal chain breaks (QK routing vs OV
transport vs MLP readout) rather than *how* to align better. A positive C3 result instead
confirms H1 and reopens the boundary claim for revision — with the §1.1 scope note: a positive
C3 is a better-executed N0 mechanism (CAA-equivalent), not a novelty result.

### 7.1 Full decision tree (pre-registered; every branch has a ruling)

| # | Branch | Pre-registered ruling |
|---|---|---|
| (a) | **Stage A gate halts** (no head with $g_h > 0$, or rank/spectral guard aborts) | A-anchor/A-uniform rejected on support data. H1 is **untestable under this operationalization** — neither falsified nor confirmed. I1 (the boundary claim) stands unchallenged by this experiment. Report the full diagnostic table ($g_h$ per head, rank/spectral values). |
| (b) | **C4 positive control fails** (bridge does not replicate: $\Delta M \le 0$ or $p \ge 0.05$) | **Invalid run.** Setup broken or benchmark drifted; **no conclusion about H1 may be drawn.** Diagnose (model hash, benchmark integrity, hook lifecycle) before any re-registration. Do not interpret C3 in an invalid run. |
| (c1) | **C3 mixed: $b > 0$ but $p \ge 0.05$** | H1 **not confirmed**. Report as weak/partial evidence with exact statistics ($b$, $c$, $p$, $\Delta M$); no success claim. |
| (c2) | **C3 mixed: $\Delta M < 0$** | Report as a **negative result** per Law #8 with full statistics. H1 not confirmed. |
| (c3) | **C3 mixed: $b > 0$ and $c > 0$** | Report net $\Delta M$ with both counts; H1 **not confirmed** (success requires $\Delta M > 0$, $p < 0.05$). |
| (d) | **Canonical branch:** C3 $\Delta M = 0$ ($p \ge 0.05$, $b = 0$) ∧ C4 $\Delta M > 0$ ($p < 0.05$, $\ge 5$ rescues) | **H1 FALSIFIED** (canonical criterion §7.0). |
| (e) | **C3 success:** $\Delta M > 0$ **and** $p < 0.05$ (with C4 valid) | **H1 confirmed** — boundary claim reopens for revision; §1.1 novelty scope applies. |

### 7.2 Halt gates are reportable outcomes (E-2)

EXP067 has three halt gates: the Stage A gate (§3.5), the rank/spectral guard (§3.3), and the
headroom gate (§5). **Any halt IS the published outcome of EXP067** — a halted EXP067 is a
result (A-anchor rejected / benchmark miscalibrated), not a non-result. On any halt: write the
full diagnostic table ($g_h$ per head, rank/spectral values, baseline accuracy) to
`experiments/runs/EXP067_qkov_subspace_procrustes/` and report it. **Explicitly forbidden:**
re-running with adjusted anchors, $K$, templates, or headroom handling under the EXP067 label
(tweak-and-rerun would make the gates p-hacking-adjacent). Any adjusted design is **EXP068**
with a new pre-registration.

## 8. Reproducibility and hygiene

- **Seeds (pre-registered):** `torch.manual_seed(20260923)`, NumPy `20260923`; C5 rotation seeds
  $\{11, 22, 33, 44, 55\}$; $B_\perp$ seed 9876 (inherited).
- **Hook isolation:** register forward hook per instance, remove after; assert handle lifecycle in
  logs; verify no inter-instance state (Law: state $z_t$ wiped between episodes).
- **Determinism:** `torch.use_deterministic_algorithms(True)` where supported; record environment
  manifest (torch/cuda versions).
- **Raw logs:** per-instance records (prompt id, base/mod correct, margin shift, KL) written to
  `experiments/runs/EXP067_qkov_subspace_procrustes/` in the EXP066 JSON schema.

## 9. What EXP067 does NOT test

- Per-instance dynamic rotations (deliberately removed as part of defect D3).
- The per-instance $\mathcal{G}/\mathcal{E}/\mathcal{S}/\mathcal{T}$ loop. A loop experiment may be
  pre-registered only after an **operational loop specification exists on paper** — no such spec
  currently exists in the repo (Wave 2 review §5). Any future loop protocol (EXP068 candidate)
  must take PPLM (Dathathri et al., ICLR 2020), ToT, and Self-Refine as explicit design priors it
  distinguishes itself from, and must beat compute-matched baselines (self-consistency, Best-of-N).
- MLP-readout or QK-attention-pattern interventions (Q3 of the formalization doc remains open).
- The origin of raw similarity O1 $\approx 0.7$ (Q2; needs template-ablation controls, separate study).
- Any claim beyond pythia-410m / layer 20 / this benchmark family (scope per I3).

---

**Pre-registration checklist:** ☐ anchors/templates fixed ☐ $K=4$, $\alpha=0.50$ fixed ☐ seeds fixed
☐ headroom gate armed ☐ Stage A gate armed ☐ SHA-256 guard armed ☐ falsification criterion recorded
☐ full decision tree recorded (§7.1) ☐ §1.1 boundary-science scope acknowledged.
*No results exist under this protocol. Any deviation is a protocol violation, not a discovery.*
