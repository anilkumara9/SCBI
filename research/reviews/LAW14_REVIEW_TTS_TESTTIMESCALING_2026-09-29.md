# Independent Law #14 Review — EXP130 (TTS) Pre-registration Draft

**Lane:** LOG-4721 (pre-assigned). **$0 CPU.** Read-only on signed
protocols, paper sources, and the GPU queue. Nothing pushed, spent,
or credential-touched.

**Protocol under review:**
`research/prereg/EXP_PREREG_TTS_TESTTIMESCALING_2026-09-29.md`
**sha256 `4640d44d1252a04f50146b4495fa32559c57cb9b3421ee8c01092c27076396eb`
— verified before review; no lane defect.**

**Gate:** LOG-4719 (PASS, conditional). **Cross-references read:**
`research/strategy/TTS_GATE_2026-09-29.md`,
`research/experiments/EXP113_EVALID_REPORT_2026-09-29.md`,
`research/experiments/EXP109_PTTSC_REPORT_2026-09-29.md`,
`research/experiments/EXP115_HDIGEN_REPORT_2026-09-29.md`,
and the research-log records for LOG-4579→4585 (EXP113),
LOG-4598/4599 (EXP115), LOG-4602/4603/4673 (EXP116), and the
H20-lane terminal binding on the entity-name generation channel.

---

## Verdict: REJECT

The dossier's pre-launch tripwire fires. The generation-channel
construct-validity gate (§1.2, §3.3) is insufficient on the program
record, and no fix within this draft's architecture can supply what
is missing. **The family never launches on this elicitation
design** — the pre-reg's own §2 tripwire branch
("Law #14 rules the generation-channel construct invalid →
Never launches — pre-launch kill, recorded").

## The defect (adversarial findings, in order of force)

**D1 — The "EVALID-cleared" claim does not transfer, and the
transfer was already tested and failed.** The pre-reg pins T1-P2
few-shot (§3.3, "The EVALID-cleared protocol (EXP113/H7,
T1-CLEAR, 60/60)") for entity-name answers on the EXP107 bench.
EXP113's clearance was on the EXP089 bench with single-letter
answers. The letter→entity transfer is not merely unvalidated —
it was tested and failed:

- **EXP115** (LOG-4598/4599, BIND): the identical elicitation
  macro-structure (3 pinned exemplar blocks, items 0–2, answers =
  their E1, target block ending after the answer slot) on
  entity-name answers on the SAME bench (identical bench pin
  `e91b302f…4f5`) → **RUN-INVALID**, G1 fired at 38/60
  unparseable. Failure mode [OBSERVATION]: few-shot recitation —
  the model regurgitates the exemplar macro-structure
  ("All 60 generations contain `Premise:`").
- **EXP116** (LOG-4602/4603, BIND at LOG-4673): P5 on the
  entity-name shape → RUN-INVALID (tail echo); registered
  consequence: "no further EXP113-cleared protocol to license
  (**P2 dead on this shape**; P5 failed)."
- **H20 lane** (bound, no caveat): "entity-name generation
  channel dead on all EXP113-cleared protocols (P2 dead on this
  shape, P5 dead on tail echo, P4 dies here)" — **RUN-INVALID,
  TERMINAL**; "honesty-instrument line closes permanently on
  this shape."

**D2 — The pre-reg's §1.2 disclosure is materially incomplete.**
§1.2(i) frames the P2 transfer as unvalidated-but-testable
("validated in-protocol by the elicitation-failure gate, not
assumed"). It omits EXP115's direct negative on the identical
structure + bench + answer shape, and omits the terminal
"dead on all EXP113-cleared protocols" binding. A construct-
validity argument that withholds the program's own bound
negative on the exact transfer is not an honest disclosure
(Law #2, Law #11).

**D3 — The Q:/A: wrapper is not a construct-validity argument.**
EXP130's §3.3 differs from EXP115's failed P2 cosmetically
(`Q:`/`A:` line wrappers around the same 3-exemplar +
target macro-structure). EXP115's diagnosed pathology was
macro-structural (document-continuation cue from repeated
exemplar blocks), not slot-label-deep. An unvalidated prompt
variant of a bound-failed apparatus is a re-test, not a new
apparatus — and the pre-reg itself titles §3.3 "T1-P2
few-shot (pinned verbatim)," placing it inside the
terminally-closed set.

**D4 — The in-protocol elicitation gate cannot rescue construct
validity.** The gate (§0(b), §5 tree) routes elicitation failure
to RUN-INVALID; it cannot manufacture a false CONTINUE. That
makes the protocol *safe* but not *worth licensing*: the
expected outcome is a near-certain RUN-INVALID re-demonstrating
EXP115's apparatus finding at ~2–4h CPU. The apparatus question
("can P2 elicit entity names on this bench") was answered;
the cheapest test has been run. Licensing this run is busywork
under the worth-it discipline, and it contradicts the H20
terminal binding ("closes permanently on this shape").

**D5 — The gate's launch condition (1) is unsatisfiable on the
record.** LOG-4719 §4 claims P2/P5 "clear ≥48/60 on both
elicitation task shapes (60/60 on T1)." The clearance is on
letter answers; for entity-name answers the record holds P2
dead (EXP115), P5 dead (EXP116), P4 dead (H20). The condition
"an EVALID-cleared elicitation protocol (P2 or P5) named" is
met in letter only, not in the answer shape this protocol
uses.

## What was checked and found sound (recorded for any re-proposal)

- **McNemar critical table (§4):** all six values independently
  recomputed from exact binomial tails — (5,0)→0.0312,
  (6,0)→0.0156, (7,1)→0.0352, (6,1)→0.0625 ✗,
  (8,2)→0.0547 ✗, (4,0)→0.0625 — all exact. The one-sided
  license and the gate-deviation correction (§9.1) are correct.
- **Budget-confound control:** "margin-select ≈ random-select"
  is operationalized, not a judgment call — CONTINUE requires
  McNemar(margin, random) one-sided p ≤ 0.05 (§2, §4); failure
  falls to HELD mechanically. Adequate.
- **EXP126 correlate fence (§3.7):** mechanical, downgrade-only,
  protocol-level. Adequate.
- **KILL bar below the significance floor (§4):** deliberate
  and honest — net ≤4 items can never reach p ≤ 0.05
  one-sided. Verified.
- **Honest frame (§6–§8):** search-and-selection tag, no
  steering/reasoning/generality claims, scoreboard zero
  untouched. Verbatim and sound.
- **H4/PTTSC differentiation, EXP056 fence:** the power
  analysis (§4) beats EXP056 by registration and power, not
  repetition. Sound.

## Observations for a re-proposal (not fixes — the draft cannot be repaired)

- **O1 (launch-gating, would have been FIX-1):** §0(b) defines
  item validity with the ≥1/16-sample condition while §3.5/§5
  stage Stage 1 before the samples are burned — the staged
  cheap-falsifier design is unexecutable as ordered
  (LOG-4704 defect class). Any re-proposal must split the
  elicitation audit (greedy-parseability gate pre-Stage-1;
  sample-parseability as the Stage-2 inclusion rule), move the
  120 option-embedding forwards + BPE records into the
  pre-Stage-1 block (Stage 1 needs them for its 120 cosines),
  and define the Stage-1 vs Stage-2 item sets separately.
- **O2:** pin the Stage-1 zero-variance branch (r_pb undefined
  when greedy correctness has zero variance).
- **O3:** "EXP109's elicitation-failure gate, carried verbatim"
  (§0(b), §2, §3.4) is misattributed — EXP109's pilot used
  ≥3 of 20 items; the ≥6/60 rule is the registered H1/H4/
  EXP108-class 10% rule. Do not claim verbatim carriage.
- **O4:** §1.2(ii)'s "constant-but-parseable output stream is a
  valid measurement (scored as accuracy)" contradicts G4 —
  a constant stream fires the instrument-deaf RUN-INVALID.
  Align the disclosure with the guard.
- **O5:** clarify the G4 cosine set (Stage-1 greedy-arm
  cosines, 60×2) once O1 is implemented.

## Re-proposal condition

This REJECT kills the family **on the P2/P4/P5 elicitation
designs for entity-name answers**, per the H20 terminal
binding. A re-proposal is licensed only with a genuinely new
elicitation apparatus carrying positive construct-validity
evidence for entity-name answers on this backbone — e.g., a
new EVALID-style elicitation-validation lane, or a small
elicitation pilot pre-registration demonstrating that a
specific prompt design defeats the EXP115 recitation
pathology. Disclosure alone does not suffice; neither does a
prompt-variant re-test of the failed apparatus. TGA
(EXP127, CONTINUE), DSF (EXP128, UNTESTED), and CLP
(EXP129, KILL) are untouched by this ruling.

---

*Review finalized 2026-09-29. Lane closed; no follow-up
dispatched (per lane brief). Nothing pushed, spent, or
credential-touched.*
