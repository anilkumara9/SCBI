# Fix-Verification — H4 (PTTSC) Pre-registration Repair

**Lane:** LOG-4550 (independent fix-verification only — this lane neither drafted nor repaired the document)
**Date:** 2026-09-29
**Document under verification:** `research/prereg/EXP_PREREG_H4_PTTSC_2026-09-29.md` (as repaired by LOG-4549)
**Underlying review:** `research/reviews/LAW14_REVIEW_H4_PTTSC_2026-09-29.md` (LOG-4548, SIGN-WITH-FIXES, 5 required fixes)

**Numbering convention:** the review's §7 refers to the KILL fence as "FIX-4" while its required-fixes section numbers it FIX-5. The repair lane followed the required-fixes section's authoritative numbering; this verification uses the same (FIX-1 = construct validity, FIX-2 = extraction, FIX-3 = parse scope, FIX-4 = deviation count, FIX-5 = KILL fence).

**Method:** exact-text search against the repaired file; no re-review of the whole document.

## FIX-1 (construct validity) — PASS

- Closing instruction found verbatim **2×**, in both templates:
  - §3.4 executor: "Develop the outline above into a final answer. Reply with the name of the higher-ranked entity and nothing else."
  - §3.5 baseline: "Answer the question above. Reply with the name of the higher-ranked entity and nothing else."
- Parse rule (§3.5) matches the review's required wording: "decode the newly generated tokens only (prompt tokens excluded — the EXP108 convention); strip whitespace and trailing punctuation (.,;:!?); case-insensitive compare against the item's two bench entity names (bench keys "A" and "C"): exact match → that entity is the vote; otherwise the generation is **UNPARSEABLE** and its vote is dropped."
- Labels re-pinned to target entity name (§3.2): "bench ground-truth labels (the target entity name, i.e. the bench's "A"-keyed entity) are used **only at metric time**".
- Tie-break re-pinned to foil entity (§3.6): "Ties (2–2, or any even split of parseable votes) are broken deterministically toward the **foil entity** (the bench's "C"-keyed entity — conservative, matching the program precedent in the H1 prereg §3.3)."
- Banned remnants (grep, case-insensitive): "single letter" = 0, "first alphabetic" = 0, "Reply with a single letter" = 0.

## FIX-2 (deterministic outline extraction) — PASS

- §3.3 contains the exact first-occurrence-marker algorithm: "scan the planner output left to right; record the first occurrence position of each literal marker `1.`, `2.`, `3.`, `4.`; for k=1..4, outline_k = the substring from the end of marker `k.` to the start of the next marker occurrence in position order (or end of output), stripped; text before the first marker (preamble) is discarded; a missing marker yields an empty outline; then drop empties and exact duplicates; planner-valid iff ≥ 2 distinct non-empty outlines remain; outline_idx for seeding is the 0-based position in the post-dedup list."
- Covers preamble, repeated/in-text markers, missing markers, and seed indexing with no residual ambiguity. DoF table updated with a matching "Outline extraction" row, plus the "Executor outline count" row (develop exactly the extracted outlines, 2–4) the review §5 requested.

## FIX-3 (parse scope + tripwire denominator) — PASS

- New-tokens-only scope pinned in §3.5: "decode the newly generated tokens only (prompt tokens excluded — the EXP108 convention)" — and in the DoF table: "Parse rule | newly generated tokens only; strip whitespace/trailing punctuation; case-insensitive exact match vs the item's two bench entity names (bench keys "A"/"C"); else UNPARSEABLE, vote dropped".
- Tripwire denominator clarified (§3.8): "if ≥ 50% of executor + baseline vote-generations across the run are UNPARSEABLE (planner generations are covered by the planner-valid rule, not the parse rule) → **RUN-INVALID (apparatus failure)** regardless of n_valid."

## FIX-4 (deviation count) — PASS

- §8 header reads: "**Deviations [FACT]:** three deviations from the dossier, recorded here, the first two mathematically required:" followed by item 3, the pilot scope: "**Pilot scope (§3.2/§7):** the dossier specifies n=60; this lane registers a 20-item pilot (first 20 in bench build order) as the honest CPU scope — mechanical and cherry-pick-free, but unrepresentative of the 60-item bench (planet-only: 15 planet-2hop + 5 planet-3hop, 0% elemental). A full-n=60 run would be a separate pre-registered lane with re-derived bars, not a re-run of this one."

## FIX-5 (KILL scope fence) — PASS

- §4 KILL row: "**KILL** | Planning adds nothing at this pilot scale on this pilot bench. The coordinator axis is retired for the piloted scope (a full-bench test remains a separate, unlicensed lane)."
- §6 KILL row: "**KILL** | Planning adds nothing at this pilot scale on this pilot bench. The coordinator axis is retired for the piloted scope."
- §2 Decision-changed KILL: "(planning the budget adds nothing at this pilot scale on this pilot bench; the coordinator axis is retired for the piloted scope)".
- Grep for the literal unqualified phrase "dead for this task class": 0 occurrences.
- Non-blocking observation: §8 also carries the sentence "A KILL retires the *TTS/coordinator axis for this task class*, not the summit program." This is interpretive scope wording, not a KILL-row reading, and does not use the unqualified "dead for this task class" phrasing the required fix names. The repair lane satisfied the stated verification criteria verbatim.

## Spot-checks (unchanged by repair) — all intact

- **McNemar table:** all seven values present and matching the review's independent recomputation — (5,0)→0.0312, (6,0)→0.0156, (6,1)→0.0625, (7,1)→0.0352, (7,2)→0.0898, (8,2)→0.0547, (9,2)→0.0327.
- **Budget-as-treatment design:** §3.7 unchanged — matched executor budget (4×48 tokens/arm), planner pass (≤160 tokens) as the treatment.
- **Seeds:** executor `2000 + 10*item_idx + outline_idx`, baseline `3000 + 10*item_idx + sample_idx`, disjoint streams, pinned.
- **Hash pins:** backbone `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed` (LOG-331); instance records `47281cd3dc243369be0aa5be2345663b752cdb4a329a16a37f08da5717230585`.
- **Determinism pins:** `model.eval()`, `torch.no_grad()` around all forward passes, `device_map="cpu"`, float32.

## Verdict: ALL-FIXES-VERIFIED

All five required fixes are present in the repaired exact version with the review's required wording. **The LOG-4548 review is hereby upgraded to SIGN.** This lane approves nothing further: execution and experiment-number minting remain the CEO launch decision.

**Boundary:** verification only; no edits to the prereg, no approval of execution, no experiment number minted, no follow-ups dispatched.
