# Pre-registration: H4 — PTTSC (Planned Test-Time Scaling Coordinator, CPU pilot)

**Candidate:** H4 — PTTSC: Planned Test-Time Scaling Coordinator (CPU pilot of planned test-time scaling: planner writes 4 outlines in one pass, frozen executor develops each, majority vote — vs 4 independent samples at matched executor budget)
**Date:** 2026-09-29
**Dossier:** `research/innovation/SPRINT_2026-09-29_SUMMIT.md` §H4 (worth-it gate passed; ranked #3)
**Lane:** LOG-4547 (drafting only)
**Status:** DRAFT — unsigned. Independent Law #14 review is a **separate lane** and is **not** this lane's work. **No experiment number minted.** No execution.

---

## 1. Hypothesis (one falsifiable sentence) [HYPOTHESIS]

At matched executor generation budget on the 20-item pilot bench, planned test-time scaling (frozen planner writes 4 outlines in one pass; frozen executor develops each; majority vote) beats unplanned repeated sampling (4 independent baseline samples; majority vote) with a one-sided McNemar exact p ≤ 0.05 — i.e., planning the test-time budget adds measurable decision capability for this task class.

**Falsifier:** planner-majority accuracy ≤ baseline-majority accuracy on the paired item set (net ≤ 0).

---

## 2. Exact question [PROPOSITION]

At fixed generation budget, does planned test-time scaling beat unplanned repeated sampling on the relational bench?

**Decision changed:** **CONTINUE** the coordinator program (a CONTINUE licenses — as *separate, later, founder-gated lanes* — the planner-executor pattern entering the EXP068-family adaptive-loop designs) vs **KILL** it (planning the budget adds nothing at this pilot scale on this pilot bench; the coordinator axis is retired for the piloted scope).

**Primary metric (registered before any run):** Δ = acc(planner-majority) − acc(baseline-majority) on n_valid paired items, with the verdict licensed by the one-sided McNemar exact test on the 2×2 paired contingency table (b = planner-right/baseline-wrong, c = planner-wrong/baseline-right).

---

## 3. Method

### 3.1 Frozen backbone [ASSUMPTION / Law #6]

- Backbone weights are **frozen**: Δθ = 0. Snapshot: `~/workspace/.exp086_weights/pythia-410m`; environment: `~/workspace/.venv-exp077` (torch 2.14.0+cpu, transformers 5.17.0 — the registered EXP106/EXP107 environment).
- The backbone parameter hash is recorded before and after the run and compared against the LOG-331 pin `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed`. Any mismatch → RUN-INVALID, quarantine, no metric may be read (Law #6, Law #13).
- **Determinism pins (Law #13):** `model.eval()` before all generation; `torch.no_grad()` around ALL forward passes; `device_map="cpu"`; float32.

### 3.2 Bench, provenance, and pilot scope

- **Items:** the 60-item EXP091 bench, rebuilt verbatim via `experiments/runs/EXP089_clm8b_falsifier/benchmark_exp089.py: build_benchmark()` (the deterministic verbatim port of the repaired EXP077 builder). Provenance pin: before any generation, the executor asserts the SHA-256 of `experiments/runs/EXP077_cone_vs_line/exp077_instance_records.json` equals `47281cd3dc243369be0aa5be2345663b752cdb4a329a16a37f08da5717230585` (carried from the EXP091 signed protocol); mismatch → RUN-INVALID. The executor asserts `len(bench) == 60` at build time (Law #9: no new benchmark construction).
- **Pilot scope (pinned, no cherry-picking):** this run uses the **first 20 items in bench build order** (indices 0–19). The executor asserts exactly 20 items at build time. A full-n=60 run would be a separate pre-registered lane, not a re-run of this one (see §7 for the CPU-honesty reason).
- **Labels (Law #7):** bench ground-truth labels (the target entity name, i.e. the bench's "A"-keyed entity) are used **only at metric time** — never during generation, never during any selection choice. The planner, executor, and baseline never see labels. Law #7 clean by construction.
- **Bench choice justification:** the EXP091 bench is the program-standard relational bench (EXP091/EXP094/EXP095/EXP105 all measured on it); it is the only bench on which the Decodability Gap and the static-family kills are registered, so the coordinator hypothesis is tested against the hardest available negative background. No alternative bench is licensed.

### 3.3 Planner spec (pinned verbatim)

- **Planner prompt template (pinned, exactly one template):**
  ```
  {PROMPT}

  Plan: Before answering, write 4 distinct numbered solution outlines (1. 2. 3. 4.), each a different approach to answering the question. Each outline must be 40 words or fewer. Do not give the final answer yet.
  ```
  where `{PROMPT}` is the item's full bench prompt verbatim (premise + question + option list), unchanged.
- **Generation spec (pinned):** greedy decoding (`do_sample=False`), `max_new_tokens=160`. One planner generation per item. No sampling, no temperature — nothing left to tune.
- **Outline extraction (pinned):** scan the planner output left to right; record the first occurrence position of each literal marker `1.`, `2.`, `3.`, `4.`; for k=1..4, outline_k = the substring from the end of marker `k.` to the start of the next marker occurrence in position order (or end of output), stripped; text before the first marker (preamble) is discarded; a missing marker yields an empty outline; then drop empties and exact duplicates; planner-valid iff ≥ 2 distinct non-empty outlines remain; outline_idx for seeding is the 0-based position in the post-dedup list. Result = the outline list for the item.
- **Planner-valid rule (pinned):** an item's planner arm is valid iff the outline list has **≥ 2 distinct non-empty outlines**. Otherwise the item is planner-invalid (see §3.8). This is the EXP108-degenerate-generation defense: an echo or a single repeated block cannot masquerade as 4 plans.

### 3.4 Executor spec (pinned verbatim)

- **Executor prompt template (pinned, exactly one template, per outline k):**
  ```
  {PROMPT}

  Outline {k}: {OUTLINE_TEXT}

  Develop the outline above into a final answer. Reply with the name of the higher-ranked entity and nothing else.
  ```
- **Generation spec (pinned):** `temperature=0.7, top_p=0.9, max_new_tokens=48`, seed pinned per (item, outline): `seed = 2000 + 10*item_idx + outline_idx` (`transformers.set_seed` + `torch.manual_seed`). Four executor generations per item (one per extracted outline; if the planner yielded only 2–3 distinct outlines, develop exactly those — the vote rule in §3.6 handles the count).
- **Sampling-parity note (pinned design decision):** the executor and the baseline (§3.5) share the IDENTICAL sampling spec (temperature, top_p, per-generation seed scheme). The only licensed difference between the arms is plan-conditioned vs unconditioned prompt content. A greedy executor vs sampled baseline would confound planning with sampling regime and is barred.

### 3.5 Baseline spec (pinned verbatim — 4 independent samples)

- **Baseline prompt template (pinned, exactly one template):**
  ```
  {PROMPT}

  Answer the question above. Reply with the name of the higher-ranked entity and nothing else.
  ```
- **Generation spec (pinned):** `temperature=0.7, top_p=0.9, max_new_tokens=48`, seed pinned per (item, sample): `seed = 3000 + 10*item_idx + sample_idx`. Four independent baseline samples per item.
- **Parse rule (pinned, both arms):** decode the newly generated tokens only (prompt tokens excluded — the EXP108 convention); strip whitespace and trailing punctuation (.,;:!?); case-insensitive compare against the item's two bench entity names (bench keys "A" and "C"): exact match → that entity is the vote; otherwise the generation is **UNPARSEABLE** and its vote is dropped. The EXP108 echo mode is caught by this rule by construction (echoed prompt text cannot exactly match an entity name).
- **Arm-valid rule (pinned):** an item's arm is valid iff it has **≥ 3 parseable votes**. Otherwise the arm is invalid for the item.

### 3.6 Vote rule (pinned, exact, with tie-break)

- Per item and per arm: **majority of the parseable votes**. Ties (2–2, or any even split of parseable votes) are broken deterministically toward the **foil entity** (the bench's "C"-keyed entity — conservative, matching the program precedent in the H1 prereg §3.3).
- The tie count per arm is reported. No other tie-break is licensed.

### 3.7 Budget definition (pinned — what "identical budget" means)

- **Matched executor budget:** 4 executor developments vs 4 baseline samples, each capped at 48 generated tokens, identical sampling spec. This is the budget matched between arms.
- **Planner overhead:** the single planner pass (≤ 160 tokens, greedy) is the *additional* test-time cost whose marginal value the experiment tests. It is NOT matched — it is the hypothesis. (This clarifies the dossier's "identical generation budget" phrasing: identical *executor* budget; the planner pass is the treatment.)
- Per-item worst-case token ceiling: 160 + 4×48 + 4×48 = 544 tokens. 20 items → 10,880 tokens max.

### 3.8 Validity, degeneracy, and RUN-INVALID gates (the EXP108 lesson)

- **Item valid** iff planner arm valid (§3.3) AND executor arm valid (§3.4/§3.6) AND baseline arm valid (§3.5/§3.6). n_valid = number of valid items (n_valid ≤ 20).
- **Elicitation-failure gate:** if 20 − n_valid ≥ 3 (> 10% of the 20-item pilot, the same 10% rule as the H1 prereg §3.4) → **RUN-INVALID (elicitation failure), NOT a verdict.** The generation apparatus failed; this is not evidence about planning.
- **Global degeneracy tripwire:** if ≥ 50% of executor + baseline vote-generations across the run are UNPARSEABLE (planner generations are covered by the planner-valid rule, not the parse rule) → **RUN-INVALID (apparatus failure)** regardless of n_valid.
- **Backbone hash mismatch** (Δθ ≠ 0) → RUN-INVALID, quarantine, no metric read (Law #6, Law #13).
- **Provenance SHA-256 mismatch** → RUN-INVALID. No metric exists.

### 3.9 Not a follow-up to EXP106/EXP107 or EXP070 [FACT]

H4 is **not** a follow-up to the EXP106/EXP107 line, and that line is closed: EXP106's transfer reading was killed by EXP107's template-control (34/60 ≤ 35/60 → KILL; the EXP106 GPU-proposal license is VOID). H4 tests a **different object** (inference-time planning, not a trained head) and reuses **no** EXP106/EXP107 artifact (no head, no decorrelated bench, no template cells). The EXP106/EXP107 lesson is incorporated as *design discipline* (every variable pinned above; template-generality explicitly not claimed — §8).
H4 **complements, not duplicates**, GPU-gated EXP070: EXP070 measures the oracle ceiling; PTTSC pilots the *mechanism* (planner-executor coordination) on CPU.

---

## 4. Decision bars (registered, with statistical license)

All bars are on the paired item set (n_valid ≤ 20). b = items where planner-majority is correct and baseline-majority is wrong; c = items where planner-majority is wrong and baseline-majority is correct. The verdict license is the **one-sided McNemar exact test** on (b, c). Critical values verified at drafting:

| (b, c) | net | one-sided exact p |
|---|---|---|
| (5, 0) | +5 | 0.0312 ✓ |
| (6, 0) | +6 | 0.0156 ✓ |
| (6, 1) | +5 | 0.0625 ✗ |
| (7, 1) | +6 | 0.0352 ✓ |
| (7, 2) | +5 | 0.0898 ✗ |
| (8, 2) | +6 | 0.0547 ✗ |
| (9, 2) | +7 | 0.0327 ✓ |

A raw accuracy-difference bar is **not** licensed at this n: net +5/20 with a single compensating flip ((6,1)) fails significance. The McNemar test on the discordant pairs is the license; the effect size is reported, not gated on.

| Outcome | Verdict | Statistical license — what the region means (no weasel words) |
|---|---|---|
| One-sided McNemar exact p ≤ 0.05 (minimum practical bar: net ≥ +5/20 with zero compensating flips, e.g. (5,0)) | **CONTINUE** | Planning the test-time budget adds measurable decision capability at this scale/bench. The coordinator program continues (later lanes only: planner-executor pattern for the EXP068-family adaptive loop). |
| net ≤ 0 (planner ≤ baseline) | **KILL** | Planning adds nothing at this pilot scale on this pilot bench. The coordinator axis is retired for the piloted scope (a full-bench test remains a separate, unlicensed lane). |
| 0 < net but McNemar p > 0.05 | **HELD** | A gain too small to license CONTINUE and too large for a clean KILL. Indeterminate. Licenses nothing, retires nothing, no re-runs. |
| Any hypothesis rewording after seeing the metric | **BARRED** | Law #4: never silently shift hypotheses. A post-hoc rewrite is scientific misconduct, not a verdict. |

**No rescue runs.** A HELD or KILL is never followed by a larger-n re-test, more outlines, a different prompt, or a re-seed — each would be an unlicensed gate tweak (barred). A full-n=60 run is a separate pre-registered lane, not a continuation of this one.

---

## 5. Degrees of freedom — pinned in advance (the EXP106/EXP107 lesson)

| Degree of freedom | Pinned value | Section |
|---|---|---|
| Bench and builder | EXP091 60-item bench, `build_benchmark()` verbatim; provenance SHA-256 pin; pilot = first 20 items in build order, asserted | §3.2 |
| n | 20 exactly (pilot scope); no subsampling beyond the pinned first-20 rule | §3.2 |
| Planner prompt | verbatim template in §3.3 — one template only | §3.3 |
| Planner generation | greedy (do_sample=False), max_new_tokens=160 | §3.3 |
| Outline extraction | first-occurrence positions of literal markers `1.`–`4.`; preamble discarded; missing marker → empty; drop empties/dups; planner-valid iff ≥ 2 distinct non-empty; seed outline_idx = 0-based post-dedup position | §3.3 |
| Executor outline count | develop exactly the extracted outlines (2–4); seed outline_idx = 0-based position in the post-dedup outline list | §3.4 |
| Executor prompt | verbatim template in §3.4 — one template only | §3.4 |
| Baseline prompt | verbatim template in §3.5 — one template only | §3.5 |
| Sampling spec (executor AND baseline) | temperature=0.7, top_p=0.9, max_new_tokens=48, pinned seeds (executor: 2000+10·i+k; baseline: 3000+10·i+k) | §3.4/§3.5 |
| Parse rule | newly generated tokens only; strip whitespace/trailing punctuation; case-insensitive exact match vs the item's two bench entity names (bench keys "A"/"C"); else UNPARSEABLE, vote dropped | §3.5 |
| Arm-valid rule | ≥ 3 parseable votes per arm per item | §3.5 |
| Vote rule | majority of parseable votes; ties → foil entity (bench "C" key) | §3.6 |
| Budget definition | matched executor budget (4×48 tokens/arm); planner pass (≤160) is the treatment | §3.7 |
| Item-valid rule | both arms valid; 20 − n_valid ≥ 3 → RUN-INVALID | §3.8 |
| Global degeneracy tripwire | ≥ 50% of executor + baseline vote-generations UNPARSEABLE → RUN-INVALID (planner covered by planner-valid rule) | §3.8 |
| Backbone parameter-hash pin | LOG-331 pin recorded before and after; any mismatch → RUN-INVALID, quarantine, no metric read | §3.1 |
| Determinism pins | `model.eval()` before all generation; `torch.no_grad()` around ALL forward passes; `device_map="cpu"`; float32 | §3.1 |
| Metric | Δ = acc(planner-majority) − acc(baseline-majority) on n_valid; verdict licensed by one-sided McNemar exact on (b, c) | §2/§4 |
| Decision bars | §4 table — no other reading licensed | §4 |
| Bench labels | used only at metric time; never during generation or selection | §3.2 |

No other variable may be adjusted after the metric is seen. Anything not in this table was not measured.

---

## 6. Falsification decision tree

| Outcome | Verdict | Meaning (no weasel words) |
|---|---|---|
| Provenance SHA-256 mismatch | **RUN-INVALID** | Bench provenance broken. No metric exists. |
| Backbone hash mismatch (Δθ ≠ 0) | **RUN-INVALID** | Law #6 violated. Quarantine. No metric exists. |
| 20 − n_valid ≥ 3 | **RUN-INVALID** | Elicitation failure — the generation apparatus did not produce. Not a verdict. |
| ≥ 50% of executor + baseline vote-generations UNPARSEABLE | **RUN-INVALID** | Apparatus failure (the EXP108 echo mode at scale). Not a verdict. |
| McNemar one-sided p ≤ 0.05 | **CONTINUE** | Planning adds measurable capability at this scale/bench. Coordinator program continues (later lanes only). |
| net ≤ 0 | **KILL** | Planning adds nothing at this pilot scale on this pilot bench. The coordinator axis is retired for the piloted scope. |
| 0 < net, p > 0.05 | **HELD** | Indeterminate gain. Licenses nothing, retires nothing, no re-runs. |
| Any post-hoc hypothesis rewording | **BARRED** | Law #4. Scientific misconduct, not a verdict. |

---

## 7. Cost / honesty statement [FACT]

- **$0 compute.** No GPU contact. No new training data. No model weights leave the frozen backbone.
- **~1.5–3.5 hours CPU** (20 items × ≤544 tokens max = 10,880 generated tokens on frozen Pythia-410m CPU; assumption: ~0.5–1 s/token for 410M-parameter float32 forward passes on this machine — stated so the estimate is checkable).
- **Why a 20-item pilot, not the dossier's n=60:** at the same token ceiling, n=60 would cost 32,640 tokens ≈ 4.5–9+ hours of single-threaded CPU generation — beyond the practical envelope and risky to leave unmonitored. The pilot is the honest CPU scope. A full-n=60 run would require a separate pre-registration with re-derived bars (see Deviation §8.2) — it is not a re-run of this lane.
- This lane **drafts only**: no execution, no experiment number minted, no signed protocol (v82/v83/v84, GPU queue, weights) touched, no push, no PR.

---

## 8. What this does NOT claim

- A CONTINUE is a **planning premium at this scale on this bench** — not superintelligence, not consciousness, not generality beyond the 20-item pilot bench, not evidence that planning helps any other task class, and not a claim about *why* planning helps (the mechanism reading is interpretation, not measurement).
- A KILL retires the *TTS/coordinator axis for this task class*, not the summit program.
- A HELD is an indeterminate observation — it licenses nothing and retires nothing.
- Template-generality is explicitly NOT claimed (one pinned planner template, one pinned executor template; a template-decorrelation follow-up would be a separate pre-registered lane — the EXP107 lesson).
- Novelty remains **N1 — Known Combination** (PTTS is prior art — Wu et al. 2609.27374, Meta FAIR 2609.26704; differentiated by bench + frozen-410m + CPU pilot + matched-budget design; complementary to GPU-gated EXP070).
- Unsigned and unreviewed until the independent Law #14 lane signs or rejects.

**Deviations [FACT]:** three deviations from the dossier, recorded here, the first two mathematically required:
1. **Budget definition (§3.7):** the dossier's "identical generation budget" is clarified to *identical executor budget* (4×48 tokens/arm) with the single planner pass (≤160 tokens) as the treatment — the planner overhead is what PTTS theory says pays off, so matching it away would test nothing.
2. **Decision bars (§4):** the dossier's raw "planner ≥ baseline + 8pp → CONTINUE" bar is **not statistically meaningful** at the registered n=20 pilot scope (+8pp ≈ +2/20 — a single compensating flip destroys significance; even net +5/20 with (b,c)=(6,1) gives p=0.0625). The CONTINUE bar is therefore licensed by the one-sided McNemar exact test (p ≤ 0.05; minimum practical configuration (5,0), net +5/20). The KILL bar (planner ≤ baseline) is unchanged from the dossier. The same McNemar license would be required at n=60 — a full-n run would be a separate lane with re-derived bars.
3. **Pilot scope (§3.2/§7):** the dossier specifies n=60; this lane registers a 20-item pilot (first 20 in bench build order) as the honest CPU scope — mechanical and cherry-pick-free, but unrepresentative of the 60-item bench (planet-only: 15 planet-2hop + 5 planet-3hop, 0% elemental). A full-n=60 run would be a separate pre-registered lane with re-derived bars, not a re-run of this one.

---

**Next steps (not this lane's):** independent Law #14 review of this exact file → CEO launch decision → execution under a minted experiment number (founder-authorized lanes only).
