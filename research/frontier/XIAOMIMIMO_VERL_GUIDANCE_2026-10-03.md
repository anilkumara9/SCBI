# Guidance brief: XiaomiMiMo/verl — what big-company RL engineering teaches a Δθ=0 program

Date: 2026-10-03. Author: study lane (analysis only, no experiments).
Source: shallow clone of https://github.com/XiaomiMiMo/verl @ a2ad9f6 (2026-10-03),
plus Section 7 of the MiMo-V2.6 technical report (PDF, created 2026-09-22, fetched from
https://huggingface.co/XiaomiMiMo/MiMo-V2.6-Pro-RL).

Bottom line: verl is a weight-update training framework, so its RL algorithms transfer
nothing to a frozen-backbone program. What DOES transfer is the engineering discipline
around verifiers, failure taxonomy, and token-exactness — Xiaomi's team learned these
from measured failures, and every one of them is documented in the repo with the failure
that motivated it. That documentation culture is itself the biggest lesson.

Evidence labels: benchmark numbers below are Xiaomi's self-reports (public-benchmark
rows are independently checkable; internal "mini" benches are vendor-reported). Code
observations are from direct reads. Claims I could not verify are marked [UNVERIFIED].

---

## 1. The five RL environments and their verifiers — what transfers to judge-free evaluation

Xiaomi's fork adds five RL environments on verl 0.9.0.dev, each pairing a task family
with a verifier that needs no trained judge:

| Domain | Task family | Verifier | Scale (train tasks) |
|---|---|---|---|
| Code | Software engineering | Executable tests | ~3k |
| Cyber (arvo) | Vulnerability reproduction | Rule checks | ~1k |
| General | Knowledge work (s3k enterprise tasks) | Rubric-based judging | ~1k |
| Visual | Web development | Visual grading (screenshots + judge) | ~2k |
| Music | Symbolic music composition (ABC notation) | Rule checks (MIDI feature scoring) | ~1k |

Scale column source: Table 5 of the MiMo-V2.6 report (Code ~3k, Cyber ~1k, General ~1k,
Visual ~2k; music ~1k from the §7.2 body text).

Transferable verifier-design patterns (all observed in code):

1. **Two-gate scoring (music arm, `recipes/design/music/scorer/`).** Gate 1 extracts the
   artifact (ABC notation fenced block → `abc2midi` → MIDI bytes); gate 2 scores MIDI
   features (acoustic, tonal, rhythmic, structural) against a reference baseline
   (`baselines/ref_full4k.json`). Lesson: separate *extraction validity* from *quality
   scoring*. A malformed artifact fails gate 1; a valid-but-bad artifact fails gate 2.
   SCBI's EXP142 was voided by a measurement-validity defect of exactly the gate-1 kind
   (length guard); a two-gate structure would have made the void explicit at design time.

2. **Rubric items with typed metadata (general arm).** Each task bundle ships
   `rubrics.json` + `verifier_meta.json` (the `VERIFIER_FILES` manifest in
   `recipes/general/general_agent/environment.py`); every rubric item carries
   method (rule/llm), weight, gate (boolean), and dim. `verify.py`, driven inside
   the pod by `general_agent/environment.py`, runs the checks;
   `_annotate_rubric_kinds` (also in
   `recipes/general/general_agent/environment.py`)
   joins results back to definitions for audit. The reward is
   optionally binarized (`REWARD_BINARIZE=True`, threshold 1.0: full marks or zero).
   Lesson: a verifier is a *specification file*, not a script — typed, weighted, gated
   items that an auditor can read without running code.

3. **Absolute vs group-relative reward is an explicit choice.** Music uses an absolute
   scale ("so periodic validation is a number worth reading"). Webdev uses a
   group-relative pick (rank each rollout against its GRPO siblings on screenshots, minus
   an absolute query-fit deduct) — relative grading is only valid because all siblings
   are present at advantage-computation time. Lesson: state which scale your score lives
   on and what comparison it licenses. SCBI verdict scripts should do the same.

4. **Offline re-verifiability by design (general arm).** `pull_post_state` (in
   `recipes/general/general_agent/environment.py`) snapshots the
   workspace and sidecar state as tarballs after each trajectory so verification can be
   re-run offline later (judge outage, audits, re-scoring) — "best-effort per part: a
   failed pull logs a warning and never affects the reward already computed." Lesson:
   an experiment whose verdict cannot be re-derived from stored artifacts is an
   experiment that cannot be independently reviewed.

5. **Reward-hygiene: corrupted rewards are tagged, never silently scored.** In
   `recipes/general/general_agent/environment.py`, a verifier that returns
   unparseable or out-of-range reward JSON
   gets `_mask(...)`: score 0.0 **plus** `error_category: REWARD_TESTBED_CORRUPTED`.
   The corruption is visible in the metrics, not hidden in the mean.

---

## 2. Agent-loop and trajectory-capture engineering — what transfers to inference-time loops

Architecture (from `recipes/{arvo,general,design}/agent_loop.py` and
`recipes/code/mimoagent_runner.py`):

- **Bridge at the narrowest contract.** The AgentLoop does NOT reimplement the agent:
  mimoagent owns the loop, tools, k8s environment, and reward. verl replaces exactly
  two seams: the model call (`LitellmModel` → `_VerlRolloutModel`, re-entering verl's
  rollout engine token-in/token-out) and tool-execution forwarding (to the Ray actor
  holding the pod, because tools must run next to the pod). The file header documents
  the three mimoagent contracts the bridge depends on, with the warning "breaking any
  of these breaks the bridge." Lesson: when SCBI builds loop apparatus around an
  existing harness, own as little as possible and write down the contracts you depend on.
- **Two deployment shapes.** Cyber/General/Visual drive mimoagent directly from a verl
  AgentLoop; Code instead runs the harness inside a uni-agent session (model gateway +
  TransferQueue trajectory capture) via `mimoagent_runner.py`, posting the final reward
  to a per-session endpoint. The submodules (mimoagent-osr, uni_agent) do not import
  each other; "the glue lives in `recipes/`." Lesson: keep the harness, the model
  gateway, and the glue in separate layers.
- **Token-exactness discipline (`token_trace.py`, `chat_delta.py`).** This is the
  sharpest transferable lesson. Chat templates do NOT round-trip: re-rendering a full
  message list through `apply_chat_template` produces different token ids than the
  incremental generation (tool-call text gets rewritten; Qwen3 injects an empty
  `<think></think>` block depending on whether the assistant turn is last —
  position-conditioned injection, not stripping of thinking; decode→encode is not a
  round trip). Xiaomi builds the token sequence incrementally
  and never re-renders an assistant turn — the buffer already holds the exact generated
  ids; only environment-injected messages get tokenized, rendered after a fixed anchor
  turn (with two concrete template traps documented, both found by a probe script —
  `probe_tool_call_format.py`, attested in docstrings only; the file itself is absent
  from the clone at `a2ad9f6`).
  **Any SCBI multi-turn loop experiment that re-renders its message list through the
  chat template can silently corrupt per-turn token attribution** (demonstrated on
  Qwen3-family templates; the failure is position-dependent, not universal). Any
  harness that re-renders per-turn must be probed. This is a
  measurement-validity defect class the program should name and test for.
- **Failure taxonomy with six infra categories** (`_INFRA_ERROR_CATEGORIES`):
  `setup/failed`, `rollout/pod_conn_timeout`, `rollout/seq_timeout`,
  `reward/exception`, `reward/env_error`, `reward/testbed_corrupted`. And two
  hard-won rules from the env files: `DROP_INFRA_FROM_GROUP=1` (exclude infra-failed
  rollouts from the comparison group — a pod that never came up scores 0.0 and hands
  siblings a spurious positive advantage) and `INVALID_REWARD_FOR_INFRA=False`
  (never write an out-of-range sentinel the optimizer — or a verdict script — would
  treat as signal). Webdev's `group_reward.py` shows the elegant version: INVALID rows
  are replaced with the **group mean**, which contributes exactly zero to a
  mean-centered decision statistic without touching the decision path.
- **Global-vs-local failure disambiguation (music scorer).** `Abc2MidiMissing` is a
  distinct exception from any scoring failure, "because it is the one that must not be
  reported as a reward of 0.0: it applies to every sample rather than to one score, so
  it is indistinguishable from 'the policy writes bad music' once flattened."
  `run_music.sh` probes for the binary on a worker and **refuses to launch** without
  it. Lesson: a harness-wide dependency failure must abort the run, never score it.
  SCBI's pre-flight checks should include dependency probes with refuse-to-launch
  semantics.
- **Measured, not inherited, configuration.** `webdev.env.example` documents that the
  sampling parameters were measured: "a run that passed these three scored 0.56 at
  step 1 while runs that left verl's naked defaults sat at 0.26–0.36 on the same
  checkpoint, data and grader weights." And: "Commented lines are the reference run's
  values. Uncommenting one at a different value changes the experiment, not just the
  run." Lesson: config values carry the measurement that justifies them; changing a
  value is a new experiment. This matches SCBI's pre-registration discipline and
  should be adopted verbatim in execution-bundle configs.
- **Multi-harness mixing against harness overfitting.** The code arm trains across
  four harness implementations (mini-mimocode, mini-bash, mini-claude-code,
  mini-codex) with step-hash mixing (seed 20260911; "changing it changes the
  experiment rather than just the shuffle"). The report's Table 7 shows gains hold on
  three additional held-out harnesses. Lesson: any behavioral claim from an agentic
  loop should be replicated across ≥2 harness implementations before it is trusted.

---

## 3. Section 7 training recipe as frontier context (Xiaomi's claims, not independently established)

- **Distillation (7.1).** MiMo-V2.6-Distill-Qwen-9B = SFT of Qwen3.5-9B on
  MiMo-generated data: 77.4B total tokens, 27.2B loss tokens (Code 23.2B / Cyber
  11.0B / General 22.0B / Visual 21.2B). Reported SFT gains: SWE-bench Pro 32.0→44.6,
  AutomationBench 5.0%→30.3%.
- **RL (7.2).** Per-domain GRPO from the same SFT checkpoint over ~8k tasks total
  (7k across the four envs + ~1k music). All 11 reported evaluations improve over SFT,
  e.g. SWE-bench Verified 61.1→66.2, Terminal Bench 2.1 37.1→52.8, OfficeQA Pro
  19.5→24.8, Toolathlon-Verified 35.2→38.0, MiMo Visual Coding (mini) 64.0→72.4,
  MiMo Cyber Bench (mini) 31.3→47.0, internal music 45.7→52.5.
- **Multi-harness coding experiment.** Joint optimization across four mini-harnesses;
  improves all 21 dataset–harness pairs (3 datasets × 7 harnesses incl. held-out);
  MiMo Code Bench (mini) gains +1.8–9.3pp over SFT across harnesses.
- **Reference run scale (from launch scripts).** 8 nodes × 8 GPUs per domain,
  GRPO group size N=8–16, batch 32–64, MAXLEN 262144 (music 116384), rollout
  temperature 0.6–1.0, 64–128 agent workers, one k8s pod per trajectory.
- **Claim shape.** The report's thesis: RL "substantially advances agentic
  capabilities" given a strong SFT initialization + high-quality environments with
  reliable verifiers. This is the same RL-scaling story as the Alibaba Qwen3.8-Max
  disclosure in the 2026-10-03 sweep — pipeline optimization, not demonstrated
  autonomous capability growth. It does not touch SCBI's Δθ=0 question either way.

---

## 4. NON-TRANSFERABLE list — does not apply to a Δθ=0 program

- RL algorithms: GRPO, PPO, DAPO, GSPO, ReMax, RLOO, PRIME, REINFORCE++, PF-PPO,
  VAPO, KL_Cov / Clip_Cov, and all advantage/loss-aggregation/entropy/KL machinery
  (incl. `NORM_ADV_BY_STD_IN_GRPO`, `LOSS_AGG_MODE`, dynamic-sampling filters).
- The SFT distillation recipe itself (77.4B tokens) and any checkpoint training.
- Training infrastructure: FSDP/Megatron backends, 3D-HybridEngine resharding,
  colocated train/rollout GPU topology, checkpointing/resume, off-policy thresholds.
- The compute scale: 8×8 GPU nodes per domain, 64–128 agent workers, per-trajectory
  k8s pods — incompatible with the $0-compute constraint.
- Judge-based rewards (the general arm's rubric LLM-judge, the webdev visual grader)
  as *training signals*; their *design patterns* (typed rubrics, gates) transfer, the
  optimization loop does not.

---

## 5. Cheapest next steps (worth-it gated: each names the decision it changes)

1. **Token-exactness unit test before any multi-turn loop experiment runs.**
   Write a CPU test asserting that the SCBI loop harness's per-turn token attribution
   is stable under incremental buffering (never re-render assistant turns through the
   chat template). *Decision it changes:* the measurement-validity gate on EXP139
   Stage-2 (re-entrant re-injection is a multi-turn loop; corrupted turn attribution
   would void the verdict exactly as the length-guard defect voided EXP142).
2. **Adopt the three-way run taxonomy in verdict scripts: valid / invalid-neutralized
   (replace with group mean) / systematic-global-failure (abort).** Add a pre-flight
   dependency probe with refuse-to-launch semantics to the experiment-runner template.
   *Decision it changes:* KILL/HELD/CONTINUE verdicts in grouped-comparison
   experiments (the EXP140 branch-selection family), where an infra failure currently
   risks masquerading as signal.
3. **Config-as-protocol comments in the EXP139 Stage-2 execution bundle.** Every
   apparatus value carries the measurement or failure that justifies it; the file
   states that changing a value is a new experiment. *Decision it changes:* whether
   the pending independent apparatus review of the Stage-2 bundle can reach Law #14
   SIGN.
4. **Post-state snapshots for re-verifiability.** The Stage-2 bundle should dump full
   trajectories plus environment state so the verdict can be re-derived offline.
   *Decision it changes:* whether a future Law #14 re-verification of the Stage-2
   verdict is possible at all.

Dormant (no licensed decision yet, recorded for the future): two-gate verifier specs,
typed rubric items with method/weight/gate/dim, and multi-harness (≥2 implementations)
replication become relevant only if SCBI ever commissions an agentic-behavior lane.

---

## 6. What was not verified

- Submodule internals were NOT read (`third_party/mimoagent-osr`, `third_party/uni_agent`
  not initialized, per instructions); mimoagent/uni-agent descriptions come from the
  root README and bridge-file headers only.
- `recipes/arvo/agent_loop.py` and `recipes/design/agent_loop.py` were skimmed for
  structural sameness with `recipes/general/agent_loop.py` (read in depth); agent-loop
  claims rest primarily on the general arm.
- No code was executed; no trajectories, rewards, or benchmark numbers were reproduced.
- Report benchmark claims (Section 7, Tables 4–7) are Xiaomi's self-reports. Public
  rows (SWE-bench Verified/Pro, Terminal Bench 2.1, OfficeQA Pro, Toolathlon-Verified,
  AutomationBench, JobBench) are checkable against public leaderboards [NOT CHECKED
  HERE]; internal "mini" benches and the music score are vendor-reported and unverifiable
  from outside.
- The MiMo-V2.6 report PDF was fetched from HuggingFace (creation date 2026-09-22);
  its Section 7 text extracted with pdftotext (some ligature/font warnings, no content
  loss observed in the extracted section).
