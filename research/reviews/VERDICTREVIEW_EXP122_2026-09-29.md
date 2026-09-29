# Independent exact-artifact verdict review — EXP122 (H16/POSITION-CUE)

**Reviewer lane:** LOG-4654 (pre-assigned). Independent review; no prior contact with the execution lane's work product beyond the artifacts it produced. Read-only on everything except this review and the LOG-4654 research-log append. $0 CPU.

## Review method

All checks were recomputed from the exact artifacts, never from the report text:
- Signed protocol (post-four-fix): `research/prereg/EXP_PREREG_H16_POSITIONCUE_2026-09-29.md`
- Raw run directory: `experiments/runs/EXP122_positioncue/out/` (canonical bench JSON, embeddings npz, head params npz, train/test ID lists, result JSON, both run logs)
- Builder script: `experiments/runs/EXP122_positioncue/build_exp122_bench.py`
- Executor script: `experiments/runs/EXP122_positioncue/exp122_execute.py`
- Authoritative log: `reports/research_log.md` (LOG-4653)

## 1. Registered bars (protocol §4, falsification tree)

- **CONTINUE:** overall test accuracy ≥ 20/30 **AND** G < 0.30, where G = acc(flipped=False) − acc(flipped=True) over the word-family cells (N_F = N_T = 15).
- **KILL:** overall ≤ 18/30 **OR** G ≥ 0.30.
- **HELD:** overall = 19/30 with G < 0.30.

## 2. Independent recomputation of the metric (from raw artifacts)

Recomputed by loading `exp122_embeddings.npz` + `exp122_head_params.npz`, scoring the 30 test IDs against the canonical bench labels with `pred = (Xw + b ≥ 0)`:

| Quantity | Lane claim | Reviewer recompute |
|---|---|---|
| Test accuracy | 27/30 = 0.9000 | **27/30 = 0.9000** ✓ |
| acc(flipped=False) | 0.8667 | **0.8667** (13/15) ✓ |
| acc(flipped=True) | 0.9333 | **0.9333** (14/15) ✓ |
| G | −0.0667 | **−0.0667** ✓ (sign convention per protocol) |
| Exact one-sided p | 0.0000042 | **4.2151659727e-06** ✓ (my own `math.comb` computation matches the executor's `4.215165972709656e-06`) |
| Per-cell (target-first/original, target-first/flipped, target-last/original, target-last/flipped) | 0.75 / 1.0 / 1.0 / 0.875 | **6/8 / 7/7 / 7/7 / 7/8** ✓ |
| N_F, N_T | 15, 15 | **15, 15** ✓ |
| Train/test overlap | 0 | **0** ✓ (30/30) |
| Test IDs ⊆ bench IDs, no extras | — | **verified** ✓ |

Bars applied: 27 ≥ 20 ✓ and G = −0.0667 < 0.30 ✓ → **CONTINUE** follows from the artifacts.

## 3. Position-scramble design (recomputed from the canonical bench JSON, not the builder summary)

- 60 items; y balanced 30/30.
- y = 1 iff tuple[0] ∈ D1 (animals), verified with an independent animal/fruit classification: **0/60 mismatches**. D1 = {Lion, Tiger, Bear, Wolf, Fox}; D2 = {Apple, Mango, Cherry, Grape, Plum} — fresh domains, disjoint from bench 1/2 sets.
- Target final sentence position balanced **15/15 within each label class** (corr(domain, final_first) = 0.0) — the scramble holds in the actual bench.
- Four 15-item cells (phrasing × flipped); hops 30/30 (2/3); two verb families ("ranks above/below", "dominates/is dominated by").

## 4. Construction gates and split

| Gate | Protocol bar | Lane record | Reviewer recompute |
|---|---|---|---|
| G-C1 (pure-template, family-1 = ranks) | ≤ 36/60 | 32/60 | **32/60** ✓ |
| Position-scramble (P: y=1 iff final_first) | ≤ 36/60 | 30/60 | **30/60** ✓ |
| G-C2 | \|Pearson(r1, r3)\| ≤ 0.10 | 0.0322 | gate record stands; threshold verified (bench-1 builder records not re-read per Law #13 fence) |
| G-C3 (QUESTION_SUFFIX byte-exact, premise extraction contract) | pin | pass | **byte-exact on all 60 items** ✓; unique IDs ✓ |
| Split disjointness | overlap → RUN-INVALID | 0 | **0** ✓ |
| Per-cell test counts | 8/7/7/8 | 8/7/7/8 | **(target-first,False)=8, (target-first,True)=7, (target-last,False)=7, (target-last,True)=8** ✓ |

## 5. Backbone, hashes, determinism, LOG continuity

- **Δθ=0:** backbone pre_hash = post_hash = `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed`, matching the LOG-331 frozen pin recorded in the research log (LOG-9126 guard). dtheta0=true.
- **Artifact hash pins:** all seven pins in `exp122_result.json` (builder script, canonical JSON, per-item JSON, embeddings npz, train IDs, test IDs, head params) match sha256 of the current files — byte-identical.
- **Deterministic rerun:** the two run logs (`exp122_console.log` vs `exp122_console_run1.log`, `exp122_stdout.log` vs `exp122_stdout_run1.log`) differ **only in wall-clock/progress-bar lines**; metrics and all artifact hashes are byte-identical across runs. The lane's deterministic-rerun claim is supported.
- **P-value provenance:** executor-computed via `math.comb` (line 64–65 of `exp122_execute.py`, docstring "Exact one-sided P(X >= k | n, 0.5), executor-computed"); result JSON records `p_computed_by: "executor (math.comb)"`; stdout log prints "executor-computed p: one-sided=0.0000042 two-sided=0.0000084". Defect class (a) honored — nothing handwritten.
- **LOG continuity:** LOG-4653 is the highest numbered entry (exactly one), and its substance (bench construction, all gate scores, extraction, metric, verdict, file paths) matches the artifacts on every checked number. LOG-4654 was next-free; continuity 4653 → 4654 holds.

## Verdict

**BIND — no caveat.** The execution lane's CONTINUE follows from the raw artifacts through the registered bars: 27/30 ≥ 20/30 and G = −0.0667 < 0.30, on a bench whose position cue is independently verified as non-informative about the label (15/15 within each label class, corr = 0.0). Every recomputed number matches exactly. Backbone frozen, record complete and hash-pinned, p-value executor-computed, rerun deterministic.

Narrow reading preserved: this CONTINUE means the trained head extracts the target's domain-set identity with position decorrelated — decodability, not steering or capability. Capability scoreboard unchanged.
