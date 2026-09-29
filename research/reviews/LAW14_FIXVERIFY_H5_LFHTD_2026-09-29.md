# Law #14 fix-verification — H5/LFH-TD pre-registration repairs (LOG-4565)

**Document under exact-version verification:** `research/prereg/EXP_PREREG_H5_LFHTD_2026-09-29.md`
**Review being verified against:** `research/reviews/LAW14_REVIEW_H5_LFHTD_2026-09-29.md`
**Verification lane:** LOG-4566 (pre-assigned). Independent of the LOG-4563 drafting lane and the LOG-4565 repair lane.
**Date:** 2026-09-29. **$0 CPU.** Read-only except this file and the log append.
**Scope:** fix-verification only — verify the five required fixes are present, quote exact text, PASS/FAIL each. Not a re-review of the whole document. No execution approved, no experiment number minted.

---

## F1 — Environment versions pinned: **PASS**

Found, §3.3 (split and training):

> *"Disjoint stratified split: `train_test_split` (**sklearn==1.9.1**, **numpy==2.5.3** — the EXP107 report's environment; both recorded in the execution worksheet)"*

Found, §6 (secondary analysis):

> *"The secondary's environment is pinned: **torch==2.14.0+cpu**, **transformers==5.17.0**, CPU thread count set and read back via `torch.get_num_threads()` — all recorded in the execution worksheet."*

All five pins present (sklearn 1.9.1, numpy 2.5.3 primary; torch 2.14.0+cpu, transformers 5.17.0, thread count set-and-read-back secondary) plus the worksheet-recording requirement for both. Matches the repair-lane claim (LOG-4565).

## F2 — Split denominators pinned: **PASS**

Key encoding pinned, §3.3:

> *"stratified by the pinned 4-cell key `f"{phrasing}_{flipped}"` with phrasing ∈ {"A-first", "C-first"} and flipped ∈ {False, True}. Under sklearn 1.9.1 + seed 20260929 the test counts per cell in sorted key order are deterministically **8/8/7/7** — ("A-first", original-word): 8, ("A-first", flipped-word): 7, ("C-first", original-word): 7, ("C-first", flipped-word): 8 — → **train n=30, test n=30** with **N_F=15 flipped=False** and **N_T=15 flipped=True** test items (8+7 and 7+8). The exact train/test item-id lists and the observed N_F, N_T are written to the run log"*

G defined with actual observed denominators, §3.6:

> *"G = acc(N_F flipped=False test items) − acc(N_T flipped=True test items) (N_F=15, N_T=15 under the pinned split encoding; both logged in the worksheet)"*

Threshold restated against the actual denominators, §4 (threshold itself unchanged at 0.30):

> *"G ≥ 0.30 — a ≥5-item gap at the pinned N_F=N_T=15 denominators; the registered EXP107 signature produced G = 30/30 − 4/30 = 0.867"*

The old "≥5 of the 15 item-margin" / unlicensed "(15 vs 15)" glosses are gone from operative sections; the one "(15-vs-15 test items)" occurrence in §9 item 3 is inside the deviation record and now describes the pinned state, not an assumption. Key form, per-cell counts, N_F/N_T, worksheet logging, and the unchanged 0.30 threshold all present.

## F3 — Artifact reference hashes pinned: **PASS**

Found, §3.2 (provenance pin):

> *"Reference hashes (independently recomputed from `experiments/runs/EXP107_templatectrl/out/exp107_test_embeddings.npz` by the LOG-4565 repair lane and matching the independent review): npz file `6cf4a8a726a2b6e4623f57d0287d95879866f77e789bcc3789fb693cf2af6a76`; embeddings-array bytes (60×1024 float32) `9b6e8afb091ba1edbb0311ba1d3414d34a65942c3fdecb4533b69720f2a99123`; ids-array bytes `3669e102222719d66f61daca46ae1ac34e844e398ae433743a5b37bfc5075cb9`."*

This verification lane independently re-computed all three hashes from `experiments/runs/EXP107_templatectrl/out/exp107_test_embeddings.npz` (file bytes via sha256, `embeddings.tobytes()` = (60,1024) float32, `ids.tobytes()`):

- npz file: `6cf4a8a726a2b6e4623f57d0287d95879866f77e789bcc3789fb693cf2af6a76` ✓
- embeddings array: `9b6e8afb091ba1edbb0311ba1d3414d34a65942c3fdecb4533b69720f2a99123` ✓
- ids array: `3669e102222719d66f61daca46ae1ac34e844e398ae433743a5b37bfc5075cb9` ✓

Three-for-three exact match. The repair-lane "confirm before pin" instruction was honored — the values were not transcribed blindly.

## F4 — Secondary backbone-contact discipline + descriptive-only status: **PASS**

Found, §6:

> *"Backbone-contact discipline (the primary never loads the backbone; the secondary does): the backbone hash is verified against the LOG-331 pin **before and after** the fresh layer 4/8/12/16 extraction (Δθ=0); the secondary extracts the **same 60 bench items by ID**."*

Found, same paragraph, the required explicit sentence:

> *"Reported descriptively with the same decision bars per layer — **per-layer bars are descriptive-only and license no verdict** (four layers at α=0.05 carry ~18.5% family-wise false-positive rate; hence no multiplicity correction beyond the SECONDARY label)."*

Both elements present: the before/after LOG-331 pin check with Δθ=0 and the same-60-items-by-ID requirement, plus the descriptive-only sentence verbatim.

## F5 — Decision-tree completeness: **PASS**

The tree now shows both precondition-failure branches explicitly:

```
├─ train/test ID overlap → RUN-INVALID (Law #7, §3.3)
└─ disjoint
    └─ train L2-logreg → determinism re-fit pass (§3.4(c))
        ├─ predictions ≠ byte-identical → RUN-INVALID (block-off discipline)
```

Both the §3.3 ID-overlap → RUN-INVALID branch and the §3.4(c) determinism-pass mismatch → RUN-INVALID branch are present. The "No other branches exist" claim follows them, properly scoped to post-precondition branches. The input-hash HALT was already present.

## Spot-check (unchanged items): **PASS**

- Hypothesis (one falsifiable sentence, §1): present, unchanged — trained L2 head on frozen layer-20 embeddings, above chance on held-out decorrelated bench.
- n=30 bars (§4): CONTINUE ≥ 20/30 (p=0.0494); KILL ≤ 18/30 (p≥0.1808) or G ≥ 0.30; HELD = 19/30 with G < 0.30 — all unchanged.
- G threshold: 0.30, unchanged.
- Deviations section (§9): complete list of 5, unchanged.
- No-generation constraint (§3.1): present, unchanged — "zero generation... hard constraint from the EXP108/EXP109 RUN-INVALID lesson."
- Only the five fix sentences and their surrounding anchors were added; decision bars, hypothesis, numbers, fences untouched.

---

## Verdict: **ALL-FIXES-VERIFIED** — the LOG-4564 independent Law #14 review on `EXP_PREREG_H5_LFHTD_2026-09-29.md` is explicitly **upgraded to SIGN**.

All five required fixes verified present and correct; F3 independently re-verified by hash recomputation. This lane approved no execution and minted no experiment number — the CEO launch decision remains a separate lane.
