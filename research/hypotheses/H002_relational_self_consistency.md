# Pre-Registered Hypothesis H-002: Relational Self-Consistency under Counterfactual Transformations

**Hypothesis ID:** `H-002` (formerly H-C)  
**Status:** `[HYPOTHESIS]`  
**Lead Agent:** [`theory-agent.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/agents/theory-agent.md)  
**Adversarial Sign-Off:** [`adversarial-reviewer.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/agents/adversarial-reviewer.md)  
**Governing Rule:** [`.agents/rules/00-core-research.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/rules/00-core-research.md)  
**Date Pre-Registered:** 2026-09-11  

---

## 1. Theoretical Decomposition of the SCBI Problem

Following the empirical findings of EXP001–EXP010, the core SCBI research question is formally decomposed into three independent hypotheses:

1. **$H_A$ — Candidate Generation Hypothesis:**  
   $$\exists P \in \mathcal{G}(x): \quad \text{Perf}(P) > \text{Perf}(I)$$
   *Empirical Status:* **CONFIRMED on BENCH-001.** Oracle selection elevates task accuracy from $24.0\% - 28.0\%$ to $50.0\% - 55.0\%$ ($p < 0.0001$).
2. **$H_B$ — Intrinsic Scalar Evaluation Hypothesis:**  
   $$\exists \phi(P, h) \in \mathbb{R}: \quad \phi \text{ predicts candidate usefulness from a single static representation pass}.$$
   *Empirical Status:* **FALSIFIED across 9 evaluated families.** (Static energy, segment reconstruction, cosine alignment, logit confidence, perturbation stability, intermediate linear statistics, output-space distribution metrics, and post-nonlinear feature variance all fail to reliably identify the useful candidate without labels).
3. **$H_C$ — Relational / Counterfactual Self-Consistency Hypothesis:**  
   $$\exists E_{\text{rel}}(P; \mathcal{V}(x)): \quad E_{\text{rel}} \text{ predicts candidate usefulness without labels by measuring relational inference evidence}.$$
   Specifically, candidate usefulness is not an intrinsic scalar property of $P$, but a **relational property**: a truth-preserving representation must remain invariant under semantic-preserving transformations ($x^+$) while remaining sensitive to semantic-changing counterfactuals ($x^-$).

---

## 2. Formal Specification of Hypothesis H-002

Let $x$ be an unlabeled input sequence. Let $\mathcal{V}(x) = (x^+, x^-)$ be two pre-registered, label-free transformations:
- $x^+ = \mathcal{T}^+(x)$: A generic meaning-preserving transformation (e.g., isotropic continuous jitter $x + \epsilon$).
- $x^- = \mathcal{T}^-(x)$: A generic meaning-changing transformation (e.g., token replacement from the domain distribution).

For each candidate $P_k \in \mathcal{G}(x)$, let $q_k^0 = f_{\theta_0}(P_k x)$, $q_k^+ = f_{\theta_0}(P_k x^+)$, and $q_k^- = f_{\theta_0}(P_k x^-)$ be the downstream predictive distributions.

Define the **Bidirectional Counterfactual Consistency Objective**:
$$E_{\text{CF}}(P_k) = D_{\text{JS}}(q_k^0, q_k^+) - \alpha D_{\text{JS}}(q_k^0, q_k^-)$$

- **Null Hypothesis ($H_0$):**  
  $$M(E_{\text{CF}}) \le M(\text{Random})$$
  Selecting candidates by minimizing $E_{\text{CF}}$ provides no statistically significant accuracy gain over random candidate selection on independent held-out data ($p \ge 0.05$).
- **Alternative Hypothesis ($H_1$):**  
  $$M(E_{\text{CF}}) > M(\text{Random})$$
  Selecting candidates by minimizing $E_{\text{CF}}$ recovers a statistically significant portion of the Oracle ceiling ($R_E > 0$, Wilcoxon $p < 0.05$).

---

## 3. Boundary Conditions & Non-Leakage Invariant
1. **Model Frozen:** $\theta_t = \theta_0, \Delta\theta_t = 0$.
2. **Zero Semantic Leakage:** $\mathcal{T}^+$ and $\mathcal{T}^-$ must be defined generically over token sequences without privileged access to ground-truth premise or distractor token masks.
3. **Pre-Registered Hyperparameters:** Divergence metric $D_{\text{JS}}$ and scaling parameter $\alpha$ must be frozen prior to inspecting experimental results.
