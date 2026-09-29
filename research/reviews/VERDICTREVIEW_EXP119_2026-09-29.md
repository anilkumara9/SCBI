# Independent Exact-Artifact Verdict Review — EXP119 (H14/PTTSC-LOGIT)

**Review lane:** LOG-4628 (pre-assigned, independent of the LOG-4627 execution lane).
**Review date:** 2026-09-29.
**Pre-registration:** `research/prereg/EXP_PREREG_H14_PTTSCLOGIT_2026-09-29.md` (Law #14 SIGN-WITH-FIXES LOG-4625; FIX-1 byte-verified LOG-4626).
**Report:** `research/experiments/EXP119_PTTSCLOGIT_REPORT_2026-09-29.md`.

## Verdict: BIND — the registered RUN-INVALID stands, no caveat.

Every binding count, gate decision, and pin was independently recomputed from the exact artifacts (`exp119_execute.py`, `exp119_result.json`, `exp119_stdout.log`, `exp119_console.log`). All match.

## Evidence (independently verified)

### 1. Falsification-tree path — followed exactly

Pre-reg §5 tree, reproduced branch by branch from the raw records:

| Tree node | Pre-reg rule | Observed (raw artifacts) |
|---|---|---|
| Bench provenance + schema + decomposition | mismatch → RUN-INVALID | canonical-JSON SHA-256 `e91b302f…058` MATCH, len=60; npz/embeddings/ids MATCH; `prompt == premise + QUESTION_SUFFIX` byte-exact 60/60 — pass |
| Backbone LOG-331 pin (pre) | mismatch → RUN-INVALID | `ec276abe…38e0ed` MATCH before first contact — pass (Δθ=0) |
| Planner prompts byte-identity vs EXP113 T2-P2 reference | mismatch → RUN-INVALID | 0/60 mismatches — pass |
| Phase 0a: planner bench-transfer | <8/10 planner-valid → RUN-INVALID | **10/10 planner-valid** (result.json `details`: all 10 items `planner_valid: true`) — did NOT fire |
| Phase 0b: logit slot with plan prefix | tokenization mismatch on ANY item → RUN-INVALID immediately (§3.7) | **fired on item 0** — plan-tail `[444, 37741, 27]` vs base-tail `[32, 37741, 27]`; console log: `FINAL VERDICT: RUN-INVALID (Phase 0b: tokenization mismatch on item 0 ...)`; `phase0b.details` empty — the run exited at the first probe item, per the "immediately" clause |
| Full run | never licensed | not reached; 60 fresh planner generations and 120 forwards never executed |

The script (`exp119_execute.py` lines 318–326) implements the §3.7 rule verbatim: the tokenization-identity check precedes both `forward()` calls; a mismatch writes the verdict and `return`s before any model forward in Phase 0b. **No forwards were run in Phase 0b.** The Phase-0 model contact was 10 planner generations only.

### 2. The tokenization mechanism — independently replicated, tokenizer-only (no model contact)

Using the venv's transformers and the snapshot tokenizer (`local_files_only`), I re-verified the exact claim:

- `tokenize(" Question: Who is higher in rank? Answer:")[-3:]` = `[32, 37741, 27]` — decode `('?', ' Answer', ':')`. Matches the report's base-tail byte-exactly.
- A plan-conditioned tail ending in `E` (report: the final outline ended with token `ĠE`): `[-3:]` = `[444, 37741, 27]` — decode `(' E', ' Answer', ':')`. Matches the report's plan-tail byte-exactly.
- Structural adjudication of the §0(6) breaking point: a plan block whose final outline ends in `?` (e.g. `"…Rank them? Answer:"`) gives `[-3:]` = `[32, 37741, 27]` — identical to baseline. Therefore the mismatch is **structural, not item-specific**: any plan block whose final outline does not end in `?` breaks the pinned [-3:] identity against the baseline's fixed `? Answer:` tail. The breaking point ("tokenization effects break the channel") was realized exactly as anticipated.

### 3. Phase 0a — verified

- 10/10 planner-valid from the result JSON's per-item detail records (n_outlines = 4 for every probe item; probe set {0,1,2,5,6,7,8,9,10,11} matches the pinned §3.7 set). Gate (<8) did not fire. Correct.
- The corrected recitation diagnostic: 10/10 probe items with ≥2 content-level verbatim recitations (result.json `content_recited_items_diagnostic: 10`). Diagnostic only — not a gate, per §3.7 and the §7.1.2 construct caveat. The report does not let it fire any gate. Correct.
- The 10/10 planner-validity is reported as an apparatus observation (T2-P2 transfers to the EXP107 bench as a plan elicitor), not a capability claim — the honesty fence (§7.1.3) holds.

### 4. Law #9 / Law #7 fences — clean

- No metric was read: `exp119_result.json` has `"items": []`, no per-item records, no McNemar table, no accuracy. Confirmed.
- `tuple[0]` as ground truth was never used for correctness — no correctness was computed. The BPE single-token re-assertion reads `tuple[0]`/`tuple[-1]` as E1/E2 strings (the H6-pinned tokenizer procedure, pre-registered §3.6), not as ground truth — no Law #7 violation.
- No per-site fidelity, no contrast, no decision bars read. The report states this explicitly; the raw artifacts confirm it.

### 5. Pins — all verified

- Bench, npz, embeddings-bytes, ids-bytes: all MATCH the pinned values (stdout + result.json worksheet agree).
- Backbone LOG-331 pre-contact pin MATCH. Post-contact pin was **not** re-checked — this is **compliant**: the §5 tree places the post-pin after the full run, which was never licensed; the report discloses this in §4 (Δθ=0 rests on the pre-pin plus eval/no_grad discipline; no training, no optimizer, no weight writes at any point). Not a defect.
- Planner prompt byte-identity: 0/60 mismatches (stdout). Environment manifest matches the registered envelope (torch 2.14.0+cpu, transformers 5.17.0, numpy 2.5.3, sklearn 1.9.1; seeds 0/0; threads 2/2). Wall 5.9 min, $0 CPU.

### 6. Fences — honored

- No verdict smuggled on the planning question: the report states the hypothesis "gets no verdict" in the pre-reg's exact language, and fences explicitly that H11's planning question is now untested on **both** EXP107 decision channels (generation dead per EXP117; plan-prefix logit slot dead per EXP119).
- The report licenses nothing and retires nothing except the exact tested composition (T2-P2 plan block between question and answer slot with the [-3:] identity requirement) — per the honesty fence §7.1.2.
- EXP112's HELD, EXP117's RUN-INVALID, and all prior statuses are untouched.

### 7. Record-keeping limitation — binding lesson recorded

The report discloses (§6) that raw Phase-0a generation texts were not persisted — only per-item counts/diagnostics are in the result JSON. Verified: no raw generation file exists in the run dir. The decisive verdict evidence (exact tail token ids on item 0) is fully present in the stdout log and result JSON, and the tokenization mechanism is independently re-verifiable tokenizer-only (done above) — so the verdict's evidentiary basis is intact. Nevertheless, this lane records the **binding lesson**: future execution lanes must persist raw generation records (and not just counts/diagnostics) before any verdict is written. Future pre-registrations should pin this as an artifact-existence gate.

## Verdict

**BIND.** EXP119's registered RUN-INVALID stands on the exact artifacts. The Phase-0b tokenization-mismatch branch was taken per the pre-registered §3.7 rule and §5 tree; the §0(6) breaking point was realized structurally and verified independently; no metric was read; all pins held; the fences are intact. No caveat applies to the verdict itself. The record-keeping limitation is recorded as a binding lesson, not a verdict defect.
