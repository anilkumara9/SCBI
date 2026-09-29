# Independent Law #14 Review — H23 Pre-registration (Within-Domain Decoy Dissection)

**Lane:** LOG-4686 (pre-assigned). **Reviewer:** independent Law #14 lane. $0 CPU.
**Artifact under review:** `~/workspace/SCBI/research/prereg/EXP_PREREG_H23_WITHINDOMAIN_2026-09-29.md` (exact file, read in full).
**Scope (Law #14 binding):** mathematical soundness and internal consistency. Not style.
**Reviewer stance:** fresh eyes; did not draft the protocol. Adversarial: attempted to falsify the bars, the bar-calibration argument, the label design, the breaking point, and the construction specification. Read-only on all signed artifacts; wrote only this review and the LOG-4686 log entry. No pushes, no commits, no credentials, no model contact.

**Verdict: SIGN — zero fixes.** The draft pre-applied all four H16 Law-#14 fix patterns, the binomial license recomputes exactly, the bars partition the outcome space completely, the breaking point is conjunctive and safe-failing, and the hypothesis is testable. No launch-gating or verdict-immaterial fixes found. No REJECT-level structural defect.

---

## 1. Registered bars — coherent, disjoint, exhaustive; binomial license recomputed exactly (defect class 1)

All cited binomial probabilities recomputed from scratch (pure `math.comb`, one-sided, p=0.5):

| Claim in draft | Recomputed | Status |
|---|---|---|
| P(X≥20\|30,0.5) = 0.0493686 (§4) | 0.0493686 | ✓ exact |
| P(X≥19\|30,0.5) = 0.1002442 (§4) | 0.1002442 | ✓ exact |
| P(X≥18\|30,0.5) = 0.1807973 (§4) | 0.1807973 | ✓ exact |
| P(X ≥ 37 \| 60, 0.5) = 0.0462305 (§3.2, G-C1 bar justification) | 0.0462305 | ✓ exact |

- CONTINUE: ≥20/30 **AND** G<0.30. KILL: ≤18/30 **OR** G≥0.30 (precedence explicit in §2, §4, §5). HELD: 19/30 with G<0.30.
- Residual case (19/30 with G≥0.30) falls under KILL via the OR clause — unambiguous. Partition complete and disjoint.
- §5 decision tree matches §4 branch for branch; no other branches exist (Law #4). The §2/§4/§5 statements of the bars are mutually consistent.
- The "≥5-item gap" gloss (0.30×15=4.5 → ≥5 items at N_F=N_T=15) is arithmetically correct.
- §3.6 requires the executor to print the exact one-sided p-value — defect class 1 complied.

## 2. Bar-calibration argument — sound

The draft bars H6's 42–57/60 honesty-logit bars from transfer ("wrong apparatus, wrong n") and binds the H5/H16 signed n=30 head bars. The reasoning is sound: H6's bars belong to an n=60 full-bench fidelity metric on a zero-generation logit readout; the head protocol's decision is on 30 held-out test items from a stratified 30/30 split. Different apparatus, different n — the non-transfer is a theorem of the bar structure, not a preference. The EXP122 bench-3 precedent (27/30, G=−0.0667) is the correct calibration, stated identically in the gate memo's adjudication. H14's McNemar bars are likewise correctly excluded. ✓

## 3. Label semantics — disclosure complete, independent pin sound (H16 §2 precedent)

- The §2 "Explicit disclosure (label-design choice)" states verbatim what carries (protocol: head spec, split seed, extraction site, construction discipline, gates, bars) and what does not (label definition). The verdict bars are stated as properties of the protocol **plus this specific label design** — the H16 disclosure pattern reproduced faithfully.
- Meaning-preserving construction: §3.2 item 2 pins the flip preserves ranking meaning and keeps `tuple[0]` = A highest-ranked; §3.4 requires the builder docstring to document (a) the meaning-preserving flip, (b) tuple[0]=A on all 60 items, (c) the label derivation rule y=1 iff tuple[0] ∈ S1.
- Independent Law-#7 pin: §3.2 item 4 requires the per-item assertion `y == (tuple[0] in S1)` independently from the item record — mechanical, separate from the prose, never a truncated inline comment (the LOG-4625/4626 FIX-1 discipline). ✓
- Target-specificity (H16 FIX-4 pattern, pre-applied): non-target tuple entities (B, C, D) are drawn from **all 14 animals** (including the neutral decoys), so tuple[0]'s subset membership is the only label-predictive cue — the correct within-domain analog of H16's mixed-domain fix. ✓

## 4. Within-domain audit and single-token assertion — executable, failure → construction-fate

- Single-domain audit (§3.2): per-item independent certification that every entity mention belongs to the 14-animal set; gate 0/60 premises with any out-of-domain entity name, audited with whole-word matching; any violation → contaminated → construction failure. Procedure pinned precisely enough for the construction lane. ✓
- Single-token assertion: 14/14 re-run on final sets at construction, tokenizer-only, real Pythia-410m tokenizer, `" "+E` encoding; "Any multi-token entity → construction restarted, not patched" — the restart-not-patch rule is explicit. Declared in §3.2, §6 item 5, and §9 item 4 as an **explicit design deviation** from the H16 lineage (which declared defect class (f) N/A) — declared, not smuggled. ✓
- ID namespace pins bench-4's `exp125_` prefix (the LOG-4679 lane's actual prefix) alongside `exp107_`, `expb2_`, `expb3_` — consistent with the canonical records. ✓

## 5. Position-scramble gate — H16 FIX-2/FIX-3 patterns pre-applied correctly

- `phrasing` denotes the **original authoring group** (30/30); the flip re-anchors the target's sentence position; **final position = phrasing XOR flipped**; per-item records carry both `phrasing` (stratification key) and final position — the H16 FIX-2 ambiguity is absent. ✓
- §3.2 item 4 pins the flip×label pattern identical across phrasing groups and requires the constructor to arrange label order within each phrasing group so final positions are 15/15 within each label class (target-first 15, target-last 15 per class) — the H16 FIX-3 soundness entailment is pinned, and the position-scramble gate (P ≤ 36/60) verifies rather than rescues. ✓
- G-C1 ≤ 36/60, G-C2 |Pearson(r3,r5)| ≤ 0.10 (against bench-3 builder records, Law-#13 fence declared — no bench-3 labels or embeddings enter), G-C3 byte-exact: coherent for the head apparatus and ported verbatim in structure from the H16 discipline. ✓
- The G-C1 bar (36/60) is the correct α=0.05 one-sided critical value: P(X≥37|60,0.5)=0.0462305, so ≥37 is "above chance" and ≤36 is not — applied identically to the position-scramble gate. ✓

## 6. Breaking point — conjunctive, complete, no number minted after partial failure

§0: "ALL of §3.2's design assertions and quantitative gates must pass. A single miss voids the apparatus." Any miss → construction-fate RUN-INVALID, hypothesis **UNTESTED** (not killed), no experiment number consumed beyond what the CEO assigns. The §5 tree admits no path to a metric after any partial failure: construction gates → RUN-INVALID; hash drift, npz/ids mismatch, train/test ID overlap, determinism re-fit mismatch, missing artifacts → RUN-INVALID before the metric stage. No gate mints a number after a partial failure. ✓

## 7. Head recipe — byte-identical to the H5/H16 pin

§3.5: `LogisticRegression(penalty='l2', C=1.0, solver='lbfgs', max_iter=1000, random_state=20260929)`; `train_test_split(test_size=0.5, seed 20260929, stratified by f"{phrasing}_{flipped}")`; L20 final-token extraction; torch==2.14.0+cpu / transformers==5.17.0 / numpy==2.5.3 / sklearn==1.9.1; no tuning (Law #7); ConvergenceWarning = reported defect, not a gate (carried from H16, §9 item 5); block-off discipline (a)–(d); Δθ=0 via LOG-331 before/after. Character-identical to H16 §3.3–§3.5. The only declared deviation (single-token hygiene) is explicit and justified. ✓

## 8. Split counts — 8/7/7/8 verified against sorted key order

Sorted keys `target-first_False, target-first_True, target-last_False, target-last_True` map to ("target-first", original)=8, ("target-first", flipped)=7, ("target-last", original)=7, ("target-last", flipped)=8 → shorthand **8/7/7/8** matches the explicit mapping exactly (the H16 FIX-1 "8/8/7/7" typo is absent — pre-avoided at drafting). N_F = 8+7 = 15, N_T = 7+8 = 15. Train/test n=30/30, disjointness asserted → RUN-INVALID on overlap. Labels are balanced within cells by the identical flip×label pattern (item 4), so stratification introduces no label confound. ✓

## 9. Binding defect classes — all addressed

- (a) executor-computed p-values: §3.6 explicit. ✓
- (b) raw records hash-pinned before verdict: §3.7 artifact-existence gate, correctly adapted (zero generation → pins embeddings + head weights); §9 item 6. ✓
- (c) label semantics cite builder docstring + independent pin: §2 disclosure, §3.2 item 4, §3.4. ✓
- (d) no EXP117 recitation reuse: §6 item 7, explicitly N/A (zero generation). ✓
- (e) [-3:] identity pin: §6 item 4, explicitly N/A (no logit channel) — matches gate memo H16 §6 item 4. ✓
- (f) single-token assertion: §6 item 5, explicitly ACTIVE with the restart-not-patch rule — declared design deviation. ✓
- (g) per-item G1: §6 item 6, explicitly N/A — "no per-item filtering occurs at construction or execution, period" (the H22 FIX-1 lesson, applied correctly). ✓

## 10. What was checked and found sound (no fix)

- Law #11 tagging (§1.1): hypothesis / observations / interpretation as separate layers; KILL reclassifies the three-bench CONTINUE as a domain-set-detector correlation, never erases (Law #8). The G≥0.30 branch's reclassification ("domain-set-detector correlation") is the correct H16-§4 analog: bench 5 is the domain-scrambled bench, so the three-bench alternative reading is the domain-set-detector story. ✓
- H17 explicitly barred (§6 item 1); no cross-bench effect sizes (§2, §9 item 9); no re-reading of benches 1–4 (Law #13 fence, §8); H22's generality hypothesis stays KILLed (§8 item 3, §10); no post-hoc rewording (Law #4); honesty ledger (§7) and no-claim list (§8) consistent with the program headline; novelty N1 (§8 item 6); summit filter NO (§10). ✓
- G definition and sign convention (original-minus-flipped, N_F=N_T=15) consistent across §2, §3.6, §4. ✓
- The residual-case coverage, the HELD no-rescue discipline, and the absence of PIVOT all match the gate memo. ✓

## Verdict restated

**SIGN.** The H23 pre-registration is mathematically sound and internally consistent. After this review, the protocol is launchable under the CEO launch decision (minting EXP126), pending the standard fix-verification step — which has nothing to verify, since no fixes were required. The launch chain's construction lane carries the conjunctive breaking point; any miss there records the hypothesis UNTESTED, never killed.
