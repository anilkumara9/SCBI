# Law #14 Adversarial Review — S6-3 Preregistration DRAFT v1 (2026-09-28)

**Reviewer:** independent Law #14 lane (fresh; did not draft any S6-3 material; no prior work on this artifact).
**Target:** `research/innovation/S6-3_PREREG_DRAFT_v1_2026-09-28.md` (DRAFT v1, UNSIGNED, 222 lines, 2026-09-28; logged LOG-4435). The draft file was **not edited** — review only.
**Verdict: ACCEPT-WITH-FIXES** — seven fixes (F1–F7) below. Two are substantive (F1: CONTINUE-reachability window + KILL evidential-weight accounting; F2: τ>1 edge case). Five are precision/citation repairs. No fix requires rebuilding the design; none alters a bar, gate value, or verdict mapping's intent. After repair: independent delta re-verification, then CEO clearance per the draft's §8.

**One-line reason:** the §4.2 algebra recomputes exactly, the license-by-difference clears LOG-4407 (verified against the EXP096 verdict's own "live lanes" text), the τ construction is licensable as a fail-safe heuristic — but the draft does not state that its licensed positive is mathematically unreachable below 13.3% coverage while declaring the design testable at 10% (F1), and the τ formalism permits an impossible firing condition it never bounds (F2).

---

## 1. Independent recomputation (§4.2 verification — from first principles)

All recomputed by this lane with exact arithmetic (pure-stdlib `math.comb`; script `/tmp/s63_law14_recompute.py`; no model, no weights, $0). **Every figure in the draft's §4.2 matches exactly.**

**McNemar minimum at α = 0.01 (doubling convention).** Exact two-sided p = 2·Σ_{i≥max(b,c)} C(b+c,i)·2^{-(b+c)}:
- b=0, c=7 → p = 2/128 = **0.015625**, n.s. (draft: 0.015625 n.s. ✓)
- b=0, c=8 → p = 2/256 = **0.0078125** < 0.01 ✓ (draft: 0.0078125 ✓)
- Conclusion: the discovery bar needs **≥8 directional flips** (b=0 case); the ≥6-flip movement gate is necessary-but-insufficient. Matches.

**Sensitivity floor:** 8/60 = **0.1333** → θ≈0.133 ✓ (draft: θ≈0.133).

**Noise specificity of the ≥6 movement gate:** P(X≥6 | N=60, θ=0.03) = **0.009144** → 0.0091 (draft: 0.0091, "<1% false-alarm" ✓); P(X<6) = 0.990856 → 0.9909 ✓.

**Spot-checks of draft-cited McNemar values (doubling):** b=0,c=6 → 0.03125 ✓ (EXP098 L20); b=1,c=3 → 0.625 ✓ (EXP099 L8); b=1,c=6 → 0.125 ✓ (EXP099 W20); b=1,c=0 → 1.0 ✓ (EXP099 W8); b=1,c=2 → 1.0 ✓ (EXP096 T). All consistent with the verdict reviews.

**New computations by this lane (not in the draft):**
- CONTINUE-reachability: flips can only occur on fired items, so the licensed positive (≥8 directional flips) requires F ≥ 8 fired items → coverage ≥ **13.3%**. The draft's coverage tripwire declares testability at ≥10% — the **[10%, 13.3%) window has the positive unreachable by construction** (see F1).
- KILL-at-floor weight: 0 flips on 6 fired items → exact one-sided 95% upper bound on the gated-conditional flip rate = **39.3%** (1−0.05^{1/6}). The draft's "flatness across 60 items" prose (see F1) overstates this.

---

## 2. Verdict: ACCEPT-WITH-FIXES — numbered fix list (minimal, precise)

### F1 (substantive) — CONTINUE-reachability window unstated; the KILL's evidential weight misaccounted at low coverage
**Defect.** §4.2 claims "Maximum achievable = 60 ≥ 8. No structural infeasibility" and "CONTINUE feasibility: needs ≥8 directional gated-T flips with the control flat — satisfiable under the hypothesis." But flips can only arise on fired items (unfired items contribute concordant pairs by deterministic copy, §2.1), so the licensed positive is **mathematically unreachable at coverage < 8/60 (13.3%)** — while §3 step 2b declares the design testable at coverage ≥ 10%. In the reachable window [10%, 13.3%), the only available verdicts are KILL / PIVOT / Underdetermined, and a KILL there rests on ~6–7 injected items (0/6 → 95% upper bound 39.3% on the gated-conditional flip rate, computed §1), not on "the test arm's flatness across 60 items" (§4.1 item 4's prose — the 54 structural concordant pairs are deterministic copies carrying no evidential weight). This is the EXP079 infeasibility class narrowed to a window: a bar unreachable by construction in a reachable world, undisclosed.
**Fix (minimal).** (a) §4.2: state the CONTINUE-reachability condition explicitly — the licensed positive requires F ≥ 8 fired items (coverage ≥ 13.3%); in the coverage window [10%, 8/60) the positive cannot fire by construction — name the window and its available routings (KILL if gated-T < 6 and gated-R sub-threshold and LIVE; PIVOT if gated-R ≥ 6; Underdetermined if FROZEN). (b) §4.1 item 4 and the §0 decision block: correct the KILL's evidential-weight prose to "the test arm's flatness across the *fired* items." (c) §4.2/§5: the verdict lane must report the coverage-conditioned sensitivity floor 8/F alongside 8/N_realized. No re-routing: the KILL in the window stays licensed (the alternative — Underdetermined-by-construction in a plausible world — is worse), but its weakness is now honestly accounted rather than rhetorically inflated.

### F2 (substantive, minor) — τ_i can exceed 1, making firing impossible by construction; unacknowledged
**Defect.** τ_i = 2·(E_i/N_i). If E_i/N_i > 0.5, then τ_i > 1 ≥ mass_i always → the item can never fire, a structural zero that dilutes coverage and can never contribute evidence. Step 0iii requires 1 ≤ E_i < N_i but never bounds the ratio; §0.2 never states the τ_i ≤ 1 operating condition.
**Fix (minimal).** Step 0iii: assert E_i/N_i ≤ 0.5 for all 60 items (violation → HOLD — the bench annotation is outside the gate's operating range). §0.2: note the τ_i ≤ 1 operating condition in one sentence.

### F3 — "Readout query" prose overstates the L11 attention read; the layer/aggregation choice needs its stated rationale
**Defect.** §0.2/§2.2 describe mass_i as "where the readout query attends to the entity span," but the read is at **layer 11 (mid-stack)**, not at the readout layer. At L11 the final token is not yet the readout query in the causal sense — the formalism (mass_i definition) is exact, but the prose mislabels the signal, and the draft's own §6-risk-1 sub-questions (mean- vs max-over-heads; L11 vs a later layer) are left as open attacks rather than answered design rationale.
**Fix (minimal).** Reword to "mid-stack (L11) attention from the final prompt token to the entity span"; add the frozen rationale in §2.2 in one to two sentences (the relevance signal is local to the injection layer — self-consistency: the hypothesis needs the *local computation at L11* to be entity-focused; mean-over-heads is the conservative relevance operationalization, pre-registered as the frozen choice). The hypothesis tested is unchanged; only the label is corrected.

### F4 — Citation error: EXP096's "3/60" should be "3/21"
**Defect.** §4.2 "KILL feasibility" says "EXP096's differently-gated T moved 3/60 at this ratio." EXP096 ran on **21** headroom-gated items (verdict review: "aimed at exactly the 21 items within calibrated reach"; "the task direction moved 3 items"). The denominator 60 is wrong.
**Fix (minimal).** "EXP096's differently-gated T moved 3/21 at this ratio."

### F5 — "Twice-uniform is standard" is uncited; the principled-vs-convenient adjudication
**Defect.** §0.2 calls twice-uniform "the standard 'concentration above chance' bar" with no citation. Twice-uniform is a conventional heuristic, not a cited standard.
**Fix (minimal).** Reword to "the conventional twice-uniform heuristic for concentration above chance" (or cite the standard). **Adjudication (binding):** τ = 2×-uniform is licensable as a *defensible pre-registered heuristic*, not as a strongly-principled constant. The license does not require strong principledness — it requires (i) no peeking surface (satisfied: closed-form, zero calibration data), (ii) fail-safe miscalibration (satisfied: §4.1 item 5 — too selective → step 2b PIVOT, never KILL/CONTINUE; too permissive → step 2c vacuous-gate flag, and the gate alone cannot manufacture the step-5 conjunction), (iii) the verdict never hinges on the constant (satisfied: τ miscalibration can produce PIVOT-untestable or a weak KILL, never a false CONTINUE — the asymmetry is falsification-first). The constant is load-bearing for *testability*, not *validity*, and testability failure is handled honestly. **Licensable as stated, with the wording corrected.**

### F6 — Step 4's "directional claim's refutation" observation is ambiguously scoped
**Defect.** The sentence "the directional claim's refutation is reported as an observation" closes step 4 covering both disjuncts. In disjunct (a) (gated-T ≥ 6 AND gated-R ≥ 6), the directional claim is *not* refuted — it is masked by matched-control fragility (the task arm may have moved directionally and significantly). Reporting "refutation" there would be false prose on a licensed verdict.
**Fix (minimal).** Scope the sentence to disjunct (b) explicitly: "(b) … → PIVOT (fragility — control-outmoves-task under the live gate); the directional claim's refutation is reported as an observation. In disjunct (a), no refutation is reported — a directional signal, if any, is uninterpretable under matched-control fragility."

### F7 — Step 2c's vacuous-gate caveat needs its exact weakened prose pre-registered
**Defect.** Step 2c: "the verdict remains licensed but the dynamic claim is weakened — disclosed, not hidden." At 100% coverage the executed experiment is *identical* to a static per-item L11 test at ratio 0.38 — the very family LOG-4407 unlicensed. The draft never states what the weakened verdict prose *is*, leaving room for post-hoc spin (a CONTINUE reported as "the first conditional causal signal at L11" when the gate did no conditioning).
**Fix (minimal).** Step 2c: pre-register the exact weakened prose, e.g. "CONTINUE (directional signal at ratio 0.38; gating unattributed — the gate was vacuous)," and require the verdict lane to use it verbatim when the caveat attaches. (Probability note: 100% coverage at 2×-uniform is unlikely — it would require every item's final token to concentrate twice-uniform mass on the entity span — but the pre-registration must cover it exactly.)

---

## 3. Per-section attack log (what I tried to break, what held, what broke)

**§0 / §0.1 — "secretly EXP096?" ATTACKED HARDEST. HELD — the distinction is real.**
- *Attack 1: is the attention gate re-expressible as a static function of the input?* On a frozen deterministic model, mass_i is *in principle* a function of the input tokens. But the license-relevant distinction is not metaphysical — it is operational: EXP096's gate was computable **without running the model** (precomputed from archived baseline margins, fixed across re-runs, blind to the forward pass); S6-3's gate is computed **from the model's live activations at execution time** and varies with the model's attentional state. More decisively, the *mechanism hypotheses* differ: EXP096 tested "inject where the model is uncertain" (margin headroom); S6-3 tests "inject where the model is attending" (attentional relevance). Different conditioning variable, different hypothesis. The draft's §0.1 states this correctly.
- *Attack 2: does LOG-4407's bar cover this anyway?* The bar's exact words (EXP096 verdict review): "**No further static per-item L11 experiments are licensed**." The same review explicitly reserves as live lanes: "**non-static conditional mechanisms (attention-state-gated, dynamic, multi-layer)**" — "Live lanes: gated/dynamic mechanisms … each requires its own pre-registration and Law #14 review." S6-3 is *named* by the bar's own reservation ("attention-state-gated"). The draft's "license by difference" is not a stretch — it is the bar's explicit carve-out. **CLEAR.**
- *Attack 3: the determinism angle.* §0.3's gate-determinism note is correct: the gate is deterministic but *novel* (never executed), so the first execution is the experiment, not a replication — no S6-4-style circularity. The pre-emptive disallowance of a "confirmation" framing for a second run is the right prophylaxis.
- **Adjudication: S6-3 is not secretly EXP096.** Different gate source (live activations vs archived margins), different conditioning variable (attentional relevance vs uncertainty headroom), different mechanism hypothesis — and the LOG-4407 bar explicitly reserves attention-state-gated mechanisms as live lanes.

**§0.2 — the τ construction. HELD as licensable heuristic, with F2/F5.** The no-peeking argument is airtight (closed-form, zero calibration data — the S3-1/S3-3 archive problem is sidestepped, not solved). The fail-safe analysis (§4.1 item 5, verified below) holds in every direction. The τ>1 edge case is F2; the "standard" claim is F5. The F5 adjudication above is binding: licensable.

**§0.3 — gate determinism. HELD.** Correct as analyzed above.

**§1 — background and license. HELD except F4.** Every cited number verified against the verdict reviews: EXP094 B=T=R=36/60, b=c=0, p=1.0, 0 flips (LOG-4375/4376/4377 — the draft cites the correct LOGs); EXP095 flips {0,0,0,1,1}, all p=1.0 (LOG-4400); EXP096 gated-T 3 flips (b=1,c=2,p=1.0), B_wrong 3 flips, ratio 0.3792, **21 items** (LOG-4407; the 3/60 denominator is F4); EXP097 ratios {1.5,3.0}, step 5a, PIVOT-fragility (LOG-4416); EXP098 L11-only 3 (p=1.0), L20-only 6 (b=0,c=6,p=0.03125, sub-bar) (LOG-4423); EXP099 L8-only 4 (p=0.625), W20 7, step-5(b) PIVOT-fragility named at L20 (LOG-4434 — verified against the verdict review); S6-5 pooled 5/381, one-sided 95% upper bound 2.74% (LOG-4409); degeneracy L11 0.7923, constructor hash `5e03f206…917f361`. The "strength precedent" argument (EXP096's 0.3792 under a different gate licenses attributing above-that movement to the gating rule) is valid as a *comparative* control; the residual confound (ungated 0.38 at L11 never tested) is named in §7 as unlicensed follow-up, not hidden — honest. The summit-filter honesty ("externally computed *from* the model's state, not *self-computed by* the model") is the right scope discipline.

**§2.1 — arms. HELD.** The 3-arm design (B / gated-T / gated-R under the identical live gate) is the correct minimal discriminant: the gated random control under the identical gate is EXP099's anti-lesson, applied. Norm-tie per fired item addresses the EXP096 double-scale bug class. The deterministic-copy rule for unfired items is exact for a frozen deterministic model (identical input + identical weights → identical output), and the run log asserts the firing vector and the copies. Fresh R seed distinct from prior streams ✓. The single-B design follows the S6-1 v2 precedent. 180 = 60 + 2×60 maximum ✓.

**§2.2 — the gate. HELD except F2/F3.** The formalism (mass_i, τ_i, fires_i ⟺ mass_i ≥ τ_i) is exact and frozen. The entity-span annotation assumption (step 0iii) is grounded: the EXP092-B bench construction carries per-item entity occurrence annotations via the real tokenizer's offset mapping (the G1′ family: 240/240 single-token in-prompt occurrences verified) — the "span" is the union of G1′-verified entity-occurrence token positions, and the draft should state this derivation explicitly (fold into F3's fix: one sentence). The "span excludes the final token" assertion is the right guard against gate/readout overlap.

**§2.3 — ratios. HELD.** Single point 0.38, bands [0.285, 0.475] = 0.38×(1±0.25) ✓; no grid, no interpolation — EXP097's lesson applied. The "one question per design" fence (not headroom-gated) is correct scoping.

**§2.4 — budget. HELD.** 180 + 60 = 240 expected ≤ 500 hard cap ✓; single-environment rule (Law #13) ✓.

**§2.5 — statistics. HELD.** One discovery contrast (gated-T-vs-B), ALPHA=0.01, no Bonferroni — stated, not hidden ✓ (no S6-4-F8 analog: the draft correctly says "one"). McNemar doubling with EXP094's (b=wrong→right, c=right→wrong) convention ✓. DELTA_BAR=0.10 program standard ✓. The ≥6 movement gate as necessary-but-insufficient is correct per §4.2. Stratum consistency carried verbatim from S6-4 v2 (attacked both directions in the S6-4 review and held) ✓. The McNemar on the full 60-pair set with unfired items as structural concordant pairs is *correct* (no injection → no possible flip) and conservative — but it is exactly what creates the F1 window (the bars operate on N=60 while the evidence lives on F fired items). The coverage tripwire (EXP096 §2.4 pattern) ✓. The liveness instrument's disclosed asymmetry is honest; its per-layer scope is correct here (single test layer — no S6-4-F3 analog). The B-agreement hook non-perturbation proof: adequate — read-only forward hooks are non-perturbative *by construction*, and step 0ii's 60/60 decision agreement is the behavioral backstop (a hook bug perturbing attention without moving any decision is possible in principle but would have to thread every item; the residual is Law #13's code-review territory, not a pre-registration defect — logged, not a fix).

**§3 — decision table. TWO DEFECTS: F1 (reachability accounting), F6/F7 (prose precision). Otherwise held — systematic first-match-wins audit:**
- Step 0: hash → B-agreement (doubles as hook proof) → annotation → degeneracy signature. Complete, correctly ordered ✓.
- Step 1: delivery probe on fired items only; ≤2 OOB per arm → exclude with count-bars on the post-exclusion set (the S6-4-F4 lesson already incorporated ✓); >2 → HOLD ✓.
- Step 2: (a) gate-source audit → HOLD ✓; (b) coverage < 10% → PIVOT before any verdict — a KILL is never manufactured from a collapsed gate ✓; (c) 100% → proceed with caveat (F7 sharpens the caveat's prose) ✓.
- Step 3: LIVE = (t≥1 OR r≥1); both-zero with coverage ≥ 10% → FROZEN → Underdetermined — never KILL from freeze-ambiguity ✓. Sanity gates route per-arm RUN-INVALID ✓.
- Step 4: (a) matched-control fragility (t≥6 AND r≥6) → PIVOT — the fragility veto over the positive is *intended* and correctly scoped to the **matched** control (no S6-4-F1 analog: gated-R is norm-tied per fired item under the identical gate) ✓; (b) control-outmoves-task (t<6 AND r≥6) → PIVOT ✓. Masking analysis: under the θ_noise=0.03 model, P(gated-R ≥ 6) = 0.0091 < 1% — a true directional effect is masked with <1% probability under the noise model; the residual (gate selecting perturbable items) is the program's standing fragility doctrine (EXP097/EXP099), correctly applied. The observation-scoping is F6.
- Step 5: the full conjunction (≥6 AND p<0.01 AND gated-R flat AND stratum-consistent AND coverage ≥ 10%) is the correct licensed-positive shape; no conjunct alone licenses anything ✓.
- Step 6: KILL fenced to "attention-gated per-item L11 injection at ratio 0.38 on EXP092-B" — correctly narrow, never to "all dynamic mechanisms" ✓; fires only with controls sub-threshold, keeping its prose honest against the fragile world (no S6-4-F9 analog — step 4b already claims the control-outmoves-task world) ✓.
- Step 7: named sub-cases are the right catch-all ✓.
- Five permitted verdicts with step→verdict mappings; no banned language ✓. Scope fence complete ✓.

**§4.1 — degeneracy analysis. HELD, with the F1 correction to item 4's prose.** Item-by-item: (1) McNemar on b=c=0 → p=1.0, fails safe toward KILL ✓ (adversarial b=60,c=0 → 2/2^60 ≈ 1.73×10⁻¹⁸ — recomputed ✓). (2) ΔM zero-variance → 0, cannot clear 0.10 ✓. (3) Flip-rate → 0 ✓. (4) Liveness — the disclosed asymmetry is honest; **but** "the KILL's weight is the test arm's flatness across 60 items" is false at low coverage (F1b). (5) Coverage tripwire — the load-bearing analysis: degenerate uniform attention → 0% → PIVOT ✓; adversarial fire-everywhere → 100% → vacuous flag with the step-5 conjunction still required ✓; fires-nowhere → step 2b short-circuits before step 6, cannot manufacture KILL ✓. Fails safe in every direction ✓. (6) Gate-source audit → HOLD ✓. (7) B-agreement hook check — fails safe toward HOLD in both degenerate and adversarial inputs ✓ (see §2.5 note on the residual). (8) gated-R flatness — the neutralization analysis (a)/(b) is correct; CONTINUE requires the full conjunction ✓. (9) Stratum consistency — correct as carried ✓.

**§4.2 — probe-feasibility + power. HELD except F1/F4.** Every number recomputed exactly (§1 of this review). The low-coverage asymmetry is *declared* (falsification-first direction ✓), but the [10%, 13.3%) unreachability window is not (F1a). The sensitivity floor 8/N_realized reporting must be joined by 8/F (F1c). The "EXP096 3/60" denominator is F4.

**§4.3 — verdict discipline. HELD.** Evaluation order frozen pre-run, no post-hoc table edits, design-change→new-number rule, gate integrity evaluated before regime routing and never re-routed, tripwire never re-thresholded ✓.

**§5 — instrumentation. HELD.** All nine items persist what the table needs; the gate audit trail (`per_item_gate.csv` with mass_i, τ_i, fired + hook-source assertion) is the right evidentiary basis for steps 2a/2b; the S3-7 rider ("no analysis pre-registered") matches the LOG-4408 watchlist ✓. Add F1c's 8/F to the worksheet's required fields.

**§6 — known design risks. HELD — the self-attack list is genuine.** Risk 1 (τ principled?): adjudicated in F5 — licensable as fail-safe heuristic. Risk 2 (secretly EXP096?): adjudicated above — the distinction holds. Risk 3 (low-coverage KILL-favoring asymmetry): declared honestly; F1 completes the disclosure. Risk 4 (gate-from-B leakage): the no-leakage argument is correct — the gate uses no label, no margin, no outcome, only the attention distribution (the model's state, not the answer), and the identical gate applies to the random control; Law #7 is about label/target leakage, and none is present. **Confirmed explicitly as requested.** Risk 5 (strength confound): the EXP096 comparison is an adequate *comparative* control; the residual is named, not hidden. Risk 6 (vacuous gate): F7 sharpens the caveat. Risk 7 (ungated α=8.0): correctly fenced as follow-up, not smuggled in.

**§7/§8 — scope and next steps. HELD.** The no-pilot, no-GPU, no-signed-artifact discipline is stated and complete; the single-lane fence is honored (this review confirms the drafting lane did not self-review — the review is this separate lane).

---

## 4. License adjudication (binding questions)

**(a) Does S6-3 clear LOG-4407's "no further static per-item L11 experiments licensed"? YES — clearly, and by the bar's own carve-out.**
LOG-4407's bar is L11-and-static scoped. The EXP096 verdict review — the bar's own source — explicitly reserves as live lanes "**non-static conditional mechanisms (attention-state-gated, dynamic, multi-layer)**," each requiring its own pre-registration and Law #14 review. S6-3's gate is a live function of the current forward pass's activations (not a static function of archived margins), testing a different mechanism hypothesis (attentional relevance vs uncertainty headroom). **CLEAR.**

**(b) Is the τ_attn construction licensable? YES — as a fail-safe pre-registered heuristic (F5 adjudication).**
The three license conditions (no peeking surface; fail-safe miscalibration; the constant cannot manufacture a verdict) are all satisfied. A miscalibrated τ can produce PIVOT-untestable or a weak KILL — never a false CONTINUE. The load-bearing joint holds.

---

## 5. What was checked and held (no fix)

The §4.2 McNemar/power/specificity algebra (recomputed exactly); all number citations to LOG-4400/4407/4409/4416/4423/4429/4432/4434, the EXP094–099 verdict reviews, the frozen archives (degeneracy 0.7923, constructor hash), and EXP093's signed pre-reg conventions; the 3-arm gated design; the identical-gate matched random control (EXP099's anti-lesson applied); norm-tie per fired item; fresh R seed; the deterministic-copy rule; the single-ratio/no-grid/no-interpolation fences; the fragility PIVOT routes (matched-control scoping correct — no shadowing defect); the licensed-positive conjunction; the KILL's narrow fencing; the no-leakage (Law #7) argument — confirmed explicitly; the CPU-only $0 / no-GPU / Δθ=0 guards; the S3-7 rider; the scope fences; the single-lane fence.

---

*Review completed 2026-09-28 by the independent Law #14 lane. Verdict: **ACCEPT-WITH-FIXES** (F1–F7). The draft file was not modified. Next: repair lane applies F1–F7 → independent delta re-verification → CEO execution clearance. No pilot authorized.*
