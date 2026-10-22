# Law #14 Independent Review — v84→v85 Change Plan (LOG-4872)

**Artifact under review:** `research/reviews/V85_CHANGE_PLAN_2026-10-01.md` (exact filename).
**Reviewer lane:** LOG-4872 (pre-assigned by the CEO). **$0 CPU, paper only.**
**Independence:** the reviewer did not draft the plan (draft lane: LOG-4871).
**Verdict: SIGN-WITH-FIXES** (1 required, 1 recommended, 1 nit).

---

## 1. What was verified independently

- **Abstract re-verified live** (2026-10-01, arXiv abs page for 2609.30275v1): title, author (Pranav Varshney), ID, and every substantive claim in the proposed text — the full-precision→quantized certification practice, scale-invariant statistics without noise floor, κ = nρ²/d with E[cos] ≈ (1+4/κ)⁻¹, ρ = 33–61 on Qwen2.5-1.5B-Instruct, 0.978–0.994 split-half agreement, the 0.996 cosine unevaluable without n, INT4 rotation beyond estimator noise, INT8 null explicitly not an equivalence claim, translation-vs-attenuation. All match the abstract; the proposed text overclaims nothing beyond it.
- **v84's own text checked:** `v84/paper.tex` has 0 "quantiz" hits (plan's claim confirmed); `\paragraph{Two measurement traps we close.}` exists at line 188 and describes exactly two traps, so inserting a separate new paragraph keeps "Two" accurate; the traps paragraph states "only McNemar decision flips count as causal evidence," so the proposed sentence "Our transfer claims rest on decision flips, never on cosine" is a true statement about the paper's discipline (the paper reports cosine values as the measured foil in C1, never as transfer evidence).
- **IEEE insertion point checked:** `v84-ieee/sections/sec-intro.tex` line 42, `\paragraph{Two measurement traps we close}` (no period — matches the plan), one flowing paragraph ending "...margin shifts are reported, never counted." Appending a "Third, ..." clause is grammatically sound. Citation commands match edition conventions (`\citep` main / `\cite` IEEE).
- **Sweep license checked** (LOG-4870): exactly one related-work addition licensed (Varshney); the sycophancy paper (2609.35544v1) marked tangential. The plan's exclusion follows its license.
- **Bib pattern checked:** proposed `@misc` entry matches `nadaf2026`'s field pattern exactly.

## 2. Bars

1. **Accuracy — PASS.** Every claim in the proposed insertion text is abstract-verified. The plan honestly flags its own abstract-only boundary (§3.1); body-level details (INT4/INT8 protocol) are not asserted in the proposed text, so none are needed.
2. **Scope discipline — PASS.** Related-work sentences only; no claim, result, figure, or numbered-claim changes; C1–C6 and the capability headline untouched; no experiment numbers named. The "no experiment numbers" restraint is the right call: v84 contains zero precision-certification discussion to attach them to, and naming EXP110/EXP138 would be ungrounded.
3. **Tone — PASS with F2.** "Convergent validation of that discipline, not corroboration of any boundary number" is exactly the honest fence. One title-level wording fix recommended below.
4. **Completeness — PASS.** Nothing missing. The sycophancy exclusion is correct per the sweep and the CEO's brief.

## 3. Fixes

- **F1 (required):** the plan says "one bib entry" but the IEEE edition's proposed clause cites `\cite{varshney2026cosine}`. The entry must be added to **both** `v84/refs.bib` **and** `v84-ieee/refs.bib`. As written, an implementer adding it to the main bib only would leave the IEEE build with an undefined citation. Name both files explicitly.
- **F2 (recommended):** the main-edition paragraph title "The quantization trap we preempt" slightly overclaims — the paper ran no quantization work, and a skimming reader could infer it did. The body text is careful; make the title match, e.g. "A quantization trap our discipline closes."
- **F3 (nit):** the abstract says "full-precision and quantized **refusal** directions"; the proposed text drops "refusal." The statistical point is estimator-general, but strict fidelity favors keeping the word or noting the generalization. Separately, the plan header's "announced 2026-09-29" is not abs-page-verified (page shows "Submitted on 12 Aug 2026"); harmless, as the date appears nowhere in the proposed paper text.

## 4. Verdict

**SIGN-WITH-FIXES.** The plan is accurate, scoped, and honestly framed. Apply F1 before implementation; F2/F3 at the implementer's discretion. No re-review required after fixes — they are editorial, not substantive.
