# ADVERSARIAL REVIEW — SCBI AMBITION SPRINT (LOG-250)

**Reviewer:** Adversarial Reviewer (standing) · **Date:** 2026-09-24 · **Status:** working review, not a signed artifact
**Mandate:** kill ideas before they cost a single GPU pass. Kills are first-class results.
**Standing law:** no hypothesis earns continuation by elegance, ambition, or sunk cost — only by surviving pre-registered falsification. Theory preservation is the most dangerous failure mode (RESEARCH_OPERATING_SYSTEM.md §1).

**Reading discharged:** AGENTS.md (14 Laws); `research/theory/CLLC_FORMALIZATION_2026-09-23.md` (LOG-247); `research/theory/P1_BOUND_DERIVATION_2026-09-24.md` (LOG-248); `research/analysis_plans/K2_ROUTING_BYPASS_PLAN_LOG223_REV4_2026-09-23.md` (+ §6 verdict table, §7 consequences); `research/innovation/SPRINT3_CANDIDATES_2026-09-23.md` (S3-1…S3-6, graveyard, ranking); `research/innovation/DIRECTION_DECISION_2026-09-23.md` (P1/P2 pivots, ordered action list); `research/analysis_plans/K3_PHASE0_HALT_REPORT_LOG238_2026-09-23.md`; CEO_DIARY.md (2026-09-24 health check). No signed artifact was edited. No numbers invented; every kill cites a recorded verdict.

---

## 1. THE CULL LIST — 16 tempting-but-doomed ideas, rejected at the door

Each entry: the idea as a theorist would pitch it, then the one-line kill with its citation. These are not strawmen — each is a real failure mode of ambitious programs.

**C1. "Wider static search"** — more cone angles, finer α grids, new offsets, different layers, multi-vector sums, per-head variants.
→ KILLED by EXP077 [FACT]: 0.0pp across cones at four angles, cone-vs-line, cone-vs-control, offset, and radial grid (ΔM=0, p=1.0 throughout). The causal family is dead; more variants are the small-experiment habit (DIRECTION_DECISION §1.6; Sprint-3 graveyard: "more static geometry" stays dead).

**C2. "Just fine-tune a little"** — LoRA/adapters/full fine-tune on the benchmark, keep everything else.
→ Violates frozen-backbone (Law #6) and the canonical objective θ_after = θ_before (MENTORSHIP_DIRECTIVE). That is a different research program, not SCBI.

**C3. "Procrustes 2.0"** — cross-vocabulary alignment with better regularization, more anchor pairs, a bigger fit.
→ KILLED and retracted [FACT]: the operator is mathematically unsound (rank-2 unembedding-space fit applied to full-rank hidden-state directions); ledger claims (+0.129) contradicted primary artifacts (−0.715/−0.697); reframed as raw cosine ~0.7 with zero causal transfer (adversarial audit 2026-09-23). Re-fitting a broken operator is theory preservation.

**C4. "QK-subspace targeting"** — steer into QK-visible directions "because the bridge is QK-visible, the failed direction wasn't."
→ KILLED by G1 weight audit [FACT] — the exact inversion of the premise: failed direction B_agg is unusually QK-visible (Ē_QK=0.390, above the random-unit-vector null 95th percentile); the working bridge is QK-unremarkable (Ē_QK=0.356, mid-null). The "Core Causal Null-Space Theorem" central sentence is false.

**C5. "The bridge, but smarter"** — whitened / per-layer-scaled / denoised normalize(E[target]−E[foil]), presented as a discovered mechanism.
→ Law #7 (LOG-197/LOG-204): the bridge is label-informed rescue control, demoted — not a mechanism control. Rebranding the normalization smuggles label leakage into a mechanism claim.

**C6. "Tilt 2.0"** — accumulate persistent readout tilt across layers or items; global tilt field.
→ KILLED by K1 [FACT]: 0 of 180 bridge directions reached the 0.9 target-row bar; EXP082 exonerated foil-suppression too (k_f = 0/60). The directional-tilt story is dead in both directions.

**C7. "Oracle loops"** — feed the correct answer's embedding back as the loop's signal; "the loop improves reasoning."
→ KILLED by EXP070 [FACT]: static/oracle loops +0pp. And it is label leakage (Law #7): the oracle signal carries the answer; any "gain" is the label, not the loop.

**C8. "Curvature from the ray"** — fit off-ray curvature from the S3-9 1-D α grid; "the grid is dense enough to bound curvature."
→ KILLED by the LOG-248 impossibility result [THEOREM-grade in-house proof]: adversarial bump construction — exact ray-match to all orders with arbitrarily large δ off-ray. A 1-D grid cannot identify off-ray curvature, period. Untestable conjecture; withdrawn from verdict eligibility by the CEO.

**C9. "Autonomous unsupervised steering"** — cluster activations, steer along cluster centroids, claim self-consistent basis invention.
→ Re-skin of a killed family: EXP077's 0.0pp verdict attaches to the *injection family*, not the derivation method. A cleverer derivation does not survive a dead causal channel. (Also: the selection rule is externally specified → LOG-247 classification applies.)

**C10. "Paid-API verifier in the loop"** — GPT-4/Claude as the judge/verifier; "we'll pay for quality signal."
→ Instant reject: $0 standing law — no paid compute, no exceptions. Also an external-label dependency (Law #7 adjacent).

**C11. "Scale to 7B"** — re-run the static steering program on a 7B model; "scale will find what 410m missed."
→ Sprint-3 graveyard: 7B scaling stays dead — re-skin of the EXP077-killed family at a size the free tier cannot serve. No budget, no license.

**C12. "Test-set-fitted directions"** — fit the steering vector on the evaluation items' labels; report rescue on the same items.
→ Label leakage, Law #7. No held-out, no claim. (This is the shape of error the Law #7 audit exists to catch.)

**C13. "Inter-instance latent exchange"** — instances share latents mid-pass; pitched as a novel autonomous mechanism.
→ The exact sentence was explicitly retracted in the REV synthesis (Law #14 re-review, all 12 fixes applied). Novelty inflation beyond the program's N1 (Known Combination) verdict; any novelty claim needs a fresh prior-art audit first (Law #10).

**C14. "CoT / Self-Refine wrapper = new capability"** — wrap the frozen model in chain-of-thought or self-critique loops and claim "the model now reasons / is more capable."
→ Silent level crossing: "improves inference" (L1) ≠ "changes computational strategy" (L2) ≠ "creates new capability" (L3). The frontier scoreboard already lists Self-Refine, ToT-family, ∇-Reasoner as *competitor* systems with capability entries; SCBI has zero. A wrapper result without forced baselines per Operating System §1 licenses no capability claim.

**C15. "Gradient steering as autonomous discovery"** — PPLM-style gradient-guided generation, pitched as the model "discovering" representations.
→ LOG-247 correction: any mechanism with an externally specified direction/reference is "inference-time activation control," NOT autonomous cognition. (PPLM is additionally a logged missing prior — the novelty was never available.)

**C16. "Re-run K2 / EXP080 / EXP081 / K3 with tweaked bars"** — same design, adjusted thresholds, no new experiment number.
→ Law #4: a design change takes a new experiment number, never a silent edit to a signed protocol. Re-running a signed battery with moved bars is significance-shopping with extra steps (cf. the LOG-226 STOP / LOG-228 interval-identity ruling).

**Cull-list size: 16.** None of these may enter the queue without a new falsifying test that the cited kill does not already cover — i.e., effectively never, unless the kill's own premises are overturned by new evidence under a new LOG.

---

## 2. SURVIVAL CRITERIA — the checklist to reach QUEUED

A candidate reaches QUEUED only if **all** of the following hold. One failure = returned to the backlog with the failing criterion named. This is the worth-it gate (Law #15) made mechanical.

1. **Frozen-backbone compatible.** Δθ = 0 structurally — no weight, adapter, bias, or running-norm updates. The Δθ=0 verification method (e.g., state_dict hash pre/post, guard-G3 style) is named in the proposal, not deferred.
2. **Not a re-skin of a killed family.** The proposal names the killed families — static direction injection (EXP077), QK-subspace targeting (G1), Procrustes alignment (retracted), label-informed bridge-as-mechanism (Law #7), persistent readout tilt (K1), static/oracle loops (EXP070), test-set-fitted directions (Law #7) — and states its delta from each *in writing*. "Different derivation, same causal family" fails this criterion (C9 precedent).
3. **A falsifying test exists.** Pre-registered kill/continue criteria with exact bars, a five-category verdict table (Supported / Not supported / Inconclusive / Underdetermined / Refuted — the only permitted verdicts), exact pass count, and T4-hours at the program-measured rate. "Interesting/promising/elegant" appears nowhere near a verdict.
4. **Mathematical license with a quantitative breaking point.** A named authorizing result with epistemic grade ([THEOREM] / [PROPOSITION] / IN-HOUSE-PROOF), an endpoint prediction with magnitude anchored to archived measurements (never invented), and a breaking point that kills the *theory* — not just the experiment — if the data cross it. Heuristic bounds are labeled heuristic (P1 precedent).
5. **Label-free arms (Law #7 audit).** Any label-informed construction is scoped explicitly as rescue/positive control, never as mechanism evidence; a G2-style provenance cross-check (construction source link + per-item mapping log) is named. If the candidate cannot state where its labels touch the design, it fails.
6. **No silent level-crossing.** The evidentiary level is declared up front — L1 (improves inference on a fixed task), L2 (changes computational strategy), L3 (new capability) — with the endpoint that licenses each. Capability language requires forced baselines per Operating System §1; decision-rescue on a fixed benchmark is L1 at best.
7. **$0.** Free-tier only (Kaggle/Colab T4). Pass budget stated exactly; total program queue stays within the free quota (QUOTA_LEDGER). No paid APIs, no paid compute, no credential or account changes — any of these is instant reject, no appeal.
8. **No autonomy claim with an externally specified direction.** Per the LOG-247 correction: externally specified direction/reference → classified "inference-time activation control," never "autonomous cognition." Re-entry to any cognition-level claim requires a later experiment that removes the externally specified direction — named, not hand-waved.
9. **No off-ray claims from ray measurements.** Per LOG-248: any curvature/extrapolation claim beyond measured points requires a pre-registered covering argument over the relevant space (not a nominal-point measurement wearing the bound's clothes). 1-D-grid conjectures about unmeasured regions are inadmissible as verdict-bearing.
10. **Novelty ≤ N1 unless audited.** The program's synthesis novelty is N1 (Known Combination). Any claim above N1 requires a fresh prior-art audit attached (Law #10); control-family proposals check the Activation-LQR boundary explicitly (CLLC §6 precedent: "feedback over activation steering" was never available as novelty).
11. **Pre-registration + Law #14 SIGN before GPU, CEO GPU clearance after.** Law #15 four answers present and honest: (1) precise question, (2) the decision it changes (KILL/CONTINUE/PIVOT named), (3) the cheapest test, (4) the mathematical license. No GPU without SIGN. Design changes take new numbers (Law #4).
12. **Not duplicating the queue.** Check against: K2, CLLC pivot battery, K3 Phase-1, EXP080/081, curvature diagnostic, Sprint-3 pilots (S3-1…S3-6 Stage 0/1). Duplicates are merged or returned.

---

## 3. STRESS-TESTS OF OUR OWN LIVE BETS

### (a) CLLC's narrowed novelty — the kill-shot

**The narrowed claim** [FACT, CLLC §6–§8]: not "feedback over activation steering" (Activation-LQR, Apr 2026, is closed-loop feedback control of frozen activations with layer-wise Jacobians and online state feedback — verified prior art), but a *cheap, Jacobian-free, partially-observed, low-rank feedback controller competitive with existing closed-loop controllers at matched or lower information/compute*. The novelty-earning contrasts are (C)-vs-(B2) and (C)-vs-(D) in EXP-CLLC-01.

**Single sharpest kill-shot:** arm **(B2) ≥ arm (C)** in EXP-CLLC-01 — adaptive open-loop (per-instance α from a pre-pass margin probe, two passes, no feedback law) captures all of the gain. Then the entire feedback apparatus is dead weight, and the pre-registered consequence fires: **KILL feedback machinery — CONTINUE adaptivity as open-loop** (CLLC §8). This is the most likely killer because the frozen pass is deterministic (F2): within-trajectory feedback needs nonlinearity (channel A), but per-instance adaptivity (channel B) needs no feedback law at all, and the steelman (§10.1) already concedes B2 is strictly simpler and cheaper than CLLC.

A second, faster kill-shot needs no GPU: a literature/object-level demonstration that the Jacobian-free economy is vacuous — e.g., that Jacobian-vector products on this architecture cost ≪ one forward pass, so "no JVPs" is not an information/compute advantage anyone would pay for. That collapses the narrowed delta to N0-redundant without running the battery.

**Guarded? Partially.** The (B2)-first ordering is guarded by design — B2 is the designated first kill, and the (C)>(B)-but-(C)≤(B2) cell is pre-registered as KILL. **The gap:** the (C)>(B2)-but-(C)<(D) cell says "CONTINUE as efficiency result *only if* (C) uses strictly less information/compute than (D)" — but "strictly less" is **not operationalized** (no pass/FLOP/JVP-count bar). The one cell that could keep CLLC alive as an efficiency contribution has no quantitative licensing rule, so a between-the-arms outcome would be decided by reviewer discretion — exactly the shape of judgment the pre-registration discipline exists to remove. **Recommended guard:** before EXP-CLLC-01 is signed, operationalize "strictly less" (e.g., total forward-pass-equivalents including JVP costs, counted by the executor) and pre-register the threshold. Also note the inherited scope guard that *is* in place: CLLC's direction v̂ is label-informed, so any success is classified "inference-time activation control," never autonomous cognition (§8) — the Law #7 demotion is inherited, not laundered.

### (b) The K2 P2 pivot branch — the stranding pattern

**The branch** [FACT, DIRECTION_DECISION + K2 §2/§7]: row 2/2r (final-position-local Supported) → P2 pivot fires → output-side mechanism program closes ("the bridge is logit steering, period") → mechanism-family pivots to trajectory/closed-loop controllers → CLLC battery deploys. Row 1 (routing Supported) → upstream attention-engagement hunt licensed.

**The stranding pattern:** **verdict-table row 4 — both restricted arms flat (b=0) with the (c) all-positions control passing G5.** Neither Supported cell can fire (row 2 needs b_a ≥ 6; row 1 needs b_b ≥ 6); the narrow routing-Refuted cell (2r) needs cell-2's pattern and doesn't fire either. Consequence as written: "The bridge does not survive position restriction at all — the license's application premise broke (L3), not either proposition. Logged; K2's question is unaskable in this form."

Under row 4: P2 **cannot** fire (no row 2), the upstream hunt **cannot** be licensed (no row 1), and the rescue is real but provably unlocalizable by position masking. The program's two licensed futures both die in one row.

**Guarded? Barely — this is the most dangerous gap in the live queue.** The cell is priced (it won't fake a verdict — that part is guarded), but its consequence names **no licensed next instrument and no decision rule for what comes after**. The generic Inconclusive remedy — "instrumentation upgrade + powered re-registration" — does not apply: re-registering at N≥100 re-asks a question whose *application premise broke* (L3), and more N cannot fix a broken premise; the named instrument (per-layer attention snapshots, S3-7 spec) presumes position-restriction is informative, which row 4 just falsified. Without a pre-registered rule, the program would sit in HOLD burning CPU theory while the GPU lanes wait — the CEO's own 2026-09-24 warning ("sophistication can become a waiting-room drug") made concrete. **Recommended guard:** pre-register now, before K2 executes, that row 4 → the position-masking attribution approach is **stood down, not re-registered** (Law #8: the negative result is retained as the finding), and the program re-scopes to whole-trajectory instruments that do not need position attribution (CLLC-style closed-loop control, which actuates the full residual stream and never asks the routing question). Note the surviving consolation, which *is* guarded: Sprint-3 verifiers (S3-1 ARP, S3-4 SAH, S3-3 DUG) retain the bridge as a causal-but-unlocalizable positive class — their $0 Stage-0 gates do not need K2's attribution answer.

(A secondary strand, also real: G10 exclusions >6 → Underdetermined via entity-mapping failures rather than verdict — the question dies by tokenizer logistics, not science. Guarded by the pre-registered floor, but worth watching: if exclusions cluster, the bench construction, not the hypothesis, is at fault.)

### (c) The curvature diagnostic — when 150 passes are wasted

**What it is** [FACT, P1_BOUND_DERIVATION §6]: randomized power iteration on ∇²D via central finite differences (~45–75 passes) + ~60 calibration passes for Mahalanobis whiteners (no activation archives exist per LOG-243, so live) ≈ **150 passes ≈ 0.002 T4-h**, GPU-gated, queued behind K2. Its job: instantiate κ̂ so P1's conditional bound δ ≤ κ̂R² becomes an operational breaking point for the CLLC (C)-arm.

**It is a waste of 150 passes in all three of these cases:**

1. **κ̂ comes back huge.** The derivation's own §7 flags it: "Attention softmax can have enormous curvature; if measured κ̂ is huge the bound is vacuous." Then δ ≤ κ̂R² licenses nothing, the breaking point is unusable, and P1 stays conditional — 150 passes bought a vacuous inequality.
2. **κ̂ comes back small or moderate — measured at the nominal point.** Power iteration estimates the top eigenvalue *at the nominal point*; the bound needs sup-κ over the injection schedule space (~24-D for Pythia-410m). Per LOG-248's adversarial bump, no nominal-point (or ray) measurement bounds off-ray curvature. Without a pre-registered covering argument, κ̂ is [CONJECTURE]-grade (the doc's own grading) and the "instantiated bound" **cannot bear a verdict** — it would launder a conjecture into a cited number in future Law #14 reviews.
3. **S3-9 returns nonlinear (CV_α[g] > 20%).** Then P1's near-ray-linearity premise fails, channel (A) is live by a different route, and the bound is not the gating instrument — the diagnostic answers a dead question.

**The one case it earns its passes:** S3-9 near-linear AND κ̂ moderate AND a pre-registered covering rule (multi-point max over the schedule space with an explicit spike criterion, not a point estimate).

**Guarded? No — this is currently unguarded.** The caveats are written in the derivation doc, but there is **no pre-registered decision rule on κ̂** (no vacuity/abort threshold, no covering protocol, no Law #14 pre-registration of the diagnostic itself) — yet it sits in the queue "priced" as if it will instantiate the bound. Spending GPU on a measurement whose verdict-bearing interpretation is still [CONJECTURE]-grade violates the worth-it gate ("no license, no work"). **Recommended guard:** no GPU for the diagnostic until it has its own pre-registered interpretation rule — abort/vacuity thresholds on κ̂, the covering protocol over schedule space, and the S3-9-near-linearity precondition — reviewed under Law #14. Until then it is a queued *proposal*, not a queued *measurement*.

---

## 4. PRE-COMMIT — Law #14 traps for any surviving candidate

When (if) a candidate survives to registration, the independent Law #14 reviewer must check these traps. Each is a named failure mode from this program's own history.

- **T1 — Label leakage (Law #7).** Trace every label/test-target from source to endpoint. Is any label reachable by the candidate generator, the selector, or the evaluator? Label-informed constructions are scoped as rescue/positive controls only. (Precedent: the LOG-204 bridge demotion.)
- **T2 — The cheap comparator.** Is the B2-equivalent present as the *first* kill — adaptive open-loop, random selection, permuted control? Any "win" against only a weak or fixed baseline is overclaiming. (Precedent: CLLC §8 (C)-vs-(B2).)
- **T3 — Budget matching.** Compute, information, and intervention budgets equalized across arms (post-hoc rescaling reported alongside raw); residual asymmetries reported explicitly, never hidden. (Precedent: EXP-CLLC-01 budget matching; (E) permuted-probe control.)
- **T4 — Evidentiary level.** L1/L2/L3 declared with the licensing endpoint; capability language flagged and held to forced baselines. No silent crossing. (Precedent: frontier scoreboard — zero SCBI capability entries.)
- **T5 — Autonomy language.** Externally specified direction/reference → "inference-time activation control" only. (Precedent: LOG-247 correction.)
- **T6 — Ray-to-off-ray.** Any claim about unmeasured regions from 1-D grids or nominal-point measurements → reject as verdict-bearing; admissible only as labeled conjecture. (Precedent: LOG-248 impossibility.)
- **T7 — Bar identity.** Flatness bars one-sided, direction stated in writing, interval family named, bite table recomputed from the named implementation *and* independently reproduced. (Precedent: LOG-226 STOP / LOG-228 ruling; TRACK7_REVIEW_CHECKLIST lint.)
- **T8 — Novelty.** N1 cap; fresh prior-art audit attached for anything above; control-family proposals check the Activation-LQR boundary. (Precedent: CLLC §6 correction.)
- **T9 — Verdict exhaustiveness.** Every observation cell mapped to exactly one of the five permitted verdicts with a pre-registered consequence; Inconclusive priced and HELD, never culled; Underdetermined distinct from negative. No cell defers to executor discretion. (Precedent: K2 §6.)
- **T10 — The worth-it gate.** Law #15 four answers present and honest; the cheapest test is actually cheapest; the mathematical license carries a theory-killing breaking point. No GPU without Law #14 SIGN + CEO clearance. (Precedent: RESEARCH_OPERATING_SYSTEM §1.)
- **T11 — No silent shifts, no duplicates.** Design changes take new numbers (Law #4); queue checked against K2 / CLLC / K3 Phase-1 / EXP080/081 / curvature diagnostic / Sprint-3 pilots. (Precedent: C16.)
- **T12 — Frozen backbone + reproducibility.** Δθ=0 verification named (hash pre/post); seeds pinned; manifests logged. (Precedent: K2 guards G3/G4.)

**Reviewer's oath for this sprint:** the sharpest service I can render the program is a kill delivered *before* the queue, not after the GPU bill. Every candidate above that dies here died for free.

---

*End of adversarial review LOG-250. No signed artifacts edited. No GPU spent. 16 ideas killed at $0.*
