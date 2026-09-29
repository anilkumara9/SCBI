# INNOVATION_SPRINT_2026-09-29_H1315 — candidate hypotheses H13/H14/H15

*Lane: LOG-4615. $0 CPU strategy proposal. No execution, no experiment numbers
minted, no signed artifact modified.*

**Scoreboard context (v2.2):** one CONTINUE (EXP111, bound, qualified),
one HELD (EXP112, bound), one apparatus CONTINUE (EXP113, bound), two KILLs
(EXP107, EXP114), five RUN-INVALIDs (EXP108, EXP109, EXP115, EXP116, EXP117),
one precision certification (EXP110). Capability scoreboard unchanged: zero
positive signals for autonomous steering; the label-free race stays tied
at zero.

**Alive lines:** H6's logit-level honesty instrument (EXP112, 41/60 HELD);
EXP111's trained output-side head (24/30, G=0.0000, CONTINUE, decodability
not steering); EXP113's T2-P2 elicitation apparatus (60/60 CONTINUE); the
adaptive-loop program (H11 RUN-INVALID was apparatus failure, not a
hypothesis kill).

**Closed axes (never resurrect):** entity-name generation shapes on base
Pythia-410m (EXP109/115/116/117 — four failures); flipped-cell
stratification (H12 killed at gate, p=0.0946); positional-order ensembling
(EXP114 KILLED); static cross-position injection at L11 (EXP094 KILLED);
new experiment numbers against already-known deterministic archived data
(Law #9 theater).

Each candidate below carries the full six-element worth-it gate.

---

## H13 (HDI-LOC): mechanistic locality of the logit-level self-report signal

1. **Exact question:** Does EXP112's logit-level self-report fidelity
   (41/60, HELD) concentrate in specific layers of base Pythia-410m when
   read via a zero-training logit lens at each layer's residual stream, on
   the same EXP107 decorrelated bench?
2. **Decision changed:** Pre-registered layer contrast
   mean(fidelity L16–L24) − mean(fidelity L0–L8): ≥ 0.10 with late-window
   fidelity ≥ 0.65 → CONTINUE the honesty-instrument program with a
   localization story; |contrast| < 0.05 → KILL the locality question
   (signal diffuse; the EXP112 HELD stands but loses its mechanistic
   foothold); in between → HELD.
3. **Cheapest test:** 60 items × 25 layers of cached forwards, logit-lens
   readout = argmax over the two entity first-token ids at each layer.
   $0 CPU, zero training, zero generation, same bench/pins/guards as
   EXP112 (G1–G4, BPE assertion, canonical order, tie-break E2, Δθ=0 via
   the LOG-331 pin).
4. **Mathematical license:** EXP112 HELD 41/60 with P(X ≥ 41 | 60, 0.5) =
   0.0031 — a real signal exists at the final layer; the logit lens is a
   standard zero-training per-layer readout; the layer contrast is a
   well-defined pre-registered statistic. The per-layer readouts are NEW
   data (never computed) — not Law-#9 theater.
5. **Quantitative prediction:** fidelity monotone non-decreasing over
   layers 12–24; late window ≥ 0.65; early window ≤ 0.55; contrast ≥ 0.10.
6. **Breaking point:** logit-lens BPE/token guards fail at any layer, or
   the profile is flat (|contrast| < 0.05) → locality KILLED; no rescue,
   no re-run.

**Summit filter:** a localizable self-report signal is a mechanistic
foothold toward self-consistent representation — the summit needs honest
internal readouts; a diffuse signal is far harder to build on. **PASS.**

---

## H14 (PTTSC-LOGIT): plan-conditioned logit-level decision

1. **Exact question:** On the EXP107 decorrelated bench, does prepending a
   T2-P2-generated plan (EXP113's cleared 60/60 protocol) to the
   executor's context change the zero-generation logit-level decision
   (EXP112's apparatus) relative to the no-plan baseline logit decision?
2. **Decision changed:** Paired McNemar on n_valid ≤ 60: p ≤ 0.05 with
   b > c → CONTINUE (the plan-conditioned pipeline is licensed as an
   adaptive-loop component); net (b−c) ≤ 0 → KILL (plan conditioning
   moves nothing even at the logit level); net > 0, p > 0.05 → HELD.
   Elicitation gates before any metric: Phase-0 and full-run
   n_valid ≥ 48/60, else RUN-INVALID.
3. **Cheapest test:** Phase-0 (~20 forwards): (a) planner outputs parse
   under EXP113's pinned rule (already 60/60 cleared — near-zero risk);
   (b) the logit decision slot functions with a plan prefix —
   context-length and tokenization effects are the binding unknown;
   <8/10 valid → RUN-INVALID.
4. **Mathematical license:** EXP112 HELD (41/60 baseline fidelity — the
   decision channel works); EXP113 apparatus CONTINUE (T2-P2 outlines
   60/60 parseable — the planner channel works). The composition is the
   untested question. This is H11's question with the dead generation
   channel replaced by the proven logit channel — H11 was RUN-INVALID
   (apparatus failure), never killed as a hypothesis.
5. **Quantitative prediction:** Honestly, no directional effect size is
   licensed; the test is for any detectable paired difference, with bars
   as above and a HELD zone against razor-thin CONTINUEs.
6. **Breaking point:** the Phase-0b-equivalent fires (logit slot
   degenerate with a plan prefix), or full-run n_valid < 48/60 →
   RUN-INVALID. A KILL retires plan-conditioning on this bench only.

**Honest fence (binds the future pre-reg):** the plan prefix is a token
asymmetry — greedy has no sampling variation, so the comparison is
pipeline-vs-baseline, not planning-vs-compute; a CONTINUE licenses the
pipeline as a component, never planning capability attribution.

**Summit filter:** adaptive plan→decision loops are the summit's
mechanism class. **PASS.**

---

## H15 (LFH-GEN2): generality of EXP111's decodability signal on a second decorrelated bench

1. **Exact question:** Does EXP111's trained L2-logistic head signal
   (24/30, G=0.0000, layer 20) replicate on a newly constructed second
   template-decorrelated bench under the same discipline (EXP107's
   kill-test discipline)?
2. **Decision changed:** Replication with acc ≥ 0.70 on the new bench's
   30-item test split and per-cell G < 0.30 → EXP111's CONTINUE
   strengthened toward a general decodability claim; acc < 0.65 or
   G ≥ 0.30 → the original was bench-specific (CONTINUE downgraded, not
   killed — the bench-1 result stands).
3. **Cheapest test:** Construct the second bench (60 items, same
   four-cell decorrelation discipline, independent item authoring) and
   validate it passes the decorrelation checks. The bench-construction
   gate is itself the breaking point. Head fits (~30 L2-logistic fits on
   CPU) are $0; the pinned EXP111 protocol (seed 20260929, stratified
   split, no sweeps) is reused byte-verbatim.
4. **Mathematical license:** EXP111's 24/30 (one-sided p=0.00072,
   G=0.0000) — a real above-chance signal on bench 1; the
   decorrelated-bench discipline is a pinned, independently reviewed
   construction protocol.
5. **Quantitative prediction:** acc ≥ 0.70 on the new bench, per-cell
   G < 0.30.
6. **Breaking point:** the new bench cannot be constructed to pass the
   decorrelation discipline (template-detector signature in the bench
   itself) → the item dies at bench construction, before any head is
   trained. Re-using bench-1 items would be Law-#9 theater and is
   explicitly barred.

**Summit filter:** the program's single surviving positive result needs
generality to matter for the summit. **PASS.**

---

## Considered and rejected (gate failures, recorded so they stay dead)

- **S5 blind-spot closure (1–4.87% band):** fails "decision changed" —
  capability stays zero whether the band closes or not; boundary-map
  polish only. Not worth a lane.
- **EXP111 per-layer head replication on bench 1:** Law-#9 theater — the
  fits are deterministic on archived data with the metric already
  computed (descriptive-only §6). Barred.
- **Cross-model check of EXP112's HELD:** deprioritized, not closed —
  no second local checkpoint is pinned, and bench-generality (H15) is
  cheaper and more diagnostic. Revisit only after H15 resolves.

## Sprint verdict

Three licensed candidates: **H13 (HDI-LOC), H14 (PTTSC-LOGIT),
H15 (LFH-GEN2)** — each passes the six-element worth-it gate and the
summit filter. Recommended dispatch order: H13 first (cheapest, pure
readout of archived bench + cached forwards), then H14 (needs a
Phase-0), then H15 (bench construction is the long pole). Each requires
its own worth-it-gate lane → pre-registration → independent Law #14
review → fix-verification → CEO launch, per the single-lane fence.
