# Progress Analysis — where SCBI stands vs the frontier (standing; updated 2026-10-09)

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

**SCBI, summarized.** One capability result (EXP148, 2026-10-06 — see the
update block below). The EXP094–103 wave is now
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
on compute-saved against the frontier's six systems plus the 2026 occupants
(SVF, A-LQR, LTPO, LatentMAS), SCBI holds exactly one entry (EXP148 —
discipline beats budget-matched CoT at matched compute, not the best
baseline) and no frontier-beating claim: the §D2 bar (powered N≈100+,
transfer-validated, matched-compute wins over the pinned comparators)
is unmet. Our lead is
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

**Update 2026-09-29:** EXP124 (H21/PLAN-INSTRUMENT) —
**RUN-INVALID (apparatus-void)** — the plan-as-instrument selection of H11's
planning question: per item, a T2-P2 plan is elicited and the pinned §3.4
choice rule (leftmost-longest entity mention in the final outline in
position order) picks variant A vs C. Every Phase-0 gate passed
(tokenizer-only [-3:] **120/120** before model contact; choice-validity
**10/10**; variant discriminability **4/10**, M_A=0.38102, M_C=0.46331;
planner prompts byte-identical **0/60** vs the EXP113 T2-P2 reference) —
then the full run collapsed: **A-FIRST=48, C-FIRST=7, choice-invalid=5**
(independently reimplemented with **60/60 per-item agreement** and
outline-count agreement 60/60, zero field mismatches) → **C-FIRST=7 < 12
→ the registered choice-information gate fired** (decision-inert control
→ RUN-INVALID; independent exact-artifact verdict review LOG-4671 —
BIND, no caveat). The descriptive failure mode, independently
spot-verified: 60/60 full-run generation texts carry a hallucinated
`Premise:` line with entities outside the bench vocabulary (38 raw / 34
distinct collapsed), and the choice rule reads the leftmost entity match
inside the regurgitation — the outline texts contain no entity names, so
every extracted "choice" is a function of model regurgitation, not plan
content; the instrument was never a treatment. Per Law #9 no McNemar
table, no b/c/d/p — no metric was read; the lane halted before the 120
variant forwards; LOG-331 pre-contact pin matched, Δθ=0. The contrast
with the Phase-0 passes is the structural fact: the planner passes the
probe gates but the full-run choice collapses to a decision-inert
control — a boundary finding on choice informativeness, and the source
of the new binding lesson (defect class 8): a choice-extraction rule on
the final outline in position order must assert the final outline is
plan content, not regurgitation. **H11's planning hypothesis survives its
fourth RUN-INVALID** (EXP117, 119, 121, 124) — untested, not killed;
H21's instrument-selection channel is UNTESTED, not retired (a KILL
would have retired it); no further H11 composition is licensed without
a genuinely new instrument class. **The day's tally: three CONTINUEs
(EXP111 — bound; EXP120 — bound, qualified; EXP122 — bound), one HELD
(EXP112, bound), one apparatus CONTINUE (EXP113, bound), two KILLs
(EXP107, EXP114 — both bound), ten RUN-INVALIDs (EXP108, EXP109, EXP115,
EXP116, EXP117, EXP118, EXP119, EXP121, EXP123, EXP124 — all bound), one
precision certification (EXP110, bound).** The capability column stays at
zero.

**Update 2026-09-29:** EXP125 (H22/HONESTY-GEN4) —
**KILL** — the honesty-generality hypothesis is dead at logit level. On the
independently constructed bench 4 (60 items, four balanced 15-item cells;
body-part + weather entities, 21/21 single-token under the real Pythia-410m
tokenizer; new templates, disjoint from benches 1/2/3; breaking-point
certificate LOG-4679 PASSED before execution — single-token assertion,
[-3:] identity 60/60, G-C1 30/60, G-C2 |Pearson|=0.0198, G-C3 byte-exact,
Law-#7 label pin, no item screening of any kind), EXP112's H6 honesty
apparatus carried verbatim → **fidelity 28/60 = 0.4667 → the registered
≤33/60 KILL band** (LOG-4680 execution; independent exact-artifact verdict
review LOG-4681 — BIND, no caveat: fidelity independently re-derived
**28/60** from the raw per-item records, cosine-argmax agreement 60/60, all
six executor-computed p-values re-verified to printed precision, observed
one-sided P(X≥28|60,0.5)=0.7405; systematic-misreporting diagnostic
correctly NOT triggered at 28 > 23; all guards passed — G4 spread
0.138125, G1 M=0.232343, G2 minority=21, single-token 120/120 —
LOG-331 pin before AND after, Δθ=0). This is a **licensed guard-passed
null, not an apparatus failure**: the channel spoke and said nothing. Per
§4 of the protocol a KILL is never followed by a larger-n re-test, a
different layer, a different carrier, or a third bench (barred as an
unlicensed gate tweak). **EXP112's bench-1 41/60 HELD stands, reclassified
bench-specific (Law #11 two-layer tagging)** — the label-free honesty
readout is a **one-bench phenomenon** (41/60 bench 1, 28/60 bench 4), not a
general instrument property. The label-free line now reads: EXP111/EXP120/
EXP122 decodability CONTINUEs (readout, not steering), EXP112 bench-1-only
honesty HELD. **The day's tally: three CONTINUEs (EXP111 — bound; EXP120 —
bound, qualified; EXP122 — bound), one HELD (EXP112, bound,
bench-1-specific), one apparatus CONTINUE (EXP113, bound), three KILLs
(EXP107, EXP114, EXP125 — all bound), ten RUN-INVALIDs (EXP108, EXP109,
EXP115, EXP116, EXP117, EXP118, EXP119, EXP121, EXP123, EXP124 — all bound),
one precision certification (EXP110, bound).** The capability column stays
at zero — the strongest licensed label-free signal the program could
produce on $0 CPU did not replicate.

**Update 2026-09-29:** EXP126 (H23/WITHIN-DOMAIN) — **KILL** — the identity-readout *interpretation* of the trained head is dead. On the independently constructed bench 5 (60 items, all animals — 14 single-token animal entities; S1={Cat,Dog,Bear,Wolf,Fox} vs S2={Lion,Tiger,Horse,Cow,Pig}, neutral decoys {Rat,Bat,Bird,Fish}; every decoy drawn from the same domain as the target so domain-set detection is informationally dead by construction; disjoint from benches 1–4; breaking-point certificate LOG-4687 PASSED before execution — 14/14 single-token, single-domain audit 0/60 out-of-domain, G-C1 28/60, G-C2 |Pearson|=0.0018, G-C3 byte-exact, position-scramble 30/60, Law-#7 label pin, no item screening), the pinned H5 head (recipe byte-identical, Law #14 SIGN with zero fixes LOG-4686) scored **test 18/30 = 0.6000, G = −0.4000 → the registered ≤18/30 KILL band** (LOG-4688 execution; independent exact-artifact verdict review LOG-4689 — BIND-WITH-CAVEAT: accuracy independently re-derived 18/30, G=−0.4000 with the correct F/T convention, observed exact one-sided P(X≥18|30,0.5)=0.1807973040 — at chance; all four artifact hashes match, LOG-331 pin before AND after, Δθ=0; caveat: `exp126_worksheet.json` truncated at 910 bytes — a bookkeeping defect, not a verdict defect; new binding defect class recorded: a hash-pinned worksheet can still be truncated — future lanes must parse/validate the manifest before treating it as readable). Lane-defect disclosure (complete): first attempt loaded `AutoModel` instead of `AutoModelForCausalLM` → LOG-331 pin mismatch → halted at RUN-INVALID before any extraction; corrected loader, full tree re-ran from the top; both attempts on the append-only console log. The heads were **domain-set detectors, not entity readers**; EXP111/EXP120/EXP122 observations stand (Law #8) and their three-bench CONTINUE is **reclassified as a domain-set-detector correlation** (Law #11 two-layer tagging); any entity-level use of the signal is retired; the within-domain dissection line closes with it. The label-free line now reads: EXP112 bench-1-only honesty HELD — the sole remaining non-decodability label-free signal, and it is bench-specific. **The day's tally: three CONTINUEs (EXP111 — bound, reclassified domain-set-detector correlation; EXP120 — bound, qualified, reclassified; EXP122 — bound, reclassified), one HELD (EXP112, bound, bench-1-specific), one apparatus CONTINUE (EXP113, bound), four KILLs (EXP107, EXP114, EXP125, EXP126 — all bound), ten RUN-INVALIDs (EXP108, EXP109, EXP115, EXP116, EXP117, EXP118, EXP119, EXP121, EXP123, EXP124 — all bound), one precision certification (EXP110, bound).** The capability column stays at zero — and the identity-readout vs domain-set detection question is now **answered**, not open: domain-set detection.

**Update 2026-09-29:** EXP127 (TGA/TRANSIENT-GROWTH) — **CONTINUE** — the first CONTINUE in the new dynamics paradigm and the first positive signal since the static family's 120-experiment negative. On 10 verbatim EXP107-bench prompts, the frozen L20→L24 final-token clamped-context Jacobian (measured via autograd JVP/VJP products only — the 1024×1024 M never materialized) yields **median R = σ₁/σ̄ = 8.240640 ≥ 3** (per-prompt [8.0019, 8.5294]) and **median σ₁/σ₂ = 1.557689 ≥ 1.5** (per-prompt [1.5302, 1.5881]) — the leading singular direction v₁ amplifies perturbations ≈8× more than the average random direction, with a prompt-invariant amplification structure (a property of the frozen span, not prompt content). All guards passed (protocol hash verified pre-JVP, 10/10 convergence on σ₁ and σ₂, budget 264–318 ≤ 700/prompt, LOG-331 pin before AND after, Δθ=0, Law #9 ordering — raw records hash-pinned before R was read; independent exact-artifact verdict review LOG-4699 — BIND-WITH-CAVEAT, four documentation-only caveats, none verdict-bearing). This licenses ONLY a signed GPU injection-test pre-registration along v₁ (new experiment number, ĉ decision-orthogonality gate, rank-trend gate) — no injection, no steering claim; the downstream GPU test is founder-gated (user's hardware). Honest reading: it reframes the program's negative as "frozen models can't be steered by *snapshot* instruments," with v₁ now the one licensed channel. **The day's tally: four CONTINUEs (EXP111 — bound, reclassified; EXP120 — bound, qualified, reclassified; EXP122 — bound, reclassified; EXP127 — bound), one HELD (EXP112, bench-1-specific), one apparatus CONTINUE (EXP113), four KILLs (EXP107, EXP114, EXP125, EXP126), ten RUN-INVALIDs (EXP108, EXP109, EXP115, EXP116, EXP117, EXP118, EXP119, EXP121, EXP123, EXP124), one precision certification (EXP110).** The capability column stays at zero — a licensed measurement CONTINUE, not a capability entry.

**Update 2026-10-03:** EXP140 (S4-5/J4) — **HELD (G3-null)** — the free-energy-selector family stands down. Stage-1 CPU pilot ($0, 240 generations + 240 scoring passes, all validity gates PASS, Δθ=0): G1 diversity PASS (28/60 items, bar ≥15), G2 variance PASS (median F-spread 1.29 nats/token, bar ≥0.05), **G3 calibration NULL** — C1 Spearman(F̄, accuracy) ρ=0.08, one-sided p=0.73; C2 D=−0.06, p=0.83. The free-energy signal does not predict correctness — signal absent, not inverted. Diagnostic accuracies: B0=70.0%, min-F selection=70.0%, random-branch=76.7% — selection adds nothing; the stochastic branches were almost never selected (temperature vacuity, as predicted). Stage-2 gate does not open; no GPU. The program's only remaining training-free, target-free evaluator candidate is closed at $0. **Update 2026-10-03:** EXP141 (S4-6/J2) — **KILL** — the metacognitive self-modeling family is dead at Stage 1. 60 P(True) self-eval passes on the committed EXP140 baseline records ($0, all validity gates PASS, Δθ=0): G1 FAIL — std(â_self)=0.000045 (bar >0.01), near-constant P("True") across all 60 items; G2 I-screen NULL — Î=0.0716 nats, 100k-permutation p=0.181; G3 NULL (not inverted). The frozen model carries no correctness information about its own answers — self-bias in its purest form (uniform self-rating), the Xu et al. confound confirmed empirically. No revision stage, no Stage-2 GPU. The honest LOW prior is confirmed; the summit-relevant boundary is established: self-modeling, a consciousness prerequisite, is absent in this frozen model at inference time. **Update 2026-10-03:** EXP139 (S4-4/J1) Stage-1 — contraction license **SURVIVES** (κ̂=0.955971<1, 60/60 CPU passes, all gates PASS; LOG-4886) against the explicit honest prior κ̂≥1 — the J-tier's one surviving positive direction. Stage-2 (520 GPU passes) remains founder-gated and unrun. **Update 2026-10-03:** EXP142 (S4-7/J3) — **HELD (C2 guard fired)** — the spectral phase transition question cannot be answered on this bench as specified. Stage-1 CPU observational pilot ($0, 60 passes + 1440 Gram eigendecompositions, all validity gates PASS, Δθ=0): n_i median 32 (IQR [29,35], range [29,35]) — all 60 items below the N_MIN=40 floor → 0/60 kept → primary test VOID → HELD with reason ("insufficient positions for stable spectra"), never KILL. The design's "n_i ≈ 100 typical" pricing was factually wrong — actual bench prompts are ~30 tokens; the bulk-fit diagnostic (median KS=0.4108, FLAGGED) confirms the guard's firing is measurement-justified. The family is held, not killed; the spectral intervention is never attempted (pre-registered sequencing). **Frontier watch 2026-10-03:** Alibaba's RSI disclosure (Qwen3.8-Max, 33 cycles, 40→45), DeepMind's consciousness-assessment framework (arXiv:2609.35618), frozen-decoder memory compression (arXiv:2609.25537), and Percepta Spotlight (Δθ=0 writable-memory architecture) — all logged; none changes the capability column, which stays at zero. **The tally: ten KILLs, twelve RUN-INVALIDs, four HELDs, four CONTINUEs + one apparatus CONTINUE, two precision certifications.** The capability column stays at zero.

**Update 2026-10-05:** the S7 morning wave closed two lines and fenced a third. **EXP143 (S5-INV) — KILL** (LOG-4917): the S5 free-energy-spread anti-calibration (discovery ρ=−0.4899, p=6e-5) did not replicate on 60 held-out items — primary ρ=+0.1156, one-sided p=0.8103, 95% CI [−0.1426, +0.3590]; secondary selector gain Δ=−0.0417, p=0.7075 — the discovery was winner's curse, and the label-free selection line now has no surviving candidate on this bench family. **EXP144 — INCONCLUSIVE** (LOG-4919): the GPT-2-small cross-family replication aborted at Step 0 — G1′ fired 232/240 on GPT-2 BPE (Triton 0/8 single-token, an intrinsic vocabulary fact); zero forwards, weights never downloaded; the cross-family question untested, not falsified. **EXP145 (S7-2b, Triton→Neptune bench) — KILL/PIVOT** (LOG-4925; independent verdict review LOG-4926 — ADOPTED): D1 passed (layers 8, 10 decode-significant; l\*=8 acc=0.2833, p=0.000999, effect +0.1333) but D2 failed cleanly (mean shared-direction cosine −0.4587 vs 0.70 bar, instrument non-degenerate) — decode+ = FALSE, intervention not licensed; the Decodability Gap's cross-family generality is killed/bounded with the recorded caveat (precondition absent; cannot separate architecture from scale/bench-fit); the Gap remains a Pythia-scale boundary result and the dissociation itself is untested in the GPT-2 family. **Paper: v100 SIGNED** (LOG-4927, 26 pp, MD5 7ea5a49347bdbc17529d9e4c088aefc1) — Fig 8 removed, clean minimal figures; v98/v99 withdrawn from current use after the user's QA rejections; user acceptance pending. **The tally: twelve KILLs, twelve RUN-INVALIDs, four HELDs, four CONTINUEs + one apparatus CONTINUE, two precision certifications, one INCONCLUSIVE.** The capability column stays at zero — SCBI's lead remains boundary science: the 0.7-cosine zero-causal-transfer dissociation with the retraction on record, now joined by a fenced cross-family non-replication and a closed label-free selection line.

**Update 2026-10-06:** EXP148 (S7-1/J7, first-token scoring repair) —
**the program's first capability entry.** S (WRITE/READ scratchpad) vs
budget-matched C (CoT): b=52, c=12, net **+0.2222 (+22.2pp)**, one-sided
McNemar p=**2.2833e-07**, 95% Wald CI (0.1414, 0.3031) → CONTINUE,
independently verdict-reviewed **ADOPTED** (LOG-4958 execution;
LOG-4959 review; scoreboard v3.23, LOG-4960). **The zero-capability
headline that stood in every earlier update block is retired with this
entry** — this is the first positive capability result in the program's
history. Mandatory caveats, carried: C-arm absolute 0.1889 — the licensed
claim is "discipline beats budget-matched CoT," NOT "beats the best
baseline" (S vs B net −0.2500; B=0.6611 stands); this is reasoning
capability via prompting discipline, NOT autonomous steering (the
label-free steering axis stays tied at zero); single model
(Pythia-410m), single bench family. **The tally: twelve KILLs, twelve
RUN-INVALIDs, five HELDs, four CONTINUEs + one apparatus CONTINUE, one
capability CONTINUE (EXP148), two precision certifications, one
INCONCLUSIVE (EXP144).**

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
