# EXP070 RUNBOOK — Oracle-Selection Ceiling (pre-registered)

**Protocol (DO NOT MODIFY):** `experiments/protocols/EXP070_ORACLE_CEILING_PREREG_SPEC.md`
**Runner:** `experiments/runs/exp070/run_exp070.py`
**Evaluator:** `experiments/runs/exp070/evaluate_exp070.py`
**Tests:** `experiments/runs/exp070/test_evaluate_exp070.py`
**Scope:** IN-SCOPE only — `EleutherAI/pythia-160m`, layer 10, α=0.50.

> This experiment must run on a GPU (Kaggle free T4 x2 or Colab free T4).
> It was built on a CPU-only machine; only the syntax and the decision-tree
> tests can be validated locally. **No model execution has happened locally.**

---

## Step 0 — Kaggle account readiness (do this FIRST)

EXP070 needs ~5,520 forward passes (≈45 min on T4 per the protocol's
conservative basis). On a free Kaggle account:

1. Sign in at kaggle.com.
2. **New accounts must verify a phone number before GPUs unlock:**
   account avatar → Settings → Phone verification.
3. In the notebook: right panel → **Accelerator: GPU T4 x2**.
4. Quota is ~30 GPU-hours/week — this run uses <1 hour.

(Colab alternative: Runtime → Change runtime type → T4 GPU. Same steps below.)

---

## Step 1 — Upload the bundle

The execution bundle is the whole `experiments/runs/exp070/` directory
(`run_exp070.py`, `evaluate_exp070.py`, `test_evaluate_exp070.py`,
`requirements.txt`, `RUNBOOK.md`, `UNTESTED_ASSUMPTIONS.md`).
Do NOT upload the entire SCBI repo to Kaggle — the bundle is self-contained
(it downloads `EleutherAI/pythia-160m` from Hugging Face at runtime).

Option A — notebook upload:
1. Kaggle → Create → New Notebook.
2. File → Upload: upload all files in `experiments/runs/exp070/`
   (or zip them and unzip in the first cell).

Option B — git (if the repo is public):
`!git clone <repo-url>` then `cd` into `experiments/runs/exp070/`.

---

## Step 2 — Install and verify

```python
!pip install -r requirements.txt
!python3 -m py_compile run_exp070.py evaluate_exp070.py test_evaluate_exp070.py
!python3 test_evaluate_exp070.py     # expect: ALL EXP070 EVALUATOR BRANCH TESTS PASSED
!python3 -c "import torch; print('cuda:', torch.cuda.is_available())"  # expect: True
```

If `cuda: False`, go back to Step 0 — the T4 x2 accelerator is not enabled.
The runner **refuses to start** without CUDA (explicit `SystemExit`), by design.

---

## Step 3 — Run

```python
!python3 run_exp070.py
```

- Working directory should be the repo root so outputs land in
  `experiments/runs/EXP070_oracle_ceiling/`.
- Expected runtime: ≈45 minutes on T4 (conservative basis; likely faster).
- **Do not interrupt**: a killed session mid-run is data per Law #8, but a
  completed run is what the decision tree needs.
- Watch the log: the **probe-construction gate (§4) and headroom gate (§6)**
  can halt the run early. A halt is the reportable outcome — save the outputs
  anyway (see Step 4).

What the run produces in `experiments/runs/EXP070_oracle_ceiling/`:
- `exp070_results.json` — decision inputs + probe gate + comparisons
- `exp070_instance_records.json` — per-instance C1..C7 correctness/KL
- `exp070_vectors.pt` — Law #13 archive (pool vectors, probe records,
  tie-break draws, support/test id lists)
- `exp070_run_log.txt` — full console log

---

## Step 4 — Evaluate (decision tree)

```python
!python3 evaluate_exp070.py experiments/runs/EXP070_oracle_ceiling/exp070_results.json
```

The evaluator prints the **pre-registered ruling branch verbatim** — that
ruling (not your own summary) is the result of EXP070.

---

## Step 5 — Return artifacts

Download from the Kaggle output / copy locally:
1. `exp070_results.json`
2. `exp070_instance_records.json`
3. `exp070_vectors.pt`
4. `exp070_run_log.txt`
5. The evaluator's printed ruling (paste or screenshot)

Place them in `experiments/runs/EXP070_oracle_ceiling/` in the local repo
and hand the evaluator ruling to the research manager (parent agent) —
**no human interpretation of the outcome before the tree rules.**

---

## Troubleshooting

| Symptom | Cause / fix |
|---|---|
| `FATAL: no CUDA GPU detected` | T4 x2 not enabled (Step 0). Do NOT pass `--allow-cpu` to work around this. |
| `HALT_PROBE` in the log | Probe-construction gate: fewer than 50 instances matched ≥3 probe items. This is branch (a) — the halt is the reportable outcome. Return the JSON. |
| `HALT_HEADROOM` in the log | Baseline accuracy outside 40–70%. Branch (a) — return the JSON. |
| `FATAL (anti-cheat)` assertion | Probe/support lists overlap test ids — a protocol violation. Stop; report; do not "fix" by editing. |
| `FATAL (F1 guard)` assertion | A zero-norm injection vector reached the hook — would have been a silent no-op. Report as a fatal data-hygiene abort. |
| `INVALID_RUN` (branch b) | C7 bridge did not rescue — setup broken or benchmark drifted. No conclusion may be drawn. |
| Session killed mid-run | Law #8: the partial log is data. Return it with a note of where it stopped. |
| `torch.use_deterministic_algorithms` warning | Non-fatal; logged. Determinism is best-effort on GPU. |

## What you must NOT do

- Do not edit the protocol file.
- Do not change seeds, pool size, probe size, or gates "to make it work".
- Any changed design = the next free experiment number at pre-registration
  time (protocol §9). Return failures as failures.
