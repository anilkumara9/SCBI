# EXP085 — Runner-up suppression cascade (I2) — PRE-REGISTRATION SKELETON (DRAFT)

> **STATUS: KILLED AS DESIGNED — CEO decision LOG-323 (2026-09-24).** Binding independent adjudication LOG-317: CONFIRM-VACUOUS. The k = 2 pin holds on all seven in-repo sources; at k = 2 the design collapses algebraically (ΔM_C2 ≡ 2·(N_f/60) − 1; Tier-0 Type-I = 1.00, kill-bar power 0.00; C3 undefined; C7 ≡ N_f/60). Do not execute. Do not re-register under a new number inheriting reviewed standing — any multi-option revival is a fresh innovation-pipeline proposal. Body below retained untouched per Law #8.
>
> _Original header follows:_

# EXP085 — Runner-up suppression cascade (I2) — PRE-REGISTRATION SKELETON (DRAFT)

> **STATUS: DRAFT — NOT SIGNED. Pre-Law #14. No experiment number is minted by
> this file; EXP085 is the *recommended* number (LOG-282; verified unclaimed in
> the research log). This skeleton exists so the next wave can cost, review,
> and formalize it. Do not execute.**

## 1. Objective (one sentence)

Test whether 2-hop relational failures are *selection* failures (the correct
answer is present at low latent rank but suppressed by a dominant wrong top-1)
repairable by target-free competitor suppression — a subtractive, readout-side,
Law-#7-compliant intervention, structurally disjoint from every additive static
direction the program has tested.

## 2. Law #15 gate card

1. **Precise question:** On headroom-verified 2-hop items the frozen model gets
   wrong, what is the latent rank of the correct option in frozen logits, and
   does masking the top-1 competitor (runner-up decode) change decisions?
   Endpoint: ΔM (decision changes), exact McNemar, N=60 (GPU population: the
   full 60-item headroom set, corruptions counted — F9).
2. **Decision it changes:** KILL / CONTINUE on the interference-repair
   mechanism family. CONTINUE licenses the program's first Law-#7-compliant
   autonomous rescue primitive and reframes the failure taxonomy
   (selection vs knowledge). KILL (either branch) closes the erasure family.
3. **Cheapest falsifying test:** Tier-0 latent-rank screen first — median
   correct-rank on failed headroom items from a ≤60-pass frozen-logit rebuild
   (LOG-284 returned archive-feasibility NEGATIVE: the EXP065/066/077 archives
   lack per-item logits, so the "$0 screen" label is retired; rebuild ≈3s on
   2×T4, CPU-trivial in pass count). Screen rule, pre-registered (F4):
   median ≤ 3 → Tier-0 passes; median in (3,5] → INCONCLUSIVE-hold → no GPU
   (rank profile published as measurement either way); median > 5 → family
   dead, no GPU. If screen passes: 60 items × 7 arms ≈ 420 forward passes ≈
   <1 min on 2×T4. Tier-0 sequenced piggyback on the K2→EXP083→EXP084 queue or
   standalone per CEO/Lead.
4. **Mathematical license:** [CONJECTURE] winner-take-all readout with foil
   interference: p(correct) is high but argmax is captured by a competitor.
   Quantitative predictions (re-derived under the F9 full-set population pin):
   (a) Tier-0: median correct-rank ≤ 3 on failed items (null median = (k+1)/2,
   F8 — licensed only if k ≥ 6); (b) predicted ΔM_C2 = (f2 − N_corr)/60, where
   f2 = # failed items with the correct option at rank 2 (Tier-0 measured) and
   N_corr = # baseline-correct items (corruptions: masking the true top-1 on a
   correct item always corrupts under single-answer MC with the deterministic
   F8 tie-break); (c) under the interference reading, E[ΔM_C4] ≈ ΔM_C2/k (F1:
   C4 masks one uniform-random option *including* the top-1, so it hits the
   true competitor with probability 1/k). Bar honesty (F3): at N=60 the
   pre-registered CONTINUE bar (LCI > δ_min = 0.05) requires observed net ≈
   12pp+ (b ≥ 7–8 in the c=0 special case; cf. EXP077 b=6 CI
   [+0.0338,+0.2015]). A +8pp prediction (b≈5, exact two-sided McNemar p =
   2·(1/2)^5 = 0.0625 > 0.05) lands Not supported per the adopted §G1b rule —
   no prediction the bar cannot see is shipped: the design is powered only for
   large net effects (L1 MDE = 10pp = 2·δ_min exactly, PARADIGM_AUDIT §B2
   boundary), with §G1b mapping the middle cells.
   Breaking points: (a) Tier-0 screen fails (median > 5) → dead (LOG-284
   fallback: ≤60-pass rebuild, not $0); median in (3,5] → INCONCLUSIVE-hold,
   no GPU (F4); (b) runner-up ΔM ≤ 0 (U < 0.05) while foil-mask (F2:
   benchmark-designated distractor) rescues → interference confirmed but not
   autonomously exploitable → PIVOT (a selector is needed; no further
   target-free erasure work); (c) C4 parity — (ΔM_C2 − ΔM_C4) with upper 95%
   CI < δ_min = 0.05 → effect is nonspecific masking, not interference →
   KILL (F1 pin); (d) runner-up null AND foil-mask null → KILL (F5 cell: no
   interference ceiling).

## 3. Design (skeleton)

- **Model:** pythia-410m (program continuity). **Benchmark:** the signed
  2-hop relational set; headroom gate 40–70% carried over.
- **Tier 0 (CPU):** latent-rank screen per §2. Archive-feasibility is settled:
  LOG-284 returned NEGATIVE (the EXP065/066/077 archives lack per-item frozen
  logits). Licensed fallback: ≤60 forward-pass frozen-logit rebuild on
  pythia-410m (~3s on 2×T4), sequenced piggyback on the K2→EXP083→EXP084 queue
  or standalone per CEO/Lead.
- **Population (F9 — pinned):** the N=60 GPU population is the FULL headroom
  set (baseline 40–70% correct per the carried-over gate), not failed-items-
  only — the honest test of a would-be method; a method that works only on
  pre-selected failures is not a method. Corruptions are counted:
  ΔM_arm = (rescues − corruptions)/60; corruptions = baseline-correct items
  (masking the true top-1 on a correct item always corrupts under single-
  answer MC with the deterministic F8 tie-break). McNemar: b = rescues,
  c = corruptions (both structurally nonzero); exact two-sided McNemar
  retained.
- **Scoring mechanics (F8 — load-bearing definitions):**
  - k = number of options per item, read from the benchmark specification and
    recorded verbatim in the formal pre-reg before signing (not verifiable
    from repo artifacts in this wave; Law #2 — no value invented here).
  - Null rank law: under uniform random ranking, rank ∼ Uniform{1..k},
    median = (k+1)/2. The Tier-0 bars are licensed only if k ≥ 6: the kill bar
    "median > 5" is unreachable for k ≤ 5 (max median is k), and the
    "median ≤ 3" prediction beats the null only for k > 5. If the benchmark's
    k < 6, the screen must be re-registered with k-relative bars before Law #14
    sign — no silent shipping.
  - rank(i) = 1 + #{j : s_j > s_i}, where s_i is the frozen logit of option i's
    representative token (benchmark's option→token mapping; multi-token options
    → first token of the option label; deterministic tie-break by lower option
    index; deviations loudly logged).
  - **Option-position audit mechanics:** measure the contingency table
    (correct-option position × C2 rescue outcome) over the 60 items; test the
    correct-position distribution against uniform (exact test). FAIL threshold:
    p ≤ 0.05 position-artifact, or the correct option systematically at
    position 2 for non-causal reasons. On FAIL: the unstratified C2 CONTINUE is
    blocked — the primary analysis is position-stratified, and no CONTINUE
    licenses on the unstratified number.
- **Arms (GPU, only if Tier 0 passes):**
  - C1 unintervened (baseline argmax accuracy);
  - C2 runner-up decode (mask top-1 option, argmax of remainder) — primary;
  - C3 top-2-suppressed decode (mask top-2) — measurement-only arm (no verdict
    rows; no Supported-licensing power per the F5 hierarchy): records whether
    rescue extends beyond rank-2, profiling the rank-2-concentration reading of
    a C2 win;
  - C4 random-mask (mask one uniform-random option *including* the top-1,
    then argmax of remainder) — discriminant: kills the "any masking helps"
    reading. (F1: the as-drafted "random non-argmax" version was vacuous —
    masking a non-argmax option leaves the argmax unchanged, so ΔM_C4 ≡ 0 by
    construction. Fixed here.) Interference-reading prediction: E[ΔM_C4] ≈
    ΔM_C2/k. Kill rule pinned in Statistics;
  - C5 output bridge — rescue control (LOG-204: positive-control status
    REVOKED; demotion carried — the CEO revisit has not happened; K1/LOG-213
    exonerated tilt but the LOG-232 brief is not accepted). Its rescue licenses
    nothing beyond readout steerability (already Supported); its failure →
    INVALID apparatus, not a mechanism verdict;
  - C6 B_wrong — negative control; construction recorded per Law #7 provenance
    discipline (LOG-177): the exact B_wrong construction (source experiment,
    layer, pooling, normalization) is pinned in the formal pre-reg — a control
    without provenance is not a control. Falsifying reading: B_wrong rescue
    parity with an injected arm → nonspecific-injection reading for injected
    arms. Bounding note (explicit): C2/C3/C4 are pure masking rules involving
    no injection at all, so C6 cannot bear on their mechanism reading — its
    relevance is bounded to the bridge-arm (C5) nonspecificity context;
  - C7 foil-mask (label-informed: mask the benchmark-designated distractor
    option — the foil defined label-side, independent of the frozen ranking)
    — ceiling arm only, never presented as a method (Law #7). Degenerate case
    stated: on items where top-1 = designated foil, C7 ≡ C2 on that item
    (identical masking). C7 analysis is stratified by (top-1 = designated-foil)
    vs (top-1 ≠ designated-foil). The PIVOT row is only meaningful under this
    independent foil definition (F2).
- **Endpoints:** primary ΔM per arm vs C1, exact McNemar two-sided, δ_min=0.05,
  verdicts per the five permitted categories only. Secondary: full rank-profile
  of the correct option on failed items (rank histogram — the screen's own
  measurement, publishable either way).
- **Statistics:** N=60 → L1 MDE 10.0pp at c=0 (PARADIGM_AUDIT §B2; c=0 is the
  reference case — under the F9 full-set reading c = corruptions > 0
  structurally, so the operating bar is the paired CI, not the c=0 MDE).
  **Hierarchical testing (F5):** C2 is the primary arm at α=0.05 — the only
  arm whose win can license Supported for the rescue claim. C3–C7 carry no
  Supported-licensing power (discriminant / ceiling / apparatus roles declared
  in the protocol, F6). A CONTINUE requires LCI > δ_min = 0.05 on C2 vs C1
  (paired exact). **C4 parity kill rule (F1):** paired exact McNemar C2 vs C4;
  parity, i.e. (ΔM_C2 − ΔM_C4) with upper 95% CI < δ_min = 0.05 → KILL
  (nonspecific masking, not interference). **Sub-threshold mapping (§G1b,
  adopted):** CI strictly inside (0,δ_min) or (−δ_min,0) → Not supported (KILL
  the rescue claim); crossing-zero with U ≥ δ_min → Inconclusive (held, never
  culled); exact boundary → hold, never licenses (LOG-285 precedent).
  **Missing cell added:** runner-up null AND foil-mask null → KILL (no
  interference ceiling; the selection-failure family closes).
- **Pre-registered confounds:** (i) option-position bias — the benchmark's
  option order must be checked for top-1 position artifacts before C2 is
  interpretable (mechanics pinned in Scoring mechanics, F8: contingency table,
  exact test, p ≤ 0.05 fail threshold, stratification-or-block consequence);
  (ii) if the correct option is systematically the *second*
  listed option for non-causal reasons, C2's win is invalid — stratify by
  correct-option position.

## 4. Cost

Tier 0: ≤60 forward passes (≈3s on 2×T4; the $0-from-archives route is closed
per LOG-284 NEGATIVE). GPU phase: 60 items × 7 arms ≈ 420 passes ≈ <1 min T4
[ESTIMATE from 22 fwd/s]. Total well under 0.01 T4-h. Cheapest GPU candidate
the program has proposed.

## 5. Novelty (honest)

N1. Adjacent: contrastive decoding (Li et al. 2023 — model-contrast, different
object; UNVERIFIED details), DoLa (layer-contrast, different). No verified
record in the program's audit tests rank-suppression as a repair for
relational-reasoning failures with decision endpoints. If the mechanism
verifies (C2 wins, C4 doesn't, rank profile concentrates at 2–3), the
*interference taxonomy* is the program's candidate N2-adjacent contribution —
not claimed here.

## 6. Relation to the boundary

- Routes around the static-additive null: the operation is subtractive and
  readout-side; it does not inject any hidden-state direction.
- Law #7-clean as a *method*: every input is the model's own frozen output.
  A CONTINUE would be the first autonomous (label-free-at-test) rescue
  primitive in the program.
- P1 bound: not applicable (no feedback loop; single-pass decode rule).
- Steelman: "you're just re-reading the model's second guess — that's
  measurement, not mechanism." Answer: the rank profile + C4 discriminant +
  C7 ceiling separate measurement (where the answer sits) from mechanism
  (suppression repairs decisions). If C2 wins only where rank=2 was already
  the argmax-adjacent choice for positional reasons, the confound
  stratification (§3) catches it. (F1/F2-adjacent point, named explicitly: if
  Tier-0 passes via rank-2 concentration, C2's rescue is partly algebraic —
  the fixed C4, the defined C7, and the position stratification are what keep
  this a mechanism test rather than a re-measurement.)

## 7. Sequencing

- After: Tier-0 logit rebuild (archive-feasibility already returned NEGATIVE,
  LOG-284 — the rebuild is the licensed plan; sequenced piggyback on
  K2→EXP083→EXP084 or standalone per CEO/Lead).
- Before: any I1-transplant GPU work. **"I2-resistant" defined (F7):**
  correct-option frozen rank > 2 AND C2 non-rescue — both pre-registered
  measurements from I2's own runs. If I2 CONTINUEs, I1's population =
  I2-resistant items, and I1's headroom gate (40–70%) plus N=60/MDE sizing are
  re-verified on the shrunk population (re-register with new N/MDE if it
  shrinks below 60). If I2 KILLs, I1's population is unchanged.
  Pre-registered-in-advance adaptive sequencing: the rule is fixed before
  outcomes are known — that is what makes the dependency auditable against
  cherry-picking. Carry this rule into I1's protocol at I1 pre-reg.
- Law #14 review required before any GPU (this skeleton is pre-review).

## 8. Open items for the formal pre-reg

- Exact headroom item list (reuse EXP077's 60 or rebuild? — recommend reuse
  with the fixed indices 0–23 convention per LOG-271/D1 precedent, loudly
  logged).
- Archive-feasibility outcome (logits present? top-k depth?).
- Option-order audit results.
- ~~Formalize the C4 discriminant's decision rule (paired McNemar C2 vs C4,
  or non-inferiority margin?)~~ — DISCHARGED by F1 (paired exact McNemar C2
  vs C4; parity kill rule pinned in §3 Statistics).
- ~~k pinned from the benchmark spec + k-relative bar check (F8 licensing
  condition: Tier-0 bars licensed only if k ≥ 6; required before Law #14
  sign).~~ — CLOSED by LOG-313 (§9.2/§9.5): **k = 2 pinned** from the
  benchmark specification (seven convergent in-repo sources: EXP066 §3.1 foil
  positioning "A or C"/"C or A"; EXP059 query format; EXP083 pilot prompt;
  K1 target_token/foil_token per item; LOG-300 binary-channel assumption
  artifact-verified; C-A "argmax over the two named options"; this draft's
  own singular-foil C7). The F8 license (k ≥ 6) FAILS. The bar check closes
  NEGATIVELY: at k = 2 the Tier-0 pass bar is vacuous (type-I = 1.0 — always
  fires, even under the null) and the kill bar is unreachable (power = 0) —
  no k-relative re-registration can repair the screen, because on failed
  items rank(correct) ≡ 2 by construction (the only alternative). This is a
  DESIGN DEFECT (§9.7), reported — not silently redesigned. The skeleton
  cannot sign as designed; CEO decision required.
- B_wrong construction provenance record (LOG-177) in the formal pre-reg.
- ~~Founder-ordered formal treatment (LOG-296 §"What the repair wave must
  deliver"): suppression operator (masking mechanics at logit/token level),
  rank(i), the foil, "I2-resistant"; winner-take-all interference model
  formalized ([CONJECTURE] → quantitative Tier-0 histogram shape, C2 recovery
  fraction, E[ΔM_C4] ≈ ΔM_C2/k); every bar derived from the null (F8), every
  prediction checked against its decision threshold (F3) — modeled on the I1
  formalization (LOG-287). Required before any SIGN.~~ — CLOSED by LOG-313:
  delivered as §9 below (definitions → suppression operator → winner-take-all
  model → every bar derived from the null with the k = 2 instantiation →
  breaking points → honesty section). The treatment's verdict is negative:
  the formalization proves the design vacuous at k = 2 (§9.7).

## 9. Formal treatment (Founder's order — LOG-313, 2026-09-24)

*Epistemic standard: [FACT] / [DEFINITION] / [CONJECTURE] / [PROPOSITION] /
[ASSUMPTION] per AGENTS.md §5. No numbers invented (Law #2): every
quantitative value below is either read from a cited in-repo source or
derived in writing. $0 spent, CPU only, Δθ = 0 throughout (Law #6).*

### 9.1 Definitions [DEFINITION]

- **M**: frozen autoregressive transformer (pythia-410m), parameters θ fixed.
- **Item x**: one 2-hop/3-hop relational query from the N = 60
  Planetary/Elemental suite (EXP065's suite, reused per EXP077 §5, F9).
- **Option set** O(x) = {t(x), f(x)}: the *target* (correct answer) and the
  *benchmark-designated foil* (distractor), the two entities named in the
  question surface form ("Who is higher in rank, A or C?"). **k := |O(x)|.**
- **Frozen scores** s(x) = (s_t, s_f) ∈ ℝ²: the model's frozen logits for the
  two option tokens at the answer position (option→token mapping per F8:
  tokenizer.encode(" " + label)[0], first token of the option label).
- **Decision rule** d(s) := argmax_{i ∈ O} s_i with deterministic tie-break τ
  (lower option index wins). Baseline correctness = 1[d(s) = t].
- **rank(i)** := 1 + #{j ∈ O : s_j > s_i ∨ (s_j = s_i ∧ idx_j < idx_i)} — the
  tie-break folded in, so ranks are a permutation of {1, …, k}.
- **Foil**: the benchmark-designated distractor, defined label-side,
  independent of the frozen ranking (F2). On this benchmark the foil is the
  wrong option on every item.
- **I2-resistant** (carried, F7): rank(correct) > 2 ∧ C2 non-rescue.

### 9.2 The k pin [FACT — read from the benchmark specification]

**k = 2.** Seven convergent in-repo sources, no value invented:

1. EXP066 spec §3.1 (the suite's instance structure, "identically ported
   from EXP065"): *"Foil positioning: Exactly 50% target-first (`A or C`)
   and 50% target-second (`C or A`)"* — each question names exactly two
   entities: target and foil.
2. EXP059 spec: the query surface form is *"Who is higher, A or C?"* →
   Correct: **A** — a binary forced choice.
3. EXP083 pilot (`test_exp083.py`): the prompt verbatim —
   `"Premise: A outranks B. B outranks C. Question: Who is higher in rank,
   A or C? Answer:"`.
4. K1 executor (`K1_execute_LOG213_2026-09-23.py`): every reconstructed
   item carries exactly `(target_token, foil_token)`; the archived decision
   variable is the t−f margin.
5. LOG-300 (independent Law #14, artifact-verified): the binary-channel
   assumption — *"the decision is determined by sign(ℓ_t − ℓ_f), i.e.
   argmax ∈ {t, f}, no third-token flips"* — verified against the K1/EXP066
   artifacts.
6. C-A spec: *"the argmax over the two named options."*
7. This draft's own C7 (F2): *"mask the benchmark-designated distractor
   option"* — one singular foil per item.

The F8 licensing condition ("Tier-0 bars licensed only if k ≥ 6") therefore
**fails**. §9.5 derives exactly what follows.

### 9.3 The suppression operator [DEFINITION]

For mask set M ⊆ O(x), the **suppression operator** S_M acts on the frozen
score vector:

> (S_M s)_i = −∞ if i ∈ M, else s_i.

Domain: ℝ^k × P(O(x)) → ℝ^k. Action: logit-level erasure at the answer
position (equivalently, restriction of the argmax to O \ M). Parameters: the
mask-set *selection rule* per arm —

- C2: M = {m₁(s)}, m₁ = argmax (the runner-up decode);
- C3: M = {m₁, m₂} (top-2 suppressed);
- C4: M = {m}, m ∼ Uniform(O(x)) (one uniform-random option *including*
  the top-1, F1);
- C7: M = {foil} (label-informed ceiling).

S_M is a **pure readout map**: it touches no hidden state, no weight, no
normalization statistic. Its only input besides the mask rule is the model's
own frozen output s — Law-#7-clean as a *method* (C7 excepted by declared
label-informed status). The C4 RNG seed is a required pin at any signing;
noted here, unpinned in this skeleton.

### 9.4 The winner-take-all interference model [CONJECTURE]

> **Interference conjecture.** The decision is d(s) = argmax (winner-take-
> all over the option scores). On failed items the correct option sits at
> low latent rank — rank(correct) ∈ {2, 3} — while a competitor captures
> the argmax: a *selection* failure (the answer was present but suppressed),
> not a *knowledge* failure. Suppressing the top-1 competitor (S_{m₁})
> promotes the runner-up to argmax and repairs the decision.

Quantitative predictions (general k):

- **P1 (Tier-0 histogram).** On failed headroom items, the rank histogram
  of the correct option concentrates at 2–3: median ≤ 3.
- **P2 (C2 recovery).** C2 rescues exactly the failed items with
  rank(correct) = 2 (masking m₁ promotes the runner-up). With f2 = # such
  items and N_corr = # baseline-correct items (corruptions: masking the
  true top-1 on a correct item always corrupts under single-answer MC with
  the deterministic τ tie-break), predicted **ΔM_C2 = (f2 − N_corr)/60**.
- **P3 (C4 discriminant).** Per item, C4 masks the true competitor m₁ with
  probability 1/k (then C4 ≡ C2 on that item) and a non-argmax option with
  probability (k−1)/k (then the argmax is unchanged, C4 ≡ C1). Hence
  **E[ΔM_C4] = ΔM_C2/k** [PROPOSITION, by linearity of expectation over the
  per-item mixture].

### 9.5 Every bar derived from the null

**Null rank law [FACT under the no-structure null].** If the correct
option's rank carries no interference structure, rank ∼ Uniform{1, …, k}
i.i.d. over items, median = (k+1)/2.

**Tier-0 bars (derived).** The pass bar (median ≤ 3) must beat the null
median; the kill bar (median > 5) must be reachable (max median = k). Both
conditions hold iff k ≥ 6 — the F8 license, derived, not stipulated.

**The bar check at k = 2 (type-I / type-II):**

| Bar | Behavior at k = 2 | Type-I | Power | Verdict |
|---|---|---|---|---|
| Pass: median ≤ 3 | max achievable median is 2 < 3 → fires on *every* dataset, including the null | **1.00** | 1.00 (fires under null too) | **Vacuous** — discriminates nothing |
| Hold: median ∈ (3,5] | empty — unreachable | — | — | Dead cell |
| Kill: median > 5 | max median 2 → never fires | 0.00 | **0.00** | **Unreachable** — the gate never closes |

The F8 license fails, and — deeper than the draft's "re-register k-relative
bars" fallback — **no** k-relative re-registration can repair the screen at
k = 2: on failed items rank(correct) ≡ 2 *by construction* (the only
alternative to the winner), modulo exact-top ties resolved by τ. The
screen's own population has a degenerate rank distribution; any bar is
either vacuous or unreachable. The Tier-0 "pass" is algebraically
guaranteed — a gate that always opens is not a gate (Law #15).

**Primary endpoint bar (derived).** Exact two-sided McNemar on paired
correct/incorrect outcomes, H0: rescues and corruptions equiprobable on
discordant pairs (no systematic decision shift). CONTINUE iff the lower
exact 95% CI bound LCI(ΔM_C2) > δ_min = 0.05 (program minimum-effect
convention, PARADIGM_AUDIT). Reference calibrations: at c = 0, LCI > 0.05
needs b ≥ 7 (b = 6 → CI [+0.0338, +0.2015], the EXP077 anchor — cited from
this draft, not recomputed); exact two-sided p for b = 5, c = 0 is
2·(1/2)^5 = 0.0625 > 0.05 (F3).

**At k = 2 the primary endpoint is algebraic [PROPOSITION].** On a failed
item the top-1 is the foil (strictly, or by τ on exact ties), so C2's mask
removes the foil and the remainder is {t} → rescue. On a correct item the
top-1 is the target, so C2's mask removes the target and the remainder is
{f} → corruption. Hence **b = N_f, c = N_c exactly**, and
**ΔM_C2 = (N_f − N_c)/60 = 2·(N_f/60) − 1** — fully determined by baseline
accuracy, with zero mechanism content. Worked example (EXP077's baseline,
34/60 correct, 26 failed — LOG-300-verified): ΔM_C2 = −8/60 = −0.1333,
exact two-sided McNemar p = 0.3663 → Not supported, never CONTINUE. Under
the carried headroom gate (40–70%), N_f ∈ [18, 36] → ΔM_C2 ∈ [−0.4, +0.2];
the CONTINUE bar (LCI > 0.05) can fire only at baselines *below* the
headroom gate — a "win" caused by the baseline, i.e. baseline accuracy
re-measured and laundered as a mechanism result (the steelman's
re-measurement warning, §6, in its strongest form).

**C4 parity kill rule (derived).** Paired exact McNemar C2 vs C4 on the same
60 items; parity — (ΔM_C2 − ΔM_C4) with upper 95% CI < δ_min — → KILL
(nonspecific masking, not interference). At k = 2, per-item C4 is a
Bernoulli(1/2) mixture of C2 and C1 (masks the top-1 w.p. 1/2), so
**Δ̂ = ΔM_C2 − ΔM_C4 = ΔM_C2/2 = ΔM_C2/k** algebraically (P3 holds!) — but
the *discriminant reading* is dead: C4 is literally C2 half the time, not
an independent "any masking helps" probe. The kill rule becomes a bar on
half the algebraic C2 effect — it tests arithmetic, not mechanism.

**Validity bars (derived from their nulls).**
- *Headroom gate 40–70%* (carried): binomial rationale — 18–36 failed items
  are needed for the rescue/corruption counts to be measurable; outside the
  window the (b, c) cells are degenerate. Validity, not mechanism.
- *C5 rescue-control → INVALID*: if the readout cannot be steered at all,
  the apparatus (logit read/write path) is broken — no mechanism verdict
  may be drawn. (LOG-204 demotion carried: licenses nothing beyond readout
  steerability.)
- *Option-position audit* (F8): exact test of correct-option position × C2
  rescue, H0 = position independent of outcome; p ≤ 0.05 → stratify-or-
  block. At k = 2 the position variable is binary (target-first "A or C"
  vs target-second "C or A") and the benchmark *constructs* it at exactly
  50/50 — the audit reduces to verifying the construction balance, and the
  confound it was built to catch (positional artifact masquerading as
  rank-2 concentration) is indistinguishable from the k = 2 tautology.

**Arm-level degeneracies at k = 2 (derived).**
- *C3*: M = {m₁, m₂} = O(x) → argmax over ∅ is **undefined**. The arm is
  degenerate and must be struck (it was measurement-only; striking is
  clean — reported here, design text in §3 untouched per Law #4).
- *C7*: M = {foil} removes the wrong option on all 60 items → **100%
  accuracy by construction**. The PIVOT row's distinguishing condition
  ("runner-up ΔM ≤ 0 (U < 0.05) *while foil-mask rescues*") is then
  algebraically true iff N_f > 0 — the "interference confirmed but not
  autonomously exploitable" reading is vacuous: masking the known-wrong
  answer in a 2-option test is not evidence of interference.
- *§7 sequencing*: "I2-resistant" = rank > 2 ∧ C2 non-rescue — rank > 2 is
  impossible at k = 2 → the I2-resistant set is **empty by construction**,
  and the I1-population rule fires vacuously.

**§G1b mapping** (adopted verbatim in §3, not re-derived): CI strictly
inside (0, δ_min) or (−δ_min, 0) → Not supported; crossing-zero with
U ≥ δ_min → Inconclusive (held, never culled); exact boundary → hold.

### 9.6 Breaking points of this formalization

- **B-a.** If the k = 2 pin is overturned (a benchmark source showing a
  genuinely scored k ≥ 3 option set), every §9.5 instantiation re-derives;
  the general-k treatment (§9.1–§9.4) stands as written.
- **B-b.** Exact-top ties (s_t = s_f): "top-1" is fixed by the same τ the
  baseline decision uses — the b = N_f / c = N_c identities hold with τ
  folded in (§9.1 rank definition). Second-order; noted, not load-bearing.
- **B-c.** The §9.7 defect verdict stands unless the design is re-registered
  under a new experiment number — corrections to this design are not made
  here (Law #4; design changes get new numbers).

### 9.7 Honesty: what this formalization buys, and what it kills

**It buys:** (i) k pinned to 2 from seven primary in-repo sources — the
F8 license fails on evidence, not suspicion; (ii) the suppression operator
as a pure readout map (Law-#7 status made exact); (iii) the winner-take-all
model with derived predictions P1–P3 (E[ΔM_C4] = ΔM_C2/k proved); (iv) the
exact locus of vacuity for every bar and arm at k = 2 — nothing hand-waved.

**It kills:** the Tier-0 screen as designed (a gate that always opens and
never closes); C3 (undefined at k = 2); C7's PIVOT semantics (algebraic
ceiling, not a ceiling measurement); the interference reading at k = 2
(the conjecture's "predictions" coincide with the benchmark's definitions —
at k = 2 the model is *unfalsifiable*, and an unfalsifiable mechanism
conjecture is not a mechanism); and the §7 I1-sequencing rule (empty
I2-resistant set).

**Design-defect report (Law #14-relevant, not a redesign).** At k = 2,
EXP085's GPU phase measures baseline accuracy through an algebraic
relabeling: ΔM_C2 ≡ 2·(N_f/60) − 1. No bar re-registration repairs this —
the defect is in the arms, not the bars. The skeleton **cannot sign as
designed**. CEO decision required: (a) KILL EXP085 as designed (the
interference-repair family closes on this benchmark — the honest
falsification-first outcome), or (b) re-register under a **new experiment
number** against a genuinely multi-option benchmark (k ≥ 6 per the F8
license) — noting that re-scoring this suite over 5 vocabulary entities
would change the benchmark construct itself (the foil-positioning control
and the t−f decision variable are defined for the binary format), so it is
a different experiment, not a repair. Either way, no GPU is licensed by
this treatment, and the Tier-0 rebuild must not run under this number.

*End of §9. Formal treatment complete: suppression operator formalized,
winner-take-all model formalized, every bar derived from the null, every
prediction checked against its decision threshold — and the check returns a
design defect, reported honestly per Law #14.*

---
*Skeleton drafted LOG-283, 2026-09-24. F1–F9 repair wave applied LOG-305,
2026-09-24. LOG-307 Law #14 re-verification SIGN (two signing-gated items).
LOG-313 signing-prep: k = 2 pinned from the benchmark spec; bar check
closes NEGATIVELY (F8 license fails; Tier-0 screen vacuous at k = 2);
Founder-ordered formal treatment delivered as §9. The treatment reveals a
fatal design defect at k = 2 — reported in §9.7, design text untouched per
Law #4. No numbers invented. No signed protocol touched. Next: independent
Law #14 adjudication of the k = 2 finding, then the CEO's decision on the
design's fate (kill as designed, or re-register under a new number).*
