# EXP092 (IBL) — Real Execution Run Report

**Date:** 2026-09-25
**Mode:** real (CPU, frozen Pythia-410m, read-only)
**CEO clearance:** LOG-4332 (Nova)
**Signed protocol:** `experiments/protocols/EXP092_IBL_PREREG_SIGNED.md` (SHA-256 `75e744ad9bae98cc86c0443823bd27b197a9c17fc106ba984e5870cf1bdb347c`)
**Launch chain:** signed (LOG-4325) → bundle build (LOG-4328) → bundle review SIGN (LOG-4331) → CEO clearance (LOG-4332) → this execution.

## Execution summary

**Command (from ~/workspace/SCBI):**
`~/workspace/.venv-exp077/bin/python experiments/runs/EXP092_ibl/run_exp092.py --out-dir experiments/runs/EXP092_ibl/out --ceo-clearance`

**Wall time:** ~4 minutes total (model load ~30s incl. G1 hash; 60 forward passes ~100s; scoring ~5s). The ~1.5 CPU-h estimate in the protocol was conservative; the actual run was far cheaper.

**Environment:** torch 2.14.0+cpu, transformers 5.17.0, numpy 2.5.3 (venv `~/.venv-exp077`).

## Guard outcomes (all PASS, in execution order)

| Guard | Outcome |
|---|---|
| G0 bench provenance | PASS — pin `9be8162633fe19aa…` recomputed; 60/60 unique (domain,tuple); strata match §4 |
| G2 oracle diagnostic | PASS — build-time artifact re-verified: oracle=0.0607, p=0.5312, gate PASS, bench-pin-bound |
| G3 phrasing balance | PASS — 30/30 A-first/C-first on the real bench builder |
| G1′ tokenizer cover | PASS — 240/240 in-prompt A/C occurrences single-token, real tokenizer, offset-mapping check, BEFORE any weight access |
| Signed-protocol digest | PASS — runner asserted the SIGNED file digest before executing |
| G1 Δθ=0 (pre) | PASS — `ec276abe3902fab0…` matches LOG-331 pin |
| G1 Δθ=0 (post) | PASS — `ec276abe3902fab0…` identical; **Δθ=0 verified** |
| G4 null-spread | PASS — every layer's permutation null has non-zero spread (0.20–0.25); instrument responsive |
| Tie rule | No exact ties encountered; rule armed, not triggered |
| Layer-20 routing | Layer 20 excluded from CONTINUE by construction |

**Embeddings sanity:** shape (24, 60, 1024), float32, no NaN, no Inf; per-layer std 0.37–3.20 (healthy, non-degenerate); 20 unique labels; option logits (60, 2) captured.

## Primary results — per-layer LOO 1-NN (K=20, chance=0.05)

Bonferroni α = 0.05/24 = 0.0020833. Effect bar = 0.10. B = 1,000 stratified permutations.

| Layer | Accuracy | p (raw) | q95 (null) | Effect (acc−q95) | Bonferroni-sig | ≥10pp |
|---|---|---|---|---|---|---|
| 0 | 0.2333 | 0.000999 | 0.1500 | +0.0833 | yes | no |
| 1 | 0.2667 | 0.000999 | 0.1500 | +0.1167 | yes | **yes** |
| 2 | 0.2333 | 0.000999 | 0.1342 | +0.0992 | yes | no |
| 3 | 0.2000 | 0.002997 | 0.1500 | +0.0500 | no | no |
| 4 | 0.2000 | 0.002997 | 0.1500 | +0.0500 | no | no |
| 5 | 0.1333 | 0.0949 | 0.1500 | −0.0167 | no | no |
| 6 | 0.1333 | 0.1069 | 0.1500 | −0.0167 | no | no |
| 7 | 0.1167 | 0.1538 | 0.1333 | −0.0167 | no | no |
| 8 | 0.1333 | 0.0909 | 0.1333 | +0.0000 | no | no |
| 9 | 0.1167 | 0.1558 | 0.1500 | −0.0333 | no | no |
| 10 | 0.1333 | 0.0939 | 0.1342 | −0.0008 | no | no |
| **11** | **0.3333** | **0.000999** | **0.1333** | **+0.2000** | **yes** | **yes** |
| 12 | 0.3167 | 0.000999 | 0.1333 | +0.1833 | yes | **yes** |
| 13 | 0.3000 | 0.000999 | 0.1333 | +0.1667 | yes | **yes** |
| 14 | 0.2667 | 0.000999 | 0.1333 | +0.1333 | yes | **yes** |
| 15 | 0.2333 | 0.000999 | 0.1333 | +0.1000 | yes | **yes** |
| 16 | 0.1333 | 0.0799 | 0.1333 | +0.0000 | no | no |
| 17 | 0.2833 | 0.000999 | 0.1333 | +0.1500 | yes | **yes** |
| 18 | 0.2667 | 0.000999 | 0.1500 | +0.1167 | yes | **yes** |
| 19 | 0.1667 | 0.0250 | 0.1500 | +0.0167 | no | no |
| 20 | 0.1500 | 0.0659 | 0.1500 | +0.0000 | no | (excluded) |
| 21 | 0.1667 | 0.0300 | 0.1500 | +0.0167 | no | no |
| 22 | 0.1667 | 0.0310 | 0.1500 | +0.0167 | no | no |
| 23 | 0.1500 | 0.0619 | 0.1500 | +0.0000 | no | no |

**S (both bars, layer≠20):** {1, 11, 12, 13, 14, 15, 17, 18} — 8 layers.
**l* = argmax effect:** layer 11 (effect +0.2000).

## Registered verdict

**AUTHORITATIVE VERDICT: CONTINUE**

Per the signed §5 TOTAL decision tree: ∃ layer l≠20 with Bonferroni-significant p_l < 0.05/24 AND (a_l − q95_l) ≥ 10pp. Eight layers satisfy both bars; l* = 11. The "misplaced information" hypothesis survives: task-relevant information (target-entity identifiability from final-token embeddings) is present at layers other than 20, peaking at layer 11 (33.3% vs 5% chance, +20pp above the null q95).

**Licensed consequence (per §5):** redirect the readout program to l* = 11. This is a *licensed CONTINUE of the IBL hypothesis*, not a capability claim. Novelty remains N1. No superhuman/conscious/autonomous claim is licensed by this result.

## Secondary statistics (registered, non-binding)

**S1 (Ross kNN-MI after PCA≤20):** 4.082639989633465 bits at ALL 24 layers — bit-identical to 13 decimals despite differing embeddings (verified by direct recomputation on layers 0, 11, 23).
[OBSERVATION] The S1 estimator is degenerate in this data regime: with k=3 and no exact distance ties (continuous embeddings), every point's neighbor count m_i = k+1 = 4, so MI = ψ(60) − ψ(4) = constant. S1 carries zero layer-discriminating information here. This does not affect the verdict (S1 is registered non-binding), but the estimator as implemented cannot serve its intended diagnostic role without ties or a larger k. Flagged for the program record.

**S2 (LM log-prob baseline):** accuracy 0.60 (36/60); mean logprob margin (target−foil) = −0.0018.
[OBSERVATION] The frozen model's own output logits favor the correct option 60% of the time on the binary A/C choice — above chance (50%), with near-zero mean margin. The S2 baseline is summit-mandated context, non-binding on the verdict.

## [INTERPRETATION] (execution agent — for the independent review to judge)

The signal pattern is striking: a broad mid-network elevation (layers 11–18, accuracy 0.23–0.33) against a near-chance background elsewhere (0.12–0.17), with layer 20 itself at 0.15. The v2 bench's entity-set oracle is at chance (0.0607), so this is not the v1 duplicate-triple confound. What the 1-NN measures is target-entity identifiability from the final-token state — the information "which entity is being asked about" is decodable at layer 11 far above chance. Whether this constitutes *relational* task information vs. entity-mention encoding is an interpretive question for the program (and the independent verdict review), not settled by this experiment. The registered decision tree's CONTINUE fires on the statistical bars, which are met.

## Raw-data paths (primary artifacts — preserved, not summarized)

- Embeddings: `experiments/runs/EXP092_ibl/out/exp092_embeddings.npz` (24×60×1024 float32 + option logits + labels/phrasing/domain)
- Extraction log: `experiments/runs/EXP092_ibl/out/exp092_extraction_log.txt`
- Extraction meta: `experiments/runs/EXP092_ibl/out/exp092_extraction_meta.json`
- Scorer report: `experiments/runs/EXP092_ibl/out/exp092_report.json` (this report's source of numbers)
- Run report: `experiments/runs/EXP092_ibl/EXP092_RUN_REPORT_2026-09-25.md` (this file)

## Cost

$0. ~4 minutes wall time (CPU). 60 forward passes, 24 layers each. Δθ=0.

---
*Execution agent, reporting to CEO Nova. Verdict reported as the registered decision tree produced it. Independent Law #14 verdict review commissioned next (required before adoption).*
