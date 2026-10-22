# S4-8′ — I2′ Multi-Option Runner-Up Suppression (Cloze Format) — Pre-registration DRAFT (UNSIGNED)

*Status: DRAFT — UNSIGNED. NOT a protocol. NOT executable. NOT signed. No experiment number minted (S4-8′ is fresh-proposal material; numbering happens after Law #14 SIGN + CEO license).*
*This document is a NEW proposal, not a repair of the S4-8 v3 draft (`S4-8_PREREG_DRAFT_v3_2026-09-28.md`, LOG-4479/4480 line, awaiting its own delta check). Nothing in v3 is modified, amended, or superseded here — v3's MC-format pre-reg continues on its own track. S4-8′ is commissioned from the EXP104 bench autopsy (LOG-4483).*
*Licensing chain: LOG-323 (EXP085 KILLED as designed — binary collapse) → LOG-4480 (S4-8 pre-reg v3 signed-track, MC format) → EXP104 Tier-0 HOLD (LOG-4482; MC bench miscalibrated by a position-A prior) → LOG-4483 (bench autopsy: verdict (a), recalibration feasible as a NEW proposal) → LOG-4484 (this draft — DRAFT lane, pre-assigned LOG).*
*$0 CPU for this document (on paper only). No signed protocol touched. No pilot authorized.*

---

## 0. Law #15 block (binding)

**Exact question [HYPOTHESIS].** EXP104's Tier-0 screen (k=8 lettered MC) returned HOLD not because 2-hop selection failures don't exist, but because the readout measured a **position-A prior** (30/60 top-1 picks at position 0, p=2.02e-12) — a format-driven artifact of the `A)…H)` enumeration interacting with a base LM. **On the SAME 60 items re-prompted as cloze completions — the option enumeration and letters removed, the 8 G1-verified candidate tokens scored at the completion position — does the Tier-0 baseline land inside the sanity band [0.25, 0.75], licensing the S4-8 suppression battery on a calibrated bench?** [HYPOTHESIS]

**What changes from S4-8 (format only).** The prompt loses the lettered option list and the terminal `Answer:`; the question text stays verbatim and a pinned completion cue ends the prompt. The scored readout changes from "argmax over the 8 option tokens at the `Answer:` position" to "argmax over the same 8 candidate tokens at the completion position." The correct-position shuffle becomes obsolete (no positions exist) and is dropped, not replaced. The foil designations, blindness record, G1 token pools, items, templates, and k=8 are carried over verbatim. Everything else — decision table, bars, statistics, battery arms, guards — is carried over from v3 unchanged (§1).

**Decision it changes.** **CONTINUE** (license the S4-8 suppression battery on the cloze bench) iff cloze Tier-0 baseline ∈ [0.25, 0.75] AND median correct-rank on failed items ≤ 5 AND n_pop ≥ 12 AND tie-guard ≤ 25% — the Tier-0 screen is a gate, and passing it licenses the battery whose verdicts are v3's §3 (KILL/CONTINUE/PIVOT) applied to cloze measurements. **LINE-CLOSED** iff cloze Tier-0 baseline < 0.25 — this is the autopsy's verdict (b): the I2′ line is untestable on Pythia-410m at $0; no third readout may be proposed (instrument surgery after two HOLDs is p-hacking the bench — the backdoor warning from v3 §6 risk 6, honored here as a pre-registered stop). **HOLD** iff baseline > 0.75 (miscalibrated upward) or tie-guard > 25% (instrument degraded) — bench problems, not mechanism verdicts.

**Cheapest falsifying test.** Cloze Tier-0 rerun: 60 forward passes (~1 min CPU, **$0**, Δθ=0, deterministic seed-pinned), reusing the EXP104 item ids and G1-verified token pools from `experiments/runs/EXP104_Tier0_rank_screen/bench_manifest.json` (items reused, measurements not reused). Baseline < 0.25 kills the line at $0 before any battery pass is spent. The six §5 degeneracy unit tests re-run on the cloze rank function (same synthetic suite) before any bench contact.

**Quantitative prediction (pre-registered, bars).** Cloze Tier-0 baseline ∈ **[0.25, 0.45]** — labeled [HYPOTHESIS], not a claim (autopsy §3 anchor: the non-pos0 subset measured 0.233 with the prior only partially removed; full removal should add points; if the Cause-2 capability gradient dominates, the number lands near chance 0.125 instead — that outcome is exactly what Tier-0 adjudicates). Tier-0 gate bars: median correct-rank over failed items ≤ 5 (premise bar — > 5 → KILL premise per v3 §3 step 2); n_pop ≥ 12 (power bar — < 12 → Underdetermined per v3 §3 step 3); tie rate ≤ 0.25 (instrument bar — > 0.25 → HOLD per v3 §3 step 5).

**Breaking point (sharp).** Cloze Tier-0 baseline < 0.25 → **LINE-CLOSED** (verdict (b) — the I2′ line is untestable on this model at $0; no further proposal on this bench family may be commissioned). ΔM_T ≤ 0.05 on a licensed battery's Tier-0 population → the autonomous top-1-mask procedure has no effect (PIVOT-or-KILL per the carried-over §4 table). T-vs-R p ≥ 0.05 with ΔM_T > 0 → **KILL** (nonspecific).

**The belief it tests (named, LOG-4483):** "EXP104's HOLD was a readout artifact (Cause 1: position prior), not a capability absence (Cause 2: no retrievable 2-hop chains at 410m)." [HYPOTHESIS] A cloze baseline inside the band supports the artifact diagnosis and licenses the battery; a baseline below 0.25 supports the absence diagnosis and closes the line.

---

## 1. What is carried over from S4-8 v3 verbatim (format-independent)

The following are **not re-derived here** — they transfer by reference to the signed v3 draft and apply to cloze measurements without modification:

- **Mathematical license [PROPOSITION]:** at k=8, correct-rank r_i ∈ {1,…,8} is not a deterministic function of correctness; masking the top-1 token (−1e9 before argmax) is a well-defined operator; the masked argmax over the surviving 7 is a genuine counterfactual. **License verdict: HOLDS for a test, not a conclusion.** Honest audits carried: (Gap 1) softmax-perturbation priced out by the R arm; (Gap 2) any CONTINUE claim is bench-scoped; (Gap 3) n_pop ≥ 12 power gate.
- **Battery arms B/T/F/R** (§4), with the R-arm exclusion rationale (exclude baseline top-1 AND correct option; seed pinned) and masking semantics (−1e9, re-argmax, ΔM_X on the Tier-0 population).
- **Decision table** (v3 §3, steps 1–11, binding first-match order), with the foil–top-1 overlap stratum (O ≤ 0.5 diagnostic / O > 0.5 non-diagnostic), the D1/D2/N1 amendments, DELTA_BAR = 0.10, ALPHA = 0.05 primary (T-vs-R McNemar exact), Bonferroni 0.0125 others, Tango CIs. **One amendment (this draft only):** the bench-sanity step is split — baseline < 0.25 → **LINE-CLOSED** (second-HOLD stop rule), baseline > 0.75 → HOLD. Everything else in the table is identical.
- **Tier-0 bars:** median correct-rank > 5 → KILL (premise); n_pop < 12 → Underdetermined; tie rate > 0.25 → HOLD; tie rate [PINNED] = (# Tier-0 items where the correct option's logit is exactly tied — float32 exact equality — for the highest logit among the 8 candidates) / n_pop.
- **G1 real-tokenizer gate:** all 480 option strings single-token and intra-item-distinct under the REAL pinned EleutherAI/gpt-neox-20b tokenizer (revision hash recorded); failure → RUN-INVALID. The G1 verification from the MC bench transfers as a tokenizer-level property — the token pools are identical strings — but the attestation is re-confirmed against the pinned artifact before the cloze run (belt-and-suspenders, $0).
- **Foil-build blindness (Law #7, D3):** the structural-foil designations, build-time rationale, builder identity, and blindness-verification result transfer from the MC bench manifest (designation preceded all model passes; checker-verified items). No re-designation occurs — cloze re-prompting does not re-open foil selection. Any post-hoc foil change remains a disqualification, not a finding.
- **Degeneracy analysis + constant-data unit tests (LOG-4338):** all six tests re-run on the cloze rank/mask/McNemar machinery before bench contact (see §5).
- **Per-item records (Law #13), Δθ = 0 hash pre/post, environment + seed manifest, verdict discipline, summit-filter caveat** (masking is executor-applied, never autonomous; no cognition gloss on any CONTINUE).

---

## 2. Cloze bench spec (the only thing that changes)

### 2.1 Items and pools (unchanged)

- **The 60 items:** identical item ids, question texts, and 8 option strings from `experiments/runs/EXP104_Tier0_rank_screen/bench_manifest.json`. The checker-verified facts (64/66 VERIFIED, 2 replaced/dropped pre-run) and the structural-foil designations transfer with their manifest evidence. No item is added, dropped, or reworded on the basis of EXP104's MC results — rewording on pilot accuracy would be Law #9 post-hoc selection.
- **The 8 candidate tokens per item:** the same G1-verified single-token pool (pairwise distinct within an item). The option strings no longer appear in the prompt; they are the *scoring set*, not the *displayed set*.

### 2.2 Prompt template (pinned, frozen)

```
<question text verbatim> The answer is
```

- The question text is byte-identical to the MC bench's stem (no `Q:` prefix change, no reformatting — any stem edit is a new proposal, not a repair).
- The completion cue is the fixed string `The answer is` (single space after; no trailing space issues — the cue is pinned as a literal, template hash recorded in the run manifest).
- **Readout position [PINNED]:** the token position immediately following the completion cue — the scored logits are the next-token logits at that position. Readout-position index recorded in the manifest.
- **No option enumeration, no letters, no `Answer:` terminal.** The model completes from its own distribution; only the 8 candidate-token logits are scored.

### 2.3 What replaces the position control (and why)

**The correct-position shuffle is dropped, not replaced.** [INTERPRETATION] The shuffle existed to distribute correct answers across the 8 letter positions; with no letters and no displayed options, positions do not exist. There is no prompt-side ordering to randomize.

**What guards prompt-side confounds now [DEFINITION + justification]:**

1. **Cue constancy.** The completion cue is the same literal string on all 60 items. Any cue-driven bias (e.g., `The answer is` boosting particular token classes through training-data collocations) is therefore *constant across items* — it shifts the baseline level, which the sanity band [0.25, 0.75] adjudicates, but it cannot differentially favor the correct token on some items and not others. A confound that is constant across items is absorbed by the baseline; the MC letter prior was lethal precisely because it interacted with per-item correct-position assignment.
2. **No candidate-order parameter.** Because the 8 candidates never appear in the prompt, there is no order variable to pin or randomize — the design space where the MC position prior lived is removed by construction, not controlled.
3. **Pre-registered non-arm:** a cue-robustness sensitivity (re-running Tier-0 under an alternative cue) is explicitly NOT part of this draft. If Tier-0 lands inside the band, cue sensitivity is a listed §6 risk for the Law #14 reviewer to weigh, not a silent second instrument. Changing the cue after seeing Tier-0 is a new proposal.

---

## 3. Readout, rank, and tie-guard (cloze)

- **Scored decision:** argmax over the 8 candidate-token logits at the pinned readout position.
- **Correct-rank r_i:** the rank of the correct candidate token's logit among the 8 candidate logits (1 = top), computed at the readout position on the Tier-0 pass.
- **Ties (pre-registered):** float32 exact equality ties are broken by **ascending token id** (deterministic; recorded per item). The MC draft's option-index tie-break is inapplicable — option indices no longer exist. This change is mechanical (a total order is required) and is the only readout-logic change besides the position pin.
- **Tie-guard (carried over):** correct-option top-1 tie rate > 0.25 in Tier-0 → HOLD. Tie rate = (# Tier-0 items where the correct candidate's logit is exactly tied for the highest logit among the 8) / n_pop.
- **Margin note [OBSERVATION from EXP104, for context not adjudication]:** on the MC bench, failed items showed mean top1−correct margin 1.137 — a solid win consistent with a prior, not a near-tie. The cloze Tier-0 worksheet records the same margin statistic; a near-zero margin distribution would indicate tie-adjacent measurement noise the tie-guard does not catch (descriptive only).

---

## 4. Tier-0 bars (carried over) + the autopsy breaking point (new)

**Carried over (v3 §2.2, binding):**

| Bar | Condition | Verdict |
|---|---|---|
| Premise | median r_i over failed items > 5 | KILL (premise) — dead at $0 |
| Power | n_pop < 12 | Underdetermined — battery does not run |
| Instrument | tie rate > 0.25 | HOLD — rank instrument degraded |
| Sanity (upper) | baseline accuracy > 0.75 | HOLD — miscalibrated upward |

**New — the autopsy breaking point (LOG-4483 §3, binding here):**

| Bar | Condition | Verdict |
|---|---|---|
| Sanity (lower) / line stop | cloze Tier-0 baseline < 0.25 | **LINE-CLOSED** — I2′ untestable on Pythia-410m at $0 |

- **Rationale [INTERPRETATION]:** the MC bench already returned one HOLD (format artifact). A second sub-band baseline under the repaired readout means 410m-scale base LM lacks retrievable 2-hop factual chains under every $0 readout tried (word-scored MC and cloze). Further instrument surgery after two HOLDs is p-hacking the bench — the v3 §6 risk-6 backdoor warning, honored here as a pre-registered stop. LINE-CLOSED maps to *Inconclusive-for-the-line, terminal*: no verdict on the mechanism, no further S4-8′ work on this model, no third readout proposal.
- **Tier-0 passes:** 60 (one per item), ~1 min CPU, $0, Δθ = 0, deterministic seed-pinned. (The ≤120-pass MC figure is obsolete — no option-logit rebuild is needed; the cloze readout extracts all 8 candidate logits in the single completion pass.)
- **Battery budget (carried over, gated on Tier-0):** 60 × 4 arms = 240 decision passes + probes ≈ 360, hard cap 500. CEO clearance gates any run regardless of venue.

---

## 5. License, prediction, feasibility, degeneracy (cloze-instantiated)

- **Mathematical license [PROPOSITION]:** transfers from v3 §1 verbatim, instantiated for cloze: removing the option enumeration removes the position prior's support — the argmax is now over content tokens in a completion context, where no positional confound exists by construction (the letters were the confound's vehicle). The license's empirical precondition is a calibrated instrument: cloze Tier-0 baseline ∈ [0.25, 0.75]. If the baseline lands below 0.25, the precondition fails and the license is void — no battery may be built on this bench family.
- **Predicted band [HYPOTHESIS, not a claim]:** cloze Tier-0 baseline ∈ **[0.25, 0.45]**. Anchor: the MC bench's non-pos0 subset measured 0.233 with the prior only partially removed; full removal should add points. If the Cause-2 capability gradient (autopsy §2) dominates, the number lands near chance (0.125) instead — Tier-0 adjudicates between these, which is its job.
- **Feasibility algebra (EXP079 lesson, on paper):** before the battery, compute from cloze Tier-0: n_pop and the minimum flips for McNemar p < 0.05 (b=6, c=0 → p = 2/64 = 0.03125; b=5, c=0 → p = 0.0625, n.s.). The n_pop ≥ 12 gate enforces this. If the computation shows DELTA_BAR = 0.10 unreachable, the battery does not run (HOLD, not a silent edit).
- **Degeneracy analysis + constant-data unit tests (LOG-4338 lesson — re-run on the cloze machinery before bench contact):** (a) constant-logit input → rank function returns the ascending-token-id tie-break (unit test asserts); (b) masking a non-top-1 candidate never changes argmax on fixed logits (asserts); (c) masking top-1 promotes the previous runner-up on fixed logits (asserts); (d) b=c=0 → McNemar p=1.0 is a valid null, not an error; (e) empty failed set → Tier-0 vacuous → KILL (premise); (f) McNemar-exact implementation cross-checked against a reference (hand recurrence or scipy.stats) on the full (b,c) grid before any bench contact; mismatches void the statistics machinery. **(g, cloze-specific)** a synthetic prompt with all 8 candidate logits forced equal at the readout position yields r_i = rank by token-id order for the correct token — the tie-break path is exercised, not assumed.

---

## 6. Six ranked design risks (for the Law #14 reviewer)

1. **Completion-cue bias replaces the letter prior.** `The answer is` is a fixed string, but its training-data collocations may differentially boost certain *content* classes (e.g., country names over city names) across templates — a constant-ish but template-correlated bias the sanity band only partially adjudicates. Mitigation: cue is identical across all items (differential item-level bias impossible); the band and the per-template worksheet are descriptive diagnostics. Reviewer: confirm the cue choice is the least-loaded natural completion, or demand the cue be pinned with a named alternative pre-registered as a *descriptive* sensitivity (not a second instrument).
2. **Candidate-absent generation concentrates on frequency priors.** Without the option list in the prompt, the model's argmax over the 8 candidates may collapse onto one high-frequency token (e.g., the same country for every item) — a content-frequency prior, not item knowledge. The rank instrument still measures (ranks 1–8 are well-defined), and a collapsed readout routes honestly to the sanity band; but the reviewer should confirm the per-item top-1 distribution diagnostic is in the worksheet (§7 item 3) and that a collapsed distribution with baseline < 0.25 closes the line rather than inviting a "better cue" repair.
3. **Comparing cloze to MC as a finding (Law #9).** The cloze Tier-0 number and the MC Tier-0 number (0.183) will both exist; treating their difference as a measured "prior-removal effect" is post-hoc metric storytelling across two uncalibrated instruments. The MC number is calibration context for the autopsy only — it must never appear as a primary or secondary result of any S4-8′ run. Reviewer: confirm the draft forbids this explicitly (§8).
4. **Rank-machinery validity under generation vs enumeration.** The MC rank function scored tokens the prompt had just displayed (copy-primed logits); the cloze rank function scores unprompted candidates. The degeneracy suite (§5) is re-run, but the reviewer should confirm test (g) genuinely exercises the generation-context path and that no MC-derived constant (e.g., the 120-pass budget, the option-index tie-break) leaks into the cloze code path.
5. **Tier-0 power under a harder task.** Cloze removes the option cueing the MC format provided; accuracy may land below 0.25 even if partial 2-hop knowledge exists — the LINE-CLOSED bar is honest about this but irreversible. Reviewer: confirm the 0.25 lower edge is the right sharp line (chance is 0.125; 0.25 = 2× chance) and that closing the line on a sub-band number is preferable to a second recalibration.
6. **Single-cue rigidity.** The entire bench hangs on one completion string's interaction with a base LM. This is pre-registered and frozen (changing the cue after Tier-0 = new proposal), but the reviewer should confirm the template-pin (§2.2) is tight enough that "the cue didn't work" cannot become a backdoor to re-prompting until the bench passes — the LINE-CLOSED rule is the enforcement.

---

## 7. Scope fence

- **EXP085's kill is untouched** (binary construct stays dead); **the S4-8 v3 draft is untouched** (its MC pre-reg continues on its own track — this draft neither amends nor supersedes it). S4-8′ is a different proposal commissioned from the EXP104 autopsy, not a branch of v3.
- **The position-A prior is a measured confound of the MC instrument, not a finding about the model.** Recorded: 30/60 top-1 picks at position 0 (binomial p=2.02e-12 under no bias), uniform across all 10 templates (2–4 pos0-picks per 6-item block), 4/11 correct items at position 0 vs 3.0 expected under a pure position prior. This design removes the confound's vehicle (the enumeration); it does not claim the model "has" or "lacks" a position preference as a cognitive property.
- **No autonomy claim:** masking is executor-applied. A CONTINUE licenses only "target-free top-1 masking rescues decisions on this cloze bench" — never "the model knew the answer."
- **No generality** beyond the k=8 2-hop cloze bench, Pythia-410m, frozen backbone. No L11 direction is involved; the S6 stand-down is a different lane.
- **EXP092 reconciliation (carried):** information presence (trained probe, 33.33%, 6.7× chance) ≠ information routability (zero-shot generation head). A cloze LINE-CLOSED does not retract EXP092; a cloze CONTINUE does not upgrade EXP092's presence claim to routability.

---

## 8. Guards (pre-registered)

- **Δθ = 0:** weight hash pre == post; mismatch voids the run (Law #13).
- **G1 gate:** re-confirmed against the pinned EleutherAI/gpt-neox-20b artifact (name + revision hash in the attestation) before any cloze pass; failure → RUN-INVALID.
- **Foil blindness:** transferred from the MC manifest; no re-designation; post-hoc change = disqualification.
- **No MC↔cloze comparison as a result:** the 0.183 MC baseline is calibration context (autopsy) only; it is not a primary, secondary, or descriptive result of any S4-8′ run. Violation = Law #9 breach.
- **Prompt freeze:** the §2.2 template is pinned at pre-reg; any cue, stem, or formatting change after SIGN is a new proposal, never a silent edit (Law #4).
- **Per-item records, seed pinning, $0 for this draft:** as v3 §4. No model runs, no weights, no GPU contact, no signed artifact modified in writing this draft.

---

## 9. Instrumentation spec (pre-registered)

Every run persists (append-only, hashed):
1. `per_item_records.csv`: (item id, arm ∈ {B,T,F,R}, top-1 decision, correct-rank r_i, 8 candidate-token logits, masked token id or none, ΔM components vs B, top1−correct margin).
2. Cloze bench manifest: 60 item ids → question text hash, the 8 candidate strings + token ids, REAL-tokenizer re-attestation (name EleutherAI/gpt-neox-20b + revision hash), transferred structural-foil designations + blindness-verification reference (MC manifest), frozen prompt-template literal + hash + pinned readout-position index, lineage pointer to the MC manifest (items reused; measurements not reused).
3. Tier-0 worksheet: failed-item list, r_i values, median, n_pop, tie rate (ascending-token-id tie-break), baseline accuracy with the §4 bar evaluations, per-template accuracy table (descriptive), per-item top-1 distribution (collapse diagnostic, §6 risk 2).
4. Δθ = 0 hash pre/post; environment + seed manifest (Law #13).
5. Masking/rank/McNemar unit-test log: the seven §5 tests, PASS/FAIL each.
6. Decision-table worksheet: the step reached, evidence cell per condition, foil–top-1 overlap O and the D2 stratum report, stratum table of all five contrasts (ΔM, b/c/p, Tango CI) on Tier-0 pop + full bench.

---

## 10. What this draft does NOT do

- Does not sign anything; does not authorize a run; does not book any compute.
- Does not mint an experiment number (reserved for the Law #14 signing lane + CEO license).
- Does not modify the S4-8 v3 draft, any signed protocol, the EXP104 bundle, or any weights.
- Does not invent numbers — every cited value comes from the autopsy (LOG-4483) or the v3 draft; the cloze construct (§2–§3) is the fresh design this draft exists to specify.

---

## 11. Next steps

Independent **Law #14 review** of this draft (separate lane — NOT commissioned here) → SIGN → CEO execution clearance → cloze Tier-0 (60 passes, $0) → (gates) → battery. **Pilot NOT authorized until all complete.** The Law #14 reviewer receives the six §6 risks as the ranked review agenda.

*Draft prepared 2026-09-28 by the S4-8′ cloze pre-reg DRAFT lane (pre-assigned LOG-4484), commissioned from the EXP104 bench autopsy (LOG-4483). v3 (`S4-8_PREREG_DRAFT_v3_2026-09-28.md`) preserved untouched. DRAFT, UNSIGNED. On paper only, $0 compute. No signed protocol file was edited; this is a new unsigned file. Awaiting independent Law #14 review.*
