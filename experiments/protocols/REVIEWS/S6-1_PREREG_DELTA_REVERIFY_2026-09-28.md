# Independent Delta Re-verification — S6-1 Pre-registration v2 Repair (LOG-4413)

**Role:** Independent Scientific Mentor & Adversarial Reviewer — fresh lane; did not write v1, the Law #14 review (LOG-4411), or the repair (LOG-4412).
**Date:** 2026-09-28. **Mode:** read-only; $0 compute; no model executed; no signed artifact touched.
**Inputs:** v1 `research/innovation/S6-1_PREREG_DRAFT_2026-09-28.md` (LOG-4410); v2 `research/innovation/S6-1_PREREG_DRAFT_v2_2026-09-28.md` (LOG-4412); binding fix list `experiments/protocols/REVIEWS/S6-1_PREREG_LAW14_REVIEW_2026-09-28.md` (LOG-4411).

## Verdict: SIGN (binding)

All five binding fixes verified applied, correctly, and within scope. v2 is ready for CEO execution clearance. No fix failed; no scope creep detected.

## Method

1. **v1 preservation check:** `md5sum` of the v1 file = `b63593d84130805c1f82e864f9eadf3a` — matches the repair lane's LOG-4412 claim exactly. v1 is byte-identical; the repair was copy-then-edit as claimed.
2. **Diff discipline:** the v1→v2 `diff` contains exactly **7 hunks / 25 changed lines**, and every hunk maps to an expected site: title + errata block + status/licensing-chain lines (2 hunks), §2.3 single-environment rule (1), §3 step 4 Threshold KILL (1), §3 scope fence (1), §4.1 item 7 (1), v2 footer line (1). No other file region touched.
3. **Decision-machinery invariance:** no decision-table number, bar (≥6 flips, p<0.01, |ΔM|<0.10, all-strata ΔM_T>0), movement gate, routing rule (steps 0–7), or verdict mapping changed. The step-4 change is exactly F3's mandate (fence-precision), not a routing change.

## Fix-by-fix verification (each recomputed from first principles, not trusted)

- **F1 — §4.1 item 7 [VERIFIED].** v1's false claim ("a dead instrument simultaneously returns T p = 1.0") is gone; the item is now marked "(corrected per Law #14 F1)" and carries the true analysis: (a) truly-frozen regime yields T=0 too → T-significance conjunct fails automatically — the actual neutralization path; (b) B_wrong=0 with significant directional T routes LIVE per the §2.4 asymmetric rule, and a CONTINUE there fires correctly. **Consistency check:** §2.4's liveness rule (v2) states verbatim "B_wrong = 0 with T ≥ 1 → ratio is LIVE (T moved where random didn't — evaluate normally; the asymmetry is disclosed in §4.1 item 4)" — the new item 7 states the identical rule. No internal contradiction remains.
- **F2 — ratio attribution [VERIFIED].** §3 step 4 and the scope fence now attribute 0.01185 to EXP095's α=0.25 point, and 0.0474 to EXP094's α=1.0 (also EXP095 α=1.0). Arithmetic cross-check: 0.0474 × 0.25 = 0.01185 exactly ✓. The enumerated battery's attributions all verify: 0.0237 = 0.0474×0.5 (EXP095 α=0.5) ✓; 0.0948 = 0.0474×2 (EXP095 α=2.0) ✓; 0.1896 = 0.0474×4 (EXP095 α=4.0) ✓; 0.3792 = 0.0474×8 (EXP096 α=8.0) ✓; delivery max band 0.4740 ✓ (matches EXP096's LOG-4407 verdict). Citation error repaired, not an invention.
- **F3 — weakened-form KILL [VERIFIED].** Step 4 now covers any non-live 3.0 — RUN-INVALID *or* FROZEN — with an inline "[state which]" requirement distinguishing representation-replacement from a never-live instrument, and the principle stated inline: "no verdict is earned on an instrument that never went live; the full-strength KILL requires both ratios live." The extension is exactly the mandated one; the routing (weakened KILL → Refuted, fenced) is unchanged.
- **F4 — range notation [VERIFIED].** "0.01185–3.0" is gone from §3 step 4 and the scope fence; replaced by the enumerated tested battery with "no interpolation between tested points is licensed" restated. **§6 risk 4's "(0.01185–0.4740)" retained — BENIGN, confirmed out of scope:** it is descriptive notation inside a risk discussion ("the KILL is scoped to the tested ratios {1.5, 3.0} plus the archived battery (0.01185–0.4740), never to 'all strengths'"), immediately fenced, and the review flagged only §3 step 4 and the scope fence. No operative claim rests on it.
- **F5 — single-environment execution [VERIFIED].** §2.3 now carries the pre-registered rule: all 300 passes in one pinned environment; no mid-run rebuilds, library upgrades, or environment changes between the B run and the injection arms; the §5.3 manifest attests the environment; violation voids the run (Law #13). The determinism premise the single-B design rests on is now guarded.

## What I could not break (adversarial spot-checks)

- The F3 extension does not weaken the full-strength KILL: it still requires both ratios live, and the weakened form is explicitly fenced in the verdict language. No hedge that guarantees a kill — a frozen 3.0 with live 1.5 at T<6 still earns only the weakened form, never the full claim.
- The F1 rewrite does not open a CONTINUE-with-caveat path: the conjunction (T significant AND B_wrong flat AND all-strata ΔM_T>0) is restated unchanged.
- The F4 enumeration includes 0.0237/0.0948 — pure arithmetic from the verified 0.0474 factor (×0.5, ×2.0), disclosed battery points, not new empirical claims.

## Next

Per pipeline: CEO execution clearance → experiment number minted (S6-1 is EXP096+ material). No pilot authorized; no GPU contact. The draft remains DRAFT/UNSIGNED — this SIGN clears the repair, not execution.
