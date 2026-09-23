# Law #14 Adversarial Bundle Review — EXP077 Execution Bundle

**Date:** 2026-09-23
**Reviewer role:** Adversarial Reviewer (Law #14)
**Subject:** `experiments/runs/exp077/` (runner, evaluator, tests, RUNBOOK, UNTESTED_ASSUMPTIONS)
+ Kaggle zip `~/workspace/your_files/kaggle/exp077_bundle.zip`
**Signed protocol:** `experiments/protocols/EXP077_CONE_VS_LINE_PREREG_SPEC.md` (PRE-REGISTERED, SIGN 2026-09-23)
**History read:** LOG-102/103/106 (pre-registration review + fixes + re-verification),
LOG-108/109/114/116 (mechanical lessons), LOG-111 (F2 doctrine), LOG-118/123 (build + smoke)

## Verdict: REVISE — 3 MAJOR findings. NOT cleared for execution.

The bundle is well-built and the smoke discipline is exemplary, but line-by-line
comparison against the signed spec surfaced three protocol-fidelity breaches, one of
which inverts a decision-tree trigger. All three fixes are mechanical (match the code
to the signed spec); none requires a new experiment number. A diff re-verification
is required after fixes before any GPU launch.

---

## MAJOR-1: μ normalized before subtraction — C6 (offset arm) deviates from §3.2

**Spec (§3.2):** `μ = (1/300)Σ_{x ∈ support} h(x)`, `v̂^c_k = normalize(v̂_k − μ)`,
`v̂^c = normalize(Σ_k v̂^c_k)`. No normalization of μ anywhere.

**Runner** (`run_exp077.py`, `build_candidate_directions`):
```python
mu = torch.stack(h_all, dim=0).mean(dim=0)          # [d]
mu = mu / (torch.norm(mu) + 1e-12)                  # unit for stability
...
diff = v_hats[k] - mu
```
`normalize(v̂_k − μ̂)` ≠ `normalize(v̂_k − μ)` whenever `‖μ‖ ≠ 1` (residual-stream
means are not unit-norm). The "unit for stability" normalization is the builder's
own invention, changes the registered intervention direction, and changes the
logged "amplification" quantity (spec: amplification of renormalizing `(v̂_k − μ)`;
runner logs `‖v̂_k − μ̂‖`). C6 feeds branch (a)(iii) ("offset C6 vs C1: p<0.05,
ΔM>0") — a wrong v̂^c means the trigger tests a different intervention than
registered.

**Fix:** delete the `mu = mu / (torch.norm(mu) + 1e-12)` line. One line, zero
scientific content — restore the registered formula.

## MAJOR-2: angular/control endpoints are the wrong statistical comparisons — the (a)(i) conjunct is inverted

**Spec (§3.6):** rescue indicators `L(x)` (line/C4), `K(x)` (cone/C9), `R(x)`
(control/C10), each requiring C1-incorrect. Discordant counts:
`angular (b,c) = (Σ K(x)(1−L(x)), Σ L(x)(1−K(x)))` — **cone vs LINE**;
`control (b2,c2) = (Σ K(x)(1−R(x)), Σ R(x)(1−K(x)))` — **cone vs CONTROL**.
§6: "Primary (confirmatory): angular cone-vs-line — McNemar exact two-sided on
(b, c); conjunct: cone-vs-control McNemar exact two-sided on (b2, c2)."
§8 (a)(i): "angular: McNemar p<0.05, b>c, **and** control McNemar p2<0.05, b2>c2".

**Runner** (results assembly): `angular = paired_stats(base_correct, cone_correct)`
= **cone vs BASELINE**; `control = paired_stats(base_correct, ctrl_correct)` =
**control vs BASELINE**. The §3.6 indicators (`L_ind`, `K_ind`, `R_ind`) are
computed correctly but never used for the endpoints.

**Evaluator** (`classify`): `(a)(i)` fires iff `ang["sig_pos"] and ctrl["sig_pos"]`
— i.e., iff the cone beats **baseline** AND the **random control beats baseline**.
That is the exact inverse of the registered logic. Spec §3.4 [INTERPRETATION]:
"if the v̂-cone beats the line but not the control, the wins are attempts-alone,
not geometry." Under the current code, the attempts-alone pattern (control also
rescues) is a CONE-WINS conjunct; data the spec routes to (c) attempts-alone
would be ruled (a). **Decision-flipping.** The (b)(i) trigger is likewise wrong:
spec = line-beats-cone (`c>b` on K-vs-L); code = cone-corrupts-vs-baseline. The
(c) attempts-alone fallback ("angular sig but control failed") inherits the wrong
comparisons, and the 39/39 tests encode the inverted logic
(`test_evaluate_exp077.py`: "(a)(i): angular + control both sig positive" with
control b=9,c=0 asserts the inversion).

**Fix:** compute the §3.6 discordant counts from the already-correct indicator
lists — `(b,c)` from `(K_ind, L_ind)`, `(b2,c2)` from `(K_ind, R_ind)` — via the
existing McNemar helper, store those as `"angular"`/`"control"`, correct the
(b)(i) message ("line beats cone"), and update the tests to the registered
comparisons. The evaluator's precedence/Holm/shape logic is otherwise correct
(verified: strict p<0.05, Holm step-down, upper-set classifier, (d)>(r)>(a)>(b)>(c)).

## MAJOR-3: benchmark is a novel construction, not the EXP065-identical suite (§5, Law #9)

**Spec (§5):** "**Benchmark:** the identical N=60 Planetary/Elemental 2-hop/3-hop
suite from EXP065 (same items, same premise permutations). No new benchmark
construction (Law #9)."

**Runner** (benchmark section): builds 60 items procedurally — Anglo support
entities as ranked subjects, planet/element entities as novel nouns, templates
`"{A} visited {ent}... Question: {ent} is larger than what? {A} or {C}?"` /
`"{A} forged {ent}... heavier than what?"`, with per-item `RandomState(6000+i)`
permutations. This is not the EXP065 suite: the historical scripts
(`run_exp065_temporary_coordinate_alignment.py`, `run_exp066_pythia410m_replication.py`)
use planet/element entities as the ranked subjects with the
`"Premise: {A} outranks {B}... Question: Who is higher in rank?"` templates (the
EXP078 runner reproduces that construction verbatim). The EXP077 suite differs in
template, subject entities, and question — and reuses support-set (Anglo)
entities as subjects, which the registered suite does not. LOG-118's
"EXP065-identical" label is incorrect; the runner docstring carries no
conservative-reading disclosure for the benchmark (unlike the support set and
C8). The gate calibrations (§5: headroom [40%,70%], bridge gate vs EXP066's
+13.33pp, historical baselines 0.6833/0.5667) are all anchored to the registered
suite.

**Fix:** replace the benchmark builder with the EXP065/066-identical construction
(port from `experiments/runs/exp078/run_exp078.py` §2, which follows the
historical script). No new experiment number — this restores the registered
design; the current construction is the deviation.

---

## U6 adjudication: (a) mechanical correction — NOT a Law #4 design change

The runner uses the F2-corrected EXP078 entity set where the spec says "the
archived support set." This is a mechanical correction of the same design:

1. The spec defines the set **procedurally and thematically** (§3.1: "30 contrast
   pairs per vocabulary × 5 vocabularies — Anglo, Biblical, Greek, Roman, Modern;
   150 rel + 150 neu presentations, exactly per
   `theory/BOUNDARY_CLAIM_FORMALIZATION.md` §2"), not by enumerated strings.
2. The byte-identical historical strings are **unexecutable** without silent
   first-subtoken truncation — banned program-wide as a Law #2-adjacent
   falsehood (LOG-100 F2; LOG-111). Reproducing them would be a protocol
   violation, not fidelity.
3. The spec's own identity criterion is **directional, not lexical**: the §5
   continuity assertion ("we are not testing the direction the null was
   established on") and A-reconstruction ("reproduces the EXP066 contrast
   directions up to the §5 continuity floor"). The smoke measured mean
   cos(v̂_1,v̂_k) = 0.7162 ≥ 0.50 — the spec's criterion passes.
4. The runner discloses the reading in its docstring and re-verifies it at
   runtime with the F2 guard (loud abort, never silent alteration).

The F2 guard itself is a conservative addition the spec does not explicitly
mandate; it can only halt loudly before any measurement, so it cannot silently
alter the design. Acceptable as documented.

## U1 device-placement audit: CLEAN

Statically traced every tensor crossing. All injection vectors (radial arms,
C6/C7/C8, cone `u_j`, control `q_j`) are CPU-built and pass through the single
choke point `vec = injection.to(device)` inside `eval_item` before the hook
(`x[:, -1, :] = x[:, -1, :] + vec`, both CUDA on GPU). The bridge matrix is
`.detach().cpu()` and moved per-call. Archives are CPU-only. `model.to(device)`
and `torch_dtype=torch.float32` are pinned. No LOG-116-class blind spot exists.
(Kaggle-compat of `model.gpt_neox.layers[20]` is retired by precedent: EXP070's
runner uses the identical accessor and completed on Kaggle's transformers 5.x;
the local smoke ran under transformers 5.17.0.)

## Sanity-hash note: builder's root cause independently VERIFIED

Recomputed on the cached checkpoint: SHA-256 over `state_dict()` with **sorted**
keys = `ec276abe…` (the runner's pre/post value); with **unsorted** insertion
order = `4c242d9a…` (the EXP067 §2 registered value) — exact match. The weights
are byte-identical to the registration environment; the mismatch is purely key
ordering. Δθ=0 binding guard (pre==post) is intact and is the binding check per
the spec. Pre-existing documentation inconsistency (EXP067 §2 text says "sorted
keys" while its value was computed unsorted) is EXP067's to annotate, not
EXP077's to fix — recommend a one-line note in EXP067 §2, no code change.

## Minor findings (non-blocking; fix with the majors)

- **m1:** evaluator `LICENSE_TEXT["r"]` references "EXP079-class re-registration"
  — confusing (EXP079 is the EXP070 probe successor). Reword to the spec's §1.2
  (r) phrasing: "Re-scope under a new pre-registration."
- **m2:** the §10 archive lists "the 8 cone axes w_j and angles φ_j"; the runner
  archives `u_list` (+ `phi_deg` in results) but not `w_j` separately. `w_j` is
  algebraically recoverable (`w_j = (u_j − cosφ_j·v̂)/sinφ_j`), but persist it
  explicitly for Law #13 completeness.
- **m3:** actual worst-case budget is 1,742, not the registered 1,740 (2 extra
  forwards building the B_wrong direction). Disclosed in UNTESTED_ASSUMPTIONS U2;
  immaterial to the free-tier conclusion, but the spec's §9 table should carry a
  footnote or the runner should note it in the log.
- **m4:** transformers 5.17 deprecates `torch_dtype=` (warning only; still
  functional). Consider `dtype=` with a version guard, or leave with the
  warning logged.
- **m5:** `interpretation_notes` in the payload cites "(I2)" for surviving
  variants — the spec's named residual is §11/P5; align the label to avoid
  inventing a new identifier.
- **m6:** RUNBOOK §5's cell block does not pin the evaluator run order
  (results JSON → `evaluate_exp077.py`); it does in §3 — harmless duplication,
  no change needed. Noted for completeness only.

## Verified clean (no findings)

- Conditions C1–C10 match the §4 table (α grid {0.25,0.5,1.0,2.0}; C6/C7 at
  α=1.0; C7 reported-only; C8 = verbatim EXP066 `make_bridge_vec` at α=0.5 via
  `get_output_embeddings()`; C9/C10 best-of-8 at α=1.0).
- Cone construction: φ_j grid, exact `cos(u_j,v̂)==cos φ_j` asserts, min φ_j =
  3.75° > 0, dedicated generator seed 7701; control: seed 7702, `|cos(r,v̂)|<0.5`
  build assert (0.0188 in smoke), identical construction.
- Gates: headroom [40%,70%] inclusive; bridge ΔM>0 AND p<0.05 (strict);
  continuity ≥ 0.50; anti-cheat prompt-identity assert; F1 injection-norm guard
  (22+60 vectors).
- v̂ construction per §3.1 (normalize-of-mean-of-normalized per vocab, then
  normalize-of-sum); μ over 300 presentations; seeds 20260923/7701/7702 with
  dedicated generators; no `D` shadowing (D_ent); no backward pass; pre/post
  hash FATAL on mismatch.
- Evaluator: precedence (d)>(r)>(a)>(b)>(c); (r) two-sided C3-vs-C1;
  Holm-gated S_H with strict p<0.05; radial shape classifier (verified against
  the §8 upper-set definition incl. singleton edge cases); M5.1 `b=c=0 → p=1.0`;
  malformed→unclassified.
- RUNBOOK/UNTESTED_ASSUMPTIONS are honest (U1–U8); the U7 wrong-C8 episode is
  correctly recorded as caught-at-smoke.

## Required before CLEAR FOR EXECUTION

1. Fix MAJOR-1 (delete μ normalization), MAJOR-2 (§3.6 discordant endpoints +
   evaluator messages + tests), MAJOR-3 (EXP065-identical benchmark).
2. Apply minors m1–m5 (m6 needs no change).
3. Re-run: `py_compile`, full evaluator suite (updated tests), CPU smoke to the
   gate path on the real model/tokenizer.
4. Commission a Law #14 **diff re-verification** of exactly these fixes against
   this report before any GPU launch. Do not launch on the current zip
   (`286c9576…`); rebuild it after fixes.

*No results were invented in this review. The CPU-smoke numbers cited (from
LOG-118/123) are mechanical validation only, not scientific results.*
