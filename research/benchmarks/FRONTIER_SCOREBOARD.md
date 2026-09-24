# FRONTIER_SCOREBOARD.md — the standing frontier scoreboard

*Owner: Track 9 (benchmark scientist). Enacted LOG-219 (campaign mode,
`research/RESEARCH_OPERATING_SYSTEM.md` §10). v1.0 — 2026-09-23, LOG-220.*

**Purpose (standing):** show, at all times, exactly how far SCBI is from the
frontier and what would constitute beating it. Every SCBI experimental
verdict is plotted here against the frontier on the same axes, with the same
honesty standards. No cherry-picking: if we trail, the board says so.

**Last literature re-check:** 2026-09-23 (LOG-220). Next due: 2026-10-23.

---

## 0. At-a-glance — frontier best vs SCBI best, gap in plain numbers

[INFERENCE]/[INTERPRETATION] — the honest headline. Tasks and model scales
differ across rows; the columns make that visible rather than hiding it.
Every frontier number below is Law-#3-verified (§6); every SCBI number is
repo-artifact-verified (§3).

| Axis | Frontier best (verified) | SCBI best on the same axis | Gap, plain numbers |
|---|---|---|---|
| Frozen-model inference-time capability (math reasoning) | **∇-Reasoner**: 80.4% MATH-500, Qwen-2.5-7B-Instruct, up from 71.2% greedy; matches GRPO at 10–40% fewer model calls. *PARTIAL* (venue + headline numbers rest on LOG-185) | No licensed capability result at any scale. Handover-era ceiling EXP070 C7: +16.67pp oracle-informed (160m), never a mechanism | **The frontier ships an 80.4%; we ship no number.** |
| Frozen-model inference-time capability (general reasoning, parameter-free) | **LatentMAS**: up to +14.6% accuracy, 70.8–83.7% token reduction, 9 benchmarks, training-free (ICML 2026 spotlight per paper comments) | Zero positive signals for autonomous steering (LOG-204) | **+14.6% vs no signal.** |
| Adaptive inference-time routing, same compute budget | **Meta-Reasoner**: +9–12% accuracy AND −28–35% inference time under the same compute budget (Findings ACL 2026 per LOG-185) | Nothing routed, nothing adapted; E-validity still [CONJECTURE] | **Gains + time cuts vs nothing to route.** |
| Training-free compute allocation | **DEER**: 19.1–80.1% shorter CoTs, +0.3–5.0% accuracy, 11 models / 10 benchmarks | No compute-allocation mechanism tested | **Demonstrated L2 vs untested.** |
| Inference-time search (coverage) | **LLM-Monkeys**: coverage scales log-linearly over 4 orders of magnitude; SWE-bench Lite 15.9%→56% at 250 samples (verifier-gated) | G/E/S/T loop: never discriminatingly tested; E-validity [CONJECTURE] | **A working scaling law vs an untested formulation.** |
| Search + self-evaluation (planning) | **ToT**: Game of 24, GPT-4: 4%→74% (BFS b=5, depth 3) | No planning/search result; EXP068 retired as-signed (Law #15 FAIL) | **4%→74% vs no result.** |
| Cheap decoding-time aggregation | **Self-consistency**: GSM8K +17.9% (PaLM-540B 56.5%→74.4%, 40 paths, majority vote) | EXP056 autonomous selection: +4pp, p=0.25, **not significant** | **+17.9pp significant vs +4pp non-significant.** |
| Static steering, decision flips | **ITI**: Alpaca TruthfulQA 32.5%→65.1% (+32.6pp) via label-trained head probes (NeurIPS 2023) | EXP077: **ΔM=0, p=1.0, N=60** (410m/L20) — five static rooms dead; G1 killed the QK-subspace mechanism | **+32.6pp (label-trained probes) vs exactly zero.** |
| Context-dependent steering | **SVF** (arXiv:2602.01654, Feb 2026): per-activation steering fields, multi-layer coordinated — *no headline number in the checked abstract* | Gated/conditional variants of our operator: **never tested** (survived EXP077's narrow kill by exemption, not evidence) | **A working 2026 method vs an untested exemption.** |
| Closed-loop representation control | **Activation-LQR**: LTV linearization + LQR feedback with tracking-error bounds, no training — *existence proof, no headline accuracy number in abstract* | CLLC candidate: narrowed distinction only, **never tested** | **Guarantees vs a narrowed claim.** |
| Selective-abstention reliability | **NoisyCoconut** (TMLR June 2026): unanimous latent-path agreement → error <15% on math reasoning via selective abstention | No reliability result of any kind | **<15% error vs no measurement.** |
| Dynamic vector composition | **RISER** (Findings ACL 2026): +3.4–6.5% avg zero-shot, 2–3× token efficiency vs CoT — *trained external router (Δθ=0-excluded, adjacent)* | No composition result | **+3.4–6.5% vs nothing.** |
| Label-free autonomous steering | **Nobody on the frontier has this either** (ITI needs labeled probes; RISER needs a trained router) | Zero positive signals (LOG-204) | **Tied at zero — this is the only axis where we are not behind, and it is the program's actual race.** |

**The headline gap [INFERENCE]:** on every published axis the frontier holds
working, verified numbers and SCBI holds a boundary map (negative results +
one demoted control). The program is not behind on one benchmark; it is
behind on the *existence* of any licensed autonomous capability. The single
axis where the frontier is also at zero — **label-free autonomous steering**
— is the only honest race SCBI can still win, and winning it requires
clearing D2's five conditions (§D2 of the adopted synthesis) at matched
compute, not matching the frontier's label-assisted numbers.

**What "beating it" does NOT mean:** matching a frontier number with a
label-informed construction (that is the bridge's error, LOG-197/204).
Beating the frontier means §4's per-family observation, which always
includes the label-use-class constraint (§2.1).

---

## 1. How to read this board

**Epistemic labels.** Every load-bearing claim carries FACT / INFERENCE /
HYPOTHESIS / SPECULATION on top of the repo's 10-label standard
(`AGENTS.md` §5; `TEAM_KNOWLEDGE_PROTOCOL.md` §3). Unlabeled load-bearing
assertions are treated as [CONJECTURE]/SPECULATION.

**Verification tags (Law #3).** VERIFIED = primary source supports the exact
claim as written (mechanism and/or figures, stated separately). PARTIALLY
VERIFIED = mechanism confirmed; specific figures or venue rest on an earlier
record (cited). UNVERIFIED = not supported by the checked source — narrowed
or withdrawn, never load-bearing. Never fabricated: no invented papers,
authors, DOIs, or numbers.

**The "same axes" columns.** Every row — frontier or SCBI — carries:
task · model/substrate · effect size with CI/N as reported · compute budget
(two-number forward-pass accounting where available; marked where the paper
does not report it) · label-use class (None / Train-probes / Per-item —
§2.1) · transfer tested (Y/N) · Δθ=0 compliance (Y / excluded-adjacent) ·
venue/status · verification · exact source. A row that cannot be filled is
marked, not guessed.

### 1.1 Label-use classes (the board's Law-#7 column)

[INFERENCE]/[INTERPRETATION]: the LOG-197 audit's binding lesson, now a
permanent scoreboard axis.

- **None:** the method uses no labels at any stage (e.g., self-consistency,
  LLM-Monkeys coverage, DEER).
- **Train-probes:** labels are used to *fit* a reusable component (probes,
  router, reward model) on a training split; the fitted component is then
  applied to held-out items without per-item label access (e.g., ITI's
  head probes, RISER's router, ∇-Reasoner's reward model). Generalization
  across items is the mechanism's license.
- **Per-item:** the intervention for item *i* is constructed from item *i*'s
  own answer/label (e.g., SCBI's bridge: normalize(E[target]−E[foil]) per
  item, proven 240/240 by the LOG-197 audit). This never generalizes by
  construction; it is a control, not a mechanism candidate.

A Per-item row may not be compared against a None row as "beating" it. Any
SCBI result that claims to beat a frontier row must match or beat the
frontier row's label-use class (None beats Train-probes beats Per-item only
when the task and compute are also matched — stricter class never loses to a
weaker one on this board).

## 2. The frontier — extracted from the adopted prior-art map (§D1) + field sweep

Source map: `research/synthesis/SYNTHESIS_A_J_REV2_2026-09-23.md` §D1, §B5–B6;
verification Appendix V (LOG-191, 2026-09-23); LOG-220 additions below.

### Family A — diff-in-means steering (static)

| Method | Task | Model(s) | Effect size (CI/N as reported) | Compute budget | Label-use | Transfer tested | Δθ=0 | Venue/status | Verification | Exact source |
|---|---|---|---|---|---|---|---|---|---|---|
| **ITI** (Li et al.) | TruthfulQA truthfulness | Alpaca (LLaMA-based) | 32.5% → 65.1% (+32.6pp) | Few hundred labeled examples for probe fitting; single forward pass + head shifts at inference | Train-probes | Y (trained probes applied to new items) | Y | NeurIPS 2023 (spotlight per secondary steering survey; venue not re-confirmed in primary fetch today) | VERIFIED (mechanism + headline numbers from arXiv abstract) | https://arxiv.org/abs/2306.03341 (checked 2026-09-23) |
| **CAA** (Rimsky et al.) | Behavioral steering (multiple) | Various | No headline decision-flip number in the checked source | Contrastive prompt pairs + inference-time addition | Train-probes (contrastive pairs) | Y | Y | ACL 2024 (long) | VERIFIED (mechanism) | https://arxiv.org/abs/2312.06681; https://aclanthology.org/2024.acl-long.828/ (App. V1) |
| **ActAdd** (Turner et al.) | Sentiment / detox steering | Various | Qualitative (sentiment shifts, single-pair data efficiency) | One contrastive pair; inference-time addition | Train-probes | Partial | Y | arXiv 2023 | VERIFIED (mechanism) | https://arxiv.org/abs/2308.10248 (App. V2) |
| **RepE** (Zou et al.) | Truthfulness reading + honesty control | LLaMA-2 (7B/13B/70B), Vicuna | Reading vectors: >90% accuracy distinguishing harmful/harmless (reported by secondary summaries — **not verified in the primary today**); headline TruthfulQA numbers likewise secondary-reported | Contrastive stimulus pairs; PCA on activation differences | Train-probes | Y | Y | arXiv preprint (v4 Mar 2025) | VERIFIED (mechanism from abstract); headline numbers PARTIALLY-VERIFIED-AT-SECONDARY (marked) | https://arxiv.org/abs/2310.01405 (abstract checked 2026-09-23) |

[INFERENCE]: Family A is the field's ablation baseline (synthesis §B6). Its
best decision-flip number (ITI +32.6pp) is label-assisted at the
Train-probes class.

### Steering Vector Fields (Feb 2026) — context-dependent steering

| Task | Model(s) | Effect size | Compute budget | Label-use | Transfer tested | Δθ=0 | Venue/status | Verification | Exact source |
|---|---|---|---|---|---|---|---|---|---|
| Multiple-choice + open-ended generation steering | Multiple LLMs | "Stronger and more reliable control than prior steering baselines" — **no headline number in the checked abstract** | Learned differentiable concept-scoring function; gradient defines per-activation direction; coordinated multi-layer intervention | Train-probes (learned boundary) | Y (across tasks) | Y (inference-time) | arXiv preprint, Feb 3 2026 | VERIFIED (mechanism, abstract) — upgraded from UNVERIFIED (LOG-220 fetch) | https://arxiv.org/abs/2602.01654 |

Consequence: the Sept-2026 sweep note is discharged — SVF is verified as a
2026 occupant of the context-dependent-steering slot. Its numbers are absent
from the abstract; a future literature pass should extract headline figures
from the full text.

### Family D — output-side dynamic optimization (frozen): ∇-Reasoner

| Task | Model(s) | Effect size | Compute budget | Label-use | Transfer tested | Δθ=0 | Venue/status | Verification | Exact source |
|---|---|---|---|---|---|---|---|---|---|
| Math reasoning | Qwen-2.5-7B-Instruct | 80.4% on MATH-500 (up from 71.2% greedy); matches GRPO at 10–40% fewer model calls than Best-of-N | Iterative test-time gradient descent on token logits (Differentiable Textual Optimization); gradient signals from LLM likelihood + reward model | Train-probes (reward model) | Y | Y (no weight updates) | ICLR 2026 per LOG-185 | PARTIALLY VERIFIED — mechanism from abstract (2026-09-23); the 80.4%/Qwen/GRPO figures + venue rest on the LOG-185 record | https://arxiv.org/abs/2603.04948 (App. V7) |

### Family E — closed-loop representation control (frozen): Activation-LQR

| Task | Model(s) | Effect size | Compute budget | Label-use | Transfer tested | Δθ=0 | Venue/status | Verification | Exact source |
|---|---|---|---|---|---|---|---|---|---|
| Activation steering toward semantic setpoints | (as reported in paper) | Formal tracking-error bounds — **existence proof; no headline accuracy number in the checked abstract** | Layer-wise Jacobians (LTV linearization); LQR feedback controllers computed offline, applied in closed loop; no offline training | None (model-based, Jacobians from the frozen weights) | Per-paper | Y | ICML 2026 per LOG-185 proceedings-listing check | VERIFIED (mechanism); venue rests on LOG-185 | https://arxiv.org/abs/2604.19018 (App. V8) |

### Family C — inference-time search + self-evaluation

| Method | Task | Model(s) | Effect size | Compute budget | Label-use | Transfer tested | Δθ=0 | Venue/status | Verification | Exact source |
|---|---|---|---|---|---|---|---|---|---|---|
| **LTPO** (Ye, Liang & Shan) | Per-instance latent optimization | Frozen LLM (per paper) | No headline number in the checked abstract | Online policy gradient on latent thought vectors; intrinsic confidence reward from the frozen LLM's own output distributions; no external supervision | None | Per-paper | Y | arXiv preprint; ICLR 2026 per paper footer | VERIFIED (mechanism) | https://arxiv.org/abs/2510.04182 (App. V10) |
| **NoisyCoconut** (Jerge & Evans) | Math reasoning w/ selective abstention | (per paper) | Unanimous latent-path agreement → error rate **<15%** via selective abstention | Controlled noise injected into latent trajectories (K=5, σ=0.1 are program [PINNED-CHOICE] operationalizations, not paper claims) | None | Per-paper | Y | **TMLR, June 2026 (published — live index verified)** | VERIFIED | https://www.jmlr.org/tmlr/papers/ (index checked 2026-09-23); https://arxiv.org/abs/2605.08221 (App. V12) |
| **Meta-Reasoner** (Sui et al.) | Reasoning-strategy routing | (per paper) | **+9–12% accuracy AND −28–35% inference-time reduction under the same compute budget** | Contextual multi-armed bandits over strategies (backtrack / change decomposition / restart) from a compact progress report, at inference time | None | Per-paper | Y | Findings of ACL 2026 per LOG-185 | VERIFIED (mechanism); venue rests on LOG-185 | https://arxiv.org/abs/2502.19918 (App. V9) |
| **PPLM** (Dathathri et al.) | Attribute-controlled generation | GPT-2 (per paper) | Attribute control with perplexity tradeoffs (2020-era; no modern headline on this axis) | Per-step hidden-state gradient updates guided by an external attribute classifier | Train-probes (external classifier) | Y | Y | ICLR 2020 | VERIFIED (mechanism) | https://arxiv.org/abs/1912.02164 (App. V3) |
| **Self-Refine** (Madaan et al.) | 7 generation/reasoning tasks | (per paper) | ~20% absolute average gain over one-step generation | Same LLM as generator + feedback + refiner, iterative | None | Per-paper | Y | NeurIPS 2023 | VERIFIED (mechanism); "plateau after 2–3 iterations / blind spots" withdrawn as factual (not in verified abstract), restated [HYPOTHESIS] | NeurIPS 2023 proceedings abstract (App. V4) |
| **ToT** (Yao et al.) | Game of 24 (+ Creative Writing, Mini Crosswords) | GPT-4 | Game of 24: **4% (CoT) → 74% (ToT)** | BFS/DFS over thought nodes (b=5, depth 3 reported), LLM self-evaluation of partial solutions | None | Task-specific | Y | arXiv 2023; NeurIPS 2023 camera-ready per secondary note | VERIFIED (mechanism + headline numbers from arXiv page) | https://arxiv.org/abs/2305.10601 |
| **Self-consistency** (Wang et al.) | GSM8K, SVAMP, AQuA, StrategyQA, ARC-c | PaLM-540B | GSM8K **+17.9%** (56.5% → 74.4%); SVAMP +11.0%; AQuA +12.2% | Majority vote over 40 sampled CoT paths | None | Y | Y | ICLR 2023 (per arXiv comments) | VERIFIED (numbers from arXiv listing) | https://arxiv.org/abs/2203.11171 |
| **LLM-Monkeys** (Brown et al.) | Coding, math, formal proofs; SWE-bench Lite | Llama-3 8B/70B, DeepSeek-Coder-V2-Instruct, Gemma | Coverage scales log-linearly over 4 orders of magnitude; **SWE-bench Lite 15.9% → 56% at 250 samples** | Repeated sampling (n up to 250/trajectory); precision requires a domain verifier | None (coverage); verifier-gated for precision | Y | Y | arXiv 2024 | VERIFIED | https://arxiv.org/abs/2407.21787 |
| **rStar-Math** (Guan et al.) | MATH, AIME | Qwen2.5-Math-7B, Phi3-mini-3.8B | MATH: **58.8% → 90.0%** (Qwen2.5-Math-7B); +4.5% over o1-preview; AIME 53.3% (8/15) | MCTS rollouts + process preference model; **4 rounds of self-evolution training** | None at test time | Y | **N — self-evolution trains the policy SLM + PPM (Δθ=0-excluded; adjacent art)** | arXiv 2025 | VERIFIED (mechanism + headline numbers) | https://arxiv.org/abs/2501.04519 |

### Family F — adaptive compute routing (frozen): DEER

| Task | Model(s) | Effect size | Compute budget | Label-use | Transfer tested | Δθ=0 | Venue/status | Verification | Exact source |
|---|---|---|---|---|---|---|---|---|---|
| CoT reasoning (10 benchmarks) | 11 reasoning LLMs | CoT length **−19.1–80.1%**, accuracy **+0.3–5.0%** | Training-free, confidence-gated early exit at reasoning transition points | None | Y (10 benchmarks) | Y | arXiv 2025 | VERIFIED | https://arxiv.org/abs/2504.15895 (App. V5) |

### Adjacent — trained-component / training-framework art (Δθ=0-excluded; constraints and comparators)

| Method | Why excluded | Headline number | Verification | Exact source |
|---|---|---|---|---|
| **RISER** (Ye et al.) | Trained external router (RL under task rewards); backbone frozen but a trained component exists | +3.4–6.5% avg zero-shot accuracy over base model; 2–3× token efficiency vs CoT, 7 benchmarks | VERIFIED (ACL Anthology page, 2026-09-23) | https://aclanthology.org/2026.findings-acl.226/ (Findings of ACL 2026) |
| **STARS** (Yang et al.) | Training framework (Jacobian Spectral Radius Regularization) | No capability number — used as a **constraint**: predicts frozen iterative latent loops gain-then-collapse without stabilization | VERIFIED | https://arxiv.org/abs/2605.26733 (App. V6) |

### Family I — training-free latent multi-agent collaboration: LatentMAS

| Task | Model(s) | Effect size | Compute budget | Label-use | Transfer tested | Δθ=0 | Venue/status | Verification | Exact source |
|---|---|---|---|---|---|---|---|---|---|
| 9 benchmarks (multi-agent latent collaboration) | (per paper) | Up to **+14.6% accuracy**, **70.8–83.7% token reduction** | Autoregressive latent-thought generation + shared latent working memory; lossless latent exchange, no text mediation | None | Y (9 benchmarks) | Y | ICML 2026 spotlight per paper comments | VERIFIED (mechanism); figures rest on the LOG-191 App. V11 verification | https://arxiv.org/abs/2511.20639 (App. V11) |

**Verification tally for v1.0 (Law #3): 19 VERIFIED + 1 PARTIALLY VERIFIED
(∇-Reasoner) + 0 UNVERIFIED.** SVF upgraded VERIFIED this cycle (mechanism;
numbers absent from abstract). Venue-only claims (∇-Reasoner, A-LQR,
Meta-Reasoner) rest on the LOG-185 record with the provenance split
declared; no verdict depends on a venue. Headline-number provenance gaps
are marked in-row (RepE numbers, SVF/A-LQR/LTPO numbers absent from checked
abstracts). If any becomes load-bearing for a verdict, it must earn a
V-record first (standing rule, App. V).

## 3. SCBI plotted on the same axes

The same columns. Nothing cherry-picked; the demotions are stated first.

### 3.1 What the program currently holds — the honest inventory

| Result | Task | Substrate | Effect size (CI/N as artifact-verified) | Compute budget | Label-use | Transfer tested | Δθ=0 | Status | Exact source |
|---|---|---|---|---|---|---|---|---|---|
| **Boundary I1** — representational–causal dissociation | Static cross-vocab injection | pythia-160m / 410m (corrected lineage) | Raw cross-vocab cosine ~0.7 → **ΔM=0 causal transfer under static injection** (Procrustes ledger claims of +0.129 retracted; actual JSONs −0.715/−0.697 — alignment destroyed) | As-run | Per-item (bridge lineage) for the positive side; None for the null side | N (boundary, not transfer) | Y | Supported (boundary observation; mechanism claim reframed as readout-misalignment-or-unknown) | `reports/adversarial_audit_exp065_exp066.md`; corrected ledger §2.2–2.4/§3 |
| **EXP077** — five static-geometry rooms dead | Cone at 4 angles, cone-vs-line, cone-vs-control, offset, radial grid (decision flips) | pythia-410m / L20 | **ΔM=0, p=1.0 throughout, N=60** | N=60 items; exact forward-pass count per run bundle (not re-verified today) | None | — (null) | Y | Supported (narrow license: unconditional 30° cone + α=1 offset killed; gated/conditional variants survive untested) | Official GPU record via LOG-128 (notebook mirror pending — disclosed) |
| **Bridge "rescue"** — DEMOTED control | Decision flips (bridge arm) | pythia-410m / L20 | Official: b=6, c=0, **ΔM=+10.00pp** (56.67%→66.67%), p=0.03125, N=60; smoke archive: 14/0/+23.33pp/p=0.000122 (never cross-compare — LOG-197) | N=60 | **Per-item** (provenance proven: 240/240, min \|cos\|=1.0000000) | N | Y | **DEMOTED per LOG-204 §H7 — under CEO re-review (not locked in) after K1-EXONERATED (LOG-213)** — retained as rescue control ("known-answer direction, NOT a mechanism control") pending the revisit; positive-control status REVOKED; Per-item class unchanged | `research/analysis_plans/LAW7_BRIDGE_AUDIT_REPORT_LOG197_2026-09-23.md`; LOG-204 ruling 1 |
| **EXP065/066 bridge arms** — demoted | Decision flips | 065: pythia-160m/L10; 066: pythia-410m/L20 | 065: 10/0, +16.67pp, p=0.001953125; 066: 8/0, +13.33pp, p=0.0078125 | As-run | Per-item | N | Y | Same demotion; label-assisted readout artifacts (Q2 Supported, narrow L1) | LOG-197 audit, E3/E4 |
| **EXP048** (P2 observation) | Decision flips | pythia-160m (artifact: `"model": "EleutherAI/pythia-160m"`) | 0.60 → 0.74, ΔM=+14pp, b=7, c=0, McNemar p=0.0078125 | As-run | Per-item (option-informed construction) | N | Y | P2 score observation; no matched modern baselines; NOT a capability claim | `experiments/runs/EXP048_regression_lock/exp048_regression_results.json` (App. V13) |
| **EXP049** | Multi-seed invariance | (handover-era) | Pooled 0.60→0.67, ΔM=+7pp, b=17, c=3, p=0.0012884, 95% CI [0.03,0.115]; per-seed seed-42 p=0.363 | As-run | Per-item | N | Y | Metadata verdict FALSIFIED_OR_WEAK | `experiments/runs/EXP049_multi_seed_invariance/exp049_multi_seed_results.json` (App. V14) |
| **EXP056** | Autonomous (unsupervised) selection | (handover-era) | 0.60→0.64, **+4pp, b=2, c=0, exact McNemar p=0.25 (one-sided) — not significant** | As-run | None (autonomous) | N | Y | SELECTION_BOTTLENECK_ACTIVE — the program's best autonomous number is a null | `experiments/runs/EXP056_autonomous_lifecycle/exp056_autonomous_results.json` (App. V15) |
| **EXP057** | Blind discovery | (handover-era) | 0.4083 vs 0.45 baseline, **−4.2pp** | As-run | None | N | Y | DISCOVERY_BOTTLENECK_PERSISTS | `experiments/runs/EXP057_blind_discovery/exp057_discovery_results.json` (App. V16) |
| **EXP058** | Basis transfer (causal→causal) | (handover-era) | 0.5333 vs 0.60 baseline, **−6.7pp** | As-run | None | N (transfer failed) | Y | TRANSFER_WEAK_OR_SPECIFIC | `experiments/runs/EXP058_basis_transfer/exp058_transfer_results.json` (App. V17) |
| **G1** — QK-null-space sentence killed | Weight-only QK/OV projection-energy audit, 48 downstream heads | pythia-410m weights (read-only, Δθ=0, $0) | B_agg Ē_QK=0.390 > random-unit-vector null 95th percentile; bridge Ē_QK=0.356 mid-null; 35/48 heads B_agg>bridge; cross-head r=0.27 | 0 forward passes | N/A (weight-only) | — | Y | **Refuted** (as a QK-subspace claim); surviving instrument: per-head table, restated around readout-coupled heads | `research/analysis_plans/G1_REPORT_2026-09-23.md` |
| **EXP079** | HALT_PROBE (probe feasibility) | CPU | max N_final=46 < 50 over ALL possible 75/75 splits — rule infeasible by construction | 0 GPU | N/A | — | Y | ACCEPT-WITH-FIXES; halt accepted | LOG-138 review; research log |
| **EXP070 C7** | Oracle ceiling | pythia-160m (corrected) | 10/0, +16.67pp, p=0.001953125 (mirror-pending) | As-run | Per-item (oracle) | N | Y | Oracle ceiling only — no autonomous content | LOG-110; LOG-197 (vector cell Underdetermined) |
| **K1** — readout-tilt falsification: **K1-EXONERATED** (LOG-213) | (a) cos(bridge, target row) vs 0.9 bar; (b) f/r flip diagnostic; (c2) swapped-scoring identity; D1 archived logit-shift | 160m/L10 + 410m/L20 archives | **All three primary runs Not supported — (a)-RULED-OUT: k=0/60, CP 95% CI [0.0000, 0.0596]** on EXP065/066/077-official; not one of 180 bridge directions reaches the 0.9 bar; EXP070 Underdetermined | $0 CPU, 0 forward passes | N/A (diagnostic) | — | Y | EXECUTED 2026-09-23. Tilt hypothesis Not supported at program level. Pre-registered consequence: §H7 demotion does NOT lock in (CEO revisits); K2 pilot LICENSED; Sprint-3 Stage-0s LICENSED; K3 CPU audit proceeds | `research/analysis_plans/K1_REPORT_LOG213_2026-09-23.md`, `K1_RESULTS_LOG213_2026-09-23.json` |
| **EXP082** — foil-suppression tilt: **EXP082-EXONERATED** (LOG-217) | Fresh battery, foil-suppression lemma + 0.484 mirror bound + joint-firing lemma | 160m/L10 + 410m/L20 archives | **Not supported — (f) k_f=0/60 on every run, CP 95% CI [0.0000, 0.0596]; (a)-contrast k_a=0/60; N_bothfire=0**; mean cosθ 0.9503/0.2775/0.2775 | $0 CPU, 0 forward passes | N/A | — | Y | EXECUTED 2026-09-23. Foil-suppression hypothesis KILLED. Static directional-readout story dead; rescue must come from the relational (t−f) readout effect or downstream transformation. Death-debt paid: S3-7 logged → LOG-221 | `research/analysis_plans/EXP082_REPORT_LOG217_2026-09-23.md`, `EXP082_RESULTS_LOG217_2026-09-23.json` |
| **S3-7** — spoiler-suppression archived-record analysis (LOG-221) | Foil-vs-third-token tabulation on rescued items | EXP065/066/077 archives | **Underdetermined** — no predicted-token labels in any archive; the pre-registered "labels absent" branch fired | $0, 0 forward passes | N/A | — | Y | Analysis complete; flipped to QUEUED with instrumentation spec (per-item top-5 tokens+logits, competitor identity, margin decomposition) | `research/analysis_plans/S37_SPOILER_ANALYSIS_LOG221_2026-09-23.md` |
| **EXP080 / EXP081** | G2 oracle ceiling; C-A donor transfer v2 | (Kaggle GPU when cleared) | 1,320 / 660 forward passes (weakest-grade ceiling ⇒ cheapest experiment) | GPU-dark | EXP080: Per-item ceiling (label-informed L1); EXP081: transfer | To be tested | Y | PRE-REGISTERED; §A.6 addenda ACCEPTED (LOG-210); gated on K1 verdict + CEO GPU clearance | `experiments/protocols/EXP080_LICENSE_ADDENDUM_LOG209_2026-09-23.md` etc. |

### 3.2 The program's position, stated without softening

[FACT]/[OBSERVATION]: the program holds **zero positive signals for
autonomous steering** (LOG-204 ruling 1 — stated plainly per the CEO's
order; unchanged by K1-EXONERATED, which exonerated the *tilt* account, not
the *label-use* fact). Its most-cited positive number (+10pp bridge rescue)
is a Per-item control whose §H7 demotion is under CEO re-review (LOG-213)
— the tilt accounts are dead on both ends (target-boost 0/60, K1;
foil-suppression 0/60, EXP082), and the live mechanism is the relational
(t−f) readout effect, still label-informed. Its best autonomous number
(+4pp, EXP056) is not significant. Its mechanism program is five dead rooms
+ one killed QK-subspace sentence + one retracted Procrustes claim + two
dead directional-readout hypotheses (K1, EXP082). Its live assets are: the
I1 boundary (a diagnostic instrument), the G1 per-head table
(a measurement-pruned instrument), the K2 pilot (LICENSED, awaiting CEO GPU
clearance), Sprint-3 Stage-0 pilots (LICENSED), the K3 CPU audit, and two
pre-registered GPU experiments still gated on CEO clearance.

[INFERENCE]: plotted on the same axes, SCBI does not trail the frontier by a
margin — it trails by *category*: the frontier has L1–L2 capability results;
SCBI has an L1 boundary map. The honest comparison is therefore not "our
+10pp vs their +32.6pp" (different label-use classes — §2.1 forbids it) but
"their None-class capability results vs our None-class nulls."

## 4. What would constitute beating it — per family, exact observations

Standing law (synthesis §D2): a result crosses from N1 to a genuine novelty
claim **iff** it simultaneously demonstrates, pre-registered: (1) per-instance
construction, (2) a transfer-validated internal evaluator, (3)
matched-compute superiority over Family C/D/E/F baselines (plus the pinned
M15 candidate-specific comparators at the Level-2 standard — lower 99.286%
CI > δ_min=0.05), (4) conditional computation (randomizing the feedback
signal must kill the gain), (5) specificity (Δ_valid − Δ_control > 0,
pre-registered). The rows below concretize that bar per family. Every row
assumes: pre-registered, frozen backbone (Δθ=0), label-use class None unless
stated, two-number forward-pass accounting, and the §2.1 rule that a
Per-item construction can never beat a None-class row.

| Family | The exact observation that would put SCBI ahead on the same axes |
|---|---|
| **A — diff-in-means steering** | A label-free, per-item-constructed direction that flips decisions at ΔM ≥ δ_min (lower 99.286% CI > 0.05, N powered per §G1b) on a held-out task where static CAA/ITI-style probes at matched forward-pass budget do not — with the specificity gap (Δ_valid − Δ_control > 0) against matched structural controls. Beats ITI's +32.6pp axis only if it also clears ITI's label-use class (None beats Train-probes). |
| **Steering Vector Fields** | A Δθ=0, parameter-free conditional steering rule (no learned concept boundary) that matches or beats SVF's reliability claim — same task family, matched compute — with the conditionality probe: randomizing the per-activation gate must kill the gain (D2 condition 4). |
| **∇-Reasoner (Family D)** | ≥80.4% on MATH-500 at equal model-call budget, without test-time gradients and without a reward model — i.e., beating a gradient-based optimizer with a gradient-free self-consistent mechanism, with conditionality demonstrated. Anything less is a replication of a 2026 occupant, not a novelty result (changed burden of proof, §D2). |
| **Activation-LQR (Family E)** | Closed-loop control of a frozen model with derived tracking-error bounds on a relational task (the CLLC narrowed distinction), beating its own matched-compute open-loop ablation — observer/controller/plant separation demonstrated, not asserted. |
| **LTPO** | Per-instance latent optimization with an internal (label-free) signal that beats pinned M15-LTPO at matched forward passes under the Level-2 standard — plus the conditionality probe (D2-4). |
| **NoisyCoconut** | <15% error on math reasoning via selective abstention at a matched or stricter abstention rate — or the same error without abstention — with the aggregation mechanism shown to be doing work beyond majority vote (specificity vs NoisyCoconut-style noise+consensus at matched compute). |
| **Meta-Reasoner** | ≥+9–12% accuracy AND ≥−28–35% inference-time reduction under the same compute budget, via a discovered (not hand-coded) strategy policy with a frozen policy scope — beating pinned M15-MetaReasoner at Level 2. |
| **PPLM / Self-Refine** | For PPLM's slot: per-step hidden-state control without any external label-trained evaluator. For Self-Refine's slot: >~20% absolute gain over one-step generation where the feedback provider is a *frozen-model verifier that counterfactually tests candidate interventions* (the §C5 open component) — E-validity demonstrated, not conjectured. |
| **ToT / Self-consistency / LLM-Monkeys** | A search/selection mechanism over *activation operators* (not output samples) that beats best-of-N / self-consistency / ToT-style search at matched forward-pass budget on the same task and substrate — with conditionality (D2-4) so it is not "search with extra steps." LLM-Monkeys' lesson applies: without a verifier, aggregation plateaus — the verifier is the load-bearing component. |
| **LatentMAS (Family I)** | +14.6% accuracy / 70–84% token reduction via latent collaboration **without** inter-instance latent exchange (bandwidth-isolation rule, §G4 condition (v): the compressed-payload control must not explain the gain) — i.e., winning on the representation claim, not the capacity account. |
| **RISER (adjacent)** | +3.4–6.5% avg zero-shot gains with a **parameter-free** router (no RL-trained component) — the Δθ=0-respecting variant must identify exactly what the trained router contributes that the parameter-free mechanism cannot. |
| **DEER (Family F)** | A compute-allocation result (early-exit or equivalent) that beats DEER's 19–80% CoT reduction / +0.3–5% accuracy band at matched compute on the same benchmarks — the forced baseline with teeth. |
| **rStar-Math (adjacent, Δθ≠0)** | Not a beatable row under the Δθ=0 boundary — it is excluded by Law #6. It stands as the scale of what *training-inclusive* test-time pipelines achieve (58.8%→90.0% MATH), i.e., the number that Δθ=0 methods are chasing without Δθ≠0's tools. |
| **The honest race (label-free autonomous steering)** | The frontier is at zero here too. Crossing: D2's five conditions simultaneously, label-use class None, at matched compute — the first licensed autonomous (label-free) steering result anywhere. This is the only row where "ahead of the frontier" is currently achievable without beating a published number. |

## 5. Update protocol (standing — LOG-219/LOG-220)

1. **Who updates.** Track 9 owns this file. If Track 9 is unstaffed, the
   Research Lead dispatches a benchmark agent **the same cycle** an
   experimental verdict lands — a verdict with no scoreboard row by the next
   standup is a process defect.
2. **What gets added, same cycle.** Every SCBI experimental verdict —
   Supported, Not supported, Inconclusive, Underdetermined, Refuted, halt,
   null — in §3's table format: experiment · task · substrate (model/layer)
   · N · metric · effect size + CI · forward-pass budget (two numbers:
   candidate passes + eval passes) · label-use class (§2.1) · transfer
   tested (Y/N) · Δθ=0 (Y/N) · status (live / demoted / retired) · exact
   artifact path. The frontier row it is compared against and the gap in
   plain numbers. **The no-cherry-picking rule:** nulls and halts are added
   with the same care as rescues; banned verdict-language
   ("interesting/promising/elegant/worth another experiment") never appears
   in verdict positions; if we trail, the board says so.
3. **Literature re-check every 30 days.** Track 4 runs the sweep; Track 9
   folds it in: new rows, corrected numbers, venue/status changes
   (e.g., the NoisyCoconut staleness lesson — never cite a stale status),
   and the "last literature re-check" date at the top. Every new record is
   Law-#3-verified before it enters a load-bearing row (earn-a-V-record
   rule, App. V).
4. **Stale-board = anomaly.** No update within 7 days of a new verdict, or
   30 days without a literature re-check → the daily health check flags it
   as an anomaly. The board is shown to the user alongside results in every
   standup.
5. **Versioning.** Dated versions (v1.0, v1.1, …) with a changelog below;
   the file is never rewritten silently.
6. **Consolidation rule.** Dated snapshot files in this directory
   (e.g., the LOG-222 analyst's `FRONTIER_SCOREBOARD_v1_2026-09-23.md`,
   `SCBI_VS_FRONTIER_2026-09-23.md`, `UPDATE_PROTOCOL_2026-09-23.md`,
   `PROGRESS_ANALYSIS_2026-09-23.md`) are preserved as historical
   records; this file is the single standing board at the §10-mandated
   path. On each update cycle Track 9 reconciles the snapshots into this
   file (recording divergences in the changelog) rather than maintaining
   parallel boards.

**Changelog.**
- v1.0 — 2026-09-23 (LOG-220): initial board at the §10-mandated path.
  20 literature records (19 VERIFIED + 1 PARTIALLY VERIFIED + 0
  UNVERIFIED); SVF upgraded from UNVERIFIED (mechanism verified via arXiv
  abstract); RISER verified via ACL Anthology; ITI / ToT / self-consistency
  / LLM-Monkeys / rStar-Math / RepE verified this cycle; SCBI rows plotted
  with the LOG-204 demotion and substrate corrections absorbed
  (EXP065/070 = 160m/L10). Consolidates the LOG-222 dated snapshot files
  (12-row sibling board + SCBI-vs-frontier + update protocol + progress
  analysis) into the single standing file — snapshots preserved as
  history. Post-write updates folded in before release: K1-EXONERATED
  (LOG-213), EXP082-EXONERATED (LOG-217), S3-7 Underdetermined (LOG-221);
  §H7 demotion status corrected to "under CEO re-review, not locked in."

---

## 6. Steelman, challenge, idea (LOG-220 — the top-lab bar)

### 6.1 Steelman — the strongest case against this scoreboard

*The board compares SCBI's 160m/410m toy-substrate results at N=60 against
frontier papers running 7B+ models with thousands of samples. The gap is a
budget artifact, not a mechanism verdict. Scoreboards that compare across
model scales flatter the frontier and demoralize the program — and the
"honest race" row concedes the whole game is unwinnable on the published
axes, which is a counsel of despair dressed as honesty.*

**Answered, not dismissed.** (1) The scale difference is *labeled in every
row* (the substrate column), not hidden — the gap statement is conditional
on scale, and §4's beating-it rows demand matched-compute comparisons, not
7B-vs-410m comparisons. The real bar for any SCBI claim was never
"∇-Reasoner's 80.4%" — it is the same-substrate forced baselines (best-of-N,
CAA, DEER-style routing on pythia-410m at equal forward passes), which the
program has never run. (2) The budget excuse covers *magnitude*, not
*existence*: DEER is training-free, NoisyCoconut is inference-only, A-LQR
needs only Jacobians, LTPO is parameter-free — the frontier's 2026 occupants
demonstrate that frozen-model inference-time capability exists *in
principle* at comparable budgets. "We're small" does not explain zero
licensed autonomous signals. (3) The "honest race" row is not despair — it
is the only row where the frontier's advantage (scale, labels, training)
does not apply, and therefore the only row where a small lab can win
outright. **Conceded:** the at-a-glance table should never be read as
"SCBI is 80.4% − 0% behind" — cross-scale arithmetic is meaningless, and any
future version that invites that reading fails its own honesty standard.

### 6.2 One challenge — the strongest falsification attempt against a live claim

**Target (live claim):** LOG-204's "the program holds ZERO positive signals
for autonomous steering," licensed via the LOG-197/204 demotion logic
(Per-item construction ⇒ rescue is a label-assisted artifact, not mechanism
evidence).

**The attack:** apply the demotion logic evenly and it dissolves Family A's
headline too. ITI — the frontier's best static-steering number (+32.6pp) —
trains its head probes on *labeled* truthfulness data. RISER trains its
router with RL under task rewards. ∇-Reasoner needs a reward model. If
label-informedness disqualifies mechanism evidence, the "static steering
works" premise of the entire published frontier collapses — and SCBI's
negative results would then be the honest frontier of the honest question,
*raising* the program's relative standing rather than lowering it. The board
as written lets the frontier keep its label-assisted numbers while SCBI's
label-assisted number is demoted — an asymmetry that flatters exactly the
occupants the changed burden of proof (§D2) says we must beat.

**The defense (why the demotion stands):** the asymmetry is real but the
*label-use classes* are not the same, and §2.1 exists precisely to make this
visible. ITI's labels fit a reusable probe on a training split; the fitted
probe is applied to *held-out items without per-item label access* —
generalization across items is the mechanism's license (label-use:
Train-probes). SCBI's bridge is constructed *per item from that item's own
answer options* (normalize(E[target]−E[foil]) per item, proven 240/240) —
the construction never faces a held-out item without its answer
(label-use: Per-item). Item-specific label use is strictly stronger
assistance than probe training, and the bridge was never given the transfer
test ITI passed. So the demotion is not asymmetric: it applies the same
rule (no Per-item construction may license a mechanism claim) to both. The
board marks ITI's +32.6pp as Train-probes on the same axis where it marks
the bridge Per-item — the comparison the board forbids (§2.1) is exactly
the one the demotion was designed to prevent. **Residual risk conceded:**
if a future audit shows ITI-style probes do not transfer without
item-adjacent leakage, the Family-A row gets demoted on this board too —
the rule cuts both ways by design.

### 6.3 One idea — a mechanism the corpus suggests but never tested

**Question.** The corpus never tested the STARS constraint on its own
operator: does repeated static injection at fixed readout show
gain-then-collapse with application depth (the STARS prediction for frozen
recurrence), flat-zero at all depths (the operator is dead in every
regime), or monotonic gain (the STARS constraint is refuted for this
operator family)?

**Mechanism (math before metaphor).** Let v be the EXP077 concept direction
at layer 20, applied as h ← h + α·v with renormalization between
applications, k = 1…5 successive applications with a full forward pass
between each (the closest frozen analogue of STARS's looped recurrence).
Pre-register the three-way partition on the decision-flip rate f(k):
(i) f(k) peaks then collapses → STARS constraint *Supported* for static
injection → the program's five dead rooms died in the wrong *regime*
(single application), and the stabilizer search (§C6's open question)
becomes the licensed next step; (ii) f(k) = 0 ∀k → the "regime-untested"
rescue narrative is *falsified* and the static operator stays dead with a
stronger license; (iii) f(k) monotonic → STARS constraint *Refuted* for
this family → re-opens the operator with a new discriminating question
(depth as a degree of freedom EXP059–077 never explored).

**Why it matters.** Every static negative in the corpus (EXP059–066, EXP077)
applies the operator once. STARS (verified, §2) motivates its entire
training framework on the observation that looped-LM performance
peaks-then-collapses with recurrence depth — a prediction the corpus cites
as a constraint but never tests on its own substrate. A non-monotonic f(k)
would be the first *qualitative* behavior the static program has ever
produced; flat-zero would convert "the static family is dead" from a
single-regime observation into a depth-swept license.

**Cheapest falsifying experiment.** N=60 items × 5 depths × 1 arm = 300
forward passes on pythia-410m/L20, reusing the EXP077 runner and evaluator
(no new code beyond a depth loop; Law #15 Q3: cheapest because the runner,
evaluator tests, and substrate are already signed and smoke-tested).
Free-tier cost: ~10 minutes of one Kaggle T4, $0.

**Kill criterion.** f(k) = 0 for all k ∈ {1,…,5} (McNemar null bar,
pre-registered) → the depth hypothesis is Not supported AND the
regime-untested rescue is falsified — the experiment is designed so its
most likely outcome *strengthens* the existing kill, satisfying the
falsification-first bar. Non-monotonic f(k) with peak > δ_min at the
Level-1 standard → STARS constraint Supported for this family; stabilizer
search licensed.

**Belief it could change.** "Single-application tests exhaust the static
operator" — the standing assumption behind all five dead rooms. A clean
gain-then-collapse on a frozen backbone would additionally be the first
*direct* Δθ=0 test of STARS's motivating observation (which STARS itself
only used to motivate a training framework), giving the result field-facing
weight beyond the program.

**Novelty audit (N1 default):** depth-swept static injection is not in the
corpus (grep: no depth/recurrence sweep of the static operator in
EXP059–077); SVF and A-LQR occupy adjacent slots but neither sweeps
application depth of a static direction. Graded N1 (Known Combination) —
it is a falsification experiment, not a novelty claim, and is proposed as
such.

---

*End of FRONTIER_SCOREBOARD.md v1.0 — LOG-220, 2026-09-23. $0 spent; no GPU;
no signed artifacts touched; all literature checks read-only fetches.*
