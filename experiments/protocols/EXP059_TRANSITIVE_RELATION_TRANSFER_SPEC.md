# EXP059 Protocol Specification: Transitive Relational Transfer Across Disjoint Surface Domains

**Status:** PRE-REGISTERED (Falsification-Oriented)  
**Date:** 2026-09-21  
**Predecessor Experiments:** EXP027, EXP056, EXP057, EXP058  
**Governing Standard:** `AGENTS.md` (14 Inviolable Laws) & `STATISTICAL_PROTOCOL_V02.md`  

---

## 1. Scientific Mandate & Core Question

Following the empirical diagnostic failures of EXP057 (benchmark validity breakdown, ungrounded entropy selection) and EXP058 (surface-bound lexical coupling, $\tau = 0.0\%$), EXP059 radically simplifies the relational target to a single controllable latent world:

$$\boxed{\textbf{Strict Transitive Ordering: } A > B \;\wedge\; B > C \implies A > C}$$

The core research question is:
$$\boxed{\textbf{Can an inference-time discovery procedure identify an intervention whose causal utility is invariant under surface-form transformations?}}$$

### Defensible Novelty Claim
We do not claim that finding activation directions or modifying inference activations is novel (established in RepE, Turner et al., Rimsky et al.). The narrow, testable hypothesis is:
$$\boxed{\textbf{whether an automatically discovered, temporary intervention can encode a task relation and transfer that intervention across deliberately disjoint surface realizations without modifying model parameters.}}$$

---

## 2. Five Pre-Registered Falsifiable Hypotheses

| Hypothesis | Test Description | Formal Falsification Criterion |
| :--- | :--- | :--- |
| **H1: Causal Intervention** | Discovered intervention improves 2-hop transitive deduction over frozen baseline. | $\Delta M_{\text{transitive}} \le 0$ (No statistically significant improvement over baseline). |
| **H2: Relation Specificity** | Intervention helps transitive queries ($A > B, B > C \implies A > C$) but does not improve matched invalid controls ($A > B, C > B \implies A > C$). | $\Delta M_{\text{transitive}} \le \Delta M_{\text{control}}$ (Equal or greater effect on structurally invalid controls). |
| **H3: Surface Invariance** | Intervention discovered on Domain A transfers to held-out Domains B, C, D with strictly disjoint lexical vocabulary. | Headroom retention $\tau_{\text{disjoint}} < 0.30$ or $\Delta M_{\text{transfer}} \le 0$ on held-out vocabulary. |
| **H4: Causal Necessity** | Scrambling, reversing, or orthogonalizing the intervention direction eliminates the behavioral gain. | Perturbed/scrambled intervention retains $\ge 70\%$ of the unperturbed benefit. |
| **H5: Reusability** | The discovered intervention generalizes across independent test instances sharing the latent relation. | Benefit exists only on discovery instances ($M_{\text{heldout}} \le M_{\text{base}}$). |

---

## 3. Disjoint Surface Realizations & Matched Relational Controls

### 3.1 Latent Relation
The invariant underlying relational logic is strict linear order: $R(x, y) = 1$ denotes "$x$ precedes $y$ / $x$ outranks $y$". The target deduction is 2-hop transitively implied relation $R(a, c) = 1$.

### 3.2 Five Disjoint Vocabulary Domains ($100\%$ Lexical Isolation)
1. **Domain 0 (Discovery Set):** Social Rank (`Alice`, `Bob`, `Charlie`, `David`, `Emma`)
2. **Domain 1 (Held-Out Names):** Novel Names (`Mira`, `Delta`, `Nova`, `Orion`, `Kael`)
3. **Domain 2 (Biomedical Signaling):** Biochemical Casework (`Kinase-A`, `Protein-B`, `Enzyme-C`, `Receptor-D`)
4. **Domain 3 (Industrial Priority):** Machine Hierarchy (`Unit-1`, `Reactor-2`, `Turbine-3`, `Generator-4`)
5. **Domain 4 (Abstract Symbolic):** Pure Symbols (`Alpha`, `Beta`, `Gamma`, `Delta`)

### 3.3 Matched Relational Controls (Structural Discrimination)
To prevent the intervention from exploiting simple token co-occurrence:
- **Valid Transitive ($R=1$):** $A > B$ and $B > C \implies$ Query: *"Who is higher, A or C?"* $\to$ Correct: **A**.
- **Invalid Common Target ($R=\emptyset$):** $A > B$ and $C > B \implies$ Query: *"Does A outrank C?"* $\to$ Correct: **Unknown / Neither**.
- **Inverted Order ($R=-1$):** $B > A$ and $C > B \implies$ Query: *"Who is higher, A or C?"* $\to$ Correct: **C**.

---

## 4. Intervention Formulation & Candidate Families

Rather than assuming a single linear basis (PCA), EXP059 compares three candidate representation structures:
1. **Subspace Projection (Linear Rank-2):** $P_V = V V^T$ with directional injection $h \leftarrow h + \alpha (h P_V)$.
2. **Contrastive Direction Vector (CAA-style):** $v = \frac{\mu_{\text{valid}} - \mu_{\text{invalid}}}{\|\mu_{\text{valid}} - \mu_{\text{invalid}}\|}$, $h \leftarrow h + \alpha v$.
3. **Soft Conceptor Operator (Jaeger 2014):** $C = X (X^T X + \lambda^{-2} I)^{-1} X^T$.

### Grounded Counterfactual Utility Selection (Not Entropy)
Candidates are evaluated on a small held-out calibration split in Domain 0 by measuring **discriminative margin gain**:
$$U(c) = \Delta \mathrm{Margin}(y_{\text{target}}, y_{\text{foil}}) - \Delta \mathrm{Margin}_{\text{control}}$$
Selecting the candidate that maximizes relational discrimination, avoiding ungrounded entropy traps.

---

## 5. Pre-Registered Decision Gate

- If H1, H2, H3, and H4 are supported: **RELATION_LEVEL_TRANSFER_SUPPORTED** (first controlled evidence of surface-invariant relational transfer).
- If H1 fails: **TRANSITIVE_INTERVENTION_INEFFECTIVE** (Pythia-160M cannot be steered on transitive reasoning).
- If H3 fails while H1 passes: **SURFACE_BOUND_ACTIVATION_GEOMETRY** (Interventions remain tied to lexical artifacts).
- If H2 fails: **NON_SPECIFIC_PERTURBATION** (Intervention acts as generic non-relational noise).
