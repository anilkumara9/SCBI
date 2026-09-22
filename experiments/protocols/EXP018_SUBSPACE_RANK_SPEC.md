# EXP018 Protocol Specification: Subspace Rank Capacity Sweep

**Status:** PRE-REGISTERED  
**Author:** Antigravity Research Team  
**Date:** 2026-09-11  
**Predecessor Experiments:** EXP013 (Evaluator signal), EXP014 (Operator softening), EXP015 (Generator redesign), EXP016 (Layer localization), EXP017 (Multi-layer coordination)  
**Governing Standard:** `AGENTS.md` (14 Inviolable Laws) & `STATISTICAL_PROTOCOL_V02.md`  

---

## 1. Context & Research Hypothesis

Across EXP014–EXP017, confirmatory Top-1 performance under rank-2 continuous linear projection converged to an invariant empirical plateau:
$$\boxed{M_{\mathrm{Identity}} = 0.6500 \quad \longrightarrow \quad M_{\mathrm{Oracle}} \approx 0.7000 - 0.7100 \quad (r=2)}$$

Crucially, contrastive preference climbed sharply from $0.79 \to 0.91-0.95$. This demonstrates that the representation is altered in the intended direction, but rank-2 projection does not reliably flip the discrete top-1 token.

EXP018 isolates **subspace rank capacity** to test the central question:
$$\boxed{\text{[HYPOTHESIS] Is the }\sim 0.71\text{ ceiling caused by insufficient subspace capacity?}}$$

---

## 2. Invariant Components & Protocol Locks

| Component | Protocol Lock | Epistemological Status |
| :--- | :--- | :--- |
| **Model** | Frozen HuggingFace `gpt2` (124M parameters, 12 layers) | `[FACT]` Pre-run & post-run SHA-256 parameter hash verification ($\Delta\theta = 0$) |
| **Benchmark** | `BENCH-002-NL` ($N_{\mathrm{dev}}=20$, seed 123; $N_{\mathrm{conf}}=100$, seed 42) | `[FACT]` Fixed distractor suppression benchmark |
| **Layer** | **Layer 8** (Block 7 output) | `[DEFINITION]` Peak single-layer depth |
| **Generator** | Native $G4_{\mathrm{sparse}}$ Dictionary Atoms ($K=4$) | `[DEFINITION]` $K \times r$ latent atoms learned per rank |
| **Scope** | All-token residual stream | `[DEFINITION]` Uniform sequence intervention |
| **Operator** | Continuous projector: $P_{\alpha, r} = I - \alpha V_r V_r^\top$ | `[DEFINITION]` Fixed contraction operator |
| **Primary $\alpha$** | **0.25** | `[DEFINITION]` Optimal fluency-preserving softening |
| **Evaluator** | $E_{\mathrm{CF}}$ (Counterfactual consistency) | `[ASSUMPTION]` Sequestered until Gate 1 Oracle headroom is statistically demonstrated |
| **Baseline** | Identity ($\alpha = 0 \implies P = I, M_I = 0.6500$) | `[FACT]` Unperturbed foundation model performance |
| **Independent Variable** | **$r \in \{2, 4, 8\}$** | `[HYPOTHESIS]` Subspace rank capacity sweep |

---

## 3. Subspace Extraction Protocol

For each rank $r \in \{2, 4, 8\}$:
1. Native $G4_{\mathrm{sparse}}$ dictionary learning extracts $n_{\mathrm{atoms}} = K \times r$ latent dictionary atoms from $H_8 \in \mathbb{R}^{T \times d}$.
2. Atoms are partitioned into $K=4$ candidate sets of $r$ vectors.
3. Each set is orthonormalized via QR decomposition: $V_k \in \mathbb{R}^{d \times r}$ with $V_k^\top V_k = I_r$.
4. Projection operator is applied via forward hook at Layer 8 block output:
   $$h' = h - 0.25 (h V_k) V_k^\top$$

---

## 4. Diagnostic Suite: Useful Correction vs. Global Destruction

1. **Intervention Displacement ($D_r$):**
   $$D_r = \frac{\|H' - H\|_F}{\|H\|_F} = 0.25 \frac{\|H V_r\|_F}{\|H\|_F}$$
2. **Logit Divergence ($\Delta_{\mathrm{KL}}$):**
   $$\Delta_{\mathrm{KL}} = D_{\mathrm{KL}}(p_{\mathrm{Identity}} \parallel p_{\mathrm{SCBI}})$$
3. **Vocabulary Overlap ($\operatorname{Overlap}_{10}$):**
   $$\operatorname{Overlap}_{10} = \frac{|\operatorname{Top10}_I \cap \operatorname{Top10}_{\mathrm{SCBI}}|}{10}$$
4. **Probability Margin ($\Delta \mathrm{Margin}$):**
   $$\Delta \mathrm{Margin} = [p(y_{\mathrm{correct}}) - p(y_{\mathrm{distractor}})]_{\mathrm{SCBI}} - [p(y_{\mathrm{correct}}) - p(y_{\mathrm{distractor}})]_{\mathrm{Identity}}$$
5. **Correct Token Log-Probability Delta ($\Delta \log p$):**
   $$\Delta \log p(y_{\mathrm{correct}}) = \log p(y_{\mathrm{correct}})_{\mathrm{SCBI}} - \log p(y_{\mathrm{correct}})_{\mathrm{Identity}}$$
6. **Target Token Rank Shift ($\Delta \mathrm{rank}$):**
   $$\Delta \mathrm{rank}(y_{\mathrm{correct}}) = \operatorname{rank}(y_{\mathrm{correct}})_{\mathrm{Identity}} - \operatorname{rank}(y_{\mathrm{correct}})_{\mathrm{SCBI}}$$

---

## 5. Pre-Registered Progression Gates

1. **Gate R1 (Rank-Capacity Breakthrough):**
   A higher rank $r \in \{4, 8\}$ achieves $M_{\mathrm{Oracle}} \ge 0.80$ while maintaining logit preservation ($\operatorname{Overlap}_{10} \ge 0.75, \Delta_{\mathrm{KL}} \le 0.20$).
   - If passed: lock that single rank for **Phase B Confirmatory Benchmark ($N=100$)**.
2. **Gate R2 (Destructive Degradation):**
   Higher rank increases displacement ($D_r > 0.20$) and collapses vocabulary overlap ($\operatorname{Overlap}_{10} < 0.70$), with no gain in $M_{\mathrm{Oracle}}$.
   - Conclude that increasing rank linearly expands the destructive subspace footprint rather than isolating task distractors.
3. **Negative Outcome Pathway:**
   If $M_{\mathrm{Oracle}}$ remains bounded across all $r \in \{2, 4, 8\}$, conclude that linear subspace rank is not the bottleneck, directing research to nonlinear/feature-dependent operators.
