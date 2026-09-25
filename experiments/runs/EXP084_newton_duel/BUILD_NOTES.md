# EXP084 BUILD NOTES — LOG-265, repaired per LOG-266 (LOG-267), stage-2
model loop per LOG-268, stage-2 Law #14 review per LOG-269 (LOG-270 fixes)

Bundle built 2026-09-24 on the CPU build machine (Python 3.12.3, no torch,
no scipy, no numpy for RNG). GPU-node code paths (torch, transformers,
model weights) are present but UNEXECUTED — the runner refuses execution
without CEO GPU clearance (signed §9, §12).

## 0B. LOG-270 — LOG-269 stage-2 review fixes (SIGN-WITH-FIXES repair)

$0, CPU only, no weights touched, no signed artifacts edited.

- **F1 [D2 binding — first-run archive]:** `check_identity` no longer
  archives-and-continues on the first run (that made binding §7 INVALID(ii)
  a self-certifying guard on the single planned run). First run now archives
  M0 then raises the dedicated `BaselinePrepassHalt` — a verdict-clean
  pre-pass halt (NOT InvalidRunError; nothing is invalid): no scientific
  arms, no verdict. The re-run replays the archive and enforces INVALID(ii)
  bit-for-bit. `cmd_run` catches `BaselinePrepassHalt` separately and
  prints the re-run directive ("Re-run the same command for the full
  loop..."). Cost: one extra ~72 fwd-equiv P0 session (24 fwd + 24 bwd),
  outside the 240/72 per-run budget.
- **F2 [GPU-blocking path bug]:** `RECORDS_REL` in `run_exp084.py` was
  `("..", "..", "EXP077_cone_vs_line", ...)` — two levels up, resolving to
  the nonexistent `experiments/EXP077_cone_vs_line/...`; every GPU run
  would loud-halt at Phase 1. Fixed to one level up
  (`experiments/runs/EXP077_cone_vs_line/`, where the pinned archive lives —
  confirmed on disk). The suite stayed green because the prior test used
  the correct path explicitly and never exercised the default (the
  untested-default class of bug).
- **M1:** BUILD_NOTES §0A/§4 mock-harness counts were stale ("12/12") —
  the harness runs 8 scenario runs / 15 checks at LOG-269, now 17/17 checks
  (4 baseline checks replacing 2, per F1). Smoke updated accordingly.
- **M2:** `exp084_statistics.py` module + function docstrings no longer
  say "zero differences are dropped" — the binding LOG-266 behavior is
  loud-halt via `assert_testable_differences` before anything reaches the
  Wilcoxon/HL internals (the drop path is defense-in-depth for direct
  callers only).
- **New tests (8):** first-run archives + halts verdict-clean
  (BaselinePrepassHalt); pre-pass halt is not INVALID; archive written and
  bit-exact; re-run replays without halt; re-run mismatch → INVALID(ii);
  DEFAULT `RECORDS_REL` resolves to the pinned archive on disk (F2
  regression); DEFAULT `RECORDS_REL` SHA == R5d pin. Evaluator suite now
  74/74; mock harness 17/17; smoke green.
- **Signed protocol untouched:** `experiments/protocols/
  EXP084_R2_NEWTON_DUEL_PREREG_SIGNED.md` was NOT edited. D1 (inexecutable
  §2 clause) and D2 (first-run case unspecified) were resolved as binding
  stage-2 interpretations per LOG-269, not protocol edits.
- **`--stage2-review-signoff` NOT cleared by this repair.** LOG-269 makes
  the flag eligible for CEO GPU clearance only after the fixes are applied,
  the suite re-run green, AND the fixes independently re-verified by the
  Law #14 reviewer. This repair agent does not self-clear; the independent
  re-verification is the remaining gate (queue order K2 → EXP083 → EXP084
  unchanged).

## 0A. LOG-268 — model-loop construction (stage-2 implementation)

The stage-2 model loop called out as "NOT in this bundle" in §0 is now
built in `run_exp084.py` (CPU-constructed; GPU node still dark). Evaluator
suite 74/74 green (was 66/66 at LOG-269; +8 targeted tests per LOG-270);
smoke PASS (40 checks: 23 prior + 17 mock-harness). No signed artifacts
edited. No model weights downloaded; no GPU passes executed; no torch
imported on the build machine.

**Architecture.** `run_full_loop(backend, budget, out_dir, log, ...)` is
backend-neutral: the CPU mock harness drives it with synthetic activation
landscapes; the GPU node drives it with `TorchBackend` (torch-only, raises
without torch). `PassBudget` (240 fwd / 72 bwd hard ceiling; 241st fwd /
73rd bwd → RuntimeError) is threaded through every forward/backward call
site, including P0, probes, all five arms, and the permuted arm.

**Ordering (§7 / §8 / §12 binding).** INVALID(i) SHA-256 state-hash preflight
(tensor-bytes-only convention, sorted float32 — matches the EXP077
historical implementation) runs before any pass; P0 identity replay runs
next (fresh-archive creation is NOT permitted — see defect D2 below);
INVALID(iii) (<12/24 defined → UNDEFINED-LANDSCAPE) short-circuits before
any contrast; the F2 apparatus-sensitivity precondition short-circuits to
INVALID/UNINFORMATIVE-PROXY before the scientific contrasts (its §7
precedence); `require_spearman_table(n_defined)` gates conjunct (e) before
any verdict machinery. Arm (d) uses the signed 3-forward/2-backward
interpretation (step 1 reuses sunk g₀; forward+gradient at p₁, p₂; final
forward at p₃); the natural Newton step norm ‖g‖/|κ̂_dir| is recorded
uncapped (F1 repair (a)).

**Statistics hardening (LOG-266 binding).** New `NonTestableDataError`
(ValeError subclass): `assert_testable_differences` loud-halts on exact
zero diffs and on ties in |d_i| (never silently drops, never tie-breaks);
`assert_no_ties` guards exact-Spearman inputs; deterministic `median()`.
All contrast inputs are pre-validated before the exact Wilcoxon/HL/Spearman
calls. F2 short-circuit added: on a dead apparatus the duel rows are not
computed at all (their tie-halts cannot preempt the INVALID(iv) verdict).

**Mock harness** (`mock_harness.py`, zero torch / zero model passes):
17/17 checks pass (8 scenario runs) through the full orchestration —
CONTINUE, KILL (flagship, cost-fair), INVALID/UNINFORMATIVE-PROXY,
INVALID/UNDEFINED-LANDSCAPE, tie loud-halt, missing-table loud-halt,
INVALID(i) tamper, baseline first-run archive + verdict-clean halt
(BaselinePrepassHalt) + identical-rerun replay + shifted-rerun
INVALID(ii) (LOG-269 D2 binding, LOG-270), and exact pass accounting
(continue: fwd=228 = 24×8 + 18 Newton + 18 permuted-eval; bwd=72;
n_e_contrast=13 paired vs n_e_evaluated=18 arm spend — see D3).
The mock's LCG/Box-Muller/Fisher-Yates fixtures are wiring-only and never
claim protocol-RNG status (torch-exclusive on the GPU node).

**CLI.** `--smoke` (0 model passes); `--run` requires BOTH
`--ceo-gpu-clearance` AND `--stage2-review-signoff` (refuses with exit 2
otherwise; verified).

**Defects D1–D5 — adjudicated by the stage-2 Law #14 review (LOG-269,
binding; see §0B for the LOG-270 repairs):**
- **D1 (probe-set source) — LICENSED as a binding stage-2 interpretation
  (no new experiment number; no signed-file edit).** The signed §2 clause
  "items 0–23 in archived order" is inexecutable as written (the pinned
  archive carries no prompt strings/options/token IDs/margins, and its
  entity-grouped order matches no in-repo builder — 6/24, 12/60 alignment).
  Binding reading: verbatim EXP077 §3 rebuild, fixed indices 0–23 —
  outcome-independent (EXP077 was a null; margins were never its endpoint).
  The deviation is loudly logged by `load_probe_set` and manifest-recorded
  in every run record (`probe_set`: records_sha256, alignment_24,
  alignment_60 — see `finish_run`). Any paper/scoreboard use of EXP084 must
  carry the deviation note. Zero delta to hypotheses, endpoints, arms,
  statistics, verdict rows, or thresholds.
- **D2 (P0 baseline) — RESOLVED by LOG-270 F1.** The first run archives M0
  then raises `BaselinePrepassHalt` (verdict-clean pre-pass halt — NOT
  InvalidRunError; nothing is invalid): no scientific arms, no verdict.
  The re-run replays the archive and enforces §7 INVALID(ii) bit-for-bit.
  The archive-and-continue self-certifying guard is gone.
- **D3 (undefined permuted donors) — acceptable deviation, NOT a protocol
  breach.** Pairwise deletion in contrast (d) deletes on a pre-treatment
  covariate (donor κ̂_dir), never on outcomes; non-gameable. Documented in
  code and recorded in the manifest (`n_e_contrast` vs `n_e_evaluated`).
- **D4 (P0-before-science ordering) — compliant as built, no change.**
  INVALID(ii) fires before any scientific arm (§7 order satisfied); the
  per-item g₀ readouts are P0-identity-arm construction (sunk/shared per
  §4/R5c), not scientific arms. Graphs are freed per item; only detached
  1024-vectors are retained. No T4 memory issue.
- **D5 (activation-leaf gradient) — accepted as a flagged residual risk;
  no code change.** The sketched construction (`torch.autograd.grad` on the
  hook-captured activation under `enable_grad`, all params
  `requires_grad_(False)`) is the standard correct construction; zero
  gradient → `ApparatusError` (loud); wrong-site/degenerate gradients →
  F2 check fails → INVALID/UNINFORMATIVE-PROXY, never a verdict.
  **Binding monitor:** per-item ‖g₀‖ is already logged
  (`[P0] item {i}: M0=… ‖g0‖=…`) — the first GPU run's log MUST be
  inspected for sane, nonzero ‖g₀‖ norms before any verdict is treated
  as final.

## 0. LOG-267 repairs (Law #14 bundle review LOG-266: SIGN-WITH-FIXES)

All three required fixes applied; evaluator suite now 49/49 green (was
37/37); smoke PASS. No signed artifacts edited.

- **Fix 1 (KILL-prong correctness):** `hodges_lehmann_ci` in
  `exp084_statistics.py` returned `[walsh[c+1], walsh[m-c-2]]` — one order
  statistic too narrow per side, contradicting its own docstring and making
  the KILL effect prong (HL upper < 0.01) fire too easily (anti-fail-safe).
  Now returns the exact test-inversion endpoints `[walsh[c], walsh[m-c-1]]`
  (degenerate guard: c == -1 → [walsh[0], walsh[m-1]]). Index audit of the
  whole module found no other off-by-one of this class (Wilcoxon ranks are
  correctly 1-indexed; Walsh-median is standard). New evaluator test
  ("HL: endpoints match exact test-inversion") compares against an
  independent exact test-inversion on a fixed n=8 fixture where the
  off-by-one changes both endpoints; empirically verified it FAILS on the
  old indices and passes on the fix.
- **Fix 2 (verdict-table completeness):** `adjudicate()` in `run_exp084.py`
  now evaluates the §7 "KILL (directional, narrow)" row at its §7 row
  position (after flagship KILL, before HELD(straddle)). The results dict is
  extended with the binding keys `median_b_minus_a` / `hl_hi_b_minus_a`
  (missing keys fail loud via KeyError at that row position). Returns
  (verdict, evidentiary, detail, secondary); secondary is None or
  {"verdict": "KILL(directional, narrow)", "evidentiary": "Not supported",
  "detail": ...}. The narrow row never replaces the primary verdict.
  INVALID rows preempt (no secondary). New tests: fires alongside
  HELD(straddle); silent when criteria fail; does not shadow flagship
  KILL; disjoint from CONTINUE conjunct (c) by §7 precedence position.
  Also per LOG-266 M3: the INVALID(iii) detail string now cites the
  definedness inequality (κ̂_dir < −κ_floor) for traceability.
- **Fix 3 (n≥20 table gate):** new `require_spearman_table(n)` in
  `exp084_spearman.py` + `MissingSpearmanTableError` (a loud FileNotFoundError
  subclass). Missing/corrupt table → loud halt naming the GPU-node NTT+Ryser
  build path and the exact build command; NO verdict is emitted (not
  INVALID, not HELD — the signed protocol has no missing-table row;
  Law #4-clean per LOG-266). Binding pre-execution condition: the stage-2
  model loop must call this at startup for the defined-set size BEFORE any
  verdict machinery. New evaluator tests cover the gate (n=12 passes,
  n=20/21 raise loudly, message names the GPU path, exact-p path halts too).
- **GPU table builder:** new `tools/build_spearman_tables_gpu.py`
  (NTT+Ryser, torch; see §1). Validated on the CPU build machine:
  `--selftest` (full pipeline vs itertools brute force, n=1..8) PASS;
  n=12 output bit-identical to the independently C-built table.
- **Minor (LOG-266 M1/M2/M3):** smoke docstring now says n=12..19 (was
  12..24); `build_spearman_tables.py` docstring corrected (D-chunking does
  NOT fit n≥20; n≥20 is GPU-node only); §1/§4/§5.1 contradiction below
  reconciled toward §1 (no background generation exists or is claimed).
- **Stage-2 gate (NOT in this bundle):** the model loop is still unbuilt
  (`main()` raises by design). CEO GPU clearance additionally requires the
  Law #14 stage-2 review of the unbuilt loop: INVALID(i) SHA-256 pre/post +
  pinned `4c242d…dd` and INVALID(ii) P0 identity checked BEFORE (iii)/(iv);
  no-tie assertion before exact Wilcoxon/HL/Spearman calls; PassBudget wired
  into every forward/backward call; torch RNG + derangement + greedy
  determinism on the GPU node; `require_spearman_table(n_defined)` at
  startup. None of this is licensed by the current bundle.

## 1. Exact Spearman null tables (LOG-264 requirement)

**Requirement:** The dose-response conjunct (e) (§5) requires Spearman
(|κ̂_dir|, ΔM_b − ΔM_d) over the defined set with a **TRUE EXACT**
permutation p-value — deterministic full null enumeration, NOT Monte Carlo.

**Method:** `tools/gen_spearman_null.c` implements the subset DP over
bitmasks (2^n states), layer-by-layer by popcount. `dp[mask][d]` counts
injective assignments of positions 1..popcount(mask) to the values in
`mask` with partial Σ(i−π_i)² == d. Counts are `unsigned __int128`
(exact; n! ≤ 24! < 2^79). The D_max_partial(m) cap keeps early layers small.
A data race in the first version (parallel source masks writing the same
dest) was found by the n=8 brute-force cross-check and fixed by
parallelizing over dest masks instead.

**Verification:**
- n ≤ 8: matches `itertools.permutations` brute force exactly.
- All n: sum == n!; symmetry count[d] == count[Dmax−d]; odd D counts == 0
  (D is always even: D = Σ(i−π_i)² ≡ Σ(i−π_i) = 0 mod 2).
- Tables generated by `tools/build_spearman_tables.py`; only d ≤ Dmax/2
  computed directly, mirrored via symmetry.

**Scalability:** 2^24 × Dmax(24)=4600 is #P-complete (no sub-exponential
exact algorithm exists). The build machine (2 cores, ~4.7GB RAM) uses
D-chunking for n ≥ 20 (chunk sized to ~1GB peak). n=20 hit the OOM killer
at 2GB target; 1GB target succeeds for n ≤ 19.

**GAP (n=20..24) — RESOLVED PATH (LOG-267):** The D-chunking approach does NOT
reduce peak memory — each chunk with d_hi still requires O(2^n × d_hi) memory
(the DP must track [0, d_hi] because shifts move counts upward). For n=20,
d_hi=1330 needs 7.8GB; for n=24, d_hi=2300 needs 199GB. Both exceed
build-machine RAM. Tables n=1..19 are complete and verified. Tables n=20..24
are NOT precomputed and are NOT being generated in the background (the §4/§5.1
"background generation" notes were stale and are retracted here).

**Path forward (binding pre-execution condition, LOG-266 Fix 3):** tables
n=20..24 MUST be built on the GPU node via the NTT+Ryser path implemented in
`tools/build_spearman_tables_gpu.py` (in this bundle) and pass the same
integrity checks (sum = n!, D=0 count = 1 ↔ identity, symmetry
count[d] = count[Dmax−d], odd D = 0) BEFORE any EXP084 execution — they are
build artifacts; the GPU node does lookup only. Algorithm: Ryser permanent
of A[i][j] = u^{ij} evaluated at 4096th roots of unity in F_p, tiled in
torch int64 (exact: all products < p² < 2^63), one inverse NTT per prime,
CRT over p1=998244353, p2=1004535809, p3=104857601 (product > 24!) to exact
integers. Validated on the CPU build machine: `--selftest` matches
itertools brute force for n=1..8, and the n=12 output is bit-identical to
the independently C-built table in `exp084_spearman_tables/`.

Kaggle-side command (run from the EXP084_newton_duel bundle directory on
the GPU node; requires torch+CUDA; minutes on a T4):
    !python3 tools/build_spearman_tables_gpu.py --n 20 21 22 23 24 --out exp084_spearman_tables/

If the defined set lands at n ≥ 20 without tables, the runner LOUD-HALTS via
`require_spearman_table()` (`MissingSpearmanTableError`, naming the command
above) — no verdict, no CONTINUE, no KILL, no HELD (verdict-clean; the
earlier "return INCONCLUSIVE" note is superseded by LOG-266: the signed
protocol has no missing-table row, so no scientific verdict may be emitted).

**CPU-only precedent:** Per EXP083, tables are build artifacts; the GPU
node does table lookup only (no recomputation).

## 2. Statistics modules

- `exp084_guards.py`: κ̂_dir < −κ_floor definedness (§3, LOG-264 Fix 1
  verbatim); exclusion split convex-uphill (κ̂_dir ≥ +κ_floor) vs too-flat
  (−κ_floor ≤ κ̂_dir < +κ_floor) (LOG-264 Fix 2 verbatim); INVALID(iii)
  at <12/24; natural step length ‖g‖/|κ̂_dir| (no cap, F1 repair (a)).
- `exp084_statistics.py`: exact one-sided Wilcoxon signed-rank via DP over
  the signed-rank null (not normal approx); Hodges-Lehmann 95% CI via
  exact critical values — exact test-inversion endpoints `[walsh[c],
  walsh[m-c-1]]` (LOG-267 Fix 1; the off-by-one `[walsh[c+1], walsh[m-c-2]]`
  is repaired and regression-tested); KILL effect prong (HL upper < 0.01,
  F10). LOG-268: `NonTestableDataError` (ValueError subclass) —
  `assert_testable_differences` loud-halts on exact zero diffs and on ties
  in |d_i| (never silently drops, never tie-breaks; LOG-266 binding);
  `assert_no_ties` guards exact-Spearman inputs; deterministic `median()`.
  n_eff < 6 raises (not decision-relevant at pre-registered bars).
- `exp084_spearman.py`: Spearman rho + exact one-sided p = P_null(D ≤ d_obs)
  via table lookup. Ties raise ValueError (exact D-distribution assumes
  untied ranks; protocol uses continuous values).
  `require_spearman_table(n)` is the binding pre-execution gate (LOG-267
  Fix 3): missing/corrupt table → `MissingSpearmanTableError` loud halt
  naming the GPU-node NTT+Ryser build command; no verdict emitted.
- `exp084_rng.py`: torch-exclusive (no numpy import; asserted in tests).
  Master 20260924, per-item 20260924+i, fixed derangement for arm (e).
  `generate_r_hat` / `derangement` raise RuntimeError without torch (GPU-only).

## 3. Runner and verdict logic

- `run_exp084.py`: five arms (§4), PassBudget hard ceiling (240 fwd + 72 bwd
  = 384 fwd-equiv; pass 241 / bwd 73 REFUSED via RuntimeError), §7 verdict
  precedence (INVALID → sensitivity → CONTINUE → HELD(win-not-curv) →
  HELD(step-noise) → KILL → narrow-KILL (secondary) → HELD(straddle)).
  `adjudicate()` returns (verdict, evidentiary, detail, secondary) with the
  §7 narrow-KILL row wired at its row position (LOG-267 Fix 2). LOG-268:
  full stage-2 model loop as backend-neutral `run_full_loop()` —
  INVALID(i) SHA-256 preflight (tensor-bytes-only, EXP077 convention),
  P0 identity replay, INVALID(iii) short-circuit, F2 precondition
  short-circuit (INVALID/UNINFORMATIVE-PROXY), `require_spearman_table`
  gate before verdict machinery, arm (d) 3-fwd/2-bwd re-linearized GD,
  guarded natural-length Newton, atomic JSON result write. `main()` CLI:
  `--smoke` (0 model passes); `--run` requires BOTH `--ceo-gpu-clearance`
  AND `--stage2-review-signoff` (exit 2 otherwise).
- Label-free: margin proxy M(h) = z1 − z2 from model's own logits only (§2).

## 4. Tests

- `test_exp084.py`: 74 evaluator tests, all pass (CPU, synthetic fixtures).
  Covers: guards (§3), Wilcoxon exact vs brute force (n=7), HL CI incl.
  exact test-inversion regression test (LOG-267 Fix 1), KILL prong,
  Spearman exact vs brute force (n=6), table integrity (n=12 sums to 12!),
  table-presence gate (LOG-267 Fix 3), RNG contract + torch-exclusivity,
  verdict precedence (§7) incl. narrow-KILL fires/silent/no-shadow/
  disjointness (LOG-267 Fix 2), pass budget ceiling + refusal, runner refusal,
  LOG-268 additions: deterministic median, tie/zero loud-halt taxonomy
  (`NonTestableDataError`), verbatim benchmark rebuild (60 items, item-0
  bit-exact, 6/24 archive alignment recorded), `InvalidRunError` row
  taxonomy, probe-set preflight (records SHA ok, deviation logged, missing
  file halts loud).
- `smoke_test.py`: startup smoke (0 model passes). Verifies imports, signed
  pins, Spearman tables n=12..19 valid, runner refusal, C source present,
  both table-build scripts present (CPU n≤19 + GPU NTT+Ryser n=20..24),
  plus §6: the full `mock_harness.py` end-to-end (17 checks). Tables
  n=20..24 are GPU-node build artifacts and are NOT smoke-checked
  (retracts the stale "still generating in background" note).
- `mock_harness.py`: 17/17 checks (8 scenario runs) through the complete
  `run_full_loop` orchestration on synthetic activation landscapes (zero
  torch, zero model passes): CONTINUE / KILL(flagship, cost-fair) /
  INVALID-UNINFORMATIVE-PROXY / INVALID-UNDEFINED-LANDSCAPE verdicts,
  tie and missing-table loud halts, INVALID(i) tamper, baseline first-run
  archive + verdict-clean halt + identical-rerun replay + shifted
  INVALID(ii) (LOG-269 D2 binding, LOG-270), exact pass accounting
  (fwd=228=24×8+18+18, bwd=72, n_e_contrast=13, n_e_evaluated=18).

## 5. Gaps and limitations (for bundle review)

1. **Tables n=20..24 not precomputed** (no background generation — retracted;
   see §1). GPU-node build: run `tools/build_spearman_tables_gpu.py` per the
   §1 Kaggle command BEFORE any EXP084 execution. The evaluator suite does
   not need n>12 tables (tests use n ≤ 12 fixtures); `require_spearman_table`
   loud-halts on missing tables with the build command.
2. **GPU-node paths untested** (torch absent on build machine): `generate_r_hat`,
   `derangement`, model forward/backward, SHA-256 guard, P0 identity check,
   and the LOG-268 model loop's `TorchBackend` (activation-leaf gradient
   readout D5, stable top-two tie rule, global P0-before-science ordering
   D4). The bundle review must verify these on the GPU node before CEO
   clearance.
3. **Wilcoxon/HL tie-handling:** exact methods raise on ties; the protocol
   does not specify tie-breaking. Continuous margin gains make ties
   measure-zero; the runner now asserts no-ties / no-zeros loudly before
   testing (`NonTestableDataError`, LOG-268).
4. **No second-δ replication** for κ̂_dir (protocol §3: explicitly declined;
   too-noisy marked UNDETERMINED per §7 attribution rule).
5. **Stage-2 Law #14 review items (LOG-268 defects D1–D5, §0A):** probe-set
   source mapping (D1), first-run P0 baseline archive licensing (D2),
   undefined permuted-donor pairwise deletion (D3), global P0-before-
   science graph retention (D4), activation-leaf gradient + deterministic
   top-two (D5). None silently resolved; all flagged for review.

## 6. Reproducibility

- Deterministic: torch-exclusive seeds, greedy decoding, fixed derangement.
- C generator: `gcc -O3 -fopenmp` (OpenMP optional; serial also correct).
- Tables are JSON with full integer counts (no float rounding).
- Signed protocol: `experiments/protocols/EXP084_R2_NEWTON_DUEL_PREREG_SIGNED.md`
  (LOG-264 fixes applied verbatim; DRAFT untouched).
