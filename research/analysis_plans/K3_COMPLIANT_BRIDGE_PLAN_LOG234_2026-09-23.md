# K3 — Law-#7-Compliant Bridge Construction Audit + Rescue Screen: FROZEN PLAN

**LOG-234 · Track-5 (AGI architecture) / Track-6 (systems) specialist · 2026-09-23**

> **FROZEN — DO NOT EXECUTE before Law #14 SIGN.**
> Execution is released only by an independent Law #14 review SIGN (reviewer assigned
> by the Research Lead; must not be the plan author). No GPU, no weights loaded, no
> forward passes have been run in the preparation of this plan.

**Cost:** Phase 0 = $0 CPU (weight algebra only, read-only model loads, zero forward
passes). Phase 1 = ≤ 240 forward passes (60 × (2 + n_supported_candidates), hard cap
400 — §8 G10), only if Phase 0 yields ≥1 Supported candidate AND the Law #14
re-verification SIGN of the Phase-0 report AND CEO GPU clearance AND the BK-04 booking.

**Scope banner:** this plan (a) audits, on CPU, whether two pinned Law-#7-compliant
bridge constructions are well-defined, statically compliant, and non-degenerate
(Phase 0 — the gate); and (b) pre-registers the GPU rescue screen of every
Phase-0-Supported candidate on the signed bench (Phase 1). It does NOT verdict K1,
K2, EXP081, or §H7; it does NOT touch EXP070 vectors (none verified — excluded from
every vector endpoint); it does NOT modify any signed artifact; it does NOT
authorize GPU before the §8 G9 release chain; it makes NO novelty claim (N1 stands);
it does NOT override EXP081's verdict authority (Law #4).

**Decision served (Law #15 Q2):** KILL / CONTINUE on the "output-side room as an
*autonomous mechanism*" hypothesis — the LOG-232 contingency: full reversal of the
narrowed §H7 demotion is contingent on a compliant construction that rescues.

---

## 0. Law #15 — the four answers (on record, before work starts)

1. **Q: What precise question does this answer?** Does a Law-#7-compliant bridge —
   constructed from premise-entity tokens only, or from donor items with the
   entity-similarity-leak control — rescue on the signed benchmark?
   Measurands: Phase 0 — per-candidate well-definedness, Law-#7 compliance by
   static token-id audit (§3, operational rule), non-degeneracy (g ≥ 0.25 floor),
   construction identity vs the signed record, geometric profile (cosines vs the
   option-informed bridge; EXP082/K1 0.9-bar machinery as descriptive checks).
   Phase 1 — per-candidate ΔM vs C1 on the signed 60-item bench (McNemar exact +
   Tango 95% CI, §G1b cells, δ_min = 0.05), with a concurrent C2 option-informed
   positive control.
2. **Decision:** **KILL / CONTINUE / HOLD.** ≥1 compliant candidate rescues
   (Tango L > δ_min) → the autonomous-mechanism reading **survives this falsifier**
   (CONTINUE; CEO revisits §H7 per the LOG-232 contingency; EXP081's discrimination
   battery remains the sole licensing authority for any transfer/capability claim).
   All tested compliant candidates NULL (McNemar p ≥ 0.05) while the concurrent
   option-informed bridge rescues at cell (1) → the "output-side room as autonomous
   mechanism" hypothesis is **Not supported** (KILL; program re-scopes to
   label-assisted steering; narrowed §H7 demotion hardens to permanent; EXP081's
   GPU release stands down pending CEO re-licensing). Anything else →
   **Inconclusive → HOLD** (§9). Phase 0 yields no Supported candidate →
   **Underdetermined** on the construction question; the GPU phase is INFEASIBLE as
   designed — do not proceed to GPU.
3. **Cheapest:** Phase 0 is $0 CPU and gates everything — a GPU run cannot answer
   whether a compliant construction *exists* and is non-degenerate. Phase 1 is
   60 × (2 + n) ≤ 240 forward passes (≤ the ~400 booked under BK-04, 0.05 T4-h),
   the minimal rescue screen: one baseline arm, one concurrent option-informed
   control, one arm per surviving candidate. No cheaper decision exists — the
   rescue question is inherently a forward-pass question, and the construction
   question is inherently a weight-algebra question. Forward-pass count:
   **Phase 0: 0. Phase 1: ≤ 240 (hard cap 400, §8 G10).**
4. **License:** §6 (L1–L4 per `research/foundations/MATHEMATICAL_LICENSE_STANDARD_2026-09-23.md`
   and the LOG-200 template). Grade: **IN-HOUSE-PROOF** for the Phase-0 algebra and
   the static compliance checks (exact, statically checkable; the computation *is*
   the proof; promotion to PROVEN-LEMMA via Law #14 SIGN + executor report
   reproducing the L1 proofs); **CONJECTURE-UNDER-TEST** for the Phase-1 causal
   upshot (a compliant-direction rescue ⇒ autonomous-mechanism reading survives) —
   assumption A2 (mid-network propagation) is undischarged. Weakest load-bearing
   grade = **CONJECTURE-UNDER-TEST** → authorizes the cheapest discriminating
   experiment only — which K3 (CPU gate + ≤240-pass screen) is. (INTUITION nowhere;
   the protocol starts.) The Law #14 reviewer verifies the grade.

---

## 1. Standing context (facts the plan inherits, not re-derives)

- LOG-197: Q1 = **Supported** (bridge = `normalize(E[target] − E[foil])`, option-informed
  on the letter of Law #7 — non-compliant as an autonomous-mechanism construction);
  Q2 = **Supported-narrow-L1** ("readout path causally accessible to an option-informed
  direction; NOT L2, NOT L3"); CI method identified as Tango (1998) exact score interval,
  reproduced to 4dp before use. [FACT — `research/analysis_plans/LAW7_BRIDGE_AUDIT_REPORT_LOG197_2026-09-23.md`]
- K1 (LOG-213) + EXP082 (LOG-217): both directional-tilt accounts killed (0/60 every run).
  The LOG-204 demotion is narrowed to Q1 alone per `research/analysis_plans/H7_DECISION_BRIEF_LOG232_2026-09-23.md`
  (DRAFT for CEO acceptance): bridge stays "rescue control (known-answer direction), NOT a
  mechanism control"; full reversal contingent on K3 — "only a Law-#7-compliant construction
  that rescues could rehabilitate the bridge as an autonomous-mechanism control."
- EXP081 v2 (`experiments/protocols/C-A_DONOR_TRANSFER_PREREG_SPEC_V2.md`, signed LOG-182):
  the donor-centroid construction is pinned — 20 donors (§3.1 donor table), "outranks"
  template, sum-of-differences-then-normalize (§4.1), degeneracy floor g ≥ 0.25 with
  **g(C3) = 1.061783 [FACT — computed]**, similarity audit s_t/s_f with **all |cos| < 0.1
  [FACT — computed]** (donor centroid near-orthogonal to every test target row), donor
  token pool disjoint from the 10-token test pool by construction, and the binding Law #7
  statement (§3.3): donor labels are support-side construction material only; test items
  are unlabeled at intervention time; the fixed bank-level centroid is identical for all
  60 items. K3's candidate (ii) reuses this signed construction **verbatim** — no re-design.
- The signed bench: N = 60 Planetary/Elemental 2-hop/3-hop items, ids
  `exp077_planet_2hop_0..14`, `exp077_planet_3hop_0..14`, `exp077_element_2hop_0..14`,
  `exp077_element_3hop_0..14`; per item `prompt`, `A` (target), `C` (foil); correct ⟺
  chosen == `A`; binary argmax over single-token `" A"` vs `" C"` encodings at the final
  position (`run_exp077.py` ll. 669–682). 3-hop items carry four premise entities
  `(A, B, C, D_ent)` with rank A > B > C > D_ent; 2-hop items carry three `(A, B, C)`
  with rank A > B > C (`run_exp077.py` ll. 586–636, the four bench-construction loops;
  executor records the exact quad-loop sub-ranges). [FACT — code read]
- Split-record invariant (LOG-197 F1 lesson, binding): the EXP077 CPU-smoke archive
  (b=14, c=0, ΔM=+0.2333, p=0.000122) and the official GPU record
  (**b=6, c=0, ΔM=+0.1000, p=0.03125** per LOG-128) are two different runs — never
  cross-compared. This plan cites the **official record only** for C2's rescue
  precedent. [DEFINITION — standing invariant]
- EXP070: **excluded from all vector endpoints** (no verified `exp070_vectors` record
  anywhere — LOG-197 E3; Underdetermined, never filled by assumption). K3 touches
  nothing from EXP070.
- Evidentiary levels (standing law, mentorship directive P1): "can improve inference"
  (Level 1) ≠ "changes computational strategy" (Level 2) ≠ "creates qualitatively new
  capability" (Level 3) — **no silent crossing**. K3's rescue verdict licenses at most
  Level 1 narrow; no Level-2/3 language appears anywhere in this plan or its executor
  reports. Permitted verdicts only: **Supported / Not supported / Inconclusive /
  Underdetermined / Refuted** (LOG-148). "Promising", "interesting", "worth another
  experiment" are forbidden in executor outputs.

---

## 2. Data sources (exact)

- **Item premise entities:** verbatim ports of the runner's bench-construction code
  (`experiments/runs/exp077/run_exp077.py` ll. 586–636): the two quad loops yield
  `(A, B, C, D_ent)` per 3-hop item; the non-option premise pair is `(B, C)` with
  prompt rank B above C. Target/foil label strings via the LOG-197 E1 procedure
  (`tokenizer.encode(" " + item["A"])[0]`, `" " + item["C"]`; EXP065/066 fields carry
  the leading space already). [FACT — code read]
- **Cross-check (guard §8 G4):** rebuilt (B_i, C_i, target_i, foil_i) strings must be
  byte-consistent with archived per-item records where they exist (EXP077 smoke
  `exp077_instance_records.json` `ent`/`typ` fields; LOG-197 established the runners'
  item definitions are byte-identical 60/60). Any mismatch = FATAL.
- **Donor bank (candidate ii):** the 20-donor pinned table, EXP081 v2 §3.1 (authoritative;
  not re-transcribed here — transcription risk); donor token ids from the v2 spec's
  pinned list; expected audit values from `experiments/protocols/C-A_PREAUDIT_2026-09-23.json`
  (g(C3) = 1.061783, s_t/s_f profiles) used as the identity re-verification target (§4 E-K3-3).
- **Unembedding matrix:** `model.get_output_embeddings().weight`, read-only, from the
  pinned pythia-410m snapshot (§9). (LOG-197 established this accessor returns the identical
  matrix the runners' `model.embed_out.weight` names under transformers 5.17.) [FACT]
- **Phase-1 (b, c):** measured fresh on the GPU run (no archive citation); decision rule
  and hook pinned verbatim from EXP077 (§5).

---

## 3. Phase-0 constructions (pinned; the compliance rule is binding)

### 3.1 [DEFINITION] — Law #7 compliance, operational (statically checkable)

A bridge construction C with token-id input multiset I(C) is Law-#7-compliant iff ALL
hold, verified by static inspection of the construction code and token-id sets (no
forward passes, no behavioral criteria):

- **(C-a)** Per-item role-relative: for each evaluated test item i, no id in I(C)
  is the token id of item i's *own* target-answer token (the item's `"A"` field).
  Operationally: {premise ids on item i} ∩ {target_i, foil_i} = ∅ per item.
- **(C-b)** Per-item role-relative: for each evaluated test item i, no id in I(C)
  is the token id of item i's *own* foil/candidate-option token (the item's
  `"C"` field).
- **(C-c)** No id in I(C) is a test label symbol or derived from the evaluation
  objective / scoring rule.
- **(C-d)** No id in I(C) comes from a held-out or future instance. Donor items are the
  licensed exception per the signed EXP081 v2 §3.3 Law #7 statement (support-side
  construction material; donor labels flow only into centroid construction, never into
  the evaluation objective); the donor token-id set is additionally verified disjoint
  from all test target/foil token ids.
- **(C-e)** Premise-non-option tokens of the evaluated items are permitted inputs
  (present-instance prompt material — not labels, not future instances). Bank-level
  aggregation additionally dissolves per-item identity: the constructed direction
  carries zero per-item information.

The executor verifies (C-a)–(C-e) by enumerating token-id sets from verbatim ports and
asserting the per-item disjointnesses. Any violation = compliance FAIL on that candidate
(verdict Not supported on the candidate's compliance claim, defect named; the
construction is not repaired in place — Law #4: a repaired construction is a new plan).

**Rationale for the per-item reading (stated once — LOG-235 F-235-1):** unembedding
rows are role-free: W_U[Mars] is the identical row whether Mars serves as a premise
entity on item i or as the target answer on item j. Law #7's target is the
*answer-key role mapping* — constructing the intervention from an item's own answer
labels — not the global identity of a token id across items. A cross-item reading
would make compliance impossible on any shared-vocabulary bench (the 10-entity pool
guarantees every premise entity is some other item's target) and would conflate the
construction's information content with the vocabulary's. The executor therefore
asserts per-item disjointness and reports the cross-item collision count descriptively
in E-K3-1 ([OBSERVATION], non-gating).

### 3.2 Candidate (i) — premise-rank bank direction [HYPOTHESIS-bearing construction]

**Pinned construction.** Over the 30 3-hop items (the only items with two non-option
premise entities), with `(B_i, C_i)` the non-option premise pair ordered by prompt rank
(B_i outranks C_i):

$$\hat{b}_P \;=\; \mathrm{normalize}\!\left(\sum_{i \in \text{3-hop}} \bigl(W_U[B_i] - W_U[C_i]\bigr)\right)$$

sum-of-differences-then-normalize (the EXP081 §4.1 algebra, applied to premise pairs).
Token ids: `tokenizer.encode(" " + entity)[0]` exactly as the runners encode entities
(EXP081 v2 §2 F2 convention). Orientation higher-minus-lower is pinned; the
lower-minus-higher sign flip is a *different* direction and is not constructed.

**Why bank-level (rejected alternative, recorded):** a per-item premise direction
(b̂_i = normalize(W_U[B_i] − W_U[C_i]) injected on its own item) would be an
item-specific intervention — item identity encoded in the vector — re-opening the
Law-#7-adjacent instance-specific-information concern. The bank-level direction is
fixed and identical for all 60 items: it carries zero per-item information (not even
which item), so a rescue is unambiguously a property of the *direction*, not the
item. That is the stronger falsifier for the autonomous-mechanism question, and it
is the pinned variant. The per-item variant is **rejected with reason**, not left open.

**Why 3-hop-only (scope fact):** 2-hop items carry a single non-option premise entity
(B); no ordered pair exists without touching an option token. The bank is therefore
3-hop-scoped (30 pairs); the fixed direction is injected on all 60 bench items in
Phase 1 (a fixed unembedding-space direction needs no per-item premise to be injected).

**Compliance argument (pre-registered, executor verifies):** B_i and C_i are never item
i's own target or foil (entities A, B, C, D_ent are distinct per item; options are A
and D_ent) — (C-a)/(C-b) hold by the static token-id check; no labels enter — (C-c);
no future instances — (C-d); premise-non-option inputs are licensed by (C-e). The
construction's input multiset is drawn exclusively from premise-non-option positions.

### 3.3 Candidate (ii) — donor-centroid direction (EXP081 v2 C3, verbatim)

**Pinned construction.** Exactly EXP081 v2 §3.1/§4.1 (the 20-donor pinned table,
"outranks" template, support vocabularies V1_Anglo…V5_Modern):

$$\hat{b}_D \;=\; \mathrm{normalize}\!\left(\sum_{d \in D_{C3}} \bigl(W_U[t_d] - W_U[f_d]\bigr)\right)$$

No re-design, no re-selection, no bank surgery (the v2 degeneracy-trap warning stands:
balancing the bank would annihilate the centroid — not done, not considered).
**Compliance argument:** signed EXP081 v2 §3.3 (label-free-at-test-time by construction;
donor token pool disjoint from the test option pool — re-verified statically in
Phase 0 as E-K3-1). Phase 0 additionally re-verifies the construction *identity*
against the signed audit values (E-K3-3): a rebuild that does not match the signed
v2 centroid is not candidate (ii).

### 3.4 Data-contact statement

- Candidate (ii): g(C3), the s_t/s_f profiles, and the donor token pool are signed
  **[FACT]s** in the corpus (EXP081 v2 §4.2–§4.3, attached pre-audit). Phase 0
  **re-verifies** them as guards/identity checks (the K1-G1 pattern), not as discoveries.
- Candidate (i): the premise-rank bank direction is a **new construction** — no cosine,
  norm, or compliance fact about it exists in the signed corpus to the author's
  knowledge. Its geometry is treatment-independent; the Law #14 reviewer verifies
  no-data-contact via corpus search pre-SIGN.

---

## 4. Phase-0 endpoints (CPU; all weight algebra)

**E-K3-1 — static Law #7 compliance audit [PRIMARY GATE].** Executor enumerates, from
verbatim ports: for candidate (i), the token-id multisets {tok(B_i), tok(C_i)} over the
30 3-hop items and {tok(target_i), tok(foil_i)} over all 60 items; asserts
{B_i, C_i} ∩ {target_i, foil_i} = ∅ per item (C-a/C-b), asserts no label-derived ids
(C-c, by code inspection of the construction), asserts no future-instance ids (C-d).
For candidate (ii): asserts the donor token-id set ∩ all test {target, foil} token ids
= ∅ (C-d, second clause) and cites the signed v2 §3.3 for the donor-label flow (C-c/C-d
first clause). Report: PASS/FAIL per candidate with the violating ids named on FAIL.
[DEFINITION]-grade check; the audit *is* the proof. Additionally report (descriptive,
non-gating, [OBSERVATION]): the cross-item collision count — the number of bank
premise entities whose token id coincides with *some other* item's target/foil token
id — expected nonzero on the shared 10-entity pool; it carries no compliance weight
per the §3.1 per-item rationale.

**E-K3-2 — non-degeneracy [GATE].** Degeneracy statistic
g = ‖Σ(W_U[x] − W_U[y])‖₂/√(#pairs) (the EXP081 §4.2 floor, precedent-anchored):
**g ≥ 0.25 required** for each candidate. Report g to 6dp. Additionally (EXP082-style A8):
report min_i‖W_U[x_i] − W_U[y_i]‖₂ over the bank pairs (per-pair floor > 0 asserted,
F1-style — a zero pair is a silent no-op contribution); min/mean/max of pair norms.
g < 0.25 → candidate Not supported (degenerate — cannot bear the rescue test);
it is not repaired (Law #4).

**E-K3-3 — construction identity [GUARD].** (a) Self-consistency: |cos(rebuilt b̂,
formula rebuild from an independent code path)| ≥ 1 − 1e-6 (guards transcription error —
the K1-G1 pattern). (b) For candidate (ii): recompute g(C3) and the s_t/s_f profiles
and assert max abs deviation vs `C-A_PREAUDIT_2026-09-23.json` ≤ 1e-6 and
|g_rebuilt − 1.061783| ≤ 1e-4 — the signed record is the identity anchor; mismatch =
FATAL (the rebuild is not the signed construction). (c) Assert all 20 donor + all 60
premise-non-option entity strings are single-token as `" "+entity` (F2 verbatim from
EXP081 v2 §2); any multi-token entity → FATAL abort naming the entity.

**E-K3-4 — geometric profile vs the option-informed bridge [DESCRIPTIVE].**
For each candidate b̂_c: with b̂_i^opt = normalize(W_U[t_i] − W_U[f_i]) the
LOG-197-verified per-item option-informed bridge (scale-free),
report the distribution over i=1..60 of cos(b̂_c, b̂_i^opt) (mean/median/min/max),
and of cos(b̂_c, ŵ_{t_i}), cos(b̂_c, ŵ_{f_i}) (the similarity channel; for (ii) this
re-verifies the signed |cos| < 0.1 fact). 0.9-bar majority-CI check (EXP082 §3
machinery, descriptive here): p̂ = #{i : |cos| ≥ 0.9}/60 with exact Clopper–Pearson
95% CI. **Pre-registered reading:** a 0.9-bar firing on candidate (i) is recorded as
a caveat attached to any Phase-1 CONTINUE verdict (a label-free construction
geometrically adjacent to target-row boosting — the rescue would survive the
falsifier but the "autonomous" reading carries the caveat); it does not gate
Phase 1. For candidate (ii) the signed expectation is no firing (|cos| < 0.1);
any firing = [OBSERVATION] against the signed audit, reported, Phase-1-gating
(the identity anchor E-K3-3(b) would already have failed).

**E-K3-5 — machine-readable twin.** `K3_CONSTRUCTION_AUDIT_RESULTS_LOG234_2026-09-23.json`:
unrounded g values, per-pair norms, per-item cosine arrays, token-id audit sets,
hashes, env manifest. Plus the executor script
`K3_construction_audit_execute_LOG234_2026-09-23.py` (filed with the report;
contains no `model(...)` call on inputs — §8 G5).

---

## 5. Phase-1 design (GPU; gated — does not exist until §8 G9 releases it)

**Release precondition (binding):** plan SIGN ∧ Phase-0 report filed with per-candidate
verdicts ∧ Law #14 targeted re-verification SIGN of the Phase-0 report ∧ CEO GPU
clearance ∧ BK-04 booking confirmed. The Phase-1 executor authors
`K3_rescue_execute_LOG234_2026-09-23.py` from this frozen spec at release; no script
exists before release.

**Arms** (N = 60 signed bench; pythia-410m; injection h ← h + αb̂ at the last-token
residual stream at transformer layer-20 output — the verbatim EXP077 hook site;
decision rule = argmax over single-token `" A"` vs `" C"` at the final position,
correct ⟺ chosen == `A`, EXP077 ll. 669–682 verbatim):

| Arm | Intervention | Role |
|---|---|---|
| C1 | none | baseline |
| C2 | per-item option-informed bridge b̂_i^opt = normalize(W_U[t_i] − W_U[f_i]), α = 0.50 | concurrent positive control (EXP077 C8 config) |
| K3i | fixed premise-rank bank direction b̂_P, α = 0.50 | candidate (i) — runs iff Phase-0 Supported |
| K3ii | fixed donor centroid b̂_D, α = 0.50 | candidate (ii) — runs iff Phase-0 Supported |

α = 0.50 for all injection arms (EXP066/EXP077 precedent — the configuration under
which the option-informed bridge rescued +10pp officially; not tuned). No α grid, no
layer sweep (Law #4: scope frozen).

**Budget:** 60 × (2 + n_supported) forward passes; n = 2 → **240 passes**, within the
~400 booked under BK-04 (0.05 T4-h). Hard cap 400 — executor asserts total ≤ 400,
else FATAL (re-plan, Law #4). All vectors weight-computed; vector construction costs
zero forward passes.

**Endpoints (per candidate arm, vs C1):** McNemar exact two-sided via
`scipy.stats.binomtest` on (b, c) discordant pairs (b = C1-wrong→arm-right,
c = C1-right→arm-wrong; b = c = 0 ⇒ p = 1.0 — EXP077 harness convention);
ΔM̂ = (b − c)/60; **Tango (1998) 95% score CI** for the paired difference with
**δ_min = 0.05** (§G1b, binding — not re-derived). **Method guard:** the Tango
implementation must reproduce the four LOG-197 E4 rows
([+0.0931,+0.2803], [+0.0651,+0.2417], [+0.0338,+0.2015], [+0.1444,+0.3544]) to 4dp
before any K3 CI is computed — else FATAL (method misidentification).

**Per-arm cells (pre-registered):** **RESCUES** iff Tango L > 0.05 (cell 1 —
meaningful rescue magnitude established); **NULL** iff McNemar p ≥ 0.05 (CI includes
0 — no directional evidence); else **CELL-4** (directional, L ≤ δ_min →
Inconclusive, HELD, never converted to a negative).

**Entity-similarity-leak control (descriptive, alongside the verdict — the leak
verdict belongs to EXP081):** for K3ii the executor reports the Phase-0 s_t/s_f
profile, the pinned 49/11 low/high stratum split (EXP081 v2 §6), and within-stratum
McNemar K3ii-vs-C1 (T4-analog, descriptive only). **Pre-registered reading:** if K3ii
RESCUES but the rescue concentrates in the high-similarity stratum with the low
stratum NULL, the CONTINUE verdict carries the pinned caveat "rescue not demonstrated
where similarity is weakest — attribution to EXP081's T3/T4/T5" (the falsifier is
about Law-#7 compliance, which is satisfied; the caveat is honest labeling, not a
verdict demotion). Additionally, the v2 spec's token-prior-direction confound is
named explicitly (Law #2 completeness — LOG-235 F-235-4): a K3ii CONTINUE also
carries the pinned caveat that the donor centroid may encode a "usually-right minus
usually-wrong" token-prior direction rather than a transferable mechanism — the
rescue reading stays with EXP081's T3/T4/T5, not with K3. For K3i: report the premise-option cosine profile (E-K3-4); the
0.9-bar caveat from Phase 0, if fired, is attached to the CONTINUE reading.

**Relationship to EXP081 (binding):** K3ii-vs-C1 uses the same arm pairing as EXP081's
T1 comparison; K3's own §5 cells apply (v2's signed T1 uses the F1 agreement rule —
the needed implication K3-NULL ⇒ T1-fails holds in the safe direction) —
intentional (cheapest screen). A K3ii rescue does **not** pre-license EXP081's
H_transfer (T3/T4/T5 still decide — Law #4); a K3ii NULL is an [OBSERVATION] EXP081's
executor must read, not a verdict on H_transfer. K3's program-level KILL, however,
fires the §9 re-scope (the cheaper sufficient answer has arrived — Law #15 Q3
applied prospectively).

---

## 6. Mathematical License (binding — Law #15 Q4)

**Grade: IN-HOUSE-PROOF** for Phase-0 algebra + static compliance checks (exact;
the computation *is* the proof; promotion to PROVEN-LEMMA via Law #14 SIGN of this
plan + executor report reproducing the L1 proofs). **CONJECTURE-UNDER-TEST** for the
Phase-1 causal upshot (A2 undischarged). Weakest load-bearing grade =
**CONJECTURE-UNDER-TEST** → authorizes the cheapest discriminating experiment only.

### L1. Authorizing results
- **Readout-shift lemma [THEOREM] (licenses Phase-1's causal reading):** Let W_U ∈
  ℝ^{V×d} be the frozen unembedding matrix, x ∈ ℝ^d the final-token residual,
  ℓ = W_U x (+ constant bias, immaterial: Δℓ is bias-independent). For unit v̂ ∈ ℝ^d,
  scalar α, token y: the perturbation x ← x + αv̂ shifts the y-logit by
  **Δℓ_y = α·(W_U[y,:]·v̂) = α‖W_U[y,:]‖₂·cos(v̂, ŵ_y)**, ŵ_y = W_U[y,:]/‖W_U[y,:]‖₂.
  *Proof:* Δℓ = W_U(αv̂); take the y-th row. ∎ (K1 §6 L1; EXP082 §6 L1 — same lemma,
  cited not re-proved; the executor reproduces the three-line proof in the report.)
- **Construction identities [FACT] (license Phase-0):** b̂_P and b̂_D are exact
  normalizations of pinned unembedding-row differences; cosine is the exact
  alignment measure; g is the exact pre-normalization energy on the √(#pairs)
  scale (EXP081 §4.2 precedent). The static compliance checks are 0/1 facts about
  token-id sets — no probabilistic content.
- **Statistical machinery [ADOPTED, not re-derived]:** McNemar exact + Tango (1998)
  score CI + δ_min = 0.05 per §G1b; method identity verified by the §5 guard
  (reproduce LOG-197 E4 rows to 4dp). Evidentiary level of a Phase-1 rescue:
  **Level 1 narrow** ("a Law-#7-compliant direction can improve inference at the
  tested configuration") — NOT Level 2, NOT Level 3; no silent crossing.
- **Epistemic labels:** [THEOREM] for the lemma; [FACT] for signed audit values and
  code-read facts; [DEFINITION] for the §3.1 compliance rule and endpoint cells;
  [HYPOTHESIS] for H_compliant ("a Law-#7-compliant bridge rescues on the signed
  bench"); [CONJECTURE] for the causal upshot (see A2) and for "rescue ⇒ autonomous
  mechanism" (the KILL/CONTINUE verdicts are verdicts on H_compliant, not proofs of
  mechanism).

### L2. Quantitative prediction
- **Phase 0:** compliance = exact PASS/FAIL (0/1 — no threshold judgment);
  non-degeneracy g ≥ 0.25 (precedent-anchored floor, EXP081's signed gate — not
  tuned to K3 data; candidate (i) has no data contact); identity tolerances
  1−1e-6 (cosine) / 1e-6 (audit-value match) / 1e-4 (g vs 1.061783).
  **No point forecast is registered** (Law #2) — the predictions are the
  threshold/gate tests.
- **Phase 1:** under H_compliant, ≥1 candidate arm lands in cell (1) (Tango L >
  0.05). Under the null, candidate arms are McNemar-NULL while C2 lands in cell (1)
  (the KILL conjunction). **No point forecast** (Law #2).

### L3. Breaking point
- **Falsifying observation (H_compliant):** all tested compliant candidates NULL ∧
  C2 in cell (1) (procedure valid, option-informed rescue at meaningful magnitude).
  **Decision: KILL** — "output-side room as autonomous mechanism" is Not supported;
  §9 re-scope fires.
- **Surviving observation:** ≥1 compliant candidate in cell (1).
  **Decision: CONTINUE** — the autonomous-mechanism reading survives this falsifier;
  §9 consequences fire (CEO revisits §H7; EXP081 remains the licensing authority).
- **Otherwise → Inconclusive → HOLD** (§9); **no Supported candidate in Phase 0 →
  Underdetermined** on the construction question → GPU INFEASIBLE, do not proceed.
- **Falsifying observation (license itself):** any §8 guard trips (compliance audit
  unexecutable, identity mismatch, Δθ=0 mismatch, Tango method-identity failure,
  budget-cap breach) → license misgraded → halt; measurements Refuted; no verdict.
- **Outcome partition:** §7's tables map every cell of {compliance} × {g} ×
  {identity} × {guards} (Phase 0) and {candidate cell} × {C2 cell} × {guards}
  (Phase 1) to exactly one of the five verdict categories (Charter M5.2).

### L4. Assumption inventory
- **A1 — item/premise labels:** verbatim ports of the runner's bench-construction
  code; `tokenizer.encode(" "+label)[0]` exactly as the runners call it. Discharge:
  §8 G4 cross-check vs archived per-item records; mismatch = FATAL.
- **A2 — mid-network propagation (UNDISCHARGED) [CONJECTURE]:** the Phase-1 causal
  upshot assumes the layer-20 injection's decision effect preserves the sign of the
  L1 readout projection (downstream layers don't reverse it). Not discharged by K3 —
  this is K2's bypass-vs-routing question. Caps the causal-upshot license at
  CONJECTURE-UNDER-TEST. The Phase-0 geometric/compliance endpoints do NOT need A2.
- **A3 — run pins:** all constructions use the pinned pythia-410m snapshot (§9);
  Δθ=0 pre/post SHA-256 via the verbatim `get_hash` formulation (see §9 — the
  EXP082-D1 lesson: the formulation is named, not assumed); executor cross-checks
  vs the archived `ec276abe…` hash. Mismatch = FATAL.
- **A4 — EXP070:** excluded from all vector endpoints (no verified vectors);
  Underdetermined cells, never filled by assumption.
- **A5 — binary scoring:** verified by code read (EXP077 ll. 669–682); grounds the
  ΔM/McNemar endpoints.
- **A6 — α/l\*/hook/dtype pinned by precedent** (EXP066/EXP077 config: α = 0.50,
  l\* = 20, last-token residual stream at layer-20 output, torch.float32) — not tuned,
  not swept (Law #4).
- **A7 — premise-bank orientation:** higher-minus-lower by prompt rank order, pinned;
  the sign-flipped variant is a different direction and is not constructed (rejected
  alternative recorded in §3.2).
- **A8 — non-degeneracy diagnostics** (per-pair norm floors, E-K3-2/E-K3-4 profiles)
  reported as [OBSERVATION]; a firing diagnostic never promotes a verdict, a
  failing gate never kills beyond its pre-registered cell.
- **A9 — donor-identity anchor:** candidate (ii) is the signed v2 C3 construction;
  E-K3-3(b) mismatch = FATAL (no silent redefinition). If the v2 spec is ever
  amended, K3 must be re-registered (Law #4).
- **A10 — per-item independence for CIs:** the 60 per-item trials are treated as
  independent Bernoulli trials; any within-run dependence (shared prompt templates)
  is not modeled — CIs are nominal; disclosed, not hidden (EXP082 A7 precedent).
- **A11 — K3-(ii) vs EXP081 jurisdiction:** K3's donor verdict is an [OBSERVATION]
  for EXP081, never a verdict on H_transfer (Law #4; §5).
- **A12 — data contact:** candidate (ii) audit values are signed [FACT]s re-verified
  as guards; candidate (i) geometry has no data contact (Law #14 verifies via corpus
  search pre-SIGN); the compliance token-id sets are 0/1 static facts, not tuned.
- **Promotion path:** IN-HOUSE-PROOF → PROVEN-LEMMA on Law #14 SIGN of this plan +
  executor report reproducing the L1 proofs; CONJECTURE-UNDER-TEST promotes only via
  downstream propagation evidence (K2-class) — never by re-labeling.

---

## 7. Verdict mapping (exhaustive — every outcome cell mapped)

### 7.1 Phase-0 per-candidate verdicts

| E-K3-1 compliance | E-K3-2 (g ≥ 0.25) | E-K3-3 identity | Guards | Per-candidate verdict |
|---|---|---|---|---|
| PASS | ≥ 0.25 | pass | pass | **Supported** — viable compliant candidate; Phase-1-eligible |
| PASS | < 0.25 | pass | pass | **Not supported** — degenerate; cannot bear the rescue test (defect named; no repair in place) |
| FAIL (ids named) | any | any | pass | **Not supported** — not Law-#7-compliant as specified (defect named; Law #4: repair = new plan) |
| cannot complete (items named) | — | — | pass | **Inconclusive** — audit uncompletable as specified |
| — | — | — | **fail** | **Refuted** (integrity failure; halt; no claim licensed) |

**Program-level Phase-0 aggregation (pre-registered):** PROCEED iff ≥1 candidate lands
**Supported**. Otherwise the construction question is **Underdetermined** → the GPU
phase is INFEASIBLE as designed → do not proceed to GPU (§9 consequences).

### 7.2 Phase-1 program verdict (only if PROCEED + §8 G9)

| Candidate arm cell(s) | C2 cell | Program verdict |
|---|---|---|
| ≥1 candidate RESCUES (cell 1) | cell 1 (L > 0.05) | **Supported** (H_compliant) → **CONTINUE** |
| ≥1 candidate RESCUES (cell 1) | cell 4 or p ≥ 0.05 | **Inconclusive** → HOLD (positive control failed; neither CONTINUE nor KILL licensed — LOG-235 F-235-2) |
| all tested candidates NULL | cell 1 (L > 0.05) | **Not supported** (H_compliant) → **KILL** |
| all tested candidates NULL | cell 4 or p ≥ 0.05 | **Inconclusive** → HOLD (KILL conjunction not established: C2's meaningful-magnitude rescue is the load-bearing conjunct — mirrors EXP081's T2 headroom-gate logic) |
| ≥1 candidate CELL-4, none RESCUES | any | **Inconclusive** → HOLD |
| — | — | **Refuted** on any guard failure (halt; no verdict) |

Mixed RESCUES + NULL across candidates → CONTINUE (the question is existential: a
compliant bridge *can* rescue); per-candidate readings recorded separately; the NULL
candidate's reading is an [OBSERVATION] for its own lineage (donor NULL → EXP081's
executor reads it; premise NULL → recorded).

**Guards-fail → Refuted takes precedence over all endpoint cells** (Law #13 —
integrity failure voids measurements).

---

## 8. Guards (FATAL on failure — halt, no verdict, report)

- **G1.** E-K3-1 static audit executes exactly as §3.1/§4; any token-id-set
  enumeration the executor cannot complete as specified → candidate Inconclusive
  (§7.1 row 4), never silently skipped.
- **G2.** E-K3-3 identity: self-consistency |cos| ≥ 1−1e-6; candidate (ii) audit-value
  match ≤ 1e-6 / |g − 1.061783| ≤ 1e-4. Mismatch = FATAL.
- **G3.** Δθ=0: pre/post SHA-256 match via the verbatim `get_hash` formulation
  (**named per the EXP082-D1 lesson:** `run_exp077.py` ll. 166–172 — SHA-256 over the
  concatenation of `state_dict()` tensors, sorted keys, CPU, float32 bytes) AND match
  the archived `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed`.
  Any mismatch = FATAL, results not reported (Law #6/#13).
- **G4.** Label/premise cross-check (§2): any item mismatch vs archived per-item
  records = FATAL.
- **G5.** Phase 0: **no forward pass at any step** (executor asserts; code inspection —
  the script contains no `model(...)` call on inputs). Phase 1: forward passes only
  inside the released executor, counted, capped.
- **G6.** F2 single-token guard (verbatim EXP081 v2 §2): every donor and premise entity
  single-token as `" "+entity`; any multi-token entity → FATAL abort naming the entity.
- **G7.** F1-style norm asserts: every bank pair ‖W_U[x] − W_U[y]‖₂ > 0; every injection
  vector norm > 0 (Phase 1). Zero = FATAL (silent no-op).
- **G8.** Phase-1 pins asserted in-script: model = pinned 410m snapshot, α = 0.50,
  l\* = 20, hook = last-token residual stream at layer-20 output, torch.float32,
  decision rule verbatim EXP077 ll. 669–682. Any deviation = FATAL.
- **G9.** Phase-1 release chain (binding): plan SIGN ∧ Phase-0 report filed ∧ Law #14
  targeted re-verification SIGN of the Phase-0 report ∧ CEO GPU clearance ∧ BK-04
  booking confirmed. **No GPU before all five.**
- **G10.** Phase-1 budget cap: total forward passes ≤ 400 (pinned expectation 240);
  exceed → FATAL, re-plan (Law #4).
- **G11.** Tango method-identity guard (§5): reproduce the four LOG-197 E4 rows to 4dp
  before any K3 CI is computed; failure = FATAL.

**Banned language:** only the five permitted verdicts. "Promising", "interesting",
"worth another experiment" forbidden in executor outputs. p-values alone license
nothing (§G1b standing ban). Inconclusive is never converted to a negative; a
diagnostic never fires a kill.

### 8.1 Δθ=0 guard + exact environment pin

| Item | Pin |
|---|---|
| Env | `/home/hatch/workspace/.venv_smoke`: torch **2.14.0+cpu**, transformers **5.17.0**, numpy **2.5.3**, scipy **1.18.1** — asserted in-script, exact (LOG-197 §0 precedent) |
| Models | `EleutherAI/pythia-410m` snapshot `9879c9b5f8bea9051dcb0e68dff21493d67e9d4f` (**the K3 pin — all constructions and both phases use 410m only**); `EleutherAI/pythia-160m` snapshot `50f5173d932e8e61f858120bcb800b97af589f46` listed for record completeness, not loaded by K3; `local_files_only`, `trust_remote_code=False`, `torch_dtype=torch.float32`, `model.eval()` |
| Hash | verbatim `get_hash` (**formulation named per the EXP082-D1 lesson:** `run_exp077.py` ll. 166–172 — SHA-256 over the concatenation of `state_dict()` tensors, sorted keys, CPU, float32 bytes); pre/post + cross-check vs archived `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed` (full 64-hex in the G1/LOG-197 archives) |
| Forward passes | Phase 0: **0** (G5). Phase 1: ≤ 240 expected, hard cap 400 (G10) |
| Seeds | deterministic; Phase 0 consumes no RNG (recorded as such); Phase 1 pins `SEED_TORCH=SEED_NUMPY=20260923` (EXP078 precedent) for harness determinism — no RNG-dependent construction |

---

## 9. Pre-registered consequences (not new decisions)

- **Phase-0 PROCEED (≥1 Supported):** the supported candidate(s) advance to the §8 G9
  release chain. Nothing else changes; no verdict on H_compliant yet.
- **Phase-0 UNDERDETERMINED (no Supported candidate):** GPU phase INFEASIBLE as
  designed — do not proceed to GPU. The §H7 narrowed demotion hardens into the
  permanent record (LOG-232 §4 contingency: "If K3 finds no compliant construction,
  the narrowed demotion hardens"). EXP081's queue position returns to the CEO
  (K3's donor-construction verdict is an [OBSERVATION] for EXP081, not an override —
  Law #4). Reported as Underdetermined on the construction question, never as a
  negative on the rescue question.
- **Phase-1 CONTINUE (H_compliant Supported):** the autonomous-mechanism reading
  survives this falsifier. CEO revisits the §H7 narrowed demotion (the LOG-232
  contingency fires). EXP081's T3/T4/T5 battery remains the **sole licensing
  authority** for any transfer/capability claim — K3 licenses at most Level 1 narrow
  ("a Law-#7-compliant direction can improve inference at the tested configuration"),
  never Level 2/3, never H_transfer. Sprint-3 / EXP080 queue ordering unchanged. Any
  Phase-0 0.9-bar or stratum-concentration caveat is attached to the CONTINUE reading
  in the report. The bridge's "rescue control (known-answer direction), NOT a mechanism
  control" status is not restored by K3 alone — restoration needs the CEO's §H7
  re-ruling with EXP081's attribution data.
- **Phase-1 KILL (H_compliant Not supported):** the "output-side room as autonomous
  mechanism" hypothesis is Not supported. The program re-scopes to **label-assisted
  steering** (P1 fires per the Law #15 record). The narrowed §H7 demotion hardens to
  permanent. EXP081's GPU release is **stood down pending CEO re-licensing** (the
  cheaper sufficient answer has arrived — Law #15 Q3 applied prospectively; EXP081's
  T1 question is answered). Sprint-3 Stage-0 pilots re-scoped: their bridge positive
  class stays label-informed (already their pre-registered status — no verdict changes).
- **Phase-1 INCONCLUSIVE → HOLD:** battery holds; EXP081 queue unchanged; Sprint-3
  pilots proceed with the compliant-bridge question explicitly **[OPEN]** in their
  interpretation notes; no pivot fires on an inconclusive cell.
- **REFUTED (either phase):** no verdict; executor reports the integrity failure; CEO
  decides. Nothing downstream moves on a refuted measurement.

---

## 10. Execution protocol (for the executors, post-SIGN — step by step)

### Phase-0 executor (post plan-SIGN)

1. Assert env (§8.1 table: versions exact); load the pinned pythia-410m snapshot
   read-only (`local_files_only`, `trust_remote_code=False`, `torch.float32`,
   `model.eval()`); G3 pre-hash gate (verbatim formulation; cross-check vs archived).
2. Port the bench-construction loops verbatim (`run_exp077.py` ll. 586–636; record
   exact quad-loop sub-ranges); rebuild (B_i, C_i, target_i, foil_i) per item; G4
   cross-check vs archived per-item records; G6 single-token assert on every entity.
3. E-K3-1: enumerate token-id sets; assert (C-a)–(C-e) per candidate; record PASS/FAIL
   with violating ids on FAIL.
4. Build b̂_P (30 3-hop pairs) and b̂_D (20 pinned donors, v2 §3.1 table); E-K3-2:
   g values to 6dp, per-pair norm floors (G7 asserts); E-K3-3: self-consistency +
   (ii) audit-value match; E-K3-4: cosine profiles vs b̂_i^opt and option rows +
   0.9-bar majority-CI descriptives.
5. G5 assert (no `model(...)` call on inputs anywhere in the script); G3 post-hash.
6. Write the machine-readable twin JSON (unrounded values, per-item arrays, token-id
   audit sets, hashes, env manifest) + the Phase-0 report with the §7.1 verdict table
   filled verbatim; report in FACT/INFERENCE/HYPOTHESIS/SPECULATION + the 10-label
   standard; evidentiary level L0 (instrument provenance) / L1 (geometry) — no L2/L3.
7. File the report; notify the Research Lead for the Law #14 targeted re-verification
   SIGN (pre-assigned reviewer, independent of the executor).

### Phase-1 executor (post G9 release chain — §8 G9)

1. Verify the five G9 release conditions on record; abort otherwise.
2. Assert env (§8.1 table); load pinned 410m snapshot on the GPU lane (`torch.float32`);
   G3 hash gate via the verbatim formulation (CPU-moved state_dict); G8 pin asserts;
   G11 Tango method-identity reproduction.
3. Load the Phase-0-SIGNED candidate vectors from the twin JSON (no recomputation
   drift — byte-compare vs the JSON's stored vectors; mismatch = FATAL).
4. Run arms C1, C2, and each Phase-0-Supported candidate arm on the 60-item bench
   (decision rule verbatim EXP077 ll. 669–682); count forward passes; G10 cap assert;
   G7 injection-norm asserts; G3 post-hash.
5. Compute per-arm McNemar exact + ΔM̂ + Tango 95% CI; apply §5 cells; fill the §7.2
   verdict table verbatim; compute the descriptive leak-control stratum readouts.
6. Write `K3_RESCUE_RESULTS_LOG234_2026-09-23.json` + report; evidentiary level L1
   narrow; no Level-2/3 language; five permitted verdicts only.

---

## 11. What this plan does not do (binding scope)

No forward passes in Phase 0; no Phase-1 verdict before the §8 G9 release chain; no
EXP070 vector endpoints (Underdetermined, excluded); no signed-artifact edits; no
novelty claim (N1 stands); no EXP081 override (K3's donor reading is an
[OBSERVATION] for EXP081, never a verdict on H_transfer); no third construction
(a new compliant construction = a new plan, Law #4); no per-item premise variant
(rejected with reason, §3.2); no α/layer/hook sweep; the executor may not convert
Inconclusive into a negative, nor a diagnostic into a kill, nor a Phase-0
Supported into a Phase-1 rescue claim.

---

## 12. Knowledge-protocol obligations (one challenge + one idea)

- **Challenge:** candidate (i)'s orientation (higher-minus-lower) is derived from the
  prompt's rank relation ("outranks"/"is lower than" wording). A critic could argue
  the rank relation is the very relational structure the autonomous-mechanism
  question is about — making (i) "relation-informed" though label-free. The plan's
  standing answer: Law #7's letter governs labels, option tokens, and future
  instances — not prompt relations — and the §3.1 static rule is satisfied exactly.
  The observation is recorded here (not smoothed over); the Law #14 reviewer may rule
  that a sign-flip sensitivity belongs in a follow-up plan (new number, Law #4).
- **Idea:** the E-K3-4 profile — cos(b̂_c, b̂_i^opt) over 60 items — is a reusable
  program asset beyond K3: it quantifies how much of the option-informed bridge's
  direction is recoverable from label-free constructions, i.e. a direct measure of
  the "label-free headroom" in unembedding space. Either outcome (high or low
  alignment) pays for its line in the plan: high alignment bounds the label-free
  ceiling; low alignment with a rescue would be the autonomous-mechanism signal.

---

*Author: Track-5/Track-6 specialist (LOG-234) · 2026-09-23 · FROZEN pending
independent Law #14 review SIGN (reviewer assigned by the Research Lead; must not
be the plan author). Experiment number: none consumed (K3 is the battery slot, not
a new experiment). On SIGN, the Phase-0 executor works §10 verbatim; any deviation
is logged per the deviation protocol (F3-class table-precision corrections allowed
with disclosure; endpoint/environment/margin/compliance-rule changes are never F3).
Phase 1 does not exist until the §8 G9 release chain completes.*

**FROZEN — DO NOT EXECUTE before Law #14 SIGN.**
