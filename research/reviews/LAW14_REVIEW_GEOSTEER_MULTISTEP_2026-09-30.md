# Law #14 Independent Review — GEOSTEER Multistep Pre-registration DRAFT + Worth-It Gate

**Lane:** independent Law #14 reviewer. **LOG-4793** (pre-assigned 4791 → 4792 → 4793; see §0).
**Date:** 2026-09-30. **$0 CPU, paper-only.** Read-only on signed protocols, weights, and artifacts.
No model runs, no GPU contact, no commits, no pushes, no spend, no publish, no dispatch,
no experiment number minted, no execution licensed (CPU or GPU).

**Review-only fence:** I did not author either artifact, I edit nothing under review, I apply no repairs,
I perform no fix-verification, I license nothing, I advance no pipeline. The only writes from this lane
are this review file and the single LOG-4793 research-log entry recording it.

---

## §0 — Independence and log-number note

- **Independence confirmed.** Both artifacts were authored by the pre-assigned LOG-4790 strategy worker
  (verified in the LOG-4790 entry at the tail of `reports/research_log.md`, which describes that lane
  authoring the worth-it gate and the DRAFT pre-reg). I am a different lane; I authored neither file.
- **Log-number collisions and repair (two).** My pre-assigned number was LOG-4791. On max-verification,
  LOG-4791 was already occupied — by a CEO incident entry ("strategy-review bookkeeping breach +
  cron dispatch-authority fix", 2026-09-30) appended after my dispatch. My LOG-4792 append then raced a
  sibling CEO-pre-assigned LOG-4792 review lane — a duplicate dispatch of the same review (both lanes
  verified 4791 as max). Per append-only continuity discipline (LOG-083/LOG-087 collision → repaired as
  LOG-093), this review takes the next free number **LOG-4793** (the later append); the sibling's LOG-4792
  entry is untouched, as is every other entry. Note: per its log entry, the sibling review independently
  converged on SIGN-WITH-FIXES with the same headline defects (norm-shortfall, tiling gap, arm-count
  mismatch) — convergent verification — and additionally flags two defects this review did not catch
  (ĉ-gate stated unconditionally in §0/§4 but conjunctively in §2; rank-trend defined twice, differently).
  Those are the sibling lane's findings, reported here secondhand for the author's repair pass.
- The CEO incident entry corroborates the independence check: it records the LOG-4790 worker performing
  the wave inline ($0 CPU, draft-only, no experiment number, no execution licensed) and the work product
  standing. The bookkeeping defect it records does not touch the artifacts under review.

## §1 — Artifacts reviewed (read in full)

1. `research/prereg/EXP_PREREG_GEOSTEER_MULTISTEP_2026-09-30.md` — DRAFT pre-registration for a CPU pilot
   of geodesic multistep steering (K = 5, sphere retraction + parallel transport) along EXP131's TGA v̂₁
   direction on frozen Pythia-410m (Δθ=0, LOG-331 pin), total norm budget pinned at B = 0.50578119.
2. `research/strategy/GEOSTEER_MULTISTEP_WORTHIT_2026-09-30.md` — Law-#15 worth-it gate for the same pilot.
3. `~/workspace/SCBI/AGENTS.md` house rules (read per runtime note before working in the tree).

**Citation spot-checks** (Law #2 — all traced in `reports/research_log.md`, none re-derived):
B = 0.50578119 and ĉ = 0.03741576759203537 from LOG-4766 (EXP131 binding KILL); LOG-331 pin
`ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed` (log lines 4872/9126/9613);
GEOSTEER (arXiv:2609.10658) identity + licensed-escalation-instrument status from LOG-4751;
GeoSteer cull, program map NEUTRAL, label-assisted, at line ~7637; EXP095 dose kill at LOG-4400;
EXP130 Law #14 REJECT (generation-channel tripwire) at LOG-4721.

---

## §2 — Adversarial checklist findings

### C1 — Decision-table completeness and KILL-first precedence

- The matched-budget null (ΔM_geo = 0 **AND** mean ĉ_geo < 0.1 **AND** McNemar(geodesic v̂₁ vs base) n.s.)
  routes honestly to instrument-level KILL with **no rescue path**: "the dynamical intervention story closes
  at the instrument level... no targeting claim over TGA dynamics is ever licensed." KILL-first precedence
  is stated twice (§2: "The KILL branches are evaluated first"; §4: "First firing verdict wins; KILL branches
  precede CONTINUE bars"). The PIVOT branch requires a distinct positive measurement (midpoint ĉ ≥ 0.1 on
  k ∈ {2,3}) and §4 orders the endpoint-ĉ KILL gate *before* the midpoint-PIVOT check — a null cannot be
  rescued into a PIVOT.
- **GAP — BLOCKING B2 (below): the tiling is not gapless.** Two outcome cells fire no branch:
  (a) ΔM_geo = 0, McNemar n.s., mean ĉ_geo ≥ 0.1, all midpoint ĉ < 0.1;
  (b) ΔM_geo > 0, McNemar n.s., ĉ_geo ≥ 0.1 (e.g. 1–4 flips on 10 pairs).
  In (a), row 1 fails on the ĉ conjunct and the PIVOT row fails on the midpoint conjunct. In (b), no KILL row
  fires (ΔM ≠ 0 defeats row 1; the path-noise row needs a matched random path that also moved) and no
  CONTINUE/PIVOT conjunct is met. Under the falsification constitution an unregistered outcome is a defect;
  cell (b) is a plausible near-miss a future lane could exploit as ambiguity.

### C2 — Licensed-question fit

- **EXP131's KILL bounds the lane; the escalation is genuinely a new instrument class.** LOG-4766 binds the
  one-shot v₁ hypothesis (ĉ = 0.0374 < 0.1, ΔM = 0, 11 arms). The draft escalates strictly to the
  LOG-4751-named instrument class — path geometry (geodesic multistep) at *fixed* total norm B. It is not a
  dose tweak in disguise: every arm spends exactly B = 0.50578119; the only degree of freedom is the path.
- **EXP095's dose kill (LOG-4400) is respected.** B is a registered constant; breaking point (d)/(b) voids
  the apparatus on any budget increase. No "bigger α" resurrection is licensable through this design.
- **EXP130's REJECT (LOG-4721) is respected.** The pilot is decision-readout only — the registered H1/H6 §3.3
  cosine decision statistic, verbatim; any generation-channel touch (logit channel, generation, decode probe)
  → RUN-INVALID (breaking point (g)/(e)). No tripwire contact.
- **The line-7637 cull is respected.** No labels, no trained head, no learned objective, no capability claim.
  The draft borrows only GEOSTEER's Riemannian path mechanics along the already-pinned v̂₁; the worth-it
  gate's seventh item states the cull boundary explicitly and the design stays inside it.

### C3 — Norm-budget audit discipline

- **BLOCKING B1 (below): the [FACT] in §3.4 is mathematically false, and the audit band is self-defeating.**
  Details in §3.
- The budget-identity conjunct is sound: B = 0.50578119 is copied verbatim from LOG-4766 (Law #2 — not
  recomputed as a new number) while the executor independently recomputes 0.01 × median ‖y_{20,last}‖ per
  the EXP129 FIX-2 rule and asserts equality within 1e-6 relative as an apparatus guard (mismatch →
  apparatus-void, bench/backbone drift). Register-constant + verify-apparatus is the correct pattern; the
  apparent "copied, NOT recomputed" vs "independently recomputes" tension resolves as registration vs guard.

### C4 — Registered bars: statistically coherent, consistent with EXP131

- McNemar one-sided p ≤ 0.05 (geodesic v̂₁ vs base) with ΔM_geo > 0; ĉ_geo < 0.1 → KILL (EXP127 §8 via
  EXP131 §4); rank-trend gate (margin-displacement v̂₁ ≥ v̂₂ on ≥ 8/10 prompts; flat/inverted → KILL);
  best-random-path null (the "best of 2" selection rule is registered before inspection — legitimate, not
  cherry-picking); B_agg-path null control (any move → RUN-INVALID, apparatus drift). All coherent and
  consistent with EXP131's licensed quantities.
- The McNemar reference is CPU-to-CPU: the one-shot arm is re-measured on CPU, never GPU-imported. Correct —
  no cross-device contamination.
- Note (not a defect): with 10 pairs the positive bar effectively requires ≥ 5/10 flips — conservative,
  pre-registered, statistically coherent.

### C5 — Mathematical claims: construction well-defined; one hidden defect (B1)

- K = 5 sphere retraction + sequential parallel transport is well-defined and $0-CPU-implementable on the
  pinned backbone: the radial retraction x ↦ x·(‖x₀‖/‖x‖) is closed-form and deterministic; parallel transport
  is defined stepwise along the construction path as rotation in span{x_k, Π_k(u)} — correct for the
  great-circle arc, since x_{k+1} = s(x_k + t_k) ∈ span{x_k, t_k} and t_k ∥ Π_k(u). No finite differences
  (breaking point (c) guards this, EXP128 constraint); no differentiability hazard (operations smooth away
  from antipodal points; ε = α/r = 0.002 keeps the path far from antipodal); transport path-dependence is
  not a hidden assumption — the transport is defined along the construction path itself, deterministically.
- The worth-it Q4 linearization accounting — K steps × O((B/K)²) = O(B²/K) second-order error, a factor-K
  reduction vs the one-shot O(B²) — is correct Taylor-remainder bookkeeping. The H₁/H₀ quantitative
  predictions are registered.
- **The hidden defect is the norm shortfall (B1):** the retraction does not preserve per-step displacement
  norm, and the draft's "exact by construction" claim is false.

### C6 — Law #2 / #3 / #9 / #11

- **Law #2:** every number traces to a cited log record (see §1 spot-checks). No invented numbers. The draft
  does not re-verify the arXiv paper's empirical claims — correctly, per scope — but see B3 on tagging.
- **Law #3 — BLOCKING B3 (below):** the worth-it gate presents GEOSTEER's reported empirical dominance claim
  as "**Theorem (licensed, in-log)**". It is not a [THEOREM] (formally proven result); it is a sweep-surfaced
  reported claim whose empirical content is UNVERIFIED by the program — LOG-4751 verified the paper's
  identity and submission date, not its results. The draft's *use* of the claim is correctly scoped
  (Riemannian formalism only; no learned objective — the cull is respected), but the label elevates an
  unverified empirical claim to theorem status.
- **Law #9:** all bars registered before any output is inspected; the per-step ĉ profile is explicitly
  "diagnostic only (not registered, not decision-gated)". No metric-cherry-picking surface.
- **Law #11:** the pre-reg observes the labeling standard ([HYPOTHESIS], [DEFINITION], [FACT], [ASSUMPTION])
  except for B1's false [FACT] and one mislabel (advisory A1).

### C7 — Fence integrity: holds

- §9 fences any GPU-resident stage (K-sweep, larger bench, per-step ĉ profile on GPU) as **founder-gated**,
  explicitly NOT licensed by the draft. The CONTINUE branch permits only *drafting* a GPU follow-up pre-reg
  (paper work, founder-gated) — no GPU contact is licensed, scheduled, or authorized. The worth-it gate
  repeats the fence. Fence holds.

### C8 — Cross-artifact consistency — BLOCKING B4 (below)

- The two artifacts describe **different pilots**. Worth-it Q3: "1 base + 1 one-shot v̂₁ control + 1 geodesic
  endpoint + 2 controls (random-path, B_agg path) = 5 arms → 50 forwards + ~10 ĉ VJPs + optional 2 midpoint
  probes." Pre-reg §3.5: 7 arms (adds the Geodesic v̂₂ endpoint; 2 random-path arms, not 1) → 70 forwards +
  20 endpoint ĉ VJPs + ≤ 20 optional midpoint forwards. The worth-it gate's own Q2 CONTINUE bar requires the
  rank-trend gate, which its Q3 design cannot deliver (no v̂₂ arm exists in it). Both documents must be
  reconciled to a single registered design before any SIGN.

---

## §3 — Verdict: SIGN-WITH-FIXES

### BLOCKING findings (each must be fixed before any Law #14 SIGN)

**B1 — False [FACT] / self-defeating norm-audit band (Law #5, #11).**
- *Location:* pre-reg §3.4 ("[FACT] Each step has exact norm ‖δ_k‖ = α by construction ... total path length
  ∑‖δ_k‖ = B exactly"); pre-reg breaking point (d) (per-step ‖δ_k‖ = B/5 ± 1e-6 relative; total ∑‖δ_k‖ = B
  ± 1e-6 relative; any miss → apparatus-void); worth-it breaking point (b) ("within float32 tolerance").
- *The defect:* for the specified radial retraction, the realized step displacement is
  δ_k = x_{k+1} − x_k with ‖δ_k‖² = (1−s)²‖x₀‖² + s²α², s = ‖x₀‖/√(‖x₀‖²+α²). With the draft's own numbers
  (B = 0.50578119, K = 5, sphere radius r = B/0.01 = 50.578119, α = B/5, ε = α/r = 0.002):
  **‖δ_k‖/α − 1 = −1.4999961e-06** (verified numerically, closed form). The ±1e-6 relative band is exceeded on
  *every* step by a *correct* implementation — the audit apparatus-voids by construction, measuring the
  retraction's geometry instead of the budget. The worth-it doc's "float32 tolerance" fails identically
  (1.5e-6 > float32 eps ≈ 1.19e-7). "∑‖δ_k‖ = B exactly" is false by the same 1.5e-6.
- *Required change:* redefine the audit measurand as the tangent pre-retraction norm ‖t_k‖ = α (exact by
  construction, measurable before retraction) at ±1e-6, **or** register the analytic correction
  (∑‖δ_k‖ = B·(1 − 1.5e-6)) with a widened band (e.g. ±1e-5); correct the [FACT] label (it is false, not a
  fact); align the worth-it doc's tolerance language to the same definition.

**B2 — Decision table not gapless (falsification constitution).**
- *Location:* pre-reg §2 decision table.
- *The defect:* two outcome cells fire no branch — (a) ΔM_geo = 0, McNemar n.s., mean ĉ_geo ≥ 0.1, all
  midpoint ĉ < 0.1; (b) ΔM_geo > 0, McNemar n.s., ĉ_geo ≥ 0.1. Cell (b) is a plausible near-miss that a
  future lane could exploit as ambiguity.
- *Required change:* add an explicit default row — any outcome matching no CONTINUE/PIVOT/RUN-INVALID/void
  conjunct → **KILL** (KILL-first precedence). This closes both cells: no positive bar met → the
  instrument-level kill stands.

**B3 — Unverified empirical claim labeled "Theorem" (Law #3, #11).**
- *Location:* worth-it gate Q4, "**Theorem (licensed, in-log):** GEOSTEER ... strictly dominates one-step
  Euclidean baselines...".
- *The defect:* GEOSTEER's dominance result is a sweep-surfaced *reported* empirical claim; only the paper's
  identity/submission was verified in-log (LOG-4751), not its results. Labeling it a [THEOREM] (formally
  proven result) violates Law #11 and the Law #3 UNVERIFIED-tagging rule.
- *Required change:* relabel as a sweep-surfaced reported claim tagged **UNVERIFIED**; reserve "licensed" for
  the instrument-class license granted by LOG-4751, not for the empirical claim. (The draft's *use* of the
  claim — Riemannian formalism only, no learned objective — is correctly scoped and needs no change.)

**B4 — Cross-artifact design mismatch (5 vs 7 arms).**
- *Location:* worth-it Q3 vs pre-reg §3.5 (arm counts, forward counts, ĉ-VJP counts, midpoint-probe counts).
- *The defect:* worth-it Q3's 5-arm/50-forward design omits the v̂₂ arm and one random-path arm, yet its own
  Q2 CONTINUE bar requires the rank-trend gate the omitted v̂₂ arm delivers. The two documents do not
  describe the same pilot.
- *Required change:* reconcile both documents to a single registered design (recommend the pre-reg's 7-arm
  design — it carries every gate Q2 requires); restate Q3's arm count, forward count (70), ĉ-VJP count (20),
  and midpoint-probe count (≤ 20) to match.

### Advisory notes (non-blocking)

- **A1** — Pre-reg §0(g) tags "Decision-readout only" as [ASSUMPTION]; it is a design constraint/guard, not
  an assumption. Relabel.
- **A2** — Worth-it Q3 "optional 2 midpoint probes" is ambiguous against pre-reg "≤ 20 optional midpoint
  forwards"; resolve in the B4 reconciliation.
- **A3** — The PIVOT-vs-KILL collision precedence (endpoints null + midpoint ĉ ≥ 0.1 + endpoint ĉ < 0.1 →
  KILL, per §4's evaluation order) is sound but stated only in §4; add one precedence sentence to the §2
  table header so the table is self-contained.

---

## §4 — What the drafts get right (for the record)

The licensed-question fit is sound: EXP131's KILL bounds the question, the escalation is a genuine new
instrument class rather than a dose tweak, EXP095's and EXP130's fences and the 7637 cull are all respected,
the GPU fence holds, the KILL-first structure is genuine (the matched-budget null closes the
dynamical-intervention story at the instrument level with no rescue path), and the worth-it gate's honesty
note correctly spends the strong H₀ prior instead of disputing it. None of the blocking findings touches
the scientific question — all four are repairable specification defects. After repair, this design is
SIGN-able.

---

## §5 — Fence confirmation (reviewer lane)

Review only. I edited no reviewed artifact, authored no protocol text, minted no experiment number, licensed
no execution (CPU or GPU), ran no models, touched no weights or signed artifacts (read-only throughout),
made no commits or pushes, spent nothing, published nothing, dispatched no subagent. Lane writes: this
review file and the single LOG-4793 research-log entry. $0 CPU.
