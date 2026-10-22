# Law #14 Independent Review — XiaomiMiMo/verl guidance brief

**Artifact:** `research/frontier/XIAOMIMIMO_VERL_GUIDANCE_2026-10-03.md` (study lane, 2026-10-03)
**Reviewer:** Independent Scientific Mentor & Adversarial Reviewer
**Date:** 2026-10-03
**Binding verdict: SIGN-WITH-FIXES** (five required fixes, F1–F5, enumerated below)

## Method [FACT]

Fresh shallow clone of `https://github.com/XiaomiMiMo/verl` @
`a2ad9f6160b03ff2d47e59832bfb6b289f37c917` to `/tmp/verl_review` (never in the
workspace; deleted after review — $0 compute, no execution of any code). I read
every cited file: `recipes/design/music/scorer/pipeline.py`,
`recipes/design/run_music.sh`, `recipes/general/general_agent/environment.py`,
`recipes/general/token_trace.py`, `recipes/general/chat_delta.py`,
`recipes/general/agent_loop.py` (header + infra categories),
`recipes/design/webdev/group_reward.py`, `scripts/design/webdev.env.example`,
`scripts/design/music.env.example`, `scripts/code/train.sh`,
`scripts/general/general.sh`, `recipes/general/env_actor.py`. I cross-checked
all Section 7 numbers against the MiMo-V2.6 report PDF (fetched from HuggingFace;
tables recovered with `pdftotext -layout` after the plain extraction dropped
Table 5's rows).

## 1. Code observations — spot-check results [FACT]

Every substantive code claim verified at the pinned commit:

- **Two-gate music scoring:** CONFIRMED. `extract_abc` (fenced ABC block →
  `abc2midi` → MIDI bytes) then scoring of MIDI features against
  `baselines/ref_full4k.json` (file exists). `Abc2MidiMissing` is a distinct
  `RuntimeError` whose docstring states the exact rationale the brief quotes
  (must not be flattened to reward 0.0 because it applies to every sample).
- **run_music.sh refuse-to-launch:** CONFIRMED. Probes `abc2midi` via
  `command -v`; FATAL exit if absent after apt-get fallback; separate
  "refusing to launch" on unresolvable Hydra config.
- **Reward hygiene:** CONFIRMED. `_mask()` in
  `recipes/general/general_agent/environment.py` returns `(0.0, output, info)`
  with `error_category: REWARD_TESTBED_CORRUPTED` on unparseable or
  out-of-range reward JSON. (`REWARD_TESTBED_CORRUPTED` itself is imported from
  the uninitialized mimoagent submodule — the brief's §6 discloses this.)
- **Typed rubric metadata:** CONFIRMED. `VERIFIER_FILES` manifest lists
  `run_verify.py`, `verify.py`, `rubrics.json`, `answer_key.json`,
  `verifier_meta.json`, `_helpers.py`; `_annotate_rubric_kinds` joins results to
  `verifier_meta.json` definitions adding exactly method (rule/llm) / weight /
  gate / dim. `REWARD_BINARIZE` (default True in `scripts/general/general.sh`,
  threshold 1.0 in `env_actor.py`) matches the brief.
- **Offline re-verifiability:** CONFIRMED. `pull_post_state` docstring is
  quoted verbatim (two tarballs: workspace/ + system/; "Best-effort per part: a
  failed pull logs a warning and never affects the reward already computed").
- **Agent-loop bridge:** CONFIRMED. The `agent_loop.py` header documents the
  two replaced seams (`LitellmModel` → `_VerlRolloutModel` re-entering verl's
  rollout engine; tool execution forwarded to the Ray actor holding the pod)
  and the three mimoagent contracts with the exact warning "breaking any of
  these breaks the bridge". `recipes/code/mimoagent_runner.py` exists for the
  Code arm's uni-agent deployment shape.
- **Token-exactness:** CONFIRMED as a real finding in the repo.
  `token_trace.py`: "we build the sequence incrementally and never re-render an
  assistant turn… the buffer already holds the exact token ids the policy
  emitted". `chat_delta.py` documents the two template traps and the fixed
  anchor-turn fix. See F2/F3 for scope corrections.
- **Failure taxonomy:** CONFIRMED verbatim. All six
  `_INFRA_ERROR_CATEGORIES` match; `INVALID_REWARD_VALUE = -999.0`;
  `fail_on_env_setup_error` refuses to score infra failures.
- **Group-mean neutralization:** CONFIRMED. `group_reward.py` docstring:
  "INVALID here means 'replace with the group's mean valid reward'… GRPO only
  ever looks at `reward - group_mean`". The brief's generalization to
  "mean-centered decision statistic" is a fair paraphrase, not a distortion.
- **Measured config:** CONFIRMED verbatim. `webdev.env.example`: "a run that
  passed these three scored 0.56 at step 1 while runs that left verl's naked
  defaults sat at 0.26-0.36"; "Commented lines are the reference run's values."
- **Multi-harness mixing:** CONFIRMED. `scripts/code/train.sh` loops
  `mini-mimocode mini-bash mini-claude-code mini-codex` with
  `MIXED_HARNESS_SEED=20260911`; report text confirms "improves on Qwen3.5-9B
  in all 21 dataset–harness pairs" and "+1.8 to 9.3 percentage points" on MiMo
  Code Bench (mini).
- **Absolute vs group-relative:** CONFIRMED verbatim. `music.env.example`:
  "This scorer has an absolute scale, unlike the web-dev arm's group-relative
  reward, so periodic validation is a number worth reading."
  `group_reward.py`: "a relative aesthetic pick across the n sibling
  screenshots, minus an absolute query-fit deduct".
- **Non-transferable identifiers:** CONFIRMED real. `norm_adv_by_std_in_grpo`
  (trainer config) and `loss_agg_mode` (`verl/workers/utils/losses.py`) exist;
  the brief's SCREAMING_CASE rendering is a style choice, not invention.

No invented files, paths, functions, or numbers found. Law #2/#3 clean.

## 2. Evidence labels [INTERPRETATION]

PASS with one required fix. §3 is properly fenced ("Xiaomi's claims, not
independently established"), the [UNVERIFIED] convention is declared and used,
and the claim-shape paragraph correctly refuses to launder the RL-scaling
story into a capability-growth claim. The brief does not present any Xiaomi
number as an independent finding.

- **F5 (required):** the §1 environment table's "Scale (train tasks)" column
  gives no source. I recovered Table 5 from the report PDF (`pdftotext
  -layout`): Code 3k / Cyber 1k / General 1k / Visual 2k with the exact
  verifiers the brief lists, plus "approximately 1k music-generation tasks"
  in the §7.2 body text. The brief's numbers are right, but the column must
  cite Table 5 of the MiMo-V2.6 report as its source and keep the "~" — the
  same labeling discipline §3 uses.

## 3. Transferability stress-test [INTERPRETATION]

The core judgment — RL algorithms transfer nothing to a Δθ=0 program;
verifier design, failure taxonomy, and token-exactness engineering do — is
**sound**. Nothing weight-update-flavored appears in the transferable column,
and the non-transferable list is complete (algorithms, SFT recipe, training
infra, compute scale, judge-as-training-signal).

Two scope corrections required on the token-exactness claim, which is the
sharpest transferability assertion in the brief:

- **F2 (required):** "Any SCBI multi-turn loop experiment that re-renders its
  message list through the chat template **will** silently corrupt per-turn
  token attribution" overstates the evidence. The repo demonstrates the defect
  on Qwen3-family templates (Qwen3-Coder / Qwen3.5 / Qwen3) via
  position-dependent rendering; a single full-list render for a fresh prefill
  is the normal, safe case. Soften to: "**can** silently corrupt
  (demonstrated on Qwen3-family templates; the failure is position-dependent,
  not universal). Any harness that re-renders per-turn must be probed." The
  recommended CPU unit test (worth-it step 1) stands as written — it is the
  correct defensive response to a demonstrated defect class.
- **F3 (required):** the parenthetical gloss "(tool-call text gets rewritten,
  thinking gets stripped, decode→encode is not a round trip)" misstates the
  second documented trap. Per the `chat_delta.py` docstring, Qwen3 *injects*
  an empty `<think></think>` block depending on whether the assistant turn is
  last — it is injection conditioned on position, not stripping of thinking.
  Correct the gloss to match the docstring.

- **F4 (required):** `probe_tool_call_format.py` is docstring-attested only —
  the file itself is not present in the shallow clone at `a2ad9f6` (referenced
  in `chat_delta.py` and `agent_loop.py`, no file found). Note this explicitly
  rather than implying the probe was inspected.

## 4. Worth-it gates [FACT]

All four next steps name the exact kill/continue decision they change:
(1) token-exactness unit test → the measurement-validity gate on EXP139
Stage-2; (2) three-way run taxonomy + refuse-to-launch pre-flight →
KILL/HELD/CONTINUE verdicts in grouped-comparison experiments (EXP140
family); (3) config-as-protocol comments → whether the Stage-2 apparatus
review can reach Law #14 SIGN; (4) post-state snapshots → whether future
Law #14 re-verification of the Stage-2 verdict is possible at all. PASS.

## 5. Non-transferable list [INTERPRETATION]

Complete. Covers RL algorithms with their advantage/loss/entropy/KL
machinery, the SFT distillation recipe, training infrastructure, compute
scale, and judge-based rewards *as training signals* (correctly distinguishing
them from their transferable design patterns). Nothing smuggled. PASS.

## Binding verdict: SIGN-WITH-FIXES

The brief is substantively accurate — I verified every code observation and
every Section 7 number against primary sources, and found no invented
content. The five required fixes are citation precision and scope
corrections; none changes the bottom line:

- **F1:** give full repo-relative paths for all code citations; the `_mask` /
  `_annotate_rubric_kinds` / `pull_post_state` / `VERIFIER_FILES` / `verify.py`
  claims live in `recipes/general/general_agent/environment.py`, not a
  top-level `environment.py`. Clarify that `general_agent/environment.py`
  drives `verify.py` inside the pod.
- **F2:** soften the token-exactness universality claim (see §3).
- **F3:** correct the `<think></think>` gloss to injection-per-position (see §3).
- **F4:** note `probe_tool_call_format.py` is docstring-attested only, file
  not found in the clone.
- **F5:** cite Table 5 of the MiMo-V2.6 report as the source of the §1 scale
  column.

After a repair lane applies F1–F5 (mechanical edits, no new research), the
brief may be treated as signed. No re-review required unless the repair
changes substance. I did not modify the brief; fixes are listed here for a
separate repair step.
