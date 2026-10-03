# EXP140 Stage-1 Run Report (S4-5 free-energy branch selection CPU pilot)

**Pre-reg:** `research/prereg/EXP_S45_prereg_DRAFT_2026-10-03.md` (SIGNED, LOG-4887). CEO venue approval: Stage-1 CPU pilot only (240 generations + 240 scoring passes). $0 compute.

## Validity gates
- (a) bench sha256: `eb304fa65a60b65ad87767d251084b256d0a79001a16b4fe8ebcd1b1f45589df` — PASS
- (b) backbone pre-hash: `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed` — PASS
- (c) determinism spot-check: B0 re-run on items 0, 30, 59 → byte-identical rationales — PASS
- (d) backbone post-hash matches pin (Δθ=0) — PASS
- Pass counts: 240 generations + 240 scoring forwards (budget 240/240) — PASS
- Degenerate branches: 0 pairs; fully-degenerate items: 0

**Note on generation count:** the committed verdict records `generations: 246` due to a diagnostic double-count bug (the spot-check loop incremented the counter twice per re-run). True model.generate calls: 243 = 240 (budget) + 3 (gate-(c) spot-check re-runs, explicitly diagnostic per pre-reg §3). The 240/240 budget gate is unaffected.

## Binding gates
- **G1 diversity:** 28/60 items with ≥2 distinct answers (bar ≥15) — **PASS**
- **G2 variance:** median F-spread = 1.289890 nats/token (bar ≥0.05) — **PASS**
- **G3 calibration:**
  - C1: Spearman(F̄, per-item accuracy) ρ = 0.0798, one-sided p (licensed, negative) = 0.7279 — **NULL** (not inverted: p_inv = 0.2721)
  - C2: partition n_wrong=20, n_right=40; D_obs = -0.0604, one-sided p (licensed, D>0) = 0.8267 — **NULL** (not inverted: p_inv = 0.1733)
  - **G3: FAIL-null** → per pre-reg §0/§3: no GPU (family stands down, not killed — signal absent, not anti-informative)

## Secondary diagnostic (C5)
- min_k F: ρ = 0.3241 (p_lic = 0.9942); D_obs = -0.1851 (p_lic = 0.9991) — **inverted**
- C5 consequence does NOT trigger (requires mean-F to pass G3; it did not). Recorded: if a future run passes mean-F while min-F inverts, the binding consequence is Stage-2's KILL-selector bar.

## Diagnostics (Stage-2 bars NOT applied)
- Accuracy (n=60): B0 = 0.7000, min-F selection = 0.7000, random-branch = 0.7667, SC = 0.7167
- ΔM_FE = 0.0000, ΔM_random = +0.0667, ΔM_SC = +0.0167 (diagnostic only)
- Selection frequency per branch: B0=23, B1=24, B2=0, B3=13 — B2 never selected (temperature vacuity: τ=0.7 sampling inflates F by construction, as predicted in design §4.3)
- Primary F and secondary F^full reported side by side per item in `stage1_records.json`

## Bar comparison (pre-reg §5 — quoted, not decided beyond Stage-1)
- G1 ✓, G2 ✓, G3 null → **HELD (G3 null: C1=null, C2=null)** — licenses nothing, kills nothing. Stage-2 gate does NOT open.
- The free-energy signal shows no calibration in the licensed direction (ρ≈0.08, null). It is not significantly inverted on the primary (mean-F) instrument, so the family is not killed — it stands down.

## Files
- `run_stage1.py` — execution script (verbatim pre-reg implementation)
- `stage1_records.json` — per-item records (60 items × 4 branches, F/F^full/answers/rationales)
- `stage1_verdict.json` — gate verdict
- `stage1_run_log.txt` — run log
