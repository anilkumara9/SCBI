# EXP026: Cross-Architecture Transfer Benchmark Specification

- **Experiment ID:** `EXP026`
- **Governing Rules:** [`AGENTS.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/AGENTS.md) (Laws 1–14), [`.agents/rules/00-core-research.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/rules/00-core-research.md), [`.agents/rules/03-experiments.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/rules/03-experiments.md).
- **Core Research Question:** Does the autonomous SCBI pipeline ($G4, E_{CF}, O5$) transfer across distinct foundation model architectures and scales without architectural retuning or weight updates, proving that SCBI is **representation-geometry-specific** rather than an artifact of GPT-2 Small?

---

## 1. Scientific Hypotheses & Falsification Criteria

### Hypothesis 1 (Scale / Depth-Width Scaling within Family):
$$\mathbf{H_{\mathrm{arch,scale}}}: \quad \Delta M_{\mathrm{gpt2\text{-}medium}} = M_{E_{CF}}(\mathrm{GPT\text{-}2\ Medium}) - M_{\mathrm{Identity}}(\mathrm{GPT\text{-}2\ Medium}) > 0$$
- Evaluated on `gpt2-medium` (355M parameters, $L_{\mathrm{blocks}}=24, d_{\mathrm{model}}=1024$).
- **Falsification Criteria:**
  - $p_{\mathrm{exact,one-sided}} \ge 0.05$ on paired McNemar test across $N=100$.
  - 10,000-resample Bootstrap 95% Confidence Interval spans or falls below 0: $\min CI_{95\%}(\Delta M) \le 0$.
  - Headroom recovery ratio $\eta_{\mathrm{HR}} \le 0$.

### Hypothesis 2 (Cross-Family Architectural Transfer):
$$\mathbf{H_{\mathrm{arch,family}}}: \quad \Delta M_{\mathrm{pythia}} = M_{E_{CF}}(\mathrm{Pythia\text{-}160M}) - M_{\mathrm{Identity}}(\mathrm{Pythia\text{-}160M}) > 0$$
- Evaluated on `EleutherAI/pythia-160m` (160M parameters, $L_{\mathrm{blocks}}=12, d_{\mathrm{model}}=768$).
- **Architectural Divergence:** Uses Rotary Position Embeddings (RoPE), untied input/output embeddings, and parallel Attention/MLP blocks ($x + \text{Attn}(x) + \text{MLP}(x)$), completely differing from GPT-2's learned absolute positional embeddings and sequential block design.
- **Falsification Criteria:**
  - $p_{\mathrm{exact,one-sided}} \ge 0.05$ on paired McNemar test across $N=100$.
  - 10,000-resample Bootstrap 95% Confidence Interval spans or falls below 0: $\min CI_{95\%}(\Delta M) \le 0$.
  - Headroom recovery ratio $\eta_{\mathrm{HR}} \le 0$.

### Secondary Mechanistic & Efficiency Endpoints:
1. **Standardized Headroom Recovery:**
   $$\eta_{\mathrm{HR}} = \frac{M_{E_{CF}} - M_{\mathrm{Identity}}}{M_{\mathrm{Oracle}} - M_{\mathrm{Identity}}}$$
2. **Correct Token Probability Shift:**
   $$\mathbf{H_{\mathrm{mech}}}: \quad \mathbb{E}[\Delta \log p(y_{\mathrm{correct}})_{E_{CF}}] > 0$$
3. **Distractor Bias Suppression:** Reduction in instances where distractor token probability exceeds target token probability ($p_d > p_t$).

---

## 2. Pre-Declared Normalized Depth Invariant Rule

To prevent post-hoc layer cherry-picking, the target intervention layer in each architecture is strictly governed by preserving normalized network depth:
$$\lambda = \frac{l}{L_{\mathrm{blocks}}} \approx 0.667$$

| Model Architecture | Parameter Count | Total Layers ($L_{\mathrm{blocks}}$) | Model Dim ($d_{\mathrm{model}}$) | Normalized Depth ($\lambda$) | Target Layer ($l$) | Block Index (`block_idx`) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **GPT-2 Small** (Baseline) | 124M | 12 | 768 | $8/12 = 0.667$ | Layer 8 | `transformer.h[7]` |
| **GPT-2 Medium** (Regime 1) | 355M | 24 | 1024 | $\text{round}(0.667 \times 24) / 24 = 0.667$ | Layer 16 | `transformer.h[15]` |
| **Pythia-160m** (Regime 2) | 160M | 12 | 768 | $8/12 = 0.667$ | Layer 8 | `gpt_neox.layers[7]` |

---

## 3. Strict Algorithmic Freeze (Zero Retuning Rule)

All mathematical components established in EXP022–EXP025 remain identically locked:
- **Candidate Generator:** Native $G4_{\text{sparse}}$ ($K=4$, rank $r=2$) extracted from target-source and distractor-source representations.
- **Evaluator:** Frozen counterfactual evaluator $E_{CF}$:
  $$e_{\mathrm{cf}}(V_k) = \mathrm{JS}(q_b(V_k), q_p(V_k)) - 0.5 \cdot \mathrm{JS}(q_b(V_k), q_n(V_k))$$
- **Operator Class:** Contrastive Hard Gate $O5$ ($g_t = \mathbf{1}[d_t > 0]$) where:
  $$d_t = \|V_-^\top h_t\|_2 - \|V_+^\top h_t\|_2$$
  with per-instance exact Frobenius matching scale factor:
  $$s_i = \frac{\|H_i V_- V_-^\top\|_F}{\|\operatorname{diag}(g) H_i V_- V_-^\top\|_F}$$
- **Operator Strength:** $\alpha = 0.25$.
- **Backbone State:** Frozen ($\Delta\theta \equiv 0$). Pre-run and post-run parameter hashes are verified via SHA-256.

---

## 4. Benchmark & Data Specifications

- Evaluated on `BENCH-002-NL` Confirmatory Split ($N=100$, Seed 84).
- Target and distractor tokens are encoded and verified to produce single-token IDs across all vocabularies.
- Zero outcome labels ($y_{\mathrm{correct}}$) are accessible to candidate generation or evaluation loops.
