# S6-3 — Dynamic Attention-Gated Injection: Does the Killed L11 Direction Move When Gated on the Model's Own Live Attention State? — Pre-registration DRAFT v1 (UNSIGNED)

*Status: DRAFT v1 — UNSIGNED. NOT a protocol. NOT executable. Awaiting independent Law #14 review (separate lane); no finding is closed. On paper only, $0 compute, CPU-only design. No signed protocol file was edited; this is a new unsigned file.*

*Licensing chain: LOG-4407 (EXP096 verdict: REFUTED — the headroom-gated rescue is dead; "no further static per-item L11 experiments licensed" — the bar S6-3 clears by gating on the model's live attention state, not on archived margins) → LOG-4408 (innovation sprint: S6-3 packet — "dynamic attention-gated injection: the direction gated on the model's own live state") → LOG-4434 (EXP099 verdict: PIVOT (fragility) — the layer-locus sweep is closed; "the program's next licensed wave is S6-3 — dynamic attention-gated injection").*

*All values below are from LOG-4400, LOG-4407, LOG-4409, LOG-4416, LOG-4423, LOG-4429, LOG-4432, LOG-4434, the EXP094–099 verdict reviews (`experiments/protocols/REVIEWS/`), the frozen execution archives, and EXP093's signed pre-reg (`experiments/protocols/EXP093_L11_CAUSAL_PREREG_SIGNED.md`) unless otherwise cited. No number is invented. Every statistic in §4.2 was recomputed by this lane from first principles ($0; no model executed, no weights touched).*
***No pilot is authorized by this draft.** Before any run: independent Law #14 review (separate lane), repair if needed, independent delta re-verification, then CEO execution clearance. CPU-only design ($0); no GPU contact under any circumstance.*

---

## 0. Binding question block

**Precise question [HYPOTHESIS].** EXP096's gate was static — precomputed from archived baseline margins before the run, identical on every re-run. Every binding verdict since has explicitly kept *dynamic* mechanisms alive. Does the killed L11 task direction move decisions when injection is gated on the model's own **live attention state** — injected only where the readout query attends to the entity span above a pre-registered threshold τ_attn, computed from the current forward pass? [HYPOTHESIS]

**Decision it changes.** **KILL:** dynamically-gated movement < 6 flips at coverage ≥ 10% with the gated random control sub-threshold → the direction is not "real but misapplied"; dynamic relevance-gating does not rescue it, and the conditional license narrows to truly dynamic mechanisms (self-computed gates and beyond). **CONTINUE:** gated flips ≥ 6 AND McNemar-exact (doubling) p < 0.01 AND gated random control flat AND stratum consistency AND coverage ≥ 10% → the first conditional causal signal at L11; the program's next lane is self-conditioned intervention. **PIVOT:** the gate fires on < 10% of items (coverage collapse → the mechanism is untestable in this form) or the gated random control moves with the task arm (attentional fragility, nonspecific). All outcomes pre-registered; exactly one will be earned.

**Cheapest falsifying test.** 60 EXP092-B items × 3 arms (B, gated-T, gated-R under the identical live gate) = 180 passes maximum (unfired items skip the injection passes by deterministic copy — §2.1), +60 reserve → 240 expected, 500 hard cap. CPU, $0. White-box forward pass with read-only attention hooks; frozen weights; Δθ=0.

**Quantitative prediction (pre-registered bars).** Gated-T-vs-B flips ≥ 6 AND McNemar-exact (doubling) p < 0.01 AND gated-R flat (< 6 flips AND |ΔM| < 0.10) AND stratum consistency (§2.5) AND gate coverage ≥ 10% → CONTINUE. Gated-T < 6 flips with coverage ≥ 10% and gated-R sub-threshold → KILL. Coverage < 10% → PIVOT (untestable form). Gated-R ≥ 6 → PIVOT (fragility), regardless of the task arm.

**Breaking point (sharp, three levels).** (i) Gate: coverage < 10% → the design declares itself untestable (PIVOT), never KILL — a KILL is never manufactured from a gate that fires nowhere. (ii) Strength: the single pre-registered ratio is 0.38 (α=8.0, realized 0.3792 per EXP096); above it the question becomes S6-1's super-license territory, not this design's — no grid, no interpolation. (iii) Degeneracy: the L11 direction set is frozen (EXP094's constructor); if its regenerated degeneracy signature deviates from 0.7923 by > 0.05 → HOLD (the pipeline changed).

**The belief it tests (named, LOG-4408):** "the direction is real but statically misapplied" — overturned-by a gated signal (the program goes self-conditioned), deepened-by a gated KILL (the conditional license narrows to truly dynamic mechanisms). [INTERPRETATION]

### 0.1 Why this is not "secretly EXP096" (the distinction Law #14 must confirm)

EXP096's gate was a **static function of archived baseline margins**: headroom precomputed from a frozen archive before the run, fixed across re-runs, blind to the model's state during the actual forward pass. S6-3's gate is a **live function of the current forward pass**: the attention mass is read from the baseline pass at execution time and varies per item with the model's own attentional state. The injected direction is the same killed L11 direction and the ratio is the same 0.38 — what changed is the *conditioning variable* (uncertainty headroom → attentional relevance), i.e. a different mechanism hypothesis: EXP096 tested "inject where the model is uncertain"; S6-3 tests "inject where the model is attending." A KILL here does not re-kill EXP096's hypothesis and a CONTINUE does not resurrect it. [INTERPRETATION]

### 0.2 The τ_attn no-peeking construction (the load-bearing answer to the packet's risk #1)

[FACT] The sprint packet (LOG-4408, S6-3 risk #1) states the load-bearing risk: S3-1/S3-3's Stage-0 died because no archive carries per-layer attention snapshots, so τ_attn **cannot be calibrated from archives**. This draft therefore calibrates nothing. τ is a **closed-form principled constant** with no calibration data and hence no peeking surface:

- For item i with prompt length N_i tokens and entity-span length E_i tokens (EXP092-B bench annotation — the same annotation family as the G1′ single-token checks; step 0 asserts it present and valid for all 60 items):
- mass_i = (1/H) Σ_h Σ_{t ∈ span_i} A^{(11,h)}_i[q_i → t], the mean-over-heads attention mass from the final prompt token q_i (the readout position — the position whose logits produce the decision) to the entity span, read from the **baseline** forward pass at layer 11 via read-only hooks.
- τ_i = 2 · (E_i / N_i) — twice the uniform-attention mass over the entity span. Twice-uniform is the standard "concentration above chance" bar: mass double the uniform expectation indicates selective attention. Pre-registered, per-item normalized, zero data, zero tuning.
- Gate fires_i ⟺ mass_i ≥ τ_i.

If the constant turns out too selective in practice, the pre-registered coverage tripwire (step 2b, EXP096 §2.4 pattern) fires honestly: coverage < 10% → PIVOT (untestable), never a manufactured KILL. The τ choice is therefore fail-safe by construction, and Law #14's job is to rule on whether 2×-uniform is *principled*, not whether it is *optimal* — optimality is not required of a pre-registered constant. [INTERPRETATION]

### 0.3 The gate-determinism note (no S6-4-style obstruction here)

[FACT] The gate is a deterministic function of the frozen baseline pass (frozen weights Δθ=0 + frozen items + pinned environment + read-only hooks): same item → same mass_i → same firing decision, every re-run. The gated experiment is therefore fully reproducible. This does **not** create S6-4's determinism obstruction: no attention-gated run has ever been executed, so the first execution is the experiment, not a replication — there is no prior observation to be circular about. (The obstruction would bite only if a *second* run on the same bench were later framed as a "confirmation" — that framing is pre-emptively disallowed here.) The gate's novelty is the gating rule itself, which is pre-registered above and has never been executed. [INTERPRETATION]

---

## 1. Background and license

- **EXP094 binding facts [OBSERVATION, LOG-4375/4376/4377]:** per-item L11 task-direction injection at α=1.0 on EXP092-B: B=T=R=36/60; McNemar b=c=0 → p=1.0000; 0 flips across 120 injection item-arms; degeneracy 0.7923 < 0.95; Δθ=0. Licensed claim: per-item static L11 directions do not move decisions **at α=1.0**.
- **EXP095 binding facts [OBSERVATION, LOG-4400]:** α-sweep {0.25, 0.5, 1.0, 2.0, 4.0}: T-vs-B flips = {0, 0, 0, 1, 1}; every McNemar p = 1.0. Verdict: **REFUTED — the magic-strength rescue is dead on the licensed five-point grid**.
- **EXP096 binding facts [OBSERVATION, LOG-4407]:** headroom-gated α=8.0 (ratio 0.3792): gated T-vs-B 3 flips, p=1.0; B_wrong 3 flips, p=1.0. Verdict: **REFUTED — the headroom-gated rescue is dead**; static per-item family closed conditionally; "no further static per-item L11 experiments licensed." **This is the strength precedent that licenses S6-3's ratio:** 0.38 at L11 has already been probed under a *different* gate (3 flips) — movement above that under the attention gate is attributable to the gating rule, not to raw strength.
- **EXP097 binding facts [OBSERVATION, LOG-4416]:** super-license ratios {1.5, 3.0}: step 5a fired → **PIVOT (fragility)**. The threshold account is dead as a mechanism claim; S6-3 stays strictly inside the linear license (single ratio 0.38, no grid).
- **EXP098 binding facts [OBSERVATION, LOG-4423]:** L11-only 3 flips (p=1.0); L20-only 6 flips (b=0, c=6, p=0.03125, sub-bar, reported as observation). S6-3 is L11-only and does not re-test the L20 observation.
- **EXP099 binding facts [OBSERVATION, LOG-4429/4434]:** layer sweep at ratio 0.38: L8-only 4 flips (p=0.625), W20 7 flips — step 5 disjunct (b) fired → **PIVOT (fragility — control-outmoves-task, named at L20)**. The anti-lesson S6-3 carries: **matched random controls are mandatory on the same items as the task arm** — S6-3's gated-R runs under the identical live gate, norm-tied per fired item.
- **S6-5 pooled audit [OBSERVATION, LOG-4409]:** task-direction pooled flips 5/381; exact one-sided 95% upper bound **2.74%** — the honest quantitative context: static task-direction movement is bounded below ~3%, not below zero.
- **License by difference [INTERPRETATION]:** S6-3 clears the LOG-4407 bar ("no further static per-item L11 experiments") because its gate is **dynamic** — a live function of the current forward pass — not a static function of archived margins. The direction, layer, ratio, and bench are deliberately the *killed* ones: the question is whether dynamic conditioning rescues them. No verdict alters EXP094–099.
- **Summit filter:** self-conditioned intervention — the perturbation gated by the model's own attentional state — is the closest CPU-testable primitive to autonomous steering. Honest about the remaining distance: the gate is *externally computed from* the model's state, not *self-computed by* the model. Boundary science either way: a gated KILL narrows the conditional license; a gated CONTINUE opens the self-conditioning program.

---

## 2. Design (frozen model, Δθ = 0; ratio 0.38; attention-gated injection at L11)

### 2.1 Arms (pre-registered)

| Arm | Injection | Gate | Role |
|---|---|---|---|
| B | none (read-only attention hooks attached) | — | baseline — single run per item; the gate is computed from this pass |
| gated-T | d_i^(11) @ 0.38·‖h_i^(11,B)‖₂, iff gate fires | live (§2.2) | **discovery test** — the dynamic-gating causal question |
| gated-R | g_i^(11), norm-tied per fired item to gated-T's δ, iff gate fires (identical live gate) | live (§2.2) | fragility discriminant + liveness instrument — the packet's "gated-B_wrong" control |

**Unfired items (pre-registered):** on items where the gate does not fire, the injection passes are **skipped** and the arm decisions are B's decisions by deterministic copy (identical input + identical frozen weights → identical output; the run log asserts the firing vector and the copies). This is exact, not an approximation. Flips can therefore only arise on fired items.

**{d_i^(11)} (frozen reuse).** EXP094's frozen per-item L11 task-contrast directions; constructor code hash-pinned `5e03f206dd907b52baa1ab6d5c9954c709d1b47d143c83f9aa85caa81917f361`; pre-run re-hash, mismatch → HOLD. Functional pin: regenerated degeneracy signature must reproduce 0.7923 within ±0.05, else HOLD. Anchored to **baseline** L11 norms ‖h_i^(11,B)‖₂ (never the perturbed norm).

**{g_i^(11)} (fresh random control).** Per-item Gaussian directions, normalized and **norm-tied per fired item** to gated-T (‖g_i^(11)‖ == ‖δ_i^(11)‖ — assertions on all fired rows; the EXP096 double-scale bug class). Fresh pre-registered seed, distinct from every prior R stream.

**Single-B design (frozen choice).** B is byte-identical across arms — 60 B + ≤120 injection = **180 passes maximum**. The attention read is hook overhead on the B pass (no extra passes).

### 2.2 The gate (pre-registered, §0.2)

For item i: N_i = prompt tokens, E_i = entity-span tokens (bench annotation; step 0 asserts 1 ≤ E_i < N_i and span excludes the final token, for all 60 items). mass_i = mean-over-heads L11 attention mass from the final prompt token to the entity span, read from the **B pass only** via read-only hooks. τ_i = 2·(E_i/N_i). Gate fires_i ⟺ mass_i ≥ τ_i. Coverage = (#fired)/60. The gate derivation is frozen: no outcome-adaptive tuning exists in this design (there is no tuning surface — τ is closed-form).

**Non-perturbation proof (pre-registered, packet risk #2):** the hooks are read-only observers; the empirical proof is step 0's B-agreement gate (60/60 vs the archived EXP094 B vector, produced by unhooked passes). Any hook-induced perturbation → HOLD, never a verdict.

### 2.3 Ratios (pre-registered, one point)

Per-item ‖δ‖/‖r‖ = **0.38** (α = 8.0; realized 0.3792 per EXP096) on fired items only. G5-style delivery bands (±25%): **[0.285, 0.475]** per (item, arm) on fired items; unfired items have **undefined** perturbation_ratio and are never probed (S6-4 precedent). **No interpolation is licensed** — 0.38 is a single pre-registered point; the strength question at L11 is EXP095/096's closed territory, not this design's. **No grid** (EXP097's lesson — a strength grid at a live gate would reopen the fragility regime without a license).

**Items:** all 60 EXP092-B items (30 A-first / 30 C-first strata, bench pin `9be8162633fe19aa…`). **Not headroom-gated** — the gating question here is attentional, not margin-based (S6-4 §2.2 precedent: one question per design).

### 2.4 Budget (pre-registered)

- **180 passes maximum** (60 B + ≤60 gated-T + ≤60 gated-R); **+60 reserved** for delivery/margin-verification repeats → **240 expected; hard cap 500.** Spend beyond 240 requires a logged, pre-cleared exception; the 500 hard cap is not waivable within this pre-registration. CPU only, $0.
- **Single-environment rule (pre-registered):** all passes in one pinned environment — no mid-run rebuilds; violation voids the run (Law #13).

### 2.5 Statistics (pre-registered)

- **McNemar exact, doubling convention** (EXP094's convention; b = wrong→right, c = right→wrong) on paired decisions: gated-T-vs-B **[discovery]**, gated-R-vs-B, gated-T-vs-gated-R [diagnostic-only — Law #9 hygiene]. All contrasts on the full 60-item paired set (unfired items contribute concordant pairs — correct: no injection, no possible flip).
- **ΔM** per EXP093's paired logit-margin convention; **Tango 95% CIs** on paired differences (descriptive).
- **DELTA_BAR = 0.10; ALPHA = 0.01** — **one** discovery contrast (gated-T-vs-B); no Bonferroni (single contrast — stated, not hidden). **Movement gate: ≥ 6 flips** (program standard; necessary but not sufficient — §4.2: significance needs ≥ 8 directional flips).
- **Stratum consistency [DEFINITION, carried from S6-4 v2 §2.4]:** let s_agg = sign(c − b) for the aggregate contrast. For each stratum s ∈ {A-first, C-first} with (b_s, c_s): consistent iff sign(c_s − b_s) = s_agg, or (b_s + c_s) < 2 (uninformative — not a contradiction). A stratum with ≥2 flips in the opposite direction fails consistency → the design cannot CONTINUE (routes to otherwise-PIVOT).
- **Correctness:** margin > 0 (strict), EXP094's convention.
- **Coverage tripwire:** coverage ≥ 10% (≥6/60 fired) → testable; < 10% → PIVOT (untestable form — §3 step 2b). (EXP096 §2.4 pattern.)
- **Liveness instrument rule:** (gated-T flips ≥ 1) OR (gated-R flips ≥ 1) → regime is LIVE → evaluate. Both 0 with coverage ≥ 10% → FROZEN → Underdetermined (no verdict licensed). Asymmetric rule carried: a moving test arm routes LIVE.
- **Sanity gates:** zero-variance decisions on any injection arm → RUN-INVALID for that arm's contrasts; ties/60 > 5% on any arm → RUN-INVALID for that arm.

---

## 3. Decision table (pre-registered)

**Arm-routing rule (binding):** every one of the 60 EXP092-B items receives B once; fired items additionally receive gated-T and gated-R (full within-item pairing on fired items; unfired items contribute B-decisions by deterministic copy — §2.1). All contrasts are paired; no item excluded from any contrast except per §3-step-1 delivery exclusions; stratum membership is the bench pin, fixed before inspection. The three strata are explicitly **(aggregate / A-first / C-first)**. No post-hoc re-routing.

**Binding evaluation order (first match wins).** Exactly one step is earned:

0. **Foundation gates.** (i) Constructor re-hash vs `5e03f206…917f361` → mismatch: **HOLD**. (ii) Per-item B-decision agreement vs the archived EXP094 B vector: 60/60 required (36/60 accuracy) → any disagreement: **HOLD** — this gate doubles as the attention-hook non-perturbation proof (packet risk #2). (iii) Entity-span annotation present and valid for all 60 items (1 ≤ E_i < N_i; span excludes the final token) → violation: **HOLD**. (iv) Regenerated {d_i^(11)} degeneracy signature: |recomputed mean|cos| − 0.7923| > 0.05 → **HOLD**. A HOLD triggers the pre-registered diagnosis lane — **never a silent re-run**. *Foundation guards only; no verdict on the hypothesis.*
1. **Delivery.** G5 probe per (fired item, arm) over the two injected cells (gated-T, gated-R): perturbation_ratio within [0.285, 0.475]. Unfired items have **undefined** perturbation_ratio and are never probed. Per arm: ≤2 fired rows out of band → those items excluded from that arm's contrasts; **the count-bars (≥6, ≥8) apply to the post-exclusion paired set** (§4.2 reports the realized N). >2 fired rows out of band on any arm → **HOLD + diagnose**. *(Maps to: Inconclusive.)*
2. **Gate integrity.** (a) **Audit:** the firing vector is derived from the B pass only — the run log asserts hook source; any injection-pass-derived gate → **HOLD**. (b) **Coverage tripwire:** coverage < 10% (<6/60 fired) → **PIVOT** (untestable — the gate is too selective; the mechanism is untestable in this form; a KILL is never manufactured from a gate that fires nowhere). (c) **Vacuous-gate flag:** coverage = 100% → proceed, with a recorded "vacuous gate" interpretation caveat (the design reduces to a static test at ratio 0.38; the verdict remains licensed but the dynamic claim is weakened — disclosed, not hidden). *(Maps to: PIVOT / proceed as specified.)*
3. **Regime routing (binding, before the global steps).** (gated-T flips ≥ 1) OR (gated-R flips ≥ 1) → **LIVE**. Both 0 **with coverage ≥ 10%** → **FROZEN** → **Underdetermined** — a KILL is never manufactured from a frozen regime. Asymmetric rule (§2.5): a moving test arm routes LIVE. Sanity gates (§2.5) route per-arm RUN-INVALID where they fire.
4. **Fragility PIVOT (EXP099's lesson, pre-registered).** First-match-wins among the disjuncts: (a) matched-control fragility — (gated-T flips ≥ 6 AND gated-R flips ≥ 6) → **PIVOT** (attentional fragility — nonspecific movement under the live gate); (b) control-outmoves-task — (gated-T flips < 6 AND gated-R flips ≥ 6) → **PIVOT** (fragility — control-outmoves-task under the live gate); the directional claim's refutation is reported as an observation. *(Maps to: Not supported for the directional claim.)*
5. **Licensed positive.** gated-T flips ≥ 6 AND McNemar-exact (doubling) p < 0.01 AND gated-R flat (< 6 flips AND |ΔM| < 0.10) AND stratum consistency (§2.5) AND coverage ≥ 10% → **CONTINUE (Supported)** — the first conditional causal signal at L11 at ratio 0.38 on EXP092-B; the program's next lane is self-conditioned intervention. *(Maps to: Supported.)*
6. **Gated KILL.** Regime LIVE, coverage ≥ 10%, gated-T flips < 6, gated-R sub-threshold (< 6 flips — any gated-R ≥ 6 world is claimed by step 4) → **Refuted: dynamic relevance-gating does not rescue the L11 direction** — the conditional license narrows to truly dynamic mechanisms. Fenced to attention-gated per-item L11 injection at ratio 0.38 on EXP092-B — never to "all dynamic mechanisms" or "all layers." *(Maps to: Refuted.)*
7. **Otherwise → PIVOT** *(maps to: Not supported for the directional claim)*, with named sub-cases: (a) gated-T ≥ 6 but p ≥ 0.01 or gated-R not flat or strata inconsistent (movement without licensed significance); (b) the step-2c vacuous-gate caveat attaches to whichever verdict fired above (weakened dynamic claim — recorded, not re-litigated).

Five permitted verdicts only (Supported / Not supported / Inconclusive / Underdetermined / Refuted); the parenthetical mappings bind each step to its verdict. No banned language. No EXP094–099 claim is altered. **Scope fence:** other layers, other ratios, other gates (headroom, self-computed), ungated α=8.0 (never tested — unlicensed follow-up, not this design), other benches/models remain follow-up material regardless of outcome; **no interpolation is licensed**.

---

## 4. Guards (pre-registered)

- **Δθ = 0:** weight hash pre == post == LOG-331 pin; any mismatch voids the run (Law #13).
- **Frozen constructor:** re-hash before any run; mismatch vs `5e03f206…917f361` → HOLD. L11 degeneracy-signature check (§3 step 0) is its functional pin.
- **Read-only hooks:** the attention read observes activations without modifying them; the empirical proof is step 0's B-agreement gate (packet risk #2). Hook implementation must be proven non-perturbative before the B pass counts — the B-agreement check *is* that proof.
- **G5-style exact-delivery probe:** per-(fired-item, arm) perturbation_ratio targets 0.38, bands [0.285, 0.475] (§2.3); aggregation rule per arm (§3 step 1).
- **Per-item records (Law #13):** every (item, arm) persists: top-1 decision, margin (EXP093's logit-margin, cited by reference), margin shift vs B, gate_fired flag; every (fired item, arm) persists: perturbation_ratio. **Non-negotiable.**
- **Norm-tie assertions:** per-fired-item ties asserted pre-run (‖g_i^(11)‖ == ‖δ_i^(11)‖; the EXP096 double-scale bug class).
- **Gate-integrity assertions:** firing vector derived from the B pass only (§3 step 2a); deterministic-copy assertion for unfired items (§2.1).
- **Arm-routing rule:** binding full pairing (§3); no post-hoc re-routing.
- **Thread pinning:** torch intra-op thread count pinned to the EXP092/EXP094 extraction value and asserted before condition B (EXP093 G4).
- **Single-environment rule:** all passes in one pinned environment; violation voids the run (Law #13).

### 4.1 Degeneracy analysis of every diagnostic (LOG-4338 lesson — constant-data unit tests, pre-registered)

Each diagnostic states what it returns on degenerate input. A diagnostic that can manufacture a positive from degenerate input is disqualified; all below fail safe:

1. **McNemar exact (doubling).** Constant input (b = c = 0): p = 1.0000 exactly → fails safe toward KILL, **cannot** manufacture CONTINUE. Adversarial input (b=60, c=0): p ≈ 1.73×10⁻¹⁸.
2. **ΔM paired difference.** Zero-variance input → ΔM = 0 exactly → cannot clear DELTA_BAR = 0.10 → fails safe.
3. **Flip-rate.** No flips → 0. Safe.
4. **The liveness instrument (gated-T ≥ 1 OR gated-R ≥ 1) — the dangerous direction.** (a) Truly-frozen regime: all arms 0 → FROZEN → Underdetermined — correct, never KILL. (b) Noise-unlocked regime: a single control noise flip with test arm 0 → LIVE → step-6 KILL fires (coverage ≥ 10% required — a noise-unlocked regime with a collapsed gate routes to step-2b PIVOT, not KILL). **Disclosed asymmetry** (S6-4 §4.1-item-4 carried): the ≥1 bar is deliberately weak to avoid manufacturing Underdetermined from freeze-ambiguity; the KILL's weight is the test arm's flatness across 60 items, not the bar's height.
5. **The coverage tripwire (new diagnostic) — the load-bearing analysis.** Degenerate input (uniform attention everywhere): mass_i = E_i/N_i < 2·E_i/N_i = τ_i for all i → coverage 0% → step 2b PIVOT (untestable) — fails safe, **never** manufactures CONTINUE or KILL. Adversarial input (τ tuned to fire everywhere): coverage 100% → step-2c vacuous-gate flag — the design reduces to a static test, but the licensed positive still requires the full step-5 conjunct (≥6 flips, p<0.01, control flat, strata consistent); the gate alone cannot manufacture a false positive. A gate that fires nowhere cannot manufacture a KILL (step 2b short-circuits before step 6). The tripwire fails safe in every direction.
6. **The gate-source audit (step 2a).** Degenerate input (executor derives the gate from an injection pass): audit assertion fails → HOLD — fails safe toward diagnosis, never toward a verdict.
7. **The B-agreement hook check (step 0ii) — new diagnostic.** Degenerate input (hooks perturb activations): B decisions deviate from the archived vector → HOLD. Fails safe toward diagnosis. Adversarial input (executor disables hooks to pass agreement): then no attention masses exist → step 0iii/2a assertions fail → HOLD. The check cannot be passed without a genuine read-only attention read.
8. **gated-R flatness — the dangerous direction (S6-4 §4.1-item-7 carried).** Flatness is a CONTINUE-*enabling* conjunct. True neutralization: (a) a truly frozen regime yields test arm 0 too, so the significance conjunct fails — the automatic neutralization path; (b) control 0 with significant directional test arm routes LIVE, and a CONTINUE there fires correctly — task-geometry-specific movement where matched-norm random injection under the identical gate moves nothing is the *strongest* evidence the gate found. **CONTINUE requires the full conjunction** (significant AND control flat AND strata consistent AND coverage ≥ 10%); no conjunct alone licenses anything.
9. **Stratum consistency (carried definition).** Degenerate input (all flips in one stratum, other stratum 0 flips): the empty stratum is uninformative (<2 flips), not contradictory → consistent. Cannot manufacture inconsistency from lopsided-but-unidirectional data. Adversarial input (flips split against the aggregate sign): fails consistency → blocks CONTINUE → fails safe toward PIVOT, never toward a false positive.

### 4.2 Probe-feasibility + power algebra (EXP079 lesson — proved, not asserted)

- **McNemar minimum at α = 0.01:** b=0, c=7 → p = 0.015625, n.s.; b=0, c=8 → p = 0.0078125 < 0.01 ✓. The discovery bar needs **≥8 directional flips** (b=0 case); the ≥6-flip movement gate is necessary-but-insufficient. Maximum achievable = 60 ≥ 8. **No structural infeasibility.**
- **Single discovery contrast:** gated-T-vs-B at family-wise 0.01 — no Bonferroni (one contrast; stated, not hidden). Controls and diagnostics are not discovery tests — disclosed, not hidden.
- **KILL feasibility:** needs gated-T < 6 at coverage ≥ 10% — satisfiable (the null predicts ~0–3; EXP096's differently-gated T moved 3/60 at this ratio).
- **CONTINUE feasibility:** needs ≥8 directional gated-T flips with the control flat — satisfiable under the hypothesis; demanding by design (the bar does not move).
- **Coverage-tripwire feasibility:** 6/60 = 10% — satisfiable; if the 2×-uniform constant misfires low, step 2b fires honestly (the tripwire's purpose).
- **Low-coverage asymmetry (disclosed):** at coverage near the 10% floor, the CONTINUE branch demands ≥6 flips among ~6–10 fired items — a high gated-conditional flip rate. The design is therefore **KILL-favoring at low coverage**; the asymmetry is declared here, not discovered later, and it points in the falsification-first direction.
- **Sweep sensitivity floor:** at N=60, the discovery bar (≥8 directional flips) implies a minimum detectable directional flip rate of θ ≈ 0.133. Effects below this are in the blind spot — disclosed, not hidden. **Post-exclusion N:** the count-bars (≥6, ≥8) apply to the post-exclusion paired set (§3 step 1) — the verdict lane recomputes and reports the realized N and the sensitivity floor (8/N_realized).
- **Noise specificity:** under a noise flip rate θ_noise = 0.03 (EXP098's L11-only moved 3/60), P(≥6 flips | N=60) = 0.0091 (S6-4 v2 §4.2) — the movement gate has <1% false-alarm rate against this noise model; P(<6) = 0.9909, so the KILL branch is well-powered against noise.
- **Delivery bands** [0.285, 0.475] per (fired item, arm): feasible by construction (EXP095/096/098 machinery).
- **Budget:** 180 + 60 = 240 expected ≤ 500 hard cap. **Replication gate** (B = 36/60 per-item agreement): feasible — deterministic CPU forward passes demonstrated across EXP094–099.
- **Conclusion:** every pre-registered bar is reachable by construction. If Law #14's independent recomputation of this algebra disagrees, the run does not proceed.

### 4.3 Verdict discipline

The §3 evaluation order, five permitted verdicts with step→verdict mappings, no post-hoc table edits; a design change is a new experiment number, never a silent edit. Gate integrity (§3 step 2) is evaluated before regime routing and cannot be re-routed after inspection. The coverage tripwire cannot be re-thresholded after inspection. **$0 compute for this draft:** on-paper only. No model runs, no weights touched, no GPU contact, no signed artifact modified.

---

## 5. Instrumentation spec (pre-registered)

Every run persists (append-only, hashed):
1. `per_item_records.csv`: (item id, stratum, arm ∈ {B, gated-T, gated-R}, top-1 decision, margin, margin shift vs B, gate_fired flag, attention mass_i, τ_i). Margin convention: EXP093's logit-margin m(h) = logit(target) − logit(foil), cited by reference — not redefined at execution time.
2. `per_item_gate.csv`: (item id, N_i, E_i, attention mass_i, τ_i, fired) — the gate audit trail; plus the hook-source assertion (gate derived from the B pass).
3. `per_item_delivery.csv`: (item id, arm, perturbation_ratio on fired items — undefined otherwise, per-item norm targets, norm-tie assertion results).
4. Constructor manifests: re-verified constructor SHA-256 (must equal `5e03f206…917f361`), P₀ hash, R-arm seed (fresh, pre-registered, distinct from all prior R streams); L11 degeneracy-signature check (0.7923 ± 0.05).
5. Δθ = 0 hash pre/post; environment + seed + thread-count manifest (Law #13 reproducibility).
6. Gate-integrity log: the firing vector, the hook-source assertion, the deterministic-copy assertion for unfired items, B-agreement 60/60 evidence.
7. Stratum table: 3 strata × 3 contrasts (gated-T-vs-B [discovery], gated-R-vs-B, gated-T-vs-gated-R [diagnostic-only]): ΔM, McNemar b/c/p, Tango 95% CI — machine-written.
8. Decision-table worksheet: the §3 step reached, with the evidence cell for each step's condition (including step-0 foundation values, gate integrity, coverage, and regime routing).
9. **S3-7 instrumentation rider** (sprint watchlist, LOG-4408): per-item top-5 token strings + ids + logits for every (item, arm), plus the baseline top-1 competitor identity — carried for free on this run's passes; no analysis pre-registered (rider only).

---

## 6. Known design risks — what Law #14 should try to break (falsification-first)

Ranked by how badly each would wound the licensed verdicts:

1. **τ = 2×(E/N): principled or convenient?** This lane claims twice-uniform is the natural "concentration above chance" bar and that optimality is not required of a pre-registered constant (the tripwire handles miscalibration). **Attack:** is 2× a principled choice or a convenient one — would 1.5× or 3× be equally defensible, and does the verdict hinge on the constant? **Attack the aggregation:** mean-over-heads is the conservative relevance signal, but max-over-heads would fire the gate more often — is mean the right operationalization of "where the readout attends"? **Attack the layer:** the gate reads L11 (the injection layer, self-consistency) — should the relevance signal come from a later layer closer to the readout? If Law #14 rules the τ construction unprincipled, the design is unlicensable (packet risk #1) — this is the draft's load-bearing joint.
2. **Is this "secretly EXP096"?** §0.1 states the distinction (static archived-margin gate vs live attention gate; uncertainty vs relevance). **Attack:** is the distinction real or verbal — could the attention gate be re-expressed as a static function of the input (in which case the LOG-4407 bar applies)? The lane's counter: the gate is computed from the model's *activations* at execution time, not from the input tokens or any archive — but Law #14 should confirm the designs test different mechanism hypotheses before licensing.
3. **The low-coverage KILL-favoring asymmetry (§4.2).** At coverage near 10%, CONTINUE demands ≥6 flips among ~6–10 fired items. **Attack:** does this make the CONTINUE branch decorative at low coverage — is the design secretly a KILL machine when the gate is selective? The lane's counter: the asymmetry is declared pre-run and points in the falsification-first direction; a CONTINUE at low coverage would be an extraordinarily strong signal. Attack whether the declared asymmetry is sufficient disclosure or a design defect.
4. **Gate-from-B: information leakage?** The gate is derived from the baseline pass, which contains no injection — but it does contain the model's full processing of the item. **Attack:** does conditioning the injection on B's attention leak outcome information into the design (Law #7 class)? The lane's counter: the gate uses no label, no margin, no outcome — only the attention distribution, which is the model's state, not the answer; and the identical gate applies to the random control. Law #14 should confirm the no-leakage argument explicitly.
5. **The strength confound (0.38 vs EXP094's 0.0474).** EXP094's 0-flip null was at α=1.0 (ratio ≈0.0474); S6-3 injects at 0.38. **Counter:** EXP096 already probed 0.3792 at L11 under a different gate (3 flips, p=1.0) — so movement *above* that level under the attention gate is attributable to the gating rule, not to raw strength. The residual confound (0.0474 → 0.38 ungated was never tested at L11) is named in §7 as unlicensed follow-up, not hidden. Attack whether the EXP096 comparison is a sufficient strength control.
6. **The vacuous gate (coverage → 100%).** Step 2c pre-registers the interpretation caveat, but **attack:** should 100% coverage instead route to HOLD (the "dynamic" in the design title would be false advertising)? The lane's counter: the verdicts remain licensed — a CONTINUE under a vacuous gate is still a directional signal at ratio 0.38, it just isn't evidence *for gating*; the caveat records exactly this. Attack whether the caveat is strong enough.
7. **Ungated α=8.0 at L11 was never tested.** If gated-T moves, the design attributes it to gating (via the EXP096 comparison, risk #5) — but the direct ungated-8.0 control does not exist. **Counter:** adding it as a fourth arm would change the packet's licensed 3-arm design; it is named here as the cheapest follow-up, not smuggled into this design. Attack whether the 3-arm design is under-controlled without it.

---

## 7. What this draft does NOT do

- Does not sign anything; does not authorize a run; does not book any compute.
- Does not mint an experiment number (reserved for the Law #14 signing lane + CEO license).
- Does not alter EXP094's–099's closed run records, any prior draft, or any signed artifact; does not touch weights.
- Does not invent numbers — every value cites LOG-4400, LOG-4407, LOG-4409, LOG-4416, LOG-4423, LOG-4429, LOG-4432, LOG-4434, the EXP094–099 verdict reviews, the frozen execution archives, or EXP093's signed pre-reg, except the τ_attn construction, the gate formalism, the power algebra, the stratum-consistency definition (carried), and the arm/delivery design choices — which are frozen design choices by this lane, flagged for Law #14 above.
- Does not license other layers, other ratios, other gates (headroom, self-computed, max-over-heads), interpolation, multi-layer compositions, other benches/models, the ungated-α=8.0 control, or any claim about the directions' decodability.
- Does not claim the gate is "self"-computation by the model — the gate is externally computed *from* the model's state (summit-filter honesty, §1). A self-computed gate is future work, not this design.
- Does not self-review, self-repair, self-clear, or self-dispatch (the S6-4 single-lane-fence lesson): this lane drafts only. Law #14 review, repair, delta re-verification, and CEO clearance are separate lanes.

---

## 8. Next steps

Independent **Law #14 adversarial review** of this v1 (separate lane, fresh to the draft) → repair lane if fixes are ordered → **independent delta re-verification** of the repaired version (separate lane) → **CEO execution clearance** → run (CPU, ≤240 passes expected, 500 hard cap). **Pilot NOT authorized until all complete. No GPU contact under any circumstance.**

---

*Draft v1 prepared 2026-09-28 by the S6-3 pre-registration drafting lane (fresh lane — did not work on S6-4/EXP099). DRAFT, UNSIGNED — awaiting independent Law #14 review; no finding is closed. On paper only, $0 compute, CPU-only design. No signed protocol file was edited.*
