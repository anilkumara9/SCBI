# EXP092 — Information-Bottleneck Localization (IBL)
## (Per-layer 1-NN scan for task information in frozen Pythia-410m)

> **DRAFT PRE-REGISTRATION — UNSIGNED.** Draft 2026-09-25. This document
> licenses NOTHING. Execution requires the full launch chain: independent
> Law #14 review → signing (CEO) → bundle build → independent bundle review
> → CEO execution clearance → execution. **Current position: DRAFT.**

> **SUCCESSION BANNER.** EXP091
> (`experiments/protocols/EXP091_CLM8B_ADAPTATION_V3_PREREG_SIGNED.md`,
> immutable, digest `747bb6a5…417b`) is **NOT superseded** — its KILL verdict
> on the zero-shot free-lunch hypothesis was ADOPTED on the record (LOG-361
> execution, LOG-362 independent verdict review: 31/60, p=0.4487, instrument
> responsive). EXP092 is a NEW experiment, not a repair: it asks the prior
> question EXP091 did not ask — *where, if anywhere,* the frozen residual
> stream carries task information — and adjudicates the program's biggest
> interpretive fork (bridge artifact vs misplaced information).

**Experiment number:** EXP092 (verified free 2026-09-25; no EXP092 file existed
in `experiments/protocols/`).
**Draft date:** 2026-09-25.
**Parent dossier:** `research/innovation/SPRINT_2026-09-25_SUMMIT.md`
(Candidate 1 — IBL; Law #15 block implemented faithfully, neither strengthened
nor weakened).
**Parent protocol:** EXP091 SIGNED (LOG-357); real execution KILL adopted
(LOG-361/362).

---

## 0. Lineage — IBL's place in the program

**The fork.** Two observations stand in tension:
- (a) The option-informed bridge rescues +16.67pp (EXP070, p=0.001953) and
  +10pp (EXP077, p=0.03125), with power localizing outside the tested concept
  subspace (EXP078). But the bridge is option-informed → Law #7 violation →
  demoted to rescue artifact, not autonomous mechanism (LOG-204).
- (b) EXP091 killed zero-shot cosine scoring of frozen layer-20 embeddings
  (31/60, p=0.4487) — but it read **only layer 20**.

The fork: is the bridge's power *misplaced information* (task signal present
in the frozen stack, just not at layer 20 — EXP091 looked in the wrong place),
or *construction artifact* (the bridge's label-informed construction
manufactures its own signal; the information is absent everywhere)? No program
experiment has scanned layers for task information. IBL is the cheapest
decisive test of this fork.

**What IBL decides.** CONTINUE → the "misplaced information" program survives
and every subsequent readout experiment re-targets to l*. KILL → the
misplaced-information hypothesis dies as a *licensed kill* (calibrated null,
not inconclusive); the LOG-204 bridge-as-artifact interpretation is
strengthened; the output-side program PIVOTs toward construction-artifact
forensics under a new number.

**What IBL is not.** It is not a capability experiment (no decision rule is
tested, no accuracy is claimed). It is diagnostic-adjudicative: a localization
scan whose output is a *layer index* (or a kill). Novelty N1 (dossier §3):
linear probing across layers is old; the *use* — artifact forensics on the
bridge — is the differentiated claim.

---

## 1. Precise question

Is max_l Î(h_l; y) > 0 at any layer l of frozen Pythia-410m on the 60-item
relational bench, where Î is 1-nearest-neighbor leave-one-out classification
accuracy on the layer's embeddings, tested against a stratified permutation
null?

---

## 2. Background (why this test exists)

- EXP091 (LOG-361/362, ADOPTED): zero-shot cosine scoring over frozen
  Pythia-410m/layer-20 embeddings on 60 novel relational items: 31/60
  (51.67%), p=0.4487; margins noise-scale (mean 6.8e-4); instrument responsive
  (G4 spread 0.0803 ≫ 1e-4). A genuine null from a working instrument. But the
  readout was at a single, program-conventional layer (20 of 24).
- The bridge lineage (EXP070/077): option-informed positive controls rescue
  decision accuracy where every static geometric variant is decision-flat
  (ΔM=0, p=1.0). The program has never determined whether the bridge's signal
  reflects task information *present* in the frozen representations (but
  misplaced relative to layer 20) or *manufactured* by the label-informed
  construction.
- Mathematical license (dossier): Fano's inequality — classification error
  lower-bounds conditional entropy H(y|h_l), so above-chance 1-NN accuracy
  certifies I(h_l; y) > 0 **without density estimation**. The permutation null
  controls finite-sample bias exactly (valid at any n, including n=60).

---

## 3. EXPLICIT SCOPE FENCE — Δθ=0 only

- **Licensed:** read-only extraction of hidden states from frozen Pythia-410m
  (all 24 layer outputs, final-token position, premise-only state text);
  1-NN classification and permutation statistics computed offline on the
  extracted embeddings. No training, no weight updates, no adapters, no
  gradient steps of any kind. θ_after = θ_before; the FrozenBackboneGuard
  hashes state_dict before/after (Law #6/Law #13).
- **OUT OF SCOPE:** any trainable probe, any fine-tuning, any new benchmark
  construction, any claim about capability or mechanism beyond the registered
  localization decision.
- **A CONTINUE does not license a capability claim.** It licenses only a
  follow-up readout experiment re-targeted to l* (new experiment number).
- **Any PIVOT redesign requires a NEW experiment number and the founder's
  explicit license where trainable apparatus is involved.**

---

## 4. Artifact lineage (read-only; nothing modified)

- `experiments/runs/EXP077_cone_vs_line/exp077_instance_records.json`:
  `47281cd3dc243369be0aa5be2345663b752cdb4a329a16a37f08da5717230585`
  (per EXP091 §4 record; pinned as provenance).
- `experiments/runs/EXP091_clm8b_falsifier_v3/out/exp091_report.json`:
  the adopted null (31/60, p=0.4487) this experiment is conditioned on.
- Frozen weight snapshot reused from LOG-331
  (`experiments/runs/EXP086_amplifier/weights/pythia-410m/`); state_dict
  SHA-256 `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed`.
- Per-item, per-layer embeddings are re-extracted from the frozen snapshot
  (CPU, read-only); the registered benchmark construction is §6.

---

## 5. Law #7 (zero leakage) statement

No training occurs, so no labels flow into any trained component. Labels (the
target entities y_i) are used only to *score* the 1-NN classifier and to
*construct* the permutation null — standard evaluation. The 1-NN classifier
itself is untrained (a distance computation). The state text is pinned to the
premise sentences only (§6), excluding the question and the option list, as in
EXP091.

---

## 6. Design

**Benchmark (Law #9: no new benchmark construction).** EXP092 reuses EXP091's
§6 bench contract exactly: the deterministic output of the verbatim-ported
repaired EXP077 benchmark builder — 60 items (30 planet + 30 element; 2-hop /
3-hop; 30 "A-first" + 30 "C-first" phrasing). The executor asserts
`len(bench) == 60` at build time. Before any extraction, the executor asserts
the SHA-256 of
`experiments/runs/EXP077_cone_vs_line/exp077_instance_records.json` equals
`47281cd3dc243369be0aa5be2345663b752cdb4a329a16a37f08da5717230585`;
mismatch → RUN-INVALID.

**Labels.** y_i = the target entity of item i (the correct answer to "who is
higher in rank?"). K = number of distinct target entities in the bench
(K=10 in the EXP091 construction: Mars, Venus, Jupiter, Saturn, Mercury,
Iron, Gold, Silver, Bronze, Steel — **asserted at build time from the bench,
not hardcoded**). Theoretical chance = 1/K; the permutation null supersedes
it.

**Embeddings.** Frozen Pythia-410m, **all 24 layer outputs** (l = 0..23),
final-token hidden state of the premise-only state text (same state-text
definition as EXP091 §6: substring from `"Premise:"` up to excluding
`" Question:"`). One forward pass per item yields all 24 layers
(`output_hidden_states=True`); 60 forward passes total. float32, CPU,
`device_map="cpu"`, `model.eval()` + `torch.no_grad()` (Law #13 pins).

**Primary statistic (decision-driving; fixed before any inspection —
Law #9).** Per layer l: 1-nearest-neighbor leave-one-out accuracy a_l.
For each item i, NN(i) = argmin_{j≠i} d_cos(h_l^{(i)}, h_l^{(j)}) with cosine
distance d_cos = 1 − cosine similarity (program-standard geometry);
predict ŷ_i = y_{NN(i)}; a_l = (1/60) Σ_i 1[ŷ_i = y_i].

**Permutation null (stratified; exact at any n).** Per layer: 1,000
permutations of the labels, **stratified by (domain × phrasing)** — 4 strata
(planet/A-first, planet/C-first, element/A-first, element/C-first), 15 items
each; labels permuted within strata. This preserves entity-frequency and
phrasing structure, so the null controls exactly the confounds the program
already knows about (positional bias, Law #14 F2 lineage). Null accuracy
distribution → per-layer p-value
p_l = (1 + #{null_acc ≥ a_l}) / 1001; q95_l = 95th percentile of the null.

**Secondary statistics (reported, NOT decision-driving).**
- (S1) KSG kNN-MI estimate between PCA-reduced embeddings (≤20 dims) and
  labels per layer — exploratory; the n=60 sample-size limitation is
  declared and it cannot move the tree.
- (S2) LM log-prob baseline (dossier §6 mandate): frozen-model
  p(correct option | premise) accuracy on the 60 items — the program's most
  obvious never-run baseline; reported for context (if at chance, the bench
  is genuinely hard; if above chance, the geometry program was looking in
  the wrong place).

**Guards (all FATAL/INVALID on failure):**
- **G1 (frozen backbone):** state_dict SHA-256 before/after extraction must
  equal the LOG-331 snapshot hash
  `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed` →
  Δθ=0 verified; mismatch → RUN-INVALID.
- **G2 (null calibration):** 1,000 stratified permutations executed per layer;
  the full null distribution recorded per layer. If any layer's null has
  zero variance (degenerate — uncalibratable) → RUN-INVALID.
- **G3 (bench integrity):** N=60 asserted at build time; phrasing balance
  30/30 asserted (carried from EXP091 G3); label set K asserted and
  reported.
- **G4 (mode stamp):** the run report MUST stamp `"mode": "mock"|"real"`;
  `from_pretrained` MUST pin `device_map="cpu"` literally (carried from
  EXP091; the LOG-331 `accelerate` deviation fix is registered in
  `requirements.txt` at build time, not post-hoc).

---

## 7. Registered bar and decision tree

Bonferroni threshold across 24 layers: α_B = 0.05/24 ≈ **2.083e-3**.
Effect-size gate (dossier): (a_l − q95_l) ≥ **0.10** (10pp).

| Condition (checked in order) | Verdict | Licenses next |
|---|---|---|
| G1/G2/G3 fail; N≠60; extraction crash | **RUN-INVALID** | Withheld, not a verdict. |
| ∃ l≠20: p_l < α_B **and** (a_l − q95_l) ≥ 0.10 | **CONTINUE** | The "misplaced information" program survives. Redirect readout program to l* = argmax over qualifying layers of (a_l − q95_l). Follow-up readout at l* under a NEW experiment number. Does NOT license capability claims. |
| (a) p_20 < α_B with (a_20 − q95_20) ≥ 0.10 — signal at the already-tested layer; **or** (b) ∃ l: p_l < α_B but (a_l − q95_l) < 0.10 — Bonferroni-significant but sub-threshold effect | **PIVOT** | (a): the misplacement framing is wrong — PIVOT to readout-instrument forensics (why does 1-NN see what EXP091's cosine scoring missed?) under a NEW number. (b): signal real but underpowered — PIVOT to a powered redesign (larger N or refined statistic) under a NEW number. |
| ∀ l: p_l ≥ α_B | **KILL** | The misplaced-information hypothesis dies — licensed kill, not inconclusive (calibrated null). Strengthens the LOG-204 bridge-as-artifact interpretation. PIVOT the output-side program toward construction-artifact forensics under a NEW number. |

### 7.1 Totality note

The tree is TOTAL: every possible outcome of the registered statistics maps
to exactly one branch. The branches are checked in the order listed;
CONTINUE requires a qualifying layer *other than* layer 20 (EXP091 already
read layer 20 — a signal there is instrument forensics, not misplacement).
Ties in l* (equal margins) are broken by lower layer index, deterministically,
and reported.

---

## 8. Falsification criteria, invalidity, refusal

**Falsifies the misplaced-information hypothesis:** no layer Bonferroni-
significant (KILL). The claim "frozen Pythia-410m carries task information
about the correct answer at some layer" is rejected at family-wise α=0.05.

**RUN-INVALID (withheld, not a verdict):** weight-hash mismatch (G1);
archive-hash mismatch (§6 provenance pin); N ≠ 60; phrasing-balance assert
failure (G3); degenerate permutation null, any layer (G2); extraction crash.

**Refusal:** the execution bundle (when built) MUST refuse any run while this
protocol is unsigned; MUST refuse any flag requesting training, GPU execution,
or weight mutation; MUST refuse a real run if the signed-protocol digest
guard mismatches. Draft status confers zero license.

**Standing review rules applied to this protocol:** (i) tokenization claims
verified by real-tokenizer execution (CEO, LOG-354) — no new tokenization
claim is made here (bench reused verbatim); (ii) the primary statistic and
all bars are fixed before inspection (Law #9).

---

## 9. Budget

$0. CPU only. ~1.5 hours wall-clock: 60 forward passes (~40 min, one run
yields all 24 layers) + per-layer 60×60 distance matrices + 24×1,000
permutation scorings (seconds) + S2 baseline (~1h). No GPU contact. Weights
already on disk from LOG-331 — no download. No new artifacts beyond the run
report.

---

## 10. Why this is the cheapest falsifier

Adjudicating the program's biggest interpretive fork — bridge artifact vs
misplaced information — requires NO new benchmark (Law #9 reuse), NO
training, NO GPU, and NO new data: one 60-pass extraction plus exact
permutation statistics on CPU. A KILL here closes the "output-side room" as
an autonomous-mechanism program and redirects the lab to artifact forensics;
a CONTINUE re-targets every downstream readout experiment to l*. No other
$0 test re-orients the program as fast (dossier §5).

---

## 11. BRUTAL CAVEATS (bannered — read before interpreting any outcome)

1. **Diagnostic, not capability.** IBL tests no decision rule and licenses no
   accuracy claim. A CONTINUE means "task information is detectable at l*,"
   not "the model can decide."
2. **n=60 is small for 10 classes.** The permutation null is exact at any n
   (hence the KILL is licensed, not inconclusive), but power for a 10pp
   effect is modest — a KILL means "no detectable signal," not "provably
   zero information."
3. **1-NN is a lower bound.** Above-chance 1-NN certifies I(h_l;y) > 0 (Fano);
   at-chance 1-NN does NOT certify I = 0 — a smarter decoder could see more.
   The KILL is scoped to the registered instrument.
4. **Label = target entity.** The scan detects information about *which*
   entity is correct, not about the relational reasoning that determines it.
   Phrasing-correlated signal is controlled by stratification, not eliminated
   from the embeddings.
5. **Premise-only state text.** The question is excluded (as in EXP091); if
   task information lives only in question-conditioned representations, this
   instrument is blind to it — registered limitation, not oversight.
6. **S1/S2 cannot move the tree.** The KSG estimate and the LM baseline are
   context only (Law #9).
7. **A CONTINUE does not touch the bridge demotion.** The LOG-204 ruling
   (bridge = rescue artifact, not autonomous mechanism) stands regardless;
   IBL only decides whether *frozen representations* carry the information
   the bridge's construction may be manufacturing.

---

## 12. Launch-chain status

DRAFT (this file) → independent Law #14 review → signing (CEO) → bundle
build → independent bundle review → CEO execution clearance → execution.
**Current position: DRAFT. Nothing is licensed.**

---

*Draft prepared by the pre-registration agent, 2026-09-25, under the 30-Day
Autonomous Campaign Charter. Implements the SPRINT_2026-09-25_SUMMIT.md
Candidate-1 (IBL) Law #15 block faithfully: precise question (§1), decision
(§7), cheapest test + cost (§9), mathematical license + quantitative
prediction + breaking point (§2/§7). No numbers invented: all hashes and
bench facts carried from EXP091's signed record.*
