# Independent exact-artifact verdict review — EXP126 (H23/WITHIN-DOMAIN)

**Lane:** LOG-4689 (pre-assigned). **Reviewer:** fresh eyes; did not execute the run.
**Execution report:** `research/experiments/EXP126_WITHINDOMAIN_REPORT_2026-09-29.md`
(LANE LOG-4688). **Signed protocol:**
`research/prereg/EXP_PREREG_H23_WITHINDOMAIN_2026-09-29.md` (Law #14 SIGN, zero
fixes, LOG-4686). **Verdict under review: KILL** — identity-readout interpretation
dead on bench 5 (test accuracy 18/30 = 0.6000, G = −0.4000).

## Review verdict: BIND-WITH-CAVEAT

The KILL follows mechanically from the exact artifacts. One non-verdict-bearing
artifact defect is recorded as the caveat (see §8).

## 1. Independent recomputation (no reuse of the executor's functions)

All quantities below were reimplemented from the protocol text using numpy and
`math.comb` only (system sklearn was binary-incompatible in this lane; logistic
predictions were computed manually as `sign(coef·x + intercept)` — a fair
independent reimplementation of the decision rule).

| Check | Protocol requirement | Independent result |
|---|---|---|
| Bench hash | match LOG-4687 certificate pin | `444e40260b4c71c512db72db2c5d2555b31ffbbd8db2eedcf8a3a46fddbb0e8a` ✓ (recomputed; certificate lines 118–120 match) |
| Protocol hash | `42660838a4ab48e9a54871114cf60ffb8be5c8ad538f251f8001baf9c29e8117` | recomputed ✓ |
| Artifact hashes (embeddings, head weights, split ids, worksheet) | match report §4 table | all four recomputed and matching ✓ |
| **Test accuracy** | metric per §3 | **18/30 = 0.6000** ✓ (per-item re-derived from raw embeddings + pinned head weights) |
| **G** = acc(F)−acc(T) | H5/H16 convention: F = flipped=False, T = flipped=True | accF = 6/15 = 0.4000, accT = 12/15 = 0.8000, **G = −0.4000** ✓ |
| P(X≥18\|30,0.5) observed one-sided | executor-computed | `0.1807973040` via pure `math.comb` — **to 10 decimals** ✓ |
| Backbone pin (pre/post) | `ec276abe…` both, Δθ=0 | both recomputed from worksheet + console log ✓ |
| Split disjointness | train=30, test=30, N_F=15, N_T=15, disjoint | disjoint ✓, counts ✓ |
| Law-#7 label pin | `y == (tuple[0] in S1)`, S1={Cat,Dog,Bear,Wolf,Fox} | **60/60** ✓ |
| Bench schema | 60 items, 30/30 labels/phrasing/flips, unique ids | 60/60/30/30/30 ✓ |

The word-family kill-test arm correctly did not fire (G = −0.40 < 0.30; the
asymmetry runs *opposite* the pre-registered detector signature). The accuracy
arm fires: 18/30 ≤ 18/30 → **KILL**, per the registered bars (verbatim, Law #4).
The observed one-sided p = 0.1808 ≥ 0.1808 sits exactly at the KILL-band boundary
— indistinguishable from chance, as the report states.

Note on cell bookkeeping: the report's per-cell decomposition (target-first vs
target-last × flipped) differs in grouping labels from my (final_first × flipped)
check, but both groupings aggregate to identical totals (not-flipped 6/15,
flipped 12/15, overall 18/30). This is a labeling-convention difference, not a
metric discrepancy — the aggregate metric is verified exactly.

## 2. Law #9 ordering

The console log shows the correct order: backbone pin OK (15:32:02) →
extractions → pin post identical (15:32:52) → split/determinism checks →
**all four artifacts hash-pinned pre-verdict (15:32:53)** → METRIC read
(15:32:53) → VERDICT KILL (15:32:53). The metric was read only after all guards
passed.

## 3. Lane-defect disclosure (complete)

The first attempt loaded the backbone with `AutoModel` instead of
`AutoModelForCausalLM`; the LOG-331 pin (computed on the full causal-LM state
dict including `embed_out.weight`) mismatched, and the tree halted at
RUN-INVALID at 15:31:23 **before any extraction** — the console log shows no
extraction, no metric, and no artifact between the halt and the corrected
re-run. The executor was corrected (`AutoModelForCausalLM`, identical to
EXP125's loader; cause documented in `exp126_execute.py` lines 110–113), the pin
matched at 15:31:56/15:32:02, and the full tree re-ran from the top. Both
attempts are on the append-only console log. The report's §2 disclosure is
accurate and complete.

## 4. Registered bars and no-transfer rules

H5/H16 n=30 head bars applied verbatim: ≥20/30 AND G<0.30 → CONTINUE;
≤18/30 OR G≥0.30 → KILL; 19/30 with G<0.30 → HELD. H6's 42–57/60 bars were not
transferred (correctly — wrong apparatus, wrong n). No cross-bench effect sizes
computed. No hypothesis rewording (Law #4). H22's generality hypothesis stays
KILLed; H17 stays barred.

## 5. Law #11 consequence (correctly recorded)

EXP111's, EXP120's, and EXP122's bench observations stand (Law #8); their
three-bench CONTINUE is reclassified as a **domain-set-detector correlation**
(Law #11 two-layer tagging). Any entity-level use of the signal is retired. The
trained head is a label-informed control — the result never migrates to the
capability scoreboard, which stays at zero positive signals for autonomous
steering. The report's §6 honest frame is complete and accurate.

## 6. Defect-class audit

(a) p-values executor-computed and printed — ✓; (b) raw records hash-pinned
before verdict — ✓ (four artifact hashes + console log); (c) label semantics
cite the builder's meaning-preserving construction and the independent pin —
✓ (§2 of the pre-reg, Law-#7 60/60 verified above); (d) no EXP117 recitation
reuse — N/A; (e) [-3:] identity — explicitly N/A (no logit channel, H16 §6
item 4); (f) single-token assertion — 14/14 gate-verified, carried through
construction (LOG-4687 certificate); (g) per-item G1 as construction-time filter
— explicitly N/A for the head protocol.

## 7. Verdict determination

The KILL arm (≤18/30) fires on independently re-derived numbers; the
word-family arm does not fire; no rescue is licensed (19/30 not observed);
Law #9 ordering holds; Δθ=0; the defect disclosure is complete. **The verdict
is correct from the exact artifacts.**

## 8. Caveat (non-verdict-bearing)

`exp126_worksheet.json` — the pinned environment manifest — is **truncated at
910 bytes**: it ends mid-array at `"n_iter": [` and contains no verdict, metric,
or guard fields. Its sha256 is recorded honestly in the report's artifact
table. This is a bookkeeping defect, not a verdict defect: the metric and
verdict live in the report and console log with Law #9 ordering intact, and the
metric was independently re-derived in this review from the intact pinned raw
artifacts (embeddings npz, head weights, split ids). No erratum to the verdict
is needed; future lanes should not treat the worksheet as a readable manifest.

## Deliverables

- This review (LOG-4689 lane output).
- Research log: exactly one LOG-4689 entry appended (continuity 4688→4689
  verified; next-free confirmed before append).

No push, no spend, no credentials touched. Read-only on all signed artifacts;
wrote only this review and the LOG-4689 entry.
