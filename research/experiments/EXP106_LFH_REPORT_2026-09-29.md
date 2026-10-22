# EXP106 (H3/LFH) — Execution Run Report

**Date:** 2026-09-29
**Lane:** LOG-4534 (execution; pre-assigned)
**Launch chain:** pre-reg drafted LOG-4529 → independent Law #14 review SIGN-WITH-FIXES LOG-4530 → three fixes applied LOG-4531 → fixes verified ALL-FIXES-VERIFIED, review upgraded to SIGN LOG-4532 → CEO launch decision LOG-4533 → this execution.
**Signed pre-registration:** `research/prereg/EXP_PREREG_H3_LFH_2026-09-29.md` (executed exactly; no modifications to any signed artifact).
**$0 CPU.** No GPU contact. No push. No credentials.

---

## 1. Environment [FACT]

| Component | Version |
|---|---|
| torch | 2.14.0+cpu |
| transformers | 5.17.0 |
| numpy | 2.5.3 |
| scikit-learn | 1.9.1 (installed into `~/.venv-exp077` for this run; CPU-only) |
| Backbone snapshot | `/home/hatch/workspace/.exp086_weights/pythia-410m` (canonical relocated snapshot per signed EXP092 v2.1 protocol) |
| Head | `LogisticRegression(penalty='l2', C=1.0)`, all other params default (lbfgs; `n_iter_=[18]`, converged) |

## 2. Backbone hash check — Law #6 [OBSERVATION]

SHA-256 over the loaded `state_dict` (292 tensors, sorted keys, float32 bytes — byte-identical replica of the EXP077/EXP091/EXP092 `compute_state_dict_hash`):

- Pre-extraction: `ec276abe3902fab0…` — **match** (Δθ=0 verified before any forward pass)
- Post-train-extraction: `ec276abe3902fab0…` — **match**
- Final (after block-off passes): `ec276abe3902fab0…` — **match**

Full pin `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed` (LOG-331). No mismatch at any point; no RUN-INVALID condition triggered.

## 3. Embedding extraction spec confirmation [FACT]

Executed exactly per the pinned spec (FIX-2):
- Item encoding: premise-sentences substring — `prompt[:prompt.index(' Question:')]`, asserting `prompt.startswith('Premise:')` (byte-identical logic to the EXP091 extractor's `state_text_of`, verified by pyc disassembly).
- Read site: `hidden_states[20]`, final token `[0, -1, :]`, float32 — **the EXP091 program-standard site as actually implemented** (verified by disassembling `extract_state_embeddings.cpython-312.pyc`: `hidden_states[LAYER]`, `LAYER=20`, `encode(text, add_special_tokens=False)`; no +1 offset).
- `model.eval()`, `requires_grad_(False)` on all parameters, `torch.no_grad()` around all extraction, `device_map="cpu"`, `torch_dtype=torch.float32`.
- One layer, one rule, identical procedure for train and test items.

**Archive admissibility ruling [INTERPRETATION]:** the EXP091 test archive (`exp091_embeddings.npz`, meta records `"layer": 20`) was produced under this exact spec → admissible, used for scoring. The EXP092 archive was produced from **full prompts**, not the premise substring → not admissible under FIX-2 → fresh 60-pass extraction run for the train bench under the pinned spec.

## 4. Train/test sets [FACT]

| | Train | Test |
|---|---|---|
| Bench | EXP092-B (rebuilt via `reference_implementation.build_bench()`; bench pin `9be81626…` **verified**) | EXP091 (archived `state` embeddings) |
| n | 60 | 60 |
| Embedding | fresh extraction, premise-only, hidden_states[20], (60, 1024) float32 | archived, premise-only, hidden_states[20], (60, 1024) float32 |
| Binary label | phrasing: 1 = A-first (30), 0 = C-first (30) | phrasing: 1 = A-first (30), 0 = C-first (30) |

**Label semantics [FACT]:** in both benches `phrasing` = premise sentence-order — A-first ⟺ target entity appears in the first premise sentence (`{A} outranks {B}. …`), C-first ⟺ target appears in the last premise sentence (`{C} is lower than {B}. …`). (EXP091 protocol §6 rationale; EXP092-B reference implementation `_phrasing` + FIX 2 option-order rule.)

## 5. Overlap tripwire — Law #7 [OBSERVATION]

Item-ID intersection (EXP092-B `exp092_*` vs EXP091 `exp077_*`): **0 shared IDs** → tripwire not triggered. No test label, target, or metric touched the training objective. C pinned at 1.0; no tuning of any kind.

## 6. Head training [OBSERVATION]

`LogisticRegression(penalty='l2', C=1.0)` fit on the 60 frozen train embeddings. Train accuracy (secondary, non-binding): **60/60 = 1.0000**.

## 7. Primary result [OBSERVATION]

- **Raw score: 60/60 = 1.0000** on the disjoint EXP091 bench.
- One-sided binomial p-value vs chance (p=0.5): **p = 8.67×10⁻¹⁹** (= 2⁻⁶⁰).
- Per-item log: `experiments/runs/EXP106_lfh/out/exp106_per_item.json` (60/60 correct).

## 8. Block-off byte-identity check [OBSERVATION]

- Test-bench reconstruction (repaired EXP077 builder logic, verbatim): **60/60 item IDs and 60/60 phrasing labels match the archive** — reconstruction validated.
- Fresh backbone-only extraction, two independent passes: **pass1 == pass2 bit-for-bit** (pipeline deterministic).
- Fresh pass vs archived embeddings used for scoring: **byte-identical** (SHA-256 `fe01b33d742be8ce` all three).
- **BLOCK-OFF: PASS.** The head is a pure additive readout; no backbone perturbation. A CONTINUE is not voided.

## 9. Verdict — in the pre-registration's exact language

**Falsification-tree branch taken:** `≥ 40/60, block-off passes` → **CONTINUE.**

Per the pre-reg: *"First autonomous output-side result in-program. Licenses a GPU head-training proposal (separate lane)."*

## 10. What this CONTINUE does and does not license (pre-reg §7 overclaim guards)

- A CONTINUE is a **first positive signal**, not superhuman cognition, not consciousness, not generality beyond the EXP091 bench, and not evidence about internal mechanisms of cognition (the head is a linear extractor — it reports what is present in the embedding, nothing more).
- It licenses **only** a GPU-scale head-training *proposal* (separate lane, founder-gated). It does not license execution, and it does not replicate JEV-27B.
- Novelty remains **N1 — Known Combination** (N2-adjacent only if independently verified).

## 11. Adversarial observation — the template confound [OBSERVATION / INTERPRETATION]

Filed under Law #11 (observation vs interpretation) and Law #14 (challenge rather than defend). This does **not** alter the registered verdict above — the bars are binding — but it determines what the verdict means.

**[OBSERVATION]** The binary label (phrasing) is **deterministically generated by the surface template**, ported verbatim across both benches:
- A-first ⟺ premise uses `{A} outranks {B}. {B} outranks {C}.`
- C-first ⟺ premise uses `{C} is lower than {B}. {B} is lower than {A}.`
- Verified: template ⟺ phrasing holds for 60/60 train items and 60/60 test items.

**[OBSERVATION]** Entity-identity cannot explain the transfer: 5 train entities are phrasing-pure (Venus→A-first; Gold, Carbon→C-first; Silver, Iron→A-first), and on **31/60 test items the train entity-prior disagrees with the template** — the head followed the **template** on all 31 (total 60/60). The two benches share no tuples and no item IDs; the only perfectly label-correlated shared structure is the template.

**[INTERPRETATION]** The head is a **surface-template detector**, not a decision-capability readout. The "transfer" is fully explained by a shared bench-construction artifact. The hypothesis's intended reading — *"the output-side room has an autonomous (non-artifact) instantiation"* — is **not supported** by this result, even though the registered metric crossed the CONTINUE bar.

**[INTERPRETATION]** Consequence for the licensed GPU proposal: any GPU head-training proposal licensed by this CONTINUE inherits the confound. It is only meaningful against a **template-controlled bench** (premise templates decoupled from the label, e.g. both templates × both labels). Without that control, a GPU-scale repeat would re-measure the same artifact at higher cost. The independent Law #14 review (LOG-4530) did not flag this confound; the review stands on the bars as written, but the evidential reading above is now on the record.

## 12. Artifacts

- Executor: `experiments/runs/EXP106_lfh/run_exp106.py`
- Execution log: `experiments/runs/EXP106_lfh/out/exp106_execution_log.txt`
- Train embeddings: `experiments/runs/EXP106_lfh/out/exp106_train_embeddings.npz`
- Per-item predictions: `experiments/runs/EXP106_lfh/out/exp106_per_item.json`
- Result JSON: `experiments/runs/EXP106_lfh/out/exp106_result.json`
- This report: `research/experiments/EXP106_LFH_REPORT_2026-09-29.md`

**Boundary:** this lane executes only. No follow-up dispatched. No re-runs (none licensed under any branch). No signed artifact modified. No push.

**Next free: LOG-4535.**
