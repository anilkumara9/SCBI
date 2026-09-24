# Adversarial Review — K3 Compliant-Bridge Plan (LOG-234)

**LOG-235 · Track-7 (adversarial review) · 2026-09-23**
**Target:** `research/analysis_plans/K3_COMPLIANT_BRIDGE_PLAN_LOG234_2026-09-23.md` (FROZEN)
**Reviewer independence:** no involvement in writing the plan; author claims treated as untrusted and re-verified against primary artifacts.
**Method:** full read of the plan; read of `research/LAW15_RETROACTIVE_AUDIT_2026-09-23.md` (Law #15 record), `research/analysis_plans/LAW7_BRIDGE_AUDIT_REPORT_LOG197_2026-09-23.md`, `research/analysis_plans/H7_DECISION_BRIEF_LOG232_2026-09-23.md`; corpus grep for prior computation of candidate (i)'s geometry; line-level verification of `experiments/runs/exp077/run_exp077.py` citations; value-level verification of `experiments/protocols/C-A_DONOR_TRANSFER_PREREG_SPEC_V2.md` §3.1/§3.3/§4.1 and `experiments/protocols/C-A_PREAUDIT_2026-09-23.json`. No code executed beyond read-only JSON inspection; no weights loaded; no GPU.

---

## Verdict: SIGN-WITH-FIXES

The plan is sound in design, honest in its disclosures, and its falsification architecture is correctly scoped. Four mechanical fixes are required before SIGN — all wording/table-precision (F3-class), none design-level. No fix alters an endpoint, margin, environment, or the compliance rule's substance.

---

## Fix list (mechanical, precisely located)

### F-235-1 — §3.1 (C-a)/(C-b) wording contradicts its own operationalization (§4 E-K3-1)

**Location:** §3.1, rules (C-a) and (C-b); §4 E-K3-1.

**Defect.** (C-a) as written: "No id in I(C) is the token id of **any test item's** target-answer token." Read literally (bare token-id reading), candidate (i) **fails** (C-a): the test entity pool is 10 shared entities ({Mars, Venus, Jupiter, Saturn, Mercury, Iron, Gold, Silver, Bronze, Steel} per the v2 spec §3.2) reused across 60 items, so every premise entity token id (e.g. Mars as B in item 3) is also some other item's target-answer token id (e.g. Mars as A in item 7 — confirmed in the pre-audit `per_item` records). Yet §3.2's parenthetical ("B_i and C_i are never **item i's own** target or foil") and E-K3-1 ("asserts {B_i, C_i} ∩ {target_i, foil_i} = ∅ **per item**") operationalize a per-item role-relative reading. An executor implementing (C-a) literally would produce a spurious compliance FAIL on the primary gate.

**Required fix.** Reword (C-a)/(C-b) to the per-item role-relative reading the plan already intends, and state the rationale once so no executor re-litigates it:

> (C-a) No id in I(C) is the token id of an entity **in its role as** the evaluated item's target-answer token (per-item role-relative). (C-b) likewise for the foil/candidate-option role. Cross-item entity reuse over the shared 10-entity pool is expected and carries no role information: the unembedding row W_U[tok] is role-free; Law #7's target is the answer key (the per-item role mapping), which never enters the construction.

And in E-K3-1, add one **descriptive** (non-gating) readout: report the count of premise token ids that coincide with some *other* item's target/foil token id (expected > 0; records the cross-item collision openly rather than hiding behind the per-item reading).

**Why this is a clarification, not a dodge (reviewer's ruling):** Law #7 (AGENTS.md) prohibits exposing "test set labels, targets, or future instances" to the construction. The *label* is the role mapping (which entity is target of item j); W_U[Mars] contains no role information. The bare-token-id reading would make *any* construction over test-pool entities non-compliant in principle — including the donor-pool-disjointness logic the program already signed — so the per-item role-relative reading is the only workable operationalization of the law's intent. The fix aligns the rule text with the already-intended operationalization.

### F-235-2 — §7.2 verdict table is not exhaustive as claimed (§6 L3)

**Location:** §7.2, Phase-1 program verdict table; §6 L3 outcome-partition claim.

**Defect.** The cell {≥1 candidate RESCUES (cell 1), C2 p ≥ 0.05 (NULL)} has no row. Row 1 covers RESCUES only with "any [C2 cell] with p < 0.05". A concurrent-C2-NULL alongside a candidate rescue is empirically unlikely (C2 rescued +10pp officially at this config) but is exactly the kind of procedure-validity failure the concurrent control exists to catch — and §6 L3 claims every {candidate cell} × {C2 cell} × {guards} cell maps to exactly one verdict category.

**Required fix.** Add one row to §7.2:

| ≥1 candidate RESCUES (cell 1) | p ≥ 0.05 (NULL) | **Inconclusive** → HOLD — positive control failed; procedure validity not established; neither CONTINUE nor KILL licensed |

This mirrors the plan's own row-3 logic (C2's rescue is load-bearing for KILL; symmetrically C2's failure blocks CONTINUE). All other cells verified mapped; Phase-0 table §7.1 verified exhaustive (identity mismatch routes through G2 FATAL → the guards-fail Refuted row).

### F-235-3 — §5 "exactly EXP081's T1 comparison" overstates endpoint identity

**Location:** §5, "Relationship to EXP081 (binding)".

**Defect.** K3ii-vs-C1 is the same *arm pairing* as EXP081's T1, but not the same endpoint machinery: the signed v2 T1 (per the LOG-203 Law #14 correction, Law #15 audit) uses the F1 agreement rule, while K3's §5 cells use McNemar + Tango L > δ_min. The implication the plan needs (K3-NULL ⇒ T1 fails) holds in the safe direction — McNemar p ≥ 0.05 means no directional rescue evidence at all, which fails T1 under either endpoint — but "exactly" is false as written.

**Required fix.** Replace with: "K3ii-vs-C1 is the same arm pairing as EXP081's T1 (C3 vs C1) — intentional (cheapest screen). K3's decision uses its own §5 cells; a K3 NULL implies T1 failure under either endpoint (no directional rescue evidence)."

### F-235-4 — §5 pre-registered caveat should name the token-prior confound

**Location:** §5, entity-similarity-leak control, pre-registered reading.

**Defect (Law #2 completeness, minor).** The plan carries the stratum-concentration caveat for a K3ii rescue but does not name the v2 spec's own sharpest honest characterization of what b̂_D *is*: "the donor bank's *token-prior direction* — 'usually-right minus usually-wrong' in unembedding space" (v2 spec §4.1 [PROPOSITION], LOG-144 §a). The similarity channel (s_t/s_f) is the same null family and is re-verified, so nothing is hidden — but the Phase-1 report's CONTINUE reading should attach the confound by name.

**Required fix.** Append to the §5 pre-registered reading: "Any K3ii CONTINUE reading additionally carries the v2 spec's token-prior-direction characterization (donor bank's 'usually-right minus usually-wrong') as part of the pinned caveat — attribution to EXP081's T3/T4/T5."

---

## Author-flagged attack points — independent assessment

### (1) §3.1 rule C-e and the rank-relation-informedness challenge (§12)

**Assessment: the construction is genuinely Law-#7-compliant on the letter; the §12 challenge is honestly disclosed, not smoothed over; not a design defect.** The rank relation used for orientation (B outranks C) is present-instance prompt content, not a label, option token, or future instance — Law #7's letter (AGENTS.md Law 7; LOG-197 §5 operational rule, quoted faithfully) governs labels/targets/future instances, not prompt relations. The construction never touches the A/C option fields; the bank-level aggregation makes the direction fixed and identical for all 60 items, so a rescue would be a property of the *direction*, not item identity — the falsifier is valid. The §12 note records the "relation-informed though label-free" objection verbatim with the plan's standing answer and leaves a sign-flip-sensitivity follow-up to the Law #14 reviewer's ruling (new number per Law #4 if pursued). That is the correct handling. The one real problem in this area is the (C-a)/(C-b) wording ambiguity → **F-235-1**.

### (2) No-data-contact claim on candidate (i)'s geometry

**Verified.** Corpus search for any prior computation of the bank-level premise-rank direction b̂_P = normalize(Σ(W_U[B_i] − W_U[C_i])) returned only the K3 plan itself and the LOG-234 dispatch entry in `reports/research_log.md` (which describes the plan, not a computation). The nearest neighbor, G1's b_mean = normalize(Σ b_i) over per-item *option-informed* bridges, is a different object (option-token differences, not premise-pair differences). No cosine, norm, or compliance fact about b̂_P exists in the signed corpus. The plan correctly delegates final corpus-search confirmation to the Law #14 reviewer pre-SIGN (§3.4).

### (3) Phase-0 KILL rule: "Underdetermined on the construction question"

**Sound; not a disguised negative.** The plan explicitly distinguishes the two questions: "Reported as Underdetermined on the construction question, **never as a negative on the rescue question**" (§9). The GPU-INFEASIBLE consequence follows directly (a rescue screen with no construction to screen is infeasible as designed — Law #15 Q3). The "narrowed §H7 demotion hardens" consequence is quoted as the LOG-232 §4 contingency, conditional on the CEO accepting that draft brief — the plan does not decide §H7 itself. This is the correct epistemic handling.

### (4) Phase-1 verdict mapping vs undischarged A2 (mid-network propagation)

**No overreach.** The KILL conjunction (all candidates NULL ∧ C2 in cell (1)) is scoped to H_compliant at the pinned configuration (A6: α = 0.50, l* = 20 — not tuned, not swept). The concurrent C2 uses the *identical* hook and α; its cell-(1) rescue discharges procedure-validity and bench headroom at this exact configuration, which is precisely what the KILL conjunction needs. A2 (undischarged) caps only the *causal-upshot* license — bypass-vs-routing is K2's question, honestly disclosed in §6 L4 — not the rescue endpoint. The verdict is "Not supported (H_compliant)", a verdict on the registered hypothesis, not a universal mechanism proof; the consequence is re-scope to label-assisted steering with a HOLD escape for every inconclusive cell. The mapping mirrors EXP081's T2 headroom-gate logic and is coherent.

### (5) Donor centroid reuse — genuine compliance or inherited option-informedness?

**Genuinely compliant on the signed record; no inherited option-informedness.** Re-verified against primary artifacts:
- v2 §3.3 Law #7 statement quoted faithfully: donor labels are support-side construction material only; test items unlabeled at intervention time; the fixed bank-level centroid is identical for all 60 items.
- C3 = "same-relation, entity-disjoint (primary arm)", 20-donor pinned table (v2 §3.1, l. 203); sum-of-differences-then-normalize (v2 §4.1); donor pool (25 support entities) disjoint from the 10-token test pool by construction (v2 §3.2).
- Identity anchors verified in `C-A_PREAUDIT_2026-09-23.json`: g_D = 1.0617830595495654 (plan: 1.061783 ✓); s_t/s_f max |cos| = 0.0918 < 0.1 across all 60 items (plan's "all |cos| < 0.1 [FACT — computed]" ✓).
- The reuse is verbatim with FATAL identity re-verification (E-K3-3(b), §8 G2): any drift means the rebuild is not the signed construction. Law #4 respected — no re-design, no re-litigation of v2's signed Law #7 ruling. The v2 spec's own token-prior confound is the sharpest residual worry and is now covered by **F-235-4**.

---

## Standard checks

- **Required sections:** all present — §0 Law #15 four answers; §1 standing context; §2 data sources; §3 Phase-0 constructions; §4 endpoints; §5 Phase-1 design; §6 license L1–L4; §7 verdict tables (7.1/7.2); §8 guards + §8.1 env pin; §9 consequences; §10 execution protocol; §11 scope exclusions; §12 knowledge-protocol obligations.
- **Endpoints exact with kill criteria:** E-K3-1–E-K3-5 exact (token-id audit, g ≥ 0.25 to 6dp, identity tolerances 1−1e-6 / 1e-6 / 1e-4, Tango + δ_min = 0.05, McNemar via `scipy.stats.binomtest`); kill criteria in §6 L3 and §7.2. Cell (4) (directional, L ≤ δ_min) correctly held as Inconclusive, never converted to a negative.
- **Verdict table exhaustive / Inconclusive reachable:** §7.1 exhaustive (verified above); Inconclusive reachable in both phases. §7.2 had one unmapped cell → **F-235-2**.
- **Guards FATAL where claimed:** G1–G11 all carry FATAL/halt; G9's five-condition release chain is binding; §7.2's "guards-fail → Refuted takes precedence" (Law #13) is consistent with §8.
- **Env pin exact:** torch 2.14.0+cpu / transformers 5.17.0 / numpy 2.5.3 / scipy 1.18.1; snapshot `9879c9b5f8bea9051dcb0e68dff21493d67e9d4f`; Δθ=0 formulation named (`run_exp077.py` ll. 166–172 — verified: `def get_hash` at l. 167, SHA-256 over sorted `state_dict()` tensors, CPU, float32 bytes) with archived-hash cross-check. Matches LOG-197 precedent.
- **No GPU/forward-pass before SIGN:** §0 scope banner, §8 G5/G9, §10 ("Phase 1 does not exist until the §8 G9 release chain completes"). Phase 0 = 0 forward passes; Phase 1 ≤ 240 (hard cap 400, BK-04).
- **No signed-protocol edits:** §11 explicit; candidate (ii) verbatim reuse; "repair = new plan" (Law #4) stated in §3.1/§4.
- **Scope discipline:** §11 binding exclusions (no EXP070 endpoints, no novelty claim — N1 stands, no EXP081 override, no third construction, no α/layer/hook sweep). The plan does not pre-decide §H7 — it implements the LOG-232 contingency as quoted, flagged as DRAFT for CEO acceptance.
- **Standing lessons:** official EXP077 record cited for C2's rescue precedent only (b=6, c=0, ΔM=+0.1000, p=0.03125 — never cross-compared with smoke); smoke archive used solely for item-definition byte-consistency (definitions, not results); EXP070 excluded from all vector endpoints (§0/§1/§6 A4); banned words ("promising"/"interesting"/"worth another experiment") appear only inside the ban statements; five permitted verdicts used throughout; evidentiary levels kept separate (Phase-0: L0/L1; Phase-1 rescue: Level 1 narrow; "never Level 2/3" explicit).
- **Law #2 (no fabrication by omission):** the plan discloses the full tilted history (LOG-197 Q1/Q2, K1 + EXP082 killing both tilt accounts, narrowed demotion per LOG-232, full reversal contingent on K3), the undischarged A2, the §12 rank-relation challenge, the stratum-concentration caveat, and the donor bank's degeneracy-trap warning. Candid throughout.
- **Line citations spot-checked:** decision rule ll. 669–682 verified (`def eval_item` l. 669; argmax l. 680); bench loops cited ll. 586–636 — actual four loops span ~ll. 592–638 (comment header l. 585), F3-class edge drift at most; §10 step 2 already requires the executor to record exact quad-loop sub-ranges, so no fix needed. `get_hash` ll. 166–172 verified.
- **Factual claims re-verified:** 3-hop quad structure (A,B,C,D_ent; rank A>B>C>D_ent; options A and D_ent; item `"C": D_ent`) confirmed in `run_exp077.py`; 2-hop has no non-option pair (options A,C; single non-option B) — the "3-hop-only bank" scope fact holds; Tango guard rows match LOG-197 E4 exactly; α = 0.50 / l* = 20 / last-token residual hook match EXP077 C8 config per LOG-197 E2.

---

## Notes (observations, not fixes)

1. The plan's §1 inherits LOG-197's model-pin observation implicitly (410m-only constructions); the E1 caveat about 160m vs 410m numerics does not affect K3 since all K3 constructions and the bench are 410m-pinned. Correctly handled.
2. §4 E-K3-4's "Phase-1-gating" clause for a candidate-(ii) 0.9-bar firing is unreachable given E-K3-3(b) passes (the signed s_t/s_f profiles re-verified to 1e-6 cap |cos| at 0.0918) — redundant but harmless; the author's parenthetical already says so.
3. Mixed RESCUES + NULL across candidates → CONTINUE is the correct existential reading of H_compliant ("a Law-#7-compliant bridge rescues"), with per-candidate readings recorded separately. No change.

---

## Bottom line

SIGN-WITH-FIXES. Apply F-235-1 through F-235-4 (all mechanical, precisely located above), then the plan is cleared for Law #14 SIGN and Phase-0 execution. The design's falsification logic is sound: the compliance rule is operational and statically checkable, the Phase-0 gate is $0 and correctly scoped as Underdetermined-not-negative, the Phase-1 KILL conjunction is properly conditioned on the concurrent positive control, and the donor reuse inherits no option-informedness. The plan's honesty about its own weak points (§12 challenge, A2, stratum caveat) is exactly what the adversarial standard requires.

*Reviewer: Track-7 (LOG-235) · 2026-09-23 · No code executed, no weights loaded, no GPU. Report filed; `reports/research_log.md` untouched per instructions (Lead owns the log).*


---

## LOG-236 — Targeted Law #14 re-verification of the LOG-235 fixes

**Track-7 (adversarial review) · 2026-09-23 · Reviewer independence: no involvement in writing the plan or applying the fixes; all claims treated as untrusted.**
**Method:** line-level read of `research/analysis_plans/K3_COMPLIANT_BRIDGE_PLAN_LOG234_2026-09-23.md` against the four F-235 fix specs; consistency sweep of every section touching the compliance rule, §7.2, and §5; grep for banned-verdict language and banner integrity. No git baseline exists for the plan file (untracked), so collateral-edit verification was done against the pre-fix text quoted in this report's fix list rather than a byte-diff — a noted limitation. No code executed, no weights loaded, no GPU.

### Per-fix verification

- **F-235-1 (§3.1 C-a/C-b + §4 E-K3-1): VERIFIED PRESENT AND FAITHFUL.** (C-a)/(C-b) reworded to the per-item role-relative reading with the exact operational form "{premise ids on item i} ∩ {target_i, foil_i} = ∅ per item". The role-free-row / answer-key-role-mapping rationale appears exactly once (§3.1, lines ~178–184: unembedding rows role-free; Law #7's target is the answer-key role mapping). E-K3-1 carries the new descriptive, non-gating, [OBSERVATION]-tagged cross-item collision count ("bank premise entities whose token id coincides with *some other* item's target/foil token id — expected nonzero on the shared 10-entity pool"). No contradiction with E-K3-1's per-item assertion, §3.2's "item i's own target or foil" compliance argument, §3.3's donor disjointness (C-d, second clause — separate, pre-existing, stricter), §8 G1, or §10 step 3. All checked consistent.
- **F-235-2 (§7.2): PRESENT, BUT DEFECTIVE — see verdict.** The new row exists verbatim as specified: "| ≥1 candidate RESCUES (cell 1) | cell 4 or p ≥ 0.05 | Inconclusive → HOLD (positive control failed; neither CONTINUE nor KILL licensed — LOG-235 F-235-2) |". However, pre-existing row 1's C2 condition — "any with p < 0.05" — was not narrowed, and now overlaps the new row: under §5's cell definitions, C2 in cell 4 has McNemar p < 0.05, so the outcome cell {≥1 candidate RESCUES, C2 cell 4} fires BOTH row 1 (→ CONTINUE) and the new row 2 (→ HOLD), with no precedence rule resolving it (only guards-fail has a stated precedence). This violates the §6 L3 outcome-partition claim ("every {candidate cell} × {C2 cell} × {guards} cell maps to exactly one of the five verdict categories"). Note row 3 already uses the precise phrasing the repair needs — "cell 1 (L > 0.05)".
- **F-235-3 (§5): VERIFIED.** "exactly EXP081's T1 comparison" is gone; §5 now reads "K3ii-vs-C1 uses the same arm pairing as EXP081's T1 comparison; K3's own §5 cells apply (v2's signed T1 uses the F1 agreement rule — the needed implication K3-NULL ⇒ T1-fails holds in the safe direction)". The surviving "Exactly EXP081 v2 §3.1/§4.1" elsewhere (§3.3) concerns construction identity, was pre-existing, and is outside this fix's scope.
- **F-235-4 (§5): VERIFIED.** The K3ii CONTINUE caveat now names the token-prior-direction confound explicitly: "the donor centroid may encode a 'usually-right minus usually-wrong' token-prior direction rather than a transferable mechanism — the rescue reading stays with EXP081's T3/T4/T5, not with K3" (tagged LOG-235 F-235-4, Law #2).

### Remaining checks

- **Collateral edits:** none detected. All pre-fix quotations in this report match the surrounding text unchanged (row-1 wording per the fix-list quote; §3.2 parenthetical; E-K3-1 assertions; §5 arms/endpoints/cells; §0/§6/§8/§9/§10/§11/§12 spot-checked). The only changes are the four fixes. (Limitation: no byte-diff baseline — see Method.)
- **Banned-verdict language:** none introduced. "Promising"/"interesting"/"worth another experiment" occur only inside the ban statements (§1, §8). New text uses only the five permitted verdicts.
- **FROZEN / DO NOT EXECUTE banner:** intact — title "FROZEN PLAN", the pre-SIGN blockquote, and the bottom banner (2× "DO NOT EXECUTE"); footer retains "FROZEN pending independent Law #14 review SIGN".

### Verdict: REVISE

F-235-1, F-235-3, F-235-4 verified faithful; F-235-2 present but its insertion broke §7.2's precedence. **Precise location of the defect:** `research/analysis_plans/K3_COMPLIANT_BRIDGE_PLAN_LOG234_2026-09-23.md`, §7.2 table, row 1, C2-condition cell — "any with p < 0.05". **Minimal repair (one cell, F3-class):** narrow row 1's C2 condition to "cell 1 (L > 0.05)" (mirroring row 3's existing precise wording). After that change the Phase-1 table is again exhaustive and mutually exclusive: {RESCUES, C2 cell 1} → CONTINUE; {RESCUES, C2 cell 4 or NULL} → HOLD; {all NULL, C2 cell 1} → KILL; {all NULL, C2 cell 4 or NULL} → HOLD; {≥1 CELL-4, none RESCUES} → HOLD; guards-fail → Refuted. The plan is NOT released for Phase-0 execution until this repair is applied and re-verified. `reports/research_log.md` untouched per instructions (Lead owns the log).

*Reviewer: Track-7 (LOG-236) · 2026-09-23 · No code executed, no weights loaded, no GPU.*


---

## LOG-237 — Final targeted re-verification of the single-cell F-235-2 repair

**Track-7 (adversarial review) · 2026-09-23 · Reviewer independence: no involvement in writing the plan or applying any fix; all claims treated as untrusted.**
**Method:** line-level read of §7.2 and all cross-referencing sections (§5 cells, §6 L3, §8, §9) of `research/analysis_plans/K3_COMPLIANT_BRIDGE_PLAN_LOG234_2026-09-23.md`; pairwise overlap audit of every §7.2 row against the §5 cell definitions; quotation-match of every fix-scoped passage against the LOG-235/LOG-236 specs; banner check. No code executed, no weights loaded, no GPU.

### (1) Repair present exactly as specified

§7.2 table, row 1, C2-condition cell now reads **"cell 1 (L > 0.05)"** (previously "any with p < 0.05"). Verified verbatim against the LOG-236-specified minimal repair. Row 3's pre-existing "cell 1 (L > 0.05)" wording is untouched and now mirrored by row 1.

### (2) Exhaustiveness and mutual exclusivity of the §7.2 table

Per §5's binding cell definitions, every candidate arm lands in exactly one of: **cell 1 / RESCUES** (Tango L > 0.05), **cell 4** (McNemar p < 0.05, L ≤ 0.05), **NULL** (p ≥ 0.05) — an exhaustive, exclusive partition. C2's cells partition identically.

**Pairwise row audit (Phase-1 table):**
- Rows 1 vs 2: candidate condition identical; C2 conditions **cell 1** vs **cell 4 or p ≥ 0.05** are exhaustive and exclusive given the cell partition — no overlap.
- Rows 3 vs 4: same split on the same C2 partition — exclusive.
- Rows {1,2} vs {3,4}: candidate conditions "≥1 RESCUES" vs "all NULL" are exclusive — no overlap.
- Row 5 ("≥1 CELL-4, none RESCUES" | any C2) vs rows 1–4: row 5's "none RESCUES" excludes rows 1–2's "≥1 RESCUES", and its "≥1 CELL-4" excludes rows 3–4's "all NULL" — exclusive despite its "any" C2 column.
- Row 6 (guards-fail → Refuted) carries stated precedence over all endpoint rows (Law #13) — no precedence conflict; LOG-236's objection (that only guards-fail had a precedence rule) is now moot because no two endpoint rows overlap.

**Exhaustiveness:** candidate-arm collective states partition into {≥1 RESCUES} / {none RESCUES, ≥1 CELL-4} / {all NULL}; each, crossed with C2's 3-cell partition, hits exactly one row. The row-1 narrowing strands no reachable outcome: the C2 outcomes removed from row 1 (cell 4, NULL) are fully covered by row 2; no candidate-arm × C2 cell is unmapped. §6 L3's outcome-partition claim ("every {candidate cell} × {C2 cell} × {guards} cell maps to exactly one of the five verdict categories") now holds. §6 L3's KILL conjunction ("all tested compliant candidates NULL ∧ C2 in cell (1)") and CONTINUE conjunction ("≥1 compliant candidate in cell (1)") remain consistent with rows 3 and 1 respectively.

### (3) Collateral edits: none detected

Quotation-match against the full fix scope (F-235-1–F-235-4 + the LOG-236 repair): the only delta in §7.2 vs the LOG-236-verified state is the single C2-condition cell in row 1. §3.1 (C-a)–(C-e) per-item role-relative wording and rationale, §3.2 parenthetical, E-K3-1 per-item assertions + descriptive collision count, §5 arm-pairing/cells/caveat text, §6 L3, §8, §9, §10, §11, §12 all unchanged. (Standing limitation: the plan file is untracked, so no byte-diff baseline exists; verification rests on quotation-match, same as LOG-236.)

### (4) FROZEN / DO NOT EXECUTE banner intact

Title "K3 — … FROZEN PLAN", the pre-SIGN blockquote ("FROZEN — DO NOT EXECUTE before Law #14 SIGN"), the bottom banner, and the footer ("FROZEN pending independent Law #14 review SIGN") all present and unaltered.

### Verdict: SIGN

The F-235-2 repair is present exactly as specified, the §7.2 table is exhaustive and mutually exclusive across all row pairs, no collateral edits were found, and the frozen banner is intact. The plan is **released for Phase-0 execution under its §10 protocol** (post plan-SIGN: Phase-0 executor works §10 verbatim; Phase 1 remains gated on the §8 G9 release chain). `reports/research_log.md` untouched per instructions (Lead owns the log).

*Reviewer: Track-7 (LOG-237) · 2026-09-23 · No code executed, no weights loaded, no GPU.*
