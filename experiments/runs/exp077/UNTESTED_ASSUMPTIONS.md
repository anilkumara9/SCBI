# EXP077 UNTESTED_ASSUMPTIONS.md

Assumptions the bundle relies on that were NOT (or not fully) tested at
bundle-construction time, with the reason and the mitigation for each.
Honest ledger: what the smoke test covers, what it cannot, and what only the
GPU run will reveal.

## Covered by the 39/39 evaluator test suite (CPU, no model)
- T1. Holm step-down (strict inequality, boundary 0.0125, the 7-0/A-headroom
      caveat from protocol §6).
- T2. Radial shape classifier: singleton {0.25} / {2.0} / {0.25,0.5} /
      {1.0,2.0} / all-alpha upper sets; Holm-rejected-but-negative-delta_m
      ignored; empty family.
- T3. All five branches fire on synthetic inputs: (d) for each of the four
      halt outcomes; (r) rescue + corruption variants, strict p<0.05 boundary,
      precedence over (a); (a)(i) angular+control, (a)(ii) both non-upper
      variants, (a)(iii) offset; (b)(i) angular-line, (b)(ii) upper-set
      variants; (c) flat-zero and attempts-alone; unclassified malformed.
- T4. Precedence: (d) > (r) > (a) > (b) > (c) verified pairwise.
- T5. `report()` renders the branch name and the matching LICENSE fragment;
      `load_results()` normalizes complete / malformed / halt payloads.

## Covered by the CPU smoke run (real model + tokenizer, --allow-cpu)
- S1. `py_compile` of all three files.
- S2. F2 single-token guard against the REAL pythia-410m tokenizer (all 25
      support + 10 benchmark entities).
- S3. Model load in float32; layer-20 hook injection path executes.
- S4. Support construction (300 contrast pairs) → v_hat / mu / v_hat^c built;
      continuity assertion evaluated on real data.
- S5. Cone/control construction with pinned seeds: |cos(r, v_hat)| < 0.5
      build assert and cos(u_j, v_hat) == cos(phi_j) exact checks on real
      vectors; injection-norm guard over all 22 static vectors.
- S6. Benchmark construction + anti-cheat assert; C1 executes and the
      headroom gate evaluates; C8 bridge arm executes and the bridge gate
      evaluates (gates may HALT on CPU -- a halt is still a valid smoke
      signal for the gate code path).
- S7. Runner reaches at least the first condition-evaluation forward passes
      (target: C1 + C8; stretch: first radial arm + first C9 items).

## NOT covered before the GPU run
- U1. **GPU-path device consistency.** The smoke runs on CPU; CPU/CUDA
      placement bugs (the EXP078 LOG-116 class) are invisible to it. Mitigation:
      all cone/control/bridge vectors are built on CPU and moved with
      `.to(device)` inside `eval_item`; this pattern was verified statically
      against the LOG-116 fix, and the bundle review must re-check every
      tensor that crosses the CPU/GPU boundary.
- U2. **Full 1,740-forward completion within a Kaggle session.** The CPU smoke
      cannot finish in reasonable time; the worst-case budget was computed
      analytically (§10: 300 support + 480 (C1–C8) + 480 (C9) + 480 (C10) =
      1,740) and the EXP078 run (similar per-forward cost) completed in 32s
      on 2×T4, so the budget is credible but unmeasured for this exact
      condition mix. **Budget note for the Law #14 review:** the runner spends
      2 additional forwards building the B_wrong direction (one Paris-capital
      contrast pair, EXP066 procedure), for an actual worst case of 1,742 —
      0.1% over the registered 1,740 bound. Immaterial to the free-tier quota
      conclusion, but the arithmetic is disclosed here rather than rounded
      into the bound.
- U3. **Deterministic reproducibility across runs.** Seeds are pinned and
      `torch.use_deterministic_algorithms(True)` is requested, but
      bit-identical GPU re-runs are not asserted (only the SHA pre/post
      backbone guard and the seeded construction are).
- U4. **The |cos(r, v_hat)| < 0.5 build assert outcome.** It is a deterministic
      function of pinned seed 7702 and the real support data; it CANNOT be
      verified without the real model. If it fails at runtime the run FATALs
      by design (protocol §3.4) -- that failure mode is itself informative
      (the seed is bad) and requires re-registration, not a silent re-seed.
- U5. **Whether the gates pass.** Headroom [40%,70%], bridge validity, and the
      continuity floor are empirical; the smoke may halt at any of them. A
      halt validates the gate code path but leaves the full condition battery
      unexecuted -- which is the correct pre-registered behavior, not a gap.
- U6. **Support entity set provenance.** The spec says "the archived support
      set" without enumerating entities; we use the F2-corrected EXP078 set
      (documented as a conservative reading in the runner docstring). This is
      a protocol-reading choice, not a tested fact; the Law #14 bundle review
      must confirm or escalate it.
- U7. **C8 construction.** The spec pins C8 to EXP066's `make_bridge_vec`
      (unembedding-space direction normalize(E[target]-E[foil]), alpha=0.5;
      ASSUMPTION A-bridge-space). The bundle implements this verbatim via
      `get_output_embeddings()`. NOTE (corrected during smoke, 2026-09-23):
      the first bundle draft implemented C8 as a per-item v_k steering vector
      -- the wrong control, caught because the CPU smoke's bridge gate failed
      with delta_m exactly 0. Fixed to the spec'd construction before any GPU
      run; no GPU result was ever produced with the wrong C8.
- U8. **Kaggle environment drift.** The bundle pins lower bounds
      (torch>=2.2, transformers>=4.44, numpy>=1.26, scipy>=1.13), not exact
      versions; a future image could change tokenizer/model-loading behavior.
      The runner logs an environment manifest into the results JSON so any
      drift is detectable post-hoc.
