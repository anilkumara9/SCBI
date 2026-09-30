# Pre-registration: B2 — EVAL: Label-free E-step Validity (bridge-ranking)

**Status:** DRAFT pre-registration. Licenses nothing. No model runs, no experiment number minted (EXP135 provisional only), no signed protocol touched, no GPU contact, no commits, no pushes. $0 CPU.
**Drafting lane:** LOG-4839 (pre-assigned by the CEO). **Source:** `research/innovation/SPRINT_2026-09-30_POST_TGA.md` §B2 (worth-it gate passed, ranked #2).
**Launch chain:** independent Law #14 review of this exact file → fix-verification (if fixes required) → CEO launch decision → execution under a minted experiment number. This lane stops at the draft.

**Governing laws:** Law #2 (no invented numbers — every constant below is pinned or executor-verified-from-record, never improvised), Law #4 (no post-hoc hypothesis shifts — the bars below are binding; non-resurrection audit §6), Law #6 (frozen backbone Δθ=0), Law #7 (zero data leakage — bench labels never touch any score), Law #9 (metrics registered before any output is inspected), Law #11 (observation vs interpretation separated throughout), Law #13 (deterministic reproducibility — seeds, hashes, environment manifest pinned below), Law #15 (worth-it gate §5).

**Epistemological labels** per `AGENTS.md` §5 ([HYPOTHESIS], [FACT], [OBSERVATION], [ASSUMPTION], [INTERPRETATION], [CONJECTURE]) are used throughout.

---

## 0. The breaking point (read first)

**[HYPOTHESIS]** At least one label-free score from the signed G/E/S loop specification ranks the known-causal bridge above 8 matched randoms — i.e., the E-step can rank candidate injection directions by causal efficacy without labels.

**Breaking point:** the normalized mean per-item Spearman correlation ρ̄\* between the score ranking and the registered causal ranking is ≤ 0.3 (bridge mean score-rank ≥ 3.8 of 9 — no ranking signal) → **KILL** "the E-step ranks candidates." The G/E/S loop as designed ends; the summit path needs an architecture rethink, not a better candidate generator.

**Drafting correction (caught here, not by review):** the sprint bet's CONTINUE bar (unnormalized Spearman ρ ≥ 0.7) is **mathematically unachievable** — with the causal ranking's 8-way tie at the bottom, the maximum tie-corrected Spearman is ρ_max = 0.5477 (derived §3.5). The bars below apply to the normalized statistic ρ\* = ρ/ρ_max, preserving the sprint's 0.7/0.3 intent on an achievable scale. The sprint's numbers are quoted in §5 as the superseded proposal; the §3.5/§3.6 bars are binding.

---

## 1. Hypothesis (one falsifiable sentence)

**[HYPOTHESIS]** The signed evaluator score S_E (LOOP_SPEC_DRAFT §2.2) — and at least one of its two components — ranks the bridge (registered causal rank 1) above 8 matched randoms (registered causal ranks tied 2–9) on the 60-item bench, with normalized mean per-item Spearman ρ̄\* ≥ 0.7 at one-sided permutation p < 0.05.

**Falsifiers:** per the §4 decision tree — CONTINUE if ρ̄\* ≥ 0.7 with p < 0.05 for the primary score; KILL if ρ̄\* ≤ 0.3; HELD if 0.3 < ρ̄\* < 0.7 or p ≥ 0.05; RUN-INVALID on apparatus failure (§3.7).

### 1.1 Why this experiment exists

The G/E/S loop's E-step (label-free evaluation of candidate bases) was signed as a specification (`theory/LOOP_SPEC_DRAFT.md`, sign-off LOG-3842) with its validity explicitly marked **[CONJECTURE]** — "unscored pending the ρ-gate." It has never been tested: EXP068 (the loop) was pre-registered and signed but its execution is GPU-gated and never ran. Every other component of the loop's premise has been attacked; the evaluator is the one load-bearing component whose validity is pure conjecture. If no label-free score can rank a known-causal direction above randoms, the loop cannot select — E is dead as designed, and no candidate-generation work (B1-class, B4-class) can rescue the architecture. If one can, the loop has a live evaluation component and E-guided selection designs are licensed.

### 1.2 The §H7 bridge-status disclosure (Law #11)

**[FACT]** The bridge is label-informed (constructed from target/foil unembedding rows). **[FACT]** LOG-204 ruled the bridge's positive-control status for autonomous-mechanism questions REVOKED (the §H7 demotion). **[FACT]** LOG-213 K1-EXONERATED the readout-tilt mechanism account ((a) 0/60, CP CI [0.0000, 0.0596]); the demotion is UNDER CEO RE-REVIEW, not irreversibly locked. **[FACT]** The bridge's causal efficacy is undisputed: +10pp, b=6, c=0, p=0.03125 on the official EXP077 GPU record (LOG-128).

**[INTERPRETATION]** B2 is an **evaluator-validity** question, not an autonomous-mechanism question. The E-step's job is to rank candidates by observed causal efficacy; it does not care *why* the anchor is causal. The bridge is therefore a valid causal-efficacy anchor for this question, with its mechanism explicitly out of scope (§8). If the Law #14 review rules otherwise, the draft — not the verdict — is what gets revised.

---

## 2. Exact question and the decision it changes

**Exact question [HYPOTHESIS]:** Can any label-free score from the signed LOOP_SPEC rank candidate injection directions by causal efficacy — specifically, does it rank the known-causal bridge above 8 matched randoms, measured by normalized mean per-item Spearman ρ̄\* against the registered causal ranking?

**Decision changed:**
- **CONTINUE** (§4): ρ̄\* ≥ 0.7 with one-sided permutation p < 0.05 for the primary score → "the E-step ranks candidates" survives; E-guided candidate-selection designs are licensed; the G/E/S architecture survives its most fundamental challenge.
- **KILL** (§4): ρ̄\* ≤ 0.3 → "the E-step ranks candidates" is dead; the G/E/S loop as designed ends (no selection without evaluation); the summit path needs an architecture rethink.
- **HELD** (§4): 0.3 < ρ̄\* < 0.7, or ρ̄\* ≥ 0.7 with p ≥ 0.05 → inconclusive; licenses nothing, kills nothing; the E-validity conjecture stays open but unlicensed.
- **RUN-INVALID** (§4): apparatus failure — the bridge artifact fails its pin, Δθ=0 fails, any score is degenerate (cannot discriminate), or the budget audit fails. Never a verdict on the hypothesis.

---

## 3. Method

### 3.1 Backbone, bench, environment [FACT / pinned]

- **Backbone:** frozen Pythia-410m, `device_map="cpu"`, float32, `model.eval()`, `torch.no_grad()` around ALL forwards. CPU-only by design ($0).
- **Δθ=0 procedure (pinned):** SHA-256 over tensor bytes with sorted `state_dict` keys, float32 (the EXP077/EXP084/EXP108 canonical convention). Hash asserted **before the first forward and after the last**; any mismatch → RUN-INVALID, exit 44. Expected pin: `ec276abe3902fab0166ce56c00de84c2c737c80af4f9c41a9cbe94e4ec38e0ed` (LOG-331).
- **Bench:** the 60-item EXP077 bench (the bridge's licensed bench — same items on which the causal anchor was measured). Provenance SHA-256 of the bench artifact asserted before any forward (executor reads the pin from the LOG-128 record chain at bundle build; recorded in the manifest). `len(bench) == 60` asserted.
- **View precondition (LOOP_SPEC_DRAFT §2.2, fix S2):** each item must expose (τ(x), {(e_i, σ_i)}) for the 5-vocabulary entity-frame substitution. Any item whose template/slot signature is unavailable is **excluded** and logged (Law #8); its views are never improvised. **Guard:** >6 exclusions (>10%) → bench mismatch → RUN-INVALID, exit 44.
- **Environment (Law #13):** torch==2.14.0+cpu, transformers==5.17.0 (the registered EXP106–EXP112 / EXP131-attempt-2 CPU environment); numpy/sklearn versions recorded in the worksheet; `torch.manual_seed(135031)` + numpy seed 135031; CPU thread count set and read back via `torch.get_num_threads()`, recorded.
- **Law #7:** bench ground-truth labels are used **nowhere** in this protocol — not in candidate construction (bridge from unembedding rows per the licensed record; randoms from a seeded RNG), not in any score (ŷ_j and M_j are target-free; μ_M/σ_M from unintervened margins), not in any selection. The only label-adjacent object is the bridge's *construction*, which predates this protocol and is not modified here.

### 3.2 The 9 candidates (pinned)

- **C1 — the bridge (causal anchor) [FACT]:** the output-bridge direction `normalize(E[t_target] − E[t_foil])` from the licensed record, injected at **layer 20** (the EXP077 bridge-arm site), with the α of the EXP077 official bridge arm. The exact vector artifact is SHA-256-pinned at bundle build time against the licensed record chain (LOG-128); the α value is read from LOG-128 at bundle build and recorded in the manifest. **If the record is ambiguous on either, the executor stops → RUN-INVALID (exit 44). Nothing is improvised** (Law #2).
- **C2–C9 — 8 matched randoms [ASSUMPTION]:** unit-norm vectors drawn i.i.d. from N(0, I_1024), normalized, seed 135008 (independent stream from the bench seed). "Matched" = unit norm (the injection operator's ‖v‖ = 1 convention) and identical site/strength/bench. Orthogonality to the bridge is NOT required; sanity check (no verdict weight): mean|cos| < 0.1 expected under the null.
- **Injection operator (signed spec §2.2):** h ← h + αB at layer 20, answer position, per view.

### 3.3 The label-free scores (signed LOOP_SPEC_DRAFT §2.2 — cited, not redefined)

For candidate B and item x, with m = 5 views (fixed = number of support vocabularies; spec §1.1):

$$C_{\mathrm{cons}}(B; x) = \frac{2}{m(m-1)} \sum_{1 \le j < \ell \le m} \mathbf{1}[\hat{y}_j(B) = \hat{y}_\ell(B)] \in [0,1]$$

(decision agreement across vocabulary-instantiated views; ŷ_j(B) = argmax over {t_target, t_foil} logits at the answer position under intervention);

$$\tilde{M}(B; x) = \mathrm{clip}\!\left(\frac{\bar{M}(B; x) - \mu_M}{\sigma_M},\, 0,\, 1\right)$$

(M̄ = mean self-margin over views; M_j(B) = top-1 minus top-2 logit over the full vocabulary — **target-free**; μ_M, σ_M = baseline unintervened margin mean/std on D_sup: 150 support items × 5 views = 750 unintervened forwards, computed once, cached);

$$S_E(B; x) = \lambda_c \cdot C_{\mathrm{cons}}(B; x) + \lambda_m \cdot \tilde{M}(B; x), \qquad \lambda_c + \lambda_m = 1.$$

- **PRIMARY score:** S_E at λ_c = 0.7 (the provisional default per EXP068's T3 tuning order). The decision tree fires ONLY on the primary (Law #9).
- **SECONDARY (diagnostic, no verdict weight):** S_E at λ_c ∈ {0.5, 0.9} (the spec's tuning grid corners); C_cons alone; M̃ alone. Reported with identical statistics for the Law #14 review's decomposition reading.
- **EXPLORATORY (no verdict weight):** probe-decodability delta (the sprint's third score — not in the signed spec; included so the review can see whether a non-spec score succeeds where spec scores fail).

### 3.4 The registered causal ranking [FACT / registered, not re-measured]

This protocol **does not re-measure causality** — it is a $0 measurement experiment on the evaluator; the causal side is registered from licensed results:

- Bridge: causal rank **1** — licensed: +10pp, b=6, c=0, p=0.03125, EXP077 official GPU record (LOG-128).
- Each random: causal ranks **tied 2–9** — licensed inertness: EXP077's random arms ΔM=0; EXP131's 8 random injection arms ΔM=0 across 10 prompts (binding KILL, LOG-4832).

The ranking is therefore {bridge: 1, randoms: tied at mean rank 5.5}. **[ASSUMPTION]** The 8 fresh randoms are causally inert like their licensed predecessors. This assumption is NOT tested here (that would be a different experiment); if it is false, the KILL reading weakens symmetrically — recorded in §8.

### 3.5 The Spearman computation (exact, with the tie correction derived)

Per item i (i = 1..60): rank the 9 candidates by the primary score (ties within score ranks broken by the spec's rule: higher C_cons, then lower candidate index). Let k_i ∈ {1..9} be the bridge's score-rank.

**[THEOREM — derived, not assumed]** With the causal ranking's 8-way tie, the tie-corrected (Pearson-on-average-ranks) Spearman per item is:

$$\rho_i = (5 - k_i) \cdot 0.136931\ldots$$

taking the 9 values {0.5477, 0.4108, 0.2739, 0.1369, 0, −0.1369, −0.2739, −0.4108, −0.5477}. **Maximum achievable ρ_max = 0.5477** (bridge ranked first), minimum −0.5477. Derivation: causal ranks [1, 5.5×8] (mean 5, var 2); score ranks a permutation of 1..9 (mean 5, var 20/3); cov = 0.5(5−k_i); ρ = 0.5(5−k_i)/√(40/3).

**Normalized statistic:** ρ\*_i = ρ_i / ρ_max = (5 − k_i)/4 ∈ {1.0, 0.75, 0.5, 0.25, 0, −0.25, −0.5, −0.75, −1.0}. **Primary endpoint:** ρ̄\* = (1/60)Σρ\*_i.

**Null distribution (exact specification):** under H0 (scores carry no causal information), each item's bridge score-rank k_i is uniform on {1..9}, independent across items. One-sided p = P(ρ̄\*_null ≥ ρ̄\*_obs) by Monte Carlo with B = 200,000 draws, seed 135031 (independent stream), MCSE reported. (Exact 9^60 enumeration is infeasible; B = 200,000 gives MCSE ≤ 0.0012 on p near 0.05.)

### 3.6 Decision bars with statistical license

| Branch | Trip condition | Reading |
|---|---|---|
| CONTINUE | ρ̄\* ≥ 0.7 **and** one-sided permutation p < 0.05 (primary score) | "The E-step ranks candidates" survives; E-guided selection designs licensed |
| KILL | ρ̄\* ≤ 0.3 (primary score) | "The E-step ranks candidates" is dead; the G/E/S loop as designed ends |
| HELD | 0.3 < ρ̄\* < 0.7, **or** ρ̄\* ≥ 0.7 with p ≥ 0.05 | Inconclusive; licenses nothing, kills nothing |
| RUN-INVALID | any §3.7 guard fires | Apparatus failure; never a verdict on the hypothesis |

Bar semantics: ρ̄\* ≥ 0.7 ⟺ bridge mean score-rank ≤ 2.2 (the sprint's "ranks the bridge at the top" intent, achievable scale). ρ̄\* ≤ 0.3 ⟺ bridge mean score-rank ≥ 3.8 (no ranking signal — worse than top-3 placement on average). The p < 0.05 conjunct on CONTINUE prevents a high-but-noisy ρ̄\* from licensing architecture decisions (Law #9: magnitude and significance bind independently, per the EXP070 precedent).

### 3.7 Guards and breaking points (trip conditions + exit codes)

- **(a) Δθ=0:** SHA-256 pre/post mismatch → RUN-INVALID, **exit 44**.
- **(b) Bridge pin:** bridge artifact SHA-256 mismatch vs the licensed record at bundle build → RUN-INVALID, **exit 44**. (The anchor must be the licensed bridge, not a lookalike.)
- **(c) Bench pin:** bench SHA-256 mismatch or len ≠ 60 → RUN-INVALID, **exit 44**.
- **(d) View-precondition exclusions:** >6 items excluded → RUN-INVALID, **exit 44**.
- **(e) Degeneracy (the EXP131 blind-tap lesson):** if ANY score (primary or secondary) has zero variance across all 9 candidates on ≥30/60 items, the evaluator cannot discriminate — apparatus void → RUN-INVALID, **exit 44**. The per-item score distributions are archived regardless (Law #8).
- **(f) Budget audit:** forward-pass ledger must equal 9×60×5 (intervention) + 300 (unintervened cache) + 750 (D_sup baseline) = 3,750 ± 0 accounted passes; any unaccounted forward → RUN-INVALID, **exit 44**.
- **(g) Readout-sensitivity positive control (mandatory since the EXP131/133 rehabilitation):** inject a fixed random vector (seed 135008, independent draw) and require the readout displacement ratio ∈ [0.99, 1.01]; miss → the readout tap is blind → apparatus-void, **exit 44**.
- **(h) Clean completion:** all guards pass → executor computes the endpoint, prints the verdict per §4, **exit 0**.

### 3.8 What is NOT measured here

Causal efficacy of any candidate (registered, §3.4); the G-step (candidate generation); the S-step (selection rule); λ tuning (λ_c = 0.7 provisional); multi-iteration loop dynamics; any backbone other than frozen Pythia-410m; any bench other than the 60-item EXP077 bench.

---

## 4. Falsification decision tree

**Precedence:** RUN-INVALID > KILL > CONTINUE > HELD. (Apparatus failure preempts all substantive verdicts; KILL preempts CONTINUE on exact-boundary data — a bar met exactly is met.)

1. Any §3.7 guard fires → **RUN-INVALID** (exit 44). Report which guard, with the numbers.
2. Else, ρ̄\* ≤ 0.3 (primary) → **KILL** "the E-step ranks candidates." Licensed reading: the signed evaluator cannot distinguish the known-causal direction from randoms by label-free scores; the G/E/S loop as designed has no working selection step. DOES NOT LICENSE: any claim about non-spec scores (exploratory §3.3 reported separately), any claim about other benches/backbones, any resurrection of killed causal families.
3. Else, ρ̄\* ≥ 0.7 and p < 0.05 (primary) → **CONTINUE** "the E-step ranks candidates." Licensed reading: the loop has a live evaluation component; E-guided candidate-selection designs are licensable as new pre-registrations. DOES NOT LICENSE: full-loop success (G and S untested), any capability claim, any generality beyond this bench/backbone.
4. Else → **HELD.** The E-validity conjecture remains exactly where it was: conjecture.

The secondary scores' ρ̄\* values are reported in the same table with identical p-values, labeled [DIAGNOSTIC — no verdict weight]. If a secondary clears the CONTINUE bars while the primary does not, the reading is HELD with a noted decomposition anomaly — never a silent promotion (Law #4).

---

## 5. Law #15 — the worth-it gate (7 points)

1. **Exact question:** Can any label-free score from the signed LOOP_SPEC rank candidate injection directions by causal efficacy — specifically, does it rank the known-causal bridge above 8 matched randoms?
2. **Decision changed:** CONTINUE the G/E/S loop's E-step (→ licenses E-guided selection designs) vs KILL it (the loop as designed ends; architecture rethink) vs HELD (conjecture stays open, unlicensed). The verdict is mechanical (§4).
3. **Cheapest test + cost:** 9 candidates × 60 items × 5 views = 2,700 intervention forwards + 1,050 cached baseline forwards = **3,750 forward passes, $0, ~2h team CPU** (the sprint's "~1h" estimate is corrected here — 3,750 CPU forwards at measured EXP131-attempt-2 throughput). No GPU. Nothing cheaper discriminates: fewer views breaks the spec's m=5; fewer items breaks the bench pin; fewer candidates breaks the ranking.
4. **Mathematical license:** the signed `theory/LOOP_SPEC_DRAFT.md` (E-validity explicitly [CONJECTURE] — untested, not killed, LOG-3842); the bridge as a measured causal anchor (+10pp, p=0.03125, EXP077 official); rank statistics need no labels (Law #7 clean — ŷ_j, M_j, μ_M/σ_M are all target-free). **Quantitative prediction:** if the E-step works, ρ̄\* ≥ 0.7 (bridge mean score-rank ≤ 2.2). **Breaking point:** ρ̄\* ≤ 0.3 (bridge mean score-rank ≥ 3.8) → KILL.
5. **Non-resurrection audit:** §6 — E-validity was never tested; no killed family asks the evaluator-ranking question.
6. **Summit filter:** B2 is architecture-critical, not capability-positive. The G/E/S loop is the program's only path to autonomous basis invention (the summit mechanism); E is its untested load-bearing link. A KILL retires the architecture before more candidate-generation work spends against it; a CONTINUE gives every downstream bet (B1-class, B4-class) a licensed selection step. No candidate claims consciousness, superhuman achievement, or generality beyond its bench.
7. **Falsification-first:** the KILL branch is the prior — the program's uniform experience is that label-free structure does not track causality (the Decodability Gap). The draft is written to make the KILL easy to earn and the CONTINUE hard.

---

## 6. Non-resurrection audit (Law #4)

**The staleness re-diff (LOG-4834/4838 lesson) was run before a word of this draft was written:** full-log grep for (a) any execution testing label-free E-step validity, (b) any Spearman ranking of candidates against a causal ranking, (c) any bridge-vs-randoms ranking by label-free scores. **Result: clean.** E-validity stands as [CONJECTURE] since the LOG-3842 sign-off (2026-09-23); EXP068 (the loop) was signed but its execution is GPU-gated and never ran; the log's Spearman hits belong to unrelated tests (EXP083/084 evaluator-monotonicity, curvature correlations — different questions, different statistics). The B1 lane's "B2 is clean" recommendation (LOG-4838) was treated as a claim to verify, not a fact — verified by independent re-diff.

**Killed families and why B2 does not resurrect them:**
- EXP107 (H3/LFH), EXP114, EXP125, EXP126, EXP129 (closed-loop), EXP131 (TGA one-shot), EXP133 (GEOSTEER): all test whether injected directions **move decisions** (causality). B2 tests whether label-free scores **rank** directions by their registered causality — a measurement question about the evaluator, asked nowhere in the corpus. Different claim class under the program's central dissociation (decodability ≠ causality extends to: rankability ≠ causality).
- EXP098 (composition PIVOT): B2 uses single-site injection only (layer 20); no composition premise, no overlap with the fenced premise.
- H7_EVALID (2026-09-29, SUMMIT_ROUND2): a different H7 (elicitation validation of structured-output protocols) — naming collision only, zero question overlap.
- The §H7 bridge demotion (LOG-204, under CEO re-review after K1-EXONERATED LOG-213): disclosed in §1.2; B2's anchor is causal *efficacy* (undisputed), not autonomous mechanism (the demoted question).

**Novelty position: N1 (Known Combination).** No E-validity test exists in the corpus or — per the sprint's audit — in the adjacent literature surveyed. The ranking design is standard; the application to the loop's E-step is new.

---

## 7. Cost and honesty

- **Compute:** 3,750 forward passes, CPU-only, $0. No GPU contact at any stage.
- **What constrains this protocol:** the signed LOOP_SPEC_DRAFT (scores, m=5, view construction); the licensed record chain (bridge vector, α, bench); the five permitted verdicts; the exit-code discipline (§3.7).
- **Honest limitations:** (i) the causal ranking is registered, not re-measured — if the 8 fresh randoms are not inert, the KILL reading weakens (§3.4 assumption recorded); (ii) n=9 candidates makes the per-item statistic coarse — power comes from 60 items, and the p < 0.05 conjunct is load-bearing on CONTINUE; (iii) λ_c = 0.7 is provisional (EXP068's T3 default), not tuned — a CONTINUE at 0.7 does not license other λ values; (iv) the sprint's "~1h" cost estimate was optimistic — corrected to ~2h here.

---

## 8. What this protocol does NOT claim

- That the bridge is an autonomous mechanism (the §H7 question — explicitly out of scope, §1.2).
- That a CONTINUE validates the G-step, the S-step, or the full loop (untested).
- That the E-step generalizes beyond frozen Pythia-410m / the 60-item bench.
- That label-free evaluation is possible in general (a CONTINUE licenses E-guided *designs*, not the general claim).
- Any capability, consciousness, or superhuman-cognition claim.

---

## 9. Deviations (complete list)

(none — draft has not executed)
