# EXP104 Bench Autopsy — Tier-0 HOLD Diagnosis (2026-09-28)

**Lane:** EXP104 BENCH AUTOPSY (analyst, CEO-briefed). **$0, committed artifacts only, no model contact, no new passes.**
**Log:** LOG-4483. **Verdict of this autopsy: (a) — a recalibrated bench is feasible via a readout change (cloze format), as a NEW proposal.**
**Does not:** mint an experiment number, modify the signed S4-8 pre-reg v3 (LOG-4480), or authorize any run.

**Inputs:** `experiments/runs/EXP104_Tier0_rank_screen/` — TIER0_REPORT_2026-09-28.md, per_item_records.json (60), tier0_worksheet.json, bench_manifest.json (60 items, 10 templates × 6). Recomputed below with a deterministic script reading those files only.

---

## 1. Per-template breakdown [OBSERVATION]

Templates map to 6-item blocks in manifest order (verified against bench_spec.py question stems).

| # | Template | Acc | Correct | Rank dist (ranks 1–8) | Median rank (failed) | Mean top1−correct margin (failed) | pos0-picks |
|---|---|---|---|---|---|---|---|
| T0 | landmarks → country | 0.167 | 1/6 | [1,2,2,1,0,0,0,0] | 3.0 | 0.638 | 4/6 |
| T1 | products → country | 0.167 | 1/6 | [1,2,2,0,0,0,1,0] | 3.0 | 1.086 | 4/6 |
| T2 | films → country | 0.000 | 0/6 | [0,1,2,1,1,1,0,0] | 3.5 | 1.094 | 4/6 |
| T3 | rivers → country | 0.333 | 2/6 | [2,3,0,0,0,1,0,0] | 2.0 | 0.907 | 4/6 |
| T4 | museums → city | 0.000 | 0/6 | [0,0,0,2,1,1,2,0] | 5.5 | 1.453 | 1/6 |
| T5 | novels → country | 0.333 | 2/6 | [2,2,0,0,0,1,0,1] | 4.0 | 1.496 | 4/6 |
| T6 | founders → US state | 0.167 | 1/6 | [1,1,1,1,0,0,0,2] | 4.0 | 1.154 | 2/6 |
| T7 | events → country | 0.500 | 3/6 | [3,1,1,1,0,0,0,0] | 3.0 | 0.592 | 2/6 |
| T8 | treaties → country | 0.167 | 1/6 | [1,2,1,0,1,0,0,1] | 3.0 | 1.230 | 3/6 |
| T9 | paintings → country | 0.000 | 0/6 | [0,0,1,0,0,4,0,1] | 6.0 | 1.416 | 2/6 |
| | **Total** | **0.183** | **11/60** | | 4.0 | 1.137 | **30/60** |

**Is the failure uniform? No — two gradients, one dominant:**
- Three templates sit at or above the sanity band's lower edge [0.25]: events 0.50, rivers 0.333, novels 0.333 (7/18 = 0.389 combined).
- Three templates are at absolute zero: films, museums→city, paintings (0/18 combined).
- But the position-A prior is uniform across ALL templates (2–4 pos0-picks per 6-item block), so the readout artifact contaminates every template's number.

## 2. Diagnosis

### Cause 1 (dominant): the word-scored MC readout measures a position prior, not knowledge [OBSERVATION → INTERPRETATION]

- **Top-1 position distribution:** position 0 picked **30/60** times; position 7 picked 12/60; positions 1–6 picked 2–4 each. Under no position bias, P(≥30 picks at one position) = **2.02e-12** (binomial, p=1/8). This is not noise; it is the instrument's dominant signal.
- The pos0-pick rate is uniform across templates (2–4 per block) → the bias is **format-driven** (the `A)…H)` enumeration + terminal `Answer:`), not content-driven.
- Of the 11 correct items, 4 were at position 0 — versus 30×(6/60)=3.0 expected under a pure position prior. **The A-picks carry no knowledge.**
- On the 30 items where the model did NOT fire its A-prior, accuracy is 7/30 = **0.233** — still below the 0.25 band edge, but above chance (0.125). Weak residual signal exists; the prior buries it.
- The shuffle seed (20260928) placed the correct answer at positions {0:6, 1:7, 2:6, 3:11, 4:5, 5:13, 6:3, 7:9} — positions 3 and 5 over-represented. The realized baseline is therefore **shuffle-seed-sensitive**: a different seed changes the number. A bench whose headline number depends on the shuffle seed through the model's position prior is not a knowledge instrument.
- Top-1 wins by mean logit margin 1.137 (median 0.906) on failed items — a solid win, not a near-tie; tie-guard 0.0. Consistent with a prior, not a close factual contest.
- The structural foil equals the top-1 on **11/49 failed items** (O = 0.212 on the n_pop=33 population → the F arm would have been diagnostic per the D2 stratum, had the battery run). The model frequently lands on the confusable distractor — it is not completing even hop 1.

**Mechanism [INTERPRETATION]:** Pythia-410m is a base (non-instruction-tuned) LM. After `Answer:`, its next-token distribution over the 8 content tokens is dominated by a primacy/copy effect from the enumerated prompt — the token following `A)` gets boosted regardless of content. Word-scoring (argmax over the 8 option logits) does not remove this; it *is* this.

### Cause 2 (secondary): a genuine 2-hop capability gradient at 410m [OBSERVATION → INTERPRETATION]

- The three zero templates are the hardest 2-hops: film→director→country, painting→museum→country, painting→museum→city. The surviving templates are easier retrievals (events, rivers, novels).
- This gradient is consistent with marginal multi-hop factual recall at 410m scale — but it is **unmeasurable** until Cause 1 is removed, because every template's number is contaminated by the position prior.

### Reconciliation with EXP092 [INTERPRETATION]

- **EXP092 [OBSERVATION]:** supervised LOO 1-NN (K=20, chance 0.05) on frozen L11 activations recovers the label at 33.33% (6.7× chance, p=0.000999). This measures **information presence** — a trained decoder reading task-relevant structure out of the representation.
- **EXP104 [OBSERVATION]:** zero-shot word-scored MC at the `Answer:` position measures **information routability** — whether the model's own untuned LM head surfaces that information as the argmax token under a multiple-choice prompt.
- **No contradiction.** Presence ≠ routability. A trained probe can read what a base model's generation head cannot surface through a format it was never trained on. EXP092's decode success does not license any expectation about EXP104's zero-shot MC accuracy, and EXP104's HOLD does not retract EXP092's presence claim. They are different constructs.

### What is NOT the cause [OBSERVATION]

- Tokenizer mapping: G1 gate was clean (0/480 multi-token option strings). The EXP090 failure mode was caught and fixed pre-run.
- Item quality: independent checker 64/66 VERIFIED, 2 flagged items replaced/dropped pre-run, blindness attested.
- The bench was well-built. The failure is the **model × format interaction**, not bench construction.

## 3. Verdict: (a) — recalibrated bench feasible, as a NEW proposal

**The fix must change the readout, not shop templates.** Selecting only the surviving templates (events/rivers/novels) on pilot accuracy would be post-hoc metric selection (Law #9), and the zero templates are also the hardest 2-hops — dropping them changes the construct being tested. All 10 templates survive into the recalibration.

### Recalibrated design (proposal only — no pre-reg drafted here)

- **What changes:** the prompt format. Replace the lettered `A)…H)` enumeration + terminal `Answer:` with a **cloze completion**: keep each item's question text verbatim, drop the option list and letters, end with a natural completion cue (e.g. `The answer is`). Score the same 8 single-token option logits at the completion position; correct-rank machinery is unchanged.
- **What stays:** all 60 items, all 10 templates, the G1-verified token pools (tokenizer-level property — transfers unchanged), the checker-verified facts, k=8, the Tier-0 decision table (premise/power/sanity/tie-guard bars), the battery design.
- **Why cloze over position-cycling:** cycling 8 rotations preserves the MC format a base LM handles poorly and multiplies every future battery pass by 8 (480-pass Tier-0, ~1920-pass battery — over the 500 hard cap). Cloze removes the letter-position confound at the source for 60 passes (~1 min CPU, $0).
- **Predicted accuracy band [HYPOTHESIS, not a claim]:** directionally 0.25–0.45. Anchor: the non-pos0 subset measured 0.233 with the prior only partially removed; full removal should add points. If the capability gradient (Cause 2) dominates, it lands near chance instead — that is exactly what the new Tier-0 adjudicates.
- **Breaking point (sharp):** cloze Tier-0 baseline < 0.25 → HOLD again → verdict flips to **(b)**: the I2′ line is untestable on Pythia-410m at $0. Structural reason: 410m-scale base LM lacks retrievable 2-hop factual chains under every $0 readout tried (word-scored MC and cloze); further instrument surgery after two HOLDs is p-hacking the bench (pre-reg §6 risk 6 backdoor warning — honored, not circumvented).

### Law-#15 packet skeleton (proposal only)

1. **Exact question [HYPOTHESIS]:** On the same 60 items re-prompted as cloze completions (no lettered options), does the Tier-0 baseline land inside the sanity band [0.25, 0.75] — i.e., was EXP104's HOLD a readout artifact (Cause 1) rather than a capability absence (Cause 2)?
2. **KILL/CONTINUE/PIVOT decision it changes:** CONTINUE (license the S4-8 battery on the cloze bench) iff cloze Tier-0 baseline ∈ [0.25, 0.75] AND median failed correct-rank ≤ 5 AND n_pop ≥ 12; KILL (line) iff cloze Tier-0 < 0.25 after this second readout — I2′ untestable on this model at $0; HOLD iff tie-guard > 0.25 or other instrument failure.
3. **Cheapest falsifying test:** cloze Tier-0 rerun — 60 forward passes, ~1 min CPU, **$0**, Δθ=0, deterministic seed-pinned. The six §4 degeneracy unit tests re-run on the cloze rank function first (same synthetic suite).
4. **Mathematical license [PROPOSITION]:** at k=8 the correct-rank r_i ∈ {1,…,8} is not a deterministic function of correctness (pre-reg §0 license, unchanged); removing the option enumeration removes the position prior's support — the argmax is then over content tokens in a completion context, where no positional confound exists by construction. Breaking point: if cloze Tier-0 < 0.25, the license's empirical precondition (a calibrated instrument) fails and no battery may be built on this bench family.

**Sequencing (not authorized here):** new unsigned proposal → Law #14 review → SIGN → CEO clearance → cloze Tier-0. This autopsy authorizes nothing.

## 4. Lineage

- Analysis scripts: deterministic reads of `per_item_records.json`, `bench_manifest.json`, `tier0_worksheet.json` (no model contact).
- Key derived numbers: pos0-picks 30/60 (p=2.02e-12 under no bias); non-pos0 accuracy 7/30=0.233; foil=top-1 on 11/49 failed (O=0.212 on n_pop=33, F arm diagnostic); mean top1−correct margin 1.137; per-template table in §1.
- Deliverable: `research/analysis_plans/EXP104_BENCH_AUTOPSY_2026-09-28.md` (this file). Log: LOG-4483.
