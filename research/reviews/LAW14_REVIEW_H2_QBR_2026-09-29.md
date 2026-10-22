# Law #14 Independent Review — H2 (QBR) Pre-registration

**Review lane:** LOG-4554 (pre-assigned). **Date:** 2026-09-29.
**Artifact under exact-version review:** `research/prereg/EXP_PREREG_H2_QBR_2026-09-29.md`
**Drafting lane:** LOG-4553 (separate agent — independence holds; this reviewer did not write the draft).
**Scope:** pre-registration only. This review approves no execution, mints no experiment number, launches nothing.
**Method:** read-only verification against `falsification_kit/` sources, the reference worksheets, `research/innovation/SPRINT_2026-09-29_SUMMIT.md` §H2, and LOG-4528/LOG-4527/LOG-4553 in `reports/research_log.md`. No model runs, no weights touched, $0 CPU.

---

## Verdict: SIGN-WITH-FIXES

**On the exact filename** `EXP_PREREG_H2_QBR_2026-09-29.md`: **SIGN-WITH-FIXES.** Two verifiable fixes required (§F below). No killing defect found — including on the license question, which was tested adversarially first (§1).

---

## 1. The license question (tested first, per brief)

The drafter's §1.1 argues H2 is licensed, not barred, by LOG-4528's condition *"no retro-verification of closed S4/S5/S6/I2′ lines (their zero-flip verdicts are transformation-invariant)"* — and explicitly invites the reviewer to kill H2 outright if §1.1 reads as rationalization. The invitation was taken seriously. Findings:

**(a) The condition's stated rationale is factually inapplicable to I2′/EXP105.** LOG-4528's parenthetical justifies the bar as *"their zero-flip verdicts are transformation-invariant."* EXP105's verdict is not a zero-flip verdict. Verified against `falsification_kit/reference/battery_worksheet.json`: dM_T = +0.2381, dM_F = +0.1429, McNemar T-vs-R b=5, c=0, p=0.0625, KILL at step 9 via `ev9 = (dM_T > 0) and (p_TR >= ALPHA)`. These are measured nonzero contrasts and a statistical null (p=0.0625), not a 0/120-flip measurement like EXP094's. The condition's rationale therefore does not cover EXP105 on its own terms — the drafter identified a genuine defect in the condition's scope, not a loophole to exploit.

**(b) The adopted paper proves the rationale's premise false for exactly these quantities.** arXiv:2609.06473 (the paper LOG-4528 adopts) shows baseline shifts and asymmetric dose-response under quantization — i.e., the *components* of a statistical-null verdict (baseline, contrast magnitudes, p-values near bars) are precision-sensitive. Extending a "transformation-invariant" bar to a verdict whose components the adopted paper proves precision-sensitive would contradict the adoption.

**(c) H2 cannot operationally re-open the KILL.** Retro-verification means re-asking "was the KILL correct?" H2's decision table contains no branch that overturns, weakens, or re-licenses the I2′ KILL — the KILL stands under CERTIFIED, CERTIFIED-WITH-NOTE, and PIVOT alike (Law #4: bars locked, no post-hoc shifts). The question is genuinely new: "does the published boundary statement need a precision index?" — precision-indexing a boundary is not re-litigating it.

**(d) The PIVOT follow-up is fenced, not a back door.** The single contingent characterization lane is restricted to the LOG-4528-adopted procedures (collinearity gate, iso-effect ladder, baseline-shift attribution) and explicitly "may not re-open I2′, S4, S5, S6, or any closed line." Characterization of the precision effect ≠ re-running the verdict.

**Conclusion on license:** H2 is *boundary precision-certification under transformation*, a new question the dossier's worth-it gate licenses. The kill invitation is declined. This is recorded as a scope ruling on the LOG-4528 condition: the condition bars re-running zero-flip lines under transformation; it does not bar precision-indexing a statistical-null verdict whose components are documented precision-sensitive. The S4/S5/S6 zero-flip lines remain closed and untouched — H2 runs only the EXP105 battery.

---

## 2. Tiers T1–T7 verified against the actual battery

Every reference value in §3.3 was checked against `falsification_kit/reference/tier0_worksheet.json` and `battery_worksheet.json`:

| Tier | Draft claims (FP32 ref) | Verified |
|------|------------------------|----------|
| T1 | TIER-0 PASSED, baseline 0.5333 | `route: TIER-0 PASSED`, `baseline_accuracy: 0.53333` ✓ |
| T2 | KILL | `decision.verdict: KILL` ✓ |
| T3 | step 9 | `decision.step: 9` ✓ |
| T4 | dM_T=+0.2381>0, dM_F=+0.1429>0, \|dM_R\|<0.05 | `dM_primary_tier0pop: {T: 0.2381, F: 0.1429, R: 0.0}` ✓ |
| T5 | T-vs-R b=5, c=0, p=0.0625 ≥ 0.05 | `contrasts["T-vs-R"]: {b:5, c:0, p:0.0625}` ✓ |
| T6 | O=0.5714 > 0.5 | `overlap_O: 0.571428` ✓ |
| T7 | n_pop=21, median failed rank 4.0 | `n_pop: 21`, `median_correct_rank_failed: 4.0` ✓ |

"Reproduce" is a per-tier Boolean with exact criteria — no undefined tolerance parameter (the dossier's "within the kit's tolerance" is properly replaced; recorded as deviation 1). The T5 attribution note ("a flip here changes the verdict class, caught by T2/T3") was verified against `core/scoring.py::battery_decision`: `ev9 = (dM_T > 0) and (p_TR >= ALPHA)` is the only KILL-9 path, so p_TR < 0.05 necessarily kills step 9 (falls through to ev7→CONTINUE/7 or a PIVOT step). Claim is correct.

Minor: T7's `n_pop > 0` clause is redundant with the F1 HALT guard (n_pop=0 halts before tiers evaluate) — harmless, not a defect.

---

## 3. Fake-quant spec: honest approximation, not vacuous

Per-output-channel symmetric INT8 on Linear weights, FP32 storage/compute, embeddings/biases/LayerNorm/activations FP32, no INT8 kernels. The draft states plainly what it is not (true INT8 hardware, activation quant, NF4) and names bitsandbytes `LLM.int8()`-exact as the GPU-gated honest ceiling. The gap is fenced three times (§4, §6(a), §7.1): CERTIFIED is scoped to the simulation. This is not vacuous: the adopted paper's core finding is that nonlinearities amplify quantization perturbations — a weight-grid rounding perturbation under FP32 compute directly probes that mechanism at the binding-bar level. The claim "certified under weight-only INT8 simulation" means something; the claim "certified under INT8" would not be made. Overclaim guard adequate.

---

## 4. Structural vs non-structural tiers: principled

T1–T3 are the binding decision-table outputs (the verdicts the paper would print); T4–T7 are diagnostic evidence components. A flip in T4–T7 with verdicts intact is a measured precision effect, not a regime change — CERTIFIED-WITH-NOTE documents rather than pivots. The distinction tracks what the paper is licensed to claim, not convenience. "Any structural flip → PIVOT" sensitivity is defended, not assumed: (1) the determinism argument (below) removes the stochastic false-positive class; (2) the adopted paper's perturbation-amplification finding makes a step flip under fake-quant the phenomenon under test, not noise. The draft honestly flags the discontinuity near binding bars (p=0.0625 one flip away) and the 6/7 note band absorbs exactly that case. Sound.

---

## 5. Determinism argument: sound

Seeded run (R_SEED=20260928, verified in `core/scoring.py`), fixed weights, deterministic fake-quant transform, CPU float32. A flip is a deterministic fact about the quantized regime, not a sampling fluke — the stochastic false-positive class genuinely does not apply. Residual risk is bench-idiosyncrasy, fenced by the single-bench scope (§7). Sound. (Fix F1 below tightens the environment side of Law #13.)

---

## 6. Δθ=0 posture under fake-quant: coherent

Verify-against-LOG-331-pin *before* quantization (proves the starting point is the licensed frozen backbone) → transform a disposable in-memory copy → record the copy's SHA (differs from pin: expected, not a violation) → `tier0.py`'s internal pre/post hash assertion guards drift *during* the run → discard the copy. The reference backbone is never modified; Law #6 holds in the licensed sense. No hole in the logic chain.

---

## 7. Zero-generation constraint: verified

`grep` over `falsification_kit/tier0.py`: zero calls to `.generate(` — forward passes only (single-token candidate logits). `battery.py` docstring: "pure logit operator… NO model contact is needed or performed." The EXP108/EXP109 RUN-INVALID lesson is correctly internalized as a hard constraint with a HALT (not substitute) clause. ✓

---

## 8. "CERTIFIED" does not overclaim

Scoping appears in the decision bar itself ("for the tested approximation class"), the honesty ledger (§6a), and the non-claims (§7.1): "Certification under fake-quant ≠ certification under true INT8 hardware." A casual reader could still misread the bare word, but the draft fences the scope at every point where the word is used to license a statement. Adequate; no fix required.

---

## 9. PIVOT is operationally defined, not a euphemism

§2 specifies (a) the exact statement template ("measured at FP32; under weight-only INT8 simulation the binding verdict is {same / shifted from step X to step Y}"), (b) exactly one follow-up lane restricted to the three LOG-4528-adopted procedures, (c) hard fences (no closed line re-opens, no capability, no new experiment numbers beyond its scope). This is a real operational definition. ✓

---

## F. Required fixes (each verifiable)

**F1 — Pin the Law #13 environment side.** The header invokes Law #13 (environment manifest pinned), but §3 never names it; `tier0.py` sets `torch.manual_seed` yet pins no thread count or deterministic flags, and CPU float32 matmul determinism across thread counts is not guaranteed. *Fix:* add one sentence requiring the execution worksheet to record torch/transformers versions and `torch.get_num_threads()` (the checked-in reference worksheet already carries `torch`/`transformers` keys, so compliance is verifiable by worksheet diff). Non-structural; execution-lane detail.

**F2 — Pin the quantized-copy presentation mechanism.** §3.3 step 2 says tier0.py runs "on the fake-quantized copy" via `--model-id`, but tier0.py loads by model-id from cache — the draft never states whether the quantized weights are held in-memory (state_dict swap post-load) or saved to a local directory used as `--model-id`. This affects reproducibility and the interpretation of the Δθ=0 guard. *Fix:* add one sentence requiring the execution worksheet to state the presentation mechanism (in-memory copy vs on-disk directory). Verifiable against the worksheet's existing `script_sha256`/`delta_theta0` fields.

Neither fix alters the hypothesis, tiers, bars, or fences.

---

## Boundary

Review lane stops here. No execution authorized, no experiment number minted, no follow-up dispatched. Fix-verification, if commissioned, is a separate lane against this exact review file.
