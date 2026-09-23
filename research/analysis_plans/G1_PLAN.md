# G1 — Weight-only QK/OV Projection-Energy Audit: FROZEN ANALYSIS PLAN

**LOG-134** · Phase 1 (plan only) · Status: **FROZEN — NO EXECUTION**
**Author:** G1 specialist analyst (Research Lead dispatch, CEO LOG-134 grant)
**Date:** 2026-09-23
**Source:** `research/innovation/SPRINT2_2026-09-23.md` §G1 (Tier 0 gate, [CONJECTURE], N1, zero ledger hits)
**Gate:** This plan goes to the Wednesday adversarial slot. Execution (Phase 2) requires
the Research Lead's explicit go-ahead after that review. No model weight was touched in
writing this plan.

---

## 1. Question and claim under test

**[CONJECTURE] under test** (handover `.muse by meta/THEORY_AND_MATHEMATICAL_FOUNDATIONS.md`
§3.3, "Core Causal Null-Space Theorem"): the failed relational contrast directions project
near-zero energy into downstream attention heads' QK subspaces — i.e.,
$\mathcal{J}_{F}(h_l)\,b_{\mathrm{dynamic}} \approx 0$ because the direction "fails to align
with the specific query/key projection matrices $W_Q^{(l+1)}, W_K^{(l+1)}$ of downstream
attention heads" — while the rescuing output bridge projects large energy
($(w_{y_t}-w_{y_f})^T\mathcal{J}_{F}(h_l)\,v_{\mathrm{output}}^{(l)} \gg 0$).

**[FACT]:** all 66 ledger experiments assume this mechanism; none measured it. EXP067's
Stage-A halt left it unexamined. This audit is the first direct measurement.

**Question.** Do the failed directions (EXP077's $B_{\mathrm{agg}}$ family, $d=1024$,
pythia-410m, layer-20 injection point) carry near-zero projection energy into downstream
heads' QK subspaces while the rescuing bridge carries large energy?

---

## 2. Notation context (M1.1 — scope: this document only)

- $l^* = 20$: injection layer (EXP077 `TARGET_LAYER`; vectors archived from
  `hidden_states[l^*+1]`, last token).
- Model: EleutherAI pythia-410m — $L = 24$ layers indexed $0..23$, $H = 16$ heads/layer,
  $d = 1024$, head dim $d_h = 64$. Local snapshot `9879c9b5f8bea9051dcb0e68dff21493d67e9d4f`
  (provenance, F5 fix: `/home/hatch/.cache/huggingface/hub/models--EleutherAI--pythia-410m/snapshots/9879c9b5f8bea9051dcb0e68dff21493d67e9d4f/`, verified 2026-09-23).
- Downstream head set $\mathcal{H} = \{(l,h) : l \in \{21,22,23\},\ h \in \{0,\dots,15\}\}$,
  $|\mathcal{H}| = 48$. (Layers strictly downstream of the $l^*=20$ injection point.)
- For head $(l,h)$ (M4.1 shapes at first use):
  $W_Q^{l,h}, W_K^{l,h}, W_V^{l,h} \in \mathbb{R}^{64 \times 1024}$ — per-head row blocks of
  the fused QKV weight; $W_O^{l,h} \in \mathbb{R}^{1024 \times 64}$ — per-head column block
  of the attention dense weight. (Executor verifies this layout against the loaded
  `state_dict` with shape asserts before any computation; layout mismatch = FATAL stop.)
- $M_{\mathrm{QK}}^{l,h} = \begin{bmatrix} W_Q^{l,h} \\ W_K^{l,h} \end{bmatrix}
  \in \mathbb{R}^{128 \times 1024}$ (vertical stack).
  Thin SVD $M_{\mathrm{QK}}^{l,h} = U\Sigma V^{\top}$, $V \in \mathbb{R}^{1024 \times k_h}$,
  $k_h = \operatorname{rank}(M_{\mathrm{QK}}^{l,h}) \le 128$ (M4.3: fit rank stated per head;
  orthogonal complement has dimension $d - k_h$).
  $P_{\mathrm{QK}}^{l,h} = V V^{\top} \in \mathbb{R}^{1024 \times 1024}$: the orthogonal
  projector onto $\operatorname{rowspace}(M_{\mathrm{QK}}^{l,h})$ — the subspace of
  residual-stream directions visible to head $(l,h)$'s query/key projections.
  **[DEFINITION] (local):** "QK subspace of head $(l,h)$".
- $M_{\mathrm{OV}}^{l,h} = \begin{bmatrix} W_O^{l,h} & (W_V^{l,h})^{\top} \end{bmatrix}
  \in \mathbb{R}^{1024 \times 128}$. Thin SVD $\to \tilde{U} \in \mathbb{R}^{1024 \times k'_h}$,
  $k'_h \le 128$. $P_{\mathrm{OV}}^{l,h} = \tilde{U}\tilde{U}^{\top}$: orthogonal projector
  onto $\operatorname{span}(\operatorname{colspace}(W_O^{l,h}) \cup
  \operatorname{rowspace}(W_V^{l,h}))$ — residual-stream directions head $(l,h)$'s OV
  circuit can read (via $W_V$) or write (via $W_O$).
  **[DEFINITION] (local):** "OV-path subspace of head $(l,h)$".
- For $v \in \mathbb{R}^{1024}$, $v \ne 0$ (M4.2 space: residual stream at layer $l^*$):
  $$e_{\mathrm{QK}}^{l,h}(v) = \frac{\lVert P_{\mathrm{QK}}^{l,h} v\rVert_2}{\lVert v\rVert_2},
    \qquad
    e_{\mathrm{OV}}^{l,h}(v) = \frac{\lVert P_{\mathrm{OV}}^{l,h} v\rVert_2}{\lVert v\rVert_2}
    \in [0,1].$$
  Scale-invariant by construction (M4.4: every vector below is unit-norm; $e$ is
  homogeneous of degree 0 regardless).
- Aggregates (primary endpoint scale):
  $$\bar{E}_{\mathrm{QK}}(v) = \frac{1}{48}\sum_{(l,h)\in\mathcal{H}} e_{\mathrm{QK}}^{l,h}(v),
    \qquad
    \bar{E}_{\mathrm{OV}}(v) = \frac{1}{48}\sum_{(l,h)\in\mathcal{H}} e_{\mathrm{OV}}^{l,h}(v).$$
- $\rho_j$, $j=1..100$: random null directions (see §5). $s_j$, $j=1..20$: companion
  steering-control directions (see §5).
- Symbol disambiguation (M1.2): $R$ = Procrustes rotation (handover sense) — not used
  computationally here; $\rho$ = random unit vector — never a rank; "rank" always written
  out or as $k_h$; "bridge" always means the output-space direction defined in §4.

---

## 3. Vector set and provenance on disk (no fabrication; gaps stated)

All archived vectors: `experiments/runs/EXP077_cone_vs_line/exp077_vectors.pt`
(137,237 B; pythia-410m; $d=1024$; layer-20 residual stream; all unit-norm, verified
2026-09-23; archive carries `pre_hash == post_hash ==
ec276abe3902fab0166ce56c00de84c2…`, i.e. $\Delta\theta = 0$ at archive time).

| Plan symbol | Archive key / construction | Provenance |
|---|---|---|
| $B_{\mathrm{agg}}$ | `v_hat` | `normalize(Σ_k v̂_k)`; the failed aggregated relational basis (EXP077 C2/C4 arm, $\Delta M = 0$) |
| $\hat{v}_k$, $k=1..5$ | `v_hats` (list of 5) | per-vocabulary normalized mean contrast directions; secondary — checks the aggregate is not a summation artifact |
| $B_{\mathrm{wrong}}$ | `B_wrong` | wrong-task (Paris-capital) contrast at layer 20; negative control ($\Delta M = 0$, $p = 1.2\times10^{-8}$ margin-shift invalidated — O5) |
| $B_{\perp}$ | `B_perp_basis` | seeded unit vector $\perp B_{\mathrm{agg}}$ (seed 9876; verified $\langle B_{\mathrm{agg}}, B_{\perp}\rangle \approx -9.3\times10^{-9}$); direction-family control |
| $b_{\mathrm{mean}}$ (bridge) | **RECONSTRUCTED — not archived** | $b_i = \mathrm{normalize}(E[t_i]-E[f_i])$, $E$ = unembedding weight from the local snapshot (§7); $t_i = $ `tokenizer.encode(" "+A_i)[0]`, $f_i = $ `tokenizer.encode(" "+C_i)[0]`; $(A_i, C_i)$ = the 60 EXP077 bench items rebuilt by the **verbatim** bench-construction code path (`experiments/runs/exp077/run_exp077.py` ll. 591–638, pinned seeds — executor imports, never reimplements); $b_{\mathrm{mean}} = \mathrm{normalize}(\sum_{i=1}^{60} b_i)$. This replicates EXP077 C8 `make_bridge_vec` (ll. 725–729) exactly: the positive control that rescued +23.33pp (b=14, c=0, p=0.000122) in the archived run |
| $\rho_j$ | fresh | §5 |
| $s_j$ | fresh | §5 (companion diagnostic) |
| diagnostics (reported only, non-decision) | `v_hat_c`, `mu`, `u_list` (8), `q_list` (8), `r_vec` | cone basis, centring offset, cone arms, control-cone arms, pinned control axis — all archived |

**Gap stated:** EXP070's vectors were never retrieved locally (nothing to use); EXP078
retrieved no vector archive (run scripts only). The "~170KB archived vectors" in the
sprint brief = the 137 KB EXP077 archive above; the bridge mean is reconstructed, not
archived — flagged here, not silently substituted.

---

## 4. Endpoint definition (formal)

**Primary endpoint (decision-relevant):** $\bar{E}_{\mathrm{QK}}(v)$ for
$v \in \{B_{\mathrm{agg}}, b_{\mathrm{mean}}\}$, tested against the $\rho$-null (§6).

**"Near-null-space" (pre-registered):**
$$\bar{E}_{\mathrm{QK}}(B_{\mathrm{agg}}) < q_{0.05}
\quad\text{AND}\quad
\bar{E}_{\mathrm{QK}}(b_{\mathrm{mean}}) > q_{0.95},$$
where $q_{0.05}, q_{0.95}$ are the 5th and 95th order statistics (0-based indices 4 and
94) of the sorted null sample $S_{\mathrm{QK}} = \{\bar{E}_{\mathrm{QK}}(\rho_j)\}_{j=1}^{100}$.
Strict inequalities; a tie at the threshold fails the conjunct (M5.1 boundary case ruled).

**Secondary endpoint:** identical statistics with $P_{\mathrm{OV}}$: $\bar{E}_{\mathrm{OV}}$,
null sample $S_{\mathrm{OV}}$, same percentile rule — reported as [OBSERVATION]; it
**cannot overturn** the QK verdict (§6).

**Exploratory (reported, no thresholds):** per-head distributions of $e_{\mathrm{QK}}^{l,h}$,
$\bar{E}$ for $\hat{v}_k, B_{\perp}, B_{\mathrm{wrong}}$, diagnostics, MLP gate/up-projection
rowspace energies (sprint's noted extension), and the $s_j$ companion (§5).

---

## 5. Random-$\rho$ null construction (seed pinned, Law #13)

- Dedicated generator: `torch.Generator().manual_seed(20260923)`; no intervening RNG use.
- $g_j \sim \mathcal{N}(0, I_{1024})$ i.i.d., $\rho_j = g_j / \lVert g_j\rVert_2$, $j=1..100$.
- Null samples: $S_{\mathrm{QK}}$, $S_{\mathrm{OV}}$ as above (each $\rho_j$ scored through
  all 48 heads; the aggregate-then-null construction matches the endpoint scale).
- **Companion steering control** $s_j$, $j=1..20$ (seed `20260924`, dedicated generator):
  $s_j = \mathrm{normalize}(E[a_j]-E[b_j])$ for 20 random token pairs $(a_j,b_j)$ drawn
  uniformly from the vocabulary excluding the 60 bench target/foil tokens.
  **Exclusion is at the encoded token-id level:** the excluded ids are exactly the
  `tokenizer.encode(" "+entity)[0]` ids used for the bridge ($t_i, f_i$ in §3) — no
  surface-string matching. **Aggregation-matched companion (F3 fix):**
  $\bar{s} = \mathrm{normalize}(\sum_{j=1}^{20} s_j)$, reported alongside the
  individual $s_j$; the rejection rule below is applied to the aggregation-matched
  comparison $\bar{E}_{\mathrm{QK}}(\bar{s})$ vs $\bar{E}_{\mathrm{QK}}(b_{\mathrm{mean}})$
  (both are aggregates — $b_{\mathrm{mean}}$ of 60, $\bar{s}$ of 20), and the
  median-of-individuals rule is reported as the second statistic.
  **Pre-registered interpretation rule:** if
  $\operatorname{median}_j \bar{E}_{\mathrm{QK}}(s_j) \ge \bar{E}_{\mathrm{QK}}(b_{\mathrm{mean}})$
  OR $\bar{E}_{\mathrm{QK}}(\bar{s}) \ge \bar{E}_{\mathrm{QK}}(b_{\mathrm{mean}})$,
  then "maximize QK-projection energy" is REJECTED as a sufficient-condition design
  objective even under a CONSISTENT verdict — high QK energy would be generic to
  unembedding-difference directions, not specific to the rescuing bridge. (This control
  exists because the bridge's rescue is independently explained by the readout bypass /
  near-direct logit steering — audit Finding 4; G1 must not let a survive-verdict upgrade
  the bridge's mechanism story.)

---

## 6. Exact permutation-$p$ procedure (M5.3)

- $H_0$: $\bar{E}_{\mathrm{QK}}(v)$ is exchangeable with the 100 null draws — i.e., $v$
  carries no special alignment with downstream QK subspaces. Exchangeability holds
  because under $H_0$ the observed direction is one more uniform-on-sphere draw; the
  projectors are fixed weight-derived quantities independent of $v$.
- $p_{\mathrm{low}}(v) = \frac{1 + \#\{j : \bar{E}_{\mathrm{QK}}(\rho_j) \le \bar{E}_{\mathrm{QK}}(v)\}}{101}$;
  $p_{\mathrm{high}}(v) = \frac{1 + \#\{j : \bar{E}_{\mathrm{QK}}(\rho_j) \ge \bar{E}_{\mathrm{QK}}(v)\}}{101}$
  (Phipson–Smyth exact Monte Carlo $p$; $B=100$ pinned, seed §5 — minimum attainable
  $p = 1/101 \approx 0.0099$).
- Reported for $v \in \{B_{\mathrm{agg}}, b_{\mathrm{mean}}\}$ on QK and OV. The $p$-values
  are evidence, not the decision rule — the decision uses the pre-registered percentile
  rule + kill comparison below.
- Degenerate input (M5.1/M5.3): if all 101 values are identical (zero variance — e.g. a
  degenerate projector), the formulas give $p = 1.0$; the percentile conjuncts fail by the
  tie rule; verdict falls to INCONCLUSIVE. This branch is assigned, not left to executor
  discretion.

---

## 7. Decision rule — exhaustive partition (M5.2)

Let $A = \bar{E}_{\mathrm{QK}}(B_{\mathrm{agg}})$, $B = \bar{E}_{\mathrm{QK}}(b_{\mathrm{mean}})$.
Exactly one fires:

1. **KILL** — if $A \ge B$: the null-space mechanism is dead; the §3.3 theorem's central
   sentence ("downstream heads project $b_{\mathrm{dynamic}}$ into their null space while
   the bridge projects large energy") is false as a QK-subspace claim; the boundary
   paper's mechanism section must be rewritten (readout-misalignment-or-unknown); the
   QK-subspace operator program is stood down before further GPU spend. (Equality fires
   the kill: the mechanism predicts strict separation.)
2. **CONSISTENT** (survive license) — else, if $A < q_{0.05}$ AND $B > q_{0.95}$: the
   projection-energy ordering is consistent with the null-space story.
3. **INCONCLUSIVE** — otherwise.

**Licenses.** CONSISTENT licenses: first direct measurement consistent with the §3.3
mechanism; a designable *correlate* (QK-projection energy) for Phase 2. It does **not**
license: causal transfer (no intervention measured), new QK-GPU spend (requires the
Wednesday adversarial review of these results), or the "maximize QK energy" objective
without the $s_j$ companion ruling in its favor (§5). KILL licenses the re-routing in (1).

---

## 8. Execution constraints (binding on Phase 2)

- CPU-only. No Kaggle, no network. `~/workspace/.venv_smoke/bin/python` (torch +
  transformers present, verified 2026-09-23).
- Model loaded with `local_files_only=True`, **`torch_dtype=torch.float32` explicit**
  (LOG-109 lesson; transformers 5.x defaults to float16 — a silent dtype flip would
  corrupt the SVD energy ratios).
- **Read-only:** weights are read, never mutated; **zero forward passes** (weight-only
  linear algebra — no hooks, no inference). $\Delta\theta = 0$ verified by recomputing
  `get_hash` (`run_exp077.py` ll. 167–174) over the loaded `state_dict` and asserting
  equality with the archived `pre_hash`/`post_hash` before any computation.
- SVD in float32 on CPU (48 heads × two $128\times1024$ thin SVDs — seconds).
- Environment manifest recorded: `pip freeze` of the venv, model snapshot hash +
  HF cache path (§2), `torch.__version__`, seed log.
- No changes to any signed protocol or artifact (Law #12/#14: results are new files).

---

## 9. Assumption inventory (M8.2)

- **[ASSUMPTION] A-G1-bridge (M4.2 transfer assumption):** $b_{\mathrm{mean}}$ is
  constructed from unembedding rows but analyzed as a residual-stream direction at
  layer $l^*$, matching its EXP077 C8 injection site. The audit tests its QK-visibility
  *at that site*, not its unembedding-space geometry. **Falsification:** if
  $\bar{E}_{\mathrm{QK}}(b_{\mathrm{mean}})$ is near-null yet the bridge rescued +23.33pp
  (b=14, c=0, p=0.000122) in the archived run,
  the framing is wrong and the rescue is attributed to the readout bypass alone — itself
  an informative outcome for the paper's mechanism section.
- **[ASSUMPTION] A-G1-linear:** the audit is a first-order linear probe (projectors,
  no LayerNorm/softmax/rotary-positional nonlinearities in the energy measure). Justified:
  the §3.3 theorem is itself stated via the downstream Jacobian $\mathcal{J}_F$ — a
  linearization — so a linear-algebra operationalization is faithful to the claim.
- **[FACT] (rotary invariance):** for invertible $R$, $\operatorname{rowspace}(RW) =
  \operatorname{rowspace}(W)$ (proof: $\{W^{\top}R^{\top}y\} = \{W^{\top}z\}$ since
  $R^{\top}$ is bijective). Hence $P_{\mathrm{QK}}^{l,h}$ is invariant to per-position
  rotary rotations on Q/K — the rotary objection does not apply to $e_{\mathrm{QK}}$.
  **(F4 strengthening):** the position-dependent case is covered by block-diagonality:
  $[R_n W_Q; R_m W_K] = \operatorname{diag}(R_n, R_m)\,[W_Q; W_K]$ with
  $\operatorname{diag}(R_n,R_m)$ invertible for $R_n \ne R_m$, so the row space is
  preserved; partial RoPE (rotation $\oplus$ identity on the non-rotated head-dim
  block) is likewise invertible, hence also row-space-preserving.
- **[ILLUSTRATIVE] sanity check (M3.1, not a decision input):** for fixed subspace dim
  $k_h \le 128$, $d=1024$, uniform-on-sphere $v$: $\mathbb{E}[\lVert P v\rVert_2^2] =
  k_h/d \le 0.125$, so $\mathbb{E}[e] \lesssim 0.354$. The executor reports the null
  sample mean against this band as a code-correctness check only.

---

## 10. Falsification checklist (M8)

1. **What would prove the plan's target claim false?** $\bar{E}_{\mathrm{QK}}(B_{\mathrm{agg}})
   \ge \bar{E}_{\mathrm{QK}}(b_{\mathrm{mean}})$ (KILL branch) — the failed direction is
   at least as QK-visible as the rescuer. Or: the $s_j$ companion shows task-free
   steering directions are equally QK-visible (kills the design-objective reading).
2. **Assumption inventory:** §9 above (A-G1-bridge, A-G1-linear); the rotary [FACT] needs
   no assumption. No others.
3. **What did the adversary try?** Reserved for the Wednesday slot; pre-registered attack
   surfaces: (a) bridge reconstruction fidelity (bench rebuild vs archived C8 vectors —
   executor cross-checks $\cos(b_i, \text{archived C8 direction})$ if retrievable);
   (b) head-set choice (21–23 vs including layer 20's own heads — executor reports
   sensitivity with layer 20 included, non-decision); (c) mean-vs-max aggregation
   (executor reports max-head energies as diagnostic); (d) the anisotropy confound — **disclosed limitation (F2 fix):** the uniform-on-sphere
   $\rho$-null does not model $B_{\mathrm{agg}}$'s data-conditioned distribution
   (contrast directions from real support data live on an anisotropic manifold);
   the relative-to-null percentile rule avoids absolute thresholds but does **not**
   correct for anisotropy. A CONSISTENT verdict therefore cannot distinguish
   "QK-subspace visibility" from "generic visibility of data-conditioned
   directions" — the $s_j$ companion (§5) is the guardrail, not a cure.
4. **Do the numbers recompute?** Executor ships a results JSON with unrounded values
   (M3.4) and the seeds; the Wednesday reviewer recomputes from the archive + snapshot.
5. **Does the label survive citation?** Any citation of a CONSISTENT verdict must carry
   "consistent with, not confirming" (M2.4 condition-laundering is a MAJOR finding).
6. **Smallest change that breaks it:** the percentile thresholds ($q_{0.05}/q_{0.95}$)
   and the mean-over-heads aggregation — both are pre-registered here precisely so they
   cannot be tuned post-hoc (Law #9).

---

## 11. Output artifacts (Phase 2, on go-ahead only)

- `research/analysis_plans/G1_RESULTS_2026-09-23.json` — unrounded numbers, seeds,
  environment manifest, per-head tables.
- `research/analysis_plans/G1_REPORT_2026-09-23.md` — verdict (KILL/CONSISTENT/
  INCONCLUSIVE), what it licenses, Wednesday-review notes.
- Log entry under the executor's LOG number in `reports/research_log.md`.
- This plan file is immutable from here (Law #14: corrections proposed, never applied,
  until signed off).

---

## 12. Review history

- 2026-09-23: plan frozen by LOG-134 specialist (Phase 1). Awaiting Wednesday
  adversarial slot + Research Lead go-ahead before Phase 2 execution.
- 2026-09-23: Wednesday adversarial review (LOG-137) — verdict **CLEAR-WITH-FIXES**,
  no FATAL, no MAJOR; five MINOR fixes F1–F5 applied above (bridge rescue number
  corrected to the archived run +23.33pp; anisotropy limitation disclosed; companion
  $s_j$ exclusion at token-id level + aggregation-matched $\bar{s}$ pre-registered;
  rotary [FACT] strengthened with block-diagonal line; snapshot cache-path
  provenance recorded). §9's "+10pp" descriptive reference corrected alongside F1
  for consistency. No re-verification required by the reviewer. **Plan re-frozen —
  weights still untouched. Phase 2 go-ahead issued by the Research Lead.**
