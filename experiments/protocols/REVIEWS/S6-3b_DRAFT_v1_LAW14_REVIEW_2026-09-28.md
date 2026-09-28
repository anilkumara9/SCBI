# Law #14 Adversarial Review — S6-3b Preregistration DRAFT v1 (2026-09-28)

**Reviewer:** independent Law #14 lane (fresh; did not draft any S6-3b material; no prior work on this artifact).
**Target:** `research/innovation/S6-3b_PREREG_DRAFT_v1_2026-09-28.md` (DRAFT v1, UNSIGNED, 233 lines, 2026-09-28; logged LOG-4442). The draft file was **not edited** — review only.
**Verdict: ACCEPT-WITH-FIXES** — two fixes (F1–F2) below, both precision/fence repairs. Neither requires rebuilding the design; neither alters a bar, gate value, or verdict mapping's intent. After repair: independent delta re-verification, then CEO clearance per the draft's §8.

**One-line reason:** the §4.2 algebra recomputes exactly, the no-peeking bright line holds under the hardest attack (see §2), the F5 τ adjudication carries intact, and all S6-3 F1–F7 lessons are present — but the draft uses the label "S6-3c" for two different follow-ups (F1), and the new mean-mass audit field's permitted use is loose enough to admit post-hoc aggregation-hopping analysis (F2).

---

## 1. Independent recomputation (§4.2 verification — from first principles)

All recomputed by this lane with exact arithmetic (pure-stdlib `math.comb`; no model, no weights, $0). **Every figure in the draft's §4.2 matches exactly.**

- **McNemar minimum at α = 0.01 (doubling):** b=0, c=8 → p = 2/256 = **0.0078125** < 0.01 ✓; b=0, c=7 → p = 2/128 = **0.015625**, n.s. ✓. The ≥8-directional-flip discovery bar stands.
- **Noise specificity:** P(X≥6 | N=60, θ=0.03) = **0.0091** ✓ (recomputed 0.009144… → 0.0091).
- **KILL-at-floor weight:** 0/6 → exact one-sided 95% upper bound = 1 − 0.05^{1/6} = **0.3930 → 39.3%** ✓.
- **Sensitivity floor:** 8/60 = **0.1333** ✓.
- **F2 operating condition re-proof (checked, not rubber-stamped):** mass_i^max = max_h Σ_{t∈span} A^{(11,h)}[q→t]; each head's weights sum to 1 over all tokens, so each head's span-mass ≤ 1, hence mass_i^max ≤ 1 always. τ_i ≤ 1 ⟺ 2·E_i/N_i ≤ 1 ⟺ E_i/N_i ≤ 0.5 — identical to S6-3's condition. The re-proof is valid; the max-aggregation changes nothing about the operating condition. ✓
- **Spot-checks of cited values against their sources:** EXP100 masses [0.0396, 0.0746] vs τ [0.2286, 0.2759] ✓ (EXP100 verdict §1); 127 passes ✓; degeneracy 0.7923/0.79226063 ✓; B=T=R=36/60 ✓ (LOG-4375/4376/4377); EXP095 {0,0,0,1,1} ✓; EXP096 3/21 at 0.3792 ✓ (F4 carried — the draft writes "3/21"); EXP098 L20 6 flips b=0,c=6,p=0.03125 ✓; EXP099 L8 4 flips p=0.625, W20 7 ✓; S6-5 5/381 → 2.74% ✓; constructor hash `5e03f206…917f361` ✓. **No invented numbers found.**

---

## 2. The two re-opened questions — binding adjudications

LOG-4441 (EXP100 verdict) explicitly re-opened "the τ-principledness and no-peeking questions" for any re-gating, "requiring its own pre-registration and Law #14 review." This review answers both. Both HOLD.

### 2a. No-peeking — HOLDS (attacked hardest)

**The attack.** The draft chose max-over-heads knowing EXP100's mean-aggregation masses never fired. Had the mean-gate fired at 50%, max would never have been proposed. Is the aggregation choice outcome-tuned — "the pre-named alternative that fires more," i.e. outcome-tuning with extra steps?

**What I verified:**
1. **τ is byte-identical to the adjudicated constant.** τ_i = 2·(E_i/N_i) appears throughout exactly as in S6-3 v2; the draft never calls it "standard" (F5 wording carried — only "program standard" appears, for the movement gate). No numeric threshold moved.
2. **The aggregation was pre-named in S6-3 v2 §2.2 — verified in the file.** Line 81: "mean-over-heads is the conservative relevance operationalization, pre-registered as the frozen choice (max-over-heads would fire the gate more often and was rejected as the less conservative option)." The draft's "pre-named alternative" claim is textually true, not reconstructed.
3. **The EXP100 verdict itself prescribed this move.** LOG-4441's next-licensed-question names "a max-over-heads aggregation" verbatim as a candidate re-gating. The choice is the verdict's own prescription, not smuggled in.
4. **No S6-3b parameter is a function of EXP100's mass measurements.** The draft cites only the *qualitative* published fact (masses below uniform on all 60 items); the specific values [0.0396, 0.0746] appear solely as background citations (§1), never in a parameter computation. The structural leg (max_h ≥ mean_h always — uniformly more permissive, zero data examined) is data-independent.

**The honest residual (the draft states it; I confirm it).** The draft admits in §6 risk #1 that "the LOG-4441 observation is what makes it the *licensed* next move rather than a guess" — i.e., the *research direction* is outcome-informed. That is not peeking. Peeking is outcome-dependence of *design parameters*; the license standard is the absence of a tuning surface, not the chooser's ignorance. There is no tuning surface here: the constant didn't move, the aggregation is discrete and pre-registered, and the firing rule is closed-form. Moreover the order tried (conservative mean first, permissive max second) is the correct falsification-first order — had max been tried first and mean second, the sequence would look like threshold-hunting; as ordered, it is disciplined exhaustion.

**Adjudication (binding): motivation-by-observation is distinguished from calibration-by-observation. The no-peeking bright line HOLDS.** The draft's §0.2 bright-line statement is verified true: no parameter is a function of EXP100's measurements.

### 2b. τ-principledness — HOLDS (F5 carried, aggregation switch does not re-open it)

The F5 binding adjudication (LOG-4436) licensed τ = 2×-uniform as a fail-safe pre-registered heuristic under three conditions: (i) no peeking surface, (ii) fail-safe miscalibration, (iii) the verdict never hinges on the constant. All three re-verified for the max-gate in §0.2's fail-safe re-proof: (i) the constant is unchanged and closed-form and §2a holds; (ii) too selective → step 2b PIVOT, too permissive → step 2c vacuous-gate flag, and the gate alone cannot manufacture the step-5 conjunction; (iii) miscalibration yields PIVOT-untestable or a weak KILL, never a false CONTINUE. The aggregation switch changes the *relevance quantifier*, not the constant — the principledness fight about the number stays settled.

**Adjudication (binding): τ remains licensable as a fail-safe pre-registered heuristic under the max-gate. The "why this aggregation" question is answered by §2a, not by re-litigating the constant.**

---

## 3. Verdict: ACCEPT-WITH-FIXES — numbered fix list (minimal, precise)

### F1 (naming collision) — "S6-3c" labels two different follow-ups
**Defect.** §0 breaking point (iv) (line 23): "A third aggregation tweak (S6-3c) is pre-emptively unlicensed by this draft." §0.2 (line 37): the later-layer relevance read "is the named S6-3c candidate if S6-3b collapses." The same label refers to (a) an unlicensed third aggregation tweak and (b) the licensed-next-question later-layer read. A future lane following the "S6-3c" pointer could not tell which design it names — a chain-of-custody defect in the program's experiment numbering.
**Fix (minimal).** In §0 breaking point (iv), delete the "(S6-3c)" label from the unlicensed-third-aggregation-tweak sentence (it is unlicensed and needs no name): "A third aggregation tweak is pre-emptively unlicensed by this draft." Keep "S6-3c" reserved for the later-layer relevance-read candidate per §0.2. One sentence in §7's "does not license" list already covers later-layer reads; no other change.

### F2 (new attack surface) — the mean-mass audit field's permitted use is under-fenced
**Defect.** §5 item 2 persists `mass_i^mean` as an "audit field — the S6-3-comparability counterfactual, persisted not analyzed," while §2.2 says it "exists so the verdict lane can audit the S6-3-comparability counterfactual without re-running." The permitted use is vague: a verdict lane could report mean-field-derived coverage ("the mean-gate would have fired on k/60") as a descriptive counterfactual — post-hoc aggregation analysis through the back door, exactly the hopping that breaking point (iv) unlicenses. Note no mean-gate *outcome* analysis is possible (no injection passes exist under the mean-gate), so the surface is narrow — but the fence should say so explicitly rather than rely on "no analysis pre-registered."
**Fix (minimal).** In §2.2 (mean-mass audit field paragraph) and §5 item 2, narrow the permitted use to the gate-integrity audit only: the mean column may be used solely to verify (a) the fired ⟺ mass_i^max ≥ τ_i consistency on all 60 rows and (b) the structural mean-fire ⟹ max-fire implication (same τ). Add to §4.3 verdict discipline: "The mean-mass audit field is evidence for the gate-integrity audit only; it is not a second gate — no verdict, worksheet cell, or report may cite any mean-field-derived coverage, flip, or counterfactual quantity." No other change.

---

## 4. Per-attack log (what I tried to break, what held, what broke)

**Attack 1 — no-peeking bright line.** ATTACKED HARDEST. HELD — see §2a. The three legs check out: structural max≥mean (data-independent) ✓; pre-named alternative (verified in S6-3 v2 §2.2 line 81) ✓; the verdict's own prescription (LOG-4441) ✓. Weakest leg noted honestly: §0.2 leg (3)'s "a 1×-uniform mean-gate would plausibly also collapse" is hedged ("plausibly") and partially counterfactual — it is not load-bearing, since legs (1)+(2)+verdict-naming carry the choice, and the stronger reason to reject candidate (a) is that it re-opens the principledness fight from zero. Not a defect; recorded.

**Attack 2 — hypothesis identity (diffuse vs existential relevance).** HELD. The LOG-4407 bar's carve-out operates at the gate-source level ("attention-state-gated, dynamic" — live function of forward-pass activations), which is unchanged; the quantifier refinement (∀-average → ∃-head) is a hypothesis refinement *within* the carved-out lane. The draft scopes the CONTINUE prose to "under existential attentional relevance" (step 5) and the KILL to "existential relevance-gating" (step 6) — the weakened claim is fenced into the verdict language itself, and §6 risk #3 self-attacks the "buying testability by spending meaning" worry with the step-5 conjunction as backstop (a vacuous relevance notion cannot manufacture ≥6 directional flips at p<0.01 with a flat matched control). No license re-run needed beyond this confirmation.

**Attack 3 — breaking point (iv) principled?** HELD. Mean and max are the two natural quantifiers over attention heads (average vs existential); the discrete space of natural aggregations is exhausted by these two. Any third aggregation (top-k mean, median, trimmed variants) would be continuous tuning in disguise — exactly the pathology the fence prevents. The fence is principled, not arbitrary. (Subject to F1's naming repair.)

**Attack 4 — §4.2 algebra.** RECOMPUTED EXACTLY — see §1. No discrepancies.

**Attack 5 — S6-3 F1–F7 carried intact.** VERIFIED ITEM-BY-ITEM:
- F1: reachability window [10%, 8/60) named with routings (§0 decision block, §4.2) ✓; "flatness across the *fired* items" ✓; 8/F alongside 8/N_realized (§4.2, §5 item 8) ✓.
- F2: re-proved for the max-gate (§0.2 — validity checked in §1 above); step 0iii asserts E_i/N_i ≤ 0.5 ✓.
- F3: prose is "mid-stack (L11) attention from the final prompt token" throughout; "readout query" appears nowhere ✓.
- F4: "EXP096's differently-gated T moved 3/21 at this ratio" ✓.
- F5: "standard" never modifies twice-uniform; the binding fail-safe-heuristic adjudication is recorded and re-proved (§0.2) ✓.
- F6: disjunct (b) keeps "the directional claim's refutation is reported as an observation"; disjunct (a) explicitly reports no refutation ✓.
- F7: step 2c pre-registers "CONTINUE (directional signal at ratio 0.38; gating unattributed — the gate was vacuous)." verbatim ✓.
- Also carried: matched random control under the identical max-gate with per-fired-item norm ties ✓; step-2b tripwire before any verdict (never KILL from a collapsed gate) ✓; first-match-wins steps 0–8 ✓; single ratio 0.38, no grid, no interpolation ✓; CPU-only $0, Δθ=0, no GPU ✓.

**Attack 6 — mean-mass audit field as post-hoc surface.** BROKE (mildly) → F2. The field is new in this draft; its fence needed sharpening. Note: no mean-gate outcome analysis is constructible (no injection passes under the mean-gate exist), so the exposure was descriptive-counterfactual only — F2 closes it.

**Attack 7 — invented numbers.** NONE FOUND — see §1 spot-checks. Every cited value traces to LOG-4400/4407/4409/4416/4423/4429/4432/4434/4440/4441, the EXP094–100 verdict reviews, or the frozen archives. The seed is described as "fresh pre-registered seed, distinct from every prior R stream including EXP100's" with no numeric value — identical to S6-3 v2's carried convention (whose executor recorded R_SEED_GATED=207101 in the manifest); not a new defect.

**Section sweep — additional notes:**
- §0.1 "not secretly S6-3/EXP100": the ∀-average vs ∃-head distinction is real; "A KILL here does not re-kill S6-3's exact gate (which died untestable, not refuted)" is correct scope hygiene ✓.
- §0.3 gate-determinism: correct; the second-run "confirmation" prophylaxis is the right guard against an S6-4-style obstruction ✓.
- §2.1 arms: 3-arm design with identical live max-gate on gated-R is EXP099's anti-lesson applied ✓; deterministic-copy rule for unfired items exact for the frozen model ✓; 180 = 60+60+60 maximum ✓.
- §3 decision table: systematic first-match-wins audit — steps 0, 1, 2a/2b/2c, 3, 4a/4b, 5, 6, 7 all correctly ordered and scoped; the F1 window language, F6 scoping, and F7 verbatim prose all present ✓. Step 6's KILL is fenced to "max-gated per-item L11 injection at ratio 0.38 on EXP092-B — never to 'all dynamic mechanisms,' 'all aggregations,' or 'all layers'" — the "all aggregations" exclusion is the correct anti-double-kill ✓.
- §4.1 degeneracy analyses: all nine items fail safe; item 5's max-gate degenerate case (uniform attention → mass^max = E/N < 2E/N → 0% → 2b PIVOT) recomputed correct ✓.
- §4.3 verdict discipline: evaluation order frozen, tripwire un-rethresholdable, aggregation un-re-choosable ✓ (F2 adds the mean-field clause).
- §6 risks: genuine self-attack list; risk #1 is correctly identified as the most likely fatal one (adjudicated in §2) ✓; risk #6 honestly notes the risk reversal (vacuous-gate now live, collapse was live for S6-3) ✓.
- §7/§8: no-pilot, no-GPU, single-lane-fence discipline complete ✓.

---

## 5. License adjudication (binding questions)

**(a) Does S6-3b clear LOG-4407's "no further static per-item L11 experiments licensed"? YES — by the same carve-out that licensed S6-3, unchanged.** The bar reserves "attention-state-gated, dynamic" mechanisms; the max-gate is a live function of the current forward pass's activations (computed from the B pass via read-only hooks, per EXP100's settled and audited preflight). The aggregation change does not move the design out of the carve-out. **CLEAR.**

**(b) Is the max-over-heads re-gating licensable without a peeking surface? YES — §2a.** The threshold is the adjudicated constant, byte-identical; the aggregation is a discrete choice among verdict-named, pre-named alternatives; no parameter is a function of EXP100's measurements. **LICENSED.**

**(c) Is the "last aggregation variant" fence principled? YES — §4 attack 3.** Mean and max exhaust the natural discrete aggregations; the fence prevents continuous tuning in disguise. **PRINCIPLED** (subject to F1's label repair).

---

## 6. What was checked and held (no fix)

The §4.2 McNemar/power/specificity algebra (recomputed exactly); the F2 operating-condition re-proof (re-derived, not trusted); all number citations to LOG-4400/4407/4409/4416/4423/4429/4432/4440/4441, the EXP094–100 verdict reviews, and the frozen archives; the no-peeking bright line (verified against the actual S6-3 v2 text and the EXP100 verdict text); the carried F5 τ adjudication; the 3-arm max-gated design with the identical-gate matched random control; per-fired-item norm ties; the fresh-seed-distinctness convention; the deterministic-copy rule; the single-ratio/no-grid/no-interpolation fences; the fragility PIVOT routes with correct matched-control scoping; the licensed-positive conjunction; the KILL's narrow fencing (including the "never all aggregations" exclusion); the no-leakage (Law #7) argument (gate uses no label, margin, or outcome — only the attention distribution; identical gate on the control — confirmed again as requested); the coverage tripwire and step-2b-before-verdict ordering; the CPU-only $0 / no-GPU / Δθ=0 guards; the S3-7 rider; the scope fences; the single-lane fence.

---

*Review completed 2026-09-28 by the independent Law #14 lane. Verdict: **ACCEPT-WITH-FIXES** (F1–F2). The draft file was not modified. Next: repair lane applies F1–F2 → independent delta re-verification → CEO execution clearance. No pilot authorized.*
