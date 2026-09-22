# EXP045: First-Principles Problem-Specific Operator Invention Protocol Specification

## 1. Executive Summary & Epistemological Status
- **Experiment ID:** `EXP045`
- **Date:** 2026-09-12
- **Lead Roles:**
  - **Research Theorist / Scientific Strategist / Skeptical Reviewer:** Formulates hypotheses, derives mathematical questions, challenges conclusions, sets falsification thresholds.
  - **Experimental Scientist / Research Engineer (Antigravity):** Implements pre-registered protocols, writes modular verified code, runs experiments, analyzes raw outputs with statistical sobriety, guarantees $\Delta\theta \equiv 0$, identifies implementation phenomena.
- **Governing Standard:** All 14 Inviolable Agent Laws in [`AGENTS.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/AGENTS.md) (specifically Law 2: Never Invent Results, Law 4: Never Silently Shift Hypotheses, Law 6: Frozen Backbone $\Delta\theta \equiv 0$, Law 7: Zero Data Leakage, Law 9: No Cherry-Picking, Law 10: Never Claim Premature Novelty, Law 13: Deterministic Reproducibility, Law 14: Challenge Rather Than Defend).
- **Codification Anchor:** [`theory/README.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/theory/README.md) §103.
- **Core Scientific Question:**
  $$\boxed{\textbf{Can a frozen foundation model autonomously invent a genuinely new internal computational operator when the existing operator toolbox contains no solution?}}$$

---

## 2. Methodological Safeguards: Rigorous Resolution of All 5 Theoretical Critiques

### Safeguard 1: Exact Statistical Consistency on the Held-Out Test Set
- **Target Benchmark:** `BENCH-004-TRANSFER` ($N_{\mathrm{test}}=50$, Seed 350).
- **Pre-Intervention Baseline:** $M_I = 0.5200$ (26/50 correct).
- **Pre-Authorized Library Oracle Bound:** $M_{\mathrm{Oracle}}(\mathcal{G}_{\mathrm{pre}}) = 0.5400$ ($+2.0\text{ pp, } b=1, c=0$).
- **Primary Structural-Invention Success Threshold ($\delta = +10.0\text{ pp}$):**
  $$\boxed{M \ge 0.6200 \ (31/50) \quad \text{with} \quad b \ge 5, \quad c = 0, \quad \text{exact one-sided McNemar } p \le 0.05}$$
  - At the minimal qualifying configuration ($b=5, c=0$), the exact paired binomial/McNemar probability is:
    $$p = \left(\frac{1}{2}\right)^5 = \frac{1}{32} = 0.03125 \le 0.05$$
  - Eliminates the previous statistical inconsistency ($b=4, c=0 \to p=0.0625$). The threshold strictly guarantees both $\Delta M \ge +10.0$ pp and conventional statistical significance ($p \le 0.05$).
- **Compute Budget ($B_{\mathrm{eval}}$):** Strictly locked to $B_{\mathrm{eval}} = 1.00$ forward passes per instance during held-out evaluation.

### Safeguard 2: Functional Non-Reducibility (Beyond Strict Non-Linearity)
Structural novelty is defined strictly by **functional non-reducibility with respect to the pre-registered operator grammar and independent audit distribution**, rather than merely whether an operator contains a non-linear activation.
$$\boxed{\textbf{An operator } G_{\mathrm{new}} \textbf{ is structurally novel iff it is functionally non-reducible with respect to the pre-registered operator grammar and independent audit distribution.}}$$
A transformation that lies outside the pre-authorized subspace (e.g., dynamic cross-head attention mixing matrix $A h$) can be structurally novel if it is mathematically non-reducible to $\operatorname{span}(\mathcal{G}_{\mathrm{pre}})$. This criterion demonstrates non-reducibility relative to the tested grammar and audit distribution, without asserting mathematical irreducibility across all conceivable representations.


### Safeguard 3: The Four-Way Structural Equivalence Classification (Including Explicit Indeterminate Zone)
For any candidate operator $G_{\mathrm{new}}$, we measure normalized reconstruction error over validation representations $h \sim \mathcal{D}_{\mathrm{audit}}$:
- **Linear Span Reducibility Metric:**
  $$E_{\mathrm{span}}(G_{\mathrm{new}}) = \min_{a_1, \dots, a_5} \frac{\mathbb{E}_{h \sim \mathcal{D}_{\mathrm{audit}}}\left[ \| G_{\mathrm{new}}(h) - \sum_{i=1}^5 a_i G_i(h) \|^2 \right]}{\mathbb{E}_{h \sim \mathcal{D}_{\mathrm{audit}}}\left[ \| G_{\mathrm{new}}(h) \|^2 \right]}$$
- **Compositional Reducibility Metric:**
  $$E_{\mathrm{comp}}(G_{\mathrm{new}}) = \min_{i, j, \alpha, \beta} \frac{\mathbb{E}_{h \sim \mathcal{D}_{\mathrm{audit}}}\left[ \| G_{\mathrm{new}}(h) - G_j(G_i(h; \alpha); \beta) \|^2 \right]}{\mathbb{E}_{h \sim \mathcal{D}_{\mathrm{audit}}}\left[ \| G_{\mathrm{new}}(h) \|^2 \right]}$$

Every candidate is mapped into one of four mutually exclusive structural classifications:
1. **Library-Equivalent:** $E_{\mathrm{span}} \le 0.05$. (Classified as linear recombination / parameter tuning of $\mathcal{G}_{\mathrm{pre}}$).
2. **Composition-Equivalent:** $E_{\mathrm{span}} > 0.05$ and $E_{\mathrm{comp}} \le 0.05$. (Classified as compositional chaining of existing primitives).
3. **Structurally Novel:** $E_{\mathrm{span}} \ge 0.80$ **and** $E_{\mathrm{comp}} \ge 0.80$. (Proven functionally non-reducible to pre-authorized primitives or compositions).
4. **Indeterminate:** $0.05 < \min(E_{\mathrm{span}}, E_{\mathrm{comp}}) < 0.80$.
   - **Crucial Inviolable Rule:** *An indeterminate candidate must NEVER be promoted to "new invention." If an indeterminate candidate produces performance gains, it is classified as Ambiguous Recombination.*

### Safeguard 4: Three-Way Dataset Separation (Zero Leakage Firewall)
The experimental protocol divides data into three strictly firewalled splits:
$$\boxed{
\mathcal{D}_{\mathrm{synth}} \ (N=15)
\longrightarrow
\text{Synthesize Candidates}
\longrightarrow
\mathcal{D}_{\mathrm{audit}} \ (N=15)
\longrightarrow
\text{Equivalence & Causal Audit}
\longrightarrow
\text{Freeze Toolbox}
\longrightarrow
\mathcal{D}_{\mathrm{test}} \ (N=50)
}$$
1. **$\mathcal{D}_{\mathrm{synth}}$ ($N=15$ unannotated prompts, Seed 250):** Used exclusively by the candidate generator to inspect internal observables $\mathcal{O}_M(x)$ and construct candidate operator definitions.
2. **$\mathcal{D}_{\mathrm{audit}}$ ($N=15$ unannotated prompts, Seed 251):** An independent held-out calibration split used exclusively to evaluate $E_{\mathrm{span}}, E_{\mathrm{comp}}$, and verify causal safety ($c_{\mathrm{audit}} = 0, \Delta\log p_{\mathrm{audit}} > 0$). Neither $\mathcal{D}_{\mathrm{synth}}$ nor $\mathcal{D}_{\mathrm{test}}$ is used for this equivalence audit.
3. **$\mathcal{D}_{\mathrm{test}}$ ($N=50$ held-out benchmark instances, Seed 350):** Completely untouched until the candidate grammar, structural classifications, and audited toolbox are cryptographically frozen. Zero labels exposed during synthesis or audit.

### Safeguard 5: Parameter Fitting $\neq$ Structural Invention
A parameterized network fitted on calibration data does not constitute a new computational primitive. The invention claim requires:
$$\boxed{\textbf{Functional Non-Reducibility } (E \ge 0.80) \ + \ \textbf{Held-Out Benefit } (\Delta M \ge +10\text{ pp}) \ + \ \textbf{Zero Corruptions } (c=0) \ + \ \textbf{Frozen Grammar}}$$
simultaneously.

---

## 3. The Four-Way Falsification Hierarchy

| Outcome | Quantitative Criteria | Scientific Attribution | Epistemological Decision |
| :--- | :--- | :--- | :--- |
| **Outcome 1: Library Selection** | Any $G_i \in \mathcal{G}_{\mathrm{pre}}$ achieves $M \ge 0.6200$ ($b \ge 5, c=0$) | Better controller / selector | Falsifies Operator Invention; confirms library routing. |
| **Outcome 2: Compositional Recombination** | A candidate classified as **Composition-Equivalent** ($E_{\mathrm{comp}} \le 0.05$) achieves $M \ge 0.6200$ ($b \ge 5, c=0$) | Compositional capability | Confirms Compositional Recombination; falsifies primitive invention. |
| **Outcome 3: Structural Operator Invention** | A candidate classified as **Structurally Novel** ($E_{\mathrm{span}} \ge 0.80, E_{\mathrm{comp}} \ge 0.80$) achieves $M \ge 0.6200$ ($b \ge 5, c=0, p=0.03125$) | Genuine Operator Invention | Confirms First-Principles Operator Invention: autonomous emergence of new computational primitives. |
| **Outcome 4: Existence Boundary Invariant** | No candidate operator (selected, composed, novel, or indeterminate) achieves $M \ge 0.6200$ | Existence Boundary Invariant | Falsifies First-Principles Operator Invention under tested regime. |

*Note on Indeterminate Candidates:* If an indeterminate candidate ($0.05 < E < 0.80$) achieves $M \ge 0.6200$, it is classified as **Outcome 2B (Ambiguous Recombination)** and explicitly barred from claiming structural invention.

---

## 4. Pre-Registered Synthesis Grammar & Candidate Pool

Candidates synthesized on $\mathcal{D}_{\mathrm{synth}}$ ($N=15$, Seed 250):

### 1. Pre-Authorized Library ($\mathcal{G}_{\mathrm{pre}}$)
- $G_1$: Residual Velocity Flow ($h + \alpha v_{\mathrm{flow}}$)
- $G_2$: Trajectory Curvature Acceleration ($h + \alpha a_{\mathrm{curv}}$)
- $G_3$: Orthogonalized Subspace Projection ($P_{h_4}^\perp(v_{\mathrm{flow}})$)
- $G_4$: Multi-Head Attention Alignment
- $G_5$: Distractor Coordinate Subspace Projection

### 2. Compositional Chaining ($\mathcal{G}_{\mathrm{comp}}$)
- $C_1 = G_3 \circ G_1$: Orthogonal velocity flow filtered through middle-layer subspace.
- $C_2 = G_2 \circ G_3$: Curvature acceleration modulated by orthogonalized projection.

### 3. Structural Candidates ($\mathcal{G}_{\mathrm{struct}}$)
- $S_1$ (**Attention-Entropy Gated Dynamic Projection**):
  $$G_{S1}(h_\ell) = h_\ell + \alpha \cdot \sigma\left(\frac{H(A_\ell) - \tau}{\beta}\right) \cdot \operatorname{LayerNorm}(W_{\mathrm{proj}} h_\ell)$$
- $S_2$ (**Cross-Layer Feature Thresholding**):
  $$G_{S2}(h_\ell) = h_\ell + \alpha \cdot \operatorname{ReLU}\big(|h_\ell - h_{\ell-2}| - \gamma \cdot \operatorname{std}(h_\ell)\big) \odot \operatorname{sign}(h_\ell - h_{\ell-2})$$
- $S_3$ (**Unembedding-Orthogonalized Context Self-Attention Modulation**):
  $$G_{S3}(h_\ell) = h_\ell + \alpha \cdot P_{W_U[\mathrm{top5}]}^\perp\left(\sum_{j} A_{\ell, \mathrm{sink}, j} \cdot h_{\ell, j}\right)$$

---

## 5. Execution Protocol & Invariance Audit

1. **Step 1: Invariance Verification:**
   - Pre-computation parameter SHA-256 hash verified: `54c88fa4897785f2bd94b32d26de1f73f1052bcc42124d563d0cda96940de936` ($\Delta\theta \equiv 0$).
2. **Step 2: Candidate Synthesis on $\mathcal{D}_{\mathrm{synth}}$ ($N=15$, Seed 250):**
   - Extract internal geometric observables $\mathcal{O}_M$. Construct operator parameters.
3. **Step 3: Formal Equivalence Audit & Causal Filter on $\mathcal{D}_{\mathrm{audit}}$ ($N=15$, Seed 251):**
   - Compute $E_{\mathrm{span}}$ and $E_{\mathrm{comp}}$ over $\mathcal{D}_{\mathrm{audit}}$ to strictly classify each candidate into: Library-Equivalent, Composition-Equivalent, Structurally Novel, or Indeterminate.
   - Execute causal safety filter ($c_{\mathrm{audit}} = 0, \Delta\log p_{\mathrm{audit}} > 0$).
   - Prune unsafe or corrupting candidates.
   - **FREEZE TOOLBOX:** Record SHA-256 hash of audited toolbox and classifications.
4. **Step 4: Confirmatory Benchmark on Held-Out $\mathcal{D}_{\mathrm{test}}$ ($N=50$, Seed 350):**
   - Execute single-pass evaluation ($B_{\mathrm{eval}} = 1.00$).
   - Verify post-computation parameter SHA-256 hash identical ($\Delta\theta \equiv 0$).
   - Map quantitative results to the Four-Way Falsification Hierarchy.
