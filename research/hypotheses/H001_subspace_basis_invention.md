# Pre-Registered Hypothesis H-001: Instance-Adaptive Subspace Projection under Frozen Backbone

**Hypothesis ID:** H-001  
**Status:** `[HYPOTHESIS]`  
**Lead Agent:** [`theory-agent.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/agents/theory-agent.md)  
**Adversarial Sign-Off:** [`adversarial-reviewer.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/agents/adversarial-reviewer.md)  
**Governing Rule:** [`.agents/rules/00-core-research.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/rules/00-core-research.md)  
**Date Pre-Registered:** 2026-09-11  

---

## 1. Theoretical Motivation & Formulation

Consider a frozen foundation language model $f_{\theta_0}: \mathcal{X} \to \mathcal{Y}$. When processing complex or distractor-heavy prompts $x \in \mathcal{X}$, the intermediate residual activation $h_0 = f_{\theta_0}^{(l)}(x) \in \mathbb{R}^{S \times d}$ contains both task-relevant feature directions and interfering distractor subspaces.

We hypothesize that an inference-time operator that constructs candidate low-rank projection matrices $P_k = I - V_k V_k^\top$ ($k \in \{1,\dots,K\}$) and selects $P^*$ minimizing an unsupervised cycle-consistency objective $\mathcal{E}(P_k, x)$ will improve output task performance without updating any model parameters ($\theta_t = \theta_0, \Delta\theta_t = 0$).

---

## 2. Formal Statistical Hypotheses

Let $M: \mathcal{Y} \times \mathcal{Y} \to \mathbb{R}$ be the pre-registered evaluation metric (Accuracy / Exact Match).  
Let $\Delta M = M(f_{\theta_0}(x; P^*)) - M(f_{\theta_0}(x; \text{baseline}))$.

- **Null Hypothesis ($H_0$):**
  $$\mathbb{E}_{x \sim \mathcal{D}}[\Delta M] \le 0$$
  relative to a compute-matched baseline given identical evaluation passes ($K$).

- **Alternative Hypothesis ($H_1$):**
  $$\mathbb{E}_{x \sim \mathcal{D}}[\Delta M] > \epsilon \quad (\epsilon > 0)$$
  with statistical significance $p < 0.01$ under a two-sided Wilcoxon signed-rank test across 5 random seeds.

---

## 3. Scope & Boundary Assumptions

1. `[ASSUMPTION 1]`: The foundation backbone remains strictly frozen ($\Delta\theta = 0$, parameter hash unchanged).
2. `[ASSUMPTION 2]`: Zero test label leakage. The candidate evaluation function $\mathcal{E}$ has no access to target $y$.
3. `[ASSUMPTION 3]`: The candidate basis $P^*$ and state $z_t$ are transient and purged post-inference.

---

## 4. Explicit Falsification Criteria (Pre-Registered)

The hypothesis $H_1$ shall be considered **falsified** if any of the following occur:
1. **Selection Equivalence with Random:** Ablation 1 (Random Selection from $\{P_k\}$) yields performance statistically indistinguishable from or superior to $\mathcal{E}$-guided selection ($p \ge 0.05$).
2. **Compute Failure:** A compute-matched Best-of-$K$ sampling baseline matches or outperforms SCBI on accuracy while having equal or lower latency.
3. **Weight Violation:** The model parameter hash changes during inference.
