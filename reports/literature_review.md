# SCBI Comprehensive Literature Review

**Document Status:** Working Draft  
**Governing Protocol:** [`research/README_LITERATURE.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/research/README_LITERATURE.md)  
**Governing Rule:** [`.agents/rules/01-literature.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/rules/01-literature.md)  
**Lead Agent:** [`literature-agent.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/agents/literature-agent.md)

---

## 1. Executive Summary

This document consolidates prior-art investigations across 6 primary search domains (Test-Time Adaptation, Activation Engineering, Prompt Optimization, KV-Cache Editing, Dictionary Learning, and Self-Consistency Search) to determine the exact relationship between SCBI and existing literature.

---

## 2. Literature Search Log

| Date | Search Domain | Query String | Engine / Database | Papers Screened | Relevant Works | New Concepts / Keywords |
| :--- | :--- | :--- | :--- | :---: | :---: | :--- |
| 2026-09-11 | Baseline Architecture | Protocol definition | Workspace baseline | — | — | Cross-vocabulary mapping |
| 2026-09-11 | Rep Engineering & TTT | `("representation engineering" OR "test-time training" OR "activation addition") AND ("frozen")` | arXiv / PapersWithCode | 15 | RepE, ActAdd, TTT, Tent | Contrastive steering, inner-loop gradient |

---

## 3. Prior-Art Equivalence & Comparison Matrix

*(Source of Truth: [`research/literature/LIT001_subspace_projection_audit.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/research/literature/LIT001_subspace_projection_audit.md))*

| Method | Venue / Year | Frozen $\theta$ ($\Delta\theta=0$) | Dynamic Representation $B_t$ | Transient State $z_t$ | Objective Evaluator $\mathcal{E}$ | Equivalence Status | Key Structural Difference |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Tent** | ICLR 2021 | No (updates BN) | No | No (persistent) | Entropy | `[DISTINCT]` | Updates normalization weights |
| **TTT** | ICML 2024 | No (updates $W_K$) | No | Yes | Reconstruction loss | `[DISTINCT]` | Updates parameter weights |
| **RepE** | NeurIPS 2023 | Yes | No (static offline) | No | None | `[DISTINCT]` | Offline global vectors |
| **ActAdd** | arXiv 2023 | Yes | No (static offline) | No | None | `[DISTINCT]` | Offline global vectors |
| **SCBI (D+C)** | This Work | **Yes** | **Yes (instance-adaptive)** | **Yes (purged)** | **$\mathcal{L}_{\text{cycle}} + \lambda \mathcal{H}$** | `[TARGET]` | Instance-adaptive basis under $\Delta\theta=0$ |

---

## 4. In-Depth Mechanism Comparisons

*(Detailed analysis of candidate works against the SCBI computation pipeline: $\text{Input} \to \text{Representation} \to \text{Adaptation} \to \text{Selection} \to \text{Prediction}$)*

---

## 5. Formal Research Gap Statement

*(Un-hyped formulation of remaining scientific questions unaddressed by prior art)*
