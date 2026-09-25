# EXP091 — Zero-Shot Contrastive-Style Scoring over Frozen Representations v3
## (CLM-8B adaptation: the free-lunch falsifier, third attempt)

> **SIGNED PRE-REGISTRATION.** Signed 2026-09-25. Independent Law #14 review: **SIGN**
> (LOG-356, 2026-09-25; review file
> `experiments/protocols/REVIEWS/EXP091_LAW14_REVIEW_2026-09-25.md`; review-target draft
> digest `1a1cf0746a0ac264…` — any post-review edit is detectable via the digest recorded
> in the launch log). This protocol licenses NOTHING on its own: execution still requires
> the launch chain — startup smoke test → CEO execution clearance (CPU-only; no GPU
> clearance required or granted) → execution.

> **SUCCESSION BANNER.** EXP090
> (`experiments/protocols/EXP090_CLM8B_ADAPTATION_V2_PREREG_SIGNED.md`,
> immutable, digest `440dd6a5…01b`) is **SUPERSEDED-BY-EXP091 for execution
> purposes**: its real execution (LOG-354) exited RUN-INVALID at the G1
> benchmark gate — the bare-word single-token check failed on 'Mars'
> (2 tokens bare; 7 of 10 bench entities multi-token bare), so no measurements
> were taken and the verdict was withheld per protocol. EXP090 remains on the
> record; its bundle modules (`experiments/runs/EXP090_clm8b_falsifier_v2/`)
> are reused by the EXP091 bundle. This protocol changes ONLY the G1 guard
> (G1 → G1', in-context single-token verification) and the action-text
> definition it constrains. Everything else — question, bar, decision tree,
> G2/G3/G4, scope fence — is identical to EXP090.

**Experiment number:** EXP091 (verified free 2026-09-25; no EXP091 file existed in
`experiments/protocols/`).
**Draft date:** 2026-09-25.
**Parent analysis:** `research/frontier_adaptations/CLM8B_ADAPTATION_2026-09-25.md`;
LOG-334 (ADAPT verdict).
**Parent protocol:** EXP090 SIGNED (LOG-350); real execution RUN-INVALID at G1
(LOG-354).

---

## 0. Lineage — the single design change, and a drafting disclosure

**Succession.** EXP089 (LOG-335 draft → LOG-336 review → LOG-337 repairs →
LOG-338 signed) died at bundle build: its §6 byte-reproduction contract was
CONFIRMED UNSATISFIABLE by binding review (LOG-344/345) — the repaired builder
yields 12/60 positional matches against the archive and the pre-repair builder
is not retained (LOG-3994/LOG-4238 provenance break, third reproduction).
EXP090 (LOG-347 draft → LOG-348 review → LOG-349 repairs → LOG-350 signed →
LOG-351 bundle → LOG-352 bundle review SIGN) repaired §6 by defining the bench
as the deterministic verbatim-ported builder output with the archive pinned as
provenance — but its real execution (LOG-353 clearance → LOG-354) exited
RUN-INVALID at G1: the EXP075-reused bare-word single-token check failed
('Mars' → 2 tokens bare; 7/10 entities multi-token bare). No embeddings were
extracted; the verdict was withheld per protocol.

**What changed in EXP091:** the G1 guard only (G1 → G1'), plus the action-text
definition the guard constrains (see §6). The bare-word check was over-strict
relative to the guard's purpose (unambiguous readout position): the CEO
verified by executing the real Pythia (GPT-NeoX) tokenizer that every entity
appears as EXACTLY ONE token in its natural in-context form (`ĠMars` etc.),
and the drafter has verified all 240 A/C occurrences across all 60 built
prompts are each covered by exactly one token (table in §6).

**Drafting disclosure (read before signing):** making G1' *only* about
in-prompt occurrences would leave it unconnected to the extraction, which
embeds the action texts as separate forward passes. To keep the guard
load-bearing on the embedded material, the action texts are defined as the
spaced single-token form `" "+A` / `" "+C` (the entity's natural BPE form —
verified 1 token for all 10 entities this session), so G1' constrains exactly
what gets embedded. The question, bar, tree, and fence are untouched. **This
coupling is flagged here explicitly for Law #14 review; the reviewer may
redirect.**

**What did NOT change:** the precise question (§1), background (§2), Δθ=0 scope
fence (§3), Law #7 statement (§5), registered bar ≥38/60 with P=0.0260 (§7),
the §7.1 TOTAL decision tree, guards G2/G3/G4, the Law #13 determinism pins,
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
- EXP089 was the first attempt (killed by its own §6 guard — unsatisfiable
  byte-reproduction contract, LOG-344/345). EXP090 was the repaired second
  attempt (LOG-347–353); its real execution exited RUN-INVALID at the G1
  bare-word gate (LOG-354) — a guard-implementation failure, not a
  measurement. Nothing about the question changed across the succession —
  only the bench and guard contracts.

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
  (recomputed 2026-09-25 by the drafter, read-only; character-identical to the
  EXP090 §4 record and the LOG-345 review record). Pinned in §6 as the
  provenance record.
- `experiments/runs/EXP077_cone_vs_line/exp077_results.json`:
  `c0d5c28d075fe74488fd1e33b93b730907577e41e1b53959d61be7d2d8bb90f7`
  (per EXP090 §4 record; verified at LOG-345)
- `experiments/runs/EXP077_cone_vs_line/exp077_vectors.pt`:
  `8793e4d0baea844f9ae6afbec7970770d161b3f827bc234d3597286b66810cb9`
  (per EXP090 §4 record; 18 tensors — the cone experiment's direction vectors,
  NOT per-item embeddings)
- `experiments/runs/EXP077_cone_vs_line/exp077_run_log.txt`:
  `49a20b96f45b54189a8f6c9ed1463418f9b2d29e572ab1e2bd19ab7daa1b1ad3`
  (per EXP090 §4 record; verified at LOG-345)
- Frozen weight snapshot reused from LOG-331
  (`experiments/runs/EXP086_amplifier/weights/pythia-410m/`); state_dict
  SHA-256 `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed`
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

## 6. Design — THE G1' GUARD CONTRACT (the single design change)

**Benchmark (Law #9: no new benchmark construction).** EXP091 defines its
benchmark exactly as EXP090 did: the deterministic output of the verbatim port
of the repaired EXP077 benchmark builder (`experiments/runs/exp077/run_exp077.py`),
as implemented in `experiments/runs/EXP089_clm8b_falsifier/benchmark_exp089.py:
build_benchmark()` and independently verified at LOG-345 (28/28 tests; G3
30/30 verified on the builder's own output; vocab lists, index arrays, and
prompt templates ported verbatim; the only addition is the `phrasing`
provenance field). The executor asserts `len(bench) == 60` at build time.

**Provenance pin (carried from EXP090).** Before any extraction, the executor
asserts the SHA-256 of
`experiments/runs/EXP077_cone_vs_line/exp077_instance_records.json` equals
`47281cd3dc243369be0aa5be2345663b752cdb4a329a16a37f08da5717230585`
(recomputed by the drafter this session — character-identical); mismatch →
RUN-INVALID. The archive is pinned as the provenance record the construction
descends from. The struck EXP089 byte-reproduction guard does not exist in
EXP091.

**Per item** (`prompt`, `A`=target, `C`=foil):
- **State text** = the premise sentences only: the substring of `prompt` from
  `"Premise:"` up to (excluding) `" Question:"`. The question and option list
  are EXCLUDED by construction.
- **Action texts** = the entity in its natural single-token BPE form:
  `" "+A` and `" "+C` (leading space included). Rationale: GPT-NeoX BPE
  represents these entities as single tokens only in spaced form (`ĠMars`);
  the bare form fragments (`Mars` → 2 tokens), which is what killed EXP090's
  execution at the old G1 gate. The spaced form is the entity as it appears
  in running text — it is the same lexical item, not a different candidate.
- **Embeddings**: frozen Pythia-410m, **layer 20** (program-standard site),
  final-token hidden state, float32, CPU, `device_map="cpu"`,
  `requires_grad_(False)` on all parameters. **Determinism pins (Law #13):**
  `model.eval()` before extraction and a `torch.no_grad()` context around ALL
  extraction (eval mode is not relied on as an HF default — it is required
  explicitly).
- **Guards (all FATAL/INVALID on failure):**
  - **G1' (in-context single-token verification; the design change):**
    every A/C occurrence in every constructed prompt must be covered by
    exactly one token, VERIFIED BY EXECUTING THE REAL TOKENIZER — never by
    reasoning about word commonness. Two enforcement points: (i) at build
    time, the benchmark builder runs the real Pythia tokenizer over all 60
    built prompts and fails loud if any entity span is multi-token; (ii) at
    extraction startup, the executor asserts `encode(" "+A)` and
    `encode(" "+C)` are each exactly one token (this is the embedded
    material). Any failure → RUN-INVALID (items are NOT silently dropped;
    the registered bar requires exactly N=60). Drafting verification (this
    session, real tokenizer, offset-mapping cover check): **240/240 A/C
    occurrences across all 60 prompts are each exactly one token**, and all
    10 spaced entities are single tokens —
    `ĠMars`[13648], `ĠVenus`[36210], `ĠJupiter`[34434], `ĠSaturn`[38876],
    `ĠMercury`[36091], `ĠIron`[17826], `ĠGold`[7284], `ĠSilver`[16309],
    `ĠBronze`[49134], `ĠSteel`[19727].
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

**G1' per-entity verification table (drafter-executed, real Pythia tokenizer,
2026-09-25):**

| Entity | Occurrences (A/C roles) | Single-token |
|---|---|---|
| Mars | 42 | 42 |
| Venus | 14 | 14 |
| Jupiter | 8 | 8 |
| Saturn | 16 | 16 |
| Mercury | 40 | 40 |
| Iron | 42 | 42 |
| Gold | 14 | 14 |
| Silver | 8 | 8 |
| Bronze | 16 | 16 |
| Steel | 40 | 40 |
| **Total** | **240** | **240** |

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
archive-hash mismatch (§6 provenance pin); any multi-token entity span under
G1' (build-time or extraction-time); phrasing-balance assert failure (G3);
N ≠ 60 for any reason; **instrument deafness (G4):** `max − min < 1e-4` over
the 120 cosine values → RUN-INVALID, never KILL.

**Refusal:** the execution bundle (when built) MUST refuse any run while this
protocol is unsigned; MUST refuse any flag requesting training, GPU execution,
or weight mutation; MUST refuse a real run if the signed-protocol digest
guard mismatches. Draft status confers zero license.

**Standing review rule (CEO, LOG-354; registered here as process law):** any
future claim that a benchmark satisfies a tokenization guard must be verified
by EXECUTING THE REAL TOKENIZER during Law #14 review — never by reasoning
about word commonness. Precedents: EXP075 (aborted — 11/35 multi-token);
LOG-336 V6 and LOG-345 (both asserted G1-satisfiability from "common single
words" without running the tokenizer; EXP090's execution proved the assertion
false at G1). A review that waves a tokenization claim through on
commonness reasoning is derelict.

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
6. **Bench provenance.** EXP091's bench is the verbatim-ported repaired
   builder's construction, NOT the archived EXP077 item order (unrecoverable —
   LOG-344/345). The archive is pinned as provenance, not as the item source.
   Any claim of the form "this is exactly the bench EXP077 ran" is UNLICENSED.
7. **G1' was verified by execution, not reasoning.** The §6 table above was
   produced by running the real Pythia tokenizer over all 60 built prompts
   (drafter, 2026-09-25) — 240/240 single-token. This is the standing rule of
   §8 applied to this protocol itself.

## 12. Launch-chain status

DRAFT (this file) → independent Law #14 review → signing (CEO) → bundle build
→ independent bundle review → CEO execution clearance → execution.
**Current position: DRAFT. Nothing is licensed.**

---

*Draft prepared by the pre-registration agent, 2026-09-25. The G1' contract
was verified satisfiable by real-tokenizer execution in this session (240/240
occurrences single-token; all 10 spaced entities single-token with ids
recorded); the archive hash was recomputed read-only
(`47281cd3…0585`, character-identical). The §0 disclosure flags the one
coupling decision (action texts as spaced single-token form) for Law #14
review.*
