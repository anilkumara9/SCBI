# Independent Law #14 Verdict Review — EXP136 (B4/ARI)

**Reviewer:** independent verdict-review lane, LOG-4853 (pre-assigned by the CEO). This lane did not draft, repair, or execute EXP136.
**Pre-registration:** `research/prereg/EXP136_PREREG_ARI_2026-09-30.md` (repaired, fix-verified PASS; EXP136 minted at CEO launch).
**Raw artifacts:** `experiments/runs/EXP136_ari/out/` — `exp136_per_item.csv` (60 rows), `exp136_records.json` (sha256 `3475a4aa63c7b133a0542691542b1152f00e2d4ad9398f8e356170233e5513ae`, independently re-hashed and matched), `exp136_run_log.txt`, `exp136_stdout.log`, `exp136_verdict.json` ("RAW").
**Execution record:** LOG-4852.

## 1. Independent recomputation from raw records

Recomputed from `exp136_per_item.csv` (60 rows; exact binomial McNemar, no library — fractions verified):

| Arm | Registered alternative | flips/60 | ΔM | b | c | p (exact) | acc arm / base |
|---|---|---|---|---|---|---|---|
| T1 (span-boost) | one-sided b>c | 1 | 0.0167 | 0 | 1 | 1.0 (=1) | 35/60 / 36/60 |
| T2 (span-ablate) | one-sided c>b | 7 | 0.1167 | 3 | 4 | 0.5 (=1/2) | 35/60 / 36/60 |
| C (uniform) | two-sided | 5 | 0.0833 | 1 | 4 | 0.375 (=3/8) | 33/60 / 36/60 |

All values match the executor's summary exactly (b, c, p, ΔM, accuracies). Internal consistency holds: b+c ≤ flips on every arm (flips count decision changes; b/c count correctness changes — a flip can move wrong→wrong).

## 2. Guard and (h) verification

- **(a) Δθ=0:** pre/post SHA-256 both `ec276abe…e0ed`, matching the LOG-331 pin. PASS.
- **(b) B-decision agreement:** 60/60 vs archived EXP094 vector (acc 36/60). PASS — the eager backend did not perturb the base.
- **(c) Bench + span pins:** bench SHA-256 `9be81626…47fc` matches; n=60, 0 span exclusions. PASS.
- **(d) (h) hook-delivery, two phases** (§3.4 thresholds checked against the logged probe values):
  - Phase 1 (T2): span mass 0.00e+00 < 1e-6 ✓; renorm 1.19e-07 < 1e-5 ✓; L1 0.2241 > 0.01 ✓; ‖o−o_base‖ = 2.13 > 1e-6 ✓ (A1 — output propagation, detached-copy path closed).
  - Phase 2 (T1): L1 0.1634 > 0.01 ✓; span mass 0.1937 > base 0.1120 (boost, not arbitrary) ✓ and > 1e-3 (non-trivial mass — the ~0-mass no-op case excluded) ✓; renorm 1.19e-07 ✓; ‖o−o_base‖ = 1.78 > 1e-6 ✓.
  - **(h) PASS on both hooks.** Delivery is proven, not inferred.
- **(e) Renormalization/finiteness:** asserted per-forward inside the patch; no violations logged. PASS.
- **(f) Budget:** 242 forwards = 4×60 + 2 probes. PASS.
- No breaking-point trips; exit 0. **No RUN-INVALID.**

## 3. Decision-table application (binding, §4; precedence RUN-INVALID > HELD > KILL > CONTINUE)

- **RUN-INVALID:** no guard tripped. Does not fire.
- **CONTINUE:** requires (T1 one-sided b>c p≤0.05 **or** T2 one-sided c>b p≤0.05) **and** (C two-sided p>0.05). T1 p=1.0, T2 p=0.5 — neither ≤ 0.05. **Does not fire.**
- **KILL:** requires **ΔM_T1 = 0 and ΔM_T2 = 0** vs B, with (h) PASS. Observed ΔM_T1 = 1/60, ΔM_T2 = 7/60. **Does not fire on the pre-reg's exact wording.**
- **HELD:** second disjunct — "(T1/T2 ΔM > 0 but directional p > 0.05) — sub-significant." T1: ΔM=1/60>0, p=1.0>0.05 ✓. T2: ΔM=7/60>0, p=0.5>0.05 ✓. (First disjunct — unattributable — does not fire: T1/T2 not significant, C p=0.375.) **HELD fires.**

## 4. On the KILL bar's strictness (the ΔM=0 question)

The pre-reg writes KILL as a strict equality (ΔM_T1 = 0 **and** ΔM_T2 = 0) and its own §3.3 license calls the bar "stringent, not vacuous" (P ≈ 3.2×10⁻⁶ under a 10% true flip rate). The observed 1 and 7 flips do not satisfy it, and Law #4 forbids re-reading "ΔM=0" as "ΔM≈0" or "no significant flips" after the fact — that would be a new bar. Moreover, the precedence order (HELD > KILL) resolves the overlap independently: HELD's sub-significant branch is literally satisfied, so HELD binds regardless.

**Honest observation (Law #11):** the flip pattern is symmetric noise, not a lurking signal — T2's 7 flips split b=3/c=4 (net movement ≈ 0), and T1's single flip is a *worsening* (c=1, b=0), opposite to its predicted direction. The HELD verdict reflects the registered bars' literal application: the experiment is **inconclusive**, not a near-miss. It licenses nothing and kills nothing. The routing-around hypothesis is neither confirmed nor dead — this test of its constructive half returned no directional signal in either arm.

## 5. Binding verdict

**HELD** — sub-significant per §4. Neither routing arm moved decisions in its registered direction (T1 p=1.0, T2 p=0.5); ΔM>0 on both arms (1/60, 7/60) trips the pre-registered sub-significant HELD branch; KILL's strict ΔM=0 bar is unmet; CONTINUE's bars are unmet; no apparatus failure. Precedence HELD > KILL > CONTINUE confirms the verdict.

**Scope:** this HELD fences nothing and licenses nothing. It does not retire the attention-routing axis, and it does not motivate a dose study (no directional signal to follow up).

---
*Verdict review: independent lane, LOG-4853. $0 CPU, paper only. Verdict only — no re-execution, no protocol changes.*
