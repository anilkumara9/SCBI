# EXP126 (H23/WITHIN-DOMAIN) Execution Report — 2026-09-29

**Lane:** LOG-4688 (pre-assigned). **Protocol:** `research/prereg/EXP_PREREG_H23_WITHINDOMAIN_2026-09-29.md`
(launch-ready: Law #14 SIGN, zero fixes, LOG-4686; protocol sha256
`42660838a4ab48e9a54871114cf60ffb8be5c8ad538f251f8001baf9c29e8117`).
**Verdict: KILL** — the identity-readout interpretation is dead on bench 5:
test accuracy 18/30 = 0.6000 ≤ 18/30 band, with G = −0.4000.
**$0 CPU. Δθ=0. The metric was read only after all guards passed (Law #9).**

---

## 1. Verdict statement

**KILL (identity-readout interpretation).** On the 60-item all-animal bench 5
(single domain, entity-subset labels y=1 iff tuple[0] ∈ S1, domain-set membership
informationally dead by construction), the pinned H5/H16 head protocol
(L2-logistic, C=1.0, lbfgs, seed 20260929, stratified 30/30, layer-20 tap site)
scored **18/30 = 0.6000** on the held-out test set with **G = acc(F) − acc(T) =
0.4000 − 0.8000 = −0.4000**. The registered KILL bar fires on the accuracy arm
(≤18/30, p ≥ 0.1808); the word-family kill-test arm did not fire (G = −0.40 < 0.30 —
the accuracy asymmetry runs the *opposite* direction of a word-family detector).

Law #11 two-layer tagging applies exactly as pre-registered: **EXP111's, EXP120's,
and EXP122's bench observations stand** (Law #8); their three-bench CONTINUE is
**reclassified as a domain-set-detector correlation**, never erased or re-scored.
Any entity-level use of the signal is retired.

---

## 2. Falsification-tree walk (all numbers executor-produced)

| Tree node | Result |
|---|---|
| Protocol sha256 | **recorded** — `42660838a4ab48e9a54871114cf60ffb8be5c8ad538f251f8001baf9c29e8117` (matches the signed draft) |
| Bench provenance + len==60 + schema (ids 60/60 unique, `expb5_` namespace, labels 30/30, phrasing 30/30, flips 30/30, Law-#7 pin 60/60, four 15-item cells, extraction contract) | **PASS** — bench sha256 `444e40260b4c71c512db72db2c5d2555b31ffbbd8db2eedcf8a3a46fddbb0e8a` == LOG-4687 certificate pin |
| Backbone LOG-331 pin (pre) | **PASS** — `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed` |
| 60 fresh layer-20 premise extractions (premises only, float32, CPU, `model.eval()`, `torch.no_grad()`, seeds 0/0, threads 2 read back 2) | **DONE** — X=(60, 1024); ~48 s |
| Backbone LOG-331 pin (post) | **PASS** — identical pin; **Δθ=0** |
| Bench hash stable across extraction (block-off (a)) | **PASS** |
| Stratified 30/30 split (seed 20260929, key `f"{phrasing}_{flipped}"`, N_F=15/N_T=15) | **PASS** — train=30, test=30, disjoint (any overlap → RUN-INVALID was armed) |
| Train L2-logreg + determinism re-fit pass (block-off (c)) | **PASS** — byte-identical test predictions (lbfgs n_iter=142; no convergence warning) |
| Artifact-existence gate (§3.7) | **PASS** — embeddings npz, head weights npz, split ids json, bench json, backbone pins — all hash-pinned before verdict |
| **test accuracy = 18/30 = 0.6000, G = −0.4000** | **KILL** — acc ≤ 18/30 arm (p ≥ 0.1808); word-family arm not triggered (G < 0.30) |

**Lane defect disclosed (caught by the tree, no silent repair):** the executor's first
attempt loaded the backbone with `AutoModel` instead of `AutoModelForCausalLM`;
the LOG-331 pin was computed on the full causal-LM state dict (includes
`embed_out.weight`), so the pre-extraction pin mismatched and the tree halted at
RUN-INVALID before any extraction. The executor was corrected to
`AutoModelForCausalLM` (the LOG-331 method, identical to EXP125's loader), the pin
matched, and the full tree re-ran from the top. No metric existed before the pin
passed (Law #9 honored); both attempts are on the append-only console log.

---

## 3. Executor-computed values (defect class (a) — printed, never handwritten)

| Quantity | Executor value |
|---|---|
| P(X ≥ 20 \| 30, 0.5) [CONTINUE bar license] | 0.0493685734 |
| P(X ≥ 19 \| 30, 0.5) [HELD boundary] | 0.1002442110 |
| P(X ≥ 18 \| 30, 0.5) [KILL no-signal license] | 0.1807973040 |
| P(X ≥ 18 \| 30, 0.5) [observed one-sided] | **0.1807973040** |
| G kill-test threshold | ±0.30; observed G = −0.4000 (fires nothing on this arm) |

The observed one-sided p = 0.1808 ≥ 0.1808 — exactly at the boundary of the
≤18/30 KILL band: the result is indistinguishable from chance.

**Registered bars (H5/H16 signed n=30 head bars, verbatim — Law #4):**

| Test accuracy | Verdict | License |
|---|---|---|
| ≥ 20/30 AND G < 0.30 | CONTINUE | identity readout survives domain-set-decoy removal |
| 19/30 AND G < 0.30 | HELD | underpowered; no rescue |
| **≤ 18/30 OR G ≥ 0.30** | **KILL** | **no identity readout on bench 5 — this run (18/30, G=−0.40)** |

No cross-bench effect sizes were computed (unlicensed). H6's 42–57/60 bars were
not transferred (wrong apparatus, wrong n).

---

## 4. Raw artifacts (hash-pinned before verdict — defect class (b))

`~/workspace/SCBI/experiments/runs/EXP126_withindomain/out/`:

| Artifact | SHA-256 | Pinned before verdict? |
|---|---|---|
| `exp126_embeddings.npz` (60×1024 float32 + ids) | `b448faf41af4a4bc0136138dd9293f24d12d772be369c1beb3b7f526f208e1e2` | yes |
| `exp126_head_weights.npz` (coef_, intercept_) | `a84846fc21c1e708760833482cd7ca345e985b29523cd593cef58bd8c8d05d8e` | yes |
| `exp126_split_ids.json` (train/test lists, N_F, N_T, seed) | `925ae590ed398993c0f7ac37f6923651253fd7af1ee29e5f542993688537a738` | yes |
| `exp126_bench5.json` (bench provenance — LOG-4687) | `444e40260b4c71c512db72db2c5d2555b31ffbbd8db2eedcf8a3a46fddbb0e8a` | yes |
| `exp126_worksheet.json` (environment, pins, guards, metric, verdict) | `66f671e9e33dab58d117808ed45dc1ba0623ca02a5f51bbeea2374338be38c37` | yes |
| `exp126_console.log` (full console transcript, both attempts) | — | yes (append-only) |
| `exp126_execute.py` (the executor) | — | — |

Environment: torch 2.14.0+cpu, transformers 5.17.0, numpy 2.5.3, sklearn 1.9.1
(`~/workspace/.venv-exp111`); `torch.manual_seed(0)`, numpy seed 0, threads=2
(read back 2). Runtime ~1 min for 60 forwards (exit code 0).

---

## 5. Descriptive findings (unlicensed observations, not verdicts)

[OBSERVATION] **Train-test inversion:** train accuracy 1.0000 (||w||=1.7255,
converged in 142 lbfgs iterations) vs test accuracy 0.6000 — the head fit the
train split perfectly and generalized at chance. [OBSERVATION] **Reversed
cell asymmetry:** per-cell test accuracies ("target-first", orig)=2/8,
("target-first", flip)=6/7, ("target-last", orig)=4/7, ("target-last", flip)=6/8 —
higher on flipped-word items (acc(T)=0.80) than original-word items (acc(F)=0.40),
i.e. G=−0.40. This is the opposite of the pre-registered word-family detector
signature (which required G ≥ +0.30) — recorded as [OBSERVATION] only; no decision
branch reads it, and no causal claim is licensed.

---

## 6. Honest frame

- A KILL here retires the **identity-readout interpretation** — the head does not
  extract entity-subset identity within a single domain. EXP111's, EXP120's, and
  EXP122's bench observations **stand** (Law #8); their three-bench CONTINUE is
  reclassified as a **domain-set-detector correlation** (Law #11) — the heads on
  benches 1–3 plausibly read only which domain set sits on top, a cue bench 5
  removes.
- The trained head is a **label-informed control**, never an autonomous mechanism —
  this result never migrates to the capability scoreboard, which stays at **zero
  positive signals for autonomous steering**.
- Per the pre-reg, a KILL is never followed by a larger-N re-test, a different
  layer, a different label design, or a sixth bench for the identity interpretation —
  each would be an unlicensed gate tweak (barred). H22's generality hypothesis
  stays **KILLed** (EXP125 — not re-opened here). No hypothesis rewording occurred
  or is licensed (Law #4).
- Novelty remains N1 — Known Combination (§8.6).

[INTERPRETATION] The program's boundary map tightens: the three-bench
decodability CONTINUEs were already decodability-not-steering (EXP122 §8); H23
shows their mechanistic reading is exhausted by a domain-set detector. The
label-free race — the actual race — stands at zero positive signals.
