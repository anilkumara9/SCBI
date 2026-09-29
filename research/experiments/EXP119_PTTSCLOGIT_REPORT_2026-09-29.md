# EXP119 — H14/PTTSC-LOGIT Run Report (2026-09-29)

**Experiment:** EXP119 (H14 — PTTSC-LOGIT: H11's planning question re-asked at the proven zero-generation logit level).
**Execution lane:** LOG-4627 (pre-assigned). **Pre-registration:** `research/prereg/EXP_PREREG_H14_PTTSCLOGIT_2026-09-29.md` (launch-eligible: Law #14 SIGN-WITH-FIXES LOG-4625, FIX-1 byte-verified LOG-4626).
**Status: RUN-INVALID** — Phase 0b tokenization-mismatch branch. The planning question was **not** tested; per pre-reg §2 this is an apparatus failure, not a verdict, and not evidence about planning.

Epistemological labels per `SCBI/AGENTS.md` §5: [FACT], [OBSERVATION], [INTERPRETATION].

---

## 1. Verdict (in exact pre-reg language)

**RUN-INVALID** — "any Phase-0 gate (§3.7), pin mismatch, baseline-reproduction failure, or the n_valid gate (§3.8) fires → the apparatus failed; the hypothesis gets no verdict. Not evidence about planning."

Registered branch taken (§5 falsification tree): **Phase 0b — tokenization mismatch (last-3 ids) on item 0 → RUN-INVALID (confound)**. Pre-reg §3.7: "the logit decision slot does not function with a plan prefix on this bench/shape; context-length or tokenization effects break the channel."

No McNemar table was computed and no decision bar was read (Law #9 — the metric is registered before output and is read only after all guards pass; the guards did not pass).

---

## 2. Pins verified before use [FACT]

| Pin | Expected | Result |
|---|---|---|
| Bench canonical-JSON SHA-256 | `e91b302f41f641c74e56957e526efcd4866bac62d134e157defe0a4cdd49e4f5` | MATCH, len=60 |
| npz bytes | `6cf4a8a726a2b6e4623f57d0287d95879866f77e789bcc3789fb693cf2af6a76` | MATCH |
| embeddings bytes | `9b6e8afb091ba1edbb0311ba1d3414d34a65942c3fdecb4533b69720f2a99123` | MATCH (60, 1024) float32 |
| ids bytes | `3669e102222719d66f61daca46ae1ac34e844e398ae433743a5b37bfc5075cb9` | MATCH; bench ids == npz ids 60/60 |
| Backbone LOG-331 (pre, before first model contact) | `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed` | MATCH (Δθ=0) |
| Bench schema (§3.1) | prompt/premise/tuple/phrasing/id; `prompt == premise + QUESTION_SUFFIX` byte-exact | 60/60 PASS |
| Planner prompts byte-identity (§3.3) | vs EXP113 T2-P2 reference construction | 0/60 mismatches |
| BPE single-token re-assertion (§3.6) | `" "+E1`, `" "+E2` each exactly one token, 120 texts | 120/120 PASS; ids match EXP112 worksheet pins |

Environment (Law #13): torch 2.14.0+cpu, transformers 5.17.0, numpy 2.5.3, sklearn 1.9.1, accelerate 1.15.0; torch/numpy seeds 0; threads set 2, read back 2; `device_map="cpu"`, float32, `model.eval()`, `torch.no_grad()` around all contact; greedy planner generations (`do_sample=False`, `max_new_tokens=160`). Wall time 5.9 min. $0 CPU.

---

## 3. Phase-0 gates [OBSERVATION]

Probe set: items {0, 1, 2, 5, 6, 7, 8, 9, 10, 11} (items 3–4 excluded — planner exemplars).

**Phase 0a — planner bench-transfer check:** planner-valid (≥2 distinct non-empty outlines per the H4 §3.3 extraction rule) = **10/10** (gate: <8 → RUN-INVALID). **Gate did NOT fire.** [OBSERVATION] T2-P2 transfers to the EXP107 bench as a plan elicitor — a small positive apparatus finding (EXP113's clearance was on the EXP091 bench).

**Phase 0a corrected recitation diagnostic (diagnostic only, NOT a gate):** items with ≥2 content-level verbatim recitations (marker-stripped both sides, strip+casefold) = **10/10**. [OBSERVATION] Replicates EXP117's construct caveat on a new bench: the T2-P2 plans on the EXP107 bench are substantially exemplar-recited. Per §7.1.2 the treatment is defined as "the T2-P2 plan text as generated"; this diagnostic fired no gate.

**Phase 0b — logit slot with plan prefix:** on the first probe item (item 0, planner-valid), the §3.7 tokenization-identity check failed:

- `tokenize(CONTEXT_PLAN)[-3:]` = **[444, 37741, 27]** → tokens `['ĠE', 'ĠAnswer', ':']`
- `tokenize(CONTEXT_BASE)[-3:]` = **[32, 37741, 27]** → tokens `['?', 'ĠAnswer', ':']`

[OBSERVATION] The final two tokens (`ĠAnswer`, `:`) are identical — the readout's final position is the same token — but the pinned rule requires the last **three** token ids to match, and the third-to-last differs: the baseline's `"...rank? Answer:"` carries `?` (id 32) where the plan-conditioned context carries the last token of the generated outline text (`ĠE`, id 444). Per §3.7 ("Tokenization mismatch on any single item → RUN-INVALID immediately (confound, not a rate)"), the run exited here. No forwards were run in Phase 0b; no further probe items were attempted.

[INTERPRETATION] The mismatch is structural, not item-specific: any plan block whose final outline does not end in `?` breaks the pinned [-3:] identity, because the baseline's tail is fixed as `? Answer:`. The §0(6) breaking point anticipated exactly this: "tokenization effects break the channel."

---

## 4. What was NOT reached

- No plan-arm or baseline-arm forwards were executed (Phase-0 records only: 10 planner generations).
- No per-item validity scoring, no baseline-reproduction check, no baseline-variation gate, no n_valid gate, no McNemar table.
- Per Law #7, the bench ground truth (`tuple[0]`) was never read — correctness was never computed.
- The backbone post-contact hash was not re-checked: the §5 tree places the post-pin after the full run, which was never licensed. Δθ=0 rests on the pre-contact LOG-331 pin plus the eval/no_grad discipline (no training, no optimizer, no weight writes at any point).

---

## 5. Honesty fence (§7.1, binding)

1. No verdict is smuggled on the planning question: H11's question remains untested — now on **both** decision channels on the EXP107 bench (generation channel dead per EXP117; plan-prefix logit slot dead per EXP119).
2. A future lane must change the plan-presentation design (e.g., a separately pre-registered context-controlled arm) — this run licenses nothing and retires nothing except the exact tested composition: T2-P2 plan block between question and answer slot with the [-3:] identity requirement.
3. Phase 0a's 10/10 planner-validity is an apparatus observation (T2-P2 transfers to the EXP107 bench), not a capability claim.
4. Novelty: N1 — Known Combination (unchanged).

---

## 6. Record-keeping limitation (disclosed)

The raw Phase-0a generation texts were not persisted to disk — only per-item counts and diagnostics (`n_outlines`, `planner_valid`, `n_recited_content_diagnostic`) are in `exp119_result.json`. The decisive evidence for the verdict (the exact tail token ids on item 0) is fully recorded in the stdout log and the result JSON, and the tokenization mechanism is independently re-verifiable with the tokenizer alone (no model contact). A future execution lane should persist raw generation records.

---

## 7. Artifacts

- Execution script: `experiments/runs/EXP119_pttsclogit/out/exp119_execute.py`
- Result JSON: `experiments/runs/EXP119_pttsclogit/out/exp119_result.json` (pins, Phase-0 counts, per-item detail records, verdict)
- Stdout log: `experiments/runs/EXP119_pttsclogit/out/exp119_stdout.log`
- Console log: `experiments/runs/EXP119_pttsclogit/out/exp119_console.log`

Falsification-tree path taken: bench ✔ → backbone pre-pin ✔ → planner byte-identity ✔ → Phase 0a 10/10 ✔ → Phase 0b item 0: tokenization mismatch → **RUN-INVALID**. No other branches exist.
