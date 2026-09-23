# Law #14 Adversarial Review — EXP078 Pre-registration Draft (Re-registration of EXP075)

**Date:** 2026-09-23
**Reviewer role:** Adversarial Reviewer (Law #14)
**Document under review:** `experiments/protocols/EXP078_SUBSPACE_BRIDGE_REREG_PREREG_SPEC.md` (DRAFT, 378 lines)
**Reference baseline:** `experiments/protocols/EXP075_SUBSPACE_BRIDGE_PREREG_SPEC.md` (SIGNED, 296 lines)
**Context:** LOG-111 (F2 guard abort on real pythia-410m tokenizer; 11/35 entities multi-token), LOG-112 (draft entry)
**Verdict: SIGN** — with one MINOR (M7.1, carried over from EXP075; fix within one review cycle)

---

## 1. Method

Full read of the draft, not on trust. Produced a complete `diff -u` of EXP075-signed vs
EXP078-draft (257 diff lines, 164 changed lines) and accounted for every hunk. Independently
re-ran the tokenizer verification the spec claims (real `EleutherAI/pythia-410m` tokenizer,
cached from the smoke-test download, `HF_HUB_OFFLINE=1`): all 11 substitutes, all 11 replaced
entities, all 10 benchmark entities, and collision checks. Read §7 decision tree in full and
checked M5.2 exhaustiveness. Checked new prose against `research/MATH_STANDARDS_CHARTER.md`
(M1–M8). Checked §0's historical claims against LOG-111 and the historical EXP066 script.

## 2. Complete diff inventory (every difference, classified)

| # | Location | Change | Classification |
|---|---|---|---|
| 1 | Title/header | EXP075→EXP078; status DRAFT pending Law #14; author role → "re-registration of EXP075"; predecessors add EXP075 (SIGNED, bundle cleared LOG-107, aborted — see §0); governing standards add `research/MATH_STANDARDS_CHARTER.md` (M1–M8) | Legitimate: re-registration bookkeeping |
| 2 | §0 (new, 32 lines) | Re-registration note: EXP075 signed→bundle cleared→F2 abort on 'Caleb' [330, 43705]; 11 multi-token entities listed by vocab; benchmark unaffected; historical EXP066 `encode(" "+e)[0]` silent truncation; Law #4 basis for new number; "ONLY design delta is §3.1 table"; budget disclosure correction noted | Legitimate: required honesty record |
| 3 | §1.1 | "EXP075 is a boundary-characterization…" → "EXP078 is…" | Legitimate rename |
| 4 | §2 | Model line: "(identical to EXP066/EXP067)" → "(identical to EXP066/EXP067/EXP075)" | Legitimate |
| 5 | §3.1 | "constructed exactly per the EXP066 support procedure … from the 5×30 support contrast pairs" → adds "with the entity substitution table below applied" | Legitimate: the delta |
| 6 | §3.1 | New: 11-row substitution table (vocab, EXP075 entity, EXP078 substitute, tokenizer check) | Legitimate: the delta |
| 7 | §3.1 | New: paragraph — substitutes verified single-token with leading-space convention, collision-free, thematic grouping preserved; unchanged entities enumerated (V1 full; V2 Aaron/Gideon; V3 Jason/Paris; V4 Marcus/Felix; V5 Liam/Noah/Maya) | Legitimate: makes full entity lists reconstructible (11+14=25 ✓) |
| 8 | §3.1 | New: "Provenance honesty [INTERPRETATION]" — support set intentionally NOT item-identical to historical EXP066 script (identity would require the forbidden silent truncation); item-identical *in procedure* | Legitimate: required honesty record |
| 9 | §3.1 | No-peeking paragraph: explicit 25-entity enumeration removed, replaced with "support entities are person names" + table/unchanged-list in §§6–7 above | Legitimate: enumeration moved, no information lost (verified: union of table + unchanged list = original 25 minus 11 replaced plus 11 substitutes) |
| 10 | §3.1 | New: "Single-token guard (F2, pre-registered, abort on violation)" paragraph — exact `" "+e` check, FATAL abort naming entity, verified 2026-09-23 against real tokenizer, remains armed as defense-in-depth | Legitimate: pre-registers the guard that fired; defense-in-depth is correct |
| 11 | §4 | C4 row: "Subspace-restricted bridge (EXP075 test)" → "(EXP078 test)" | Legitimate rename |
| 12 | §5 | Benchmark: adds "(same items, same premise permutations — byte-identical; the benchmark entities are all single-token and untouched by the §3.1 substitution)" | Legitimate: preempts Law #9 concern |
| 13 | §5 | "not a trigger for adjustment under EXP075" → "under EXP078" | Legitimate rename |
| 14 | §7.1(a) | "not a re-run under EXP075" → "under EXP078" | Legitimate rename |
| 15 | §7.2 | "EXP075 has three halt gates" → "EXP078…"; "a halted EXP075" → "halted EXP078"; "under the EXP075 label" → "EXP078 label"; adds "(EXP075→EXP078 precedent; EXP070 minor-m1 precedent)" | Legitimate: precedent correctly extended |
| 16 | §8 | Seeds: adds "All seeds identical to EXP075 — the entity substitution changes construction *inputs*, not the registered randomness." | Legitimate: correct and important clarification |
| 17 | §8 | Budget: "420 forward passes … < 30 min" → "≈1,080 forward passes: 300 support + 2 B_wrong + 60 baseline + 720 conditions (the EXP075 spec's '420' counted conditions only and omitted support — same procedure, corrected accounting). ≈ < 45 min (sprint estimate scaled)" | Legitimate: LOG-100 F3 correction, honestly framed as disclosure fix |
| 18 | §9 | Title "What EXP075 does NOT test" → "EXP078"; numbering paragraph rewritten: EXP078 identity + retired-EXP075-number clause | Legitimate |
| 19 | Checklist | Adds: §0 note, substitution table w/ real-tokenizer verification, F2 guard armed, seeds identical, budget corrected, provenance honesty; drops "$K$ n/a" (K genuinely n/a) | Legitimate |

**No other differences exist.** No mechanism, threshold, gate value, seed, condition definition,
endpoint, or decision-tree logic changed. The draft is exactly what it claims to be: EXP075 +
entity substitution + honesty records.

## 3. Substitution-table verification (independent, real tokenizer)

| Substitute | Tokens (`" "+name`) | Old entity | Tokens | Collision |
|---|---|---|---|---|
| Joel | 1 ✓ | Caleb | 2 ✓ | none |
| Ruth | 1 ✓ | Miriam | 2 ✓ | none |
| Abel | 1 ✓ | Reuben | 2 ✓ | none |
| Ajax | 1 ✓ | Hector | 2 ✓ | none |
| Apollo | 1 ✓ | Nestor | 2 ✓ | none |
| Atlas | 1 ✓ | Priam | 2 ✓ | none |
| Julius | 1 ✓ | Lucius | 2 ✓ | none |
| Augustus | 1 ✓ | Titus | 2 ✓ | none |
| Diana | 1 ✓ | Silas | 2 ✓ | none |
| Eli | 1 ✓ | Sora | 2 ✓ | none |
| Finn | 1 ✓ | Leila | 2 ✓ | none |

Benchmark entities (Mars/Venus/Jupiter/Saturn/Mercury/Iron/Gold/Silver/Bronze/Steel): all
exactly 1 token ✓ — the "benchmark untouched" claim holds. Collision check covered all
support, benchmark, and named foil entities (B_wrong's Paris-capital contrast uses Paris,
already in V3 support — pre-existing design, unchanged). The spec documents the verification
method (leading-space convention, pythia-410m tokenizer, date 2026-09-23); the F2 guard
re-verifies at execution. Thematic grouping preserved (Biblical/Greek/Roman/Modern).

## 4. Decision-tree partition (M5.2)

The tree is byte-identical to the signed EXP075 tree except the two EXP075→EXP078 label
strings (items 11, 14). Precedence (a)→(b)→(c)→(d)→(e)→(f)→(g), (h)/(i) conditional on
(f)/(g). Exhaustiveness over the outcome space (gates passed, C3 valid): C4 (ΔM>0,p<0.05)→(e);
C4 (b=c=0)→(f); all other C4 cells (ΔM>0 p≥0.05; ΔM<0; ΔM=0 with b=c>0)→(g). No cell lacks a
branch; no cell lands in two branches. The entity change is orthogonal to the tree (no
branch conditions reference entities). **Partition intact.**

Note on (e)'s license text ("contingent on EXP070's ceiling verdict"): EXP070 has since
returned branch (c2) UNINFORMATIVE_PROBE. The contingency phrasing is verdict-agnostic and
remains correct — label-free findability is still not established. Not a finding.

## 5. MATH_STANDARDS_CHARTER (M1–M8) on new prose

- **M1:** §0/§3.1 additions use only previously defined terms (F2 guard, Law #4, B_agg
  procedure); no new symbols. ✓
- **M2:** New claims carry [FACT — procedural record] / [FACT] / [INTERPRETATION] labels
  per AGENTS.md §5. No theorem/proposition promotions; no condition-laundering (the
  provenance note states its condition — "would require reproducing the silent
  truncation" — in the sentence). ✓
- **M3:** Budget arithmetic 300+2+60+720 = 1082 ≈ 1,080 ✓ (matches LOG-100 F3).
  "< 45 min (sprint estimate scaled)" is disclosed as a scaled estimate, not a
  measurement. ✓
- **M4:** No operators redefined; shapes/spaces ($S \subset \mathbb{R}^{1024}$,
  $Q_S \in \mathbb{R}^{1024\times5}$) carried over verbatim from the signed spec. ✓
- **M5.2:** verified in §4 above. **M5.1/M5.3/M5.4:** no new decision procedures or
  statistical tests introduced. ✓
- **M6:** no new proofs/sketches. ✓
- **M7:** one carried-over instance — see MINOR-1 below. ✓ otherwise.
- **M8:** no new mathematical claims. ✓

## 6. §0 honesty audit

- "EXP075 was SIGNED and its execution bundle cleared for execution (LOG-107)" — matches log. ✓
- "triggered the F2 guard … 'Caleb' encodes to 2 tokens ([330, 43705]) … aborted the run
  before any forward pass" — matches LOG-111 and the smoke log (FATAL pre-construction). ✓
- "11 multi-token entities, all in the support vocabularies" — independently confirmed (§3). ✓
- Historical script "silent first-subtoken truncation, undisclosed" via
  `tokenizer.encode(" " + e)[0]` — confirmed by grep over
  `experiments/scripts/run_exp066_pythia410m_replication.py` (7 [0]-indexing sites). The note
  does **not** claim the EXP065/066 audit conclusions change — correctly scoped; the audit's
  conclusions concern Procrustes mathematics, unaffected by entity tokenization. No
  overstatement. ✓
- Law #4 basis explicit; "EXP075 remains on record as the aborted attempt; its number is
  retired, never reused" (§9) — correct number hygiene. ✓
- "No results exist under this protocol" retained. ✓

## 7. Findings

**MINOR-1 [M7.1, carried over from EXP075 — not introduced by this draft]:** Branch (f)
LICENSES contains "the EXP068 loop would be searching an empty room *in this
operationalization*". "Empty room" is metaphor doing illustrative work inside license text,
which M7.1 forbids; the operational content ("$S$, as constructed, is causally irrelevant
as a search space") survives deletion of the metaphor (M7.3), so this is decorative, not
load-bearing. **Fix (within one review cycle):** delete the "searching an empty room"
clause or relocate it to a motivation section. Not blocking: the sentence was signed in
EXP075, the draft's mandate was verbatim carryover, and altering it here would itself be
unlisted drift.

No MAJOR findings. No FATAL findings.

## 8. Verdict

**SIGN.** The draft is a faithful re-registration: the complete diff contains only the
declared entity substitution, the §0/§3.1/§8/§9 honesty records, and renames. The hard
constraint (single-token substitutes) was independently verified against the real tokenizer.
The decision tree's exhaustive partition is intact. M1–M8 hold on all new prose. The §0
record is accurate and correctly scoped. The banner may advance to PRE-REGISTERED.

*Adversarial note on what this review did not do:* it did not re-litigate EXP075's signed
design (mechanism, gates, thresholds) — that was settled by its own Law #14 review. It
verified that this draft *is* EXP075 plus the declared delta, and that the delta satisfies
its own hard constraint. The next load-bearing check is the EXP078 execution bundle's
Law #14 review, which must confirm the bundle's entity lists match §3.1 exactly and the F2
guard is armed against the real tokenizer (the failure mode that created this
re-registration). No primary artifacts modified; no results invented.*
