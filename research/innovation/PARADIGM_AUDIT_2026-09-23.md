# Paradigm Audit + Compute Strategy — 2026-09-23 (LOG-198)

**Role:** Track-5 superintelligence/AGI architecture × Track-6 systems (direction review)
**Commission:** LOG-198 (CEO directive, parallel CPU-only track; the LOG-197 audit chain is NOT disturbed)
**Inputs read before writing (knowledge protocol discharged):**
`research/synthesis/SYNTHESIS_A_J_REV2_2026-09-23.md` (§§C, D, H, I, J),
`research/synthesis/CLUSTER_A_2026-09-23.md` (full),
`research/innovation/SPRINT_2026-09-23.md` + `SPRINT2_2026-09-23.md` (full),
`research/analysis_plans/G1_REPORT_2026-09-23.md` (full),
`research/RESEARCH_OPERATING_SYSTEM.md` (§4 compute discipline; §5 revolution test),
`research/MENTORSHIP_DIRECTIVE.md` (P1–P4, three evidentiary levels, verdict standard),
`experiments/protocols/EXP068_LOOP_PREREG_SPEC.md` (§§4, 12 — budget table),
`reports/research_log.md` (LOG-109/110, LOG-160–162, LOG-172, LOG-176, LOG-182, LOG-195, LOG-197, LOG-198).
**Cost:** $0 GPU. No experiments run. No weights touched. No new experiment numbers minted; proposals are proposals.
**Epistemic standard (binding):** every load-bearing claim carries FACT / INFERENCE / HYPOTHESIS / SPECULATION
plus the repo 10-label (AGENTS.md §5) and its evidentiary level L1/L2/L3
(L1 = can improve inference ≠ L2 = changes the computational strategy ≠ L3 = creates qualitatively
new capability — no silent crossing). Verdicts use ONLY: Supported / Not supported / Inconclusive /
Underdetermined / Refuted.

---

# (a) PARADIGM AUDIT — is Pythia-410m / layer-20 / static-steering a fertile hunting ground or a local minimum?

## A1. The evidence ledger (endpoints, not vibes)

**[FACT]**/[OBSERVATION], L1/below-L1 (boundary): raw cross-vocabulary cosine of relational contrast
directions is +0.7186 (EXP065, pythia-160m) and +0.6852 (EXP066, pythia-410m); static injection of the
aggregated basis B_agg yields ΔM = 0.0pp (b=c=0, McNemar p=1.0) on N=60 benchmarks with verified headroom
(19 and 26 rescuable errors). The dissociation (geometric similarity ≈0.7, zero causal transfer) is the
program's best-evidenced proposition — **verdict Supported** (boundary I1).

**[FACT]**/[OBSERVATION], below L1: five independent static-geometry families are decision-flat at
Pythia-410m/L20 — (1) EXP064/065/066 static B_agg (ΔM=0, b=c=0); (2) EXP077 radial α∈{0.25,0.5,1.0,2.0}
(all ΔM=0); (3) EXP077 angular cone-vs-line (all ΔM=0, p=1.0); (4) EXP077 cone-vs-control and α=1.0 offset
(ΔM=0); (5) EXP078's subspace localization (median projected bridge energy 0.0544 < 0.10 —
ENERGY_GATE_HALT). EXP077's licensed kill is narrow (unconditional ρ=30° cone, α=1 offset;
gated/conditional variants survive) — the kill is **Not supported** (static geometric variants rescue)
*within the licensed bounds*, not globally.

**[FACT]**/[OBSERVATION], below L1: the Procrustes operator the program tested was mathematically unsound —
rank-≤2 unembedding-space fit applied to full-rank hidden-state directions, reducing cross-vocabulary cosine
to +0.0032/−0.0118 (Δcos = −0.7154/−0.6971); the "aligned-basis injection fails" verdict is
**Inconclusive** (never tested with a sound operator). EXP067 halted at Stage A (rank 33/64) — no sound
dynamic alignment has been tested at all.

**[FACT]**/[OBSERVATION] (G1, LOG-134), below L1: the "Core Causal Null-Space Theorem" (§3.3 central
sentence) is **Refuted** as a QK-subspace claim — failed direction B_agg is unusually QK-visible
(Ē_QK=0.389985, above the random null 95th percentile 0.361730), while the rescuing bridge is
QK-unremarkable (Ē_QK=0.356185, mid-null) — the exact inversion of the theorem's prediction. The
QK-subspace operator program is stood down. Mechanism for the inertness: readout-misalignment-or-unknown
[CONJECTURE]/[OPEN].

**[FACT]**/[OBSERVATION], L1: the output bridge (normalize(E[target]−E[foil]), option-informed) rescues
decisions repeatedly: EXP065 +16.67pp (b=10,c=0); EXP066 +13.33pp (b=8,c=0); EXP070 C7 +16.67pp (b=10,c=0);
EXP077 official GPU +10pp (b=6,c=0, CI [+0.0338,+0.2015] — does NOT clear δ_min=0.05, does NOT survive the
Level-2 multiplicity budget α₂=0.00714); EXP077 smoke +23.33pp. **Verdict: Supported** as *readout-path
steerability* (L1). The rescue *mechanism* is [CONJECTURE]/[OPEN]; the bridge is **always c=0** (zero
corruptions — a signature worth noting, not a license).

**[FACT]**/[OBSERVATION], L1: EXP070 branch (c2) UNINFORMATIVE_PROBE — oracle selection over the
hidden-state candidate pool yielded ΔM=+0.00pp; the probe carried no transferable signal; ceiling
**Inconclusive** (unmeasured, not zero); EXP068 explicitly NOT cancelled by this. EXP075 aborted (infeasible
probe by construction — F2 guard fired: 11/35 entities multi-token); re-registered as EXP078.

**[FACT]**/[OBSERVATION]: the entire corpus's positive evidence is L1 or below. Nothing reaches L2
(changes the computational strategy) or L3 (qualitatively new capability). The field has moved:
Steering Vector Fields (Feb 2026, offline field + training-free KNN baseline beats static CAA) and
Activation-LQR (Apr 2026, closed-loop feedback control with tracking-error bounds) — both verified-live
per the field sweep — demote static CAA to the field's *ablation baseline*. The program has NOT tested
adaptive/closed-loop methods at scale; EXP068 (adaptive G/E/S/T loop) is signed but shelved without its
registered gate.

## A2. The paradigm verdict

**[INFERENCE]**/[INTERPRETATION], program-level: the Pythia-410m/L20/static-steering program is
**a local minimum as a capability-discovery program** and **a fertile substrate as a boundary-science
program**. These two verdicts are distinct and both stand:

- **Local minimum for discovery — verdict: Not supported (as a discovery substrate).**
  The convergence is overdetermined, not accidental: five static-geometry families flat (A1), the
  only tested alignment operator unsound, the QK mechanism refuted, the evaluator-validity of the one
  adaptive formulation (G/E/S/T) [CONJECTURE]/unvalidated, and the field's 2026 occupants (SVF, A-LQR)
  already dominating the tested operator family (CAA-equivalence → N0 for the mechanism). The repeated
  pattern — "measure geometry, inject statically, ΔM=0" — is the definition of an exhausted gradient:
  the cost per falsification is trivial (~500 passes, <30 min T4), yet each falsification leaves the
  next variant standing one room over with the same un-asked mechanism question. Continuing to
  enumerate unconditional static-geometry variants at L20 is [INFERENCE] theory preservation dressed
  as diligence: the nulls are honest, the iteration is not.

- **Fertile for boundary science — verdict: Supported (as a boundary substrate).**
  The I1 dissociation is a *diagnostic instrument* (Cluster A §C3): "raw geometric similarity vs.
  causal transfer" separates geometric structure from causal structure, and any successor mechanism —
  ours or the field's — can be run through it. The five dead rooms under narrow licenses are a map
  of where the mechanism isn't, with unusual precision. That map is publishable boundary science;
  it is also the launch pad for any pivot, because it constrains what the successor must NOT be.

**[INFERENCE]**/[INTERPRETATION] (track 5): the honest accounting of the current substrate's *live*
signals is exactly one — the output-side bridge — and it is under three standing attacks it has not
answered: K1 (readout-tilt falsification, cos≥0.9 / label-shuffle persistence), K2 (bypass-vs-routing
discriminator, 180 passes), K3 (Law #7 compliance — the bridge is option-informed by construction;
an autonomous mechanism needs a compliant construction that rescues). Until K1 rules, there is no
positive-evidence base for an autonomous mechanism program — only a steering observation. The K-ordering
is binding on interpretation for exactly this reason: if K1 confirms tilt, the K3 audit dissolves
(there is no mechanism left to audit for label compliance).

**[SPECULATION]**/[CONJECTURE] (track 6, systems): the binding resource constraint (~25 GPU-hours total,
no budget, one Kaggle session at a time) is not the program's real bottleneck — the bottleneck is the
*verdict budget*: the rate at which pre-registered falsification attempts can be designed, reviewed
(Law #14), and adjudicated. GPU time for the L1 adjudications below totals under 3 hours. Spending
the rest on more static geometry would be the failure mode the mentor named: machinery without
map/protocol fixes = scope creep.

## A3. STAY vs QUIT/PIVOT criteria — falsifiable, pre-registerable in spirit

These criteria name the exact observations in the next 1–2 experiments that keep the program on this
substrate vs force a pivot. They are ordered by the §H6 battery (K1 first — it is $0 and logically
prior; K2/K3 preparation may parallelize, interpretation waits on K1).

### KEEP — all five must hold for the program to STAY on Pythia-410m/L20 with the current mechanism family

1. **K1 fails to confirm readout tilt** [OBSERVATION]: cos(bridge direction, unembedding row of
   t_target) < 0.9 (pre-registered) AND the label-shuffle test shows the rescue *hurts* (roles-swapped
   scoring), not rescue-persistence. Verdict licensed: the output-side room is more than a target boost.
   (Fires on $0 CPU, archived artifacts — the first thing the program runs.)
2. **K2 shows routing, not bypass** [OBSERVATION]: premise-entity-position injection rescues while
   final-token-only injection does not (exact two-sided 95% CI for (ΔM_b − ΔM_a) clears δ_min=0.05,
   L > 0.05). Verdict licensed: the bridge engages upstream attention computation — there is a
   mechanism to chase, not just a logit tilt.
3. **K3: the Law-#7-compliant bridge rescues** [OBSERVATION]: bridge reconstructed from premise-entity
   tokens only (or donor items with the entity-similarity-leak control) yields ΔM > 0 (lower 95% CI > 0;
   margin-clearing, L > δ_min, preferred). Verdict licensed: autonomous (label-free-at-eval) output-side
   steering exists.
4. **EXP080 (G2 oracle ceiling) shows non-bridge marginal rescue** [OBSERVATION]: the marginal-rescue
   decomposition's bin (ii) > 0 — i.e., oracle selection over the output-side pool rescues items the
   bridge does not. Verdict licensed: there is a *selection prize* in the output room beyond the bridge —
   an evaluator program (DPRS/E7) has headroom worth building. If bin (ii) = 0: "bridge ceiling, not
   pool ceiling" — all evaluator-shaped work over this pool is stood down (the spec's pre-registered
   consequence, LOG-167/B2).
5. **EXP081 (C-A donor transfer v2) shows transfer** [OBSERVATION]: donor-centroid bridge ΔM > 0,
   Supported at L1 (lower 95% CI > δ_min, McNemar, N=60), while the entity-similarity-leak control does
   not rescue. Verdict licensed: the bridge's power is relation-general, not item-specific — the
   program's first label-free-at-test-time capability primitive.

If 1–5 all fire: STAY. The substrate is licensed for one more generation: the EXP068 loop re-pointed
at the output room (DPRS — search in readout space, not the causally-dead contrast space), or the
closed-loop controller pilot (CLLC) built on a surviving K2 mechanism.

### PIVOT — any one of these forces a pivot (substrate, scale, or mechanism-family change)

- **P1. K1 confirms readout tilt** (cos ≥ 0.9 OR label-shuffle rescue-persistence under the §G1b
  CI+δ_min rule): the bridge's positive-control status is revoked to *rescue* control (per §H7 the
  demotion decision itself is the CEO's, logged explicitly). **Pivot:** mechanism-family → closed-loop
  control (CLLC) or donor-transfer-free generation; the output-side *steering* program is re-scoped to
  "label-assisted steering" (N0 vs CAA with a known-answer direction — the §B attack applies). Do NOT
  keep searching the output room for a mechanism that died at K1.
- **P2. K1 survives but K2 shows bypass** (ΔM_a ≥ ΔM_b, CI for (ΔM_b − ΔM_a) with U < δ_min): the bridge
  is logit steering, period — Supported for bypass, Not supported for routing. **Pivot:** mechanism-family
  → generation-step controllers (bridge-amplified CoT, Sprint2 C-C: intervene on the reasoning
  *trajectory*, not the final readout) or closed-loop feedback; the "output-side mechanism" program is
  closed as mechanism science (survives only as engineering — H4 demote branch).
- **P3. K1/K2 survive but K3 fails** (compliant bridge ΔM = 0 while option-informed bridge rescues):
  the output-side room as an *autonomous mechanism* is Not supported — the rescues are a label-assisted
  readout-steering artifact. **Pivot:** substrate → a paradigm where the direction source is
  label-free by construction (donor banks with strict Law #7 provenance, NLA intent-derived directions
  — Sprint New Idea 7, gated on host-model availability), or mechanism-family → verifier/controller
  separation (Cluster A E4: the verifier never sees labels either).
- **P4. EXP080 bin (ii) = 0** (bridge ceiling, not pool ceiling): **Pivot:** the evaluator/search
  program over activation-space pools is stood down entirely; resources redirect to (i) the K1–K3
  mechanism adjudication, (ii) the closed-loop controller pilot (which does not need a pool), and
  (iii) boundary publication. This is Sprint2's "verifier-first" gate doing its job.
- **P5. EXP081 donor ΔM = 0 while self-bridge rescues** (per the pre-registered kill): the bridge is
  item-specific; transfer hopes for this intervention family are dead. **Pivot:** mechanism-family →
  closed-loop control or multi-step trajectory repair (Sprint2 C-C); the donor-transfer line is closed
  and stays closed (Law #8 — dead ideas stay dead unless new evidence resurrects them).

**What "pivot" means concretely** (the three named options, [INFERENCE]/[PROPOSITION]):
(a) *Substrate change:* Gemma 3 + Gemma Scope 2 SAE-feature steering (Sprint New Idea 4 — the only
substrate proposal that changes the *unit* of intervention from raw directions to identifiability-guarded
features, with the invalid-run branch pre-registered); (b) *Scale change:* Pythia-2.8B/6.9B or a bigger
frozen model at matched compute — licensed ONLY with the forced-bigger-model baseline already run
(§I condition 1); (c) *Mechanism-family change:* open-loop additive steering → closed-loop feedback
control (CLLC/A-LQR lineage — the 2026 field direction the program has not tested).

### QUIT — the family-level kill (per adopted §H3; no discretionary rescue path)

The temporary-computation mechanism family is **Refuted** and the arm closed iff ALL of: (1) every
eligible candidate lands in G-Branch F1–F4 (no Branch S); (2) no Box-1 fingerprint passes (no L2
evidence anywhere — gains, if any, are L1-only); (3) harm ledgers show no rescuable subset; (4) no
candidate beats the oracle-fixed ceiling. **Consequence (pre-registered):** no new C-variants, no
re-tuning rescues; resources redirect to publishing the negative — *why temporary computation cannot
add capability under Δθ=0 is itself a boundary claim of publishable value* — plus mechanistic
understanding of the boundary. The §J roadmap's honest consequence stands: at pre-registered N=80,
Branch S is likely unreachable; an L2+ bid requires a re-registered N (see §B2 arithmetic).

---

# (b) COMPUTE STRATEGY — max signal per GPU-hour on ~25h of free Kaggle (2×T4, one session at a time)

## B1. Cost model [FACT — program-measured where stated; estimates tagged]

- Throughput: **~22 fwd/s on pythia-410m** on 2×T4 [OBSERVATION — Sprint2 standing fact].
- EXP068's own budget table: **0.5 s/pass on pythia-160m** for the loop's per-instance trajectory
  (multi-step overhead), worst case ≈ 13 h for ~93k passes; expected a small fraction.
- Standing discipline (§4): forward-pass costing before design; cheap screens gate expensive runs;
  $0 pre-registration gates (LOG-177: leakage pre-audit; geometric-identity check) attach before any
  donor/control design is signed.

**Total spend plan: ~3h of the 25h for the licensed falsification sequence; ~22h held in reserve**
for the powered re-registrations that verdicts license (see the sequencing table's "reserve" row).
Spending the reserve now — before K1 rules — is the exact failure mode P3/P4 forbid: buying
machinery when the map is undecided.

## B2. MDE arithmetic — explicit, for every candidate run (exact McNemar, c=0)

Decision rule (binding stats revision, §G1b): every primary comparison reports Δ̂M with the exact
two-sided 95% CI; δ_min = 0.05 (5pp); L > δ_min → Supported; U < 0 or U < δ_min → Not supported;
otherwise Inconclusive (held, never culled). The program's NTDP power rule (adopted, §G4): a
candidate whose MDE > 2·δ_min is held (Inconclusive) at that level — no N increase is pre-registered
in the current protocols; any N increase requires a new pre-registration with its own MDE computation.

Exact-McNemar MDE at c=0: MDE = min{b : 2·(1/2)^b ≤ α} / N.
- Level-1 (α=0.05, two-sided): b ≥ 6 (2^6=64 → p=0.03125 — the EXP077 official cell).
- Level-2 (α₂=0.00714, 99.286%): b ≥ 9 (2^9=512 → p=0.003906).

| Planned N | L1 MDE | L2 MDE | vs 2·δ_min = 10pp |
|---|---|---|---|
| 45 (EXP068 test phase) | 13.3pp (6/45) | 20.0pp (9/45) | both > 10pp — **held at both levels** |
| 60 (EXP080/081/K2/K3) | 10.0pp (6/60) | 15.0pp (9/60) | L1 at boundary; L2 > 10pp — **L2 claims held** |
| 80 (NTDP) | 7.5pp (6/80) | 11.25pp (9/80) | L2 > 10pp — **Branch S held** (the adopted honest consequence) |
| 100 (re-registered) | 6.0pp (6/100) | 9.0pp (9/100) | L2 clears — **minimum N for any L2-adjudicating run** |

**[INFERENCE]**/[INTERPRETATION]: no run at any currently planned N can license a Level-2 verdict —
this is not a budget problem, it is a registration problem. The honest use of the 25h is L1
adjudication (kill/survive at the mechanism level) plus $0 falsifiers; any L2+ bid waits for a
re-registered N≥100 protocol — whose GPU cost is itself trivial (~1,000 passes ≈ minutes at
22 fwd/s), but which the program may not reach for until the K1–K3 battery rules, or the powered
run adjudicates an unlicensed mechanism (theory preservation).

## B3. Pilot-first discipline — what each pilot must show before the full run is licensed

1. **K1 (readout-tilt): no pilot — it IS the $0 screen.** Runs first, on archived EXP065/066/077
   artifacts: cos(bridge, unembedding row of t_target) vs the pre-registered 0.9 bar; correct-item
   flip analysis (diagnostic readout, pre-registered f ≥ r/2 strengthens tilt); label-shuffle test.
   **Licenses:** K3's bite (a tilt verdict dissolves the Law #7 question — no mechanism left to audit).
2. **K2 pilot (180 passes, ~minutes):** the pilot IS the experiment — there is no larger K2. What it
   must show to license K3's interpretation: either routing (b-position rescue, a-position null —
   mechanism exists upstream) or bypass (a ≥ b — the output-side mechanism program closes). A flat
   null on both arms is itself information: the archived b_mean does not transfer to the signed
   EXP077/078 benchmark under position ablation → Inconclusive on mechanism, K3 proceeds regardless.
3. **K3 (compliant-bridge build): pilot = the construction algebra, verified on CPU before GPU.**
   The weight-only construction (premise-entity unembedding rows; donor centroids) is computed and
   its Law #7 compliance audited (construction inputs enumerated — no option tokens) with $0
   passes. **The test phase (~400 passes) is licensed only if** the construction audit passes AND K1
   did not confirm tilt. If K1 confirmed tilt, K3 does not run — auditing the label compliance of a
   confirmed readout tilt is wasted motion (pre-registered ordering).
4. **EXP080 (G2 oracle ceiling): no pilot — it IS the evaluator gate.** Licensed to run as signed
   (EXP080, PRE-REGISTERED, LOG-172). **Before the full NTDP-style search program is ever built,**
   EXP080 must show bin (ii) > 0 (non-bridge marginal rescue). The (d)/(e) licenses are gated on
   non-bridge marginals — survival cannot ride the bridge's back (LOG-167/B2).
5. **EXP081 (C-A donor transfer v2): pilot = the attached $0 pre-audit (done).** g(C3)=1.061783
   (4.25× floor), low stratum 49 items / 23 headroom, C4′ hardened. **Licensed to run once** LOG-197's
   bridge-leakage audit lands and the CEO clears GPU. Its kill criterion is pre-registered: donor
   ΔM ≤ 0 while self-bridge rescues → transfer hope dead for this family.
6. **CLLC closed-loop controller pilot (the replacement big-bet candidate): pilot on pythia-160m
   first** — 60 items × (6 conditions + per-item Jacobians ≈ 2–3F each) ≈ 1–2 h T4. **What the pilot
   must show before any 410m run:** (i) Jacobian conditioning κ ≤ pre-registered κ_max (control
   authority exists); (ii) measured setpoint-tracking error within the bound's order of magnitude
   (the A-LQR "faithful-but-inert" cell is pre-registered: ΔM=0 with bounds holding → the controller
   formulation is withdrawn for relational reasoning — report as a negative); (iii) ΔM_CLLC > 0 with
   lower 95% CI > δ_min where open-loop injection of the same final correction does not rescue
   (feedback-vs-open-loop is the discriminating comparison). A 160m pilot failure on (i) or (ii)
   kills the 410m run before it spends.
7. **Anisotropy / template-contamination analyses ($0, P3-style):** compare raw vs corpus-centred
   cross-vocab cosines vs the 1/√d chance band; rebuild per-vocab directions with rotated relation
   wording. **What they must show before any centred-basis *injection* GPU run (Sprint Idea 5 /
   EXP073-class):** that the raw 0.7 survives centring as geometric signal. If the 0.7 collapses to
   the chance band under centring, the boundary paper's positive half is restated (shared geometry =
   anisotropic bias) and the centred-injection run is stood down — the null was a hygiene artifact,
   not a mechanism to chase further.

## B4. The EXP068 ruling — honest, head-on

**Is shelving our biggest bet (~93k passes) while grinding small nulls the right call?**

**Short answer: yes — and the honest version is stronger than "the gate hasn't licensed it."**
[INFERENCE]/[INTERPRETATION], five converging reasons:

1. **The gate is unmet, and the gate is the right gate.** EXP068's registered gate (ρ-gate +
   §4b transfer probe + headroom halt) has not licensed execution. Running it anyway would violate
   the program's own signed protocol — the same violation the program correctly refused in EXP079's
   infeasible-probe closure. Shelving is protocol compliance, not timidity.
2. **The search pool is in the causally-dead room.** EXP068's G draws from bootstrap-resampled
   *contrast directions* — the v̂ family. EXP078 localized the bridge's causal power *outside* that
   subspace (e_median = 0.0544 < 0.10); five static families are flat; Sprint2's standing DOA ruling
   already killed "any new hidden-state candidate search before the ceiling is re-measured." A
   licensed EXP068 would spend ~93k passes searching a room five experiments say is empty.
   That is theory preservation by implementation weight — the exact failure mode the standing law
   names.
3. **The test phase is underpowered at the level that matters.** N=45 → L1 MDE 13.3pp, L2 MDE 20pp
   (B2 table) — both above 2·δ_min. Even a clean run could not license the mechanism verdicts the
   program needs; it could only produce Inconclusive cells dressed as a 13-hour result.
4. **EXP068 does not test the P1 bar.** Per adopted §D2 condition 4 (conditionality), a per-instance
   loop whose gain does not depend on its computed per-instance quantities is open-loop selection —
   steering with extra steps. EXP068's signed design tests conditions 1–3 of the novelty boundary
   partially, but not 4 (conditionality) or 5 (specificity). The D3 conditionality probe
   (re-run with E's measurements randomly permuted; Δ̂ = ΔM_loop − ΔM_permuted-E with exact 95% CI;
   U < δ_min → Not supported for L2) is the falsifier EXP068 needs — and it is a re-run arm, not a
   93k-pass build.
5. **EXP070's lesson cuts against the loop, not for waiting.** The oracle ceiling over the loop's
   own pool returned UNINFORMATIVE_PROBE — and the protocol's licensed reading is "the probe carried
   no transferable signal," explicitly NOT "EXP068 is cancelled." The program is in the worst
   epistemic cell: the loop is neither licensed nor dead, and the evidence that would move it is not
   being collected. Small nulls that *are* the collected evidence (K1/K2/K3/EXP080) are the right
   grind; the wrong grind would be more geometry variants.

**If the honest answer is that EXP068's gate will never license it — say so.** [INFERENCE]: the
gate *could* license it mechanically (a future probe could pass the ρ-gate), but the license would
be to search the dead room at N=45 with no conditionality probe. **The CEO should not run EXP068
as-signed even if the gate passed.** The replacement for the program's large bet, sequenced after
the K1–K3 battery, is one of:
- **(i) DPRS — the loop re-pointed at the output room** (E7): per-instance search in *readout
  space*, licensed only if EXP080's bin (ii) > 0 proves a selection prize exists beyond the bridge.
  This preserves the G/E/S/T formulation distinction (the program's only unvalidated novelty
  candidate) while moving it to the room where causality lives.
- **(ii) CLLC closed-loop controller pilot** (synthesis §E C1): the A-LQR-lineage bet — feedback
  control with tracking-error bounds, the 2026 field direction, untested by this program at any
  scale. Per-item cost ≈ 2F cached; the pilot is 1–2h on 160m with a pre-registered
  faithful-but-inert kill cell. This is the mechanism-family change P1/P2 contemplate.
- **(iii) Nothing** — if K1 confirms tilt and EXP080's bin (ii) = 0, the honest large bet is the
  boundary paper plus the mechanistic account of *why* Δθ=0 temporary computation cannot add
  capability here. That is the §H license executing, not surrender.

The small-experiment habit is theory preservation **only when small runs avoid the mechanism's
throat**. K1/K2/K3/EXP080 are aimed at the throat (the bridge's mechanism, the evaluator's prize,
the loop's adaptivity). More unconditional geometry variants would be the habit at its worst —
and they are shelved below.

## B5. Shelve list (with reasons — the Friday-cull discipline, in writing)

| Shelved | Reason |
|---|---|
| EXP068 as-signed (~93k passes) | Gate unlicensed; pool in causally-dead room (EXP078); N=45 underpowered (L1 MDE 13.3pp); no conditionality probe. Re-point (DPRS) or replace (CLLC), never run as-is. |
| Unconditional static-geometry variants (Sprint Ideas 5/6/7-class; EXP077 rooms) | Five dead rooms; the kill licenses are narrow but the *pattern* (flat ΔM across radial/angular/affine) is five-fold. Gated variants survive — they belong to the adaptivity tournament (Sprint New Idea 5), not to more static runs. |
| Centred-basis *injection* (Sprint Idea 5 / EXP073-class) | Not run — but sequenced BEHIND the $0 anisotropy analysis (B3.7). If the 0.7 collapses under centring, the run is stood down; if it survives, the run is licensed as an adversarial re-test of our own null. |
| Any new hidden-state candidate search/selection | Standing DOA ruling (Sprint2 kill list, item 2) — in force until a ceiling is re-measured (EXP080) or the pool moves rooms (DPRS). |
| Margin-shift/confidence endpoints or unvalidated evaluator objectives | Killed (Law #9; B_wrong p=1.2e-08 with b=c=0). Decision changes only; any future evaluator pre-registers a confidence-oracle control. |
| Label-informed bridge presented as a method | Killed as a proposal class (Law #7); positive control / ceiling probe only. |
| Naive self-critique loops; "online optimization" or "adaptive steering" as novelty claims | Killed by the 2026 literature (AVI; ∇-Reasoner; SVF+STARS) — residual claims are strictly the target-free, gradient-free, activation-space variants (Sprint2 kill list, items 5–7). |
| 7B+ scaling of current designs | Cut on resources (Sprint cut list) — revisit only with a mechanism that survives K1–K3 at 410m. |

---

# (c) SEQUENCING TABLE

Throughput basis: ~22 fwd/s on pythia-410m, 2×T4 [OBSERVATION]. T4-hours are wall estimates
[ILLUSTRATIVE] (math charter M3.1) with derivations shown. MDE per B2 (exact McNemar, c=0).
"N/A" pilot gates are marked honestly. Runs are ordered by logical priority (K1 first —
$0 and logically prior), not by GPU convenience.

| # | Run | Forward passes | Est. T4-hours | Pilot gate (what must show before the full run) | MDE at planned N (L1 / L2) | Verdict |
|---|---|---|---|---|---|---|
| 1 | **K1** — readout-tilt falsification (cos≥0.9 bar; flip analysis; label-shuffle) | 0 (CPU re-analysis of archived EXP065/066/077 artifacts) | 0 | None — it IS the $0 screen | N/A (diagnostic; verdicts per §G1b CI+δ_min) | **RUN NOW** |
| 2 | Anisotropy + template-contamination analyses (raw vs centred cosines vs 1/√d; rotated wording) | 0 (CPU; archived activations/vectors) | 0 | None — P3-style boundary hygiene | N/A | **RUN NOW** (parallel with K1) |
| 3 | **EXP080** — G2 oracle ceiling, Phase A (PRE-REGISTERED, LOG-172) | 1,320 (300 rebuild + 600 + 420; verified) | ~0.02 | None — it IS the evaluator gate. Blocked on LOG-197 verdict + CEO GPU clearance (adopted gate). | N=60: 10.0pp / 15.0pp. L1 at the 2·δ_min boundary; L2 held. | **RUN** (first GPU run after the audit lands) |
| 4 | **K2** — bypass-vs-routing discriminator (60 items × 3 positions) | ~180 | ~0.005 | None — the pilot IS the experiment. Preparation parallel; *interpretation* waits on K1 (binding ordering). | N=60: 10.0pp / 15.0pp (diagnostic CI rule, not a Supported-machine) | **RUN** (prep now, interpret post-K1) |
| 5 | **K3** — Law-#7-compliant bridge build + test | ~0 build (weight rows, CPU) + ~400 test [ESTIMATE] | ~0.02 | CPU construction audit passes (no option-token inputs) AND K1 did not confirm tilt. If K1 confirms tilt → does not run. | N=60: 10.0pp / 15.0pp | **RUN conditionally** (prep now) |
| 6 | **EXP081** — C-A donor transfer v2 (PRE-REGISTERED, LOG-182) | 660 | ~0.01 | $0 pre-audit attached (done: g(C3)=1.061783, 49/11 strata, 23 headroom). Blocked on LOG-197 verdict + CEO GPU clearance. | N=60: 10.0pp / 15.0pp. L1 boundary; L2 held. | **WAIT** (post-audit; second GPU run) |
| 7 | **CLLC pilot** — closed-loop controller, pythia-160m (replacement big-bet candidate) | ~600–1,000 (60 items × (6 cond + Jacobians ≈2–3F)) [ESTIMATE] | ~1–2 | 160m pilot must show: κ ≤ κ_max; tracking error within bound's order; ΔM>0 with L>δ_min vs open-loop same-correction control. Failure on (i)/(ii) kills the 410m run. | N=60: 10.0pp / 15.0pp (L1 adjudication only) | **PILOT** (after K2's routing verdict; the A-LQR bound-check is its own gate) |
| 8 | **EXP068** as-signed — per-instance G/E/S/T loop | ~93,000 worst case (≈13h at 0.5 s/pass on 160m); ~11,025/arm at defaults | ~13 worst / ~1.5 expected fraction | ρ-gate + §4b transfer probe + headroom (ALL UNMET). Even if met: pool in dead room; N=45 underpowered; no conditionality probe. | N=45: 13.3pp / 20.0pp — **held at both levels** | **SHELVE** — do not run as-signed; re-point (DPRS, needs EXP080 bin(ii)>0) or replace (CLLC) |
| 9 | Re-registered N≥100 L2-adjudicating run (any mechanism surviving K1–K3 + EXP081) | ~1,000–2,000 (N=100 × ~10–20 conditions) [ESTIMATE] | ~0.02–0.03 | Surviving mechanism with L1 Supported + Law #14-signed re-registration with its own MDE computation (B2: N=100 → L2 MDE 9.0pp < 2·δ_min). | N=100: 6.0pp / 9.0pp — **L2 clears** | **RESERVE** — not designed until the battery rules; budget held, not spent |
| — | **Budget reserve** | — | **~22h held** | Released only by: (a) K1–K3 battery verdicts, (b) EXP080/081 rulings, (c) CLLC pilot outcome, or (d) an L2-licensed re-registration. | — | **HOLD** |

**Ledger check (track 6):** 0 + 0 + 0.02 + 0.005 + 0.02 + 0.01 + ~1.5 + 0 + 0 ≈ **~1.6h worst case**
for the full licensed falsification sequence — 6% of the 25h budget. The remaining ~23h is not
"idle": it is the powered follow-through (row 9, CLLC 410m, DPRS build, boundary replication)
that only verdicts can license. Spending it before K1 rules would be buying answers to questions
the program has already decided to ask in order.

**Shelving is not burial (Law #8):** every shelved item above keeps its kill criterion on file;
a shelved item is resurrected only by new evidence meeting its own pre-registered bar — never by
impatience, and never under its old number if the design changed (Law #4).

---

## Closing — the honest headline (track 5 × track 6)

**[INFERENCE]**/[INTERPRETATION]: the paradigm is a local minimum for discovery and fertile ground
for boundary science — both verdicts stand, and the compute strategy follows the split. The next
1–2 experiments that matter are not the ones that spend the most GPU: they are K1 ($0 — does the
bridge survive its own falsification?), K2 (180 passes — does the rescue route through computation
or bypass it?), and EXP080 (1,320 passes — does the output room contain a selection prize beyond
the bridge?). If those three go against the program, the honest move is the pivot the criteria name —
closed-loop control, a new substrate, or the boundary paper — not a sixth static-geometry room.
If they go for the program, the re-pointed loop (DPRS) or the controller pilot (CLLC) becomes the
large bet with a powered N≥100 re-registration behind it. Either way, the 25 hours are enough —
because the questions that decide the program's direction cost almost nothing to ask.

*End of deliverable. No GPU used. No experiments run. No new experiment numbers minted.
No signed protocol, primary artifact, or LOG-197 chain material modified. Δθ=0 throughout.*

---
## STANDING CORRECTION — the adopted (b) reading (LOG-212, 2026-09-23)

The (b) flip-analysis reading stated in this document ("f ≥ r/2 strengthens a
tilt verdict") is the ADOPTED §H6 mapping, kept verbatim in K1 REV1 per Law #4
(no silent hypothesis shifts). **It is recorded as backwards vs the program's
own L1 license** (LOG-206 §2, CEO ruling LOG-212): L1 proves a pure readout tilt
strictly increases the t−f margin, hence predicts f = 0 exactly — the archived
f = 0, r > 0 pattern is tilt-*confirming* under the license. **No future tilt
verdict may lean on the adopted (b) reading until it is re-registered**
(recommended alignment: f ≥ r/2 contradicts a *clean* tilt; f = 0 is the
tilt-predicted pattern). This note amends the reading prospectively; the
documents historical description of K1's adopted battery is unchanged.
