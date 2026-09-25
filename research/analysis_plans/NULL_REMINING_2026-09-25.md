# NULL RE-MINING — 2026-09-25

**Agent:** NULL RE-MINING agent, reporting to CEO (Nova), under the 30-Day Autonomous Campaign Charter (Lane 3).
**Mission:** Re-mine primary null/kill/retraction artifacts with fresh mathematics. Every null is ore.
**Status labels:** per AGENTS.md §5. All findings below are [OBSERVATION] (exploratory re-mining) unless tagged; nothing here is licensed — follow-ups need pre-registration.

**Artifacts (read-only, never modified):**
- `experiments/runs/EXP091_clm8b_falsifier_v3/out/exp091_embeddings.npz` — state/actA/actC (60×1024, float32), ids, phrasing. Pythia-410m, layer 20. Mode=real. Registered verdict KILL (31/60, p=0.4487), adopted LOG-362.
- `experiments/runs/EXP091_clm8b_falsifier_v3/out/exp091_report.json` — per-item cosA/cosC/correct/phrasing.
- `experiments/runs/EXP077_cone_vs_line/exp077_vectors.pt` — v_hat, v_hat_c, mu, u_list, q_list, r_vec, B_wrong, B_perp_basis (1024-dim, Pythia-410m layer 20 — same space as EXP091 embeddings).
- `experiments/runs/EXP077_cone_vs_line/exp077_results.json` — NEITHER: all static variants ΔM=0, p=1.0; bridge +10pp (p=0.03125).
- `experiments/runs/EXP065_coordinate_alignment/exp065_results.json`, `experiments/runs/EXP066_pythia410m_replication/` — retraction records (raw cosine ~0.7, post-Procrustes ~0). Aggregates only; no embedding artifacts (forensic fact, LOG-097).
- EXP070: primary artifacts live in the Kaggle notebook outputs only (no repo mirror); recorded verdict BRANCH (c2) UNINFORMATIVE, bridge C7 +16.67pp (b=10,c=0,p=0.001953).

**What `state`/`actA`/`actC` are (from the extraction code, read not trusted):**
- `state[i]`: layer-20 final-token hidden state of the premise sentences (contextualized).
- `actA[i]` / `actC[i]`: layer-20 final-token hidden state of `" "+A` / `" "+C` encoded STANDALONE (single token, no context).
- Registered instrument: argmax(cos(state,actA), cos(state,actC)).

---

## PART 1 — PRE-COMMITTED ANALYSIS PLAN (written BEFORE any analysis ran)

Anti-p-hacking rule: the eight analyses below run exactly once as specified. Anything conceived after seeing results goes in PART 3 (post-hoc observations), clearly labeled, with no formal tests. ~12 formal tests total; all p-values reported raw AND Holm-corrected; interpretation conservative. Exploratory re-mining — no result here licenses a claim.

**A1. Margin calibration.** Point-biserial r(|cosA−cosC|, correct) with 95% CI (Fisher z). Pre-committed reading: |r|<0.2 → margins carry no correctness information beyond the registered null.

**A2. Partition heterogeneity.** (a) Domain (planet vs element, parsed from item ids) × correctness: Fisher exact, α=0.05. (b) Hop-count (2-hop vs 3-hop, parsed from ids) × correctness: Fisher exact, α=0.05. (c) Target entity A (10 levels, 6 items each) × correctness: chi-square df=9, α=0.05. Wilson 95% CIs per cell (descriptive).

**A3. Phrasing association.** Fisher exact (phrasing × correctness), α=0.05. (Registered split means 0.50/0.533 already suggest null; this is the formal test.)

**A4. Spectral separability.** SVD of centered 60×1024 state matrix. Descriptive: effective rank (#σ > 1% of σ_max), variance explained by top-3 PCs. Tests: two-sample t-tests (Welch) on PC1/PC2/PC3 scores by correctness, Bonferroni α=0.05/3.

**A5. Unsupervised clustering.** k-means k=2 on standardized states (seed 0, 10 restarts); chi-square (cluster × correctness) df=1, α=0.05. Descriptive: silhouette, adjusted Rand index vs correctness.

**A6. Cross-projection onto EXP077 directions.** Same-space check required first (model/layer/dim). For each of v_hat, v_hat_c, mu, B_wrong, r_vec: point-biserial r(state·d̂, correctness) with 95% CI. 5 pre-committed correlations, Bonferroni-noted. [RATIONALE] EXP077's v_hat is the relational-concept direction from a different task's support set; static injection along it moved nothing (NEITHER). This asks whether it carries any signal in EXP091's embedding space anyway — a genuine cross-task geometric query, not a tautology.

**A7. Bridge-direction geometry.** (a) Descriptive: mean pairwise cosine among the 60 per-item bridge directions b_i = normalize(actA_i − actC_i); resultant length ||mean(b_i)|| (0=uniform … 1=identical). (b) ONE pre-committed test: 5-fold CV — mean bridge direction learned on train folds, sign of held-out state projection predicts correctness; accuracy vs 0.5, exact binomial, α=0.05. [NOTE] The bridge is label-informed by construction (Law #7); the CV version tests whether a STABLE foil→target direction exists that generalizes to unlabeled held-out states. The registered instrument (31/60) is the non-CV answer; this is the stability-generalization complement.

**A8. EXP065/066 structural note (records only).** No embedding artifacts exist — analysis from recorded aggregates. Question: what does "raw cosine ~0.7, post-Procrustes ~0" structurally license? (Procrustes finds the best rotation; if the 0.7 were rotationally-alignable semantic correspondence, alignment should preserve/increase it. Its collapse implies the raw similarity was never rotational — the precise structural content of the retraction.)

---

## PART 2 — RESULTS

All analyses ran exactly once as pre-committed. 15 formal tests; Holm correction over the full battery noted below. [OBSERVATION] throughout — exploratory re-mining, nothing licensed.

### A1. Margin calibration — STRONG ANTI-CALIBRATION [OBSERVATION]
- Point-biserial r(|margin|, correct) = **−0.68**, 95% CI [−0.80, −0.52].
- Mann-Whitney U (margins by correctness): **p = 1.05e-06**.
- Median margin: correct items 0.00031 vs wrong items 0.00090.
- Pre-committed reading (|r|<0.2 → no calibration) is violated in the strongest way: the instrument's "confidence" predicts INCORRECTNESS. Larger |cosA−cosC| → more likely wrong.

### A2. Partition heterogeneity
- (a) Domain (planet vs element) × correctness: Fisher exact **p = 0.0017**. Element 22/30 = 0.733; planet 9/30 = 0.300. Survives Holm (15 tests).
- (b) Hop (2-hop vs 3-hop): p = 1.0 (16/30 vs 15/30). Null.
- (c) Target entity (10 levels) × correctness: chi-square df=9, **p = 0.083** — not significant. Per-entity Wilson 95% CIs: Bronze 5/6 [0.44,0.97], Silver 5/6, Steel 5/6, Gold 4/6, Iron 3/6, Mars 3/6, Jupiter 2/6, Venus 2/6, Mercury 1/6 [0.03,0.56], Saturn 1/6. (Entity pattern mirrors domain; the test lacks power at n=6/entity.)

### A3. Phrasing association
- Fisher exact (phrasing × correctness): **p = 1.0**. A-first 15/30, C-first 16/30. Null, as registered.

### A4. Spectral separability
- Centered 60×1024 state matrix: effective rank 47 (>1% of σ_max); top-3 PCs explain 81.9% of variance.
- PC1 t-test by correctness: **p = 0.0005** (Bonferroni-significant). PC2 p=0.28, PC3 p=0.79.
- CONFOUND: r(PC1, domain indicator) = **+0.99**. PC1 IS the domain axis (planet-premise vs element-premise states). The PC1 "signal" is the A2a domain effect in spectral clothing — no independent structure.

### A5. Unsupervised clustering
- k-means k=2 (seed 0, 10 restarts): clusters [30,30]; cluster×correctness chi2 **p = 0.0019**; table [[9 correct/21 wrong],[22 correct/8 wrong]].
- CONFOUND: the clusters recover the domain split (same 30/30). Not independent structure.

### A6. Cross-projection onto EXP077 directions (same 1024-dim layer-20 space confirmed)
- v_hat (relational-concept direction): r = +0.05, 95% CI [−0.21,+0.30]. Null.
- v_hat_c (control): r = −0.07, CI [−0.32,+0.18]. Null.
- **mu (support-set mean): r = +0.39, 95% CI [+0.16,+0.59], p = 0.0018** (t=3.27). Survives Holm. CONFOUND CHECK: r(mu-proj, domain) = +0.30 — partially domain-driven, but within-element r = +0.42 (n=30) and within-planet r = +0.19. The residual within-element correlation is post-hoc and uncorrected — intriguing, not licensed.
- B_wrong: r = −0.15. Null. r_vec: r = +0.10. Null.
- [INTERPRETATION] EXP077's concept direction carries no signal in EXP091's space (consistent with the NEITHER). The mu correlation is the only cross-task hint and needs pre-registered replication.

### A7. Bridge-direction geometry (task item 2)
- Per-item bridge b_i = normalize(actA_i − actC_i): mean pairwise cosine = **+0.20** (sd 0.41); resultant ||mean(b)|| = **0.46**. The bridge directions are only weakly consistent across items — there is no single stable "target-minus-foil" axis in this space.
- 5-fold CV (mean bridge learned on train folds, sign of held-out state projection predicts correctness): **29/60 = 0.483, binomial p = 0.65**. Null.
- [INTERPRETATION] The bridge "works" in EXP070 (+16.67pp) and EXP077 (+10pp) ONLY as a label-informed, in-sample rescue: it is constructed per-item from the TRUE target/foil and never tested for generalization. The honest bridge-analog in EXP091's autonomous space — a cross-validated stable direction — carries no signal. This precisely bounds the bridge: it is a known-answer geometric construction, not a discoverable autonomous direction. (EXP070's primary artifacts live in the Kaggle notebook only — no repo mirror — so per-instance bridge re-mining there was impossible; recorded aggregates only.)

### A8. EXP065/066 structural note (records; no embedding artifacts exist — forensic fact)
- Recorded: raw cosine +0.7186/+0.6852; post-Procrustes +0.0032/−0.0118; Δcos −0.7154/−0.6971.
- Structural content: the Procrustes fit (rotation V1→Vk on the support clouds) can only preserve-or-improve genuine rotational correspondence. Its collapse to ~0 proves the raw ~0.7 was NEVER rotationally realizable — it was the shared anisotropy axis (all vocab-mean vectors pointing ~the same absolute direction), not cross-vocabulary semantic correspondence. The retraction's boundary claim is therefore mechanistically explained: the 0.7 was anisotropy, and anisotropy does not transfer under static injection.
- This is the SAME phenomenon as the EXP091 static bias (below): cos(mean-state, token) ≈ 0.20 for all entities — a shared mean direction that all embeddings align with, whose per-entity differences masquerade as signal.

### Holm summary
15 formal tests. Surviving Holm at 0.05: A1 (p=1.05e-06), A4-PC1 (p=0.0005, domain-confounded), A2a domain (p=0.0017), A5 kmeans (p=0.0019, domain-confounded), A6-mu (p=0.0018, partially confounded). Independent robust findings: **anti-calibration (A1)** and **domain asymmetry (A2a)**.

---

## PART 3 — POST-HOC OBSERVATIONS (conceived after seeing results; descriptive only, no confirmatory tests)

### P1. THE MECHANISM OF THE NULL: static-bias dominance (the single most important finding)
Decompose the decision variable d_i = cos(S_i,a_i) − cos(S_i,c_i), with M = mean normalized state and static pair-bias b_i = M·a_i − M·c_i (fixed per (A,C) entity pair, computable WITHOUT the item's state):
- r(b_i, d_i) = **+0.97**. The instrument's decision variable is 97% static pair-bias, ~3% item-specific.
- r(|b_i|, margin_i) = **+0.90**. The instrument's "confidence" is 90% static-bias magnitude.
- Static-bias rule alone (pick A iff b_i>0): 30/60 = 0.500; instrument: 31/60 = 0.517; agreement 95% (57/60). Items where the item-specific residual beats the static rule: 2; where it loses: 1. **Net contribution of item-specific relational information: +1/60 — indistinguishable from noise.**
- [INTERPRETATION] EXP091's instrument was never measuring relational reasoning. It measures per-pair static token-embedding anisotropy (how much each entity's token aligns with the average premise-state direction), plus noise. The KILL is therefore stronger than "no signal detected": the instrument is blind by construction — it cannot see relations, only static bias. The residual (the only place a relational signal could hide) is null.
- This also explains A1's anti-calibration: margin ≈ |static bias|. Large |bias| with wrong sign → confidently wrong (8 element pairs, 21 planet pairs have anti-bias); small |bias| → coin flip. Within elements the split is surgically clean: all 22 correct items have margin ≤ 0.00042; all 8 wrong items have margin ≥ ~0.001 (Spearman r = −0.60; planet side −0.03, null).
- The domain asymmetry (A2a) is a property of the bench's (A,C) pairings × static bias, not reasoning: element pairings happen to carry pro-A bias (73%), planet pairings anti-A bias (70%).

### P2. Recency hypothesis: KILLED
Geometric test (last-mentioned vs first-mentioned entity in the premise): 31/60 = 0.517 recency-consistent; mean(cosLast − cosFirst) = −0.00001 ≈ 0. The premise-final state does NOT systematically resemble the last-mentioned entity. (Phrasing was already null at A3; this kills the mechanism too.)

### P3. Level difference by domain (descriptive)
Mean cosines: planet items cosA/cosC ≈ 0.204/0.205; element items ≈ 0.176/0.176. Planet premise-states are overall more aligned with planet token embeddings — expected lexical-content effect (premises mention planets), but it does not help the decision (d is what matters, and d is bias-dominated).

### P4. mu within-element residual (unlicensed hint)
Within-element r(mu-proj, correct) = +0.42 (n=30, post-hoc). If real, EXP077's support-set mean direction carries weak cross-task signal. Pre-registered replication required before any interpretation.

---

## PART 4 — RANKED FOLLOW-UP HYPOTHESES

### H1 (top). Bias-subtracted residual instrument — "is there ANY relational signal under the bias?"
- **Precise question:** After removing the per-pair static anisotropy bias b_i (estimated by cross-fitting from DISJOINT items, Law #7-compliant — never the test item's own state), does sign(d_i − b_i) predict correctness above chance?
- **KILL/CONTINUE/PIVOT:** Kills or continues the "residual relational signal" hypothesis; determines whether EXP091's null is "instrument blind" (residual null → blind) vs "signal exists but was masked" (residual >chance → lead). Directly affects the program's read of the entire static-cosine family.
- **Cheapest falsifying test:** Cross-fitted residual accuracy on the EXISTING 60 items — $0 CPU, minutes, no new data, no GPU. (Exploratory re-mining computation is licensed under Lane 3; any CLAIM from it requires a fresh pre-registered EXP number.)
- **Mathematical license:** d_i = b_pair(i) + ε_i with b estimated out-of-fold. Under H0 (no relational signal), ε_i is symmetric noise → residual accuracy = 0.5. **Prediction:** residual ≈ 0.5 (extends the P1 finding). **Breaking point:** cross-fitted residual accuracy significantly >0.5 (binomial, pre-registered α) breaks the pure-bias model and opens a genuine lead.
- Status: exploratory computation permitted now; claim requires pre-registration.

### H2. Anisotropy-projected bridge — "is the bridge's rescue power anisotropy or geometry?"
- **Precise question:** Does the label-informed bridge (EXP070/077) retain rescue power after projecting actA/actC onto the orthogonal complement of the anisotropy axis M?
- **KILL/CONTINUE/PIVOT:** Kills the "bridge = genuine relational direction" reading (if rescue vanishes) or continues it (if rescue survives projection).
- **Cheapest falsifying test:** CPU geometric recomputation on EXP091 embeddings ($0); causal confirmation needs GPU re-run of the bridge condition (queued lane).
- **Mathematical license:** if bridge rescue is anisotropy, removing the M-component destroys it; prediction: rescue attenuates to ~null. Breaking point: rescue survives → genuine relational component.
- Status: exploratory, not licensed.

### H3. mu cross-task replication — "does the support-set mean direction generalize?"
- **Precise question:** Does projection onto EXP077's mu predict correctness on a FRESH relational bench (new entities, pre-registered), within-domain?
- **KILL/CONTINUE/PIVOT:** Kills the P4 hint (replication null) or continues it as the program's first cross-task geometric lead.
- **Cheapest falsifying test:** CPU-only replication using existing weights + new bench: 60 items × 1 projection — $0, ~minutes of compute once the bench is built.
- **Mathematical license:** H0: r=0. Pre-registered one-sided test at α=0.05, n=60 → needs r>0.21. Prediction under skepticism: r≈0. Breaking point: r>0.21 → lead.
- Status: exploratory, not licensed; requires new EXP number for any claim.

### H4. Popularity-balanced bench (methodological)
- **Precise question:** Do the (A,C) pairings systematically confound entity static-bias with the correct answer? Would a bench with bias-balanced pairings change any static instrument's verdict?
- **KILL/CONTINUE/PIVOT:** Informs all future bench design; kills the "bench is neutral" assumption if bias predicts the answer key.
- **Cheapest falsifying test:** Compute b_i for all possible pairings from existing embeddings; test b_i × answer-key association — $0 CPU, existing artifacts.
- **Mathematical license:** under a neutral bench, corr(b_i, correct_answer_i) = 0. Breaking point: significant correlation → bench confounded.
- Status: exploratory, not licensed.

### H5. Strategic read (not an experiment)
- None of the re-mined structure suggests a path to autonomous capability via static geometric readouts: they are anisotropy-dominated by construction (P1, A8). The program's capability bets properly live in the GPU queue (adaptive mechanisms: K2, EXP083/084/086-B) and in genuinely new pre-registered mechanisms — not in further re-mining of static cosine geometry. Re-mining has now characterized the null completely; diminishing returns beyond H1–H4.

---

**Provenance:** all numbers recomputed from primary artifacts in-session (numpy/scipy, seeds pinned); no artifact modified (read-only); $0 CPU. Pre-committed plan (Part 1) written before any analysis executed. Post-hoc section labeled per the anti-p-hacking rule.
