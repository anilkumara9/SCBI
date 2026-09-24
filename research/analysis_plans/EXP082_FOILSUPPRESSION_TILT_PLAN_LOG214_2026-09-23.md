# EXP082 — Foil-Suppression Tilt Falsification: FROZEN PLAN

**LOG-214 · Track-8 (Experimental Statistician) · 2026-09-23**
**Status:** FROZEN — pending Law #14 review. **DO NOT EXECUTE before Law #14 SIGN (LOG-215, pre-assigned).**
**Cost:** $0 CPU. Zero forward passes. Read-only weight-tensor reads only.
**Scope banner:** this plan pre-registers, computes, and verdicts the foil-suppression-tilt
question (EXP082's own HYPOTHESIS), with K1(a)'s measurand recomputed as a contrast
endpoint under this plan's own rationale. It is a NEW experiment, not a continuation of
K1: it inherits NOTHING from K1's battery (CEO ruling LOG-212). It does NOT verdict K1's
battery, does NOT decide §H7, does NOT touch EXP070 vectors (none verified — excluded),
does NOT modify any signed artifact, does NOT authorize GPU, and makes NO novelty claim
(N1 assumed).
**Relationship to K1 (jurisdiction, stated once):** EXP082's (a)-contrast computation and
K1's (a) verdict are the same number computed under two independent registrations.
Neither inherits the other's verdict; EXP082's (a)-contrast cell carries NO K1 kill
authority (K1's kill authority lives in K1's battery, LOG-205/REV1). The joint
interpretability the CEO ordered is a 2×2 *outcome partition* (§5), not a shared verdict.

---

## 0. Law #15 — the four answers (on record, before work starts)

1. **Q: What precise question does this answer?** On which items, if any, does the
   bridge's rescue power come from FOIL SUPPRESSION — the injected direction driving the
   *foil* token's logit down (b̂_i ≈ −ŵ_{f_i}), flipping argmax to the target — rather
   than TARGET BOOST (b̂_i ≈ ŵ_{t_i})? Measurand: per-item
   d_i = cos(−b̂_i, ŵ_{f_i}) vs the pre-registered 0.9 bar, with exact Clopper–Pearson
   95% CI and the majority rule mirroring K1(a)'s structure; the (a)-contrast
   c_i = cos(b̂_i, ŵ_{t_i}) is recomputed alongside for the jointly-interpretable 2×2
   partition (§5). This is NOT a "persistence" question (LOG-212; the persistence
   framing is struck as geometrically inaccurate) — it is a distinct, near-mutually-
   exclusive per-item geometric claim.
2. **Decision:** **KILL / PIVOT / HOLD** — (f) Supported → **PIVOT** the tilt-
   interpretation sub-workstream (downstream characterization must model a foil-directed
   readout shift; the exclusive "target boost" framing is withdrawn); (f) Not supported
   → **KILL** the foil-suppression-tilt hypothesis for these runs (the broader readout-
   tilt question continues under K1's battery, unaffected); Inconclusive → **HOLD**;
   Refuted → halt, CEO decides.
3. **Cheapest:** $0 CPU, archived artifacts + read-only weight reads, zero forward
   passes. No cheaper decision exists — a GPU run cannot answer a geometric question
   about already-archived constructions; the (f) cosine, the (a)-contrast, the
   norm-ratio bound, and the joint-firing lemma check are all weight algebra.
   Forward-pass count: **0**. GPU is not needed (nothing below requires one); no GPU
   spend is registered.
4. **License:** §6 (L1–L4 per
   `research/foundations/MATHEMATICAL_LICENSE_STANDARD_2026-09-23.md`); the Law #14
   reviewer verifies the grade.

---

## 1. Standing context (facts the plan inherits, not re-derives)

- LOG-197: Q1=Supported (bridge = normalize(E[target]−E[foil]), option-informed on the
  letter of Law #7), Q2=Supported-narrow-L1 ("readout path causally accessible to an
  option-informed direction; NOT L2, NOT L3"). [FACT —
  `research/analysis_plans/LAW7_BRIDGE_AUDIT_REPORT_LOG197_2026-09-23.md`]
- LOG-206 §1(ii)(b) (reviewer-derived, independently recomputed): (a)-firing requires
  ‖w_f‖ ≤ 0.484‖w_t‖ (at cosθ=0); the MIRROR condition ‖w_t‖ ≤ 0.484‖w_f‖ is
  foil-row dominance — the bridge ≈ −ŵ_f, suppressing the foil logit rather than
  boosting the target. Per item the two are near-mutually-exclusive (joint firing
  needs anti-aligned rows). [THEOREM — reviewed derivation; EXP082 proves the mirror
  lemma in-house in §6]
- LOG-212 (CEO ruling, option iii): the foil-suppression phenomenon earns its OWN
  fresh pre-registration with its own rationale; EXP082 inherits nothing from K1.
  The adopted (b) flip-count reading is BACKWARDS vs the L1 license — a standing
  correction: no future tilt verdict may lean on it; the L1-aligned reading
  (f = 0 is the tilt-predicted pattern) is the honest one. [FACT —
  `reports/research_log.md` LOG-212]
- LOG-200 (foundations standard): license template, grade rubric, F-200-2 run-pin
  correction (every license names the run-pinned matrix). [DEFINITION — binding]
- EXP082 has had **no data contact** on its measurands: the per-item foil cosine
  cos(−b̂_i, ŵ_{f_i}) was never computed anywhere in the signed corpus (corpus search
  2026-09-23: no file computes it; the struck K1 (c1) formulation was never executed).
  The 0.9 bar is treatment-independent, mirrored from K1(a)'s pre-registered bar. [FACT]

### 1.1 Substrate pins (run-pinned; F-200-2)

| Run | Model (executed) | Layer | d | α_run | N | (r, f)=(b, c) primary | ΔM̂ [Tango 95% CI] | §G1b cell |
|---|---|---|---|---|---|---|---|---|
| EXP065 | `EleutherAI/pythia-160m` | 10 | 768 | 1.0 | 60 | (10, 0) | +0.1667 [+0.0931, +0.2803] | (1) L > δ_min |
| EXP066 | `EleutherAI/pythia-410m` | 20 | 1024 | 1.0 | 60 | (8, 0) | +0.1333 [+0.0651, +0.2417] | (1) L > δ_min |
| EXP077 | `EleutherAI/pythia-410m` | 20 | 1024 | 0.5 | 60 | (6, 0) official GPU | +0.1000 [+0.0338, +0.2015] | (4) Inconclusive |
| EXP077 | (smoke, secondary) | 20 | 1024 | 0.5 | 60 | (14, 0) | +0.2333 [+0.1444, +0.3544] | labeled secondary |

Archived Δθ=0 (pre==post): EXP065 `54c88fa4897785f2…`, EXP066 `4c242d9ac702a402…`,
EXP077 `ec276abe3902fab0…` (full hashes in §8; executor re-verifies verbatim).
Archived aggregate logit shifts [OBSERVATION — records]: EXP065 Δℓ_t=+0.3597,
Δℓ_f=−0.4042; EXP066 Δℓ_t=+0.3448, Δℓ_f=−0.4044. EXP077 official: no archived
logit shifts — recorded as unavailable, never filled by assumption.
EXP070: **excluded from all endpoints** (no verified `exp070_vectors` record
anywhere — LOG-197 E3). Its cells are Underdetermined, never filled by assumption.

---

## 2. Data sources (exact)

- **Item (target, foil) label strings:** verbatim ports of the runners'
  item-construction code (the LOG-197 E1 procedure, re-verified as a guard in §7):
  EXP065 `experiments/scripts/run_exp065_temporary_coordinate_alignment.py`
  ll. 258–259, 286–287, 315–316, 343–344 (`"target_token": " " + true_target`,
  `"foil_token": " " + true_foil`); EXP066 `run_exp066_pythia410m_replication.py`
  ll. 251–252, 279–280, 308–309, 336–337; EXP077 `runs/exp077/run_exp077.py`
  ll. 600/613/623/636 (`"A"`, `"C"`; A=target, C=foil per l. 588) with
  ll. 725–727 (`tokenizer.encode(" " + item["A"])[0]`).
  Token ids: `tokenizer.encode(" " + label)[0]` exactly as the runners call it
  (EXP065/066 fields already carry the leading space).
- **Cross-check (guard, §7):** rebuilt label strings must be byte-consistent with
  archived per-item records where they exist (EXP066 `exp066_instance_evaluations.json`
  prompts; EXP077 smoke `exp077_instance_records.json` `ent`/`typ` fields; LOG-197
  established the four runners' item definitions are byte-identical 60/60).
  Mismatch on any item = FATAL (no results reported).
- **Unembedding matrix:** `model.get_output_embeddings().weight`, read-only, from the
  RUN-PINNED snapshot (§8). (LOG-197 established this accessor returns the identical
  matrix the runners' `model.embed_out.weight` names under transformers 5.17.)
- **Flip counts (f = c_archived):** EXP065 `exp065_results.json →
  stage_B_confirmatory_results.Same_Layer_Output_Bridge.(rescues_b, corruptions_c)`;
  EXP066 `exp066_replication_results.json → stage_B_conditions.Same_Layer_Output_Bridge.
  (rescues_b, corruptions_c)`; EXP077 official GPU record per LOG-197 E4 pin
  (b=6, c=0 — cited from `reports/research_log.md` LOG-128); smoke
  `exp077_results.json → stage_B_conditions.C8_bridge` as labeled secondary.
  Archived [FACT — records]: (r, f) = (10, 0) / (8, 0) / (6, 0 official) / (14, 0 smoke).

---

## 3. Endpoint (f) — geometric foil-suppression test [PRIMARY]

**Computation (per run, per item i = 1..60):**
b̂_i = normalize(E_run[t_i] − E_run[f_i]) — the LOG-197-verified construction,
scale-free (α drops out of the cosine);
d_i = cos(−b̂_i, ŵ_{f_i}), ŵ_{f_i} = W_U[f_i,:]/‖W_U[f_i,:]‖₂ (foil row of the
run-pinned unembedding matrix).
Executor asserts: ‖W_U[t_i]‖₂ > 0, ‖W_U[f_i]‖₂ > 0, t_i ≠ f_i for all i.

**Report (per run):** mean, median, min, max of {d_i}; fraction
p̂_f = #{i : d_i ≥ 0.9}/60 with **exact Clopper–Pearson 95% CI**; histogram
(10 bins) in the machine-readable twin JSON.

**Pre-registered decision rule (mirrors K1(a)'s structure):**
- (f)-FIRES iff **lower 95% CI of p̂_f > 0.5** — we are 95% confident a majority
  of items' bridge directions are foil-row suppressions. → feeds EXP082=Supported.
- (f)-RULED-OUT iff **upper 95% CI of p̂_f < 0.5** — the data rule out a
  majority-foil-suppression. → feeds EXP082=Not supported.
- Else → neither; feeds EXP082=Inconclusive.

**Why 0.9 is discriminating (non-vacuity, pre-registered):** for equal-norm
orthogonal rows, d = 1/√2 ≈ 0.707 < 0.9 [FACT — algebra, §6 L1]. d ≥ 0.9 ⟺
‖w_f‖ − ‖w_t‖cosθ ≥ 0.9‖w_t − w_f‖; at cosθ=0 this requires
‖w_t‖ ≤ 0.484‖w_f‖ — the FOIL row must *dominate* the difference direction.
The bar does not fire on generic unembedding geometry; it fires only if the
construction is geometrically a foil suppression. If (f) fires, the "relational
(t−f) direction" reading collapses: the target row is geometrically negligible in
the difference direction, so there is no non-trivial relational structure left to
rescue.

**The 0.9 bar is justified, not copied blindly:** the bar is the mirror image of
K1(a)'s adopted 0.9 bar (same "essentially the row direction" semantics, same
√(0.19/0.81) ≈ 0.484 non-vacuity constant by the symmetry of the difference
construction — §6 L1). Treatment-independence holds: no data contact (§1).

**Kill bars bite (verified, not trusted — recomputed 2026-09-23):**
(f)-FIRES needs **≥39/60** items ≥ 0.9 (38/60 → lower CP = 0.4990, no fire);
(f)-RULED-OUT needs **≤21/60** (22/60 → upper CP = 0.5010, no fire).
Wide honest Inconclusive band; bars are non-vacuous and asymmetric-power-safe.
(Identical arithmetic to K1's LOG-206 §6 — the threshold is a function of N=60
and the rule, not of the measurand.)

**Flip-count handling (standing correction, LOG-212 — binding):** the adopted (b)
reading (f ≥ r/2 strengthens tilt) is BACKWARDS vs the L1 license and is NOT used
anywhere in EXP082. The L1-aligned reading is: a pure readout shift strictly
increases the t−f margin on every item, hence predicts **f = 0 exactly**; f ≥ r/2
would contradict a *clean* directional effect. Archived f = 0 on all primary runs
is reported as [OBSERVATION] consistent with the L1-aligned reading. **Flip counts
carry zero decision weight in EXP082** — they are a consistency check, not an
endpoint. (No re-registration is needed here precisely because no weight is placed
on them: this plan never leans on (b).)

---

## 4. Endpoint (a) — target-boost contrast [CONTRAST, not a verdict]

**Computation:** c_i = cos(b̂_i, ŵ_{t_i}) per item per run; p̂_a = #{i : c_i ≥ 0.9}/60
with exact Clopper–Pearson 95% CI. Same fire/ruled-out rule as §3, applied ONLY to
fill the 2×2 partition (§5) — **(a)-contrast fires nothing, rules nothing out, and
carries no K1 authority.** If (a) were fired here it would duplicate K1's battery;
EXP082 instead uses (a) as the joint-interpretability coordinate its CEO dispatch
requires.

**Why recompute rather than cite:** citing K1's (a) would be inheriting from K1's
battery (forbidden, LOG-212). EXP082 re-measures the same geometric quantity under
its own rationale and its own guards; the two computations are independent
measurements of one number, and any discrepancy is itself a reportable [OBSERVATION]
(flagged to the CEO; it does not adjudicate between them).

---

## 5. Discriminating logic (boxed)

The geometric joint lemma is pre-registered in §6 L1 (IN-HOUSE-PROOF): on any single
item, (a)-firing ∧ (f)-firing ⟹ cosθ ≤ −0.62 (row anti-alignment; spherical-triangle
proof in §6). Outside that regime the two tilts are near-mutually-exclusive: at
cosθ=0, (a) needs ‖w_f‖ ≤ 0.484‖w_t‖ while (f) needs ‖w_t‖ ≤ 0.484‖w_f‖.

> **BOX — the 2×2 outcome partition {(a)} × {(f)}, majority-CI cells:**
>
> | (a)-contrast | (f) | Pre-registered meaning |
> |---|---|---|
> | fires | ruled out | **Target-boost tilt; foil-suppression rejected.** The bridge's readout geometry is target-directed. EXP082's HYPOTHESIS is dead for these runs. |
> | ruled out | fires | **FOIL-SUPPRESSION TILT SUPPORTED** — the bridge's readout geometry is foil-directed on the majority of items. This is EXP082's phenomenon. |
> | fires | fires | **Antipodal-axis readout tilt:** both majority cells fire ⟹ by the joint lemma, both-fire items satisfy cosθ ≤ −0.62 (G4 verifies per both-fire item; N_bothfire reported). Boost and suppression coincide geometrically (b̂ ≈ ŵ_t ≈ −ŵ_f); the "rather than" in the question is void — a single antipodal readout axis. If N_bothfire = 0 the two majority cells fired on disjoint item sets and the antipodal reading is NOT licensed — record as Inconclusive-on-antipodal (heterogeneous item geometry), not "antipodal, undistinguished." Otherwise the readout-tilt family is Supported as to direction-ambiguity-resolved; the *foil-rather-than-target* HYPOTHESIS as stated is not distinguished — recorded as "antipodal, undistinguished." |
> | ruled out | ruled out | **Readout-bias geometry rejected:** neither target-boost nor foil-suppression describes the majority of items. EXP082's HYPOTHESIS is dead; the readout-tilt family as a geometric explanation is exonerated for these runs. (Consequence: the bridge's rescue must be attributed elsewhere — mechanism, downstream transformation, or another readout structure — questions for other experiments, not this one.) |
> | either/both neutral | any | **Inconclusive** on the affected cells; the neutral cell contributes no direction. |
>
> **What uniquely supports foil-suppression tilt OVER (i) target-boost:** (f)-FIRES ∧
> (a)-RULED-OUT. The majority of items' bridge directions are ≥0.9-aligned with the
> foil row's negation while a majority-target-boost is ruled out. The near-mutual-
> exclusivity makes (f)-fire alone strongly suggestive outside the anti-aligned regime,
> but the conjunction is the clean discriminating cell — pre-registered, not
> double-counted.
>
> **What uniquely supports it OVER (ii) a relational (t−f) readout structure:** (f)-firing makes the
> target row geometrically negligible in the difference direction
> (‖w_t‖ ≤ 0.484‖w_f‖ at cosθ=0) — the foil suppression is a single-axis claim with no
> non-trivial relational (t−f) structure left. A relational mechanism needs both rows
> structurally non-trivial; (f)-firing removes that footing.
>
> **What KILLS the foil-suppression reading:** (f)-RULED-OUT (upper 95% CP CI of
> p̂_f < 0.5) on all primary runs.
>
> **What kills the experiment's own premise:** (P1) the bridge-identity guard fails
> (§7 G1) — the audited construction is not what EXP082 measures, so the (f) endpoint
> is undefined; (P2) any both-fire item with cosθ > −0.62 + 1e-6 (G4) — the L1 joint
> lemma is mathematically refuted, the license is misgraded, measurements are voided.

---

## 6. Mathematical License (binding — Law #15 Q4; template from LOG-200 §A.4)

**License grade: IN-HOUSE-PROOF** for the foil-suppression lemma + geometric
endpoints (f)/(a)-contrast — exact algebra on pinned weights; the computation *is*
the proof; promotion to PROVEN-LEMMA via LOG-215 Law #14 SIGN of this plan + an
executor report reproducing the L1 proof. **CONJECTURE-UNDER-TEST** for the causal
upshot (foil-suppression geometry ⇒ the rescue was *caused* by foil suppression) —
EXP082 is the falsification attempt; assumption A2 below is undischarged.
Weakest load-bearing grade = **CONJECTURE-UNDER-TEST** → authorizes the cheapest
discriminating experiment only — which EXP082 ($0, zero forward passes) is.
(INTUITION nowhere; the protocol starts.)

### L1. Authorizing result
- **Statement (exact):** Let W_U ∈ ℝ^{V×d} be the frozen unembedding matrix,
  x ∈ ℝ^d the final-token residual, logits ℓ = W_U x (+ constant bias, immaterial:
  Δℓ is bias-independent). For unit v̂ ∈ ℝ^d, scalar α, token y: the perturbation
  x ← x + αv̂ shifts the y-logit by
  **Δℓ_y = α·(W_U[y,:]·v̂) = α‖W_U[y,:]‖₂·cos(v̂, ŵ_y)**,
  ŵ_y = W_U[y,:]/‖W_U[y,:]‖₂. *Proof:* Δℓ = W_U(αv̂); take the y-th row. ∎
  **Foil-suppression lemma:** let w_t = W_U[t_i,:], w_f = W_U[f_i,:],
  b̂_i = (w_t − w_f)/‖w_t − w_f‖₂ with ‖w_t − w_f‖₂ > 0, and the injected direction
  v̂ = b̂_i, α_run > 0. Then
  **cos(−b̂_i, ŵ_{f_i}) ≥ 0.9 ⟺ Δℓ_{f_i} ≤ −0.9α_run‖w_{f_i}‖₂**.
  *Proof:* by L1 with y = f_i, Δℓ_{f_i} = α_run(w_{f_i}·b̂_i) =
  −α_run‖w_{f_i}‖₂cos(−b̂_i, ŵ_{f_i}); with all quantities nonzero and α_run > 0,
  the inequality on the cosine is equivalent to the quantitative foil-logit
  suppression bound. ∎
  **Mirror-bound derivation:** d_i := cos(−b̂_i, ŵ_{f_i}) =
  (‖w_f‖ − ‖w_t‖cosθ)/‖w_t − w_f‖, cosθ = (w_t·w_f)/(‖w_t‖‖w_f‖). So
  d_i ≥ 0.9 ⟺ ‖w_f‖ − ‖w_t‖cosθ ≥ 0.9‖w_t − w_f‖; at cosθ = 0 ⟺
  ‖w_t‖/‖w_f‖ ≤ √(0.19/0.81) ≈ 0.4843. Equal-norm orthogonal rows ⟹
  d_i = 1/√2 ≈ 0.7071 < 0.9. The 0.9 bar fires only on foil-row dominance.
  **Joint-firing lemma:** on any single item, d_i ≥ 0.9 ∧ c_i ≥ 0.9 ⟹
  cosθ ≤ −0.62. *Proof:* let γ = arccos(0.9) ≈ 25.84°; the two firings give
  angle(b̂,ŵ_t) ≤ γ and angle(−b̂,ŵ_f) = angle(b̂,−ŵ_f) ≤ γ. By the spherical
  triangle inequality, angle(ŵ_t,−ŵ_f) ≤ 2γ. But angle(ŵ_t,−ŵ_f) = π − θ, so
  π − θ ≤ 2γ and cos(π − θ) ≥ cos(2γ) ⟹ −cosθ ≥ 2(0.9)² − 1 = 0.62 ⟹
  cosθ ≤ −0.62. ∎ In that regime b̂ ≈ ŵ_t ≈ −ŵ_f: boost and suppression coincide.
- **Companion identity (licenses the reconstruction):** b_i = α_run·
  normalize(E_run[t_i] − E_run[f_i]), E_run the run-pinned unembedding matrix
  (LOG-197 E1/E2, Q1=Supported; run pins per F-200-2 §1.1). Combined: the direct
  readout component of the bridge's effect on the foil is
  Δℓ_{f_i} = α_run‖W_U[f_i]‖₂cos(b̂_i, ŵ_{f_i})
           = −α_run‖W_U[f_i]‖₂d_i ≤ −0.9α_run‖W_U[f_i]‖₂ when (f) fires.
- **Source:** in-house elementary proofs (reproduced in the executor report);
  construction identity from the signed LOG-197 audit.
- **Epistemic label:** [THEOREM] for the lemma, mirror bound, and joint lemma
  (graded IN-HOUSE-PROOF pending LOG-215 review); [FACT] for the audited identity;
  [CONJECTURE] for the causal upshot (see A2).

### L2. Quantitative prediction for the primary endpoint
- **Endpoint:** (f) — per-item d_i = cos(−b̂_i, ŵ_{f_i}), i=1..60 per run.
- **Prediction:** under H_FS (foil-suppression tilt), p_f = P(d_i ≥ 0.9) has lower
  exact 95% CI > 0.5. Under foil-neutral geometry (canonical equal-norm-orthogonal
  case: d = 1/√2 ≈ 0.707 < 0.9), d_i stays bounded from 1. **No point forecast is
  registered** (Law #2) — the prediction is the threshold test, whose non-vacuity
  is derived above.
- **Derivation:** the foil-suppression lemma — d_i ≥ 0.9 is exactly the condition
  "the injected direction is ≥0.9-aligned with the foil row's negation," i.e. the
  injection's direct readout effect is a ≥0.9·α‖W_U[f]‖ foil-logit suppression.

### L3. Breaking point
- **Falsifying observation (foil-suppression):** (f)-FIRES on ≥1 primary run (§3).
  **Decision: PIVOT** the tilt-interpretation sub-workstream (§9): downstream
  characterization (K2's bypass question, Sprint-3 Stage-0s, CLLC scoping) must model
  a foil-directed readout shift; the exclusive "target boost" framing is withdrawn
  where assumed. Does NOT override K1's battery verdict; does NOT decide §H7.
- **Exonerating observation:** (f)-RULED-OUT on all primary runs.
  **Decision: KILL** the foil-suppression-tilt hypothesis for these runs — the
  readout-tilt question continues under K1's (a) battery, which this plan does not
  touch.
- **Otherwise → Inconclusive → HOLD:** no interpretation fires; pilots proceed with
  the foil question explicitly [OPEN].
- **Falsifying observation (license itself):** bridge-identity guard fails (§7 G1),
  or any both-fire item violates the joint lemma (cosθ > −0.62 + 1e-6, §7 G4), or
  any other §7 guard trips → license misgraded → halt; measurements Refuted;
  no verdict.
- **Outcome partition:** §7's verdict table maps every cell of
  {(f)-fire/out/neutral} × {(a)-contrast} × {guards pass/fail} × {EXP070 n/a}
  to exactly one of the five verdict categories (Charter M5.2).

### L4. Assumption inventory
- **A1 — item labels:** verbatim ports of runner item-construction code; tokenizer
  `" "+label` `[0]` encoding exactly as the runners call it. Discharge: §7
  cross-check vs archived per-item records; mismatch = FATAL.
- **A2 — mid-network propagation (UNDISCHARGED):** the causal upshot assumes the
  layer-10/20 injection's foil-margin effect preserves the sign of the L1 readout
  projection (downstream layers don't reverse the foil suppression). Not discharged
  by EXP082 — the geometric (f) endpoint does NOT need A2. Carried as
  [CONJECTURE]; caps the causal-upshot license at CONJECTURE-UNDER-TEST.
- **A3 — run pins:** E_run is the executed model's matrix; pinned snapshots (§8);
  Δθ=0 pre/post SHA-256 via the verbatim `get_hash` (run_exp077.py ll. 166–172);
  executor cross-checks against the archived pre_hash values. Mismatch = FATAL —
  no results reported (Law #6/#13).
- **A4 — EXP070:** excluded from all endpoints (no verified vectors);
  Underdetermined cells, never filled by assumption.
- **A5 — [removed in drafting; number retired]** (F2 — license hygiene, LOG-215);
- **A6 — bars pre-registered:** 0.9 (="essentially the negated foil-row direction")
  and the majority-CI rule (="the typical item") chosen treatment-independently;
  EXP082 has had no data contact on these cosines.
- **A7 — item-independence for the Clopper–Pearson CI:** the 60 per-item trials
  are treated as independent Bernoulli trials. Any within-run item dependence
  (shared prompt templates) is not modeled — the CI is nominal; disclosed, not hidden.
- **A8 — non-degenerate difference rows:** the executor asserts and reports
  min_i‖W_U[t_i] − W_U[f_i]‖₂ across all items × runs. Distinct tokens can carry
  near-identical rows, which would make b̂_i noise-dominated; a firing on a
  noise-dominated item would be spurious. The minimum is reported as a diagnostic
  [OBSERVATION]; it does not void any verdict absent a guard failure.
- **Promotion path:** IN-HOUSE-PROOF → PROVEN-LEMMA on LOG-215 SIGN of this plan +
  executor report reproducing the L1 proofs; CONJECTURE-UNDER-TEST promotes only via
  downstream propagation evidence (e.g., K2-class bypass data) — never by re-labeling.

**Signed:** Track-8 (LOG-214) · 2026-09-23 · **Law #14 review:** LOG-215, pre-assigned, pending.

---

## 7. Verdict mapping (exhaustive — every outcome cell mapped, no "we'll decide later")

Per-run verdicts first (EXP065, EXP066, EXP077-official; smoke secondary labeled):

| (f) | (a)-contrast | Guards | Per-run verdict |
|---|---|---|---|
| FIRES | ruled out | pass | **Supported** — pure foil-suppression tilt |
| FIRES | neutral | pass | **Supported** — foil-suppression tilt (target-boost not ruled out) |
| FIRES | fires | pass | **Supported** — antipodal-axis readout tilt (boost ≡ suppression; G4 joint lemma verified per both-fire item; N_bothfire reported; N_bothfire = 0 → Inconclusive-on-antipodal, heterogeneous item geometry) |
| ruled out | any | pass | **Not supported** — foil-suppression reading killed ((a) cell recorded) |
| neither | any | pass | **Inconclusive** |
| — | — | **fail** | **Refuted** (measurements invalid; no claim licensed; halt, report) |
| EXP070 cells | — | — | **Underdetermined** (no verified vectors; excluded) |

Rows 1–3 all map to Supported with distinct recorded readings — no conflicting-branch
cell (the 2×2 meanings are partitioned in §5; the both-fire antipodal cell is the
§5 third row). Guards-fail → Refuted takes precedence over all endpoint cells
(correct per Law #13 — integrity failure voids measurements).

**Program-level aggregation (pre-registered):** EXP082-SUPPORTED iff **≥1 primary run**
lands Supported — rationale: the bridge *construction* is shared across runs; the
question is whether the construction *can* act as a foil suppressor, and a control is
only as clean as its dirtiest use (mirrors K1's aggregation rationale; same CEO-
override clause: the CEO may override with reasons logged).
EXP082-EXONERATED iff **all** primary runs land Not supported. Otherwise
**Inconclusive**.

**Guards (all FATAL on failure — halt, no verdict):**
G1. Bridge-identity re-verification: |cos(rebuilt b̂_i, LOG-197 formula)| ≥ 1−1e-6
  on all 60 items × 3 runs (the formula IS the rebuild; this guards transcription error).
G2. Label cross-check (§2): any item mismatch vs archived per-item records = FATAL.
G3. Δθ=0: pre/post SHA-256 match via verbatim `get_hash`, AND match the archived
  pre_hash values (§8). Any mismatch = FATAL, results not reported.
G4. Joint-lemma check: for every both-fire item (d_i ≥ 0.9 ∧ c_i ≥ 0.9), assert
  cosθ ≤ −0.62 + 1e-6. Any violation = FATAL — the L1 joint lemma is mathematically
  refuted, the license is misgraded (Law #13 analog).
G5. No forward pass executed at any step (executor asserts; code inspection — the
  script contains no `model(...)` call on inputs).
G6. Sanity asserts: ‖W_U[t_i]‖₂ > 0, ‖W_U[f_i]‖₂ > 0, t_i ≠ f_i for all i
  (grounds A8's diagnostic).

**D2 — foil-shift consistency diagnostic [REPORT-ONLY, no decision weight]:**
the executor reports (i) the L1-predicted per-item foil shifts
Δℓ̂_{f,i} = α_run(b̂_i·W_U[f_i]) (weights-only; negative by the lemma on (f)-firing
items — reported in the twin JSON for the record); (ii) the archived aggregate foil
shift sign (EXP065 −0.4042, EXP066 −0.4044 — negative ✓ consistent; EXP077 official:
no archived logit shifts — reported unavailable, never a negative). A sign mismatch
would be an [OBSERVATION] against the causal upshot, not a kill — the geometric
verdict stands on the cosine, not the aggregate.

**Banned language:** the verdicts above are the only permitted categories
(Supported / Not supported / Inconclusive / Underdetermined / Refuted).
"Promising", "interesting", "worth another experiment" are forbidden anywhere in the
executor report. The "persistence" framing is struck (LOG-212) and does not appear.
p-values alone license nothing (§G1b standing ban respected). No novelty claim (N1).

---

## 8. Δθ=0 guard + exact environment pin

| Item | Pin |
|---|---|
| Env | `/home/hatch/workspace/.venv_smoke`: torch **2.14.0+cpu**, transformers **5.17.0**, numpy **2.5.3** — asserted in-script, exact (LOG-197 §0) |
| Models | `EleutherAI/pythia-160m` snapshot `50f5173d932e8e61f858120bcb800b97af589f46`; `EleutherAI/pythia-410m` snapshot `9879c9b5f8bea9051dcb0e68dff21493d67e9d4f`; `local_files_only`, `trust_remote_code=False`, `torch_dtype=torch.float32`, `model.eval()` |
| Hash | verbatim `get_hash` (SHA-256 over `state_dict()` tensors, sorted keys, CPU float32 bytes — `run_exp077.py` ll. 166–172); pre/post + cross-check vs archived: EXP065 `54c88fa4897785f2…`, EXP066 `4c242d9ac702a402…`, EXP077 `ec276abe3902fab0…` (full 64-hex in archives) |
| Forward passes | **0** — weight reads + archived records only (G5) |
| Seeds | deterministic; no RNG consumed (recorded as such) |

---

## 9. Pre-registered consequences (not new decisions)

- **EXP082-SUPPORTED (foil-suppression tilt):** PIVOT the tilt-interpretation
  sub-workstream — any downstream readout-shift characterization (K2's bypass
  question, Sprint-3 Stage-0 pilots, CLLC scoping, the mentor's synthesis
  directionality note) must model a *foil-directed* readout shift, not a target
  boost; the exclusive "it is a target boost, full stop" framing is withdrawn where
  it was assumed. Does NOT override K1's battery verdict (K1 answers tilt-vs-
  mechanism; EXP082 answers which direction the tilt points) and does NOT decide §H7.
- **EXP082-EXONERATED (foil-suppression Not supported):** the foil-suppression-tilt
  hypothesis is dead for these runs; the readout-tilt question rests entirely on
  K1's (a) battery. No pivot fires.
- **EXP082-Inconclusive:** no interpretation fires; pilots proceed with the foil
  question explicitly **[OPEN]** in their interpretation notes.
- **EXP082-Refuted (integrity):** no verdict; executor reports the failure; CEO decides.
- The executor may not convert Inconclusive into a negative, nor a diagnostic into a
  kill, nor a Supported cell into a claim beyond the recorded §5 reading.

---

## 10. Execution steps (for the executor, post-SIGN)

1. Assert env (§8 table); load run-pinned snapshots read-only; G3 hash gate; G6 sanity.
2. Rebuild per-item (t_i, f_i) label strings via verbatim ports (§2); G2 cross-check;
   G1 bridge-identity guard.
3. Compute (f): {d_i} per run → stats + p̂_f + Clopper–Pearson 95% CI → apply §3 rule.
4. Compute (a)-contrast: {c_i} per run → stats + p̂_a + Clopper–Pearson 95% CI (contrast
   only — no K1 authority).
5. Joint checks: per-item both-fire flag; G4 joint-lemma assert (cosθ ≤ −0.62+1e-6);
   report anti-alignment fraction [OBSERVATION].
6. Read archived (b, c); report flip counts as [OBSERVATION] under the L1-aligned
   reading (f = 0 tilt-predicted; zero decision weight — §3).
7. D2 foil-shift diagnostic (report-only).
8. Machine-readable twin JSON (unrounded values, per-item d_i/c_i/cosθ arrays, N_bothfire
   and the both-fire item index set, hashes, env manifest) + this report's verdict table
   filled verbatim from §7.
9. Report in FACT/INFERENCE/HYPOTHESIS/SPECULATION + 10-label standard; evidentiary
   level L1 (readout-path geometry/causal-accessibility — no L2/L3 crossing).

---

## 11. What this plan does not do (binding scope)

No forward passes; no K1/K2/K3 verdicts (EXP082's (a)-contrast is not K1's (a));
no EXP070 endpoints (Underdetermined); no GPU; no signed-artifact edits;
no (b)-based verdict (the adopted (b) reading is struck for future tilt use —
this plan places zero weight on flip counts); no "persistence" framing;
no bridge reconstruction under Law #7 compliance; no novelty claim (N1 stands).

---

## 12. Knowledge-protocol obligations (one challenge + one idea)

- **Challenge:** the archived end-to-end signature (EXP065 Δℓ_t=+0.3597,
  Δℓ_f=−0.4042; EXP066 +0.3448/−0.4044) shows a near-symmetric BOTH-sides shift.
  Under a pure (a)-firing geometry the foil shift would be small; under a pure
  (f)-firing geometry the target shift would be small. A large both-sides aggregate
  is prima facie consistent with NEITHER pure endpoint firing — it points at the
  neither-fire cell (or the anti-aligned both-fire cell). The plan answers this
  honestly: the geometric verdict rests on the per-item cosines, not the aggregate;
  the aggregate is reported via D2 with zero decision weight, and a both-out majority
  would kill the foil-suppression reading exactly as pre-registered (§5 row 4).
  EXP082 cannot rescue its hypothesis from the geometry.
- **Idea:** the G4 joint-firing check is a free, pre-registered measurement of
  unembedding geometry itself: the both-fire fraction is a direct count of how many
  (target, foil) option-token row pairs are anti-aligned (cosθ ≤ −0.62). If it is 0/60
  across runs, that is a reusable [OBSERVATION] for the program — benchmark option
  rows are never antipodal, which bounds any future "antipodal axis" mechanism story.
  Either outcome pays for its line in the plan.

---

*Author: Track-8 (LOG-214) · 2026-09-23 · FROZEN. Experiment number EXP082 verified
unminted at registration (next free after EXP081, minted LOG-182). This plan inherits
nothing from K1's battery (CEO ruling LOG-212). Execution only after Law #14 SIGN.*

**DO NOT EXECUTE before Law #14 SIGN (LOG-215, pre-assigned).**
