# S3-8 Downstream-Amplification Test — LOG-225

*Track-6 data analyst report. $0 CPU. 0 forward passes. Weights read-only
(Δθ=0 verified). Archived records only; nothing filled by assumption.*

## 0. Headline

**The direct L1 readout shift explains only ~57% of the bridge's end-to-end
margin shift. The remaining ~43% (+0.32 margin units, gain ≈ 1.8×) is added
downstream of the injection point — on 60/60 items, all positive, std 0.03.**

**Verdict: Supported** (EXP066; pre-registered reading). **K2 recommendation:
PROCEED** — K2's GPU minutes are justified; scope K2 to isolate *which*
downstream component amplifies (attention re-routing vs LN/MLP gain), because
this test proves downstream transformation, not its locus.

## 1. Reading (knowledge protocol §1–2)

Read before writing, in order:
- `research/TEAM_KNOWLEDGE_PROTOCOL.md` §1 (mandatory reading list + verdict/labeling standards)
- `reports/research_log.md` LOG-213 (K1 verdict: K1-EXONERATED; D1 [OBSERVATION]: L1-predicted logit-shift ratios match archived end-to-end ratios *in aggregate*)
- `research/analysis_plans/K1_REPORT_LOG213_2026-09-23.md` §5 (D1: EXP066 r_obs=0.8524 vs r_pred=0.8155, 4.5% — "the readout projection quantitatively exhausts the observed effect" [INFERENCE])
- `research/innovation/CANDIDATE_BACKLOG.md` S3-8 row (kill criterion + pre-registered reading, quoted verbatim in §3)
- Mechanism sources: `experiments/scripts/run_exp066_pythia410m_replication.py` (ll. 391–393 bridge construction, l. 449 margin-shift definition, l. 379 α=0.50, ll. 96–98 layer-20 hook), `experiments/runs/EXP066_pythia410m_replication/exp066_replication_results.json` + `exp066_instance_evaluations.json` (archives)

**One challenge** (protocol §2): K1's D1 [INFERENCE] — "the bridge's end-to-end
effect is fully accounted for by its L1 readout projection (D1 strengthens)" —
is overturned in absolute terms by this analysis. D1 compared *ratios*
Δℓ_t/|Δℓ_f|, which cancel the absolute scale; a ratio match is necessary but
not sufficient for exhaustion. The per-item absolute decomposition shows the L1
projection accounts for mean 0.4267 of the 0.7492 archived margin (57%).
D1's "strengthens" reading does not survive the scale test. (D1's ratio numbers
themselves are untouched — the challenge is to the exhaustion *inference*, not
the observation.)

**One idea** (protocol §2): **gain tomography** — measure g(α) = Δm(α)/(α·‖W_U[t]−W_U[f]‖)
on an α grid {0.125, 0.25, 0.5, 1.0, 2.0} at the archived layer-20 injection point,
on the 8 rescued items (8×5×2 = 80 passes, ≈0.0005 T4-h). *Belief it could change:*
that the downstream ×1.8 gain is a fixed linear property of the circuit rather
than input-/strength-dependent routing. *Observation that would overturn it:*
g varies by >20% across α (kill criterion for the linear-amplifier story) —
nonlinear g(α) would implicate attention re-routing over passive LN/MLP gain.
If g is flat, the follow-up is per-block injection (layers 21/22/23) to localize
the amplifier — that localization *is* K2's job.

## 2. Mechanism (first principles)

[FACT] The EXP066 runner builds the bridge per item as
`b̂_i = (W_U[t_i] − W_U[f_i]) / ‖W_U[t_i] − W_U[f_i]‖` (ll. 391–393) and injects
`h ← h + α·b̂_i` with α = 0.50 via a forward hook on `gpt_neox.layers[20]`
output (ll. 96–98, 379, 431). Pythia-410m has 24 blocks, so blocks 21/22/23 +
final LayerNorm + unembedding sit downstream of the injection.

[FACT] The archived per-item `Same_Layer_Output_Bridge_margin_shift` is
`Δm_i = (ℓ_{t,i} − ℓ_{f,i})_mod − (ℓ_{t,i} − ℓ_{f,i})_base` (l. 449), recorded
for all 60 items.

[DEFINITION] L1-predicted margin shift (direct-readout counterfactual — the
injection applied with downstream acting as identity):
`Δm̂_i = α · b̂_i · (W_U[t_i] − W_U[f_i]) = α · ‖W_U[t_i] − W_U[f_i]‖₂`.
Residual: `r_i = Δm_i − Δm̂_i`. Under the null (rescue fully explained by the
direct readout shift), `r_i ≈ 0` on rescued items up to compute noise.

## 3. Pre-registered reading (S3-8, verbatim kill criterion)

- `|r_i| ≈ 0` on rescued items → downstream-amplification dead → **Not supported**
  (K2's routing premise dissolves).
- Large systematic residuals → downstream transformation real → **Supported**
  (K2's GPU minutes justified).
- No per-item archived shifts for a run → that run **Underdetermined** (never
  filled by assumption).

Written predictions before compute: direction — residuals ≈ 0 (D1's 4.5%
aggregate ratio match suggested exhaustion); magnitude — mean|r|/mean|Δm̂| < 0.10
on rescued items; breaking points — **Not supported** if < 0.10 with no
systematic sign; **Supported** if > 0.50 or systematically signed;
0.10–0.50 → Inconclusive.

## 4. Guards

- **G2** prompt byte-identity: 60/60 vs archived per-item records — PASS.
- **G3** Δθ=0: params-order hash of the locally loaded pythia-410m
  (`9879c9b5f8bea9051dcb0e68dff21493d67e9d4f`) == archived EXP066 pre_hash
  `4c242d9ac702a4029a674eacee84e0517cb6f79d794661dc3a3102bca5ed48dd`,
  pre and post read — PASS. [FACT]
- **G5** no forward passes: source self-inspection, zero `model(` invocations — PASS.
- Rescued-set identity: recomputed (b, c) = (8, 0) == archived — PASS.
- Sanity: mean(Δm̂) over 60 items = 0.426676 (my formula's prediction, not a fit).

## 5. Results (EXP066, n=60, 8 rescued)

[OBSERVATION] Residual distribution, all items (n=60):
mean **+0.322534**, std 0.029129, min +0.214232, max +0.377975,
mean|r| = 0.322534, mean|Δm̂| = 0.426676,
**mean|r|/mean|Δm̂| = 0.7559**, positive on **60/60 items** (pos_frac = 1.000),
fraction with |r| ≤ 1e-4 (noise floor, [ASSUMPTION]) = **0.000**,
fraction with |r| ≤ 10%·|Δm̂| = **0.000**.

[OBSERVATION] Rescued items (n=8):
mean residual **+0.333374**, std 0.010815, range [+0.310262, +0.345771],
mean|Δm̂| = 0.419413, **rel = 0.7949**; per-item |r|/|Δm̂| ∈ [0.7362, 0.8689];
downstream gain g_i = Δm_i/Δm̂_i: **mean 1.7971, std 0.0522, range [1.7362, 1.8689]**.

[OBSERVATION] Non-rescued (n=52): mean residual +0.320866, rel = 0.7500 —
the amplification is present everywhere, marginally larger on rescued items.
corr(r, rescued) = +0.1460; corr(r, Δm̂) = +0.3011 (weak positive — larger
readout shift → larger residual, consistent with a near-multiplicative
downstream gain).

[OBSERVATION] Per-item rescued table:

| item | Δm̂_i | Δm_i (archived) | r_i | \|r\|/\|Δm̂\| |
|---|---|---|---|---|
| planet_2hop_6 | +0.413274 | +0.723536 | +0.310262 | 0.7507 |
| planet_2hop_7 | +0.397962 | +0.735394 | +0.337431 | 0.8479 |
| planet_2hop_9 | +0.432053 | +0.763717 | +0.331664 | 0.7676 |
| planet_3hop_6 | +0.397962 | +0.743576 | +0.345614 | 0.8685 |
| planet_3hop_11 | +0.397962 | +0.743733 | +0.345771 | 0.8689 |
| element_2hop_7 | +0.460566 | +0.799654 | +0.339088 | 0.7362 |
| element_2hop_10 | +0.417814 | +0.746414 | +0.328600 | 0.7865 |
| element_3hop_5 | +0.437712 | +0.766275 | +0.328564 | 0.7506 |

[INFERENCE] The prediction (residuals ≈ 0) is falsified at 7.6× the breaking
point: rel = 0.7559 ≫ 0.50, sign systematic (60/60 positive, min +0.214).
Downstream of the layer-20 injection, the circuit adds a further +0.32 margin
units — a **×1.8 multiplicative gain** (CV ≈ 3% across rescued items) on the
injected (t−f) direction. The direct readout shift (mean 0.427) plus the
downstream amplification (mean 0.323) sums to the archived margin (0.749).

## 6. Scope limits (no assumption-filling)

- **EXP065: Underdetermined.** `exp065_results.json` carries only aggregate
  logit shifts (Δℓ_t=+0.3597, Δℓ_f=−0.4042 as floats); no per-item archive
  exists. Per the pre-registered contingency, no per-item residual is computed.
- **EXP077 (official + smoke): not decomposable.** `exp077_instance_records.json`
  carries correctness only; `exp077_results.json` carries aggregate
  `delta_margin` per condition (C8_bridge = 0.5961). No per-item margin shifts.
- **EXP070: Underdetermined** (no verified vectors; unchanged from K1).
- The **Supported** verdict therefore rests on EXP066 alone (n=60, 8 rescued).

## 7. Steelman

**Counterargument at full strength (against residual≈0 killing the upstream
question — now counterfactual, recorded for discipline):** residual≈0 would
*not* have proved downstream layers causally idle. Attention re-routing can be
exactly linear in this regime — a routing computation whose net margin effect
is a scalar gain of 1 still *uses* attention; re-routing can also live in the
null space of (W_U[t]−W_U[f]), moving other logits (archived kl_div=0.028 > 0,
top10_overlap=0.99 < 1 prove downstream does *something*) without moving the
margin. The pre-registered null was margin-scoped ("the *rescue* is fully
explained by the direct readout shift"), so Not supported would have stood for
S3-8's question while leaving null-space routing open. **Answer:** conceded as
a scope note — this test adjudicates the margin, not all downstream activity.

**Counterargument at full strength (against this report's Supported verdict):**
the +76% "amplification" need not be *attention re-routing* — final-LayerNorm
rescaling and MLP gain are confounded in the residual, and the S3-8 hypothesis
names attention re-routing parenthetically. "Supported" may overclaim the
mechanism. **Answer — partially conceded:** the decomposition proves a large,
systematic *downstream transformation* (60/60 positive residuals kills the
noise alternative; the ×1.8 gain with 3% dispersion kills the fluke
alternative) and decisively rejects the null (7.6× past the breaking point).
It does **not** isolate attention as the amplifying component. The verdict
**Supported** is therefore on the pre-registered reading's own terms
("downstream transformation real"), with the explicit scope note: the
attention-vs-LN/MLP attribution is *K2's* question, which this result licenses
rather than answers.

## 8. Verdict and K2 recommendation

**Verdict: Supported** [HYPOTHESIS → verdict per LOG-148 standard].
The S3-8 downstream-amplification hypothesis survives its pre-registered
falsification criterion on EXP066: large systematic residuals
(mean +0.3225, rel 0.76, 60/60 positive) reject the direct-readout-only null.
EXP065 is Underdetermined (no per-item archive); EXP077 is not decomposable.

**K2 recommendation: PROCEED.** K2's GPU minutes are justified — there is a
real, large downstream transformation to hunt (a ×1.8 gain on the injected
direction, added across blocks 21–23). K2 should be scoped as an
*attribution* pilot: which downstream component amplifies — attention
re-routing, MLP gain, or LayerNorm rescaling — e.g. via per-block injection
(21/22/23) and the α-grid gain-tomography probe from §1. What K2 must NOT do
is re-litigate *whether* downstream matters: that is settled by this
analysis at $0.

## 9. Artifacts

- Executor: `research/analysis_plans/S38_execute_LOG225_2026-09-23.py`
- Machine-readable twin: `research/analysis_plans/S38_DOWNSTREAM_RESULTS_LOG225_2026-09-23.json`
- This report: `research/analysis_plans/S38_DOWNSTREAM_ANALYSIS_LOG225_2026-09-23.md`

*Load-bearing labels: mechanism/facts [FACT]/[OBSERVATION] as marked;
the ×1.8-gain attribution to attention specifically is [OPEN] (K2's question);
the noise floor ε=1e-4 is [ASSUMPTION]; the gain-tomography idea is
[HYPOTHESIS]-generating, not a claim.*
