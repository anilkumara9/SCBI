# Independent exact-artifact verdict review — EXP117 (H11/PTTSC-GEN)

**Review lane:** LOG-4610 (pre-assigned). **Verdict: BIND** — the registered RUN-INVALID stands on the exact artifacts, no caveat.

**Scope of review:** the execution report (`research/experiments/EXP117_PTTSCGEN_REPORT_2026-09-29.md`), the signed pre-registration (`research/prereg/EXP_PREREG_H11_PTTSCGEN_2026-09-29.md`, Law #14 SIGN-WITH-FIXES LOG-4607, fix byte-verified LOG-4608), and the raw artifacts in `experiments/runs/EXP117_pttscgen/out/`. This lane is independent of the LOG-4609 execution lane; nothing in this review modifies any signed artifact.

---

## 1. Independent recomputation from the raw records

From `exp117_generations.json` (20 records: 10 `phase0a_planner` + 10 `phase0b_baseline`) and `exp117_result.json`, this lane independently verified:

| Claim | Report | Independent | Match |
|---|---|---|---|
| Phase 0a probe set | {0,1,2,5,6,7,8,9,10,11} | {0,1,2,5,6,7,8,9,10,11} | ✓ |
| Phase 0a literal §3.7 gate | 0/10 (≥6 → fire) | all 10 records `n_recited_literal=0` | ✓ |
| Phase 0a content diagnostic | 10/10 with ≥2 content recitations | all 10 records `n_recited_content_diagnostic=3` | ✓ |
| Phase 0a token-overlap diagnostic | 0.7054 | 0.7054129853522436 (raw) | ✓ |
| Phase 0b parseable | 0/10 (<8 → fire) | 10/10 outputs non-exact-match | ✓ |
| Phase 0b distinct/minority | 0 / 0 | 0 / 0 | ✓ |
| Generations / exceptions | 20/20, 0 | 20 records, `exception: null` ×20 | ✓ |
| Bench provenance pin | `47281cd3…058` MATCH | `47281cd3…058` in worksheet | ✓ |
| Backbone LOG-331 pin (pre) | MATCH | `ec276abe…0ed` in worksheet | ✓ |
| Planner prompt byte-identity | 0/60 mismatches | worksheet `planner_prompt_byte_identity_mismatches: 0` | ✓ |
| Fidelity / McNemar | none exist | `"items": []`, no metric keys | ✓ |

**Gate order honored:** Phase 0a (literal) passed → Phase 0b fired → no full run licensed. The registered tree branch (`bench ok → backbone pin (pre) ok → prompts byte-verified ok → Phase 0a literal 0/10 (<6) pass → Phase 0b: 0/10 parseable (<8) → RUN-INVALID`) was taken exactly.

---

## 2. The 0b failure mode — verified verbatim from the raw generations

The enumeration failure mode is byte-real. All 10 Phase-0b outputs fail the registered exact-match parse rule (strip + trailing punctuation + case-insensitive exact match vs the bench's "A"/"C" entity names). Verbatim excerpts (byte-identical to the raw records):

- Item 0: `'\n\n1. Jupiter\n\n2. Mars\n\n3. Venus\n'` — enumerated listing, no single selection.
- Item 2: `'\n\nMercury\n\nMercury is the highest-ranked'` — entity name followed by continuation; the exact-match rule (correctly, per §3.6) scores it UNPARSEABLE.
- Item 10: `'\n\nJupiter\n\nThe lower-ranked entity is:\n\n'` — degenerating into a new prompt tail.

Item 2 is the important calibration case: it *contains* the right entity name but the registered rule scores it unparseable. This is not an error — it is the pre-registered rule operating as written, and the margin (0/10 vs the ≥8/10 bar) is far beyond any reasonable rule perturbation. No plausible re-parse changes the gate outcome.

---

## 3. Adjudication of the §3.7 protocol-defect discovery

The execution lane flagged a protocol defect: the literal §3.7 recitation definition — "an outline **recites** iff it exactly equals (after strip + casefold) one of the 4 pinned exemplar OUTLINES" — compares extracted outlines against the **marker-prefixed** exemplar lines (`"1. Restate the question's ordering constraint in my own words."`, as the `OUTLINES` block is pinned in §3.3), while the §3.3 extraction rule strips the numeric markers from extracted outlines. A verbatim *content* recitation therefore **cannot** satisfy the literal definition by construction.

**Adjudication (three points, as tasked):**

(a) **The defect is real — yes.** Verified both by construction (the definition/exraction pair is structurally incompatible) and empirically: the raw Phase-0a item-0 output opens with the verbatim exemplar block `\n1. Restate the question's ordering constraint in my own words.\n2. Check each premise statement against the two candidate entities.\n3. Eliminate the entity contradicted by any premise.\n4. Name the remaining entity as the answer.` — content-recitation with markers intact — while the literal gate scored `n_recited_literal=0` on all 10 items and the content-level diagnostic (against marker-stripped exemplar content) scored 3/4 outlines on all 10 items. The report's §2 is byte-faithful to the raw records, including the 0.7054 mean max token-overlap diagnostic.

(b) **The defect does NOT change the verdict.** The executor applied the gate exactly as written (Law #4 — no mid-run rewrite; correct). Phase 0b fired independently (0/10 parseable < 8/10), which is itself a registered RUN-INVALID branch. Even if the §3.7 definition had fired, the verdict would be RUN-INVALID via a different branch; even if the definition had been silently "corrected" mid-run, Phase 0b would still have killed the run. The verdict is overdetermined.

(c) **The defect must be recorded — it is.** This review records it here as a binding apparatus-definition lesson: **no future protocol may reuse the §3.7 literal recitation definition** — the exemplar-comparison side of the definition must be marker-stripped identically to the extraction rule, or the gate is structurally inert. The report's fence §5.2 (the finding is an [OBSERVATION], not a license to rerun with a "fixed" gate — any re-derived gate is a separate pre-registered lane) is honored; no re-run is licensed by this review.

---

## 4. Fences

- **No verdict smuggled:** the report kills/holds/continues nothing; H11's planning question was never tested. The registered falsification-tree branch names the RUN-INVALID branch and no decision bar was read. Verified: `exp117_result.json` contains no metric, no McNemar table, no n_valid.
- **Prior verdicts unchanged:** H4 stays RUN-INVALID-from-EXP109 (this review does not revisit it). EXP109's report was read: "Baseline: 80/80 generations UNPARSEABLE" — the EXP117 report's prior-claim is byte-faithful. EXP115 (38/60 recitation) and EXP116 (37/60 tail echo) were verified against their own reports during this review.
- **The 4th-consecutive claim checked:** EXP109 sampled 80/80 unparseable (verified in EXP109's report), EXP115 greedy few-shot 38/60 recitation (verified in EXP115's report §2), EXP116 greedy priming 37/60 tail echo (verified in EXP116's report §2), EXP117 greedy priming on EXP091 0/10 enumeration (verified above). The claim is accurate; the regimes differ (sampled vs greedy) and the report does not overstate comparability.
- **No post-hoc softening:** the report's §5 fences are honored, including §5.2's bar on re-derived-gate re-runs.

---

## 5. Non-binding observations (not caveats; do not affect the verdict)

1. **Byte-identity reference disclosed honestly:** the report's §1 honesty note records that EXP113's raw JSON stores no prompts, so the byte-identity check ran against the signed `exp113_run.py` construction code rather than stored prompts. This is disclosed, not hidden, and `mismatches: 0` stands on the reconstructible reference. No defect.
2. **Post-run backbone pin not taken:** the registered falsification tree routes the post-run pin check through the full-run branch; Phase-0b RUN-INVALID exits before it. The report discloses this. Law #6 is not breached (the backbone was read-only throughout; the pre-run pin matched). No defect.
3. **The Phase-0 probe set excludes items 3–4** (the planner's exemplars), exactly as §3.7 pins. Verified in the raw records.

---

## 6. Verdict

**BIND.** EXP117's registered RUN-INVALID stands on the exact artifacts: every binding count recomputed exactly, the 0b failure mode verified verbatim from the raw generations, the §3.7 protocol defect adjudicated real-but-non-decisive and recorded for future protocols, all fences honored. No caveat required.
