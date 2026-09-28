# S6-3c v1 → v2 Delta Re-verification (2026-09-28)

**Lane:** independent delta re-verification (fresh; did not draft v1, did not review it, did not repair it).
**Target files:**
- v1: `research/innovation/S6-3c_PREREG_DRAFT_v1_2026-09-28.md`
- v2: `research/innovation/S6-3c_PREREG_DRAFT_v2_2026-09-28.md`
- Fix spec: `experiments/protocols/REVIEWS/S6-3c_DRAFT_v1_LAW14_REVIEW_2026-09-28.md` (F1–F2, LOG-4450)

## Check 1 — v1 immutability
`sha256sum` of v1 = `1e52eaae577419cc94d863fa6a045a879294b384d6564e4cc6f180a9050df331` — **matches** the pre-repair hash exactly. v1 untouched. PASS.

## Check 2 — F1–F2 applied exactly as specified

- **F1** (Law #7 decision-proxy fence):
  - §5 item 8 (v2 line 199) appends: "The worksheet reports B-arm accuracy on fired items and on unfired items separately (both computable from per_item_records.csv; descriptive only — no verdict, bar, or routing consequence is pre-registered for this split)." — **verbatim match** with the LOG-4450 spec. PASS.
  - §4.3 verdict discipline (v2 line 185) appends: "The fired-vs-unfired B-accuracy split is the decision-proxy audit for the Law #7 readout-proximity risk (§6 risks #1–2): it is reported descriptively so the verdict lane can state whether the gate behaved as a near-decision proxy; it does not alter any step's routing." — **verbatim match** with the LOG-4450 spec. PASS.
  - No new passes, no new columns — both quantities derive from pre-registered `per_item_records.csv`; the existing **S6-3b F2-class no-extra-attention-column fence** in the same §4.3 sentence remains intact. PASS.
- **F2** (prose off-by-one): §0.2 leg 2 (v2 line 38) now reads "L20 sits **3 blocks below** the final block"; v1 (line 38) read "4 blocks below" — exactly the one-word change specified, applied at the correct location. PASS.

## Check 3 — no unauthorized changes
Full `diff` reviewed hunk-by-hunk (6 content hunks, lines 1–7/5/38/185/199/232/236). Every change traces to:
- F1 (lines 185/199), F2 (line 38), or
- standard repair bookkeeping: title/status v1→v2 labels (lines 1/3), licensing chain extended with LOG-4449/4450 (line 5), §8 chain-position update (line 232), v2 footer recording v1's hash (line 236).

No new design, no bar change, no invented numbers, no rewording outside the fix scope. PASS.

## Check 4 — v2 header discipline
v2 title: "Pre-registration DRAFT v2 (UNSIGNED)". Status line: "DRAFT v2 — UNSIGNED... F1–F2 repaired per LOG-4450... v1 SHA-256: 1e52eaae577419cc94d863fa6a045a879294b384d6564e4cc6f180a9050df331 (v1 was NOT edited)." No pilot authorized. PASS.

## Verdict: SIGN

All checks pass. The repair lane's claims are verified: F1–F2 applied exactly, v1 byte-identical, nothing else changed. v2 is authorized to proceed to CEO execution clearance. This lane takes no further action.

*Verified 2026-09-28 by the independent S6-3c delta re-verification lane. $0 compute; no model runs, no weights touched.*
