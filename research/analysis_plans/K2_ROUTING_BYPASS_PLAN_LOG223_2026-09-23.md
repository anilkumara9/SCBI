# K2 — Routing-vs-Bypass Discriminator: FROZEN Pre-registration

**LOG-223 · Track-8 pre-registration drafter · 2026-09-23**
**Status:** FROZEN. **DO NOT EXECUTE before Law #14 SIGN (LOG-224, pre-assigned) and CEO GPU clearance.**

---

## 0. Honest headline + ambition bar (LOG-218 double bar)

**Headline [INFERENCE]:** K1 and EXP082 killed both directional tilt stories — the bridge is a relational (t−f) direction that rescues +10pp with no target-boost and no foil-suppression. S3-8 (LOG-222, in flight) is now asking whether that rescue is a pure direct readout shift (residuals ≈ 0) or needs downstream depth (residuals large). **K2 asks the question one level deeper, and it is the last mechanistic question the output-side room can answer:** does the rescue *route through upstream attention computation* — i.e., does any upstream mechanism exist at all — or does it *bypass* attention entirely, riding the final-position residual stream straight into the unembedding?

**Belief-change (ambition bar A1, in writing):** the belief that changes is "the bridge engages upstream computation." If the bypass arm rescues ≥ the entity-position arm (contrast CI excluding a δ_min routing advantage), the output-side *mechanism* program closes — the bridge is logit steering, period — and the P2 pivot fires (mechanism-family → trajectory/closed-loop controllers; the bridge survives only as engineering). If the entity-position arm rescues while the final-token arm is flat, there is a mechanism upstream to hunt — the program earns its first positive mechanism existence claim since the bridge was found, and the attention-engagement measurement campaign (which heads/positions carry the rescue) is licensed. A weak steelman fails the review same as a weak license: the strongest case against this design is boxed in §8, at full strength, answered or conceded.

---

## 1. Knowledge-protocol discharge (what was read)

Read before writing, in order:

1. `research/TEAM_KNOWLEDGE_PROTOCOL.md` §1 (the mandatory reading list; briefing template LOG-218).
2. `research/innovation/PARADIGM_AUDIT_2026-09-23.md` §K2 — the adopted K2 design (§H6 battery): (a) final-token-only vs (b) premise-entity-position injection vs (c) all-positions, 60 items × 3 conditions ≈ 180 passes, CI-for-(ΔM_b − ΔM_a) kill rule, K-ordering semantics (interpretation waits on K1; preparation parallel).
3. `research/innovation/SPRINT3_CANDIDATES_2026-09-23.md` — S3-1..S3-6 candidates (context: ARP's fingerprint program is downstream of a K2 routing verdict; S3-8 seeded from the K1 death-debt).
4. `reports/research_log.md` — LOG-213 (K1-EXONERATED, verbatim: all three runs Not supported, k=0/60, CI [0.0000, 0.0596]; both directional tilts dead per LOG-217/EXP082; **pre-registered consequence: K2 pilot LICENSED**), LOG-218 (top-lab amendment: AMBITION × RIGOR, first principles, quantitative predictions, steelman), LOG-219 (campaign mode; deaths-owe-candidates), LOG-222 (S3-8 dispatched: per-item residual ‖archived end-to-end margin shift − L1-predicted shift‖ ≈ 0 → K2's premise dissolves; large residuals → K2 justified).
5. `research/foundations/MATHEMATICAL_LICENSE_STANDARD_2026-09-23.md` (LOG-200) — the L1–L4 license template, grade rubric (this plan's license self-graded below), §A.6 transition rule.
6. `research/analysis_plans/S37_SPOILER_ANALYSIS_LOG221_2026-09-23.md` §§5–6 — the conceded steelman and the **competitor-logit-drop** reusable readout-side causal endpoint (Δlogit of the baseline's top-1 competitor, bridge vs random-rotation control), attached here as a secondary diagnostic.
7. Primary records: EXP065 results (pythia-160m, L10, α=0.5, bridge +16.67pp b=10 c=0), EXP066 results (pythia-410m, L20, α=0.5, bridge +13.33pp b=8 c=0), EXP077 official (pythia-410m/L20, C8 bridge = EXP066 `make_bridge_vec` verbatim at α=0.5, +10pp b=6 c=0), EXP065 runner line 423 (`h + alpha_val * v_vec` broadcast over all positions at the target layer module), EXP077 instance records schema (`item`, `ent`, `typ`, `correct`, `rescue_indicators`, 60 items).

**One challenge (knowledge protocol §2):** this plan carries two run-pins (160m/L10 and 410m/L20) with different archived b_mean vectors. If the pins diverge — e.g., routing at 160m/L10 but bypass at 410m/L20 — the program-level aggregation rule (§7) must record Inconclusive and treat the divergence as an [OBSERVATION] about layer-dependence, not let the cleaner-looking pin quietly dominate the verdict. Pin-divergence must never be adjudicated by aesthetics.

**One idea:** the §5 positional-confinement lemma's converse is a reusable instrument, not a one-off: *any* future intervention claim can be position-ablated to test attention-mediation. Together with S3-7's competitor-logit-drop, K2 adds a second entry to the program's growing "reusable adjudication endpoints" shelf — position-ablation for routing, competitor-logit-drop for suppression-vs-promotion.

---

## 2. Rationale, premises, and the S3-8 dependency

**[FACT]:** K1-EXONERATED (LOG-213) — not one of 180 bridge directions reaches the 0.9 target-row bar; the bridge is a relational (t−f) direction, not a target boost. EXP082-EXONERATED (LOG-217) — foil-suppression Not supported on every run (k_f = 0/60); the bridge is neither target-directed nor foil-directed on any item of any run — yet rescues +10pp. The static directional-readout story is dead.

**[INFERENCE]:** what remains is exactly two accounts of the rescue:
- **(i) Bypass:** the injected direction rides the final-position residual stream into the unembedding with no attention mediation — direct logit steering.
- **(ii) Routing:** the injected direction is transported and transformed by downstream attention computation before it moves the decision — a mechanism exists upstream.

**S3-8 dependency [HYPOTHESIS, recorded]:** LOG-222 is testing per-item whether the rescue is fully explained by the direct L1 readout shift. **K2's premise depends on its outcome:** if S3-8 finds residuals ≈ 0 (pure readout-side), K2's routing question dissolves — there is no depth-mediated effect to route through, and K2 should not spend its GPU minutes (CEO re-evaluates this plan's license). If residuals are large, K2 is the right next discriminator. This plan is FROZEN now; its *interpretation* waits on LOG-222 exactly as §H6 interpretation once waited on K1.

**Law #15 Q1 (recorded):** does the bridge's rescue route through upstream attention computation (routing) or bypass it via the final-position residual→unembedding path (bypass)?

**Law #15 Q2 (decision changed):** CONTINUE both ways, with pre-named consequences — bypass Supported → P2 pivot fires (output-side mechanism program closes; bridge demoted to engineering; mechanism-family → trajectory/closed-loop controllers); routing Supported → upstream mechanism hunt licensed (attention-engagement campaign, CLLC routing-signal pilot); Inconclusive → HOLD (question open; instrumentation upgrade + powered re-registration are the options, not silent culling); Underdetermined → fix cause, re-run under a new LOG. S3-8-resolved-before-execution: if residuals ≈ 0, this plan's premise is dissolved and the CEO stands it down rather than executing a question nobody needs answered.

**Law #15 Q3 (cheapest; costed exactly):** 180 forward passes on the primary pin (60 items × 3 arms; baseline correctness from archived official records — no re-baselining passes). The mechanism question (does the rescue route through attention?) cannot be answered from CPU/archived data: the archive holds only all-position bridge runs, so position-ablation is not deducible without live passes. Everything else — runner build, bridge-identity check (cosine vs archived vectors), entity-position mapping feasibility, CI/MDE arithmetic, this document — is CPU/$0. Secondary pin (160m/L10) +180 passes = 360 total, pre-registered as a conditional replication (see §4). At the program-measured 22 fwd/s (2×T4), 180 passes ≈ 8.2 s ≈ 0.002 T4-h; 360 ≈ 16 s ≈ 0.005 T4-h. The budget is passes, not hours; the adopted ~180-pass budget fits the primary pin exactly.

**Law #15 Q4:** the Mathematical License, §5.

---

## 3. Design

### 3.1 Run pins (frozen; no new experiment number — K2 is a kill-battery probe, not a new EXP)

| Pin | Model | Target layer | α | Bridge vector | Benchmark items | Bridge rescue (archived) |
|---|---|---|---|---|---|---|
| **K2-P (primary)** | `EleutherAI/pythia-410m` | L20 | 0.5 | per-item archived b_mean = normalize(E[target]−E[foil]) (EXP077 C8 = EXP066 `make_bridge_vec` verbatim) | EXP077 official 60 items (`exp077_instance_records.json`) | +10.00pp, b=6, c=0, p=0.03125 |
| **K2-S (secondary, conditional)** | `EleutherAI/pythia-160m` | L10 | 0.5 | per-item archived b_mean (EXP065) | EXP065 60 items | +16.67pp, b=10, c=0 |

K2-S runs only after K2-P's verdict **and** CEO GPU clearance; it is the layer/model replication. EXP070 is excluded (Underdetermined, mirror-pending — per task guard).

### 3.2 Arms (per pin)

All arms: frozen model, hook at the target layer's output (same hook site as the archived runs), per-position masked additive injection of α·b̂; decision read at the final token exactly as the archived runs (argmax over {target, foil} logits).

- **(a) FINAL-ONLY:** inject only at the final sequence position. **License:** the §5 positional-confinement lemma — this perturbation cannot reach any other position via attention (causal mask: no position attends to the future), so any rescue is attention-free readout bypass. The pure bypass probe.
- **(b) ENTITY-ONLY:** inject only at the premise-entity token positions (head/tail entity strings from the item record, mapped to token positions with the pinned tokenizer before any GPU pass; multi-token entities → all their tokens; mapping recorded per item — see guard G7). **License:** no residual-stream shortcut exists from these causally-upstream positions to the final position; any effect on the decision MUST travel via attention computations at layers > l*. A rescue here = routing through attention.
- **(c) ALL-POSITIONS:** the archived construction verbatim (broadcast over all positions). **Positive control:** reproduces the historical rescue; validates that the benchmark still has headroom and the bridge vector is intact. FATAL gate if it fails (guard G5).

**Baseline:** archived official baseline correctness per item (EXP077 C1 official; EXP065 baseline) — no new baseline passes.

### 3.3 Pass count (exact)

Per pin: 60 items × 3 arms = **180 forward passes**. K2-P alone = 180 (within the adopted ~180 budget). K2-P + K2-S = 360. Logit archiving (top-5 tokens + ids + logits per arm per item; §3.6) adds zero forward passes — logits are already computed.

### 3.4 Primary endpoint (mirror of §H6; no silent shifts per Law #4)

Δ̂M_b − Δ̂M_a, where Δ̂M_arm = (b_arm − c_arm)/60 vs the archived baseline, with the **exact two-sided 95% CI for the difference of two paired proportions** (arm outcomes are paired on the same 60 items — the contrast is P_b(right) − P_a(right) on one paired sample; Tango's exact interval). Verdict bars per the binding §G1b protocol, δ_min = 0.05:

- **Routing Supported / bypass Not supported:** L(Δ̂M_b − Δ̂M_a) > 0.05 AND b_b ≥ 6 (L1 MDE at c=0) AND U(Δ̂M_a) < 0.05 (the bypass channel demonstrably flat).
- **Bypass Supported / routing Not supported:** Δ̂M_a ≥ Δ̂M_b AND U(Δ̂M_b − Δ̂M_a) < 0.05 (rules out a δ_min advantage of (b) over (a)) AND b_a ≥ 6 (the rescue is actually present, not a degenerate both-null).

Per-arm diagnostics (reported, never verdict-bearing alone): McNemar exact p and exact 95% CI for each arm's Δ̂M.

### 3.5 Kill bars (recomputed arithmetic)

N=60 per pin. L1 MDE at c=0: b ≥ 6 (2⁶=64 → p=0.03125 ≤ 0.05) = 10pp — the minimum present rescue. The contrast CI's exact width depends on the joint discordant table; worst-case MDE is bounded by the per-arm MDE (10pp); failure of the contrast CI to clear δ_min → **Inconclusive (held, never culled)** — a straddle is a power statement, not a bypass verdict. This is the LOG-218 §F2 discipline: p ≥ 0.05 alone never fires a falsifier.

### 3.6 Secondary diagnostic endpoint (S3-7's reusable endpoint; verdict-discipline)

**Competitor-logit-drop** (S3-7 §5.6 conceded steelman, §6 instrumentation spec): on items where the baseline is wrong and the arm is right (rescued), record Δlogit of the *baseline's top-1 competitor token* under the arm vs under a random-rotation control (EXP066's `Random_Rotation_Seed_0–4` control family, 1 seed pre-registered). Competitive suppression predicts competitor-specific demotion beyond the control; re-routing predicts target promotion without competitor demotion.

**Scope discipline:** this endpoint discriminates *suppression from promotion within an arm* — it does NOT discriminate routing from bypass (both accounts are compatible with either logit pattern). It is therefore a recorded **[OBSERVATION]-only diagnostic**: it never fires the primary kill, never appears in the verdict table, and is offered to the Law #14 reviewer as a candidate future endpoint, not forced into K2's verdict space. Cost: zero extra forward passes (top-5 logits archived during the budgeted passes); the random-rotation control adds one 60-pass arm — pre-registered as part of the diagnostic (241→ wait: 60 × 4 = 240 passes per pin). **Corrected count:** 60 items × 4 conditions {(a), (b), (c), (d) random-rotation control} = **240 passes per pin**; K2-P = 240 (1.33× the adopted ~180 budget — flagged honestly; the diagnostic control is what pushes past 180); K2-P+K2-S = 480. The Law #14 reviewer may cut the (d) arm to hold the 180 budget; the primary verdict is unchanged either way (pre-registered).

### 3.7 Assumptions discharged at design time

- Decision position = final token [FACT — all corpus runs read logits at `logits[0, -1, :]`].
- Injection site = target-layer output module, same as archived runs [FACT — EXP065 runner ll. 423–430; EXP077 §2].
- Entity positions locatable pre-GPU with the pinned tokenizer [ASSUMPTION — feasibility checked CPU-first; mapping failures recorded per item, items with unmappable entities excluded → counts toward Underdetermined accounting].

---

## 4. Guards (FATAL unless marked diagnostic)

- **G1 bridge-identity:** per item, cos(b_K2, b_archived-pin) ≥ 1 − 1e-6 AND ‖b‖ equals the archived injection norm (relative error ≤ 1e-5). Any item failing → item excluded, recorded; ≥3 failures → run INVALID.
- **G2 label cross-check:** the target/foil option tokens used per item must match the benchmark's recorded target/foil exactly; mismatch → item excluded.
- **G3 Δθ=0:** sha256 of model state_dict pre-run == post-run; mismatch → FATAL, results not reported.
- **G4 no-forward-pass-except-licensed:** executor counts passes; K2-P must be exactly 240 (180 if the Law #14 reviewer cuts (d)); K2-S exactly the same; overrun → INVALID.
- **G5 (c)-reproduction gate:** b_c ≥ 6 (L1 MDE) else the run is INVALID → verdict Underdetermined with cause recorded (benchmark or vector broken; routing question unaskable).
- **G6 EXP070 excluded:** no EXP070 records, artifacts, or vectors used anywhere.
- **G7 Law #7 provenance note:** the bridge is the archived label-informed vector (normalize(E[target]−E[foil])) used *as a mechanistic probe*. K2 probes where the rescue travels; it draws no autonomous-mechanism claim from the label-informed construction — that question is K3's, untouched here.
- **G8 entity-mapping:** position masks logged per item (token ids + strings); multi-token handling pre-registered (§3.2); unmappable → item excluded, recorded.
- **G9 LayerNorm-scale diagnostic (steelman-4 check, diagnostic not a gate):** per-position residual norms at the final layer recorded for (a)/(b); if the (b)/(a) final-layer norm ratio diverges from the injection-norm ratio by >2×, the divergence is recorded as an [OBSERVATION] (covariate, never a post-hoc gate).

---

## 5. Mathematical License (binding — Law #15 Q4; see research/foundations/MATHEMATICAL_LICENSE_STANDARD_2026-09-23.md)

**License grade:** IN-HOUSE-PROOF (positional-confinement lemma: elementary proof from the causal mask, complete, but not yet through adversarial review — sufficient for the cheapest discriminating experiment, not for a full-budget run) / IN-HOUSE-PROOF (bridge construction identity, LOG-197 two-link chain E1+E2).

### L1. Authorizing result

- **Statement (exact) — the positional-confinement lemma [PROPOSITION]:** Let M be a causal (left-to-right masked) decoder transformer with per-position residual streams and additive intervention δ applied to the layer-l* output at a set of positions P. Then: (i) for all layers l > l* and all positions j < min(P), the activation at (l, j) equals the unintervened activation (proof: by induction, position j attends only to positions ≤ j, so δ at positions ≥ min(P) is never in its receptive field); (ii) if P = {p_last} (final position only), δ influences the output logits *only* through the final-position residual path to the unembedding — attention-mediated transport to any other position is impossible because no position j > p_last exists; (iii) if P ⊆ {positions < p_last}, δ can influence the final-token logits *only* through attention computations at layers l > l* (queries at positions > p attending to keys at p) — attention is the only inter-position channel in the frozen architecture (LayerNorm and MLPs are per-position operators [FACT]).
- **Source:** in-house proof (elementary induction on the causal mask; M4 space/shape checks trivial — positions and layers are the objects). Proof document to be attached at Law #14 review; the K2 run is graded as the license's empirical exercise, not its proof.
- **Epistemic label:** [PROPOSITION] (→ [THEOREM] after Law #14 adversarial review of the proof).
- **Companion identity [PROPOSITION]:** b_archived = α·normalize(E[t]−E[f]) per item (LOG-197 E1+E2 chain); discharged per guard G1.

### L2. Quantitative prediction for the primary endpoint

- **Endpoint:** Δ̂M_b − Δ̂M_a with Tango exact two-sided 95% CI (§3.4).
- **Prediction — direction:** under bypass, Δ̂M_a ≥ Δ̂M_b — the final-position injection sits maximally coupled to the unembedding (direct residual path); attention-mediated transport from entity positions can only dilute the direction (attention weights ≤ 1, mixing across 12 downstream layers at L20). Under routing, Δ̂M_b − Δ̂M_a > 0 with Δ̂M_a ≈ 0 — the readout path alone cannot rescue; the rescue requires attention transport.
- **Prediction — magnitude (anchored, not invented):** historical all-position rescues: +16.67pp (EXP065), +13.33pp (EXP066), +10.00pp (EXP077 official). Under bypass: Δ̂M_a ≥ Δ̂M_b with Δ̂M_a expected within-or-above the historical band (arm (a) ⊆ arm (c)'s positions; the readout coupling is maximal) — pre-registered anchor Δ̂M_a ≥ +10pp (the L1 MDE boundary), Δ̂M_b ≥ 0. Under routing: Δ̂M_b − Δ̂M_a clearing +0.05 with Δ̂M_a ≈ 0 (U(Δ̂M_a) < 0.05). **Conceded uncertainty:** the position-restricted arms have no historical precedent — the (c) arm quantifies the restriction cost (Δ̂M_(c) − Δ̂M_b = dilution penalty, recorded).
- **Derivation:** direction follows from L1 (i)–(iii) + attention-weight bound; magnitude anchored to the three archived rescues; coverage: all 60 items per pin; tolerance: the exact CI.

### L3. Breaking point

- **Falsifying the bypass account:** L(Δ̂M_b − Δ̂M_a) > 0.05 with Δ̂M_a flat — routing demonstrably adds what the pure readout path cannot. Decision: CONTINUE (upstream mechanism hunt licensed; §2 consequences).
- **Falsifying the routing account:** U(Δ̂M_b − Δ̂M_a) < 0.05 with Δ̂M_a ≥ Δ̂M_b and b_a ≥ 6 — no routing advantage survives the CI. Decision: CONTINUE (P2 pivot fires; output-side mechanism program closes).
- **Breaking the license's application premise:** (c) fails guard G5 (the bridge does not survive position restriction at all) → neither account is tested → Inconclusive, never a verdict on either proposition (Charter M5.2 partition honored).
- **Outcome partition:** the §7 table maps every cell — routing-Supported / bypass-Supported / routing-Refuted (narrow, §7) / Inconclusive / Underdetermined — to a verdict and a consequence; no cell defers to executor discretion.

### L4. Assumption inventory

- **A1:** the causal-mask induction holds for the frozen architecture (no bidirectional leakage) — discharge: architectural [FACT] for GPT-NeoX-style decoders; verified by the hook-site read in the archived runners.
- **A2:** bridge identity = archived construction (guard G1 discharges per item; promotion path: Law #14 review of this plan).
- **A3:** entity-position mapping correct (guard G8; unmappable items excluded, counted).
- **A4:** LayerNorm re-normalization does not invert the (a)/(b) coupling asymmetry (diagnostic G9 records the check; no verdict rides on it).
- **A5:** Δθ=0 (guard G3 — FATAL on violation).
- **A6:** dilution by attention across 12 downstream layers does not wash a real routing effect below the 10pp L1 MDE while leaving the (c) arm intact — **conceded as the license's load-bearing risk** (see §8 steelman-1; the honest response is the Inconclusive partition, not a stronger claim).
- **Promotion path:** the lemma to [THEOREM] via Law #14 adversarial review of the standalone proof (LOG-224 scope); the causal upshot of any K2 verdict stays at mechanism-adjudication (L1), never a capability claim.

---

## 6. Verdict table (exhaustive; five categories only)

Pin-level verdicts (K2-P first; K2-S conditional):

| # | Observation (per pin) | Verdict: routing | Verdict: bypass | Consequence |
|---|---|---|---|---|
| 1 | L(Δ̂M_b−Δ̂M_a) > 0.05, b_b ≥ 6, U(Δ̂M_a) < 0.05 | **Supported** | **Not supported** | Upstream mechanism exists. License: attention-engagement campaign (which heads/positions carry the rescue); CLLC routing-signal pilot; ARP (S3-1) fingerprint program unblocked with a verified positive mechanism class. |
| 2 | U(Δ̂M_b−Δ̂M_a) < 0.05, Δ̂M_a ≥ Δ̂M_b, b_a ≥ 6 | **Not supported** | **Supported** | P2 pivot fires: output-side mechanism program closes (bridge = logit steering, period); mechanism-family → trajectory/closed-loop controllers; bridge survives only as engineering. |
| 2r | Cell 2 holds AND L(Δ̂M_a) > 0.05 AND b_b = c_b = 0 | **Refuted** | **Supported** | As cell 2, with the routing account actively contradicted (flat-zero under the only channel it could use) — Law #8: the routing reading stays dead unless new evidence resurrects it. |
| 3 | Contrast CI straddles (neither bar clears) | **Inconclusive** | **Inconclusive** | HELD, never culled. Options: instrumentation upgrade (per-layer attention snapshots per S3-7 §6 spec) + powered re-registration at N≥100 (B2: N=100 → L2 MDE 9.0pp); or concede the pilot's ceiling. |
| 4 | Both arms flat (b=0) with (c) passing G5 | **Inconclusive** | **Inconclusive** | The bridge does not survive position restriction at all — the license's application premise broke (L3), not either proposition. Logged; K2's question is unaskable in this form. |
| 5 | Any FATAL guard fails / records missing | **Underdetermined** | **Underdetermined** | Fix cause; re-run under a new LOG. Nothing is filled by assumption. |

**Program-level aggregation:** both pins in the same cell → program verdict inherits the cell. Any pin divergence → **Inconclusive** program-level, with the divergence recorded as an [OBSERVATION] (layer-dependence hypothesis stays queued; the §1 challenge applies).

**Secondary diagnostic (§3.6) verdict discipline:** recorded as [OBSERVATION] only; it can *suggest* a follow-up pre-registration (suppression-vs-promotion dispute) but fires no kill and appears in no row above. Banned verdict language absent throughout.

---

## 7. Consequences and ordering (pre-registered)

- K2-P executes only after: (i) Law #14 SIGN (LOG-224), (ii) CEO GPU clearance, (iii) LOG-222 (S3-8) verdict — if residuals ≈ 0, the CEO re-evaluates this plan's license before any pass is spent (§2 dependency).
- K2-S executes only after K2-P's verdict + fresh CEO GPU clearance.
- K3's CPU construction audit proceeds in parallel (ordering is binding on interpretation, not preparation — §H6).
- EXP080/081 remain gated on the Law #7 audit + CEO GPU clearance (unchanged).

---

## 8. Steelman box (the strongest case against this design, at full strength)

**Steelman 1 — propagation washout (power, not evidence).** Injection at L20 leaves 12 downstream layers of attention mixing before the readout. Even if the rescue genuinely routes through attention, the entity-position signal is diluted by attention weights at every layer — a real routing effect could shrink below the 10pp L1 MDE while the final-token arm, sitting on the readout path, rescues cleanly. The design would then return "bypass Supported" for a routing world. **Answered in part, conceded in part:** the honest response is structural — any contrast-CI straddle lands in the Inconclusive cell (held, never a bypass verdict), and the (c) arm measures the restriction cost directly (Δ̂M_(c) − Δ̂M_b). But the asymmetry is real and conceded: this pilot has more power to confirm bypass than to confirm routing, because bypass's predicted pattern (a clean, maximal (a) rescue) is easier to see than routing's (a diluted (b) rescue beating a flat (a)). The Law #14 reviewer should treat a cell-2 verdict as provisional-pending-replication and a cell-3 as the modal honest outcome.

**Steelman 2 — position non-comparability (norm confound).** Arms (a), (b), (c) inject at 1, k, and T positions respectively — total injected norm differs across arms. A critic argues the contrast measures total norm, not position. **Answered:** the licensed comparison is (b) vs (a), and under bypass (a) should dominate *regardless* of norm — it is exactly on the readout path with maximal unembedding coupling, while any attention-mediated transport from (b) can only attenuate. Total-norm arguments predict (c) > everything, which the (c) arm checks directly. Per-position α is held fixed (matching the archived broadcast semantics), and per-arm norms are recorded. The residual asymmetry favoring bypass on power grounds is conceded (see steelman-1's conclusion).

**Steelman 3 — the contrast needs depth that static injection already killed.** Five static-geometry families are decision-flat at L20; one could argue any upstream-position intervention is a priori dead and K2 is theory preservation dressed as a discriminator. **Answered:** those kills are narrowly licensed to *unconditional static-geometry variants of the contrast direction* — the bridge is not a contrast direction (EXP078: median projected bridge energy 0.0544 < 0.10, ENERGY_GATE_HALT — the bridge lives outside the dead room), and the bridge demonstrably rescues (+10pp official). K2 tests the rescuing vector, not the dead family. The steelman fails on the license scope.

**Steelman 4 — LayerNorm re-normalization asymmetry (conceded).** Adding a vector at one position vs many changes local LayerNorm statistics; re-normalization could attenuate (a) and (b) differently, making the contrast partly a normalization artifact. **Conceded:** diagnostic guard G9 records per-position final-layer residual norms for (a)/(b); if the (b)/(a) norm ratio diverges from the injection-norm ratio by >2×, it is recorded as an [OBSERVATION] and the verdict is read with that caveat. It is deliberately not a gate — a post-hoc gate would be Law #4-adjacent.

**Steelman 5 — the competitor-logit-drop diagnostic smuggles a second mechanism question into K2.** **Answered by scope discipline:** §3.6 keeps it [OBSERVATION]-only with no verdict cell, no kill, and no consequence row. If the reviewer judges even that too much scope, the (d) arm is cut and K2-P returns to exactly 180 passes.

---

## 9. First-principles check (LOG-218 §2)

No authority is invoked without reduction: the design's authorization is the causal-mask lemma (§5 L1) — an induction on the attention mask, not "the literature suggests." The bridge's empirical anchors are program-measured rescues, not field analogies. The S3-7 endpoint is included on its conceded causal logic (competitor demotion vs target promotion), not on S3-7's authority. Where the math runs out (dilution magnitude, LayerNorm behavior), the plan says so (§5 A6, §8 steelmen 1/4) instead of borrowing confidence.

---

## 10. Execution release checklist (for the LOG-224 reviewer)

- [ ] L1–L4 license section graded ≥ CONJECTURE-UNDER-TEST (self-grade IN-HOUSE-PROOF; verify the lemma proof document).
- [ ] Kill bars recomputed from primary sources (MDE 6/60 at c=0; δ_min=0.05 inheritance disclosed).
- [ ] Verdict table exhaustiveness (every contrast-CI × per-arm cell lands in exactly one row; Charter M5.2).
- [ ] Law #15 Q1–Q4 on record (§2, §5).
- [ ] Steelman graded (a weak steelman fails the review same as a weak license).
- [ ] Pass-count exactness (240/pin with (d); 180/pin without) and the S3-8 dependency noted as a pre-execution CEO re-check.
- [ ] EXP070 excluded; EXP065/066/077/EXP082 numbers used verbatim (no invented figures).

---

**DO NOT EXECUTE before Law #14 SIGN (LOG-224, pre-assigned) and CEO GPU clearance.**
