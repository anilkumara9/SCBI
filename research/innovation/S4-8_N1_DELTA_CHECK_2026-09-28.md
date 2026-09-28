# S4-8 N1 Fix — Second Delta Check (LOG-4480)

*Status: VERIFY — binding. This document verifies; it does not edit v1, v2, v3, the review, or the first delta verify; does not authorize a run; does not mint an experiment number.*
*Verifier: independent second-delta lane (pre-assigned LOG-4480), first-touch — this lane has not touched the S4-8 draft, its repair wave, or the EXP085 chain before this verification.*
*Inputs read in full: `research/innovation/S4-8_PREREG_DRAFT_v3_2026-09-28.md` (LOG-4479, v3); `research/innovation/S4-8_PREREG_DELTA_VERIFY_2026-09-28.md` (LOG-4478, first delta verify + N1 exact fix); line-by-line diff of v2 vs v3 (4 changed hunks, all attributable to the N1 fix + direct cross-references + version renumbering).*
*Compute: $0 CPU. No model runs, no weights touched, no signed artifact modified. v3 was NOT edited.*

---

## 1. The N1 fix as specified (LOG-4478, §3)

1. Amend step 8's condition to `…AND overlap O ≤ 0.5 (F diagnostic per the pre-registered stratum)`.
2. Add: "If O > 0.5, the F-significant pattern carries no binding consequence per the stratum — the evaluation falls through to step 9/11."

## 2. Verification of v3's amended step 8

- **(a) F-significance routes only when O ≤ 0.5 — VERIFIED.** v3 step 8 reads: "not CONTINUE, AND ΔM_F > 0 with F-vs-B McNemar p < 0.0125, **AND overlap O ≤ 0.5 (F diagnostic per the pre-registered stratum)** → PIVOT". The O-gate is a binding conjunct of the condition, evaluated first-match-wins in the table.
- **(b) O > 0.5: no binding consequence, falls through to 9/11 — VERIFIED.** v3 step 8 carries the exact sentence: "If O > 0.5, the F-significant pattern carries no binding consequence per the stratum — the evaluation falls through to step 9/11." The enumeration is correct: step 9 (KILL nonspecific) and step 11 (Otherwise → PIVOT) are the downstream catch-alls; step 10 (KILL null) is unreachable with a significant F on a 60-item bench (8 flips minimum for p < 0.0125 ⇒ ΔM_F ≥ 8/60 = 0.133 > 0.05).
- **(c) Step-9 parenthetical covers the O > 0.5 corner — VERIFIED.** v3 step 9: "(D1/N1: this step now fires only when the F-significant pattern did not route to step 8 — including the O > 0.5 corner, where the F pattern is non-diagnostic per the stratum, so the rationale is accurate.)" The rationale "random masking matches — generic perturbation" is therefore licensed exactly when the F pattern is either absent or non-diagnostic — the misdescription N1 targeted is gone.
- **(d) D2 stratum ↔ step 8 consistent in all corners — VERIFIED.**

| Corner | Stratum says | Step 8 does | Consistent |
|---|---|---|---|
| O = 0 | F diagnostic (O ≤ 0.5) | O-gate holds; F-significant routes to PIVOT | YES |
| O ≤ 0.5 | F diagnostic, routes per steps 6/8 | O-gate holds | YES |
| O > 0.5 | F non-diagnostic, descriptive only, no binding consequence | O-gate fails; fall-through to 9/11 | YES |
| O = 1 | non-diagnostic (F ≡ T on all Tier-0 items) | cannot fire | YES |

Cross-references also consistent: §0 PIVOT clause "(§3 step 8, D1 — requires overlap O ≤ 0.5; at O > 0.5 the F pattern is non-diagnostic per the stratum)"; §2.5 "F is non-diagnostic at foil–top-1 overlap > 0.5"; stratum body unchanged.

- **(e) No text drift — VERIFIED.** The v2↔v3 diff contains exactly 4 hunks: (1) title + status line (v2→v3, N1 amendment description, LOG-4479), (2) §0 PIVOT cross-reference (O ≤ 0.5 clause), (3) steps 8–9 (the amendment itself), (4) §8 trailer (v3 note, LOG-4479). No bars, α levels, definitions, mappings, or fence text changed. v1 and v2 untouched on disk.

## 3. Binding verdict: N1 RESOLVED

The N1 defect (step 8 vs the D2 stratum, O > 0.5 corner — LOG-4478 §3) is fixed in v3 as specified: the misattribution corner is unreachable, the fall-through is explicit, and every cross-reference names the same rule. **v3 step 8 is now consistent with the D2 stratum and ready for SIGN.**

### Non-blocking observation (N2, pre-existing — NOT part of the N1 fix, NOT a blocker)

Step 6 (PIVOT diagnostic: ΔM_T ≤ 0 AND ΔM_F > 0, p < 0.0125) is not O-gated, so it can fire in the O > 0.5 corner where the stratum declares F non-diagnostic. This tension is inherited from the Law #14 review's own D2 specification ("O ≤ 0.5 → F diagnostic (routes per steps 6/8)" — the review never demanded an O-gate on step 6), and step 6's corner (T flat, F rescues only where foil ≠ top-1) carries a self-contained rationale that does not misattribute — unlike the N1 corner. Raised for the signing lane's awareness; under this lane's authority (the N1 fix only) it does not block SIGN.

## 4. Full-chain binding verdict

- LOG-4475: v1 draft (DRAFT, UNSIGNED)
- LOG-4476: independent Law #14 review → **SIGN-WITH-FIXES** (8 fixes D1–D5/m1–m3)
- LOG-4477: repair wave v2 (DRAFT, UNSIGNED)
- LOG-4478: first delta verify → **8/8 VERIFIED, 7/7 elements PASS** + new binding defect N1 with exact fix
- LOG-4479: v3 amendment (DRAFT, UNSIGNED — N1 fix applied as pre-registered text)
- **LOG-4480 (this lane): N1 RESOLVED — second delta check PASSED**

The SIGN-WITH-FIXES conditions from LOG-4476 are now fully discharged. **The S4-8 pre-registration is SIGNED.** The next and final gate before any run is **CEO execution clearance** (then Tier-0 screen → battery gate). No experiment number is minted by this check; numbering follows the Law #14 signing + CEO license per the v3 header.

*Verified 2026-09-28 by the independent S4-8 second-delta lane (pre-assigned LOG-4480). $0 CPU, on-paper only. v3 NOT edited.*
