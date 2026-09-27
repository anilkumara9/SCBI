# Law #14 Independent Adversarial Review — K3 Phase-1 Causal Rescue Screen Pre-registration DRAFT

**Reviewer:** Independent Law #14 Reviewer (reports to the founder; verdict binding).
**Target:** `experiments/protocols/K3_PHASE1_PREREG_DRAFT_2026-09-26.md` — DRAFT, UNSIGNED.
**Licensing:** founder ruling LOG-4359 (2026-09-26); source packet LOG-242; draft delivered LOG-4360.
**Date:** 2026-09-26. **Compute:** $0, CPU only, read-only on all signed protocols — no file edited by this review.

---

## Verdict: **SIGN-WITH-FIXES** — one blocking finding (F1), four non-blocking advisories (A1–A4).

The draft is faithful to the LOG-242 Phase-1 CEO packet, carries no invented numbers, passes the worth-it gate honestly, and guards the right things (Δθ=0, Law-#7 compliance, G4 byte-exact recompute, C2 procedure-validity with HOLD-on-NULL). It is **not** signed: the decision table (§3) uses three different undefined gating terms while the licensed operational definition sits unbound in §2.1 prose. F1 below is a mechanical, interpretation-free repair.

---

## Fidelity audit (all numbers traced to LOG-238–242 — PASS)

| Draft claim | Source | Status |
|---|---|---|
| g = 1.922505 ≥ 0.25 (candidate i), g = 1.061783 ≥ 0.25 (candidate ii) | LOG-241 (rounds verified LOG-4330) | ✓ |
| audit-value match 7.45e-9 ≤ 1e-6; \|g−1.061783\| = 9.56e-8 ≤ 1e-4 | LOG-241 | ✓ |
| k = 0/60 both candidates; CP95 [0.0000, 0.0596] | LOG-241 | ✓ |
| ≤240 expected passes; hard cap 400 | LOG-242 CEO packet | ✓ |
| McNemar exact + Tango 95% CIs; δ_min = 0.05 | LOG-242 CEO packet | ✓ |
| Arms C1 / C2 / K3i / K3ii | LOG-242 CEO packet | ✓ |
| G9 ledger 3/5; outstanding (4) CEO GPU clearance, (5) BK-04 booking | LOG-242 | ✓ |
| 30 3-hop items (bench composition) | LOG-234 plan shape (log l.4203); signed R1 plan l.190 — see A3 | ✓ (true; citation imprecise) |
| "signed EXP081 v2 donor centroid" | LOG-234 plan shape (log l.4203); "signed" basis LOG-182 spec (log l.4258) | ✓ |
| LOG-204 bridge demotion; K1 LOG-213/217; EXP082 LOG-278 | program record | ✓ |
| GPU queue K2→EXP083→EXP084→EXP086-B→EXP088→EXP087 | LOG-4358/4359 context; LOG-242 compute-order supersession noted, not edited | ✓ |
| No experiment number minted; DRAFT/UNSIGNED accurate; no capability claims | draft §6–§7 | ✓ |
| $0 compute for the draft; no signed-protocol edits | draft §4, §7; file listing confirms new file only | ✓ |

No invented numbers found. No silently widened claims found. The licensed CONTINUE/KILL/Inconclusive-HOLD readings are carried in substance from LOG-242.

## Worth-it gate (Law #15 — PASS)

Exact question (compliant construction causally sufficient vs label-leakage null), decision it changes (KILL / CONTINUE / Inconclusive-HOLD, each named), cheapest falsifying test (the screen itself with C2 as procedure-validity falsifier; Phase-0 at $0; no archived route licenses a causal conclusion), quantitative prediction (≥1 supported candidate rescues at McNemar-exact significance, effect ≥ δ_min = 0.05, C2 meaningful), breaking point (compliant NULL + C2 clearly rescues → KILL; C2 NULL → never KILL on a broken control) — all present, all honest. "Survival here is not proof" is correctly stated.

## Budget arithmetic (recomputed — PASS)

5 injection conditions (C1-i, C1-ii, C2, K3i, K3ii) × 30 items = 150 injection passes + 30 baseline passes = **180 expected ≤ 240**; hard cap 400 intact. Licensed figures check out under the natural reading. (Decomposition shown in the signed version — see A2.)

## Guards (PASS)

Δθ=0 (weight hash pre == post, Law #13); Law-#7 compliance re-asserted under rules C-a–C-e with zero test-label contact, construction-identity guards, g ≥ 0.25 floor re-checked; G4 per-item (id,t,f) recomputed byte-exact vs the signed pre-audit JSON with nothing inherited (Law #3); G5 zero forward-invocation; C2's procedure-validity role correctly makes Inconclusive-HOLD the verdict on a broken control. The 0.9-bar caveat mechanism is real and registered (R1 plan ll. 393–401, 636: caveat attaches to any Phase-1 CONTINUE verdict; candidate-(ii) firing = observation against the signed audit, Phase-1-gating) — see A4 for the citation fix.

---

## Blocking finding

### F1 — Decision-table gating terms undefined in the binding table (location: draft §3)

**Defect.** §3's decision table — the binding artifact an executor reads — uses three different undefined terms: row 1 fires on "C2 is meaningful", row 2 on "C2 clearly rescues", row 3 on "C2 NULL". None is operationalized in §3. The licensed operational definition exists but sits unbound in §2.1 prose: **cell (1)** = Tango 95% CI lower bound L > δ_min = 0.05 (signed R1 plan ll. 454–455: "≥1 candidate arm lands in cell (1) (Tango L > 0.05)"; l.460: "C2 in cell (1) (procedure valid, option-informed rescue at meaningful magnitude)"), with the licensed third reading "C2 outside cell (1) → no licensed verdict" (draft §2.1).

**Consequence.** Without the binding, the marginal-C2 band (C2 rescues weakly — e.g., McNemar-significant but Tango L ≤ 0.05, or effect < δ_min) has no clean routing: row 2 requires "clearly", row 3 says "NULL", and "meaningful" ≠ "clearly rescues" leaves row 1 vs row 2 ambiguous. An executor facing marginal C2 with all-compliant-NULL would have to invent the verdict — a Law #9 violation manufactured by the pre-registration itself. Same defect class as the R4 review's F1 (dead zone).

**Required fix (mechanical — no interpretation needed).** Rewrite the §3 table rows in cell-(1) terms, verbatim in substance from §2.1's licensed readings:

| Condition | Verdict |
|---|---|
| ≥1 compliant candidate in cell (1) AND C2 in cell (1) | **CONTINUE** — the autonomous-mechanism reading survives this falsifier *only* |
| All compliant candidates outside cell (1) AND C2 in cell (1) | **KILL** — re-scope to label-assisted steering |
| C2 outside cell (1) | **Inconclusive-HOLD** — regardless of the compliant arms; procedure not validated, no verdict licensable |

Retain the cell-(1) definition (Tango L > 0.05) as a binding definitional line immediately above the table. This partitions the outcome space totally with no overlap and no dead zone, and it is a tightening of the LOG-242/LOG-234 licensed readings, not a rewrite (KILL still requires a clearly-valid procedure; marginal C2 still cannot license KILL).

---

## Non-blocking advisories

- **A1.** "Five permitted verdicts only" (draft §0, §3, §4) is never enumerated. In the signed version, list the five permitted verdicts carried from LOG-240/242.
- **A2.** Budget: the licensed ≤240 / cap-400 figures are correct; show the recomputed decomposition (5 conditions × 30 items + 30 baseline = 180) in the signed version so the number is self-verifying.
- **A3.** Citation precision: the "30 3-hop items" bench composition traces to LOG-234's plan shape (log l.4203) and the signed R1 plan (l.190), not to LOG-242. The draft's blanket "all values from LOG-242" attribution should cite LOG-234 for that datum.
- **A4.** The §4 guard phrase "the pre-registered Phase-1 caveat protocol governs" should point at the exact registered text — R1 plan ll. 393–401, 636 (0.9-bar caveat attaches to any Phase-1 CONTINUE verdict; candidate-(ii) firing is Phase-1-gating) — rather than a vague protocol name.

---

## Release conditions (unchanged by this review)

This SIGN-WITH-FIXES does not sign anything, authorize GPU, book BK-04, mint an experiment number, or commission the separate signing lane. After F1 is repaired, the draft requires a fresh independent review (repair re-verification, delta-only on F1) before SIGN. Execution remains conditional on: CEO GPU clearance, BK-04 booking, K2 executed + Sprint-3 pilots cleared, sequencing behind the founder GPU queue.

---

*Review completed 2026-09-26. Binding verdict: **SIGN-WITH-FIXES**.*
