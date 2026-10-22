# EXP139 Stage-2 — Founder GPU Execution Bundle

**Experiment:** EXP139 / S4-4 — re-entrant attractor dynamics, Stage-2 full attractor test (T=8).
**Protocol (binding):** `research/prereg/EXP139_S44_prereg_DRAFT_2026-10-03.md` (SIGNED, LOG-4885), §5.
**Stage-1 result:** κ̂ = 0.955971 < 1 (LOG-4886) — contraction license SURVIVES; Stage-2 gate is open.
**Status:** bundle built and CPU-tested 2026-10-03; Law #14 apparatus review (LOG-4896) and follow-up repair verification (LOG-4897) complete — founder GPU execution licensed.

## What this bundle does

Runs the pre-registered Stage-2 protocol: all 60 bench items (view 0), T=8 fixed
re-entrant iterations (480 R-evaluations + 60 baseline passes = **540 forward passes**),
decodes the t=8 attractor state, computes ΔM_attractor vs the committed baseline with
the pre-registered Newcombe paired 95% interval, and checks the binding trajectory
diagnostic (‖h^(t+1)−h^(t)‖₂ strictly decreasing, t=0..7). Frozen backbone (Δθ=0);
no training; validity gates (bench pin, backbone pin, 60/60 yhat fidelity) trip to
RUN-INVALID, never to a verdict.

## Founder steps (Kaggle, GPU notebook, T4)

1. **New Kaggle notebook** → Settings → Accelerator: **GPU (T4)**; **Internet: ON**.
2. **Upload this bundle's files** into the notebook working directory (keep the
   folder structure: `run_stage2.py`, `exp139_stage2_lib.py`, `requirements.txt`,
   `data/`, `tests/`).
3. **Download the pinned model** (one cell; public repo, no login needed):
   ```
   !huggingface-cli download EleutherAI/pythia-410m --revision 9879c9b5f8bea9051dcb0e68dff21493d67e9d4f
   ```
4. **Install the pinned environment** (one cell):
   ```
   !pip install -r requirements.txt
   ```
5. **Run the CPU structural tests first** — no GPU contact, no downloads; zero FAILs
   required (SKIP lines are expected on Kaggle — provenance checks verify
   build-machine files):
   ```
   !python tests/test_bundle_cpu.py
   ```
6. **Run Stage-2** (minutes on a T4):
   ```
   !python run_stage2.py
   ```
   Expected console markers: backbone pre-hash `ec276abe…`, bench sha256 `eb304fa6…`,
   `(c) baseline yhat match: 60/60`, `forwards total=540`, `CLEAN COMPLETION exit 0`.
   Exit code **44** means RUN-INVALID (a validity gate tripped) — stop and send the log.
7. **Send back to the CEO:** `out/stage2_run_log.txt`, `out/stage2_records.json`,
   `out/stage2_verdict.json`, `out/RUN_REPORT.md`.

## What the outputs mean

- `stage2_verdict.json` → paired table (b, c), Newcombe Δ̂/L/U, trajectory diagnostic,
  and the §6 branch report.
- If Δ̂ ≤ 0 the report emits **HELD(f)** ("converges to nothing useful — dynamics
  exist, no capability; licenses nothing, kills nothing") per the binding Law #14
  apparatus-review adjudication (LOG-4896): the §6 falsification table governs;
  the pre-reg's §0 breaking-points line and §5 bar assigning KILL are superseded
  as drafting defects. This is a pre-execution disambiguation of a drafting
  defect, not a post-hoc bar shift.

## Documented execution choices (not protocol changes)

- **540 passes, not 520:** the pre-reg's cost line assumes reusing Stage-1's 20 h_i
  states, but Stage-1 archived only norms, not vectors — all 60 baselines are
  recomputed (deterministic per machine; cross-machine equivalence is anchored
  by validity gates (a)–(c), not by a bitwise claim).
- **Trajectory backstop:** strictly decreasing diff-norms (t=0..7) required on
  **all 60 items** (strict) — the conservative reading of the pre-reg's
  unaggregated "must be strictly decreasing" (see BUNDLE_NOTES.md).
- **Readout convention:** two-way candidate comparison, matching Stage-1 and the
  committed EXP135 records (the pre-reg §2 text says full-vocab argmax; the paired
  table is only well-defined under the two-way convention).
- **Gate (c)** extended to 60/60 as the direct analog of §3(c); the paired table
  still uses the COMMITTED baseline yhat.
- Full audit: `BUNDLE_NOTES.md`.
