# SCBI Literature Review & Prior-Art Protocol

## Self-Consistent Basis Invention (SCBI)

---

## 1. Purpose

This document defines the official literature-review, prior-art, novelty-analysis, and research-gap protocol for **Self-Consistent Basis Invention (SCBI)**.

The purpose of this document is not to prove that SCBI is novel.

The purpose is to determine, as rigorously as possible:

1. What has already been proposed.
2. What has already been implemented.
3. What terminology different research communities use for similar ideas.
4. Which existing methods are mathematically or algorithmically equivalent to SCBI.
5. Which methods are merely related but fundamentally different.
6. Whether SCBI contains a genuinely distinguishable contribution.
7. Whether the contribution is theoretical, algorithmic, empirical, architectural, or merely a recombination of existing ideas.
8. What research gap, if any, remains after the literature audit.

The literature process must be capable of producing a conclusion that says:

> **SCBI is not novel.**

This is a valid and scientifically valuable outcome.

---

# 2. Central Literature Question

The primary literature question is:

> **Has prior work already demonstrated or formalized inference-time construction, adaptation, optimization, selection, or replacement of temporary representations or coordinate systems while keeping the underlying foundation-model parameters frozen?**

This question must be investigated broadly.

Searching only for the exact phrase **"Self-Consistent Basis Invention"** is insufficient.

The concept may already exist under completely different terminology.

---

# 3. SCBI Working Definition for Literature Search

Until the theory is finalized, literature searches should use the following working abstraction.

Let:

* `θ` = parameters of a pretrained foundation model.
* `x` = input.
* `z_t` = temporary inference-time state.
* `B_t` = temporary candidate representation, basis, coordinate system, transformation, subspace, dictionary, or related representation object.
* `y_t` = model prediction.
* `L` = evaluation objective.

Core SCBI constraint:

```text
θ remains frozen during the core inference procedure.
```

The proposed inference process may construct, evaluate, modify, retain, or discard temporary state and/or representation objects.

Conceptually:

```text
Input x
   ↓
Frozen model θ
   ↓
Initial representation/state
   ↓
Temporary representation B₀
   ↓
Candidate generation
   ↓
Evaluation
   ↓
Consistency/objective test
   ↓
Accept / reject / modify
   ↓
B₁
   ↓
...
   ↓
Final temporary representation/state
   ↓
Prediction
```

This abstraction is intentionally broader than the eventual implementation.

---

# 4. Critical Warning: Terminology Is Not Evidence

The term **basis** must not be assumed to mean a mathematical linear basis.

Existing literature may use terms such as:

* latent representation
* latent space
* coordinate system
* feature space
* subspace
* dictionary
* prototype
* embedding
* transformation
* adapter
* context
* memory
* temporary parameters
* fast weights
* test-time parameters
* state
* activation state
* hidden state
* task representation
* task-specific representation
* learned representation
* dynamic representation
* inference-time representation
* adaptive representation

All potentially relevant terminology must be investigated.

Likewise, the phrase **self-consistent** must not be assumed to distinguish SCBI from prior work.

---

# 5. Literature Search Philosophy

The literature review must follow a **funnel strategy**.

Start broad.

Then progressively narrow.

```text
Broad conceptual search
        ↓
Inference-time adaptation
        ↓
Frozen-model adaptation
        ↓
Representation adaptation
        ↓
Temporary representation/state optimization
        ↓
Dynamic basis/subspace construction
        ↓
Self-consistency mechanisms
        ↓
Closest algorithmic matches
        ↓
Exact overlap analysis
```

Do not begin with searches designed to confirm SCBI.

---

# 6. Required Literature Categories

The literature audit must investigate at least the following categories.

## 6.1 Test-Time Adaptation

Search for methods that modify model behavior during inference/test time.

Examples of terminology:

* test-time adaptation
* test-time training
* test-time optimization
* test-time learning
* test-time inference adaptation
* source-free adaptation
* online adaptation
* continual test-time adaptation

Questions:

* Are parameters updated?
* Are only temporary states updated?
* Is the backbone frozen?
* Is adaptation persistent?
* Is adaptation per-example?
* Is adaptation per-batch?
* Is adaptation task-level?
* Is the adaptation representational?

---

# 7. Test-Time Training

Investigate methods where additional objectives are optimized during inference.

Determine:

* What is optimized?
* Parameters?
* Activations?
* Latent variables?
* Prompts?
* Adapters?
* Memory?
* Representations?
* Auxiliary modules?

Determine whether the optimization is temporary or persistent.

A method that updates `θ` is not automatically equivalent to core SCBI.

---

# 8. Frozen-Model Inference Adaptation

Search specifically for methods where:

```text
θ = constant
```

during inference.

Investigate whether prior work adapts:

* hidden states
* latent variables
* prompts
* context
* external memory
* feature transformations
* activation distributions
* representations
* intermediate layers
* attention patterns
* routing decisions
* temporary modules

This category is especially important.

---

# 9. Representation Adaptation

Search for inference-time methods that dynamically alter representations without modifying the underlying model weights.

Relevant concepts may include:

* representation adaptation
* latent adaptation
* feature adaptation
* activation adaptation
* representation alignment
* latent-space optimization
* feature-space optimization
* inference-time representation learning
* online representation learning

For each method, determine whether the representation is:

1. Fixed.
2. Learned during pretraining.
3. Learned during fine-tuning.
4. Learned during inference.
5. Generated per input.
6. Generated per task.
7. Persistent across examples.
8. Discarded after inference.

---

# 10. Latent Optimization

Investigate methods that optimize latent variables while keeping model parameters frozen.

Examples of possible concepts:

* latent optimization
* latent variable inference
* activation optimization
* hidden-state optimization
* feature-space search
* latent-space search
* energy-based inference
* iterative inference
* test-time latent optimization

Important question:

> Is SCBI simply latent optimization under a different name?

This question must be answered explicitly.

---

# 11. Dynamic Subspaces and Basis Construction

Search mathematical and machine-learning literature for methods involving:

* dynamic basis construction
* learned basis functions
* adaptive basis
* basis optimization
* basis selection
* dictionary learning
* adaptive subspaces
* task-specific subspaces
* low-dimensional subspaces
* learned coordinate systems
* dynamic coordinate transformations
* subspace optimization
* representation dictionaries
* feature dictionaries

Determine whether the basis is:

* global
* task-specific
* sample-specific
* learned offline
* learned online
* optimized at inference time
* temporary
* persistent

---

# 12. Self-Consistency Literature

Search for the exact concept of self-consistency independently from SCBI.

Investigate:

* self-consistency decoding
* consistency regularization
* consistency objectives
* prediction consistency
* representation consistency
* latent consistency
* cycle consistency
* internal consistency
* cross-view consistency
* iterative consistency
* agreement-based optimization

Critical question:

> Does existing "self-consistency" already provide the same accept/reject mechanism proposed by SCBI?

Do not assume the word itself represents novelty.

---

# 13. Prompt Optimization and Test-Time Prompting

Investigate:

* prompt optimization
* prompt tuning
* test-time prompting
* dynamic prompting
* automatic prompt search
* inference-time prompt optimization
* soft prompts
* continuous prompts
* prompt adaptation
* context optimization

Determine whether prompts function as a temporary coordinate system or representation.

If yes, determine whether SCBI is fundamentally different or merely a generalization.

---

# 14. Model Editing

Investigate:

* model editing
* local model editing
* transient model editing
* test-time model editing
* memory-based model editing
* activation editing
* representation editing

The distinction between:

```text
temporary representation modification
```

and

```text
model parameter modification
```

must be explicitly analyzed.

---

# 15. Fast Weights and Temporary Parameters

Investigate work involving:

* fast weights
* temporary weights
* ephemeral parameters
* dynamic parameters
* inner-loop learning
* meta-learning
* learned optimizers
* temporary adaptation
* rapid adaptation

Determine whether these methods already provide an equivalent mechanism to SCBI.

A temporary parameter mechanism may be mathematically equivalent even if it does not use the word "basis."

---

# 16. Meta-Learning

Investigate:

* MAML
* implicit meta-learning
* learned optimizers
* adaptation-based meta-learning
* in-context meta-learning
* fast adaptation
* task-conditioned adaptation

Determine:

```text
What changes?
When does it change?
Where does it change?
Does θ remain frozen?
Is the adapted state temporary?
```

Do not classify methods only by their names.

---

# 17. In-Context Learning

Investigate whether existing in-context learning can already be interpreted as temporary representation construction.

Search concepts including:

* in-context learning
* task inference
* implicit task representation
* context-dependent representations
* latent task representations
* in-context adaptation
* task vectors
* contextual representations

Critical question:

> If the model constructs a temporary task representation entirely from context, is SCBI merely an explicit implementation of a phenomenon already present in in-context learning?

This question must be addressed.

---

# 18. Agentic Search and Iterative Inference

Investigate methods that repeatedly:

```text
generate → evaluate → revise → retry
```

including:

* iterative inference
* self-refinement
* self-correction
* search-based reasoning
* inference-time search
* test-time compute scaling
* deliberation
* verifier-guided generation
* tree search
* beam search
* Monte Carlo search
* candidate selection
* rejection sampling

Determine whether SCBI's candidate-generation/evaluation loop is algorithmically distinct.

---

# 19. Retrieval and Memory

Investigate:

* retrieval-augmented generation
* external memory
* episodic memory
* working memory
* neural memory
* task memory
* key-value memory
* prototype memory
* retrieval-based adaptation

Ask:

> Is the proposed temporary basis actually an external memory mechanism?

If the answer is potentially yes, the distinction must be formally defined.

---

# 20. Activation Steering and Representation Engineering

Investigate:

* activation steering
* representation engineering
* activation addition
* steering vectors
* concept vectors
* latent directions
* feature interventions
* activation patching
* representation editing

This area is highly relevant because it may involve changing internal representations while leaving model weights frozen.

Determine whether SCBI:

1. Creates representations dynamically.
2. Searches over representations.
3. Evaluates candidate representations.
4. Selects representations based on an objective.
5. Discards them after inference.

---

# 21. Feature Learning and Dictionary Learning

Investigate:

* dictionary learning
* sparse coding
* sparse autoencoders
* feature discovery
* learned dictionaries
* basis decomposition
* independent components
* PCA-like adaptation
* online PCA
* adaptive feature bases

Determine whether a dynamically constructed basis already exists in classical machine learning.

SCBI must not claim novelty simply because the mechanism is applied to foundation models.

---

# 22. Classical Optimization and Numerical Methods

The literature review must not be limited to modern LLM papers.

Investigate relevant concepts from:

* optimization
* numerical linear algebra
* adaptive coordinate systems
* basis pursuit
* coordinate descent
* trust-region methods
* adaptive subspaces
* Krylov methods
* variable projection
* latent-variable optimization
* online optimization
* iterative refinement

The goal is to determine whether the mathematical mechanism itself is already known.

---

# 23. Neuroscience and Cognitive Modeling

Where relevant, investigate literature involving:

* dynamic representations
* context-dependent representations
* task representations
* neural population codes
* representational remapping
* adaptive coding
* predictive representations

These sources should inform conceptual interpretation but must not be treated as direct evidence for machine-learning novelty unless technically comparable.

---

# 24. Search Query Families

The literature agent must generate multiple query families rather than relying on one query.

Example family:

```text
"inference-time representation adaptation"
```

```text
"test-time representation learning frozen model"
```

```text
"frozen backbone latent optimization inference"
```

```text
"temporary representation inference neural network"
```

```text
"dynamic basis construction neural network inference"
```

```text
"adaptive subspace test-time learning"
```

```text
"online basis selection neural networks"
```

```text
"latent space optimization frozen model"
```

```text
"activation optimization inference frozen model"
```

```text
"self-consistency representation optimization"
```

```text
"temporary latent state optimization transformer"
```

```text
"inference-time adaptation without parameter updates"
```

The literature agent must expand these query families using terminology discovered during the search.

---

# 25. Search Sources

The literature review should prioritize primary sources.

Preferred sources:

1. Peer-reviewed papers.
2. Official conference proceedings.
3. arXiv papers when necessary.
4. Official project pages.
5. Author-maintained technical pages.
6. Theses/dissertations.
7. Patents when relevant.
8. Established textbooks for classical foundations.

Search engines and indexing services may be used for discovery, but the final evidence should preferably reference the original source.

---

# 26. Primary Source Rule

Whenever possible:

```text
Search result
    ↓
Original paper
    ↓
Paper abstract
    ↓
Method section
    ↓
Algorithm
    ↓
Experiments
    ↓
Exact comparison with SCBI
```

Do not treat a blog post summarizing a paper as sufficient evidence when the original paper is available.

---

# 27. No Fabricated Citations

The literature agent must NEVER:

* invent a paper title
* invent an author
* invent a DOI
* invent an arXiv identifier
* invent a publication year
* invent experimental results
* invent quotations
* fabricate mathematical claims
* attribute an idea to the wrong paper

If a source cannot be verified:

```text
UNVERIFIED
```

must be used.

Unverified sources must not be used as evidence for novelty conclusions.

---

# 28. Literature Evidence Levels

Every important literature claim must receive an evidence level.

## Level A — Direct Primary Evidence

The original paper explicitly describes the relevant mechanism.

Example:

```text
A paper explicitly optimizes latent representations at inference time while
keeping the backbone parameters frozen.
```

---

## Level B — Strong Technical Similarity

The paper does not use the same terminology but its mechanism is closely related.

---

## Level C — Conceptual Similarity

The paper addresses a similar research question but uses a substantially different mechanism.

---

## Level D — Peripheral Similarity

The paper is relevant background but does not threaten the core novelty.

---

## Level E — Speculative Similarity

The connection is only a hypothesis and requires further analysis.

---

# 29. Required Literature Record

Every serious candidate paper must be recorded using a structured format.

```yaml
paper_id:
title:
authors:
year:
venue:
url:
identifier:

research_area:

problem:
method:

model_type:

parameter_updates:
  backbone:
  temporary_parameters:
  activations:
  latent_state:
  external_memory:

inference_time_adaptation: true/false

representation_adaptation: true/false

basis_or_subspace:
  present: true/false
  description:

candidate_generation:
  present: true/false
  description:

candidate_evaluation:
  present: true/false
  description:

self_consistency:
  present: true/false
  definition:

temporary_state:
  present: true/false
  description:

persistence:
  per_token/per_example/per_task/persistent/unknown:

closest_SCBI_component:

similarity_level:
  direct/strong/conceptual/peripheral/speculative:

potential_overlap:

key_difference:

novelty_risk:
  high/medium/low:

evidence_notes:

verified_by:
date_reviewed:
```

---

# 30. Mandatory Comparison Dimensions

Every high-relevance paper must be compared against SCBI across the following dimensions.

| Dimension                          | Prior Work | SCBI                    |
| ---------------------------------- | ---------- | ----------------------- |
| Backbone frozen                    | ?          | Core requirement        |
| Inference-time adaptation          | ?          | Yes                     |
| Temporary state                    | ?          | Proposed                |
| Temporary representation           | ?          | Proposed                |
| Dynamic basis                      | ?          | Proposed                |
| Candidate generation               | ?          | Proposed                |
| Candidate evaluation               | ?          | Proposed                |
| Self-consistency criterion         | ?          | To be defined           |
| Per-input adaptation               | ?          | Possible                |
| Persistent parameter updates       | ?          | No in core SCBI         |
| External memory                    | ?          | Not required            |
| Prompt modification                | ?          | Not required            |
| Model editing                      | ?          | Not required            |
| Iterative search                   | ?          | Possible                |
| Representation discarded afterward | ?          | Expected in core design |

The table is not evidence of novelty.

It is a comparison framework.

---

# 31. Exact Algorithmic Overlap Test

For every potentially similar method, perform the following test.

Ask:

### Step 1

Does the method keep the underlying model parameters frozen?

If no:

```text
Not equivalent under the core SCBI constraint.
```

Continue investigating because a variant may still be relevant.

---

### Step 2

Does the method modify or construct an inference-time representation/state?

If no:

```text
Weak overlap.
```

If yes:

Continue.

---

### Step 3

Is the representation dynamically generated or selected?

If no:

```text
Potentially related but incomplete overlap.
```

---

### Step 4

Does the method evaluate candidate representations?

If yes:

Potentially strong overlap.

---

### Step 5

Does the evaluation use a consistency or task-performance objective?

If yes:

Potentially very strong overlap.

---

### Step 6

Does the resulting mechanism produce substantially the same computational process as SCBI?

If yes:

```text
HIGH PRIOR-ART OVERLAP
```

At this point, the research manager must investigate whether SCBI is merely a renaming or reformulation.

---

# 32. Mathematical Equivalence Test

Two methods do not need to use the same terminology to be equivalent.

The theory agent must attempt to determine whether:

```text
Method A
```

can be rewritten into:

```text
SCBI formulation
```

without changing its behavior.

For example, if a prior method performs:

```text
z' = argmin_z L(f_θ(x,z))
```

and SCBI performs:

```text
z* = argmin_z L(f_θ(x,z))
```

then changing the terminology does not establish novelty.

Likewise, if a prior method optimizes a transformation:

```text
B* = argmin_B L(f_θ(x;B))
```

and SCBI performs the same optimization, the distinction must come from an additional scientifically meaningful mechanism.

---

# 33. Novelty Must Be Multi-Dimensional

Novelty should not be represented by a single yes/no label.

Evaluate:

### Conceptual novelty

Is the research question itself new?

### Mathematical novelty

Is the formulation new?

### Algorithmic novelty

Is the optimization/search procedure new?

### Architectural novelty

Is the system structure new?

### Empirical novelty

Does the work demonstrate a previously unknown capability?

### Theoretical novelty

Does it establish a new theorem, bound, or explanation?

### Application novelty

Is an existing mechanism being applied to a new domain?

Application novelty alone must not be described as algorithmic novelty.

---

# 34. Novelty Risk Classification

Each research direction receives:

## LOW

Little directly overlapping prior work identified.

This does **not** mean proven novel.

---

## MEDIUM

Several related mechanisms exist, but a meaningful distinction may remain.

---

## HIGH

A highly similar mechanism exists.

---

## CRITICAL

Prior work appears to implement essentially the same mechanism.

When risk is critical, stop making novelty claims and investigate the overlap deeply.

---

# 35. The "Could This Already Exist?" Rule

Before proposing any new SCBI component, the literature agent must ask:

> **Could this mechanism already exist under another name?**

Examples:

```text
Temporary basis
→ latent adapter?
→ activation steering?
→ fast weight?
→ task representation?
→ prompt?
→ memory?
→ subspace?
```

```text
Self-consistency test
→ verifier?
→ consistency regularization?
→ rejection sampling?
→ candidate selection?
→ self-refinement?
```

```text
Candidate basis generation
→ search?
→ dictionary learning?
→ latent optimization?
→ prompt search?
→ evolutionary search?
```

This prevents terminology-based false novelty.

---

# 36. Negative Literature Findings

Negative findings must be documented.

Examples:

```text
No directly equivalent method was found after searching X databases
using Y query families.
```

This is acceptable.

However:

```text
No paper exists.
```

is generally too strong unless an exhaustive and defensible search can establish it.

Preferred wording:

> No directly equivalent work was identified within the reviewed literature.

---

# 37. Literature Saturation

The literature review should continue until additional searches produce diminishing returns.

A search round can be considered saturated only when:

1. Multiple terminology families have been searched.
2. Major adjacent research areas have been investigated.
3. Citation chains from the closest papers have been followed.
4. Important papers' references have been inspected.
5. Papers citing important prior work have been investigated.
6. Multiple databases/search engines have been used where appropriate.
7. Newly discovered terminology has been searched.
8. New searches mostly return already-known papers.

The literature agent must record the saturation rationale.

---

# 38. Citation Chaining

For every highly relevant paper:

```text
Paper
 ↓
References
 ↓
Earlier foundational methods
```

and:

```text
Paper
 ↓
Citations
 ↓
Later methods
```

must be investigated.

A single search result is never sufficient for a strong novelty conclusion.

---

# 39. Related-Work Graph

The literature agent should construct a conceptual graph.

Example:

```text
                    SCBI
                     │
       ┌─────────────┼─────────────┐
       │             │             │
 Test-Time       Representation   Iterative
 Adaptation      Adaptation       Search
       │             │             │
       │             │             │
   TTT/TTA       Activation      Self-Refinement
                    Steering
       │             │             │
       └─────────────┼─────────────┘
                     │
              Latent Optimization
                     │
               Dynamic Subspaces
```

The actual graph must be generated from verified literature rather than assumed categories.

---

# 40. Closest-Method Ranking

The literature agent must identify the **10 closest existing methods** to SCBI.

Rank them using:

1. Algorithmic similarity.
2. Mathematical similarity.
3. Frozen-backbone similarity.
4. Representation similarity.
5. Inference-time adaptation similarity.
6. Candidate-search similarity.
7. Evaluation/selection similarity.
8. Temporary-state similarity.

For each method, produce:

```text
Similarity score:
Why similar:
Why different:
Potential overlap:
What SCBI would need to demonstrate to remain distinct:
```

---

# 41. Literature Matrix

Maintain:

```text
research/literature/literature_matrix.csv
```

Suggested columns:

```text
paper_id
title
year
area
frozen_backbone
test_time
representation_adaptation
latent_optimization
temporary_state
basis_or_subspace
candidate_generation
candidate_evaluation
self_consistency
iterative_search
memory
prompt_adaptation
parameter_update
algorithm_similarity
mathematical_similarity
novelty_risk
notes
```

The matrix must be updated whenever an important paper is discovered.

---

# 42. Research Gap Definition

A research gap must not be written as:

> Nobody has done this.

Instead, use:

> Existing work addresses A, B, and C, but the reviewed literature does not appear to directly address D under constraints E and F.

A valid gap must contain:

```text
Existing literature
+
Precise missing capability
+
Precise constraint
+
Evidence
```

---

# 43. Example Gap Structure

Weak:

> There is no work on dynamic representations.

Strong:

> Existing inference-time adaptation methods reviewed in this study primarily modify model parameters, prompts, or latent states. A potentially less explored direction is dynamically constructing and evaluating an explicit temporary representation object while keeping the foundation-model parameters frozen throughout the inference procedure. This distinction requires further verification against the closest prior work.

The second statement is still provisional.

---

# 44. Novelty Claim Levels

The research team must use carefully calibrated language.

### Level 0

> Related work exists.

### Level 1

> The proposed formulation differs from the reviewed methods in X.

### Level 2

> The reviewed literature does not appear to contain the exact combination of X, Y, and Z.

### Level 3

> We identify a potentially novel algorithmic formulation.

### Level 4

> We establish a novel theoretical result.

Level 4 requires actual evidence.

Never jump from Level 0 to Level 4.

---

# 45. What Does NOT Establish Novelty

The following are insufficient:

* New name.
* New acronym.
* Different notation.
* New repository.
* New implementation.
* Applying an old method to an LLM.
* Combining known methods without a meaningful new mechanism.
* Better benchmark performance alone.
* Using a larger model.
* Using more inference compute.
* Describing an existing mechanism differently.
* Replacing "latent" with "basis."
* Replacing "adaptation" with "invention."

---

# 46. Benchmark Performance Is Not Novelty

Suppose SCBI achieves:

```text
Accuracy = 85%
```

while an existing method achieves:

```text
Accuracy = 80%
```

This does not automatically establish algorithmic novelty.

The improvement could result from:

* more compute
* better hyperparameters
* stronger model
* more iterations
* additional information
* leakage
* different preprocessing
* different evaluation
* unfair baseline
* implementation differences

Novelty and performance must be analyzed separately.

---

# 47. Fair Comparison Requirement

When comparing SCBI with prior methods, document:

```text
Model
Dataset
Training data
Inference budget
Number of forward passes
Number of optimization steps
Additional parameters
External information
Memory
Prompt length
Random seeds
Hardware
Evaluation metric
Stopping criteria
```

If these differ substantially, the comparison must be qualified.

---

# 48. Literature-to-Experiment Connection

Literature findings must directly influence experiments.

For example:

```text
Literature finding:
Existing method optimizes latent state.

Experiment:
Compare SCBI against latent-state optimization under equal compute.
```

Another example:

```text
Literature finding:
Activation steering provides fixed steering vectors.

Experiment:
Compare fixed steering vectors against dynamically constructed SCBI representations.
```

Another:

```text
Literature finding:
Test-time training updates model parameters.

Experiment:
Compare parameter adaptation against frozen-parameter SCBI.
```

The literature review is therefore not a separate activity from experimentation.

---

# 49. Required Ablation Against Closest Prior Work

SCBI must eventually be compared against the strongest relevant prior mechanisms.

At minimum, investigate whether experiments should include:

```text
Frozen model
vs.
SCBI
vs.
latent optimization
vs.
activation adaptation
vs.
prompt optimization
vs.
test-time training
vs.
relevant representation adaptation
```

The exact baseline list must be determined after literature review.

Do not choose baselines merely because they are easy to implement.

---

# 50. Literature Review Deliverables

The literature phase must produce:

```text
research/literature/
├── README.md
├── search_log.md
├── literature_matrix.csv
├── candidate_papers.md
├── closest_methods.md
├── citation_graph.md
├── terminology_map.md
├── novelty_risks.md
└── sources/
```

Additionally:

```text
research/related_work/
├── test_time_adaptation.md
├── representation_learning.md
├── latent_optimization.md
├── activation_steering.md
├── self_consistency.md
├── meta_learning.md
├── in_context_learning.md
├── iterative_inference.md
└── dynamic_subspaces.md
```

These files should be created only when evidence supports the category.

---

# 51. Search Log Requirements

Every major search session must record:

```text
Date:
Researcher/Agent:
Database/Search Engine:
Query:
Purpose:
Results:
Relevant Papers:
New Terminology:
Follow-up Searches:
Conclusion:
```

Example:

```text
Date: YYYY-MM-DD

Query:
"inference-time representation adaptation frozen model"

Purpose:
Identify prior work involving representation adaptation without
backbone parameter updates.

Results:
...

New terminology:
...

Follow-up:
...

Conclusion:
...
```

---

# 52. Literature Agent Responsibilities

The literature agent must:

1. Search broadly.
2. Search terminology variants.
3. Find primary sources.
4. Verify papers.
5. Follow citation chains.
6. Extract exact mechanisms.
7. Record evidence.
8. Identify overlap.
9. Identify contradictions.
10. Identify missing research.
11. Challenge novelty claims.
12. Maintain the literature matrix.
13. Maintain the terminology map.
14. Report uncertainty.

The literature agent must **not** decide that SCBI is novel merely because no exact phrase appears in search results.

---

# 53. Theory Agent Responsibilities

The theory agent must take the closest methods and ask:

```text
Can their algorithms be mathematically rewritten as SCBI?
```

If yes:

```text
Potential mathematical overlap.
```

If no:

```text
Document the exact mathematical distinction.
```

The theory agent must actively search for counterexamples to claimed distinctions.

---

# 54. Reviewer Responsibilities

The adversarial reviewer must ask:

> "Why isn't SCBI just an existing method with different terminology?"

It must attempt to reduce SCBI to known methods.

For example:

```text
SCBI = latent optimization?
SCBI = prompt optimization?
SCBI = activation steering?
SCBI = test-time training?
SCBI = meta-learning?
SCBI = search?
SCBI = self-refinement?
SCBI = memory?
SCBI = dynamic subspace optimization?
SCBI = combination of existing methods?
```

Every serious possibility must be investigated.

---

# 55. Research Manager Responsibilities

The research manager must not permit:

* premature novelty claims
* citation shortcuts
* selective literature
* ignored contradictory papers
* weak baseline selection
* terminology-based distinctions
* unsupported research-gap claims

The manager must maintain a decision log.

---

# 56. Literature Decision Log

Maintain:

```text
reports/novelty_report.md
```

with decisions such as:

```text
Decision:
SCBI mechanism overlaps strongly with method X.

Action:
Modify hypothesis H001.

Reason:
The prior method already performs temporary latent optimization.

Date:
...
```

This preserves scientific history.

---

# 57. Handling Contradictory Literature

If two papers make conflicting claims:

Do not choose the paper that supports SCBI.

Instead:

1. Record both.
2. Verify experimental conditions.
3. Inspect definitions.
4. Compare datasets.
5. Compare model architectures.
6. Compare evaluation metrics.
7. Determine whether the disagreement is genuine.
8. Record the uncertainty.

---

# 58. Literature Cutoff

Every literature report must state its search date.

Example:

```text
Literature reviewed through:
YYYY-MM-DD
```

Because new research can appear after the review.

For a final paper, perform a final literature refresh before submission.

---

# 59. Reproducibility of Literature Search

Where practical, preserve:

* exact queries
* dates
* databases
* search results
* paper identifiers
* URLs
* downloaded PDFs
* extracted notes
* inclusion/exclusion decisions

This allows another researcher to reproduce the literature audit.

---

# 60. Inclusion Criteria

A paper should receive detailed analysis when it contains at least one strong connection to:

* inference-time adaptation
* frozen-model adaptation
* temporary representations
* latent optimization
* dynamic subspaces
* basis construction
* activation optimization
* self-consistency
* iterative candidate evaluation
* test-time representation learning
* temporary model state
* fast adaptation

Peripheral papers may be recorded but do not require full analysis.

---

# 61. Exclusion Criteria

A paper may be excluded from the core comparison when it has no meaningful connection to the SCBI mechanism.

Examples:

* unrelated supervised learning
* ordinary pretraining
* generic classification
* unrelated optimization
* unrelated generative modeling

However, foundational mathematical work should still be retained when it informs SCBI theory.

---

# 62. Important Distinction: Similar vs Equivalent

The following hierarchy must always be respected:

```text
Related
   ≠
Similar
   ≠
Mechanistically overlapping
   ≠
Mathematically equivalent
   ≠
Identical
```

Literature conclusions must state which level applies.

---

# 63. Required Final Novelty Audit

Before claiming any form of novelty, the following questions must be answered:

### Q1

What are the five closest existing methods?

### Q2

What exactly does each method optimize?

### Q3

What exactly remains frozen?

### Q4

What temporary state exists?

### Q5

Does any prior work construct a temporary representation?

### Q6

Does any prior work evaluate candidate representations?

### Q7

Does any prior work use a consistency objective?

### Q8

Does any prior work perform the entire proposed loop?

### Q9

Can any existing algorithm be rewritten as SCBI?

### Q10

What exact property distinguishes SCBI?

### Q11

Is that distinction scientifically meaningful?

### Q12

Does an experiment isolate that distinction?

If Q10 or Q11 cannot be answered clearly, novelty remains unresolved.

---

# 64. Final Novelty Report Structure

The final report should use:

```markdown
# SCBI Novelty Assessment

## 1. Search Scope

## 2. Search Method

## 3. Terminology Investigated

## 4. Closest Existing Methods

## 5. Direct Overlap

## 6. Mathematical Overlap

## 7. Algorithmic Differences

## 8. Experimental Differences

## 9. Potential Research Gap

## 10. Counterarguments

## 11. Remaining Uncertainty

## 12. Novelty Assessment

## 13. Recommended Research Direction
```

The report must explicitly state confidence and uncertainty.

---

# 65. Allowed Conclusions

The literature review may conclude:

### Outcome A — Strong novelty potential

A meaningful gap appears to remain.

### Outcome B — Partial novelty

The mechanism overlaps existing work but contains a distinguishable component.

### Outcome C — Recombination

SCBI appears to combine known mechanisms in a new configuration.

This can still be scientifically valuable, but must be described honestly.

### Outcome D — Existing method

A prior method already implements substantially the same mechanism.

SCBI should then be reformulated.

### Outcome E — Unresolved

The available evidence is insufficient to determine novelty.

This is preferable to making an unsupported claim.

---

# 66. Research Reformulation Rule

If the literature reveals that SCBI's original formulation already exists, do not artificially defend the original formulation.

Instead:

```text
Original hypothesis
      ↓
Prior-art discovery
      ↓
Overlap analysis
      ↓
Identify missing limitation/capability
      ↓
Reformulate hypothesis
      ↓
New literature audit
```

The research may evolve.

That is not research failure.

---

# 67. No Goalpost Moving

The research team must not redefine SCBI after seeing favorable literature results solely to preserve a novelty claim.

Any major definition change must be recorded in:

```text
reports/research_log.md
```

with:

```text
Previous definition:
New definition:
Reason:
Literature evidence:
Expected scientific consequence:
Date:
```

---

# 68. Literature and Implementation Separation

The implementation must not determine the literature definition.

Incorrect:

> We implemented B as a matrix, therefore SCBI means matrix-based basis optimization.

Correct:

> The implementation currently represents B as a matrix because this is a testable instantiation of the broader hypothesis.

Implementation choices must remain subordinate to the scientific question.

---

# 69. Literature and Results Separation

Positive experimental results must never be used to reinterpret prior work selectively.

If a prior method performs similarly:

```text
Record it.
```

If a prior method outperforms SCBI:

```text
Record it.
```

If SCBI outperforms the prior method:

```text
Record it.
```

The literature review exists to establish the scientific landscape, not to support a desired conclusion.

---

# 70. Minimum Prior-Art Checklist

Before beginning major SCBI experiments, confirm:

```text
[ ] Test-time adaptation reviewed
[ ] Test-time training reviewed
[ ] Frozen-model adaptation reviewed
[ ] Representation adaptation reviewed
[ ] Latent optimization reviewed
[ ] Activation steering reviewed
[ ] Dynamic subspace methods reviewed
[ ] Basis/dictionary methods reviewed
[ ] Self-consistency methods reviewed
[ ] Prompt optimization reviewed
[ ] Model editing reviewed
[ ] Fast weights reviewed
[ ] Meta-learning reviewed
[ ] In-context learning reviewed
[ ] Iterative inference reviewed
[ ] Search-based inference reviewed
[ ] Memory/retrieval methods reviewed
[ ] Citation chains followed
[ ] Top 10 closest methods identified
[ ] Mathematical equivalence tested
[ ] Novelty risks documented
[ ] Research gap documented
```

---

# 71. Final Rule

The literature process must answer:

> **What has already been done that could make SCBI unnecessary, non-novel, or merely a reformulation?**

Only after answering that question should the research team ask:

> **What remains genuinely unexplored?**

And only after that should it ask:

> **What experiment can establish whether that unexplored mechanism actually matters?**

---

# 72. Scientific Principle

> **Do not search for evidence that SCBI is new. Search for evidence that SCBI has already been done.**

If the research survives that search, its novelty claim becomes substantially stronger.

If it does not survive, the research should change.

**The objective is not to protect the SCBI idea.
The objective is to discover the truth about it.**
