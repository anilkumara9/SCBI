# Pre-registration: H21 — PLAN-INSTRUMENT (Plan-Conditioned Instrument Selection)

**Status:** DRAFT pre-registration. Licenses nothing. No model runs, no experiment number minted, no signed protocol touched, no GPU contact, no commits, no pushes. $0 CPU.
**Drafting lane:** LOG-4667 (pre-assigned). **Source:** `research/strategy/INNOVATION_DESIGN_SESSION_POST_EXP123_2026-09-29.md` §H21 (LOG-4665) → worth-it gate PASS, `research/strategy/H21_GATE_2026-09-29.md` (LOG-4666).
**Launch chain:** independent Law #14 review of this exact file → fix-verification (if fixes required) → CEO launch decision → execution under a minted experiment number. This lane stops at the draft.

**Governing laws:** Law #4 (no post-hoc hypothesis shifts — the bars below are binding), Law #6 (frozen backbone Δθ=0), Law #7 (zero data leakage — bench ground truth used only at metric time; the planner exemplars are format demonstrations, not labels; the choice-extraction rule is symmetric in the two candidate entities and knows nothing of which is correct), Law #9 (metrics registered before any output is inspected), Law #13 (deterministic reproducibility — seeds, hashes, environment manifest pinned below).

**Epistemological labels** per `SCBI/AGENTS.md` §5: [OBSERVATION], [HYPOTHESIS], [INTERPRETATION], [PROPOSITION], [ASSUMPTION], [FACT].

---

## 0. Worth-it gate (the 6 elements, recorded before drafting)

**[HYPOTHESIS under test]** H21 (PLAN-INSTRUMENT): the EXP113-cleared T2-P2 planner's choice between two phrasing variants (A-first / C-first) of the decision prompt — the choice a pinned mechanical function of the generated plan text, the plan text never entering any decision prompt — changes the frozen backbone's zero-generation logit-level decision (EXP112's apparatus) relative to a random-phrasing control, on the 60-item EXP107 template-decorrelated bench — paired per item, licensed by the one-sided McNemar exact test.

1. **Exact question:** Does a planning artifact — the T2-P2 planner's choice between two phrasing variants of the decision prompt, with the plan text never entering the prompt — steer the decision outcome, measured by paired (per-item) comparison of the EXP112 logit readout on the plan-chosen phrasing versus a random-chosen phrasing, under a paired McNemar test on correctness?
2. **Decision changed (bars carried verbatim from the H21 gate memo §2 — a fidelity-to-license requirement, not a new choice):**
   - **CONTINUE** — one-sided McNemar p < 0.05 AND d ≥ 10 (d = discordant pairs) → the hypothesis "plan-informed instrument selection moves decisions vs random, label-free" continues. Licenses plan-as-instrument as a candidate adaptive-loop component. The honest caveat rides with it: this is **steering-adjacent** (the plan chooses the measurement instrument), not full autonomous steering; it belongs to the label-free None-class (§2.1 — no training, no labels). This would be the program's first label-free plan→decision causal signal.
   - **KILL** — p ≥ 0.05 AND d ≥ 40 → retires the instrument-selection channel: plan-informed choice moves nothing under this apparatus. d ≥ 40 is the registered 80%-power floor (power(q=0.70) at d=40 → 0.807, α=0.05 one-sided; executor-computed at the gate lane: d=38 → 0.774, d=40 → 0.807, d=44 → 0.861).
   - **HELD** — p ≥ 0.05 with d < 40 → underpowered; licenses nothing, retires nothing. No rescue. (Draft gap-fill, §8 item 7, flagged for Law #14: p < 0.05 with d < 10 → HELD as well — the gate's "minimum discordant floor d ≥ 10 for any CONTINUE" principle admits no CONTINUE below d=10.)
   - **RUN-INVALID** — any §5 breaking-point miss (apparatus-void, UNTESTED — hypothesis gets no verdict, no number minted).
   
   Notes (gate §2, verbatim): (i) a reverse-direction asymmetry (planner systematically picks the worse phrasing) is an unlicensed descriptive observation, not a verdict; (ii) this gate refines the design session's "two-sided" sketch to one-sided, matching the directional quantitative prediction in §4 — deviation recorded, subject to Law #14 review of the pre-reg (§8 item 1, §9).
3. **Cheapest test:** 60 planner choice-generations (pinned T2-P2 prompt, EXP113 §3.3 verbatim, + the pinned mechanical choice-extraction of §3.4 — Law #7-clean: no bench labels touch the planner; correctness of the pinned exemplars is irrelevant to the parseability metric, as in H7) + 120 variant forwards (60 items × 2 phrasing variants — A-first and C-first, the EXP107 bench's genuine `phrasing` field, 30/30 balanced, verified in `EXP107_templatectrl/out/exp107_per_item.json`) + 60 choice-arm forwards (EXP112 pinned readout on the planner-chosen variant per item; the random arm, seed-pinned, is derived from the same 120 variant forwards — no extra model contact needed). Total: **60 generations + 180 forwards, $0 CPU.**
4. **Mathematical license:** EXP113's T2 clearance (bound CONTINUE, LOG-4584 — few-shot P2 and priming P5 clear 80% on both task shapes; the planner channel works — EXP119 Phase-0a 10/10 and EXP121 Phase-0a 10/10 on the same bench; the choice-generation is a T2-P2 generation plus a mechanical extraction, so elicitation is licensed). EXP112's readout (bound HELD, 41/60 — the decision channel works; baseline reproduction 60/60 archived in EXP121). Paired McNemar with executor-computed p: the exact one-sided binomial test on the discordant pairs — the correct paired test for two decision rules on the same items, no asymptotic approximation. Power floor (executor-computed at the gate lane, registered here): at one-sided α=0.05, power 0.807 at d=40 for true discordant asymmetry q=0.70 (gate-lane computed: d=37 → 0.807, d=38 → 0.774, d=39 → 0.740, d=40 → 0.807, d=44 → 0.861 — exact binomial critical values are non-monotone in d); the registered KILL bar takes d ≥ 40 as a conservative pre-registered cutoff; below it a p ≥ 0.05 is underpowered → HELD. Why phrasing-selection is a valid planning instrument: the planner's choice is a deterministic function of the generated plan text (plan-conditioned), and the plan text never enters the decision prompt. The token-asymmetry confound that fenced EXP119/EXP121 is **sidestepped by construction, not by disclosure** — there is no plan-token arm whose effect could be attributed to extra context tokens, because no plan token reaches the readout (§3.9).
5. **Quantitative prediction:** under planning-steers-decisions, the discordant pairs skew toward plan-chosen-correct (q > 0.5, targeted q ≈ 0.70 for power); under planning-is-inert, the discordant split is symmetric (q = 0.5) and the choice-gate (a) below fires or the test lands HELD/KILL.
6. **Breaking point (conjunctive — any miss → apparatus-void, UNTESTED, no number minted):** (a) the choice-information gate — each phrasing chosen ≥ 20% of the time (≥ 12/60); a constant choice is a decision-inert control, not a treatment; (b) Phase-0 phrasing-discriminability — on a pinned 10-item probe, the two phrasing variants must yield different EXP112 readouts on ≥ 3/10 items; if the variants are decision-indistinguishable, the planner's choice cannot move decisions; (c) per-arm G1 guard as a CONSTRUCTION-TIME filter — both phrasing variants must pass H6's channel-level G1 (M ≥ 0.01) on the Phase-0 probe, symmetric across variants (the EXP121 class-6 defect made structurally impossible: G1 validity is a property of the prompt variants — fixed, pinned strings — not a post-hoc per-item screen on a treatment arm; collapsing items are pre-registered as invalid; per-item G1 degeneracy in the full run on the pinned prompts fires RUN-INVALID as apparatus drift, never item-dropping); (d) Δθ=0 pins — LOG-331 backbone hash asserted before the first generation and after the last forward; mismatch → RUN-INVALID; (e) raw records — all 60 choice-generations and all forward records persisted and hash-pinned before any verdict (EXP119 lesson); p-value executor-computed, never hand-written (defect class 1). Additionally: planner choice-valid ≥ 8/10 on the Phase-0a probe (T2-P2 parse rule, EXP113 §3.4); both variant tails byte-identical to the QUESTION_SUFFIX tail (the identity surface is asserted absent, not assumed).

**Key challenges adjudicated:**

(a) **The choice-extraction rule is specified at drafting (not in the gate memo).** [PROPOSITION] The gate licensed "a pinned mechanical choice-extraction" without specifying it. This draft pins the final-outline entity-mention rule (§3.4): the planner's last extracted outline (its decision commitment — the pinned exemplars' outline 4 is "Name the remaining entity as the answer") is scanned left-to-right for the first literal occurrence of either candidate entity name (E1 = `tuple[0]`, E2 = `tuple[-1]`); the first-named entity selects the phrasing variant that presents that entity first (A-FIRST if E1, C-FIRST if E2); no mention → choice-invalid. The rule is a deterministic function of the plan text (plan-conditioned), mechanical (a script, no judgment), symmetric in E1/E2 (it does not know which entity is correct — Law #7-clean), and its failure signature is honest: exemplar recitation (the EXP117/EXP119 10/10 recitation finding) yields entity-free final outlines → choice-invalid → the Phase-0a <8/10 gate fires → RUN-INVALID (apparatus-void). This specification is a genuine draft-level gap-fill and a fair Law #14 rejection ground if judged arbitrary (§8 item 4, §9).

(b) **Phrasing-swap vs the EXP107 word-family flip.** [FACT] The EXP107 builder's pinned `flip_premise` preserves phrasing and swaps the word family (it is the template-decorrelation instrument) — it cannot produce the opposite phrasing variant. H21 needs, per item, the A-first and C-first phrasings with the word family held fixed. This draft therefore pins a distinct deterministic phrasing-swap (§3.5) — an involution the execution lane verifies (`SWAP(SWAP(P)) == P` on all 60 premises; mismatch → RUN-INVALID). The swap preserves the ranking meaning (A > B > C [> D]) and changes only the target's sentence position.

(c) **Token-asymmetry is sidestepped by construction — the design's core dodge.** [PROPOSITION] All three H11 failure modes are dodged structurally, not by disclosure (§3.9): EXP117's generation channel is dead — zero entity-name generation anywhere; the only generation is the EXP113-cleared T2-P2 planner, and the decision readout is EXP112's pinned logit channel only (a degenerated planner is caught by the Phase-0a choice-valid gate before any metric is read). EXP119's tokenization identity — plan text never enters any decision prompt; both phrasing variants are byte-verbatim fixed strings ending in the identical `" Question: Who is higher in rank? Answer:"` tail; the [-3:] identity surface does not exist by construction and is asserted byte-identical at Phase-0. EXP121's plan-arm G1 mass collapse — the readout prompts are the pinned baseline prompts; G1 behavior is the EXP112-archived channel's own (60/60 reproduction in EXP121); plan tokens cannot push mass off the final position because they are never in the context; per-item G1 is screened at construction time on the two prompt variants, symmetrically — the selection-biased dropout that killed EXP121 has no treatment arm to act on.

(d) **H11's hypothesis is alive, not killed.** [OBSERVATION] The planning question (does plan text change decisions?) is RUN-INVALID three times on three apparatuses (EXP117's generation channel; EXP119's prefix composition; EXP121's suffix composition — LOG-4644 + LOG-4646 erratum) and was never killed as a hypothesis. H21 is a new channel under Law #4 (no generation channel, no plan-prefix, no plan-suffix), not a re-run. A KILL here retires the instrument-selection channel and exhausts H11's fourth logit-channel composition — no further H11 composition is licensed without a genuinely new instrument class (gate §7).

---

## 1. Hypothesis (one falsifiable sentence)

**[HYPOTHESIS]** On the 60-item EXP107 template-decorrelated bench, the plan-chosen phrasing variant's logit decision (frozen backbone reads argmax over the two pinned entity token ids at the final position of the planner-selected A-first/C-first variant context) differs in decision accuracy from the random-chosen variant's logit decision against the bench's tuple[0] target entity — paired one-sided McNemar exact p < 0.05 with d ≥ 10, discordance skewed toward plan-chosen-correct.

**Falsifiers:** p ≥ 0.05 with d ≥ 40 → the instrument-selection channel is retired (KILL); any Phase-0 gate, pin, pre-check, or validity check fires → RUN-INVALID (apparatus, not a verdict).

### 1.1 How H21 differs from H11/EXP117, H14/EXP119, H19/EXP121, H6/EXP112, and EXP113 [FACT]

[OBSERVATION] H11 (EXP117) asked the planning question through a generation decision channel — RUN-INVALID at Phase 0b (0/10 parseable). The question was never tested.

[OBSERVATION] H14/EXP119 asked it through a plan-**prefix** composition — RUN-INVALID at Phase 0b on item 0; the plan's final token broke the pinned [-3:] tokenization identity (LOG-4628, structural, BIND). The question was never tested.

[OBSERVATION] H19/EXP121 asked it through a plan-**suffix** composition (placement A) — RUN-INVALID at the elicitation-failure gate (n_valid=38/60 < 48; LOG-4644 + LOG-4646 erratum): per-item G1 mass collapse on the plan arm with selection-biased dropout (the class-6 defect). The question was never tested.

[OBSERVATION] H6 (EXP112) built the zero-generation logit decision channel on the EXP107 bench (41/60 HELD) — no planning.

[OBSERVATION] EXP113 validated T2-P2 elicitation (60/60 parseable, bound CONTINUE) — parseability, not decisions.

H21 is a **new hypothesis composition**: H11's question (does planning change decisions?) through H6's channel (zero-generation logit readout) on H6's bench (EXP107), where the planning artifact's only causal handle is **instrument selection** — the T2-P2 planner's choice between two fixed phrasing variants of the decision prompt, with zero plan tokens in any decision context. What carries over from H19: the T2-P2 planner spec (§3.3, byte-verbatim), the outline-extraction rule, the McNemar one-sided license, the Δθ=0 pins, the bench and its provenance pins, the 60/60 baseline-reproduction integrity check, the defect-class discipline. What carries over from H6: the logit readout apparatus, the tie-break, the BPE assertion, the G1 guard discipline (restructured as a construction-time filter). What is new: the plan-conditioned choice extraction (§3.4), the two phrasing variants with the pinned phrasing-swap construction (§3.5), the choice-vs-random paired design with the discordant-count floors (§4), and the structural token-asymmetry sidestep (§3.9).

---

## 2. Exact question and the decision it changes

**Exact question [HYPOTHESIS]:** At fixed logit-readout decoding on the 60-item EXP107 bench, does the T2-P2 planner's choice between the A-first and C-first phrasing variants of the decision prompt — extracted mechanically from the generated plan text, plan text never entering the prompt — change the zero-generation logit-level decision accuracy relative to a random phrasing choice?

### 2.1 The label-free None-class [DEFINITION]

A **label-free None-class** instrument is one in which **no training** (no weight updates, no adapters, no learned probes) and **no labels** (no ground-truth targets at any stage of planner generation, choice extraction, or readout — Law #7; bench targets used at metric time only) enter the causal path from planning to decision. H21's plan-conditioned instrument selector belongs to this class: the backbone is frozen, the choice-extraction rule (§3.4) is a mechanical script over generated text, and the readout is a fixed logit argmax. A CONTINUE here is therefore **steering-adjacent** (the plan chooses the measurement instrument; the instrument does the deciding), not full autonomous steering.

**Decision changed (verbatim from the gate memo §2):**
- **CONTINUE** (§4): one-sided McNemar p < 0.05 AND d ≥ 10 → the hypothesis "plan-informed instrument selection moves decisions vs random, label-free" continues. Licenses plan-as-instrument as a candidate adaptive-loop component — steering-adjacent, label-free None-class, NOT full autonomous steering. This would be the program's first label-free plan→decision causal signal.
- **KILL** (§4): p ≥ 0.05 AND d ≥ 40 → retires the instrument-selection channel: plan-informed choice moves nothing under this apparatus. d ≥ 40 is the registered 80%-power floor.
- **HELD** (§4): p ≥ 0.05 with d < 40 → underpowered; licenses nothing, retires nothing. No rescue. (Plus the §8-item-7 gap-fill: p < 0.05 with d < 10 → HELD — no CONTINUE below the d ≥ 10 floor.)
- **RUN-INVALID:** any §5 breaking-point miss → apparatus-void, UNTESTED; the hypothesis gets no verdict, no number minted.

**Primary metric (registered before any run):** per-item correctness of the two arms against the bench's tuple[0] target entity (the target per the builder's meaning-preserving construction — `build_exp107_bench.py` module docstring: the ranking meaning "A > B > C [> D]" is preserved and "the target's sentence position (first for A-first, last for C-first)" is preserved, so `tuple[0]` = A is the highest-ranked entity on all 60 items; pinned independently by H6 §3.2: "E1 = `tuple[0]` (the target entity)" — defect class 3, the FIX-1 label-pin discipline). Choice arm: EXP112 readout on the planner-chosen variant (fresh forward, §3.8). Random arm: EXP112 readout on the seed-pinned random variant (derived from the 120 variant forwards, §3.8). b = choice-correct/random-wrong; c = choice-wrong/random-correct; d = b+c. Verdict licensed by the one-sided McNemar exact test: p = P(X ≥ b | n = d, 0.5), executor-computed.

**The seven binding defect classes are pinned as protocol requirements:**
1. **Executor-computed p-values only** (EXP120 lesson): the execution script computes and prints the one-sided McNemar p-value from the raw decision table; the report quotes the script's printed value verbatim. A p-value appearing in the report but absent from the raw logs is a defect (erratum if discovered post-verdict).
2. **Raw generation records persisted before any verdict** (EXP119 lesson): all 60 planner generation texts and all 180 forward logs are persisted as artifacts, hash-pinned, before the verdict is written. Artifact-existence gate: missing artifact → RUN-INVALID.
3. **FIX-1 label-pin discipline** (LOG-4625/4626): the tuple[0]-as-target citation references the bench builder's meaning-preserving construction and H6 §3.2's independent pin — never a truncated code comment.
4. **No reuse of EXP117's §3.7 recitation definition** (LOG-4610): no recitation definition is used anywhere in H21 — gated or diagnostic. The choice-valid rule (§3.4) is structural (entity-mention in the final outline); exemplar recitation manifests as choice-invalidity and is caught honestly by the Phase-0a gate. The EXP117/EXP119 10/10 recitation finding is disclosed as the construct caveat (§7), not measured.
5. **The [-3:] identity pin on the composition** (EXP119 lesson): no plan text enters any decision context, so the identity surface does not exist — and it is asserted absent, not assumed: Phase-0pre asserts `tokenize(V)[-3:] == [32, 37741, 27]` (`?`, `ĠAnswer`, `:`) for every variant of every item before any model contact.
6. **Single-token entity assertion for the logit apparatus** (H18 lesson): satisfied by inheritance — H21 introduces no new bench and no new entities; EXP112's BPE single-token pin (t1/t2 from EXP112's worksheet) carries over unchanged.
7. **Per-item G1 as construction-time filter only** (EXP121 class-6 defect): G1 validity is a property of the two fixed prompt variants, screened channel-level at Phase-0b symmetrically; per-item G1 in the full run is a monitored invariant — any degenerate forward fires RUN-INVALID (apparatus drift), never item-dropping.

**Law #7 posture:** the ground-truth target (tuple[0]) is used **only at metric time** — never during planner generation, never during choice extraction (the §3.4 rule is symmetric in E1/E2 and does not know which entity is correct), never during readout, never in any selection or gating choice. The T2-P2 planner exemplars are format demonstrations (their correctness is irrelevant); they carry no labels. The random-variant draw is seed-pinned and label-blind.

---

## 3. Method

### 3.1 Frozen backbone, bench, environment [FACT / pinned]

- **Backbone:** frozen Pythia-410m snapshot `~/workspace/.exp086_weights/pythia-410m`. `device_map="cpu"`, float32, `model.eval()` before all model contact, `torch.no_grad()` around ALL forwards and generations.
- **Δθ=0 procedure (pinned):** SHA-256 over tensor bytes with sorted `state_dict` keys, float32 (the EXP077/EXP084/EXP108 canonical convention). Asserted **before the first model contact and after the last**; any mismatch → RUN-INVALID, quarantine, no metric read. Expected pin: `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed` (LOG-331).
- **Bench:** the 60-item EXP107 template-decorrelated bench — identical provenance pins as H6 §3.2 / H19 §3.1: canonical bench-JSON SHA-256 `e91b302f41f641c74e56957e526efcd4866bac62d134e157defe0a4cdd49e4f5`; npz `6cf4a8a726a2b6e4623f57d0287d95879866f77e789bcc3789fb693cf2af6a76`; embeddings-bytes `9b6e8afb091ba1edbb0311ba1d3414d34a65942c3fdecb4533b69720f2a99123`; ids-bytes `3669e102222719d66f61daca46ae1ac34e844e398ae433743a5b37bfc5075cb9`. `len(bench) == 60` asserted. Rebuilt at execution by `experiments/runs/EXP107_templatectrl/build_exp107_bench.py::build_bench()` (deterministic, no RNG, no model calls). **Bench-schema assertion (pinned):** every record has `prompt`, `premise`, `tuple` (len ≥ 2), `phrasing`, `id` keys; `prompt == premise + QUESTION_SUFFIX` byte-exactly, where QUESTION_SUFFIX = `" Question: Who is higher in rank? Answer:"` (EXP112-pinned); `phrasing` ∈ {`A-first`, `C-first`} with exactly 30/30 balance (verified at drafting in `EXP107_templatectrl/out/exp107_per_item.json`; re-asserted at execution). Any mismatch → RUN-INVALID.
- **Environment (Law #13):** torch==2.14.0+cpu, transformers==5.17.0, numpy==2.5.3, sklearn==1.9.1; `torch.manual_seed(0)` + numpy seed 0; CPU threads set and read back via `torch.get_num_threads()`; greedy decoding (`do_sample=False`) for the planner generations; nothing left to tune. The random-variant draw uses `numpy.random.default_rng(20260929)` (pinned seed, the EXP120 convention). All recorded in the execution worksheet.

### 3.2 Item set [PROPOSITION]

All 60 items in bench build order (indices 0–59). No subsampling, no pilot phase beyond the pinned Phase-0 probe items (which are regenerated fresh in the full run — Phase-0 records are diagnostics, never metric inputs; Law #9).

### 3.3 Planner spec — T2-P2 imported byte-verbatim from H19 §3.3 (H14 §3.3 ← H11 §3.3 ← H7 §3.3) [FACT]

The planner prompt for target item t is constructed **byte-exactly** per H14 §3.3:

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
- `{PROMPT}` = the item's bench `prompt` field verbatim (the item's own-phrasing prompt).

**Byte-identity check (Law #13):** the execution lane asserts the 60 constructed planner prompts are byte-identical to the H19 §3.3 construction for the same target items; any mismatch → RUN-INVALID (apparatus bug).

**Generation spec (pinned):** greedy (`do_sample=False`), `max_new_tokens=160`. One planner generation per item (60 total in the full run).

**Outline extraction (pinned — EXP113 §3.4, the T2 parse rule):** scan the output left to right; record the first occurrence position of each literal marker `1.`, `2.`, `3.`, `4.`; for each marker in position order, outline = the substring from the end of the marker to the start of the next marker in position order (or end of output), stripped; drop empties and exact duplicates → ordered outline list L (position order).

### 3.4 Choice extraction — the pinned mechanical rule (NEW — §0(a) specification) [PROPOSITION]

The planner's choice is extracted from the generated plan text by a deterministic script (no human judgment, no labels):

1. Apply the §3.3 outline extraction → ordered outline list L.
2. If |L| < 2 → **choice-invalid** (the T2-P2 parse rule fails; the planner produced no usable plan).
3. Let F = the last element of L (the final outline in position order — the planner's decision commitment; the pinned exemplars' outline 4 is "Name the remaining entity as the answer").
4. Let E1 = the item's `tuple[0]`, E2 = the item's `tuple[-1]` (bench record strings, as written in the premise; assert E1 != E2 at construction).
5. Scan F left to right for literal **case-sensitive** occurrences of E1 and E2, **leftmost-longest** (at each position, if both names match, the longer wins — pinned tie-break; in practice no bench-1 entity name is a prefix of another).
6. If the leftmost match is E1 → choice = **A-FIRST**. If E2 → choice = **C-FIRST**. If neither occurs in F → **choice-invalid**.
7. **choice-valid** iff a choice in {A-FIRST, C-FIRST} is extracted.

**Rationale (pinned):** the final outline is where the planner commits to an answer; the first-named entity in that commitment is the planner's attentional focus; the instrument selected is the phrasing variant that presents that entity first. The rule is a deterministic function of the plan text (plan-conditioned), symmetric in E1/E2 (it does not know which entity is correct — Law #7), and mechanical. **Honest failure signature:** exemplar recitation (the EXP117/EXP119 10/10 recitation finding) yields entity-free final outlines → choice-invalid → the Phase-0a <8/10 gate fires → RUN-INVALID (apparatus-void). The instrument was never a treatment, and the design says so rather than manufacturing a choice.

### 3.5 The two phrasing variants (pinned construction — NEW) [PROPOSITION]

For each item i with bench premise P_i, phrasing φ_i ∈ {A-first, C-first}, hop h_i ∈ {2, 3}, word family, and entities:

- **V_own(i)** = the bench `prompt` field verbatim (= P_i + QUESTION_SUFFIX). **Decomposition assertion (pinned):** `P_i + QUESTION_SUFFIX == prompt` byte-exactly for every item before variant construction; any mismatch → RUN-INVALID.
- **V_other(i)** = `SWAP(P_i) + QUESTION_SUFFIX`, where SWAP is the pinned deterministic phrasing-swap (meaning-preserving: the ranking A > B > C [> D] and the word family are held fixed; only the target's sentence position changes):
  - 2-hop, outranks family: `"Premise: {A} outranks {B}. {B} outranks {C}."` ↔ `"Premise: {B} outranks {C}. {A} outranks {B}."`
  - 2-hop, lower-than family: `"Premise: {B} is lower than {A}. {C} is lower than {B}."` ↔ `"Premise: {C} is lower than {B}. {B} is lower than {A}."`
  - 3-hop, outranks family: `"Premise: {A} outranks {B}. {B} outranks {C}. {C} outranks {D}."` ↔ `"Premise: {C} outranks {D}. {B} outranks {C}. {A} outranks {B}."`
  - 3-hop, lower-than family: `"Premise: {B} is lower than {A}. {C} is lower than {B}. {D} is lower than {C}."` ↔ `"Premise: {D} is lower than {C}. {C} is lower than {B}. {B} is lower than {A}."`
- **Involution check (pinned):** the execution lane asserts `SWAP(SWAP(P)) == P` byte-exactly for all 60 premises; mismatch → RUN-INVALID (construction bug).
- **Variant labels:** V_A(i) = the A-first variant, V_C(i) = the C-first variant (one is V_own, the other V_other).
- Both variants are **fixed strings constructed once at lane start** (construction time; no model contact, no RNG, no per-run variation). They are the only decision contexts in H21.

**Why not the EXP107 `flip_premise`:** that pinned function preserves phrasing and swaps the word family — it is the template-decorrelation instrument, not a phrasing instrument. H21 needs the opposite phrasing with the word family held fixed, so a distinct pinned function is required (§8 item 5).

### 3.6 Logit readout, decision rule, guards (pinned — H6/EXP112) [FACT]

- **Readout (per variant per item):** one forward pass, `torch.no_grad()`; logits read at the final position only; `readout = argmax(logit[t1], logit[t2])`; ties (exact float equality) → E2 (mirrors H6).
- **Entities/token ids:** E1 = `tuple[0]`, E2 = `tuple[-1]`; t1/t2 = the pinned single-token ids from EXP112's worksheet. **BPE assertion carries over (defect class 6):** H21 introduces no new bench and no new entities — EXP112's single-token pin applies unchanged; no re-assertion needed, no items screened.
- **Decision entity:** E1 if readout selects t1, else E2.
- **G1 — construction-time filter (pinned, the class-6 structural fix):** for variant v ∈ {A, C}, M_v = mean over the Phase-0 probe items of the post-softmax mass on (t1, t2) at the final position; require **M_A ≥ 0.01 AND M_C ≥ 0.01**, symmetric across variants (§3.7). G1 validity is a property of the fixed prompt variants, screened once at construction.
- **G1 — full-run invariant:** every forward's post-softmax mass on (t1, t2) is monitored; **any** degenerate forward (< 0.01) → **RUN-INVALID** (apparatus drift on the pinned prompts), never item-dropping. This is the EXP121 class-6 defect made structurally impossible: there is no treatment arm on which selection-biased dropout can act.
- **Correctness:** per arm per item, correct iff the decision entity equals `tuple[0]` (ground truth; Law #7 — metric time only).

### 3.7 Phase-0 gates (pinned — tokenizer pre-check first, then both gates before any metric) [PROPOSITION]

**Phase-0pre — tokenizer-only variant checks (no model contact):** before any model contact, the execution lane constructs all 60 variant pairs per §3.5 and asserts for every variant of every item: `tokenize(V)[-3:] == [32, 37741, 27]` (`?`, `ĠAnswer`, `:` — the EXP112/EXP119-pinned QUESTION_SUFFIX tail). **Mismatch on any single variant → RUN-INVALID immediately** (the identity surface is asserted absent, not assumed — defect class 5). The involution check (§3.5) and the decomposition assertion (§3.5) are verified here as well.

Phase-0a/0b run on the pinned probe set **{0, 1, 2, 5, 6, 7, 8, 9, 10, 11}** (10 items; items 3–4 excluded — they are the planner's exemplars). All Phase-0 model contact uses the pinned §3.3–§3.6 specs.

- **Phase-0a — planner choice-validity:** run the §3.3 planner on the 10 probe items; extract outlines and choices per §3.3–§3.4. If **<8/10 probe items are choice-valid** → **RUN-INVALID** (the T2-P2 planner does not yield instrument recommendations on this bench; elicitation failure — the honest apparatus-void, §0(a) failure signature).
- **Phase-0b — variant discriminability and channel G1:** for each probe item, run the §3.6 readout on both variants V_A and V_C.
  - **Discriminability:** the two variants must yield **different decision entities** on **≥ 3/10** probe items. If <3/10 differ → **RUN-INVALID** (the phrasing variants are decision-indistinguishable; the planner's choice cannot move decisions — gate breaking point (b)).
  - **Channel-level G1:** M_A ≥ 0.01 AND M_C ≥ 0.01 (means over the probe) → else **RUN-INVALID** (gate breaking point (c), symmetric across variants).

Phase-0 records are diagnostics only and never enter the metric. If Phase-0 passes, the full run (§3.8) regenerates all 60 items fresh (greedy decoding is deterministic — no selection on partial data, Law #9).

### 3.8 Full run, validity, integrity checks [PROPOSITION]

If Phase-0 passes: 60 planner generations (§3.3) + choice extraction (§3.4) → n_valid = number of choice-valid items (≤ 60).

- **Choice-information gate (a) — pre-metric:** each phrasing chosen on **≥ 12** items (absolute count = 20% of 60); else **RUN-INVALID** (a constant choice is a decision-inert control, not a treatment). Checked on the 60 full-run choices before any readout.
- **120 variant forwards:** §3.6 readout on both variants × 60 items. Per-item G1 invariant monitored (§3.6); any degenerate forward → RUN-INVALID.
- **Baseline-reproduction integrity check (pinned — carried from H19 §3.8):** the 60 V_own readouts (the variant matching each item's bench phrasing = the bench prompt verbatim = EXP112's context) must match EXP112's archived readout column (`exp112_per_item.json`, `readout` field) **60/60**; any mismatch → **RUN-INVALID** (apparatus drift — greedy decoding is deterministic on byte-identical contexts). This check arbitrates environment/weight integrity independently of the hash pins.
- **60 choice-arm forwards:** fresh §3.6 forward on the planner-chosen variant per item. **Determinism cross-check (pinned):** the choice-forward logits must be byte-identical to the corresponding variant forward's logits from the 120; mismatch → RUN-INVALID (nondeterminism bug). This turns the gate's 60 choice-arm forwards into an integrity pin rather than redundant contact.
- **Random arm (derived, no extra contact):** `numpy.random.default_rng(20260929)`; per item in build order, u ~ Uniform[0,1); variant = V_A if u < 0.5 else V_C; correctness from the corresponding 120-forward readout.
- **Correctness and the paired table:** per item per arm, correct iff decision entity == `tuple[0]` (Law #7 — metric time only). b = choice-correct/random-wrong; c = choice-wrong/random-correct; d = b+c.
- **Executor-computed McNemar p-value:** the execution script computes the one-sided exact p = P(X ≥ b | n = d, 0.5) = Σ_{k=b}^{d} C(d,k)/2^d from the raw decision table and prints it; the report quotes the script's printed value verbatim (defect class 1).
- **Deterministic re-read:** the readout/parse/choice script is a pinned pure function of the raw logs; run twice, assert byte-identical decision tables; mismatch → RUN-INVALID.
- **>10% per-contact exceptions** (generation or forward) → RUN-INVALID (apparatus bug); exceptions otherwise caught, logged, scored as failed contacts.
- **Raw-record pinning (defect class 2):** all 60 generation records and all 180 forward records persisted and hash-pinned **before** any verdict; missing artifact → RUN-INVALID.

### 3.9 Why there is no token-asymmetry confound — the sidestep (pinned) [PROPOSITION]

EXP119 and EXP121 were fenced by the token-asymmetry confound: the plan arm's context was longer than the baseline's by the plan block, so a CONTINUE could not attribute any change to planning vs additional context tokens. H21 has **no plan-token arm**: the planner's plan text never enters any decision prompt. The only thing that crosses from the planning stage to the decision stage is the **choice** — one bit selecting between two fixed, byte-verbatim prompts. Both decision contexts are pinned strings of comparable length (they differ only in premise phrasing); there is no "extra tokens" treatment whose effect could be confounded with planning. The treatment under test is precisely the **information content of the plan-conditioned choice** — which is exactly what the paired McNemar evaluates (choice-arm vs random-arm correctness). A CONTINUE therefore licenses the plan-as-instrument pipeline without the planning-vs-compute attribution fence that bound H14/H19 (§7.1 of those protocols does not apply here — and that non-application is itself pinned, not assumed).

### 3.10 What H21 reuses vs rebuilds [FACT]

Reuses byte-verbatim: the T2-P2 planner template and exemplars (H19 §3.3 ← H14 §3.3 ← H11 §3.3 ← H7 §3.3), the outline-extraction rule (EXP113 §3.4), the logit readout + tie-break + BPE assertion (H6/EXP112), the bench + provenance pins, the backbone pin procedure (LOG-331), the 60/60 baseline-reproduction integrity check (H19 §3.8), the probe-item set {0,1,2,5,6,7,8,9,10,11} (H19 §3.7), the McNemar one-sided license (H14 §4). Rebuilds (adaptations, all listed in §8): the choice-extraction rule (§3.4), the two phrasing variants with the pinned phrasing-swap (§3.5), the choice-vs-random paired design with discordant-count floors (§4), the construction-time G1 filter (§3.6–§3.7), the token-asymmetry sidestep (§3.9).

---

## 4. Decision bars with statistical license

All bars are on the n_valid choice-valid items (n_valid ≤ 60). b = choice-correct/random-wrong; c = choice-wrong/random-correct; d = b+c. Verdict licensed by the **one-sided McNemar exact test**: p = P(X ≥ b | n = d, 0.5) = Σ_{k=b}^{d} C(d,k)/2^d, executor-computed. Illustrative critical values (computed exactly at drafting — the executor recomputes from raw data at execution):

| (b, c) | d | one-sided exact p | bar |
|---|---|---|---|
| (10, 0) | 10 | 0.000977 | ✓ CONTINUE |
| (9, 1) | 10 | 0.010742 | ✓ CONTINUE |
| (8, 2) | 10 | 0.054688 | ✗ HELD |
| (7, 3) | 10 | 0.171875 | ✗ HELD |
| (7, 0) | 7 | 0.007812 | ✗ HELD (d < 10 floor) |
| (9, 0) | 9 | 0.001953 | ✗ HELD (d < 10 floor) |
| (28, 12) | 40 | 0.008295 | ✓ CONTINUE |
| (26, 14) | 40 | 0.040345 | ✓ CONTINUE |
| (25, 15) | 40 | 0.076930 | ✗ KILL |
| (22, 18) | 40 | 0.317914 | ✗ KILL |

| Outcome | Verdict | What the region means (no weasel words) |
|---|---|---|
| One-sided p < 0.05 **and** d ≥ 10 | **CONTINUE** | Plan-informed instrument selection moves decisions vs random, label-free. Licenses plan-as-instrument as a candidate adaptive-loop component — steering-adjacent, None-class, NOT full autonomous steering. The program's first label-free plan→decision causal signal. |
| p ≥ 0.05 **and** d ≥ 40 | **KILL** | Plan-informed choice moves nothing under this apparatus. The instrument-selection channel is retired; H11's fourth logit-channel composition is exhausted — no further H11 composition is licensed without a genuinely new instrument class. |
| p ≥ 0.05 with d < 40; **or** p < 0.05 with d < 10 (gap-fill, §8 item 7) | **HELD** | Underpowered. Licenses nothing, retires nothing, no rescue. |
| Any hypothesis rewording after seeing outputs | **BARRED** | Law #4. Scientific misconduct, not a verdict. |

**Statistical honesty (disclosed):** the d ≥ 10 floor means thin discordance can never CONTINUE no matter how clean the skew ((9,0) at d=9 → HELD); the d ≥ 40 KILL floor means a null result on fewer than 40 discordant pairs is HELD, not evidence of absence — the power floor (0.807 at q=0.70, d=40, one-sided α=0.05; gate-lane computed: d=38 → 0.774, d=44 → 0.861) is the registered justification. **No rescue runs:** a HELD or KILL is never followed by a larger-n re-test, a different choice-extraction rule, a different readout, or a re-seed — each would be an unlicensed gate tweak (barred). A reverse-direction skew (b << c, p ≈ 1) is reported as an unlicensed descriptive observation (gate §2(i)) and takes the KILL/HELD bar its (p, d) cell dictates — never a verdict of its own.

---

## 5. Falsification decision tree

```
bench provenance + len==60 + schema (prompt/premise/tuple/phrasing keys; prompt == premise + QUESTION_SUFFIX; phrasing 30/30)
 ├─ mismatch → RUN-INVALID (apparatus)
 └─ ok → variant construction (§3.5): SWAP involution + decomposition assertions
     ├─ mismatch → RUN-INVALID (construction bug)
     └─ ok → Phase-0pre: tokenizer-only [-3:] tail check on all 120 variant contexts
         ├─ any variant tail ≠ [32, 37741, 27] → RUN-INVALID (identity surface exists)
         └─ ok → backbone LOG-331 pin (pre)
             ├─ mismatch → RUN-INVALID (quarantine)
             └─ ok → planner prompts byte-verified vs H19 §3.3 T2-P2 construction
                 ├─ mismatch → RUN-INVALID (apparatus bug)
                 └─ ok → Phase-0a: planner choice-validity (10 probe items)
                     ├─ <8/10 choice-valid → RUN-INVALID (elicitation failure)
                     └─ pass → Phase-0b: variant discriminability + channel G1 (10 probe items)
                         ├─ <3/10 items with differing variant readouts → RUN-INVALID (instruments indistinguishable)
                         ├─ M_A < 0.01 or M_C < 0.01 → RUN-INVALID (channel degenerate)
                         └─ pass → full run: 60 planner generations + choice extraction
                             ├─ >10% per-contact exceptions → RUN-INVALID
                             └─ ok → choice-information gate: each phrasing chosen ≥ 12
                                 ├─ fails → RUN-INVALID (decision-inert control)
                                 └─ ok → 120 variant forwards (+ per-item G1 invariant)
                                     ├─ any degenerate forward → RUN-INVALID (apparatus drift)
                                     └─ ok → backbone pin (post); mismatch → RUN-INVALID (quarantine)
                                         └─ ok → baseline reproduction: V_own readouts vs EXP112 archived
                                             ├─ ≠60/60 → RUN-INVALID (apparatus drift)
                                             └─ ok → 60 choice-arm forwards + determinism cross-check
                                                 ├─ logits mismatch vs variant forwards → RUN-INVALID (nondeterminism)
                                                 └─ ok → deterministic re-read ×2; mismatch → RUN-INVALID
                                                     └─ ok → paired one-sided McNemar on (b, c), executor-computed p
                                                         ├─ p < 0.05, d ≥ 10 → CONTINUE
                                                         ├─ p ≥ 0.05, d ≥ 40 → KILL
                                                         └─ otherwise → HELD
```

No other branches exist. No re-runs, no larger item sets, no post-hoc bars, no choice-rule modifications mid-run (Law #4, Law #9).

---

## 6. Cost and honesty

- **$0 CPU, ~25–40 min worst case:** Phase-0pre ≈ minutes (tokenizer-only, no model contact); Phase-0a ≈ 10 generations (~5–10 min); Phase-0b = 20 forwards (~seconds); full run = 60 generations (≤160 tokens each, ~15–25 min calibrated against EXP119) + 180 single forwards (~2–3 min calibrated against EXP112's 180 forwards in ~86 s). No GPU contact. Zero training; backbone frozen, Δθ=0.
- **Honesty ledger:** (a) the choice-extraction rule (§3.4) is specified at drafting — it is the design's most contestable element, and the pre-registration says so (§0(a), §8 item 4, §9) rather than burying it; (b) the token-asymmetry confound is sidestepped by construction (§3.9), not disclosed as a fence — the draft pins exactly why no plan-token arm exists; (c) the recitation caveat is disclosed — the planner may recite exemplars, and the design converts recitation into honest apparatus-void via the choice-valid gate rather than measuring around it; (d) the finding is backbone-specific (base Pythia-410m, CPU, logit readout) and bench-specific (EXP107); (e) the (p<0.05, d<10) cell is a draft gap-fill, flagged for Law #14, not smuggled into the gate's bars.

---

## 7. What H21 does NOT claim

### 7.1 The honesty fence (binding)

1. A CONTINUE licenses plan-as-instrument as a **steering-adjacent candidate adaptive-loop component** — it does **not** license the claim of autonomous steering, agentic planning, reasoning, consciousness, or deceptive intent. The label-free None-class membership (§2.1 — no training, no labels) is the precise scope: the plan chooses the measurement instrument; the instrument does the deciding.
2. **Recitation caveat:** planner-valid plans ≠ good plans, and plan *quality* is not measured. EXP117's and EXP119's Phase-0a diagnostics found 10/10 probe items with ≥2 content-level verbatim recitations of the T2-P2 exemplars (LOG-4610, BIND; LOG-4628, BIND) — the planner partially recites. H21's choice rule converts recitation into choice-invalidity (entity-free final outlines) rather than scoring around it; a CONTINUE does not claim the plans are good — only that the plan-conditioned choice moves decisions vs random. EXP117's literal recitation definition is not reused anywhere (defect class 4).
3. Not generality beyond this bench (60 items, one backbone, one readout regime, two fixed phrasing variants). The phrasing variants are template pairs, not natural-distribution coverage.
4. A KILL retires the instrument-selection channel on frozen base Pythia-410m under CPU protocols — not the summit program, not test-time scaling in general, not trained-probe approaches (which live in a different class and were never candidates for the label-free frontier rows, §2.1).
5. A RUN-INVALID at Phase-0pre vs 0a vs 0b vs the choice-information gate vs the reproduction check distinguishes *which* apparatus piece failed (variant construction / planner elicitation / instrument discriminability / choice informativeness / environment drift) — each is a boundary finding, not a verdict. H11's question survives every RUN-INVALID.
6. **Novelty: N1 — Known Combination.** Plan-conditioning, phrasing variants, and logit-lens readouts are prior art; the combination (frozen-410m + T2-P2 plan text as a pure instrument selector + paired choice-vs-random logit-decision test with discordant-count floors) is the contribution (Law #10).

---

## 8. Deviations (complete list — the H9-review lesson: no omissions)

**From the design session's H21 sketch (LOG-4665):**
1. **One-sided McNemar** (this draft §4; gate §2) refining the session's two-sided sketch — matches the directional quantitative prediction (q > 0.5). Deviation recorded at the gate lane; carried forward here and **flagged for Law #14 review** (§9).
2. **KILL bar d ≥ 40 with the exact 80%-power floor** (gate §4: power(q=0.70) d=40 → 0.807, one-sided α=0.05) replacing the session's "≥80% power for a 10pp paired shift" sketch.
3. **Costing 60 generations + 180 forwards** — gate §3 licensed 60 generations + 120 variant forwards; the additional 60 choice-arm forwards are this draft's addition (item 8), replacing the session's "240 forwards + 60 gens" sketch; the 60 choice-arm forwards double as the determinism cross-check (§3.8).

**Specified at drafting (not in the gate memo — fair Law #14 scrutiny grounds):**
4. **The choice-extraction rule (§3.4)** — final-outline first-entity-mention, leftmost-longest, case-sensitive, choice-valid composite with the T2 parse rule. The gate licensed "a pinned mechanical choice-extraction" without specifying it (§0(a)).
5. **The phrasing-swap construction (§3.5)** — the gate named "two phrasing variants (A-first and C-first, the EXP107 bench's genuine phrasing field)"; the opposite-variant construction via the pinned involutive swap (not the EXP107 word-family flip, which preserves phrasing) is specified here, with the involution check.
6. **Baseline-reproduction check** (V_own readouts vs EXP112's archived `readout` column, 60/60 — carried from H19 §3.8); not explicit in the gate memo.
7. **(p < 0.05, d < 10) → HELD gap-fill** — the gate's bars leave this cell undefined; the gate's "minimum discordant floor d ≥ 10 for any CONTINUE" principle resolves it. **Flagged for Law #14.**
8. **Determinism cross-check** (choice-forward logits byte-identical to the corresponding variant forward's logits) — gives the gate's 60 choice-arm forwards an integrity function.
9. **Forward-record pinning clarified as 180 (120 + 60)** — the gate's §5(e) "120 forward records" is read as the variant forwards; the 60 choice-arm forwards are pinned likewise. The honest superset governs.
10. **Probe set pinned {0, 1, 2, 5, 6, 7, 8, 9, 10, 11}** (H19's set; items 3–4 are the planner exemplars).

**From H6's pre-registered spec (EXP112's apparatus):**
11. **New question:** plan-conditioned instrument selection vs random, measured on decision accuracy — H6 measured self-report fidelity vs the cosine decision statistic.
12. **Two fixed phrasing variants per item** instead of H6's single self-report context.
13. **Metric:** accuracy vs `tuple[0]` (labels at metric time only, Law #7) instead of fidelity vs the cosine decision statistic.
14. **Decision bars:** paired one-sided McNemar with discordant-count floors (§4) instead of H6's fidelity bands.
15. **Planner generation added:** T2-P2 (H19 §3.3 ← H14 §3.3 ← H11 §3.3 ← H7 §3.3), greedy, ≤160 tokens.
16. **G1 restructured:** channel-level construction-time filter on the two fixed variants (Phase-0b, symmetric) + full-run monitored invariant — instead of H6's per-arm-per-item validity screen (the EXP121 class-6 structural fix).
17. **G4 not applicable** (no cosine decision statistic in H21); **G2-style variation not applicable** (no baseline arm — the random arm is derived from the same 120 forwards).
18. **Per-cell diagnostic dropped** — cell stratification was killed at the H12 worth-it gate (p = 0.0946 noise); no decision branch and no diagnostic reads the cells.

**From EXP113/H7's spec:**
19. **T2-P2 prompt imported byte-verbatim** (§3.3); the T2 parse rule is **extended** with the choice extraction (§3.4) — the parse rule itself is unchanged.
20. **Task shape:** the planner output is used as an instrument selector (via §3.4), not scored for parseability as an end in itself — the 80% clearance bar is replaced by the choice-valid ≥8/10 Phase-0a gate and the ≥12/60 choice-information gate.

**Unchanged from the gate memo (noted for completeness):** the four registered bars (modulo gap-fill item 7), the five conjunctive breaking points, the Δθ=0 pins, the bench and environment pins, the Law #7 posture, all seven defect classes, the summit-filter statement.

---

## 9. Boundary

Independent Law #14 review of this exact file is a separate lane. No experiment number is minted by this draft. Execution, if ever launched, is a CEO decision under a minted number. This lane stops here.

**What this protocol cannot show:** whether the planner's choice would survive a different choice-extraction rule (the §3.4 rule is one pinned operationalization of "plan-conditioned choice" — a CONTINUE is conditional on it); whether phrasing-selection works outside the two template phrasings; why the planner's focus lands where it does (no mechanistic claim about the plan content); anything about the trained-probe line (different class, §2.1).

**Deviation carried forward for Law #14 review:** the one-sided McNemar (§4, §8 item 1) refining the design session's two-sided sketch — the gate lane recorded it as matching the directional prediction; the reviewer should confirm the directional license is earned and not a post-hoc tightening. The (p<0.05, d<10) → HELD gap-fill (§8 item 7) and the draft-specified choice-extraction rule (§8 item 4) are likewise flagged as reviewer-scrutiny items: a REJECT on any of them is a legitimate review outcome.
