# EXP061 Protocol Specification: Mechanistic Dissection of Transitive Intervention Efficacy

**Status:** PRE-REGISTERED (Diagnostic & Dissection-Oriented)  
**Date:** 2026-09-21  
**Predecessor Experiments:** EXP059, EXP060  
**Governing Standard:** `AGENTS.md` (14 Inviolable Laws) & `STATISTICAL_PROTOCOL_V02.md`  

---

## 1. Scientific Mandate & Core Question

EXP060 demonstrated that a ground-truth-informed linear representation intervention at Layer 7 achieves a large, statistically significant performance gain on 2-hop and 3-hop transitive reasoning tasks:
$$\Delta M_{L2} = +36.7\text{ pp} \quad (b=11, c=0, p = 0.0005)$$
$$\Delta M_{L3} = +36.7\text{ pp} \quad (b=13, c=2, p = 0.0037)$$

However, this gain coexists with a substantial probability distribution disruption ($\text{Mean } \Delta\log p \approx -8.3$) and fails to generalize across 1-hop mappings, distractor-interleaved chains, and novel planetary entities.

Before designing further benchmarks, EXP061 isolates:
$$\boxed{\textbf{Where does the }+36.7\text{ pp effect at Levels 2 and 3 come from?}}$$
Specifically: **Does the successful intervention modify relational computation, or merely exploit a stable lexical/positional vulnerability in the benchmark?**

---

## 2. Ten Diagnostic Tests

To resolve whether the effect represents relational steering or blunt option suppression, EXP061 conducts 10 targeted mechanistic tests on the Level-2 and Level-3 benchmark splits ($N=60$ total instances):

### Test 1: Target-Token Logit Shift ($\Delta \text{Logit}_{\text{target}}$)
- Measures raw logit shift for the ground-truth target token before softmax.

### Test 2: Foil-Token Logit Shift ($\Delta \text{Logit}_{\text{foil}}$)
- Measures raw logit shift for the incorrect foil token before softmax.
- **Diagnostic Ratio:**
  $$R_{\text{shift}} = \frac{\Delta \text{Logit}_{\text{target}}}{\Delta \text{Logit}_{\text{foil}}}$$
  If $\Delta \text{Logit}_{\text{target}} \approx 0$ while $\Delta \text{Logit}_{\text{foil}} \ll 0$, the intervention acts via targeted foil suppression rather than target amplification.

### Test 3: All-Vocabulary Logit Redistribution & Top-$k$ Turnover
- Measures shift in non-target, non-foil vocabulary logits across the entire 50,257-token vocabulary.
- Computes Top-10 token turnover, output entropy change $\Delta H$, and KL divergence $D_{\text{KL}}(P_{\text{base}} \parallel P_{\text{intervened}})$.

### Test 4: Position-Specific Injection
- Compares injection at the final query token position ($t_{\text{query}}$) against injection at:
  - Premise subject token ($t_{\text{premise1}}$)
  - Premise verb token ($t_{\text{verb}}$)
  - Uniform injection across all sequence positions.

### Test 5: Entity-Specific vs. Random Direction
- Replaces the informed direction $v^*$ with:
  - $v_{\text{rand}}$: Random unit vector in $\mathbb{R}^{d}$.
  - $v_{\text{shuff}}$: Randomly shuffled dimensions of $v^*$.

### Test 6: Name-Swapped Intervention (Lexical vs. Relational Specificity)
- Inverts the entity names in the intervention vector while maintaining the prompt, testing whether the vector encodes specific token embeddings (`Alice`, `Bob`) or the abstract comparative relation.

### Test 7: Premise Permutation Sensitivity
- Evaluates whether the $+36.7\text{ pp}$ intervention rescues the model under reversed premise order ($C < B < A$), or whether its benefit is restricted to canonical surface order ($A > B > C$).

### Test 8: Operator Sign Reversal
- Inverts the intervention sign ($\alpha \to -\alpha$).
- Tests whether performance symmetrically degrades / inverts.

### Test 9: Rank-Preserving Orthogonal Controls
- Projects $v^*$ onto the orthogonal complement of the unembedding difference $(W_U[\text{target}] - W_U[\text{foil}])^{\perp}$, testing whether direct unembedding alignment is necessary for the benefit.

### Test 10: Paired Instance-Level Outcome Ledger
- For every condition, reports exact instance-level paired outcomes:
  $$b = \text{base wrong, intervention correct}$$
  $$c = \text{base correct, intervention wrong}$$
  $$\Delta M = \frac{b - c}{N}$$
  with exact paired McNemar $p$-values.

---

## 3. Pre-Registered Decision Framework

1. **Outcome A: Genuine Relational Induction Confirmed**
   $$\Delta \text{Logit}_{\text{target}} > 0 \quad \wedge \quad \text{Maintains gain on permuted premises} \quad \wedge \quad D_{\text{KL}} \le 1.0$$
   *Conclusion:* The intervention genuinely strengthens latent transitive relational computation.
2. **Outcome B: Lexical / Positional Vulnerability Exploitation Confirmed**
   $$\Delta \text{Logit}_{\text{target}} \le 0 \quad \wedge \quad \Delta \text{Logit}_{\text{foil}} \ll 0 \quad \wedge \quad \text{Collapses on permuted premises}$$
   *Conclusion:* The intervention does not induce transitive reasoning; it exploits an asymmetric logit suppression vulnerability that accidentally aligns with the correct answer under canonical prompt ordering.
