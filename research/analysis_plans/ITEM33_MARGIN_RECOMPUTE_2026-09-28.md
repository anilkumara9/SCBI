# ITEM-33 margin recomputation — 2026-09-28 (LOG-4472)

Analysis lane only. Precondition flagged by the V83 change plan (LOG-4471, overstatement O1).
Committed-artifact analysis; $0 CPU; no GPU; no new experiment; no experiment number minted.
v82, the V83 plan, and all signed protocols untouched.

## Question

The gap analysis's Fix 4 proposed an Item-33 hero vignette citing **item-level** injection
margin shifts (+0.010/−0.004). v82 L391 prints only the **mean across items** (+0.0059/−0.0076).
Can Item 33's item-level injection margin shift be recovered from the EXP093 primaries?

## [FACT] Decode margin — VERIFIED from EXP092 primaries

Method: `research/analysis_plans/item33_margin_recompute_2026-09-28.py`
(sha256 `de8835810c52e729bb084b885c2bd8a74ba8820371cf3840ac38d3ee1f3f1ed`),
deterministic numpy-only, layer L_STAR=11 (EXP092 `verdict_detail.l_star`),
per-item 1-NN margin = nearest-different-class distance − nearest-same-class distance.

Results (`item33_margin_recompute_results_2026-09-28.json`,
sha256 `a0cb9c8356e847d341dc590f115e2dd6c1310b69847a1733b898917fa5cb6498`):

- Item 33 (`exp092_elemental_2hop_3`): margin **1.0133**, same-class min 2.1059,
  different-class min 3.1192, **rank 2 of 60**. Top-5: 31 (1.1549), 33 (1.0133),
  56 (0.9871), 48 (0.8932), 41 (0.8405).
- Matches v82 L391's "1.013; same-class 2.106 vs. different-class 3.119; second-largest"
  to 5e-4. [OBSERVATION]

## [FACT] Injection margin shifts — UNRECOVERABLE from EXP093 primaries

`run_exp093.py` computed the per-item margin arrays (mB, mP, mN — 60 items × 3 conditions)
in memory and persisted **only the aggregates** in `out/exp093_report.json` secondaries:

- `mean_margin_shift_P = 0.005951849619547526` → v82's +0.0059
- `mean_margin_shift_N = -0.007636133829752604` → v82's −0.0076

A repo-wide sweep (`grep -rln margin_shift`, all `*.csv/*.npz/*.npy/*per_item*`) found
**no per-item margin file anywhere** in the EXP093 bundle or the repo
(EXP094's `per_item_records.csv` belongs to a different experiment and a different
direction family — not usable here).

[OBSERVATION] Recovery would require a 180-pass model re-run to regenerate the
logits — a new experiment on the user's GPU, outside this lane's $0-CPU
committed-artifact authorization.

## [FACT] The gap analysis's +0.010/−0.004 appears in NO artifact

String search across v82 source, all EXP093 primaries, the EXP093 run report,
and all verdict reviews: zero hits. The numbers are unverified and must not be printed.

## Vignette verdict: REWRITE (not drop)

The vignette as proposed (per-item arrow +0.010/−0.004) **must not be used**.
The usable form, fully artifact-grounded:

> "Item 33: decodes correctly with the 2nd-largest 1-NN margin (1.013; same-class
> 2.106 vs. different-class 3.119) → the mean injection margin shift is only
> +0.0059/−0.0076 **across items** → decision unchanged."

The margin-shift figure must be labeled mean-across-items, or the arrow ships without
a number. This keeps the CoT-Figure-1 social-media strip honest and closes
overstatement O1 permanently.

## Lineage

- Script: `research/analysis_plans/item33_margin_recompute_2026-09-28.py`
- Results: `research/analysis_plans/item33_margin_recompute_results_2026-09-28.json`
- EXP092 primaries: `experiments/runs/EXP092_ibl/out/exp092_embeddings.npz`
- EXP093 aggregates: `experiments/runs/EXP093_l11_causal/out/exp093_report.json`
