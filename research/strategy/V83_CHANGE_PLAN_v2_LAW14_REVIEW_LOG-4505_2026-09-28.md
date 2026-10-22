# V83 Change Plan v2 — Independent Law #14 Review (LOG-4505)

**Date:** 2026-09-28 · **Lane:** INDEPENDENT LAW #14 REVIEW (pre-assigned LOG-4505; review only — no modification of v82, the v1/v2 plans, or any signed protocol; no experiment number minted; no clearance granted; no build work) · **$0 compute**

**Target:** `research/strategy/V83_CHANGE_PLAN_v2_2026-09-28.md`
**Target sha256:** `3c3df27c705f5c80d876c1d2285487da935eea49a054b13b11cbf3fbb6ff88cd` (verified this lane; v1 plan sha256 `b66a741709aa9f72ca5fb87358b33a09463ecdb0c62baafff881f5ed9acd00dc` untouched)

**Context [FACT]:** LOG-4471 recorded the independent Law #14 review of the v1 plan (three flags O1/O2/O3 + tension T1). LOG-4494 was a CEO self-audit producing v2 — a self-audit is not an independent review under Law #14. This lane is the required independent review of v2.

**Epistemology:** Law #11 labels throughout — [FACT] (verifiable from a LOG entry, bundle artifact, or v82's text), [OBSERVATION] (reviewer's reading), [INTERPRETATION] (judgment).

---

## 1. Disposition of LOG-4471's flags in v2

| Flag (LOG-4471) | Addressed in v2? | Evidence |
|---|---|---|
| **O1** — Item-33 vignette attributed unverified item-level margin numbers +0.010/−0.004 | **YES — resolved** | Change #6R: per-item recompute declared INFEASIBLE per LOG-4472 (aggregate means only; 180-pass GPU recovery barred). The figures +0.010/−0.004 are **hard-banned** in four places (Part 1 Change #6 row; Change #6R prohibition; provenance table; Part 4 decision (b)). Founder picks mean-labeled arrow or no arrow. Grep of v2: every occurrence of +0.010/−0.004 is a prohibition, never an attributed claim. |
| **O2** — Gap 1 "missing dose-response" partially stale (EXP095 ran the 5-point α dose-response; what remains unmeasured is the hero shared-direction curve) | **YES — resolved** | Change #3 ADOPT as-is with the EXP095 scope fence (LOG-4400) and S6 stand-down (LOG-4464) retained; provenance table carries the EXP095 5-point α dose-response row (LOG-4399/4400); v2 adds the explicit instruction that v83 must NOT present EXP105 as filling Change #3's gap. Matches v1 Change #3's three-part statement verbatim in substance. |
| **O3** — `figs/_superseded/` confirmed uncompiled (0 references) | **YES — informational** | Nothing to fix; v2 Change #10 ADOPT as-is; Fig. 6 caption rewrite must cover the new I2′ branch (covered by Change #2 addendum). |
| **T1** — Fix 10's cut of the five-stage vision vs. founder's standing full-vision preference | **YES — held as founder decision** | Change #12 ADOPT as-is; Part 4(c) offers (i) boxed compression or (ii) full retention. Matches v1's "compression, not deletion — founder call" compromise. |

---

## 2. v82 line-level grounding (verified this lane against `~/workspace/scbi-paper/v82/paper.tex`, read-only)

| v2 claim | v82 check | Result |
|---|---|---|
| Discussion L391 → Item-33 material | L391: "Item~33 decodes correctly with the second-largest 1-NN margin of all 60 items ($1.013$; same-class $2.106$ vs.\ different-class $3.119$), yet the mean injection margin shift is only $+0.0059$ / $-0.0076$ across items" | ✅ matches v2's 1.0133 / 2.1059 / 3.1192 / +0.0059/−0.0076 to ≤3e-4; "across items" wording confirmed in v82 itself |
| Item-33 injection means +0.0059518/−0.0076361 | LOG-4472 (`ITEM33_MARGIN_RECOMPUTE_2026-09-28.md`, L23: item 33 = `exp092_elemental_2hop_3`, margin 1.0133) | ✅ |
| §sec:kills (L367), §sec:phasediagram (L376), limitations L394, app:master L530 | `\label{sec:kills}` L367; `\label{sec:phasediagram}` L376; `\section{Limitations}` L394; `\label{app:master}` L530 | ✅ all exact |
| 1/(d−r) dilution law, 1/1022, Proposition 1 + L270 | L270: "keeps roughly one-thousandth ($1/1022$) of its squared alignment"; Proposition 1 at L262–270 | ✅ |
| "Decodes at 6.7× chance" (33.33/5 = 6.667), EXP092 p=0.000999 | L157: "$20/60 = 33.33\\% ($p = 0.000999$…)" | ✅ |
| "Steers zero decisions" (EXP093 McNemar b=c=0, p=1.0, ΔM=0) | L157: "(McNemar $b=c=0$, $p = 1.0$…), $\\Delta M = 0$, zero flips" | ✅ |
| "Checkable claims" box (Change #8) | L173: "Our contributions are five checkable claims…" (C1–C5) | ✅ grounded |
| Fig. 1 boxed callout (Change #6R) | `\label{fig:hero}` L158, "The Decodability Gap in one figure" | ✅ |
| Fig. 6 / phase diagram (Change #10/#13) | `\label{fig:phasediagram}` L342 | ✅ |
| S4-8 pre-reg SIGNED (LOG-4480), S4-8′ SIGNED (LOG-4488) | LOG-4480: "The S4-8 pre-registration is SIGNED"; LOG-4488: "The S4-8′ cloze-format pre-registration (v2) is SIGNED" | ✅ |

**EXP104/105 numbers spot-checked against the log:** 11/60 = 0.1833 (LOG-4481/4482) ✅; position-A prior 30/60, p=2.02e-12 (LOG-4483) ✅; EXP105 Tier-0 32/60 = 0.5333, n_pop 21, tie guard 0.0 (LOG-4489) ✅; EXP105 battery ΔM_T=+0.2381, ΔM_R=0.0, b=5/c=0, p=0.0625, O=0.571, step-9 KILL (LOG-4491/4492) ✅; N1 O ≤ 0.5 gate pre-registered (LOG-4479 amendment, D2 stratum in LOG-4476 review) and validated at O=0.571 (LOG-4491) ✅; EXP085 death-debt framing ("selection failures measurable/repairable", LOG-623 clearance / LOG-696 chain) ✅.

---

## 3. Item-33 verdict

**[FACT]** v2 never uses +0.010/−0.004 as evidence. All four mentions are prohibitions. The only margin-shift numbers v2 licenses for the vignette are the LOG-4472 aggregate means (+0.0059518/−0.0076361), required to be **explicitly labeled as means across all 60 items**, or no margin arrow at all. This exactly implements LOG-4471 O1's directive.

---

## 4. Binding-verdict consistency (no contradictions found)

- **I2′ closed:** v2's Change #13 keeps the line CLOSED per pre-registered stop rules, presented as falsification-terminal; the honest headline (zero positive autonomous-steering signals, scoreboard v1.4 / LOG-4492) travels with it. Consistent.
- **S6 stand-down:** Change #3 cites LOG-4464; Part 4(a) approval explicitly does NOT authorize violating the S6 stand-down. Consistent.
- **Scoreboard v1.4:** cited as the honest-headline source. Consistent.
- **Procrustes retraction:** untouched. The named 1/(d−r) dilution law (Change #4) is the corrected theorem reading from v82 L270, not a revived transfer claim. Consistent.
- **Novelty N1:** v2 makes no novelty claim; v82 C5 (L180) unchanged. Consistent.
- **Change #1's firewall:** v2 correctly separates the hero claim (EXP092/93 static injection) from the I2′ line (masking on two-hop recall) and refuses to let EXP105's Refuted verdict weaken "steers zero decisions". [INTERPRETATION] Correct — different interventions, different benches, different questions.

---

## 5. Defects

### D1 (MINOR, fixable — the only defect): stale LOG-4491 truncation caveat

**[FACT]** v2's Provenance-caveat asserts: "the research log's own LOG-4491 entry is truncated mid-sentence (verified in-file: ends at 'applied the pre-registered arms B/T/F/R', verdict text missing)" and requests "CEO append-only log repair — not performed by this lane."

**[FACT]** In-file verification this lane: LOG-4491 (`reports/research_log.md`, L63) is **complete** — Verdict, Numbers, Decision-table walk, and Deliverables sections all present. The append-only repair already landed at **LOG-4495** (L44). The caveat was accurate at LOG-4494 time but is now stale; the requested repair is already done.

**Fix:** replace the caveat with "LOG-4491 was truncated mid-sentence; append-only repair completed at LOG-4495; the entry is now complete." One-line correction; no other content changes. Nothing in the plan's recommendations depends on the stale caveat.

### No other defects found

- **Provenance gaps:** 0 (all 20 planned claims trace to a LOG entry, bundle artifact, or v82's text; the one caveat is D1, not a gap).
- **Contradictions with v1:** none. **Fabricated numbers:** none. **Scope violations:** none — the approval brief (Part 4a) fences out new experiments, verdict changes, guardrail softening, arXiv submission, and S6-stand-down violation.

---

## 6. Binding verdict

**SIGN-WITH-FIXES** — the v2 plan is structurally sound and may proceed to the founder decision brief once D1's one-line correction is applied. The LOG-4471 flags are all verifiably disposed; every line-level v82 attribution checks out; the Item-33 ban is airtight; no binding verdict is contradicted.

**Reviewer independence note:** this lane did not participate in LOG-4494 (the v2 authoring audit); it read v2 as a fixed target (sha256 above) and performed independent in-file verification of every checked claim.

*Review complete 2026-09-28. No experiment number minted; no clearance granted; no v83 build authorized — build still requires the founder's Part 4 decisions.*
