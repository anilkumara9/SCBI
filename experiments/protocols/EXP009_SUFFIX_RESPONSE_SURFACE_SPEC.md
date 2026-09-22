# EXP009 Protocol: Suffix Response Surface & Information Localization Study

**Protocol ID:** `EXP009`  
**Status:** Pre-Registered (Joint Collaboration: Antigravity & ChatGPT)  
**Date:** 2026-09-11  
**Lead Implementer:** [`implementation-agent.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/agents/implementation-agent.md)  
**Independent Reviewer:** [`adversarial-reviewer.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/agents/adversarial-reviewer.md)  
**Governing Rules:** [`00-core-research.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/rules/00-core-research.md), [`03-experiments.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/rules/03-experiments.md)  

---

## 1. Scientific Objective & Research Question

**Primary Research Question:**
$$\boxed{\textbf{At what stage of the frozen computation does candidate usefulness become identifiable?}}$$

Following EXP008, we proved that pre-selection single-layer geometric statistics at intermediate layer $l$ fail to identify candidate usefulness. However, true candidate correctness is realized after the non-linear readout suffix $f^{>l}_{\theta_0}$.

The goal of EXP009 is **not** to jump to another heuristic evaluator $E_5$, but to execute a pre-registered diagnostic mapping the response surface of the frozen suffix and localizing whether candidate usefulness becomes identifiable across computational stages.

---

## 2. Pre-Registered Hypotheses

### Hypothesis H9 (Suffix Identifiability Hypothesis)
- **Null Hypothesis ($H_{0,\text{suffix}}$):**  
  Within discriminatory instances ($N_{\text{disc}} = 35$), label-free output distribution statistics $Z_{ik} = \psi(f^{>l}_{\theta_0}(P_{ik} h_0))$ possess no statistically significant discriminative power between correct and incorrect candidates ($\bar{R} = 0.50$, cluster-bootstrap 95% CI spans 0.50).
- **Alternative Hypothesis ($H_{1,\text{suffix}}$):**  
  At least one label-free output distribution statistic $Z$ (e.g. candidate-to-ensemble consensus divergence, output curvature, predictive entropy) distinguishes correct from incorrect candidates with $\bar{R} > 0.50$ (within-instance permutation $p < 0.05$).

### Hypothesis H10 (Layer-wise Localization Hypothesis)
- Intervening at intermediate layers $\{l_{\text{prefix}}, l_{\text{suffix,1}}, l_{\text{suffix,2}}\}$ reveals a monotonic increase in candidate identifiability as representations approach the linear readout head.

---

## 3. Pre-Registered Diagnostic Metrics

### A. Suffix Response Surface Features (Label-Free / Output-Space)
For candidate $k$, compute probability distribution $q_k = \text{softmax}(f^{>l}_{\theta_0}(P_k h_0)) \in \Delta^C$:
1. **Output Predictive Entropy:** $H(q_k) = -\sum_{c=1}^C q_{kc} \ln(q_{kc} + 1e-9)$
2. **Top-1 / Top-2 Margin:** $\Delta_{\text{margin}}(q_k) = q_{k,(1)} - q_{k,(2)}$
3. **Logit Norm:** $\|z_k\|_2$ where $z_k = f^{>l}_{\theta_0}(P_k h_0)$
4. **Logit Variance:** $\text{Var}(z_k)$
5. **Candidate-to-Ensemble Consensus Divergence:**
   $$D_{\text{JS}}(q_k, \bar{q}), \quad \bar{q} = \frac{1}{K}\sum_{j=1}^K q_j$$
6. **Mean Pairwise Output Divergence:**
   $$\bar{D}_{\text{pair}}(q_k) = \frac{1}{K-1}\sum_{j \ne k} D_{\text{JS}}(q_k, q_j)$$
7. **View-Consistency (Output Curvature):**
   $$E_{\text{view}}(P_k) = \frac{1}{J}\sum_{j=1}^J D_{\text{JS}}(q_k, q_{k}^{(j)}), \quad q_k^{(j)} = \text{softmax}(f^{>l}(P_k (h_0 + \epsilon_j))), \quad \epsilon_j \sim \mathcal{N}(0, 0.05^2 I)$$

### B. Diagnostic Information Classifier Test (Cluster-Cross-Validated)
Train a simple ridge logistic regression with strict **leave-one-instance-out (LOIO) cross-validation** on:
1. Intermediate features $X$ only ($6$ features)
2. Suffix output features $Z$ only ($7$ features)
3. Combined features $(X, Z)$ ($13$ features)
*Purpose:* Strictly as a diagnostic of empirical mutual information $I(Y; X, Z) > 0$, NOT as an SCBI evaluator.

---

## 4. Statistical Rigor Protocol
- Primary metric: Mean per-instance ranking accuracy $\bar{R} = \frac{1}{35}\sum_{i=1}^{35} R_i$.
- Uncertainty: Cluster-bootstrap over the 35 discriminatory instances (10,000 replicates).
- Null hypothesis significance: Exact within-instance permutation test (preserving candidate counts per instance).
- Immutability guard: Model parameters and buffers verified with SHA-256 before and after execution ($\Delta\theta = 0$).
