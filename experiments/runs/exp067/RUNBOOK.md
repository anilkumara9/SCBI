# EXP067 RUNBOOK — free-tier execution (Kaggle first, Colab backup)

**Cost: $0.** No paid GPU, no API keys, no sign-ups beyond a free Kaggle/Google account.

**What you are running:** the pre-registered EXP067 protocol
(`experiments/protocols/EXP067_QKOV_SUBSPACE_PROCRUSTES_SPEC.md`) — a
boundary-characterization experiment, not a novelty experiment (protocol §1.1).
Default config is **pythia-410m** (IN-SCOPE, the pre-registered configuration);
`--model pythia-160m` is an OUT-OF-SCOPE pilot only (bannered at runtime, and the
evaluator prints NO PROTOCOL RULING for it).

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
   needs well under that.)
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
4. In the first cell, install dependencies:
   ```python
   !pip install -q transformers>=4.44 scipy>=1.13
   ```
   (torch ships with the Kaggle image; the command above only upgrades what is
   stale. Alternatively `!pip install -q -r SCBI/experiments/runs/exp067/requirements.txt`
   after cloning.)
5. Clone the repo (public):
   ```python
   !git clone https://github.com/anilkumara9/SCBI.git
   %cd SCBI
   ```
   If your working copy has local-only files (this execution bundle), the clone
   will NOT contain `experiments/runs/exp067/`. Upload it with copy-paste commands:
   ```python
   # a) On your machine: zip the bundle folder -> exp067_bundle.zip
   #    (zip the folder experiments/runs/exp067/ including its name)
   # b) In the notebook: Add data -> Upload -> select exp067_bundle.zip
   # c) Find the dataset slug shown under the uploaded data (e.g. "anilkumar/exp067-bundle"),
   #    then run:
   !mkdir -p /tmp/exp067bundle && unzip -o "/kaggle/input/<dataset-slug>/exp067_bundle.zip" -d /tmp/exp067bundle
   !cp -r /tmp/exp067bundle/experiments/runs/exp067 ./experiments/runs/exp067
   !ls experiments/runs/exp067   # must show: run_exp067.py  evaluate_exp067.py  RUNBOOK.md  requirements.txt
   ```
   Replace `<dataset-slug>` with the exact name shown in the right-hand panel
   under your upload. If the `ls` does not show `run_exp067.py`, the copy failed —
   do not proceed; re-check the slug and the zip's internal folder structure.
6. Run (from the repo root) — the in-scope pre-registered configuration (default):
   ```python
   !python experiments/runs/exp067/run_exp067.py
   ```
   For an out-of-scope smoke pilot only (prints a banner; evaluator gives no ruling):
   ```python
   !python experiments/runs/exp067/run_exp067.py --model pythia-160m
   ```
7. **Expected runtime:** tens of minutes ×2–4 for pythia-410m on a T4 (~2,100 short
   forward passes total: 560 anchor + 300 support-contrast + ~1,260 Stage B).
   The log streams progress per stage.
   Watch the first minutes: the head-decomposition self-check (§2b) must pass —
   if it fails, the run aborts loudly (that is a finding about the environment,
   not a bug to patch around).
8. **Outputs land in** `experiments/runs/EXP067_qkov_subspace_procrustes/`:
   - `exp067_results.json` — all statistics + the outcome flag
   - `exp067_vectors.pt` — Law #13 archive (anchors, rotations, bases)
   - `exp067_instance_records.json` — per-instance records
   - `exp067_run_log.txt` — full log
9. Get the ruling (in the same notebook, or locally after download):
   ```python
   !python experiments/runs/exp067/evaluate_exp067.py
   ```
   This prints one of the pre-registered branches (a/b/c1/c2/c3/d/e) VERBATIM
   for an in-scope run. For a `--model pythia-160m` pilot it prints
   `NO PROTOCOL RULING -- OUT-OF-SCOPE PILOT` with raw statistics instead —
   that is the correct behavior; do not quote pilot numbers as a ruling.
10. **Download:** Kaggle → notebook **⋯ menu → Download** won't include cell
    outputs' files; instead, in a final cell:
    ```python
    !tar czf /kaggle/working/exp067_artifacts.tar.gz -C experiments/runs EXP067_qkov_subspace_procrustes
    ```
    then download `/kaggle/working/exp067_artifacts.tar.gz` from the output panel.
    (Or **Save Version → Save & Run All** to persist outputs to the notebook's
    version history.)

## Path B — Google Colab (backup; free tier GPU)

1. **colab.research.google.com** → New notebook.
2. **Runtime → Change runtime type → Hardware accelerator: T4 GPU** → Save.
3. Same cells as Path A steps 4–9 (Colab has internet on by default).
4. Colab free tier may throttle or disconnect long sessions; if the run dies
   mid-way, re-run — the script has no checkpointing (a halt or crash means
   re-running from scratch; Law #8: keep the failed log, it is data).
5. Download via `files.download()`:
   ```python
   from google.colab import files
   !tar czf /content/exp067_artifacts.tar.gz -C /content/SCBI/experiments/runs EXP067_qkov_subspace_procrustes
   files.download('/content/exp067_artifacts.tar.gz')
   ```

## What success looks like (checklist)

- [ ] `exp067_run_log.txt` shows: model loaded → pre-hash logged →
      `Injection-vector norms (F1 guard, all > 0)` → Stage A per-head `g_h`
      table → `Stage A gate PASSED` → headroom `PASSED` → Stage B 7-condition
      ledger → `Delta theta == 0` confirmed → artifacts saved.
- [ ] `exp067_results.json` has `"outcome": "COMPLETED"` and
      `"protocol_scope": "IN-SCOPE (pythia-410m, layer 20)"`.
- [ ] `evaluate_exp067.py` prints one of the pre-registered branches (a/b/c1/c2/c3/d/e).
- [ ] `exp067_vectors.pt` exists (Law #13 archive).

## If the Stage A gate HALTS — read this

**A halt is not a failure. It is the reportable outcome of EXP067**
(protocol §7.1 branch (a), §7.2). Do NOT tweak anchors, K, templates, or seeds
and re-run under the EXP067 label — that is forbidden (it would make the gates
p-hacking-adjacent). Instead:

1. Download `exp067_results.json` + `exp067_run_log.txt` (the halt diagnostics:
   per-head `g_h` table, rank/spectral values).
2. Run `evaluate_exp067.py` — it will print the branch-(a) ruling verbatim.
3. Report the halt back: it means A-anchor/A-uniform was rejected on support
   data and H1 is untestable under this operationalization. That is a scientific
   result, and the honest one.

## After the run

Send back `exp067_results.json` (and the log). The ruling from
`evaluate_exp067.py` determines the next step per the pre-registered tree —
falsified / confirmed / mixed / invalid / halted — and the program proceeds
from there. Do not reinterpret the numbers outside the decision tree (Law #9).
