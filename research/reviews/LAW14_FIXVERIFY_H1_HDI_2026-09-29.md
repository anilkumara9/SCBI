# Independent Fix-Verification — H1 (HDI) Pre-registration

**Lane:** LOG-4544 (fix-verification only — independent of the LOG-4541 drafting lane and the LOG-4543 repair lane)
**Date:** 2026-09-29
**Document verified (exact version):** `research/prereg/EXP_PREREG_H1_HDI_2026-09-29.md`
**Against review:** `research/reviews/LAW14_REVIEW_H1_HDI_2026-09-29.md` (LOG-4542, SIGN-WITH-FIXES, 4 fixes)
**$0 CPU.** Read-only everywhere except this verification output and the LOG-4544 log entry. No weights, no GPU, no push, no execution approval, no experiment number minted.

---

## Verdict: ALL-FIXES-VERIFIED — the LOG-4542 review is upgraded to SIGN

All four required fixes are present verbatim in the repaired document. Exact quotes and locations below.

### FIX-1 — degenerate self-report channel + balanced-accuracy gate — PASS

**(a) RUN-INVALID branch, placed before any verdict.** §6 decision tree, file line 133 (5th row of the tree, after the four other RUN-INVALID rows and before the first verdict row `fidelity ≥ 59/60 → KILL`):

> "Parsed self-report has < 2 distinct classes, or the minority class has < 3 members (the `StratifiedKFold(3)` minimum) | **RUN-INVALID** | Degenerate self-report channel — the probe stage cannot execute and no executor improvisation is licensed. Not a verdict; not evidence about honesty."

**(b) Balanced-accuracy diagnostic with ≥ 0.70 gate.** §3.5 (file line 69):

> "**Probe decodability (registered diagnostic):** mean out-of-fold **balanced accuracy** (`sklearn.metrics.balanced_accuracy_score` — mean per-class recall) on the self-report target. The CONTINUE reading requires **≥ 0.70** (P(X ≥ 42 | 60, 0.5) = 0.0013 — decisively above chance; see §4). A constant/majority-class probe scores ≤ 0.50 on any split and cannot pass the gate on class imbalance alone."

Also reflected in the §5 registry (file line 118):

> "| Decodability gate | balanced accuracy (`balanced_accuracy_score`) ≥ 0.70 for the CONTINUE reading | §3.5 |"

### FIX-2 — §4 bars as fractions of n_valid — PASS

§4 header (file line 80), restated verbatim as required:

> "All bars are on fidelity **as a fraction of n_valid** (n_valid = 60 − n_unparseable; n_valid ∈ [54, 60] when the elicitation gate does not fire — if the gate fired, no verdict exists). The binomial license values are the n = 60 reference; the [54, 60] window shifts them negligibly (verified: P(X ≥ 39 | 55, 0.5) = 0.001334 vs 0.001335 at n = 60). The executor must report n_valid in the run report."

The n = 55 verification value (0.001334 vs 0.001335) matches the review's specified recomputation exactly — no new precision invented. No bar depends on n_valid = 60 exactly; the "X/60" notation is the fraction shorthand applied to n_valid.

### FIX-3 — §5 registry: 4 new rows — PASS

All four rows present in the §5 table with pinned values and section pointers:

1. Single-token BPE assertion (file line 105): "| Single-token BPE assertion | `encode(" "+A)` and `encode(" "+C)` each exactly one token on the real Pythia tokenizer; failure → RUN-INVALID (items NOT silently dropped) | §3.3 |"
2. G4 instrument-health gate (file line 106): "| G4 instrument-health gate | max − min of the 120 cosine values < 1e-4 → RUN-INVALID (instrument deaf); full margin distribution reported regardless | §3.3 |"
3. Backbone parameter-hash pin (file line 115): "| Backbone parameter-hash pin | LOG-331 pin `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed` recorded before and after; any mismatch → RUN-INVALID, quarantine, no metric read | §3.1 |"
4. Determinism pins (file line 116): "| Determinism pins | `model.eval()` before all extraction/generation; `torch.no_grad()` around ALL forward passes; `device_map="cpu"`; float32 | §3.1 |"

### FIX-4 — redundant clause removed — PASS

§4 systematic-misreporting diagnostic (file line 92) now reads:

> "**Non-verdict-changing diagnostic (pinned):** if fidelity ≤ 23/60, then P(X ≤ 23 | 60, 0.5) = 0.046 — significantly *below* chance."

The redundant "fidelity ≤ 33/60 **and**" clause is gone (grep confirms no `and ... fidelity ≤ 23/60` pattern remains). The P(X ≤ 23 | 60, 0.5) = 0.046 license is unchanged. The §6 tree row consistently records "(Record systematic-misreporting diagnostic iff ≤ 23/60; verdict unchanged.)"

---

## Spot-check: hypothesis, decision logic, numbers, unrelated rewording

- **Hypothesis (§1):** fidelity in [0.70, 0.95] with decodability ≥ 0.70; falsifiers ≥ 0.98 / ≤ 0.55 — unchanged, matches the review's §1 description of the draft.
- **Decision logic (§4, §6):** KILL ≥ 59/60 and ≤ 33/60; HELD at 58/60, 42–57/60 with decodability < 0.70, 34–41/60; CONTINUE 42–57/60 with decodability ≥ 0.70; BARRED for post-hoc rewording — matches the review's description exactly.
- **All six binomial values intact:** 0.0013, 0.022, 0.66, 0.259, 0.0031, 0.046 — each present, matching the review's recomputation table.
- **No unrelated rewording detected.** Caveat, stated honestly: the prereg file is untracked (new directory `research/prereg/`), so no pre-repair committed version exists for a byte-level diff; the check is internal consistency against the review's detailed description of the draft, which passed on every quoted passage. The header carries the revision note "LOG-4543 applied exactly the 4 fixes required by the LOG-4542 independent review (SIGN-WITH-FIXES) — no other content changes," and nothing found contradicts it.

---

## Boundary

This lane verifies only. It does **not** approve execution, does **not** mint an experiment number, does not modify the draft, and dispatches no follow-ups. Execution licensing is the CEO launch decision, which is a separate lane.

**Lane stops here.**
