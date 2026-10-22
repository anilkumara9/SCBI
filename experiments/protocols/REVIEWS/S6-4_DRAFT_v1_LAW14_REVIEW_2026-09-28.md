# Law #14 Adversarial Review — S6-4 Preregistration DRAFT v1 (2026-09-28)

**Reviewer:** independent Law #14 lane (fresh; did not draft, repair, or verify any S6-4 material; no prior work on this artifact).
**Target:** `research/innovation/S6-4_PREREG_DRAFT_2026-09-28.md` (DRAFT v1, UNSIGNED, 2026-09-28). The draft file was **not edited** — review only.
**Verdict: ACCEPT-WITH-FIXES** — nine fixes (F1–F9) below. Three are substantive decision-table defects (F1 shadowing, F2 ordering, F3 liveness scope); six are precision/citation repairs. No fix requires rebuilding the design; none alters a bar, gate value, or verdict mapping's intent. After repair: independent delta re-verification, then CEO clearance per the draft's §8.

**One-line reason:** the determinism obstruction (§0.1) is correct, the power algebra recomputes exactly, and both license bars clear — but the decision table has three genuine defects: an unmatched fragility clause that can shadow the licensed L8 positive (F1), a regime-routing order that masks a pipeline-change HOLD (F2), and a global liveness instrument licensing a per-layer KILL (F3).

---

## 1. Independent recomputation (§4.2 verification — from first principles)

All recomputed by this lane with exact binomial arithmetic (pure-stdlib `math.comb`; script `/tmp/s64_law14_recompute.py`; no model, no weights, $0). **Every figure in the draft's §4.2 matches exactly.**

**McNemar minimum at per-layer α = 0.005 (doubling convention).** Exact two-sided p = 2·Σ_{i≥max(b,c)} C(b+c,i)·2^{-(b+c)}:
- b=0, c=8 → p = 2/256 = **0.0078125**, n.s. (draft: 0.0078125 n.s. ✓)
- b=0, c=9 → p = 2/512 = **0.00390625** < 0.005 ✓ (draft: 0.00390625 ✓)
- Conclusion: the discovery bar needs **≥9 directional flips** (b=0 case); the ≥6 movement gate is necessary-but-insufficient. Matches.

**L20 confirm-or-kill power (exact binomial, need ≥9 flips at the p<0.005 bar):**
| N | θ | P(X≥9) recomputed | draft |
|---|---|---|---|
| 60 | 0.10 | **0.141636** → 0.142 | 0.142 ✓ |
| 115 | 0.10 | **0.823459** → 0.823 | 0.823 ✓ |
| 60 | 0.07 | **0.023137** → 0.023 | 0.023 ✓ |
| 115 | 0.07 | **0.414629** → 0.415 | 0.415 ✓ |

**Noise specificity of the ≥6 movement gate:** P(X≥6 | N=60, θ=0.03) = **0.009144** → 0.0091 (draft: 0.0091, "<1% false-alarm" ✓); P(X<6) = 0.990856 → 0.9909 ✓.

**Clopper–Pearson 95% interval on the observed 6/60:** solved the defining equations P(X≥6|p=L)=0.025 and P(X≤6|p=U)=0.025 by bisection (300 iterations; sf increasing / cdf decreasing in p — an earlier bisection in my scratch script had the monotonicity flipped and converged degenerately; corrected and re-verified): θ ∈ **[0.0376, 0.2051]** (draft: [0.0376, 0.2051] ✓).

**Sensitivity floor:** 9/60 = **0.15** ✓ (draft: θ≈0.15).

**Spot-checks of cited McNemar values (doubling):** b=0,c=6 → 0.03125 ✓ (EXP098 L20); b=1,c=2 → 1.0 ✓ (EXP096); b=3,c=9 → 0.1460 ✓ (EXP098 W-joint); b=6,c=7 → 1.0 ✓. All consistent with the verdict reviews.

---

## 2. Verdict: ACCEPT-WITH-FIXES — numbered fix list (minimal, precise)

### F1 (substantive) — Step 5's unmatched W20-fragility clause shadows the licensed L8 positive
**Defect.** Step 5 fires PIVOT on `(W20 flips ≥ 6)` **alone**, ahead of step 6 in first-match-wins order. Reachable state: L8-only ≥ 6 flips with McNemar p < 0.005, W8 flat (<6, |ΔM|<0.10), strata consistent (step 6's full CONTINUE conjunct holds) **and** W20 ≥ 6 → the draft routes to PIVOT (fragility) instead of CONTINUE. W20 is **not** the matched control for L8-only (W8 is); the draft's own §2.4 defines W-flatness per matched arm. An L20-regime fragility observation vetoing an L8 discovery is unmatched-control cross-contamination. The bracket's rationale — "L20-only is deterministically 6 per the anchor, so fresh-randomness W20 ≥ 6 completes the fragility pattern" — treats the anchor's *expected-by-construction* sub-bar reproduction as the task-side of a fragility pattern, which is conceptually muddled (EXP097's fragility pattern was task-vs-matched-control, both measured).
**Fix (minimal).** Scope step 5 to the matched disjunct: `(L8-only flips ≥ 6 AND W8 flips ≥ 6) → PIVOT (fragility)`. Move the W20 ≥ 6-alone clause to a post-step-6 caveat: evaluate step 6's conjunct first; if it holds → **CONTINUE with a named "L20 fragile-regime caveat"** (W20 ≥ 6 — the L20 layer is in the fragility regime; the anchor's sub-bar status is uninterpretable as mechanism evidence); if step 6's conjunct fails and W20 ≥ 6 → **PIVOT (fragility)**, naming L20. First-match-wins order otherwise unchanged.

### F2 (substantive) — Step 3's FROZEN clause is unreachable in the intact world and masks a HOLD in the broken world
**Defect.** Step 3: "Both controls 0 AND both test arms 0 (delivery confirmed) → FROZEN → Underdetermined." The two test arms are L20-only and L8-only. Under the determinism obstruction (§0.1), an intact pipeline yields L20-only = 6 flips **deterministically** — so "both test arms 0" requires L20-only = 0, which is *impossible* in the intact world (FROZEN is dead code there) and *implies pipeline change* in the broken world. In the broken (all-zero) world, step 3 fires **Underdetermined** before step 4's anchor check can fire **HOLD**, masking the pipeline-change diagnosis the anchor exists to provide.
**Fix (minimal).** In step 3, check the anchor **count** before regime routing: if L20-only flips ≠ 6 → **HOLD** (the frozen pipeline changed; step 4's set-equality check then runs inside the diagnosis lane). The FROZEN → Underdetermined route becomes: `(W20 = 0) AND (W8 = 0) AND (L8-only = 0)` **with the anchor count verified = 6** → Underdetermined. This makes FROZEN reachable and correct, and preserves "never manufacture a KILL from freeze-ambiguity."

### F3 (substantive) — The sweep KILL's "Regime LIVE" is global, but the KILL is per-layer
**Defect.** Step 7 fires the sweep KILL on "Regime LIVE" where LIVE = (W20 ≥ 1) OR (W8 ≥ 1) (§2.4). Reachable state: W20 ≥ 1, W8 = 0, L8-only = 0 → LIVE via W20 only → step 7 KILLs "no licensed causal locus at L8" from an **L8-unproven-live regime**. This violates the draft's own freeze-ambiguity principle (§4.1 item 4a: a truly-frozen regime → Underdetermined, never KILL): an L8-frozen-but-L20-live regime is freeze-ambiguous *at L8*, and the KILL's weight ("the test arms' flatness across 60 items") is uninformative at a layer whose perturbations demonstrably reach no decision. S6-1/S6-2's global instrument was sound because each had one matched control for one test arm; this sweep has two layers and needs per-layer liveness for the per-layer KILL component.
**Fix (minimal).** Step 7's KILL requires **L8-liveness**: `(W8 ≥ 1) OR (L8-only ≥ 1)` (a moved test arm is itself liveness evidence). If global-LIVE holds via W20 only with W8 = 0 and L8-only = 0 → route to step 8's named PIVOT sub-case **(d) "incomplete sweep — L8-regime unproven-live (global liveness via W20 only)"**, not KILL. KILL feasibility is preserved: in a live regime W8 ≥ 1 on 60 items is near-certain at ratio 0.38 (EXP096's B_wrong moved 3/21 gated; EXP098's W-joint moved 12/60).

### F4 — Post-exclusion effective N is unstated
**Defect.** Step 1 permits ≤2 out-of-band rows per (layer, arm) → those items are excluded from that arm's contrasts. All §4.2 algebra (≥9-flip minimum, power, specificity, θ≈0.15 floor) is computed at N=60, but the bars then operate on a paired set of N ≤ 58.
**Fix (minimal).** Step 1: the count-bars (≥6, ≥9) apply to the **post-exclusion paired set**; §4.2: the verdict lane recomputes and reports the realized N and the sensitivity floor (9/N_realized; e.g. 9/58 ≈ 0.155). Impact is rounding-level, but the binding N must be stated.

### F5 — Zero-norm routing contradiction between §2.1 and step 1
**Defect.** §2.1: ">2 zero-norm directions → that layer void." Step 1 (first-match-wins, evaluated earlier): "**any** zero-norm direction → HOLD + diagnose." §4.1 item 6 agrees with step 1 ("delivery HOLD (§3 step 1) before any gate is computed"). §2.1's void routing is fully shadowed — and the draft's §6 risk 4 asks Law #14 to confirm the tripwires, which cannot be confirmed while two sections disagree.
**Fix (minimal).** Correct §2.1: zero-norm directions route to **HOLD + diagnose** per step 1 (a broken constructor is a setup defect, not a degeneracy); the §3-step-2 void path covers **only** the ≥0.95 mean-|cosine| case. §4.1 item 6 already states this — make §2.1 match it.

### F6 — Citation precision: EXP095's pass count
**Defect.** §4.2: "CPU-feasible ($0; EXP095 ran 724 passes)." The EXP095 verdict review explicitly flags the executor's "724 passes" narration as **double-counting** T(1.0) inside the 300-T count; the binding quantities are **660 recorded rows** (and the 1300 hard cap), both satisfied.
**Fix (minimal).** Cite "660 recorded rows (the '724 passes' executor narration double-counts T(1.0) — EXP095 verdict review)."

### F7 — Step-2 prose precision (two parts)
**Defect.** (a) The L20-void sub-clause ("Mean pairwise |cosine| over {d_i^(20)} ≥ 0.95 → L20 void … the consistency anchor (step 4) is skipped if L20 is void") is **unreachable**: step 0(iii) HOLDs whenever |recomputed − 0.6639| > 0.05, and 0.95 − 0.6639 = 0.2861 ≫ 0.05 — the tighter signature gate always fires first. (b) "The licensed positive (step 6) remains available for the testable layer" is false for the only reachable void case (L8 void): step 6 **is** the L8 positive and is unavailable; the reachable routing is anchor-validation + PIVOT (step 8b, incomplete sweep).
**Fix (minimal).** Step 2: clarify the void path is live **only for {d_i^(8)}** (new construction; L20 regeneration is guarded by the tighter step-0 signature gate). Replace the "licensed positive remains available" sentence with: "L8-void → step 6 is unavailable; the anchor (step 4) still validates the setup, and the sweep routes to PIVOT (step 8b, incomplete sweep) — the KILL is downgraded as stated."

### F8 — §2.4 wording contradiction on discovery contrasts
**Defect.** "Two discovery contrasts (L8-only-vs-B; the L20 anchor is explicitly NOT a discovery contrast)" — self-contradictory: it lists one.
**Fix (minimal).** Reword: "**One** discovery contrast (L8-only-vs-B; the L20 anchor is explicitly NOT a discovery contrast). The per-layer 0.005 bar holds the discovery family-wise rate at ≤0.01 (Bonferroni over the 2 swept layers — conservative, since only one layer carries a discovery contrast)."

### F9 — Name the control-outmoves-task sub-case instead of KILLing through it
**Defect.** Reachable state: L8-only < 6 **and** W8 ≥ 6 (matched random control out-moves the task direction at L8). First-match-wins currently: step 5 doesn't fire (needs L8-only ≥ 6), step 6 doesn't fire, step 7 fires **KILL** whose licensed prose reads "inertness generalizes across the probed depth; the boundary law extends." In a world where random L8 perturbations demonstrably move decisions, "inertness generalizes" is false prose on a licensed verdict. Per the draft's own Law #15 block, this world is "movement without directional significance (fragility)" → PIVOT.
**Fix (minimal).** Add to step 5 a third disjunct: `(L8-only flips < 6 AND (W8 ≥ 6 OR W20 ≥ 6)) → PIVOT (fragility — control-outmoves-task / fragile regime, naming the layer)`, with the directional claim's refutation reported as an observation. Step 7's KILL then fires only when controls are sub-threshold, keeping its "inertness generalizes" prose honest.

---

## 3. Per-section attack log (what I tried to break, what held, what broke)

**§0 / §0.1 — the determinism obstruction. ATTACKED HARDEST. HELD — the obstruction is CORRECT.**
- *Attack 1: is the forward pass truly deterministic?* The draft's evidence chain: frozen weights (Δθ=0, LOG-331 pin) + hash-pinned constructor + frozen EXP092-B bench pin + pinned torch intra-op threads (EXP093 G4 precedent) + single pinned CPU environment. Precedent: 60/60 per-item B-decision agreement reproduced across EXP094→EXP098 (verified in the EXP098 verdict review, step 0). The residual risk (executor environment drift, silent non-determinism) is exactly what the step-4 anchor is designed to catch. No gap found in the determinism premise as a *conditional* claim.
- *Attack 2: is there a legitimate replication sense the draft misses?* A re-run is informative **about the setup** (catches executor bugs like EXP096's double-scale bug class, environment drift, thread-count changes) — the draft explicitly prices this as "setup validation" and builds step 4 around it. It is **not** informative about the L20 *signal* (re-computation ≠ replication): conditional on the frozen pipeline, the L20-only arm's outcome is a deterministic function of already-observed inputs. The draft's sentence "Any draft framing the L20 arm as a 'powered confirm-or-kill' on these items is circular by construction" is correct.
- *Attack 3: could the anchor reproduce a bug rather than the truth?* If EXP098's 6 flips were a deterministic executor bug, the anchor reproduces the bug. The draft's §4.1 item 5 addresses adversarial tuning but not this. This is a genuine residual — but it is Law #13's territory (append-only hashed artifacts, independent verdict recomputation from the primary CSV, which EXP098's review performed with zero discrepancies), not a pre-registration defect. Logged as a caveat, not a fix.
- **Adjudication: the sweep+anchor reframing is sound.** S6-4 cannot confirm-or-kill the L20 signal on the pinned bench; the three-job reframing (L8 discovery / L20 consistency anchor / cross-layer patterns) is the honest design. The N≈115 powered replication is correctly specified, priced, and fenced as unlicensed.

**§1 — background and license. HELD, with adjudication below (§5).** Every cited number verified against the verdict reviews and run archives: EXP094 B=T=R=36/60, b=c=0, p=1.0, 0 flips (the T=34/60 figures in the EXP094 review's §1 are the *struck* LOG-4373 fabrication — the binding numbers are LOG-4374/4375/4376's; the draft cites the correct LOGs); EXP095 flips {0,0,0,1,1}, all p=1.0; EXP096 gated 3 flips (b=1,c=2, p=1.0), B_wrong 3 flips (b=2,c=1, p=1.0), ratio 0.3792 (consistent with the [0.2844,0.4740] delivery band: 0.3792×0.75=0.2844); EXP097 T 7 flips @1.5 (b=1,c=6, p=0.125), 10 @3.0 (b=2,c=8, p=0.109375), B_wrong 11/15; EXP098 L20-only 6 flips (b=0,c=6, p=0.03125), L11-only 3 (p=1.0), joint 7, W-joint 12, degeneracy L20 0.6639 / L11 0.7923 (both confirmed in `exp098_report.json` / run log and EXP094's `exp094_report.json`); constructor hash `5e03f206…917f361` confirmed in `constructor_manifest.json`; EXP098 R_SEED=94094 confirmed. "License by difference" reasoning is valid (no L11 arm; L20 arm is a non-discovery anchor).

**§2.1 — arms and direction construction. HELD except F5/F7.** The {d_i^(20)} regeneration pin (re-hash + 0.6639±0.05 functional signature) is tight and correct. The {d_i^(8)} construction is adequately pinned for new-design territory (procedure = the hash-pinned C-1 contrast on L8 residuals; required manifest with procedure hash, norms, pairwise-|cosine| summary; the §3-step-2 gate as its check). Norm-tie count: 120 assertions = 60 items × 2 layers ✓. The zero-norm→void vs →HOLD contradiction is F5. Single-B design follows the S6-1 v2 F2 precedent (accepted at LOG-4411/4418).

**§2.2 — ratios. HELD.** 0.38 point, bands [0.285,0.475] = 0.38×(1±0.25) ✓; the no-interpolation fence and the 0.38 breaking-point fence are correctly scoped. L20 baseline-norm anchoring is EXP098's procedure (the draft's "(§0.1 of S6-2 v2)" pointer is imprecise — the anchoring is stated in S6-2 v2's DEFINITION—co-injection block — but the procedure itself is correctly carried; wording note only).

**§2.3 — budget. HELD.** 300 = 60 + 4×60 ✓; 360 expected ≤ 500 hard cap ✓.

**§2.4 — statistics. HELD except F3/F8.** McNemar doubling with b=wrong→right, c=right→wrong matches EXP094's convention ✓; DELTA_BAR=0.10 is the program standard ✓; the ≥6 movement gate as necessary-but-insufficient is correct per §4.2. The "two discovery contrasts" wording is F8. The asymmetric liveness rule is disclosed honestly; its per-layer gap is F3.
- *Stratum consistency — attacked both directions, HELD.* Too lenient? A single opposite-direction flip (b_s+c_s=1) cannot refute directionality; under the θ_noise=0.03 model the expected opposing flips per stratum at the KILL boundary are ~0.4 — the <2 exemption prevents noise from manufacturing inconsistency. The draft's §4.1 item 8 analysis is correct. Blocking a true positive? Under a true directional effect (θ_dir≈0.15) plus noise on the ~12 wrong-eligible items per stratum, P(≥2 opposing noise flips in a stratum) ≈ 1−0.97^12−12·0.03·0.97^11 ≈ **0.049** — a ~5%/stratum cost, acceptable, and the required stratum table (instrumentation item 8) makes any stratum-concentrated positive visible. Note (not a fix): the definition is *sign-consistency*, not homogeneity — an all-in-one-stratum directional effect passes; the verdict lane should report per-stratum (b_s,c_s) alongside the consistency verdict (already required).

**§3 — decision table. THREE DEFECTS: F1, F2, F3 (+F4, F7, F9). Otherwise held.**
- Step 0: foundation gates are complete and correctly ordered (hash → B-agreement → degeneracy signature). ✓
- Step 1: delivery probe scope (four injected cells; non-injected cells undefined) follows the S6-2 v2 F3 precedent ✓. Post-exclusion N is F4.
- Step 2: void logic direction is sound (void→PIVOT, never KILL — a KILL cannot be manufactured on an untested layer) ✓; prose precision is F7.
- Step 3: ordering defect is F2; per-layer liveness gap is F3.
- Step 4: set-equality (not just count) is the right check — same items ⇒ same b/c since B is fixed ✓. Evaluated before the global steps and fenced as non-verdict ✓.
- Step 5: matched disjunct (L8≥6 AND W8≥6) is correct (EXP097 precedent) ✓; the unmatched W20 clause is F1; the control-outmoves-task gap is F9.
- Step 6: the full conjunction (≥6 AND p<0.005 AND W8 flat AND stratum-consistent) is the correct licensed-positive shape; no conjunct alone licenses anything ✓.
- Step 7: KILL fencing ("static per-item injection at L8/L20, ratio 0.38, EXP092-B — never to 'all layers'") is correctly narrow, and the parenthetical preserving EXP098's sub-bar observation is honest ✓; liveness scope is F3; fragile-world prose is F9.
- Step 8: the named sub-cases are the right catch-all ✓; add F3's sub-case (d).

**§4.1 — degeneracy analysis. HELD except as noted.** Item-by-item: (1) McNemar on b=c=0 → p=1.0, fails safe ✓ (adversarial b=60,c=0 → p≈1.73×10⁻¹⁸ — recomputed 2/2^60 = 1.73×10⁻¹⁸ ✓). (2) ΔM zero-variance → 0 ✓. (3) Flip-rate → 0 ✓. (4) Liveness — the disclosed asymmetry is honest; the "KILL's weight is the test arms' flatness" defense holds only at a live layer → F3. (5) Anchor — fails safe toward HOLD ✓; the executor-tuning analysis is adequate for the stated threat model. (6) Degeneracy gates — fail safe toward void/PIVOT ✓; the zero-vector edge correctly routes to step 1 (which is exactly F5's point — §2.1 must match). (7) W-flatness — the neutralization analysis (a)/(b) is correct ✓. (8) Stratum consistency — correct as analyzed above ✓.

**§4.2 — probe-feasibility + power. HELD except F4/F6.** Every number recomputed exactly (§1 of this review). The N≈115 pricing (575 passes + fresh bench construction per EXP092's signed protocol with G2 null-calibration and oracle diagnostic) is correctly scoped as the binding constraint. The noise model θ_noise=0.03 is disclosed as a model ("under a noise flip rate"), justified by EXP098's L11-only 3/60 — adequate with the note that the verdict lane should report realized W8/W20 flip rates alongside.

**§4.3 — verdict discipline. HELD.** Evaluation order frozen pre-run, five permitted verdicts with step→verdict mappings, no post-hoc edits, design-change→new-number rule ✓.

**§5 — instrumentation. HELD.** All ten items persist what the table needs; the machine-written routing/anchor/stratum logs precede the table walk ✓. The S3-7 rider ("carried for free; no analysis pre-registered") matches the LOG-4408 watchlist recommendation exactly ✓.

**§6 — known design risks. HELD — the draft's self-attack list is genuine.** Risk 1 (the obstruction) is the right top risk and this review adjudicates it correct. Risk 2 (wasted anchor): adjudicated — the anchor is the only injection-pipeline cross-validation (B-agreement validates only the base pipeline; the anchor validates the injection machinery at the operating ratio against the EXP096 double-scale bug class); 60/300 passes is proportionate insurance. Risk 3 (θ≈0.15 floor making CONTINUE decorative): the disclosed asymmetry (well-powered KILL-or-PIVOT, demanding CONTINUE) is the honest design — the bar does not move. Risk 4: gate values confirmed adequate subject to F5. Risk 5 (stratum consistency): adjudicated above. Risk 6 (W20 fresh seed): the fresh draw is the non-circular choice; no double-counting (new measurement, norm-tied to a different arm than EXP098's W-joint). Risk 7 (Phase 2): correctly fenced as unlicensed.

**§7/§8 — scope and next steps. HELD.** The no-pilot, no-GPU, no-signed-artifact discipline is stated and complete.

---

## 4. License adjudication (binding questions)

**(a) Does S6-4 clear LOG-4407's "no further static per-item L11 experiments licensed"? YES — clearly.**
LOG-4407's bar is explicitly L11-scoped ("No further static per-item L11 experiments are licensed"; the S6-1 dispatch at LOG-4409–4413 reaffirmed the bar is license-scoped). S6-4 contains **no L11 arm at all** — its test arms are L8-only (new layer) and L20-only (consistency anchor). EXP097's three-experiment closure is "fenced to single-layer static per-item injection" (L11). The draft's "license by difference" (different layers, not L11) is valid. **CLEAR.**

**(b) Is the L20 anchor within license given EXP098's "no single-layer L20 follow-up licensed"? YES — the anchor is not a follow-up.**
EXP098's verdict (LOG-4423): "a dedicated single-layer L20 design is new-design territory (the named observation's p<0.01 bar was not met, so no follow-up is licensed by this verdict)." A "follow-up" is a new test aimed at the L20 signal. The S6-4 L20 arm is: (i) packet-licensed — LOG-4408's S6-4 packet explicitly specifies "causal layer sweep: initial L8 and L20 test"; (ii) non-discovery by construction — no discovery contrast, no licensed finding about L20 causality, step 4 fenced as setup validation; (iii) expected to reproduce by determinism, with deviation routing to HOLD (diagnosis), never to a verdict. It re-tests nothing and discovers nothing. **The anchor is within license as setup validation.** The draft's step-7 KILL prose ("no licensed causal locus at L8 or L20") is honest *given* the step-7 parenthetical preserving EXP098's sub-bar observation as reported-but-sub-bar — the KILL claims the absence of a *licensed* positive, not L20 inertness.

---

## 5. What was checked and held (no fix)

The determinism obstruction (§0.1); all §4.2 power/McNemar/CP figures (recomputed exactly); all number citations to LOG-4407/4408/4423, the EXP094–098 verdict reviews, the frozen archives (degeneracy 0.7923/0.6639, constructor hash, R_SEED=94094), and EXP093's signed pre-reg conventions; the L8 construction pinning; the W20 fresh-seed choice; the S3-7 rider; the stratum-consistency definition (both attack directions); the liveness instrument's disclosed asymmetry; the scope fences; the anchor's 60-pass price (proportionate insurance, not waste); the θ≈0.15 sensitivity floor disclosure.

---

*Review completed 2026-09-28 by the independent Law #14 lane. Verdict: **ACCEPT-WITH-FIXES** (F1–F9). The draft file was not modified. Next: repair lane applies F1–F9 → independent delta re-verification → CEO execution clearance. No pilot authorized.*
