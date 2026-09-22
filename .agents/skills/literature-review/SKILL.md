---
name: literature-review
description: Comprehensive workflow for conducting systematic prior-art audits, cross-vocabulary literature retrieval, mathematical equivalence analyses, and novelty classification grounded in SCBI protocols.
---

# Literature Review Skill

This skill provides an exhaustive, systematic playbook for conducting literature audits, evaluating prior art, identifying equivalent mathematical formulations, and formalizing research gaps for **Self-Consistent Basis Invention (SCBI)**.

**Foundational Protocol:** [`documentation/README_LITERATURE.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/documentation/README_LITERATURE.md)  
**Governing Rule:** [`.agents/rules/01-literature.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/.agents/rules/01-literature.md)

---

## When to Use This Skill

Activate this skill whenever:
- Surveying prior art for any new candidate mechanism, representation, or loss function.
- Evaluating whether a proposed SCBI concept already exists in machine learning literature under different terminology.
- Authoring the "Related Work" or "Background" section of a paper or research report.
- Performing an equivalence audit between SCBI and test-time adaptation / representation engineering methods.

---

## Step-by-Step Execution Protocol

### Step 1: Query Expansion Across 6 Literature Clusters

Never search solely for the phrase *"Self-Consistent Basis Invention"*. You must translate the conceptual mechanism into the vocabularies of disparate research fields:

1. **Test-Time Adaptation (TTA) / Test-Time Training (TTT):**
   - Queries: `("test-time adaptation" OR "test-time training" OR "fully test-time") AND ("frozen" OR "parameter-free" OR "representation")`
   - Key questions: Does the method update weights $\theta$, BN statistics, or purely temporary state $z_t$?
2. **Representation Engineering & Activation Steering:**
   - Queries: `("representation engineering" OR "activation addition" OR "steering vectors" OR "activation patching") AND ("inference-time" OR "dynamic")`
   - Key questions: Is the steering vector pre-computed or dynamically generated and self-evaluated per sample?
3. **Dynamic Prompt & Prefix Tuning:**
   - Queries: `("dynamic prompt" OR "instance-adaptive prefix" OR "test-time prompt generation") AND ("frozen model")`
   - Key questions: Are prompt tokens optimized via backprop or dynamically retrieved/constructed?
4. **Key-Value Cache Manipulation:**
   - Queries: `("KV cache editing" OR "dynamic key-value compression" OR "attention state steering")`
   - Key questions: Does attention cache modification act as an implicit coordinate basis change?
5. **Dictionary Learning & Subspace Methods:**
   - Queries: `("sparse autoencoders" OR "dictionary learning" OR "subspace projection" OR "basis decomposition") AND ("activation space" OR "hidden states")`
   - Key questions: Is the dictionary static or adapted per inference episode?
6. **Search & Self-Consistency Decoding:**
   - Queries: `("self-consistency" OR "tree-of-thought" OR "best-of-n" OR "inference-time search") AND ("internal state" OR "representation")`
   - Key questions: Does search operate over token outputs $y$ or latent representations $B_t$?

---

### Step 2: Mathematical Equivalence Extraction

For every retrieved paper that shares characteristics with SCBI:
1. Extract the **Update Operator**: Write down their update rule for parameters and representations.
2. Check the **Backbone Parameter Invariant**:
   $$\Delta\theta \stackrel{?}{=} 0$$
   If the method updates any parameter $\theta$, mark as `[DIFFERENT_INVARIANT: PARAMETER_UPDATE]`.
3. Check the **State Transience**:
   Does state $z_t$ persist across episodes or get discarded after sample inference?
4. Check the **Representation Object**:
   Is there an explicit basis, projection matrix, or coordinate frame $B_t$?

---

### Step 3: Equivalence & Taxonomy Classification

Classify the candidate work into one of the formal relationship categories:

| Relationship Category | Operational Definition | Scientific Action |
| :--- | :--- | :--- |
| `[IDENTICAL]` | Same mathematics and identical conceptual framing. | SCBI claim is completely non-novel; cite as prior art. |
| `[EQUIVALENT]` | Different terminology/application, but mathematically isomorphic. | Document the isomorphism; acknowledge equivalence. |
| `[SUBSUMES]` | The prior method is a broader generalization containing SCBI as a special case. | Frame SCBI as a specific instantiation/analysis of the broader class. |
| `[SUBSUMED_BY]` | The prior method is a narrower special case of SCBI. | Explicitly demonstrate how SCBI generalizes it. |
| `[ORTHOGONAL]` | Addresses a different problem with complementary mechanisms. | Discuss as combinable or complementary. |
| `[DISTINCT]` | Solves a similar problem with fundamentally different mathematical mechanics. | Contrast in detail across assumptions, complexity, and mechanics. |

---

### Step 4: Structured Prior-Art Comparison Matrix

Every literature audit must conclude with a markdown comparison matrix:

```markdown
| Paper / Method | Year | Backbone Frozen? | Dynamic per Instance? | Transient State? | Explicit Basis B_t? | Evaluation Objective E? | Equivalence Status | Key Distinction |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| Tent (Wang et al.) | 2021 | No (BN updated) | Yes | No (persists) | No | Entropy | DISTINCT | Updates BN params; no basis invention |
| RepE (Zou et al.) | 2023 | Yes | No (static probe) | No | Yes (vector) | None (pre-computed) | DISTINCT | Pre-computed static vectors |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |
```

---

### Step 5: Research Gap Formulation

State the research gap using neutral, precise language:
- If a genuine gap exists: *"While prior work [A, B] explores static steering and [C, D] explores parameter adaptation, the construction and self-consistent evaluation of temporary coordinate frames under a strict $\Delta\theta=0$ invariant remains unformalized."*
- If no gap exists: *"Prior work [X] has demonstrated an identical mechanism under the framework of [Y]. Therefore, SCBI constitutes an application of [Y] to the frozen foundation setting."*
