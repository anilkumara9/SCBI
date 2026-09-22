---
name: statistical-analysis
description: Rigorous methodology for evaluating experimental data, calculating effect sizes, computing bootstrap confidence intervals, conducting non-parametric significance testing, and categorizing failure distributions.
---

# Statistical Analysis Skill

This skill governs the statistical aggregation, hypothesis verification, significance testing, and failure mode analysis for empirical evaluations of **Self-Consistent Basis Invention (SCBI)**.

**Foundational Documents:**
- [`documentation/researchidea.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/documentation/researchidea.md) §8 (Empirical evidence & statistical analysis)
- [`documentation/theory.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/documentation/theory.md) §3 (Operationalization of $\Delta M$)
- **Governing Rule:** [`.agents/rules/03-experiments.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/rules/03-experiments.md)

---

## When to Use This Skill

Activate this skill whenever:
- Aggregating raw experimental runs across multiple random seeds.
- Testing whether performance improvements $\Delta M$ are statistically significant.
- Authoring experimental results tables, figures, or confidence bounds.
- Dissecting failure modes (scenarios where SCBI degraded output quality).

---

## Statistical Standards for SCBI

### 1. Multi-Seed Replication
- Every experimental number reported in a paper or report must be derived from at least **5 independent random seeds** ($S \ge 5$).
- Point estimates without dispersion metrics are strictly unacceptable. Always report:
  $$\mu \pm \sigma \quad [\text{95\% CI}_{\text{lower}}, \text{95\% CI}_{\text{upper}}]$$

### 2. Bootstrap Confidence Intervals (95% CI)
- Avoid assuming normal error distributions for benchmark accuracy.
- Use 1,000 bootstrap resamples (BCa or percentile bootstrap) on instance-level performance:
  ```python
  import numpy as np
  def bootstrap_ci(diffs: np.ndarray, n_boot: int = 1000, ci: float = 0.95) -> tuple[float, float]:
      boot_means = [np.mean(np.random.choice(diffs, size=len(diffs), replace=True)) for _ in range(n_boot)]
      alpha = (1 - ci) / 2
      return float(np.percentile(boot_means, 100 * alpha)), float(np.percentile(boot_means, 100 * (1 - alpha)))
  ```

### 3. Non-Parametric Significance Testing
- Compute paired instance-level differentials:
  $$d_i = M(\text{SCBI}(x_i)) - M(\text{baseline}(x_i))$$
- Perform a two-sided **Wilcoxon signed-rank test** on paired differentials $\{d_i\}_{i=1}^N$.
- Report the test statistic $W$ and the exact $p$-value.
- If $p \ge 0.01$, the null hypothesis $H_0$ cannot be rejected; the claim of improvement is not statistically established.

### 4. Effect Size Metrics
- In addition to $p$-values, report **Cohen's $d$** or non-parametric **Cliff's $\delta$**:
  $$\text{Cliff's } \delta = \frac{\#(\text{SCBI} > \text{baseline}) - \#(\text{SCBI} < \text{baseline})}{N \times N}$$
- Classify effect size according to standard thresholds:
  - $|\delta| < 0.147$: Negligible
  - $0.147 \le |\delta| < 0.33$: Small
  - $0.33 \le |\delta| < 0.474$: Medium
  - $|\delta| \ge 0.474$: Large

---

## Mandatory Failure Mode Analysis

Every empirical report must analyze the instances where SCBI failed ($\Delta M_i < 0$):

```markdown
### Failure Mode Distribution Analysis
Total Test Instances: N = 1,000
- Instances where SCBI improved performance (ΔM > 0): N+ = 210 (21.0%)
- Instances where SCBI tied baseline (ΔM = 0): N= = 720 (72.0%)
- Instances where SCBI degraded performance (ΔM < 0): N- = 70 (7.0%)

#### Failure Taxonomy Breakdown (N- = 70):
1. **Degenerate Representation (Collapse):** Basis B_t collapsed to near-rank-deficient subspace (N = 32, 45.7%).
2. **Objective Misalignment:** Low self-consistency loss E correlated with incorrect final output (N = 25, 35.7%).
3. **Iteration Oscillation:** Inference cycled between candidate states without convergence (N = 13, 18.6%).
```

---

## Statistical Verification Checklist

- [ ] Evaluated across at least 5 seeds.
- [ ] 95% bootstrap confidence intervals computed and reported.
- [ ] Paired non-parametric statistical tests (Wilcoxon) executed; exact $p$-values stated.
- [ ] Effect sizes (Cliff's $\delta$ / Cohen's $d$) calculated.
- [ ] Negative instances ($N^-$) cataloged and attributed to concrete failure classes.
