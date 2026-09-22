# EXP049 Protocol Specification: Multi-Seed & Split Invariance Audit

**Status:** PRE-REGISTERED  
**Date:** 2026-09-21  
**Predecessor Experiments:** EXP043, EXP048 (Regression Lock Confirmed)  
**Governing Standard:** `AGENTS.md` (14 Inviolable Laws) & `STATISTICAL_PROTOCOL_V02.md`  

---

## 1. Scientific Context & Mandate

In EXP048, the $+14.0\text{ pp}$ headroom of $G_{\text{contrastive}}$ on `EleutherAI/pythia-160m` Layer 7 was deterministically reproduced on Seed-84 ($M_{\text{base}} = 60.0\% \to M_G = 74.0\%, b=7, c=0, p=0.00781$).

Before addressing questions of general cognitive control, **EXP049 subjects this empirical anchor to an immediate multi-seed adversarial challenge**. It evaluates whether the headroom holds consistently across 4 independent, unseen benchmark splits (Seeds 42, 168, 256, 512; $N=50$ each, total pooled $N=200$) or collapses as an artifact of Seed-84 sampling variance.

$$\boxed{\text{Does } G_{\text{contrastive}} \text{ deliver statistically significant headroom across independent random splits?}}$$

---

## 2. Invariant Protocol Locks

| Parameter | Protocol Lock | Epistemological Basis |
| :--- | :--- | :--- |
| **Model** | `EleutherAI/pythia-160m` | `[FACT]` Pre/post SHA-256 hash: `54c88fa4897785f2bd94b32d26de1f73f1052bcc42124d563d0cda96940de936` |
| **Target Layer** | Layer 7 (0-indexed = Block 7) | `[DEFINITION]` Locked from EXP048 |
| **Operator** | $G_{\text{contrastive}}$: SVD on mean-centered distractor span hidden states | `[DEFINITION]` Exact EXP048 formulation |
| **Subspace Rank** | $r = 2$ | `[DEFINITION]` SVD truncation rank |
| **Operator Strength** | $\alpha = 0.25$ | `[DEFINITION]` Projection subtraction factor |
| **Benchmark** | `BENCH-002-NL` (pure) | `[FACT]` 4 independent seeds: 42, 168, 256, 512 ($N=50$ each) |
| **Prompt Field** | `inst["base"]` | `[DEFINITION]` Fixed standard format |
| **Span Anchors** | `" Distractor:"` and `" Question:"` | `[DEFINITION]` Regex offset mapping |
| **Immutability Check** | $\Delta\theta = 0$ | `[FACT]` Verifying hash immutability |

---

## 3. Pre-Registered Hypotheses & Success Criteria

### 3.1 Primary Endpoint (Pooled Replication):
$$\Delta M_{\text{pooled}} = \frac{1}{4} \sum_{s \in \{42, 168, 256, 512\}} (M_{G, s} - M_{\text{base}, s})$$
- Pre-registered success threshold:
  $$\Delta M_{\text{pooled}} \ge +8.0\text{ pp} \quad \land \quad p_{\text{exact,pooled}} < 0.01 \quad \land \quad CI_{95\%}(\Delta M_{\text{pooled}}) > 0$$
  evaluated via exact paired binomial McNemar test and 10,000 bootstrap resamples.

### 3.2 Per-Seed Consistency Criterion:
- Across the 4 seeds, $\Delta M_s > 0$ on at least 3 out of 4 seeds.
- Per-seed corruption budget: $c_s \le 2$ on every individual seed.
- Net rescue ratio: Total rescued instances $b_{\text{total}} \ge 3 \times c_{\text{total}}$.

### 3.3 Negative Controls:
- **Ablation Control 1 (Random Subspace):** Replace $V_c$ with a random orthonormal basis $V_{\text{rand}} \in \mathbb{R}^{d \times 2}$. Must yield $\Delta M_{\text{rand}} \approx 0$ ($p > 0.05$).
- **Ablation Control 2 (Orthogonal Complement):** Project along the orthogonal complement $V_\perp$. Must fail to improve or actively degrade performance.

---

## 4. Pre-Registered Falsification Criteria

The core claim that $G_{\text{contrastive}}$ provides robust steering on Pythia-160M is **falsified** if:
1. $\Delta M_{\text{pooled}} \le 0$ or pooled McNemar $p \ge 0.05$.
2. $\Delta M_s \le 0$ on $\ge 2$ of the 4 independent seeds.
3. Total corruptions $c_{\text{total}} \ge b_{\text{total}}$ (the intervention introduces as much damage as benefit).
4. Random subspace control matches or outperforms $G_{\text{contrastive}}$ ($\Delta M_{\text{rand}} \ge \Delta M_G$).

---

## 5. Epistemological Interpretation Matrix

| Outcome | Epistemological Status | Interpretation |
| :--- | :--- | :--- |
| **All Criteria Passed** | `[OBSERVATION]` | $G_{\text{contrastive}}$ is a statistically invariant geometric steering direction in Pythia-160M for distractor suppression, ruling out seed artifact. Validates advancing to Cross-Task (EXP050) and Baseline Tournament (EXP052). |
| **Criteria Fails** | `[FALSIFIED]` | The EXP043/EXP048 finding was a statistical fluke on Seed-84. The contrastive subspace direction is not generalizable even across splits of the same synthetic task. |
