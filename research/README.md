# SCBI Research

## Self-Consistent Basis Invention

**Research Goal & Scientific Scope**

---

## 1. Purpose of This Document

This document defines the research goal, scientific scope, boundaries, terminology, and guiding principles for the SCBI research project.

It is the **highest-level research specification** for this repository.

All future:

* mathematical formulations
* implementations
* experiments
* evaluations
* literature reviews
* hypotheses
* benchmarks
* research claims
* paper drafts

must remain consistent with this document unless the research direction is deliberately revised and that revision is explicitly documented.

This document must **not** be silently changed to make experimental results look better.

---

# 2. What Is SCBI?

SCBI stands for:

> **Self-Consistent Basis Invention**

SCBI is a research concept investigating whether a frozen foundation model can perform useful **inference-time adaptation through temporary representations and states**, without modifying the underlying model parameters.

The central research idea is to investigate whether an inference system can temporarily construct, evaluate, modify, and retain useful representations while the underlying foundation model remains frozen.

The research focuses on the distinction between:

**changing the model**

and

**changing how information is represented and processed during inference.**

The current conceptual SCBI system therefore separates:

1. The frozen foundation model
2. Temporary inference state
3. Candidate representation / basis
4. Candidate generation
5. Candidate evaluation
6. Candidate selection
7. State evolution
8. Final inference

These components must remain conceptually distinguishable throughout the research.

---

# 3. Central Research Question

The primary question of this research is:

> **Can a frozen foundation model improve its inference behavior by dynamically constructing and selecting temporary representations during inference, without changing its underlying parameters?**

This is the central question.

All experiments should ultimately help answer this question or a clearly derived sub-question.

---

# 4. Core Hypothesis

The initial hypothesis is:

> A frozen foundation model may be able to improve its inference behavior when it is allowed to construct and evaluate temporary representations or coordinate systems that are optimized for the current inference problem.

This is a **research hypothesis**, not an established fact.

The project must never treat this hypothesis as proven merely because the mechanism appears theoretically plausible.

Evidence must come from:

* prior-art analysis
* mathematical analysis
* controlled experiments
* baseline comparisons
* ablation studies
* statistical analysis
* failure analysis
* independent reproduction where possible

---

# 5. What Remains Frozen?

A fundamental constraint of the core SCBI formulation is that the foundation-model parameters remain frozen.

Let:

$$
\theta
$$

represent the parameters of the underlying foundation model.

For the core SCBI experiments:

$$
\theta_{t+1} = \theta_t = \theta
$$

throughout inference.

In other words:

> **SCBI does not modify the underlying model parameters during the core experiment.**

This distinction is critical.

If an experiment updates the foundation-model parameters, that experiment must be explicitly labeled as a **variant**, not presented as the core SCBI mechanism.

---

# 6. What May Change?

Although the backbone remains frozen, SCBI investigates whether temporary inference-time variables can change.

The initial conceptual variables include:

### Frozen parameters

$$
\theta
$$

The underlying model parameters.

---

### Input

$$
x
$$

The current inference input.

---

### Temporary state

$$
z_t
$$

A temporary state maintained during inference.

The exact definition of \(z_t\) remains a research question and must be formally specified before implementation.

---

### Candidate basis / representation

$$
B_t
$$

A temporary candidate representation or coordinate system.

The precise mathematical meaning of "basis" must be established through the theoretical research rather than assumed from the name SCBI.

---

### Prediction

$$
\hat{y}_t
$$

The model's prediction at inference step \(t\).

---

### Evaluation objective

$$
\mathcal{L}
$$

An objective used to evaluate candidate states or representations.

The objective must be explicitly defined.

It must not be chosen after observing results simply to make SCBI perform better.

---

# 7. Conceptual SCBI Process

The current research concept can be represented as:

```text
Input
  │
  ▼
Frozen Foundation Model
       θ
  │
  ▼
Initial Representation
  │
  ▼
Temporary State z₀
  │
  ▼
Candidate Basis B₀
  │
  ▼
┌───────────────────────────────┐
│       SCBI Inference Loop     │
│                               │
│  Generate candidate           │
│          ↓                    │
│  Evaluate candidate           │
│          ↓                    │
│  Check consistency/objective  │
│          ↓                    │
│  Update / retain / discard    │
│          ↓                    │
│  Continue or terminate        │
└───────────────────────────────┘
  │
  ▼
Final Temporary State
  │
  ▼
Final Representation
  │
  ▼
Prediction
```

This diagram is **conceptual only**.

It must not be interpreted as the final algorithm.

The exact mechanism for:

* candidate generation
* evaluation
* consistency
* updating
* retention
* termination

must be established through research.

---

# 8. What Does "Self-Consistent" Mean?

The term **self-consistent** is currently a research hypothesis rather than a finalized mathematical definition.

The project must determine what consistency should mean.

Potential interpretations may include:

* consistency between candidate representations
* consistency between intermediate and final predictions
* stability across inference iterations
* agreement under transformations
* consistency between multiple candidate states
* improvement under an explicit objective
* internal agreement between representation and prediction

These possibilities must be investigated.

The implementation must **not arbitrarily choose one definition and then claim that it is the definitive meaning of SCBI.**

A formal definition must emerge from the theoretical research.

---

# 9. What Does "Basis" Mean?

The word **basis** is also provisional.

The research must determine whether \(B_t\) should mathematically represent:

* a linear basis
* a learned coordinate system
* a subspace
* a transformation
* a dictionary
* a latent representation
* an activation-space transformation
* another representation structure

The term must be formally defined before strong theoretical claims are made.

Until then:

> **B_t = temporary candidate representation / coordinate system**

should be treated as the working definition.

---

# 10. Research Objective

The overall objective is to determine whether SCBI provides a meaningful mechanism for inference-time adaptation under a frozen backbone.

The investigation should answer:

### A. Effectiveness

Does SCBI improve task performance?

### B. Causality

Is the improvement actually caused by the SCBI mechanism?

### C. Generalization

Does the improvement transfer across:

* tasks
* datasets
* inputs
* models
* distribution shifts

where appropriate?

### D. Efficiency

Does the improvement justify its additional inference computation?

### E. Stability

Does SCBI behave reliably or does the temporary state become unstable?

### F. Robustness

Does SCBI continue working under different seeds, configurations, and conditions?

### G. Mechanistic understanding

Can we understand *why* SCBI works when it works?

### H. Scientific novelty

Is the mechanism genuinely distinct from existing research?

---

# 11. Scientific Novelty Is an Open Question

SCBI must **not** initially be described as a novel method.

The research must first determine how SCBI relates to existing areas including:

* Test-Time Adaptation
* Test-Time Training
* Inference-Time Learning
* Inference-Time Optimization
* Online Learning
* Representation Learning
* Representation Engineering
* Activation Steering
* Latent-Space Optimization
* Prompt Optimization
* Self-Consistency
* Adaptive Inference
* Meta-Learning
* Model Editing
* Frozen-Model Adaptation

The possibility that SCBI overlaps heavily with an existing method is a valid research outcome.

If existing literature already contains the essential mechanism, the project should:

1. identify the overlap
2. document it
3. determine whether a meaningful distinction exists
4. revise the research question if necessary

The project must prioritize **scientific correctness over preserving the original name or hypothesis.**

---

# 12. What SCBI Is NOT

The core SCBI research should not automatically be interpreted as:

### Traditional fine-tuning

SCBI does not modify foundation-model parameters in the core formulation.

### Parameter-efficient fine-tuning

Methods such as adapters or LoRA should not automatically be considered SCBI.

They may be useful comparison methods, but they change trainable parameters.

### Prompt engineering

Changing a textual prompt alone is not sufficient to constitute SCBI.

### Retrieval-Augmented Generation

RAG may be a related or complementary technique, but retrieval itself is not SCBI.

### Chain-of-thought prompting

Generating longer reasoning traces does not automatically constitute SCBI.

### Self-consistency decoding

The relationship between SCBI and self-consistency must be experimentally and theoretically investigated rather than assumed.

### Model editing

SCBI should not modify persistent model knowledge unless a clearly defined variant is being studied.

---

# 13. Core Research Boundaries

The following boundaries should remain active throughout the project.

## Boundary 1 — Frozen backbone

Core experiments must keep \(\theta\) frozen.

## Boundary 2 — Temporary adaptation

SCBI adaptation should be temporary unless an experiment explicitly investigates persistence.

## Boundary 3 — No hidden training

The system must not secretly train model parameters.

## Boundary 4 — No test-set leakage

Evaluation information must not be used improperly to optimize the method.

## Boundary 5 — No post-hoc metric selection

Metrics must be defined before results are analyzed.

## Boundary 6 — No cherry-picking

Failed experiments must remain recorded.

## Boundary 7 — Equal-compute comparisons

When comparing methods, additional inference computation must be measured and reported.

## Boundary 8 — Reproducibility

Experiments must be reproducible from recorded configurations.

## Boundary 9 — Evidence before claims

A result must exist before a result is claimed.

## Boundary 10 — Literature before novelty

Prior-art analysis must precede novelty claims.

---

# 14. Primary Scientific Questions

The project should progressively answer the following questions.

## Q1 — Does SCBI work?

Can temporary inference-time representation adaptation improve predictions?

## Q2 — Is the improvement meaningful?

Is the improvement large enough to matter?

## Q3 — Is it caused by SCBI?

Could the same improvement be obtained through a simpler mechanism?

## Q4 — Is SCBI better than simpler alternatives?

For example:

* fixed representation
* random representation
* simple state adaptation
* representation-only adaptation
* compute-matched search

## Q5 — Why does it work?

Can we identify a mechanism explaining the improvement?

## Q6 — When does it fail?

Understanding failure is as important as understanding success.

## Q7 — How expensive is it?

What additional:

* latency
* memory
* FLOPs
* inference steps
* candidate evaluations

does SCBI require?

## Q8 — Does it generalize?

Does it work beyond one model and one benchmark?

## Q9 — Is it stable?

Does it behave consistently across seeds and conditions?

## Q10 — Is it genuinely different?

What distinguishes SCBI from existing approaches?

---

# 15. Research Philosophy

The project follows a falsification-first philosophy.

The default attitude should be:

> **"Assume the hypothesis could be wrong, then design experiments capable of showing that it is wrong."**

This is preferable to:

> "Find experiments that demonstrate SCBI works."

A strong negative result can be more scientifically valuable than a weak positive result.

---

# 16. Evidence Hierarchy

Evidence should be considered in approximately this order:

### Level 1 — Mathematical consistency

Is the formulation internally coherent?

### Level 2 — Controlled toy experiments

Does the mechanism work in a simple environment?

### Level 3 — Benchmark experiments

Does it work on realistic tasks?

### Level 4 — Baseline comparisons

Does it outperform credible alternatives?

### Level 5 — Ablation studies

Can the contribution of each component be isolated?

### Level 6 — Reproduction

Can results be reproduced?

### Level 7 — Cross-model validation

Does the mechanism survive different architectures?

### Level 8 — Independent validation

Can another researcher reproduce or validate the finding?

Strong scientific claims should require correspondingly strong evidence.

---

# 17. Positive Results Are Not Enough

Suppose SCBI obtains:

```text
Baseline: 72.1%
SCBI:      75.4%
```

That does **not** automatically establish that SCBI works.

We must investigate:

* Did SCBI use more computation?
* Did SCBI see additional information?
* Was the baseline properly tuned?
* Was the evaluation set indirectly used?
* Was the result dependent on one random seed?
* Does a simpler representation search produce the same result?
* Does random search achieve the same improvement?
* Does increasing inference compute alone produce the improvement?
* Does the effect disappear on another dataset?
* Does the effect disappear with another model?

The research must distinguish:

> **observed improvement**

from:

> **causal evidence for the proposed mechanism.**

---

# 18. Negative Results

Negative results must be preserved.

Examples include:

```text
SCBI fails on Dataset A.
SCBI becomes unstable after N iterations.
SCBI provides no improvement over compute-matched search.
SCBI improves accuracy but doubles latency.
SCBI works only on one model family.
SCBI collapses under distribution shift.
```

These are legitimate scientific findings.

They must never be deleted merely because they weaken the narrative.

---

# 19. Research Drift Prevention

The project must not gradually change from:

> inference-time representation adaptation

into:

> fine-tuning

simply because fine-tuning performs better.

Similarly, the project must not gradually change from:

> frozen model

into:

> trainable model

without explicitly declaring a new research variant.

Every major conceptual change must be documented in:

```text
reports/research_log.md
```

with:

```text
Previous definition:
New definition:
Reason for change:
Evidence motivating change:
Effect on research questions:
Effect on previous experiments:
```

Previous results must never be silently reinterpreted as results for the new definition.

---

# 20. Research Variants

If alternative mechanisms are explored, they must receive explicit names.

For example:

```text
SCBI-Core
SCBI-State
SCBI-Basis
SCBI-Persistent
SCBI-Parameter-Updated
```

These names are placeholders.

They should only be introduced when the corresponding variants are formally defined.

The core method and variants must never be mixed in reports.

---

# 21. Experimental Discipline

Every experiment must answer a specific question.

Before execution, record:

```text
Experiment ID:
Research Question:
Hypothesis:
Null Hypothesis:
Model:
Dataset:
Baseline:
SCBI Configuration:
Compute Budget:
Metrics:
Seeds:
Expected Outcome:
Falsification Condition:
```

After execution:

```text
Observed Result:
Variance:
Runtime:
Memory:
Interpretation:
Failure Cases:
Alternative Explanation:
Reviewer Criticism:
Conclusion:
```

---

# 22. Computational Efficiency

SCBI potentially introduces additional inference computation because it may evaluate multiple candidate representations.

Therefore, accuracy alone is insufficient.

The research must measure:

* inference latency
* number of candidate evaluations
* number of inference iterations
* memory usage
* approximate compute
* throughput
* scaling behavior

The research should investigate:

> **Does the additional computation produce enough improvement to justify itself?**

---

# 23. Reproducibility Requirements

Every meaningful experiment must record:

```text
Model
Model version
Dataset
Dataset version
Dataset split
Random seed
SCBI configuration
Baseline configuration
Inference steps
Candidate count
Evaluation objective
Hardware
Software environment
Python version
Dependencies
Git commit
Runtime
Results
```

A result that cannot be reproduced must be labeled accordingly.

---

# 24. Implementation Principle

The implementation should follow the research specification.

The research specification should **not** be changed merely to accommodate the implementation.

If implementation difficulty reveals that a definition is ambiguous:

1. stop
2. document the ambiguity
3. resolve it theoretically
4. update the specification
5. then implement

This prevents implementation decisions from accidentally becoming research assumptions.

---

# 25. Separation of Responsibilities

The repository should maintain clear separation:

```text
Literature
    │
    ▼
Research Gap
    │
    ▼
Hypothesis
    │
    ▼
Theory
    │
    ▼
Algorithm
    │
    ▼
Implementation
    │
    ▼
Experiment
    │
    ▼
Evaluation
    │
    ▼
Adversarial Review
    │
    ▼
Conclusion
```

No stage should be skipped simply because a later stage is easier.

---

# 26. Expected Research Outcomes

At the end of the investigation, several outcomes are acceptable.

### Outcome A — Strong support

SCBI demonstrates meaningful improvement with convincing evidence.

### Outcome B — Partial support

SCBI works under specific conditions but has important limitations.

### Outcome C — Negative result

SCBI does not provide meaningful improvement.

### Outcome D — Existing method

The central mechanism substantially overlaps with existing research.

### Outcome E — Reformulation

The original SCBI idea is insufficiently defined or motivated and must be reformulated.

All five are scientifically valid.

The project is successful if it discovers the truth about the hypothesis—not only if the hypothesis succeeds.

---

# 27. Definition of Research Success

The project should not define success as:

> "SCBI beats a benchmark."

Instead, success means:

> **We can provide a rigorous, reproducible, evidence-based answer about whether inference-time representation/state adaptation under a frozen foundation model provides a meaningful and distinguishable capability.**

A successful research program should eventually be able to explain:

1. What SCBI is.
2. Why it should work.
3. When it works.
4. When it fails.
5. How much it costs.
6. How it compares with existing methods.
7. What mechanism produces the observed behavior.
8. Whether the contribution is genuinely distinct from prior work.

---

# 28. Non-Negotiable Research Rules

These rules apply to every future SCBI document.

### Rule 1

**Never fabricate evidence.**

### Rule 2

**Never fabricate citations.**

### Rule 3

**Never claim novelty prematurely.**

### Rule 4

**Never hide negative results.**

### Rule 5

**Never silently fine-tune the backbone.**

### Rule 6

**Never change an experiment after seeing its result without documenting the change.**

### Rule 7

**Never choose metrics after seeing results.**

### Rule 8

**Never compare SCBI against intentionally weak baselines.**

### Rule 9

**Never confuse correlation with causation.**

### Rule 10

**Never allow implementation convenience to redefine the scientific hypothesis.**

### Rule 11

**Every major claim must have evidence.**

### Rule 12

**Every experimental result must have a reproducible configuration.**

### Rule 13

**Every research assumption must be explicitly documented.**

### Rule 14

**Every major conceptual change must be versioned and logged.**

### Rule 15

**The research is allowed to conclude that SCBI does not work.**

---

# 29. Current Research Status

```text
Research name:
SCBI

Full name:
Self-Consistent Basis Invention

Research stage:
Conceptual investigation

Core hypothesis:
Inference-time adaptation through temporary representation/state
modification while keeping the foundation-model parameters frozen.

Backbone:
Frozen

Mathematical formulation:
Not finalized

Algorithm:
Not finalized

Literature audit:
Required

Novelty:
UNKNOWN

Experimental evidence:
Not established

Benchmark results:
Not established

Theoretical guarantees:
Not established

Production readiness:
Not applicable

Paper readiness:
Not applicable
```

---

# 30. Immediate Research Priority

Before implementing a large SCBI system, the research should establish:

```text
1. Precise definition of SCBI
          ↓
2. Literature / prior-art audit
          ↓
3. Mathematical formulation
          ↓
4. Minimal algorithm
          ↓
5. Strong baseline selection
          ↓
6. Minimal falsification experiment
          ↓
7. Controlled evaluation
          ↓
8. Adversarial review
```

The project must **not skip directly from the concept to a large-scale implementation.**

---

# 31. Source of Truth

This README defines the current high-level research scope.

More detailed documents may refine:

* mathematical definitions
* algorithmic details
* experimental protocols
* implementation decisions

but they must not silently contradict this document.

When a conflict exists, the conflict must be explicitly identified and resolved.

---

# 32. Final Principle

The purpose of SCBI research is not to prove that SCBI is brilliant.

The purpose is to determine:

> **whether the underlying idea represents a real, useful, measurable, and scientifically defensible capability.**

If the evidence supports SCBI, the research should make the strongest defensible claim.

If the evidence contradicts SCBI, the research should preserve that result.

If existing literature already contains the core idea, the research should acknowledge it and identify whether there remains a meaningful contribution.

The standard for this project is therefore:

**Evidence over narrative.
Reproducibility over speed.
Falsification over confirmation.
Scientific accuracy over novelty claims.**
