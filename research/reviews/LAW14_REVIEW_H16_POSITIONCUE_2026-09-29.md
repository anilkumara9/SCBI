# Independent Law #14 Review — H16 Pre-registration (PTTSC-SUFFIX → POSITIONCUE)

**Lane:** LOG-4651 (pre-assigned). **Reviewer:** independent Law #14 lane. $0 CPU.
**Artifact under review:** `~/workspace/SCBI/research/prereg/EXP_PREREG_H16_POSITIONCUE_2026-09-29.md` (exact file, read in full).
**Scope (Law #14 binding):** mathematical soundness and internal consistency. Not style.
**Reviewer stance:** fresh eyes; did not draft the protocol. Adversarial: attempted to falsify the bars, the breaking point, and the construction specification.

**Verdict: SIGN-WITH-FIXES** — four fixes, all launch-gating (the protocol cannot be executed unambiguously without them). No fix alters the verdict bars, the hypothesis, or the breaking-point structure. No REJECT-level structural defect found: the bars partition the outcome space completely, the binomial license is exact, the breaking point is conjunctive and safe-failing, and the hypothesis is testable.

---

## 1. Binomial license — recomputed exactly (defect class (a) compliance)

All §4 p-value claims recomputed from scratch (one-sided binomial, p=0.5):

| Claim in draft | Recomputed | Status |
|---|---|---|
| P(X≥20\|30,0.5) = 0.0494 | 0.0493686 | ✓ |
| P(X≥19\|30,0.5) = 0.1002 | 0.1002442 | ✓ |
| P(X≥18\|30,0.5) = 0.1808 | 0.1807973 | ✓ |
| P(X≥37\|60,0.5) ≈ 0.047 (G-C1/position gate) | 0.0462305 | ✓ |

Critical value 20/30 is correct: P(X≥20)=0.0494 ≤ 0.05 < P(X≥19)=0.1002. The directional p-inequalities are correct: scores ≥20/30 have p ≤ 0.0494; scores ≤18/30 have p ≥ 0.1808. The §4 values are pre-registered bar licenses (descriptive), not results — defect class (a) is complied with: §3.6 explicitly requires the executor to print the exact one-sided p-value, never handwritten.

## 2. The six bars — mathematically coherent, complete partition

- CONTINUE: ≥20/30 **AND** G<0.30.
- KILL: ≤18/30 **OR** G≥0.30 (precedence explicit in §2 and §4: "takes precedence over any overall score").
- HELD: 19/30 with G<0.30.
- The residual case (19/30 with G≥0.30) falls under KILL via the OR clause — unambiguous.
- Partition is complete and disjoint. The "≥5-item gap" gloss for G≥0.30 is arithmetically correct (0.30×15=4.5 → ≥5 items at N_F=N_T=15).
- §5 decision tree matches §4 exactly, branch for branch. No other branches exist (Law #4).

## 3. G definition — consistent with the H15 discipline

G = acc(flipped=False) − acc(flipped=True), N_F=N_T=15, stated identically in §2, §3.6, and §4. Cross-checked against EXP120's report: G = acc(F)−acc(T) with F=flipped=False (0.7333), T=flipped=True (0.9333), G=−0.2000. The sign convention (original-minus-flipped) is stated and consistent; 'flipped' (True) plays the role of EXP120's 'T'. ✓

## 4. Position-scramble gate — constructively verifiable, conjunctive breaking point

- The gate (pure-position rule P ≤ 36/60) is string-level, no model contact (§3.2: "quantitative, string-level, no model contact") — verifiable by the constructor **before** any head is trained. ✓
- §0 makes the breaking point conjunctive: "ALL of §3.2's design assertions and quantitative gates must pass. A single miss voids the apparatus." Any miss → construction-fate RUN-INVALID, hypothesis UNTESTED, no experiment number minted. ✓
- The 36/60 bar is the correct α=0.05 one-sided critical value (P(X≥37|60,0.5)=0.0462; scores ≥37 are significant, so ≤36 is "not above chance"). Same bar correctly applied to G-C1. ✓

## 5. The six binding defect classes — all addressed

- (a) Executor-computed p-values: §3.6 explicit. ✓
- (b) Raw records hash-pinned before verdict: §3.7 artifact-existence gate, correctly adapted ("zero generation in H16, so the gate pins raw embeddings + head weights instead of raw generations"); §9 item 5. ✓
- (c) Label semantics cite builder docstring + independent pin, never truncated comment: §3.2 item 4 and §3.4 explicit (LOG-4625/4626 FIX-1 discipline). ✓
- (d) No EXP117 recitation reuse: §9 item 6, explicitly N/A (zero generation). ✓
- (e) [-3:] identity pin: §6 item 4, explicitly N/A (no logit channel). ✓
- (f) Single-token assertion: §6 item 5, explicitly N/A (embedding apparatus; H18 binds only logit-channel benches). ✓

## 6. H17 — genuinely absent

§6 item 1 explicitly bars per-layer secondaries ("H17 through the back door — explicitly barred"); §8 item 7; §10 boundary ("H17 stays rejected... no layer-resolved bars, no contingent per-layer secondary"). EXP111 §7 layer numbers enter only as mathematical-license context (§1.1) and license no verdict. No layer-resolved contingent bars smuggled in. ✓

## 7. Honest license of a CONTINUE — stated and consistent

§7(b): "a CONTINUE licenses only 'identity readout survives position decorrelation' — decodability, **not steering or capability**." §8 items 1–2: correlation at one layer, no capability claim, "downstream causal tests (steering, decision-flip) are required before any capability statement. The capability scoreboard stays at zero positive signals for autonomous steering." Consistent with the program's honest headline. ✓

---

## Fixes required (all launch-gating)

### FIX-1 (launch-gating): §3.5 per-cell count shorthand contradicts the explicit mapping

**Defect:** "the test counts per cell in sorted key order are deterministically **8/8/7/7** — ("target-first", original): 8, ("target-first", flipped): 7, ("target-last", original): 7, ("target-last", flipped): 8".

With the pinned key `f"{phrasing}_{flipped}"` (flipped ∈ {False, True}), sorted key order is target-first_False, target-first_True, target-last_False, target-last_True — i.e. **8, 7, 7, 8**, not 8/8/7/7. The explicit mapping is correct (it matches EXP120's observed "pinned 8/7/7/8 encoding": A-first_False 8, A-first_True 7, C-first_False 7, C-first_True 8). The "8/8/7/7" shorthand is a false factual claim carried over from the H5 pre-reg §3.3 (same typo there). N_F=15 (8+7) and N_T=15 (7+8) are unaffected.

**Why launch-gating:** the "deterministically 8/8/7/7" is a pinned assertion the execution lane must satisfy; as written it is unsatisfiable (the true sklearn 1.9.1 + seed 20260929 output is 8/7/7/8 per the mapping). An execution lane asserting the shorthand would spuriously fail determinism.

**Fix:** change the shorthand to "8/7/7/8" to match the explicit per-cell mapping. Do not touch the mapping. (Note for the program: the same "8/8/7/7" typo exists in the signed H5 pre-reg §3.3 — that signed file is not to be edited; this fix applies only to the H16 draft's statement.)

### FIX-2 (launch-gating): disambiguate "phrasing" (original group) from final sentence position

**Defect:** §3.2 item 2 defines `phrasing` ∈ {"target-first", "target-last"} (30/30) as "the target's sentence position in the premise", but in the same item requires the flip to "re-anchor the target's sentence position per the builder's own documented rule" — under the cited EXP107 discipline the flip moves the target subject↔object (EXP107 pre-reg: "the flip also moves the target from sentence-subject to sentence-object — registered honest limitation"). For flipped items, "phrasing" (original group) and final sentence position therefore differ, and the parenthetical "(the target's sentence position in the premise)" is false for half the bench. The constructor cannot unambiguously satisfy "phrasing 30/30" and the position assertions simultaneously.

**Fix:** state explicitly that "phrasing" denotes the **original authoring group** (30/30); the flip moves the target's sentence position (re-anchors it, EXP107-style); **final position = phrasing XOR flipped**. Correct the parenthetical accordingly. Per-item records must carry both `phrasing` (original group, the stratification key) and final position (used by the position-scramble gate).

### FIX-3 (launch-gating): pin final-position × label balance so the "by construction" claim is sound

**Defect:** §3.2 item 4 ("Within each label class, the target's sentence position is balanced: target-first 15, target-last 15") and the position-scramble gate ("Position is balanced within each label class by construction, so P scores 30/60 by construction") are only valid for **final** positions. Under FIX-2's reading (flip moves position), final-position × label 15/15 does **not** follow from the currently pinned assertions (original-phrasing 30/30 + 15 flips per group by index parity). It additionally requires the flip×label pattern to be identical across the two phrasing groups — otherwise the "by construction 30/60" justification is unsound (the quantitative P ≤ 36/60 gate would still catch violations, but the specification's entailment claim would be false).

**Fix:** state explicitly that item 4's balance refers to **final** sentence positions, and add the construction constraint that the flip×label pattern is identical across phrasing groups (equivalently: the constructor arranges label order within each phrasing group so that final positions are 15/15 within each label class). The quantitative position-scramble gate (P ≤ 36/60) then verifies, rather than rescues, the construction.

### FIX-4 (launch-gating): specify non-target tuple entities as mixed-domain

**Defect:** §3.2 pins D1/D2 and `tuple[0]` = A (y=1 iff A ∈ D1) but never specifies the domains of the non-target tuple entities B, C, [D]. If the constructor builds same-domain tuples (all-animals vs all-fruits), a premise-level domain detector — not a **target**-identity readout — would pass the bars, and a CONTINUE would not license §7(b)'s "the head extracts a domain-set property of the **target**". The hypothesis (§1: "a property of the **target entity's** identity") would then outrun the construction.

**Fix:** add one construction specification: B, C, [D] are drawn from **both** D1 and D2 (mixed-domain tuples), so that `tuple[0]`'s domain is the only domain cue predictive of y. (The position-vs-content discrimination holds either way; this fix is required for the "target" specificity the verdict interpretation claims.)

---

## What was checked and found sound (no fix)

- Six-bar partition, precedence, and binomial license (§2, §4, §5): sound.
- G definition, sign convention, denominators (§2, §3.6, §4): consistent with H15/EXP120.
- Conjunctive breaking point; apparatus-void → UNTESTED with no number minted (§0, §3.2): sound.
- Position-scramble and G-C1 gate bars (≤36/60) and their α=0.05 justification: correct.
- Backbone pin (LOG-331 hash before/after, §3.3), determinism pins, environment pins: consistent with the EXP120 discipline.
- Head spec pinned verbatim (no tuning, Law #7): `LogisticRegression(penalty='l2', C=1.0, solver='lbfgs', max_iter=1000, random_state=20260929)` matches EXP120's pinned head.
- Split: 30/30, disjointness asserted → RUN-INVALID on overlap; determinism re-fit pass → RUN-INVALID on mismatch: sound.
- Record-keeping artifact-existence gate before verdict (§3.7): sound (EXP119 lesson applied).
- Law #7 posture (§3.4, §3.8): test labels for final registered evaluation only; no test-informed selection: sound.
- Law #11 tagging (§1.1): hypothesis / observations / interpretation kept as separate layers; KILL reclassifies rather than erases (Law #8): sound.
- Explicit "not licensed" list (§2), H17 exclusion (§6.1, §8.7, §10), no-logit-channel / no-single-token N/A statements (§6.4–6.5, §9.6): sound.
- Cost/honesty (§7), no-claim list (§8), deviations list (§9), boundary + summit filter NO (§10): sound and consistent with the honest headline.

## Verdict restated

**SIGN-WITH-FIXES.** Four launch-gating fixes (FIX-1 through FIX-4 above). None changes the hypothesis, the six bars, the breaking-point structure, or any quantitative gate value. After fix-verification of this exact file, the protocol is launchable under a CEO decision and a minted experiment number.

**Reviewer:** LOG-4651 lane. Read-only on all signed artifacts; wrote only this review and the LOG-4651 log entry. No pushes, no commits, no credentials, no model contact.
