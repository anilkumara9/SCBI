# Next-Direction Innovation Sprint — 2026-09-28

*Innovation lead lane. Falsification-first. No execution, no compute, $0 — proposals only.*
*Licensing chain: LOG-4391 (Monday session, S5-1–S5-4 PROPOSALs) → LOG-4400 (EXP095 verdict: REFUTED) → LOG-4407 (EXP096 verdict: REFUTED).*

## 0. Situation [FACT]

EXP095 + EXP096 closed the static per-item L11 family **conditionally** (within the linear license, ratio ≤ 0.38) — the program's first conditionally-closed mechanism family. Both verdicts bar any further static per-item L11 experiment: no re-sweeps, no α=16 variant (both follow-up conditions failed), nothing pre-licensed. The Monday backlog S5-1–S5-4 is exhausted (all four executed or completed — marked in `CANDIDATE_BACKLOG.md`).

**What survives, per the binding verdicts:** gated/dynamic mechanisms, multi-layer compositions, >0.4740-ratio regimes (including the untested ‖δ‖/‖r‖>1 breaking point), other layers/benches. **What is untouched:** the GPU queue (K2 → EXP083 → EXP084 → EXP086 Stage B → EXP088 → EXP087) — parked on the founder's Kaggle; this sprint proposes CPU-only $0 lanes exclusively.

**Death-debt accounting (LOG-219 rule):** this sprint is the death-debt payment for EXP095 and EXP096 — every null below produces ≥1 new falsifiable candidate, logged before the workstream closes.

## Ranked proposals

### S6-1 — The threshold-account breaking point: injection beyond the linear license (‖δ‖/‖r‖ > 1) [TOP GREEN-LIGHT]

**Precise question [HYPOTHESIS].** EXP095 mapped the dose-response inside the linear license (max ratio 0.1896); EXP096 pushed to ratio 0.38 — both flat. The program's own license (LOG-4391) named ‖δ‖/‖r‖>1 as the threshold account's breaking point, and both verdicts fenced it as untested. Does the per-item L11 task direction move decisions when the injection **exceeds** the linear license — where the threshold account ("the push is real but needs to dominate the residual") predicts the effect finally registers?

**Decision it changes.** **KILL:** movement < 6 at ratios {1.5, 3.0} with the B_wrong OOD-control behaving per the instrument check → the threshold account dies entirely; the static family's inertness is deeper than strength at *every* coherent strength — the ultimate boundary statement, and the paper's wall gains its far side. **CONTINUE:** directional movement (flips ≥ 6, McNemar-exact p < 0.01, B_wrong flat) → the threshold account is vindicated; the license boundary was the whole story; the static family reopens above ratio 1 and the program's next lane is the >1 regime. **PIVOT:** both arms move together → OOD fragility, nonspecific; the >1 regime is decision-noise, not a mechanism.

**Cheapest falsifying test.** 60 EXP092-B items × 3 arms (B, T(ratio), B_wrong(ratio)) × 2 ratios {1.5, 3.0} = 360 passes, CPU, $0, reusing the EXP095 executor pattern (ratio = α·0.0474, so ratio 1.5 → α≈31.6, ratio 3.0 → α≈63.3 — computationally identical cost to the licensed sweeps). No new machinery.

**Mathematical license.** None from the linear license — that is the point; the design deliberately exits it. The threshold account's own prediction supplies the license: once ‖δ‖ dominates ‖r‖, first-order Δm ≈ α⟨∇m,d⟩ no longer binds and the response is set by the model's off-manifold behavior; a real directional push must register as decisions move. **Breaking point of the threshold account itself:** if nothing directional moves at ratio 3.0, no "stronger push" rescue remains coherent within static injection — beyond that the intervention replaces the representation rather than perturbing it.

**Quantitative prediction (pre-registered bars).** Per ratio: T-vs-B flips ≥ 6 AND McNemar-exact (doubling) p < 0.01 AND B_wrong flat (< 6 flips) AND ΔM_T > 0 → CONTINUE. T-vs-B flips < 6 at both ratios AND the instrument check passes → KILL.

**Feasibility algebra (EXP079 lesson) — the instrument check.** The genuine threat: at ratio 3.0 the residual is δ-dominated and the regime may be decision-frozen (nothing *can* move). Pre-registered: B_wrong must flip ≥ 1 item across the sweep, else the regime is declared decision-frozen → **Underdetermined**, never KILL. Companion fluency check: degenerate outputs (token repetition / collapse) on any arm → that ratio RUN-INVALID. The KILL is therefore never manufactured by a broken regime.

**The belief it tests [INTERPRETATION].** "The push is real but too weak" — overturned-by directional movement above ratio 1 (threshold vindicated), deepened-by a clean KILL (inertness is structural, not a strength artifact at any strength).

**Summit filter.** Honest: boundary science, not capability — but it completes the static-family map the paper needs (the wall's far side), which is the citable infrastructure everything else builds on.

**Top risks for Law #14.** (1) OOD-collapse confound — mitigated by the instrument check + fluency gate, but Law #14 must confirm the Underdetermined routing can't be gamed. (2) Is ratio 3.0 "replacing the representation"? — the packet's own breaking-point argument; Law #14 should rule whether 3.0 is still a perturbation. (3) Single-regime scope — a KILL here must be fenced to "static injection at all coherent strengths," never to dynamic mechanisms.

---

### S6-2 — Multi-layer composition: do two inert interventions compose into movement?

**Precise question [HYPOTHESIS].** Every verdict so far is single-layer. The scope fences explicitly kept multi-layer compositions alive. Do the individually-inert static interventions at L11 (task direction, killed) and a downstream layer L20 (the EXP077 layer — bridge/relational territory) compose into causal movement when co-injected?

**Decision it changes.** **KILL:** joint L11+L20 movement < 6 → composition doesn't rescue; inertness is compositional, closing the last static-combination degree of freedom. **CONTINUE:** joint flips ≥ 6 with McNemar p < 0.01 while both single-layer arms stay flat (< 6) → first compositional causal signal; the program's next lane is the multi-layer program (which pairs, which layers, interaction vs additive). **PIVOT:** single-layer arms move → the premise (individual inertness) was wrong at this bench/strength; re-derive before composing.

**Cheapest falsifying test.** 60 items × 5 arms (B, L11-only, L20-only, L11+L20 joint, B_wrong-joint at matched total norm) = 300 passes, CPU, $0. One downstream layer (L20 suggested default — precedent: EXP077; the prereg lane may argue L23/readout-adjacent instead).

**Mathematical license.** Superposition: if single-layer margin shifts Δm^(11), Δm^(20) are individually sub-threshold, the joint shift can cross the flip boundary additively — the test distinguishes additive crossing (joint flips ⊆ union of near-threshold single-layer items) from genuine interaction (joint flips on items neither arm nearly moved), via the per-item margin-shift ledger both verdicts' instrumentation already persists.

**Quantitative prediction.** Joint T-vs-B flips ≥ 6 AND p < 0.01 AND both single-layer arms < 6 flips AND B_wrong-joint flat → CONTINUE. Joint < 6 → KILL. Additive-vs-interaction decomposition reported regardless (it decides what a CONTINUE means).

**Breaking point.** If the joint norm must exceed ratio ~0.5 per layer to move anything, the design exits the linear license per-layer and becomes S6-1's question instead — pre-register the per-layer ratio cap (0.38, the EXP096 maximum) so the composition claim stays inside the license it tests.

**The belief it tests [INTERPRETATION].** "Inertness is a single-layer property" — overturned-by a compositional signal (the program goes multi-layer), deepened-by a compositional KILL (the wall extends to pairs).

**Summit filter.** Composition is a primitive any autonomous self-steering system needs (a self-steering model would compose interventions across layers). Boundary science with a compositional twist — honest.

**Top risks for Law #14.** (1) Layer choice (L20 vs readout-adjacent) — is the default principled or convenient? (2) The additive-vs-interaction decomposition must be pre-registered sharply, or a CONTINUE will be uninterpretable. (3) Per-layer direction construction needs its own degeneracy check (the d_i constructor is L11-specific).

---

### S6-3 — Dynamic attention-gated injection: the direction gated on the model's own live state

**Precise question [HYPOTHESIS].** EXP096's gate was static — precomputed from archived baseline margins. The verdicts explicitly kept *dynamic* mechanisms alive. Does the killed L11 direction move decisions when injection is gated on the model's own **live attention state** — injected only where the readout query attends to the entity span above a pre-registered threshold τ_attn?

**Decision it changes.** **KILL:** dynamically-gated movement < 6 → the direction is not "real but misapplied"; dynamic relevance-gating doesn't rescue it. **CONTINUE:** gated flips ≥ 6, p < 0.01, gated-B_wrong flat → first conditional causal signal at L11; the program's next lane is self-conditioned intervention. **PIVOT:** the gate fires on <10% of items (coverage collapse) → the mechanism is untestable in this form; or B_wrong moves with T → attentional fragility, nonspecific.

**Cheapest falsifying test.** 60 items × 3 arms (B, gated-T, gated-B_wrong under the identical live gate) ≈ 180 passes + attention-read overhead, CPU, $0. White-box forward pass; frozen weights; Δθ=0.

**Mathematical license.** Attention as relevance selection [CONJECTURE made testable]: the hypothesis is the task direction carries real content but static injection wastes it on inattentive positions; gating on live attention concentrates the perturbation where the readout actually draws entity information. The breaking point is τ_attn calibration — see risks.

**Quantitative prediction.** Gated T-vs-B flips ≥ 6 AND p < 0.01 AND gated-B_wrong < 6 flips AND gate coverage ≥ 10% of items → CONTINUE. Gated T < 6 with coverage ≥ 10% → KILL. Coverage < 10% → PIVOT (untestable form).

**The belief it tests [INTERPRETATION].** "The direction is real but statically misapplied" — overturned-by a gated signal, deepened-by a gated KILL (the conditional license narrows to truly dynamic mechanisms).

**Summit filter.** Strongest of the CPU lanes: self-conditioned intervention — the model gating its own perturbation by its own attentional state — is the closest CPU-testable primitive to autonomous steering. Honest about the distance remaining (externally computed gate, not self-computed).

**Top risks for Law #14.** (1) **τ_attn calibration is the load-bearing risk:** S3-1/S3-3's Stage-0 died because no archive carries per-layer attention snapshots — τ cannot be calibrated from archives; it must be pre-registered from a small live calibration battery or a principled constant (e.g., uniform-attention × k), with an in-run coverage tripwire (EXP096 §2.4 pattern). If Law #14 rules τ unprincipled, the design is unlicensable. (2) Implementation complexity — the attention-read must be proven non-perturbative (read-only hooks, verified by B-arm bit-agreement). (3) Is this "secretly EXP096"? — No: EXP096's gate was a static function of archived margins; this gate is a live function of the current forward pass. The prereg must state the distinction in one paragraph.

---

### S6-4 — Causal layer sweep: where else is information causal?

**Precise question [HYPOTHESIS].** EXP092 licensed l*=11 as the decode layer (information map); EXP093–096 killed causal influence at L11 (causal map: zero). Does task-direction injection move decisions at **other** layers — the decode curve's neighbors and the readout-adjacent layers?

**Decision it changes.** **KILL:** movement < 6 at every swept layer → the inertness generalizes beyond L11; the boundary law extends across the probed depth. **CONTINUE:** any layer with flips ≥ 6, McNemar p < 0.01 (Bonferroni over swept layers), B_wrong flat → causal locus found; the program pivots to that layer (per-item/dose-response program replays there). **PIVOT:** movement without directional significance → layer-specific fragility, not geometry.

**Cheapest falsifying test.** Phase 1: 2 layers (L8 — below the decode peak; L20 — the EXP077/bridge layer) × 60 items × 3 arms = 360 passes, CPU, $0. Phase 2 (licensed only if Phase 1 KILLs cleanly): extend to the readout-adjacent layer — separate pre-reg, never a silent extension.

**Mathematical license.** EXP092's decode sweep is the information map; the causal map is unmeasured elsewhere. The license is positional: causal influence of a representation is a function of where in the computational graph it is injected (downstream depth determines remaining transformation). Breaking point: layers where the task direction itself is degenerate (mean|cos| ≥ 0.95) are excluded by the degeneracy gate — never KILL on a powerless test.

**Quantitative prediction.** Per-layer bars mirror EXP095's (flips ≥ 6, p < 0.01 Bonferroni-over-layers, B_wrong flat, stratum consistency). All-layer < 6 → KILL.

**The belief it tests [INTERPRETATION].** "Inertness is an L11 property" — overturned-by a causal locus elsewhere, deepened-by cross-layer KILL (the wall gets taller).

**Summit filter.** Boundary science — mapping where (if anywhere) frozen geometry is causal is the prerequisite map for any steering program. Honest.

**Top risks for Law #14.** (1) Per-layer direction construction: the d_i constructor is L11-specific; each layer's direction needs its own frozen specification + degeneracy check — the prereg must not hand-wave this. (2) Multiplicity over layers — Bonferroni is the proposed correction; Law #14 may demand adjacent-layer replication instead. (3) Cost discipline — the 2-layer Phase 1 cap must be hard; "just one more layer" is how sweeps become fishing.

---

### S6-5 — Pooled power audit of the static-family kill battery (EXP093–EXP096) [$0, no pre-reg chain]

**Precise question [HYPOTHESIS].** S5-2 (LOG-4392) quantified the early static-geometry kills. What flip-rate does the **full** battery — EXP093, EXP094, EXP095 (5 α), EXP096 (gated) — actually rule out, per-arm and pooled?

**Decision it changes.** **KILL (of the skeptic's "small real effect"):** pooled exact 95% upper bounds tight (sub-1% on the pooled battery) → the paper's quantitative claims stand at the honest bound; the boundary law is numerically serious. **PIVOT:** any bound exceeds what the paper's language claims → re-rate the manuscript's language to the honest bound (falsification applied to our own licenses — the S5-2 precedent).

**Cheapest falsifying test.** $0: exact Clopper–Pearson / rule-of-three bounds from committed verdict statistics — zero new forwards. Dispatchable immediately; no pre-registration chain (analysis of committed artifacts, per S5-2's license).

**Mathematical license.** Exact binomial bounds on committed flip counts [FACT]. Breaking point: none — it is pure quantification; it cannot resurrect or kill any mechanism, only rate the claims.

**The belief it tests [INTERPRETATION].** "Static geometry is dead" as a *strong quantitative* claim — the audit decides whether the program's own license language is honest.

**Summit filter.** None directly — paper infrastructure. Still worth doing: it is the cheapest way to harden the manuscript's §3.

---

## Watchlist (not ranked — needs re-licensing or is a rider)

- **J1 κ̂-screen, CPU re-scoped (S4-4).** The backlog's "cheapest summit experiment" (re-entrant attractor dynamics) is GPU-queued, but the κ̂ contraction screen is ~40 passes — CPU-feasible in principle. Proposing it here only as a **venue-change candidate**: needs Law #14 + CEO re-licensing of venue before anything. Not ranked because the backlog explicitly sequences the J-series behind GPU lanes; unilaterally re-licensing venue is above this sprint's pay grade.
- **S3-7 instrumentation rider.** The spoiler-suppression question needs per-item top-5 token logs that no archive carries. Standing recommendation: attach the S3-7 instrumentation spec (top-5 token strings+ids+logits, baseline top-1 competitor identity, margin decomposition) to the **next CPU run's protocol** — whichever S6 candidate executes first carries the logging for free.
- **Relational decode follow-up (S5-3's open thread).** S5-3 closed entity-decodability 0/8; the relational-vs-neutral construct needs new support-set embeddings + new data collection + fresh prereg. Real work, real cost — parked until a CPU lane needs it or the GPU program frees capacity.

## What was NOT proposed and why

- **α=16 variant** — explicitly NOT licensed by the EXP096 verdict (both follow-up conditions failed). Proposing it would defy a binding verdict.
- **Any further static per-item L11 sweep** — barred by both verdicts. A proposal that is secretly another L11 sweep is a defect; none above is.
- **GPU lanes (K2, EXP083/084/086B/088/087, S3-1/S3-3 Stage-0b, J-series)** — untouched; parked on the founder's Kaggle per standing orders.

## Recommendation

**Green-light S6-1 first** (threshold breaking point → preregistration lane). It is the breaking point the program itself named in LOG-4391's license; it is the cheapest falsifying test of the last coherent static rescue; and both of its live outcomes are decisive for the paper (KILL → the wall's far side, the ultimate boundary statement; CONTINUE → the license boundary was the story and the >1 regime becomes the program). S6-5 (power audit) dispatches in parallel at $0 — no pre-reg chain needed. S6-2 follows on S6-1's verdict; S6-3 and S6-4 are queued behind, each needing its prereg lane when reached.
