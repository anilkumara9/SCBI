# EXP087 — Independent Law #14 Bundle Review (2026-09-25)

**Reviewer:** Independent Scientific Mentor & Adversarial Reviewer — reports
DIRECTLY to the founder. This verdict is binding; the CEO cannot override,
suppress, or recall it.

**Target:** `experiments/runs/EXP087_translation_signature/` (CPU construction,
$0 GPU, LOG-339). This is a BUNDLE review: does the built code faithfully
implement the signed protocol? It is not a protocol re-review.

**Binding sources read in full before review:**
- `experiments/protocols/EXP087_TRANSLATION_SIGNATURE_PREREG_SIGNED.md`
  (signed LOG-324; SHA-256 verified untouched this review:
  `32c27415b20fa0d07adb4fffb61127859c5e726fbfecff642a89e91fc1358d23` —
  matches the LOG-330/erratum record character-for-character)
- `experiments/protocols/ERRATUM_EXP087_STALE_WATERMARK_2026-09-24.md`
  (LOG-329/330; R5 binding resolution: μ̂ ∉ [0.649, 0.849] → RUN-INVALID)
- `experiments/runs/EXP087_translation_signature/BUILD_NOTES.md`
- All bundle modules: `run_exp087.py`, `exp087_benchmark.py`,
  `exp087_guards.py`, `exp087_rng.py`, `exp087_join.py`,
  `exp087_statistics.py`, `exp087_verdicts.py`, `exp087_support.py`,
  `test_exp087.py`, `smoke_test.py`, `mock_harness.py`, `manifest.json`,
  `requirements.txt`
- Cross-checked against the primary sources the bundle claims verbatim
  status from: `experiments/scripts/run_exp066_pythia410m_replication.py`
  (bridge hook, `make_bridge_vec`, B_agg construction ll. 97–154),
  `experiments/runs/EXP066_pythia410m_replication/exp066_instance_evaluations.json`,
  `research/analysis_plans/K1_RESULTS_LOG213_2026-09-23.json`

## Verdict: SIGN-WITH-FIXES

The bundle is faithful to the signed protocol in every registered
endpoint, verdict row, guard, and budget that matters. Three fixes are
required before it is clear for CEO GPU-clearance consideration. None of
the fixes changes a registered endpoint, verdict, cost, or mapping — no
new experiment number is triggered.

---

## 1. Faithfulness findings (all verified, not trusted)

**F-1 R5 binding remap — CORRECT.** `exp087_verdicts.adjudicate` evaluates
the R5 envelope FIRST and maps a breach to RUN-INVALID with the mechanism
verdict withheld, even when a mechanism-row break co-occurs (test
`r5_dominates` covers exactly this). The draft's struck CONTINUE mapping
(E87-4, highest severity) is nowhere reachable: the module docstring
explicitly marks it superseded. The binding layer governs; the code obeys
the binding layer.

**F-2 Falsification rows R1–R4 — CORRECT.**
- R1: `min Δm_i > 0` AND `c == 0` both required; either break → CONTINUE.
- R2: `P = {i : m0,i < 0 < m0,i + Δm_i}` — verified algebraically identical
  to the protocol's `{m₀,i ∈ (−μ−ε_i, 0)}` since Δm_i = μ+ε_i; Hamming = 0
  required.
- R3: `rescued_C3 ⊆ rescued_C2` exact set check; violators reported.
- R4: one-sided p < 0.05 for corr > 0; ANY other outcome (including
  non-significant positive) → CONTINUE. The t-distribution p-value was
  independently recomputed by the reviewer via numerical integration:
  r = 0.49708, n = 60 → one-sided p = 2.671e-05, matching the bundle.
  (Observation O1 below on the protocol's parenthetical.)

**F-3 Arms and budget — CORRECT with noted construction cost.** C1/C2/C3 at
pythia-410m/L20, α = 0.5, 60 items × 3 arms = 180 measurement passes. The
C3 support construction (150 pairs × 2 passes = 300) is the registered
EXP066-verbatim B_agg definition, not an unregistered extra — the EXP066
archive holds no B_agg vector (verified: no `b_agg` key in the 60 archive
records), so reconstruction is the only constructible route. Observation
O2 records the budget split.

**F-4 Bridge vector — VERBATIM.** Original EXP066 `make_bridge_vec`:
`w = embed_out.weight[tt,:] − embed_out.weight[ft,:]`,
`w / (torch.norm(w) + 1e-12)`. The bundle's execution path uses
`model.embed_out.weight` with the identical normalization. Character-level
match on the formula.

**F-5 Injection mechanics — VERBATIM.** The reviewer's initial attack
(broadcast `v.view(1,1,-1)` added to the full layer output vs the
protocol's "final-token position") is RESOLVED in the bundle's favor: the
archived EXP066 runner's hook does exactly the same broadcast
(`h_mod = h + alpha_val * v_vec` on the full sequence output); "final-token
position" in the protocol refers to the readout (`logits[0,-1,:]`), which
the bundle also matches. The bundle reproduces the archived intervention,
which is what the determinism pin requires.

**F-6 B_agg construction — VERBATIM.** 5 support vocabularies
(Anglo/Biblical/Greek/Roman/Modern, identical entity lists), identical
triples/quads index tables, identical `q_opts` alternation
(`(i % 2 == 0)`), byte-identical prompt templates, `hidden_states[L+1]
[0,-1,:]` relational-minus-neutral differences, per-vocab
normalize→mean→normalize, sum→normalize aggregation with the same 1e-12
guards. The pure-math `aggregate_b_agg` is torch-free and unit-tested.

**F-7 Benchmark port — VERIFIED against the archive.** The G2 byte-identity
check (archive insertion order == O, all 60 prompts byte-verbatim) passes
on the reviewer's rerun. The archive is the ground truth; the port matches
it exactly regardless of upstream script drift.

**F-8 Pinned join — CORRECT and load-bearing.** All four failure modes
raise JoinError (bad length, duplicates, hash mismatch, missing keys);
60/60 unique keys enforced; SHA-256 over UTF-8 prompt bytes with no
normalization. The reviewer's rerun reproduces r = 0.49708 under the O
pairing and r = −0.21388 under sorted-key pairing — the pairing is
genuinely load-bearing, and the pin prevents exactly the silent
mis-pairing failure.

**F-9 Refusal gates — CORRECT.** `--execute` without BOTH
`--bundle-review-signoff` AND `--ceo-gpu-clearance` exits 2 before any
weight access (verified by subprocess on the reviewer's rerun). Single-flag
also refuses. The flags are attestations; the docstring correctly notes
that presenting them without the underlying SIGN/clearance is a Law #4
violation by the operator.

**F-10 Δθ=0 guard — CORRECT.** Pre/post state-dict SHA-256 with FATAL on
mismatch; verified to catch a 0.001 perturbation on a fake state dict.

**F-11 LayerNorm 4σ diagnostic — CORRECT and verdict-inert.** Exact
two-sided `|Δm_i − μ̂| > 4·sample_std(ddof=1)` per §8 item 4; recorded in
diagnostics only, never consulted by any verdict branch (verified by code
path inspection — `layernorm_saturation_flag` output flows only to
`report["diagnostics"]`).

**F-12 §8 items 3–5 resolutions — ACCEPTED.** Item 3 (no second seed):
de-facto enforced — `torch.manual_seed` is called exactly once on the
execution path; no second seed exists anywhere. (Precision fix F3 on the
documentation.) Item 4 (4σ rule): exact and diagnostic-only, verified
above. Item 5 (KILL venue): documentation-only, changes nothing
registered. None alters endpoint/verdict/cost/mapping.

---

## 2. Binding adjudications on the three provisional interpretations

**A1. GROSS_CORRUPTION_BAR = 4 — ACCEPTED.** The protocol's §3 guard (iii)
licenses "large deviation invalidates the run as a replication (apparatus)"
but leaves "large" unquantified. The build's bar preserves the registered
R1 mapping in the mechanism-relevant zone (any c ∈ {1,2,3} still breaks R1
→ CONTINUE) and reserves RUN-INVALID for c ≥ 4, where the run demonstrably
is not the registered C2 arm under the determinism pin (archived c = 0).
The threshold does not alter any registered row; it only decides whether a
break is read as mechanism (small c) or apparatus (large c). The CEO may
replace the number with written rationale; it may not be silently edited.

**A2. Execution-time pinned-join failure → RUN-INVALID — ACCEPTED.** The
protocol's strike clause (§8 item 2) applied at signing, where the join
was verified working. At execution time the protocol names no verdict; the
build's mapping is the only one that neither silently mis-pairs R4 nor
launders an apparatus failure into a mechanism verdict. R1–R3 and R5 do not
use the join, so no registered row is disturbed. Ratified as binding.

**A3. Headroom gate [0.40, 0.70] with violation → RUN-INVALID — ACCEPTED,
with correction of the record.** The [0.40, 0.70] band is NOT provisional:
it is protocol text (§3 Design: "headroom gate 40–70% carried over"). Only
the violation mapping (RUN-INVALID, apparatus) is build-lane, and it is
ratified: a benchmark-regime violation cannot license a mechanism verdict.
Check order (after R5) is immaterial — both are RUN-INVALID.

---

## 3. Required fixes (F1–F3)

**F1 (apparatus integrity — REQUIRED). Pin the model snapshot revision in
the `--execute` path.** `run_exp087.py::execute` calls
`AutoModelForCausalLM.from_pretrained(G.MODEL_ID, ...)` and
`AutoTokenizer.from_pretrained(G.MODEL_ID, ...)` with NO `revision=` pin.
The protocol's determinism pin requires the pinned snapshot (LOG-331:
HF revision `9879c9b5f8bea9051dcb0e68dff21493d67e9d4f`). Without the pin, a
silent wrong-revision download runs to a verdict on the wrong weights —
undetectable by the Δθ=0 guard (pre==post only) or the G2 check (prompts
only). Fix: add
`revision="9879c9b5f8bea9051dcb0e68dff21493d67e9d4f"` to both
`from_pretrained` calls (define as `G.MODEL_REVISION` in
`exp087_guards.py`; changing the pin is a design change → new experiment
number). Two lines; blocks a silent invalidation of a GPU run.

**F2 (precision — REQUIRED). Log the FULL pre/post state-dict hash in the
execution report.** Currently only the first 16 hex chars reach stdout and
nothing reaches the report JSON. A revision/pin failure is then
undetectable post-hoc. Fix: include the full `pre_hash`/`post_hash` (and
the pinned `MODEL_REVISION`) in the report dict written by
`write_report`.

**F3 (precision — REQUIRED). Repair the §8-item-3 documentation.**
BUILD_NOTES.md claims "`exp087_rng.require_single_seed(1)` must be called
on the execution path" — the function does not exist and nothing calls it
(verified by repo-wide grep). Either implement it and call it, or correct
the note to state the de-facto enforcement (single `torch.manual_seed`
call; no second seed anywhere in the bundle). The resolution itself (no
second seed) is satisfied; only the documented mechanism is false.

Applying F1–F3 does not change any registered endpoint, verdict, cost, or
mapping — no new experiment number.

---

## 4. Observations (not defects, no action required)

- **O1.** The signed protocol §2's parenthetical "(archived r = 0.49708,
  p = 5.3e-05" quotes the TWO-sided p; the registered decision rule is
  one-sided p < 0.05, which the bundle implements correctly
  (one-sided p = 2.67e-05, independently verified). The bundle is faithful
  to the registered rule; the parenthetical is protocol text, not a bundle
  defect.
- **O2.** GPU budget is 180 measurement passes + 300 B_agg construction
  passes (the registered C3-arm definition). Recommend the execution log
  record both counts separately; the §4 "180 forward passes" covers the
  measurement arms.
- **O3.** The mock harness's S1 seed-search loop (first passing seed wins)
  is deterministic (fixed seed sequence) — inelegant, not a defect.
- **O4.** `tok.encode(label)[0]` silently truncates multi-token entities;
  this matches the protocol's specified convention and the archived run's
  convention, so replication fidelity is preserved. Noted for future
  benchmark ports.

---

## 5. Independent test reruns (this review, 2026-09-25)

- `test_exp087.py`: **59/59 pass** (reviewer's run; matches build claim)
- `smoke_test.py`: **8/8 pass** (reviewer's run; includes `--execute`
  refusal, exit 2, via subprocess)
- `mock_harness.py`: **8/8 scenarios pass** — S1 KILL; S2–S5 CONTINUE by
  the correct row; S6 R5 RUN-INVALID; S7 JoinError→RUN-INVALID; S8
  archived reproduction r_pinned = 0.49708 (p = 2.67e-05),
  r_sorted = −0.21388, μ̂_arch = 0.74921 in envelope (reviewer's run)

No test count was taken on trust; every number above is from the
reviewer's own executions.

## 6. License statement

GPU execution remains **NOT LICENSED**. On application of F1–F3 (verified
by diff, not by attestation), this bundle is cleared for the CEO's GPU
clearance decision. Queue position on clearance: behind K2 → EXP083 →
EXP084 → EXP086 Stage B → EXP088; no pre-emption. The signed protocol was
not edited by this review; the review file is the binding record.
