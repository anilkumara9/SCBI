# Independent Verdict Review: EXP138 (B5/TGA-INT8 — Precision Certification of the TGA Injection Nulls)

**Experiment:** EXP138, minted at the CEO launch decision (LOG-4864).
**Pre-registration (signed):** `research/prereg/EXP138_PREREG_TGAINT8_2026-09-30.md` — Law #14 SIGN-WITH-FIXES (LOG-4861), all fixes applied (LOG-4862), fix-verification PASS with no amendments (LOG-4863). Provenance check: the SHA-256 pinned in the run records (`60b1dbc7f…fddb37`) matches the signed repaired draft byte-for-byte — the execution lane ran exactly the reviewed protocol.
**Review lane:** LOG-4865 (pre-assigned, independent of the LOG-4860 drafting, LOG-4862 repair, and LOG-4864 execution lanes).
**Date:** 2026-09-30. **$0 CPU, paper only. No verdict on any closed line is re-opened by this review.**

## Verdict: CERTIFIED

**The TGA injection nulls reproduce under weight-only INT8 fake-quantization of the frozen backbone. All four decision tiers reproduce; both apparatus guards hold; no breaking-point trip.**

---

## 1. Independent re-derivation of the tier Booleans

Every Boolean below was recomputed from the raw per-item records in `experiments/runs/EXP138_tgaint8/out/exp138_records.json`, not from the execution lane's claimed Booleans.

| Tier | Bar (pre-reg) | Recomputed | Source of truth |
|------|---------------|------------|-----------------|
| Q1 | ĉ_q < 0.1 | ĉ_q = 0.03747118 (mean of 10 per-prompt VJPs; values 0.0108–0.0664); 0 exclusions (< 3) → **PASS** | per-prompt array, exact match to report |
| Q2 | ΔM_v1,q = 0 over 110 arm-pairs | 0 flips across all 11 arms × 10 prompts; v̂₁ = 0, B_agg = 0 → **PASS** | per-item `dm` maps |
| Q3 | ΔM_geo,q = 0 | 0 flips on geo_v1 and geo_bagg arms, all 10 items → **PASS** | per-item geodesic `dm` maps |
| Q4 | one-sided McNemar p_q ≥ 0.05 | b = 0, c = 0 → p = 1.000000 exactly (recomputed binomial) → **PASS** | Q2's zero flips entail it; independent bite reserved for partial-flip scenarios |
| Q5 | ΔM_Bagg,q = 0 (guard) | 0 → **PASS**; no RUN-INVALID | one-shot bagg arm |
| Q6 | (h) r_q ∈ [0.99, 1.01] both arms (guard) | r = 1.0000001 on both arms → **PASS**; no RUN-INVALID | `r_probes` |

**Baseline shifts (separate attribution, §4):** 0/10 quantized α=0 decisions differ from FP32 (arrays `fp32_base_decisions` vs `quantized_base_decisions` compared element-wise). The licensed paper-statement template (§4) is filled with X = 0.

**Decision-table application:** Q1 ∧ Q2 ∧ Q3 ∧ Q4 all reproduce → **CERTIFIED** per §4. No PIVOT branch (no Q1–Q4 fail). No RUN-INVALID branch (Q5/Q6 hold).

---

## 2. Breaking-point audit (a)–(h)

- **(a) Δθ=0:** FP32 backbone hash pre = post = `ec276abe…4ec38e0ed`, matching the LOG-331 pin. Held.
- **(b) v₁ re-pin:** `exp127_vectors.npz` hash `9b527c02…f581f` matches the pre-reg. Held.
- **(c) No finite differences:** runner reuses EXP131/EXP133 code verbatim; ĉ via exact-autograd VJP; no FD term anywhere in the injection pipeline (same as the FP32 certifications). Held.
- **(d) Norm-budget matching:** one-shot — zero violations of the 1e-6 relative tolerance across all 100 non-base arms against the run's budget B_q = 0.5044928550720215. Geodesic — between-arms `sum_dlt` matching is bit-identical (worst relative diff 1.54e-15) on all 10 items. Held for the verdict-relevant property (see §4 note on the absolute reference).
- **(e) B_agg null-control:** Q5, 0 flips. Held.
- **(f) Delivery verified:** Q6, both arms in range. Held.
- **(g) No training/weight mutation:** pure forwards; quantized copy discarded post-run. Held.
- **(h) Quantized-copy integrity:** pre = post = `ed919d47…cab9c33`; additionally byte-identical to EXP110's independently produced quantized manifest (implementation-exact reproduction of the certified pattern). Held.

**No breaking-point trip. No trip was missed by the execution lane.**

---

## 3. Scope and fences (§7) — confirmed honored

1. Fake-quant ≠ true INT8 hardware — the review records this as the honest ceiling; the records note FP32 compute throughout.
2. The EXP131/EXP133 binding KILLs are not re-opened, strengthened, or re-licensed — they stand regardless of this CERTIFIED outcome.
3. No PIVOT licensed, so the bounded characterization lane in §2 is not activated.
4. No capability claim; no training; no closed line re-run.
5. Novelty remains N1 — Known Combination, as pre-registered.
6. Presentation mechanism recorded per A2: in-memory `state_dict` transform (no saved model dir).

---

## 4. Adversarial notes (disclosed, non-blocking)

- **(d) absolute-reference tension:** the geodesic per-item `sum_dlt` values cluster at ~1.55e-6 relative below the pre-reg's quoted target B = 0.50578119. This is *not* a breaking-point trip: (d)'s stated purpose is between-arm comparability ("the verdict would measure the budget, not the regime"), which holds to machine epsilon, and the target value itself was pinned at EXP133 only "within 1e-4 rel" (per the Law #14 review §2) — an 8-digit rounded reference cannot carry a 1e-6 absolute tolerance. The deviation is ~7.8e-7 absolute against margins at the 1e-3 scale; it cannot flip any decision. Recorded as a specification tension for future pre-regs (state which property the tolerance binds to), not a defect in this run.
- **(c) dependence on verbatim reuse:** the "no finite differences" claim rests on the runner reusing EXP131/EXP133 code verbatim. The per-prompt ĉ values (0.0108–0.0664, tight cluster matching FP32's 0.03742) are consistent with exact-autograd VJP through the quantized graph; an FD leak would show up as ĉ-scale distortion, and ĉ_q = 0.03747 ≈ FP32 0.03742 is the opposite signature.
- **Records provenance:** fresh SHA-256 of `exp138_records.json` (`58182baa…044c735c`) matches the report's `records_pin`; the `.sha256` sidecar was not independently checked beyond this — the two-agree basis (fresh hash + report pin) is sufficient under Law #13.

---

## 5. Binding statement

Per the pre-registered decision bars and the A1-licensed paper-statement template:

*"The TGA injection nulls (EXP131 ĉ < 0.1, ΔM_v1 = 0; EXP133 ΔM_geo = 0) reproduce under weight-only INT8 fake-quantization; 0/10 quantized-baseline decisions shifted vs FP32 at α = 0, and the injection nulls reproduce against the quantized baseline."*

**Interpretation:** precision-regime-dependence is killed for the TGA nulls under the tested approximation class (weight-only INT8 simulation, Pythia-410m, single model). The TGA boundary may carry this bounded precision-generality statement. It does not generalize to true INT8 hardware, activation quantization, other models, or any capability claim.

**This verdict is binding.** No PIVOT follow-up is licensed. The TGA precision-certification chapter is closed with CERTIFIED.
