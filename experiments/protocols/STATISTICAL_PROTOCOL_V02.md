# Statistical & Measurement Protocol V0.2

**Protocol ID:** STAT-V0.2  
**Governing Review:** Reviewer V0.2 Sections 3, 4, 8, 9  
**Status:** Pre-Registered & Frozen  
**Date:** 2026-09-11  

---

## 1. Seed Separation

To prevent seed confounding (Reviewer Section 8), every experiment configuration explicitly distinguishes:
- `dataset_seed`: Controls synthetic data generation and train/test splits.
- `candidate_generation_seed`: Controls token slice sampling in generator $\mathcal{G}$.
- `model_sampling_seed`: Controls stochastic perturbation in sampling baselines.
- `experiment_seed`: Master root seed initializing deterministic libraries.

---

## 2. Selection Regret & Pre-Registered Tolerance

Let $M \in [0, 1]$ be downstream accuracy.  
For candidate pool $\{P_1, \dots, P_K\}$ on instance $x_i$:
- $k_{\mathcal{E}} = \arg\min_k \mathcal{E}(P_k, h)$ (Intrinsic Selection)
- $k_{\text{random}} \sim \text{Uniform}(1, K)$ (Random Selection)
- $k_{\text{oracle}} = \arg\max_k M(f_{\theta_0}(x; P_k))$ (Oracle Selection)

### Selection Regret Definitions:
$$\text{Regret}_{\mathcal{E}} = M(P_{k_{\text{oracle}}}) - M(P_{k_{\mathcal{E}}})$$
$$\text{Regret}_{\text{random}} = M(P_{k_{\text{oracle}}}) - M(P_{k_{\text{random}}})$$

### Pre-Registered Falsification Tolerance:
$$\epsilon_{\text{regret}} = 0.02 \quad (2.0\% \text{ accuracy})$$
If $|\text{Regret}_{\mathcal{E}} - \text{Regret}_{\text{random}}| \le \epsilon_{\text{regret}}$, the intrinsic evaluator is formally classified as **providing no meaningful selection signal beyond chance**.

---

## 3. Inferential Statistics & Equivalence Standard

Per Reviewer Section 3:
- A non-significant $p$-value ($p \ge 0.05$) shall **never** be cited as evidence that SCBI equals baseline.
- All comparisons must report:
  1. Mean paired difference: $\Delta M = M_{\text{SCBI}} - M_{\text{baseline}}$
  2. 95% Bootstrap Confidence Interval ($B=1000$ resamples)
  3. Paired Wilcoxon signed-rank test statistic $W$ and two-sided $p$-value
  4. Cliff's $\delta$ effect size.

---

## 4. Best-of-$N$ Baseline Selection Rule

Per Reviewer Section 9, the Best-of-$N$ baseline cannot access ground-truth labels.  
**Rule:** The baseline draws $N=4$ stochastic representations, evaluates internal prediction entropy under the unmodified model, and selects the sample with lowest entropy:
$$k^*_{\text{baseline}} = \arg\min_{i \in \{1,\dots,N\}} \mathcal{H}(\text{logits}(h_i))$$
This ensures parity: both SCBI and the baseline select candidates without test labels.
