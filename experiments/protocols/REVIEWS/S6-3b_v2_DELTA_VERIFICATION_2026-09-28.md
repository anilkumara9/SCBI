# S6-3b v1 → v2 Delta Re-verification (2026-09-28)

**Lane:** independent delta re-verification (fresh; did not draft v1, did not review it, did not repair it).
**Target files:**
- v1: `research/innovation/S6-3b_PREREG_DRAFT_v1_2026-09-28.md`
- v2: `research/innovation/S6-3b_PREREG_DRAFT_v2_2026-09-28.md`
- Fix spec: `experiments/protocols/REVIEWS/S6-3b_DRAFT_v1_LAW14_REVIEW_2026-09-28.md` (F1–F2, LOG-4443)

## Check 1 — v1 immutability
`sha256sum` of v1 = `6f79f555e81f8e827ef6a3ca42a90313dea6715f905d192b20aa8c6a28e07e73` — **matches** the pre-repair hash exactly. v1 untouched. PASS.

## Check 2 — F1–F2 applied exactly as specified

- **F1** (naming collision): v2 §0 breaking point (iv) now reads "A third aggregation tweak is pre-emptively unlicensed by this draft." — the "(S6-3c)" label is deleted; the sentence is otherwise byte-identical to v1. `grep -n "S6-3c"` on v2 returns exactly one hit (line 37): "it is the named S6-3c candidate if S6-3b collapses" — the later-layer-relevance-read candidate per §0.2. Exact per spec. PASS.
- **F2** (mean-field audit fence):
  - §2.2 (v2 line 90): "the mean column exists for the gate-integrity audit ONLY: the verdict lane may use it solely to verify (a) the fired ⟺ mass_i^max ≥ τ_i consistency on all 60 rows and (b) the structural mean-fire ⟹ max-fire implication (same τ). It is not a second gate; no mean-field-derived coverage, flip, or counterfactual quantity may be cited." The v1 "audit the S6-3-comparability counterfactual" invitation is gone. PASS.
  - §5 item 2 (v2 line 189): "attention mass_i^mean [audit field — gate-integrity audit only: fired⟺max≥τ consistency + mean-fire⟹max-fire check; not a second gate]". PASS.
  - §4.3 verdict discipline (v2 line 181): the fence sentence appears **verbatim** — "The mean-mass audit field is evidence for the gate-integrity audit only; it is not a second gate — no verdict, worksheet cell, or report may cite any mean-field-derived coverage, flip, or counterfactual quantity." Character-for-character match with the LOG-4443 spec. PASS.

## Check 3 — no unauthorized changes
Full `diff` reviewed hunk-by-hunk (9 hunks, lines 1/3/5/23/90/181/189/229/233). Every change traces to:
- F1 (line 23), F2 (lines 90/181/189), or
- standard repair bookkeeping: title/status v1→v2 labels (lines 1/3), licensing chain extended with LOG-4442/4443 (line 5), §8 chain-position update (line 229), v2 footer recording v1's hash (line 233).

No new design, no bar change, no invented numbers, no rewording outside the fix scope. PASS.

## Check 4 — v2 header discipline
v2 title: "Pre-registration DRAFT v2 (UNSIGNED)". Status line: "DRAFT v2 — UNSIGNED... F1–F2 repaired per LOG-4443... v1 SHA-256: 6f79f555e81f8e827ef6a3ca42a90313dea6715f905d192b20aa8c6a28e07e73 (v1 was NOT edited)." No pilot authorized. PASS.

## Non-blocking observation (not a discrepancy)
v2 line 205 (§6 risk 2, the self-attack log) retains the drafting lane's original counter prose ("the field is persisted, not analyzed; ... any future use needs its own pre-registration"). The LOG-4443 fix spec named only §2.2, §5 item 2, and §4.3 — all three are exact — and §6 is the attack narrative, not a permission grant. The binding fence lives in §2.2/§4.3/§5, which the verdict lane follows. Flagged for the verdict lane's awareness only; not a repair defect.

## Verdict: SIGN

All checks pass. The repair lane's claims are verified: F1–F2 applied exactly, v1 byte-identical, nothing else changed. v2 is authorized to proceed to CEO execution clearance. This lane takes no further action.

*Verified 2026-09-28 by the independent S6-3b delta re-verification lane. $0 compute; no model runs, no weights touched.*
