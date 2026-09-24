# Adversarial Review — K3 Phase-0 R1 Re-registered Plan (LOG-239)

**LOG-240 · Track-7 (adversarial review) · 2026-09-23**
**Target:** `research/analysis_plans/K3_PHASE0_R1_PLAN_LOG239_2026-09-23.md` (FROZEN)
**Superseded signed plan (inheritance source):** `research/analysis_plans/K3_COMPLIANT_BRIDGE_PLAN_LOG234_2026-09-23.md` (Law #14 SIGNED via LOG-235/236/237 — its SIGN is inherited; only the R1 delta is litigated here)
**Reviewer independence:** no involvement in writing the R1 plan (or the LOG-234 plan); all author claims treated as untrusted and re-verified against primary artifacts.
**Method:** full line-level read of the R1 plan; machine `diff` against the signed LOG-234 plan (complete hunk enumeration); read-only JSON inspection of `experiments/protocols/C-A_PREAUDIT_2026-09-23.json` (field names, record count, id uniqueness, example-record byte-match); read of `research/analysis_plans/K3_PHASE0_HALT_REPORT_LOG238_2026-09-23.md` (§1–§3, §8); read of `reports/adversarial_review_k3_plan_2026-09-23.md` (LOG-235/236/237); grep scans for banned-verdict language, leftover old-source references, and LOG-240 banner integrity. No code executed beyond read-only JSON loads, no weights loaded, no GPU. No `reports/research_log.md` entry written (the Lead owns the log).

---

## Verdict: SIGN

The R1 re-registration is exactly what it declares itself to be: the signed LOG-234 plan with G4's cross-check repointed from the pre-repair smoke archive to the signed pre-audit JSON's per-item records, plus a binding D1-lesson note and a binding Law #3 recompute requirement. The delta audit found **no undeclared changes**. The repointed G4 is **satisfiable as written** — the cited JSON path exists, `similarity_audit.per_item` holds exactly 60 records each carrying the fields `(id, t, f)` with 60 unique ids, the field names match the plan's specification, and the plan's example record is byte-identical to the actual first record. FATAL-on-mismatch is retained everywhere; the smoke archive is barred without weakening G4; the recompute requirement is imperative, not advisory; the Law #4 chain is cited correctly; the banner names LOG-240; banned-verdict language appears only inside the ban statements.

**Release:** K3-Phase0-R1 is released for Phase-0 execution under its §10 protocol (post-SIGN). Phase 1 remains gated on the §8 G9 release chain. The inherited SIGN on all carried-over sections (endpoints, guards, tables, pins, tolerances, license) stands — the LOG-235 F-235-1–F-235-4 fixes and the LOG-237 §7.2 repair are carried over verbatim (verified by the diff's silence in those sections).

---

## 1. Carry-over audit — every delta enumerated (vs the signed LOG-234 plan)

Machine `diff` produced 11 hunks; every one is accounted for:

| # | Location | Change | Declared? |
|---|---|---|---|
| 1 | Title + header | "(R1)"; LOG-234 → LOG-239; banner adds "(LOG-240)" | Yes — re-registration numbering |
| 2 | New blockquote after banner | **Law #4 chain (re-registration reason):** names the superseded plan, the LOG-238 halt, FATAL G4 / plan-premise defect D1, 12/60 vs 48 mismatches; declares the single change (G4 repointed) and that all else carries over verbatim; Law #8 smoke-archive preservation; G4 not weakened | Yes — the declared re-registration rationale |
| 3 | §2 cross-check bullet | Repointed from smoke `exp077_instance_records.json` `ent`/`typ` to `experiments/protocols/C-A_PREAUDIT_2026-09-23.json` `similarity_audit.per_item`, 60 `(id, t, f)` records, 60/60 byte-agreement, any mismatch = FATAL; old pin marked **superseded** | Yes — the declared G4 repoint |
| 4 | §2 (new bullet) | **D1-lesson note (binding):** smoke archive is pre-MAJOR-3-repair (entity-grouped 6/entity; Anglo-subjects bench; planet targets 21/7/2/0/0 post-repair); never to be used as a cross-check source; LOG-197's byte-identity sentence mis-scoped by LOG-234; future sources must be signed + verified on the post-repair bench | Yes — the declared D1 note |
| 5 | E-K3-5, §5, §10 filenames | `K3_CONSTRUCTION_AUDIT_RESULTS_LOG234` → `LOG239`; `K3_construction_audit_execute_LOG234` → `LOG239`; `K3_rescue_execute_LOG234` → `LOG239`; `K3_RESCUE_RESULTS_LOG234` → `LOG239` | Yes — mechanical renames under the new plan number (avoids collision with LOG-238's filed twins) |
| 6 | §6 L4 A1 | Discharge repointed: "§8 G4 cross-check vs the signed pre-audit per-item records (`similarity_audit.per_item`, 60 `(id,t,f)` records); expected 60/60 byte-agreement; any item mismatch = FATAL" | Yes — consequence of the G4 repoint |
| 7 | §8 G4 | Full rewrite: byte-comparison of rebuilt per-item `(id, t, f)` (index-aligned, exact strings) against the signed pre-audit JSON; **any item mismatch = FATAL**; **executor RECOMPUTES the comparison itself from the source JSON file** (Law #3 — does not inherit LOG-238's 60/60 claim); cross-checking against the smoke archive **prohibited** (D1-lesson note, binding) | Yes — the declared G4 repoint + recompute requirement |
| 8 | §9 (Phase-0 PROCEED bullet) | **R1-specific consequence (pre-registered):** if the repointed G4 passes, Phase-0 proceeds under this re-registration and the LOG-238 halt **converts to a superseded halt** — the halt report preserved in place, never deleted or edited (Law #8); record shows halted-then-superseded | New text, but declared in-document and consistent with Law #8 (see §N below) |
| 9 | §10 step 2 | G4 cross-check vs the signed pre-audit JSON (index-aligned, byte-exact per-item (id, t, f); expected 60/60; any mismatch = FATAL); executor recomputes itself (Law #3); smoke-archive cross-check forbidden (binding) | Yes — the declared G4 repoint + recompute requirement |
| 10 | Footer | Author LOG-239; names LOG-240; "Plan number: **K3-Phase0-R1**"; Law #4 chain restated (LOG-234 SIGNED via LOG-235/236/237 → LOG-238 halt → R1 repoints G4, all else verbatim) | Yes — re-registration numbering |
| 11 | Bottom banner | "FROZEN — DO NOT EXECUTE before Law #14 SIGN (LOG-240)" | Yes — required by the brief |

**No undeclared deltas.** All endpoints (E-K3-1–E-K3-5), guards G1–G11, §7 verdict tables, §6 license L1–L4, §8.1 env pin, §9 remaining consequences, §10 remaining steps, §11 scope, §12 knowledge-protocol obligations, and every tolerance, pin, and decision rule are byte-identical to the signed plan. The inherited LOG-235/236/237 SIGN therefore stands on all carried-over sections. **No scope violation.**

---

## 2. G4 satisfiability (verify item (2) of the brief)

Verified against the primary artifact (read-only JSON load — no weights, no GPU):

- **Path exists:** `experiments/protocols/C-A_PREAUDIT_2026-09-23.json` loads.
- **`similarity_audit.per_item`:** present; exactly **60 records**.
- **Field names:** every record carries `id`, `t`, `f` (plus `s_t`, `s_f` — unused by G4, harmless). **All 60 ids unique.**
- **Field-name match:** the plan specifies "60 `(id, t, f)` records" — matches the artifact exactly. No second D1-class field-name defect.
- **Example byte-match:** the plan's §2 example record `{"id": "exp077_planet_2hop_0", "t": "Mars", "f": "Jupiter", ...}` is byte-identical to the artifact's first record (modulo the `...` ellipsis) — the author cited the real artifact, not a fabricated sample.
- **Id scheme:** ids `exp077_planet_2hop_0` … `exp077_element_3hop_14` match the plan §1 bench-id scheme (`exp077_planet_2hop_0..14`, etc.), so the plan's "rebuild `(id, t, f)` per item" instruction is well-defined: id ↔ bench item id, t ↔ target, f ↔ foil.
- **Index alignment:** the artifact's `per_item` order (planet_2hop, planet_3hop, element_2hop, element_3hop) is consistent with the halt report's recorded quad-loop sub-ranges (0–14 / 15–29 / 30–44 / 45–59) — the "index-aligned" comparison is executable by the §10 port.
- **(i) signed:** the JSON is attached to the signed EXP081 v2 spec (`C-A_DONOR_TRANSFER_PREREG_SPEC_V2.md`, "Status: PRE-REGISTERED — signed by the CEO (Research Lead) under LOG-182") as binding computed values — satisfying the D1-lesson note's requirement (i).
- **(ii) post-repair bench:** the LOG-238 halt report §3 recorded the port's 60/60 byte-agreement with these records as a descriptive [OBSERVATION]; the R1 plan correctly treats that as an *expectation to re-verify* ("Expected agreement: 60/60"), not an inherited fact — that is precisely what the Law #3 recompute requirement discharges.

The one nominal B_i/C_i looseness in §10 step 2 ("rebuild (B_i, C_i, target_i, foil_i) per item" — premise entities have no analog in the per-item records) is **inherited verbatim from the signed LOG-234 plan** and is harmless: §8 G4 defines the byte comparison exclusively on the per-item `(id, t, f)` tuple, and B_i/C_i serve only the construction and the G6 single-token assert. Not a defect.

---

## 3. D1-lesson note (verify item (3) of the brief)

The note is binding ("D1-lesson note (binding — added in R1)"). It:

- States the [FACT, per LOG-238] premise: the smoke archive is pre-MAJOR-3-repair, structurally unreconcilable with the post-repair bench (entity-grouped 6/entity vs 21/7/2/0/0; Saturn/Mercury never targets post-repair).
- **Bars the archive absolutely:** "It must **never** be used as a cross-check source for the post-repair bench" — reinforced by §8 G4 ("Cross-checking against the pre-repair smoke archive ... is prohibited (the §2 D1-lesson note, binding)") and §10 step 2 ("It must not cross-check against `exp077_instance_records.json`").
- **Does not weaken G4:** "Any item mismatch = FATAL" is stated in §2, §8 G4, and §10 step 2; the note explicitly records "does NOT weaken G4 (the cross-check remains FATAL and load-bearing for A1)". The Law #13 precedence (guards-fail → Refuted) is inherited untouched.
- Names the defect class (same as LOG-197 F1 and EXP082's D1) and sets the forward rule: any future cross-check source must be (i) signed and (ii) verified on the post-repair bench.

---

## 4. Law #4 chain (verify item (4) of the brief)

Cited correctly in both the post-banner blockquote and the footer:

- **Superseded plan:** `research/analysis_plans/K3_COMPLIANT_BRIDGE_PLAN_LOG234_2026-09-23.md`, "Law #14 SIGNED via LOG-235/236/237" — correct.
- **Halt:** "That plan's Phase-0 execution (LOG-238) HALTED at §10 step 2" — correct (`K3_PHASE0_HALT_REPORT_LOG238_2026-09-23.md`).
- **Reason:** "FATAL G4 caused by plan-premise defect D1" with the 12/60-matches / 48-mismatches evidence and the pre-repair-smoke-archive vs post-repair-bench characterization — faithful to the halt report §3.

The re-registration vehicle itself is the correct Law #4 vehicle: the superseded plan is untouched (no silent edit), and R1 is a new numbered plan consuming the same K3 battery slot ("Experiment number: none consumed").

---

## 5. Recompute requirement (verify item (5) of the brief)

**Binding, not advisory.** §8 G4: "**The executor RECOMPUTES this comparison itself from the source JSON file** — it does not inherit, quote, or otherwise rely on the LOG-238 run's 60/60 byte-agreement claim (Law #3: recompute-don't-trust; the LOG-238 60/60 agreement is a claim to verify, not a fact to inherit)." §10 step 2: "The executor recomputes the full 60/60 comparison itself from the JSON file (Law #3); it inherits nothing from LOG-238's claim." Both are imperative and located in the executor's step-by-step protocol. The mechanism is specified (index-aligned, exact-string byte comparison), so an executor cannot comply nominally by asserting the outcome without doing the comparison.

---

## 6. Banner (verify item (6) of the brief)

"FROZEN — DO NOT EXECUTE before Law #14 SIGN (LOG-240)" appears in the top blockquote, and the footer names LOG-240 as the releasing workstream ("FROZEN pending independent Law #14 review SIGN under LOG-240 (reviewer assigned by the Research Lead; must not be the plan author)"). The title carries "(R1)" and the footer names the plan number **K3-Phase0-R1**. 4× "LOG-240" mentions total. Banner integrity: intact.

---

## 7. Banned-verdict language (verify item (7) of the brief)

"Promising", "interesting", "worth another experiment" occur **only** inside the two ban statements (§1, §8) — the same two locations as in the signed plan; no new occurrences. All verdict language in the plan uses only the five permitted verdicts (Supported / Not supported / Inconclusive / Underdetermined / Refuted). §9, §7.1, §7.2, §0 Q2, and §6 L3 all use permitted verdicts exclusively. No banned-verdict language.

---

## Notes (observations, not fixes — do not block SIGN)

**N1 — §9's R1-specific "superseded halt" consequence.** This is the only in-document addition that goes beyond the brief's enumerated delta list (§8 + §10 step 2 repoint, §2 D1 note, recompute requirement). It is declared in-document ("R1-specific consequence (pre-registered)"), non-gating, and Law #8-consistent (halt report preserved, never edited). It does not alter any endpoint, guard, margin, or verdict mapping, and it does not license any claim about the halted run (the LOG-238 §7.1 Refuted-per-candidate cells and their "no claim licensed; CEO decides" consequence stand). Recorded for the Lead's awareness; not a scope violation.

**N2 — Plan expects, does not assert, 60/60.** The plan's "Expected agreement: 60/60" rests on the LOG-238 halt run's descriptive 60/60 observation. The plan is careful to present this as an expectation (not a [FACT] tag) and to make the executor's own recompute the discharging event. Correct handling of the Law #3 asymmetry; no inheritance-by-reference.

**N3 — The (id,t,f) mapping is implicit but unambiguous.** The plan does not write out "t = target_i, f = foil_i" in a single sentence, but §1 defines A = target / C = foil, §2 defines the record fields, and the halt report's §3 D1 corollary demonstrated exactly this mapping at 60/60. No executor ambiguity worth a wording fix — the §8 G4 "byte-compared (index-aligned, exact strings)" instruction plus the §2 example record pin the format.

**N4 — Carried-over fixes reconfirmed present.** The diff's silence across §§3–7 confirms the LOG-235 F-235-1 (per-item role-relative (C-a)/(C-b) + rationale + descriptive collision count), F-235-2/LOG-237 (single-cell repair — §7.2 row 1 reads "cell 1 (L > 0.05)"), F-235-3 (T1 arm-pairing wording), and F-235-4 (token-prior confound caveat) are all inherited verbatim. The §7.2 table remains exhaustive and mutually exclusive as audited in LOG-237.

---

## Bottom line

**SIGN.** The R1 re-registration is a faithful, minimal Law #4 repair of a plan-premise defect: every changed line is declared, the repointed G4 is satisfiable against the verified artifact (60 `(id, t, f)` records, fields match, example byte-matches), FATAL-on-mismatch is retained, the smoke archive is barred without weakening the guard, the Law #3 recompute is binding imperative, the Law #4 chain is cited correctly, the banner names LOG-240, and no banned-verdict language appears. K3-Phase0-R1 is **released for Phase-0 execution** under its §10 protocol. Phase 1 remains non-existent until the §8 G9 release chain completes.

*Reviewer: Track-7 (LOG-240) · 2026-09-23 · No code executed, no weights loaded, no GPU. `reports/research_log.md` untouched (Lead owns the log).*
