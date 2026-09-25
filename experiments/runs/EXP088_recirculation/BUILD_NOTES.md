# EXP088 execution bundle — build notes

**Experiment:** EXP088 (recirculation belief-state transfer)
**Signed protocol:** `experiments/protocols/EXP088_RECIRCULATION_PREREG_SIGNED.md` (IMMUTABLE — untouched by this bundle)
**Built:** 2026-09-24 · **Cost:** $0 · **Compute:** CPU only · **Weights touched:** none · **GPU:** dark
**Bundle stage:** ready for independent Law #14 bundle review — NOT self-declared GPU-ready.

The GPU queue remains K2 → EXP083 → EXP084 → EXP086 → EXP088 (no pre-emption).

## What this bundle is

The full EXP088 model loop, built from the signed protocol without editing it:
a deterministic Stage-A (s,d) perplexity screen with the F7 INVALID gate, the
F2 fixed-RAND-vector draw (once per run), the Stage-B three-arm
discrimination (D→S / S→D / RAND) with the F8 ramping schedule, the
DeltaTheta pre/post SHA guard, a hard forward-call budget, and the binding
§G1b/F5 verdict adjudication. Every endpoint is CPU-tested; the model loop
itself is verified end-to-end on a synthetic mock backend (zero weights,
zero torch, zero model passes).

## Files

| File | Role |
|---|---|
| `run_exp088.py` | Model-loop orchestration (`run_full_loop`, backend-neutral) + `TorchBackend` sketch (GPU node) + CLI. `--run` requires BOTH `--ceo-gpu-clearance` AND `--bundle-review-signoff`; otherwise exit 2, no artifact, no log. |
| `exp088_endpoints.py` | Paired 2×2 tables, exact one-sided McNemar, Tango 95% score CI, §G1b mapping (F5), F6 curve classes, F7 gate, verdict adjudication. Pure stdlib. |
| `exp088_ramping.py` | F8 schedule: `alpha_eff(t) = alpha·min(t/10,1)`, 1-indexed positions; schedule id `F8-linear-10`. Pure stdlib. |
| `exp088_rng.py` | Torch-exclusive fixed RNG: `MASTER_SEED = RAND_SEED = 20260924`; `draw_rand_unit_vector` (GPU node only; raises without torch). |
| `exp088_probeset.py` | EXP077 60-item benchmark rebuild (EXP084-D1 convention) + F11 pinned-archive preflight (`RECORDS_SHA256 = 47281cd3…0585`). |
| `stageA_corpus.json` | **Pinned Stage-A corpus artifact** (built 2026-09-24; see below). |
| `tools/build_stageA_corpus.py` | Deterministic corpus builder (re-runnable; re-verifies pins). |
| `test_exp088.py` | Evaluator suite: **24/24 checks pass** (2026-09-24, CPU). |
| `mock_harness.py` | Mock-model end-to-end harness: **22/22 checks pass** (zero model passes). |
| `smoke_test.py` | Startup smoke: **7/7 gates pass** (also via `run_exp088.py --smoke`). |
| `manifest.json` | Bundle manifest (pins, budget, licensed/not-licensed). |
| `requirements.txt` | Pinned build/test dependencies. |

## Stage-A corpus artifact (pinned at build)

- **Source:** `wikitext` / `wikitext-103-raw-v1` / `validation` split
  (`https://huggingface.co/datasets/wikitext/resolve/main/wikitext-103-raw-v1/validation-00000-of-00001.parquet`,
  657,209 bytes, sha256 `204929b7ff9d6184…`; 3,760 rows → 250,011 tokens)
- **Tokenizer:** Pythia-410m `tokenizer.json`
  (`https://huggingface.co/EleutherAI/pythia-410m/resolve/main/tokenizer.json`,
  2,113,710 bytes, sha256 `c24618a1b3e6a381…`)
- **Content:** first 50,000 token ids of the row-ordered token stream
  (exactly 50,000; vocab max id 50,276; all non-negative ints — verified
  independently of the builder)
- **Token-id SHA-256** (comma-joined ASCII ids): `4206c056e87b209c1f47d3230138e5e2ce7b79697a8fa2a03a6a7442ff4bada7`
  — transcribed into `run_exp088.py::CORPUS_TOKEN_IDS_SHA256`; the startup
  preflight refuses to run on any mismatch.
- **Caveat (for the Law #14 review):** Wikitext derives from Wikipedia and is
  *not* held out from Pythia pretraining. It is held out from *this
  experiment* (no overlap with the synthetic Stage-B probe) and is disjoint
  from the discrimination benchmark — the protocol's "held-out" reading the
  bundle implements. Whether that reading is acceptable is the reviewer's
  call; the builder logs the caveat loudly rather than laundering it.

## Budget arithmetic (exact, not estimated)

- Stage A: 20 corpus-passes × 25 blocks = **500** forward calls
  (2 no-recirculation repeats × 25 × 1 call + 9 grid pairs × 25 × 2 calls)
- Stage B: 60 baseline × 1 + 9 arms × 60 × 2 = **1,140** forward calls
- **Total ceiling: 1,640** (`FWD_BUDGET`; `PassBudget` refuses call 1,641)

The signed protocol's "≈450 block-passes / ≈1,590 total" is an estimate; the
bundle implements the exact F7 requirement (two baseline repeats, F8 §5
grid) and records the discrepancy here for the review.

## Verification (all 2026-09-24, CPU, $0)

- `test_exp088.py`: **24/24** — McNemar vs brute-force binomial (300 random
  tables, exact agreement); Tango containment (200 tables), swap-symmetry
  (worst |err| 2.2e-16), degenerate tables, width∝1/√n; §G1b strict
  boundaries at exactly 0.05; F6 five classes; F7 strict->eps, argmax,
  margin, tie→ValueError; all verdict cells + B2 override; probe-set
  rebuild/decision-rule/pinned-archive preflight; F8 schedule + loud
  validation; RNG pins + torch-exclusivity; runner clearance refusal,
  budget ceiling, preflight-before-model-construction, geometry-drift halt.
- `mock_harness.py`: **22/22** — full `run_full_loop` on synthetic fixtures:
  Stage-A INVALID (flat + noise-floor variants), argmax tie loud-halt,
  CONTINUE / KILL×2 / PIVOT×2 / HELD verdict cells, the B4-vs-F5 tension
  cell → HELD (not KILL), DeltaTheta tamper → halt, RAND drawn exactly once
  per run, leak-spec threading (D→S / S→D-swapped / RAND geometries), pinned
  alphas, exact call accounting, the LOG-320 full-scale budget guard (25
  blocks → 1,640 ≤ ceiling), and the per-arm (capture_src, capture_dst,
  hook_layer) leak-layer wiring check.
- `smoke_test.py`: **7/7** — imports without torch; `--run` refusal (exit 2,
  no artifact/log); preflight crash guard on missing corpus; preflight pass
  on pinned artifacts; corpus pin match; evaluator 24/24; harness 22/22.

## Mechanical defects found and repaired during the build

1. S→D leak-spec wiring reversed the source/destination (now: shallow `s=d*`,
   deep destination `d=s*`).
2. Tensor-vs-string alias comparison (now an explicit layer-equality branch).
3. F7 statistic description corrected (LOG-320 F3): the code computes
   mean-over-tokens of per-token perplexity differences (mean of `exp(nll)`
   differences — the protocol's literal "mean perplexity-reduction" reading),
   licensed as implemented; NOT corpus-level PPL `exp(mean nll)`.
   Description fixed; code unchanged; noise floor on the same statistic.
4. Forward budget arithmetic repaired (LOG-320 F2): the ceiling
   undercounted Stage-A corpus passes (19 × 25 instead of the true
   2 repeats × 25 + 9 pairs × 25 × 2 = 500); hard ceiling now 1,640,
   `PassBudget` refuses call 1,641.
5. Stage-A INVALID path wording corrected (LOG-320 F5):
   `write_invalid_record` recomputes the state hash at INVALID-write time
   (post-halt) and records it as both pre/post SHA — the pre-run hash is
   not carried through; frozen weights (Δθ≡0) make the recomputed hash
   identical. Substance unchanged.
6. No startup preflight before weight access (now `_startup_preflight`:
   corpus → records → geometry → out-dir → torch/CUDA, all before
   `TorchBackend` construction; `--run` refuses without it).
7. Git-commit manifest resolved `SCBI/experiments` instead of repo root
   `SCBI` (now ascends to the repo root; verified against `git rev-parse`).

## Protocol tensions carried to the Law #14 review (NOT resolved here)

1. **B4 vs binding F5/§G1b.** Literal B4 ("S→D ≥ D→S → KILL") contradicts the
   binding sub-threshold mapping ("CI reaching 0.05 is held, never culled").
   The bundle implements the binding mapping: primary KILL only when Tango
   U < 0.05; a non-positive point estimate whose CI reaches 0.05 is
   HELD/PIVOT (mock cell `b4_tension` verifies HELD). LOG-320 adjudication
   (a): LICENSED AS IMPLEMENTED — binding F5 (CI reaching 0.05 is held,
   never culled), primary KILL only when Tango U < 0.05.
2. **EXP077 archive carries no prompt strings.** The pinned F11 archive
   describes a different 60-item benchmark (uniform 6/entity, grouped)
   than the §3 builder's (skewed: Mars×21/Iron×21…); the item SETS differ,
   so this is not a reordering and the archive's exact prompts are
   unrecoverable. The bundle's probe is the protocol's licensed fallback —
   "the program's standard probe — decided at build, registered before
   running" (60 fixed synthetic 2/3-hop MCQ items, deterministic,
   outcome-independent, deviation loudly logged). LOG-320 tension ruling
   #2: licensed as implemented via the fallback reading, WITH the
   corrected characterization (F4).
3. **Stage-A "held-out" corpus** (see caveat above). LOG-320 adjudication
   (b): LICENSED AS SPECIFIED — held out from this experiment and disjoint
   from the Stage-B probe; the pretraining-overlap caveat stays.
4. **Cost estimate vs exact F7 rule** (see budget section above).
   LOG-320 tension ruling #4: approach licensed (exact over estimate);
   the ceiling arithmetic repaired to 1,640 (F2).

## Not licensed by this bundle

GPU execution · model weight access · efficacy/capability claims ·
signed-protocol edits · any verdict about the science (no scientific run
has occurred — the verdict cells above are synthetic-fixture checks of the
adjudication logic, not experimental outcomes).
