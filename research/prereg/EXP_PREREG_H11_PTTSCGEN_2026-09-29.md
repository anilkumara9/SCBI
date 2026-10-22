# Pre-registration: H11 — PTTSC-GEN (Planner/Executor, Generation-Channel Revival)

**Status:** DRAFT pre-registration. Licenses nothing. No model runs, no experiment number minted, no signed protocol touched, no GPU contact, no commits, no pushes. $0 CPU.
**Drafting lane:** LOG-4606 (pre-assigned). **Source:** the H7-CONTINUE registered consequence ("H4-revival lanes are licensable as NEW hypotheses, each naming its clearing protocol and each carrying its own elicitation-failure gate" — EXP113 report §"Registered verdict"), restated in EXP109's run report §5 ("a future planner-executor test would be a separate pre-registered lane with a re-derived elicitation design"). This lane is the H4-axis planner/executor revival — a NEW hypothesis, not a revival of H4.
**Launch chain:** independent Law #14 review of this exact file → fix-verification (if fixes required) → CEO launch decision → execution under a minted experiment number. This lane stops at the draft.

**Governing laws:** Law #4 (no post-hoc hypothesis shifts — the bars below are binding), Law #6 (frozen backbone Δθ=0), Law #7 (zero data leakage — no bench labels touch the apparatus; the planner exemplars are format demonstrations, not labels), Law #9 (metrics registered before any output is inspected), Law #13 (deterministic reproducibility — seeds, hashes, environment manifest pinned below).

**Epistemological labels** per `SCBI/AGENTS.md` §5: [OBSERVATION], [HYPOTHESIS], [INTERPRETATION], [PROPOSITION], [ASSUMPTION], [FACT].

---

## 0. Worth-it gate (the 6 elements, recorded before drafting)

**[HYPOTHESIS under test]** H11 (PTTSC-GEN): the plan-conditioned generation pipeline — T2-P2-elicited numbered outlines (the EXP113-cleared planner protocol), each outline developed into a final entity-name answer by the frozen executor (greedy priming slot), majority vote — beats the unconditioned greedy baseline (same answer slot, no outline) on decision accuracy over the 60-item EXP091 bench, paired per item.

1. **Exact question:** At fixed greedy decoding on the 60-item EXP091 bench, does the plan-conditioned pipeline (T2-P2 planner → per-outline entity-name developments → majority vote) achieve higher decision accuracy than the unconditioned baseline (identical answer slot, no outline), paired per item, licensed by the one-sided McNemar exact test?
2. **Decision changed:**
   - **CONTINUE** (McNemar one-sided p ≤ 0.05, b > c): the plan-conditioned pipeline adds measurable decision accuracy at this scale/bench — the planner-executor pattern enters the EXP068-family adaptive-loop designs as a registered component (later lanes only).
   - **KILL** (net b−c ≤ 0): plan-conditioning adds nothing on this bench/apparatus — the coordinator axis is retired for the piloted scope.
   - **HELD** (net > 0, p > 0.05): indeterminate gain; licenses nothing, retires nothing, no re-runs.
   - **RUN-INVALID:** any Phase-0 gate or the elicitation gate fires — the apparatus failed; the hypothesis gets no verdict.
3. **Cheapest test:** Phase 0 answers the two binding unknowns for ~20 generations (~15–30 min $0 CPU) before the full run is licensed: (0a) the planner-recitation check — T2-P2's 60/60 EXP113 clearance was mechanical-parse only, and verbatim exemplar recitation would pass that parse rule (the EXP115 pathology applied to outlines); (0b) the decision-channel mini-gate — the entity-name generation slot has failed 3/3 prior attempts (EXP109 sampled 80/80 unparseable; EXP115 greedy few-shot 38/60 recitation; EXP116 greedy priming 37/60 tail echo), and no validated generation decision channel exists. No cheaper test answers the planning question: EXP109's apparatus is dead (n_valid=0), EXP113 tested elicitation not planning, and the two Phase-0 unknowns are each independently worth answering as boundary findings.
4. **Mathematical license:** paired one-sided McNemar exact on the discordant pairs (b, c); minimum practical CONTINUE configuration (5,0) → p = 0.03125 (verified at drafting, §4). The test is powered for decision-grade effects (≥5 net flips with clean discordance), not fine-grained gains — disclosed, mirroring H8's statistical-honesty note.
5. **Quantitative prediction:** Phase 0a — if T2-P2 elicits genuine outlines, expect <6/10 probe items with ≥2 verbatim-recited outlines (recitation rate unknown; this is the test). Phase 0b — the entity-name priming slot is untested on EXP091 (priors: 0–63% parseable on other benches/prompts); expect ≥8/10 parseable with variation if the slot is a working decision channel, else the gate fires → RUN-INVALID (itself a boundary finding: no generation decision channel on the program's standard bench). Full run, conditional on Phase 0: if plan-conditioning adds a decision-grade effect, expect McNemar (b,c) with b−c ≥ +5 clean → CONTINUE; if it adds nothing, expect net ≈ 0 → KILL.
6. **Breaking point:** Phase 0a (≥6/10 recited → RUN-INVALID — the T2-P2 clearance was format-recitation, and the planner is not planning); Phase 0b (<8/10 parseable or degenerate variation → RUN-INVALID — the decision channel does not exist on this bench/shape); the 48/60 elicitation gate; the McNemar bars. The design is refused (REJECT, a legitimate review outcome) if the pipeline-vs-baseline comparison is judged too confounded to license, or if the recitation/decision-channel risks are judged unmanageable — both are fair Law #14 grounds.

**The key challenge — is H11's question different from dead H4/EXP109 and from EXP113 itself?** [PROPOSITION]

[OBSERVATION] EXP109 (H4/PTTSC) ended **RUN-INVALID**: n_valid = 0/20 — the verbatim T2-P1 planner degenerated into a repetition attractor (18/20 items) and the sampled entity-name baseline was 80/80 unparseable. The *apparatus* failed; the planning hypothesis was never tested (EXP109 report §5: "not a verdict about planning"). [OBSERVATION] EXP113 (H7/EVALID) ended **CONTINUE**: T2-P2 (few-shot) cleared 60/60 parseable numbered outlines on this exact bench — but parseability is format, not planning; EXP113 tested elicitation, not decisions.

H11 asks the question EXP109 posed but could not test — does plan-conditioning improve decisions? — with a *different apparatus on both arms*: the planner uses the EXP113-cleared T2-P2 protocol (imported byte-verbatim, §3.3) instead of the dead T2-P1; the executor/baseline use greedy decoding with a priming answer slot (all EXP113 clearances were greedy; EXP109's sampled baseline failed 80/80) instead of H4's sampled regime. This is not a re-run (re-runs are barred): it is the separately pre-registered lane with re-derived elicitation design that EXP109's report §5 and EXP113's CONTINUE consequence explicitly license. The two highest-risk adaptations — (i) whether T2-P2's outlines are genuine plans or exemplar recitation, (ii) whether any entity-name generation slot works as a decision channel on this bench — are each front-loaded into cheap Phase-0 gates rather than assumed. If either fails, the run is RUN-INVALID before any metric exists.

**Gate verdict: PASS.** The planning question is open (EXP109 tested nothing), the license is explicit (EXP113's CONTINUE consequence), the test is cheap ($0 CPU, Phase 0 in ~15–30 min), and the breaking points are registered in advance.

---

## 1. Hypothesis (one falsifiable sentence)

**[HYPOTHESIS]** On the 60-item EXP091 bench, the plan-conditioned pipeline (frozen planner writes outlines in one pass via the T2-P2 few-shot protocol; frozen executor develops each outline into an entity-name answer under greedy decoding; majority vote) beats the unconditioned baseline (same greedy answer slot, no outline) on decision accuracy — paired one-sided McNemar exact p ≤ 0.05.

**Falsifiers:** net (b−c) ≤ 0 on the paired valid items → the coordinator axis is retired for this scope; Phase-0 gate failures → RUN-INVALID (apparatus, not a verdict).

### 1.1 How H11 differs from H4/EXP109 and from EXP113 [FACT]

[OBSERVATION] H4's pre-registration (LOG-4547; Law #14 SIGN-WITH-FIXES → SIGN) specified: verbatim T2-P1 planner (greedy, 160 tokens), temperature=0.7/top_p=0.9 executor and baseline with entity-name answers, 4 independent baseline samples, matched executor budget, n=20 pilot. [OBSERVATION] EXP109 executed it exactly and went RUN-INVALID (n_valid=0): the planner fell into the "Write a list of the possible answers" repetition attractor on 18/20 items, and the sampled baseline was 80/80 unparseable.

H11 is a **new hypothesis**, not H4 revived: the planner protocol (T2-P2 few-shot, the EXP113 clearance), the decoding regime (greedy throughout — every EXP113 clearance was greedy), the answer slot (priming tail, adapted from T1-P5's mechanism), the baseline (single greedy generation — greedy has no sampling variation to match), the budget framing (pipeline-vs-baseline with disclosed compute asymmetry, not H4's matched-budget planning-premium test), and the item set (n=60 full bench, not the n=20 pilot) are all different. What carries over: the scientific question (does plan-conditioning improve decisions?), the outline-extraction rule, the parse rule, the vote rule with foil tie-break, and the elicitation-gate discipline.

[OBSERVATION] EXP113 validated *elicitation* (≥80% parseable formats), not planning and not decisions. H11 does not re-test elicitation as an end in itself — Phase 0 checks the two construct prerequisites (planner genuinely planning; answer slot genuinely deciding), and the full run tests the decision question EXP113 never asked.

---

## 2. Exact question and the decision it changes

**Exact question [HYPOTHESIS]:** At fixed greedy decoding on the 60-item EXP091 bench, does the plan-conditioned pipeline (T2-P2-elicited outlines → per-outline entity-name developments → majority vote) achieve higher decision accuracy than the unconditioned baseline (identical answer slot, no outline)?

**Decision changed:**
- **CONTINUE** (§4): McNemar one-sided p ≤ 0.05 with b > c → the planner-executor pattern enters the EXP068-family adaptive-loop designs as a registered component (later, separately pre-registered lanes only).
- **KILL** (§4): net (b−c) ≤ 0 → plan-conditioning adds nothing on this bench/apparatus; the coordinator axis is retired for the piloted scope (a different apparatus remains a separate, unlicensed lane).
- **HELD** (§4): net > 0 but p > 0.05 → indeterminate; licenses nothing, retires nothing, no re-runs.
- **RUN-INVALID:** any Phase-0 gate (§3.7) or the elicitation gate (§3.8) fires, or backbone/provenance pins mismatch → the apparatus failed; the hypothesis gets no verdict. Not evidence about planning.

**Primary metric (registered before any run):** Δ = acc(pipeline-majority) − acc(baseline) on n_valid paired items (n_valid ≤ 60), verdict licensed by the one-sided McNemar exact test on (b, c) where b = pipeline-right/baseline-wrong, c = pipeline-wrong/baseline-right.

---

## 3. Method

### 3.1 Frozen backbone, bench, environment [FACT / pinned]

- **Backbone:** frozen Pythia-410m snapshot `~/workspace/.exp086_weights/pythia-410m`. `device_map="cpu"` (requires accelerate==1.15.0 per EXP113's honest note 1), float32, `model.eval()` before all generation, `torch.no_grad()` around ALL generations.
- **Δθ=0 procedure (pinned):** SHA-256 over tensor bytes with sorted `state_dict` keys, float32 (the EXP077/EXP084/EXP108 canonical convention). Asserted **before the first generation and after the last**; any mismatch → RUN-INVALID, quarantine, no metric read. Expected pin: `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed` (LOG-331).
- **Bench:** the 60-item EXP091 bench, rebuilt verbatim via `experiments/runs/EXP089_clm8b_falsifier/benchmark_exp089.py: build_benchmark()` — the identical builder H7 used, so T2-P2 is validated on exactly this bench. Provenance: SHA-256 of `experiments/runs/EXP077_cone_vs_line/exp077_instance_records.json` = `47281cd3dc243369be0aa5be2345663b752cdb4a329a16a37f08da5717230585` asserted before any generation; `len(bench) == 60` asserted. Mismatch → RUN-INVALID. [OBSERVATION — verified from the builder source] The bench's option order alternates (`target_first = (i % 2 == 1)`); the target entity is always the bench's "A"-keyed entity, the foil the "C"-keyed entity; the 60 triples are distinct, so a content-following decision channel must show variation.
- **Environment (Law #13):** torch==2.14.0+cpu, transformers==5.17.0, numpy==2.5.3, accelerate==1.15.0; `torch.manual_seed(0)` + numpy seed 0; CPU threads set and read back via `torch.get_num_threads()`; greedy decoding (`do_sample=False`) everywhere; nothing left to tune. All recorded in the execution worksheet.
- **Law #7:** bench ground-truth labels (the "A"-keyed target entity) are used **only at metric time** — never during generation, never during any selection choice. The T2-P2 planner exemplars are format demonstrations (outlines whose correctness is irrelevant); they carry no labels.

### 3.2 Item set [PROPOSITION]

All 60 items in bench build order (indices 0–59). No subsampling, no pilot phase beyond the pinned Phase-0 probe items (which are regenerated fresh in the full run — Phase-0 records are diagnostics, never metric inputs).

### 3.3 Planner spec — T2-P2 imported byte-verbatim from H7 [FACT]

The planner prompt for target item t is constructed **byte-exactly** per H7 §3.3 T2-P2 and EXP113's honest note 3:

- `TAIL` = `Plan: Before answering, write 4 distinct numbered solution outlines (1. 2. 3. 4.), each a different approach to answering the question. Each outline must be 40 words or fewer. Do not give the final answer yet.`
- `OUTLINES` (pinned verbatim, both exemplars — format demonstrations; correctness irrelevant):
  ```
  1. Restate the question's ordering constraint in my own words.
  2. Check each premise statement against the two candidate entities.
  3. Eliminate the entity contradicted by any premise.
  4. Name the remaining entity as the answer.
  ```
- `block(i)` = `{PROMPT_i}` + `"\n\n"` + `TAIL` + `"\n"` + `OUTLINES`, for exemplar items i ∈ {3, 4} (bench build order, pinned).
- `prompt(t)` = `block(3)` + `"\n\n"` + `block(4)` + `"\n\n"` + `{PROMPT_t}` + `"\n\n"` + `TAIL`.
- `{PROMPT}` = the item's full bench prompt verbatim (premise + question + option list), unchanged.

**Byte-identity check (Law #13):** the execution lane asserts the 60 constructed planner prompts are byte-identical to EXP113's T2-P2 prompts for the same target items (reference: `experiments/runs/EXP113_evalid/out/exp113_raw.json`); any mismatch → RUN-INVALID (apparatus bug).

**Generation spec (pinned):** greedy (`do_sample=False`), `max_new_tokens=160`. One planner generation per item.

**Outline extraction (pinned — H4 §3.3 verbatim):** scan the planner output left to right; record the first occurrence position of each literal marker `1.`, `2.`, `3.`, `4.`; for k=1..4, outline_k = the substring from the end of marker `k.` to the start of the next marker occurrence in position order (or end of output), stripped; text before the first marker (preamble) discarded; a missing marker yields an empty outline; drop empties and exact duplicates; **planner-valid iff ≥ 2 distinct non-empty outlines remain**.

### 3.4 Executor spec (pinned) [PROPOSITION]

For each extracted outline k (2–4 per the §3.3 rule), one executor generation with the pinned template (byte-exact):

```
{PROMPT}

Outline {k}: {OUTLINE_TEXT}

Develop the outline above into a final answer. Reply with the name of the higher-ranked entity and nothing else.

The higher-ranked entity is:
```

**Generation spec (pinned):** greedy (`do_sample=False`), `max_new_tokens=16`. (Entity names are 1–3 tokens; the short cap limits echo/tail-runaway risk — the EXP115/116 lesson. This is adaptation §8.5.)

### 3.5 Baseline spec (pinned) [PROPOSITION]

One baseline generation per item with the pinned template (byte-exact) — the identical answer slot as §3.4, minus the outline:

```
{PROMPT}

Reply with the name of the higher-ranked entity and nothing else.

The higher-ranked entity is:
```

**Generation spec (pinned):** greedy (`do_sample=False`), `max_new_tokens=16`. (Single generation: greedy decoding has no sampling variation, so H4's 4-sample baseline degenerates to 4 identical copies — adaptation §8.4.)

### 3.6 Parse rule and vote rule (pinned — H4/EXP109 verbatim) [FACT]

- **Parse rule:** decode the newly generated tokens only (prompt tokens excluded — the EXP108 convention); strip whitespace and trailing punctuation (`.,;:!?`); case-insensitive compare against the item's two bench entity names (bench keys "A" and "C"): exact match → that entity is the vote; otherwise the generation is **UNPARSEABLE** and its vote is dropped.
- **Vote rule:** per item, the pipeline arm's decision = majority of its parseable executor votes; ties (any even split) broken deterministically toward the **foil entity** (bench "C" key — conservative, the H1/H4 precedent). The baseline arm's decision = its single generation's parsed entity.
- **Accuracy:** per arm per item, correct iff the arm's decision equals the bench's "A"-keyed target entity.

### 3.7 Phase-0 gates (pinned — the EXP115/116 lesson; both fire before any metric) [PROPOSITION]

Phase 0 runs on the pinned probe set **{0, 1, 2, 5, 6, 7, 8, 9, 10, 11}** (10 items; items 3–4 excluded because they are the planner's exemplars — the recitation probe would be confounded on them). All Phase-0 generations use the pinned §3.3–§3.5 specs.

- **Phase 0a — planner recitation check:** run the §3.3 planner on the 10 probe items; extract outlines per §3.3. An outline **recites** iff it exactly equals (after strip + casefold) one of the 4 pinned exemplar `OUTLINES`. An item is **recited** iff ≥2 of its outlines recite. If **≥6/10 probe items are recited** → **RUN-INVALID** (the planner is reciting exemplars, not planning; T2-P2's clearance was format-recitation — construct failure). [Rationale: EXP115's pathology was verbatim exemplar recitation passing a mechanical parse rule; T2-P2's 60/60 EXP113 clearance was mechanical-parse only and never checked for recitation. The exact-match criterion is conservative by design — paraphrase-recitation is reported as a diagnostic (mean max token-overlap vs exemplars) but does not fire the gate; this limitation is disclosed.]
- **Phase 0b — decision-channel mini-gate:** run the §3.5 baseline slot on the 10 probe items; parse per §3.6. Require **≥8/10 parseable** AND **≥2 distinct parsed entity names with minority ≥2** (variation guard — legitimate here: the 10 probe triples are distinct, so a content-following channel must vary; this is the G2-style guard from H9/H10, re-licensed for a varying-label bench). If either condition fails → **RUN-INVALID** (no generation decision channel exists on this bench/shape; the hypothesis cannot be tested).

Phase-0 records are diagnostics only and never enter the metric. If Phase 0 passes, the full run (§3.8) regenerates all 60 items fresh (greedy decoding is deterministic, so Phase-0 outputs are reproduced identically — no selection on partial data, Law #9).

### 3.8 Full run, item validity, and the elicitation gate [PROPOSITION]

If Phase 0 passes: 60 planner generations (§3.3) + up to 240 executor generations (§3.4) + 60 baseline generations (§3.5), all greedy, zero exceptions tolerated silently (per-generation exceptions caught, logged, scored UNPARSEABLE; >10% exceptions → RUN-INVALID, apparatus bug).

- **Item valid** iff planner-valid (§3.3: ≥2 distinct non-empty outlines) AND ≥2 executor votes parseable AND baseline parseable. n_valid = number of valid items (≤60).
- **Elicitation-failure gate:** n_valid < 48/60 (below the 80% EXP113 clearance threshold) → **RUN-INVALID**. Not a verdict.
- **Deterministic re-parse:** the parse script is a pinned pure function of the raw generation logs; run twice, assert byte-identical parse tables; mismatch → RUN-INVALID.

### 3.9 Budget definition (pinned — the H4 matched-budget framing is dropped) [PROPOSITION]

H4's matched executor budget (4 sampled developments vs 4 sampled baselines) is impossible at greedy decoding (no sampling variation). The comparison is therefore **pipeline-vs-baseline**, not planning-premium-at-matched-budget: the planner arm spends up to 160 + 4×16 = 224 tokens/item vs the baseline's 16 tokens/item. The token asymmetry is the treatment cost, and any gain cannot be attributed to planning specifically vs additional compute — this confound is **disclosed as a fence** (§7.1), not hand-waved. A compute-controlled follow-up (e.g., a sham-outline arm) would be a separate pre-registered lane, not part of this one.

### 3.10 What H11 reuses vs rebuilds [FACT]

Reuses byte-verbatim: the T2-P2 planner template (H7 §3.3), the outline-extraction rule (H4 §3.3), the parse rule (H4 §3.5/EXP109), the vote rule with foil tie-break (H4 §3.6), the bench + builder + provenance pin, the backbone pin procedure. Rebuilds (adaptations, all listed in §8): greedy regime, priming answer slot, single baseline generation, n=60, 48/60 gate, Phase-0 gates, pipeline-vs-baseline budget framing.

---

## 4. Decision bars with statistical license

All bars are on the paired valid-item set (n_valid ≤ 60). b = pipeline-right/baseline-wrong; c = pipeline-wrong/baseline-right. Verdict licensed by the **one-sided McNemar exact test**: p = P(X ≥ b | n = b+c, 0.5). Critical values verified at drafting:

| (b, c) | net | one-sided exact p |
|---|---|---|
| (5, 0) | +5 | 0.03125 ✓ CONTINUE |
| (4, 0) | +4 | 0.0625 ✗ HELD |
| (6, 0) | +6 | 0.015625 ✓ |
| (6, 1) | +5 | 0.0625 ✗ HELD |
| (7, 1) | +6 | 0.03515625 ✓ |
| (9, 2) | +7 | 0.03271484375 ✓ |
| (8, 3) | +5 | 0.11328125 ✗ HELD |

| Outcome | Verdict | What the region means (no weasel words) |
|---|---|---|
| McNemar one-sided p ≤ 0.05 **and** b > c (minimum practical: net +5 with zero compensating flips) | **CONTINUE** | The plan-conditioned pipeline adds measurable decision accuracy at this scale/bench. The planner-executor pattern enters the adaptive-loop designs (later lanes only). |
| net (b−c) ≤ 0 | **KILL** | Plan-conditioning adds nothing on this bench/apparatus. The coordinator axis is retired for the piloted scope. |
| net > 0 but p > 0.05 | **HELD** | Indeterminate gain. Licenses nothing, retires nothing, no re-runs. |
| Any hypothesis rewording after seeing outputs | **BARRED** | Law #4. Scientific misconduct, not a verdict. |

**Statistical honesty (disclosed):** with n_valid ≤ 60, the test reliably detects decision-grade effects (≥5 net flips with clean discordance); smaller true effects land in HELD by design. **No rescue runs:** a HELD or KILL is never followed by a larger-n re-test, more outlines, a different slot, or a re-seed — each would be an unlicensed gate tweak (barred). A compute-controlled follow-up is a separate pre-registered lane, not a continuation.

---

## 5. Falsification decision tree

```
bench provenance + len==60
 ├─ mismatch → RUN-INVALID (apparatus)
 └─ ok → backbone LOG-331 pin (pre)
     ├─ mismatch → RUN-INVALID (quarantine)
     └─ ok → planner prompts byte-verified vs EXP113 T2-P2 records
         ├─ mismatch → RUN-INVALID (apparatus bug)
         └─ ok → Phase 0a: recitation check (10 probe items)
             ├─ ≥6/10 items with ≥2 verbatim-recited outlines → RUN-INVALID (planner not planning)
             └─ pass → Phase 0b: decision-channel mini-gate (10 probe items, baseline slot)
                 ├─ <8/10 parseable OR <2 distinct entities (minority <2) → RUN-INVALID
                 └─ pass → full run: 60 planner + ≤240 executor + 60 baseline generations
                     ├─ >10% per-generation exceptions → RUN-INVALID
                     └─ ok → backbone pin (post); mismatch → RUN-INVALID (quarantine)
                         └─ ok → deterministic re-parse ×2; mismatch → RUN-INVALID
                             └─ ok → n_valid < 48 → RUN-INVALID (elicitation failure)
                                 └─ n_valid ≥ 48 → paired McNemar one-sided on (b, c)
                                     ├─ p ≤ 0.05, b > c → CONTINUE
                                     ├─ b − c ≤ 0 → KILL
                                     └─ b − c > 0, p > 0.05 → HELD
```

No other branches exist. No re-runs, no larger item sets, no post-hoc bars, no slot modifications mid-run (Law #4, Law #9).

---

## 6. Cost and honesty

- **$0 CPU, ~2.5–4.5h worst case:** Phase 0 ≈ 20 generations (~15–30 min); full run ≤ 360 generations (60×≤160 + 240×≤16 + 60×≤16 ≈ 14,400 tokens max). Calibrated against EXP109 (108 generations in 20.9 CPU-min) and EXP115 (60 generations in 142.5s). No GPU contact. Generation is the *subject* of measurement — the licensed exception to the program's logit-readout posture, fenced to this apparatus question (the H7 precedent).
- **Honesty ledger:** (a) Phase 0 is the binding constraint — the full run is licensed only if both mini-gates pass, and the most likely failure (decision channel, 3/3 priors) is front-loaded, not buried; (b) the compute confound (§3.9) is disclosed, not controlled — a CONTINUE does not isolate planning; (c) T2-P2's content is unchecked by EXP113 — Phase 0a checks it, and the verbatim-match criterion's paraphrase blind spot is disclosed; (d) the finding is backbone-specific (base Pythia-410m, CPU, greedy).

---

## 7. What H11 does NOT claim

1. A CONTINUE licenses the plan-conditioned **pipeline** as an adaptive-loop component — it does **not** license the claim that *planning* (vs additional compute, vs outline text as extra context) caused the gain. The planning-vs-compute attribution is explicitly unlicensed (§3.9).
2. Parseable outlines ≠ real plans; the recitation gate (§3.7, Phase 0a) guards the construct mechanically, but outline *quality* is not measured — a CONTINUE does not claim the outlines are good plans, only that the pipeline using them beats the baseline.
3. Not reasoning, not consciousness, not capability beyond this bench (60 items, one backbone, one decoding regime).
4. A KILL retires the coordinator axis for the piloted scope (this bench, this apparatus) — not the summit program, not test-time scaling in general (cf. H8/POE's fences).
5. A RUN-INVALID at Phase 0a vs 0b vs the 48/60 gate distinguishes *which* apparatus piece failed (planner content / answer slot / pipeline elicitation) — each is a boundary finding, not a verdict.
6. **Novelty: N1 — Known Combination.** Planner-executor test-time patterns are prior art (H4's pre-reg §8: Wu et al., Meta FAIR); the combination (frozen-410m + greedy + validated-elicitation apparatus + paired McNemar decision test) is the contribution (Law #10).

---

## 8. Adaptations (complete list — H11 was not in the round-2 dossier; the H9-review lesson: no omissions)

**From H4's pre-registered design:**
1. **Planner protocol:** verbatim T2-P1 → H7's T2-P2 (few-shot). *Why:* EXP109 demonstrated T2-P1 degenerates into the repetition attractor on 18/20 items; T2-P2 cleared 60/60 parseable outlines on this exact bench (EXP113). This substitution is the EXP113-licensed revival.
2. **Decoding regime:** temperature=0.7/top_p=0.9 sampling → greedy throughout. *Why:* every EXP113 clearance was under greedy; EXP109's sampled baseline failed 80/80 unparseable; sampling is unvalidated on this backbone.
3. **Answer slot:** H4's bare "Reply with the name of the higher-ranked entity and nothing else." → the same sentence plus the priming tail "The higher-ranked entity is:". *Why:* the bare slot's greedy behavior is unknown; the priming tail imports T1-P5's continuation mechanism (its entity-name-shape risk is absorbed by Phase 0b — the EXP116 lesson).
4. **Baseline generations:** 4 independent samples → 1 greedy generation. *Why:* greedy has no sampling variation; 4 copies would be identical. Consequence: the matched-budget framing is dropped (see 6).
5. **Generation caps:** planner stays 160; executor/baseline 48 → 16. *Why:* entity names are 1–3 tokens; short caps limit echo/tail-runaway risk (the EXP115/116 lesson).
6. **Budget definition:** matched executor budget → pipeline-vs-baseline with disclosed compute asymmetry (§3.9). *Why:* at greedy, repeated sampling is impossible; the planning-premium-at-matched-budget question H4 posed cannot be asked in this regime. The attribution fence (§7.1) carries the honesty load.
7. **n:** 20-item pilot → full 60-item bench. *Why:* the McNemar license needs discordant-pair room; cost (≤14,400 tokens, ~2.5–4.5h) is within the CPU envelope; the pilot scope was H4's cost decision, not a scientific one.
8. **Elicitation gate:** 20−n_valid ≥ 3 → n_valid ≥ 48/60. *Why:* the 80% EXP113 clearance threshold, scaled to n=60.
9. **Phase-0 mini-gates added** (recitation check + decision-channel validation, §3.7). *Why:* the EXP115/116 lesson — validated-on-one-shape does not transfer, and T2-P2's content was never checked. In neither H4 nor H7.
10. **Item-valid/arm-valid rule:** H4's per-arm "≥ 3 parseable votes" validity (§3.5: 4 executor + 4 baseline generations per item) → H11's per-item rule: planner-valid (§3.3) AND ≥2 executor votes parseable AND baseline parseable (§3.8). *Why:* at greedy, the baseline arm has exactly 1 generation and the executor arm has 2–4 (one per extracted outline), so H4's ≥3-of-4 per-arm rule is arithmetically impossible; the thresholds are re-derived for the reduced generation counts. The ≥2-executor-parseable floor preserves H4's anti-degeneracy intent (an item decided on a single executor vote is excluded). This is a forced consequence of adaptations 2 and 4, not an independent design choice.

**From H7's T2-P2 spec:**
11. **No change.** The planner template, exemplar items (3, 4), exemplar outlines, and generation spec are imported byte-verbatim; the execution lane byte-verifies against EXP113's raw prompts (§3.3). The probe-item exclusion (3, 4) in Phase 0a is a *gating* choice, not a spec change.

**Unchanged from H4 (noted for completeness):** the outline-extraction rule (§3.3), the parse rule (§3.6), the vote rule with foil tie-break (§3.6), the bench/builder/provenance pin (§3.1), the backbone pin procedure (§3.1), the McNemar one-sided license (§4).

---

## 9. Boundary

Independent Law #14 review of this exact file is a separate lane. No experiment number is minted by this draft. Execution, if ever launched, is a CEO decision under a minted number. This lane stops here.
