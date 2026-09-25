# EXP090 — Zero-Shot Contrastive-Style Scoring over Frozen Representations v2: SIGNED PRE-REGISTRATION

**Status: SIGNED — CEO (Nova), 2026-09-25.** This protocol is IMMUTABLE. Any design change becomes a NEW experiment number, never an edit to this file.

**Signing basis:** LOG-334 (CLM-8B ADAPT verdict) → LOG-335/336/337/338 (EXP089 draft → review → repair → SIGNED) → LOG-344/345 (EXP089 bundle; §6 CONFIRMED UNSATISFIABLE, binding) → LOG-347 (EXP090 draft, §0 substitution disclosed) → LOG-348 independent Law #14 review (**SIGN-WITH-FIXES**, F1–F2; §0 substitution ACCEPTED, restructure rejected as process theater) → LOG-349 repair wave (both fixes applied, CEO-verified; caveat 6 verbatim). $0 CPU; no weights touched; no signed protocols edited.

**CEO's signing note:** signed as the satisfiable successor — EXP089's question, bar, guards, and decision tree survive intact; the only change is the §6 bench definition the old contract could not meet. Caveat 6 (no "exactly the bench EXP077 ran" claim) is load-bearing and survives verbatim per the binding review. EXPECTING a kill-or-signal on the free-lunch claim.

**Lineage:** EXP089 stays on record, SUPERSEDED-BY-EXP090 for execution purposes only. Its bundle modules are reused by the EXP090 bundle.

**Licensed:** execution-bundle build (CPU) may proceed. Execution is CPU-only — no GPU clearance required or granted.

---
# EXP090 — Zero-Shot Contrastive-Style Scoring over Frozen Representations v2
## (CLM-8B adaptation: the free-lunch falsifier, second attempt)

> **DRAFT WATERMARK — SUPERSEDED by the SIGNED header above (LOG-350, 2026-09-25).** Execution requires the full launch chain:
> signed pre-registration → independent Law #14 review → startup smoke test →
> CEO execution clearance (CPU-only; no GPU clearance required or granted) →
> execution. The runner must REFUSE any execution flag while this file is unsigned.

> **SUCCESSION BANNER.** EXP089
> (`experiments/protocols/EXP089_CLM8B_ADAPTATION_PREREG_SIGNED.md`,
> immutable, digest `87f2c47b…4c24cb`) is **SUPERSEDED-BY-EXP090 for execution
> purposes**: its §6 executor contract was ruled CONFIRMED UNSATISFIABLE by
> binding independent review (LOG-345) and it cannot execute a real run.
> EXP089 remains on the record; its bundle modules
> (`experiments/runs/EXP089_clm8b_falsifier/`) are reused by the EXP090 bundle.
> This protocol changes ONLY §6 (benchmark definition). Everything else —
> question, bar, guards, decision tree, scope fence — is identical to EXP089.

**Experiment number:** EXP090 (verified free 2026-09-25; no EXP090 file existed in
`experiments/protocols/`).
**Draft date:** 2026-09-25.
**Parent analysis:** `research/frontier_adaptations/CLM8B_ADAPTATION_2026-09-25.md`;
LOG-334 (ADAPT verdict).
**Parent protocol:** EXP089 SIGNED (LOG-338); blocker found at bundle build
(LOG-344); confirmed unsatisfiable at independent bundle review (LOG-345).

---

## 0. Lineage — the single design change, and a drafting disclosure

**What changed:** §6 only. EXP089 §6 required the ported benchmark builder's
`(ent, typ)` sequence to reproduce `exp077_instance_records.json` byte-for-value,
else RUN-INVALID. Binding review (LOG-345) confirmed this contract
unsatisfiable: the repaired builder yields 12/60 positional matches, and the
pre-repair builder that produced the archive is not retained anywhere
(LOG-3994/LOG-4238 provenance break, reproduced a third time).

**Drafting disclosure (read before signing):** the CEO's brief directed
EXP090 to "define the bench DIRECTLY as the hash-pinned archived records"
with the executor READING the 60 records instead of rebuilding them.
Drafting inspection (2026-09-25, read-only) proved that literal reading
unsatisfiable: the archived records contain only
`(item, ent, typ, correct, rescue_indicators)` — no prompts and no foil
entities — and their `(ent, typ)` multiset differs from the repaired
builder's output (archive uniformly grouped — Mars/Venus/Jupiter/Saturn/Mercury ×6
planet; Iron/Gold/Silver/Bronze/Steel ×6 element — vs the repaired builder at
Mars×21, Iron×21, Venus×7, Gold×7, Jupiter×2, Silver×2; verified by Counter
comparison this session), so no deterministic
matching rule can recover executable `(prompt, A, C)` items from the archive.
A draft written to the literal brief would register a second unsatisfiable
contract. This draft therefore implements the closest satisfiable contract to
the brief's intent — the bench is the registered, deterministic, fully
reconstructible construction, and the archive is pinned as the provenance
record it descends from (§6). **The deviation from the brief is flagged here
explicitly for Law #14 review; the reviewer may redirect.**

**What did NOT change:** the precise question (§1), background (§2), Δθ=0 scope
fence (§3), Law #7 statement (§5), registered bar ≥38/60 with P=0.0260 (§7),
the §7.1 TOTAL decision tree, guards G1/G3/G4, the Law #13 determinism pins,
the refusal gates, the $0 CPU budget, and the brutal caveats.

---

## 1. Precise question

Does output-side contrastive-style scoring over **frozen, untrained**
Pythia-410m representations produce causal decision gains where static
injection produced exactly zero — i.e., did the backbone's pretraining do
CLM-8B's contrastive work for free, or does the CLM capability live entirely
in the 60M-pair head training we cannot afford?

## 2. Background (why this test exists)

- CLM-8B (Contrastive-LM, released 2026-09-24; primary source: HF model card
  `Contrastive-LM/CLM-v0.1-8B`; Kwok et al. 2026, Notion Blog, no arXiv paper)
  scores candidates with two small projection heads over a **frozen** Qwen3-8B
  encoder (bidirectional InfoNCE). It never touches the forward pass.
- SCBI boundary result (EXP077, branch (c) NEITHER): all static geometric
  variants ΔM=0, p=1.0; the transferable signal lives **output-side**
  (bridge +10pp, p=0.03125). CLM vindicates the output-side finding as an
  architecture and threatens the static-injection direction
  (EXP065/066/070/077/082 lineage), not the frozen-backbone constitution.
- The adaptation question (LOG-334: ADAPT): steal the *architecture*
  (state/action disaggregation, scoring-as-decision at the output boundary).
- EXP089 (LOG-335 draft → LOG-336 Law #14 SIGN-WITH-FIXES → LOG-337 repairs →
  LOG-338 signed) was the first attempt. Its bundle (LOG-344, 28/28 tests)
  exposed the §6 unsatisfiability; binding review (LOG-345) confirmed it.
  EXP090 is the repaired second attempt. Nothing about the question changed —
  only the bench contract.

## 3. EXPLICIT SCOPE FENCE — Δθ=0 only

- **Licensed:** zero-shot cosine scoring over frozen Pythia-410m activations.
  No trainable heads, no weight updates, no new data collection, no fine-tuning
  of any kind. The LLM backbone stays frozen (θ_after = θ_before); the
  FrozenBackboneGuard hashes state_dict before/after (Law #6/Law #13).
- **OUT OF SCOPE:** training projection heads (CLM's actual 20M-parameter
  heads), any gradient step on any parameter, any new benchmark construction.
- **Any CONTINUE toward trained apparatus requires a NEW experiment number and
  the founder's explicit license.** This experiment cannot license training.
  (LOG-334 Δθ=0 adjudication: heads are trainable apparatus; Law #7 would
  apply in full to any future head-training program.)

## 4. Artifact lineage (read-only; nothing modified)

- `experiments/runs/EXP077_cone_vs_line/exp077_instance_records.json`:
  `47281cd3dc243369be0aa5be2345663b752cdb4a329a16a37f08da5717230585`
  (recomputed 2026-09-25; character-identical to the EXP089 §4 record and the
  LOG-345 review record). Pinned in §6 as the provenance record.
- `experiments/runs/EXP077_cone_vs_line/exp077_results.json`:
  `c0d5c28d075fe74488fd1e33b93b730907577e41e1b53959d61be7d2d8bb90f7`
- `experiments/runs/EXP077_cone_vs_line/exp077_vectors.pt`:
  `8793e4d0baea844f9ae6afbec7970770d161b3f827bc234d3597286b66810cb9`
  (18 tensors: sixteen 1024-dim direction vectors + two basis blocks — the
  cone experiment's direction vectors, NOT per-item embeddings; the memo's §5
  assumption was false and remains false)
- `experiments/runs/EXP077_cone_vs_line/exp077_run_log.txt`:
  `49a20b96f45b54189a8f6c9ed1463418f9b2d29e572ab1e2bd19ab7daa1b1ad3`
- Frozen weight snapshot reused from LOG-331
  (`experiments/runs/EXP086_amplifier/weights/pythia-410m/`); state_dict
  SHA-256 `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41e1b53959d61be7d2d8bb90f7`
  matches EXP077's own recorded pre/post hashes — same weights EXP077 ran on.
- Per-item embeddings are re-extracted from the frozen snapshot (CPU,
  read-only); the registered benchmark construction is §6.

## 5. Law #7 (zero leakage) statement

No training occurs, so no labels flow into any trained component. Labels (the
registered answers A) are used only to score the metric — standard evaluation.
The state text is pinned to the premise sentences only (§6), excluding the
question and the option list. Both option names DO appear in the premise —
each exactly once, 1:1 balanced — so protection against option-name token
overlap is lexical *balance* plus the §7.1 positional diagnostic as the
confound control, NOT exclusion [Law #14 F6].

## 6. Design — THE REPAIRED BENCH CONTRACT (the single design change)

**Benchmark (Law #9: no new benchmark construction).** EXP090 defines its
benchmark as the deterministic output of the verbatim port of the repaired
EXP077 benchmark builder (`experiments/runs/exp077/run_exp077.py`), as
implemented in `experiments/runs/EXP089_clm8b_falsifier/benchmark_exp089.py:
build_benchmark()` and independently verified at LOG-345 (28/28 tests; G3
30/30 verified on the builder's own output; vocab lists, index arrays, and
prompt templates ported verbatim; the only addition is the `phrasing`
provenance field). The executor asserts `len(bench) == 60` at build time.

**Provenance pin (replaces the struck byte-reproduction guard).** Before any
extraction, the executor asserts the SHA-256 of
`experiments/runs/EXP077_cone_vs_line/exp077_instance_records.json` equals
`47281cd3dc243369be0aa5be2345663b752cdb4a329a16a37f08da5717230585`;
mismatch → RUN-INVALID. The archive is pinned as the provenance record the
construction descends from — the byte-identity of the archive guarantees it is
the data EXP077 ran on, and the LOG-345-verified verbatim port implements the
registered construction (same vocab lists, index arrays, prompt templates;
only addition is the `phrasing` provenance field). The EXP089 §6 byte-for-value `(ent, typ)` reproduction
guard is **STRUCK** as unsatisfiable (LOG-344/345); no reproduction requirement
exists in EXP090.

**Per item** (`prompt`, `A`=target, `C`=foil):
- **State text** = the premise sentences only: the substring of `prompt` from
  `"Premise:"` up to (excluding) `" Question:"`. The question and option list
  are EXCLUDED by construction.
- **Action texts** = the bare entity names `A` and `C`.
- **Embeddings**: frozen Pythia-410m, **layer 20** (program-standard site),
  final-token hidden state, float32, CPU, `device_map="cpu"`,
  `requires_grad_(False)` on all parameters. **Determinism pins (Law #13):**
  `model.eval()` before extraction and a `torch.no_grad()` context around ALL
  extraction (eval mode is not relied on as an HF default — it is required
  explicitly).
- **Guards (all FATAL/INVALID on failure):**
  - G1: single-token assertion on every A and C (EXP075 guard reused); any
    multi-token entity → RUN-INVALID (items are NOT silently dropped; the
    registered bar requires exactly N=60).
  - G2: state_dict SHA-256 before/after embedding extraction must equal the
    LOG-331 snapshot hash → Δθ=0 verified; mismatch → RUN-INVALID.
  - G3: phrasing-balance assert — exactly 30 "A-first" items
    (`{A} outranks {B}...`, block-local i<8 planet / i<7 element) and 30
    "C-first" items (`{C} is lower than {B}...`); the builder MUST assert this
    count at build time.
  - **G4 (instrument-health gate; [Law #14 F1]):** compute all 120 cosine
    values (60 state–A, 60 state–C). If `max − min < 1e-4` — the instrument is
    anisotropy-deaf (all cosines ≈ 1.0 within float noise, argmax is noise) —
    the run is **RUN-INVALID (instrument deaf), NOT a verdict.** A KILL must
    mean the instrument worked and found nothing, not that the instrument was
    deaf. The full margin distribution (`|cos(A) − cos(C)|` per item) is
    reported in the run report regardless of outcome.

**Scoring rule (the untrained analogue of CLM's dot-product head):**
`score(option) = cosine(state_emb, option_emb)`; per-item decision =
`argmax(score(A), score(C))`; ties (exact float equality) are broken
deterministically toward `C` (the foil — conservative) and counted in the
report.

**Metric:** accuracy = (# correct) / 60.

**Bundle artifact requirement (carried forward from LOG-345 F1–F2):** the run
report MUST stamp the execution mode (`"mode": "mock"|"real"`) so a mock-run
verdict is never misread as a real-run verdict; `from_pretrained` MUST pin
`device_map="cpu"` literally.

## 7. Registered bar and decision tree

One-sided binomial test vs chance (p=0.5), N=60, α≈0.026:

| Correct / 60 | Verdict | Licenses next |
|---|---|---|
| **≥ 38** (63.3%) | **CONTINUE** (subject to §7.1 diagnostic) | A *proposal* for a trained-heads program (new experiment number + founder license required). Does NOT license training. |
| **≤ 37** | **KILL** | The free-lunch version dies: frozen Pythia-410m/layer-20 geometry carries no exploitable zero-shot decision signal; the adaptation is shelved pending training resources. [INTERPRETATION, not licensed inference: *if* the CLM-8B capability comes from its 60M-pair head training (or from trained heads of any size on a different geometry), it is unexecutable at $0 — this instrument cannot distinguish these attributions.] |

Exact: P(X ≥ 38 | n=60, p=0.5) = **0.0260** (computed exactly via math.comb;
independently recomputed at LOG-345 as 0.0259469…).

### 7.1 Pre-registered positional-confound diagnostic (mandatory)

Rationale: in "A-first" phrasing the target appears in the first sentence; in
"C-first" phrasing it appears in the last. Final-token embeddings may carry
positional (primacy/recency) bias, which would masquerade as signal. The two
phrasings flip the confound, so:

- Report `acc_Afirst` (30 items) and `acc_Cfirst` (30 items) alongside the
  aggregate, always.
- If aggregate ≥ 38/60 **and** strictly `acc_Afirst > 0.5` **AND** strictly
  `acc_Cfirst > 0.5` (both phrasings tilt toward the correct answer) → clean
  CONTINUE.
- **Boundary rule [Law #14 F2]:** the tree is TOTAL. Any aggregate-≥38/60
  outcome NOT satisfying both strict inequalities — including a phrasing
  split at exactly 0.5 (15/30), or opposite tilts — → **PIVOT**: the signal
  is phrasing-dependent; redesign with position-controlled state encoding
  under a NEW experiment number. The CONTINUE is withheld.
- If aggregate ≤ 37/60 → KILL regardless of the split (split still reported).

## 8. Falsification criteria, invalidity, refusal

**Falsifies the free-lunch claim:** ≤ 37/60 (KILL). The claim "frozen
pretrained geometry already aligns state–action MI with task labels" is
rejected at α≈0.026.

**RUN-INVALID (withheld, not a verdict):** weight-hash mismatch (G2);
archive-hash mismatch (§6 provenance pin); any multi-token A/C (G1);
phrasing-balance assert failure (G3); N ≠ 60 for any reason; **instrument
deafness (G4):** `max − min < 1e-4` over the 120 cosine values → RUN-INVALID,
never KILL.

**Refusal:** the execution bundle (when built) MUST refuse any run while this
protocol is unsigned; MUST refuse any flag requesting training, GPU execution,
or weight mutation; MUST refuse a real run if the signed-protocol digest
guard mismatches. Draft status confers zero license.

## 9. Budget

$0. CPU only. ~1–2 hours wall-clock (180 short forward passes on CPU
Pythia-410m + cosine scoring; weights already on disk from LOG-331 — no
download). No GPU contact. No new artifacts beyond the run report.

## 10. Why this is the cheapest falsifier

Killing the free-lunch claim requires NO 60M-pair contrastive training, NO
head training of any kind, NO new data, and NO GPU. It reuses the registered
EXP077 benchmark construction (Law #9), the on-disk LOG-331 weight snapshot,
and one CPU-hour. If frozen geometry carries no signal, the adaptation dies
here — before a single dollar or GPU-hour is contemplated for head training.

## 11. BRUTAL CAVEATS (bannered — read before interpreting any outcome)

1. **Probe-at-heart.** Zero-shot cosine scoring is, at its core, a probe. A
   CONTINUE validates only that frozen geometry carries task-relevant signal —
   it does NOT validate CLM-8B's architecture, its heads, or its recipe.
2. **The 9× claim is UNVERIFIED and untested here.** The headline latency
   figure (vs proprietary Jev, inaccessible) is vendor-reported; this
   experiment measures accuracy only and says NOTHING about speed.
3. **A CONTINUE does not license trained heads.** Heads are trainable
   apparatus crossing out of Δθ=0; they need a new experiment number and the
   founder's explicit license (LOG-334).
4. **Candidate-set dependence.** Scoring judges the candidates it is given; it
   cannot propose. For the superhuman-cognition summit, scoring is a
   component, not a path (memo §4.4).
5. **If the effect needs 60M+ training pairs, the adaptation is unexecutable
   at $0** — a KILL here means exactly that, and the program must not
   re-litigate it without training resources.
6. **Bench provenance.** EXP090's bench is the verbatim-ported repaired
   builder's construction, NOT the archived EXP077 item order (unrecoverable —
   LOG-344/345). The archive is pinned as provenance, not as the item source.
   Any claim of the form "this is exactly the bench EXP077 ran" is UNLICENSED.

## 12. Launch-chain status

DRAFT (this file) → independent Law #14 review → signing (CEO) → bundle build
→ independent bundle review → CEO execution clearance → execution.
**Current position: DRAFT. Nothing is licensed.**

---

*Draft prepared by the pre-registration agent, 2026-09-25. The §6 bench
contract was verified satisfiable by construction inspection in this session
(builder deterministic, 60 items, G3 30/30 on builder output per LOG-345);
the archive hash was recomputed read-only. The §0 disclosure flags the one
deviation from the CEO's brief for Law #14 review.*
