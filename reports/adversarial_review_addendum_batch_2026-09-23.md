# Law #14 Adversarial Review — Addendum Batch (LOG-200 / LOG-201 / LOG-202 / LOG-199)

**Reviewer:** Track 7 adversarial scientist · **LOG-203** · 2026-09-23 · CPU/$0, docs only
**Scope:** one combined Law #14 pass over four new artifacts. Read in full; every
finding below carries section-level (and where possible line-level) evidence.
**Review standard:** honest labels, verifiable numbers, no overreach, no fabricated
citations, no silent edits to signed artifacts, FACT/INFERENCE/HYPOTHESIS/SPECULATION
layer respected.

**Verdicts:** LOG-200 — SIGN-WITH-FIXES · LOG-201 — SIGN-WITH-FIXES ·
LOG-202 (playbook + ledger) — SIGN-WITH-FIXES · LOG-199 — SIGN-WITH-FIXES.
No REJECTs: every defect found is reparable without changing the artifact's core
verdict; nothing fabricates, nothing silently rewrites a signed protocol.

---

## Artifact 1 — `research/foundations/MATHEMATICAL_LICENSE_STANDARD_2026-09-23.md` (LOG-200)

**Verdict: SIGN-WITH-FIXES** (2 required fixes, 1 note). The rubric is sound, the
template is enforceable, the worked example's numbers check out against the executed
audit report, the addenda recommendation is the correct way to handle queued
protocols, and all cited papers are real with faithful summaries.

### What holds up (checked against primary sources)

**R1. License-grade rubric (§A.3) is coherent.** The ordering PROVEN-LEMMA >
CITED-THEOREM > IN-HOUSE-PROOF > CONJECTURE-UNDER-TEST > INTUITION(disqualifying)
scales authorization with proof + adversarial-review status. The three grade-discipline
rules are enforceable *procedurally*: author assigns → Law #14 reviewer verifies
under Charter M1–M8 → mid-protocol upgrades are new appended licenses (not edits) →
downgrades automatic on undiscovered assumptions (Charter M2.3) → logged in
`reports/research_log.md`. The INTUITION-disqualifies rule is not a slogan: the
template (§A.4) has no INTUITION option, and the worked example demonstrates a
license naming its own failure mode (the E2 "label-free construction path" falsifier).
✓

**R2. Worked-example numbers match the executed audit report**
(`research/analysis_plans/LAW7_BRIDGE_AUDIT_REPORT_LOG197_2026-09-23.md`), item by item:
- α: "EXP065/066: α=1; EXP070/077: α=0.50" — report §1: "EXP065 1.0, EXP066 1.0,
  EXP070 0.50 (`ALPHA`), EXP077 0.50 (`ALPHA_BRIDGE`)". ✓
- 60 items × 4 runs — report §1 table: 60 each, 240 checks. ✓
- `|cos| ≥ 1−1e-6` — report: min |cos| = 1.0000000 over all 240. ✓
- Norm relative error ≤ 1e-5 — report: 1.192e-07 (max). ✓
- "EXP070's vectors are UNVERIFIED... Underdetermined" — report §3(c) E3:
  EXP070 vector-consistency Underdetermined (no byte-identical mirror). ✓
- The companion Law #7 compliance criterion (Q1=Supported ⇒ non-compliant *by
  definition*) — report §5: "Law #7 compliance: **non-compliant on the letter**".
  The example's pre-registered "breaking point cuts against the author's hopes"
  is exactly what the executed report did. ✓

**R3. §A.6 addenda-vs-reregistration is sound and touches nothing signed.**
Addenda are "appended, dated, signed, Law-#14-reviewed" — the program's standing
correction discipline (propose, never silently apply). The recovered licenses are
genuinely in the signed text, not invented: EXP080's "bridge ceiling, not pool
ceiling" collapse is verbatim the signed spec's (d)/(e) rows
(`experiments/protocols/G2_ORACLE_CEILING_PREREG_SPEC.md` ll. 567–568); EXP081's
regrouping identity and the `cos = 0.9999999999999998` corroboration are in the
signed v2 spec (ll. 115, 461) and the JSON twin
(`experiments/protocols/C-A_PREAUDIT_2026-09-23.json:816`). ✓

**R4. Citations verified live (Law #3), summaries faithful:**
- Merrill & Sabharwal, "The Expressive Power of Transformers with Chain of
  Thought," arXiv:2310.07923 — real (arXiv abs page fetched 2026-09-23; submitted
  11 Oct 2023, ICLR 2024). Abstract confirms the P1 summary: log steps add
  little; linear steps (projected pre-norm) recognize all regular languages
  under standard complexity conjectures; polynomial steps recognize exactly P. ✓
- Wang et al., "Self-Consistency Improves Chain of Thought Reasoning in Language
  Models," arXiv:2203.11171 — real (fetched; ICLR 2023). Abstract's numbers match
  the P4 numbers exactly: GSM8K +17.9, SVAMP +11.0, AQuA +12.2, StrategyQA +6.4. ✓
- P2's TACL citations — both real: Merrill & Sabharwal, "The Parallelism
  Tradeoff," TACL 11:531–545 (2023) (arXiv:2207.00729; page range matches);
  Merrill, Sabharwal & Smith, "Saturated Transformers are Constant-Depth
  Threshold Circuits," TACL 2022 (arXiv:2106.16213). ✓

**R5. Honest admissions correctly stated.** B.3(1): the oracle bound P3 is "nearly
vacuous" (forbids only information creation, not recomposition — P4 is the standing
counterexample). B.3(3): P1/P2 are ∃θ, not fixed-θ ("'∃θ: CoT helps' does not imply
'for our frozen θ, N more steps add capability C'"). The category-error guard is
explicitly imported into the license template's applicability check. ✓

**R6. 10-label standard applied.** Load-bearing claims carry [FACT]/[DEFINITION]/
[PROPOSITION]/[CONJECTURE]/[INTERPRETATION]/[OPEN] per `AGENTS.md` §5, plus the
mentor FACT/INFERENCE/HYPOTHESIS/SPECULATION layer where the fact/inference line
is crossed. Law #15's four answers are present and binding at the document head. ✓

### Required fixes

**F-200-1 (required) — §A.5 L2 repeats a false quantitative claim.**
The paragraph states: "1e-6 is three orders of magnitude above float32 unit
roundoff (~1.2e-7 per op on unit vectors)". Arithmetic: 1e-6 / 1.2e-7 ≈ **8.4× —
less than one order of magnitude, not 10³×**. The phrase is quoted faithfully
from the signed LOG-197 plan (plan ll. 73–74), so this is the plan's error, not a
fabrication — but a *foundations standard on mathematical rigor* cannot carry a
false orders-of-magnitude claim, and the worked example is where future authors
will copy the phrasing from. **Fix:** per the document's own change protocol
(Reading guide: "amended by dated addendum, not silent edit"), append a dated
addendum to §A.5: "[CORRECTION 2026-09-23: 1e-6 is ≈8× float32 unit roundoff, not
10³× — the signed plan's phrasing is arithmetically wrong; the tolerance choice
itself (1e-6, passed with 240/240) is unaffected.]"

**F-200-2 (required) — §A.5 L1/A3 must name the run-specific model pin.**
The example's L1 states the identity with "E is the frozen unembedding weight
matrix" and A3 notes EXP070's vector cell is Underdetermined — but it never
states what the executed audit report disclosed (report §1 "Load-bearing
provenance fact" and §7 note 1): **EXP065 and EXP070 executed on
`EleutherAI/pythia-160m`; EXP066 and EXP077 on `pythia-410m`**; E1's first link
is 410m-matrix self-consistency for EXP065/070, not byte-copies of the executed
160m numerics. The two-link chain (E1+E2) is honest as written, but a license
example should surface the model pin in L1's statement ("E = the run's pinned
model's unembedding matrix — 160m for EXP065/070, 410m for EXP066/077, per the
E2 model-pin table") so no future author reads E1 as having measured the
executed 160m vectors. **Fix:** dated addendum to §A.5 L1 + A3.

**N-200-1 (note, not blocking).** §A.1 uses `[INFERENCE]` as a standalone label;
the labeling preamble defines the AGENTS.md §5 label set plus the mentor layer.
`[INFERENCE]` is the mentor-layer term (the playbook maps it to
[INTERPRETATION]). Acceptable under the preamble's stated convention, but the
standard should use it consistently (either always paired or mapped) so reviewers
applying Charter M1–M8 don't have to guess which layer a bare `[INFERENCE]` sits
on.

---

## Artifact 2 — `research/innovation/ARCHITECTURE_ANALYSIS_2026-09-23.md` (LOG-201)

**Verdict: SIGN-WITH-FIXES** (1 required fix — the known defect, confirmed and
sharper than briefed; 1 note). The "partially principled, weighted toward
convenience" verdict is genuinely argued from architecture (§1.1–1.5), claims are
honestly graded ([STRUCTURAL]/[ANALOGY], no theorems claimed — stated explicitly
in the grading key and §1.6), hunting-ground triggers are genuine observation-gates
(§3 table), and the pass-count math checks out (360/22 = 16.4s ≈ "16 s";
240-pass and 180-pass probes bounded as "minutes"; the 2×T4 throughput basis is
sourced to the paradigm audit). All 9 UNVERIFIED tags are honest and non-load-bearing
(logit-lens citations; Pythia-1B width/layers; SAE availability; RoPE/gate specs).

### Required fix

**F-201-1 (required) — the 160m omission is confirmed, and it is worse than the
brief suggests.** `grep -c -i "160m"` on the document returns **0**. The analysis
rests on a uniform "Pythia-410m / layer 20" substrate narrative that is false for
half the cited experimental record. Verified against primary sources:

| Experiment | Actual model (runner-pinned) | Actual injection layer | Downstream blocks | LOG-201's narrative assumes |
|---|---|---|---|---|
| EXP065 | `EleutherAI/pythia-160m` (`run_exp065_temporary_coordinate_alignment.py` l. 77) | **Layer 10** — concept extraction (l. 95) *and* bridge arm (ll. 483–491 "Same-Layer Output Bridge (v_output at Layer 10)") | 1 (of 12) | 410m / L20 / 3 blocks |
| EXP070 | `EleutherAI/pythia-160m` (`experiments/runs/exp070/run_exp070.py` l. 83) | **Layer 10** ("l* = 10 (83% depth, matching EXP065)", l. 86) | 1 (of 12) | 410m / L20 / 3 blocks |
| EXP066 | pythia-410m | Layer 20 | 3 (of 24) | ✓ correct |
| EXP077 | pythia-410m | Layer 20 | 3 (of 24) | ✓ correct |

Consequences for the analysis's structural claims:
- §1.2's "exactly two channels... 3 downstream blocks" and §1.5's "at 3 blocks
  from a linear readout, 'output-side' and 'works' nearly coincide by
  construction" are 410m-specific. EXP065's bridge rescue (ΔM=+16.67pp,
  p=0.001953125 — one of the four rescues the analysis explains) happened at
  **L10 of a 12-layer model — one block from the readout**, where the bypass
  channel is even more dominant and the "48-head routing" discussion does not
  apply (160m has 12 heads/layer, not 16).
- §1.2's "At L10, by contrast, 14 downstream blocks (224 heads) — room for
  processing" is about **410m**/L10. The program's actual L10 injections were on
  the **160m** (1 downstream block). A reader can easily conflate the two; the
  analysis must not let them.
- §1.6's convenience column ("Pythia-410m chosen for throughput... never for
  architectural suitability") misses the actual history, which ironically
  *supports* its verdict: EXP066's runner pins the choice explicitly —
  `target_layer = 20  # Equivalent proportional depth (83.33%) to Layer 10 on
  160M` — i.e., L20 was inherited via fractional-depth mapping from the original
  160m/L10 experiment, never localized. The analysis's "inherited without any
  localization study" claim is right, but it never shows the reader the
  inheritance.

**Fix:** add a substrate-attribution table (the one above, with file:line pins)
to §0; re-scope §1.2/§1.5's channel arithmetic to the correct (model, layer)
pairs per experiment; amend §1.6's verdict table so the "convenience" column
records the 160m-origin and the 83.33%-fractional-depth port (with the EXP066
runner citation); and qualify Ground 1's "L8/L12/L16 at 410m" proposal as
genuinely untested (the program's mid-layer injections were all on the 12-layer
model). The §1.6 verdict itself ("partially principled, weighted toward
convenience") may stand — the fix strengthens it.

### Note

**N-201-1.** §4 Q4 ("architectural argument, analogy vs theorem graded") is a
weaker license than the LOG-200 rubric's INTUITION-disqualifying bar — [ANALOGY]
is doing real work here (the mid-network concept-formation depth profile, the
superposition/width argument, the SwiGLU-gate story). The document is honest
about this (no theorem claimed; analogy graded as analogy), so this passes —
but once LOG-200 is ratified, this analysis's [ANALOGY]-graded passages license
at most CONJECTURE-UNDER-TEST, never a full-budget run. Record that implication;
do not silently promote the analysis later.

---

## Artifact 3 — `research/innovation/COMPUTE_PLAYBOOK_2026-09-23.md` + `research/innovation/QUOTA_LEDGER.md` (LOG-202)

**Verdict: SIGN-WITH-FIXES** (1 required fix on the ledger, 2 minor fixes and 1
nit on the playbook). The UNVERIFIED tagging is honest and complete, the
bookkeeping rules name their enforcers, the costings are sane, the user-action
request is clean, and the DIRECTION_DECISION order discrepancy is explicitly
flagged as the CEO's decision — not silently resolved.

### What holds up

**R1. UNVERIFIED tags honest and complete.** `grep -o UNVERIFIED | wc -l` = 21;
one is the epistemology-definition line (§0: "single-source or contradictory
items are tagged UNVERIFIED per Law #3"), leaving **20 tags** — the document's
stated count is exactly right under that method (see F-202-2 for the required
clarification). Spot-checked for completeness: the genuinely uncertain items are
all tagged — Kaggle reset-day conflict (§1a), session-cap conflict, idle-timeout
conflict, P100-vs-Python-3.12 caution, Colab quota (third-party only), Lightning
22-vs-75 conversion conflict, ZeroGPU undocumented run-limit, Paperspace/GCP/AWS
third-party claims. No load-bearing number rides on an untagged claim; conflicts
are recorded as conflicts, not resolved by assertion. ✓

**R2. Bookkeeping rules are enforceable.** §3 names the enforcer for each rule:
Lead books (rule 3), CEO clears/voids (rules 2–3), executors run only booked
entries (rule 3), reconciliation every Sunday against named sources (rule 5),
headroom formula `ceil(2.5 × estimate)` (rule 4), reserve-vs-available accounting
(rule 6). Procedural, not automated — acceptable for an operational playbook;
the ledger's status state machine (`booked → running → spent`, `void`/`refunded`)
gives the audit trail. ✓

**R3. Costings sane.** Throughput basis stated (22 fwd/s, 410m, 2×T4). EXP080:
1,320/22 = 60s = 0.0167h → 0.05 booked ✓. EXP081: 660/22 = 30s → 0.03 ✓. K3:
~400 → 0.05 ✓. CLLC pilot 1–2h est → 2.00 ✓. Ledger total 0.05+0.03+0.10+0.05+
2.00 = 2.23 ≈ "2.25" ✓; reserve 27.75 + 2.25 = 30 ✓. ✓

**R4. Single user-action request is clear and touches no credentials.** §5 lists
exactly three actions (Colab smoke test; Lightning free-tier signup reporting
only the visible balance; HF account age/email verification), each with an
explicit "report back" (not "hand over"), and a standing prohibition: "do not
share passwords, tokens, or codes; add any card; upgrade." Agents are forbidden
from signing in. ✓

**R5. GPU-order discrepancy flagged as a CEO decision, not silently resolved.**
§4's ordering note states verbatim: "this sequence follows the CEO's LOG-202
instruction. LOG-198's DIRECTION_DECISION listed K3 before EXP080" — naming the
departed-from document. The conditionality argument is defensible: K1 gates K3
and the Sprint-3 pilots' interpretation, while EXP080/081 are gated on the
LOG-197 verdict + CEO clearance, and EXP080's bin (ii) result is interpretable
under either K1 verdict (LOG-201's own §3 decision tree uses it on both
branches). The playbook does not pretend the discrepancy doesn't exist. ✓

### Required fixes

**F-202-1 (required) — the ledger carries no Law #15 answers.** The playbook has
them (§6); `QUOTA_LEDGER.md` — a separately reviewed artifact — has none: no
Q1 (what question the ledger answers), Q2, Q3, or Q4. The brief's cross-cutting
rule is "every artifact must carry Law #15's four answers." **Fix:** add a
Law #15 block to the ledger header (it may reference the playbook's §6 as the
landscape record, with ledger-specific answers: Q1 = booking-integrity record;
Q2 = no unbooked/unlicensed GPU run; Q3 = a markdown table, $0; Q4 = n/a,
operational instrument, stated honestly).

**F-202-2 (minor, required) — "20 UNVERIFIED tags" needs its counting method.**
Raw `grep -o` gives 21; 20 holds only excluding the §0 epistemology-definition
line. A verifier who greps will conclude the count is wrong. **Fix:** one line
in §0 or §7: "20 tags counted; the §0 definitional line excluded."

**F-202-3 (minor, required) — Sprint-3 booking breaks the headroom rule.**
Rule 4: "booked T4-h = ceil(2.5 × estimate)". Sprint-3: ~0.05 est → 2.5× = 0.125
→ booked **0.10**, below the rule every other line satisfies. **Fix:** book 0.13
or state in the ledger entry that the 0.05 estimate already includes contingency
(and then the rule's "estimate" means pre-contingency — say so).

**N-202-1 (nit).** "EXP068 as-signed (~93k passes, ~13h worst case)": at the
stated 22 fwd/s, 93,000 passes ≈ 1.2h, not 13h. The 13h figure presumably folds
in session overhead / re-run budget / the adaptive loop's non-forward-pass cost —
one line of rationale, or a corrected figure.

---

## Artifact 4 — `research/LAW15_RETROACTIVE_AUDIT_2026-09-23.md` (LOG-199)

**Verdict: SIGN-WITH-FIXES** (1 scope fix, 1 precision fix). The four answers for
the four audited items are genuinely on record and do not contradict the signed
protocols; the EXP068 FAIL verdict follows from Q3/Q4; the as-signed design is
retired, not parked.

### What holds up

**R1. Four answers are on record, not post-hoc.** Spot-checked against signed
artifacts:
- EXP080 Q1 ("selection prize in bin (ii), non-bridge candidates") — the signed
  spec defines bin (ii) as "non-bridge marginal rescues"
  (`G2_ORACLE_CEILING_PREREG_SPEC.md` ll. 289, 486–488, 567–568). Q2's
  CONTINUE/KILL mapping and the "bridge ceiling, not pool ceiling" collapse are
  the spec's own (d)/(e) rows. ✓
- LOG-197's four answers match the frozen plan (plan §§2–3, §5 compliance
  criterion, §8–§9). ✓
- EXP081's Q4 ("conjecture under test, breaking point = the C5
  entity-similarity arm explaining the transfer") matches the signed v2 spec's
  F1 fix (agreement < ⌈5n_d/6⌉ kills the transfer claim). ✓
- EXP068 Q3/Q4: "~93,000 passes worst case" vs the $0 K1 and the already-queued
  EXP080 oracle ceiling as strictly cheaper sufficient answers; Q4's "E-validity
  a standing [CONJECTURE], no computable breaking point" matches LOOP_SPEC's
  "implementability MEDIUM, E-validity unproven." The FAIL verdict follows
  deductively from Q3 (not cheapest) and Q4 (license too weak to name a breaking
  point). The shelving is grounded, not merely repeated. ✓

**R2. No zombie workstream.** The disposition is explicit: "the as-signed design
is retired, not parked. Any future adaptive-loop attempt is a new experiment
number with a new Law #15 record." The question survives (re-asked through
CLLC/DPRS), the design dies. Law #8 satisfied. ✓

### Required fixes

**F-199-1 (required) — scope gap: the mandate is discharged for 4 items, but
the pipeline has more.** The mandate states: "every pipeline item must have its
four answers on record. Where an answer is missing, write it or stop the work."
A repo-wide grep for Law #15 four-answer records finds them only in this audit
and in LOG-200 (the standard itself). **K1, K2, K3, the CLLC 160m pilot, and the
Sprint-3 Stage-0 pilots have no Law #15 record anywhere** — yet the playbook
books GPU for them (BK-03/04/05) and the compliance summary ("3 of 4 pass... No
zombie workstreams remain") reads as pipeline-complete. **Fix:** either (a)
record the four answers for K1/K2/K3, the CLLC pilot, and the Sprint-3 pilots in
a dated follow-up section of this audit (with owners and gate dates), or (b)
explicitly scope-limit the audit ("covers signed/queued experiment protocols as
of 2026-09-23; battery and pilot items receive their Law #15 records at
pre-registration, before any booking") and log the follow-up as a dated entry in
`reports/research_log.md`. Until then, the "no zombie" claim is true for the
audited four but overclaims for the pipeline.

**F-199-2 (required) — EXP081 Q1 misnames the decision endpoint.**
The audit's Q1 reads: "transfer to held-out items (**ΔM > 0 at L1,
pre-registered margin**)..." But the signed v2 spec (Law #9) states: "No
margins, no Wilcoxon, no KL, no cosine-deltas **as decision endpoints —
anywhere**" (spec l. 598); the decision endpoint is the F1 agreement rule
(agreement < ⌈5n_d/6⌉ kills the transfer claim). A Law #15 audit whose Q1
contradicts the signed protocol's endpoint register is exactly the defect this
review class exists to catch. **Fix:** reword the parenthetical to the actual
pinned endpoint (e.g., "donor transfer at the pre-registered F1 agreement bar,
with the C5 entity-similarity leak controlled").

---

## Cross-cutting checks

| Check | Finding |
|---|---|
| Law #15's four answers on every artifact | LOG-200 ✓ · LOG-201 ✓ (§4) · playbook ✓ (§6, Q4 honestly "n/a — operational document") · **ledger ✗ (F-202-1)** · LOG-199 ✓ (per-item) |
| Fabricated citations (Law #3) | None found. Both arXiv IDs and both TACL citations verified by live fetch 2026-09-23; summaries faithful. LOG-201's external claims tagged UNVERIFIED, never load-bearing. |
| Signed files edited | None. All four are new files; LOG-200 §A.6 explicitly routes changes through dated addenda. |
| FACT/INFERENCE/HYPOTHESIS/SPECULATION layer | Respected in all four; 10-label standard applied (N-200-1 consistency note). |
| Numbers verifiable | All checked numbers reconcile (see R2/R3 per artifact) except F-200-1 (orders-of-magnitude arithmetic) and N-202-1 (93k-passes/13h tension). |
| GPU/credentials | $0, docs only, no GPU, no credentials touched. Confirmed in each artifact's cost/epistemology header. |

---

*Review ends. Fixes F-200-1, F-200-2, F-201-1, F-202-1, F-202-2, F-202-3, F-199-1,
F-199-2 are required before the SIGN in each verdict converts to a clean SIGN.
N-items are notes for the authors' next revision. No artifact is rejected; no
finding requires re-running anything.*
