# Independent Verdict Review — EXP137 (B3/TGA-DECODE)

**Lane:** LOG-4858 (pre-assigned by the CEO). **Status:** independent — this lane did not draft, review, or execute EXP137.
**Sources read in full:** `research/prereg/EXP137_PREREG_TGADECODE_2026-09-30.md` (signed, Law #14 SIGN LOG-4856, no fixes required), `experiments/runs/EXP137_tgadecode/out/exp137_report.json` (raw results), LOG-4857 (execution record), `AGENTS.md` laws #2, #7, #11, #14.

---

## 1. Independent recomputation (Law #2 — no invented numbers)

**Primary statistic — derived from raw per-item records, not the summary:**
- `per_item.correct`: 60 entries; exactly 2 `true` (indices 14, 24).
- Consistency check: at both flagged indices `predicted_label == true_label`; zero unflagged indices match (no undercount).
- **a = 2/60 = 0.0333** — matches the report's `primary.accuracy` exactly. [OBSERVATION]

**Permutation p-value — sanity-checked from the registered formula:**
- p = (1 + n_ge) / (1 + B) = (1 + 5901) / (1 + 10000) = 5902/10001 = **0.5901409859** — matches the report to 10 decimal places. [OBSERVATION]
- Internal coherence: null mean 0.0355 ≈ observed 0.0333; p ≈ 0.59 is exactly the expected reading for an observation at the null center. The 2/60 observation is *below* the 5% chance rate (3/60 expected under K=20). No anomaly.

**Breaking points (§3.5, all → RUN-INVALID):**
- Report records all 7 untripped (`tripped: false` for (a)–(g)).
- LOG-4857 independently confirms each apparatus check: A1 SHA-256 `9b527c…13dc` exact with 10 `v1__` keys; v̂₁ coherence mean |cosine| = 0.9973 ≥ 0.99 (canonical-direction premise holds); A2 SHA-256 `9219bd…95fae` exact, layers (24, 60, 1024); strata (16/14/14/16) exact; 60 ids match the EXP092-B bench pin; 20 unique labels; scalar variance > 0; zero exact 1-NN distance ties.
- **No breaking point tripped → no RUN-INVALID.** The apparatus is sound; the verdict is on the hypothesis.

---

## 2. Decision-table application (binding, §4)

| Branch | Registered bar | Observed | Fires |
|---|---|---|---|
| CONTINUE | a ≥ 0.15 (≥9/60) AND p < 0.00208 | a = 0.0333, p = 0.5901 | No |
| **KILL** | **a ≤ 0.08 (≤4/60)** | **a = 0.0333** | **Yes** |
| HELD | 0.08 < a < 0.15, or a ≥ 0.15 with p ≥ 0.00208 | — | No |
| RUN-INVALID | any §3.5 trip | none | No |

The three bars are disjoint and exhaustive over (a, p) space. No post-hoc re-binning (Law #4).

---

## 3. Secondary statistics (pre-registered, non-binding)

- **S2 random-direction controls** [OBSERVATION]: v̂₁'s 0.0333 sits inside the random 1-D projection spread [0.0, 0.0167, 0.0167, 0.0333, 0.0333, 0.0667, 0.0667] — tied at the mode with two randoms (rank 3/9 among v̂₁ + 8 controls). The distinguished direction decodes no better than random 1-D projections. Corroborates the null reading; cannot override the primary verdict.
- **S1 full-vector 1-NN at layers[19] = 0.1667** [OBSERVATION]: speaks to the *space*, not the v̂₁ *channel*. Per the pre-reg it cannot override the primary verdict (Law #9, Law #11 — observation separated from interpretation; no post-hoc metric substitution).

---

## 4. Binding verdict

**VERDICT: KILL**

**Pre-registered justification:** 1-NN LOO accuracy on the v̂₁-projected `layers[19]` scalars is 2/60 = 0.0333 ≤ 0.08 (≤4/60), the registered KILL bar, with a sound apparatus (all breaking points untripped) and a coherent null (p = 0.5901, observation at the null center). Per §4: **"the TGA channel carries no task information above the null ceiling."**

**Scope (per the pre-reg's fence):** the TGA story closes completely — the direction *exists* (EXP127, amplification 8.24×), *carries nothing* (this verdict), *moves nothing* (EXP131/133 binding KILLs). This verdict does not touch EXP127's dynamics measurement, the S1 full-vector observation, or any steering claim beyond the registered hypothesis. A CONTINUE interpretation of S1 or S2 would be a post-hoc bar change and is refused under Law #4.

**Single-lane fence held:** verdict only. No re-execution, no protocol changes.

---

*End of LOG-4858 verdict review.*
