# Breaking-point certificate — EXP126 (H23/WITHIN-DOMAIN) bench 5

**Lane:** LOG-4687 (construction). **Protocol:**
`~/workspace/SCBI/research/prereg/EXP_PREREG_H23_WITHINDOMAIN_2026-09-29.md`
(launch-ready: Law #14 SIGN, zero fixes, LOG-4686).

**Certificate verdict:** `PASS`

Conjunctive breaking point (protocol section 0): any miss on the §3.2
design assertions, the single-domain audit, the single-token assertion,
G-C1, G-C2, G-C3, or the position-scramble gate -> construction-fate
RUN-INVALID, hypothesis UNTESTED, no number minted, no execution.
All hold on the evidence below.

## 1. No item screening (EXP121 lesson)

- Exactly 60 base items emitted; all 60 enter the bench (`len(bench) == 60` asserted).
- Flip selection is by sorted position within each phrasing group (even
  positions flip), never by item content.
- No per-item filtering of any kind at construction: no model calls, no RNG,
  no item dropped, reweighted, or re-selected. The builder asserts
  `len(flip_ids) == 30` and `len(bench) == 60` at build time.
- Cell counts verified: target-first/original 15, target-first/flipped 15,
  target-last/original 15, target-last/flipped 15.
- Labels 30/30 (y=1 iff tuple[0] ∈ S1); hop x label 15/15/15/15.

## 2. (a) Single-token entity assertion — FINAL set, real tokenizer

Tokenizer: `/home/hatch/workspace/.exp086_weights/pythia-410m` (tokenizer-only; no weights loaded, no forwards).
Encoding: `encode(" "+E, add_special_tokens=False)` exactly per the H6 section 3.3 pin.
Result: **14/14 single-token** — zero multi-token entities.

| entity | token id | entity | token id |
|---|---|---|---|
| Cat | 12441 | Horse | 27950 |
| Dog | 21048 | Cow | 18544 |
| Bear | 25743 | Pig | 40274 |
| Wolf | 17698 | Rat | 18194 |
| Fox | 11024 | Bat | 15103 |
| Lion | 26571 | Bird | 25080 |
| Tiger | 31822 | Fish | 23645 |

Any multi-token entity would have restarted construction, not patched it;
none was found, so no restart occurred.

## 3. Single-domain audit (the discriminative gate)

- Every entity mention on every bench-5 premise was audited against the
  14-animal set with whole-word matching (`verify_cells`).
- Result: **0/60 premises contain any out-of-domain entity**.
- A domain-set detector has no input here by construction: this is the
  gate that makes H23 discriminative.

## 4. Template-decorrelation discipline

### G-C1 pure-template detector (diagnostic)

- T predicts y=1 iff the first premise sentence uses family-1
  (` towers over ` / ` crouches under `). Score: **28/60**, gate bar <= 36/60 -> **PASS**.

### G-C2 entity-rank correlation (diagnostic)

- Flattened entity-index sequences bench-3 vs bench-5 (sorted-by-ID
  canonical order, 240 elements each). Pearson: **+0.0018**, |Pearson| = 0.0018,
  bar <= 0.10 -> **PASS**.
- Bench-5 uses the S1/S2-interleaved GC2 index (label-agnostic canonical
  order) so the check measures entity-assignment independence, not
  label-structure similarity; bench-5's label pattern (Y1+7) and hop rule
  (hash-based) are structurally independent of bench-3's.
- Computed against bench-3's builder records only; no bench-3 labels or
  embeddings enter the analysis (Law #13 fence).

### G-C3 byte-exact decomposition (FULL gate)

- `QUESTION_SUFFIX` byte-exact: True
- prompt == premise + QUESTION_SUFFIX on all 60 items: True
- Deterministic re-run byte-identical: True
- **G-C3 verdict: PASS**

### Position-scramble gate (discriminative)

- P predicts y=1 iff the target occupies the first final sentence position.
  Score: **30/60**, gate bar <= 36/60 -> **PASS**.
- Final position balanced 15/15 within each label class by construction
  (identical flip x label pattern across phrasing groups).

## 5. (c) Law-#7 own label pin

- Builder's meaning-preserving construction docstring (in
  `build_exp126_bench.py`): the flip preserves the ranking meaning
  (A > B > C [> D]), so `tuple[0] = A` is the highest-ranked entity on
  all 60 items.
- Label derivation rule: **y=1 iff tuple[0] ∈ S1 = {Cat, Dog, Bear, Wolf, Fox}**,
  y=0 iff tuple[0] ∈ S2 = {Lion, Tiger, Horse, Cow, Pig} — a property of the
  target's identity within a single domain (explicit design deviation from
  the H5/H16 label definitions, per the H23 pre-reg §2 disclosure).
- Independent per-item assertion (`verify_cells`, mechanical, separate from
  the prose): `y == (tuple[0] in S1)` — **60/60 pass**. `target_subset`
  field matches the label on all 60 items.
- Labels enter only this pin and the pre-registered head targets, never the
  apparatus (protocol section 3.7).

## 6. Disjointness and independence

- ID namespace: `expb5_*` — no collision with `exp107_`/`exp077_` (bench 1),
  `exp120_`/`expb2_` (bench 2), `exp122_`/`expb3_` (bench 3), `exp125_` (bench 4).
- Verb families (`towers over`/`crouches under`, `looms over`/`cowers beneath`)
  contain no prior-bench verb-family substring (asserted per item).
- Entity vocabulary: the 14-animal set overlaps bench-3's animal set
  {Lion, Tiger, Bear, Wolf, Fox} by protocol design (the H23 gate pins the
  14-animal vocabulary); independence of the entity *assignments* is via
  hash-selected entities with salt `exp126` (vs bench-3's `exp122`),
  verified by the G-C2 gate above.

## 7. Determinism (Law #13)

- Builder: no RNG, no model calls, pure string construction.
- Rebuild pin: `444e40260b4c71c512db72db2c5d2555b31ffbbd8db2eedcf8a3a46fddbb0e8a`
- Fresh re-run pin: `444e40260b4c71c512db72db2c5d2555b31ffbbd8db2eedcf8a3a46fddbb0e8a` — **match**.
- Canonical JSON on disk (`out/exp126_bench5.json`) sha256: `444e40260b4c71c512db72db2c5d2555b31ffbbd8db2eedcf8a3a46fddbb0e8a` — **match**.

## 8. Hashes

| artifact | sha256 |
|---|---|
| out/exp126_bench5.json | `444e40260b4c71c512db72db2c5d2555b31ffbbd8db2eedcf8a3a46fddbb0e8a` |
| build_exp126_bench.py | `9302cad0a20eac95bc92d278c8ef42d77706ac48e97db71563b347199886197e` |
| certify_exp126_bench.py | `adade0d4964d09da571fa2e5149803317ed25716154f474855884c9c26539cbd` |
| tokenizer.json | `c24618a1b3e6a38167beff1c72cffd126c3a66254347304b50547d12c5f25624` |

## 9. Environment manifest

- python 3.12.3, Linux-7.0.0-38-generic-x86_64-with-glibc2.39
- transformers 5.17.0
- tokenizer source: `/home/hatch/workspace/.exp086_weights/pythia-410m`
- Note: defect class (e) ([-3:] tokenization-identity pin) is explicitly N/A
  for H23 (protocol §6 item 4 — no logit channel, embedding-readout design).

## 10. Verdict

**PASS** — all conjunctive breaking-point elements hold: (a) 14/14
single-token on the final set; single-domain audit 0/60 out-of-domain;
G-C1 28/60 diagnostic PASS, G-C2 |Pearson|=0.0018 diagnostic PASS,
G-C3 FULL PASS, position-scramble 30/60 PASS;
(c) Law-#7 own label pin on record (y == (tuple[0] in S1), 60/60);
no item screening; 60 items, four balanced 15-item cells, 30/30 labels;
disjointness asserted; determinism re-run hash match.
Execution is **licensed to proceed** under a minted experiment
number (CEO decision).
