# S6-3d v1 → v2 Delta Re-verification (2026-09-28)

**Lane:** independent delta re-verification (fresh; did not draft, review, repair, or clear any S6-3d material).
**Target files:**
- v1: `research/innovation/S6-3d_PREREG_DRAFT_v1_2026-09-28.md` (pre-repair SHA-256: `9461c16a7d55166d4a9849e8aee68bd11c504295b8b5b91a2bd95866d81e5f36`; LOG-4456)
- v2: `research/innovation/S6-3d_PREREG_DRAFT_v2_2026-09-28.md`
- Fix spec: `experiments/protocols/REVIEWS/S6-3d_DRAFT_v1_LAW14_REVIEW_2026-09-28.md` (LOG-4457: ACCEPT-WITH-FIXES F1–F2)

## Check 1 — v1 immutability
`sha256sum` of v1 = `9461c16a7d55166d4a9849e8aee68bd11c504295b8b5b91a2bd95866d81e5f36` — **matches** the pre-repair hash exactly. v1 untouched. PASS.

## Check 2 — v2 hash (self-verified)
`sha256sum` of v2 = `1a49dd0c20d8a3a9f611c5726114a4f34f3c4b0bdff5581a107a8dcf09c0a1c0` — **matches** the repair lane's reported hash. PASS.

## Check 3 — F1 applied exactly as specified
Fix spec (LOG-4457 §3, F1): change "a fourth/fifth externally-computed attention-gate variant" to "a fifth externally-computed attention-gate variant" (line 232). No other change.
- v1 line 232 reads: "…a **fourth/fifth** externally-computed attention-gate variant (breaking point iv — the family closes with this wave)…"
- v2 line 232 reads: "…a **fifth** externally-computed attention-gate variant (breaking point iv — the family closes with this wave)…"

Exact one-word repair, correct location, verbatim match with the spec. PASS.

## Check 4 — F2 applied exactly as specified
Fix spec (LOG-4457 §3, F2): change "(LOG-4450's adjudication (d), judged principled)" to "(LOG-4450's adjudication (c), judged principled)" (line 216). No other change.
- v1 line 216 reads: "…the \"last externally-computed attention-gate variant\" fence (LOG-4450's adjudication **(d)**, judged principled)…"
- v2 line 216 reads: "…the \"last externally-computed attention-gate variant\" fence (LOG-4450's adjudication **(c)**, judged principled)…"

Exact one-word repair, correct location, verbatim match with the spec. PASS.

## Check 5 — no unauthorized changes (full diff, hunk-by-hunk)
The v1→v2 `diff` contains exactly **7 hunks**:
1. Line 1 — title label "DRAFT v1 (UNSIGNED)" → "DRAFT v2 (UNSIGNED)". *Standard repair bookkeeping.*
2. Line 3 — status line "DRAFT v1 — UNSIGNED" → "DRAFT v2 — UNSIGNED". *Standard repair bookkeeping.*
3. Line 5 — licensing chain extended: appends "→ LOG-4456 (S6-3d v1 draft) → LOG-4457 (Law #14 review: ACCEPT-WITH-FIXES F1–F2)". *Standard repair bookkeeping.*
4. Line 216 — **F1**. (See Check 3.)
5. Line 232 — **F2**. (See Check 4.)
6. Line 240 — §8 chain-position update: "Independent Law #14 review (separate lane)" → "Law #14 review complete (LOG-4457: ACCEPT-WITH-FIXES)". *Standard repair bookkeeping.*
7. Line 244 — footer: v1 drafting-lane footer → v2 footer recording "applied LOG-4457 F1–F2 verbatim only (v1 SHA-256 9461c16a7d55166d4a9849e8aee68bd11c504295b8b5b91a2bd95866d81e5f36; v1 NOT edited)". *Standard repair bookkeeping.*

Every hunk traces to F1, F2, or standard repair bookkeeping. **No new design, no bar change, no invented numbers, no rewording outside the fix scope.** PASS.

## Check 6 — v2 header discipline
- Title: "Pre-registration DRAFT v2 (UNSIGNED)". ✓
- Status: "DRAFT v2 — UNSIGNED"; explicitly "NOT a protocol. NOT executable." ✓
- F1–F2 repaired per LOG-4457 (licensing chain line 5). ✓
- v1 hash recorded in footer (line 244). ✓
- No pilot authorized (line 8: "No pilot is authorized by this draft"; line 240: "Pilot NOT authorized until all complete"). ✓
- No experiment number minted (only historical EXP100/101/102 references in the licensing chain). ✓

PASS.

## Verdict: SIGN

All checks pass. The repair lane's claims are verified: F1–F2 applied exactly as the LOG-4457 fix spec demands, v1 byte-identical to its pre-repair hash, and nothing else changed. v2 is authorized to proceed to CEO execution clearance. This lane takes no further action.

*Verified 2026-09-28 by the independent S6-3d delta re-verification lane. $0 compute; no model runs, no weights touched.*
