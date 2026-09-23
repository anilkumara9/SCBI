# EXP079 RUNBOOK — Oracle-Selection Ceiling with Out-of-Sample Probe (pre-registered)

**Protocol (DO NOT MODIFY):** `experiments/protocols/EXP079_BETTER_PROBE_PREREG_SPEC.md`
**Runner:** `experiments/runs/exp079/run_exp079.py`
**Evaluator:** `experiments/runs/exp079/evaluate_exp079.py`
**Tests:** `experiments/runs/exp079/test_evaluate_exp079.py`
**Scope:** IN-SCOPE only — `EleutherAI/pythia-160m`, layer 10, α=0.50.

> This experiment must run on a GPU (Kaggle free T4 x2 or Colab free T4).
> It was built on a CPU-only machine; only the syntax, the decision-tree
> tests, the null-bar computation, and the probe-construction gate were
> validated locally. **No GPU execution has happened locally.**

**Mandate:** EXP079 is the better-probe re-registration mandated by EXP070's
branch-(c2) ruling (LOG-110). It must never be a silent re-run of EXP070.
The design delta (§0): split-half support (BUILD/HELDOUT), up-to-15-item
out-of-sample probes (min 8), and a calibrated H_sel null bar (95th pct,
seed 7979, computed at runtime with the realized N_final).

---

## Step 0 — Kaggle account readiness (do this FIRST)

EXP079 needs ~15,720 forward passes worst case (≈2 h on the protocol's
conservative basis; ~15–30 min expected on T4 for pythia-160m). On a free
Kaggle account:

1. Sign in at kaggle.com.
2. **New accounts must verify a phone number before GPUs unlock:**
   account avatar → Settings → Phone verification.
3. In the notebook: right panel → **Accelerator: GPU T4 x2**.
4. Quota is ~30 GPU-hours/week — this run uses well under 2 hours.

(Colab alternative: Runtime → Change runtime type → T4 GPU. Same steps below.)

---

## Step 1 — Upload the bundle

The execution bundle is the whole `experiments/runs/exp079/` directory
(`run_exp079.py`, `evaluate_exp079.py`, `test_evaluate_exp079.py`,
`requirements.txt`, `RUNBOOK.md`, `UNTESTED_ASSUMPTIONS.md`).
Do NOT upload the entire SCBI repo to Kaggle — the bundle is self-contained
(it downloads `EleutherAI/pythia-160m` from Hugging Face at runtime).

Option A — notebook upload:
1. Kaggle → Create → New Notebook.
2. File → Upload: upload all files in `experiments/runs/exp079/`
   (or zip them and unzip in the first cell).

Option B — git (if the repo is public):
`!git clone <repo-url>` then `cd` into `experiments/runs/exp079/`.

---

## Step 2 — Install and verify

```python
!pip install -r requirements.txt
!python3 -m py_compile run_exp079.py evaluate_exp079.py test_evaluate_exp079.py
!python3 test_evaluate_exp079.py     # expect: ALL EXP079 EVALUATOR BRANCH TESTS PASSED
!python3 -c "import torch; print('cuda:', torch.cuda.is_available())"  # expect: True
```

If `cuda: False`, go back to Step 0 — the T4 x2 accelerator is not enabled.
The runner **refuses to start** without CUDA (explicit `SystemExit`), by design.

---

## Step 3 — Run the experiment

```python
!python3 run_exp079.py
```

Order of operations (§9): probe-construction/N_final gate (metadata) →
5-instance pilot (degeneracy → loud HALT) → full probe + oracle selection →
conditions C1..C7 → diagnostics → `exp079_results.json` +
`exp079_instance_records.json` + `exp079_vectors.pt` + `exp079_run_log.txt`
in `experiments/runs/EXP079_better_probe/`.

**Expected gates:** (1) `N_final >= 50` else `HALT_PROBE`; (2) baseline
40–70% else `HALT_HEADROOM`; (3) pilot degeneracy (EXP070's failure mode)
else `HALT_DEGENERACY`. **Halts are reportable outcomes** (Law #8) — the
evaluator routes every halt payload to branch (a).

> **Builder's finding (CPU-verified, see UNTESTED_ASSUMPTIONS.md):** under the
> signed spec's exact construction (5-vocabulary support, even/odd split,
> (hop, index-pattern) probe key), the HELDOUT match counts give
> **N_final = 26 < 50**, so gate (1) is expected to fire and the GPU run
> should terminate in minutes with a reportable `HALT_PROBE` (branch (a)).
> This is the faithful execution of the pre-registered gate — do not
> "fix" the matching, split, or thresholds to force the run through; that
> would be a protocol change requiring re-registration (Law #4). The Law #14
> bundle review must rule on this before any GPU launch.

---

## Step 4 — Evaluate (the ruling)

```python
!python3 evaluate_exp079.py experiments/runs/EXP079_better_probe/exp079_results.json
```

The evaluator prints the pre-registered decision-tree ruling VERBATIM:
branch (a)/(b)/(c1*)/(c2*)/(c3*)/(d)/(e)/(f) with its LICENSES /
DOES-NOT-LICENSE text. Copy the ruling verbatim into the run report.

---

## Step 5 — Preserve artifacts

Download from the notebook output directory:
- `exp079_results.json` (primary artifact)
- `exp079_instance_records.json`
- `exp079_vectors.pt` (Law #13 vector archive)
- `exp079_run_log.txt`

Record SHA-256 + sizes of each. The Δθ=0 binding guard is the runtime
pre/post parameter-hash match, printed in the log.
