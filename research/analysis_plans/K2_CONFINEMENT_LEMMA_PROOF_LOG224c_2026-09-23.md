# Positional-Confinement Lemma — Standalone Proof

**LOG-224c · Track-8 pre-registration drafter · 2026-09-23**
**Status:** standalone proof document for the positional-confinement lemma (K2 pre-registration REV1 §5 L1; REV2 §5 L1).
**Epistemic grade:** [PROPOSITION].
**DO NOT CITE AS [THEOREM] — requires Law #14 review for [THEOREM] promotion.**
**Use in K2 REV2:** required for the [THEOREM] promotion path, NOT a blocker for pilot SIGN — per the LOG-224b ruling, the inline §5 proof suffices for pilot SIGN.

---

## 1. Statement (exact; REV1 §5 L1, REV2 §5 L1 — unchanged)

Let M be a causal (left-to-right masked) decoder transformer with per-position residual streams and additive intervention δ applied to the layer-l* output at a set of positions P. Then:

- **(i)** for all layers l > l* and all positions j < min(P), the activation at (l, j) equals the unintervened activation;
- **(ii)** if P = {p_last} (final position only), δ influences the output logits only through the final-position residual path — **no δ transport between positions** is possible, because no position j > p_last exists; the final-position residual passes through local downstream operators (residual-path LayerNorm/MLPs at the final position, final LayerNorm, unembedding);
- **(iii)** if P ⊆ {positions < p_last} (G10-disjoint from the final position), δ can influence the final-token logits only through attention computations at layers l > l* (queries at positions > p attending to keys at p) — attention is the only inter-position channel in the frozen architecture (LayerNorm and MLPs are per-position operators [FACT]).

---

## 2. Notation and assumptions

- h_{l,j} ∈ R^d: residual-stream activation at layer l, position j (l = 0…L, j = 0…T−1).
- Layer block: h_{l,j} = h_{l−1,j} + A_{l,j} + F_{l,j}, where A_{l,j} (attention-block output) and F_{l,j} (MLP-block output) act per position; normalization layers are per-position operators [ASSUMPTION — architectural [FACT] for GPT-NeoX-style decoders].
- Attention at position j reads only keys/values from positions k ≤ j (causal mask) [FACT]; i.e., A_{l,j} = f_{l,j}({h_{l−1,k} : k ≤ j}).
- Intervention: x̃_{l*,p} = h_{l*,p} + δ for p ∈ P; every other (l, j) activation equals the unintervened h_{l,j}.
- Decision read: logits = U(LN(h_{L,p_last})) — logits are read at the final token [FACT — all corpus runs read `logits[0, −1, :]`].

---

## 3. Proof

### 3.1 Part (i) — induction on layers

**Base (l = l*):** for j < min(P), j ∉ P, so h_{l*,j} is unintervened.

**Induction hypothesis:** for layer l−1 (l−1 ≥ l*), h_{l−1,j} equals the unintervened activation for all j < min(P).

**Step:** consider layer l and position j < min(P). The attention output A_{l,j} depends only on {h_{l−1,k} : k ≤ j} (causal mask). Since j < min(P), every k ≤ j satisfies k < min(P); by the induction hypothesis every input is unintervened, so A_{l,j} is unchanged. The MLP output F_{l,j} and the LayerNorm at j depend only on position-j quantities, which are unintervened. Hence h_{l,j} = h_{l−1,j} + A_{l,j} + F_{l,j} equals the unintervened value.

By induction, for all l ≥ l* and all j < min(P), the activation at (l, j) equals the unintervened activation. ∎

### 3.2 Part (ii) — P = {p_last}

Here min(P) = p_last. By (i), for all l > l*, every position j < p_last carries no δ. No position j > p_last exists. The decision logits are read at p_last. Therefore δ can influence the logits only through the residual path at position p_last itself, from layer l* to the readout — through the local downstream operators (residual-path LayerNorm/MLPs at the final position, final LayerNorm, unembedding). **No δ transport between positions is possible.** ∎

*Scope note:* the claim is positional, not computational — attention at p_last still executes over unchanged keys/values; the lemma does not say attention is "bypassed" or "off." (This is why REV1 §0 item 4 conformed the loose glosses.)

### 3.3 Part (iii) — P ⊆ {positions < p_last} (the G10 disjointness premise)

Disjointness: p_last ∉ P, so h_{l*,p_last} is unintervened. By (i), all positions j < min(P) are unintervened at all l > l*. For l > l*, the update at (l, p_last) comes from exactly two sources: (a) its own attention A_{l,p_last}, whose keys/values range over positions k ≤ p_last — *including* p ∈ P where δ lives; (b) per-position operators (MLP, LayerNorm), which see only position-p_last quantities and therefore cannot introduce δ from any other position. Hence the only channel by which δ can reach the p_last residual — and thereby the final-token logits — is attention computation at layers l > l* (queries at positions > p attending to keys at p ∈ P). Attention is the only inter-position channel in the frozen architecture (LayerNorm and MLPs are per-position operators [FACT]). ∎

---

## 4. What the lemma does and does not license

- **Does:** license the K2 (a) FINAL-ONLY arm — with P = {p_last}, any rescue is final-position-local: no upstream δ transport — and the (b) ENTITY-ONLY arm — any effect from causally-upstream positions must travel between positions, i.e., through attention.
- **Does not:** bound *attenuation*. The lemma says which channels *can* carry δ, not how much they dilute it; 12 layers of attention mixing can wash a real routing signal below the L1 MDE. That asymmetry is REV2's conceded load-bearing risk (§5 A6, §8 steelmans 1–2) — it is priced as the Inconclusive partition, not proven away.

---

## 5. Grade and promotion path

**Grade: [PROPOSITION]** (canonical reporting layer: INFERENCE — an in-house derivation whose inputs, the causal mask and the per-position operators, are [FACT]). The proof was re-derived from scratch and survived the LOG-224 and LOG-224b reviews with no hole found.

**Promotion path:** to [THEOREM] via Law #14 adversarial review of this document. Until then, no program-level belief change may cite the lemma as [THEOREM]; the K2 verdicts cite it as [PROPOSITION] per REV2 §5.
