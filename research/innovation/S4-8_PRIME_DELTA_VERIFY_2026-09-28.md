# S4-8′ Delta Re-verification — v1 → v2 Repair Wave (LOG-4487)

**Lane:** S4-8′ DELTA RE-VERIFICATION. **Log:** LOG-4487 (pre-assigned). **Date:** 2026-09-28.
**Inputs:** v1 `S4-8_PRIME_PREREG_DRAFT_2026-09-28.md` (LOG-4484), v2 `S4-8_PRIME_PREREG_DRAFT_v2_2026-09-28.md` (LOG-4486), Law #14 review `S4-8_PRIME_PREREG_REVIEW_LAW14_2026-09-28.md` (LOG-4485).
**Scope:** verify ONLY the repair wave's v2 changes against the review's four defects; no protocol edits, no runs, no signed artifact touched. $0 CPU.

---

## 1. Diff result

v1 vs v2 diffed line by line. Exactly 6 changed hunks, all attributable to the four fixes + version markings:
1. Title/header: "DRAFT (UNSIGNED)" → "DRAFT v2 (UNSIGNED, post-Law-#14-repair)".
2. Status line: v2 markings; **stale header corrected** — "LOG-4479/4480 line, awaiting its own delta check" → "**SIGNED at LOG-4480** — N1 resolved" (direct consequence of D1's corrected anchoring).
3. Licensing chain: extended LOG-4484 (draft v1) → LOG-4485 (review, SIGN-WITH-FIXES) → LOG-4486 (v2 repair lane).
4. §0: "six §5 degeneracy unit tests" → "seven §5 degeneracy unit tests (a)–(g)".
5. §1: anchoring rewritten (D1).
6. §2.3 item 3: descriptive cue sensitivity appended (D4).
7. §9 item 3: token-id uniformity diagnostic appended (D3).
8. Footer colophon: v2 repair provenance added.

No other text drift. No numbers invented. No experiment number minted. v3, v1, and the review file untouched.

## 2. Fix scores

| Fix | Review demand | v2 state | Score |
|---|---|---|---|
| **D1 (MAJOR)** — anchoring | Review demanded the carryover be anchored to "currently **unsigned**" v3. Repair lane premise-checked against the log and found the unsigned premise FALSE: LOG-4480's full-chain binding verdict declares "**The S4-8 pre-registration is SIGNED**" (line 561–564 of `reports/research_log.md`: "### LOG-4480 — S4-8 N1 second delta check complete: RESOLVED — pre-registration SIGNED", N1 resolved). | §1 now: cites v3 (`S4-8_PREREG_DRAFT_v3_2026-09-28.md`) as **SIGNED at LOG-4480**; states the review's unsigned premise was checked false against the record; **restates the carried-over bars as this draft's own binding specification, contingent on that recorded SIGN**; **requires re-review before signing if a later signed v3 amendment alters any carried-over element**. All three intent elements present. | **VERIFIED** (premise-corrected form; the log record matches the repair's claim) |
| **D2 (MINOR)** — test count | §0 "six" → "seven §5 degeneracy unit tests (a)–(g)". | §0 line 18 now reads "The seven §5 degeneracy unit tests (a)–(g)". Verbatim to review's fix text. | **VERIFIED** |
| **D3 (MINOR)** — token-id uniformity diagnostic | Append exact diagnostic text to §9 item 3. | Appended verbatim: "Descriptive diagnostic: per-item rank of the correct candidate's token id among the 8 candidate token ids (should be ~uniform over {1,…,8}); per-item tie-event flag (float32 exact equality). If tie events occur and correlate with token-id rank, the rank instrument is voided (HOLD) pending re-review." | **VERIFIED** |
| **D4 (MINOR)** — descriptive cue sensitivity | Append exact sensitivity text to §2.3 item 3. | Appended verbatim: "Pre-registered descriptive sensitivity (NOT a second instrument): if Tier-0 passes its gates, the Tier-0 worksheet may include a re-run under the single named alternative cue `Answer:` + completion (one line in the worksheet, descriptive only, never a gate or a result). It may not be added, removed, or re-cued after any Tier-0 number is seen." Consistent with the preceding "Pre-registered non-arm" sentence. | **VERIFIED** |

## 3. Remaining defect (pre-existing, review-missed — NOT introduced by the repair wave)

- **§1 line 38: "all six tests re-run on the cloze rank/mask/McNemar machinery"** — v1 had the same "six" (line 38); the review's D2 scoped only §0, so this instance was never fixed. §5 lists (a)–(g) = 7 tests and §9 item 5 says "the seven §5 tests". One-word textual inconsistency: an executor counting "six" risks skipping the cloze-specific (g).
- **Exact remaining fix:** §1 line 38 → "all seven tests (a)–(g) re-run on the cloze rank/mask/McNemar machinery before bench contact (see §5)."

## 4. New defects introduced by the repair wave

**None.** The D1 premise-correction is documented on-record (LOG-4486 + v2 footer) and matches the log; the stale-header correction is a direct consequence of D1, not scope creep.

## 5. Binding verdict: **SIGN-WITH-FIXES**

S4-8′ draft v2 is cleared for CEO signing consideration after the single one-word fix in §3 above (textual only; no re-review of design required). The repair wave discharged all four review defects to intent; the remaining inconsistency predates the repair and was missed by the review, not introduced by it. **Not authorized by this verification:** any run, any pilot, any experiment number, any GPU contact. Sequencing: §1 one-word fix → CEO signing consideration → CEO execution clearance → cloze Tier-0 (60 passes, $0).

*Verified 2026-09-28 by the DELTA RE-VERIFICATION lane (pre-assigned LOG-4487). $0 CPU. No protocol edited. No signed artifact touched.*
