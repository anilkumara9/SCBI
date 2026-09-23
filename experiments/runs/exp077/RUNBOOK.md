# EXP077 RUNBOOK — Cone-vs-Line Geometry

**Experiment:** EXP077 — "Cone-vs-Line Geometry: Is the Relational Concept Conical?"
**Protocol (binding):** `experiments/protocols/EXP077_CONE_VS_LINE_PREREG_SPEC.md` (SIGNED 2026-09-23)
**Adversarial review:** `reports/adversarial_review_exp077_prereg_2026-09-23.md` (verdict: SIGN)
**Model:** `EleutherAI/pythia-410m`, layer 20, float32 — the ONLY registered config (IN-SCOPE).
**Status:** bundle built, evaluator tests 39/39, smoke validation in progress.

---

## 0. GPU access (do this first — new accounts)

1. Sign in to Kaggle. **New accounts need phone verification before any GPU quota appears.**
2. Verify quota: avatar → **Settings → Phone verification** (complete it), then any notebook → right panel → **Accelerator: GPU T4 x2** shows remaining hours.
3. If you create the notebook via the API/CLI, set the accelerator explicitly (the UI default may be CPU/none).

## 1. Create the notebook

1. Upload `exp077_bundle.zip` as a **dataset** (Add data → Upload → your zip), or attach via the notebook's "Add data" panel.
2. New Notebook → right panel → **Accelerator: GPU T4 x2**.
3. Copy the cell block from §5 below into the first code cell and run.

## 2. What the run does (protocol §9 order)

1. SHA-256 pre-guard, F2 single-token entity guard (real tokenizer, before any forward).
2. Support build: 5 vocabs × 30 contrast pairs → `v_hat` (=B_agg), `mu`, `v_hat^c`; **continuity assertion** (gate).
3. Cone (seed 7701) + control (seed 7702) construction; build asserts (`|cos(r,v_hat)|<0.5`, `cos(u_j,v_hat)==cos(phi_j)`).
4. Benchmark N=60 + anti-cheat assert.
5. **C1** baseline → **headroom gate** [40%, 70%] (branch (d) if it fails).
6. **C8** output bridge → **bridge validity gate** (delta_m>0 AND p<0.05; branch (d) if it fails).
7. Full launch: C2–C5 (alpha grid), C6 (offset-removed), C7 (B_wrong, reported only), C9 (cone best-of-8), C10 (control best-of-8).
8. Frozen-backbone pre/post hash match (FATAL if it mismatches), Law-13 archive, results JSON.

Expected budget: ≤1,740 forward passes, ~3–6 min on 2×T4.

## 3. After the run

1. Download from the notebook output (`experiments/runs/EXP077_cone_vs_line/`):
   - `exp077_results.json` (primary artifact)
   - `exp077_instance_records.json`
   - `exp077_vectors.pt`
   - `exp077_run_log.txt`
2. Record SHA-256 of each file.
3. Run the evaluator: `python3 evaluate_exp077.py exp077_results.json` → pre-registered ruling (d)/(r)/(a)/(b)/(c).
4. **Report the branch verbatim.** The branch's LICENSE fragment states exactly what may be claimed.

## 4. Branch outcomes (protocol §8) — what each means for the program

| Branch | Meaning | Program consequence |
|---|---|---|
| (d) INVALID | a gate fired (headroom / bridge / continuity / anti-cheat) | No geometry claim; re-design, new experiment number |
| (r) REPLICATION FAILURE | C3 (alpha=0.50) differs from C1 | The v_hat/alpha=0.50 null did not replicate — escalate, re-register the whole boundary before any cone-vs-line claim |
| (a) CONE-WINS | cone (angular+control) OR non-upper radial set OR offset rescues | Withdraw the blanket I1 null → geometry-conditional claim |
| (b) LINE-WINS | cone corrupts OR upper radial set | I1 line interpretation strengthened; rho=30° cone killed |
| (c) NEITHER | flat zero | rho=30° unconditional cone + alpha=1.0 offset killed; other radii / gated / conditional variants survive |

## 5. Notebook cell block (copy-paste)

```python
# EXP077: cone-vs-line geometry (pre-registered; SIGNED 2026-09-23)
!pip install -q -r /kaggle/input/<your-dataset-slug>/exp077/requirements.txt
import os, zipfile
zipfile.ZipFile("/kaggle/input/<your-dataset-slug>/exp077_bundle.zip").extractall("/kaggle/working")
os.chdir("/kaggle/working")
!python3 exp077/run_exp077.py
```

Replace `<your-dataset-slug>` with the dataset path shown in the notebook's data panel.
Outputs land in `experiments/runs/EXP077_cone_vs_line/`. When the cell finishes,
download the four files listed in §3 and run `evaluate_exp077.py`.

## 6. Safety / guard notes (read before launching)

- **Never re-run under EXP077 after a design change.** Entity substitutions, new seeds, different rho/alpha grids, or a better probe all require a NEW pre-registered experiment number (Law #4).
- **Halts are results.** If the run prints `HALT_* — THIS IS THE RESULT`, that halt IS the reportable outcome (branch (d)); do not "fix and re-run" silently.
- **Do not commit, push, or PR anything.** Repository ownership is unverified; all results stay local until the user directs otherwise.
- The registered SHA-256 sanity value comes from EXP067 §2; a mismatch warning is NON-FATAL — the binding guard is the runtime pre/post match.
- Frozen-backbone (`Δθ = 0`) is enforced by the pre/post hash match; a mismatch is a CRITICAL FATAL, not a result.
