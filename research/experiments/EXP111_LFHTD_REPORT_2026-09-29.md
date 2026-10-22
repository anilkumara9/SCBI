# EXP111 (H5/LFH-TD) Run Report — 2026-09-29

**Status:** EXP111 executed per signed pre-registration `EXP_PREREG_H5_LFHTD_2026-09-29.md` (LOG-4563 draft → LOG-4564 SIGN-WITH-FIXES → LOG-4565 repairs → LOG-4566 ALL-FIXES-VERIFIED/SIGN → LOG-4567 CEO launch as EXP111).

## Verdict

**CONTINUE** — overall test accuracy 24/30 = 0.8000 with G = 0.0000 (< 0.30). This is the day's first autonomous output-side result: the trained linear head extracts the position feature from the frozen backbone on a template-decorrelated bench with zero template-detector signature.

## 1. Artifact verification (pre-reg §3.2 — all three hashes recomputed before training)

[OBSERVATION] All three pinned hashes match:
- npz file: `6cf4a8a7…af6a76` — match
- embeddings-array bytes: `9b6e8afb…99123` — match
- ids-array bytes: `3669e102…5075cb9` — match

Embeddings shape (60, 1024) float32; ids (60,) str. Primary analysis used archived embeddings only — **zero backbone contact, Δθ=0 structural** (no model loaded, no weights touched).

## 2. Split (pre-reg §3.3 — pinned)

- sklearn==1.9.1, numpy==2.5.3, seed **20260929**, `train_test_split(test_size=0.5, random_state=20260929, stratify=f"{phrasing}_{flipped}")`
- Train n=30, test n=30, **ID overlap = 0** (disjointness asserted)
- Per-cell test counts: A-first_False 8, A-first_True 7, C-first_False 7, C-first_True 8 — matching the pinned 8/8/7/7 encoding
- N_F=15 (flipped=False test), N_T=15 (flipped=True test) — both denominators as pinned

## 3. Head training (pinned spec, Law #7 — no tuning)

`LogisticRegression(penalty='l2', C=1.0, solver='lbfgs', max_iter=1000, random_state=20260929)` on the 30-item train split. No L2-C sweep, no layer choice, no solver choice, no seed re-rolls.

- Determinism pass: re-fit from the same artifact → **byte-identical test predictions** (pass)
- Head weight hash: `483a91a8…afdf9f28`
- Head weight L2 norm: 1.880708
- Train accuracy (sanity): 1.0000

## 4. Test evaluation (n=30)

| Metric | Value |
|---|---|
| Overall accuracy | 24/30 = 0.8000 |
| acc(flipped=False, N_F=15) | 0.8000 (12/15) |
| acc(flipped=True, N_T=15) | 0.8000 (12/15) |
| **G** = acc(F) − acc(T) | **0.0000** |

Per-cell descriptives: A-first/original 0.8750 (7/8); A-first/flipped 0.8571 (6/7); C-first/original 0.7143 (5/7); C-first/flipped 0.7500 (6/8).

## 5. Decision bars applied (pre-reg §4 verbatim)

- G ≥ 0.30? **No** (G=0.0000). Template-detector signature absent.
- Overall ≥ 20/30 with G < 0.30? **Yes** (24/30; one-sided binomial p ≈ 0.0014 vs chance).
- **→ CONTINUE.** Falsification-tree branch: determinism OK → evaluate → G<0.30 and overall ≥20/30 → CONTINUE.

## 6. What this verdict licenses and does not claim

**Licenses:** the GPU head-training proposal voided by EXP107 is **re-licensed** under the decorrelated-bench discipline; the §6 secondary per-layer analysis is licensed (same run, descriptive-only).

**Does NOT claim** (§8 fences): this is a correlation at one layer (20) on one bench (n=30 test, Pythia-410m) — not consciousness, not generality, not superhuman cognition. Capability claims require downstream causal tests (steering, decision-flip). Does not re-license H1/H4, static-injection lines, or any closed family. Novelty N1 — Known Combination.

## 7. Secondary per-layer analysis (§6 — descriptive-only, licenses no verdict)

[OBSERVATION] Executed in the same run per the CONTINUE license. Environment: torch=2.14.0+cpu, transformers=5.17.0, sklearn=1.9.1, numpy=2.5.3, threads set=2 read-back=2, seed 20260929. Backbone LOG-331 pin `ec276abe…38e0ed` verified **before and after** extraction (Δθ=0). Bench rebuilt deterministically, pin `e91b302f…df49e4f` matching EXP107. Same 60 items by ID; same stratified 30/30 split; same pinned head spec; zero generation (forward passes only). One deviation recorded honestly: `device_map='cpu'` was dropped from the load call because transformers 5.17.0 requires `accelerate` for device maps — CPU-only execution makes this a no-op (no behavioral change; the pinned library versions are untouched).

| Layer | Accuracy | G | Note |
|---|---|---|---|
| 4 | 24/30 = 0.8000 | −0.1333 | descriptive-only |
| 8 | 30/30 = 1.0000 | 0.0000 | descriptive-only |
| 12 | 29/30 = 0.9667 | 0.0667 | descriptive-only |
| 16 | 30/30 = 1.0000 | 0.0000 | descriptive-only |
| 20 (primary) | 24/30 = 0.8000 | 0.0000 | binding (above) |

[INTERPRETATION] The position signal is decodable across layers with no template-detector signature at any layer (all |G| ≤ 0.1333 << 0.30). The per-layer bars are descriptive-only per §6 and license no verdict; four layers at α=0.05 carry ~18.5% family-wise false-positive rate. No layer licenses a new verdict or re-opens any closed family.

## 8. Files

- Report: this file (`EXP111_LFHTD_REPORT_2026-09-29.md`)
- Raw logs: `~/workspace/SCBI/experiments/runs/EXP111_lfhtd/out/` — `exp111_result.json`, `exp111_execution_log.txt`, `exp111_test_predictions.npy`, `exp111_secondary_result.json`, `exp111_secondary_log.txt`
- Scripts: `exp111_run.py` (primary), `exp111_secondary.py` (secondary)

No data invented. Falsification-tree branch: CONTINUE. Lane stops here.
