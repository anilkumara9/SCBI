# Execution Report: EXP132 — ε-Free Directional-Gain Field

**Lane:** LOG-4743. **License:** CEO launch decision LOG-4741; pre-registration
post-fix SHA-256 `6963043b8bed628646520bf3a2eb15389c2740eb4b85d913a8a7bcf2202ec6cf`
(protocol hash verified before any model contact — match).

## Verdict

**apparatus-void (RUN-INVALID).** The hypothesis is UNTESTED; no ΔGini minted.

The §3.3 multi-ε float64 convergence diagnostic — the protocol's breaking
point — failed on **0/10 prompts** (required ≥ 8/10). Per the falsification
decision tree (§5): "convergence diagnostic < 8/10 prompts → apparatus-void;
hypothesis UNTESTED; the instrument failed."

## Decision-tree walk (code order, Law #9)

| Tree node | Outcome |
|---|---|
| Backbone LOG-331 pin (pre) | MATCH `ec276abe3902fab0…` |
| Prompt set: 10 pinned ids (protocol §3.1) | PASS (verbatim match) |
| Probe provenance: EXP077 support-set recipe, SHA-256 `56828e953024101685692f02297ad90f817187733b2b8b497c73189921a6c9b2` recorded pre-JVP | PASS |
| Multi-ε convergence diagnostic (§3.3) | **0/10 prompts passed → apparatus-void** |
| JVP batches | NOT RUN (tree stopped at the diagnostic per Law #9 ordering) |
| Raw-record hash-pin / metric / decision | NOT REACHED — no ΔGini minted |

Per-prompt diagnostic outcomes (worst |F(ε)−JVP|/JVP over 9 probes × 3 layers
{0,11,23} × ε ∈ {1e-6,1e-7,1e-8}; bar: ≤ 0.25):

[Law #13 provenance note] The worst-relative-error figures in the table
below are worksheet-derived, from the lane's diagnostic worksheet
(`/tmp/diag_full.log`), which no longer exists (/tmp is ephemeral). They are
not reproducible from the committed console, which evidences only
per-prompt PASS/FAIL.

| Prompt | Diagnostic | Worst rel. err |
|---|---|---|
| exp107_flip_exp077_planet_2hop_0 | FAIL | 2.19e+05 |
| exp107_ctrl_exp077_planet_2hop_1 | FAIL | 1.82e+05 |
| exp107_flip_exp077_planet_2hop_2 | FAIL | 1.59e+05 |
| exp107_ctrl_exp077_planet_2hop_3 | FAIL | 2.13e+05 |
| exp107_flip_exp077_planet_2hop_4 | FAIL | 1.85e+05 |
| exp107_ctrl_exp077_planet_2hop_5 | FAIL | 2.46e+05 |
| exp107_flip_exp077_planet_2hop_6 | FAIL | 1.36e+05 |
| exp107_ctrl_exp077_planet_2hop_7 | FAIL | 2.08e+05 |
| exp107_ctrl_exp077_planet_2hop_8 | FAIL | 2.43e+05 |
| exp107_flip_exp077_planet_2hop_9 | FAIL | 1.75e+05 |

**Decision set: 0 prompts. Median ΔGini: UNMEASURED (not minted).**

## What the diagnostic found [OBSERVATION]

The failure is not a code defect — it is a property of the map. Instrument
validation performed during this lane (deterministic, prompt-independent):

1. **The JVP is correct.** `make_g` reproduces the base-forward readout
   exactly (relative error 0.0 at all layer splices, float32 and float64).
   The analytic JVP (‖Dg₀·u‖ ≈ 4.48) is the true infinitesimal derivative.
2. **Finite differences do not converge to it.** (Worksheet-derived; not
   reproducible from committed artifacts — see the provenance note at the
   per-prompt table.) At ε=1e-3, F(ε)≈4.17 (≈JVP). At ε=1e-4, F≈22. At
   ε=1e-5, F≈223. At ε∈{1e-6,1e-7,1e-8}, F≈1.6e3–1.4e5. The quotient
   *grows* as ε shrinks — the opposite of Taylor behavior — with an
   ε-independent numerator floor ≈ 2e-3.
3. **Block-by-block trajectory** (ε=1e-6, float64 — worksheet-derived; not
   reproducible from committed artifacts). The perturbation is well-behaved
   through block 12 (scaled diff ≈ 5, linear regime), then amplifies
   super-exponentially from block 13: 28× → 76× → 282× → 703× → 1083× by
   block 21. Bisection localizes the sharp transition to scale ≈ 1e-11
   (worksheet-derived; see FIX-1 in the independent review — no analyticity
   claim is licensed).
4. **The model's own forward confirms it.** (Worksheet-derived; not
   reproducible from committed artifacts.) Recomputing F(ε) through the
   unmodified model (pre-hook splice) gives identical quotients — this is
   not an artifact of the manual block loop.

[INTERPRETATION] What the diagnostic measures is the linear-regime radius at
the registered 25% tolerance — the scale below which the first-order (JVP)
approximation is 25%-accurate. The data place this below 1e-8 (bisection
localizes the sharp transition onset at ≈1e-11 — worksheet-derived; see the
provenance note below). The signed protocol states the map is C^∞ (§3.3), so
no analyticity (Taylor-radius) claim is licensed here. The AD JVP remains
the exact infinitesimal derivative; what failed is its finite-difference
validation — finite differences could not validate it at any accessible
scale (≥ 1e-8 in float64). The protocol licensed no test of whether the
exact JVP predicts finite-ε behavior.

## Why this is apparatus-void, not a verdict

The protocol's breaking point (b) is explicit: the diagnostic gates the
decision set, and fewer than 8 passing prompts voids the apparatus. The JVP
sensing primitive is *mathematically* sound (it computes the true derivative),
but the diagnostic — the registered instrument-health check — fails because
the derivative's linear regime at the registered 25% tolerance (below 1e-8;
bisection onset of the sharp transition ≈1e-11 is worksheet-derived) lies
below every probed ε. The
instrument as *licensed* (JVP validated by finite-difference convergence)
does not exist. Per Law #4, the bars bind as written; the diagnostic cannot
be re-interpreted post-hoc into a pass.

## Relation to EXP128 [INTERPRETATION]

This deepens EXP128's RUN-INVALID finding. EXP128 showed finite differences
at ε=1e-3 measure amplification-driven saturation, not the derivative.
EXP132 shows the complementary boundary: finite differences cannot validate
the exact AD derivative at any accessible scale, so the instrument as
licensed (FD-validated JVP sensing) does not exist. The AD JVP itself is
the exact infinitesimal derivative; the protocol licensed no test of its
predictive content at finite ε. The DSF soft-spot hypothesis remains
UNTESTED (it was never measured, by either instrument).

[FACT — EXP128 erratum finding] The independent review confirmed a latent
defect in EXP128's executor: it applies `model.gpt_neox.final_layer_norm` to
`hidden_states[24]`, which in transformers 5.17.0 is already post-final-
LayerNorm — a double application deviating from the correct single-norm
readout by relative norm 0.165 (independently measured). EXP128's linearity
diagnostic therefore measured the wrong construct, not the registered
`x_{24,last}`. Verdict-category impact: none — EXP128 stopped before
metrics either way, so RUN-INVALID / DSF-UNTESTED stands as a category — but
its reported linearity numbers ("1/12 within 25%", "amplification-driven
transition saturation") are void as measurements of the registered object and
require a dedicated erratum (recommended; this report does not rewrite
EXP128's report). EXP132's own readout was verified correct (exactly one
final LayerNorm applied at every splice).

## Honest frame

- **Characterization only** — no targeting claim is made or implied;
  Family B's targeting mission stays UNTESTED and unlicensed.
- No ΔGini was minted; no Gini field was measured; the JVP batches were
  never run (tree stopped at the diagnostic).
- Δθ=0 verified by the LOG-331 backbone pre-pin. The Law #6 weight-integrity
  pin (h_mid — backbone hash re-verified after the float64 round-trip, console
  line 22) WAS performed. The Law #9 raw-record hash-pin was correctly NOT
  reached (the gate failed first — no verdict metrics were computed; no
  weight mutation possible by construction: no optimizer, no loss, eval mode,
  requires_grad=False throughout).
- No labels anywhere (Law #7 clean).
- No generality beyond Pythia-410m and the 10 pinned prompts.
- The capability scoreboard is unaffected (still zero positive signals for
  autonomous steering).

## Executor and records

- Executor: `experiments/runs/EXP132_dgf/run_exp132.py` (eager attention
  backend — the CPU sdpa/flash backend has no backward; backbone pin
  unaffected). Official run exit code 42 (apparatus-void) via the registered
  falsification tree.
- Console log: `experiments/runs/EXP132_dgf/out/exp132_console.log`.
- Diagnostic instrument-health records: the lane's worksheet
  (`/tmp/diag_full.log`) is gone (/tmp is ephemeral); the quantitative
  figures above are worksheet-derived and not reproducible from the
  committed console, which evidences only per-prompt PASS/FAIL (Law #13).
- Protocol: `research/prereg/EXP_PREREG_DGF_GAINFIELD_2026-09-29.md`
  (SHA-256 `6963043b…c6cf`, verified pre-contact).
- Backbone: LOG-331 `ec276abe3902fab0…` (pre-pin MATCH).
- Environment: torch 2.14.0+cpu, transformers 5.17.0, numpy 2.5.3, CPU,
  2 threads, $0.
