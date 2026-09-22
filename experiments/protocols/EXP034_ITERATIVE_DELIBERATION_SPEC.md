# EXP034: Multi-Pass Iterative Latent Deliberation Specification

## 1. Executive Summary & Epistemological Status
- **Experiment ID:** `EXP034`
- **Date:** 2026-09-11
- **Governing Law:** All 14 Inviolable Agent Laws in [`AGENTS.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/AGENTS.md).
- **Epistemological Status:** `[HYPOTHESIS]` Pre-registered confirmatory benchmark evaluating whether multi-pass iterative recurrence in latent space autonomously amplifies relational contrast to match supervised single-pass headroom without human labels, under strict compute-matched accounting.
- **Evaluated Architecture:** `EleutherAI/pythia-160m` (12 layers, $d_{\mathrm{model}}=768$, Revision `e72e396263595503028d71243171317d7ae65463`).
- **Benchmark:** `BENCH-002-NL` ($N = 50$ confirmatory instances, Seed 84).
- **Frozen Backbone Guarantee:** Parameter SHA-256 hash verified invariant before and after inference: `54c88fa4897785f2bd94b32d26de1f73f1052bcc42124d563d0cda96940de936` ($\Delta\theta \equiv 0$).

---

## 2. Theoretical Motivation & The Deliberation Paradigm

EXP032 refuted static covariance ($\Sigma(h) \to \text{PCA} \not\to V^*$). EXP033 demonstrated that internal relational differences (inter-layer trajectory $h_8 - h_6$ and contextual counterfactuals) achieve positive target log-probability shifts ($\Delta\log p > 0$) with zero corruption ($c=0$), but single-pass relational steering reached only $+6.0$ pp ($p=0.1250$), falling short of supervised contrast ($+14.0$ pp, $p=0.0078$).

This confirms the 3-level hierarchy:
1. **Level 1 (Static Geometry):** Fails / corrupts ($\Delta\log p < 0$).
2. **Level 2 (Relational Perturbations):** Correct directional axis ($\Delta\log p > 0$, $c=0$), but single-pass projection is limited in amplitude.
3. **Level 3 (Dynamic Computation Geometry):** Iterative deliberation across recurrent passes allows the model to refine its internal trajectory dynamically.

$$\boxed{\textbf{Central Question: Can Iterative Deliberation Bridge the Gap to Supervised Headroom Without Labels?}}$$

---

## 3. Deliberation Mechanics & FLOP Accounting

Let $h^{(0)}$ denote the unintervened hidden state representation. At each deliberation step $t \in \{1, \dots, T\}$:
1. Compute the relational trajectory acceleration:
   $$v^{(t)} = h^{(t-1)}_8 - h^{(t-1)}_6$$
2. Extract the rank-2 orthonormal basis $V^{(t)} = \operatorname{span}(v^{(t)}_1, v^{(t)}_2)$ via SVD.
3. Apply the linear steering operator at Layer 8:
   $$h^{(t)}_8 = h^{(t-1)}_8 - \alpha P_{V^{(t)}} h^{(t-1)}_8 \quad (\alpha = 0.25)$$
4. Propagate the updated residual state through Layers 9–12 to compute revised logits and track convergence:
   $$\delta^{(t)} = \frac{\|h^{(t)}_8 - h^{(t-1)}_8\|_2}{\|h^{(t-1)}_8\|_2}$$

### Evaluated Conditions (Compute-Matched Protocol):
1. **Condition 1 ($M_I$):** Unintervened Baseline (1 pass, $T=1$).
2. **Condition 2 ($G_{\mathrm{contrastive}}$):** Supervised Single-Pass Reference (1 pass, $T=1$).
3. **Condition 3 ($\text{SCBI-Delib}(T=1)$):** Single-Pass Relational Trajectory ($T=1$).
4. **Condition 4 ($\text{SCBI-Delib}(T=2)$):** 2-Step Iterative Deliberation ($T=2$).
5. **Condition 5 ($\text{SCBI-Delib}(T=3)$):** 3-Step Iterative Deliberation ($T=3$).
6. **Condition 6 ($\text{Baseline-Bo3}$):** Compute-Matched Repeated Sampling (Best-of-3, $T=3$ passes).
7. **Condition 7 ($\text{Random-Delib}(T=3)$):** 3-Step Iteration with Random Grassmannian Subspaces (Null Control, $T=3$).

---

## 4. Pre-Registered Hypotheses & Falsification Criteria

### Hypothesis 1: Deliberative Amplification ($H_{\mathrm{delib}}$)
$$\Delta M(\text{SCBI-Delib}(T \in \{2, 3\})) \ge +10.0\text{ pp} \quad \text{AND} \quad p < 0.05 \text{ vs. } M_I$$
- **Predicted Outcome:** Multi-step iterative deliberation significantly amplifies the $+6.0$ pp single-pass gain to $\ge +10.0$ pp, outperforming Compute-Matched Best-of-3 sampling and closing at least 70% of the gap to supervised contrast without human labels.
- **Falsification Criterion:** If $\text{SCBI-Delib}(T \ge 2)$ yields $\Delta M \le +6.0$ pp or causes corruption ($c > 0$), the hypothesis that iterative recurrence in latent space autonomously amplifies relational contrast is rejected.

### Hypothesis 2: Trajectory Stability ($H_{\mathrm{stability}}$)
$$\delta^{(t)} < 0.25 \quad \forall t \in \{1, 2, 3\}$$
- **Predicted Outcome:** Latent updates converge smoothly without causing representation explosion or degenerative collapse.

---

## 5. Statistical Protocol
- Parameter SHA-256 hash verified identical pre- and post-run ($\Delta\theta \equiv 0$).
- 1,000-resample bootstrap 95% confidence intervals for all conditions.
- Exact Paired McNemar tests vs. $M_I$, vs. Compute-Matched Bo3, and vs. Random Deliberation.
- Output saved to `experiments/runs/EXP034_deliberation/exp034_deliberation_results.json`.
