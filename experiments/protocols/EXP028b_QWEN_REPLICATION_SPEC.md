# EXP028b Protocol Specification: Modern Architecture Replication on Qwen2.5-0.5B

## 1. Executive Mandate & Research Objective

EXP028a provided prospective confirmation on `facebook/opt-125m` that representation-level statistics can prospectively identify a viable intervention stage ($l^*=7$) without task labels. However, OPT-125M remains a sequential pre-LN architecture. 

**EXP028b** tests the critical question:
> **Does the representation-only stage predictor correctly select a useful intervention stage on a genuinely different modern architecture (`Qwen/Qwen2.5-0.5B`)?**

`Qwen/Qwen2.5-0.5B` is a modern 24-layer foundation model incorporating:
- 24 Transformer decoder layers ($d_{\mathrm{model}} = 896$)
- Rotary Position Embeddings (RoPE)
- SwiGLU activation functions
- RMSNorm pre-normalization
- QK-Norm attention stabilization
- 151,665 token vocabulary

---

## 2. Inviolable Governance Laws (AGENTS.md)

1. **Law 1 (Read Before Modifying):** Anchor strictly in definitions and protocols.
2. **Law 2 (Never Invent Results):** All numbers must be produced by direct empirical code execution.
3. **Law 4 (Never Silently Shift Hypotheses):** Pre-register success criteria before running benchmark evaluation.
4. **Law 6 (Frozen Backbone):** $\Delta\theta \equiv 0$. Pre- and post-run parameter hashes must match.
5. **Law 7 (Zero Data Leakage):** Phase A must run strictly on unlabeled calibration prompts with zero benchmark label exposure.
6. **Law 8 (Never Delete Failed Experiments):** Retain all runs.
7. **Law 9 (No Cherry-Picking):** Lock $l^*$ permanently before Phase B; no post-hoc layer re-centering.
8. **Law 13 (Deterministic Reproducibility):** Pin seeds (Seed 123 for calibration, Seed 84 for benchmark).
9. **Law 14 (Challenge Rather Than Defend):** Adversarially test whether the stage-selection principle generalizes to modern architectures.

---

## 3. Two-Phase Protocol Architecture

### Phase A: Prospective Stage Prediction (Unlabeled Calibration Only)
1. Load `Qwen/Qwen2.5-0.5B`.
2. Compute backbone SHA-256 hash ($\theta_0$).
3. Run forward passes on $N_{\mathrm{calib}} = 20$ unlabeled prompt representations (`BENCH-002-NL` calibration subset, Seed 123).
4. For all candidate layers $l \in [0, 23]$:
   - Compute token-level contrastive separation $d_t = \|P_- h_t\| - \|P_+ h_t\|$.
   - Compute representation selectivity index $\mathrm{SI}_{\mathrm{rep}}(l) = \text{mean}(d_{\mathrm{dist}} > 0) - \text{mean}(d_{\mathrm{prem}} > 0)$.
   - Compute Grassmann subspace orthogonality $\mathcal{O}_{\mathrm{subspace}}(l) = 1 - \frac{\|V_+^\top V_-\|_F}{\sqrt{r}}$.
   - Compute intrinsic representation score:
     $$S_{\mathrm{representation}}(l) = \mathrm{SI}_{\mathrm{rep}}(l) \times \mathcal{O}_{\mathrm{subspace}}(l)$$
   - Compute pre-outcome intervention diagnostic (on calibration prompts):
     $$S_{\mathrm{intervention}}(l) = \frac{\mathrm{SI}(l)}{1 + \mathrm{KL}(l)}$$
5. Identify:
   - Locked layer: $l^* = \arg\max_l S_{\mathrm{representation}}(l)$
   - Runner-up layer: $l_{\mathrm{second}} = \arg\max_{l \neq l^*} S_{\mathrm{representation}}(l)$
   - Margin: $\Delta S = S(l^*) - S(l_{\mathrm{second}})$
6. Save immutable lock record to `experiments/runs/EXP028b_qwen/exp028b_prediction_lock.json` and compute SHA-256 checksum.

### Phase B: Confirmatory Benchmark Evaluation
1. Reveal confirmatory benchmark instances ($N=100$, Seed 84).
2. Evaluate locked layer $l^*$ against:
   - Unintervened Baseline Identity ($M_I$)
   - Pre-declared normalized baseline layer: Layer 16 ($\lambda = 16/24 \approx 0.667$)
   - Runner-up / adjacent layer
3. Operators evaluated at each stage:
   - Identity ($I$)
   - Random candidate subspace ($O5_{\mathrm{random}}$)
   - Autonomous selection via Counterfactual Evaluator ($O5_{E_{CF}}$)
   - Empirical Oracle candidate ($O5_{\mathrm{Oracle}}$)

---

## 4. Pre-Registered Tri-State Outcome Space

| Outcome State | Formal Mathematical Condition | Epistemological Meaning |
| :--- | :--- | :--- |
| **Outcome 1: Prediction Confirmed** | $\Delta M_{\mathrm{Oracle}}(l^*) > 0 \text{ AND } M_{\mathrm{Oracle}}(l^*) \ge M_{\mathrm{Oracle}}(\text{Layer 16})$ | Strong evidence for generalizable prospective stage-selection on modern architectures |
| **Outcome 2: Coarse Validity** | $\Delta M_{\mathrm{Oracle}}(l^*) \le 0 \text{ AND } \exists l \in \{l^* \pm 1, 16\} : \Delta M_{\mathrm{Oracle}}(l) > 0$ | Representation metric has coarse predictive validity; local calibration needed |
| **Outcome 3: Prediction Falsified** | $\Delta M_{\mathrm{Oracle}}(l) \le 0 \ \forall l \in \{l^*, 16\}$ | Stage-selection principle fails on this modern architecture; boundary established |

---

## 5. Pre-Registered Statistical Hypotheses

- **Primary Endpoint:** $\Delta M_{\mathrm{Oracle}}(l^*) = M_{\mathrm{Oracle}}(l^*) - M_I > 0$ with 10,000-bootstrap 95% CI strictly excluding zero.
- **Secondary Endpoints:**
  - Autonomous Headroom: $\Delta M_{E_{CF}}(l^*) > 0$ and $M_{E_{CF}}(l^*) > M_{\mathrm{Random}}(l^*)$.
  - Target Token Log-Probability: $\Delta \log p(y_{\mathrm{correct}}) > 0$ (Paired Wilcoxon signed-rank test).
  - Selectivity Index: $\mathrm{SI}(l^*) > 0$.
  - Output Preservation: $\mathrm{KL} < 0.05$, Top-10 vocabulary overlap $> 90\%$.
  - Pairwise McNemar test and Wilcoxon test: $l^*$ vs. Layer 16 baseline.
