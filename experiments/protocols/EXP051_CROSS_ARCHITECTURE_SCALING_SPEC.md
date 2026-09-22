# EXP051 Protocol Specification: Cross-Architecture & Scaling Transfer Test

**Status:** PRE-REGISTERED  
**Date:** 2026-09-21  
**Predecessor Experiments:** EXP048, EXP049, EXP050  
**Governing Standard:** `AGENTS.md` (14 Inviolable Laws) & `STATISTICAL_PROTOCOL_V02.md`  

---

## 1. Scientific Context & Mandate

To qualify as a fundamental neural computation mechanism, temporary basis construction must transfer across model families (different tokenizers, positional embeddings, normalization schemes) and model sizes.

**EXP051 tests the intervention across 3 architectural families and a 20x parameter scaling range:**
- **Family 1 (Pythia):** `EleutherAI/pythia-70m`, `pythia-160m`, `pythia-410m`, `pythia-1.4b` (RoPE embeddings, LayerNorm)
- **Family 2 (GPT-2):** `gpt2` (124M), `gpt2-medium` (355M) (Learned absolute positional embeddings)
- **Family 3 (Qwen 2.5):** `Qwen/Qwen2.5-0.5B`, `Qwen2.5-1.5B` (SwiGLU, RMSNorm)

$$\boxed{\text{Does the basis intervention mechanism operate across model architectures and scaling regimes?}}$$

---

## 2. Invariant Protocol Locks

| Parameter | Protocol Lock | Epistemological Basis |
| :--- | :--- | :--- |
| **Normalized Layer Depth** | $l / L \approx 0.58 - 0.67$ (rounded to nearest integer layer) | `[DEFINITION]` Standardized middle-layer depth |
| **Subspace Rank** | $r = 2$ | `[DEFINITION]` Subspace dimensionality |
| **Dynamic Scaling** | $\alpha_{\text{eff}} = \alpha_0 \cdot \frac{\bar{\sigma}_{\text{Pythia-160M}}}{\sigma_l}$ | `[DEFINITION]` Variance-normalized scale factor |
| **Benchmark** | `BENCH-002-NL` Seed-84 ($N=50$) | `[FACT]` Standardized evaluation instances |
| **Backbone Immutability** | SHA-256 verified per model ($\Delta\theta = 0$) | `[FACT]` Parameter immutability |

---

## 3. Pre-Registered Hypotheses & Success Criteria

### 3.1 Architectural Transfer Hypothesis:
$$\Delta M_{\text{family}} > 0 \quad \text{for each family } \in \{\text{Pythia}, \text{GPT-2}, \text{Qwen}\}$$
At least one model in each of the 3 families must demonstrate statistically significant accuracy gain ($p_{\text{McNemar}} < 0.05$).

### 3.2 Scaling Monotonicity Hypothesis:
Within the Pythia family ($70\text{M} \to 1.4\text{B}$):
$$M_G(1.4\text{B}) \ge M_G(410\text{M}) \ge M_G(160\text{M}) \ge M_G(70\text{M})$$
The absolute intervention performance must scale monotonically with base model capacity.

---

## 4. Pre-Registered Falsification Criteria

The generality of the mechanism is **falsified** if:
1. $G_{\text{contrastive}}$ fails completely ($\Delta M \le 0$) across all models in Family 2 (GPT-2) and Family 3 (Qwen).
2. The intervention collapses base performance ($\Delta M < -5\text{ pp}$) on larger models ($410\text{M}$ or $1.4\text{B}$).
3. Random subspace projection performs equivalently to $G_{\text{contrastive}}$ on other architectures.

---

## 5. Epistemological Interpretation Matrix

| Outcome | Epistemological Status | Interpretation |
| :--- | :--- | :--- |
| **Transfers across all 3 families** | `[OBSERVATION]` | The basis invention mechanism reflects an architecture-invariant principle of autoregressive transformer representation geometry. |
| **Works only on Pythia** | `[OBSERVATION]` | The effect is an architectural quirk specific to the Pythia pretraining recipe or attention structure. |
