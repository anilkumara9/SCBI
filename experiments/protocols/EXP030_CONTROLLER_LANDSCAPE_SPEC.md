# Protocol Specification: EXP030 — Controller vs. Stage Viability Landscape Matrix

## 1. Executive Summary & Purpose

- **Experiment ID:** `EXP030`
- **Model Audited:** `EleutherAI/pythia-160m` (12 layers, $d_{\mathrm{model}}=768$, Revision: `e72e396263595503028d71243171317d7ae65463`).
- **Benchmark:** `BENCH-002-NL` ($N=50$, Seed 84).
- **Core Scientific Question:**
  > **Is intermediate representation viability an immutable property of depth, or is it governed by an interaction between depth ($l$), controller gating policy ($g$), and intervention strength ($\alpha$)?**
- **Epistemological Status of the Tri-Partite Model:** The Tri-Partite Architecture ($\text{Search} + \text{Stage} + \text{Control}$) is treated strictly as a **working hypothesis awaiting empirical falsification**, not an established theorem.

---

## 2. Inviolable Governance Locks & Protocol Boundaries

1. **Law 1 & 6 (Frozen Backbone):** Parameter SHA-256 hash verified before and after inference (`54c88fa4897785f2bd94b32d26de1f73f1052bcc42124d563d0cda96940de936`, $\Delta\theta \equiv 0$).
2. **Law 7 (Zero Data Leakage):** Candidate representations and gating thresholds are computed strictly from the prompt representation itself; test set labels $y$ are isolated from the intervention loop.
3. **Law 9 & 14 (No Goalpost Shifting / Falsifiable Hypotheses):**
   - All 45 cells ($5\text{ layers} \times 3\text{ controllers} \times 3\text{ strengths}$) are evaluated against the exact same unintervened baseline $M_I$.
   - Primary endpoints ($\Delta M$, $\Delta\log p(y_{\mathrm{correct}})$) and bootstrap confidence intervals are pre-registered before execution.

---

## 3. Factorial Design: 5 Depths × 3 Controllers × 3 Strengths (45 Conditions)

Every cell evaluates an intervention on the residual stream at layer $l$:
$$h_l' = h_l - \alpha \cdot g_t \cdot \left(P_{V} h_l\right)$$
where $P_V = V V^\top$ is the rank-2 contrastive subspace extracted from the distractor representation.

### Dimension 1: Depth Grid ($l \in \{2, 4, 6, 8, 10\}$)
- $l=2$ ($\lambda \approx 0.167$): Early plastic stage.
- $l=4$ ($\lambda \approx 0.333$): Known viable stage from EXP027/029.
- $l=6$ ($\lambda \approx 0.500$): Mid-network stage.
- $l=8$ ($\lambda \approx 0.667$): Late stage (failed under hard gate in EXP027; rescued under linear in EXP029).
- $l=10$ ($\lambda \approx 0.833$): Pre-unembedding stage.

### Dimension 2: Controller Gating Policy ($g \in \{C0, C1, C2\}$)
1. **$C0$ (Ungated Linear Projection):**
   $$g_t \equiv 1.0 \quad \forall t$$
   Intervenes uniformly across all token positions.
2. **$C1$ (Soft Sigmoid Gate):**
   $$g_t = \sigma\left(\frac{d_t - \tau}{\tau_{\mathrm{scale}}}\right), \quad d_t = \|P_V h_{l,t}\|_2 - \|P_{V_+} h_{l,t}\|_2$$
   where $\tau = \operatorname{median}(d)$ and $\tau_{\mathrm{scale}} = \operatorname{std}(d) + 10^{-6}$.
3. **$C2$ (Contrastive Hard Gate, $O5$):**
   $$g_t = \mathbf{1}[d_t > 0.0]$$
   Standard SCBI hard gating baseline from EXP022–EXP028.

### Dimension 3: Intervention Strength Sweep ($\alpha \in \{0.10, 0.25, 0.50\}$)
- $\alpha = 0.10$: Gentle perturbation.
- $\alpha = 0.25$: Standard repository baseline.
- $\alpha = 0.50$: Aggressive perturbation.

---

## 4. Pre-Registered Definitions & Primary Endpoints

### 4.1 Primary & Secondary Endpoints
- **Primary Endpoint:** $\Delta M(l, g, \alpha) = M(l, g, \alpha) - M_I$ (Top-1 exact match difference against the unintervened baseline).
- **Secondary Endpoint:** Mean target token log-probability difference:
  $$\Delta\log p(l, g, \alpha) = \frac{1}{N}\sum_{i=1}^N \left(\log p_i^{\mathrm{intervened}}(y_i) - \log p_i^{\mathrm{base}}(y_i)\right)$$
- **Statistical Uncertainty:** 1,000-resample bootstrap 95% confidence intervals for $\Delta M$ and $\Delta\log p$ for every cell.

### 4.2 Pre-Registered Definition of a "Viability Region"
> `[DEFINITION]` **Viability Region:** A contiguous set of $\ge 2$ evaluated layers $\{l_j, l_{j+1}\}$ in which the best pre-registered controller/strength combination produces strictly positive headroom:
> $$\Delta M(l) > 0 \quad \text{and} \quad \Delta\log p(l) > 0 \quad (\text{with } 95\%\text{ bootstrap CI excluding zero for at least one metric})$$

### 4.3 Definition of the Viability Landscape $\mathcal{V}(l)$
For each layer $l$, the viability set is defined as:
$$\mathcal{V}(l) = \left\{(g, \alpha) \in \{C0, C1, C2\} \times \{0.10, 0.25, 0.50\} : \Delta M(l, g, \alpha) > 0 \text{ and } \Delta\log p(l, g, \alpha) > 0\right\}$$

---

## 5. Tri-State Falsification Decision Tree

1. **Outcome A (Broad Viability Across Depths — Tri-Partite Model Strongly Supported):**
   - If $\ge 4$ of the 5 evaluated layers exhibit non-empty viability sets ($|\mathcal{V}(l)| \ge 1$), the hypothesis that SCBI is constrained to a narrow isolated layer is **falsified**. Efficacy is confirmed as an interaction between representation depth and controller policy.
2. **Outcome B (Narrow Depth Primacy — Stage Selection Fundamental):**
   - If only Layer 4 (or an isolated contiguous pair) produces positive headroom regardless of controller or strength ($|\mathcal{V}(l)| = \emptyset$ for $l \notin \{4, 6\}$), the tri-partite controller hypothesis is **falsified**. Pure architectural depth remains the fundamental constraint.
3. **Outcome C (Structured Controller-Depth Interaction — Adaptive Control Law):**
   - If the optimal controller $g^*(l) = \arg\max_{g} \Delta M(l, g, \alpha^*)$ systematically shifts with depth (e.g. Early layers favor Soft/Hard gating $C1/C2$, while Late layers favor Ungated Linear $C0$), this establishes that **gating requirements invert across the depth hierarchy**.
