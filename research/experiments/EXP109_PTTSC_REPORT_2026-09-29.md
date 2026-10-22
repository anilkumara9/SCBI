# EXP109 (H4/PTTSC) Run Report — 2026-09-29

**Pre-registration:** `research/prereg/EXP_PREREG_H4_PTTSC_2026-09-29.md` (LOG-4547; independent review SIGN-WITH-FIXES LOG-4548; fixes applied LOG-4549; ALL-FIXES-VERIFIED → SIGN LOG-4550; CEO launch LOG-4551; execution lane LOG-4552)
**Lane:** LOG-4552 (execution only — no protocol, paper, or weight modification; no push; no GPU)
**Outcome: RUN-INVALID (elicitation failure; apparatus-failure tripwire also fires). No metric read. Not a verdict about planning.**

---

## 1. Environment [FACT]

- Backbone snapshot: `~/workspace/.exp086_weights/pythia-410m` (frozen)
- Environment: `~/workspace/.venv-exp077` — torch 2.14.0+cpu, transformers 5.17.0 (registered EXP106/EXP107 environment)
- Determinism pins: `model.eval()` before all generation; `torch.no_grad()` around ALL forward passes; `device_map="cpu"`; float32
- Executor script: `experiments/runs/EXP109_pttsc/exp109_run.py` (verbatim implementation of pre-reg §3.3–§3.8)
- Raw logs: `experiments/runs/EXP109_pttsc/out/exp109_raw.json` (108 generations, per-item)
- Analysis: `experiments/runs/EXP109_pttsc/out/exp109_analysis.json`; console: `out/exp109_console.log`
- Generation wall time: 20.9 min (108 generations; within the 1.5–3.5 h budget)

## 2. Integrity checks [OBSERVATION]

| Check | Pin | Observed | Result |
|---|---|---|---|
| Provenance SHA-256 (`exp077_instance_records.json`) | `47281cd3…0585` | `47281cd3…0585` | PASS |
| Bench size | 60 | 60 | PASS |
| Pilot scope | first 20 in build order, exactly 20 | items 0–19 (15× planet-2hop + 5× planet-3hop) | PASS |
| Backbone hash BEFORE | `ec276abe…38e0ed` (LOG-331) | `ec276abe…38e0ed` | PASS |
| Backbone hash AFTER | must equal BEFORE | `ec276abe…38e0ed` | PASS — Δθ=0, no quarantine |

## 3. Generation results [OBSERVATION]

| Item(s) | Planner outlines | Planner-valid (≥2 distinct non-empty) | Executor parseable | Baseline parseable |
|---|---|---|---|---|
| 0–14 (2hop) | 0 — degenerate repetition loop (see below) | No (×15) | 0/0 | 0/4 (×15) |
| 15, 17 (3hop) | 4 each — answer-enumeration, not plans (see below) | Yes (mechanical rule) | 0/4 each | 0/4 each |
| 16, 18, 19 (3hop) | 0 — degenerate repetition loop | No (×3) | 0/0 | 0/4 (×3) |

**Planner degenerate mode (18/20 items):** greedy decoding falls into a repetition attractor emitting only
`"Plan: Write a list of the possible answers to the question."` repeated — no `1.`–`4.` markers at all
(confirmed on run items 0–14, 16, 18, 19 and on 2 standalone diagnostic probe items). The pre-reg's
EXP108-degenerate-generation defense (planner-valid rule) caught this by construction.

**Items 15/17 "outlines":** the 4 extracted spans are candidate-answer enumerations
(e.g. `1. Saturn is the highest in rank. 2. Mars is the highest in rank. … 5. … 6. …`), not solution
outlines — a construct-validity observation. They satisfy the *mechanical* planner-valid rule (≥2 distinct
non-empty), but both items still fail item-validity because executor (0/4) and baseline (0/4) arms are invalid.

**Baseline:** 80/80 generations UNPARSEABLE across all 20 items — no sampled generation produced an exact
entity-name match (EXP108 echo mode at scale).

## 4. RUN-INVALID gates (§3.8) [OBSERVATION]

- **Elicitation-failure gate:** n_valid = 0 → 20 − n_valid = 20 ≥ 3 → **FIRES.**
- **Apparatus-failure tripwire:** 88/88 = 100% of executor + baseline vote-generations UNPARSEABLE ≥ 50% → **FIRES.**
- Backbone / provenance gates: PASS (no mismatch).

**Result: RUN-INVALID.** The script stopped after generation; no metric was read (per Law #6/#13 discipline —
no (b, c) table, no McNemar p, no per-arm accuracy exists for this run).

## 5. Verdict and licensing [FACT per §6]

**RUN-INVALID (elicitation failure).** Per the pre-registered falsification tree: *"The generation apparatus
failed; this is not evidence about planning."* It is not a verdict about the PTTSC hypothesis.

- Licenses: **nothing.** Retires: **nothing.** No re-runs, no larger-n re-test, no prompt tweak, no re-seed
  (each barred as an unlicensed gate tweak, §4).
- The coordinator axis is **not** retired for the piloted scope — a KILL requires net ≤ 0 on valid paired
  items, which does not exist here.
- A future planner-executor test would be a **separate pre-registered lane** with a re-derived elicitation
  design (the registered planner template demonstrably does not elicit outline-format output from this
  backbone under greedy decoding); it is not a continuation of EXP109.

## 6. Falsification-tree branch taken

`20 − n_valid ≥ 3` → **RUN-INVALID** (row 3 of §6; row 4 also satisfied). No hypothesis rewording occurred.

---

*Report finalized 2026-09-29. Execution lane closed; no follow-up dispatched (per lane brief).*
