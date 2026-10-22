# EXP124 (H21/PLAN-INSTRUMENT) Execution Report — 2026-09-29

**Lane:** LOG-4670 (pre-assigned). **Protocol:** `research/prereg/EXP_PREREG_H21_PLANINSTRUMENT_2026-09-29.md`
(launch-ready: Law #14 SIGN-WITH-FIXES LOG-4668; FIX-1/2/3 byte-verified LOG-4669).
**Verdict: RUN-INVALID** — choice-information gate (breaking point (a)): C-FIRST=7 < 12.
**$0 CPU. Δθ=0. No metric was read (Law #9 — the metric is read only after all guards pass).**

---

## 1. Verdict statement

**RUN-INVALID (apparatus-void; hypothesis UNTESTED, no verdict on H21).** The full run produced
choice-valid plans on 55/60 items, but the extracted choice distribution was
**A-FIRST=48, C-FIRST=7, choice-invalid=5**. The pre-registered choice-information gate
requires each phrasing to be chosen on ≥ 12 items (20% of 60); C-FIRST=7 < 12, so the
planner's output is a decision-inert control, not a treatment. Per §5 of the pre-registration,
the lane halted at the gate: no variant forwards, no choice-arm forwards, no random arm,
no McNemar table were constructed. **b, c, d, p do not exist** — no paired table was built,
and none is reported.

H11's planning question survives this RUN-INVALID (as it survived EXP117, EXP119, EXP121).
H21's instrument-selection channel receives no verdict.

---

## 2. Falsification-tree walk (all numbers executor-produced)

| Tree node | Result |
|---|---|
| Bench provenance + len==60 + schema (`prompt`/`premise`/`tuple`/`phrasing`/`id`; `prompt == premise + QUESTION_SUFFIX`; phrasing 30/30) | **PASS** — bench SHA-256 `e91b302f…4f5` matched; npz/embeddings/ids pins matched |
| Variant construction (§3.5): SWAP involution + decomposition | **PASS** — 60/60 premises matched exactly one pinned template; `SWAP(SWAP(P))==P` 60/60; V_A/V_C labels consistent with bench phrasing |
| Phase-0pre: tokenizer-only `[-3:]` on all 120 variant contexts | **PASS** — 120/120 tails `== [32, 37741, 27]` (`?`, `ĠAnswer`, `:`); no model contact |
| Backbone LOG-331 pin (pre) | **PASS** — `ec276abe3902fab0…` before first generation |
| Planner prompts byte-verified vs H19 §3.3 T2-P2 | **PASS** — 0/60 mismatches vs independent EXP113 reference reconstruction |
| Phase-0a: planner choice-validity (probe {0,1,2,5,6,7,8,9,10,11}) | **PASS** — 10/10 choice-valid (≥ 8 required) |
| Phase-0b: variant discriminability + channel G1 | **PASS** — 4/10 items with differing variant readouts (≥ 3 required); M_A=0.38102, M_C=0.46331 (both ≥ 0.01) |
| Full run: 60 planner generations + choice extraction (§3.4) | 60/60 generated, 0 exceptions; **n_valid=55/60; A-FIRST=48, C-FIRST=7, invalid=5** |
| **Choice-information gate: each phrasing ≥ 12** | **FAIL → RUN-INVALID** — C-FIRST=7 < 12 (decision-inert control) |
| 120 variant forwards / backbone post-pin / baseline reproduction / choice-arm forwards / McNemar | **not reached** (halted at gate, per tree order) |

**Δθ=0 note:** the post-contact backbone pin was not computed because the lane halted at the
choice-information gate before the forward phase (the tree places the gate before the 120
forwards). The pre-contact pin matched LOG-331; the script contains no optimizer, no backward
pass, no weight mutation of any kind — the backbone could not have been trained by construction.

---

## 3. Descriptive failure-mode analysis (unlicensed observation, not a verdict)

Re-reading the 55 choice-valid raw generations against the pinned §3.3/§3.4 rules:

- **55/55** final outlines (F, the last element of L in position order) contain a **hallucinated
  premise** — a `Premise: …` line the model emitted that matches no bench item (34 distinct
  hallucinated premises across the 55; entities like Gold/Iron/Silver/Bronze, absent from bench 1).
- **55/55** choices are driven by the **leftmost entity match inside the hallucinated region** —
  the outline texts themselves contain no entity names, so every extracted "choice" is a function
  of model regurgitation, not of plan content.
- The generation pattern is uniform: verbatim recitation of the T2-P2 exemplars, then a
  hallucinated premise + question + TAIL, then re-recitation of the exemplars until the 160-token
  cap. This is consistent with the EXP117/EXP119 10/10 recitation finding (LOG-4610, LOG-4628, BIND).

[INTERPRETATION] The §3.4 choice rule was applied faithfully (deterministic, label-blind,
mechanically correct), but the object it operates on is not a "plan-conditioned choice" in any
meaningful sense — it is entity mentions in model regurgitation. The choice-information gate
fired honestly: the instrument was never a treatment. This does not change the verdict
(the gate's outcome is binding); it characterizes *which* apparatus piece failed (§7.5):
the planner elicits text, but not plan text whose final outline commits to an answer.

---

## 4. Raw artifacts (hash-pinned; persisted on the RUN-INVALID path — defect class 2)

`~/workspace/SCBI/experiments/runs/EXP124_planinstrument/out/`:

| Artifact | SHA-256 |
|---|---|
| `exp124_generations.json` (70 records: 10 probe + 60 full-run) | `1759881d314848ac43b2cd5b6fb81262edbf0285672fd8fe7c8712df9cb7796a` |
| `exp124_forwards.json` (20 records: Phase-0b probe forwards) | `2f8c638b182fbd21df8867d648b1babffc7a64789581ea4d378af7d693026563` |
| `exp124_run.json` (gates, phases, per-item choices) | `0ce9343b143a02baab718fc369f8513d56da56887338e8039f19a7acf9f09959` |
| `exp124_worksheet.json` (environment manifest, pins) | `c6d953ffe201c123cc7553d1631ae798a877a84b842d039ac2cba0c4fc59c626` |
| `exp124_console.log` | `d5b4059603132b132120201d204462e084c6e0e7cf12e10ddfe8cd7c36d580cb` |
| `exp124_execute.py` (the executor; `.venv-exp077`: torch 2.14.0+cpu, transformers 5.17.0) | — |

Environment: torch 2.14.0+cpu, transformers 5.17.0, numpy 2.5.3, sklearn 1.9.1;
`torch.manual_seed(0)`, numpy seed 0, threads=2 (read back 2); greedy decoding, `max_new_tokens=160`.
The McNemar executor line was never printed because the metric stage was not reached — correctly,
per Law #9. No p-value is quoted in this report (defect class 1: none was computed).

---

## 5. Honest frame

- A RUN-INVALID is not a KILL: the instrument-selection channel is **untested, not retired**.
  H11's fourth logit-channel composition consumed its attempt without a verdict.
- The program's label-free race remains tied at zero: still no positive signal for autonomous
  steering; the trained-readout CONTINUEs (EXP111, EXP120) and the EXP112 HELD are unchanged.
- **New binding lesson (defect class 8):** a choice-extraction rule whose input is the *final
  outline in position order* must assert that the final outline is plan content, not
  regurgitation — or the instrument is unlicensed. Future plan-as-instrument designs must gate
  on generation construct-validity (e.g., final outline contains no `Premise:`/question-tail
  regurgitation) before any choice extraction.
- Novelty remains N1 — Known Combination (§7.1.6).
