# SCBI Assumptions, Constraints & Boundary Conditions

## 1. Purpose

This document defines the assumptions under which SCBI is studied.

An assumption must never silently become a fact.

Every assumption has to be:

* explicit;
* testable where possible;
* justified;
* tracked;
* revisable.

---

## 2. Core Assumptions

### A1 — Frozen Backbone

Core SCBI assumes:

$$
\theta_t=\theta_0
$$

throughout inference.

---

### A2 — Temporary Adaptation

SCBI adaptation occurs through:

$$
B_t
$$

and/or:

$$
z_t.
$$

---

### A3 — Temporary State

Temporary state does not become persistent model parameters during a core inference episode.

---

### A4 — Defined Objective

Candidate representations must be evaluated using a predefined objective.

---

### A5 — Controlled Information

The information available to SCBI must be explicitly specified.

---

### A6 — Controlled Compute

Additional inference computation must be measured.

---

## 3. Default Information Boundary

Unless an experiment explicitly states otherwise:

SCBI may access:

* current input;
* frozen model outputs;
* frozen model internal representations;
* temporary state;
* temporary candidate representations.

SCBI may not access:

* test labels;
* future examples;
* hidden evaluation answers;
* privileged metadata;
* external information.

---

## 4. External Tools

Retrieval, browsing, external models, databases, and human evaluators are not automatically part of core SCBI.

If used, label them explicitly.

---

## 5. Parameter Assumption

The following are forbidden in core SCBI:

```text
θ update
LoRA update
adapter update
bias update
normalization parameter update
persistent embedding update
persistent optimizer state
```

---

## 6. Initialization

The experiment must define:

$$
B_0
$$

and:

$$
z_0.
$$

Possible initialization mechanisms must be documented.

Never allow initialization to depend on unavailable test information.

---

## 7. Objective Assumptions

The objective must be defined before final test evaluation.

Do not change the objective after seeing final results merely to improve performance.

---

## 8. Stochasticity

If randomness exists, record:

* random seed;
* number of trials;
* sampling mechanism;
* candidate count;
* stochastic hyperparameters.

---

## 9. Dataset Assumptions

Clearly define:

```text
training data
validation data
test data
```

Avoid test-set optimization.

---

## 10. Compute Assumption

Report:

```text
hardware
model size
inference time
candidate count
iterations
memory
FLOPs or proxy where available
```

---

## 11. Representation Assumption

Do not assume that every temporary representation is mathematically a basis.

Until proven otherwise:

$$
B_t
$$

means:

> temporary candidate representation / coordinate system.

---

## 12. Self-Consistency Assumption

Self-consistency remains:

```text
OPEN
```

until formally defined and empirically validated.

---

## 13. Generalization Assumptions

Do not assume improvement on one task implies:

* general reasoning improvement;
* general intelligence improvement;
* transfer;
* robustness;
* scaling.

Each requires separate evidence.

---

## 14. Failure Assumptions

Expect possible:

* no improvement;
* instability;
* representation collapse;
* excessive compute;
* search failure;
* evaluator failure;
* leakage;
* overfitting;
* baseline superiority.

The system must be designed to record these.

---

## 15. Assumption Change Protocol

When an assumption changes:

```text
Assumption ID:
Previous:
New:
Reason:
Evidence:
Affected theory:
Affected implementation:
Affected experiments:
Date:
```

Never silently change an assumption.

---

## 16. Final Rule

If an implementation requires an assumption that is not documented here, stop and document it before proceeding.
