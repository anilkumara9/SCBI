# S6-2 — Multi-Layer Composition: Do Two Inert Interventions Compose Into Movement? — Pre-registration DRAFT v1 (UNSIGNED)

*Status: DRAFT v1 — UNSIGNED. NOT a protocol. NOT executable. No Law #14 review performed; no finding is closed. On paper only, $0 compute, CPU-only design. No signed protocol file was edited; this is a new unsigned file.*
*Licensing chain: LOG-4407 (EXP096 verdict: "no further static per-item L11 experiments licensed" — the bar S6-2 must clear by material difference) → LOG-4408 (innovation sprint: S6-2 ranked #2 — "S6-2 follows on S6-1's verdict") → LOG-4416 (EXP097 verdict: PIVOT (fragility) — the threshold account dead as a mechanism; the EXP095/096/097 three-experiment closure is fenced to* single-layer *static per-item injection; multi-layer compositions explicitly EXP097+ material).*
*All values below are from LOG-4407, LOG-4408, LOG-4416, the EXP094/EXP095/EXP096/EXP097 verdict reviews (`experiments/protocols/REVIEWS/`), the frozen execution archives, and EXP093's signed pre-reg (`experiments/protocols/EXP093_L11_CAUSAL_PREREG_SIGNED.md`) unless otherwise cited. No number is invented. Every statistic in §4.2 was recomputed by this lane from first principles ($0; no model executed, no weights touched).*
***No pilot is authorized by this draft.** Before any run: independent Law #14 review + SIGN (separate lane), repair if needed, independent delta re-verification, then CEO execution clearance. CPU-only design ($0); no GPU contact under any circumstance.*

---

## 0. Law #15 block (binding)

**Precise question [HYPOTHESIS].** Every binding verdict to date is single-layer: L11 static per-item injection is closed across the full battery (EXP094/095/096/097), and L20 static geometry is closed for the tested variants (EXP077 branch (c)). The scope fences explicitly kept multi-layer compositions alive. Do the individually-inert static interventions at L11 (per-item task direction, killed) and L20 (per-item task direction, untested in this form) compose into causal movement when co-injected in a single forward pass? [HYPOTHESIS]

**Decision it changes.** **KILL** the compositional rescue if joint L11+L20 movement < 6 flips with the regime verified live and both single-layer premises held — inertness is compositional; the wall extends to pairs; the last static-combination degree of freedom closes. **CONTINUE** (licensed positive) if joint flips ≥ 6 AND McNemar-exact (doubling) p < 0.01 AND both single-layer arms stay flat (< 6) AND the joint random control stays flat — the program's first compositional causal signal; the multi-layer program opens (which pairs, which layers, interaction vs additive). **PIVOT** if a single-layer arm moves (the individual-inertness premise was wrong — re-derive before composing), if joint and control move together (summed-δ fragility, nonspecific), or if the regime is decision-frozen (pre-mapped below). All outcomes pre-registered; exactly one will be earned.

**Cheapest falsifying test.** 60 EXP092-B items × 5 arms (B, L11-only, L20-only, L11+L20 joint, W-joint at matched per-layer norms) = 300 passes (+ 60 reserve → 360 expected, 500 hard cap), CPU, $0. One downstream layer (L20 — the selection principle is pre-registered in §2.1, not asserted as unique). Per-layer ratio 0.38 (α = 8.0, the EXP096 maximum — the strongest licensed single-layer strength, giving the compositional account its best shot while staying inside the license).

**Quantitative prediction (pre-registered, bars).** Joint-vs-B: flips ≥ 6 AND McNemar-exact (doubling) p < 0.01 AND L11-only < 6 flips AND L20-only < 6 flips AND W-joint flat (< 6 flips AND |ΔM| < 0.10) AND ΔM_joint > 0 in all three strata (strict) → CONTINUE, scoped to L11+L20 co-injection at per-layer ratio 0.38 on EXP092-B. Joint < 6 at a live regime with premises held → KILL. Near-miss p ∈ [0.01, 0.05) → PIVOT (S5-1 v2 F1 precedent — never CONTINUE-with-caveat).

**Breaking point (sharp, two levels).** (i) In-band: joint movement < 6 with the regime live and both single-layer arms flat → compositional inertness; KILL. No "try three layers" rescue is licensed by this draft — that is new-design territory, not an extension. (ii) License boundary: per-layer ratio is capped at 0.38 (the EXP096 maximum). If joint movement required per-layer ratios above 0.38, the design would exit the linear license per-layer and the question would become S6-1's (super-license fragility), not composition's — the cap keeps the composition claim inside the license it tests. [INTERPRETATION of scope]

**The belief it tests (named, LOG-4408):** "inertness is a single-layer property" — overturned-by a direction-specific compositional signal (the program goes multi-layer), deepened-by a compositional KILL (the wall extends to pairs). [INTERPRETATION]

### 0.1 The composition license treatment (the central honesty section — what Law #14 must attack first)

[FACT] Per-layer ratios ≤ 0.38 are inside the linear-perturbation license (EXP093 signed pre-reg §License, cited by reference): to first order, Δm_i ≈ α₁₁·⟨∇ₕ₁₁m_i, d_i^(11)⟩ + α₂₀·⟨∇ₕ₂₀m_i, d_i^(20)⟩. The remainder is O(α²) per layer.

[INTERPRETATION] The honest null is therefore **additive superposition**: Δm_joint ≈ Δm_L11-only + Δm_L20-only. Compositional inertness is the claim that the joint does nothing beyond what the two single-layer nulls sum to. This null is *licensed by the perturbation theory both single-layer kills already used* — it is not a borrowed conclusion but the falsifiable baseline the design is built to break. What is NOT licensed is any prediction about the **interaction term** Δm_int = Δm_joint − Δm_L11 − Δm_20. The test probes for interaction; a positive is empirical, never derived.

[INTERPRETATION — the "bigger δ" objection, absorbed not dodged] A critic may argue co-injection is just a larger total δ, and EXP097 already showed large δ → fragility. Three answers, all pre-registered: (1) the fragility regime was per-layer ratio > 1; here per-layer ≤ 0.38 is the regime where single-layer T *and* single-layer B_wrong are both flat (EXP096: B_wrong 3/21 at 0.38) — if the joint moves while the matched-total-norm W-joint stays flat, "larger δ" is priced out by the control; (2) the §2.5 additive-vs-interaction decomposition classifies a positive as *additive crossing* (the critic's story, pre-registered as the weaker CONTINUE) vs *genuine interaction* (the story the critic cannot tell) — the design absorbs the objection into its verdict machinery; (3) the causal graph genuinely differs: the L11 perturbation is nonlinearly transformed by eight transformer blocks (layers 12–19) before the L20 injection lands — no single-layer injection at any norm replicates two intervention nodes with nonlinear propagation between them.

[DEFINITION — co-injection] In one forward pass: inject δ_i^(11) at layer 11's residual-stream output; run layers 12–19 normally (transforming the perturbed representation); inject δ_i^(20) at layer 20's residual-stream output; complete the pass. The L20 injection norm is anchored to the **baseline** L20 residual norm ‖h_i^(20,B)‖₂ (computed from the B pass) — never to the perturbed norm, which would make the treatment define its own denominator. The realized ratio against the perturbed norm is reported as a diagnostic.

[INTERPRETATION] What a KILL means: two individually-inert static interventions do not compose into causal movement — the wall extends to pairs. What it does NOT mean: anything about three-layer compositions, dynamic/gated mechanisms, other layer pairs/benches/models (fenced — §3); anything about the directions' decodability; anything about single-layer L20 causality beyond the premise observation (§3 step 4 names it).

---

## 1. Background and license

- **EXP094 binding facts [OBSERVATION, LOG-4375/4376/4377]:** per-item L11 task-direction injection at α=1.0 on EXP092-B: B=T=R=36/60; McNemar b=c=0 → p=1.0000; 0 flips across 120 injection item-arms; degeneracy 0.7923 < 0.95; Δθ=0. Licensed claim: per-item static L11 directions do not move decisions **at α=1.0**.
- **EXP095 binding facts [OBSERVATION, LOG-4400]:** α-sweep {0.25, 0.5, 1.0, 2.0, 4.0}: T-vs-B flips = {0, 0, 0, 1, 1}; every McNemar p = 1.0. Verdict: **REFUTED — the magic-strength rescue is dead on the licensed five-point grid**.
- **EXP096 binding facts [OBSERVATION, LOG-4407]:** headroom-gated α=8.0 (ratio 0.3792): gated T-vs-B 3 flips, p=1.0; B_wrong 3 flips, p=1.0. Verdict: **REFUTED — the headroom-gated rescue is dead**; static per-item family closed conditionally; "no further static per-item L11 experiments licensed."
- **EXP097 binding facts [OBSERVATION, LOG-4416]:** super-license ratios {1.5, 3.0}: T-vs-B 7 flips @1.5 (p=0.125), 10 flips @3.0 (p=0.109375); B_wrong 11 and 15 flips — step 5a fired → **PIVOT (fragility)**: the >1 regime moves decisions nonspecifically (random direction flips MORE than the task direction). The threshold account — the last coherent static rescue — is dead as a mechanism claim. Three-experiment closure (EXP095/096/097), fenced to **single-layer** static per-item injection.
- **EXP077 binding facts [OBSERVATION, 2026-09-23]:** at Pythia-410m/layer 20, branch (c) NEITHER — no static geometric variant of the concept direction (cone at four angles, cone-vs-line, cone-vs-control, offset, radial grid) moved decision accuracy (ΔM=0, p=1.0 throughout). Licensed claim: the tested static *geometric* variants are inert at L20. NOTE — the per-item task direction d_i^(20) at ratio 0.38 was NOT tested; the L20-only arm is therefore both a premise check and a novel single-layer test (handled — §3 step 4).
- **License by difference [INTERPRETATION]:** S6-2 clears the LOG-4407 bar because it is not a static per-item L11 experiment: two intervention nodes, nonlinear propagation between them (layers 12–19), a superposition null with an interaction probe, and verdicts (compositional KILL, interaction CONTINUE, additive-crossing CONTINUE) that no single-layer battery could produce. The EXP097 scope fence explicitly leaves multi-layer compositions open.
- **Summit filter:** composition is a primitive any self-steering system needs. A compositional KILL deepens the boundary map (the wall extends to pairs — citable infrastructure); a CONTINUE opens the multi-layer program. Caveat preserved: injection is externally applied, not self-computed — never an autonomy result.

---

## 2. Design (frozen model, Δθ = 0; per-layer ratio 0.38; one forward pass)

### 2.1 Arms (pre-registered)

| Arm | L11 injection | L20 injection | Role |
|---|---|---|---|
| B | none | none | baseline — single run per item (S5-1 v2 F2 precedent) |
| L11-only | d_i^(11) @ 0.38·‖h_i^(11,B)‖₂ (α=8.0) | none | premise check — L11 inertness at the max licensed strength |
| L20-only | none | d_i^(20) @ 0.38·‖h_i^(20,B)‖₂ (α=8.0) | premise check + novel single-layer L20 test |
| Joint | d_i^(11) @ 0.38·‖h_i^(11,B)‖₂ | d_i^(20) @ 0.38·‖h_i^(20,B)‖₂ | test arm — co-injection, one pass |
| W-joint | g_i^(11), norm-tied per-layer to the Joint arm's L11 component | g_i^(20), norm-tied per-layer to the Joint arm's L20 component | discriminant + liveness instrument (summed-δ-noise control) |

**Layer-selection principle (pre-registered, not uniqueness-claimed).** L20 is the default downstream layer because: (a) it is downstream of L11 in the concept pathway with eight nonlinear blocks between the intervention points (the interaction substrate); (b) EXP077 separated geometric-dead from relational-live mechanisms at exactly this layer — the killed direction's signal, if it exists anywhere downstream, must pass through here; (c) the per-item task direction is constructible there by the same contrast procedure. The draft does NOT claim L20 is the uniquely correct second layer — a different downstream layer is new-design territory, not a parameter tweak.

**{d_i^(11)}, {g_i^(11)} (frozen specification).** Identical to S6-1 v2 §2.1: regenerated from the frozen EXP094 constructor `experiments/runs/EXP094_peritem_l11/constructor.py`, hash-pinned `5e03f206dd907b52baa1ab6d5c9954c709d1b47d143c83f9aa85caa81917f361` [FACT]; pre-run re-hash, mismatch → HOLD. Pinned R-arm seed for {g_i}.

**{d_i^(20)} (new construction, pre-registered procedure).** The same task-contrast constructor run on **L20 residual-stream activations** (per-item direction from the identical contrast procedure, not a transported L11 vector). Pre-registered HOLD path: if the contrast fails to separate at L20 (degeneracy gate §3 step 2 fires at ≥0.95, or >2 zero-norm directions) the design is Underdetermined — never silently substituted with a different direction family. The L20 construction manifest (procedure hash, per-item norms, pairwise |cosine| summary) is a required artifact.

**Norm-tie (per layer, per item).** ‖g_i^(11)‖ == ‖δ_i^(11,joint)‖ and ‖g_i^(20)‖ == ‖δ_i^(20,joint)‖ asserted on all 60 items × 2 layers (120 assertions) — the EXP096 double-scale bug class, guarded per-layer.

**Single-B design (frozen choice).** B is byte-identical across arms (no injection) — 60 B + 240 injection = **300 passes**. Step-0 gate doubles as the determinism self-check.

### 2.2 Ratios (pre-registered, one point per layer)

Per-layer ‖δ‖/‖r‖ = **0.38** (α = 8.0; realized 0.3792 per EXP096). G5-style delivery bands (±25%): **[0.285, 0.475]** per (layer, arm). **No interpolation is licensed** — the per-layer ratio is a single pre-registered point; other per-layer ratios are new-design territory. The per-layer cap (0.38, the EXP096 maximum) is the breaking-point fence from the packet: above it the question becomes S6-1's, not composition's.

**Items:** all 60 EXP092-B items (30 A-first / 30 C-first strata, bench pin). **Not gated** — the composition question is about the push composing, not about headroom (gating would conflate EXP096's conditionality with S6-2's composition; S6-1 v2 §2.2 precedent).

### 2.3 Budget (pre-registered)

- **300 passes** (60 B + 240 injection); **+60 reserved** for delivery/margin-verification repeats → **360 expected; hard cap 500.** Spend beyond 360 requires a logged, pre-cleared exception; the 500 hard cap is not waivable within this pre-registration. CPU only, $0.
- **Single-environment rule (pre-registered, S6-1 v2 F5 carried):** all 300 passes in one pinned environment — no mid-run rebuilds; violation voids the run (Law #13).

### 2.4 Statistics (pre-registered)

- **McNemar exact, doubling convention** (EXP094's convention) on paired decisions: joint-vs-B **[discovery]**, L11-only-vs-B, L20-only-vs-B, W-joint-vs-B, joint-vs-W-joint [diagnostic-only — Law #9 hygiene].
- **ΔM** per EXP093's paired logit-margin convention; **Tango 95% CIs** on paired differences.
- **DELTA_BAR = 0.10; ALPHA_disc = 0.01** — single discovery bar (the joint-vs-B contrast). **Family-wise disclosure:** one discovery test at 0.01 → 1% family-wise for the discovery claim; premise checks and controls are not discovery tests; the §2.5 decomposition is descriptive, not a test — disclosed, not hidden. **Movement gate: ≥ 6 flips** (program standard; necessary but not sufficient — §4.2).
- **Correctness:** margin > 0 (strict), EXP094's convention.
- **Liveness instrument rule:** W-joint flips ≥ 1 → regime is LIVE → evaluate. W-joint flips = 0 AND joint flips = 0 (delivery confirmed) → FROZEN → Underdetermined (no verdict licensed). W-joint = 0 with joint ≥ 1 → LIVE (asymmetric rule, S6-1 v2 §2.4 carried).
- **Sanity gates:** zero-variance decisions on any injection arm → RUN-INVALID for that arm's contrasts (carried as sanity; replacement is not the in-license concern); ties/300 > 5% on any arm → RUN-INVALID for that arm.

### 2.5 Additive-vs-interaction decomposition (pre-registered, reported regardless of verdict)

For each item i, from the persisted margin ledger: Δm_11(i), Δm_20(i), Δm_joint(i) (margin shifts vs B), Δm_add(i) = Δm_11(i) + Δm_20(i), Δm_int(i) = Δm_joint(i) − Δm_add(i).

[DEFINITION — nearly moved] Item i is **nearly moved** by single-layer arm A iff sign(Δm_A(i)) = −sign(m_B(i)) AND |Δm_A(i)| ≥ 0.5·|m_B(i)| — the arm pushed the margin at least halfway toward the flip boundary. (Edge: m_B(i) = 0 → nearly-moved iff |Δm_A(i)| > 0.) The 50% threshold is a frozen design choice by this lane, disclosed here — Law #14 rules whether it is principled or gerrymandered; it cannot move after the run.

**Classification (descriptive):** each joint-flip item is **additive-explained** if it lies in NearlyMoved(L11) ∪ NearlyMoved(L20), else an **interaction-candidate**. Reported: counts of each class, the per-item Δm_int ledger, and the correlation of Δm_joint with Δm_add across items. This classification does not alter any verdict — it decides what a CONTINUE *means*: ≥1 interaction-candidate among the joint flips → **genuine-interaction CONTINUE** (the program's first compositional causal signal); all joint flips additive-explained → **additive-crossing CONTINUE** (composition rescues via superposition — the weaker claim, still a compositional positive).

---

## 3. Decision table (pre-registered)

**Arm-routing rule (binding):** every one of the 60 EXP092-B items receives B once and all four injection arms (full within-(item) pairing); all contrasts are paired; no item excluded from any contrast; stratum membership is the bench pin, fixed before inspection. No post-hoc re-routing.

**Binding evaluation order (first match wins).** Exactly one step is earned:

0. **Foundation gates.** (i) Constructor re-hash vs `5e03f206…917f361` → mismatch: **HOLD**. (ii) Per-item B-decision agreement vs the archived EXP094 B vector: 60/60 required → any disagreement: **HOLD**. (iii) Degeneracy sanity on {d_i^(11)}: |recomputed mean|cos| − 0.7923| > 0.05 → **HOLD**. A HOLD triggers the pre-registered diagnosis lane — **never a silent re-run**. *Foundation guards only; no verdict on the hypothesis.*
1. **Delivery.** G5 probe per (layer, i, arm): perturbation_ratio within [0.285, 0.475]. Per (layer, arm): ≤2 rows out of band → those items excluded from that arm's contrasts. >2 rows out of band on any (layer, arm), or any zero-norm direction → **HOLD + diagnose**. *(Maps to: Inconclusive.)*
2. **Degeneracy.** Mean pairwise |cosine| over {d_i^(20)} ≥ 0.95 → **Underdetermined** — the L20 direction set is degenerate; the composition test is powerless (the d_i constructor is L11-specific; this gate is its pre-registered check). {d_i^(11)} ≥ 0.95 → **Underdetermined** (carried). *(Maps to: Underdetermined.)*
3. **Regime routing (binding, before the global steps).** W-joint flips ≥ 1 → **LIVE**. W-joint flips = 0 AND joint flips = 0 (delivery confirmed) → **FROZEN** → **Underdetermined** — a KILL is never manufactured from a frozen regime. W-joint = 0 with joint ≥ 1 → **LIVE** (asymmetric rule). Sanity gates (§2.4) route per-arm RUN-INVALID where they fire.
4. **Premise PIVOT.** L11-only flips ≥ 6 OR L20-only flips ≥ 6 → **PIVOT** — the individual-inertness premise was wrong at this bench/strength; the composition question is unasked; re-derive before composing. **Named observation (pre-registered):** if L20-only ≥ 6 with McNemar p < 0.01, that is reported as a licensed single-layer L20 positive (EXP077 tested geometric variants, not this direction — this would be the program's first single-layer causal signal at a non-readout layer) and re-licenses a dedicated L20 follow-up; the composition verdict is PIVOT regardless. *(Maps to: Not supported for the composition claim.)*
5. **Fragility PIVOT.** Joint flips ≥ 6 AND W-joint flips ≥ 6 → **PIVOT** (fragility — nonspecific summed-δ movement, EXP097 step-5a precedent: the joint requirement fires only on T ≥ 6 **and** control ≥ 6 jointly). *(Maps to: Not supported for the directional claim.)*
6. **Compositional KILL.** Regime LIVE, premises held (both singles < 6), joint-vs-B flips < 6 → **Refuted: inertness is compositional** — two individually-inert static interventions do not compose into causal movement at per-layer ratio 0.38; the wall extends to pairs; the last static-combination degree of freedom closes. *(Maps to: Refuted.)*
7. **Licensed positive.** Joint-vs-B flips ≥ 6 AND McNemar-exact (doubling) p < 0.01 AND W-joint flat (< 6 flips AND |ΔM| < 0.10) AND ΔM_joint > 0 in **all three** strata (strict) → **CONTINUE (Supported)**, scoped to L11+L20 co-injection at per-layer ratio 0.38 on EXP092-B — then the §2.5 decomposition classifies it (genuine-interaction vs additive-crossing), reported inline, verdict unchanged. *(Maps to: Supported.)*
8. **Otherwise → PIVOT** *(maps to: Not supported for the global claim)*, with named sub-cases: (a) joint ≥ 6 but p ≥ 0.01 (movement without directional significance — near-miss band included, never CONTINUE-with-caveat); (b) sign-heterogeneous joint movement across strata with null joint-vs-W specificity.

Five permitted verdicts only (Supported / Not supported / Inconclusive / Underdetermined / Refuted); the parenthetical mappings bind each step to its verdict. No banned language. No EXP094/095/096/097 claim is altered. **Scope fence:** three-layer compositions, other layer pairs, other per-layer ratios, dynamic/gated mechanisms, other benches/models remain follow-up material regardless of outcome; the KILL is fenced to static two-layer (L11+L20) co-injection at per-layer ratio 0.38 on EXP092-B — never to "all compositions" or "all mechanisms"; **no interpolation is licensed**.

---

## 4. Guards (pre-registered)

- **Δθ = 0:** weight hash pre == post == LOG-331 pin `ec276abe…`; any mismatch voids the run (Law #13).
- **Frozen constructor:** re-hash before any run; mismatch vs `5e03f206…917f361` → HOLD. L20 construction follows the pre-registered procedure (§2.1) with its own manifest; the §3-step-2 gate is its check.
- **G5-style exact-delivery probe:** per-(layer,i,arm) perturbation_ratio targets 0.38, bands [0.285, 0.475] (§2.2); aggregation rule per (layer, arm) (§3 step 1). Realized-vs-perturbed-norm diagnostic for the L20 anchor (§0.1).
- **Per-item records (Law #13):** every (item, arm) persists: top-1 decision, margin (EXP093's logit-margin, cited by reference), margin shift vs B; every (item, arm, layer) persists: perturbation_ratio. **Non-negotiable.**
- **Norm-tie assertions:** 120 per-layer ties asserted pre-run (EXP096 bug class).
- **Arm-routing rule:** binding full pairing (§3); no post-hoc re-routing.
- **Thread pinning:** torch intra-op thread count pinned to the EXP092/EXP094 extraction value and asserted before condition B (EXP093 G4).
- **Single-environment rule:** all 300 passes in one pinned environment; violation voids the run (Law #13; S6-1 v2 F5 carried).

### 4.1 Degeneracy analysis of every diagnostic (LOG-4338 lesson — constant-data unit tests, pre-registered)

Each diagnostic states what it returns on degenerate input. A diagnostic that can manufacture a positive from degenerate input is disqualified; all below fail safe:

1. **McNemar exact (doubling).** Constant input (b = c = 0): p = 1.0000 exactly → fails safe toward KILL, **cannot** manufacture CONTINUE. Adversarial input (b=60, c=0): p ≈ 1.73×10⁻¹⁸.
2. **ΔM paired difference.** Zero-variance input → ΔM = 0 exactly → cannot clear DELTA_BAR = 0.10 → fails safe.
3. **Flip-rate.** No flips → 0. Safe.
4. **The liveness instrument (W-joint ≥ 1) — the dangerous direction.** (a) Truly-frozen regime: W-joint = 0, joint = 0 → FROZEN → Underdetermined — correct, never KILL. (b) Noise-unlocked regime: a single W-joint noise flip with joint = 0 → LIVE → step-6 KILL fires. **Disclosed asymmetry** (S6-1 v2 §4.1-item-4 carried): the ≥1 bar is deliberately weak to avoid manufacturing Underdetermined from freeze-ambiguity; the KILL's weight is the joint's flatness across 60 items, not the bar's height.
5. **The L20 degeneracy gate (≥0.95 → Underdetermined).** Could it dodge a KILL? It fires only when the L20 direction set is near-identical across items — i.e., the second intervention is not a per-item direction at all. On a genuine per-item set it cannot fire (L11 precedent: 0.7923). Fails safe toward Underdetermined, never toward KILL or CONTINUE. **Zero-vector edge:** a zero-norm d_i^(20) sits at perturbation_ratio = 0, outside every §2.2 band → delivery HOLD (§3 step 1) **before** the gate is ever computed.
6. **W-joint flatness — the second dangerous direction (S6-1 v2 F1 carried).** Flatness is a CONTINUE-*enabling* conjunct. True neutralization analysis: (a) a truly frozen regime yields joint = 0 too, so the joint-significance conjunct fails — the automatic neutralization path; (b) W-joint = 0 with significant directional joint routes LIVE, and a CONTINUE there fires correctly — task-geometry-specific compositional movement where matched-norm random co-injection moves nothing is the *strongest* evidence for composition. **CONTINUE requires the full conjunction** (joint significant AND W-joint flat AND all-strata ΔM_joint > 0 AND premises held); no conjunct alone licenses anything.
7. **The "nearly moved" classifier (new diagnostic).** Degenerate input (all single-layer Δm = 0): nearly-moved sets are empty → any joint flips classify as interaction-candidates. Fail-safe toward the honest reading: if neither arm moved any margin yet the joint flips decisions, that *is* interaction by definition. Adversarial input (all items nearly-moved): every joint flip classifies additive-explained → the weaker CONTINUE — the classifier cannot manufacture a genuine-interaction claim from saturated input. The classifier is descriptive; it alters no verdict.
8. **The premise-PIVOT gate (singles ≥ 6).** Could a noisy single-layer arm dodge a KILL? If L20-only truly moves ≥6, the composition question is malformed — PIVOT is correct, and the named single-layer observation (§3 step 4) preserves the discovery instead of burying it. Fails safe toward honesty, never toward a manufactured KILL.

### 4.2 Probe-feasibility algebra (EXP079 lesson — proved, not asserted)

- **McNemar minimum at ALPHA_disc = 0.01:** b=8, c=0 → p = 2·(1/2)⁸ = 0.0078125 < 0.01 ✓; b=7, c=0 → p = 0.015625, n.s. The discovery bar needs ≥8 directional flips; the ≥6-flip movement gate is necessary-but-insufficient. Maximum achievable = 60 ≥ 8. **No structural infeasibility.**
- **KILL feasibility:** needs joint < 6 at a live regime with premises held — satisfiable (the null predicts ~0–2; EXP096's single-layer B_wrong moved 3/21 at this ratio).
- **Liveness feasibility:** W-joint ≥ 1 flip — two simultaneous 0.38 random nudges; satisfiable by the same arithmetic; if it genuinely fails, the regime is frozen → step 3 fires honestly.
- **Family-wise:** one discovery contrast at 0.01 → 1% family-wise for the discovery claim — disclosed, not hidden; premise checks and controls are not discovery tests; the decomposition is descriptive.
- **Delivery bands** [0.285, 0.475] per (layer, arm): the executor's ratio targeting is EXP095/096's machinery (ratio = α·0.0474); bands ±25% by the G5 convention. Feasible by construction.
- **Budget:** 300 + 60 = 360 expected ≤ 500 hard cap. **Replication gate** (B = 36/60 per-item agreement): feasible — deterministic CPU forward passes demonstrated across EXP094/095/096/097.
- **Conclusion:** every pre-registered bar is reachable by construction. If Law #14's independent recomputation of this algebra disagrees, the run does not proceed.

### 4.3 Verdict discipline

The §3 evaluation order, five permitted verdicts with step→verdict mappings, no post-hoc table edits; a design change is a new experiment number, never a silent edit. Regime routing is computed before the global table and cannot be re-routed after inspection. **$0 compute for this draft:** on-paper only. No model runs, no weights touched, no GPU contact, no signed artifact modified.

---

## 5. Instrumentation spec (pre-registered)

Every run persists (append-only, hashed):
1. `per_item_records.csv`: (item id, stratum, arm ∈ {B, L11-only, L20-only, Joint, W-joint}, top-1 decision, margin, margin shift vs B). Margin convention: EXP093's logit-margin m(h) = logit(target) − logit(foil), cited by reference — not redefined at execution time.
2. `per_layer_delivery.csv`: (item id, arm, layer ∈ {11, 20}, perturbation_ratio, per-layer norm targets, norm-tie assertion results).
3. Constructor manifests: re-verified EXP094 constructor SHA-256 (must equal `5e03f206…917f361`), P₀ hash, R-arm seed, G7 carry-over attestation; L20 construction manifest (procedure hash, per-item d_i^(20) norms, pairwise |cosine| summary — §3-step-2 gate inputs).
4. Δθ = 0 hash pre/post; environment + seed + thread-count manifest (Law #13 reproducibility).
5. Delivery probe log: per-(layer,i,arm) perturbation_ratio vs the §2.2 bands; per-(layer,arm) PASS/FAIL aggregation decisions (§3 step 1 rule); L20 realized-vs-perturbed-norm diagnostic (§0.1).
6. Regime-routing log: the computed routing (LIVE / FROZEN / per-arm RUN-INVALID) with its evidence — machine-written, before the global table is walked.
7. Stratum table: 3 strata × 5 contrasts (joint-vs-B, L11-only-vs-B, L20-only-vs-B, W-joint-vs-B, joint-vs-W-joint [diagnostic-only]): ΔM, McNemar b/c/p, Tango 95% CI — machine-written.
8. **Margin-shift ledger** (§2.5 inputs): per item — Δm_11, Δm_20, Δm_joint, Δm_W, Δm_add, Δm_int, nearly-moved flags per single-layer arm, joint-flip class (additive-explained / interaction-candidate).
9. Decision-table worksheet: the §3 step reached, with the evidence cell for each step's condition (including step-0 foundation values and regime routing).

---

## 6. Known design risks — what Law #14 should try to break (falsification-first)

Ranked by how badly each would wound the licensed verdicts:

1. **Material difference: is co-injection a different mechanism or "bigger δ"?** The LOG-4407 bar forbids re-testing the killed family under a new name. **Counter offered (threefold, §0.1):** (a) the matched-total-norm W-joint control prices out total-δ effects — if "bigger δ" were the story, W-joint would move with the joint; (b) the §2.5 decomposition pre-registers the critic's story as *additive-crossing CONTINUE*, the weaker claim — the design absorbs the objection rather than dodging it; (c) eight nonlinear transformer blocks sit between the intervention nodes — no single-layer injection replicates that causal graph. **Attack the counters,** not just the question.
2. **Layer choice L20 — principled or convenient?** **Counter:** the draft pre-registers the selection *principle* (downstream concept-pathway layer, eight blocks of propagation substrate, EXP077's mechanism-separation layer) and explicitly disclaims uniqueness — a different downstream layer is new-design territory. Attack whether the principle is strong enough to license *this* pair, or whether the pair is underdetermined by it.
3. **The "nearly moved" 50% threshold — principled or gerrymandered?** It is a new operational definition by this lane. **Counter:** halfway-to-the-flip-boundary is the natural operationalization of "the arm almost did it alone"; it is frozen pre-run, disclosed, descriptive-only (alters no verdict), and its degenerate-input behavior is analyzed (§4.1 item 7). Attack whether 50% is arbitrary in a way that biases the additive/interaction split.
4. **L20 direction construction.** The d_i constructor is L11-specific; the task contrast may not separate at L20, or the set may be degenerate. **Counter:** the pre-registered HOLD/Underdetermined paths (§2.1, §3 step 2) make this a fail-safe, never a silent substitution — but Law #14 should confirm the gate values (0.95, >2 zero-norms) are the right tripwires and not KILL-dodgers.
5. **L20-only double duty.** It is simultaneously a premise check and a novel single-layer test; a critic may argue a ≥6 L20-only movement deserves CONTINUE rather than PIVOT. **Counter:** the composition question genuinely cannot be asked cleanly if a premise arm moves — but the §3-step-4 named observation preserves the discovery as a licensed single-layer positive with its own follow-up license, so nothing is buried. Attack whether the PIVOT label understates a first-positive.
6. **Single-B design.** Same attack surface as S6-1 v1 risk 8: per-arm B re-verification vs the step-0 archive gate. Counter carried (step-0 re-verifies B agreement before any injection; batch effects are executor-scheduling, guarded by the single-environment rule).

---

## 7. What this draft does NOT do

- Does not sign anything; does not authorize a run; does not book any compute.
- Does not mint an experiment number (reserved for the Law #14 signing lane + CEO license).
- Does not alter EXP094's/EXP095's/EXP096's/EXP097's closed run records, any prior draft, or any signed artifact; does not touch weights.
- Does not invent numbers — every value cites LOG-4407, LOG-4408, LOG-4416, the EXP094/095/096/097 verdict reviews, the frozen execution archives, or EXP093's signed pre-reg, except the co-injection definition, the per-layer ratio point, the layer-selection principle, the "nearly moved" classifier, and the decomposition machinery — which are frozen design choices by this lane, flagged for Law #14 above.
- Does not license three-layer compositions, other layer pairs, other per-layer ratios, interpolation, dynamic/gated mechanisms, other benches/models, or any claim about the directions' decodability.

---

## 8. Next steps

Independent **Law #14 review** of this draft (separate lane) → SIGN or ACCEPT-WITH-FIXES → repair lane if needed → independent delta re-verification → **CEO execution clearance** → run (CPU, ≤360 passes expected, 500 hard cap). **Pilot NOT authorized until all complete. No GPU contact under any circumstance.**

---

*Draft prepared 2026-09-28 by the S6-2 pre-registration drafter. DRAFT, UNSIGNED — Law #14 review requested but not performed; no finding is closed. On paper only, $0 compute, CPU-only design. No signed protocol file was edited.*
