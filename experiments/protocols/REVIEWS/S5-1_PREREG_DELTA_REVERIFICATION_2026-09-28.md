# Law #14 Delta Re-verification — S5-1 Pre-registration DRAFT v2 (LOG-4397)

*Reviewer: Independent Scientific Mentor & Adversarial Reviewer (standing role; reports to the founder; binding verdict authority). Fresh reviewer — did not write the v1 draft, the v1 review, or the v2 repair.*
*Target: `research/innovation/S5-1_PREREG_DRAFT_v2_2026-09-28.md` (LOG-4396 repair of LOG-4395 ACCEPT-WITH-FIXES).*
*Method: read-only. Every number below recomputed from first principles (exact binomial, McNemar doubling convention) or verified by text search against the draft; nothing trusted from the repair lane's arithmetic. No model executed, no weights touched, $0 compute.*
*Date: 2026-09-28.*

## Verdict

**SIGN.** The v2 draft is authorized for CEO execution clearance. All four flagged fixes (F1, F2, F4, F6) verify against the binding LOG-4395 requirements; both open §6 items (5, 6) confirm held; every errata claim spot-checked matches an actual v1→v2 change. No third repair lane is needed. The pilot remains unauthorized until CEO execution clearance — this SIGN closes the Law #14 gate only.

## What was recomputed (independently, from primaries)

**F1 — Discovery bar.** McNemar exact, doubling convention, recomputed by hand:
- b=8, c=0 → p = 2·2⁻⁸ = 0.0078125 < 0.01 ✓ (minimum significant table)
- b=7, c=0 → p = 0.015625, n.s. ✓ (next table down correctly fails)
- b=6, c=0 → 0.03125; b=5, c=0 → 0.0625 (guard-contrast ladder intact)
- Family-wise: 1 − 0.99⁵ = 0.04901 ≈ 0.049 ✓ (matches draft's "≈ 0.049")

**F11 (spot-check) — Doubling arithmetic.** b=60, c=0 → 2·2⁻⁶⁰ = 1.7347×10⁻¹⁸ ≈ 1.73×10⁻¹⁸ ✓ (v1's 8.7×10⁻¹⁹ was wrong; v2 correct).

**F8 (spot-check).** log₁₀(16) = 1.2041 → "1.2 orders" ✓.

**F9 (spot-check).** 8 × 0.0474 = 0.3792 < 1 → stays inside the license ✓.

**F2 (spot-check).** 60 + 300 + 300 = 660 ✓; 660 + 150 = 810 ✓.

## What held (fix-by-fix)

- **F1 — HELD.** ALPHA_disc = 0.01 on the T(α)-vs-B(α) discovery contrast only; guards stay at 0.05. Decision table routes cleanly: step 4b (p ≥ 0.01 → PIVOT), step 5 (p < 0.01 for CONTINUE), step 6c (near-miss p ∈ [0.01,0.05) → PIVOT, "never CONTINUE-with-caveat"). Text search: no `p < 0.05` discovery language survives anywhere outside guard context. Step 6b's wrong-direction bar was also updated to p < 0.01 (v1 had 0.05 — the repair lane caught it; errata understated this, the change is correct). Adjacent-α replication accepted only as a pre-registered substitute (not taken). No escape hatch exists for a near-miss to become a CONTINUE.
- **F2 — HELD.** Single B run: §2.3 budgets 660 injection (60 B + 300 T + 300 B_wrong) + 150 reserve = 810 expected, 1300 hard cap; §0 cheapest-test arithmetic matches; pairing is B(i) vs T(α,i) vs B_wrong(α,i) throughout §3/§5. Text search for "five independent [B] replications" / "300 B passes" in the draft body: zero hits (the two grep hits are the errata quoting v1 and "five independent per-α tests" describing the grid — both legitimate).
- **F4 — HELD.** Step 3 verdict: "Refuted: the magic-strength rescue of the per-item static family is refuted *on the licensed five-point grid*" — no bare "KILL family" in the body (sole grep hit is the errata quoting v1). B_wrong-moved sub-case present: B_wrong(α) ≥ 6 anywhere while all T(α) < 6 → KILL stands, report must state nonspecific fragility observed.
- **F6 — HELD.** Step 0: (i) per-item B-decision agreement required when archived, else 36/60 aggregate with disclosed compensating-flip weakness; (ii) worksheet records the exact T(1.0)-vs-B flip count, nonzero <6 → foundation-wobble flag, sweep proceeds; (iii) HOLD → pre-registered diagnosis lane (re-hash weights vs LOG-331 pin, verify thread pinning, byte-compare prompts) — "never a silent re-run" stated verbatim. §5 item 6 worksheet spec carries all three.
- **§6 item 5 — HELD.** The linearity diagnostic remains a non-binding proposal; it appears nowhere in the §3 decision table and cannot change any verdict.
- **§6 item 6 — HELD.** The >1 threshold-account fence is airtight: §0 breaking point (ii), §3 step 3, and the §3 scope fence ("remains untested regardless of outcome") are mutually consistent; no verdict step can be read as killing the threshold account.
- **Errata integrity — HELD.** F3: body uses `constructor_manifest.json` in both locations (§2 frozen-spec, §4 guards); the one `constructor_manifest_run` hit is the errata quoting v1. F8/F9/F11 verified above. F5 (same-α in step 4a), F7 (HOLD+diagnose vs per-α exclusion), F10 ("targets" norm language), F12 (4th arm declined, interpretive fence in step 5), F13 (T-vs-B_wrong diagnostic-only in §2.4) all present as claimed.

## What broke

Nothing. No defect found in the delta scope. Two non-blocking observations (not defects, no action required):
1. §5 item 5's "135 cells" counts 3 strata × 5 α × 3 contrasts × 3 statistics — plausible, machine-written; outside the delta scope.
2. The F1 errata line understates the repair: step 6b's bar was also tightened 0.05 → 0.01. The change is correct and consistent; the errata is merely incomplete, not wrong.

## Authorization

This SIGN closes the Law #14 gate opened at LOG-4395. Next: CEO execution clearance, then the run (CPU, ≤810 expected, 1300 hard cap, $0; no GPU contact under any circumstance). The draft remains UNSIGNED — signing/minting the experiment number is the CEO's act, not this review's.
