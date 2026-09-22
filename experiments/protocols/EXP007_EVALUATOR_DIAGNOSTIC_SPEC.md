# EXP007: Evaluator Diagnostic Matrix Specification

**Experiment ID:** EXP007  
**Status:** Pre-Registered Competing Hypotheses  
**Governing Rule:** [`.agents/rules/00-core-research.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/rules/00-core-research.md), [`.agents/rules/03-experiments.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/rules/03-experiments.md)  
**Collaborators:** Antigravity (Implementation Lead) & ChatGPT (Independent Reviewer)  
**Date:** 2026-09-11  

---

## 1. Central Research Question

$$\boxed{\text{Can an information-valid, label-free evaluator recover the useful candidate without oracle access?}}$$

Candidate Pool Ceiling (established in EXP005): **50.0% Accuracy** (vs. 28.0% baseline).

---

## 2. Evaluator Suite & Information Boundaries

| Evaluator ID | Name | Mathematical Formulation | Information Scope | Scientific Status |
| :--- | :--- | :--- | :---: | :--- |
| **V0.1** | Reconstruction + Entropy | $\|h - Ph\|_F / \|h\|_F + 0.1 \mathcal{H}(Ph)$ | $h_0$ only | Reference V0.1 heuristic |
| **Random** | Null Selection | $k \sim \text{Uniform}(1, K)$ | None | Null control baseline |
| **E1-oracle** | Privileged Segment Mask | $\|h_p - P h_p\| / \|h_p\| - 0.5 \|h_d - P h_d\| / \|h_d\|$ | $h_{\text{premise}}, h_{\text{distractor}}$ | **PRIVILEGED STRUCTURAL CEILING** |
| **E1-unsupervised** | Variance-Segmented Mask | Splits tokens by token-level variance $\sigma_s^2$: top 50% vs bottom 50% | $h_0$ only (no labels) | Unsupervised heuristic |
| **E2** | Query-Context Alignment | $-\cos(P \bar{h}_{\text{query}}, P \bar{h}_{\text{context}})$ | $h_0$ query/context positions | Geometric heuristic |
| **E3** | Downstream Logit Margin | $- (\text{logit}_{\text{top1}} - \text{logit}_{\text{top2}})$ | $f_{\theta_0}^{(>l)}(Ph)$ | **CONFIDENCE-BASED SELECTION** |
| **E4** | Candidate Self-Consistency | $\frac{1}{J(J-1)} \sum_{a \ne b} \text{JS}(p(P h^{(a)}) \parallel p(P h^{(b)}))$ | Independent noise views $h^{(j)}$ | **CANDIDATE SELF-CONSISTENCY** |
| **Oracle** | Label-Supervised Ceiling | $k^* = \arg\max_k \mathbf{1}[\hat{y}(P_k) == y]$ | Ground-truth $y$ | Empirical Ceiling |

---

## 3. Pre-Registered Hypotheses & Success Criteria

### Candidate-Level Predictiveness:
For each evaluator $E$, compute Spearman rank correlation across all $N \times K = 400$ candidate evaluations:
$$\rho = \text{Spearman}(E_k, \mathbf{1}[\text{candidate correct}])$$
- Null Hypothesis: $H_0: \rho \le 0$.
- Alternative Hypothesis: $H_1: \rho > 0$.

### Instance-Level Selection Gain:
$$\Delta = M(E) - M(\text{Random})$$
Report:
- Mean accuracy $M(E)$
- Selection Regret: $M(\text{Oracle}) - M(E)$
- 95% Bootstrap Confidence Interval on $\Delta$ ($B=1000$)
- Wilcoxon signed-rank test $p$-value.
