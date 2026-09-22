# EXP036: Trajectory-Aware Representation Diagnostics & Rollback Control Specification

## 1. Executive Summary & Epistemological Status
- **Experiment ID:** `EXP036`
- **Date:** 2026-09-12
- **Governing Law:** All 14 Inviolable Agent Laws in [`AGENTS.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/AGENTS.md).
- **Epistemological Status:** `[HYPOTHESIS]` Pre-registered diagnostic benchmark investigating whether internal representation trajectory metrics (displacement, subspace alignment, entropy change) predict future representation gain versus representation corruption, and whether a trajectory-aware Rollback Controller can safely prune corrupted steps.
- **Evaluated Architecture:** `EleutherAI/pythia-160m` (12 layers, $d_{\mathrm{model}}=768$, Revision `e72e396263595503028d71243171317d7ae65463`).
- **Benchmark:** `BENCH-002-NL` ($N = 50$ confirmatory instances, Seed 84).
- **Frozen Backbone Guarantee:** Parameter SHA-256 hash verified invariant before and after inference: `54c88fa4897785f2bd94b32d26de1f73f1052bcc42124d563d0cda96940de936` ($\Delta\theta \equiv 0$).

---

## 2. Theoretical Motivation: Beyond Static Output Confidence

EXP032 proved:
$$\boxed{\text{Static activation variance } \neq \text{ Task-relevant intervention direction}}$$

EXP035 proved:
$$\boxed{\text{Output decision margin } \neq \text{ Latent-state stability}}$$

A scalar readout margin tells us current logit separation, but contains zero geometric information about whether a subsequent representation update will rescue an error or corrupt a stable state.

To prevent representation corruption ($c=3 \to 5$ in EXP034/035), the controller must observe **internal trajectory geometry**:
$$\boxed{\pi_t = f(h_t, \Delta h_t, \text{Alignment}_t, \Delta H_t) \longrightarrow \{\text{CONTINUE}, \text{STOP}, \text{ROLLBACK}\}}$$

$$\boxed{\textbf{Central Question: Can Internal Trajectory Geometry Predict Gain vs. Corruption and Guide Safe Rollback?}}$$

---

## 3. Internal Trajectory Diagnostic Metrics

For each transition from step $t-1$ to step $t$ ($t \in \{1, 2, 3\}$), compute:
1. **Relative Latent Displacement ($d_t$):**
   $$d_t = \frac{\|h_8^{(t)} - h_8^{(t-1)}\|_F}{\|h_8^{(t-1)}\|_F}$$
2. **Subspace Principal Angle / Directional Coherence ($\rho_t$):**
   Cosine similarity between successive update vectors:
   $$\rho_t = \frac{\langle \Delta h_8^{(t)}, \Delta h_8^{(t-1)} \rangle}{\|\Delta h_8^{(t)}\| \|\Delta h_8^{(t-1)}\|}$$
3. **Entropy Differential ($\Delta H_t$):**
   $$\Delta H_t = H(p^{(t)}) - H(p^{(t-1)})$$
4. **Target Attractor Directionality:**
   Projection energy ratio of the update along the target readout subspace.

### Ground-Truth Outcome Labels per Transition:
- **Gain ($G$):** Error at $t-1 \implies$ Correct at $t$ ($b$-event).
- **Corruption ($C$):** Correct at $t-1 \implies$ Error at $t$ ($c$-event).
- **Neutral ($N$):** State remains correct or remains incorrect.

---

## 4. Evaluated Controllers in EXP036

1. **Baseline ($M_I$):** Unintervened single pass ($M_I = 0.6000$).
2. **Supervised Reference ($G_{\mathrm{contrastive}}$):** Gold-standard token contrast ($+14.0$ pp, $p=0.0078$).
3. **Fixed $T=1$ Deliberation:** Single-step trajectory ($+6.0$ pp, $b=3, c=0$).
4. **Fixed $T=2$ Deliberation:** Ungated 2-step steering ($+4.0$ pp, $b=5, c=3$).
5. **Trajectory-Aware Rollback Controller ($\pi_{\mathrm{rollback}}$):**
   Execute Step 1 $\to$ Execute Step 2.
   Evaluate trajectory stability condition:
   $$\text{If } \rho_2 < \rho_{\mathrm{threshold}} \text{ or } d_2 > d_{\mathrm{threshold}} \implies \text{ROLLBACK to Step 1 logits!}$$
   $$\text{Else } \implies \text{ACCEPT Step 2 logits!}$$
   Grid of thresholds: $\rho_{\mathrm{thresh}} \in \{0.0, 0.2, 0.5, 0.8\}$, $d_{\mathrm{thresh}} \in \{0.10, 0.15, 0.20\}$.

---

## 5. Pre-Registered Hypotheses & Falsification Criteria

### Hypothesis 1: Trajectory Identifiability ($H_{\mathrm{ident}}$)
At least one internal trajectory metric ($d_t$, $\rho_t$, or $\Delta H_t$) exhibits statistically significant separation between Gain events ($G$) and Corruption events ($C$) (Mann-Whitney $U$ test, $p < 0.05$).

### Hypothesis 2: Rollback Gain Preservation ($H_{\mathrm{rollback}}$)
$$\Delta M(\pi_{\mathrm{rollback}}) \ge +8.0\text{ pp} \quad \text{AND} \quad c \le 1 \quad \text{AND} \quad p < 0.05 \text{ vs. } M_I$$
- **Predicted Outcome:** Rollback control rejects destabilizing Step 2 updates, reducing corruptions from $c=3$ down to $c \le 1$ while preserving at least 4 of the 5 rescues ($b \ge 4$), yielding $\ge +8.0$ pp net headroom ($68.0\%+$).
- **Falsification Criterion:** If all rollback conditions fail to achieve $\Delta M \ge +8.0$ pp or still exhibit $c \ge 3$, the hypothesis that trajectory-aware rollback solves representation corruption is rejected.

---

## 6. Statistical Protocol
- Pre/post parameter SHA-256 hash verified invariant ($\Delta\theta \equiv 0$).
- Mann-Whitney $U$ rank tests on diagnostic metric distributions ($G$ vs. $C$).
- 1,000-resample bootstrap 95% confidence intervals for $\Delta M$.
- Exact Paired McNemar tests vs. $M_I$ and vs. Fixed $T=1$.
- Output saved to `experiments/runs/EXP036_trajectory_rollback/exp036_trajectory_rollback_results.json`.
