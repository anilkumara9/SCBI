# Independent Exact-Artifact Verdict Review — EXP129 (CLP closed-loop adaptive pursuit)

**Lane:** LOG-4716 (pre-assigned). **$0 CPU.** Fresh eyes — the reviewer did not
execute this run. Read-only everywhere except this review and the research-log
append. Nothing pushed, spent, or credential-touched.

**Verdict: BIND-WITH-CAVEAT** — the execution lane's KILL is correct from the
exact artifacts. The caveats are documentation-only and non-verdict-bearing.

## Scope

EXP129 (CLP, Family C) reported **KILL** — median per-item feedback-gain ratio
r = 1.000005 ≤ 1.2 (bar). The loop adds nothing the push didn't already do.
Saturation and dose-in-disguise KILL branches evaluated first per FIX-1
precedence; neither fired.

## What I did

Reimplemented the §4 decision-statistic computation from the protocol text —
I did **not** reuse the executor's functions. Every number below comes from
the raw artifacts in `experiments/runs/EXP129_clp/out/`.

## Verification results

1. **Protocol hash:** on-disk sha256 = signed post-erratum
   `8eea9f0d659501885cbe7e30657824a372495fda9ecc130c8cc4a0cabeee5ba7`;
   matches the report and the console pre-forward pin. ✓

2. **Median ratio re-derived: 1.0000048288402206 → 1.000005.**
   Stored per-item `r` equals the registered definition
   `‖d₂‖/max(‖d_sum‖,‖d_single‖)` exactly (all 10, |Δ| < 1e-12). Sorted:
   [0.9997644, 0.9997879, 0.9998918, 0.9999387, 0.9999803, 1.0000293,
   1.0000545, 1.0000794, 1.0001067, 1.0002242]; median = mean of the middle
   two = 1.0000048288… ✓. The KILL bar (≤ 1.2) fires. ✓

3. **KILL-branch flags re-derived:**
   - saturation median ‖d₂−d₁‖/‖d₁‖ = 1.013390064239502 → 1.013390 ✓
     (bar ≤ 0.1 — did not fire) ✓
   - dose-in-disguise median ‖d₂‖/‖d_sum‖ = 1.6523812231656738 → 1.652381 ✓
     (bar ≤ 1.2 — did not fire) ✓
   The precedence claim (KILL branches evaluated first) is consistent with
   the console record. ✓

4. **Δθ=0:** backbone pins pre/post both
   `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed`
   (worksheet + console). ✓

5. **Guards:**
   - v̂₁ re-pin: npz sha256
     `9b527c026d0ee307192725429f655e628f403505343dc018de3cfe15db6113dc`;
     10/10 `v1__<prompt_id>` alignment; all unit norm. ✓
   - v̂₂ derivation (LOG-4714 erratum): seed `20260929_4714`, K=40, exact
     JVP/VJP, all unit norm, 10/10 `v2__<prompt_id>` alignment. ✓
     Orthogonality: all |v̂₂ᵀv̂₁| pass the apparatus-void bar 1e-6
     (worst case 1.30e-08 — see C2). ✓
   - Budget B = 0.50578363 recorded in the console BEFORE the first
     perturbed forward. ✓
   - 50 forwards (10 base + 40 arm), exit 0. ✓
   - Component norm audit: `norm_audit` true on all 10 items (40/40
     components). ✓
   - Sensing-discipline assert: ops = {exact-jvp, exact-vjp}; zero
     finite-difference terms (console + worksheet). ✓
   - Correction-rule pin: single frozen §3.5 rule, `rule_id_ok` true on all
     10 items. ✓
   - Prompt ids: the 10 canonical EXP107 ids, verbatim, matching the
     decision set. ✓

6. **Raw-artifact hashes:**
   - `exp129_per_item.json` → `14a566…83fee` — **matches on disk** ✓
   - `exp129_vectors.npz` → `e3d869…13773e` — **matches on disk** ✓
   - `exp129_worksheet.json` → report records `ec3b68…6673c0a`; on-disk
     `ad7e01…7e6c1` — **MISMATCH, explained (C1)**
   - `exp129_console.log` → report records `702227…d7d5470`; on-disk
     `45dd17…c64bf` — **MISMATCH, explained (C1)**

7. **Ambiguity notes (executor-disclosed, adjudicated):**
   - **Readout site.** §3.1's "(post-final-LayerNorm)" parenthetical
     contradicts the protocol's own apparatus: v̂₁ is EXP127's pre-norm
     propagator vector, the deflated recurrence is on MᵀM, and the
     correction rule is ŵ = Mᵀd̂₁/‖Mᵀd̂₁‖. A post-norm d₁ would sit outside
     M's codomain and make the adjoint rule ill-defined under the
     protocol's formulas — the pre-norm (EXP127-map) reading is the only
     executable one. **Adjudicated: the executor's reading is correct; the
     parenthetical is a drafting slip.** Verdict-immaterial (the KILL does
     not depend on the readout choice).
   - **Flips recorded as "not measured."** The protocol says flips are
     "recorded as [OBSERVATION] only"; the executor recorded "not
     measured," justified by the absence of any licensed decision-readout
     channel (logits barred §6; generation/probe/head barred §3.7; no
     residual decision channel licensed). Defensible, disclosed, and
     verdict-immaterial — no bar reads flips. Noted, not a defect.

8. **Honest frame:** control-efficiency, not capability; capability
   scoreboard at zero; the KILL is recorded as adverse evidence against
   the GPU closed-loop line's premise without unlicensing signed bundles.
   ✓

## Caveats (documentation-only, non-verdict-bearing)

- **C1 — hash-pin chain for two artifacts.** The report's worksheet and
  console-log SHA-256 values are *pre-finalization* pins: both files
  received post-verdict appends ("worksheet finalized and re-validated"
  + verdict section; the final "median r … / VERDICT: KILL / ==
  EXP129 execution complete ==" console lines) *after* the pin node.
  The pinned byte states no longer exist on disk, so those two pins
  cannot be independently re-verified from current disk bytes. The
  verdict-determining artifact (`exp129_per_item.json`) is exactly
  pinned and intact, and the console record shows the pin preceded the
  decision-statistic computation (Law #9 ordering intact). Lesson for
  future lanes: write the verdict into a *new* file, never append to
  pinned artifacts.
- **C2 — v̂₂ orthogonality margin overstated.** The report claims "all 10
  |v̂₂ᵀv̂₁| < 1.1e-08"; the console itself shows 1.164e-08 for prompt 9
  and my recompute gives max 1.30e-08. The apparatus-void bar is 1e-6,
  so the guard passes by ~77× — report wording only.
- **C3 — descriptive precision.** The report's "r ∈ [0.9998, 1.0002]" is
  4dp-rounded (exact range 0.9997644–1.0002242), and "equals the
  single-shot arm's to four decimal places" is loose (max |r−1| = 2.2e-4).
  Precision only; the verdict bar sits at 1.2.
- **C4 (note).** Flips recorded as "not measured" rather than as an
  observation — see §7; disclosed, justified, no bar affected.

## Bottom line

The KILL is exact: feedback re-targeting buys nothing per unit norm —
median r = 1.000005, the loop's second act is the open-loop single shot
re-derived by the adjoint. A real null, not an apparatus failure: every
breaking-point guard passed and the falsification tree ran to the decision
node. The caveats touch documentation precision, not the verdict.

**Next in the launch chain:** scoreboard sync, then commit-prep for the
EXP129 wave. No push — founder token still pending.
