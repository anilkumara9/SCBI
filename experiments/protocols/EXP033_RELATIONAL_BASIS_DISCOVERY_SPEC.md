# EXP033: Autonomous Relational Basis Discovery Specification

## 1. Executive Summary & Epistemological Status
- **Experiment ID:** `EXP033`
- **Date:** 2026-09-11
- **Governing Law:** All 14 Inviolable Agent Laws in [`AGENTS.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/AGENTS.md).
- **Epistemological Status:** `[HYPOTHESIS]` Pre-registered confirmatory benchmark evaluating whether internal relational geometry can autonomously discover task-relevant SCBI intervention directions without semantic token tags.
- **Evaluated Architecture:** `EleutherAI/pythia-160m` (12 layers, $d_{\mathrm{model}}=768$, Revision `e72e396263595503028d71243171317d7ae65463`).
- **Benchmark:** `BENCH-002-NL` ($N = 50$ confirmatory instances, Seed 84).
- **Frozen Backbone Guarantee:** Parameter SHA-256 hash verified invariant before and after inference: `54c88fa4897785f2bd94b32d26de1f73f1052bcc42124d563d0cda96940de936` ($\Delta\theta \equiv 0$).

---

## 2. Theoretical Motivation & The Relational Paradigm

EXP032 conclusively established that the tested unlabeled covariance eigenvectors did not reliably recover the task-relevant intervention direction ($\Sigma(h) \to \text{PCA} \not\to V^*$). Whether this failure is caused by variance being dominated by token position, syntactic framing, or residual stream scaling remains an open mechanistic hypothesis. What is empirically established is:

$$\boxed{\text{high activation variance} \neq \text{task-relevant intervention direction}}$$

In biological and artificial neural networks, useful functional representations are **relational**: they emerge from differences between competing semantic hypotheses, attention-weighted pathways, or counterfactual states ($h_i - h_j$). The paradigm shifts from Level 1 (Static Geometry: $\Sigma(h)$) to Level 2 (Relational Geometry: $h_i - h_j$).

$$\boxed{\textbf{Central Question: Can Unlabeled Relational Differences Discover Task-Relevant Bases Without Human Token Tags?}}$$

---

## 3. Candidate Relational Generators ($\mathcal{G}_{\mathrm{relational}}$)

All generators are evaluated at the proven champion configuration: **Layer 8, $C_0$ Ungated Linear Projection ($\alpha=0.25$, rank $r=2$)**:

### Generator 1: $G_{\mathrm{explicit-contrast}}$ (Supervised Reference Baseline)
Gold-standard reference using human-provided premise and distractor token tags. (Benchmark: $+14.0$ pp headroom in EXP030–032).

### Generator 2: $G_{\mathrm{attention-relational}}$ (Attention-Weighted Relational Difference)
Uses the model's own internal self-attention pattern at the preceding block (Layer 7).
1. Compute the average attention weight $a_t = \frac{1}{H} \sum_{heads} A_{7, head}[\text{last\_token}, t]$ across prompt tokens.
2. Partition tokens into high-attention tokens (top 20%) and low-attention tokens (bottom 20%).
3. Compute the mean activation difference:
   $$\Delta h_{\mathrm{attn}} = \bar{h}[\text{high\_attn}] - \bar{h}[\text{low\_attn}]$$
4. Form $V_{\mathrm{attn}}$ by orthonormalizing $\Delta h_{\mathrm{attn}}$ and its dominant orthogonal complement.

### Generator 3: $G_{\mathrm{hypothesis-contrast}}$ (Top-2 Output Prediction Conflict)
Uses the model's own internal uncertainty between its top-2 competing predictions at the readout:
1. Under the unintervened forward pass, extract the top-2 predicted token IDs: $y_1 = \arg\max \text{logits}$, $y_2 = \text{runner-up}$.
2. Extract the corresponding unembedding vectors from $W_U \in \mathbb{R}^{V \times d}$:
   $$w_{\mathrm{diff}} = W_U[y_1] - W_U[y_2]$$
3. Form $V_{\mathrm{hyp}}$ from $w_{\mathrm{diff}}$ and its projection onto the residual stream.

### Generator 4: $G_{\mathrm{latent-counterfactual}}$ (Contextual Perturbation Difference)
Computes the difference vector between the original residual state and a perturbed forward pass:
1. Run a parallel forward pass where 20% of non-essential prompt tokens are masked with `<|endoftext|>`.
2. Compute the residual stream difference across tokens:
   $$\Delta h_{\mathrm{latent}} = h_{\mathrm{orig}} - h_{\mathrm{perturbed}}$$
3. SVD on $\Delta h_{\mathrm{latent}}$ to extract top-2 principal difference directions.

### Generator 5: $G_{\mathrm{trajectory-difference}}$ (Inter-Layer Computation Trajectory)
Captures the directional evolution of the residual stream as representation transforms between mid-stage reasoning and late-stage read-out:
1. Extract residual states at Layer 6 ($h_6$) and Layer 8 ($h_8$).
2. Compute the inter-layer trajectory update:
   $$\Delta h_{\mathrm{traj}} = h_8 - h_6$$
3. Center and compute SVD on $\Delta h_{\mathrm{traj}}$ to extract top-2 principal acceleration directions.

### Generator 6: $G_{\mathrm{random}}$ (Null Control Baseline)
Random orthonormal rank-2 subspace sampled uniformly from the Stiefel manifold.

---

## 4. Pre-Registered Hypotheses & Falsification Criteria

### Hypothesis 1: Relational Recovery ($H_{\mathrm{relational}}$)
$$\Delta M(G_{\mathrm{relational}}) \ge +8.0\text{ pp} \quad \text{AND} \quad \Delta\log p(G_{\mathrm{relational}}) > 0$$
- **Predicted Outcome:** At least one unlabeled relational generator captures statistically significant headroom above baseline ($p < 0.05$) and achieves a positive target log-probability shift, proving that internal relational differences discover useful intervention directions without human token tags.
- **Falsification Criterion:** If all relational generators yield $\Delta M \le +2.0$ pp or $\Delta\log p \le 0$, the hypothesis that internal relational differences discover useful bases is rejected.

---

## 5. Statistical Protocol
- Pre/post parameter SHA-256 hash verified identical ($\Delta\theta \equiv 0$).
- 1,000-resample bootstrap 95% confidence intervals for $\Delta M$.
- Exact Paired McNemar tests vs. $M_I$ and vs. $G_{\mathrm{random}}$.
- Output data saved to `experiments/runs/EXP033_relational/exp033_relational_results.json`.
