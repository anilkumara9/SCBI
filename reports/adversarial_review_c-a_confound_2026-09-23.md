# Law #14 Adversarial Review — C-A Entity-Similarity-Leak Confound

**Date:** 2026-09-23 · **Dispatch:** LOG-144 · **Reviewer role:** Law #14 Adversarial Reviewer
**Target:** C-A sketch in `research/innovation/SPRINT2_2026-09-23.md` §C-A (cross-item donor-bridge transfer)
**Mandate:** Sprint-2 condition (b), CEO-endorsed — C-A's pre-registration must survive this confound review before any bundle work.
**Mode:** analysis only; no GPU, no experiments, no signed artifacts touched.

**Corpus read (TEAM_KNOWLEDGE_PROTOCOL §1):** `research/TEAM_KNOWLEDGE_PROTOCOL.md`,
`research/innovation/SPRINT2_2026-09-23.md` (§C-A verified verbatim), `AGENTS.md` (14 laws),
`research/analysis_plans/G1_REPORT_2026-09-23.md`, `reports/adversarial_audit_exp065_exp066.md`
(Findings 3–4), `reports/adversarial_review_exp078_bundle_2026-09-23.md`,
`reports/adversarial_review_exp077_prereg_2026-09-23.md`, `theory/BOUNDARY_CLAIM_FORMALIZATION.md`,
`experiments/runs/exp077/run_exp077.py` (benchmark construction + `make_bridge_vec`),
plus injected standing context (`MEMORY.md`, mentorship directive P1–P4, evidentiary levels).

**One challenge (§2 obligation):** the sprint's C-A sketch assumes donor↔test answer-token overlap is a
controllable corner case ("survives donor↔test token-overlap stratification"). The benchmark construction
shows it is the *default*: 60 test items draw answers from a **10-token pool**
(Mars, Venus, Jupiter, Saturn, Mercury, Iron, Gold, Silver, Bronze, Steel — `run_exp077.py:149-150`),
with `A`=target, `C`=foil per item. Any donor bank drawn from the same item distribution
**necessarily shares answer tokens with test items**. Leakage is therefore the null hypothesis for any
C3 rescue, not a confound to be stratified away as an afterthought. Worse, the sketch's implied fix —
balancing the donor bank across answer tokens — *annihilates the intervention itself* (§1.4 below):
a balanced bank's centroid cancels to near-noise, killing power under *both* hypotheses.

**One idea (§2 obligation):** a **$0-GPU weight-only leakage pre-audit as a standing pre-registration gate**
for any donor-bridge design: from weights alone compute the donor centroid's pre-normalization norm
(degeneracy check) and the per-test-item similarity features `s_t(j)`, `s_f(j)` (§1.2); pre-register only
if the centroid is non-degenerate *and* the low-similarity stratum is non-empty with headroom. This
falsifies degenerate designs before a single forward pass and costs nothing.

---

## 0. What C-A claims, and what the confound is

**The proposal (verified against SPRINT2 §C-A):** apply a bridge direction built from *labeled donor items*
(entity-disjoint, same relation template) to unlabeled test items. Arms: C1 baseline · C2 oracle self-bridge
(positive control) · C3 same-relation donor-centroid bridge (primary) · C4 different-relation donor
(negative) · C5 random-target donor (content control) · C6 random direction. Endpoint: McNemar exact, N=60.
Kill: ΔM_C3 ≤ 0 while C2 rescues. The sketch names the confound: "C3's win is licensed as transfer only if
it survives donor↔test token-overlap stratification."

**The confound, stated plainly:** the donor bridge may rescue test items by **steering the readout toward
answer tokens that are identical or similar to donor answer tokens** — without transferring any abstract
relational structure. Under audit Finding 4 ([INTERPRETATION], corroborated by G1), the bridge is
near-direct answer-logit steering, QK-unremarkable (G1: bridge Ē_QK = 0.356, mid-null, p_high = 0.23 —
[OBSERVATION]). A donor bridge is therefore, mechanistically, a *similarity-weighted prior over answer
tokens*. If it "works," the program will have demonstrated dataset-prior steering, not cross-item
structural transfer — and will have spent its best label-free capability slot on a mirage.

**Evidentiary level (mentorship directive, standing law):** even a clean C-A win reaches at most Level 1
("can improve inference" via an intervention). It cannot reach Level 2 ("changes computational strategy")
or Level 3 ("creates qualitatively new capability"), because under *both* the transfer and leakage
hypotheses the mechanism is readout steering. The pre-registration must not claim otherwise (P1: the
canonical question stays mechanism-level).

---

## (a) Mathematical formalization of the confound

### Setup ([DEFINITION] / FACT — grounded in `run_exp077.py:725-729` and the audit)

- Unembedding matrix $W_U \in \mathbb{R}^{V \times d}$ ($d=1024$, pythia-410m); rows $W_U[y]$.
- Per-item oracle bridge: $b(x_j) = \mathrm{normalize}(W_U[t_j] - W_U[f_j])$, $t_j$ = target (item `A`),
  $f_j$ = foil (item `C`). Injection at layer $l^*=20$ (last token): $h \leftarrow h + \alpha b$, $\alpha$
  pre-registered (EXP077 used a fixed `ALPHA_BRIDGE`).
- Donor bank $D$ (labeled, premise-entity-disjoint from test items). Donor-centroid bridge
  (recommend the sum-of-differences form, pinned in pre-reg):
  $$\hat{b}_D = \mathrm{normalize}\!\left(\sum_{d \in D} (W_U[t_d] - W_U[f_d])\right)
  = \mathrm{normalize}\!\left(\sum_{y} W_U[y]\,(n_t(y) - n_f(y))\right)$$
  where $n_t(y), n_f(y)$ count donor occurrences of token $y$ as target/foil. **This identity is the
  whole confound in one line** ([PROPOSITION]/INFERENCE — algebra, no experiment): the centroid is the
  donor bank's *token-prior direction* — "usually-right minus usually-wrong" in unembedding space.

### The bypass model ([INTERPRETATION] — audit Finding 4; G1 corroboration)

Injection perturbs final logits approximately as (downstream residual propagation of a QK-unremarkable
direction — [OBSERVATION] G1 §1–§4):

$$\Delta \ell_j(y) \;\approx\; \alpha\,\langle W_U[y],\, \hat{b}_D \rangle \;+\; \text{(attention-mediated terms, not privileged per G1)}$$

i.e. the intervention adds logit mass to answer $y$ **exactly in proportion to $y$'s unembedding
similarity to the donor bank's target-minus-foil direction**. No relational computation is required
for a decision flip — only that the argmax over the two named options moves.

### The leakage channels (load-bearing; label each)

For test item $j$ with options $\{t_j, f_j\}$, define the weight-only, $0$-GPU similarity features
([DEFINITION] proposed for the pre-reg):

$$s_t(j) = \cos(\hat{b}_D,\, W_U[t_j]), \qquad s_f(j) = \cos(\hat{b}_D,\, W_U[f_j])$$

- **L1 — target-identity leakage** ([HYPOTHESIS], directly testable): $\exists d: t_d = t_j$.
  Then $W_U[t_j]$ carries a positive coefficient in $\hat{b}_D$ and the injected direction contains a
  component *parallel to the oracle self-bridge*. With a 10-token answer pool shared between donors
  and tests ([FACT] from benchmark construction), $P(t_d = t_j) > 0$ is structural, not accidental.
- **L2 — target-similarity leakage** ([HYPOTHESIS]): $t_d \ne t_j$ but $\cos(W_U[t_d], W_U[t_j])$
  large (same-category entities — planets vs planets — have similar unembedding rows). Boosts $t_j$
  via category similarity.
- **L3 — foil-suppression leakage** ([HYPOTHESIS]): $f_d \sim f_j$; the negative $W_U[f_d]$
  components suppress the foil; a correct decision via suppression, not relation.
- **L4 — bank-prior leakage** ([HYPOTHESIS]): $(n_t - n_f)$ skewed (e.g., some entities appear as
  target more often in the donor bank); $\hat{b}_D$ then boosts frequently-correct tokens on *every*
  test item. If donor and test items are drawn from the same benchmark distribution, the prior
  transfers even with zero per-item similarity.
- **L5 — template wording** ([ASSUMPTION], controlled by design): relation wording ("outranks" /
  "is lower than") is constant across arms; it enters $h$, not $\hat{b}_D$ (unembedding-space), so
  it cannot produce arm differences. Pre-register as a design constant.

### The observational signature that separates leakage from transfer

([PROPOSITION]/INFERENCE — the pre-reg's discrimination logic:)

- **Leakage signature:** C3's per-item rescue is predicted by $s_t(j) - s_f(j)$; rescue concentrates
  in the high-similarity stratum; the similarity-matched different-relation control C4′ (§b)
  rescues as much as C3; the permuted-label control C5 (§b) rescues as much as C3.
- **Transfer signature:** C3 rescues items in the **low-similarity stratum** ($s_t(j)$ at/below the
  pre-registered null); C3 beats similarity-matched C4′ (paired McNemar $p<0.05$); the relation-match
  indicator carries significant weight with $(s_t, s_f)$ covaried; C5 (relation content destroyed,
  prior preserved) fails.

### The centroid-degeneracy trap ([PROPOSITION]/INFERENCE — the sketch's unspotted design flaw)

If the donor bank is *balanced* so $n_t(y) \approx n_f(y)$ for all $y$ (the naive "fix" for L4), then
$\sum_d (W_U[t_d]-W_U[f_d]) \approx 0$ and $\hat{b}_D$ is a **renormalized near-noise vector** —
C3 becomes C6 (random direction) by construction, with zero power under *both* hypotheses.
Balancing does not de-confound; it annihilates. The pre-reg must therefore report the
pre-normalization norm $\|\sum_d (W_U[t_d]-W_U[f_d])\|$ against the $\sqrt{|D|}$ scale and gate on
non-degeneracy (§b.6) — the EXP078 energy-gate lesson applied at design time.

---

## (b) Required design features and controls for the C-A pre-registration

The pre-reg **MUST** contain all of the following. Anything less cannot separate transfer from leakage.

### b.1 Donor-selection rules (exact, pinned)
1. Donors are labeled items **disjoint from the 60 test items** (no shared premise triples; Law #7:
   donor labels are support-side construction material; test items remain unlabeled at intervention
   time — state this explicitly).
2. Pre-register the **exact donor list** (item ids), relation template(s), and the $(t_d, f_d)$
   **token histogram over the 10-entity pool** — L4 made auditable.
3. Pre-register the centroid construction: sum-of-differences-then-normalize (recommended) vs
   per-donor-normalize-then-average. Do not leave this to the builder; the bypass math differs.
4. **Do not "fix" leakage by balancing** the donor bank (§a, degeneracy trap). Keep a natural bank,
   disclose its skew, and rely on controls + stratification.

### b.2 Weight-only similarity audit (pre-GPU, $0 cost — the §2 idea as a gate)
5. Compute $\hat{b}_D$, then $s_t(j), s_f(j)$ for all 60 test items from weights alone; report both
   distributions and the permutation null (random donor banks of equal size → null distribution of
   $s_t$; pre-register the percentile used).
6. **Degeneracy gate:** report $\|\sum_d (W_U[t_d]-W_U[f_d])\| / \sqrt{|D|}$; pre-register a floor
   (e.g. ≥ 0.25 of the single-donor scale). Below floor → **redesign the donor bank, never run**.
7. **Stratum feasibility gate:** the low-similarity stratum (b.4) must be non-empty **and contain
   headroom items** (C1-wrong items — else the stratum test is vacuous). If empty → the benchmark
   cannot support the transfer claim in this operationalization → DO-NOT-RUN as a transfer test
   (may still run as a leakage demonstration, §d).

### b.3 Similarity-matched negative controls (the arms the sketch lacks)
8. **C4′ — similarity-matched different-relation donor** (replaces the sketch's naive C4): donor
   bank from a different relation template ("is next to" support items), selected by a pre-registered
   greedy-matching algorithm to **match C3's $(s_t, s_f)$ distribution** over test items within
   tolerance $\delta$ (pre-registered). Report achieved match quality. Rationale ([INFERENCE]): the
   sketch's C4 confounds relation with similarity — different-relation donors have a different
   token-similarity profile, so C3 > C4 proves nothing about relation. Only a similarity-matched
   C4′ isolates the relation channel.
   - *Pre-registered fallback:* if matching fails (max discrepancy $> \delta$), the C3-vs-C4′
     contrast is demoted to exploratory and the stratum analysis (b.4) becomes the primary
     discrimination. No post-hoc promotion (Law #4).
9. **C5 — permuted-label donor (prior-preserving, relation-destroying)** (redefines the sketch's C5):
   same donor premises, but $(t_d, f_d)$ pairings **randomly permuted among donors** (seed-pinned).
   This preserves the bank token prior $(n_t - n_f)$ exactly while destroying per-donor relational
   content. If C5 ≈ C3 → the rescue is prior/similarity, not relation. The sketch's "random-target
   donor" destroys both channels and therefore discriminates nothing — this redefinition is mandatory.
10. **C6 — random unit direction** (procedure control, unchanged). **C2 — oracle self-bridge**
    (positive control AND headroom gate: if C2 fails to rescue on this run, $p \ge 0.05$, then any
    C3 null is **Inconclusive**, not a kill — procedure invalid).

### b.4 The exact comparisons
11. **Primary:** McNemar exact per arm vs C1 (N=60, $\alpha=0.05$). No Wilcoxon/margin endpoints
    anywhere (Law #9; audit Finding 3 — B_wrong $p=1.2e-08$ with $b=c=0$ invalidated margins).
12. **Discrimination contrast:** paired McNemar on C3-vs-C4′ decisions directly (not via separate
    vs-C1 tests — Law #9-adjacent: comparing significances is not a significance comparison).
13. **Stratum analysis:** pre-register the low/high-similarity split **before any forward pass**
    (e.g. median split on $s_t(j)$, or tertiles with the middle dropped — pinned, not chosen
    post-hoc). Within-stratum McNemar C3-vs-C1. Transfer requires the low stratum to fire.
14. **Item-level model (pre-registered):** rescue$_j$ ~ relation-match$_j$ + $s_t(j)$ + $s_f(j)$
    (+ pre-registered link, e.g. logistic). Transfer requires the relation-match coefficient
    significant with similarities covaried. This is the precise "survives stratification" the
    sketch gestures at.

### b.5 Decision rule for each outcome (verdicts only from the permitted set)
- **Transfer licensed (HYPOTHESIS: Supported)** iff ALL hold: (T1) C3 vs C1: $\Delta M>0$, $p<0.05$;
  (T2) C2 rescues ($p<0.05$), else Inconclusive; (T3) C3 beats C4′ paired ($p<0.05$); (T4) low-similarity
  stratum fires ($p<0.05$); (T5) C5 does **not** rescue ($p \ge 0.05$); (T6) relation-match coefficient
  significant with $(s_t,s_f)$ covaried. License capped at evidentiary **Level 1**.
- **Leakage verdict (transfer HYPOTHESIS: Not supported; if C4′/C5 match C3 quantitatively,
  Refuted under this operationalization)** if: C3 rescues but T3 fails (C4′ ≈ C3), or rescue
  concentrates in the high-similarity stratum with low-stratum null, or C5 ≈ C3.
- **Kill (sketch's criterion, retained):** $\Delta M_{C3} \le 0$ ($p \ge 0.05$) while C2 rescues →
  donor bridge is item-specific; transfer hope for this family dead ([INFERENCE] — licenses the
  family-level kill only for *unembedding-difference donor bridges at $l^*$*, not for all transfer).
- **Underdetermined** if: C3 rescues but C4′ matching failed tolerance (fallback active) with
  conflicting stratum/model readings, or strata underpowered. "Partial transfer" is not a verdict
  (verdict standard, LOG-148).

### b.6 Budget, seeds, and anti-creep clauses
15. Recompute the forward-pass budget arithmetically from (arms × 60 × passes-per-item); the
    sprint's "2,700 passes" does not follow from 6 arms × 60 items — pin the real number, seeds,
    $\alpha$, $l^*$, hook position, SHA-256 $\Delta\theta=0$ guards.
16. **License-creep pre-emption (Law #4/#11):** the pre-reg's LICENSES section must state in
    words: *"A C3 win that fails any of T3–T6 is not transfer; it is similarity/prior steering
    consistent with audit Finding 4."* The sketch's kill criterion is one-sided (null kills, win
    auto-licenses) — the license side must be written with equal force.
17. Cite and distinguish EXP058 (LOG-066; killed internal-state cross-domain transfer — different
    mechanism family and granularity: hidden-state bases vs output-side donor bridges) and EXP078
    branch (a) (bridge power lies outside the relational-contrast subspace $S$, $e_{\mathrm{median}}
    = 0.0544$ — [OBSERVATION] — which is *why* a donor bridge cannot be a relational-contrast
    direction in disguise; if C-A works it works as readout steering, and the only question is
    whether the steering is relation-mediated).

---

## (c) PASS/FAIL criteria for signing the C-A pre-registration draft

I **SIGN** iff every item below is present and pinned (values, seeds, tolerances, exact formulas).
I **REJECT** (with the missing items enumerated) otherwise. No partial signatures.

1. [DONORS] Exact donor list (ids), relation templates, premise-disjointness proof vs the 60 test
   items, and the $(t_d,f_d)$ token histogram over the 10-entity pool. Law #7 statement (donor
   labels support-side only; test items unlabeled).
2. [CENTROID] Construction formula pinned (sum-of-differences recommended); degeneracy gate with
   pre-registered floor; weight-only similarity audit ($s_t, s_f$ distributions + permutation null)
   reported pre-GPU; stratum feasibility gate (non-empty low stratum with headroom).
3. [C4′] Similarity-matched different-relation donor arm with pre-registered matching algorithm,
   tolerance $\delta$, achieved-match report, and the demotion-to-exploratory fallback if matching fails.
4. [C5] Permuted-label (prior-preserving, relation-destroying) control as defined in b.3.9 —
   not the sketch's "random-target donor."
5. [STRATA] Low/high-similarity split rule frozen before any forward pass (cutoff value or
   percentile rule, pinned); within-stratum McNemar as a decision endpoint.
6. [MODEL] Pre-registered item-level model (rescue ~ relation-match + $s_t$ + $s_f$) with link
   function and the significance requirement on the relation-match coefficient.
7. [DECISION TREE] All five outcomes with verdicts from the permitted set only
   (Supported / Not supported / Inconclusive / Underdetermined / Refuted): transfer license
   (T1–T6 conjunctive), leakage verdict, kill, C2-headroom Inconclusive branch, C4′-matching-failure
   fallback. The anti-creep sentence from b.6.16 verbatim in LICENSES.
8. [ENDPOINTS] McNemar exact only; no margins/Wilcoxon/KL as decision endpoints (Law #9);
   C2-headroom gate; evidentiary level capped at Level 1 (no Level 2/3 language).
9. [HYGIENE] Recomputed pass budget, pinned seeds/$\alpha$/$l^*$/hook, SHA-256 $\Delta\theta=0$,
   EXP058 + EXP078(a) cited-and-distinguished, novelty N1 retained (Law #10).

---

## (d) The strongest falsification of the C-A claim itself

**The experiment/analysis:** run the pre-registered design; the C-A transfer hypothesis is
**Refuted** (not merely Not supported) if the **permuted-label control C5 rescues indistinguishably
from C3** (paired McNemar C3-vs-C5 $p \ge 0.05$ with C3 vs C1 significant) **or** C3's rescue is
**fully accounted for by $s_t(j) - s_f(j)$** with the relation-match coefficient null in the
item-level model. Either result shows the donor bridge's causal power is *entirely* token-identity/
similarity/prior steering — the relation template contributes nothing, and "donor-bridge transfer"
is a misdescription of dataset-prior steering.

**The $0-GPU pre-falsification (do first):** the weight-only audit (b.2) can kill the *design* before
the pre-reg is even signed — if the planned donor bank is degenerate (balanced → centroid ≈ noise)
or the low-similarity stratum is empty of headroom items, C-A cannot discriminate under either
hypothesis and the design is void. This costs nothing and is the cheapest falsification available
to the program.

**What a leakage verdict licenses:**
1. The C-A transfer HYPOTHESIS → **Refuted** under the tested operationalization (unembedding-difference
   donor bridges, $l^*=20$, this benchmark). The program's "best label-free capability candidate"
   slot **vacates**: C-A is removed from Tier 1; C-B (self-bridge fixed point) becomes the lead
   capability bet, per the sprint's recommended sequence.
2. A first-class **negative result** for the boundary paper's mechanism section: donor bridges rescue
   via similarity/prior steering, not relational transfer — consistent with (and strengthening)
   audit Finding 4 and G1. Publishable as boundary science, not as a capability.
3. It does **NOT** license: killing the oracle self-bridge family (C2's rescue stands — the mechanism
   question narrows to "what lawful structure, if any, lives in $W_U$ differences beyond token
   identity"); any claim about hidden-state transfer (different family, EXP058 already killed its
   static form); any weakening of other pre-registrations.
4. **Does C-A deserve a pre-registration at all?** As a *capability* pre-registration: **only** if it
   passes this review's gates (b–c) — otherwise the run cannot discriminate and is DO-NOT-RUN in
   that form. As a *leakage-demonstration* pre-registration (C3 vs C5/C4′ designed to *show* the
   steering): yes, that is legitimate boundary science — but it must be labeled as such, not as a
   capability bet.

---

## (e) Verdict on the current C-A sketch: **REVISE**

**REVISE** — not PROCEED, not DO-NOT-RUN.

The sketch's instinct is correct (it names the confound and the stratification requirement), and the
null is informative, so the idea is not dead. But the design as sketched **cannot separate leakage
from transfer**, and the gaps are structural, not cosmetic:

1. **C4 (different-relation donor) confounds relation with similarity.** Without similarity matching
   (C4′), C3 > C4 is uninterpretable. This is the load-bearing flaw.
2. **C5 (random-target donor) destroys both the relation channel and the prior channel** — it
   discriminates nothing. It must be redefined as the permuted-label, prior-preserving control.
3. **"Token-overlap stratification" is named but not operationalized**: no similarity metric, no
   donor-selection rule addressing the 10-token-pool structural overlap, no stratum cutoffs, no
   item-level model, no decision conjuncts.
4. **The kill criterion is one-sided**: the null kills, but a win is auto-licensed as transfer.
   The license side (T1–T6) must be written with equal force, including the anti-creep sentence.
5. **The centroid-degeneracy trap is unaddressed**: the natural "fix" (balancing donors) annihilates
   the intervention; the pre-reg needs the degeneracy gate.
6. **Budget arithmetic is unverified** ("2,700 passes" does not follow from the arm structure);
   recompute from first principles.

**Required revisions** = §(b) + §(c) in full. A pre-registration draft incorporating them will be
signed under LOG-144's authority. A draft missing any of (c).1–(c).9 will be rejected with the
missing items enumerated — no negotiation on the matched C4′, the permuted-label C5, or the
conjunctive license, since those three are exactly what separates this experiment from an
expensive demonstration of logit steering.

*Adversarial independence note (Law #14): this verdict answers to the CEO alone. No instruction to
soften it was received; none would have been honored. The donor bridge is the program's pet rescuer
(P2: results are evidence, not identity — sunk-cost bias disallowed), which is precisely why its
strongest confound had to be formalized before anyone is allowed to love a C3 win.*

---

*End of LOG-144 review. Report: `reports/adversarial_review_c-a_confound_2026-09-23.md`.*
