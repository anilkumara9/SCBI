# Procrustes Failure Analysis: Why the EXP065/066 Alignment Operator Scrambles

**Author role:** Theory Agent
**Date:** 2026-09-23
**Status:** First proof document in `theory/proofs/`
**Depends on:** `reports/adversarial_audit_exp065_exp066.md` (Finding 2), `theory/BOUNDARY_CLAIM_FORMALIZATION.md`

**Notation context (per `theory/README_DEFINITIONS.md` §87):** In *this* document, $R$ denotes the
orthogonal Procrustes factor (not the SCBI representation update), $r$ denotes matrix rank
(not a vector), and $d$ the ambient dimension. All other SCBI symbols follow the definitions doc.

**Labels** follow `AGENTS.md` §5. The Lemma below is proved and rated **[THEOREM]**; the Proposition is
proved *under an explicitly labeled* **[ASSUMPTION]** (random-completion model) and is therefore rated
**[PROPOSITION]**, not [THEOREM]. Steps that are not airtight are flagged in §6.

---

## 1. The operator as implemented [FACT]

From `experiments/scripts/run_exp066_pythia410m_replication.py` (identical structure in the EXP065 script):

```python
U, S, Vh = torch.linalg.svd(E_k.T @ E_0_2hop)  # E_*: [2, d] stacks of unembedding rows
R_k = U @ Vh                                   # [d, d], claimed "rotation"
v_aligned = R_k @ v_hat_by_vocab["V1_Anglo"]   # v_hat: hidden-state contrast direction
```

- $E_k, E_0 \in \mathbb{R}^{2 \times d}$: rows are **unembedding** vectors
  (`model.embed_out.weight` rows for entity tokens). $d = 768$ (EXP065) / $1024$ (EXP066).
- $\hat{v} \in \mathbb{R}^d$: normalized mean contrast direction
  $\Delta h = h_{l^*}(\text{rel}) - h_{l^*}(\text{neu})$, a **residual-stream** direction at layer $l^*$.
- The intent (code comment): "$R \cdot E_0^T = E_k^T$", i.e. $R$ solves the orthogonal Procrustes problem
  $\min_{R \in O(d)} \|R A - B\|_F$ with $A = E_0^T$, $B = E_k^T$ ($d \times 2$), then $R$ is applied to $\hat{v}$.

**[FACT]:** $M := E_k^T E_0 \in \mathbb{R}^{d \times d}$ satisfies $\operatorname{rank}(M) \le 2$ exactly
(it is a product of a $d \times 2$ and a $2 \times d$ matrix).

---

## 2. Lemma (rank-deficient Procrustes non-uniqueness) [THEOREM]

**Lemma.** Let $M \in \mathbb{R}^{d \times d}$ with $\operatorname{rank}(M) = r < d$ and thin SVD
$M = U_r \Sigma_r V_r^T$. The minimizers of $\|RX - Y\|_F$ over $R \in O(d)$, where $M = YX^T$, are
*exactly* the matrices

$$R = U_r V_r^T + U_0 Q_0 V_0^T, \qquad Q_0 \in O(d-r)\ \text{arbitrary},$$

where $U = [U_r, U_0]$, $V = [V_r, V_0]$ complete to full SVDs. In particular the minimizer is
**not unique**: on the $(d-r)$-dimensional orthogonal complement of the fit subspace, $R$ is
implementation-defined, not task-defined. The code's choice $R = UV^T$ corresponds to $Q_0 = I$.

*Proof.* $\|RX - Y\|_F^2 = \|X\|_F^2 + \|Y\|_F^2 - 2\,\mathrm{tr}(R^T YX^T) = C - 2\,\mathrm{tr}(R^T M)$,
so minimizing is equivalent to maximizing $\mathrm{tr}(R^T M)$.
With $M = U\Sigma V^T$:
$$\mathrm{tr}(R^T M) = \mathrm{tr}(R^T U\Sigma V^T) = \mathrm{tr}(V^T R^T U\,\Sigma) =: \mathrm{tr}(Z\Sigma),$$
where $Z = V^T R^T U \in O(d)$. Now $\mathrm{tr}(Z\Sigma) = \sum_{i=1}^d \sigma_i z_{ii} \le \sum_i \sigma_i$
since $|z_{ii}| \le 1$ for orthogonal $Z$. With $\sigma_1 \ge \cdots \ge \sigma_r > 0 = \sigma_{r+1} =
\cdots = \sigma_d$, the maximum $\sum_i \sigma_i$ is attained iff $z_{ii} = 1$ for all $i \le r$.
An orthogonal $Z$ with $z_{ii} = 1$ for $i \le r$ must satisfy: row $i$ has unit norm with $i$-th entry
$1$, hence all other entries of row $i$ are $0$; by orthogonality the same holds for column $i$.
Thus $Z = \operatorname{diag}(I_r, Z_0)$ with $Z_0 \in O(d-r)$. Then
$R^T = VZU^T$, i.e. $R = UZ^T V^T = U_r V_r^T + U_0 Z_0^T V_0^T$.
Every $Q_0 = Z_0^T \in O(d-r)$ attains the maximum, and no other $R$ does. ∎

**[INTERPRETATION]:** For EXP065/066, $r \le 2$ while $d \in \{768, 1024\}$. The "rotation" is
determined on at most a 2-dimensional subspace; on the remaining $\ge 766$ dimensions it is an
arbitrary choice of the SVD implementation (LAPACK's null-space completion), carrying zero
task information.

---

## 3. Proposition (scramble bound) [PROPOSITION]

**[ASSUMPTION] A-comp (random-completion model):** Model the arbitrary completion $Q_0$ as
Haar-distributed on $O(d-r)$. (Justification: the Lemma shows $Q_0$ is unconstrained by the task;
any specific choice, including the code's $Q_0 = I$, is arbitrary *with respect to the alignment
objective*. The expectation below quantifies behavior over this arbitrary degree of freedom.)

**Proposition.** Let $S = \mathrm{col}(V_r)$ (dim $r$, the "fit subspace"), $T = \mathrm{col}(U_r)$,
and $P_S, P_{S^\perp}, P_{T^\perp}$ the orthogonal projectors. For fixed unit vectors $v, w \in
\mathbb{R}^d$, under A-comp:

$$\mathbb{E}_{Q_0}\big[(w^T R v)^2\big] \;=\; \underbrace{(w^T U_r V_r^T v)^2}_{\text{constrained part}}
\;+\; \underbrace{\frac{\|P_{S^\perp} v\|^2 \,\|P_{T^\perp} w\|^2}{\,d - r\,}}_{\text{arbitrary part}}.$$

*Proof.* Write $w^T R v = a + b^T Q_0 c$ with scalar $a = w^T U_r V_r^T v$,
$b = U_0^T w \in \mathbb{R}^{d-r}$, $c = V_0^T v \in \mathbb{R}^{d-r}$.
Haar symmetry ($Q_0 \stackrel{d}{=} -Q_0$) gives $\mathbb{E}[b^T Q_0 c] = 0$.
For the second moment: $\mathbb{E}[Q_0 c c^T Q_0^T] = \frac{\|c\|^2}{d-r} I_{d-r}$. Write
$c = \|c\|\,e$ with $e$ a unit vector; the claim reduces to
$\mathbb{E}[(Q_0e)(Q_0e)^T] = I_{d-r}/(d-r)$. Since $Q_0$ is Haar on $O(d-r)$, the random
vector $Q_0e$ is uniform on the unit sphere $S^{d-r-1}$ (the pushforward of Haar measure
under $Q_0 \mapsto Q_0e$ is the rotation-invariant probability measure on the sphere). For
$u$ uniform on the sphere, $\mathbb{E}[uu^T]$ is invariant under conjugation by any fixed
orthogonal matrix, hence has zero off-diagonals (sign-flip $u_i \mapsto -u_i$) and equal
diagonal entries (coordinate permutations); with
$\mathrm{tr}\,\mathbb{E}[uu^T] = \mathbb{E}\|u\|^2 = 1$ the common diagonal value is
$1/(d-r)$. The final formula is unchanged — only the justification is corrected (the earlier
version invoked Schur's lemma where the argument actually needed is sphere-uniformity). Thus
$\mathbb{E}[(b^T Q_0 c)^2] = b^T \big(\frac{\|c\|^2}{d-r} I\big) b = \|b\|^2\|c\|^2/(d-r)$.
Expanding $\mathbb{E}[(a + b^TQ_0c)^2] = a^2 + 2a\cdot 0 + \|b\|^2\|c\|^2/(d-r)$ and noting
$\|b\| = \|P_{T^\perp} w\|$, $\|c\| = \|P_{S^\perp} v\|$ completes the proof. ∎

**Corollary (quantitative scramble).** Since $|a| \le \|P_S v\|$ (Cauchy–Schwarz:
$|w^T U_r V_r^T v| \le \|V_r^T v\|\cdot\|U_r^T w\| \le \|P_S v\|$), deterministically in $v, w$:

$$\mathbb{E}_{Q_0}\big[(w^T R v)^2\big] \;\le\; \|P_S v\|^2 + \frac{1}{d-r}.$$

For *typical* $v, w$ (fixed $r$-dim subspaces, $\mathbb{E}\|P_S v\|^2 = r/d$ by symmetry):

$$\mathbb{E}|\cos(Rv, w)| \;\le\; \sqrt{\mathbb{E}[(w^T Rv)^2]} \;\lesssim\; \sqrt{\frac{r+1}{d}}
\qquad\text{(Jensen)}.$$

**Numerics for EXP065/066** ($r = 2$):
| $d$ | scramble bound $\sqrt{3/d}$ | observed $\cos(R\hat{v}_1, \hat{v}_k)$ (mean) |
|---|---|---|
| 768 (EXP065) | 0.0625 | $+0.0032$ |
| 1024 (EXP066) | 0.0541 | $-0.0118$ |

> **Table caveat (prominent):** the bound column upper-bounds **$\mathbb{E}|\cos|$** —
> expectation of the *absolute* cosine — under A-comp and the *illustrative* genericity
> assumption (T-1, below); the observed column is the *signed* mean cosine. Values inside
> the band show consistency with the scramble model, not confirmation of it (M3.3).

> **[CORRECTIONS PASS 2026-09-23 — T-1 status]:** The bound column above is **illustrative scale;
> genericity unmeasured**. Computing $\|P_S \hat{v}_k\|$ from the primary artifacts was attempted:
> the result JSONs (`exp065_results.json`, `exp066_replication_results.json`) store only scalar
> summaries (per-vocabulary raw/aligned cosines), not the anchor stacks $E_k$ or the contrast
> directions $\hat{v}_k$; no `.pt`/`.npy` vector dumps exist in the run directories; the run scripts
> do not persist vectors. Recomputation requires model execution, which is unavailable in this
> environment. The *deterministic* bound $\|P_S v\|^2 + 1/(d-r)$ holds regardless; the $\sqrt{3/d}$
> numerics assume the genericity $\mathbb{E}\|P_S \hat{v}\|^2 = r/d$ and remain illustrative until a
> future run archives the raw vectors. (Law #13 implication: future runs must archive intervention
> vectors in run artifacts.)

**[INTERPRETATION]:** Both observed values lie inside the predicted scramble band. The Stage A
"failure" is the expected output of the operator: a rotation fit on 2 anchor vectors cannot but
scramble a generic full-rank direction. For the rotation to *preserve* the observed raw cosine of
$\approx 0.7$, one would need $\|P_S \hat{v}\| \gtrsim 0.7$ — i.e., the relational contrast direction
concentrated in the 2D span of two unembedding token vectors — which was never established and is
not credible without evidence. The "generic full-rank direction" reading is conditional on the
unmeasured genericity assumption; see the T-1 caveat above.

---

## 4. The unstated cross-space assumption [ASSUMPTION] → evidence against

**[ASSUMPTION] A-cross (reconstructed; was unstated in the original work):**
Let $R^* = \arg\min_{R \in O(d)} \|R A_{\mathrm{emb}} - B_{\mathrm{emb}}\|_F$ with
$A_{\mathrm{emb}}, B_{\mathrm{emb}}$ unembedding-row anchors for vocabularies $V_1, V_k$, and let
$\hat{v}_1, \hat{v}_k$ be residual-stream relational contrast directions. A-cross asserts
$\cos(R^* \hat{v}_1, \hat{v}_k) > \cos(\hat{v}_1, \hat{v}_k)$ — i.e., a rotation aligning
*token-identity* geometry in unembedding space transfers to *relational-reasoning* directions in the
residual stream.

**[FACT]:** A-cross was never validated, pre-registered, or tested independently of the confounded
Stage A procedure.

**[OBSERVATION]:** Stage A of EXP065/066 ($\Delta\cos \approx -0.72 / -0.70$) is inconsistent with
A-cross under the rank-2 operationalization used. A-cross is therefore **unsupported and, in this
operationalization, contradicted**; the general question "does *some* rotation transfer" remains
**[OPEN]** and is the subject of **[HYPOTHESIS]** H1 (`theory/BOUNDARY_CLAIM_FORMALIZATION.md` §3.3).

Note the two defects are independent: even with full-rank anchors, A-cross would still require
validation; even in the same space, a rank-2 fit would still scramble. EXP067 is designed to fix
*both* (same-space fit + full-rank constraints).

**Charitable rescue of A-cross (T-2).** Stated uncharitably, A-cross is a strawman — no serious
reader would defend fitting on token-identity geometry to rotate relational directions *once the
assumption is stated plainly*. Its salvageable core is a uniformity claim: that a
vocabulary-renaming rotation estimated from *some* same-space correspondences acts uniformly on
*relational* directions. That core is exactly what EXP067 tests empirically: the rotation is fit
on role-matched entity-frame anchors (same space, full rank), and the Stage A gate evaluates the
gain $g_h$ on held-out *relational* directions $\tilde{v}_k^{(h)}$ — the gate is the rescue's
empirical test, named [ASSUMPTION] A-uniform in the protocol. This document defeats the assumption
as originally operationalized; the rescue is the live hypothesis.

---

## 5. Consequence for the boundary claim

The Lemma + Proposition show the EXP065/066 "aligned" condition injected a scrambled basis.
Its $\Delta M = 0$ therefore cannot bear on whether *alignment* enables causal transfer.
The valid boundary evidence is the static-basis result (O1+O3 of the formalization doc).
Full reframing: `theory/BOUNDARY_CLAIM_FORMALIZATION.md` §3.

---

## 6. Adversarial self-review (attack surface on this document)

1. **A-comp is a modeling choice, not a fact — read this first.** `torch.linalg.svd` is
   deterministic on fixed input/platform, so the observed cosine is *one draw from an unknown
   deterministic completion rule*, not a sample from a distribution. The Proposition's expectation
   is therefore taken over the **design space of admissible completions**, not over a sampling
   distribution governing the observed run — it quantifies how much of the output is
   task-constrained versus implementation-chosen. What is **[FACT]**-level, and what makes the
   observed draw *task-arbitrary*, is the **Lemma**, not the Proposition: the completion $Q_0$
   is unconstrained by the alignment objective, so the procedure's output on the
   $(d-r)$-dimensional complement is implementation-defined regardless of which deterministic
   rule produced it. Flagged, not hidden.
2. **$\hat{v}$ is fixed, not random.** The "typical $v$" numerics assume genericity of the
   empirical direction w.r.t. the anchor subspace. The *deterministic* bound
   $\|P_S v\|^2 + 1/(d-r)$ holds regardless; the numerics only illustrate scale.
3. **Sign of observed values.** The model predicts $|\cos| \lesssim 0.06$, i.e. scramble to
   *near-zero*, not systematic anti-alignment — consistent with observations ($+0.0032$, $-0.0118$;
   per-vocab values all within $\pm 0.07$).
4. **Repeated singular values do NOT break fit-part uniqueness (corrected 2026-09-23; the
   original claim was false).** The $r$-dimensional fit part $U_rV_r^T$ is unique regardless of
   singular-value multiplicities: the Lemma's proof never uses distinctness of the nonzero
   $\sigma_i$, and $U_rV_r^T$ is invariant under simultaneous within-eigenspace rotations
   $(U_r, V_r) \to (U_rW, V_rW)$, where $W$ is orthogonal and block-diagonal on the
   repeated-$\sigma$ eigenspaces, since $U_rWW^TV_r^T = U_rV_r^T$. All non-uniqueness lives in
   the orthogonal-complement completion $Q_0$. EXP067's spectral-gap check is therefore
   reframed: it is a **rank-boundary gap check** ($\tilde{\sigma}_{64}$ vs $\tilde{\sigma}_1$,
   guarding the *rank estimate* $r = 64$ against near-degenerate $\tilde{M}_h$), not a guard
   on fit-part uniqueness. Verified 2026-09-23: EXP067's spec (§3.3, "near-degenerate →
   abort") and runner docstring make no uniqueness claim about the gap check, so no change
   was needed there — the check itself is unchanged; only its stated purpose is corrected.
5. **What this proof does NOT show:** it does not prove alignment is impossible in principle, nor
   that the raw similarity O1 ($\approx 0.7$) is task-meaningful (see Q2 in the formalization doc).

**Rating:** Lemma = **[THEOREM]** (airtight). Proposition = **[PROPOSITION]** (rigorous derivation,
conditional on the explicitly labeled A-comp). Overall document: *rigorous proof sketch* — promote
nothing to [THEOREM] beyond the Lemma.
