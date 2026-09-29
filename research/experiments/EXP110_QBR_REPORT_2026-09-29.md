# EXP110 — H2/QBR (Quantization-Boundary Robustness) execution report

**Date:** 2026-09-29. **Lane:** LOG-4558 (pre-assigned). **Experiment number:** EXP110.
**Pre-registration:** `research/prereg/EXP_PREREG_H2_QBR_2026-09-29.md` (CEO launch LOG-4557; independent Law #14 SIGN, LOG-4556).
**Verdict:** **CERTIFIED-WITH-NOTE** — 6/7 tiers reproduce with T1–T3 (structural tiers) intact. The single flipped tier is documented as a bounded, measured precision effect; verdicts are unchanged. Certification holds. (Exact pre-reg §4 language.)
**Falsification-tree branch taken:** `6/7 true AND T1∧T2∧T3 true → CERTIFIED-WITH-NOTE (flip documented as bounded precision effect; verdicts unchanged)`.
**Fences honored (§7):** certification is scoped to the INT8 *simulation* — it is not a claim about true INT8 hardware; it does not strengthen, re-open, or re-license the closed I2′/EXP105 KILL; the KILL stands regardless; no closed line was re-run; novelty N1 (Known Combination).

---

## 1. Environment sanity (pre-reg §3.3 step 1) [FACT]

`bash falsification_kit/reproduce_exp105.sh` → printed **`REPRODUCTION EXACT ✔`** (exit 0). All 31 unit tests PASS; battery re-run on committed EXP105 logits matches the published worksheet on all 7 comparison fields (verdict KILL, step 9, n_pop 21, dM_T 0.23809523809523808, dM_R 0.0, p_TvsR 0.0625, O 0.5714285714285714).

### Law #13 environment manifest [FACT]

| Key | Value |
|---|---|
| torch | `2.14.0+cpu` (matches reference pin) |
| transformers | `5.17.0` (matches reference pin) |
| venv | `~/workspace/.venv-exp095/bin/python` |
| CPU threads set | 2 (via `OMP_NUM_THREADS=2`, `MKL_NUM_THREADS=2`, `torch.set_num_threads(2)`) |
| CPU threads read back | 2 (`torch.get_num_threads()`) |
| device | cpu only; no GPU contact at any point |
| seed | 20260928 (Tier-0 and battery) |
| bench | `falsification_kit/bench/cloze_bench.json`, 60 cloze items, G1 single-token gate 60/60 passed on the quantized model |

---

## 2. Backbone Δθ=0 handling (pre-reg §3.2) [FACT]

- **FP32 backbone verified before quantization:** `get_hash` (SHA-256 over concatenation of `state_dict()` tensors, sorted keys, CPU float32 bytes — verbatim procedure from `experiments/runs/exp077/run_exp077.py` ll.166–174, the LOG-331 method) = `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed` — **matches the LOG-331 pin exactly**. The starting point is the licensed frozen backbone.
- A first-pass hash using tier0.py's parameter-order hash produced `4c242d9a…` (mismatch). Root cause: **hash-method difference, not weight difference** — tier0.py hashes `model.parameters()` order; the LOG-331 pin hashes sorted `state_dict()` keys. Re-running with the verbatim LOG-331 procedure reproduces the pin exactly. Documented here so no one re-discovers it.
- **Fake-quantization applied to a disposable copy:** per-output-channel symmetric INT8 on **every** `nn.Linear` weight (97 Linear layers, 271,488 output rows; 0 exact-zero rows): `scale_c = max|w_c|/127`; `w_sim = clamp(round(w_c/scale_c), −128, 127) × scale_c`, stored and computed in float32. Embeddings, biases, LayerNorm parameters, and all activations stayed FP32. No INT8 GEMM kernels — all compute float32.
- **Quantized-copy presentation mechanism (F2):** saved-to-local-directory, presented to tier0.py via `--model-id /home/hatch/workspace/SCBI/experiments/runs/EXP110_qbr/out/quantized_model` (tokenizer saved alongside).
- **Quantized-copy SHA-256:** `ed919d476819051e2ac7f16461bb07a0befa8886bb0c9f9ed28e14f20cab9c33` — differs from the pin, **as expected**. The copy is disposable and was never persisted into any artifact.
- **Δθ=0 during the run:** tier0.py's internal pre/post-run hash assertion held (`weight hash identical pre/post` printed); the FP32 reference weights were never modified.

---

## 3. Zero generation (pre-reg §3.1 hard constraint) [FACT]

`tier0.py` performs forward passes only (single-token candidate logits; no `.generate(` anywhere in the file — verified by code read). `battery.py` is pure logit arithmetic (masking at −1e9 before argmax; no model contact). No generation step was required; the run proceeded on the licensed path.

---

## 4. Results — seven tiers (pre-reg §3.3) [OBSERVATION]

Reference (FP32): `falsification_kit/reference/battery_worksheet.json` + EXP105. Quantized: this run.

| # | Tier | Reference (FP32) | Quantized (INT8 sim) | Boolean |
|---|------|-------------------|-----------------------|---------|
| T1 | Tier-0 verdict | `TIER-0 PASSED` @ 0.5333 | `TIER-0 PASSED` @ 0.5333 (28 failed, tie_rate 0.000) | **TRUE** |
| T2 | Battery verdict class | `KILL` | `KILL` | **TRUE** |
| T3 | Battery step | step 9 | step 9 | **TRUE** |
| T4 | Contrast signs/band | dM_T=+0.2381>0, dM_F=+0.1429>0, \|dM_R\|<0.05 | dM_T=+0.2000>0, dM_F=+0.1500>0, \|dM_R\|=0.0000<0.05 | **TRUE** |
| T5 | McNemar non-significance | T-vs-R b=5, c=0, p=0.0625 ≥ 0.05 | T-vs-R b=4, c=0, p=0.1250 ≥ 0.05 | **TRUE** |
| T6 | Foil–top-1 overlap gate | O=0.5714 > 0.5 | O=**0.5000** — not > 0.5 (exactly at gate) | **FALSE** |
| T7 | Population comparability | n_pop=21, median failed rank 4.0 | n_pop=**20** (within ±5 of 21, >0; median failed rank **4.0**) | **TRUE** |

**Score: 6/7, with structural tiers T1–T3 intact.**

### The flipped tier (T6) — bounded measured precision effect [OBSERVATION + INTERPRETATION]

Under the INT8 simulation the battery population shrank 21→20 (one failed item's correct-rank moved above the rank-5 population bound, i.e. the population, not the model, shifted at the margin). The T-vs-R discordance moved b=5→b=4, p=0.0625→0.1250 — the binding bar is still missed by a wider margin. Foil–top-1 overlap fell from 12/21=0.5714 to 10/20=0.5000, landing **exactly on** the 0.5 gate, so the strict `O > 0.5` reproduce-criterion fails. This is the deterministic precision effect the pre-reg anticipated: a single *non-structural* (diagnostic-evidence) flip while verdict class and step are unchanged. The run is fully deterministic (seeded, fixed weights, deterministic fake-quant, CPU float32); the flip is a deterministic fact about the quantized regime, not a sampling fluke, and single-bench scope is fenced in §7.

**Decision bars (§4):** any structural flip (T1/T2/T3) or ≤5/7 → PIVOT. **Not triggered.** → **CERTIFIED-WITH-NOTE** [INTERPRETATION].

---

## 5. What this certifies and what it does not [INTERPRETATION]

- **Certified:** the EXP105 battery's binding verdict (KILL at step 9) is precision-regime-robust under weight-only INT8 *fake-quantization* (per-channel symmetric, float32 compute, single bench, single model). Precision-regime-dependence is killed **for the tested approximation class**. The boundary may carry a bounded precision-generality statement, indexed as simulation-only.
- **Not claimed:** certification under true INT8 hardware (different rounding/accumulation), activation quantization, or NF4. No strengthening, re-opening, or re-licensing of the I2′ KILL — it stands regardless. No capability claim; no superhuman-cognition claim. The one licensed follow-up characterization lane (collinearity gate + iso-effect ladder + baseline-shift attribution) is **not** dispatched here: the PIVOT branch was not taken.

---

## 6. Provenance [FACT]

- Raw logs: `~/workspace/SCBI/experiments/runs/EXP110_qbr/out/` — `tier0_quantized.json`, `battery_quantized.json`, `tier0_stdout.log`, `battery_stdout.log`, `fakequant_manifest.json`, `fakequant_stdout.log`, `quantized_model/` (disposable copy; may be deleted after archival verification).
- Sanity log: `/tmp/exp110_repro.log` (`REPRODUCTION EXACT ✔`, exit 0).
- Quantizer script: `/tmp/exp110/fake_quantize.py` (ephemeral; procedure fully described in §2).
- Cost: $0 CPU. Tier-0: 60 forward passes on the quantized copy (~70s item time + ~40s load/hash guard). No GPU contact. No model weights modified (FP32 reference untouched; only the disposable copy was transformed).
