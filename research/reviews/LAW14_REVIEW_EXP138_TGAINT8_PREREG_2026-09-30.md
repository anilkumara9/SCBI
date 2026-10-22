# Law #14 Independent Review: B5/TGA-INT8 Pre-registration Draft

**Artifact under review (exact filename):** `research/prereg/EXP138_PREREG_TGAINT8_2026-09-30.md`
**Review lane:** LOG-4861 (pre-assigned, independent of the LOG-4860 drafting lane).
**Date:** 2026-09-30. **$0 CPU, paper only. No repairs, no execution.**

## Verdict: SIGN-WITH-FIXES

**On the exact filename** `EXP138_PREREG_TGAINT8_2026-09-30.md`: **SIGN-WITH-FIXES.** One verifiable fix required (§F1 below). Two non-blocking advisories (§A1–A2). No killing defect found — including on the LOG-4528-condition license question, which was tested adversarially first (§1).

---

## 1. The license question (tested first, per the draft's adversarial invitation)

The draft's §1.1 argues B5 is boundary precision-certification, not barred retro-verification under LOG-4528's condition ("no retro-verification of closed S4/S5/S6/I2′ lines"). I tested this adversarially:

- **The condition's text** (LOG-4528): "no retro-verification of closed S4/S5/S6/I2′ lines (their zero-flip verdicts are transformation-invariant)." The TGA line is not named. The condition was written 2026-09-29; the TGA line closed 2026-09-30 (EXP131 binding KILL LOG-4832, EXP133 binding KILL LOG-4818). The draft's chronology claim is correct.
- **The rationale test:** the condition's rationale is transformation-invariance of *zero-flip verdicts*. EXP131's KILL rests on a measurement (ĉ = 0.03742 via exact-autograd VJP) *and* a causal null (ΔM_v1 = 0) — not a literal zero-flip verdict of the S4/S5/S6 kind. The adopted paper (arXiv:2609.06473) documents that causal structure and baseline decisions *do* shift under quantization while geometry survives. The rationale does not cleanly cover the TGA nulls.
- **The precedent test:** H2/EXP110 was the I2′ analogue. Its Law #14 review (LOG-4554/4556) explicitly declined the kill invitation: "H2 licensed as boundary precision-certification, not barred retro-verification." EXP110 executed to CERTIFIED-WITH-NOTE (LOG-4558). B5 is the TGA analogue of that licensed precedent, with the same §1.1 structure and the same adversarial kill invitation.
- **The fencing test:** B5 cannot overturn, re-open, or re-license the EXP131/EXP133 KILLs or any closed line (§7.2–7.3). The KILLs stand regardless of outcome. This is not retro-verification in the verdict-threatening sense.

**Ruling:** §1.1 is not a rationalization. B5 is licensed as boundary precision-certification. I decline the kill invitation. The condition's scope is not stretched.

---

## 2. Tier review (Q1–Q6)

| Tier | Verdict | Basis |
|------|---------|-------|
| Q1 (ĉ_q < 0.1) | **PASS** | Binding bar matches EXP131 (0.03742 < 0.1). VJP through the quantized graph is well-defined: the `round()` in fake-quant applies to the weight-derivation step (constants during the forward pass); the VJP is w.r.t. the activation x_{20,last}, so autograd is standard. The draft's "the VJP is well-defined" is correct — this subtle point is handled. Exclusion rule (‖g_i‖ < 1e-12 → exclude; ≥3 → apparatus-void) carried over from EXP131. |
| Q2 (ΔM_v1,q = 0) | **PASS** | 11-arm protocol (v̂₁, v̂₂, 8 randoms, B_agg) × 10 prompts = 110 arm-pairs, matching EXP131's structure. Quantized-regime baseline is the correct comparator (see §4). |
| Q3 (ΔM_geo,q = 0) | **PASS** | Geodesic protocol with norm budget B = 0.50578119 — verified against EXP133's console log ("budget pin OK: recomputed B matches 0.50578119 within 1e-4 rel"). |
| Q4 (p_q ≥ 0.05) | **PASS** | One-sided McNemar, v̂₁ vs quantized base. Correct direction for a null-confirmation bar. Partially entailed by Q2 in the all-zero case (b=c=0 → p=1.0) but has independent bite in partial-flip scenarios; same "recorded for attribution" role as H2's T5. Not vacuous. |
| Q5 (B_agg → RUN-INVALID) | **PASS** | Apparatus guard correctly fenced to RUN-INVALID, not PIVOT. A dead-control flip means the quantized bench drifted, not that precision opened a window. |
| Q6 ((h) → RUN-INVALID) | **PASS** | Delivery re-verified under quantization on *both* arms (one-shot and geodesic). The blind-tap lesson correctly applied to the new regime. r_q ∈ [0.99, 1.01]. |

**Missing tier?** None. EXP110's population-comparability tier (T7) has no analogue here — B5's population is fixed by design (10 prompts), not filtered like the battery's n_pop. The ĉ exclusion rule (≥3 exclusions → apparatus-void) covers the degenerate case.

**No vacuous tier.** Every tier is checkable and can fail meaningfully.

---

## 3. Decision table

- **CERTIFIED ⟺ Q1∧Q2∧Q3∧Q4:** correct. All four are the binding nulls; all must reproduce.
- **PIVOT ⟺ any Q1–Q4 fail:** correct. The PIVOT definition (§2) is as precise as H2's licensed precedent: (a) precision-indexed boundary statement, (b) exactly one follow-up characterization lane restricted to the three LOG-4528-adopted procedures (collinearity gate, iso-effect ladder, baseline-shift attribution), (c) explicit fences (no re-opening closed lines, no capability, no new numbers beyond scope).
- **RUN-INVALID ⟺ Q5/Q6 fail:** correct precedence. The falsification tree (§5) checks apparatus guards before verdict bars. An apparatus failure in the new regime cannot masquerade as a precision finding.
- **No CERTIFIED-WITH-NOTE band:** H2 had one (6/7 with structure intact). B5 does not. This is correct, not a gap — B5's four decision tiers are *all* structural (they are the binding nulls themselves). A note band would be incoherent here. The draft's §4 records the deviation from the dossier honestly.

**PIVOT licensing scope — verified adequate:** "one bounded characterization lane" is operationally defined (the three procedures, the fences). A separate pre-reg would be drafted at dispatch time per program convention; the license boundary is clear.

---

## 4. The baseline judgment (quantized-regime baseline for all ΔM)

**Ruling: correct scoping, not a defect.**

The question B5 asks is whether precision *opens a transfer window* — i.e., whether injection moves decisions in the quantized regime that it did not move at FP32. ΔM_q measured against the quantized baseline is the correct quantity for this question. Measuring against the FP32 baseline would conflate two distinct phenomena (quantization's own baseline shift vs. injection's causal effect).

The draft requires baseline shifts to be reported separately per the adopted baseline-shift-attribution discipline (§3.3 step 5, §4). This mirrors EXP110's T1 handling ("a baseline shift alone does not fail T1 unless the verdict category changes"), which was SIGNed. The scoping is consistent with the licensed precedent.

See advisory A1 for the paper-statement implication.

---

## 5. EXP110 pattern application

Verified against `research/prereg/EXP_PREREG_H2_QBR_2026-09-29.md` §3.2 and the EXP110 execution report:

| Element | EXP110 | B5 draft | Match |
|---------|--------|----------|-------|
| Quant formula | per-channel symmetric INT8, scale_c = max\|w_c\|/127, clamp(round(w_c/scale_c),−128,127)×scale_c | Identical, verbatim | ✓ |
| Scope | every nn.Linear weight | every nn.Linear weight | ✓ |
| Exclusions | embeddings, biases, LayerNorm, activations FP32; no INT8 GEMM | Identical | ✓ |
| Δθ=0 (a) | FP32 pin check before quantization (LOG-331 pin) | Identical pin cited | ✓ |
| Δθ=0 (b–e) | disposable copy, copy SHA recorded, pre/post hash assertion, discard after | Identical (a)–(e) | ✓ |
| Honest ceiling | bitsandbytes LLM.int8()-exact GPU-gated, named as unreached | Identical | ✓ |

**The v₁ re-pin (§3.3 step 3):** `exp127_vectors.npz` SHA-256 `9b527c026d0ee307192725429f655e628f403505343dc018de3cfe15db6113dc` verified against EXP127's worksheet and console log; `v1__<prompt_id>` id format verified against EXP131's runner. The *same-direction-new-regime* scoping is correct — re-deriving v̂₁ under quantization would be a different experiment; the "direction changed" question is properly assigned to the PIVOT follow-up's collinearity gate.

**Deviation (correct):** EXP110's step 1 (reproduce_exp105.sh sanity) is replaced by the FP32 pin check — the appropriate analogue since B5 doesn't use the falsification kit.

---

## 6. Breaking points (a)–(h)

All eight are well-formed with correct trip conditions. (d)'s 1e-6 relative tolerance matches §3.3 step 5. (f) correctly requires (h) on both arms. No over-strict trip. No missing trip in the apparatus class.

**One gap → F1 below** (random-direction provenance, a Law #13 reproducibility gap rather than a trip-condition gap).

---

## 7. Worth-it gate and non-resurrection

**Worth-it gate (7 points):** all hold. Exact question ✓, decision changed (CERTIFIED vs PIVOT, precisely defined) ✓, cheapest test ($0 CPU ~2–4h; the question is inherently regime-specific) ✓, mathematical license (arXiv:2609.06473 [OBSERVATION] + EXP110's certified methodology; quantitative prediction ĉ_q < 0.1, ΔM = 0) ✓, breaking point (any flip → PIVOT) ✓, non-resurrection audit ✓, summit filter (honest boundary infrastructure) ✓.

**Non-resurrection (Law #4):** sound. Full-log staleness re-diff (LOG-4860) found no TGA-under-quantization execution. Differentiated from the gate-killed true-INT8/bitsandbytes-exact (GPU-gated; B5 is the CPU-feasible pattern). The LOG-4528 condition is addressed head-on with the adversarial kill invitation (declined, §1 above).

---

## F. Required fix

**F1 — Pin the 8 matched-norm randoms' provenance (Law #13).** §3.3 step 5 says "re-run EXP131's 11-arm protocol (v̂₁, v̂₂, 8 matched-norm randoms, B_agg dead control)" but does not specify whether the 8 randoms are (a) re-used verbatim from EXP131's records or (b) freshly drawn. If (a), cite the EXP131 record hashes. If (b), pin the RNG seeds and stream. As written, the execution lane cannot reproduce the random set deterministically. One sentence fixes it.

---

## A. Advisories (non-blocking)

**A1 — Baseline-shift magnitude in the CERTIFIED paper statement.** The baseline judgment (§4 above) is correct, but consider: a large quantized-baseline shift (e.g., 4/10 prompts flip at α=0) with ΔM_q = 0 would still CERTIFY. The licensed paper statement ("TGA boundary precision-certified") should then explicitly carry the baseline-shift magnitude (e.g., "X/10 baseline decisions shifted under fake-quant; injection nulls reproduce against the quantized baseline") so the generality claim is not misleading. The draft already requires separate reporting; this advisory asks that the reporting be *bound into* the CERTIFIED statement template.

**A2 — Quantized-copy presentation mechanism.** EXP110's pre-reg (§3.3 step 2) required the execution worksheet to state the presentation mechanism (in-memory state_dict swap vs saved-to-local-directory as model-id). B5's draft is silent. Advisory: require the execution worksheet to record it (Law #13). B5's runner is bespoke (not tier0.py), so this is documentation rather than a design gap.

---

## Boundary

Review only. No edits to the draft, no execution, no number minted. The F1 fix needs a repair lane + byte-check against this review; A1–A2 are at the repair lane's discretion. Upon F1's application, the pre-registration is launch-ready pending the CEO launch decision.
