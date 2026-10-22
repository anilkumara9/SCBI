# Law #14 Fix-Verification — EXP_PREREG_H3_LFH_2026-09-29.md

**Verification lane:** LOG-4532 (pre-assigned). **Independent** of both the LOG-4529 drafting lane and the LOG-4531 repair lane.
**Date:** 2026-09-29
**Artifact verified:** `research/prereg/EXP_PREREG_H3_LFH_2026-09-29.md` (H3 — LFH pre-registration, as revised by the LOG-4531 repair lane)
**Review under verification:** `research/reviews/LAW14_REVIEW_H3_LFH_2026-09-29.md` (LOG-4530, verdict SIGN-WITH-FIXES, three required fixes)
**Scope:** $0 CPU. Read-only everywhere except this file and the LOG-4532 log append. No execution approved, no experiment number minted. This lane does not re-review the document's science — it checks only that the three required fixes are present as specified, and that nothing else moved the bars, hypothesis, verdict logic, or numbers.

## Verdict: ALL-FIXES-VERIFIED

All three required fixes are present in the draft, quoted verbatim below. The hypothesis, decision bars, verdict logic, and registered numbers are unchanged. **Per the LOG-4530 review, its verdict upgrades to SIGN.** The artifact is cleared for the CEO launch-decision lane. This lane approves no execution and mints no experiment number.

---

## FIX-1 — Pin the L2 regularization strength (Law #4 / Law #9): **PASS**

Found in §3.3, quoted exactly:

> "**Regularization pinned — FIX-1 (Law #4):** inverse-regularization strength **C = 1.0** (`sklearn.linear_model.LogisticRegression(penalty='l2', C=1.0)`), fixed before any run. No cross-validation, no grid search, no EXP091 test label, target, or metric may inform this choice."

- The pinned value (C = 1.0, the review's own fixed-constant example) is stated. No CV/grid-search escape hatch remains; the train-data-only clause ("fixed before any run") and the explicit bar on EXP091 test information close the post-hoc tuning vector.

## FIX-2 — Pin the embedding source (Law #4 / Law #9): **PASS**

Found in §3.3, quoted exactly:

> "**Embedding source pinned — FIX-2 (Law #4):** frozen Pythia-410m, **layer 20** — the program-standard read site for EXP091-bench frozen embeddings (`experiments/protocols/EXP091_CLM8B_ADAPTATION_V3_PREREG_SIGNED.md`, signed protocol). Extraction spec: final-token hidden state, float32, CPU, `device_map="cpu"`, `requires_grad_(False)` on all parameters, `model.eval()` with `torch.no_grad()` around all extraction. Item encoding: premise-sentences substring (from `"Premise:"` up to, excluding `" Question:"`) per the bench-construction code path. The identical procedure applies to EXP092-B training items and EXP091 test items — one layer, one rule, no per-bench fishing. Archived embeddings may be used (zero new forwards) only if their archive manifest records this exact layer-20 provenance; otherwise the executor runs the single extraction pass under this spec."

- Single layer named (layer 20), cited via the signed protocol rather than invented. Full extraction spec present (token pooling, dtype, device, grad flags, eval mode, item encoding). Identical procedure train/test. Archive provenance requirement explicit — no layer-fishing vector remains.

## FIX-3 — Extend the Law #7 bar to model selection (Law #7): **PASS**

Found in §3.2, quoted exactly:

> "**Model-selection bar — FIX-3 (Law #7):** No EXP091 test label, target, or metric may inform any model-selection choice (regularization strength, embedding layer/source, decision threshold); all such choices are pinned above or derived from train data only."

- The required sentence appears **verbatim** in §3.2, matching the review's required text character for character (checked against `LAW14_REVIEW_H3_LFH_2026-09-29.md` "Required fixes", FIX-3).

---

## No-change spot-check: bars, verdict logic, hypothesis, numbers — **PASS**

- **Decision bars (§4):** unchanged — ≥ 40/60 → CONTINUE (one-sided p ≈ 0.0067), ≤ 35/60 → KILL, 36–39/60 → HELD with "no re-runs, no larger-n rescue" barred. The p ≈ 0.0067 value is present and identical to the reviewed version.
- **Verdict logic (§5):** unchanged — decision tree rows, RUN-INVALID/INVALID conditions, and the "hypothesis rewording = BARRED" row all intact.
- **Hypothesis (§1):** unchanged — "An L2-regularized logistic head (~2k parameters) … scoring **≥ 40/60** …"; falsifier ≤ 35/60 intact.
- The only textual deltas versus the reviewed version are the three added fix blocks above (each labeled FIX-1/2/3); no reformatting, rewording, or improvement of unrelated sections was observed.

**Observation (non-defect):** §7 still reads "Unsigned and unreviewed until the independent Law #14 lane signs or rejects." A review (LOG-4530) now exists and this verification upgrades it to SIGN — the sentence is mildly stale but it asserts nothing false about the draft's state (unsigned still true; the signature event is external). Left for the signing lane to tidy; not a fix-verification failure.

---

## Boundary

This lane upgrades the LOG-4530 review verdict to SIGN and clears the artifact to the CEO launch-decision lane. It approves **no execution**, mints **no experiment number**, and dispatches **no follow-up work**. Founder-authorized lanes only from here. This lane stops here.
