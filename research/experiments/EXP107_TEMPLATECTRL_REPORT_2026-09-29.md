# EXP107 execution report — template-control kill-test of the EXP106 transfer reading

**Date:** 2026-09-29
**Lane:** LOG-4540 (execution, CEO-launched LOG-4539)
**Pre-registration:** `research/prereg/EXP_PREREG_EXP107_TEMPLATECTRL_2026-09-29.md`
(independent Law #14 review SIGN via LOG-4536 → repairs LOG-4537 → fix-verification
ALL-FIXES-VERIFIED LOG-4538)
**Status:** executed exactly per pre-registration. No signed protocol, paper source,
or GPU-queue artifact touched. $0 compute.

---

## 1. Environment [FACT]

| Component | Value |
|---|---|
| torch | 2.14.0+cpu |
| transformers | 5.17.0 |
| numpy | 2.5.3 |
| sklearn | 1.9.1 |
| venv | `~/workspace/.venv-exp077` (EXP106 environment; version pins identical to the registered `~/.venv-exp077`) |
| Backbone snapshot | `~/workspace/.exp086_weights/pythia-410m` |
| Read site | hidden_states[20], final token `[0, -1, :]`, float32, CPU |
| Head | `LogisticRegression(penalty='l2', C=1.0)`, all other params default; fit `n_iter_=[18]` (identical to EXP106's fit) |

## 2. Precondition checks (all must pass before the metric is admissible) [OBSERVATION]

| Check | Expected | Observed | Status |
|---|---|---|---|
| Reuse-integrity: embeddings-array SHA-256 | `4e6229bea083570f17e3368326d9848c9a8db5dc25c7efc75f0e1a2960b5683c` | exact match | PASS |
| Reuse-integrity: ids-array SHA-256 | `4668fc45716d46b408c778c93d2d844ad9b2c5bafb33458ec30a4b673ed44474` | exact match | PASS |
| Decorrelated-bench pin (canonical JSON SHA-256) | `e91b302f41f641c74e56957e526efcd4866bac62d134e157defe0a4cdd49e4f5` | exact match | PASS |
| Bench cells | 4 × 15 (phrasing × template word-family) | `A-first/original 15, A-first/flipped 15, C-first/original 15, C-first/flipped 15` | PASS |
| Item-ID overlap tripwire train/test | 0 | 0 | PASS |
| Backbone hash pre-extraction | `ec276abe…e0ed` | match | PASS |
| Backbone hash mid / post / final | `ec276abe…e0ed` (Δθ=0) | match ×3 | PASS |
| Pipeline-continuity sanity gate (retrain head in EXP106 env, score original EXP091 bench rebuilt verbatim via `build_test_premises`) | 60/60 | **60/60** | PASS |
| Block-off: determinism pass1 == pass2 | bit-identical | True | PASS |
| Block-off: scored embeddings byte-identical to fresh backbone-only pass | bit-identical | True (`sha 9b6e8afb…` all three) | PASS |

No precondition failed. No RUN-INVALID. The verdict below is admissible.

## 3. Primary metric [OBSERVATION]

**Decorrelated-bench accuracy: 34/60 = 0.5667.**

One-sided binomial p vs chance (0.5): **p = 0.1831** (P(X ≥ 34 | n=60, p=0.5)).

### Per-cell breakdown (4 × 15)

| Cell | Score |
|---|---|
| A-first / original-words | 15/15 |
| A-first / flipped-words | 4/15 |
| C-first / original-words | 15/15 |
| C-first / flipped-words | 0/15 |

**Original-word cells: 30/30. Flipped-word cells: 4/30.**

[INTERPRETATION — non-binding, per pre-reg §5:] the cell signature is the
registered template-detector signature (original-cells high, flipped-cells ~0):
the head's 60/60 on the template-correlated bench did not survive
meaning-preserving template decorrelation. The 4/15 (vs 0/15) asymmetry in the
flipped cells is within the registered ±5 embedding-shift noise absorbed by the
KILL bar; it moves nothing about the decision.

## 4. Verdict — in the pre-registration's exact language [OBSERVATION]

> **≤ 35/60 → KILL the EXP106 transfer reading.** The 60/60 was pure template
> artifact. The GPU proposal licensed by EXP106's CONTINUE is **VOID**; any new
> GPU proposal must be re-licensed against a template-decorrelated design. No
> rescue runs.

**Score 34/60 ≤ 35/60 → KILL.**

Falsification-tree branch taken: "≤ 35/60 → KILL — The EXP106 transfer reading
is dead — pure template artifact. EXP106's GPU proposal license is VOID."

### What this verdict licenses and voids [FACT, per pre-reg §2/§4/§7]

- **Killed:** the EXP106 transfer reading — "the output-side room has an
  autonomous (non-artifact) instantiation." The 60/60 is established as pure
  surface-template detection, not a target-position readout.
- **Voided:** the GPU head-training proposal licensed by EXP106's CONTINUE.
  Any new GPU proposal must be re-licensed against a template-decorrelated
  design (founder-gated; no execution licensed).
- **Not re-litigated:** EXP106's registered CONTINUE verdict stands as
  registered — its decision bars were binding; this experiment tested the
  *reading* of that verdict, not the verdict.
- **Not claimed:** no generality beyond this bench; no claim about what
  surface cue the head used — per the registered caveat, a collapsed score
  kills the transfer reading under *either* a word-template or a
  subject-position cue, and this test does not distinguish them.
- No re-run, no larger-n rescue (unlicensed — barred).

## 5. Artifacts [FACT]

- Executor: `experiments/runs/EXP107_templatectrl/run_exp107.py` (LOG-4540)
- Raw logs: `experiments/runs/EXP107_templatectrl/out/exp107_execution_log.txt`
- Scored embeddings: `experiments/runs/EXP107_templatectrl/out/exp107_test_embeddings.npz`
- Per-item records: `experiments/runs/EXP107_templatectrl/out/exp107_per_item.json`
- Result JSON: `experiments/runs/EXP107_templatectrl/out/exp107_result.json`
- Bench builder (unchanged): `experiments/runs/EXP107_templatectrl/build_exp107_bench.py`

**Lane stops here.** No follow-ups dispatched (barred). Independent review of
this execution is a separate lane, not this lane's work.
