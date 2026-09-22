# EXP062 Protocol Specification: Representation-vs-Decision Disambiguation

**Status:** PRE-REGISTERED (Falsification Experiment & Hierarchical Causal Audit)  
**Date:** 2026-09-21  
**Predecessor Experiments:** EXP059, EXP060, EXP061  
**Lead Agents:** Research Manager, Theory Agent, Experiment Agent, Adversarial Reviewer  
**Governing Standard:** `AGENTS.md` (14 Inviolable Laws) & `STATISTICAL_PROTOCOL_V02.md`  

---

## 1. Scientific Mandate & Core Problem

EXP061 established that single-layer linear representation interventions ($h \leftarrow h + \alpha v$) can cleanly and selectively shift output decision margins ($\Delta \text{Logit}_{\text{target}} \approx +0.12, \Delta \text{Logit}_{\text{foil}} \approx -0.14, D_{\text{KL}} \le 0.0014$), achieving a statistically significant accuracy improvement ($+13.3\text{ pp}, p=0.0039$) with minimal vocabulary disturbance (supporting Capability **C5: Mechanistic Specificity**).

However, EXP061 also demonstrated that this intervention leaves the model's severe premise-order dependence completely unameliorated (canonical premise accuracy = 70.0% vs. reversed premise accuracy = 33.3%, gap = $+36.7\text{ pp}$).

This establishes a fundamental scientific dilemma:
$$\boxed{\textbf{Is the SCBI vector encoding a relational computation, or is it merely an output decision direction whose construction happens to correlate with the correct answer?}}$$

EXP062 is a pre-registered falsification benchmark designed to resolve this distinction through a hierarchical causal decomposition.

---

## 2. Competing Hypotheses & Primary Endpoints

### 2.1 Primary vs. Secondary Endpoints
- **Primary Endpoint:** **Behavioral Causal Transfer** ($\Delta M_{\text{transfer}}$):
  $$\Delta M_{\text{transfer}} = M(v_{\text{source}} \to \text{heldout}) - M_{\text{baseline}}$$
  accompanied by exact paired outcomes ($b$ rescues, $c$ corruptions, exact McNemar $p$).
- **Secondary Mechanistic Endpoint:** **Representation Subspace Similarity** ($S_{\text{rel}}$):
  $$S_{\text{rel}} = \cos(v_i, v_j)$$
  *Note:* Two vectors can encode equivalent functions without being geometrically identical, and conversely, high cosine similarity does not guarantee functional causal rescue. Behavioral transfer is the supreme arbiter of computational recovery.

### 2.2 Formal Hypotheses
- **Hypothesis A ($H_A$): Relational Representation Hypothesis**
  The intervention captures an abstract relational operator:
  $$\Delta M_{\text{transfer}}(v_{A>B>C} \to X>Y>Z) > 0 \quad (p < 0.05)$$
  Transfer succeeds across disjoint entities, vocabulary, and domains sharing the identical transitive relation.
- **Hypothesis B ($H_B$): Decision / Lexical Representation Hypothesis**
  The intervention operates as a localized decision-boundary shift tied to surface tokens or prompt geometry:
  $$\Delta M_{\text{transfer}}(v_{A>B>C} \to X>Y>Z) \le 0$$
  The intervention's efficacy collapses when target/foil identities change or when query polarity is reversed.

---

## 3. Hierarchical Four-Tier Invariance Model

Claims of "relational representation" must satisfy a 4-tier hierarchy of progressively harder invariances:

1. **Tier 1 — Output Identity:**
   Does the vector simply encode the direct unembedding contrast $W_U[t] - W_U[f]$? (Evaluated via isolated token subtraction without relational context).
2. **Tier 2 — Entity Invariance:**
   Does the intervention discovered on $A > B > C$ transfer to $X > Y > Z$ under identical syntax?
3. **Tier 3 — Surface Invariance:**
   Does the intervention survive changes in relational wording (`taller` $\to$ `higher`), premise presentation order, and query polarity?
4. **Tier 4 — Structural Invariance:**
   Does the intervention transfer across completely disparate domains (e.g., human names $\to$ planetary sizes)?

*Epistemological Constraint:* Only successful causal transfer at **Tier 4** justifies the term *"abstract relational representation"*.

---

## 4. Causal-Factor Matrix

Because surface transformations frequently confound multiple computational variables (lexical identity, tokenization, positional encoding, and attention routing), each diagnostic condition is explicitly classified:

| Condition | Lexical | Position | Syntax | Relation | Main Causal Inference |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **1. Target/Foil Relabeling** | ✓ | same | ~ | same | Output token binding vs. abstract choice |
| **2. Entity Permutation** | ✓ | ~ | same | same | Entity invariance (Tier 2 transfer) |
| **3. Vocabulary Substitution** | ✓ | same | ~ | same | Wording / lexical invariance |
| **4. Premise Reordering** | same | ✓ | ✓ | same | Order invariance (attention robustness) |
| **5. Query Polarity Reversal** | ~ | same | ✓ | inverted | Polarity alignment / functional inversion |
| **6. Random Matched-Norm** | — | — | — | — | Null reference direction |
| **7. Isolated Unembedding Contrast** | ✓ | same | None | None | Tier 1 baseline (non-relational context) |
| **8. Cross-Instance Swap (Within-Task)** | ✓ | ✓ | ✓ | different | Instance specificity vs. task generalizability |
| **9. Mean Relational Vector ($\bar{v}_{\text{rel}}$)** | ~ | ~ | ~ | same | Shared subspace efficacy |
| **10. Cross-Domain Transfer (Planetary)** | ✓ | ✓ | ✓ | same | Tier 4 Structural invariance |
| **11. Relation-Inverted Negative Control** | same | ~ | same | inverted | Causal direction vs. surface entity alignment |

*(Note: `~` denotes entangled factors such as BPE segmentation, positional phase shifts, or attention-pattern adjustments).*

---

## 5. Representation Similarity Matrix (Identity Baseline)

Before interpreting behavioral transfer, EXP062 computes the identity baseline matrix measuring $S_{\text{rel}} = \cos(v_i, v_j)$ across 5 reference pairings:

1. **Same Relation, Same Vocabulary ($S_{\text{base}}$):** Pairs of instances with identical relation and vocabulary.
2. **Same Relation, Different Entities ($S_{\text{ent}}$):** Transitive instances with disjoint entity names.
3. **Same Relation, Different Syntax ($S_{\text{syn}}$):** Transitive instances with synonym wording.
4. **Different / Inverted Relation, Same Entities ($S_{\text{inv}}$):** $A > B > C$ vs. $C > B > A$ using the exact same names.
5. **Random Unrelated Pairs ($S_{\text{rand}}$):** Independent random instances.

### Formal Representation-Level Criterion:
$$\boxed{S_{\text{rel}}(\text{Same Relation}) > S_{\text{rel}}(\text{Different Relation})}$$
If $\cos(v_{ABC}, v_{XYZ}) \le \cos(v_{ABC}, v_{CBA})$ or matches random pairs, the geometric vectors cannot be interpreted as encoding relation-specific latent coordinates.

---

## 6. The Relation-Inverted Control (Crucial Negative Control)

To isolate whether the vector tracks **relational direction** or merely **entity surface presence**:
- Given instance $I_{\text{canonical}}$: `"Alice is taller than Bob. Bob is taller than Charlie. Who is tallest? (Alice / Charlie)"` producing $v_{\text{canonical}}$.
- Construct matched counterfactual $I_{\text{inverted}}$: `"Charlie is taller than Bob. Bob is taller than Alice. Who is tallest? (Charlie / Alice)"`.
- Both instances share identical entity vocabulary, syntactic framing, and option choices, but have opposite relational truths.
- **Evaluation:**
  - Vector alignment: $\cos(v_{\text{canonical}}, v_{\text{inverted}})$.
  - Cross-transfer: Applying $v_{\text{canonical}}$ to $I_{\text{inverted}}$. If the vector encodes relational truth, it must harm or invert $I_{\text{inverted}}$; if it merely biases toward `Alice`, it will corrupt the counterfactual.

---

## 7. Four Primary Metrics per Condition

For every condition, EXP062 logs:
1. **Accuracy Shift:** $\Delta M = \frac{b - c}{N}$, with paired rescues ($b$), corruptions ($c$), and exact two-tailed McNemar $p$-value.
2. **Decision Margin Shift:** $\Delta m_{\text{target-foil}} = \frac{1}{N}\sum (\Delta \text{Logit}_{\text{target}} - \Delta \text{Logit}_{\text{foil}})$.
3. **Distributional Distortion:** Kullback-Leibler divergence $D_{\text{KL}}(P_{\text{intervened}} \parallel P_{\text{base}})$ and Top-10 vocabulary overlap percentage.
4. **Representation Alignment:** $\cos(v_{\text{source}}, v_{\text{target}})$.

---

## 8. Pre-Registered Decision Tree

The outcome of EXP062 is pre-registered across four mutually exclusive scientific pathways:

1. **Branch 1: Abstract Relational Basis Confirmed**
   - Condition 9 (Cross-Instance) and Condition 10 (Cross-Domain) achieve statistically significant positive transfer ($\Delta M_{\text{transfer}} > 0, p < 0.05$).
   - Relation-Inverted Control confirms functional polarity reversal.
   - *Interpretation:* SCBI constructs a reusable, transferable computational representation of transitive ordering.
2. **Branch 2: Representation Similarity without Functional Transfer**
   - $\cos(v_i, v_j)$ is high across instances ($> 0.50$), but behavioral transfer fails ($\Delta M_{\text{transfer}} \le 0$).
   - *Interpretation:* The model represents similar relational features in activation space, but single-layer additive injection is insufficient to drive downstream reasoning circuits across differing contexts.
3. **Branch 3: Functional Transfer without Geometric Identity**
   - Behavioral transfer succeeds ($\Delta M_{\text{transfer}} > 0$), but cosine similarity between instance vectors is low ($\cos(v_i, v_j) \approx 0$).
   - *Interpretation:* Different surface realizations recruit distinct functional coordinate subspaces that nevertheless execute equivalent decision steering.
4. **Branch 4: Surface / Instance-Specific Decision Direction Confirmed**
   - Neither behavioral transfer nor representation similarity holds ($\Delta M_{\text{transfer}} \le 0$, $\cos \le \cos_{\text{rand}}$).
   - Condition 7 (Isolated Unembedding Contrast) matches or exceeds contextual intervention efficacy.
   - *Interpretation:* The SCBI vector is an instance-specific decision boundary shift at the unembedding layer. The current basis-construction mechanism does not construct abstract relational representations.
