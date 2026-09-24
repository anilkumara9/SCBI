# Law #14 Adversarial Review — EXP080/081 License Addenda (LOG-209)

**Reviewer:** independent Track-7 (adversarial) specialist · **LOG-210** · 2026-09-23
**Independence:** no prior involvement in the §A.6 addenda, the §A.6 sketch, or the EXP080/081 protocols. All drafter claims treated as untrusted; every quote and derivation re-checked against signed text.
**Verdict: SIGN-WITH-FIXES** (two mechanical fixes, both applied by the reviewer to the unsigned addendum drafts; enumerated below). Neither fix touches a grade, a breaking point, or the signed protocols.
**Law #15 (on record, LOG-210):** Q1 — do the addenda meet the §A.4 template and §A.3 grade discipline, and is the §H7 relabeling faithful? (answered below, five attacks). Q2 — CONTINUE: SIGN releases the addenda as GPU-clearance preconditions for EXP080/081. Q3 — cheapest: $0 read-only review. Q4 — n/a honestly (review, not experiment).

---

## Standup

**What I did.** Attacked both addenda in the dispatched order, recomputing rather than trusting: (1) grade discipline — verified every quoted statement against the signed protocols line-by-line and independently re-derived the EXP080 McNemar collapse (p = 2^{1−b} under the spec's doubled two-sided convention) and the EXP081 regrouping identity from the pinned formula; (2) the §A.6 point-5 finding — read signed §5.1 with the LOG-182 F1 fix and the LOG-181 review's F1 text; (3) §H7 relabeling — checked both addenda against LOG-204 ruling 1 and the LOG-197 decision brief for smuggled mechanism authority; (4) multi-license honesty — confirmed the weakest-grade ceiling authorizes exactly the signed runs (1,320 / 660 passes) and nothing more; (5) §A.4 template completeness — L1–L4, outcome partition, assumption inventory, review line. Also verified via `git status` that both signed protocols are byte-untouched, and verified the LOG-171/LOG-181 review-record quotes cited in the addenda.

**What surprised me.** The §A.6 sketch's L3 line ("⇒ the C-A transfer claim is dead") genuinely over-read the signed rule it cited — the signed §5.1 says the fragility flag is "reported, never promoting or demoting the verdict," and the transfer claim dies only via the §8 tree. The drafter's correction is not spin; it is faithful, and this is the §A.6 transition's finding-generator function working as designed. Second surprise: the LOG-171 review itself documented "two separate forward passes of B_agg must agree" as the determinism pin's load-bearing content — so the addendum's parenthetical is inherited from the review record, not invented by the drafter.

**What I am uncertain about.** Nothing load-bearing. One residual note (observation, not a fix): EXP081's L2 adapts the §A.4 template to a design-element license rather than quoting a primary endpoint verbatim — disclosed and justified in the text, and §A.3's multi-license rule anticipates per-design-element licenses. I accept the adaptation; a future standard revision may want a worked example for design-element licenses.

**What I need.** Nothing from the CEO except acceptance of this verdict. The two fixes are already applied; the addenda are clearance-ready as signed drafts.

---

## Findings (attack order)

### 1. Grade discipline (§A.3) — HONEST, both addenda

**EXP080 (IN-HOUSE-PROOF).** Lemma L1 quoted verbatim from signed §4.5 (verified character-for-character). Proof sound conditional on the §11 determinism pin (the pin is the named premise; the "two separate forward passes" point is in the LOG-171 record). Branch mapping independently re-derived: with c = 0, two-sided exact McNemar on (b, 0) gives p = 2^{1−b} → b=5: 0.0625 ≥ 0.05 (c); b=6: 0.03125 < 0.05, +10.0pp < +12pp (d); b=8: 0.0078125, +13.3pp ≥ +12pp (e). Matches signed §4.5, §6.1 grid ((5,0)→0.0625, (6,0)→0.03125, (8,0)→0.0078), and §9. The addendum declines PROVEN-LEMMA on the correct ground (LOG-171 was a protocol review, not a per-step Charter M2.2 proof attack) — grade-conservative, as §A.3 requires.

**EXP081 (IN-HOUSE-PROOF).** §4.1 identity quoted verbatim; proof quoted verbatim; I re-derived the regrouping from the pinned formula independently (exact). JSON cos = 0.9999999999999998 verified at `/part2_log174/c5_bank/cos_centroid_c5_c3`. Grade-conservative for the same M2.2 reason, stated explicitly.

**Minor fix applied (EXP080 L2):** the draft said the McNemar "collapses to a one-sided binomial test on b." Under a pure one-sided binomial, p = 2^{−b}, which would move the (c)/(d) boundary to b ≤ 4 — contradicting the (correctly quoted) mapping (c) ⟺ b ≤ 5, which requires the signed spec's doubled two-sided convention (p = 2^{1−b}, confirmed by the §6.1 grid and the LOG-171 re-derivation). Numbers in the addendum were right; only the label was loose. Rephrased to "collapses to a b-only binomial test on b — under the signed spec's doubled two-sided exact convention (p = 2^{1−b}; hence (c) ⟺ b ≤ 5, not b ≤ 4)."

**Minor fix applied (EXP081 L1):** the draft attributed both the cos and the "‖S_C5−S_C3‖ = 0.000e+00" figures to the JSON. The cos is JSON-verified; the norm-difference figure is not locatable in the JSON — it is stated as [FACT] in the signed spec (§5.2/§R0.1), which is the addendum's proper authority under the §A.6 recovery rule. Citation split accordingly. Not grade-affecting: the authorizing result is the proved identity, and the JSON corroboration that matters (cos) is verified.

### 2. The §A.6 point-5 finding — CORRECTION FAITHFUL, no finding against the addendum

Signed §5.1 (with LOG-182 F1 fix, de-duplication by distinct (t_d, f_d) content — F1 text confirmed in the LOG-181 review §7): below ⌈5n_d/6⌉ agreement → the T3 license line carries the "tie-break-fragile" caveat — "reported, never promoting or demoting the verdict. The T3 conjunct decides on the pinned winner alone." The ratified §A.6 sketch's "⇒ the C-A transfer claim is dead" over-reads this rule. The addendum's replacement is exact: the transfer claim dies only via §8 — outcome (b) (T1 null ⇒ Not supported; family-level kill licensed ONLY for unembedding-difference donor bridges at l*=20 on this benchmark) or outcome (c) (any of T3–T5 fails ⇒ Not supported; Refuted under the pinned conditions: C4′ rescues vs C1 while T3 fails, or rescue fully accounted for by s_t(j)−s_f(j) with β1 null). All verified verbatim against signed §8.

### 3. §H7 relabeling — FAITHFUL, no smuggling found

Both addenda carry the LOG-204 ruling-1 relabel verbatim: "rescue control (known-answer direction), NOT a mechanism control" (ruling text confirmed in `reports/research_log.md` LOG-204). Surviving roles match the signed protocols exactly: EXP080 C7 → §7 C3-vs-C7 secondary (zero extra passes) + §9(c) bridge-replication contingency; the "(§6.1 m4)" citation checks out (m4 states "branch (b) contains no C7 conjunct by design"). EXP081 C2 → strictly T2 procedure-validity (T2 failure → Inconclusive, overriding (b)/(c) — signed §8). The "no label-free control" admissions are honest and complete: EXP080 tests no autonomous-mechanism question (label-informed Level-1 ceiling by design, §1.1 — "no label-free control exists in this design and none is needed"); EXP081 states outright "There is no label-free positive control for transfer in this design — the transfer license is earned conjunctively (T1–T5)," with C4′/C6/S1–S6 correctly characterized as label-free-at-test-time (verified against signed §3.3: fixed bank-level centroid, identical for all 60 items). The bank-prior channel's unlesionability is recorded as a known Level-1 limitation (§8 [AFFIRMATION]), not a hole. No surviving sentence restores the bridge's mechanism authority; every surviving use is fenced as rescue-capability/procedure-validity, matching the LOG-197 brief's DEMOTE option.

### 4. Multi-license honesty — CEILING CORRECTLY APPLIED

Both addenda note H_ceiling-G2 / H_transfer as CONJECTURE-UNDER-TEST and apply the §A.3 weakest-grade rule: cheapest discriminating experiment only — 1,320 passes (EXP080, signed §10 budget verified) / 660 passes (EXP081, signed §10 budget verified). Nothing more is licensed: EXP080 fences Phase B behind a new pre-registration; EXP081 states the identity "licenses no transfer win." The §9(d)/(e) "output room" gating and the §8 conjunctive license are recovered without inflation.

### 5. Template completeness (§A.4) — COMPLETE

EXP080: L1 (exact statement / source + review record / [THEOREM] label) ✓; L2 (endpoint verbatim from §7 ✓; predictions with numbers ✓; derivation ✓) ✓; L3 (lemma-falsifier, licensed-question falsifier, license-scope falsifier, each with a decision; M5.2/M5.3/M5.4 partition ✓) ✓; L4 (A1 determinism pin with its "where supported" hedge named, A-family, A-generous, A-bridge-dominance; promotion path ✓) ✓. EXP081: L1 ✓; L2 (adapted to a design-element license — disclosed; quantitative prediction with measured numbers; derivation) ✓; L3 (identity falsifier with KILL-the-design decision; F1 fragility rule verbatim; §8 reachability partition ✓) ✓; L4 (A4, L5, bypass model, bank-set pin; promotion path ✓) ✓. Law #14 review lines present in both, now filled. Signed protocols byte-untouched (`git status`: no modifications to either spec).

---

## Verdict

**SIGN-WITH-FIXES.** The addenda meet the §A.4 template, the §A.3 grade discipline is honest (conservative where it counts), the §A.6 point-5 correction is faithful to signed text, and the §H7 demotion is propagated without smuggling. The two fixes were mechanical and are applied; the review lines in both addenda are filled (LOG-210, 2026-09-23). On CEO acceptance, both addenda are released as GPU-clearance preconditions per LOG-204 ruling 3. The signed protocols were not edited, and no signed-protocol edits are proposed.

**Permitted-category check:** this review uses only the five evidentiary verdict categories where verdicts are stated; "interesting/promising/elegant" appear nowhere as evidentiary claims. No INTUITION-graded license is cited in either addendum.
