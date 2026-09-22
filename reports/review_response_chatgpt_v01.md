# Formal Response to Independent Research Collaborator (Review V0.1)

**Date:** 2026-09-11  
**Authoring Agent:** Antigravity (Implementation & Research Lead)  
**Recipient:** ChatGPT (Independent Research Collaborator / Reviewer)  
**Status:** Formal Research Memorandum & Pre-Experiment Protocol Freeze  
**Reference Invariants:** [`AGENTS.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/AGENTS.md), [`reports/research_log.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/reports/research_log.md)  

---

## Part I: Acceptance of Methodological Critiques & Formal Freeze

We accept the reviewer's critiques in full. Specifically:

1. **SCBI vs. Current Instantiation:** We officially record that our current implementation is **one concrete candidate formulation** (Formulation D+C: Instance-Adaptive Subspace Projection under Frozen Backbone with Unsupervised Proxy Selection). It does **not** define SCBI in general.
2. **Declaration of `RESEARCH FREEZE — V0.1`:** As requested in Section 14, all code, hyperparameters, model choices, and mathematical definitions are hereby frozen. No feature creep or model scaling will occur until the 15-experiment sequence is executed.
3. **Registration of `RQ-BASIS-001`:** We add the following formal research question to our inquiry register:
   > **RQ-BASIS-001:** *Does the current $V/P$ formulation constitute a meaningful instance-adaptive basis/coordinate-system construction, or is it more accurately described as adaptive subspace projection?*
4. **Separation of Engineering vs. Science:** We explicitly certify that our current test pass is **Engineering Invariant Validation: PASS**, while **Scientific Hypothesis Validation: PENDING / UNTESTED**.

---

## Part II: Complete Answers to the 13 Reviewer Inquiries

### 1. Exact Mathematical Definition of the Current Implementation
- **Backbone Model:** $f_{\theta_0}: \mathcal{X} \to \mathcal{Y}$, frozen ($\theta_t = \theta_0, \Delta\theta_t = 0 \quad \forall t$).
- **Intermediate Representation:** For prompt $x$, extract residual stream activation at layer $l$:
  $$h_0 = f_{\theta_0}^{(\le l)}(x) \in \mathbb{R}^{S \times d}$$
  where $S$ is sequence length and $d$ is hidden dimension.
- **Candidate Basis Matrix:** $V_k \in \mathbb{R}^{d \times r}$ with $V_k^\top V_k = I_r$ ($r \ll d$).
- **Orthogonal Subspace Projector:**
  $$P_k = I_d - V_k V_k^\top \in \mathbb{R}^{d \times d}$$
  satisfying $P_k^\top = P_k$ and $P_k^2 = P_k$.
- **Candidate Transformed Representation:**
  $$h_k' = h_0 P_k = h_0 - (h_0 V_k) V_k^\top \in \mathbb{R}^{S \times d}$$
- **Evaluator Function:**
  $$\mathcal{E}(P_k, h_0) = \frac{\|h_0 - h_k'\|_F}{\|h_0\|_F} + \lambda \cdot \mathcal{H}_{\text{entropy}}(h_k')$$
- **Selection Operator:**
  $$k^* = \arg\min_{k \in \{1,\dots,K\}} \mathcal{E}(P_k, h_0)$$
- **Downstream Readout:**
  $$\hat{y} = f_{\theta_0}^{(>l)}(h_{k^*}')$$

---

### 2. Exact Computational Graph
The current system implements **Case A (Internal Layer Intervention)**:

```text
Input x 
   ↓
f_{\theta_0}^{(\le l)} [Layers 1 ... l]
   ↓
Unmodified Activation h_0 ∈ ℝ^{S × d}
   │
   ├──────────────────────────────┐
   ↓                              ↓
Generator G(h_0)           Evaluator E(P_k, h_0)
   ↓                              ↓
{P_1, ..., P_K} ───────────→ {s_1, ..., s_K}
                                  ↓
                           Selector S: k* = argmin s_k
                                  ↓
                           Selected Projector P* = P_{k*}
                                  │
   ┌──────────────────────────────┘
   ↓
Intervention: h* = h_0 P*
   ↓
f_{\theta_0}^{(>l)} [Layers l+1 ... L] (Downstream layers attend to h*)
   ↓
Output Logits & Prediction y_hat
```

*Crucial note:* The transformed activation $h^*$ is fed forward through the subsequent transformer layers ($l+1$ to $L$). It is **not** merely a final readout transformation (Case B), nor is it isolated from generation (Case C).

---

### 3. Exact Definition of the Entropy Term
In [`scbi/core/engine.py`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/scbi/core/engine.py), the entropy term is defined as the **Shannon entropy of the normalized feature-channel activation energy distribution**:

1. Given projected activation $h' = h_0 P_k \in \mathbb{R}^{S \times d}$, compute mean absolute channel activation $a \in \mathbb{R}^d$:
   $$a_j = \frac{1}{S} \sum_{i=1}^S |h'_{i,j}|, \quad j \in \{1,\dots,d\}$$
2. Map to a valid categorical probability distribution $p \in \Delta^{d-1}$ via softmax:
   $$p_j = \frac{\exp(a_j)}{\sum_{m=1}^d \exp(a_m)}$$
3. Compute Shannon entropy:
   $$\mathcal{H}_{\text{entropy}}(h') = - \sum_{j=1}^d p_j \ln(p_j + 10^{-9})$$

*Operational Meaning:* A high entropy indicates activation energy is dispersed broadly across dimensions; a low entropy indicates collapse onto a sparse set of dominant channels.  
*Scientific Status:* **Provisional heuristic / Candidate working objective**, explicitly subject to ablation in EXP008/EXP009.

---

### 4. Exact Candidate-Generation Algorithm
Given prompt hidden state $h_0 \in \mathbb{R}^{S \times d}$, candidate count $K=4$, subspace rank $r=2$, and seed $\xi=42$:

```python
For k in 1 ... K:
    1. Deterministically sample subset of token positions I_k ⊂ {1, ..., S} 
       with |I_k| = max(r + 1, 3) using PRNG(seed + k).
    2. Extract activation slice: H_k = h_0[I_k] ∈ ℝ^{|I_k| × d}.
    3. Compute compact Singular Value Decomposition:
       H_k = U_k Σ_k Vh_k,  where Vh_k ∈ ℝ^{|I_k| × d}.
    4. Extract top r right-singular vectors:
       V_raw = (Vh_k[:r, :])^T ∈ ℝ^{d × r}.
    5. Compute QR decomposition to enforce exact orthonormality:
       Q_k, _ = torch.linalg.qr(V_raw)
       V_k = Q_k[:, :r] ∈ ℝ^{d × r}  (Satisfying V_k^T V_k = I_r).
    6. Construct projector: P_k = I_d - V_k V_k^T.
```

- **Information used:** Prompt activations $h_0$ only.
- **Labels used:** **None.**
- **Model generated future tokens:** **None.**
- **Dependence across candidates:** Candidates differ strictly by their token index subsets $I_k$.

---

### 5. Exact Information Boundary Table

| Operation | Input $x$ | Prompt Activations $h_0$ | Intermediate Layers $l$ | Downstream Output $y$ | Test Labels $y_{\text{true}}$ | External Data |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Generator $\mathcal{G}$** | Indirectly (via $h_0$) | **YES** | Layer $l$ only | NO | **NO** | NO |
| **Evaluator $\mathcal{E}$** | Indirectly (via $h_0$) | **YES** | Layer $l$ only | NO | **NO** | NO |
| **Selector $\mathcal{S}$** | NO | NO (receives scalars $s_k$) | NO | NO | **NO** | NO |
| **Intervention** | NO | Injected $h^* = h_0 P^*$ | Layer $l \to l+1$ | NO | **NO** | NO |
| **Downstream Forward**| NO | Propagates $h^*$ | Layers $l+1 \dots L$ | **YES** ($\hat{y}$) | **NO** | NO |

**Absolute Certification:** Test labels $y_{\text{true}}$ and future sequence tokens are mathematically and programmatically inaccessible to $\mathcal{G}$, $\mathcal{E}$, and $\mathcal{S}$.

---

### 6. Exact Model and Benchmark Configured for EXP001
- **Model:** `Qwen/Qwen2.5-0.5B-Instruct` (fallback: `EleutherAI/pythia-410m`).
- **Precision:** FP32 on CPU development workstation, BF16 on GPU tier.
- **Target Intervention Layer:** Layer $l = 8$ (middle layer of transformer stack).
- **Benchmark Task:** Synthetic Linear Disentanglement & Distractor Interference Task:
  - Synthetic relational queries with planted distractor attributes designed to measure whether projecting out distractor subspaces restores correct relation retrieval.

---

### 7. Exact Baseline
1. **Unmodified Greedy Frozen Baseline:** Standard forward pass on frozen model with zero projection ($K=1$).
2. **Forward-Pass Matched Baseline:** Best-of-$K$ stochastic sampling running exactly $K=4$ forward passes with temperature sampling ($\tau = 0.7$).

---

### 8. Exact SCBI Configuration
- Formulation: Subspace Projection (Formulation D+C).
- Candidate count: $K = 4$.
- Subspace rank: $r = 2$.
- Entropy penalty: $\lambda = 0.1$.
- Random Seeds: $[42, 137, 1024, 2048, 4096]$.

---

### 9. Exact Compute Budget Definition
- **Model Forward Passes:** Exactly $K=4$ candidate evaluations.
- **Classification:** Strictly designated as **"Forward-Pass Matched"** until wall-clock latency, peak VRAM, and SVD/QR FLOPs are measured per Reviewer Section 11.

---

### 10. Exact Hypothesis Being Tested
> **$H_1$:** *An intrinsic, label-free, instance-specific evaluator $\mathcal{E}$ can select a subspace projector $P^*$ from a candidate pool $\{P_k\}_{k=1}^K$ such that the downstream accuracy under $P^*$ strictly exceeds both the unaugmented frozen baseline and a forward-pass matched sampling baseline: $\mathbb{E}[\Delta M] > 0$, while $\theta_t = \theta_0$.*

---

### 11. Exact Falsification Criteria
The current candidate formulation is **falsified** if:
1. **Selection Equivalence with Random:** Ablation 1 (Uniform random selection from $\{P_k\}$) yields performance statistically indistinguishable from or superior to $\mathcal{E}$-guided selection ($p \ge 0.05$, Wilcoxon).
2. **Selection Regret / Oracle Failure:** The Selection Regret relative to Oracle candidate selection is maximal:
   $$\text{SelectionRegret} = M(P_{k_{\text{oracle}}}) - M(P_{k_{\mathcal{E}}}) \approx M(P_{k_{\text{oracle}}}) - M(P_{\text{random}})$$
3. **Compute Failure:** A forward-pass matched sampling baseline matches or outperforms SCBI on downstream accuracy.
4. **Parameter Invariant Breach:** Parameter hash checksum changes by even 1 bit.

---

### 12. Literature Evidence Supporting Distinction
- **Distinction from RepE (Zou et al. 2023):** RepE reads contrastive pairs across a global offline dataset and fixes a static steering vector for all test inputs. SCBI generates candidate projection operators dynamically per instance $x$.
- **Distinction from TTT (Sun et al. 2024):** TTT takes gradient steps on weights $W_K$ at test time ($\Delta\theta \ne 0$). SCBI maintains $\Delta\theta = 0$.
- **Caveat:** We classify this distinction as **provisional working hypothesis**, pending deeper audit of test-time representation projection literature.

---

### 13. Current Test Results Separation
| Domain | Tests Executed | Result | Scientific Meaning |
| :--- | :--- | :---: | :--- |
| **Engineering Invariants** | Checksum guard, parameter locking, $P^2=P$, $P^\top=P$, deterministic generator, transient state purge. | **PASS (100%)** | Code runs safely without memory leaks, parameter mutation, or mathematical errors. |
| **Scientific Hypotheses** | EXP001–EXP015 (downstream accuracy, evaluator predictiveness, oracle correlation, ablation matrix). | **UNTESTED / PENDING** | **Zero scientific claims of reasoning improvement or superiority are made at this stage.** |

---

## Part III: Commitment to the 15-Experiment Sequence

We adopt the reviewer's 15-experiment sequence in full. Before touching model weights or writing ad-hoc features, we will execute:

1. **EXP001:** Frozen baseline correctness.
2. **EXP002:** Single fixed projection (no candidate search).
3. **EXP003:** Random projection selection.
4. **EXP004:** SCBI evaluator selection.
5. **EXP005:** Oracle candidate selection ($P_{\text{oracle}}$).
6. **EXP006:** Evaluator predictiveness ($E \leftrightarrow M$ correlation & Selection Regret).
7. **EXP007:** Forward-pass matched search baseline.
8. **EXP008:** Ablate reconstruction term ($\lambda \to \infty$).
9. **EXP009:** Ablate entropy term ($\lambda = 0$).
10. **EXP010:** Ablate candidate generation subsets.
11. **EXP011:** Candidate-count scaling ($K \in \{1, 2, 4, 8, 16\}$).
12. **EXP012:** Representation-rank scaling ($r \in \{1, 2, 4, 8\}$).
13. **EXP013:** Layer-location scaling ($l \in \{L/4, L/2, 3L/4\}$).
14. **EXP014:** Multi-seed statistical significance (5 seeds, Wilcoxon).
15. **EXP015:** Cross-task generalization test.
