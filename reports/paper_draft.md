# Self-Consistent Basis Invention: Inference-Time Representation Adaptation under Frozen Backbone Constraints

**Authors:** SCBI Research Consortium  
**Document Status:** Working Draft  
**Governing Protocol:** [`reports/README.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/reports/README.md), [`.agents/skills/paper-writing/SKILL.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/skills/paper-writing/SKILL.md)

---

## Abstract

We investigate **Self-Consistent Basis Invention (SCBI)**, an inference-time adaptation paradigm examining whether a frozen foundation model ($\Delta\theta = 0$) can improve task performance through the dynamic construction, evaluation, and selection of temporary representation coordinate frames ($B_t$). Operating strictly within transient state boundaries, SCBI separates candidate generation, self-consistency evaluation, and state transition without modifying model weights. Under compute-matched evaluation controls equalizing inference FLOPs against test-time sampling baselines, we evaluate the validity of the SCBI hypothesis across benchmark suites. We present complete empirical ablations, statistical significance bounds, and an analysis of identified failure regimes.

---

## 1. Introduction

Central Research Question:
> *Can a frozen foundation model improve its inference behavior by dynamically constructing and selecting temporary representations during inference, without changing its underlying parameters?* ([`research/README.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/research/README.md) §3)

### Contributions
1. **Theoretical Specification:** Formal decomposition of the inference step into operators $(\mathcal{G}, \mathcal{E}, \mathcal{S}, \mathcal{T})$ preserving the strict parameter invariant $\theta_t = \theta_0$.
2. **Prior-Art Equivalence Analysis:** Exhaustive taxonomic positioning against test-time adaptation, representation engineering, soft prompting, and dictionary learning.
3. **Compute-Matched Empirical Benchmark:** Controlled evaluation against forward-pass-equalized baselines with 5 mandatory ablations and failure mode profiling.

---

## 2. Related Work & Prior-Art Positioning

*(Full taxonomy matrix comparing SCBI against TTA, steering vectors, dynamic prompt tuning, KV cache editing, and sparse autoencoders)*

---

## 3. Mathematical Formulation

- Parameter Space: $\Theta$ with $\theta \in \Theta$
- Input & Output Spaces: $\mathcal{X}, \mathcal{Y}$
- State & Basis Spaces: $\mathcal{Z}, \mathcal{B}$
- Step Tuple: $(\mathcal{G}, \mathcal{E}, \mathcal{S}, \mathcal{T})$

---

## 4. Empirical Evaluation

- Compute-Budget Matching:
- Primary & Secondary Metrics:
- 5-Part Ablation Suite:
- Statistical Significance:

---

## 5. Limitations, Failure Modes & Negative Results

*(Objective documentation of computational overhead, convergence limits, and failure conditions)*

---

## 6. Conclusion & Future Work

*(Empirically bounded conclusion avoiding speculative claims)*
