# Law #14 Adversarial Review — S6-3c Preregistration DRAFT v1 (2026-09-28)

**Reviewer:** independent Law #14 lane (fresh; did not draft any S6-3c material; no prior work on this artifact).
**Target:** `research/innovation/S6-3c_PREREG_DRAFT_v1_2026-09-28.md` (DRAFT v1, UNSIGNED, 238 lines, 2026-09-28; logged LOG-4449). The draft file was **not edited** — review only.
**Verdict: ACCEPT-WITH-FIXES** — two fixes (F1–F2) below, both precision/fence repairs. Neither requires rebuilding the design; neither alters a bar, gate value, aggregation, read layer, or verdict mapping's intent. After repair: independent delta re-verification, then CEO clearance per the draft's §8.

**One-line reason:** the §4.2 algebra recomputes exactly, the no-peeking bright line holds under the hardest attack (no L20 attention masses exist anywhere in the program record — verified by search, not asserted), the F5 τ adjudication carries intact for the new read layer, and all S6-3/S6-3b lessons are present — but the draft's new Law #7 readout-proximity surface needs an explicit checkable fence (F1), and one descriptive off-by-one needs correcting (F2).

---

## 1. Independent recomputation (§4.2 verification — from first principles)

All recomputed by this lane with exact arithmetic (pure-stdlib `math.comb`; no model, no weights, $0). **Every figure in the draft's §4.2 matches exactly.**

- **McNemar minimum at α = 0.01 (doubling):** b=0, c=8 → p = 2/256 = **0.0078125** < 0.01 ✓; b=0, c=7 → p = 2/128 = **0.015625**, n.s. ✓. The ≥8-directional-flip discovery bar stands.
- **Noise specificity:** P(X≥6 | N=60, θ=0.03) = **0.0091** ✓ (recomputed 0.00914398… → 0.0091).
- **KILL-at-floor weight:** 0/6 → exact one-sided 95% upper bound = 1 − 0.05^{1/6} = **0.3930 → 39.3%** ✓.
- **Sensitivity floor:** 8/60 = **0.1333** ✓.
- **F2 operating condition re-proof for the L20 read (checked, not rubber-stamped):** mass_i^{L20,mean} = (1/H)·Σ_h Σ_{t∈span} A^{(20,h)}_i[q_i→t]; each head's weights sum to 1 over all tokens, so each head's span-mass ≤ 1, hence the mean over heads ≤ 1 always. τ_i ≤ 1 ⟺ 2·E_i/N_i ≤ 1 ⟺ E_i/N_i ≤ 0.5 — identical to S6-3/S6-3b. The re-proof is valid; the layer change moves nothing about the operating condition. The layer-independence claim in §4.2 is true. ✓
- **Spot-checks of cited values against their sources:** EXP100 masses [0.0396, 0.0746] vs τ [0.2286, 0.2759] ✓ (EXP100 verdict §1); EXP101 16/60=26.7%, gated-T 1 flip (b=0,c=1,p=1.0), gated-R 0 flips, ΔM −0.0236 (protocol definition), seed 311019, 159 passes (92 experiment), 44 unfired copied ✓ (EXP101 verdict §1); EXP098 L20-only 6 flips (b=0,c=6,p=0.03125, sub-bar) ✓ (LOG-4423); EXP099 L8-only 4 flips (p=0.625), W20 7 flips ✓ (LOG-4429/4434); EXP095 {0,0,0,1,1} ✓; EXP096 3/21 at 0.3792 ✓ (F4 carried — the draft writes "3/21"); EXP094 B=T=R=36/60, degeneracy 0.7923 ✓; S6-5 5/381 → 2.74% ✓; constructor hash `5e03f206…917f361` ✓; bench pin `9be8162633fe19aa…` ✓. **No invented numbers found.**

---

## 2. The two re-opened questions — binding adjudications

LOG-4448 (EXP101 verdict) explicitly re-opened "the τ-principledness and no-peeking questions" for any re-gating, "requiring its own pre-registration and Law #14 review." This review answers both. Both HOLD.

### 2a. No-peeking — HOLDS (attacked hardest)

**The attack.** The draft chose L20 knowing EXP098's L20-only movement record, and chose mean-over-heads in the new layer space. Is the layer choice outcome-tuned — "the layer that moved before," i.e. outcome-tuning with extra steps? And is "conservative-first" a principled ordering or a guess laundering a second predictable collapse?

**What I verified:**
1. **τ is byte-identical to the adjudicated constant.** τ_i = 2·(E_i/N_i) appears throughout exactly as in S6-3 v2 / S6-3b v2; the draft never calls it "standard" (F5 wording carried — only "program standard" appears, for the movement gate). No numeric threshold moved.
2. **No L20 attention masses exist anywhere in the program record.** Searched `experiments/runs/` and `research/innovation/` (excluding the S6-3c draft itself) for L20 attention-mass quantities: zero hits. EXP100's gate CSV has columns `(item_id,E,N,mass,tau,fired,gate_source)`; EXP101's has `(item_id,E,N,mass_max,mass_mean,tau,fired,firing_rule,gate_source)` — all L11 quantities. The draft's bright-line factual claim ("no L20 attention masses have been observed anywhere in this program's record") is verified true, not asserted.
3. **The EXP101 verdict itself prescribed this move.** LOG-4448's next-licensed-question names "a later-layer relevance read, e.g. the reserved S6-3c candidate" as requiring "fresh pre-registration and Law #14 review." The choice is the verdict's own prescription, not smuggled in.
4. **The layer choice is from the license record, not from any attention measurement.** EXP098's L20 observation is a *movement* observation (6 flips, sub-bar), not a gate-calibration measurement — no S6-3c parameter is a function of any attention mass. The "conservative-first" ordering (mean before max in the new space) applies LOG-4443's endorsed principle (conservative mean first, permissive max second — "disciplined exhaustion") to the new hypothesis space; it is a stated convention, and max-at-L20 is named as the S6-3d candidate rather than smuggled in.

**The honest residual (the draft states it in §6 risk #5; I confirm it).** Had EXP098's L20 shown 0 flips, L20 would not have been chosen — the *research direction* is outcome-informed. That is not peeking. Peeking is outcome-dependence of *design parameters*; the license standard is the absence of a tuning surface, not the chooser's ignorance (LOG-4443's binding adjudication). There is no tuning surface here: the constant didn't move, the layer and aggregation are discrete pre-registered choices, and the firing rule is closed-form.

**On the "second predictable collapse" attack (§6 risk #4):** the draft's counter — the L11 record does not transfer to L20 because attention distributions shift across layers, and L20-mean masses are unobserved — is a reasonable prior but unproven for this model/bench. It does not need to be proven: the tripwire handles a collapse honestly (step 2b PIVOT), and the draft discloses the possibility rather than promising firing. Not a defect; recorded.

**Adjudication (binding): motivation-by-observation is distinguished from calibration-by-observation. The no-peeking bright line HOLDS.** The draft's §0.2 bright-line statement is verified true: no parameter is a function of any EXP094–101 measurement.

### 2b. τ-principledness — HOLDS (F5 carried, layer change does not re-open it)

The F5 binding adjudication (LOG-4436) licensed τ = 2×-uniform as a fail-safe pre-registered heuristic under three conditions: (i) no peeking surface, (ii) fail-safe miscalibration, (iii) the verdict never hinges on the constant. All three re-verified for the L20 read (§6 risk #6 states them explicitly): (i) the constant is unchanged and closed-form and §2a holds; (ii) too selective → step 2b PIVOT, too permissive → step 2c vacuous-gate flag, and the gate alone cannot manufacture the step-5 conjunction; (iii) miscalibration yields PIVOT-untestable or a weak KILL, never a false CONTINUE. The layer change moves the *read locus*, not the constant — the principledness fight about the number stays settled.

**Adjudication (binding): τ remains licensable as a fail-safe pre-registered heuristic under the L20 read. The "why this layer" question is answered by §2a, not by re-litigating the constant.**

---

## 3. Verdict: ACCEPT-WITH-FIXES — numbered fix list (minimal, precise)

### F1 (new attack surface) — the Law #7 readout-proximity risk needs a checkable fence
**Defect.** §6 risks #1–2 honestly flag the lead risk — L20's readout-adjacency means the gate may behave as a near-decision proxy — and ask Law #14 to rule. The ruling (see §4, attack 3): the *statistical* no-leakage argument holds (the identical-gate matched control symmetrizes any subset-level confound, including answer-correlation — defense (b) is layer-independent and decisive). But the *interpretive* residual is real: if the gate fires mostly where B is already correct, a CONTINUE's prose ("conditional causal signal under L20 attentional relevance") would be checkably ambiguous between relevance-gating and decision-proxy evidence — and the verdict lane currently has no licensed vocabulary to report which world it is in. The program's F2 precedent (S6-3b) is to fence new attack surfaces explicitly rather than rely on honesty alone.
**Fix (minimal).** In §5 item 8 (decision-table worksheet), add: "The worksheet reports B-arm accuracy on fired items and on unfired items separately (both computable from per_item_records.csv; descriptive only — no verdict, bar, or routing consequence is pre-registered for this split)." In §4.3 verdict discipline, add: "The fired-vs-unfired B-accuracy split is the decision-proxy audit for the Law #7 readout-proximity risk (§6 risks #1–2): it is reported descriptively so the verdict lane can state whether the gate behaved as a near-decision proxy; it does not alter any step's routing." No other change. (No new passes, no new columns — both quantities come from pre-registered records; the audit cannot manufacture or block any verdict.)

### F2 (descriptive precision) — off-by-one in the readout-adjacency prose
**Defect.** §0.2 leg 2 (line 38): "L20 sits 4 blocks below the final block." The draft's own rejected-alternatives list names "L23 (final block)" — under the program's 0-indexed convention, L20 is 3 blocks below L23 (21, 22, 23), not 4. Descriptive only; no parameter depends on it.
**Fix (minimal).** Change "4 blocks below" to "3 blocks below" (one word). No other change.

---

## 4. Per-attack log (what I tried to break, what held, what broke)

**Attack 1 — the layer question (not "secretly S6-3b").** HELD. S6-3/S6-3b read relevance at the injection layer (self-consistency); S6-3c reads it at a readout-adjacent layer while injecting at L11. The gate's *source* and the relevance claim's *locus* both change — a genuinely different mechanism claim ("the model's later, decision-shaping attention state is the right relevance signal"), not a re-aggregation. The dropped F3 self-consistency rationale is explicitly replaced (not silently): the new rationale — readout-adjacent relevance — is a real rationale change (it changes what counts as evidence and why), honestly disclosed as weaker-motivated than self-consistency. Less-principled is not unlicensable, and the draft does not hide the trade. The LOG-4407 bar is re-cleared by the unchanged carve-out: the bar bans *static* per-item L11 experiments; the L20 mean-gate is a live function of the current forward pass's activations (computed from the B pass via read-only hooks) — the carve-out operates at the gating-mechanism level, which is dynamic here. **CLEAR.**

**Attack 2 — no-peeking.** ATTACKED HARDEST. HELD — see §2a. Four legs verified: byte-identical constant ✓; zero L20 attention masses in the record (searched, not asserted) ✓; the verdict's own prescription (LOG-4448) ✓; layer from the license record, not from measurements ✓. The "conservative-first" ordering is a stated convention applied from LOG-4443's endorsed principle, with max-at-L20 named (S6-3d) rather than smuggled. The honest residual (direction outcome-informed) is distinguished from peeking per the binding LOG-4443 standard.

**Attack 3 — Law #7 readout-proximity.** STATISTICAL ARGUMENT HELD; INTERPRETIVE RESIDUAL FENCED → F1. Defenses attacked in turn: (a) gate sees no label/margin/decision — true, and necessary but not sufficient alone; (b) identical gate on the matched random control — **decisive and layer-independent**: both arms face the identical fired subset by construction, so any subset-level confound (answer-correlation included) is symmetrized; a CONTINUE still requires task-geometry-specific movement (≥6 directional flips, p<0.01) with the control flat — the EXP099 anti-lesson applied; (c) gate fixed from the frozen B pass before any injection — true, rules out adaptive selection; (d) strata pinned — true, rules out post-hoc re-routing. The McNemar doubling convention and stratum-consistency definition both survive answer-correlated subsets (directionality remains testable). What (a)–(d) do not settle is the *interpretation* of a CONTINUE under a near-decision-proxy gate — hence F1's descriptive audit, which gives the verdict lane the licensed vocabulary to report it. The KILL and PIVOT interpretations are unaffected (a KILL under an answer-correlated gate is *stronger* evidence, not weaker).

**Attack 4 — §4.2 algebra.** RECOMPUTED EXACTLY — see §1. No discrepancies.

**Attack 5 — carried lessons.** VERIFIED ITEM-BY-ITEM:
- F1: reachability window [10%, 8/60) with routings (§0 decision block, §4.2) ✓; "flatness across the *fired* items" ✓; 8/F alongside 8/N_realized (§4.2, §5 item 8) ✓.
- F2: re-proved for the L20 read (§4.2 — validity checked in §1 above); step 0iii asserts E_i/N_i ≤ 0.5 ✓.
- F3: "readout query" and "decision attention" appear only inside the prohibition sentences ("never 'readout query,' never 'decision attention'") — the discipline holds ✓; the read is "later-layer (L20) attention from the final prompt token" throughout ✓.
- F4: "EXP096's differently-gated T moved 3/21 at this ratio" ✓.
- F5: "standard" never modifies twice-uniform (only "program standard" for the movement gate) ✓; the three-condition re-verification is explicit (§6 risk #6) ✓.
- F6: disjunct (b) keeps "the directional claim's refutation is reported as an observation"; disjunct (a) explicitly reports no refutation ✓.
- F7: step 2c pre-registers "CONTINUE (directional signal at ratio 0.38; gating unattributed — the gate was vacuous)." verbatim ✓.
- Also carried: matched random control under the identical L20 gate with per-fired-item norm ties ✓; step-2b tripwire before any verdict (never KILL from a collapsed gate) ✓; first-match-wins steps 0–8 ✓; single ratio 0.38, no grid, no interpolation ✓; CPU-only $0, Δθ=0, no GPU ✓; fresh-seed-distinctness convention (no numeric value in the draft — the S6-3b convention) ✓; deterministic-copy rule ✓; S3-7 rider ✓.
- S6-3b F2-class fence: §2.2 deliberately persists **no** extra attention columns ("No extra audit columns"); §5 item 1 persists only the gate's own mass_i^{L20,mean}; §5 item 2's gate CSV has no non-gate attention column; §4.3 carries the verbatim "no non-gate attention quantity" fence ✓. The attack surface stays closed.

**Attack 6 — "LAST externally-computed attention-gate variant" fence.** HELD, with a noted residual. The discrete space {mean, max} × {L11, L20} is exhausted by licensed, discrete choices: mean/max exhaust the natural head-aggregations (S6-3b's binding adjudication), and L11/L20 are the two layers with any license record (injection layer; the only later-than-L11 layer with a movement record — L8's record is *earlier* than L11, hence a different hypothesis). Naming S6-3d (max-at-L20) as an unlicensed *candidate* requiring its own pre-registration and review is explicit sequencing, not a hidden hop — §7's "does not license" list and breaking point (iv) agree. Residual (not a defect): the layer-exhaustion argument is thinner than the aggregation-exhaustion argument (it rests on the license record, not on a closed discrete space); the draft is honest about this. Recorded.

**Attack 7 — invented numbers.** NONE FOUND — see §1 spot-checks. Every cited value traces to LOG-4400/4407/4409/4416/4423/4429/4432/4434/4440/4441/4447/4448, the EXP094–101 verdict reviews, or the frozen archives. The "4 blocks" prose (F2) is the only factual imprecision found, and it is descriptive, not numeric-parameter.

**Section sweep — additional notes:**
- §0 decision block: KILL/CONTINUE/PIVOT routings complete; the belief under test is named ("the direction is real but the relevance read was at the wrong layer") ✓.
- §0.3 gate-determinism: correct; the second-run "confirmation" prophylaxis is the right guard against an S6-4-style obstruction ✓.
- §2.1 arms: 3-arm design with identical live L20 mean-gate on gated-R is EXP099's anti-lesson applied ✓; injection anchored to baseline L11 norms (the injection layer is unchanged — only the gate's read layer moved) ✓; 180 = 60+60+60 maximum ✓.
- §3 decision table: systematic first-match-wins audit — steps 0, 1, 2a/2b/2c, 3, 4a/4b, 5, 6, 7 all correctly ordered and scoped; the F1 window language, F6 scoping, and F7 verbatim prose all present ✓. Step 6's KILL is fenced to "L20-mean-gated per-item L11 injection at ratio 0.38 on EXP092-B — never to 'all dynamic mechanisms,' 'all layers,' or 'all aggregations'" — the correct anti-double-kill ✓.
- §4.1 degeneracy analyses: all nine items fail safe; item 5's L20 degenerate case (uniform attention → mass^{L20,mean} = E/N < 2E/N → 0% → 2b PIVOT) recomputed correct ✓; item 7's adversarial input (hooks disabled → no L20 masses → step 0iii/2a HOLD) is the right trap ✓.
- §4.3 verdict discipline: evaluation order frozen, tripwire un-rethresholdable, read layer un-changeable, aggregation un-re-choosable ✓.
- §6 risks: genuine self-attack list; risks #1–2 correctly identified as the most likely fatal ones (adjudicated in §4 attack 3) ✓; risk #4's "laundering a collapse" attack is answered honestly (recorded in §2a) ✓.
- §7/§8: no-pilot, no-GPU, no experiment number minted, single-lane-fence discipline complete ✓.

---

## 5. License adjudication (binding questions)

**(a) Does S6-3c clear LOG-4407's "no further static per-item L11 experiments licensed"? YES — by the same carve-out that licensed S6-3/S6-3b, unchanged.** The bar bans static experiments; the L20 mean-gate is a live function of the current forward pass's activations. The read layer is not the injection layer — the carve-out operates at the gating-mechanism level, which is dynamic here. **CLEAR.**

**(b) Is the later-layer re-gating licensable without a peeking surface? YES — §2a.** The threshold is the adjudicated constant, byte-identical; the layer and aggregation are discrete choices among verdict-named, license-record alternatives; no parameter is a function of any EXP094–101 measurement (verified: no L20 attention masses exist anywhere in the record). **LICENSED.**

**(c) Is the "last externally-computed attention-gate variant" fence principled? YES — §4 attack 6.** {mean, max} × {L11, L20} exhausts the licensed discrete choices; further moves (other layers, other aggregations, new threshold families, self-computed gates) each need their own pre-registration and review. S6-3d is a named unlicensed candidate, not a hidden hop. **PRINCIPLED** (subject to F2's prose repair; residual noted in §4).

---

## 6. What was checked and held (no fix)

The §4.2 McNemar/power/specificity algebra (recomputed exactly); the F2 operating-condition re-proof for the L20 read (re-derived, not trusted — the layer-independence claim is true); all number citations to LOG-4400/4407/4409/4416/4423/4429/4432/4434/4440/4441/4447/4448, the EXP094–101 verdict reviews, and the frozen archives; the no-peeking bright line (verified by searching the actual record for L20 attention masses — zero hits — and against the EXP101 verdict text); the carried F5 τ adjudication; the 3-arm L20-mean-gated design with the identical-gate matched random control; per-fired-item norm ties; the fresh-seed-distinctness convention; the deterministic-copy rule; the single-ratio/no-grid/no-interpolation fences; the fragility PIVOT routes with correct matched-control scoping; the licensed-positive conjunction; the KILL's narrow fencing; the Law #7 no-leakage argument at the statistical level (defense (b) is layer-independent — confirmed again as the draft requested); the coverage tripwire and step-2b-before-verdict ordering; the S6-3b F2-class fence (no extra attention columns — verified in §5); the CPU-only $0 / no-GPU / Δθ=0 guards; the S3-7 rider; the scope fences; the single-lane fence.

---

*Review completed 2026-09-28 by the independent Law #14 lane. Verdict: **ACCEPT-WITH-FIXES** (F1–F2). The draft file was not modified. Next: repair lane applies F1–F2 → independent delta re-verification → CEO execution clearance. No pilot authorized.*
