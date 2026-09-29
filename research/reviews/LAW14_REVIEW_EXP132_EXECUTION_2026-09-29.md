# Law #14 Independent Review — EXP132 Execution (LOG-4744)

**Reviewer role:** independent execution review (Law #14). **Lane:** LOG-4744 (pre-assigned).
**Under review:** EXP132 execution (LOG-4743), executor
`experiments/runs/EXP132_dgf/run_exp132.py`, official console
`experiments/runs/EXP132_dgf/out/exp132_console.log`, execution report
`research/experiments/EXP132_DGF_GAINFIELD_REPORT_2026-09-29.md`.
**Reviewer performed independent recomputation** (rotary/materiality, mask equivalence,
LN placement, hidden-state layout) on the same pinned weights — no new experiment was run;
all checks are read-only apparatus audits.

## Verdict: SIGN-WITH-FIXES

The **binding outcome is confirmed and BOUND**: the §3.3 multi-ε float64 convergence
diagnostic passed on **0/10 prompts** (bar: ≥ 8/10) → **apparatus-void (RUN-INVALID)**,
hypothesis UNTESTED, no ΔGini minted, median ΔGini UNMEASURED. Every protocol-compliance
checkpoint the reviewer could independently verify **matches**. The six numbered fixes
below concern the report's interpretation language, figure provenance, pin terminology,
and a confirmed latent defect in EXP128 — none of them moves the binding verdict.

## Binding facts independently verified [FACT]

1. **Protocol hash pre-model-contact:** the file
   `research/prereg/EXP_PREREG_DGF_GAINFIELD_2026-09-29.md` on disk hashes to
   `6963043b8bed628646520bf3a2eb15389c2740eb4b85d913a8a7bcf2202ec6cf`,
   identical to the console's `protocol_pin`. The executor exits 42 on mismatch
   before any model contact (executor l.116–120). MATCH.
2. **Backbone pre-pin:** console records
   `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed` = LOG-331 pin.
   MATCH. Δθ=0 apparatus: eval mode, `requires_grad_(False)`, no optimizer/loss;
   backbone hash **re-verified after the float64 round-trip** (console:
   "model restored to float32; backbone hash re-verified after round-trip").
3. **Prompt set:** 10 ids verified verbatim against protocol §3.1 in-executor
   (mismatch → exit 42); console: "prompts: 10 pinned ids verified". PASS.
4. **Probe provenance:** semantic probe SHA-256
   `56828e953024101685692f02297ad90f817187733b2b8b497c73189921a6c9b2`
   recorded pre-JVP; support continuity `mean_cos_v1=0.7163`; unit-norm audit
   passed (1 semantic + 80 isotropic). PASS.
5. **Diagnostic parameters byte-match the signed protocol:** `DIAG_EPS=[1e-6,1e-7,1e-8]`,
   `DIAG_TOL=0.25`, `DIAG_LAYERS=[0,11,23]`, `N_PROMPTS=10`, `K_ISO=8`,
   and the pass rule (a prompt passes only if **every** probe × layer × ε satisfies
   `|F(ε)−JVP|/JVP ≤ 0.25`) implements protocol §3.3 exactly, including the
   "non-convergence → prompt excluded; < 8 passing → apparatus-void" tree.
6. **Official outcome:** console lines 18–27 record FAIL on all 10 prompts;
   "decision set: 0/10 prompts passed the diagnostic" → "apparatus-void: fewer than
   8 diagnostic-passing prompts. Hypothesis UNTESTED." Exit code 42 via the registered
   falsification tree. The JVP batches, verdict metrics, and Law #9 raw-record
   hash-pin were **correctly not reached** (Law #9 ordering: the gate failed first).
7. **Law #7:** no labels anywhere in the lane. **Law #6:** weights untouched (see 2).

## Apparatus audit — pre-execution implementation defects [FACT]

The lane reported four implementation defects found and fixed before the official run.
Independent verification:

- **(a) Missing rotary position embeddings — CONFIRMED material.** Re-running layer-0
  attention with vs without rotary on the pinned weights: relative output difference
  **0.98** at the attention block, decaying to **0.062** at the final readout.
  The fix was causally necessary; the pre-fix smoke numbers were void.
- **(b) Explicit causal mask vs default — PHANTOM, no defect existed.** The reviewer's
  test: explicit `create_causal_mask` + explicit `position_ids` + explicit rotary
  embeddings reproduces the default path (`attention_mask=None`, no position args)
  with relative error **0.0**. The default eager path was causal all along; the
  explicit implementation is faithful to it. The report's executor note is accurate
  and no correction is needed here.
- **(c) Final-LayerNorm placement — CONFIRMED correct for this lane, with a
  subtlety documented below.** For diagnostic layers {0,11,23}, `hidden_states[l]`
  is the true input to block *l* (see layout finding), and `make_g` applies exactly
  one final LayerNorm before the readout — consistent with the report's "relative
  error 0.0 at all layer splices" claim.
- **(d) CPU SDPA/flash backward — correctly sidestepped** via eager attention; in any
  case the diagnostic uses finite differences and forward-mode AD
  (`torch.autograd.functional.jvp`), neither of which requires a backward pass.

## Hidden-state layout finding (transformers 5.17.0) [FACT]

Direct probing of `GPTNeoXForCausalLM(..., output_hidden_states=True)` on the pinned
weights gives 25 entries with this layout:

- `hs[0]` = post-dropout embeddings; `hs[k]` = output of block *k−1* for 1 ≤ k ≤ 23;
- **`hs[24]` = post-final-LayerNorm state** (relative error 0.0 vs the model's
  `last_hidden_state`); the raw output of block 23 is **not** present in the tuple.

Consequences:

- **EXP132 is unaffected:** diagnostic layers {0,11,23} and probe site 21 all index
  true block inputs; `make_g`'s single final-LN application is correct.
- **EXP128's latent defect is CONFIRMED real (see FIX-5).**

## Numbered fixes (all required before the wave is committable)

**FIX-1 — Replace "Taylor radius ≈ 1e-11" with the licensed quantity.**
The report's [INTERPRETATION] "the layer-to-readout map's Taylor radius is ≈ 1e-11"
is mathematically unlicensed: the **signed protocol itself** (§3.3) states
"Pythia is C^∞, so differentiability is vacuous." Taylor radius is a claim about
analyticity; nothing in the diagnostic measures it, and the claim contradicts the
protocol's own premise. What the diagnostic measures is the scale below which the
**first-order approximation is 25%-accurate** — the linear-regime radius at the
registered tolerance — which the data place **below 1e-8** (bisection onset of the
sharp transition ≈ 1e-11 is worksheet-derived; see FIX-3). A large-curvature smooth
map (e.g. x + 10^10·x², infinite Taylor radius, linear regime ~10^-10) exhibits
exactly this behavior; curvature and analyticity must not be conflated.

**FIX-2 — Narrow "no operational meaning as a gain" to the licensed conclusion.**
The AD JVP is the true infinitesimal derivative — the lane verified `make_g`
reproduces the base forward exactly, and forward-mode AD is exact. What the
diagnostic establishes is narrower: **finite differences cannot validate the JVP at
any accessible scale**, so the instrument *as licensed* (FD-validated JVP sensing)
does not exist → apparatus-void. The report must not claim the derivative lacks
predictive content at finite ε; the protocol licensed no test of that proposition.
The existing "Why this is apparatus-void, not a verdict" section already states the
correct narrow conclusion — the "Relation to EXP128" paragraph must be conformed
to it.

**FIX-3 — Provenance-mark the quantitative observation claims.**
The per-prompt worst-relative-error table (1.36e5–2.46e5) and [OBSERVATION] items
2–4 (F(ε) values across ε, the block-13+ amplification trajectory, the ≈1e-11
bisection) trace to the lane's worksheet (`/tmp/diag_full.log`), which **no longer
exists** — /tmp is ephemeral and the file is gone. The committed console evidences
only per-prompt PASS/FAIL. Per Law #13 these figures are therefore **not
re-derivable from committed artifacts**. Either re-run the diagnostic worksheet and
commit it under `experiments/runs/EXP132_dgf/out/`, or label every such figure
"worksheet-derived; not reproducible from committed artifacts." The binding verdict
does not depend on them.

**FIX-4 — Disambiguate the two pins.**
The report's "(post-pin not reached …)" and the executor's post-diagnostic
"backbone hash re-verified" (h_mid) are **not inconsistent** — they are different
pins. The Law #9 **raw-record hash-pin** was correctly not reached (gate failed
first — protocol-compliant). The Law #6 **weight-integrity pin** (h_mid) **was**
performed after the float64 round-trip. The report must name which pin in each
statement.

**FIX-5 — EXP128 erratum (separate lane; recorded here as a finding).**
EXP128's `base_forward`/`perturbed_forward` apply `model.gpt_neox.final_layer_norm`
to `hidden_states[24]`, which — per the layout finding above — is **already
post-final-LayerNorm** in transformers 5.17.0. The double application deviates from
the correct single-norm readout by relative norm **0.165** (independently measured).
EXP128's linearity diagnostic therefore measured the **wrong construct** (double-
normalized readout), not the registered `x_{24,last}`. Verdict-category impact:
**none** — EXP128 stopped before metrics either way, so RUN-INVALID / DSF-UNTESTED
stands as a category; but its report's substantive linearity numbers
("1/12 within 25%", "amplification-driven transition saturation") are void as
measurements of the registered object and require an erratum. Note the EXP132
executor already flagged this ("executor's double-norm was a latent bug") and
EXP132's own readout is correct. Recommend a dedicated EXP128 erratum lane; this
review does not rewrite EXP128's report.

**FIX-6 (minor) — Console hygiene.** `exp132_console.log` contains duplicated
pre-diagnostic blocks (protocol-pin/bench/env/backbone lines appear twice —
append-mode residue from an earlier attempt). Truncate or annotate so the official
run's record is unambiguous. Not verdict-material.

## What the review explicitly does NOT license

- No resurrection of finite-difference DSF sensing (EXP128's instrument stays dead;
  EXP132's diagnostic killed the FD-validated variant too — both are kills of
  *instruments*, and Family B's targeting mission remains UNTESTED and unlicensed).
- No promotion of the ≈1e-11 figure beyond FIX-1's narrow reading.
- No claim about what EXP128's linearity check *would* have shown on the correct
  readout — that is unmeasured, not inferable.
- The capability scoreboard is unaffected: still **zero positive autonomous-steering
  signals**.

## Reviewer sign-off

**SIGN-WITH-FIXES.** Binding outcome BOUND as stated above. The wave
(protocol, executor, console, report with FIX-1→FIX-6 applied, scoreboard sync) is
committable once the fixes are byte-verified; no re-execution is required or
licensed.

## Post-sign verification note (2026-09-29, LOG-4744 lane)

After signing, an orphaned background test (script lost to /tmp ephemerality,
uninspectable) reported a make_g-style replay error of ≈0.45, contradicting the
lane's "rel error 0.0" claim. The reviewer re-derived make_g fidelity from
scratch: replaying `blocks[l:]` + one final LayerNorm from captured
`hidden_states[l]` reproduces the post-final-LN readout (`hs[24]`) at relative
error **0.0** for all diagnostic layers {0, 11, 23}. The contradictory figures
(0.45 stray; 0.98 in the reviewer's first replication attempt) both traced to
comparing against a wrong base target (`final_ln` applied one block early),
not to a make_g defect. Apparatus item (c) stands doubly verified; no change
to the SIGN-WITH-FIXES verdict.

## Post-sign record-integrity note (2026-09-29, LOG-4744 lane)

An unidentified background process executed `rm -f out/exp132_console.log &&
python run_exp132.py --smoke`. Verified afterward: the official console file on
the main filesystem is **intact and byte-identical** to the 30-line record this
review cites (the rm did not take effect on the main filesystem). Two findings
from the incident: (1) the smoke run independently reproduced the official
checkpoints (backbone LOG-331 pin, probe SHA-256 `56828e95…6c9b2`, diagnostic
FAIL, post-round-trip h_mid re-verification) — a second, independent
apparatus-void observation; (2) the executor's `--smoke` path has a robustness
bug: with 0 passing prompts it skips the apparatus-void exit
(`if n_d < 8 and not SMOKE`), runs JVP batches over an empty decision set, and
crashes with `IndexError` in `median_executor`. Not verdict-material for the
official run (which correctly exits 42), but the smoke path needs a graceful
empty-decision-set guard. Recommend against any lane deleting or overwriting
`out/exp132_console.log` — it is the committed evidence for the bound outcome.

## Post-sign replication note (2026-09-29, LOG-4744 lane)

A full official (non-smoke) re-execution of `run_exp132.py` completed
independently of the reviewed run: 0/10 diagnostic prompts passed, outcome
"apparatus-void: fewer than 8 diagnostic-passing prompts. Hypothesis UNTESTED.",
exit code 42 (`/tmp/exp132_official.log`). The committed console
`out/exp132_console.log` was verified afterward: still exactly the original 30
lines (the re-run's file writes did not land on the main filesystem — the
executor opens the log in append mode, so any future on-filesystem re-run
would append a second copy; see FIX-6). The binding outcome is therefore
independently replicated: two full runs, same verdict.
