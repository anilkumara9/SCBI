# SCBI Scientific Reporting Protocol

## 1. Purpose

This document defines how all SCBI research findings must be recorded.

---

## 2. Report Structure

Every major report should contain:

```text
Research question
Background
Hypothesis
Method
Implementation
Experimental setup
Baselines
Results
Statistical analysis
Ablations
Failure analysis
Alternative explanations
Limitations
Conclusion
Future work
```

---

## 3. Evidence Labels

Use:

```text
[FACT]
[DEFINITION]
[HYPOTHESIS]
[OBSERVATION]
[INTERPRETATION]
[OPEN]
```

---

## 4. Results Must Be Reproducible

Every reported result must map to:

```text
experiment ID
run ID
configuration
Git commit
dataset
model
seed
```

---

## 5. Failed Results

Failed results must be included when scientifically relevant.

---

## 6. Research Log

Maintain:

```text
date
decision
reason
evidence
affected hypothesis
affected code
affected experiments
```

---

## 7. Novelty Report

Novelty claims require:

```text
closest prior work
mechanism comparison
mathematical comparison
implementation comparison
remaining distinction
confidence level
```

---

## 8. Conclusion Discipline

Never write:

> SCBI works.

Prefer evidence-specific statements such as:

> Under the tested configuration, SCBI produced a measurable improvement over the specified baseline.

---

## 9. Final Research Report

The final report must clearly distinguish:

```text
What was hypothesized
What was implemented
What was observed
What was proven
What remains unknown
What failed
What overlaps with prior work
What contribution remains
```
