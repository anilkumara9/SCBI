# SCBI Algorithm Specification

## 1. Purpose

This document defines the algorithmic structure of SCBI.

The algorithm must implement the research specification rather than redefine it.

---

## 2. Inputs

The algorithm receives:

$$
x
$$

and a frozen model:

$$
f_{\theta_0}.
$$

Optional supervised experiments may additionally receive:

$$
y.
$$

---

## 3. Initialization

Initialize:

$$
z_0=I_z(x)
$$

and:

$$
B_0=I_B(x).
$$

Initialization must not violate the information boundary.

---

## 4. Core Algorithm

```text
SCBI(x, frozen_model):

    verify model parameters are frozen

    initialize z0
    initialize B0

    for t = 0 ... T_max:

        construct current representation

        generate candidate representations

        evaluate each candidate

        calculate consistency if enabled

        select candidate

        decide accept/reject

        update temporary representation

        update temporary state

        check termination

    construct final representation

    generate final prediction

    verify frozen parameters

    return prediction and research metadata
```

---

## 5. Candidate Generation

Define:

$$
\mathcal{C}_t=G_t(x,h_t,z_t,B_t).
$$

Every candidate must be represented explicitly.

Record:

```text
candidate ID
generation method
seed
representation metadata
generation cost
```

---

## 6. Candidate Evaluation

For each candidate:

$$
s_i=S(B_i,x,z_t).
$$

If consistency exists:

$$
c_i=C(B_i,x,z_t).
$$

The combined objective must be predefined.

---

## 7. Candidate Selection

Example:

$$
B_t^\star
=
\arg\min_i
J(B_t^{(i)},z_t;x).
$$

The direction of optimization must be explicit.

---

## 8. Acceptance Rule

Define:

$$
a_t=A(B_t^\star,B_t,z_t).
$$

Possible rule:

$$
a_t=
\mathbf{1}
[
J(B_t^\star)<J(B_t)-\epsilon
].
$$

This is an example only.

The actual rule must be selected experimentally and documented.

---

## 9. State Update

$$
z_{t+1}=U(z_t,B_t^\star,a_t).
$$

No persistent parameter update is allowed.

---

## 10. Termination

The algorithm must terminate when one of the predefined conditions is reached:

```text
maximum iterations
budget exhausted
convergence
no meaningful improvement
stable representation
```

---

## 11. Final Prediction

$$
\hat y
=
f_{\theta_0}^{(y)}
(T_{B_T}(h_T,z_T,x)).
$$

---

## 12. Required Metadata

Every run should record:

```text
model
model hash
dataset
sample ID
seed
B0
z0
candidate count
iterations
candidate scores
consistency scores
accepted candidates
rejected candidates
termination reason
runtime
memory
parameter hash before
parameter hash after
prediction
evaluation result
```

---

## 13. Frozen Model Verification

Before execution:

$$
H_{\text{before}}=H(\theta_0).
$$

After execution:

$$
H_{\text{after}}=H(\theta_T).
$$

Require:

$$
H_{\text{before}}=H_{\text{after}}.
$$

If not, mark the run invalid for core SCBI.

---

## 14. Algorithm Variants

Variants must have explicit names.

Examples:

```text
SCBI-Gradient
SCBI-RandomSearch
SCBI-Beam
SCBI-Evolutionary
SCBI-LearnedGenerator
```

Do not mix variants in a single result table without identifying them.

---

## 15. Algorithm Correctness

Before performance evaluation, test:

1. frozen parameters;
2. candidate generation;
3. candidate evaluation;
4. selection;
5. state update;
6. termination;
7. reproducibility.

Correctness comes before optimization.

---

## 16. Final Rule

No production-quality optimization should occur until the minimal algorithm has been validated against the mathematical specification.
