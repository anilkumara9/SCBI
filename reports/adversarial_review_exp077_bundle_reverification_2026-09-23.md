# Law #14 Diff Re-verification — EXP077 Bundle Repair

**Date:** 2026-09-23
**Reviewer role:** Adversarial Reviewer (Law #14, diff re-verification)
**Subject:** `experiments/runs/exp077/` repaired per
`reports/adversarial_review_exp077_bundle_2026-09-23.md` (LOG-124); repair
agent's work logged as LOG-125.
**Signed protocol:** `experiments/protocols/EXP077_CONE_VS_LINE_PREREG_SPEC.md`
(PRE-REGISTERED, SIGN 2026-09-23)

## Verdict: REVISE — 1 residual item (m5 half-addressed). The 3 MAJORS are verified fixed.

Nothing else failed. The residual is a two-line evaluator-text fix with zero
test impact; no new majors were found. Do not launch until the m5 residual is
applied and the zip rebuilt (byte-identity would break otherwise).

---

## 1. MAJOR-1 (μ normalization) — VERIFIED FIXED

- The `mu = mu / (torch.norm(mu) + 1e-12)` line is deleted from
  `build_candidate_directions` (`run_exp077.py` L279 area). `mu` is the raw
  stack mean; `diff = v_hats[k] - mu` matches spec §3.2
  (`v̂^c_k = normalize(v̂_k − μ)`, raw μ).
- Searched the whole runner for any other μ normalization: none
  (only the docstring's registered formula, the raw-mean construction, and the
  spec-compliant logged quantity `‖v̂_k − μ‖` at L493).
- The repair agent's smoke archived μ norm = 55.26 (not unit) — consistent
  with raw-μ construction.

## 2. MAJOR-2 (angular/control endpoints) — VERIFIED FIXED

- `discordant_stats(K, M)` is module-level and pure (no tensors): implements
  spec §3.6 exactly — `b = ΣK(1−M)`, `c = ΣM(1−K)`, McNemar exact two-sided
  via `binomtest`, `b=c=0 → p=1.0` (M5.1).
- Endpoints: `angular = discordant_stats(K_ind, L_ind)` (cone vs LINE),
  `control = discordant_stats(K_ind, R_ind)` (cone vs CONTROL), at runner
  L877–878. The indicator lists (`L_ind`, `K_ind`, `R_ind`) are computed per
  §3.6 (rescue requires C1-incorrect) and are Python int lists.
- Evaluator (`evaluate_exp077.py` `classify`): (a)(i) now fires iff
  `ang["sig_pos"] and ctrl["sig_pos"]` on the §3.6 discordant counts — cone
  beats LINE and cone beats CONTROL. The inverted conjunct (control beats
  baseline) is gone. (b)(i) = `ang["sig_neg"]` with message "line beats cone".
  (c) attempts-alone message: "angular (cone vs line, §3.6) significant but
  the cone-vs-control conjunct failed". Precedence/Holm/shape logic untouched
  (previously verified).
- Test suite: **44/44 pass** under `~/workspace/.venv_smoke` (torch available).
  The 5 new `discordant_stats` regression tests pin the formula
  ((b,c) arithmetic, delta_m, b=c=0→p=1.0, 9-0 split p=0.00390625,
  concordant-pair exclusion). The attempts-alone test now asserts
  (c) NEITHER ("cone beats line, cone-vs-control failed → NEITHER") — the
  inversion is gone from the tests too. (Note: under system python without
  torch, 39/44 run and the 5 runner-import tests skip; this is environmental,
  not a failure.)

## 3. MAJOR-3 (benchmark port) — VERIFIED FIXED

- The runner's benchmark section is now the EXP065/066-identical construction
  ported from `experiments/runs/exp078/run_exp078.py`: same
  `TRIPLES_INDICES`/`QUADS_INDICES` constants (verified identical by eval),
  same novel vocabularies, same `"Premise: {A} outranks {B}..."` templates
  with the same `i%2` target-first parities and the same `i<8`/`i<7` template
  splits per domain/hop.
- Independent programmatic comparison of the reconstructed 60-item lists
  (prompt, target, foil) from both runners: **60/60 items, zero diffs.**
- Law #9 satisfied: no new benchmark construction.

## 4. Minors m1–m5 — m1–m4 verified; m5 HALF-ADDRESSED (the residual)

- **m1** ✓: evaluator `LICENSE_TEXT["r"]` now reads "Re-scope under a new
  pre-registration before any cone-vs-line claim" (spec §1.2 wording).
- **m2** ✓: `w_j` persisted explicitly (`w_list` in the archive dict, L995).
- **m3** ✓: budget footnote — runner L512 logs "actual worst case 1,742;
  0.1% over the [1,740]" and UNTESTED_ASSUMPTIONS U2 discloses it.
- **m4** ✓: `torch_dtype=` kept deliberately with a comment citing LOG-109
  (warning only; `dtype=` would break 4.x compat).
- **m5** ⚠ **HALF-ADDRESSED (residual):** the runner payload's
  `interpretation_notes` was aligned ("spec §11 residual P5", runner L1059),
  but `evaluate_exp077.py`'s `LICENSE_TEXT` still cites the invented
  identifier "(I2)" in two places — L191 ("other radii/gated variants survive
  (I2)") and L194 ("conditional (concept-projection) variants survive (I2)").
  The spec never defines "(I2)"; its named residual is §11/P5.
  Fix (2 lines, no test changes — no test pins the string):
  replace `(I2)` with `(§11/P5 residual)` in both lines, then rebuild the zip.
  This is reporting text only; decision logic is unaffected.

## 5. U1 device audit — STILL CLEAN

- `discordant_stats` is pure Python statistics on int indicator lists; no
  tensor operations or device crossings were added in the repair. The single
  `injection.to(device)` choke point in `eval_item` is untouched.

## 6. U6 entity-set ruling — STANDS

- The repair did not touch the support set (`SUPPORT_VOCABULARIES` still the
  F2-corrected EXP078 set; "Joel" present). The benchmark port changed ITEMS
  (planets/elements, already F2-verified), not support strings. No new entity
  strings introduced.

## 7. Zip byte-identity — VERIFIED (pre-m5-fix)

- Live runner sha256 = `ea74062582f562bed0a0ffe4dd4850af9d53e3eb77af2045bd9361ea85b51984`
  (matches LOG-125); evaluator = `5d4dfbc283582406044b2ee25a5165eff25b51db598c684109f5fdc0c48c5167`
  (matches LOG-125); zip-embedded files byte-identical to live files;
  zip = `f662d7c879021402148e399c555ac5bee25ee65fa23d997e27fd37dfa099b836`
  (matches LOG-125). **The m5 fix will change the evaluator bytes; the zip
  must be rebuilt after applying it, and the new hashes recorded.**

## Required before CLEAR FOR EXECUTION

1. Apply the m5 residual (2-line evaluator text fix above).
2. Re-run `py_compile` + the 44-test suite (expect 44/44).
3. Rebuild `~/workspace/your_files/kaggle/exp077_bundle.zip`; record new
   evaluator/zip hashes in the log.
4. No further Law #14 cycle is needed for this residual — it is
   mechanical reporting text, verified here to be logic-neutral — but the
   parent must confirm the rebuilt zip's byte-identity before any GPU launch.

*No results were invented in this review. CPU-smoke numbers cited are
mechanical validation only, not scientific results.*
