# EXP087 Execution Bundle — Build Notes (LOG-332, 2026-09-25)

## Binding sources (read in full before build)
- `experiments/protocols/EXP087_TRANSLATION_SIGNATURE_PREREG_SIGNED.md`
  (signed at LOG-324; immutable — untouched by this build)
- `experiments/protocols/ERRATUM_EXP087_STALE_WATERMARK_2026-09-24.md`
- LOG-329 (`reports/research_log.md`): LOG-329 precedence rule —
  **signed header + embedded at-signing resolutions = BINDING LAYER**;
  retained draft body = adopted design text; on conflict the binding layer
  governs. In particular the R5 binding resolution is
  **μ̂ ∉ [0.649, 0.849] → RUN-INVALID**, NOT the draft's struck "CONTINUE".

## Bundle contents
`experiments/runs/EXP087_translation_signature/`

| File | Purpose |
|---|---|
| `exp087_benchmark.py` | Verbatim 60-item benchmark port (EXP065/066 identical); pinned order O; G2 byte-identity check |
| `exp087_guards.py` | Pins (model/layer/N/α/R5 envelope/archived values); startup crash guard; frozen-backbone SHA-256 guard; dual-flag refusal gate; determinism fingerprint; **provisional** GROSS_CORRUPTION_BAR (see §8-item note) |
| `exp087_rng.py` | Master seed 20260925; deterministic Python RNG; second-seed prohibition |
| `exp087_join.py` | Pinned K1 c_i join: O order; 60 unique keys; SHA-256 prompt identity; JoinError on any failure |
| `exp087_statistics.py` | μ̂ + envelope; positivity; rescue-set Hamming; subset; McNemar b/c; Pearson r + one-sided p via deterministic incomplete beta; 4σ LayerNorm diagnostic |
| `exp087_verdicts.py` | R5 precedence; headroom gate; guard-iii gross gate; R1–R4 → CONTINUE; all-hold → KILL |
| `exp087_support.py` | C3 support set: verbatim EXP066 B_agg construction (150 pairs); torch-free aggregation tested |
| `run_exp087.py` | CLI: `--analyze` (CPU), `--mock`, `--execute` (refuses without BOTH license flags) |
| `test_exp087.py` | Evaluator tests |
| `smoke_test.py` | Fast pre-flight checks |
| `mock_harness.py` | 8 end-to-end scenarios on CPU |
| `manifest.json`, `requirements.txt` | Bundle manifest; execution-path requirements |
| `BUILD_NOTES.md` | This file |

## §8 delegated items 3–5 — final resolutions (LOG-329 Order 3)

**Item 3 — second seed for C1.** Resolution: NO second seed.
Rationale: C1 is deterministic under the pinned snapshot + pinned
environment; a second seed gives no information and would exceed the
registered 180-pass budget. Enforcement is de-facto: `torch.manual_seed`
is called exactly once on the execution path (`run_exp087.py::execute`)
and no second seed exists anywhere in the bundle. (F3 correction,
LOG-340: an earlier draft of this note falsely claimed an
`exp087_rng.require_single_seed(1)` call that does not exist and was never
called; the RNG module was never the enforcement mechanism. The
resolution — no second seed — was always satisfied.) Status: resolved
in-build; independent bundle review LOG-340 (F-12) ACCEPTED.

**Item 4 — LayerNorm saturation 4σ rule.** Resolution: exact two-sided
residual rule `|Δm_i − μ̂| > 4·sample_std(Δm), ddof=1` implemented in
`exp087_statistics.layernorm_saturation_flag`. It is DIAGNOSTIC ONLY:
flagged items are listed in the report and feed the analysis §6
discussion; they do NOT independently change any verdict. Rationale: the
uniform-field prediction is about the *mean* translation; extreme outliers
are informative about saturation but the protocol registers no verdict on
them. Status: resolved in-build; flagged for independent review.

**Item 5 — KILL write-up venue.** Resolution: documentation-only — a KILL
write-up is an addendum to the boundary-paper §5.4 lineage, NOT a
standalone note, and changes nothing about endpoint, verdict, cost, or
mapping. Status: resolved in-build; flagged for independent review.

## Binding adjudications on the three build-lane interpretations (LOG-340)

Independent Law #14 bundle review (LOG-340; reviewer reports to the
founder directly) ruled on all three. The rulings below are BINDING —
the CEO may replace a number with written rationale; none may be silently
edited.

1. **GROSS_CORRUPTION_BAR = 4 — ACCEPTED (binding, A1).** The signed
   protocol's guard §3(iii) licenses "large deviation invalidates the
   run" but leaves "large" unquantified. The bar preserves the registered
   R1 mapping in the mechanism-relevant zone (any c ∈ {1,2,3} still breaks
   R1 → CONTINUE) and reserves RUN-INVALID for c ≥ 4, where the run
   demonstrably is not the registered C2 arm under the determinism pin
   (archived c = 0). The threshold was invented in the build lane; it is
   NOT signed protocol text — it is now binding review text.

2. **Join-failure mapping — ACCEPTED, ratified as binding (A2).**
   `run_exp087.py::analyze` maps an execution-time pinned-join failure to
   RUN-INVALID (apparatus; mechanism verdict withheld; rerun required).
   R1–R3 and R5 do not use the join, so no registered row is disturbed.

3. **Headroom gate [0.40, 0.70] — ACCEPTED with record correction (A3).**
   The [0.40, 0.70] band is NOT provisional: it is protocol text (§3
   Design: "headroom gate 40–70% carried over"). Only the violation
   mapping (RUN-INVALID, apparatus) was build-lane, and it is ratified: a
   benchmark-regime violation cannot license a mechanism verdict. Check
   order (after R5) is immaterial — both are RUN-INVALID. NOTE: in the
   archived-data reproduction the base-accuracy figure is not in the
   archive, so the gate is exercised only on synthetic data in this
   build.

Prior provisional text (superseded by the rulings above, retained for
the audit trail): the bar was implemented as a provisional interpretation
with the reviewer invited to accept/replace/strike; the join mapping was
flagged for review; the headroom band was described as provisional.

## Verified archive values (grounding, 2026-09-25)
From `experiments/runs/EXP066_pythia410m_replication/exp066_instance_evaluations.json`
(60 records) and `research/analysis_plans/K1_RESULTS_LOG213_2026-09-23.json`:
- μ̂_arch = 0.7492101669311524; min Δm_arch = 0.6481475830078125;
  sup|ε| = 0.10106258392333989 (all pinned in `exp087_guards.py`).
- Under the pinned O pairing: r(Δm_arch, c_K1) = **0.49708** (R4 passes).
  Under sorted-key pairing: r = **−0.21388** — pairing is load-bearing;
  the pinned join exists to prevent exactly this failure.
- Archive insertion order: planet_2hop_0..14, planet_3hop_0..14,
  element_2hop_0..14, element_3hop_0..14 (= O).

## Repair wave — binding Law #14 fixes F1–F3 (LOG-340 verdict)

- **F1 (apparatus integrity):** `MODEL_REVISION = "9879c9b5f8bea9051dcb0e68dff21493d67e9d4f"`
  (LOG-331 pinned snapshot) added to `exp087_guards.py`; both
  `--execute` `from_pretrained` calls in `run_exp087.py` now pass
  `revision=G.MODEL_REVISION`. Blocks a silent wrong-revision download
  that would run to a verdict on the wrong weights — undetectable by the
  Δθ=0 guard (pre==post only) or G2 (prompts only). Changing the pin is a
  design change → NEW experiment number.
- **F2 (precision):** `execute()` now injects the FULL `state_dict_hash_pre`
  / `state_dict_hash_post`, `model_id`, `model_revision`, and
  `delta_theta_zero` into the report dict written by `write_report` —
  a revision/pin failure is detectable post-hoc in the report JSON.
- **F3 (precision):** the false `require_single_seed(1)` claim in the §8
  item-3 note repaired (function never existed; enforcement is the
  de-facto single `torch.manual_seed` call on the execution path).

None of F1–F3 changes any registered endpoint, verdict, cost, or mapping —
no new experiment number.

## Test status (this build — actual runs, 2026-09-25)
- `test_exp087.py`: **59/59 pass** (evaluator, incl. archived-data reproduction)
- `smoke_test.py`: **8/8 pass** (incl. `--execute` refusal without flags, exit 2)
- `mock_harness.py`: **8/8 scenarios pass** (S1 KILL; S2–S5 CONTINUE by row;
  S6 R5 RUN-INVALID; S7 join-failure → JoinError; S8 archived r=0.49708 /
  sorted-r=−0.21388 / μ̂=0.74921 in envelope)

## License state
- Bundle construction: CPU, $0 GPU — authorized under standing orders.
- GPU execution: **NOT LICENSED.** Independent Law #14 bundle review
  (independent of the build lane) must SIGN first, then CEO GPU clearance.
  The runner's `--execute` path refuses (exit 2) without both flags.
- Signed protocol: verified untouched (sha256 recorded in the LOG entry).
