# Independent exact-artifact verdict review — EXP123 (H20/P4 apparatus validation)

*Lane: independent verdict review, LOG-4662 pre-assigned. $0 CPU. Fresh eyes.
Read-only on all signed artifacts; this lane writes only its own review file
and the pre-assigned LOG-4662 append. It does not re-run, repair, or
re-interpret the experiment.*

*Review date: 2026-09-29. Execution report under review:
`research/experiments/EXP123_P4APPARATUS_REPORT_2026-09-29.md`
(execution lane LOG-4661). Signed protocol:
`research/prereg/EXP_PREREG_H20_P4APPARATUS_2026-09-29.md`
(Law #14 signed, FIX-1/FIX-2 byte-verified at LOG-4660).*

---

## 1. Registered bars (protocol §4/§5, transcribed)

- **Exceptions > 6/60 → RUN-INVALID** (environment bug), checked first.
- **n_unparseable ≤ 6 → CONTINUE** (≥54/60 parseable clears EXP113's ≥48/60 bar).
- **n_unparseable ≥ 7 → RUN-INVALID, TERMINAL** on the entity-name shape
  (all EXP113-cleared protocols dead on this shape; honesty-instrument line
  closes permanently; H1/H4 T1/T2 clearances untouched).
- n_unparseable ≤ 6 AND n_parseable < 48 → HELD (declared arithmetically
  unreachable: n_unparseable ≤ 6 ⇒ n_parseable ≥ 54 at n=60).
- No inferential statistic registered; no p-value may appear (EXP120 lesson,
  honored by construction).

## 2. Independent re-verification from exact artifacts

All checks recomputed from `experiments/runs/EXP123_p4apparatus/out/`,
reading the raw files directly — never the lane's summaries.

### 2a. Independent re-parse of the 60 raw generation texts

The pinned §3.4 rule was re-implemented from scratch:
`raw.strip()` → `rstrip('.,;:!?\'")]}')` → case-insensitive exact match
against e1/e2 → parseable iff exactly one matches (XOR).

| Count | Lane claim | Independent recomputation |
|---|---|---|
| n_items | 60 | 60 (item_idx 0–59, unique) |
| n_parseable | 0 | **0** |
| n_unparseable | 60 | **60** |
| n_exceptions | 0 | **0** (exception flags all null; `exp123_exceptions.json` = `[]`) |
| Empty generations | — | 0 (all 60 are real, non-empty model outputs) |

- Zero mismatches against the lane's own `exp123_parse_table.json`
  (item-by-item comparison of all 60 rows).
- Lane's raw `output` strings in the parse table are byte-identical to
  the raw generation records in `exp123_generations.json` (asserted on
  all 60).
- No `p_value` appears in `exp123_result.json` or `exp123_parse_table.json`;
  none computed.

### 2b. Registered bars applied to the recomputed counts

- Exceptions 0 ≤ 6 → the apparatus bug branch does not fire.
- n_unparseable = 60 ≥ 7 → the elicitation-failure gate fires on the full 60.
- The lane's verdict **RUN-INVALID, TERMINAL** follows by direct
  application of the registered §4/§5 tree. No ambiguity, no discretion.

### 2c. Pins (protocol §3)

- **Bench:** canonical SHA-256 `e91b302f41f641c74e56957e526efcd4866bac62d134e157defe0a4cdd49e4f5`
  asserted at runtime (script line 114), len==60, schema keys present,
  `prompt == premise + QUESTION_SUFFIX` byte-exact on all 60 (script lines
  112–120, console `[13:49:04] bench pin OK`).
- **P4 hyperparameters:** `repetition_penalty=1.2, no_repeat_ngram_size=3,
  do_sample=False, max_new_tokens=4` asserted byte-identical to §3.3
  (script line 147–148, console `[13:49:20]`).
- **Decode pin:** `tokenizer.decode(new_token_ids, skip_special_tokens=True)`
  (script line 163); input-prompt tokens never enter the parse.
- **Deterministic rerun:** 60 pass-B generations byte-identical to pass-A
  (console `[13:51:32]`).
- **Re-parse ×2:** byte-identical parse tables (console `[13:51:34]`).
- **Token pin (diagnostic):** all 10 entities single-token with leading space.

### 2d. Backbone Δθ=0 (LOG-331)

Expected pin `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed`:
matched BEFORE the first model contact and AFTER the last (console
`[13:49:20]` and `[13:51:34]`, `exp123_result.json` gates backbone_pre/post
`ok: true`). Δθ=0 holds.

### 2e. Raw-artifact hash pins (independent SHA-256)

| Artifact | Claimed pin | Recomputed |
|---|---|---|
| `exp123_generations.json` | `662b9feb…f513c6` | **match** (byte-identical) |
| `exp123_result.json` | `3dc49c82…278340` | **match** (byte-identical) |

Raw records persisted before the verdict (defect class 2 satisfied).

### 2f. Research-log bookkeeping

LOG-4661 is exactly one entry, next-free after LOG-4660, dated 2026-09-29,
substance matches the artifacts (60/60 unparseable, 0/60 parseable,
0 exceptions, hash pins, terminal reading). Continuity intact.

## 3. Terminal reading check (§7/§9 of protocol)

The report's §1/§6/§8 correctly:

- leaves **H1/H4's T1/T2 clearances untouched** (58/60-class on their own
  shapes; the verdict never speaks about them);
- states the **honesty-instrument line closes permanently on the
  entity-name shape** — no protocol rescue, no larger-n rescue, no
  parameter tweak licensed;
- does not rescue EXP112's bench-2 logit line (a different instrument);
- keeps the label-free race tied at zero;
- reads the expected outcome as a finding, not a failure (the pre-reg
  predicted P(n_unparseable ≥ 7) ≈ 1 under P4-dead).

No scope creep, no summit overclaim. Novelty stated as N1 — Known
Combination.

## 4. Verdict

**BIND — no caveat.**

The execution lane's RUN-INVALID (terminal) verdict is correct on the
exact artifacts: independently recomputed n_parseable=0/60, n_unparseable=60/60,
n_exceptions=0, all pins hold, all hash pins match, the registered
elicitation-failure gate fires at n_unparseable=60 ≥ 7, and the report's
terminal reading stays inside the licensed scope. The honest headline
stands: the entity-name generation channel is dead on all EXP113-cleared
protocols (P2 dead on this shape, P5 dead on tail echo, P4 dies here).

*Single-lane fence respected: this lane reviews and reports; it does not
self-clear, scoreboard-sync, or dispatch downstream work.*
