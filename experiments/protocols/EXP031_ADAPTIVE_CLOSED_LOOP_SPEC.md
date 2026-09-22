# EXP031: Closed-Loop Adaptive Controller & Multi-Stage Cascaded Representation Control Specification

## 1. Executive Summary & Epistemological Status
- **Experiment ID:** `EXP031`
- **Date:** 2026-09-11
- **Governing Law:** All 14 Inviolable Agent Laws in [`AGENTS.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/AGENTS.md).
- **Epistemological Status:** `[HYPOTHESIS]` Pre-registered confirmatory benchmark evaluating Multi-Stage Cascaded Representation Control and Closed-Loop Adaptive Controller Policies on `EleutherAI/pythia-160m`.
- **Target Model:** `EleutherAI/pythia-160m` (12 layers, $d_{\mathrm{model}}=768$, Revision: `e72e396263595503028d71243171317d7ae65463`).
- **Benchmark:** `BENCH-002-NL` ($N = 50$ confirmatory instances, Seed 84).
- **Frozen Backbone Guarantee:** Parameter SHA-256 hash verified invariant before and after inference: `54c88fa4897785f2bd94b32d26de1f73f1052bcc42124d563d0cda96940de936` ($\Delta\theta \equiv 0$).

---

## 2. Research Question & Theoretical Motivation

EXP030 established that:
1. Viability is an **extended regional landscape**, with Layers 2, 4, 6, and 8 all possessing viable controller configurations ($\mathcal{V}(l) \neq \emptyset$).
2. A profound **Controller $\times$ Depth Interaction** exists:
   - Early representations ($l=2$) demand **selective token gating** ($C_2, \alpha=0.50 \implies +10.0$ pp) to protect diffuse semantic states.
   - Late representations ($l=8$) demand **ungated linear projection** ($C_0, \alpha=0.25 \implies +14.0$ pp) because token separation collapses while steering susceptibility peaks.
   - Terminal representations ($l \ge 10$) fail across all controllers ($\mathcal{V}(10) = \emptyset$).

In biological cognition, executive control is never a single-point impulse. It operates as a **hierarchical cascade**: early sensory-associative representations receive selective inhibitory filtering, while late pre-motor representations receive directional goal steering.

$$\boxed{\textbf{Central Question: Does Multi-Stage Cascaded Control } L2[C_2] \oplus L8[C_0] \textbf{ Produce Synergistic Headroom Exceeding Any Single Layer?}}$$

---

## 3. Mathematical Formulation of the Cascade Operator

Let $h_l \in \mathbb{R}^{T \times d}$ denote the residual stream representation after block $l$.  
A multi-stage cascade operator $\mathcal{T}_{\mathrm{cascade}}$ applies simultaneous, sequential hooks at layers $l_1 < l_2 < \dots < l_K$:

$$h'_{l_k} = h_{l_k} - \alpha_k \cdot g_k(h_{l_k}, V_k) \cdot P_{V_k} h_{l_k}, \quad k \in \{1, \dots, K\}$$

Where:
- $V_k \in \mathbb{R}^{d \times r}$ is the contrastive subspace basis invented for layer $l_k$.
- $P_{V_k} = V_k V_k^\top$ is the projection matrix.
- $g_k \in \{C_0, C_1, C_2\}$ is the controller policy assigned to stage $k$:
  - $C_0$: Ungated linear ($g_k \equiv 1$).
  - $C_1$: Soft sigmoid ($g_k = \sigma(d_t / \tau)$).
  - $C_2$: Contrastive hard gate ($g_k = \mathbf{1}\{d_t > 0\}$).

The transformed state $h'_{l_k}$ propagates through intermediate transformer blocks $l_k + 1 \dots l_{k+1}$ before encountering the subsequent intervention stage.

---

## 4. Factorial Experimental Conditions

Unintervened Baseline: $M_I$ on `BENCH-002-NL` ($N=50$, Seed 84).

### Set 1: Single-Stage Baselines (Champions from EXP030)
1. `L2_C2_a50`: Early Champion — Layer 2, Hard Gate $C_2$, $\alpha=0.50$ (Prior: $+10.0$ pp).
2. `L4_C0_a25`: Bottleneck Champion — Layer 4, Ungated $C_0$, $\alpha=0.25$ (Prior: $+8.0$ pp).
3. `L8_C0_a25`: Late Champion — Layer 8, Ungated $C_0$, $\alpha=0.25$ (Prior: $+14.0$ pp, global single-stage max).

### Set 2: Two-Stage Hierarchical Cascades
4. `Cascade_L2_C2_L8_C0_nominal`: **The Hierarchical Champion:** $L2[C_2, \alpha=0.50] \oplus L8[C_0, \alpha=0.25]$.
5. `Cascade_L2_C2_L8_C0_gentle`: $L2[C_2, \alpha=0.25] \oplus L8[C_0, \alpha=0.25]$ (Gentle early gate).
6. `Cascade_L2_C0_L8_C0`: $L2[C_0, \alpha=0.25] \oplus L8[C_0, \alpha=0.25]$ (Ungated at both stages).
7. `Cascade_L4_C0_L8_C0`: $L4[C_0, \alpha=0.25] \oplus L8[C_0, \alpha=0.25]$ (Bottleneck to Late).

### Set 3: Tri-Stage Deep Cascade
8. `Cascade_TriStage_L2_L4_L8`: $L2[C_2, \alpha=0.25] \oplus L4[C_0, \alpha=0.15] \oplus L8[C_0, \alpha=0.25]$.

### Set 4: Closed-Loop Dynamic Adaptive Controller ($\mathcal{C}^*_{\mathrm{dynamic}}$)
9. `Adaptive_Dynamic_Policy`: An autonomous runtime function:
   $$g^*(l) = \begin{cases} C_2 \ (\alpha=0.50), & l \le 3 \\ C_0 \ (\alpha=0.25), & 4 \le l \le 8 \\ \text{None}, & l \ge 9 \end{cases}$$
   Evaluated as a dynamic policy selection per layer.

---

## 5. Pre-Registered Hypotheses & Falsification Criteria

### Hypothesis 1: Multi-Stage Synergy ($H_{\mathrm{synergy}}$)
$$\Delta M\big(L2[C_2] \oplus L8[C_0]\big) > \max\big(\Delta M(L2[C_2]), \; \Delta M(L8[C_0])\big) = \mathbf{+14.0\text{ pp}}$$
- **Predicted Outcome:** Early selective gating ($L2$) attenuates distractor noise before the 1D bottleneck ($L4$), leaving late representations ($L8$) primed for directional attention steering. Accuracy reaches $\ge \mathbf{76.0\%}$ ($\Delta M \ge \mathbf{+16.0\text{ pp}}$).
- **Falsification Criterion:** If $\Delta M(L2 \oplus L8) \le +14.0$ pp, the multi-stage synergy hypothesis is rejected.

### Hypothesis 2: Non-Destructive Invariance ($H_{\mathrm{stability}}$)
$$\Delta\log p(y_{\mathrm{correct}}) > 0 \quad \text{and} \quad \text{Vocabulary Overlap} \ge 85.0\%$$
- Multi-stage intervention maintains representation stability without cumulative logit corruption.

---

## 6. Verification & Reproducibility Protocol
- Model parameters hashed before and after execution.
- Deterministic random seeding ($S=84$).
- Raw prediction files written to `experiments/runs/EXP031_adaptive/exp031_cascade_results.json`.
