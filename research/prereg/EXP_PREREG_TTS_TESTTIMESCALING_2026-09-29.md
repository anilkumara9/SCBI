# Pre-registration: TTS — Test-Time Scaling by Margin-Verified Best-of-N in the Frozen Pythia-410m

**Lane:** LOG-4720 (pre-assigned). **Family:** D of the paradigm-break
sprint (LOG-4693). **Gate:** LOG-4719 (PASS, conditional). **License:**
EXP113 (LOG-4585, apparatus CONTINUE — EVALID protocols P2 (few-shot)
and P5 (priming) clear 60/60 on the T1 single-token-answer shape:
generation on this backbone is *validatable*, so the generation
channel is not dead as an apparatus); the frontier's scaling-law
observations (program records: LLM-Monkeys log-linear coverage;
self-consistency +17.9pp; ∇-Reasoner 71.2→80.4% on MATH-500, verified
LOG-185; Meta-Reasoner +9–12% at −28–35% time); [THEOREM] best-of-N
with a calibrated verifier dominates greedy in expectation.

**$0 CPU. Δθ=0 by construction.** This pre-registration licenses a
$0 CPU pilot only — **it is not a steering claim and no autonomous
capability is licensed by it.** The pilot measures
*verifier-selection gain at matched budget* — whether the frozen
model's own margin carries selection value — not reasoning,
not steering. Draft only; licenses nothing until the launch chain
(independent Law #14 review — whose generation-channel
construct-validity ruling is the pre-launch tripwire — →
fix-verification → CEO launch decision → execution under a minted
number).

**Pre-reg decision record (bench caveat, gate §3):** the bench is the
60-item EXP107 template-decorrelated bench (four balanced 15-item
cells crossing phrasing × template word-family; registered bench pin
`e91b302f41f641c74e56957e526efcd4866bac62d134e157defe0a4cdd49e4f5`),
rebuilt verbatim via
`experiments/runs/EXP107_templatectrl/build_exp107_bench.py`. **No
larger bench is licensed by this pre-reg.** Generality beyond the 60
pinned items is barred (§10).

---

## 0. The breaking point (read first)

Conjunctive. Any miss → **apparatus-void or RUN-INVALID as stated,
hypothesis UNTESTED** (Law #9 ordering: guards → backbone pin →
bench provenance pin → EVALID gate (elicitation audit) → Stage 1
(calibration) → raw-record hash-pin (Stage 1) → Stage 2 (sampling +
selection) → raw-record hash-pin (Stage 2) → McNemar → decision):

(a) **Δθ=0** — backbone LOG-331 parameter hash
    `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed`
    (sorted `state_dict` keys, float32, tensor bytes — the
    EXP077/EXP084/EXP108 canonical convention) pinned before the
    first generation and re-pinned after the last; any mismatch →
    apparatus-void.
(b) **Elicitation validity** — the P2 few-shot protocol is pinned
    (§3.3); EXP109's elicitation-failure gate, carried verbatim at
    the registered 10% rule: `60 − n_valid ≥ 6` → **RUN-INVALID
    (elicitation failure)** before any metric is read. Item valid
    iff the greedy generation is parseable AND ≥ 1 of the 16
    samples is parseable (§3.4). The generation apparatus failed;
    this is not evidence about scaling.
(c) **Verifier-calibration pre-gate** — Stage 1 point-biserial
    correlation r_pb(margin, greedy-correctness) ≥ 0.30 (pinned,
    Law #4 — §3.5); miss → **RUN-INVALID** (the test measured the
    verifier, not the scaling); Stage 2 is never licensed.
(d) **Budget control** — the random-selection arm is present and
    its outcome is reported regardless of the margin arm's result;
    a run without it → apparatus-void (the verdict would measure
    the budget, not verification).
(e) **No training, no weight mutation** — pure forwards through a
    frozen model in eval mode (`model.eval()`,
    `torch.no_grad()` around ALL generations and embedding
    forwards); the executor contains no optimizer and no loss.
    The verifier is the registered cosine statistic — never a
    trained head (Law #7).
(f) **G4 instrument-health** (carried from H6 §3.3): max − min over
    the cosine values < 1e-4 → **RUN-INVALID (instrument deaf)**,
    not a verdict. A KILL must mean the instrument worked and
    found nothing.

[DEFINITION] The registered cosine decision statistic (H1 §3.3 /
H6 §3.3, verbatim): candidate entities E1 = `tuple[0]` (the target
entity), E2 = `tuple[-1]` (the foil); option texts `" " + E1` and
`" " + E2` (leading space); the executor asserts
`encode(" "+E)` is exactly one token on the real Pythia tokenizer
for every item — any failure → RUN-INVALID (items are NOT
silently dropped); option embeddings = frozen Pythia-410m layer-20
final-token hidden state of the single-token option text;
`score(E) = cosine(state_emb, option_emb)`; decision =
argmax(score(E1), score(E2)); ties (exact float equality) → E2;
**margin** = `|cos(E1) − cos(E2)|`.

[DEFINITION] The verifier application (this protocol, §3.5): for
item i and generated sample s, the verifier state text is
`item['prompt']` verbatim + `" "` + `gen_{i,s}.strip()`; the
state embedding is the layer-20 final-token hidden state of that
text; `margin_{i,s}` and `vote_{i,s}` are the registered statistic
applied to that state. The margin-selected arm picks
`s* = argmax_s margin_{i,s}` (ties → lowest sample index) among
the item's parseable samples; its vote is `vote_{i,s*}`.

## 1. Hypothesis (one falsifiable sentence)

[HYPOTHESIS] On the frozen Pythia-410m, at matched sampling budget,
margin-verified best-of-N selection (N=16, verifier = the
registered cosine margin statistic, no trained verifier) beats
greedy decoding by ≥ +10pp (paired McNemar one-sided p ≤ 0.05)
on the 60-item EXP107 template-decorrelated relational bench;
if the gain is < +4pp at N=16, the TTS axis is dead for this bench
class.

### 1.1 Why this experiment exists

[INTERPRETATION] The frontier's numbers live on the test-time
axis (self-consistency +17.9pp, ∇-Reasoner, Meta-Reasoner,
LLM-Monkeys coverage). The program's one attempt (EXP056: +4pp,
p=0.25, n.s.) was unpowered and unregistered. This family does
not steer, inject, decode snapshots, or compose plan text. It
*samples* (generation as measurement, not as elicitation of
content) and *selects* by a frozen, untrained statistic. The new
quantity is **verifier-selection gain at matched budget** —
unmeasured in the program's history — and the design carries its
own executioners: the Stage-1 calibration gate (§3.5), the
random-selection control (§3.6), and the elicitation-failure
gate (breaking point (b)). If the margin is noise, Stage 1 kills
the family for ~30 minutes of CPU. If the gain is budget, the
random-selection arm kills the verifier story.

### 1.2 The generation-channel construct (for Law #14's ruling)

[OPEN → for Law #14 to rule] The dossier (LOG-4693 §D) wrote the
generation channel off (EXP115/116/123 killed
*elicitation-as-readout* and entity-name generation). This
protocol's position is that EXP113's EVALID apparatus
(LOG-4579→4585, CONTINUE) built exactly the construct-validity
machinery those deaths were missing: protocols P2 and P5 clear
60/60 on the T1 single-token-answer shape, and the protocol pins
P2 (§3.3) with EXP109's elicitation-failure gate (breaking point
(b)). Two disclosures for the ruling: (i) EXP113's clearance was
on the EXP089 bench with letter answers; this protocol applies P2
to the EXP107 bench with entity-name answers — the transfer is
validated in-protocol by the elicitation-failure gate, not
assumed; (ii) EXP113's clearance metric was parseability
(format-following, not correctness) — correctness is this
protocol's metric, and a constant-but-parseable output stream is
a valid measurement (scored as accuracy), not an apparatus
failure. If Law #14 rules the generation-channel construct still
invalid, the family never launches (pre-launch kill, recorded;
gate §2).

## 2. Exact question and the decision it changes

[QUESTION] At matched generation budget, does margin-verified
best-of-N (N=16) beat greedy by a registered margin on the
relational bench class?

| best-of-N (margin-selected) vs greedy, paired on valid items | Decision |
|---|---|
| **Δ ≥ +10pp AND McNemar(margin, greedy) one-sided p ≤ 0.05 AND McNemar(margin, random) one-sided p ≤ 0.05** | **CONTINUE** — margin-verified test-time scaling works on this bench class; the program's first capability-positive $0 result. Tagged search-and-selection, never steering or reasoning (§7). |
| **Correlate signature fires** (Δ_original ≥ +10pp AND Δ_flipped ≤ 0, §3.7) with primary CONTINUE met | **HELD** — domain-set-correlate signature; CONTINUE withheld pending a domain-decorrelated bench. |
| **Δ < +4pp at N=16** | **KILL** — the TTS axis is dead for this bench class; stop proposing TTS pilots here. |
| **+4pp ≤ Δ < +10pp, or beats greedy but not random-selection** | **HELD** — recorded, no re-test without a new gate. The budget account (margin-select ≈ random-select) is recorded: the gain is tokens, not verification. |
| **Stage 1 calibration fails** (r_pb < 0.30) | **RUN-INVALID** — the test measured the verifier, not the scaling; the N=16 samples are never burned. |
| **Elicitation-failure gate fires** (60 − n_valid ≥ 6) | **RUN-INVALID** — apparatus finding (EXP109's defect class), not a verdict about scaling. |
| **Law #14 rules the generation-channel construct invalid** | **Never launches** — pre-launch kill, recorded. |

Δ is in percentage points on the valid-item set
(`n_valid ≤ 60`). The McNemar license is one-sided exact on the
paired 2×2 table (b = margin-right/greedy-wrong, c =
margin-wrong/greedy-right) — the H4/H14/H19 program standard.
Critical values verified at drafting (§4). The bars are Law #4 —
verbatim from the gate (LOG-4719 §2); no recalibration.

## 3. Method

### 3.1 Frozen backbone

- Backbone weights are **frozen**: Δθ = 0. Snapshot:
  `~/workspace/.exp086_weights/pythia-410m`; environment:
  `~/workspace/.venv-exp077` (torch 2.14.0+cpu, transformers
  5.17.0, numpy 2.5.3, sklearn 1.9.1, accelerate 1.15.0 — the
  registered EXP107–EXP113 environment).
- The backbone parameter hash (sorted `state_dict` keys,
  float32, tensor bytes) is recorded **before the first
  generation and after the last** and compared against the
  LOG-331 pin
  `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed`.
  Any mismatch → RUN-INVALID, quarantine, no metric may be read
  (Law #6, Law #13).
- Determinism pins (Law #13): `model.eval()` before all
  forwards; `torch.no_grad()` around ALL generations and
  embedding forwards; `device_map="cpu"`; float32; torch/numpy
  seeds pinned; sampling RNG = `torch.Generator` with
  per-(item, sample) seeds `20260929_4720 + item_idx*100 + s`
  (s ∈ {0…15}, 0-based); CPU thread count set and read back via
  `torch.get_num_threads()`, recorded in the worksheet.

### 3.2 Bench (pinned)

The 60-item EXP107 template-decorrelated bench, rebuilt verbatim
via `experiments/runs/EXP107_templatectrl/build_exp107_bench.py`
(deterministic; no RNG; no model calls): four balanced 15-item
cells crossing phrasing × template word-family —
(A-first, original-words), (A-first, flipped-words),
(C-first, original-words), (C-first, flipped-words). Item order:
bench build order (indices 0–59). No shuffling, no subsampling.

- **Registered bench pin:** SHA-256 of the canonical JSON
  serialization =
  `e91b302f41f641c74e56957e526efcd4866bac62d134e157defe0a4cdd49e4f5`
  (verified at drafting, LOG-4720). Mismatch at execution →
  RUN-INVALID.
- Candidate entities per item: E1 = `tuple[0]` (the target
  entity), E2 = `tuple[-1]` (the foil) — the H6 §3.2 pin.
- Labels (`tuple[0]`) are used **at metric time only** (Law #7),
  except the 3 pinned P2 exemplar answers (§3.3), which are
  demonstrations, never test-item labels in any selection.

### 3.3 Elicitation protocol — T1-P2 few-shot (pinned verbatim)

The EVALID-cleared protocol (EXP113/H7, T1-CLEAR, 60/60): three
pinned exemplars (items 0, 1, 2 in bench build order) shown as

    Q: {prompt_i}
    A: {E1_i}

then the target item as

    Q: {prompt_target}
    A:

where `{prompt}` is the item's `prompt` field verbatim
(premise + `" Question: Who is higher in rank? Answer:"`, no
trailing space — H6 §3.4) and `{E1_i}` is the exemplar's true
label (`tuple[0]`). Decoding: greedy arm `do_sample=False`;
sample arms `do_sample=True`, temperature = 1.0 (pinned),
`max_new_tokens=8` (the T1 single-token-answer shape). The 16
samples use the per-(item, sample) pinned seeds (§3.1).

**Clearance-transfer disclosure (for Law #14, §1.2):** EXP113
cleared P2 on the EXP089 bench with letter answers; this
protocol applies it to the EXP107 bench with entity-name
answers. The transfer is not assumed — it is validated
in-protocol by breaking point (b).

### 3.4 Parse rule and item validity (pinned)

**Parse rule (deterministic, total):** strip the generation;
take the first whitespace-delimited token; strip trailing
punctuation (`.,;:!?'"`); uppercase. Parseable iff the result
equals `E1.upper()` or `E2.upper()`; the vote is the matched
entity (ties impossible — one token). Otherwise UNPARSEABLE.
Per-generation exceptions are caught, logged with traceback,
and scored UNPARSEABLE (never silently dropped, never aborts
the run).

**Item valid** iff the greedy generation is parseable AND ≥ 1
of the 16 samples is parseable. `n_valid` = number of valid
items. **Elicitation-failure gate:** `60 − n_valid ≥ 6` (>10%,
the H1/H4 10% rule) → **RUN-INVALID (elicitation failure)**
before any metric is read.

### 3.5 Stage 1 — verifier calibration (the cheap falsifier)

On the greedy arm only (~30 min, ~6% of the budget): for each
valid item, compute `margin_i` (the §0 verifier application on
the greedy sample's state) and `correct_i = [vote_greedy ==
label]`. The calibration statistic is the point-biserial
correlation r_pb(margin, correctness) over the valid items.

- **Pass:** r_pb ≥ 0.30 (pinned, Law #4) → Stage 2 licensed.
- **Fail:** r_pb < 0.30 → **RUN-INVALID** — the test measured
  the verifier, not the scaling; the N=16 samples are never
  burned. This is the falsification test the dossier buried in
  its breaking point, foregrounded as a stage gate.

Stage-1 records (greedy generations, verifier embeddings,
margins, votes, the calibration statistic) are hash-pinned
(§3.8) before Stage 2 is licensed — Stage 2 cannot be tuned on
Stage 1.

### 3.6 Stage 2 — scaling (only if Stage 1 passes)

Per valid item, 16 samples (960 generations) + the greedy
generation. Arms:

- **Margin-selected best-of-N:** `s* = argmax_s margin_{i,s}`
  over the item's parseable samples (ties → lowest sample
  index); accuracy = mean over valid items of
  `[vote_{i,s*} == label]`.
- **Random-selected best-of-N (the budget control):** the same
  16 samples, uniform pick among the parseable ones (seeded
  per item: `20260929_4720 + item_idx`); accuracy likewise.
  The random-selection arm isolates verifier-selection from
  budget — if margin-select ≈ random-select, the gain is
  tokens, not verification.
- **Greedy:** the Stage-1 greedy vote; accuracy likewise.

Primary metric: Δ = acc(margin) − acc(greedy) in percentage
points on the valid-item set; McNemar one-sided exact on the
paired tables. The random-selection arm's outcome is reported
regardless of the margin arm's result (breaking point (d)).

### 3.7 The EXP126 threat — domain-set-correlate branch (pinned)

EXP126 reclassified the decodability CONTINUEs as
domain-set-detector correlations: what looked like entity
reading was set-structure reading. The same threat applies to
the margin verifier: a margin calibrated *through* the
domain-set correlate passes the Stage-1 check while selecting
domain-conforming completions — the bench score rises while
cognition doesn't. The bench's template-decorrelated cells are
the in-protocol instrument for this threat.

**Registered branch:** for every verdict, report per-cell Δ —
Δ_original (the 30 original-word items) and Δ_flipped (the 30
flipped-word items). If the correlate signature fires —
**Δ_original ≥ +10pp AND Δ_flipped ≤ 0** — while the primary
bars would give CONTINUE, the verdict is **HELD** instead,
tagged "domain-set-correlate signature — CONTINUE withheld
pending a domain-decorrelated bench." This rule can only
downgrade CONTINUE to HELD, never upgrade; it is the
mechanical reading of gate §8(5).

### 3.8 Raw-record hash-pin specification (defect class (b))

Before the decision statistic is computed — and before any
decision branch — the executor hash-pins (SHA-256) the raw
artifacts, in two stages per the Law #9 ordering. A metric
minted without its stage's pin → apparatus-void:

- **Stage-1 pin:** per-item greedy generation texts, parse
  results, verifier state texts, state embeddings (or their
  hashes), the 120 cosine values, margins, votes, the
  calibration statistic r_pb, the elicitation audit
  (n_valid, the 10% gate computation).
- **Stage-2 pin:** per (item, sample) generation texts, parse
  results, verifier state texts, cosines, margins, votes; the
  margin-argmax indices; the random-selection indices and
  seeds; the 120 option-embedding records (texts, BPE
  assertion results, embeddings); the per-arm accuracy tables;
  the McNemar contingency tables.
- Both stages: the environment manifest (versions, thread
  count read back, backbone LOG-331 pin values pre/post,
  bench provenance pin), the append-only console log.

The Stage-1 pin is computed before Stage 2 is licensed; the
Stage-2 pin before the McNemar tables are computed. The
SHA-256 values are recorded in the worksheet before the
decision statistic exists.

### 3.9 Guards and what is NOT measured here

- G4 instrument-health (§0(f)); BPE single-token assertion
  (§0); option-embedding integrity (120 fresh forwards,
  §3.6 hash discipline applies).
- **No semantic-direction arms** (EXP077/EXP094 territory —
  barred). **No injection of any kind** — TTS injects nothing;
  it samples and selects.
- **No probe, no head, no training.** Nothing is fitted; the
  verifier is the registered statistic (Law #7 clean).
- **No plan composition** (EXP124/H21 territory — barred).
- **No cross-field comparisons.** The Δ stands alone;
  generality beyond Pythia-410m and the 60 pinned items is
  barred.
- **No finite differences.** There is no finite-difference
  estimator anywhere in this protocol.

## 4. Decision bars with statistical license

The decision statistic is Δ = acc(margin-selected) −
acc(greedy) in percentage points on the valid-item set, with
the McNemar one-sided exact license (H4/H14/H19 program
standard). Critical values verified at drafting (exact binomial
tails, computed a priori — not from any run):

| (b, c) | net | one-sided exact p |
|---|---|---|
| (5, 0) | +5 | 0.0312 ✓ (H4's row) |
| (6, 0) | +6 | 0.0156 ✓ |
| (7, 1) | +6 | 0.0352 ✓ |
| (6, 1) | +5 | 0.0625 ✗ |
| (8, 2) | +6 | 0.0547 ✗ |

Bars (Law #4, verbatim from the gate):

- **CONTINUE:** Δ **≥ +10pp** AND McNemar(margin, greedy)
  one-sided p **≤ 0.05** AND McNemar(margin, random) one-sided
  p **≤ 0.05** — margin-verified selection beats greedy and
  beats the budget control. (Unless the correlate signature
  fires → HELD, §3.7.)
- **KILL:** Δ **< +4pp** at N=16 — the TTS axis is dead for
  this bench class. Coherence note: a net gain ≤ 4 items can
  never reach p ≤ 0.05 one-sided (even (4,0) → 0.0625), so the
  KILL bar sits below the significance floor by construction.
- **HELD:** Δ ∈ [+4pp, +10pp), or beats greedy but not
  random-selection (the budget account), or the correlate
  signature fires — recorded, no re-test without a new gate.

**Power analysis (a priori, n=60):** the +10pp bar = 6 items
net. It is significant only when the gain is concentrated
(e.g., (6,0) p=0.0156; (7,1) p=0.0352); a diffuse +10pp
(e.g., (12,6)) fails p ≤ 0.05. The bar is demanding by
registration — that is the point: EXP056's +4pp n.s. is beaten
by registration and power, not by repetition. The gate memo's
"(6,0)→p=0.03125" was the two-sided value; this pre-reg uses
the one-sided license (0.015625), the program standard —
deviation 1, §9.

Statistical license: the bars are registered properties of the
measurement itself (defect class (a): Δ and the McNemar tables
are executor-computed, never handwritten). The gate's
quantitative prediction bands (from program records only):
null (verifier adds nothing / curve flat) → Δ < +4pp;
budget account → margin-select ≈ random-select (both ≥
greedy +4pp); TTS hypothesis → Δ ≥ +10pp with both McNemar
gates; calibration failure → RUN-INVALID at Stage 1.

## 5. Falsification decision tree

All numbers executor-produced. Law #9 ordering: guards →
backbone pin → bench provenance pin → EVALID gate
(elicitation audit: parse, item validity, the 10% gate) →
Stage 1 (calibration: greedy margins vs correctness, r_pb) →
raw-record hash-pin (Stage 1) → Stage 2 (960 samples +
verifier forwards + selection) → raw-record hash-pin
(Stage 2) → McNemar → decision.

| Tree node | Required result |
|---|---|
| Bench provenance: EXP107 bench rebuilt, canonical JSON SHA-256 `e91b302f…dd49e4f5` | **PASS** — mismatch → RUN-INVALID |
| BPE assertion: `encode(" "+E)` exactly one token for all 120 option texts | **PASS** — failure → RUN-INVALID (items NOT dropped) |
| G4 instrument-health: max − min of cosine values ≥ 1e-4 | **PASS** — miss → RUN-INVALID (instrument deaf) |
| Backbone LOG-331 pin (pre) | **PASS** — `ec276abe…e0ed` |
| Elicitation audit: parse per §3.4; item validity; `60 − n_valid < 6` | **PASS** — the 10% gate; violation → RUN-INVALID before any metric |
| Stage 1: r_pb(margin, greedy-correctness) ≥ 0.30 | **PASS** — miss → RUN-INVALID; Stage 2 never licensed |
| Raw-record hash-pin (Stage 1) | **PASS** — defect class (b) |
| Stage 2: 960 samples + 960 verifier forwards + 120 option forwards; batch order free across items | **DONE** — exit code 0 |
| Backbone LOG-331 pin (post) | **PASS** — identical; Δθ=0 |
| Raw-record hash-pin (Stage 2) | **PASS** — defect class (b) |
| Budget control present and reported | **PASS** — breaking point (d) |
| **Δ and the two McNemar tables** | **§4 bars** — CONTINUE / KILL / HELD |
| Per-cell diagnostic: Δ_original, Δ_flipped | **§3.7 branch** — correlate signature → HELD |

Any tree node miss → apparatus-void or RUN-INVALID as
stated, hypothesis UNTESTED, no Δ minted.

## 6. What this protocol explicitly does NOT do

- **No steering claim.** Nothing is injected, nothing is
  steered; the capability scoreboard stays at zero.
- **No reasoning claim.** A CONTINUE is tagged
  search-and-selection (§7), never "the model reasons
  better."
- **No new verifier.** The margin is the registered cosine
  statistic (H1/H6); no head is trained, no label enters
  any selection (Law #7).
- **No plan text.** No composition near the prompt
  (EXP124/H21 territory).
- **No bench built for readout.** The bench is the pinned
  EXP107 template-decorrelated bench; no new bench is
  constructed.
- **No cross-bench inheritance.** The calibration check runs
  on the relational bench itself (§3.5); the EXP126 threat is
  fenced per-cell (§3.7).
- **No cross-field comparisons.** Generality beyond
  Pythia-410m and the 60 pinned items is barred.

## 7. Cost and honesty

Stage 1: 60 generations + 60 verifier forwards (~30 min).
Stage 2: 960 generations + 960 verifier forwards + 120
option-embedding forwards. Total ≈ **1,020 generations +
1,140 embedding forwards ≈ 2–4h CPU, $0**. No training, no
labels in the loop, no GPU.

**Honest frame (verbatim):** this is a search-and-selection
question, not a capability-of-reasoning claim — capability
scoreboard stays at zero; a CONTINUE here would be the
program's first capability-positive $0 result, tagged as
margin-verified best-of-N beating greedy on this bench class,
never "the model reasons better"; no generality beyond
Pythia-410m and the pinned bench.

## 8. What TTS does NOT claim

- Not steering. Selection never becomes a steering claim —
  the scoreboard's "zero positive autonomous-steering
  signals" headline is untouched either way.
- Not reasoning. The margin selects; it does not improve
  cognition. A CONTINUE is search-and-selection.
- Not generality. One model (Pythia-410m), one bench (60
  pinned EXP107 items).
- Not a mechanism account. The Δ measures verifier-selection
  gain; it does not explain *why* the margin calibrates.
- Not a resurrection. EXP056 (fenced, not repeated),
  H4/PTTSC (differentiated, not revived), EXP115/116/123
  (generation-channel deaths — the construct-validity
  distinction is Law #14's to rule), EXP124/H21, H22, H23,
  G1, the static-snapshot paradigm (LOG-4693) stay dead;
  TGA (EXP127) stays CONTINUE'd and is not re-gated; DSF
  (EXP128) stays UNTESTED; CLP (EXP129) stays KILLed — TTS
  assumes nothing about any of them.
- Novelty: N1 — Known Combination (§7.1.6 of the program
  record).

## 9. Deviations from the dossier and the gate (complete list)

1. **Gate §5 "(6,0)→p=0.03125" → this pre-reg §4:** the
   gate's value was the two-sided McNemar tail; the pre-reg
   uses the one-sided license (0.015625), the H4/H14/H19
   program standard. The bar ("p ≤ 0.05") is unchanged.
2. **Gate §2 "beats random-selection-of-N by a pinned margin"
   → this pre-reg §2/§4:** the pinned margin is specified as
   McNemar(margin, random) one-sided p ≤ 0.05 (same license
   as the primary).
3. **Gate §3 "pinned correlation threshold" → this pre-reg
   §3.5:** pinned at r_pb ≥ 0.30 (Law #4 pre-reg choice, not
   derived from program records — stated, not smuggled).
4. **Gate §8(5) "the pre-reg must name this branch" → this
   pre-reg §3.7:** the EXP126 correlate branch is specified
   mechanically (Δ_original ≥ +10pp AND Δ_flipped ≤ 0 →
   HELD, CONTINUE withheld).
5. **Gate §3 left the verifier application implicit → this
   pre-reg §0/§3.5:** the verifier state is pinned as the
   item prompt verbatim + `" "` + the stripped sample; the
   margin-selected arm picks the argmax-margin parseable
   sample (ties → lowest index).
6. **Gate left item validity implicit → this pre-reg §3.4:**
   item valid iff greedy parseable AND ≥ 1/16 samples
   parseable; the 10% elicitation-failure gate is the
   registered H1/H4 rule (`60 − n_valid ≥ 6`).
7. **Gate §4 named the EVALID apparatus → this pre-reg
   §1.2/§3.3:** the P2 clearance-transfer (EXP089 letter
   answers → EXP107 entity answers) is disclosed as a named
   limitation; the transfer is validated in-protocol by the
   elicitation-failure gate, and Law #14's ruling is the
   tripwire.
8. No other deviations. The gate's design assertions, bars,
   breaking point, and seventh item are honored verbatim.

## 10. Boundary

- This pre-reg licenses a $0 CPU pilot only. **No GPU contact,
  no steering claim, no autonomous capability** is licensed.
- No generality beyond frozen Pythia-410m and the 60 pinned
  EXP107 items is licensed.
- The Δ is one scalar per arm on the pinned bench only — it
  says nothing about other benches, models, or N.
- If any breaking-point item fails, the apparatus is void —
  no re-parse rescue, no post-hoc threshold argument, no
  verifier redefinition.
- The seventh-item record (gate §7) stands: the constraining
  kills are snapshot-instrument, semantic-direction, or
  content-readout results; none ever measured
  verifier-selection gain; TTS is unfollowed in this form and
  never killed. H17, S5, H12, bench re-reading,
  EXP117/118/119/121/123/124 reruns, entity-name generation,
  H22's generality, H23's identity interpretation, the TGA
  program (CONTINUE'd), the DSF soft-spot premise (UNTESTED),
  and the CLP adaptive-pursuit premise (KILLed) stay dead
  (or untouched, as marked).
