# Adversarial Review — EXP068 Pre-registration Protocol (Law #14)

**Reviewer role:** Adversarial Reviewer (red-team; Law #14 — challenge, don't defend)
**Date:** 2026-09-23
**Target:** `experiments/protocols/EXP068_LOOP_PREREG_SPEC.md` (drafted 2026-09-23)
**Constraining sources:** `theory/LOOP_SPEC_DRAFT.md` (signed), `experiments/protocols/EXP067_QKOV_SUBSPACE_PROCRUSTES_SPEC.md` (template), `AGENTS.md` (14 laws)
**Verdict: SIGN-WITH-FIXES** — one FATAL-class hole (fixable without redesign), nine MAJOR fixes, several MINORs. No REJECT-level flaw: the protocol's skeleton (gates, halts-as-results, LICENSES discipline, N1 framing) is sound.

---

## 0. Standing note: hype pressure vs. the protocol's discipline

The user is currently pressing for "mind-blowing," "world-changing" framing. This protocol
correctly refuses: §1.1 and §14 hold the N1 line (better-validated mechanism, never N2;
"invention" appears only in the program name and in the prohibition). **This must not be
softened in revision.** The strongest thing this review can say is that the draft's honesty
machinery — pre-registered halts, kill criteria, license statements — is exactly what makes
any future positive result *believable*, which is worth more than any adjective. Law #10 and
Law #14 require me to defend the N1 framing against the current pressure, and I do.

---

## 1. [FATAL] A-eval-transfer: the transfer hole is real, and a labeled assumption does not close it

**The drafter's self-identified weakest point is confirmed as the weakest point — and it is
sign-blocking.**

The ρ-gate (§4) validates $\mathcal{E}$ on $\mathcal{D}_{\mathrm{gate}}$: 50
*support-distribution* items (support vocabularies V1–V5). The test phase runs the loop on
60 *novel-vocabulary* items (planets/elements). The transfer dimension is the *item's*
vocabulary: the gate establishes "agreement across support views tracks rescue on
support-vocabulary items"; the test phase needs "agreement across support views tracks
rescue on novel-vocabulary items." No decision-tree branch can detect transfer failure:

- Transfer failure presents as: gate passes ($\hat\rho>0$, $p<0.05$ on support items),
  then C3 $\Delta M \le 0$ on test items — because $\mathcal{E}$ selects for consistency
  across support views, which no longer tracks rescue on novel-vocabulary items.
- Branch (d) then fires and its [INTERPRETATION] licenses the **structural** reading:
  "even a validity-gated, per-instance selection loop cannot extract causal transfer…
  the dissociation is structural, not operator-quality."
- That reading would be **false** under transfer failure. The correct reading would be
  "$\mathcal{E}$ doesn't transfer" — a verdict on the instrument, not the loop hypothesis.

F4 (blind-spot) does **not** cover this hole: transfer failure can present as *low*
$C_{\mathrm{cons}}$ (evaluator noisy on the test distribution → selections ~random →
$\Delta M \le 0$ without high consistency), in which case F4 is silent and (d) licenses
the structural conclusion unopposed. Even when F4 fires alongside (d), the canonical
ruling takes the structural interpretation. A labeled [ASSUMPTION] therefore leaves the
experiment's centerpiece falsification confounded by an undetectable alternative
explanation — a Law #4 (falsifiability) failure. **This needs a protocol-level check.**

### Required fix T1: pre-registered transfer probe (§4b)

- **$\mathcal{D}_{\mathrm{xfer}}$:** 15 items carved by fixed pre-registered seed from the
  N=60 test suite *before* any test-phase execution; permanently excluded from the
  confirmatory set afterward (**test phase runs on N=45**). Labels used for probe
  measurement only — validity measurement, not test time (same Law #7 logic as the gate).
- **Procedure:** identical to the §4 gate ($K$ candidates via $\mathcal{G}_1$ from
  $\mathcal{D}_{\mathrm{tune}}$ only; $S_E$ over $m=5$ views; true rescue indicators under
  the §4 rescue definition fixed per G1 below), per-instance top-$S_E$, point-biserial
  $\hat\rho_{\mathrm{xfer}}$, one-sided exact permutation $p$.
- **Halt rule:** HALT iff $\hat\rho_{\mathrm{xfer}} \le 0$ **or** one-sided $p \ge 0.20$.
  Rationale (pre-register this): the probe is a *degradation screen*, not a second
  confirmatory gate. The arithmetic is principled, not arbitrary: at $n=15$, one-sided
  $p = 0.20$ corresponds to $t \approx 0.87$ (df=13), i.e. $\hat\rho \lesssim 0.235$ —
  **exactly the gate's effect-size floor**, re-expressed at reduced $n$. The probe therefore
  applies the *same* effect-size standard as the gate instead of demanding $\hat\rho \gtrsim
  0.44$ (which $p<0.05$ at $n=15$ would require, halting valid-but-noisy transfers).
- **Pre-registered risk (state it):** at true $\rho = 0.5$, P(false halt) $\approx 18\%$;
  at true $\rho = 0.6$, $\approx 10\%$; sensitivity to true $\rho = 0$ is $80\%$ by
  construction. A halt is a reportable outcome ("$\mathcal{E}$ does not transfer"), not a
  wasted run.
- **Order:** tuning → ρ-gate → transfer probe → headroom (on the 45) → test phase.
- **New branch (a2):** "Transfer-probe HALT — $\mathcal{E}$ does not transfer to the test
  distribution. H_loop **untestable** under this evaluator on this distribution — neither
  falsified nor confirmed. LICENSES: '$S_E$ validated on support-distribution items carries
  no measurable signal on novel-vocabulary items.' DOES NOT LICENSE: 'the loop fails'
  (the test phase never ran); 'no evaluator could transfer' (only this $S_E$ form tested)."
- **Branch (d) rider:** the canonical falsification and its structural interpretation are
  *conditional on probe passage*. Add to (d): "Precondition: transfer probe passed. The
  structural reading is licensed only because the transfer confound was screened."
- **Bookkeeping:** budget table +≈800 passes ($15 \times 53$); test-phase lines recomputed
  at N=45; static conditions $5 \times 45 = 225$; headroom gate on the 45; checklist gains
  probe items; §9 A-eval-transfer becomes "Tested by the transfer probe (§4b); residual
  risk: the probe is a screen, not a proof."
- **Dangling reference:** §9's "see the reviewer's notes (§13)" points at §13
  (Reproducibility), which contains no review notes. Reword to "see adversarial review."

**Answer to the drafter's question:** A-eval-transfer **needs the protocol-level transfer
check**; it does not survive as a labeled assumption. Cost ≈800 forward passes and 15
test items; the alternative is an unconfounded-looking falsification that may be false.

---

## 2. [MAJOR] The ρ-gate: criterion accepted, definitions missing

**The criterion itself is adequate.** GO iff $\hat\rho > 0$ AND one-sided exact permutation
$p < 0.05$ at $n=50$. Verified: one-sided $p<0.05$ at $n=50$ (df=48, $t>1.677$) implies
$\hat\rho \gtrsim 0.235$ — the drafter's "moderate effect-size floor" arithmetic is correct,
and the floor is honestly labeled [CONVENTIONAL]. $n=50$ is enough *because the gate is a
screen, not a proof*: it licenses the test phase, and the test phase (especially the C4
ablation) is the real arbiter of whether $\mathcal{E}$ drives selection. With the §1
transfer probe in place, the residual "weak-but-valid $\mathcal{E}$" risk is handled by
(d)/(f), not by raising the gate floor (raising it would manufacture false halts).

**But the gate is under-defined in ways that affect implementability and interpretation:**

- **G1 — Define $\mathbf{1}[\mathrm{rescue}]$.** §4 says "the true rescue indicator
  $\mathbf{1}[\mathrm{rescue}]$" without defining it. Required:
  $\mathbf{1}[\mathrm{rescue}(B;x)] := \mathbf{1}[\hat{y}(B;x) = y \;\land\;
  \hat{y}(\emptyset;x) \neq y]$ (true rescue: intervened-correct where unintervened-wrong),
  with $\hat{y}(\emptyset;x)$ the unintervened decision on $x$. Budget the +1
  unintervened pass per gate item explicitly (state whether the §12 "+m" covers it — it
  does not on its face).
- **G2 — Report the rescue base rate.** If $\mathcal{D}_{\mathrm{gate}}$ items are mostly
  already-correct unintervened, $\mathbf{1}[\mathrm{rescue}]$ is sparse and $\hat\rho$ is
  unstable. Required: report gate-item baseline accuracy and the rescuable fraction;
  pre-register a low-information caveat (rescuable fraction <10% → gate outcome flagged
  low-information; reported, not a halt — the test phase remains the arbiter).
- **G3 — The B₀ exclusion needs a companion diagnostic.** Excluding $B_0$ from the gate
  candidate set is defensible for the gate's stated purpose (testing $\mathcal{E}$'s
  *among-candidate* discrimination — its argmax job), but the loop also uses $\mathcal{E}$
  to compare candidates against the incumbent (acceptance rule
  $S_E(B_t^*) > S_E(B_t) + \delta$, $B_0 = B_{\mathrm{agg}}$), and that comparison is never
  validated. The "anchor the correlation artifactually" justification is hand-waving.
  Required (exploratory, not gating; +6 passes/gate item — add to budget): per gate
  instance compute $S_E(B_0;x)$ over the $m$ views and $\mathbf{1}[\mathrm{rescue}(B_0;x)]$,
  and report $\mathrm{corr}(\Delta S_E, \Delta\mathrm{rescue})$ with $\Delta$ relative to
  $B_0$. This tests the acceptance rule's premise on held-out data. (The incumbent
  comparison is *also* tested in the test phase via F3 — this diagnostic is the gate-time
  complement.)
- **G4 — Note range restriction.** The primary per-instance analysis conditions on the
  argmax (range restriction attenuates $\hat\rho$ — conservative for a gate, but say so);
  the candidate-level analysis is the less-attenuated complement. One sentence.

---

## 3. [MAJOR] Kill triggers: analysis and required tightenings

- **F2 (collapse to static, $\cos>0.95$ on $>80\%$, [ARBITRARY]): arbitrary-but-reasonable,
  no perverse incentive.** The "loop correctly converges to $B_{\mathrm{agg}}$ because it
  is optimal" case is handled: then C3≡C2, F3 fires, and branch (f3) rules "gain
  attributable to the static direction, not adaptation" — the correct verdict, since
  H_loop requires *per-instance selection* to add value. F2 is a diagnostic, not a halt;
  nothing is optimized against it at test time. Required: report the full
  $\cos(B^*(x), B_{\mathrm{agg}})$ distribution (the [ARBITRARY] tags promise sensitivity
  analysis — deliver the data for it).
- **F3 attribution rider overreaches as stated.** "If additionally C3-vs-C4 gives $p \ge
  0.05$ or $\Delta M_{\mathrm{loop}} \le \Delta M_{\mathrm{rand}}$, the evaluator contributes
  nothing beyond search." Two tightenings required: (i) scope to the primary endpoint —
  "no *demonstrated* $\Delta M$ contribution beyond search" (a non-significant difference
  is a failure to demonstrate, not a proof of absence; and equal net $\Delta M$ can hide
  different $(b,c)$ risk profiles — require reporting the full $(b,c)$ decomposition for
  C3 vs C4); (ii) soften (f2)'s LICENSES "search helps, the evaluator doesn't" to "no
  demonstrated evaluator contribution to $\Delta M$."
- **F4 vs (d) precedence is ambiguous.** F4 ($\mathrm{mean}\,C_{\mathrm{cons}}(B^*) \ge 0.8$
  while $\Delta M_{\mathrm{loop}} \le 0$) is essentially a subset of (d)'s condition.
  Required: state that (d) takes precedence as the canonical ruling and F4 is reported as
  the *diagnostic characterization* of the (d) outcome when both fire. Also note the
  overlap honestly: with $\lambda_c$ tuned high, $C_{\mathrm{cons}}(B^*) \ge 0.8$ is expected
  *by construction*, so F4 ≈ (d) + "the loop did what it was told." Report the
  $C_{\mathrm{cons}}(B^*)$ distribution regardless (MINOR).
- **(f1) lacks its LICENSES statement** although §11's contract says every branch states
  one. Required: "(f1) LICENSES: 'per-instance selection yields gains over baseline fully
  accounted for by the static CAA direction; no evidence of adaptation benefit.' DOES NOT
  LICENSE: 'the loop is useless' (it matched static; the failure is *adaptation*, not
  *steering')."

---

## 4. [MAJOR] C4: the text contradicts the budget table on compute-matching

§6 describes C4 as "selection uniform-random over $\mathcal{C}_t$ (seed-fixed) instead of
$S_E$" — i.e., C4 *skips* the evaluator's $K{\cdot}m{\cdot}T$ forward passes — while §12
budgets C4 at the full 32,700 ("same bound (compute-matched by construction)"). Both
cannot be true, and "identical … budget" is false under the §6 reading. This matters
because C4 is the *attribution* control: if C3≈C4, the protocol wants to conclude the
evaluator contributes nothing, but under the §6 reading C3 used strictly more compute to
tie — the honest conclusion would be "no gain *despite* more compute," a stronger
negative than the rider states.

**Required:** make C4 truly compute-matched — C4 computes $S_E$ identically to C3 (same
forward passes) but selects uniform-random over $\mathcal{C}_t$, *ignoring* the computed
scores. Reword §6 C4 accordingly ("isolates the evaluator's *selection* contribution at
identical compute"). The §12 budget line then becomes true as written. (The wasted compute
is free-tier-feasible and is the price of a clean attribution control — cf. the EXP067
bundle review's F1 lesson: never let a control silently do less than its label claims.)

---

## 5. [MAJOR] Decision tree: precedence, licensing, H_loop alignment

- **D1 — Precedence rule missing.** (d), (f), (g), (e) can co-fire (e.g., F3 + F5; F4 +
  (d)). Post-hoc branch assignment is Law #4-adjacent interpretive freedom. Required:
  pre-register precedence **(a)/(a2) → (b) → (c) → (d) → (g) → (f) → (e)**.
- **D2 — (e) over-licenses against C7.** The positive criterion is "C3 beats-or-ties C7
  (F5 not triggered)," but (e) LICENSES "causal transfer gains over … compute-matched
  output-level search." If $\Delta M_{\mathrm{BoN}} > \Delta M_{\mathrm{loop}}$
  non-significantly, "gains over output-level search" is false. Required: conditional
  licensing — "beats output-level search" language only if C3-vs-C7 McNemar $p<0.05$
  favors C3; otherwise "not dominated by compute-matched output-level search (F5 not
  triggered); $\Delta M_{\mathrm{BoN}}$ vs $\Delta M_{\mathrm{loop}}$ reported."
- **D3 — H_loop's third conjunct vs. the operational criterion.** H_loop (carried verbatim
  from the loop spec) says "**beats** compute-matched output-level search"; the positive
  criterion operationalizes it as "beats-or-ties (F5 not triggered)." "Not significantly
  dominated" ≠ "beats." Required: add an explicit labeled note in §1 acknowledging this
  operationalization gap (do not silently soften a verbatim-carried hypothesis — Law #4),
  with D2's conditional language as the reporting rule.
- **D4 — Branch (a2)** per §1.
- **D5 — Branch (d) rider** per §1.

---

## 6. [MAJOR] Tuning: the δ shared-trajectory claim is false as stated

§3.1: "$\delta$ by recomputing acceptances offline under each $\delta$ value (no new
forward passes). This is legitimate because the loop records the full $S_E$ history."

**This is not legitimate, and the sentence is false.** The recorded trajectory was
generated under the provisional $\delta = 0.02$ acceptance path. Under a counterfactual
$\delta' = 0$, every $t$ where the acceptance decision flips changes $B_{t+1}$, which
changes $\mathcal{G}_2$'s subsequent candidate sets — the recorded $S_E$ history is
*conditional on the wrong path* wherever decisions disagree. (By contrast, $T_{\max}$
truncation **is** exact: $T_{\max}$ is a pure stop cap, so trajectory prefixes are
invariant — that half of the claim is fine.)

**Required:** split the claim. $T_{\max}$-by-truncation: exact, legitimate. $\delta$-by-
recomputation: label [APPROXIMATION], state the bias direction as unknown, bound its
influence ($\delta$ affects only the acceptance threshold; 3-value grid; frozen before
the gate). Replace the false legitimacy sentence. The tuning stays within the 15k cap
either way; honesty, not compute, is the issue (Law #11).

**Also required (tuning order):** the listed coordinate order ends with $\delta$ last,
but the shared-trajectory step computes $T_{\max}$ *and* $\delta$ together using
provisional $\lambda_c = 0.7$, *before* $\lambda$ is tuned. State the actual execution
order and which provisional values each step uses — the current text contradicts itself.

---

## 7. [MAJOR] Implementability: the support items' structure must be stated, not assumed

The ρ-gate (§4), the $\lambda$/$\delta$/$\alpha$ tuning objectives (§3.1), and the transfer
probe (§1 fix) all assume $\mathcal{D}_{\mathrm{tune}}$/$\mathcal{D}_{\mathrm{gate}}$ items
support (template $\tau$, entity slots, target/foil, rescue) evaluation. I verified against
`run_exp065_temporary_coordinate_alignment.py`: the support pairs' **p_rel prompts**
("Premise: A outranks B… Question: Who is higher in rank…?") do have relational-template
structure with a determinate correct answer (A) — so the assumption is *satisfiable*, and
the loop spec §2.2's "holds by construction" is correct for the 150 support items.

**Required:** say so explicitly in the protocol — "tune/gate items are the support pairs'
p_rel relational prompts with $(\tau, \{(e_i,\sigma_i)\}, t_{\mathrm{target}}, t_{\mathrm{foil}})$;
the p_neu prompts are construction scaffolding for $\Delta h$ only." An implementer
should not have to reverse-engineer EXP065 to discover what $x \in \mathcal{D}_{\mathrm{gate}}$
*is*. If any tuning objective cannot be computed on support items as constructed, that is
a protocol defect to fix now, not at execution.

---

## 8. [MAJOR] C7: computable and fair — with three gaps

$N(x) = F(x)$ **is** computable (C3 runs first per instance; $F(x)$ is recorded) and the
matching is fair *in the pre-registered unit* (total forward passes). Required fixes:

- **C7a:** pre-register the BoN sampling seed (Law #13 — C4/C5 have seeds; C7 doesn't).
- **C7b:** define the per-sample vote as $\arg\max_{t \in \{t_{\mathrm{target}}, t_{\mathrm{foil}}\}}
  \mathrm{logit}_t$ (restricted two-token decision, matching the primary endpoint).
  "Majority vote over $\{t_{\mathrm{target}}, t_{\mathrm{foil}}\}$ decisions" is ambiguous
  about samples whose top-1 is neither token.
- **C7c:** correct the NOTE's overclaim. "C7 can never be accused of a compute advantage in
  either direction" is false: in *decision-sample* terms BoN gets $F(x)$ decision samples
  while the loop's $F(x)$ includes non-decision $\mathcal{E}$ passes — the matching is
  **generous to BoN**, biasing F5 conservatively against the loop. Say exactly that
  (pre-registered, intended, A-budget).

---

## 9. [MINOR] G₁-from-$\mathcal{D}_{\mathrm{tune}}$-at-all-times: accept, but label honestly

The Phase 2 hardening (§8.3) was about **gate-time** cleanliness (don't validate
$\mathcal{E}$ on data that generated its candidates). Extending it to the **test phase**
is *not* "the conservative reading" of that fix — it is a **disambiguation of a loop-spec
ambiguity** (§2.1 says "support contrast pairs ($k=1..5$, $j=1..30)"; post-S3-split the
resampling source is unspecified). The extension is acceptable and I do not require
reverting it: it keeps $\mathcal{D}_{\mathrm{gate}}$ quarantine auditable ("neither its
vectors nor its labels are used thereafter" — simple, checkable), it makes the gate and
test generator-distributions identical (so the ρ-gate's validation applies cleanly), and
it is a *harder* test for the loop. But the protocol must state the rationale and the
cost: test-phase candidates are weaker than the spec's 150-pair resampling, so the tested
object is the $\mathcal{D}_{\mathrm{tune}}$-restricted loop variant — a critic may note
this, and the protocol should concede it upfront rather than have it discovered.

---

## 10. [MINOR] Budget: honest, with mechanical updates

The §12 arithmetic checks out ($15{,}000 + 2{,}650 + 3{\times}32{,}700 + 300 \approx
116{,}000$; $14{,}700$ at defaults matches the loop spec; $F(x)$ formula verified).
Worst-case + expected + 5-instance pilot requirement is the honest structure. Required
mechanical updates only: +≈800 probe passes; test-phase lines at N=45; statics at 225;
G3's +300; C7a seed (no cost change). The 15k tuning cap [ARBITRARY] is coherent
(tuning ≈13% of worst-case total; cap-binds → documented as budget-limited). The
410m [ESTIMATE] is properly quarantined as out-of-scope.

---

## 11. Verified clean (checked independently, not on trust)

- ρ-gate effect-size arithmetic ($\hat\rho \gtrsim 0.235$ floor at $n=50$, $p<0.05$) ✓
- SHA-256 binding guard with the E-4 registered-value distinction (EXP067 §2) ✓
- Law #13 archiving — the T-1 lesson is applied (candidates, $S_E$ scores, per-view
  decisions, $z_T$ histories, gate record, tuning grids) ✓
- Margin shifts exploratory-only (O5 stands; $\tilde{M}$ licensed solely by the gate) ✓
- Headroom gate with halt-as-reportable-outcome semantics ✓
- C8 positive-control discipline (EXP067 §7.1 branch-(b) logic preserved) ✓
- $B_0 := B_{\mathrm{agg}}$ incumbent justification (conservative by construction) ✓
- Tweak-and-rerun forbidden; changed design = EXP069 (Law #4) ✓
- N1 framing in §1.1/§14 — holds under current user pressure for revolutionary language;
  no N2 creep in any branch's LICENSES (after D2 fix) ✓
- $T_{\max}$-by-truncation exactness ✓; coordinate-wise tuning as the faithful reading of
  loop-spec §1.1 ✓; $m=5$ fixed ✓; $k=1$ restriction pre-registered ✓

---

## 12. Consolidated required fixes (do not edit the draft until all are addressed)

**FATAL (sign-blocking):**
- **T1** — Add the §4b transfer probe (15 carved items, N=45 test, $p \ge 0.20$ halt screen,
  branch (a2), branch-(d) rider, budget/checklist/§9 updates).

**MAJOR:**
- **G1** — Define $\mathbf{1}[\mathrm{rescue}]$; budget the unintervened pass.
- **G2** — Report rescue base rate; pre-register the low-information caveat.
- **G3** — Add the exploratory $B_0$-relative $\Delta$-diagnostic (+300 passes).
- **K1** — C4 computes $S_E$ identically, selects random ignoring scores (fix text to match
  the budget table's "compute-matched").
- **K2** — Scope the F3 attribution rider to demonstrated $\Delta M$; report $(b,c)$
  decomposition; soften (f2) LICENSES.
- **K3** — Add (f1) LICENSES / DOES-NOT-LICENSE.
- **K4** — (d)-before-(g)/(f)/(e) precedence; F4 as diagnostic characterization of (d).
- **D1** — Full branch precedence: (a)/(a2) → (b) → (c) → (d) → (g) → (f) → (e).
- **D2** — (e) conditional licensing on the C3-vs-C7 comparison.
- **D3** — Labeled note on H_loop's "beats" vs the "not dominated" operationalization.
- **T2** — $\delta$ recomputation labeled [APPROXIMATION]; replace the false legitimacy
  sentence.
- **T3** — Reconcile the tuning execution order with the shared-trajectory step.
- **T4** — State the support items' $(\tau, \mathrm{slots}, \mathrm{target}, \mathrm{foil})$
  structure explicitly (p_rel prompts; p_neu is scaffolding).
- **C7a/b/c** — BoN seed; per-sample vote definition; honest bias-direction NOTE.

**MINOR:**
- **M1** — G₁ extension labeled as spec disambiguation with rationale + cost conceded.
- **M2** — F2/F4 full-distribution reporting for the promised sensitivity analysis.
- **M3** — "STOP rules" reworded (only F1 halts; F2–F5 are falsification triggers).
- **M4** — Range-restriction note on the gate's primary analysis.
- **M5** — Budget table mechanical updates (probe, N=45, G3).
- **M6** — Fix the dangling "reviewer's notes (§13)" reference.

**Recommended (non-blocking):** report gate and probe $\hat\rho$ values side-by-side in all
outcomes (tracks degradation even when both pass); pre-register the 45-item headroom
recalibration explicitly (baseline ∈ [40%,70%] on the carved set).

---

## 13. Bottom line

This is a strong draft — the gates, the halt semantics, the LICENSES discipline, and the
N1 framing are all correct in structure. Its one fatal flaw is the hole the drafter found
itself: without a transfer check, the experiment's canonical falsification cannot
distinguish "the loop fails" from "the evaluator doesn't transfer," and branch (d)'s
structural interpretation would then be a confounded claim wearing a pre-registered
ruling. The probe closes it for ≈800 forward passes. Fix T1–C7c, re-verify the diff, sign.

*No results exist under this protocol. No primary artifacts were touched. No bundle files
were edited (none exist yet). This review changes no numbers — it changes what the
protocol is allowed to claim.*

---

## 14. Re-review of corrections (Law #14) — 2026-09-23

**Verdict: SIGN-WITH-FIXES** — one new MAJOR (a genuine edge-case hole in the implemented
T1 fix itself, one-line fix), two MINORs. The draft is not yet the signed pre-registration.

### 14.1 Verified by independent computation (not on trust)

- **T1 transfer probe — present and structurally correct.** §4b contains every required
  element: $\mathcal{D}_{\mathrm{xfer}}$ = 15 items carved by fixed seed 68024 before any
  test-phase execution, permanently excluded afterward (confirmatory N=45); HALT iff
  $\hat\rho_{\mathrm{xfer}} \le 0$ or one-sided $p \ge 0.20$; branch (a2) well-formed with
  LICENSES/DOES-NOT-LICENSE; phase order tuning → gate → probe → headroom(on 45) →
  test(on 45); budget table carries the probe at ≈810 passes ($15 \times 53 = 795$ + 15
  unintervened, §12).
- **t→ρ arithmetic — verified exactly (scipy).** One-sided $p = 0.20$ at $n=15$ (df=13)
  ⟺ $t \approx 0.870$ ⟺ $\hat\rho \lesssim 0.2346$; the gate's floor at $n=50$ (df=48) is
  $\hat\rho \gtrsim 0.2353$. "Exactly the gate's effect-size floor, re-expressed at
  reduced $n$" is true to three decimals. $p < 0.05$ at $n=15$ would require
  $\hat\rho \gtrsim 0.441$ — the draft's stated 0.44 is correct.
- **"80% by construction" sensitivity — verified analytically and by Monte Carlo.**
  $P(\mathrm{halt} \mid \rho=0) = 1 - P(\hat\rho>0 \land p<0.20) = 1 - 0.20 = 0.80$
  exactly (one-sided $p<0.20$ implies $\hat\rho>0$); MC (60k reps) gives 0.798.
- **(d) structural-reading precondition — present in all three required places:** the
  (d) ruling cell ("Precondition: transfer probe passed… had the probe halted, (a2) —
  not (d) — would have fired"), the §11 interpretation paragraph, and the §10 positive
  criterion ("transfer probe passed (§4b)"). The precedence chain (a2 before everything)
  additionally enforces it structurally: (d) cannot fire after a probe halt because the
  run stops.
- **Majors spot-check — all confirmed in the text:** $\mathbf{1}[\mathrm{rescue}]$ defined
  once (§4 G1) and referenced identically in §4b and G3; C4 truly compute-matched (§6 text
  matches the §12 budget line — the EXP067-bundle F1 lesson applied); $\delta$ labeled
  [APPROXIMATION] with the false legitimacy sentence **withdrawn for $\delta$** and
  correctly retained for $T_{\max}$ truncation; branch precedence
  (a)/(a2)→(b)→(c)→(d)→(g)→(f)→(e) pre-registered in §11; (e) conditional licensing (D2)
  present; H_loop "beats" vs "not dominated" softening labeled in §1 (D3); C7 seed 68025,
  per-sample vote definition, honest bias-direction NOTE, overclaim withdrawn; support-item
  $(\tau, \mathrm{slots}, t_{\mathrm{target}}, t_{\mathrm{foil}})$ structure stated in §5 (T4).
- **Budget — arithmetic verified:** $15{,}000 + 2{,}700 + 300 + 810 + 3 \times 24{,}525 +
  225 = 92{,}610 \approx 93{,}000$ worst-case at N=45. $93{,}000 \times 0.5\,\mathrm{s} =
  12.9\,\mathrm{h} \approx 13\,\mathrm{h}$ — the wall-clock is marked
  [CONJECTURE — pending hardware measurement] with a 5-instance pilot requirement to
  rescale from measurement. Honest.
- **N1 defense — holds.** §1.1 and §14 unchanged in framing; no fix introduced
  novelty-tier language; no branch licenses N2; "invention" still appears only in the
  program name and the prohibition. The review's §0 defense stands un-eroded.

### 14.2 Required fixes

**MAJOR — P1 (degenerate transfer probe; one-line fix, sign-blocking):**
The probe halt rule "HALT iff $\hat\rho_{\mathrm{xfer}} \le 0$ or one-sided $p \ge 0.20$"
is undefined when the probe rescue indicator has zero variance (all 15 items rescued or
none rescued → $\hat\rho$ NaN, $p$ NaN; NaN comparisons are False). The probe then
**passes vacuously** and the run proceeds to the test phase with the transfer confound
unscreened — resurrecting exactly the confound T1 was built to kill, after which branch
(d) could fire with its structural reading. This is not negligible under skewed rescue
base rates: at base rate 0.9, P(all 15 rescued) ≈ 0.21. The gate has G2's low-information
flag; the probe has no base-rate or degeneracy handling at all. Required: pre-register a
degenerate-probe rule — e.g. "zero-variance probe rescue indicator → probe inconclusive →
HALT with an (a2)-style report (transfer unscreened)" — or an explicit alternative. An
implementer must not improvise this at execution.

**MINOR — m1 (false-halt risk numbers not reproducible):** the pre-registered
"P(false halt) ≈ 18% at true $\rho=0.5$, ≈10% at true $\rho=0.6$" could not be reproduced:
independent Monte Carlo under latent-normal DGPs (rescue base rates 0.3/0.5/0.7) gives
≈10–13.5% and ≈3–5%. The error is in the conservative direction (overstates the probe's
cost) and these are disclosures, not gating thresholds — but the DGP is unstated, so the
numbers are unverifiable. Fix: state the DGP that yields the quoted values, or re-derive
/ soften to an order-of-magnitude statement.

**MINOR — m2 ((f4) tidiness):** sub-branch (f4) is listed in the (f) row but carries no
LICENSES statement of its own and is unreachable under the pre-registered precedence
(F4's condition implies $\Delta M \le 0$, so (d) always fires first). Harmless; add "(f4)
characterized under (d)+F4" for tidiness.

### 14.3 Bottom line

The corrections are faithful and the arithmetic at the heart of T1 is exact — but the
re-review caught a real edge-case hole *in the T1 fix itself*: a degenerate probe passes
silently. One line closes it. Fix P1 (and m1/m2), and the protocol signs.

### 15. Final focused verification (P1/m1/m2) — 2026-09-23 — VERDICT: **SIGN**

**Scope:** verify exactly three corrections, by reading the spec (`experiments/protocols/EXP068_LOOP_PREREG_SPEC.md`, 595 lines). No redesign authority; no threshold authority.

**P1 — degenerate-probe rule: VERIFIED.** The rule exists as a `[DEFINITION]` block in §4b immediately after the halt criterion: zero-variance probe rescue indicator on $\mathcal{D}_{\mathrm{xfer}}$ → inconclusive → **HALT** with an (a2)-style reportable outcome ("transfer unscreened — probe degenerate"); $\hat\rho_{\mathrm{xfer}}$/$p$ recorded as undefined; a degenerate probe must NOT pass and must NOT be silently dropped; the ~0.21-scale motivation (base rate 0.9) is stated. It is also in the (a2) branch's §11 trigger list ("or degenerate zero-variance probe → inconclusive, §4b") with the reporting rule (record $\hat\rho$/$p$ as undefined, report the zero-variance indicator record and the probe rescue base rate). **Closure trace:** the degenerate rule fires on the indicator's *variance* — a condition independent of $\hat\rho$/$p$ — so the NaN-vacuous-pass path (NaN comparisons evaluate False → old halt rule passes) is unreachable: the run halts before the old rule is ever evaluated. The trigger covers the full binary degenerate case (all 15 rescued or none rescued). Phase order (probe → headroom → test) means no degenerate probe can proceed to the test phase. **The T1 confound cannot be resurrected through this hole.**

**m1 — false-halt risks under stated DGP: VERIFIED.** The risks are now ≈10–12% at true $\rho=0.5$ / ≈3–5% at true $\rho=0.6$ under an explicit biserial-normal DGP ($R \sim \mathrm{Bernoulli}(b)$, $S = \rho(R-b)/\sqrt{b(1-b)} + \sqrt{1-\rho^2}\,\varepsilon$, population point-biserial exactly $\rho$), with the method stated (12,000 reps, 499 permutations, degenerate probes counted as halts contributing ≤0.5%), the 80%-by-construction sensitivity with independent MC (0.805), cross-validation against this review's independent MC (10–13.5% / 3–5%), and a named DGP-sensitivity disclosure (latent-$Z$ parameterization: ≈22–26% / ≈12–16%). The old 18%/10% numbers appear only in the replacement disclosure ("belonged to an unstated DGP and could not be reproduced — those numbers are replaced here, not silently kept"). Internally consistent; no contradiction with §14.2.

**m2 — (f4) tidiness: VERIFIED.** The (f) row now reads "(f4) F4 blind-spot pattern — characterized under (d)+F4".

**Surgical-diff check: CLEAN.** 564 → 595 lines (+31), fully accounted for by P1's ~20-line `[DEFINITION]` block and m1's ~10-line paragraph expansion. Single `HALT iff` occurrence (unchanged wording); single degenerate-probe rule; (a2) row extended with the degenerate trigger; the (d) structural-reading rider intact and still conditional on probe passage; N1 framing untouched — the diff is confined to §4b and the (a2)/(f) rows of §11. No threshold meaning altered; no gate softened or strengthened; no new language anywhere else.

**VERDICT: SIGN.** `experiments/protocols/EXP068_LOOP_PREREG_SPEC.md` (595 lines, 2026-09-23) is now the **SIGNED pre-registration** for EXP068. Law #14 satisfied: drafted → adversarially reviewed → corrected → re-reviewed → corrected → verified. The protocol's honesty machinery (pre-registered halts, the ρ-gate, the §4b transfer probe with its degenerate rule, kill criteria F1–F5, LICENSES/DOES-NOT-LICENSE on every branch, N1 framing) is intact and sign-off is final. Any design change from this point forward is EXP069-or-later, never a silent edit to this artifact.

### 16. Focused Law #14 verification of the Mathematics Auditor corrections (pinned ρ-gate permutation parameters + degenerate-gate rule) — 2026-09-23 — VERDICT: **SIGN**

**Scope:** verify exactly two surgical corrections flagged by the Mathematics Auditor and applied by the corrections integrator, by reading the spec (`experiments/protocols/EXP068_LOOP_PREREG_SPEC.md`, now 621 lines). No redesign authority; no threshold authority. Governing: `AGENTS.md` Laws #4/#13/#14, `MATH_STANDARDS_CHARTER.md` M5.2 (exhaustive partition) and M5.3 (pinned parameters + degenerate-input handling, now binding).

**C1 — pinned permutation-test parameters: VERIFIED.** §4 carries a `[DEFINITION]` block ("Permutation-test parameters (pinned, Law #13; closes M5.3 MINOR)"): one-sided $p$ is the Monte Carlo approximation to the exact permutation p-value with **$B = 9{,}999$** random label permutations, plus-one convention $p = (1 + \#\{\hat\rho_{\mathrm{perm}} \ge \hat\rho_{\mathrm{obs}}\})/(1 + B)$, fixed seed **`perm_seed = 68026`** [ARBITRARY — any fixed value; recorded here; the seed and the realized $p$ are archived in the gate record per Law #13]. One-line rationale present: MCSE $\sqrt{0.05 \cdot 0.95 / 9999} \approx 0.0022$ at the $p = 0.05$ boundary; pinned seed makes the realized ruling deterministic and exactly reproducible. **Arithmetic independently recomputed:** MCSE $= 0.002180 \approx 0.0022$ ✓; denominator $1 + B = 10000$ ✓; the pre-existing effect-size floor is consistent — $t_{48,0.95} = 1.6772 \Rightarrow \hat\rho \gtrsim 0.2353$ ✓. No gate semantics changed: GO is still $\hat\rho > 0$ AND one-sided permutation $p < 0.05$ on $n = 50$.

**C2 — degenerate-gate rule: VERIFIED.** §4 carries a `[DEFINITION]` block ("Degenerate-gate rule (pre-registered; mirrors §4b; closes the ρ-gate partition gap, M5.2)"): if $\mathbf{1}[\mathrm{rescue}]$ has zero variance on $\mathcal{D}_{\mathrm{gate}}$ (all 50 rescued or none), $\hat\rho$ and its permutation $p$ are undefined → the gate is **inconclusive** → **HALT**, reported exactly as branch (a) with the degenerate case named ("ρ-gate degenerate — rescue indicator constant on $\mathcal{D}_{\mathrm{gate}}$; evaluator unscreened"); a degenerate gate must NOT pass and must NOT be silently dropped; $\hat\rho$/$p$ recorded as undefined, plus the zero-variance indicator record and the gate rescue base rate. **Motivation arithmetic recomputed:** $0.9^{50} \approx 0.0052 \approx 0.005$ ✓ — expected-scale, not pathological. **F1 (§10) conforms:** "ρ-gate fails ($\hat\rho \le 0$ or one-sided permutation $p \ge 0.05$, or degenerate zero-variance gate → inconclusive, §4)" ⇒ HALT before test. **Branch (a) (§11) conforms:** trigger "($\hat\rho \le 0$ or $p \ge 0.05$; or degenerate zero-variance gate → inconclusive, §4)"; license distinguishes non-degenerate ("$\mathcal{E}$ **invalid** … H_loop is **untestable under this evaluator**") from degenerate ("**inconclusive, not invalid**: the gate measured nothing about $S_E$'s signal — rescue indicator constant on $\mathcal{D}_{\mathrm{gate}}$; evaluator unscreened"); reporting rule complete for both cases. **Mirrors the §4b/(a2) precedent without contradiction:** separate gates, consistent semantics (variance-fired, inconclusive-not-invalid, must-not-pass, base-rate reported).

**Exhaustive partition (M5.2): VERIFIED.** Every (variance × $\hat\rho$ × $p$) cell lands in exactly one branch:
- var>0 ∧ $\hat\rho>0$ ∧ $p<0.05$ → **GO** (test phase proceeds)
- var>0 ∧ $\hat\rho>0$ ∧ $p\ge0.05$ → **(a)** HALT (via "$p \ge 0.05$")
- var>0 ∧ $\hat\rho\le0$ (any $p$) → **(a)** HALT (via "$\hat\rho \le 0$")
- var=0 → **(a)** inconclusive (degenerate rule)
- boundary $\hat\rho=0$ → (a) via "$\hat\rho \le 0$"; boundary $p=0.05$ → (a) via "$p \ge 0.05$" (GO requires strict $<$)
- var=0 ∧ $\hat\rho$-defined → **impossible** (M5.4 one-liner: a constant indicator leaves one class empty, so the group means defining the point-biserial $r_{pb}$ do not exist)
- no double-rule: NaN $\le$ 0 evaluates False, so the degenerate clause is the only operative trigger for var=0.
**Closure trace:** the rule fires on the indicator's *variance* — a condition independent of $\hat\rho$/$p$ — so the NaN path is unreachable; the run halts before the GO rule is ever evaluated. Same closure logic as the P1 probe verification (§15). The ρ-gate's asymmetry with the probe (the Math Audit's original complaint) is closed.

**Surgical-diff check: CLEAN.** The spec is untracked in git, so verification was by full read plus targeted grep (same method as the EXP070 focused verification). The only M5.2/M5.3 closure markers in the file are the two new `[DEFINITION]` blocks; the F1 (§10) and branch-(a) (§11) trigger/license text conforms; the §4b/(a2) degenerate-probe machinery is untouched. N1 framing (§1.1) intact; all thresholds, gates, and license substance elsewhere read unchanged.

**Non-blocking observations for the execution-bundle author (not findings):** (i) the degenerate rule's NaN parenthetical ("NaN comparisons evaluate False, so the GO rule above would pass the gate vacuously") is implementation-pattern-dependent — under `GO = (ρ̂>0 ∧ p<0.05)` NaN makes GO False (gate fails); the vacuous-pass path is via the failure-check negation. The operative rule is unambiguous regardless: implement as an **explicit variance assertion before computing ρ̂**, never rely on NaN-propagation semantics. The closure trace holds for any compliant implementation. (ii) `perm_seed = 68026` is recorded in §4 with archiving mandated per Law #13; the §13 seed summary list does not echo it — tidiness only. (iii) Carried residuals already named in the integrator's log (LOG-091): the measure-zero edge of constant $S_E$ across all 50 pairs with varying rescue also makes $\hat\rho$ undefined and is unruled (practically impossible with $K=8$ bootstrap candidates); and the §4b transfer probe's permutation $p$ remains unpinned — flagged for the same treatment when the probe's execution code is written.

**VERDICT: SIGN.** The amended protocol (621 lines, 2026-09-23) **stands cleared for execution-bundle construction**. The Mathematics Auditor's two corrections are faithfully integrated: the ρ-gate's M5.2 partition is now exhaustive and its M5.3 reproducibility requirement satisfied. Law #14 chain for this amendment: auditor-flagged → corrected → independently verified. Any design change from this point forward remains EXP069-or-later.
