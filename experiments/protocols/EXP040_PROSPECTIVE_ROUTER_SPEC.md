# EXP040: Prospective Generator Router Specification

## 1. Executive Summary & Epistemological Status
- **Experiment ID:** `EXP040`
- **Date:** 2026-09-12
- **Governing Law:** All 14 Inviolable Agent Laws in [`AGENTS.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/AGENTS.md) (specifically Law 7: Zero Data Leakage, Law 9: No Cherry-Picking, Law 13: Deterministic Reproducibility).
- **Epistemological Status:** `[HYPOTHESIS]` Pre-registered confirmatory benchmark evaluating whether a prospective generator router $q_\phi(g \mid h_0)$—calibrated on an independent training split and completely frozen before evaluation—can autonomously predict the optimal representation generator family ($G_1$: Trajectory, $G_2$: Context, $G_3$: Attention) on an unseen, held-out test split, recovering a substantial fraction of the Oracle multi-generator ceiling under an exact $1.0$ forward pass budget ($\Delta\theta \equiv 0$).
- **Evaluated Architecture:** `EleutherAI/pythia-160m` (12 layers, $d_{\mathrm{model}}=768$, Revision `e72e396263595503028d71243171317d7ae65463`).
- **Benchmark Splits:**
  - **Calibration / Training Split:** `BENCH-002-NL` ($N_{\mathrm{calib}} = 50$, Seed 123) used exclusively to fit router parameters $\phi$.
  - **Locked Confirmatory Test Split:** `BENCH-002-NL` ($N_{\mathrm{test}} = 50$, Seed 84) evaluated strictly with frozen router $\phi$ without label leakage.
- **Frozen Backbone Guarantee:** Pre/post parameter SHA-256 hash verified invariant: `54c88fa4897785f2bd94b32d26de1f73f1052bcc42124d563d0cda96940de936`.

---

## 2. Theoretical Motivation: From Spectral Search to Computational Modes

EXP039 established a clean scientific division:
1. **Heterogeneous Generator Complementarity Confirmed:** $G_1$ (Trajectory), $G_2$ (Contextual), and $G_3$ (Attention) rescue non-overlapping failure instances (Union $N=5$, Inst 34 rescued exclusively by $G_3$).
2. **Oracle Multi-Generator Bound:** Under hindsight selection, the pool achieves $70.0\%$ accuracy ($+10.0$ pp, $b=5, c=0, p=0.03125$).
3. **The Open Gap:** The $70.0\%$ mark represents an *Oracle upper bound*, not an autonomous SCBI result; the autonomous policy remained at $66.0\%$.

Rather than searching candidates sequentially or treating generators as arbitrary mathematical classes, EXP040 conceptualizes the generators as **distinct computational modes**:
- $G_1 \longrightarrow \text{Trajectory Correction (inter-layer forward flow)}$
- $G_2 \longrightarrow \text{Contextual Reinterpretation (premise perturbation stabilization)}$
- $G_3 \longrightarrow \text{Attention Rerouting (head allocation contrast)}$

The objective is to evaluate:
$$\boxed{\textbf{Can an unseen, label-free router recover a substantial fraction of the 70\% Oracle ceiling?}}$$

---

## 3. Router Architecture & Probability Estimation ($P(\text{success} \mid g, h_0)$)

To avoid forcing brittle discrete categorization, the router estimates the probability of success for each generator:
$$\hat{P}(g \text{ succeeds} \mid \mathbf{s}(h_0)) = \sigma(\mathbf{w}_g^\top \mathbf{s}(h_0) + b_g)$$
and selects the generator maximizing expected success:
$$g^* = \arg\max_{g \in \{G_1, G_2, G_3\}} \hat{P}(g \text{ succeeds} \mid \mathbf{s}(h_0))$$

### Pre-Intervention Feature Vector $\mathbf{s}(h_0) \in \mathbb{R}^6$:
Computed strictly at the end of the unperturbed forward pass ($T=0$) before any candidate intervention:
1. **Flow Velocity Ratio:** $r_{\mathrm{flow}} = \|h_8^{(0)} - h_6^{(0)}\| / (\|h_6^{(0)} - h_4^{(0)}\| + 10^{-8})$
2. **Context-to-Query Attention Entropy:** $H_{\mathrm{attn}} = -\sum_i a_i \log(a_i + 10^{-8})$ at Layer 8
3. **Premise vs. Distractor Attention Ratio:** $\text{Ratio}_{\mathrm{attn}} = \sum_{t \in \mathrm{prem}} a_t / (\sum_{t \in \mathrm{dist}} a_t + 10^{-8})$
4. **Normalized Residual Energy:** $E_{\mathrm{res}} = \|h_8^{(0)} - \bar{h}_8^{(0)}\|_F / \|h_8^{(0)}\|_F$
5. **Context Premise Cosine Similarity:** $S_{\mathrm{context}} = \langle h_8^{(0)}[-1], \bar{h}_{8,\mathrm{prem}}^{(0)} \rangle / (\|h_8^{(0)}[-1]\| \|\bar{h}_{8,\mathrm{prem}}^{(0)}\|)$
6. **Clause Subspace Margin:** $M_{\mathrm{clause}} = \|P_{\mathcal{V}_{\mathrm{prem}}} h_8^{(0)}[-1]\|_2 - \|P_{\mathcal{V}_{\mathrm{dist}}} h_8^{(0)}[-1]\|_2$

---

## 4. Anti-Leakage Protocol & Two-Phase Pipeline

```text
               PHASE A: ROUTER CALIBRATION (Seed 123, N=50)
                                    │
                Extract s(h_0) on Unintervened Forward Pass
                Evaluate G_1, G_2, G_3 Outcomes to Generate Targets
                Fit Probabilistic Router W_g, b_g via Calibrated Logistic Regression
                                    │
                                    ▼
                         LOCK ROUTER PARAMETERS φ*
                                    │
               PHASE B: CONFIRMATORY EVALUATION (Seed 84, N=50)
                                    │
                Extract s(h_0) on Fresh Held-Out Instances
                Apply Frozen Router: g* = argmax P(success | g, s(h_0))
                Execute Single-Pass Intervention using G_g* (B_eval = 1.0)
                                    │
                                    ▼
                Compute Held-Out Accuracy, McNemar p, and Headroom
```

---

## 5. Evaluated Conditions on Confirmatory Test Set ($N=50$, Seed 84)

1. **Condition 1 (Baseline $M_I$):** Unintervened single pass ($M_I = 0.6000$).
2. **Condition 2 ($G_{\mathrm{contrastive}}$):** Supervised reference baseline ($+14.0$ pp, $p=0.0078$).
3. **Condition 3 (Static $G_1$):** Always use Inter-Layer Trajectory Flow ($1.0$ pass).
4. **Condition 4 (Static $G_2$):** Always use Contextual Perturbation ($1.0$ pass).
5. **Condition 5 (Static $G_3$):** Always use Attention Relational Routing ($1.0$ pass).
6. **Condition 6 (Oracle Multi-Generator Bound):** Hindsight best generator per test instance ($70.0\%$, $+10.0$ pp, $p=0.03125$).
7. **Condition 7 (Prospective Router $\pi_{\mathrm{router}}$):** Autonomous generator selection via frozen $\phi^*$ using only $T=0$ pre-intervention features ($1.0$ pass).

---

## 6. Pre-Registered Hypotheses & Falsification Criteria

### Hypothesis 1: Held-Out Autonomous Headroom Recovery ($H_{\mathrm{router}}$)
$$M(\pi_{\mathrm{router}}) > \max(M(G_1), M(G_2), M(G_3)) \quad \text{on held-out test split under } B_{\mathrm{eval}} = 1.0$$
- **Prediction:** The frozen prospective router achieves $M \ge 0.6800$ ($+8.0$ pp headroom, $c \le 1$), recovering at least half of the Oracle headroom gap ($66\% \to 70\%$) on the held-out test set without exceeding $1.0$ forward pass per instance.
- **Falsification Criterion:** If the frozen router achieves test accuracy $\le 0.6600$ or suffers regressions ($c \ge 2$), the hypothesis that pre-intervention representation observables can prospectively route generator selection is rejected.

---

## 7. Statistical Protocol
- Pre/post parameter SHA-256 hash verified invariant ($\Delta\theta \equiv 0$).
- 1,000-resample bootstrap 95% confidence intervals.
- Exact Paired McNemar tests vs. $M_I$ and vs. Static $G_1$.
- Output saved to `experiments/runs/EXP040_prospective_router/exp040_prospective_router_results.json`.
