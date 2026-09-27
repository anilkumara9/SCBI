# Law #14 Delta Re-verification — S4-9 Pre-registration Repair (LOG-4370 → LOG-4371)

**Reviewer:** Independent Scientific Mentor & Adversarial Reviewer, Law #14 capacity (reports to the founder; verdict binding; not overridable by CEO or Research Lead). Independent of the LOG-4370 repair lane.
**Target:** `research/innovation/S4-9_PREREG_DRAFT_2026-09-27.md` — DRAFT, UNSIGNED — repaired draft at commit `c6acf96` (`lane/log4370-s4-9-prereg-repair`), diffed against the original draft at `0e6a2fb` (`lane/log4368-s4-9-prereg-draft`).
**Binding review under verification:** LOG-4369 (`bbaf46f`, `lane/log4369-s4-9-prereg-review`): SIGN-WITH-FIXES, four blocking findings F1–F4, seven advisories A1–A7.
**Scope:** DELTA-ONLY. The full LOG-4369 review is not re-litigated. Verified: (1) each repair implements its required fix; (2) advisories A1–A7 applied; (3) every diff hunk traces to a finding, advisory, or logged judgment call — no untraced change; (4) no new defects introduced; (5) nothing signed that should not be.
**Date:** 2026-09-27. **Compute:** $0, CPU only, paper only. Read-only on all signed protocols/artifacts/weights — the only writes are this report and the LOG-4371 log entry, on a worktree of `lane/log4371-s4-9-prereg-reverify` (from `main` @ `bfe3a80`); the shared working tree and `main` were not disturbed.

---

## Verdict: **SIGN** (binding)

All four blocking repairs verified implemented as the review required (F1–F4: PASS each). All seven advisories verified applied (A1–A7: PASS each). The repair lane's four logged judgment calls are each sound and licensed (no scope creep, no new finding). The draft remains DRAFT/UNSIGNED, no experiment number minted, pilot NOT authorized. The S4-9 pre-registration is ready for CEO licensing. Execution remains conditional on: CEO execution clearance (CPU, <0.005 T4-h). Three non-blocking observations are recorded below; none blocks SIGN.

---

## F1 — Decision table: binding 6-step evaluation order (PASS)

Verified against the review's required fix, line by line:

| Required | Repaired draft | Status |
|---|---|---|
| Binding evaluation order above the table, first match wins | §3: "**Binding evaluation order (first match wins — F1 repair).** The executor evaluates the steps in this exact order; exactly one step is earned" | ✓ |
| 1. Delivery probe FAILS → Inconclusive/HOLD, single routing | Step 1: "G5-style probe FAILS (§4 aggregation rule) → **Inconclusive/HOLD** — procedure invalid; no verdict licensable. Single routing for delivery failure." | ✓ |
| 2. Mean pairwise \|cosine\| ≥ 0.95 (norm-CV removed) → Underdetermined | Step 2 verbatim, maps to Underdetermined | ✓ |
| 3. (b+c T-vs-B) + (b+c R-vs-B) < 6 → KILL (family) → Refuted | Step 3 verbatim, maps to Refuted | ✓ |
| 4. T-vs-R p ≥ 0.05 with overlapping Tango CIs → KILL (specificity) → Refuted | Step 4 verbatim, maps to Refuted | ✓ |
| 5. ΔM_T > 0.10 AND T-vs-R p < 0.05 AND stratum-consistent (ΔM_T > 0 in all three strata, strict) → CONTINUE → Supported, bench-scoped | Step 5 verbatim + strict definition; maps to Supported | ✓ |
| 6. Otherwise → PIVOT → Not supported (global claim), with named sub-cases (a) sign-heterogeneous, (b) consistent wrong-direction steering ΔM_T < −0.10 with T-vs-R p < 0.05 (never KILL), (c) stratum-inconsistent positive (underlicensed) | Step 6 verbatim with all three sub-cases; maps to Not supported | ✓ |
| Delete §2.3's "Delivery unproven → Underdetermined" | Sentence deleted; §2.3 now routes delivery FAIL to Inconclusive/HOLD per §3 step 1 — "a procedure problem; never KILL and never Underdetermined" | ✓ |
| "Consistent" operationally defined | Step 5: "defined as ΔM_T > 0 in **all three** strata (aggregate, A-first, C-first; strict — a zero or negative stratum fails consistency)" | ✓ |

**Hand-verified total partition** (both review dead zones + both original double-fire cases traced through the order):
- Dead zone 1 — consistent wrong-direction steering (ΔM_T = −0.15, T-vs-R p < 0.05): probe PASS → step 1 no; not degenerate → step 2 no; flips ≥ 6 → step 3 no; p < 0.05 → step 4 no; ΔM_T > 0.10 fails → step 5 no; step 6 sub-case (b), **never KILL**. CLOSED.
- Dead zone 2 — ΔM_T > 0.10, T-vs-R p < 0.05, stratum-inconsistent: steps 1–4 pass through; step 5's strict consistency fails; step 6 sub-case (c), **underlicensed, never CONTINUE**. CLOSED.
- Double-fire case A (T≈R≈0, delivery proven): step 3 fires first; step 4 never reached — single verdict. RESOLVED.
- Double-fire case B (delivery fail + degenerate constructor): step 1 fires first — single routing. RESOLVED.
- Step 6 is a total catch-all ("Otherwise → PIVOT"), so exactly one step is earned in every outcome. §0's "exactly one row will be earned" is now true.

## F2 — Frozen constructor spec C-1 (§2.1.1) (PASS)

Verified against the review's required (i)–(iv):
- (i) Inputs + token spans: item's input-token IDs as in the B-arm pass, byte-identical tokenization; readout-anchor = last prompt token; the same position read at L11 and injected at. Explicit NOT-read list (labels, answer keys, target tokens, correct-option indices, other items' data, label-knowledge aggregates). ✓
- (ii) Contrast algorithm: Pass A (task framing, B-arm pass) → a_i; Pass B (same text under fixed label-free neutral prefix P₀) → b_i; r_i = a_i − b_i; exact-zero r_i flagged in manifest, caught downstream by the G5 band. ✓
- (iii) Normalization + norm matching: u_i = r_i/‖r_i‖₂; d_i = u_i × (0.0474 × ‖h_i^B‖₂) — perturbation_ratio = 0.0474 exactly per item (EXP093-licensed norm, LOG-4352); injection at the readout-anchor position, before the next block. ✓
- (iv) G7.1–G7.5 audit embedded (§2.1.3), executed against the frozen hash before any run; attestation persisted in the constructor manifest (§5 item 2); FAIL → **DISQUALIFICATION** (run voided, not a negative result; only a fresh constructor + fresh audit may proceed). Genuine disqualification bar. ✓

**Freeze stress test** (the re-verification question): could two implementers build different constructors? The algorithm, inputs, spans, normalization, norm formula, and injection position are fully pinned. The one free parameter — the literal P₀ string — is pinned pre-run by the G7.1 freeze (constructor code + config + P₀ + dependency pins, SHA-256, committed before any run) and constrained by the G7.3 label-swap invariance test; any post-freeze P₀ change is a new hash = a new manifest, not a silent substitution. The spec is frozen modulo a named, hashed, pre-run-bound artifact — that is the review's own freeze mechanism, and the repair extends it correctly to P₀. PASS.

## F3 — Full-within-item-pairing rule; phantom "N" retired (PASS)

- The binding rule in §3 matches the review's required text **verbatim** (checked character-for-character against the review's quoted block): all 60 items receive B, T, R; all contrasts within-item paired; no exclusions; stratum pin fixed pre-inspection; re-routing structurally impossible. The placeholder and the deferred "registered before the run" language are gone. ✓
- "N-vs-B routing" renamed out of S4-9's binding rules. Remaining "N" mentions are all explicitly marked historical: §0's P/N arms are EXP093's own historical arms; §3's parenthetical states the backlog row's "N-vs-B" referred to the per-item test arm, that S4-9's arms are B/T/R, and that "the N label does not appear anywhere in this design's binding rules". No executor searching for an "N arm" can be misled. ✓

## F4 — Norm-CV clause deleted; collinearity-only gate (PASS)

- "OR per-item norm coefficient of variation < 0.05" deleted from §3 step 2 and §4; the false drafting note ("without changing the packet's breaking point") deleted. Grep confirms no live norm-CV trigger remains — the only two mentions are (a) a repair annotation "(F4: norm-CV clause removed)" inside step 2 and (b) §6 item 3's historical record of the rejection, neither a gate. ✓
- Single check stands: mean pairwise |cosine| ≥ 0.95 → Underdetermined (§3 step 2, §4 degeneracy gate). The packet's breaking point (collinearity) is restored exactly. Norm uniformity is correctly documented as *intended* by the C-1 construction; the all-zero-d_i case is caught by the G5 per-item band (0 sits outside 0.0355–0.0593). ✓

## A1–A7 — all applied (PASS each)

- **A1:** "six cells" → **nine** (§3 step 5: "aggregate / A-first / C-first × (T-vs-B, R-vs-B, T-vs-R) = **nine** cells"; §5 item 5 already listed nine). ✓
- **A2:** all six steps carry "(Maps to: …)" parentheticals — Inconclusive / Underdetermined / Refuted / Refuted / Supported / Not supported (global claim); plus the reconciliation paragraph mapping §0's four Law-#15 outcomes to steps 3–6 and steps 1–2 to procedure/power guards. ✓
- **A3:** ΔM_T = (1/n)Σ[correct_T(i) − correct_B(i)] defined in §2.3 with correct_X(i) as top-1 correctness; T-vs-R clarified as T(i)-vs-R(i) direct pairing, not vs baseline. ✓
- **A4:** aggregation rule pre-registered — "PASS iff ≥ 58/60 items sit within the band with margin shift recorded; otherwise probe FAIL → Inconclusive/HOLD" — adopted verbatim from the review's supplied example (§4 and §5 item 4). ✓
- **A5:** N_final computation recorded on paper — b=6, c=0 → p = 2/64 = 0.03125 < 0.05; b=5, c=0 → p = 0.0625, n.s. (arithmetic matches the review); max ΔM = 1.0 ≥ DELTA_BAR = 0.10, no structural cap; EXP079 lesson closed inside the pre-registration. ✓
- **A6:** R arm — "‖g_i‖₂ = ‖d_i‖₂" norm tie; isotropic Gaussian in the 512-dim L11 residual space, normalized then scaled; seed pinned in the manifest. ✓
- **A7:** margin convention cited by reference — EXP093's logit-margin m(h) = logit(target) − logit(foil), `experiments/protocols/EXP093_L11_CAUSAL_PREREG_SIGNED.md` §3 — not redefined at execution time (§5 item 1; §4 guard points to it). The cited path exists on `main`. ✓

## No scope creep — repair lane's judgment calls (all sound, licensed; no new finding)

1. **C-1 constructor science** (algorithm, neutral-prefix reference design, norm-matching formula): new design by the repair lane, explicitly licensed by the review's "the science belongs to the repair lane". Audited above: the task-framing-vs-neutral-prefix contrast reads only input-token activations under two presentations; label-swap invariance holds mechanically (G7.3); the EXP093 norm is reused, not re-derived; the R-arm specificity control prices out constructor cleverness. Sound.
2. **§6 closures**: items 1–2 recorded CLOSED with the review's resolutions embedded (G7.1–G7.5 in §2.1.3; binding pairing rule in §3); item 3 recorded REJECTED per F4, faithfully restating the review's reasoning. Accurate record-keeping, not new science.
3. **§7/§8 updates**: review-has-happened (LOG-4369) recorded; next steps = independent delta re-verification → SIGN → CEO clearance; pilot NOT authorized until all three complete. The new §7 honesty bullet ("the only new numbers are the review-supplied A4 example and recomputed McNemar-exact values") is accurate — verified: 58/60 adopted verbatim from the review; 0.03125/0.0625 match the review's arithmetic; no other numbers invented.
4. **Header licensing chain** extended LOG-4369 → LOG-4370: factual.

**Diff-traceability sweep:** every hunk in the 0e6a2fb→c6acf96 diff traces to F1–F4, A1–A7, or one of the four logged judgment calls above. No untraced change found.

## Nothing signed that shouldn't be (PASS)

- Title and header: DRAFT (UNSIGNED); "NOT a protocol. NOT executable. NOT reviewed. No experiment number minted". §7: does not sign, does not authorize a run, does not mint an experiment number, does not alter signed artifacts. §8: pilot NOT authorized until delta re-verification + SIGN + CEO clearance. Footer: "(still DRAFT, UNSIGNED — repair does not sign)". ✓ No signature line, no experiment number, no pilot authorization anywhere.

---

## Non-blocking observations (do not affect SIGN)

1. **Review-report citation path / merge ordering.** The draft's §8 cites `research/innovation/REVIEWS/S4-9_PREREG_LAW14_REVIEW_2026-09-27.md`. That file exists on `lane/log4369-s4-9-prereg-review` but the repair branch (`c6acf96`) was cut from the draft tip and does not contain it, so the citation is not yet repo-true at a single commit. Both branches must land on `main` (review branch first or together) before the path resolves. Merge-process note for the CEO; not a repair defect.
2. **Step 6(a) example wording.** Sub-case (a) reads "sign-heterogeneous movement across items/strata with null T-vs-R specificity" — the null-specificity qualifier makes the example overlap step 4's condition, which fires earlier. Harmless: the binding content is the "Otherwise → PIVOT" catch-all, and the sub-cases are illustrative, not rows. No routing changes; left as-is to avoid churn on a signed-path document.
3. **Step-2 repair annotation.** "(F4: norm-CV clause removed)" is audit-trail language inside the binding artifact. Consistent with program precedent (K3 LOG-4362); transparent, not a defect.

---

## Release conditions

This SIGN signs the **pre-registration only**. It does not authorize a run or pilot, does not mint an experiment number, does not book compute, and does not commission any execution lane. Execution remains conditional on: **CEO execution clearance** (CPU, <0.005 T4-h, $0). The EXP093 KILL is untouched by every step of the table. No signed protocol, artifact, or weights were read-modified by this re-verification; the review lane wrote only this report and the LOG-4371 log entry.

---

*Re-verification completed 2026-09-27 by the Independent Scientific Mentor & Adversarial Reviewer (Law #14, reports to the founder). Binding verdict: **SIGN**. Report: `research/innovation/REVIEWS/S4-9_PREREG_LAW14_REVERIFY_2026-09-27.md`. $0 compute, CPU only, paper only.*
