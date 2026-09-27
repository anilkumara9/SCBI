# Law #14 Independent Adversarial Review — S4-9 Pre-registration DRAFT

**Reviewer:** Independent Scientific Mentor & Adversarial Reviewer, Law #14 capacity (reports to the founder; verdict binding; not overridable by CEO or Research Lead).
**Target:** `research/innovation/S4-9_PREREG_DRAFT_2026-09-27.md` — DRAFT, UNSIGNED (LOG-4368, commit `0e6a2fb` on `lane/log4368-s4-9-prereg-draft`).
**Licensing chain:** LOG-4352 (EXP093 KILL UPHELD, binding) → LOG-4353 (S4-9 born from death-debt, PAID) → LOG-4365 (Law-#15 worth-it packet, GO) → LOG-4366 (reconciled; draft commissioned) → LOG-4368 (draft delivered). This review is pre-assigned LOG-4369.
**Date:** 2026-09-27. **Compute:** $0, CPU only, paper only. Read-only on all signed protocols/artifacts/weights — no file outside this review lane edited or created except the review report and the LOG-4369 log entry.

---

## Verdict: **SIGN-WITH-FIXES** — four blocking findings (F1–F4), seven advisories (A1–A7)

The draft is faithful to the LOG-4365 packet, carries no invented numbers, passes the Law-#15 gate honestly, guards the right things (Δθ=0, G7-as-disqualification, per-item margin CSV closing the LOG-4352 Law-#13 gap, N_final gate, no pilot authorized, no experiment number minted), and correctly refuses to touch EXP093's signed protocol. It is **not** signed: the §3 decision table — the binding artifact an executor reads — (a) does not totally partition the outcome space and has no evaluation order (same defect class as the K3 review's blocking F1), (b) contradicts §2.3 on delivery-failure routing, (c) routes a reachable outcome (consistent wrong-direction steering) to no row at all; the T-arm constructor — the intervention under test — is unspecified, so the pre-registration is unexecutable as written; the arm-routing "rule" is a placeholder carrying a phantom arm label; and the Underdetermined trigger contains a false-void clause (norm CV) that changes the packet's breaking point. All four blocking findings have mechanical, interpretation-free repairs below. After repair, the draft requires a fresh independent delta re-verification before SIGN. Execution remains conditional on: Law #14 SIGN, then CEO execution clearance. **No pilot is authorized by this review.**

---

## Fidelity audit (all numbers traced to LOG-4352 / LOG-4365 — PASS)

| Draft claim | Source | Status |
|---|---|---|
| EXP093: Δ = 0.0000; McNemar b = c = 0 → p = 1.0 all six tests (P-vs-B, N-vs-B × 3 strata); acc 0.6000/0.9667/0.2333 | LOG-4352 | ✓ |
| perturbation_ratio = 0.0474 (~4.7% of residual norm); margins +0.0059 P / −0.0076 N | LOG-4352 | ✓ |
| DELTA_BAR = 0.10, ALPHA = 0.05 verbatim | LOG-4352 / LOG-4365 | ✓ |
| 3 arms × 60 items ≈ 180–240 passes; hard cap 400; CPU <0.005 T4-h; $0 | LOG-4365 (backlog row) | ✓ |
| Delivery tolerance ±25% → 0.0355–0.0593 (0.0474 × 0.75 = 0.03555; × 1.25 = 0.05925) | recomputed | ✓ |
| Movement gate ≥ 6 flips ≈ Δ̄ = 0.10 at n = 60 | LOG-4365 §4 Gap 3 | ✓ |
| Licensed claim scoped to "≥10pp causal transfer via a shared static direction at layer 11"; per-item reserved as EXP094+ | LOG-4352 | ✓ |
| Death-debt PAID (LOG-4353); not a revival/edit of EXP093's signed protocol (digest `3e0f269b…` intact) | LOG-4352 §4 / LOG-4353 | ✓ |
| No experiment number minted; DRAFT/UNSIGNED accurate; pilot NOT authorized; no signed file modified | draft §7–§8 | ✓ |
| $0 compute for the draft; no weights touched; no GPU contact | draft §4, §7 | ✓ |

No invented numbers found. No silently widened claims found. The "six cells" slip (§3 vs §5) is flagged as A1, not a fidelity failure — the binding instrumentation spec (§5) lists the correct nine cells.

## Law #15 block (PASS, with the decision-table mechanics repaired under F1)

Precise falsifiable question ("does an item-specific task direction move decisions on the same bench where the shared direction moved none?"), decision it changes (two KILL paths, licensed CONTINUE, PIVOT — each named), cheapest falsifying test (3×60 paired, CPU, <0.005 T4-h; no cheaper decision exists for the shared-vs-per-item question), quantitative prediction (ΔM_T > 0.10 AND ΔM_T > ΔM_R with McNemar p < 0.05 on T-vs-R), sharp breaking point (ΔM_T ≤ 0.10 with ΔM_R within noise → KILL; degenerate {d_i} → Underdetermined, never KILL on a powerless test), named belief ("the EXP093 kill was about sharedness, not location"). All present and honest. The "exactly one row will be earned" assertion in §0 is *not* currently true — F1's dead zones break it; the repair restores it.

## Guards (PASS on Δθ=0, margin CSV, instrumentation; constructor and routing incomplete — F2, F3)

- **Δθ=0:** weight hash pre == post, mismatch voids the run (Law #13). Adequate as a pre-registered guarantee. PASS.
- **Per-item margin CSV (Law #13 repair):** draft §4/§5 require per-item, per-arm (B/T/R) margins, top-1 decisions, perturbation_ratio, and margin shifts persisted append-only. This closes the LOG-4352 non-blocking observation exactly. PASS (margin definition citation → A7).
- **Instrumentation spec:** per-item CSV, constructor manifest (code hash, inputs, label-contact attestation, d_i norms + pairwise |cosine| summary), Δθ=0 hashes, environment + seed manifest, delivery probe log, stratum table, decision-table worksheet. Adequate. PASS.
- **N_final feasibility gate:** procedure correctly specified with a HALT_PROBE-style stop; the computation is deferred rather than recorded — A5 verifies it passes on paper.
- **G7 / constructor / routing:** incomplete — F2, F3.

---

## Blocking findings

### F1 — §3 decision table does not totally partition the outcome space; no evaluation order; §2.3 contradicts §3 on delivery routing (location: draft §2.3, §3)

**Defect.** Five sub-defects, all in the binding execution artifact:

(a) **No evaluation order; rows double-fire.** Row 1 (KILL family) and row 2 (KILL specificity) both fire when T≈R≈0 with delivery proven. Rows 5 (HOLD) and 6 (Underdetermined) both fire when delivery fails on a degenerate constructor. The draft lists rows without precedence, so an executor facing either case must invent priority — a Law #9 violation manufactured by the pre-registration itself. (Same defect class as the K3 review's blocking F1.)

(b) **Dead zone 1 — consistent wrong-direction steering.** Row 1's condition is internally contradictory for this case: "ΔM_T ≤ ΔM_shared-baseline (≈ 0 both)" is satisfied by ΔM_T = −0.15, but "T-vs-B movement ≈ 0" is not (9 wrong-way flips is real movement). Row 3 (CONTINUE) requires ΔM_T > +0.10. Row 4 (PIVOT) requires sign-heterogeneity or null T-vs-R specificity — neither holds for sign-consistent, task-specific negative steering (T-vs-R p < 0.05, R ≈ 0). **No row fires.** This outcome is reachable (a mis-signed but causal constructor) and scientifically it refutes the KILL — a causal channel exists — so misrouting it is not a harmless gap. Note the packet's own breaking point ("ΔM_T ≤ 0.10 with ΔM_R within sampling noise of ΔM_T → KILL") does not earn KILL here either, since ΔM_R is not within noise of ΔM_T. The draft must route it somewhere; currently it routes nowhere.

(c) **Dead zone 2 — stratum-inconsistent but T-vs-R-significant positive.** Row 3 requires the stratum table be "present and consistent"; row 4 requires "null T-vs-R specificity". A result with ΔM_T > 0.10, T-vs-R p < 0.05, but the effect concentrated in one stratum only (aggregate-only positive) satisfies neither "consistent" nor "null T-vs-R". **No row fires.** The packet's intent (LOG-4365 §3: "a claim that survives only in aggregate is underlicensed and routes to PIVOT") has no binding row to land on.

(d) **"Consistent" is undefined in the binding table.** The CONTINUE bar hinges on a judgment term with no operational definition — the exact defect class the K3 F1 blocked on ("meaningful"/"clearly rescues"/"NULL" unbound in §3).

(e) **§2.3 contradicts §3 row 5.** §2.3: "Delivery unproven → Underdetermined, never KILL." §3 row 5: "Delivery probe FAILS → Inconclusive/HOLD — procedure invalid; no verdict licensable." Underdetermined and Inconclusive/HOLD are different verdicts with different consequences (question undecidable from this run vs. procedure invalid, rerun required). One condition, two routings.

**Required fix (mechanical).** Insert the following binding evaluation order immediately above the §3 table (first match wins), rewrite the rows in its terms, and delete §2.3's "Delivery unproven → Underdetermined" sentence:

1. **Delivery:** G5-style probe FAILS → **Inconclusive/HOLD** (procedure invalid; no verdict licensable). Single routing for delivery failure.
2. **Degeneracy:** {d_i} degenerate — mean pairwise |cosine| ≥ 0.95 (F4: norm-CV clause removed) — → **Underdetermined** (R4: never KILL on a powerless test).
3. **Movement:** (b+c on T-vs-B) + (b+c on R-vs-B) < 6 → **KILL** (family): inertness is not a sharedness artifact; licensed claim expands to all static L11 task directions. *(Maps to Refuted.)*
4. **Specificity:** T-vs-R McNemar p ≥ 0.05 with overlapping Tango CIs → **KILL** (specificity): nonspecific perturbation; no causal license for per-item task geometry. *(Maps to Refuted.)*
5. **Licensed positive:** ΔM_T > 0.10 AND T-vs-R p < 0.05 AND stratum-consistent — defined as ΔM_T > 0 in **all three** strata (strict; a zero or negative stratum fails consistency) — → **CONTINUE**, bench-scoped to EXP092-B. *(Maps to Supported.)*
6. **Otherwise → PIVOT** *(maps to Not supported for the global claim)*, with named sub-cases: (a) sign-heterogeneous movement across items/strata; (b) consistent wrong-direction steering (ΔM_T < −0.10 with T-vs-R p < 0.05) — causal channel exists, sign story is EXP095 material; (c) T-vs-R significant but stratum-inconsistent (e.g., aggregate-only positive) — underlicensed per LOG-4365 §3, conditional design is EXP095 material.

This order codifies existing draft intent (step 3 before step 4 matches §2.3's movement gate: specificity is interpreted only after movement clears; step 2 before step 3 honors the R4 rule in §0's breaking point), partitions the space totally with no overlap, closes both dead zones, and makes §0's "exactly one row will be earned" true.

### F2 — The T-arm constructor is unspecified: the intervention under test is undefined (location: draft §2.1, §4, §6 item 1)

**Defect.** The draft pre-registers bars, guards, statistics, and verdicts for an intervention — "per-item task direction d_i" — whose construction is given only as "built from within-item task geometry at L11" / "e.g. a within-item task contrast at L11" (packet LOG-4365 §1). No algorithm, no input tensors, no contrast operation, no normalization, no norm-matching formula. An executor cannot build the T arm from this draft; any two executors would build different d_i. That is the maximal Law #9 hazard: executor discretion over the entire test arm. The draft itself concedes the point ("Constructor contract (to be stress-tested by Law #14 before any SIGN)"; §6 item 1; "the run does not start without it"), which means the draft *as written* is not a signable pre-registration — SIGN would license an unexecutable document.

**Required fix (mechanical in form; the science belongs to the repair lane).** The signed version must contain a frozen constructor specification with: (i) exact input tensors and token spans; (ii) the within-item contrast operation stated as an algorithm; (iii) normalization and the per-item norm-matching formula (target 0.0474 of residual norm); (iv) the G7 label-free audit procedure from §6-answer-1 below, executed against the frozen constructor hash *before* any run, with the attestation persisted in the constructor manifest (§5 item 2). A label-informed constructor is a disqualification (run voided), never a positive. The repair lane writes the constructor; the delta re-verification checks it is frozen, complete, and G7-audited — the reviewer does not design the constructor here.

### F3 — The arm-routing "rule" is a placeholder carrying a phantom arm label (location: draft §3, §6 item 2)

**Defect.** §3 states the routing rule "is registered before the run; its exact wording is a Law-#14 stress target" — i.e., the pre-registration defers part of the registration to after SIGN. A pre-registration that does not contain its allocation rule is not complete. Compounding it, the draft (and the packet LOG-4365 §2/§3, and the backlog S4-9 row) carry the stale label **"N-vs-B routing"** inherited from EXP093's arm names — but S4-9's arms are B/T/R; no N arm exists. The draft's parenthetical ("the per-item test arm plays the role EXP093's N arm played") translates it once, but the binding rule still names a phantom arm. An executor searching the design for the "N arm" finds nothing — ambiguity in the primary-contrast definition.

**Required fix (mechanical).** Replace the placeholder with the explicit rule the design already implies (paired within-item McNemar, §2.3 — there is no between-items allocation to specify):

> **Arm-routing rule (binding):** every one of the 60 EXP092-B bench items receives all three arms (B, T, R); all contrasts (T-vs-B, R-vs-B, T-vs-R) are within-item paired; no item is excluded from any contrast; stratum membership (aggregate / A-first / C-first) is the EXP092-B bench pin, fixed before inspection. There is no between-items allocation and no post-hoc re-routing — re-routing is structurally impossible under full pairing.

And rename "N-vs-B routing" → "T-vs-B routing" everywhere in the signed draft (the backlog row's "N" is the per-item test arm; the label does not survive into S4-9's B/T/R design). No packet edit is needed (the packet is worth-it analysis, not the binding artifact), but the signed pre-registration must not name the phantom arm.

### F4 — The Underdetermined trigger's norm-CV clause is unsound and changes the packet's breaking point (location: draft §3 row 6, §4; answers §6 item 3)

**Defect.** The draft registers "{d_i} degenerate: mean pairwise |cosine| ≥ 0.95 OR per-item norm coefficient of variation < 0.05 → Underdetermined", with a drafting note claiming this split is "without changing the packet's breaking point." The claim is false, and the second disjunct is scientifically wrong:

- The packet's breaking point (LOG-4365 §4) is *collinearity*: "If per-item norm variance across items is degenerate **(all d_i ≈ collinear)**" — the parenthetical shows the packet meant directional degeneracy. The draft's OR **adds** a new void condition the packet never licensed.
- Norm uniformity does not make the test powerless. The per-item question is about *directional* content; norms are deliberately matched to the EXP093 perturbation ratio per item. A family with diverse directions and uniform norms is the *ideal* matched case — full power. Routing it to Underdetermined voids informative runs. (If the clause was meant as a constructor-bug detector, it is miscategorized: a broken constructor is a procedure problem → Inconclusive/HOLD, not a verdict about the world. The G5 delivery probe already guards the true degenerate case, all-zero d_i, via the perturbation_ratio band.)

**Required fix (mechanical).** Single check: **mean pairwise |cosine| ≥ 0.95 → Underdetermined**. Delete the "OR per-item norm coefficient of variation < 0.05" clause from §3 row 6 and §4. This restores the packet's breaking point exactly (collinearity = powerless per-item test = the shared-direction case already killed → R4 Underdetermined).

---

## Non-blocking advisories

- **A1.** §3 says "six cells as in EXP093" for the stratum table; §5's instrumentation spec correctly lists aggregate / A-first / C-first × (T-vs-B, R-vs-B, T-vs-R) = **nine** cells. "Six" is a stale carryover from EXP093's two contrasts. Fix: six → nine in §3 (the §5 spec already governs).
- **A2.** Verdict-count inconsistency: §0 says "all four outcomes pre-registered" (the Law-#15 four: KILL / KILL-spec / CONTINUE / PIVOT), §3 lists six rows, and the "five permitted verdicts (Supported / Not supported / Inconclusive / Underdetermined / Refuted)" are never mapped to rows (same gap as the K3 review's A1). Fix: enumerate the mapping in the signed version — KILL rows → Refuted; CONTINUE → Supported; PIVOT → Not supported (global claim; conditional follow-up is EXP095 material); HOLD → Inconclusive; Underdetermined → Underdetermined.
- **A3.** ΔM is never explicitly defined; §2.3's "McNemar exact on paired decisions (T-vs-B, R-vs-B, T-vs-R), per item relative to baseline decisions" muddles the T-vs-R contrast (the trailing clause suggests all three are vs baseline). Fix: define ΔM_T = (1/n)Σ[correct_T(i) − correct_B(i)] (paired accuracy difference, EXP093's Δ convention), and state that the T-vs-R McNemar pairs T(i) vs R(i) decisions directly.
- **A4.** The G5-style delivery probe is per-item (tolerance band ±25%) but the probe→verdict aggregation is unregistered: how many items must sit inside the band for probe PASS vs FAIL? Fix: pre-register the aggregation rule (e.g., PASS iff ≥ 58/60 items within band with margin shift recorded; else FAIL → HOLD). Without it, row 5's trigger is executor judgment.
- **A5.** The N_final feasibility gate (§4) is specified as a procedure but the computation is deferred. It passes on paper — record it: McNemar-exact significance at any n requires ≥ 6 unidirectional discordant pairs (b=6, c=0 → p = 2/64 = 0.03125 < 0.05; b=5, c=0 → p = 0.0625, n.s.), which is exactly the registered ≥6-flip movement gate; unlike EXP079's split-limited probe there is no structural cap (max achievable ΔM = 1.0 ≥ DELTA_BAR = 0.10). Recording this closes the EXP079 lesson inside the pre-registration instead of deferring it.
- **A6.** R arm underspecified: state explicitly "R item-i norm = T item-i norm" and the random-direction sampling distribution (e.g., isotropic Gaussian in the 512-dim residual space, normalized; seed in the manifest). One line each.
- **A7.** The per-item margin CSV (§5 item 1) should cite EXP093's margin convention by reference so "margin" is not redefined at execution time.

---

## Answers to the draft's three §6 open items

**1. G7 label-free audit procedure (proposed; the run must not start without it).**
G7.1 — **Freeze:** constructor code + config + dependency pins hashed (SHA-256) and committed before any run; the audit applies to that hash, and the manifest (§5 item 2) records it.
G7.2 — **Input attestation:** an independent lane (no authorship of the constructor) enumerates every input the constructor reads. Allowed: the item's own input-token activations at L11 (prompt/question tokens only). Forbidden: item labels, answer keys, target tokens, correct-option indices, any other item's data, any aggregate computed with label knowledge. The audit first documents *where EXP092-B's label lives* so the auditor can verify the constructor cannot reach it.
G7.3 — **Label-swap invariance test (the auditable disqualification bar):** run the frozen constructor on the bench with labels randomly permuted (equivalently, replaced with constants); the produced {d_i} must be identical to the production run (bit-for-bit, or max abs diff ≤ 1e-9). Any label path fails this test mechanically — no judgment involved.
G7.4 — **Cross-item isolation:** verify d_i uses only item i's data (no leakage from other items' labels or answers).
G7.5 — **Verdict:** PASS → attestation + hashes persisted in the constructor manifest. FAIL (any label contact) → **DISQUALIFICATION**: not a negative result; the run is voided; only a fresh constructor with a fresh audit may proceed.

**2. T-vs-B routing-rule wording (stress test).** Verdict: the current wording is not a rule — it is a deferred promise ("is registered before the run") wrapped around a phantom arm label ("N-vs-B"). The stress test it fails is the simplest one: *quote the rule an executor would follow.* There is none to quote. The repair is F3 above: full within-item pairing stated explicitly (which makes post-hoc re-routing structurally impossible), and the N label retired. With that wording, open item 2 is closed — there is no residual degree of freedom to stress.

**3. Norm-vs-collinearity split (confirmation requested).** Not confirmed — **rejected** (F4). The split's direction (separating the two concepts the packet conflated) is right; the OR is wrong. Norm CV < 0.05 must not trigger Underdetermined: it does not indicate a powerless test, it adds a void condition the packet never licensed (contradicting the drafting note's "without changing the packet's breaking point"), and the genuine degenerate-norm case (all-zero d_i) is already caught by the G5 delivery probe. Keep the collinearity check only.

---

## Release conditions (unchanged by this review)

This SIGN-WITH-FIXES does not sign anything, authorize any run or pilot, mint an experiment number, book compute, or commission the repair lane (repair is a separate lane). After F1–F4 are repaired (A1–A7 at the repair lane's discretion, A4/A5 recommended), the draft requires a fresh independent delta re-verification before SIGN. Execution remains conditional on: Law #14 SIGN → CEO execution clearance. The EXP093 KILL is untouched by every row of the repaired table. No signed artifact was modified by this review; no weights were touched; no runs were performed.

---

*Review completed 2026-09-27. Binding verdict: **SIGN-WITH-FIXES** (F1–F4 blocking; A1–A7 advisory). Report: `research/innovation/REVIEWS/S4-9_PREREG_LAW14_REVIEW_2026-09-27.md`.*
