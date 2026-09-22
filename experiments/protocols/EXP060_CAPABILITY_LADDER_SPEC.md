# EXP060 Protocol Specification: Relational Capability Ladder and Intervention-Ceiling Decomposition

**Status:** PRE-REGISTERED (Diagnostic & Falsification-Oriented)  
**Date:** 2026-09-21  
**Predecessor Experiments:** EXP056, EXP057, EXP058, EXP059  
**Governing Standard:** `AGENTS.md` (14 Inviolable Laws) & `STATISTICAL_PROTOCOL_V02.md`  

---

## 1. Scientific Mandate & Core Question

Following EXP059's definitive negative result (Specificity Gap = $-0.176$, confirming that single-shot linear interventions failed to induce transitive deduction and shifted structural controls more than relational queries), the research program transitions from monolithic benchmarks to an explicit **diagnostic capability decomposition**:

$$\boxed{\textbf{Can ANY intervention recover missing computation, or is there an intervention/representation ceiling?}}$$

We isolate where failure occurs within the tri-partite decomposition:
```text
                         SCPM Diagnostic Tree
                                  │
          ┌───────────────────────┼───────────────────────┐
          ▼                       ▼                       ▼
Representation Discovery   Intervention Operator    Model Capability Ceiling
 (Autonomous Bottleneck)     (Wrong Math/Routing)     (Latent Signal Absent)
          │                       │                       │
 Oracle > Base, Auto <= Base     All Operators Fail      Oracle <= Base
```

---

## 2. The 6-Level Relational Capability Ladder

To pinpoint the exact boundary of causally recoverable computation in frozen Pythia-160M ($\Delta\theta = 0$), we construct a calibrated 6-level capability ladder:

### Level 0: Lexical In-Context Association (Recall)
- **Form:** $A \to B$. Direct associative binding in context.
- **Example:** `"Item Alpha is paired with target Blue. Item Beta is paired with target Red. Given Item Alpha, the paired target is:"` $\to$ **Blue**.
- **Mechanistic Anchor:** Single-hop induction / associative recall.

### Level 1: Direct Relational Mapping (1-Hop)
- **Form:** $A > B \to$ query relation.
- **Example:** `"Statement: Alice is taller than Bob. Question: Who is taller, Alice or Bob?"` $\to$ **Alice**.
- **Mechanistic Anchor:** Direct lexical comparison without chaining.

### Level 2: 2-Hop Transitive Deduction (Clean Chain)
- **Form:** $A > B \wedge B > C \implies A > C$.
- **Example:** `"Statement: Alice is taller than Bob. Bob is taller than Charlie. Question: Who is taller, Alice or Charlie?"` $\to$ **Alice**.
- **Positional Permutation Control:** Symmetrically evaluated with reversed surface order (`"Charlie is shorter than Bob. Bob is shorter than Alice. Who is taller?"`) to disentangle semantic order from surface position heuristics.

### Level 3: 3-Hop Transitive Deduction (Deep Chain)
- **Form:** $A > B \wedge B > C \wedge C > D \implies A > D$.
- **Example:** `"Statement: Alice is taller than Bob. Bob is taller than Charlie. Charlie is taller than David. Question: Who is taller, Alice or David?"` $\to$ **Alice**.
- **Mechanistic Anchor:** Multi-step relational composition.

### Level 4: Distractor-Resistant Transitivity (Interleaved Chain)
- **Form:** $A > B \wedge X > Y \wedge B > C \wedge Z > Q \implies A > C$.
- **Example:** Interleaving 2 irrelevant relational statements between the relevant premises.
- **Mechanistic Anchor:** Relational routing and distractor suppression under compositional deduction.

### Level 5: Compositional Transfer (Disjoint Surface Vocabulary)
- **Form:** 2-hop transitive deduction implemented across completely disjoint symbolic / novel tokens.
- **Mechanistic Anchor:** Cross-vocabulary structural invariance ($C4$).

---

## 3. The Tri-Condition Evaluation Scheme

At **every single level** $k \in \{0, 1, 2, 3, 4, 5\}$, three conditions are evaluated on identical instances:

1. **Condition 1: Base Model (Greedy)**  
   The unintervened, frozen model forward pass ($\Delta\theta = 0$). Establishes native accuracy $M_{\text{base}}(k)$.
2. **Condition 2: Privileged Oracle Intervention**  
   An intervention constructed with privileged knowledge of the ground-truth relational contrast:
   $$v^* = \frac{\mu(h_{\text{target}}) - \mu(h_{\text{foil}})}{\|\mu(h_{\text{target}}) - \mu(h_{\text{foil}})\|}, \quad h \leftarrow h + \alpha v^*$$
   Tests whether the latent space contains *any* recoverable signal that can improve the computation when guided by an optimal direction.
3. **Condition 3: Autonomous SCPM**  
   An unguided candidate generation and counterfactual selection procedure operating strictly without labels or privileged spans.

---

## 4. Pre-Registered Diagnostic Adjudication Criteria

For each level $k$:

1. **Diagnostic Outcome A: Representation / Intervention Ceiling**
   $$\Delta M_{\text{oracle}}(k) \le 0 \quad \text{and} \quad \Delta\log p_{\text{oracle}}(k) \le 0$$
   *Conclusion:* The model representations lack causally accessible signals for level $k$, or the intervention operator family cannot express the required transformation. This identifies the hard computational boundary of the backbone.
2. **Diagnostic Outcome B: Autonomous Discovery Bottleneck**
   $$\Delta M_{\text{oracle}}(k) > 0 \quad \text{and} \quad \Delta M_{\text{auto}}(k) \le 0$$
   $$\boxed{RDG(k) \equiv M_{\text{oracle}}(k) - M_{\text{auto}}(k) > 0}$$
   *Conclusion:* Computational recoverability ($C2$) is supported, but autonomous discovery ($C3$) fails. The bottleneck is strictly localized to discovery/selection.
3. **Diagnostic Outcome C: Autonomous Capability Confirmed**
   $$\Delta M_{\text{auto}}(k) > 0 \quad \text{and} \quad p_{\text{McNemar}} < 0.05 \quad \text{and} \quad RDG(k) \le 0.5 \times \Delta M_{\text{oracle}}(k)$$
   *Conclusion:* Both causal recoverability ($C2$) and autonomous discovery ($C3$) are supported at level $k$.

---

## 5. Experimental Controls & Protocol Safeguards

1. **Positional Balance:** At all relational levels, target entity position is balanced (50% first-entity correct, 50% second-entity correct) to prevent surface-order exploitation.
2. **Frozen Backbone:** Pythia-160M parameters verified invariant via pre- and post-run SHA-256 hash.
3. **Instance Size:** $N = 30$ instances per level ($6 \times 30 = 180$ instances total).
4. **Statistical Testing:** Exact paired McNemar tests and 10,000-resample bootstrap confidence intervals.
