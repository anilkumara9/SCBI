# SCBI Experimental Protocol

## 1. Purpose

This document defines how SCBI experiments must be designed, executed, recorded, and interpreted.

---

## 2. Experimental Principle

Every experiment must answer a specific research question.

Do not run experiments merely because they are easy to run.

---

## 3. Experiment Structure

Every experiment must contain:

```text
Research question
Hypothesis
Independent variable
Dependent variable
Controls
Baseline
Dataset
Model
Configuration
Compute budget
Information boundary
Metrics
Expected outcome
Falsification condition
```

---

## 4. Experiment IDs

Use:

```text
EXP001
EXP002
EXP003
...
```

Never overwrite previous experiment definitions.

---

## 5. Experiment Lifecycle

```text
Design
→ Review
→ Implement
→ Validate
→ Run baseline
→ Run SCBI
→ Run controls
→ Analyze
→ Review
→ Archive
```

---

## 6. First Experiments

Recommended order:

### EXP001

**Frozen baseline correctness & minimal subspace prototype.**  
- Config: [`experiments/configs/EXP001_minimal_prototype.yaml`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/experiments/configs/EXP001_minimal_prototype.yaml)  
- Target Hypothesis: [`research/hypotheses/H001_subspace_basis_invention.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/research/hypotheses/H001_subspace_basis_invention.md)  
- Tests: Backbone immutability, candidate generation $\mathcal{G}$, self-consistency evaluation $\mathcal{E}$, and compute-matched sampling.

### EXP002

Minimal SCBI functionality on multi-attribute interference tasks.

### EXP003

Baseline vs SCBI.

### EXP004

Random representation control.

### EXP005

No-selection ablation.

### EXP006

No-consistency ablation.

### EXP007

Compute-matched baseline.

### EXP008

Iteration scaling.

### EXP009

Candidate-count scaling.

### EXP010

Robustness.

---

## 7. Required Controls

At minimum consider:

```text
Frozen baseline
Random representation
Fixed representation
Extra-compute baseline
SCBI without selection
SCBI without consistency
SCBI with one iteration
SCBI with multiple iterations
```

---

## 8. Seeds

Stochastic experiments should use multiple seeds.

Record every seed.

---

## 9. Dataset Splits

Never tune the final system on the test set.

---

## 10. Failure Recording

Failures must be stored.

Record:

```text
failure
cause
conditions
logs
possible explanation
whether reproduced
```

---

## 11. No Result Deletion

Do not delete unsuccessful experiments merely because they weaken the hypothesis.

---

## 12. Experiment Metadata

Each run should record:

```text
experiment ID
timestamp
git commit
model
dataset
seed
configuration
hardware
runtime
memory
parameter hash
results
```

---

## 13. Result Interpretation

Use:

```text
Observation
Interpretation
Alternative explanation
Required follow-up
```

Do not directly convert results into causal claims.

---

## 14. Reproducibility

A result is not considered reliable until it can be reproduced under the recorded configuration.
