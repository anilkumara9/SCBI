# EXP011 Protocol: Bidirectional Counterfactual Consistency Study

**Protocol ID:** `EXP011`  
**Status:** Pre-Registered (Joint Collaboration: Antigravity & ChatGPT)  
**Date:** 2026-09-11  
**Lead Implementer:** [`implementation-agent.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/agents/implementation-agent.md)  
**Independent Reviewer:** [`adversarial-reviewer.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/agents/adversarial-reviewer.md)  
**Governing Rules:** [`00-core-research.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/rules/00-core-research.md), [`03-experiments.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/rules/03-experiments.md)  

---

## 1. Scientific Objective & Research Question

**Primary Research Question:**
$$\boxed{\textbf{Can an unsupervised evaluator identify task-improving candidate representations by testing bidirectional counterfactual consistency (invariance under } x^+ \textbf{ + sensitivity under } x^- \textbf{)?}}$$

EXP001–EXP010 proved that static scalar representation properties fail to identify useful candidate projections. In accordance with Hypothesis `H-002`, EXP011 transitions SCBI from static intrinsic evaluation to **relational counterfactual evaluation**.

---

## 2. Inviolable Procedural Constraints
1. **Strict Data Independence:**
   - Evaluated on genuinely independent held-out instances (`dataset_seed = 888`, `candidate_seed = 666 + i`, $N = 100$).
   - Disjoint from discovery data (seeds 42, 137, 4096) and EXP010 data (seeds 999, 777, 8192).
2. **Frozen Architecture & Model:**
   - Same frozen foundation model ($\Delta\theta = 0$, verified via SHA-256 pre- and post-run parameter checksums).
   - Same candidate generator $\mathcal{G}$ ($K = 4, r = 2$).
3. **Zero Semantic Leakage:**
   - Generic transformations $\mathcal{T}^+$ and $\mathcal{T}^-$ applied uniformly without access to true labels $y$ or ground-truth segment masks ($h_{\text{premise}}$ vs $h_{\text{distractor}}$).

---

## 3. Pre-Registered Counterfactual Views & Evaluators

For each input $x \in \mathbb{R}^{S \times d}$:
- **$x^+$ (Meaning-Preserving View):** Continuous isotropic perturbation $x^+ = x + \epsilon$, where $\epsilon \sim \mathcal{N}(0, 0.05^2 I)$.
- **$x^-$ (Meaning-Changing View):** Generic token corruption replacing 50% randomly chosen sequence tokens with vectors from the standard domain distribution $\mathcal{N}(0, I)$.

For candidate $k$, let:
- $q_k^0 = \text{softmax}(f_{\theta_0}(P_k x))$
- $q_k^+ = \text{softmax}(f_{\theta_0}(P_k x^+))$
- $q_k^- = \text{softmax}(f_{\theta_0}(P_k x^-))$

### Evaluator Formulations (Minimization Convention):
1. **$E_{\text{CF}}$ (Primary Bidirectional Objective):**
   $$E_{\text{CF}}(P_k) = D_{\text{JS}}(q_k^0, q_k^+) - 0.5 \cdot D_{\text{JS}}(q_k^0, q_k^-)$$
   *(Minimizing favors high stability under $x^+$ and high divergence under $x^-$. Pre-registered parameter $\alpha = 0.5$.)*
2. **$E_{\text{pos}}$ (Stability-Only Ablation):**
   $$E_{\text{pos}}(P_k) = D_{\text{JS}}(q_k^0, q_k^+)$$
   *(Tests whether stability alone degenerates into uninformative collapse).*
3. **$E_{\text{neg}}$ (Sensitivity-Only Ablation):**
   $$E_{\text{neg}}(P_k) = -D_{\text{JS}}(q_k^0, q_k^-)$$
   *(Tests whether sensitivity alone selects noisy outliers).*
4. **Random Selection (Null Baseline):**
   $$P^*_{\text{random}} \sim \text{Uniform}(\{P_k\})$$
5. **Oracle Selection (Empirical Ceiling):**
   $$P^*_{\text{oracle}} = \arg\max_k \mathbf{1}[y_k = y_{\text{true}}]$$

---

## 4. Pre-Registered Falsification Criteria
- **Primary Metric:** Instance selection accuracy $M$, paired difference $\Delta = M(E_{\text{CF}}) - M(\text{Random})$, 95% bootstrap CI on $\Delta$, and Wilcoxon signed-rank $p$-value.
- **Oracle Recovery:** $R_E = \frac{M(E_{\text{CF}}) - M(\text{Random})}{M(\text{Oracle}) - M(\text{Random})}$.
- **Falsification Threshold:** If $M(E_{\text{CF}}) \le M(\text{Random})$ or Wilcoxon $p \ge 0.05$, the hypothesis that generic bidirectional counterfactual consistency identifies useful representations is **falsified**.
