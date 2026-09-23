# Adversarial Audit Report: EXP065 / EXP066 Stage A & Statistical Endpoints

**Auditor role:** Adversarial Reviewer (red-team) + Implementation Agent (code forensics)
**Date:** 2026-09-23
**Scope:** `experiments/runs/EXP065_coordinate_alignment/`, `experiments/runs/EXP066_pythia410m_replication/`,
`experiments/scripts/run_exp065_temporary_coordinate_alignment.py`, `experiments/scripts/run_exp066_pythia410m_replication.py`,
`.muse by meta/COMPREHENSIVE_EXPERIMENT_LEDGER.md`, `.muse by meta/README.md` §3, `manifest.json`
**Method:** Recomputed all Stage A statistics directly from primary artifacts (result JSONs + run logs);
traced the Procrustes operator through source; inspected the Wilcoxon endpoint definition in code.
No new experiments were run; no numbers were generated beyond recomputation of stored artifacts.

**Epistemological labels** follow `AGENTS.md` §5 (`[FACT]`, `[OBSERVATION]`, `[INTERPRETATION]`, `[CONJECTURE]`, `[ASSUMPTION]`, `[OPEN]`).

---

## FINDING 1 [CRITICAL]: Summary documents contradict primary artifacts on Stage A

**[OBSERVATION]** Recomputation from `exp065_results.json` (`stage_A_alignment_discovery`):

| Vocab | raw_cosine | aligned_cosine | delta_cosine |
|---|---|---|---|
| V2_Biblical | +0.7379 | -0.0640 | -0.8019 |
| V3_Greek | +0.7144 | +0.0217 | -0.6927 |
| V4_Roman | +0.6996 | +0.0023 | -0.6973 |
| V5_Modern | +0.7224 | +0.0527 | -0.6697 |
| **mean** | **+0.7186** | **+0.0032** | **-0.7154** |

The run log independently records: `Stage A Summary: Mean Raw Cosine = +0.7186 | Mean Aligned Cosine = +0.0032`.

**[OBSERVATION]** Recomputation from `exp066_replication_results.json` (`stage_A_alignment`): mean raw
+0.6852 → mean aligned -0.0118, **delta = -0.6971**. Run log confirms.

**[FACT]** The ledger (`.muse by meta/COMPREHENSIVE_EXPERIMENT_LEDGER.md` §2.3) states:
"Stage A (Alignment Discovery): Procrustes rotation **increased** cross-vocabulary alignment by **+0.1290**
cosine similarity over raw directions." The handover README (§3) generalizes to "robust geometric alignment
under closed-form Procrustes rotation (Δcos ≈ +0.13 to +0.79)".

**[INTERPRETATION]** The claimed +0.1290 is irreconcilable with the primary artifacts (sign flipped,
magnitude off by ~5.5x). Both flagship runs show the Procrustes step **destroying** cross-vocabulary
similarity (→ ~0), not improving it. The "+0.79" figure appears misattributed from EXP064 Level A
(raw aggregated-basis alignment, a different quantity — not a Procrustes delta).

**Required action:** Correct the ledger, handover README §3, and `manifest.json` `key_findings`
to report Δcos ≈ -0.72 (EXP065) / -0.70 (EXP066), raw cosine ≈ +0.70. Per Law #2/#11, summaries must
match primary artifacts. The +0.1290 figure must be either sourced to a real artifact or retracted.

---

## FINDING 2 [CRITICAL]: The Procrustes alignment operator is mathematically unsound for its stated purpose

**[FACT]** (from source, `run_exp066...py` lines 196–203 and `get_procrustes_rotation`, lines 381–389;
identical structure in the EXP065 script):
```python
U, S, Vh = torch.linalg.svd(E_k.T @ E_0_2hop)   # E_*: [2, d] stacks of unembedding rows
R_k = U @ Vh                                    # [d, d]
v_aligned = R_k @ v_hat_by_vocab["V1_Anglo"]    # v_hat: hidden-state contrast direction
```
- `E_k`, `E_0` are 2×d stacks of **unembedding** vectors (`model.embed_out.weight` rows for entity tokens).
- `v_hat` is a **residual-stream contrast direction** Δh = h(rel) − h(neu) at the target layer (layer 10 / 20).

**[FACT]** M = E_k^T @ E_0 is d×d but rank ≤ 2. The orthogonal Procrustes solution R = U V^T is therefore
constrained only on the 2-dimensional anchor subspace; on the remaining (d−2)-dimensional orthogonal
complement the SVD completion is arbitrary with respect to the task.

**[INTERPRETATION]** Applying R to a generic hidden-state direction scrambles almost all of its energy:
the expected post-"alignment" cosine is ~0 regardless of input. The observed values (-0.0118, +0.0032)
are exactly this predicted outcome. **The Stage A "failure" is not a scale effect or a mystery — it is the
mathematically expected output of the operator as implemented.**

**[ASSUMPTION] (unstated, now falsified-or-unsupported):** that a rotation fit on unembedding-space token
vectors transfers to residual-stream relational-reasoning directions. No validation of this cross-space
transfer was performed; EXP065/066 Stage A are evidence against it.

**Consequence for Stage B:** Condition 2 ("Aligned Dynamic Basis", R(x) @ B_agg) injected a
**scrambled** basis, not an aligned one. Its ΔM = 0 therefore cannot support the claim
"geometric alignment is not sufficient for causal interchangeability" — the alignment premise was never
satisfied. The valid boundary evidence is **Condition 1 (Static B_agg)**: raw cross-vocabulary cosine was
already ~0.69 with no rotation, yet injection yielded ΔM = 0.0 (b=0, c=0, p=1.0) under full headroom
(26 rescuable errors), while the output-bridge control rescued 8/26 (p=0.0078). **The paper's central
claim should be reframed around the static-basis result, not the Procrustes narrative.**

**[OPEN]** Whether a *sound* alignment operator (fit in the same space as the intervention, full-rank
constraints — e.g., the proposed EXP067 QK/OV subspace Procrustes) would change the Stage B verdict.
EXP067 is well-motivated precisely as a fix for this finding.

---

## FINDING 3 [HIGH]: The Wilcoxon endpoint is a statistical trap

**[FACT]** (from source, line 459): `wilc_p = float(stats.wilcoxon(margin_shifts).pvalue)` where
`margin_shift = (t_l_m − f_l_m) − (t_l_b − f_l_b)` — the per-instance change in target-minus-foil
**logit margin**, not a decision variable.

**[OBSERVATION]** EXP066 endpoints:

| Condition | ΔM | b | c | McNemar p | Wilcoxon p (margins) | mean Δmargin |
|---|---|---|---|---|---|---|
| Static_B_agg | 0.0 | 0 | 0 | 1.0 | 0.041 | +0.009 |
| Aligned_Dynamic_Basis | 0.0 | 0 | 0 | 1.0 | **1.6e-11** | **−0.041** |
| Same_Layer_Output_Bridge | +0.133 | 8 | 0 | 0.0078 | 1.6e-11 | +0.749 |
| Random_Rotation_Control | +0.007 | 0.4 | 0 | 1.0 | n/a | −0.003 |
| Dynamic_B_perp | 0.0 | 0 | 0 | 1.0 | 0.21 | +0.003 |
| Dynamic_B_wrong | 0.0 | 0 | 0 | 1.0 | **1.2e-08** | −0.021 |

**[INTERPRETATION]**
1. A "highly significant" Wilcoxon p with b=c=0 means only that the intervention systematically shifted
   logit margins without flipping any decision — a distributional nudge, not a causal effect.
2. The **negative control** `Dynamic_B_wrong` (unrelated Paris-capital contrast) is "significant" at
   p=1.2e-08. **[INTERPRETATION]** Margin-shift significance is therefore not task-relevant evidence:
   *any* residual-stream injection perturbs margins. Citing wilcoxon_p as support for a causal claim
   would be invalidated by the project's own control.
3. Notably, the "aligned" intervention shifted margins **negatively** (−0.041, p=1.6e-11): consistent
   with Finding 2 — a scrambled basis acts as structured noise slightly suppressing the target logit.
4. The ledger correctly reports only McNemar. But the raw `wilcoxon_p` fields in the JSONs invite
   misreading by future agents or readers.

**Required action:** Relabel `wilcoxon_p` as exploratory (or remove as an endpoint); add a note that
margin-shift significance is invalidated as a causal measure by the B_wrong control. Do not report
Wilcoxon p-values alongside McNemar without this qualification.

---

## FINDING 4 [MEDIUM]: Positive-control interpretation boundary

**[FACT]** `make_bridge_vec` builds the bridge from `embed_out.weight[t_target] − embed_out.weight[t_foil]`
— a normalized **unembedding-space** direction — injected at the target layer.

**[INTERPRETATION]** This is near-direct answer-logit steering; its success (+13.3pp, 8/26 rescues) shows
that behavior is steerable at layer 20 via output-space directions. That is expected, not a validation of
the SCBI mechanism. It is a legitimate "causal access exists at this layer" control, but must not be
framed as supporting the representation-synthesis theory. (KL divergence corroborates: bridge 0.028 vs
~0.0002 for basis conditions — only the bridge meaningfully moves the output distribution.)

---

## FINDING 5 [LOW]: Experiment inventory gap

**[OBSERVATION]** The ledger claims EXP001–EXP066 (66 experiments); `experiments/runs/` contains 61
directories, with EXP001–EXP006 bundled in one and **EXP051, EXP055 absent**. Minor bookkeeping gap;
reconcile or annotate.

---

## Recommended corrections (require Research Manager sign-off per Law #12)

1. Amend ledger §2.3/§2.4, handover README §3, and `manifest.json` `key_findings.geometric_alignment`:
   raw cosine ≈ +0.70 (genuine, no rotation); Procrustes Δcos ≈ −0.72/−0.70 (destroys similarity).
2. Reframe the central scientific claim: **high raw cross-vocabulary geometric similarity (~0.7) of
   relational contrast directions with zero causal transfer under static injection (ΔM=0, full headroom)
   vs. +13.3pp output-bridge rescue** — this is the clean, defensible boundary result.
3. Reposition EXP067 (QK/OV subspace Procrustes) as the *fix* for Finding 2: same-space, full-rank
   alignment — the experiment that actually tests whether sound alignment enables causal transfer.
4. Stats hygiene: demote `wilcoxon_p` to exploratory with the B_wrong invalidation note.
5. Complete the literature review (currently `TBD` in `reports/novelty_report.md`) **before** any paper
   draft: the reframed claim needs positioning against steering-vector / activation-addition /
   representation-engineering prior art, where brittleness of steering on complex reasoning is documented.
6. Reconcile the EXP051/EXP055 inventory gap.

**What was NOT done:** no data was modified, no summaries were rewritten, no new experiments were run.
Corrections are proposed, not applied — awaiting sign-off.
