# EXP039: Prospective Representation-Generator Selection Specification

## 1. Executive Summary & Epistemological Status
- **Experiment ID:** `EXP039`
- **Date:** 2026-09-12
- **Governing Law:** All 14 Inviolable Agent Laws in [`AGENTS.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/AGENTS.md).
- **Epistemological Status:** `[HYPOTHESIS]` Pre-registered confirmatory benchmark testing whether an autonomous model can prospectively predict which qualitative representation generator ($G_{\mathrm{trajectory}}$, $G_{\mathrm{context}}$, or $G_{\mathrm{attention}}$) is optimal for a given prompt *before* spending forward passes to evaluate candidates, evaluating whether prospective generator selection captures Oracle multi-generator headroom under $1.0$ forward pass per instance ($\Delta\theta \equiv 0$).
- **Evaluated Architecture:** `EleutherAI/pythia-160m` (12 layers, $d_{\mathrm{model}}=768$, Revision `e72e396263595503028d71243171317d7ae65463`).
- **Benchmark:** `BENCH-002-NL` ($N = 50$ confirmatory instances, Seed 84).
- **Frozen Backbone Guarantee:** Pre/post parameter SHA-256 hash verified invariant: `54c88fa4897785f2bd94b32d26de1f73f1052bcc42124d563d0cda96940de936`.

---

## 2. Theoretical Motivation: Representation Strategy vs. Blind Search

EXP038 established a decisive negative result:
$$\boxed{\text{More Candidate Bases } \not\Rightarrow \text{ Better Inference}}$$
Iterating blindly through secondary singular vectors ($V_2 = \operatorname{SVD}_{3:4}$) tripled compute cost ($2.98$ passes/instance) while yielding only 1 rescue across 49 attempts, achieving lower FLOP efficiency than a single well-targeted pass.

This demonstrates that `CHANGE BASIS` cannot simply mean spectral exhaustion of a single matrix. Useful representation search requires selecting among **qualitatively distinct candidate generators**:
$$\mathcal{G}_{\mathrm{pool}} = \{G_{\mathrm{trajectory}}, G_{\mathrm{context}}, G_{\mathrm{attention}}\}$$

However, evaluating all generators sequentially is computationally wasteful ($3\times$ FLOPs). Therefore, EXP039 addresses the fundamental question:

$$\boxed{\textbf{Can a model autonomously predict which representation generator to use BEFORE spending inference compute?}}$$

Mathematically, the system deploys a prospective selection policy:
$$q(g \mid x, h_0) \longrightarrow G_{g^*} \longrightarrow V_{g^*}$$
spending only **$1$ intervention forward pass** per instance.

---

## 3. The 3 Qualitatively Distinct Generator Families ($\mathcal{G}_{\mathrm{pool}}$)

All bases are rank-2 subspaces extracted at target Layer 8:

1. **$G_1$: Inter-Layer Trajectory Flow ($G_{\mathrm{trajectory}}$)**
   - Mechanism: Extracts the principal vector of representational evolution between intermediate depths:
     $$V_{\mathrm{traj}} = \operatorname{SVD}(h_8^{(0)} - h_6^{(0)})_{1:2}$$
   - Hypothesis: Best suited when the model is transitioning cleanly across syntactic/semantic processing stages.

2. **$G_2$: Contextual Counterfactual Perturbation ($G_{\mathrm{context}}$)**
   - Mechanism: Masks 20% of context tokens to extract the subspace most sensitive to prompt premise integrity:
     $$V_{\mathrm{context}} = \operatorname{SVD}(h_8^{(0)} - h_{8,\mathrm{pert}}^{(0)})_{1:2}$$
   - Hypothesis: Best suited when distractor competition threatens context premise retention.

3. **$G_3$: Attention-Derived Relational Subspace ($G_{\mathrm{attention}}$)**
   - Mechanism: Computes the residual difference between attention head outputs with highest attention to the premise vs. distractor:
     $$V_{\mathrm{attn}} = \operatorname{SVD}(h_{8,\mathrm{attn\_prem}} - h_{8,\mathrm{attn\_dist}})_{1:2}$$
   - Hypothesis: Best suited when cross-attention routing is entangled between competing entity candidates.

---

## 4. Prospective Selection Policy ($q(g \mid x, h_0)$)

The selection policy $q(g \mid x, h_0)$ operates strictly on pre-intervention observables available at the end of the unperturbed forward pass ($T=0$):
1. **Flow Curvature Ratio:**
   $$r_{\mathrm{flow}} = \frac{\|h_8^{(0)} - h_6^{(0)}\|}{\|h_6^{(0)} - h_4^{(0)}\|}$$
2. **Context-to-Query Attention Entropy:**
   $$H_{\mathrm{attn}} = -\sum_i a_i \log a_i \quad (\text{last-token attention over context tokens})$$
3. **Representation Anisotropy / Residual Energy:**
   $$e_{\mathrm{res}} = \frac{\|h_8^{(0)} - h_8^{(0)}[-1]\|_F}{\|h_8^{(0)}\|_F}$$

### Policy Rule:
- If $H_{\mathrm{attn}}$ is high (diffuse attention across entities) $\longrightarrow$ Select **$G_3$ (Attention Relational)** to resolve head routing.
- If $r_{\mathrm{flow}} \ge 1.0$ (strong inter-layer acceleration) $\longrightarrow$ Select **$G_1$ (Trajectory Flow)** to steer forward evolution.
- Else $\longrightarrow$ Select **$G_2$ (Contextual Perturbation)** to stabilize premise coordinates.

---

## 5. Evaluated Conditions & Benchmark Architecture

1. **Condition 1 (Baseline $M_I$):** Unintervened single pass ($T=1$, $M_I = 0.6000$).
2. **Condition 2 ($G_{\mathrm{contrastive}}$):** Supervised reference baseline ($+14.0$ pp, $p=0.0078$).
3. **Condition 3 (Static $G_1$):** Always use Inter-Layer Trajectory Flow ($1.0$ pass).
4. **Condition 4 (Static $G_2$):** Always use Contextual Perturbation ($1.0$ pass).
5. **Condition 5 (Static $G_3$):** Always use Attention-Derived Relational Subspace ($1.0$ pass).
6. **Condition 6 (Oracle Generator Selection $\pi_{\mathrm{oracle}}$):** Post-hoc selection of the best generator per instance $g \in \{G_1, G_2, G_3\}$ (establishing the theoretical upper bound of the pool).
7. **Condition 7 (Prospective Generator Selection $\pi_{\mathrm{prospective}}$):** Selection of $g^*$ via policy $q(g \mid x, h_0)$ using only $T=0$ internal representations ($1.0$ intervention pass).

---

## 6. Pre-Registered Hypotheses & Falsification Criteria

### Hypothesis 1: Heterogeneous Generator Complementarity ($H_{\mathrm{complement}}$)
$$\text{Oracle Accuracy } M(\pi_{\mathrm{oracle}}) > \max(M(G_1), M(G_2), M(G_3))$$
- **Prediction:** The three generator families rescue distinct, non-overlapping subsets of failure instances, such that the multi-generator pool contains substantially higher headroom than any single generator alone.
- **Falsification Criterion:** If the union of rescues across all three generators equals the rescues of $G_1$ alone, the hypothesis of qualitative generator complementarity is rejected.

### Hypothesis 2: Prospective Selection Superiority ($H_{\mathrm{prospective}}$)
$$M(\pi_{\mathrm{prospective}}) > \max(M(G_1), M(G_2), M(G_3)) \quad \text{under} \quad B_{\mathrm{eval}} = 1.0$$
- **Prediction:** Prospective selection correctly matches instances to their optimal generator family before intervention, achieving higher net accuracy than any single static generator while strictly consuming only $1$ evaluation pass per instance.
- **Falsification Criterion:** If prospective selection achieves accuracy $\le \max(M(G_1), M(G_2), M(G_3))$ or incurs excess corruptions ($c \ge 2$), the hypothesis of prospective generator selection is rejected.

---

## 7. Statistical Protocol
- Pre/post parameter SHA-256 hash verified invariant ($\Delta\theta \equiv 0$).
- 1,000-resample bootstrap 95% confidence intervals.
- Exact Paired McNemar tests vs. $M_I$ and vs. Static $G_1$.
- Output saved to `experiments/runs/EXP039_generator_selection/exp039_generator_selection_results.json`.
