# Pre-registration: H23 — Within-Domain Decoy Dissection of the Three-Bench Trained-Head Signal

**Status:** DRAFT pre-registration. Licenses nothing. No model runs, no experiment number minted, no signed protocol touched, no GPU contact, no commits, no pushes. $0 CPU.
**Drafting lane:** LOG-4685 (pre-assigned). **Source:** `research/strategy/H23_GATE_2026-09-29.md` (worth-it gate PASS at LOG-4684 — the gate memo's six items, decision bars, and binding defect classes are binding here).
**Launch chain:** independent Law #14 review of this exact file → fix-verification (if fixes required) → CEO launch decision (minting EXP126) → execution under the minted experiment number. This lane stops at the draft.

**Governing laws:** Law #4 (no post-hoc hypothesis shifts — the bars below are binding), Law #6 (frozen backbone Δθ=0), Law #7 (zero data leakage — extended below to every model-selection decision), Law #8 (nothing retroactively un-happens — EXP111's, EXP120's, and EXP122's bench observations stand under any H23 outcome), Law #9 (metrics registered before any output is inspected), Law #11 (Law-#11 tagging — H23's identity-readout hypothesis, the three benches' observations, and their CONTINUE interpretations are separate layers), Law #13 (deterministic reproducibility — seeds, hashes, environment manifest pinned below), Law #14 (independent review of this exact file is a separate lane).

**Epistemological labels** per `SCBI/AGENTS.md` §5: [OBSERVATION], [HYPOTHESIS], [INTERPRETATION], [PROPOSITION], [ASSUMPTION], [FACT].

---

## 0. The breaking point (read first)

**Bench construction is the breaking point.** If any construction gate in §3.2 fails → the lane dies at construction: **no head is trained, no metric is read, and no experiment number is consumed beyond what the CEO assigns.** The log records the construction failure as a construction-fate RUN-INVALID (apparatus void — the identity-readout hypothesis received no test; recorded **UNTESTED, not killed**). If no valid fifth bench can be constructed, H23 is void; a contaminated-bench run is never licensed.

The breaking point is conjunctive: ALL of §3.2's design assertions and quantitative gates must pass. A single miss voids the apparatus.

---

## 1. Hypothesis (one falsifiable sentence)

**[HYPOTHESIS]** The three-bench trained-head signal — trained L2-logistic heads on frozen Pythia-410m layer-20 final-token embeddings scoring 24/30, 25/30, and 27/30 with no word-family-detector signature — is a **true entity-identity readout** (extracts a property of the target entity's identity within a single domain) rather than a **domain-set detector** (reading only which domain set sits on top), tested by running the pinned H5/H16 head protocol byte-verbatim on a newly constructed all-animal bench 5 where the label encodes the target's entity-subset membership and domain-set membership carries zero information by construction.

### 1.1 Why this experiment exists

[OBSERVATION] EXP111 (H5/LFH-TD): trained L2-logistic head on frozen layer-20 embeddings scored **24/30** (one-sided p≈0.0014) with **G=0.0000** on the EXP107 template-decorrelated bench — CONTINUE, bound at LOG-4567. [OBSERVATION] EXP120 (H15/LFH-GEN2): the same pinned protocol scored **25/30** (exact one-sided p=0.0001624) with **G=−0.2000** on an independently constructed second decorrelated bench — qualified CONTINUE, bound at LOG-4634/4636. [OBSERVATION] EXP122 (H16/POSITIONCUE): the pinned H5 head protocol scored **27/30 = 0.9000** with **G=−0.0667** and |Pearson|=0.0322 position-decorrelation on bench 3 — CONTINUE, bound at LOG-4655.

**Law-#11 tagging:** H23's [HYPOTHESIS] (identity-readout vs domain-set-detector) and the three benches' [OBSERVATION]s are separate layers, and the three-bench CONTINUE is a third layer ([INTERPRETATION]) whose meaning H23 tests. An H23 **KILL** of the identity-readout interpretation retires that interpretation only; the three [OBSERVATION]s **stand** (Law #8) and the three-bench CONTINUE is **reclassified** as a domain-set-detector correlation — never erased or re-scored.

[INTERPRETATION] The program's only bound CONTINUEs are in trained-readout decodability (scoreboard v3.0). Their narrow reading (EXP122 §8: "a CONTINUE means the head extracts the target's identity with position decorrelated") leaves a surviving confound: on all three benches the target and distractor entities came from **different domain sets per cell**, so a coarse "which domain set is on top" detector produces the same CONTINUE pattern as a true entity-identity readout. The domain-set cue was never separated — the H16 pattern repeated one level up: the EXP107 builder's honest limitation named position (separated at H16); the H23 design names domain-set membership, and separates it here by making every bench-5 premise single-domain (all animals). Bench 5 makes domain-set membership informationally dead by construction — exactly what makes the test discriminative. It is the cheapest licensed way to give the three-bench line its first mechanistic foothold or retire its mechanistic use.

---

## 2. Exact question and the decision it changes

**Exact question [HYPOTHESIS]:** Is the three-bench trained-head signal a *domain-set detector* or a *true entity-identity readout*? Test: the pinned H5/H16 head protocol — byte-verbatim head spec, split seed 20260929, layer-20 extraction site, Δθ=0 backbone pin — on a newly constructed bench 5 where **every premise is single-domain (all animals)**, the label encodes the target's entity-subset membership (S1 vs S2), decoy options are drawn from the same domain as the target, and a construction audit certifies **zero cross-domain entities**.

**Decision changed:**
- **CONTINUE (identity-readout interpretation):** test accuracy **≥ 20/30** (one-sided binomial p ≤ 0.0494 vs chance, the H5/H16 signed bar) **AND** **G < 0.30** (G = acc(flipped=False) − acc(flipped=True) over the word-family cells, carried verbatim from the H15/H16 discipline) → the trained head extracts entity identity within a single domain; the three-bench CONTINUE gains a mechanistic foothold — the signal is not exhausted by a domain-set detector. Strengthens the boundary characterization; licenses nothing downstream (no steering, no capability — §Summit below).
- **KILL (identity interpretation):** test accuracy **≤ 18/30** (p ≥ 0.1808) **or** **G ≥ 0.30** → the identity reading is dead. The three **observations stand** (Law #8 — nothing retroactively un-happens) but their CONTINUE is **reclassified as a domain-set-detector correlation** under Law #11's two-layer tagging; any entity-level use of the signal is retired.
- **HELD:** **19/30** with **G < 0.30** → underpowered zone; no rerun, no larger-N rescue (the EXP106/EXP111 no-rescue discipline).

**PIVOT** does not appear in H23's outcome set.

**Explicit disclosure (label-design choice):** What is carried verbatim from H5/H16 is the **protocol** — head spec, split seed, extraction site, construction discipline, gates, and bars — **not the label definition**. Bench-5 labels are y=1 iff the highest-ranked entity (tuple[0]) belongs to entity-subset **S1 = {Cat, Dog, Bear, Wolf, Fox}**; y=0 iff it belongs to **S2 = {Lion, Tiger, Horse, Cow, Pig}** — a property of the target's **identity within a single domain**, distinct from bench-3's domain-set-membership labels and bench-1/2's A-first position labels. The design must change for the test to be discriminative: on a single-domain bench, a domain-set-membership label would carry zero information and the test would be void. This label choice is pinned below (§3.2, §3.4) and cited via the builder's construction docstring plus the independent pin (defect class (c)); the verdict bars are properties of the protocol **plus this specific label design** — a different label design would be a different hypothesis, never an amendment.

**Not licensed:** any post-hoc cross-bench effect-size comparison (no t-test between bench-1/2/3 and bench-5 accuracies — unlicensed cross-bench effect sizes, the H15 lesson); any re-reading of bench-1/2/3/4 data, re-fitting on bench-1/2/3/4 embeddings, re-cutting the fixed EXP111/EXP120/EXP122 splits (Law #13 fence, §8); any transfer of H6's 42–57/60 honesty-logit bars (wrong apparatus, wrong n — the gate memo's bar-calibration adjudication; the H5/H16 signed n=30 head bars bind here).

---

## 3. Method

### 3.1 No-generation protocol [ASSUMPTION]

H23 requires **zero generation** (the EXP108/EXP109/EXP115/EXP116 hard constraint carries over). The design is forward-pass-only embedding extraction for bench 5 plus vector arithmetic on archived bench-5 embeddings. No autoregressive decoding appears anywhere in this design. No plan text, no tokenization-identity surface (EXP119's break has no purchase here).

### 3.2 Phase 0 — Bench-5 construction (the breaking point) [PROPOSITION]

Bench 5 is **independently authored** under the EXP107 kill-test discipline (LOG-4535 bench builder is the model of the discipline, not the source of the content). The construction lane writes a deterministic builder script (no RNG, no model calls — pure string construction, like `build_exp107_bench.py`) satisfying ALL of the following. Any failure → the lane dies here per §0 (construction-fate RUN-INVALID, hypothesis UNTESTED).

1. **Single domain, new verb families.** The entity vocabulary is **14 animals**: {Cat, Dog, Bear, Wolf, Fox, Lion, Tiger, Horse, Cow, Pig, Rat, Bat, Bird, Fish} — all verified single-token under the real Pythia-410m tokenizer with `" "+E` leading-space encoding at the LOG-4684 gate (14/20 checked; Deer, Goat, Sheep, Frog, Snake, Crab excluded as multi-token). Entity-subset design: **S1 = {Cat, Dog, Bear, Wolf, Fox}** (target subset A), **S2 = {Lion, Tiger, Horse, Cow, Pig}** (target subset B), neutral decoys **{Rat, Bat, Bird, Fish}** appearing only as non-target tuple entities. Premise templates use two new verb families distinct from bench-1 ("outranks"/"is lower than"), bench-2 ("surpasses"/"is below"), bench-3 ("ranks above"/"ranks below", "dominates"/"is dominated by"), and bench-4 (EXP125's families) — a meaning-preserving pair documented in the builder's own docstring. **Check:** no bench-5 premise contains any prior-bench verb-family substring; no shared template content words beyond ordinary English function words. The `QUESTION_SUFFIX` (`" Question: Who is higher in rank? Answer:"`, byte-exact) and the `"Premise:"` framing are shared **format**, not template content.
2. **Structure parallel to benches 1/3:** 60 items; 2-hop and 3-hop premises; entity tuples of length 3 or 4 with `tuple[0]` = the highest-ranked entity A (the builder's meaning-preserving construction preserves "the ranking meaning (A > B > C [> D]) ... preserved"); the non-target tuple entities (B, C, and D when present) are drawn from **all 14 animals** (including the neutral decoys), so that `tuple[0]`'s subset membership is the only label-predictive cue; `phrasing` ∈ {"target-first", "target-last"} (30/30 — the original authoring group, NOT the target's final sentence position); a deterministic meaning-preserving flip applied to 15 items per phrasing (within each phrasing group sorted by id, even positions flip — the EXP107 discipline) → four balanced 15-item cells: (target-first, original) ×15, (target-first, flipped) ×15, (target-last, original) ×15, (target-last, flipped) ×15. The flip must preserve ranking meaning, keep `tuple[0]` = A as the highest-ranked entity, and re-anchor the target's sentence position per the builder's own documented rule (EXP107-style): **final position = phrasing XOR flipped**. Per-item records carry both `phrasing` (original group, the stratification key) and the final sentence position (used by the position-scramble gate).
3. **Design-time assertions** (mirroring `verify_cells`): 60 items; phrasing 30/30; four 15-item cells; flipped items use the OPPOSITE verb family from originals; extraction contract (`prompt` starts `"Premise:"`, `premise == prompt[:prompt.index(' Question:')]`); ID namespace distinct from benches 1–4 (e.g. `'expb5_...'`; assert no id starts with `'exp107_'`, `'expb2_'`, `'expb3_'`, `'exp125_'`, all ids unique); canonical rebuild determinism (re-running the builder script yields byte-identical canonical JSON).
4. **Labels [Law #7 — the bench-5 own label pin]:** `y = 1` **iff the highest-ranked entity (tuple[0]) belongs to entity-subset S1**; `y = 0` iff it belongs to S2. Labels balanced 30/30 by construction. Within each label class, the target's **final** sentence position (phrasing XOR flipped — see item 2) is balanced: target-first 15, target-last 15 (position-scrambled — position carries no information about the label). The flip×label pattern is identical across the two phrasing groups — the constructor arranges label order within each phrasing group so that final positions are 15/15 within each label class — so the "balanced by construction" entailment is sound; the position-scramble gate then verifies, rather than rescues, the construction. Per-item records carry `target_subset` ∈ {S1, S2}, `phrasing`, `flipped`, and an assertion verifying `y == (tuple[0] in S1)` independently from the item record (the bench's own documented construction rule — not inherited from bench-1/2's y=A-first convention or bench-3's y=domain-membership convention).

**Decorrelation gates (quantitative, string-level, no model contact):**

- **Single-domain audit (the discriminative gate):** the builder asserts — and an independent audit certifies per item — that **every entity mention on every bench-5 premise belongs to the 14-animal set**. Zero cross-domain entities. **Gate: 0/60 premises contain any out-of-domain entity name** (audited against the 14-animal set with whole-word matching). A domain-set detector has no input here by construction: this is the gate that makes H23 discriminative. Any violation → contaminated → construction failure.
- **G-C1 — pure-template detector gate:** define the pure-template rule T: predict y=1 iff the first premise sentence uses family-1. Verb-family assignment is decorrelated from target subset by construction (deterministic by item-index parity, independent of subset), so T scores ≈ 30/60 by construction. **Gate: T scores ≤ 36/60** — i.e., not above chance at α=0.05 one-sided (P(X ≥ 37 | 60, 0.5) = 0.0462305). A score above the bar means the bench is template-decodable → contaminated → construction failure.
- **G-C2 — entity-rank correlation gate:** let `r3` be bench-3's flattened entity-index sequences (the EXP122 builder records) and `r5` bench-5's, in canonical item order. **Gate: |Pearson(r3, r5)| ≤ 0.10.** Catches accidental structural copying of bench-3's entity assignments. (G-C2 compares bench-5's construction against bench-3's builder records for this design check only — it feeds no bench-3 labels or embeddings into the analysis; Law #13 fence §8.)
- **G-C3 — template-decomposition pin:** the bench-5 builder's template decomposition is independently pinned (QUESTION_SUFFIX byte-exact + canonical-order construction), so the meaning-preserving flip can be independently verified from the builder code. Failure → construction failure.
- **Position-scramble gate:** define the pure-position rule P: predict y=1 iff the target occupies the "first" final sentence position. Final position is balanced within each label class by construction (item 4, including the identical flip×label pattern across phrasing groups), so P scores 30/60 by construction. **Gate: P scores ≤ 36/60.** If position were informative about the label, the test could not separate a position detector from an identity readout. A score above the bar → contaminated → construction failure.

**Single-token assertion (defect class (f) — ACTIVE here):** all 14 entity names are asserted single-token under the real Pythia-410m tokenizer with `" "+E` encoding at construction (gate-verified at LOG-4684; re-run on the final sets by the construction lane — tokenizer-only). Any multi-token entity → construction restarted, not patched. (Departure from the H16 lineage's N/A: the H23 gate adopts single-token as construction hygiene — zero cost, keeps bench 5 logit-compatible for future reuse; declared here as an explicit design deviation, per the gate memo.)

If any design-time assertion, the single-domain audit, the single-token assertion, G-C1, G-C2, G-C3, or the position-scramble gate fails → **the item dies at bench construction; no head is trained; no metric is read; the hypothesis is recorded UNTESTED (no experiment number minted).** A further apparatus breaking point applies at execution: determinism re-fit pass fails or train/test ID overlap → RUN-INVALID (the EXP111 §3.4/§3.3 discipline).

### 3.3 Phase 1 — Bench-5 embedding extraction (fresh backbone contact) [PROPOSITION]

- **Embedding site:** `hidden_states[20]`, final token, float32, CPU — frozen Pythia-410m, layer 20. 60 forward passes on the bench-5 **premises only** (no question, no option list — the EXP107 extraction discipline).
- **Backbone pin:** `~/workspace/.exp086_weights/pythia-410m`; parameter hash recorded **before and after** all 60 extractions and compared against the LOG-331 pin `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed`. Any mismatch → RUN-INVALID, quarantine, no metric may be read (Law #6, Law #13).
- **Determinism pins (Law #13):** `model.eval()` before all forwards; `torch.no_grad()` around ALL forward passes; CPU-only; float32; torch/numpy seeds = 0; CPU thread count set and read back via `torch.get_num_threads()`, recorded in the worksheet.
- **Environment (pinned):** torch==2.14.0+cpu, transformers==5.17.0, numpy==2.5.3, sklearn==1.9.1 — the EXP120 §3.3 registered environment.
- **Provenance:** extracted embeddings written as an npz (`embeddings` (60, 1024) float32, `ids` (60,) str); all 60 IDs byte-match the bench-5 per-item JSON. Canonical bench-5 JSON sha256 recorded.

### 3.4 Label pinning (Law #7 — the EXP119 FIX-1 lesson) [PROPOSITION]

The bench-5 builder's module docstring documents (a) the meaning-preserving flip, (b) that `tuple[0]` = A is the highest-ranked entity on all 60 items, and (c) the label derivation rule: **y=1 iff tuple[0] ∈ S1 = {Cat, Dog, Bear, Wolf, Fox}, y=0 iff tuple[0] ∈ S2 = {Lion, Tiger, Horse, Cow, Pig}**, with the per-item assertion verifying `y == (tuple[0] in S1)` independently. **The pre-reg and the execution report cite the builder's construction docstring plus the independent pin — never a truncated inline comment** (the LOG-4625/4626 FIX-1 lesson). Bench-5 labels are used only as the head's train targets (the pre-registered use) and as the test evaluation labels; test labels are used only for the final registered evaluation — no test-informed selection anywhere (no head-spec change, no seed change, no cell re-weighting on seeing bench-5 data).

### 3.5 Split and training [PROPOSITION] — H5 §3.3–§3.4 pinned verbatim

- **Disjoint stratified split:** `train_test_split` (**sklearn==1.9.1**, **numpy==2.5.3**), `test_size=0.5`, **seed pinned: 20260929**, stratified by the pinned 4-cell key `f"{phrasing}_{flipped}"` with phrasing ∈ {"target-first", "target-last"} and flipped ∈ {False, True}. Under sklearn 1.9.1 + seed 20260929 the test counts per cell in sorted key order are deterministically **8/7/7/8** — ("target-first", original): 8, ("target-first", flipped): 7, ("target-last", original): 7, ("target-last", flipped): 8 — → **train n=30, test n=30** with **N_F=15 flipped=False** and **N_T=15 flipped=True** test items. The exact train/test item-id lists and the observed N_F, N_T are written to the run log; disjointness is asserted (any overlap → RUN-INVALID).
- **Head:** `LogisticRegression(penalty='l2', C=1.0, solver='lbfgs', max_iter=1000, random_state=20260929)`. All hyperparameters pinned here — **no tuning** (Law #7 extended to every model-selection decision: no L2-C sweep, no layer choice, no solver choice, no seed re-rolls; the EXP106 review lesson). One shot; no sweeps.
- **Convergence posture (registered):** no convergence gate beyond the pinned lbfgs spec. If the fit does not converge (ConvergenceWarning), it is a **reported defect** in the worksheet — noted alongside the verdict, not a verdict gate and not RUN-INVALID by itself.
- **Block-off discipline:** (a) bench-5 canonical JSON hash recorded before extraction and verified byte-identical after; (b) head weights derived only from the pinned train split; (c) determinism pass — re-fit from the same npz and assert byte-identical test predictions; (d) final weight-hash logged. Any mismatch → RUN-INVALID.
- **Δθ=0 (Law #6) [PROPOSITION]:** satisfied via the before/after LOG-331 hash check (§3.3); the only trained parameters are the logistic head's (w, b) on the pinned train split.

### 3.6 Metrics [PROPOSITION]

Primary: overall accuracy on the 30 held-out test items. Secondary (kill-test): per-cell accuracies — specifically the word-family signature gap:
**G = acc(N_F flipped=False test items) − acc(N_T flipped=True test items)** (N_F=15, N_T=15 under the pinned split encoding; both logged in the worksheet). Also reported descriptively: per-cell (4-cell) accuracies, train accuracy (sanity only — no bar on it), head weight norm. The executor prints the exact one-sided binomial p-value (executor-computed, never handwritten — defect class (a)); the descriptive two-sided value may also be printed by the executor.

### 3.7 Record-keeping gate (the EXP119 lesson) [PROPOSITION]

The following are all written and hash-pinned (sha256) in the run records **before any verdict is written** — an artifact-existence gate: builder script, bench-5 canonical JSON, per-item JSON records, extracted embedding npz, train/test item-ID lists, fitted head parameters (coef_, intercept_), backbone hashes before/after extraction. **Missing artifact → RUN-INVALID (incomplete record).** (Defect class (b): H23 has zero generation, so "raw generation records" become "raw embedding + head-weight artifacts hash-pinned before verdict".) Raw records persist before verdict; the verdict's evidentiary basis is intact by construction.

### 3.8 Law #7 posture [PROPOSITION]

Bench-5 ground-truth labels are used only as the pre-registered head targets and the final registered evaluation; no test-informed model selection. Entity names are the pre-registered measurement inputs (the embedding extraction requires the premise texts). Law #7 is clean by construction.

---

## 4. Decision bars with statistical license

n=30 test items, one-sided binomial vs chance (p=0.5), α=0.05: the critical value is **20/30** (exact one-sided p=0.0493686; 19/30 → p=0.1002442 — fails the bar; 18/30 → p=0.1807973). All values verified at drafting (carried from the H5/H16 pre-regs' licensed bars; recomputed by the H16 Law #14 review at LOG-4651).

- **CONTINUE (identity-readout interpretation):** overall test accuracy **≥ 20/30** (p ≤ 0.0494) **AND** no word-family signature (**G < 0.30**).
- **KILL (identity interpretation):** word-family signature present (**G ≥ 0.30** — a ≥5-item gap at the pinned N_F=N_T=15 denominators; takes precedence over any overall score) **OR** overall test accuracy **≤ 18/30** (p ≥ 0.1808). EXP111/EXP120/EXP122's bench observations stand (Law #8) and their CONTINUE is reclassified as a domain-set-detector correlation (Law #11); any entity-level use of the signal is retired.
- **HELD:** overall = **19/30** with G < 0.30. Underpowered zone: neither continue nor kill; no rerun, no larger-N rescue (the EXP106 no-rescue discipline applies).

**Pre-installed kill-test, one sentence:** *If the trained head reproduces the word-family detector signature — high accuracy on original-word test items but at-chance accuracy on flipped-word test items (G ≥ 0.30) — the identity-readout reading is KILLED, and the bench-5 result is reclassified as word-template detection, with no rerun or larger-N rescue; EXP111/EXP120/EXP122's bench observations stand and their three-bench CONTINUE is reclassified as a domain-set-detector correlation, never erased.*

---

## 5. Falsification decision tree

```
Phase 0 — bench-5 construction (the breaking point)
 ├─ any §3.2 design-time assertion fails (vocab/family freshness, cells,
 │   extraction contract, label check, ID namespace, canonical rebuild) → RUN-INVALID (construction)
 ├─ single-domain audit: any out-of-domain entity → RUN-INVALID (construction: domain cue present)
 ├─ single-token assertion: any multi-token entity → RUN-INVALID (construction: restarted, not patched)
 ├─ G-C1 pure-template detector > 36/60 → RUN-INVALID (construction: template-decodable bench)
 ├─ G-C2 |Pearson(r3,r5)| > 0.10 → RUN-INVALID (construction: not decorrelated from bench 3)
 ├─ G-C3 template decomposition not independently pinnable → RUN-INVALID (construction)
 ├─ position-scramble gate: pure-position detector > 36/60 → RUN-INVALID (construction: position informative)
 └─ ALL PASS → canonical bench-5 JSON pin recorded; per-item records written
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
                                  ├─ G ≥ 0.30 → KILL (identity interpretation dead;
                                  │    EXP111/EXP120/EXP122 observations stand; three-bench CONTINUE
                                  │    reclassified as domain-set-detector correlation)
                                  │    (takes precedence over any overall score)
                                  ├─ G < 0.30 and overall ≥ 20/30 → CONTINUE
                                  │    (identity readout survives domain-set-decoy removal —
                                  │    decodability only, §7)
                                  ├─ G < 0.30 and overall = 19/30 → HELD (underpowered; no rescue)
                                  └─ G < 0.30 and overall ≤ 18/30 → KILL (no identity readout on bench 5;
                                       three-bench CONTINUE reclassified as domain-set-detector correlation)
```

No other branches exist. No re-runs, no re-seeds, no post-hoc bars (Law #4, Law #9).

---

## 6. What this protocol explicitly does NOT do

1. **No secondary per-layer analysis.** H17 (standalone layer-profiling) was rejected at the design session (LOG-4638) because it names no decision a profile changes; H23's decision is fully fired by the primary layer-20 bar. Folding layer-resolved bars into H23 would be H17 through the back door — explicitly barred. EXP111 §7 layer numbers enter only as mathematical-license context (§1.1 citation above) and license no verdict.
2. No re-reading of bench-1/2/3/4 data, no re-fitting on bench-1/2/3/4 embeddings, no re-cutting the fixed EXP111/EXP120/EXP122 splits (Law #13 fence, §8).
3. No cross-bench effect-size comparisons (no post-hoc cross-bench t-test — the split is powered for the bar, not for comparisons).
4. **No logit channel.** H23 is an embedding-readout design; there is no plan-context composition, so defect class (e) — the [-3:] tokenization-identity pin — does not bind. Stated explicitly so no reviewer later demands it post-hoc.
5. **Single-token assertion IS active (defect class (f)).** The readout is a trained logistic head on final-token embeddings of full premises; H18's multi-token finding binds logit-channel benches, but the H23 gate adopts the single-token assertion (14/14, tokenizer-only) as construction hygiene — zero cost, keeps bench 5 logit-compatible for future reuse. Declared in §3.2 as an explicit design deviation from the H16 lineage, not a tweak.
6. **Per-item G1 explicitly N/A.** The EXP121 class-6 lesson (per-item mass screening only at construction, never post-hoc) has no purchase here: the H5/H16 head protocol carries no G1 mass guard at all — no per-item filtering occurs at construction or execution, period. Stated explicitly so no reviewer demands a G1 gate post-hoc.
7. **No EXP117 recitation reuse (defect class (d))** — zero generation in H23; stated explicitly.

---

## 7. Cost and honesty

- **$0 CPU, ~1.5h.** Bench-5 construction (pure string authoring, no model calls); 60 layer-20 CPU forward passes (~30–60 min, Δθ=0); logistic fit + bookkeeping + determinism pass on archived bench-5 embeddings. No generation anywhere.
- **Honesty ledger:** (a) the test set is n=30 — powered for the pre-registered bar (20/30, p=0.0494) but not for fine distinctions; (b) a CONTINUE licenses only **"identity readout survives domain-set-decoy removal"** — decodability, **not steering or capability** — the head extracts the target's entity-subset property at layer 20, nothing more; (c) the verdict bars are properties of the protocol **plus the pinned subset-label design** (§2 disclosure) — a different label design is a different hypothesis, not an amendment; (d) no generality beyond bench 5, the layer, or the model is claimed (§8).

---

## 8. What H23 does NOT claim

1. A CONTINUE is a **correlation at one layer on one bench** — it is not consciousness, not generality beyond the bench, not superhuman cognition.
2. A CONTINUE does not claim capability beyond the task: downstream causal tests (steering, decision-flip) are required before any capability statement. The trained head is a **label-informed control**, never an autonomous mechanism — a CONTINUE here never migrates to the capability scoreboard, which stays at zero positive signals for autonomous steering.
3. A CONTINUE does not re-license H1/H4, static-injection lines, or any closed family. H22's generality hypothesis stays **KILLed** (EXP125 — barred re-test per protocol §4; nothing here re-opens it).
4. A KILL retires only the **identity-readout interpretation** — it does not erase EXP111's, EXP120's, or EXP122's bench observations (Law #8); their CONTINUE is reclassified as a domain-set-detector correlation under Law #11's two-layer tagging, never un-happened.
5. Law #13 fence: bench 5 is an independent apparatus — no re-reading of bench-1/2/3/4 data, no re-fitting, no re-cutting. The G-C2 correlation gate compares bench-5's construction against bench-3's builder records as a design check only; it feeds no bench-1/2/3/4 labels or embeddings into the analysis.
6. Novelty: **N1 — Known Combination.** Trained linear probes on decorrelated benches are a known combination; no new mechanism is claimed (Law #10).
7. No layer-resolved or logit-level claims of any kind.

---

## 9. Deviations from the dossier and from H5/H16 (complete list)

1. **Bench-5 construction phase prepended** (the breaking point): construction discipline with design-time assertions and five quantitative gates (single-domain audit, G-C1, G-C2, G-C3, plus the position-scramble gate carried from H16) plus the single-token assertion, whose failure voids the item before any head is trained — the H16 discipline carried over with the new discriminative gate added.
2. **Label semantics re-designed, protocol carried verbatim:** bench-5 labels encode the target's entity-subset membership (S1 vs S2 within a single domain) instead of the position feature or the domain-set membership; the H5/H16 *protocol* (head spec, split seed, extraction site, bars, gates, record-keeping) carries byte-verbatim — the label definition does not (§2 disclosure). This is the design change the H23 gate requires for the test to be discriminative.
3. **Single-domain audit (new discriminative gate, §3.2):** independent per-item certification of zero cross-domain entities — the gate that makes domain-set-decoy vs identity-readout separable.
4. **Single-token assertion ACTIVE (§3.2, §6 item 5):** explicit design deviation from the H16 lineage — 14/14 single-token at construction (tokenizer-only), declared here rather than smuggled.
5. **No convergence gate:** a non-converged lbfgs fit is a reported defect, not a gate (§3.5) — carried from H16.
6. **Record-keeping artifact-existence gate retained** (§3.7): the EXP119 lesson — with the defect-class (b) adaptation: zero generation in H23, so the gate pins raw embeddings + head weights instead of raw generations.
7. **Defect classes (d), (e), (g) explicitly N/A:** no EXP117 recitation reuse (zero generation), no [-3:] identity pin (no logit channel), no per-item G1 (head protocol carries no mass guard) — each stated explicitly in §6 so reviewers do not demand them post-hoc.
8. **H17 explicitly not folded in:** no per-layer secondary, no descriptive layer numbers as bars (§6 item 1) — the EXP111 §7 layer profile enters only as mathematical-license context.
9. **Cross-bench effect-size comparisons explicitly unlicensed** (§2): the gate memo's quantitative prediction is honored only as directional prediction under each hypothesis; no post-hoc t-test between benches. H6's 42–57/60 bars explicitly barred from transfer.

---

## 10. Boundary

**What this protocol cannot show:** (a) whether the identity-readout signal, if CONTINUE, is causal — steering/decision-flip tests are required before any capability statement (§8); (b) whether the signal exists at any other layer, bench, or model — one bench, one layer (20), one model; (c) whether the label-free race or any steering mechanism exists — H23 does not compete with it.

**Summit filter:** **NO — boundary-science dissection, not a summit move.** It adds no capability, routing, or self-improving loop. It is worth it only as license-maintenance for the three-bench line: a domain-set-detector finding kills any entity-level use of the signal, and an identity-readout finding gives the program's best observation its first mechanistic foothold. The label-free race remains the actual race; this lane does not compete with it.

**H22's generality hypothesis stays KILLed:** EXP125's KILL (28/60, ≤33/60 band, bound at LOG-4681) is not re-opened here — nothing in H23's outcome set re-licenses an honesty-generality re-test at any n, layer, carrier, or bench (§8 item 3).

Independent Law #14 review of this exact file is a separate lane. No experiment number is minted by this draft. Execution, if ever launched, is a CEO decision under a minted number (EXP126). This lane stops here.
