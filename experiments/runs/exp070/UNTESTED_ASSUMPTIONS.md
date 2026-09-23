# EXP070 Untested Assumptions Inventory

**Rule:** anything the bundle or protocol assumes but no tool in this session has
verified. The top of this file lists the assumptions most likely to bite on
Kaggle; the rest are ordered by execution phase.

## Top risks on Kaggle (highest expected cost if wrong)

1. **The +12pp worth-chasing bar is acknowledged arbitrary (protocol §7.3).**
   The evaluator runs sensitivity bands at +12/+16/+20pp, but the branch routing
   itself is gated on +12pp. If the true selection prize is real but sits at, e.g.,
   +8pp, the tree routes to (d) — "signal exists, below the bar" — and EXP068 is
   not justified even though a real effect exists. The bar is a judgment call, not
   a measurement.
2. **Template matching assumes support and test items share index patterns.**
   The probe map matches on (hop, index-pattern) and requires ≥3 vocabulary-matched
   probe items per instance. If the EXP065 item-construction code produced a test
   item whose index pattern never appears in the support set, it is excluded; if
   ≥11 such instances exist, N_final < 50 and the run halts (branch (a)) with no
   ceiling measurement. The re-implementation of the EXP065 items in `run_exp070.py`
   (including the exact i>=8 / i>=7 reversal splits) has never been executed, so a
   construction bug here is the single most likely cause of an (a) halt.
3. **Probe items are a labeled analog of the loop's per-instance views — the
   analogy is asserted, not validated (§3.2).** If the probe carries signal but the
   signal is uncorrelated with selection quality on test items, the oracle ceiling
   can be exceeded by the real loop (false kill) or the probe can be noisy and
   understate the ceiling (false (c2)). There is no transferability measurement in
   EXP070 itself.
4. **The G2-ring formula `normalize(v + ε)` vs the loop spec.**
   Protocol §3.1 notes σ=0.1 in d=768 gives E[cos]≈0.34 — a ~70° spray, "closer to
   repeated random search with selection than to fine hill-climbing". The pool is
   therefore what it is: 8 sprays around 8 bootstrap draws plus the incumbent.
   The A-pool family (protocol §7) is explicitly excluded; any EXP070 kill says
   nothing about it.
5. **Deterministic-algorithms availability on the Kaggle T4 image.**
   The runner calls `torch.use_deterministic_algorithms(True)` inside try/except
   and logs a warning if unavailable; non-deterministic ops would silently break
   exact bitwise reproducibility while leaving all statistical conclusions valid.

## Construction-phase assumptions

6. The tokenizer's encoding of `" " + EntityName` is a single token for every
   entity (Planetary/Elemental and support vocabularies). If any name splits into
   multiple tokens, `tokenizer.encode(t_tok_str)[0]` silently uses the wrong token
   and the C7 bridge baseline for that item is meaningless. (Same latent issue
   existed in EXP065/066; the replication gate (g) in §8 is the tripwire.)
7. `model.embed_out` exists with that exact attribute name in the installed
   transformers version (make_bridge_vec). If transformers renamed the output
   head, C7 crashes loudly — a fatal, not a silent error.
8. `model.gpt_neox.layers[TARGET_LAYER]` and `hidden_states[TARGET_LAYER + 1]`
   indexing hold in the installed transformers version (same convention as
   EXP065/066/067, but pinned versions were not tested locally).
9. Bootstrap resample indices drawn with `np.random.default_rng(7001)` match the
   loop spec's "bootstrap-resampled contrast aggregations" only procedurally —
   there is no reference implementation to diff against; the formula was read
   from the spec text.
10. Dirichlet(1,…,1) draws (seed 7002) are correct per loop spec §2.1 — same
    caveat as (9): spec-read, not reference-compared.

## Probe-gate assumptions

11. The 25% H_sel floor and the r_pb one-sided p<0.05 are [ARBITRARY] protocol
    parameters; the runner implements them verbatim. A different floor would
    reclassify some (c1)/(c2) boundary cases.
12. `scipy.stats.pointbiserialr` returns NaN only under zero variance; the runner
    also guards `np.var(probe_margins)==0` defensively before calling it.
13. The tie-break generator (`torch.Generator().manual_seed(7005)`) draws in
    instance order; archiving the draw index per instance preserves auditability
    even if the stream position is questioned.

## Evaluation-phase assumptions

14. The evaluator is pure: it reads McNemar p, (b,c), ΔM, the probe gate, and
    halt flags from `exp070_results.json` and computes no new statistics. If the
    runner wrote a wrong number, the evaluator rules on the wrong number —
    the (g) consistency check (C2 ΔM=0 with b=c=0 while C7 rescues) is the only
    tripwire, and it is informational, not gating.
15. Historical dry-run of the evaluator on EXP065/066 numbers is a schema
    exercise only: the (b,c,p) cells were computed under EXP065/066's pairing
    conventions, not EXP070's C3-vs-C2 pairing; routing the cell is a logic
    test, not a re-analysis.

## Compute assumptions

16. ≈5,520 forward passes / ≈45 min on T4 is the protocol's conservative basis;
    actual wall-clock on Kaggle's T4 x2 (shared, throttled) is unmeasured.
17. `exp070_vectors.pt` (~17×768 float32 + archives) fits Kaggle's disk and
    downloads — unmeasured but far below the 20 GB typical limit.
