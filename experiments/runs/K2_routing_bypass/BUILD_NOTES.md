# K2 BUILD NOTES — LOG-226 assumptions inventory

Every interpretive choice made while building this bundle, and every defect
escalated rather than silently resolved. Nothing here changes the signed REV2
protocol; where the protocol could not be implemented literally, the bundle
implements it exactly as written and the gap is flagged for the CEO.

## 1. Resolved readings (adopted; documented, not silent)

**R1. G2 target/foil cross-check.** The pinned `exp077_instance_records.json`
does not record target/foil strings or prompts, so literal G2 ("option tokens
match the benchmark's recorded target/foil") cannot be checked against the
archive. Adopted reading: G2 is satisfied by (i) rebuilding the benchmark with
the EXP077 §3 builder ported verbatim, (ii) cross-checking rebuilt `ent`/`typ`
per index against the archive, and (iii) the single-token entity guard (M5.3)
plus the reconstruction-identity norm fingerprint. The residual literal gap is
flagged in §4.

**R2. Arm-(b) position scope.** REV2 names arm (b) "premise-entity-position
injection". Adopted reading: entity-string matching is restricted to the
premise substring (text before `"Question:"`), so question-side occurrences of
an entity string do not receive injection. Rationale: the arm's name and the
hypothesis under test (premise→final transport) both scope to the premise.

**R3. G4 pass count vs G10 exclusions.** REV2 pins 180 passes and separately
permits ≤6 G10 exclusions with "continue at actual N". Adopted reading: the G4
licensed count binds to 3 × N_actual (180 at full N=60; 162 at N=54, etc.).
Exclusions are decided before any GPU pass, so padding excluded items back to
180 would fabricate unlicensed passes. The runner enforces exactly
3 × N_actual.

**R4. Per-arm "exact 95% CI".** REV2 §3.4 names the primary contrast CI as
"Tango (score) two-sided 95% CI" and per-arm diagnostics as "McNemar exact p
and exact 95% CI". Adopted reading: the same Tango (score) interval is used
for the per-arm Δ̂M CIs (the protocol's designated paired-difference CI;
consistent with the K1 report's archived "lower 95% CI (Tango)" column, which
this bundle's implementation reproduces exactly: 0.0931/0.0651/0.0338/0.1444).
ADDENDUM (REV4 / LOG-228): the row-1 flatness conjunct is NOT the two-sided
diagnostic CI — it is the true ONE-SIDED 95% Tango upper (z=1.6449,
constrained-MLE variance), the one-directional form of the same interval
family; the two-sided CI stays as the reported per-arm diagnostic.

**R5. G9 diagnostic.** REV2 specifies only "the per-position residual norms at
the final layer" and "the G9 ratio". Adopted operationalization (diagnostic,
never verdict-bearing): within each injected pass, the localization ratio =
mean(per-position final-layer residual norm at injected positions) /
mean(per-position final-layer residual norm at non-injected positions).
G9 >> 1 → localized footprint; G9 ≈ 1 → broad position effects. Per-item
ratios and a "broad-effect rescues" count are recorded as [OBSERVATION].

**R6. Checklist-B reference pin.** The build-time observed tokenizer revision
`9879c9b5f8bea9051dcb0e68dff21493d67e9d4f` is a warn-only reference: the runner
logs the resolved revision and warns on mismatch. The signed checklist
requires logging, not pinning; a missing log is a recorded deviation, not INVALID.

**R7. Working directory.** Archive paths are repo-layout-relative
(`experiments/runs/EXP077_cone_vs_line/`). The bundle is Kaggle-ready via the
RUNBOOK's `git clone` cell, which restores the layout.

## 2. Verified properties (tested, not assumed)

- **Tango (score) CI correctness:** (i) reduces to McNemar's score statistic at
  δ=0 (exact match); (ii) reproduces the program's four archived K1 Tango lower
  bounds to 4 decimals (independent implementation, different agent);
  (iii) matches scipy's two-sided binomtest on the McNemar reduction;
  (iv) arm-swap symmetry CI(y,x) = −CI(x,y); (v) contains the point estimate;
  (vi) Z(δ) monotone decreasing on dense grids; (vii) seeded Monte-Carlo
  coverage of the nominal 95% CI within [0.925, 0.975] at two parameter
  settings, n_sim=1000 each.
- **One-sided 95% Tango upper (REV4 row-1 bar):** `tango_one_sided_upper`
  solves Z(δ) = −z_0.95 (z = 1.6449) through the SAME constrained-MLE score
  machinery (`tango_score_z`) as the validated two-sided path — one interval
  family, not two. Reproduces the signed canonical bite table to 6dp:
  0.043147 / 0.056902 / 0.067926 / 0.047712 (4dp forms 0.0431 / 0.0569 /
  0.0679 / 0.0477); z_0.95 = 1.644854 ≈ 1.6449 (tol 1e-3); strictly below the
  two-sided upper on all four canonical tables. The row-1 conjunct in
  `adjudicate_verdict` was REPLACED (not supplemented) with U_1s < 0.05; the
  two-sided per-arm CI remains as a reported diagnostic (REV4 §3.4).
- **McNemar exact p:** reproduces the archived smoke bridge-gate p
  (0.0001220703125) and the L1 MDE anchor (b=6,c=0 → 0.03125).
- **Archive cross-check:** the real `exp077_instance_records.json` re-derives
  b=14, c=0, p=0.0001220703125, ΔM=+0.2333 for C8 vs C1 through this bundle's
  endpoint code.
- **Verdict table:** all six rows (1, 2, 2r, 3, 4, 5) fire on synthetic data;
  row-5 aggregation covers all six FATAL sources; G10 6-vs-7 floor tested.
  Row-1 headline world uses a FLAT arm-(a) (0/60 → U_1s = 0.0431 fires);
  b=c=1 (U_1s = 0.0569) and b=c=2 (U_1s = 0.0679) worlds do NOT fire row 1;
  the N=54 exclusion-floor flat world fires row 1 (U_1s = 0.0477).
- **Row-3 catch-all (REV4 §6 widening):** the adjudicator's row-3 else-branch
  is explicit: contrast CI straddles → Inconclusive, OR the contrast clears
  but a per-arm conjunct fails (flatness for row 1: U_1s ≥ 0.05;
  rescue-presence for row 2: b_a < 6) → Inconclusive with a recorded
  `row3_reason` (`contrast_clears_row1_flatness_fails` /
  `contrast_clears_row2_rescue_presence_fails` / `contrast_straddle`).
  Tested: b=c=1 and b=c=2 worlds land in the named flatness-fail branch.

## 3. What was NOT executed

No GPU was used. No model weights were loaded in this build session (torch /
transformers are not installed on this machine). Phase 0's model-dependent
steps (tokenizer load, gate-A rebuilds, benchmark reconstruction against the
real tokenizer) run on the Kaggle CPU before the clearance gate. The 84
evaluator tests are pure-CPU and do not touch the model.

## 4. Escalated defects (implemented exactly as written; NOT silently fixed)

**D1. Row-1 U(Δ̂M_a) < 0.05 bar is unsatisfiable for a flat arm.**
RESOLVED by REV3 per LOG-227 (Law #14 option (a)), CORRECTED per LOG-228/229
— this section records the defect's history; the bundle now implements the
repaired bar. Under the protocol's Tango (score) 95% CI, the narrowest
achievable TWO-SIDED upper bound at N=60 is z²/(n+z²) = 0.0602 > δ_min =
0.05 (attained at zero discordant pairs; any discordants widen it), so the
REV2 row-1 conjunct "final-position channel demonstrably flat" could only
fire on a materially negative arm (a). The repair (LOG-227) replaces the
bar with the **true one-sided 95% Tango upper bound** U_1s(Δ̂M_a) < 0.05
(z = 1.6449, constrained-MLE variance) — the one-directional form of the
protocol's per-arm diagnostic CI. LOG-228's interval-identity ruling binds
true Tango: the ruling's recomputed numbers (0.0379/0.0536) were the
q-pinned score form (variance at the unconstrained MLE, Wald-like,
anti-conservative, unvalidated) — rejected BY NAME as interval-shopping;
the ruling's name controls. LOG-229 corrected the canonical bite table to
the named implementation (independently reproduced by three methods to
6dp): N=60 s=0 → **0.043147 FIRES**; b=c=1 → **0.056902 FAILS**;
b=c=2 → **0.067926 FAILS**; N=54 s=0 → **0.047712 FIRES** — including the
b=c=1 transcription slip **0.056009 → 0.056902**, which was an error in
LOG-226's report (the bundle code was always correct). Consequence priced
in REV4: row 1 fires ONLY at s_a=0 at N=60; any discordant-pair mass on
arm (a) — even net-zero b_a=c_a=1 — fails flatness → row-3 catch-all →
Inconclusive (HELD, never culled); the partition is ruled INTENDED
(LOG-228). The bundle implements the repaired bar exactly as written:
`tango_one_sided_upper` reuses the K1-validated score machinery (one
interval family), `adjudicate_verdict` uses it in row 1 (replace, not
supplement), and the evaluator tests pin the corrected table.

**D2. Literal G2 vs archive schema.** The pinned archive records `ent`/`typ`
per item but no target/foil strings or prompts (see R1). If the CEO requires
literal token-level G2 against recorded target/foil, the archive cannot supply
it; the adopted cross-check is the strongest faithful substitute.

**D3. Gate-A reference path assumes single-token target/foil.** The independent
CPU reference reconstruction requires the target and foil to be single tokens
(true of the present benchmark per M5.3). Multi-token entities would need a
protocol amendment; the runner logs the token ids per item.

## 5. Deviation and challenge records (for the final report)

- **Challenge (construction-identity):** the norm fingerprint is weak — any
  unit vector scaled to α=0.5 passes the norm check. The true implementation
  license rests on (i) deterministic reconstruction (byte-identical rebuilds),
  (ii) the live all-position positive-control gate (G5), and (iii) the anchor
  cross-checks (M5.1/M5.2). The bundle enforces all three.
- **Idea (not part of K2):** after K2 adjudicates routing vs final-position
  locality, localize the ×1.8 downstream gain by injecting at later block
  outputs under the same position masks. Cheapest falsifier: block-23-output,
  final-position-only injection — if residual gain over the L1 readout
  prediction collapses, amplification lies in blocks 21–23.
