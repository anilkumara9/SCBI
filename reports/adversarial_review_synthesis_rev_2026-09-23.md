# Law #14 Adversarial Review — LOG-188 — Revised A–J Synthesis

**Target:** `research/synthesis/SYNTHESIS_A_J_REV_2026-09-23.md` (1,912 lines), read in full, against the LOG-158 original, the mentor's LOG-183 review (11 findings), LOG-185 (sole citation authority), both binding specs, and the LOG-186 ruling (`reports/research_log.md:3578`, confirmed as the record — no separate audit file exists).

**Supplementary charges applied during review:** the mentor's 9 re-review acceptance criteria (items 13–21) and the Fresh-object rule (item 22).

## VERDICT: SIGN-WITH-FIXES

The revision genuinely implements the mentor's program: the statistical replacement is real (not lipstick), the literature map is faithful to LOG-185 including both partials, the false H5a sentence is extinct, the bridge reframing holds, the falsification architecture is unsoftened, and H3 has no rescue path. **No design-level defect** warranting REVISE. **12 mechanical defects** found, all fixable by the Lead with exact replacement text — three of them (F3/F4/F5) touch the statistical protocol's pre-data-contact completeness and must be fixed before the mentor's re-review, because they are exactly the class of "formal weakness that could let a positive result survive on a technicality."

All 12 fixes were applied by the Research Lead on 2026-09-23 (verified by grep; the three F5 CI corrections were independently recomputed by the Lead with a Tango score implementation — all three corrected lowers confirmed: −0.0132, +0.0651, +0.0338).

---

## Per-attack-point findings

**1. Statistics, cosmetic vs real — GENUINE, with three exceptions.** All seven mandated sites replaced (DPRS Box 2, C4 Box 2, C5 Box 2, F3 predictions, G4 S(iv), G4 F1, F1 cull — verified in text). The four-cell mapping (§G1b) is exhaustive and mutually exclusive (case analysis: L>δ→S; else L≤δ with U<0→NS, 0≤U<δ→NS, U≥δ→I; no overlap, no limbo). "p ≥ 0.05" occurs only in ban statements (lines 35, 1201, 1833, 1905). **Exceptions:** (a) K2 line 1487 retained "difference n.s." as a decision input — the banned sin in different letters (see F2); (b) three A3 lower CIs are miscomputed/mislabeled (see F5); (c) Level-2 CI level ambiguous (see F3).

**2. Power honesty — arithmetic SOUND, protocol INCOMPLETE.** Recomputed independently: two-sided exact McNemar at N=80, c=0 needs b≥6 → MDE=7.5pp ✓ (note: the draft correctly says "two-sided" where the binding spec said "one-sided" — the drafter fixed the spec's slip). At Level-2 α₂=0.00625, MDE=11.25pp (b≥9) — recomputed — which exceeds 2·δ_min=10pp, so the adaptation rule fires at N=80 for every candidate. The draft is honest that Bonferroni is conservative and that Inconclusive (not Not supported) is the container — it does **not** silently license underpowered kills. But the adaptation rule said "N is increased per the stated rule" (line 1240) and **no such rule was stated anywhere** — the pre-registration was incomplete on its own terms (see F4).

**3. Alpha hierarchy — coherent structure, overclaimed wording.** Level-2 Bonferroni over 8 candidates is real; the anti-recycling rule has teeth (no same-data re-analysis to manufacture a pass). But "Total program α = 0.05, partitioned across four levels" was false as a partition: Level 1 spends α₁=0.05, Level 2 spends 8×0.00625=0.05, Level 3 spends 0.05 per check. And "re-consume Level-2 budget" meant FWER is controlled *within* each NTDP run, not across sequential re-tests — the budget is replenished, contradicting a strict "no borrowing" reading (see F12).

**4. Literature traceability — PASS for all seven.** Every mechanism, venue, and date matches LOG-185 verbatim: LTPO (arXiv-only, no venue invented ✓), Meta-Reasoner (Findings of ACL 2026; 9–12%/28–35% ✓), LatentMAS (ICML 2026 spotlight ✓), NoisyCoconut qualified at its only venue-carrying use ("arXiv preprint under review at TMLR; **not** a published TMLR paper" ✓; all other uses are "NoisyCoconut-style," needing no venue), RISER with the external-router nuance at both mentions ✓, ∇-Reasoner (ICLR 2026; 80.4% MATH-500 on Qwen-2.5-7B-Instruct ✓), Activation-LQR under its actual title with the proceedings listing ✓. Two details LOG-185 does not support, both carried from LOG-158: the ∇-Reasoner "matches GRPO at 10–40% fewer model calls" (the B5 tag discloses "verified by Cluster B via public web search" two-tier provenance — disclosed) and DEER's figures tagged bare "[FACT]/[OBSERVATION, verified]" (provenance overstated; see F10).

**5. The false sentence — EXTINCT.** Line 937 explicitly retracts ("the claim that no competitor uses inter-instance latent exchange is retracted (it was false)"); R(h) records the kill. Remaining "inter-instance latent exchange" occurrences describe LatentMAS's occupancy — the opposite of the false claim. No paraphrase or implication survives.

**6. Bridge reframing — CONSISTENT.** "Converge" appears only in negated contexts. A3/A7/C1 all carry the one-confounded-construction framing, the Law-#7 caveat, and the raised K1/K3 weight ✓.

**7. TTPS — baseline operational, primitive check aspirational.** The interpreter-only baseline is constructible as specified ✓. But "no task solver hidden in primitives" was enforced by documentation + prohibition, not by a check (see F8).

**8. ASR — [INCOMPLETE] honest, advancement ungated.** Tag present, "inadmissible" language present, E-summary discloses. But nothing structurally barred C4 from §F/§G — "inadmissible" was asserted, not gated (see F9).

**9. Preservation — FULL STRENGTH.** A4 (Refuted), A5 (Not supported on the pooled bound — computation re-verified: exactly ±0.0126 at N=300, U<δ_min ✓), A6, A9, D2 (all five), F1 structure, H3 ("executes without re-approval"), §I definition + grades, track-7 verdict, §I "rules out the entire corpus" — all unsoftened, no narrowed licenses ✓.

**10. EXP023 — matches LOG-186 on every load-bearing point** (no grid; EXP013/EXP030 attributions; seed-123→pinned config→seed-84; no Bonferroni; pooled b=14, c=1, p=0.000488 with pre-specification caveat; "Supported (L1, selection-optimism caveat)"). The caveat text omitted two of the ruling's precise specifics (see F6).

**11. R(h) — substantively complete, systematically misnumbered.** Every finding addressed, but finding numbers were off-by-one from #6 onward against the mentor's own numbering, and the burden-of-proof box was misattributed to "finding #10" — it comes from the review's closing section, not a numbered finding (see F1). For a document returning to the mentor, misattributing the mentor's finding numbers is a real defect.

**12. G5 arithmetic — CONSISTENT.** 80×15×8=9,600F ✓; 15 conditions consistent with the M15 addition ✓; H5 80×4×8=2,560≈2,500F ✓.

**13. Prior-art verification (Law #3) — PASS** for all new claims; 0 UNVERIFIED per LOG-185; SVF correctly marked UNVERIFIED, unplaced, never used rhetorically ✓. See point 4 for the two carried-forward details.

**14. Narrower boundary — PASS for all four.** DPRS vs LTPO (discrete readout-space top-k perturbation search ⊂ general latent optimization ✓); ASR vs Meta-Reasoner (target-free internal-reward bandit + policy-scope pin ⊂ contextual strategy routing ✓); LCMIC vs LatentMAS (backbone+residual-exchange+verifier/arbiter+relational-task formulation ⊂ shared-memory collaboration ✓); CLB vs NoisyCoconut (intra-layer fork + provably non-selection merge ⊂ branching+consensus, with the draft noting NoisyCoconut's own aggregation is selection-adjacent ✓).

**15. p≥0.05 ban —** see point 1; only K2's "n.s." survived (fixed by F2).

**16. Pre-data-contact completeness — three gaps:** (a) Level-2 CI level unpinned (F3); (b) N-increase "stated rule" phantom (F4); (c) K1 "cos ≈ 1" threshold unpinned (F11). All mechanical — all fixed.

**17. A3/A7 reframing —** see point 6 ✓.

**18. K1/K2/K3 ordering — SOUND, no hole.** K1 tilt → reading withdrawn, positive-control status revoked, E8 premise removed, C1 setpoint re-specified ✓ collapses. K2 bypass-Supported → "logit steering, period" ✓ collapses. K3 compliant-null → autonomous-room Not supported ✓ collapses. Order K1→K2→K3 is logically prior-chain-correct, and each is "designed to lose cleanly." (K2 needed F2 for full discipline — applied.)

**19. Mechanism baselines — PASS.** TTPS interpreter-only (tests the interpreter's contribution), CLB merge-vs-select + NoisyCoconut-style (tests non-selection), LCMIC §F3 four-arm (tests the channel), ASR uniform-heavy + Meta-Reasoner comparator (tests the allocation policy). Each discriminates the claimed mechanism, none merely the implementation ✓.

**20. Compute matching — PASS.** The two-number rule's cost inventory (§G1b) covers Jacobians, backward passes, reward-model training/inference, interpreter ops, bandit updates, memory movement, latent-agent communication, cached-gain construction; applied in G2/G3/G5. No unmatched cost found.

**21. H3 executability — PASS.** Grep for discretionary language ("may retain," "further analysis," "pending re-analysis," "discretionary") is clean. The trigger is four arithmetic/verdict conditions. H4's degenerate branch and §H7's reserved CEO decision are legitimate, not rescues ✓.

**22. Fresh-object rule.** (a) The draft discloses its discharge stance in the header ("cites their FACTS as given"). Named carried-forward conclusions: B1 CAA-equivalence, B4 Self-Refine/PPLM mappings, DEER figures, STARS constraint, GRPO-matching detail, A8 handover numbers (explicitly caveated "selection context unverified"). The track-7 verdict rests on B1 (carried) + A4/A5 (primary artifacts; A5 re-derived under the new stats). This is disclosed architecture, not smuggling — but LOG-184 scoped verification to the seven papers, so whether the mentor accepts the carried base is the mentor's adjudication, not something this draft can settle. (b) Material-change audit: the one retained conclusion whose footing changed (A5) is explicitly addressed in R(h) ("stronger footing, not weaker"); all downgrades/narrowings (A1, A3, DPRS, C4, C5, C6, EXP023) are explicit; A4/A6/A9/D2/F1/H3/§I/track-7 are genuinely unaffected by the new machinery. No theory-preservation defect. (c) Architecture vs conclusions properly distinguished.

**Standing principle (machinery vs protocol):** the draft adds machinery only where the mentor ordered it (M15 comparators, §F3 fourth arm). No scope creep. Judged on protocol + boundary: both are sound modulo the fixes.

---

## Fixes applied by the Research Lead (all mechanical-and-verifiable)

- **F1.** Finding references renumbered to the mentor's numbering (TTPS=#7, ASR=#8, FLOP accounting=#9, EXP023=#10; burden-of-proof unnumbered as the review's closing note); verified by grep — no stale numbers remain.
- **F2.** K2 kill criterion: "(ΔM_a ≥ ΔM_b, difference n.s.)" → "and the exact two-sided 95% CI for (ΔM_b − ΔM_a) rules out a δ_min advantage of (b) over (a) (U < 0.05)". No "n.s." survives in the document.
- **F3.** Level-2 CI level pinned: "CIs at Level 2 are 1−α₂ = 99.375% exact two-sided intervals"; Branch S (i)/(ii) now read "lower 99.375% CI (1−α₂) > δ_min = 0.05". *Consequence stated:* at 99.375% the Level-2 MDE is 11.25pp, so the adaptation rule fires at N=80 — Branch S is unreachable at the pre-registered N until N is re-registered larger with its own MDE computation (see F4).
- **F4.** Phantom "stated rule" deleted: "N is increased per the stated rule or the candidate is held" → "the candidate is held (Inconclusive) — no N increase is pre-registered in this protocol; any N increase requires a new pre-registration with its own MDE computation."
- **F5.** Three A3 lower CIs corrected to the stated Tango method (Lead independently recomputed: EXP064 [−0.0132, +0.1370]; EXP066 [+0.0651, +0.2417]; EXP077 official [+0.0338, +0.2015]) and the adjudication updated: EXP066's lower CI clears δ_min — a fourth margin-clearing demonstration. The A3 top-line verdict is unaffected; the error was conservative in direction.
- **F6.** EXP023 caveat gained the ruling's two specifics: "the mechanism was selected among 5 on N=20 dev, and L=8 was inherited from EXP013's grid".
- **F7.** Stale LOG-186 note replaced: "the ruling's record is the research_log.md entry (line 3578); applied exactly as issued."
- **F8.** TTPS primitive check operationalized: each primitive executed standalone on the NTDP task must yield ΔM with U < δ_min (cannot rescue alone); violators removed from the DSL before TTPS runs.
- **F9.** ASR gated explicitly: "C4/ASR may not enter §F culling or §G NTDP runs — and no Box-1/Box-2 verdict for ASR is licensable — until the policy-scope declaration is pre-registered."
- **F10.** DEER provenance tag corrected: "[FACT]/[OBSERVATION, verified in LOG-158 Cluster B audit — not re-verified under LOG-185]".
- **F11.** K1 threshold pinned: both "cos ≈ 1" → "cos ≥ 0.9 (pre-registered)".
- **F12.** Honest alpha-budget wording: hierarchical (not "partitioned") control; "Budget is per-experiment: FWER is controlled within each NTDP run, not across sequential re-tests."

## Could not check / limitations (reviewer's)

1. Whether EXP065's and EXP070 C7's identical (b=10, c=0, N=60) CIs reflect independent data — artifact-level, out of scope; no verdict depends on their independence.
2. The content of a future N-increase rule — it doesn't exist; F4 removes the dangling reference rather than inventing the rule.
3. RISER's full-paper router-training setup — LOG-185 itself flags this as follow-up; the draft carries LOG-185's stated nuance faithfully, which is all the revision can do.
4. The carried-forward LOG-158 base (point 22a) — named above; whether it satisfies the fresh-object rule is a CEO/mentor adjudication, since LOG-184 scoped verification to the seven papers.

**Bottom line (reviewer):** the drafter did the hard work correctly — the statistics are real, the map is honest, the kills are intact. The defects were all in the last mile of formal precision (numbering, one leftover "n.s.," three miscomputed CI lowers, two unpinned parameters, one phantom rule reference). None was structural.

---

*LOG-188 discharged 2026-09-23. Reviewed target: SYNTHESIS_A_J_REV_2026-09-23.md with all 12 fixes applied. No GPU used; no signed protocols or primary artifacts modified.*
