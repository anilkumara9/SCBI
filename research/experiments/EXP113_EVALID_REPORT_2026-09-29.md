# EXP113 — H7/EVALID Execution Report (2026-09-29)

**Experiment:** EXP113 (H7 — EVALID: Elicitation Validation Instrument)
**Pre-registration:** `research/prereg/EXP_PREREG_H7_EVALID_2026-09-29.md` (signed, Law #14 SIGN)
**CEO launch:** LOG-4583. **Execution lane:** LOG-4584.
**Verdict: CONTINUE**

## Registered verdict (pre-reg §4, applied verbatim)

- r1 (T1 single-token): P1=0, P2=60, P3=0, P4=58, P5=60 → **T1-CLEAR = {P2, P4, P5}** (≥48/60)
- r2 (T2 numbered outlines): P1=24, P2=60, P3=0, P4=0, P5=60 → **T2-CLEAR = {P2, P5}** (≥48/60)
- Both T1-CLEAR and T2-CLEAR non-empty → **CONTINUE**: H1-revival and H4-revival lanes are licensable as NEW hypotheses, each naming its clearing protocol and each carrying its own elicitation-failure gate (e.g., the EXP108 `n_unparseable ≥ 7` gate). This does not revive H1/H4 themselves.

## Environment manifest (Law #13)

- torch==2.14.0+cpu, transformers==5.17.0, numpy==2.5.3, accelerate==1.15.0 (see honest note 1)
- CPU threads set=2, read back=2; seeds: torch 0, numpy 0; device=cpu, float32, greedy (`do_sample=False`)
- Backbone: `~/workspace/.exp086_weights/pythia-410m`, `model.eval()`, `torch.no_grad()` around all generations
- Backbone SHA-256 (sorted `state_dict` keys, float32, tensor bytes only — EXP077/EXP084/EXP108 canonical):
  - BEFORE: `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed` — matches LOG-331 pin
  - AFTER: `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed` — Δθ=0 confirmed
- Bench: 60-item EXP089 bench rebuilt verbatim via `benchmark_exp089.build_benchmark()`; provenance SHA-256 of `experiments/runs/EXP077_cone_vs_line/exp077_instance_records.json` = `47281cd3dc243369be0aa5be2345663b752cdb4a329a16a37f08da5717230585` — matches pin; `len(bench)==60` asserted

## Execution

- 600 generations completed (5 protocols × 2 tasks × 60 items), pinned order P1→P5, T1-then-T2, bench build order, no early abandonment, no mid-run modification
- Per-generation exceptions: 0/600. Empty generations: 2/600 (both T1-P4, items 45/50 — scored UNPARSEABLE per the registered rule; far below the 10% RUN-INVALID threshold)
- Deterministic re-parse ×2: byte-identical parse tables (assertion passed)
- No RUN-INVALID branch fired

### Honest implementation notes (deviations, both benign and documented)

1. **accelerate installed:** the pinned `device_map="cpu"` load requires `accelerate` under transformers 5.17.0 (same issue documented in EXP111). Installed `accelerate==1.15.0` ($0, CPU-only placement shim — no numeric effect) so the pinned `device_map="cpu"` spec is honored exactly, rather than dropping it as EXP111 did. Recorded in the environment manifest.
2. **T1-P2 exemplar answers:** "the true labels of items 0/1/2 as produced by the pinned builder" = the single letter `A` for all three (bench ground-truth labels are A=target per the H1 pre-reg; `ent` is always field `A`). Deterministic; per §3.1 cannot inflate the parseability metric. Few-shot block format: `Q: {PROMPT_i}` + T1-P1 question + `\nA: A` (×3), then `Q: {PROMPT_target}` + T1-P1 question + `\nA:`.
3. **T2-P2 exemplar format:** `{PROMPT_3}\n\n` + T2-P1 tail + `\n` + pinned outlines, `\n\n`-joined with the item-4 block, then `\n\n` + target item + T2-P1 tail. Documented exactly; no other construction was tried.

### Infrastructure incident (apparatus, not a verdict)

The first launch died silently at 180/600 generations with no traceback. `uptime` showed the VM had rebooted ~1 minute prior (up 1 min) — an infrastructure event, not a code or OOM failure. No metric had been read (the 180 partial records existed only in memory and were lost). Per Law #4 the partial data cannot be a result; the run was relaunched **from scratch** (full 600, same code/seeds/pins) and completed cleanly. The crashed attempt's console log is preserved as `exp113_console_crash1.log`. A write-only crash-recovery checkpoint (`exp113_raw_partial.json`, every 60 generations) was added before relaunch as a diagnostic; it was never read back and changed no number.

## Per-protocol results

| Protocol | T1 single-token (/60) | T2 numbered outlines (/60) |
|---|---|---|
| P1 verbatim baselines | **0** — 100% `\n\nQuestion:` echo (block_a=1.0); reproduces EXP108 exactly | **24** — planner-loop phrase on 16.7% (block_b); 24 items produced ≥2 real outlines |
| P2 few-shot | **60** ✓ CLEAR | **60** ✓ CLEAR |
| P3 explicit stop | **0** — first token is `'\n'` on all 60 | **0** — model rewrites the instruction instead of outlining |
| P4 repetition penalty | **58** ✓ CLEAR (2 empties) | **0** — penalty derails into off-distribution text |
| P5 priming | **60** ✓ CLEAR | **60** ✓ CLEAR |

Clearance (≥48/60): T1 → P2, P4, P5. T2 → P2, P5.

## Descriptive observations (change no verdict)

- T1-P2/P4/P5 outputs are exclusively the letter `A` — the format the exemplars/priming demonstrated. The registered metric is parseability only (§3.1: a constant "A" scores 60/60); this is format-following, not answer-correctness.
- Few-shot (P2) and priming (P5) clear 80% on **both** task shapes — the only protocols that do.
- Asymmetry: repetition penalty fixes T1 (58/60) but destroys T2 (0/60, derailed text). The explicit-stop protocols fail on both shapes.
- T2-P1's 24/60 shows the base model *can* emit numbered outlines under the verbatim planner prompt — just unreliably.

## Falsification-tree branch taken

`bench provenance ok → backbone pin ok → 600 generations (no early abandonment) → empty/exception rates ok → backbone pin (post) ok → re-parse byte-identical → T1-CLEAR={P2,P4,P5}, T2-CLEAR={P2,P5} → both non-empty → CONTINUE`

## What this does NOT claim (§7)

1. Parseable output ≠ reasoning, ≠ honesty, ≠ capability — the clearing protocols produced *formatted text*, nothing more.
2. CONTINUE validates the *elicitation methods only*. H1/H4 revival lanes are new hypotheses with their own pre-registrations and elicitation-failure gates.
3. Backbone-specific: base Pythia-410m, CPU, greedy — no claim about other models, instruction-tuned variants, or sampling regimes.
4. Novelty: N1 — Known Combination.

## Artifacts

- Raw records: `~/workspace/SCBI/experiments/runs/EXP113_evalid/out/exp113_raw.json` (600 records, parse table, counts, blocklist diagnostic, environment)
- Console: `exp113_console.log`; crashed first attempt: `exp113_console_crash1.log`
- Script: `~/workspace/SCBI/experiments/runs/EXP113_evalid/exp113_run.py`
