# Law #14 Independent Review — EXP133 Amendment C (breaking point (d) tolerance recalibration)

**Lane:** independent Law #14 reviewer. **LOG-4805** (CEO pre-assigned). **Date:** 2026-09-30.
**$0 CPU, paper-only.** Read-only on signed protocols, weights, and artifacts. No model runs,
no GPU contact, no commits, no pushes, no spend, no publish, no dispatch, no experiment
number minted, no execution licensed.

**Artifact reviewed (exact version):**
`~/workspace/SCBI/research/prereg/EXP133_AMENDMENT_C_2026-09-30.md` — DRAFT amendment
covering ONLY breaking point (d) (norm-budget equality tolerance 1e-6 → 1e-4 relative).

**Review-only fence:** I did not author the amendment or the pre-reg. I edit nothing under
review, apply no repairs, license nothing, advance no pipeline. My only writes are this
review file and the single LOG-4805 research-log entry.

**Independence confirmed.** The amendment was authored by the LOG-4804 draft lane; the
signed pre-reg by the LOG-4790 strategy worker. I authored neither.

---

## §0 — Context verified

- LOG-4803 (EXP133 re-execution): APPARATUS-VOID on breaking point (d). CPU-recomputed
  B = 0.50578363 vs verbatim LOG-4766 B = 0.50578119; rel diff **4.832e-06 > 1e-6** →
  void before any injection forward. Diagnostic: identical B with and without
  `torch.use_deterministic_algorithms(True)`; backbone/bench/B_agg pins bit-exact.
  Conclusion recorded there: tolerance defect, not drift.
- The signed pre-reg's §0(d) (verified verbatim in
  `research/prereg/EXP_PREREG_GEOSTEER_MULTISTEP_2026-09-30.md` line 18) reads:
  "the executor independently recomputes B = 0.01 × median ‖y_{20,last}‖ per the EXP129
  FIX-2 rule and asserts equality with 0.50578119 **within 1e-6 relative**" — exactly
  the clause the amendment strikes. The amendment's characterization of the original
  text is accurate; no strawman.

---

## §1 — Checklist findings

**1. Narrowness — PASS.** The amendment's operative change is confined to §0(d)'s
equality tolerance plus the §5 checklist paragraph. §4's everything-unchanged list
(decision table, hypothesis, budget, breaking points (a), (b)-as-amended-by-B, (c),
(e), (f), (g), arms, readout, ĉ_geo definition, records discipline) was checked
against the signed pre-reg's structure — complete and accurate. No science changes,
no new quantities, no re-interpretation of prior verdicts. Laws #4/#5 clean.

**2. Justification honesty — PASS.** The 1e-4 calibration is genuinely supported, not a
convenience relaxation:
- The noise floor (4.832e-06) is a *measured* value from LOG-4803's diagnostic, not an
  estimate — reproduced with and without deterministic algorithms, with all other
  pins bit-exact, isolating cross-device fp numerics (cuBLAS/cuDNN vs CPU reduction
  ordering across ~20 blocks) as the cause.
- 1e-4 sits >20× above the measured noise floor — a real margin, not a rounding-up.
- The alternative (keeping 1e-6) is *demonstrated unsatisfiable* on CPU: the LOG-4803
  run voided on it with zero drift present. Keeping it would guarantee a repeat void.

**3. Dose-fence integrity — PASS.** The tolerance change cannot affect the injected dose:
- The signed pre-reg mandates the verbatim B = 0.50578119 injected per Law #2
  ("NOT recomputed as a new number") — the amendment explicitly preserves this
  (§2 point 3).
- The per-step tangent audits (‖t_k‖ = B/5 ± 1e-6, ∑‖t_k‖ = B ± 1e-6) are unchanged,
  and — critically — were *demonstrated satisfiable on CPU*: LOG-4803's smoke test
  passed 25/25 tangent audits at α±1e-6. The amendment does not ask the reader to take
  satisfiability on faith; it was reality-checked, which is exactly the discipline §5
  now requires.
- The relaxed tolerance gates only the drift-detector check, never the dose.

**4. Drift-detection power — PASS.** 1e-4 relative = 0.01%. A wrong bench (different
prompts) shifts the 10-prompt median ‖y_{20,last}‖ at the percent level or worse —
hidden-state norms vary across prompts by far more than 0.01%. A wrong backbone
(different weights) shifts norms massively. The amendment's "orders of magnitude more
than 1e-4" claim is sound: 1e-4 remains orders of magnitude below any realistic drift
signal while sitting >20× above measured noise. The check retains its function.

**5. §5 checklist addition — PASS.** Well-formed and correctly scoped: requires numerical
breaking-point tolerances to cite a measured bound or an explicit margin-over-noise
argument, "never a round number chosen for tidiness." Cites both EXP133 voids as the
motivating defect class. This is the right systemic fix — it would have caught both
the (b) artifact-contents defect (had the inventory clause existed) and this (d)
tolerance defect at review time.

**6. Status honesty — PASS.** "DRAFT — licenses nothing" stated at the top; the draft
repeatedly states it licenses no execution and that re-execution needs fresh CEO
clearance. No hidden licensing language found.

**Law #4 (no silent hypothesis shift) — CLEAN.** The tolerance governs run/no-run only;
it cannot bias any §2 verdict branch. A looser drift-detector does not make KILL,
CONTINUE, or PIVOT easier to obtain — those are decided by measured ΔM/ĉ against
registered bars. No Law #2/#3/#9 issues: every number is cited to LOG-4803/LOG-4766,
no invented results, no metric changes.

---

## §2 — Verdict

**SIGN.** The amendment is narrow, honestly justified by measured evidence, preserves
the dose fence intact, retains drift-detection power, and adds the correct systemic
checklist fix. No blocking findings. No advisories — §3's verification discipline
(recording both B values + rel diff pre-forward) already covers auditability.

**Disposition:** Amendment C approved as drafted. EXP133 may re-execute under the signed
pre-reg as amended by Amendments B and C, upon fresh CEO clearance.
