# EXP123 execution report — H20: P4 repetition-penalty apparatus validation on the entity-name shape

*Lane: EXP123 execution, LOG-4661 pre-assigned. $0 CPU. Read-only on the
signed pre-registration (no signed artifact modified). Execution of the
signed pre-registration
`research/prereg/EXP_PREREG_H20_P4APPARATUS_2026-09-29.md` (Law #14 signed,
two fixes byte-verified). This lane mints EXP123.*

*Execution date: 2026-09-29.*

---

## 1. Headline

**Verdict: RUN-INVALID, TERMINAL** — the elicitation-failure gate fired on
the full 60: **n_unparseable=60/60 ≥ 7**. Per the registered §4/§5 bars,
the entity-name generation channel is dead on **all** EXP113-cleared
protocols (P2 died on this shape, P5 died on tail echo, P4 dies here). The
honesty-instrument line closes **permanently on this shape** — no protocol
rescue, no larger-n rescue, no parameter tweak is licensed. This is the
*expected* outcome under the P4-dead alternative (the pre-reg predicted
P(n_unparseable ≥ 7) ≈ 1): a finding, not a failure. H1/H4's T1/T2
clearances on their own shapes are untouched. The label-free race stays
tied at zero.

## 2. Execution record

| Item | Value |
|---|---|
| Bench | Verbatim EXP107 60-item template-decorrelated bench; canonical SHA-256 `e91b302f41f641c74e56957e526efcd4866bac62d134e157defe0a4cdd49e4f5`; npz `6cf4a8a7…`; embeddings-bytes `9b6e8afb…`; ids-bytes `3669e102…`; schema + `prompt == premise + QUESTION_SUFFIX` assertions all pass |
| Backbone | Frozen Pythia-410m (`~/workspace/.exp086_weights/pythia-410m`), `device_map="cpu"`, float32, `model.eval()`, `torch.no_grad()` on all generations |
| Backbone pin (LOG-331) | `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed` — **match BEFORE and AFTER** all 120 generations; Δθ=0 |
| Decoding (P4, §3.3) | `repetition_penalty=1.2`, `no_repeat_ngram_size=3`, greedy (`do_sample=False`), `max_new_tokens=4`; asserted byte-identical to §3.3 |
| Environment | torch 2.14.0+cpu, transformers 5.17.0, numpy 2.5.3; seeds torch=0, numpy=0; CPU threads set and read back |
| Generations | 60 pass-A (primary) + 60 pass-B (deterministic rerun, fixed seeds) = 120; **byte-identical** |
| Per-generation exceptions | **0/60** (exception gate: >6 → RUN-INVALID; did not fire) |
| Token pin (§3.5) | All 10 entities (Mars, Venus, Jupiter, Saturn, Mercury, Iron, Gold, Silver, Bronze, Steel) single-token with leading space — re-asserted |
| Decode pin | `tokenizer.decode(new_token_ids, skip_special_tokens=True)`; input-prompt tokens never decoded into `raw` |
| Raw records | `exp123_generations.json` persisted + hash-pinned **before the verdict**: SHA-256 `662b9feb0cbe7e458eae5b4d4542e7c7495bacaa5fef72ae5331013784f513c6` |
| Re-parse ×2 | Parse tables **byte-identical** |
| G1 | Not applicable by registration (§2.4) — generation apparatus, no logit slot read |

## 3. Counts (the registered numbers)

| Count | Value |
|---|---|
| n_items | 60 |
| n_parseable | **0** |
| n_unparseable | **60** |
| n_exceptions | 0 |
| Correctness diagnostic (decision-silent): names-e1 | 0 of 0 |
| Correctness diagnostic (decision-silent): names-e2 | 0 of 0 |

No p-values registered; none computed (Law #9 compliant — the bars are count
bars).

## 4. What the generations actually look like

All 60 generations are real, non-degenerate model outputs — this is a
genuine signal, not a decode artifact:

- 18 distinct outputs across 60 items; all are continuation-attractor text,
  e.g. `' Mercury, the planet'`, `' The Sun, the'`, `' The one who has'`,
  `' The highest ranked person'`, `' Gold, Silver and'`.
- The most common single output (`' The one who has'`, 12/60) never names
  either candidate entity.

This matches the pre-reg's breaking mechanism [INTERPRETATION]:
`repetition_penalty=1.2` down-weights tokens already present in the input
context — including the entity-name tokens in the premise — biasing
*against* emitting the entity name, compounding EXP117's enumeration and
continuation attractors (EXP113's own T2 datum: P4=0/60 on outlines).
On the entity-name shape, P4 is not an elicitation protocol at all; it is
an anti-elicitation protocol.

## 5. Falsification-tree path taken

bench provenance + len==60 + schema → ok → backbone LOG-331 pin (pre) → ok
→ P4 hyperparameters asserted byte-identical → ok → full run: 60 greedy P4
generations (no early abandonment) → exceptions 0/60 (gate ok) → backbone
pin (post) → ok → raw generation records persisted + hash-pinned → ok →
re-parse ×2 byte-identical → ok → **elicitation-failure gate on the full
60: n_unparseable=60 ≥ 7 → RUN-INVALID, TERMINAL**.

No deviation from the pinned bench, hyperparameters, or parse rule at any
point. No HELD branch reachable (declared unreachable by arithmetic, §4).
No p-value computed or needed.

## 6. Honest frame

- A parseable-rate of 0/60 closes the entity-name **generation** channel
  across all EXP113-cleared protocols. It does **not** speak about H1/H4's
  T1/T2 clearances (58/60-class on their own single-letter and outline
  shapes), which are untouched.
- It does not rescue EXP112's bench-2 logit line (a different instrument,
  dead on a different apparatus). The label-free race stays tied at zero.
- Parseability ≠ correctness (registered): the 0/60 is a *format*
  measurement — the model never produced a text that exactly matches either
  candidate entity name. The decision-silent correctness diagnostic is
  vacuous (0 of 0).
- Backbone-specific (base Pythia-410m, CPU), bench-specific (EXP107),
  protocol-specific (P4 decoding). Novelty N1 — Known Combination (registered).

## 7. Artifacts

- Executor: `experiments/runs/EXP123_p4apparatus/out/exp123_execute.py`
  (SHA-256 recorded in result)
- Raw generations: `out/exp123_generations.json` (SHA-256
  `662b9feb0cbe7e458eae5b4d4542e7c7495bacaa5fef72ae5331013784f513c6`)
- Exceptions: `out/exp123_exceptions.json`
- Parse table: `out/exp123_parse_table.json`
- Result: `out/exp123_result.json` (SHA-256
  `3dc49c821fed8fc114167c63ad1680cd4fe3c0025a4e15d4783409064972873d`)
- Console: `out/exp123_console.log`; stdout: `out/exp123_stdout.log`

## 8. Next steps (licensed)

None on the entity-name generation shape — the terminal verdict closes the
line permanently. Downstream lanes must not re-run P4 or any EXP113-cleared
protocol on this shape. Independent exact-artifact verdict review of this
report (Law #14 / verdict-review discipline) is the next licensed action.

---

*Single-lane fence respected: this lane executes and reports; it does not
self-review, self-clear, or dispatch downstream work.*
