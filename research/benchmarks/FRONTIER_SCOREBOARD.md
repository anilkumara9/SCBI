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
| Static steering, decision flips | **ITI**: Alpaca TruthfulQA 32.5%→65.1% (+32.6pp) via label-trained head probes (NeurIPS 2023) | EXP077: **ΔM=0, p=1.0, N=60** (410m/L20) — five static rooms dead; **EXP093: the shared L11 task direction is also ΔM=0, p=1.0 (b=c=0)** — causal inertness, not measurement failure; the L20 boundary generalizes: **information ≠ influence**. G1 killed the QK-subspace mechanism. **S5-2** (LOG-4392): per-arm 95% upper **4.87%** (n=60, 0/60) — effects ≥4.87% dead on every bench; the skeptic's 1–5% "small real effect" band NOT killed at $0 (the 1–4.87% band is the declared blind spot); grand pooled 0.38% (0/780) assumes across-arm exchangeability. **S5-3** (LOG-4393): 0/8 decode probes clear the bar → EXP077 variants never-decodable, not decodable-yet-inert (instrument LIVE on synthetic D1a). **EXP106→EXP107** (LOG-4534/4540): the trained output-side head's **60/60** disjoint-bench transfer reading was **killed as a template artifact** (34/60, p=0.1831 — original-word cells 30/30, flipped-word cells 4/30; GPU head-training proposal void). **EXP110** (LOG-4558): the EXP105 KILL-at-step-9 verdict is **precision-certified under weight-only INT8 fake-quantization** (6/7 tiers, structural intact; T6 O 0.5714→0.5000 as a bounded precision effect) — boundary-science, not capability; the I2′ KILL stands. **EXP111** (H5/LFH-TD, LOG-4568): trained L2-logistic head on the EXP107 **template-decorrelated** bench (H3's re-licensed attempt under the kill-test's own discipline): **24/30 = 0.8000, one-sided p=0.00072** (independent review LOG-4569 QUALIFIED — required footnote: the report's 0.0014 is the two-sided value; one-sided 0.00072, descriptive-only, no branch affected), **G=0.0000** (acc(F)=acc(T)=0.8000, far below the 0.30 kill threshold — no template-detector signature) → **CONTINUE** — the program's first output-side result to survive adversarial testing. The GPU head-training proposal voided by EXP107 is re-licensed under decorrelated-bench discipline (still founder-hardware-gated). **Boundary-science decodability entry, NOT capability** — one layer-20 correlation on one n=30 bench; capability needs downstream causal tests. | **+32.6pp (label-trained probes) vs exactly zero at two layers. The 60/60 trained-readout signal died as a template artifact; the boundary holds under INT8 simulation but nothing steers. One above-chance head signal (EXP111, 24/30 on the decorrelated bench) survived adversarial testing — and EXP120 replicated it on a second independently constructed decorrelated bench (25/30, G=−0.2000; independent review QUALIFIED, verdict stands) — and **EXP122** (H16/POSITION-CUE, LOG-4653) dissected the position cue on a third, independently constructed *position-scrambled* bench (27/30 = 0.9000, G=−0.0667; independent review LOG-4654 — BIND, no caveat) — decodability on three benches, not steering.** |
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

**v1.3 delta [FACT], 2026-09-28:** a new program line opened — **I2′
(selection-failure instrumentation, EXP085's death-debt)**. EXP104's
Tier-0 screen (LOG-4481) HOLDed on bench sanity (0.1833 < 0.25); the
autopsy (LOG-4483) diagnosed a **position-A prior (30/60, p=2.02e-12)** —
a measured instrument confound, not a model finding and not a premise
kill. The licensed recalibration (S4-8′, SIGNED LOG-4488) re-prompts the
same 60 items as cloze completions; EXP105 is running with a binding
breaking point (cloze Tier-0 < 0.25 → LINE-CLOSED). **Capability
scoreboard: unchanged — still zero positive signals for autonomous
steering; the label-free race stays tied at zero.**

**v1.4 delta [FACT], 2026-09-28:** the I2′ line reached its terminal
state — **falsification-terminal, not capability.** EXP105 (cloze
Tier-0, LOG-4489) **PASSED** the sanity bars that EXP104 failed: baseline
**0.5333 (32/60)** inside [0.25, 0.75], median correct-rank on failed
items **4.0 ≤ 5**, n_pop = **21 ≥ 12**, tie-guard **0.0 ≤ 0.25**
— the cloze format rescued measurability (0.1833 → 0.5333), confirming
the LOG-4483 position-A diagnosis: the prior was a readout-format
artifact, not a knowledge absence. The intervention battery (LOG-4491)
then **KILLED the readout-suppression premise at step 9**: ΔM_T = +0.2381
(5/21 rescues) vs ΔM_R = 0.0000 (0/21) — clean direction — but the
primary T-vs-R McNemar-exact **p = 0.0625 ≥ 0.05**, missed by exactly one
flip (b=6 would have certified CONTINUE). Foil overlap O = 0.571 > 0.5
→ F arm non-diagnostic — the S4-8 N1 amendment's O ≤ 0.5 gate (a
pre-registered design decision) anticipated exactly this failure mode and
is recorded as a validated design lesson. Pre-registered stop rules now
close the battery line: no re-run, no larger population, no third
readout. **Capability scoreboard: unchanged — still zero positive
signals for autonomous steering; the label-free race stays tied at
zero.**

**v1.5 delta [FACT], 2026-09-29:** plotted the two S5 boundary-strengthening
verdicts from the 9-28 wave — **S5-2 power audit** (LOG-4392): exact
one-sided 95% upper **4.87%** per arm (n=60, 0/60) over every static-geometry
kill (EXP065/066, EXP077 ×8, EXP093, EXP094's T-vs-B arm; EXP094 aggregate
(0/120) → 2.47%; Bench-A pooled L20 (0/540) → 0.55%; Bench-B pooled L11
(0/180) → 1.65%; grand pooled (0/780) → 0.38% — pooled figures assume
across-arm exchangeability, collapsing to 4.87% under perfect cross-arm
correlation; EXP078 contributes no bound — energy-gate halt, not a
flip-rate kill). The skeptic's 1–5% "small real effect" band is **NOT killed
at $0** — the 1–4.87% per-arm band is the declared blind spot; **the audit
plots an honest bound, not a kill.** **S5-3 decode probes** (LOG-4393):
0/8 EXP077-variant probes clear the EXP092 bar (v_hat acc=0.0667, p=0.3227;
V6 acc=0.1167 rejected by Bonferroni + 10pp bar; V7 acc=0.0000) →
**never-decodable PIVOT** — the eight Gap-4 rooms were empty (informational
wall), not decodable-yet-inert; instrument LIVE on synthetic D1a
(acc=1.0, p=0.001). **Paper marker: v84 is the release candidate**
(LOG-4519, CEO GRANT — supersedes v83; v84 = v83 + converging-evidence
related work + O1/O2 polish, a strict content superset; v83 frozen as prior
RC). EXP095/096/097 (LOG-4400/4407/4416) and the EXP105 battery
(LOG-4491, repaired LOG-4495) were verified in-file this cycle — binding
numbers confirmed, no superseding LOG found; already plotted at v1.2/v1.4,
no re-plot. Daily frontier sweep (LOG-4513): two converging-evidence finds
(arXiv:2609.31401 Ravulapalli/Chadha — probe accuracy rises while
steering benefit stays negligible; arXiv:2609.25366 Jia/Mu, TMLR Sep 2026 —
readable-but-not-reliably-controllable, ~25% flips at best) — tracked for
the next §5 fold-in cycle; **headline confirmed unchanged: zero positive
signals for autonomous steering; the label-free race stays tied at zero.**
No literature re-check this cycle (next due 2026-10-23).

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
| **EXP067** — STAGE_A_HALT (LOG-130) | Adaptive-loop full-rank Procrustes operationalization | pythia-410m (2×T4) | Halt at Stage A guard: rank/spectral violated (head 0: rank=33, gap=1.59e-08; 80 anchors span ~33/64 dims) — H1 untestable under this operationalization; I1 stands unchallenged | 70.79s GPU | N/A (halt) | — | Y | Halted (pre-registered branch a); Δθ=0 confirmed (pre==post) | `experiments/runs/EXP067*`; LOG-130 |
| **EXP078** — BRANCH (a) ENERGY_GATE_HALT (LOG-117) | Oracle-scale static bridge, subspace-restricted | pythia-410m (GPU) | Halt at energy gate — as predicted; oracle-strength static injection has no decision headroom | GPU | Per-item (oracle) | — | Y | Halted (predicted); +16.67pp oracle ceiling remains a ceiling, not a mechanism | LOG-117 |
| **K3 Phase-0** — HALT on FATAL G4 (LOG-238) | CPU audit plan self-guard | CPU | Halted on plan-premise defect D1 — the plan died on its own guard; re-registration commissioned | $0 CPU | N/A | — | Y | Halted; re-registration commissioned, K3 Phase-1 verdict outstanding | LOG-238 |
| **S3-1 / S3-3 Stage-0 archived gates** — INFEASIBLE (LOG-243) | Target-free causal verification on archived records | Archived artifacts (8 + exp077_vectors.pt) | **Killed as an approach:** no per-layer activation/attention snapshots exist in any archive — archived gate infeasible, not merely underpowered; pivoted to Stage-0b live pilots | $0 CPU | N/A | — | Y | Killed (approach); pivots QUEUED | LOG-243; `research/innovation/CANDIDATE_BACKLOG.md` |
| **EXP085** — KILLED as designed (LOG-323) | Runner-up suppression on binary forced-choice bench | (draft only — never executed) | k=2 algebra collapses the design (ΔM_C2 ≡ 2·(N_f/60)−1, Tier-0 Type-I=1.00, kill-bar power 0.00, C3 undefined, C7 ≡ N_f/60) — binary benches make rank-suppression **untestable by construction** | $0 | N/A | — | Y | Killed as designed (CEO decision on binding LOG-317 adjudication); draft retained bannered KILLED per Law #8 | LOG-323; LOG-317 |
| **EXP090** — RUN-INVALID, G1 by construction (LOG-354) | CLM-8B free-lunch falsifier, attempt 2 | CPU (real tokenizer) | RUN-INVALID: 7/10 bench entities multi-token (Jupiter, Mars, Mercury, Saturn, Venus, Bronze, Steel) — the G1 single-token assumption was asserted by two Law #14 reviews without running the real tokenizer; registered bench cannot satisfy G1 under any execution → verdict withheld | $0 CPU | N/A | — | Y | RUN-INVALID (design defect); weights untouched | `experiments/runs/EXP090_clm8b_falsifier_v2/out/exp090_exec_stdout.log`; LOG-354 |
| **EXP091** — KILL: zero-shot cosine scoring dead (LOG-361/362) | Zero-shot cosine-similarity scoring, frozen final-token embeddings, novel relational items | pythia-410m / L20 | **31/60 (51.67%), exact one-sided binomial p=0.4487**; A-first 0.50 / C-first 0.5333; margins noise-scale (mean 6.8e-4); instrument responsive (G4 spread 0.0803 ≫ 1e-4) — genuine null; CLM-8B free-lunch version KILLED as designed (≤37/60 bar) | 60 passes, $0 CPU | None (zero-shot) | N | Y | Killed (executed real, CPU); independent verdict review ADOPTED (LOG-362); Δθ=0 verified | LOG-361/362; `experiments/runs/EXP091*` |
| **EXP092** — CONTINUE: layer-11 task information licensed (LOG-4336/4338) | Information-Bottleneck Localization — per-layer 1-NN LOO on frozen embeddings | pythia-410m, all 24 layers | Layer 11: **acc 0.3333 (20/60), stratified-permutation p=0.000999 < α_B=0.0020833, effect +0.2000 ≥ 0.10**; S = {1,11,12,13,14,15,17,18} clear both bars; L20 acc 0.15, p=0.0659 (correctly excluded). ADOPT-WITH-CORRECTIONS (binding). **Licensed claim: frozen layer 11 carries significant task information (1-NN LOO, Bonferroni-significant, ≥10pp above null).** Novelty N1. No capability claim licensed. | $0 CPU (~1.5h) | None | N | Y | Continue, l* = 11; S1 (Ross kNN-MI) retired — proven vacuous by construction (MI = ψ(60)−ψ(4) exactly in this regime; any successor MI diagnostic needs a degeneracy analysis + constant-data unit test) | LOG-4336 (execution), LOG-4338 (binding review), `experiments/runs/EXP092_ibl/` |
| **EXP093** — KILL UPHELD: shared layer-11 direction causally inert (LOG-4352) | Static injection of the shared layer-11 task direction on EXP092-B | pythia-410m / L11 | **Δ = 0.0000; McNemar b = c = 0 → p = 1.0 in all six tests** (P-vs-B and N-vs-B × 3 strata); perturbation real (4.7% of residual norm, reached the logits, G5 rel_err 4.3e-07) but flipped zero decisions — causal inertness, not measurement failure. **Information ≠ influence at layer 11; the layer-20 boundary generalizes.** Falsifies "≥10pp causal transfer via a shared static direction at layer 11" only. | $0 CPU (~10–15 min) | None | N | Y | Killed (executed real, CPU); independent verdict review binding (LOG-4352); Δθ=0 verified (pre/post `ec276abe…`) | LOG-4352; `experiments/protocols/REVIEWS/EXP093_LAW14_VERDICT_REVIEW_2026-09-25.md` |
| **EXP094** — KILL: per-item static L11 geometry refuted by inertness (LOG-4376/4377) | Per-item static L11 injection (per-item direction, not shared) | pythia-410m / L11 | **0 flips across 120 injection arms** (B=T=R=36/60, p=1.0) despite confirmed delivery; per-item static-geometry family closed at L11 | $0 CPU | None | N | Y | Refuted (executed real, CPU); independent verdict review ADOPTED (LOG-4377) | LOG-4376/4377; `experiments/runs/EXP094*` |
| **S5-2** — power audit: honest bounds on the static-geometry kills (LOG-4392) | Flip-rate upper bounds over committed static-geometry kill statistics | pythia-410m / L20 (EXP065, EXP066, EXP077 ×8 variants) + L11 (EXP093, EXP094); EXP078 contributes NO bound (ENERGY_GATE_HALT, localization not a flip-rate kill — LOG-117) | Exact one-sided 95% upper = 1−0.05^{1/n}. Per-arm **(0/60): 4.87% exact / 5.00% Ro3 / 5.96% CP-2sided** — applies to EXP065, EXP066, each EXP077 variant, EXP093, EXP094's T-vs-B arm. EXP094 aggregate (0/120): **2.47%**. Bench-A pooled L20 (0/540): **0.55%**; Bench-B pooled L11 (0/180): **1.65%**; grand pooled (0/780): **0.38%**. **Pooling caveat [FACT]:** arms share the same 60 items — pooled figures assume across-arm exchangeability; under perfect cross-arm correlation the pool collapses to the per-arm 4.87% (honest: Bench-A ∈ [0.55%, 4.87%], Bench-B ∈ [1.65%, 4.87%]) | 0 new passes ($0 arithmetic over committed statistics) | N/A | — | Y | **Supported (audit)** — CONFIRM + QUANTIFY: PIVOT does not fire (no bound outruns its license); the skeptic's 1–5% "small real effect" band is **NOT killed at $0** — the 1–4.87% per-arm band remains the declared blind spot. What $0 buys: effects ≥4.87% dead per arm on every bench; ≥2.47% dead on the EXP094 aggregate; ≥1.65% pooled at L11; ≥0.55% as an across-arm average at L20 (exchangeability assumed). N≈100+ replication priced (independently reproduced from committed statistics). **The audit plots an honest bound, not a kill** | LOG-4392; `research/analysis_plans/S5-2_POWER_AUDIT_2026-09-28.md` |
| **S5-3** — paired decode probes: never-decodable PIVOT (LOG-4393) | EXP092's licensed decode protocol on the eight killed EXP077 variants' directions (Gap 4: decodable-yet-inert vs never-decodable) | pythia-410m / L20 (archived EXP077 directions; index 20 = EXP077 target layer) | **0/8 clear the bar** (Bonferroni p < 0.05/8 + (acc − q95) ≥ 0.10): v_hat probes (V1–V5, V8) acc=0.0667, p=0.3227, effect=−0.033; V6 (r_vec) acc=0.1167, p=0.0499 — rejected by BOTH bars; V7 (v_hat^c) acc=0.0000, p=1.0. **Instrument LIVE:** D1a synthetic-1-D machinery check acc=1.0, p=0.001, effect=+0.85 (variant nulls are real nulls, not deafness); D1b: 1-D entity information at L20 is weak along any real direction tried (label-informed: acc=0.05, p=0.75) | $0 CPU, 0 new model passes (≤480 CPU probes on archived artifacts); deterministic re-run byte-identical | None | N | Y | **PIVOT (never-decodable)** — the Gap-4 rooms were empty (informational wall), not decodable-yet-inert. 8 arms = 3 distinct directions (v_hat; r_vec cos=0.019 to v_hat; v_hat^c). Consistent with EXP077's branch-(c) NEITHER GPU verdict. Caveat: decode target is target-entity identifiability (EXP092's licensed operationalization), not EXP077's relational-vs-neutral construct | LOG-4393; `research/analysis_plans/S5_3_REPORT_2026-09-28.md`, `research/analysis_plans/s5_3_decode_probes_2026-09-28.py` |
| **EXP095** — KILL: α-grid inert (LOG-4400) | α grid sweep on per-item L11 injection | pythia-410m / L11 | α ∈ {0.25,0.5,1,2,4} → task flips {0,0,0,1,1} — inert below bar at every ratio | $0 CPU | None | N | Y | Refuted | LOG-4400 |
| **EXP096** — KILL: headroom-gated movement fragility (LOG-4407) | Headroom-gated per-item L11 injection | pythia-410m / L11 | Headroom-gated T and B_wrong each moved 3 — movement exists but is not attributable to the task direction | $0 CPU | None | N | Y | Refuted | LOG-4407 |
| **EXP097** — PIVOT: fragility (LOG-4416) | Fragility probe of per-item L11 movement | pythia-410m / L11 | Movement not directionally attributable | $0 CPU | None | N | Y | PIVOT (fragility) | LOG-4416 |
| **EXP098** — PIVOT: composition premise not supported (LOG-4423) | Layer-composition injection (L11, L20, joint, random-joint) | pythia-410m / L11, L20 | L11: 3 flips; L20: 6 flips (all right→wrong); joint: 7 flips; **random joint: 12 flips** — no interaction candidates; composition premise unsupported | $0 CPU | None | N | Y | PIVOT (premise) | LOG-4423 |
| **EXP099** — PIVOT: fragility — directional claim not supported (LOG-4434) | Directional fragility probe | pythia-410m / L8 | L8 moved 4; **W20 random moved 7** — directional claim not supported | $0 CPU | None | N | Y | PIVOT (fragility) | LOG-4434 |
| **EXP100** — PIVOT (untestable): S6-3 mean-gate collapse (LOG-4441) | Mean-over-heads L11 attention-gated injection of the killed per-item L11 direction @ 0.38 | pythia-410m / L11 (gate read at L11) | Coverage **0/60** — mass_i ∈ [0.0396, 0.0746] vs τ_i ∈ [0.2286, 0.2759]; gate never close to firing on any item; 0 injection passes; step-2b coverage tripwire (<10%) fired | 127 CPU passes, $0 | None | — (null; untestable) | Y | **PIVOT (untestable)** — step-2b tripwire; not a KILL of dynamic gating (forbidden from a collapsed gate); not a fragility finding | LOG-4441; `experiments/runs/EXP100_gated_L11/` |
| **EXP101** — KILL: S6-3b max-gate refuted (LOG-4448) | Max-over-heads L11 attention-gated injection of the killed per-item L11 direction @ 0.38 | pythia-410m / L11 (gate read at L11) | Coverage **16/60 = 26.67%** (gate testable). gated-T vs B: **1 flip (b=0, c=1, p=1.0)** — sole flip right→wrong on `exp092_elemental_2hop_0`. gated-R vs B: 0 flips. ΔM (paired logit-margin): gated-T −0.0236, gated-R −0.0171 (flat, \|ΔM\|<0.10). Evidential weight (16 fired): 0 directional-positive flips → one-sided 95% UB **17.1%** on gated-conditional directional flip rate | 159 CPU passes, $0 | None | N | Y | **Refuted** — step-6 Gated KILL; fenced to max-gated per-item L11 injection @0.38 on EXP092-B | LOG-4448; `experiments/runs/EXP101_gated_L11_max/` |
| **EXP102** — PIVOT (untestable): S6-3c L20-mean-gate collapse (LOG-4455) | Mean-over-heads **L20** attention-gated injection of the killed per-item L11 direction @ 0.38 | pythia-410m / L11 (gate read at L20) | Coverage **1/60 = 1.67%** — single fired item `exp092_elemental_3hop_0` (mass 0.23303 ≥ τ 0.22857); mass range [0.0346, 0.2330] vs τ [0.2286, 0.2759]; gated-T vs B 0 flips; gated-R vs B 0 flips; ΔM 0.0 all contrasts; step-2b tripwire fired. F1 decision-proxy audit (descriptive only): B accuracy 1/1 fired vs 35/59 unfired | 129 CPU passes, $0 | None | — (null; untestable) | Y | **PIVOT (untestable)** — step-2b tripwire; not a KILL | LOG-4455; `experiments/runs/EXP102_L20gated_L11/` |
| **EXP103** — KILL: S6-3d L20-max-gate refuted; gate family closed 4/4 (LOG-4462) | Max-over-heads **L20** attention-gated injection of the killed per-item L11 direction @ 0.38 | pythia-410m / L11 (gate read at L20) | Coverage **55/60 = 91.67%** (gate testable). gated-T vs B: **3 flips (b=1, c=2, p=1.0)** — 1 wrong→right, 2 right→wrong. gated-R vs B: 1 flip (b=1, c=0, p=1.0). gated-T vs gated-R: b=1, c=3, p=0.625. ΔM: gated-T −0.012874, gated-R −0.029963 (flat). Evidential weight (55 fired): 1 directional-positive flip → one-sided 95% UB **5.3%**. F1 audit: B accuracy 34/55 fired vs 2/5 unfired (gate not a near-decision proxy; descriptive) | 237 CPU passes, $0 | None | N | Y | **Refuted** — step-6 Gated KILL; the {mean,max}×{L11,L20} externally-computed attention-gate family is CLOSED 4/4 (mean-L11 untestable, max-L11 Refuted, mean-L20 untestable, max-L20 Refuted). LOG-4460 terminality claim engages: no fifth tweak of this family, ever, under this license | LOG-4462; `experiments/runs/EXP103_L20maxgated_L11/` |
| **S6-5 pooled audit** — directional flip ceiling (LOG-4409) | Pooled task-direction decision flips across the static S6 program | pythia-410m / L11 | **5/381** task-direction decision flips → one-sided 95% upper bound **2.74%** on the pooled directional flip rate | $0 CPU | None | — | Y | Supported (audit; boundary quantification) | LOG-4409 |
| **S6 L11-rescue program — STAND-DOWN (LOG-4463/4464)** | Innovation-design lane: four self-computed-gate candidates constructed and falsified on paper (P prompt-instructed self-gate, E output-uncertainty gate, C activation-magnitude read, B probe-based gate) | CPU design only | No design clears the worth-it gate: P fails principled-threshold/license/interpretability (base-model noise, illusory "self," bench re-baselining); E fails threshold/license (threshold is a guess); C fails the terminality claim directly (fifth externally-computed gate); B fails interpretability (label-informed by construction, LOG-197 precedent). **Rational update: the direction is the problem, not the gate.** Ten experiments, ~2,000 CPU passes. Pre-registered re-opening conditions: (i) a license-bearing observation for a specific self-computed gate enters the record; (ii) a new direction family earns its license; (iii) founder orders otherwise | $0 CPU | N/A (design) | — | Y | **STAND-DOWN** (CEO ruling LOG-4464) — no further injection of the killed per-item L11 direction on CPU lanes; GPU queue untouched | LOG-4463/4464; `research/innovation/S6_STANDDOWN_RECOMMENDATION_2026-09-28.md` |
| **EXP104** — HOLD → Inconclusive: Tier-0 bench sanity failure (LOG-4481/4482) | Tier-0 correct-rank screen for the I2′ line (are selection failures measurable/repairable — EXP085's death-debt question) | pythia-410m / next-token position after terminal `Answer:` | Baseline accuracy **11/60 = 0.1833** < 0.25 sanity band; failed 49; median correct-rank (failed) = **4** (bar ≤ 5 met); n_pop (failed ∧ rank ≤ 5) = **33** (bar ≥ 12 met); tie-guard 0/33 = 0.0. G1 tokenizer gate 0/480 clean; checker 64/66 (1 item replaced, 1 dropped → 59 VERIFIED + 1 backup). §3 binding step-4: HOLD (bench sanity) → **Inconclusive**. The premise/power bars were satisfied — the failure is bench calibration, not the selection-failure premise. Battery NOT licensed, NOT run | 60/60 passes, 58.7 s CPU fp32, $0 | None | N (null) | Y (Δθ=0 verified, pre/post weight sha256 identical) | **HOLD→Inconclusive** (executed real, CPU, signed S4-8 pre-reg v3 LOG-4480, CEO clearance LOG-4482) — premise NOT killed | LOG-4481/4482; `experiments/runs/EXP104_Tier0_rank_screen/` |
| **Position-A prior** — measured MC-instrument confound (LOG-4483) | Autopsy of EXP104's HOLD (analyst lane, committed artifacts only, no new passes) | pythia-410m (EXP104 bundle records) | Top-1 at position 0 on **30/60 items**, P ≥ 30 under no bias = **2.02e-12**; uniform across all 10 templates (2–4 pos0-picks per 6-item block) → format-driven (`A)…H)` enumeration + terminal `Answer:`), not content-driven. Of the 11 correct, 4 at position 0 ≈ 3.0 expected under a pure prior — the A-picks carry no knowledge. Non-A-prior items: **7/30 = 0.233** (< 0.25 sanity, above 0.125 chance). Shuffle seed over-represented correct positions 3 and 5 → the realized baseline is shuffle-seed-sensitive: this MC bench, in this format, is not a knowledge instrument. Recorded as a bench confound, NOT a model finding. EXP092 reconciliation: supervised 1-NN at L11 (33.33% vs 5%, p=0.000999) measures information *presence*; EXP104 measures *routability* of the untuned base head — no contradiction | 0 new passes ($0 analyst recompute) | N/A (diagnostic) | — | Y | Supported (diagnostic; deterministic recompute from bundle, deliverable with sha256 lineage) | LOG-4483; `research/analysis_plans/EXP104_BENCH_AUTOPSY_2026-09-28.md` |
| **S4-8 / S4-8′ — pre-registration milestones (LOG-4480, LOG-4488)** | Signed Tier-0 protocols for the I2′ line: S4-8 (MC correct-rank screen, v3, chain LOG-4475→4480) and S4-8′ (cloze recalibration, v2, chain LOG-4484→4488) | Paper only | S4-8: seven §5 degeneracy unit tests + foil–top-1 overlap stratum (O ≤ 0.5 gate on the step-8 F diagnostic) + G1 tokenizer gate + foil-build blindness. S4-8′: re-prompts the same 60 items as cloze completions (`<question> The answer is`, cue pinned/frozen), drops the correct-position shuffle, scores the same 8 G1-verified candidate tokens with ascending-token-id tie-break; **new binding breaking point: cloze Tier-0 baseline < 0.25 → LINE-CLOSED** (I2′ untestable on Pythia-410m at $0, no third readout); predicted band 0.25–0.45 [HYPOTHESIS] | $0 CPU | N/A (protocols) | — | Y | **SIGNED** (both, Law #14 full chains; S4-8′ fixes incl. one-word remainder LOG-4488) — EXP105 (cloze Tier-0) is the first execution under S4-8′, executed as EXP105 (below) — outcome now plotted | LOG-4480 (S4-8); LOG-4484–4488 (S4-8′); `research/innovation/S4-8_PREREG_DRAFT_v3_2026-09-28.md`, `S4-8_PRIME_PREREG_DRAFT_2026-09-28.md` |
| **EXP105 Tier-0** — PASSED: cloze measurability rescued (LOG-4489) | Tier-0 correct-rank screen on the cloze recalibration (S4-8′ first execution) | pythia-410m / next-token position after pinned completion cue | Baseline accuracy **32/60 = 0.5333** inside [0.25, 0.75] — NOT line-closed; median correct-rank (failed) = **4.0** ≤ 5; n_pop (failed ∧ rank ≤ 5) = **21** ≥ 12; tie-guard 0/21 = **0.0** ≤ 0.25; alt-cue descriptive baseline (`Answer:`) 0.5 (not a gate). G1 tokenizer gate 0/480; Δθ=0 (pre/post weight sha256 identical). Run survived a VM restart at 13 records — `verify_resume.py` confirmed a bit-exact 8-logit match before resuming 47 more | 60/60 passes, $0 CPU, torch 2.14.0+cpu / transformers 5.17.0 in a rebuilt venv | None | N (null-positive: passed sanity, no steering claim) | Y | **PASSED** (Tier-0 only; licensed the battery — NOT a capability result) | LOG-4489; `experiments/runs/EXP105_cloze_Tier0/` |
| **EXP105 battery** — KILL (nonspecific), step 9 → **Refuted** (LOG-4491) | Intervention battery on the Tier-0 population: logit-level truth/falsity/random masking operators (B/T/F/R arms) | pythia-410m / recorded Tier-0 8-candidate logits (zero model contact) | Tier-0 population n_pop = 21. ΔM_T = **+0.2381** (5/21 rescues); ΔM_F = +0.1429 (3/21); ΔM_R = **0.0000** (0/21 — perfectly flat). Primary binding contrast T-vs-R McNemar-exact: b=5, c=0 → **p = 0.0625 ≥ 0.05** — missed CONTINUE by exactly one flip (b=6, c=0 → p=0.03125 would have certified). Tango 95% CIs: T-vs-R (0.047, 0.451); F-vs-B (−0.034, 0.346); R-vs-B (−0.155, 0.155). Foil–top-1 overlap **O = 12/21 = 0.571 > 0.5** → F arm non-diagnostic (pre-registered stratum; the N1 amendment's gate anticipated this). Decision walk: step-7 CONTINUE fails on the primary p-value; step-8 fails (F-vs-B p=0.25, O > 0.5); **step 9 fires → Refuted**. Pre-registered stop rules close the line: no re-run, no larger population, no third readout | 0 model passes (logit-level operators), $0 CPU, R seed pinned 20260928; one implementation bug caught and fixed mid-lane (degenerate Tango CI transcription — rewrote as bounded MLE, verified on symmetric/null/grid cases; worksheet numbers from the fixed implementation) | None | N | Y (Δθ=0 by construction) | **Refuted** — readout-suppression premise KILLED as a certified-specific mechanism; the rescue direction was clean but specificity was not certified. Not evidence masking is generic — evidence the licensed test could not certify specificity | LOG-4491; `experiments/runs/EXP105_battery/` (report, worksheet, per-item CSV/JSON, executor) |
| **EXP106 → EXP107** — **KILL**: the label-free head's 60/60 transfer reading was a template artifact (H3 arc) | Trained output-side head transfer: L2-logistic head (C=1.0) on frozen L20 final-token embeddings, fit on one 60-item bench, scored on a disjoint 60-item bench (item-ID overlap 0); then a template-decorrelated control (word-family × phrasing, 4×15 balanced cells, deterministic rewriting) | pythia-410m / L20 (frozen; block-off byte-identity check passed) | EXP106: **60/60**, one-sided binomial **p=8.67e-19** → registered CONTINUE (the program's first above-chance trained-readout signal). EXP107: **34/60 = 0.5667, one-sided p=0.1831** ≤ 35/60 KILL bar → **KILL**. Per-cell: 15/15, 4/15, 15/15, 0/15 — original-word cells 30/30, flipped-word cells 4/30 (the registered template-detector signature); 31/31 training-prior-vs-template disagreements followed the template | CPU; sklearn head on extracted embeddings; $0 | Train-probes (head fit on disjoint-bench labels, applied to held-out items) | Y (the transfer claim itself) → N on control | Y | **Killed (transfer reading)** — GPU head-training proposal licensed by the CONTINUE is void; no re-run, no larger-N rescue; kill holds whether the cue is word-template or subject-position | LOG-4534/4540; `research/experiments/EXP107_TEMPLATECTRL_REPORT_2026-09-29.md`; independent verdict review LOG-4559 (BIND) |
| **EXP108** — **RUN-INVALID**: honesty-instrument elicitation failure (H1) | Self-report honesty probe: 60 self-report generations; strip → first alphabetic char → {A, C}, else UNPARSEABLE; registered gate n_unparseable ≥ 7 → RUN-INVALID | pythia-410m base (greedy generation), CPU | **n_unparseable = 60/60 ≥ 7 → RUN-INVALID (elicitation failure)**. All 60 emitted the identical token sequence `[187, 187, 23433, 27]` = "\n\nQuestion:" — document-pattern continuation, not answers. No fidelity score, no balanced accuracy exist. H1 is neither KILLED nor CONTINUED | 60 generations, CPU, $0 | N/A (apparatus) | — | Y | **RUN-INVALID (apparatus)** — required footnote (review LOG-4559 QUALIFY): no per-item generation records retained; evidence is a single console-log summary line; future runs of this class must retain per-item logs | LOG-4546; `research/experiments/EXP108_HDI_REPORT_2026-09-29.md` |
| **EXP109** — **RUN-INVALID**: planner/executor elicitation failure, 20-item pilot (H4) | Planner emits 4 outlines; frozen executor develops each; majority vote; vs 4 independent samples at identical generation budget. Planet-only pilot (15 planet-2hop + 5 planet-3hop; no elemental items) | pythia-410m base (greedy generation), CPU | Planner arm: **18/20 items zero numbered outlines** (repetition attractor: "Plan: Write a list of the possible answers to the question"); 2 items mechanical enumerations, executor 0/4 parseable. Baseline: **80/80 unparseable**. **n_valid = 0/20** — elicitation-failure gate fires (20 ≥ 3); global degeneracy tripwire fires (88/88). No accuracy, no (b,c) table, no McNemar p exists | 108 generations, 20.9 CPU-min, $0 | N/A (apparatus) | — | Y | **RUN-INVALID (apparatus)** — planner/executor axis NOT retired; pilot-scope fenced (a KILL would require net ≤ 0 on valid paired items — never reached) | LOG-4552; `research/experiments/EXP109_PTTSC_REPORT_2026-09-29.md` |
| **EXP110** — **CERTIFIED-WITH-NOTE**: the EXP105 KILL-at-step-9 verdict is precision-certified under weight-only INT8 fake-quantization (H2) | Re-run the cleared EXP105 falsification-kit battery on a fake-quantized frozen backbone (per-output-channel symmetric INT8 on all 97 Linear weight matrices, FP32 compute; zero generation by design) | pythia-410m, CPU; torch 2.14.0+cpu / transformers 5.17.0, threads 2, seed 20260928; backbone verified against the LOG-331 pin before quant (disposable copy, discarded after run) | **6/7 tiers reproduce** — T1 Tier-0 PASSED @ 0.5333 = ref; T2 KILL = KILL; T3 step 9 = 9; T4 dM_T=+0.2000>0, dM_F=+0.1500>0, \|dM_R\|<0.05 (ref +0.2381/+0.1429/flat); T5 T-vs-R b=4,c=0,p=0.1250 ≥ 0.05 (ref b=5,c=0,p=0.0625); **T6 flipped: O=0.5000 (not > 0.5) vs ref 0.5714** — n_pop 21→20 at the rank-5 margin; T7 n_pop=20 within ±5 of 21. Structural tiers T1–T3 intact → CERTIFIED-WITH-NOTE (pre-reg §4 branch); PIVOT correctly not triggered | Quantized Tier-0 (60 forward passes) + battery, ~2–4h CPU, $0; sanity gate `reproduce_exp105.sh` = EXACT ✔ before quant | None | — (boundary certification) | Y | **Certified (boundary-science)** — simulation-scoped (NOT true INT8 hardware; bitsandbytes-exact is the GPU-gated ceiling); the I2′ KILL stands regardless; no closed line re-opens; **no capability claim licensed** | LOG-4558; `research/experiments/EXP110_QBR_REPORT_2026-09-29.md`; independent verdict review LOG-4559 (BIND) |
| **EXP111** — **CONTINUE**: trained head on the template-decorrelated bench survives the kill-test that killed EXP106 (H5/LFH-TD) | L2-logistic head (C=1.0, lbfgs) on frozen L20 final-token embeddings of the EXP107 template-decorrelated bench; stratified 30/30 train/test split (seed 20260929, key `{phrasing}_{flipped}`, train/test ID overlap 0); registered CONTINUE ⇔ ≥20/30 AND G < 0.30 | pythia-410m / L20 (frozen; block-off byte-identity; embeddings extracted from archived EXP107 artifact — three artifact hashes verified pre-training; no backbone loaded for primary analysis); skull-layer secondary L4/L8/L12/L16 descriptive-only | **Test 24/30 = 0.8000** (per-cell 7/8, 6/7, 5/7, 6/8; acc(F)=acc(T)=0.8000), **G = 0.0000 < 0.30** → CONTINUE (the only firing branch; kill branch G ≥ 0.30 correctly not triggered). Train acc 1.0000, no tuning; determinism re-fit byte-identical; head hash 483a91a8…afdf9f28. **One-sided binomial p = 0.00072** (report's 0.0014 is the two-sided value — required footnote, descriptive-only, no branch affected). Secondary (descriptive): L4 24/30 G=−0.1333; L8 30/30 G=0.0000; L12 29/30 G=0.0667; L16 30/30 G=0.0000 — position signal decodable across layers, no signature at any layer. LOG-331 pin verified pre AND post (Δθ=0) | sklearn CPU fit, $0 | Train-probes (head fit on disjoint-bench labels, held-out items) | Y (the head's read of the decorrelated bench) | Y | **CONTINUE (bound)** — first output-side result to survive adversarial testing; the GPU head-training proposal voided by EXP107 is **re-licensed under decorrelated-bench discipline** (founder-hardware-gated); **NOT a capability result** — one layer-20 correlation on one n=30 bench; novelty N1; fences: no generality, no consciousness, no capability until downstream causal tests; no re-licensing of H1/H4/static/closed lines | LOG-4568; `research/experiments/EXP111_LFHTD_REPORT_2026-09-29.md`; independent verdict review LOG-4569 (QUALIFIED — p-value footnote) |
| **EXP112** — **HELD**: honesty instrument in logit-readout form, zero generation (H6/HDI-LR) | First-token entity-name-logit self-report (argmax over two pinned token logits, single-token BPE 120/120, byte-exact QUESTION_SUFFIX — no new wording) vs registered cosine-argmax decision statistic, on the EXP107 template-decorrelated bench; zero generation — H1 explicitly NOT revived (new hypothesis under a new apparatus) | pythia-410m (frozen; 180 fresh single-token forwards; LOG-331 pin matched before AND after, Δθ=0); archived premise embeddings reused (three artifact hashes verified before use) | **Fidelity 41/60 = 0.6833** (P(X≥41\|60,0.5)=0.0031 — real above chance, below the decisive bar) → registered 34–41/60 band → **HELD**. Law #14-grade degeneracy guards ran **before** any metric read: G1 mean mass 0.301075 ≥ 0.01 (min 0.0685), G2 readout balance 27/33 — channel genuine, non-degenerate; a dead channel could not masquerade as a measurement. Descriptive per-cell: flipped-word cells 24/30 vs original-word cells 17/30 — registered [OBSERVATION], changes no verdict | 180 forwards, CPU, $0 | None (no training, no labels; template-free by construction) | — (instrument) | Y | **HELD (bound)** — weak honesty-decoding correlation at one read site; **licenses nothing, retires nothing, no re-runs** (Law #4); not consciousness, generality, or capability; novelty N1 | LOG-4575; `research/experiments/EXP112_HDILR_REPORT_2026-09-29.md`; independent verdict review LOG-4576 (BIND — no caveat) |
| **EXP113** — **CONTINUE**: elicitation validation — at least one pinned protocol clears ≥80% mechanically-parseable structured outputs on both task shapes (H7/EVALID) | Instruction-following apparatus validation: T1 single-token answer (H1 self-report shape), T2 numbered outlines (H4 planner shape); 5 pinned protocols (P1 verbatim baselines, P2 few-shot, P3 explicit stop, P4 repetition penalty, P5 priming) | pythia-410m base (frozen), CPU, greedy decoding | **T1:** P1=0/60 (EXP108 echo path reproduced), P2=60/60, P3=0/60, P4=58/60, P5=60/60. **T2:** P1=24/60, P2=60/60, P3=0/60, P4=0/60 (penalty derails outlines), P5=60/60. Clearance bar ≥48/60 → T1-CLEAR={P2,P4,P5}, T2-CLEAR={P2,P5}, both non-empty → CONTINUE. Few-shot (P2) and priming (P5) are the only protocols clearing both shapes | 600 generations, CPU, $0 (first launch died at 180/600 on a VM reboot — no metric read; full re-run from scratch; crash log preserved; deterministic re-parse byte-identical; 0 exceptions; 2 empties scored UNPARSEABLE; no RUN-INVALID fired) | None (parseability metric; exemplars carry labels but the metric is parseability) | — (apparatus validation) | Y (LOG-331 pin before AND after, Δθ=0) | **CONTINUE (bound)** — licenses H1/H4 revival as NEW hypotheses with the named clearing protocols (each carrying its own elicitation-failure gate); does NOT revive H1/H4 themselves. **Methodological/apparatus entry, NOT capability**: parseable output ≠ reasoning, honesty, or capability; backbone-specific (base Pythia-410m, CPU, greedy); novelty N1 | LOG-4584; `research/experiments/EXP113_EVALID_REPORT_2026-09-29.md`; independent verdict review LOG-4585 (BIND — no caveat) |
| **EXP114** — **KILL**: positional-order ensembling (H8/POE) — K=5 ensemble of frozen-backbone position logits over randomized presentation orders | Test-time ensembling over positional orderings of the EXP107 template-decorrelated 2-hop cloze bench; paired head-to-head against the canonical single-order baseline; 360/360 forward passes, zero generation | pythia-410m base (frozen), CPU, float32, logit readout at the pinned site | **acc_ensemble 38/60 = 0.6333 vs acc_baseline 41/60 = 0.6833; net (b−c) = −3 (b=2, c=5, n=7); one-sided exact McNemar p = 0.9375** — the ensemble scored 5pp BELOW the baseline. Registered bars: CONTINUE required p ≤ 0.05 with b > c — not met; HELD required net > 0 — not met; **net ≤ 0 → KILL** | 360 forward passes (300 ensemble K=5 order bits + 60 baseline), CPU, $0; order patterns independently replicated from random.Random(20260929), 0/60 mismatches | None (logit readout; no training, no labels touch the apparatus) | — (ensembling method, not transfer) | Y (LOG-331 pin before AND after all 360 forwards, Δθ=0) | **KILL (bound)** — retires only the positional-order-ensembling axis for this task class; test-time scaling in general and the adaptive-loop program are explicitly NOT retired. Below-baseline reading a labeled [OBSERVATION]; no post-hoc softening; novelty N1 | LOG-4591; `research/experiments/EXP114_POE_REPORT_2026-09-29.md`; independent verdict review LOG-4592 (BIND — no caveat) |
| **EXP115** — **RUN-INVALID**: honesty instrument with generation-based self-reports, few-shot (P2) elicited (H9/HDI-GEN) | Few-shot self-report generations on the EXP107 template-decorrelated bench; registered gate n_unparseable ≥ 7 (of 60) → RUN-INVALID; fidelity vs archived EXP112 per-item decisions | pythia-410m base (frozen; 60 greedy generations; LOG-331 pin matched before AND after, Δθ=0); archived EXP112 per-item decisions reused (sha256 `f8133f1f…1a804625` independently re-verified by the execution lane); record/bench alignment 60/60; archived G4 re-check 0.085052 ≥ 1e-4 | **n_unparseable = 38/60 ≥ 7 → G1 FIRED** — failure mode: few-shot recitation (model regurgitates the last exemplar block; all 60 generations contain `Premise:` — e.g. ` Jupiter\n\nPremise: Jupiter is` verbatim from exemplar 2). G2 passed (moot). Fidelity **null** — no decision-bar number exists (gate evaluated before any metric, in code). Deterministic re-parse ×2 byte-identical; per-item generation records retained (the EXP108 lesson) | 60 generations, CPU, $0 | N/A (apparatus) | — (instrument never tested) | Y | **RUN-INVALID (apparatus, bound)** — the hypothesis was never tested; H6's logit-level HELD stands; P5 reserved for a separate pre-registration (the pre-reg's registered consequence); no verdict smuggled | LOG-4598; `research/experiments/EXP115_HDIGEN_REPORT_2026-09-29.md`; independent verdict review LOG-4599 (BIND — no caveat) |
| **EXP116** — **RUN-INVALID**: honesty instrument with priming-protocol (P5) generation-based self-reports (H10/HDI-PRIM) | Priming-protocol self-report generations on the EXP107 template-decorrelated bench; single-block mid-sentence priming template (zero exemplar blocks — the EXP115 recitation pathology structurally blocked); registered G1/G2 gates before metrics; fidelity vs archived EXP112 decisions | pythia-410m base (frozen; 60 greedy generations, max_new_tokens=8; LOG-331 pin before AND after, Δθ=0); archived EXP112 decisions sha256 independently re-verified; bench pin `e91b302f…4f5` | **n_unparseable = 37/60 ≥ 7 → G1 FIRED** — new, *distinct* failure mode: tail echo (27 of the 37 unparseable echo the unfinished priming sentence `"\n\nThe entity higher in rank is"` verbatim; **0/60 generations contain `Premise:`** — recitation confirmed absent). G2 passed (moot). Fidelity **null** — not wrong, *absent*, exactly as the pre-reg requires. Prompts byte-exact: end mid-sentence with `is:`, exactly one `Premise:`, zero exemplar blocks. Shape-change risk disclosed in the pre-reg (§3.3, §8) — P5's 60/60 clearance was on the single-letter shape; this RUN-INVALID is the disclosed risk materializing | 60 generations, CPU, $0 | N/A (apparatus) | — (instrument never tested) | Y | **RUN-INVALID (apparatus, bound)** — two DIFFERENT apparatus failures on the same bench (recitation vs tail echo); **the generation-level honesty instrument has no EXP113-cleared protocol left on the entity-name shape** — P2 dead (EXP115), P5 dead (EXP116); the hypothesis was never tested. H6's logit-level HELD (41/60) stands alone as the only honesty signal. Reviewer note (non-binding): P4 (repetition penalty) cleared T1-only and was never in the named protocol set — future-proposal material, not a defect | LOG-4602; `research/experiments/EXP116_HDIPRIM_REPORT_2026-09-29.md`; independent verdict review LOG-4603 (BIND — no caveat) |
| **EXP117** — **RUN-INVALID**: planner/executor pipeline with P2-primed decision slot, Phase-0 gated (H11/PTTSC-GEN) | Plan-conditioned planner/executor pipeline vs baseline on the EXP089 bench; Phase-0a recitation gate + Phase-0b decision-channel mini-gate fire before the full run | pythia-410m base (frozen; 20 Phase-0 generations, greedy; LOG-331 pin matched pre-run, Δθ=0); planner prompts byte-verified **0/60 mismatches** against the signed `exp113_run.py` T2-P2 construction (EXP113's raw JSON stores no prompts — disclosed honestly); 20/20 generations, 0 exceptions | **Phase 0b: 0/10 parseable < 8/10 → FIRED** — failure mode: entity-name enumeration (model lists entities, e.g. `'\n\n1. Jupiter\n\n2. Mars\n\n3. Venus\n'`, instead of naming one). Phase 0a literal §3.7 gate 0/10 (≥6 → did NOT fire). Full run NOT licensed; McNemar never reached. **4th consecutive entity-name-generation-slot failure** on this shape (EXP109 80/80 sampled; EXP115 38/60 recitation; EXP116 37/60 tail echo; EXP117 0/10 enumeration). **Protocol-defect discovery:** §3.7's literal recitation definition is structurally inert for *content* recitation (marker-stripped extraction vs marker-prefixed exemplar lines — content diagnostic 10/10 ≥2 recitations while the literal gate scored 0/10) — adjudicated **REAL but non-decisive** (gate applied as written; 0b fired independently; RUN-INVALID overdetermined). Binding lesson: **no future protocol may reuse the §3.7 definition** | 20 generations, CPU, $0 | N/A (apparatus) | — (planning question never tested) | Y | **RUN-INVALID (apparatus, bound)** — no verdict smuggled; H4 stays RUN-INVALID-from-EXP109; EXP109/115/116 statuses unchanged; H6's logit-level HELD stands alone as the only honesty signal | LOG-4609; `research/experiments/EXP117_PTTSCGEN_REPORT_2026-09-29.md`; independent verdict review LOG-4610 (BIND — no caveat) |
| **EXP118** — **RUN-INVALID**: logit-lens layer-locality of the H6 honesty signal (H13/HDI-LOC) | H6 apparatus extended per-layer via the logit lens (final LayerNorm + unembedding, no bias; argmax over the two pinned entity-name token ids; ties → E2); pre-registered contrast C = mean(fidelity L16–L24) − mean(fidelity L0–L8); per-site degeneracy diagnostic (mean post-softmax mass on (t1,t2) < 0.01) + run-validity rule (<5 non-degenerate sites in either window → RUN-INVALID); 41/60-exact consistency pin on EXP112's archived decision column (HALT-on-drift) | pythia-410m base (frozen; 1080 forwards, 60 items × 18 layer sites, CPU, $0; LOG-331 pin matched before AND after all forwards, Δθ=0); consistency pin PASSED (lens@L24 byte-identical 60/60 to EXP112's archived readout column, 41/60 = 0.6833 exactly); BPE single-token 120/120; all provenance pins MATCH | **Early window 0/9 non-degenerate < 5/9 → RUN-INVALID** — the logit lens cannot speak at early layers on this bench (early max mass 0.000022, ~450× below the 0.01 threshold; entity-name tokens acquire unembedding mass only in the final ~5 layers). Per Law #9, **no per-site fidelity and no contrast C was read** — no verdict smuggled on the late-locality hypothesis. **Integrity win:** the executor's first attempt double-normalized at L24 → 5/60 argmax flips; the pre-registered consistency pin HALTed that attempt and arbitrated the fix (corrected lens: lm_head(h_24) at L24 == out.logits to 4.4e-06). **Report-factual defect** (verdict-untouched): report §10/§11 claimed `exp118_worksheet.json` was written — false (script writes artifacts only after the validity-rule exit; filesystem-wide find: no such file) — corrected by **erratum LOG-4621** | 1080 forwards, CPU, $0 | N/A (apparatus) | — (late-locality question never tested) | Y | **RUN-INVALID (apparatus, bound)** — review LOG-4620 QUALIFY (verdict stands, one binding caveat recorded as erratum); no verdict smuggled; EXP112's HELD (41/60) stands unchanged; H6's logit-level HELD stands alone as the only honesty signal, with no layer foothold | LOG-4619/4620/4621; `research/experiments/EXP118_HDILOC_REPORT_2026-09-29.md`; independent verdict review LOG-4620 (QUALIFY — caveat: worksheet-claim erratum) |
| **EXP119** — **RUN-INVALID**: planning hypothesis re-asked on the zero-generation logit channel (H14/PTTSC-LOGIT) | Plan-conditioned planner/executor pipeline vs baseline on the EXP107 template-decorrelated bench; Phase-0a planner bench-transfer + Phase-0b tokenization-identity pin (plan-tail [-3:] vs fixed `? Answer:` baseline-tail [-3:]; mismatch on ANY item → RUN-INVALID immediately); full run never licensed | pythia-410m base (frozen; 10 Phase-0a planner generations only; LOG-331 pin matched pre-contact, Δθ=0); tokenizer-only mechanism replication (no model contact) | **Phase 0b tokenization-identity mismatch on item 0: plan tail `[444, 37741, 27]` vs baseline `[32, 37741, 27]`** → RUN-INVALID; zero Phase-0b forwards ran; no metric read (Law #9); tuple[0] never touched (Law #7). Structural mechanism (independent review): any plan block whose final outline doesn't end in `?` breaks the identity — the §0(6) breaking point ("tokenization effects break the channel") realized exactly as anticipated. Phase 0a 10/10 planner-valid (gate did not fire) — apparatus observation: T2-P2 transfers to EXP107 as a plan elicitor | 10 generations, CPU, $0 | N/A (apparatus) | — (planning question never tested) | Y | **RUN-INVALID (apparatus, bound)** — H11's planning hypothesis now untested on BOTH EXP107 decision channels (generation dead per EXP117, plan-prefix logit slot dead per EXP119); licenses nothing, retires only the exact tested composition (T2-P2 plan block + [-3:] identity); EXP112's HELD unchanged. Binding lesson: future execution lanes must persist raw generation records before any verdict is written (EXP119's Phase-0a texts were not persisted; verdict intact) | LOG-4627/4628; `research/experiments/EXP119_PTTSCLOGIT_REPORT_2026-09-29.md`; independent verdict review LOG-4628 (BIND — no caveat) |
| **EXP120** — **CONTINUE (QUALIFIED)**: EXP111's trained-head signal replicates on a second independently constructed template-decorrelated bench (H15/LFH-GEN2) | Trained L2-logistic head (C=1.0, lbfgs, no tuning) on frozen L20 final-token embeddings of a NEW 60-item bench (bench 2: four 15-item cells, new verb families "surpasses"/"is below", new river+tree entity sets, no shared template vocabulary beyond ordinary English function words); stratified 30/30 train/test split (seed 20260929, ID overlap 0) — the pinned H5 discipline verbatim; registered bars: ≥20/30 AND G<0.30 → CONTINUE | pythia-410m / L20 (frozen; 60 fresh CPU forwards; LOG-331 pin before AND after, Δθ=0) | Construction gates ALL pass: design-time assertions; G-C1 pure-template detector **30/60 ≤ 36/60** (chance-level); G-C2 \|Pearson\| = **0.0475 ≤ 0.10** (no bench-1 labels/embeddings enter the analysis — Law #13); G-C3 QUESTION_SUFFIX byte-exact + deterministic rebuild; canonical pin `1d7d22c0…82fb2eee`. **Test 25/30 = 0.8333** (per-cell 4/8, 7/7, 7/7, 7/8; acc(F)=0.7333, acc(T)=0.9333), **G = −0.2000 < 0.30** → CONTINUE. Exact one-sided binomial p = **0.00016** (report's hand-written "≈0.0009" corrected by erratum LOG-4635; conservative error, verdict-unaffected). Determinism re-fit byte-identical; all seven record-keeping artifacts hash-pinned before the verdict; run-1 JSON tuple-key crash repaired by full deterministic re-run (byte-identical hashes, both logs preserved) | 60 extractions + sklearn head fit, $0 CPU, torch 2.14.0+cpu / transformers 5.17.0 / sklearn 1.9.1 | Train-probes (head fit on bench-2 train split, applied to held-out test items) | Y (the head's read of bench 2; the generality hypothesis: EXP111 replicates) | Y | **CONTINUE (bound, QUALIFIED)** — the output-side readout room's positive is now a two-bench observation of the same trained-readout signal (layer-20 subject-position cue); **boundary-science decodability entry, NOT capability** — correlation, not steering; no decision flips moved; no cross-bench statistical comparison (unlicensed fence honored); EXP111's bench-1 observation restated, never re-adjudicated (Law #8); fences: no capability, no generality beyond the two benches/layer/model, no re-licensing of H1/H4 or closed families, novelty N1. New defect class recorded: **report authors hand-writing p-values instead of executor-computed values** — future pre-registrations must pin p-values as executor-computed | LOG-4633 (execution); `research/experiments/EXP120_LFHGEN2_REPORT_2026-09-29.md` (§10 erratum LOG-4635); independent verdict review LOG-4634 (QUALIFY — verdict stands, p-value caveat) |
| **EXP121** — **RUN-INVALID**: planning hypothesis re-asked on the logit channel through the tail-preserving composition (H19/PTTSC-SUFFIX) | Plan-conditioned pipeline vs baseline on the EXP107 template-decorrelated bench with the plan text inserted BETWEEN the premise and the fixed question tail (placement A — licensed by a tokenizer-only [-3:] pre-check), so both arms end in byte-identical `" Question: Who is higher in rank? Answer:"`; Phase-0a planner bench-transfer + Phase-0b [-3:] identity + G1 per-arm pins; full run (60 planner generations + 60 plan-arm + 60 baseline-arm forwards) | pythia-410m base (frozen; 60 greedy generations + 120 forwards, CPU, $0; LOG-331 pin before AND after all model contact, Δθ=0) | **Phase-0 gates ALL passed** (tokenizer-only [-3:] identity 60/60 before model contact; Phase 0a planner-valid 10/10; Phase-0b identity + G1 10/10) — EXP119's structural break does NOT recur under placement A (both tails `[32, 37741, 27]`); the pre-reg's §0(6) breaking point ("tokenization effects break the channel") did not realize. Full run: planner-valid 60/60; baseline-arm G1 60/60 (mass 0.068–0.568); baseline reproduction **60/60** vs EXP112's archived readout; baseline variation distinct=2/minority=27 (gate passed). **Plan-arm G1: 22/60 degenerate** (summed post-softmax mass on the two pinned entity tokens 0.000142–0.008571 < 0.01 — the distribution concentrates elsewhere at the final position) → **n_valid = 38/60 < 48 → RUN-INVALID (elicitation-failure gate)**. Also fires under the stricter sum ≥ 0.02 reading (30 < 48). Per Law #9 **no McNemar table and no metric was read** — no verdict smuggled. **Execution defect (disclosed, not a defect class):** the script's `finalize()` truncated the execute script to 0 bytes before hashing — the lane reconstructed the script and the review verified it bytecode-identical to the executed .pyc; reconstruction holds. **Report-factual defect** (verdict-untouched): "a second independent full run reproduced n_valid = 38 exactly" is unverifiable from retained artifacts (attempt 2's generations overwritten, not retained) — corrected by **erratum LOG-4646**; verified claim: n_valid=38/60 recomputed independently from final-run artifacts, deterministic re-read ×2 byte-identical | 60 generations + 120 forwards, CPU, $0 | N/A (apparatus) | — (planning question never tested) | Y | **RUN-INVALID (apparatus, bound)** — review LOG-4645 QUALIFY (verdict stands, one documentation caveat recorded as erratum LOG-4646); H11's planning hypothesis remains untested on the logit channel — **third distinct apparatus failure mode** (EXP117: generation channel; EXP119: tokenization identity; EXP121: plan-arm G1 mass collapse); zero decision data. One licensed upside, honestly fenced: placement A is a candidate adaptive-loop component for the plan-text pipeline — the token-asymmetry confound stands disclosed, not removed, so no planning-vs-compute attribution is licensed | LOG-4644 (execution); `research/experiments/EXP121_PTTSCSUFFIX_REPORT_2026-09-29.md` (ERRATUM LOG-4646); independent verdict review LOG-4645 (QUALIFY — verdict stands, two-run caveat) |

| **EXP122** — **CONTINUE (BIND)**: position-cue dissection — the trained head reads the target's domain-set identity on a position-scrambled bench (H16/POSITION-CUE) | Trained L2-logistic head (C=1.0, lbfgs, no tuning) on frozen L20 final-token embeddings of a NEW 60-item bench (bench 3: four 15-item cells, fresh animal/fruit entity sets disjoint from benches 1/2, new verb families "ranks above/below" and "dominates/is dominated by"); the target's final sentence position is balanced 15/15 within each label class (position-scrambled, corr = 0.0 — position carries no label information); stratified 30/30 train/test split (seed 20260929, ID overlap 0); registered bars ≥20/30 AND G<0.30 → CONTINUE | pythia-410m / L20 (frozen; 60 fresh CPU forwards; LOG-331 pin before AND after, Δθ=0) | Construction gates ALL pass: design-time assertions; G-C1 pure-template detector 32/60 ≤ 36/60; position-scramble gate (pure-position detector) 30/60 ≤ 36/60; G-C2 \|Pearson\| = 0.0322 ≤ 0.10 — no bench-1 labels or embeddings entered the analysis (Law #13); G-C3 QUESTION_SUFFIX byte-exact + deterministic rebuild; canonical pin `2b65f01e…82b165ca`; deterministic rerun byte-identical (run logs differ only in wall-clock lines). **Test 27/30 = 0.9000** (per-cell 6/8, 7/7, 7/7, 7/8; acc(F)=0.8667, acc(T)=0.9333), **G = −0.0667 < 0.30** → CONTINUE. Exact one-sided binomial p = **4.215e-06** (executor-computed via math.comb, printed by the executor — defect class (a) honored). Determinism re-fit byte-identical; all seven record-keeping artifacts hash-pinned before the verdict | 60 extractions + sklearn head fit, $0 CPU | Train-probes (head fit on bench-3 train split, applied to held-out test items) | Y (the head's read of bench 3; the position-dissection hypothesis: the signal is not a subject-position detector) | Y | **CONTINUE (bound, BIND)** — the output-side readout room's positive is now a three-bench observation of the trained identity-readout signal with position decorrelated: the head extracts the target's domain-set identity (D1 animals vs D2 fruits) at 27/30 on a bench where target sentence position is balanced 15/15 within each label class (corr = 0.0) — the subject-position-detector alternative is excluded. **Boundary-science decodability entry, NOT capability** — correlation, not steering; no decision flips moved; no cross-bench statistical comparison (unlicensed fence honored); EXP111's and EXP120's observations restated, never re-adjudicated (Law #8); fences: no capability, no generality beyond the three benches/layer/model, no re-licensing of H1/H4 or closed families, novelty N1 | LOG-4653 (execution); `research/experiments/EXP122_POSITIONCUE_REPORT_2026-09-29.md`; independent verdict review LOG-4654 (BIND — no caveat) |

| **EXP123** — **RUN-INVALID (TERMINAL)**: P4 repetition-penalty apparatus validation on the entity-name shape — the last EXP113-cleared generation protocol dies (H20/P4APPARATUS) | P4 decoding (`repetition_penalty=1.2`, `no_repeat_ngram_size=3`, greedy, `max_new_tokens=4`) on the verbatim EXP107 60-item template-decorrelated bench (canonical SHA-256 `e91b302f41f641c74e56957e526efcd4866bac62d134e157defe0a4cdd49e4f5`; `prompt == premise + QUESTION_SUFFIX` byte-exact 60/60); pinned §3.4 parse rule: `raw.strip()` → `rstrip('.,;:!?\'")]}')` → case-insensitive exact match against e1/e2 → parseable iff exactly one matches (XOR); registered bars: exceptions > 6/60 → RUN-INVALID (environment), n_unparseable ≤ 6 → CONTINUE, n_unparseable ≥ 7 → RUN-INVALID TERMINAL; no p-value registered or computed (Law #9) | pythia-410m base (frozen; 60 pass-A + 60 pass-B deterministic rerun = 120 generations, byte-identical; LOG-331 pin matched before AND after all model contact, Δθ=0); decode via `tokenizer.decode(new_token_ids, skip_special_tokens=True)` — input-prompt tokens never decoded into `raw` | **n_parseable = 0/60, n_unparseable = 60/60, n_exceptions = 0** (0 ≤ 6 → environment-bug branch not fired; **60 ≥ 7 → elicitation-failure gate fires on the full 60**). Generations are real, non-degenerate model outputs (0/60 empty) — 18 distinct outputs, all continuation attractors (e.g. `' Mercury, the planet'`, `' The Sun, the'`, most common `' The one who has'` at 12/60 — never names either candidate). Pre-reg's breaking mechanism realized: `repetition_penalty=1.2` down-weights tokens present in the input context — *including the entity-name tokens in the premise* — biasing *against* emitting the entity name, compounding EXP117's continuation attractors (EXP113's own T2 datum: P4=0/60 on outlines). On the entity-name shape P4 is an anti-elicitation protocol. Deterministic rerun byte-identical; re-parse ×2 byte-identical; raw records persisted + hash-pinned before the verdict (defect class 2 satisfied) | 120 generations, CPU, $0 | N/A (apparatus) | — (instrument closed) | Y | **RUN-INVALID (apparatus, TERMINAL, bound)** — the expected outcome under the P4-dead alternative (pre-reg predicted P(n_unparseable ≥ 7) ≈ 1): a finding, not a failure. **The entity-name generation channel is dead on ALL EXP113-cleared protocols** (P2 dead on this shape EXP115, P5 dead on tail echo EXP116, P4 dies here) — the honesty-instrument line closes **permanently on the entity-name shape**: no protocol rescue, no larger-n rescue, no parameter tweak licensed. H1/H4's T1/T2 clearances untouched; does not rescue EXP112's bench-2 logit line (different instrument); label-free race stays tied at zero. Parseability ≠ correctness (0/60 is a *format* measurement — the model never produced text matching either candidate; decision-silent correctness diagnostic vacuous, 0 of 0). Novelty N1 | LOG-4661 (execution); `research/experiments/EXP123_P4APPARATUS_REPORT_2026-09-29.md`; independent verdict review LOG-4662 (BIND — no caveat) |

| **EXP124** — **RUN-INVALID**: plan-as-instrument selection — the choice-information gate fires on the collapsed choice distribution (H21/PLAN-INSTRUMENT) | Plan-conditioned T2-P2 plans as the treatment instrument on the EXP107 template-decorrelated bench: per item, the planner elicits a T2 numbered-outline plan; the pinned §3.4 choice rule (leftmost-longest entity mention in the final outline in position order, |L|≥2) picks variant A vs C; registered choice-information gate: each phrasing chosen on ≥ 12 items (20% of 60) → else RUN-INVALID (decision-inert control); no metric downstream | pythia-410m base (frozen; 70 planner generations: 10 Phase-0 probe + 60 full-run, greedy, max_new_tokens=160; 20 Phase-0b probe forwards only — halted at the gate before the 120 variant forwards; LOG-331 pin matched pre-contact, Δθ=0) | **Phase-0pre: 120/120** tokenizer-only [-3:] == [32, 37741, 27]; **Phase-0a: 10/10** choice-valid (probe items 0,1,2,5,6,7,8,9,10,11); **Phase-0b: 4/10** with differing variant readouts (≥3 required), M_A=0.38102, M_C=0.46331 (both ≥0.01); planner prompts byte-identical **0/60 mismatches** vs EXP113 T2-P2 reference. Full run: **A-FIRST=48, C-FIRST=7, choice-invalid=5** (55/60 choice-valid; independent reimplementation 60/60 per-item agreement, outline-count agreement 60/60) → **C-FIRST=7 < 12 → choice-information gate FIRED → RUN-INVALID**. Failure mode (descriptive, spot-verified): 60/60 full-run generation texts contain a hallucinated `Premise:` line with entities outside the bench vocabulary; 55/55 choices are leftmost entity matches inside the hallucinated region (38 raw / 34 distinct collapsed) — the outline texts themselves contain no entity names, so every extracted "choice" is a function of model regurgitation, not plan content. Per Law #9 **no McNemar table, no b/c/d/p — no metric was read** — no verdict smuggled; the halt occurred before the forward phase, so no post-contact backbone pin exists (pre pin matched; Δθ=0 by construction) | 70 generations + 20 probe forwards, CPU, $0 | N/A (apparatus) | — (instrument-selection never tested) | Y | **RUN-INVALID (apparatus-void, bound)** — review LOG-4671 BIND (no caveat): verdict follows mechanically from the artifacts; the Phase-0-pass/full-run-collapse contrast is the key structural fact — the planner passes the probe gates but the full-run choice collapses to a decision-inert control. **H21's instrument-selection channel is UNTESTED, not retired** (a KILL would have retired it); H11's planning hypothesis survives its **FOURTH RUN-INVALID** (EXP117, 119, 121, 124) — untested, not killed; no further H11 composition is licensed without a genuinely new instrument class (per the H21 draft §0(d)). **New binding lesson (defect class 8):** a choice-extraction rule on the final outline in position order must assert the final outline is plan content, not regurgitation — or the instrument is unlicensed; future plan-as-instrument designs must gate on generation construct-validity (e.g. final outline contains no `Premise:`/question-tail regurgitation) before any choice extraction | LOG-4670 (execution); `research/experiments/EXP124_PLANINSTRUMENT_REPORT_2026-09-29.md`; independent verdict review LOG-4671 (BIND — no caveat) |

### 3.2 The program's position, stated without softening

[FACT]/[OBSERVATION]: the program holds **zero positive signals for
autonomous steering** (LOG-204 ruling 1 — stated plainly per the CEO's
order; unchanged by K1-EXONERATED, which exonerated the *tilt* account, not
the *label-use* fact, and unchanged by EXP092-CONTINUE, which licenses
task-information at L11, not a steering mechanism). Its most-cited positive
number (+10pp bridge rescue) is a Per-item control whose §H7 demotion is
under CEO re-review (LOG-213) — the tilt accounts are dead on both ends
(target-boost 0/60, K1; foil-suppression 0/60, EXP082), and the live
mechanism is the relational (t−f) readout effect, still label-informed. Its
best autonomous number (+4pp, EXP056) is not significant. Its mechanism
program is six dead static-geometry rooms (five at L20 + the shared-direction
L11 generalization, EXP093) + one killed QK-subspace sentence + one retracted
Procrustes claim + two dead directional-readout hypotheses (K1, EXP082) +
one dead free-lunch scorer (EXP091, a genuine null from a working instrument)
+ one algebraic-untestability boundary (EXP085, k=2) + one infeasible
archived-verification approach (S3-1/S3-3 Stage-0) + two predicted halts
(EXP067 Stage A, EXP078 energy gate) + one plan halted on its own guard (K3
Phase-0). Its live assets are: the I1 boundary (a diagnostic instrument), the
G1 per-head table (a measurement-pruned instrument), the K2 pilot (LICENSED,
awaiting founder GPU), Sprint-3 Stage-0b pilots (QUEUED — need Law-#14-signed
plans + CEO GPU clearance), the R1–R7 pipeline (R1/R2/R3 signed and queued),
S4-8/S4-9 (fresh proposals from the Friday cull, LOG-4353), and
EXP080/081/084 still gated on CEO GPU clearance. The week's one licensed
positive: **EXP092 — frozen Pythia-410m layer 11 carries significant task
information** (1-NN LOO, Bonferroni-significant, ≥10pp above null) — an
observation, not a capability; EXP093's kill banked its immediate
consequence: information ≠ influence.

**The S6 L11-rescue program, closed 2026-09-28 (LOG-4464).** The nine
rescue experiments after EXP094 read as one arc. Per-item static geometry
refuted by inertness (EXP094: 0 flips/120 arms); the α grid inert at every
ratio (EXP095); movement that exists but is not directionally attributable
(EXP096/097, EXP099 fragility); the composition premise not supported
(EXP098: random joint 12 flips vs 7 joint); and the externally-computed
attention-gate family closed 4/4 — mean-at-L11 untestable at 0/60 coverage
(EXP100), max-at-L11 Refuted (EXP101: 1 flip, right→wrong), mean-at-L20
untestable at 1/60 (EXP102), max-at-L20 Refuted (EXP103: 3 flips, p=1.0,
1 positive/55 fired → one-sided 95% UB 5.3%). The S6-5 pooled audit fixes
the program ceiling: 5/381 directional flips, one-sided 95% UB **2.74%**.
An innovation-design lane then falsified all four self-computed-gate
candidates on paper (LOG-4463) — the CEO ruled STAND-DOWN on the whole
L11-rescue program (LOG-4464) with the rational update **"the direction is
the problem, not the gate."** What this arc contributes is boundary
science, not capability: ten experiments, ~2,000 CPU passes, $0, every
rescue dead, untestable, or uninterpretable — the wall behind the L11
direction is now mapped on all four gate cells and the static/per-item
geometry side. The LOG-4460 terminality claim bars any fifth
externally-computed gate variant; surviving conditional license is
self-computed gates and beyond, each needing its own pre-registration and
Law #14 review. The S5-2 power audit (LOG-4392) fixes the honest bounds on
the underlying static-geometry kills — per-arm 95% upper 4.87%, the
skeptic's 1–5% band NOT killed at $0 — and S5-3 (LOG-4393) re-licenses the
eight EXP077 variants as never-decodable (0/8 clear the bar): the rooms
were empty, not decodable-yet-inert. The GPU queue (K2 → EXP083 → EXP084 → EXP086 Stage B →
EXP088 → EXP087) is untouched. **Capability scoreboard: unchanged — still
zero positive signals for autonomous steering.**

**The I2′ line, opened and CLOSED 2026-09-28 (LOG-4480–4491).** EXP085's death-debt
(selection-failure instrumentation) ran its full arc in one day: S4-8 SIGNED
(LOG-4480), EXP104 Tier-0 → HOLD on bench sanity (0.1833 < 0.25) →
Inconclusive (LOG-4481/4482); autopsy traced the HOLD to a position-A prior
(30/60, p=2.02e-12), an instrument confound, not a premise kill (LOG-4483);
S4-8′ cloze recalibration SIGNED (LOG-4488); EXP105 Tier-0 **PASSED**
(0.5333, LOG-4489) — the cloze format rescued measurability and confirmed
the A-prior diagnosis; EXP105 battery **Refuted at step 9** (LOG-4491):
ΔM_T = +0.2381 vs ΔM_R = 0.0000, but primary T-vs-R McNemar p=0.0625 ≥ 0.05 —
missed CONTINUE by one flip; foil overlap O = 0.571 > 0.5 made the F arm
non-diagnostic, exactly as the pre-registered N1 gate anticipated. Pre-
registered stop rules closed the line: no re-run, no larger population, no
third readout. **The I2′ line is a complete falsification-terminal arc —
instrument built, confound diagnosed and removed, premise certified-not-
specific by its own licensed bar.** Boundary science, not capability.

**The summit-sprint H-wave, 2026-09-29 (LOG-4527–4558).** All four
sprint hypotheses executed to binding outcomes. H3's label-free head
produced the day's apparent positive — 60/60 transfer, p=8.67e-19 —
and the program's own adversarial machinery killed it within hours:
EXP107's template-decorrelated bench scored the exact template-detector
signature (34/60, p=0.1831; original-word cells 30/30, flipped-word
cells 4/30), voiding the GPU head-training proposal the CONTINUE had
licensed — the output-side trained-head room is retired as artifact-only
unless a new family earns its license. H1 (EXP108) and H4 (EXP109) died
at the apparatus layer, not their hypotheses: base Pythia-410m cannot
follow instruction-style generation prompts — self-reports collapsed to a
degenerate echo, planners to a repetition attractor. The durable
methodological rule: any generation-based frozen experiment must validate
instruction-following before treating outputs as measurements. H2
(EXP110) certified the I2′ boundary under weight-only INT8
fake-quantization (6/7 tiers, structural intact) — the program's first
licensed precision-certification of a boundary verdict, simulation-scoped
and fenced. And the program's adversarial machinery then *confirmed*
a positive: **H5 (EXP111)** — the trained L2 head scored **24/30 = 0.8000,
one-sided p=0.00072, G=0.0000** on the very template-decorrelated bench
that killed EXP106, firing the CONTINUE branch with the kill branch
untouched (LOG-4568 execution; independent review LOG-4569 QUALIFIED,
required p-value footnote). This is the **day's first genuine positive
signal and the program's first output-side result to survive adversarial
testing** — but it is a **boundary-science decodability entry, not a
capability entry**: one layer-20 correlation on one n=30 bench; the GPU
head-training proposal voided by EXP107 is re-licensed under
decorrelated-bench discipline (still founder-hardware-gated). The
wave's net: one killed transfer reading; two RUN-INVALID apparatus
failures; one precision-certified boundary; one hardened apparatus rule;
and one surviving above-chance output-side correlation; and one HELD
honesty-instrument reading — **H6 (EXP112)**, the H1 successor under a
zero-generation apparatus, scored **fidelity 41/60 = 0.6833**, inside the
registered 34–41/60 HELD band (all degeneracy guards passed before any
metric was read — the channel is genuine, the signal is weak and below
the decisive bar; it licenses nothing and retires nothing; LOG-4575
execution, independent review LOG-4576 BIND). The wave's net: one killed
transfer reading; two RUN-INVALID apparatus failures; one
precision-certified boundary; one hardened apparatus rule; one surviving
above-chance output-side correlation; one HELD honesty reading; one
apparatus CONTINUE (EXP113, bound); and one clean test-time-scaling kill (EXP114, bound). On the apparatus side, the generation axis is open for this
backbone under pinned protocols: few-shot (P2) and priming (P5) clear ≥80%
mechanically-parseable outputs on both the H1-shaped (T1) and H4-shaped (T2)
tasks, which licenses H1/H4 revival as NEW hypotheses with the named clearing
protocols (each carrying its own elicitation-failure gate) but revives neither. **H8 (EXP114)** — the positional-order-ensembling test-time-scaling axis — is cleanly dead: the K=5 ensemble scored **38/60 vs the canonical single-order baseline 41/60 (net −3, one-sided exact McNemar p=0.9375)**, firing the registered net ≤ 0 → KILL branch with no post-hoc re-interpretation. The fences hold: this retires only the positional-order-ensembling axis for this task class — test-time scaling in general and the adaptive-loop program are explicitly NOT retired. The 5pp below-baseline reading is a labeled [OBSERVATION]; no rescue is licensed or implied (LOG-4591 execution; independent verdict review LOG-4592 BIND, no caveat).

**H9 (EXP115) and H10 (EXP116)** — the two EXP113-licensed honesty-instrument
revival hypotheses — both died at the apparatus layer without ever testing
the hypothesis, and the two deaths were *different* failures, each
independently confirmed from the raw generations (independent exact-artifact
verdict reviews LOG-4599/4603 — both BIND, no caveat): few-shot (P2)
elicitation collapsed into recitation (n_unparseable = **38/60** ≥ 7; all 60
generations contain `Premise:`, the last exemplar block regurgitated verbatim),
while priming (P5) elicitation — structurally immune to recitation (zero
exemplar blocks) — collapsed into tail echo (n_unparseable = **37/60** ≥ 7; 27
of the 37 unparseable echo the unfinished priming sentence
`"\n\nThe entity higher in rank is"` verbatim; 0/60 contain `Premise:` — recitation
confirmed absent). Both failures were inside the pre-regs' disclosed risk
envelopes; the gates fired before any metric was read (fidelity null, not
wrong); all archive pins and the LOG-331 backbone pin (Δθ=0) independently
re-verified. **Apparatus failures, not hypothesis failures — but the
consequence is final for this line: the generation-level honesty instrument
has no EXP113-cleared protocol left on the entity-name shape** (P2 dead on
this shape, EXP115; P5 just failed, EXP116). H6's logit-level HELD (41/60)
stands alone as the only honesty signal. The reports KILL, HELD, and CONTINUE
nothing — no verdict was smuggled. The durable methodological update:
instruction-following validation on a task *shape* does not transfer to an
*answer* shape — P5's 60/60 clearance was on single letters, and the
entity-name shape broke it (LOG-4603 reviewer note: P4, cleared T1-only, was
never in the named protocol set and remains untested future-proposal material,
not a defect in this report).

**H11 (EXP117)** — the EXP113-licensed planner/executor revival hypothesis,
a NEW apparatus on the T2 numbered-outline shape (not a re-run of EXP109) —
died at the Phase-0 gates without ever testing the planning question
(independent exact-artifact verdict review LOG-4610 — BIND, no caveat).
Phase 0b fired with **0/10 parseable**: the model enumerates entities as a
list (e.g. `'\n\n1. Jupiter\n\n2. Mars\n\n3. Venus\n'`) instead of naming one
— the **4th consecutive entity-name-generation-slot failure** on this shape
(EXP109 80/80 sampled; EXP115 38/60 recitation; EXP116 37/60 tail echo;
EXP117 0/10 enumeration). Phase 0a's literal recitation gate did NOT fire
(0/10) while the content-level diagnostic scored 10/10: the review
adjudicated a REAL protocol defect — the §3.7 literal recitation definition
compares marker-stripped extracted outlines against marker-prefixed
exemplar lines, making it structurally inert for content recitation — but
it did NOT change the verdict (the gate was applied as written; Phase 0b
fired independently; the RUN-INVALID is overdetermined). It is recorded as
a binding apparatus-definition lesson: **no future protocol may reuse the
§3.7 definition.** The generation channel for entity-name answers is dead
on base Pythia-410m across four different apparatuses; H6's logit-level HELD
stands alone as the only honesty signal. Apparatus failure, not a hypothesis
failure — no verdict was smuggled, EXP109/115/116 statuses unchanged.
Parseable output ≠ reasoning, honesty, or capability — a real methodological
gain, not a capability signal. **Capability
scoreboard: unchanged — still zero positive signals for autonomous
steering; the label-free race stays tied at zero. One n=30 bench does
not move the capability scoreboard.**

**H13 (EXP118)** — asked WHERE the H6 honesty signal lives (H6's apparatus extended per-layer via the zero-training logit lens) — died at the pre-registered run-validity rule without ever testing the late-locality hypothesis (independent exact-artifact verdict review LOG-4620 — QUALIFY: the verdict stands on the exact artifacts, with one binding caveat recorded below). Early window (L0–L8) **0/9 non-degenerate** (required ≥5): the logit lens cannot speak at early layers on this bench — entity-name tokens acquire unembedding mass only in the final ~5 layers (early max mass 0.000022, ~450× below the 0.01 threshold). Per Law #9, **no per-site fidelity and no contrast C was read** — no verdict smuggled. The protocol's integrity proved itself: the executor's first attempt double-normalized at L24 (5/60 argmax flips), and the pre-registered 41/60-exact consistency pin HALTed that attempt and arbitrated the corrected lens — a genuine apparatus win, not a finding about the model. The caveat: the report's §10/§11 claimed `exp118_worksheet.json` was written — false (the script writes artifacts only after the validity-rule exit; a filesystem-wide find returns no such file) — corrected by **erratum (LOG-4621)**; verdict untouched. Apparatus failure, not a hypothesis failure. H6's logit-level HELD (41/60) stands alone as the only honesty signal — with no layer foothold yet, and no larger-N rescue, no different window, and no different lens is licensed (all barred). **Capability scoreboard: unchanged — still zero positive signals for autonomous steering; the label-free race stays tied at zero.**

**H14 (EXP119)** — re-asked H11's planning question on the proven zero-generation logit channel, and the channel itself died at the apparatus layer (independent exact-artifact verdict review LOG-4628 — BIND, no caveat). The pre-registered Phase-0b tokenization-identity pin (plan-tail [-3:] must equal the baseline's fixed `? Answer:` tail [-3:]) failed on the first probe item: plan tail `[444, 37741, 27]` vs baseline `[32, 37741, 27]` — the plan block's final outline ends in a word, not `?`, so the final token run differs. The review replicated this tokenizer-only (no model contact) and adjudicated it **structural, not item-specific**: any plan block whose final outline does not end in `?` breaks the pinned identity — the pre-reg's §0(6) breaking point ("tokenization effects break the channel") realized exactly as anticipated. Zero Phase-0b forwards ran; per Law #9 no metric was read and tuple[0] was never touched (Law #7) — no verdict smuggled; the full run was never licensed. Consequence: **H11's planning hypothesis is now untested on both EXP107 decision channels** (the generation channel died in EXP117, the plan-prefix logit slot died here). Small positive, honestly framed: Phase 0a scored **10/10 planner-valid** (gate did not fire) — T2-P2 transfers to the EXP107 bench as a plan elicitor (apparatus observation, not a capability claim). The binding record-keeping lesson: the execution lane did not persist raw Phase-0a generation texts (counts and diagnostics only — verdict intact, record-keeping insufficient); **future execution lanes must persist raw generation records before any verdict is written.** Apparatus failure, not a hypothesis failure. H6's logit-level HELD (41/60) stands alone as the only honesty signal. **Capability scoreboard: unchanged — still zero positive signals for autonomous steering; the label-free race stays tied at zero.**

**H15 (EXP120)** — the generality test the innovation sprint
pre-registered for EXP111's output-side positive: does the trained head
replicate on a *second, independently constructed* template-decorrelated
bench? Yes, with the license exactly as written (independent
exact-artifact verdict review LOG-4634 — QUALIFY: the registered
CONTINUE stands, one documentation-precision caveat). Bench 2 passed
every construction gate — design-time assertions (60 items, four 15-item
cells, opposite verb families on flipped items, `exp120_*` namespace
disjoint from bench 1), G-C1 pure-template detector 30/60 ≤ 36/60, G-C2
|Pearson| = 0.0475 ≤ 0.10 (**no bench-1 labels or embeddings entered
the analysis — the review verified the Law #13 fence in the
implementation, not just the claim**), G-C3 byte-exact decomposition —
and the pinned H5 protocol ran verbatim: **test 25/30 = 0.8333 with G =
−0.2000 < 0.30**, firing the registered ≥20/30-with-G<0.30 CONTINUE
branch (LOG-4633 execution; backbone LOG-331 pin before AND after all 60
fresh CPU extractions, Δθ=0; determinism re-fit byte-identical). The
review recomputed the head test from scratch with numpy — 25/30,
per-cell descriptives, and G all match. The single caveat: the report's
hand-written "≈0.0009" p-value for 25/30 is wrong — exact one-sided is
**0.00016** — an error in the *conservative* direction that cannot have
licensed the verdict, corrected by **erratum (LOG-4635)**; the
executor never computed a p. The unlicensed cross-bench
statistical-comparison fence was honored (each bench's numbers stated
descriptively, no test between bench 1 and bench 2), and EXP111's
bench-1 observation was restated, never re-adjudicated (Law #8). The
binding apparatus-definition lesson from this cycle: **report authors
hand-writing p-values instead of executor-computed values is now a
defect class** — future pre-registrations must pin p-values as
executor-computed (the run-1 JSON tuple-key crash was itself repaired
honestly: full deterministic re-run, byte-identical artifact hashes,
both logs preserved). Honest placement: the output-side readout room's
positive is now a **two-bench observation** — a trained L2 head
extracting the subject-position cue at layer 20 on two independently
constructed benches — but it is still **boundary-science decodability,
not capability**: correlation, not steering; no decision flips moved;
the label-free race stays tied at zero; EXP112's HELD untouched.

**H16 (EXP122)** — the position-cue dissection of EXP111/EXP120's trained-head signal: does the head read the target's domain-set identity, or merely its sentence position? The test ran the pinned H5 discipline verbatim on a third, independently constructed bench (bench 3: 60 items, fresh animal/fruit entity domains disjoint from benches 1/2, new verb families "ranks above/below" and "dominates/is dominated by", four 15-item cells) with the position scramble built into the construction itself — the target's final sentence position is balanced **15/15 within each label class** (corr = 0.0), so position carries no label information, and a dedicated pure-position detector gate (30/60 ≤ 36/60) guards the design. All construction gates passed (G-C1 32/60, position gate 30/60, G-C2 |Pearson| = 0.0322 — no bench-1 labels or embeddings entered the analysis (Law #13), G-C3 QUESTION_SUFFIX byte-exact + deterministic rebuild; LOG-331 pin before AND after all 60 fresh CPU extractions, Δθ=0). The trained L2-logistic head (C=1.0, lbfgs, seed 20260929, no tuning, determinism re-fit byte-identical) scored **test 27/30 = 0.9000** (per-cell 6/8, 7/7, 7/7, 7/8; acc(F)=0.8667, acc(T)=0.9333), **G = −0.0667 < 0.30** → CONTINUE (independent exact-artifact verdict review LOG-4654 — BIND, no caveat; exact one-sided p = 4.215e-06, executor-computed — defect class (a) honored). Honest placement: the output-side readout room's positive is now a **three-bench observation of the identity-readout signal with position decorrelated** — the subject-position-detector alternative is excluded — but it remains **boundary-science decodability, not capability**: correlation, not steering; no decision flips moved; no cross-bench statistical comparison was licensed or run; EXP111's and EXP120's observations restated, never re-adjudicated (Law #8); fences hold (no capability, no generality beyond the three benches/layer/model, no re-licensing of H1/H4 or closed families); novelty N1. H11's planning hypothesis remains untested across the three EXP117/EXP119/EXP121 apparatus failures — zero decision data. **Capability scoreboard: unchanged — still zero positive signals for autonomous steering; the label-free race stays tied at zero.**

**H19 (EXP121)** — re-asked H11's planning question a second time on the logit channel, now through the composition that survives EXP119's structural break: the plan text sits between the premise and the fixed question tail (placement A), so both arms end in the byte-identical ` Question: Who is higher in rank? Answer:` run. Every apparatus-layer gate that killed EXP117/EXP119 was cleared: tokenizer-only [-3:] pre-check **60/60** before model contact, Phase 0a planner-valid **10/10**, Phase-0b identity + G1 **10/10** — the pre-reg's §0(6) breaking point ("tokenization effects break the channel") did NOT realize. The full run (60 planner generations + 60 plan-arm + 60 baseline-arm forwards, 0 exceptions, Δθ=0) died one layer deeper, at the readout-mass degeneracy gate: on 22/60 items the plan-inserted arm drove the summed post-softmax mass on the two pinned entity tokens to 0.000142–0.008571 (< 0.01 — the distribution concentrates elsewhere at the final position) while the baseline arm never dropped below 0.068 on the same items → **n_valid = 38/60 < 48 → RUN-INVALID (elicitation-failure gate)** (independent exact-artifact verdict review LOG-4645 — QUALIFY: the verdict stands on the exact artifacts, one documentation caveat recorded as **erratum LOG-4646** — the report's "second independent full run reproduced n_valid = 38" is unverifiable from retained artifacts; the verified claim is n_valid=38/60 recomputed independently from the final-run artifacts, deterministic re-read ×2 byte-identical). Also fires under the stricter sum ≥ 0.02 reading (30 < 48); baseline reproduction 60/60 vs EXP112's archived readout; baseline variation distinct=2/minority=27 (gate passed); per Law #9 **no McNemar table and no metric was read** — no verdict smuggled. Consequence: **H11's planning hypothesis remains untested on the logit channel — now THREE distinct apparatus failure modes** (EXP117: generation channel; EXP119: tokenization identity; EXP121: plan-arm G1 mass collapse) — zero decision data, and each failure closes only its own exact composition. The one licensed upside, honestly fenced: placement A is a candidate adaptive-loop component for the plan-text pipeline — the token-asymmetry confound stands disclosed, not removed, so no planning-vs-compute attribution is licensed. **Capability scoreboard: unchanged — still zero positive signals for autonomous steering; the label-free race stays tied at zero.**

**H20 (EXP123)** — the P4 repetition-penalty apparatus validation (the LOG-4603 reviewer note's reserved future-proposal material, now its own licensed experiment) — asked the one remaining honest question on the entity-name shape: is there any EXP113-cleared generation protocol that isn't dead here? No: P4 (`repetition_penalty=1.2`, `no_repeat_ngram_size=3`, greedy, `max_new_tokens=4`) on the verbatim EXP107 60-item bench produced **n_parseable = 0/60, n_unparseable = 60/60, n_exceptions = 0** — the elicitation-failure gate fired on the full 60 (independent exact-artifact verdict review LOG-4662 — BIND, no caveat; independently recomputed from the raw artifacts with zero mismatches; deterministic rerun byte-identical; re-parse ×2 byte-identical; raw records persisted and hash-pinned before the verdict; LOG-331 pin before AND after all model contact, Δθ=0). The generations are real, non-degenerate model outputs (0/60 empty) — 18 distinct continuation attractors (e.g. `' Mercury, the planet'`, `' The Sun, the'`, the most common `' The one who has'` at 12/60 — never naming either candidate) — a genuine signal, not a decode artifact: the pre-reg's breaking mechanism realized exactly (the repetition penalty down-weights tokens already present in the input context, *including the entity-name tokens in the premise*, biasing against emitting the entity name — on this shape P4 is an anti-elicitation protocol, compounding EXP117's continuation attractors and EXP113's own T2 datum of P4=0/60 on outlines). This was the **expected** outcome (pre-reg predicted P(n_unparseable ≥ 7) ≈ 1): a finding, not a failure. **Terminal reading, licensed:** the entity-name generation channel is dead on **all** EXP113-cleared protocols — P2 died on this shape (EXP115), P5 died on tail echo (EXP116), P4 dies here — the honesty-instrument line closes **permanently on the entity-name shape** (no protocol rescue, no larger-n rescue, no parameter tweak licensed); H1/H4's T1/T2 clearances are untouched; EXP112's bench-2 logit line is not rescued (a different instrument); the label-free race stays tied at zero. Parseability ≠ correctness (registered): 0/60 is a *format* measurement; the decision-silent correctness diagnostic is vacuous (0 of 0). Apparatus closure, not a hypothesis kill. **Capability scoreboard: unchanged — still zero positive signals for autonomous steering; the label-free race stays tied at zero.**

**H21 (EXP124)** — plan-as-instrument selection (H11's planning question
re-asked through the instrument-selection channel): per item, a T2-P2 plan
is elicited and the §3.4 choice rule picks variant A vs C from the final
outline in position order. Phase-0 cleared everywhere (tokenizer-only
[-3:] 120/120 before model contact; choice-validity 10/10; variant
discriminability 4/10 with M_A=0.38102, M_C=0.46331; planner prompts
byte-identical 0/60 vs the EXP113 T2-P2 reference) — then the full run
collapsed: **A-FIRST=48, C-FIRST=7, choice-invalid=5** (independently
reimplemented with 60/60 per-item agreement, outline-count agreement
60/60) → **C-FIRST=7 < 12 → the registered choice-information gate
fired** (decision-inert control → RUN-INVALID; independent exact-artifact
verdict review LOG-4671 — BIND, no caveat). The descriptive failure mode:
60/60 full-run generation texts carry a hallucinated `Premise:` line with
entities outside the bench vocabulary (38 raw / 34 distinct collapsed),
and the choice rule reads the leftmost entity match inside the
regurgitation — the instrument was never a treatment. Per Law #9 no
McNemar table, no b/c/d/p — no metric was read; the lane halted before
the 120 variant forwards (no post-contact backbone pin; pre-contact pin
matched, Δθ=0 by construction). **H11's planning hypothesis survives its
FOURTH RUN-INVALID** (EXP117 generation, EXP119 tokenization identity,
EXP121 plan-arm G1 collapse, EXP124 choice-information collapse) —
untested, not killed; the instrument-selection channel is NOT retired by
verdict (a KILL would have retired it); **no further H11 composition is
licensed without a genuinely new instrument class** (per the H21 draft
§0(d)). **Capability scoreboard: unchanged — still zero positive signals
for autonomous steering; the trained-head line remains a three-bench
identity-readout CONTINUE (decodability, not steering); the label-free
race stays tied at zero.**

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
- v1.1 — 2026-09-25 (LOG-4353, Friday cull): added the week's verdict rows —
  EXP067 STAGE_A_HALT, EXP078 ENERGY_GATE_HALT, K3 Phase-0 HALT on FATAL G4,
  S3-1/S3-3 Stage-0 archived-gate INFEASIBLE, EXP085 KILLED as designed,
  EXP090 RUN-INVALID (G1 by construction), EXP091 KILL (free-lunch scorer),
  EXP092 CONTINUE (L11 task information licensed — the week's one licensed
  positive), EXP093 KILL UPHELD (information ≠ influence generalizes the
  L20 boundary); §3.2 inventory and §0 static-steering row updated to match.
  Same axes, same honesty: SCBI holds zero positive signals for autonomous
  steering; the label-free race stays tied at zero. No literature re-check
  this cycle (next due 2026-10-23).
- v1.2 — 2026-09-28 (benchmark-analyst lane): plotted the full EXP094–103
  S6 wave + S6 stand-down — EXP094 (per-item static L11 KILL by inertness,
  0/120), EXP095 (α-grid KILL), EXP096 (KILL, fragility), EXP097
  (PIVOT-fragility), EXP098 (PIVOT-premise, composition unsupported),
  EXP099 (PIVOT-fragility, directional claim not supported), EXP100
  (PIVOT-untestable, mean-L11 gate 0/60), EXP101 (Refuted, max-L11 gate
  16/60, 1 flip right→wrong), EXP102 (PIVOT-untestable, mean-L20 gate
  1/60), EXP103 (Refuted, max-L20 gate 55/60, 3 flips p=1.0, one-sided 95%
  UB 5.3% on directional flip rate) — the {mean,max}×{L11,L20} externally-
  computed attention-gate family closed 4/4; S6-5 pooled audit (5/381 →
  95% UB 2.74%); S6 L11-rescue STAND-DOWN (LOG-4463/4464, "the direction
  is the problem, not the gate"). §3.1 rows + §3.2 position paragraph added.
  Capability scoreboard: unchanged — zero positive signals for autonomous
  steering; the label-free race stays tied at zero. Standing
  PROGRESS_ANALYSIS.md written (one page, 2026-09-28). No literature
  re-check this cycle (next due 2026-10-23).
- v1.3 — 2026-09-28 (benchmark-analyst lane, LOG-4490): opened the **I2′
  line** (selection-failure instrumentation, EXP085's death-debt) —
  EXP104 Tier-0 (LOG-4481/4482): HOLD → Inconclusive (0.1833 < 0.25 bench
  sanity; premise/power bars met; battery NOT run); EXP104 autopsy
  (LOG-4483): **position-A prior 30/60, p=2.02e-12** as a measured
  instrument confound (not a model finding, not a premise kill), 7/30 =
  0.233 on non-A-prior items, per-template gradient recorded; S4-8
  pre-reg SIGNED (LOG-4480, chain LOG-4475→4480) and S4-8′ cloze
  pre-reg SIGNED (LOG-4488, chain LOG-4484→4488) with binding breaking
  point (cloze Tier-0 < 0.25 → LINE-CLOSED). EXP105 (cloze Tier-0) marked
  running — outcome NOT plotted. §0 headline + §3.2 position updated;
  PROGRESS_ANALYSIS.md gained an I2′ section. No literature re-check
  this cycle (next due 2026-10-23).
- v1.4 — 2026-09-28 (benchmark-analyst lane, LOG-4492): closed the **I2′
  line** as falsification-terminal — EXP105 Tier-0 PASSED (LOG-4489:
  0.5333 inside [0.25, 0.75], median failed-item correct rank 4.0,
  n_pop 21, tie guard 0.0; cloze rescued measurability 0.1833 → 0.5333,
  confirming the position-A diagnosis) + EXP105 battery Refuted at
  step 9 (LOG-4491: ΔM_T = +0.2381 vs ΔM_R = 0.0000, primary T-vs-R
  McNemar p=0.0625 ≥ 0.05, missed CONTINUE by one flip; O = 0.571 > 0.5
  → F arm non-diagnostic, as the pre-registered N1 gate anticipated;
  stop rules close the line — no re-run, no larger population, no third
  readout). §0 delta + §3.1 rows + §3.2 I2′ paragraph rewritten to the
  terminal state. Capability scoreboard: unchanged — zero positive
  signals for autonomous steering; the label-free race stays tied at
  zero. PROGRESS_ANALYSIS.md I2′ section updated to terminal. No
  literature re-check this cycle (next due 2026-10-23).
- v1.5 — 2026-09-29 (scoreboard-sync lane, LOG-4524): plotted **S5-2 power
  audit** (LOG-4392 — per-arm 95% upper 4.87% (n=60, 0/60) over EXP065/066,
  EXP077×8, EXP093, EXP094's T-vs-B arm; EXP078 no bound; pooled figures
  with exchangeability caveat: Bench-A 0.55%, Bench-B 1.65%, grand 0.38%;
  skeptic's 1–5% band NOT killed at $0 — honest bound, not a kill) and
  **S5-3 decode probes** (LOG-4393 — 0/8 clear the bar, never-decodable
  PIVOT for all eight EXP077 variants; instrument LIVE on D1a). §0
  static-steering row + §3.2 position paragraph updated. **Paper marker:
  v84 is the release candidate** (LOG-4519, CEO GRANT, superseding v83 —
  strict content superset; v83 frozen as prior RC). Premises verified
  in-file this cycle: EXP095/096/097 (LOG-4400/4407/4416) and EXP105
  battery (LOG-4491, repaired LOG-4495) — binding numbers confirmed, no
  contradictions, no supersession; already plotted at v1.2/v1.4, not
  re-plotted. Daily sweep LOG-4513: headline confirmed unchanged (zero
  positive signals; race tied at zero); two converging-evidence finds
  (arXiv:2609.31401, arXiv:2609.25366) tracked for the next §5 fold-in.
  No literature re-check this cycle (next due 2026-10-23).

**v1.6 delta [FACT], 2026-09-29:** plotted the summit-sprint H-wave
verdicts (independent exact-artifact verdict review LOG-4559 —
EXP107/109/110 BIND, EXP108 BIND-QUALIFIED with a required footnote).
**H3 (LFH) → EXP106→EXP107:** the trained output-side head scored
**60/60** on the disjoint transfer bench (one-sided binomial
p=8.67e-19 → registered CONTINUE, LOG-4534) — the program's first
above-chance trained-readout signal — and died on adversarial
dissection: EXP107's template-control bench (four balanced 15-item
cells, word-family × phrasing decorrelated, deterministic rewriting,
no new model calls) scored **34/60 = 0.5667, one-sided p=0.1831** —
the exact template-detector signature (original-word cells 30/30,
flipped-word cells 4/30; per-cell 15/15, 4/15, 15/15, 0/15; on all 31
items where the training-entity prior disagreed with the template, the
head followed the template). The EXP106 autonomous-transfer reading
is **KILLED**; the GPU head-training proposal it licensed is void —
no re-run, no larger-N rescue (LOG-4540 execution; review ADOPTED).
The test cannot distinguish a word-template cue from a
subject-position cue — the kill holds under either. **H1 (HDI) →
EXP108: RUN-INVALID** — all 60 self-reports unparseable (identical
degenerate token echo `[187, 187, 23433, 27]` = "\n\nQuestion:" —
base Pythia-410m continued the document pattern instead of answering);
no fidelity score, no balanced accuracy exist; H1 is neither KILLED
nor CONTINUED (LOG-4546 execution; review QUALIFIED with required
footnote: **no per-item generation records were retained — the
60/60 evidence is a single console-log summary line, and the parse
step cannot be independently re-computed**; future runs of this class
must retain per-item logs). **H4 (PTTSC) → EXP109: RUN-INVALID** —
18/20 planner items degenerated into a repetition attractor ("Plan:
Write a list of the possible answers to the question"), 80/80 baseline
generations unparseable, **n_valid = 0/20** (elicitation-failure gate
fires at 20 ≥ 3; global degeneracy tripwire fires at 88/88); no
accuracy, no (b,c) table, no McNemar p exists; the planner/executor
axis is **NOT retired**, pilot-scope fenced (LOG-4552 execution;
review ADOPTED). **H2 (QBR) → EXP110: CERTIFIED-WITH-NOTE** — the
EXP105 KILL-at-step-9 verdict reproduces under weight-only INT8
fake-quantization: **6/7 tiers**, structural tiers (Tier-0 verdict,
battery verdict class, battery step) intact; the single flip T6
(foil–top-1 overlap O: 0.5714 → 0.5000, n_pop 21→20 at the rank-5
margin) is a bounded, measured, deterministic precision effect —
documented as a note, not a pivot; certification is simulation-scoped
(not true INT8 hardware — bitsandbytes-exact is the GPU-gated ceiling);
the I2′ KILL stands regardless (LOG-4554 license ruling:
precision-certification of a statistical-null verdict ≠ the barred
retro-verification; the independent review declined the kill
invitation, SIGN). **Capability scoreboard: unchanged — still zero
positive signals for autonomous steering; the label-free race stays
tied at zero.** Durable gains this cycle are methodological: (1) base
Pythia-410m demonstrably cannot follow instruction-style generation
prompts (EXP108/EXP109 apparatus failures) — any generation-based
frozen experiment must validate instruction-following before treating
outputs as measurements; (2) the Decodability Gap boundary now carries
a bounded precision-certification statement (EXP110) — a
boundary-science entry, not a capability. No literature re-check this
cycle (next due 2026-10-23).
  PROGRESS_ANALYSIS.md: v84 release-candidate marker updated.
**v1.7 delta [FACT], 2026-09-29:** plotted **EXP111 (H5/LFH-TD)** —
**CONTINUE**, the day's first genuine positive signal and the program's
first output-side result to survive adversarial testing (independent
exact-artifact verdict review LOG-4569 — QUALIFIED with one required
footnote). Trained L2-logistic head (C=1.0, no tuning) on frozen L20
embeddings of the EXP107 template-decorrelated bench (stratified 30/30
split, seed 20260929, train/test ID overlap 0; three artifact hashes
verified pre-training; determinism re-fit byte-identical, head hash
483a91a8…afdf9f28): **test 24/30 = 0.8000** (per-cell 7/8, 6/7, 5/7, 6/8;
acc(F)=acc(T)=0.8000), **G = 0.0000 < 0.30** — the pre-installed
template-detector kill-test that executed EXP106 correctly did NOT fire
(24/30 ≥ 20/30 with G < 0.30 fires the only CONTINUE branch). **One-sided
binomial p = 0.00072** — required footnote: the report's 0.0014 is the
two-sided value; descriptive-only, no decision branch affected. The GPU
head-training proposal voided by EXP107 is re-licensed under
decorrelated-bench discipline (still founder-hardware-gated). Honest
placement: this is a **boundary-science decodability entry, NOT a
capability entry** — one layer-20 correlation on one n=30 bench; the
fences hold (no generality, no consciousness, no capability until
downstream causal tests; no re-licensing of H1/H4, static lines, or any
closed family); novelty N1. **Capability scoreboard: unchanged — still
zero positive signals for autonomous steering; the label-free race stays
tied at zero. One n=30 bench does not move the capability scoreboard.**
The day stands honestly: one positive output-side correlation survived
adversarial testing; the EXP106 kill, the two RUN-INVALIDs, and the
precision certification stand alongside it — none weakened, none
re-opened. Secondary per-layer (L4 24/30 G=−0.1333; L8 30/30; L12 29/30
G=0.0667; L16 30/30) descriptive-only, no verdict language. No
literature re-check this cycle (next due 2026-10-23).

**v1.8 delta [FACT], 2026-09-29:** plotted **EXP112 (H6/HDI-LR)** —
**HELD** (independent exact-artifact verdict review LOG-4576 — BIND, no
caveat). The honesty instrument rebuilt in logit-readout form — zero
generation, so EXP108's echo-path failure mode cannot recur by
construction: first-token entity-name-logit readout (argmax over the two
pinned logits, single-token BPE 120/120, byte-exact QUESTION_SUFFIX)
vs the registered cosine-argmax decision statistic on the EXP107
template-decorrelated bench (all three archive hashes verified; backbone
LOG-331 pin matched before AND after all 180 fresh forwards, Δθ=0).
**Fidelity 41/60 = 0.6833** (P(X≥41|60,0.5)=0.0031 — real above chance,
below the decisive bar) lands inside the registered 34–41/60 HELD band —
the CONTINUE branch (42–57/60) never fired. The Law #14-grade degeneracy
guards ran **before** any metric was read: G1 mean mass 0.301075 ≥ 0.01,
G2 readout balance 27/33 — the channel is genuine and non-degenerate; a
dead channel could not have masqueraded as a measurement. **HELD licenses
nothing, retires nothing, no re-runs (Law #4)** — a weak honesty-decoding
correlation at one read site, not consciousness, generality, or
capability. Registered [OBSERVATION], changes no verdict: fidelity
concentrates in flipped-word cells (24/30) vs original-word cells
(17/30) — recorded for separately pre-registered future work. H1 is
explicitly NOT revived: new hypothesis under a new apparatus.
**The day's tally, honestly: one CONTINUE (EXP111, bound), one HELD
(EXP112, bound), one KILL (EXP107), two RUN-INVALIDs (EXP108, EXP109),
one precision certification (EXP110, bound).** HELD is neither a positive
nor a kill. **Capability scoreboard: unchanged — still zero positive
signals for autonomous steering; the label-free race stays tied at
zero.** No literature re-check this cycle (next due 2026-10-23).

**v2.6 delta [FACT], 2026-09-29:** plotted **EXP121 (H19/PTTSC-SUFFIX)** — **RUN-INVALID** (independent exact-artifact verdict review LOG-4645 — QUALIFY: the verdict stands on the exact artifacts, one documentation caveat). H11's planning question, re-asked on the logit channel through the tail-preserving composition (plan text between the premise and the fixed ` Question: Who is higher in rank? Answer:` tail — placement A, licensed by a tokenizer-only [-3:] pre-check), cleared every apparatus-layer gate that killed EXP117 and EXP119: [-3:] identity **60/60**, Phase 0a planner-valid **10/10**, Phase-0b identity + G1 **10/10** — the EXP119 structural break (any plan block whose final outline doesn't end in `?` breaks the pinned identity) does not recur under placement A; the pre-reg's §0(6) breaking point ("tokenization effects break the channel") did NOT realize. The full run (60 planner generations + 60 plan-arm + 60 baseline-arm forwards, 0 exceptions, Δθ=0) died one layer deeper, at the readout-mass degeneracy gate: plan-arm G1 degenerate on **22/60** items (summed post-softmax mass on the two pinned entity tokens 0.000142–0.008571 < 0.01 — the distribution concentrates elsewhere at the final position) while the baseline arm never dropped below 0.068 on the same items → **n_valid = 38/60 < 48 → RUN-INVALID (elicitation-failure gate)**. Invariant under the stricter sum ≥ 0.02 reading (30 < 48); baseline reproduction **60/60** vs EXP112's archived readout; baseline variation distinct=2/minority=27 (gate passed); per Law #9 **no McNemar table and no metric was read** — no verdict smuggled. **H11's planning hypothesis is now untested across THREE distinct apparatus failure modes** on the frozen backbone (EXP117: generation channel; EXP119: tokenization identity; EXP121: plan-arm G1 mass collapse) — zero decision data, and each failure closes only its own exact composition. The caveat: the report's "a second independent full run reproduced n_valid = 38 exactly (deterministic greedy decoding)" is **unverifiable from retained artifacts** — attempt 2's 60 generation records were overwritten by the final fresh run and not retained — corrected by **erratum (LOG-4646)**; the verified claim is n_valid=38/60 recomputed independently from the retained final-run artifacts (zero field mismatches) with a deterministic re-read ×2 byte-identical. Verdict untouched. Secondary note (not a caveat): the script's `finalize()` truncated the execute script to 0 bytes before hashing — the lane reconstructed the script and the review verified it bytecode-identical to the executed .pyc; disclosed in the report, not a defect class. **Apparatus failure, not a hypothesis failure.** The one licensed upside, honestly fenced: placement A is now a candidate adaptive-loop component for the plan-text pipeline — the token-asymmetry confound stands disclosed, not removed — no planning-vs-compute attribution licensed. **The day's tally, honestly: two CONTINUEs (EXP111, EXP120 — both bound), one HELD (EXP112, bound), one apparatus CONTINUE (EXP113, bound), two KILLs (EXP107, EXP114 — both bound), EIGHT RUN-INVALIDs (EXP108, EXP109, EXP115, EXP116, EXP117, EXP118, EXP119, EXP121 — all bound), one precision certification (EXP110, bound).** **Capability scoreboard: unchanged — still zero positive signals for autonomous steering; the label-free race stays tied at zero.** No literature re-check this cycle (next due 2026-10-23). §3.1 row + §3.2 H19 paragraph added.

**v2.9 delta [FACT], 2026-09-29:** plotted **EXP124 (H21/PLAN-INSTRUMENT)** — **RUN-INVALID (apparatus-void)** (independent exact-artifact verdict review LOG-4671 — BIND, no caveat). The plan-as-instrument selection of H11's planning question — per item, a T2-P2 plan elicited and the pinned §3.4 choice rule picking variant A vs C from the final outline in position order — cleared every Phase-0 gate (tokenizer-only [-3:] **120/120** before model contact; choice-validity **10/10**; variant discriminability **4/10** with M_A=0.38102, M_C=0.46331; planner prompts byte-identical **0/60** vs the EXP113 T2-P2 reference) then collapsed in the full run: **A-FIRST=48, C-FIRST=7, choice-invalid=5** (independently reimplemented from the raw generations with **60/60 per-item agreement** and outline-count agreement 60/60; zero field mismatches) → **C-FIRST=7 < 12 → the registered choice-information gate fired** (breaking point (a): decision-inert control → RUN-INVALID). Descriptive failure mode, independently spot-verified: 60/60 full-run generation texts carry a hallucinated `Premise:` line with entities outside the bench vocabulary (38 raw / 34 distinct collapsed), and the choice rule reads the leftmost entity match inside the regurgitation — the outline texts contain no entity names, so every extracted "choice" is a function of model regurgitation, not plan content; the instrument was never a treatment. Per Law #9 **no McNemar table, no b/c/d/p — no metric was read** — no verdict smuggled; the lane halted before the 120 variant forwards (no post-contact backbone pin exists; pre-contact pin matched, Δθ=0 by construction). **Terminal reading:** H11's planning hypothesis survives its **FOURTH RUN-INVALID** (EXP117 generation, EXP119 tokenization identity, EXP121 plan-arm G1 collapse, EXP124 choice-information collapse) — untested, not killed; H21's instrument-selection channel is UNTESTED, not retired (a KILL would have retired it); **no further H11 composition is licensed without a genuinely new instrument class** (per the H21 draft §0(d)). **The day's tally, honestly: three CONTINUEs (EXP111 — bound; EXP120 — bound, qualified; EXP122 — bound), one HELD (EXP112, bound), one apparatus CONTINUE (EXP113, bound), two KILLs (EXP107, EXP114 — both bound), TEN RUN-INVALIDs (EXP108, EXP109, EXP115, EXP116, EXP117, EXP118, EXP119, EXP121, EXP123, EXP124 — all bound), one precision certification (EXP110, bound).** **Capability scoreboard: unchanged — still zero positive signals for autonomous steering; the trained-head line remains a three-bench identity-readout CONTINUE (decodability, not steering); the label-free race stays tied at zero.** No literature re-check this cycle (next due 2026-10-23). §3.1 row + §3.2 H21 paragraph added.

**v2.8 delta [FACT], 2026-09-29:** plotted **EXP123 (H20/P4APPARATUS)** — **RUN-INVALID, TERMINAL** (independent exact-artifact verdict review LOG-4662 — BIND, no caveat). The last EXP113-cleared generation protocol on the entity-name shape — P4 repetition penalty (`repetition_penalty=1.2`, `no_repeat_ngram_size=3`, greedy, `max_new_tokens=4`) on the verbatim EXP107 60-item bench — died completely: **n_parseable = 0/60, n_unparseable = 60/60, n_exceptions = 0** (independently recomputed from the raw artifacts, zero mismatches; deterministic rerun byte-identical; re-parse ×2 byte-identical; raw records persisted and hash-pinned before the verdict; LOG-331 pin before AND after, Δθ=0). The generations are real, non-degenerate model outputs (0/60 empty) — 18 distinct continuation attractors, none naming either candidate — a genuine signal, not a decode artifact: the pre-reg's breaking mechanism realized exactly (repetition penalty down-weights tokens already present in the input context, *including the entity-name tokens in the premise* — on this shape P4 is an anti-elicitation protocol, compounding EXP117's attractors and EXP113's own T2 datum P4=0/60 on outlines). This was the **expected** outcome (pre-reg predicted P(n_unparseable ≥ 7) ≈ 1) — a finding, not a failure. **Terminal reading, licensed:** the entity-name generation channel is dead on **ALL** EXP113-cleared protocols (P2 dead on this shape EXP115, P5 dead on tail echo EXP116, P4 dies here) — the honesty-instrument line closes **permanently on the entity-name shape** (no protocol rescue, no larger-n rescue, no parameter tweak); H1/H4's T1/T2 clearances untouched; EXP112's bench-2 logit line not rescued (different instrument); **label-free race stays tied at zero**. **The day's tally, honestly: three CONTINUEs (EXP111 — bound; EXP120 — bound, qualified; EXP122 — bound), one HELD (EXP112, bound), one apparatus CONTINUE (EXP113, bound), two KILLs (EXP107, EXP114 — both bound), NINE RUN-INVALIDs (EXP108, EXP109, EXP115, EXP116, EXP117, EXP118, EXP119, EXP121, EXP123 — all bound), one precision certification (EXP110, bound).** **Capability scoreboard: unchanged — still zero positive signals for autonomous steering; the trained-head line remains a three-bench identity-readout CONTINUE (decodability, not steering).** No literature re-check this cycle (next due 2026-10-23). §3.1 row + §3.2 H20 paragraph added.

**v2.7 delta [FACT], 2026-09-29:** plotted **EXP122 (H16/POSITION-CUE)** — **CONTINUE** (independent exact-artifact verdict review LOG-4654 — BIND, no caveat). The position-cue dissection EXP111/EXP120's trained-head signal needed: does the head read the target's domain-set identity, or merely its sentence position? The pinned H5 discipline ran verbatim on a third, independently constructed bench (bench 3: 60 items, fresh animal/fruit entity sets disjoint from benches 1/2, new verb families "ranks above/below" and "dominates/is dominated by", four 15-item cells) with the position scramble built into the construction — the target's final sentence position balanced 15/15 within each label class (corr = 0.0), so position carries no label information; all construction gates passed (design-time assertions; G-C1 32/60 ≤ 36/60; position-scramble gate 30/60 ≤ 36/60; G-C2 |Pearson| = 0.0322 ≤ 0.10 — no bench-1 labels or embeddings entered the analysis (Law #13); G-C3 QUESTION_SUFFIX byte-exact + deterministic rebuild; LOG-331 pin before AND after all 60 fresh CPU extractions, Δθ=0); trained L2-logistic head (C=1.0, lbfgs, seed 20260929, no tuning) → **test 27/30 = 0.9000** (per-cell 6/8, 7/7, 7/7, 7/8; acc(F)=0.8667, acc(T)=0.9333), **G = −0.0667 < 0.30** → CONTINUE (LOG-4653 execution). The review recomputed the head test from scratch (27/30, per-cell, G — all match) and independently verified the scramble from the canonical bench JSON (0/60 label mismatches, corr 0.0). **Honest placement:** the output-side readout room's positive is now a three-bench observation of the identity-readout signal with position decorrelated — the subject-position-detector alternative is excluded — but it remains **boundary-science decodability, not capability**: correlation, not steering; no decision flips moved; EXP111's and EXP120's observations restated, never re-adjudicated (Law #8); fences: no capability, no generality beyond the three benches/layer/model, no re-licensing of H1/H4 or closed families, novelty N1. H11's planning hypothesis remains untested across the three apparatus failure modes (EXP117 generation, EXP119 tokenization identity, EXP121 plan-arm G1 collapse) — zero decision data. **The day's tally, honestly: three CONTINUEs (EXP111 — bound; EXP120 — bound, qualified; EXP122 — bound), one HELD (EXP112, bound), one apparatus CONTINUE (EXP113, bound), two KILLs (EXP107, EXP114 — both bound), eight RUN-INVALIDs (EXP108, EXP109, EXP115, EXP116, EXP117, EXP118, EXP119, EXP121 — all bound), one precision certification (EXP110, bound).** **Capability scoreboard: unchanged — still zero positive signals for autonomous steering; the label-free race stays tied at zero.** No literature re-check this cycle (next due 2026-10-23). §3.1 row + §3.2 H16 paragraph added.

**v2.5 delta [FACT], 2026-09-29:** plotted **EXP120 (H15/LFH-GEN2)** —
**QUALIFIED CONTINUE** (independent exact-artifact verdict review
LOG-4634 — QUALIFY: the registered CONTINUE stands, one
documentation-precision caveat). EXP111's trained-head signal replicates
on an independently constructed, template-decorrelated second bench:
bench 2 (60 fresh items, four 15-item cells, new verb families
"surpasses"/"is below" replacing bench 1's "outranks"/"is lower than",
new river+tree entity sets, no shared template vocabulary beyond
ordinary English function words) passed every construction gate —
design-time assertions; G-C1 pure-template detector **30/60 ≤ 36/60**
(chance-level, by construction); G-C2 |Pearson| = **0.0475 ≤ 0.10** (no
bench-1 labels or embeddings entered the analysis — the Law #13 fence
was verified in the implementation, not just asserted); G-C3
QUESTION_SUFFIX byte-exact + deterministic rebuild ✓; canonical pin
`1d7d22c0…82fb2eee` — and the pinned H5 protocol ran verbatim (seed
20260929, stratified 30/30 split, ID overlap 0; LogisticRegression(l2,
C=1.0, lbfgs, max_iter=1000), no tuning, one shot): **test 25/30 =
0.8333** (per-cell 4/8, 7/7, 7/7, 7/8; acc(F)=0.7333, acc(T)=0.9333),
**G = −0.2000 < 0.30** → ≥20/30 with G<0.30 fires the registered
CONTINUE branch (LOG-4633 execution; backbone LOG-331 pin before AND
after all 60 fresh CPU extractions, Δθ=0; determinism re-fit
byte-identical). The review recomputed the head test from scratch with
numpy (25/30 ✓, per-cell ✓, G ✓). The caveat: the report's hand-written
descriptive p ("≈0.0009" for 25/30) is wrong — exact one-sided is
0.00016, two-sided 0.00032 (the error understates the evidence and cannot
have licensed the verdict, since the registered bar is count-based) —
corrected by **erratum (LOG-4635)**; verdict untouched. The unlicensed
cross-bench statistical-comparison fence was honored (each bench's
numbers stated descriptively, no test between bench 1 and bench 2), and
EXP111's bench-1 observation was restated, never re-adjudicated (Law
#8). **Record-keeping defect class recorded:** EXP120's §7 p was never
computed by the executor — the report author hand-wrote it; **future
pre-registrations must pin p-values as executor-computed.** **Honest
placement:** the output-side readout room's positive is now a two-bench
observation — a trained head extracting the subject-position cue at layer
20 on two independently constructed benches — but it remains
**boundary-science decodability, NOT capability**: correlation, not
steering; no decision flips moved; the label-free race stays tied at
zero; EXP112's HELD untouched. **The day's tally, honestly: two
CONTINUEs (EXP111, EXP120 — both bound), one HELD (EXP112, bound), one
apparatus CONTINUE (EXP113, bound), two KILLs (EXP107, EXP114 — both
bound), seven RUN-INVALIDs (EXP108, EXP109, EXP115, EXP116, EXP117,
EXP118, EXP119 — all bound), one precision certification (EXP110,
bound).** **Capability scoreboard: unchanged — still zero positive
signals for autonomous steering; the label-free race stays tied at
zero.** No literature re-check this cycle (next due 2026-10-23).

**v2.4 delta [FACT], 2026-09-29:** plotted **EXP119 (H14/PTTSC-LOGIT)** — **RUN-INVALID** (independent exact-artifact verdict review LOG-4628 — BIND, no caveat). The H11 planning question, re-asked on the proven zero-generation logit channel, died at the pre-registered Phase-0b tokenization-identity pin on the first probe item: plan tail `[444, 37741, 27]` vs baseline `[32, 37741, 27]` — the plan block's final outline ends in a word, not `?`, so the final token run differs from the baseline's fixed `? Answer:` tail. The review replicated the mechanism tokenizer-only (no model contact) and adjudicated it **structural, not item-specific**: any plan block whose final outline doesn't end in `?` breaks the pinned [-3:] identity — the pre-reg's §0(6) breaking point ("tokenization effects break the channel") realized exactly as anticipated. **Zero Phase-0b forwards ran; n_valid, correctness, and McNemar were never computed; tuple[0] never touched** (Law #7) — no verdict smuggled; the full run was never licensed. **H11's planning hypothesis is now untested on both EXP107 decision channels** (generation dead per EXP117, plan-prefix logit slot dead per EXP119). The positive apparatus note: Phase 0a scored **10/10 planner-valid** (gate did not fire) — T2-P2 transfers to the EXP107 bench as a plan elicitor (apparatus observation, not a capability claim). **Record-keeping binding lesson:** EXP119's raw Phase-0a generation texts were not persisted (counts/diagnostics only — verdict intact, record-keeping insufficient); **future execution lanes must persist raw generation records before any verdict is written.** **Apparatus failure, not a hypothesis failure.** **The day's tally, honestly: one CONTINUE (EXP111, bound), one HELD (EXP112, bound), one apparatus CONTINUE (EXP113, bound), two KILLs (EXP107, EXP114 — both bound), SEVEN RUN-INVALIDs (EXP108, EXP109, EXP115, EXP116, EXP117, EXP118, EXP119 — all bound), one precision certification (EXP110, bound).** **Capability scoreboard: unchanged — still zero positive signals for autonomous steering; the label-free race stays tied at zero.** No literature re-check this cycle (next due 2026-10-23).

**v2.3 delta [FACT], 2026-09-29:** plotted **EXP118 (H13/HDI-LOC)** — **RUN-INVALID** (independent exact-artifact verdict review LOG-4620 — QUALIFY: the verdict stands on the exact artifacts, one binding caveat recorded as erratum LOG-4621). The layer-locality question (where does EXP112's 41/60 HELD fidelity live, via the zero-training logit lens across 18 layer sites) never reached its metric: the pre-registered run-validity rule fired on the early window — **0/9 non-degenerate sites** (required ≥5) — the logit lens cannot speak at early layers on this bench. Entity-name tokens acquire unembedding mass only in the final ~5 layers (early max mass 0.000022, ~450× below the 0.01 threshold). Per Law #9 **no per-site fidelity and no contrast C was read** — no verdict smuggled; EXP112's HELD stands unchanged. The consistency pin PASSED (lens@L24 byte-identical 60/60 to EXP112's archived column, 41/60 exactly), and the pin proved its worth: the executor's first attempt double-normalized at L24 (5/60 argmax flips) and the pin HALTed it — the corrected lens is what the registered protocol accepted. **Apparatus failure, not a hypothesis failure.** The caveat: the report's §10/§11 falsely claimed `exp118_worksheet.json` was written (the script writes artifacts only after the validity-rule exit; filesystem-wide find: no such file) — corrected by erratum (LOG-4621); verdict untouched. **The day's tally, honestly: one CONTINUE (EXP111, bound), one HELD (EXP112, bound), one apparatus CONTINUE (EXP113, bound), two KILLs (EXP107, EXP114 — both bound), six RUN-INVALIDs (EXP108, EXP109, EXP115, EXP116, EXP117, EXP118 — all bound), one precision certification (EXP110, bound).** **Capability scoreboard: unchanged — still zero positive signals for autonomous steering; the label-free race stays tied at zero.** No literature re-check this cycle (next due 2026-10-23).

**v2.2 delta [FACT], 2026-09-29:** plotted **EXP117 (H11/PTTSC-GEN)** —
**RUN-INVALID** (independent exact-artifact verdict review LOG-4610 —
BIND, no caveat). The EXP113-licensed planner/executor revival hypothesis
(a NEW apparatus on the T2 numbered-outline shape — not a re-run of
EXP109) never reached the planning question: Phase 0b's decision-channel
mini-gate fired with **0/10 parseable** — the model enumerates entities as
a list (`'\n\n1. Jupiter\n\n2. Mars\n\n3. Venus\n'`) instead of naming
one — the **4th consecutive entity-name-generation-slot failure** on this
shape (EXP109 80/80 sampled; EXP115 38/60 recitation; EXP116 37/60 tail
echo; EXP117 0/10 enumeration). Phase 0a's literal recitation gate did NOT
fire (0/10) while the content-level diagnostic scored 10/10: the review
adjudicated a **REAL protocol defect** — the §3.7 literal recitation
definition is structurally inert for content recitation
(marker-stripped extraction vs marker-prefixed exemplar lines) — but it
did NOT change the verdict (the gate was applied as written; Phase 0b
fired independently; the RUN-INVALID is overdetermined), and it is recorded
as a binding apparatus-definition lesson: **no future protocol may reuse
the §3.7 definition.** Planner prompts byte-verified 0/60 mismatches
against the signed `exp113_run.py` T2-P2 construction (the raw JSON stores
no prompts — disclosed honestly); backbone LOG-331 pin matched pre-run,
Δθ=0. **Apparatus failure, not a hypothesis failure — no verdict smuggled;
the generation channel for entity-name answers is dead on base Pythia-410m
across four apparatuses.** **The day's tally, honestly: one CONTINUE
(EXP111, bound), one HELD (EXP112, bound), one apparatus CONTINUE (EXP113,
bound), two KILLs (EXP107, EXP114 — both bound), five RUN-INVALIDs (EXP108,
EXP109, EXP115, EXP116, EXP117 — all bound), one precision certification
(EXP110, bound).** **Capability scoreboard: unchanged — still zero positive
signals for autonomous steering; the label-free race stays tied at zero.**
No literature re-check this cycle (next due 2026-10-23).

**v2.1 delta [FACT], 2026-09-29:** plotted **EXP115 (H9/HDI-GEN)** and
**EXP116 (H10/HDI-PRIM)** — both **RUN-INVALID** (independent exact-artifact
verdict reviews LOG-4599 and LOG-4603 — both BIND, no caveat). The two
EXP113-licensed honesty-instrument revival hypotheses died at the apparatus
layer on the same bench via two DIFFERENT failures, each independently
confirmed from the raw generations: EXP115 (few-shot P2 elicitation):
n_unparseable = **38/60** ≥ 7 → G1 fired; failure mode few-shot recitation
(last exemplar block regurgitated; all 60 generations contain `Premise:`).
EXP116 (priming P5 elicitation, zero exemplar blocks — recitation
structurally blocked): n_unparseable = **37/60** ≥ 7 → G1 fired; new failure
mode tail echo (27 of 37 unparseable echo the unfinished priming sentence
verbatim; 0/60 contain `Premise:` — recitation confirmed absent). Both
failures inside the pre-regs' disclosed risk envelopes; both gates fired
before any metric was read (fidelity null, not wrong); all archive pins and
the LOG-331 backbone pin (Δθ=0) independently re-verified. **Apparatus
failures, not hypothesis failures — but the consequence is final for this
line:** the generation-level honesty instrument has no EXP113-cleared
protocol left on the entity-name shape (P2 dead, EXP115; P5 dead, EXP116).
H6's logit-level HELD (41/60) stands alone as the only honesty signal.
**The day's tally, honestly: one CONTINUE (EXP111, bound), one HELD (EXP112,
bound), one apparatus CONTINUE (EXP113, bound), two KILLs (EXP107, EXP114 —
both bound), four RUN-INVALIDs (EXP108, EXP109, EXP115, EXP116 — all bound),
one precision certification (EXP110, bound).** **Capability scoreboard:
unchanged — still zero positive signals for autonomous steering; the
label-free race stays tied at zero.** No literature re-check this cycle
(next due 2026-10-23).

**v2.0 delta [FACT], 2026-09-29:** plotted **EXP114 (H8/POE)** —
**KILL** (independent exact-artifact verdict review LOG-4592 — BIND, no
caveat). The round-2 wave's first clean negative: positional-order
ensembling of frozen-backbone position logits over K=5 randomized
presentation orders vs the canonical single-order baseline on the EXP107
template-decorrelated bench (360/360 forward passes, zero generation;
order patterns independently replicated from random.Random(20260929),
0/60 mismatches; all three archive hashes and the LOG-331 backbone pin
matched before AND after, Δθ=0): **acc_ensemble 38/60 = 0.6333 vs
acc_baseline 41/60 = 0.6833; net (b−c) = −3 (b=2, c=5, n=7); one-sided
exact McNemar p = 0.9375** — the ensemble scored 5pp BELOW the baseline,
firing the registered net ≤ 0 → KILL branch with no post-hoc
re-interpretation. **Fences honored:** retires only the
positional-order-ensembling axis for this task class — test-time scaling
in general and the adaptive-loop program are explicitly NOT retired; no
reasoning, consciousness, or capability consequence; the below-baseline
reading is a labeled [OBSERVATION], no softening. **The day's tally,
honestly: one CONTINUE (EXP111, bound), one HELD (EXP112, bound), one
apparatus CONTINUE (EXP113, bound), two KILLs (EXP107, EXP114 — both
bound), two RUN-INVALIDs (EXP108, EXP109), one precision certification
(EXP110, bound).** This is a clean kill of a test-time-scaling variant —
failures first. **Capability scoreboard: unchanged — still zero positive
signals for autonomous steering; the label-free race stays tied at
zero.** No literature re-check this cycle (next due 2026-10-23).

**v1.9 delta [FACT], 2026-09-29:** plotted **EXP113 (H7/EVALID)** —
**CONTINUE** (independent exact-artifact verdict review LOG-4585 —
BIND, no caveat). The bounded apparatus question that gates honest
H1/H4 revival: 5 pinned elicitation protocols × 2 task shapes (T1
single-token answer = H1 self-report shape; T2 numbered outlines = H4
planner shape) × 60 items = 600 greedy generations on frozen base
Pythia-410m, every output parsed by the registered mechanical scripts
(deterministic re-parse byte-identical; 0 exceptions; 2 empties scored
UNPARSEABLE; no RUN-INVALID fired; backbone LOG-331 pin matched before
AND after, Δθ=0). **Counts:** T1 — P1=0 (the EXP108 echo path
reproduced), P2=60, P3=0, P4=58, P5=60; T2 — P1=24, P2=60, P3=0, P4=0
(repetition penalty derails the outline task), P5=60. Clearance bar
≥48/60 → T1-CLEAR={P2,P4,P5}, T2-CLEAR={P2,P5}, both non-empty →
**CONTINUE**. Few-shot (P2) and priming (P5) are the only protocols
clearing both shapes. **Consequence, fenced:** H1/H4 revival is
licensable as NEW hypotheses with the named clearing protocols (each
carrying its own elicitation-failure gate) — H1/H4 themselves are NOT
revived. First launch died at 180/600 on a VM reboot (no metric read;
full re-run from scratch; crash log preserved). **The day's tally,
honestly: one CONTINUE (EXP111, bound), one HELD (EXP112, bound), one
KILL (EXP107), two RUN-INVALIDs (EXP108, EXP109), one precision
certification (EXP110, bound), one apparatus CONTINUE (EXP113, bound).**
This is a methodological/apparatus entry — the generation axis is open
for this backbone under pinned protocols, a real methodological gain —
**not a capability signal.** **Capability scoreboard: unchanged —
still zero positive signals for autonomous steering; the label-free
race stays tied at zero.** No literature re-check this cycle (next due
2026-10-23).
- v2.9 — 2026-09-29 (scoreboard-sync lane, LOG-4672): plotted **EXP124
  (H21/PLAN-INSTRUMENT)** — **RUN-INVALID (apparatus-void)** (independent
  exact-artifact verdict review LOG-4671 — BIND, no caveat). Plan-as-instrument
  selection on H11's planning question: every Phase-0 gate passed (tokenizer-only
  [-3:] 120/120; choice-validity 10/10; variant discriminability 4/10,
  M_A=0.38102, M_C=0.46331; planner prompts byte-identical 0/60 vs the EXP113
  T2-P2 reference), then the full-run choice collapsed —
  **A-FIRST=48, C-FIRST=7, choice-invalid=5** (independent reimplementation
  60/60 per-item agreement, outline-count agreement 60/60) →
  **C-FIRST=7 < 12 → the registered choice-information gate fired**
  (decision-inert control). Descriptive failure mode: 60/60 full-run generation
  texts carry a hallucinated `Premise:` line with entities outside the bench
  vocabulary; the choice rule reads the leftmost entity match inside the
  regurgitation — the outline texts contain no entity names, so every extracted
  "choice" is model regurgitation, not plan content; the instrument was never a
  treatment. Per Law #9 no McNemar table, no b/c/d/p — no metric was read; the
  lane halted before the 120 variant forwards (pre-contact LOG-331 pin matched,
  Δθ=0 by construction). **Terminal reading:** H11's planning hypothesis survives
  its **fourth RUN-INVALID** (EXP117, 119, 121, 124) — untested, not killed; H21's
  instrument-selection channel is UNTESTED, not retired (a KILL would have retired
  it); **no further H11 composition licensed without a genuinely new instrument
  class** (H21 draft §0(d)); new binding lesson recorded (defect class 8 —
  choice-extraction on the final outline must assert the final outline is plan
  content, not regurgitation). §3.1 row + §3.2 H21 paragraph added. The day's
  tally: three CONTINUEs (EXP111, EXP120 — qualified, EXP122), one HELD
  (EXP112), one apparatus CONTINUE (EXP113), two KILLs (EXP107, EXP114),
  **TEN RUN-INVALIDs (EXP108, EXP109, EXP115, EXP116, EXP117, EXP118, EXP119,
  EXP121, EXP123, EXP124)**, one precision certification (EXP110). Capability
  scoreboard: unchanged — zero positive signals for autonomous steering; the
  trained-head line remains a three-bench identity-readout CONTINUE
  (decodability, not steering); the label-free race stays tied at zero.
- v2.8 — 2026-09-29 (scoreboard-sync lane, LOG-4663): plotted **EXP123
  (H20/P4APPARATUS)** — **RUN-INVALID, TERMINAL** (independent exact-artifact
  verdict review LOG-4662 — BIND, no caveat). P4 repetition-penalty decoding
  (`repetition_penalty=1.2`, `no_repeat_ngram_size=3`, greedy,
  `max_new_tokens=4`) on the verbatim EXP107 60-item bench:
  **n_parseable = 0/60, n_unparseable = 60/60, n_exceptions = 0**
  (independently recomputed from the raw artifacts, zero mismatches;
  deterministic rerun + re-parse ×2 byte-identical; raw records hash-pinned
  before the verdict; LOG-331 pin before AND after, Δθ=0). The generations
  are real, non-degenerate model outputs — 18 distinct continuation
  attractors, none naming either candidate — a genuine signal, not a decode
  artifact: the pre-reg's breaking mechanism realized (repetition penalty
  down-weights input-context tokens *including the entity-name tokens in
  the premise*, biasing against emitting the entity name — an
  anti-elicitation protocol on this shape; compounds EXP113's own T2 datum
  P4=0/60 on outlines). The expected outcome (pre-reg predicted
  P(n_unparseable ≥ 7) ≈ 1) — a finding, not a failure. **Terminal reading:**
  the entity-name generation channel is dead on **all** EXP113-cleared
  protocols (P2 EXP115, P5 EXP116, P4 here) — the honesty-instrument line
  closes **permanently on the entity-name shape** (no protocol rescue, no
  larger-n rescue, no parameter tweak); H1/H4's T1/T2 clearances untouched;
  EXP112's bench-2 logit line not rescued (different instrument); label-free
  race stays tied at zero. §3.1 row + §3.2 H20 paragraph added. The day's
  tally: three CONTINUEs (EXP111, EXP120 — qualified, EXP122), one HELD
  (EXP112), one apparatus CONTINUE (EXP113), two KILLs (EXP107, EXP114),
  **NINE RUN-INVALIDs (EXP108, EXP109, EXP115, EXP116, EXP117, EXP118,
  EXP119, EXP121, EXP123)**, one precision certification (EXP110).
  **Capability scoreboard: unchanged — still zero positive signals for
  autonomous steering; the trained-head line remains a three-bench
  identity-readout CONTINUE (decodability, not steering).** No literature
  re-check this cycle (next due 2026-10-23).
- v2.7 — 2026-09-29 (scoreboard-sync lane, LOG-4655): plotted **EXP122
  (H16/POSITION-CUE)** — **CONTINUE** (independent exact-artifact verdict
  review LOG-4654 — BIND, no caveat). The position-cue dissection EXP111/EXP120's
  trained-head signal needed: does the head read the target's domain-set
  identity, or merely its sentence position? The pinned H5 discipline ran
  verbatim on a third, independently constructed bench (bench 3: 60 items,
  fresh animal/fruit entity sets disjoint from benches 1/2, new verb families
  "ranks above/below" and "dominates/is dominated by", four 15-item cells) with
  the position scramble built into the construction — the target's final
  sentence position balanced 15/15 within each label class (corr = 0.0), so
  position carries no label information. All construction gates passed (G-C1
  32/60 ≤ 36/60; position-scramble gate 30/60 ≤ 36/60; G-C2 |Pearson| = 0.0322 ≤
  0.10 — Law #13 fence honored; G-C3 QUESTION_SUFFIX byte-exact; LOG-331 pin
  before AND after all 60 fresh CPU extractions, Δθ=0); trained L2-logistic
  head (C=1.0, lbfgs, seed 20260929, no tuning) → **test 27/30 = 0.9000**
  (per-cell 6/8, 7/7, 7/7, 7/8; acc(F)=0.8667, acc(T)=0.9333),
  **G = −0.0667 < 0.30** → CONTINUE (LOG-4653 execution). Exact one-sided p =
  4.215e-06, executor-computed (defect class (a) honored). The review
  recomputed the head test from scratch and independently verified the scramble
  from the canonical bench JSON (0/60 label mismatches). **Honest placement:**
  the output-side readout room's positive is now a three-bench observation of
  the identity-readout signal with position decorrelated — the
  subject-position-detector alternative is excluded — but it remains
  **boundary-science decodability, not capability**: correlation, not steering;
  no decision flips moved; EXP111's and EXP120's observations restated, never
  re-adjudicated (Law #8); fences hold (no capability, no generality beyond the
  three benches/layer/model, no re-licensing of H1/H4 or closed families);
  novelty N1. H11's planning hypothesis remains untested across the three
  apparatus failure modes (EXP117 generation, EXP119 tokenization identity,
  EXP121 plan-arm G1 collapse) — zero decision data. §3.1 row + §3.2 H16
  paragraph added. **The day's tally, honestly: three CONTINUEs (EXP111 —
  bound; EXP120 — bound, qualified; EXP122 — bound), one HELD (EXP112, bound),
  one apparatus CONTINUE (EXP113, bound), two KILLs (EXP107, EXP114 — both
  bound), eight RUN-INVALIDs (EXP108, EXP109, EXP115, EXP116, EXP117, EXP118,
  EXP119, EXP121 — all bound), one precision certification (EXP110, bound).**
  **Capability scoreboard: unchanged — still zero positive signals for
  autonomous steering; the label-free race stays tied at zero.** No literature
  re-check this cycle (next due 2026-10-23).
- v2.6 — 2026-09-29 (scoreboard-sync lane, LOG-4647): plotted **EXP121
  (H19/PTTSC-SUFFIX)** — **RUN-INVALID** (independent exact-artifact verdict
  review LOG-4645 — QUALIFY: the verdict stands on the exact artifacts, one
  documentation caveat). The planning question, re-asked on the logit channel
  through the tail-preserving composition (plan text between the premise and
  the fixed question tail — placement A), cleared every gate that killed
  EXP117/EXP119 (tokenizer [-3:] identity 60/60; planner-valid 10/10;
  logit-slot 10/10) but died at the readout-mass gate: plan-arm G1 degenerate
  on 22/60 items (summed mass 0.000142–0.008571 < 0.01) →
  **n_valid = 38/60 < 48 → RUN-INVALID (elicitation-failure gate)**. Invariant
  under the stricter sum ≥ 0.02 reading (30 < 48); baseline reproduction
  60/60; no McNemar read per Law #9. The caveat: the report's "second
  independent full run reproduced n_valid = 38" is unverifiable from retained
  artifacts — corrected by erratum (LOG-4646); the verified claim is
  n_valid=38/60 recomputed independently from final-run artifacts,
  deterministic re-read ×2 byte-identical. H11's planning hypothesis now
  untested across **three** distinct apparatus failure modes (EXP117
  generation, EXP119 tokenization identity, EXP121 plan-arm G1 collapse) —
  zero decision data. Licensed upside: placement A is a candidate
  adaptive-loop component for the plan-text pipeline (token-asymmetry
  confound disclosed, not removed). §3.1 row + §3.2 H19 paragraph added.
  **The day's tally, honestly: two CONTINUEs (EXP111, EXP120 — both bound),
  one HELD (EXP112, bound), one apparatus CONTINUE (EXP113, bound), two
  KILLs (EXP107, EXP114 — both bound), eight RUN-INVALIDs (EXP108, EXP109,
  EXP115, EXP116, EXP117, EXP118, EXP119, EXP121 — all bound), one precision
  certification (EXP110, bound).** **Capability scoreboard: unchanged —
  still zero positive signals for autonomous steering; the label-free race
  stays tied at zero.** No literature re-check this cycle (next due
  2026-10-23).
- v2.5 — 2026-09-29 (scoreboard-sync lane, LOG-4636): plotted **EXP120
  (H15/LFH-GEN2)** — **QUALIFIED CONTINUE** (independent exact-artifact verdict
  review LOG-4634 — QUALIFY: the registered CONTINUE stands, one
  documentation-precision caveat). EXP111's trained-head signal replicates
  on a second independently constructed template-decorrelated bench: all
  construction gates pass (design-time assertions; G-C1 pure-template
  detector 30/60 ≤ 36/60; G-C2 |Pearson| = 0.0475 ≤ 0.10 — no bench-1
  labels or embeddings entered the analysis (Law #13, verified in the
  implementation); G-C3 decomposition byte-exact; backbone LOG-331 before
  AND after all 60 extractions, Δθ=0); the pinned H5 protocol ran verbatim
  (seed 20260929, stratified 30/30 split, ID overlap 0;
  LogisticRegression(l2, C=1.0, lbfgs, max_iter=1000), no tuning, one shot)
  → **test 25/30 = 0.8333** (per-cell 4/8, 7/7, 7/7, 7/8),
  **G = −0.2000 < 0.30** → CONTINUE (LOG-4633 execution). The review
  recomputed the head test from scratch with numpy (25/30, per-cell, G —
  all match). The caveat: the report's hand-written descriptive p
  ("≈0.0009" for 25/30) is wrong — exact one-sided 0.00016, two-sided
  0.00032 (conservative error, verdict-unaffected) — corrected by erratum
  (LOG-4635). The output-side readout room's positive is now a two-bench
  observation (layer-20 subject-position cue); **boundary-science
  decodability, NOT capability** — correlation, not steering; no decision
  flips moved; the label-free race stays tied at zero; EXP112's HELD
  untouched. Cross-bench statistical comparison fence honored (no test
  between bench 1 and bench 2); EXP111's bench-1 observation restated,
  never re-adjudicated (Law #8). New defect class recorded: **report
  authors hand-writing p-values instead of executor-computed values** —
  future pre-registrations must pin p-values as executor-computed. §0
  static-steering row + §3.1 row + §3.2 H15 paragraph added. **The day's
  tally, honestly: two CONTINUEs (EXP111, EXP120 — both bound), one HELD
  (EXP112, bound), one apparatus CONTINUE (EXP113, bound), two KILLs
  (EXP107, EXP114 — both bound), seven RUN-INVALIDs (EXP108, EXP109,
  EXP115, EXP116, EXP117, EXP118, EXP119 — all bound), one precision
  certification (EXP110, bound).** **Capability scoreboard: unchanged —
  still zero positive signals for autonomous steering; the label-free race
  stays tied at zero.** No literature re-check this cycle (next due
  2026-10-23).
- v2.4 — 2026-09-29 (scoreboard-sync lane, LOG-4629): plotted **EXP119
  (H14/PTTSC-LOGIT)** — **RUN-INVALID** (independent exact-artifact verdict
  review LOG-4628 — BIND, no caveat). The H11 planning question re-asked on
  the zero-generation logit channel died at the pre-registered Phase-0b
  tokenization-identity pin: plan tail `[444, 37741, 27]` vs baseline
  `[32, 37741, 27]` on item 0 — structural (any plan block whose final
  outline doesn't end in `?` breaks the pinned [-3:] identity), the §0(6)
  breaking point ("tokenization effects break the channel") realized exactly
  as anticipated; zero Phase-0b forwards ran, no metric read, tuple[0] never
  touched. H11's planning hypothesis is now untested on both EXP107 decision
  channels (generation dead per EXP117, plan-prefix logit slot dead per
  EXP119). Phase 0a 10/10 planner-valid: T2-P2 transfers to EXP107 as a plan
  elicitor (apparatus observation, not a capability claim). Binding
  record-keeping lesson: future execution lanes must persist raw generation
  records before any verdict is written (EXP119's Phase-0a texts were not
  persisted; verdict intact). **Apparatus failure, not a hypothesis failure.**
  The day's tally: one CONTINUE (EXP111), one HELD (EXP112), one apparatus
  CONTINUE (EXP113), two KILLs (EXP107, EXP114), **seven RUN-INVALIDs
  (EXP108, EXP109, EXP115, EXP116, EXP117, EXP118, EXP119)**, one precision
  certification (EXP110). **Capability scoreboard: unchanged — still zero
  positive signals for autonomous steering; the label-free race stays tied
  at zero.** No literature re-check this cycle (next due 2026-10-23).
- v2.3 — 2026-09-29 (scoreboard-sync lane, LOG-4622): plotted **EXP118
  (H13/HDI-LOC)** — **RUN-INVALID** (independent exact-artifact verdict
  review LOG-4620 — QUALIFY: the verdict stands, one binding caveat recorded
  as erratum LOG-4621). The logit lens cannot speak at early layers on this
  bench: early window (L0–L8) **0/9 non-degenerate** (required ≥5) — entity-name
  tokens acquire unembedding mass only in the final ~5 layers. Per Law #9 no
  per-site fidelity and no contrast C was read — no verdict smuggled;
  EXP112's HELD stands unchanged. The consistency pin PASSED (lens@L24
  byte-identical 60/60, 41/60 exactly) and arbitrated the double-normalization
  fix on the executor's first attempt (5/60 argmax flips HALTed). The
  report's false `exp118_worksheet.json` claims were corrected by erratum
  (LOG-4621); verdict untouched. **Apparatus failure, not a hypothesis
  failure.** The day's tally: one CONTINUE (EXP111), one HELD (EXP112), one
  apparatus CONTINUE (EXP113), two KILLs (EXP107, EXP114), **six RUN-INVALIDs
  (EXP108, EXP109, EXP115, EXP116, EXP117, EXP118)**, one precision
  certification (EXP110). **Capability scoreboard: unchanged — still zero
  positive signals for autonomous steering; the label-free race stays tied
  at zero.** No literature re-check this cycle (next due 2026-10-23).
- v2.2 — 2026-09-29 (scoreboard-sync lane, LOG-4611): plotted **EXP117
  (H11/PTTSC-GEN)** — **RUN-INVALID** (independent exact-artifact verdict
  review LOG-4610 — BIND, no caveat). The EXP113-licensed planner/executor
  revival hypothesis (a NEW apparatus on the T2 numbered-outline shape,
  not a re-run of EXP109) never reached the planning question: Phase 0b's
  decision-channel mini-gate fired with **0/10 parseable** — the model
  enumerates entities as a list (`'\n\n1. Jupiter\n\n2. Mars\n\n3. Venus\n'`)
  instead of naming one — the **4th consecutive entity-name-generation-slot
  failure** on this shape (EXP109 80/80 sampled; EXP115 38/60 recitation;
  EXP116 37/60 tail echo; EXP117 0/10 enumeration). Phase 0a's literal
  recitation gate did NOT fire (0/10) while the content diagnostic scored
  10/10: the review adjudicated the **§3.7 protocol-defect discovery REAL
  but non-decisive** (marker-stripped extraction vs marker-prefixed
  exemplar lines — structurally inert for content recitation) — the gate
  was applied as written (Law #4), Phase 0b fired independently, and the
  RUN-INVALID is overdetermined. Binding lesson recorded: **no future
  protocol may reuse the §3.7 definition.** Planner prompts byte-verified
  0/60 mismatches against the signed `exp113_run.py` T2-P2 construction
  (raw JSON stores no prompts — disclosed); backbone LOG-331 pin matched
  pre-run, Δθ=0. **Apparatus failure, not a hypothesis failure — no verdict
  smuggled; no rescue licensed.** The day's tally: one CONTINUE (EXP111),
  one HELD (EXP112), one apparatus CONTINUE (EXP113), two KILLs (EXP107,
  EXP114), five RUN-INVALIDs (EXP108, EXP109, EXP115, EXP116, EXP117), one
  precision certification (EXP110). **Capability scoreboard: unchanged —
  still zero positive signals for autonomous steering; the label-free race
  stays tied at zero.** No literature re-check this cycle (next due
  2026-10-23).
- v2.1 — 2026-09-29 (scoreboard-sync lane, LOG-4604): plotted **EXP115
  (H9/HDI-GEN)** and **EXP116 (H10/HDI-PRIM)** — both **RUN-INVALID**
  (independent exact-artifact verdict reviews LOG-4599/4603, both BIND, no
  caveat). Two DIFFERENT apparatus failures on the same bench: P2 few-shot
  elicitation died on recitation (n_unparseable = 38/60 ≥ 7; all 60
  generations contain `Premise:`, the last exemplar block regurgitated
  verbatim); P5 priming elicitation — zero exemplar blocks, recitation
  structurally blocked — died on tail echo (n_unparseable = 37/60 ≥ 7; 27
  of 37 unparseable echo the unfinished priming sentence verbatim; 0/60
  contain `Premise:`). Both failures inside the pre-regs' disclosed risk
  envelopes; both gates fired before any metric was read (fidelity null,
  not wrong); all archive pins and the LOG-331 backbone pin (Δθ=0)
  independently re-verified. **Apparatus failures, not hypothesis failures
  — but the consequence is final for this line:** the generation-level
  honesty instrument has no EXP113-cleared protocol left on the entity-name
  shape; H6's logit-level HELD (41/60) stands alone as the only honesty
  signal. The day's tally: one CONTINUE (EXP111), one HELD (EXP112), one
  apparatus CONTINUE (EXP113), two KILLs (EXP107, EXP114), four
  RUN-INVALIDs (EXP108, EXP109, EXP115, EXP116), one precision certification
  (EXP110). **Capability scoreboard: unchanged — still zero positive
  signals for autonomous steering; the label-free race stays tied at zero.**
  No literature re-check this cycle (next due 2026-10-23).
- v2.0 — 2026-09-29 (scoreboard-sync lane, LOG-4593): plotted **EXP114
  (H8/POE) KILL** — K=5 positional-order ensemble 38/60 vs canonical
  single-order baseline 41/60 (net −3, one-sided McNemar p=0.9375;
  independent verdict review LOG-4592 BIND, no caveat); retires only the
  positional-order-ensembling axis for this task class (test-time scaling
  in general and the adaptive-loop program NOT retired); below-baseline
  reading a labeled [OBSERVATION]. The day's tally: one CONTINUE, one
  HELD, one apparatus CONTINUE, two KILLs, two RUN-INVALIDs, one
  precision certification. **Capability scoreboard: unchanged — zero
  positive signals for autonomous steering.** No literature re-check this
  cycle (next due 2026-10-23).
- v1.9 — 2026-09-29 (scoreboard-sync lane, LOG-4586): plotted **EXP113
  (H7/EVALID) CONTINUE** — 5 pinned protocols × 2 task shapes × 60
  items = 600 greedy generations; T1-CLEAR={P2,P4,P5}, T2-CLEAR={P2,P5}
  (clearance ≥48/60) → CONTINUE (independent verdict review LOG-4585
  BIND, no caveat); few-shot and priming clear both shapes → H1/H4
  revival licensable as NEW hypotheses with the named protocols (not
  revived); **apparatus/methodological entry, NOT capability** (parseable
  output ≠ reasoning, honesty, or capability). The day's tally: one
  CONTINUE, one HELD, one KILL, two RUN-INVALIDs, one precision
  certification, one apparatus CONTINUE. **Capability scoreboard:
  unchanged — zero positive signals for autonomous steering.** No
  literature re-check this cycle (next due 2026-10-23).
- v1.8 — 2026-09-29 (scoreboard-sync lane, LOG-4577): plotted **EXP112
  (H6/HDI-LR) HELD** — fidelity 41/60 = 0.6833 inside the registered
  34–41/60 band (independent verdict review LOG-4576 BIND); Law
  #14-grade degeneracy guards passed before any metric read; **licenses
  nothing, retires nothing**; the day's tally: one CONTINUE, one HELD,
  one KILL, two RUN-INVALIDs, one precision certification.
  **Capability scoreboard: unchanged — zero positive signals for
  autonomous steering.** No literature re-check this cycle (next due
  2026-10-23).
- v1.7 — 2026-09-29 (scoreboard-sync lane, LOG-4570): plotted **EXP111
  (H5/LFH-TD) CONTINUE** — trained L2-logistic head 24/30 = 0.8000,
  G = 0.0000 on the EXP107 template-decorrelated bench (the same kill-test
  discipline that executed EXP106); one-sided p = 0.00072 (independent
  verdict review LOG-4569 QUALIFIED — required footnote: the report's
  0.0014 is the two-sided value, descriptive-only). First output-side
  result to survive adversarial testing; GPU head-training proposal
  re-licensed under decorrelated-bench discipline (founder-hardware-gated).
  Boundary-science decodability entry, NOT capability: one layer-20
  correlation on one n=30 bench; fences hold (no generality, no
  consciousness, no capability until downstream causal tests). §0
  static-steering row + §3.1 rows + §3.2 position paragraph updated.
  **Capability scoreboard: unchanged — zero positive signals for autonomous
  steering; the label-free race stays tied at zero.** No literature
  re-check this cycle (next due 2026-10-23).
- v1.6 — 2026-09-29 (scoreboard-sync lane, LOG-4560): plotted the
  summit-sprint H-wave — EXP106→EXP107 (H3: 60/60 disjoint-bench transfer
  reading KILLED as a template artifact, 34/60 p=0.1831; GPU
  head-training proposal void; output-side trained-head room retired as
  artifact-only), EXP108 (H1: RUN-INVALID — 60/60 self-reports
  unparseable; apparatus finding, H1 neither killed nor continued;
  required footnote: no per-item generation records retained —
  evidence is a single log-summary line), EXP109 (H4: RUN-INVALID —
  planner repetition attractor, n_valid=0/20; axis NOT retired,
  pilot-scope fenced), EXP110 (H2: CERTIFIED-WITH-NOTE — 6/7 tiers,
  structural intact; T6 O 0.5714→0.5000 as a bounded precision effect;
  EXP105's KILL-at-step-9 precision-certified under weight-only INT8
  fake-quantization; I2′ KILL stands; simulation-scoped, not true
  INT8 hardware). Independent exact-artifact verdict review LOG-4559
  folded in (EXP107/109/110 BIND; EXP108 QUALIFIED with the required
  footnote). §0 delta + static-steering row + §3.1 rows + §3.2
  position paragraph updated. **Capability scoreboard: unchanged —
  zero positive signals for autonomous steering; the label-free race
  stays tied at zero.** Durable gains are methodological: generation
  experiments must validate instruction-following before measuring
  (base Pythia-410m cannot follow generation instructions); the
  Decodability Gap boundary now carries a bounded precision-
  certification. No literature re-check this cycle (next due
  2026-10-23).

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
