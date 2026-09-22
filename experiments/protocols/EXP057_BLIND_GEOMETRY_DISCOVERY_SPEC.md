# EXP057 Protocol Specification: Blind Task-Geometry Discovery

**Status:** PRE-REGISTERED  
**Date:** 2026-09-21  
**Predecessor Experiments:** EXP048, EXP049, EXP050, EXP056  
**Governing Standard:** `AGENTS.md` (14 Inviolable Laws) & `STATISTICAL_PROTOCOL_V02.md`  

---

## 1. Scientific Mandate & Objectives

In EXP056, the Representation Discovery Gap ($RDG$) was formally quantified:
$$RDG = M(\text{oracle-guided basis}) - M(\text{autonomous basis}) = 74.0\% - 64.0\% = 10.0\text{ percentage points}$$
proving that **autonomous representation discovery is the central unresolved bottleneck of SCPM**.

EXP057 tests whether SCPM can infer the task structure that determines its temporary representation **without being given token spans, distractor locations, target locations, or task-specific structural annotations**.

$$\boxed{\text{Can SCPM autonomously discover task-relevant computational geometry from raw token dynamics?}}$$

---

## 2. Invariant Constraints & Protocols

1. **Frozen Backbone:** Model parameters remain strictly invariant ($\Delta\theta = 0$, SHA-256 verified).
2. **Zero Oracle Spans:** No token offset mappings, distractor boundaries, or entity labels are provided.
3. **Zero Structural Metadata:** The task geometry type is completely hidden from SCPM.
4. **Zero Test-Label Leakage:** Target tokens are evaluated exclusively at output readout.
5. **Episodic Discard:** Temporary bases $B_t$ and memory buffers are completely wiped between instances.

---

## 3. The 8-Step Autonomous Hypothesis Lifecycle

```text
Prompt x ──► Forward Pass ──► Generate Hypotheses {H_geom} ──► Construct Bases {B_k}
                                                                      │
                                                                      ▼
Discard B_t ◄── Final Output ◄── Select Best ◄── Refine / Reject ◄── Counterfactual Eval
```

1. **Hypothesis Generation ($\mathcal{G}$):** From prompt hidden states $H \in \mathbb{R}^{L \times d}$, generate 6 structural candidate bases:
   - $B_{\text{hierarchical}}$: Subspace spanned by token depth decay.
   - $B_{\text{temporal}}$: Subspace spanned by sequential token lag differences $(h_t - h_{t-1})$.
   - $B_{\text{causal}}$: Subspace spanned by forward causal gradient projections.
   - $B_{\text{interaction}}$: Subspace spanned by cross-token interaction covariance.
   - $B_{\text{exclusion}}$: Subspace spanned by token set orthogonal complement.
   - $B_{\text{contrastive}}$: Subspace spanned by maximum variance token cluster.
2. **Basis Construction:** Compute rank-2 orthonormal projection matrices $P_k = V_k V_k^\top$.
3. **Intervention:** Apply transient modulation $h \leftarrow h - \alpha (h P_k)$ at Layer 7.
4. **Counterfactual Evaluation ($\mathcal{E}_{\text{cf}}$):** Score each basis by distribution sharpening (negative entropy) and perturbational stability without outcome labels.
5. **Rejection:** Discard hypotheses that fail to sharpen the distribution over baseline.
6. **Refinement:** Refine the top candidate via 1-step Gram-Schmidt alignment.
7. **Selection:** Elect winning representation $B_t^* = \arg\max_k \mathcal{E}_{\text{cf}}(B_k)$.
8. **Discard:** Reclaim memory buffers; verify state isolation.

---

## 4. Benchmark Suite: `BENCH-005-HIDDEN-GEOMETRY`

Evaluates $N=120$ instances ($20$ instances per geometry across $6$ distinct computational structures):
1. **Hierarchy:** Category depth & taxonomic inheritance.
2. **Temporal:** Chronological ordering & milestone progression.
3. **Causal:** Directed cause-effect chains.
4. **Interaction:** Non-linear conjunction & XOR logic.
5. **Exclusion:** Negation, set difference & mutual exclusivity.
6. **Distractor:** Lexical attractor competition.

---

## 5. Pre-Registered Hypotheses & Success Criteria

### 5.1 Primary Endpoint (Autonomous Discovery Over Controls):
$$M(\text{Autonomous SCPM}) > \max(M(\text{Random Basis}), M(\text{Prompt PCA})) \quad \text{with } p < 0.05$$

### 5.2 Secondary Endpoint (Representation Discovery Gap Reduction):
$$RDG_{\text{EXP057}} = M(\text{Oracle Basis}) - M(\text{Autonomous SCPM}) \le 6.0\text{ percentage points}$$
(A significant reduction from the $10.0\text{ pp}$ gap in EXP056).

---

## 6. Pre-Registered Falsification Criteria

Blind task-geometry discovery is **falsified** if:
1. Autonomous SCPM does not significantly outperform Prompt PCA or Random Basis ($p \ge 0.05$).
2. $RDG$ remains $\ge 10.0\text{ pp}$ across the 6 geometry suites.
3. The selected geometry matches the true underlying task geometry at a rate no better than chance ($1/6 \approx 16.7\%$).
