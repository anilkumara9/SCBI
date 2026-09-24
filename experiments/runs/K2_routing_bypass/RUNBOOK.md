# K2 RUNBOOK — Routing-vs-Bypass Execution Bundle

**Experiment:** K2 — "Routing vs Bypass: does the output-bridge rescue require
inter-position transport, or is it final-position-local?"
**Protocol (binding):** `research/analysis_plans/K2_ROUTING_BYPASS_PLAN_LOG223_REV2_2026-09-23.md` (SIGNED, LOG-224c)
**Build:** LOG-226 — this directory. Evaluator tests 62/62 pass (CPU).
**Model:** `EleutherAI/pythia-410m`, layer 20, α=0.5 — the ONLY registered config.
**Status:** bundle built, CPU tests green. **DO NOT EXECUTE on GPU before CEO GPU clearance.**

---

## 0. GPU access (do this first — new accounts)

1. Sign in to Kaggle. **New accounts need phone verification before any GPU quota appears.**
2. Verify quota: avatar → **Settings → Phone verification** (complete it), then any notebook → right panel → **Accelerator: GPU T4 x2** shows remaining hours.
3. If you create the notebook via the API/CLI, set the accelerator explicitly (the UI default may be CPU/none).

## 1. Create the notebook

The runner reads the pinned EXP077 archives via repo-relative paths
(`experiments/runs/EXP077_cone_vs_line/`), so the notebook needs the repo layout.
Easiest: clone the public repo in the notebook.

1. New Notebook → right panel → **Accelerator: GPU T4 x2**.
2. Copy the cell block from §5 below into the first code cell and run.

## 2. What the run does (REV2 §3.2 order)

**Phase 0 — CPU pre-execution (no GPU needed):**
1. Load tokenizer; checklist B (log SHA-256 + HF revision; missing log = recorded deviation, not INVALID).
2. Load model on CPU (float32); G3 pre-hash (state-dict SHA-256).
3. Verify pinned archive hashes (`exp077_instance_records.json`, `exp077_results.json`, `exp077_vectors.pt`).
4. Gate A: two independent per-item `b_K2` rebuilds must be byte-identical AND norms within 1e-5 of the run-logged C8 norms; tokenizer checksum + revision logged. **FAIL blocks GPU clearance with cause.**
5. Ruling-6 cross-checks: G2 (ent/typ per index vs archive), M5.1 (anchor b=14/c=0/p=0.0001220703125), M5.2 (rescue anchor ΔM=+0.2333 vs rebuilt-bench C1=0.60/C8=50/60), M5.3 (single-token entity guard), C8-norm fingerprint, F1 continuity note.
6. Benchmark rebuild (EXP077 §3 verbatim) + mask/table records.

**GPU phase (requires `--ceo-gpu-clearance`):**
7. Model to GPU; Δθ=0 guard (all params `requires_grad_(False)`).
8. Three arms × N_actual items = 180 licensed passes: (a) final-token-only, (b) premise-entity-position, (c) all-positions.
9. G3 post-hash (FATAL on mismatch), G4 pass count (= 3 × N_actual; FATAL otherwise), G5 (c)-gate (b_c ≥ 6; INVALID otherwise), G9 diagnostic (diagnostic only), G10 exclusions (≤6 ok; 7th → Underdetermined).

**Phase 9 — adjudication (CPU):** paired Tango (score) 95% CIs, kill bars L>0.05 / U<0.05,
six-row verdict table. Writes `k2_results.json`, `k2_instance_records.json`, `k2_run_log.txt`.

Expected budget: 180 forward passes, ~2–5 min on 2×T4.

## 3. After the run

1. From the notebook output (`experiments/runs/K2_routing_bypass/`), download:
   - `k2_results.json` (primary artifact)
   - `k2_instance_records.json`
   - `k2_run_log.txt`
2. Record SHA-256 of each file.
3. Run the authoritative evaluator: `python3 evaluate_k2.py` → pre-registered ruling.
   The evaluator re-derives the verdict from the archived per-item outcomes; the
   runner's verdict is display only. **Report the row verbatim.**

## 4. Verdict rows (REV2 §3.5) — what each means

| Row | Routing verdict | Local verdict | Meaning |
|---|---|---|---|
| 1 | Supported | Not supported | (b) rescues >5pp over (a); final-position channel flat |
| 2 | Not supported | Supported | (a) rescues; (b) adds nothing over (a) |
| 2r | **Refuted** | Supported | (b) rescues literally zero while (a) rescues — strong anti-routing |
| 3 | Inconclusive | Inconclusive | contrast CI straddles ±δ_min |
| 4 | Inconclusive | Inconclusive | both arms flat; (c) reproduces |
| 5 | Underdetermined | Underdetermined | a FATAL guard fired (G1/G3/G4/G5/records/G10) |

**Known plan-level defect (escalated, NOT silently fixed):** row 1's conjunct
`U(Δ̂M_a) < 0.05` ("the final-position channel demonstrably flat") is unsatisfiable
for a *flat* arm at N=60 under the plan's own Tango (score) CI — the narrowest
possible Tango 95% upper bound at N=60 is z²/(n+z²) = 0.0602 > δ_min = 0.05.
Row 1 as written can only fire when arm (a) is materially *negative*. The bundle
implements the bar exactly as written; the CEO / Law #14 process must adjudicate
whether to amend it. See BUILD_NOTES.md §4.

## 5. Notebook cell block (copy-paste)

```python
# K2 routing-vs-bypass (pre-registered REV2; SIGNED 2026-09-23; LOG-226 bundle)
# STEP 1 — CPU pre-execution (verifies gates; refuses GPU work without clearance):
!git clone --depth 1 https://github.com/anilkumara9/SCBI.git
%cd SCBI
!pip install -q -r experiments/runs/K2_routing_bypass/requirements.txt
!python3 experiments/runs/K2_routing_bypass/test_k2.py        # 62/62 must pass
!python3 experiments/runs/K2_routing_bypass/run_k2.py         # CPU only: stops at the clearance gate

# STEP 2 — GPU phase (ONLY after explicit CEO GPU clearance):
!python3 experiments/runs/K2_routing_bypass/run_k2.py --ceo-gpu-clearance

# STEP 3 — authoritative ruling:
!python3 experiments/runs/K2_routing_bypass/evaluate_k2.py
```

Without `--ceo-gpu-clearance` the runner executes Phase 0 only and exits 3 with
`GPU_CLEARANCE_REQUIRED`. Outputs land in `experiments/runs/K2_routing_bypass/`.

## 6. Reproducibility notes

- Seeds: torch 20260923, numpy 20260923, `torch.use_deterministic_algorithms(True)` when available.
- Frozen backbone: Δθ=0 enforced by pre/post state-dict SHA-256 (G3); FATAL on mismatch.
- The evaluator tests (`test_k2.py`) are seeded, deterministic, CPU-only, stdlib-only.
- The Tango (score) CI implementation reproduces the program's archived K1 Tango
  lower bounds exactly (0.0931 / 0.0651 / 0.0338 / 0.1444) and matches scipy's
  binomtest on the McNemar reduction; 95% CI Monte-Carlo coverage verified.
