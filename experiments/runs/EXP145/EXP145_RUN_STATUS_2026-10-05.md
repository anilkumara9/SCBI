# EXP145 — Execution Status (2026-10-05) — COMPLETE

## VERDICT: KILL/PIVOT (decode− / steer−, intervention arm not licensed)

The frozen four-cell table was applied exactly. The generality claim is
killed/bounded with the recorded caveat: the gap's precondition
(decodability) is absent here; this outcome cannot separate an architecture
effect from scale/bench-fit (the §1 steelman). The dissociation itself is
untested in this family.

## Key numbers

- D1: PASS — layers [8, 10] with p < 0.05/12 and (acc−q95) ≥ 0.10;
  l*=8, acc=0.2833, p=0.000999, effect=+0.1333 (layer 10: acc=0.2500,
  p=0.000999, effect=+0.1000, boundary-inclusive).
- D2: FAIL — mean_i cos(v^(−i), u_i) = −0.4587 (bar 0.70); l*=8.
  The LOO corrections do not cohere into a shared direction in GPT-2-small.
- decode+ = D1 AND D2 = FALSE → decode− → intervention arm NOT licensed.
- S2 (LM log-prob baseline, non-binding): acc=0.4833 (29/60),
  mean raw-logit margin=−0.4475.
- Model revision: `607a30d783dfa663caf39e06633721c8d4cfcd7e` (S0.2,
  character-identical).
- Bench pin: `b9eac3893ddfbc67400a5d2b5cbb694ba81308471caf4a150476227065e56545`.
- Δθ=0 asserted by pre/post state-dict hash (extraction phase). $0 CPU.

## Step 0: FULL PASS (exit 0)

All S7-2b §4 Step-0 gates passed. The run proceeded past the point where
EXP144 stopped.

| Gate | Result |
|---|---|
| S0.2 model revision (programmatic resolve + assert) | PASS — `607a30d783dfa663caf39e06633721c8d4cfcd7e`, character-identical to plan pin |
| S0.1 bench pin (recomputed over loaded pinned JSON) | PASS — `b9eac3893ddfbc67400a5d2b5cbb694ba81308471caf4a150476227065e56545`, character-identical |
| S0.1a procedural cross-check (Law #14 fix 3) | PASS — procedural pin == loaded JSON pin |
| G0 bench provenance | PASS — 60/60 unique, strata match |
| G2 oracle diagnostic (re-bound to new pin) | PASS — 0.0607, p=0.5312, bit-identical to committed |
| Tokenizer files downloaded (weights NOT downloaded) | 13 files at pinned revision |
| **G1′ live re-fire (the EXP144-killer)** | **PASS — 240/240 single-token under GPT-2 BPE** |

Full log: `exp145_step0_log.txt`. Manifest: `exp145_manifest.json`.

## Extraction arm: BLOCKED on runtime user-confirmation gate

The extraction script (`exp145_extract.py`: 60 forward passes, GPT-2-small,
CPU, incremental JSONL records) was launched in the execution venv
(`~/workspace/.exp_venvs/exp142`, torch 2.14.1+cpu) but the background exec
entered `pending_user_confirmation` status with zero output — a runtime
approval gate, most likely on the ~500MB weights download from the HF Hub.
Session: `proc_4a77fec7f54f` (pid 10574). Left pending (not killed) in case
the approval is granted and it can proceed.

No forward passes have executed. No verdict exists. Δθ=0 trivially holds
(weights never accessed).

## Bundle adaptations (all licensed)

- `exp145_*.py` copied from the staged EXP144 bundle with mechanical
  `exp144_`→`exp145_` / `EXP144`→`EXP145` renames; no algorithmic changes.
- `exp145_common.py`: `build_bench()` loads the pinned S7-2b JSON (the
  single licensed execution-side change, S7-2b §7); `guard_g2_oracle()`
  re-binds the derivation-time diagnostic (bit-identical) to the new pin;
  added `guard_s01a_procedural_crosscheck()` (Law #14 fix 3).
- `exp145_step0_download.py`: S0.1/S0.1a/S0.2 asserts per S7-2b §4.
- `exp145_verdict.py`: writes EXP145 deliverables + a LOG-4922 entry DRAFT
  (`exp145_log_entry_draft.md`); the research-log prepend is the parent's lane.

## To resume

1. Approve/clear the pending confirmation on `proc_4a77fec7f54f`, or
   re-run: `~/workspace/.exp_venvs/exp142/bin/python exp145_extract.py`
   from `~/workspace/SCBI/experiments/runs/EXP145/` (records are incremental;
   completed items are skipped).
2. Then: `exp145_decode.py` (numpy) → `exp145_directions.py` →
   `exp145_decision.py` (only if D1+D2 pass) → `exp145_verdict.py`.
