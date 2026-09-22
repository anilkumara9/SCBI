# SCBI Implementation Specification

## 1. Purpose

This document defines how the mathematical SCBI specification must be translated into software.

Implementation must follow:

```text
theory/README_DEFINITIONS.md
theory/README.md
theory/README_ASSUMPTIONS.md
theory/README_FORMULATION.md
theory/README_ALGORITHM.md
```

---

## 2. Implementation Principle

Code must not redefine the research.

If implementation requires a new assumption:

1. stop;
2. document it;
3. update the relevant research specification;
4. obtain explicit approval;
5. continue implementation.

---

## 3. Architecture

Recommended structure:

```text
scbi/
├── core/
│   ├── engine.py
│   ├── state.py
│   ├── representation.py
│   ├── candidate.py
│   ├── evaluator.py
│   ├── selector.py
│   └── termination.py
│
├── models/
│   ├── frozen_model.py
│   └── model_adapter.py
│
├── representations/
│   ├── base.py
│   ├── transforms.py
│   └── candidates.py
│
├── optimization/
│   ├── search.py
│   └── gradient.py
│
└── baselines/
```

---

## 4. Frozen Model Interface

The model wrapper must expose:

```text
load()
forward()
get_representation()
predict()
parameter_hash()
verify_frozen()
```

---

## 5. State Interface

Temporary state must be isolated from persistent model parameters.

Example conceptual interface:

```text
SCBIState:
    representation
    temporary_memory
    iteration
    candidate_history
    scores
```

---

## 6. Representation Interface

Representations must expose:

```text
create()
transform()
serialize()
distance()
complexity()
```

Only methods relevant to the chosen formulation should actually be implemented.

---

## 7. Candidate Interface

Each candidate should have:

```text
candidate_id
representation
generation_metadata
score
consistency_score
accepted
```

---

## 8. Evaluation Interface

The evaluator must be deterministic where possible.

It must clearly specify:

```text
input
candidate
state
objective
score
```

---

## 9. Selection Interface

Selection must implement the mathematical rule.

Do not add undocumented heuristics.

---

## 10. Experiment Isolation

Each experiment must specify:

```text
model
dataset
configuration
seed
variant
information boundary
compute budget
```

---

## 11. No Silent Fine-Tuning

Any code path that changes model parameters must be disabled for core SCBI.

Tests should detect accidental changes.

---

## 12. Reproducibility

Record:

* Git commit;
* dependency versions;
* model identifier;
* dataset version;
* seed;
* hardware;
* configuration.

---

## 13. Testing

Required tests:

```text
test_frozen_parameters
test_representation
test_candidate_generation
test_candidate_evaluation
test_selection
test_state_update
test_termination
test_reproducibility
```

---

## 14. Logging

Log every iteration:

```text
iteration
candidate IDs
scores
consistency
selected candidate
accept/reject
state summary
runtime
memory
```

---

## 15. Invalid Run Conditions

Mark a run invalid if:

* parameters changed;
* test labels leaked;
* configuration is unknown;
* results cannot be reproduced;
* implementation differs from recorded specification;
* experiment crashed before required metadata was recorded.

---

## 16. Implementation Status

Do not optimize prematurely.

First implement:

```text
minimal correct SCBI
```

Then:

```text
optimized SCBI
```

Performance optimizations must preserve algorithmic equivalence.
