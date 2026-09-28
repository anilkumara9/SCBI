# S6-4 — Causal Layer Sweep: Is There a Causal Locus Beyond L11? — Pre-registration DRAFT v1 (UNSIGNED)

*Status: DRAFT v1 — UNSIGNED. NOT a protocol. NOT executable. No Law #14 review yet; no finding is closed. On paper only, $0 compute, CPU-only design. No signed protocol file was edited; this is a new unsigned file.*
*Licensing chain: LOG-4407 (EXP096 verdict: "no further static per-item L11 experiments licensed" — the bar S6-4 clears by testing different layers, not L11) → LOG-4408 (innovation sprint: S6-4 packet — "causal layer sweep: initial L8 and L20 test") → LOG-4423 (EXP098 verdict: PIVOT (premise) — L20-only moved 6 flips, b=0, c=6, all right→wrong, p=0.03125, sub-bar; the named L20 positive did NOT fire) → CEO reprioritization (S6-4 dispatched ahead of S6-3: the EXP098 verdict made the layer-locus question the most decision-relevant open item; S6-3 follows after).*
*All values below are from LOG-4407, LOG-4408, LOG-4423, the EXP094/095/096/097/098 verdict reviews (`experiments/protocols/REVIEWS/`), the frozen execution archives, and EXP093's signed pre-reg (`experiments/protocols/EXP093_L11_CAUSAL_PREREG_SIGNED.md`) unless otherwise cited. No number is invented. Every statistic in §4.2 was recomputed by this lane from first principles ($0; no model executed, no weights touched).*
***No pilot is authorized by this draft.** Before any run: independent Law #14 review + SIGN (separate lane), repair if needed, independent delta re-verification, then CEO execution clearance. CPU-only design ($0); no GPU contact under any circumstance.*

---

## 0. Law #15 block (binding)

**Precise question [HYPOTHESIS].** Every binding verdict to date is single-layer, and L11 static per-item injection is closed across the full battery (EXP094/095/096/097). EXP098's L20-only arm moved 6 flips (all right→wrong, p=0.03125) — a live sub-bar signal, not a licensed discovery. Does task-direction injection move decisions **directionally** at L8 or L20 under the sweep bars — is there a causal locus beyond L11, or was L11 simply the wrong layer to look at? [HYPOTHESIS]

**Decision it changes.** **KILL:** no layer reaches the licensed bars (L8-only < 6 flips at a live regime; L20 reproduces its sub-bar 6 as the consistency anchor) → inertness generalizes beyond L11; the boundary law extends across the probed depth. **CONTINUE:** any layer with flips ≥ 6 AND McNemar-exact (doubling) p < 0.005 (Bonferroni over the 2 swept layers) AND matched B_wrong flat AND stratum consistency → causal locus found; the program pivots to that layer (the per-item/dose-response program replays there). **PIVOT:** movement without directional significance (fragility), the sub-bar middle, or an incomplete sweep. All outcomes pre-registered; exactly one will be earned.

**Cheapest falsifying test.** 60 EXP092-B items × 5 arms (B, L20-only, L8-only, W20, W8 at matched per-layer norms) = 300 passes (+ 60 reserve → 360 expected, 500 hard cap), CPU, $0. Two layers (L8 — below the decode peak; L20 — the EXP077/bridge layer and the EXP098 signal layer), one bench, one environment.

**Quantitative prediction (pre-registered, bars).** Per-layer discovery: flips ≥ 6 AND McNemar-exact (doubling) p < 0.005 AND matched control flat (< 6 flips AND |ΔM| < 0.10) AND stratum consistency (§2.4) → CONTINUE, scoped to that layer at ratio 0.38 on EXP092-B. L20-only is EXPECTED to reproduce EXP098's 6 flips (b=0, c=6) as the consistency anchor (§3 step 4) — this is setup validation, not a discovery test (§0.1). L8-only < 6 at a live regime → no locus at L8.

**Breaking point (sharp, three levels).** (i) Sweep: L8-only < 6 flips with the regime live and L20 reproducing its anchor → no licensed locus at either probed layer; KILL (fenced — §3). (ii) Degeneracy: per-layer direction set with mean pairwise |cosine| ≥ 0.95 → that layer void (pre-registered §3 step 2); both void → Underdetermined. (iii) Consistency: L20-only flip set ≠ EXP098's L20-only flip set → **HOLD** — the frozen pipeline changed; diagnose, never verdict.

**The belief it tests (named, LOG-4408):** "inertness is an L11 property" — overturned-by a licensed causal locus at L8 or L20 (the program pivots to that layer), deepened-by a clean sweep KILL (the wall gets taller across depth). [INTERPRETATION]

### 0.1 The determinism obstruction (the central honesty section — what Law #14 must attack first)

[FACT] The frozen pipeline is deterministic: frozen weights (Δθ=0, LOG-331 pin) + frozen direction constructor (hash-pinned `5e03f206dd907b52baa1ab6d5c9954c709d1b47d143c83f9aa85caa81917f361`) + frozen items (EXP092-B bench pin) + pinned threads + single pinned environment → the forward pass is a deterministic function of (item, direction, ratio). Precedent: per-item B-decision agreement 60/60 reproduced across EXP094→EXP098.

[THEOREM — the determinism obstruction, proved not asserted] S6-4's L20-only arm (same 60 items, same {d_i^(20)}, same ratio 0.38, same anchoring) **deterministically reproduces** EXP098's L20-only outcome: 6 flips, b=0, c=6, the same 6 items. Therefore S6-4 **cannot** confirm-or-kill the L20 6-flip signal — a re-run on the pinned bench is a re-computation, not a replication. Any draft framing the L20 arm as a "powered confirm-or-kill" on these items is circular by construction. This lane so frames nothing.

[INTERPRETATION — the reframing] S6-4 is a **layer sweep**, not an L20 replication. Its three jobs: (1) **L8 discovery** — the true discovery test (no prior observation; standard bars); (2) **L20 consistency anchor** — the L20-only arm is EXPECTED to reproduce EXP098's 6-flip set (§3 step 4); reproduction validates the frozen setup, non-reproduction is a HOLD (the pipeline changed); (3) **cross-layer patterns** — the sweep separates "locus at L8," "locus at L20" (via the anchor's sub-bar status — see below), and "no locus anywhere probed."

[INTERPRETATION — what "confirm-or-kill the L20 signal" actually requires] A genuine replication needs FRESH items (re-running pinned items adds zero information under determinism). Power analysis (exact binomial, this lane, §4.2): to confirm the observed pattern (θ=0.1 directional flip rate) at the Bonferroni bar (p<0.005, requiring ≥9 unidirectional flips), N≈115 fresh items gives 82% power; N=60 gives 14%. The 95% Clopper-Pearson interval on the observed 6/60 is θ ∈ [0.0376, 0.2051] — the effect-size uncertainty is large. **The N≈115 powered L20 replication is specified and priced in §4.2 but NOT licensed by this draft** — it requires fresh bench construction per EXP092's signed protocol (G2 null-calibration, oracle diagnostic) plus explicit CEO licensing via a separate pre-registration. S6-4's outcomes inform that decision; none of them triggers it automatically.

[INTERPRETATION — the power asymmetry, disclosed] At N=60 (the bench pin — the only 60-item pool of this construction): the L8 discovery test has a sensitivity floor of θ≈0.15 directional flip rate (9/60); effects below this are in the blind spot. The sweep KILL (L8 <6 at live) has 99% specificity under noise θ=0.03. The design is therefore a well-powered KILL-or-PIVOT sweep with a licensed-but-demanding CONTINUE branch — the bar does not move, and the power is stated here, not discovered later.

---

## 1. Background and license

- **EXP094 binding facts [OBSERVATION, LOG-4375/4376/4377]:** per-item L11 task-direction injection at α=1.0 on EXP092-B: B=T=R=36/60; McNemar b=c=0 → p=1.0000; 0 flips across 120 injection item-arms; degeneracy 0.7923 < 0.95; Δθ=0. Licensed claim: per-item static L11 directions do not move decisions **at α=1.0**.
- **EXP095 binding facts [OBSERVATION, LOG-4400]:** α-sweep {0.25, 0.5, 1.0, 2.0, 4.0}: T-vs-B flips = {0, 0, 0, 1, 1}; every McNemar p = 1.0. Verdict: **REFUTED — the magic-strength rescue is dead on the licensed five-point grid**.
- **EXP096 binding facts [OBSERVATION, LOG-4407]:** headroom-gated α=8.0 (ratio 0.3792): gated T-vs-B 3 flips, p=1.0; B_wrong 3 flips, p=1.0. Verdict: **REFUTED — the headroom-gated rescue is dead**; static per-item family closed conditionally; "no further static per-item L11 experiments licensed."
- **EXP097 binding facts [OBSERVATION, LOG-4416]:** super-license ratios {1.5, 3.0}: T-vs-B 7 flips @1.5 (p=0.125), 10 flips @3.0 (p=0.109375); B_wrong 11 and 15 flips — step 5a fired → **PIVOT (fragility)**. The threshold account is dead as a mechanism claim. Three-experiment closure (EXP095/096/097), fenced to **single-layer** static per-item injection.
- **EXP098 binding facts [OBSERVATION, LOG-4423]:** L11+L20 co-injection: L11-only 3 flips (p=1.0); **L20-only 6 flips, b=0, c=6, all right→wrong, p=0.03125**; Joint 7 flips (all additive-explained, 0 interaction-candidate); W-joint 12 flips. Verdict: **PIVOT (premise)** — the L20-only premise arm moved, so the composition question was unasked. The named licensed single-layer L20 positive did NOT fire (requires p<0.01; observed 0.03125) — the 6-flip movement is a reported observation in the pre-registered near-miss band, never a discovery. L20 degeneracy 0.6639 < 0.95.
- **EXP077 binding facts [OBSERVATION, 2026-09-23]:** at Pythia-410m/layer 20, branch (c) NEITHER — no static *geometric* variant of the concept direction moved decision accuracy. Licensed claim: the tested static geometric variants are inert at L20. The per-item task direction is a different construction (EXP098's C-1 on L20 residuals).
- **License by difference [INTERPRETATION]:** S6-4 clears the LOG-4407 bar because it tests **different layers** (L8, L20), not L11 — and its L20 arm is a consistency anchor for EXP098's already-reported observation, not a re-test of a killed family. No verdict alters EXP094–098. The L8 direction construction is new-design territory within this pre-registration (not a silent extension of anything).
- **Summit filter:** mapping where (if anywhere) frozen geometry is causal across depth is the prerequisite map for any steering program. A clean sweep KILL deepens the boundary law (citable infrastructure); a licensed locus reorients the program. Honest either way.

---

## 2. Design (frozen model, Δθ = 0; per-layer ratio 0.38; one forward pass per (item, arm))

### 2.1 Arms (pre-registered)

| Arm | L8 injection | L20 injection | Role |
|---|---|---|---|
| B | none | none | baseline — single run per item (S5-1 v2 F2 precedent) |
| L20-only | none | d_i^(20) @ 0.38·‖h_i^(20,B)‖₂ | **consistency anchor** — expected to reproduce EXP098's 6-flip set (§3 step 4); NOT a discovery test (§0.1) |
| L8-only | d_i^(8) @ 0.38·‖h_i^(8,B)‖₂ | none | **discovery test** — the sweep's causal question at L8 |
| W20 | none | g_i^(20), norm-tied per-item to L20-only | fresh-randomness fragility discriminant at L20 (fresh seed, not EXP098's W-joint draw) |
| W8 | g_i^(8), norm-tied per-item to L8-only | none | fragility discriminant + liveness instrument at L8 |

**{d_i^(20)} (frozen reuse).** Regenerated from the frozen EXP098 procedure — identical C-1 task-contrast on L20 residuals (Pass A vs P0), anchored to **baseline** L20 norms ‖h_i^(20,B)‖₂ (never the perturbed norm); constructor code hash-pinned `5e03f206dd907b52baa1ab6d5c9954c709d1b47d143c83f9aa85caa81917f361`; pre-run re-hash, mismatch → HOLD. Functional pin: the regenerated set's mean pairwise |cosine| must reproduce EXP098's 0.6639 within ±0.05, else HOLD. [FACT: procedure per `experiments/runs/EXP098_multilayer_composition/out/constructor_manifest.json`]

**{d_i^(8)} (new construction, pre-registered procedure).** The identical C-1 task-contrast procedure run on **L8 residual-stream activations** (per-item direction from the same contrast, not a transported vector). Pre-registered HOLD path: degeneracy gate §3 step 2 (≥0.95) or >2 zero-norm directions → that layer void (never silently substituted). The L8 construction manifest (procedure hash, per-item norms, pairwise |cosine| summary) is a required artifact.

**{g_i^(20)}, {g_i^(8)} (fresh random controls).** Per-item Gaussian directions, normalized and **norm-tied per-layer per-item** to the corresponding test arm (‖g_i^(20)‖ == ‖δ_i^(20)‖, ‖g_i^(8)‖ == ‖δ_i^(8)‖ — 120 assertions; the EXP096 double-scale bug class, guarded per-layer). Fresh pre-registered seeds, distinct from EXP098's R_SEED=94094 stream.

**Single-B design (frozen choice).** B is byte-identical across arms (no injection) — 60 B + 240 injection = **300 passes**. Step-0 gate doubles as the determinism self-check.

### 2.2 Ratios (pre-registered, one point per layer)

Per-layer ‖δ‖/‖r‖ = **0.38** (α = 8.0; realized 0.3792 per EXP096). G5-style delivery bands (±25%): **[0.285, 0.475]** per (layer, arm). **No interpolation is licensed** — 0.38 is a single pre-registered point; other per-layer ratios are new-design territory. The 0.38 cap is the breaking-point fence: above it the question becomes S6-1's (super-license fragility, closed for L11), not the sweep's. L20 anchoring to baseline norms is carried from EXP098 (§0.1 of S6-2 v2); L8 anchoring is identical (baseline L8 norms).

**Items:** all 60 EXP092-B items (30 A-first / 30 C-first strata, bench pin). **Not gated** — the sweep question is about layer locus, not headroom (S6-1 v2 §2.2 precedent).

### 2.3 Budget (pre-registered)

- **300 passes** (60 B + 240 injection); **+60 reserved** for delivery/margin-verification repeats → **360 expected; hard cap 500.** Spend beyond 360 requires a logged, pre-cleared exception; the 500 hard cap is not waivable within this pre-registration. CPU only, $0.
- **Single-environment rule (pre-registered, S6-1 v2 F5 carried):** all 300 passes in one pinned environment — no mid-run rebuilds; violation voids the run (Law #13).

### 2.4 Statistics (pre-registered)

- **McNemar exact, doubling convention** (EXP094's convention; b = wrong→right, c = right→wrong) on paired decisions: L20-only-vs-B **[consistency anchor — not a discovery contrast]**, L8-only-vs-B **[discovery]**, W20-vs-B, W8-vs-B, L8-only-vs-W8 [diagnostic-only — Law #9 hygiene].
- **ΔM** per EXP093's paired logit-margin convention; **Tango 95% CIs** on paired differences (descriptive).
- **DELTA_BAR = 0.10; per-layer ALPHA = 0.005** — family-wise 0.01, Bonferroni over the 2 swept layers (the packet's "p < 0.01 Bonferroni-over-layers," disambiguated: the 0.01 is the family-wise level). **Two discovery contrasts** (L8-only-vs-B; the L20 anchor is explicitly NOT a discovery contrast). **Movement gate: ≥ 6 flips** (program standard; necessary but not sufficient — §4.2).
- **Stratum consistency [DEFINITION, pre-registered]:** let s_agg = sign(c − b) for the aggregate contrast. For each stratum s ∈ {A-first, C-first} with (b_s, c_s): consistent iff sign(c_s − b_s) = s_agg, or (b_s + c_s) < 2 (uninformative — not a contradiction). A stratum with ≥2 flips in the opposite direction fails consistency → the layer cannot CONTINUE (routes to otherwise-PIVOT).
- **Correctness:** margin > 0 (strict), EXP094's convention.
- **Liveness instrument rule:** (W20 flips ≥ 1) OR (W8 flips ≥ 1) → regime is LIVE → evaluate. Both controls 0 flips AND both test arms 0 flips (delivery confirmed) → FROZEN → Underdetermined (no verdict licensed). Asymmetric rule carried (S6-1 v2 §2.4): a 0-control with a moving test arm routes LIVE.
- **Sanity gates:** zero-variance decisions on any injection arm → RUN-INVALID for that arm's contrasts; ties/300 > 5% on any arm → RUN-INVALID for that arm.

---

## 3. Decision table (pre-registered)

**Arm-routing rule (binding):** every one of the 60 EXP092-B items receives B once and all four injection arms (full within-item pairing); all contrasts are paired; no item excluded from any contrast; stratum membership is the bench pin, fixed before inspection. The three strata are explicitly **(aggregate / A-first / C-first)** (S6-1 v2 precedent). No post-hoc re-routing.

**Binding evaluation order (first match wins).** Exactly one step is earned:

0. **Foundation gates.** (i) Constructor re-hash vs `5e03f206…917f361` → mismatch: **HOLD**. (ii) Per-item B-decision agreement vs the archived EXP094 B vector: 60/60 required (36/60 accuracy) → any disagreement: **HOLD**. (iii) Regenerated {d_i^(20)} degeneracy signature: |recomputed mean|cos| − 0.6639| > 0.05 → **HOLD**. A HOLD triggers the pre-registered diagnosis lane — **never a silent re-run**. *Foundation guards only; no verdict on the hypothesis.*
1. **Delivery.** G5 probe per (item, arm, layer) over the four injected (layer, arm) cells — (20, L20-only), (20, W20), (8, L8-only), (8, W8): perturbation_ratio within [0.285, 0.475]. Non-injected cells have **undefined** perturbation_ratio and are never probed (S6-2 v2 F3 precedent). Per (layer, arm): ≤2 rows out of band → those items excluded from that arm's contrasts. >2 rows out of band on any (layer, arm), or any zero-norm direction → **HOLD + diagnose**. *(Maps to: Inconclusive.)*
2. **Degeneracy (per-layer void logic, pre-registered).** Mean pairwise |cosine| over {d_i^(20)} ≥ 0.95 → **L20 void**; over {d_i^(8)} ≥ 0.95 → **L8 void**. Both void → **Underdetermined** (whole test). One void → the other layer proceeds alone: the licensed positive (step 6) remains available for the testable layer; the sweep KILL (step 7) is **downgraded to PIVOT** (incomplete sweep — "no locus" cannot be closed with a layer untested); the consistency anchor (step 4) is skipped if L20 is void (setup cross-validation lost — reported as a caveat, verdicts unchanged). *(Maps to: Underdetermined / PIVOT as specified.)*
3. **Regime routing (binding, before the global steps).** (W20 flips ≥ 1) OR (W8 flips ≥ 1) → **LIVE**. Both controls 0 AND both test arms 0 (delivery confirmed) → **FROZEN** → **Underdetermined** — a KILL is never manufactured from a frozen regime. Asymmetric rule (§2.4). Sanity gates (§2.4) route per-arm RUN-INVALID where they fire.
4. **Consistency anchor (setup validation — NOT a verdict step).** L20-only flip **set** must equal EXP098's L20-only flip set (the same 6 items; b=0, c=6 expected). Equality → setup validated; proceed. Any difference (different count or different items) → **HOLD** — the frozen pipeline changed; diagnose, never verdict. *This step guards the experiment; it licenses no finding about L20 causality (EXP098's observation stands as reported, sub-bar).*
5. **Fragility PIVOT.** (L8-only flips ≥ 6 AND W8 flips ≥ 6) OR (W20 flips ≥ 6) [L20-only is deterministically 6 per the anchor, so fresh-randomness W20 ≥ 6 completes the fragility pattern] → **PIVOT** (fragility — nonspecific δ-driven movement), naming the layer(s). *(Maps to: Not supported for the directional claim.)*
6. **Licensed positive (L8).** L8-only flips ≥ 6 AND McNemar-exact (doubling) p < 0.005 AND W8 flat (< 6 flips AND |ΔM| < 0.10) AND stratum consistency (§2.4) → **CONTINUE (Supported)** — causal locus at L8 at ratio 0.38 on EXP092-B; the per-item/dose-response program replays at L8. *(Maps to: Supported.)*
7. **Sweep KILL.** Regime LIVE, L8-only flips < 6 (L20 anchor reproduced per step 4) → **Refuted: no licensed causal locus at L8 or L20** — the EXP098 L20 observation remains sub-bar as reported (this design does not re-test it — §0.1); inertness generalizes across the probed depth; the boundary law extends. Fenced to static per-item injection at L8/L20, ratio 0.38, EXP092-B — never to "all layers" or "all mechanisms." *(Maps to: Refuted.)*
8. **Otherwise → PIVOT** *(maps to: Not supported for the global claim)*, with named sub-cases: (a) L8-only ≥ 6 but p ≥ 0.005 or W8 not flat or strata inconsistent (movement without licensed significance); (b) step-2 single-layer void (incomplete sweep); (c) sign-heterogeneous L8 movement across strata.

Five permitted verdicts only (Supported / Not supported / Inconclusive / Underdetermined / Refuted); the parenthetical mappings bind each step to its verdict. No banned language. No EXP094–098 claim is altered. **Scope fence:** other layers (including readout-adjacent — the packet's Phase 2, separate pre-reg only), other ratios, three-layer compositions, dynamic/gated mechanisms, other benches/models remain follow-up material regardless of outcome; **no interpolation is licensed**. The cross-layer patterns (§6) are interpretations of step outcomes, not separate verdicts.

---

## 4. Guards (pre-registered)

- **Δθ = 0:** weight hash pre == post == LOG-331 pin; any mismatch voids the run (Law #13).
- **Frozen constructor:** re-hash before any run; mismatch vs `5e03f206…917f361` → HOLD. L8 construction follows the pre-registered procedure (§2.1) with its own manifest; the §3-step-2 gate is its check. L20 set carries the degeneracy-signature check (§3 step 0).
- **G5-style exact-delivery probe:** per-(item,arm,layer) perturbation_ratio targets 0.38, bands [0.285, 0.475] (§2.2); aggregation rule per (layer, arm) (§3 step 1). L20 realized-vs-perturbed-norm diagnostic carried from EXP098.
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
4. **The liveness instrument (W20 ≥ 1 OR W8 ≥ 1) — the dangerous direction.** (a) Truly-frozen regime: all arms 0 → FROZEN → Underdetermined — correct, never KILL. (b) Noise-unlocked regime: a single control noise flip with test arms 0 → LIVE → step-7 KILL fires. **Disclosed asymmetry** (S6-1 v2 §4.1-item-4 carried): the ≥1 bar is deliberately weak to avoid manufacturing Underdetermined from freeze-ambiguity; the KILL's weight is the test arms' flatness across 60 items, not the bar's height.
5. **The consistency anchor (step 4) — new diagnostic.** Degenerate input: if the pipeline were non-deterministic, the anchor would fail spuriously → HOLD (not a verdict). Fails safe toward diagnosis, never toward a false KILL or CONTINUE. Adversarial input (executor "tunes" to reproduce): the anchor reproduces the *flips*, but the discovery test is at L8 with fresh directions — tuning L20 buys nothing at L8. Cannot manufacture a positive.
6. **The per-layer degeneracy gates (≥0.95 → void).** Could a gate dodge a KILL? It fires only when a direction set is near-identical across items — i.e., that layer's intervention is not a per-item direction at all. On a genuine per-item set it cannot fire (L20 precedent: 0.6639; L11 precedent: 0.7923). Fails safe toward void/PIVOT, never toward KILL or CONTINUE. **Zero-vector edge:** a zero-norm direction sits at perturbation_ratio = 0, outside every §2.2 band → delivery HOLD (§3 step 1) **before** any gate is computed.
7. **W-flatness — the dangerous direction (S6-2 v2 §4.1-item-6 carried).** Flatness is a CONTINUE-*enabling* conjunct. True neutralization analysis: (a) a truly frozen regime yields test arms 0 too, so the significance conjunct fails — the automatic neutralization path; (b) control 0 with significant directional test arm routes LIVE, and a CONTINUE there fires correctly — task-geometry-specific movement where matched-norm random injection moves nothing is the *strongest* evidence for a locus. **CONTINUE requires the full conjunction** (significant AND control flat AND strata consistent); no conjunct alone licenses anything.
8. **Stratum consistency (new diagnostic).** Degenerate input (all flips in one stratum, other stratum 0 flips): the empty stratum is uninformative (<2 flips), not contradictory → consistent. Cannot manufacture inconsistency from lopsided-but-unidirectional data. Adversarial input (flips split against the aggregate sign): fails consistency → blocks CONTINUE → fails safe toward PIVOT, never toward a false positive.

### 4.2 Probe-feasibility + power algebra (EXP079 lesson — proved, not asserted)

- **McNemar minimum at per-layer α = 0.005:** b=0, c=8 → p = 0.0078125, n.s.; b=0, c=9 → p = 0.00390625 < 0.005 ✓. The discovery bar needs **≥9 directional flips** (b=0 case); the ≥6-flip movement gate is necessary-but-insufficient. Maximum achievable = 60 ≥ 9. **No structural infeasibility.**
- **Bonferroni:** 2 discovery contrasts (L8-only-vs-B; the L20 anchor is explicitly not a discovery contrast) at family-wise 0.01 → per-contrast 0.005. The consistency anchor and all controls/diagnostics are not discovery tests — disclosed, not hidden.
- **KILL feasibility:** needs L8-only < 6 at a live regime — satisfiable (the null predicts ~0–3; EXP098's L11-only moved 3/60 at this ratio).
- **Liveness feasibility:** (W20 ≥ 1) OR (W8 ≥ 1) — satisfiable; if both genuinely fail with test arms at 0, the regime is frozen → step 3 fires honestly.
- **Sweep sensitivity floor:** at N=60, the discovery bar (≥9 directional flips) implies a minimum detectable directional flip rate of θ ≈ 0.15. Effects below this are in the blind spot — disclosed, not hidden.
- **Noise specificity:** under a noise flip rate θ_noise = 0.03 (EXP098's L11-only moved 3/60), P(≥6 flips | N=60) = 0.0091 — the movement gate has <1% false-alarm rate against this noise model; P(<6) = 0.9909, so the KILL branch is well-powered against noise.
- **The L20 confirm-or-kill power analysis (exact binomial, this lane):** assuming the observed pattern replicates (each item flips R→W w.p. θ, never W→R), confirming at p<0.005 needs ≥9 flips: P(X≥9 | N=60, θ=0.10) = **0.142**; P(X≥9 | N=115, θ=0.10) = **0.823**; at the conservative θ=0.07: 0.023 (N=60), 0.415 (N=115). The 95% Clopper-Pearson interval on the observed 6/60 is θ ∈ [0.0376, 0.2051]. **Conclusion:** a genuine L20 confirm-or-kill needs **N≈115 fresh items** (82% power at the point estimate) — specified and priced below, NOT licensed by this draft (§0.1).
- **Pricing the unlicensed follow-up:** N=115 × 5 arms (B, L20-only, W20, + 2 reserve/diagnostic) ≈ 575 passes + fresh bench construction per EXP092's signed protocol (G2 null-calibration, oracle diagnostic — separate pre-registration required). CPU-feasible ($0; EXP095 ran 724 passes), but the bench construction is the binding constraint, not the passes.
- **Delivery bands** [0.285, 0.475] per (layer, arm): feasible by construction (EXP095/096/098 machinery).
- **Budget:** 300 + 60 = 360 expected ≤ 500 hard cap. **Replication gate** (B = 36/60 per-item agreement): feasible — deterministic CPU forward passes demonstrated across EXP094–098.
- **Conclusion:** every pre-registered bar is reachable by construction. If Law #14's independent recomputation of this algebra disagrees, the run does not proceed.

### 4.3 Verdict discipline

The §3 evaluation order, five permitted verdicts with step→verdict mappings, no post-hoc table edits; a design change is a new experiment number, never a silent edit. Regime routing is computed before the global table and cannot be re-routed after inspection. The consistency anchor (§3 step 4) is evaluated before the global steps and cannot be re-interpreted after inspection. **$0 compute for this draft:** on-paper only. No model runs, no weights touched, no GPU contact, no signed artifact modified.

---

## 5. Instrumentation spec (pre-registered)

Every run persists (append-only, hashed):
1. `per_item_records.csv`: (item id, stratum, arm ∈ {B, L20-only, L8-only, W20, W8}, top-1 decision, margin, margin shift vs B). Margin convention: EXP093's logit-margin m(h) = logit(target) − logit(foil), cited by reference — not redefined at execution time.
2. `per_layer_delivery.csv`: (item id, arm, layer ∈ {8, 20}, perturbation_ratio, per-layer norm targets, norm-tie assertion results).
3. Constructor manifests: re-verified EXP094 constructor SHA-256 (must equal `5e03f206…917f361`), P₀ hash, R-arm seeds (fresh, pre-registered, distinct from EXP098's 94094); L20 degeneracy-signature check (0.6639 ± 0.05); L8 construction manifest (procedure hash, per-item d_i^(8) norms, pairwise |cosine| summary — §3-step-2 gate inputs).
4. Δθ = 0 hash pre/post; environment + seed + thread-count manifest (Law #13 reproducibility).
5. Delivery probe log: per-(item,arm,layer) perturbation_ratio vs the §2.2 bands; per-(layer,arm) PASS/FAIL aggregation decisions (§3 step 1 rule); L20 realized-vs-perturbed-norm diagnostic (EXP098 precedent).
6. Regime-routing log: the computed routing (LIVE / FROZEN / per-arm RUN-INVALID) with its evidence — machine-written, before the global table is walked.
7. Consistency-anchor log: L20-only flip set vs EXP098's L20-only flip set (set-equality check, §3 step 4) — machine-written.
8. Stratum table: 3 strata × 5 contrasts (L20-only-vs-B [anchor], L8-only-vs-B [discovery], W20-vs-B, W8-vs-B, L8-only-vs-W8 [diagnostic-only]): ΔM, McNemar b/c/p, Tango 95% CI — machine-written.
9. Decision-table worksheet: the §3 step reached, with the evidence cell for each step's condition (including step-0 foundation values, regime routing, and the anchor check).
10. **S3-7 instrumentation rider** (sprint watchlist, LOG-4408): per-item top-5 token strings + ids + logits for every (item, arm), plus the baseline top-1 competitor identity — carried for free on this run's passes; no analysis pre-registered (rider only).

---

## 6. Known design risks — what Law #14 should try to break (falsification-first)

Ranked by how badly each would wound the licensed verdicts:

1. **The determinism obstruction (§0.1) — is the reframing correct?** This lane claims S6-4 cannot confirm-or-kill the L20 signal on the pinned bench and reframes the experiment as a sweep + anchor. **Attack:** is there any legitimate sense in which re-running L20-only is informative beyond setup validation (e.g., a subtle non-determinism this lane dismisses too fast)? If the obstruction is wrong, the whole §0.1 reframing — and the step-4 anchor design — is misbuilt.
2. **Is the L20 anchor a wasted arm?** 60 of the 300 passes reproduce a known result. **Counter:** the anchor is the only frozen-setup cross-validation available (B-agreement validates the base pipeline; the anchor validates the *injection* pipeline at a new layer pair); without it, an L8 null could be blamed on broken injection machinery. Attack whether the price (60 passes) is worth the insurance.
3. **The sweep's sensitivity floor (θ≈0.15).** The L8 discovery test can only see large directional effects. **Counter:** disclosed in §4.2; the KILL branch is well-powered; a sub-threshold L8 effect is genuinely out of reach at N=60 and belongs to the priced follow-up regime, not to goalpost-moving. Attack whether the floor makes the CONTINUE branch decorative.
4. **L8 direction construction.** The d_i constructor is L11-specific; the task contrast may not separate at L8, or the set may be degenerate. **Counter:** the pre-registered void/Underdetermined paths (§2.1, §3 step 2) make this a fail-safe, never a silent substitution — but Law #14 should confirm the gate values (0.95, >2 zero-norms) are the right tripwires and not KILL-dodgers (cf. S6-2 v2 §4.1-item-5).
5. **Stratum consistency — principled or gerrymandered?** It is a new operational definition by this lane. **Counter:** sign-agreement with an uninformative-stratum exemption is the natural operationalization of "not driven by one stratum"; it is frozen pre-run, disclosed, and its degenerate-input behavior is analyzed (§4.1 item 8). Attack whether the <2-flip exemption is too lenient.
6. **W20 fresh seed.** EXP098's W-joint already measured L20 fragility (12 flips); S6-4 re-draws W20 fresh. **Counter:** the fresh draw is an independent fragility check (the old draw's 12 flips could be seed-luck); reusing EXP098's seed would be the circular choice. Attack whether two fragility measurements at L20 double-count.
7. **Phase-2 readout-adjacent layer.** The packet licenses Phase 2 only on a clean Phase-1 KILL, via separate pre-reg. **Counter:** pre-registered here as unlicensed-by-this-draft; "just one more layer" is how sweeps become fishing (packet's own risk #3). Attack whether even naming Phase 2 invites scope creep.

---

## 7. What this draft does NOT do

- Does not sign anything; does not authorize a run; does not book any compute.
- Does not mint an experiment number (reserved for the Law #14 signing lane + CEO license).
- Does not alter EXP094's–098's closed run records, any prior draft, or any signed artifact; does not touch weights.
- Does not invent numbers — every value cites LOG-4407, LOG-4408, LOG-4423, the EXP094–098 verdict reviews, the frozen execution archives, or EXP093's signed pre-reg, except the determinism-obstruction proof, the power analysis, the stratum-consistency definition, the L8 construction procedure, and the arm/delivery design choices — which are frozen design choices by this lane, flagged for Law #14 above.
- Does not license the N≈115 powered L20 replication (specified and priced in §4.2, explicitly unlicensed — needs fresh bench construction + separate pre-reg + CEO license).
- Does not license other layers, other ratios, interpolation, three-layer compositions, dynamic/gated mechanisms, other benches/models, Phase 2 (readout-adjacent), or any claim about the directions' decodability.

---

## 8. Next steps

Independent **Law #14 review** of this draft (separate lane) → SIGN or ACCEPT-WITH-FIXES → repair lane if needed → independent delta re-verification → **CEO execution clearance** → run (CPU, ≤360 passes expected, 500 hard cap). **Pilot NOT authorized until all complete. No GPU contact under any circumstance.**

---

*Draft v1 prepared 2026-09-28 by the S6-4 pre-registration drafter (reprioritized ahead of S6-3 per CEO order: the EXP098 verdict made the layer-locus question the most decision-relevant open item). DRAFT, UNSIGNED — no Law #14 review yet; no finding is closed. On paper only, $0 compute, CPU-only design. No signed protocol file was edited.*
