# R4 (EOC) — Stage −1 Report

*2026-09-26. License: LOG-4353 (Friday cull). Lane: Poole 2016 citation verification + λ̂ finite-difference proxy sanity check on a toy random network. $0 compute, CPU only, numpy; no model weights, no pretrained forward passes, no signed protocols touched. On paper + toy only.*

## 1. Citation: Poole et al. 2016 — VERIFIED with attribution correction

- **The paper exists and is the right framework:** Poole, Lahiri, Raghu, Sohl-Dickstein, Ganguli, "Exponential expressivity in deep neural networks through transient chaos", arXiv:1606.05340, NIPS 2016 (NeurIPS poster 7128; abstract verified against arXiv + NeurIPS.cc).
  - [FACT] It proves an order-to-chaos expressivity phase transition in random deep nets and derives the correlation-map slope χ₁ (Eq. 7) — explicitly "a multiplicative stretch factor" partitioning ordered (χ₁ < 1) from chaotic (χ₁ > 1) regions (Fig. 2D). χ₁ − 1 is the theoretical object the λ̂ diagnostic finite-differences across depth, so Poole 2016 is the correct framework citation for the λ̂≈0 criticality criterion.
- **Attribution correction (misattribution found):** the worth-it analysis states "signal-propagation depth scales are maximal at criticality" as a Poole 2016 theorem. A full-text search of Poole 2016 (ar5iv) contains **zero** occurrences of "depth scale". That theorem belongs to **Schoenholz, Gilmer, Ganguli, Sohl-Dickstein, "Deep Information Propagation", ICLR 2017 (arXiv:1611.01232)**, whose abstract states verbatim: "As a corollary to this, we argue that in networks at the edge of chaos, one of these depth scales diverges. Thus arbitrarily deep networks may be trained only sufficiently close to criticality."
- **Effect on the license:** survives with corrected attribution. Poole 2016 licenses the diagnostic object (χ₁ / finite-depth stretch factor, the order–chaos boundary at λ̂ = 0); Schoenholz et al. 2017 licenses the "maximal propagation at criticality" half of the story. The worth-it analysis's Gap 1 (trainability → inference-time decision accuracy is analogical, one inferential step) applies under either attribution and is unchanged. **Action required before pre-registration: the pre-reg must cite Schoenholz et al. 2017 for the depth-scale-maximality claim, not Poole 2016.**

## 2. λ̂ finite-difference proxy on a toy random net — WELL-DEFINED

Setup: numpy random MLP, widths [64, 128×10, 64] (L = 11 layers), tanh, Gaussian weights; 20 normalized random items; λ̂(x) = log(‖Δh_L‖/‖Δh_0‖)/L from passes (x, x + εu), u a random unit direction. Script: `/tmp/r4_stage_minus1/lambda_hat_toy.py` (re-runnable; master seed 20260926). All numbers below are computed, not invented.

| Check | Result |
|---|---|
| Well-definedness | **0 NaN / 0 Inf over 860 measurements** — no degenerate ‖Δh₀‖, no blow-up |
| ε-robustness (1e-6 … 1e-2, 5 decades, fixed seeds) | per-decade means identical to 5 decimals; cross-decade Pearson **r = 1.0000** (0.9998 at 1e-2) — proxy sits in the linear regime; ε choice is non-load-bearing |
| Regime discrimination (gain sweep) | gain 0.5 → λ̂ = **−0.683** (ordered); gain 1.0 → λ̂ = **−0.004** (critical); gain 1.5 → λ̂ = **+0.210** (chaotic). Regime separation (~0.5–0.9) is **30–60× the within-item seed noise** — the diagnostic detects the regime it is supposed to |
| Seed stability (fixed net, u-seed varies — the real-experiment case) | within-item std **0.013**; cross-item std of per-item means **0.003** (discriminability ratio ≈ 0.23) — seed noise dominates item-to-item variation on a random net |

**Honest reading:** the proxy is mechanically sound (defined, ε-independent, regime-sensitive), but on random nets the λ̂(x) per-item signal is *seed noise, not item structure* (within-item std 4× the cross-item spread). For the real experiment this means: (a) direction seed must be pinned exactly once, as the skeleton already requires; (b) the skeleton's **Var(∣λ̂_baseline∣) floor gate is genuinely load-bearing, not optional** — if a frozen model's items show no more λ̂ variance than seed noise, the dose-response test is powerless and the pre-reg must fire Underdetermined, never KILL; (c) Stage 0's seed/ε-stability gate must be run on the real model before any scheduling, exactly as sequenced.

## 3. Signal for the R4 lane: **CONTINUE to full pre-registration** (with a citation erratum)

- λ̂ proxy: WELL-DEFINED — gates satisfied on toy; nothing here licenses a diagnostic-invalid KILL.
- Citation: Poole 2016 VERIFIED as the framework paper, with the depth-scale-maximality claim **re-attributed to Schoenholz et al. 2017** (append-only erratum to `R4_WORTHIT_ANALYSIS_2026-09-25.md`; signed artifacts untouched).
- Pre-reg hardening confirmed by this wave: (1) cite Schoenholz 2017 for the depth-scale claim; (2) pin the ε-direction seed once; (3) keep the Var(∣λ̂_baseline∣) floor as the power gate — the toy shows it will be needed.
