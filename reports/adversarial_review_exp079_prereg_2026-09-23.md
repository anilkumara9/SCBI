# Law #14 Adversarial Review: EXP079 Pre-registration Draft — SIGN (minor findings only)

**Date:** 2026-09-23
**Reviewer role:** Adversarial Reviewer (Law #14)
**Artifact reviewed:** `experiments/protocols/EXP079_BETTER_PROBE_PREREG_SPEC.md` (DRAFT, LOG-119)
**Reviewed against:** SIGNED EXP070 spec (`experiments/protocols/EXP070_ORACLE_CEILING_PREREG_SPEC.md`),
LOG-110 (EXP070 (c2) ruling), LOG-119 (draft entry), `AGENTS.md` 14 Laws,
`research/MATH_STANDARDS_CHARTER.md` (M1–M8), `STATISTICAL_PROTOCOL_V02.md`
**Method:** full read of the draft (not on trust) + independent recomputation of every
[FACT — computed] the gate rests on + diff-classification of EXP070→EXP079 deltas.

**Verdict: SIGN — 0 MAJOR, 0 MODERATE, 5 MINOR (all non-blocking).**
The banner may advance to PRE-REGISTERED once the minors are addressed (or explicitly deferred
with justification); none blocks signing.

---

## 1. Load-bearing verification: the calibrated gate's arithmetic (independent recomputation)

The entire probe-signal gate rests on the Multinomial(N, 1/17) max-fraction null. I recomputed
it independently (numpy 1.26.4, 100k draws, seed 7979 — the spec's pre-registered seed):

| Quantity | Spec claim | Independent recomputation | Match |
|---|---|---|---|
| H_sel null mean, N=60 | 0.121 | 0.1210 | ✓ |
| H_sel null sd, N=60 | 0.020 | 0.0195 | ✓ |
| 95th percentile bar, N=60 | 0.150 | 0.1500 | ✓ exact |
| 95th percentile bar, N=50 | 0.160 | 0.1600 | ✓ exact |
| P(null H_sel ≥ 0.100), N=60 | 0.976 | 0.9755 | ✓ |
| Old 0.25 floor in sd units | ≈6.5 | 6.60 | ✓ |

**[FACT — verified]:** the [FACT — computed] labels on the gate bar are correct to the quoted
precision. The 0.25→calibrated replacement is the single most important improvement in this
re-registration, and its numbers are right.

**Diagnosis grounding check:** EXP070 §6's "≈86%" figure for diagnostic (i) under selection
noise — I initially recomputed ≈82.4% under a uniform-score model, which would have been a
discrepancy. Recomputing under the correct Binomial(5, 0.5) score model (probe scores are sums
of Bernoulli items, not uniform) gives **≈86.4%** — the cited figure is correct under its
model. The degeneracy diagnosis (observed 6.7% vs ≈86% noise expectation; H_sel=0.100 below the
null mean 0.121) is correctly grounded. No finding.

**Budget arithmetic:** 17 × 15 × 60 = 15,300 probe forwards; + 7 × 60 = 420 test forwards;
total ≤ 15,720. ✓. Wall-clock ≈2h at the program's 0.49 s/pass basis (15,720 × 0.49 ≈ 7,700 s). ✓.

---

## 2. EXP070 → EXP079 delta classification (complete)

Every difference from the signed EXP070 spec, classified:

| # | Delta | Classification |
|---|---|---|
| 1 | §0 re-registration note + degeneracy diagnosis ([OBSERVATION]/[INTERPRETATION] labeled) | Legitimate — mandated by (c2); labels correct per AGENTS.md §5 |
| 2 | Split-half: BUILD (even indices, 75 pairs) for all candidate construction; HELDOUT (odd, 75) for probing only | Legitimate — the mechanism of the probe fix; deterministic, no seed |
| 3 | Third disjointness assertion: probe∩BUILD=∅ (+ post-run audit) | Legitimate — closes the exact in-sample path |
| 4 | Probe size: up to 15 items/instance, min 8 (was 5/min 3) | Legitimate — granularity fix |
| 5 | H_sel bar: 0.25 [ARBITRARY] → 95th-pct null bar (seed 7979, adapts to N_final) | Legitimate — verified §1 above |
| 6 | B_agg built from BUILD-half (C2 apples-to-apples); branch (g) interprets deviation as drift diagnostic | Legitimate — documented in §3.1, §3.4, §7 |
| 7 | Branches (c1)/(c2)/(c3) → (c1*)/(c2*)/(c3*) with upgraded licenses | Legitimate — (c2*) now reads pool-homogeneity + mandates pool-diversity diagnostic, forbids third probe iteration |
| 8 | New assumptions: A-probe-v2, A-selection-noise (attenuated), A-split-representativeness (stated debt) | Legitimate — named, not smuggled |
| 9 | Pilot probe-yield smoke check (degeneracy → HALT before full spend) | Legitimate — cheap insurance, explicitly non-ruling |
| 10 | §11/§12 non-goals: no re-litigation of EXP070 (c2); 410m replication takes next free number | Legitimate — Law #4 hygiene |

**No mechanism, threshold (other than the disclosed gate replacement), seed, condition,
endpoint, or tree-logic drift beyond the licensed probe redesign.** Hypotheses H_ceiling/H_0
are verbatim from EXP070; the research question's "on out-of-sample probes" addition is the
disclosed design change. New number EXP079 verified free (no collision in protocols/ or
runs/). The drafter modified no files outside the spec + LOG-119. **No hypothesis-shifting
(Law #4). No silent re-run of EXP070 — this is its mandated successor.**

---

## 3. Criterion-by-criterion findings

### (1) Decision-tree uniqueness/exhaustiveness — MINOR-2 only
The partition over (C3-vs-C2 McNemar p, ΔM sign, margin vs +12pp, gate pass/fail) is exhaustive:
{p≥0.05}→{(c1*) gate pass, (c2*) gate fail}; {p<0.05, ΔM>0, margin≥12pp}→(e);
{p<0.05, ΔM>0, margin<12pp}→(d) (exact 12.00pp → (e), covered); {p<0.05, ΔM<0}→(c3*).
(a) halts on gate failure; (b) invalidates on C7 failure; (f) has explicit precedence over
(c1*)/(c3*)/(d)/(e). **MINOR-2:** (f) and (c2*) can co-fire (precedence note explicitly does
not suspend (c2*)'s probe logic), and their licenses are mutually compatible (both: no kill,
no justification, diagnose further) — but the co-firing resolution is implicit. Add one
sentence: "If (f) and (c2*) co-fire, the ruling reports both; the operative license is
(c2*)'s (ceiling unmeasured, NOT cancelled, pool-diversity diagnostic next) together with
(f)'s diagnostic mandate." Non-blocking; the ruling stays coherent either way.

### (2) License tightness, esp. EXP068 — MINOR-4 (suggestion)
- (c1*): gated kill → "EXP068 cancelled in its current form", with the full does-not-license
  column (no H_loop falsification, family/model/benchmark restriction, re-motivation as new
  pre-registration). Tight. **MINOR-4 (suggestion):** name "the BUILD-half pool" explicitly in
  the license text (currently "over this pool" — defined in §3.1, so acceptable as-is).
- (c2*): ceiling unmeasured, EXP068 NOT cancelled, pool-homogeneity reading, **required next
  step is a pool-diversity diagnostic — not a third probe iteration**. This is the correct
  anti-degeneracy constraint on the program's iteration loop. Tight.
- (c3*): ungated kill on significant negative — valid given the direction-neutral tie-break
  (seed 7005) is retained. Tight.
- (d)/(e): inherited, tight; the asymmetry note (kill withdraws justification / win merely
  justifies building) preserved verbatim in spirit.
- A-pool amendment honestly discloses the kill-easier bias of the BUILD-half pool and names
  the calibrated gate as the protection. The license is family-restricted, matching what was
  measured. No overclaim.

### (3) Split-half disjointness — airtight at the id level
probe∩test=∅, support∩test=∅, **probe∩BUILD=∅** — all runtime-asserted, violation = protocol
violation (abort, never silent correction), all id lists archived (§10). BUILD∩HELDOUT=∅ by
deterministic even/odd construction. The in-sample path (exact-pair reuse) is closed.
*Observation (not a finding):* entity-level overlap between BUILD and HELDOUT pairs is not
asserted — correctly scoped, since the degeneracy mechanism was exact-pair memorization, and
G1 candidates are pair-aggregates that never see a HELDOUT pair's hidden states.

### (4) Monte Carlo null-gate — sound; MINOR-5 (limitation note)
Verified exact (§1). The procedure (100k draws, seed 7979, K=17, realized N_final, 95th
percentile) is pre-registered and adapts correctly. **MINOR-5:** add one [LIMITATION]
sentence noting the candidate-exchangeability idealization — the 8 G1 candidates share B_agg's
span, so under pure noise the effective candidate count is < 17 and the true false-pass rate
of the (iii) bar may sit slightly above the nominal 5%. The (ii) transfer test remains the
primary gate and is unaffected. Non-blocking.

### (5) Diagnosis vs fix — grounded
6.7% vs ≈86% (verified under the binomial score model), H_sel=0.100 < null mean 0.121
(verified), P(null ≥ 0.100)=0.976 (verified) → degeneracy, not noise. Root cause (in-sample
probing: all 17 candidates built from the same 150 pairs they were probed on) matches EXP070
§3.1/§3.2/§3.5(3). The fix breaks the exact mechanism: probe items are pair-id-disjoint from
all construction data; 16 score levels replace 6, making top-ties the exception. The pilot
expectation ((i) materially above 6.7%, ties rare) is a falsifiable smoke signal, explicitly
not a ruling. ✓.

### (6) No hypothesis-shifting — clean
H_ceiling/H_0 verbatim; new experiment number; §11 forbids re-litigating EXP070 (c2);
§0 documents the delta as the only licensed changes. Law #4 satisfied.

### (7) Bar labeling — MINOR-1
The H_sel bar is null-calibrated (non-arbitrary). Diagnostic (ii) uses conventional α.
**MINOR-1:** the +12pp worth-chasing bar lost the `[ARBITRARY — sensitivity analysis
required]` tag it carried in EXP070 (§1.2 (d)/(e) rows and §8). The justification and the
+16/+20pp sensitivity bands are present; restore the tag in both tables to keep the labeling
discipline continuous. (The bar is still a judgment call — the tag is the honest label.)

### (8) Budget / determinism / anti-cheat / Δθ=0 — clean
Budget ≤15,720 verified; single Kaggle session feasible. Seeds complete (master 20260923,
7001–7005, 9876, **7979** new; even/odd split deterministic, needs none).
`torch.use_deterministic_algorithms(True)` stated. Anti-cheat §3.5 strengthened (three
disjointness assertions + post-run audit). SHA-256 pre/post binding guard, Δθ=0, no backward
pass. Law #13 archive list complete (adds split indices, Monte Carlo summary).

---

## 4. Minor findings (non-blocking)

- **MINOR-1:** Restore `[ARBITRARY — sensitivity analysis required]` on the +12pp bar in the
  §1.2 table (d)/(e) rows and the §8 (d)/(e) rows, matching EXP070's labeling.
- **MINOR-2:** Add one explicit sentence resolving (f)+(c2*) co-firing (both licenses stand;
  operative license = (c2*)'s + (f)'s diagnostic mandate) for M5.2 uniqueness.
- **MINOR-3:** §0 "only one thing changes" slightly overstates — the pool construction inputs
  change (BUILD-half) alongside the probe. Qualify: "the 17-family pool construction (family
  unchanged; inputs BUILD-half per design delta 1)". The transparency is already in §0/§7;
  this is wording precision.
- **MINOR-4 (suggestion):** name "the BUILD-half pool" explicitly in the (c1*) license text.
- **MINOR-5:** add a one-sentence [LIMITATION] on the H_sel null's candidate-exchangeability
  idealization (G1 span-sharing; (iii)-path false-pass rate may sit slightly above nominal 5%).

## 5. What was NOT in scope / explicitly deferred
- Bundle implementation review (comes after the bundle is built — the Law #14 bundle review
  must verify the even/odd split, the three disjointness assertions, and the analysis-time
  Monte Carlo against this spec).
- Whether the A-split-representativeness debt bites in practice (pilot will reveal; HALT
  provisions cover it).

---

**Banner may advance to PRE-REGISTERED.** No primary artifacts modified; no results invented;
no results exist under this protocol.
