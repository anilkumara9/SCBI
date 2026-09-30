# Amendment DRAFT B: Breaking point (b) + §3.3 — licensed deterministic recovery of v̂₂ and B̂_agg for EXP133

**Lane:** LOG-4800 (CEO pre-assigned). **Status: DRAFT — licenses nothing.** This is a narrow
amendment draft to the CEO-SIGNED pre-reg
`research/prereg/EXP_PREREG_GEOSTEER_MULTISTEP_2026-09-30.md` (signed LOG-4798).
It amends ONLY breaking point (b) and §3.3. It licenses no execution; EXP133 re-execution
requires independent review of this amendment + fresh CEO clearance.

**$0 CPU scope.** Paper + artifact-inventory only; no model forwards were run to produce this draft.

---

## §1 — What tripped and why [FACT]

EXP133 went APPARATUS-VOID on breaking point (b) (LOG-4799):
`experiments/runs/EXP127_tga/out/exp127_vectors.npz` (SHA-256
`9b527c026d0ee307192725429f655e628f403505343dc018de3cfe15db6113dc`, intact)
contains 20 keys — 10 × `v1__<prompt_id>` (1024,) and 10 × `urand__<prompt_id>` (64×1024).
Zero `v2__` keys, zero `bagg__` keys. The signed pre-reg's breaking point (b) required all
three id families and ordered apparatus-void on miss; it further forbade re-running EXP131's
deflated power iteration ("re-pin only"). The conjunction was unsatisfiable — a **pre-reg
factual defect**, not an apparatus defect: the npz never contained v2/B_agg keys.
Two independent Law #14 reviews (LOG-4792, LOG-4793) and fix-verification (LOG-4797) checked
the breaking points' *logic* but never inventoried the artifact's *actual keys*.

## §2 — Amended breaking point (b)

**Strikes** the "re-pin only / no re-derivation" clause. **Replaces** with licensed
deterministic recovery, per direction family:

**(b1) v̂₁ — unchanged.** Re-pinned from `exp127_vectors.npz` exactly as before
(SHA-256 match + 10/10 `v1__<prompt_id>` id alignment; miss → apparatus-void).

**(b2) v̂₂ — licensed deterministic reproduction.** Reproduced with EXP131's exact derivation
(`experiments/bundles/exp131_v1inj/run_exp131.py` §7, the LOG-4714 erratum parameters):
seeded deflated power iteration, generator seed `20260929_4714` (`torch.Generator`,
CPU-seeded), K=40 fixed iterations per prompt, exact JVP/VJP sensing on the frozen
L20→L24 propagator, orthogonalization against the re-pinned v̂₁,i at every step,
prompts in pinned bench order (`BENCH_PIN e91b302f41f641c74e56957e526efcd486bac62d134e157defe0a4cdd49e4f5`).
This is licensed (not barred) because LOG-4714 records the derivation as
"Law #4 deterministic given seed + apparatus + frozen backbone" — reproducing it with
identical inputs IS re-pinning, not re-derivation in the drift-risk sense the original
clause fenced.

**(b3) B̂_agg — deterministic reconstruction with ground-truth hash verification.**
Reconstructed from the EXP077 archived support set via `exp077_support.py`
(`support_prompts` → 300 fixed presentations → `build_candidate_directions`; zero
randomness in the module — code-audited). The reproduced B_agg SHA-256
(float32 bytes) MUST equal EXP131's recorded pin
`d3556d83751634a2fc5114d56c4ee246bb1b296293d2adcde40a369da1600ae1`
(`exp131_records.json` → `pins.bagg_reconstruction`). Mismatch → apparatus-void.

## §3 — Verification discipline for the recovered directions

1. **Run-twice determinism:** the v2 reproduction is executed twice on CPU; the two runs
   must be bit-identical (SHA-256 equality). Miss → apparatus-void (nondeterminism —
   the LOG-4714 determinism assertion fails).
2. **Definitional asserts (per prompt):** ‖v̂₂,i‖ = 1 ± 1e-6; |v̂₂,i · v̂₁,i| < 1e-6
   (EXP131's own orthogonality assert, exit 44 on miss). Miss → apparatus-void.
3. **B_agg hash gate:** reproduced hash == `d3556d83…` exactly. Miss → apparatus-void.
4. **New pins:** the reproduced v2/B_agg SHA-256 values are recorded as the amended
   direction pins in the execution records (replacing the unsatisfiable npz-key clause).
5. **[CONJECTURE — stated honestly]:** EXP131 derived v2 on a T4 GPU; the CPU reproduction
   uses float32 throughout. Ulp-level GPU-vs-CPU differences (e.g. TF32 matmuls on Ampere)
   cannot be ruled out against EXP131's exact v2 bits — no v2 ground-truth hash was ever
   recorded. The rank-trend gate is a *relative* within-pilot comparison
   (v̂₁-effect vs v̂₂-effect) and is robust to ulp-level direction differences; the
   orthogonality + unit-norm asserts bound the reproduction to the correct mathematical
   object (the K=40 deflated second singular direction). If the run-twice check or the
   definitional asserts fail, the pilot does not proceed.

## §4 — Everything else unchanged [FACT]

The decision table (§2, including the B2 DEFAULT → INCONCLUSIVE row), the norm budget
B = 0.50578119 and its §0(d) audit, breaking points (a) and (c)–(g), the 7-arm design,
the H1/H6 §3.3 readout, the PIVOT/CONTINUE/KILL bars, and the founder-gated GPU fence
are ALL unchanged by this amendment. This amendment touches ONLY the v2/B_agg sourcing
clause.

## §5 — Law #14 review-checklist addition (process fix)

Breaking points that reference artifact *contents* (keys, vectors, hashes inside a file)
must be verified against the actual artifact — key inventory via direct inspection —
not merely against the spec text describing the artifact. Logic review without inventory
review let this defect class survive two independent reviews and a fix-verification
(LOG-4792/4793/4797). Future review briefs: require the reviewer to list the artifact's
actual contents (e.g. `npz` key listing with shapes) alongside the breaking-point text
that cites them, and to flag any cited content not found as a BLOCKING finding.
