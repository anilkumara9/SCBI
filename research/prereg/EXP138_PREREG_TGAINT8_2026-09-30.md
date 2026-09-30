# Pre-registration: B5 — TGA-INT8 (Precision Certification of the TGA Injection Nulls)

**Status:** DRAFT pre-registration. Licenses nothing. No model runs, no experiment number minted, no signed protocol touched, no GPU contact, no commits, no pushes. $0 CPU.
**Drafting lane:** LOG-4860 (pre-assigned). **Source:** `research/innovation/SPRINT_2026-09-30_POST_TGA.md` §B5 (worth-it gate passed, ranked #5 — boundary infrastructure).
**Experiment number:** EXP138 provisional, minted only at the CEO launch decision.
**Launch chain:** independent Law #14 review of this exact file → fix-verification (if fixes required) → CEO launch decision → execution under the minted number. This lane stops at the draft.

**Governing laws:** Law #4 (no post-hoc hypothesis shifts — the bars below are binding), Law #6 (frozen backbone Δθ=0), Law #7 (zero data leakage — no bench labels touch the apparatus beyond the pre-registered use), Law #9 (metrics registered before any output is inspected), Law #13 (deterministic reproducibility — seeds, hashes, environment manifest pinned below).

---

## 1. Hypothesis (one falsifiable sentence)

**[HYPOTHESIS]** The TGA injection nulls — EXP131's one-shot v̂₁ null (ĉ = 0.03742 < 0.1, ΔM_v1 = 0 over 110 arm-pairs) and EXP133's geodesic-multistep null (ΔM_geo = 0, ĉ_geo = 0.0374) — reproduce under weight-only INT8 fake-quantization of the frozen backbone: the TGA boundary is precision-regime-robust at the binding-bar level.

### 1.1 The B5-vs-LOG-4528-condition argument (read this before anything else)

LOG-4528 adopted the steering-under-compression discipline (arXiv:2609.06473) with an explicit **condition**: *"no retro-verification of closed S4/S5/S6/I2′ lines (their zero-flip verdicts are transformation-invariant)."* B5 re-runs the TGA injection instruments under a precision transformation. On its face, this looks like the barred thing. The honest case that it is not:

1. **B5 does not touch the S4/S5/S6 static-injection lines or the I2′ battery.** Those verdicts are covered by the condition's rationale and stay closed and untouched. B5 targets only the TGA injection nulls (EXP131/EXP133), a verdict family the condition never named — the TGA line closed 2026-09-30, after the condition was written.
2. **The TGA nulls are not literal zero-flip verdicts of the S4/S5/S6 kind.** EXP131's binding KILL rests on a *measurement* (ĉ = 0.03742, the decision-orthogonality gate via exact-autograd VJPs) *and* a causal test (ΔM_v1 = 0). The adopted compression paper (2609.06473) shows exactly these kinds of quantities — causal structure, baseline decisions — can shift under quantization while geometry survives. The condition's rationale ("verdicts are transformation-invariant") was asserted for the static lines, never for the TGA dynamics-matched nulls.
3. **B5 is not retro-verification of the TGA verdicts.** Retro-verification would ask "were the KILLs correct?" B5 asks a *new* question the sprint's worth-it gate licenses: "does the TGA boundary statement need a precision index?" The draft **fences** this explicitly (§7): B5 cannot overturn, re-open, or re-license the EXP131/EXP133 KILLs or any closed line. The KILLs stand regardless of B5's outcome.
4. **Precedent:** the program already licensed this exact activity class. H2 (EXP110) was the I2′ analogue of B5; its Law #14 review (LOG-4554) explicitly declined the kill invitation — *"H2 licensed as boundary precision-certification, not barred retro-verification"* — and EXP110 executed to CERTIFIED-WITH-NOTE (LOG-4558). B5 is the TGA analogue of that licensed precedent.

**[INTERPRETATION]** B5 is therefore *boundary precision-certification under transformation*, not retro-verification. Extending LOG-4528's condition to bar B5 would stretch it beyond its stated rationale and contradict the licensed H2/EXP110 precedent.

**Adversarial invitation:** if the independent Law #14 reviewer judges §1.1 a rationalization — i.e., that re-running the TGA instruments under any transformation *is* the barred retro-verification — the reviewer is asked to **kill B5 outright** rather than repair it. That kill would be recorded as a verdict on the condition's scope, not a defect in this draft.

---

## 2. Exact question and the decision it changes

**Exact question [HYPOTHESIS]:** Do the TGA decision nulls reproduce under INT8 fake-quantization, or does precision open a transfer window where the full-precision nulls held?

**Decision changed:**
- **CERTIFIED** (§4): the TGA nulls reproduce under weight-only INT8 simulation → the TGA boundary is precision-certified; the paper may carry an honest, bounded precision-generality statement for the TGA closure.
- **PIVOT** (defined below): precision is a new axis for the TGA story → the TGA boundary needs a *precision-indexed* statement, and one follow-up characterization lane is licensed (bounded, §4). The EXP131/EXP133 KILLs stand regardless — PIVOT reopens the question in the quantized regime only.
- **KILL** does not appear in B5's outcome set: B5 cannot kill the TGA boundary (a null reproduces) and cannot kill regime-dependence beyond the tested approximation class.

**PIVOT defined precisely:** a pivot to a precision-indexed TGA boundary statement. Concretely: (a) the program's TGA claims are qualified as "measured at FP32; under weight-only INT8 simulation the binding nulls are {reproduced / shifted: <exact shift>}"; (b) exactly one follow-up characterization lane is licensed, restricted to applying the LOG-4528-adopted procedures (matched-geometry collinearity gate between the FP32 and quantized v̂₁, censored iso-effect dose ladder, baseline-shift attribution) to locate which precision effect drove the flip; (c) the follow-up may not re-open EXP131, EXP133, or any closed line, may not claim capability, and may not mint new experiment numbers beyond its own pre-registered scope.

---

## 3. Method

### 3.1 The nulls under test (FP32 references) [FACT]

| # | Null | FP32 reference | Source |
|---|------|----------------|--------|
| N1 | One-shot decision-orthogonality | ĉ = 0.03742 < 0.1 (mean over 10 prompts, exact-autograd VJP of the cosine margin w.r.t. x_{20,last}) | EXP131, LOG-4830 |
| N2 | One-shot causal null | ΔM_v1 = 0 — zero decision flips over 110 arm-pairs (11 arms × 10 prompts: v̂₁, v̂₂, 8 matched-norm randoms, B_agg dead control); median margin-displacement ratio 0.5592; McNemar one-sided p = 1.0; rank trend 4/10 | EXP131, LOG-4830 |
| N3 | Geodesic-multistep causal null | ΔM_geo = 0; ĉ_geo = 0.0374; McNemar one-sided p = 1.0; zero decision flips | EXP133, LOG-4817 |
| N4 | Dead-control guard | ΔM_Bagg = 0 (EXP131); B_agg-path null (EXP133) | EXP131/EXP133 |
| N5 | Delivery verification | (h): r = 1.0000001 ∈ [0.99, 1.01] — the injection hook reaches the readout tap (the blind-tap lesson, Amendment D) | EXP131/EXP133 |

Secondary (descriptive, not barred): EXP131's median margin-displacement ratio (0.5592), rank trend (4/10), dose detector (d2) rel = 4.832e-6 ≤ 1e-4.

### 3.2 Fake-quantization spec [PROPOSITION]

The EXP110-certified pattern, applied unchanged:
- **What:** weight-only INT8 simulation on a *copy* of the frozen Pythia-410m weights.
- **Exact method:** per-output-channel symmetric INT8 fake-quantization of every `nn.Linear` weight matrix: `scale_c = max|w_c| / 127`; `w_sim = clamp(round(w_c / scale_c), −128, 127) × scale_c`, stored and computed in **float32**. Embeddings, biases, LayerNorm parameters, and all activations stay FP32; no INT8 GEMM kernels — all compute is float32. Deterministic given the weights; pinned `torch` only.
- **What it approximates:** weight-only INT8 inference as studied in arXiv:2609.06473. **What it is not:** true INT8 hardware behavior, activation quantization, or NF4. bitsandbytes `LLM.int8()`-exact is GPU-gated and named as the honest ceiling this run does not reach.
- **Backbone Δθ=0 handling (pinned answer):** (a) the FP32 model is verified against the LOG-331 backbone pin `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed` **before** quantization; (b) the fake-quant transform is applied to a disposable in-memory copy; (c) the copy's SHA-256 is recorded in the worksheet (differs from the pin — expected, not a violation); (d) an internal pre/post-run hash assertion on the quantized copy guards against drift *during* the run (the EXP110 tier0.py discipline); (e) the quantized weights are discarded after the run. Δθ=0 is preserved in the licensed sense: the FP32 reference backbone is never modified.

### 3.3 Re-test protocol on the quantized backbone [PROPOSITION]

Execution (a later lane) runs, in order:
1. **FP32 pin check:** verify the FP32 backbone against the LOG-331 pin before any quantization. Miss → HALT.
2. **Quantized copy derivation:** apply §3.2 to a disposable copy; record the copy's SHA-256.
3. **v₁ re-pin:** `exp127_vectors.npz` SHA-256 must match `9b527c026d0ee307192725429f655e628f403505343dc018de3cfe15db6113dc` with all 10 per-prompt ids aligned as `v1__<prompt_id>` — the injected direction is the FP32 EXP127 direction (same direction, new precision regime). Miss → apparatus-void.
4. **Quantized ĉ re-measurement (N1):** recompute ĉ via exact-autograd VJP of the registered cosine margin w.r.t. x_{20,last} **through the quantized graph** (FP32 compute, fake-quant weights — the VJP is well-defined). Same 10 prompts, same exclusion rule (‖g_i‖ < 1e-12 → exclude; ≥3 exclusions → apparatus-void).
5. **Quantized one-shot injection (N2):** re-run EXP131's 11-arm protocol (v̂₁, v̂₂, 8 matched-norm randoms, B_agg dead control) on the quantized backbone — 10 prompts, norm budget B matched per arm (float32 tolerance 1e-6 relative), injection hook with `prepend=True` per Amendment D. **All ΔM statistics are computed against the quantized-regime baseline** (base forward on the quantized model). Baseline shifts vs FP32 are reported separately per the adopted baseline-shift-attribution discipline — a baseline shift alone does not fail any tier.
6. **Quantized geodesic multistep (N3):** re-run EXP133's geodesic protocol (K=5, sphere retraction + parallel transport, total norm budget B = 0.50578119) on the quantized backbone.
7. **Delivery verification (h) under quantization (N5):** the (h) probe must show r ∈ [0.99, 1.01] on the quantized model for both the one-shot and geodesic arms. The blind-tap lesson applies in the new regime: unverified delivery voids the null.
8. **Raw-record hash-pin** per Law #8; quantized copy discarded after the run.

**The six tiers** — checkable comparisons of the quantized run against the FP32 references:

| # | Tier | FP32 reference | "Reproduces" criterion |
|---|------|----------------|------------------------|
| Q1 | Quantized ĉ | 0.03742 < 0.1 | ĉ_q < 0.1 (VJP through the quantized graph) |
| Q2 | Quantized one-shot causal null | ΔM_v1 = 0 (0/110) | ΔM_v1,q = 0 vs the quantized baseline |
| Q3 | Quantized geodesic causal null | ΔM_geo = 0 | ΔM_geo,q = 0 vs the quantized baseline |
| Q4 | Quantized McNemar non-significance | p = 1.0 | p_q ≥ 0.05 (one-sided, v̂₁ vs quantized base) |
| Q5 | B_agg dead control (apparatus guard) | ΔM_Bagg = 0 | ΔM_Bagg,q = 0 — miss → RUN-INVALID, not PIVOT |
| Q6 | Delivery (h) under quantization (apparatus guard) | r = 1.0000001 ∈ [0.99, 1.01] | r_q ∈ [0.99, 1.01] on both arms — miss → RUN-INVALID (apparatus-void), not PIVOT |

**What "reproduce" means:** each tier is a Boolean against the quantized-regime baseline. No exact-numeric-match requirement on magnitudes (quantization perturbs logits; demanding bit-identity would test the wrong thing).

---

## 4. Decision bars with statistical license

- **Q1 ∧ Q2 ∧ Q3 ∧ Q4 all reproduce → CERTIFIED.** Precision-regime-dependence is killed for the TGA nulls under the tested approximation class (weight-only INT8 simulation, single model). The TGA boundary may carry a bounded precision-generality statement.
- **Any of Q1–Q4 fails → PIVOT** (defined in §2). A decision flip on either injection arm, or ĉ_q ≥ 0.1, means precision opens what full precision closed.
- **Q5 or Q6 fails → RUN-INVALID** (apparatus-void). A dead-control flip means the quantized bench is not what the FP32 bench measured; an (h) miss means delivery is unverified in the new regime. Neither is a verdict on precision.

**False-positive risk — addressed honestly.** The run is fully deterministic (seeded, fixed FP32 weights, deterministic fake-quant, CPU float32) — a flip is a deterministic fact about the quantized regime, not a sampling fluke, so the stochastic false-positive class does not apply (the EXP110 determinism argument, §4). The residual risk is bench-idiosyncrasy, fenced by the single-bench scope in §7. Per the adopted compression paper, precision *does* amplify small perturbations through nonlinearities — a flip under fake-quant is itself the phenomenon B5 tests for, not noise to be explained away.

*Deviation from the dossier (recorded):* the dossier's "any decision flip → PIVOT" is preserved for Q1–Q4 but fenced — Q5/Q6 (apparatus guards) trip RUN-INVALID, not PIVOT, so an apparatus failure in the new regime cannot masquerade as a precision finding.

---

## 5. Falsification decision tree

```
FP32 pin check (LOG-331)
 ├─ miss → HALT (backbone drift; apparatus finding, licenses nothing)
 └─ match ✔
     └─ derive quantized copy (SHA-256 recorded) → v₁ re-pin
         ├─ miss → apparatus-void (wrong direction; hypothesis UNTESTED)
         └─ match ✔
             └─ quantized ĉ + one-shot 11-arm + geodesic + (h) → 6 tier Booleans (Q1..Q6)
                 ├─ Q5 or Q6 false → RUN-INVALID (apparatus-void in the new regime)
                 ├─ Q1∧Q2∧Q3∧Q4 true → CERTIFIED (TGA nulls precision-certified
                 │    under weight-only INT8 simulation; bounded generality licensed)
                 └─ any of Q1..Q4 false → PIVOT
                      → precision-indexed TGA boundary statement required
                      → one follow-up characterization lane licensed (§2: collinearity
                        gate + iso-effect ladder + baseline-shift attribution only)
                      → EXP131/EXP133 KILLs stand; no closed line re-opens;
                        no capability claimed
```

No other branches exist. No re-runs, no larger populations, no post-hoc bars (Law #4, Law #9).

---

## 6. Breaking points (trip conditions)

Conjunctive with §3.3 ordering. Any miss → **apparatus-void or RUN-INVALID as stated, hypothesis UNTESTED**:

(a) **Δθ=0** — FP32 backbone LOG-331 pin verified before quantization and the FP32 reference never modified; any FP32 mismatch → apparatus-void.
(b) **v₁ re-pin** — `exp127_vectors.npz` hash + 10/10 id alignment; miss → apparatus-void.
(c) **No finite differences** — the EXP131/EXP128 constraint carries over: no finite-difference sensing anywhere in the injection pipeline; any such term → apparatus-void.
(d) **Norm-budget matching** — every injection arm spends exactly B under the quantized model (1e-6 relative tolerance); any miss → apparatus-void (the verdict would measure the budget, not the regime).
(e) **B_agg null-control holds** — Q5; miss → RUN-INVALID (apparatus drift in the quantized regime).
(f) **Delivery verified** — Q6 (h) r_q ∈ [0.99, 1.01] on both arms; miss → apparatus-void (blind-tap lesson in the new regime).
(g) **No training, no weight mutation** — pure forwards; the FP32 reference weights are never modified; the quantized copy is derived once and discarded after the run.
(h) **Quantized-copy integrity** — internal pre/post-run hash assertion on the quantized copy holds; drift → apparatus-void.

## 7. What B5 does NOT claim

1. Certification under fake-quant ≠ certification under true INT8 hardware (different rounding/accumulation; §3.2).
2. A CERTIFIED outcome does not re-open, strengthen, or re-license the closed EXP131/EXP133 verdicts — the KILLs stand regardless.
3. A PIVOT outcome does not license re-running any closed line (S4/S5/S6/I2′/TGA) under quantization — only the bounded characterization lane in §2.
4. No claim about trained heads, conditional steering, or any capability gain.
5. No claim of superhuman cognition, consciousness, or generality beyond the tested bench/model/approximation class.
6. **Novelty: N1 — Known Combination.** Fake-quantization + the TGA injection protocols is a known combination; no new mechanism is claimed. (Law #10.)

---

## 8. Worth-it gate (7 points, Law #15)

1. *Exact question:* Do the TGA decision nulls (EXP131 ĉ<0.1 / ΔM=0; EXP133 ΔM_geo=0) reproduce under weight-only INT8 fake-quantization, or does precision open a transfer window?
2. *Decision changed:* **CERTIFIED** (precision-robust TGA boundary → bounded paper-generality statement) vs **PIVOT** (precision-indexed boundary; the TGA question reopens in the quantized regime only).
3. *Cheapest test + cost:* EXP110's certified fake-quant pattern + re-run of the TGA decision arms (quantized ĉ VJPs, 11-arm one-shot, geodesic multistep, (h) under quantization). **$0 CPU, ~2–4h.** No cheaper test exists: the question is inherently about the quantized regime.
4. *Mathematical license:* arXiv:2609.06473 [OBSERVATION] — causal structure can shift under quantization while geometry survives (the exact phenomenon B5 tests for); EXP110's certified fake-quant methodology (Law #14 SIGN, independently bound). *Quantitative prediction:* nulls reproduce — ĉ_q < 0.1, ΔM = 0 on both arms.
5. *Breaking point:* any decision flip on either injection arm, or ĉ_q ≥ 0.1 → **PIVOT** (§4).
6. *Non-resurrection audit (Law #4):* EXP110 certified the I2′ battery, not the TGA kills — different verdict family (full-log staleness re-diff: no TGA-under-quantization execution exists). Differentiated from the gate-killed true-INT8/bitsandbytes-exact (GPU-gated; B5 is the CPU-feasible fake-quant pattern). The LOG-4528 condition is addressed head-on in §1.1 with an adversarial kill invitation.
7. *Summit filter:* honest — boundary infrastructure (paper generality), not capability. No candidate claims consciousness or superhuman achievement.

---

## 9. Boundary

Independent Law #14 review of this exact file is a separate lane. No experiment number is minted by this draft (EXP138 provisional). Execution, if ever launched, is a CEO decision under a minted number. This lane stops here.
