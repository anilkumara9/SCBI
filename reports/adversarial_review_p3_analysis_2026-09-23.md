# Adversarial Review: P3 ($0) Anti-Steerability Analysis

**Reviewer role:** Adversarial Reviewer (Law #14)
**Date:** 2026-09-23
**Document under review:** `research/innovation/P3_ANALYSIS_2026-09-23.md`
(banner: ANALYSIS — PENDING ADVERSARIAL REVIEW — NOT A FINDING; LOG-097)
**Proposal:** sprint New Idea 3, `research/innovation/SPRINT_2026-09-23.md` §"New Idea 3",
ACCEPTED with conditions (adversarial review 2026-09-23)
**Verdict:** **ENDORSE-WITH-QUALIFICATIONS** (4 qualifications, §6 — Q1 load-bearing)

---

## 0. Review method

Law #14 requires attempting to break the work, not merely reading it. I did not
re-read the analyst's numbers and nod; I recomputed them:

- Independently recomputed (b, c) per condition from
  `exp066_instance_evaluations.json` (60 records, 0 missing fields — verified);
  checked against the summary JSON's `stage_B_conditions` for every matched
  condition and against the analyst's §4 table. **All match exactly.**
- Independently recomputed per-instance mean margin shifts, sd, and
  positive-fraction per condition; checked against the analyst's §5 table.
  **All match to the reported precision** (means +0.0090/−0.0406/+0.7492/
  +0.0031/−0.0205; sds 0.0303/0.0157/0.0381/0.0173/0.0196).
- Independently verified the 8 bridge-rescued item ids and the two
  random-seed flips (both `pythia410m_planet_2hop_9`, also bridge-rescued).
  **Match the analyst's §4 list exactly.**
- Recomputed Stage A raw cosines: EXP065 {0.7379, 0.7144, 0.6996, 0.7224},
  mean 0.7186, spread 0.038; EXP066 {0.6734, 0.5652, 0.7248, 0.7776},
  mean 0.6852, spread 0.212. **Match §6.**
- Script forensics: EXP065's `results_json` (script lines ~660–676) contains
  only aggregate tables — no per-instance file is written (analyst's
  "MISSING" claim confirmed). EXP066's script issues exactly two
  `json.dump` calls (results payload, instance records) and zero
  `torch.save`/`np.save` — `v_hat_by_vocab` is in-memory only
  (lines 146–152, consumed at 200–202). **The "uncomputable coherence half"
  is forensically confirmed, not asserted.**

No numbers were generated beyond recomputation. No primary artifacts were
touched.

---

## 1. The self-flagged weakness: the Tan-gap / tautology attack

**The hostile case, steelmanned.** Tan's "anti-steerable" is logit-difference
opposite to intent (~1/3 of items). The analyst defines anti-steerability as
decision flips (McNemar corruptions c). The sprint's own adversarial review
*predicted* the degenerate branch would fire trivially because b=c=0 was
already established. So the 0.0% result was baked in: the gate is defined in
terms of a quantity known to be zero, the answer was knowable before the
analysis ran, and the "premise withdrawn" verdict is therefore tautological.
Meanwhile the level where Tan's harm actually lives — logit margins — is
declared off-limits by the program's own Finding 3, so the analysis answers a
question Tan never asked and claims the unreliability literature "does not
apply."

**Ruling: the tautology charge fails; a scoped version of the concern survives
as Qualification Q1.**

Three reasons the charge fails:

1. **The operationalization was pre-registered, not post-hoc.** The sprint's
   "Endpoints" section for P3 states verbatim: "Per-sample signed outcome
   ledgers (not margins — the ledger is decision changes, which already
   satisfies O5)." The flips-only gate is the *accepted* operationalization.
   The analyst did not choose it to guarantee a result; choosing the
   logit-level version would have violated the program's binding endpoint
   hierarchy (Law #9; audit Finding 3, now program law via the applied
   corrections). Under Law #14, attacking the analyst for following the
   accepted pre-registration is attacking the wrong document — the objection
   belongs to the proposal review, which already accepted it.

2. **The definition does not guarantee the result; the world did.** A
   flips-only gate does not entail c=0. Had static B_agg corrupted 20 of 60
   items, the >15% branch would have fired and the signed evaluators would
   have needed amendment. The degenerate branch was *predicted likely*, not
   *entailed* — the sprint said "nearly guaranteed," and the analyst still
   had to check every condition, including the 5 random-rotation seeds whose
   per-seed (b, c) were not all pre-determined in the aggregates (see §4).

3. **The result excludes a real alternative explanation.** The question P3 was
   chartered to answer is: "is static CAA's failure partly mismeasurement —
   does aggregate ΔM=0 mask per-sample harm?" The answer, at the decision
   level the program's endpoints license, is now *no*: c=0 means literally
   zero corruptions across 60 instances × 10 conditions. "Mismeasurement via
   masking" is a specific, previously-open alternative to the standing null,
   and it is now closed. That is information, not tautology.

**What survives.** The analysis answers the *decision-level* version of Tan's
question and is barred by program law from answering the logit-level version.
The §5 margin data *shows* logit-level nudges exist (static B_agg shifts
margins positively, p=0.041; B_wrong shifts them negatively, p≈1.2e-08) —
Finding 3's entire point is that these nudges are decision-irrelevant, not
that they don't exist. The report's withdrawal language must therefore carry
the decision-level qualifier wherever it travels (M2.5: conditional results
name their condition in every citation). See **Q1**.

---

## 2. Standard battery

### (a) Branch-chain soundness

The accepted tree triggers a harm-ledger amendment (and Law #14 re-review)
**only** on the >15% branch. Observed: 0.0% for every condition in both runs.
The >15% branch did not fire; the middle band did not fire. **No amendment is
required, and no re-review is triggered — the chain is sound.**

The missing EXP065 per-instance ledger does not weaken this: the gate
computes c/N, and EXP065's aggregates give `corruptions_c = 0` exactly, so the
fraction is 0% with no item identity needed. The analyst is explicit that
item-level EXP065 analyses are *permanently foreclosed* (§8) — correct, and
the Law #13 lesson is logged, not buried.

The uncomputable coherence half: the proposal named coherence "the real
payload" and the archive cannot run it. The analyst records the
premise-withdrawn branch as a **partial firing** (fraction leg met
degenerately; coherence leg open, §7.4) and refuses to claim "coherence high"
from the anisotropy-confounded raw-cosine proxy. This is the honest handling;
claiming the full conjunction would have been condition-laundering. See
**Q2** for the one wording repair needed.

M5.2 note: the accepted tree did not explicitly name the mixed-feasibility
case (one run ledgered, one not). The analyst's resolution — EXP065's
fraction from exact aggregates, since c=0 is algebraically sufficient for the
gate — is sound, disclosed, and introduces no executor discretion over any
branch outcome. No finding.

### (b) Over-claim check

- §8 "corroborated at the per-sample level: it is not an average masking
  corruptions." Licensed: this is exactly what c=0 everywhere establishes,
  against the masking alternative. It does not strengthen the null against
  other alternatives, and the report does not claim it does.
- §4's "[INTERPRETATION] A borderline item, movable by unstructured noise —
  chance, not signal." The *borderline-item* reading is well-supported (the
  bridge also rescues `planet_2hop_9`; the item sits near the decision
  boundary under two unrelated perturbations). The "chance, not signal" gloss
  is unnecessary — two independent seeds landing on the same item is mildly
  surprising under pure chance — but it is labeled [INTERPRETATION] per
  Law #11, so this is a style note, folded into **Q4**.
- §5's "confirmed from the per-instance records to be decision-irrelevant"
  is consistent with the audit's Finding 3 and labeled interpretation.
- No claim exceeds the "NOT A FINDING" banner. The DOES-NOT-LICENSE list
  (§8) is unusually careful: no forward-looking 0% claims, no coherence
  claims, no EXP065 item-level resurrection.

### (c) Observation/interpretation separation (Law #11)

Labels are used consistently throughout: [OBSERVATION] for recomputed
values and archive contents, [INTERPRETATION] for readings, [ASSUMPTION] for
the static-B_agg intent definition and the proxy confound, [OPEN] for the
per-pair agreement question, [NOTE] for the Tan gap, [EXPLORATORY] for §5.
The §6 proxy paragraph labels its own confound *before* drawing the
limited inference — the correct order. **Pass.**

### (d) Sequencing

The sprint mandated P3 before any EXP068/070 execution. The analysis is
complete; the remaining gate was *this review*. **With this verdict, the P3
sequencing mandate is discharged.** The report's §8 is honest that review was
the remaining gate. See **Q3** for the required scoping of "may proceed":
it discharges the P3 blocker; it does not clear anything else, and each
signed protocol's own pre-registered halt gates still bind at execution.

This also resolves the recorded P3/EXP070 sequencing conflict: P3 was
completable from the archive without GPU, and is now complete and reviewed.
EXP070 execution is no longer sequenced behind unfinished P3 work.

### (e) Threat to the standing boundary result

None. The analysis *corroborates* the decision-level null (raw cross-vocab
cosine ~0.7, zero causal transfer under static injection) against the
masking alternative. The coherence proxy's high aggregate cosines are
correctly refused as evidence (anisotropy confound, Idea-5 hygiene). The §5
margin data re-confirms Finding 3, which underwrites the endpoint hierarchy
the boundary result rests on. **The boundary result is untouched and
slightly strengthened.**

---

## 3. What the analysis genuinely added (non-pre-determined content)

For the record, not all of this was fully baked into the aggregates:

- The per-seed random-rotation item identity: the summary's b=0.4 average
  resolves to exactly two rescue events, both on `pythia410m_planet_2hop_9`,
  both rescues (c=0), on an item the bridge also rescues. This rules out
  "random noise corrupts items" even in the noise control and identifies a
  genuinely borderline item. Small, real, and not available from the summary
  JSON.
- The forensic confirmation that EXP065's per-instance records are
  irrecoverable (script writes aggregates only) — a permanent archive fact
  with Law #13 consequences, now logged rather than assumed.

---

## 4. Findings on the analysis (severity per the charter)

- **No FATAL findings.** No cross-space operator claims, no shape errors —
  the document makes no operator claims at all; its mathematics is
  arithmetic on archived (b, c) counts.
- **No MAJOR findings.** The decision tree was followed; no branch outcome
  was altered; no condition was laundered (the coherence leg is explicitly
  left open).
- **Qualifications below (MINOR, wording/citation hygiene):** the numbers,
  branch firings, and disclosures are sound; the fixes constrain how the
  conclusions may be *cited*, not what was *found*.

---

## 5. Verdict: ENDORSE-WITH-QUALIFICATIONS

**ENDORSE** the analysis's results and branch firings: anti-steerable
fraction 0.0% for every condition in both runs; degenerate branch fires;
premise withdrawn on the fraction leg; no >15% branch; no harm-ledger
amendment required; no Law #14 re-review triggered; coherence unmeasured and
recorded open; P3 sequencing mandate discharged.

**WITH THE FOLLOWING QUALIFICATIONS** (to be applied by the analyst/CEO as
in-place wording repairs; the analysis file itself must not be silently
rewritten — repairs as dated addenda or explicit edits with changelog, per
Law #5/#12):

**Q1 (load-bearing) — scope the withdrawal claim to the decision level.**
§7.2's "no hidden harm, no mismeasured aggregate" and "the unreliability
literature does not apply to our setting" must carry an explicit
decision-level qualifier wherever they appear, with a pointer to §9.1 in
§7.2 itself — not two sections later. Required sense: "Tan-style
aggregate-masking does not afflict our *decision-level* verdicts; logit-level
nudges exist (§5) and are excluded as *endpoints* by Finding 3, not shown
absent; Braun's coherence concern remains open." Without this, a future
agent or reader could cite P3 as refuting Tan/Braun at the logit level where
their constructs actually operate — the exact condition-laundering M2.5
forbids.

**Q2 — align the headline with the accepted conjunction.** The proposal's
kill criterion was a conjunction (fraction ≤5% **AND** coherence high). §7.2's
headline "The methodological premise is WITHDRAWN" must not be citable
without the §7.4 partial-firing statement adjacent to it: withdrawal fires
on the fraction leg; the coherence leg is open. One sentence of adjacency
fixes it.

**Q3 — scope the sequencing license.** §8's "EXP070 and EXP068 may proceed
to execution on their signed protocols" discharges *the P3 sequencing
blocker only*. It must be read with: each protocol's own pre-registered
halt gates still bind at execution time, and EXP068 has no execution bundle
yet — "may proceed" is not clearance to run EXP068, which remains gated on
its own bundle construction and review.

**Q4 (minor; style per Law #11) — drop the "chance, not signal" gloss.**
The analysis's gloss on the bridge rescues as "chance, not signal" is an
interpretive adjective the numbers do not need; remove it and let the
(b, c, p) statistics carry the claim.

---
*[CEO completion note 2026-09-23: the reviewer's deliverable as written ended
mid-sentence at "gates (hal" with a truncation marker; Q3's completion and Q4
above are completed from the reviewer's own delivered verdict summary (handoff
2026-09-22T21:40:13Z), which stated all four qualifications in substance. No
wording beyond that summary has been invented. — CEO]*
...[truncated 1192 chars]