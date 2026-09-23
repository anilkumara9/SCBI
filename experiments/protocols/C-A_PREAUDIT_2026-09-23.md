# C-A Weight-Only Leakage Pre-Audit — (c).2 Gate Values

**Status: PRE-AUDIT ATTACHMENT — computed, not signed.** For the Law #14
reviewer's pre-signing checklist (§12, items 2 and 5). Does not modify the draft
spec (`C-A_DONOR_TRANSFER_PREREG_SPEC.md`, DRAFT LOG-150) or any signed
protocol/artifact.

**Date:** 2026-09-23 · **Dispatch:** LOG-160 · **Role:** weight-only pre-audit specialist
**Machine-readable twin:** `C-A_PREAUDIT_2026-09-23.json` (same directory; every
value below is duplicated there).
**Compute:** CPU only, **$0 GPU, zero forward passes** — pure weight arithmetic on
$W_U$. Every number in this document is **[FACT — computed]**.

## 0. Method and guards

- **Model:** local HF snapshot of pythia-410m,
  `/home/hatch/.cache/huggingface/hub/models--EleutherAI--pythia-410m/snapshots/9879c9b5f8bea9051dcb0e68dff21493d67e9d4f`,
  loaded read-only exactly as G1 (LOG-134): transformers 5.17.0
  `AutoModelForCausalLM`, `torch_dtype=torch.float32`, `local_files_only`,
  `trust_remote_code=False`, `model.eval()`. No forward pass was executed at any point.
- **SHA-256 guard** (`get_hash` verbatim from `run_exp077.py` ll. 166–174):
  pre = `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed`
  [FACT — computed]; post = `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed`
  [FACT — computed]; archived (G1) = `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed`.
  **pre == post == archived ⇒ Δθ = 0** [FACT — computed].
- **Replication note (transparency):** transformers 5.17.0 renames the checkpoint
  file's `embed_out.weight` to `lm_head.weight` in `state_dict()` (returned by
  `model.get_output_embeddings()`); values are byte-identical to the file tensor
  (verified). The 24 uint8 `attention.bias`, 24 `attention.masked_bias`, and 24
  `rotary_emb.inv_freq` file tensors are ignored-on-load
  (`_keys_to_ignore_on_load_unexpected` / `persistent=False`) → 292 hashed keys.
  A naive hash over raw file keys does **not** reproduce the archived hash; the
  G1-venv replication above does, exactly.
- **$W_U$:** `model.get_output_embeddings().weight`, shape (50304, 1024), float32
  [FACT — computed].
- **F2 guard** (verbatim convention): all 35 entities (25 support + 10 test) encode
  as exactly one token under `" "+e` — **PASSED** [FACT — computed].
- **Donor list:** the spec's 20-donor verbatim table was cross-checked against the
  pinned generative formula (5 vocabs × triples $i\in\{0,1,2,3\}$, $t_d=A$, $f_d=C$)
  — **identical** [FACT — computed].
- **Test items:** the 60 items were rebuilt by the verbatim `run_exp077.py` §3
  construction; all 60 prompt strings verified **identical** to EXP066's executed
  pythia-410m instance evaluations (`exp066_instance_evaluations.json`, ids
  `pythia410m_*` ↔ `exp077_*` by suffix) [FACT — computed].

## 1. Degeneracy gate — (c).2

Pinned formula: $\hat{b}_D = \mathrm{normalize}(\sum_{d\in D}(W_U[t_d]-W_U[f_d]))$,
$|D|=20$.

| Quantity | Value |
|---|---|
| $g(D) = \\|\sum_d(W_U[t_d]-W_U[f_d])\\| / \sqrt{20}$ | **1.061783** [FACT — computed] |
| Floor | 0.25 |
| **Ruling** | **PASS** — $1.061783 \ge 0.25$ (4.25× the floor) |

Independently recomputed via the per-entity $(n_t-n_f)$ identity — identical to 6
decimals [FACT — computed]. $\|\hat{b}_D\| = 1$ by construction. The bank is far
from the degeneracy trap: no redesign required.

## 2. Weight-only similarity audit — $s_t(j), s_f(j)$

$s_t(j)=\cos(\hat{b}_D, W_U[t_j])$, $s_f(j)=\cos(\hat{b}_D, W_U[f_j])$, $j=1..60$.

| Feature | min | median | max | mean | std |
|---|---|---|---|---|---|
| $s_t$ | **-0.091793** | **-0.035416** | **0.081702** | -0.038264 | 0.032482 |
| $s_f$ | **-0.039005** | **0.010345** | **0.081702** | -0.003907 | 0.028335 |

(all [FACT — computed]). Count with $s_t(j) > s_f(j)$: **9 / 60** [FACT — computed].

**Structural finding (load-bearing for §6/T4 interpretation):** $s_t(j)$ depends
only on the item's *target entity*, so it takes exactly **6 distinct values**
across the 60 items [FACT — computed]:

| Target entity | $s_t$ | Items |
|---|---|---|
| Venus | -0.091793 | 7 |
| Mars | -0.048545 | 21 |
| Iron | -0.035416 | 21 |
| Gold | -0.015161 | 7 |
| Silver | 0.026304 | 2 |
| Jupiter | 0.081702 | 2 |

(all [FACT — computed]). The donor centroid is near-orthogonal to every test
target's unembedding row (all $|\cos| < 0.1$): the token-similarity channel the
leakage audit measures is **weak in absolute terms**. Full per-item table
(id, $t_j$, $f_j$, $s_t$, $s_f$) is in the JSON twin.

## 3. Permutation null — (c).2

Pinned procedure: 200 random donor banks, $|D|=20$, drawn without replacement
*within* bank from the 150-item same-template ("outranks") support pool
(15 triples + 15 quads per vocab × 5 vocabs; $(t,f)=(A,C)$ triples, $(A,D)$ quads),
`SEED_PERMNULL=20261123` (`numpy.random.default_rng`, sequential
`rng.choice(150, 20, replace=False)`). Null statistic: $\mathrm{mean}_j\, s_t(j)$
per bank. Descriptive audit, not a decision endpoint.

| Quantity | Value |
|---|---|
| Null mean ± sd | **-0.034053 ± 0.013496** [FACT — computed] |
| Null p5 / p50 / p95 | **-0.057162 / -0.033560 / -0.012494** [FACT — computed] |
| Observed C3 bank $\mathrm{mean}_j s_t(j)$ | **-0.038264** [FACT — computed] |
| **Observed bank's percentile of the 200-bank null** | **38.0** [FACT — computed] |
| $Q_{\mathrm{null}}(p_{\mathrm{obs}})$ | -0.038087 [FACT — computed] |
| Count of items with $s_t(j) > Q_{\mathrm{null}}(p_{\mathrm{obs}})$ | **32 / 60** [FACT — computed] |

The C3 bank's aggregate target-similarity sits at the **38th percentile** of the
random-donor null — squarely typical, not an outlier. (Descriptive; the spec
registers no decision on this number.)

## 4. Stratum feasibility gate — (c).2 / §4.4

Pinned rule: median split on $s_t^{C3}(j)$ over the 60 items; low $=\{s_t \le
\mathrm{median}\}$ (ties → low).

| Quantity | Value |
|---|---|
| Median $s_t$ | **-0.035416** (= Iron's $s_t$ exactly) [FACT — computed] |
| Low stratum size | **49** [FACT — computed] |
| High stratum size | **11** [FACT — computed] |
| C1-wrong overall | **26 / 60** (EXP066 baseline 34/60 = 56.67%) [FACT — computed] |
| **Low-stratum C1-wrong (headroom)** | **23** [FACT — computed] |
| **Ruling** | **PASS** — low stratum non-empty AND $23 \ge 5$ headroom items |

Headroom source: EXP066's executed pythia-410m baseline
(`exp066_instance_evaluations.json`, `base_correct`) on the identical 60 items
(all 60 prompts verified identical, §0) with the identical strict-$>$ decision
rule — a prior artifact, **no new forward pass**. The 23 headroom item ids are
listed in the JSON twin (`stratum_feasibility.low_stratum_headroom_items`).

**Reviewer flag (not a gate failure):** because $s_t$ takes only 6 distinct values
(§2), the pinned median split is effectively an **entity-group split** — low =
{Mars, Venus, Iron} (49 items), high = {Gold, Silver, Jupiter} (11 items) — not
the ~30/30 per-item gradient the spec's "~30/30" aside envisioned. The rule as
pinned was applied verbatim (ties → low); the T4 low-stratum reading should be
interpreted with this coarseness in mind. The feasibility gate itself is
satisfied with large margin (23 vs the required 5).

**Why EXP077_cone_vs_line records were NOT used:** their per-(ent,typ)
distribution is uniform (6 per cell), contradicting the pinned construction's
skewed target-entity coverage (e.g. 21 Mars-planet items) — a different executed
item set. Using them item-by-item for headroom would be fabrication (Law #2).
EXP066's evaluations are on the pinned items (prompt-verified) and are the valid
prior artifact.

## 5. Donor $(t_d,f_d)$ histogram — L4 auditability

Over the **25-entity support pool** (5 vocabs × 5 entities), computed from the
pinned donor list [FACT — computed]:

| Vocab | $e_0$ $(n_t,n_f)$ | $e_1$ | $e_2$ | $e_3$ | $e_4$ |
|---|---|---|---|---|---|
| V1_Anglo (Alice, Bob, Charlie, David, Emma) | (2,0) | (1,0) | (1,1) | (0,1) | (0,2) |
| V2_Biblical (Aaron, Joel, Gideon, Ruth, Abel) | (2,0) | (1,0) | (1,1) | (0,1) | (0,2) |
| V3_Greek (Ajax, Jason, Apollo, Paris, Atlas) | (2,0) | (1,0) | (1,1) | (0,1) | (0,2) |
| V4_Roman (Marcus, Julius, Augustus, Felix, Diana) | (2,0) | (1,0) | (1,1) | (0,1) | (0,2) |
| V5_Modern (Liam, Noah, Eli, Maya, Finn) | (2,0) | (1,0) | (1,1) | (0,1) | (0,2) |

i.e. $n_t-n_f$: $e_0$:+2, $e_1$:+1, $e_2$:0, $e_3$:-1, $e_4$:-2 per vocab — exactly
the spec §3.1 L4 histogram [FACT — computed; claim **confirmed**].

**"10-entity pool" claim — verified:** a 10-entity donor histogram cannot exist for
entity-disjoint donors. The test answer pool is exactly the 10 entities
{Mars, Venus, Jupiter, Saturn, Mercury, Iron, Gold, Silver, Bronze, Steel}; the
donor pool is the 25 support entities; donor ∩ test = **∅** (verified)
[FACT — computed]. Donor entities ⊆ support pool: verified. The 25-entity
support-pool reporting in the spec is the correct framing.

**Premise-disjointness build assert (analog):** the 20 donor prompt strings vs the
60 test prompt strings — overlap = **∅** [FACT — computed].

## 6. Rulings summary

| Gate (spec §4) | Result |
|---|---|
| Degeneracy $g(D) \ge 0.25$ | **PASS** — 1.061783 |
| Stratum feasibility (non-empty low + ≥5 headroom) | **PASS** — 49 low, 23 headroom |
| DO-NOT-RUN trigger (empty or headroom-free low stratum) | **Not triggered** |
| Permutation-null percentile (descriptive) | 38.0 — typical, no outlier |
| Donor histogram vs spec L4 | Confirmed; 25-entity framing verified |
| Δθ=0 pre/post | PASS — ec276abe3902fab0… tri-match |

## 7. Notes for the Law #14 reviewer

1. The audit is complete for the C3 bank. C4′/C5 banks are not yet selected
   (C4′ matching is a separate pre-GPU step per §5.1); their $g(D)$ values attach
   when selected — the spec requires them before signature (§12 item 2).
2. The stratum coarseness flag (§4) is the one substantive interpretive caveat;
   it does not fail any gate.
3. The absolute similarity magnitudes (§2) are small ($|s_t|<0.1$ everywhere):
   under the spec's bypass model, the C3 bridge's per-item logit steering via
   the donor centroid is a weak channel — consistent with H_leak being the null,
   and with the permutation null showing the bank is unremarkable.
4. Environment: `/home/hatch/workspace/.venv_smoke` (torch 2.14.0+cpu,
   transformers 5.17.0, numpy 2.5.3) — the G1-venv; audit script at
   `/tmp/ca_pre_audit.py` (ephemeral; procedure fully described in §0).

---

# Part 2 — C4′/C5 banks (LOG-174)

**Status: computed, not signed.** Extends Part 1 (LOG-160) above; extends, does
not redo. Does not modify the draft spec (`C-A_DONOR_TRANSFER_PREREG_SPEC.md`,
DRAFT LOG-150) or any signed protocol/artifact. Machine-readable values are in
the JSON twin's `part2_log174` key.

**Dispatch:** LOG-174 · **Role:** C-A pre-audit completion specialist ·
**Compute:** CPU only, **$0 GPU, zero forward passes** — pure weight arithmetic
on $W_U$. Every number in this section is **[FACT — computed]**.

**Method and guards (this session):** same model snapshot, read-only,
`local_files_only`, `torch.float32`, unembedding rows only. SHA-256 pre =
`ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed` [FACT —
computed]; post identical; archived (G1) identical ⇒ **Δθ = 0** [FACT —
computed]. C3 centroid rebuilt from the verbatim 20-donor table as a sanity
check: per-item $s_t, s_f$ match the JSON twin to max|Δ| = 1.09e-08 / 6.61e-09;
$g(C3)$ recomputed = 1.061783 (identical to 6 decimals) [FACT — computed].
Environment: `/home/hatch/workspace/.venv_smoke` (torch 2.14.0+cpu,
transformers 5.17.0, numpy 2.5.3); script `/tmp/ca_pre_audit_part2.py`
(ephemeral; procedure fully described here).

## 8. C4′ bank selection — pinned greedy similarity-matching (§5.1)

**Candidate pool (pinned, built verbatim):** 150 "is next to" items — for each
of the 5 support vocabularies, the 15 `TRIPLES_INDICES` triples and 15
`QUADS_INDICES` quads with $(t_c,f_c)=(A,C)$ for triples, $(A,D)$ for quads;
ids `ca_C4cand_{vk}_triple_{i}` / `ca_C4cand_{vk}_quad_{i}` [FACT — constructed].
Structural note: `TRIPLES_INDICES`/`QUADS_INDICES` repeat tuples (indices 10–14
mirror 0–4), so the 150 items carry only **30 distinct $(t,f)$ pairs** (120
duplicate-content items) [FACT — computed].

**Rule applied verbatim:** $B_0=\emptyset$; at each step choose the candidate
minimizing
$D(B)=\tfrac{1}{60}\sum_j(|s_t^{B}(j)-s_t^{C3}(j)|+|s_f^{B}(j)-s_f^{C3}(j)|)$;
ties → lowest candidate index — deterministic, **no RNG used** (per spec "no
seed needed"); stop when $D(B_k)\le\delta=0.05$ or $|B_k|=30$ [DEFINITION —
pinned procedure].

**Step 1:** argmin over all 150 singletons = `ca_C4cand_V5_Modern_triple_1`
($(t,f)=$(Noah, Maya), "is next to" triple), $D=0.046564\le0.05$ ⇒ **stop at
$|B|=1$** [FACT — computed]. Independently reproduced via vectorized argmin
(identical index, $D=0.046564062$) [FACT — computed]. 7 of 150 singletons
already satisfied $D\le0.05$; a duplicate-content twin of the winner exists in
the pool — the lowest-index tie-break decided [FACT — computed].

**Branch fired:** **STOP-D≤δ (matching succeeded).** The §5.1 demotion
fallback **did NOT fire** — T3 is not demoted; no exploratory re-labeling
[FACT — procedure outcome].

**Achieved-match report (per §5.1, attached):**

| Quantity | Value |
|---|---|
| Final $\|B\|$ | **1** |
| Achieved $D$ | **0.046564** (δ = 0.05) |
| Selected donor id | `ca_C4cand_V5_Modern_triple_1` (Noah − Maya) |
| $g(B)$ | **0.860981** ≥ 0.25 — **PASS** (3.44× floor) |
| per-item $\|s_t^B - s_t^{C3}\|$ min / med / max / mean | 0.006682 / 0.026718 / 0.043542 / 0.024645 |
| per-item $\|s_f^B - s_f^{C3}\|$ min / med / max / mean | 0.005491 / 0.021975 / 0.069394 / 0.021919 |

(all [FACT — computed]).

**Reviewer flag (not a gate failure):** the pinned rule licenses a **singleton
"bank"** — the spec pins no minimum bank size. The Law #14 reviewer must rule
whether a 1-donor C4′ operationalizes the intended similarity-matched
different-relation contrast for T3. No re-registration is made here (Law #4).

## 9. C5 permuted-label bank (§5.2)

**Pinned procedure applied:** permutation of $\{0..19\}$ from
`numpy.random.default_rng(seed)`; seed 20261067 → fixed point present; seed
20261068 → fixed point present; seed **20261069** → fixed-point-free
permutation $\pi$ (2 redraws, deterministic rule) [FACT — computed]. Final
permutation and the 20 $(t_{\pi(i)}, f_i)$ pairs are in the JSON twin
(`part2_log174.c5_bank`) [FACT — computed].

**Constraint verification:** target multiset and foil multiset are preserved
exactly; per-entity $(n_t-n_f)$ identical to C3's for all 25 support entities —
**PASS** [FACT — computed].

**Degeneracy:** $g(C5)$ = **1.061783** ≥ 0.25 — **PASS** (4.25× floor; identical
to C3's, as the multiset-preserved sum requires) [FACT — computed].

**Load-bearing finding:** under the pinned §4.1 identity
$\hat{b}_D=\mathrm{normalize}(\sum_y W_U[y]\,(n_t(y)-n_f(y)))$, the identical
$(n_t-n_f)$ prior forces $\hat{b}_{C5} \equiv \hat{b}_{C3}$ exactly:
$\cos(\hat{b}_{C5},\hat{b}_{C3}) = 1.000000000000000$,
$\|S_{C5}-S_{C3}\| = 0.000\mathrm{e}{+}00$ [FACT — computed]. The permuted
pairing is invisible to the pinned centroid construction — **C5's intervention
vector is geometrically identical to C3's.**

**Consequence for the reviewer (arithmetic, not a verdict):** T1 (C3 rescues)
and T5 (C5 does not rescue) are mutually exclusive under the pinned
construction; the §8 refutation clause "paired C3-vs-C5 $p\ge0.05$ with C3 vs
C1 significant → **Refuted**" would fire *by construction* whenever C3 rescues
(a paired comparison of an arm with itself yields $b=c=0$, $p=1.0$); outcome
(c)'s "C5 rescues vs C1 ($p<0.05$)" is guaranteed iff C3 rescues. The C5 control
**as pinned cannot discriminate relational content from prior/similarity
steering.** No redesign is proposed here (Law #4); the Law #14 reviewer rules.

## 10. Degeneracy rulings — all three banks

| Bank | $g(D)$ | Floor | Ruling |
|---|---|---|---|
| C3 (Part 1, LOG-160) | 1.061783 | 0.25 | **PASS** |
| C4′ | 0.860981 | 0.25 | **PASS** |
| C5 | 1.061783 | 0.25 | **PASS** |

(all [FACT — computed]).

## 11. Stratum analog under the C4′ centroid

Median split on $s_t^{C4'}(j)$; low $=\{s_t \le \mathrm{median}\}$
(ties → low). C1-wrong from EXP066 `base_correct` prior artifact (ids mapped by
suffix; same source as Part 1 §4) — C1-wrong total **26/60** [FACT — computed].

| Quantity | Value |
|---|---|
| Median $s_t^{C4'}$ | **-0.008480** (= Gold's value; ties → low) |
| Low stratum size | **35** [FACT — computed] |
| High stratum size | **25** [FACT — computed] |
| Low-stratum C1-wrong (headroom) | **16** (≥5 required — analog **PASS**) |
| High-stratum C1-wrong | **10** |

$s_t^{C4'}$ per target entity: Mars −0.005002408, Venus −0.053171409, Jupiter
0.102744769, Iron −0.028734122, Gold −0.008479731, Silver −0.006090125 —
**6 distinct values** (one per target entity) [FACT — computed]. Low entities:
Venus (7), Iron (21), Gold (7); high entities: Mars (21), Jupiter (2), Silver
(2) [FACT — computed].

Note: the binding §4.4 feasibility gate is pinned to the **C3** stratum (Part 1:
**PASS**, 49 low / 23 headroom). The above is the C4′-centroid analog supplied
for the reviewer's T3/T4 reading.

## 12. T4-readability analysis (LOG-160's open item)

**(a) C3's pinned stratum.** $s_t$ takes exactly 6 distinct values (one per
target entity; all $|\cos|<0.1$), so the pinned median split is necessarily an
**entity-group split**: low = {Mars (21), Venus (7), Iron (21)} = **49** items;
high = {Gold (7), Silver (2), Jupiter (2)} = **11** items — not ~30/30. Headroom:
23 low / 3 high (of 26 C1-wrong) [all FACT — computed].

**Honest limitation statement:** T4 ("low-similarity stratum fires") tests
rescue on low-similarity *target entities* with exactly **3 independent
entity-level observations** in the low stratum; the 49 items share 3 distinct
$s_t$ values, so the stratifying feature has zero within-entity variation. A
T4 license can at most mean transfer across 3 low-similarity target entities —
it is not a 49-observation per-item gradient test, and the spec's "~30/30"
aside does not obtain. [INTERPRETATION of FACTs]

**(b) The C4′ bank does not change this picture.** $s_t^{C4'}$ likewise takes 6
distinct values (one per target entity — structural: $s_t(j)$ depends only on
the item's target entity under *any* bank centroid), so any median split is
again an entity-group split [FACT — computed]. The grouping differs —
low = {Venus, Iron, Gold} = 35; high = {Mars, Jupiter, Silver} = 25 (§11) —
which matters for the arm-specific $(s_t,s_f)$ features in §7's item-level
model, but the coarseness is unchanged [FACT — computed]. The Law #14 reviewer
rules on whether a 3-entity low stratum supports T4's licensed reading; **no
re-registration is made here** (Law #4).

## 13. Reviewer checklist delta (§12 items 2, 3, 4, 5)

- **Item 2 [CENTROID]:** $g(D)$ now computed for all three banks — C3 1.061783
  **PASS**, C4′ 0.860981 **PASS**, C5 1.061783 **PASS**. Complete.
- **Item 3 [C4′]:** achieved-match report attached ($D=0.046564\le0.05$,
  branch STOP-D≤δ, singleton bank, §8). The demotion fallback did not fire —
  T3 remains deciding per the spec, subject to the reviewer's ruling on the
  singleton-bank flag (§8).
- **Item 4 [C5]:** construction verified against all pinned constraints; the
  centroid-identity consequence (§9) is flagged for the reviewer — the T1/T5
  conjunct pair and the §8 refutation clause cannot operate as written under
  the pinned §4.1 formula.
- **Item 5 [STRATA]:** C3 feasibility already **PASS** (Part 1); C4′-centroid
  analog computed (§11, analog PASS 16 ≥ 5); T4-readability limitation stated
  (§12), not re-registered.

**No research-log entry written** (LOG-174 covers this dispatch, per
instructions).
