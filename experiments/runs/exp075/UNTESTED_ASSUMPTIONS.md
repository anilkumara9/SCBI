# EXP075 UNTESTED ASSUMPTIONS

Honest listing of everything the bundle assumes but could not verify locally
(no GPU/torch on this machine). The runner script and evaluator are
syntax-validated and the decision-tree evaluator is branch-tested; everything
below is a runtime assumption awaiting real execution.

## A. Tokenization (highest-risk untested item)

1. **Entity tokens assumed single-token.** The runner takes
   `tokenizer(" " + entity).input_ids[0]` — i.e., the *first* subtoken — and
   treats it as the entity's embedding. Multi-subtoken entities (e.g. "Ganges"
   may or may not be single-token in Pythia's BPE; hyphenated or non-English
   entities are riskier) are **silently truncated to their first subtoken**.
   - Impact: pairs would still run (no crash), but S and the bridge would be
     built on first-subtoken embeddings rather than entity embeddings — a
     silent semantic drift that would corrupt the causal interpretation.
   - Mitigation: the runner logs per-entity tokenization (id + single-token
     flag) in the run log; the runner **aborts early if ANY support or test
     entity is multi-token** (F2 guard, immediately after tokenizer load,
     before any forward pass and before S construction — implemented
     2026-09-23 per the bundle review's F2; the claim is code-true, not
     aspirational). Multi-token entities are never silently included.
   - Adversarial review should confirm this early-abort is the right call
     (alternative: multi-token averaging, which the spec does not license).

2. **Leading-space convention.** `" " + entity` assumes the standard
   word-internal (non-BOS) tokenization for these slot terms. If the template
   context produces a different tokenization boundary (e.g. the template ends
   with a character that merges differently), the support embeddings and the
   benchmark's logits could read different ids for the "same" entity.
   - The runner logs the raw tokenized id with the log for every entity, and
     the benchmark re-tokenizes the *exact same strings*, so support/test
     consistency holds by construction; only the interpretation ("this is the
     entity's canonical embedding") could drift.

## B. Benchmark equivalence

3. **EXP065/066 construction fidelity — VERIFIED (not assumed).** The runner's
   support and benchmark constructions were diffed item-by-item against
   `experiments/scripts/run_exp066_pythia410m_replication.py` (the historical
   EXP066 procedure) during the bundle's Law #14 review (2026-09-23, U4/F4)
   and found item-identical: support entity lists, `triples_indices`/`quads_indices`
   (all 15+15), rel/neu prompt templates, `q_opts` parity (`i % 2 == 0`),
   `v_hat_k = normalize(mean(normalize(delta_h)))`, `B_agg = normalize(Σ v_hat_k)`,
   `B_perp` seed 9876, `B_wrong` Paris-capital prompts,
   `hidden_states[target_layer+1]` indexing; benchmark entity lists, index
   lists, templates, `target_first` parity, `is_rev` alternation,
   target/foil assignment (instance IDs and metadata fields differ only).
   - Residual: item-identity holds for the *construction procedure*; the
     historical *results* comparison still rests on the (d)-rider baselines.
   - Mitigation (unchanged): historical baseline accuracies (68.33%, 56.67%)
     are carried as fields for the branch-(d) rider, not used as gates.

## C. Intervention mechanics

4. **Hook placement on the residual stream.** The runner registers a forward
   hook on `model.gpt_neox.layers[20]` adding δ to `module_out[0]`
   (residual-stream activations) — the same placement as EXP065/066's harness.
   Whether this is the causally right site for a *direction* claim is not
   testable here; EXP065/066 used the same site, so cross-experiment
   comparability is preserved by construction.
5. **KL-divergence comparability.** C4 renormalizes `P_S v̂` back to unit norm,
   injecting δ at the same α as C3. If e is near the 0.10 bar, the retained
   signal is amplified up to 10× its natural scale, so C4's KL is not
   commensurable with C3's KL. The KL guardrail is therefore **exploratory
   only** (reported per condition, not a gate). Interpretation of a C4 rescue
   must carry the amplification caveat (protocol §3.4; audit Finding 4).
6. **No CPU fallback for real runs.** The runner hard-aborts without CUDA.
   An intentional `--allow-cpu` escape hatch exists (mirroring EXP070's
   bundle) but is strongly discouraged; a CPU run would be too slow for the
   registered scope and risks timeout artifacts. Adversarial review may
   decide to remove the override entirely.

## D. Budget and determinism

7. **Forward-pass budget.** The signed spec budgets 420 condition forwards, but
   that figure omits the 300 support forwards that §3.1's support procedure
   requires (150 pairs × rel/neu). The true total is ≈ **1,082** model
   forwards: 300 (support) + 2 (B_wrong) + 60 (baseline) + 720 (6 conditions ×
   60 items × base+modified for KL). The extra 360 KL-duplicate forwards do
   not change any estimand — the unintervened comparator is the correct one
   for the KL — and ≈1,082 short forwards on a T4 (≈10–20 min) is still far
   inside free-tier quota. The excess is therefore acceptable; the figures
   stated elsewhere in this bundle have been corrected to ≈1,080
   (2026-09-23, bundle review F3/U1). Caching the baseline forward is a
   permitted optimization, not a requirement.
8. **Determinism claims.** Seeds are `SEED_TORCH=SEED_NUMPY=20260923` (harness;
   restored after B_perp) and `SEED_B_PERP=9876` (B_perp construction only);
   thin-QR is deterministic (no seed needed); `torch.use_deterministic_algorithms(True)`
   is set where supported; the artifact logs all seeds. Full bitwise
   reproducibility on GPU is not guaranteed (CUDA kernels,
   `torch.backends.cudnn`), but no claim in the decision tree depends on
   bitwise determinism — only on the published seeds being run.
9. **Registered-hash sanity warning.** The runner compares the loaded model's
   SHA-256 against the EXP067 §2 registered value but does NOT abort on
   mismatch (floats are non-reproducible; a mismatch is a warning logged for
   diagnosis). A model-hash mismatch coinciding with branch (c) would be the
   first diagnostic lead per branch (c)'s ruling text.

## E. Math the bundle trusts

10. **Rank-guard threshold.** `σ_min/σ_max > 1e-6` is a judgment call, not a
    theorem. A subspace could pass the guard yet still be effectively
    lower-dimensional in a way that distorts e (rank-guard caveat, §3.1).
    The full singular-value spectrum is archived so any threshold can be
    audited post hoc.
11. **Energy-ratio interpretation.** `e = ‖P_S v̂‖²` measures the *fraction of
    the bridge's norm* in S, not the fraction of the bridge's *causal
    relevance*. A small e kills nothing; a large e licenses nothing beyond
    the non-vacuity the protocol claims.
12. **McNemar on paired rescues/corruptions.** The exact two-sided
    conditional binomial p on (b, c) follows the program's standard
    (EXP065/066 audit). It conditions on discordant count; with tiny (b+c)
    it has low power — a known, pre-registered property, not a fix.

## F. No-peeking discipline — whitelist substitution (disclosed deviation)

13. **Ordering + signature stands in for the spec's path whitelist** (bundle
    review U3/F7, 2026-09-23). Protocol §3.1's path whitelist presupposes
    support artifacts on disk ("support artifact directories"). This runner
    reads **zero files** — support deltas are generated in-script — so a
    filesystem whitelist is vacuous. The no-peeking invariant is instead
    achieved more strongly: `build_subspace_S()` is called **before the
    benchmark exists** (ordering — S is frozen at §3.1, the benchmark is built
    after), receives **only** the support contrast deltas (signature-enforced —
    test items are not in scope at call time), and the entity domains are
    structurally disjoint (person names vs planets/elements — verified
    against the historical EXP066 script, see item 3). This substitution is a
    disclosed, reasoned deviation from the spec's letter that preserves its
    intent (m1); it is the disclosure the runner's docstring references.
