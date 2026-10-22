# Pre-registration: H3 — LFH (Label-Free Head)

**Candidate:** H3 — LFH: Label-Free Head (CPU-scoped honest shadow of the JEV-27B frozen-backbone + trained-head architecture)
**Date:** 2026-09-29
**Dossier:** `research/innovation/SPRINT_2026-09-29_SUMMIT.md` §H3 (worth-it gate passed; ranked #1)
**Lane:** LOG-4529 (drafting only)
**Status:** DRAFT — unsigned. Independent Law #14 review is a **separate lane** and is **not** this lane's work. **No experiment number minted.** No execution.

---

## 1. Hypothesis (one falsifiable sentence) [HYPOTHESIS]

An L2-regularized logistic head (~2k parameters) trained exclusively on frozen-embedding labels from the EXP092-B bench transfers above chance to the **disjoint** EXP091 60-item bench, scoring **≥ 40/60** with byte-identical block-off against the backbone pin — i.e., the output-side room has an autonomous (non-artifact) instantiation.

**Falsifier:** ≤ 35/60 (chance-level performance) on the disjoint bench.

---

## 2. Exact question [PROPOSITION]

Does a *trained* output-side head on the frozen backbone transfer above chance to a disjoint bench — i.e., does the output-side room have an autonomous (non-artifact) instantiation?

**Decision changed:** **CONTINUE** the output-side capability program (a CONTINUE licenses a separate, founder-gated GPU-scale head-training proposal) vs **KILL** it (even trained readouts do not transfer; the room is artifact-only — retire it, deepening LOG-204).

**Primary metric (registered before any run):** accuracy of the trained head on the 60-item EXP091 bench. One-sided binomial test vs chance (p=0.5).

---

## 3. Method

### 3.1 Frozen backbone [ASSUMPTION / Law #6]

- Backbone weights are **frozen**: Δθ = 0. Before and after the run, the backbone parameter hash is recorded and compared; any mismatch → RUN-INVALID, quarantine, no metric may be read (Law #6, Law #13).
- The head is an *external, detachable* readout: it never modifies, adapts, or conditions the backbone.

### 3.2 Disjoint-bench labels (Law #7)

- **Train labels:** EXP092-B bench items only. **Test items:** EXP091 60-item bench.
- **Overlap tripwire (Law #7):** before any training, compute the item-ID intersection between the EXP092-B training set and the EXP091 test bench. **Overlap > 0 → RUN-INVALID.** The run aborts; provenance is repaired and the pre-registration is re-run under a corrected record. No metric from an invalid run may be read, quoted, or plotted.
- No test labels, targets, or EXP091 embeddings beyond the frozen features may touch the training objective (Law #7 — zero data leakage).
- **Model-selection bar — FIX-3 (Law #7):** No EXP091 test label, target, or metric may inform any model-selection choice (regularization strength, embedding layer/source, decision threshold); all such choices are pinned above or derived from train data only.

### 3.3 Head training

- Model: L2-regularized logistic regression (~2k parameters) on **frozen backbone embeddings**.
- **Regularization pinned — FIX-1 (Law #4):** inverse-regularization strength **C = 1.0** (`sklearn.linear_model.LogisticRegression(penalty='l2', C=1.0)`), fixed before any run. No cross-validation, no grid search, no EXP091 test label, target, or metric may inform this choice.
- **Embedding source pinned — FIX-2 (Law #4):** frozen Pythia-410m, **layer 20** — the program-standard read site for EXP091-bench frozen embeddings (`experiments/protocols/EXP091_CLM8B_ADAPTATION_V3_PREREG_SIGNED.md`, signed protocol). Extraction spec: final-token hidden state, float32, CPU, `device_map="cpu"`, `requires_grad_(False)` on all parameters, `model.eval()` with `torch.no_grad()` around all extraction. Item encoding: premise-sentences substring (from `"Premise:"` up to, excluding `" Question:"`) per the bench-construction code path. The identical procedure applies to EXP092-B training items and EXP091 test items — one layer, one rule, no per-bench fishing. Archived embeddings may be used (zero new forwards) only if their archive manifest records this exact layer-20 provenance; otherwise the executor runs the single extraction pass under this spec.
- Inputs: archived embeddings if EXP091/EXP092-B embeddings are on disk (zero new forwards); otherwise a single 60-pass embedding extraction (no gradient ever flows into the backbone).
- Seed pinned; environment manifest logged; raw instance logs preserved (Law #13).

### 3.4 JEV-27B block-off byte-identical discipline [FACT — adopted from the 2026-09-29 frontier sweep]

- **Disable switch:** the trained head is detached, leaving the bare frozen backbone.
- **Byte-identical check:** outputs with head-attached inference path vs head-detached backbone are compared bit-for-bit on the full test bench. **Any mismatch → apparatus verdict INVALID**: the capability claim is inadmissible, because the head is then not a pure additive readout (Law #14-adjacent apparatus gate — recorded here as a stated check, reviewed by the separate review lane).
- The block-off check must **pass before any capability claim is admissible** (a CONTINUE verdict with a failed block-off is void).

### 3.5 What the positive cannot be (linear-probe theory) [THEOREM — stated, reviewed separately]

A linear head can only extract information already present in the embedding — a positive result is not manufacturable from noise. This is the mathematical license for reading a ≥ 40/60 outcome as genuine transfer rather than an artifact of the head itself.

---

## 4. Decision bars (registered)

- **≥ 40/60** → **CONTINUE.** One-sided binomial p ≈ **0.0067** vs chance (verified at drafting; the dossier's "≈0.003" annotation was loose and is corrected here — the bar itself is unchanged). With byte-identical block-off passed: first autonomous output-side result in-program; licenses a GPU-scale head-training *proposal* (separate lane, founder-gated).
- **≤ 35/60** → **KILL.** Under chance, P(X ≤ 35) = 0.92 — the bar deliberately fails to distinguish from chance. Verdict: "trained output-side readout transfers" is dead; the output-side room is artifact-only; retire it (deepens LOG-204). No rescue runs.
- **36–39/60 (in-between zone)** → **HELD / INCONCLUSIVE.** One-sided P(X ≥ 36 | chance) = 0.078 — not significant at α = 0.05, not a clean kill. Neither CONTINUE nor KILL is licensed. No decision is taken; no re-run, no larger-n rescue (an unlicensed larger-n re-test would be a gate tweak — barred). The observation is recorded as indeterminate only; it licenses nothing and retires nothing.

---

## 5. Falsification decision tree

| Outcome | Verdict | Meaning (no weasel words) |
|---|---|---|
| Item-ID overlap > 0 | **RUN-INVALID** | Law #7 violated. Abort before training. No metric exists. |
| Backbone hash mismatch (Δθ ≠ 0) | **RUN-INVALID** | Law #6 violated. Quarantine. No metric exists. |
| Block-off byte-identity fails | **INVALID** | Head is not a pure additive readout. Any accuracy number from the run is inadmissible. A CONTINUE is void. |
| ≥ 40/60, block-off passes | **CONTINUE** | First autonomous output-side result in-program. Licenses a GPU head-training proposal (separate lane). |
| ≤ 35/60 | **KILL** | Trained readouts do not transfer. The output-side room is artifact-only. Retire the room. |
| 36–39/60 | **HELD** | Indeterminate. Licenses nothing, retires nothing, no re-runs. |
| Any hypothesis rewording after seeing the metric | **BARRED** | Law #4: never silently shift hypotheses. A post-hoc rewrite is scientific misconduct, not a verdict. |

---

## 6. Cost / honesty statement [FACT]

- **$0 compute.** No GPU contact. No new training data. No model weights leave the frozen backbone.
- **~30 minutes CPU** (logistic fit on archived embeddings + disjointness check + block-off byte-identity check).
- This lane **drafts only**: no execution, no experiment number minted, no signed protocol (v82/v83/v84, GPU queue, weights) touched, no push, no PR.

---

## 7. What this does NOT claim

- A CONTINUE is a **first positive signal**, not superhuman cognition, not consciousness, not generality beyond the EXP091 bench, and not evidence about internal mechanisms of cognition (the head is a linear extractor — it reports what is present in the embedding, nothing more).
- A KILL retires the *output-side readout room*, not the summit program; it deepens the LOG-204 artifact interpretation.
- This pre-registration does **not** replicate JEV-27B (108M head, GPU-scale) — it is its honest CPU shadow.
- Novelty remains **N1 — Known Combination** (N2-adjacent only if a CONTINUE is independently verified).
- Unsigned and unreviewed until the independent Law #14 lane signs or rejects.

---

**Next steps (not this lane's):** independent Law #14 review of this exact file → CEO launch decision → execution under a minted experiment number (founder-authorized lanes only).
