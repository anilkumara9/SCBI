# EXP032: Autonomous Internal Basis Discovery from Unlabeled Activation Geometry Specification

## 1. Executive Summary & Epistemological Status
- **Experiment ID:** `EXP032`
- **Date:** 2026-09-11
- **Governing Law:** All 14 Inviolable Agent Laws in [`AGENTS.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/AGENTS.md).
- **Epistemological Status:** `[HYPOTHESIS]` Pre-registered confirmatory benchmark evaluating whether unlabeled internal activation geometry can discover useful SCBI candidate subspaces without token-level supervision.
- **Evaluated Architecture:** `EleutherAI/pythia-160m` (12 layers, $d_{\mathrm{model}}=768$, Revision `e72e396263595503028d71243171317d7ae65463`).
- **Benchmark:** `BENCH-002-NL` ($N_{\mathrm{calib}}=20$ unlabeled calibration prompts, Seed 123; $N=50$ confirmatory instances, Seed 84).
- **Frozen Backbone Guarantee:** Parameter SHA-256 hash verified invariant before and after inference: `54c88fa4897785f2bd94b32d26de1f73f1052bcc42124d563d0cda96940de936` ($\Delta\theta \equiv 0$).

---

## 2. Core Scientific Question

> **Can unlabeled activation geometry generate candidate subspaces that recover SCBI intervention efficacy without explicit premise/distractor token supervision?**

### The Critical Epistemological Premise:
A covariance eigenvector is strictly a direction of maximal activation variance. It cannot be assumed a priori that $u_1 \equiv \text{task}$ or $u_2 \equiv \text{distractor}$; eigenvectors may capture token-position structure, common residual directions, frequency, or syntax. EXP032 directly tests whether variance-derived directions contain functionally useful intervention subspaces.

---

## 3. Mathematical Formulation of Candidate Generators ($\mathcal{G}$)

For a given layer $l$ and instance representation $h \in \mathbb{R}^{T \times d}$:

### Generator 1: $G_{\mathrm{contrastive}}$ (Supervised Reference Baseline)
Uses manual token indices (`prem_indices`, `dist_indices`) to compute:
$$h_{\mathrm{prem}} = h[\text{prem}], \quad h_{\mathrm{dist}} = h[\text{dist}]$$
Extracting $V_{\mathrm{dist}}$ via SVD on centered distractor activations (EXP026/027 reference).

### Generator 2: $G_{\mathrm{cov\_token}}$ (Prompt Token Covariance)
Computes the empirical covariance across all $T$ tokens within the prompt:
$$\bar{h} = \frac{1}{T} \sum_{t=1}^T h_t, \quad \Sigma_{\mathrm{token}} = \frac{1}{T} \sum_{t=1}^T (h_t - \bar{h})(h_t - \bar{h})^\top \in \mathbb{R}^{d \times d}$$
SVD: $\Sigma_{\mathrm{token}} = U \Lambda U^\top$.  
Candidate subspaces $V_k$ are formed by clustering principal eigenvectors:
- $V_{\mathrm{top}} = [u_1, u_2]$ (Dominant variance)
- $V_{\mathrm{mid}} = [u_3, u_4]$ (Sub-dominant variance)
- $V_{\mathrm{tail}} = [u_5, u_6]$ (Tail variance)

### Generator 3: $G_{\mathrm{cov\_prompt}}$ (Context Population Covariance)
Computed across the mean token representations of the 20 unlabeled calibration prompts:
$$\mu_p = \frac{1}{T_p} \sum_{t} h_{p,t}, \quad \Sigma_{\mathrm{prompt}} = \frac{1}{P} \sum_{p=1}^P (\mu_p - \bar{\mu})(\mu_p - \bar{\mu})^\top$$
Captures inter-prompt semantic variance rather than intra-prompt token variance.

### Generator 4: $G_{\mathrm{residualized}}$ (Position-Residualized Covariance)
Subtracts the mean token representation at each relative token position $\tau \in \{1, \dots, T\}$ computed across calibration prompts to eliminate position-embedding artifacts:
$$\tilde{h}_t = h_t - \bar{h}_{\mathrm{pos}(t)}, \quad \Sigma_{\mathrm{residual}} = \frac{1}{T} \sum_{t=1}^T \tilde{h}_t \tilde{h}_t^\top$$

### Generator 5: $G_{\mathrm{random}}$ (Null Control Baseline)
Generates random rank-$r$ orthonormal matrices $V_{\mathrm{rand}} \in \mathrm{St}(r, d)$ sampled uniformly from the Stiefel manifold.

---

## 4. Evaluation Protocol & Pre-Registered Hypotheses

### Primary Evaluation Conditions:
All generators are evaluated at the proven champion depth: **Layer 8** with **$C_0$ Ungated Linear Projection ($\alpha=0.25$)**, which achieved $+14.0$ pp headroom in EXP030.

### Pre-Registered Tri-State Hypotheses:

1. **Outcome 1 (Autonomous Recovery Confirmed):**
   $$\Delta M(G_{\mathrm{cov\_token}}) \ge +8.0\text{ pp} \quad \text{AND} \quad \Delta M(G_{\mathrm{cov\_token}}) > \Delta M(G_{\mathrm{random}})$$
   Unlabeled activation geometry autonomously discovers useful intervention directions without token supervision, capturing substantial headroom over the random baseline.
2. **Outcome 2 (Population / Residualization Superiority):**
   $G_{\mathrm{cov\_token}}$ fails due to token-position artifacts, but $G_{\mathrm{residualized}}$ or $G_{\mathrm{cov\_prompt}}$ achieves positive headroom ($\ge +8.0$ pp).
3. **Outcome 3 (Unsupervised Geometry Refuted):**
   All covariance-derived generators fail to exceed $G_{\mathrm{random}}$ ($\Delta M \le \Delta M(G_{\mathrm{random}})$). Unlabeled variance axes do not align with task-critical intervention directions; explicit semantic contrast remains necessary.

---

## 5. Required Metrics & Statistical Endpoints
- Baseline accuracy: $M_I$ (30/50, $0.6000$).
- Top-1 Accuracy $M(G)$, Headroom $\Delta M(G) = M(G) - M_I$.
- 95% Bootstrap Confidence Intervals (1,000 resamples) for $\Delta M$.
- Mean continuous target token log-probability shift $\Delta\log p(y_{\mathrm{correct}})$.
- Candidate Quality Spread: $M_{\mathrm{Oracle}}(G) - M(G_{\mathrm{random}})$.
- Headroom Retention Ratio: $\eta = \Delta M(G) / \Delta M(G_{\mathrm{contrastive}})$.
