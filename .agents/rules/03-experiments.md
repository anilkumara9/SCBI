# Rule 03: Experimental Protocols & Empirical Rigor

**Applies to:** All benchmark designs, experimental executions, ablation studies, baseline comparisons, and metric evaluations.  
**Foundational Documents:**
- [`documentation/researchidea.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/documentation/researchidea.md) §4, §8 (Core hypothesis and empirical verification standards)
- [`documentation/theory.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/documentation/theory.md) §3 (Operationalization of $\Delta M$)
- [`documentation/math.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/documentation/math.md) §12–§16 (Inference budgets, baseline comparisons, ablations)

---

## 1. Operationalizing Improvement ($\Delta M$)

Empirical performance must always be quantified relative to a rigorously controlled baseline:

$$\Delta M = M(\text{SCBI}) - M(\text{baseline})$$

- **Core Scientific Rule:** An observed $\Delta M > 0$ is strictly evidence of performance differential under that specific protocol. It is **never** automatic proof that the SCBI mechanism caused the gain until all confounding variables (compute, sampling diversity, prompt length, randomness) are controlled.

---

## 2. Compute-Matched Baselines (Mandatory Invariant)

Comparing an iterative SCBI method that performs $K$ forward passes against a single-forward-pass baseline ($K=1$) and claiming superiority is **scientifically invalid**.

Every experimental evaluation must include budget-matched baselines:
1. **FLOP-Matched / Forward-Pass-Matched:** If SCBI uses $K \times T$ evaluations, baselines must include:
   - Self-Consistency / Best-of-$N$ with $N = K \times T$ forward passes;
   - Chain-of-Thought / Test-Time Search with equivalent token/compute budgets;
   - Ensembling / Monte Carlo sampling matched on compute.
2. **Latency & Memory Footprint:** Wall-clock latency and peak VRAM must be logged and tabulated alongside accuracy metrics.

---

## 3. Mandatory Ablation Matrix

Any experimental paper, report, or benchmark submission must include the following 5 ablations:

| Ablation | Modification | Purpose |
| :--- | :--- | :--- |
| **Ablation 1: Random Selection** | Replace $\mathcal{S}(\dots)$ with uniform random selection over generated $\{B_{t,k}\}$. | Tests whether the evaluation objective $\mathcal{E}$ actually provides signal. |
| **Ablation 2: Static Basis** | Fix $B_t = B_0$ across all steps without update. | Isolates the benefit of dynamic basis invention vs fixed projection. |
| **Ablation 3: Shuffled / Null Metric** | Invert or perturb the self-consistency loss $\mathcal{E}$. | Proves whether optimizing the specific self-consistency metric is beneficial or detrimental. |
| **Ablation 4: Budget Curve ($T$)** | Evaluate $T \in \{0, 1, 2, 3, 5, 10\}$. | Verifies monotonic or diminishing returns with respect to iteration count. |
| **Ablation 5: Zero-State ($z_t = \emptyset$)** | Run candidate generation without carrying over state $z_t$. | Evaluates the necessity of persistent inference state. |

---

## 4. Zero Data Leakage & Test Integrity

- Ground truth labels $y$ must **never** be accessible during the candidate generation, evaluation, or selection phases.
- If unsupervised self-consistency is used, ensure no proxy signal leaks ground truth from test examples.
- Pre-processing statistics (e.g. normalization, scaling) must be computed exclusively on training/validation splits, never on test sets.

---

## 5. Statistical Rigor Standards

- **Seed Replication:** All experiments must be conducted across a minimum of 5 distinct random seeds.
- **Reporting Metrics:** Mean $\mu$, standard deviation $\sigma$, and 95% bootstrap confidence intervals must be reported.
- **Significance Testing:** Paired Wilcoxon signed-rank tests or permutation tests must be reported when claiming statistically significant differences.
- **Failure Analysis:** A dedicated table detailing failure cases (instances where $\Delta M < 0$) must be included in every empirical report.
