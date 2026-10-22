# Independent Fix-Verification — EXP107 template-control pre-registration (Law #14 follow-up)

**Lane:** LOG-4538 (fix-verification; pre-assigned). Independent of the LOG-4535 design lane and the LOG-4537 repair lane.
**Date:** 2026-09-29
**Document verified:** `research/prereg/EXP_PREREG_EXP107_TEMPLATECTRL_2026-09-29.md` (post-LOG-4537 repair state)
**Review under check:** `research/reviews/LAW14_REVIEW_EXP107_TEMPLATECTRL_2026-09-29.md` (LOG-4536 independent review, verdict **SIGN-WITH-FIXES**)
**Independence [FACT]:** this lane did not write the draft and did not apply the repairs. Verification only — no edits to the prereg or review, no re-review of the whole document, no execution approved, no EXP107 minted.
**Cost:** $0 CPU. Read-only everywhere except this verification file and the LOG-4538 log append. No push, no weights, no GPU contact, no credentials touched.

**Verification method [FACT]:** adversarial text-level check against the review's stated fix definitions. For each fix: the exact repaired text is quoted below from the file, and the review's own verification criterion is re-run independently.

---

## FIX-1 — precision softening ("exactly 30/60" → "≈30/60" + parenthetical): PASS

**Required by review:** in §2 (worth-it gate, quantitative prediction) and §3.6 (registered rival predictions), change "exactly 30/60" to "≈30/60" and append "(point prediction; ±5 of embedding-shift noise absorbed by the ≤35/60 KILL bar)". Verification criterion: `grep -c "exactly 30/60" research/prereg/EXP_PREREG_EXP107_TEMPLATECTRL_2026-09-29.md` returns 0.

**Found (§2, line 28, worth-it gate):**
> `quantitative prediction = pure template artifact ⇒ ≈30/60 on balanced 4×15 cells (point prediction; ±5 of embedding-shift noise absorbed by the ≤35/60 KILL bar), genuine position readout ⇒ ~60/60; breaking point = the 36–39/60 HELD zone.`

**Found (§3.6, line 71, registered rival predictions):**
> `- **Pure template-artifact reading** (head = "outranks-words → A-first" detector): original cells 30/30 correct, flipped cells 0/30 → **≈30/60** (point prediction; ±5 of embedding-shift noise absorbed by the ≤35/60 KILL bar).`

**Criterion re-run:** `grep -c "exactly 30/60"` on the prereg returns **0**. No remaining occurrences anywhere in the file.

**Exact figures preserved (verified builder output untouched):** the detector mechanics remain exact — "original cells 30/30 correct, flipped cells 0/30"; cell balance "balanced 4×15 cells" intact; decision bars, p-values, and hashes unchanged. The repair touched only the qualifier on the artifact point prediction, exactly as licensed. PASS.

## FIX-2 — environment pin in §3.2 (Law #13): PASS

**Required by review:** append to §3.2 (head spec): "Retrain executes in the EXP106 environment (sklearn 1.9.1, `~/.venv-exp077`, torch 2.14.0+cpu) so the sanity gate tests pipeline determinism, not cross-version optimizer drift." Verification criterion: the string "1.9.1" appears in §3.2.

**Found (§3.2, line 44):**
> `- Head: `sklearn.linear_model.LogisticRegression(penalty='l2', C=1.0)`, all other params default — the EXP106 spec verbatim (lbfgs, deterministic on fixed data). No tuning of any kind. Retrain executes in the EXP106 environment (sklearn 1.9.1, `~/.venv-exp077`, torch 2.14.0+cpu) so the sanity gate tests pipeline determinism, not cross-version optimizer drift.`

The text matches the review's required wording verbatim, including torch 2.14.0+cpu. PASS.

## Spot-check — bars, verdict logic, hypothesis unchanged: PASS

- **Decision bars (registered, §4, lines 79–81):** ≥ 40/60 → CONTINUE (p ≈ 0.0067); ≤ 35/60 → KILL the EXP106 transfer reading (GPU proposal license VOID, no rescue runs); 36–39/60 → HELD/INCONCLUSIVE (no re-run, no larger-n rescue). Decision-tree table (lines 95–97) agrees. Block-off precondition intact: "must **pass before any verdict is admissible** (a CONTINUE or KILL with a failed block-off is void)."
- **Verdict logic (§7, lines 115–116):** CONTINUE = genuine position-readout signal (not cognition, not consciousness, not generality); KILL scoped to "only the EXP106 transfer reading," does not re-litigate EXP106's registered CONTINUE; GPU proposal remains founder-gated and proposal-only. All guards intact.
- **Hypothesis (§1):** "A logistic head (L2, C=1.0) ... retains **≥ 40/60** accuracy on a template-decorrelated 60-item bench (four balanced 15-item cells crossing phrasing × template word-family), with byte-identical block-off — i.e., the EXP106 transfer is a target-position readout surviving meaning-preserving rephrasing, not a surface-template artifact." Unchanged.

---

## Verdict

**ALL-FIXES-VERIFIED.** Both LOG-4536 fixes are present in the exact form required, the review's own verification criteria are satisfied independently, and no bar, verdict logic, hypothesis, or number was altered. **The LOG-4536 independent Law #14 review verdict is hereby upgraded from SIGN-WITH-FIXES to SIGN** for `research/prereg/EXP_PREREG_EXP107_TEMPLATECTRL_2026-09-29.md`.

**Boundary:** this lane verifies fixes only. It does NOT approve execution, does NOT mint EXP107, and dispatches no follow-ups. Launch is the CEO's decision.
