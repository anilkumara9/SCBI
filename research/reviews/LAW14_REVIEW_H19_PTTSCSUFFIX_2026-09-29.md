# Independent Law #14 Review — H19 Pre-registration (PTTSC-SUFFIX)

**Review lane:** LOG-4642 (pre-assigned, independent of the LOG-4641 drafting lane).
**Review date:** 2026-09-29.
**Target:** `research/prereg/EXP_PREREG_H19_PTTSCSUFFIX_2026-09-29.md` (~40 KB, §§0–9 + boundary).
**Ground sources:** `research/strategy/H19_GATE_2026-09-29.md` (LOG-4640, binding gate memo); `research/prereg/EXP_PREREG_H14_PTTSCLOGIT_2026-09-29.md` (H14, SIGN-WITH-FIXES LOG-4625, FIX-1 byte-verified LOG-4626); `research/reviews/VERDICTREVIEW_EXP119_2026-09-29.md` (LOG-4628, BIND); `research/strategy/INNOVATION_DESIGN_SESSION_POST_EXP120_2026-09-29.md` §H19 (LOG-4638).
**Method:** full read of the draft; diff-verified every "carried verbatim" claim against H14; recomputed the McNemar table independently; mechanically verified the placement-(A) tokenization claim with the pinned Pythia-410m snapshot tokenizer (tokenizer-only, no model contact); swept the 20 discrepancy classes.

## Verdict: SIGN-WITH-FIXES (one documentation-precision fix)

The design is licensed, the bars are faithful, the fences hold, and the placement-(A) rationale is mechanically sound. One undefined identifier in the pinned §3.4 context template requires a documentation-precision fix before launch; it cannot affect the verdict because the replace-form construction is authoritative and self-arbitrating.

## What was verified

**1. Structure:** §§0–9 + boundary all present, no truncation placeholders, epistemological labels per SCBI/AGENTS.md §5.

**2. Placement-(A) rationale — mechanically verified (tokenizer-only).** Using the exp-cpu venv transformers and the pinned snapshot tokenizer (`~/workspace/.exp086_weights/pythia-410m`, `local_files_only`):
- `tokenize(" Question: Who is higher in rank? Answer:")` → `[19782, 27, 8452, 310, 2169, 275, 5958, 32, 37741, 27]`, tail `['?', 'ĠAnswer', ':']`.
- Two probe contexts differing upstream (`premise + " Plan:\n1. Foo.\n2. Bar." + SUFFIX` vs `premise + " " + SUFFIX`) both yield `[-3:] = [32, 37741, 27]` — identical to the verbatim baseline tail. The draft's claim ("identical text ⇒ identical tokens ⇒ identical last-three ids") holds on the real tokenizer: GPT-2's pre-tokenizer chunk-splits at word boundaries, so the trailing suffix's last three tokens are determined by the trailing text alone. The pin is evidence; the argument is correct.

**3. Placement (B) barred:** §0(a) and §8 item 5 bar placement (B) under Law #4 as a re-run of the retired EXP119 composition — matches VERDICTREVIEW_EXP119's structural adjudication.

**4. [-3:] pin carried verbatim:** Phase 0-pre (tokenizer-only pre-check on all 60 items before any model contact, mismatch → RUN-INVALID immediately) plus the pre-check re-armed on the real compositions in Phase 0b — operational and self-arbitrating. The re-arm is redundant given the mechanical result above but harmless; it also guards against placeholder-vs-real divergence.

**5. Honesty fence:** §7.1 item 1 carries H14's text and adds "The suffix design does not change this: the plan arm is still longer than the baseline." §0(c) likewise states the fence is unchanged. Nowhere does the draft claim placement (A) removes the token-asymmetry confound — explicitly the opposite. Verdict-licensed attribution (pipeline as adaptive-loop component only, never planning-vs-compute) is intact.

**6. McNemar bars:** §4 table and decision rows match H14 §4 exactly; I recomputed all seven one-sided exact p-values independently: (5,0)=0.03125 ✓, (4,0)=0.0625 ✓, (6,0)=0.015625 ✓, (6,1)=0.0625 ✓, (7,1)=0.03515625 ✓, (9,2)=0.03271484375 ✓, (8,3)=0.11328125 ✓. The KILL bar's strengthened wording ("through a working composition … stronger than EXP119's RUN-INVALID") is declared in §8 item 4 and consistent with the gate memo; it retires the same question, smuggles no new hypothesis.

**7. Five binding defect classes:** all pinned as protocol requirements in §2 — (1) executor-computed p-values only (§3.8: script computes and prints p, report quotes verbatim), (2) raw generation records hash-pinned before any verdict (artifact-existence gate), (3) FIX-1 label-pin discipline (§2 metric citation uses the builder's meaning-preserving construction + H6 §3.2 pin — the corrected wording), (4) no reuse of EXP117's §3.7 literal definition, (5) the [-3:] pin on the composition. The pre-reg form of the EXP120 lesson is operational: the review can check the raw logs for a printed p.

**8. Deviations list:** 25 items (7 vs H14, 12 vs H6, 6 vs H11) — every drift from H14 is declared (composition change, pre-check, context rule, KILL strengthening, placement-(B) bar, executor p-value, artifact gate). Checked for undocumented drift across §§0–9 against H14: none, except FIX-1 below.

**9. Laws:** Law #4 (bars binding, no rescue runs, placement (B) barred as re-run), Law #7 (tuple[0] at metric time only; planner exemplars are format demos), Law #9 (metric registered before any output; Phase-0 records diagnostic-only), Law #13 (pins, seeds, env, byte-identity checks, deterministic re-read ×2). No scope creep — no per-layer secondary, no cross-bench effect-size comparison. The §2 tuple[0] citation uses the FIX-1-corrected wording.

**10. Gate-memo fidelity:** bars, breaking point, Phase-0a re-gate, honesty fence, and the five defect classes all match H19_GATE_2026-09-29.md. The §0(5) elaboration ("b−c ≥ +5 clean") is consistent with the memo's directional prediction and the (5,0) minimum CONTINUE — not a drift.

## FIX-1 (documentation-precision, launch-gating, verdict-immaterial)

**Location:** §3.4, the sentence beginning "`CONTEXT_PLAN` = `{PREMISE}` + `" "` + `PLAN_BLOCK` + ` QUESTION_SUFFIX_WITHOUT_LEADING_SPACE`".

**Defect:** `QUESTION_SUFFIX_WITHOUT_LEADING_SPACE` is an identifier defined nowhere in the document — it is a malformed descriptive descriptor inside the pinned context-template section. It cannot license a wrong construction (the `PROMPT.replace(QUESTION_SUFFIX, " " + PLAN_BLOCK + QUESTION_SUFFIX, 1)` code-equivalent form plus the exactly-once assertion are authoritative and self-arbitrating), but a pinned template section must not contain an undefined term an executor could misread.

**Prescribed replacement (exact):** replace that sentence with:

- `CONTEXT_PLAN` — exact pinned construction: `{PREMISE}` + `" Plan:\n"` + the re-numbered outlines joined by `"\n"` + `" Question: Who is higher in rank? Answer:"`, where `{PREMISE}` is the bench record's `premise` field verbatim. In code-equivalent form: `CONTEXT_PLAN = PROMPT.replace(QUESTION_SUFFIX, " " + PLAN_BLOCK + QUESTION_SUFFIX, 1)` — the plan block is inserted between the premise and the question tail, once, in placement (A). If the substitution does not occur exactly once → RUN-INVALID (apparatus bug).

**Note for the fix-verification lane:** verify the replacement is the only byte change (diff against the pristine copy).

## Verdict detail

SIGN-WITH-FIXES. On FIX-1 application and byte-verification, the H19 pre-registration is launch-eligible. The follow-up (not dispatched by this lane): separate fix-verification → CEO launch decision with experiment-number minting.

**Lane boundaries:** $0 CPU for research actions (tokenizer-only mechanical check); read-only on all signed protocols, paper sources, and the GPU queue; no experiment number minted; no follow-ups dispatched; no push; no credentials, weights, or GPU contact. This lane did not modify the draft.
