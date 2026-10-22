# Law #14 Review — S4-5 (J4) Free-Energy Branch Selection Pre-registration DRAFT

**Reviewer:** Independent Scientific Mentor & Adversarial Reviewer (no hand in the design or the draft)
**Date:** 2026-10-03
**Document reviewed:** `~/workspace/SCBI/research/prereg/EXP_S45_prereg_DRAFT_2026-10-03.md` (exact file; 182 lines)
**Design under which it is written:** `~/workspace/SCBI/research/innovation/S45_DESIGN_2026-10-03.md` (CONDITIONAL RUN), reviewed in `~/workspace/SCBI/research/innovation/S45_DESIGN_REVIEW_2026-10-03.md` (APPROVE-WITH-CONDITIONS C1–C5)
**Review verdict:** **SIGN-WITH-FIXES** (3 mechanical fixes, §9). No structural flaw warrants REJECT; execution additionally needs CEO approval per the design's launch chain.

This review is of the pre-registration draft only. It licenses nothing to run, mints no experiment number, and touches no signed artifact.

---

## 0. C2-direction ruling (priority) — **CONFIRM the draft's resolution**

The design's §5 contains a genuine internal contradiction, and the drafting lane read it correctly:

- Design §5, C1: Spearman(F̄, per-item accuracy), one-sided, **negative** direction — licensed direction stated twice as "lower F ↔ higher accuracy."
- Design §5, C2 literal text: "mean F̄ on majority-wrong items **<** mean F̄ on majority-right items."
- The licensed direction entails: majority-wrong (low accuracy) → **higher** mean F̄, i.e. wrong **>** right. The literal `<` tests the *inverted* hypothesis against the design's own Law #15 prediction.

**Ruling:** the draft's resolution (C2 trip: wrong **>** right, one-sided) is the correct form. The `<` is a transcription slip, not a design choice — the licensed direction is the candidate's Law #15 prediction and appears twice in the design. The draft additionally resolves the mirroring correctly: TESTA's R2 found wrong-items mean margin 1.0578 > right-items 0.8627 (the anti-calibrated observation), and the draft's C2 mirrors that procedure with the sign in the licensed direction. **CONFIRMED — no change.**

---

## 1. Condition closure C1–C5 — ALL CLOSED (verified)

- **C1 — seeds pinned.** §2 pins S_B2=20261004, S_B3=20261005, S_PERM_C2=20261006, S_RANDOM=20261003. No seed chosen at runtime. ✓
- **C2 — H-wave precedent corrected.** §1 cites LOG-4552. Independently grep-verified: the "108 generations in 20.9 min" figure appears in the LOG-4552 entry (line 11474, EXP109 execution report, 2026-09-29); LOG-4553 is the H2 QBR pre-registration draft (line 11476). The design's LOG-4553 citation was indeed a misattribution. ✓
- **C3 — prior art, abstract level, honestly labeled.** §8 verifies Jinnai et al. arXiv:2311.05263, Freitag et al. arXiv:2111.09388, CycleVLA arXiv:2601.02295 at abstract level via arXiv API (2026-10-03) with distinctions from S4-5 stated; FREIA distinction restated; full-text verification explicitly flagged as follow-up for any paper use. Independent re-verification by this reviewer was rate-limited at review time (arXiv API returned rate-limit errors); nothing in the draft's characterizations contradicts the predecessor review's verified FREIA reading or the abstracts' public summaries, and the draft's "abstract-level only" labeling satisfies Law #3 (no fabricated citations; nothing marked verified that is not). No citation must stay UNVERIFIED beyond the flagged full-text follow-up. ✓ (with the noted limitation)
- **C4 — degenerate handling + dual reporting.** §2 pins R_max=48; empty rationale → F undefined → branch excluded from selection/F-statistics/SC/vote/per-item accuracy with diagnostic count; ≥3 fully-degenerate items → pilot VOID; identical branches → spread 0, lowest-index tie-break; primary F_k and secondary F^full_k reported side by side. No improvisation surface left. ✓
- **C5 — min-F consequence stated.** §3: secondary min_k-F inversion while mean-F passes G3 → binding consequence is Stage-2's KILL-selector bar (ΔM_FE ≤ ΔM_random) — "mean-calibration is not a selection license." The instrument/selector gap is closed. ✓

---

## 2. Bar fidelity: draft vs design — IDENTICAL (no silent softening)

Checked point-by-point against the design's §2 and §5:

| Bar | Design | Draft | Match |
|---|---|---|---|
| G1 diversity | ≥2 distinct answers, ≥25% items | ≥15/60 items (15/60 = 25%) | ✓ |
| G2 variance | median F-spread ≥ 0.05 nats/token | identical | ✓ |
| G3 pass | C1 ∧ C2 both pass, licensed direction | identical | ✓ |
| G3 either-null | no GPU, stands down | HELD (b), "no GPU" | ✓ |
| G3 either-inverted | KILL family outright | identical | ✓ |
| CONTINUE | ΔM_FE ≥ +8pp ∧ LCI > 0.05 ∧ ΔM_FE > ΔM_random (p < 0.05) | identical, McNemar-exact specified | ✓ |
| KILL (selector) | ΔM_FE ≤ ΔM_random | identical | ✓ |
| KILL (branching) | ΔM_FE ≤ 0 | identical | ✓ |
| PIVOT | G3 passes ∧ Stage-2 kills selector | identical | see §7 — unreachable under stated precedence |
| HELD | 0 < ΔM_FE < +8pp, or LCI straddles 0.05 | expanded to (a)–(e) | see §8 — one sub-case gap |

No bar was softened, moved, or re-worded in the favorable direction. Law #4 holds.

---

## 3. Pins — VERIFIED against committed records

- Backbone pin `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed`: present in `experiments/runs/EXP139_stage1/stage1_records.json` (backbone_pre). ✓
- Bench pin `eb304fa65a60b65ad87767d251084b256d0a79001a16b4fe8ebcd1b1f45589df`: present in the same records (bench_sha256) and in the RUN_REPORT bench check. ✓
- Model revision `9879c9b5f8bea9051dcb0e68dff21493d67e9d4f` (LOG-331 pin) and `tie_word_embeddings: false`: stated as verified from the EXP139 pre-reg; consistent with the records' fidelity claim. ✓
- TESTA numbers cited in §1/§8: ρ=−0.3958, p=0.0017, wrong 1.0578, right 0.8627 — all grep-verified verbatim in `research/innovation/TESTA_CALIBRATION_2026-10-03.md` (lines 57–69). ✓
- Licensing chain LOGs (LOG-288, LOG-4353, LOG-4879, LOG-4883): all exist as log entries. ✓
- Bench reconstruction source (`run_exp135.py` `build_bench`, `make_views`, `tok1`): stated as reconstruction source; the bench pin binds it. ✓

---

## 4. Cost correction — VERIFIED correct

The design's §3 stated "240 generations + 300 forward passes," derived as 60×4 branch passes + 60 "B0-equivalent baseline passes." B0 is one of the 4 branches, so the design double-counted: the 240 already includes B0's generation and scoring. The draft's correction (240 generations + 240 combined scoring passes, answer readout folded into the teacher-forced pass) is arithmetically right, and the fold is exact for a causal LM (appended suffix does not alter earlier tokens' log-probs). Still ~1h CPU by the LOG-4552 precedent. The correction is flagged in §1, not buried. ✓

---

## 5. Newcombe construction — VERIFIED

§6 gives the explicit Wilson (z=1.96, no continuity correction) and Newcombe Method-10 equations. The formulas were checked term-by-term against the standard forms: center = (p̂ + z²/2n)/(1 + z²/n), half = z·√(p̂(1−p̂)/n + z²/4n²)/(1 + z²/n), L = Δ̂ − √((p̂_b − l_b)² + (u_c − p̂_c)²), U = Δ̂ + √((u_b − p̂_b)² + (p̂_c − l_c)²). All correct. Paired (b,c) construction standard. Binding bar Δ̂ ≥ 0.08 ∧ L > 0.05 matches the Law #15 block. ✓

---

## 6. Law #7 firewall — AIRTIGHT

§7: labels touch only bench evaluation (accuracy, ΔM, paired tables) and the G3 instrument (per-item correctness). "No branch score, no selection, no ranking, no gate threshold sees labels." G1/G2 use no labels; G3 thresholds (p < 0.05, licensed direction) are fixed here, never tuned. The selector (argmin_k F_k) is computable with labels absent. The mean-F (not min-F) instrument is a genuine firewall refinement. ✓

---

## 7. PIVOT is unreachable under the stated precedence — FIX REQUIRED (F1)

The draft states precedence **KILL > PIVOT > CONTINUE > HELD** and defines:

- KILL (selector): G3 either-inverted **or** Stage-2 ΔM_FE ≤ ΔM_random.
- PIVOT: G3 passes **but Stage-2 KILLs the selector.**

"Stage-2 KILLs the selector" is exactly ΔM_FE ≤ ΔM_random, which trips KILL-selector first under the stated precedence. PIVOT can never be earned — it is a dead branch in a binding verdict document. (The design review's case-table walk missed this; a gap is not the issue here, an unreachable branch is.) **Fix F1:** demote PIVOT to an annotated sub-reading of KILL-selector — "when G3 passed, the KILL-selector verdict carries the calibrated-signal sub-reading: signal real but selection-useless" — or give PIVOT a trip condition distinct from KILL-selector's. Recommended: the sub-reading form (one sentence in §5), which preserves the stated precedence.

---

## 8. HELD (c) has a coverage gap — FIX REQUIRED (F2)

The draft's case table is claimed gap-free, but one region is unmapped:

- CONTINUE requires Δ̂ ≥ +8pp ∧ L > 0.05 ∧ ΔM_FE > ΔM_random **with p < 0.05**.
- KILL requires ΔM_FE ≤ ΔM_random.
- HELD (c) covers "0 < ΔM_FE < +8pp, or Δ̂ ≥ +8pp with LCI straddling 0.05."

The region {Δ̂ ≥ +8pp, LCI > 0.05, ΔM_FE > ΔM_random numerically, **p ≥ 0.05**} matches no branch. This region is non-empty (paired McNemar-exact can fail significance on a positive numerical Δ). **Fix F2:** extend HELD (c) to "positive ΔM_FE failing either the Newcombe magnitude bar or the paired-significance bar," so every (ΔM_FE, ΔM_random, LCI, p) region maps to exactly one verdict. One-sentence edit.

---

## 9. Verdict: SIGN-WITH-FIXES

Apply these three mechanical fixes to the draft; no further Law #14 review cycle is needed if a verification lane confirms each fix is textual-only:

1. **F1 — PIVOT reachability.** §5: demote PIVOT to an annotated sub-reading of KILL-selector ("calibrated-signal sub-reading: signal real but selection-useless, when G3 passed") or give it a distinct trip condition. Keep precedence KILL > PIVOT > CONTINUE > HELD.
2. **F2 — HELD (c) coverage.** §5: extend HELD (c) to cover {Δ̂ ≥ +8pp, LCI > 0.05, ΔM_FE > ΔM_random, p ≥ 0.05}: "positive ΔM_FE failing either the magnitude bar or the paired-significance bar."
3. **F3 — record the review limitation.** §8 or the header: note that the three non-FREIA citations were abstract-level-verified by the drafting lane and that independent reviewer re-verification was rate-limited at review time; full-text verification remains a flagged follow-up before any paper use.

**What this review does NOT do:** it does not license execution (CEO approval still required), mint an experiment number, or approve Stage 2 (strictly gated on G1–G3 all passing in the licensed direction, plus signed pre-registration, CEO GPU clearance, and founder Kaggle slot).

---

## 10. Summary

The S4-5 pre-registration draft is binding-quality work. All five design-review conditions close cleanly (seeds pinned; LOG-4552 citation corrected and grep-verified; prior art honestly abstract-level with full-text follow-up flagged; R_max=48 and degenerate-branch handling leave no improvisation surface; the min-F-inversion consequence is stated). The flagged C2-direction deviation is resolved correctly — the draft's "wrong > right" is CONFIRMED against the licensed direction, and the design's literal "<" was a transcription slip. The pins, the cost correction, and the Newcombe construction all verify. The bar set is identical to the design's (no softening); the Law #7 firewall is airtight; the bars are non-vacuous. Two specification defects remain, both mechanical: PIVOT is unreachable under the stated precedence (fix: demote to a KILL-selector sub-reading) and HELD (c) leaves one sub-region unmapped (fix: extend its wording). SIGN-WITH-FIXES; apply F1–F3, then CEO approval licenses Stage 1.
