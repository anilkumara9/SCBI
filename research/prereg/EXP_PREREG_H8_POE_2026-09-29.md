# Pre-registration: H8 — POE (Positional-Order Ensembling)

**Status:** DRAFT pre-registration. Licenses nothing. No model runs, no experiment number minted, no signed protocol touched, no GPU contact, no commits, no pushes. $0 CPU.
**Drafting lane:** LOG-4588 (pre-assigned). **Source:** `research/innovation/SPRINT_2026-09-29_SUMMIT_ROUND2.md` §H8 (worth-it gate passed, ranked #4).
**Launch chain:** independent Law #14 review of this exact file → fix-verification (if fixes required) → CEO launch decision → execution under a minted experiment number. This lane stops at the draft.

**Governing laws:** Law #4 (no post-hoc hypothesis shifts — the bars below are binding), Law #6 (frozen backbone Δθ=0), Law #7 (zero data leakage — no bench labels touch the apparatus; no order-count tuning after results), Law #9 (metrics registered before any output is inspected), Law #13 (deterministic reproducibility — seeds, hashes, environment manifest pinned below).

Epistemic labels follow `SCBI/AGENTS.md` §5 (`[HYPOTHESIS]`, `[PROPOSITION]`, `[ASSUMPTION]`, `[OBSERVATION]`, `[INTERPRETATION]`, `[FACT]`).

---

## 1. Hypothesis (one falsifiable sentence)

**[HYPOTHESIS]** Averaging entity-name logits over K=5 randomized option-presentation orders improves the frozen backbone's decision accuracy on the 60-item EXP107 template-decorrelated bench above the single canonical-order baseline by a decision-grade margin — paired exact McNemar one-sided p ≤ 0.05.

**Falsifiers:** net improvement ≤ 0 (ensemble accuracy ≤ baseline accuracy) → the positional-order ensembling axis is dead for this task class; net improvement > 0 but paired p > 0.05 → underpowered (HELD), not a positive.

---

## 2. Exact question and the decision it changes

**Exact question [HYPOTHESIS]:** At fixed frozen backbone, does averaging option logits over randomized presentation orders beat a single-order readout on the 60-item bench — i.e., does test-time computation buy decision accuracy with zero generation?

**Decision changed:**
- **CONTINUE:** paired exact McNemar one-sided p ≤ 0.05 (ensemble > baseline) → the test-time-scaling axis is alive; order-ensembling enters the EXP068-family adaptive-loop designs as a registered component.
- **KILL:** net ≤ 0 → presentation averaging adds nothing; the positional-order-ensembling TTA axis is dead for this task class.
- **HELD:** net > 0 but p > 0.05 → underpowered zone; licenses nothing, retires nothing; the only permitted next step is a separately pre-registered K-increased follow-up (which must pass its own worth-it gate — no automatic re-run, Law #4).

---

## 3. Method

### 3.1 Item set and labels [PROPOSITION]

The 60-item EXP107 template-decorrelated bench, rebuilt deterministically via `experiments/runs/EXP107_templatectrl/build_exp107_bench.py: build_bench()` (no model calls, no RNG). Four balanced 15-item cells: (A-first/C-first) × (original/flipped word families). Provenance pin: before any forward pass, the executor asserts the SHA-256 of the canonical bench JSON equals `e91b302f41f641c74e56957e526efcd4866bac62d134e157defe0a4cdd49e4f5` (the H6/EXP112-registered pin); mismatch → HALT. `len(bench) == 60` asserted.

Labels: the bench's registered `y` — `y=1` iff phrasing is A-first (target `tuple[0]` first-mentioned in the premise), `y=0` otherwise; balanced 30/30 (`run_exp107.py:94`). Accuracy is agreement of the entity prediction with `y`: prediction maps to 1 if `tuple[0]`, 0 if `tuple[1]`; `correct_i = 1[pred_i == y_i]`.

No training. No train/test split (nothing is trained — the comparison is paired on all 60 items). Labels are used only for the final accuracy computation, never by the apparatus.

### 3.2 Prompt construction (pinned byte-exact) [PROPOSITION]

The bench items carry no option list — the execution lane constructs order-varied prompts by a pinned rule. Let `premise_i` be the bench's stored premise (starts with `"Premise: "`), `E1_i = tuple[0]`, `E2_i = tuple[1]` the two entity names, and `QUESTION_SUFFIX = " Question: Who is higher in rank? Answer:"` (byte-exact, `build_exp107_bench.py:53`).

For order bit `o ∈ {0, 1}`:
```
prompt(i, o) = premise_i + " Options: " + first + ", " + second + "." + QUESTION_SUFFIX
```
where `(first, second) = (E1_i, E2_i)` if `o = 0` (canonical order = the bench's stored tuple order), else `(E2_i, E1_i)` (swapped).

No letters appear anywhere in the option list — the list is unlabeled, so there is no letter-mapping construct-validity question (the EXP109 lesson). The insertion format is byte-identical across all items and both orders except the entity permutation, which is the experimental variable.

### 3.3 Order-generation scheme (K=5, pinned) [PROPOSITION]

For each item (in canonical bench order), draw 5 i.i.d. order bits from `{0, 1}` using Python `random.Random(20260929)` (pinned seed, pinned RNG). Bit 0 → canonical order, bit 1 → swapped. The 5-bit pattern per item is logged in the execution worksheet (so the analysis reports how many items received degenerate 5–0 compositions — expected ≈ 6% of items under i.i.d. draws; this is the dossier's K=5 design, kept as specified).

The **baseline** is a separate registered forward pass per item with the canonical order (`o = 0`), not one of the ensemble draws.

**[ASSUMPTION]** The K=5 i.i.d. scheme is the dossier's pinned design. With only 2 distinct permutations, the 5-draw mean is an unbiased estimate of the 50/50 order average; the variance-reduction logic (dossier §H8.4) goes through regardless of per-item composition.

### 3.4 Readout and answer extraction (entity names, no letters) [PROPOSITION]

One forward pass per constructed prompt (frozen Pythia-410m, CPU, float32, greedy — no sampling; position-0 logits at the final answer position *are* the measurement; zero generation).

Let `t1_i = encode(" " + E1_i)[0]`, `t2_i = encode(" " + E2_i)[0]` — the pinned single-token entity-name ids (the H6 readout contract). **Single-token BPE assertion:** the executor asserts `encode(" "+E)` is exactly one token on the real Pythia tokenizer for every entity of every item; any failure → **RUN-INVALID** (items are NOT silently dropped).

Per (item, order): read `logit[t1_i]`, `logit[t2_i]` from the single forward pass. **Tie-break (pinned):** exact float-equality ties → `tuple[1]` (E2), mirroring H6's conservative tie-break.

**Why this is construct-valid (the EXP109 lesson):** the decision is defined directly on entity names — argmax over the two pinned entity token ids. No letter tokens are ever read as answers, so no letter-mapping definition is required. The readout is the logit analogue of H6's registered self-report read.

### 3.5 Ensemble and baseline decisions [PROPOSITION]

- **Ensemble prediction:** `pred_ens_i = argmax_e mean_{k=1..5} logit_e(prompt(i, o_{ik}))`, with the §3.4 tie-break.
- **Baseline prediction:** `pred_base_i = argmax_e logit_e(prompt(i, 0))`, with the §3.4 tie-break.
- **Accuracies:** `acc_ens = (1/60) Σ correct_ens_i`, `acc_base = (1/60) Σ correct_base_i`, against the §3.1 labels.

### 3.6 Metric and statistical test (registered) [PROPOSITION]

**Primary metric:** the paired outcome table (ensemble vs baseline) on the same 60 items. Let `b` = #{baseline wrong, ensemble right} (fixes), `c` = #{baseline right, ensemble wrong} (breaks). **Registered test:** paired exact McNemar, one-sided (Hₐ: ensemble > baseline): `p = P(X ≥ b | n = b+c, 0.5)`.

**Degenerate table (pinned):** if `b = c = 0` (ensemble and baseline agree on all 60 items), the test is undefined — this is registered as net = 0 → **KILL** (no improvement observed; ensembling adds nothing on this bench).

**Descriptive-only secondary:** per-cell (phrasing × flipped) ensemble-vs-baseline accuracies, reported descriptively; no decision branch reads them.

### 3.7 Template-trap posture [PROPOSITION]

Template-free by construction, on two independent grounds:
1. The EXP107 bench is template-decorrelated by construction (phrasing × word-family balanced 4×15; EXP107 verified a pure template detector scores ≈ 30/60).
2. The H8 apparatus introduces no new wording: the option-list insertion is byte-identical across items except the permuted entity order (the experimental variable); the readout is over entity-name tokens; no training occurs; no labels touch the apparatus (§3.1). There is no template left to detect — the only thing that varies across the K orders is which entity is listed first.

### 3.8 Law #7 — no tuning freedoms [PROPOSITION]

Pinned with zero residual freedom: K=5, seed 20260929, RNG `random.Random`, i.i.d. bit scheme, canonical baseline order, option-insertion format (§3.2), entity token ids via the BPE assertion, tie-break, McNemar one-sided α=0.05. The order count, seed, prompt format, and decision rule may not be adjusted after any output is inspected (Law #4, Law #7).

### 3.9 Frozen backbone Δθ=0 [PROPOSITION]

Backbone verified against the LOG-331 pin `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed` (canonical sorted-`state_dict`-keys hash method, per the EXP110/EXP112 execution reports) **before the first forward pass and after the last**. Any mismatch → RUN-INVALID. The backbone is never modified; all 360 forwards are read-only inference.

### 3.10 Law #13 environment and determinism [PROPOSITION]

The execution worksheet records: exact torch/transformers versions, CPU thread count set and read back via `torch.get_num_threads()`, the pinned seed, the per-item 5-bit order patterns, and the backbone pin before/after. All 360 prompts are reconstructible byte-exactly from the bench + seed + §3.2 rule (deterministic re-run must reproduce all predictions).

---

## 4. Decision bars with statistical license

- **CONTINUE:** paired exact McNemar one-sided p ≤ 0.05 with b > c → the TTA axis is alive; order-ensembling enters the adaptive-loop designs. Canonical minimum: `(b, c) = (5, 0)` → p = (1/2)⁵ = 0.03125.
- **HELD:** net (b − c) > 0 but p > 0.05 → underpowered; licenses nothing, retires nothing; only a separately pre-registered K-increased follow-up is permitted (own worth-it gate required).
- **KILL:** net ≤ 0 (including the b = c = 0 degenerate case) → presentation averaging adds nothing; the positional-order-ensembling axis is dead for this task class.

**Statistical honesty (disclosed):** with n = 60, the paired test reliably detects decision-grade effects (≥ 5 net flips with clean discordance); smaller true effects (≈ 2–4pp) land in HELD by design — the test is powered for the dossier's claimed effect class, not for fine-grained TTA gains. The (4,0) table gives p = 0.0625 > 0.05: four clean flips are *not* enough, and the pre-reg does not pretend otherwise.

---

## 5. Falsification decision tree

```
bench pin check (e91b302f…4f5)
 ├─ mismatch → HALT (bench drift; licenses nothing)
 └─ match ✔
     backbone LOG-331 pin check
     ├─ mismatch → RUN-INVALID
     └─ match ✔
         BPE single-token assertion (all entities, all items)
         ├─ any failure → RUN-INVALID (items NOT dropped)
         └─ pass ✔
             360 forwards (300 ensemble + 60 baseline) → per-item predictions
             backbone pin re-check → mismatch → RUN-INVALID
             └─ paired exact McNemar one-sided on (b, c)
                 ├─ p ≤ 0.05, b > c → CONTINUE (TTA axis alive; order-ensembling
                 │    enters adaptive-loop designs)
                 ├─ b − c > 0, p > 0.05 → HELD (underpowered; K-increased
                 │    follow-up only via separate pre-registration)
                 └─ b − c ≤ 0 (incl. b = c = 0) → KILL (axis dead for this
                      task class)
```

No other branches exist. No re-runs, no larger K, no post-hoc bars (Law #4, Law #9).

---

## 6. Cost and honesty

- **$0 CPU, ~2–4h**: 360 forward passes on frozen Pythia-410m CPU (300 ensemble + 60 baseline) + hash checks + analysis. Zero generation (forward passes + pure logit arithmetic only — the EXP108/EXP109 lesson is structural here: the design cannot degenerate the way generation protocols did).
- **Honesty ledger:** (a) the test detects option-*list* positional bias cancellation, not premise-position bias (the premise order is identical across all K+1 prompts per item); (b) a CONTINUE licenses order-ensembling as an adaptive-loop *component*, not a capability claim; (c) single bench (60 items), single model — no generality beyond.

---

## 7. What H8 does NOT claim

1. An ensembling gain is not reasoning, not consciousness, not a capability beyond this bench — it is variance reduction over a presentation nuisance variable.
2. A CONTINUE does not claim the model "understands" order-invariance — only that averaging over orders improves the registered decision.
3. A KILL retires only the positional-order-ensembling axis for this task class — not test-time scaling in general, not the adaptive-loop program.
4. No claim about trained heads (H5's room), honesty (H6's room), or elicitation (H7's room).
5. **Novelty: N1 — Known Combination.** Positional-bias ensembling is known in the literature; the combination with this bench/apparatus is the contribution (Law #10).

---

## 8. Deviations from the dossier (complete list)

1. **Forward count 600 → 360.** The dossier's "60 items × K=5 orders × 2-option logit readouts = 600 forward passes" double-counts: one forward pass yields logits for the full vocabulary, so both entity logits are read from a single pass. Correct count: 300 ensemble + 60 baseline = 360. Cost honesty: ~2–4h CPU (not ~2h for a miscounted 600).
2. **Dossier's "+3/60 → p ≤ 0.05" is mathematically wrong.** (b,c) = (3,0) gives exact one-sided p = 0.125 > 0.05. Replaced with the exact McNemar rule; canonical minimum (5,0) → p = 0.03125 (verified).
3. **Dossier's "p > 0.05 → KILL" lumped the underpowered case with the negative case.** Added HELD for net > 0 but p > 0.05 (mirrors the H5/H6/H7 held-zone structure); KILL is now exactly net ≤ 0.
4. **Degenerate table pinned:** b = c = 0 → KILL (net = 0). The dossier did not address the undefined-test case.
5. **Tie-break pinned** (ties → E2/tuple[1], mirroring H6). The dossier did not specify one.
6. **Baseline pinned** as the bench's canonical stored tuple order. The dossier said "single canonical order" without specifying which.
7. **Order-generation scheme pinned** (i.i.d. bits, `random.Random(20260929)`, per-item patterns logged). The dossier said "K random orders" without a scheme or seed.
8. **Option-list prompt construction pinned byte-exactly** (§3.2). The dossier did not specify how options are presented.
9. **Answer extraction on entity-name tokens, no letters** (the EXP109 construct-validity lesson). The dossier did not specify the readout; letter-based readout would have repeated EXP109's undefined-mapping defect.

---

## 9. Boundary

Independent Law #14 review of this exact file is a separate lane. No experiment number is minted by this draft. Execution, if ever launched, is a CEO decision under a minted number. This lane stops here.
