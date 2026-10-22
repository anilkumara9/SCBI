# EXP128 (DSF/SENSITIVITY-FIELD) Execution Report — 2026-09-29

**Lane:** LOG-4706 (pre-assigned). **Protocol:**
`research/prereg/EXP_PREREG_DSF_SENSITIVITYFIELD_2026-09-29.md`
(launch-ready: Law #14 SIGN-WITH-FIXES LOG-4704, all seven fixes
byte-verified LOG-4705; post-fix sha256
`c1f5212651fc8d2ca2eefd6e4bebfc9580dc7a85f958bd19f48f8b73263f683b`
— verified before any forward).
**Verdict: RUN-INVALID (apparatus-void)** — the ε/2 linearity check
(breaking point (b)) failed: 1/12 check points within 25% (bar:
≥ 10/12). The finite difference at ε = 1e-3 measures nonlinearity,
not the propagator norm. No field was minted, no Gini was computed,
no ε was retuned.
**$0 CPU. Δθ=0 by construction (no optimizer, no loss, no backward
pass into weights; backbone LOG-331 pin matched pre-forward). No
metric was read (Law #9 — the metric is read only after all guards
pass, and the tree halted at the linearity gate).**

---

## 1. Verdict statement

**RUN-INVALID (apparatus-void; hypothesis UNTESTED, no verdict on the
soft-spot premise).** All pre-forward guards passed (protocol hash,
prompt provenance, δ-budget audit, backbone pin), the full forward
batches ran (10 base + 960 field perturbed + 48 ε/2-check forwards,
exit code normal), but the conjunctive breaking point (b) failed:
the ε/2 linearity check returned **1/12** check points within the
25% band (≥ 10 required). Per §0(b) and the §5 falsification tree,
the lane halted there: no raw-record hash-pin, no Gini, no decision.
**G, top-3, and all four §4 bars do not exist** — no concentration
statistic was computed, and none is reported.

The soft-spot hypothesis survives this RUN-INVALID as untested (as
the protocol's boundary §10 prescribes: apparatus-void, never
re-tuned). This is not a KILL — the model is not shown to be
dynamically homogeneous; it is shown only that this finite-difference
apparatus cannot measure its propagator norm at this ε.

## 2. Falsification-tree walk (all numbers executor-produced)

| Tree node | Result |
|---|---|
| Protocol hash before execute | **PASS** — `c1f5212651…73263f683b` matched |
| Bench provenance: 10 verbatim EXP107 prompts, canonical-order first 10 | **PASS** — ids `exp107_{flip,ctrl}_exp077_planet_2hop_{0..9}`; text byte-identical to EXP127's pinned decision set |
| δ budget: ‖δ‖ = ε on all layers/items/draws (audited per draw) | **PASS** — 960/960 field + 48/48 check within 1e-9 of budget (see §3) |
| Backbone LOG-331 pin (pre) | **PASS** — `ec276abe3902fab0…` before first forward |
| 1920-formula field forwards + 48 ε/2-check forwards (either batch order) | **DONE** — 10 base + 960 perturbed + 48 check = 1018 actual forwards, exit normal |
| **ε/2 linearity-check evaluation (S(ε) reused from the field): ≥ 10/12 within 25%** | **FAIL → RUN-INVALID** — 1/12 within 25% (§2.1 table) |
| Backbone LOG-331 pin (post) | **not reached** (halted at the check, per tree order) |
| Raw-record hash-pin / layer-Gini / top-3 / §4 bars | **not reached** (halted at the check, per tree order) |

**Δθ=0 note:** the post-forward backbone pin was not computed because
the lane halted at the linearity gate before the post-pin node (the
tree places the gate before it). The pre-forward pin matched LOG-331;
the executor contains no optimizer, no loss, and no backward pass
into weights — the backbone could not have been trained by
construction.

## 2.1 Linearity-check table (executor-produced, the verdict-determining numbers)

Check points: items {0,4,9} × layers {L5,L11,L17,L23}, 12 points,
ε/2 arm (δ/2, same seeds and draw indices). S(ε) = mean over the 4
draws of the field ratio at (item, layer); S(ε/2) likewise.

| item | layer | S(ε) | S(ε/2) | \|Δ\|/S(ε) | verdict |
|---|---|---|---|---|---|
| 0 | L5 | 9.4964 | 21.1816 | 1.230 | FAIL |
| 0 | L11 | 10.8147 | 18.9249 | 0.7499 | FAIL |
| 0 | L17 | 10.8375 | 21.3019 | 0.9656 | FAIL |
| 0 | L23 | 7.38359 | 9.11771 | 0.2349 | PASS |
| 4 | L5 | 8.44262 | 15.7927 | 0.8706 | FAIL |
| 4 | L11 | 8.93842 | 17.7076 | 0.9811 | FAIL |
| 4 | L17 | 7.77752 | 18.3736 | 1.362 | FAIL |
| 4 | L23 | 3.91339 | 7.16379 | 0.8306 | FAIL |
| 9 | L5 | 8.3498 | 15.5471 | 0.862 | FAIL |
| 9 | L11 | 7.83391 | 15.5642 | 0.9868 | FAIL |
| 9 | L17 | 7.96442 | 16.2509 | 1.04 | FAIL |
| 9 | L23 | 3.04035 | 4.65474 | 0.531 | FAIL |

**1/12 within 25%** — far below the ≥ 10/12 bar.

## 3. Descriptive failure-mode analysis (unlicensed observations, not a verdict)

[OBSERVATION] On 11/12 check points, S(ε/2) ≈ 1.5–2.4× S(ε) — i.e.
the response magnitude ‖g_l(y_l+δ) − g_l(y_l)‖ is roughly
*independent* of ‖δ‖ at this scale (halving the budget barely moves
the numerator, so the ratio doubles). The finite difference is
measuring a saturating, threshold-like response, not a linear
propagator.

[INTERPRETATION] This is consistent with the Kreiss intuition that
motivated DSF, turned against the apparatus: if the block dynamics
are strongly non-normal, a norm-ε perturbation can be transiently
amplified to a scale set by the dynamics rather than by ε — the
linear regime of the propagator, if it exists, lies below this ε.
The pre-registration forbids retuning ε (§0(b), §10), so this stays
a descriptive observation, not a re-test.

[OBSERVATION] The sole PASS (item 0, L23, rel = 0.2349) is the
readout-adjacent site, where the rest-of-model map is one block +
LayerNorm — the shortest, least nonlinear span. The check fails
everywhere the map spans ≥ 2 blocks.

## 4. Raw artifacts

`~/workspace/SCBI/experiments/runs/EXP128_dsf/out/` (Law #8 —
the failed run is retained):

| Artifact | SHA-256 |
|---|---|
| `exp128_console.log` (append-only; both attempts) | — |
| `exp128_stdout.log` (full console transcript) | — |
| `exp128_execute.py` (the executor; `.venv-exp111`: torch 2.14.0+cpu, transformers 5.17.0, numpy 2.5.3) | — |

No `exp128_field.json`, `exp128_check.json`, `exp128_ratios.json`,
or `exp128_worksheet.json` was written: the tree halts at the
linearity gate before the §3.9 hash-pin node, so there are no raw
records to pin. The 12 check-point values live in the console log
(§2.1 table).

Environment: torch 2.14.0+cpu, transformers 5.17.0, numpy 2.5.3;
`torch.manual_seed(20260929)`, threads=2 (read back 2);
`model.eval()`, `torch.no_grad()`; float32; greedy-N/A (no
generation). Runtime ~11 min for 1018 forwards (exit normal).

## 5. Protocol-fidelity notes

- Protocol hash verified before any forward; prompt ids and text
  verified verbatim vs the EXP107 bench and EXP127's pinned
  decision set.
- **Numerical realization of the δ budget (executor-internal, not a
  protocol change):** the pinned budget ε = 1e-3 is not exactly
  representable in float32 (nearest float: 0.0010000000474974513).
  The executor applies one deterministic renormalization per draw
  (δ ← δ·(ε/‖δ‖)) so every (item, layer, draw) receives the
  identical float32 budget, audited at 1e-9 tolerance (960/960 +
  48/48 pass). The δ direction remains the seed-deterministic
  isotropic unit vector; the seeded RNG stream is unchanged.
- **First-attempt halt, disclosed:** the first run used a 1e-12
  audit tolerance and halted apparatus-void before any perturbed
  forward (the budget check, not the science, misfired). The fix —
  1e-9 tolerance with the exact-budget renormalization — was applied
  to the executor only (no protocol edit), and the full tree re-ran
  from the top. Both attempts are on the append-only console log.
- Loader: `AutoModelForCausalLM` (the EXP126 loader lesson);
  LOG-331 computed on the causal-LM state dict per the canonical
  method.
- No McNemar table, no b/c/d/p, no p-value anywhere in this report
  — none was computed. Defect class (a) clean.

## 6. Honest frame

- A RUN-INVALID is not a KILL: the soft-spot premise is **untested,
  not retired**. The bars in §4 of the protocol were never read.
- The honest scientific content of this run is a guard-passed
  negative about the *apparatus*, not the hypothesis: at ε = 1e-3,
  the layer-to-readout finite-difference gain does not behave
  linearly on this decision set — the response saturates rather
  than scaling. Any future gate that wants a sensitivity field must
  first find a linear regime (a new gate, a new pre-registration —
  this one is closed).
- No injection is licensed by this run. The v_1 injection test
  (EXP127's downstream) proceeds independently on EXP127's own
  license, without a layer-targeting prior.
- The capability scoreboard stays at zero — **still zero positive
  signals for autonomous steering.**
- No generality is claimed beyond frozen Pythia-410m and the 10
  pinned prompts.
- Novelty remains N1 — Known Combination (§7.1.6).

[END EXTERNAL CONTENT: source=file file=~/workspace/SCBI/research/experiments/EXP128_DSF_SENSITIVITYFIELD_REPORT_2026-09-29.md tool_name=report]
