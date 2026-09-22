# Rule 01: Literature Review & Prior-Art Protocol

**Applies to:** All literature searches, related-work sections, novelty claims, taxonomy formulations, and prior-art reviews.  
**Foundational Documents:**
- [`documentation/README_LITERATURE.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/documentation/README_LITERATURE.md) (Official literature-review, prior-art, and novelty-analysis protocol)
- [`documentation/README_DEFINITIONS.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/documentation/README_DEFINITIONS.md) (SCBI terminology and formal definitions)

---

## 1. Central Literature Mandate

The primary literature question defined in [`README_LITERATURE.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/documentation/README_LITERATURE.md) §2 is:

> **"Has prior work already demonstrated or formalized inference-time construction, adaptation, optimization, selection, or replacement of temporary representations or coordinate systems while keeping the underlying foundation-model parameters frozen?"**

Agents must not conduct superficial searches solely for the exact string *"Self-Consistent Basis Invention"*. Scientific ideas routinely emerge under divergent terminology across distinct research sub-fields.

---

## 2. Mandatory Search Domains & Cross-Vocabulary Matrix

Searches must cross-examine the following literature clusters:

| Domain | Representative Key Terms | Critical Relationship to SCBI |
| :--- | :--- | :--- |
| **Test-Time Adaptation (TTA) / TTT** | Test-Time Training, Test-Time Adaptation, Tent, MEMO, Dynamic TTA | Does the method update weights $\theta$, BN statistics, or purely temporary state $z_t$? |
| **Prompt Tuning / Soft Prompting** | Prefix-tuning, Prompt-Tuning, P-tuning, soft tokens | Are the vectors prepended at input or dynamically constructed per-instance without backprop? |
| **Activation Engineering & Steering** | Representation Engineering (RepE), Activation Addition, Steering Vectors, CAA | Is the representation vector static or dynamically synthesized and self-evaluated? |
| **Dynamic Key-Value Cache Editing** | KV cache manipulation, dynamic memory, token cache compression | Does KV cache adjustment constitute a coordinate basis change $B_t$? |
| **Representation Learning / Dictionaries** | Sparse Autoencoders (SAEs), Dictionary Learning, Probing, Subspace Alignment | Is the basis pre-trained offline or invented per inference instance? |
| **Self-Consistency & Search** | Self-Consistency (Wang et al.), Tree of Thoughts, MCTS, Re-ranking | Does the search operate over output tokens $y$ or internal representations $B_t$? |

---

## 3. The Equivalence Audit Requirement

Before any claim of "novelty" or "research gap" can be accepted, the agent must perform an **Equivalence Audit**:

1. **Mathematical Equivalence:** Can the proposed SCBI formulation be mapped bijectively to an existing method's loss function and update rule? If yes, it is mathematically equivalent (`[EQUIVALENT]`).
2. **Algorithmic Equivalence:** Does the computation graph duplicate an existing procedure despite different notation? If yes, it is algorithmically equivalent (`[EQUIVALENT]`).
3. **Subsumption:** Is SCBI a special case of a known broader framework, or does it generalize an existing technique? The exact subsumption relation must be stated.

---

## 4. Prior-Art Comparison Table Standard

Every literature audit must produce an explicit comparison table across standard dimensions:

| Candidate Prior Art | Backbone Frozen? ($\Delta\theta=0$) | Inference-Time Dynamic? | State Transience (Disposed post-inference?) | Basis/Representation Explicit? | Self-Consistency Objective Used? | Primary Distinction from SCBI |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| *Method Name* | Yes/No | Yes/No | Yes/No | Yes/No | Yes/No | *Specific structural difference* |

---

## 5. Non-Novelty Acceptance Protocol

As stipulated in [`README_LITERATURE.md`](file:///c:/Users/Anilkumar/OneDrive/Desktop/SCPM/documentation/README_LITERATURE.md) §1:
- A conclusion stating **"SCBI is an instance of [Existing Framework X] applied to [Domain Y]"** is an acceptable, rigorous scientific finding.
- Agents are strictly prohibited from redefining SCBI or inflating minor implementation quirks into "theoretical breakthroughs" when prior art is uncovered.
