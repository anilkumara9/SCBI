# Independent Verdict Review: EXP135 (B2/EVAL) — Label-free E-step Validity

**Review lane:** LOG-4846 (pre-assigned by the CEO). **Status:** INDEPENDENT — this lane did not draft, repair, or execute this experiment.
**Pre-reg:** `research/prereg/EXP135_PREREG_EVAL_2026-09-30.md` (as amended LOG-4842). **Execution record:** LOG-4843.
**Artifacts reviewed:** `experiments/runs/EXP135_eval/out/exp135_report.json`, `exp135_per_item.csv`, `exp135_records.json`, `exp135_run_log.txt`, `exp135_checkpoint.json`, `run_exp135.py`.

---

## 1. Independent recomputation of the primary endpoint

Recomputed from `exp135_per_item.csv` (60 rows), not from the report JSON's summary:

- ρ\*_i = (5 − k_i)/4 mapping verified exact on all 60 rows.
- **ρ̄\* = −0.0041667** (report: −0.0042 ✓)
- **Mean bridge score-rank k̄ = 5.0167** (report: 5.02 ✓)
- Bridge-rank distribution: k=1:3, 2:8, 3:11, 4:6, 5:8, 6:7, 7:3, 8:4, 9:10 (report matches ✓)

**KILL bar check:** ρ̄\* = −0.0042 ≤ 0.3 → **the KILL condition is met.** (The p-value is not a conjunct on the KILL branch.)

**p-value sanity check:** independent Monte Carlo (B=50,000, seed 999, n=60 uniforms) gives p ≈ 0.529 vs reported 0.530275 (B=200,000, MCSE ≤ 0.0011). Consistent. The p-value carries no verdict weight here but the computation is sound.

---

## 2. Guard verification (all 8, from raw artifacts)

| Guard | Pre-reg trip | Observed | Verdict |
|---|---|---|---|
| (a) Δθ=0 | pre/post hash mismatch | pre = post = `ec276abe…e0ed` (LOG-331 pin) | PASS |
| (b) Bridge pin | artifact mismatch / α ≠ 0.5 | bridge re-derived deterministically from licensed recipe (`normalize(E[t]−E[f])`, `' '+entity`, `[0]`); α asserted = 0.5 | PASS |
| (c) Bench pin | sha mismatch / len ≠ 60 | 60/60, sha256 `eb304fa6…` | PASS |
| (d) Exclusions | >6 excluded | 0 excluded, n = 60 | PASS |
| (e) Degeneracy | ≥n/2 = 30 items zero-variance | **29/60** for S_E at λ ∈ {0.7, 0.5, 0.9} — independently recomputed from `exp135_records.json` per §3.3 formulas | PASS |
| (f) Budget | forwards ≠ 50n+750+N_g | 3,751 = 3,751 (2,700 + 300 + 750 + 1) | PASS |
| (g) Readout-sensitivity | r ∉ [0.99, 1.01] | r = 1.0000000 | PASS |
| (h) Inertness | any random > ⌈0.01·5n⌉ = 3 flips | C2–C9: 2,1,1,2,0,1,1,1 — independently recomputed vs `cache_unintervened` | PASS |

**No guard fires. Not RUN-INVALID.**

### 2.1 The (e) proximity (as tasked)

29 degenerate items vs the ≥30 trip — **one item short of the apparatus-void threshold.** The reading is mechanical: 29 < 30 → PASS. This lane does not move the bar. But the proximity is recorded honestly: 48.3% of items have zero score variance across all 9 candidates. The evaluator is nearly blind on this bench — which is itself consistent with the KILL reading (the scores carry almost no discriminative signal), but it is not a guard trip and does not alter the verdict.

### 2.2 (b) implementation note (non-blocking)

The executor re-derived the bridge deterministically from the licensed construction recipe rather than hashing a pre-built artifact against the LOG-128 record. The pre-reg's intent — the anchor must be the licensed bridge, not a lookalike — is satisfied (the construction is the licensed recipe, α = 0.5 asserted, reconstruction hash recorded). This is a faithful implementation, not a deviation.

---

## 3. The defect-and-rerun (as tasked)

LOG-4843 records: the first run crashed in post-processing (exit 1) after all 3,751 forwards due to a missing `H_ALLOW_FRAC` constant; the constant (0.01) was added, checkpointing added, and a **full deterministic re-run** was executed. Assessment:

- The runner script (`run_exp135.py`, 08:08) contains `H_ALLOW_FRAC = 0.01` at line 36 — the fix is present.
- The run log (08:08–08:52) and all artifacts are timestamp-consistent with the clean re-run.
- All protocol randomness is seed-pinned (§3.1), so the re-run's forwards are bit-identical to the first run's; only the post-processing differs. The defect cannot have altered the results.
- **Honestly recorded, no compromise.** The checkpoint file exists as evidence of the re-run's provenance.

---

## 4. Secondary scores (Law #4 decomposition check)

Per §4: a secondary clearing the CONTINUE bars while the primary does not → HELD with a noted anomaly, never promotion.

- S_E(0.5): ρ̄\* = 0.1083, p = 0.101615 → does not clear CONTINUE.
- S_E(0.9): ρ̄\* = 0.1542, p = 0.034135 → p < 0.05 but ρ̄\* = 0.1542 ≪ 0.7 → does not clear CONTINUE.

**No decomposition anomaly.** Both secondaries also sit at or below the KILL magnitude (≤0.3), consistent with the primary reading. They carry no verdict weight per Law #9.

---

## 5. Decision-table application

Precedence: RUN-INVALID > KILL > CONTINUE > HELD.

1. No §3.7 guard fires → not RUN-INVALID.
2. ρ̄\* = −0.0042 ≤ 0.3 (primary) → **KILL** fires. Precedence over CONTINUE/HELD is moot (neither is reachable: ρ̄\* < 0.7).

---

## 6. Binding verdict

# **KILL** — "the E-step ranks candidates" is dead.

**Pre-registered justification (§4.2):** the primary endpoint ρ̄\* = −0.0042 ≤ 0.3 on the signed S_E (λ_c = 0.7) score. The bridge's mean score-rank (5.02 of 9) is indistinguishable from uniform random ranking. **Licensed reading:** the signed evaluator cannot distinguish the known-causal direction from randoms by label-free scores; the G/E/S loop as designed has no working selection step.

**Does NOT license:** any claim about non-spec scores, other benches/backbones, or resurrection of killed causal families (§4.2).

**What this kills:** the G/E/S loop as designed. E-validity — [CONJECTURE] since LOG-3842 — is now refuted at the registered bars. The program's only path to autonomous basis invention needs an architecture rethink, not a better candidate generator. Per §5.6, no candidate claims beyond this bench.

---

## 7. Review-lane notes for the record

- The (e) guard's 29/60 proximity is the narrowest apparatus margin in this program's recent history. The bar held as written. Future E-class designs should expect heavy score degeneracy on this bench.
- The executor's mid-run defect was handled exactly per the program's norms: stop, record, fix, deterministic re-run, disclose. No verdict weight is affected.
- This is the program's **eighth binding KILL** and its most architecturally consequential: it retires not a mechanism but the selection architecture itself.
