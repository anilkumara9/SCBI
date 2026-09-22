# SCBI Evaluation, Metrics, Statistics & Ablation Protocol

## 1. Purpose

This document defines how SCBI performance must be evaluated.

---

## 2. Primary Metric

Every task must have a predefined primary metric.

Examples:

```text
accuracy
exact match
F1
BLEU/ROUGE where justified
task-specific score
loss
reward
```

Do not select the primary metric after seeing results.

---

## 3. Secondary Metrics

Possible secondary metrics:

* latency;
* memory;
* compute;
* robustness;
* calibration;
* consistency;
* representation complexity.

---

## 4. Performance Difference

$$
\Delta M
=
M_{SCBI}
-
M_{baseline}.
$$

Report both absolute and relative improvement where meaningful.

---

## 5. Statistical Reporting

For stochastic experiments report:

$$
\mu
$$

and:

$$
\sigma.
$$

Where appropriate report confidence intervals and effect sizes.

---

## 6. Per-Example Analysis

Where practical, analyze:

```text
examples improved
examples unchanged
examples degraded
```

This is often more informative than average performance alone.

---

## 7. Ablation Matrix

At minimum:

| Variant         | Purpose                               |
| --------------- | ------------------------------------- |
| Baseline        | Reference                             |
| SCBI            | Full method                           |
| No-B adaptation | Test representation mechanism         |
| Random B        | Test meaningfulness of representation |
| No selection    | Test selection                        |
| No consistency  | Test consistency contribution         |
| T=1             | Test iterative process                |
| T>1             | Test iterative process                |
| Compute-matched | Control compute                       |

---

## 8. Robustness

Evaluate:

* input perturbation;
* formatting changes;
* domain shift;
* difficult examples;
* alternative seeds.

---

## 9. Statistical Caution

Do not use statistical tests mechanically.

The chosen test must match:

* paired/unpaired data;
* distribution;
* number of samples;
* repeated measurements.

---

## 10. Multiple Comparisons

If many hypotheses are tested, consider the effect of multiple comparisons.

Do not report only the most favorable metric.

---

## 11. Causal Evidence

Strong evidence requires:

$$
\text{SCBI}
>
\text{appropriate controlled alternatives}.
$$

Ablations should isolate individual components.

---

## 12. Failure Analysis

For degraded examples determine:

```text
representation failure
candidate generation failure
evaluation failure
selection failure
state update failure
termination failure
model limitation
dataset issue
```

---

## 13. Final Evaluation Rule

A claim should be no stronger than the evidence supporting it.
