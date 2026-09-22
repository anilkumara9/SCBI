# EXP028c Protocol Specification: Positional-Mechanism & Architectural Replication on BLOOM-560M

## 1. Executive Mandate & Research Objective

EXP028a (OPT-125M) and EXP028b (Qwen2.5-0.5B) demonstrated that intrinsic representation-stage statistics prospectively identify viable intervention depths across two distinct foundation models without task labels.

**EXP028c** tests the critical next hypothesis on `bigscience/bloom-560m`:
> **Does the frozen, representation-only stage predictor prospectively identify a useful SCBI intervention depth in an architecture with ALiBi positional biases and a substantially different transformer design?**

`bigscience/bloom-560m` provides an aggressive stress test of stage selection because it incorporates:
- 24 Transformer decoder layers ($d_{\mathrm{model}} = 1024$)
- Attention with Linear Biases (**ALiBi**) positional mechanism (zero learned positional embeddings, zero RoPE)
- LayerNorm pre-normalization
- GeLU activation functions
- Untied input and output embeddings
- 250,680 token multilingual vocabulary

---

## 2. Inviolable Epistemological Scope Condition & Caution

Per pre-registration requirements:
> `[EPISTEMOLOGICAL CAUTION]` **The ALiBi positional mechanism is a model-level architectural characteristic, not itself a causal variable in this experiment. A successful BLOOM result would demonstrate transfer across the tested architectural/positional-encoding boundary, but would not establish that ALiBi-independence is the causal explanation.**

---

## 3. Pre-Registered Formula & Governance Rules

The representation score formula remains strictly immutable and unadjusted:
$$S_{\mathrm{representation}}(l) = \mathrm{SI}_{\mathrm{rep}}(l) \times \mathcal{O}_{\mathrm{subspace}}(l)$$
- Zero weighting modifications.
- Zero Qwen- or OPT-derived adjustments.
- Zero architecture-specific normalization.
- Zero manual layer re-centering.

Governing Laws:
- **Law 1 (Read Before Modifying):** Anchor strictly in definitions and protocols.
- **Law 2 (Never Invent Results):** All data must come from direct code execution.
- **Law 4 (Never Silently Shift Hypotheses):** Pre-register all endpoints before inspecting benchmark outputs.
- **Law 6 (Frozen Backbone):** $\Delta\theta \equiv 0$. Parameter hashes verified invariant before and after inference.
- **Law 7 (Zero Data Leakage):** Phase A strictly operates on $N_{\mathrm{calib}}=20$ unlabeled calibration prompt representations (Seed 123) with zero task labels.
- **Law 9 (No Cherry-Picking):** Lock $l^*$ permanently before Phase B.
- **Law 13 (Deterministic Reproducibility):** Seeds pinned (Seed 123 for calibration, Seed 84 for benchmark).
- **Law 14 (Challenge Rather Than Defend):** Report empirical results regardless of outcome.

---

## 4. Two-Phase Protocol Architecture

### Phase A: Prospective Stage Prediction (Unlabeled Calibration Only)
1. Load `bigscience/bloom-560m`.
2. Record model commit hash, tokenizer specifications, and compute pre-inference parameter SHA-256 ($\theta_0$).
3. Run forward passes on $N_{\mathrm{calib}} = 20$ unlabeled calibration prompt representations (`BENCH-002-NL`, Seed 123).
4. Across all candidate layers $l \in [0, 23]$:
   - Compute token-level contrastive evidence $d_t = \|P_- h_t\| - \|P_+ h_t\|$.
   - Compute representation selectivity index $\mathrm{SI}_{\mathrm{rep}}(l) = \text{mean}(d_{\mathrm{dist}} > 0) - \text{mean}(d_{\mathrm{prem}} > 0)$.
   - Compute Grassmann subspace orthogonality $\mathcal{O}_{\mathrm{subspace}}(l) = 1 - \frac{\|V_+^\top V_-\|_F}{\sqrt{r}}$.
   - Compute $S_{\mathrm{representation}}(l) = \mathrm{SI}_{\mathrm{rep}}(l) \times \mathcal{O}_{\mathrm{subspace}}(l)$.
   - Compute pre-outcome intervention diagnostic $S_{\mathrm{intervention}}(l) = \frac{\mathrm{SI}(l)}{1 + \mathrm{KL}(l)}$.
5. Identify:
   - Locked layer: $l^* = \arg\max_l S_{\mathrm{representation}}(l)$
   - Runner-up layer: $l_{\mathrm{second}} = \arg\max_{l \neq l^*} S_{\mathrm{representation}}(l)$
   - Margin: $\Delta S = S(l^*) - S(l_{\mathrm{second}})$
6. Save immutable lock record to `experiments/runs/EXP028c_bloom/exp028c_prediction_lock.json` and seal with SHA-256 checksum.

### Phase B: Confirmatory Benchmark Evaluation
1. Reveal confirmatory benchmark instances ($N=100$, Seed 84).
2. Evaluate locked layer $l^*$ against:
   - Unintervened Baseline Identity ($M_I$)
   - Pre-declared heuristic baseline: Layer 16 ($\lambda = 16/24 \approx 0.667$)
   - Runner-up layer
3. Evaluate Operators:
   - Identity ($I$)
   - Random candidate subspace ($O5_{\mathrm{random}}$)
   - Autonomous selection via Counterfactual Evaluator ($O5_{E_{CF}}$)
   - Empirical Oracle candidate ($O5_{\mathrm{Oracle}}$)

---

## 5. Pre-Registered Tri-State Outcome Space

| Outcome State | Mathematical Condition | Epistemological Meaning |
| :--- | :--- | :--- |
| **Outcome 1: Prediction Confirmed** | $\Delta M_{\mathrm{Oracle}}(l^*) > 0 \text{ AND } M_{\mathrm{Oracle}}(l^*) \ge M_{\mathrm{Oracle}}(\text{Layer 16})$ | Strong prospective evidence that stage selection transfers to ALiBi/BLOOM architecture |
| **Outcome 2: Coarse Validity** | $\Delta M_{\mathrm{Oracle}}(l^*) \le 0 \text{ AND } \exists l \in \{l_{\mathrm{runner-up}}, 16\} : \Delta M_{\mathrm{Oracle}}(l) > 0$ | Metric has coarse predictive validity; runner-up captures headroom |
| **Outcome 3: Prediction Falsified** | $\Delta M_{\mathrm{Oracle}}(l) \le 0 \ \forall l \in \{l^*, 16\}$ | Stage-selection principle fails on this architecture; domain boundary characterized |

---

## 6. Pre-Registered Statistical Hypotheses

- **Primary Endpoint:** $\Delta M_{\mathrm{Oracle}}(l^*) = M_{\mathrm{Oracle}}(l^*) - M_I > 0$ with 10,000-bootstrap 95% CI strictly excluding zero.
- **Comparative Endpoints:**
  - Locked Layer $l^*$ vs. Baseline Layer 16: Exact Paired McNemar Test ($p_{\mathrm{one-sided}} < 0.05$).
  - Target Token Log-Probability: $\Delta \log p(y_{\mathrm{correct}})$ advantage (Paired Wilcoxon Signed-Rank Test).
  - Autonomous SCBI Efficacy: $M_{E_{CF}}(l^*) > M_{\mathrm{Random}}(l^*)$.
  - Representation Preservation: Output $\mathrm{KL} < 0.05$, Top-10 vocabulary overlap $> 85\%$.
