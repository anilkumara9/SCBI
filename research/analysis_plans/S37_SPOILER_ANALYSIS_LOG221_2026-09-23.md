# LOG-221 — S3-7 Spoiler-Suppression Archived-Record Analysis

**Track-6 data analysis | LOG-221 (pre-assigned) | 2026-09-23**
**Hypothesis under test (S3-7, [HYPOTHESIS]):** the bridge rescues by *suppressing
whichever token the baseline predicted* (competitive elimination), not by
directional alignment with target or foil rows.
**Guards:** $0 · 0 forward passes · archived records read-only · no data invented.
**Verdict:** **Underdetermined** — predicted-token labels are absent from every
archive; the hypothesis neither survives nor dies, stays queued.

---

## 0. Honest headline

The archives cannot answer the question. EXP077, EXP066, and EXP065 record only
per-arm *binary correctness* (plus scalar `margin_shift` deltas in EXP066) — no
per-item predicted-token labels, no top-1 token ids, no foil-vs-third-token
field exists anywhere in the three run archives. The pre-registered tabulation
(foil vs third-token majority on rescued items) is not computable from archived
data. This analysis changes no belief: before this work, the candidate's
expected fate was already written in its own backlog row ("Archived labels
absent → Underdetermined (stays queued)"). What it converts is an *assumption*
into a verified [FACT], and it leaves behind the exact instrumentation spec a
future run must archive so S3-7 can actually be adjudicated. Call this what it
is: infrastructure bookkeeping, not discovery. The ambition question — *could
this change what anyone believes?* — answered in writing: **no.**

## 1. Read before writing (knowledge protocol §1 compliance)

| # | What I read | What it contributed |
|---|---|---|
| 1 | `reports/research_log.md` LOG-217 | EXP082-EXONERATED verdict; exact numbers (k_a=k_f=0/60, CP CI [0, 0.0596]); the foil-suppression kill and the death-debt that created S3-7 |
| 2 | `research/innovation/CANDIDATE_BACKLOG.md` S3-7 row | The hypothesis, its pre-registered reading tree, its $0 archived-record test plan |
| 3 | `research/TEAM_KNOWLEDGE_PROTOCOL.md` §1 (structure) | Mandatory reading-list architecture; confirms this dispatch's proportionate reading scope |

## 2. Pre-compute prediction (direction + magnitude + breaking point, in writing)

**Prediction:** labels absent in all three archives. Rationale [INFERENCE]: no
runner spec in the EXP065→EXP082 lineage ever defined a per-item
predicted-token archive field; endpoints were binary correctness and scalar
margin shifts. **Breaking point:** even a labels-present, third-token-majority
finding could license only "H survives, earns pre-registration" — never a
mechanism claim (see §5 steelman). The achievable verdict space was bounded to
{Underdetermined, at-best hypothesis-survival} before a single file was opened.

## 3. Schema findings [FACT]

### EXP077 — `experiments/runs/EXP077_cone_vs_line/exp077_instance_records.json`
- Array of 60 records. Fields per record: `item`, `ent`, `typ`, `correct`,
  `rescue_indicators`. Nothing else.
- `correct`: dict of 10 booleans keyed by arm (`C1`, `C2_a025`, `C3_a050`,
  `C4_a100`, `C5_a200`, `C6_offset`, `C7_Bwrong`, `C8_bridge`, `C9_cone`,
  `C10_control`).
- `rescue_indicators`: dict of 8 integer 0/1 flags (geometry-arm contrasts,
  all 0 on inspected items).
- **No predicted-token labels, no top-1 token ids, no token strings, no logit
  vectors, no margin fields.** A programmatic scan for key fragments
  (`token`, `label`, `pred`) returned zero fields.
- Rescued items (C1 wrong → C8_bridge right): **14 of 60** [FACT]. These are
  the items the tabulation would have consumed; the tabulation column
  (baseline predicted token) does not exist.

### EXP066 — `experiments/runs/EXP066_pythia410m_replication/exp066_instance_evaluations.json`
- Dict of 60 items (`pythia410m_planet_2hop_0…`, `…_3hop_…`). Fields per item:
  `prompt`, `base_correct`, and per-arm `{arm}_correct` booleans plus
  `{arm}_margin_shift` scalars (Static_B_agg, Aligned_Dynamic_Basis,
  Same_Layer_Output_Bridge, Random_Rotation_Seed_0–4, Dynamic_B_perp,
  Dynamic_B_wrong).
- **No token labels.** `margin_shift` is a signed scalar delta (mean values
  reported in LOG-217: e.g. bridge arm 0.6394/0.6885 mean/max); it encodes no
  token identity and cannot reconstruct which token the baseline predicted.
- Rescued items (base wrong → Same_Layer_Output_Bridge right): **8 of 60**
  [FACT] — likewise untabulable.

### EXP065 — `experiments/runs/EXP065_coordinate_alignment/exp065_results.json`
- Single aggregate dict (12 top-level keys: hashes, layer, sample_size,
  baseline_accuracy, stage A/B/C results, criteria). No per-item records at
  all. Nothing to tabulate.

**Bottom line [FACT]:** no archive in the EXP065/066/077 lineage stores the
baseline's predicted token on any item.

## 4. The pre-registered tabulation

Not computable. The pre-registered reading tree was:

- labels present + baseline=foil on majority of rescued items → H killed
- labels present + third-token majority → H survives, earns pre-registration
- **labels absent → Underdetermined** ← this branch fired.

No counts, no CIs to report — reporting any would be invention.

## 5. Steelman at full strength (then answered)

**The steelman:** *Even if the archives had contained labels and shown a
third-token majority on rescued items, that finding would not license the
spoiler mechanism — and the dispatch's own reading tree overstates what the
tabulation can buy.*

1. **Binary records can't show margins.** A tabulation records *which* token
   won, not *how close* the race was. Suppression is a margin phenomenon: it
   predicts the competitor's logit *falls* under the bridge. A
   foil-vs-third-token count cannot distinguish "bridge demoted the baseline's
   top-1 competitor" from "bridge left the competitor untouched and the target
   rose past it" — the latter is re-routing, a different mechanism with the
   same observable.
2. **Suppression vs re-routing are observationally identical in correctness
   records.** Both predict baseline-wrong → bridge-right. The tabulation's
   only added information is the identity of the baseline's error — which is a
   fact about the *baseline*, not about the *bridge*. Inferring the bridge's
   mechanism from the baseline's error distribution is a category error: it
   attributes to the intervention what belongs to the pre-intervention state.
3. **Selection bias confound.** Items where the baseline confidently predicts
   the foil vs diffusely predicts a third token differ in difficulty and in
   baseline entropy. A third-token majority among rescued items could reflect
   that hard items (low baseline confidence, scattered errors) are the ones
   the bridge can rescue — a selection effect on item difficulty, not evidence
   of competitive elimination.
4. **Foil-exoneration doesn't transfer.** EXP082 killed *foil*-suppression
   geometry; S3-7 needs its own causal endpoint, and the tabulation is not
   one. "The foil wasn't the competitor" does not entail "the actual
   competitor was suppressed."
5. **Verdict discipline.** Under the adopted evidentiary standard, the only
   permitted verdicts are Supported / Not supported / Inconclusive /
   Underdetermined / Refuted. A correlational tabulation — even a clean one —
   cannot reach "Supported" for a mechanism claim; at most it warrants a
   pre-registration. The reading tree's "earns pre-registration" phrasing is
   correct only if read as *hypothesis survival*, never as *mechanism
   support*.

**Answer (partial concession, partial tightening):** concede points 1–4 in
full — the tabulation, had it existed, would have been an *observational
pattern*, not a mechanism test, and the reading tree should have been
explicit that third-token majority licenses only a *refined* pre-registration,
not a survival verdict with momentum. The conceded refinement, recorded as a
standing requirement: **any future S3-7 pre-registration must carry a causal
endpoint, not just the tabulation** — specifically, on rescued items, the
Δlogit of the baseline's top-1 competitor under bridge vs under a
random-rotation control. Competitive elimination predicts
competitor-specific demotion under the bridge *beyond* the control; re-routing
predicts target promotion without competitor demotion. That is the
discriminating experiment; the tabulation alone is its screening step.

## 6. What a future instrumented run must archive (exact spec)

To adjudicate S3-7, a future run (new experiment number, signed protocol,
pre-registered before execution) must archive per item, per arm (at minimum
C1 baseline, C8_bridge, and one inert control such as random rotation):

1. **Top-k predicted tokens (k ≥ 5):** token strings + token ids + raw logits.
2. **Baseline top-1 competitor identity:** the token id/string of C1's top-1
   prediction (this is the column S3-7 needs).
3. **Margin decomposition:** logit(target) − logit(top-1 competitor), per arm —
   the scalar EXP066 archived is insufficient without the competitor identity.
4. **Runner decision-rule version + pre/post weight hashes** (Δθ=0 discipline
   unchanged; Law #7 leakage audit applies — archiving logits touches the
   readout path, and the open K1 readout-bias decision (§H7) must be settled
   before this instrumentation is licensed).
5. **Prompt text and item id** (EXP066 already does this; EXP077's
   entity-grouped records should carry the full prompt string too).

Without (1)–(3), S3-7 cannot leave Underdetermined. With them, the licensed
test is: competitor-logit-drop (bridge vs control) on rescued items +
the foil-vs-third-token tabulation as the screening step.

## 7. Verdict and what it licenses

**Verdict: Underdetermined.** Predicted-token labels are absent from the
EXP065, EXP066, and EXP077 archives; the foil-vs-third-token tabulation on
rescued items (14 EXP077 items, 8 EXP066 items identified as the tabulation
population) is not computable.

**What this licenses next:**
- **NOT** a pre-registration of the spoiler mechanism — the hypothesis has
  earned nothing new; it stays queued exactly where S3-7's row left it.
- **YES** to attaching the §6 instrumentation spec to S3-7's backlog row, so
  the next runner build archives what adjudication requires.
- **YES** to tightening the future reading tree: any S3-7 pre-registration
  must include the competitor-logit-drop causal endpoint (bridge vs control),
  not the tabulation alone (per the §5 concession).

## 8. Knowledge-protocol contributions

- **One challenge:** S3-7's own backlog row pre-priced this outcome ("Archived
  labels absent → Underdetermined (stays queued)"). Dispatching a full
  analysis for a pre-priced outcome is defensible only as *verification* — the
  schema had to be checked, not assumed — but the lab should be honest that
  this was schema QA, and route future "check the archive" dispatches with
  that label and proportionate effort rather than as mechanism work.
- **One idea:** the competitor-logit-drop endpoint (§5.5/§6) generalizes
  beyond S3-7: any future "suppression vs promotion" mechanism dispute in the
  bridge program (including the K2 routing/bypass pilot gated on K1) should
  pre-register the same Δlogit-of-the-baseline-winner (bridge vs control)
  contrast. It is the program's first reusable readout-side causal endpoint
  now that the static directional-readout story is dead (EXP082).

---

*Author: Track-6 data analyst (LOG-221) · 2026-09-23 · $0 · 0 forward passes ·
archived records read-only · no data invented.*
