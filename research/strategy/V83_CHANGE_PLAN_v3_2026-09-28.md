# V83 Change Plan v2 — Post-I2′ Audit
**Date:** 2026-09-28 · **Lane:** V83 CHANGE-PLAN AUDIT (LOG-4494; analysis only; v82 frozen, untouched; no experiment number minted) · **$0 compute**
**Inputs:** `V83_CHANGE_PLAN_2026-09-28.md` (LOG-4471) · new results: LOG-4472 (Item-33 recompute) · LOG-4481/4482 (EXP104 Tier-0) · LOG-4483 (bench autopsy) · LOG-4484→4488 (S4-8′ chain) · LOG-4489 (EXP105 Tier-0) · LOG-4491 (EXP105 battery) · LOG-4490/4492 (scoreboard v1.3/v1.4) · `~/workspace/scbi-paper/v82/paper.tex` (read-only)
**Epistemology:** Law #11 labels throughout — [FACT] (verifiable from a LOG entry, bundle artifact, or v82's text), [OBSERVATION] (reviewer's reading), [INTERPRETATION] (judgment).

---

## PART 1 — Line-by-line audit of the v1 plan against the new results

| Change (v1) | Verdict | What the new results change |
|---|---|---|
| #1 Viral number ("Decodes at 6.7× chance; steers zero decisions") | **ADOPT as-is** | [FACT] Nothing in EXP104/EXP105 touches the hero claim: the viral line is about the shared L11 direction injection (EXP092/93), the I2′ line is a separate question (masking intervention on two-hop recall). The EXP105 battery's Refuted verdict does not weaken "steers zero decisions" — if anything it extends the boundary theme. No edit. |
| #2 Boundary-map expansion (EXP094–103 + S6-5) | **ADOPT with addendum** | [FACT] The ledger must now add the I2′ line as its own closed arc: EXP104 Tier-0 HOLD→Inconclusive (LOG-4481/4482, baseline 11/60 = 0.1833 < 0.25 sanity band) · bench autopsy (LOG-4483, position-A prior 30/60, p=2.02e-12, MC bench dead as a knowledge instrument) · S4-8/S4-8′ pre-regs SIGNED (LOG-4480, LOG-4488) · EXP105 Tier-0 PASSED (LOG-4489, 32/60 = 0.5333 inside [0.25,0.75], n_pop 21, tie guard 0.0) · EXP105 battery Refuted at step 9 (LOG-4491, ΔM_T=+0.2381 vs ΔM_R=0.0000, T-vs-R McNemar b=5,c=0, p=0.0625 ≥ 0.05, missed CONTINUE by one flip; O=0.571 > 0.5 → F arm non-diagnostic) · line CLOSED per pre-registered stop rules. The phase diagram redraw (Fig. 6) gains the I2′ arc as a falsification-terminal branch. |
| #3 Honest dose-response disclosure | **ADOPT as-is** | [FACT] EXP095's scope fence (LOG-4400) and the S6 stand-down (LOG-4464) are unchanged by the new results. [OBSERVATION] Cross-reference only: the I2′ battery is a separate pre-registered line (S4-8′), not a dose-response on the hero shared-direction claim — v83 must not present EXP105 as filling Change #3's gap. Add one sentence to that effect in Limitation 6's neighborhood. |
| #4 Dilution law name | **ADOPT as-is** | Unaffected. |
| #5 Named enemy | **ADOPT as-is** | Unaffected. |
| #6 Item-33 hero vignette | **STALE PRECONDITION — RESOLVED by LOG-4472** | [FACT] The v1 plan's precondition ("recompute Item 33's item-level injection shift from EXP093 artifacts; if infeasible, use means labeled as such or ship without the margin arrow") is now decided: recomputation is INFEASIBLE — EXP093 persisted only aggregate margin shifts (mean P +0.0059518, mean N −0.0076361); per-item arrays were never saved; recovery needs a 180-pass GPU re-run (LOG-4472), which the no-GPU-spend rule bars. The gap analysis's +0.010/−0.004 appears in no artifact and must never be printed. **Revised spec (see Change #6R below).** |
| #7 Term discipline | **ADOPT as-is** | Unaffected. |
| #8 Abstract/intro restructure | **ADOPT as-is** | [OBSERVATION] The "Checkable claims" box should now include the I2′ terminal verdict (one line: "Two-hop recall masking: rescue direction clean, specificity uncertified — line closed (EXP105)"). |
| #9 Limitations as thesis | **ADOPT as-is** | [OBSERVATION] Add the position-A prior as a methods lesson in the limitations preface: the rig's own readout format was the dominant signal (30/60 at position 0, p=2.02e-12) — "a null the rig is proven capable of breaking" now has a concrete sibling: "an instrument the rig proved capable of invalidating." |
| #10 Caption audit | **ADOPT as-is** | Fig. 6's caption rewrite must cover the new I2′ branch (covered by Change #2 addendum). |
| #11 Reproduce-the-hero box | **ADOPT as-is** | [OBSERVATION] Scope stays the hero figure (EXP092/93). The EXP105 bundles are deterministic and $0-CPU reproducible, but folding them into the reproduce box is out of scope — note as optional follow-up, not a v83 requirement. |
| #12 Compress §sec:future | **ADOPT as-is** | Unaffected by new results. Cut-depth remains a founder decision. |

**Stale items fixed in v2:** Change #6's precondition (resolved by LOG-4472) · Change #2's ledger (missing the I2′ arc) · Change #8/#9's new cross-references.

---

## PART 2 — Revised and new changes

### Change #6R — Item-33 hero vignette, revised spec (replaces v1 Change #6's open precondition)
- **v82 location:** Discussion L391 → boxed callout on Fig. 1.
- **Change:** The vignette strip reads: "Item 33 (`exp092_elemental_2hop_3`): decodes with margin **1.0133** (2nd of 60; same-class min 2.1059, different-class min 3.1192) → decision unchanged under injection." The margin-shift arrow, if shown, carries the **mean-across-items** numbers **+0.0059/−0.0076 explicitly labeled as means across all 60 items, not Item 33's own shift** (LOG-4472). Alternative: ship the vignette with no margin arrow at all.
- **Why [FACT]:** Decode margin 1.0133, rank 2/60 verified by deterministic recomputation from EXP092 embeddings, matches v82 L391 to 5e-4 (LOG-4472, `ITEM33_MARGIN_RECOMPUTE_2026-09-28.md`). Per-item shifts are unrecoverable without a new 180-pass GPU run — barred by the no-spend rule.
- **Hard prohibition [FACT]:** the gap analysis's +0.010/−0.004 appears in no artifact — it must not be printed anywhere in v83.
- **Founder decision (b):** (i) mean-labeled arrow, or (ii) no arrow. There is no third option (recomputation is infeasible).

### Change #13 — NEW: the I2′ line arc on the boundary map (highest-impact new content)
- **v82 locations:** kill ledger §sec:kills (L367); phase diagram §sec:phasediagram (L376) + Fig. 6 caption; master table app:master (L530); limitations L394 (methods lesson).
- **Change:** Add the I2′ arc as a complete falsification-terminal branch: EXP085's death-debt (the question: are selection failures measurable/repairable) → S4-8 MC bench dead at 0.1833 (LOG-4481) → autopsy: position-A prior 30/60, p=2.02e-12 (LOG-4483) — **the lettered multiple-choice format is not a knowledge instrument on this base LM** → S4-8′ cloze recalibration rescues measurability 0.1833 → 0.5333 (LOG-4489) → truth-masking rescue direction clean (ΔM_R=0.0000) but specificity uncertified by one flip (p=0.0625, LOG-4491) → **line CLOSED** per pre-registered stop rules (no re-run, no larger population, no third readout).
- **Design lesson banked [FACT]:** the S4-8 N1 amendment's O ≤ 0.5 foil-overlap gate is a *validated* design lesson — EXP105's F arm went non-diagnostic at O=0.571 exactly as the gate anticipated (LOG-4491). v83 should name it as such; it is the paper's best evidence that the pre-registration machinery caught a real failure mode in advance.
- **Why [FACT]:** all numbers trace to LOG-4481/4483/4489/4491 and their bundles (scoreboard v1.4, LOG-4492).
- **Predicted effect:** This is the paper's strongest "we test our own instruments" story — a bench killed by its own format prior, a recalibration that worked, and a battery that missed by one flip. It converts the boundary map from a list of kills into a narrative of instrument discipline.
- **Risk:** The arc must be presented as falsification-terminal, never as capability — the honest headline (zero positive autonomous-steering signals, LOG-4492) travels with it. Risk LOW if the "line CLOSED" language is binding.

---

## PART 3 — Provenance table: every v83-planned claim → its source

| Planned claim | Source |
|---|---|
| "Decodes at 6.7× chance" (33.33/5 = 6.667) | EXP092 master table (v82 app:master, p=0.000999) |
| "Steers zero decisions" (0 flips at α=1.0) | EXP093 McNemar b=c=0, p=1.0 (v82 §sec:results) |
| EXP094–103 ledger rows + verdicts | LOG-4377, 4400, 4407, 4416, 4434, 4423, 4441, 4455, 4448, 4462 |
| S6-5 pooled bound 2.74% (5/381) | LOG-4409 |
| S6 stand-down ("the direction is the problem, not the gate") | LOG-4463/4464 (scope fence: killed per-item L11 direction, frozen Pythia-410m, EXP092-B only) |
| EXP095 5-point α dose-response, flat, REFUTED | LOG-4399/4400 (+ scope fence "no 'all strengths' claim") |
| Threshold account NOT SUPPORTED | LOG-4416 (EXP097) |
| 1/(d−r) dilution law, 1/1022 | v82 Proposition 1 + L270 |
| Item-33 decode margin 1.0133, rank 2/60 | LOG-4472 (`ITEM33_MARGIN_RECOMPUTE_2026-09-28.md` + results JSON) |
| Item-33 injection means +0.0059/−0.0076 (across items) | LOG-4472 (aggregate means +0.0059518/−0.0076361; per-item arrays never saved) |
| +0.010/−0.004 does not exist in any artifact | LOG-4472 [FACT] — hard prohibition stands |
| EXP104 Tier-0 HOLD (0.1833 < 0.25 sanity band) | LOG-4481/4482; bundle `experiments/runs/EXP104_Tier0_rank_screen/` |
| Position-A prior 30/60, p=2.02e-12 | LOG-4483; `EXP104_BENCH_AUTOPSY_2026-09-28.md` |
| EXP105 Tier-0 PASSED (0.5333, n_pop 21, tie 0.0) | LOG-4489; bundle `experiments/runs/EXP105_cloze_Tier0/` |
| EXP105 battery Refuted at step 9 (ΔM_T=+0.2381, ΔM_R=0.0, p=0.0625, O=0.571) | Battery worksheet JSON (`experiments/runs/EXP105_battery/battery_worksheet_exp105.json`, verified field-by-field this lane); LOG-4492's scoreboard record |
| N1 O ≤ 0.5 gate = validated design lesson | LOG-4479 (amendment) + LOG-4491 (O=0.571 → F non-diagnostic) |
| Honest headline (zero positive signals) | LOG-4492 (scoreboard v1.4) |

**Provenance gaps found: 0.** Every planned claim traces to a LOG entry, a bundle artifact, or v82's own text.

**Provenance caveat [FACT] (D1 correction, LOG-4506):** LOG-4491 was truncated mid-sentence; append-only repair completed at LOG-4495; the entry is now complete.

---

## PART 4 — Founder decision checklist

| # | Decision | Options | What it unlocks |
|---|---|---|---|
| (a) | **Approve building v83** | Yes / No / Defer | Yes → the v83 build lane may start from frozen v82 with Changes #1–13 as specified here, followed by mandatory Law #14 review of the v83 diff before any external use. No → v82 stays the current paper; this plan stays parked. Defer → nothing changes; the plan remains build-ready. Approving does NOT authorize: new experiments/compute, changes to signed protocols/verdicts/artifacts, softening limitations or novelty, "all strengths/layers" generalizations, arXiv submission or public posting, or violating the S6 stand-down. |
| (b) | **Item-33 vignette variant** (Change #6R) | (i) Mean-labeled margin arrow (+0.0059/−0.0076 labeled as means across items) / (ii) No margin arrow | (i) keeps the worked-example strip with the shift arrow under an explicit means label; (ii) ships decode-margin-only. Recomputation is off the table (LOG-4472: needs a 180-pass GPU re-run; no-spend rule). The +0.010/−0.004 figures are banned under both options. |
| (c) | **§sec:future cut depth** (Change #12) | (i) Boxed compression (three-bet summary + falsifiers, staged horizon as one-liners) / (ii) Full retention | (i) follows the gap analysis's credibility argument; (ii) follows the founder's standing full-vision preference. Either way the five stages keep their killers and the full vision is not deleted. |

---

## Appendix — audit trail

- **Stale items fixed:** Change #6's open precondition → resolved by LOG-4472 (infeasible; spec rewritten as #6R). Change #2's ledger → I2′ arc added. Change #8/#9 cross-references → I2′ claim-box line + position-A methods lesson.
- **New content added:** Change #13 (I2′ arc + validated N1 O-gate design lesson).
- **Contradictions found:** none — no new result contradicts any v1-planned change.
- **Provenance gaps:** 0 (see table). One caveat (D1, corrected LOG-4506): LOG-4491 was truncated; append-only repair completed at LOG-4495; the entry is now complete.
- **v82 untouched** [FACT]: no paper source was read-for-write, let alone modified, by this lane. Original plan file untouched. $0 compute.

*Lane complete 2026-09-28. Analysis only; no experiment number minted.*
