# Adversarial Review — EXP070 Pre-registration (Oracle-Selection Ceiling)

**Role:** Adversarial Reviewer (Law #14)
**Date:** 2026-09-23
**Verdict:** **SIGN-WITH-FIXES** — 5 MAJOR required fixes (M1–M5), 6 minors (m1–m6). Do not sign until M1–M5 are applied and the diff re-reviewed.
**Draft reviewed:** `experiments/protocols/EXP070_ORACLE_CEILING_PREREG_SPEC.md`
**Sources read:** `.agents/agents/adversarial-reviewer.md`, `AGENTS.md` (14 laws),
`research/innovation/SPRINT_2026-09-23.md` (Idea 2), `theory/LOOP_SPEC_DRAFT.md`,
`experiments/protocols/EXP067_QKOV_SUBSPACE_PROCRUSTES_SPEC.md`,
`experiments/protocols/EXP068_LOOP_PREREG_SPEC.md` (§2, §11 — cross-checked claims).

---

## Executive summary

The core methodology is sound: the verifier-first ceiling argument is valid, the probe-oracle
avoids test-label contamination (an improvement over the sprint sketch's test-label argmax —
see m5), the anti-cheat structure is nearly airtight, the 7 conditions isolate the right
contrasts, and the budget fits free-tier compute. The draft's honesty infrastructure (named
assumptions, LICENSES / DOES NOT LICENSE per branch, A-pool explicitly flagged for attack)
is at the EXP067 standard.

But the decision procedure has five load-bearing flaws, two of them capable of producing a
false kill of EXP068 — the exact failure mode this pre-test exists to avoid committing:

1. **M1:** Branch (d) is mathematically unreachable and the +8pp bar is vacuous — and the
   draft's own justification sentence for +8pp is arithmetically false.
2. **M2:** The kill branch (c) is not gated on probe signal. A 5-item probe over 17 candidates
   is noise-dominated; the B_agg tie-break then defaults the oracle to static, manufacturing
   kills out of measurement noise. The diagnostics exist but don't gate the ruling.
3. **M3:** The "conservative" tie-break toward B_agg biases the *ceiling* toward the kill, and
   §3.5(3)'s "deliberately generous" reasoning is backwards (winner's curse attenuates the
   measured ceiling; it does not inflate it).
4. **M4:** Branch (c) claims "H_loop is DEAD." H_loop (loop spec §5) is the *adaptive,
   target-free* loop; EXP070 tests label-informed selection over a static pool. The kill
   cannot falsify H_loop — it withdraws EXP068's cost-benefit justification. The license
   overstates what was tested.
5. **M5:** Anti-cheat asserts probe∩test = ∅ but never support∩test = ∅, though candidates
   are built from the full support set.

None requires redesigning the experiment. All are fixable on paper. Hence SIGN-WITH-FIXES,
not REJECT.

---

## MAJOR findings (required)

### M1 — Branch (d) is unreachable; the +8pp bar never binds; the justification sentence is false

[FACT — verified by direct computation.] Under exact two-sided McNemar at α = 0.05:

- (b=5, c=0): p = 2·(½)⁵ = **0.0625** — not significant.
- (b=6, c=0): p = 2·(½)⁶ = **0.03125** — significant.
- With corruptions the floor is higher (b=8, c=1 → p = 0.039, net 7).

So any significant oracle-vs-static difference on N ∈ [50, 60] implies |ΔM| ≥ **10pp**
(6/60; 12pp at N=50). The joint branch-(e) condition (margin ≥ +8pp **and** p < 0.05) is
therefore decided by the p-value alone — the +8pp margin threshold is strictly redundant.
**Branch (d)** ("wins small": p < 0.05 but margin < +8pp) **cannot fire on the pre-registered
N range.** It is dead code in the decision tree.

Consequences:
- (a) The draft's justification sentence — "+8pp ≈ 5 net rescued items with McNemar p < 0.05"
  (§8) — is **false**: 5 net pure rescues give p = 0.0625, not p < 0.05.
- (b) The "survives halving" rationale is internally inconsistent: the effective bar is the
  ~10pp significance floor, so a halved gap (~5pp) would fall *below* the detection floor on
  N=60. A bar that "survives halving" would need to sit near ~20pp, not 8pp.
- (c) The +4pp sensitivity band is below the significance floor — reporting "the ruling at
  +4pp" is vacuous. Only the +12pp band can actually discriminate.

**Required fix:** re-derive the worth-chasing bar honestly. Either (i) remove branch (d) and
restate the bar so it actually binds (e.g., a magnitude judgment on the significant gap —
report the observed oracle–static gap with 95% CI and pre-register the "worth chasing"
criterion on the CI, such as lower bound clearing a stated floor), or (ii) prove branch (d)
reachable under a stated alternative (it is not, under the current test). The sensitivity
analysis must be re-centered above the significance floor. Any threshold that remains without
derivation keeps its [ARBITRARY] marking.

### M2 — The kill is not gated on probe signal; the apparatus manufactures kills from noise

[INTERPRETATION — structural.] The oracle selects argmax over 17 candidates on a **5-item**
probe. Each candidate's probe score takes only 6 values {0, 0.2, …, 1.0}; the standard error
of a candidate's mean probe correctness is ≈ 0.22 at p = 0.5. Ties are rampant, and the
tie-break cascade (self-margin → pool index → **B_agg wins**) resolves most selections
without probe signal. Net effect: whenever the probe is uninformative, the oracle *defaults
to static*, ΔM_oracle − ΔM_static = 0 follows mechanically, and **branch (c) fires on noise**.

The draft has the right diagnostics — §6(i) (fraction of instances with strict probe wins
over B_agg) and §6(ii) (point-biserial probe-margin↔rescue correlation) — and A-probe even
names the risk. But the decision tree does not gate on them: "branch (c) must be read with
that caveat logged" (§7) while **EXP068 is cancelled anyway**. A caveat attached to a
cancellation is not a safeguard; it is a footnote on an execution.

**Required fix:** gate branch (c) on probe signal. Minimum structure:

- **(c1) Kill:** probe diagnostics show the oracle *had* signal (pre-register the floor —
  e.g., diagnostic (i) ≥ 25% [ARBITRARY] and/or diagnostic (ii) r_pb significantly > 0)
  yet no test gain → H_loop's justification is withdrawn; EXP068 cancelled.
- **(c2) Uninformative:** probe diagnostics show no signal → the ceiling was **unmeasured**,
  not zero. EXP068 is **not** cancelled. Required next step: re-register with a better probe
  (see recommendation below), never a silent re-run.

**Recommendation (not required):** enlarge the probe to 2 items per vocabulary (10 items):
17 × 10 × 60 + 420 = 10,620 passes ≈ 90 min conservative — still fits free-tier. This halves
the selection-noise SE and makes (c1) vs (c2) easier to separate.

### M3 — The tie-break is kill-ward, not conservative; §3.5(3)'s "generous" reasoning is backwards

Two claims in the draft point in opposite directions:

1. §3.3: "Conservative tie-break toward the incumbent: if B_agg is among the top-tied
   candidates, it wins the tie — the oracle deviates from static only on a *strict* probe win."
   Called "conservative." **Conservative for whom?** It shrinks the oracle–static gap, making
   branch (e) harder and branch (c) easier. It is conservative for the *justification* claim
   and anti-conservative for the *kill* claim. In a pre-test whose kill cancels a research
   direction, biasing the instrument toward the kill is the wrong direction.
2. §3.5(3): "The ceiling is deliberately generous: candidates are built from the same support
   items the oracle probes on. This makes an oracle *loss* more damning." **This is backwards.**
   Evaluating candidates on the items they were built from induces *winner's curse*: the oracle
   selects the candidate that best fits 5 noisy probe items, which then regresses on the test
   item. Probe-overfitting **attenuates** the measured test ceiling; it does not inflate it.
   The design is not generous — it is kill-ward by a second, independent mechanism.

**Required fix:** (a) make the tie-break direction-neutral — drop the B_agg preference;
use the remaining deterministic cascade (probe correctness → seeded-random or index order,
pre-registered) and state its neutrality implication; (b) correct §3.5(3): name the
winner's-curse attenuation honestly as a *limitation* of the ceiling measurement (it makes
kills easier, not more damning), and let the significance + magnitude bar (post-M1 fix)
carry the conservatism for justification, where it belongs.

### M4 — "H_loop is DEAD" overstates the license; the 2-step ring is a false remedy (A-pool ruling)

The draft invites attack on A-pool first; here it is.

**On the feared scenario:** the draft worries the rescuing direction lies "2+ perturbation
steps from every G1 candidate." But [FACT — computed]: with σ = 0.1 in d = 768,
E[cos(v, normalize(v+ε))] ≈ 1/√(1+dσ²) = 1/√8.68 ≈ **0.34** — a ~70° cone, not a local
neighborhood. The "1-step ring" is a **wide spray**, and a hypothetical "2-step ring" would
sit at cos ≈ 0.12 from its parent — nearly orthogonal, i.e., nearly random. Two consequences:

- (a) A static 2-step ring would **not** address the adaptivity gap anyway: no static snapshot
  captures re-centering on accepted incumbents. Demanding it would be security theater —
  budget spent to look rigorous while leaving the real gap untouched. **Do not add it.**
- (b) The wide step size actually *strengthens* the ceiling argument: with 70° steps there is
  little hill to climb — the loop's G2 is closer to repeated random search with selection
  than to fine hill-climbing, and the static pool (sprays around all 8 G1 draws) represents
  that search faithfully. The draft should state this angular scale honestly (see m6) rather
  than leaving "local perturbation" unquantified.

**On the license (the real fix):** H_loop is defined in `theory/LOOP_SPEC_DRAFT.md` §5 as the
*adaptive, target-free* G/E/S/T loop. EXP070 tests *label-informed* selection over a *static*
pool. These are different hypotheses. "H_loop is DEAD within the pre-registered search family"
is a category error — H_loop does not live in that family. What branch (c) can honestly
license: **"no label-informed selection over this pool beats static here; the cost-benefit
justification for building EXP068 is withdrawn; EXP068 is cancelled in its current form."**
The practical effect (cancellation) is unchanged; the epistemic statement is now true.

**Required fix:** reword the branch-(c) LICENSES cell to the justification-withdrawal
framing; add to DOES NOT LICENSE: "falsification of the adaptive loop hypothesis (never
tested)"; and add the re-motivation path: "a future loop protocol motivated by a *different*
candidate family (e.g., a positive EXP075 subspace result) is a new pre-registration, not a
resurrection of the killed justification." The §1.2 oracle-loss column needs the same
correction wherever it says H_loop "is dead."

### M5 — Anti-cheat asserts probe∩test = ∅ but never support∩test = ∅

Candidates are built from the **full support set** (150 pairs), while the runtime
disjointness assertion (§3.2) and the post-run audit (§3.5(1)) cover only probe∩test.
If any support item coincided with a test item, candidates would be built from test data —
a leakage path the assertions do not close. The sets are *defined* disjoint (loop spec §1),
but the audit must verify, not assume.

**Required fix:** add runtime assertion `support_ids ∩ test_ids = ∅` (and archive both id
lists — already required by §10) alongside the existing probe∩test check.

---

## MINOR findings

- **m1 — EXP071 numbering collision.** The header note correctly vacates the sprint's
  provisional EXP071 (Idea 3) and states "changed design under EXP070 = EXP071." But §9
  then pre-names the 410m replication "EXP071." Both cannot hold. Fix: §9 should say the
  410m replication "takes the next free number at pre-registration time" (the header note's
  own formula for Idea 3), not pre-claim EXP071.
- **m2 — "Never better" overstatement.** §1.2 [NOTE]: "a realizable loop can only do worse
  than the oracle, never better, *within the pool*." On any given realization a lucky
  target-free pick can match the oracle. Qualify: "cannot *systematically* beat" / "in
  expectation."
- **m3 — Margin as tie-break.** §3.3 tie-break step (1) uses mean probe self-margin —
  the O5-invalidated concept. As a tie-break (not an endpoint) it is arguably benign, but it
  imports margin noise into selection. Either justify in one sentence (tie-break ≠ endpoint)
  or drop to the deterministic cascade. (Partially subsumed by M3's required rework.)
- **m4 — Gate ordering.** §5 says the probe-construction gate runs "before anything else";
  §9's 5-instance pilot measures wall-clock. State the order explicitly:
  probe-construction/N_final gate (metadata, no GPU) → pilot (GPU) → full launch.
  Consider having the pilot also report the probe-yield estimate.
- **m5 — Undocumented improvement over the sprint sketch.** The sprint's Idea 2 kill criterion
  specifies "argmax-rescue per instance" — readable as test-label argmax. The draft's
  probe-oracle (support analogs only; test labels purely evaluative) is strictly better
  (avoids contaminating the ceiling), but the deviation is never documented. Per Law #12,
  add one sentence noting and justifying it.
- **m6 — Unquantified "local perturbation."** State the effective angular scale of σ = 0.1
  (E[cos] ≈ 0.34, ~70° cone in d = 768) in §3.1. It bears directly on the A-pool argument
  (see M4): wide steps make the static snapshot a *better* proxy for the adaptive path, and
  the reader deserves the number, not the adjective "local."

---

## Target-by-target summary (the 8 assigned probes)

| # | Target | Finding |
|---|---|---|
| 1 | A-pool false-kill route | License tightening required (M4); 2-step ring rejected as false remedy; angular-scale analysis strengthens the ceiling logic when stated honestly (m6) |
| 2 | +8pp [ARBITRARY] threshold | Vacuous — significance floor dominates; branch (d) unreachable; justification sentence false (M1) |
| 3 | Probe noise / stability | Noise-dominated selection + kill-ward tie-break; diagnostics must gate the kill (M2); consider 10-item probe |
| 4 | Tie-break toward B_agg | Kill-ward, not conservative; §3.5(3) reasoning backwards — winner's curse attenuates, not inflates (M3) |
| 5 | 160m vs 410m | Clean: EXP068's in-scope model is 160m (verified in EXP068 draft §2), kill scoped to "this benchmark/model/layer," 410m correctly deferred — except the §9 EXP071 pre-naming collision (m1) |
| 6 | Anti-cheat | Nearly airtight (probe discipline, deterministic construction, post-run audit, Law #7 scoping for the oracle); one gap: support∩test assertion missing (M5) |
| 7 | Budget | Arithmetic verified: 17×5×60 = 5,100 + 420 = 5,520 passes; 45-min conservative estimate consistent with the loop spec's rate basis; pilot requirement present; caching optimization legitimate |
| 8 | EXP071 vacating note | Present and unambiguous in the header note — but undermined by §9's pre-naming (m1) |

---

## Verified clean (independently checked, not on trust)

- Research question and H_ceiling/H0 are falsifiable and correctly scoped as a methodology
  pre-test, not a method (Law #4, #10).
- The pool-widening rationale (G1-only → G1 + ring + incumbent) is a documented, reasoned
  deviation from the sprint sketch that closes the "but refinement would find it" objection.
- N1 framing held: §1.1 and §11 explicitly deny novelty-tier movement in all branches,
  including under branch (e).
- α = 0.50 fixed with stated rationale (program continuity; tuning would spend the budget
  the pre-test exists to save). Per-instance α correctly listed in §12 as untested.
- Headroom gate (40–70%), N_final ≥ 50 gate, C7 positive-control invalid-run discipline,
  and halt-as-reportable-outcome semantics all match the EXP067 template standard.
- SHA-256 Δθ=0 binding guard with the E-4 binding-vs-sanity distinction; no backward pass
  anywhere; Law #6 satisfied.
- Margin-shift endpoints correctly quarantined as exploratory (O5 discipline); primary and
  kill endpoints are decision changes with McNemar exact.
- Branch (f) (C4 ≥ C3 → uninformative, not kill/justify) is the correct f2-analog and shows
  the decision tree was designed by someone who understands selection attribution.
- Branch (g) (C2 null-replication check with drift flag) is good hygiene.
- Status labels: [ARBITRARY] markings present on +8pp; [CONJECTURE] on wall-clock;
  [TO BE REGISTERED] on the SHA-256 — honest throughout. (M1's fix must preserve this.)
- Numbering note resolving the EXP068 "changed design = EXP069" vs sprint EXP069 (Idea 1)
  collision is accurate — verified against the EXP068 draft (3 occurrences) and the sprint.

---

## Verdict rationale

SIGN-WITH-FIXES rather than REJECT because: the experiment's *identity* — a cheap,
verifier-first ceiling measurement with honest anti-cheat and a complete decision tree —
is the right experiment, and every flaw found is a flaw in the *decision procedure and its
licenses*, fixable on paper without changing what gets executed. REJECT would be warranted
for test-label contamination, an unfalsifiable question, or a budget that doesn't fit —
none present.

The single most dangerous flaw is **M2**: an ungated kill on a noisy probe can cancel
EXP068 while measuring nothing, which is precisely the false-kill failure mode the draft
claims A-pool naming protects against. M1 is the cleanest technical catch; M4 is the most
philosophically load-bearing. All five must be fixed and the diff re-reviewed before signing.

---

## Required fixes checklist (for the corrections integrator)

- [ ] **M1:** re-derive the worth-chasing bar (significance floor ≥10pp on N=60); remove or
  repair branch (d); correct the "+8pp ≈ 5 net rescues, p < 0.05" sentence; re-center
  sensitivity bands above the floor.
- [ ] **M2:** split branch (c) into (c1) kill / (c2) uninformative, gated on pre-registered
  probe-signal diagnostics (i) and (ii) with stated floors.
- [ ] **M3:** direction-neutral tie-break (drop B_agg preference); correct §3.5(3)
  winner's-curse reasoning; conservatism lives in the significance+magnitude bar.
- [ ] **M4:** branch-(c) and §1.2 license reworded to justification-withdrawal (not
  "H_loop is DEAD"); add adaptive-hypothesis and re-motivation-path exclusions to
  DOES NOT LICENSE. No 2-step ring.
- [ ] **M5:** runtime assertion support_ids ∩ test_ids = ∅ + archived id lists.
- [ ] **m1–m6** as listed above.

*No draft files were edited. No primary artifacts touched. No results invented.*

---

## Re-review (diff verification) — 2026-09-23

**Role:** Adversarial Reviewer (Law #14, second pass)
**Verdict:** **SIGN-WITH-FIXES** — M1–M5 and m1–m6 verified fixed by independent reading and
computation; **2 new MINOR findings (m7, m8)** in the decision procedure require one more
surgical pass before signing. The draft was not edited.

### Verification by target (read, not trusted)

**M1 — Worth-chasing bar.** [FACT — recomputed independently.] Exact two-sided McNemar at
α=0.05: (5,0)→p=0.0625; (6,0)→p=0.03125; (8,0)→p=0.007812 (13.33pp at N=60); (8,1)→p=0.039062
(11.67pp). The spec's table matches to all decimals. The bar is now **+12pp [ARBITRARY]** with
the derivation stated honestly: any significant gap on N∈[50,60] implies ≥6 net pure rescues
(≥10pp at N=60; ≥12pp at N=50), so a bar at or below +10pp would never bind independently of
the p-value — at +10pp, {margin<10pp}⊆{p≥0.05}, making the magnitude condition decoration.
+12pp is the lowest round bar strictly above the floor where the two conditions exclude
different outcomes ((6,0): 10.0pp, p=0.03125 → significant but below bar). Branch (d) is now
reachable: (6,0) on N=60 fires (d); (8,0) at 13.3pp fires (e); at the N_final=50 floor the
conditions coincide and (d) is unreachable there — stated in-protocol. The false "+8pp ≈ 5
net rescued items with McNemar p<0.05" sentence is gone, explicitly retracted as false.
Sensitivity bands re-centered at +12/+16/+20pp. The "lenient bar" note is honest: +12pp
halved is 6pp (below the detection floor), so +12 is lenient and the halving-honest ~+20pp
sits as the upper band, not the primary bar — a clean reversal of the draft's inconsistent
"survives halving" rationale, disclosed as such. No +8pp-bar remnants (grep-verified).

**M2 — Branch (c) split.** (c1)/(c2)/(c3) defined consistently in §1.2 and §8 (triggers,
licenses, and exclusions match across both). The probe-signal gate (§8 header) is evaluated
*on entering branch (c), before any (c1)/(c2) ruling* — stated verbatim, not implied.
Gate prongs: (ii) r_pb>0 one-sided p<0.05 when Y_x has nonzero variance; (iii) H_sel≥25%
[ARBITRARY] for the zero-rescue edge (within branch (c), zero-variance Y_x ⟹ all-zero, so
the parenthetical is correct in context). The deviation from the review's "(i)≥25%" example
is correctly reasoned and documented per Law #12 (§6 NOTE): under pure noise (i)≈86% —
**recomputed independently at 0.8635** under the binomial(5,0.5) noise model (P(B_agg
top-tied)=0.1365 over 17 i.i.d. 6-valued scores) — so (i) is high under both informative and
noisy probes and cannot gate; the gate rests on (ii) (transfer) and (iii) (decisiveness).
Noise-kill protection verified structurally: under a pure-noise probe, (ii) has only its
stated 5% false-pass rate and (iii)'s 25% floor sits far above the noise max-share
(independent MC: mean 0.121, p99 0.183 on N=60) → (c2) fires, EXP068 is NOT cancelled.
The gate genuinely blocks manufactured kills.

**M3 — Tie-break.** B_agg preference dropped; seeded-random draw over top-tied (seed 7005,
archived per instance; §10 seed list consistent). Direction-neutral in expectation — stated,
with the corrected rationale (the old "conservative" framing named as kill-ward). Winner's-
curse attenuation quantified, **not asserted**: E[best-of-17 noise probe score]≈0.88 vs true
0.50 and P(winner scores 1.0)≈0.42 — **both recomputed independently (0.8776, 0.4171)** under
the exact stated noise model. A-generous→A-attenuation rename consistent everywhere
(grep-verified: "generous"/"A-generous" appear only inside "was backwards" framings).

**M4 — License.** "H_loop is DEAD" fully replaced (grep-verified, zero remnants) with
justification-withdrawal in §1.1, §1.2 (c1)/(c3), and §8 (c1)/(c3). DOES NOT LICENSE gains
the adaptive-hypothesis exclusion and the re-motivation path (future loop on a different
candidate family = new pre-registration). A-pool license tightened with the angular scale
stated (§7: σ=0.1 in d=768 → E[cos]≈0.34, ~70° cone — recomputed: 1/√8.68≈0.3395 ✓;
2-step at cos≈0.12 ≈83° ✓); 2-step ring rejected as security theater with the adaptivity
argument, not merely asserted.

**M5 — Anti-cheat.** Runtime assertion support_ids∩test_ids=∅ present alongside probe∩test
(§3.2), violation aborts as protocol violation, both id lists archived (§10), leakage clause
§3.5(4) extended to support/test overlap. Closed.

**Minors m1–m6.** m1: EXP071 pre-claims removed — "next free number at pre-registration time"
in header note, §8 (c2), §9, §10, §12 (grep: EXP071 appears only in the vacating note). m2:
"never better" qualified to "cannot systematically beat … in expectation (a lucky single
realization may match it)". m3: margin tie-break dropped with the O5 rationale cited. m4:
gate ordering explicit in §9 — metadata gate → 5-instance pilot (wall-clock + probe-yield
smoke check on (i)/(iii), sanity signal not ruling) → full launch. m5: Law #12 deviation
note present (§3.3: probe-oracle vs sprint's test-label-readable sketch). m6: angular scale
in §3.1 with the computed E[cos].

### New findings (decision-procedure scan)

**m7 (MINOR, required) — outcome-space partition gap.** The C3-vs-C2 outcome {ΔM>0,
McNemar p≥0.05} — e.g., (b=5,c=0): +8.3pp, p=0.0625 — has **no branch**. (c1) requires
ΔM≤0; (d) requires p<0.05; (e) requires both. A positive-but-nonsignificant oracle result
falls through the tree, leaving the executor to improvise — the exact freedom a
pre-registration must foreclose (a motivated reader could call +8.3pp "a positive trend,
not a kill"). Required: extend (c1)'s trigger to "no statistically significant C3-vs-C2
gain (p≥0.05), probe-signal gate passed" (the (c1) license — "no label-informed selection
beats static here" — already covers nonsignificant positives; only the trigger's ΔM≤0
clause is too narrow), and conform (c2)'s "shows no gain as in (c1)" wording to the
extended trigger.

**m8 (MINOR, required) — (f) precedence unstated.** Branch (f) ("do not kill or justify on
selection grounds") can co-fire with (e) (C4≥C3 while C3 beats C2 by ≥12pp: the "selection
prize" is then a pool prize, and (e)'s license would be false) and with (c1) (C4≥C3≈C2:
the oracle methodology is uninformative per (f)'s own license, yet (c1) would kill).
Table order places (f) after (d)/(e), which under a top-to-bottom reading gives (e) the
wrong priority. Required: one pre-registered precedence sentence — (f) is evaluated before
the selection-grounded rulings (c1)/(c3)/(d)/(e), and a fired (f) suspends their
selection-prize/justification licenses (it does not suspend (c2)'s probe-informativeness
logic or (b)'s invalid-run discipline).

### Verdict rationale

SIGN-WITH-FIXES rather than SIGN because a pre-registered decision tree must partition the
outcome space and resolve branch conflicts without executor improvisation — m7 and m8 are
genuine holes, however small. They are also mechanical: m7 is a trigger-clause widening, m8
a precedence sentence; neither changes what gets executed, any threshold, or any license's
substance. A focused verification of the two sentences (not a full re-review) suffices
before signing. Everything the first review required is now verified fixed by independent
computation; the experiment's identity — a cheap verifier-first ceiling with honest
anti-cheat, a probe-gated kill, and N1 framing throughout — is intact.

*No draft files were edited. No primary artifacts touched. No results invented.*

---

**Reviewer Sign-Off:** Pending — m7/m8 applied and the two sentences verified.

---

## Final sign-off (focused verification) — 2026-09-23

**Role:** Adversarial Reviewer (Law #14, focused verification per the re-review's own recommendation)
**Verdict:** **SIGN** — the EXP070 pre-registration is hereby the **SIGNED pre-registration**.
`experiments/protocols/EXP070_ORACLE_CEILING_PREREG_SPEC.md` is execution-ready and strictly
confirmatory. Changed design = the next free number at pre-registration time.

### m7 — partition gap: CLOSED

- The (c1) trigger in the §8 decision-tree row reads "no statistically significant gain
  ($p \ge 0.05$), **and** the probe-signal gate passes". The §1.2 summary table carries the
  same trigger: "no statistically significant C3-vs-C2 gain ($p \ge 0.05$), probe-signal gate
  passed (§8)". Semantically identical — the §8 row header already scopes "C3 vs C2", so the
  qualifier is redundant there, and "(§8)" is the summary's pointer to the definition. Noted
  as trivial phrasing variance between summary and definition, not a defect.
- The old clause ("ΔM_oracle − ΔM_static ≤ 0 with McNemar p ≥ 0.05") is gone — grep-verified,
  zero remnants.
- §1.2 (c2) row conformed explicitly ("no statistically significant C3-vs-C2 gain as in (c1),
  probe-signal gate failed (§8)"); §8 (c2) row conforms via pointer ("C3 vs C2 shows no gain
  as in (c1), **but** the probe-signal gate fails").
- Falling-through cell traced: (b=5,c=0) → +8.3pp, p=0.0625 ≥ 0.05 → enters branch (c) →
  probe-signal gate evaluated first → passes → **(c1)**; fails → **(c2)**. The cell no longer
  falls through; no executor improvisation is possible.
- Partition exhaustiveness (C3-vs-C2 outcome space): p ≥ 0.05 → (c1)/(c2) via the gate;
  p < 0.05 ∧ ΔM > 0 ∧ margin ≥ +12pp → (e); p < 0.05 ∧ ΔM > 0 ∧ margin < +12pp → (d);
  p < 0.05 ∧ ΔM < 0 → (c3); p < 0.05 ∧ ΔM = 0 is impossible under McNemar (b≠c ⟹ ΔM≠0).
  (a)/(b) are orthogonal preconditions; (g) is a consistency check. No gap remains.

### m8 — precedence: STATED AND RESOLVED

- The precedence [DEFINITION] note exists at the §8 table header: "(f) is evaluated before
  the selection-grounded rulings (c1)/(c3)/(d)/(e); a fired (f) suspends their selection
  licenses (not (c2)'s probe logic, not (b)'s invalid-run discipline)".
- Cross-referenced from the (f) row ("see the branch-precedence note above").
- Co-firing (f)+(e) resolves to exactly one operative ruling: (f) is evaluated first, (e)'s
  selection license is suspended, and the operative ruling is (f)'s "Do not kill or justify
  on selection grounds". (f)+(c1)/(c3)/(d) resolve identically. (f)+(c2): the carve-out is
  explicit — (c2)'s probe logic stands, and its operative statements ("do not kill/justify
  on selection grounds; diagnose" + "ceiling unmeasured; EXP068 NOT cancelled; re-register")
  are mutually consistent, both directing to diagnosis/re-registration. No contradiction.

### Surgical-diff check

The spec file is untracked in git (no committed baseline to diff against); the check was
performed by full read plus targeted grep. Every section matches the re-review's verified
description except the m7/m8-targeted sentences: §1.2 (c1)/(c2) rows, §8 (c1)/(c2) rows, the
new §8 precedence note, and the (f) row cross-reference. The M1–M5 and m1–m6 fixes were
spot-verified intact (+12pp bar, probe-signal gate, direction-neutral tie-break,
justification-withdrawal license, support∩test assertion). Nothing beyond m7/m8 changed.

*No draft files were edited by this reviewer. No primary artifacts touched. No results invented.*

**Reviewer Sign-Off:** **SIGNED** — Adversarial Reviewer, 2026-09-23. EXP070 may proceed to execution on free-tier compute per the pre-registered protocol.
