# Independent Law #14 Review — H8/POE Pre-registration

**Artifact under exact-version review:** `EXP_PREREG_H8_POE_2026-09-29.md`
**Review lane:** LOG-4589 (pre-assigned), independent of the LOG-4588 drafting lane.
**Verdict: SIGN** — no fixes required.

**Scope:** This review tests the pre-registration document only. It licenses nothing, approves no execution, mints no experiment number. Fix-verification, CEO launch decision, and execution are separate later lanes.

---

## 1. Hypothesis (review point 1)

**[FACT]** The hypothesis is well-formed and falsifiable: "Averaging entity-name logits over K=5 randomized option-presentation orders improves the frozen backbone's decision accuracy on the 60-item EXP107 template-decorrelated bench above the single canonical-order baseline by a decision-grade margin — paired exact McNemar one-sided p ≤ 0.05."

The decision is defined exactly: `pred_ens_i = argmax_e mean_{k=1..5} logit_e(prompt(i, o_ik))` vs `pred_base_i = argmax_e logit_e(prompt(i, 0))`, paired on the same 60 items, accuracy against the registered bench labels (y=1 iff A-first). The falsifiers in §1 map onto the §4 decision bars without contradiction (checked §1 against §4 line by line — unlike the H7 draft, there is no wording/tree mismatch here). **PASS.**

## 2. Decision bars and McNemar math (review point 2)

**[FACT]** All McNemar values independently recomputed (exact binomial, verified in Python):

| (b, c) | one-sided p | registered outcome |
|---|---|---|
| (5, 0) | 0.03125 | CONTINUE (canonical minimum) |
| (4, 0) | 0.0625 | HELD (correctly not CONTINUE) |
| (3, 0) | 0.125 | — (dossier's "+3/60 → p≤0.05" is wrong; drafter's correction valid) |
| (2, 0) | 0.25 | — |
| (1, 0) | 0.5 | — |

The CONTINUE bar (p ≤ 0.05, one-sided, α=0.05 canonical) is honestly decision-grade at n=60: the test is conditional on the discordant count, so the bar adapts correctly (e.g., (10,5) → p≈0.151 → HELD, not a false CONTINUE). The draft's §4 honesty disclosure — "smaller true effects (≈2–4pp) land in HELD by design" — is accurate. **PASS.**

## 3. KILL bar and the degenerate table (review point 3)

**[INTERPRETATION]** Pinning b=c=0 → KILL (net = 0) is principled. The b=c=0 table means ensemble and baseline produce byte-identical predictions on all 60 items — ensembling observably adds nothing on this bench. This is not an uninformative table: the baseline sits at ~53% (Tier-0), far from ceiling, so a full-agreement table is a genuine null result, not a ceiling artifact. The KILL fence (§7.3) correctly retires only the positional-order-ensembling axis for this task class. **PASS.**

## 4. K=5 i.i.d. scheme with 2 permutations (review point 4)

**[FACT]** P(all-5-same composition) = 2×(1/2)⁵ = 0.0625 ≈ 6% — the draft's "~6%" is exact.

**[INTERPRETATION]** Keeping the dossier's i.i.d. design rather than redesigning is the honest choice, for two reasons. First, the scheme is unbiased for the 50/50 order average (E[#canonical] = E[#swapped] = 2.5 per item); a degenerate 5–0 item simply receives no ensembling benefit, which is the variance-reduction logic working honestly, not a defect. Second, any balanced redesign (e.g., forced 3–2 compositions) would *reduce* estimator variance and make CONTINUE *easier* — keeping i.i.d. is the conservative, non-self-serving option. The per-item 5-bit patterns are logged in the worksheet, so compositions are auditable. **No redesign required. PASS.**

## 5. Single-order baseline (review point 5)

**[FACT]** The baseline is pinned as the bench's stored tuple order (o = 0, §3.2, §3.8), with the bench JSON itself pin-checked (SHA-256 `e91b302f…4f5`, the H6/EXP112-registered pin) before any forward pass. The execution lane has zero freedom to cherry-pick a weak baseline order. **PASS.**

## 6. Template posture (review point 6)

**[INTERPRETATION]** Sound on both grounds the draft claims. (1) The EXP107 bench is template-decorrelated by construction (a pure template detector scores ≈30/60, verified EXP107). (2) The apparatus introduces no new wording: the option-list insertion is byte-identical across items except the permuted entity order — the experimental variable itself. On the residual concern (does permuting entity order interact with the position label y=1-iff-A-first?): the label is determined by *premise phrasing*, which is byte-identical across all K+1 prompts per item; the option-list order is orthogonal to the label by construction, and the ensemble averages over both orders, cancelling any first-option bias rather than exploiting it. The §6(a) honesty fence — "detects option-list positional bias cancellation, not premise-position bias" — states exactly this boundary. **PASS.**

## 7. EXP109 construct-validity lesson (review point 7)

**[FACT]** The readout is argmax over the two pinned entity-name token ids `t1_i = encode(" "+E1_i)[0]`, `t2_i = encode(" "+E2_i)[0]` — the H6 readout contract. No letters appear anywhere in the option list (unlabeled list), so no letter-mapping definition is required and EXP109's undefined-mapping defect cannot recur. The single-token BPE assertion (failure → RUN-INVALID, items never silently dropped) is airtight and mirrors the H6 gate that survived review. The QUESTION_SUFFIX byte-exact pin was verified against `build_exp107_bench.py:53` — matches. **PASS.**

## 8. Tie-break E2 (review point 8)

**[INTERPRETATION]** Pinning exact float-equality ties → E2 (tuple[1]), mirroring H6, is principled: the identical rule applies to both arms (§3.5), so it cannot bias the paired comparison. Exact float equality of two distinct logits is measure-zero in float32 inference absent quantization — ties are not expected to occur at all; the pin exists to close a definitional gap, not to decide cases. **PASS.**

## 9. The 9 deviations (review point 9)

**[FACT]** Each deviation verified against the dossier's H8 section (`SPRINT_2026-09-29_SUMMIT_ROUND2.md`):

1. **600 → 360 forwards:** genuine repair. The dossier double-counted — one forward yields full-vocabulary logits, so both entity logits are read from a single pass. 300 ensemble + 60 baseline = 360 is correct.
2. **"+3/60 → p≤0.05" correction:** genuine repair. (3,0) → p = 0.125, verified above. The dossier's claim is mathematically wrong.
3. **HELD zone added:** genuine repair. Splits the dossier's lumped "p>0.05 → KILL" into underpowered (HELD) vs negative (KILL); mirrors the H5/H6/H7 held-zone structure.
4. **Degenerate table pinned (b=c=0 → KILL):** genuine repair. The dossier left the undefined-test case unaddressed; the pin is the principled choice (see §3 of this review).
5. **Tie-break pinned:** genuine repair — closes a definitional gap.
6. **Baseline pinned as canonical tuple order:** genuine repair — the dossier's "single canonical order" was unspecified.
7. **Order-generation scheme pinned:** genuine repair — the dossier's "K random orders" had no scheme or seed.
8. **Prompt construction pinned byte-exactly:** genuine repair — the dossier did not specify option presentation.
9. **Entity-name readout, no letters:** genuine repair — applies the EXP109 construct-validity lesson the dossier omitted.

**[INTERPRETATION]** All nine are genuine repairs; none is a smuggled weakening. Notably, deviations 3, 4, and 7 make the test *harder* or more honest, not easier. **PASS.**

## 10. Residual checks

- **§1/§4 consistency:** hypothesis falsifiers map onto the decision tree exactly; no wording contradiction. **PASS.**
- **Decision tree completeness:** bench-pin HALT, backbone-pin RUN-INVALID, BPE-assertion RUN-INVALID, and the three verdict branches are all present; "No other branches exist" is properly scoped to post-precondition branches. **PASS.**
- **Law #7:** labels touch only the final accuracy computation; order bits drawn from a pinned RNG independent of labels; K, seed, prompt format, decision rule all pinned with no post-inspection tuning freedom. **PASS.**
- **Law #13:** backbone pin before/after (LOG-331 canonical method), environment manifest recorded, per-item order patterns logged, all 360 prompts byte-reconstructible. Matches the H2 F1 standard. **PASS.**
- **Law #6 (Δθ=0):** 360 read-only inference forwards; backbone never modified. **PASS.**
- **Cost honesty:** 360 forwards, ~2–4h $0 CPU. The dossier's "~2h" was attached to a miscounted 600; the draft's corrected estimate is honest. **PASS.**
- **Overclaim fences (§7):** present and adequate — ensembling gain is variance reduction, not reasoning; CONTINUE licenses a component, not a capability; KILL retires only this axis. Novelty N1. **PASS.**
- **Artifact ground truth:** the npz hash re-verified against the H6-reviewed pin (`6cf4a8a7…af6a76`) — exact match. The bench pin is the H6/EXP112-registered `e91b302f…4f5`, asserted at execution with HALT on mismatch. **PASS.**

## Verdict

**SIGN** on the exact filename `EXP_PREREG_H8_POE_2026-09-29.md`. No fixes required.

The draft is unusually well-pinned: every statistical claim recomputed exactly, every degree of freedom the dossier left open closed by a genuine repair, and the two most tempting self-serving moves (redesigning the order scheme to balanced, lumping the underpowered zone into KILL) both declined in favor of the harder, more honest option. The single most adversarial finding available — the ~6% degenerate compositions — is honestly logged and unbiased by construction.

**Boundary:** review only. No draft edits, no execution approval, no experiment number minted, no follow-ups dispatched. Fix-verification (not required — no fixes), the CEO launch decision, and execution are separate later lanes.
