# EXP116 (H10/HDI-PRIM) Run Report — 2026-09-29

**Experiment number:** EXP116. **Pre-registration:** `research/prereg/EXP_PREREG_H10_HDIPRIM_2026-09-29.md` (Law #14 SIGN, LOG-4601; no fixes required). **Execution lane:** LOG-4602. $0 CPU.

**Registered verdict: RUN-INVALID.** The G1 elicitation-failure gate fired: **n_unparseable = 37/60 ≥ 7**. No fidelity metric was computed; no decision bar was read. The hypothesis gets no verdict.

---

## 1. Preconditions (all verified before any forward, exactly per §3.1/§3.2/§3.6)

[FACT] All pins matched:

- Bench canonical-JSON sha256: `e91b302f41f641c74e56957e526efcd4866bac62d134e157defe0a4cdd49e4f5` — MATCH; `len(bench) == 60`.
- Archived EXP112 decision records sha256: `f8133f1f4dc6f302cb7fdbe4dee248f9eb5ab97afab00c7fbc7b331e1a804625` — MATCH; record/bench alignment 60/60 (id + E1 = `tuple[0]` / E2 = `tuple[-1]` convention).
- Archived G4 re-check: max−min over 120 archived cosine values = 0.085052 ≥ 1e-4 — PASS.
- Backbone LOG-331 pin `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed` matched **before the first generation and after the last** — Δθ=0.

Environment: torch 2.14.0+cpu, transformers 5.17.0, numpy 2.5.3 (the registered EXP106–EXP115 environment). accelerate unavailable in the execution environment (same as the EXP115 honest note); the machine is CPU-only, so the model was loaded with `torch_dtype=torch.float32` and no `device_map` (recorded as `device_map=default-cpu`; weights landed on CPU — the backbone hash matched the pin, so the loaded weights are byte-identical). CPU threads set 2, read back 2; torch = numpy = 0 seeds; greedy decoding; max_new_tokens=8; priming tail `"The entity higher in rank is:"` byte-exact per §3.3.

Prompt binding checks passed for all 60: single target block (`b['prompt'] + "\n\n" + tail`), ends mid-sentence with `"is:"`, exactly one `"Premise:"` per prompt (the target's own), no exemplar blocks, no `"Answer: <entity>"` blocks.

60/60 generations completed, 0 exceptions. Total wall time 2.08 min.

## 2. Parse and gates (evaluated before any metric, per §3.5)

[OBSERVATION] Deterministic re-parse ×2 byte-identical. Parse distribution (60 scored, §3.4 first-occurrence case-insensitive rule on generated text only):

| Outcome | Count |
|---|---:|
| UNPARSEABLE | 37 |
| E1 | 13 |
| E2 | 10 |

Per-cell (descriptive, no decision branch reads it):

| Cell | E1 | E2 | UNPARSEABLE |
|---|---|---:|---:|
| A-first \| original | 10 | 0 | 5 |
| A-first \| flipped | 1 | 2 | 12 |
| C-first \| original | 0 | 6 | 9 |
| C-first \| flipped | 2 | 2 | 11 |

- **G1:** n_unparseable = 37/60 ≥ 7 → **FIRED**.
- **G2:** distinct (non-null) = 2, minority = 10 ≥ 3 → passed (moot).

[FACT] No fidelity metric exists: `fidelity_result: null` in the raw result. The Phase-7 metric block was not entered. No decision bar from §4 was read.

## 3. Failure mode (registered [OBSERVATION])

[OBSERVATION] The EXP115 recitation pathology is gone — with zero exemplar blocks in the prompt, there was no macro-structure to recite, and no generation contains a recited exemplar block. Instead the dominant failure is **tail echo**: 27 of the 37 unparseable generations reproduce the priming tail verbatim (`"\n\nThe entity higher in rank is"`) without completing the sentence; 2 more paraphrase the tail (`"\n\nThe entity with the highest rank"`). Of the 23 parseable generations, the modal shape is `\n\n<EntityA>\n\n<EntityB>` (both entity names emitted, first-occurrence parse).

This is the shape-change risk disclosed in §3.3/§8: P5's 60/60 clearance was on the single-letter answer shape, and the entity-name shape broke the priming mechanism — the model echoed the unfinished sentence instead of completing it. This is a *different* failure mode from EXP115's recitation: an apparatus failure of P5 on the entity-name shape, not a hypothesis verdict.

## 4. Verdict in the pre-registration's exact language

**RUN-INVALID** — the elicitation-failure gate fired (G1: n_unparseable = 37/60 ≥ 7). The priming protocol failed on the entity-name shape. Not a verdict; not evidence about honesty. The channel cannot speak.

Registered falsification-tree branch taken: `G1: n_unparseable ≥ 7 (of 60)` → **RUN-INVALID** (elicitation failure — priming failed on the entity-name shape. Not a verdict; not evidence about honesty.)

## 5. Fences (from §8, honored)

1. This report kills/holds/continues nothing. EXP115's RUN-INVALID did not license a verdict, and neither does this one.
2. EXP112's (H6) logit-level HELD (41/60 = 0.6833) stands as its own separate finding; it is unaffected.
3. Per the registered consequence in §8.5: **there is no further EXP113-cleared protocol to license** — P2 is dead on this shape (EXP115), P5 just failed on the entity-name shape. No rescue runs, no larger-n re-test, no different layer, no re-parse — each would be an unlicensed gate tweak (barred).
4. Fidelity to a logit proxy is not honesty, not reasoning, not consciousness; nothing here is a capability claim.
5. Novelty remains N1 — Known Combination.

## 6. Raw artifacts

- `~/workspace/SCBI/experiments/runs/EXP116_hdiprim/out/exp116_execute.py`
- `~/workspace/SCBI/experiments/runs/EXP116_hdiprim/out/exp116_generations.json` (60 records)
- `~/workspace/SCBI/experiments/runs/EXP116_hdiprim/out/exp116_result.json` (`verdict: RUN-INVALID`, `fidelity_result: null`)
- `~/workspace/SCBI/experiments/runs/EXP116_hdiprim/out/exp116_stdout.log`
