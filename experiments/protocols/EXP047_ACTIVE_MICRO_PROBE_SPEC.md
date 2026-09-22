# EXP047: Active Inference Causal Micro-Probing Protocol Specification

## 1. Executive Summary & Epistemological Status
- **Experiment ID:** `EXP047`
- **Date:** 2026-09-12
- **Lead Roles:**
  - **Research Theorist / Scientific Strategist / Skeptical Reviewer:** Formulates hypotheses, derives mathematical questions, challenges conclusions, sets falsification thresholds.
  - **Experimental Scientist / Research Engineer (Antigravity):** Implements pre-registered protocols, writes modular verified code, runs experiments, analyzes raw outputs with statistical sobriety, guarantees $\Delta\theta \equiv 0$, identifies implementation phenomena.
- **Governing Standard:** All 14 Inviolable Agent Laws in [`AGENTS.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/AGENTS.md) (specifically Law 2: Never Invent Results, Law 4: Never Silently Shift Hypotheses, Law 6: Frozen Backbone $\Delta\theta \equiv 0$, Law 7: Zero Data Leakage, Law 9: No Cherry-Picking, Law 10: Never Claim Premature Novelty, Law 13: Deterministic Reproducibility, Law 14: Challenge Rather Than Defend).
- **Codification Anchor:** [`theory/README.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/theory/README.md) §105–§106.
- **Core Scientific Question:**
  $$\boxed{\textbf{Can a tiny, reversible, compute-bounded micro-probe reveal whether an internal representation intervention is likely to help, prior to full execution?}}$$

---

## 2. Scientific Motivation & The Elimination of Passive Observables

### 2.1 The Completed Elimination Chain
Across 46 benchmarks, every attempt to diagnose or control representations using passive, static snapshots has been falsified:
1. **Static Activation Variance / Covariance:** Insufficient (EXP032: energy perturbation degraded accuracy to $56\%$).
2. **Output Margin Stopping:** Insufficient (EXP035: blind to latent drift, $c=3$).
3. **Kinematic Trajectory Smoothness:** Insufficient (EXP036: smooth drift into corrupt attractors).
4. **Input Feature Normalization:** Insufficient (EXP042: fails to resolve cross-architecture causal mismatch).
5. **Passive Global Pre-Intervention Observables:** Insufficient (EXP046: AUC = 0.50 across all 4 feature subsets).

### 2.2 Core Epistemic Distinction
$$\boxed{\textbf{Observable Uncertainty } \neq \textbf{Action Utility}} \qquad \text{and} \qquad \boxed{\textbf{Representational Geometry } \neq \textbf{Intervention Usefulness}}$$
High predictive entropy or narrow margins demonstrate that the unsteered model is uncertain, but carry zero information about whether an internal representation intervention will successfully rescue the instance.

### 2.3 The Active Inference Paradigm Shift
The causal receptivity of a neural trajectory cannot be inferred from a passive snapshot without perturbing the system. We transition the controller from passive classification ($x \to a^*$) to **Active Inference Causal Probing**:
$$\boxed{
x \longrightarrow \text{Reversible Micro-Probe } \epsilon G(h) \longrightarrow \text{Observe Local Response } (\Delta \mathcal{M}_{12}, d_{\mathrm{disp}}, \kappa) \longrightarrow \text{Commit or Rollback}
}$$

---

## 3. Mathematical Specification of the Micro-Probe Architecture

### 3.1 Model & Split-Pass Caching
- **Foundation Model:** `EleutherAI/pythia-160m` ($L=12$ layers, $d_{\mathrm{model}}=768$, parameter SHA-256 verified before and after inference).
- **Intervention Layer:** $l^* = 8$.
- **Full Intervention Operator:** Audited operator $G^*$ at scale $\alpha = 0.25$.
- **Micro-Probe Scale:** $\epsilon = \rho \cdot \alpha = 0.20 \cdot 0.25 = 0.05$.

### 3.2 Split-Pass Execution & Compute Cost Accounting
1. **Prefix Forward Pass (Layers $1 \dots l^*$):**
   $$h_{l^*} = \text{Forward}_{1 \dots l^*}(x)$$
   Cache baseline hidden state $h_{l^*}^{(0)} = h_{l^*}$.
   *Compute cost:* $C_{\mathrm{prefix}} = \frac{l^*}{L} = \frac{8}{12} \approx 0.67$ forward pass.

2. **Baseline Forward Continuation (Layers $l^*+1 \dots L$):**
   $$z^{(0)} = \text{Unembed}\Big(\text{Forward}_{l^*+1 \dots L}(h_{l^*}^{(0)})\Big)$$
   *Compute cost:* $C_{\mathrm{base\_cont}} = \frac{4}{12} \approx 0.33$ forward pass.
   *Cumulative compute so far:* $0.67 + 0.33 = 1.00$ forward pass.

3. **Reversible Micro-Probe Pass (Layers $l^*+1 \dots L$):**
   Inject micro-perturbation:
   $$\tilde{h}_{l^*}^{(\epsilon)} = h_{l^*}^{(0)} + \epsilon \cdot G^*(h_{l^*}^{(0)})$$
   Evaluate probe trajectory:
   $$z^{(\epsilon)} = \text{Unembed}\Big(\text{Forward}_{l^*+1 \dots L}(\tilde{h}_{l^*}^{(\epsilon)})\Big)$$
   *Compute cost:* $C_{\mathrm{probe}} = \frac{4}{12} \approx 0.33$ forward pass.
   *Cumulative compute through probe evaluation:* $1.00 + 0.33 = 1.33$ forward passes.

### 3.3 Observable Causal Response Metrics ($\mathcal{O}_{\mathrm{probe}}$)
Computed without access to ground truth labels:
1. **Differential Margin Expansion ($\Delta \mathcal{M}_{12}$):**
   $$\mathcal{M}_{12}(z) = z_{(1)} - z_{(2)}$$
   $$\Delta \mathcal{M}_{12} = \mathcal{M}_{12}(z^{(\epsilon)}) - \mathcal{M}_{12}(z^{(0)})$$
2. **Trajectory Displacement / Strain ($d_{\mathrm{disp}}$):**
   $$d_{\mathrm{disp}} = \frac{\| h_L^{(\epsilon)} - h_L^{(0)} \|_2}{\| h_L^{(0)} \|_2 + 10^{-6}}$$
3. **Local Controllability Ratio ($\kappa$):**
   $$\kappa(G; x) = \frac{\Delta \mathcal{M}_{12}}{d_{\mathrm{disp}} + 10^{-4}}$$
   Measures margin expansion per unit of trajectory strain.
4. **Predictive Vocabulary Entropy Shift ($\Delta H_{\mathrm{vocab}}$):**
   $$\Delta H_{\mathrm{vocab}} = H_{\mathrm{vocab}}(z^{(\epsilon)}) - H_{\mathrm{vocab}}(z^{(0)})$$

### 3.4 The Commit / Rollback Gating Policy
$$\pi_{\mathrm{probe}}(x) = \begin{cases}
\textbf{Commit } (\mathcal{R}): & \text{if } \kappa(G; x) > \tau_{\mathrm{commit}} \text{ and } \Delta H_{\mathrm{vocab}} \le 0 \\
\textbf{Rollback } (\emptyset): & \text{otherwise}
\end{cases}$$

- **If Commit ($\mathcal{R}$):**
  Apply full intervention:
  $$\tilde{h}_{l^*}^{(\alpha)} = h_{l^*}^{(0)} + \alpha \cdot G^*(h_{l^*}^{(0)})$$
  Evaluate final prediction:
  $$z^* = z^{(\alpha)} = \text{Unembed}\Big(\text{Forward}_{l^*+1 \dots L}(\tilde{h}_{l^*}^{(\alpha)})\Big)$$
  *Instance Compute:* $0.67 + 0.33 + 0.33 + 0.33 = 1.67$ forward passes.
- **If Rollback ($\emptyset$):**
  Discard micro-probe state; return cached baseline output $z^* = z^{(0)}$.
  *Instance Compute:* $1.33$ forward passes (includes the probe).

---

## 4. Dataset Splits & Calibration Protocol

### 4.1 Calibration Split ($\mathcal{D}_{\mathrm{calib}}$, $N_{\mathrm{calib}} = 30$)
- 15 instances from `BENCH-002-NL` (Seed 123).
- 15 instances from `BENCH-004-TRANSFER` (Seed 250).
- **Procedure:** Run micro-probe and measure $\kappa$ and $\Delta H_{\mathrm{vocab}}$ on $\mathcal{D}_{\mathrm{calib}}$. Find the threshold $\tau_{\mathrm{commit}}^*$ that maximizes net utility on calibration instances without observing test labels.
- **Freeze Lock:** Save the calibrated threshold and parameters to `exp047_probe_calibration.json` with SHA-256 hash before running the test set.

### 4.2 Confirmatory Test Split ($\mathcal{D}_{\mathrm{test}}$, $N_{\mathrm{test}} = 100$)
- 50 held-out instances from `BENCH-002-NL` (Seed 84).
- 50 held-out instances from `BENCH-004-TRANSFER` (Seed 350).

---

## 5. Pre-Registered Utility Function & Policies

### 5.1 Utility Function
$$U(a \mid x) = \operatorname{Correct}(a \mid x) - \lambda \cdot C(a) - \gamma \cdot \mathbf{1}[\text{Corrupted}(a \mid x)]$$
- $\lambda = 0.05$ (Compute penalty).
- $\gamma = 1.00$ (Corruption penalty).
- $C(\emptyset) = 1.00$.
- $C(\mathcal{R}_{\mathrm{blind}}) = 1.05$.
- $C(\pi_{\mathrm{probe}}) = 1.33$ (if rolled back) / $1.67$ (if committed full).

### 5.2 Evaluated Policies
1. $\pi_{\mathrm{always}\text{-}\emptyset}$: Unsteered baseline.
2. $\pi_{\mathrm{always}\text{-}\mathcal{R}}$: Blind full intervention.
3. $\pi_{\mathrm{passive}\text{-}\mathrm{diag}}$: EXP046 static pre-intervention classifier.
4. $\pi_{\mathrm{active}\text{-}\mathrm{probe}}$: Proposed active micro-probe with commit/rollback.
5. $\pi_{\mathrm{oracle}}$: Retrospective instance-optimal upper bound.

---

## 6. Pre-Registered Hypotheses & Tri-State Outcomes

| Outcome | Quantitative Criteria | Scientific Interpretation |
| :--- | :--- | :--- |
| **Outcome 1: Active Inference Confirmed** | $\mathrm{AUC}(\kappa_{\mathrm{probe}}) \ge 0.70$, $\bar{U}(\pi_{\mathrm{probe}}) > \bar{U}(\pi_{\emptyset})$, $c = 0$, $p_{\mathrm{McNemar}} \le 0.05$ | **Major Breakthrough:** Reversible micro-probing breaks the passive observable boundary, providing reliable causal signal for prospective computation control. |
| **Outcome 2: Safe Selective Control (Partial Efficacy)** | $\mathrm{AUC}(\kappa_{\mathrm{probe}}) \ge 0.65$, $\bar{U}(\pi_{\mathrm{probe}}) > \bar{U}(\pi_{\emptyset})$, $c = 0$, $p > 0.05$ | Active probing safely avoids corruptions and improves net utility, but statistical power is insufficient for definitive confirmation. |
| **Outcome 3: Conservative Inertia (Under-Triggering)** | Rollback rate $> 95\%$, $\bar{U}(\pi_{\mathrm{probe}}) \approx \bar{U}(\pi_{\emptyset})$, $c = 0$ | The probe is overly conservative, defaulting to baseline abstention and missing viable rescues. |
| **Outcome 4: Active Probing Refuted** | $\mathrm{AUC}(\kappa_{\mathrm{probe}}) \le 0.55$ or $\bar{U}(\pi_{\mathrm{probe}}) \le \bar{U}(\pi_{\emptyset})$ or $c \ge 2$ | **Falsification:** Even dynamic micro-probing fails to reveal intervention utility prior to full execution. |
