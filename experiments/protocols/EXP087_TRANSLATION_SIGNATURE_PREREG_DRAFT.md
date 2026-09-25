# EXP087 — Uniform-field threshold model of the output bridge (translation-signature verification) — PRE-REGISTRATION SKELETON (DRAFT)

> **STATUS: DRAFT — NOT SIGNED. Pre-Law #14. No experiment number is minted by
> this file; EXP087 is the *recommended* number (LOG-292; verified unclaimed in
> the protocols directory and the research log — renumbered from EXP086 after
> a concurrent wave minted EXP086 for the R3 amplifier draft; standing
> collision rule applied). NUMBER-COLLISION REPAIR (LOG-300 F6, discharged
> 2026-09-24): a concurrent wave's `EXP087_RECIRCULATION_PREREG_DRAFT.md`
> briefly claimed EXP087; it has been renumbered to
> `EXP088_RECIRCULATION_PREREG_DRAFT.md` (verified: exactly one EXP087 draft
> file exists in the protocols directory). EXP087 is this skeleton's number;
> the number mints only at signing. This skeleton exists so the
> next wave can cost, review, and formalize it. Do not execute.**
>
> **LOG-314 (2026-09-24) — signing-prep lane:** §8 item 1 RESOLVED (±0.10
> licensed in writing as a between-configuration envelope — a statistical
> bar is shown not-derivable from archived data); §8 item 2 RESOLVED (c_i
> alignment join pinned: order pin O + SHA-256 prompt-hash verification;
> R4 licensed, strike not needed). New §8 item 6 records an R5
> verdict-mapping defect for the CEO's signing decision (table left as
> LOG-306 signed it). DRAFT / unsigned / GPU-dark watermarks intact; no
> signed protocol touched.

## 1. Objective (one sentence)

Test whether the output bridge's decision effect is *exactly* a uniform
t−f margin translation — i.e., whether the rescue set is parameter-free
predictable from archived base margins — which would close the bridge's
mechanism candidacy (KILL) and leave it a calibrated instrument, or, on any
mismatch, evidence non-translation structure worth chasing (CONTINUE).

## 2. Law #15 gate card

1. **Precise question:** Is the bridge's per-item margin shift Δm_i = μ + ε_i
   with sup|ε_i| < μ (strict positivity), and does the observed rescue set
   equal {i : m₀,i ∈ (−μ−ε_i, 0)} exactly, where m₀,i is the per-item base
   t−f margin? Endpoints: per-item (m₀,i, Δm_i) logging on N=60; exact
   set-identity check (parameter-free); boundary-band subset check on a weak
   arm.
2. **Decision it changes:** KILL / CONTINUE on whether the bridge's decision
   effect has any non-translation structure — the program's last open
   mechanism question about the only intervention that ever moved decisions
   (K1 exonerated tilt; LOG-197 Q1/Q2 kept the L1 license narrow; mechanism
   still [OPEN]).
   - **KILL** (identity holds exactly, c=0, μ̂ replicates): the bridge's
     decision effect is closed-form explained — no item-specific mechanism,
     no propagation story, no further mechanism experiments on this family.
     The bridge becomes a calibrated translation instrument (rescue control
     with a predictive model), nothing more.
   - **CONTINUE** (any mismatch — a corruption, a rescued item outside the
     band, corr(Δm_i, c_i) not replicated per the pinned rule below): the
     pure-translation model is dead; non-translation structure exists —
     item-specific or nonlinear propagation effects — and the mechanism hunt
     re-opens on the output side with a concrete anomaly to chase.
     **Law #7 boundary (LOG-300 F7):** a CONTINUE verdict does NOT license
     using the bridge as a positive control for autonomous steering — the
     bridge is option-informed (LOG-204 §H7 demotion stands: rescue control
     / known-answer direction, NOT a mechanism control). Any follow-on
     mechanism claim requires a non-option-informed intervention.
3. **Cheapest falsifying test:** 180 forward passes (3 arms × 60 items,
   pythia-410m/L20, <1 min on 2×T4): C1 baseline logging per-item base
   margin m₀,i and decision; C2 bridge (EXP066 `make_bridge_vec` verbatim,
   α=0.5) logging per-item Δm_i and decision; C3 static B_agg (α=0.5)
   logging per-item Δm_i and decision (boundary-band control). No new
   construction, no new benchmark — the archive already holds every vector
   this needs except the un-logged base margins.
4. **Mathematical license:** [PROPOSITION] the Uniform Translation
   Signature (LOG-286 §3), **conditional on the explicit
   [ASSUMPTION] (binary channel)** below:
   - **[ASSUMPTION — binary channel (LOG-300 F1):** on every item, the
     decision is determined by sign(ℓ_t − ℓ_f) — i.e., argmax ∈ {t, f}, no
     third-token flips. The translation premise constrains only the t−f
     margin; without this assumption, (a) does not follow, because on a
     base-correct item the intervention could push a third token k above t
     (the premise says nothing about (w_{t_i}−w_{k})·δh), producing a
     corruption with m₀,i + Δm_i > 0 intact. The same assumption underwrites
     (b)'s ⇔ (a base-wrong item with t beating f but losing to a third
     token would have m₀ < 0 without being wrong in the t−f sense).]
   - Given the binary-channel assumption: if Δm_i = μ + ε_i with μ > 0 and
     sup|ε_i| < μ, then (a) c = 0 necessarily (no t−f-channel corruption);
     (b) rescue set = {m₀,i ∈ (−μ−ε_i, 0)}; (c) the t−f-margin decision
     effect is fully parameterized by (μ, {ε_i}).
   - The primary endpoint (Hamming(P, observed rescues) = 0) is *exactly
     the empirical test of this assumption* — the experiment's strength,
     not a weakness. "Parameter-free" is therefore slightly oversold (P is
     built from measured per-item Δm_i; the test's real content is the
     binary-channel assumption).
   Quantitative predictions (from `exp066_instance_evaluations.json`):
   (a) min_i Δm_i > 0 (archived: 0.64815); μ̂ within the pinned
   between-configuration envelope 0.74921 ± 0.10 (i.e. [0.649, 0.849] —
   an envelope, NOT a statistical bar; full justification §8 item 1,
   resolved LOG-314);
   (b) rescued_C2 == {m₀,i + Δm_i > 0 > m₀,i} exactly (Hamming distance 0);
   (c) corr(Δm_i, cos(b̂_i, ŵ_{t_i})) > 0, one-sided p < 0.05 (archived
   r = 0.49708, p = 5.3e-05 — this is a partial replication, not a
   discovery: Δm_i is re-measured on the fresh run; c_i is reused from K1's
   weights-only archive, legitimate under Δθ=0 determinism but not
   re-measured — pairing via the pinned join rule, §8 item 2, resolved
   LOG-314);
   (d) rescued_C3 ⊆ rescued_C2 (boundary-band subset; archived smoke
   precedent: cone-rescued ⊆ bridge-rescued in
   `exp077_instance_records.json`).
   **Falsification table (LOG-300 F3 — registered rows, not prose):**

   | # | Claim under test | Prediction | Breaking point | Verdict implication |
   |---|---|---|---|---|
   | R1 | Uniform translation (strict positivity) | min_i Δm_i > 0 | any C2 corruption (c > 0) — or, conditional on the F1 binary-channel assumption, any Δm_i ≤ 0 | translation model dead → **CONTINUE** |
   | R2 | Rescue-set identity (parameter-free) | rescued_C2 == P exactly, Hamming = 0 | any rescued item with m₀,i + Δm_i ≤ 0; any Hamming ≠ 0 | → **CONTINUE** (F1 assumption is the test's content; a mismatch is a crack in the readout-only account) |
   | R3 | Boundary-band subset | rescued_C3 ⊆ rescued_C2 | **a C3 rescue of a C2-resistant item** (standalone KILL row for the subset proposition) | → **CONTINUE**: non-readout structure implicated |
   | R4 | corr replication (partial) | corr(Δm_i, c_i) > 0, one-sided p < 0.05 | **any other outcome, including a non-significant positive corr** — the (0, p ≥ 0.05) zone is a break, not a hold | → **CONTINUE** (anomaly) |
   | R5 | μ̂ replication (apparatus envelope) | μ̂ ∈ [0.649, 0.849] (0.74921 ± 0.10 between-configuration envelope — §8 item 1 resolved LOG-314; NOT a statistical bar) | μ̂ outside the envelope | → **CONTINUE** |

   Any single row's breaking point → the pure-translation model is dead
   (all five hold exactly → **KILL** the mechanism candidacy).

   **F4 note (LOG-300; RESOLVED LOG-314):** the ±0.10 bar is ≈ the archived
   per-item spread (sup|ε| = 0.10106, recomputed from the archive) and ~20×
   SE(μ̂) ≈ 0.0049 — it is NOT a statistical replication bar, and no such
   bar is derivable: the replication re-measures the same 60 items, so μ̂′
   has a degenerate distribution under the determinism pin (full
   derivation §8 item 1). ±0.10 is licensed **in writing as a
   between-configuration envelope** (0.74921 ± 0.10, i.e. [0.649, 0.849]):
   it covers both historical configuration means (0.749 at 410m/α=0.5;
   0.7639 at 160m per `exp065_results.json`, LOG-300's α=1.0
   characterization) and the per-item spread envelope, and catches only
   gross apparatus failure — it does NOT measure replication precision and
   does NOT test the translation hypothesis. The old justification
   ("archived σ̂_ε = 0.038 × ~2.6") stays struck. §8 item 6 records the R5
   verdict-mapping consequence for the CEO's signing decision.

## 3. Design (skeleton)

- **Model / layer:** pythia-410m, layer 20 (program continuity with
  EXP066/077). **Benchmark:** the signed 60-item 2-hop/3-hop relational set
  (EXP066-identical; headroom gate 40–70% carried over).
- **Arms (GPU):**
  - C1 unintervened — log per-item base margin m₀,i = ℓ_{t_i} − ℓ_{f_i}
    and decision. (The archive never logged m₀,i — this arm exists only to
    supply it.)
  - C2 output bridge — EXP066 `make_bridge_vec` verbatim
    (normalize(E[t_i] − E[f_i]), α = 0.5, L20 residual, final-token
    position); log per-item Δm_i and decision. Labeled *rescue control /
    instrument calibration* per LOG-204 §H7 — NOT a mechanism arm (Law #7).
  - C3 static B_agg (α = 0.5, L20) — boundary-band control; log per-item
    Δm_i and decision. Predicted: |Δm_i| ~ 0.01–0.03 (archived mean
    +0.009), rescue set ⊆ C2's (possibly empty).
- **Primary analysis (parameter-free, pre-registered):** compute the
  predicted rescue set P = {i : m₀,i < 0 < m₀,i + Δm_i} from C1+C2 logs;
  report Hamming(P, observed rescues). P == observed → translation model
  holds → KILL the mechanism candidacy. Any mismatch → CONTINUE.
- **Secondary analyses (pre-registered):** (i) μ̂, σ̂_ε, min Δm_i with the
  strict-positivity check; (ii) μ̂ replication vs the 0.74921 ± 0.10
  between-configuration envelope (apparatus check — §8 item 1, resolved
  LOG-314; NOT a statistical bar);
  (iii) corr(Δm_i, c_i) one-sided partial-replication test (c_i =
  cos(b̂_i, ŵ_{t_i}) from weights-only recomputation, K1-verified
  construction): **PASS = one-sided p < 0.05 for corr > 0; any other
  outcome — including a non-significant positive corr — → CONTINUE
  (anomaly)**. The item-alignment join is PINNED (§8 item 2, resolved
  LOG-314): the K1 JSON carries no per-item ids, so the join is an order
  pin — c[j] ↔ instance key O[j] (verbatim list in §8 item 2), licensed by
  K1's archive-verified G2 byte-identity guard — with SHA-256 prompt-hash
  verification required on the fresh-run side (FATAL on mismatch). Pairing
  c[j] with O[j] reproduces the archived r = 0.49708 exactly (sorted-key
  pairing gives r = −0.21388, confirming the pairing is load-bearing). Any
  join failure → R4 struck at signing, not carried unresolved;
  (iv) boundary-band subset: rescued_C3 ⊆ rescued_C2 (exact set check —
  falsification row R3);
  (v) random-field threshold fit: rescue fraction among wrong items vs
  μ̂ against the archived (0.749 → 8/26; 0.764 → 10/19) points.
- **Statistics:** the primary check is deterministic (exact identity), not
  a significance test — N=60 gives 60 independent per-item (m₀, Δm)
  constraints on a zero-free-parameter model. Secondary (iii) uses the
  archived effect size (r = 0.497) for a one-sided partial-replication
  test (Δm_i re-measured; c_i reused from the K1 archive under Δθ=0).
  δ_min = 0.05 and McNemar conventions apply only if a decision-count
  comparison is reported; they are not the primary endpoint.
- **Pre-registered confounds / guards:** (i) Δθ=0 hash guard (per-runner
  verbatim formulation — LOG-213 G3 lesson); (ii) LayerNorm-saturation
  check: if any |Δm_i| deviates > 4σ from μ̂, flag nonlinearity (feeds the
  breaking-point analysis, not silently dropped); (iii) the C2 arm must
  reproduce the archived b=8/c=0 cell within McNemar noise — a large
  deviation invalidates the run as a replication (apparatus check, cf. the
  smoke-vs-official 14-vs-6 discrepancy noted in LOG-286).

## 4. Cost

180 forward passes ≈ <1 min on 2×T4 [ESTIMATE from 22 fwd/s]. $0 beyond
the queued GPU time. Queues behind K2 → EXP083 → EXP084 (no pre-emption).

## 5. Novelty (honest)

N1. No prior-art claim: this is a *mechanism-closure* experiment on the
program's own instrument, not a new method. Adjacent: the program's own K1
(D1 readout-projection match) and LOG-197 Q2 (narrow L1 license) — EXP087
is the decision-level closure of that line. If the identity holds, the
publishable unit is a *negative* mechanism result with a predictive model
(rare and valuable); if it breaks, the anomaly is the program's first
evidence of non-readout structure.

## 6. Relation to the boundary

Strengthens I1 whichever way it goes. KILL branch: the boundary paper gains
a closed-form account of its only positive phenomenon ("the bridge is a
uniform margin translation; c=0 is a theorem, not a signature") — the
honest headline the program owes. CONTINUE branch: the first crack in the
readout-only account — the highest-value anomaly the program has produced.

## 7. Sequencing

Draft (this file) → Law #14 review → formal pre-registration → GPU queue
(behind K2/EXP083/EXP084) → verdict → either instrument-calibration note
(KILL) or anomaly-chase proposal (CONTINUE). The standing boundary-band
subset screen (§3 secondary iv) is proposed alongside as a $0 standing
analysis amendment for all future weak-arm results with per-item records.

## 8. Open items for the formal pre-reg

1. **[RESOLVED LOG-314 — the μ̂ replication bar.]** First-principles
   derivation. All headline numbers recomputed from the primary artifact
   `experiments/runs/EXP066_pythia410m_replication/exp066_instance_evaluations.json`
   (per-item `Same_Layer_Output_Bridge_margin_shift`): μ̂ = 0.74921,
   σ̂_ε = 0.03808, sup|ε| = 0.10106, min Δm_i = 0.64815, SE(μ̂) =
   σ̂_ε/√60 ≈ 0.00492. — **Estimator and sampling distribution:** μ̂ is the
   mean over N = 60 FIXED benchmark items, and the EXP087 replication
   re-measures the SAME 60 items (not a sample). Under the protocol's
   determinism pin (Δθ=0; pinned snapshot, code, environment), each Δm_i
   is a fixed scalar, so the replication's μ̂′ has a DEGENERATE
   distribution: μ̂′ = 0.74921 with probability 1, up to unmeasured
   floating-point/device noise. There is NO non-degenerate sampling
   distribution for |μ̂′−μ̂| derivable from archived data: (i) SE(μ̂) is the
   standard error of a *superpopulation* mean — it quantifies item
   heterogeneity, not replication noise on the same items (using it as a
   replication bar is the exact error LOG-300 F4 struck); (ii) a
   device/seed numerical-tolerance component has no archived measurement —
   the only two historical points (0.74921 at 410m/α=0.5; 0.76393 at 160m
   per `experiments/runs/EXP065_coordinate_alignment/exp065_results.json`
   `Same_Layer_Output_Bridge/delta_margin`, LOG-300's α=1.0
   characterization) differ in model AND α, i.e. are different quantities,
   not reruns — so any such tolerance number would be convention-by-fiat,
   which is forbidden; (iii) a priori fp-error bounds for a 410M-param
   forward pass are vacuous. **Conclusion:** a statistical replication bar
   is NOT derivable without assumptions the protocol cannot license. Per
   the reviewer-licensed alternative, **±0.10 is justified in writing as a
   between-configuration ENVELOPE, not a statistical bar**, centered at the
   archived 410m/α=0.5 mean: **R5 bar = 0.74921 ± 0.10, i.e. μ̂ ∈ [0.649,
   0.849]**. — **WHAT THE ENVELOPE COVERS:** (a) both historically observed
   configuration means — 0.74921 (410m/α=0.5) and 0.76393 (160m),
   |Δ| = 0.0147 ≪ 0.10; (b) the archived per-item spread envelope
   sup|ε| = 0.10106 ≈ 0.10 — no single-item anomaly can break the mean
   through it (max single-item leverage on μ̂ is sup|ε|/60 ≈ 0.0017);
   (c) gross apparatus failure — margin units are O(1) logits, so a
   mis-constructed bridge (dropped normalization, wrong vector, wrong
   readout extraction) shifts μ̂ by O(1) or collapses it toward the C3
   scale (archived C3 mean +0.009); a wrong-α run (α=1.0 on 410m ≈ 2×0.749
   ≈ 1.5 under α-linearity) breaks the envelope. — **WHAT IT DOES NOT
   COVER:** (a) NOT replication precision — under the determinism pin a
   true replication has |μ̂′−μ̂| ≈ 0 to unmeasured numerical noise; the
   envelope is ~20× SE(μ̂) and cannot detect subtle misconfiguration;
   (b) NOT configuration discrimination — a wrong configuration whose mean
   falls inside [0.649, 0.849] (e.g. 160m at 0.7639) PASSES the envelope
   without being a replication of the 410m/α=0.5 arm (configuration
   identity is enforced by the determinism pin + §3 apparatus guard (iii),
   not by R5); (c) NOT the translation hypothesis — R5 tests the
   apparatus, not the mechanism (R1/R2 test translation structure). The
   old justification ("archived σ̂_ε = 0.038 × ~2.6") stays struck
   (LOG-304).
2. **[RESOLVED LOG-314 — the c_i item-alignment join is PINNED.]** The K1
   JSON (`research/analysis_plans/K1_RESULTS_LOG213_2026-09-23.json`,
   `endpoint_a.EXP066.c`, 60 floats) carries no per-item key material, so a
   pure prompt-hash join against the JSON is IMPOSSIBLE as specified — the
   constructible join is an ORDER PIN licensed by K1's archive-verified G2
   guard, with SHA-256 prompt-hash byte-identity verification required on
   the fresh-run side. Construction chain (verified in-repo): `c[j]` is
   appended by `compute_endpoint_a` iterating `ids066_410`
   (`research/analysis_plans/K1_execute_LOG213_2026-09-23.py` ll. 328–351),
   built from `items065_066` in order; K1's G2 guard asserted
   `rec066[O[j]]["prompt"] == items065_066[j]["prompt"]` byte-verbatim for
   all j (FATAL on mismatch; guard passed), where O is the verbatim order
   list from the executor (ll. 265–268):
   O = [pythia410m_planet_2hop_0..14, pythia410m_planet_3hop_0..14,
   pythia410m_element_2hop_0..14, pythia410m_element_3hop_0..14]
   (i.e. `pythia410m_planet_2hop_{i}`, `pythia410m_planet_3hop_{i}`,
   `pythia410m_element_2hop_{i}`, `pythia410m_element_3hop_{i}` for i = 0..14,
   in that block order). Independently verified in this wave: the archive
   `experiments/runs/EXP066_pythia410m_replication/exp066_instance_evaluations.json`
   holds 60 unique keys whose file-insertion order EQUALS O (this is why the
   archived r exists under insertion-order pairing), and pairing c[j] with
   O[j] reproduces the archived r = 0.49708 exactly (sorted-key pairing gives
   r = −0.21388, confirming the pairing is load-bearing). **Pinned join
   rule:** (inputs) the K1 JSON, the EXP066 archive, the verbatim O list
   above, and the EXP087 fresh-run per-item logs; (hash function) SHA-256
   over the UTF-8 bytes of the prompt string, byte-verbatim, no
   normalization; (join rule) for j = 0..59, pair c[j] with the fresh-run
   record whose `instance_key == O[j]`, and REQUIRE
   SHA-256(fresh prompt) == SHA-256(archive prompt at O[j]) — FATAL on any
   mismatch (a changed prompt invalidates the join; it never silently
   mis-pairs); (tie-breaking) none required — keys are unique on both sides
   (assert |keys| = 60 and all-distinct on each side; duplicates → join
   FAILS); (failure modes) c length ≠ 60 → fail; fresh key set ≠ O set →
   fail; any prompt-hash mismatch → fail; duplicate keys → fail. **Runner
   requirement:** every fresh-run per-item log record carries `instance_key`
   verbatim from the benchmark spec (the benchmark is EXP066-identical, so
   the 60 keys of O). On ANY join failure, R4 is unlicensed and must be
   STRUCK at signing — it is not carried as unresolved and has no fallback.
   The corr endpoint's decision rule is unchanged (PASS = one-sided p < 0.05
   for corr > 0; any other outcome → CONTINUE); the join makes the pairing
   bit-for-bit reproducible by an independent implementer. **Strike not
   needed:** the join pins honestly, so R4 stays registered.
3. Decide whether C1's m₀,i logging needs a second seed (determinism pin
   says no; reviewer to confirm).
4. Pre-register the LayerNorm-saturation flag's exact 4σ rule vs an
   absolute-margin rule.
5. Confirm the KILL-branch write-up venue (boundary-paper §5.4 addendum vs
   standalone note).
6. **[OPEN — LOG-314 design-defect report; CEO signing decision.]** The
   envelope justification (item 1) reveals an inconsistency in the
   registered falsification table: R5's breaking point (μ̂ outside the
   envelope) maps to **CONTINUE (anomaly)**, but the envelope is licensed
   as an APPARATUS sanity bound, not a mechanism test. Under the
   determinism pin a true replication has |μ̂′−μ̂| ≈ 0; the envelope is
   ~20× wider than SE(μ̂), so a breach is almost certainly apparatus
   failure (mis-constructed bridge, wrong readout extraction), which
   licenses neither KILL nor CONTINUE on the mechanism — it licenses a
   rerun. Mapping breach→CONTINUE would systematically misread broken runs
   as non-translation structure, contradicting §3 guard (iii) ("a large
   deviation invalidates the run as a replication"). **Proposed re-mapping
   (NOT applied — the table is left exactly as LOG-306 signed it, per Law
   #4):** μ̂ outside [0.649, 0.849] → RUN-INVALID (apparatus), mechanism
   verdict withheld, rerun required. The CEO decides at signing whether to
   adopt this re-mapping or keep the registered CONTINUE mapping with
   written rationale. This item must not be signed past unresolved.

## 9. Steelman

*The identity is guaranteed to hold because the bridge is constructed from
the readout rows — this experiment can only confirm what K1's D1 already
showed.* Answer: D1 matched *aggregate* ratios within 4.5–11%; it did not
test the *per-item* identity, the strict-positivity condition, or the
rescue-set prediction — and it is exactly at the per-item level that a
propagation/attention-routed component would appear (K2's open question).
A deterministic per-item identity is a strictly stronger claim than a
ratio match, and its breaking points are pre-registered. If it holds, the
KILL is real: the mechanism question this program has kept open for 60+
logs closes with an equation, not a shrug.
