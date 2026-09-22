# EXP008 Protocol: Candidate Mechanism Decomposition & Identifiability Study

**Protocol ID:** `EXP008`  
**Status:** Pre-Registered (Joint Collaboration: Antigravity & ChatGPT)  
**Date:** 2026-09-11  
**Lead Implementer:** [`implementation-agent.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/agents/implementation-agent.md)  
**Independent Reviewer:** [`adversarial-reviewer.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/agents/adversarial-reviewer.md)  
**Governing Rules:** [`00-core-research.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/rules/00-core-research.md), [`03-experiments.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/rules/03-experiments.md)  

---

## 1. Scientific Objective & Research Question

**Primary Research Question:**
$$\boxed{\textbf{Is candidate usefulness identifiable from the pre-selection representation information available to an SCBI evaluator?}}$$

Following the results of EXP001–EXP007, we know that under `BENCH-001`, the candidate pool contains task-improving projections (Oracle = 50.0% vs. Baseline = 28.0%, Random = 34.0%), but all 6 evaluated intrinsic/unsupervised evaluators yielded recovery ratios $R_E \approx 0$ and pairwise ranking accuracies $R \approx 0.50$.

Before proposing an $E_5$ evaluator or migrating to an LLM, we must determine whether successful candidates possess any measurable, information-valid statistical or geometric signature that separates them from unsuccessful candidates within the same instance.

---

## 2. Pre-Registered Hypotheses

### Hypothesis H8 (Candidate Identifiability Hypothesis)
- **Null Hypothesis ($H_0$):**  
  Conditioned on discriminatory instances ($N_{\text{disc}} = 35$), there is no statistically significant difference in any pre-selection, label-free representation statistic between correct and incorrect candidates. Formally, for all pre-selection features $X_{ik} = \phi(h_{i0}, P_{ik})$:
  $$P(Y_{ik} = 1 \mid X_{ik}) = P(Y_{ik} = 1) \quad \text{within instance}, \quad R_X = P(X_{\text{correct}} > X_{\text{incorrect}}) = 0.50.$$
- **Alternative Hypothesis ($H_1$):**  
  At least one pre-selection, label-free representation statistic $X$ distinguishes correct from incorrect candidates within instances with pairwise ranking accuracy $R_X > 0.50$ (permutation $p < 0.05$).

---

## 3. Feature Extraction Protocol (Per Candidate $k \in \{1, 2, 3, 4\}$ per Instance $i$)

### A. Pre-Selection Representation Statistics (Information-Valid / Unsupervised)
1. **Retained Energy Ratio:** $\rho_{\text{retain}} = \frac{\|P_k h_0\|_F}{\|h_0\|_F}$
2. **Removed Energy Ratio:** $\rho_{\text{remove}} = \frac{\|(I - P_k) h_0\|_F}{\|h_0\|_F}$
3. **Effective Rank:** $r_{\text{eff}} = \exp\left(-\sum \tilde{\sigma}_j \ln \tilde{\sigma}_j\right)$, where $\tilde{\sigma}_j$ are normalized singular values of $P_k h_0$.
4. **Representation Variance:** $\text{Var}(P_k h_0) = \frac{1}{d} \sum_{c=1}^d \text{Var}_s((P_k h_0)_{s, c})$
5. **Token Cosine Uniformity:** Mean pairwise cosine similarity across sequence tokens in $P_k h_0$.
6. **Subspace Distance to Centroid:** $D(P_k, \bar{P})$, distance of candidate projector to pool mean projector.

### B. Privileged Diagnostic Features (Causal Verification / Ground Truth Required)
*These features use ground-truth benchmark information and are strictly forbidden for selection, but are essential to decompose the physical mechanism:*
1. **Distractor Energy Removed:** $\rho_{\text{remove, dist}} = \frac{\|(I - P_k) h_{\text{distractor}}\|_F}{\|h_{\text{distractor}}\|_F}$
2. **Premise Energy Preserved:** $\rho_{\text{retain, prem}} = \frac{\|P_k h_{\text{premise}}\|_F}{\|h_{\text{premise}}\|_F}$
3. **Signal-to-Distractor Ratio (SDR):** $\text{SDR} = \frac{\|P_k h_{\text{premise}}\|_F}{\|P_k h_{\text{distractor}}\|_F + 1e-8}$
4. **Prototype Alignment Margin:** Cosine similarity to true class prototype minus max cosine similarity to incorrect class prototypes in representation space.
5. **Downstream Correct Logit:** $\text{logit}_{y_{\text{true}}}(f^{>l}(P_k h_0))$

---

## 4. Evaluation & Statistical Falsification Criteria

For each feature $f \in \mathcal{F}$:
1. **Within-Instance Pairwise Ranking Accuracy:**
   $$R_f = \frac{1}{|\mathcal{P}|} \sum_{(c, inc) \in \mathcal{P}} \mathbf{1}[f(c) > f(inc)] + 0.5 \cdot \mathbf{1}[f(c) = f(inc)]$$
   evaluated across all 115 pairwise comparisons on the 35 discriminatory instances.
2. **Permutation Significance Test:**
   $B = 2,000$ permutations of candidate correctness labels within each discriminatory instance.
   Two-sided $p$-value tested against the null $R_f = 0.50$.
3. **Within-Instance Effect Size (Cohen's $d_z$):**
   $$d_z = \frac{\bar{D}_f}{s_{D_f}}, \quad D_f = f(\text{correct}) - f(\text{incorrect})$$
4. **Candidate Geometry Audit:**
   Compare mean pairwise distance $D(P_{\text{correct}}, P_{\text{correct}})$ vs. $D(P_{\text{correct}}, P_{\text{incorrect}})$ to test whether correct candidates form a geometrically localized cluster.

---

## 5. Invariant Guards
- Frozen backbone: $\theta_t = \theta_0, \Delta\theta_t = 0$.
- Checksums verified: Pre- and post-run parameter and buffer SHA-256 hashes must match.
