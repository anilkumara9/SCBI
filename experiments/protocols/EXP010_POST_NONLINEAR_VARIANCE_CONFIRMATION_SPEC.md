# EXP010 Protocol: Confirmatory Post-Nonlinear Variance Selection Study

**Protocol ID:** `EXP010`  
**Status:** Pre-Registered (Joint Collaboration: Antigravity & ChatGPT)  
**Date:** 2026-09-11  
**Lead Implementer:** [`implementation-agent.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/agents/implementation-agent.md)  
**Independent Reviewer:** [`adversarial-reviewer.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/agents/adversarial-reviewer.md)  
**Governing Rules:** [`00-core-research.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/rules/00-core-research.md), [`03-experiments.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/rules/03-experiments.md)  

---

## 1. Scientific Objective & Epistemological Status

**Status:** Level 2 Confirmatory Test (Pre-Registered after EXP009 Discovery).  
**Primary Research Question:**
$$\boxed{\textbf{Does post-nonlinear representation variance at Layer } l+1 \textbf{ enable an unsupervised evaluator to select useful candidates on unseen, independent instances?}}$$

In EXP009, exploratory analysis identified that post-GELU representation variance at Layer $l+1$ separated correct from incorrect candidates within instances ($\bar{R} = 0.6452, p = 0.0192$). Because EXP009 tested multiple features across multiple layers, this finding represents a **discovery hypothesis**.

EXP010 is the strictly pre-registered **confirmatory experiment** on genuinely independent instances ($D_{\text{discovery}} \cap D_{\text{EXP010}} = \emptyset$) to evaluate whether an evaluator based on this signal ($E_{\text{var}}$) genuinely breaks the selection bottleneck.

---

## 2. Inviolable Procedural Constraints
1. **Strict Data Independence:**
   - Generated using novel dataset seed (`dataset_seed = 999`, $N=100$) and novel candidate seeds (`candidate_seed = 777 + i`).
   - Completely disjoint from EXP001–EXP009 discovery data.
2. **Frozen Architecture & Generator:**
   - Same benchmark distribution (`distractor_rank = 2`, `distractor_scale = 1.5`, $d=32$, $C=4$).
   - Same frozen backbone model ($\Delta\theta = 0$, SHA-256 parameter hashes verified before and after).
   - Same candidate generator $\mathcal{G}$ ($K=4, r=2$).
   - Zero parameter tuning, zero threshold adjustments.

---

## 3. Pre-Registered Evaluator Formulations

We test the complete selection ladder across the exact same frozen candidate pool:

1. **Random Selection (Null Reference):**
   $$P^*_{\text{random}} \sim \text{Uniform}(\{P_1, \dots, P_K\})$$
2. **V0.1 (Original Intrinsic Energy Evaluator):**
   $$E_{\text{V0.1}}(P_k) = \frac{\|h_0 - P_k h_0\|_F}{\|h_0\|_F} + 0.1 \mathcal{H}(\sigma(P_k h_0))$$
3. **$E_{\text{var}}$ (Primary Confirmatory Evaluator):**
   $$E_{\text{var}}(P_k) = -\text{Var}\left(f^{l \to l+1}_{\theta_0}(P_k h_0)\right)$$
   *(Minimizing $E_{\text{var}}$ selects the candidate maximizing post-nonlinear feature variance.)*
4. **$E_{\text{norm}}$ (Activation Magnitude Ablation):**
   $$E_{\text{norm}}(P_k) = -\|f^{l \to l+1}_{\theta_0}(P_k h_0)\|_2$$
   *(Tests whether the effect is driven by raw activation norm rather than variance.)*
5. **$E_{\text{var+norm}}$ (Combined Ablation):**
   $$E_{\text{var+norm}}(P_k) = -(\text{Var}(z_{l+1}) + 0.1 \|z_{l+1}\|_2)$$
6. **Oracle Selection (Empirical Candidate Pool Ceiling):**
   $$P^*_{\text{oracle}} = \arg\max_k \mathbf{1}[y_k = y_{\text{true}}]$$

---

## 4. Pre-Registered Hypotheses & Falsification Criteria

### Primary Hypothesis $H_{1,\text{EXP010}}$:
$$H_0: M(E_{\text{var}}) \le M(\text{Random}) \quad \text{versus} \quad H_1: M(E_{\text{var}}) > M(\text{Random})$$
- **Primary Metric:** Instance-level selection accuracy $M = \frac{1}{N}\sum_{i=1}^N \mathbf{1}[\hat{y}_{i, P^*} = y_i]$.
- **Paired Selection Gain:** $\Delta = M(E_{\text{var}}) - M(\text{Random})$ with 95% bootstrap CI and Wilcoxon signed-rank test.
- **Oracle Recovery Ratio:**
  $$R_E = \frac{M(E) - M(\text{Random})}{M(\text{Oracle}) - M(\text{Random})}$$
- **Falsification Threshold:**
  If $M(E_{\text{var}}) - M(\text{Random}) \le 0$ or Wilcoxon $p \ge 0.05$, the hypothesis that post-nonlinear variance provides an exploitable selection evaluator is **falsified**.

### Anti-Collapse Diagnostics:
For all selected candidates, record representation effective rank, variance, norm, and sparsity to verify that $E_{\text{var}}$ does not select degenerate or blown-up activations.
