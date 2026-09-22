# EXP012 Protocol: Hierarchical Support-Set Relational Validation Study

**Protocol ID:** `EXP012`  
**Status:** Pre-Registered (Joint Collaboration: Antigravity & ChatGPT)  
**Date:** 2026-09-11  
**Lead Implementer:** [`implementation-agent.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/agents/implementation-agent.md)  
**Independent Reviewer:** [`adversarial-reviewer.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/agents/adversarial-reviewer.md)  
**Governing Rules:** [`00-core-research.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/rules/00-core-research.md), [`03-experiments.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/rules/03-experiments.md)  

---

## 1. Scientific Objective & Research Question

**Primary Research Question:**
$$\boxed{\textbf{Does evaluating candidate representations against an unlabeled multi-instance support set provide the relational evidence required to identify useful candidates without labels?}}$$

EXP001–EXP010 established that static scalar representation properties fail to identify useful candidate projections. EXP011 demonstrated that single-instance counterfactual consistency produced a positive directional signal ($R_E = +23.1\%$), but suffered from weak measurement channels in the synthetic model ($D_{\text{JS}} < 0.01$).

EXP012 tests the next logical hierarchical step: evaluating candidate representations using **Relational Support-Set Evidence** $E_{\text{support}}(P; \mathcal{V}(x_i), S_i)$, testing invariance under local perturbation alongside contrastive discrimination across an unlabeled support set $S_i$.

---

## 2. Inviolable Procedural Constraints
1. **Strict Data Independence:**
   - Evaluated on genuinely independent held-out instances (`dataset_seed = 555`, `candidate_seed = 333 + i`, $N = 100$).
   - Completely disjoint from discovery data (seeds 42, 137, 4096), EXP010 (seeds 999, 777), and EXP011 (seeds 888, 666).
2. **Frozen Architecture & Model:**
   - Same frozen foundation model ($\Delta\theta = 0$, verified via SHA-256 pre- and post-run parameter checksums).
   - Same candidate generator $\mathcal{G}$ ($K = 4, r = 2$).
3. **No Cross-Instance Projection Transfer:**
   - The candidate projector $P_{ik}$ remains strictly tied to target instance $x_i$. It is evaluated against the support set $S_i$ by measuring contrastive divergence from the baseline outputs of support instances $q_{\text{base}}(s_j)$.

---

## 3. Pre-Registered Hierarchical Ladder

We evaluate four hierarchical levels of candidate selection across the exact same frozen pool:

1. **Level 0 (Null Reference):** Random Selection:
   $$P^*_{\text{random}} \sim \text{Uniform}(\{P_{ik}\})$$
2. **Level 1 (Single-Instance Intrinsic):** $E_{\text{single}}$ (V0.1 Energy Reconstruction):
   $$E_{\text{single}}(P_{ik}) = \frac{\|h_0 - P_{ik} h_0\|_F}{\|h_0\|_F} + 0.1 \mathcal{H}(\sigma(P_{ik} h_0))$$
3. **Level 2 (Single-Instance Counterfactual):** $E_{\text{CF}}$ (Bidirectional Counterfactual from EXP011):
   $$E_{\text{CF}}(P_{ik}) = D_{\text{JS}}(q_k(x_i), q_k(x_i^+)) - 0.5 \cdot D_{\text{JS}}(q_k(x_i), q_k(x_i^-))$$
4. **Level 3 (Multi-Instance Relational):** $E_{\text{support}}$ (Support-Set Relational Consistency):
   $$E_{\text{support}}(P_{ik}) = D_{\text{JS}}(q_k(x_i), q_k(x_i^+)) - \alpha \cdot \frac{1}{m} \sum_{j=1}^m D_{\text{JS}}(q_k(x_i), q_{\text{base}}(s_j))$$
   *(Pre-registered parameters: $\alpha = 0.5$, support size $m = 4$.)*
5. **Upper Bound (Empirical Ceiling):** Oracle Selection:
   $$P^*_{\text{oracle}} = \arg\max_k \mathbf{1}[y_k = y_{\text{true}}]$$

---

## 4. Pre-Registered Hypotheses & Falsification Criteria
- **Primary Hypothesis ($H_{1,\text{EXP012}}$):**  
  $$M(E_{\text{support}}) > M(\text{Random})$$
  with $p < 0.05$ under a paired Wilcoxon signed-rank test on independent data.
- **Oracle Recovery Ratio:**
  $$R_E = \frac{M(E_{\text{support}}) - M(\text{Random})}{M(\text{Oracle}) - M(\text{Random})}$$
- **Falsification Threshold:** If $M(E_{\text{support}}) \le M(\text{Random})$ or Wilcoxon $p \ge 0.05$, the hypothesis that support-set relational consistency recovers the candidate ceiling is **falsified**.
