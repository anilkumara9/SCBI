# Independent Law #14 Review — EXP127 v₁ Injection-Test Pre-registration (GPU-bound)

**Lane:** LOG-4725 (pre-assigned). **$0 CPU.** Read-only review; no protocol
edit made by this lane. **Verdict: SIGN-WITH-FIXES.**

**Protocol under review:**
`research/prereg/EXP_PREREG_TGA_V1_INJECTION_2026-09-29.md` —
sha256 `a93612e28064d4b6f37481c52a4424068177c6f4ee7693450306e7cb3f83c3e5`
(confirmed before any reading; matches the drafted value).

**Cross-reference checked:** EXP127 execution report
(`research/experiments/EXP127_TGA_TRANSIENTGROWTH_REPORT_2026-09-29.md`);
paradigm-break dossier `research/strategy/PARADIGM_BREAK_SPRINT_2026-09-29.md`
(Family A); EXP128 RUN-INVALID records; EXP129 KILL records; EXP077
`run_exp077.py` (B_agg reconstruction recipe); EXP127 run directory
`experiments/runs/EXP127_tga/out/`.

**Review posture:** binding Mentor adjudication. This protocol is GPU-bound
for the founder's hardware, so the review is held to the stricter standard:
no unpinned degree of freedom may survive in any verdict-reading quantity,
because a GPU run spends the founder's time and attention.

---

## 1. The four gate/control specs — protocol-level, verified

1. **Matched random controls (§3.3, §3.5):** K = 8 seeded isotropic unit
   vectors per prompt (`torch.Generator`, seeds `20260929_4724 +
   prompt_idx*100 + j`), every arm norm-matched to budget B with a
   float32-tolerance component audit (breaking point (d)). The dose-fence
   is mechanical. ✓
2. **Dead B_agg control (§3.3, breaking point (e)):** re-derived
   deterministically from the archived support set per EXP077's
   `build_candidate_directions` (§"Reconstruct v_hat_k, v_hat (=B_agg),
   mu, v_hat^c", verified present in `run_exp077.py` line 252; the
   construction `v_hat = normalize(sum_k v_hat_k)` is deterministic
   given the archived support presentations). No B_agg artifact hash
   exists in program records, and the protocol invents none (Law #2) —
   the worksheet records the reconstruction hash at execution. Law-#2
   honest. ✓
3. **Decision-orthogonality gate ĉ (§0 [DEFINITION], §3.7, §4 tree):**
   ĉ_i = |⟨v̂₁,i, ĝ_i⟩| with g_i the exact-autograd VJP of the
   registered cosine margin w.r.t. x_{20,last} on the base
   (no-injection) forward; mean over ≤ 10 prompts; ĉ < 0.1 → KILL;
   ‖g_i‖ < 1e-12 exclusions recorded, ≥ 3 exclusions → apparatus-void.
   Protocol-level. ✓
4. **Singular-rank trend gate (§3.7, §4 tree):** margin displacement
   must rank-order disp(v̂₁) > disp(v̂₂) > median disp(random) on
   ≥ 8/10 prompts; flat → KILL. Protocol-level. ✓

**Artifact re-pins verified against the run directory (this lane):**
`exp127_vectors.npz` sha256 recomputed as
`9b527c026d0ee307192725429f655e628f403505343dc018de3cfe15db6113dc`
(exact match to the protocol's pinned value); 20 keys = 10
`v1__<prompt_id>` + 10 `urand__<prompt_id>` (no `v2__` keys — consistent
with the LOG-4714 erratum's finding); the 10 `v1__` ids are exactly the
protocol's 10 prompt ids (flip {0,2,4,6,9}, ctrl {1,3,5,7,8}).
The re-pin spec is executable as written. ✓

## 2. B_agg apparatus-drift rule — correct severity

"Any B_agg flip → RUN-INVALID (apparatus drift)" (§0(e), §2, §4 tree).
The routing is correct: a flip on the dead control means the bench or
backbone is not what EXP077 measured — the safe outcome is UNTESTED, not
a verdict. The draft's justification ("the bench or backbone is not what
EXP077 measured") correctly covers bench mismatch as well as drift, since
the injection prompts are EXP107-first-10, not EXP077's construction set.
No fix. ✓

## 3. ĉ gate construction — no circularity

The ĉ gate is computed from the base (no-injection) forward's VJP,
*before* any injection forward (§5 ordering: artifact re-pins → budget
→ ĉ gate → forward batches). It reuses no injection output. The §0
ordering string places the ĉ gate before forward batches, consistent
with §5 modulo FIX-3. ✓

## 4. Non-resurrection audit — clean

§7 names every constraining kill (EXP077/093/094, S5-2, S5-3, G1,
EXP115/116/123, EXP125, EXP126, LOG-4693 paradigm death, EXP128,
EXP129). The Law #4 direction-class argument holds: no killed lane ever
injected along v₁ (the dynamics' own leading singular vector); the
semantic-direction kills do not fence a dynamics-matched direction.
One-shot injection only (no loop — EXP129's KILL does not transfer);
exact artifact re-pinning (no finite-difference term anywhere —
EXP128's death does not transfer). The EXP126 domain-set-detector
caveat is inherited, not re-litigated. ✓

## 5. Law #9 ordering — executable, no LOG-4704-class circularity

§5: `guards → backbone pin → artifact re-pins → budget computation
and record → ĉ gate → forward batches → validity-check evaluation
(norm audit + B_agg null-control + re-pin) → raw-record hash-pin →
metric → decision`. The validity checks (including the B_agg
null-control) sit before the hash-pin; the verdict metrics (median r,
ΔM, McNemar, rank trend) are read only after the pin, and the pin
covers exactly their inputs (§3.8). No check reuses a later stage's
output. Executable. ✓ (One cosmetic gap: §0's ordering string omits
the budget step — FIX-3.)

## 6. Honest frame — verified

CONTINUE is conjunctive and complete: ĉ ≥ 0.1 AND median r ≥ 2 AND
ΔM_v1 > 0 with one-sided McNemar p ≤ 0.05 AND rank-trend holds AND
ΔM_Bagg = 0 (§2, §3.7, §4). "A margin gain without flips is HELD,
never CONTINUE." The scoreboard stays at zero until a bound positive
lands; no generality beyond Pythia-410m L20→L24 and the 10 pinned
prompts; §8 disclaims reasoning, cognition, mechanism, and
resurrection explicitly. ✓

---

## Fixes

### Launch-gating (verdict-material — the protocol may not launch until fixed)

1. **Pin the McNemar "best-random" comparator.** §2 and §3.7 read
   "McNemar(v₁, random) one-sided p ≤ 0.05" / "v₁ vs best-random arm"
   without defining whether "best-random" is the single random arm
   j* with the most flips across all 10 items (global best) or the
   per-item best random arm. This is a Law #4 degree of freedom inside
   the CONTINUE bar. Fix: pin one definition in §3.7 and carry it to
   §2/§4 verbatim.
2. **Pin the zero-denominator branch of the margin-displacement ratio.**
   r_i = |margin_{v1,i} − margin_{base,i}| / max_j |margin_{rand_j,i}
   − margin_{base,i}| is undefined when all 8 random arms move the
   margin by exactly 0 on item i — a live possibility given the
   program's zero floors (EXP094). Fix: pin the branch in §3.7, e.g.
   0/0 → r_i = 1 and x/0 → r_i = +∞ for x > 0, with denominator-zero
   items disclosed as a diagnostic in the report.

### Verdict-immaterial

3. **Align the §0 Law #9 ordering string with §5.** §0 omits the
   "budget computation and record" step that §5 (correctly) places
   between artifact re-pins and the ĉ gate. One-line fix.
4. **State the v̂₂ derivation iteration count explicitly.** §3.3 pins
   v̂₂ "per the LOG-4714 erratum" (seed `20260929_4714`, exact
   JVP/VJP); the erratum's K=40 fixed iteration count should appear
   in this protocol's own text rather than by reference alone.
5. **Cost the v̂₂ derivation in §6.** The "~120 forwards + ~10 VJPs"
   budget omits the deflated power iteration (~800 autograd products
   through the 4-block span at K=40 × 2 × 10 prompts). Minutes on a
   T4 either way, but the honest number belongs in the protocol.
6. **Add the a priori McNemar one-sided exact critical table** for
   n=10 (program standard — cf. the EXP130 draft). Transparency fix;
   the test is already well-defined.

---

**Deliverable note:** no protocol edit was made by this lane; the six
fixes are for the fix-verification lane. Nothing pushed, spent, or
credential-touched. House rules (`~/workspace/SCBI/AGENTS.md`) read
before reviewing.
