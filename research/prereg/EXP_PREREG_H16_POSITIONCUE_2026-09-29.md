# Pre-registration: H16 — Position-Cue Dissection of the Two-Bench Trained-Head Signal

**Status:** DRAFT pre-registration. Licenses nothing. No model runs, no experiment number minted, no signed protocol touched, no GPU contact, no commits, no pushes. $0 CPU.
**Drafting lane:** LOG-4650 (pre-assigned). **Source:** `research/strategy/H16_GATE_2026-09-29.md` (worth-it gate PASS at LOG-4649 — the gate memo's six items, decision bars, and binding defect classes are binding here).
**Launch chain:** independent Law #14 review of this exact file → fix-verification (if fixes required) → CEO launch decision → execution under a minted experiment number. This lane stops at the draft.

**Governing laws:** Law #4 (no post-hoc hypothesis shifts — the bars below are binding), Law #6 (frozen backbone Δθ=0), Law #7 (zero data leakage — extended below to every model-selection decision), Law #8 (nothing retroactively un-happens — EXP111's and EXP120's bench observations stand under any H16 outcome), Law #9 (metrics registered before any output is inspected), Law #11 (Law-#11 tagging — H16's identity-readout hypothesis, EXP111's and EXP120's observations, and their CONTINUE interpretations are separate layers), Law #13 (deterministic reproducibility — seeds, hashes, environment manifest pinned below), Law #14 (independent review of this exact file is a separate lane).

**Epistemological labels** per `SCBI/AGENTS.md` §5: [OBSERVATION], [HYPOTHESIS], [INTERPRETATION], [PROPOSITION], [ASSUMPTION], [FACT].

---

## 0. The breaking point (read first)

**Bench construction is the breaking point.** If any construction gate in §3.2 fails → the lane dies at construction: **no head is trained, no metric is read, and no experiment number is consumed beyond what the CEO assigns.** The log records the construction failure as a construction-fate RUN-INVALID (apparatus void — the identity-readout hypothesis received no test; recorded **UNTESTED, not killed**). If no valid third bench can be constructed, H16 is void; a contaminated-bench run is never licensed.

The breaking point is conjunctive: ALL of §3.2's design assertions and quantitative gates must pass. A single miss voids the apparatus.

---

## 1. Hypothesis (one falsifiable sentence)

**[HYPOTHESIS]** EXP111/EXP120's trained-head signal — a trained L2-logistic head on frozen Pythia-410m layer-20 final-token embeddings scoring 24/30 and 25/30 with no template-detector signature — is an **entity-identity readout** (extracts a property of the target entity's identity) rather than a **subject-position detector**, tested by running the pinned H5 head protocol byte-verbatim on a newly constructed position-scrambled bench where the label encodes the target's domain-set membership and the target's sentence position carries no information.

### 1.1 Why this experiment exists

[OBSERVATION] EXP111 (H5/LFH-TD): trained L2-logistic head on frozen layer-20 embeddings scored **24/30** (one-sided p≈0.0014) with **G=0.0000** on the EXP107 template-decorrelated bench — CONTINUE, bound at LOG-4567. [OBSERVATION] EXP120 (H15/LFH-GEN2): the same pinned protocol scored **25/30** (exact one-sided p=0.0001624) with **G=−0.2000** on an independently constructed second decorrelated bench — qualified CONTINUE, bound at LOG-4634/4636.

**Law-#11 tagging:** H16's [HYPOTHESIS] (identity-readout vs position-detector) and EXP111/EXP120's [OBSERVATION]s are separate layers, and the two-bench CONTINUE is a third layer ([INTERPRETATION]) whose meaning H16 tests. An H16 **KILL** of the identity-readout interpretation retires that interpretation only; the two [OBSERVATION]s **stand** (Law #8) and the two-bench CONTINUE is **reclassified** as a position-detector correlation — never erased or re-scored.

[INTERPRETATION] The program's only bound CONTINUEs are in trained-readout decodability (scoreboard v2.5). Their narrow reading (EXP120 §8: "a CONTINUE means the head extracts *position* on a second bench") leaves the mechanism unidentified — the position cue is the only surviving confound named by both verdict reviews. H16 is the identified successor to the EXP107 builder's registered honest limitation ("the flip also moves the target from sentence-subject to sentence-object position, so a collapsed score kills the EXP106 transfer reading under EITHER a word-template cue or a subject-position cue; the test does not identify which surface cue the head used"). It is the cheapest licensed way to give the two-bench line a mechanistic foothold or retire its mechanistic use.

---

## 2. Exact question and the decision it changes

**Exact question [HYPOTHESIS]:** Is the EXP111/EXP120 trained-head signal a *subject-position detector* or an *entity-identity readout*? Test: the pinned H5 head protocol — byte-verbatim head spec, split seed 20260929, layer-20 extraction site, Δθ=0 backbone pin — on a newly constructed position-scrambled bench where the label encodes a property of the **target entity's identity** (highest-ranked entity's domain-set membership) and the target's sentence position is scrambled (balanced within each label class, position carries no information).

**Decision changed:**
- **CONTINUE (identity-readout interpretation):** test accuracy **≥ 20/30** (one-sided binomial p ≤ 0.0494 vs chance, the EXP111/EXP120 bar) **AND** **G < 0.30** (G = acc(flipped=False) − acc(flipped=True) over the word-family cells, carried verbatim from the H15 discipline) → the trained head extracts the target's identity with position decorrelated; the two-bench CONTINUE gains a mechanistic foothold — the signal is not exhausted by a position detector.
- **KILL (identity interpretation):** test accuracy **≤ 18/30** (p ≥ 0.1808) **or** **G ≥ 0.30** → the identity reading is killed. EXP111/EXP120's **observations stand** (Law #8 — nothing retroactively un-happens) but their CONTINUE is **reclassified as a position-detector correlation** under Law #11's two-layer tagging; any mechanistic use of the signal in the program is retired.
- **HELD:** **19/30** with **G < 0.30** → underpowered zone; no rerun, no larger-N rescue (the EXP106/EXP111 no-rescue discipline).

**PIVOT** does not appear in H16's outcome set.

**Explicit disclosure (label-design choice):** What is carried verbatim from H5 is the **protocol** — head spec, split seed, extraction site, construction discipline, gates, and bars — **not the label definition**. Bench-1/2 labels are y=1 iff A-first (the position feature itself — H5 pre-reg §3.2; EXP120 §8). Bench-3 labels are y=1 iff the highest-ranked entity belongs to domain-set D1 (vs D2) — a property of the target's **identity** — with the target's sentence position balanced within each label class. The design must change for the test to be discriminative: under A-first labels, an identity bench cannot be distinguished from a position bench. This label choice is pinned below (§3.2, §3.4) and cited via the builder's construction docstring plus the independent pin (defect class (c)); the verdict bars are properties of the protocol **plus this specific label design** — a different label design would be a different hypothesis, never an amendment.

**Not licensed:** any post-hoc cross-bench effect-size comparison (no t-test between bench-1/2 and bench-3 accuracies — unlicensed cross-bench effect sizes, the H15 lesson); any re-reading of bench-1 or bench-2 data, re-fitting on bench-1/2 embeddings, re-cutting the fixed EXP111/EXP120 splits (Law #13 fence, §8).

---

## 3. Method

### 3.1 No-generation protocol [ASSUMPTION]

H16 requires **zero generation** (the EXP108/EXP109/EXP115/EXP116 hard constraint carries over). The design is forward-pass-only embedding extraction for bench 3 plus vector arithmetic on archived bench-3 embeddings. No autoregressive decoding appears anywhere in this design. No plan text, no tokenization-identity surface (EXP119's break has no purchase here).

### 3.2 Phase 0 — Bench-3 construction (the breaking point) [PROPOSITION]

Bench 3 is **independently authored** under the EXP107 kill-test discipline (LOG-4535 bench builder is the model of the discipline, not the source of the content). The construction lane writes a deterministic builder script (no RNG, no model calls — pure string construction, like `build_exp107_bench.py`) satisfying ALL of the following. Any failure → the lane dies here per §0 (construction-fate RUN-INVALID, hypothesis UNTESTED).

1. **New vocabulary, new verb families.** Two new 5-entity named sets in fresh domains: **D1 = animals {Lion, Tiger, Bear, Wolf, Fox}** and **D2 = fruits {Apple, Mango, Cherry, Grape, Plum}** — disjoint from bench 1's {Mars, Venus, Jupiter, Saturn, Mercury, Iron, Gold, Silver, Bronze, Steel} and bench 2's rivers/trees sets. Premise templates use two new verb families: family-1 **"ranks above"/"ranks below"**, family-2 **"dominates"/"is dominated by"** — a meaning-preserving pair documented in the builder's own docstring. **Check:** no bench-3 premise contains any bench-1/bench-2 verb-family substring (`" outranks "`, `" is lower than "`, bench-2's "surpasses"/"is below" substrings); no shared template content words beyond ordinary English function words. The `QUESTION_SUFFIX` (`" Question: Who is higher in rank? Answer:"`, byte-exact) and the `"Premise:"` framing are shared **format**, not template content.
2. **Structure parallel to bench 1/2:** 60 items; 2-hop and 3-hop premises; entity tuples of length 3 or 4 with `tuple[0]` = the highest-ranked entity A (the builder's meaning-preserving construction preserves "the ranking meaning (A > B > C [> D]) ... preserved"); the non-target tuple entities (B, C, and D when present) are drawn from BOTH D1 and D2 (mixed-domain tuples), so that `tuple[0]`'s domain is the only domain cue predictive of y; `phrasing` ∈ {"target-first", "target-last"} (30/30 — the original authoring group, NOT the target's final sentence position); a deterministic meaning-preserving flip applied to 15 items per phrasing (within each phrasing group sorted by id, even positions flip — the EXP107 discipline) → four balanced 15-item cells: (target-first, original) ×15, (target-first, flipped) ×15, (target-last, original) ×15, (target-last, flipped) ×15. The flip must preserve ranking meaning, keep `tuple[0]` = A as the highest-ranked entity, and re-anchor the target's sentence position per the builder's own documented rule (EXP107-style): **final position = phrasing XOR flipped**. Per-item records carry both `phrasing` (original group, the stratification key) and the final sentence position (used by the position-scramble gate).
3. **Design-time assertions** (mirroring `verify_cells`): 60 items; phrasing 30/30; four 15-item cells; flipped items use the OPPOSITE verb family from originals; extraction contract (`prompt` starts `"Premise:"`, `premise == prompt[:prompt.index(' Question:')]`); ID namespace distinct from benches 1/2 (e.g. `'expb3_...'`; assert no id starts with `'exp107_'` or `'expb2_'`, all ids unique); canonical rebuild determinism (re-running the builder script yields byte-identical canonical JSON).
4. **Labels [Law #7 — the bench-3 own label pin]:** `y = 1` **iff the highest-ranked entity (tuple[0]) belongs to domain-set D1 (animals)**; `y = 0` iff it belongs to D2 (fruits). Labels balanced 30/30 by construction. Within each label class, the target's **final** sentence position (phrasing XOR flipped — see item 2) is balanced: target-first 15, target-last 15 (position-scrambled — position carries no information about the label). The flip×label pattern is identical across the two phrasing groups — the constructor arranges label order within each phrasing group so that final positions are 15/15 within each label class — so the "balanced by construction" entailment is sound; the position-scramble gate then verifies, rather than rescues, the construction. Per-item records carry `target_domain` ∈ {D1, D2}, `phrasing`, `flipped`, and an assertion verifying `y == (tuple[0] in D1)` independently from the item record (the bench's own documented construction rule — not inherited from bench 1/2's y=A-first convention).

**Decorrelation gates (quantitative, string-level, no model contact):**

- **G-C1 — pure-template detector gate:** define the pure-template rule T: predict y=1 iff the first premise sentence uses family-1. Verb-family assignment is decorrelated from target domain by construction (deterministic by item-index parity, independent of domain), so T scores ≈ 30/60 by construction. **Gate: T scores ≤ 36/60** — i.e., not above chance at α=0.05 one-sided (P(X ≥ 37 | 60, 0.5) ≈ 0.047). A score above the bar means the bench is template-decodable → contaminated → construction failure.
- **G-C2 — entity-rank correlation gate:** let `r1` be bench-1's flattened entity-index sequences (the EXP107 builder records) and `r3` bench-3's, in canonical item order. **Gate: |Pearson(r1, r3)| ≤ 0.10.** Catches accidental structural copying of bench-1's entity assignments. (G-C2 compares bench-3's construction against bench-1's builder records for this design check only — it feeds no bench-1 labels or embeddings into the analysis; Law #13 fence §8.)
- **G-C3 — template-decomposition pin:** the bench-3 builder's template decomposition is independently pinned (QUESTION_SUFFIX byte-exact + canonical-order construction), so the meaning-preserving flip can be independently verified from the builder code. Failure → construction failure.
- **Position-scramble gate (new, discriminative):** define the pure-position rule P: predict y=1 iff the target occupies the "first" final sentence position. Final position is balanced within each label class by construction (item 4, including the identical flip×label pattern across phrasing groups), so P scores 30/60 by construction. **Gate: P scores ≤ 36/60.** This is the gate that makes H16 discriminative: if position were informative about the label, the test could not separate a position detector from an identity readout. A score above the bar → contaminated → construction failure.

If any design-time assertion, G-C1, G-C2, G-C3, or the position-scramble gate fails → **the item dies at bench construction; no head is trained; no metric is read; the hypothesis is recorded UNTESTED (no experiment number minted).** A further apparatus breaking point applies at execution: determinism re-fit pass fails or train/test ID overlap → RUN-INVALID (the EXP111 §3.4/§3.3 discipline).

### 3.3 Phase 1 — Bench-3 embedding extraction (fresh backbone contact) [PROPOSITION]

- **Embedding site:** `hidden_states[20]`, final token, float32, CPU — frozen Pythia-410m, layer 20. 60 forward passes on the bench-3 **premises only** (no question, no option list — the EXP107 extraction discipline).
- **Backbone pin:** `~/workspace/.exp086_weights/pythia-410m`; parameter hash recorded **before and after** all 60 extractions and compared against the LOG-331 pin `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed`. Any mismatch → RUN-INVALID, quarantine, no metric may be read (Law #6, Law #13).
- **Determinism pins (Law #13):** `model.eval()` before all forwards; `torch.no_grad()` around ALL forward passes; CPU-only; float32; torch/numpy seeds = 0; CPU thread count set and read back via `torch.get_num_threads()`, recorded in the worksheet.
- **Environment (pinned):** torch==2.14.0+cpu, transformers==5.17.0, numpy==2.5.3, sklearn==1.9.1 — the EXP120 §3.3 registered environment.
- **Provenance:** extracted embeddings written as an npz (`embeddings` (60, 1024) float32, `ids` (60,) str); all 60 IDs byte-match the bench-3 per-item JSON. Canonical bench-3 JSON sha256 recorded.

### 3.4 Label pinning (Law #7 — the EXP119 FIX-1 lesson) [PROPOSITION]

The bench-3 builder's module docstring documents (a) the meaning-preserving flip, (b) that `tuple[0]` = A is the highest-ranked entity on all 60 items, and (c) the label derivation rule: **y=1 iff tuple[0] ∈ D1 (animals), y=0 iff tuple[0] ∈ D2 (fruits)**, with the per-item assertion verifying `y == (tuple[0] in D1)` independently. **The pre-reg and the execution report cite the builder's construction docstring plus the independent pin — never a truncated inline comment** (the LOG-4625/4626 FIX-1 lesson). Bench-3 labels are used only as the head's train targets (the pre-registered use) and as the test evaluation labels; test labels are used only for the final registered evaluation — no test-informed selection anywhere (no head-spec change, no seed change, no cell re-weighting on seeing bench-3 data).

### 3.5 Split and training [PROPOSITION] — H5 §3.3–§3.4 pinned verbatim

- **Disjoint stratified split:** `train_test_split` (**sklearn==1.9.1**, **numpy==2.5.3**), `test_size=0.5`, **seed pinned: 20260929**, stratified by the pinned 4-cell key `f"{phrasing}_{flipped}"` with phrasing ∈ {"target-first", "target-last"} and flipped ∈ {False, True}. Under sklearn 1.9.1 + seed 20260929 the test counts per cell in sorted key order are deterministically **8/7/7/8** — ("target-first", original): 8, ("target-first", flipped): 7, ("target-last", original): 7, ("target-last", flipped): 8 — → **train n=30, test n=30** with **N_F=15 flipped=False** and **N_T=15 flipped=True** test items. The exact train/test item-id lists and the observed N_F, N_T are written to the run log; disjointness is asserted (any overlap → RUN-INVALID).
- **Head:** `LogisticRegression(penalty='l2', C=1.0, solver='lbfgs', max_iter=1000, random_state=20260929)`. All hyperparameters pinned here — **no tuning** (Law #7 extended to every model-selection decision: no L2-C sweep, no layer choice, no solver choice, no seed re-rolls; the EXP106 review lesson). One shot; no sweeps.
- **Convergence posture (registered):** no convergence gate beyond the pinned lbfgs spec. If the fit does not converge (ConvergenceWarning), it is a **reported defect** in the worksheet — noted alongside the verdict, not a verdict gate and not RUN-INVALID by itself.
- **Block-off discipline:** (a) bench-3 canonical JSON hash recorded before extraction and verified byte-identical after; (b) head weights derived only from the pinned train split; (c) determinism pass — re-fit from the same npz and assert byte-identical test predictions; (d) final weight-hash logged. Any mismatch → RUN-INVALID.
- **Δθ=0 (Law #6) [PROPOSITION]:** satisfied via the before/after LOG-331 hash check (§3.3); the only trained parameters are the logistic head's (w, b) on the pinned train split.

### 3.6 Metrics [PROPOSITION]

Primary: overall accuracy on the 30 held-out test items. Secondary (kill-test): per-cell accuracies — specifically the word-family signature gap:
**G = acc(N_F flipped=False test items) − acc(N_T flipped=True test items)** (N_F=15, N_T=15 under the pinned split encoding; both logged in the worksheet). Also reported descriptively: per-cell (4-cell) accuracies, train accuracy (sanity only — no bar on it), head weight norm. The executor prints the exact one-sided binomial p-value (executor-computed, never handwritten — defect class (a)); the descriptive two-sided value may also be printed by the executor.

### 3.7 Record-keeping gate (the EXP119 lesson) [PROPOSITION]

The following are all written and hash-pinned (sha256) in the run records **before any verdict is written** — an artifact-existence gate: builder script, bench-3 canonical JSON, per-item JSON records, extracted embedding npz, train/test item-ID lists, fitted head parameters (coef_, intercept_), backbone hashes before/after extraction. **Missing artifact → RUN-INVALID (incomplete record).** (Defect class (b): H16 has zero generation, so "raw generation records" become "raw embedding + head-weight artifacts hash-pinned before verdict".) Raw records persist before verdict; the verdict's evidentiary basis is intact by construction.

### 3.8 Law #7 posture [PROPOSITION]

Bench-3 ground-truth labels are used only as the pre-registered head targets and the final registered evaluation; no test-informed model selection. Entity names are the pre-registered measurement inputs (the embedding extraction requires the premise texts). Law #7 is clean by construction.

---

## 4. Decision bars with statistical license

n=30 test items, one-sided binomial vs chance (p=0.5), α=0.05: the critical value is **20/30** (exact one-sided p=0.0494; 19/30 → p=0.1002 — fails the bar; 18/30 → p=0.1808). All values verified at drafting (carried from the H5/H15 pre-regs' licensed bars).

- **CONTINUE (identity-readout interpretation):** overall test accuracy **≥ 20/30** (p ≤ 0.0494) **AND** no word-family signature (**G < 0.30**).
- **KILL (identity interpretation):** word-family signature present (**G ≥ 0.30** — a ≥5-item gap at the pinned N_F=N_T=15 denominators; takes precedence over any overall score) **OR** overall test accuracy **≤ 18/30** (p ≥ 0.1808). EXP111/EXP120's bench observations stand (Law #8) and their CONTINUE is reclassified as a position-detector correlation (Law #11); any mechanistic use of the signal is retired.
- **HELD:** overall = **19/30** with G < 0.30. Underpowered zone: neither continue nor kill; no rerun, no larger-N rescue (the EXP106 no-rescue discipline applies).

**Pre-installed kill-test, one sentence:** *If the trained head reproduces the word-family detector signature — high accuracy on original-word test items but at-chance accuracy on flipped-word test items (G ≥ 0.30) — the identity-readout reading is KILLED, and the bench-3 result is reclassified as word-template detection, with no rerun or larger-N rescue; EXP111/EXP120's bench observations stand and their two-bench CONTINUE is reclassified as a position-detector correlation, never erased.*

---

## 5. Falsification decision tree

```
Phase 0 — bench-3 construction (the breaking point)
 ├─ any §3.2 design-time assertion fails (vocab/family freshness, cells,
 │   extraction contract, label check, ID namespace, canonical rebuild) → RUN-INVALID (construction)
 ├─ G-C1 pure-template detector > 36/60 → RUN-INVALID (construction: template-decodable bench)
 ├─ G-C2 |Pearson(r1,r3)| > 0.10 → RUN-INVALID (construction: not decorrelated from bench 1)
 ├─ G-C3 template decomposition not independently pinnable → RUN-INVALID (construction)
 ├─ position-scramble gate: pure-position detector > 36/60 → RUN-INVALID (construction: position informative)
 └─ ALL PASS → canonical bench-3 JSON pin recorded; per-item records written
     └─ canonical bench-3 JSON pin recorded; per-item records written
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
                                  │    EXP111/EXP120 observations stand; two-bench CONTINUE
                                  │    reclassified as position-detector correlation)
                                  │    (takes precedence over any overall score)
                                  ├─ G < 0.30 and overall ≥ 20/30 → CONTINUE
                                  │    (identity readout survives position decorrelation —
                                  │    decodability only, §7)
                                  ├─ G < 0.30 and overall = 19/30 → HELD (underpowered; no rescue)
                                  └─ G < 0.30 and overall ≤ 18/30 → KILL (no identity readout on bench 3;
                                       two-bench CONTINUE reclassified as position-detector correlation)
```

No other branches exist. No re-runs, no re-seeds, no post-hoc bars (Law #4, Law #9).

---

## 6. What this protocol explicitly does NOT do

1. **No secondary per-layer analysis.** H17 (standalone layer-profiling) was rejected at the design session (LOG-4638) because it names no decision a profile changes; H16's decision is fully fired by the primary layer-20 bar. Folding layer-resolved bars into H16 would be H17 through the back door — explicitly barred. EXP111 §7 layer numbers enter only as mathematical-license context (§1.1 citation above) and license no verdict.
2. No re-reading of bench-1 or bench-2 data, no re-fitting on bench-1/2 embeddings, no re-cutting the fixed EXP111/EXP120 splits (Law #13 fence, §8).
3. No cross-bench effect-size comparisons (no post-hoc cross-bench t-test — the split is powered for the bar, not for comparisons).
4. **No logit channel.** H16 is an embedding-readout design; there is no plan-context composition, so defect class (e) — the [-3:] tokenization-identity pin — does not bind. Stated explicitly so no reviewer later demands it.
5. **No single-token assertion.** The readout is a trained logistic head on final-token embeddings of full premises, not a logit-level single-token decode; H18's multi-token finding (LOG-4639) binds only logit-channel benches and does not bind here. Stated explicitly (defect class (f)).

---

## 7. Cost and honesty

- **$0 CPU, ~1.5h.** Bench-3 construction (pure string authoring, no model calls); 60 layer-20 CPU forward passes (~30–60 min, Δθ=0); logistic fit + bookkeeping + determinism pass on archived bench-3 embeddings. No generation anywhere.
- **Honesty ledger:** (a) the test set is n=30 — powered for the pre-registered bar (20/30, p=0.0494) but not for fine distinctions; (b) a CONTINUE licenses only **"identity readout survives position decorrelation"** — decodability, **not steering or capability** — the head extracts a domain-set property of the target at layer 20, nothing more; (c) the verdict bars are properties of the protocol **plus the pinned identity-label design** (§2 disclosure) — a different label design is a different hypothesis, not an amendment; (d) no generality beyond bench 3, the layer, or the model is claimed (§8).

---

## 8. What H16 does NOT claim

1. A CONTINUE is a **correlation at one layer on three benches** — it is not consciousness, not generality beyond the benches, not superhuman cognition.
2. A CONTINUE does not claim capability beyond the task: downstream causal tests (steering, decision-flip) are required before any capability statement. The capability scoreboard stays at zero positive signals for autonomous steering.
3. A CONTINUE does not re-license H1/H4, static-injection lines, or any closed family.
4. A KILL retires only the **identity-readout interpretation** — it does not erase EXP111's or EXP120's bench observations (Law #8); their CONTINUE is reclassified as a position-detector correlation under Law #11's two-layer tagging, never un-happened.
5. Law #13 fence: bench 3 is an independent apparatus — no re-reading of bench-1/2 data, no re-fitting, no re-cutting. The G-C2 correlation gate compares bench-3's construction against bench-1's builder records as a design check only; it feeds no bench-1/2 labels or embeddings into the analysis.
6. Novelty: **N1 — Known Combination.** Trained linear probes on decorrelated benches are a known combination; no new mechanism is claimed (Law #10).
7. No layer-resolved or logit-level claims of any kind.

---

## 9. Deviations from the dossier and from H5/H15 (complete list)

1. **Bench-3 construction phase prepended** (the breaking point): construction discipline with design-time assertions and four quantitative gates (G-C1, G-C2, G-C3, plus the new position-scramble gate) whose failure voids the item before any head is trained — the H15 discipline carried over with the new gate added.
2. **Label semantics re-designed, protocol carried verbatim:** bench-3 labels encode the target's identity (domain-set membership) instead of the position feature; the H5 *protocol* (head spec, split seed, extraction site, bars, gates, record-keeping) carries byte-verbatim — the label definition does not (§2 disclosure). This is the design change the H16 gate requires for the test to be discriminative.
3. **New position-scramble gate (§3.2):** the pure-position detector must score ≤ 36/60 on the constructed bench (constructor-side validation before any head is trained) — the gate that makes position-decoy vs identity-readout separable.
4. **No convergence gate:** a non-converged lbfgs fit is a reported defect, not a gate (§3.5) — simpler than a convergence bar, avoiding an unlicensed veto.
5. **Record-keeping artifact-existence gate retained** (§3.7): the EXP119 lesson — with the defect-class (b) adaptation: zero generation in H16, so the gate pins raw embeddings + head weights instead of raw generations.
6. **Defect classes (d)–(f) explicitly N/A:** no EXP117 recitation reuse (zero generation), no [-3:] identity pin (no logit channel), no single-token assertion (embedding apparatus) — each stated explicitly in §6 so reviewers do not demand them post-hoc (§6 items 4–5).
7. **H17 explicitly not folded in:** no per-layer secondary, no descriptive layer numbers as bars (§6 item 1) — the EXP111 §7 layer profile enters only as mathematical-license context.
8. **Cross-bench effect-size comparisons explicitly unlicensed** (§2): the gate memo's quantitative prediction is honored only as directional prediction under each hypothesis; no post-hoc t-test between benches.

---

## 10. Boundary

**What this protocol cannot show:** (a) whether the identity-readout signal, if CONTINUE, is causal — steering/decision-flip tests are required before any capability statement (§8); (b) whether the signal exists at any other layer, bench, or model — one bench, one layer (20), one model; (c) whether the label-free race (H18) or any steering mechanism exists — H16 does not compete with it.

**Summit filter:** **NO — boundary-science dissection, not a summit move.** It adds no capability, routing, or self-improving loop. It is worth it only as license-maintenance for the two-bench line: a position-detector finding kills any mechanistic use of the signal, and an identity-readout finding gives the program's best observation its first mechanistic foothold. The label-free race (H18) remains the actual race; this lane does not compete with it.

**H17 stays rejected:** H17 (standalone layer-profiling) was rejected at the design session (LOG-4638) and is not resurrected here — no layer-resolved bars, no contingent per-layer secondary, no descriptive layer numbers licensing any verdict (§6 item 1). This boundary is explicit so no review later reads H16 as a partial H17.

Independent Law #14 review of this exact file is a separate lane. No experiment number is minted by this draft. Execution, if ever launched, is a CEO decision under a minted number. This lane stops here.
