# H20 pre-registration: P4 repetition-penalty apparatus validation on the entity-name shape (LOG-4658)

*Lane: pre-registration drafting lane, LOG-4658 pre-assigned. $0 CPU.
Read-only on signed protocols, paper sources, and the GPU queue — this
lane drafts the pre-registration only. No experiment number is minted by
this draft; execution, if ever launched, is a CEO decision under a minted
number (the H7 precedent). Nothing signed is modified; no commit, no
push, no credentials.*

*Template: H5/H14/H19 pre-registration structure (§§0–9 + boundary).
Superseding reference: `~/workspace/SCBI/research/strategy/H20_GATE_2026-09-29.md`
(LOG-4657; the worth-it gate PASS). Source-of-truth hierarchy: the gate
memo's registered bars and design assertions are honored verbatim; this
draft pins them into executable form. Where the drafting brief's
§4 parenthetical is arithmetically inconsistent, the fix is recorded
in §8 (deviation 10) rather than silently reproduced (the LOG-4610
"no omissions" lesson; Law #4).*

---

## 0. Worth-it gate (the 6 elements, recorded before drafting)

*Recorded from the LOG-4657 gate memo (`H20_GATE_2026-09-29.md`); this
section is a faithful transcription, not a re-adjudication.*

1. **Exact question [HYPOTHESIS]:** Does the P4 repetition-penalty
   protocol — the last EXP113-cleared protocol never tested on the
   entity-name shape — elicit ≥80% mechanically-parseable entity-name
   self-reports on the EXP107 template-decorrelated bench, i.e. is there
   *any* cleared elicitation protocol that keeps the entity-name
   generation channel alive? The entity-name family has died on three
   distinct apparatuses: P2 recitation on the generation channel
   (EXP117: 0/10, enumeration attractor), P5 tail echo (EXP116 review
   lineage), and EXP121's plan-inserted logit slot on G1 mass collapse
   (22/60 items at 0.000142–0.008571 vs the 0.01 bar, n_valid=38/60 →
   RUN-INVALID).
2. **Decision changed:** ≥48/60 parseable → **CONTINUE** (licenses the
   honesty-instrument revival line with P4 as a **NEW hypothesis** under
   Law #4 — not a revival of H9/H10 — carrying its own
   elicitation-failure gate into any downstream protocol);
   n_unparseable ≥ 7 → **RUN-INVALID**, a **TERMINAL apparatus verdict**
   on the entity-name shape (the channel is dead on *all* EXP113-cleared
   protocols; the honesty-instrument line closes **permanently on this
   shape**; H1/H4's T1/T2 clearances on their own shapes untouched).
3. **Cheapest test:** 60 greedy generations on the verbatim EXP107
   `{PROMPT}` under the pinned P4 hyperparameters
   (`repetition_penalty=1.2`, `no_repeat_ngram_size=3`, greedy,
   `max_new_tokens=4`), plus the pinned mechanical parse rule and the
   elicitation-failure gate on the full 60 (no early abandonment, Law #9).
4. **Mathematical license:** EXP113's T1-P4 clearance at 58/60
   [OBSERVATION]; EXP107 bench discipline — 60 items, four 15-item cells,
   meaning-preserving template decorrelation [FACT]; EXP121's 22/60
   plan-arm G1 collapse [OBSERVATION]; the penalty-suppresses-name
   breaking mechanism [INTERPRETATION]: `repetition_penalty=1.2`
   down-weights tokens already present in the input context — including
   the entity-name tokens in the premise — biasing *against* emitting the
   entity name, compounding EXP117's enumeration and continuation
   attractors (EXP113's own T2 datum: P4=0/60 on outlines).
5. **Quantitative prediction:** P4-works → parseable rate in the
   clearance band, ≥48/60 (0.80), point analog of EXP113's 58/60.
   P4-dead → parseable rate ∈ [0, 20]/60; P(n_unparseable ≥ 7) ≈ 1 —
   the RUN-INVALID branch is the *expected* outcome and is itself the
   licensed terminal finding.
6. **Breaking point:** conjunctive — any deviation from the pinned
   bench, pinned hyperparameters, or pinned parse rule renders the
   apparatus void: **UNTESTED, no number minted, no metric read**.
   Checked at gate (LOG-4657): all 10 EXP107 entity names are
   single-token (tokenizer-only, real Pythia-410m snapshot tokenizer,
   vocab 50254) — zero multi-token entities, so the H18 pattern does not
   fire; the P4 hyperparameters are template-independent and transfer
   exactly; the template swap is the experiment's *registered unknown*,
   not an apparatus void (Law #4: new hypothesis under a
   named-but-untested protocol).

**Summit filter — MARGINAL (stated without inflation).** Apparatus
validation, not a summit move. Honest downstream value if CONTINUE: it
re-opens the *entity-name self-report* question via a generation
instrument on the EXP107 shape. It does **not** rescue EXP112's bench-2
line — H18's void was the logit-level readout on bench 2; a P4 CONTINUE
licenses a *different* instrument (generation self-report), a separate
hypothesis, not the label-free logit race H18 tested. The label-free
race stays tied at zero either way.

---

## 1. Hypothesis (one falsifiable sentence)

**[HYPOTHESIS]** The P4 repetition-penalty decoding protocol
(`repetition_penalty=1.2`, `no_repeat_ngram_size=3`, greedy,
`max_new_tokens=4`), EXP113-cleared at 58/60 on the single-letter T1
shape, elicits ≥48/60 mechanically-parseable entity-name self-reports
from frozen base Pythia-410m on the 60-item EXP107
template-decorrelated bench — i.e. the entity-name generation channel
survives under at least one EXP113-cleared protocol.

---

## 2. Exact question and the decision it changes

**Exact question [HYPOTHESIS]:** On the verbatim EXP107 bench prompts,
under the pinned P4 decoding hyperparameters, are ≥48 of 60 greedy
generations mechanically parseable as entity-name self-reports?

**Decision changed (registered before any run):**

- **CONTINUE** (§4): n_unparseable ≤ 6 (hence ≥54/60 parseable, above
  the ≥48/60 clearance bar) → the entity-name generation channel is
  alive under P4. Licenses the honesty-instrument revival line with P4
  as a **NEW hypothesis** under Law #4 (not a revival of H9/H10, not a
  continuation of any existing hypothesis), which must carry its own
  elicitation-failure gate into any downstream protocol.
- **RUN-INVALID — TERMINAL** (§4): n_unparseable ≥ 7 on the full 60 →
  the entity-name generation channel is dead on **all** EXP113-cleared
  protocols (P2 died EXP117, P5 died on tail echo, P4 dies here). The
  honesty-instrument line closes **permanently on this shape** — no
  further protocol rescue is licensed on the entity-name shape. This is
  an *apparatus* verdict (the elicitation channel is dead), not a
  hypothesis verdict, and it is the *expected* outcome under the P4-dead
  alternative — a finding, not a failure.
- **HELD** (§4): registered for protocol completeness — n_unparseable ≤
  6 but < 48/60 parseable (underpowered; closes nothing, continues
  nothing, no rescue). **Declared unreachable by arithmetic**
  (n_unparseable ≤ 6 ⇒ ≥54/60 parseable); see the fix recorded in §8
  deviation 10. No re-runs, no larger-n re-tests, no protocol tweaks —
  each would be an unlicensed gate tweak (barred).
- **RUN-INVALID — apparatus void:** any deviation from the pinned
  bench (§3.1), pinned hyperparameters (§3.3), or pinned parse rule
  (§3.4); any pin mismatch (backbone LOG-331, bench provenance);
  >10% per-generation exceptions; re-parse ×2 byte-mismatch; raw
  records missing at verdict time. UNTESTED, no number minted, no
  metric read (Law #4, Law #9).

**Primary metric (registered before any run):** count of mechanically
parseable generations among the 60 items (n_parseable; n_unparseable =
60 − n_parseable). Parseability is a deterministic function of the
generation text and the pinned candidate entity names (§3.4) — a
script, not human judgment. **The registered metric is parseability
(format), not correctness** (EXP113's Law #7 posture, carried verbatim):
a generation that names the *wrong* candidate entity still counts as
parseable. The parse rule never reads the bench labels, so no label
exposure can inflate any registered number. (Of the parseable items, a
correctness-vs-`tuple[0]` count is reported as a **decision-silent
diagnostic** to inform any licensed downstream lane — it reads no
branch of §5.)

**Binding defect classes pinned as protocol requirements (EXP119/EXP120
lessons):**
1. **No p-values are hand-written anywhere** (the bars are count bars;
   the design carries no inferential statistic — this honors the
   EXP120 lesson by construction).
2. **Raw generation records persisted and hash-pinned before any
   verdict** (EXP119 lesson, defect class 2): all 60 raw generation
   texts are persisted as artifacts, SHA-256 hash-pinned, before the
   verdict is written. Artifact-existence gate: missing or unpinned raw
   records → RUN-INVALID.
3. **Label semantics cite the builder's construction and H6's
   independent pin:** the two candidate entity names are E1 = `tuple[0]`
   (the target entity — the bench builder's meaning-preserving flip
   keeps "the ranking meaning (A > B > C [> D]) ... preserved", pinned
   independently by H6 §3.2: "E1 = `tuple[0]` (the target entity)")
   and E2 = `tuple[-1]` (the lowest-ranked entity, the H6 pin). Never a
   truncated positional comment (LOG-4625/4626 lesson).
4. **G1 does NOT apply** (§0.6, stated again so no lane re-invents it):
   G1 (per-item `sum post-softmax mass on (t1,t2) ≥ 0.01`, EXP119/EXP121)
   is a *logit-slot* validity guard for readouts that score a forward
   pass at the final position. H20 is a *generation* apparatus — no
   logit slot is read, no mass is scored. The validity apparatus is the
   mechanical-parse bar (§3.4) + the elicitation-failure gate (§4) +
   the re-parse ×2 byte-identity pin (§3.8). G1 is replaced, not
   carried.

**Law #7 posture:** bench ground-truth labels are used **only** in the
decision-silent correctness diagnostic (§2) — never during generation,
never in any selection or gating choice. The metric is parseability
(format); labels cannot move any registered number.

---

## 3. Method

### 3.1 Frozen backbone, bench, environment [FACT / pinned]

- **Backbone:** frozen Pythia-410m snapshot `~/workspace/.exp086_weights/pythia-410m`.
  `device_map="cpu"`, float32, `model.eval()` before all model contact,
  `torch.no_grad()` around ALL generations.
- **Δθ=0 procedure (pinned):** SHA-256 over tensor bytes with sorted
  `state_dict` keys, float32 (the EXP077/EXP084/EXP108 canonical
  convention). Asserted **before the first model contact and after the
  last**; any mismatch → RUN-INVALID, quarantine, no metric read.
  Expected pin: `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed`
  (LOG-331).
- **Bench:** the 60-item EXP107 template-decorrelated bench — **verbatim,
  no new bench construction** — identical provenance pins as H6 §3.2 /
  EXP112 §1 / H14 §3.1 / H19 §3.1: canonical bench-JSON SHA-256
  `e91b302f41f641c74e56957e526efcd4866bac62d134e157defe0a4cdd49e4f5`;
  npz `6cf4a8a726a2b6e4623f57d0287d95879866f77e789bcc3789fb693cf2af6a76`;
  embeddings-bytes
  `9b6e8afb091ba1edbb0311ba1d3414d34a65942c3fdecb4533b69720f2a99123`;
  ids-bytes `3669e102222719d66f61daca46ae1ac34e844e398ae433743a5b37bfc5075cb9`.
  `len(bench) == 60` asserted. **Bench-schema assertion (pinned):**
  every record has `prompt`, `premise`, `tuple` (len ≥ 2), `phrasing`,
  `id` keys; `prompt == premise + QUESTION_SUFFIX` byte-exactly, where
  QUESTION_SUFFIX = `" Question: Who is higher in rank? Answer:"`
  (EXP112-pinned). Any mismatch → RUN-INVALID.
- **Environment (Law #13):** torch==2.14.0+cpu, transformers==5.17.0,
  accelerate==1.15.0 (the pinned `device_map="cpu"` load shim,
  documented in EXP113 with no numeric effect), numpy==2.5.3;
  `torch.manual_seed(0)` + numpy seed 0; CPU thread count set and read
  back via `torch.get_num_threads()`; all recorded in the execution
  worksheet.

### 3.2 Item set [PROPOSITION]

All 60 items in bench build order (indices 0–59). No subsampling, no
pilot phase. **No early abandonment** — all 60 generations complete
regardless of partial results (EXP113's "no selection on partial
data", Law #9); the elicitation-failure gate (§4) reads on the full
60.

### 3.3 P4 protocol — pinned verbatim from EXP_PREREG_H7_EVALID §3.3 (T1-P4 line) [FACT]

- **Generation context:** the bench record's `prompt` field **verbatim**
  (`{PREMISE} + " Question: Who is higher in rank? Answer:"`). Zero new
  wording, no template wrapper, no few-shot exemplars, no priming
  suffix — the deviation from the T1 shape is the *decoding protocol
  applied to the EXP107 template*, which is the registered unknown.
- **Decoding hyperparameters (pinned, template-independent):**
  `repetition_penalty=1.2`, `no_repeat_ngram_size=3`, greedy
  (`do_sample=False`), `max_new_tokens=4`. One generation per item.
  No alternative parameter sets; nothing left to tune (Law #4).
- **Token-cap check (pinned):** every EXP107 candidate entity name is
  one token (LOG-4657 pin, §3.5), so every name fits within the 4-token
  generation cap. The cap is never the reason an item is unparseable
  by construction; items that generate past the name (continuation
  attractor) are scored by the parse rule exactly as generated.

### 3.4 Mechanical parse rule (pinned — a script, not human judgment) [FACT]

Per item, let `e1 = tuple[0]` (the highest-ranked entity, the H6 pin)
and `e2 = tuple[-1]` (the lowest-ranked entity, the H6 pin):

```
raw     = generation text (decoded tokens only — the input prompt is never part of the parse)
s       = raw.strip()                                   # strip whitespace
s       = s.rstrip('.,;:!?\'")]}')                      # pinned trailing-punctuation set
lower   = s.lower()
m1      = (lower == e1.lower())
m2      = (lower == e2.lower())
parseable  =  m1 XOR m2          # exactly one candidate matches → parseable
unparseable = otherwise          # including empty generation, both match, neither match
```

- **Decode pin (Law #13):** generation text =
  `tokenizer.decode(new_token_ids, skip_special_tokens=True)`;
  input-prompt tokens are never decoded into `raw`.
- **Empty generations** are scored UNPARSEABLE per the registered
  rule (the EXP113 precedent: T1-P4's 2 empties were scored
  UNPARSEABLE, far below the 10% RUN-INVALID threshold).
- **Deterministic:** the rule is a total deterministic function of
  (generation text, e1, e2). No judgment, no fuzzy matching, no
  substring rescue of the enumeration attractor (`\n\n1. Jupiter\n\n2.
  Mars...` is UNPARSEABLE, exactly as EXP117's 0/10).
- **Token pin (LOG-4657, checked not tripped):** all 10 EXP107 entity
  names — Mars, Venus, Jupiter, Saturn, Mercury, Iron, Gold, Silver,
  Bronze, Steel — encode as exactly one token with leading space on the
  real Pythia-410m snapshot tokenizer (e.g. `ĠMars` → [13648],
  `ĠJupiter` → [34434]). The parse rule is a text-level exact match, so
  multi-token status could not break it the way it broke EXP112's
  logit-slot readout (the H18 pattern) — stated as the checked breaking
  point, not a gate.
- **Correctness diagnostic (decision-silent):** of the parseable items,
  report `n(parseable AND names e1)` vs `n(parseable AND names e2)`.
  This diagnostic reads no branch of §5; the verdict never conditions
  on correctness.

### 3.5 Candidate-entity pins (the H6 pin, carried) [FACT]

- E1 = `tuple[0]` — the target entity under the bench builder's
  meaning-preserving construction ("the ranking meaning (A > B > C
  [> D]) ... preserved"), independently pinned by H6 §3.2
  ("E1 = `tuple[0]` (the target entity)").
- E2 = `tuple[-1]` — the lowest-ranked entity (the H6 pin).
- Single-token re-assertion carried from H19 §3.6 as a **diagnostic
  only**: `" "+e1` and `" "+e2` tokenizing to one token is asserted at
  gate (LOG-4657, done) and re-asserted at execution; unlike H19 it is
  not a firing gate here — the parse rule is text-level — but any
  deviation → apparatus-void RUN-INVALID (deviation from the pinned
  protocol), items never dropped.

### 3.6 Exception logging [FACT — EXP113 discipline]

- **Per-generation exceptions:** caught per generation, logged with
  traceback, scored UNPARSEABLE for that item (never silently dropped,
  never aborts the run).
- If per-generation exceptions exceed 10% of the 60 (i.e. >6) →
  RUN-INVALID (environment/code bug, not a protocol property; the
  EXP113 rule scaled to n=60).

### 3.7 Raw records before verdict [FACT — the EXP119 lesson, defect class 2]

All 60 raw generation texts are persisted as artifacts, SHA-256
hash-pinned, **before the verdict is written**. Artifact-existence
gate: missing or unpinned raw records → RUN-INVALID. The execution
worksheet records the pin; the report quotes it verbatim.

### 3.8 Deterministic re-parse [FACT — EXP113 discipline]

The execution lane runs the pinned parse rule **twice** over the 60
persisted generation texts and asserts **byte-identical parse tables**;
any mismatch → RUN-INVALID (apparatus bug, not a protocol property).

### 3.9 Phase-0 — none

Unlike H14/H19, H20 has no planner, no logit slot, and no composition
whose tokenization can confound a readout — the context is the
verbatim bench prompt, and the breaking points were checked at gate
(LOG-4657, tokenizer-only). The apparatus is therefore licensed
without a Phase-0 gate; the Phase-0 slot of the template is
explicitly vacated (recorded so no lane re-adds one post-hoc).

---

## 4. Decision bars with statistical license

The bars are **count bars on the full 60 items** — no inferential
statistic is registered, and none is computed (the EXP120 lesson is
honored by construction: there is no p-value to hand-write).

| Outcome | Verdict | What the region means (no weasel words) |
|---|---|---|
| n_unparseable ≤ 6 (⇒ ≥54/60 parseable, above EXP113's ≥48/60 clearance bar) | **CONTINUE** | The entity-name generation channel is alive under P4 — the first (and last untested) EXP113-cleared protocol to keep it alive. Licenses the honesty-instrument revival line with P4 as a **NEW hypothesis** under Law #4 (not a revival of H9/H10), which must carry its own elicitation-failure gate into any downstream protocol. |
| n_unparseable ≥ 7 | **RUN-INVALID — TERMINAL** | The entity-name generation channel is dead on **all** EXP113-cleared protocols (P2 died EXP117, P5 died on tail echo, P4 dies here). The honesty-instrument line closes **permanently on this shape** — no further protocol rescue is licensed on the entity-name shape. An *apparatus* verdict, not a hypothesis verdict; the *expected* outcome under the P4-dead alternative (P(n_unparseable ≥ 7) ≈ 1) — a finding, not a failure. H1/H4's T1/T2 clearances on their own shapes are untouched. |
| n_unparseable ≤ 6 **and** n_parseable < 48 | **HELD** | Registered for protocol completeness: underpowered; closes nothing, continues nothing, no rescue. **Declared unreachable by arithmetic** — with n=60, n_unparseable ≤ 6 implies n_parseable ≥ 54. The branch exists so the tree is exhaustive; the gate-memo bar structure gives the elicitation-failure gate precedence. See §8 deviation 10 for the arithmetic fix applied to the drafting brief. |

**Statistical honesty (disclosed):** with n=60 and count bars, the
design detects apparatus-grade behavior only — a protocol either keeps
the channel alive at EXP113's clearance level or trips the
elicitation-failure gate. Marginal intermediate behavior is by design
either the gate firing (RUN-INVALID) or the unreachable HELD branch —
there is no "close but not quite" region that a larger-n rescue could
salvage, and no re-runs, no protocol tweaks, no template modifications
mid-run are licensed (Law #4, Law #9).

**No rescue runs:** a RUN-INVALID is never followed by a larger-n
re-test, a different penalty value, a different stop, or a re-seed —
each would be an unlicensed gate tweak (barred). The terminal reading
is the point: the line closes on this shape.

---

## 5. Falsification decision tree

```
bench provenance + len==60 + schema (prompt/premise/tuple keys; prompt == premise + QUESTION_SUFFIX)
 ├─ mismatch → RUN-INVALID (apparatus void)
 └─ ok → backbone LOG-331 pin (pre)
     ├─ mismatch → RUN-INVALID (quarantine)
     └─ ok → P4 hyperparameters asserted byte-identical to §3.3
         ├─ mismatch → RUN-INVALID (apparatus void)
         └─ ok → full run: 60 greedy P4 generations (no early abandonment)
             ├─ per-generation exceptions >10% → RUN-INVALID (apparatus)
             └─ ok → backbone pin (post); mismatch → RUN-INVALID (quarantine)
                 └─ ok → raw generation records persisted + hash-pinned
                     ├─ missing/unpinned → RUN-INVALID (defect class 2)
                     └─ ok → deterministic re-parse ×2
                         ├─ byte-mismatch → RUN-INVALID (apparatus)
                         └─ ok → ELICITATION-FAILURE GATE on the full 60:
                             ├─ n_unparseable ≥ 7 → RUN-INVALID, TERMINAL (closes the entity-name shape line permanently)
                             └─ n_unparseable ≤ 6 → parseability check:
                                 ├─ ≥48/60 parseable → CONTINUE (P4 licenses the NEW honesty-instrument hypothesis)
                                 └─ <48/60 parseable → HELD, no rescue (arithmetically unreachable; §8.10)
```

No other branches exist. No re-runs, no larger item sets, no post-hoc
bars, no protocol modifications mid-run (Law #4, Law #9).

---

## 6. Cost and honesty

- **$0 CPU, ~10–20 min worst case:** 60 greedy generations of
  ≤4 new tokens each — trivially cheap (calibrated against EXP113's
  600 generations and EXP112's 180 forwards in ~86 s). No GPU contact.
  Zero training; backbone frozen, Δθ=0.
- **Honesty ledger:** (a) the registered metric is parseability
  (format), not correctness — a generation naming the wrong candidate
  still counts as parseable, so the CONTINUE bar can fire on a channel
  that "works" only formally; the decision-silent correctness
  diagnostic (§3.4) exists precisely to make this visible; (b) the
  elicitation-failure gate takes precedence over the clearance bar —
  if the gate fires at n_unparseable ≥ 7, the run is RUN-INVALID even
  though the raw count (≤53/60) could have been read as "close to the
  bar"; the terminal reading is the licensed one, not a pessimistic
  spin; (c) the template swap (T1-P1 letter template → EXP107
  entity-name `{PROMPT}`) is the experiment's registered unknown — a
  CONTINUE does not claim P4 "transfers" in any general sense, only
  that this one protocol-shape pair kept the channel alive; (d) the
  finding is backbone-specific (base Pythia-410m, CPU) and
  bench-specific (EXP107).

---

## 7. What H20 does NOT claim

### 7.1 The honesty fence (binding)

1. A CONTINUE licenses P4 as an **honesty-instrument** (an elicitation
   protocol that can keep the entity-name generation channel alive) —
   it does **not** license the claim that the self-reports are *honest*
   (faithful to the model's ranking belief). Honesty is the separate
   downstream hypothesis (carrying its own elicitation-failure gate),
   not H20's verdict.
2. A CONTINUE does **not** rescue EXP112's bench-2 line. H18's void was
   the logit-level honesty readout on bench 2; a P4 CONTINUE licenses a
   *different* instrument (generation self-report on the EXP107 shape),
   a separate hypothesis. The label-free race stays tied at zero either
   way.
3. Parseability ≠ correctness: the metric never distinguishes naming
   the right entity from naming the wrong one — only the pinned
   decision-silent diagnostic (§3.4) does.
4. Not reasoning, not consciousness, not deceptive intent, not
   capability beyond this bench (60 items, one backbone, one decoding
   protocol).
5. A RUN-INVALID (terminal) retires the entity-name generation channel
   on the EXP107 shape across **all** EXP113-cleared protocols — not
   the summit program, not generation in general, not H1/H4's own
   T1/T2 clearances, not test-time scaling in general.
6. A HELD (unreachable by construction) would license nothing and
   retire nothing.
7. **Novelty: N1 — Known Combination.** Repetition-penalty decoding
   and entity-name self-report elicitation are prior art; the
   combination (frozen-410m + T1-P4 hyperparameters applied to the
   EXP107 entity-name `{PROMPT}` + mechanical entity-name parse rule)
   is the contribution (Law #10).

---

## 8. Deviations (complete list — the H9-review lesson: no omissions)

**From H7's pre-registered spec (EXP113's apparatus):**
1. **Single protocol, not five:** H20 tests only T1-P4 (the one
   EXP113-cleared protocol never tested on the entity-name shape).
   P2 and P5 already died on this shape (EXP117; the EXP116 review
   lineage); P1 and P3 never cleared anything. No protocol survey is
   re-run.
2. **Bench swap:** EXP107's 60-item template-decorrelated bench (with
   the verbatim `{PROMPT}` context) instead of the EXP089 bench. This
   is the experiment's registered unknown (Law #4), not an apparatus
   void.
3. **Parse rule adapted to the shape:** H7's T1 letter rule (first
   alphabetic character ∈ {A, C}) is replaced by the entity-name
   exact-match rule (§3.4) — same mechanical character (deterministic,
   script-level, no judgment), different target alphabet. The T2
   outline rule is dropped entirely (not the tested shape).
4. **No few-shot exemplars, no priming, no template wrapper:** the
   generation context is the bare verbatim `{PROMPT}` — P4 is a
   decoding-only protocol, and its pinned definition (H7 §3.3) applies
   it to the item's full prompt unchanged.
5. **Verdicts re-licensed:** CONTINUE licenses a NEW honesty-instrument
   hypothesis (Law #4) instead of H1/H4 revivals; RUN-INVALID at the
   elicitation-failure gate is **terminal on the entity-name shape**
   (permanently closes the line) instead of per-protocol VALID-data.
6. **Phase-0 vacated** (§3.9): no planner, no logit slot, no
   composition — the breaking points were checked at gate (LOG-4657).
7. **Exceptions threshold scaled:** >6/60 (10%) instead of >60/600.

**From H6/EXP112's apparatus:** 8. **Generation channel instead of
logit readout** (the defining adaptation — this is the last channel
not yet killed on this shape). G1 is replaced by the mechanical-parse
bar + elicitation gate + re-parse pin (§2.4).

**From the drafting brief (§4 parenthetical):**
9. **(none — the brief's bars are honored verbatim as registered in
   the gate memo).**

**Drafting-lane fixes (recorded so no review re-invents them):**
10. **Arithmetic fix to the §4 middle region:** the brief's
    parenthetical "Between 41–47 parseable (n_unparseable ≤ 6 but
    < 48)" is arithmetically impossible — with n=60, n_unparseable ≤ 6
    implies n_parseable ≥ 54, so the 41–47 region cannot coexist with
    n_unparseable ≤ 6. Per the gate memo, the elicitation-failure gate
    takes precedence (RUN-INVALID at n_unparseable ≥ 7 on the full 60),
    which makes the middle region unreachable. The draft registers the
    middle region as HELD-no-rescue for tree-exhaustiveness (§4, §5)
    and declares it unreachable, rather than silently reproducing the
    inconsistency (the LOG-4610 "no omissions" lesson). If the intended
    design was instead a weaker gate (e.g. CONTINUE at ≥48 with
    RUN-INVALID only below some floor), that is a *different*
    hypothesis structure requiring a new worth-it gate — not a silent
    edit to this signed protocol (Law #4).
11. **P2-death citation correction (F2):** §0's gate-memo transcription and the draft's
    citations (deviation 1; §9's "P2 (EXP117)") attribute P2's entity-name-shape death
    to EXP117. The record shows EXP117's 0/10 was the **P5-lineage priming slot** on the
    EXP091 bench (enumeration attractor) — P2's entity-name-shape death is **EXP115**
    (few-shot recitation, RUN-INVALID — confirmed by VERDICTREVIEW_EXP116_2026-09-29:
    "P2 is dead on this shape (EXP115)"). §0 keeps the gate-memo transcription verbatim;
    this deviation carries the correction. The terminal license is unaffected (P2 is dead
    on this shape either way) — citation precision only.

**Unchanged from H7 (noted for completeness):** the pinned P4
hyperparameters (§3.3), the Δθ=0 procedure with the LOG-331 pin, the
sorted-state_dict SHA-256 convention, the re-parse ×2 byte-identity
pin, the per-generation exception-logging discipline, the "no early
abandonment / no selection on partial data" discipline, the raw-records
requirement (strengthened to hash-pinned-before-verdict per the
EXP119 lesson).

---

## 9. Boundary

- **What this protocol cannot show:** whether a parseable
  entity-name generation reflects the model's ranking belief (that is
  the downstream honesty hypothesis, separately pre-registered); why
  any individual generation parsed or failed (the attractors are
  interpretation, not measurement); whether P4 works on any other
  bench, template, backbone, or decoding regime; whether a different
  untested protocol would keep the channel alive (the terminal
  RUN-INVALID closes only the *EXP113-cleared* protocol set on this
  shape).
- **The terminal RUN-INVALID reading:** on n_unparseable ≥ 7, the
  entity-name generation channel is dead on all EXP113-cleared
  protocols — P2 (EXP117), P5 (tail echo), P4 (here). The
  honesty-instrument line closes **permanently on this shape**; no
  protocol rescue, no larger-n rescue, no parameter tweak is licensed
  on the entity-name shape. H1/H4's T1/T2 clearances (58/60,
  60/60-class on their own shapes) are **untouched** — this verdict
  never speaks about them.
- **The CONTINUE reading:** P4 kept the entity-name channel alive
  where P2 and P5 died. That licenses the NEW honesty-instrument
  hypothesis under Law #4 — carrying its own elicitation-failure gate
  — and nothing more. The label-free race stays tied at zero; the
  summit filter is MARGINAL.
- Independent Law #14 review of this exact file is a separate lane.
  No experiment number is minted by this draft. Execution, if ever
  launched, is a CEO decision under a minted number. This lane stops
  here.

---

*Pre-registration lane: LOG-4658. $0 CPU. Read-only on signed
protocols, paper sources, GPU queue. Draft ends here; the single-lane
fence is respected — this lane does not self-review, self-repair,
self-clear, or self-dispatch execution.*
