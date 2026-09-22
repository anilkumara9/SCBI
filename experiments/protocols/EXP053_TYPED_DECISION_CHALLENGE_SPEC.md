# EXP053 Protocol Specification: Continuous Subspace Invention vs. Typed Decision Systems

**Status:** PRE-REGISTERED  
**Date:** 2026-09-21  
**Predecessor Experiments:** EXP048, EXP052  
**Governing Standard:** `AGENTS.md` (14 Inviolable Laws) & `STATISTICAL_PROTOCOL_V02.md`  

---

## 1. Scientific Context & Mandate

An important external challenge to latent continuous representation modification comes from **discrete typed decision systems** (e.g., Jev/Laya-style architectures), which enforce explicit symbolic type schemas, syntactic grammars, or discrete validation rules during inference.

The scientific objective of EXP053 is NOT to "beat Jev on one benchmark," but to determine the **functional division of labor** between continuous cognitive basis invention ($B_t$) and discrete typed decision mechanisms.

$$\boxed{\text{What are the complementary regimes of continuous representation invention vs. discrete typed decision systems?}}$$

---

## 2. System Implementations & Architecture

| Condition | Modality | Mechanism | Where Applied |
| :--- | :--- | :--- | :--- |
| **System 0: Baseline** | Unconstrained | Standard greedy autoregressive decoding | Logits / Next token |
| **System 1: SCPM ($M_\theta + B_t$)** | Continuous Latent | Instance-level subspace projection $P_c = V_c V_c^\top$ | Layer 7 residual stream |
| **System 2: Typed Decision (Jev/Laya)** | Discrete Symbolic | Type-schema validator & grammar-constrained token masking | Output vocabulary projection |
| **System 3: Hybrid ($M_\theta + B_t + \text{Typed}$)** | Dual-Level Coupled | Subspace projection in Layer 7 + typed schema masking at output | Layer 7 + Output |

---

## 3. Pre-Registered Hypotheses & Success Criteria

### 3.1 Orthogonality Hypothesis ($H_{\text{ortho}}$):
- Continuous basis invention ($B_t$) resolves **associative semantic interference** (where distractors cause wrong token associations despite valid syntax).
- Typed decision systems resolve **discrete type/constraint violations** (where outputs violate problem grammar or type constraints).
- On purely semantic interference instances:
  $$\Delta M_{B_t} > \Delta M_{\text{Typed}} \quad (p < 0.05)$$
- On syntax/type-constrained instances:
  $$\Delta M_{\text{Typed}} > \Delta M_{B_t} \quad (p < 0.05)$$

### 3.2 Constructive Synergy Hypothesis ($H_{\text{synergy}}$):
The hybrid system achieves strict Pareto dominance over both individual systems:
$$M_{\text{Hybrid}} > \max(M_{B_t}, M_{\text{Typed}}) \quad \text{with } p < 0.01$$
demonstrating that continuous representation invention and typed decision systems are orthogonal, non-redundant cognitive modules.

---

## 4. Pre-Registered Falsification Criteria

Continuous basis invention is **falsified as a redundant mechanism** if:
1. Pure typed decision systems match or exceed SCPM across *all* instances, including associative semantic interference ($M_{\text{Typed}} \ge M_{B_t}$ uniformly).
2. The hybrid system provides zero marginal benefit over the pure typed decision system ($M_{\text{Hybrid}} = M_{\text{Typed}}$).

---

## 5. Epistemological Interpretation Matrix

| Outcome | Epistemological Status | Interpretation |
| :--- | :--- | :--- |
| **Orthogonality confirmed** | `[OBSERVATION]` | Demonstrates that continuous latent basis invention operates at the semantic representation level, serving as a distinct cognitive substrate that cannot be replaced by external symbolic/typed constraints. |
| **Typed systems dominate uniformly** | `[OBSERVATION]` | Concludes that inference control should be conducted purely symbolically at the token/type interface, rendering continuous internal basis manipulation obsolete. |
