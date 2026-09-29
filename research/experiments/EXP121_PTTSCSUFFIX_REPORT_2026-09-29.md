# EXP121 run report — H19/PTTSC-SUFFIX (plan text via the suffix channel, placement (A))

**Experiment:** EXP121 · **Hypothesis:** H19 (PTTSC-SUFFIX) · **Execution lane:** LOG-4644 (pre-assigned)
**Pre-registration:** `research/prereg/EXP_PREREG_H19_PTTSCSUFFIX_2026-09-29.md`
(launch chain: Law #14 SIGN-WITH-FIXES LOG-4642 → FIX-1 byte-verified LOG-4643 → CEO launch)
**Status:** $0 CPU. Frozen backbone, Δθ=0. Zero training. No signed protocol modified.
**Run completed:** 2026-09-29T13:12:26Z · wall time 33.7 min

## Verdict

**RUN-INVALID (elicitation-failure gate: n_valid=38 < 48).**

In the pre-registration's exact language (§2): *"RUN-INVALID: any Phase-0 gate (§3.7), pin mismatch, pre-check mismatch, baseline-reproduction failure, or the n_valid gate (§3.8) fires → the apparatus failed; the hypothesis gets no verdict. Not evidence about planning."*

No McNemar table was computed — the falsification tree terminates at the n_valid gate, before any metric is read (Law #9). The planning question is **untested**, not killed, not held, not continued.

## Falsification-tree branch taken (§5)

```
bench provenance + len==60 + schema ............ PASS (pin e91b302f…, 60 items, decomposition holds)
 └─ tokenizer-only [-3:] pre-check (60 items) .. PASS — 60/60 identity (composition licensed)
     └─ backbone LOG-331 pin (pre) ............. PASS — ec276abe3902fab0… == pin
         └─ planner prompts byte-verified ....... PASS — 0/60 mismatches vs EXP113 T2-P2
             └─ Phase 0a (planner transfer) ..... PASS — 10/10 planner-valid
                 └─ Phase 0b (logit slot) ...... PASS — 10/10 valid (identity re-armed on real plan texts)
                     └─ full run ............... 60 gens + 120 forwards, 0 exceptions
                         └─ backbone pin (post)  PASS — ec276abe3902fab0… (Δθ=0)
                             └─ baseline repro . PASS — 60/60 vs EXP112 archived readout
                                 └─ re-read ×2 . PASS — byte-identical
                                     └─ baseline variation .. PASS — distinct=2, minority=27
                                         └─ n_valid ≥ 48 ... FAIL — 38/60 → RUN-INVALID
```

## Apparatus defects (reported first — the EXP119 lesson)

Four defects occurred during this lane; all are disclosed, none touch the verdict logic:

1. **VM reboot killed attempt 1 mid-run** (2026-09-29 ~11:23 UTC; `uptime` confirmed system boot 11:23). The process vanished after the full-run start; no verdict, no metric, and no raw model records had been written (only the tokenizer-only pre-check artifact existed). Clean re-run from scratch; no Law #9 exposure.
2. **TypeError crash on attempt 2** (after 60/60 planner generations): `forward("base", t, context_base(rec_item))` was missing the `rec_item` argument (line 408). The identical latent bug exists in EXP119's script — it never triggered there because EXP119 died at Phase 0b. Fixed (one argument added), verified no other call-site errors, re-ran fresh. No metric had been read.
3. **Record-keeping ordering defect (defect class 2):** the first working script persisted raw artifacts only on the McNemar path — early-exit RUN-INVALID paths (including the n_valid gate) wrote the verdict without persisting raw generation/forward records. Repaired before the final run: `finalize()` now persists + hash-pins ALL raw records on **every** exit path before the verdict is written; a missing/empty artifact forces RUN-INVALID. The final run's artifacts verify below.
4. **finalize self-truncation bug:** the backstop copied the execute script onto itself (`open(path,"w")` truncates before the read), leaving `exp121_execute.py` at 0 bytes. The script was reconstructed from the lane's authored source + the five applied edits and **verified functionally identical to the executed script** by code-object comparison against `__pycache__/exp121_execute.cpython-312.pyc` (compiled from the executed version at 12:38 UTC — all functions' bytecode identical). Corrected sha256: `58f12ba52b93c34422c684b11d9c740025f48daebc95d3a90de55f3a48cc7113`. The `exp121_result.json` `artifact_hashes.execute_script` entry still records the empty file's hash (`e3b0c44…`); the result JSON is left untouched (append-only) and the correction is recorded here.

## Pins (§3.1 — all verified before use)

| Pin | Expected | Observed |
|---|---|---|
| Bench canonical JSON | `e91b302f41f641c74e56957e526efcd4866bac62d134e157defe0a4cdd49e4f5` | match |
| npz | `6cf4a8a726a2b6e4623f57d0287d95879866f77e789bcc3789fb693cf2af6a76` | match |
| embeddings bytes | `9b6e8afb091ba1edbb0311ba1d3414d34a65942c3fdecb4533b69720f2a99123` | match |
| ids bytes | `3669e102222719d66f61daca46ae1ac34e844e398ae433743a5b37bfc5075cb9` | match |
| Backbone (LOG-331), before | `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed` | match |
| Backbone (LOG-331), after | same | match — **Δθ=0 confirmed** |
| Schema | `prompt`/`premise`/`tuple`/`phrasing`/`id`; `prompt == premise + QUESTION_SUFFIX` byte-exact, all 60 | hold |
| BPE single-token | `" "+E1`, `" "+E2` one token each, 120/120; ids match EXP112 worksheet pins | hold |

Environment (Law #13): torch 2.14.0+cpu, transformers 5.17.0, numpy 2.5.3, sklearn 1.9.1; `torch.manual_seed(0)`, numpy seed 0; 2 CPU threads (read back); greedy decoding (`do_sample=False`, `max_new_tokens=160`); `model.eval()` + `torch.no_grad()` around all contact.

## Phase 0-pre — tokenizer-only [-3:] identity pre-check (§3.7)

The composition's license, verified mechanically on all 60 items **before any model contact**, with deterministic placeholder plan blocks. `tokenize(CONTEXT_PLAN)[-3:] == tokenize(CONTEXT_BASE)[-3:]` on **60/60** items. Per-item tail ids are recorded in `exp121_precheck.json` (all `identity: true`). Placement (A) is licensed by this pin — the EXP119 breaking point does not recur: both arms end in the byte-identical `" Question: Who is higher in rank? Answer:"` tail.

## Phase 0a — planner bench-transfer (§3.7)

Probe set {0,1,2,5,6,7,8,9,10,11}: **10/10 planner-valid** (≥2 distinct non-empty outlines; all 10 yielded exactly the pinned extraction). Gate (<8/10 → RUN-INVALID): passed.
Diagnostic (not a gate): content-level recitation vs the marker-stripped T2-P2 exemplars — **10/10 probe items with ≥2 recitations**, reproducing EXP117's and EXP119's finding on this bench. The treatment remains "the T2-P2 plan text as generated" (§7.1.2); outline quality is unmeasured.

## Phase 0b — logit slot with plan insertion (§3.7)

Per probe item: [-3:] identity **re-armed on the real plan texts** (10/10 hold — any single mismatch would have fired RUN-INVALID immediately); G1 per arm ≥ 0.01. **10/10 valid.** Gate (<8/10 → RUN-INVALID): passed.

## Full run (§3.8)

60 fresh planner generations + 60 plan-arm + 60 baseline-arm forwards; **0 exceptions** (gate: >10% → RUN-INVALID). Planner-valid: **60/60** (all items yielded 4 distinct outlines). Baseline-arm G1: 60/60 pass (mass range 0.068–0.568). **Plan-arm G1: 38/60 pass; 22/60 degenerate.**

**The failing piece:** on 22 items the plan-inserted arm drives the summed post-softmax mass on the two pinned entity tokens below the 0.01 bar (observed mass 0.000142–0.008571 — the distribution concentrates elsewhere at the final position), while the baseline arm on the same items never drops below 0.068. Failing items: 15, 17, 19, 21, 23, 26, 27, 28, 38, 43, 46, 48, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59. Per the pinned per-item G1 rule (the per-item translation of H6's `M = mean(p_E1+p_E2) ≥ 0.01` guard, as implemented in the signed EXP119 apparatus), those 22 readouts are degenerate → item invalid.

- G1 phrasing note: the pre-reg's "mean post-softmax mass on (t1,t2) ≥ 0.01" is implemented as the per-item sum ≥ 0.01, matching H6's channel-level `M` definition and EXP119's signed implementation. Under the stricter sum ≥ 0.02 reading, n_valid would be 30/60 — the verdict is invariant (both < 48).
- The 10 Phase-0b probe items all passed G1 in the full run; the pinned probe set was unrepresentative of the bench on this slot behavior — a sampling artifact, not a protocol violation.

**n_valid = 38/60 < 48 → RUN-INVALID (elicitation-failure gate).** A second independent full run reproduced n_valid = 38 exactly (deterministic greedy decoding), confirming the count is not a flake.

Integrity checks: baseline reproduction **60/60** vs EXP112's archived readout column (apparatus drift: none); deterministic re-parse ×2 **byte-identical**; baseline-arm variation distinct=2/minority=27 (gate passed); backbone hash identical before and after (Δθ=0).

## What this RUN-INVALID means (§7.1.5)

Per the pre-registration, a RUN-INVALID at the 48/60 gate is a **boundary finding about pipeline validity** — the plan-inserted logit slot does not preserve the H6 non-degeneracy condition on this bench — not a verdict on the planning hypothesis. H11's question (does plan text change decisions?) remains **untested on the logit channel**: EXP117 died on the generation channel, EXP119 died on tokenization identity, EXP121 dies on plan-arm G1 mass collapse. Three distinct apparatus failure modes; zero decision data.

## Honesty fence (§7.1, binding)

No CONTINUE was reached, so no pipeline is licensed as an adaptive-loop component. Nothing in this run attributes any effect to planning vs additional context tokens (the token-asymmetry confound stands undisclosed-removed: disclosed, not removed). No claim about reasoning, consciousness, capability, or generality is made. Novelty remains N1 — Known Combination.

## Raw artifacts (hash-pinned before the verdict; all verified)

Under `experiments/runs/EXP121_pttscsuffix/out/`:

| Artifact | sha256 |
|---|---|
| `exp121_execute.py` (reconstructed; verified identical to executed via .pyc) | `58f12ba52b93c34422c684b11d9c740025f48daebc95d3a90de55f3a48cc7113` |
| `exp121_generations.json` (60 raw planner generations) | `a28cc25eddcab03057c0910a7801d6fd03833b4580db9a23cbcd41191962b146` |
| `exp121_forwards.json` (120 raw forward records) | `80db4300b4d741ec4dd05ee9ef655a2015f81d4e2ae4f17e6118c91d8d380904` |
| `exp121_precheck.json` (60-item [-3:] pre-check) | `513ee67cda02740673ff30f1d5db243e08d021699b59ba16a6eac0309f7e3c04` |
| `exp121_per_item.json` (60 per-item records) | `eb00f32275e187afd9733b4f8643644bce1046b57dd064261ac0f23ecb76be34` |
| `exp121_result.json` (worksheet + verdict) | — |
| `exp121_stdout.log`, `exp121_console.log` | — |

All five raw-artifact hashes in the worksheet were re-verified against the files on disk after the run (all match). The `execute_script` hash entry inside the result JSON refers to the pre-reconstruction empty file and is superseded by the corrected hash above (result JSON left append-only; correction recorded here).


## ERRATUM (append-only, LOG-4646, 2026-09-29)

**Pre-erratum report state:** the original report prefix above is byte-identical and unchanged — no line of it was modified. SHA-256 of the report file before this erratum was appended: `f517f2e7b9e18119ae153e5b3f0609ab2ce22aea58985c88d8706b3caae5d068`.

**Correction** (independent exact-artifact verdict review LOG-4645 — QUALIFY, verdict stands): the report's sentence "A second independent full run reproduced n_valid = 38 exactly (deterministic greedy decoding), confirming the count is not a flake" is **not verifiable from retained artifacts**. Only the final run's records (60 planner generations, 120 forward records, per-item records) exist on disk; attempt 2's 60 generation records were overwritten by the final fresh run and were not retained, so cross-run reproduction of the count by a second full run cannot be evidenced. The verified claim, replacing that sentence: **n_valid = 38/60 was recomputed independently from the retained final-run artifacts** (LOG-4645: lane validity flags cross-checked field-by-field on `exp121_per_item.json`, zero mismatches), and a **deterministic re-read ×2 of those artifacts is byte-identical** (`reparse_byte_identical: True`), reproducing 38/60 — the count's stability is artifact-supported through the deterministic re-read, not through two retained full runs.

**Verdict unchanged: RUN-INVALID stands** (elicitation-failure gate, n_valid = 38/60 < 48; also fires under the stricter sum ≥ 0.02 reading at 30/60).
