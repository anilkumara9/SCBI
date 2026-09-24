# AMBITION SPRINT — Experiment-Design Specialist Deliverable (LOG-250)

*2026-09-24. CPU only, $0. No weights touched. No signed artifacts edited.
This is a design document, not a protocol: nothing here is licensed to execute
until it passes Law #14 review and signed pre-registration.*

**Law #15 Q4 (stated honestly):** this deliverable answers Q4 as n/a — design
work only; no GPU spent, no weights touched, no signed files edited. The Law #15
packets inside are templates for future pre-registrations, not licenses.

**Epistemic labels** follow the repo standard ([FACT], [DEFINITION],
[HYPOTHESIS], [CONJECTURE], [ASSUMPTION], [OBSERVATION], [INTERPRETATION],
[OPEN]). All cost numbers derived from program-measured anchors are [FACT];
extrapolations are marked [CONJECTURE]/[ESTIMATE].

---

## PART A — THE CHEAP-KILL TOOLKIT

### A.1 Pass-count model (program-measured anchors)

[FACT] Measured anchor (K2 plan LOG-223 REV4 §3.4, "Law #15 Q3"): **22 forward
passes/second on the Kaggle 2×T4 node** for Pythia-410m, layer-20 injection,
single-token readout, short prompts. Hence:

| Passes (410m) | Wall time | T4-h (node-hour convention) |
|---|---|---|
| 1 | 0.0455 s | 1.26e-5 |
| 60 | 2.7 s | 0.00076 |
| 90 | 4.1 s | 0.0011 |
| 120 | 5.5 s | 0.0015 |
| 144 | 6.5 s | 0.0018 |
| 150 | 6.8 s | 0.0019 |
| 180 | 8.2 s | 0.0023 (≈0.002 as booked) |
| 360 | 16.4 s | 0.0046 (≈0.005 as booked) |

Formula: `T4-h ≈ passes / 79200` at 410m. [DEFINITION] "T4-h" here = node-hour
on the Kaggle 2×T4 session (the program's booking convention), not per-GPU-hour.

[CONJECTURE/ESTIMATE] Pythia-160m throughput: no program measurement on record.
FLOP-ratio extrapolation 410/160 ≈ 2.56 → **≈56 fwd/s (ESTIMATE)**, 1 pass ≈
0.0179 s, `T4-h ≈ passes / 201600`. **Rule:** the smoke test (mandatory, §A.2)
must time ≥20 warmup passes on the actual node and recalibrate this row before
any 160m booking is finalized; if measured throughput is <40 fwd/s, the pass
budget is cut, never the time budget extended.

Budget tiers (standing, consistent with the Law #15 Q2 order of battle):
- **Kill pilot: 60–150 passes** (≈0.0008–0.0019 T4-h @410m). Fits inside a
  single Kaggle session's noise floor. This is the only tier this document
  designs for.
- **Attribution/scale pilot: ≤660 passes** (≈0.008 T4-h) — needs a CONTINUE
  verdict from a kill pilot plus CEO GPU clearance.
- **Powered licensing run: ≤1,320 passes** (≈0.017 T4-h) — needs Law #14 review
  of the kill-pilot report plus a pre-registered power analysis.
- **Hard ceiling:** nothing above 1,320 passes without a fresh Law #15 packet
  and explicit CEO clearance. EXP068-as-signed (~93k passes) stays shelved.

Wall-clock honesty: pass time is not session time. Every booking adds the
startup smoke test (~3–8 min incl. three-crash history buffer) and per-arm
archiving overhead; the runner must log `t_start/t_end` per arm so the next
iteration's model improves. The budget is passes, not hours — but the session
must never be booked on pass math alone.

### A.2 Kill-pilot template (60–150 passes)

Every kill pilot is built from this skeleton. Deviations are recorded as
F-series findings (K2 precedent: F1–F4), never silently absorbed.

1. **Probe set:** the pinned 60-item EXP077-derived set where licensed; kill
   pilots may use a fixed 24- or 30-item stratified subset (seed-pinned) when
   the kill criterion is a gross-miss bar — the subset index list is part of
   the pre-registration. Subsetting is a *weakening* of the kill (a miss at
   N=30 is less decisive than at N=60); the verdict ladder in §A.4 prices this.
2. **Baseline arm: $0.** Reuse archived smoke/baseline records where the
   protocol licenses it (K2 precedent: "baseline correctness from archived
   smoke records — no re-baselining passes"). Re-baselining spends passes to
   re-learn a known number; it is banned unless the archive's tokenizer or
   prompt builder changed.
3. **Arms:** 2–4 arms including the mandatory negative-control battery (§A.3).
   Typical shape: 30 items × 3–4 arms = 90–120 passes.
4. **Determinism:** seeds pinned (torch + numpy, K2 used 20260923-style dated
   seeds); greedy decoding; environment manifest logged; parameter hash before
   and after inference (Law #13).
5. **Startup smoke test (mandatory):** ≤12 passes on 3 items covering every
   arm once, asserting (i) the runner reaches the verdict code path, (ii) the
   identity arm reproduces the archived baseline bit-for-bit, (iii) throughput
   ≥80% of the booked model. Three Kaggle startup crashes burned quota — the
   smoke gate is a Law, not a suggestion. Smoke passes count toward the 150
   ceiling.
6. **Evaluator discipline:** the evaluator ships with its own test suite
   (K2: 84/84; EXP070: 18/18), CPU-only, seeded, deterministic, stdlib-only
   where possible. Minimum required test groups: CI-math correctness (Tango
   two-sided + one-sided reproduction of the canonical table, §A.4), verdict
   table firing on synthetic worlds (all rows), guard behavior (exclusion
   floors), seed determinism. The suite runs on CPU before the bundle leaves
   the lab.
7. **Manifest:** protocol path + sha256, file hashes, seeds, tokenizer revision
   (warn-only reference, K2 R6 precedent), pass budget, arm definitions.
   `manifest.json` excluded from its own hash (self-reference).

### A.3 Mandatory negative-control battery

Every kill pilot carries ALL of the following unless the pre-registration
argues a specific exemption past Law #14. The battery exists because every
killed family in program history died to one of these:

1. **Label-free arms (Law #7).** No target/foil strings, no correctness
   labels, no benchmark metadata may touch any candidate direction, selection
   rule, or scoring function. The label-informed bridge is **disqualified as a
   mechanism arm** (LOG-204 demotion; Law #7 audit LOG-197). Its sole licensed
   role is the *apparatus-sensitivity check*: "can this runner detect a causal
   effect at all" (EXP070 LOG-110 license). A pilot that needs the bridge to
   show a mechanism effect has no mechanism result.
2. **Information-destroyed controls.** For every directional intervention at
   norm ρ: (a) isotropic Gaussian noise at norm ρ (destroys direction, keeps
   norm); (b) sign-flipped direction (tests directionality vs magnitude);
   (c) the same vector with positions shuffled across the sequence (destroys
   positional information). If the candidate ≡ all three, the effect is a
   norm/energy artifact, not a mechanism.
3. **Permuted/shuffled controls.** The intervention vector (or selection score)
   computed for item *i* is applied to item *j≠i* (fixed derangement,
   seed-pinned). Survival of the effect under permutation = the intervention
   carries no item-specific information → KILL the information-carrying claim.
4. **Identity/appendix arms ($0 or near-$0).** The α=0 / empty-intervention arm
   must reproduce the archived baseline exactly — this is the apparatus check,
   not science. Failure here invalidates the session, not the hypothesis.
5. **Wrong-answer quarantine.** Any arm whose construction requires knowing
   which option is correct is a *rescue control*, reported separately, never
   contrasted as a mechanism arm. The verdict table must be computable with
   all such arms deleted.

### A.4 Pre-registration skeleton + decision tree

```
0. Law #15 packet (Q1 precise question; Q2 decision named KILL/CONTINUE/PIVOT;
   Q3 cheapest-why with exact pass count; Q4 math license: theorem → prediction
   → breaking point)
1. Arms, pass budget, probe subset, seeds, baseline license
2. Negative-control battery mapping (§A.3: which arm serves which control)
3. Endpoints: PRIMARY = discrete ΔM (McNemar exact + Tango CIs). SECONDARY =
   margins (Wilcoxon signed-rank / sign test) ONLY where licensed by precedent
   (S3-8, K1). Law #9 (EXP081 F-199-2): margins are never decision endpoints
   where the program has banned them — the skeleton marks the license explicitly.
4. DECISION TREE (all thresholds numeric, all branches named):
   - KILL_gross: candidate arm ≡ null arm AND the two-sided 95% CI for the
     candidate−null contrast excludes the mechanism's own claimed minimum
     effect δ_claim (the proponent's number, not ours). A theory that predicts
     +0.15 and measures a CI of [−0.02, +0.03] is dead — no second pilot.
   - KILL_flat: on the canonical flatness bar — one-sided 95% Tango upper
     U_1s(Δ̂M) < 0.05 fires ONLY at s=0 discordant pairs for N=60
     (canonical table: N=60 s=0 → 0.043147 FIRES; b=c=1 → 0.056902 FAILS;
     b=c=2 → 0.067926 FAILS; N=54 s=0 → 0.047712 FIRES). A flat pilot at N<60
     cannot fire the 0.05 bar (rule-of-three floor ≈ 3/N); it lands in HELD.
   - HELD (Inconclusive): CI straddles δ_claim, or the pilot shows sub-claim
     signal, or N was subset-reduced. HELD never upgrades to CONTINUE. The
     report prices the powered follow-up (pass count + power analysis) and
     returns the candidate to the queue. No zombie workstreams (Law #15).
   - CONTINUE: licensed ONLY as "CONTINUE to a powered pilot," never as a
     capability claim. Requires: directional bar cleared (lower 95% CI > 0 on
     the primary discrete endpoint, or pre-registered one-sided p ≤ 0.05 with
     the MDE anchor documented) AND the negative-control battery flat AND a
     pre-registered power analysis for the next stage (N for δ_min=0.05 at 80%
     power; program MDE anchor: b=6,c=0 → p=0.03125 at N=60).
   - PIVOT: the pilot kills the stated mechanism but the data license a
     neighboring question (pre-registered pivot list, max 2; anything else is
     a new Law #15 packet).
5. Guards (G-series): exclusion floors, tokenizer-drift warn, pass-budget
   hard stop (runner refuses pass N+1), determinism re-check.
6. Law #14 review slot: reviewer signs the *skeleton* before the runner is built.
```

**The power-gate clause (standing):** a ≤150-pass pilot has no license to
produce a positive capability verdict — the September power-gate lesson (N=80,
Level-2 99.375% CIs holding candidates Inconclusive) binds here. Pilots are
asymmetric instruments: they can KILL (falsification is cheap) or HOLD; only
powered, pre-registered stages can CONTINUE toward a claim. Any document that
lets a pilot "suggest promise" as a verdict has failed Law #9.

### A.5 Killed-family antibodies (checklist per design)

Each Part-B design states, in one line per family, why its positive signal —
if observed — cannot be the already-killed thing:

- *Static direction injection (0.0pp):* the design's decisive contrast must be
  *conditional* (curvature/adaptivity/composition-dependent), never a raw
  directional ΔM. Any arm reducible to "add vector v" is disqualified at design.
- *QK-null-space mechanism:* no QK/OV-projection-energy claim may appear in the
  math license (G1 killed the central sentence; boundary claim I1 survives only
  on endpoints).
- *Procrustes alignment:* no cross-space fitted map in the pipeline; any
  alignment operator must be derived label-free or not exist.
- *Label-informed bridge:* §A.3 item 1 + 5. The bridge appears at most once per
  program, as the apparatus check.
- *Persistent readout tilt:* K1 exonerated tilt (0/180 reached the 0.9 bar);
  any design whose positive arm requires persistent tilt across items must
  re-derive the license from scratch — "tilt" is a dead word until then.

---

## PART B — KILL-FIRST DESIGNS BY MECHANISM CLASS

Common parameters: Pythia-410m/layer 20 unless noted; 30-item seed-pinned
stratified subset (kill pilots; §A.2.1); baseline from archived smoke records
($0); costs via §A.1 (T4-h ≈ passes/79200 @410m). Every design carries its Law
#15 Q1–Q4 inline (Q4 for the *design document* is n/a; the Q4 shown is the
candidate's math license for its future packet).

---

### B.1 Feedback-controller mechanisms

**Law #15.**
- Q1: Does a closed-loop controller (intermediate-margin readout → corrective
  injection, 3 steps, fixed total norm budget R) beat the best open-loop
  injection designed from the S3-9 affine fit on the same budget?
- Q2: KILL the feedback-controller claim for this budget class if the loop adds
  nothing beyond the curvature envelope; CONTINUE to a powered N=80 pilot only
  if the loop clears the envelope.
- Q3 (cheapest): 144 passes. Per item (N=24): 2 curvature probes (±h central
  difference along the planned correction direction → κ̂ per item), 1
  open-loop arm (affine-designed ū), 3 closed-loop steps. 24×6 = 144 passes ≈
  6.5 s ≈ **0.0018 T4-h**. Everything else (affine fit, κ̂ arithmetic, verdict)
  is CPU/$0. N=24 (not 30) because the kill criterion is margin-based
  (Wilcoxon), where N=24 has licensed precedent in the program's margin
  analyses, and the curvature probes dominate the budget.
- Q4 (math license): **[THEOREM]** P1 bound (LOG-248): for the practical
  feedback-vs-open-loop gap δ, 0 ≤ δ ≤ 2ε (affine-model error) and
  δ ≤ κR² under κ-bounded Hessian. **[ASSUMPTION]** A3 = LOG-246 F2: the frozen
  plant is deterministic, so a controller with a perfect internal model ≡
  open-loop exactly — feedback's only licit gain is exploiting curvature /
  model error. **Prediction:** closed-loop gain G_fb − G_ob ≤ κ̂R² (measured
  per item, same budget set). **Breaking point:** observed
  G_fb − G_ob > κ̂R² upper bound, pre-registered.

**Arms.** (a) Open-loop: ū from the archived S3-9 affine fit (1 pass).
(b) Closed-loop: 3 correction steps, each re-reading the label-free top-2
margin proxy and stepping within the remaining budget (3 passes). (c) Curvature
probes: ±h along the step-1 direction (2 passes). Controls: permuted-step
control (apply item *i*'s step-1 correction to item *j*, §A.3.3); the
controller's readout is the model's own top-2 margin — no targets anywhere
(§A.3.1).

**KILL (numeric, pre-registered):** one-sided Wilcoxon (H₁: fb > ob) on per-item
margin gains p ≥ 0.20 **and** the two-sided 95% CI for median(G_fb − G_ob) lies
entirely below the per-item κ̂R² envelope → the loop is model-error
exploitation inside the proven bound, not a new capability. **KILL the class
for this budget.**

**CONTINUE:** lower 95% CI of median(G_fb − G_ob) exceeds the κ̂R² envelope
upper bound → genuine feedback signal beyond curvature → license the powered
N=80 pilot with the envelope as the null.

**Antibodies:** the contrast is fb−ob *conditional on the curvature envelope* —
a raw directional gain would be the killed static-injection story; the envelope
makes it a different question. No QK claims. No labels in the loop.

---

### B.2 Ephemeral memory / workspace mechanisms (H2-flavored)

**Law #15.**
- Q1: Does a writable scratch state persisting across forward passes within
  one inference enable *accumulating* computation — i.e., does a 2-step
  write→read→refine→read workspace beat a 1-step write→read workspace?
- Q2: KILL the workspace-accumulation claim if 2-step ≡ 1-step; CONTINUE to a
  powered pilot only if refinement separates with the shuffled-content control
  flat.
- Q3 (cheapest): 120 passes. Per item (N=30): arm A 1-step workspace (1 pass),
  arm B 2-step workspace (2 passes), arm C shuffled-content workspace
  (information-destroyed, 1 pass). 30×4 = 120 ≈ 5.5 s ≈ **0.0015 T4-h**.
  Baseline $0 (archived).
- Q4 (math license): **[PROPOSITION]** A workspace with W writable bits across
  T passes implements at most T rounds of inter-pass communication; the
  capacity gain over a single pass is bounded by the mutual information the
  passes share through W. **Prediction:** if refinement carries no usable
  signal, B ≡ A on decisions and margins (the workspace is a prompt-shaped
  distractor). **Breaking point:** one-sided sign/Wilcoxon separation B > A
  with C flat.

**Arms.** (a) A: single write of the question-derived scratch vector, read at
decision. (b) B: write → read → refine-write → read. (c) C: workspace seeded
with a deranged other-item's scratch content (information-destroyed, §A.3.2/3).
The scratch vector is derived from the question text only — never from
options/targets (§A.3.1).

**KILL (numeric):** two-sided Wilcoxon B−A on margins p > 0.10 with |median
diff| < 0.01 margin units **and** C ≡ A (p > 0.10) → no accumulation, no
content-sensitivity → **KILL the H2 accumulation claim** (the workspace is
decorative).

**CONTINUE:** one-sided Wilcoxon B > A p ≤ 0.05 **and** C flat vs baseline
(|Δ̂M_C| with U_1s < 0.05) → genuine refinement signal → license powered pilot
with a capacity-ablation arm (vary W).

**Antibodies:** B−A is a *conditional* contrast (refinement given the same
write); a raw A−baseline gain alone would be static-prompting territory and is
not verdict-bearing. Permuted-write control kills the "lucky content" story.

---

### B.3 Adaptive routing mechanisms (H4-flavored)

**Law #15.**
- Q1: Does per-item adaptive choice of the intervention site (layer ∈
  {16,20,24}, chosen by a label-free score) beat the best fixed site (layer 20)?
- Q2: KILL the adaptive-routing claim if adaptive ≡ fixed ≡ random-site;
  CONTINUE only if adaptive beats fixed on the discrete endpoint.
- Q3 (cheapest): 120 passes. Per item (N=30): fixed arm (1 pass), adaptive arm
  (1 scoring pass reusing the forward cache + 1 intervention pass = 2), null
  arm (random site, same budget, 1 pass). 30×4 = 120 ≈ **0.0015 T4-h**.
- Q4 (math license): **[PROPOSITION]** Adaptive selection from K sites with a
  label-free score s(x) beats fixed-site only if s(x) correlates with
  per-item amenability a(x); the oracle (hindsight best-site) gap is the
  ceiling, and a label-free rule must capture a positive fraction of it.
  **Prediction:** with an uninformative score, adaptive ≡ fixed (the choice is
  noise). **Breaking point:** McNemar exact on adaptive−fixed discordant pairs,
  one-sided p ≤ 0.05 in the adaptive direction.

**Arms.** (a) Fixed: layer-20 injection (the program's standard pin).
(b) Adaptive: score = per-layer residual-norm concentration at the candidate
layers from the scoring pass (content-blind, label-free); inject at argmax.
(c) Null: uniform-random site ∈ {16,20,24} (seed-pinned). Direction: the
label-free top-PC output direction (§B.4's D) or pure norm-matched noise — the
routing question is about the *site choice*, so the injected content is held
fixed and label-free across arms.

**KILL (numeric):** McNemar adaptive-vs-fixed one-sided p > 0.20 **and**
adaptive ≡ null (two-sided p > 0.20) → the score is uninformative, adaptivity
is vacuous → **KILL the H4 routing claim** for this score family. (A different
score family is a new Law #15 packet, not a rescue.)

**CONTINUE:** McNemar one-sided p ≤ 0.05 adaptive > fixed **and** the adaptive
gain is a positive fraction of the oracle gap (computed CPU-free from the same
passes: oracle = best of the three sites per item — note this uses no labels,
only the arms' own outcomes) → license the powered pilot.

**Antibodies:** the score never sees labels (or the arm is disqualified, not
merely penalized). The oracle gap is reported as a ceiling, never as an arm.

---

### B.4 Output-side / readout mechanisms

**Law #15.**
- Q1: Is there a *label-free* output-side perturbation that moves decisions
  beyond what scalar rescaling and isotropic noise explain? (The only known
  output-side transferable direction is label-derived and demoted — this asks
  whether the output side holds anything lawful at all.)
- Q2: KILL the label-free output-direction claim if the PC direction ≡
  rescale ≡ noise; CONTINUE only if the direction beats both with directionality
  (sign-flip separation).
- Q3 (cheapest): 120 passes. Per item (N=30): arm S scalar rescale ×1.1 of the
  final residual (1 pass); arm D top-PC direction injection at matched norm
  (1 pass); arm N isotropic Gaussian noise at matched norm (1 pass); arm D2
  sign-flipped PC (directionality, 1 pass). 30×4 = 120 ≈ **0.0015 T4-h**. The
  PC is fit once on CPU from archived final-residuals across *all* probe items
  (no correctness labels — pure distributional direction, $0).
- Q4 (math license): **[THEOREM]** The unembedding is linear; any output-side
  directional effect on the (t−f) logit margin beyond scalar rescaling must
  come from the direction's alignment with the readout. **[OBSERVATION]** S3-8:
  downstream gain ×1.8 exists for a label-derived direction — the class
  question is whether any of that structure is reachable label-free.
  **Prediction:** if the output side's lawful structure is entirely
  label-derived, D ≡ S ≡ N. **Breaking point:** D > S and D > N with D ≠ D2.

**KILL (numeric):** two-sided Wilcoxon D−S p > 0.10 **and** D−N p > 0.10 →
the label-free output direction carries nothing beyond scale/noise → **KILL**.
(The ×1.8 amplification stays attributed to the label-derived rescue control;
the readout-mechanism class for autonomous steering is closed.)

**CONTINUE:** one-sided Wilcoxon D > S and D > N both p ≤ 0.05 **and**
two-sided D−D2 p ≤ 0.05 (genuine directionality, not norm) → license a powered
pilot with the PC refit on a disjoint calibration split (no leakage).

**Antibodies:** the direction is fit with zero correctness labels — Law #7
satisfied by construction. The demoted bridge appears nowhere in this design.

---

### B.5 Frozen-circuit composition mechanisms

**Law #15.**
- Q1: Does rewiring frozen subcircuits at inference time — patching a layer-10
  attention-block output into the layer-20 residual stream — create computation
  detectable beyond a content-free patch of the same norm?
- Q2: KILL the composition claim for this site pair if patch ≡ null-patch ≡
  sign-flip; CONTINUE to a site-pair scan only on content-specific separation.
- Q3 (cheapest): 90 passes. Per item (N=30): arm P compositional patch
  (1 pass), arm N shuffled-position same-norm patch (information-destroyed,
  1 pass), arm Z sign-flipped patch (directionality, 1 pass). 30×3 = 90 ≈
  4.1 s ≈ **0.0011 T4-h** — the cheapest class pilot in Part B.
- Q4 (math license): **[PROPOSITION]** A cross-site patch is a
  rank-constrained additive intervention; if downstream readout cannot
  distinguish the patched content from a null patch, the "composition" is
  additive noise by operational definition. **Prediction:** P ≡ N unless the
  patched signal is specifically read out downstream. **Breaking point:**
  one-sided Wilcoxon P > N on margins, p ≤ 0.05, with P ≠ Z.

**KILL (numeric):** two-sided Wilcoxon P−N p > 0.10 **and** P−Z p > 0.10 →
patch content irrelevant → **KILL the composition claim for the L10→L20 pair**.
(The class dies one site-pair at a time; the next pair is a new packet, and
the third consecutive pair-kill retires the class for the quarter.)

**CONTINUE:** one-sided P > N p ≤ 0.05 **and** two-sided P−Z p ≤ 0.05 →
content-specific composition signal → license the powered site-pair scan
(pre-registered pair list, ≤660 passes).

**Antibodies:** no QK/OV energy claims (G1). No fitted cross-space map
(Procrustes). The patched content is the model's own activation — no labels.

---

## PART C — PROPONENT'S OWN CANDIDATES (each with a full Law #15 packet)

*Lens applied: the cheapest decisive tests reveal the best ideas. Both
candidates below are designed so that their most likely failure mode costs
under 150 passes to observe.*

---

### X1 — Residual recurrence (fixed-point iteration through the frozen backbone)

**The idea.** Run the forward pass; add a scaled copy of the final residual
stream back onto the input embeddings; run again:
x_{k+1} = E + α·r(x_k), θ frozen, α a single label-free scalar. If the
backbone's input→residual map has an attracting fixed point near a better
decision region, iteration is inference-time computation no single pass can
do. If it doesn't, the mechanism kills itself — that self-killing property is
what makes it the cheapest idea in this document.

**Law #15 packet.**
- **Q1 (precise question):** Does 2-step residual recurrence (α = 0.1,
  label-free) change any decision or margin vs the single pass on the probe set?
- **Q2 (decision):** KILL the recurrence family if flat at step 2; CONTINUE
  to an iteration-count scan only on monotone margin improvement with
  contracting displacement. Decision flips without monotone gain = instability
  → PIVOT to instability characterization, never CONTINUE.
- **Q3 (cheapest-why):** 60 passes — 30 items × (1 baseline + 1 recurrence
  pass) = 60 ≈ 2.7 s ≈ **0.0008 T4-h**, the cheapest pilot in the program.
  α is chosen by a $0 CPU contraction diagnostic on archived residuals
  (estimate the local Lipschitz constant of E ↦ r(E) by finite differences on
  archived activations — no GPU). No re-baselining; baseline from archived
  smoke records.
- **Q4 (math license):** **[THEOREM]** (Banach, contraction branch) If
  Φ(x) = E + α·r(x) is a contraction (Lipschitz L < 1) on the trajectory, there
  is a unique fixed point and iteration converges into its basin — prediction:
  step-2 ≡ step-1 on decisions, margins contract → the mechanism is
  *self-killing by its own math*. **[PROPOSITION]** (non-contraction branch) If
  L ≥ 1, iteration may diverge or enter 2-cycles — prediction: unbounded
  displacement or oscillation → kills the "stable capability gain" claim.
  **Breaking point (the only surviving branch):** monotone margin gain with
  ‖x_{k+1} − x_k‖ strictly decreasing — pre-registered as one-sided Wilcoxon
  (recurrence vs single) p ≤ 0.05 AND median displacement contraction ratio
  < 0.9. Every other outcome is KILL or PIVOT-to-instability.

**Arms (60 passes):** (a) baseline, archived ($0). (b) recurrence step-1→2
(1 pass; the step-1 forward is the baseline pass's cache — the runner reuses
it, so only the second pass is new). Controls: α = 0 arm (identity — must
reproduce baseline bit-for-bit, apparatus check, 0 extra passes via cache
validation); sign-flipped α = −0.1 (directionality); shuffled-residual
recurrence (add item *j*'s residual to item *i* — information-destroyed).
The control arms reuse the same 30 items; total stays ≤ 150 passes even with
all controls live (30×4 = 120 worst case ≈ 0.0015 T4-h).

**KILL (numeric, pre-registered):** McNemar b = c = 0 on decisions **and**
two-sided Wilcoxon on margins p ≥ 0.10 **and** max displacement bounded by the
CPU-predicted contraction envelope → **KILL the recurrence family**
(the backbone's map is a contraction or a no-op on this task — either way,
iteration buys nothing).

**CONTINUE:** one-sided Wilcoxon p ≤ 0.05 with positive median margin gain
**and** contraction ratio < 0.9 → license the 5-step scan at N=60 (300 passes,
≈0.0038 T4-h) with a divergence guard (hard stop if displacement grows).

**Why this is the best cheap idea:** the kill condition is the *likely*
outcome under both branches of its own math — the experiment is priced at the
cost of confirming what the theorem already suspects, and the surviving branch
(monotone gain + contraction) is exactly the signature no killed family can
fake (static injection can't produce step-2 ≠ step-1; tilt can't produce
contraction).

---

### X2 — One Newton step vs one gradient step at equal L2 budget (second-order feedback duel)

**The idea.** At the injection site, take one optimizer-style activation
correction maximizing the label-free top-2 margin proxy: a gradient step vs a
Newton step (−Ĥ⁻¹g, Hessian-vector product via central finite differences).
If curvature carries usable signal beyond the gradient, Newton wins at equal
norm budget — the cheapest possible win for the entire second-order feedback
family. If Newton ≡ GD, the family loses its flagship argument at the door:
five Newton steps will never be cheaper than five GD steps, so there is no
point pricing them.

**Law #15 packet.**
- **Q1 (precise question):** Does a single Newton correction beat a single
  gradient correction (equal L2 norm, same site, label-free margin-proxy
  objective) on per-item margins?
- **Q2 (decision):** KILL the second-order feedback family if Newton ≡ GD;
  CONTINUE to a curvature-spectrum study only if Newton wins directionally.
- **Q3 (cheapest-why):** 120 passes — per item (N=24): 1 baseline + 1 GD step
  + 2 finite-difference probes (central difference along g for the Hv product)
  + 1 Newton step = 5 passes; 24×5 = 120 ≈ 5.5 s ≈ **0.0015 T4-h**. The
  pass-count asymmetry (Newton costs 3 passes to GD's 1) is deliberate: the
  contrast is per-step *quality* at equal norm, and the duel is designed so
  that Newton's extra cost is part of what must be justified.
- **Q4 (math license):** **[THEOREM]** For a quadratic objective, Newton
  converges in one step while GD needs O(κ(H)) steps (κ = Hessian condition
  number) — prediction: Newton's margin gain ≥ GD's, with the gap growing in
  the measured condition number. **[INTERPRETATION]** If Newton ≤ GD, the
  curvature is either too small to matter (the κR² regime of the P1 bound —
  second order is provably negligible) or too noisy to exploit (finite-difference
  Hv drowns in activation noise) — both kill the family's premise, and the
  experiment distinguishes which (the probes themselves estimate κ).
  **Breaking point:** one-sided Wilcoxon (Newton − GD) on margins, p ≤ 0.05
  for CONTINUE.

**Arms:** (a) GD step at norm ρ along the margin-proxy gradient (1 pass).
(b) Newton step at norm ρ using Ĥ⁻¹g from the two probes (3 passes incl.
probes). (c) Random-direction step at norm ρ (information-destroyed, 1 pass).
All directions/gradients from the model's own activations — no labels (§A.3.1).

**KILL (numeric, pre-registered):** median(ΔM_Newton − ΔM_GD) ≤ 0 (two-sided
Wilcoxon p ≥ 0.10, |median| < 0.01 margin units) → **KILL the second-order
family** — its flagship loses to first-order at equal budget; report includes
the measured κ to say *why* (too-flat vs too-noisy), which is the useful
negative result.

**CONTINUE:** one-sided Wilcoxon Newton > GD p ≤ 0.05 **and** Newton > random
(p ≤ 0.05, proving the win is curvature-specific, not step-noise) → license
the curvature-spectrum study (κ-stratified pilot, ≤660 passes).

**Why this is the second-best cheap idea:** it converts the program's standing
curvature bound (δ ≤ κR², LOG-248) from a defensive weapon into an offensive
one — either Newton wins and the bound's regime is shown to be exploitable, or
Newton loses and the bound is empirically confirmed as the ceiling. Both
outcomes move the program.

---

## APPENDIX — canonical numbers reused by all pilots

- Throughput: 22 fwd/s @410m (measured); ≈56 fwd/s @160m (ESTIMATE — smoke-test
  recalibration mandatory). T4-h ≈ passes/79200 (@410m).
- Flatness bar (one-sided 95% Tango upper U_1s < 0.05): N=60 s=0 → 0.043147
  FIRES; b=c=1 → 0.056902 FAILS; b=c=2 → 0.067926 FAILS; N=54 s=0 → 0.047712
  FIRES. (K2 canonical table, independently reproduced ×3.)
- L1 MDE anchor: b=6, c=0 → McNemar exact p = 0.03125 (N=60).
- δ_min = 0.05 (program standard for the discrete endpoint).
- Verdict asymmetry: pilots KILL or HOLD; only powered stages CONTINUE toward
  claims. "Suggestive" is not a verdict.

*End of deliverable. Next step per program law: Law #14 review of this document
as a design object, then CEO selection of which pilots to pre-register.*
