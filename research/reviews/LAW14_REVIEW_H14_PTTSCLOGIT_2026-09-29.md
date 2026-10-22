# Independent Law #14 Review — H14 (PTTSC-LOGIT)

**Review lane:** LOG-4625 (pre-assigned). **Status:** independent of the drafting lane (LOG-4624). **Verdict: SIGN-WITH-FIXES** — launch-eligible pending one documentation-precision fix; no design flaw found.
**Reviewed artifact:** `research/prereg/EXP_PREREG_H14_PTTSCLOGIT_2026-09-29.md` (read in full, all 10 sections §0–§9; zero truncation placeholders verified).
**Reference documents read in full:** EXP112 run report (`EXP112_HDILR_REPORT_2026-09-29.md`), H6 pre-registration (`EXP_PREREG_H6_HDILR_2026-09-29.md`), H11 pre-registration (`EXP_PREREG_H11_PTTSCGEN_2026-09-29.md`), `build_exp107_bench.py` (builder source, lines 1–180), `exp112_per_item.json` (archived records schema).
**Method:** every binding number independently recomputed; every factual citation checked against the cited source; the deviation list swept against the body (the H9-review lesson). No model runs, no signed artifact modified, $0 CPU.

---

## Checklist results

### 1. Bars/numbers — all verified, tiling gapless, no razor-thin CONTINUE

All seven §4 McNemar one-sided exact p-values independently recomputed from first principles (p = P(X ≥ b | n = b+c, 0.5)):

| (b, c) | net | recomputed p | draft's p | match |
|---|---|---|---|---|
| (5, 0) | +5 | 0.03125 | 0.03125 | ✓ |
| (4, 0) | +4 | 0.0625 | 0.0625 | ✓ |
| (6, 0) | +6 | 0.015625 | 0.015625 | ✓ |
| (6, 1) | +5 | 0.0625 | 0.0625 | ✓ |
| (7, 1) | +6 | 0.03515625 | 0.03515625 | ✓ |
| (9, 2) | +7 | 0.03271484375 | 0.03271484375 | ✓ |
| (8, 3) | +5 | 0.11328125 | 0.11328125 | ✓ |

The §0(4) shorthand ((5,0) → 0.03125 CONTINUE; (4,0) → 0.0625 HELD; (6,1) → 0.0625 HELD) matches. Tiling: p ≤ 0.05 with b > c → CONTINUE; net (b−c) ≤ 0 → KILL; net > 0 with p > 0.05 → HELD. Every (b, c) region lands in exactly one verdict (b = c → net 0 → KILL; b < c → KILL; all consistent with the pre-registered rule). Minimum practical CONTINUE (5, 0) at p = 0.03125 is not razor-thin and matches the H11-licensed bars. The HELD zone absorbs (4,0) and (6,1) by construction.

### 2. The §3.7 lesson — genuinely fixed, not renamed

Verified: the draft does NOT reuse H11 §3.7's structurally-inert literal recitation definition (adjudicated inert at LOG-4610). Instead: (i) Phase-0a gates on the structural planner-valid rule (≥2 distinct non-empty outlines — content-agnostic); (ii) the corrected content-level recitation diagnostic compares **marker-stripped exemplar content vs marker-stripped extracted outlines** (strip+casefold, both sides) — the LOG-4610 defect was stripping on the extraction side only; (iii) the diagnostic is explicitly diagnostic-only, not a gate; (iv) EXP117's 10/10 content-recitation finding is disclosed as a construct caveat (§7.1.2) and the treatment is defined as "the T2-P2 plan text as generated". This is a real fix, not a rename.

### 3. Token-asymmetry fence — airtight

H11 §3.9/§7.1 carried over and adapted (§3.9, §7.1 item 1): "A CONTINUE licenses the plan-text-conditioned **pipeline** as an adaptive-loop component — it does **not** license the claim that *planning* (vs additional context tokens, vs plan-shaped text as extra context) caused the change." No claim in the draft lets a CONTINUE be read as planning capability. The fence's force covers positional effects of the longer context as part of "additional context tokens" — positional shift is a consequence of the disclosed treatment cost, not a separate unlicensed attribution. No fix required.

### 4. Integrity checks — operationally specified, not aspirational

- **Phase-0b tokenization identity** (§3.7): `tokenize(CONTEXT_PLAN)[-3:] == tokenize(CONTEXT_BASE)[-3:]`, pinned, mechanical, fires RUN-INVALID immediately on any single mismatch. Self-arbitrating.
- **Baseline-reproduction check** (§3.8): 60/60 match against `exp112_per_item.json`'s `readout` field. Verified the field exists (archived records carry `readout` among 18 fields; 60 records). Byte-identical baseline context + deterministic greedy forwards + the §3.2 41/60-exact consistency precedent make this a genuine apparatus-drift arbiter. Self-arbitrating.
- The §3.4 decomposition assertion (`{PREMISE} + QUESTION_SUFFIX == {PROMPT}` byte-exact) is real: verified `build_exp107_bench.py` line 124 (`'prompt': premise + QUESTION_SUFFIX`) and line 53 (`QUESTION_SUFFIX = " Question: Who is higher in rank? Answer:"` — byte-exact match to the draft's string).

### 5. Law #7 posture — verified, one citation fix required (FIX-1)

The metric (accuracy vs `tuple[0]`) uses labels **only at metric time** — never during planner generation, never during readout, never in gating. This is Law #7-clean. The ground-truth construct is sound: the builder's flip is meaning-preserving (module docstring: "re-anchoring subject/object so the ranking meaning (A > B > C [> D]) and the target's sentence position ... are preserved"), so `tuple[0]` = A is the highest-ranked entity — the correct answer to "Who is higher in rank?" — on all 60 items, both phrasings, both flip states. H6 §3.2 independently pins "E1 = `tuple[0]` (the target entity)".

**Defect (documentation-precision):** §2 cites the builder as `"Label semantics: target (tuple[0])"`. The actual comment (line 167) is:
`# Label semantics: target (tuple[0]) in first premise sentence iff A-first.`
The draft's truncation drops the qualifier, and the full comment is a *positional* check on the bench text — it does **not** establish `tuple[0]` as the ground-truth answer. The ground-truth status comes from the module docstring's meaning-preservation and H6 §3.2's pinning. The conclusion is correct; the citation as written is misleading. FIX-1 corrects it (exact wording below). §8 item 19's "(EXP107 label semantics)" is vague but not a false quotation; it is corrected by the same fix for precision.

### 6. Deviations — complete (20 items), body swept, no undocumented thirteenth

§8 lists 12 adaptations vs H6 and 8 vs H11. Each was verified genuine against the body. The body was swept section by section (§0–§9) for unlisted spec differences: the bench-schema assertion (§3.1), decomposition assertion (§3.4), `<2048` assertion, and exception rule (§3.8) are validity assertions that can only fire RUN-INVALID — they change no decision region and are subsumed by the listed bench/apparatus adaptations (observation, not a required fix). The probe-item set, generation spec, and McNemar license are correctly recorded in the "Unchanged from H11" note. Zero truncation placeholders: all 10 sections present and complete.

### 7. Laws #4/#7/#9/#13 — compliant

- **Law #4:** bars binding; §4 "Any hypothesis rewording after seeing outputs → BARRED"; §5 tree has no re-runs, no larger-n rescue, no template modifications mid-run.
- **Law #7:** §2 "only at metric time"; planner exemplars are format demonstrations (correctness irrelevant). Clean.
- **Law #9:** Phase-0 records are diagnostics, never metric inputs; the full run regenerates all 60 items fresh (§3.2, §3.7). The metric is registered before any model contact.
- **Law #13:** seeds (torch=numpy=0), threads set and read back, environment manifest pinned, LOG-331 hash before/after, byte-identity checks, deterministic re-read ×2. The 60 planner generations + 120 forwards are $0 CPU-licensable (calibrated against EXP112's 180 forwards in ~86 s and EXP117's 20 generations in 5.8 min — the stated ~20–30 min envelope is honest).
- **Law #6:** Δθ=0, hash before first and after last model contact; quarantine on mismatch. **Law #11:** epistemological labels used throughout.

### 8. Worth-it gate (§0) — genuinely new

H14 is not a silent revival: H11's planning question was never tested (EXP117 RUN-INVALID at Phase 0b — apparatus failure, not hypothesis failure); H6 tested honesty without planning; EXP113 tested elicitation, not decisions. New data (60 fresh planner generations + 120 fresh logit forwards), new apparatus composition (H11's question × H6's proven channel on H6's bench), new experiment number licensed. The gate's PASS stands. The §0(6) invitation to REJECT on recitation-confound grounds was considered and declined: the causal question (does the plan text change the logit decision?) is answerable regardless of outline quality, the fence denies planning attribution, and a KILL is informative either way.

---

## FIX-1 (required before launch — citation precision, §2 and §8 item 19)

The §2 parenthetical currently reads:

`correct iff the decision entity equals the bench record's `tuple[0]` (the target entity per the bench builder's registered label semantics — `build_exp107_bench.py`: "Label semantics: target (tuple[0])"; ents are ordered highest-ranked first, and the flip preserves ranking meaning).`

Replace with the following exact wording:

`correct iff the decision entity equals the bench record's `tuple[0]` (the target entity per the bench builder's registered construction — `build_exp107_bench.py` module docstring: the meaning-preserving flip keeps "the ranking meaning (A > B > C [> D]) ... preserved", so `tuple[0]` = A is the highest-ranked entity on all 60 items; pinned independently by H6 §3.2: "E1 = `tuple[0]` (the target entity)").`

And in §8 item 19, replace `(EXP107 label semantics)` with `(EXP107 bench: `tuple[0]` = A, the highest-ranked entity under the meaning-preserving flip — H6 §3.2)`.

Rationale: the truncated comment quotation is misleading (the full comment is a positional check, not a ground-truth license). The conclusion is correct; the citation must be.

## Observations for the launch lane (not defects, no fix required)

- **O1.** The "Unchanged from H11" completeness note lists "the T2-P2 planner template and exemplars (§3.3)": the template, outline lines, and exemplar *indices* are unchanged, but the exemplar *prompts* are bench-dependent (EXP107 items 3–4 here vs EXP091 items 3–4 in H11). The binding §3.3 spec is unambiguous ({PROMPT} = the EXP107 bench prompt field), and §3.3's honesty note discloses the bench difference. No executor can follow the spec and use the wrong bench.
- **O2.** The §3.3 byte-identity check's phrasing ("byte-identical to the H11 §3.3 construction") is slightly odd — a prompt is byte-identical to a prompt, not to a construction — but the parenthetical ("the signed H11 pre-registration §3.3 code-equivalent construction") makes the procedure operationally clear, and the check is self-arbitrating (RUN-INVALID on mismatch, never silently wrong).

---

## Verdict

**SIGN-WITH-FIXES.** The science is licensed: the question is new, the bars are binding and correctly computed, the fences are airtight, the §3.7 lesson is genuinely honored, and the integrity checks are operational. One documentation-precision fix (FIX-1) before the CEO launch decision. Fix-verification is a separate lane.
