# EXP080 Mathematical License Addendum — LOG-209

**Status:** ADDENDUM to the signed protocol
`experiments/protocols/G2_ORACLE_CEILING_PREREG_SPEC.md`
(PRE-REGISTERED, CEO-signed LOG-172, 2026-09-23).
**The signed protocol text is not modified by this file** (corrections
discipline; §A.6 transition rule, CEO-RATIFIED per LOG-204 ruling 3).
**Dispatch:** LOG-209 · **Date:** 2026-09-23 · **Cost:** $0, CPU, docs only.
**Author role:** Track-1 (theory) protocol specialist.

**Law #15 (on record, LOG-209):**
1. Q: the recovered license (graded) for EXP080's oracle-ceiling design, plus the
   control story under the §H7 demotion.
2. Decision: CONTINUE — this signed addendum is a precondition for GPU
   clearance of EXP080; without it clearance cannot be sought.
3. Cheapest: $0 paperwork vs re-drafting and re-reviewing a signed protocol
   through full Law #14 cycles (weeks, zero scientific gain).
4. License: this addendum IS the Q4 instrument — its L1–L4, reviewer-verified.

---

## Mathematical License (binding — Law #15 Q4; see research/foundations/MATHEMATICAL_LICENSE_STANDARD_2026-09-23.md)

**License grade:** IN-HOUSE-PROOF (promotion-ready). Per §A.3: may authorize a
pilot or scale-gated run only; full-run authorization requires promotion via
Law #14 review of the proof attacking each step per Charter M2.2.
(INTUITION is disqualifying — not cited here.)

### L1. Authorizing result
- **Statement (exact):** **Lemma L1 — the superset lemma** (§4.5 of the signed
  spec): *"Under the §11 determinism pin (seeds 7201/7202/20260923 fixed,
  deterministic algorithms where supported), on C3-vs-C2:
  c = #{x : C2 correct ∧ C3 wrong} = 0 exactly."*
  *Proof.* B_agg ∈ P (§3.1 item 10). If r(B_agg; x) = 1 then
  max_{B∈P} r(B; x) = 1, and the §4.1 tie-break draws only among the correct
  candidates — so C3 is correct whenever C2 is. Hence
  {C2 correct} ⊆ {C3 correct} exactly, and c = 0. ∎
- **Source:** in-house proof,
  `experiments/protocols/G2_ORACLE_CEILING_PREREG_SPEC.md` §4.5. The
  LOG-171 Law #14 re-review
  (`reports/adversarial_review_g2_prereg_r2_2026-09-23.md`, §B2) found the
  proof **"airtight under the determinism pin"** and independently re-derived
  the b-term branch mapping; CEO signed PRE-REGISTERED at LOG-172 on that
  SIGN. The proof has not yet been attacked step-by-step per Charter M2.2 —
  hence IN-HOUSE-PROOF, not PROVEN-LEMMA.
- **Epistemic label:** [THEOREM] — conditional on the determinism pin; per
  Math Charter M2.4 the condition is named in every citation of it.

### L2. Quantitative prediction for the primary endpoint
- **Endpoint (verbatim from §7):** Primary (confirmatory): ΔM (percentage
  points) on paired decisions, C3 vs C1; McNemar exact two-sided on (b, c).
  Key comparison (the kill): C3 vs C2 — b = oracle-rescues (C3 correct, C2
  wrong); c = oracle-corruptions (C3 wrong, C2 correct).
- **Prediction:** (1) Under the determinism pin, **c = 0 exactly**, so the
  C3-vs-C2 McNemar collapses to a b-only binomial test on b — under the signed
  spec's doubled two-sided exact convention (p = 2^{1−b}; hence (c) ⟺ b ≤ 5, not
  b ≤ 4). Branch mapping
  in b-terms (§6.1, independently recomputed by the LOG-171 reviewer):
  **(c) ⟺ b ≤ 5**; **(d) ⟺ b ∈ {6, 7}**; **(e) ⟺ b ≥ 8**.
  (2) C3 ⊇ C2 pointwise ⇒ ΔM_oracle ≥ ΔM_static on every realization — the
  pool-oracle is an **upper bound by construction** on the selection prize: a
  realizable target-free selector over P cannot *systematically* beat the
  label-informed oracle in expectation (§1.2).
  (3) The §9(d)/(e) "output room" licenses quantify a selection prize **only
  if** non-bridge marginal rescues (bin (ii) of the §7 decomposition) > 0.
- **Derivation:** (1)–(2) are Lemma L1 plus the §4.1 argmax definition
  (B*(x) = argmax_{B∈P} r(B; x)); (3) is the §9(d)/(e) B2c gating on the §7
  marginal-rescue decomposition — all direct algebra, no new modeling.

### L3. Breaking point
- **Falsifying observation (the lemma itself):** any measured item with
  C2 correct ∧ C3 wrong (c > 0) under the determinism pin ⇒ Lemma L1 is
  refuted; the determinism pin is the prime suspect (two separate forward
  passes of B_agg must agree — §4.5). **Decision:** suspend the b-terms branch
  mapping and diagnose the pin; the tree's general (b, c)-form still assigns
  every cell (M5.2) — this is why the tree is not written only in b-terms.
- **Falsifying observation (the licensed question):** bin(ii) (non-bridge pool
  ceiling) = 0 ⇒ the (d)/(e) "output room" licenses **collapse to "bridge
  ceiling, not pool ceiling" reporting only** (Law #8); no selection-signal
  license issues. The kill in branch (c) (b ≤ 5, p ≥ 0.05 ⇒ Not supported,
  evaluator program stood down) **stands per m7**.
- **Falsifying observation (license scope):** any downstream use of the
  label-informed B*(x) directions as a proposed *technique* (§4.4 anti-cheat)
  = protocol violation — the license covers the ceiling **measurement** only;
  Law #7's test-time information boundary applies to any future evaluator,
  not to this diagnostic (§1.1). **Decision:** KILL the misuse; invalid run,
  reported per Law #8 — never silently corrected.
- **Outcome partition:** §6.1 McNemar grid + §7 impossible-cells-carrying-proof
  + §9 branch precedence cover every cell (M5.2/M5.3/M5.4); all reachability
  and power claims are conditional on c = 0, named as such.

### L4. Assumption inventory
- **A1 — the determinism pin** (§11: seeds 7201/7202/20260923 fixed;
  deterministic algorithms "where supported"). Justification: pinned seeds +
  the Δθ=0 SHA-256 guard; discharge: runtime pre/post hash match. If the pin
  fails, c > 0 cells become reachable — assigned, not fatal to the tree.
- **A-family (§8):** the 10-member pool P at layer 20 fairly represents the
  output-side evaluator program's search space; the branch-(c) kill is
  licensed **only within this pre-registered family**, on this
  benchmark/model/layer. Not dischargeable inside the protocol — it bounds
  the license, recorded not smuggled.
- **A-generous (§4.3):** selecting on the test item's own label *inflates* the
  measured ceiling; it cannot deflate it. Direction of risk: the kill is
  easier to trust, the win is harder to trust as achievable. The §9 +12pp
  bar, the Phase-B gating, and the asymmetry (§1.2) carry the conservatism.
- **A-bridge-dominance (§3.2):** the self-bridge is expected to dominate
  selection where it rescues; the §7 marginal-rescue decomposition is the
  pre-registered check. Discharge: the decomposition itself.
- **Promotion path:** PROVEN-LEMMA via a Law #14 review of the lemma
  attacking each proof step per Charter M2.2 (LOG-171 verified the pin and
  the statement and re-derived the branch mapping — a protocol review, not a
  per-step M2.2 proof attack); promotion logged in `reports/research_log.md`.

---

## §H7 control relabeling (LOG-204 ruling 1 — DEMOTE)

C7 ("Self-bridge (positive control)", §5) is hereby relabeled **"rescue
control (known-answer direction), NOT a mechanism control"** per the LOG-204
ruling. Its positive-control status for autonomous-mechanism questions is
REVOKED. Its surviving, non-mechanism roles are exactly the signed ones:
the §7 C3-vs-C7 secondary measurement (zero extra passes — data already
collected) and the §9(c) bridge-replication contingency (Law #8:
distinguishes *bridge-degradation* from *evaluator-failure* when the kill
fires). C7 non-replication is **not** a validity failure — branch (b)
contains no C7 conjunct by design (§6.1 m4); it is the measured ceiling.

**What serves as the control for EXP080's autonomous-mechanism question:**
the honest answer is that EXP080 tests none. It is a **label-informed ceiling
measurement by design** (§1.1; evidentiary Level 1 only — "can improve
inference"); no autonomous (label-free) selection claim is on the table, so
**no label-free control exists in this design and none is needed**. The
selection question ("does *selection* beat random?") is controlled by C4
(random selection over P, branch (f)); the target-free directions an
evaluator could construct are the pseudo-bridges inside the pool itself.
Any autonomous-mechanism claim belongs to Phase B behind a new
pre-registration — this addendum does not license it.

---

## Honest-reporting note (§A.6 point 5)

Best honest grade for the recovered license: **IN-HOUSE-PROOF** — matches the
§A.6 sketch; no downgrade required. Multi-license note per §A.3:
H_ceiling-G2 itself is a [HYPOTHESIS] — the protocol is its falsification
attempt, so the hypothesis-side license is CONJECTURE-UNDER-TEST; the weakest
load-bearing grade authorizes the cheapest discriminating experiment only —
which this is (1,320 passes, ≈60s on 2×T4, free-tier trivial). The grade
therefore does not change the clearance story; it is reported because the
rubric requires it.

---

**Signed:** Track-1 (theory) protocol specialist · LOG-209 · 2026-09-23 ·
**Law #14 review:** SIGN-WITH-FIXES — LOG-210 (independent Track-7 adversarial reviewer, no prior involvement in §A.6 addenda or EXP080/081 protocols), 2026-09-23. Two mechanical fixes applied by the reviewer (McNemar convention phrasing; norm-difference citation). Report: `reports/adversarial_review_addenda_law14_2026-09-23.md`.
