# Independent Pre-registration Verification — EXP148 (LOG-4956)

**Verifier:** Independent pre-registration verifier, 2026-10-06. Did not draft the pre-registration; verdict is binding.
**Artifact verified:** `research/analysis_plans/EXP148_PREREG_2026-10-06.md` (FINAL, sign-ready; LOG-4955).
**Reference:** J7 proposal SIGN review (LOG-4954), EXP147 verdict (2026-10-05), signed S7-1 plan (2026-10-05), committed `EXP147_RESULTS_2026-10-05.json`.
**Verdict: SIGN.**

This verification attempted to break the pre-registration — transcription errors, unaddressed advisories, drifted bars, degenerate signals, scope leaks. It found none.

---

## 1. Pins character-identical [FACT]

All three long identifiers verified character-by-character against both the EXP147 verdict text and the committed results JSON (`bench_pin` field):

| Identifier | Pre-reg value | Committed source | Match |
|---|---|---|---|
| Bench pin (64 hex) | `2b055b53127a241b72338a82373c3efc7b666256e25d8c584d45989278c14dcf` | results `bench_pin` + verdict §5 | ✅ 64/64 |
| Model revision (40 hex) | `9879c9b5f8bea9051dcb0e68dff21493d67e9d4f` | verdict §5 | ✅ 40/40 |
| Δθ=0 program pin (64 hex) | `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed` | verdict §2/§5 (pre/post) | ✅ 64/64 |

No transcription errors. The 2026-10-05 AGENTS.md lesson (single-hex-digit typos) was applied via scripted exact-substring comparison, not eyeballing. Law #2 holds.

## 2. LOG-4954 advisories concretely addressed

- **(i) C/S scoring-pipeline unit test:** §5.4(u0) — zero-forward unit test with 5 synthetic cases ((a) standard `ANSWER:`, (b) lowercase variant, (c) multiple occurrences/last-wins, (d) trailing ramble, (e) missing → 0). Concrete, not mentioned-in-passing. ✅
- **(ii) Exemplar reuse vs rebuild:** §5.2 — "reuse EXP147's Step-0-pinned exemplar file byte-identical. If that file is unavailable at execution, rebuild exemplars by the S7-1 §5.2 construction procedure... and record the new pin." Explicit rule with fallback. ✅
- **(iii) Power as upper bounds:** §2.3 — full [CAVEAT] block: "the power figures above are upper bounds" if compositional strata contribute ~0 discordant pairs; "the ceiling biases toward HELD (wide CIs), never toward false KILL or false CONTINUE." Registered, not hand-waved. ✅

## 3. Worth-it gate — complete, no drift

All 7 Law #15 points present (§1.1–1.7). Decision bars compared against S7-1 §1.2 and §3/§4:
- CONTINUE/KILL/PIVOT/HELD/RUN-INVALID conditions match S7-1 verbatim, including the two-sided McNemar clause (ii) which S7-1 §3 already operationalized ("no significant anti-discipline effect — else HELD").
- The §1.7 breaking point adds the Step-0 dry-run gate to S7-1's KILL conjunction — this is the licensed substantive delta of EXP148 (the repair's gate), not drift. Explicitly flagged as the addition.
- Mathematical license §1.5(a)–(d) inherited unchanged from S7-1. ✅

## 4. Step-0 dry-run gate — binding, correctly specified

- 20 fresh items, subset seed registered at execution and **distinct from 7101** ✅
- B arm only, T_B=15, greedy, §5.3 first-token scoring ✅
- Pass: B ∈ [0.2, 0.8] → full run licensable (still needs CEO execution authorization) ✅
- Fail: → "EXP148 STOPS at design cost (~300 forwards). No full run, no verdict; the stop is logged." ✅
- False-fail ≈ 5.5% independently recomputed at LOG-4954 (Bin(20, 0.6611)); pre-reg cites it as [FACT]. ✅
- Seed rule sane: fresh randomness, no reuse of construction seed. ✅

## 5. Law #9 — metrics pre-registered, no peeking

- Primary (pooled first-token accuracy difference, McNemar on S−C discordant pairs) and secondaries registered before any new output. ✅
- The pre-reg's governing-laws block states C/S arms never ran in EXP147 — confirmed against the verdict ("Arms C and S not run") and the committed results. There is no unrun data to peek at. ✅
- EXP147's descriptive first-token numbers are labeled prior observations, not tuning targets. ✅

## 6. Guards well-formed and computable

(a) Δθ=0 pre/post hash — computable. (b) model revision programmatic — computable. (c) bench pin recompute 64/64 — computable. (d) first-token B ∈ [0.2, 0.8] — correctly adapted to the repair (was full-generation exact-match; now first-token), computable. (e) ≥50% WRITE-span regex — computable on raw text. (f) token-count ratios — computable. (f′) band [2/3, 3/2] — computable. (g) ≤50k forwards — computable. (h) 72h throughput gate — computable. (u0) synthetic-string unit test — computable, zero forwards. All trip conditions map to the §4 decision table without ambiguity. ✅

## 7. No degenerate-by-construction signals

Per the 2026-10-05 lesson, each scored signal was asked "can this vary across items in principle?":
- Per-arm first-token correctness: varies (EXP147: 119/180) ✅
- Guard (e) WRITE-span presence: varies with model behavior ✅
- Token counts (f)/(f′): vary ✅
- Bench pin / Δθ=0 hash: integrity constants by design (guards (a)/(c)), not scored signals — correctly constant. ✅
No S5-1-class degeneracy (identically-valued "agreement") present. ✅

## 8. Scope fence present

§0: "tests J7... at **Pythia-410m only**. It licenses no claim about other models, other scales, or other model families. Cross-family generality is bounded by EXP145's independent KILL/PIVOT; nothing here re-opens it." ✅

---

## Verdict

**SIGN.** The pre-registration is sound: pins verified character-identical, all three review advisories concretely addressed, worth-it gate complete with no drift, dry-run gate binding and correctly calibrated, Law #9 respected, guards computable, no degenerate signals, scope fenced.

Execution of the Step-0 dry run may proceed on CEO authorization. Full-run execution remains gated on the dry run passing. Nothing in this verification licenses the full run.

---

*Verification conducted 2026-10-06. No model forwards run. No files modified except this report and the LOG-4956 entry.*
