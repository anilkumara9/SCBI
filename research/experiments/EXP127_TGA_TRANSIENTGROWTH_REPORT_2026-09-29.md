# EXP127 (TGA/TRANSIENT-GROWTH) Execution Report — 2026-09-29

**Lane:** LOG-4698 (pre-assigned). **Protocol:**
`research/prereg/EXP_PREREG_TGA_TRANSIENTGROWTH_2026-09-29.md`
(launch-ready: Law #14 SIGN-WITH-FIXES LOG-4696; all five fixes
byte-verified LOG-4697; post-fix sha256
`5dea0d419794fe6aa1fce056b9225625aa6ec3b55c57fab39bb7cb9e7d6e2882`
— verified before any JVP).
**Verdict: CONTINUE** — median R = 8.240640 ≥ 3 AND median σ₁/σ₂ =
1.557689 ≥ 1.5. The frozen L20→L24 propagator possesses a
distinguished maximally-amplified direction v₁ whose transient gain
dwarfs the gain along random directions.
**$0 CPU. Δθ=0. R was read only after all guards passed and raw
records were hash-pinned (Law #9).**

---

## 1. Verdict statement

**CONTINUE — the dynamics-matched injection program is licensed for a
GPU gate.** On the 10 verbatim EXP107-bench prompts (canonical-order
first 10), the clamped-context final-token-map Jacobian
M = ∂x_{24,last}/∂x_{20,last} has:

- **median R = σ₁/σ̄ = 8.240640** (per-prompt R ∈ [8.0019, 8.5294]) —
  the leading singular direction amplifies perturbations **≈8×**
  more than the average random direction;
- **median σ₁/σ₂ = 1.557689** (per-prompt ∈ [1.5302, 1.5881]) — the
  amplifier is concentrated on a distinguished leading direction,
  clearing the 1.5 auxiliary bar on all 10 prompts.

Per §2 of the protocol, this CONTINUE licenses **a signed GPU
injection-test pre-registration** along v₁ vs matched-norm random
directions vs B_agg (the EXP077 dead direction), minting a new
experiment number — the first licensed injection direction since the
static family closed. It licenses **no injection by itself**, no
steering claim, and does **not** move the capability scoreboard
(still zero positive signals for autonomous steering).

## 2. Falsification-tree walk (all numbers executor-produced)

| Tree node | Result |
|---|---|
| Protocol hash before execute | **PASS** — `5dea0d41…6e2882` matched |
| Prompt set: verbatim EXP107 bench, canonical first 10, ids pinned | **PASS** — 10/10 ids `exp107_{flip,ctrl}_exp077_planet_2hop_{0..9}` |
| Backbone LOG-331 pin (pre) | **PASS** — `ec276abe3902fab0…` |
| Manual-span sanity (diagnostic): max‖f(z₀)−x₂₄,base‖ | **PASS** — 2.4e-04 … 8.2e-04 across prompts (≤ 1e-3) |
| σ₁ power iteration (1e-6 rel / 5 iters / ≥20) | **PASS** — 10/10 converged (20–26 iters) |
| Hutchinson σ̄ (K=64, same M, same budget) | **PASS** — present on all 10 |
| Direct random arm (K=64, same M) | **PASS** — present on all 10 |
| Deflated σ₂ (1e-4 rel / 5 iters / ≥10) | **PASS** — 10/10 converged (19–36 iters) |
| Budget cap 700 products/prompt | **PASS** — per-prompt totals 264–318 |
| Direct-vs-Hutchinson agreement trip (diagnostic ≤0.15) | **PASS** — 0.0083 … 0.0263 on all 10 |
| Raw records hash-pinned | **PASS** — before R was read |
| Backbone LOG-331 pin (post) | **PASS** — identical; Δθ=0 |
| **median R** (decision set n_d=10) | **8.240640 ≥ 3** |
| **median σ₁/σ₂** (same decision set) | **1.557689 ≥ 1.5** |

No p-value was computed, quoted, or needed — the R ≥ 3 decision is
a registered ratio bar (defect class 1).

## 3. Per-prompt measurements (executor-produced)

| prompt | σ₁ | σ₂ | σ̄ (Hutch) | R | σ₁/σ₂ | products |
|---|---|---|---|---|---|---|
| exp107_flip_exp077_planet_2hop_0 | 9.4258 | 6.1597 | 1.1764 | 8.0123 | 1.5302 | 272 |
| exp107_ctrl_exp077_planet_2hop_1 | 10.1139 | 6.4644 | 1.1994 | 8.4328 | 1.5646 | 264 |
| exp107_flip_exp077_planet_2hop_2 | 9.4991 | 6.1036 | 1.1766 | 8.0735 | 1.5563 | 280 |
| exp107_ctrl_exp077_planet_2hop_3 | 9.7816 | 6.2740 | 1.1743 | 8.3299 | 1.5591 | 268 |
| exp107_flip_exp077_planet_2hop_4 | 9.3863 | 6.0444 | 1.1708 | 8.0170 | 1.5529 | 270 |
| exp107_ctrl_exp077_planet_2hop_5 | 10.0669 | 6.3390 | 1.1803 | 8.5294 | 1.5881 | 270 |
| exp107_flip_exp077_planet_2hop_6 | 9.2663 | 6.0141 | 1.1580 | 8.0019 | 1.5408 | 318 |
| exp107_ctrl_exp077_planet_2hop_7 | 10.0364 | 6.4195 | 1.2040 | 8.3359 | 1.5634 | 276 |
| exp107_ctrl_exp077_planet_2hop_8 | 9.5429 | 6.1450 | 1.1658 | 8.1858 | 1.5529 | 278 |
| exp107_flip_exp077_planet_2hop_9 | 9.9041 | 6.2641 | 1.1939 | 8.2954 | 1.5811 | 290 |

[OBSERVATION] The measurements are strikingly prompt-invariant:
σ₁ ∈ [9.27, 10.11], σ₂ ∈ [6.01, 6.46], σ̄ ∈ [1.158, 1.204],
R ∈ [8.00, 8.53]. The propagator's amplification structure is a
property of the frozen span, not of prompt content — exactly what a
dynamics-matched instrument requires. The σ₁/σ₂ ratio sits in a
narrow band [1.53, 1.59], clearing the 1.5 bar on every prompt but
leaving a real second amplified direction σ₂ ≈ 6.1–6.5 in play.

## 4. Raw artifacts (hash-pinned before R was read — defect class 2)

`~/workspace/SCBI/experiments/runs/EXP127_tga/out/`:

| Artifact | SHA-256 | Pinned before R? |
|---|---|---|
| `exp127_per_prompt.json` (10 records: ids, prompts, T, sanity, σ₁/σ₂ traces+iters+convergence, Hutchinson Tr, direct norms, R, per-arm product counts) | `66f028ba1fb786a71cc1b5956924ce1bc42ffa0612eac877f951224e85e8bc13` | yes |
| `exp127_vectors.npz` (v₁ per prompt + 64 direct uⱼ per prompt, float32) | `9b527c026d0ee307192725429f655e628f403505343dc018de3cfe15db6113dc` | yes |
| `exp127_worksheet.json` (environment manifest, pins, final verdict) | `f045413af61a1a4f58ca21063f90048417c12428afc096261a6d581f83cba918` | yes |
| `exp127_console.log` (full console transcript) | `787580106e3ffebd252a468c1ed35f506324a9f46b00db337f5d0ba2ddfae69e` | yes (append-only) |
| `exp127_execute.py` (the executor) | — | — |

Environment: torch 2.14.0+cpu, transformers 5.17.0, numpy 2.5.3;
`torch.manual_seed(20260929)`, per-prompt generators seeded
`20260929 + prompt_index`; threads=2 (read back 2); `model.eval()`,
float32, CPU; all parameter tensors `requires_grad=False`. Runtime
~2.7 min for the full 10-prompt measurement (exit code 0).

## 5. Method-integrity notes (for the Law #14 review)

1. **transformers 5.x hidden-states indexing:** `@capture_outputs`
   returns `hs[24]` = final-layer-norm output, NOT block 23's
   output. The protocol's x_{24} (output of block 23, pre-norm) was
   obtained from the real layer-23 module — verified
   `fln(module(hs[23])) == hs[24]` to 0.0. The manual 4-block span
   reproduces the model at the base point to ≤ 8.2e-04 on all
   prompts (diagnostic, §2).
2. **torch 2.14 `vjp` API:** `torch.autograd.functional.vjp(f,
   (z,), (w,))` returns `(output, vjp_result)` directly (no
   callable); the executor reads `[1][0]`. Each call = 1 VJP
   product under the §3.6 counting rule.
3. **Per-head qkv layout:** rows `[h*192:h*192+64]` = q_h (etc.),
   verified against the module's attention output to 9.8e-05.
4. **No materialization:** M (1024×1024) was never materialized;
   all σ estimates are from autograd JVP/VJP products only.
5. The executor contains no optimizer, no loss, no backward pass
   into weights — Δθ=0 by construction, confirmed by identical
   pre/post LOG-331 pins.

## 6. Honest frame

- A CONTINUE here licenses a **GPU injection-test pre-registration**,
  not a steering claim. The downstream pre-reg carries its own
  Law #14 review, its own bars, and the ĉ decision-orthogonality
  gate (ĉ < 0.1 → KILL at injection) plus the rank-trend KILL gate.
- R ≥ 3 does not claim v₁ steers anything; it claims the dynamics
  contain a usable directional amplifier worth testing. The
  capability scoreboard stays at zero.
- No generality beyond Pythia-410m L20→L24 and the 10 pinned
  prompts is licensed. The cross-position (unfrozen-KV) Jacobian
  remains unmeasured by design (§3.3, §10).
- The σ₁/σ₂ band [1.53, 1.59] clears the auxiliary bar but is not
  a wide margin — the injection pre-reg should carry the rank-trend
  gate exactly as named in §2, since σ₂ ≈ 6.3 is itself a strong
  amplifier.
- Novelty remains N1 — Known Combination (§7.1.6).
