# S5-2 — Power audit of the static-geometry kills (2026-09-28)

**License:** LOG-4391 (S5-2 marked "QUEUED, dispatchable"). $0 CPU, zero new model forwards — pure arithmetic over committed statistics. No signed protocol touched; no weights loaded.

## Committed statistics used (all [FACT], sourced)

| Kill | Committed datum | Source |
|---|---|---|
| EXP065 geometric (Condition 1, static B_agg) | N=60, ΔM=0, b=0, c=0, p=1.0 (GPT2-XL L10) | `reports/adversarial_audit_exp065_exp066.md` ll.74–79; LOG-4384 |
| EXP066 geometric (replication) | N=60, ΔM=0, b=c=0, p=1.0 (pythia-410m L20) | LOG-3475; LOG-4384 |
| EXP077 ×8 (official GPU) | N=60/arm; radial α∈{0.25,0.5,1.0,2.0}: ΔM=+0.00pp, p=1.000000, S_H=[]; angular/control/offset/replication: b=0,c=0,p=1.0; baseline 0.5667 (34/60) | LOG-3387 verbatim evaluator ruling |
| EXP078 | ENERGY_GATE_HALT — no causal arms executed | LOG-117; LOG-3360 |
| EXP093 (L11) | N=60, Δ=0.0000, b=c=0 → p=1.0, all six tests | LOG-4352 |
| EXP094 (L11 per-item) | 0 decision flips across 120 injection item-arms; B=T=R=36/60, p=1.0000 | LOG-4375/4376/4377; `experiments/protocols/REVIEWS/EXP094_VERDICT_REVIEW_2026-09-27.md` l.48–50 |

Zero-flip reading for EXP077 radial arms: committed stats are (ΔM=0, p=1.000000); the zero-flip reading follows the ruling's "flat-zero trigger … flat zero across cone/line/offset/radial" language (LOG-3387). Even under b=c=k>0, ΔM=0 exactly constrains net movement to zero.

## Per-kill 95% upper bounds on flip-rate (0 events observed)

Method: exact one-sided 95% upper = 1 − 0.05^{1/n} (the quantity the rule-of-three 3/n approximates); two-sided Clopper–Pearson upper = 1 − 0.025^{1/n} as the conservative column.

| Kill | flips/n | Exact 1-sided 95% | Rule-of-three 3/n | CP 2-sided upper |
|---|---|---|---|---|
| EXP065 | 0/60 | 4.87% | 5.00% | 5.96% |
| EXP066 | 0/60 | 4.87% | 5.00% | 5.96% |
| EXP077 each variant (×8) | 0/60 | 4.87% | 5.00% | 5.96% |
| EXP093 | 0/60 | 4.87% | 5.00% | 5.96% |
| EXP094 aggregate (T+R) | 0/120 | 2.47% | 2.50% | 3.03% |
| EXP094 per-arm (T-vs-B, decision-relevant) | 0/60 | 4.87% | 5.00% | 5.96% |
| EXP078 | — | — | — | — (no flip datum; see note) |

## Same-bench pooled bounds

Bench families from committed baselines: Bench A = pythia-410m L20, 60 items, baseline 34/60 (EXP066 + EXP077×8 — EXP077's baseline "0.5667 (=EXP066 historical)" per LOG-3387); Bench B = pythia-410m L11, 60 items, baseline 36/60 (EXP093 + EXP094 on EXP092-B). EXP065 (GPT2-XL) is its own bench.

| Pool | flips/trials | Exact 1-sided 95% | Rule-of-three |
|---|---|---|---|
| Bench A: EXP066 + EXP077×8 | 0/540 | 0.55% | 0.56% |
| Bench B: EXP093 + EXP094 | 0/180 | 1.65% | 1.67% |
| Grand pooled (all causal static-geometry arms) | 0/780 | 0.38% | 0.38% |

**Pooling caveat [FACT]:** arms within a bench share the same 60 items, so arm-trial outcomes are not independent. The pooled figures above assume across-arm exchangeability (within-item independence). Under perfect cross-arm correlation the pool collapses to the per-arm 4.87%. The honest reading: pooled upper ∈ [0.55%, 4.87%] for Bench A, [1.65%, 4.87%] for Bench B — the pooled figure is an across-arm consistency bound, not a 540/180-item sample.

## EXP078 note (category correction)

EXP078 is not a flip-rate kill and contributes no bound: it halted at the pre-registered energy gate (e_median=0.0544 < 0.10; HALT_ENERGY) before any causal test executed. Its license is a localization measurement ("bridge's causal power lies almost entirely outside S"), not a causal null. No flip-rate arithmetic applies.

## Decision call

- **PIVOT?** No. No bound outruns its license: every kill's licensed claim (ΔM=0, p=1.0, "inert") is consistent with the computed bounds. No paper re-rating triggered — the paper's own limitation set already carries the N=60 blind spot (LOG-4390 Gap 2).
- **KILL the skeptic's "small real effect"?** Not earned. The skeptic's band is 1–5% flip-rate (LOG-4390 Gap 2: "N=60 blind to 1–5%"). The per-arm bound is 4.87% — it sits at the top of that band, not below it. What $0 arithmetic does buy: effects ≥4.87% per arm are dead on every bench; ≥2.47% dead on the EXP094 aggregate; ≥1.65% dead pooled at L11 (Bench B); ≥0.55% dead as an across-arm average on the L20 bench (exchangeability assumed). The 1–4.87% per-arm band remains the program's declared blind spot.
- **Verdict: CONFIRM + QUANTIFY.** Licenses hold; the skeptic is cornered into the declared blind band but not killed. This audit is the arithmetic receipt for LOG-4390 Gap 2: the N≈100+ replication remains priced (already priced, not newly discovered).
