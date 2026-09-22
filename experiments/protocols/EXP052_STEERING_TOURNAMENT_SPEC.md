# EXP052 Protocol Specification: Steering & Activation Intervention Tournament

**Status:** PRE-REGISTERED  
**Date:** 2026-09-21  
**Predecessor Experiments:** EXP048, EXP049  
**Governing Standard:** `AGENTS.md` (14 Inviolable Laws) & `STATISTICAL_PROTOCOL_V02.md`  

---

## 1. Scientific Context & Mandate

To claim scientific novelty, SCPM must demonstrate superior Pareto efficiency (Accuracy vs. Inference Compute) against well-established inference-time steering and test-time search methods:
1. **RepE (Representation Engineering / ActAdd - Zou et al. 2023):** Static offline mean-difference direction added at test time.
2. **CAA (Contrastive Activation Addition - Rimsky et al. 2023):** Offline token-pair subtraction steering.
3. **Activation Patching / Causal Tracing (Meng et al. 2022):** Clean activation swapping.
4. **Test-Time Compute (TTC - Wang et al. 2022):** Best-of-$N$ and Self-Consistency sampling ($N = 4$ matched passes).

$$\boxed{\text{Does dynamic instance-level basis construction beat static steering vectors and compute-matched sampling?}}$$

---

## 2. Invariant Protocol Locks & Compute Matching

| Method | Forward Passes | Vector/Basis Source | Tuning Budget |
| :--- | :--- | :--- | :--- |
| **Greedy Baseline** | 1 | None | None |
| **RepE (ActAdd)** | 1 | Offline computed across calibration split | Grid search on calibration split |
| **CAA** | 1 | Offline contrastive pairs across calibration | Grid search on calibration split |
| **Best-of-4 Sampling** | 4 | Temperature $T=0.7$, Top-$p=0.9$ | Tuned temperature on calibration split |
| **SCPM ($G_{\text{contrastive}}$)** | 1 | Dynamic instance-level distractor SVD | Frozen $\alpha = 0.25, r = 2$ |
| **SCPM (Multi-Candidate)** | 4 | $K=4$ candidate bases + intrinsic evaluator | Frozen $K=4$ |

---

## 3. Pre-Registered Hypotheses & Success Criteria

### 3.1 Head-to-Head Pareto Dominance:
$$\Delta M_{\text{SCPM}} > \max(\Delta M_{\text{RepE}}, \Delta M_{\text{CAA}}) \quad \text{with } p_{\text{McNemar}} < 0.05$$
SCPM must outperform static global steering vectors because static vectors cannot adapt to instance-specific distractor semantic content.

### 3.2 Compute-Matched Test-Time Search Dominance:
Under identical forward-pass compute budget ($B=4$ passes per instance):
$$M_{\text{SCPM}(K=4)} \ge M_{\text{Best-of-4}} \quad \land \quad \text{Latency}_{\text{SCPM}} \le 0.70 \times \text{Latency}_{\text{Best-of-4}}$$

---

## 4. Pre-Registered Falsification Criteria

SCPM's superiority is **falsified** if:
1. Static RepE or CAA achieves equal or higher accuracy ($\Delta M_{\text{RepE}} \ge \Delta M_{\text{SCPM}}$) with zero instance-level SVD overhead.
2. Best-of-4 sampling achieves significantly higher accuracy ($p < 0.05$) than SCPM at matched forward passes.
3. SCPM incurs $>3\times$ latency overhead compared to static steering while delivering $<2\text{ pp}$ marginal accuracy gain.

---

## 5. Epistemological Interpretation Matrix

| Outcome | Epistemological Status | Interpretation |
| :--- | :--- | :--- |
| **SCPM beats static steering** | `[OBSERVATION]` | Proves that dynamic instance-level basis construction captures instance-specific geometry that static global steering vectors fundamentally miss. |
| **Static RepE matches SCPM** | `[OBSERVATION]` | Falsifies the necessity of dynamic basis invention. The phenomenon reduces to static activation steering, disproving the cognitive basis invention hypothesis. |
