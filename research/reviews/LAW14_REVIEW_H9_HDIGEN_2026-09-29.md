# Independent Law #14 Review — H9 (HDI-GEN) Pre-registration

**Reviewer lane:** LOG-4596 (independent of the LOG-4595 drafting lane).
**Artifact under review:** `research/prereg/EXP_PREREG_H9_HDIGEN_2026-09-29.md` (read in full).
**Reference artifacts read:** `research/experiments/EXP113_EVALID_REPORT_2026-09-29.md` (full), `research/prereg/EXP_PREREG_H7_EVALID_2026-09-29.md` (P2 spec, §66), `research/prereg/EXP_PREREG_H6_HDILR_2026-09-29.md` (§3.2, §134), `research/experiments/EXP108` report (elicitation gate, lines 34–36, 47), `experiments/runs/EXP112_hdildr/out/exp112_per_item.json` (archive: 60 records, fields, sha256), `experiments/runs/EXP107_templatectrl/build_exp107_bench.py` (QUESTION_SUFFIX line 53, builder lines 40–70, 129, 167–169).
**$0 CPU.** No signed protocol modified, no execution, no weights touched.

---

## 1. Bars and numbers — independently recomputed from first principles ✓

All six p-value claims in §4 were recomputed exactly (n=57, exact binomial):

| Claim in pre-reg | Independent recomputation | Match |
|---|---|---|
| P(X ≥ 56 \| 57, 0.98) = 0.6839 | 0.6839 | ✓ |
| P(X ≥ 40 \| 57, 0.5) = 0.0016 | 0.0016 | ✓ |
| P(X ≤ 54 \| 57, 0.99) = 0.0196 | 0.0196 | ✓ |
| P(X ≥ 39 \| 57, 0.5) = 0.0038 | 0.0038 | ✓ |
| P(X ≥ 31 \| 57, 0.5) = 0.2983 | 0.2983 | ✓ |
| P(X ≤ 21 \| 57, 0.5) = 0.0314 | 0.0314 | ✓ |

Bar-fraction labels verified: 56/57=0.9825, 55/57=0.9649, 40/57=0.7018, 54/57=0.9474, 39/57=0.6842, 32/57=0.5614, 31/57=0.5439 — all correct as rounded. Region boundaries tile [0,57] completely (≤31 / 32–39 / 40–54 / 55 / ≥56) — no gaps, no overlaps. The §1 hypothesis sentence "[0.70, 0.95]" is rounding shorthand for §4's binding [0.7018, 0.9474]; §4 is declared the binding table, so no executor ambiguity.

## 2. Elicitation gate — H7-CONTINUE consequence honored ✓

H7-CONTINUE's registered consequence requires each revival lane to name its clearing protocol and carry its own elicitation-failure gate. H9 names P2 (verified: EXP113 T1-P2 cleared 60/60 on both task shapes, report lines 10–11, 46, 51) and carries G1 + G2:
- **G1** (n_unparseable ≥ 7 of 60 → RUN-INVALID): matches the EXP108 registered gate bar exactly (verified in the EXP108 report: "Pre-registered gate (≥7)" fired on 60/60; the H1 pre-reg gate identical). ✓ "mirrors EXP108's registered gate" is accurate.
- **G2** (≥2 distinct values AND minority ≥ 3 of 57, else RUN-INVALID): correctly addresses the documented EXP113 "all A" observation (EXP113 report line 55: "T1-P2/P4/P5 outputs are exclusively the letter A — the format the exemplars/priming demonstrated"; T1-P2 scored 60/60 parseability while content-degenerate). The guard is disclosed in §9 item 5 as an *addition*, not misattributed to H7. ✓
- Both guards fire before any metric is read (§3.5, falsification tree). ✓

## 3. The six recorded deviations — one gap found (FIX F1), one precision issue (FIX F2)

§9 claims a complete six-item list of deviations from H7's T1-P2 spec. Comparing H7's actual T1-P2 spec (`EXP_PREREG_H7_EVALID`, line 66: "Q: {PROMPT_i} + question + A: {true label of item i}, then the target item with the T1-P1 question and a trailing A:. Greedy, max_new_tokens=4") against H9's §3.3:

1. Answer slot A/C letters → entity names — genuine repair, recorded. ✓
2. n = 57 (exemplar exclusion) — genuine, bars re-derived. ✓
3. Archived decision arm (zero new forwards) — genuine, hash-pinned, G4 re-check. ✓
4. Elicitation gate imported from EXP108 — genuine, verified in item 2 above. ✓
5. G2 variation guard added — genuine, disclosed as addition. ✓
6. Ground-truth constancy disclosed — genuine. Verified independently from the bench builder: premises are "A outranks B. B outranks C." / "C is lower than B. B is lower than A." — in both, A (tuple[0]) is highest; `tgt = b['tuple'][0]` (builder lines 167–169). ✓ The no-substring claim (§3.4) is trivially true for the planet/element vocab.

**Gaps in the deviation record (required fixes, below).**

## 4. Archived EXP112 decision arm — provenance sound ✓

- The archive file exists at the pinned path with 60 per-item records carrying `E1`, `E2`, `decision`, `cos_E1`, `cos_E2` fields.
- Its sha256 was **independently recomputed by this reviewer**: `f8133f1f4dc6f302cb7fdbe4dee248f9eb5ab97afab00c7fbc7b331e1a804625` — byte-identical to the pin in §3.2. ✓
- E1 = tuple[0], E2 = tuple[-1] convention matches H6 §3.2 (verified in `EXP_PREREG_H6_HDILR`, lines 60 and 134). ✓
- The archived G4 re-check (max−min over archived cos values ≥ 1e-4) is re-verifiable by the executor from the same pinned file; HALT on archive drift is registered. ✓
- Decision distribution is 30 E1 / 30 E2 overall — no pre-reg claim contradicts this.

## 5. Worth-it gate (§0) — genuinely a new question ✓

The adversarial challenge "H6 already answered this" is correctly defeated in §0 and §1.1: H6 (EXP112) measured the position-0 next-token *distribution* (argmax over two pinned token logits), never emitted text; H9 reads the *generated string* (up to 8 tokens) via the validated P2 protocol and extracts entity names from it. Greedy decoding's first emitted token equals the position-0 argmax, but H9's parse observes leading whitespace, punctuation, multi-token completions, and hedging — behavioral phenomena the logit proxy cannot see. The instrument-operability argument (an oversight gate reads outputs, not logits) is substantive. The quantitative prediction discriminates the two accounts (proxy-real vs proxy-artifact). **Gate PASS stands.**

Reviewer note (non-fix): the three few-shot exemplar answers are all E1 (the ground truth, §3.3). This biases the generated channel toward E1, but the design is robust to it: the archived decision distribution is ~50% E1, so a constant-E1 channel can reach at most ~28–29/57 — below the 32/57 HELD floor, i.e. it cannot manufacture a CONTINUE. The bias direction is disclosed in §3.7/§9.

## 6. Law compliance ✓ (with §9-record fixes below)

- **Law #4:** bars binding; post-hoc rewording explicitly BARRED in §4 and the falsification tree; no re-run/no larger-K rescue (HELD/KILL final). ✓
- **Law #7:** the 3 exemplar items' in-context answers are excluded from scoring (§2, §3.7); no other labels touch the metric; fidelity compares parse vs the archived *decision statistic*, never vs labels. ✓
- **Law #9:** primary metric, parse rule, guards, and bars all registered before any output; §3.3 pins "no early abandonment". ✓
- **Law #13:** torch/numpy seeds, greedy decoding, thread-count readback, bench pin, archive pin, LOG-331 backbone pin before AND after generations, deterministic re-parse ×2 byte-identical. ✓
- **Law #10:** N1 — Known Combination (§8.6), consistent with program practice. ✓
- **Law #6:** Δθ=0, backbone hash before/after, mismatch → RUN-INVALID + quarantine. ✓

## 7. Falsification tree — complete ✓

Every branch terminates in HALT, RUN-INVALID, KILL, HELD, or CONTINUE, or is BARRED. All n = 0..57 covered by the verdict rows. The ≤21/57 systematic-misreporting diagnostic is explicitly non-verdict-changing (verdict stays KILL) — correctly labeled [OBSERVATION]. No dead ends, no unregistered re-runs.

---

## Required fixes (SIGN-WITH-FIXES)

**F1 — Record the max_new_tokens change in §9.** H7's T1-P2 used `max_new_tokens=4` (H7 pre-reg, line 66); H9's §3.3 pins `max_new_tokens=8`. This parameter change appears nowhere in the §9 deviation list, which claims completeness ("complete list"). Add to §9 (as item 7 or folded into item 1): "max_new_tokens: 4 → 8 — H7's T1-P2 generated ≤4 tokens for single-letter answers; H9 allows 8 tokens so the §3.4 parse rule can find multi-token entity names and leading whitespace/punctuation (part of the generation-level question)."

**F2 — Correct the "imported verbatim" claim in §9 item 1.** §9.1 currently states: "The few-shot structure (3 pinned exemplars, Q:/A: format, greedy decoding) is imported verbatim; only the answer slot carries entity names." H7's T1-P2 used literal `Q:`/`A:` prefixes; H9's pinned template drops them — exemplar answers follow the bench prompt's own `Answer:` slot (`{PROMPT_i} {E1_i}`). Replace the sentence with: "The few-shot *structure* (3 pinned exemplars demonstrating question→answer, greedy decoding) is imported; H7's literal `Q:`/`A:` prefixes are replaced by the bench's own `Answer:` slot — the answer appears after `Answer:` rather than after `A:`. The full template is pinned in §3.3 and is the binding specification."

Neither fix changes the protocol, the bars, or any pinned value — §3.3 remains the binding specification. A separate fix-verification lane must confirm both edits before CEO launch.

---

## Verdict: **SIGN-WITH-FIXES**

The H9 pre-registration is rigorous: numbers exact, gates real, the worth-it gate passes, the archived-arm provenance is sound, and the falsification tree is complete. The two defects are both in the §9 deviation record's completeness, not in the experimental design. Fix F1 and F2, verify, then it is launch-eligible.

**Single most important finding:** the §9 deviation list — which the draft claims is complete — omits a real parameter change (max_new_tokens 4→8) and misdescribes the Q:/A: format adaptation as "imported verbatim" when the literal prefixes were dropped; the program's complete-deviation standard requires F1/F2 before launch. No design flaw was found.
