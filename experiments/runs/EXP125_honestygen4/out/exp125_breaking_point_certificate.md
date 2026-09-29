# Breaking-point certificate — EXP125 (H22/HONESTY-GEN4) bench 4

**Lane:** LOG-4679 (construction). **Protocol:**
`~/workspace/SCBI/research/prereg/EXP_PREREG_H22_HONESTYGEN4_2026-09-29.md`
(launch-ready: Law #14 SIGN-WITH-FIXES LOG-4676, FIX-1 byte-verified
LOG-4677, doc-consistency LOG-4678).

**Certificate verdict:** `PASS`

Conjunctive breaking point (protocol section 0): any miss on (a),
(b)-G-C3, or (c) -> apparatus-void, hypothesis UNTESTED, no number
minted, no execution. All three hold on the evidence below.

## 1. No item screening (EXP121 lesson)

- Exactly 60 base items emitted; all 60 enter the bench (`len(bench) == 60` asserted).
- Flip selection is by sorted position within each phrasing group (even
  positions flip), never by item content.
- No per-item filtering of any kind at construction: no model calls, no RNG,
  no item dropped, reweighted, or re-selected. The builder asserts
  `len(flip_ids) == 30` and `len(bench) == 60` at build time.
- Cell counts verified: A-first/original 15, A-first/flipped 15,
  C-first/original 15, C-first/flipped 15.

## 2. (a) Single-token entity assertion — FINAL sets, real tokenizer

Tokenizer: `/home/hatch/workspace/.exp086_weights/pythia-410m` (tokenizer-only; no weights loaded, no forwards).
Encoding: `encode(" "+E, add_special_tokens=False)` exactly per the H6 section 3.3 pin.
Result: **21/21 single-token** — zero multi-token entities.

| entity | token id | entity | token id |
|---|---|---|---|
| Heart | 15382 | Rain | 21398 |
| Lung | 37792 | Snow | 18724 |
| Liver | 17687 | Storm | 25005 |
| Bone | 34257 | Wind | 17054 |
| Brain | 24114 | Ice | 22078 |
| Eye | 27919 | Frost | 37838 |
| Ear | 40627 | Cloud | 18189 |
| Hand | 10535 | Thunder | 27926 |
| Foot | 12867 | Mist | 31872 |
| Rib | 31641 | Dew | 45797 |
| Skin | 37019 | | |

Any multi-token entity would have restarted construction, not patched it;
none was found, so no restart occurred.

## 3. (b) Template-decorrelation discipline

### G-C1 pure-template detector (diagnostic)

- T predicts A-first iff the first premise sentence uses family-1
  (` outshines `). Score: **30/60**, gate bar <= 36/60 -> **PASS**.
- A trip is recorded, not verdict-bearing (the honesty metric cannot read it).

### G-C2 entity-rank correlation (diagnostic)

- Flattened entity-index sequences bench-1 vs bench-4 (canonical order,
  240 elements each). Pearson: **-0.0198**, |Pearson| = 0.0198, bar <= 0.10 -> **PASS**.
- Computed against bench-1's builder records only; no bench-1 labels or
  embeddings enter the analysis (Law #13 fence).

### G-C3 byte-exact decomposition (FULL gate)

- `QUESTION_SUFFIX` byte-exact: True
- prompt == premise + QUESTION_SUFFIX on all 60 items: True
- Deterministic re-run byte-identical: True
- **G-C3 verdict: PASS**

### [-3:] token-tail identity (defect class 5)

- All 60 composed contexts tokenized with the real tokenizer; final three
  ids asserted == `[32, 37741, 27]` (`?`, `ĠAnswer`, `:`).
- Result: **60/60 match** -> **PASS**.

## 4. (c) Law-#7 own label pin

- Builder's meaning-preserving construction docstring (in
  `build_exp125_bench.py`): the flip preserves the ranking meaning
  (A > B > C [> D]), so `tuple[0] = A` is the highest-ranked entity on
  all 60 items.
- Independent per-item assertion (`verify_cells`, mechanical, separate from
  the prose): `tuple[0]` appears whole-word in the first premise sentence
  iff A-first — **60/60 pass** (whole-word match; "Ear" is a substring of
  "Heart", so the assertion is not raw-substring). Label convention
  `y = 1 iff A-first` — 60/60 pass.
- Labels enter only this pin, never the apparatus (protocol section 3.7).

## 5. Disjointness (no entity reuse)

- Bench-4 entities (21): Heart, Lung, Liver, Bone, Brain, Eye, Ear, Hand, Foot, Rib, Skin, Rain, Snow, Storm, Wind, Ice, Frost, Cloud, Thunder, Mist, Dew
- Bench 1 (planets/elements, protocol-cited set), bench 2 (canonical JSON,
  10 entities), bench 3 (canonical JSON, 10 entities): set-membership check
  -> **zero overlap** (asserted in `verify_cells`).
- ID prefixes: `exp125_*` — no collision with `exp077_`/`exp107_`
  (bench 1), `exp120_` (bench 2), `exp122_` (bench 3), `exp092_`.

## 6. Determinism (Law #13)

- Builder: no RNG, no model calls, pure string construction.
- Rebuild pin: `4995545cae3b662567166d1549952e304d19ced014431bb48637f4b5e27c6cf7`
- Fresh re-run pin: `4995545cae3b662567166d1549952e304d19ced014431bb48637f4b5e27c6cf7` — **match**.
- Canonical JSON on disk (`out/exp125_bench4.json`) sha256: `4995545cae3b662567166d1549952e304d19ced014431bb48637f4b5e27c6cf7` — **match**.

## 7. Hashes

| artifact | sha256 |
|---|---|
| out/exp125_bench4.json | `4995545cae3b662567166d1549952e304d19ced014431bb48637f4b5e27c6cf7` |
| build_exp125_bench.py | `b65ceb5e3edc7643037cd57ebf856be0d60fa01b9e85ec939a51b62dba464e3a` |
| certify_exp125_bench.py | `971f7c677d3762338269ca077e372c6e37cca4bfb03757b093fd9d22f27531dd` |
| tokenizer.json | `c24618a1b3e6a38167beff1c72cffd126c3a66254347304b50547d12c5f25624` |

## 8. Environment manifest

- python 3.12.3, Linux-7.0.0-38-generic-x86_64-with-glibc2.39
- transformers 5.17.0
- tokenizer source: `/home/hatch/workspace/.exp086_weights/pythia-410m`

## 9. Verdict

**PASS** — all conjunctive breaking-point elements hold: (a) 21/21
single-token on the final sets; (b) G-C1 30/60 diagnostic PASS, G-C2
|Pearson|=0.0198 diagnostic PASS, G-C3 FULL PASS, [-3:] identity 60/60;
(c) Law-#7 own label pin on record; no item screening; 60 items, four
balanced 15-item cells; disjointness asserted; determinism re-run hash
match. Execution is **licensed to proceed** under a minted experiment
number (CEO decision).
