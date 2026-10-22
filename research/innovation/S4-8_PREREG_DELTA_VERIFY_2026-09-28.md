# S4-8 Pre-registration v2 — Independent Delta Re-verification (LOG-4478)

*Status: VERIFY — binding. This document verifies; it does not edit v1, v2, or the review; does not authorize a run; does not mint an experiment number.*
*Verifier: independent delta lane (pre-assigned LOG-4478), first-touch — this lane has not touched the S4-8 draft, its repair wave, or the EXP085 chain before this verification.*
*Inputs read in full: `research/innovation/S4-8_PREREG_DRAFT_v2_2026-09-28.md` (LOG-4477, v2); `research/innovation/S4-8_PREREG_DRAFT_2026-09-28.md` (LOG-4475, v1); `research/innovation/S4-8_PREREG_REVIEW_LAW14_2026-09-28.md` (LOG-4476, review). Diffed v1 vs v2 line by line.*
*Compute: $0 CPU. No model runs, no weights touched, no signed artifact modified. v2 was NOT edited.*

---

## 0. Process finding (affects the verification standard)

**The review file is itself truncated.** `S4-8_PREREG_REVIEW_LAW14_2026-09-28.md` ends mid-sentence in Law #8 with a literal embedded `...[truncated 10000 chars]` marker — the review lane wrote a file that was cut off. The §3 fix-text section ("exact fix text") the review's executive summary refers to was **never written**; it does not exist in the file.

Per the task instruction, each fix was therefore judged against the review's **defect descriptions + intent** (Elements 1–7, law-by-law notes), not against fix text that doesn't exist. All 8 defect descriptions are present inline in the review body — none is missing. The repair lane's fix-ID tags (D1–D5, m1–m3) are all present in v2 and each maps to a real defect description. The "verbatim" standard in the review's executive summary cannot be literally applied; intent-fidelity is the applied standard.

---

## 1. Per-fix verification (v1 vs v2 diff)

| Fix | Defect intent (review, inline) | v2 change (fix-ID tagged) | Score |
|---|---|---|---|
| **D1** (MAJOR) | v1 step 8 (KILL nonspecific) misroutes the pattern {ΔM_T > 0, T-vs-R p ≥ 0.05, ΔM_F > 0 significant} — rationale "random masking matches" misdescribes a foil-positive pattern; the F-significant pattern must be evaluated **before** the nonspecific kill. | New step 8 **PIVOT (foil interference, D1)**: "not CONTINUE, AND ΔM_F > 0 with F-vs-B p < 0.0125 → PIVOT", evaluated (first-match-wins) **before** step 9 KILL (nonspecific). Rationale must name the foil arm; must never read "random masking matches — generic perturbation" in this corner. Step 9's own tag confirms it fires only when the F-pattern did not route. §0's PIVOT clause cross-references step 8. | **VERIFIED** |
| **D2** (MAJOR) | CONTINUE conjunct \|ΔM_F\| < 0.05 unreachable in the expected foil–top-1 overlap world (foil == top-1 on many Tier-0 items); v1 step 10's parenthetical contradicts the table by giving the overlap check no adjudicating role. Overlap must be a pre-registered **stratum**, not a parenthetical. | F conjunct removed from §0 prediction, §2.5 flat band ("for R under CONTINUE"), and step 7 CONTINUE. New pre-registered **foil–top-1 overlap stratum (D2)**: O = fraction of Tier-0 items where foil token == top-1 token; O > 0.5 → F non-diagnostic (descriptive, no binding consequence); O ≤ 0.5 → F diagnostic (routes per steps 6/8). v1 step-10 parenthetical deleted; its example moved to step 11 "Otherwise". | **VERIFIED** |
| **D3** (MAJOR) | Law #7 foil-build blindness guard needs operationalization — "the distractor judged most confusable" must be auditable as model-blind. | New **"Foil-build blindness (operationalized, D3)"** section: named builder identity pre-registered (role + lane id in manifest); blindness criterion = zero model outputs observed on any S4-8 bench item at designation time; independent verification lane confirms designation-timestamps precede first model pass + manifest rationale/hashes + zero pre-pass model artifacts. Carried in §4 guards and §5 item 2. | **VERIFIED** |
| **D4** (MAJOR) | (a) G1 instrument unnamed — pin tokenizer name + revision/hash (§2.1/§4); (b) Law #13 — pin prompt template + readout position. | New **bench-build procedure (D4)** (a)–(e): (d) frozen prompt template (verbatim block) with **pinned readout position** (token after terminal `Answer:`), template hash + index persisted; (e) tokenizer artifact named **EleutherAI/gpt-neox-20b**, exact revision hash required in the §5 item 2 attestation **before any model pass**. §3 step 1, §4 G1 gate, and §5 item 2 all reference the pinned artifact. | **VERIFIED** (note: name pinned; hash required pre-pass in attestation rather than printed in draft — implements the auditable-instrument intent; step 1 RUN-INVALID voids on incomplete verification) |
| **D5** (MAJOR) | Tie-guard instrument underspecified — "correct-option top-1 tie rate" used by the binding step 5 HOLD bar with no pinned numerator/denominator. | Step 5: **Tie rate [PINNED, D5]** = (# Tier-0 items where the correct option's logit is exactly tied — float32 exact equality — for the highest logit among the 8 options) / n_pop. Carried as "D5-pinned numerator/denominator" in §5 item 3. | **VERIFIED** |
| **m1** (MINOR) | "Probes" undefined; v1 budget double-counts ("240 + probes ≈ 360"). | §0: **Probes [DEFINITION, m1]** = non-decision readout passes extracting the 8-option logit vector + correct-rank at the pinned readout position (vs arm decision passes recording only the masked-argmax decision). Budgeted ≤2/item (≈120 total); beyond the 360 planning figure counts against the 500 hard cap. §2.4: battery = 240 decision passes + probes ≈ 360. | **VERIFIED** |
| **m2** (MINOR) | License label inflated ("THEOREM-adjacent"). | **Mathematical license [PROPOSITION — elementary combinatorial fact, m2]** + proof sketch (k ≥ 3: correctness ↛ rank). No claim beyond a test-license. | **VERIFIED** |
| **m3** (MINOR) | McNemar-exact implementation needs a reference cross-check (implementation review will need it). | §4 unit test **(f)**: McNemar-exact cross-checked against a reference (hand recurrence or scipy.stats) on the full (b,c) grid **before any bench contact**; mismatches void the statistics machinery. Six tests total, all pre-bench. | **VERIFIED** |

**Score: 8/8 VERIFIED.** Section structure v1→v2 is identical (87 changed lines, all attributable to the 8 fixes + direct consequences: stratum, bench-build procedure, blindness operationalization, probe definition, step renumbering). Nothing beyond the fixes + direct consequences changed.

---

## 2. v2 element re-scores (review's 7 elements)

1. **Rank measurability / EXP085 escape:** unchanged — **PASS**.
2. **G1 real-tokenizer gate:** instrument named, revision hash required pre-pass, gate first in binding order, per-string attestation — **PASS**.
3. **Falsification bars:** D1/D2 repaired; one binding test (T-vs-R, α=0.05), Bonferroni 0.0125 elsewhere, DELTA_BAR=0.10, sharp breaking points — **PASS**.
4. **Cheapest test + Tier-0 bar:** probes defined (m1), 120 + 360 = 480 ≤ 500 budget arithmetic consistent — **PASS**.
5. **Degeneracy + unit tests:** six pre-bench tests incl. m3 reference cross-check — **PASS**.
6. **Scope fence:** unchanged, airtight — **PASS**.
7. **Feasibility algebra:** n_pop ≥ 12 gate, no hidden cap, HOLD-not-silent-edit — **PASS**.

**7/7 PASS.**

---

## 3. New-defect check (introduced by the repair wave)

**One new defect found — N1 (binding): step 8 vs the D2 stratum, O > 0.5 corner.**

- The D2 stratum states: "If O > 0.5, the F arm is **non-diagnostic** — F results are reported descriptively by stratum **with no binding consequence**."
- Step 8 (D1) routes on F-significance with **no O condition**. In the O > 0.5 world this corner is reachable: F duplicates T on a majority of Tier-0 items, so a significant F-vs-B (≥8 unidirectional flips, p < 0.0125) can co-occur with a sub-bar or R-matched T (e.g., ΔM_T > 0.10 but T-vs-R p ≥ 0.05 because the random arm rescued the same items) — step 7 fails, step 8 fires, and the verdict rationale claims "the structural-foil mask rescued — interference confirmed" when the foil mask **was** the top-1 mask on most items. That is exactly the misattribution the D2 stratum was created to prevent, and it contradicts the stratum's "no binding consequence."
- The defect descriptions did not demand an O-gate on step 8 — this is genuinely new, introduced by the repair wave.

**Exact fix (required):** amend step 8's condition to `…AND overlap O ≤ 0.5 (F diagnostic per the pre-registered stratum)`; add: "If O > 0.5, the F-significant pattern carries no binding consequence per the stratum — the evaluation falls through to step 9/11."

No other new defects: no wording drift in verdict mappings, no contradictory bars (DELTA_BAR, flat band, α levels consistent across §0/§2.5/§3), no scope creep (fence text byte-identical in substance; EXP085 kill untouched; no L11 content).

---

## 4. Binding verdict

**SIGN-WITH-FIXES.** 8/8 fixes VERIFIED, 7/7 elements PASS — the repair wave is faithful. One new binding defect (N1: step 8 needs the O ≤ 0.5 gate) must be applied as exact pre-registered text before SIGN. The fix is a one-condition amendment; no redesign, no re-review of the whole draft required — a second delta check of the amended step 8 text is sufficient. No experiment number minted; no run authorized; CEO execution clearance still required after SIGN.

*Verified 2026-09-28 by the independent S4-8 delta re-verification lane (pre-assigned LOG-4478). $0 CPU, on-paper only. v2 NOT edited.*
