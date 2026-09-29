# EXP131 RUNBOOK — TGA v₁ Injection Test (pre-registered, founder-run on GPU)

**Protocol (DO NOT MODIFY):** `EXP_PREREG_TGA_V1_INJECTION_2026-09-29.md`
(post-fix SHA-256 `d85205f4ce2b1aadd2b2bda64397f7523e15958cf4fd8d903acccf0fd7f8bf52` —
the executor verifies this at startup and **refuses to run on mismatch**.)
**Runner:** `run_exp131.py`
**Tree unit tests:** `test_decision_tree.py`
**Vendored inputs:** `build_exp107_bench.py` (verbatim EXP107 bench builder),
`exp077_support.py` (verbatim EXP077 support-set constants + B_agg reconstruction).

> **GPU required.** This was built and unit-tested on a CPU-only machine:
> the decision-tree logic tests (11/11) pass and the `--smoke` pipeline
> runs end-to-end locally, but the full run must execute on a GPU
> (Kaggle free T4 or Colab free T4). **No verdict has been produced.**
> This is a steering *test*, not a steering claim — the capability
> scoreboard stays at zero until a bound positive lands.

## What it tests

EXP127 found that Pythia-410m's frozen L20→L24 propagator has a distinguished
leading singular direction v̂₁ (median amplification R = 8.24× over average
random directions). No injection in program history has ever been *along v̂₁*.
This experiment asks, with pre-registered falsification bars:

> Does one-shot injection of a fixed norm-matched perturbation along v̂₁
> (at x_{20,last}) move decisions where matched-norm random directions and
> the dead B_agg control move nothing?

**CONTINUE** (all conjunctive): ĉ ≥ 0.1, median margin-displacement ratio ≥ 2
(v₁ vs best random arm), ΔM_v1 > 0 with one-sided McNemar p ≤ 0.05,
rank trend holds (disp(v̂₁) > disp(v̂₂) > median random on ≥ 8/10 prompts),
ΔM_Bagg = 0.
**KILL**: ĉ < 0.1, or v̂₁ inert, or flat rank trend, or the ≥ 2× bar unmet.
**HELD**: margin gain without flips. **RUN-INVALID**: B_agg moves any decision.

Cost: ~120 injection forwards + ~10 ĉ VJPs + ~800 autograd products (v̂₂
derivation) + 300 support presentations for the B_agg reconstruction —
minutes on a single T4, $0.

## Step 0 — Kaggle account readiness (do this FIRST)

1. Sign in at kaggle.com.
2. **New accounts must verify a phone number before GPUs unlock:**
   account avatar → Settings → Phone verification.
3. In the notebook: right panel → **Accelerator: GPU T4**.
4. Quota is ~30 GPU-hours/week — this run uses well under 1 hour.

(Colab alternative: Runtime → Change runtime type → T4 GPU. Same steps below.)

## Step 1 — Upload the bundle

The execution bundle is the whole `exp131_v1inj/` directory:

- `run_exp131.py` (executor)
- `build_exp107_bench.py` (verbatim bench builder)
- `exp077_support.py` (verbatim EXP077 support machinery)
- `test_decision_tree.py` (tree unit tests)
- `requirements.txt`
- `EXP_PREREG_TGA_V1_INJECTION_2026-09-29.md` (**already vendored —
  verify its SHA-256 matches `d85205f4ce2b1aadd2b2bda64397f7523e15958cf4fd8d903acccf0fd7f8bf52`
  before uploading**)
- `RUNBOOK.md`

**Separately upload** `exp127_vectors.npz` (EXP127's hash-pinned vector
artifact, SHA-256 `9b527c026d0ee307192725429f655e628f403505343dc018de3cfe15db6113dc`)
into the same directory.

Do NOT upload the entire SCBI repo — the bundle is self-contained. It
downloads `EleutherAI/pythia-410m` from Hugging Face at runtime (the
LOG-331 backbone pin verifies the weights before any forward).

## Step 2 — Install and run

```bash
pip install -r requirements.txt
python run_exp131.py
```

Expected runtime: **~10–20 minutes on a T4** (300 support presentations for
the B_agg reconstruction + 120 injection forwards + ~10 ĉ VJPs +
~800 autograd products for the v̂₂ deflated power iteration).

Optional pre-flight (runs the full pipeline on 1 prompt with K=1 random
arm, a few minutes):

```bash
python test_decision_tree.py     # tree-logic tests, CPU-only, no model
python run_exp131.py --smoke     # end-to-end pipeline, model-loaded
```

> **The `--smoke` run is expected to print KILL — and that is NOT the
> experiment's answer.** The 1-prompt/K=1 smoke configuration degenerates
> the ĉ statistic by design (the build lane observed ĉ = 0.0634, under the
> 0.1 bar); the KILL verdict from a smoke run is a branch-exercising
> artifact proving the tree executes end-to-end, not an experiment result.
> **Only the full run's verdict counts.**

## Step 3 — What the output looks like

The executor prints a Law #9-ordered console trace ending with:

```
======================================================================
VERDICT: <CONTINUE | KILL | HELD | RUN-INVALID | APPARATUS-VOID>
reason: <one-line tree reason>
======================================================================
```

Possible halts: exit 42 = protocol/pin guard failure; 43 = B_agg
null-control fired (RUN-INVALID, apparatus drift — **not** a verdict);
44 = apparatus-void (breaking-point miss — hypothesis UNTESTED).

**Where the raw records land** (in `out/`, relative to the bundle dir):

- `exp131_console.log` — append-only console trace (every guard, pin, and
  tree node logged in order)
- `exp131_records.json` + `exp131_records.json.sha256` — the raw-record
  hash-pin: per (item, arm) injection records, ĉ values, re-pin records,
  budget audit, environment manifest — minted **before** any metric
- `exp131_report.json` — verdict + all decision statistics

**Download all of `out/`** and hand it back — the verdict is not official
until the independent review lane binds it.

## Guard rails (what the executor enforces itself)

- Protocol hash refusal gate at startup (mismatch → exit 42, nothing runs).
- LOG-331 backbone parameter hash pinned before the first forward and
  re-pinned after the last.
- v̂₁ re-pin: npz hash + all 10 `v1__<prompt_id>` id alignment; no
  finite-difference reconstruction permitted.
- v̂₂ via the LOG-4714 erratum derivation (K=40, seed pinned);
  |v̂₂ᵀv̂₁| < 1e-6 asserted.
- B_agg re-derived deterministically from the EXP077 archived support set
  (verbatim reconstruction); its reconstruction hash is recorded; the
  B_agg arm must move zero decisions or the run is RUN-INVALID.
- Budget B = 1% of median ‖y_{20,last}‖, recorded before the first
  injection forward; every arm's injected norm audited against B.
- ĉ gate evaluated before any injection forward; no finite-difference
  sensing anywhere (mechanically asserted whitelist: exact JVP/VJP only).
- Δθ=0 by construction: no optimizer, no loss, no backward pass into
  weights; eval mode; `requires_grad=False` on all parameters.
