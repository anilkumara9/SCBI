# Law #14 Independent Bundle Review — EXP086 Stage B (R3 Dynamical Amplifier)

**Reviewer:** Independent Law #14 bundle reviewer (reports directly to the founder; binding).
**Date:** 2026-09-25
**Bundle:** `experiments/runs/EXP086_amplifier/` (Stage-B implementation wave, 2026-09-25)
**Protocol:** `experiments/protocols/EXP086_R3_AMPLIFIER_PREREG_SIGNED.md`
**Protocol SHA-256 (self-verified):** `6fe122a0230d9dfc58a01d14c15da77f5e995e6beeae8c1f2e71af32943498f6` — **MATCHES** the digest in the task mandate.

## Verdict: SIGN-WITH-FIXES

The bundle is substantially well-constructed — the verdict table is exact, the
JVP/VJP/deflation mathematics is correct, Δθ=0 is sound, Law #7 is clean, and
the fail-safes are loud. But independent verification falsified the readiness
claim on **three protocol-fidelity defects** (F1–F3), one false documentation
claim (F4), and several unrecorded binding interpretations (F5–F6). None
requires re-registration — all are mechanical corrections that implement the
*signed* design — but the bundle is **NOT licensed for CEO GPU clearance
consideration until every required fix is applied and independently
re-verified by execution** (torch-free tests re-run green + the probe-identity
diff re-run clean).

**Scope:** Stage-B implementation only. Stage A (executed LOG-331, verdict
None by construction) is out of scope except where the bundle's Stage-A
modules affect Stage-B startup (checked: they don't — imports are lazy,
torch-free at module level).

**Method:** Read the signed protocol in full; read every bundle module;
re-derived the power-iteration/JVP/VJP/deflation math by hand; programmatically
diffed the probe rebuild against `run_exp077.py` (exec'd its exact construction
block) and against `run_exp084.py`; independently re-ran `test_exp086.py`
(104/104 pass) and `smoke_test.py` (16/16 pass); wrote and ran 14 independent
verdict-precedence probes against `exp086_verdicts.adjudicate` (14/14 pass,
covering all 7 adversarial probes plus V2/V3/V4/V7/V10/V11/V12).

---

## Required fixes

### F1 — The F2 sign rule is not applied to the treatment (protocol §4 fidelity; load-bearing)

**Protocol (§4, F2):** "v̂_r ← sign(⟨v̂_r, n̂⟩)·v̂_r — oriented to the +gap side
of the label-free decision normal. Rationale: gives the family its best
licensed shot; an arbitrary numerical sign must not decide the treatment."

**What the code does:** `run_full_loop` (run_exp086.py:801–806) computes
sign-flipped copies `vs` — but uses them **only** for the ĉ diagnostic
(`alpha = abs(_dot(vs[0], n_hat))`, where the `abs()` makes the sign
irrelevant anyway). The injected arms resolve via
`TorchBackend._resolve_direction` (lines 609–637), which returns
`self._v_cache[key]` — the **unsigned** power-iteration outputs cached at
line 575. The signed vectors are never written back to the cache, never
passed to `inject_and_eval`, and never stored in the run record.

**Consequence:** every injected direction (v̂₁/v̂₂/v̂₃ on all items, and the
Stage-2 permuted arm which resolves donor `(j,1)` from the same cache) carries
an **arbitrary numerical sign** — exactly what F2 forbids. This is not
cosmetic. Under the signed +gap rule the linear term is gap-*increasing* by
construction (Δg ≈ ε‖∇g‖⟨n̂,v̂₁⟩ ≥ 0), so decision flips must come from
nonlinear effects; under arbitrary sign, half the items get gap-*decreasing*
perturbations and flips can arise linearly. A primary win under the current
code would therefore **not be the signed test** — it would be uninterpretable
against the pre-registered claim. The defect also corrupts the discriminating
rank endpoint (v̂₁ vs v̂₃ with independently arbitrary signs).

BUILD_NOTES ("Sign rule: v̂_r ← sign(⟨v̂_r, n̂⟩)·v̂_r (§4 F2)") misdescribes the
bundle as implementing F2. It does not.

**Required fix:** apply the sign rule to the vectors that are actually
injected — e.g. a backend method that writes the signed directions back after
the sign computation (keeping `run_full_loop` backend-neutral), so that
`_resolve_direction` returns the F2-oriented vectors for v1/v2/v3 and the
permuted donor. Re-run the torch-free suites. No re-registration: this
*implements* the signed design; it does not change it.

### F2 — Power iteration costs 4 fwd-equiv/iteration, not the registered 3; the budget counter under-counts actual compute

**Protocol (§4):** "each iteration = 1 JVP (≈1 fwd) + 1 VJP (≈2 fwd)".
**Protocol (§11):** "deflated power iteration 3 vectors × 12 iters ×
(1 JVP ≈ 1 fwd + 1 VJP ≈ 2 fwd) = **108**" per item; total ceiling **7380**.

**What the code does:** `power_iteration` (run_exp086.py:530–551) performs
**two** JVPs per iteration — `jvp(f, delta0, w)` for Jw, `vjp(f, delta0, Jw)`
for JᵀJw, **plus** `jvp(f, delta0, w_new)` (line 549) solely to evaluate the
Rayleigh quotient ρ = ‖Jw_new‖². Under the protocol's own accounting
convention that is 2 + 2 = **4 fwd-equiv/iteration**, i.e. up to **144**
per item, while `run_full_loop` charges `budget.charge(108, …)`.

**Consequence:** worst-case actual compute is 60×(1 + 144 + 2 + 10) + 120 =
**9540 fwd-equiv ≈ 29% over the 7380 hard ceiling** the CEO would clear. The
`PassBudget` "hard ceiling" does not bound actual compute, and the §11
"honestly counted" claim is violated. (The runner would log 7380 while
burning ~9540.)

**Required fix:** eliminate the redundant JVP — compute the Rayleigh quotient
from the already-available first JVP of each iteration (ρ_t = ‖Jw_t‖², the
textbook power-iteration diagnostic; w_t is already in the deflated subspace
for ranks 2–3, and exactly equals w_new for rank 1). Convergence criterion
(relative change < 1e-3 × 3 consecutive, 12-cap) and σ̂ = √ρ are unchanged.
This makes actual cost exactly the registered 3 fwd-equiv/iteration with zero
change to the science. The alternative (charge 144/item) would exceed the
signed budget and require re-registration — so the JVP elimination is the
only fix compatible with the signed protocol. Re-run suites after the change.

### F3 — Probe rebuild is not verbatim: 1 of 60 prompts differs from EXP077

**Protocol (§6.1):** "verbatim rebuild, fixed indices. Any deviation (index
shift, item substitution) is loudly logged per EXP084-D1; the deviation note
is a required artifact."

**Evidence (programmatic):** I exec'd the exact benchmark-construction block
from `experiments/runs/exp077/run_exp077.py` and diffed all 60 items against
`build_benchmark_items()`. Index tuples, vocabularies, IDs, ent/typ, and
`target_first` parity all match — **except** `run_exp086.py:262`, which uses
`if i < 8:` where EXP077 uses `if i < 7:` (element-3hop block). Result:
global item 52 (`exp077_element_3hop_7`) —

- EXP077: "Premise: Steel is lower than Bronze. Bronze is lower than Gold. Gold is lower than Iron. …"
- EXP086: "Premise: Iron outranks Gold. Gold outranks Bronze. Bronze outranks Steel. …"

Same relational content, same question/options/answer — but a different
prompt string, and the deviation is **undisclosed** (BUILD_NOTES claims
"verbatim EXP077 construction"; the runtime deviation note covers only the
archive-lacks-prompts issue, not this).

**Required fix:** `i < 8` → `i < 7` on line 262; re-run `test_exp086.py`,
`smoke_test.py`, and the probe-identity diff (must return 0 diffs). No
re-registration (restores the signed verbatim requirement).

### F4 — The EXP084-D1 deviation note rests on a false premise

BUILD_NOTES and the `run_exp086.py:188–189` comment claim EXP084's
`build_benchmark` "uses DIFFERENT index tuples (a 15-cycle rotation set)."
Programmatic diff of the current `experiments/runs/EXP084_newton_duel/run_exp084.py`
against EXP077 shows its `_BENCH_TRIPLES`/`_BENCH_QUADS` are **identical** to
EXP077's `TRIPLES_INDICES`/`QUADS_INDICES` (all 30 tuples match; no rotation
set exists in the file). The note's conclusion — follow the authoritative
EXP077 construction — is correct and stands, but the false factual claim
about EXP084 must be removed/corrected in BUILD_NOTES, the code comment, and
the manifest note. (A review artifact that misattributes a defect to a
sibling experiment is itself a defect.)

### F5 — Unrecorded binding interpretations (protocol under-specifications the bundle silently resolves)

The protocol leaves the following ambiguous; the bundle picks readings that
are defensible but **undisclosed**, some materially affecting kill rows. Each
must be recorded in BUILD_NOTES/manifest as the binding interpretation:

- **(a) ĉ denominator:** `alphas` (hence ĉ and exceedance E) are computed over
  **non-aborted items only** (`run_full_loop`, else-branch). Protocol D6
  ("ĉ := (1/N)Σ_i |⟨v̂₁,n̂⟩|") does not restrict N. Including aborted
  (degenerate-direction) items would lower ĉ toward the chance level and make
  the V5 kill row easier to fire; excluding them is the less kill-prone
  reading. Defensible — but it must be declared, not silent.
- **(b) Rank-validity aggregation:** median of σ̂₁/σ̂₃ over non-aborted items
  (already flagged in BUILD_NOTES; record as the binding reading).
- **(c) The `converged` flag is diagnostic-only.** BUILD_NOTES falsely states
  "else converged=False → runner ABORTS item (§6.4)". The runner never aborts
  on `converged=False`; the σ̂₁/σ̂₂ < 1.1 ratio alone governs per-item aborts
  and the V3 fraction (this matches the explicit §6.4 pin; V3's "(Rayleigh
  stall)" parenthetical is descriptive). Correct the BUILD_NOTES sentence and
  record the ratio-rule as binding.
- **(d) Headroom timing:** the protocol (§6.1/§6.2) says headroom is "verified
  at build from archived correctness records"; the bundle verifies it at
  **runtime from the live baseline** (which is the more valid feasibility
  check, and fires before any direction budget is spent). Record the
  deviation-from-letter/compliance-with-intent explicitly.

### F6 — Manifest seed-schedule formula does not match the code

`manifest.json` documents `item_norm_seed(item, norm) = 20260924 + 100*item +
norm`; `exp086_rng.py:25` implements `20260924 + 1000*i + norm_idx`. Both
schedules are pairwise-unique (120 seeds) and deterministic — no scientific
impact — but Law #13 documentation must match the code. Correct the manifest.

---

## Advisory notes (non-blocking; for the CEO's clearance decision)

**A1 — GPU-fatal risk: `torch.use_deterministic_algorithms(True)` × default
attention path.** The CPU readiness test passed `attn_implementation="eager"`
*specifically because* torch-CPU flash-attention backward is unimplemented;
the GPU node will use the default attention path, which was never exercised
with deterministic algorithms on. Deterministic mode can raise on
non-deterministic SDPA/flash kernels depending on the torch build. Recommend a
GPU pre-flight (one item, `--run` gates) before the full 60-item run, or an
explicit `attn_implementation` pin with a documented fallback. Not a bundle
defect — an execution-venue risk.

**A2 — No per-item checkpointing.** The run record
(`exp086_stage_b_record.json`) is written once at the end of `finish_run`. Any
mid-run loud halt (NaN/Inf logits, degenerate gradient, or the uncaught
`NonTestableDataError` when a contrast has zero discordant pairs — possible in
principle if an arm never disagrees with its control) loses all per-item
data. The halts are fail-safe (never a wrong verdict), but a crash at item 59
wastes the GPU budget with nothing preserved. Recommend atomic per-item
checkpointing; at minimum, wrap the contrast statistics so a degenerate table
produces a loud, artifact-writing INVALID rather than a bare traceback.

**A3 — Stage-2 permuted donors include aborted items.** `power_iteration`
populates `_v_cache` for every item (abort is decided after), and the
Stage-2 derangement runs over all 60 indices — so a live item can receive an
aborted donor's degenerate v̂₁, which §6.4 says "would degenerate to random"
and is therefore a *weaker* item-specificity control (anti-conservative for
the V7 CONTINUE conjunct). The protocol is silent on donor eligibility.
Recommend documenting the reading or restricting the derangement to live
donors.

**A4 — Tango CI fallback bracket.** If the outward-stepping bracket fails,
`find_endpoint` falls back to full-range bisection without verifying the
bracket, which can in principle return a wrong-but-ordered interval in
degenerate tables (the `lo > hi` guard catches inversion only). The evaluator
suite cross-checks the implementation against dense-grid inversion on 6
tables, so residual risk is low. Noted for completeness.

---

## What verified clean (checklist responses)

1. **Protocol fidelity (§4/§6):** JVP/VJP/deflation construction is
   mathematically correct — hook adds δ at the layer-20 output/final position
   only; `vjp(f,δ₀,Jw)` returns JᵀJw; deflation implements
   (I−V̂V̂ᵀ)JᵀJ(I−V̂V̂ᵀ); σ̂_r = √ρ; sign of nothing else assumed. Convergence
   criterion (Rayleigh relative change < 1e-3 × 3 consecutive, 12-iteration
   cap) is faithfully implemented. **Except F1 (sign) and F2 (extra JVP).**
2. **Correctness endpoint:** greedy argmax over the full vocabulary at the
   answer position vs the single-token target (`build_probe` loudly refuses if
   target/foil are not single tokens) — the correct reading of the §4 sketch
   for single-token options. The primary contrast is the arm-vs-arm paired
   correctness difference with one-sided McNemar on discordant pairs and
   Tango 95% CI — the binding sensible reading of "flip-rate" (a raw
   change-counting reading would reward anti-steering, which the §7 ledger is
   explicitly designed to flag).
3. **Law #7:** clean. Direction construction (power iteration, n̂ from the
   model's own top-2) never touches labels; the target token ID is used only
   in `baseline_forward`/`inject_and_eval` correctness; headroom uses baseline
   correctness (endpoint use, standard). No bridge arm anywhere.
4. **Probe identity:** index tuples programmatically verified identical to
   EXP077 (and, contra the bundle's note, to EXP084's as well). **Except F3
   (one prompt) and F4 (false EXP084 claim).**
5. **Budget:** line-item charging matches the protocol exactly (108/item PI,
   2 VJP, 1/arm, 120 Stage-2, 7380 ceiling, hard refusal). **Except F2 (actual
   vs charged).**
6. **Fail-safes:** degenerate gradient, unresolvable direction tags,
   zero/defective ‖h‖, NaN/Inf h and logits, non-unit/non-finite B_agg,
   missing archives (sha256-pinned), missing weights dir, absent clearances —
   all loud halts, no silent passes. The `fused-slice` V-extraction path is a
   loud dead branch (LOG-327 repair intact).
7. **Verdict precedence:** 14/14 independent probes pass — V1–V4 INVALID rows,
   V5 preempts V7, V6 preempts V11, V7 full CONTINUE, V7b-before-V8 HELD,
   stage-2 gate raises `InvalidRunError` (never a silent verdict), V8 PIVOT,
   V9/V10/V11/V12 HELD, UNCLASSIFIED fall-through HELD. Exact §9 order.
8. **Frozen backbone:** `requires_grad_(False)` on all params, `.eval()`, no
   optimizer, no `.backward()` on params, no in-place weight ops;
   `FrozenBackboneGuard` snapshots the state_dict hash before the first
   weight-touching phase and verifies after Stage-2 (mismatch → INVALID V1).
   `sha256_state_dict` uses the program-standard float32-bytes convention.
9. **GPU-fatal risks:** no torch/transformers at module import time (all lazy
   inside `TorchBackend._setup`); no hardcoded absolute paths (archive/B_agg
   paths are bundle-relative, existence-checked by the crash guard);
   `--run` refuses without `--weights` pointing at a local directory (no HF
   hub network fallback); CUDA-absent refusal is loud. **Except A1.**

## Test evidence (independently re-run this review)

- `test_exp086.py`: **104/104 pass** (matches BUILD_NOTES).
- `smoke_test.py`: **16/16 pass** (matches BUILD_NOTES).
- `run_exp086.py --smoke`: exit 0.
- Verdict-precedence probes (authored for this review): **14/14 pass**.
- Probe-identity diff vs EXP077 construction: **1 diff** (F3); tuple diff vs
  EXP084: **0 diffs** (F4).
- `mock_harness.py`: re-run started during this review (long synthetic tail);
  BUILD_NOTES reports 13/13 — the verdict paths it covers were independently
  re-verified by this review's 14 probes.
- Signed protocol digest re-verified: `6fe122a0…93498f6` ✓.

---

## Binding conditions for SIGN

The verdict upgrades to **SIGN** (bundle licensed for CEO GPU-clearance
consideration) when **all** of the following are discharged and independently
re-verified by execution:

1. F1 fixed: injected directions carry the F2 sign (probe: signed cache or
   equivalent; assert `⟨v̂_r,n̂⟩ ≥ 0` on a synthetic backend test).
2. F2 fixed: power iteration performs exactly 1 JVP + 1 VJP per iteration
   (probe: count autodiff calls per iteration on a synthetic backend, or
   structural assertion; charged budget == actual).
3. F3 fixed: line 262 `i < 7`; probe-identity diff vs EXP077 returns 0 diffs.
4. F4 fixed: false EXP084 claim removed from BUILD_NOTES/code comment/manifest.
5. F5 recorded: (a)–(d) binding readings written into BUILD_NOTES + manifest.
6. F6 fixed: manifest seed formula matches `exp086_rng.py`.
7. Full torch-free suites re-run green after the fixes.

No protocol edit is required or permitted for any of the above (all implement
the signed design). A1–A4 are recommended but do not gate SIGN.

*Reviewer independence note: this review was conducted against the signed
protocol and the bundle artifacts only. No bundle, protocol, or other file
was modified in the course of this review.*

---

## Addendum — Re-verification of LOG-4326 fixes (LOG-4333): **REJECT** — two fixes incomplete

**Reviewer:** Independent Law #14 Reviewer (reporting directly to the founder; binding).
**Date:** 2026-09-25.
**Target:** `experiments/runs/EXP086_amplifier/` at commit `5c3d67d` (LOG-4327 fix wave).

### Verdict: REJECT — F4 and F6 are not discharged

Four of the six required fixes verify clean by execution. Two do not. The
upgrade conditions ("F1–F6 discharged … independently re-verified by
execution") are therefore not met. Both failures are documentation-only and
take minutes to repair; no science is affected.

### What verified

- **F1 (sign rule in treatment) — VERIFIED.** Exercised the real
  `TorchBackend.apply_sign_rule` with synthetic torch tensors (model load
  stubbed): all three cached v̂_r flipped to ⟨v̂_r,n̂⟩ ≥ 0 (dots 0.952, 1.0,
  0.0), unit norms preserved, signed v̂_1 returned for the ĉ diagnostic,
  missing cache → loud `RuntimeError`. Call ordering verified in
  `run_full_loop`: `apply_sign_rule` (line 842) precedes every
  `inject_and_eval` (lines 853, 862, 1054); `_resolve_direction` reads the
  flipped cache. The unsigned cache is never injected.
- **F2 (budget honest) — VERIFIED.** `power_iteration` performs exactly 1 JVP
  + 1 VJP per iteration; the Rayleigh quotient is `‖Jw‖²` from the iteration's
  own JVP (second JVP block removed). Charged 108/item = actual 3×12×3
  fwd-equiv; worst case 60×121 + 120 = 7380 = the hard ceiling. Charged ==
  actual.
- **F3 (probe verbatim) — VERIFIED.** Exec'd EXP077's exact inline
  construction block (`run_exp077.py` lines 587–637, `log` stubbed):
  **0/60 prompt diffs** vs `build_benchmark_items()`.
- **F5 (binding interpretations) — VERIFIED.** All five recorded in
  BUILD_NOTES (§"Binding interpretations", F5): ĉ over non-aborted items only
  (confirmed in code — `alphas.append` sits in the non-aborted `else`
  branch); rank-validity median-of-non-aborted; `converged` diagnostic-only
  (false "→ runner ABORTS" corrected in BUILD_NOTES and the
  `power_iteration` docstring; no lingering false claims found);
  headroom-at-runtime recorded; sign rule scope covers the permuted donor.
- **Suites — VERIFIED.** `test_exp086.py` **104/104** and `smoke_test.py`
  **16/16**, re-run by this review. (Note: 3 tests fail in a torch-present
  venv because they assert torch-absent refusal behavior — the
  "104/104" claim reproduces exactly under a torch-blocking import hook,
  i.e. the torch-free build-machine environment the suite is written for.
  Environmental, not a bundle defect.)
- **Verdict precedence — no regression.** `exp086_verdicts.py` (and guards,
  statistics, rng, henrici) are byte-identical between the pre-fix and
  post-fix commits; the LOG-4326 14/14 probe verification stands.

### What failed

- **F4 (false EXP084 claim) — INCOMPLETE.** The LOG-4326 ruling ordered the
  false claim removed from "BUILD_NOTES, the code comment, and the manifest
  note." BUILD_NOTES and the manifest now document the retraction correctly.
  But `run_exp086.py:199-200` **still asserts the false claim as a live
  comment**:
  `# DEVIATION NOTE (EXP084-D1 class): EXP084's run_exp084.py build_benchmark`
  `# claims a "verbatim" rebuild but uses DIFFERENT index tuples (a 15-cycle`
  `# rotation set). EXP086 does NOT follow EXP084; ...`
  This review independently proved the claim false: EXP084's
  `_BENCH_TRIPLES`/`_BENCH_QUADS` are byte-identical to EXP077's
  `TRIPLES_INDICES`/`QUADS_INDICES` (15/15 triples, 15/15 quads). A code
  comment asserting a known-false defect against a sibling experiment is
  exactly what F4 ordered removed. **Required:** correct the comment to
  reflect the retraction (point at the BUILD_NOTES F4 correction).
- **F6 (manifest seed schedule) — INCOMPLETE.** The manifest was corrected
  from `100*item` to `1000*item`, but the recorded formula is still wrong.
  Manifest: `item_norm_seed(item, norm) = 20260924 + 1000*item + 10*norm + k`.
  Code (`exp086_rng.py:29`, the sole seed function, sole call site
  `run_exp086.py:665`): `20260924 + 1000*i + norm_idx`. No code computes
  `10*norm + k`; the manifest formula does not describe the code. Law #13
  requires documentation to match code. **Required:** manifest schedule →
  `item_norm_seed(item, norm_idx) = 20260924 + 1000*item + norm_idx`.

### Conditions for SIGN

Apply the two documentation corrections above (no science change, no suite
re-run required beyond a JSON-validity check and a re-grep for lingering
copies). Re-verification is then a check, not a re-adjudication: confirm the
comment is corrected, the manifest formula matches `exp086_rng.py`, and no
other copies of either false statement remain.

Untouched by this ruling: EXP091's ADOPTED KILL (LOG-361/362), the LOG-204
bridge demotion, the H1 closure (LOG-4317), EXP092's chain (LOG-4319–4325),
the LOG-4321 weights-integrity clearance. The A1–A4 advisories stand as
non-blocking.

*Reviewer independence note: this addendum was appended; the original review
above is untouched. No bundle, protocol, or other file was modified in the
course of this re-verification.*

---

## Addendum 2 — Narrow re-verification of the LOG-4333 conditions (LOG-4335): **SIGN**

**Reviewer:** Independent Law #14 Reviewer (reporting directly to the founder; binding).
**Date:** 2026-09-25.
**Target:** the two documentation corrections from the LOG-4333 REJECT ruling, applied at LOG-4334 (commit `5827de6`).

This was a check, not a re-adjudication. All three named conditions hold, verified by execution:

**Condition 1 — F4 comment corrected: VERIFIED.**
`run_exp086.py:199–204` now carries an explicit RETRACTION NOTE: the earlier
"DEVIATION NOTE (EXP084-D1 class)" claiming EXP084's `build_benchmark` uses
"DIFFERENT index tuples (a '15-cycle rotation set')" is stated as FALSE and
RETRACTED, citing the programmatic diff (EXP084's `_BENCH_TRIPLES`/`_BENCH_QUADS`
byte-identical to EXP077's `TRIPLES_INDICES`/`QUADS_INDICES`, 15/15 triples,
15/15 quads). The claim appears in the comment only as the quoted object of
the retraction — no live assertion remains.

**Condition 2 — F6 manifest formula matches code: VERIFIED (by execution).**
The manifest schedule now reads `item_norm_seed(item, norm_idx) = 20260924 +
1000*item + norm_idx`, against `exp086_rng.py:29` (`return MASTER_SEED + 1000
* i + norm_idx`, `MASTER_SEED = 20260924`). Executed directly:
`item_norm_seed(0,0)=20260924`, `(0,1)=20260925`, `(7,0)=20267924`,
`(59,1)=20319925` — all match the manifest formula; `seed_schedule()` yields
120 pairwise-distinct seeds.

**Condition 3 — no lingering live copies: VERIFIED.**
Directory-wide grep for "15-cycle"/"rotation set" over
`experiments/runs/EXP086_amplifier/` returns 6 occurrences, all in retraction
contexts: this review file's own evidence quotes (lines 132, 360–361 —
append-only record, untouched), `BUILD_NOTES.md:27` (the retraction note),
`run_exp086.py:200,204` (the retraction note itself, quoting the claim it
retracts). No live assertion of the false claim survives.

**Binding verdict: SIGN.** The LOG-4326 upgrade conditions are met. The
EXP086 Stage-B bundle is cleared for the GPU pre-flight chain. CEO GPU
clearance and stage-2 review signoff remain user-gated; this SIGN does not
authorize execution. The A1–A4 advisories stand as non-blocking GPU
pre-flight items.

Untouched by this ruling: EXP091's ADOPTED KILL (LOG-361/362), the LOG-204
bridge demotion, the H1 closure (LOG-4317), EXP092's chain (LOG-4319–4331),
the LOG-4321 weights-integrity clearance.

*Reviewer independence note: this addendum was appended; the original review
and the LOG-4333 addendum above are untouched. No bundle, protocol, or other
file was modified in the course of this re-verification.*
