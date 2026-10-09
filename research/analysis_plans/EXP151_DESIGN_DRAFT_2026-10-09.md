# EXP151 Design Draft — Law #15 worth-it packet: re-priced transitive-only hop dose-response at n=380/hop level — 2026-10-09

**Status: DRAFT — NOT SIGNED. NOT EXECUTED. NO EXPERIMENT NUMBER MINTED.** This design draft is the Law #15 worth-it packet licensed by the CEO's LOG-4977 ruling (option (a)) closing the LOG-219 OPEN debt. It awaits independent Law #14 review, CEO sign, and CEO number-mint. No forwards have been run under this packet.

**Drafting lane:** EXP151 Law #15 packet lane (design only), 2026-10-09. **This lane does not mint experiment numbers** — the number (expected: EXP151) is minted by the CEO at the Law #15 SIGN-and-mint, per LOG-4977 constraint (7).

---

## 1. Parent context [FACT]

EXP148 (J7) CONTINUE ADOPTED (LOG-4958/4959; independent verdict review ADOPT, LOG-4960): frozen Pythia-410m, WRITE/READ discipline beat budget-matched CoT by net +22.2pp (b=52, c=12, one-sided McNemar p=2.2833e-07, 95% Wald CI (0.1414, 0.3031)) — the program's first capability entry.

EXP149 (LOG-4969) HELD both follow-ups at Step-0 gates: (a) hop dose-response — pooled dry-run gate tripped on a compositional-heavy draw (B=0.90); post-stop diagnostic found violent stratum heterogeneity (compositional-2hop 0.9895 / 3-hop 0.9316 at ceiling; transitive-2hop 0.3105 / 3-hop 0.3316). (b) GPT-2-small portability — rebuilt-bench calibration B=0.15 outside the band (delivery fine; the boundary is calibration, not delivery). LOG-4969 licensed two repairs: (i) stratified dry-run gate, (ii) hardened-compositional template OR transitive-only dose-response.

EXP150 (LOG-4971/4972/4973) executed the transitive-only repair: stratified gate PASS (T2/T3 B = 0.3000/0.3000), C+S pilot licensed the full run (d_pilot = 0.30 → power 0.566 ≥ 0.53 floor), then the first full-run C+S block showed d_block1 = 0.40 → registered power 0.466 < 0.53 → **STOP/HELD per the registered bench-size rule** (a computation, not a choice). The hardened-compositional secondary was NOT built: validity constraints (v2)/(v4) are jointly unsatisfiable on the registered model+pool (all 40 closed-pool entities are 2 BPE tokens under Pythia — a pre-reg defect the Law #14 review missed; design-record finding). The transitive dose-response question remains unanswered — not refuted, not supported.

LOG-4976 (Friday cull #2) escalated the LOG-219 debt to the CEO; LOG-4977 ruled option (a): a re-priced transitive-only re-attempt via a fresh Law #15 packet, with the discordant rate now priced from the d_block1 = 0.40 datum — not guessed.

---

## 2. Design verdict: transitive-only dose-response at n_T2 = n_T3 = 380

**Registered design value [DEFINITION]:** n_T2 = n_T3 = **380 per hop level**, fixed by the registered bench: **2 transitive strata × 380 items = 760 items** (transitive-2hop, transitive-3hop; transitive recipe carried from EXP147/148 §5.1). The ruling's operative quantity is the per-hop-level n=380 — the power table, the bench-size rule, and the guard arithmetic are all keyed to it.

**Registered cost-feasibility flag [FACT — computed, not asserted]:** the LOG-4977 prose "4 strata × 380" reads literally as 1,520 items. At the registered recipe (255 forwards/item: B:15 + C:120 + S:120), that prices 387,600 generation + 600 dry-run + 4,800 pilot = **393,000 > guard (g) = 200,000** — cost-infeasible under the ruling's own numbered constraint (5) (guard (g) ≤ 200k). The feasible configuration delivering the ruling's operative n=380/hop-level is the transitive-only 2-strata × 380 bench: 193,800 + 600 + 4,800 = **199,200 ≤ 200k** [registered]. The registered guard wins over the prose reading (Law #2). CEO disposition LOG-4979: the 2-strata 760-item design is accepted; the LOG-4977 "4 strata × 380" prose was a transcription error; guard (g) needs no amendment. [Fix E1, Law #14 review 2026-10-09.]

**Cost-carry flag [FACT]:** the ruling's "≈60–70k forwards" estimate is a carry of EXP150's *realized* (early-stopped) cost (15.9k forwards — the run stopped at the first block). The full-run design cost for a transitive-only 2×380 bench is **199,200** forwards (computed above), ≈9h wall at EXP148 rates — the same order as EXP150's 199.8k design. The realized cost is lower only if the registered stops fire. CEO disposition LOG-4979: the worth-it call is priced at the 199,200-forward design cost — ACCEPTED. [Fix E1, Law #14 review 2026-10-09.]

**Power for the design [FACT]:** at n=380/level, design d-range **[0.30, 0.40]** (EXP150's [0.30, 0.36] extended to include the EXP150 d_block1 = 0.40 datum — the effect is now priced, not guessed; per the cull's option-(a) language): SE(θ) = 0.0370–0.0435, power **0.74–0.88** for δ = +0.10, one-sided α = 0.05 — the registered true-power band is **[0.74, 0.88]** (table, §6). The bench-size STOP floor is the band floor: **0.74**.

**Zero-margin flag [FACT]:** at the observed datum d = 0.40, registered power = 0.7429 — clears the 0.74 floor by **0.003**. The design is exactly powered at the observed discordant rate, with no headroom: any pilot/block rate above 0.40 trips the STOP. This is registered honestly here. CEO disposition LOG-4979: the 0.74 floor stands as the band floor (E3 precedent); the worth-it call at the priced cost is ACCEPTED. [Fix E1, Law #14 review 2026-10-09.]

---

## 3. The questions

**Primary — transitive-only hop dose-response [HYPOTHESIS]:** the WRITE/READ discipline advantage over budget-matched CoT grows with reasoning depth on the transitive strata: net(S−C) at transitive-3hop exceeds net(S−C) at transitive-2hop — δ̂_T3 − δ̂_T2 > 0, on frozen Pythia-410m, with a fresh bench at the registered n.

**Breaking point (primary):** 95% CI for (δ̂_T3 − δ̂_T2) entirely ≤ 0, with per-level guards (d_s),(e),(f),(f′) PASS → **KILL** the transitive-scoped dose-response claim (the gain does not grow with hops on the transitive strata; EXP148's CONTINUE stands as a pooled effect, not a depth effect). A second HELD here is a design-debt finding, not a license for another re-attempt — the apparatus stands down at that point (LOG-4977).

**Scope fence [DEFINITION]:** transitive strata only, Δθ=0, no fine-tuning. No Gap claim, no steering claim, no compositional claim, no cross-family claim. Whatever fires here *scopes* EXP148's CONTINUE; nothing overturns it. Hardened-compositional is excluded by design-record (see §5) — its reconciliation is a deferred, unlicensed lane.

---

## 4. Stratified dry-run gate (licensed repair (i), carried from EXP150 — binding, precedes the full run)

**Registered subset:** 20 fresh items per stratum × 2 transitive strata = 40 items (subset seed = construction_seed + 11 = 151012, registered at design — the A2 seed-derivation rule; no execution-time improvisation), B arm only, T_B=15, greedy, EXP149 pre-reg §5.3 scoring (carried verbatim). Computable before any full-run forward. Uses no test labels in prompts (Law #7 — golds touch scoring only).

**(d-T2)/(d-T3):** transitive-2hop / transitive-3hop B accuracy ∈ [0.2, 0.8] [ASSUMPTION — registered] → else the study STOPS at design cost, logged HELD — the primary is unmeasurable. Each gate can vary in principle (a stratum's 20-item B accuracy is a genuine measurement). A compositional-heavy draw cannot trip these gates — the EXP149a hole stays closed.

**Cost:** 40 × 15 = 600 forwards. Design cost: 193,800 (generation) + 600 (stratified dry run) + 4,800 (C+S pilot, §6) = **199,200 ≤ guard (g) 200k** [registered].

---

## 5. Design-record: hardened-compositional stays excluded (not a procedure)

**Carried design-record finding [FACT, LOG-4973]:** validity constraint (v2) ("every gold is a single token under the Pythia tokenizer") fails literally — all 40 closed-pool entities are 2 BPE tokens under Pythia (' Zorp' → ['ĠZ','orp'], verified offline, zero forwards) — while (v4) pins the closed 40-entity pool. (v2)-literal and (v4) are jointly unsatisfiable on the registered model+pool; no pool subset or model change satisfies both. This draft does not reconcile (v2)/(v4) — that reconciliation is a deferred, unlicensed lane (LOG-4977). No hardened-compositional strata, gates, or secondary statistics are registered here.

**EXP148's transitive recipe is the instrument [DEFINITION]:** bench construction carries EXP147/148 §5.1 (transitive) verbatim; the instrument is the measured one, not a repaired one.

---

## 6. Power and decision machinery (carried from the signed EXP150 pre-reg, re-keyed to n=380)

**Worth-it gate (Law #15, 7 points):**
1. **Exact question [HYPOTHESIS]:** §3 — is the discipline gain depth-driven on transitive strata with a bench that can supply the design's own power bar (δ̂_T3 > δ̂_T2)?
2. **Decisions changed:** CONTINUE (§4 of the pre-reg): 95% CI for (δ̂_T3 − δ̂_T2) entirely above 0 AND transitive-3hop S−C one-sided p < 0.05 → dose-response supported; the capability entry gains a transitive-scoped depth axis. KILL: CI entirely ≤ 0 with per-level guards (d_s),(e),(f),(f′) PASS → the gain is not depth-driven on transitive strata. HELD: anything else. RUN-INVALID: apparatus guard trip — never a verdict.
3. **Cheapest test:** the EXP148 three-arm design (B: T_B=15; C, S: T=120 budget-matched) on a fresh transitive-only bench, 2 strata × 380 items = 760 items, frozen Pythia-410m, greedy, Δθ=0, preceded by the binding stratified Step-0 gate.
4. **Cost:** $0 CPU. **199,200 ≤ guard (g) 200k** (design, computed §4). Wall ≈ 9h at EXP148 rates — re-gated at Step 0 (guard (h) ≤ 72h).
5. **Mathematical license:** EXP148/EXP149/EXP150 pre-reg §§2–3 inherited unchanged — (a) first-token scoring [DEFINITION]; (b) WRITE/READ discipline definition [DEFINITION]; (c) budget-matched CoT control [DEFINITION] with guard (f′); (d) McNemar machinery [DEFINITION] with the S7-1 §2.2 Wald convention (SE = √[(b+c) − (b−c)²/n]/n).
6. **Quantitative predictions:** if depth-driven on transitive: δ̂_T3 − δ̂_T2 ≥ +0.10. If the breaking point holds: δ̂_T3 − δ̂_T2 ≤ 0. **Power licenses:** pre-reg §2 — the registered true-power band is [0.74, 0.88] over the design d-range [0.30, 0.40]; the bench-size STOP floor is the band floor **0.74**; whether to run at the §2 zero-margin is the CEO's Law #15 call (registered honestly here; the call is not this document's).
7. **Breaking points:** §3 — plus the binding stratified Step-0 gate (§4) and the registered bench-size STOP rule (pre-reg §2): a (d-T*) trip STOPS the study at design cost; a Step-0 registered power < 0.74 (pilot keying) or a first-block power < 0.74 (block keying) STOPS at that point, logged HELD — computations, not choices.

**Why this is worth doing [INTERPRETATION]:** the primary is the cleanest remaining test of whether the program's first capability entry is depth-driven, now asked on a bench that can supply the design's own power bar at the priced discordant rate. A KILL is a sharp boundary (pooled/headroom-driven gain, not depth-driven); a CONTINUE genuinely extends the entry with a depth axis. A second HELD closes the apparatus line honestly.

---

## 7. Feasibility

**Compute:** $0 CPU. 199,200 design forwards ≤ guard (g) 200k. Wall ≈ 9h at EXP148 rates — re-gated at Step 0 (guard (h) ≤ 72h, throughput probe carried). Never self-escalate to GPU.

**Env:** the EXP149 lane restored the EXP148 CPU stack family in `~/workspace/.exp149-venv` (torch 2.14.x+cpu, transformers 5.17.0, numpy) — the execution lane re-verifies and records its own manifest (Law #13), reusing the venv if intact. Weights from local caches only — no HF Hub contact at execution.

**Model:** frozen Pythia-410m. Greedy decoding. Δθ=0 verified by pre/post state-dict hash (guard (a)). Model revision resolved programmatically at Step 0 from cache (expectation `9879c9b5f8bea9051dcb0e68dff21493d67e9d4f` — carried, re-resolved not transcribed).

---

## 8. Open items for the independent Law #14 reviewer

1. **Bench-size flag:** the literal "4 strata × 380" reading of the LOG-4977 prose is cost-infeasible (393,000 > 200k, computed §2); this draft carries 2-strata × 380 delivering the ruling's operative n_T2=n_T3=380. Is the guard-(g) precedence reading (numbered constraint over prose) the right disposition, or should the reviewer insist the draft hold for a CEO amendment first?
2. **Zero margin at d=0.40:** registered power 0.7429 vs the 0.74 floor — a 0.003 margin. Is registering the floor at the band floor (E3 precedent) correct here, or should the floor sit below the observed datum by a registered margin?
3. **Design d-range extension:** [0.30, 0.40] prices the EXP150 block datum. Is extending the carried d-range on prior data a Law #9 risk (the design's power bar now depends on a datum from the earlier run), or is it the honest pricing the cull's option (a) describes?
4. **Seed-derivation rule:** construction 151001; dry-run = construction + 11; pilot = construction + 23 (registered at design, no execution-time choice). Does this satisfy the A2 advisory?
5. **Second-HELD standing-down:** the draft registers that a second HELD is a design-debt finding licensing no further re-attempt. Is that the right terminal registration, or does it over-constrain a future CEO?

---

## Fixes applied (Law #14 review repair lane, 2026-10-09)

- **E1:** four operative-text "[For CEO disposition]" flags (design §2 cost-feasibility / cost-carry / zero-margin; pre-reg §6 item 2) converted to the recorded dispositions — CEO disposition LOG-4979: (1) the 2-strata 760-item design is accepted; the LOG-4977 "4 strata × 380" prose was a transcription error; guard (g) needs no amendment. (2) the worth-it call is priced at the 199,200-forward design cost — ACCEPTED. (3) the 0.74 floor stands as the band floor (E3 precedent); the worth-it call at the priced cost is ACCEPTED. Each edited paragraph marked [Fix E1, Law #14 review 2026-10-09]. (Independently re-verified this lane: no "[For CEO disposition]" markers remain in operative text.)

---

*Design draft finalized 2026-10-09 (Law #15 packet lane; license LOG-4977). Status: DRAFT — NOT SIGNED. NOT EXECUTED. NO NUMBER MINTED. No forwards run. Companion: `EXP151_PREREG_DRAFT_2026-10-09.md`. Awaited: independent Law #14 review of both drafts → CEO Law #15 SIGN-and-mint → execution authorization (Step-0 gates first). Execution NOT licensed by this document.*
