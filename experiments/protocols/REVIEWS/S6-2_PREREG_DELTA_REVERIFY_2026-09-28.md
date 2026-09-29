# S6-2 pre-registration v2 — independent delta re-verification (2026-09-28)

**Reviewer:** Independent Scientific Mentor & Adversarial Reviewer (fresh lane — did not write v1, the Law #14 review, or the repair).
**Binding fix list:** `S6-2_PREREG_LAW14_REVIEW_2026-09-28.md` (LOG-4418) — verdict ACCEPT-WITH-FIXES, three binding fixes F1–F3.
**Scope of this lane:** verify the v2 repair only. Read-only; no edits, $0 compute, no model executed.

## Verdict: SIGN (binding)

All three Law #14 fixes are applied correctly and within scope. The repair is clean. The draft is ready for CEO execution clearance.

## Checks (each done independently, not trusted from the repair lane)

### v1 preservation — PASS
`md5sum` on `S6-2_PREREG_DRAFT_2026-09-28.md` returns `634327ed301a427c37f92d2da7a46ec0` — byte-identical to the md5 claimed in the repair lane's LOG-4419 entry and in v2's own errata block. The repair was copy-then-edit; v1 was not touched.

### Scope discipline — PASS
`diff` v1→v2 is exactly 7 hunks, all at the intended sites: (1) title v1→v2; (2) append-only errata block + status line; (3) §2.4 family-wise disclosure; (4) §3 arm-routing rule; (5) §3 step 1 delivery-probe scope; (6) §4.2 family-wise disclosure; (7) footer status update. No decision-table number, bar, gate, routing rule, or verdict mapping changed. The quantitative prediction (§0), the §3 steps 0–8 table, the McNemar bars, the movement gate (≥6), DELTA_BAR, ALPHA_disc — all untouched.

### F1 (strata enumeration, §3 arm-routing rule) — PASS
The arm-routing rule now reads, verbatim: "The three strata are explicitly **(aggregate / A-first / C-first)** — aggregate = all 60 items, A-first = the 30 A-first bench-pin items, C-first = the 30 C-first bench-pin items (S6-1 v2 precedent; F1, LOG-4418)." This reconciles with §2.2's unchanged "30 A-first / 30 C-first strata, bench pin" item split: aggregate is the full 60, the two named sub-strata are the 30/30 split. The step 7 / §5 "all three strata" requirement now has an explicit referent. No required change was skipped: F1 asked only for the arm-routing rule to name the three strata.

### F2 (family-wise disclosure, §2.4 + §4.2) — PASS
Both §2.4 and §4.2 now disclose the union bound as **≈2% family-wise** across the two conditional discovery claims (joint-vs-B contrast at 0.01; step-4 named L20-only positive at 0.01). The mutual exclusivity (L20-positive requires premise-fail → PIVOT, precluding the joint CONTINUE) is noted separately and NOT assumed in the union bound — the conservative reading the review demanded. A text search confirms zero remaining "1% family-wise" claims in v2. The review allowed either ≈2% disclosure or an explicit mutual-exclusivity argument; the repair took the first route and did it in both locations that carried the old disclosure.

### F3 (delivery-probe scope, §3 step 1) — PASS
Step 1 now enumerates the six injected (layer, arm) cells — (11, L11-only), (20, L20-only), (11, Joint), (20, Joint), (11, W-joint), (20, W-joint) — and declares that non-injected cells (e.g. (20, L11-only), (11, L20-only)) have **undefined** perturbation_ratio and are never probed. The literal-misread hazard (every non-injected cell tripping the >2-out-of-band HOLD) is closed.

### Repairer's noted ambiguities — confirmed within binding scope
1. §2.2's "30 A-first / 30 C-first" split left as-is: correct — F1 bound only the arm-routing rule, and the aggregate stratum is now defined there as all 60 items.
2. The review's non-binding observation recorded without change: correct — the review's own §"Non-binding observations" is explicitly "not verdict conditions," so no change was required.

## What this SIGN does and does not do
This SIGN clears the **repair only**: the three fixes are in, correctly placed, and nothing else moved. It is not an execution clearance and not a re-review of the draft's decision machinery (that was LOG-4418's lane). The draft remains DRAFT/UNSIGNED.

**Next per pipeline:** CEO execution clearance → experiment number minted. No pilot authorized; no GPU contact.
