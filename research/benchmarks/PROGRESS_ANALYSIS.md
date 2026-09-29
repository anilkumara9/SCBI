# Progress Analysis — where SCBI stands vs the frontier (standing; updated 2026-09-29)

*Standing Benchmark Analyst. One page. No softening. Supersedes the
2026-09-23 snapshot (`PROGRESS_ANALYSIS_2026-09-23.md`, preserved as
history). Full evidence: `FRONTIER_SCOREBOARD.md` §3.*

**The frontier, summarized.** In 2025–2026 the field shipped working
inference-time computation on frozen models: ∇-Reasoner (71.2→80.4%
MATH-500, 10–40% fewer calls), LatentMAS (up to +14.6% accuracy, 70–84%
token reduction), Meta-Reasoner (+9–12% accuracy at −28–35% inference time,
same budget), DEER (−19–80% chain-of-thought at +0.3–5.0% accuracy),
Self-Refine (~+20% absolute across 7 tasks), self-consistency (+17.9pp on
GSM8K), LLM-Monkeys (15.9%→56% SWE-bench Lite at 250 samples),
Activation-LQR (closed-loop LQR steering with tracking-error bounds),
NoisyCoconut (<15% error via selective abstention). The bar for
"inference-time compute does something" is high, published, and rising.

**SCBI, summarized.** Zero capability results. The EXP094–103 wave is now
complete and reads as the boundary map: per-item static L11 geometry
refuted by pure inertness (EXP094: 0 flips across 120 injection arms);
the α grid inert at every ratio (EXP095); movement that exists but is not
directionally attributable (EXP096/097/099 — fragility);
the composition premise not supported (EXP098 — random joint moved 12
vs 7 joint); and the {mean,max}×{L11,L20} externally-computed
attention-gate family closed 4/4 (EXP100 mean-at-L11: 0/60 coverage,
untestable; EXP101 max-at-L11: 16/60, 1 flip right→wrong, Refuted; EXP102
mean-at-L20: 1/60, untestable; EXP103 max-at-L20: 55/60, 3 flips p=1.0,
Refuted). The S6-5 pooled audit fixes the program ceiling at 5/381
directional flips (one-sided 95% UB 2.74%). The whole L11-rescue program
was then stood down (LOG-4463/4464): no self-computed-gate design clears
the worth-it gate — the rational update is "the direction is the problem,
not the gate." Ten experiments, ~2,000 CPU passes, $0. The only positive
numbers in the program's history were the label-assisted bridge rescues,
demoted to rescue controls (LOG-197/204); its best autonomous number was
+4pp, non-significant (EXP056). **Update 2026-09-29: EXP111 is the day's
first genuine positive signal** — a trained L2-logistic head on the
EXP107 template-decorrelated bench scored **24/30 = 0.8000, one-sided
p=0.00072, G=0.0000** → CONTINUE (independent verdict review LOG-4569
QUALIFIED; the GPU head-training proposal voided by EXP107 is re-licensed
under decorrelated-bench discipline, still founder-hardware-gated).
This is a **boundary-science decodability entry, not a capability entry**:
one layer-20 correlation on one n=30 bench; one n=30 bench does not move
the capability scoreboard. The program's first output-side result to
survive adversarial testing — and its honesty test passed alongside it:
the same kill-test discipline that executed EXP106.

**The gap.** Not a margin — an absence. On accuracy-at-matched-compute and
on compute-saved, SCBI has no entry while the frontier has six systems
plus the 2026 occupants (SVF, A-LQR, LTPO, LatentMAS). Our lead is
boundary science: the static + per-item + externally-gated rescue
program — every tested rescue dead, untestable, or uninterpretable — is
now a *map*, not a single null. That is real and publishable as a
boundary result (the gap analysis flags it as the largest no-new-compute
evidence delta for v84 — current release candidate, superseding v83 per
LOG-4519; v84 = v83 + converging-evidence related work + O1/O2 polish).
It is not a capability and does not compete with
any frontier row. The one axis where the frontier is also at zero —
**label-free autonomous steering** — remains the only honest race.
**Update 2026-09-29:** one positive output-side correlation survived
adversarial testing (EXP111: 24/30, G=0.0000 on the decorrelated bench) —
a decodability entry, not a steering entry, so the capability column stays
at zero and the honest headline for autonomous steering is unchanged.
**Update 2026-09-29:** EXP112 (H6/HDI-LR) **HELD** — the honesty
instrument rebuilt without generation: fidelity between the frozen
backbone's first-token logit-readout self-report and the registered
cosine-argmax decision statistic = **41/60 = 0.6833** (P(X≥41|60,0.5) =
0.0031 — real above chance, below the decisive bar), inside the
registered 34–41/60 HELD band (independent exact-artifact verdict review
LOG-4576 — BIND, no caveat). The channel is genuine: Law #14-grade
degeneracy guards (G1 mean mass 0.301075 ≥ 0.01, G2 readout balance
27/33) passed before any metric was read, all three archive hashes and
the LOG-331 backbone pin (before AND after the 180 fresh forwards)
verified, Δθ=0. HELD licenses nothing, retires nothing, no re-runs —
a weak honesty-decoding correlation at one read site, not consciousness,
generality, or capability. **Update 2026-09-29:** EXP113 (H7/EVALID)
**CONTINUE** — the bounded apparatus question that gates honest H1/H4
revival: 5 pinned elicitation protocols × 2 task shapes (T1 single-token
answer = H1 self-report shape; T2 numbered outlines = H4 planner shape)
× 60 items = 600 greedy generations on frozen base Pythia-410m, every
output parsed by the registered mechanical scripts (deterministic
re-parse byte-identical; 0 exceptions; no RUN-INVALID fired; backbone
LOG-331 pin before AND after, Δθ=0). T1 — P1=0/60, P2=60/60, P3=0/60,
P4=58/60, P5=60/60; T2 — P1=24/60, P2=60/60, P3=0/60, P4=0/60, P5=60/60;
clearance ≥48/60 → T1-CLEAR={P2,P4,P5}, T2-CLEAR={P2,P5}, both
non-empty → **CONTINUE**. Few-shot (P2) and priming (P5) are the only
protocols clearing both shapes — H1/H4 revival is licensable as NEW
hypotheses with the named clearing protocols (each with its own
elicitation-failure gate); H1/H4 themselves are NOT revived
(independent exact-artifact verdict review LOG-4585 — BIND, no caveat).
Methodological/apparatus entry: parseable output ≠ reasoning, honesty,
or capability — the generation axis is open for this backbone under
pinned protocols, a real methodological gain, not a capability signal.
**Update 2026-09-29:** EXP114 (H8/POE) **KILL** — positional-order
ensembling, the round-2 wave's first clean negative: K=5 ensemble of
frozen-backbone position logits over randomized presentation orders vs
the canonical single-order baseline on the EXP107
template-decorrelated bench (360/360 forward passes, zero generation;
order patterns independently replicated from random.Random(20260929),
0/60 mismatches; all three archive hashes and the LOG-331 backbone pin
matched before AND after, Δθ=0): **acc_ensemble 38/60 = 0.6333 vs
acc_baseline 41/60 = 0.6833; net (b−c) = −3; one-sided exact McNemar
p = 0.9375** — the ensemble scored 5pp BELOW the baseline, firing the
registered net ≤ 0 → KILL branch with no post-hoc re-interpretation.
Fences honored: retires only the positional-order-ensembling axis for
this task class — test-time scaling in general and the adaptive-loop
program are explicitly NOT retired; the below-baseline reading is a
labeled [OBSERVATION], no softening (independent exact-artifact verdict
review LOG-4592 — BIND, no caveat).
**The day's tally: one CONTINUE (EXP111), one HELD (EXP112), one
apparatus CONTINUE (EXP113), two KILLs (EXP107, EXP114), two
RUN-INVALIDs (EXP108, EXP109), one precision certification (EXP110).** The
capability column stays at zero.
**Update 2026-09-29:** EXP115 (H9/HDI-GEN) and EXP116 (H10/HDI-PRIM) — both
**RUN-INVALID** — the two EXP113-licensed honesty-instrument revival
hypotheses died at the apparatus layer on the same bench via two
*different* failures, each independently confirmed from the raw generations
(independent exact-artifact verdict reviews LOG-4599/4603 — both BIND, no
caveat): few-shot (P2) elicitation collapsed into recitation
(n_unparseable = **38/60** ≥ 7; all 60 generations contain `Premise:`, the
last exemplar block regurgitated verbatim), while priming (P5) elicitation —
with zero exemplar blocks, structurally immune to recitation — collapsed
into tail echo (n_unparseable = **37/60** ≥ 7; 27 of the 37 unparseable
echo the unfinished priming sentence verbatim; 0/60 contain `Premise:`).
Both failures were inside the pre-regs' disclosed risk envelopes; the
gates fired before any metric was read (fidelity null, not wrong). These
are apparatus failures, not hypothesis failures — but the consequence is
final for this line: **the generation-level honesty instrument has no
EXP113-cleared protocol left on the entity-name shape** (P2 dead, EXP115;
P5 dead, EXP116). H6's logit-level HELD (41/60) stands alone as the only
honesty signal. The reports KILL, HELD, and CONTINUE nothing.
**The day's tally: one CONTINUE (EXP111), one HELD (EXP112), one apparatus
CONTINUE (EXP113), two KILLs (EXP107, EXP114), four RUN-INVALIDs (EXP108,
EXP109, EXP115, EXP116), one precision certification (EXP110).** The
capability column stays at zero.

**What closes it.** The §D2 six-condition bar: per-instance construction,
transfer-validated evaluator, matched-compute wins over ∇-Reasoner /
Activation-LQR / Meta-Reasoner / DEER / LatentMAS plus the pinned M15
comparators, conditional-computation proof, specificity gap — at powered
N≈100+. The live lanes toward that bar: the GPU queue (K2 → EXP083 →
EXP084 → EXP086 Stage B → EXP088 → EXP087, founder's Kaggle), and a new
direction family earning its own license (the S6 stand-down pre-registered
the re-opening conditions). The honest base rate, from the synthesis's
own power analysis: at current N the program is a falsification-and-
boundary program. The scoreboard will record a beaten frontier the day the
six conditions are met — and will say "not yet" every day until then.

---

## The I2′ line (opened and CLOSED 2026-09-28) — selection-failure instrumentation

**Terminal state.** I2′ answered EXP085's death-debt question — are
selection failures measurable and repairable? — with a complete
falsification-terminal arc in one day. Chain: S4-8 pre-registration
SIGNED (LOG-4480) → EXP104 Tier-0 executed (LOG-4481/4482) → HOLD →
Inconclusive (0.1833 < 0.25 bench sanity; premise bars met, battery NOT
run) → bench autopsy (LOG-4483): the HOLD was a position-A prior —
30/60 top-1 at position 0, p=2.02e-12 — format-driven, an instrument
confound not a premise kill → S4-8′ cloze recalibration SIGNED
(LOG-4488) → **EXP105 Tier-0 PASSED (LOG-4489)**: baseline 32/60 =
0.5333 inside [0.25, 0.75] (NOT line-closed), median correct-rank on
failed items 4.0 ≤ 5, n_pop 21 ≥ 12, tie-guard 0.0 — the cloze format
rescued measurability (0.1833 → 0.5333) and confirmed the A-prior
diagnosis: the prior was a readout-format artifact, not a knowledge
absence → **EXP105 battery Refuted at step 9 (LOG-4491)**: ΔM_T =
+0.2381 (5/21 rescues) vs ΔM_R = 0.0000 (0/21, perfectly flat) — clean
direction — but the primary T-vs-R McNemar-exact p=0.0625 ≥ 0.05,
missed CONTINUE by exactly one flip; foil–top-1 overlap O = 0.571 > 0.5
→ F arm non-diagnostic, exactly as the pre-registered N1 amendment's
O ≤ 0.5 gate anticipated (validated design lesson). Pre-registered stop
rules closed the line: no re-run, no larger population, no third
readout.

**The instrument lesson, banked.** The MC bench in lettered format is not
a knowledge instrument on this base LM (position-A prior + shuffle-seed
sensitivity); cloze scoring restores it. This reconciles with EXP092:
the supervised 1-NN (33.33% vs 5%, p=0.000999) measures information
*presence*; EXP104 measured the untuned head's *routability*. Presence ≠
routability — another dissociation, not a contradiction.

**The verdict's honest reading.** Refuted is not evidence that masking
is generic — it is evidence the licensed test could not certify
specificity. The observed rescue direction was clean (random masking
rescued 0/21); the binding significance bar was missed by one flip at
n_pop=21. This is a falsification-terminal entry on the boundary map,
not a capability entry and not a premise kill.

**What changed, what didn't.** The honest headline is unchanged: zero
positive signals for autonomous steering; the label-free race stays tied
at zero. What changed is that the program's first selection-failure line
ran its entire licensed arc — instrument built, confound diagnosed and
removed, premise certified-not-specific by its own pre-registered bar —
in one day, $0, Δθ=0, with the terminal condition written *before* the
run, not after.
