# INNOVATION DESIGN SESSION — post-EXP120 (LOG-4638)

*Lane: LOG-4638 (pre-assigned). $0 CPU strategy memo: no execution, no
experiment numbers minted, no signed artifact modified, no GPU contact,
no commits, no pushes.*

**Read:** `INNOVATION_SPRINT_2026-09-29_H1315.md` (LOG-4615), `H15_GATE_2026-09-29.md`
(LOG-4630), `VERDICTREVIEW_EXP120_2026-09-29.md` (LOG-4634), `FRONTIER_SCOREBOARD.md`
(v2.5, §3.1/§3.2 inventory).

**State of play (v2.5):** two CONTINUEs (EXP111, EXP120 — both bound),
one HELD (EXP112, bound), one apparatus CONTINUE (EXP113, bound), two KILLs
(EXP107, EXP114 — both bound), seven RUN-INVALIDs (EXP108, EXP109, EXP115,
EXP116, EXP117, EXP118, EXP119 — all bound), one precision certification
(EXP110, bound). **Capability scoreboard: zero positive signals for
autonomous steering; the label-free race stays tied at zero.**

**Alive lines:** EXP111/EXP120's two-bench trained-head decodability signal
(layer 20, subject-position cue — correlation, not capability); EXP112's
logit-level honesty instrument (41/60, HELD); EXP113's T2-P2 elicitation
apparatus (60/60, CONTINUE); H11's planning hypothesis (RUN-INVALID twice
on two apparatuses — hypothesis alive, both tested compositions retired).

**Three binding apparatus lessons this memo must dodge or honor:**
(i) EXP117/109/115/116: the generation channel for entity-name answers is
dead on base Pythia-410m across four apparatuses — zero generation in all
new designs unless the design's breaking point is itself elicitation;
(ii) EXP118: early-layer logit lens is silent (0/9 non-degenerate) — read
only where the instrument is proven live (L24 consistency pin 41/60-exact,
or layer-20 extraction where EXP111/EXP120 are bound);
(iii) EXP119: tokenization breaks plan-prefix channels — any plan-context
composition must carry the [-3:] tokenization-identity pin or retire it
with the same rule; any plan text must be byte-verified under the real
tokenizer. Plus the EXP120 defect class: **p-values are executor-computed,
never hand-written** — future pre-registrations pin this.

---

## H16 candidate (a): position-cue dissection of the two-bench head signal

1. **Exact question:** Is the EXP111/EXP120 trained-head signal (layer 20,
   final-token embeddings) a *subject-position detector* or an *entity-identity
   readout*? Test: the pinned H5 head protocol on a newly constructed
   position-scrambled bench (same template/decorrelation discipline as
   EXP107/EXP120, but the target entity's sentence position carries no
   information — scrambled across premise slots).

2. **Decision changed:** bars carried from the H15 discipline —
   ≥20/30 with G<0.30 → CONTINUE the **identity-readout** interpretation
   (the signal survives position decorrelation; the two-bench CONTINUE
   gains a mechanistic foothold); ≤18/30 or G≥0.30 → KILL the identity
   interpretation — the two-bench CONTINUE is **reclassified as a
   position-detector correlation** (downgrade under Law #11's two-layer
   tagging; EXP111/EXP120's observations stand, their interpretation
   narrows); 19/30 with G<0.30 → HELD, no rescue.

3. **Summit filter:** **NO** — this is boundary-science dissection, not a
   summit move. It does not add capability, routing, or a self-improving
   loop; it clarifies what the program's best observation *is*. It is
   worth it only as license-maintenance for the two-bench line: a
   position-detector story kills any mechanistic use of the signal.

4. **Apparatus dodge:** uses the pinned H5 head protocol (embeddings +
   sklearn, zero generation — EXP117's failure impossible); reads at
   layer 20 only, where EXP111/EXP120 are bound (EXP118's early-layer
   degeneracy never entered); no plan text, no tokenization-identity
   surface (EXP119's break has no purchase).

5. **Worth-it sketch:** cheapest test — one 60-item position-scrambled
   bench + 60 layer-20 CPU extractions + the byte-verbatim H5 head spec
   (seed 20260929, stratified 30/30, no sweeps), $0 CPU. Mathematical
   license: EXP120's 25/30 (p=0.00016) with G=−0.2000 is a real two-bench
   signal; position is the only surviving confound named by both verdict
   reviews' narrow readings. Quantitative prediction (directions only):
   under identity-readout, ≥20/30 with G<0.30; under position-detector,
   collapse toward chance or G≥0.30 (the flipped-cell cells now flip the
   position cue too). Breaking point: **bench construction is the breaking
   point** — the EXP120 discipline (design assertions, G-C1 ≤36/60,
   G-C2 |Pearson|≤0.10, G-C3 byte-exact decomposition, Law-#7 own label
   pin) PLUS a position-scramble gate (target position decorrelated from
   the label — pure-position detector ≤36/60 on the new bench); any gate
   fails → lane dies at construction, no head trained.

6. **License conflicts:** new bench = independent apparatus (Law #13 —
   no bench-1/bench-2 labels or embeddings enter analysis); the head is
   fit fresh on the new bench's own pinned labels (Law #7); the bars are
   count-based from the executor (the EXP120 p-value defect class is
   explicitly pinned away). Does not re-read EXP111/EXP120 data (Law #9),
   does not touch the S6-4 stand-down (no L11 injection), H12 (no
   re-reading), EXP117/118/119 (no channel re-run). **Compliant.**

**Disposition: ACCEPT as H16 (worth-it-gate lane next, priority 3).**

---

## H17 candidate (b): layer-profiling of the two-bench head signal — REJECTED as a standalone lane

The EXP111 report already carries a descriptive per-layer secondary
(L4 24/30 G=−0.1333; L8 30/30 G=0.0000; L12 29/30 G=0.0667; L16 30/30
G=0.0000 — the position cue is decodable across layers, no signature
anywhere). A pre-registered repeat on bench 2 changes **no decision**:
EXP120's CONTINUE is already bound; a "diffuse" vs "local" answer fires no
pre-registered bar — there is no KILL/CONTINUE/PIVOT attached to the
profile, only description. This is descriptive science without a killing
decision — the worth-it gate's item 2 fails. **Rejected as standalone.**
Layer-resolved bars may be folded into H16's design only if the worth-it
lane can name a decision they change (none found at design-session level).

---

## H18 candidate (c): EXP112's honesty instrument on bench 2 — the label-free generality test

1. **Exact question:** Does EXP112's logit-level honesty fidelity (41/60,
   HELD, label-free) replicate on bench 2 — the independently constructed
   decorrelated bench (60 items, new river+tree entities, `exp120_*`
   namespace) — under EXP112's exact pinned apparatus?

2. **Decision changed:** bars mirrored from the H6 discipline —
   fidelity ≥45/60 (P(X≥45|60,0.5)=0.0002, the decisive band the H6
   pre-reg named) → CONTINUE the honesty instrument toward a decisive
   reading; 34–41/60 → HELD holds (generality of the *band*, not the
   point); <34/60 or any degeneracy guard fires → the HELD is reclassified
   bench-specific (Law #11 two-layer tagging; EXP112's observation stands).
   The unlicensed fence carries over: no statistical comparison between
   bench-1 and bench-2 fidelities.

3. **Summit filter:** **YES** — the label-free race is the only axis where
   the frontier is also at zero, and it is the program's actual race. An
   honest self-report readout on a frozen model is the summit's mechanism
   class (self-consistent representation needs honest internal readouts).
   EXP112 is label-free (None class — no training, no labels); EXP111/EXP120
   are Train-probes class and can never win the label-free axis (§2.1).

4. **Apparatus dodge:** zero generation (logit readout — EXP117's failure
   impossible); reads at **L24/final layer only**, where the 41/60-exact
   consistency pin is proven (EXP118's early-layer silence is sidestepped
   by never going early); no plan text — the [-3:] tokenization-identity
   surface does not exist (EXP119's break has no purchase); BPE + suffix
   pins re-run on bench 2's own tokens (see breaking point).

5. **Worth-it sketch:** cheapest test — 60 fresh single-token forwards on
   bench 2's items at the EXP112 decision site, $0 CPU, Δθ=0 (LOG-331 pin
   before/after). Mathematical license: EXP112 HELD 41/60 with
   P(X≥41|60,0.5)=0.0031 — a real above-chance signal on bench 1; the
   two-bench discipline is now pinned and twice executed. Quantitative
   prediction (directions only): under generality, fidelity inside the
   34–41/60 band or above it; under bench-specificity, collapse toward
   30/60. Breaking point: **pinning is the breaking point** — bench 2's
   entity tokens must pass the BPE single-token assertion (120/120 on
   bench 2's own token ids) AND bench 2 must expose a byte-exact
   QUESTION_SUFFIX-equivalent decomposition; either fails → lane dies at
   pinning, no metric read (RUN-INVALID, no verdict smuggled). Note:
   bench-2 entities (rivers/trees: Yangtze, Thames, Ganges) must be
   verified single-token under the real tokenizer before the pre-reg is
   drafted — the EXP090/EXP118 lesson.

6. **License conflicts:** bench 2 is an independent apparatus (Law #13 —
   bench-2 items are construction-fresh; no bench-1 archive re-read,
   Law #9); no labels anywhere in the apparatus (Law #7 moot, honored by
   construction); EXP112's HELD is restated, never re-adjudicated
   (Law #8); this is a new hypothesis under a new apparatus, not a repair
   of EXP112 (Law #4). **Compliant.**

**Disposition: ACCEPT as H18 (worth-it-gate lane next, priority 1 — the
label-free race is the actual race).**

---

## H19 candidate (d): H11's planning question through a suffix channel

1. **Exact question:** Does plan text inserted as a **suffix between the
   premise and the question** — so the final `…? Answer:` token run is
   byte-identical in both arms — change the zero-generation logit-level
   decision (EXP112's apparatus) relative to the no-plan baseline on the
   EXP107 bench? (Paired McNemar, same as H14's bars.)

2. **Decision changed:** one-sided paired McNemar on n_valid items,
   p ≤ 0.05 with b > c → CONTINUE (the suffix plan-conditioned pipeline
   licensed as an adaptive-loop component); net (b−c) ≤ 0 → KILL
   (plan-conditioning moves nothing even at the logit level through a
   working channel — retires plan-conditioning on this bench's logit
   channel); net > 0, p > 0.05 → HELD. Phase-0a (<8/10 planner-valid →
   RUN-INVALID) and the tokenization-identity pin (mismatch on ANY item →
   RUN-INVALID immediately) carried verbatim from H14's pre-reg.
   n_valid ≥ 48/60 or RUN-INVALID.

3. **Summit filter:** **YES** — adaptive plan→decision loops are the
   summit's mechanism class, and this is the only live approach to H11's
   planning question. PASS.

4. **Apparatus dodge:** zero generation (EXP117's failure impossible);
   the [-3:] identity holds **by construction** (suffix placed
   before the fixed `? Answer:` tail) but is still verified by the
   same mechanical pin — if it fails on any item, the H14 rule fires
   RUN-INVALID immediately (EXP119's break is the gate, not the fate);
   Phase-0a planner transfer is already 10/10 on EXP107 (EXP119's
   apparatus observation — reduces but does not remove the elicitation
   gate); consistency pin against EXP112's archived readout on the
   baseline arm before any metric read (the EXP118 integrity lesson).

5. **Worth-it sketch:** cheapest test — tokenizer-only verification of
   the [-3:] identity on the suffix design + 10 planner generations +
   120 forwards, $0 CPU. Mathematical license: EXP112's HELD (the
   decision channel works), EXP113's T2-P2 clearance (the planner
   channel works), EXP119 Phase-0a 10/10 (transfer holds on EXP107) —
   the composition is the untested question. Quantitative prediction:
   no directional effect licensed; the test is for any paired
   difference, bars as above. Breaking point: the tokenization-identity
   pin fails on any item (the suffix does not perfectly preserve the
   tail under the real tokenizer) → RUN-INVALID, full run never
   licensed; or Phase-0a <8/10 → RUN-INVALID.

6. **License conflicts:** H11's planning **hypothesis was RUN-INVALID
   twice on two apparatuses — never KILLED as a hypothesis**; the
   suffix composition is a NEW channel, not a re-run of EXP117's
   generation pipeline or EXP119's prefix+identity composition (H14's
   brief licensed exactly this succession). The H14 honesty fence binds
   prospectively: token asymmetry (suffix vs no-suffix) + greedy
   determinism → a CONTINUE licenses the pipeline as a component,
   never planning-vs-compute attribution. **Compliant.**

**Disposition: ACCEPT as H19 (worth-it-gate lane next, priority 2 —
the summit's mechanism class, with the failure mode structurally gated).**

---

## H20 candidate (e): P4 (repetition-penalty) apparatus validation on the entity-name shape

1. **Exact question:** Does the P4 repetition-penalty protocol (cleared
   T1-only at 58/60, EXP113) elicit ≥80% mechanically-parseable entity-name
   self-reports on the EXP107 template-decorrelated bench — the shape
   where P2 died (recitation) and P5 died (tail echo)?

2. **Decision changed:** ≥48/60 parseable (EXP113's clearance bar) →
   CONTINUE — licenses the honesty-instrument revival line with P4 as a
   NEW hypothesis carrying its own elicitation-failure gate; the gate
   n_unparseable ≥ 7 fires → RUN-INVALID (the entity-name generation
   channel is then dead on all EXP113-cleared protocols, and the line is
   closed on this shape — a terminal apparatus verdict).

3. **Summit filter:** **MARGINAL** — apparatus validation, not a summit
   move. It re-opens (or permanently closes) the honesty-instrument line,
   which is summit-relevant only at second order.

4. **Apparatus dodge:** the EXP116 review's own note marks P4 as the one
   untested protocol on the entity-name shape — this tests exactly the
   disclosed risk; generation is gated by the pre-registered
   elicitation-failure gate (the EXP108/115/116 lesson); raw per-item
   generation records persisted before any verdict (the EXP119 lesson).

5. **Worth-it sketch:** cheapest test — 60 generations, $0 CPU.
   Mathematical license: EXP113 cleared P4 at 58/60 on the T1 shape; the
   entity-name shape is the registered unknown. Quantitative prediction:
   binary — the clearance bar is the prediction. Breaking point: the
   P4 penalty derails outlines the way it did on T2 (EXP113: P4=0/60 on
   outlines) → the gate fires, RUN-INVALID, line closed.

6. **License conflicts:** new hypothesis under a named-but-untested
   protocol (EXP113's explicit license), not a revival of H9/H10
   (Law #4); no closed channel re-run. **Compliant.**

**Disposition: ACCEPT as H20 (worth-it-gate lane, priority 4 —
apparatus-only, last resort if H16–H19 are blocked).**

---

## Explicitly rejected (staying dead)

- **H17 (b) as a standalone lane** — descriptive profiling with no
  decision bars; EXP111's descriptive secondary already maps it (see §H17).
- **S5 blind-spot closure (1–4.87% band)** — still fails "decision
  changed" (LOG-4615 ruling stands; capability stays zero either way).
- **Any fifth externally-computed gate variant** — barred by the
  LOG-4460 terminality claim and the LOG-4464 stand-down ("the direction
  is the problem, not the gate").
- **H12 stratified re-reading** — killed at gate (LOG-4613); Law #9.
- **Re-reading EXP111's bench-1 embeddings for any new metric** — Law #9
  theater, barred (the H12/H15 lesson).
- **EXP117/118/119's exact dead compositions re-run** — each verdict
  retires exactly its tested composition; repetition without a new
  channel is not licensed.
- **Anything requiring GPU or founder hardware action** — founder-gated,
  not CPU-licensed.
- **Cross-model EXP112 check** — still deprioritized (no pinned second
  checkpoint; bench-generality via H18 is cheaper).
- **Any claim that a Train-probes result "beats" a None-class frontier
  row** — §2.1 forbids it; the label-free race is the only axis where
  SCBI is not behind.

---

## Ranked recommendation

1. **H18 (c) — EXP112 honesty generality on bench 2.** One line: the
   label-free race is the actual race, and this is the cheapest decisive
   test of whether the program's only label-free signal generalizes.
2. **H19 (d) — planning via the suffix channel.** One line: the summit's
   mechanism class, hypothesis alive, both prior deaths structurally
   gated by the same pre-registered pins.
3. **H16 (a) — position-cue dissection.** One line: license-maintenance
   for the two-bench CONTINUE; decides whether the signal is a position
   detector or an identity readout.
4. **H20 (e) — P4 apparatus validation.** One line: last-resort
   apparatus lane; permanently closes or re-opens the honesty
   instrument on the entity-name shape.

*Single-lane fence applies to each: worth-it-gate lane → pre-registration
draft → independent Law #14 review → fix-verification → CEO launch
decision → execution under a minted number. No lane may advance itself.*

*Defect classes carried forward (binding on all future pre-registrations):
(1) p-values are executor-computed, never hand-written; (2) raw generation
records persisted before any verdict; (3) no truncated-comment label
citations (FIX-1 discipline); (4) no reuse of EXP117's §3.7 recitation
definition; (5) the [-3:] tokenization-identity pin on any plan-context
composition.*
