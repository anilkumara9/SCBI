# Rule 02: Theoretical Framework & Mathematical Invariants

**Applies to:** All theoretical derivations, mathematical formulations, proof structures, and formal definitions.  
**Foundational Documents:**
- [`documentation/theory.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/documentation/theory.md) (SCBI Mathematical Research Specification)
- [`documentation/math.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/documentation/math.md) (SCBI Theory Specification)
- [`documentation/README_DEFINITIONS.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/documentation/README_DEFINITIONS.md) (SCBI Formal Definitions)

---

## 1. The Frozen-Backbone Invariant (Non-Negotiable)

In all core SCBI mathematical specifications:

$$\boxed{\theta_t = \theta_0 \quad \forall t \in \{0, 1, \dots, T\} \implies \Delta\theta_t = 0}$$

### Absolute Prohibitions for Core SCBI:
Under no circumstances may any theoretical derivation or model assumption for core SCBI rely upon:
- Gradient updates to weight matrices ($W, b$);
- Optimization of parameter-efficient fine-tuning (PEFT) weights (LoRA, adapters, soft prompt embeddings);
- Shifting running statistics (e.g., BatchNorm, LayerNorm persistent affine parameters);
- Optimizer state carrying over between independent inference instances.

**Variant Boundary:** Any framework where $\Delta\theta \ne 0$ is NOT core SCBI and must be mathematically designated with the suffix `[VARIANT]` (e.g., `SCBI-PT`, `SCBI-Adapter`) per [`theory.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/documentation/theory.md) §7.

---

## 2. Mathematical Spaces & Universe

All formulations must strictly operate within the mathematical universe defined in [`theory.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/documentation/theory.md) §5:

- $\Theta$: Parameter space of the foundation model ($f_\theta: \mathcal{X} \to \mathcal{Y}$).
- $\mathcal{X}$: Input space instance $x \in \mathcal{X}$.
- $\mathcal{Y}$: Output/prediction space $\hat{y} \in \mathcal{Y}$ and optional ground truth $y \in \mathcal{Y}$.
- $\mathcal{H}$: Intermediate activation / hidden-state space $h \in \mathcal{H}$.
- $\mathcal{Z}$: Temporary inference-time state space $z_t \in \mathcal{Z}$.
- $\mathcal{B}$: Admissible space of temporary representation objects $B_t \in \mathcal{B}$.

---

## 3. Formal Decomposition of the SCBI Step

Every theoretical formulation of an SCBI inference step $t \to t+1$ must be explicitly decomposed into the formal operators specified in [`math.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/documentation/math.md):

1. **Candidate Generation:**
   $$\mathcal{G}: (x, z_t, \theta_0) \to \{B_{t,1}, B_{t,2}, \dots, B_{t,K}\} \subset \mathcal{B}$$
2. **Candidate Evaluation (Self-Consistency / Objective):**
   $$\mathcal{E}: (B_{t,k}, x, z_t, \theta_0) \to \mathbb{R}$$
   *(Note: The objective must be mathematically defined, e.g., energy minimization, cycle consistency, reconstruction stability, or likelihood consensus. It cannot remain an informal heuristic.)*
3. **Candidate Selection:**
   $$B_t^* = \mathcal{S}\left(\{B_{t,k}\}, \{\mathcal{E}(B_{t,k})\}\right) = \arg\min_k \mathcal{E}(B_{t,k})$$
4. **State Transition:**
   $$z_{t+1} = \mathcal{T}(z_t, B_t^*, x, \theta_0)$$
5. **Inference Readout:**
   $$\hat{y}_t = f_\theta(x; z_t, B_t^*)$$

---

## 4. Bounded Computational Budget

Every theoretical algorithm must explicitly specify its inference budget $T < \infty$ and per-step complexity $\mathcal{O}(C_{\text{step}})$.
- Infinite asymptotic loops without explicit convergence guarantees are disallowed.
- If convergence proofs are attempted, the contraction mapping or Lyapunov function must be formally identified.

---

## 5. Definition Change Protocol

No agent may alter a definition in [`README_DEFINITIONS.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/documentation/README_DEFINITIONS.md) without:
1. Identifying whether the definition is `Fixed` or `Working`;
2. Documenting the theoretical inconsistency or literature evidence necessitating the change;
3. Recording backward compatibility impact on existing proofs and benchmark code;
4. Formally tagging the revision with a changelog entry.
