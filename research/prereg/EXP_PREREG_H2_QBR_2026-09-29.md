# Pre-registration: H2 — QBR (Quantization-Boundary Robustness)

**Status:** DRAFT pre-registration. Licenses nothing. No model runs, no experiment number minted, no signed protocol touched, no GPU contact, no commits, no pushes. $0 CPU.
**Drafting lane:** LOG-4553 (pre-assigned). **Source:** `research/innovation/SPRINT_2026-09-29_SUMMIT.md` §H2 (worth-it gate passed, ranked #4).
**Launch chain:** independent Law #14 review of this exact file → fix-verification (if fixes required) → CEO launch decision → execution under a minted experiment number. This lane stops at the draft.

**Governing laws:** Law #4 (no post-hoc hypothesis shifts — the bars below are binding), Law #6 (frozen backbone Δθ=0), Law #7 (zero data leakage — no bench labels touch the apparatus beyond the kit's pre-registered use), Law #9 (metrics registered before any output is inspected), Law #13 (deterministic reproducibility — seeds, hashes, environment manifest pinned below).

---

## 1. Hypothesis (one falsifiable sentence)

**[HYPOTHESIS]** The EXP105 falsification-kit battery's binding verdict (KILL at step 9) reproduces under weight-only INT8 fake-quantization of the frozen backbone — i.e., the Decodability Gap boundary is precision-regime-robust at the binding-bar level.

### 1.1 The H2-vs-LOG-4528-condition argument (read this before anything else)

LOG-4528 adopted the steering-under-compression discipline (arXiv:2609.06473) with an explicit **condition**: *"no retro-verification of closed S4/S5/S6/I2′ lines (their zero-flip verdicts are transformation-invariant)."* H2 re-runs the EXP105 battery — the I2′ line's falsification instrument — under a precision transformation. On its face, this looks like the barred thing. The honest case that it is not:

1. **H2 does not touch the S4/S5/S6 static-injection lines.** Those verdicts are literal zero-flip measurements (EXP094: 0/120 flips), where the condition's rationale — transformation-invariance — holds cleanly. They stay closed and untouched.
2. **The I2′/EXP105 verdict is not a zero-flip verdict.** It is a *statistical null*: KILL at step 9 with McNemar T-vs-R p=0.0625, resting on baseline 0.5333, n_pop=21, and measured contrasts dM_T=+0.2381 / dM_F=+0.1429 / dM_R=0. The adopted compression paper shows exactly these kinds of quantities move under quantization (baseline shifts, asymmetric dose-response). The condition's rationale — "verdicts are transformation-invariant" — does not cover a statistical-null verdict whose components the adopted paper proves precision-sensitive.
3. **H2 is not retro-verification of the I2′ verdict.** Retro-verification would ask "was the KILL correct?" H2 asks a *new* question the dossier's worth-it gate licenses: "does the published boundary statement need a precision index?" The draft **fences** this explicitly (§7): H2 cannot overturn, re-open, or re-license the I2′ KILL or any closed line. The KILL stands regardless of H2's outcome.

**[INTERPRETATION]** H2 is therefore *boundary precision-certification under transformation*, not retro-verification. Extending LOG-4528's condition to bar H2 would stretch it beyond its stated rationale.

**Adversarial invitation:** if the independent Law #14 reviewer judges §1.1 a rationalization — i.e., that re-running the I2′ instrument under any transformation *is* the barred retro-verification — the reviewer is asked to **kill H2 outright** rather than repair it. That kill would be recorded as a verdict on the condition's scope, not a defect in this draft.

---

## 2. Exact question and the decision it changes

**Exact question [HYPOTHESIS]:** Do the EXP105 battery's binding verdicts reproduce under INT8 fake-quantization, or does precision open/close a transfer window at the binding-bar level?

**Decision changed:**
- **CERTIFIED** (7/7 tiers, or 6/7 with structure intact — §4): the boundary is precision-certified under weight-only INT8 simulation → the paper may carry an honest, bounded precision-generality statement.
- **PIVOT** (defined below): precision is a new axis → the boundary needs a *precision-indexed* statement, and one follow-up characterization lane is licensed (bounded, §4).
- **KILL** does not appear in H2's outcome set: H2 cannot kill the boundary (a null reproduces) and cannot kill regime-dependence beyond the tested approximation class. The dossier's "bit-identical → KILL regime-dependence" is restated here as CERTIFIED (7/7) — the regime-dependence claim is what dies, not the boundary.

**PIVOT defined precisely:** a pivot to a precision-indexed boundary statement. Concretely: (a) the program's boundary claims (Decodability Gap) are qualified as "measured at FP32; under weight-only INT8 simulation the binding verdict is {same / shifted from step X to step Y}"; (b) exactly one follow-up characterization lane is licensed, restricted to applying the LOG-4528-adopted procedures (matched-geometry collinearity gate, censored iso-effect dose ladder, baseline-shift attribution) to locate which precision effect drove the flip; (c) the follow-up may not re-open I2′, S4, S5, S6, or any closed line, may not claim capability, and may not mint new experiment numbers beyond its own pre-registered scope.

---

## 3. Method

### 3.1 No-generation design constraint (EXP108/EXP109 lesson) [ASSUMPTION]

EXP108 (H1) and EXP109 (H4) both went **RUN-INVALID** on generation degeneracy — base Pythia-410m cannot follow generation instructions (88/88 vote-generations unparseable, repetition attractors). H2 therefore requires **zero generation**: `tier0.py` performs forward passes only (single-token candidate logits, no autoregressive decoding); `battery.py` is pure logit arithmetic with no model contact. This is a hard design constraint: any execution step that required generation would be out of scope, and the run would HALT rather than substitute an elicitation.

### 3.2 Fake-quantization spec [PROPOSITION]

- **What:** weight-only INT8 simulation on a *copy* of the frozen Pythia-410m weights.
- **Exact method:** per-output-channel symmetric INT8 fake-quantization of every `nn.Linear` weight matrix: `scale_c = max|w_c| / 127`; `w_sim = clamp(round(w_c / scale_c), −128, 127) × scale_c`, stored and computed in **float32**. Embeddings, biases, LayerNorm parameters, and all activations stay FP32; no INT8 GEMM kernels are used — all compute is float32. This is the "fake" in fake-quantization: **simulated quantization on float32 compute vs true INT8 kernels** (which would change accumulation order and rounding). Implemented with pinned `torch` only (no new dependency); the transform is deterministic given the weights.
- **What it approximates:** weight-only INT8 inference as studied in arXiv:2609.06473. **What it is not:** true INT8 hardware behavior, activation quantization, or NF4. bitsandbytes `LLM.int8()`-exact is GPU-gated and is named here as the honest ceiling this run does not reach.
- **Backbone Δθ=0 handling (pinned answer):** (a) the FP32 model is verified against the LOG-331 backbone pin `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed` **before** quantization — proving the starting point is the licensed frozen backbone; (b) the fake-quant transform is applied to a disposable in-memory copy; (c) the copy's SHA-256 is recorded in the worksheet (it will differ from the pin — expected, not a violation); (d) `tier0.py`'s internal pre/post-run hash assertion still applies and guards against drift *during* the run; (e) the quantized weights are discarded after the run and never persist into any artifact. Δθ=0 is preserved in the licensed sense: the reference backbone is never modified.

### 3.3 Kit phases and the seven tiers [PROPOSITION]

Execution (a later lane) runs, in order:
1. **Environment sanity:** `bash falsification_kit/reproduce_exp105.sh` — must print `REPRODUCTION EXACT ✔`. If it does not, HALT (environment drift; do not proceed to quantized comparison). The execution worksheet must also record the Law #13 environment manifest: exact torch and transformers versions (reference worksheet pins `torch=2.14.0+cpu`, `transformers=5.17.0`) and the CPU thread count the executor sets and reads back via `torch.get_num_threads()` — compliance verifiable against the reference worksheet's existing `torch`/`transformers` keys by worksheet diff.
2. **Quantized Tier-0:** `tier0.py --model-id EleutherAI/pythia-410m` on the fake-quantized copy (same bench, same seed 20260928, float32 dtype flag). Records per-item candidate logits. The execution worksheet must state the quantized-copy presentation mechanism — in-memory `state_dict` swap after model load, or saved-to-local-directory used as `--model-id` — since tier0.py loads by model-id from cache and §3.2's "disposable in-memory copy" pins the quantization target, not how the copy is presented to the runner.
3. **Quantized battery:** `battery.py` on the quantized Tier-0 records (same seed; F1 empty-population guard active — n_pop=0 → HALT, never a verdict).

**The seven tiers** — seven checkable comparisons of the quantized run against the FP32 reference (reference values from `falsification_kit/reference/`, EXP105):

| # | Tier | Reference (FP32) | "Reproduces" criterion |
|---|------|-------------------|------------------------|
| T1 | Tier-0 verdict | `TIER-0 PASSED` (baseline 0.5333) | Quantized Tier-0 verdict is also `TIER-0 PASSED`. Baseline-shift magnitude is reported separately per the adopted baseline-shift-attribution discipline — a baseline shift alone does not fail T1 unless the verdict category changes. |
| T2 | Battery verdict class | `KILL` | Quantized battery verdict class is also `KILL`. |
| T3 | Battery step | step 9 | Quantized battery step is also 9. |
| T4 | Contrast signs/band | dM_T=+0.2381 > 0, dM_F=+0.1429 > 0, |dM_R| < 0.05 (flat band) | Same sign pattern: dM_T > 0, dM_F > 0, |dM_R| < 0.05. Magnitudes are compared descriptively, not barred. |
| T5 | Primary McNemar non-significance | T-vs-R: b=5, c=0, p=0.0625 ≥ 0.05 | p ≥ 0.05 (the binding bar is still missed). Note: a flip here changes the verdict class, so it is already caught by T2/T3 — T5 is recorded for attribution. |
| T6 | Foil–top-1 overlap gate | O = 0.5714 > 0.5 (gate violated) | O > 0.5 (the apparatus condition — foil arm non-diagnostic — is unchanged). |
| T7 | Population comparability | n_pop = 21, median failed rank 4.0 | n_pop within ±5 of 21 **and** n_pop > 0 (F1 guard). Median failed rank reported descriptively. |

*Deviation from the dossier (recorded):* the dossier's "7 tiers" was loose — it did not name them. The tiers above are this draft's binding specification. The dossier's "within the kit's tolerance" is replaced by the per-tier Boolean criteria above; there is no tolerance parameter left undefined.

**What "reproduce" means:** each tier is a Boolean. "Reproduce" = the Boolean holds. No exact-numeric-match requirement on magnitudes (quantization perturbs logits; demanding bit-identity would test the wrong thing); no statistical-equivalence test beyond the binding bars the kit already carries (McNemar exact, Tango CIs, DELTA_BAR=0.10, flat band |dM|<0.05, O_GATE=0.5 — all pre-registered in `core/scoring.py`).

---

## 4. Decision bars with statistical license

- **7/7 tiers reproduce → CERTIFIED.** Precision-regime-dependence is killed for the tested approximation class (weight-only INT8 simulation, single bench, single model). The boundary may carry a bounded precision-generality statement.
- **6/7 tiers reproduce with T1–T3 (structural tiers) intact → CERTIFIED-WITH-NOTE.** The single flipped tier is documented as a bounded, measured precision effect; verdicts are unchanged. Certification holds.
- **Any structural flip (T1, T2, or T3 changes) OR ≤5/7 tiers reproduce → PIVOT** (defined in §2).

**False-positive risk — addressed honestly.** With n_pop=21, a single item changes any dM by ±1/21 ≈ ±0.048, comparable to the flat band; the decision table is discontinuous near the binding bars (the reference p=0.0625 missed by one flip). A skeptic could call "any flip → PIVOT" trigger-happy. Two answers: (1) the run is fully deterministic (seeded, fixed weights, deterministic fake-quant, CPU float32) — a flip is a deterministic fact about the quantized regime, not a sampling fluke, so the stochastic false-positive class does not apply; the residual risk is bench-idiosyncrasy, which is fenced by the single-bench scope in §7. (2) Per the adopted compression paper, precision *does* amplify small perturbations through nonlinearities — a step flip under fake-quant is itself the phenomenon H2 is testing for, not noise to be explained away. The 6/7 CERTIFIED-WITH-NOTE band exists precisely so that a lone *numeric* (non-structural) flip is documented rather than pivoted.

*Deviation from the dossier (recorded):* the dossier's "any tier flips → PIVOT" is refined — a single non-structural flip (6/7) certifies with a note rather than pivoting. The structural tiers (verdict class, step) retain the dossier's sensitivity: any flip there pivots.

---

## 5. Falsification decision tree

```
reproduce_exp105.sh
 ├─ ≠ EXACT → HALT (environment drift; apparatus finding, licenses nothing)
 └─ = EXACT ✔
     └─ quantized tier0.py + battery.py → 7 tier Booleans (T1..T7)
         ├─ 7/7 true → CERTIFIED (boundary precision-certified under
         │    weight-only INT8 simulation; bounded generality statement licensed)
         ├─ 6/7 true AND T1∧T2∧T3 true → CERTIFIED-WITH-NOTE (flip documented
         │    as bounded precision effect; verdicts unchanged)
         └─ T1 or T2 or T3 false, OR ≤5/7 true → PIVOT
              → precision-indexed boundary statement required
              → one follow-up characterization lane licensed (§2: collinearity
                gate + iso-effect ladder + baseline-shift attribution only)
              → I2′ KILL stands; no closed line re-opens; no capability claimed
```

No other branches exist. No re-runs, no larger populations, no post-hoc bars (Law #4, Law #9).

---

## 6. Cost and honesty

- **$0 CPU, ~2–4h** (one quantized Tier-0 run of 60 forward passes on Pythia-410m CPU + battery + analysis; the FP32 reference is the checked-in worksheet, not a re-run). No GPU contact. No generation (hard constraint, §3.1).
- **Honesty ledger:** (a) fake-quant approximates weight-only INT8; true INT8 kernels and bitsandbytes-exact are out of scope — any "certified" claim is explicitly scoped to the simulation; (b) single bench (60 cloze items), single model (Pythia-410m) — no generality beyond; (c) a CERTIFIED outcome does not strengthen the I2′ KILL; (d) a PIVOT outcome does not license re-running closed lines under quantization.

---

## 7. What H2 does NOT claim

1. Certification under fake-quant ≠ certification under true INT8 hardware (different rounding/accumulation; §3.2).
2. A CERTIFIED outcome does not re-open, strengthen, or re-license the closed I2′/EXP105 verdict — the KILL stands regardless.
3. A PIVOT outcome does not license re-running any closed S4/S5/S6/I2′ line under quantization — only the bounded characterization lane in §2.
4. No claim about trained heads (H3's territory), conditional steering (K2/EXP083/084's territory), or any capability gain.
5. No claim of superhuman cognition, consciousness, or generality beyond the tested bench/model/approximation class.
6. **Novelty: N1 — Known Combination.** Fake-quantization + the published falsification kit is a known combination; no new mechanism is claimed. (Law #10.)

---

## 8. Deviations from the dossier (complete list)

1. "7 tiers" named and bound as T1–T7 with per-tier Boolean criteria (§3.3) — the dossier left them unspecified.
2. "Any tier flips → PIVOT" refined: single non-structural flip (6/7) → CERTIFIED-WITH-NOTE; structural flips or ≤5/7 → PIVOT (§4). Justified by the determinism argument and the compression paper's perturbation-amplification finding.
3. "Bit-identical verdicts → KILL regime-dependence" restated as CERTIFIED (7/7) — the regime-dependence claim is what dies, not the boundary (§2).
4. PIVOT given a precise operational definition (precision-indexed statement + one bounded characterization lane + explicit fences) — the dossier's "precision-indexed boundary" was unelaborated (§2).
5. Fake-quantization spec pinned to per-channel symmetric INT8 on Linear weights, FP32 compute, with the Δθ=0 pin-check-then-derive procedure — the dossier's "round(w/scale)" was underspecified (§3.2).
6. No-generation hard constraint added from the EXP108/EXP109 RUN-INVALID lesson (§3.1).
7. The H2-vs-LOG-4528-condition argument (§1.1) is new — the dossier did not address the condition. The draft invites the reviewer to kill H2 if §1.1 reads as rationalization.

---

## 9. Boundary

Independent Law #14 review of this exact file is a separate lane. No experiment number is minted by this draft. Execution, if ever launched, is a CEO decision under a minted number. This lane stops here.
