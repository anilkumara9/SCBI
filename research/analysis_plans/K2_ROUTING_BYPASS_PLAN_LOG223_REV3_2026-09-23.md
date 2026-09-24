# K2 — Routing-vs-Bypass Discriminator: REV3 Pre-registration

**LOG-223 · Track-8 pre-registration drafter · 2026-09-23 · REV3**
**Status:** FROZEN (revision of frozen LOG-223 plan; the frozen original, REV1, and REV2 are untouched).
**Revised under:** Law #14 ruling **LOG-227** (2026-09-23) — D1 repair, option (a): the row-1 flatness conjunct becomes the one-sided 95% Tango upper bound.
**Targeted re-check:** LOG-228 (pre-assigned) — revised text only.
**DO NOT EXECUTE before Law #14 SIGN (targeted re-check LOG-228, pre-assigned) and CEO GPU clearance.**

---

## REV3 changelog (what changed vs REV2 — nothing else moved)

**Revision record [FACT]:** REV3 implements the Law #14 LOG-227 ruling on defect D1 (option (a)). No design change beyond the ruling: the ambition bar (belief-change A1) stands exact and unchanged; kill bars L > 0.05 / U < 0.05; δ_min = 0.05 unchanged; the primary contrast stays two-sided 95% Tango per §G1b; the verdict table; pin-divergence → Inconclusive; guards G2–G9; Law #15 four answers; the binding cell-2 reading; §7 provisional-pending-replication; §8's six steelman entries — all stand.

1. **Row-1 flatness repair (option (a), LOG-227).** Row 1's third conjunct (in §3.4 and in the §6 verdict table) becomes **`U_1s(Δ̂M_a) < 0.05`** — the one-sided 95% upper confidence bound for ΔM_a from the Tango (score) interval family (z = 1.6449), the one-directional form of the protocol's per-arm diagnostic CI. The [JUSTIFICATION — LOG-227 repair of D1] block is given verbatim in §3.4. Row 3's observation text is widened to the catch-all (§6) to close the pre-existing exhaustiveness gap the repair makes live.
2. **Seventh steelman (§8).** The significance-shopping objection — one-sided intervals as the classic tool for manufacturing significance — steelmanned at full strength, answered honestly (the LOG-227 bite-check: δ_min unchanged, primary contrast stays two-sided, pre-registered pre-data, b=c=2 fails). The steelman stands or the repair escalates; burying it is not an option.
3. **Gate references updated.** Targeted Law #14 SIGN re-check moves to **LOG-228** (pre-assigned). The §10 checklist names the repaired bar's bundle implementation requirement (implemented in the separate bundle chain: F1 evaluate_k2.py replace-not-supplement, F2 six new evaluator tests incl. row-3 catch-all, F3 BUILD_NOTES + manifest hashes).
4. **Law #4 compliance statement** recorded in §3.4: pre-execution repair; hypothesis, question, δ_min, and contrast endpoint unchanged; the two-sided bar was an instrument-specification error; documented as a new revision per "design changes take a new number." C1–C3 satisfied [FACT, LOG-227].

---

## REV2 changelog (what changed vs REV1 — nothing else moved)

**Revision record [FACT]:** REV2 implements the four LOG-224b text-only fixes (F1–F4). No design change: the ambition bar (belief-change A1) stands exact and unchanged; kill bars L > 0.05 / U < 0.05; the verdict table; pin-divergence → Inconclusive; guards G2–G9; Law #15 four answers; the binding cell-2 reading; §7 provisional-pending-replication; §8's six steelman entries at full strength — all stand.

1. **F1 (vector identity + retraction).** The LOG-224b retraction is applied to the plan record: REV1's four per-item-archive claims (§0 changelog item 1, §1 item 5, §3.1 K2-P bridge-vector cell, §5-L1 companion identity) are corrected. `exp077_vectors.pt` holds **18 tensors only** (`v_hat`, `v_hat_c`, `mu` 1×1024 each; `v_hats`, `v_hat_c_ks` 5 each; `u_list`, `q_list` 8×1024 each; `r_vec`, `B_wrong`, `B_perp_basis`); **zero per-item C8 vectors exist**; only per-item norms were archived (`exp077_results.json → injection_vector_norms`, all = α=0.5) [FACT, LOG-224b byte-level parse]. The REV1 statement that the LOG-224 reviewer verified per-item vector existence is **retracted** — the LOG-224b reviewer is the first to byte-check the file (misattribution corrected). Guard G1 is rewritten as **construction-identity**: (a) deterministic rebuild of per-item b_K2 = α·normalize(E[t]−E[f]) from pinned model + pinned tokenizer + the in-repo deterministic benchmark construction (`run_exp077.py` §3 constants); (b) per-item norm match vs the run-logged C8 norms (rel. err ≤ 1e-5); (c) per-item target/foil token mapping logged (feeds G2); (d) identity chain = E1+E2 source link (C8 = EXP066 `make_bridge_vec` verbatim, in the runner source) + the EXP077 run-log F1 guard record. Graded [INFERENCE] (deterministic reconstruction), not [FACT]. The norm fingerprint (b) is stated as a **weak identity check** (any unit×α vector passes it); the honest license for K2 vector identity is **deterministic-reconstruction + the live (c)-gate** (guard G5) — implying no archive-grade verification. The K2-S row gets the same honest treatment: EXP065 has no vector archive (`results.json` + `run_log.txt` only); identity via the same construction-identity protocol.
2. **F2 (G10 exclusion floor).** Pre-registered rule: **>6 exclusions (>10%) → the run is Underdetermined** with the exclusion cause recorded; at ≤6 exclusions, the discordant-based bars and the paired contrast CI apply at the **actual N**. The actual N is recorded in the verdict table's accounting (§6).
3. **F3 (steelman-6).** The **"acc 0.5667"** figure for the official bench is **dropped** — unverifiable: no in-repo per-item records for the official bench exist to source it (LOG-224 [FACT]). Steelman-6 stands at full strength without it.
4. **F4 (lemma-proof document).** Standalone proof attached: `research/analysis_plans/K2_CONFINEMENT_LEMMA_PROOF_LOG224c_2026-09-23.md`, graded [PROPOSITION], marked **"DO NOT CITE AS [THEOREM] — requires Law #14 review for [THEOREM] promotion."** Per the LOG-224b ruling, §5 states verbatim: the document is required for the [THEOREM] promotion path, NOT a blocker for pilot SIGN — the inline §5 proof suffices for pilot SIGN.

---

## 0. REV1 changelog (what changed vs the frozen LOG-223 plan — nothing else moved)

1. **Bench pin (CEO decision).** K2-P's 410m pin is pinned to the **EXP077 smoke bench**, not the official bench the frozen plan cited. Exact pinning:
   - Benchmark items + per-item baseline correctness: `experiments/runs/EXP077_cone_vs_line/exp077_instance_records.json` (60 items; `correct` field per item; schema: `item`, `ent`, `typ`, `correct`, `rescue_indicators`).
   - Bridge vectors: **construction-identity** (guard G1) — `experiments/runs/EXP077_cone_vs_line/exp077_vectors.pt` holds **18 tensors only** (`v_hat`, `v_hat_c`, `mu` 1×1024 each; `v_hats`, `v_hat_c_ks` 5 each; `u_list`, `q_list` 8×1024 each; `r_vec`, `B_wrong`, `B_perp_basis`): **zero per-item C8 vectors exist**; only per-item norms were archived (`exp077_results.json → injection_vector_norms`, all = α=0.5) [FACT, LOG-224b]. The REV1 claim of per-item vectors "verified by the LOG-224 reviewer" is retracted — the LOG-224b reviewer is the first to byte-check the file.
   - Item/tokenizer mapping: `item` + `ent` strings from the records, tokenized with the pinned `EleutherAI/pythia-410m` HF tokenizer pre-GPU (guards G7/G10).
   - **Rescue anchor (reviewer-verified, `exp077_results.json` → `bridge_gate` block):** Δm = **+0.233333 (23.33pp), b = 14, c = 0, p = 0.0001220703125**, baseline accuracy 0.60. [FACT]
   - The **official bench (b=6, +10pp, c=0)** is recorded as a **post-K2-P replication option** once its per-item records are mirrored in-repo per the standing LOG-197 TODO — **not claimed as executable**. No EXP070 records anywhere (guard G6 stands).
2. **(d) arm CUT.** The random-rotation control arm is removed from the battery. K2-P = exactly **180 passes** (60 items × 3 arms); G4 binds to the 180 branch. Zero-extra-pass top-5 token+logit archiving retained on all arms as a non-verdict-driving instrument (preserves future S3-7 optionality; explicitly not a verdict endpoint).
3. **Dependency discharged.** All "LOG-222" references now read **LOG-225**. S3-8 (LOG-225) returned **Supported**: mean per-item residual **+0.322534** (std 0.0291, positive on 60/60 items), downstream gain **g mean 1.797** (×1.8, std 0.052). The §7 pre-execution gate (iii) resolves toward **PROCEED**. K2 is now scoped as an **attribution pilot** (which component amplifies), not a whether-downstream-matters pilot. Law #15 Q2 stands as-is (both branches were pre-priced).
4. **Gloss conformance.** Every loose gloss ("attention-free", "bypass attention entirely", "pure bypass probe", "straight into the unembedding") is conformed to the lemma's binding **positional** claim: **no δ transport *between* positions**. Cell-2 verdict-reading instruction (binding): **"no upstream δ transport; the rescue is final-position-local (readout + local downstream gain)" — NOT "pure direct readout shift."**
5. **G8/G10 disjointness.** New guard: any item whose entity token span coincides with the final sequence position is excluded and recorded before any GPU pass (arms (a)/(b) would otherwise coincide on that item; the lemma assumes disjointness).
6. **Terminology.** "Tango's exact interval" → **"Tango (score) two-sided 95% CI"** throughout.
7. **Steelman box:** §8's five entries retained at full strength; **sixth entry added** — the smoke-bench headroom objection, steelmanned at full strength, answered-and-conceded.

**Unchanged:** kill bars L > 0.05 / U < 0.05; verdict-table exhaustiveness; pin-divergence → Inconclusive; guards G1–G3, G5–G9; Law #15 four answers; the S3-9 non-folding; the narrow routing-Refuted cell; EXP070 exclusion.

---

## 0.1 Honest headline + ambition bar (LOG-218 double bar)

**Headline [INFERENCE]:** K1 and EXP082 killed both directional tilt stories — the bridge is a relational (t−f) direction that rescues with no target-boost and no foil-suppression. S3-8 (LOG-225, **Supported**) settled the downstream question at $0: the direct L1 readout shift explains only ~57% of the margin shift; the circuit adds a further +0.32 margin units (×1.8, on 60/60 items). **K2 asks the question one level deeper, and it is the attribution question the S3-8 result licensed:** the gain is real and downstream — *which component amplifies it*? Does the rescue reach the decision via δ transported *between* positions (routing through attention computation at layers > l*), or is the rescue final-position-local (no inter-position δ transport — the final-position residual path through local downstream operators)?

**Belief-change (ambition bar A1, in writing):** the belief that changes is "the bridge engages upstream computation." If the bypass arm rescues ≥ the entity-position arm (contrast CI excluding a δ_min routing advantage), the output-side *mechanism* program closes — the bridge is logit steering, period — and the P2 pivot fires (mechanism-family → trajectory/closed-loop controllers; the bridge survives only as engineering). If the entity-position arm rescues while the final-token arm is flat, there is a mechanism upstream to hunt — the program earns its first positive mechanism-existence claim since the bridge was found, and the attention-engagement measurement campaign (which heads/positions carry the rescue) is licensed. A weak steelman fails the review same as a weak license: the strongest case against this design is boxed in §8, at full strength, answered or conceded.

**Ambition × rigor check (LOG-218):** *could this change what anyone believes?* **Yes.** Bypass-Supported closes the output-side mechanism program — the field's belief that a frozen-model steering vector must engage upstream computation dies with it. Routing-Supported licenses the program's first positive mechanism-existence claim since the bridge, reopening the attention-engagement hunt. Either cell moves belief; Inconclusive is priced, not hidden.

---

## 1. Knowledge-protocol discharge (what was read)

Read before writing, in order (REV1 inherits the frozen §1 list and adds):

1. `research/TEAM_KNOWLEDGE_PROTOCOL.md` §1 (mandatory reading list; briefing template LOG-218).
2. `reports/research_log.md` — **LOG-224** (the Law #14 verdict: SIGN-WITH-FIXES, 6 fixes; the smoke/official bench conflation [FACT]; CEO bench decision SMOKE; (d) CUT; S3-8 follow-ups (a) STAND AS-IS, (b) S3-9 stays queued, (c) ×1.8-gain confound → gloss conformance only); **LOG-225** (S3-8 Supported: residual mean +0.322534, g mean 1.797, ×1.8, 60/60 positive; dependency PROCEED; numbering repair: "LOG-222" → LOG-225); LOG-213 (K1-EXONERATED; K2 pilot licensed), LOG-218 (ambition × rigor), LOG-219 (campaign mode).
3. The frozen plan: `research/analysis_plans/K2_ROUTING_BYPASS_PLAN_LOG223_2026-09-23.md` (unchanged; REV1 is a separate dated file).
4. The S3-8 result: `research/analysis_plans/S38_DOWNSTREAM_ANALYSIS_LOG225_2026-09-23.md` (dependency record; the ×1.8-gain scope note — attention attribution unresolved — is why K2 is an attribution pilot).
5. Artifact existence checks (no execution): `experiments/runs/EXP077_cone_vs_line/exp077_instance_records.json` (60 items, schema `item`/`ent`/`typ`/`correct`/`rescue_indicators`) and `experiments/runs/EXP077_cone_vs_line/exp077_vectors.pt` (18 tensors — `v_hat`, `v_hat_c`, `mu` 1×1024 each; `v_hats`, `v_hat_c_ks` 5 each; `u_list`, `q_list` 8×1024 each; `r_vec`, `B_wrong`, `B_perp_basis` [FACT, LOG-224b]; torch-zip structure intact; **no per-item C8 vectors** — only per-item norms in `exp077_results.json → injection_vector_norms`, all = α=0.5); rescue anchor from `exp077_results.json` → `bridge_gate`: **b=14, c=0, Δm=+0.233333, p=0.0001220703125** [FACT].
6. **REV3 additions:** `reports/research_log.md` **LOG-227** (the Law #14 ruling on D1 — option (a) one-sided repair; satisfiability recomputed 0.0432 < 0.05 at N=60, 0.0477 < 0.05 at the G10 floor; bite-check b=c=1 fires / b=c=2 fails; options (b)–(d) rejected with reasons; R1–R7 CONFIRM all, OVERTURN none; D2 escalated as a recorded known defect, not a blocker); the frozen LOG-223 plan and REV2 (inheritance base — both untouched). `~/workspace/SCBI/AGENTS.md` (the 14 Inviolable Laws, Law #4/#9 scope).

**One challenge (knowledge protocol §2; REV3-scoped):** the one-sided repair makes row 1 *directionally exclusive* in a way the LOG-228 reviewer should explicitly confirm as intended: a routing world in which arm (a) carries a small-but-real positive rescue (e.g. b_a = 4, c_a = 0 — Δ̂M_a = 6.67pp > δ_min) now fails the flatness conjunct *by design* (correctly — that is not a flat channel), so if the contrast bar also clears, the observation falls into the row-3 catch-all → Inconclusive, never Supported. Any routing world with even mild final-position leakage can therefore never be routing-Supported — only Inconclusive. [INTERPRETATION] This is the honest partition (a routing claim with local leakage is genuinely ambiguous about the transport mechanism, and Inconclusive is priced, not hidden), but the program should own it: the LOG-227 ruling preserved answerability of the headline case (clean routing: Δ̂M_a ≈ 0) at the price of making partial-leakage routing worlds unlicenseable. A reader who expects row 1 to catch "routing plus a little local readout" is misreading the bar.

**One idea (knowledge protocol §2):** the D1 repair generalizes into a standing design rule for every future kill-battery: **any per-arm "demonstrably flat/quiet" conjunct should be one-sided from the start, declared directional by construction** — two-sided flatness bars are an instrument-specification error whenever the negative direction is inferentially irrelevant. *Could this change what anyone believes?* Yes — the belief that a two-sided CI is always the more rigorous default: the D1 arithmetic (narrowest two-sided upper 0.0602 > 0.05 at N=60) falsifies satisfiability outright, while the directional form (0.0432) bites and survives the G10 floor. Cheapest falsifier of the rule: apply it to a battery where the "flat" direction genuinely matters (e.g. a kill bar on negative rescue) — the rule would license a directional miss there, which is why the rule must state the directionality in writing at registration. Free-tier cost: $0 (protocol text only). Proposal: add it to `research/TRACK7_REVIEW_CHECKLIST.md` as a pre-registration lint ("flatness bars: one-sided, direction stated").

**One challenge (knowledge protocol §2; REV1-scoped):** the REV1 bench pin makes K2-P's headroom larger (b=14 anchor) than the official bench (b=6) that a post-K2-P replication will use. If a cell-2 verdict on the smoke pin is treated as settled without that replication, the program-level closure rests on the higher-headroom pin alone — the replication is a guardrail, not decoration. §7 requires it before the P2 pivot is reported as settled.

**One idea (knowledge protocol §2):** per-block attribution as K2's follow-up grammar — once K2 adjudicates routing vs final-position-locality, the ×1.8 gain's locus (blocks 21/22/23 vs final LayerNorm vs unembedding) can be localized by per-block injection at the *same* position mask, reusing K2's arms as a template. Cheapest falsifier of "the gain is all final-LayerNorm": inject the bridge at the block-23 output, final position only — if the residual over the L1 prediction collapses, the amplifier sits in blocks 21–23.

---

## 2. Rationale, premises, and the (discharged) S3-8 dependency

**[FACT]:** K1-EXONERATED (LOG-213) — not one of 180 bridge directions reaches the 0.9 target-row bar; the bridge is a relational (t−f) direction, not a target boost. EXP082-EXONERATED (LOG-217) — foil-suppression Not supported on every run (k_f = 0/60); the bridge is neither target-directed nor foil-directed on any item of any run — yet rescues +23.33pp (smoke bench) / +10pp (official bench). The static directional-readout story is dead.

**[INFERENCE]:** what remains is exactly two positional accounts of the rescue:
- **(i) Final-position-local:** the injected direction reaches the decision with **no δ transport between positions** — the final-position residual path through local downstream operators (residual-path LayerNorm/MLPs at the final position, final LayerNorm, unembedding). This is the lemma's binding claim; it is never phrased as "attention-free" or "bypassing attention entirely."
- **(ii) Routing:** δ is transported *between* positions by attention computation at layers > l* before it moves the decision — a mechanism exists upstream.

**S3-8 dependency [DISCHARGED]:** S3-8 (LOG-225) returned **Supported** — mean residual +0.322534, downstream gain ×1.8, positive on 60/60 items. The direct-readout-only null is dead at $0; the premise "downstream transformation is real" is confirmed. **K2 is therefore scoped as an attribution pilot** — which component amplifies (attention re-routing vs LN/MLP gain) — not a whether-downstream-matters pilot. The "residuals ≈ 0" branch of the dependency is closed; the frozen plan's pre-priced "residuals large" branch licenses this execution.

**Law #15 Q1 (recorded):** does the bridge's rescue reach the decision via δ transported between positions (routing) or via the final-position-local path with no inter-position δ transport?

**Law #15 Q2 (decision changed; stands as-is):** CONTINUE both ways, with pre-named consequences — final-position-local Supported → P2 pivot fires (output-side mechanism program closes; bridge demoted to engineering; mechanism-family → trajectory/closed-loop controllers); routing Supported → upstream mechanism hunt licensed (attention-engagement campaign, CLLC routing-signal pilot); Inconclusive → HOLD (question open; instrumentation upgrade + powered re-registration, not silent culling); Underdetermined → fix cause, re-run under a new LOG. A cell-2 verdict is read per the binding instruction in §4: "no upstream δ transport; the rescue is final-position-local (readout + local downstream gain)" — NOT "pure direct readout shift."

**Law #15 Q3 (cheapest; costed exactly):** **180 forward passes** on the primary pin (60 items × 3 arms; baseline correctness from archived smoke records — no re-baselining passes). The mechanism question cannot be answered from CPU/archived data: the archive holds only all-position bridge runs, so position-ablation is not deducible without live passes. Everything else — runner build, bridge-identity check (construction-identity, guard G1), entity-position mapping feasibility, CI/MDE arithmetic, this document — is CPU/$0. Secondary pin (160m/L10) +180 passes = 360 total, pre-registered as a conditional replication (see §4). At the program-measured 22 fwd/s (2×T4), 180 passes ≈ 8.2 s ≈ 0.002 T4-h; 360 ≈ 16 s ≈ 0.005 T4-h. The budget is passes, not hours; the adopted ~180-pass budget fits the primary pin exactly. **The (d) arm is CUT per LOG-224 — the diagnostic it served is preserved as zero-extra-pass archiving (§3.6).**

**Law #15 Q4:** the Mathematical License, §5.

---

## 3. Design

### 3.1 Run pins (frozen; no new experiment number — K2 is a kill-battery probe, not a new EXP)

| Pin | Model | Target layer | α | Bridge vector | Benchmark items | Bridge rescue (archived) |
|---|---|---|---|---|---|---|
| **K2-P (primary)** | `EleutherAI/pythia-410m` | L20 | 0.5 | per-item **construction-identity** b_K2 = α·normalize(E[target]−E[foil]), rebuilt from the pinned model + pinned tokenizer + the in-repo deterministic benchmark construction (`run_exp077.py` §3 constants); LOG-197 E1+E2 source link (C8 = EXP066 `make_bridge_vec` verbatim, in the runner source). No per-item vector archive exists — identity licensed by deterministic reconstruction (§4 G1) | EXP077 **smoke** 60 items (`experiments/runs/EXP077_cone_vs_line/exp077_instance_records.json`) | **+23.33pp, b=14, c=0, p=0.0001220703125** (smoke `bridge_gate`; baseline acc 0.60) |
| **K2-S (secondary, conditional)** | `EleutherAI/pythia-160m` | L10 | 0.5 | construction-identity (same G1 protocol): **EXP065 has no vector archive** — `results.json` + `run_log.txt` only. Vectors rebuilt from the pinned `EleutherAI/pythia-160m` + pinned tokenizer + the EXP065 in-repo runner construction | EXP065 60 items | +16.67pp, b=10, c=0 |

K2-S runs only after K2-P's verdict **and** CEO GPU clearance; it is the layer/model replication. EXP070 is excluded (Underdetermined, mirror-pending — per task guard). **The official bench (b=6, +10pp) is a post-K2-P replication option** once its per-item records are mirrored in-repo per the LOG-197 TODO — not claimed as executable.

### 3.2 Arms (per pin)

All arms: frozen model, hook at the target layer's output (same hook site as the archived runs), per-position masked additive injection of α·b̂; decision read at the final token exactly as the archived runs (argmax over {target, foil} logits).

- **(a) FINAL-ONLY:** inject only at the final sequence position. **License:** the §5 positional-confinement lemma — with P = {p_last}, δ cannot reach any other position via attention (causal mask: no position attends from the future), so any rescue is **final-position-local: no δ transport between positions**; the rescue path is the final-position residual through local downstream operators (residual-path LayerNorm/MLPs at the final position, final LayerNorm, unembedding). Per the cell-2 reading instruction, this is NOT "pure direct readout shift" and NOT "bypassing attention entirely" — the lemma's claim is positional.
- **(b) ENTITY-ONLY:** inject only at the premise-entity token positions (head/tail entity strings from the item record, mapped to token positions with the pinned tokenizer before any GPU pass; multi-token entities → all their tokens; mapping recorded per item — see guards G7/G10). **License:** no residual-stream shortcut exists from these causally-upstream positions to the final position; any effect on the decision must travel *between* positions — i.e., through attention computations at layers > l* — because attention is the only inter-position channel in the frozen architecture (LayerNorm and MLPs are per-position operators [FACT]). A rescue here = routing through attention.
- **(c) ALL-POSITIONS:** the archived construction verbatim (broadcast over all positions). **Positive control:** reproduces the historical rescue; validates that the benchmark still has headroom and the bridge vector is intact in the K2 runner. FATAL gate if it fails (guard G5).

**Baseline:** archived **smoke** baseline correctness per item (`correct` field in `exp077_instance_records.json`) — no new baseline passes.

### 3.3 Pass count (exact)

Per pin: 60 items × 3 arms = **180 forward passes**. K2-P alone = 180 (exactly the adopted budget). K2-P + K2-S = 360. Top-5 token+logit archiving (§3.6) adds **zero** forward passes — logits are already computed. G4 binds to the 180 branch per pin.

### 3.4 Primary endpoint (mirror of §H6; no silent shifts per Law #4)

Δ̂M_b − Δ̂M_a, where Δ̂M_arm = (b_arm − c_arm)/60 vs the archived baseline, with the **Tango (score) two-sided 95% CI for the difference of two paired proportions** (arm outcomes are paired on the same 60 items — the contrast is P_b(right) − P_a(right) on one paired sample). Verdict bars per the binding §G1b protocol, δ_min = 0.05:

- **Routing Supported / final-position-local Not supported:** L(Δ̂M_b − Δ̂M_a) > 0.05 AND b_b ≥ 6 (L1 MDE at c=0) AND **U_1s(Δ̂M_a) < 0.05** (the final-position channel demonstrably flat).

[JUSTIFICATION — LOG-227 repair of D1]: the flatness conjunct is **directional by construction** — it rules out a material *positive* arm-(a) effect (H_routing predicts Δ̂M_a ≈ 0; the conjunct always meant "rule out material positive (a)-effect"); the negative direction is inferentially irrelevant. The two-sided bar **over-tested** (one-sided 97.5% stringency) and was **unsatisfiable** at N=60 — the narrowest possible two-sided 95% upper bound is z²/(n+z²) = **0.0602 > 0.05** (exact CP for 0/60 gives 0.0596 — also > 0.05), so a *flat* arm (a) always failed and row 1 could only fire when arm (a) was materially *negative*: the routing-Supported cell was unreachable as intended. Satisfiability recomputed: narrowest one-sided Tango upper at N=60 = 2.7057/62.7057 = **0.0432 < 0.05**; exact-binomial cross-check **0.0487 < 0.05**. **The bar bites:** b=c=1 fires (≈0.0379); b=c=2 fails (≈0.0536). **G10-floor robustness:** at N=54 the one-sided Tango upper is **0.0477 < 0.05** — the CP form would break at **0.0539**, hence the Tango pin. **δ_min = 0.05 unchanged; the primary contrast stays two-sided 95% Tango per §G1b; the five verdict categories are untouched.** The two-sided bar was an instrument-specification error; this repair is pre-execution (no data touched, no results seen), the hypothesis, question, δ_min, and contrast endpoint are unchanged, and C1–C3 are satisfied — documented as a new revision per "design changes take a new number" (Law #4 compliance [FACT, LOG-227]).
- **Final-position-local Supported / routing Not supported:** Δ̂M_a ≥ Δ̂M_b AND U(Δ̂M_b − Δ̂M_a) < 0.05 (rules out a δ_min advantage of (b) over (a)) AND b_a ≥ 6 (the rescue is actually present, not a degenerate both-null). **Reading instruction (binding):** "no upstream δ transport; the rescue is final-position-local (readout + local downstream gain)" — NOT "pure direct readout shift."

Per-arm diagnostics (reported, never verdict-bearing alone): McNemar exact p and exact 95% CI for each arm's Δ̂M.

### 3.5 Kill bars (recomputed arithmetic; unchanged)

N=60 per pin (the bars and the paired contrast CI apply at the actual post-exclusion N per the ≤6-exclusion floor — guard G10). L1 MDE at c=0: b ≥ 6 (2⁶=64 → p=0.03125 ≤ 0.05) = 10pp — the minimum present rescue. The contrast CI's exact width depends on the joint discordant table; worst-case MDE is bounded by the per-arm MDE (10pp); failure of the contrast CI to clear δ_min → **Inconclusive (held, never culled)** — a straddle is a power statement, not a final-position-local verdict. This is the LOG-218 §F2 discipline: p ≥ 0.05 alone never fires a falsifier.

### 3.6 Top-5 logit archiving (non-verdict instrument; replaces the (d) arm)

On all arms, the executor archives the **top-5 token ids + logits at the decision position per item** — **zero extra forward passes**. This is explicitly **not a verdict-driving endpoint**: it fires no kill, appears in no verdict row, and only preserves **future S3-7 optionality** (the competitor-logit-drop diagnostic can be computed post-hoc against a separately licensed random-rotation control arm, which would be a new LOG, not a silent extension of K2). The LOG-224 ruling stands: the (d) arm's diagnostic cannot touch the licensed question, so it is cut rather than budgeted.

### 3.7 Assumptions discharged at design time

- Decision position = final token [FACT — all corpus runs read logits at `logits[0, -1, :]`].
- Injection site = target-layer output module, same as archived runs [FACT — EXP065 runner ll. 423–430; EXP077 §2].
- Entity positions locatable pre-GPU with the pinned tokenizer [ASSUMPTION — feasibility checked CPU-first; mapping failures recorded per item, items with unmappable entities excluded → counts toward Underdetermined accounting].
- Entity span ∩ {final position} = ∅ [pre-registered exclusion — guard G10].

---

## 4. Guards (FATAL unless marked diagnostic)

- **G1 bridge-identity (construction-identity) [INFERENCE]:** no per-item vector archive exists for either pin — vector identity is licensed by deterministic reconstruction, graded [INFERENCE] (deterministic reconstruction), never [FACT]: (a) rebuild per-item b_K2 = α·normalize(E[t]−E[f]) from the pinned model + pinned tokenizer + the in-repo deterministic benchmark construction (`run_exp077.py` §3 constants for K2-P; the EXP065 in-repo runner construction for K2-S); (b) per-item ‖b_K2‖ must match the run-logged C8 norms in `exp077_results.json → injection_vector_norms` (relative error ≤ 1e-5); (c) the target/foil token mapping is logged per item (feeds G2); (d) identity chain = E1+E2 source link (C8 = EXP066 `make_bridge_vec` verbatim, in the runner source) + the EXP077 run-log F1 guard record. **Honesty caveat (LOG-224b):** the norm fingerprint in (b) is a weak identity check — any unit×α vector passes it. The honest license for K2 vector identity is **deterministic-reconstruction + the live (c)-gate** (guard G5): it implies no archive-grade verification. Any item failing (a)–(c) → item excluded, recorded; ≥3 failures → run INVALID.
- **G2 label cross-check:** the target/foil option tokens used per item must match the benchmark's recorded target/foil exactly; mismatch → item excluded.
- **G3 Δθ=0:** sha256 of model state_dict pre-run == post-run; mismatch → FATAL, results not reported.
- **G4 no-forward-pass-except-licensed:** executor counts passes; K2-P must be **exactly 180**; K2-S exactly 180; overrun → INVALID. (The 240 branch is closed by the (d) cut.)
- **G5 (c)-reproduction gate:** b_c ≥ 6 (L1 MDE) else the run is INVALID → verdict Underdetermined with cause recorded (benchmark or vector broken; routing question unaskable). **Why non-vacuous under the b=14 baseline:** the gate checks the K2 runner's *live* (c) arm, not the archive — the floor is L1 MDE (b=6), deliberately below the b=14 anchor, so it tests implementation integrity (hook site, vector identity G1, position masks) and current benchmark headroom rather than demanding full archive reproduction. A masking bug, wrong hook, or benchmark regression can still trip it. [INFERENCE]
- **G6 EXP070 excluded:** no EXP070 records, artifacts, or vectors used anywhere.
- **G7 Law #7 provenance note:** the bridge is the archived label-informed vector (normalize(E[target]−E[foil])) used *as a mechanistic probe*. K2 probes where the rescue travels; it draws no autonomous-mechanism claim from the label-informed construction — that question is K3's, untouched here.
- **G8 entity-mapping:** position masks logged per item (token ids + strings); multi-token handling pre-registered (§3.2); unmappable → item excluded, recorded.
- **G9 LayerNorm-scale diagnostic (steelman-4 check, diagnostic not a gate):** per-position residual norms at the final layer recorded for (a)/(b); if the (b)/(a) final-layer norm ratio diverges from the injection-norm ratio by >2×, the divergence is recorded as an [OBSERVATION] (covariate, never a post-hoc gate).
- **G10 disjointness (pre-registered exclusion):** any item whose entity token span includes the final sequence position is excluded and recorded **before any GPU pass**. Rationale: arms (a)/(b) would coincide on that item; the lemma assumes P_a ∩ P_b = ∅. Exclusion count reported per arm; exclusions count toward the Underdetermined accounting, never silently dropped. **Exclusion floor (pre-registered):** **>6 exclusions (>10%) → the run is Underdetermined** with the exclusion cause recorded; at ≤6 exclusions, the discordant-based bars and the paired contrast CI apply at the **actual N** (the verdict table's accounting records the actual N).

---

## 5. Mathematical License (binding — Law #15 Q4; see research/foundations/MATHEMATICAL_LICENSE_STANDARD_2026-09-23.md)

**License grade:** IN-HOUSE-PROOF (positional-confinement lemma: elementary proof from the causal mask, complete, re-derived from scratch and surviving the LOG-224 review — promotion to [THEOREM] still requires the standalone Law #14 review of the proof document) / IN-HOUSE-PROOF (bridge construction identity, LOG-197 two-link chain E1+E2).

### L1. Authorizing result

- **Statement (exact) — the positional-confinement lemma [PROPOSITION]:** Let M be a causal (left-to-right masked) decoder transformer with per-position residual streams and additive intervention δ applied to the layer-l* output at a set of positions P. Then: (i) for all layers l > l* and all positions j < min(P), the activation at (l, j) equals the unintervened activation (proof: by induction, position j attends only to positions ≤ j, so δ at positions ≥ min(P) is never in its receptive field); (ii) if P = {p_last} (final position only), δ influences the output logits only through the final-position residual path — **no δ transport between positions** is possible, because no position j > p_last exists; the final-position residual passes through local downstream operators (residual-path LayerNorm/MLPs at the final position, final LayerNorm, unembedding); (iii) if P ⊆ {positions < p_last} (G10-disjoint from the final position), δ can influence the final-token logits only through attention computations at layers l > l* (queries at positions > p attending to keys at p) — attention is the only inter-position channel in the frozen architecture (LayerNorm and MLPs are per-position operators [FACT]).
- **Source:** in-house proof (elementary induction on the causal mask; M4 space/shape checks trivial — positions and layers are the objects). Standalone proof document: `research/analysis_plans/K2_CONFINEMENT_LEMMA_PROOF_LOG224c_2026-09-23.md` (graded [PROPOSITION]; **DO NOT CITE AS [THEOREM] — requires Law #14 review for [THEOREM] promotion**). Per the LOG-224b ruling, the standalone document is required for the [THEOREM] promotion path, NOT a blocker for pilot SIGN — the inline §5 proof suffices for pilot SIGN. The K2 run is graded as the license's empirical exercise, not its proof.
- **Epistemic label:** [PROPOSITION] (→ [THEOREM] after Law #14 adversarial review of the proof).
- **Companion identity [PROPOSITION]:** b_K2 = α·normalize(E[t]−E[f]) per item, by deterministic reconstruction from the pinned model + pinned tokenizer + the archived construction (LOG-197 E1+E2 chain); discharged per guard G1 — never against a per-item archive, because none exists.

### L2. Quantitative prediction for the primary endpoint

- **Endpoint:** Δ̂M_b − Δ̂M_a with the Tango (score) two-sided 95% CI (§3.4).
- **Prediction — direction:** under the final-position-local account, Δ̂M_a ≥ Δ̂M_b — the final-position injection sits maximally coupled to the unembedding (direct residual path); attention-mediated transport from entity positions can only dilute the direction (attention weights ≤ 1, mixing across 12 downstream layers at L20). Under routing, Δ̂M_b − Δ̂M_a > 0 with Δ̂M_a ≈ 0 — the final-position path alone cannot rescue; the rescue requires inter-position δ transport.
- **Prediction — magnitude (anchored to the smoke bench, not invented):** archived rescues: +16.67pp (EXP065), +13.33pp (EXP066), **+23.33pp (EXP077 smoke, b=14, c=0 — the K2-P anchor)**. Under the final-position-local account: Δ̂M_a ≥ Δ̂M_b with Δ̂M_a expected within-or-above the historical band (arm (a) ⊆ arm (c)'s positions; readout coupling maximal) — pre-registered anchor Δ̂M_a ≥ +10pp (the L1 MDE boundary); arm (c) expected near the smoke anchor (+23.33pp), with Δ̂M_(c) − Δ̂M_b = the restriction-cost measurement (recorded). Under routing: Δ̂M_b − Δ̂M_a clearing +0.05 with Δ̂M_a ≈ 0 (U_1s(Δ̂M_a) < 0.05). **Conceded uncertainty:** the position-restricted arms have no historical precedent — the (c) arm quantifies the restriction cost directly.
- **Derivation:** direction follows from L1 (i)–(iii) + attention-weight bound; magnitude anchored to the three archived rescues (smoke bench for K2-P); coverage: all 60 items per pin; tolerance: the Tango (score) two-sided 95% CI.

### L3. Breaking point

- **Falsifying the final-position-local account:** L(Δ̂M_b − Δ̂M_a) > 0.05 with Δ̂M_a flat — routing demonstrably adds what the final-position path cannot. Decision: CONTINUE (upstream mechanism hunt licensed; §2 consequences).
- **Falsifying the routing account:** U(Δ̂M_b − Δ̂M_a) < 0.05 with Δ̂M_a ≥ Δ̂M_b and b_a ≥ 6 — no routing advantage survives the CI. Decision: CONTINUE (P2 pivot fires; output-side mechanism program closes) — read per the binding cell-2 instruction, never as "pure direct readout shift."
- **Breaking the license's application premise:** (c) fails guard G5 (the bridge does not survive position restriction at all) → neither account is tested → Inconclusive, never a verdict on either proposition (Charter M5.2 partition honored).
- **Outcome partition:** the §7 table maps every cell — routing-Supported / final-position-local-Supported / routing-Refuted (narrow, §7) / Inconclusive / Underdetermined — to a verdict and a consequence; no cell defers to executor discretion.

### L4. Assumption inventory

- **A1:** the causal-mask induction holds for the frozen architecture (no bidirectional leakage) — discharge: architectural [FACT] for GPT-NeoX-style decoders; verified by the hook-site read in the archived runners.
- **A2:** bridge identity = the archived construction, licensed by deterministic reconstruction (guard G1 discharges per item; promotion path: Law #14 review of this plan).
- **A3:** entity-position mapping correct (guards G8/G10; unmappable or coincident items excluded, counted).
- **A4:** LayerNorm re-normalization does not invert the (a)/(b) coupling asymmetry (diagnostic G9 records the check; no verdict rides on it).
- **A5:** Δθ=0 (guard G3 — FATAL on violation).
- **A6:** dilution by attention across 12 downstream layers does not wash a real routing effect below the 10pp L1 MDE while leaving the (c) arm intact — **conceded as the license's load-bearing risk** (see §8 steelman-1; the honest response is the Inconclusive partition, not a stronger claim).
- **Promotion path:** the lemma to [THEOREM] via Law #14 adversarial review of the standalone proof (LOG-224c scope); the causal upshot of any K2 verdict stays at mechanism-adjudication (L1), never a capability claim.

---

## 6. Verdict table (exhaustive; five categories only)

Pin-level verdicts (K2-P first; K2-S conditional):

| # | Observation (per pin) | Verdict: routing | Verdict: final-position-local | Consequence |
|---|---|---|---|---|
| 1 | L(Δ̂M_b−Δ̂M_a) > 0.05, b_b ≥ 6, **U_1s(Δ̂M_a) < 0.05** (one-sided 95% Tango upper; see §3.4 [JUSTIFICATION — LOG-227 repair of D1]) | **Supported** | **Not supported** | Upstream mechanism exists. License: attention-engagement campaign (which heads/positions carry the rescue); CLLC routing-signal pilot; ARP (S3-1) fingerprint program unblocked with a verified positive mechanism class. |
| 2 | U(Δ̂M_b−Δ̂M_a) < 0.05, Δ̂M_a ≥ Δ̂M_b, b_a ≥ 6 | **Not supported** | **Supported** | P2 pivot fires: output-side mechanism program closes (bridge = logit steering, period); mechanism-family → trajectory/closed-loop controllers; bridge survives only as engineering. **Binding reading: "no upstream δ transport; the rescue is final-position-local (readout + local downstream gain)" — NOT "pure direct readout shift."** |
| 2r | Cell 2 holds AND L(Δ̂M_a) > 0.05 AND b_b = c_b = 0 | **Refuted** | **Supported** | As cell 2, with the routing account actively contradicted (flat-zero under the only channel it could use) — Law #8: the routing reading stays dead unless new evidence resurrects it. |
| 3 | **No row-1/2/2r pattern: contrast CI straddles, OR the contrast clears but the per-arm conjuncts (flatness for row 1, rescue-presence b_a ≥ 6 for row 2) fail** — catch-all; closes the pre-existing exhaustiveness gap the LOG-227 repair makes live | **Inconclusive** | **Inconclusive** | HELD, never culled. Options: instrumentation upgrade (per-layer attention snapshots per S3-7 §6 spec) + powered re-registration at N≥100 (B2: N=100 → L2 MDE 9.0pp); or concede the pilot's ceiling. |
| 4 | Both arms flat (b=0) with (c) passing G5 | **Inconclusive** | **Inconclusive** | The bridge does not survive position restriction at all — the license's application premise broke (L3), not either proposition. Logged; K2's question is unaskable in this form. |
| 5 | Any FATAL guard fails / records missing | **Underdetermined** | **Underdetermined** | Fix cause; re-run under a new LOG. Nothing is filled by assumption. |

**Program-level aggregation:** both pins in the same cell → program verdict inherits the cell. Any pin divergence → **Inconclusive** program-level, with the divergence recorded as an [OBSERVATION] (layer-dependence hypothesis stays queued; the §1 challenge applies).

**Exclusion accounting (binding):** every pin-level verdict records the actual N (60 − exclusions) with the exclusion-cause log attached; exclusions are never silently dropped. >6 exclusions (>10%) → the run is Underdetermined with the exclusion cause recorded (guard G10).

**Secondary archiving (§3.6) verdict discipline:** the top-5 logit archives are recorded as [OBSERVATION] only; they fire no kill and appear in no row above. Banned verdict language absent throughout.

---

## 7. Consequences and ordering (pre-registered)

- K2-P executes only after: (i) Law #14 SIGN (LOG-228 targeted re-check), (ii) CEO GPU clearance. ~~(iii)~~ — the S3-8 pre-execution gate is **discharged**: S3-8 (LOG-225) Supported → **PROCEED** (recorded, not re-litigated).
- A cell-2 verdict on the smoke pin is reported as **provisional-pending the official-bench replication** (b=6, +10pp) before the P2 pivot is treated as settled — per the §1 challenge.
- K2-S executes only after K2-P's verdict + fresh CEO GPU clearance.
- K3's CPU construction audit proceeds in parallel (ordering is binding on interpretation, not preparation — §H6).
- S3-9 (gain tomography, ~80 passes) stays queued — out of §H6 jurisdiction, distinct verdict space; may run in parallel or after K2.
- EXP080/081 remain gated on the Law #7 audit + CEO GPU clearance (unchanged).

---

## 8. Steelman box (the strongest case against this design, at full strength)

**Steelman 1 — propagation washout (power, not evidence).** Injection at L20 leaves 12 downstream layers of attention mixing before the readout. Even if the rescue genuinely routes through attention, the entity-position signal is diluted by attention weights at every layer — a real routing effect could shrink below the 10pp L1 MDE while the final-token arm, sitting on the readout path, rescues cleanly. The design would then return "final-position-local Supported" for a routing world. **Answered in part, conceded in part:** the honest response is structural — any contrast-CI straddle lands in the Inconclusive cell (held, never a final-position-local verdict), and the (c) arm measures the restriction cost directly (Δ̂M_(c) − Δ̂M_b). But the asymmetry is real and conceded: this pilot has more power to confirm the final-position-local account than to confirm routing, because the local account's predicted pattern (a clean, maximal (a) rescue) is easier to see than routing's (a diluted (b) rescue beating a flat (a)). The Law #14 reviewer should treat a cell-2 verdict as provisional-pending-replication and a cell-3 as the modal honest outcome.

**Steelman 2 — position non-comparability (norm confound).** Arms (a), (b), (c) inject at 1, k, and T positions respectively — total injected norm differs across arms. A critic argues the contrast measures total norm, not position. **Answered:** the licensed comparison is (b) vs (a), and under the final-position-local account (a) should dominate *regardless* of norm — it is exactly on the final-position path with maximal unembedding coupling, while any attention-mediated transport from (b) can only attenuate. Total-norm arguments predict (c) > everything, which the (c) arm checks directly. Per-position α is held fixed (matching the archived broadcast semantics), and per-arm norms are recorded. The residual asymmetry favoring the local account on power grounds is conceded (see steelman-1's conclusion).

**Steelman 3 — the contrast needs depth that static injection already killed.** Five static-geometry families are decision-flat at L20; one could argue any upstream-position intervention is a priori dead and K2 is theory preservation dressed as a discriminator. **Answered:** those kills are narrowly licensed to *unconditional static-geometry variants of the contrast direction* — the bridge is not a contrast direction (EXP078: median projected bridge energy 0.0544 < 0.10, ENERGY_GATE_HALT — the bridge lives outside the dead room), and the bridge demonstrably rescues (+23.33pp smoke). K2 tests the rescuing vector, not the dead family. The steelman fails on the license scope.

**Steelman 4 — LayerNorm re-normalization asymmetry (conceded).** Adding a vector at one position vs many changes local LayerNorm statistics; re-normalization could attenuate (a) and (b) differently, making the contrast partly a normalization artifact. **Conceded:** diagnostic guard G9 records per-position final-layer residual norms for (a)/(b); if the (b)/(a) norm ratio diverges from the injection-norm ratio by >2×, it is recorded as an [OBSERVATION] and the verdict is read with that caveat. It is deliberately not a gate — a post-hoc gate would be Law #4-adjacent.

**Steelman 5 — the archiving instrument smuggles a second mechanism question into K2.** **Answered by scope discipline:** §3.6 keeps the top-5 logit archives [OBSERVATION]-only with no verdict cell, no kill, and no consequence row — and the (d) control arm is CUT, so no compute is spent on the unlicensed question. If the reviewer judges even the archiving too much scope, it can be dropped with zero effect on the licensed verdict.

**Steelman 6 — the smoke bench's headroom flatters the final-position-local reading (new; introduced by the REV1 bench pin).** The smoke anchor (b=14, +23.33pp at baseline acc 0.60 — 24 items of headroom) is the largest rescue in the corpus; K2-P's arms inherit far more room than the official bench (b=6, +10pp) ever had. A critic argues this flatters the local account twice over: (a) arm (a) is expected to reproduce a large, easy-to-see rescue, while routing's signal still faces 12 layers of dilution — steelman-1's power asymmetry is *amplified*, biasing the pilot toward closure; (b) the (c)-gate floor (b=6) sits far below the b=14 anchor, so the gate can pass while the bridge is already degraded in the K2 runner, making it a weak guard. **Answered in part, conceded in part:** the verdict bars are unchanged and the licensed contrast is *relative* (Δ̂M_b − Δ̂M_a with δ_min = 0.05) — headroom does not move the bar, and the (c)-gate's purpose is implementation-sanity (G5), never anchor-reproduction, which the plan never demands. Headroom cuts both ways: more baseline errors means arm (b) also has room to rescue, so routing's bar is not stricter on the smoke pin. And the official-bench replication is queued post-K2-P precisely to give a cell-2 verdict an independent, lower-headroom check before the P2 pivot is treated as settled (§7). **Conceded:** the modal asymmetry (steelmans 1–2) is genuinely amplified on the smoke pin — a cell-2 verdict there is provisional-pending-replication, and a reader who forgets that is misreading the plan.

**Steelman 7 — the one-sided repair is significance-shopping (new; introduced by the REV3 D1 repair).** One-sided intervals are the classic tool for manufacturing significance: swapping a two-sided CI for a one-sided one at the same nominal 95% silently relaxes the bar on the tested direction. A hostile reader will say: the protocol hit an unsatisfiable bar and, instead of paying for N or accepting the rescope, changed the instrument to one that can pass — exactly the move Law #9 exists to catch. Why is this not post-hoc loosening dressed as directional semantics? **Answered in full, not conceded:** (1) **δ_min = 0.05 is unchanged** — the quantity the program cares about, the materiality threshold, did not move a hundredth of a point; the thing being tested is identical, only the instrument's directionality now matches the conjunct's always-one-sided meaning. (2) The **primary contrast** — the verdict-driving comparison — **stays two-sided 95% Tango per §G1b**; the one-sided form applies only to a per-arm *diagnostic* whose semantics are directional by construction (it rules out a material *positive* (a)-effect; the negative direction is inferentially irrelevant). (3) The repair is **pre-registered pre-data**: no data touched, no results seen; it is ruled by Law #14 (LOG-227) and documented as a new revision, with Law #4 compliance (C1–C3) recorded — the hypothesis, question, δ_min, and contrast endpoint are all unchanged. (4) **The bar still bites:** b=c=1 fires (≈0.0379); b=c=2 fails (≈0.0536) — a genuinely flat arm passes while even a two-item swing fails; this is not a free pass, and the LOG-227 bite-check is on the record. Had any of (1)–(4) failed, this objection would have stood and the repair would have been **escalated rather than buried** — significance-shopping it is not, and that is precisely why the repair is priced here in the open instead of absorbed silently into the table.

---

## 9. First-principles check (LOG-218 §2)

No authority is invoked without reduction: the design's authorization is the causal-mask lemma (§5 L1) — an induction on the attention mask, not "the literature suggests." The bridge's empirical anchors are program-measured rescues (smoke anchor b=14, c=0, p=0.0001220703125 — reviewer-verified), not field analogies. Where the math runs out (dilution magnitude, LayerNorm behavior), the plan says so (§5 A6, §8 steelmen 1/4/6) instead of borrowing confidence.

---

## 10. Execution release checklist (for the LOG-228 reviewer)

- [ ] L1–L4 license section graded ≥ CONJECTURE-UNDER-TEST (self-grade IN-HOUSE-PROOF; verify the lemma proof document, `K2_CONFINEMENT_LEMMA_PROOF_LOG224c_2026-09-23.md`).
- [ ] Kill bars recomputed from primary sources (MDE 6/60 at c=0; δ_min=0.05 inheritance disclosed); repaired flatness bar `U_1s(Δ̂M_a) < 0.05` (one-sided 95% Tango, z=1.6449) verified satisfiable at N=60 (0.0432 < 0.05) and at the G10 floor N=54 (0.0477 < 0.05).
- [ ] Verdict table exhaustiveness (every contrast-CI × per-arm cell lands in exactly one row, incl. the row-3 catch-all; Charter M5.2).
- [ ] **Bundle implements the repaired bar (separate bundle chain, required before SIGN):** F1 — `evaluate_k2.py` implements `U_1s` (replace, don't supplement); F2 — six new evaluator tests, incl. the row-3 catch-all; F3 — BUILD_NOTES + manifest hashes updated.
- [ ] Law #15 Q1–Q4 on record (§2, §5).
- [ ] Steelman graded — **seven** entries at full strength (a weak steelman fails the review same as a weak license).
- [ ] Pass-count exactness (**180/pin; G4 binds to the 180 branch**), the (d) cut verified, the S3-8 dependency discharged (gate (iii) → PROCEED), and EXP070 excluded.
- [ ] Bench pin verified: `exp077_instance_records.json` + `exp077_vectors.pt` paths, smoke rescue anchor (b=14, c=0, p=0.0001220703125), official bench recorded as post-K2-P replication option only.
- [ ] EXP065/066/077/EXP082 numbers used verbatim (no invented figures); "Tango (score) two-sided 95% CI" terminology throughout.
- [ ] Gloss conformance: no loose gloss ("attention-free", "bypass attention entirely", "pure bypass probe", "straight into the unembedding") outside the lemma's binding positional claim; cell-2 reading instruction present.

---

**DO NOT EXECUTE before Law #14 SIGN (targeted re-check LOG-228, pre-assigned) and CEO GPU clearance.**
