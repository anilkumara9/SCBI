# EXP117 (H11/PTTSC-GEN) Run Report — 2026-09-29

**Experiment number:** EXP117. **Pre-registration:** `research/prereg/EXP_PREREG_H11_PTTSCGEN_2026-09-29.md` (Law #14 SIGN-WITH-FIXES, LOG-4607; fix byte-verified, LOG-4608). **Execution lane:** LOG-4609. $0 CPU.

**Registered verdict: RUN-INVALID.** The Phase-0b decision-channel mini-gate fired: **0/10 probe items parseable** (< 8/10). No full run was licensed; no fidelity/decision metric exists. The hypothesis gets no verdict.

---

## 1. Preconditions (all verified before any generation, exactly per §3.1)

[FACT] All pins matched:

- Bench provenance SHA-256: `47281cd3dc243369be0aa5be2345663b752cdb4a329a16a37f08da5717230585` — MATCH; `len(bench) == 60`.
- Backbone LOG-331 pin `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed` matched **before the first generation** — Δθ=0 procedure per the EXP077/EXP084/EXP108 canonical convention (sorted `state_dict` keys, float32 tensor bytes). (The pre-reg's falsification tree routes the post-run pin check through the full-run branch only; Phase-0b RUN-INVALID exits the tree before it.)
- Planner-prompt byte-identity: the 60 §3.3-constructed planner prompts are **byte-identical (0/60 mismatches)** to the reference implementation of EXP113's signed `exp113_run.py` T2-P2 construction (`build_prompts`, lines 68–122). [Honesty note: EXP113's raw JSON (`exp113_raw.json`) does not store prompts, so the byte-identity is against the signed execution script's construction code — the closest reconstructible reference.]

Environment (Law #13): torch==2.14.0+cpu, transformers==5.17.0, numpy==2.5.3, accelerate==1.15.0; torch.manual_seed(0), numpy seed 0; CPU threads set 2, read back 2; `device_map="cpu"` honored exactly (accelerate present — the EXP113 precedent); float32; `model.eval()`; `torch.no_grad()` around all generations; greedy (`do_sample=False`) everywhere.

---

## 2. Phase 0a — recitation check (registered gate; 10 probe items)

[OBSERVATION] Planner generations (T2-P2, greedy, max_new_tokens=160) completed 10/10, zero exceptions. Outlines extracted per the H4 §3.3 rule (verbatim import).

**Literal gate (§3.7, the binding definition):** 0/10 probe items with ≥2 verbatim-recited outlines (gate: ≥6/10 → RUN-INVALID). **The gate did not fire.**

**Protocol-defect discovery [OBSERVATION]:** the literal §3.7 definition — "an outline recites iff it exactly equals (after strip + casefold) one of the 4 pinned exemplar OUTLINES" — compares extracted outlines against the marker-prefixed exemplar lines ("1. Restate ..."), but the §3.3 extraction rule strips the markers. Consequently a verbatim *content* recitation of the exemplar block (the EXP115 pathology applied to outlines) **cannot** satisfy the literal definition: the literal gate is non-binding for its target failure mode. This was verified by construction before the run (smoke tests) and confirmed empirically: the content-level diagnostic — comparison against marker-stripped exemplar content, reported as a diagnostic only, not a gate — shows **10/10 probe items with ≥2 content-level verbatim recitations**. The planner recited the exemplar block verbatim on every probe item; the literal gate scored 0/10. The paraphrase-recitation diagnostic (registered): mean max token-overlap vs exemplars = 0.7054.

[INTERPRETATION] Phase 0a's literal gate passed, but the diagnostic shows T2-P2's EXP113 "60/60 clearance" was, at the content level, format-recitation — exactly the risk §3.7 was written to catch, and the gate as pinned could not catch it. The independent verdict review must adjudicate the bindingness of the literal gate application (this lane applied it as written — Law #4; it did not rewrite the pre-reg mid-run).

Per the registered tree, Phase 0a passing (literal) licensed Phase 0b.

---

## 3. Phase 0b — decision-channel mini-gate (registered gate; 10 probe items)

[OBSERVATION] Baseline-slot generations (§3.5, greedy, max_new_tokens=16) completed 10/10, zero exceptions. Parsed per the §3.6 rule (generated tokens only; strip; trailing punctuation; case-insensitive exact match vs bench "A"/"C" entity names).

- **Parseable: 0/10** (gate: <8/10 → RUN-INVALID).
- Distinct parsed entity names: 0; minority: 0 (gate: <2 distinct or minority <2 → RUN-INVALID — also fails, moot).

**Failure mode [OBSERVATION]:** the model treats the priming slot as a *listing* task, not a selection: the dominant output shape is an enumerated list of entity names (`"\n\n1. Jupiter\n\n2. Mars\n\n3. Venus\n"`), which the exact-match parse rule scores UNPARSEABLE. One item began `"\n\nMercury\n\nMercury is the highest-ranked"` — an entity name followed by a continuation, also UNPARSEABLE under the registered exact-match rule. This is the 4th consecutive generation decision-channel failure on an entity-name slot: EXP109 sampled 80/80 unparseable, EXP115 few-shot 38/60 recitation, EXP116 priming 37/60 tail echo, and now EXP117 priming on the EXP091 bench 0/10 enumeration.

**No full run was licensed.** No planner/executor/baseline pipeline generations beyond Phase 0; no n_valid; no McNemar table; no decision bar read. Phase-0 records are diagnostics and never enter any metric (Law #9). Per the registered tree branch: `Phase 0b: <8/10 parseable → RUN-INVALID (no generation decision channel exists on this bench/shape; the hypothesis cannot be tested)`.

---

## 4. Verdict in the pre-registration's exact language

**RUN-INVALID** — the Phase-0b decision-channel mini-gate fired (0/10 parseable < 8/10). Not a verdict about planning; not evidence about the coordinator axis. The channel cannot speak on this bench/shape. (The worth-it gate's registered prediction for this branch: itself a boundary finding — no generation decision channel on the program's standard bench.)

Registered falsification-tree branch taken: `bench ok → backbone pin (pre) ok → prompts byte-verified ok → Phase 0a literal 0/10 (<6) pass → Phase 0b: 0/10 parseable (<8) → RUN-INVALID`.

---

## 5. Fences (from §7, honored)

1. This report kills/holds/continues nothing — H11's planning question was never tested.
2. The §3.7 protocol-defect finding is an [OBSERVATION] about the apparatus definition, not a verdict and not a license to rerun with a "fixed" gate — any re-derived gate is a separate pre-registered lane.
3. The token-asymmetry disclosure (§3.9) and the planning-vs-compute fence (§7.1) are moot — no metric exists to be fenced.
4. Not reasoning, not consciousness, not capability beyond this bench.
5. Novelty remains N1 — Known Combination.

---

## 6. Raw artifacts

- `~/workspace/SCBI/experiments/runs/EXP117_pttscgen/out/exp117_execute.py` (pinned script)
- `~/workspace/SCBI/experiments/runs/EXP117_pttscgen/out/exp117_generations.json` (20 records: 10 Phase-0a + 10 Phase-0b)
- `~/workspace/SCBI/experiments/runs/EXP117_pttscgen/out/exp117_result.json` (`verdict: RUN-INVALID`, no metric)
- `~/workspace/SCBI/experiments/runs/EXP117_pttscgen/out/exp117_stdout.log` + `exp117_console.log`
- Total wall time: 5.8 min; 20/20 generations completed; 0 exceptions.

**Environment note:** the pinned `device_map="cpu"` spec was honored exactly (accelerate==1.15.0 present in the execution venv) — the EXP113 precedent, not the EXP115/116 default-cpu fallback.
