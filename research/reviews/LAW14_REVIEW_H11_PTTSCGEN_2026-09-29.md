# Law #14 Review — H11 (PTTSC-GEN) Pre-registration (LOG-4607)

**Artifact reviewed:** `research/prereg/EXP_PREREG_H11_PTTSCGEN_2026-09-29.md` (the exact file; no other version)
**Review lane:** LOG-4607 (pre-assigned). Independent of the LOG-4606 drafting lane. $0 CPU. Read-only everywhere except this review and the log append.
**Sources cross-checked:** `research/prereg/EXP_PREREG_H4_PTTSC_2026-09-29.md`, `research/prereg/EXP_PREREG_H7_EVALID_2026-09-29.md`, `research/experiments/EXP109_PTTSC_REPORT_2026-09-29.md`, `research/experiments/EXP113_EVALID_REPORT_2026-09-29.md` (full text), `research/experiments/EXP115_HDIGEN_REPORT_2026-09-29.md`, `research/experiments/EXP116_HDIPRIM_REPORT_2026-09-29.md` (full text), and the EXP091 bench builder `experiments/runs/EXP089_clm8b_falsifier/benchmark_exp089.py` (executed to verify builder claims).

## Verdict: SIGN-WITH-FIXES

One documentation-precision fix is required before launch. No design flaw was found; the protocol (§3.3 remains the binding spec) is unaffected.

---

## 1. Bars/numbers — all verified from first principles

Every §4 McNemar one-sided exact p-value recomputed independently (p = P(X ≥ b | n=b+c, 0.5)):

| (b, c) | draft p | recomputed | verdict use |
|---|---|---|---|
| (5, 0) | 0.03125 | 1/32 = 0.03125 | ✓ CONTINUE |
| (4, 0) | 0.0625 | 1/16 = 0.0625 | ✓ HELD |
| (6, 0) | 0.015625 | 1/64 = 0.015625 | ✓ |
| (6, 1) | 0.0625 | 8/128 = 0.0625 | ✓ HELD |
| (7, 1) | 0.03515625 | 9/256 = 0.03515625 | ✓ |
| (9, 2) | 0.03271484375 | 67/2048 = 0.0327148… | ✓ |
| (8, 3) | 0.11328125 | 232/2048 = 0.11328125 | ✓ HELD |

Region tiling is complete: p ≤ 0.05 ∧ b > c → CONTINUE; net ≤ 0 → KILL; net > 0 ∧ p > 0.05 → HELD — no gaps, no overlaps, no razor-thin CONTINUE (the (4,0) and (6,1) net-+5 cases are correctly HELD, not CONTINUE). The table's asymmetry (net +5 insufficient at n=7 but sufficient at n=5) is the mathematically correct consequence of the exact test.

## 2. Phase-0 gates

- **0a recitation rule is mechanically decidable:** "an outline recites iff it exactly equals (after strip + casefold) one of the 4 pinned exemplar OUTLINES; an item is recited iff ≥2 of its outlines recite; ≥6/10 → RUN-INVALID." Pinned exemplars, pinned criterion, pinned threshold — no judgment call remains. ✓
- **The recitation-rationale is sound:** EXP115 demonstrated verbatim exemplar recitation passes a mechanical parse rule; EXP113's T2-P2 60/60 clearance was mechanical-parse only (the T2 parse rule requires ≥2 distinct non-empty outlines; four verbatim-recited exemplars yield four distinct outlines after dedup — verbatim recitation *passes* EXP113's clearance rule). The gate tests a real, documented blind spot. ✓
- **0b numbers are honestly calibrated:** the three cited priors are accurate against the reports (EXP109: 80/80 sampled baseline unparseable; EXP115: 38/60 unparseable under greedy few-shot; EXP116: 37/60 unparseable under greedy priming). The <8/10-parseable and variation-guard (<2 distinct entities, minority <2) thresholds are operational gates, disclosed as such — no false p-value license is claimed for Phase 0. ✓
- **48/60 full-run gate matches EXP113's 80% clearance threshold** (EXP113 report "Registered verdict": T1-CLEAR/T2-CLEAR defined at ≥48/60). ✓
- **Paraphrase-recitation blind spot is honestly disclosed** (§3.7: "the exact-match criterion is conservative by design — paraphrase-recitation is reported as a diagnostic (mean max token-overlap vs exemplars) but does not fire the gate; this limitation is disclosed"). ✓

## 3. Central honesty fence (§3.9 / §7.1) — airtight

The matched-budget framing is dropped *and the draft says why in one sentence* (greedy has no sampling variation to match — verified against H4 §3.7, which pinned identical sampling specs as the basis of its matched-budget design). The pipeline-vs-baseline comparison carries a disclosed ~2.7× token asymmetry (60×≤160 + 240×≤16 vs 60×≤16 — arithmetic verified: ≤14,400 tokens total, matching the §6 cost estimate). §7.1 explicitly unlicenses planning-vs-compute attribution ("a CONTINUE licenses the plan-conditioned **pipeline** as an adaptive-loop component — it does **not** license the claim that *planning* (vs additional compute, vs outline text as extra context) caused the gain"). The CONTINUE consequence in §2 ("the planner-executor pattern enters the EXP068-family adaptive-loop designs as a registered component") is consistent with §7.1 — it claims a component pattern, not planning capability. No claim in the draft lets a CONTINUE be read as planning capability. The foil tie-break (bias toward the foil = conservative against CONTINUE) is preserved from H4 §3.6. ✓

## 4. Deviations — one omission found (the fix)

§8's claim of completeness was swept against the body. Nine of the ten listed items are genuine, and the H7 "no change" item (10) was verified byte-level: H11 §3.3's TAIL, OUTLINES, block(i) construction, exemplar items (3, 4), and generation spec are byte-identical to H7 §3.3 T2-P2 (cross-checked against EXP113's honest note 3 — the same construction `{PROMPT_i}\n\n` + TAIL + `\n` + OUTLINES, `\n\n`-joined). The byte-verification check against `exp113_raw.json` is operationally pinned (reference path + mismatch → RUN-INVALID), not aspirational. The H4 §1.1 claims (greedy planner 160 tokens; temperature=0.7/top_p=0.9 executor/baseline; 4 baseline samples; matched budget; n=20 pilot; 20−n_valid ≥ 3 gate; LOG-4547→4552 chain) were all verified verbatim against H4's pre-reg and the log.

**The omission (FIX-1):** H4's arm/item-validity rule is not the same as H11's, and §8 does not record the change. H4 §3.8: "Item valid iff planner arm valid AND executor arm valid AND baseline arm valid", where H4 §3.5 pins "an item's arm is valid iff it has **≥ 3 parseable votes**" (4 executor + 4 baseline generations per item). H11 §3.8: item valid iff planner-valid (§3.3) AND **≥2 executor votes parseable** AND **baseline parseable**. With H11's generation counts (2–4 executor developments, 1 baseline), H4's ≥3-of-4 per-arm rule is arithmetically impossible — so the threshold change is a *forced* consequence of adaptations 2 and 4 — but it is a real spec difference (the executor-arm floor moves from ≥3 to ≥2, the baseline-arm floor from ≥3/4 to 1/1), and the §8 completeness claim is broken by its absence.

## 5. Worth-it gate (§0) — PASS stands

The key challenge resolves as the draft argues: EXP109's RUN-INVALID (n_valid=0/20, verified against the EXP109 report) means the planning hypothesis was never tested — the report's own §5 says so ("not evidence about planning", "a future planner-executor test would be a separate pre-registered lane"). EXP113's CONTINUE licensed exactly this lane ("H4-revival lanes licensable as NEW hypotheses, each with the named clearing protocol and its own elicitation-failure gate"). H11 is not a re-run: both arms' apparatus differ (T2-P2 planner vs dead T2-P1; greedy priming slot vs sampled regime), and the two binding unknowns are front-loaded into cheap Phase-0 gates rather than assumed. The §6 breaking point explicitly names REJECT as a legitimate review outcome, which is the honest framing. The gate stands.

## 6. Laws #4/#7/#9/#13

- **#4:** bars binding; "Any hypothesis rewording after seeing outputs → BARRED. Scientific misconduct, not a verdict." ✓ No post-hoc freedoms anywhere.
- **#7:** labels used only at metric time (pinned, §3.1); the T2-P2 exemplars are outline format demonstrations, not labels — verified against H7 §3.3 (the true-label exemplars were T1-P2's; H11 uses T2-P2 only). ✓
- **#9:** primary metric registered pre-run; Phase-0 records pinned as diagnostics that never enter the metric; the full run regenerates all 60 items fresh with greedy determinism — "no selection on partial data" — pinned, not assumed. ✓
- **#13:** torch.manual_seed(0) + numpy seed 0; greedy everywhere; LOG-331 pin before/after; bench provenance pin (independently re-verified: sha256 of `exp077_instance_records.json` = `47281cd3dc243369be0aa5be2345663b752cdb4a329a16a37f08da5717230585` — matches the pin byte-exactly); 60-item bench rebuilt verbatim (len==60 asserted; 60/60 distinct prompts; 10/10 distinct probe prompts — the §3.7 "probe triples are distinct" claim verified at the prompt level, which is the operative level for the variation guard); environment manifest (torch/numpy/transformers/accelerate versions, thread count, seeds). ✓

## 7. Falsification tree — complete

Every branch terminates: bench/provenance → RUN-INVALID; backbone pre → RUN-INVALID; prompt byte-verify → RUN-INVALID; Phase 0a → RUN-INVALID; Phase 0b → RUN-INVALID; exceptions >10% → RUN-INVALID; backbone post → RUN-INVALID; re-parse mismatch → RUN-INVALID; n_valid < 48 → RUN-INVALID; McNemar → CONTINUE/HELD/KILL. No dead ends, no unregistered re-runs (the "No rescue runs" clause in §4 explicitly bars larger-n re-tests, more outlines, different slots, re-seeds). The KILL retire-scope is fenced ("the coordinator axis is retired for the piloted scope", §7.4). ✓

---

## Required fix (documentation precision only — no design change)

**FIX-1 — §8 omits the item-valid/arm-valid rule adaptation.** Insert a new item at the end of the "From H4's pre-registered design" list (after item 9; renumber the existing "From H7's T2-P2 spec: 10. No change" to item 11), with this exact wording:

> **10. Item-valid/arm-valid rule:** H4's per-arm "≥ 3 parseable votes" validity (§3.5: 4 executor + 4 baseline generations per item) → H11's per-item rule: planner-valid (§3.3) AND ≥2 executor votes parseable AND baseline parseable (§3.8). *Why:* at greedy, the baseline arm has exactly 1 generation and the executor arm has 2–4 (one per extracted outline), so H4's ≥3-of-4 per-arm rule is arithmetically impossible; the thresholds are re-derived for the reduced generation counts. The ≥2-executor-parseable floor preserves H4's anti-degeneracy intent (an item decided on a single executor vote is excluded). This is a forced consequence of adaptations 2 and 4, not an independent design choice.

## What was verified and found sound (summary)

- All seven §4 p-values exact; tiling gapless; no razor-thin CONTINUE.
- T2-P2 import byte-verbatim vs H7 (template, exemplars, spec); byte-verification check operationally pinned.
- Phase-0a/0b gates mechanically decidable, honestly calibrated against the cited priors, blind spot disclosed.
- Honesty fence airtight: no claim path from CONTINUE to planning capability.
- Worth-it gate PASS; Laws #4/#7/#9/#10/#13 comply; falsification tree complete; bench pins re-verified byte-exact.

**Lane boundaries held:** no protocol edited, no execution dispatched, no self-review. Fix-verification of FIX-1 and the CEO launch decision are separate later lanes.
