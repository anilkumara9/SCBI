# Self-Consistent Basis Invention (SCBI)

## Research Repository

SCBI investigates whether a frozen foundation model can improve inference behavior through temporary inference-time representation construction and selection.

> [!IMPORTANT]
> **Meta Muse Research Swarm Handover:**
> The complete autonomous research handover package, 6-agent swarm specifications, formal mathematical theory, 66-experiment compendium, and the 4-phase roadmap to revolutionize AI are accessible in [`.muse by meta/`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.muse%20by%20meta/).
> 
> **Current Scientific Milestone (EXP066 Confirmed):**
> Cross-scale replication on `EleutherAI/pythia-410m` confirmed that the **representational–causal dissociation replicates across Pythia scale (160M $\to$ 410M)** with $\Delta\theta \equiv 0$ strictly verified.

---

## Core Research Question

> Can a frozen foundation model improve its inference behavior by dynamically constructing and selecting temporary representations during inference without changing its underlying parameters?

---

## Core Constraint

$$
\boxed{\theta_t=\theta_0}
$$

The foundation-model parameters remain frozen in core SCBI experiments.

---

## Conceptual Pipeline

```text
Input
  ↓
Frozen Foundation Model
  ↓
Initial Representation
  ↓
Temporary State
  ↓
Candidate Representations
  ↓
Candidate Evaluation
  ↓
Selection / Acceptance
  ↓
Temporary Representation Update
  ↓
Repeat
  ↓
Final Representation
  ↓
Prediction
```

---

## Important Status

SCBI is a research hypothesis.

The following are currently NOT established:

* effectiveness;
* novelty;
* superiority;
* theoretical guarantees;
* convergence;
* generalization;
* computational advantage.

---

## Repository Structure

```text
research/
├── README.md
├── README_LITERATURE.md
├── literature/
├── related_work/
├── hypotheses/
├── research_gaps/
└── bibliography/

theory/
├── README.md
├── README_DEFINITIONS.md
├── README_ASSUMPTIONS.md
├── README_FORMULATION.md
├── README_ALGORITHM.md
├── README_COMPLEXITY.md
└── proofs/

scbi/
├── README.md
├── core/
├── models/
├── representations/
├── state/
├── optimization/
└── baselines/

experiments/
├── README.md
├── configs/
├── scripts/
├── runs/
├── checkpoints/
└── results/

evaluation/
├── README.md
├── metrics/
├── statistical_tests/
├── ablations/
└── failure_analysis/

reports/
├── README.md
├── research_log.md
├── literature_review.md
├── experiment_report.md
├── novelty_report.md
└── paper_draft.md
```

---

## Source-of-Truth Hierarchy

### Definitions

```text
theory/README_DEFINITIONS.md
```

### Mathematical specification

```text
theory/README.md
```

### Assumptions

```text
theory/README_ASSUMPTIONS.md
```

### Literature

```text
research/README_LITERATURE.md
```

### Algorithm

```text
theory/README_ALGORITHM.md
```

### Implementation

```text
scbi/README.md
```

### Experiments

```text
experiments/README.md
```

### Evaluation

```text
evaluation/README.md
```

---

## Agent Rules

Antigravity must:

1. read the relevant README before modifying that area;
2. never invent research results;
3. never fabricate citations;
4. never silently modify the hypothesis;
5. never silently change mathematical definitions;
6. never update frozen parameters in core SCBI;
7. never use test labels without declaring the experiment;
8. never delete failed experiments;
9. never select metrics after seeing results;
10. never claim novelty without prior-art analysis;
11. distinguish observation from interpretation;
12. document major research decisions;
13. preserve reproducibility;
14. challenge the hypothesis rather than defend it.

---

## Research Philosophy

The goal is not to make SCBI appear successful.

The goal is to determine scientifically:

> **What SCBI actually is, whether it differs from existing approaches, whether it works, why it works if it works, and under what conditions it fails.**

A negative result is scientifically valuable.

An overlap with existing work is scientifically valuable.

A reformulation is scientifically valuable.

Only evidence should determine the final conclusion.

---

## Current Research State

```text
Research goal: defined
Terminology: provisionally defined
Mathematical specification: provisionally defined
Literature audit: required
Final formulation: open
Algorithm: open
Implementation: not yet validated
Experiments: not yet established
Effectiveness: unknown
Novelty: unknown
```

---

## First Priority

Before building a sophisticated implementation:

```text
1. Audit prior art
2. Identify closest methods
3. Attack the hypothesis
4. Select/formalize the minimal formulation
5. Implement the smallest falsifiable prototype
6. Verify frozen parameters
7. Establish a strong baseline
8. Run controlled experiments
9. Perform ablations
10. Analyze failures
```

---

## Final Principle

> **Do not let the implementation define the science. Let the science define the implementation, and let evidence determine the conclusion.**
