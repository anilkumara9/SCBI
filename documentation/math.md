# SCBI Theory Specification

## Self-Consistent Basis Invention

---

## 1. Purpose

This document defines the theoretical research framework for **Self-Consistent Basis Invention (SCBI)**.

Its purpose is to convert the high-level research hypothesis into a mathematically precise, testable framework while preserving enough generality to investigate multiple possible implementations.

This document is a **research specification**, not a claim that the proposed formulation is correct.

Every definition, assumption, objective, and algorithm described here must remain open to revision if:

* literature reveals prior equivalent formulations,
* mathematical analysis exposes inconsistencies,
* experiments falsify an assumption,
* computational constraints make an assumption unrealistic,
* or a simpler formulation explains the same phenomenon.

---

# 2. Central Research Question

SCBI investigates the following question:

> **Can a frozen foundation model improve its inference behavior by dynamically constructing, evaluating, and selecting temporary representations during inference without changing its underlying parameters?**

The theoretical framework must determine whether this question can be formulated rigorously.

---

# 3. Core Objects

The initial theoretical system contains the following objects.

Let:

$$
\theta
$$

denote the parameters of a pretrained foundation model.

Let:

$$
x
$$

denote an input instance.

Let:

$$
y
$$

denote the desired target or ground-truth output when available.

Let:

$$
z_t
$$

denote temporary inference-time state at step \(t\).

Let:

$$
B_t
$$

denote a temporary candidate representation, basis, coordinate system, transformation, subspace, dictionary, or related representational object.

Let:

$$
\hat{y}_t
$$

denote the prediction produced at inference step \(t\).

Let:

$$
\mathcal{L}
$$

denote an evaluation objective.

The basic system is therefore:

$$
(\theta,x,z_t,B_t)
\rightarrow
\hat{y}_t
$$

with:

$$
\theta=\text{constant}
$$

throughout core SCBI inference.

---

# 4. Frozen Backbone Constraint

The central constraint is:

$$
\theta_{t+1}=\theta_t=\theta
$$

for every inference step \(t\).

Therefore:

$$
\Delta\theta=0
$$

during the core SCBI procedure.

This distinction is fundamental.

If an experiment updates \(\theta\), it must not be described as a core SCBI experiment.

It must instead be labeled as a variant such as:

```text
SCBI + parameter adaptation
```

or:

```text
SCBI-PT
```

with the exact modification documented.

---

# 5. Temporary State

The temporary state is represented as:

$$
z_t.
$$

The state may contain one or more of:

* latent variables
* intermediate representations
* activation modifications
* candidate structures
* task-specific information
* temporary memory
* optimization state
* representation-selection state

The exact contents of \(z_t\) must be determined experimentally and theoretically.

Do not assume that \(z_t\) must be a vector.

A general formulation is:

$$
z_t\in\mathcal{Z}
$$

where:

$$
\mathcal{Z}
$$

is the temporary inference-state space.

---

# 6. Temporary Representation

The central representational object is:

$$
B_t\in\mathcal{B}.
$$

At this stage, **basis** is a provisional term.

Possible interpretations include:

### Linear basis

$$
B_t=[b_1,b_2,\ldots,b_k]
$$

where the vectors span a subspace.

### Coordinate transformation

$$
B_t:\mathcal{H}\rightarrow\mathcal{H}'
$$

### Projection

$$
B_t=P_t
$$

where:

$$
P_t^2=P_t
$$

### Learned feature dictionary

$$
B_t=\{b_1,\ldots,b_k\}
$$

### Representation transformation

$$
h'_t=T_{B_t}(h_t)
$$

### Subspace

$$
\mathcal{S}_t\subseteq\mathcal{H}
$$

### General temporary representation object

$$
B_t\in\mathcal{B}
$$

where \(\mathcal{B}\) is an appropriately defined representation space.

The research must determine which interpretation provides the strongest scientifically justified formulation.

---

# 7. Why "Basis" Must Remain Provisional

The word basis may imply mathematical properties such as:

* linear independence
* spanning
* dimensionality
* coordinate representation

The eventual SCBI mechanism may or may not satisfy these properties.

Therefore the research must not assume:

$$
B_t
$$

is a formal linear basis until mathematically justified.

The initial abstraction is:

> **A temporary representational object that can alter the model's inference computation without modifying the backbone parameters.**

The theory agent must determine whether a stricter definition is possible.

---

# 8. Foundation Model

Define the frozen foundation model as:

$$
f_\theta.
$$

Given input \(x\):

$$
h_0=f_\theta(x).
$$

The model may contain multiple computational layers:

$$
h_{l+1}=F_l(h_l;\theta_l).
$$

The complete parameter set is:

$$
\theta=\{\theta_1,\theta_2,\ldots,\theta_L\}.
$$

For core SCBI:

$$
\theta_l'=\theta_l
$$

for every layer \(l\).

---

# 9. SCBI Intervention

SCBI introduces a temporary intervention into inference.

A generalized formulation is:

$$
h'_t=T(B_t,h_t,z_t)
$$

where:

* \(h_t\) = model representation
* \(B_t\) = temporary representation object
* \(z_t\) = temporary state
* \(T\) = representation transformation/intervention

The frozen model then processes:

$$
h'_t
$$

without changing \(\theta\).

Thus:

$$
\hat{y}_t=f_\theta(x;B_t,z_t)
$$

is used as a shorthand for inference under the temporary state.

---

# 10. Candidate Generation

At each iteration, SCBI may generate a candidate:

$$
B_t^{(c)}
$$

where \(c\) indexes candidate representations.

Candidate generation can be expressed as:

$$
B_t^{(c)}
\sim
G_\phi(x,z_t,B_t)
$$

where \(G_\phi\) is a candidate-generation mechanism.

Important:

$$
\phi
$$

does not necessarily represent trainable model parameters.

It may represent:

* a deterministic algorithm
* a search procedure
* a heuristic
* an external proposal model
* a learned generator
* random perturbation
* gradient-based optimization
* evolutionary search
* sampling

The specific mechanism must be experimentally justified.

---

# 11. Candidate Evaluation

Each candidate must be evaluated.

Define:

$$
S(B_t^{(c)};x,z_t)
$$

as a candidate score.

For supervised evaluation:

$$
S=-\mathcal{L}(\hat{y},y).
$$

For unsupervised or self-supervised evaluation:

$$
S=-\mathcal{L}_{self}(\hat{y},x,z_t,B_t).
$$

For consistency-based evaluation:

$$
S=C(B_t^{(c)};x,z_t).
$$

The exact objective must be explicitly defined.

---

# 12. Self-Consistency

The term **self-consistency** is currently provisional.

It must eventually be defined mathematically.

One possible formulation is:

$$
C(B;x,z)
=
\operatorname{Agreement}
\left(
f_\theta(x;B,z),
f_\theta(x;\tilde{B},\tilde{z})
\right).
$$

However, this is only one possibility.

Other definitions may involve:

* agreement across transformations
* stability under perturbations
* prediction agreement
* internal representation agreement
* temporal consistency
* objective consistency
* multi-view consistency
* cross-candidate agreement

The research must determine which definition is scientifically meaningful.

---

# 13. Candidate Selection

Given candidates:

$$
\{B_t^{(1)},B_t^{(2)},\ldots,B_t^{(K)}\}
$$

select:

$$
B_t^*
=
\arg\max_{B\in\mathcal{C}_t}
S(B;x,z_t)
$$

or equivalently:

$$
B_t^*
=
\arg\min_{B\in\mathcal{C}_t}
\mathcal{L}(B;x,z_t).
$$

This creates the fundamental selection mechanism.

However, candidate selection alone is not sufficient to establish SCBI as a new algorithm.

Prior literature must be checked for equivalent procedures.

---

# 14. State Update

The temporary state may then be updated:

$$
z_{t+1}
=
U(z_t,B_t^*,x).
$$

Possible forms include:

$$
z_{t+1}=z_t
$$

(no state update),

or:

$$
z_{t+1}=U_\psi(z_t,B_t^*,x).
$$

The update mechanism must be explicitly specified for every implementation.

---

# 15. Representation Update

A candidate may also produce a new representation:

$$
B_{t+1}
=
R(B_t,B_t^*,z_t,x).
$$

Examples include:

### Replacement

$$
B_{t+1}=B_t^*
$$

### Incremental update

$$
B_{t+1}=B_t+\Delta B_t
$$

### Weighted update

$$
B_{t+1}
=
(1-\alpha)B_t+\alpha B_t^*
$$

### Search-tree expansion

$$
B_{t+1}\in\operatorname{Children}(B_t)
$$

These are candidate mechanisms, not fixed requirements.

---

# 16. Accept / Reject Mechanism

SCBI may contain an explicit acceptance criterion.

For example:

$$
\text{Accept}(B_t^{(c)})
\iff
S(B_t^{(c)})>S(B_t).
$$

Or:

$$
\text{Accept}(B_t^{(c)})
\iff
\Delta S_t>\epsilon.
$$

where:

$$
\Delta S_t
=
S(B_t^{(c)})-S(B_t).
$$

If the candidate fails:

$$
B_{t+1}=B_t.
$$

If accepted:

$$
B_{t+1}=B_t^{(c)}.
$$

The exact rule must be experimentally tested.

---

# 17. General SCBI Iteration

A generalized iteration is:

$$
B_t
\rightarrow
\mathcal{C}_t
\rightarrow
\text{Evaluate}
\rightarrow
B_t^*
\rightarrow
\text{Consistency Test}
\rightarrow
(B_{t+1},z_{t+1}).
$$

More explicitly:

$$
\mathcal{C}_t
=
G(x,z_t,B_t)
$$

$$
B_t^*
=
\arg\max_{B\in\mathcal{C}_t}
S(B;x,z_t)
$$

$$
z_{t+1}
=
U(z_t,B_t^*,x)
$$

$$
B_{t+1}
=
R(B_t,B_t^*,z_t,x).
$$

After \(T\) iterations:

$$
(B_T,z_T)
$$

are used to produce the final prediction:

$$
\hat{y}
=
f_\theta(x;B_T,z_T).
$$

---

# 18. Core SCBI Computational Graph

Conceptually:

```text
                    θ
                    │
                    │ frozen
                    ▼
x ───────────────► fθ
                    │
                    ▼
                   h₀
                    │
                    ▼
              temporary state z₀
                    │
                    ▼
             candidate generator
                    │
          ┌─────────┼─────────┐
          ▼         ▼         ▼
         B₁        B₂        B₃
          │         │         │
          └─────────┼─────────┘
                    ▼
               evaluation
                    │
                    ▼
             consistency test
                    │
             ┌──────┴──────┐
             ▼             ▼
           reject         accept
             │             │
             └──────┬──────┘
                    ▼
              state update
                    │
                    ▼
                 next step
                    │
                   ...
                    │
                    ▼
              final B*, z*
                    │
                    ▼
                prediction
```

---

# 19. Core Constraint Set

Core SCBI should satisfy:

$$
\boxed{\Delta\theta=0}
$$

and:

$$
\boxed{B_t,z_t\text{ may change during inference}}
$$

and:

$$
\boxed{\text{candidate representations may be evaluated}}
$$

and potentially:

$$
\boxed{\text{candidate representations may be accepted or rejected}}
$$

The final implementation must determine which of these are essential versus optional.

---

# 20. Research Hypothesis

The initial hypothesis is:

> **A frozen foundation model may improve inference behavior when it can construct and evaluate temporary representations or coordinate systems adapted to the current inference problem.**

This is a hypothesis.

It is not an established result.

---

# 21. Null Hypothesis

The primary null hypothesis should be:

$$
H_0:
$$

> Dynamic temporary representation construction provides no meaningful improvement over an appropriately controlled frozen-model inference baseline under equal information and compute conditions.

The alternative hypothesis:

$$
H_1:
$$

> Dynamic temporary representation construction provides a statistically and practically meaningful improvement over the controlled baseline.

---

# 22. Stronger Null Hypothesis

A stronger falsification criterion is:

> Any observed improvement from SCBI can be fully explained by additional inference compute, additional model calls, additional information, prompt changes, or other non-representational effects.

Therefore, SCBI must eventually be compared against compute-matched controls.

---

# 23. Causal Question

The key causal question is:

> **Does dynamically constructing the temporary representation cause the improvement?**

Observed correlation is insufficient.

For example:

$$
\text{SCBI accuracy}>\text{baseline accuracy}
$$

does not establish that:

$$
\text{dynamic basis construction}
\rightarrow
\text{improvement}.
$$

The improvement could arise from another factor.

---

# 24. Compute-Matched Formulation

Let:

$$
C(M)
$$

denote inference computational cost.

A fair comparison should attempt to satisfy:

$$
C(SCBI)\approx C(Baseline).
$$

If equal compute is impossible, the difference must be reported.

Performance should therefore be studied as a function of compute:

$$
P(C).
$$

This allows comparison between:

* performance
* inference cost
* number of model calls
* latency
* memory
* candidate count
* optimization steps

---

# 25. Information-Matched Formulation

Let:

$$
I(M)
$$

denote information available to method \(M\).

A fair comparison should attempt to maintain:

$$
I(SCBI)\approx I(Baseline).
$$

If SCBI receives additional information, that information must be explicitly documented.

---

# 26. Adaptation Budget

Define:

$$
K
$$

as the number of candidate representations considered.

Define:

$$
T
$$

as the number of inference iterations.

Define:

$$
F
$$

as the number of additional foundation-model forward passes.

Define:

$$
M
$$

as temporary memory usage.

The performance should therefore be considered as:

$$
P=P(K,T,F,M).
$$

This prevents a system from being described as more capable simply because it uses unlimited inference computation.

---

# 27. Representation Complexity

A candidate representation should have measurable complexity.

Possible measures include:

$$
d(B)
$$

for dimensionality,

$$
\|B\|
$$

for magnitude,

$$
\operatorname{rank}(B)
$$

for rank,

or:

$$
C_B
$$

for computational complexity.

The exact measure depends on the final representation.

---

# 28. Stability

A scientifically useful SCBI system should ideally be stable.

For perturbations:

$$
x'=x+\delta
$$

we can study:

$$
D(B^*(x),B^*(x')).
$$

If small perturbations produce arbitrarily large representation changes:

$$
D(B^*(x),B^*(x'))\gg D(x,x'),
$$

the mechanism may be unstable.

This must be measured rather than assumed.

---

# 29. Representation Quality

If SCBI constructs a representation:

$$
B^*
$$

its usefulness should be measurable.

Potential criteria:

* downstream performance
* prediction confidence
* robustness
* consistency
* compression
* sample efficiency
* transfer
* calibration
* stability
* computational efficiency

No metric should be selected solely because it produces favorable results.

---

# 30. Objective Function

The general SCBI objective can be expressed as:

$$
J(B,z;x)
=
-\mathcal{L}(f_\theta(x;B,z))
+
\lambda C(B,z)
$$

where:

* \(\mathcal{L}\) measures task loss
* \(C(B,z)\) measures complexity/cost
* \(\lambda\) controls the complexity penalty

This is only a candidate formulation.

The research must determine whether:

1. a supervised objective is possible,
2. a self-supervised objective is required,
3. a consistency objective is sufficient,
4. an external evaluator is required,
5. or another objective is more appropriate.

---

# 31. General Optimization Form

The theoretical problem can be written as:

$$
(B^*,z^*)
=
\arg\min_{B,z}
\mathcal{L}
\left(
f_\theta(x;B,z)
\right)
+
\lambda C(B,z)
$$

subject to:

$$
\theta=\text{constant}.
$$

This expresses the broad problem but does not yet define the SCBI algorithm.

The algorithmic contribution, if any, must come from how the optimization is performed.

---

# 32. Discrete Candidate Search

SCBI may alternatively operate over a candidate set:

$$
\mathcal{C}(x,z_t)
=
\{B_1,\ldots,B_K\}.
$$

Then:

$$
B_t^*
=
\arg\min_{B_i\in\mathcal{C}}
\mathcal{L}(B_i).
$$

This makes SCBI a search-and-selection procedure.

The literature audit must determine whether this is already equivalent to known inference-time search methods.

---

# 33. Continuous Optimization

If \(B\) is differentiable, the system may optimize:

$$
B_{t+1}
=
B_t
-
\eta
\nabla_B
\mathcal{L}
\left(
f_\theta(x;B_t,z_t)
\right).
$$

Here:

$$
\theta
$$

remains frozen while:

$$
B_t
$$

changes.

This is an important baseline formulation.

The research must determine whether this reduces to existing latent optimization or test-time optimization methods.

---

# 34. Gradient-Free Optimization

If gradients through \(B\) are unavailable or undesirable:

$$
B_{t+1}
=
\operatorname{Search}
\left(
B_t,\mathcal{L}
\right).
$$

Possible mechanisms include:

* random search
* evolutionary search
* coordinate search
* Bayesian optimization
* beam search
* candidate sampling
* rejection sampling

These are not inherently novel.

---

# 35. Self-Consistency Constraint

A more general formulation may use:

$$
\mathcal{C}_{self}(B,z,x)
$$

as a self-consistency constraint.

Then:

$$
\min_{B,z}
\mathcal{L}(B,z,x)
$$

subject to:

$$
\mathcal{C}_{self}(B,z,x)\geq\tau.
$$

Where:

$$
\tau
$$

is a predefined consistency threshold.

The exact definition of:

$$
\mathcal{C}_{self}
$$

is a central theoretical research problem.

---

# 36. Multi-Objective Formulation

SCBI may need to optimize multiple objectives:

$$
J
=
\mathcal{L}_{task}
+
\lambda_1\mathcal{L}_{consistency}
+
\lambda_2 C_{compute}
+
\lambda_3 C_{representation}.
$$

Therefore:

$$
(B^*,z^*)
=
\arg\min_{B,z}J.
$$

The research must avoid introducing unnecessary objectives.

Every additional term must have a scientific justification.

---

# 37. General Algorithm

A generic SCBI procedure is:

```text
Input:
    x
    frozen model fθ
    initial state z₀
    initial representation B₀
    evaluation function S
    candidate generator G
    update rule U
    maximum iterations T

For t = 0 ... T-1:

    1. Generate candidate representations:
       Cₜ = G(x, zₜ, Bₜ)

    2. Evaluate each candidate:
       sᵢ = S(Bᵢ, x, zₜ)

    3. Select best candidate:
       B*ₜ = argmax sᵢ

    4. Apply consistency/acceptance criterion.

    5. If accepted:
           Bₜ₊₁ = update(Bₜ, B*ₜ)
       Else:
           Bₜ₊₁ = Bₜ

    6. Update temporary state:
           zₜ₊₁ = U(zₜ, Bₜ₊₁, x)

Return:
    B*
    z*
    prediction ŷ
```

This is a conceptual algorithm.

It must not be treated as the final algorithm until tested against prior art.

---

# 38. Termination

Possible termination conditions include:

### Fixed iterations

$$
t=T.
$$

### Convergence

$$
|J_{t+1}-J_t|<\epsilon.
$$

### Representation convergence

$$
D(B_{t+1},B_t)<\epsilon_B.
$$

### No improvement

$$
J_{t+1}\geq J_t.
$$

### Consistency threshold

$$
C_t>\tau.
$$

The chosen termination condition must be predetermined for each experiment.

---

# 39. Computational Complexity

Let:

* \(T\) = number of iterations
* \(K\) = candidates per iteration
* \(F\) = cost of one model evaluation

Then a basic candidate-evaluation loop may have complexity approximately:

$$
O(TKF).
$$

Additional representation-generation cost:

$$
O(TK G)
$$

where \(G\) is candidate-generation cost.

Total:

$$
O(TK(F+G)).
$$

This must be measured empirically.

---

# 40. Memory Complexity

Let:

$$
d_B
$$

represent the size of the temporary representation.

If \(K\) candidates are stored simultaneously:

$$
O(Kd_B)
$$

additional memory may be required.

If candidates are evaluated sequentially:

$$
O(d_B)
$$

may be sufficient.

The implementation should prefer memory-efficient evaluation when scientifically equivalent.

---

# 41. Parameter Efficiency

Core SCBI must satisfy:

$$
\Delta |\theta|=0.
$$

However, temporary representation size may be nonzero:

$$
|\mathcal{B}|>0.
$$

Therefore SCBI potentially trades:

```text
persistent parameters
```

for:

```text
temporary inference computation/state.
```

This tradeoff must be measured.

---

# 42. Distinction From Fine-Tuning

Fine-tuning performs:

$$
\theta'
=
\operatorname{Update}(\theta).
$$

Core SCBI performs:

$$
\theta'=\theta.
$$

Instead:

$$
(B_t,z_t)
$$

may change.

Therefore:

```text
Fine-tuning:
change model parameters.

SCBI:
change temporary inference representation/state.
```

This distinction is necessary but not sufficient for novelty.

---

# 43. Distinction From Prompt Optimization

Prompt optimization changes an input or prompt representation:

$$
p\rightarrow p'.
$$

SCBI may operate on internal representations:

$$
h\rightarrow h'.
$$

However, if the final SCBI mechanism only changes prompts, the research may overlap strongly with prompt optimization.

The exact intervention location must therefore be specified.

---

# 44. Distinction From Activation Steering

Activation steering generally modifies internal activations using some steering mechanism.

SCBI may additionally:

1. construct candidate representations,
2. evaluate them,
3. select among them,
4. update them iteratively.

Whether this constitutes a meaningful distinction must be demonstrated.

---

# 45. Distinction From Test-Time Training

Test-time training may update parameters:

$$
\theta_t\rightarrow\theta_{t+1}.
$$

Core SCBI requires:

$$
\theta_t=\theta.
$$

If SCBI changes only temporary state/representation, the mechanisms differ.

However, the literature review must determine whether frozen-model test-time methods already perform equivalent state optimization.

---

# 46. Distinction From Self-Consistency Decoding

Self-consistency decoding may generate multiple outputs:

$$
y_1,\ldots,y_K
$$

and select an answer using agreement.

SCBI instead proposes evaluating representations:

$$
B_1,\ldots,B_K.
$$

But this difference alone does not prove novelty.

The exact candidate object and selection mechanism must be compared mathematically.

---

# 47. Distinction From RAG

RAG modifies available information by retrieving external documents:

$$
x\rightarrow(x,D).
$$

SCBI does not inherently require external retrieval.

However, if an implementation uses retrieval to construct \(B_t\), retrieval becomes an additional component and must be controlled.

---

# 48. Distinction From Model Editing

Model editing changes model behavior by modifying parameters or internal mechanisms.

Core SCBI must preserve:

$$
\theta.
$$

Any persistent modification must be treated as a separate variant.

---

# 49. Theoretical Research Questions

The theory phase must answer:

### TQ1

What exactly is a basis?

### TQ2

What mathematical object should \(B_t\) be?

### TQ3

What makes a representation an SCBI representation?

### TQ4

What exactly does "self-consistent" mean?

### TQ5

What information is allowed to construct \(B_t\)?

### TQ6

What information is forbidden?

### TQ7

Can \(B_t\) be optimized without changing \(\theta\)?

### TQ8

When does optimizing \(B_t\) reduce to latent optimization?

### TQ9

When does SCBI reduce to prompt optimization?

### TQ10

When does SCBI reduce to activation steering?

### TQ11

When does SCBI reduce to search?

### TQ12

What makes SCBI algorithmically distinct?

### TQ13

Can SCBI be formally shown to improve a class of problems?

### TQ14

What are its computational limits?

### TQ15

When should SCBI fail?

---

# 50. Required Counterexamples

The theory must actively construct counterexamples.

Examples:

### Counterexample 1

A frozen model where no temporary representation improves performance.

### Counterexample 2

A task where SCBI selects an unstable representation.

### Counterexample 3

A problem where more inference compute explains the entire improvement.

### Counterexample 4

A problem where prompt optimization performs equally well.

### Counterexample 5

A problem where latent optimization is mathematically equivalent.

### Counterexample 6

A problem where candidate generation collapses to random search.

These counterexamples are scientifically useful.

---

# 51. No Universal Improvement Claim

SCBI must not assume:

$$
P(SCBI)>P(Baseline)
$$

for every task.

The more realistic research objective is:

$$
\exists \mathcal{D}
:
P(SCBI|\mathcal{D})
>
P(Baseline|\mathcal{D})
$$

under identifiable conditions.

The research must investigate those conditions.

---

# 52. Conditional Research Hypothesis

A stronger formulation is:

> SCBI may provide benefits when the task contains inference-relevant structure that can be represented more effectively by a temporary task-specific representation than by the model's default representation.

This hypothesis is testable.

---

# 53. Failure Conditions

Potential failure modes include:

* representation collapse
* unstable optimization
* overfitting to evaluation signals
* evaluator mismatch
* excessive inference cost
* candidate redundancy
* poor candidate generation
* representation degeneracy
* no meaningful improvement
* compute-only gains
* benchmark-specific behavior
* sensitivity to initialization
* dependence on external information

Every major failure mode should eventually receive an experiment.

---

# 54. Generalization

A successful SCBI mechanism should not only work on a single benchmark.

Study:

$$
P(SCBI|\mathcal{D}_1)
$$

and:

$$
P(SCBI|\mathcal{D}_2)
$$

across distinct task families.

Potential axes:

* reasoning
* classification
* retrieval
* scientific problems
* coding
* multimodal tasks
* structured prediction

The actual benchmark selection belongs in the experiment specification.

---

# 55. Mechanistic Questions

If SCBI improves performance, investigate:

> What changed inside the computation?

Potential analyses include:

* representation geometry
* dimensionality
* activation distributions
* attention patterns
* feature utilization
* representation similarity
* candidate diversity
* convergence behavior
* state trajectories

Performance alone does not explain mechanism.

---

# 56. Representation Trajectory

SCBI may generate a trajectory:

$$
B_0,B_1,\ldots,B_T.
$$

Analyze:

$$
D(B_t,B_{t+1}).
$$

Potentially:

$$
D_t=D(B_t,B_{t+1}).
$$

This can reveal:

* rapid convergence
* gradual adaptation
* oscillation
* collapse
* instability
* task-dependent behavior

---

# 57. State Trajectory

Likewise:

$$
z_0,z_1,\ldots,z_T.
$$

Analyze:

$$
D(z_t,z_{t+1}).
$$

The relationship between:

$$
B_t
$$

and:

$$
z_t
$$

is itself a research question.

---

# 58. Minimal Theoretical Claim

Before attempting a strong theorem, establish the weakest meaningful claim:

> A frozen model can be coupled to a temporary inference-time representation mechanism without changing the underlying model parameters.

This is primarily a systems/theoretical construction.

The stronger claim:

> The mechanism improves inference performance.

requires empirical evidence.

An even stronger claim:

> SCBI provides an advantage under a defined class of problems.

requires both theory and empirical evidence.

---

# 59. Evidence Hierarchy

Theoretical claims should be categorized as:

### Definition

Established by explicit specification.

### Proposition

Supported by mathematical derivation.

### Theorem

Formally proved.

### Conjecture

Plausible but unproven.

### Hypothesis

Empirically testable claim.

### Observation

Empirical result.

### Interpretation

Explanation inferred from observations.

These categories must never be mixed.

---

# 60. No Unsupported Theorems

The theory agent must never generate a theorem merely because it makes the research appear stronger.

A theorem requires:

1. Precise assumptions.
2. Precise statement.
3. Valid derivation.
4. Proof.
5. Examination of edge cases.
6. Attempted counterexample.

If any of these are missing, label the claim appropriately.

---

# 61. Theoretical Deliverables

The theory phase should eventually produce:

```text
theory/
├── README.md
├── definitions.md
├── assumptions.md
├── formulation.md
├── algorithm.md
├── complexity.md
├── objectives.md
├── guarantees.md
├── limitations.md
└── proofs/
```

These files should be created progressively.

Do not fill them with speculative mathematics simply to complete the directory.

---

# 62. Mathematical Notation Policy

Use consistent notation throughout the repository.

Recommended initial notation:

| Symbol            | Meaning                    |
| ----------------- | -------------------------- |
| \(x\)             | input                      |
| \(y\)             | target                     |
| \(\theta\)        | frozen model parameters    |
| \(f_\theta\)      | frozen foundation model    |
| \(h_t\)           | internal representation    |
| \(B_t\)           | temporary representation   |
| \(z_t\)           | temporary inference state  |
| \(\mathcal{C}_t\) | candidate set              |
| \(G\)             | candidate generator        |
| \(S\)             | candidate score            |
| \(\mathcal{L}\)   | loss                       |
| \(U\)             | state update               |
| \(R\)             | representation update      |
| \(T\)             | maximum iterations         |
| \(K\)             | candidates per iteration   |
| \(\tau\)          | threshold                  |
| \(\lambda\)       | regularization coefficient |

If the theory changes these definitions, update the source-of-truth document and record the change.

---

# 63. Definition Change Protocol

If a mathematical definition changes, record:

```text
Previous definition:
New definition:
Reason:
Evidence:
Affected equations:
Affected experiments:
Date:
```

Never silently redefine:

$$
B_t
$$

or:

$$
z_t.
$$

---

# 64. Core vs Variant Theory

The repository must distinguish:

## Core SCBI

$$
\Delta\theta=0.
$$

Temporary representation/state adaptation is allowed.

## Variant SCBI

Any modification beyond the core formulation.

Examples:

```text
SCBI + parameter adaptation
SCBI + retrieval
SCBI + external verifier
SCBI + learned candidate generator
SCBI + multimodal representation
```

Variants must never be silently presented as the core algorithm.

---

# 65. Theory-to-Experiment Contract

Every theoretical component must eventually correspond to an experiment.

Example:

$$
B_t
$$

→ measure representation change.

$$
z_t
$$

→ measure state trajectory.

$$
C(B_t)
$$

→ ablate consistency criterion.

$$
K
$$

→ compute scaling experiment.

$$
T
$$

→ convergence experiment.

If a theoretical component cannot be experimentally examined, its role must be justified.

---

# 66. Minimal Formal Objective

Until stronger theory is established, the safest generic formulation is:

$$
\boxed{
(B^*,z^*)
=
\operatorname{Search}
\left[
\mathcal{L}
\left(
f_\theta(x;B,z)
\right),
\mathcal{C}_{self}(B,z,x),
C(B,z)
\right]
}
$$

subject to:

$$
\boxed{\theta\text{ is frozen}}
$$

This is intentionally broad.

It should be refined only after literature and theoretical analysis.

---

# 67. Core Scientific Test

The central experiment eventually needs to distinguish:

```text
Frozen model
        ↓
default representation
        ↓
prediction
```

from:

```text
Frozen model
        ↓
temporary representation construction
        ↓
candidate evaluation
        ↓
selection/update
        ↓
prediction
```

while controlling for:

* model
* data
* information
* inference compute
* evaluation
* random seed
* preprocessing

The goal is to isolate the effect of the temporary representation mechanism.

---

# 68. Ultimate Theoretical Goal

The theory should eventually answer:

> **Under what conditions can a frozen model benefit from inference-time construction and selection of temporary representations, and what distinguishes this process from existing latent optimization, test-time adaptation, activation steering, prompting, search, and other inference-time methods?**

That is the central theoretical target.

---

# 69. Non-Negotiable Rules

1. Never assume \(B_t\) is a mathematical basis without proof or definition.
2. Never assume self-consistency is novel.
3. Never change \(\theta\) in core SCBI.
4. Never hide parameter updates.
5. Never claim a theorem without a proof.
6. Never use notation to disguise an existing method.
7. Never confuse mathematical formulation with algorithmic novelty.
8. Never confuse empirical improvement with theoretical guarantee.
9. Never ignore equivalent formulations from other fields.
10. Never optimize the theory solely to produce positive experiments.
11. Always construct counterexamples.
12. Always preserve failed formulations.
13. Record major definition changes.
14. Compare against mathematically equivalent methods.
15. Keep core SCBI separate from variants.

---

# 70. Final Principle

The purpose of this theory is not to make SCBI look mathematically sophisticated.

The purpose is to make the research **precise enough to be wrong**.

A useful theory is one where another researcher can say:

> "Here is exactly what SCBI claims."

and then determine:

> "Here is exactly where that claim fails—or where the evidence supports it."

That standard must guide the remainder of the SCBI research.
