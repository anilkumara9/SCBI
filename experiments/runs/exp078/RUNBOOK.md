# EXP078 RUNBOOK — free-tier execution (Kaggle first, Colab backup)

**Cost: $0.** No paid GPU, no API keys, no sign-ups beyond a free Kaggle/Google account.

**What you are running:** the pre-registered EXP078 protocol
(`experiments/protocols/EXP078_SUBSPACE_BRIDGE_REREG_PREREG_SPEC.md`) — a
**boundary-characterization and loop-motivation experiment, not a novelty
experiment** (protocol §1.1). It tests whether the known-working output bridge
retains its rescue when restricted to the rank-5 per-vocabulary contrast
subspace S. In-scope config only: **pythia-410m, layer 20, α=0.50**.

**Bundle status: BUILT — CLEARED FOR EXECUTION (Law #14 diff re-verification
LOG-107, 2026-09-23).**

---

## Path A — Kaggle (primary; 30 hrs/week free GPU)

0. **Phone verification (do this FIRST — the #1 first-run failure).** New Kaggle
   accounts get **no GPU quota until the phone number is verified**: go to
   **kaggle.com → your avatar → Settings → Phone verification** and complete it.
   Without this, step 2 below will silently offer no GPU option and the script
   will abort loudly with "FATAL: no CUDA GPU detected" (that abort is the
   script protecting you from a many-hours CPU run — do not bypass it with
   `--allow-cpu` unless you know what you are doing).
1. Go to **kaggle.com** → sign in → **Create → New Notebook**.
2. Right-hand panel → **Accelerator: GPU T4 x2**. (Free quota: 30 h/week. This run
   needs well under that: ≈1,080 total forward passes (≈720 condition + 300
   support + 60 baseline), <30 min.)
3. Right-hand panel → **Internet: ON**. Required: HuggingFace model download +
   pip. Without internet the run cannot start.
3b. **Pre-flight GPU check (new cell, run before anything else).** If this
   errors, STOP — do not run the experiment on CPU:
   ```python
   !nvidia-smi --query-gpu=name,memory.total --format=csv
   import torch
   assert torch.cuda.is_available(), \
       "NO GPU DETECTED. Enable Accelerator: GPU T4 x2 (step 2; new accounts: step 0 first)."
   print("GPU OK:", torch.cuda.get_device_name(0))
   ```
4. Upload the bundle. The execution bundle is the whole `experiments/runs/exp078/`
   directory (`run_exp078.py`, `evaluate_exp078.py`, `test_evaluate_exp078.py`,
   `requirements.txt`, `RUNBOOK.md`, `UNTESTED_ASSUMPTIONS.md`). Do NOT upload the
   entire SCBI repo — the bundle is self-contained (it downloads
   `EleutherAI/pythia-410m` from Hugging Face at runtime).
   - Kaggle → Create → New Notebook → File → Upload: upload all files in
     `experiments/runs/exp078/` (or zip them and unzip in the first cell).
5. In the first cell, install dependencies and verify:
   ```python
   !pip install -q -r requirements.txt
   !python3 -m py_compile run_exp078.py evaluate_exp078.py test_evaluate_exp078.py
   !python3 test_evaluate_exp078.py     # expect: ALL EXP078 EVALUATOR BRANCH TESTS PASSED
   !python3 -c "import torch; print('cuda:', torch.cuda.is_available())"  # expect: True
   ```
6. Run (from the directory containing the bundle files):
   ```python
   !python3 run_exp078.py
   ```
   - Outputs land in `experiments/runs/EXP078_subspace_bridge/` (created
     relative to the working directory).
   - Expected runtime: <30 min on T4 (≈1,080 total forward passes: ≈720
     condition + 300 support + 60 baseline).
   - **Do not interrupt**: a killed session mid-run is data per Law #8, but a
     completed run is what the decision tree needs.
   - Watch the log: the **rank guard (§3.1), energy gate (§3.4), and headroom
     gate (§5)** can halt the run early. A halt IS the reportable outcome —
     save the outputs anyway (see step 8).
7. Get the ruling (in the same notebook, or locally after download):
   ```python
   !python3 evaluate_exp078.py
   ```
   This prints one of the pre-registered branches (a/a'/b/c/d/e/f/g/h/i)
   VERBATIM. That printed ruling is the result of EXP078.
8. **Download:** in a final cell:
   ```python
   !tar czf /kaggle/working/exp078_artifacts.tar.gz -C experiments/runs EXP078_subspace_bridge
   ```
   then download `/kaggle/working/exp078_artifacts.tar.gz` from the output panel.
   (Or **Save Version → Save & Run All** to persist outputs to the notebook's
   version history.)

## Path B — Google Colab (backup; free tier GPU)

1. **colab.research.google.com** → New notebook.
2. **Runtime → Change runtime type → Hardware accelerator: T4 GPU** → Save.
3. Same cells as Path A steps 4–7 (Colab has internet on by default).
4. Colab free tier may throttle or disconnect long sessions; if the run dies
   mid-way, re-run — the script has no checkpointing (a halt or crash means
   re-running from scratch; Law #8: keep the failed log, it is data).
5. Download via `files.download()`:
   ```python
   from google.colab import files
   !tar czf /content/exp078_artifacts.tar.gz -C /content/experiments/runs EXP078_subspace_bridge
   files.download('/content/exp078_artifacts.tar.gz')
   ```

## What success looks like (checklist)

- [ ] `exp078_run_log.txt` shows: model loaded → pre-hash logged →
      registered-hash sanity check → S constructed, rank guard PASSED →
      energy gate PASSED (median e reported + sensitivity) → headroom PASSED →
      Stage B 7-condition ledger → `Delta theta == 0` confirmed → artifacts saved.
- [ ] `exp078_results.json` has `"outcome": "COMPLETED"` and
      `"protocol_scope": "IN-SCOPE (pythia-410m, layer 20)"`.
- [ ] `evaluate_exp078.py` prints one of the pre-registered branches.
- [ ] `exp078_vectors.pt` exists (Law #13 archive: Q_S, v_hat_k, per-item
      projections pre/unit norm, energy ratios, rank diagnostics).

## If a gate HALTS — read this

**A halt is not a failure. It is the reportable outcome of EXP078**
(protocol §7.2). Do NOT adjust the subspace construction, energy bar, or
headroom handling and re-run under the EXP078 label — that is forbidden (it
would make the gates p-hacking-adjacent). Instead:

1. Download `exp078_results.json` + `exp078_run_log.txt` (the halt diagnostics).
2. Run `evaluate_exp078.py` — it will print the branch ruling verbatim:
   - `(a)` energy halt: **uninformative causal test, informative localization
     measurement** — the low e *is* the evidence that the bridge's causal
     power lies almost entirely outside S. Re-design required, not a kill.
   - `(a')` rank halt: S is degenerate — re-design required.
   - `(b)` headroom halt: benchmark miscalibrated — no conclusions.
3. Report the halt back. Any adjusted design takes the **next free number at
   pre-registration time** (protocol §9).

## What you must NOT do

- Do not edit the protocol file.
- Do not change seeds, the 0.10 energy bar, the rank-guard ratio, or gates
  "to make it work".
- Do not interpret C4/C5 in an invalid run (branch (c): C3 failed to replicate).
- Do not read branch (e) as loop validation: it licenses only a
  label-informed, per-item existential direction inside S; mechanism
  (relational vs. logit-steering) is unidentified; label-free findability is
  not established.
- Any changed design = the next free experiment number at pre-registration
  time. Return failures as failures.

## After the run

Send back `exp078_results.json` (and the log). The ruling from
`evaluate_exp078.py` determines the next step per the pre-registered tree —
supported / falsified / mixed / invalid / halted — and the program proceeds
from there. Do not reinterpret the numbers outside the decision tree (Law #9).
