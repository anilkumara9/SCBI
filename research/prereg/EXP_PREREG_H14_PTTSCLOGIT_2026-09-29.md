# Pre-registration: H14 — PTTSC-LOGIT (Plan-Conditioned Logit-Level Decision)

**Status:** DRAFT pre-registration. Licenses nothing. No model runs, no experiment number minted, no signed protocol touched, no GPU contact, no commits, no pushes. $0 CPU.
**Drafting lane:** LOG-4624 (pre-assigned). **Source:** `research/strategy/INNOVATION_SPRINT_2026-09-29_H1315.md` §H14 (worth-it gate passed).
**Launch chain:** independent Law #14 review of this exact file → fix-verification (if fixes required) → CEO launch decision → execution under a minted experiment number. This lane stops at the draft.

**Governing laws:** Law #4 (no post-hoc hypothesis shifts — the bars below are binding), Law #6 (frozen backbone Δθ=0), Law #7 (zero data leakage — bench ground truth used only at metric time; the planner exemplars are format demonstrations, not labels), Law #9 (metrics registered before any output is inspected), Law #13 (deterministic reproducibility — seeds, hashes, environment manifest pinned below).

**Epistemological labels** per `SCBI/AGENTS.md` §5: [OBSERVATION], [HYPOTHESIS], [INTERPRETATION], [PROPOSITION], [ASSUMPTION], [FACT].

---

## 0. Worth-it gate (the 6 elements, recorded before drafting)

**[HYPOTHESIS under test]** H14 (PTTSC-LOGIT): prepending a T2-P2-generated plan (EXP113's cleared protocol, imported byte-verbatim via H11 §3.3) to the executor's context changes the frozen backbone's zero-generation logit-level decision (EXP112's apparatus) relative to the no-plan baseline logit decision, on the 60-item EXP107 template-decorrelated bench — paired per item, licensed by the one-sided McNemar exact test.

1. **Exact question:** At fixed greedy/logit-readout decoding on the 60-item EXP107 bench, does the plan-conditioned context (bench prompt + T2-P2 plan block, logit readout at the final position) produce different decisions than the unconditioned baseline context (bench prompt verbatim, same readout), paired per item, with correctness scored against the bench's tuple[0] target entity?
2. **Decision changed:**
   - **CONTINUE** (McNemar one-sided p ≤ 0.05, b > c): the plan-text-conditioned pipeline changes decisions at the logit level — the pipeline enters the adaptive-loop designs as a registered component (later lanes only), under the §7.1 fence.
   - **KILL** (net b−c ≤ 0): plan conditioning moves nothing even at the logit level — the plan-conditioning question is retired on the EXP107 bench (logit channel tested and null; the generation channel on EXP107 remains untested).
   - **HELD** (net > 0, p > 0.05): indeterminate; licenses nothing, retires nothing, no re-runs.
   - **RUN-INVALID:** any Phase-0 gate, pin, or validity check fires — the apparatus failed; the hypothesis gets no verdict.
3. **Cheapest test:** Phase 0 answers the two binding unknowns for ~20 generations + ~20 forwards (~20–30 min $0 CPU) before the full run is licensed: (0a) the planner's bench transfer — T2-P2's 60/60 clearance was on the EXP091 bench (EXP113), and H14 runs on the EXP107 bench; planner-validity (≥2 distinct non-empty outlines per H11 §3.3) is re-gated on 10 probe items; (0b) the logit decision slot with a plan prefix — context-length and tokenization effects are the binding unknown (the plan block changes the middle of the context); per-item validity requires both arms' G1 mass ≥ 0.01 and final-token tokenization identity between arms; <8/10 valid → RUN-INVALID. No cheaper test answers the planning question: H11's apparatus is dead on the generation channel, and the logit-level composition is untested.
4. **Mathematical license:** EXP112 HELD (41/60 self-report fidelity — the zero-generation logit decision channel works on this exact bench); EXP113 apparatus CONTINUE (T2-P2 outlines 60/60 parseable — the planner channel works). The composition — plan text in context, logit decision out — is the untested question. This is H11's question with the dead generation channel replaced by the proven logit channel; H11 was RUN-INVALID (apparatus failure), never killed as a hypothesis. Paired one-sided McNemar exact on the discordant pairs (b, c); minimum practical CONTINUE configuration (5,0) → p = 0.03125 (verified at drafting, §4).
5. **Quantitative prediction:** Honestly, no directional effect size is licensed — the test is for any detectable paired difference. If plan-conditioning adds a decision-grade effect, expect McNemar (b,c) with b−c ≥ +5 clean → CONTINUE; if it adds nothing, expect net ≈ 0 → KILL. The HELD zone absorbs underpowered regions by design.
6. **Breaking point:** Phase 0a (<8/10 planner-valid → RUN-INVALID — the planner does not transfer to this bench); Phase 0b (<8/10 valid or tokenization mismatch → RUN-INVALID — the logit slot does not function with a plan prefix); baseline reproduction ≠ 60/60 vs EXP112's archived readout (apparatus drift); the 48/60 n_valid gate; the McNemar bars. The design is refused (REJECT, a legitimate review outcome) if the plan-text treatment is judged too confounded by the known recitation caveat (§7.1.2) to license — a fair Law #14 ground.

**Key challenges adjudicated:**

(a) **Is H14's question genuinely new vs H11 (generation RUN-INVALID) and H6 (honesty, no planning)?** [PROPOSITION] Yes. [OBSERVATION] EXP117 (H11) ended RUN-INVALID at Phase 0b (0/10 parseable) — the generation decision channel does not exist on the entity-name shape, so H11's planning question was never tested. [OBSERVATION] EXP112 (H6) tested the honesty instrument's self-report fidelity (41/60 HELD) — no planning, no plan conditioning. [OBSERVATION] EXP113 tested elicitation (parseability), not decisions. H14 asks H11's question — does plan-conditioning change decisions? — through H6's proven zero-generation logit channel, on H6's bench. New apparatus composition, new data (60 fresh planner generations + 120 fresh logit forwards), new experiment number licensed. Not a re-run (re-runs are barred): H11's generation apparatus is not re-executed.

(b) **The token-asymmetry honesty fence.** [PROPOSITION] Carried over from H11 §3.9/§7.1 and adapted: the plan arm's context is longer than the baseline's by the plan block (~≤200 tokens). Greedy/logit readout has no sampling variation, so the comparison is pipeline-vs-baseline with the token asymmetry disclosed — not planning-vs-compute. A CONTINUE licenses the plan-text-conditioned pipeline as an adaptive-loop component only; planning-vs-compute attribution is explicitly unlicensed (§7.1).

(c) **Mathematical license.** [FACT] The McNemar critical values are verified at drafting (§4): (5,0) → 0.03125 ✓ CONTINUE; (4,0) → 0.0625 ✗ HELD; (6,1) → 0.0625 ✗ HELD. The HELD zone (net > 0, p > 0.05) blocks razor-thin CONTINUEs by construction.

(d) **Phase-0 and the §3.7 lesson.** [OBSERVATION] EXP117's Phase-0a adjudication (LOG-4610, BIND): H11 §3.7's literal recitation definition (exact match vs marker-prefixed exemplar lines) is structurally inert for verbatim content recitation because the §3.3 extraction rule strips the markers — the literal gate scored 0/10 while the content-level diagnostic showed 10/10 probe items with ≥2 content-level recitations. H14 does **not** reuse the inert definition. Instead: (i) Phase-0a gates on the structural planner-valid rule (≥2 distinct non-empty outlines — the plan has outline structure, whatever its content); (ii) a corrected content-level recitation diagnostic is reported (marker-stripped exemplar content vs marker-stripped extracted outlines, exact match after strip+casefold — diagnostic only, not a gate); (iii) the treatment is defined as "the T2-P2 plan text as generated", and EXP117's 10/10 diagnostic is disclosed as a construct caveat in the honesty fence (§7.1.2). The worth-it verdict does not depend on plan quality: the causal question (does the plan text change the logit decision?) is answerable regardless, and a KILL is informative either way.

**Gate verdict: PASS.** The planning question is open at the logit level (untested composition of two cleared apparatuses), the test is cheap ($0 CPU, ~20–30 min), the breaking points are registered in advance, and the known confounds (recitation, token asymmetry, bench transfer) are front-loaded into gates or fenced — not assumed away.

---

## 1. Hypothesis (one falsifiable sentence)

**[HYPOTHESIS]** On the 60-item EXP107 template-decorrelated bench, the plan-conditioned logit decision (frozen backbone reads argmax over the two pinned entity token ids at the final position of the plan-augmented context) differs from the unconditioned baseline logit decision (same readout on the verbatim bench prompt) in decision accuracy against the bench's tuple[0] target entity — paired one-sided McNemar exact p ≤ 0.05 with b > c.

**Falsifiers:** net (b−c) ≤ 0 on the paired valid items → the plan-conditioning question is retired on this bench (logit channel); Phase-0 gate or pin failures → RUN-INVALID (apparatus, not a verdict).

### 1.1 How H14 differs from H11/EXP117, H6/EXP112, and EXP113 [FACT]

[OBSERVATION] H11 (EXP117) asked the planning question through a generation decision channel: T2-P2 planner → per-outline greedy executor generations → majority vote vs greedy baseline. It ended RUN-INVALID at Phase 0b — the entity-name generation slot is not a decision channel on base Pythia-410m (4th consecutive failure: EXP109/115/116/117). The question was never tested.

[OBSERVATION] H6 (EXP112) built the zero-generation logit decision channel on the EXP107 bench: context = bench prompt verbatim, readout = argmax(logit[t1], logit[t2]) at the final position, 41/60 HELD fidelity vs the cosine decision statistic. No planning, no plan conditioning.

[OBSERVATION] EXP113 validated T2-P2 elicitation (60/60 parseable outlines) on the EXP091 bench — parseability, not planning, not decisions.

H14 is a **new hypothesis**: H11's scientific question (does plan-conditioning change decisions?) asked through H6's proven channel (zero-generation logit readout) on H6's bench (EXP107). What carries over from H11: the question, the T2-P2 planner spec (§3.3, byte-verbatim), the outline-extraction rule, the McNemar license and bars, the 48/60 validity gate, the token-asymmetry fence. What carries over from H6: the logit readout apparatus, the G1/G2 guard discipline, the BPE assertion, the tie-break, the bench and its provenance pins. What is new: the plan-conditioned context template (§3.4), the two-arm paired design, the Phase-0b tokenization-identity check, the baseline-reproduction integrity check.

---

## 2. Exact question and the decision it changes

**Exact question [HYPOTHESIS]:** At fixed logit-readout decoding on the 60-item EXP107 bench, does prepending the T2-P2-generated plan block to the executor context change the zero-generation logit-level decision relative to the no-plan baseline?

**Decision changed:**
- **CONTINUE** (§4): McNemar one-sided p ≤ 0.05 with b > c → the plan-text-conditioned pipeline changes decisions at the logit level; the pipeline enters the adaptive-loop designs as a registered component (later, separately pre-registered lanes only), under the §7.1 fence.
- **KILL** (§4): net (b−c) ≤ 0 → plan conditioning moves nothing even at the logit level; the plan-conditioning question is retired on the EXP107 bench (logit channel tested and null; the generation channel on EXP107 was never tested).
- **HELD** (§4): net > 0 but p > 0.05 → indeterminate; licenses nothing, retires nothing, no re-runs.
- **RUN-INVALID:** any Phase-0 gate (§3.7), pin mismatch, baseline-reproduction failure, or the n_valid gate (§3.8) fires → the apparatus failed; the hypothesis gets no verdict. Not evidence about planning.

**Primary metric (registered before any run):** paired accuracy difference on n_valid items (n_valid ≤ 60). Per item per arm: decision = the readout entity (§3.6); correct iff the decision entity equals the bench record's `tuple[0]` (the target entity per the bench builder's registered construction — `build_exp107_bench.py` module docstring: the meaning-preserving flip keeps "the ranking meaning (A > B > C [> D]) ... preserved", so `tuple[0]` = A is the highest-ranked entity on all 60 items; pinned independently by H6 §3.2: "E1 = `tuple[0]` (the target entity)"). b = plan-arm-correct/baseline-arm-wrong; c = plan-arm-wrong/baseline-arm-correct. Verdict licensed by the one-sided McNemar exact test: p = P(X ≥ b | n = b+c, 0.5).

**Law #7 posture:** the ground-truth target (tuple[0]) is used **only at metric time** — never during planner generation, never during readout, never in any selection or gating choice. The T2-P2 planner exemplars are format demonstrations (their correctness is irrelevant); they carry no labels.

---

## 3. Method

### 3.1 Frozen backbone, bench, environment [FACT / pinned]

- **Backbone:** frozen Pythia-410m snapshot `~/workspace/.exp086_weights/pythia-410m`. `device_map="cpu"`, float32, `model.eval()` before all model contact, `torch.no_grad()` around ALL forwards and generations.
- **Δθ=0 procedure (pinned):** SHA-256 over tensor bytes with sorted `state_dict` keys, float32 (the EXP077/EXP084/EXP108 canonical convention). Asserted **before the first model contact and after the last**; any mismatch → RUN-INVALID, quarantine, no metric read. Expected pin: `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed` (LOG-331).
- **Bench:** the 60-item EXP107 template-decorrelated bench — identical provenance pins as H6 §3.2 / EXP112 §1: canonical bench-JSON SHA-256 `e91b302f41f641c74e56957e526efcd4866bac62d134e157defe0a4cdd49e4f5`; npz `6cf4a8a726a2b6e4623f57d0287d95879866f77e789bcc3789fb693cf2af6a76`; embeddings-bytes `9b6e8afb091ba1edbb0311ba1d3414d34a65942c3fdecb4533b69720f2a99123`; ids-bytes `3669e102222719d66f61daca46ae1ac34e844e398ae433743a5b37bfc5075cb9`. `len(bench) == 60` asserted. **Bench-schema assertion (new):** every record has `prompt`, `premise`, `tuple` (len ≥ 2), `phrasing`, `id` keys; `prompt == premise + QUESTION_SUFFIX` byte-exactly, where QUESTION_SUFFIX = `" Question: Who is higher in rank? Answer:"` (EXP112-pinned). Any mismatch → RUN-INVALID.
- **Environment (Law #13):** torch==2.14.0+cpu, transformers==5.17.0, numpy==2.5.3, sklearn==1.9.1; `torch.manual_seed(0)` + numpy seed 0; CPU threads set and read back via `torch.get_num_threads()`; greedy decoding (`do_sample=False`) for the planner generations; nothing left to tune. All recorded in the execution worksheet.

### 3.2 Item set [PROPOSITION]

All 60 items in bench build order (indices 0–59). No subsampling, no pilot phase beyond the pinned Phase-0 probe items (which are regenerated fresh in the full run — Phase-0 records are diagnostics, never metric inputs; Law #9).

### 3.3 Planner spec — T2-P2 imported byte-verbatim from H11 §3.3 (H7 §3.3) [FACT]

The planner prompt for target item t is constructed **byte-exactly** per H11 §3.3 (itself byte-verbatim from H7 §3.3 T2-P2):

- `TAIL` = `Plan: Before answering, write 4 distinct numbered solution outlines (1. 2. 3. 4.), each a different approach to answering the question. Each outline must be 40 words or fewer. Do not give the final answer yet.`
- `OUTLINES` (pinned verbatim exemplars — format demonstrations; correctness irrelevant):
  ```
  1. Restate the question's ordering constraint in my own words.
  2. Check each premise statement against the two candidate entities.
  3. Eliminate the entity contradicted by any premise.
  4. Name the remaining entity as the answer.
  ```
- `block(i)` = `{PROMPT_i}` + `"\n\n"` + `TAIL` + `"\n"` + `OUTLINES`, for exemplar items i ∈ {3, 4} (bench build order, pinned).
- `prompt(t)` = `block(3)` + `"\n\n"` + `block(4)` + `"\n\n"` + `{PROMPT_t}` + `"\n\n"` + `TAIL`.
- `{PROMPT}` = the item's bench `prompt` field verbatim.

**Byte-identity check (Law #13):** the execution lane asserts the 60 constructed planner prompts are byte-identical to the H11 §3.3 construction for the same target items (reference: the signed H11 pre-registration §3.3 code-equivalent construction); any mismatch → RUN-INVALID (apparatus bug). [Honesty note: T2-P2's 60/60 clearance (EXP113) was on the EXP091 bench; H14 runs the planner on the EXP107 bench — the bench transfer is re-gated by Phase-0a, not assumed.]

**Generation spec (pinned):** greedy (`do_sample=False`), `max_new_tokens=160`. One planner generation per item.

**Outline extraction (pinned — H11 §3.3 / H4 §3.3 verbatim):** scan the planner output left to right; record the first occurrence position of each literal marker `1.`, `2.`, `3.`, `4.`; for k=1..4, outline_k = the substring from the end of marker `k.` to the start of the next marker occurrence in position order (or end of output), stripped; text before the first marker (preamble) discarded; a missing marker yields an empty outline; drop empties and exact duplicates; **planner-valid iff ≥ 2 distinct non-empty outlines remain**.

### 3.4 Plan-conditioned executor context (pinned — new) [PROPOSITION]

For each planner-valid item, the plan block is constructed byte-exactly:

- `PLAN_BLOCK` = `"Plan:\n"` + `"\n".join(f"{i+1}. {o}" for i, o in enumerate(OUTLINES))`, where OUTLINES are the extracted planner-valid outlines (2–4) in extraction order, re-numbered sequentially.
- `CONTEXT_PLAN` = `{PREMISE}` + `" Question: Who is higher in rank?\n\n"` + `PLAN_BLOCK` + `" Answer:"`, where `{PREMISE}` is the bench record's `premise` field verbatim.

**Decomposition assertion (pinned):** the execution lane asserts `{PREMISE} + QUESTION_SUFFIX == {PROMPT}` byte-exactly for every item before constructing plan contexts (this verifies the split point); any mismatch → RUN-INVALID.

**Rationale for the template:** the readout is at the final position; the plan block sits between the question and the answer slot, so the final `" Answer:"` region mirrors the baseline's suffix shape. The total context stays far below the 2048-token window (bench prompts are short; plan blocks ≤ ~200 tokens); the execution lane asserts `len(tokenize(CONTEXT_PLAN)) < 2048` for every item.

### 3.5 Baseline context (pinned — H6/EXP112 verbatim) [FACT]

`CONTEXT_BASE` = the bench record's `prompt` field verbatim (`{PREMISE} + " Question: Who is higher in rank? Answer:"`). Zero new wording — identical to EXP112's self-report context.

### 3.6 Logit readout, decision rule, guards (pinned — H6/EXP112) [FACT]

- **Readout (per arm per item):** one forward pass, `torch.no_grad()`; logits read at the final position only; `readout = argmax(logit[t1], logit[t2])`; ties (exact float equality) → E2 (mirrors H6).
- **Entities/token ids:** E1 = `tuple[0]`, E2 = `tuple[-1]`; t1/t2 = the pinned single-token ids from EXP112's worksheet. **BPE single-token re-assertion (pinned):** `" "+E1` and `" "+E2` each tokenize to exactly one token on the real Pythia tokenizer, for all 60 items (120/120); any failure → RUN-INVALID, items NOT dropped.
- **Decision entity:** E1 if readout selects t1, else E2.
- **G1 (per arm per item, pinned):** mean post-softmax mass on (t1, t2) ≥ 0.01 — the H6 non-degeneracy rule. An arm-item readout failing G1 is degenerate.
- **G2-style variation (baseline arm, pinned as a firing gate):** across the 60 baseline-arm readouts: ≥2 distinct decision entities with minority ≥ 3 — else RUN-INVALID (the baseline channel is not discriminating; apparatus failure). [Adaptation: the plan arm's variation is diagnostic only — the plan could legitimately push accuracy high; a constant plan arm is reported, not gated.]
- **Correctness:** per arm per item, correct iff the decision entity equals `tuple[0]` (ground truth; Law #7 — metric time only).

### 3.7 Phase-0 gates (pinned — both fire before any metric) [PROPOSITION]

Phase 0 runs on the pinned probe set **{0, 1, 2, 5, 6, 7, 8, 9, 10, 11}** (10 items; items 3–4 excluded — they are the planner's exemplars). All Phase-0 model contact uses the pinned §3.3–§3.6 specs.

- **Phase 0a — planner bench-transfer check:** run the §3.3 planner on the 10 probe items; extract outlines per §3.3; score planner-valid per item. If **<8/10 probe items are planner-valid** → **RUN-INVALID** (T2-P2 does not transfer to the EXP107 bench as a plan elicitor; construct failure). [Rationale: EXP113's 60/60 clearance was on EXP091; the bench transfer is the untested step, front-loaded here, not assumed.]
  - **Corrected recitation diagnostic (diagnostic only, NOT a gate):** for each probe item, compare each extracted outline against the marker-stripped exemplar content (the 4 exemplar lines with their leading `"N. "` markers removed, then strip+casefold) — an outline recites iff it exactly equals one of these. Report the per-item recitation counts and the probe-set rate. This definition corrects H11 §3.7's structural defect (LOG-4610: the literal definition compared marker-stripped extractions against marker-prefixed exemplar lines and was inert). EXP117's finding (10/10 probe items with ≥2 content-level recitations on the EXP091 bench) is disclosed as the construct caveat (§7.1.2); it does not fire any gate because the treatment is defined as the generated plan text whatever its content.
- **Phase 0b — logit slot with plan prefix:** for each of the 10 probe items: construct `CONTEXT_PLAN` and `CONTEXT_BASE` per §3.4–§3.5 (asserting the §3.4 decomposition); assert **tokenization identity**: `tokenize(CONTEXT_PLAN)[-3:] == tokenize(CONTEXT_BASE)[-3:]` (the `" Answer:"` region must tokenize identically — else the readout positions are not comparable); run both forwards; score G1 per arm. A probe item is **valid** iff tokenization identity holds AND both arms pass G1 (mass ≥ 0.01). If **<8/10 probe items are valid** → **RUN-INVALID** (the logit decision slot does not function with a plan prefix on this bench/shape; context-length or tokenization effects break the channel). Tokenization mismatch on any single item → RUN-INVALID immediately (confound, not a rate).

Phase-0 records are diagnostics only and never enter the metric. If Phase 0 passes, the full run (§3.8) regenerates all 60 items fresh (greedy decoding is deterministic — no selection on partial data, Law #9).

### 3.8 Full run, item validity, integrity checks, and the n_valid gate [PROPOSITION]

If Phase 0 passes: 60 planner generations (§3.3) + 60 plan-arm forwards (§3.4, §3.6) + 60 baseline-arm forwards (§3.5, §3.6), all with zero exceptions tolerated silently (per-contact exceptions caught, logged, scored as failed; >10% exceptions → RUN-INVALID, apparatus bug).

- **Item valid** iff planner-valid (§3.3) AND plan-arm G1 pass AND baseline-arm G1 pass. n_valid = number of valid items (≤60).
- **Baseline-reproduction integrity check (pinned):** the 60 fresh baseline-arm readout decisions must match EXP112's archived readout column (`exp112_per_item.json`, `readout` field) **60/60**; any mismatch → **RUN-INVALID** (apparatus drift — the baseline context is byte-identical to EXP112's, and greedy decoding is deterministic). This check arbitrates environment/weight integrity independently of the hash pins.
- **Baseline-arm variation gate:** <2 distinct decision entities or minority <3 across the 60 baseline readouts → **RUN-INVALID** (the baseline channel is not discriminating).
- **Elicitation-failure gate:** n_valid < 48/60 (below the 80% EXP113 clearance threshold, H11's gate) → **RUN-INVALID**. Not a verdict.
- **Deterministic re-read:** the readout/parse script is a pinned pure function of the raw forward logs; run twice, assert byte-identical decision tables; mismatch → RUN-INVALID.

### 3.9 Budget definition (pinned — H11's framing carried over and adapted) [PROPOSITION]

H11's pipeline-vs-baseline framing is carried over: the plan arm's context is longer than the baseline's by the plan block (~≤200 tokens + template). At logit readout there is no sampling variation, so no matched-budget design exists — the comparison is pipeline-vs-baseline with the token asymmetry disclosed as the treatment cost. Any gain cannot be attributed to planning specifically vs additional context tokens — this confound is **disclosed as a fence** (§7.1), not hand-waved. A context-controlled follow-up (e.g., a sham-plan arm) would be a separate pre-registered lane, not part of this one.

### 3.10 What H14 reuses vs rebuilds [FACT]

Reuses byte-verbatim: the T2-P2 planner template and exemplars (H11 §3.3 ← H7 §3.3), the outline-extraction rule (H4 §3.3), the logit readout + tie-break + BPE assertion (H6/EXP112), the G1 guard (H6), the bench + provenance pins (H6 §3.2), the backbone pin procedure (LOG-331), the McNemar one-sided license and critical values (H11 §4), the 48/60 gate (H11 §3.8). Rebuilds (adaptations, all listed in §8): the two-arm paired design, the plan-conditioned context template, the tokenization-identity check, the baseline-reproduction integrity check, the composite item-validity rule, accuracy-vs-tuple[0] as the metric, the corrected recitation diagnostic.

---

## 4. Decision bars with statistical license

All bars are on the paired valid-item set (n_valid ≤ 60). b = plan-arm-correct/baseline-arm-wrong; c = plan-arm-wrong/baseline-arm-correct. (E1 = tuple[0] is always the correct entity, so b = plan-E1/baseline-E2 and c = plan-E2/baseline-E1.) Verdict licensed by the **one-sided McNemar exact test**: p = P(X ≥ b | n = b+c, 0.5). Critical values verified at drafting:

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
| McNemar one-sided p ≤ 0.05 **and** b > c (minimum practical: net +5 with zero compensating flips) | **CONTINUE** | The plan-text-conditioned pipeline changes decisions at the logit level. The pipeline enters the adaptive-loop designs as a registered component (later lanes only), under the §7.1 fence. |
| net (b−c) ≤ 0 | **KILL** | Plan conditioning moves nothing even at the logit level. The plan-conditioning question is retired on the EXP107 bench (logit channel tested and null; the generation channel on EXP107 was never tested). |
| net > 0 but p > 0.05 | **HELD** | Indeterminate. Licenses nothing, retires nothing, no re-runs. |
| Any hypothesis rewording after seeing outputs | **BARRED** | Law #4. Scientific misconduct, not a verdict. |

**Statistical honesty (disclosed):** with n_valid ≤ 60, the test reliably detects decision-grade effects (≥5 net flips with clean discordance); smaller true effects land in HELD by design. **No rescue runs:** a HELD or KILL is never followed by a larger-n re-test, a different plan template, a different readout, or a re-seed — each would be an unlicensed gate tweak (barred). A context-controlled follow-up is a separate pre-registered lane, not a continuation.

---

## 5. Falsification decision tree

```
bench provenance + len==60 + schema (prompt/premise/tuple keys; prompt == premise + QUESTION_SUFFIX)
 ├─ mismatch → RUN-INVALID (apparatus)
 └─ ok → backbone LOG-331 pin (pre)
     ├─ mismatch → RUN-INVALID (quarantine)
     └─ ok → planner prompts byte-verified vs H11 §3.3 T2-P2 construction
         ├─ mismatch → RUN-INVALID (apparatus bug)
         └─ ok → Phase 0a: planner bench-transfer (10 probe items)
             ├─ <8/10 planner-valid → RUN-INVALID (planner does not transfer)
             └─ pass → Phase 0b: logit slot with plan prefix (10 probe items)
                 ├─ tokenization mismatch (last-3 ids) on any item → RUN-INVALID (confound)
                 ├─ <8/10 items both-arms G1-pass → RUN-INVALID (slot broken)
                 └─ pass → full run: 60 planner generations + 120 forwards
                     ├─ >10% per-contact exceptions → RUN-INVALID
                     └─ ok → backbone pin (post); mismatch → RUN-INVALID (quarantine)
                         └─ ok → baseline reproduction vs EXP112 archived readout
                             ├─ ≠60/60 → RUN-INVALID (apparatus drift)
                             └─ ok → deterministic re-read ×2; mismatch → RUN-INVALID
                                 └─ ok → baseline-arm variation (<2 distinct or minority <3)
                                     ├─ fails → RUN-INVALID (baseline not discriminating)
                                     └─ ok → n_valid < 48 → RUN-INVALID (validity failure)
                                         └─ n_valid ≥ 48 → paired McNemar one-sided on (b, c)
                                             ├─ p ≤ 0.05, b > c → CONTINUE
                                             ├─ b − c ≤ 0 → KILL
                                             └─ b − c > 0, p > 0.05 → HELD
```

No other branches exist. No re-runs, no larger item sets, no post-hoc bars, no template modifications mid-run (Law #4, Law #9).

---

## 6. Cost and honesty

- **$0 CPU, ~20–30 min worst case:** Phase 0 ≈ 20 generations + 20 forwards (~15–25 min; calibrated against EXP117's 20 generations in 5.8 min — the planner generations dominate); full run = 60 generations (≤160 tokens each) + 120 single forwards (~15–20 min; calibrated against EXP112's 180 forwards in ~86 s). No GPU contact. Zero training; backbone frozen, Δθ=0.
- **Honesty ledger:** (a) Phase 0 is the binding constraint — the full run is licensed only if both mini-gates pass, and the two binding unknowns (planner bench transfer; logit slot with plan prefix) are front-loaded, not buried; (b) the token-asymmetry confound (§3.9) is disclosed, not controlled — a CONTINUE does not isolate planning; (c) the recitation caveat (§7.1.2) is disclosed — the treatment is the plan text as generated, and outline quality is unmeasured; (d) the finding is backbone-specific (base Pythia-410m, CPU, logit readout) and bench-specific (EXP107).

---

## 7. What H14 does NOT claim

### 7.1 The honesty fence (binding)

1. A CONTINUE licenses the plan-text-conditioned **pipeline** as an adaptive-loop component — it does **not** license the claim that *planning* (vs additional context tokens, vs plan-shaped text as extra context) caused the change. The planning-vs-compute attribution is explicitly unlicensed (§3.9).
2. **Recitation caveat (the §3.7 lesson):** planner-valid outlines ≠ real plans, and outline *quality* is not measured. EXP117's Phase-0a diagnostic found 10/10 probe items with ≥2 content-level verbatim recitations of the T2-P2 exemplars (LOG-4610, BIND) — the planner partially recites. H14's treatment is therefore defined as "the T2-P2 plan text as generated" (partially recited, partially item-specific), and a CONTINUE does not claim the outlines are good plans — only that the pipeline using their text changes decisions vs baseline. H11 §3.7's literal recitation definition is not reused (adjudicated structurally inert); the corrected content-level diagnostic (§3.7) is reported, not gated.
3. Not reasoning, not consciousness, not deceptive intent, not capability beyond this bench (60 items, one backbone, one readout regime).
4. A KILL retires the plan-conditioning question for the EXP107 bench via the logit channel — not the summit program, not test-time scaling in general, not the generation channel on EXP107 (untested).
5. A RUN-INVALID at Phase 0a vs 0b vs the reproduction check vs the 48/60 gate distinguishes *which* apparatus piece failed (planner transfer / plan-prefix slot / environment drift / pipeline validity) — each is a boundary finding, not a verdict.
6. **Novelty: N1 — Known Combination.** Plan-conditioning and logit-lens readouts are prior art; the combination (frozen-410m + T2-P2 plan text in context + paired logit-decision test) is the contribution (Law #10).

---

## 8. Deviations (complete list — the H9-review lesson: no omissions)

**From H6's pre-registered spec (EXP112's apparatus):**
1. **New question:** H6 measured self-report fidelity vs the cosine decision statistic; H14 measures plan-vs-no-plan accuracy vs the bench target. The McNemar statistic, arms, and bars are registered before any model contact.
2. **Two arms per item** (plan-conditioned context vs verbatim baseline context) instead of H6's single self-report context (+ archived decision column).
3. **Metric:** accuracy vs `tuple[0]` (labels at metric time only, Law #7) instead of fidelity vs the cosine decision statistic.
4. **Decision bars:** paired McNemar one-sided (H11's bars, §4) instead of H6's fidelity bands.
5. **Planner generation added:** T2-P2 (H11 §3.3 ← H7 §3.3), greedy, ≤160 tokens — H6 had zero generation.
6. **Composite item-validity rule:** planner-valid AND plan-arm G1-pass AND baseline-arm G1-pass (new; §3.8).
7. **n_valid ≥ 48/60 gate** (from H11 §3.8; new vs H6).
8. **Phase-0 gates added** (0a planner bench-transfer; 0b logit slot with plan prefix, §3.7). In neither H6 nor H11's original form.
9. **Baseline-reproduction integrity check** (60/60 vs EXP112's archived readout column; §3.8). New.
10. **G4 not applicable** (no cosine decision statistic in H14); **G2-style variation**: firing gate for the baseline arm (§3.8), diagnostic-only for the plan arm (§3.6).
11. **BPE single-token assertion re-applied** to the same entities (t1/t2 from EXP112's worksheet); failure → RUN-INVALID as in H6.
12. **Per-cell diagnostic dropped** — cell stratification was killed at the H12 worth-it gate (p = 0.0946 noise); no decision branch and no diagnostic reads the cells (same as H13 §3.8).

**From H11's pre-registered spec:**
13. **Decision channel:** zero-generation logit readout (H6's apparatus) instead of greedy generation executor/baseline developments. This is the defining adaptation — H11's question, H6's channel.
14. **Bench:** EXP107 template-decorrelated bench (H6's bench, with H6's provenance pins) instead of the EXP091 bench. Consequence: T2-P2's EXP113 clearance was on EXP091, so the planner's bench transfer is re-gated by Phase-0a rather than assumed.
15. **No majority vote:** one logit readout per arm per item instead of per-outline executor votes with foil tie-break. Ties (exact float equality) → E2 per H6's rule.
16. **Phase 0b redefined:** logit slot with plan prefix (tokenization identity + G1 per arm) instead of the generation-slot parse gate. H11's Phase 0b tested a channel that does not exist (EXP117 0/10); H14 tests the channel EXP112 proved.
17. **Recitation handling:** H11 §3.7's literal definition dropped (adjudicated structurally inert, LOG-4610); replaced by the planner-valid structural rule (gated) + the corrected content-level diagnostic (diagnostic only) + the §7.1.2 construct caveat.
18. **Plan presentation:** all extracted outlines in a single plan block within one context (§3.4) instead of per-outline executor generations.
19. **Ground-truth key:** bench `tuple[0]` target entity (EXP107 bench: `tuple[0]` = A, the highest-ranked entity under the meaning-preserving flip — H6 §3.2) instead of the EXP091 bench's "A"-keyed entity. Same role (the correct answer), different bench schema.
20. **Token asymmetry smaller but still disclosed:** the plan arm adds ~≤200 context tokens (vs H11's ≤224 generated tokens); the §3.9/§7.1 fence is carried over unchanged in force.

**Unchanged from H11 (noted for completeness):** the T2-P2 planner template and exemplars (§3.3), the outline-extraction rule (§3.3), the McNemar one-sided license and critical values (§4), n=60, the 48/60 gate (§3.8), the probe-item set {0,1,2,5,6,7,8,9,10,11} (§3.7).

---

## 9. Boundary

Independent Law #14 review of this exact file is a separate lane. No experiment number is minted by this draft. Execution, if ever launched, is a CEO decision under a minted number. This lane stops here.
