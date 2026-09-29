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

**Update 2026-09-29:** EXP117 (H11/PTTSC-GEN) — **RUN-INVALID** — the
EXP113-licensed planner/executor revival hypothesis (a NEW apparatus on the
T2 numbered-outline shape, not a re-run of EXP109) never reached the
planning question: Phase 0b's decision-channel mini-gate fired with **0/10
parseable** (the model enumerates entities as a list instead of naming one),
the 4th consecutive entity-name-generation-slot failure on this shape
(EXP109 80/80 sampled; EXP115 38/60 recitation; EXP116 37/60 tail echo;
EXP117 0/10 enumeration). Phase 0a's literal recitation gate did NOT fire
(0/10) while the content-level diagnostic scored 10/10 — the independent
exact-artifact verdict review (LOG-4610 — BIND, no caveat) adjudicated a
**REAL protocol defect**: the §3.7 literal recitation definition is
structurally inert for content recitation (marker-stripped extraction vs
marker-prefixed exemplar lines) — but it did NOT change the verdict (the
gate was applied as written; Phase 0b fired independently; the RUN-INVALID
is overdetermined), and it is recorded as a binding apparatus-definition
lesson: **no future protocol may reuse the §3.7 definition.** Planner
prompts byte-verified 0/60 mismatches against the signed `exp113_run.py`
T2-P2 construction; backbone LOG-331 pin matched pre-run, Δθ=0.
**Apparatus failure, not a hypothesis failure — no verdict smuggled; the
generation channel for entity-name answers is dead on base Pythia-410m
across four apparatuses.** **The day's tally: one CONTINUE (EXP111), one
HELD (EXP112), one apparatus CONTINUE (EXP113), two KILLs (EXP107,
EXP114), five RUN-INVALIDs (EXP108, EXP109, EXP115, EXP116, EXP117), one
precision certification (EXP110).** The capability column stays at zero.

**Update 2026-09-29:** EXP118 (H13/HDI-LOC) — **RUN-INVALID** — the layer-locality question (where does EXP112's 41/60 HELD fidelity live, via the zero-training logit lens across 18 layer sites) never reached its metric: the pre-registered run-validity rule fired on the early window — **0/9 non-degenerate sites** (required ≥5) — the logit lens cannot speak at early layers on this bench (entity-name tokens acquire unembedding mass only in the final ~5 layers). Per Law #9 no per-site fidelity and no contrast C was read — no verdict smuggled; EXP112's HELD stands unchanged. The consistency pin PASSED (lens@L24 byte-identical 60/60 to EXP112's archived column, 41/60 exactly) and arbitrated the double-normalization fix on the executor's first attempt (5/60 argmax flips HALTed) — a genuine apparatus-integrity win, not a model finding. The independent exact-artifact verdict review (LOG-4620 — QUALIFY) bound one caveat: the report's §10/§11 falsely claimed `exp118_worksheet.json` was written — corrected by **erratum (LOG-4621)**; verdict untouched. **Apparatus failure, not a hypothesis failure.** **The day's tally: one CONTINUE (EXP111), one HELD (EXP112), one apparatus CONTINUE (EXP113), two KILLs (EXP107, EXP114), six RUN-INVALIDs (EXP108, EXP109, EXP115, EXP116, EXP117, EXP118), one precision certification (EXP110).** The capability column stays at zero.

**Update 2026-09-29:** EXP119 (H14/PTTSC-LOGIT) — **RUN-INVALID** — the H11 planning question re-asked on the proven zero-generation logit channel died at the pre-registered Phase-0b tokenization-identity pin: plan tail `[444, 37741, 27]` vs baseline `[32, 37741, 27]` on the first probe item — the plan block's final outline ends in a word, not `?`, so the final token run differs from the baseline's fixed `? Answer:` tail. The independent exact-artifact verdict review (LOG-4628 — BIND, no caveat) replicated the mechanism tokenizer-only (no model contact) and adjudicated it **structural, not item-specific**: any plan block whose final outline doesn't end in `?` breaks the pinned [-3:] identity — the pre-reg's §0(6) breaking point ("tokenization effects break the channel") realized exactly as anticipated. Zero Phase-0b forwards ran; per Law #9 no metric was read and tuple[0] was never touched (Law #7) — no verdict smuggled; the full run was never licensed. **H11's planning hypothesis is now untested on both EXP107 decision channels** (generation dead per EXP117, plan-prefix logit slot dead per EXP119). Small positive, honestly framed: Phase 0a scored **10/10 planner-valid** (gate did not fire) — T2-P2 transfers to the EXP107 bench as a plan elicitor (apparatus observation, not a capability claim). **Binding record-keeping lesson:** the execution lane did not persist raw Phase-0a generation texts (counts/diagnostics only — verdict intact, record-keeping insufficient); future execution lanes must persist raw generation records before any verdict is written. **Apparatus failure, not a hypothesis failure.** **The day's tally: one CONTINUE (EXP111), one HELD (EXP112), one apparatus CONTINUE (EXP113), two KILLs (EXP107, EXP114), seven RUN-INVALIDs (EXP108, EXP109, EXP115, EXP116, EXP117, EXP118, EXP119), one precision certification (EXP110).** The capability column stays at zero. **Update 2026-09-29:** EXP120 (H15/LFH-GEN2) — **QUALIFIED CONTINUE** —
the generality test EXP111's output-side positive needed: the trained
L2-logistic head replicates on a *second, independently constructed*
template-decorrelated bench (60 fresh items, four 15-item cells, new verb
families "surpasses"/"is below" replacing bench 1's "outranks"/"is lower
than", new river+tree entity sets; all construction gates passed —
G-C1 pure-template detector 30/60 ≤ 36/60, G-C2 |Pearson| = 0.0475 ≤ 0.10
with no bench-1 labels or embeddings entering the analysis (Law #13,
verified in the implementation), G-C3 decomposition byte-exact; LOG-331
pin before AND after all 60 fresh CPU extractions, Δθ=0): **test 25/30 =
0.8333** (per-cell 4/8, 7/7, 7/7, 7/8), **G = −0.2000 < 0.30** → the
registered ≥20/30 with G<0.30 CONTINUE branch fires (LOG-4633 execution).
The independent exact-artifact verdict review (LOG-4634 — QUALIFY)
recomputed everything from scratch with numpy — 25/30, per-cell, G, all
match — and bound one documentation-precision caveat: the report's
hand-written "≈0.0009" p for 25/30 is wrong — exact one-sided is
**0.00016** — an error in the conservative direction, corrected by
**erratum (LOG-4635)**; the verdict never depended on it. The cross-bench
statistical-comparison fence was honored (each bench's numbers stated
descriptively, no test between bench 1 and bench 2), and EXP111's
bench-1 observation was restated, never re-adjudicated (Law #8).
**Honest placement:** the output-side readout room's positive is now a
two-bench observation — a trained head extracting the subject-position
cue at layer 20 on two independently constructed benches — but it remains
**boundary-science decodability, not capability**: correlation, not
steering; no decision flips moved. The defect class banked: **report
authors hand-writing p-values instead of executor-computed values** —
future pre-registrations must pin p-values as executor-computed. **The
day's tally: two CONTINUEs (EXP111, EXP120 — both bound), one HELD
(EXP112, bound), one apparatus CONTINUE (EXP113, bound), two KILLs
(EXP107, EXP114 — both bound), seven RUN-INVALIDs (EXP108, EXP109,
EXP115, EXP116, EXP117, EXP118, EXP119 — all bound), one precision
certification (EXP110, bound).** The capability column stays at zero.
H6's logit-level HELD (41/60) stands alone as the only honesty signal.
**Update 2026-09-29:** EXP121 (H19/PTTSC-SUFFIX) — **RUN-INVALID** — the planning question, re-asked on the logit channel through the tail-preserving composition (plan text between the premise and the fixed ` Question: Who is higher in rank? Answer:` tail — placement A), cleared every apparatus gate that killed EXP117/EXP119 (tokenizer [-3:] identity 60/60, Phase 0a planner-valid 10/10, Phase-0b identity + G1 10/10; the EXP119 structural break does not recur under placement A) but died one layer deeper, at the readout-mass degeneracy gate: on 22/60 items the plan-inserted arm drove the summed post-softmax mass on the two pinned entity tokens to 0.000142–0.008571 (< 0.01 — the distribution concentrates elsewhere at the final position) while the baseline arm never dropped below 0.068 on the same items → **n_valid = 38/60 < 48 → RUN-INVALID (elicitation-failure gate)** (independent exact-artifact verdict review LOG-4645 — QUALIFY: verdict stands on the exact artifacts, one documentation caveat — the report's "second independent full run reproduced n_valid = 38" is unverifiable from retained artifacts, corrected by **erratum (LOG-4646)**; the verified claim is n_valid=38/60 recomputed independently from final-run artifacts, deterministic re-read ×2 byte-identical). Invariant under the stricter sum ≥ 0.02 reading (30 < 48); baseline reproduction 60/60 vs EXP112's archived readout; baseline variation distinct=2/minority=27 (gate passed); per Law #9 no McNemar table was read — no verdict smuggled. **H11's planning hypothesis is now untested across three distinct apparatus failure modes** (EXP117 generation, EXP119 tokenization identity, EXP121 plan-arm G1 collapse) — zero decision data. The one licensed upside, honestly fenced: placement A is a candidate adaptive-loop component for the plan-text pipeline — the token-asymmetry confound stands disclosed, not removed, so no planning-vs-compute attribution is licensed. **Apparatus failure, not a hypothesis failure.** **The day's tally: two CONTINUEs (EXP111, EXP120 — both bound), one HELD (EXP112, bound), one apparatus CONTINUE (EXP113, bound), two KILLs (EXP107, EXP114 — both bound), eight RUN-INVALIDs (EXP108, EXP109, EXP115, EXP116, EXP117, EXP118, EXP119, EXP121 — all bound), one precision certification (EXP110, bound).** The capability column stays at zero.

**Update 2026-09-29:** EXP122 (H16/POSITION-CUE) — **CONTINUE** — the
position-cue dissection EXP111/EXP120's trained-head signal needed: does
the head read the target's domain-set identity, or merely its sentence
position? The pinned H5 discipline ran verbatim on a *third, independently
constructed* bench (bench 3: 60 items, four 15-item cells, fresh
animal/fruit entity sets disjoint from benches 1/2, new verb families
"ranks above/below" and "dominates/is dominated by") with the position
scramble built into the construction — the target's final sentence
position balanced **15/15 within each label class** (corr = 0.0), so
position carries no label information; all construction gates passed
(G-C1 32/60 ≤ 36/60; position-scramble gate 30/60 ≤ 36/60; G-C2
|Pearson| = 0.0322 ≤ 0.10 — no bench-1 labels or embeddings entered the
analysis (Law #13); G-C3 QUESTION_SUFFIX byte-exact; LOG-331 pin before
AND after all 60 fresh CPU extractions, Δθ=0): **test 27/30 = 0.9000**
(per-cell 6/8, 7/7, 7/7, 7/8; acc(F)=0.8667, acc(T)=0.9333),
**G = −0.0667 < 0.30** → the registered CONTINUE branch fires
(LOG-4653 execution). The independent exact-artifact verdict review
(LOG-4654 — BIND, no caveat) recomputed the head test from scratch —
27/30, per-cell, G, all match — and independently verified the scramble
from the canonical bench JSON (0/60 label mismatches, corr 0.0). Exact
one-sided p = **4.215e-06**, executor-computed (defect class (a) honored).
**Honest placement:** the output-side readout room's positive is now a
three-bench observation of the identity-readout signal *with position
decorrelated* — the subject-position-detector alternative is excluded —
but it remains **boundary-science decodability, not capability**:
correlation, not steering; no decision flips moved; the cross-bench
statistical-comparison fence was honored (each bench's numbers stated
descriptively, no test between benches); EXP111's and EXP120's
observations restated, never re-adjudicated (Law #8); fences: no
capability, no generality beyond the three benches/layer/model, no
re-licensing of H1/H4 or closed families, novelty N1. H11's planning
hypothesis remains untested across the three apparatus failure modes
(EXP117 generation, EXP119 tokenization identity, EXP121 plan-arm G1
collapse) — zero decision data. **The day's tally: three CONTINUEs
(EXP111 — bound; EXP120 — bound, qualified; EXP122 — bound), one HELD
(EXP112, bound), one apparatus CONTINUE (EXP113, bound), two KILLs
(EXP107, EXP114 — both bound), eight RUN-INVALIDs (EXP108, EXP109,
EXP115, EXP116, EXP117, EXP118, EXP119, EXP121 — all bound), one
precision certification (EXP110, bound).** The capability column stays at
zero.

**Update 2026-09-29:** EXP123 (H20/P4APPARATUS) — **RUN-INVALID,
TERMINAL** — the last EXP113-cleared generation protocol on the
entity-name shape died completely: P4 repetition-penalty decoding
(`repetition_penalty=1.2`, `no_repeat_ngram_size=3`, greedy,
`max_new_tokens=4`) on the verbatim EXP107 60-item bench yielded
**n_parseable = 0/60, n_unparseable = 60/60, n_exceptions = 0**
(independently recomputed from the raw artifacts, zero mismatches;
deterministic rerun + re-parse ×2 byte-identical; raw records persisted
and hash-pinned before the verdict; LOG-331 pin before AND after, Δθ=0).
The generations are real, non-degenerate model outputs (0/60 empty) — 18
distinct continuation attractors, none naming either candidate — a genuine
signal, not a decode artifact: the pre-reg's breaking mechanism realized
exactly (the repetition penalty down-weights tokens already present in the
input context, *including the entity-name tokens in the premise*, biasing
against emitting the entity name — on this shape P4 is an
anti-elicitation protocol, compounding EXP117's continuation attractors
and EXP113's own T2 datum of P4=0/60 on outlines). This was the
**expected** outcome (pre-reg predicted P(n_unparseable ≥ 7) ≈ 1): a
finding, not a failure. **Terminal reading, licensed:** the entity-name
generation channel is dead on **all** EXP113-cleared protocols — P2 died
on this shape (EXP115), P5 died on tail echo (EXP116), P4 dies here —
the honesty-instrument line closes **permanently on the entity-name
shape** (no protocol rescue, no larger-n rescue, no parameter tweak
licensed); H1/H4's T1/T2 clearances are untouched; EXP112's bench-2 logit
line is not rescued (a different instrument); the label-free race stays
tied at zero. Parseability ≠ correctness (registered): 0/60 is a *format*
measurement; the decision-silent correctness diagnostic is vacuous (0 of
0). Apparatus closure, not a hypothesis kill (independent exact-artifact
verdict review LOG-4662 — BIND, no caveat). **The day's tally: three
CONTINUEs (EXP111 — bound; EXP120 — bound, qualified; EXP122 — bound),
one HELD (EXP112, bound), one apparatus CONTINUE (EXP113, bound), two
KILLs (EXP107, EXP114 — both bound), nine RUN-INVALIDs (EXP108, EXP109,
EXP115, EXP116, EXP117, EXP118, EXP119, EXP121, EXP123 — all bound), one
precision certification (EXP110, bound).** The capability column stays at
zero.

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
