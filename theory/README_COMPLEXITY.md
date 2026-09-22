# SCBI Computational Complexity Specification

## 1. Purpose

This document defines how SCBI computational cost must be measured.

SCBI must not claim an improvement without reporting the computational cost required to obtain it.

---

## 2. Variables

Let:

$$
T
$$

= number of inference iterations.

$$
K_t
$$

= candidates evaluated at iteration \(t\).

$$
K=\sum_tK_t
$$

= total candidate evaluations.

$$
C_f
$$

= cost of one frozen-model evaluation.

$$
C_G
$$

= candidate-generation cost.

$$
C_S
$$

= candidate-evaluation cost.

---

## 3. Approximate Cost

A generalized SCBI cost is:

$$
C_{\text{SCBI}}
\approx
\sum_{t=0}^{T-1}
[
C_G(t)
+
K_tC_S(t)
+
C_U(t)
].
$$

If every candidate requires a complete model forward pass:

$$
C_{\text{SCBI}}
\approx
\sum_t K_t C_f.
$$

---

## 4. Baseline Cost

Define:

$$
C_{\text{base}}.
$$

Report:

$$
R_C
=
\frac{C_{\text{SCBI}}}{C_{\text{base}}}.
$$

---

## 5. Time Complexity

Report:

```text
average latency
median latency
p95 latency where useful
total inference time
candidate-generation time
evaluation time
update time
```

---

## 6. Memory Complexity

Report:

* model memory;
* temporary state memory;
* candidate memory;
* activation memory;
* peak memory.

---

## 7. Search Complexity

Report:

$$
K
$$

and:

$$
T.
$$

A method that evaluates more candidates must be compared fairly.

---

## 8. Compute-Matched Baseline

Create a baseline with approximately equivalent inference computation.

For example:

```text
Baseline + equivalent extra forward passes
```

This determines whether SCBI provides benefit beyond simply spending more compute.

---

## 9. Scaling Analysis

Where practical, evaluate:

$$
K\rightarrow2K\rightarrow4K
$$

and:

$$
T\rightarrow2T\rightarrow4T.
$$

Measure performance versus cost.

---

## 10. Efficiency Curve

Produce:

$$
\text{performance}
\quad\text{vs}\quad
\text{compute}.
$$

This is more informative than reporting only a single accuracy number.

---

## 11. Complexity Claims

Never claim:

```text
efficient
scalable
cheap
fast
```

without measurements.

---

## 12. Final Principle

SCBI must justify its additional inference computation through measurable capability gains.
