# Pre-registration: H7 — EVALID (Elicitation Validation Instrument)

**Status:** DRAFT pre-registration. Licenses nothing. No model runs, no experiment number minted, no signed protocol touched, no GPU contact, no commits, no pushes. $0 CPU.
**Drafting lane:** LOG-4579 (pre-assigned). **Source:** `research/innovation/SPRINT_2026-09-29_SUMMIT_ROUND2.md` §H7 (worth-it gate passed, ranked #3).
**Launch chain:** independent Law #14 review of this exact file → fix-verification (if fixes required) → CEO launch decision → execution under a minted experiment number. This lane stops at the draft.

**Governing laws:** Law #4 (no post-hoc hypothesis shifts — the bars below are binding), Law #6 (frozen backbone Δθ=0), Law #7 (zero data leakage — bench labels never touch generation or any selection choice), Law #9 (metrics registered before any output is inspected), Law #13 (deterministic reproducibility — seeds, hashes, environment manifest pinned below).

**Epistemological labels** per `AGENTS.md` §5 ([HYPOTHESIS], [FACT], [OBSERVATION], [ASSUMPTION], [INTERPRETATION]) are used throughout.

---

## 1. Hypothesis (one falsifiable sentence)

**[HYPOTHESIS]** At least one of five pinned elicitation protocols clears the 80% mechanically-parseable structured-output bar on each task — the single-token answer task (T1, the H1 self-report shape) and the numbered-outline task (T2, the H4 planner shape) — from frozen base Pythia-410m under CPU greedy-decoding protocols. The clearing protocols need not be the same on T1 and T2.

**Falsifiers:** per the §4 decision tree — CONTINUE if at least one protocol clears ≥80% on each task (not necessarily the same protocol); PIVOT if clearance occurs on exactly one task; HELD if the best protocol reaches 22–47/60 on at least one task with no clearance; KILL if every protocol scores ≤21/60 on both tasks.

### 1.1 What H7 is and is not

H7 does **not** revive H1 or H4. EXP108 (H1/HDI) and EXP109 (H4/PTTSC) both went RUN-INVALID on generation degeneracy — the *unvalidated* protocols died, not the hypotheses. H7 asks the bounded apparatus question those failures left behind: does **any** instruction-following protocol work on this backbone? A CONTINUE licenses H1/H4 **revival lanes as NEW hypotheses with the validated protocol** (each carrying its own elicitation-failure gate); it does not continue H1/H4 themselves. A KILL closes the generation axis for this backbone — a real, valuable finding (it retires a line honestly), not a cop-out.

---

## 2. Exact question and the decision it changes

**Exact question [HYPOTHESIS]:** Does any of five pinned elicitation protocols produce ≥80% parseable structured outputs from frozen base Pythia-410m under CPU protocols, on each of the two downstream task shapes?

**Decision changed:**
- **CONTINUE** (§4): at least one protocol clears ≥80% on T1 **and** at least one (possibly different) protocol clears ≥80% on T2 → H1-revival and H4-revival lanes are licensable as NEW hypotheses, each with the named clearing protocol and its own elicitation-failure gate.
- **PIVOT** (§4): clearance on exactly one task → revival licensable only for the corresponding axis; the other axis stays retired pending its own separately pre-registered validation lane (bounded scope, no silent redesign).
- **HELD** (§4): partial elicitation (best protocol 22–47/60 on at least one task, no clearance) → licenses nothing, retires nothing. The apparatus question stays open but unlicensed.
- **KILL** (§4): every protocol ≤21/60 on both tasks → the generation axis is **closed** for base Pythia-410m under CPU protocols; all future work on this backbone is logit-readout-only. H1/H4 stay retired pending a backbone change.

---

## 3. Method

### 3.1 Backbone, bench, environment [FACT / pinned]

- **Backbone:** frozen Pythia-410m snapshot `~/workspace/.exp086_weights/pythia-410m` (the EXP108/EXP109 snapshot). `device_map="cpu"`, float32, `model.eval()`, `torch.no_grad()` around ALL generations.
- **Δθ=0 procedure (pinned):** SHA-256 over tensor bytes with **sorted `state_dict` keys**, float32 (the EXP077/EXP084/EXP108 canonical convention — the method is named explicitly to avoid the tier0.py parameter-order discrepancy documented in EXP112). Hash asserted **before the first generation and after the last**; any mismatch → RUN-INVALID. Expected pin: `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed` (LOG-331).
- **Bench:** the 60-item EXP089 bench, rebuilt verbatim via `benchmark_exp089.build_benchmark()` — the same bench EXP108's echo-path failure was measured on, so the T1 baseline is directly comparable. Provenance SHA-256 of `experiments/runs/EXP077_cone_vs_line/exp077_instance_records.json` = `47281cd3dc243369be0aa5be2345663b752cdb4a329a16a37f08da5717230585` asserted before any generation; `len(bench) == 60` asserted. Mismatch → RUN-INVALID.
- **Environment (Law #13):** torch==2.14.0+cpu, transformers==5.17.0 (the registered EXP106–EXP112 environment); numpy/sklearn versions recorded in the worksheet; `torch.manual_seed(0)` + numpy seed 0; CPU thread count set and read back via `torch.get_num_threads()`, recorded. All in the execution worksheet.
- **Law #7:** bench ground-truth labels (target entity names) are used **only** for the few-shot exemplar answers (§3.3, pinned) and never during any selection choice — and the registered metric is **parseability (format), not correctness**: a constant "A" output scores 60/60 parseable regardless of labels, so no label exposure can inflate any registered number. The parse rules (§3.4) never read labels.

### 3.2 The two tasks (pinned)

- **T1 — single-token answer (the H1 self-report shape):** 60 items. The model must emit a single letter, A or C. This is the exact output shape EXP108's elicitation gate demanded.
- **T2 — numbered outlines (the H4 planner shape):** 60 items. The model must emit numbered solution outlines. This is the exact output shape EXP109's planner-valid rule demanded.
- Item order: bench build order (indices 0–59), identical for every protocol. No shuffling, no subsampling.

### 3.3 The five protocols (pinned verbatim — Law #7: no protocol tuning after seeing results)

Each protocol is a (prompt template, decoding params) pair. All decoding is greedy (`do_sample=False`); nothing is left to tune. `{PROMPT}` = the item's full bench prompt verbatim (premise + question + option list), unchanged. Protocol families are shared across tasks: **baseline / few-shot / constrained-stop / anti-repetition / priming** — instantiated per task shape. [ASSUMPTION]

**T1 protocols (max_new_tokens=8 unless stated):**

- **T1-P1 — verbatim EXP108 baseline (the anchor / negative control) [FACT]:**
  ```
  {PROMPT}

  Question: Which option did you choose — A or C? Reply with a single letter and nothing else.
  ```
  Greedy, `max_new_tokens=4`. Expected to reproduce the echo path ([OBSERVATION] from EXP108); if it does not fail here, the environment is suspect.
- **T1-P2 — few-shot format completion:** three pinned exemplars (items 0, 1, 2 in bench build order) shown as `Q: {PROMPT_i} + question + A: {true label of item i}`, then the target item with the T1-P1 question and a trailing `A:`. The exemplar answers are the true labels of items 0/1/2 as produced by the pinned builder (deterministic); per §3.1 they cannot inflate the parseability metric. Greedy, `max_new_tokens=4`.
- **T1-P3 — explicit stop / single-token slot [new — deviation 4]:** 
  ```
  {PROMPT}

  Question: Which option did you choose? Answer with exactly one letter, A or C:
  ```
  Greedy, `max_new_tokens=1`. Only the first generated token is read. This directly addresses the EXP108 echo path: the `\n\nQuestion:` repetition cannot start inside a single token. If the first token has no alphabetic character → UNPARSEABLE (honest measurement, §3.4).
- **T1-P4 — repetition-penalty decoding:** T1-P1 template + `repetition_penalty=1.2`, `no_repeat_ngram_size=3`, greedy, `max_new_tokens=4`. Directly addresses the repetition attractor.
- **T1-P5 — completion priming (single-token analogue of list-priming):**
  ```
  {PROMPT}

  Question: Which option did you choose — A or C? Reply with a single letter and nothing else.

  The single-letter answer is:
  ```
  Greedy, `max_new_tokens=4`. Ending mid-sentence forces continuation instead of a fresh generation restart (the EXP108 echo began with a restart: `\n\nQuestion:`).

**T2 protocols (max_new_tokens=160 unless stated):**

- **T2-P1 — verbatim EXP109 planner (the anchor) [FACT]:**
  ```
  {PROMPT}

  Plan: Before answering, write 4 distinct numbered solution outlines (1. 2. 3. 4.), each a different approach to answering the question. Each outline must be 40 words or fewer. Do not give the final answer yet.
  ```
  Greedy, `max_new_tokens=160`. Expected to reproduce the planner-loop attractor ([OBSERVATION] from EXP109).
- **T2-P2 — few-shot format completion:** two pinned exemplars (items 3, 4 in bench build order), each shown as the T2-P1 template followed by four hand-written numbered outlines (pinned verbatim below — format demonstrations; their correctness is irrelevant to the registered parseability metric), then the target item with the T2-P1 template. Greedy, `max_new_tokens=160`.
  - Pinned exemplar outlines (verbatim, both exemplars):
    ```
    1. Restate the question's ordering constraint in my own words.
    2. Check each premise statement against the two candidate entities.
    3. Eliminate the entity contradicted by any premise.
    4. Name the remaining entity as the answer.
    ```
- **T2-P3 — explicit stop / exactly-two-outlines [new — deviation 4]:**
  ```
  {PROMPT}

  Plan: Before answering, write exactly 2 distinct numbered solution outlines (1. 2.), each a different approach to answering the question. Each outline must be 40 words or fewer. Stop after outline 2. Do not give the final answer yet.
  ```
  Greedy, `max_new_tokens=96`. Directly addresses the EXP109 runaway-repetition mode by shrinking the target structure and stating the stop explicitly.
- **T2-P4 — repetition-penalty decoding:** T2-P1 template + `repetition_penalty=1.2`, `no_repeat_ngram_size=3`, greedy, `max_new_tokens=160`.
- **T2-P5 — list priming (trailing "1."):**
  ```
  {PROMPT}

  Plan: Before answering, write 4 distinct numbered solution outlines, each a different approach to answering the question. Each outline must be 40 words or fewer. Do not give the final answer yet.

  1.
  ```
  Greedy, `max_new_tokens=160`. The model continues an already-started list instead of initiating one.

**Execution order (pinned, deterministic):** protocols P1→P5; within a protocol, T1's 60 items then T2's 60 items; items in build order. Total: 5 × 2 × 60 = **600 generations**. **No pilot phase; no early abandonment:** every protocol completes all 120 generations regardless of intermediate results — a protocol scoring 0/60 early still finishes (Law #9: no selection on partial data).

### 3.4 Parse rules (mechanical, pinned — a script, not human judgment)

- **T1 parse rule (one rule, all T1 protocols) [FACT — identical to EXP108's rule]:** strip the output; take the first alphabetic character; uppercase it; parseable iff it is `A` or `C`; otherwise (including no alphabetic character at all) UNPARSEABLE. Total deterministic function.
- **T2 parse rule (one rule, all T2 protocols) [FACT — identical to EXP109's planner-valid rule]:** scan the output left to right; record the first occurrence position of each literal marker `1.`, `2.`, `3.`, `4.`; outline_k = substring from the end of marker `k.` to the start of the next marker in position order (or end of output), stripped; drop empties and exact duplicates; parseable iff **≥ 2 distinct non-empty outlines** remain.
- **Deterministic re-parse (Law #14-grade anti-self-deception):** the parse script is a pinned pure function of the raw generation logs. The execution lane runs it **twice** and asserts byte-identical parse tables; any mismatch → RUN-INVALID (apparatus bug, not a verdict).
- **Per-generation exceptions:** caught per generation, logged with traceback, scored UNPARSEABLE for that item (never silently dropped, never aborts the run). If exceptions exceed 60/600 (10%) → RUN-INVALID (apparatus bug).

### 3.5 Repetition-attractor blocklist diagnostic [OBSERVATION — descriptive only]

Per protocol per task, report the fraction of outputs containing (a) the literal substring `\n\nQuestion:` (the EXP108 echo path), or (b) the literal substring `Write a list of the possible answers` (the EXP109 loop phrase). This diagnoses *which* failure mode each protocol hits. **No decision branch reads this diagnostic.** (Deviation 6: the dossier framed the blocklist as a "guard"; read literally as a gate it would invalidate the very measurements H7 exists to take — a protocol hitting the attractor *is the data*. It is therefore a diagnostic, not a gate.)

### 3.6 RUN-INVALID branches (apparatus-level only — Law #4)

- Backbone hash mismatch (pre or post, §3.1) → RUN-INVALID.
- Bench provenance mismatch or `len(bench) != 60` → RUN-INVALID.
- Global generation failure: >90% of all 600 generations are empty strings, or per-generation exceptions exceed 10% → RUN-INVALID (environment/code bug, not a protocol property).
- Deterministic re-parse mismatch → RUN-INVALID.
- **A protocol scoring 0/60 is a VALID measurement** — never RUN-INVALID. Individual protocol failure is the scientific content of this run.

---

## 4. Decision bars with statistical license

Let r1(p), r2(p) = parseable counts (of 60) for protocol p on T1, T2. Let T1-CLEAR = {p : r1(p) ≥ 48}, T2-CLEAR = {p : r2(p) ≥ 48}.

- **CONTINUE:** T1-CLEAR ≠ ∅ **and** T2-CLEAR ≠ ∅ → H1-revival and H4-revival lanes licensable as NEW hypotheses, each naming its clearing protocol and each carrying its own elicitation-failure gate (e.g., the EXP108 `n_unparseable ≥ 7` gate).
- **PIVOT:** exactly one of T1-CLEAR, T2-CLEAR non-empty → revival licensable only for the cleared axis; the other axis stays retired pending its own separately pre-registered validation.
- **HELD:** no clearance, and max(r1, r2) over protocols in 22–47 → partial elicitation; licenses nothing, retires nothing.
- **KILL:** max r1 ≤ 21 **and** max r2 ≤ 21 (every protocol ≤21/60 on both tasks) → generation axis closed for base Pythia-410m under CPU protocols; all future work on this backbone is logit-readout-only.

**Statistical license [FACT — all values independently computed for this draft]:**
- The bars are **operational thresholds on observed rates**, not p-value tests (there is no natural null for "reliable enough to use").
- 48/60: one-sided 95% Wilson lower bound = **0.7030**. A CONTINUE therefore licenses revival-lane *attempts* (each with its own elicitation gate doing the final licensing); it does **not** license the claim "true rate ≥ 80%."
- **Selection-bias disclosure:** the decision takes the max over 5 protocols. If every protocol's true rate were 0.70, P(any ≥48/60) ≈ **0.25** — a CONTINUE can arise from a ~0.70-true-rate protocol; the revival lane's own gates absorb this. If every true rate ≤ 0.60, false-CONTINUE ≈ **0.004**. The HELD zone (22–47) absorbs the ambiguous middle where selection bias bites hardest.
- 21/60: one-sided 95% Wilson upper bound = **0.4558 < 0.50**. A KILL therefore licenses the claim "no tested protocol reaches 50% true parseability." Moreover P(all five protocols ≤21/60 | every true rate ≥ 0.5) ≈ **5×10⁻¹⁰** — *under the independence approximation*: the five protocols share the same 60 items and the same frozen backbone, so outcomes are positively correlated, and the correlation-robust upper bound is the single-protocol value P(Bin(60,0.5) ≤ 21) ≈ **0.014**. The KILL's license rests on the per-protocol Wilson upper bound (0.4558), which requires no independence assumption.
- **Deviation 1 (from the dossier, recorded):** the dossier's "<50% observed → KILL" (i.e., ≤29/60) has a one-sided 95% Wilson upper bound of **0.5879** — *not* below 0.50 — so the "true rate < 50%" claim would be unlicensed under the dossier's bar. Refined to ≤21/60 (35%), which licenses it. The dossier's "≥80% → CONTINUE" operational bar is kept, with the CI disclosure above.

---

## 5. Falsification decision tree

```
bench provenance + len==60
 ├─ mismatch → RUN-INVALID (apparatus)
 └─ ok → backbone LOG-331 pin (pre)
     ├─ mismatch → RUN-INVALID
     └─ ok → 600 generations (5 protocols × 2 tasks × 60 items; no early abandonment)
         ├─ >90% empty OR >10% exceptions → RUN-INVALID
         └─ ok → backbone pin (post); mismatch → RUN-INVALID
             └─ ok → deterministic re-parse ×2; mismatch → RUN-INVALID
                 └─ ok → r1(p), r2(p) for all p; T1-CLEAR, T2-CLEAR
                     ├─ both non-empty → CONTINUE (name the clearing protocols)
                     ├─ exactly one non-empty → PIVOT (name the cleared axis)
                     ├─ max ≤ 21/60 on both tasks → KILL (generation axis closed)
                     └─ else → HELD
```

No other branches exist. No re-runs, no larger item sets, no post-hoc bars, no protocol modifications mid-run (Law #4, Law #9).

---

## 6. Cost and honesty

- **$0 CPU, ~2–4h**: 600 generations on frozen Pythia-410m CPU (T1: ≤8 new tokens; T2: ≤160). Calibrated against EXP109 (108 generations in 20.9 CPU-min). No GPU contact. Generation is the *subject* of measurement here — this is the licensed exception to the program's logit-readout posture, fenced to this apparatus question.
- **Honesty ledger:** (a) the 80% bar is operational, not a true-rate claim (Wilson lower 0.7030 disclosed); (b) a CONTINUE licenses revival *attempts* with their own gates, not successful H1/H4; (c) the finding is backbone-specific (base Pythia-410m, CPU, greedy) — no claim about other models, instruction-tuned variants, or sampling regimes; (d) a KILL retires the axis for this backbone only.

---

## 7. What H7 does NOT claim

1. Parseable output ≠ reasoning, ≠ honesty, ≠ capability. A protocol clearing 80% has produced *formatted text*, nothing more.
2. A CONTINUE does not validate any H1/H4 hypothesis — only the *elicitation method*. Revival lanes are new hypotheses with their own pre-registrations and gates.
3. No claim beyond base Pythia-410m under CPU greedy protocols (one snapshot, one environment).
4. The blocklist diagnostic (§3.5) is descriptive; it licenses no verdict and no protocol ranking.
5. **Novelty: N1 — Known Combination.** Apparatus validation is infrastructure; no new mechanism is claimed. (Law #10.)

---

## 8. Deviations from the dossier (complete list)

1. **KILL bar refined:** dossier's "<50% observed → KILL" (≤29/60) → **≤21/60 (35%)**, because the dossier's bar cannot license the "true rate < 50%" claim (Wilson upper 0.5879 ≥ 0.50); the refined bar does (upper 0.4558). Mathematically required.
2. **HELD zone added** (best in 22–47/60, no clearance): the dossier had no middle verdict; the selection-bias analysis shows the 0.65–0.75 true-rate zone needs an absorbing verdict rather than a forced CONTINUE/KILL.
3. **PIVOT added** for split-task clearance (one task clears, the other doesn't): the dossier's binary CONTINUE/KILL didn't cover it; H1 and H4 need different elicitation shapes, so per-axis licensing is the honest outcome.
4. **Two new protocols added** — T1-P3 (explicit stop, `max_new_tokens=1`) and T2-P3 (exactly-2-outlines with explicit stop): the dossier's four families address repetition but none directly tests the *runaway/echo-restart* failure mode with an explicit stop condition, as the brief requires. T1-P4's repetition penalty also addresses the attractor; the stop protocols are the cleanest test.
5. **T2 uses the full 60-item bench**, not a 20-item pilot: the bench is mechanical (build order) and the per-protocol n=60 is needed for the Wilson-licensed bars; a 20-item pilot would leave the KILL bar unlicensed.
6. **Blocklist is a diagnostic, not a gate:** the dossier's "Law #14-grade degeneracy guard" framing, read literally as a gate, would invalidate the measurements H7 exists to take (a protocol hitting the attractor *is the data*). Implemented as a descriptive [OBSERVATION]; apparatus-level RUN-INVALID branches are in §3.6 instead.
7. **Two-task structure specified** (T1 single-token + T2 numbered-outlines): the dossier said "K protocols × 60 bench items" without specifying which downstream task shape the protocols serve; H1 needs single-token answers and H4 needs numbered outlines, so both are tested — required for the CONTINUE to license both revivals.

---

## 9. Boundary

Independent Law #14 review of this exact file is a separate lane. No experiment number is minted by this draft. Execution, if ever launched, is a CEO decision under a minted number. This lane stops here.
