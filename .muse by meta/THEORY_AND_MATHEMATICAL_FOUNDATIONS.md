# Theory and Mathematical Foundations of SCBI

> **Epistemological Level:** Formal Mathematical Specification  
> **Source Documents:** `theory/README.md`, `theory/README_DEFINITIONS.md`, `theory/README_ALGORITHM.md`  
> **Authoring Swarm:** Muse Theory Agent & Research Director  

---

## 1. Mathematical Spaces of SCBI

Self-Consistent Basis Invention (SCBI) operates across six formally defined mathematical spaces:

| Symbol | Space Name | Mathematical Structure | Operational Role in SCBI |
| :---: | :--- | :--- | :--- |
| $\Theta$ | **Parameter Space** | $\mathbb{R}^{P}$ ($P = 1.6 \times 10^8$ or $4.05 \times 10^8$) | The static weights of the frozen foundation model. **Constraint:** $\Delta\theta \equiv 0$. |
| $\mathcal{X}$ | **Instance Space** | Sequence of discrete tokens $\mathcal{V}^*$ | Natural language input prompts containing premise context and query. |
| $\mathcal{Y}$ | **Target Output Space** | Discrete vocabulary simplex $\Delta^{|\mathcal{V}|}$ | Next-token probability distribution produced by the unembedding head. |
| $\mathcal{H}_l$ | **Hidden Residual Space** | $\mathbb{R}^d$ ($d = 768$ at 160M, $d = 1024$ at 410M) | Activation state at layer $l$. Intermediate computational manifold. |
| $\mathcal{Z}$ | **Projection Space** | $\mathbb{R}^k$ ($k \ll d$) | Low-dimensional task or role subspace extracted across demonstrations. |
| $\mathcal{B}$ | **Basis Manifold** | $\{B \in \mathbb{R}^{d \times r} : B^T B = I_r\}$ | Orthonormal or normalized directional vectors encoding relational programs. |

---

## 2. The Four Fundamental SCBI Operators

SCBI decomposes inference-time basis synthesis into four decoupled operators:

```text
               D_support (Premises / Demonstrations)
                                │
                                ▼
                       ┌─────────────────┐
                       │  Generator G    │  --> Extracts candidate bases B_cand
                       └────────┬────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │  Evaluator E    │  --> Evaluates consistency / consistency loss
                       └────────┬────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │  Selector S     │  --> Selects optimal basis B*
                       └────────┬────────┘
                                │
   Target Instance x            │
           │                    ▼
           ▼           ┌─────────────────┐
    Alignment A(x) ──> │  Transformer T  │  --> Modulates residual stream h'(x) = h(x) + α b(x)
                       └─────────────────┘
```

### 2.1 The Generator Operator ($\mathcal{G}$)
$$\mathcal{G}: 2^{\mathcal{X} \times \mathcal{Y}} \to \mathcal{P}(\mathcal{B})$$
Given a support set $\mathcal{D}_{\text{support}}$ containing instances of a relational reasoning task, $\mathcal{G}$ computes activation trajectories across layers and extracts candidate bases.
- In EXP063–EXP066, $\mathcal{G}$ constructs a **counterfactual contrast direction**:
  $$\Delta h_i = h_l(x_i^{\text{rel}}) - h_l(x_i^{\text{neutral}})$$
  $$\hat{v}_k = \frac{\frac{1}{M}\sum_{i=1}^M \frac{\Delta h_i}{\|\Delta h_i\|_2}}{\left\|\frac{1}{M}\sum_{i=1}^M \frac{\Delta h_i}{\|\Delta h_i\|_2}\right\|_2}$$
  Aggregated across $K$ disjoint vocabularies:
  $$B_{\text{agg}} = \frac{\sum_{k=1}^K \hat{v}_k}{\left\|\sum_{k=1}^K \hat{v}_k\right\|_2}$$

### 2.2 The Evaluator Operator ($\mathcal{E}$)
$$\mathcal{E}: \mathcal{B} \times \mathcal{D}_{\text{support}} \to \mathbb{R}$$
Computes self-consistency scores or pseudo-likelihood under candidate interventions without requiring ground-truth supervision.

### 2.3 The Selector Operator ($\mathcal{S}$)
$$\mathcal{S}: \mathcal{P}(\mathcal{B}) \times \mathbb{R}^{|\mathcal{P}(\mathcal{B})|} \to \mathcal{B}$$
Selects the optimal basis $B^* = \arg\max_{B} \mathcal{E}(B)$.

### 2.4 The Dynamic Alignment Operator ($A(x)$ / $\mathcal{T}$)
$$\mathcal{T}: \mathcal{B} \times \mathcal{X} \to \mathcal{H}_l$$
Adapts the canonical support basis $B^*$ to the target instance $x$ on-the-fly.

In EXP065 and EXP066, this is realized via the **Subspace-Preserving Role-Procrustes Alignment**:
1. For target instance $x$, extract premise entity representations:
   $$E(x) = \left[ w(e_{\text{head}}), w(e_{\text{tail}}) \right]^T \in \mathbb{R}^{2 \times d}$$
2. Reference canonical support frame:
   $$E_0 = \left[ w(e_{\text{head}}^{(0)}), w(e_{\text{tail}}^{(0)}) \right]^T \in \mathbb{R}^{2 \times d}$$
3. Closed-form orthogonal rotation via Singular Value Decomposition:
   $$E(x)^T E_0 = U \Sigma V^T \implies R(x) = U V^T \in O(d)$$
4. Dynamic rotated intervention:
   $$b_{\text{dynamic}}(x) = R(x) B_{\text{agg}}$$
   $$h'_l(x) = h_l(x) + \alpha \cdot b_{\text{dynamic}}(x)$$

---

## 3. The Geometric–Causal Dissociation Formalism

The central theoretical discovery of this research is the formal breakdown of the linear representation hypothesis when extended to cross-vocabulary causal interventions.

### 3.1 The Representation Geometry (Level A: Succeeded)
Let $\Delta h_A$ and $\Delta h_B$ be internal relational directions extracted from vocabularies $\mathcal{V}_A$ and $\mathcal{V}_B$. Under Procrustes rotation $R_{A \to B}$:
$$\cos(R_{A \to B} \Delta h_A, \Delta h_B) \approx +0.70 \text{ to } +0.80$$
This demonstrates that the **abstract geometric structure** of the relation is preserved across lexical realizations as a rigid rotation in $\mathcal{H}_l$.

### 3.2 The Downstream Causal Readout (Level B: Boundary Established)
Let the downstream transformer computation from layer $l$ to the final layer $L$ be $F_{l \to L}: \mathcal{H}_l \to \mathcal{H}_L$, followed by the unembedding head $W_U \in \mathbb{R}^{|\mathcal{V}| \times d}$.

The decision margin between target token $y_t$ and foil token $y_f$ is:
$$\text{Margin}(x) = (w_{y_t} - w_{y_f})^T h_L(x) = (w_{y_t} - w_{y_f})^T F_{l \to L}(h_l(x))$$

When injecting an intervention $v \in \mathcal{H}_l$:
$$h'_l(x) = h_l(x) + \alpha v$$
The resulting logit margin shift is governed by the downstream Jacobian $\mathcal{J}_{F}(h_l)$:
$$\Delta \text{Margin} \approx \alpha (w_{y_t} - w_{y_f})^T \mathcal{J}_{F}(h_l(x)) \, v$$

### 3.3 The Core Causal Null-Space Theorem
$$\boxed{\mathcal{J}_{F}(h_l(x)) \, b_{\text{dynamic}}(x) \approx 0 \quad \text{while} \quad (w_{y_t} - w_{y_f})^T \mathcal{J}_{F}(h_l(x)) \, v_{\text{output}}^{(l)} \gg 0}$$

**Theoretical Explanation:**
1. **The Positive Control ($v_{\text{output}}^{(l)}$):** The output bridge vector is constructed directly from the unembedding weights $w_{y_t} - w_{y_f}$. Because the residual stream preserves an unimpeded linear bypass to the unembedding layer ($\mathcal{J} \approx I + \sum \text{MLP} + \sum \text{Attn}$), $v_{\text{output}}$ bypasses the internal routing heads and directly tilts the output logits.
2. **The Dynamic Internal Basis ($b_{\text{dynamic}}$):** Rotating $B_{\text{agg}}$ via $R(x)$ aligns the vector in the ambient embedding space $\mathbb{R}^d$, but **fails to align with the specific query/key projection matrices $W_Q^{(l+1)}, W_K^{(l+1)}$ of downstream attention heads**. The downstream heads project $b_{\text{dynamic}}$ into their null space or treat it as off-manifold noise, resulting in zero behavioral rescue.

---

## 4. The 10 Epistemological Status Labels

In all scientific reporting and documentation generated by Muse agents, every statement of fact or deduction must carry one of the 10 constitutional epistemological tags:

1. `[FACT]`: Established mathematical theorem or standard computation (e.g., SVD of $E(x)^T E_0$ is orthogonal).
2. `[DEFINITION]`: Project standard mathematical definition from `theory/README_DEFINITIONS.md`.
3. `[HYPOTHESIS]`: Empirical proposition pre-registered for falsification prior to inspecting data.
4. `[CONJECTURE]`: Plausible conceptual intuition without formal proof or controlled empirical validation.
5. `[ASSUMPTION]`: Scope condition or boundary constraint imposed for analysis ($\Delta\theta = 0$).
6. `[PROPOSITION]`: Mathematical statement intended for formal derivation.
7. `[THEOREM]`: Formally proven result with complete derivation.
8. `[OBSERVATION]`: Empirical measurement from a controlled experiment with exact $p$-value and sample size.
9. `[INTERPRETATION]`: Scientific explanation or inductive inference drawn from an observation.
10. `[OPEN]`: Unresolved scientific frontier requiring further controlled experimentation.
