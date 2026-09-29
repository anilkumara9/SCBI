# Independent Exact-Artifact Verdict Review — EXP111 (H5/LFH-TD)

**Lane:** independent verdict-review (LOG-4569 pre-assigned). Independent of the drafting (LOG-4563), review (LOG-4564), repair (LOG-4565), fix-verification (LOG-4566), launch (LOG-4567), and execution (LOG-4568) lanes. Read-only verification; nothing modified.

**Documents reviewed:** `EXP111_LFHTD_REPORT_2026-09-29.md` (exact filename) vs `EXP_PREREG_H5_LFHTD_2026-09-29.md` (exact filename) vs raw artifacts in `experiments/runs/EXP111_lfhtd/out/`.

**Verdict: QUALIFY** — the registered **CONTINUE** stands on the artifacts, with one required footnote caveat (§7 below).

## 1. Decision-bar application (pre-reg §4, verbatim)

Registered: CONTINUE ⇔ overall ≥ 20/30 AND G < 0.30; KILL ⇔ G ≥ 0.30 regardless of overall, OR overall ≤ 18/30; HELD ⇔ 19/30 with G < 0.30. Observed from the raw artifacts (independently recomputed, §2): **24/30**, **G = 0.0000**. The CONTINUE branch is the only one that fires. The G ≥ 0.30 kill branch (pre-installed kill-test, one sentence) is correctly not triggered. The 0.30 threshold is used as pinned — no post-hoc reinterpretation of the signature threshold anywhere in the report.

## 2. Independent recomputation from raw artifacts (not summaries)

Recomputed by this lane from `exp111_test_predictions.npy` (30 int64 predictions), the test-ID list in `exp111_result.json`, and per-item labels in the EXP107 artifact (`exp107_per_item.json`):

- Overall accuracy: **24/30 = 0.8000** — matches report exactly.
- acc(flipped=False, N_F=15): 0.8000 (12/15); acc(flipped=True, N_T=15): 0.8000 (12/15) — matches report exactly.
- **G = acc(F) − acc(T) = 0.8000 − 0.8000 = 0.0000** — matches report exactly; denominator-explicit as pinned (N_F=N_T=15).
- Per-cell: A-first_False 7/8 = 0.8750; A-first_True 6/7 = 0.8571; C-first_False 5/7 = 0.7143; C-first_True 6/8 = 0.7500 — all match the report to 4dp.
- Per-cell test counts: 8/8/7/7 as pinned — matches.
- Train/test ID overlap: **0** (verified from the raw ID lists, not from the `disjoint: true` field) — matches.

## 3. Determinism re-fit (block-off discipline §3.4(c))

Independently re-fit `LogisticRegression(penalty='l2', C=1.0, solver='lbfgs', max_iter=1000, random_state=20260929)` on the pinned train split (sklearn==1.9.1, numpy==2.5.3 — pinned environment reproduced) using the archived EXP107 embeddings:

- Re-fit predictions **byte-identical** to archived `exp111_test_predictions.npy` — matches the report's determinism claim.
- Second independent refit byte-identical to the first — determinism holds.
- Head weight hash matches `483a91a8…afdf9f28` — matches.
- Head L2 norm 1.8807075023651123 — matches the report's 1.880708.

## 4. Provenance pins (pre-reg §3.2)

Independently re-hashed from `experiments/runs/EXP107_templatectrl/out/exp107_test_embeddings.npz`: npz file hash, embeddings-array bytes hash, and ids-array bytes hash **all match** the pinned reference values. Embeddings shape (60, 1024) float32; ids (60,) str — as reported. No backbone was loaded for the primary analysis (embeddings-only, sklearn fit).

## 5. Secondary per-layer analysis (pre-reg §6 — descriptive-only)

- Values in `exp111_secondary_result.json` / `exp111_secondary_log.txt` match the report exactly: L4 24/30 G=−0.1333; L8 30/30 G=0.0000; L12 29/30 G=0.0667; L16 30/30 G=0.0000.
- The JSON carries `"note": "DESCRIPTIVE-ONLY — licenses no verdict (pre-reg §6)."`; the log tags every per-layer line `(DESCRIPTIVE-ONLY)`. **No verdict language appears anywhere** in the secondary artifacts or the report's §7.
- Backbone LOG-331 pin `ec276abe…38e0ed` verified **before and after** extraction, Δθ=0 — recorded in the secondary JSON and log. Bench pin matched the EXP107 pin. Environment pinned (torch=2.14.0+cpu, transformers=5.17.0, threads 2 set / 2 read back, seed 20260929). The `device_map='cpu'` deviation is documented as a CPU-only no-op — accepted as honest disclosure; the pinned library versions are untouched.

## 6. Overclaim fences

The report's §6 fences are present and verbatim-spirited: one layer-20 correlation on one n=30 bench; not consciousness, not generality, not superhuman cognition; capability claims require downstream causal tests; no re-licensing of H1/H4, static-injection lines, or any closed family; novelty N1 — Known Combination. No fence is violated by the verdict wording.

## 7. Required footnote caveat (the QUALIFY)

The report's §5 states "one-sided binomial p ≈ 0.0014 vs chance" for 24/30. The pre-reg registered a **one-sided** binomial vs chance. The exact one-sided p for 24/30 at n=30 is **0.00072**; 0.0014 is the **two-sided** value (verified: Σ_{k=24..30} C(30,k)/2^30 = 0.0007155). The critical-value registration (20/30 → one-sided p=0.0494) was correctly stated in the pre-reg and independently confirmed. **Required caveat:** the report's p-value descriptor should read "one-sided p ≈ 0.00072 (two-sided ≈ 0.0014)". This is descriptive-only — the registered bar is the **count criterion** (≥20/30), not the p-value, and both values are far below α=0.05, so no decision branch changes. No post-hoc bar is involved.

## 8. Minor observations (no caveat required)

- sklearn 1.9.1 emits a `FutureWarning` that `penalty` is deprecated (removal in 1.10). The pinned spec `penalty='l2'` is executed behaviorally as-registered; determinism is unaffected. Cosmetic only.
- The pre-reg's Law #7 posture (stratification key includes phrasing, which is perfectly label-correlated) is exactly as pinned in §3.3 — no post-hoc selection, no violation introduced by the execution.

## Conclusion

Every binding number in the CONTINUE verdict was independently recomputed from the raw artifacts and matches the report exactly: 24/30, G=0.0000 (denominator-explicit, N_F=N_T=15), zero train/test overlap, pinned hashes, byte-identical determinism re-fit, per-cell 8/8/7/7. The kill-test logic was applied as registered — the G ≥ 0.30 template-detector signature is absent, so the kill branch correctly does not fire. The secondary analysis licenses no verdict and claims none; Δθ=0 is verified for the backbone-contacting secondary. The overclaim fences stand.

**The CONTINUE verdict BINDS on the artifacts, qualified only by the required footnote caveat in §7** (one-sided p ≈ 0.00072, not ≈ 0.0014 — descriptive only, no branch affected).

Lane stops here. No execution authorized, no follow-ups dispatched, no artifact modified.
