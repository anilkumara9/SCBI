# K1 — Readout-Tilt Falsification: FROZEN PLAN

**LOG-205 · Track-8 (Experimental Statistician) · 2026-09-23**
**Status:** FROZEN — pending Law #14 review (LOG-206, pre-assigned). **DO NOT EXECUTE before SIGN.**
**Cost:** $0 CPU. Zero forward passes. Read-only weight-tensor reads only.
**Scope banner:** this plan computes K1(a), K1(b), K1(c) and verdicts them. It does NOT
run K2/K3, does NOT touch EXP070 vectors (none verified — excluded), does NOT modify any
signed artifact, and does NOT authorize GPU.

---

## 0. Law #15 — the four answers (on record, before work starts)

1. **Q: What precise question does this answer?** Is the bridge's rescue power a
   geometric tilt toward the target token's unembedding row (label-assisted readout
   artifact) rather than a relational mechanism? Measurands: (a) per-item
   cos(bridge direction, unembedding row of t_target) vs the pre-registered 0.9 bar;
   (b) correct→wrong flips f vs wrong→correct rescues r (diagnostic readout,
   pre-registered f ≥ r/2 strengthens tilt); (c) the label-shuffle test, operationalized
   as (c1) swapped-construction geometric persistence + (c2) swapped-scoring identity
   (§5.3 — the naive re-scoring is arithmetically vacuous; the plan says so plainly).
2. **Decision:** **KILL / PIVOT** — tilt confirmed kills the autonomous output-side
   mechanism reading, locks the LOG-204 §H7 demotion (mandatory/irreversible), fires
   P1, stands down K3. Tilt exonerated → **CONTINUE** (KEEP chain: K2 pilot, Sprint-3
   Stage-0s, K3-CPU licensed; CEO revisits §H7). Inconclusive → **HOLD** (battery holds;
   pilots proceed with bridge status [OPEN]).
3. **Cheapest:** $0 CPU, archived artifacts + read-only weight reads, zero forward
   passes. No cheaper decision exists — a GPU run cannot answer a geometric question
   about already-archived vectors. Forward-pass count: **0**.
4. **License:** §6 (L1–L4 per
   `research/foundations/MATHEMATICAL_LICENSE_STANDARD_2026-09-23.md`); the Law #14
   reviewer verifies the grade.

---

## 1. Standing context (facts the plan inherits, not re-derives)

- LOG-197: Q1=Supported (bridge = normalize(E[target]−E[foil]), option-informed on the
  letter of Law #7 — non-compliant as an autonomous-mechanism construction), Q2=
  Supported-narrow-L1 ("readout path causally accessible to an option-informed direction;
  NOT L2, NOT L3"). CI method identified: Tango (1998) exact score interval, reproduced
  to 4dp before use. [FACT — `research/analysis_plans/LAW7_BRIDGE_AUDIT_REPORT_LOG197_2026-09-23.md`]
- LOG-198 §1: K1 is the adopted battery's first gate; §H6 interpretation ordering is
  binding (no K2/K3 verdict before K1 rules). [DEFINITION — adopted]
- LOG-204 Ruling 1 (§H7): bridge DEMOTED to "rescue control (known-answer direction),
  NOT a mechanism control"; positive-control status for autonomous-mechanism questions
  REVOKED. Formal lock-in conditional on K1: confirms-tilt → mandatory/irreversible;
  exonerates → CEO revisits. [FACT — `reports/research_log.md` LOG-204]
- LOG-200 (foundations standard): license template, grade rubric, F-200-2 run-pin
  correction (every license names the run-pinned matrix). [DEFINITION — binding]
- K1 has had **no data contact** on its measurands: LOG-197's battery-scope banner
  explicitly did not compute K1(a); cos(bridge, target row) was never computed anywhere
  in the corpus. The 0.9 bar is pre-registered in adopted §H6, treatment-independent.
  [FACT]

### 1.1 Substrate pins (run-pinned; F-200-2)

| Run | Model (executed) | Layer | d | α_run | N | (r, f)=(b, c) primary | ΔM̂ [Tango 95% CI] | §G1b cell |
|---|---|---|---|---|---|---|---|---|
| EXP065 | `EleutherAI/pythia-160m` | 10 | 768 | 1.0 | 60 | (10, 0) | +0.1667 [+0.0931, +0.2803] | (1) L > δ_min |
| EXP066 | `EleutherAI/pythia-410m` | 20 | 1024 | 1.0 | 60 | (8, 0) | +0.1333 [+0.0651, +0.2417] | (1) L > δ_min |
| EXP077 | `EleutherAI/pythia-410m` | 20 | 1024 | 0.5 | 60 | (6, 0) official GPU | +0.1000 [+0.0338, +0.2015] | (4) Inconclusive |
| EXP077 | (smoke, secondary) | 20 | 1024 | 0.5 | 60 | (14, 0) | +0.2333 [+0.1444, +0.3544] | labeled secondary |

Archived Δθ=0 (pre==post): EXP065 `54c88fa4897785f2…`, EXP066 `4c242d9ac702a402…`,
EXP077 `ec276abe3902fab0…` (full hashes in §8; executor re-verifies verbatim).
Archived aggregate logit shifts [OBSERVATION — records, feed D1 §5.4]:
EXP065 Δℓ_t=+0.3597, Δℓ_f=−0.4042, Δmargin=+0.7639;
EXP066 Δℓ_t=+0.3448, Δℓ_f=−0.4044, Δmargin=+0.7492.
EXP070: **excluded from all vector-level endpoints** (no verified `exp070_vectors`
record anywhere in the repo — LOG-197 E3). Its cells are Underdetermined, never
filled by assumption. Its log-cited (b,c)=(10,0) may appear as labeled secondary in
(b) only — never verdict-bearing.

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
- **(b, c) counts:** EXP065 `exp065_results.json →
  stage_B_confirmatory_results.Same_Layer_Output_Bridge.(rescues_b, corruptions_c)`;
  EXP066 `exp066_replication_results.json → stage_B_conditions.Same_Layer_Output_Bridge.
  (rescues_b, corruptions_c)`; EXP077 official GPU record per LOG-197 E4 pin
  (b=6, c=0 — cited from `reports/research_log.md` LOG-128); smoke
  `exp077_results.json → stage_B_conditions.C8_bridge` as labeled secondary.
  Where per-item correctness records exist (EXP066 instance evaluations;
  EXP077 smoke instance_records), the executor recomputes (b, c) from them as an
  archive-integrity check.

---

## 3. Endpoint (a) — geometric target-boost test [PRIMARY KILL ENDPOINT]

**Computation (per run, per item i = 1..60):**
b̂_i = normalize(E_run[t_i] − E_run[f_i]) — the LOG-197-verified construction,
scale-free (α drops out of the cosine);
c_i = cos(b̂_i, ŵ_{t_i}), ŵ_{t_i} = W_U[t_i,:]/‖W_U[t_i,:]‖₂ (row of the run-pinned
unembedding matrix).
Executor asserts: ‖W_U[t_i]‖₂ > 0, ‖W_U[f_i]‖₂ > 0, t_i ≠ f_i for all i.

**Report (per run):** mean, median, min, max of {c_i}; fraction
p̂_a = #{i : c_i ≥ 0.9}/60 with **exact Clopper–Pearson 95% CI**; histogram
(10 bins) in the machine-readable twin JSON.

**Pre-registered decision rule:**
- (a)-KILL FIRES iff **lower 95% CI of p̂_a > 0.5** — we are 95% confident a
  majority of items' bridge directions are target-row boosts. → feeds K1=Supported.
- (a)-RULED-OUT iff **upper 95% CI of p̂_a < 0.5** — the data rule out a
  majority-target-boost (equivalence-to-null at the practical bar). → feeds
  K1=Not supported.
- Else → neither; feeds K1=Inconclusive.

**Why 0.9 is discriminating (non-vacuity, pre-registered):** for equal-norm
orthogonal rows, c = 1/√2 ≈ 0.707 < 0.9 [FACT — algebra]. c ≥ 0.9 ⟺
‖w_t‖ − ‖w_f‖cosθ ≥ 0.9‖w_t − w_f‖; at cosθ=0 this requires ‖w_f‖ ≤ 0.484‖w_t‖ —
the target row must *dominate* the difference direction. The bar does not fire on
generic unembedding geometry; it fires only if the construction is geometrically a
target boost. If (a) fires, §H6's words stand: "it is a target boost, full stop" —
the −foil component is geometrically negligible and the "relational (t−f)
direction" reading collapses.

---

## 4. Endpoint (b) — correct-item flip analysis [DIAGNOSTIC, not a standalone kill]

Per §H6 (adopted, implemented verbatim — Law #4): f = correct→wrong flips
(= c_archived), r = wrong→correct rescues (= b_archived).
Pre-registered reading: **f ≥ r/2 strengthens a tilt verdict**;
**f ≈ 0 with r > 0 (lower 95% CI of ΔM > δ_min) weakens it**; reported as
[OBSERVATION] feeding the K1 verdict.

**Caveat for the record [INTERPRETATION — flagged for LOG-206]:** the (b) reading
as specified diagnoses *broad disruption* (a crude bias flipping decisions both
ways), not the *narrow geometric tilt* of K1's Law-#15 Q1. The L1 license (§6)
predicts f = 0 for a pure readout shift (the t−f margin strictly increases), so the
archived f = 0, r > 0 pattern is *consistent with* the narrow tilt while the adopted
(b) reading scores it as *weakening* tilt. The plan keeps the adopted mapping
verbatim (no silent hypothesis shift) and rests the kill criterion on (a)/(c1);
(b) feeds the verdict as a cleanliness diagnostic: f ≥ r/2 would indicate the
injection is not a clean directional effect at all.

Archived (b) inputs [FACT — records]: EXP065 (r=10, f=0; lower CI +0.0931 > δ_min),
EXP066 (r=8, f=0; lower CI +0.0651 > δ_min), EXP077 official (r=6, f=0; lower CI
+0.0338 ≯ δ_min — the "weakens" condition's CI clause is NOT met → neutral),
EXP077 smoke (r=14, f=0) secondary.

---

## 5. Endpoint (c) — the label-shuffle test

### 5.1 The vacuity lemma (why the naive operationalization is not the test)

[THEOREM — arithmetic, stated so no one mistakes it for evidence:] under the
runners' binary argmax scoring (`chosen = A if logits[t_A] > logits[t_C] else C`;
EXP077 `run_exp077.py` ll. 669–682; same binary structure in EXP065/066),
re-scoring archived items with target/foil roles swapped while holding the
injection fixed yields (b_swap, c_swap) = (c_orig, b_orig) and
ΔM_swap = −ΔM_orig **exactly**, for every run, under *both* the tilt and the
mechanism hypothesis. It cannot discriminate them and "rescue-persistence"
(ΔM_swap clearing +δ_min) is arithmetically impossible given ΔM_orig > 0.
**Therefore the fixed-injection swapped-scoring is NOT registered as a
discriminating endpoint.** It is computed once as (c2) below — an
archive-integrity check, not evidence.

### 5.2 Endpoint (c1) — swapped-construction geometric persistence [KILL-CAPABLE]

**The discriminating question the spec intends:** is the "bridge ≈ target-row"
property anchored to the *true labels*, or is it label-independent formula
geometry (normalize(w_X − w_Y) ≈ ŵ_X for *whatever* X)? A true relational
mechanism's rescue must depend on the labels being true; a readout tilt's
"rescue" is a property of the construction formula + unembedding geometry and
**persists under relabeling**.

**Computation (per run, per item):** b̂′_i = −b̂_i (the bridge the verified code
*would* build with roles swapped — licensed by LOG-197 E1/E2; no new assumption);
p_i = cos(b̂′_i, ŵ_{f_i}) = −cos(b̂_i, ŵ_{f_i}) (swapped bridge vs swapped-target row).
**Report:** same as (a): distribution + p̂_c = #{i : p_i ≥ 0.9}/60 with exact
Clopper–Pearson 95% CI.
**Pre-registered decision rule (mirrors (a)):**
- (c1)-PERSISTENCE FIRES iff **lower 95% CI of p̂_c > 0.5** → the target-boost
  property is label-independent formula geometry → feeds K1=Supported
  ("rescue-persistence under label shuffling" made geometrically precise).
- (c1)-RULED-OUT iff **upper 95% CI of p̂_c < 0.5** → the (a)-alignment is specific
  to the true labeling (the geometry tracks truth) → weakens tilt, feeds
  K1=Not supported.
- Else → neutral.

**Kill criterion (binding, from §H6):** (a)-KILL FIRES **OR** (c1)-PERSISTENCE
FIRES → the bridge is readout bias; the "output-side mechanism" reading is
withdrawn; the bridge's positive-control status is revoked to *rescue* control.

### 5.3 Endpoint (c2) — swapped-scoring identity [INTEGRITY CHECK, not evidence]

Compute (b_swap, c_swap) from archived per-item records with roles swapped;
assert (b_swap, c_swap) == (c_orig, b_orig) exactly and ΔM_swap == −ΔM_orig
(the §5.1 identity). Report as [OBSERVATION]. **Any deviation = FATAL**
archive-integrity failure → measurements Refuted, no K1 verdict, halt and report
(Law #13). On success it licenses no claim about tilt vs mechanism — recorded so
the naive reading can never be laundered as evidence later.

### 5.4 Diagnostic D1 — archived logit-shift signature [DIAGNOSTIC]

Already archived [OBSERVATION — records]: EXP065 Δℓ_t=+0.3597/Δℓ_f=−0.4042;
EXP066 Δℓ_t=+0.3448/Δℓ_f=−0.4044 (target↑, foil↓, near-symmetric — the tilt sign
signature; necessary, not sufficient). Executor additionally computes the
L1-predicted per-item shifts Δℓ̂_{t,i} = α_run(b̂_i·W_U[t_i]),
Δℓ̂_{f,i} = α_run(b̂_i·W_U[f_i]) from weights alone and the ratio diagnostic
r_obs = Δℓ_t/|Δℓ_f| vs r_pred = mean_i(Δℓ̂_{t,i}/|Δℓ̂_{f,i}|).
Pre-registered reading: |r_obs − r_pred|/r_pred ≤ 0.5 [ARBITRARY — rationale:
downstream transformation can rescale but sign-preserving propagation keeps the
readout-projection ratio within 2×] **strengthens** tilt (the readout projection
quantitatively exhausts the end-to-end effect); larger divergence is **neutral**
(the gap localizes to downstream transformation — precisely K2's bypass-vs-routing
question — and does not kill the geometric tilt). Cannot fire the kill criterion.

---

## 6. Mathematical License (binding — Law #15 Q4; template from LOG-200 §A.4)

**License grade: IN-HOUSE-PROOF** for the geometric endpoints (a)/(c1) — exact
algebra on pinned weights; the computation *is* the proof; promotion to
PROVEN-LEMMA via LOG-206 Law #14 SIGN. **CONJECTURE-UNDER-TEST** for the causal
upshot (tilt geometry ⇒ the rescue was *caused* by readout tilt) — K1 is the
falsification attempt; assumption A2 below is undischarged (K2's question).
Weakest load-bearing grade = **CONJECTURE-UNDER-TEST** → authorizes the cheapest
discriminating experiment only — which K1 ($0, zero forward passes) is.
(INTUITION nowhere; the protocol starts.)

### L1. Authorizing result
- **Statement (exact):** Let W_U ∈ ℝ^{V×d} be the frozen unembedding matrix,
  x ∈ ℝ^d the final-token residual, logits ℓ = W_U x (+ constant bias, immaterial:
  Δℓ is bias-independent). For unit v̂ ∈ ℝ^d, scalar α, token t: the perturbation
  x ← x + αv̂ shifts the t-logit by
  **Δℓ_t = α·(W_U[t,:]·v̂) = α‖W_U[t,:]‖₂·cos(v̂, ŵ_t)**,
  ŵ_t = W_U[t,:]/‖W_U[t,:]‖₂. *Proof:* Δℓ = W_U(αv̂); take the t-th row. ∎
  Corollary: if cos(v̂, ŵ_t) ≥ 0.9 then Δℓ_t ≥ 0.9α‖W_U[t,:]‖₂ — a positive logit
  bias toward t linear in the row norm.
- **Companion identity (licenses the reconstruction):** b_i = α_run·
  normalize(E_run[t_i] − E_run[f_i]), E_run the run-pinned unembedding matrix
  (LOG-197 E1/E2, Q1=Supported; run pins per F-200-2 §1.1). Combined: the direct
  readout component of the bridge's effect is Δℓ_{t_i} =
  α_run‖W_U[t_i]‖₂cos(b̂_i, ŵ_{t_i}) ≥ 0.9α_run‖W_U[t_i]‖₂ when (a) fires.
- **Source:** in-house elementary proof (three lines, reproduced in the executor
  report); construction identity from the signed LOG-197 audit.
- **Epistemic label:** [THEOREM] for the lemma; [FACT] for the audited identity;
  [CONJECTURE] for the causal upshot (see A2).

### L2. Quantitative prediction for the primary endpoint
- **Endpoint:** (a) — per-item c_i = cos(b̂_i, ŵ_{t_i}), i=1..60 per run.
- **Prediction:** under H_T (readout tilt), p_a = P(c_i ≥ 0.9) has lower exact 95%
  CI > 0.5. Under the relational-mechanism null with geometrically non-trivial
  t−f structure, c_i stays bounded from 1 (canonical equal-norm-orthogonal case:
  c = 1/√2 ≈ 0.707 < 0.9). **No point forecast is registered** (Law #2) — the
  prediction is the threshold test, whose non-vacuity is derived in §3.
- **Derivation:** L1 corollary + construction identity; c_i ≥ 0.9 is exactly the
  condition "the injected direction is ≥0.9-aligned with the target row," i.e.
  the injection's direct readout effect is a ≥0.9·α‖W_U[t]‖ logit bias toward t.
- (c1): same bar on p_i = −cos(b̂_i, ŵ_{f_i}) (persistence ⟺ label-independence).

### L3. Breaking point
- **Falsifying observation (tilt):** (a)-KILL ∨ (c1)-PERSISTENCE fires (§3, §5.2).
  **Decision: KILL** the autonomous output-side mechanism reading **+ PIVOT** the
  program (P1 fires): LOG-204 §H7 demotion locks in — mandatory, irreversible;
  K3 does not run (auditing label compliance of a confirmed tilt is wasted motion —
  §H6's own reasoning); K2 not licensed as a mechanism discriminator (any K2 run
  needs fresh CEO clearance as characterization-only).
- **Exonerating observation:** (a)-RULED-OUT ∧ (c1)-RULED-OUT on all primary runs.
  **Decision: CONTINUE** the KEEP chain: CEO revisits §H7; K2 pilot licensed;
  Sprint-3 Stage-0 pilots licensed (positive class intact); K3's CPU construction
  audit proceeds.
- **Otherwise → Inconclusive → HOLD:** battery holds; pilots proceed with bridge
  status explicitly [OPEN]; no pivot fires on an inconclusive cell.
- **Falsifying observation (license itself):** bridge-identity guard fails (§7),
  output-bias/material premise error found, or any §7 guard trips → license
  misgraded → halt; measurements Refuted; no verdict.
- **Outcome partition:** §7's verdict table maps every cell of
  {(a)-fire/out/neutral} × {(c1)-fire/out/neutral} × {(b) reading} × {guards pass/
  fail} × {EXP070 n/a} to exactly one of the five verdict categories (Charter M5.2).

### L4. Assumption inventory
- **A1 — item labels:** verbatim ports of runner item-construction code; tokenizer
  `" "+label` `[0]` encoding exactly as the runners call it. Discharge: §7
  cross-check vs archived per-item records; mismatch = FATAL.
- **A2 — mid-network propagation (UNDISCHARGED):** the causal upshot assumes the
  layer-10/20 injection's t−f margin effect preserves the sign of the L1 readout
  projection (downstream layers don't reverse it). Not discharged by K1 — this is
  K2's bypass-vs-routing question. Carried as [CONJECTURE]; caps the causal-upshot
  license at CONJECTURE-UNDER-TEST. The (a)/(c1) geometric endpoints do NOT need A2.
- **A3 — run pins:** E_run is the executed model's matrix; pinned snapshots (§8);
  Δθ=0 pre/post SHA-256 via the verbatim `get_hash` (run_exp077.py ll. 166–172);
  executor cross-checks against the archived pre_hash values. Mismatch = FATAL —
  no results reported (Law #6/#13).
- **A4 — EXP070:** excluded from vector endpoints (no verified vectors);
  Underdetermined cells, never filled by assumption.
- **A5 — binary scoring:** verified by code read (EXP077 ll. 669–682; EXP065/066
  same argmax structure — executor cites lines); grounds the §5.1 vacuity lemma.
- **A6 — bars pre-registered:** 0.9 (="essentially the target-row direction") and
  the majority-CI rule (="the typical item") chosen treatment-independently; K1 has
  had no data contact on these cosines (LOG-197 never computed them).
- **Promotion path:** IN-HOUSE-PROOF → PROVEN-LEMMA on LOG-206 SIGN of this plan +
  executor report reproducing the L1 proof; CONJECTURE-UNDER-TEST promotes only via
  K2 (bypass) evidence or equivalent — never by re-labeling.

**Signed:** Track-8 (LOG-205) · 2026-09-23 · **Law #14 review:** LOG-206, pending.

---

## 7. Verdict mapping (exhaustive — every outcome cell mapped, no "we'll decide later")

Per-run verdicts first (EXP065, EXP066, EXP077-official; smoke secondary labeled):

| (a) | (c1) | (b) diagnostic | Guards | Per-run verdict |
|---|---|---|---|---|
| KILL fires | any | any | pass | **Supported** (tilt confirmed) |
| any | PERSISTENCE fires | any | pass | **Supported** (tilt confirmed) |
| ruled out | ruled out | weakens/neutral | pass | **Not supported** (tilt exonerated) |
| ruled out | ruled out | f ≥ r/2 | pass | **Not supported** (geometry rules tilt out; (b) notes unclean effect — recorded, doesn't resurrect tilt) |
| neither fires nor ruled out | — | — | pass | **Inconclusive** |
| — | — | — | **fail** | **Refuted** (measurements invalid; no claim licensed; halt, report) |
| EXP070 vector cells | — | — | — | **Underdetermined** (no verified vectors; excluded) |

**Program-level aggregation (pre-registered):** K1-CONFIRMED iff **≥1 primary run**
lands Supported — rationale: the bridge *construction* is shared across runs; the
§H7 question is whether the construction *can* act as a pure target boost, and a
positive control must be clean in *all* its uses. K1-EXONERATED iff **all** primary
runs land Not supported. Otherwise **Inconclusive**. (A control is only as clean as
its dirtiest use; the CEO may override with reasons logged.)

**Guards (all FATAL on failure — halt, no verdict):**
G1. Bridge-identity re-verification: |cos(rebuilt b̂_i, LOG-197 formula)| ≥ 1−1e-6
  on all 60 items × 3 runs (the formula IS the rebuild; this guards transcription error).
G2. Label cross-check (§2): any item mismatch vs archived per-item records = FATAL.
G3. Δθ=0: pre/post SHA-256 match via verbatim `get_hash`, AND match the archived
  pre_hash values (§8). Any mismatch = FATAL, results not reported.
G4. (c2) identity: (b_swap,c_swap)==(c,b) exactly on recomputation from per-item records.
G5. No forward pass executed at any step (executor asserts; code inspection — the
  script contains no `model(...)` call on inputs).

**Banned language:** the verdicts above are the only permitted categories
(Supported / Not supported / Inconclusive / Underdetermined / Refuted).
"Promising", "interesting", "worth another experiment" are forbidden anywhere in
the executor report. p-values alone license nothing (§G1b standing ban respected).

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

- **K1-CONFIRMED (tilt Supported):** LOG-204 §H7 demotion locks in — mandatory and
  irreversible ("rescue control (known-answer direction), NOT a mechanism control");
  P1 pivot fires (output-side steering re-scoped to "label-assisted steering";
  mechanism-family pivot to closed-loop control — CLLC pilot licensed);
  **K3 does not run**; K2 not licensed as mechanism discriminator; Sprint-3 Stage-0
  pilots re-scoped (their bridge positive class is compromised — feasibility checks
  may continue, verdicts wait on re-scoping).
- **K1-EXONERATED (tilt Not supported):** CEO revisits §H7; K2 pilot licensed
  (GPU minutes); Sprint-3 Stage-0 pilots licensed (positive class intact); K3's CPU
  compliant-bridge construction audit proceeds; §H6 ordering resumes.
- **K1-Inconclusive:** battery holds; Sprint-3 pilots proceed with bridge status
  explicitly **[OPEN]** in their interpretation; no pivot fires on an inconclusive cell.
- **K1-Refuted (integrity):** no verdict; executor reports the failure; CEO decides.

---

## 10. Execution steps (for the executor, post-SIGN)

1. Assert env (§8 table); load run-pinned snapshots read-only; G3 hash gate.
2. Rebuild per-item (t_i, f_i) label strings via verbatim ports (§2); G2 cross-check;
   G1 bridge-identity guard.
3. Compute (a): {c_i} per run → stats + p̂_a + Clopper–Pearson 95% CI → apply §3 rule.
4. Read archived (b, c); recompute from per-item records where available; apply §4
   reading (diagnostic).
5. Compute (c1): {p_i} per run → p̂_c + CI → apply §5.2 rule. Compute (c2): assert
   §5.1 identity (G4).
6. D1: archived sign signature (already in hand) + ratio diagnostic vs L1 prediction.
7. Machine-readable twin JSON (unrounded values, per-item c_i/p_i arrays, hashes,
   env manifest) + this report's verdict table filled verbatim from §7.
8. Report in FACT/INFERENCE/HYPOTHESIS/SPECULATION + 10-label standard; evidentiary
   level L1 (readout-path geometry/causal-accessibility — no L2/L3 crossing).

---

## 11. What this plan does not do (binding scope)

No forward passes; no K2/K3 verdicts; no EXP070 vector endpoints (Underdetermined);
no GPU; no signed-artifact edits; no bridge reconstruction under Law #7 compliance
(that's K3's, gated); no novelty claim (N1 stands). The executor may not convert
Inconclusive into a negative, nor a diagnostic into a kill.

---

## 12. Knowledge-protocol obligations (one challenge + one idea)

- **Challenge:** the adopted (b) reading (f ≥ r/2 strengthens *tilt*) diagnoses
  broad disruption, while K1's Law-#15 Q1 asks about the *narrow* geometric tilt —
  for which the L1 license predicts f = 0. The plan keeps the adopted mapping
  verbatim (Law #4) and rests the kill on (a)/(c1), but LOG-206 should rule whether
  (b)'s reading needs re-registration before it can bear weight in any future
  tilt verdict. The tension is on the record here, not smoothed over.
- **Idea:** the D1 ratio diagnostic (r_obs vs r_pred) is a $0 causal-quantitative
  upgrade path: if the L1-predicted logit-shift ratios match the archived end-to-end
  ratios within 2×, the readout projection *quantitatively exhausts* the observed
  effect — tilt evidence stronger than geometry alone. If they diverge, the
  divergence localizes to downstream transformation, which *is* K2's question —
  either outcome pays for the program.

---

*Author: Track-8 (LOG-205) · 2026-09-23 · FROZEN pending LOG-206 Law #14 review.
Execution only after SIGN. On SIGN, the executor works §10 verbatim; any deviation
is logged per the deviation protocol (F3-class table-precision corrections allowed
with disclosure; endpoint/environment/margin changes are never F3).*
