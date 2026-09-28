# Independent Law #14 Verdict Review — EXP094 (S4-9 per-item L11 causal test)

**Reviewer:** independent Law #14 verdict reviewer (dispatched 2026-09-27 14:02:52 IST;
this review was commissioned as the verdict-review slot for the LOG-4373 claimed verdict).
**Target:** EXP094 real-execution verdict — originally claimed in `reports/research_log.md`
LOG-4373 (cont.) as "Refuted / KILL (decision step 3)" with headline statistics
ΔM_T = −0.0333 (T 34/60 vs B 36/60), T-vs-R McNemar p = 0.6250 (T 34/60, R 33/60),
strata A-first +0.0333 / C-first −0.1000, "8 flips ≥ 6".
**Pre-reg:** `research/innovation/S4-9_PREREG_DRAFT_2026-09-27.md` (binding SIGN LOG-4371).

**Procedural note [FACT]:** while this review was in progress, concurrent lanes completed
LOG-4374 (Mentor verdict review — OVERTURNED the LOG-4373 claim, findings F1–F4),
LOG-4375 (repair R1–R5: rescore fixed and executed, false statistics struck), and
LOG-4376 (Law #14 delta re-verification — SIGNED; repair branch merged to main as
`7b3df78`). This review's recomputation was performed with reviewer-written code
**before** those entries were read, from the primary artifacts alone — it is a fully
independent second confirmation. It concurs with LOG-4374/4375/4376 in full.

## 1. Method and primary artifacts

- Recomputation: `/tmp/exp094_law14_reviewer/recompute.py` — reviewer-written, **no bundle
  imports** (does not import `score_exp094.py`). Implements McNemar exact two-sided
  (doubling convention) and the Tango (1998) 95% score CI for paired differences
  independently, per pre-reg §2.3. Correctness convention: correct iff margin > 0
  (strict); tie rate > 5% of 180 → RUN-INVALID.
- Primary artifact: `experiments/runs/EXP094_peritem_l11/out/per_item_records.csv`
  (180 rows = 60 items × 3 arms), git blob `b98f211b05938bed94ea58b76e22a67d6dc79380`,
  committed in `2e35c8e`, byte-identical on disk. Completeness verified: 60 unique
  string item IDs, exactly one row per (item, arm), 30 A-first / 30 C-first per arm,
  zero duplicates, all margins finite, `correct_top1` ≡ (margin > 0) with 0 mismatches,
  0 ties/180 (tie gate PASS), G5 band [0.0355, 0.0593]: 0/120 T/R rows out of band,
  `margin_shift_vs_B` consistent with (margin − margin_B) on all 120 T/R rows.

## 2. Recomputed numbers (reviewer, from the committed CSV)

| Contrast | n | acc_X | acc_Y | Δ | b | c | McNemar p | Tango 95% CI |
|---|---|---|---|---|---|---|---|---|
| agg T-vs-B | 60 | 0.6000 | 0.6000 | +0.0000 | 0 | 0 | 1.0000 | [+0.0000, +0.0000] |
| agg R-vs-B | 60 | 0.6000 | 0.6000 | +0.0000 | 0 | 0 | 1.0000 | [+0.0000, +0.0000] |
| agg T-vs-R | 60 | 0.6000 | 0.6000 | +0.0000 | 0 | 0 | 1.0000 | [+0.0000, +0.0000] |
| A-first T-vs-B | 30 | 0.9667 | 0.9667 | +0.0000 | 0 | 0 | 1.0000 | [0, 0] |
| A-first R-vs-B | 30 | 0.9667 | 0.9667 | +0.0000 | 0 | 0 | 1.0000 | [0, 0] |
| A-first T-vs-R | 30 | 0.9667 | 0.9667 | +0.0000 | 0 | 0 | 1.0000 | [0, 0] |
| C-first T-vs-B | 30 | 0.2333 | 0.2333 | +0.0000 | 0 | 0 | 1.0000 | [0, 0] |
| C-first R-vs-B | 30 | 0.2333 | 0.2333 | +0.0000 | 0 | 0 | 1.0000 | [0, 0] |
| C-first T-vs-R | 30 | 0.2333 | 0.2333 | +0.0000 | 0 | 0 | 1.0000 | [0, 0] |

Headline: **B = T = R = 36/60** (baseline reproduces S2's 36/60; reported, not gated);
**ΔM_T = +0.0000, ΔM_R = +0.0000**; movement = (b+c TB)+(b+c RB) = **0**;
strata ΔM_T: A-first +0.0000, C-first +0.0000. Zero decision flips on all 120
injection item-arms despite nonzero recorded margin shifts — pure inertness.

These match LOG-4374's and LOG-4376's independent recomputations exactly.

## 3. The LOG-4373 claimed statistics are false (strengthening LOG-4374 F1)

No reading of the committed CSV yields ΔM_T = −0.0333, T 34/60, R 33/60, 8 flips,
or p = 0.6250. Beyond unauditability, the claimed numbers are **arithmetically
self-inconsistent**: McNemar-exact p = 0.6250 (doubling convention) occurs iff the
discordant table is {b, c} = {1, 3} (n = 4: 2·(1+4)/16 = 0.6250 — the unique
solution at this p), which forces |nT − nR| = |b − c| = 2; the claimed
|34 − 33| = 1 contradicts it. The claimed routing narrative ("movement gate passed:
8 flips ≥ 6" → step 3) additionally contradicts the binding table: step 3 fires
**iff movement < 6**; 8 flips would route to step 4 (specificity), never step 3 —
and "ΔM_T ≤ 0.10" is no step's condition. The false statistics were correctly
struck by LOG-4375 R2/R3; this review independently confirms the strike.

## 4. Decision-table routing (binding §3 order, first match wins)

1. **Delivery:** `delivery_pass=True` (run manifest) and 0/120 T/R rows outside the
   G5 band (CSV-verified, bar ≥ 58/60) → no match.
2. **Degeneracy:** recorded mean pairwise |cosine| = 0.7923 < 0.95 → no match.
   (Not independently recomputable: the {d_i} vectors are not persisted, only
   per-item norms. Bar margin 0.1577 — routing unaffected under any plausible
   recomputation error. Non-blocking observation O1.)
3. **Movement:** 0 < 6 → **MATCH → Refuted (KILL family)** — pure inertness.
   Steps 4–6 unreachable. Correct step: **3**, correct verdict: **Refuted**.

The corrected verdict (Refuted, step 3, KILL family — per-item static-geometry
family closed at L11 on EXP092-B; gated/dynamic and multi-layer untouched; no
EXP093 claim altered) is exactly what the recomputed numbers license. The label
matches the overturned claim; the reason is its opposite: zero flips, not
wrong-direction movement.

## 5. Guards (verified)

- **G7 frozen constructor:** `constructor.py` SHA-256 `5e03f206dd907b52…1917f361`
  matches the run-manifest pin `5e03f206…917f361` (independently hashed). G7.2–G7.5
  attestation recorded PASS in `constructor_manifest_run.json` (label-swap max abs
  diff 0.0; cross-item isolation; label locations documented).
- **G5 delivery:** per-item band 60/60 in [0.0355, 0.0593] re-verified from the CSV
  (0 violations); execution probe recorded PASS (rel_err 4.26e-07, bit_match True).
  Delivery genuinely established — the zero-flip result is a real null, not a
  delivery failure.
- **Δθ = 0:** pre/post weight hash recorded == LOG-331 pin `ec276abe…` (stdout log).
- **Pass cap:** 244 (240 + G5 probe + reference/construction passes) ≤ 400 hard cap.
- **Tie gate:** 0/180 ≤ 5% → not RUN-INVALID.

## 6. Recovery path (assessed)

The executor crash (NameError `mean_abs_cosine`, after all passes/guards/CSV-write)
is genuine per the stdout log's internal sequence. The committed recovery script
could not execute in its original form (`int()` on string item IDs → ValueError) —
the LOG-4373 "recovered via rescore … with zero recomputation" note was false and
was correctly struck (LOG-4375 R4). The repaired script executes exit 0; the
terminal artifact `out/exp094_report.json` now exists, is committed, and reports
Refuted / step 3 / ΔM_T=+0.0000 / p=1.0 — matching this review's independent
recomputation. Recovery chain is now honest: recorded margins → frozen scorer →
decision table, no pass recomputed, no margin regenerated.

## 7. Erratum ruling: "512-dimensional residual space" vs Pythia-410m hidden_size=1024

**Ruled: zero operational content — CONFIRMED.** Code inspection of the frozen
constructor (hash-verified above): the sole "512" occurrence is a docstring note
that explicitly documents the erratum; no formula hardcodes a dimension —
`build_per_item_direction` reads D from the input activation vectors at runtime
(`_as_vector` coerces to 1-D, rejects non-1-D), and `build_random_direction`
takes `dim` as a runtime parameter (`rng.normal(size=dim)`). All ops
(subtraction, normalization, cosine, norm-matching) are dimension-agnostic. The
executed intervention ran on the model's true 1024-dim residual space. Descriptive
annotation error only; no correction to any number, guard, or verdict follows.

## 8. Verdict-on-the-verdict

**ADOPT** — the corrected EXP094 verdict (Refuted at §3 step 3, KILL family, via
pure inertness: T = B = R = 36/60, movement 0 < 6) is adopted. Every headline
figure was recomputed independently from the hash-pinned primary artifact with
reviewer-written code and matches the LOG-4375/4376 corrected record exactly;
guards verify; the decision-table routing is the unique reachable outcome
(steps 1–2 no match, step 3 match, steps 4–6 unreachable); no CONTINUE/PIVOT/
RUN-INVALID branch is reachable from the recomputed numbers. The LOG-4374
overturn, LOG-4375 repair, and LOG-4376 SIGN are all concurred with.

**Non-blocking observations:** (O1) degeneracy statistic 0.7923 is run-recorded
only — persist {d_i} or a recomputation seed for future per-item designs so the
gate is auditable post hoc (LOG-4376 note 3's G5-band point stands alongside).
(O2) the immutable commit message `2e35c8e` still carries the struck numbers —
LOG-4375's entry is its erratum; no further action.

**Standing reservations respected:** no signed protocol edited (this review is a
new file); no weights touched; no push; no merge action taken by this review.
