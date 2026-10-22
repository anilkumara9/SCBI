# Law #14 Review — S4-7 (J3) Spectral Phase Transition Pre-registration DRAFT

**Reviewer:** Independent Scientific Mentor & Adversarial Reviewer (no hand in the design or the draft)
**Date:** 2026-10-03
**Document reviewed:** `~/workspace/SCBI/research/prereg/EXP_S47_prereg_DRAFT_2026-10-03.md` (exact file; 249 lines)
**Design under which it is written:** `~/workspace/SCBI/research/innovation/S47_DESIGN_2026-10-03.md` (CONDITIONAL RUN), reviewed in `~/workspace/SCBI/research/innovation/S47_DESIGN_REVIEW_2026-10-03.md` (APPROVE-WITH-CONDITIONS C1–C5)
**Review verdict:** **SIGN** — clean, no mechanical fixes. All five conditions verified closed; no structural flaw.

This review is of the pre-registration draft only. It licenses nothing to run, mints no experiment number, and touches no signed artifact.

---

## 0. Reading note

I read the full draft, the full design, and the full predecessor design review. I independently verified: the three original prior-art citations (Martin & Mahoney arXiv:1810.01075, neural collapse arXiv:2008.08186, intrinsic dimensionality arXiv:2012.13255) via arXiv API; the new Ettori (2026) citation (arXiv:2601.17357v1) via arXiv API; the bench/backbone/HF-revision pins against the committed EXP141 Stage-1 records (`experiments/runs/EXP141_stage1/stage1_records.json`); the Δ_s ≥ 2 bar against the J3 sketch (`research/innovation/S4_I1_FORMALIZATION_AND_J_TIER_2026-09-24.md` line 227); and a sample of LOG numbers (LOG-4879, LOG-4888, LOG-4890, LOG-243, LOG-331, LOG-288) against `reports/research_log.md`.

---

## 1. Condition closure C1–C5 — ALL CLOSED (verified)

- **C1 — σ̂² estimator pinned.** §2 fixes the noise-variance estimator: bulk-median fit against the theoretical MP median at γ_i, with m_MP(γ_i) solving F_{γ_i}(m) = 1 − 1/(2γ_i) via numerical integration of the closed-form MP density f(x) = √((λ₊−x)(x−λ₋))/(2πγ_iσ²x) on [λ₋, λ₊]. I checked the mathematics: for γ_i > 1 the MP law has an atom at 0 of mass 1 − 1/γ_i, so the continuous part has mass 1/γ_i; the equation selects the point where the continuous CDF reaches half its mass — the median of the nonzero spectrum. Correct. The density formula and the bulk-edge formula λ₊ = σ̂²(1+√γ_i)² are the standard forms. Bulk-fit diagnostic (median KS distance, flag 0.15, reported not binding) is pinned. The max-inside-permutation construction is stated explicitly in one sentence (§2): the max-over-layers transformation is computed identically for every item inside every permutation; only labels are shuffled. ✓
- **C2 — n_i measurement-validity guard.** §2 pins N_MIN = 40 (design parameter); items with n_i < 40 are excluded with a diagnostic count; if <30 items remain → HELD with reason ("insufficient positions for stable spectra"), never KILL. The threshold is reasonable: the design prices n_i ≈ 100 typical, so 40 is a floor for degenerate items, not a truncation of the distribution. The <30 → HELD rule is conservative (avoids spurious KILL on underpowered data). The n_i distribution (median, IQR, range, below-floor count) is reported regardless. ✓
- **C3 — prior-art verification.** All four citations verified real by me via arXiv API:
  - Martin & Mahoney, arXiv:1810.01075 — "Implicit Self-Regularization in Deep Neural Networks: Evidence from Random Matrix Theory and Implications for Learning." The draft's characterization (JMLR 2021; MP bulk + signal outliers in trained weight matrices; 5+1 phases) is accurate; the distinctions (weight matrices vs activation covariances; across-models generalization vs per-item correctness within one frozen model) hold.
  - Neural collapse, arXiv:2008.08186 — Papyan, Han & Donoho, PNAS 2020. Characterization accurate; distinctions (training-time vs inference-time; class structure vs per-item correctness) hold.
  - Intrinsic dimensionality, arXiv:2012.13255 — Aghajanyan, Zettlemoyer & Gupta, ACL 2021. Characterization accurate; distinctions (parameter-space vs activation-space; fine-tuning vs inference) hold.
  - Ettori (2026), arXiv:2601.17357v1 — "Spectral Geometry for Deep Learning: Compression and Hallucination Detection via Random Matrix Theory," Davide Ettori, UIC MS thesis (defended 2025-11-21). EigenTrack: real-time hallucination/OOD detection via spectral features and temporal dynamics. The draft's characterization is accurate and the distinctions hold: (a) EigenTrack trains classifiers on spectral features — S4-7 is training-free MP counting + label permutation test; (b) hallucination/OOD detection vs correctness-grouped signal-eigenvalue counts with binding bars; (c) master's thesis, not peer-reviewed — the draft states this. The design's honest negative is correctly superseded, and the novelty read N1 remains valid: the specific construction (training-free MP-outlier counting + one-sided label permutation test on Δ_s with the backlog's bars) is unclaimed in the found art. Nothing is marked verified that is not. ✓
- **C4 — validity gates.** §3: (a) bench sha256, (b) backbone pre-hash, (c) post-run backbone hash (Δθ=0), (d) 60/60 passes, (e) determinism spot-check (3 items, byte-identical s_{i,l}). Any failure → VOID → HELD with reason, never a verdict. The standard kit, complete. ✓
- **C5 — citation fix.** The Friday cull is cited as LOG-4879 in the §1 licensing chain and the C5 closure note; the design's "LOG-4889/LOG-4879" error is corrected. LOG-4879 verified as the Friday cull entry. ✓

---

## 2. Bar fidelity: draft vs design — IDENTICAL (no silent softening)

Checked against the design's §2:

| Bar | Design | Draft | Match |
|---|---|---|---|
| KILL (observational) | p ≥ 0.05 | identical | ✓ |
| CONTINUE | p < 0.05 ∧ Δ_s ≥ 2 | identical | ✓ |
| HELD | p < 0.05 ∧ Δ_s < 2 | identical | ✓ |
| Precedence | KILL > CONTINUE > HELD | identical | ✓ |
| PIVOT | none licensed, none invented | none invented | ✓ |
| Δ_s ≥ 2 source | J3 sketch Law #15 prediction | verified verbatim at sketch line 227 | ✓ |

No bar was softened, moved, or re-worded in the favorable direction. Law #4 holds.

---

## 3. Falsification tree — JOINTLY NON-VACUOUS

Every (p, Δ_s) region maps to exactly one branch under KILL > CONTINUE > HELD:

- p ≥ 0.05 (any Δ_s, including wrong-direction Δ_s < 0 with p ≈ 1) → KILL.
- p < 0.05 ∧ Δ_s ≥ 2 → CONTINUE (licenses only a new worth-it gate for spectral intervention).
- p < 0.05 ∧ Δ_s < 2 → HELD (a).
- C2 guard fires (<30 items with n_i ≥ 40) → HELD (b).
- Stage-1 unrun/infeasible/validity-gate failure → HELD (c), VOID.

No region is unmapped; no two branches collide. The boundary Δ_s = 2 is assigned to CONTINUE (≥ 2), HELD (a) covers < 2 — no gap. No PIVOT invented — correct restraint, matching the backlog row (which licenses no PIVOT).

---

## 4. Law #7 firewall — AIRTIGHT

§5: this is a purely observational test. There is no candidate score, no selection, no trigger, no revision, no ranking. Bench labels define the correct/failed groups in the primary permutation test — that is the validation, and it is the only thing labels touch. The σ̂² estimator, the MP edge, the s_{i,l} counts, and the s_i statistic are all computed label-blind; the permutation seed is fixed (S_PERM = 20261010), never chosen at runtime. The firewall is intact because there is nothing labels could leak into beyond the pre-registered grouping.

---

## 5. Pins and seeds — VERIFIED

Against the committed EXP141 Stage-1 records (`stage1_records.json`, `pins`):

- Backbone: `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed` (pre and post) ✓
- Bench: `eb304fa65a60b65ad87767d251084b256d0a79001a16b4fe8ebcd1b1f45589df` ✓
- HF revision: `9879c9b5f8bea9051dcb0e68dff21493d67e9d4f` ✓

Seeds: S_PERM = 20261010 (100,000-permutation primary test), pinned. No sampling anywhere — all forwards deterministic; no seed is chosen at runtime. Law #13 clean.

---

## 6. One-sided construction — CORRECT

Licensed direction Δ_s > 0; one-sided p = fraction of permuted Δ_s ≥ observed Δ_s; KILL iff p ≥ 0.05. If the true effect is wrong-direction and large, p ≈ 1 → KILL (the bias-coherence counter-argument is collected by the instrument, not rhetorically absorbed). If null, p is uniform and KILL fires with probability 0.95 — the backlog's bar ("permutation p ≥ 0.05 → KILL the observational claim"). The construction matches the predecessor design review's verified logic (§3 of that review). The draft states it correctly.

---

## 7. Numbers and citations — NO INVENTIONS FOUND

Spot-checked against the research log: LOG-288 (J-tier born), LOG-243 (archives insufficient), LOG-331 (EXP086 on real Pythia-410m weights — the HF revision pin's origin), LOG-4879 (Friday cull), LOG-4883 (G/E/S stood down), LOG-4888 (EXP140 stand-down), LOG-4890 (EXP141 kill), LOG-4680 (EXP125 kill, referenced in the non-resurrection audit). All exist with matching substance. The four internal-signal failures (TESTA anti-calibration, EXP140 null, EXP141 kill, EXP125 kill) are characterized consistently with their records. No invented numbers, citations, or LOG numbers found.

---

## 8. Remaining UNCHECKED items — APPROPRIATELY DEFERRED

- The executing lane implements the MP-median numerical integration verbatim from §2 — an implementation detail, correctly deferred (the equation is checked here; the code is the executor's).
- The n_i distribution is unknown until the pilot runs — the C2 guard handles this pre-registered, so nothing blocks sign-off.
- Prior-art search should be re-run before any paper use (§8.7 of the draft) — a paper-stage follow-up, not a pre-reg blocker.

---

## 9. Verdict: SIGN

The pre-registration draft is signed. All five conditions C1–C5 are closed and verified; the bars are identical to the signed design; the falsification tree is jointly non-vacuous; the Law #7 firewall is airtight; pins and seeds are verified; the one-sided construction is correct; no numbers or citations are invented.

**What this review does NOT do:** it does not license execution (CEO approval still required), mint an experiment number, or approve any intervention (the spectral intervention needs its own worth-it gate + Law #14-signed pre-registration + CEO GPU clearance + founder Kaggle slot — nothing is pre-licensed here).

---

## 10. Summary

The S4-7 pre-registration is a clean, binding protocol. Its MP construction is a principled pre-registered counting rule with the label permutation test as the real falsification instrument; the σ̂² estimator math checks out (the median equation selects the median of the nonzero spectrum correctly); the max-inside-permutation construction has no multiple-comparisons inflation; the n_i guard is sound and conservative; all four prior-art citations are independently verified real (including the new Ettori thesis, which correctly supersedes the design's honest negative while leaving the N1 novelty read intact); the bars match the design exactly; and the intervention sharp edge stays honestly deferred. The honest prior remains against the signal, and a null here would close the last J-tier line — but the protocol is built to collect exactly that outcome. Signed without fixes.
