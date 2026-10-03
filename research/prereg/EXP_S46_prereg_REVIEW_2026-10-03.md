# Law #14 Review — S4-6 (J2) Metacognitive Self-Modeling Pre-registration DRAFT

**Reviewer:** Independent Scientific Mentor & Adversarial Reviewer (no hand in the design or the draft)
**Date:** 2026-10-03
**Document reviewed:** `~/workspace/SCBI/research/prereg/EXP_S46_prereg_DRAFT_2026-10-03.md` (exact file; 181 lines)
**Design under which it is written:** `~/workspace/SCBI/research/innovation/S46_DESIGN_2026-10-03.md` (CONDITIONAL RUN), reviewed in `~/workspace/SCBI/research/innovation/S46_DESIGN_REVIEW_2026-10-03.md` (APPROVE-WITH-CONDITIONS C1–C3)
**Review verdict:** **SIGN**
**Review method:** full read of the draft, full read of the design, full read of the predecessor design review; independent verification of EXP125's characterization against LOG-4680; independent verification of all three pins (bench, backbone, HF revision) against the committed `experiments/runs/EXP140_stage1/stage1_records.json`; title-level verification of Kamoi (ACL Anthology 2024.tacl-1.78) and Xu (ACL Anthology 2024.acl-long.826); arXiv API rate-limited at review time (same as the predecessor review); full case-table walk of §5.

This review is of the pre-registration draft only. It licenses nothing to run, mints no experiment number, and touches no signed artifact. Stage 1 still needs CEO approval; Stage 2 needs CEO GPU clearance plus the founder's Kaggle slot.

---

## 0. §1 mechanical-clarification ruling (priority) — **CONFIRM the draft's adaptation**

The design's §5 C2 carried TESTA's "majority-wrong/right" language, which presupposes per-item multiple views (TESTA's wrong = ≤2/5 correct across 5 views). S4-6 contributes **one baseline answer per item** (binary correctness), so the partition adapts to mean(â_self | baseline-wrong items) < mean(â_self | baseline-right items), one-sided permutation, licensed direction (higher â_self ↔ higher accuracy) unchanged.

**Ruling:** CONFIRMED. The adaptation preserves the statistical form (partition by correctness, one-sided permutation test on the mean difference, licensed direction) while matching the bench's structure. This is a transcription-level clarification, not a bar change — the same class of ruling as the S4-5 C2-direction confirmation, which the design review there handled the same way.

---

## 1. Condition closure C1–C3 — ALL CLOSED (verified)

- **C1 — EXP125 characterization corrected. ✓** The draft's §1 and §6(v) characterize EXP125 as a first-token logit-readout honesty self-report (fidelity 28/60 vs the registered cosine-argmax decision statistic, LOG-4680, bench-specific). I independently read LOG-4680: "KILL — the honesty-instrument generality hypothesis is dead at logit level. Fidelity between the frozen backbone's first-token logit-readout self-report and the registered cosine-argmax decision statistic on fresh bench 4 = 28/60 = 0.4667... EXP112's bench-1 HELD (41/60) stands per Law #8, reclassified bench-specific (Law #11)." The draft's characterization is accurate. The "verbalized vs distributional" framing appears nowhere in the draft (grep confirms: the two occurrences are meta-sentences explicitly stating its absence). The non-resurrection rests on the four correct grounds (a–d) from the design review. ✓
- **C2 — revision mechanics pinned. ✓** §2 pins revision decoding GREEDY (matching baseline ŷ_i); trigger-rate floor 15/60 (25% of the bench, pre-registered design parameter); <15 triggered → revision test VOID → HELD with reason. The floor is a stated design parameter (not derived from data — §10.7 admits this); the VOID rule is unambiguous. ✓
- **C3 — Kamoi and Xu verified. ✓** Both confirmed real via the ACL Anthology at review time: Kamoi et al., "When Can LLMs Actually Correct Their Own Mistakes? A Critical Survey of Self-Correction of LLMs," 2024.tacl-1.78; Xu et al., "Pride and Prejudice: LLM Amplifies Self-Bias in Self-Refinement," 2024.acl-long.826. The characterizations match the papers: Kamoi's three findings (no successful prompt-only self-correction except exceptionally suited tasks; works with reliable external feedback; fine-tuning enables it) and Xu's self-bias result (formally defined, prevalent across six LLMs, amplified by self-refine). Limitation noted: the arXiv API was rate-limited at review time, so my confirmation is title/venue-level via the Anthology; the drafting lane's full-text read of Xu and abstract/metadata check of Kamoi stand. Nothing is marked verified that is not. Full-text re-verification remains flagged for any paper use, as the draft itself states. ✓ (with the noted limitation)

---

## 2. Bar fidelity: draft vs design — IDENTICAL (no silent softening)

Checked point-by-point:

| Bar | Design | Draft | Match |
|---|---|---|---|
| G1 variance | std > 0.01, non-constant | identical | ✓ |
| G2 I-screen | 4-bin MI + Miller-Madow + 100k permutations; null (p ≥ 0.05) → KILL before revision | identical, seed pinned 20261007 | ✓ |
| G3 pass | C1 Spearman positive ∧ C2 partition, both one-sided p < 0.05 | identical, seed pinned 20261008 | ✓ |
| G3 either-null | no GPU, stands down | HELD (b), "no GPU" | ✓ |
| G3 either-inverted | KILL family outright | identical | ✓ |
| CONTINUE | I-screen passes ∧ ΔM_trig ≥ +8pp ∧ LCI > 0.05 ∧ ΔM_trig > ΔM_rand (p < 0.05) | identical, McNemar-exact specified | ✓ |
| KILL (self-model) | I-screen null | identical | ✓ |
| KILL (calibration) | G3 either-inverted | identical | ✓ |
| KILL (revision) | ΔM_trig ≤ ΔM_rand | identical | ✓ |
| PIVOT | I > 0 but ΔM_trig ≤ 0 | identical, reachability annotated | ✓ |
| HELD | 0 < ΔM_trig < +8pp, LCI straddle, numerical superiority p ≥ 0.05 | identical, + trigger-floor VOID | ✓ |
| τ_rev | 0.5, pre-registered design parameter | identical | ✓ |
| Revision decode | unpinned (C2) | GREEDY (condition closure, not a softening) | ✓ |
| Trigger floor | unspecified (C2) | 15/60 + VOID rule (condition closure) | ✓ |

No bar was softened, moved, or re-worded in the favorable direction. Law #4 holds. The two condition-closure additions (greedy decode, floor) are tightenings, not loosenings.

---

## 3. Falsification tree — JOINTLY NON-VACUOUS; PIVOT REACHABLE

Walked the full (I, ΔM_trig, ΔM_rand, LCI) space against precedence KILL (any) > PIVOT > CONTINUE > HELD:

- G2 null → KILL (self-model); G3 inverted → KILL (calibration); G1 fails → HELD (a); G2/G3 null → HELD (b).
- Stage 2 (requires G1–G3 all passing, explicitly linked in §3):
  - ΔM_trig ≥ +8pp ∧ L > 0.05 ∧ ΔM_trig > ΔM_rand (p < 0.05) → CONTINUE.
  - ΔM_trig ≤ ΔM_rand → KILL (revision).
  - ΔM_rand < ΔM_trig ≤ 0 → PIVOT fires without KILL (revision) tripping — **reachable**, non-empty region. The S4-5 F1 lesson was learned.
  - 0 < ΔM_trig < +8pp / LCI straddle / numerical superiority with p ≥ 0.05 → HELD (c).
  - ΔM_trig ≥ +8pp ∧ ΔM_trig ≤ ΔM_rand → HELD (d) (precedence: KILL revision).
  - Trigger floor not met / validity gate fails / unrun → HELD (e), VOID.
- Every region maps to exactly one verdict. No gap (contrast the S4-5 review's F2, which found one here and which this draft avoids by construction).

---

## 4. Pins — VERIFIED against committed EXP140 Stage-1 records

- Backbone pin `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed`: present in `experiments/runs/EXP140_stage1/stage1_records.json` (`pins.backbone_pre`, `pins.backbone_post`). ✓
- Bench pin `eb304fa65a60b65ad87767d251084b256d0a79001a16b4fe8ebcd1b1f45589df`: present (`pins.bench`). ✓
- HF revision `9879c9b5f8bea9051dcb0e68dff21493d67e9d4f`: present (`pins.hf_revision`). ✓
- Model `EleutherAI/pythia-410m`, dtype float32: present (`pins.model`, `pins.dtype`). ✓

---

## 5. Seeds — ALL PINNED (Law #13 clean)

S_PERM_G2 = 20261007 (I-screen permutation), S_PERM_C2 = 20261008 (G3 C2 partition), S_RANDTRIG = 20261009 (random-trigger subset). Self-eval is teacher-forced — no sampling seed needed. No seed is chosen at runtime.

---

## 6. Law #7 firewall — AIRTIGHT

§7: labels touch only bench evaluation (accuracy, ΔM, paired tables), the G2 I-screen instrument (correctness c), and the G3 calibration instrument (per-item correctness). "No self-eval score, no trigger, no revision, no gate threshold sees labels." G1 uses no labels; G2/G3 thresholds (p < 0.05, licensed direction) and τ_rev = 0.5 are fixed here, never tuned on labels. â_self is computable with labels absent.

---

## 7. Newcombe construction — VERIFIED

§6 gives the explicit Wilson (z=1.96, no continuity correction) and Newcombe Method-10 equations. Checked term-by-term against the standard forms — identical to the S4-5 construction I verified term-by-term in the EXP140 pre-reg review. Binding bar Δ̂ ≥ 0.08 ∧ L > 0.05 matches the Law #15 block. ✓

---

## 8. Baseline-source decision — LEGITIMATE AND PINNED

The draft REUSES the committed EXP140 B0 records as ŷ_i, with the review's §7 legitimacy grounds (committed, deterministic, byte-identical on re-run). Stage-1 = 60 self-eval passes (no baseline regeneration), within the design's ≤120-pass budget. The choice is pinned in §1, not left to the executing lane. The reuse-vs-regenerate option was the design's own; the draft chose one branch. ✓

---

## 9. Spot-checks for invented numbers/citations/LOGs

- LOG-288 (S4-6 born): exists as "LOG-288 — J-tier: four summit-aimed candidates" (grep-verified). ✓
- LOG-4680, LOG-4883, LOG-4888, LOG-331: all exist (LOG-4680 read in full above; LOG-4883/4888 are this week's entries). ✓
- TESTA numbers referenced (ρ=−0.3958, p=0.0017): verified verbatim in the S4-5 pre-reg review chain. ✓
- EXP140 figures referenced (min-F 70.0%, random-branch 76.7%): match LOG-4888. ✓
- EXP140 B0 baseline for the reuse claim: EXP140's run records carry the B0 branch (the execution lane's records are committed). ✓

No invented numbers, citations, or LOG numbers found. Law #2/Law #3 clean.

---

## 10. UNCHECKED items — none blocking sign-off

- Kamoi full-text: abstract/metadata-level verification stands; full-text flagged for paper use (the draft's own framing). Not blocking for a pre-reg.
- Xu full-text: drafting lane read the PDF; my independent confirmation is venue/title-level (arXiv rate-limited). The characterization is consistent with the known paper. Not blocking for a pre-reg.
- The executing lane must implement the §6 equations verbatim and archive the code (the draft says so; standard).

---

## 11. Verdict: SIGN

All three conditions C1–C3 are closed and verified; the §1 mechanical clarification is confirmed (baseline-wrong/right adaptation); bars are identical to the signed design with no softening; the falsification tree is jointly non-vacuous with a reachable PIVOT; the Law #7 firewall is airtight; all pins verify against the committed EXP140 records; all seeds are pinned; no invented numbers or citations. No mechanical fixes required — this review issues a clean SIGN.

**What this review does NOT do:** it does not license execution (CEO approval still required), mint an experiment number, or approve Stage 2 (strictly gated on G1–G3 all passing in the licensed direction, plus CEO GPU clearance, plus the founder's Kaggle slot).

---

## 12. Summary

The S4-6 pre-registration draft is sound, falsification-first, and ready for CEO approval. The EXP125 characterization is corrected and verified against LOG-4680; the revision mechanics (greedy decode, 15/60 trigger floor + VOID rule) are pinned; Kamoi and Xu are verified real with accurate characterization; the C2 partition adaptation is confirmed as a faithful mechanical clarification; bars match the signed design exactly; the falsification tree covers every region with a reachable PIVOT; the firewall is airtight; pins and seeds verify. The honest prior is against the signal — a G2-null kill at $0 would be the expected and summit-relevant outcome.
