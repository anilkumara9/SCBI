# EXP079 UNTESTED ASSUMPTIONS

Assumptions that could not be tested on the CPU-only build machine. The GPU
run must watch for these; any violation is data, not a bug to silently fix.

## Tested locally (CPU smoke)
- `py_compile` clean on all three scripts.
- Full evaluator branch suite passes: **27/27 tests** (all 9 branches,
  (f)/(c2*) and (f)/(e) co-fire precedence, exact p=0.05 and +12pp boundaries,
  the historical EXP065 falling-through cell, null-bar N=50/N=60/monotonicity).
- Calibrated H_sel null bar: N=60 → 0.150, N=50 → 0.160 (seed 7979, 100k
  draws) — reproduces the spec's [FACT — computed] exactly.
- Tokenizer guard (F2-style, hard halt): all 10 test entities single-token
  under the real pythia-160m tokenizer. Support-entity token audit logged:
  **11 of the 25 inherited EXP070 support names are 2-token** (Caleb, Miriam,
  Reuben, Hector, Nestor, Priam, Lucius, Titus, Silas, Sora, Leila) — probe
  correctness uses first-token matching, exactly EXP070's method; disclosed
  in the run log, not a silent truncation. Substitution would change the
  signed support construction (Law #4) and was NOT done.
- Model load (CPU float32), param_hash determinism.
- Support metadata: 5 vocabs × 30 pairs; even/odd split → BUILD=75,
  HELDOUT=75, disjoint.
- Probe map under the faithful (hop, index-pattern) key (EXP070's key;
  reversal flag not part of it): **N_final = 26 < 50** (4+9 survivors per
  domain) → the pre-registered **HALT_PROBE** gate fires. Probe-size range
  0–10 (the 15-item cap never binds).
- All three disjointness assertions (probe∩test, support∩test, probe∩BUILD).
- Halt payload → evaluator → branch (a) VERBATIM path.
- Full compute_delta_h on CPU (150 pairs × 2 forwards): shapes 5×[30,768],
  finite, nonzero.
- build_pool on the real Δh: 17 unit vectors; G2-ring parent-cosine mean
  ≈0.34 (spec §3.1 E[cos]≈0.34 reproduced); 8 G1 + 8 ring + BUILD B_agg.
- Intervention hook mechanics (one steered CPU forward, LOG-116 device
  pattern).
- Oracle selection rule unit check (correctness-rate argmax, seeded
  tie-break among top-tied only).
- Pilot degeneracy rule (R3) unit check (4/5 tied → halt; 0/5 → pass).

## NOT tested locally
- GPU forward passes (hook injection at layer 10 on CUDA, 2×T4).
- Wall-clock on GPU (budget ceiling 15,720 passes; actual will be far lower
  if the N_final gate fires).
- `torch.use_deterministic_algorithms(True)` on CUDA (falls back to a logged
  warning if unsupported — not fatal).
- The 5-instance pilot and everything downstream of it (unreachable: the
  pre-registered N_final gate fires first — see below).
- The full probe + C1..C7 + calibrated-gate path (same reason).

## Protocol executability (flagged for the Law #14 bundle review)

**[OBSERVATION]** Under the signed spec's exact construction — 5-vocabulary
support (EXP070's, mandated verbatim), even/odd index split, (hop,
index-pattern) probe key (EXP070's key, reversal not part of it) — the
HELDOUT match counts per (hop, pattern) are 0, 5, or 10 (5 vocabs × 0–2 odd
indices per pattern; the 15-item cap never binds). With the N_PROBE_MIN=8
cutoff, **26/60 test instances qualify → N_final = 26 < 50 → the N_final
gate HALTs the run by design** (protocol §3.2, §5; evaluator branch (a)).

This is a faithful implementation of the signed spec — not a builder error.
The Law #14 pre-registration review (LOG-120) verified the null bar, the
budget arithmetic, and the deltas, but did **not** independently compute
N_final under the (hop, index-pattern) key; the budget's "17×15×60" line
assumes 60 surviving instances, which the signed matching rule does not
deliver. The bundle review must decide: (a) accept the HALT_PROBE outcome as
the run's reportable result (branch (a)); or (b) kick back for
re-registration with a feasible probe rule (e.g., hop-only matching, or a
stratified split preserving per-pattern coverage) — which per Law #4 takes a
new experiment number or a signed addendum, never a silent edit. The builder
did not alter matching, split rules, or thresholds.

## Conservative readings adopted (documented, not improvised)
1. **R1 — oracle selection score = mean binary correctness** over probe items
   (spec §3.3: r(B;q) = 1[correct on q]; "unchanged from EXP070 §3.3", whose
   code implements correctness-rate argmax — not probability margin). The
   "probe margin" in diagnostic (ii) is winner_rate − B_agg_rate
   (correctness rates), per §6. The pilot/selection code paths were
   unit-tested; the GPU probe phase itself was not.
2. **R2 — G1 bootstrap = 15-with-replacement per vocabulary** over that
   vocab's 15 BUILD (even-indexed) Δh (EXP070's 30-from-30 analog);
   Dirichlet(1×5) over the 5 vocabularies (seeds 7001/7002). Verified
   structurally on CPU (pool builds, norms, ring-cosine).
3. **R3 — pilot degeneracy HALT operationalization** (§9: "if the pilot
   reproduces EXP070's degeneracy, HALT"): tie_rate = fraction of the 5
   pilot instances with a tied oracle argmax (n_tied > 1);
   HALT_DEGENERACY iff tie_rate ≥ 4/5. (EXP070's degeneracy was near-ceiling
   ties making the seeded tie-break the effective selector; §9 EXPECTS
   "ties rare".) Unit-tested with synthetic records; never exercised on GPU.
4. **R4 — B_star excludes the B_agg incumbent** from the "best single
   BUILD-only candidate direction" argmax (B_agg is an aggregate, not a
   single candidate direction).
5. **Probe-key reading:** (hop, index-pattern), reversal flag NOT part of the
   key — exactly EXP070's probe key (`s["hop"] == sig["hop"] and
   tuple(s["pattern"]) == tuple(sig["pattern"])`). Including reversal would
   give N_final ≤ 30 (support has no reversed prompts); the builder kept
   EXP070's key.
6. **Support-entity tokenization:** 11/25 support names are 2-token; probe
   correctness uses first-token matching = EXP070's method, disclosed in the
   run log (Law #13). Not "fixed" — fixing would change the signed
   construction.

## Known debts (from the spec, not the builder)
- A-split-representativeness: even/odd indices assumed exchangeable within
  each vocabulary (spec §7 — stated debt).
- A-pool: the kill is licensed only within the pre-registered search family
  (spec §7).
- H_sel null exchangeability idealization (spec §0 [LIMITATION]): G1
  span-sharing may push the (iii)-path false-pass rate above nominal 5%.
- Winner's curse on ~10 noisy probe items (spec §3.5(3)): attenuated vs
  EXP070 but present; direction of risk is kill-easier.
- The pre-registration review did not verify probe feasibility (N_final);
  the bundle review should treat the §"Protocol executability" observation
  above as a first-class finding.
