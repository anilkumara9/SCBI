# Independent Law #14 review: H20 (P4 apparatus validation) pre-registration (LOG-4659)

*Lane: LOG-4659 (pre-assigned). $0 CPU. Read-only everywhere except
this review and the research-log append. Fresh eyes — this lane did
not draft the protocol. No experiment number minted; no signed
artifact modified; no commit, no push, no credentials.*

**Reviewed file:** `~/workspace/SCBI/research/prereg/EXP_PREREG_H20_P4APPARATUS_2026-09-29.md`
(draft lane LOG-4658). **Superseding reference:**
`~/workspace/SCBI/research/strategy/H20_GATE_2026-09-29.md` (LOG-4657,
worth-it gate PASS). Law #14 scope: mathematical soundness and
internal consistency, not style.

---

## 1. Bar coherence and the arithmetic fix — VERIFIED

The three bars (§4, §5) are coherent, disjoint, and exhaustive over
`{0, …, 60}`:

- `n_unparseable ≤ 6` → CONTINUE (with the registered definition
  `n_unparseable = 60 − n_parseable` (§2), this implies `≥54/60`
  parseable — above EXP113's `≥48/60` clearance bar);
- `n_unparseable ≥ 7` → RUN-INVALID, terminal;
- `n_unparseable ≤ 6` **and** `n_parseable < 48` → HELD, no rescue.

The "unreachable by arithmetic" claim is **correct**: the parse rule
(§3.4) is a total function — every item is scored exactly once, and
exceptions are scored UNPARSEABLE (§3.6) — so `n_parseable =
60 − n_unparseable` holds exactly on every reading of the rule. With
`n_unparseable ≤ 6`, `n_parseable ≥ 54` follows; the middle region is
genuinely unreachable, not merely unlikely. The draft's §8 deviation
10 documents the drafting-brief fix honestly (the brief's
"41–47 parseable with ≤6 unparseable" parenthetical was arithmetically
impossible) rather than silently reproducing it — the LOG-4610
no-omissions lesson, honored.

Gate-precedence note: the LOG-4657 gate memo registers both
"`≥48/60` parseable → CONTINUE" and "`n_unparseable ≥ 7` →
RUN-INVALID", which overlap on 48–53 parseable under exact partition.
The draft resolves the overlap by explicit gate precedence (stated in
§0.2, §4, §6b, §8.10): the elicitation-failure gate fires first, so
the effective CONTINUE region is `n_parseable ∈ [54, 60]`. This is the
only consistent reading that keeps both registered bars meaningful,
and it is registered explicitly — not assumed. No silent bar shift:
§6b discloses that `≤53/60` "could have been read as close to the bar"
and that the terminal reading is the licensed one.

## 2. Elicitation-failure gate and counting — VERIFIED

- `n_unparseable = 60 − n_parseable` (§2) with the total parse rule
  (§3.4: `parseable = m1 XOR m2`, `unparseable = otherwise` —
  explicitly including empty generations, both-match, neither-match)
  and exceptions scored UNPARSEABLE (§3.6): the two counts partition
  the 60 items exactly. No double-counting, no unscored items.
- Exception threshold: ">10% of the 60 (i.e. >6)" (§3.6) — 10% of 60
  is exactly 6, so ">10%" ⇔ `>6` ⇔ `≥7`. The parenthetical is
  arithmetically correct.
- Precedence in the §5 tree is sound: the `>6` exceptions branch
  (RUN-INVALID, apparatus void) is checked *before* the
  elicitation-failure gate, so a high-exception run cannot pollute the
  terminal apparatus verdict's meaning. Both paths yield RUN-INVALID;
  no branch conflict.

## 3. Mechanical parse rule — deterministic; one pin gap (F1)

The rule is a total deterministic function of (generation text, e1,
e2): `strip()` → `rstrip` with the pinned punctuation set
`'.,;:!?\'")]}'` → case-insensitive exact match vs `e1`/`e2` →
parseable iff exactly one matches. Edge cases:

- Empty/whitespace-only generation → UNPARSEABLE: explicit. ✓
- Both-match (`m1 ∧ m2`): requires `e1 == e2` (case-insensitive).
  Independently verified on the deterministic EXP107 rebuild
  (`build_exp107_bench.build_bench()`): **0/60 items** have
  `tuple[0] == tuple[-1]` — the edge cannot fire on this bench; and
  even hypothetically the XOR handles it deterministically
  (→ unparseable). ✓
- Continuation attractor (`Mercury is the highest-ranked`) and
  enumeration attractor (`\n\n1. Jupiter…`) → unparseable by
  exact-match, as registered. ✓
- Leading punctuation is not stripped (only trailing): deterministic
  protocol choice, not an ambiguity. ✓

**F1 (launch-gating, minor — one pinned sentence):** §3.4 defines
`raw` as "generation text (decoded tokens only — the input prompt is
never part of the parse)" but does not pin the decode call. Whether
the executor decodes with `skip_special_tokens=True` vs `False` can
move parseability counts on edge items (e.g. an emitted `</s>` inside
the 4-token window breaks exact matches). The "input prompt never
part of the parse" clause is the critical pin and it *is* present;
the special-token handling is not. Add, in §3.3 or §3.4: "Generation
text = `tokenizer.decode(new_token_ids, skip_special_tokens=True)`;
input-prompt tokens are never decoded into `raw`." Verdict-immaterial
to the bars; a Law #13 reproducibility pin.

## 4. Terminal RUN-INVALID reading — licensed, one citation slip (F2)

- H1/H4's T1/T2 clearances were on the single-letter/outline shapes;
  H20 tests the entity-name shape. The draft's "clearances untouched"
  is licensed. ✓
- P5's entity-name-shape death is confirmed in the record:
  VERDICTREVIEW_EXP116_2026-09-29 documents the tail-echo failure
  ("the model echoed the unfinished sentence instead of completing
  it"). ✓
- **F2 (verdict-immaterial documentation fix):** the draft (and the
  LOG-4657 gate memo it transcribes) attributes P2's death to
  "EXP117". The record shows EXP117's 0/10 was the **P5-lineage
  priming slot** on the EXP091 bench (enumeration attractor —
  EXP117 report §3.7/line 42: "now EXP117 priming on the EXP091 bench
  0/10 enumeration"); P2's entity-name-shape death is **EXP115**
  (few-shot recitation, RUN-INVALID — confirmed by the EXP116
  verdict review: "P2 is dead on this shape (EXP115)"). The terminal
  license is unaffected (P2 is dead on this shape either way), so
  this is citation precision, not a bar or gate issue. Suggested
  placement: §8 as deviation 11, keeping §0's gate-memo transcription
  verbatim.

## 5. P4 hyperparameters and bench pins — VERIFIED

- §3.3 (`repetition_penalty=1.2`, `no_repeat_ngram_size=3`, greedy
  `do_sample=False`, `max_new_tokens=4`) matches EXP_PREREG_H7_EVALID
  §3.3 line 74 (T1-P4) **exactly**. ✓
- Bench: deterministic rebuild verified — 60 items; schema keys
  ⊇ {prompt, premise, tuple, phrasing, id}; `prompt == premise +
  QUESTION_SUFFIX` byte-exact on all 60; all 10 entities
  {Mars, Venus, Jupiter, Saturn, Mercury, Iron, Gold, Silver, Bronze,
  Steel} as listed. The canonical bench-JSON pin
  `e91b302f…` matches the executor convention (EXP121's BENCH_PIN).
  ✓

## 6. G1 non-application; no logit-slot leakage — VERIFIED

The "G1 not applied" statement (§2 defect class 4, §0.6) is correct:
G1 is a logit-slot validity guard; H20 is a generation apparatus with
no forward-pass scoring. Full-text scan: every "logit"/"mass" mention
is historical (EXP121's collapse, H18's void) or definitional (the G1
replacement statement). The method (§3) and the falsification tree
(§5) contain **no** logit reads, no mass scoring, no forward-pass
branch. §3.9's vacated Phase-0 is appropriate — no planner, no logit
slot, no composition whose tokenization could confound a readout.

## 7. No p-values — CORRECT, no fix needed

No p-value is registered and none is computed; the draft discloses
this twice (§2 defect class 1, §4) with the reason: the bars are
deterministic count rules on a full census of 60, registered before
the run — there is no sampling inference to wrap. This is Law #9
compliant (registered before any run) and honors the EXP120 lesson
by construction (nothing for a report author to hand-write). The §4
"Statistical honesty" paragraph discloses the design's limits
(``no 'close but not quite' region''). Adding a descriptive binomial
tail would be optional, not required; the current posture is the
honest one.

## 8. Tokenization pins — independently verified

Via the real Pythia-410m snapshot tokenizer
(`~/workspace/.exp086_weights/pythia-410m`, vocab 50254), reading
`tokenizer.json` directly: all 10 entity names exist as single vocab
entries with leading space — `ĠMars`→13648, `ĠJupiter`→34434 (both
matching the draft's examples), and likewise for the other eight.
A BPE encoding of a string exactly equal to a vocab token always
yields that single token, so the "every name fits the 4-token cap"
claim (§3.3) holds independently of the gate's check.

## 9. Other consistency notes (no action)

- No undefined identifiers (the H19 lesson): `QUESTION_SUFFIX`,
  `n_parseable`, `n_unparseable`, `E1`/`E2`, `e1`/`e2` are all defined
  at first use.
- §3.5's single-token re-assertion is correctly scoped as diagnostic
  (the parse rule is text-level); its "any deviation → apparatus
  void" clause is the conjunctive breaking point (§0.6), not a
  metric gate — consistent.
- §7.5 / §9 boundary correctly limits the terminal verdict to the
  EXP113-cleared protocol set on this shape (not generation in
  general, not H1/H4).
- The correctness-vs-`tuple[0]` count is registered decision-silent
  and reads no §5 branch — Law #7 compliant (labels touch only the
  diagnostic).

---

## Verdict: SIGN-WITH-FIXES

Two fixes, neither touching a bar, a gate, or the hypothesis:

- **F1 — launch-gating (minor, one pinned sentence):** pin the decode
  call in §3.3/§3.4 — generation text =
  `tokenizer.decode(new_token_ids, skip_special_tokens=True)`;
  input-prompt tokens never decoded into `raw`. (Law #13
  reproducibility pin; verdict-immaterial to the bars.)
- **F2 — verdict-immaterial (documentation):** correct the P2-death
  citation from EXP117 to **EXP115** (EXP117's 0/10 was the P5-lineage
  priming slot on the EXP091 bench), suggested as §8 deviation 11.

The bars are coherent, disjoint, and exhaustive; the unreachable-HELD
declaration is arithmetically correct; the counting partitions the 60
exactly; the parse rule is deterministic with all edge cases handled;
the terminal reading is licensed with H1/H4 untouched; P4 and bench
pins are byte-exact against their sources; G1 is correctly replaced;
the no-p-value posture is the honest one; and the tokenization claims
check out independently.

*Review lane: LOG-4659. $0 CPU. Single-lane fence respected — this
lane does not repair the draft, clear execution, or dispatch any
lane.*
