# EXP016 Protocol Specification: Layer Localization & Multi-Layer Coordination

**Status:** PRE-REGISTERED  
**Author:** Antigravity Research Team  
**Date:** 2026-09-11  
**Predecessor Experiments:** EXP013 (Evaluator signal), EXP014 (Operator sweep), EXP015 (Generator characterization & confirmatory benchmark)  
**Governing Standard:** `AGENTS.md` (14 Inviolable Laws) & `STATISTICAL_PROTOCOL_V02.md`  

---

## 1. Context & Epistemological Pre-Registration

In EXP015, evaluating sparse feature dictionary learning ($G4_{\mathrm{sparse}}$) against the baseline temporal quartile generator ($G0$) at Layer 10 yielded virtually identical confirmatory performance ($M_{\mathrm{Oracle}} = 0.700$ vs. $0.710$, both $p > 0.10$). Crucially, per scientific integrity guidelines:
$$\boxed{\text{[OBSERVATION] EXP015 provides evidence consistent with, but does not prove, a Layer-10 ceiling.}}$$

EXP016 isolates **depth and multi-layer coordination** to test the central research question:
$$\boxed{\text{[HYPOTHESIS] Is the }\sim0.70\text{ performance ceiling caused by intervening at only Layer 10?}}$$

---

## 2. Locked Invariant Components (Single-Variable Discipline)

To isolate depth and coordination without confounding, all algorithmic parameters established in EXP013–EXP015 are strictly frozen:

| Component | Protocol Lock | Epistemological Status |
| :--- | :--- | :--- |
| **Model** | HuggingFace `gpt2` (124M parameters, 12 blocks) | `[FACT]` Pre-run & post-run SHA-256 parameter hash verification ($\Delta\theta = 0$) |
| **Dataset** | `BENCH-002-NL` ($N_{\mathrm{dev}}=20$, seed 123; $N_{\mathrm{conf}}=100$, seed 42) | `[FACT]` Fixed distractor suppression benchmark |
| **Generator** | **$G4_{\mathrm{sparse}}$ Sparse Dictionary Atoms** ($K=4$, $\text{rank}=2$) | `[DEFINITION]` Dictionary atoms fitted per layer |
| **Operator** | Continuous projector: $P_\alpha = I - \alpha V V^\top$ | `[DEFINITION]` Fluency-preserving operator |
| **Single-Layer $\alpha$** | **0.25** | `[DEFINITION]` Optimal continuous intervention strength |
| **Scope** | All-token residual stream | `[DEFINITION]` Uniform sequence intervention |
| **Evaluator** | $E_{\mathrm{CF}}$ (Counterfactual consistency) | `[ASSUMPTION]` Sequestered until Gate 1 Oracle headroom is statistically demonstrated |
| **Baseline** | Identity ($\alpha=0 \implies P=I$) | `[FACT]` Unmodified model performance $M_I$ |
| **Primary Endpoint** | $\Delta M_{\mathrm{Oracle}} = M_{\mathrm{Oracle}} - M_I$ | `[HYPOTHESIS]` Primary measure of headroom |

---

## 3. Native Basis Requirement (Anti-Transplantation Rule)

Under no circumstances may a candidate basis computed at Layer 10 be transplanted into an earlier layer $l < 10$.
For each evaluated layer $l \in \{4, 6, 8, 10\}$:
$$H_l \longrightarrow \mathcal{G}_{l,\mathrm{sparse}}(H_l) \longrightarrow V_l \in \mathbb{R}^{d \times 2}$$
where $H_l \in \mathbb{R}^{T \times d}$ is the unperturbed hidden representation at layer $l$ (output of transformer block $l-1$). The candidates $\{V_{l,1}, \dots, V_{l,K}\}$ must be native to the geometric manifold of that layer.

---

## 4. Phase A: Single-Layer Localization Screen ($N_{\mathrm{dev}} = 20$)

Screen candidate layers $L \in \{4, 6, 8, 10\}$ on $N_{\mathrm{dev}} = 20$ development instances (`dev_seed=123`).

### Primary Metrics per Layer $l$:
1. $M_I$: Top-1 accuracy under Identity.
2. $M_{\mathrm{Oracle}, l}$: Top-1 accuracy under oracle selection among $K=4$ native candidates $P_{0.25}^{(l, k)}$.
3. $\Delta M_l = M_{\mathrm{Oracle}, l} - M_I$: Headroom over Identity.
4. $M_{\mathrm{Random}, l}$: Top-1 accuracy under random selection from candidate pool, and under uniform random orthogonal 2D subspace $V_{\mathrm{rand}} \in \mathbb{R}^{d \times 2}$.
5. Headroom Spread: $M_{\mathrm{Oracle}, l} - M_{\mathrm{Random}, l}$.

### Essential Residual Diagnostics:
1. **Intervention Displacement ($D_l$):**
   $$D_l = \frac{\|H_l' - H_l\|_F}{\|H_l\|_F} = \alpha \frac{\|H_l V_l\|_F}{\|H_l\|_F}$$
2. **Logit Preservation / KL Divergence ($\Delta_{\mathrm{KL}}$):**
   $$\Delta_{\mathrm{KL}} = D_{\mathrm{KL}}(p_{\mathrm{Identity}} \parallel p_{\mathrm{SCBI}}) = \sum_{v \in \mathcal{V}} p_I(v) \log \frac{p_I(v)}{p_{\mathrm{SCBI}}(v)}$$
3. **Top-$k$ Vocabulary Overlap ($\operatorname{Overlap}_{10}$):**
   $$\operatorname{Overlap}_{10} = \frac{|\operatorname{Top10}(p_{\mathrm{Identity}}) \cap \operatorname{Top10}(p_{\mathrm{SCBI}})|}{10}$$

---

## 5. Phase C & D: Multi-Layer Coordination & Budget Conservation

If Phase A establishes that earlier layers carry meaningful headroom, multi-layer combinations will be tested:
$$\{4, 6\}, \quad \{6, 8\}, \quad \{8, 10\}, \quad \{4, 8\}, \quad \{4, 6, 8, 10\}$$

### Budget Conservation Rule:
To prevent confounding multi-layer coordination with increased cumulative intervention energy:
$$A_{\mathrm{total}} = 0.25 \implies \alpha_l = \frac{0.25}{n}$$
- $n=1$: $\alpha = 0.25$
- $n=2$: $\alpha = 0.125$
- $n=4$: $\alpha = 0.0625$

### Coordination Mechanisms:
- **M1 (Independent-Coordinate Intervention):** Bases $V_l$ generated from unmodified forward pass activations; projections applied simultaneously.
- **M2 (Sequential Adaptive Intervention):** Activations modified at layer $l_1$, propagated forward, and layer $l_2$ basis generated from the transformed state: $V_{l_2} = \mathcal{G}(F^{l_1 \to l_2}(H_{l_1}'))$.

---

## 6. Pre-Registered Decision Criteria

1. **Gate A1 (Layer Localization Headroom):**
   Phase A identifies at least one layer $l \in \{4, 6, 8\}$ with:
   $$\Delta M_l > \Delta M_{10} \quad \text{or} \quad (M_{\mathrm{Oracle}, l} - M_{\mathrm{Random}, l} > M_{\mathrm{Oracle}, 10} - M_{\mathrm{Random}, 10})$$
   with stable logit preservation ($\operatorname{Overlap}_{10} \ge 0.70$).
2. **Confirmatory Breakthrough Thresholds:**
   - **Strong Evidence:** $M_{\mathrm{Oracle}} \ge 0.75 \land \text{CI}_{95\%}(\Delta M) > 0 \land p < 0.05$.
   - **Very Strong Result:** $M_{\mathrm{Oracle}} \ge 0.80 \land M_{\mathrm{Random}} \approx M_I \land D_l \text{ is modest}$.
3. **Negative Outcome Pathway:**
   If all layers $L \in \{4, 6, 8, 10\}$ remain bounded at $M_{\mathrm{Oracle}} \le 0.70$ without separation, conclude that layer depth alone cannot break through the single-layer subspace ceiling, directing research to nonlinear / cross-layer interaction operators.
