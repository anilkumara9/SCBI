---
name: paper-writing
description: Scholarly drafting and manuscript preparation guide enforcing rigorous tone, anti-hype standards, epistemological status tagging, compute-matched reporting, and transparent failure documentation for SCBI.
---

# Paper Writing Skill

This skill governs the writing, structural composition, tone, and citation standards for scholarly papers, technical reports, and research preprints documenting **Self-Consistent Basis Invention (SCBI)**.

**Foundational Documents:**
- [`documentation/researchidea.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/documentation/researchidea.md) §1, §9 (Scientific scope and research claims)
- [`documentation/theory.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/documentation/theory.md) §2 (Scientific status labels)
- [`documentation/README_DEFINITIONS.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/documentation/README_DEFINITIONS.md) (Source of truth for vocabulary)
- [`documentation/README_LITERATURE.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/documentation/README_LITERATURE.md) (Related work standards)
- **Governing Rules:** [`.agents/rules/00-core-research.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/rules/00-core-research.md), [`.agents/rules/01-literature.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/rules/01-literature.md)

---

## When to Use This Skill

Activate this skill whenever:
- Drafting conference or journal submissions (NeurIPS, ICML, ICLR, ACL).
- Writing technical whitepapers, arXiv preprints, or project summaries.
- Composing executive summaries or milestone deliverables.
- Reviewing manuscript drafts for un-hedged claims or promotional language.

---

## Scholarly Tone & Anti-Hype Standards

### 1. Forbidden Marketing Terminology
Eliminate hyperbolic adjectives and replace them with factual statements:

| Prohibited Phrase | Reason for Rejection | Approved Scientific Alternative |
| :--- | :--- | :--- |
| *"Revolutionary paradigm"* | Empty marketing hype. | *"Inference-time representational mechanism"* |
| *"Vastly outperforms"* | Imprecise and sensational. | *"Improves Accuracy by 3.2% (p < 0.01, Wilcoxon)"* |
| *"Groundbreaking novelty"* | Disrespects prior literature. | *"Distinguishable from prior TTA via invariant Δθ=0"* |
| *"Unprecedented reasoning"* | Unsubstantiated hyperbole. | *"Outperforms compute-matched Best-of-N on 4/5 tasks"* |
| *"Flawless / Solves the problem"* | Empirically false. | *"Reduces error rate by 18% with identified failure modes"* |

### 2. Epistemological Status Tagging
In theoretical and methodological sections, label statements using the project taxonomy:
- *"Under the assumption that $\mathcal{H}$ is locally Euclidean `[ASSUMPTION]`, we state that the basis update converges `[PROPOSITION]`..."*

---

## Standard Manuscript Structure

### 1. Title & Abstract
- **Title:** Descriptive and precise (e.g., *"Self-Consistent Basis Invention: Evaluating Inference-Time Representation Adaptation under Frozen Backbone Constraints"*).
- **Abstract Structure:**
  - Problem context (limits of static inference).
  - Core hypothesis (dynamic representation selection without parameter updates).
  - Method summary (operators $\mathcal{G}, \mathcal{E}, \mathcal{S}, \mathcal{T}$).
  - Key empirical finding with compute-matched baseline comparison.
  - Transparent statement of limitations and failure regimes.

### 2. Introduction
- Present the central research question from [`researchidea.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/documentation/researchidea.md) §3 verbatim.
- Emphasize the strict frozen-backbone constraint ($\Delta\theta=0$).
- Explicitly state the contributions: theoretical, algorithmic, and empirical.

### 3. Related Work & Prior-Art Positioning
- Provide the structured comparison table required by [`01-literature.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/rules/01-literature.md).
- Discuss test-time adaptation, activation engineering, soft prompting, and dictionary learning.
- Acknowledge any mathematical equivalences openly and cite prior art generously.

### 4. Mathematical Formulation
- Define the mathematical universe ($\Theta, \mathcal{X}, \mathcal{Y}, \mathcal{H}, \mathcal{Z}, \mathcal{B}$) per [`theory.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/documentation/theory.md).
- Detail candidate generation, candidate evaluation objective, candidate selection, and state updates per [`math.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/documentation/math.md).
- Formalize the computational complexity and budget bounds.

### 5. Empirical Evaluation
- Detail benchmarks, pre-registered metrics, and random seeds ($S \ge 5$).
- Prominently feature the compute-matched baselines table.
- Detail the 5 mandatory ablations (Random, Static, Null Objective, Budget Curve, Zero-State).
- Include confidence intervals and Wilcoxon significance values.

### 6. Limitations, Failure Modes & Negative Results
- Dedicate a prominent section to failure analysis:
  - Where does SCBI fail?
  - What is the latency and memory overhead?
  - In what task regimes does compute-matched standard sampling outperform SCBI?

---

## Pre-Submission Manuscript Checklist

- [ ] Central research question stated explicitly.
- [ ] No prohibited marketing phrases present.
- [ ] Mathematical notation matches [`README_DEFINITIONS.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/documentation/README_DEFINITIONS.md).
- [ ] Prior-art table compares against all 6 literature clusters.
- [ ] Baselines are compute-matched (forward passes, FLOPs, latency).
- [ ] All 5 ablations reported with error bars.
- [ ] Dedicated failure modes section included in main body.
