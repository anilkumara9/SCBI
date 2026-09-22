# SCBI Literature Review, Prior Art & Novelty Protocol

## 1. Purpose

This document defines how the SCBI project must investigate existing research before making claims about novelty, originality, contribution, or distinction.

The primary objective is not to prove that SCBI is novel.

The objective is to determine:

> **What already exists, what SCBI overlaps with, what is genuinely different, and whether the proposed research question remains scientifically meaningful.**

---

## 2. Core Rule

Never assume:

```text
new name = new method
```

Never assume:

```text
different implementation = novel algorithm
```

Never assume:

```text
not found in initial search = does not exist
```

Novelty must be established through systematic prior-art analysis.

---

## 3. Literature Search Categories

Antigravity must investigate at minimum:

### A. Test-Time Adaptation

Search for:

* test-time adaptation;
* test-time training;
* source-free adaptation;
* online adaptation;
* inference-time adaptation;
* transductive adaptation;
* test-time optimization.

### B. Inference-Time Optimization

Search for:

* inference-time optimization;
* test-time optimization;
* optimization during inference;
* latent optimization;
* hidden-state optimization;
* activation optimization;
* representation optimization.

### C. Representation Adaptation

Search for:

* dynamic representations;
* adaptive representations;
* temporary representations;
* latent-space adaptation;
* activation-space adaptation;
* coordinate transformations;
* learned bases;
* adaptive bases;
* subspace adaptation.

### D. Model Internal Modification

Search for:

* activation steering;
* activation editing;
* representation editing;
* hidden-state intervention;
* latent intervention;
* feature manipulation;
* internal state optimization.

### E. Search-Based Inference

Search for:

* iterative refinement;
* candidate generation and selection;
* inference-time search;
* adaptive computation;
* test-time search;
* tree search;
* beam search;
* evolutionary inference.

### F. Self-Consistency

Search for:

* self-consistency decoding;
* consistency-based inference;
* agreement-based inference;
* multi-sample consistency;
* verifier-based inference.

### G. Prompt / Context Optimization

Search for:

* prompt optimization;
* automatic prompt optimization;
* test-time prompt optimization;
* context optimization;
* soft prompt inference;
* prompt search.

### H. Meta-Learning

Search for:

* fast adaptation;
* inner-loop adaptation;
* meta-learning;
* task-conditioned representations;
* rapid adaptation.

---

## 4. Search Strategy

Search progressively.

### Level 1 — Broad

Search the general concept.

### Level 2 — Mechanism

Search each individual SCBI component.

### Level 3 — Mathematical

Search mathematical formulations similar to:

$$
\min_{B,z}J(B,z;x)
$$

subject to:

$$
\theta=\theta_0.
$$

### Level 4 — Architecture

Search for implementations where frozen models dynamically modify temporary internal representations.

### Level 5 — Terminology variants

Do not search only for the term "SCBI."

Search conceptually equivalent terminology.

---

## 5. Required Literature Record

Every important paper must be recorded using:

```text
Title:
Authors:
Year:
Venue:
URL:
DOI/arXiv:
Method:
Problem:
Backbone:
Does it update θ?
Does it modify hidden states?
Does it create temporary representations?
Does it search candidate representations?
Does it use an evaluator?
Does it use external information?
Does it use ground truth?
Inference-time computation:
Closest SCBI component:
Similarity:
Difference:
Potential overlap:
Potential distinction:
Confidence:
```

---

## 6. Evidence Hierarchy

Prefer:

1. original research papers;
2. official conference proceedings;
3. official repositories;
4. authors' papers;
5. reputable technical reports;
6. secondary surveys.

Do not treat random blogs as proof of novelty.

---

## 7. Closest-Method Matrix

Create a table:

| Method   | Frozen θ | Temporary State | Representation Adaptation | Candidate Search | Selection | External Info | Similarity |
| -------- | -------: | --------------: | ------------------------: | ---------------: | --------: | ------------: | ---------: |
| Method A |          |                 |                           |                  |           |               |            |
| Method B |          |                 |                           |                  |           |               |            |
| Method C |          |                 |                           |                  |           |               |            |
| SCBI     |      Yes |             Yes |                       Yes |              TBD |       TBD |           TBD |          — |

Do not fill unknown fields by guessing.

Use:

```text
Unknown
```

when evidence is insufficient.

---

## 8. Mechanism-Level Comparison

Do not compare only names.

Compare:

$$
\text{Input}
\rightarrow
\text{Representation}
\rightarrow
\text{Adaptation}
\rightarrow
\text{Selection}
\rightarrow
\text{Prediction}
$$

for each method.

Determine exactly where SCBI differs.

---

## 9. Novelty Levels

Use these categories:

### N0 — Clearly existing

The proposed mechanism already exists substantially unchanged.

### N1 — Known combination

Existing mechanisms are combined differently.

### N2 — Meaningful formulation difference

The formulation differs in a technically meaningful way.

### N3 — Strong methodological distinction

The mechanism appears substantially different from prior work.

### N4 — Potentially novel

There is evidence of a new mechanism, but extensive verification is still required.

Never call something "novel" merely because it received N4 internally.

---

## 10. Negative Novelty Result

If literature shows SCBI overlaps heavily with existing work, report:

```text
SCBI overlap discovered.
Original hypothesis requires reformulation.
Existing method:
Overlap:
Difference:
Remaining research gap:
Recommended reformulation:
```

This is a successful research outcome.

---

## 11. Literature Search Log

Maintain:

```text
Date:
Search query:
Database/search engine:
Results reviewed:
Relevant papers:
New terminology discovered:
New competing methods:
Implication for SCBI:
```

This prevents repeatedly searching the same concepts without learning.

---

## 12. No Citation Fabrication

Never invent:

* papers;
* authors;
* dates;
* conferences;
* DOIs;
* URLs;
* results;
* quotations.

If a source cannot be verified, mark it:

```text
UNVERIFIED
```

---

## 13. No Premature Novelty Claim

Before any publication, resume, grant, investor, or public claim states that SCBI is novel:

1. complete the literature search;
2. identify closest methods;
3. perform mechanism-level comparison;
4. perform mathematical comparison;
5. identify overlaps;
6. obtain adversarial review;
7. document remaining distinction.

---

## 14. Required Literature Deliverables

Antigravity must eventually produce:

```text
research/literature/
research/related_work/
research/research_gaps/
research/bibliography/
reports/literature_review.md
reports/novelty_report.md
```

---

## 15. Final Principle

The literature process exists to answer:

> **Is SCBI actually a new scientific mechanism, a new formulation of an existing mechanism, a combination of existing mechanisms, or a reformulation of an existing idea?**

The answer must come from evidence rather than preference.
