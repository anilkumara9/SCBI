# SCBI Formal Formulation Candidates

## 0. Canonical Program Objective (adopted 2026-09-23, LOG-142)

The program's formal objective, superseding the narrower "can SCPM improve
accuracy" framing:

$$
\theta_{after}=\theta_{before}
$$

while temporary computational state evolves during inference:

$$
(B_t,z_t,C_t,M_t,\ldots)\;\to\;(B_{t+1},z_{t+1},C_{t+1},M_{t+1},\ldots).
$$

Organizing question: *what discovery would have to be true for a frozen model
to become far more cognitively capable through inference-time computation?*

This objective is mechanism-level (P1): the bar is qualitatively new
computation, not a better benchmark score. All candidate formulations below
are evaluated against it. Anchored definitions of B_t, z_t (and friends)
are UNCHANGED — see `README_DEFINITIONS.md`; this section states the
program objective, not new vocabulary, so Law #5's Definition Change
Protocol is not triggered.

## 1. Purpose

This document contains candidate mathematical formulations of SCBI.

It does not assume that the first formulation is correct.

The purpose is to compare formulations and determine which one most accurately represents the research hypothesis.

---

## 2. Core Constraint

All core formulations must satisfy:

$$
\theta_t=\theta_0.
$$

---

## 3. Formulation A — Direct Representation Optimization

$$
B^\star
=
\arg\min_{B\in\mathcal{B}}
J(B;x)
$$

subject to:

$$
\theta=\theta_0.
$$

This is the simplest formulation.

### Advantages

* mathematically simple;
* easy to prototype;
* clear optimization variable.

### Risks

* may collapse into ordinary latent optimization;
* may not justify the word "basis";
* may overlap heavily with prior work.

---

## 4. Formulation B — Iterative Candidate Search

$$
\mathcal{C}_t
=
G_t(B_t,z_t,x)
$$

then:

$$
B_t^\star
=
\arg\min_{B\in\mathcal{C}_t}
J(B,z_t;x)
$$

and:

$$
(B_{t+1},z_{t+1})
=
(R,U)(B_t^\star,z_t).
$$

This explicitly represents search.

---

## 5. Formulation C — Consistency-Regularized Optimization

$$
J(B,z;x)
=
L_{\text{task}}
+
\lambda_C L_{\text{consistency}}
+
\lambda_B L_{\text{representation}}.
$$

Then:

$$
(B^\star,z^\star)
=
\arg\min_{B,z}J(B,z;x).
$$

This formulation makes self-consistency part of the objective.

---

## 6. Formulation D — Multi-Candidate Selection

Generate:

$$
B^{(1)},\ldots,B^{(K)}.
$$

Evaluate:

$$
s_i=S(B^{(i)},x).
$$

Select:

$$
B^\star
=
\arg\max_i s_i.
$$

This is a candidate-selection interpretation.

---

## 7. Formulation E — Sequential State-Space Search

Define:

$$
s_t=(B_t,z_t).
$$

Then:

$$
s_{t+1}
=
F(s_t,x).
$$

The objective becomes:

$$
\max_{\tau}
J(\tau,x)
$$

where:

$$
\tau=(s_0,s_1,\ldots,s_T).
$$

This treats SCBI as trajectory optimization.

---

## 8. Formulation Comparison

Evaluate each candidate formulation against:

| Property                    |        A |        B |        C |        D |        E |
| --------------------------- | -------: | -------: | -------: | -------: | -------: |
| Frozen θ                    |        ✓ |        ✓ |        ✓ |        ✓ |        ✓ |
| Temporary representation    |        ✓ |        ✓ |        ✓ |        ✓ |        ✓ |
| Candidate search            | Optional |        ✓ | Optional |        ✓ |        ✓ |
| State adaptation            | Optional |        ✓ |        ✓ | Optional |        ✓ |
| Explicit consistency        |       No | Optional |        ✓ | Optional | Optional |
| Simple implementation       |        ✓ |        ✓ |   Medium |        ✓ |   Harder |
| Potential prior-art overlap |     High |      TBD |      TBD |     High |      TBD |

Do not select based on convenience alone.

---

## 9. Selection Criteria

The preferred formulation should maximize:

1. scientific clarity;
2. falsifiability;
3. reproducibility;
4. interpretability;
5. distinction from existing methods;
6. measurable mechanism;
7. reasonable computational cost.

---

## 10. Required Formulation Decision

Before implementation, record:

```text
Selected formulation:
Why selected:
Rejected formulations:
Reason for rejection:
Closest prior art:
Remaining open questions:
```

---

## 11. Important Rule

If literature demonstrates that a formulation already exists, do not rename it SCBI.

Instead:

* identify the overlap;
* determine whether another formulation remains meaningful;
* reformulate if justified;
* document the change.

---

## 12. Current Status

No formulation should be considered permanently final until:

1. literature analysis;
2. mathematical analysis;
3. implementation feasibility;
4. falsification experiment;

have been performed.
