# EXP019 Protocol Specification: Feature-Dependent Activation-Gated Intervention

**Status:** PRE-REGISTERED  
**Author:** Antigravity Research Team  
**Date:** 2026-09-11  
**Predecessor Experiments:** EXP013–EXP018  
**Governing Standard:** `AGENTS.md` (14 Inviolable Laws) & `STATISTICAL_PROTOCOL_V02.md`  

---

## 1. Context & Research Hypothesis

In EXP018, expanding linear subspace rank from $r=2 \to 4 \to 8$ did not break the performance ceiling; instead, it reduced Oracle headroom and increased representation disruption.

The causal diagnostic is that uniform linear projection:
$$h_t' = (I - \alpha V V^\top) h_t$$
applies the identical fractional suppression across all sequence tokens, including tokens where the candidate feature is not expressed.

EXP019 tests **conditional, feature-dependent intervention**:
$$\boxed{\text{[HYPOTHESIS] Intervening selectively where the candidate feature is actively expressed}}$$
$$\boxed{\text{preserves useful correction while preventing collateral disruption to uninvolved tokens.}}$$

---

## 2. Invariant Components & Protocol Locks

| Component | Protocol Lock | Epistemological Status |
| :--- | :--- | :--- |
| **Model** | Frozen HuggingFace `gpt2` (124M parameters, 12 layers) | `[FACT]` Pre-run & post-run SHA-256 parameter hash verification ($\Delta\theta = 0$) |
| **Benchmark** | `BENCH-002-NL` ($N_{\mathrm{dev}}=20$, seed 123; $N_{\mathrm{conf}}=100$, seed 42) | `[FACT]` Fixed distractor suppression benchmark |
| **Layer** | **Layer 8** (Block 7 output) | `[DEFINITION]` Optimal single-layer depth |
| **Generator** | Native $G4_{\mathrm{sparse}}$ Dictionary Atoms ($K=4$) | `[DEFINITION]` $n_{\mathrm{atoms}} = 8$ atoms learned per layer |
| **Subspace Rank** | **$r = 2$** | `[DEFINITION]` Optimal linear dimensionality |
| **Base Strength** | **$\alpha = 0.25$** | `[DEFINITION]` Optimal continuous intervention strength |
| **Scope** | All-token residual stream (modulated by token gate $g_t$) | `[DEFINITION]` Uniform sequence with token-level gating |
| **Evaluator** | $E_{\mathrm{CF}}$ (Counterfactual consistency) | `[ASSUMPTION]` Sequestered until Gate 1 Oracle headroom is statistically demonstrated |
| **Baseline** | Identity ($\alpha = 0 \implies P = I, M_I = 0.6500$) | `[FACT]` Unperturbed foundation model performance |

---

## 3. Operator Formulations: Linear vs. Hard-Gated vs. Soft-Gated

For sequence token representations $h_t \in \mathbb{R}^d$ ($t \in \{1, \dots, T\}$) at Layer 8:
- Feature projection: $z_t = V^\top h_t \in \mathbb{R}^2$.
- Feature activation energy: $e_t = \|z_t\|_2 = \|V^\top h_t\|_2$.
- Standardized prompt energy: $\hat{e}_t = \frac{e_t - \mu_e}{\sigma_e + \epsilon}$.

### Operators Compared:
1. **O0 (Linear Baseline Control):**
   $$g_t = 1.0 \implies h_t' = h_t - 0.25 V V^\top h_t$$
2. **O1 (Hard Activation Gate):**
   $$g_t = \mathbf{1}[e_t > P_{75}(e)] \implies h_t' = h_t - 0.25 \cdot \mathbf{1}[e_t > P_{75}(e)] \cdot V V^\top h_t$$
3. **O2 (Soft Sigmoid Gate — Primary Operator):**
   $$g_t = \sigma\left(\frac{\hat{e}_t - \tau}{T_{\mathrm{temp}}}\right) \implies h_t' = h_t - 0.25 \cdot g_t \cdot V V^\top h_t$$
   with pre-registered threshold $\tau = P_{75}(\hat{e})$ and fixed temperature $T_{\mathrm{temp}} = 1.0$.

---

## 4. Diagnostics & Matched-Budget Controls

1. **Mean Gate Activation Budget ($B$):**
   $$B = \frac{1}{T} \sum_{t=1}^T g_t$$
2. **Total Intervention Magnitude ($A$):**
   $$A = \frac{\sum_t \|h_t' - h_t\|_2}{\sum_t \|h_t\|_2}$$
3. **Token-Partitioned Selective Displacement ($D_{\mathrm{high}}$ vs. $D_{\mathrm{low}}$):**
   - High-energy tokens: $\mathcal{T}_{\mathrm{high}} = \{t : e_t > P_{75}(e)\} \implies D_{\mathrm{high}} = \frac{1}{|\mathcal{T}_{\mathrm{high}}|} \sum_{t \in \mathcal{T}_{\mathrm{high}}} \frac{\|h_t' - h_t\|_2}{\|h_t\|_2}$
   - Low-energy tokens: $\mathcal{T}_{\mathrm{low}} = \{t : e_t \le P_{75}(e)\} \implies D_{\mathrm{low}} = \frac{1}{|\mathcal{T}_{\mathrm{low}}|} \sum_{t \in \mathcal{T}_{\mathrm{low}}} \frac{\|h_t' - h_t\|_2}{\|h_t\|_2}$
   - Test prediction: $D_{\mathrm{high}} \gg D_{\mathrm{low}}$.
4. **Logit Preservation:** $\Delta_{\mathrm{KL}} = D_{\mathrm{KL}}(p_I \parallel p_{\mathrm{SCBI}})$ and $\operatorname{Overlap}_{10}$.
5. **Representation Metrics:** $\Delta \mathrm{Margin}$, $\Delta \log p$, $\Delta \mathrm{rank}$.

---

## 5. Pre-Registered Decision Criteria

1. **Gate G1 (Gated Headroom Advantage):**
   $$M_{\mathrm{Oracle,gated}} > M_{\mathrm{Oracle,linear}} \quad \land \quad M_{\mathrm{Random,gated}} \approx M_{\mathrm{Identity}}$$
   $$\Delta_{\mathrm{KL,gated}} < \Delta_{\mathrm{KL,linear}} \quad \land \quad \operatorname{Overlap}_{10,\mathrm{gated}} > \operatorname{Overlap}_{10,\mathrm{linear}}$$
   If passed: lock the winning gated operator (O1 or O2) for **Phase B Confirmatory Benchmark ($N=100$)**.
2. **Negative Outcome Pathway:**
   If activation gating produces no gain in $M_{\mathrm{Oracle}}$ or degrades performance, conclude that feature presence alone does not determine intervention utility, directing research to semantic feature re-orientation rather than suppression.
