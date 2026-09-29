# INNOVATION DESIGN SESSION — post-EXP123 (LOG-4665)

*Lane: LOG-4665 (pre-assigned). $0 CPU strategy memo: no execution, no
experiment numbers minted, no signed artifact modified, no GPU contact,
no commits, no pushes.*

**Read:** `INNOVATION_DESIGN_SESSION_POST_EXP120_2026-09-29.md` (LOG-4638),
`EXP121_PTTSCSUFFIX_REPORT_2026-09-29.md` (LOG-4644, incl. LOG-4646 erratum),
`VERDICTREVIEW_EXP122_2026-09-29.md` (LOG-4654), `EXP122_POSITIONCUE_REPORT_2026-09-29.md`
(LOG-4653), `EXP123_P4APPARATUS_REPORT_2026-09-29.md` (LOG-4661),
`VERDICTREVIEW_EXP123_2026-09-29.md` (LOG-4662), `H18_GATE_2026-09-29.md`
(LOG-4639), `FRONTIER_SCOREBOARD.md` (v2.8).

**State of play (v2.8):** three CONTINUEs (EXP111, EXP120 qualified,
EXP122 bound — the trained-head identity-readout line, three benches,
position decorrelated), one HELD (EXP112, bound, label-free), one
apparatus CONTINUE (EXP113, bound), two KILLs (EXP107, EXP114 — bound),
nine RUN-INVALIDs (108, 109, 115, 116, 117, 118, 119, 121, 123 — all
bound), one precision certification (EXP110, bound). **Capability
scoreboard: still zero positive signals for autonomous steering; the
label-free race stays tied at zero.**

**Closed lines this cycle:** H11's planning question is now
RUN-INVALID on THREE logit-channel compositions — EXP117 (generation
channel dead), EXP119 (tokenization-identity break), EXP121 (plan-arm
G1 mass collapse, 38/60 < 48 — the valid-item dropout is selection-
biased against the treatment, see H21 §2 breaking point). The hypothesis
is alive; all three tested compositions are retired. The entity-name
generation channel is TERMINALLY dead (EXP123 closed it: P2/EXP115,
P5/EXP116, P4/EXP123 — no fourth protocol licensed on this shape).
H18's bench-2 reuse is dead (apparatus-void: 4/10 multi-token entities);
bench 2 stays contaminated for the logit apparatus.

**Apparatus lessons binding on this memo:**
(i) No entity-name generation anywhere, on any design, unless the
design's breaking point is itself elicitation (EXP123 terminal rule).
(ii) Any plan-context composition must carry the [-3:] tokenization-
identity pin or retire under the H14 rule (EXP119 lesson).
(iii) Per-item G1 validity cannot be screened post-hoc on the treatment
arm — items where the plan arm collapses the final-position mass are
exactly the items where the treatment "did something"; dropping them
biases the estimand, not just the power (EXP121 lesson).
(iv) p-values executor-computed, never hand-written; raw generation
records persisted before any verdict (EXP120/EXP121 defect classes).
(v) Single-token entities asserted at construction for any bench meant
for the logit apparatus (EXP090/H18 lesson).

---

## H21 candidate: plan-as-instrument-selection (a NEW H11 apparatus)

1. **Exact question:** Does plan-conditioned *instrument selection* —
   the EXP113-cleared T2-P2 planner choosing between two phrasing
   variants of the decision prompt, plan text never entering the
   decision prompt itself — change the zero-generation logit-level
   decision (EXP112's apparatus) relative to a random-choice control
   on the EXP107 bench? (Paired McNemar, plan-chosen vs random-chosen
   arms.)

2. **Decision changed:** paired two-sided McNemar on n_valid items:
   p ≤ 0.05 → CONTINUE — the hypothesis "plan-informed instrument
   selection moves decisions vs random, label-free" continues; this
   would be the program's first label-free plan→decision causal
   signal. p > 0.05 with pre-registered ≥80% power for a 10pp paired
   shift → KILL (plan-informed choice moves nothing under this
   apparatus — retires instrument-selection as a channel). p > 0.05
   underpowered → HELD, no rescue. G1 non-degeneracy guard (M ≥ 0.01
   channel-level, H6's pin) per arm; any arm degenerate → RUN-INVALID.
   Backbone Δθ=0 pins (LOG-331) before and after; raw records
   persisted before the verdict.

3. **Summit filter:** **YES** — adaptive plan→decision loops are the
   summit's mechanism class, and this is the first live design for
   H11's question that does not put plan tokens in the prompt. An
   honest caveat rides with the CONTINUE: instrument selection is
   steering-adjacent (the plan chooses the measurement), not full
   autonomous steering; it still belongs to the label-free axis (§2.1
   None class — no training, no labels).

4. **Apparatus dodge (all three H11 failure modes):**
   - EXP117 (generation dead): no entity-name generation anywhere —
     readout is EXP112's pinned logit channel only.
   - EXP119 (tokenization identity): plan text **never enters any
     decision prompt** — both phrasing variants are byte-verbatim
     fixed strings; the [-3:] identity surface does not exist.
   - EXP121 (G1 mass collapse): the readout prompts are the pinned
     baseline prompt — G1 behavior is the EXP112-archived channel's
     own, reproduced 60/60 in EXP121; plan tokens cannot push mass
     off the final position because they are never in the context.
   The EXP121 selection-bias lesson is honored structurally: G1
   validity is a property of the *prompt variants* (screened at
   Phase-0 on the probe set), not of post-hoc per-item dropout on a
   treatment arm.

5. **Worth-it sketch:** cheapest test — 60 planner choice-generations
   (T2-P2 pinned prompt + a pinned choice-extraction) + 120 baseline
   forwards (60 items × 2 phrasing variants) + 60 choice-arm forwards
   = 240 forwards + 60 gens, $0 CPU. Mathematical license: EXP113
   T2-P2 CONTINUE (the planner channel works on EXP107 — EXP119
   Phase-0a 10/10, EXP121 Phase-0a 10/10) + EXP112 HELD (the readout
   works — 41/60, and 60/60 baseline reproduction in EXP121); the
   EXP107 schema carries a `phrasing` field with genuine variants.
   Quantitative prediction: no directional accuracy claim is licensed —
   the test is for any systematic paired difference, bars as in §2.
   Breaking points (all RUN-INVALID, pre-metric): Phase-0a planner
   choice-valid <8/10, OR the choice is constant (each phrasing chosen
   <20% of probe items — an information gate, no default choice);
   Phase-0b the two phrasings are NOT decision-discriminable at the
   EXP112 readout site on a probe set (registered bar, e.g. <3/10
   differ — a constant-choice control cannot be a treatment); any arm
   G1-degenerate; backbone pin mismatch.

6. **License conflicts:** H11's hypothesis was RUN-INVALID three
   times — **never KILLED**; instrument-selection is a NEW channel
   under Law #4, not a re-run of any dead composition (no generation
   channel, no plan-prefix, no plan-suffix). New hypothesis number
   required at the worth-it lane; does not re-adjudicate any bound
   verdict (Law #8); uses no bench-1 archive re-read beyond the pinned
   protocol copies (Law #9 honored — fresh forwards only).

**Disposition: ACCEPT as H21 (worth-it-gate lane next, priority 1 —
the summit's mechanism class; the only $0 CPU design that gives H11 a
live channel).**

---

## H22 candidate: EXP112's HELD honesty readout on a FRESH bench (H18 re-licensed)

1. **Exact question:** Does EXP112's logit-level honesty fidelity
   (41/60, HELD, label-free) hold on **bench 4** — a newly constructed,
   independently built template-decorrelated bench (new entity sets,
   new templates, single-token entities asserted at construction) —
   under EXP112's exact pinned apparatus?

2. **Decision changed:** H6's SIGNED bars bind any re-licensing (the
   LOG-4639 bar-discrepancy audit — the design session's 45-band and
   the dispatch's 38-band are both overruled by H6's signed pre-reg
   §4): 42–57/60 → CONTINUE the honesty instrument toward a decisive
   reading; 34–41/60 → HELD holds (generality of the band); ≤33/60 →
   KILL of the generality hypothesis — EXP112's bench-1 HELD stands
   per Law #8, reclassified bench-specific (Law #11 two-layer tagging);
   =58/60 → HELD; ≥59/60 → KILL. Unlicensed fence carries over: no
   statistical comparison between bench-1 and bench-4 fidelities.

3. **Summit filter:** **YES** — the label-free race is the only axis
   where the frontier is also at zero; it is the program's actual
   race. An honest self-report readout on a frozen model is the
   summit's mechanism class.

4. **Apparatus dodge:** zero generation (logit readout — EXP117's
   failure impossible); reads at L24/final layer only, where the
   41/60-exact consistency pin is proven (EXP118's early-layer silence
   never entered); no plan text (EXP119's break has no purchase).
   Contaminated bench 2 is never touched — bench 4 is construction-
   fresh (EXP090/H18 lesson: single-token entity assertion at
   construction, byte-exact decomposition gate).

5. **Worth-it sketch:** cheapest test — 240 fresh forwards, $0 CPU
   (60 premise-embedding extractions L20-final-token + 120 single-
   token option embeddings + 60 self-report forwards; the LOG-4639
   correction stands — all fresh, Law #13). Δθ=0 (LOG-331 pin
   before/after). Mathematical license: EXP112 HELD 41/60,
   P(X≥41|60,0.5)=0.0031 — a real above-chance signal on bench 1; the
   two-bench discipline is now pinned and thrice executed (EXP111/
   EXP120/EXP122 constructions). Quantitative prediction (directions
   only): under generality, fidelity inside the 34–41/60 band or above
   it; under bench-specificity, collapse toward 30/60. Breaking
   points: BPE single-token assertion fails on any bench-4 entity →
   lane dies at construction, no pre-reg; byte-exact decomposition
   gate fails → no pre-reg; channel-level G1 M ≥ 0.01 guard fails →
   RUN-INVALID, no metric.

6. **License conflicts:** new bench, new forwards, no Law #9 re-read;
   EXP112's HELD restated, never re-adjudicated (Law #8); new
   hypothesis under a new apparatus (Law #4).

**Disposition: ACCEPT as H22 (worth-it-gate lane next, priority 2 —
the label-free race; H18's hypothesis re-licensed on clean ground).**

---

## H23 candidate: within-domain decoy dissection of the identity-readout line

1. **Exact question:** Is the EXP111/EXP120/EXP122 trained-head signal
   an **entity-level identity readout** or a **coarse domain-set
   detector** (animals-vs-fruits membership)? Test: the pinned H5 head
   protocol on bench 5 — same template/decorrelation discipline as
   EXP122's construction, but target and distractor drawn from the
   SAME domain (both animals or both fruits), label = which entity.

2. **Decision changed:** bars carried from the H15/H16 discipline —
   ≥20/30 with G<0.30 → CONTINUE the entity-identity interpretation
   (the three-bench CONTINUE gains a genuinely mechanistic foothold:
   the head reads identity, not just set membership); ≤18/30 or
   G≥0.30 → KILL the identity interpretation — the three-bench line
   is reclassified as a **domain-set-detector correlation**
   (Law #11 two-layer tagging; the observations stand, the
   interpretation narrows); 19/30 with G<0.30 → HELD, no rescue.

3. **Summit filter:** **NO** — boundary-science dissection, not a
   summit move. It clarifies what the program's best observation IS;
   it does not add capability, routing, or a loop. Worth it only as
   license-maintenance: a coarse domain-detector story kills any
   entity-level use of the signal.

4. **Apparatus dodge:** pinned H5 head protocol (embeddings + sklearn,
   zero generation — EXP117's failure impossible); layer 20 only,
   where the three-bench line is bound (EXP118 never entered); no
   plan text, no tokenization-identity surface.

5. **Worth-it sketch:** cheapest test — one 60-item bench-5
   construction (EXP120's discipline + same-domain-decoy gates) + 60
   layer-20 CPU extractions + the byte-verbatim H5 head spec
   (seed 20260929, stratified 30/30, no sweeps), $0 CPU.
   Mathematical license: EXP122's CONTINUE (27/30, G=−0.0667, position
   decorrelated) leaves domain-membership as the named surviving
   confound in the narrow reading. Quantitative prediction
   (directions only): under entity-identity, ≥20/30 with G<0.30;
   under coarse-detector, collapse toward chance or G≥0.30 (the
   distractor now shares the target's domain). Breaking point: bench
   construction is the breaking point — the EXP120 discipline
   (design assertions, G-C1 ≤36/60, G-C2 |Pearson|≤0.10, G-C3
   byte-exact decomposition, Law-#7 own-label pin) PLUS same-domain-
   decoy gates (target and distractor same domain on every item,
   domain balanced across label classes); any gate fails → lane dies
   at construction, no head trained.

6. **License conflicts:** independent apparatus (Law #13); fresh head
   on fresh bench's own pinned labels (Law #7); no re-read of any
   prior bench's embeddings (Law #9); count-based executor bars (the
   EXP120 p-value defect class pinned away); no S6-4/L11 injection
   (the LOG-4464 stand-down).

**Disposition: ACCEPT as H23 (worth-it-gate lane next, priority 3 —
decides what the program's best observation is).**

---

## Candidate (d): the honest capability answer

(d) asked what would move the capability scoreboard off zero. The
honest answer: **H21 is the answer.** No other $0 CPU design on the
table names a label-free decision-moving mechanism with a real
mathematical license. The trained-head line is Train-probes class —
it can never beat the None-class frontier rows on the label-free axis
(§2.1), and its selective-abstention use is therefore rejected as a
capability candidate (it would repeat the "probe beats frontier"
error the rejections list bars). The GPU queue (K2 → EXP083 →
EXP084 → EXP086-B/EXP088 → EXP087, R4, K3 Phase-1) stays founder-
gated and is not a CPU-licensed candidate. Boundary science remains
the program's honest deliverable; H21 is the only live capability-
adjacent bet.

---

## Explicitly rejected (staying dead)

- **Fourth generality bench (new domain families):** the KILL bar —
  "reclassify the three-bench line as domain-pair-specific" — is a
  real decision, but it has no downstream consequence the program can
  act on, unlike H23's mechanism narrowing (which kills entity-level
  use of the signal). One head-line lane at a time: H23 is the
  sharper question. A fourth-bench generality lane may return as a
  follow-up only if H23 CONTINUES. Rejected for now.
- **H17 layer profiling (standalone)** — descriptive, no decision
  bars; stays rejected.
- **S5 blind-spot closure (1–4.87% band)** — fails "decision
  changed"; capability stays zero either way.
- **Fifth externally-computed gate** — barred by the LOG-4460
  terminality claim and the LOG-4464 stand-down.
- **H12 re-reading / bench-1 re-reading** — Law #9; barred.
- **EXP117/118/119/121/123 exact dead compositions re-run** — each
  verdict retires exactly its tested composition; repetition without
  a new channel is not licensed.
- **Entity-name generation channel on any new composition** — EXP123
  terminal rule.
- **Anything requiring GPU or founder hardware action** — founder-
  gated, not CPU-licensed.
- **Selective abstention / routing with the trained head as a
  capability claim** — Train-probes class cannot beat None-class
  frontier rows (§2.1); the claim would be the barred "probe beats
  frontier" error.
- **Claims that a trained-probe result beats a label-free frontier
  row** — §2.1 forbids it.

---

## Ranked recommendation

1. **H21 — plan-as-instrument-selection.** One line: the summit's
   mechanism class, H11's only live channel, all three failure modes
   structurally dodged — the only $0 CPU capability-adjacent bet.
2. **H22 — EXP112 honesty generality on fresh bench 4.** One line: the
   label-free race is the actual race; H18's hypothesis re-licensed on
   clean, single-token-asserted ground.
3. **H23 — within-domain decoy dissection.** One line: decides whether
   the program's best observation is an identity readout or a coarse
   domain detector — license-maintenance for the three-bench line.

*Single-lane fence applies to each: worth-it-gate lane → pre-
registration draft → independent Law #14 review → fix-verification →
CEO launch decision → execution under a minted number. No lane may
advance itself.*

*Defect classes carried forward (binding on all future pre-
registrations): (1) p-values executor-computed, never hand-written;
(2) raw generation records persisted before any verdict; (3) no
truncated-comment label citations (FIX-1 discipline); (4) no reuse of
EXP117's §3.7 recitation definition; (5) the [-3:] tokenization-
identity pin on any plan-context composition; (6) per-item G1 validity
may not be screened post-hoc on a treatment arm (EXP121 lesson); (7)
single-token entities asserted at construction for any logit-
apparatus bench (EXP090/H18 lesson).*
