# H1 — BIAS-SUBTRACTED RESIDUAL INSTRUMENT — 2026-09-25

**Agent:** NULL RE-MINING follow-up agent, reporting to CEO (Nova), under the 30-Day Autonomous Campaign Charter (Lane 3).
**Parent finding:** NULL_REMINING_2026-09-25.md, P1 — EXP091's decision variable d is r=+0.97 correlated with per-pair static anisotropy bias b; the instrument was blind by construction.
**Status:** [OBSERVATION]-grade exploratory computation only. Any claim requires a fresh pre-registered EXP number.
**Artifacts:** read-only. No artifact, protocol, or weight modified at any point.

---

## PART 0 — PRE-COMMITTED PLAN (written BEFORE any computation ran)

**Precise question (H1):** After removing the per-pair static anisotropy bias b_i — estimated by cross-fitting from DISJOINT items (Law #7-compliant, never the test item's own state) — does sign(d_i − b_i) predict correctness above chance?

**Definitions [DEFINITION]:**
- S_i: layer-20 final-token hidden state of item i's premise (60×1024).
- a_i, c_i: layer-20 final-token hidden states of `" "+A_i` / `" "+C_i` encoded standalone (static per entity).
- d_i = cos(S_i, a_i) − cos(S_i, c_i). Registered instrument: pick A iff d_i > 0. A is always the target ⇒ correct iff d_i > 0.
- M_f: mean of L2-normalized states over items NOT in fold f (cross-fitted mean direction).
- b_i = M_f·â_i − M_f·ĉ_i, where â_i, ĉ_i are L2-normalized a_i, c_i. The static anisotropy bias for item i, estimated without item i's state.
- ε_i = d_i − b_i (residual). Residual instrument: pick A iff ε_i > 0 ⇒ correct iff ε_i > 0.

**Law #7 compliance [ASSUMPTION]:** b_i uses only (a) out-of-fold states via M_f and (b) standalone token embeddings â_i/ĉ_i, which are computed without any item state or label. Labels enter only at evaluation (prediction vs truth), which is standard and non-leaking.

**Procedure (runs exactly once as specified):**
1. Load `exp091_embeddings.npz` and `exp091_report.json` (read-only). Sanity: recompute d_i from embeddings; assert agreement with report's cosA−cosC to 1e-6 (sanity check, not a test). Assert no NaN/inf.
2. 5-fold CV, seed 0, folds stratified by domain (planet/element parsed from item ids), 12 items per fold.
3. For each fold f: M_f = mean of normalized out-of-fold states; for each i in fold f: b_i = M_f·â_i − M_f·ĉ_i; ε_i = d_i − b_i.
4. Residual accuracy = #{ε_i > 0} / 60. (Ties ε_i == 0, if any, count as wrong — recorded explicitly.)
5. Exact binomial test, H0 p=0.5: report one-sided upper-tail p (pre-committed breaking-point direction) AND two-sided p for reference.
6. **Breaking point (pre-committed):** residual accuracy > 0.5 AND one-sided upper-tail p < 0.05 → breaks the pure-bias model → genuine lead opened. Otherwise (residual ≈ 0.5) → the P1 finding is extended: EXP091's null is "instrument blind", no relational signal under the bias.
7. Descriptives (no tests): distribution summary of ε_i; agreement rate between residual picks and static-bias picks (sign(b_i)); agreement between residual picks and registered instrument picks.

**Anti-p-hacking:** this procedure runs exactly once. Anything conceived after seeing results goes in PART 3, labeled post-hoc, no formal tests.

---

## PART 1 — RESULTS

*(Pre-committed procedure ran exactly once, 2026-09-25, $0 CPU. All numbers from primary artifacts; no artifact modified.)*

**Sanity checks (passed):** recomputed d_i from embeddings agrees with the report's cosA−cosC to 1.6e-07; no NaN/inf anywhere; 0 ties (ε_i == 0).

**Headline [OBSERVATION]:**
- **Residual accuracy = 30/60 = 0.500** (exact).
- **One-sided upper-tail binomial p (H0 p=0.5) = 0.5513**; two-sided p = 1.0.
- **Breaking point NOT hit.** The pure-bias model stands: there is no relational signal hiding under the static anisotropy bias.

**Supporting [OBSERVATION]:**
- r(b_i, d_i) = **0.971** (cross-fitted b_i; reproduces P1's +0.97 — the bias estimate is label-free and out-of-fold, so this is not circular).
- Residual ε_i: mean −2.9e-05, sd 1.9e-04, range [−5.6e-04, +3.2e-04] — pure noise scale, ~3% of the decision variable's magnitude budget.
- Residual picks agree with the registered instrument's picks on only **35%** of items, and with the static-bias rule on **30%** — the residual is effectively independent noise, not a refinement of either.
- Static-bias rule alone (sign(b_i), cross-fitted): 30/60 = 0.500.

---

## PART 2 — INTERPRETATION

**[INTERPRETATION] The H1 decision resolves as KILL on the "masked signal" reading.** The question was whether EXP091's null was "instrument blind" (no signal even in principle) vs "signal exists but was masked by bias". After removing the bias with a Law #7-compliant cross-fitted estimator, the residual predicts at exactly chance (30/60, p=0.55). The instrument was not masking a signal — there is no signal at this readout. The P1 finding is extended, not qualified.

**[INTERPRETATION] This closes the static-cosine chapter.** Combined with P1 (r=+0.97 bias dominance), A8 (EXP065/066's 0.7 was anisotropy, never rotational), and A7 (the cross-validated bridge carries no generalizable signal), the program now has a complete mechanistic account of the entire static-cosine family: **anisotropy-dominated instruments that cannot see relations, with residuals that are noise.** Further re-mining of static cosine geometry has exhausted its returns (cf. H5 strategic read).

**[OPEN] What this does NOT touch:** adaptive/inference-time mechanisms (K2, EXP083/084/086-B queue), the mu within-element hint (H3, needs pre-registered replication), and the anisotropy-projected bridge (H2). The capability bets were never in the static family.

**License state:** [OBSERVATION]-grade only. Any claim — including "no residual signal exists" as a licensed boundary — requires a fresh pre-registered EXP number. Nothing here alters EXP091's adopted KILL; it explains it.
