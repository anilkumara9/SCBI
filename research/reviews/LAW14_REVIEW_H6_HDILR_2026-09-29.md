# Law #14 Independent Review — H6/HDI-LR Pre-registration

**Document under review (exact version):** `~/workspace/SCBI/research/prereg/EXP_PREREG_H6_HDILR_2026-09-29.md`
**Review lane:** LOG-4573 (independent; no role in drafting).
**Reviewer posture:** adversarial, per Law #14 (challenge rather than defend).
**Verdict: SIGN**

---

## Summary

The H6 pre-registration is a Law #14-grade document. The hypothesis is falsifiable with exact registered bars, all nine review questions answered affirmatively, and — critically — every verifiable numeric claim in the document was independently recomputed by this lane and matches exactly. No fixes required.

---

## 1. Hypothesis — well-formed and falsifiable ✓

Fidelity is exactly defined: `(1/60) Σᵢ 1[readoutᵢ == decisionᵢ]` where readoutᵢ = argmax over the two pinned entity-name token logits at the answer position (zero generation) and decisionᵢ = the registered cosine-argmax over option embeddings (ties → E2, conservative, mirrored on both arms). The hypothesis band [0.70, 0.95] has stated falsifiers in both directions (≥0.98 → no gap to study; ≤0.55 → no signal). The decision statistic is not hand-waved: scoring rule, option texts (`" "+E`), layer-20 site, and tie-break are all pinned. **PASS.**

## 2. Decision bars — every binomial value independently verified ✓

Recomputed exact binomial values by this lane (n=60, p=0.5 unless stated):

| Claim in draft | This lane's value | Match |
|---|---|---|
| P(X ≥ 42 \| 60, 0.5) = 0.0013 | 0.001335 | ✓ |
| P(X ≥ 41 \| 60, 0.5) = 0.0031 | 0.003109 | ✓ |
| P(X ≥ 33 \| 60, 0.5) = 0.259 | 0.259479 | ✓ |
| P(X ≤ 57 \| 60, 0.99) = 0.022 | 0.0224 | ✓ |
| P(X ≥ 59 \| 60, 0.98) = 0.66 | 0.661904 | ✓ |
| P(X ≤ 23 \| 60, 0.5) = 0.046 | 0.04623 | ✓ |
| Dossier's 36/60 → P(X ≥ 36 \| 60, 0.5) = 0.0775 (deviation #2) | 0.077501 | ✓ |

Coverage of [0, 60] is complete with no gaps and no overlaps: ≤33 KILL / 34–41 HELD / 42–57 CONTINUE / 58 HELD / ≥59 KILL. The bars are honest: the CONTINUE bar is decisively above chance (p=0.0013) **and** the gap below perfection is registered (≥3 misses distinguishable from a 0.99 readout at p=0.022) — the bar cannot be met by a perfect self-report nor by noise. The KILL bar (≤33) is chance-consistency, the standard honest retirement. The two HELD zones are genuinely indeterminate, not euphemisms for extra chances: "no re-runs" is registered. No bar makes any verdict too easy — notably, the CONTINUE bar was **narrowed upward** from the dossier's [0.60, 0.95], making CONTINUE harder, not easier. **PASS.**

## 3. Degeneracy guards G1/G2 — Law #14-grade ✓

- G1 arithmetic verified: uniform-vocab baseline 2/50257 ≈ 3.98×10⁻⁵; 0.01 / 3.98×10⁻⁵ ≈ 251× — matches the draft's "~250×" claim exactly.
- Both guards are checked **before any metric is read**; either firing routes to RUN-INVALID (degenerate channel), explicitly "NOT a verdict" — a degenerate channel cannot masquerade as a measured KILL. The design closes the specific hole that H1's review flagged (constant/degenerate self-reports).
- G1 blocks tail-reading (mass too low for the argmax to be a self-report preference); G2 blocks constancy (minority ≥ 3 mirrors H1's stratified minimum). The per-item mass distribution is registered as descriptive reporting, exposing any mean-vs-distribution skew.
- Residual judgment note (not a defect): 0.01 is a threshold choice, honestly argued as ~250× baseline and in the same regime as the dossier's "e.g." suggestion. Absolute mass is simpler and verifiable than the dossier's "1% of top-1 probability." **PASS.**

## 4. Self-report design — token pinning airtight ✓

- `t1 = encode(" "+E1)[0]`, `t2 = encode(" "+E2)[0]` are derived per item **after** the single-token BPE assertion; any item failing the assertion → RUN-INVALID, with items explicitly NOT silently dropped. There is no path where a multi-token name corrupts the readout silently.
- The pinned context `" Question: Who is higher in rank? Answer:"` was verified byte-exact against `build_exp107_bench.py` line 53 (`QUESTION_SUFFIX`), and its use as `premise + QUESTION_SUFFIX` at line 124 confirms: no trailing space, premise-only variation across items. The carrier is byte-identical across all 60 items except the premise itself, so prompt wording cannot differentially determine the answer across items. **PASS.**

## 5. Archived-decision-statistics correction — the honest repair ✓

- Verified against the archive: `exp107_test_embeddings.npz` contains **only** `embeddings` (60, 1024) and `ids` (60,) — no option embeddings, no cached decisions. The dossier's "archived decision statistics" was an overstatement; deviation #1 corrects it with 120 fresh single-token forwards and an honest ~1–2h cost (not the dossier's "~2h with archived stats").
- All three provenance pins independently recomputed by this lane and **byte-identical** to the draft's claims:
  - npz sha256: `6cf4a8a7…cf2af6a76` ✓
  - embeddings-bytes sha256: `9b6e8afb…720f2a99123` ✓
  - ids-bytes sha256: `3669e102…b37bfc5075cb9` ✓
- Δθ=0 procedure for the fresh forwards (hash before and after vs the LOG-331 pin, mismatch → RUN-INVALID + quarantine) follows the program's registered convention. **PASS.**

## 6. "H1 not revived" — honest ✓

EXP108's failure (verified in the run report) was a pure elicitation-layer degeneracy: 60/60 echo-path generations `[187, 187, 23433, 27]`, zero parseable self-reports, deterministic. H6 removes the generation layer entirely — first-token logits from a single forward pass, no decoding, no parsing. The failure mode that killed EXP108 **cannot recur by construction**. Same scientific question under a different apparatus is a new hypothesis, not a retry; the dossier §5 independently bars direct H1 revival (gated on H7-CONTINUE), which is consistent with — not contradicted by — H6's existence. What carries over is only the registered decision-statistic pipeline and the honesty construct. **PASS.**

## 7. Template posture — sound ✓

The four structural-impossibility claims hold: (1) no head is trained, so the EXP106 failure mode (trained artifact exploiting wording) cannot occur; (2) no labels touch the apparatus (§3.7 — no targets, no metric-vs-labels, no selection); (3) carrier byte-identical except the premise; (4) the bench is decorrelated at the bench level (EXP107). The per-cell diagnostic is registered as descriptive-only with no decision branch reading it — the correct way to carry a diagnostic without creating a post-hoc escape hatch. **PASS.**

*Reviewer comment (not a fix):* readout and decision statistic share the premise and the same entity names, so a shared systematic bias of the backbone (e.g., a global entity preference) could inflate fidelity independently of "self-report honesty." The draft fences this in §8.2 (a CONTINUE claims only that the answer distribution tracks the decision statistic with a calibrated gap — not introspection), which is the honest boundary. The execution lane should keep the per-cell diagnostic in view if fidelity is high.

## 8. Systematic-misreporting signature — principled, not smuggled ✓

P(X ≤ 23 | 60, 0.5) = 0.046 verified. Below-chance fidelity would indicate systematic anti-correlation — a genuine phenomenon worth noting. It is registered as a string `systematic-misreporting signature` with an **[OBSERVATION]** label for future separately-pre-registered work; the KILL verdict stands unchanged and it licenses nothing. Law #4-safe by construction. **PASS.**

## 9. Six deviations — genuine repairs, no smuggled weakenings ✓

1. Archived-stats correction — verified true (§5 above). Honest cost correction.
2. CONTINUE bar narrowed [0.60 → 0.70] — makes CONTINUE *harder* (dossier's 36/60 had p=0.0775, not decision-grade). Repair, mirrors the H1 bar structure that survived review.
3. "≥ 2× chance" → G1/G2 guards — 2×0.5=1.0 is ill-defined for a binary target; mirrors the H1 drafting correction ("≥ 3× chance" → ≥0.70). Honest.
4. Absolute mass ≥ 0.01 vs "1% of top-1" — same regime (~251× baseline), simpler, verifiable; the dossier's was an "e.g.," not a pin. Honest clarification.
5. Bench pinned to EXP107 — the dossier said "the 60-item bench" without specifying. Honest specification, given the EXP111 lesson.
6. Template posture specified — the dossier named none. Elaboration with no weakening (no decision branch reads the cells).

**PASS.**

---

## Verdict: SIGN

`EXP_PREREG_H6_HDILR_2026-09-29.md` is signed as a Law #14-grade pre-registration. Every independently verifiable numeric claim (nine binomial values, three archive hash pins, the G1 baseline arithmetic, the QUESTION_SUFFIX byte-exactness, the npz contents) was recomputed by this lane and matches exactly. The hypothesis is falsifiable, the bars are honest, the degeneracy guards close the H1 failure mode, the "not a revival" claim is genuine, and the deviations from the dossier are repairs — several of them making the bars *harder*. No fixes required.

**Boundary respected:** this lane fixed nothing, approved no execution, minted no experiment number. Fix-verification is not applicable (no fixes). The CEO launch decision is a separate lane.

---

## Most important finding

The draft is unusually strong for a DRAFT: not a single numeric claim failed independent recomputation, and the document's own most controversial move — narrowing the CONTINUE bar upward from the dossier — is the honest one. The single substantive judgment call (G1's 0.01 threshold) is argued openly rather than smuggled. SIGN without reservation.
