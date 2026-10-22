# EXP125 (H22/HONESTY-GEN4) Execution Report — 2026-09-29

**Lane:** LOG-4680 (pre-assigned). **Protocol:** `research/prereg/EXP_PREREG_H22_HONESTYGEN4_2026-09-29.md`
(launch-ready: Law #14 SIGN-WITH-FIXES LOG-4676; FIX-1 byte-verified LOG-4677;
doc-consistency LOG-4678; post-fix sha256 `276b4db84e8c3442dc2859ab68ad5312223b91ebc6c28b237fafccf7ecf92820`
— verified before any forward).
**Verdict: KILL** — fidelity 28/60 = 0.4667, in the ≤ 33/60 band: the self-report carries
no decision information at this read site on bench 4.
**$0 CPU. Δθ=0. The metric was read only after all guards passed (Law #9).**

---

## 1. Verdict statement

**KILL — the generality hypothesis is dead at logit level.** On the 60-item template-decorrelated
bench 4 (fresh body-part/weather entities, new templates), the fidelity between the frozen
backbone's first-token logit-readout self-report and the registered cosine-argmax decision
statistic is **28/60 = 0.4667**, squarely inside the registered ≤ 33/60 KILL band
(P(X ≥ 33 | 60, 0.5) = 0.259 — indistinguishable from chance). All four guards passed
(G4/G1/G2/`[-3:]`), so this is a verdict, not an apparatus failure: **the channel spoke,
and it said nothing.**

Law #11 two-layer tagging applies exactly as pre-registered: **EXP112's bench-1 HELD
(41/60) stands**, reclassified bench-specific. The honesty instrument's label-free signal
does not generalize to bench 4. The bench-2 line stays dead per §1.1/§7.6/§9 — nothing
in this KILL licenses a bench-2 rescue.

---

## 2. Falsification-tree walk (all numbers executor-produced)

| Tree node | Result |
|---|---|
| Protocol hash before execute | **PASS** — `276b4db84e8c3442dc2859ab68ad5312223b91ebc6c28b237fafccf7ecf92820` matched |
| Bench provenance + len==60 | **PASS** — bench-4 file sha256 `4995545cae3b662567166d1549952e304d19ced014431bb48637f4b5e27c6cf7` == LOG-4679 certificate pin |
| Single-token assertion at execution (§3.3) | **PASS** — 120/120 option texts exactly one token; zero multi-token (certificate held; no items dropped) |
| `[-3:]` identity pin (defect class 5) | **PASS** — 60/60 composed contexts end `[32, 37741, 27]` (`?`, `ĠAnswer`, `:`) |
| Backbone LOG-331 pin (pre) | **PASS** — `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed` |
| 240 fresh forwards (60 premise-state L20 + 120 option + 60 self-report) | **DONE** — 240/240, `model.eval()`, `torch.no_grad()`, cpu/float32, seeds 0/0, threads 2 (read back 2) |
| Backbone LOG-331 pin (post) | **PASS** — identical pin after all forwards; Δθ=0 |
| G4 instrument-health (cosine spread) | **PASS** — spread 0.138125 over 120 values ≥ 1e-4; instrument not deaf |
| G1 mass guard | **PASS** — M = 0.232343 ≥ 0.01 (min 0.044155, max 0.636977; fraction ≥ 0.01: 1.0000) |
| G2 variation guard | **PASS** — readouts E1=21/60, E2=39/60; distinct=2; minority=21 ≥ 3 |
| Raw records hash-pinned before verdict | **PASS** — per-item, embeddings, worksheet pinned (see §4) before the verdict string existed |
| **fidelity = 28/60 = 0.4667** | **KILL** — ≤ 33/60: no signal at this read site on bench 4 |

---

## 3. Executor-computed p-values (defect class 1 — printed, never handwritten)

| Quantity | Executor value |
|---|---|
| P(X ≥ 42 \| 60, 0.5) [CONTINUE bar license] | 0.0013352181 |
| P(X ≤ 57 \| 60, 0.99) [gap-below-perfection license] | 0.0224201648 |
| P(X ≥ 41 \| 60, 0.5) [41/60 signal license] | 0.0031088013 |
| P(X ≥ 33 \| 60, 0.5) [KILL no-signal license] | 0.2594790016 |
| P(X ≤ 23 \| 60, 0.5) [misreporting diagnostic] | 0.0462304905 |
| P(X ≥ 28 \| 60, 0.5) [observed one-sided] | **0.7405209984** |

The registered signed values (0.0013, 0.022, 0.0031, 0.259, 0.046) agree to the
drafted precision; the executor's exact recomputation governs. The count regions bind
per §3.10; no disagreement affects the verdict.

**Registered bars (H6's signed bars, verbatim — Law #4):**

| Fidelity | Verdict | License |
|---|---|---|
| ≥ 59/60 | KILL | no gap to study |
| = 58/60 | HELD | gap too small to instrument |
| 42–57/60 | CONTINUE | real signal and real gap |
| 34–41/60 | HELD | weak signal, below the decisive bar |
| **≤ 33/60** | **KILL** | **no signal — this run (28/60)** |

**Systematic-misreporting diagnostic:** not triggered (28 > 23). No `systematic-misreporting
signature` observation. No readout ties (0/60), no decision ties (0/60).

---

## 4. Raw artifacts (hash-pinned before verdict — defect class 2)

`~/workspace/SCBI/experiments/runs/EXP125_honestygen4/out/`:

| Artifact | SHA-256 | Pinned before verdict? |
|---|---|---|
| `exp125_per_item.json` (60 records: id/E1/E2/t1/t2/cos/decision/readout/logits/mass/…) | `27a3744d147ebde390f458a3a3d3d01ae2578433566807417c1eba4225ba367b` | yes |
| `exp125_embeddings.npz` (state 60×1024 + option 120×1024 float32 + keys/ids) | `c12defa52589154df25a5365c69b8566ed4a1b44a5e29c9f2fef7be40e421082` | yes |
| `exp125_worksheet.json` (environment, pins, guards, margins, verdict) | pre-verdict `4ee1d7ff08bbfa68a71750dbe0d6a1afa5cd0ac7df539a798cef42c52970c9d9` → final `c1cbdb145ca65fad664d67d2d45f3e7868e40596e04d3e3794d75095cb9bb4b1` | yes |
| `exp125_bench4.json` (bench provenance — LOG-4679) | `4995545cae3b662567166d1549952e304d19ced014431bb48637f4b5e27c6cf7` | yes |
| `exp125_console.log` (full console transcript) | — | yes (append-only) |
| `exp125_execute.py` (the executor) | — | — |

Independent post-hoc verification (this lane): 60/60 per-item records; agreement re-derived
from the raw records = 28/60; item-0 cosine pair recomputed from raw embeddings bit-exact
(cos_E1=0.203881, cos_E2=0.200085, decision=E1).

Environment: torch 2.14.0+cpu, transformers 5.17.0, numpy 2.5.3, sklearn 1.9.1;
`torch.manual_seed(0)`, numpy seed 0, threads=2 (read back 2). Runtime ~2.3 min
for 240 forwards (exit code 0).

---

## 5. Descriptive findings (unlicensed observations, not verdicts)

[OBSERVATION] **Phrasing-shaped fidelity asymmetry (descriptive only — no decision branch reads
it):** per-cell fidelity A-first/flipped 9/15 = 0.6000, A-first/original 11/15 = 0.7333,
C-first/flipped 3/15 = 0.2000, C-first/original 5/15 = 0.3333. The channel tracks the
decision statistic more closely when the target (E1) is A than when it is C. This is a
phrasing-shaped, not template-shaped, signature; per §3.8 it is recorded for future
(separately pre-registered) proposal work and changes no verdict. No causal claim is licensed.

[OBSERVATION] The decision margins are tiny (median 0.0010, max 0.0045) — the two cosine
values are near-indistinguishable on most items — yet G4's spread test passed honestly
(0.138125 over all 120 values): the instrument is deaf to nothing here, the argmax just
carries little stable preference. That is compatible with a true no-signal verdict rather
than a G4 miss.

---

## 6. Honest frame

- A KILL here retires the **generality hypothesis at logit level**, never EXP112's bench-1
  HELD: EXP112 stands per Law #8, reclassified bench-specific (Law #11 two-layer tagging).
  The honesty instrument's label-free readout is now a **one-bench phenomenon** — 41/60 on
  bench 1, 28/60 on bench 4 — not a general instrument property.
- The label-free race remains the actual race, and this result is a real null in it: a
  cleanly licensed, four-guard-passed, hash-pinned negative. It does not move the capability
  scoreboard (still zero positive signals for autonomous steering) — the honest story is that
  the strongest licensed label-free signal the program could produce on $0 CPU did not
  replicate.
- Per §4 of the protocol, a KILL is never followed by a larger-n re-test, a different layer,
  a different carrier, a third bench, or a re-read — each would be an unlicensed gate tweak
  (barred). No cross-bench fidelity comparison is licensed.
- No hypothesis rewording occurred or is licensed (Law #4).
- Novelty remains N1 — Known Combination (§7.1.6).
