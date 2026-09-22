# EXP056 Protocol Specification: Autonomous Closed-Loop Basis Lifecycle Verification

**Status:** PRE-REGISTERED  
**Date:** 2026-09-21  
**Predecessor Experiments:** EXP048, EXP049, EXP052  
**Governing Standard:** `AGENTS.md` (14 Inviolable Laws) & `STATISTICAL_PROTOCOL_V02.md`  

---

## 1. Scientific Context & Mandate

The $G_{\text{contrastive}}$ baseline relies on token span offsets to extract the distractor representation. To realize full **Self-Consistent Basis Invention (SCBI)** as a self-contained cognitive architecture, the model must **autonomously construct, evaluate, select, and discard** temporary representations without external token annotations.

EXP056 evaluates an autonomous candidate generator $\mathcal{G}_{\text{unsup}}$ and intrinsic consistency evaluator $\mathcal{E}_{\text{unsup}}$ that operate strictly from the raw prompt representations.

$$\boxed{\text{Can a frozen model autonomously invent and select useful bases without token-span annotations?}}$$

---

## 2. Invariant Closed-Loop Architecture

The complete cognitive lifecycle consists of 5 explicit phases:

```text
Prompt x ──► Forward Pass ──► Residual Covariance ──► SVD Candidates {B_k}
                                                               │
                                                               ▼
Discard B_t ◄── Predict y ◄── Select B* ◄── Intrinsic Evaluator E_unsup({B_k})
```

1. **Construct ($\mathcal{G}_{\text{unsup}}$):** Extract candidate subspaces from top principal components of prompt token hidden state covariance $\Sigma_h = \frac{1}{L} \sum_{i=1}^L (h_i - \bar{h})(h_i - \bar{h})^\top$.
2. **Evaluate ($\mathcal{E}_{\text{unsup}}$):** Compute intrinsic representation consistency / energy reduction score for each candidate $B_k$.
3. **Select ($\mathcal{S}$):** $B^* = \arg\max_k \mathcal{E}_{\text{unsup}}(B_k)$.
4. **Intervene & Infer:** Predict $\hat{y}$ under modulated representation.
5. **Discard:** Reclaim memory buffers; verify that no state persists to subsequent instances.

---

## 3. Pre-Registered Hypotheses & Success Criteria

### 3.1 Autonomous Headroom Recovery:
$$\eta_{\text{autonomous}} = \frac{M(\text{Autonomous}) - M_{\text{base}}}{M(G_{\text{contrastive}}) - M_{\text{base}}} \ge 0.50$$
The fully autonomous loop must recover at least $50\%$ of the supervised span-contrastive headroom.

### 3.2 Intrinsic Evaluator Predictive Validity:
$$\rho_{\text{Spearman}}(\mathcal{E}_{\text{unsup}}(B_k), \Delta \log p(y^* \mid B_k)) \ge +0.25 \quad (p < 0.001)$$
The unsupervised evaluator must exhibit statistically significant positive rank correlation with true prediction confidence.

### 3.3 Zero Leakage & State Isolation:
- Post-inference memory audit: Zero tensor references remaining.
- Inter-instance isolation: Model logits for instance $i$ must be strictly identical whether evaluated alone or after instance $i-1$.
- Weight immutability: $\Delta\theta = 0$ (verified by SHA-256 hash).

---

## 4. Pre-Registered Falsification Criteria

Autonomous basis invention is **falsified** if:
1. $\mathcal{E}_{\text{unsup}}$ performs no better than random candidate selection (Ablation 1: $p > 0.05$).
2. Headroom recovery $\eta_{\text{autonomous}} \le 0.10$, indicating that token-level supervision is strictly required to locate the effective subspace.
3. State leakage occurs between consecutive test instances.

---

## 5. Epistemological Interpretation Matrix

| Outcome | Epistemological Status | Interpretation |
| :--- | :--- | :--- |
| **Criteria Passed ($\eta \ge 0.50$)** | `[OBSERVATION]` | Fully validates Hypothesis A: A frozen model possesses intrinsic mathematical signals enabling autonomous cognitive basis invention without human span supervision. |
| **Evaluator fails to beat random** | `[OBSERVATION]` | Re-confirms the fundamental information-theoretic bottleneck identified in EXP007/EXP008: Beneficial subspaces exist, but their utility is informationally unidentifiable from intermediate representations alone without external supervision. |
