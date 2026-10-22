# Law #14 Review — EXP135 Sprint Design (Worth-It Gate)

**Reviewer:** Independent Scientific Mentor & Adversarial Reviewer (no hand in the design)
**Date:** 2026-10-03
**Document:** `~/workspace/SCBI/research/innovation/EXP135_SPRINT_DESIGN_2026-10-03.md` (154 lines, DRAFT)
**Design-lane verdict under review:** CONDITIONAL RUN (Phase 1 only)
**Review verdict: REJECT** — the design is unsound as specified; the killing reason is decisive and computable at $0 from the committed records right now.

---

## The decisive finding (point 5 — Test B's bars on the committed records)

The design's Test B computes S(B) = #{flips at m⁰ ≤ m̃} − #{flips at m⁰ > m̃} for all 9 EXP135 candidates from `experiments/runs/EXP135_eval/out/exp135_records.json`, with binding bars **S(bridge) > max S(randoms) AND S(bridge) ≥ +8** and §4.4 predicting "S(bridge) ≥ +8".

I computed S(B) exactly per the design's §4.3 spec on the committed records (C1 = bridge per `run_exp135.py:340`; median m̃ = 0.8585 over the 300 unintervened margins):

| Candidate | Pair flips | S(B) |
|---|---|---|
| C1 (bridge) | **0** | **0** |
| C2–C9 (randoms) | 2,1,1,2,0,1,1,1 | 2,1,1,2,0,1,1,1 |

**S(bridge) = 0.** The bars require 0 > 2 and 0 ≥ +8 — both false. Test B fails by the design's *own binding KILL conditions* ("S(bridge) ≤ max S(randoms), or S(bridge) < +8 → KILL") before any execution lane runs. The §4.4 prediction "S(bridge) ≥ +8" is falsified by the very records Phase 1 uses.

**Root cause — a factual error in the gate document.** The design asserts the bridge "flips more pairs than randoms per guard (h)". Guard (h) in `exp135_run_log.txt` is a **randoms-only** inertness check (C2–C9 pair-flips = 2,1,1,2,0,1,1,1, allow ≤ 3); it says nothing about the bridge, and the bridge (C1) flipped **0 of 300 pairs**. My flip-count method matches the run's own guard-(h) accounting exactly, so this is not a measurement artifact. The design lane verified the records' *structure* ("[FACT — structure verified 2026-10-03]") but never computed the flip counts — a five-line check that would have killed the design instantly. The "+8" prediction and the "bridge flips more" claim violate Law #2 (no invented numbers): they are not grounded in the committed records, and appear to conflate EXP077's GPU flips (6 McNemar-b items on a different bench) with EXP135's 300-pair records.

**Deeper consequence.** The bridge's causal efficacy was established in EXP077's records (6 baseline-wrong→bridge-right items). In EXP135's records — the only records where the 9 candidates co-exist — the bridge flipped nothing: it is behaviorally identical to the inert randoms *there*. The design's positive anchor is mislocated. No bar adjustment repairs this: with zero bridge flips, S(bridge) ≡ 0 and no calibration-signed statistic has anything to sign. This is also, ironically, consistent with EXP135's own KILL — but it means the sprint's question cannot even be *attempted* on these records, let alone answered.

---

## Per-point findings

**1. §4.1 structural-failure claim — CONFIRMED.** Checked against `theory/LOOP_SPEC_DRAFT.md` §2.2: C_cons(B;x) is pairwise agreement of induced decisions ŷ_j(B) across views (a direction flipping every view to the *wrong* answer scores C_cons = 1); M̃(B;x) is the clipped normalized mean of M_j(B) = top-1 − top-2 logit, explicitly "target-free". Both inputs are functions of the intervention's output distribution carrying no correctness sign. No λ reweighting can create the absent sign channel. The design's explanation of S_E's failure is correct and non-trivial.

**2. §4.2 "uniquely available channel" — SURVIVES, with a boundary note.** Steelmanned alternatives: (a) cross-view agreement among candidates — sign-less (it is C_cons); (b) the intervention's own margin m¹ — sign-less (target-free by construction). For *correctness-signed* information, the baseline's calibration is indeed the only per-pair channel. Boundary: the baseline's 56.67% accuracy is itself a labeled fact (EXP077) — the design cites it as such, which is the correct epistemic handling. The "uniqueness" holds within the per-pair observable set; cross-item labeled structure (the 6 McNemar items) is validation-only, not selection input.

**3. Test A's Law #7 boundary — FIREWALL SOUND (moot for the sprint).** Test A validates the *instrument* (margin–correctness relationship) using licensed facts from EXP077's GPU record; it scores no candidate, and no candidate score sees labels. Using items *selected* as baseline-wrong/bridge-right to test "are margins lower where baseline is wrong" is a genuine empirical question (margins could be high despite wrongness), not circular. The fallback path (bench labels directly on the cache) is properly flagged for what it is. Ruling: no Law #7 violation — but with Test B dead, Test A cannot license this sprint. It survives as a candidate standalone $0 micro-analysis (informative for S4-5's premise per §5.iv), not as part of this design.

**4. Threshold-crossing confound — HONESTLY STATED, Phase-2 foil argument MOOT.** The design correctly states Phase 1 can KILL but cannot CONFIRM (§3, §9). Whether the foil-bridge breaks the confound is untestable here: Phase 2 is gated on Phase 1, and Phase 1's Test B is already dead. Noted in passing: the design's prediction "foil flips concentrate at high m⁰" is asserted, not derived — the threshold mechanics it names would push *every* direction's flips to low m⁰. This would have needed adversarial scrutiny had Phase 2 ever licensed. It will not.

**5. Test B's bars — NOT NON-VACUOUS; IMPOSSIBLE. (Killing point, see above.)** The bars are binding and well-formed as *falsifiers* — which is precisely why they kill the design at review time. The defect is not the bars but the false factual premise beneath them.

**6. Non-resurrection audit — LOGICALLY VALID, MATERIALLY INAPPLICABLE.** The selection-vs-mechanism distinction is real: using killed lanes' results as test data does not revive their hypotheses, and the audit correctly separates the E-step ranker, S6, and S4-5. But its load-bearing premise — "bridge = positive anchor" — holds in EXP077's records, not in EXP135's. The sprint re-tests no killed hypothesis (true), yet has no positive anchor in the data it uses (fatal).

**7. CONDITIONAL RUN — WRONG. The correct design-lane verdict was DO NOT RUN.** A worth-it gate whose Phase-1 Test B fails on the committed records, by its own binding bars, at $0 verification cost, is not conditionally runnable — it is rejected. The design lane's failure to compute flip counts before predicting "S(bridge) ≥ +8" is the process defect; the worth-it gate's *structure* (binding bars, honest confounds) is what caught it, which is the system working as intended, one stage too late.

---

## Final verdict: REJECT

**Killing reason:** Test B's positive anchor (the bridge, C1) flipped 0 of 300 pairs in the committed EXP135 records, so S(bridge) ≡ 0 and Test B fails the design's own binding bars (S(bridge) > max S(randoms) = 2; S(bridge) ≥ +8) with zero execution cost. The design's factual premise ("bridge flips more pairs than randoms per guard (h)") is false — guard (h) covers only the randoms C2–C9. No condition short of a rewrite repairs this: the sprint's question cannot be attempted on these records.

**What would be needed for a future attempt (not approved, not designed here):** a positive anchor with actual flips in the records the statistic is computed on — e.g., a re-anchoring to EXP077-style GPU records where the bridge flipped 6 items, with the statistic reformulated for that record structure and new matched inert anchors. That is a different design requiring its own worth-it gate and Law #14 review. It is not licensed by this verdict.

**Salvage note:** Test A (calibration instrument check, §3) remains a sound standalone $0 analysis and is informative for S4-5's premise regardless of this sprint's fate. If the CEO wants it, it should be commissioned as its own micro-lane with the Law #7 firewall as specified — not as a back door to this sprint.

**Process note for the CEO:** the worth-it gate functioned — binding bars plus committed records killed a bad idea at design-review cost. The defect was the design lane asserting record-grounded predictions without computing them. Future design lanes: any quantitative prediction about committed records must be accompanied by the actual computation on those records, in the design document, before the verdict.
