# EXP028: Prospective Functional-Stage Alignment Replication Protocol Specification

**Status:** Pre-Registered Experimental Specification  
**Governing Laws:** [`AGENTS.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/AGENTS.md) Laws 1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14  
**Target Architecture (EXP028a):** `facebook/opt-125m` (125M parameters, 12 layers, $d_{\mathrm{model}}=768$, Meta AI lineage, pre-LN transformer decoder)  
**Calibration Dataset (Phase A):** Unlabeled prompt slice ($N_{\mathrm{calib}}=20$, Seed 123) from `BENCH-002-NL` (zero access to target labels)  
**Confirmatory Benchmark (Phase B):** `BENCH-002-NL` Confirmatory Set ($N=100$, Seed 84)  
**Output Prediction Lock:** `experiments/runs/EXP028_prospective/exp028_prediction_lock.json`  
**Output Confirmatory Benchmark:** `experiments/runs/EXP028_prospective/exp028_confirmatory_results.json`  

---

## 1. Scientific Context & Motivation

In EXP026, the pre-declared normalized depth heuristic ($\lambda = l/L \approx 0.667$, Layer 8 of 12) transferred within the GPT-2 family but failed on `EleutherAI/pythia-160m` ($M_{\mathrm{Oracle}} = M_I = 0.5900, \Delta M_{\mathrm{Oracle}} = 0.0000$).
In EXP027, a diagnostic decomposition revealed that the failure was best explained by a **functional depth mismatch**:
- At Layer 4 ($\lambda \approx 0.333$), Pythia-160M achieved $M_{\mathrm{Oracle}} = 0.7100$ ($\Delta M_{\mathrm{Oracle}} = \mathbf{+0.1200}$), with strong contrastive selectivity ($\mathrm{SI} = 0.3844$) and minimal logit drift ($\mathrm{KL} = 0.0463$).
- Layer 4 was statistically superior to Layer 8 in paired testing ($b/c = 13/1, p = 0.000916$).

However, EXP027 was a **post-hoc diagnostic**. A scientific principle cannot rely on retrospective layer sweeping. 
**Objective of EXP028:** Test whether an unsupervised, architecture-independent probe can prospectively predict the effective SCBI intervention stage $l^*$ on an unseen model (`facebook/opt-125m`) **strictly before ground truth labels are revealed or task accuracy is evaluated**.

---

## 2. Inviolable Protocol Locks & Leakage Boundaries

1. `[LAW 6]` **Frozen Parameter Invariant ($\Delta\theta \equiv 0$):** Pre/post execution SHA-256 parameter hashes must match identically. No weights or buffers may be updated.
2. `[LAW 7]` **Strict Prediction-Before-Outcome Firewall:**
   - In Phase A, the stage prediction algorithm receives **only unlabelled prompt texts** (`Context: ... Distractor: ... Question: ... Answer:`).
   - Target tokens $y_{\mathrm{correct}}$ and distractor tokens $y_{\mathrm{distractor}}$ are **strictly prohibited** from Phase A.
   - The predicted layer $l^*$ must be locked and hashed in an immutable JSON file **before** Phase B execution commences.
3. `[LAW 9 & 14]` **Anti-Cherry-Picking Invariant:** Under no circumstances will $l^*$ be shifted post-hoc if it underperforms. The primary test is evaluated strictly at the pre-registered $l^*$.
4. `[LAW 13]` **Deterministic Reproducibility:** Seeds, token offsets, and device precision (`float32`) are pinned.

---

## 3. Mathematical Specification of Stage Selection Metrics

For each layer $l \in \{1, \dots, L\}$ (where $L=12$ for OPT-125M):

### Metric 1: Intrinsic Representation Stage Score ($S_{\mathrm{representation}}$, Primary Predictor)
Computed in a **single forward pass** over unlabeled prompt representations $h_t(l) \in \mathbb{R}^d$, with **zero interventions applied** and **zero downstream forward passes**:
$$S_{\mathrm{representation}}(l) = \mathrm{SI}_{\mathrm{rep}}(l) \times \mathcal{O}_{\mathrm{subspace}}(l)$$
where:
1. **Prompt Contrastive Selectivity ($\mathrm{SI}_{\mathrm{rep}}$):**
   Using SVD subspaces $V_+ \in \mathbb{R}^{d \times r}$ from premise token slices and $V_- \in \mathbb{R}^{d \times r}$ from distractor token slices:
   $$e_t^- = \|V_-^\top h_t(l)\|_2, \quad e_t^+ = \|V_+^\top h_t(l)\|_2, \quad d_t = e_t^- - e_t^+$$
   $$\mathrm{SI}_{\mathrm{rep}}(l) = P(d_t > 0 \mid t \in \mathcal{T}_{\mathrm{distractor}}) - P(d_t > 0 \mid t \in \mathcal{T}_{\mathrm{premise}})$$
2. **Grassmann Subspace Orthogonality ($\mathcal{O}_{\mathrm{subspace}}$):**
   Measures the angular separation between the premise and distractor subspace spans:
   $$\mathcal{O}_{\mathrm{subspace}}(l) = 1.0 - \frac{\|V_+^\top V_-\|_F}{\sqrt{r}}$$
   ($\mathcal{O} \to 1$ implies mutually orthogonal, non-interfering representation manifolds; $\mathcal{O} \to 0$ implies collinear collapse).

**Prospective Stage Lock:**
$$l^* = \arg\max_{l \in \{1, \dots, L\}} S_{\mathrm{representation}}(l)$$

### Metric 2: Pre-Outcome Intervention Diagnostic Score ($S_{\mathrm{intervention}}$, Secondary Diagnostic)
Evaluates whether applying $O5$ to prompt representations causes downstream logit drift, without accessing target tokens:
$$S_{\mathrm{intervention}}(l) = \frac{\mathrm{SI}_{\mathrm{rep}}(l)}{1.0 + \mathrm{KL}_{\mathrm{unlabeled}}(l)}$$
where $\mathrm{KL}_{\mathrm{unlabeled}}(l) = \mathrm{KL}(p_{\mathrm{base}} \,\|\, p_{O5})$ on the prompt's last token distribution.

---

## 4. Confirmatory Benchmark Evaluation (Phase B)

Once $l^*$ is permanently locked, Phase B evaluates `facebook/opt-125m` on `BENCH-002-NL` ($N=100$, Seed 84):
1. **Condition 1 (Baseline Identity):** Unmodified model inference ($M_I$).
2. **Condition 2 (Pre-Declared Heuristic Layer 8):** SCBI evaluated at linear normalized depth $\lambda = 8/12 \approx 0.667$.
3. **Condition 3 (Prospective Predicted Layer $l^*$):** SCBI evaluated at the locked prospective layer $l^*$.

### Endpoints & Statistical Hypotheses:
- **Primary Hypothesis:** $\Delta M_{\mathrm{Oracle}}(l^*) = M_{\mathrm{Oracle}}(l^*) - M_I > 0$ with exact McNemar test $p < 0.05$ and bootstrap 95% CI $> 0$.
- **Comparative Hypothesis:** $M_{\mathrm{Oracle}}(l^*) > M_{\mathrm{Oracle}}(8)$ tested via exact paired McNemar test ($p < 0.05$).
- **Secondary Mechanistic Endpoints:**
  - Autonomous candidate recovery: $\Delta M_{E_{CF}}(l^*) > 0$
  - Target-token probability change: $\Delta \log p(y_{\mathrm{correct}}) > 0$
  - Selectivity Index: $\mathrm{SI}(l^*) > 0.20$

---

## 5. Pre-Registered Tri-State Decision Matrix

| Empirical Result | Primary Criterion | Secondary Criterion | Pre-Registered Scientific Conclusion |
| :--- | :--- | :--- | :--- |
| **Outcome 1: Confirmed** | $\Delta M_{\mathrm{Oracle}}(l^*) > 0$ ($p < 0.05$) | $l^*$ outperforms or equals Layer 8 ($M(l^*) \ge M(8)$) | **Generalizable Stage-Selection Principle:** Unsupervised representation geometry prospectively predicts functional intervention depth across model families. |
| **Outcome 2: Coarse Validity** | $l^*$ underperforms, but $l^* \pm 1$ captures positive headroom ($\Delta M > 0$) | $S_{\mathrm{representation}}(l)$ captures the general region | **Partial Predictive Validity:** The metric localizes the active computational regime but requires higher resolution. |
| **Outcome 3: Falsified** | $l^*$ fails ($\Delta M \le 0$) and no positive headroom exists across layers | — | **Principle Falsification:** Residual-space SCBI fails on the tested pre-LN architecture, or representation geometry does not govern intervention capacity. |
