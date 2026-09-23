# Law #14 Adversarial Review — G2 Oracle-Ceiling Pre-registration Draft

**Verdict: REVISE** (4 blocking items; re-review required after fixes)
**Role:** Law #14 Adversarial Reviewer (LOG-152 dispatch; answers to the CEO; no instruction to soften was accepted or followed)
**Date:** 2026-09-23
**Target:** `experiments/protocols/G2_ORACLE_CEILING_PREREG_SPEC.md` (LOG-143 draft, LOG-151; no experiment number minted)
**Banner authorized:** NONE — remains **DRAFT**. The PRE-REGISTERED banner advances only on a SIGN after re-review.
**Scope:** analysis only — no GPU, no experiments. Every load-bearing number below was recomputed, not trusted.

---

## 0. What the draft gets right (verified clean — V1–V9)

These were attacked and held:

- **V1 — McNemar arithmetic independently recomputed:** (5,0)→p=0.0625, (6,0)→p=0.03125, (8,0)→p=0.007812, (11,3)→p=0.057373, (0,0)→p=1.0 — all match the §6.1 table exactly. ΔM values (+8.33/+10.0/+13.33pp) confirmed.
- **V2 — Budget arithmetic:** 12×60+7×60 = 720+420 = 1,140 ✓. (The corrected 10-member pool of §B3 recomputes to 600+420 = **1,020**.)
- **V3 — m7 precedent is real:** research log L3057 documents EXP070's re-review widening the kill trigger to p≥0.05 to close the positive-but-nonsignificant partition gap. Adoption here is legitimate.
- **V4 — Feasibility proof structure is valid** (conditional on branch (a)): the LOG-138 discipline is honored — N_final is derived in closed form before the gate, not asserted. LOG-113's independent tokenizer verification (all 10 benchmark entities single-token) is real; the e_median=0.0544 degeneracy-guard anchor is real (LOG-116).
- **V5 — Bridge construction grounded:** the draft's b(x) = normalize(W_U[t_x]−W_U[f_x]) via `get_output_embeddings()` matches `run_exp078.py` L487–493 verbatim (LOG-114 fix respected).
- **V6 — No Law #4 re-run:** G2's output-side pool is a different family from EXP070's hidden-state pool; EXP070's uninformative-probe failure mode is absent by construction (no probe exists). EXP077/078 distinguished, not repeated.
- **V7 — No rescue pre-commitment:** the draft text contains no "bridge-removed re-run" follow-up; the (c) re-motivation path is correctly scoped to *a different family + new pre-registration*. (LOG-143's handoff summary overstates this — the draft is cleaner than its summary.)
- **V8 — Hygiene:** anti-cheat clause armed; Δθ=0 guard *specified* (pre/post SHA-256 over sorted-keys state_dict concatenation, binding = runtime match) not gestured; N1 retained; verdict vocabulary uses only permitted categories (Supported / Not supported / Inconclusive / Underdetermined); evidentiary level capped at 1 with explicit level-2/3 refusals; A-family named as the false-kill route.
- **V9 — Tree precedence is sound:** (a)→(b)→(f)→exactly-one-of-(c/d/e), (g) informational overlay — unique and exhaustive on the (C3-vs-C2) space (modulo blocking item B4's correction).

---

## 1. Blocking items (must be fixed; re-review required)

### B1 — The Q_S artifact does not exist; pool member 9 is unsourcable as specified; the provenance claim is false

**[FACT — verified by inspection]:**
- `run_exp078.py` writes `exp078_vectors.pt` (containing Q_S) at L750 — *after* the energy gate.
- On HALT_ENERGY the runner calls `sys.exit(0)` at L555 via `save_halt`, which persists only `exp078_results.json` + log. **No Q_S is ever saved on the halt path.**
- The EXP078 GPU run halted at (a) ENERGY_GATE_HALT (LOG-116); the CPU smoke also halted at HALT_ENERGY (LOG-114). The RUNBOOK checklist item "`exp078_vectors.pt` exists" is unchecked.
- Filesystem sweep: no `exp078_vectors.pt` anywhere in `~/workspace` (only `exp077_vectors.pt`, a different experiment); `exp078_bundle.zip` contains code only.

**Consequence:** §3.1 item 9's sourcing — "the archived EXP078 CPU-smoke artifact (the smoke run built and persisted Q_S; LOG-114)" — is **false**. No such artifact was ever persisted. At G2 build time the (a)-halt "Q_S artifact missing" will *always* fire, so the protocol as written can never execute. A pre-registration whose readiness gate cannot pass is not a fail-closed design; it is a stillborn document. The hash-pinning question the drafter flagged is moot: there is nothing to pin.

**Required — drafter's choice, both compliant:**
- **Path A (rebuild):** pre-register a Phase-0 weight-only Q_S rebuild inside G2: the exact pinned support set (the F2-corrected EXP078 support set — item list + seeds, not a prose pointer), ~300 support forward passes, deterministic thin-QR with its determinism pinned, orthonormality/rank asserts, artifact hash recorded in the manifest. Budget becomes 600+300+420 = **1,320** passes (with the B3 pool correction). The (a)-halt then covers genuine build failures, not a guaranteed one.
- **Path B (drop):** remove the P_S-residue member (pool → 9; budget 540+420 = **960**), with an explicit rationale for deviating from the SPRINT2 §G2 pool enumeration. Note: EXP078 measured e_median=0.0544 (bridge power ~95% outside S), so this member is expected to be near-orthogonal to the bridge — dropping it is scientifically cheap.
- **Either way:** delete the false provenance parenthetical. A false artifact-provenance claim in a pre-registration is Law #2-adjacent and blocks any SIGN on its own.

### B2 — The kill criterion tests bridge replication, not the selection prize (hypothesis infidelity)

**[FACT — derived, then verified against the draft's own constructions]:** B_agg ∈ P (§3.1 item 10) and selection is argmax-correctness (§4.1). Under the §11 determinism pin, {C2 correct} ⊆ {C3 correct} *exactly*: if r(B_agg;x)=1 then max_B r(B;x)=1 and the tie-break draws only among correct candidates, so C3 is correct whenever C2 is. **Hence c = 0 deterministically on C3-vs-C2** — the McNemar collapses to a one-sided binomial test on b, and:

- (c) ⟺ b ≤ 5; (d) ⟺ b ∈ {6,7}; (e) ⟺ b ≥ 8.
- b ≥ b_bridge := #{x : bridge correct ∧ B_agg wrong} (bridge ∈ P). Historical b_bridge = 6 (GPU) — exactly the (d) floor.

The draft never states this lemma, and its absence corrupts three things:

1. **The kill is misattributed.** Given the boundary null (C2 ≡ C1, checked by (g)), branch (c) can fire *only* via bridge non-replication (b ≤ 5 ⟺ the bridge rescues ≤5 items). The (c) license — "the output-side evaluator program is stood down… no target-free evaluator over this family can justify its cost" — is therefore never a clean evaluator-kill; it always coincides with the bridge degrading from its measured 6. One item of drift stands down the program for the bridge's failure, while the evaluator-specific question (do the target-free pseudo-bridges add anything?) is never the deciding factor.
2. **Survival is unearned.** If the bridge replicates at 6, (d) fires with all 6 rescues from the bridge — and the (d) license "a selection signal exists in the output room" is issued for what is, measurably, a bridge signal. The (e) license ("a per-instance selection prize exists in the output room") has the same flaw.
3. **The §7 composition audit cannot detect the trap it was built for.** It audits "the distribution of B*(x) over the 12 pool members on items where C3 beats C2" — but B*(x) is a *uniform-random draw over the correct set* (§4.1 tie-break), so its distribution measures tie density, not oracle preference. It is confounded by construction and cannot distinguish "bridge ceiling" from "pool ceiling."

**Required (all spec-text edits; no new data collection):**
- **B2a — State the superset lemma** (M1/M5.4): under the determinism pin, c=0 exactly; restate the branch mapping in b-terms ((c)⟺b≤5, (d)⟺b∈{6,7}, (e)⟺b≥8). Note the tree's general form still assigns any c>0 cell if determinism fails (no M5.2 violation), but all reachability/power claims are conditional on c=0.
- **B2b — Fix the audit:** replace the B*(x)-distribution audit with the correct-set marginal-rescue decomposition, pre-registered: per rescued item, the full correct set; report (i) rescued with bridge correct, (ii) rescued with bridge wrong but ≥1 non-bridge member correct (**the true selection prize**), (iii) rescued with *only* non-bridge members correct. Add a pre-registered **secondary C3-vs-C7 McNemar** (zero extra passes — data already collected) as the direct bridge-superiority measure feeding the audit. No new branch (M5.2 intact); it is measurement, not a ruling.
- **B2c — Gate the license language:** the (d)/(e) "selection signal/prize exists in the output room" licenses may be issued **only if** the non-bridge marginal rescue count (B2b-ii) is > 0; otherwise the ruling must read "**bridge ceiling**, not pool ceiling" (Law #8), and (d)'s "program survives" must be qualified as resting on the bridge alone. Correct (c)'s license to carry the bridge-replication contingency: given C2-null replication, (c) ⟺ bridge rescues ≤5 — the stand-down is on the pool as measured, with bridge-degradation distinguished from evaluator-failure in the report (Law #8 honesty; the kill itself stays simple per the m7 discipline).

### B3 — B_⊥ and B_wrong must come OUT of the selection pool (budget-fitting, not principle)

**[FACT]:** the source idea (`research/innovation/SPRINT2_2026-09-23.md` §G2) enumerates the pool as {self-bridge, 7 pseudo-bridges, P_S-residue, B_agg} = **10 members**. The 12-count — and the 1,140 figure — closes only with B_⊥ and B_wrong in the *selection* pool, which the drafter admits was arithmetic-driven (LOG-143). The "oracle must fall back to a control so the gap is pure selection gain" rationale does not support their inclusion: **B_agg alone** is the fallback that forces c=0 and makes the gap pure selection gain (§B2). B_⊥/B_wrong add nothing to that argument.

Including known-dead controls in an argmax-correctness pool is not neutral:
- it can only **inflate** b (a dead control uniquely correct by chance = a junk rescue in the ceiling);
- it **dilutes the (f)-branch instrument** (C4 uniform over 12 with 2 dead members is a weaker attribution test than uniform over 10 live candidates);
- it pollutes the composition audit with meaningless tie-break draws;
- it costs 120 forward passes (~10.5% of budget) for negative scientific value.

**Required:** remove B_⊥ and B_wrong from the *selection* pool P (they stay as test conditions C5/C6 — the forced baselines). Consequences, all mechanical: |P|=10; §10 budget becomes 10×60+7×60 = **1,020** passes (~47s); §4.2 C4 uniform over 10 (seed 7202 unchanged); §3/§7/checklist updated. This realigns the spec with its own source idea.

### B4 — The reachability table contains an unreachable cell (M5.4)

§6.1 lists (b,c)=(11,3) — "the ≥+12pp-but-nonsignificant cell exists and is assigned to (c), closing the partition gap" — and claims "every branch is reachable by construction." Under the B2a lemma (c=0 by construction under determinism), **c>0 cells are unreachable**; there is no partition gap for (11,3) to close. An impossible cell presented as reachable is an M5.4 violation in the strong form (unargued *and* misclassified).

**Required:** move (11,3) to the §7 impossible-cells list **with its proof** ("c=0 under the §11 determinism pin + B_agg ∈ P ⇒ any c>0 cell unreachable"), and restate §6.1 reachability in b-terms: (c) via b≤5 (the null region the program inhabits), (d) via b∈{6,7}, (e) via b≥8. The (5,0) m7 cell stays as the canonical positive-but-nonsignificant assignment.

---

## 2. Minor findings (fix within one review cycle; non-blocking for a future SIGN)

- **m1 — §4.1's M3 rationale is misapplied.** Under correctness-argmax, the tie-break *cannot* affect b (any draw among correct candidates is correct; any draw among all-wrong is wrong) — so a B_agg-preferring tie-break could not "bias the instrument toward the kill branch." The M3 correction is vacuous here. Keep direction-neutral (it is the right choice for audit cleanliness), but correct the rationale or drop the M3 citation.
- **m2 — §9(b): name the comparator.** "C5/C6 show McNemar p<0.05" — against what? (Presumably C1.) Pin it.
- **m3 — §9(b) C1 band [40%,70%] is uncited.** Provenance exists (EXP067 headroom gate per LOG-129; EXP077 smoke C1=0.60) — cite it.
- **m4 — §6.1 "branch (b)'s C7 requirement" is a misnomer.** Branch (b) contains no C7 conjunct — deliberately (C7 non-replication is the measured ceiling, not invalidity). Reword as positive-control *detectability*, not a (b) requirement.
- **m5 — Cell completeness (M5.2/M5.3):** branches (a), (b), (f) carry no explicit evidentiary-level statement, and (g) carries no verdict line. Add: (a)/(b) level — none (halt/invalid; verdict Inconclusive already stated); (f) — level 1 stated explicitly; (g) — "verdict: none; informational overlay by design."
- **m6 — §2 SHA-256 procedure vs history.** The draft pins "sorted keys" — fine as a procedure — but LOG-123 root-caused that EXP067's registered value `4c242d9a…` was computed *unsorted* despite "sorted keys" text. Document that the registered sanity value must not be compared against a sorted-keys computation, to avoid a spurious sanity-mismatch alarm at execution.
- **m7 — §7 degenerate-input "proof"** ("b=c ⇒ the exact binomial tail sums to 1") is hand-wavy; restate cleanly via the B2a lemma (b=c=0 is the only b=c case under determinism; p=1.0 by convention for the degenerate test).

---

## 3. Attack-point rulings (summary)

1. **Hypothesis fidelity — FAIL as written (B2).** The kill criterion is a genuine falsifier of the *pool ceiling* but not of the *evaluator program's selection premise*: it is too easy to survive on (bridge guarantees b≥~6 → (d)/(e) on the bridge's back, with unearned "output room" licenses) and misattributed on death (a kill always coincides with bridge non-replication). Fixable at the license/audit level per B2a–c — no design change needed beyond B1/B3.
2. **Pool inclusion — REQUIRE REMOVAL (B3).** Budget-fitting, admitted; unsupported by the drafter's own rationale; the source idea's pool is 10. B_⊥/B_wrong stay as C5/C6 test conditions.
3. **Q_S sourcing — hash-pinning is MOOT (B1).** The artifact does not exist (verified: halt path exits before `torch.save`; no .pt in repo; RUNBOOK unchecked). The (a)-halt path is pre-registered but would always fire — that is not fail-closed, it is stillborn. Require the Path A rebuild (fully pre-registered) or Path B drop, and deletion of the false provenance claim.
4. **Dominance trap — audit INSUFFICIENT as written (B2b–c).** The B*(x)-distribution audit is confounded by the uniform tie-break. The draft does *not* pre-commit to a bridge-removed rescue re-run (good — LOG-143's summary overstates); the (c) re-motivation path is correctly scoped. Require the marginal-rescue audit + C3-vs-C7 secondary + license gating.
5. **Decision tree — exhaustive but mislabeled (B4, m5).** The (a)/(b)/(f)/(c)/(d)/(e)/(g) partition is unique and exhaustive; every cell carries LICENSES/DOES-NOT-LICENSE and a permitted verdict. Defects: (11,3) misclassified as reachable (B4); missing level/verdict lines on (a)/(b)/(f)/(g) (m5).
6. **Feasibility & budget — PASS with corrections.** Arithmetic recomputed ✓ (1,140 as written; 1,020 under B3; 1,320 under B1-Path-A+B3). The closed-form N_final=60 proof is valid conditional on (a) — the LOG-138 discipline is genuinely honored. Δθ=0 guard specified, not gestured (m6 aside).
7. **Labeling & levels — PASS.** Double-labeling discipline held on load-bearing claims; no banned phrases as verdicts ("worth-chasing" is a threshold name, not a verdict category); level-1 cap explicit throughout with level-2/3 refusals in (e).
8. **Prior art & novelty — PASS.** N1 retained; forced baselines present (C1/C2/C5/C6/C7); no silent re-run of a killed design (EXP070's pool was hidden-state; its probe failure mode is absent by construction).

---

## 4. Required resubmission package

1. B1: choose Path A (pre-registered Q_S rebuild, +300 passes) or Path B (drop P_S-residue); delete the false LOG-114 provenance claim.
2. B2a: state the c=0 superset lemma; restate branch mapping in b-terms.
3. B2b: replace the audit with the marginal-rescue decomposition + pre-registered C3-vs-C7 secondary.
4. B2c: gate (d)/(e) "output room" licenses on non-bridge marginal rescues > 0 ("bridge ceiling" reporting otherwise); add the bridge-contingency note to (c).
5. B3: 10-member selection pool; budget 1,020 (1,320 with B1-Path-A); C4 over 10.
6. B4: (11,3) → impossible-cells with proof; §6.1 reachability in b-terms.
7. m1–m7 fixed.

No results exist under this protocol; no primary artifacts were touched; no numbers were invented. The banner stays **DRAFT** until a Law #14 re-review signs the resubmission.
