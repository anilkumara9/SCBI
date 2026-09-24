# Adversarial Review — K1 Readout-Tilt Plan (LOG-205)

**LOG-206 · Track-7 (Independent Adversarial Reviewer) · 2026-09-23**
**Target:** `research/analysis_plans/K1_READOUT_TILT_PLAN_LOG205_2026-09-23.md` (FROZEN)
**Independence note:** no prior involvement in K1, the LOG-197 audit, or the direction
decision. All derivations below were recomputed from primary sources (runner code,
archived JSONs, adopted synthesis text), not trusted from the plan.
**Verdict: ESCALATE-TO-CEO** (point 1 — design change; legitimate verdict per dispatch,
not a failure of the plan-writer). Scope of escalation is narrow: everything else in
the plan is SIGN-ready modulo enumerated mechanical fixes.

---

## Verdict summary

| Attack point | Ruling |
|---|---|
| 1(i) vacuity proof | **CORRECT** — re-derived from scoring code |
| 1(ii) (c1) status | **DESIGN CHANGE** → ESCALATE-TO-CEO |
| 2. (b) tension | Verbatim-keep is the correct Law #4 posture; (b) survives as diagnostic; kill-on-(a)/(c1) structure honest given disclosure. (b)'s adopted reading needs re-registration before future tilt use (ruling on the §12 challenge: YES). |
| 3. Grade discipline | **PASS** — grades match §A.3; L1 and §3 derivations recompute; 3 MINOR L4 gaps |
| 4. Verdict-table exhaustiveness (M5.2) | **NEAR-PASS** — one drafting gap, mechanical fix |
| 5. Run pins / Underdetermined | **PASS** |
| 6. Standard battery | **PASS** |

**Law #15 on record:** Q1 — the plan minus (c1) is a faithful, executable,
honestly-graded falsification of the readout-tilt question; (c1) as specified is not
faithful to the adopted battery and needs a CEO decision. Q2 — **ESCALATE** (not
CONTINUE/SIGN): the $0 execution releases on the CEO's (c1) ruling plus the mechanical
fixes below, then targeted re-verification of the diffs. Q3 — cheapest: $0 read-only
review, done. Q4 — n/a honestly (review, not experiment).

---

## 1. The (c) operationalization question (load-bearing)

### 1(i). The vacuity proof is CORRECT — re-derived independently

Runner scoring, verified by code read (not trusted from the plan):

- EXP077 `experiments/runs/exp077/run_exp077.py` (`eval_item`): `chosen = A if
  logits[toks_A] > logits[toks_C] else C` — binary argmax between the two option tokens.
- EXP065 `experiments/scripts/run_exp065_temporary_coordinate_alignment.py`:
  `mod_correct.append(bool(t_l_m > f_l_m))` — binary.
- EXP066 `experiments/scripts/run_exp066_pythia410m_replication.py`:
  `is_mod_corr = bool(t_l_m > f_l_m)` — binary.

Re-derivation: per item, baseline logits ℓ_b, injected logits ℓ_m (injection fixed).
Orig-correctness: baseline B_i ⟺ ℓ_b[t_i] > ℓ_b[f_i]; injected M_i ⟺ ℓ_m[t_i] >
ℓ_m[f_i]. Swapped re-scoring treats the foil as target: swapped-correctness ⟺
ℓ[f_i] > ℓ[t_i] = ¬orig-correctness (strict `>`, absent exact ties). Hence
b_swap = #{i : B_i ∧ ¬M_i} = c_orig, c_swap = b_orig, and
**ΔM_swap = (b_swap − c_swap)/N = −ΔM_orig exactly**. The derivation uses only the
scoring structure and the fixed injection — it holds under both the tilt and the
mechanism hypothesis, so the endpoint cannot discriminate them. "Rescue-persistence"
(ΔM_swap ≥ +δ_min) is arithmetically impossible given ΔM_orig > 0. The lemma stands.

MINOR (fix F-V1): the lemma as stated claims exactness unconditionally; exact ties
(ℓ[t_i] = ℓ[f_i], possible in principle under strict-`>` scoring) would break the
identity. G4's FATAL-on-deviation covers this operationally, but the §5.1 statement
should carry the "absent exact ties" qualifier.

### 1(ii). (c1) is a DESIGN CHANGE requiring CEO sign-off — ESCALATE

There is no third option, so I pick: **design change**. Exact textual basis.

Adopted §H6 (SYNTHESIS_A_J_REV2_2026-09-23.md), verbatim:

> (c) **label-shuffle test** — re-score archived items with target/foil roles swapped: a
> true relational mechanism must now *hurt*; a readout tilt still "helps" toward the
> original target token. **Kill criterion:** (a) cos ≥ 0.9 OR (c) shows
> rescue-persistence under label shuffling (read under the §G1b CI+δ_min rule) → the
> bridge is readout bias; the "output-side mechanism" reading is withdrawn; the
> bridge's positive-control status is revoked to *rescue* control, not *mechanism*
> control.

Plan §5.2 (c1), verbatim in substance: measurand p_i = cos(−b̂_i, ŵ_{f_i}) ≥ 0.9 with
**lower 95% Clopper–Pearson CI of p̂_c > 0.5**; kill feeds "K1=Supported
('rescue-persistence under label shuffling' made geometrically precise)", presented
under the header "**Kill criterion (binding, from §H6)**".

Three independent reasons this is a design change, not a faithful operationalization:

**(a) Measurand and decision rule both changed.** The adopted (c) kill is
"rescue-persistence under label shuffling (**read under the §G1b CI+δ_min rule**)" —
a behavioral ΔM endpoint. (c1) is a geometric cosine-persistence endpoint under the
(a)-mirrored 0.9/majority-CI rule. An operationalization fills in underspecified
implementation details; it does not replace the measurand and the decision rule. The
"binding, from §H6" attribution in §5.2 is false — §H6 contains no such endpoint.

**(b) The discriminating logic changed, and the replacement logic is geometrically
inaccurate.** The spec's contrast is "mechanism hurts / tilt helps-t_orig". (c1)'s
stated rationale is "the target-boost property is label-independent formula geometry
(normalize(w_X − w_Y) ≈ ŵ_X for *whatever* X)". I derived: (a)-firing requires
‖w_f‖ ≤ 0.484‖w_t‖ (at cosθ=0); (c1)-firing requires ‖w_t‖ ≤ 0.484‖w_f‖. Per item the
two are near-mutually-exclusive (joint firing needs anti-aligned rows). So a
(c1)-alone firing — which the plan's OR-kill would fire on — does **not** show
"persistence" of the (a) property; it shows **foil-row dominance**, i.e. a
foil-suppression tilt, a different geometric claim than anything in §H6. The
"persistence" framing only coheres for the both-fire case. The plan's kill rule and
its rationale do not describe the same observation.

**(c) It expands the adopted kill surface past a mentor-adopted battery.** The
synthesis was adopted (LOG-195 ADOPT) as written. The adopted (c), being vacuous,
contributes nothing discriminating — so the effective adopted kill is (a) alone.
(c1) adds a second, unadopted kill branch (foil-suppression geometry). Repairing a
vacuous adopted endpoint is a protocol change; protocol changes to an adopted battery
are CEO decisions, not reviewer-blessable.

**This escalation is not a mark against the plan-writer.** Proving the vacuity openly,
keeping the literal reading as the (c2) integrity check (exactly the right use), and
submitting the repair for review instead of laundering it is exemplary Law #4/#14
conduct. The repair simply exceeds reviewer authority.

**What the CEO must decide (exactly):**
1. The status of (c1): (i) adopt it as the repaired (c) endpoint — in which case §5.2's
   rationale must be rewritten (the "persistence"/"label-independent formula geometry"
   framing is geometrically inaccurate for the (c1)-alone kill case; the honest
   alternatives are "both-fire = anti-aligned-row formula geometry" vs "(c1)-alone =
   foil-suppression tilt", each with its own stated discriminating logic) and the
   false "binding, from §H6" attribution removed; (ii) direct a different repair; or
   (iii) strike (c) as a discriminating endpoint and rest K1 on (a)+(b)+(c2)+D1.
2. Rule on the §12 challenge (my ruling below is a recommendation): (b)'s adopted
   reading must be re-registered before bearing weight in any future tilt verdict.

**Reviewer's recommendation (labeled [INTERPRETATION], CEO disposes):** option (iii).
(a) alone is a faithful implementation of the adopted kill criterion's first
disjunct; the adopted (c) is vacuous; a foil-suppression endpoint, if wanted, should
be pre-registered as a new numbered endpoint under a fresh LOG with its own
rationale — not smuggled in as "(c1)". This is the Law #4-clean path: no kill
surface beyond what the mentor adopted.

---

## 2. The (b) tension

**Ruling: the verbatim-keep is the correct Law #4 posture; the tension does not
invalidate (b); the kill structure is honest given disclosure.**

- Adopted §H6 (b), verbatim: "**diagnostic readout** (not a standalone kill):
  symmetric correct→wrong flips (bias) vs only wrong→correct (rescue);
  pre-registered reading — f ≥ r/2 strengthens a tilt verdict, f ≈ 0 with r > 0
  (lower 95% CI > δ_min) weakens it, reported as [OBSERVATION] feeding the K1
  verdict."
- The plan keeps this mapping verbatim and rests the kill on (a)/(c1), with the
  tension disclosed twice (§4 caveat, §12 challenge). Rewriting (b)'s reading
  in-plan to match the license would be the actual Law #4 violation (post-hoc
  hypothesis shift to rescue a favored reading). The writer chose correctly.
- (b) is not demoted to decoration: the adopted spec already demotes it ("not a
  standalone kill"), and the plan preserves a defined verdict-table role — rows 3/4
  split on the (b) reading, and §4 assigns it the cleanliness-diagnostic function
  (f ≥ r/2 ⟹ "not a clean directional effect at all"). It feeds the verdict; it does
  not fire the kill. That is its adopted job.

**Ruling on the §12 challenge (does (b)'s reading need re-registration before future
tilt use): YES.** The adopted mapping is backwards relative to the program's own L1
license: L1 proves a pure readout tilt strictly increases the t−f margin
(Δℓ_t − Δℓ_f > 0 for the injected direction), hence predicts f = 0 exactly. The
archived f = 0, r > 0 pattern is tilt-*confirming* under the license and
tilt-*weakening* under the adopted mapping — a direct contradiction, and the
license is the proven statement. The adopted (b) reading diagnoses broad disruption
("bias" as noise), not the narrow geometric tilt of K1's Law-#15 Q1; the two were
conflated in the adopted text. For **this** execution the verbatim-keep + disclose
posture is correct and (b) must not modulate the (a)-kill; before (b) bears weight
in any future tilt verdict, its reading must be re-registered (recommendation: align
with L1 — f ≥ r/2 contradicts a *clean* tilt; f = 0 is the tilt-predicted pattern).

Minor structural note (non-blocking): the verdict table lets (a)-KILL override any
(b) reading without modulation (rows 1–2, "(b) diagnostic: any"). With archived f=0
this is moot, but a future f ≥ r/2 ∧ (a)-fire conjunction has no pre-registered
meaning — worth one sentence when (b) is re-registered.

---

## 3. Grade discipline (§A.3) — PASS with 3 MINOR L4 gaps

- **IN-HOUSE-PROOF for L1 + geometric endpoints (a)/(c1): correct.** The L1 lemma is
  proven in-house with the complete proof reproduced; it has not yet survived
  adversarial review — LOG-206 is that review — which is exactly the §A.3
  IN-HOUSE-PROOF definition ("Proven in-house, proof complete, but not yet through
  adversarial review. Provisional."). Promotion to PROVEN-LEMMA conditioned on LOG-206
  SIGN is the correct promotion path (rubric: "Full run requires promotion via Law
  #14 review of the proof").
- **CONJECTURE-UNDER-TEST for the causal upshot (tilt geometry ⇒ rescue caused by
  readout tilt): correct.** No proof; A2 (mid-network propagation) is undischarged and
  carried as [CONJECTURE]; K1 *is* the falsification attempt; $0/zero-forward-pass =
  the cheapest discriminating experiment per Law #15 Q3. Weakest-load-bearing-grade
  ceiling respected. INTUITION nowhere — the protocol starts.
- **L1 derivation recomputed:** Δℓ = W_U(αv̂); t-th row gives
  Δℓ_t = α(W_U[t,:]·v̂) = α‖W_U[t,:]‖₂cos(v̂,ŵ_t) ✓. Corollary (cos ≥ 0.9 ⟹
  Δℓ_t ≥ 0.9α‖W_U[t]‖₂) holds since all α_run > 0 (1.0/1.0/0.5) ✓.
- **§3 non-vacuity recomputed:** c = cos(b̂,ŵ_t) = (‖w_t‖ − ‖w_f‖cosθ)/‖w_t − w_f‖,
  so c ≥ 0.9 ⟺ ‖w_t‖ − ‖w_f‖cosθ ≥ 0.9‖w_t − w_f‖ ✓; at cosθ=0 ⟹
  ‖w_f‖/‖w_t‖ ≤ √(0.19/0.81) ≈ 0.4843 ✓ (plan: 0.484 ✓); equal-norm orthogonal rows
  ⟹ c = 1/√2 ≈ 0.7071 < 0.9 ✓. The bar does not fire on generic geometry — non-vacuous.
- **L2** states numbers, tolerance, coverage; "No point forecast is registered
  (Law #2)" is the correct Law #2 posture ✓.
- **L4 gaps (MINOR — none demotes the L1 grade; they attach to statistics/operations,
  not the lemma; add as A7/A8 or fold into A5):**
  - F-G1: item-independence for the Clopper–Pearson CI (60 items treated as
    independent Bernoulli trials) is assumed, not listed.
  - F-G2: non-degenerate ‖w_t − w_f‖₂ not assumed — the plan asserts t_i ≠ f_i, but
    distinct tokens can have near-identical rows, making b̂ noise-dominated. Executor
    should assert/report min_i‖w_t − w_f‖₂.
  - F-G3: A5's binary-scoring verification should note the executor must cite the
    Stage-B scoring lines for EXP066 too (verified here:
    `is_mod_corr = bool(t_l_m > f_l_m)`), and the vacuity lemma needs the
    "absent exact ties" qualifier (same fix as F-V1).

---

## 4. Verdict-table exhaustiveness (Charter M5.2) — NEAR-PASS, one mechanical fix

- **Fix F-T1 (mechanical):** row 5's (a) cell reads "neither fires nor ruled out",
  which literally leaves cells ((a)=ruled-out, (c1)=neutral) and ((a)=neutral,
  (c1)=ruled-out) uncovered. Reword to "(a) did not fire" (keeping (c1) "—" as any),
  i.e. "no kill fired and not both ruled out → Inconclusive". Then every cell of
  {(a)}×{(c1)}×{(b)}×{guards} lands in exactly one branch.
- Guards-fail → **Refuted** takes precedence over all endpoint cells ✓ (correct per
  Law #13 — integrity failure voids measurements).
- All three (b) readings covered: f ≥ r/2 → row 4; weakens/neutral → row 3 ✓.
- (a)-fire and (c1)-fire both map to **Supported** — no conflicting-branch cell ✓.
- **Aggregation rule:** "K1-CONFIRMED iff ≥1 primary run lands Supported …
  K1-EXONERATED iff all primary runs land Not supported … Otherwise Inconclusive."
  Disclosed pre-registered choice with rationale (shared construction; "a control is
  only as clean as its dirtiest use"); the adopted battery does not specify
  aggregation. **§H7 lock-in correctly scoped** — verified against LOG-204 Ruling 1
  verbatim: "K1-confirms-tilt → demotion mandatory and irreversible; K1-exonerates →
  CEO revisits." ✓
- Observation (not a finding): ≥1-of-3 runs at 95% inflates the family-wise
  false-confirm rate; the plan's rationale + CEO-override clause make this a
  disclosed judgment call, not a smuggled one. No action required.

---

## 5. Run pins and Underdetermined discipline — PASS

- Pins correct per the F-200-2 correction and LOG-211 absorption check:
  EXP065→`EleutherAI/pythia-160m`/L10, EXP066→`pythia-410m`/L20,
  EXP077→`pythia-410m`/L20; each run uses its own pinned unembedding matrix; §8 pins
  exact (snapshots `50f5173d…`/`9879c9b5…`, `local_files_only`,
  `trust_remote_code=False`, float32, `model.eval()`); venv
  `/home/hatch/workspace/.venv_smoke` exists; torch 2.14.0+cpu / transformers 5.17.0 /
  numpy 2.5.3 asserted in-script.
- Archived inputs spot-verified against primary records (not trusted): EXP065
  (b,c)=(10,0) ✓, Δℓ_t=+0.3597/Δℓ_f=−0.4042/Δmargin=+0.7639 ✓
  (`exp065_results.json`); EXP066 (8,0) ✓ (`exp066_replication_results.json`);
  EXP077 official (6,0) ✓ (research_log LOG-128: "Bridge gate PASSED (C8 +10pp,
  b=6,c=0,p=0.03125)"); ΔM CIs match the adopted §G1b table ✓.
- EXP070 excluded from all vector endpoints; Underdetermined cells never filled by
  assumption ✓. Tidy note (non-blocking): §1.1 permits EXP070's log-cited (10,0) "as
  labeled secondary in (b) only" but §4 does not exercise it — either include it
  labeled-secondary or drop the permission; do not leave executor discretion.
- Δθ=0 guard adequate: G3 = verbatim `get_hash` pre/post SHA-256 + cross-check vs
  archived pre_hash; FATAL on mismatch, no results reported ✓. G5 (no forward pass;
  code inspection) ✓.

---

## 6. Standard battery — PASS

- **Numbers pre-registered:** 0.9 bar ✓, f ≥ r/2 ✓, δ_min = 0.05 ✓ (in (b)'s CI
  clause), Tango-1998 exact CIs for the (b) ΔM clause (reproduced to 4dp per LOG-197)
  ✓, Clopper–Pearson exact CIs for (a)/(c1) ✓.
- **Kill criteria bite (verified, not trusted):** (a)-KILL (lower 95% CI of p̂_a >
  0.5) needs **≥39/60** items ≥ 0.9 (38/60 → lower CP = 0.4990, no fire);
  (a)-RULED-OUT (upper CI < 0.5) needs **≤21/60** (22/60 → upper = 0.5010, no fire).
  Wide honest Inconclusive band; bars are non-vacuous and asymmetric-power-safe.
- **Five categories only** (Supported / Not supported / Inconclusive /
  Underdetermined / Refuted); banned words ("promising", "interesting", "worth
  another experiment") appear solely inside the ban-list sentence itself ✓.
  Program-level K1-CONFIRMED/K1-EXONERATED are mapped to the per-run categories ✓.
- **Labels:** FACT/INFERENCE/HYPOTHESIS/SPECULATION + 10-label standard applied to
  load-bearing claims throughout §§1–8; D1's 2× tolerance honestly tagged
  [ARBITRARY] with rationale ✓.
- **Consequences match the adopted decision:** confirm → §H7 demotion locks
  (mandatory/irreversible) + P1 fires + K3 stands down ✓ (LOG-198 §1, LOG-204
  Ruling 1); exonerate → CEO revisits §H7 ✓; Inconclusive → HOLD with bridge status
  [OPEN] ✓.

---

## Mechanical fixes required before SIGN (after the CEO's §1 ruling)

1. **F-V1:** §5.1 vacuity lemma — add "absent exact ties" qualifier (strict-`>`
   scoring); G4's FATAL-on-deviation already covers the operational side.
2. **F-T1:** §7 row 5 — reword (a) cell to "(a) did not fire" so the M5.2 partition
   is literally exhaustive (covers (a)=ruled-out/(c1)=neutral and the mirror cell).
3. **F-G1/G2/G3:** L4 — add A7 (item-independence for the Clopper–Pearson CI), A8
   (non-degenerate ‖w_t − w_f‖₂; executor asserts/reports min), and the A5
   line-citation + tie qualifier.
4. **F-S1:** §1.1 vs §4 — resolve the EXP070 log-cited (10,0) "may appear as labeled
   secondary" permission (include labeled-secondary or delete the permission).
5. **F-C1 (contingent on CEO adopting (c1)):** rewrite §5.2's rationale (the
   "persistence" framing is geometrically inaccurate for the (c1)-alone kill case —
   see §1(ii)(b)) and remove the false "binding, from §H6" attribution.

Targeted re-verification of the diffs only; no re-review of the full plan needed.

---

## What the writer got right (on record)

The vacuity proof, the (c2)-as-integrity-check design, the verbatim-keep of the (b)
mapping with the tension disclosed rather than smoothed, the A2-undischarged honesty
capping the causal grade, the [ARBITRARY] tag on D1's 2×, the EXP070 Underdetermined
discipline, and the §12 challenge inviting exactly this review — this is how
falsification-first plans are supposed to be written. The escalation is about
jurisdiction over an adopted battery's endpoint, not about the quality of the work.

---

*Reviewer: Track-7 (LOG-206) · 2026-09-23 · Independent — no prior K1/LOG-197/direction
involvement. Methods: scoring-code reads (3 runners), archived-JSON spot checks,
independent re-derivation of the vacuity lemma, L1, and §3 algebra, Clopper–Pearson
threshold computation, verbatim cross-checks against SYNTHESIS_A_J_REV2 §G1b/§H6/§H7,
the license standard §A.3, Charter M1–M8/M5.2, LOG-198 §1, LOG-204 Ruling 1, and
AGENTS.md Laws #2/#4/#9/#11/#14.*
