# Pre-registration: H15 — LFH-GEN2 (Label-Free Head, Generality test on a second decorrelated bench)

**Status:** DRAFT pre-registration. Licenses nothing. No model runs, no experiment number minted, no signed protocol touched, no GPU contact, no commits, no pushes. $0 CPU.
**Drafting lane:** LOG-4631 (pre-assigned). **Source:** `research/strategy/INNOVATION_SPRINT_2026-09-29_H1315.md` §H15 and `research/strategy/H15_GATE_2026-09-29.md` (worth-it gate PASS at LOG-4630 — the gate memo's six items and decision bars are binding here).
**Launch chain:** independent Law #14 review of this exact file → fix-verification (if fixes required) → CEO launch decision → execution under a minted experiment number. This lane stops at the draft.

**Governing laws:** Law #4 (no post-hoc hypothesis shifts — the bars below are binding), Law #6 (frozen backbone Δθ=0), Law #7 (zero data leakage — extended below to every model-selection decision), Law #8 (nothing retroactively un-happens — EXP111's bench-1 observation stands under any H15 outcome), Law #9 (metrics registered before any output is inspected), Law #11 (Law-#11 tagging — H15's generality hypothesis and EXP111's bench-1 observation are separate layers), Law #13 (deterministic reproducibility — seeds, hashes, environment manifest pinned below).

**Epistemological labels** per `SCBI/AGENTS.md` §5: [OBSERVATION], [HYPOTHESIS], [INTERPRETATION], [PROPOSITION], [ASSUMPTION], [FACT].

---

## 0. The breaking point (read first)

**Bench construction is the breaking point.** If any decorrelation gate in §3.1 fails → the lane dies at construction: **no head is trained, no metric is read, and no experiment number is consumed beyond what the CEO assigns.** The log records the construction failure as a construction-fate RUN-INVALID (apparatus void — the generality hypothesis received no test). If no valid second bench can be constructed, H15 is void; a contaminated-bench run is never licensed.

---

## 1. Hypothesis (one falsifiable sentence)

**[HYPOTHESIS]** EXP111's trained-head signal — a trained L2-logistic head on frozen Pythia-410m layer-20 final-token embeddings scoring 24/30 (G=0.0000) on the EXP107 template-decorrelated bench — replicates (≥20/30 with G<0.30) on a newly constructed second template-decorrelated bench under EXP111's exact pinned discipline, i.e., the trained readout extracts a template-invariant feature, not a bench-specific correlation.

### 1.1 Why this experiment exists

[OBSERVATION] EXP111 (H5/LFH-TD) is the program's single surviving positive result: a trained L2-logistic head on frozen layer-20 embeddings scored **24/30** test accuracy with **G=0.0000** on the EXP107 template-decorrelated bench — CONTINUE, bound at LOG-4567 (report §5, pre-reg §4 verbatim bars). The test set is n=30; the bar clears α=0.05 one-sided (p≈0.0014).

**Law-#11 tagging:** H15's [HYPOTHESIS] (generality of the decodability signal) and EXP111's bench-1 [OBSERVATION] are separate layers. A generality **KILL** in H15 retires the generality hypothesis only; EXP111's bench-1 observation **stands** (Law #8) and is **reclassified** as a bench-specific correlation, never erased or re-scored.

**[INTERPRETATION]** The program's single surviving positive result needs generality to matter for the summit; a bench-specific correlation cannot be built on. H15 is the cheapest licensed generality test — one fresh bench, 60 CPU forwards, the byte-verbatim EXP111 protocol.

---

## 2. Exact question and the decision it changes

**Exact question [HYPOTHESIS]:** Does EXP111's trained-head signal replicate on a newly constructed second template-decorrelated bench — new templates, new entity sets, new distractor geometry — under EXP111's exact pinned discipline (bench 2's own 60 items, own labels, own embedding extraction)?

**Decision changed:**
- **CONTINUE** the generality hypothesis: test accuracy **≥ 20/30** (one-sided binomial p ≤ 0.0494 vs chance, the EXP111 bar) **AND** **G < 0.30** → the trained head extracts a template-invariant feature; the output-side program's single positive result earns a generality claim beyond one bench.
- **Generality KILLED (H15's KILL bar):** test accuracy **≤ 18/30** (p ≥ 0.1808) **or** **G ≥ 0.30** → the bench-1 result is a bench-specific artifact; the generality hypothesis is KILLED. EXP111's bench-1 **observation stands** (Law #8) but is **downgraded**: reclassified as a bench-specific correlation, not an apparatus-level transfer claim. The output-side readout room is retired.
- **HELD** (registered): **19/30** with **G < 0.30** (the razor case) → underpowered zone; no rerun, no larger-N rescue (the EXP106 no-rescue discipline applies).

**PIVOT** does not appear in H15's outcome set.

**Not licensed:** any post-hoc cross-bench effect-size comparison (no t-test between bench-1 and bench-2 accuracies — the 30/30 split is powered for the bar, not for cross-bench effect sizes); any re-reading of bench-1 data (Law #13 fence, §8).

---

## 3. Method

### 3.1 No-generation protocol [ASSUMPTION]

H15 requires **zero generation** (the EXP108/EXP109 hard constraint carries over). The design is forward-pass-only embedding extraction for bench 2 plus vector arithmetic on archived embeddings. No autoregressive decoding appears anywhere in this design.

### 3.2 Phase 0 — Bench-2 construction (the breaking point) [PROPOSITION]

Bench 2 is **independently authored** under the EXP107 kill-test discipline (LOG-4535 bench builder is the model of the discipline, not the source of the content). The construction lane writes a deterministic builder script (no RNG, no model calls — pure string construction, like `build_exp107_bench.py`) satisfying ALL of the following. Any failure → the lane dies here per §0 (construction-fate RUN-INVALID).

1. **New vocabulary, new templates.** Two new 5-entity named sets (new domains), entity sets disjoint from bench 1's {Mars, Venus, Jupiter, Saturn, Mercury, Iron, Gold, Silver, Bronze, Steel}. Premise templates with two new verb families (family-1 / family-2) — a meaning-preserving pair documented in the builder's own docstring. **Check:** no bench-2 premise contains the substrings `" outranks "` or `" is lower than "` (bench-1's verb families); no shared template content words beyond ordinary English function words. The `QUESTION_SUFFIX` (`" Question: Who is higher in rank? Answer:"`, byte-exact per `build_exp107_bench.py`) and the `"Premise:"` framing are shared **format**, not template content.
2. **Structure parallel to bench 1:** 60 items; 2-hop and 3-hop premises; entity tuples of length 3 or 4 with `tuple[0]` = the highest-ranked entity A (the builder's meaning-preserving construction preserves "the ranking meaning (A > B > C [> D]) ... preserved"); `phrasing` ∈ {A-first, C-first} (30/30); a deterministic meaning-preserving flip applied to 15 items per phrasing (within each phrasing group sorted by id, even positions flip — the EXP107 discipline) → four balanced 15-item cells: (A-first, original) ×15, (A-first, flipped) ×15, (C-first, original) ×15, (C-first, flipped) ×15. The flip must preserve ranking meaning and re-anchor the target's sentence position per the builder's own documented rule.
3. **Design-time assertions** (mirroring `verify_cells`): 60 items; phrasing 30/30; four 15-item cells; flipped items use the OPPOSITE verb family from originals; extraction contract (`prompt` starts `"Premise:"`, `premise == prompt[:prompt.index(' Question:')]`); ID namespace distinct from bench 1 (e.g. `'expb2_...'`; assert no id starts with `'exp107_'`, all ids unique); label check per the builder's own construction: `tuple[0]` (the target) appears in the first premise sentence **iff** A-first.
4. **Labels [Law #7]:** `y = 1` iff A-first (the EXP111 label convention), carried in the per-item records alongside `phrasing` ∈ {A-first, C-first} and `flipped` ∈ {True, False}. Bench 2's own tuple[0]-label pinning procedure (see §3.4) is executed before any metric is computed.

**Decorrelation gates (quantitative, string-level, no model contact):**

- **G-C1 — pure-template detector gate:** define the pure-template rule T: predict A-first iff the first premise sentence uses family-1 (bench-2's family-1, per its own builder). Under the flip discipline T scores 30/60 by construction. **Gate: T scores ≤ 36/60** — i.e., not above chance at α=0.05 one-sided (P(X ≥ 37 | 60, 0.5) ≈ 0.047). A score above the bar means the bench is template-decodable → contaminated → construction failure.
- **G-C2 — entity-rank correlation gate:** let `r1`, `r2` be the flattened entity-index sequences (the vocabulary-index triples/quads, zero-padded to length 4) of bench 1 and bench 2 in canonical item order. **Gate: |Pearson(r1, r2)| ≤ 0.10.** Catches accidental structural copying of bench 1's entity assignments. (G-C2 compares bench-2's construction against bench-1's builder records for this design check only — it feeds no bench-1 labels or embeddings into the analysis; Law #13 fence §8.)
- **G-C3 — template-decomposition pin:** the bench-2 builder's template decomposition is independently pinned (the EXP107 equivalent of `QUESTION_SUFFIX` byte-exact + canonical-order construction), so the meaning-preserving flip can be independently verified from the builder code.

If G-C1, G-C2, or G-C3 fails → **the item dies at bench construction; no head is trained; the log records the construction failure.** A further apparatus breaking point applies at execution: determinism re-fit pass fails or train/test ID overlap → RUN-INVALID (the EXP111 §3.4/§3.3 discipline).

### 3.3 Phase 1 — Bench-2 embedding extraction (fresh backbone contact) [PROPOSITION]

Unlike EXP111's primary (archived embeddings, zero backbone contact), bench 2's embeddings are extracted fresh:

- **Embedding site:** `hidden_states[20]`, final token, float32, CPU — frozen Pythia-410m, layer 20. 60 forward passes on the bench-2 **premises only** (no question, no option list — the EXP107 extraction discipline).
- **Backbone pin:** `~/workspace/.exp086_weights/pythia-410m`; parameter hash recorded **before and after** all 60 extractions and compared against the LOG-331 pin `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed`. Any mismatch → RUN-INVALID, quarantine, no metric may be read (Law #6, Law #13).
- **Determinism pins (Law #13):** `model.eval()` before all forwards; `torch.no_grad()` around ALL forward passes; CPU-only (`device_map="cpu"` attempted — the EXP111-recorded transformers-5.17.0 behavior governs: if the environment requires dropping it, the drop is a CPU-only no-op and is logged); float32; torch/numpy seeds = 0; CPU thread count set and read back via `torch.get_num_threads()`, recorded in the worksheet.
- **Environment (pinned):** torch==2.14.0+cpu, transformers==5.17.0, numpy==2.5.3, sklearn==1.9.1 — the EXP111 §6 secondary's registered environment, which did fresh extractions.
- **Provenance:** extracted embeddings written as an npz (`embeddings` (60, 1024) float32, `ids` (60,) str); all 60 IDs byte-match the bench-2 per-item JSON (mirroring the EXP111 §3.2 verification). Canonical bench-2 JSON sha256 recorded.

### 3.4 Label pinning (Law #7 — the EXP119 FIX-1 lesson) [PROPOSITION]

The bench-2 builder's module docstring documents the meaning-preserving flip and states that `tuple[0]` = A is the highest-ranked entity on all 60 items; the builder's per-item assertion (`tuple[0]` in the first premise sentence iff A-first) provides the independent pin. **The pre-reg and the execution report cite the builder's construction docstring plus the independent pin — never a truncated inline comment** (the LOG-4625/4626 FIX-1 lesson). Bench 2's labels (`y=1 iff A-first`) are used only as the head's train targets (the pre-registered use) and as the test evaluation labels; test labels are used only for the final registered evaluation — no test-informed selection anywhere (no head-spec change, no seed change, no cell re-weighting on seeing bench-2 data).

### 3.5 Split and training [PROPOSITION] — EXP111 §3.3–§3.4 pinned verbatim

- **Disjoint stratified split:** `train_test_split` (**sklearn==1.9.1**, **numpy==2.5.3**), `test_size=0.5`, **seed pinned: 20260929**, stratified by the pinned 4-cell key `f"{phrasing}_{flipped}"` with phrasing ∈ {"A-first", "C-first"} and flipped ∈ {False, True}. Expected test counts per cell in sorted key order deterministically **8/8/7/7** — ("A-first", original): 8, ("A-first", flipped): 7, ("C-first", original): 7, ("C-first", flipped): 8 — → **train n=30, test n=30** with **N_F=15 flipped=False** and **N_T=15 flipped=True** test items. The exact train/test item-id lists and the observed N_F, N_T are written to the run log; disjointness is asserted (any overlap → RUN-INVALID).
- **Head:** `LogisticRegression(penalty='l2', C=1.0, solver='lbfgs', max_iter=1000, random_state=20260929)`. All hyperparameters pinned here — **no tuning** (Law #7 extended to every model-selection decision: no L2-C sweep, no layer choice, no solver choice, no seed re-rolls; the EXP106 review lesson). One shot; no sweeps.
- **Block-off discipline (adapted — backbone IS loaded for extraction):** (a) bench-2 canonical JSON hash recorded before extraction and verified byte-identical after; (b) head weights derived only from the pinned train split; (c) determinism pass — re-fit from the same npz and assert byte-identical test predictions; (d) final weight-hash logged. Any mismatch → RUN-INVALID.
- **Δθ=0 (Law #6) [PROPOSITION]:** satisfied via the before/after LOG-331 hash check (§3.3); the only trained parameters are the logistic head's (w, b) on the pinned train split.

### 3.6 Metrics [PROPOSITION]

Primary: overall accuracy on the 30 held-out test items. Secondary (kill-test): per-cell accuracies — specifically the template-detector signature gap:
**G = acc(N_F flipped=False test items) − acc(N_T flipped=True test items)** (N_F=15, N_T=15 under the pinned split encoding; both logged in the worksheet). Also reported descriptively: per-cell (4-cell) accuracies, train accuracy (sanity only — no bar on it), head weight norm.

### 3.7 Record-keeping gate (the EXP119 lesson) [PROPOSITION]

The following are all written and hash-pinned (sha256) in the run records **before any verdict is written** — an artifact-existence gate: builder script, bench-2 canonical JSON, per-item JSON records, extracted embedding npz, train/test item-ID lists, fitted head parameters (coef_, intercept_), backbone hashes before/after extraction. **Missing artifact → RUN-INVALID (incomplete record).** Raw records persist before verdict; the verdict's evidentiary basis is intact by construction.

### 3.8 Law #7 posture [PROPOSITION]

Bench-2 ground-truth labels are used only as the pre-registered head targets and the final registered evaluation; no test-informed model selection. Entity names are the pre-registered measurement inputs (the embedding extraction requires the premise texts). Law #7 is clean by construction.

---

## 4. Decision bars with statistical license

n=30 test items, one-sided binomial vs chance (p=0.5), α=0.05: the critical value is **20/30** (exact one-sided p=0.0494; 19/30 → p=0.1002 — fails the bar; 18/30 → p=0.1808). All values verified at drafting (carried from the H5 pre-reg's licensed bars).

- **CONTINUE:** overall test accuracy **≥ 20/30** (p ≤ 0.0494) **AND** no template-detector signature (**G < 0.30**).
- **KILL (of the H15 generality hypothesis):** template-detector signature present (**G ≥ 0.30** — a ≥5-item gap at the pinned N_F=N_T=15 denominators; the registered EXP107 signature produced G = 30/30 − 4/30 = 0.867) **regardless of overall score**; OR overall test accuracy **≤ 18/30** (p ≥ 0.1808). EXP111's bench-1 observation stands (Law #8) and is reclassified as a bench-specific correlation.
- **HELD:** overall = **19/30** with G < 0.30. Underpowered zone: neither continue nor kill; no rerun, no larger-N rescue (the EXP106 no-rescue discipline applies).

**Pre-installed kill-test, one sentence:** *If the trained head reproduces the EXP107 template-detector signature — high accuracy on original-word test items but at-chance accuracy on flipped-word test items (G ≥ 0.30) — the generality reading is KILLED, and the bench-2 result is reclassified as template detection, with no rerun or larger-N rescue; EXP111's bench-1 observation is reclassified as bench-specific, never erased.*

---

## 5. Falsification decision tree

```
Phase 0 — bench-2 construction (the breaking point)
 ├─ any §3.2 design-time assertion fails (cells, families, extraction contract,
 │   label check, ID namespace) → RUN-INVALID (construction)
 ├─ G-C1 pure-template detector > 36/60 → RUN-INVALID (construction: template-decodable bench)
 ├─ G-C2 |Pearson(r1,r2)| > 0.10 → RUN-INVALID (construction: not decorrelated from bench 1)
 └─ G-C3 template decomposition not independently pinnable → RUN-INVALID (construction)
     └─ canonical bench-2 JSON pin recorded; per-item records written
         Phase 1 — 60 fresh layer-20 extractions (backbone hash vs LOG-331 pin)
          ├─ hash drift → RUN-INVALID (quarantine), no metric may be read
          └─ npz/ids byte-match per-item records
              └─ stratified 30/30 split (seed 20260929, pinned key encoding)
                  ├─ train/test ID overlap → RUN-INVALID (Law #7)
                  └─ disjoint
                      └─ train L2-logreg → determinism re-fit pass (§3.5)
                          ├─ predictions ≠ byte-identical → RUN-INVALID (block-off discipline)
                          └─ determinism OK → artifact-existence gate (§3.7)
                              ├─ any artifact missing/unhashed → RUN-INVALID (incomplete record)
                              └─ all artifacts pinned → evaluate on 30 held-out
                                  ├─ G ≥ 0.30 → KILL (generality hypothesis dead;
                                  │    EXP111 bench-1 stands, reclassified bench-specific)
                                  │    (takes precedence over any overall score)
                                  ├─ G < 0.30 and overall ≥ 20/30 → CONTINUE
                                  │    (template-invariant feature licensed on a second bench)
                                  ├─ G < 0.30 and overall = 19/30 → HELD (underpowered; no rescue)
                                  └─ G < 0.30 and overall ≤ 18/30 → KILL (no transfer on bench 2;
                                       output-side readout room retired as bench-specific)
```

No other branches exist. No re-runs, no re-seeds, no post-hoc bars (Law #4, Law #9).

---

## 6. What this protocol explicitly does NOT do

1. **No secondary per-layer analysis.** EXP111's §6 secondary already explored layers 4/8/12/16 descriptively on bench 1; re-running it on bench 2 would be a per-layer search — barred as scope creep. H15 tests one protocol at one read site (layer 20).
2. No re-reading of bench-1 data, no re-fitting on bench-1 embeddings, no re-cutting the fixed EXP111 split (Law #13 fence, §8).
3. No cross-bench effect-size comparisons (no post-hoc cross-bench t-test — the split is powered for the bar, not for comparisons).

---

## 7. Cost and honesty

- **$0 CPU, ~1.5h.** Bench-2 construction (pure string authoring, no model calls); 60 layer-20 CPU forward passes (~30–60 min, Δθ=0); logistic fit + bookkeeping + determinism pass on archived bench-2 embeddings. No generation anywhere.
- **Honesty ledger:** (a) the test set is n=30 — powered for the pre-registered bar (20/30, p=0.0494) but not for fine distinctions; (b) bench-2's labels encode the subject-position cue (A-first → y=1), so a CONTINUE means the head extracts *position* on a second bench — a legitimate frozen-backbone signal but a narrow one; (c) no generality beyond the two benches, the layer, or the model is claimed (§8).

---

## 8. What H15 does NOT claim

1. A CONTINUE is a **correlation at one layer on two benches** — it is not consciousness, not generality beyond the benches, not superhuman cognition.
2. A CONTINUE does not claim capability beyond the task: downstream causal tests (steering, decision-flip) are required before any capability statement.
3. A CONTINUE does not re-license H1/H4, static-injection lines, or any closed family.
4. A KILL retires only the **generality hypothesis** — it does not erase EXP111's bench-1 observation (Law #8), which is reclassified as a bench-specific correlation, never un-happened.
5. Law #13 fence: bench 2 is an independent apparatus — no re-reading of bench-1 data, no re-fitting, no re-cutting. The G-C2 correlation gate compares bench-2's construction against bench-1's builder records as a design check only; it feeds no bench-1 labels or embeddings into the analysis.
6. Novelty: **N1 — Known Combination.** Trained linear probes on decorrelated benches are a known combination; no new mechanism is claimed (Law #10).

---

## 9. Deviations from the dossier and from EXP111 (complete list)

1. **Bench-2 construction phase prepended** (the breaking point): the H5 pre-reg started from archived embeddings; H15 pins a full construction discipline with design-time assertions and three quantitative gates (G-C1, G-C2, G-C3) whose failure voids the item before any head is trained.
2. **Fresh extraction instead of archived embeddings:** bench-2 embeddings are extracted with 60 new CPU forwards, so the LOG-331 backbone hash check is required before AND after (EXP111's primary needed no backbone contact; its §6 secondary provides the registered precedent and environment).
3. **Record-keeping artifact-existence gate added** (§3.7): the EXP119 lesson (LOG-4628) — builder script, canonical JSON, per-item records, embedding npz, train/test ID lists, head parameters all hash-pinned before any verdict; missing artifact → RUN-INVALID.
4. **FIX-1 label-pin discipline** (§3.4): cite the bench-2 builder's construction docstring plus the independent pin; never a truncated inline comment (the LOG-4625/4626 lesson).
5. **No secondary per-layer analysis** (§6): the H5 §6 secondary was licensed on bench 1; H15 runs one protocol at one read site — the per-layer search is barred as scope creep.
6. **H15-KILL semantics pinned:** the KILL bar applies to the generality hypothesis; EXP111's bench-1 observation stands under Law #8 and is reclassified, never erased (Law #11 two-layer tagging, §1.1).
7. **Cross-bench effect-size comparisons explicitly unlicensed** (§2): the dispatch brief's quantitative prediction is honored only as directional prediction under each hypothesis; no post-hoc t-test between benches.

---

## 10. Boundary

Independent Law #14 review of this exact file is a separate lane. No experiment number is minted by this draft. Execution, if ever launched, is a CEO decision under a minted number. This lane stops here.
