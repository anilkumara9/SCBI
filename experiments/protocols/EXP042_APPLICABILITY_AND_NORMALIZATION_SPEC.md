# EXP042: Self-Calibrating Generator Applicability & Normalized Routing Specification

## 1. Executive Summary & Epistemological Status
- **Experiment ID:** `EXP042`
- **Date:** 2026-09-12
- **Governing Law:** All 14 Inviolable Agent Laws in [`AGENTS.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/AGENTS.md) (specifically Law 4: Never Silently Shift Hypotheses, Law 6: Frozen Backbone, Law 7: Zero Data Leakage, Law 8: Never Delete Failed Experiments, Law 10: Never Claim Premature Novelty, Law 13: Deterministic Reproducibility, Law 14: Challenge Rather Than Defend).
- **Epistemological Status:** `[HYPOTHESIS]` Pre-registered benchmark testing a two-stage meta-controller architecture:
  $$\boxed{\text{Stage 1: Generator Applicability Filter } A(G_i \mid x, h) \longrightarrow \text{Stage 2: Architecture-Normalized Routing } q(G_i \mid \tilde{\mathbf{s}}(h_0), A)}$$
  evaluating whether applicability-gated abstention prevents cross-task degradation on `BENCH-004-TRANSFER`, and whether model-normalized state representations ($\tilde{\mathbf{s}}$) eliminate cross-architecture corruptions on GPT-2 124M under an exact $1.00$ forward pass budget ($\Delta\theta \equiv 0$).
- **Core Scientific Questions:**
  1. *Task Level:* Can an automated applicability estimate $A(G_i)$ detect when the candidate library contains no valid transformations ($M_{\mathrm{Oracle}} \approx M_I$), successfully defaulting to $G_{\mathrm{identity}}$ and eliminating false-positive degradation ($c=0$)?
  2. *Architecture Level:* Does normalizing representation observables against model-specific moments ($\tilde{\mathbf{s}} = (\mathbf{s} - \boldsymbol{\mu}) / \boldsymbol{\sigma}$) or percentile ranks eliminate catastrophic corruptions ($c=5 \to c \le 1$) when transferring the router across different architectures (Pythia-160M to GPT-2 124M)?

---

## 2. Theoretical Motivation: Two-Stage Meta-Control

EXP041 proved that zero-shot transfer failed for two completely different reasons:
- **Cross-Task Failure:** The candidate generator library lacked viable transformations for `BENCH-004-TRANSFER` ($M_{\mathrm{Oracle}} \le M_I = 52.0\%$). Routing among non-viable generators degraded accuracy to $48.0\%$.
- **Cross-Architecture Failure:** On GPT-2, candidate headroom existed ($68.0\%$, $+4.0$ pp, $b=2, c=0$), but raw Euclidean coordinate mismatch caused the Pythia router to pick corrupted modes ($c=5$), dropping accuracy to $56.0\%$.

Rather than attempting to train a complex black-box neural router, EXP042 decomposes inference-time representation control into two transparent questions:
1. **Can this problem be helped?** ($A(G_i \mid x, h) > \tau_A$)
2. **How should it be helped?** ($g^* = \arg\max_{G_i: A(G_i) > \tau_A} \hat{P}(\text{success} \mid G_i, \tilde{\mathbf{s}})$)

---

## 3. Mathematical Formulation

### Stage 1: Generator Applicability $A(G_i \mid x, h_0) \in [0, 1]$
Computed prior to intervention strictly from pre-intervention representations:
1. **$A(G_1)$ (Trajectory Flow Applicability):**
   $$A(G_1) = \mathbf{1}\left[\rho_{\mathrm{inter}} > 0.40 \ \wedge \ r_{\mathrm{flow}} \in [0.5, 3.0]\right]$$
   where $\rho_{\mathrm{inter}} = \cos(h_8 - h_6, h_6 - h_4)$. If the trajectory velocity is chaotic, decelerating, or inverted, $G_1$ is marked non-applicable ($A(G_1)=0$).
2. **$A(G_2)$ (Contextual Perturbation Applicability):**
   $$A(G_2) = \mathbf{1}\left[\frac{\|h_8 - h_8^{\mathrm{pert}}\|}{\|h_8\|} \in [0.02, 0.35]\right]$$
   If masking context yields negligible shift ($<0.02$) or catastrophic collapse ($>0.35$), $A(G_2)=0$.
3. **$A(G_3)$ (Attention Relational Applicability):**
   $$A(G_3) = \mathbf{1}\left[\text{Ratio}_{\mathrm{attn}} > 1.20 \ \wedge \ H_{\mathrm{attn}} < 0.90 H_{\max}\right]$$
   If attention is diffuse and unspecialized, attention relational rerouting cannot extract a contrastive subspace ($A(G_3)=0$).
4. **Abstention Decision:**
   If $\sum_i A(G_i) == 0$, the controller selects $G_{\mathrm{identity}}$ (no intervention, $h' = h$).

### Stage 2: Architecture-Normalized State Representation $\tilde{\mathbf{s}}(h_0)$
Four normalization regimes evaluated:
1. **Regime N1 (Raw Features):** Raw unnormalized vector $\mathbf{s}(h_0) \in \mathbb{R}^6$ (EXP040 baseline).
2. **Regime N2 (Model-Normalized Z-Scores):** $\tilde{\mathbf{s}} = (\mathbf{s} - \boldsymbol{\mu}_{\mathrm{model}}) / (\boldsymbol{\sigma}_{\mathrm{model}} + 10^{-8})$, where $(\boldsymbol{\mu}, \boldsymbol{\sigma})$ are computed over unlabeled baseline runs of that model.
3. **Regime N3 (Percentile / Rank Normalization):** Each feature is mapped to its empirical CDF percentile $\in [0, 1]$ relative to reference baseline activation distributions.
4. **Regime N4 (Relative Layer-Ratio):** Normalized against layer-mean norm: $\tilde{\mathbf{s}} = \mathbf{s} / \|h_8\|_F$.

---

## 4. Evaluated Test Conditions

### Test Split 1: Cross-Task Transfer (`BENCH-004-TRANSFER`, Pythia-160M, $N=50$, Seed 350)
1. **Baseline ($M_I$):** $52.0\%$.
2. **Oracle Multi-Generator Bound:** $52.0\%$.
3. **Un-Gated Raw Router (from EXP041):** $48.0\%$ ($-4.0$ pp, $b=0, c=2$).
4. **Applicability-Gated Router ($\pi_{\mathrm{applicability}}$):** Evaluated with Stage 1 filter to test whether it defaults to $G_{\mathrm{identity}}$ and eliminates the $c=2$ corruptions.

### Test Split 2: Cross-Architecture Transfer (`BENCH-002-NL`, GPT-2 124M, $N=50$, Seed 84)
1. **Baseline ($M_I$):** $64.0\%$.
2. **Oracle Multi-Generator Bound:** $68.0\%$ ($+4.0$ pp, $b=2, c=0$).
3. **Un-Normalized Raw Router (from EXP041):** $56.0\%$ ($-8.0$ pp, $b=1, c=5$).
4. **Model-Normalized Router (N2 Z-Score):** Standardized against GPT-2's internal activation moments.
5. **Rank-Normalized Router (N3 Percentile):** Standardized via empirical CDF rank.
6. **Applicability + Normalized Composite Router:** Stage 1 filter combined with Stage 2 normalized routing.

---

## 5. Pre-Registered Hypotheses & Falsification Criteria

### Hypothesis 1: Applicability Abstention Prevents Cross-Task Regressions ($H_{\mathrm{abstain}}$)
$$M(\pi_{\mathrm{applicability}} \mid \text{BENCH-004}) \ge 0.5200 \quad \text{and} \quad c = 0$$
- **Prediction:** Applicability filtering marks $A(G_i) = 0$ on non-viable tasks, defaulting to $G_{\mathrm{identity}}$ and eliminating the $c=2$ corruptions observed in EXP041.
- **Falsification Criterion:** If the applicability gate triggers destructive interventions ($c \ge 2$) on `BENCH-004`, the hypothesis is falsified.

### Hypothesis 2: Model-Normalized Architecture Transfer ($H_{\mathrm{norm\_transfer}}$)
$$M(\pi_{\mathrm{normalized}} \mid \text{GPT-2}) > 0.5600 \quad \text{and} \quad c \le 2$$
- **Prediction:** Standardizing features against GPT-2's internal activation moments prevents selecting corrupted modes $G_1/G_2$, recovering accuracy from $56\%$ towards baseline ($64\%$) or Oracle ($68\%$).
- **Falsification Criterion:** If model-normalized features fail to reduce corruptions below $c=3$, the hypothesis that z-score/rank normalization resolves cross-architecture router transfer is rejected.

---

## 6. Reproducibility & Ledger Output
- Pre/post SHA-256 parameter hashes verified for Pythia-160M and GPT-2 124M ($\Delta\theta \equiv 0$).
- Exactly $1.00$ forward pass per instance ($B_{\mathrm{eval}} = 1.00$).
- Results saved to `experiments/runs/EXP042_applicability/exp042_applicability_results.json`.
