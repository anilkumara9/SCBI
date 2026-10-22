# Law #14 Independent Review — EXP131 Amendment F (budget drift-detector)

**Reviewer:** independent Law #14 lane (LOG-4828 pre-assigned by the CEO). No prior
involvement in the draft. $0 CPU, paper only.
**Verdict: SIGN** — no blocking findings, no advisories.

## Materials read in full

- `experiments/bundles/exp131_v1inj/AMENDMENT_DRIFT_DETECTOR_2026-09-30.md` (DRAFT)
- LOG-4825 (independent SIGN on Amendment E, incl. the (b) mini-amendment recommendation),
  LOG-4826 (CEO commission), LOG-4827 (draft record), in `reports/research_log.md`
- Signed pre-reg `experiments/bundles/exp131_v1inj/EXP_PREREG_TGA_V1_INJECTION_2026-09-29.md`
  §0 (breaking-point/exit conventions)
- `experiments/bundles/exp131_v1inj/run_exp131.py` (executor, spot-verified)
- `~/workspace/SCBI/AGENTS.md`

## Findings

### 1. Mechanical correctness — PASS

- **Insertion point exact.** The executor's section 5 ends at the
  `log("budget B = 0.01 * median||y20|| = %.8f  (recorded BEFORE first injection forward)" % B)`
  line (line 266); the section-5b header (breaking point (h)) follows immediately with
  no intervening statements. The draft's "between line 266 and the section-5b header"
  is implementable verbatim.
- **Assertion implementable exactly.** `|B_cpu − 0.50578119| / 0.50578119 ≤ 1e-4`
  uses only in-scope names; B is positive and finite at that point (the executor's
  `assert B > 0 and math.isfinite(B)` precedes the log line), and the divisor is a
  nonzero literal.
- **Miss behavior matches convention.** `sys.exit(44)` is the executor's
  apparatus-void code: verified at 8 call sites (v1 hash, v1 ids, (h) control,
  v2 orthogonality, ĉ exclusions, per-arm norm audit, (d) budget audit, backbone
  post-pin) — every one logs "apparatus-void" and exits 44. Exit 42 = HALT/hash
  quarantine, 43 = RUN-INVALID; 44 is the correct choice for a breaking-point miss.
- **Zero decision forwards.** Sections 5/5b precede section 6 ("option embeddings
  (fresh forwards, no injection)") and all injection batches; the draft's claim
  holds by code order.

### 2. Reference constant — PASS

- `0.50578119` is traceable: the local Kaggle report
  (`experiments/runs/EXP131_tga_v1inj/out/exp131_report.json`) records
  `budget_B = 0.505781192779541`; LOG-4766 and the scoreboard cite `0.50578119`.
- The 8-decimal truncation introduces relative error ≈ 5.5e-9 against the full
  float64 value — four orders of magnitude below the 1e-4 band. The constant is a
  measured value (Law #2), not invented, and the truncation is provably immaterial.
- The draft's "occurs 0 times in `run_exp131.py`" verified by direct grep
  (count = 0): the detector is a genuine addition, not a duplicate.

### 3. Band justification — PASS

- 1e-4 sits 20.7× above the measured CPU-vs-GPU drift of relative 4.832e-6
  (LOG-4803: backbone, bench, and B_agg pins bit-identical; diagnosis
  cross-device floating-point ordering). LOG-4805 (independent SIGN on EXP133's
  Amendment C) already established 1e-4 as the demonstrated-safe detector band,
  and the draft cites it as a band, not as an imported breaking point — the honest
  fencing LOG-4825 required.
- **False-void risk negligible.** A legitimate CPU run trips the detector only if
  cross-device drift exceeds 1e-4 relative — >20× the measured noise floor. The
  1e-6 alternative is demonstrated unsatisfiable across devices (LOG-4803's void).
- The drift license transfers: same model, same LOG-331 weights pin, same
  transformers 5.17.0, same B computation (1% of median ‖y_{20,last}‖).

### 4. Narrowness — PASS

The draft changes exactly one thing: the (d2) detector. Verified against the
"everything else unchanged" clause: dose B remains the runtime-computed CPU value
(the detector only observes it), hypothesis, bench, arms, §2 decision table,
metrics, seeds, the (d) same-device per-arm audit (1e-6, unaffected), and the (h)
control are untouched. The signed pre-reg is byte-identical; its startup SHA-256
check still passes. The document is DRAFT, paper-only, and explicitly licenses
nothing (Law #4/#5 hold).

### 5. Redundancy — NOT REDUNDANT (genuine gap covered)

- Backbone pin: catches weight/environment change, not dose shift.
- (d) per-arm norm audit (1e-6): same-device — a systematic cross-device shift in
  B_cpu passes (d) on every arm while the dose differs from the GPU-registered B.
- (h) positive control: verifies delivery (tap moves), not dose magnitude.
- (d2) is the only guard that compares the runtime dose against the registered
  dose. The gap is real and previously bit the program (LOG-4803).

### Law #11 labeling — PASS (one passing observation)

All [FACT] labels verified against primary sources. Observation (non-blocking,
no fix required): the "Miss behavior [DEFINITION — executor convention]" label
self-qualifies as an executor convention rather than a project definition; it is
honest as written.

## Disposition

Amendment F approved as drafted: a narrow, mechanical, correctly-specified
apparatus addition. It licenses nothing by itself — executor implementation and
execution still require fresh CEO clearance.
