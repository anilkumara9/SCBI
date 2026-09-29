# Independent Law #14 Review — H22 Pre-registration (HONESTY-GEN4)

**Review lane:** LOG-4676 (pre-assigned, independent of the LOG-4675 drafting lane).
**Review date:** 2026-09-29.
**Target:** `research/prereg/EXP_PREREG_H22_HONESTYGEN4_2026-09-29.md` (259 lines, §§0–9 + boundary).
**Ground sources:** `research/strategy/H22_GATE_2026-09-29.md` (LOG-4674, binding gate memo, worth-it gate PASS); `research/prereg/EXP_PREREG_H6_HDILR_2026-09-29.md` (H6 apparatus, EXP112 — 41/60 HELD); the LOG-4639 bar-discrepancy audit (H6 bars bind verbatim); `research/strategy/H18_GATE_2026-09-29.md` (LOG-4639 — bench-2 apparatus-void).
**Method:** full read of the draft; diff-checked every "carried verbatim" claim against H6; independently recomputed all five cited binomial probabilities plus the two auxiliary quantities with exact arithmetic; mechanically verified all 21 entity token IDs and the QUESTION_SUFFIX `[-3:]` tail on the real Pythia-410m snapshot tokenizer (tokenizer-only, no model contact); checked bar coherence/disjointness/exhaustiveness by integer enumeration; swept for undocumented drift, cross-bench comparisons, H18 revival, and screening loopholes.

## Verdict: SIGN-WITH-FIXES (one launch-gating, verdict-immaterial fix)

The design is licensed, the H6 apparatus is carried faithfully, the bars bind verbatim, all fences hold, and every cited number is exact. One clause (§3.5, the construction-time per-item filtering allowance) is in tension with the model-free construction discipline and needs a one-line tightening before the construction lane is briefed; it cannot change any verdict because no decision bar reads it.

## What was verified

**1. Decision bars — coherent, disjoint, exhaustive (checked by integer enumeration).** Integer counts 0–60 partition as: 0–33 → KILL, 34–41 → HELD, 42–57 → CONTINUE, 58 → HELD, 59–60 → KILL — 61/61 integers covered, zero overlap, zero gaps. Post-hoc rewording → BARRED is an orthogonal Law-#4 rule, not a count region. RUN-INVALID (gates) and apparatus-void/HALT (pre-number) are orthogonal outcome classes, consistently distinguished in the breaking point (§0.6) and the falsification tree (§5). §1's falsifiers ([0.70, 0.95] hypothesis; ≥0.98 / ≤0.55 falsifiers) match the bars exactly (42/60 = 0.70, 57/60 = 0.95; 59/60 = 0.9833; 33/60 = 0.55). Matches the LOG-4639-audited H6 bands verbatim.

**2. Binomial probabilities — all recomputed exactly (independent).** P(X≥42|60,0.5)=0.001335 → cited 0.0013 ✓. P(X≤57|60,0.99)=0.02242 → cited 0.022 ✓. P(X≥41|60,0.5)=0.003109 → cited 0.0031 ✓. P(X≥33|60,0.5)=0.259479 → cited 0.259 ✓. P(X≤23|60,0.5)=0.04623 → cited 0.046 ✓. Auxiliary claims also exact: P(X≥59|60,0.98)=0.662 → cited 0.66 ✓; 2/50257≈3.98×10⁻⁵ → cited ~4×10⁻⁵ ✓. The statistical-license usages are correct: P(X≤57|60,0.99) is the ≥3-miss probability under near-perfection; the ≤33 KILL region is genuinely chance-consistent. The draft cites these as "the H6-signed values" and — correctly per defect class 1 — registers the executor's exact recomputation as operative, with the count regions (not the numbers) as the decision contract (§3.10).

**3. H6 apparatus carried verbatim; the 240-vs-180 deviation is justified and declared.** H6: 60 self-report + 120 option forwards = 180 (state side archived). H22: 60 premise-state L20 + 120 option + 60 self-report = 240. The justification — bench 4 has no archive, so H6 §3.2's archive form is replaced by fresh extractions per Law #13 — is stated identically in §0.3, §3.3, §3.9, §6, and §8.2, and matches the gate memo. Fidelity formula identical to H6 §2. Decision statistic identical to H6 §3.3 (premise-only state text, `" "+E` option texts, layer 20, cosine argmax, ties→E2, G4 spread gate at 1e-4) except fresh state extractions. Readout spec identical to H6 §3.4 (argmax over pinned ids at final position, ties→E2, zero generation). G1/G2 guards identical to H6 §3.5 (M≥0.01; ≥2 distinct with minority≥3). Backbone hash pin, environment, determinism pins identical to H6 §3.6.

**4. Single-token assertion discipline — mechanically verified.** All 21 entity names with token IDs in §3.2(a) verified against the real Pythia-410m snapshot tokenizer (`~/workspace/.exp086_weights/pythia-410m`, tokenizer-only): 21/21 single-token with matching ids (Heart [15382] … Dew [45797]). Matches the LOG-4674 gate-level evidence, which the draft cites without re-running — and the breaking point (a) correctly requires the construction lane to re-run the assertion on the **final** sets (tokenizer, `" "+E` encoding exactly per the H6 §3.3 pin, multi-token → construction restarted not patched). The `[-3:]` identity pin (§3.4) verified on the real tokenizer: `" Question: Who is higher in rank? Answer:"` ends in `[32, 37741, 27]` (`?`, `ĠAnswer`, `:`). The procedure is pinned precisely enough to execute. Every logit-apparatus statement carries the single-token pin — no gap.

**5. Template-decorrelation transfer (G-C1/G-C2/G-C3).** G-C1 (≤36/60) and G-C2 (|Pearson|≤0.10) transfer in diagnostic form — a deliberate, declared deviation (§8.3) justified by §3.8: no head is trained, no labels touch the apparatus, the carrier is byte-identical across items, so a template cue cannot inflate the readout-vs-decision agreement the metric measures. The thresholds mean the same *measurement* as in EXP107/EXP120; their *decision role* is downgraded to recorded-not-verdict-bearing, transparently. G-C3 (byte-exact decomposition) transfers in full — correctly so, since it protects the readout-region token identity. The registered per-cell descriptive diagnostic (§3.8) provides the observation channel for any template-shaped signature without letting it touch a verdict. Coherent.

**6. No cross-bench fidelity comparisons.** The unlicensed fence appears in §0.2, §0.5, §4, and §7.7 ("bench 4 stands alone; bench-1's 41/60 HELD stands either way"); §8.9 bars bench-1 re-reading (Law #9). No sentence compares bench-4 fidelity to bench-1's 41/60 beyond the HELD-band *prediction* (§0.5, §2) — the prediction is the licensed form, not a post-hoc comparison. Clean.

**7. H18's bench-2 line stays dead.** §1.1 explicitly bars the 36-item sub-bench rescue and any bench-2 rerun; §3.9 lists bench 2 under "Not reused"; §7.6 and §9 restate the line stays dead. All H18 mentions are referential (the apparatus-void precedent for asserting single-token at construction). No revival, no rescue language.

**8. Additional Law #14 sweeps.** Laws #4 (bars binding, no rescue runs, BARRED rewording), #6/#13 (Δθ=0 hash before/after all 240 forwards, seeds, threads, env), #7 (labels never touch the apparatus; own-label FIX-1 pin before pre-registration), #8/#11 (EXP112's bench-1 HELD restated, never re-adjudicated; two-layer tagging on KILL), #9 (metric registered, no bench-1 data), #12 (log chain) — all hold. Degrees-of-freedom table (§4.1) is complete and matches the method sections. Epistemological labels per SCBI/AGENTS.md §5 are applied throughout. Entity-domain disjointness from benches 1/2/3 is asserted by construction-lane set-membership check (bench-1 names enumerated; no overlap with body parts/weather).

## FIX-1 (launch-gating, verdict-immaterial)

**Location:** §3.5, the sentence: "Any per-item mass filtering is licensed **only at construction** (the builder's filtering discipline, if any, is a design contract documented before bench items are finalized); **no per-item screening occurs at execution.**"

**Defect:** This clause is in internal tension with §3.2's model-free construction discipline ("60 items built deterministically by the construction lane (**no model calls, no RNG**)"). A per-item mass measurement requires backbone contact — which construction forbids — so the allowance is either vacuous or, read permissively, opens a model-contact item-screening door at construction, exactly the post-hoc-screening class the EXP121 lesson bars. The run-level G1 guard itself is verbatim H6 and unaffected.

**Fix (one sentence, replace the parenthetical clause):** state explicitly that no per-item filtering of any kind occurs at construction or at execution — the construction lane makes no model calls (the single-token assertion is tokenizer-only), and the builder documents the absence of any item screening in the breaking-point certificate. Nothing else in §3.5 changes; the run-level G1 guard with its RUN-INVALID form stays exactly as signed.

**Gating:** launch-gating — must be fixed before the CEO briefs the construction lane, so the certificate cannot be read as licensing mass-based screening. Verdict-immaterial — no decision bar reads per-item filtering; all bars in §4 are unchanged.

## Observation (not a fix)

§0.6(b) cites "(the honesty metric cannot read them — H6 §3.8)" — H6 §3.8's literal content is the template posture with the per-cell diagnostic changing no verdict "because there is no trained artifact to reclassify." The substance supports the claim (no trained artifact, no labels → template cues cannot move the metric), so the citation is adequate as shorthand; no change required.

## Sign-off

Verdict: **SIGN-WITH-FIXES.** Apply FIX-1 (one sentence in §3.5), verify the fix byte-level (fix-verification lane), then the draft is launch-ready. No other change licensed.
