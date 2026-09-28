# S6-5 — Pooled power audit of EXP093–EXP096 (2026-09-28)

**License:** LOG-4408 (innovation sprint, ranked #5, "dispatchable in parallel immediately"). $0 CPU, zero new model forwards — pure arithmetic over committed records. No signed protocol touched; no weights loaded. Read-only on records.

**Method [FACT]:** flip counts recomputed from the primary CSVs by `s6_5_recompute_2026-09-28.py` (pure-stdlib; own binomial-CDF bisection for Clopper–Pearson — no statistics library trusted). Exact one-sided 95% upper = smallest p with P(X ≤ k | n, p) = 0.05 (closed form 1 − 0.05^{1/n} for k = 0, verified by bisection); CP two-sided upper = smallest p with P(X ≤ k | n, p) = 0.025. Same convention as S5-2 / LOG-4392.

## Committed statistics used (all [FACT], sourced)

| Experiment | Committed datum | Source |
|---|---|---|
| EXP093 (L11, shared ±v direction) | b = c = 0 on P-vs-B and N-vs-B → 0 flips / 60-item arm (zero-flip entailed by b=c=0) | `experiments/protocols/REVIEWS/EXP093_LAW14_VERDICT_REVIEW_2026-09-25.md` Check 1; LOG-4352 |
| EXP094 (L11 per-item) | 0 flips across 120 injection item-arms (T 60 + R 60); B=T=R=36/60 | LOG-4375/4376/4377; EXP094 verdict review §2 |
| EXP095 (L11 per-item α-sweep) | T-vs-B flips {0,0,0,1,1} over α ∈ {0.25,0.5,1.0,2.0,4.0}; B_wrong {0,0,0,0,2} | LOG-4400; EXP095 verdict review §1 |
| EXP096 (L11 per-item, gated α=8.0) | T(8.0): 3/21 flips (b=1,c=2,p=1.0); B_wrong(8.0): 3/21 (b=2,c=1,p=1.0); 5 wrong/16 right at baseline | LOG-4407; EXP096 verdict review §1 |
| S5-2 pools (carried) | EXP065 0/60; EXP066 0/60; EXP077 ×8 0/60 each; Bench A 0/540; Bench B 0/180; grand 0/780 | LOG-4392 |

## Recomputation verification (this lane, from primaries)

[OBSERVATION] Recomputed from `experiments/runs/EXP095_alpha_sweep/out/per_item_records.csv` (660 rows): per-(α, arm) flips vs B are exactly {T: 0,0,0,1,1; B_wrong: 0,0,0,0,2} — zero discrepancies with LOG-4400. From `experiments/runs/EXP096_headroom_gated/out/per_item_records.csv` (102 rows): T(8.0) 3/21, B_wrong(8.0) 3/21 — zero discrepancies with LOG-4407.

[OBSERVATION] S5-2 verification sample recomputed by this lane's independent code: 0/60 → 4.87%, 0/120 → 2.47%, 0/540 → 0.55%, 0/180 → 1.65%, 0/780 → 0.38% — all five reproduce LOG-4392 exactly.

**Flip definition [DEFINITION]:** one trial = one injection cell ((item, α, arm) for EXP095; (item, arm) for EXP094/EXP096); an event = the cell's top-1 correctness differs from the baseline decision for the same item (and α). Margin shifts without decision change are NOT events — the bound is on decision-flip rate, not on margin movement (margins did move; EXP093's review documents +0.0059/−0.0076 mean shifts).

## Per-experiment bounds (new)

| Experiment | flips/trials | Exact 1-sided 95% | CP 2-sided upper | Observed rate |
|---|---|---|---|---|
| EXP095 T-only (task direction) | 2/300 | 2.08% | 2.39% | 0.67% |
| EXP095 all injection (T + B_wrong) | 4/600 | 1.52% | 1.70% | 0.67% |
| EXP096 T-only, gated set | 3/21 | 32.92% | 36.34% | 14.29% |
| EXP096 all injection, gated set | 6/42 | 26.26% | 28.54% | 14.29% |

[INTERPRETATION] EXP096's gated set alone (n=21) is nearly uninformative — 32.92% upper. Its evidentiary weight comes from pooling with the family, not from standing alone. This is disclosed, not hidden.

## Pooled bounds

| Pool | flips/trials | Exact 1-sided 95% | CP 2-sided upper | Observed |
|---|---|---|---|---|
| **Static per-item family, T-only** (EXP094 T 0/60 + EXP095 T 2/300 + EXP096 T 3/21) | 5/381 | **2.74%** | 3.04% | 1.31% |
| Static per-item family, all injection | 10/762 | 2.22% | 2.40% | 1.31% |
| Bench B extended (pythia-410m L11, EXP092-B: EXP093 0/60 + EXP094 0/120 + EXP095 4/600 + EXP096 6/42) | 10/822 | 2.05% | 2.23% | 1.22% |
| Grand extended (S5-2 0/780 + EXP095 4/600 + EXP096 6/42) | 10/1422 | 1.19% | 1.29% | 0.70% |

**Pooling caveat [FACT]:** cells within a pool share the same 60 EXP092-B items, so cell outcomes are not independent — EXP095's two T flips are the *same item* at α=2.0 and α=4.0, and EXP096's gated 21 are a subset of the same 60. The pooled figures assume across-cell exchangeability. Under perfect cross-cell correlation the pool collapses toward the per-cell 4.87%. Honest reading: the family T-only pooled upper ∈ [2.74%, 4.87%] — an across-cell consistency bound, not a 381-independent-item sample. (Same caveat class as LOG-4392's.)

**Family-mix note [FACT]:** EXP093 used a *shared* ±v direction, not per-item directions — it is a different family from EXP094/095/096. The "static per-item family" pools exclude it; the Bench-B-extended and grand pools include it and are labeled family-mixed.

**B_wrong reading [OBSERVATION]:** B_wrong flipped 2/300 at EXP095 α=4.0 and 3/21 at EXP096 α=8.0 — the items *are* flippable by large random nudges. The task-direction bound (T-only) is the causal-inertness quantity; the all-injection bound mixes in the flippability control. Both are reported; neither is hidden.

## What the pooled bound buys — and does not buy

**Buys [INTERPRETATION]:** across the closed static per-item family, task-direction flip-rates ≥ ~3% are dead (2.74% one-sided / 3.04% two-sided, exchangeability assumed); ≥ ~2.2% dead counting all injection cells. The EXP095+EXP096 verdicts' "zero-ish" readings are now arithmetically receipted: the observed family rate is 1.31% with an upper bound under 3.1%.

**Does not buy [INTERPRETATION]:** (1) It does not convert the null into a positive — a bound is a ceiling on the effect, not evidence of absence; "inert" remains a licensed shorthand for "below the bound," never a proof of zero. (2) It does not touch margin shifts — the interventions demonstrably moved logits; the bound is decision-flips only. (3) It does not license the >0.4740-ratio regime, other layers, or gated/dynamic mechanisms (binding scope fences from LOG-4400/4407).

## The skeptic's 1–5% band — where it stands now

[INTERPRETATION] LOG-4390 Gap 2 priced the blind spot at 1–5% per N=60 arm. Status after this audit:
- **Single-cell blind spot: unchanged.** One (item, arm, α) cell at n=60 still carries 4.87% — the 1–4.87% band is the program's declared per-cell blind spot, and no $0 arithmetic moves it.
- **Family-pooled: the skeptic is cornered into 1–~3%.** The static per-item family's T-only upper is 2.74% (one-sided) / 3.04% (two-sided). A skeptic positing a 3–5% task-direction flip-rate across the family is now ruled out (exchangeability assumed); a skeptic positing 1–3% is not.
- **The N≈100+ replication remains priced** (LOG-4390, LOG-4392) — this audit moves the pooled ceiling, not the per-cell floor. No paper re-rating triggered: the paper's limitation set already carries the N=60 blind spot.

## Decision call

- **PIVOT?** No. No bound outruns its license: every kill's licensed claim (ΔM≈0, p=1.0, "inert") is consistent with the computed bounds — the observed family rate (1.31%) sits comfortably under every upper bound.
- **KILL the skeptic's "small real effect"?** Not earned at $0 — the 1–~3% family band and 1–4.87% per-cell band survive. What $0 buys: ≥4.87% dead per cell; ≥2.74% dead across the static per-item family (T-only); ≥2.05% dead on the extended L11 bench; ≥1.19% dead grand-pooled (family-mixed, exchangeability assumed).
- **Verdict: CONFIRM + QUANTIFY.** The EXP094/095/096 kills hold; the skeptic is cornered from 1–5% into 1–~3% (family) while the per-cell 1–4.87% blind spot stands as declared. This audit is the arithmetic receipt for the EXP095+EXP096 closure: the two-experiment boundary law now carries a number — below ~3%, not below zero.

## Files

- This report: `research/analysis_plans/S6_5_POOLED_POWER_AUDIT_2026-09-28.md`
- Recomputation script: `research/analysis_plans/s6_5_recompute_2026-09-28.py` (pure stdlib)
- Bounds JSON: `research/analysis_plans/s6_5_bounds_2026-09-28.json`

*Dated 2026-09-28. $0 compute; no model executed; no weights touched; no signed artifact edited. All flip counts recomputed from primary CSVs; all S5-2 sample bounds reproduced exactly.*
