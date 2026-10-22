# Pre-registration: H5 — LFH-TD (Label-Free Head on the Template-Decorrelated Bench)

**Status:** DRAFT pre-registration. Licenses nothing. No model runs, no experiment number minted, no signed protocol touched, no GPU contact, no commits, no pushes. $0 CPU.
**Drafting lane:** LOG-4563 (pre-assigned). **Source:** `research/innovation/SPRINT_2026-09-29_SUMMIT_ROUND2.md` §H5 (worth-it gate passed, ranked #1).
**Launch chain:** independent Law #14 review of this exact file → fix-verification (if fixes required) → CEO launch decision → execution under a minted experiment number. This lane stops at the draft.

**Governing laws:** Law #4 (no post-hoc hypothesis shifts — the bars below are binding), Law #6 (frozen backbone Δθ=0), Law #7 (zero data leakage — extended below to every model-selection decision), Law #9 (metrics registered before any output is inspected), Law #13 (deterministic reproducibility — seeds, hashes, environment manifest pinned below).

**Epistemological labels** per `SCBI/AGENTS.md` §5: [OBSERVATION], [HYPOTHESIS], [INTERPRETATION], [PROPOSITION], [ASSUMPTION].

---

## 1. Hypothesis (one falsifiable sentence)

**[HYPOTHESIS]** A linear head trained on frozen Pythia-410m layer-20 embeddings scores above chance on a held-out template-decorrelated bench, i.e., the trained readout extracts the position feature from the frozen backbone when word-template cues are decorrelated from labels.

### 1.1 Why this experiment exists

[OBSERVATION] EXP106's head scored 60/60 (p=8.67×10⁻¹⁹) on a template-correlated bench; EXP107's kill-test proved the reading was surface-template detection (34/60, p=0.1831, with the exact template-detector signature: 30/30 on original-word cells, 4/30 on flipped-word cells). The EXP106 transfer reading is dead; the GPU head-training proposal it licensed is void. H5 is the honest successor: re-test the trained-head hypothesis on the EXP107 decorrelated bench, where the template trap is neutralized by construction, with the EXP107 signature pre-installed as a kill-test. If H5 scores above chance with the right signature, it is the day's first genuine positive-signal candidate. If it matches the EXP107 template signature, it dies as another template detector.

---

## 2. Exact question and the decision it changes

**Exact question [HYPOTHESIS]:** Does a trained linear head on the frozen backbone transfer above chance when trained and evaluated on a bench where word-template cues are decorrelated from labels (disjoint split, zero template-label correlation in train and test by construction)?

**Decision changed:**
- **CONTINUE** the output-side capability program: first autonomous output-side result; re-licenses the GPU head-training proposal (voided by EXP107) under the decorrelated-bench discipline.
- **KILL** the output-side readout program: even trained linear readouts don't transfer on a template-decorrelated bench; the room is template-artifact-only — retire it, and deepen the EXP107 interpretation.
- **HELD** (registered): borderline zone — neither continue nor kill; no rerun, no larger-N rescue.

**PIVOT** does not appear in H5's outcome set. The dossier's "any above-chance → CONTINUE" is replaced by the bar in §4.

---

## 3. Method

### 3.1 No-generation protocol [ASSUMPTION]

H5 requires **zero generation** (forward-pass-only extraction for the secondary analysis; pure logit/vector arithmetic otherwise). This is a hard constraint from the EXP108/EXP109 RUN-INVALID lesson. No autoregressive decoding appears anywhere in this design.

### 3.2 Data and provenance [PROPOSITION]

- **Input artifact:** `experiments/runs/EXP107_templatectrl/out/exp107_test_embeddings.npz` — verified present: `embeddings` (60, 1024) float32, `ids` (60,) str. All 60 IDs byte-match the per-item JSON (`exp107_per_item.json`), which carries labels `y`, `phrasing` ∈ {A-first, C-first}, `flipped` ∈ {True, False}, all verified by the drafting lane.
- **Embedding site:** `hidden_states[20]`, final token, float32, CPU (EXP107 read-site, verified in the EXP107 report) — frozen Pythia-410m, layer 20. No new forward passes for the primary analysis (zero-cost archived embeddings).
- **Bench structure [OBSERVATION]:** 60 items in four balanced 15-item cells — (A-first, original-word) ×15, (A-first, flipped-word) ×15, (C-first, original-word) ×15, (C-first, flipped-word) ×15. Labels y=1 iff A-first (the intended position feature; EXP107 noted the test does not distinguish word-template from subject-position cue — the position cue is the legitimate signal here). Word-template cues are decorrelated from labels by construction: a pure template detector scores ≈ 30/60 [OBSERVATION, EXP107].
- **Provenance pin (Law #13):** the execution lane records the sha256 of the npz before any training and verifies byte-identity against the reference values below; any drift → HALT. Reference hashes (independently recomputed from `experiments/runs/EXP107_templatectrl/out/exp107_test_embeddings.npz` by the LOG-4565 repair lane and matching the independent review): npz file `6cf4a8a726a2b6e4623f57d0287d95879866f77e789bcc3789fb693cf2af6a76`; embeddings-array bytes (60×1024 float32) `9b6e8afb091ba1edbb0311ba1d3414d34a65942c3fdecb4533b69720f2a99123`; ids-array bytes `3669e102222719d66f61daca46ae1ac34e844e398ae433743a5b37bfc5075cb9`.

### 3.3 Split and training [PROPOSITION]

- **Disjoint stratified split:** `train_test_split` (**sklearn==1.9.1**, **numpy==2.5.3** — the EXP107 report's environment; both recorded in the execution worksheet), `test_size=0.5`, **seed pinned: 20260929**, stratified by the pinned 4-cell key `f"{phrasing}_{flipped}"` with phrasing ∈ {"A-first", "C-first"} and flipped ∈ {False, True}. Under sklearn 1.9.1 + seed 20260929 the test counts per cell in sorted key order are deterministically **8/8/7/7** — ("A-first", original-word): 8, ("A-first", flipped-word): 7, ("C-first", original-word): 7, ("C-first", flipped-word): 8 — → **train n=30, test n=30** with **N_F=15 flipped=False** and **N_T=15 flipped=True** test items (8+7 and 7+8). The exact train/test item-id lists and the observed N_F, N_T are written to the run log; disjointness is asserted (any overlap → RUN-INVALID).
- **Head:** `LogisticRegression(penalty='l2', C=1.0, solver='lbfgs', max_iter=1000, random_state=20260929)`. All hyperparameters pinned here — **no tuning** (Law #7 extended to every model-selection decision: no L2-C sweep, no layer choice, no solver choice, no seed re-rolls; the EXP106 review lesson).
- **Law #7 posture:** test labels are used only for the final registered evaluation; no test-informed selection anywhere. Train labels are the bench's own labels — the pre-registered use. The split seed is pinned before execution.

### 3.4 Block-off byte-identical discipline (LOG-4528 adoption) [PROPOSITION]

The JEV-27B-adopted discipline for frozen-backbone + attached-module claims applies here in its "no backbone contact" form: the backbone is **never loaded** in the primary analysis, so no attached module can perturb it. Checks: (a) input artifact hash pinned pre-training; (b) head weights derived only from the pinned train split; (c) determinism pass — re-fit from the same artifact and assert byte-identical test predictions; (d) final weight-hash logged. Any mismatch → RUN-INVALID.

### 3.5 Δθ=0 (Law #6) [PROPOSITION]

Satisfied structurally: no backbone is loaded, no weights are touched, no adapters exist. The only trained parameters are the logistic head's (w, b) on the pinned train split.

### 3.6 Metrics [PROPOSITION]

Primary: overall accuracy on the 30 held-out test items. Secondary (kill-test): per-cell accuracies — specifically the template-detector signature gap:
**G = acc(N_F flipped=False test items) − acc(N_T flipped=True test items)** (N_F=15, N_T=15 under the pinned split encoding; both logged in the worksheet). Also reported descriptively: per-cell (4-cell) accuracies, train accuracy (sanity only — no bar on it), head weight norm.

---

## 4. Decision bars with statistical license

n=30 test items, one-sided binomial vs chance (p=0.5), α=0.05: the critical value is **20/30** (exact one-sided p=0.0494; 19/30 → p=0.1002 — fails the bar). All values verified by the drafting lane.

- **CONTINUE:** overall test accuracy **≥ 20/30** (p ≤ 0.0494) **AND** no template-detector signature (**G < 0.30**).
- **KILL:** template-detector signature present (**G ≥ 0.30** — a ≥5-item gap at the pinned N_F=N_T=15 denominators; the registered EXP107 signature produced G = 30/30 − 4/30 = 0.867) **regardless of overall score**; OR overall test accuracy **≤ 18/30** (p ≥ 0.1808).
- **HELD:** overall = **19/30** with G < 0.30. Underpowered zone: neither continue nor kill; no rerun, no larger-N rescue (the EXP106 no-rescue discipline applies).

**Pre-installed kill-test, one sentence:** *If the trained head reproduces the EXP107 template-detector signature — high accuracy on original-word test items but at-chance accuracy on flipped-word test items (G ≥ 0.30) — the autonomous-transfer reading is KILLED, and the head is reclassified as a template detector, with no rerun or larger-N rescue.*

---

## 5. Falsification decision tree

```
sha256(exp107_test_embeddings.npz) pinned (§3.2 reference hashes)
 ├─ hash ≠ expected → HALT (apparatus drift; licenses nothing)
 └─ hash OK
     └─ stratified 30/30 split (seed 20260929, pinned key encoding)
         ├─ train/test ID overlap → RUN-INVALID (Law #7, §3.3)
         └─ disjoint
             └─ train L2-logreg → determinism re-fit pass (§3.4(c))
                 ├─ predictions ≠ byte-identical → RUN-INVALID (block-off discipline)
                 └─ determinism OK → evaluate on 30 held-out
                     ├─ G ≥ 0.30 → KILL (template-detector signature; transfer reading dead)
                     │    (takes precedence over any overall score)
                     ├─ G < 0.30 and overall ≥ 20/30 → CONTINUE (autonomous output-side transfer;
                     │    re-licenses GPU head-training under decorrelated-bench discipline;
                     │    secondary per-layer analysis licensed, §6)
                     ├─ G < 0.30 and overall = 19/30 → HELD (underpowered; no rescue)
                     └─ G < 0.30 and overall ≤ 18/30 → KILL (no transfer on the decorrelated bench;
                          output-side readout room retired as template-artifact-only)
```

No other branches exist. No re-runs, no re-seeds, no post-hoc bars (Law #4, Law #9).

---

## 6. Secondary registered analysis (contingent on CONTINUE only)

If and only if the primary lands **CONTINUE**, the execution lane is licensed to run one bounded secondary analysis, in the same run, under this pre-registration: repeat the identical protocol (§3.3–§3.6, same seeds, same bars, no per-layer tuning) on layer-wise final-token embeddings extracted fresh at layers **4, 8, 12, 16** (60 items each, frozen Pythia-410m CPU, seed-pinned, Δθ=0). The secondary's environment is pinned: **torch==2.14.0+cpu**, **transformers==5.17.0**, CPU thread count set and read back via `torch.get_num_threads()` — all recorded in the execution worksheet. Backbone-contact discipline (the primary never loads the backbone; the secondary does): the backbone hash is verified against the LOG-331 pin **before and after** the fresh layer 4/8/12/16 extraction (Δθ=0); the secondary extracts the **same 60 bench items by ID**. Reported descriptively with the same decision bars per layer — **per-layer bars are descriptive-only and license no verdict** (four layers at α=0.05 carry ~18.5% family-wise false-positive rate; hence no multiplicity correction beyond the SECONDARY label). This replaces the dossier's standalone "per-layer trained-head transfer search" lane (killed at the gate as a standalone candidate).

---

## 7. Cost and honesty

- **$0 CPU, ~1h.** Primary analysis uses archived embeddings (zero new forward passes): logistic fit + bookkeeping + determinism pass. The secondary analysis, if licensed, adds 240 forward passes (~30–60 min CPU).
- **Honesty ledger:** (a) the test set is n=30 — powered for the pre-registered bar (20/30, p=0.0494) but not for fine distinctions; (b) the bench's labels encode the subject-position cue (A-first → y=1), so a CONTINUE means the head extracts *position*, not templates — this is a legitimate frozen-backbone signal but a narrow one; (c) no generality beyond the bench, the layer, or the model is claimed (§8).

---

## 8. What H5 does NOT claim

1. A CONTINUE is a **correlation at one layer on one bench** — it is not consciousness, not generality, not superhuman cognition.
2. A CONTINUE does not claim capability beyond the task: downstream causal tests (steering, decision-flip) are required before any capability statement.
3. A CONTINUE does not re-license H1/H4, static-injection lines, or any closed family.
4. A KILL does not say "linear heads can never transfer" — it retires only the output-side readout room on this bench class, deepening EXP107.
5. Novelty: **N1 — Known Combination.** Trained linear probes on decorrelated benches are a known combination; no new mechanism is claimed (Law #10).

---

## 9. Deviations from the dossier (complete list)

1. **Test n reduced 60 → 30.** The dossier's bar ("≥ 40/60 on the held-out decorrelated split, binomial p ≈ 0.003 vs 0.5") is mathematically incompatible with its own "disjoint split within the bench" design: the bench has 60 items total, so a disjoint train/test split cannot yield a 60-item held-out set. The draft replaces it with a stratified 30/30 split and bars at n=30 (CONTINUE 20/30, p=0.0494). The power loss is honest: the bar still clears α=0.05 one-sided.
2. **HELD zone added** (19/30, p=0.1002): the dossier's breaking point ("≤ 35/60 → KILL") left no room between the bar and the floor; the draft registers the single razor case explicitly rather than forcing a verdict.
3. **Kill-test signature formalized as G ≥ 0.30** (15-vs-15 test items): the dossier said "template-detector signature present → KILL" without a numeric criterion; the draft pins the threshold (EXP107 produced G=0.867, so 0.30 is conservative and still signature-shaped).
4. **Per-layer search folded as a bounded secondary analysis** (layers 4/8/12/16, CONTINUE-contingent) rather than left as an implicit future lane — the dossier killed the standalone lane and said "folded as a secondary registered analysis"; this draft specifies the fold.
5. **Block-off discipline specified in its "no backbone contact" form** (§3.4): the dossier invoked the JEV-27B discipline without saying how it applies to a no-forwards design; the draft pins the hash-based and determinism-pass checks.

---

## 10. Boundary

Independent Law #14 review of this exact file is a separate lane. No experiment number is minted by this draft. Execution, if ever launched, is a CEO decision under a minted number. This lane stops here.
