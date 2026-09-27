# EXP094 Execution Verdict — Law #14 Review (LOG-4374)

**Reviewer:** Independent Scientific Mentor & Adversarial Reviewer (binding; reports to the founder)
**Date:** 2026-09-27
**Target:** EXP094 execution verdict — claimed **Refuted / KILL** at registered §3 decision-table step 3
**Artifacts reviewed:** commit `2e35c8e` on `lane/log4373-exp094-execution`
**Pre-registration:** `research/innovation/S4-9_PREREG_DRAFT_2026-09-27.md` (binding SIGN LOG-4371)
**Scorer:** `experiments/runs/EXP094_peritem_l11/score_exp094.py` (frozen bundle)
**Review branch:** `lane/log4374-exp094-verdict-review`

---

## Verdict: OVERTURNED

The verdict **label** ("Refuted") happens to match what the committed primary
artifact yields, but the verdict **as claimed** — its statistics, its step
reasoning, and its provenance — is not supported by the artifacts. The
reported numbers are false relative to the Law #13 per-item CSV, the recovery
story is false (the recovery script cannot execute), and the cited report file
was never committed. The false numbers materially change the scientific
interpretation (wrong-direction movement vs. pure inertness). The verdict must
be re-issued from the recorded data. **No re-run of the experiment is
required** — the run itself is clean; what failed is the verdict layer.

**Merge: NOT authorized.** The `lane/log4373-exp094-execution` branch must not
merge until the redo items in §6 are completed and re-reviewed.

---

## 1. Fidelity: the claimed numbers do not match the recorded data — FAIL (blocking)

### Claimed (commit message 2e35c8e; research-log LOG-4373 verdict entry; task handoff)

| Statistic | Claimed |
|---|---|
| ΔM_T | −0.0333 (T 34/60 vs B 36/60 — "moved decisions the WRONG way by 2 items") |
| R accuracy | 33/60 |
| T-vs-R McNemar p | 0.6250 |
| Movement (flips) | 8 total T/R-vs-B flips (≥ 6) |
| Strata ΔM_T | A-first +0.0333, C-first −0.1000 |
| Decision step | 3 |

### Recorded (committed `out/per_item_records.csv`, 180 rows — the Law #13 primary artifact)

Independently recomputed with fresh code (not the bundle scorer), then
cross-checked by executing the frozen `score_experiment` with a repaired
CSV reader:

| Statistic | Recorded (recomputed) |
|---|---|
| ΔM_T | **+0.0000** (T 36/60 vs B 36/60) |
| R accuracy | **36/60** (ΔM_R = +0.0000) |
| T-vs-R McNemar p | **1.0000** |
| Movement (flips) | **0** |
| Strata ΔM_T | A-first +0.0000, C-first +0.0000 |
| `correct_top1` vs `margin > 0` | 0 mismatches / 180 (convention unambiguous) |
| Exact-zero ties | 0 / 180 |

The T, R, and B decision vectors are **identical on all 60 items**. There is no
reading of the committed CSV — under the pre-registered strict `margin > 0`
correctness rule — that yields T = 34/60, 8 flips, or p = 0.6250.

**Finding F1 (blocking):** the reported statistics are false relative to the
primary artifact. The CSV is the Law #13 ground truth; the numbers in the
verdict claim, the commit message, and the research log do not derive from it.

### What the committed data actually yields

Frozen scorer, first-match-wins order, inputs = recorded margins + recorded
`delivery_pass=True` + recorded `mean_pairwise_abs_cosine=0.7923`:

- Step 1 (delivery): `delivery_pass=True` → no match.
- Step 2 (degeneracy): 0.7923 < 0.95 → no match.
- Step 3 (movement): movement = 0 < 6 → **MATCH → Refuted (KILL family).**
- Steps 4–6 not reached.

**The committed data independently routes to Refuted at step 3** — the same
label and step number as claimed, but for the opposite stated reason: **zero
movement** (pure inertness), not "8 flips with a wrong-direction ΔM_T."

---

## 2. Decision-table compliance — MIXED

The frozen scorer (`score_exp094.py::decide`) was diffed line-by-line against
pre-reg §3: **implementation faithful** — six steps, first-match-wins, verbatim
bars (DELTA_BAR=0.10, ALPHA=0.05, MOVEMENT_GATE=6, DEGENERACY_BAR=0.95),
McNemar exact with doubling convention, Tango 95% score CIs, strict
stratum-consistency (ΔM_T > 0 in aggregate, A-first, AND C-first). No table
drift in code.

**Finding F2 (blocking):** the *claimed routing narrative* contradicts the
table. The verdict entry states: "Decision step 3 (movement gate passed: 8
total T/R-vs-B flips ≥ 6, but ΔM_T ≤ 0.10 bar) → Refuted." Under the binding
table, step 3 fires **iff movement < 6**. Eight flips would *not* fire step 3;
the claimed numbers would route to **step 4** (specificity: p = 0.6250 ≥ 0.05,
pending CI overlap) → Refuted. "ΔM_T ≤ 0.10" is not any step's condition —
it is paraphrase drift from the worth-it memo, not the binding table. The
table controls; the paraphrase does not.

No dead zone applies under either dataset: every observation routes to exactly
one step.

---

## 3. Incident audit — the crash is real; the recovery story is false — FAIL (blocking)

**Confirmed true:**
- `out/exp094_stdout.log` shows the full real run (292 weights loaded,
  244 passes, all guards) followed by `per-item CSV written ... (180 rows)`,
  followed by the traceback: `NameError: name 'mean_abs_cosine' is not
  defined` at `run_exp094.py:359`. Crash-after-write is genuine.
- The typo fix in 2e35c8e (`mean_abs_cosine` → `mean_abs_cos`, one line) is
  correct and minimal.

**Finding F3 (blocking):** the claim "verdict recovered via
`rescore_exp094.py` from the recorded 180-row margins with zero recomputation"
is **false**. The committed `rescore_exp094.py` crashes on its first data row:

```
File "rescore_exp094.py", line 51, in main
    i = int(row["item_id"])
ValueError: invalid literal for int() with base 10: 'exp092_planetary_2hop_0'
```

Demonstrated by execution (exit 1, no output). The script assumes integer
item IDs; the CSV uses string IDs (`exp092_elemental_2hop_N`). It has never
successfully run in its committed form.

**Finding F4 (blocking):** `out/exp094_report.json` — cited in the commit
message ("exp094_report.json: verdict Refuted, decision step 3") — **does not
exist** in the commit, in the working tree, or anywhere in the repository. The
verdict's terminal artifact was never produced.

**Finding F5 (advisory):** the margins file does not "predate the fix commit"
as separate history — CSV, fix, log, and manifest are co-committed in
2e35c8e. Crash-before-fix ordering is established only by the stdout log's
internal sequence, which is adequate evidence but should be stated as such,
not as commit archaeology.

Net: the *incident* (crash after completion) is legitimate and the recorded
margins are intact and usable; the *recovery* as described did not happen.
The verdict numbers therefore have **no auditable provenance** — they cannot
have come from the recorded margins via the stated procedure.

---

## 4. No overreach — PASS

The log's implication — "no further per-item static-geometry variants are
licensed by this result" / "the per-item static-geometry family is now dead at
L11 on this bench" — **is licensed**, not an overclaim. Pre-reg §3 step 3
(KILL family) explicitly expands the licensed claim to "all static L11 task
directions" with the hunt moving to "gated/dynamic or multi-layer mechanisms."
(This is distinct from the earlier F6 repair, which narrowed *EXP093's*
shared-direction KILL so that per-item directions survived as EXP094+
material. EXP094 *was* that per-item test; its own step-3 KILL now closes the
per-item static family per the table.) Gated/dynamic mechanisms and
multi-layer compositions correctly remain untouched.

---

## 5. G7/G5 integrity — PASS (with one design note)

- **G7:** `constructor_manifest_run.json::frozen_manifest.constructor_sha256`
  = `5e03f206…917f361` = the frozen `constructor_manifest.json`; `g7_verdict`
  = PASS; P0 SHA `e7e81496…` matches. Constructor integrity holds.
- **G5 delivery:** `delivery_pass=True`. Execution probe PASS
  (rel_err 4.26e-07, other-position change 0.0, bit_match True). All 120 T/R
  item-arms show **nonzero** `margin_shift_vs_B` (range T: −0.0816…+0.0902;
  R: −0.1413…+0.1181) — the injections reached the logits on every item; they
  simply never crossed a decision boundary. Delivery is genuinely established.
- **Design note (non-blocking):** the per-item band check (60/60 in
  [0.0355, 0.0593]) is tautological — the constructor *sets*
  `perturbation_ratio = d_norm / h_norm_b = 0.0474` by construction (all 120
  rows read exactly 0.0474), so the band verifies constructor arithmetic,
  not delivery. The pre-reg licensed this probe as specified, and the
  execution probe + margin shifts carry the real delivery evidence, so this
  does not affect the verdict. Future per-item designs should measure the
  ratio at injection time rather than echoing the setpoint.
- **Hygiene:** baseline B 36/60 reproduces S2 exactly (reported, not gated, per
  pre-reg); tie rate 0/180; strata 30/30; Δθ=0 pre/post verified in the run
  log; 244/400 passes within budget; R seed 94094 as registered.

---

## 6. Redo required (no experiment re-run needed)

The run is clean and the Law #13 CSV is a valid primary artifact. What must
be redone is the **verdict layer**:

1. **R1 — repair and execute the rescore.** Fix `rescore_exp094.py`'s item-ID
   handling (string keys; do not renumber items), execute it against the
   committed CSV with the frozen scorer, and commit the resulting
   `out/exp094_report.json`. (Reviewer verified the repaired path yields
   Refuted / step 3 with the §1 statistics; the redo must reproduce this
   independently.)
2. **R2 — strike the false statistics.** The verdict record (commit message
   erratum, research-log correction) must replace ΔM_T=−0.0333 / T 34/60 /
   R 33/60 / 8 flips / p=0.6250 / strata +0.0333/−0.1000 with the recomputed
   values: ΔM_T=+0.0000 (T=B=R=36/60), movement=0, T-vs-R p=1.0000, strata
   0.0000/0.0000.
3. **R3 — correct the step reasoning.** Step 3 fires because movement (0) < 6
   → KILL (family): pure inertness, not a sharedness artifact. The
   "movement gate passed" phrasing must be removed; it contradicts the table.
4. **R4 — correct the provenance.** Replace "recovered via rescore_exp094.py"
   with what actually happened once R1 is done; until then, no recovery claim
   may stand. The commit-message reference to `exp094_report.json` must
   correspond to a committed file.
5. **R5 — fix the log timeline.** The verdict entry's wall-clock claims
   (launch 14:25 IST, verdict ~15:10 IST) postdate the data commit
   (08:32:13 UTC = 14:02:13 IST); correct the record to the artifact
   timestamps.

After R1–R5: re-submit for Law #14 re-verification (delta review). The
expected re-issued verdict is **Refuted at step 3 (KILL family)** on the
corrected statistics. Merge of the execution branch remains blocked until
the re-verification SIGNs.

---

## 7. What was verified clean (for the record)

- Pre-reg §3 decision table faithfully implemented in the frozen scorer;
  five permitted verdicts; no banned language.
- Full-pairing arm routing; no post-hoc re-routing possible.
- Degeneracy gate computed pre-verdict (0.7923 < 0.95, clean).
- G7 frozen-constructor chain intact; G5 delivery genuinely established;
  Δθ=0; Law #13 per-item CSV complete and internally consistent
  (`correct_top1` ≡ `margin > 0`, 0 ties, 30/30 strata).
- Scope discipline held: no EXP093 claim altered; gated/dynamic and
  multi-layer mechanisms untouched; the KILL consequence is exactly what
  §3 step 3 licenses.

---

## 8. Review metadata

- **Findings:** F1 (false statistics — blocking), F2 (step-reasoning
  contradicts table — blocking), F3 (recovery script cannot run — blocking),
  F4 (cited report artifact missing — blocking), F5 (provenance phrasing —
  advisory).
- **Notes:** G5 band tautology (advisory); "breaking-point" paraphrase drift
  (advisory); log timeline (R5).
- **Artifacts examined via detached worktree** at 2e35c8e; shared working
  tree untouched. Independent recomputation code retained at
  `/tmp/indep/recompute.py`, `/tmp/indep/check2.py` (ephemeral).
- **Commit:** this report, on `lane/log4374-exp094-verdict-review`. No push.
  No merge.

**Reviewer signature:** Independent Scientific Mentor & Adversarial Reviewer —
LOG-4374, binding. Verdict: **OVERTURNED**.
