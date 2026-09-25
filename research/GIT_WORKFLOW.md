# SCBI Git Workflow — Lab Standard Operating Procedure

Adopted 2026-09-25 by founder order ("constantly push to the github and also pull
request everything — tell to your team properly like how lab do").
Standing rule; amendable only by the founder.

## 1. Branching model

- `main` is protected and always in a working state. **Nobody commits to `main`
  directly** — not the CEO, not workers, not the reviewer.
- Every workstream gets a topic branch, cut from current `main`:

  ```
  exp/<NNN>-<slug>        experiments, e.g. exp/093-l11-causal-bundle
  review/<NNN>-<slug>      independent reviews, e.g. review/093-law14-bundle
  analysis/<slug>          analyses, re-mining, forensics
  docs/<slug>              docs, SOPs, scoreboard updates
  fix/<slug>               hotfixes to tooling (never to signed protocols)
  sync/<date>-<slug>       backlog syncs, only when authorized by the CEO
  ```

- One branch = one reviewable unit. If a session produces two unrelated units,
  cut two branches.

## 2. Commit discipline

- Commit early, commit often — end every work session with a clean tree.
- Message format:

  ```
  <area>: <imperative summary> (LOG-XXXX)

  <what and why, 1-3 lines; name the review verdict if any>
  ```

  Examples: `exp093: build causal-transfer bundle, 21/21 tests green (LOG-4344)`,
  `review: Law #14 SIGN on EXP093 bundle (LOG-4345)`.
- Never commit: credentials, tokens, model weights, `.npz`/weight snapshots,
  `node_modules`, scratch files. The `.gitignore` is law; check `git status`
  before every commit.
- Signed protocols are immutable. A correction = append-only erratum in the run
  report or a new experiment number — never a force-push, never a rewrite.
  **Force-push is forbidden, always.**

## 3. Push discipline — "constantly push"

- Push the branch at the end of every work session, and whenever a meaningful
  unit completes. A branch that exists only locally does not exist.
- Pushes require a fresh founder-supplied token each time (used once, transiently,
  never stored, never written to memory or files). The CEO keeps every branch
  push-ready so a token turns into a push in one step.
- Verify fast-forward before pushing (`git fetch origin`, compare). If the remote
  moved, rebase the topic branch onto the new `main` — never merge `main` into
  the topic branch, never force-push.

## 4. Pull-request discipline — "pull request everything"

- Every branch merges via a PR. No exceptions.
- PR title: `[<area>] <summary> (LOG-XXXX)`. PR body uses the template:

  ```markdown
  ## What
  ## Why (worth-it gate: question / decision / cheapest test / license)
  ## Verification (tests, guards, review verdicts — link LOG entries)
  ## Risk / notes
  ```

- Review-before-merge:
  - Research artifacts (protocols, bundles, analyses, verdicts): PR needs an
    independent Law #14 **SIGN** (or SIGN-WITH-FIXES with fixes applied and
    re-verified) before merge. The reviewer's verdict is binding.
  - Docs/tooling: CEO sign-off suffices.
- Merge = squash-and-merge for workstreams with many micro-commits, rebase-merge
  for clean linear histories. Delete the branch after merge.
- The founder is the only one who can merge a PR that the reviewer rejected.

## 5. Standing orders to the team

1. Cut a branch before you start. Name it per §1.
2. Keep `git status` clean at session end; push the branch.
3. Open a PR with the §4 template when the unit is done.
4. Never commit to `main`. Never force-push. Never commit secrets or weights.
5. If the remote moved, rebase — ask the CEO if there is a conflict you do not
   fully understand.

## 6. What "constantly" means in practice

The lab pushes branch-by-branch through the day as units complete; `main`
advances PR-by-PR after review. Anyone opening GitHub sees live branches, open
PRs with LOG-linked descriptions, and a `main` that is always green. That is
the lab standard.
