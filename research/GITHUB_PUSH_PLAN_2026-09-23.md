# GitHub Push Plan — LOG-196

*Prepared 2026-09-23 by the Research Lead. User authorization: push all
program work to https://github.com/anilkumara9/SCBI.git (origin, branch
main). Status: PLAN ONLY — no push executed. Push is blocked on CEO
confirmation of write authentication (user adds the lab's SSH public key to
GitHub). Local commits may be created to stage the series; the push itself
waits for the CEO's explicit clearance.*

## Pre-push state

- Branch: `main`; remote `origin` = the authorized URL (fetch + push).
- 68 changed/untracked entries: 27 reports, 19 experiments, 12 research,
  3 theory, 7 modified (incl. research_log.md, paper_draft.md,
  novelty_report.md, ledger, manifest, formulation doc).
- Total new content ≈ 4.5 MB (runs 2.3 MB, reports 1.6 MB, synthesis
  0.5 MB). No large binaries; no zips/npz/pkl/h5 among the changes.

## Secrets sweep — PASS (2026-09-23)

- No `.env`, `kaggle.json`, `.netrc`, `*credential*`, `*.pem`, `*.key`
  (private), or `id_rsa*` anywhere in the tree (`.git/` excluded).
- Pattern grep for `ghp_|gho_|github_pat_|sk-|AKIA|BEGIN PRIVATE KEY|api_key`
  across the repo: zero hits. A narrower prose-pattern check over the
  68 changed files flagged two files (research_log.md, CEO_DIARY.md) —
  both manually inspected, both false positives (words like
  "benchmark-equivalence", "key finding"; no credential values).
- Kaggle credentials remain in the Secure Vault only; they never enter
  the repo. The GitHub SSH public key is shared with the user out-of-
  band, not committed.
- `.gitignore` already excludes: `__pycache__/`, `*.py[cod]`,
  `.venv/`, `*.bin`, `*.safetensors`, `*.pt`, `*.pth`, `*.onnx`,
  `checkpoints/`, `experiments/runs/*/tensors/`,
  `experiments/runs/*/weights/`, `.env`, `*.key`, `*token*`, `*.pem`,
  `wandb/`, editor/OS junk.

### .gitignore additions (commit with the push series)

```gitignore
# Notebook checkpoints & execution byproducts
.ipynb_checkpoints/
*.ipynb  # Kaggle notebooks live on Kaggle; the repo keeps .py sources

# Local experiment scratch
experiments/runs/*/scratch/
*.npz
*.pkl

# Push-plan staging
*.bundle-push-pending
```

(Rationale: `.py` sources are the audit trail; notebook JSON diffs are
noise. Run-result JSONs/CSVs stay tracked — they ARE the evidence.)

## Commit series (logical, audit-trail-preserving)

Create locally in this order; push once as a batch after auth
confirmation. One `git push -u origin main` at the end — no force-push,
ever.

1. `chore(governance): research operating system, charters, and team
   structure`
   `research/RESEARCH_OPERATING_SYSTEM.md`
   `research/RESEARCH_LEAD_CHARTER.md`
   `research/TEAM_KNOWLEDGE_PROTOCOL.md`
   `research/MATH_STANDARDS_CHARTER.md`
   `research/CHATGPT_MENTORSHIP_DIRECTIVE.md`
   `research/EXPERT_TRACKS.md`
   `research/TEAM_ROSTER_2026-09-23.md`
   `research/CEO_DIARY.md` (modified → new file? it is untracked;
   include here)

   *Note: CEO_DIARY.md contains internal deliberation notes. It is
   pushed deliberately — the program's "document everything" standard
   and the diary-as-institutional-memory design assume it is readable
   by future agents and reviewers. Flag for CEO: if any diary passage
   must stay private, say so before the push and it moves to
   `research/hidden/` (gitignored).*

2. `feat(experiments): pre-registered protocols EXP067–EXP081, C-A v2,
   G2, innovation proposals`
   `experiments/protocols/*.md` (12 protocol specs incl. C-A pre-audit
   JSON/MD), `research/innovation/`

3. `data(runs): experiment run artifacts EXP067–EXP079`
   `experiments/runs/exp067/ exp070/ exp075/ exp077/ exp078/ exp079/
   EXP077_cone_vs_line/` — result JSONs, evaluator logs, hashes.
   (Tensors/weights excluded by .gitignore — verify with
   `git status --ignored` before committing.)

4. `docs(reviews): Law #14 adversarial reviews and audit trail`
   `reports/adversarial_*.md` (25 review files), 
   `reports/adversarial_audit_exp065_exp066.md`

5. `docs(literature): prior-art verification records and analysis
   plans`
   `research/literature/audit_2026-09-23.md`
   `research/literature/mentor_citations_verification_2026-09-23.md`
   `research/analysis_plans/`

6. `docs(synthesis): A–J synthesis LOG-158 → REV (LOG-187) → REV2
   (LOG-191)`
   `research/synthesis/` — all three versions preserved; the audit
   trail IS the product. Includes edit specs and stats drafts.

7. `docs(theory): boundary formalization, loop spec, Procrustes proofs`
   `theory/BOUNDARY_CLAIM_FORMALIZATION.md`
   `theory/LOOP_SPEC_DRAFT.md`
   `theory/proofs/procrustes_failure_analysis.md`

8. `docs(sync): corrected ledger, manifest, paper draft, novelty
   report, research log`
   The 7 modified files: `.muse by meta/COMPREHENSIVE_EXPERIMENT_LEDGER.md`,
   `.muse by meta/README.md`, `.muse by meta/manifest.json`,
   `reports/research_log.md`, `reports/paper_draft.md`,
   `reports/novelty_report.md`, `theory/README_FORMULATION.md`.
   (These carry the EXP065/066 retractions — the commit message must
   say so: "retract false Procrustes improvement claims; reframe as
   boundary result".)

9. `docs(push): GitHub push plan and .gitignore hardening`
   `research/GITHUB_PUSH_PLAN_2026-09-23.md`, `.gitignore` additions.

## Pre-push verification checklist (run in order, all must pass)

- [ ] `git status --ignored` shows no `tensors/`, `weights/`,
      `checkpoints/`, `.ipynb`, or credential files staged.
- [ ] `git log --stat` reviewed: 9 commits, messages match the series.
- [ ] Secrets sweep re-run on the staged tree (patterns above): clean.
- [ ] CEO confirms write authentication (user added SSH key; CEO
      verified with `ssh -T git@github.com` or a dry-run fetch).
- [ ] CEO diary privacy flag cleared (commit 1 note above).

## The push (CEO clearance required)

```bash
cd ~/workspace/SCBI
git push -u origin main
```

If the push is rejected (non-fast-forward): STOP, do not force-push —
report to the CEO; the remote has commits the lab does not have, and
merging them is a CEO decision, not a mechanical step.

## Branch/tag convention going forward

- `main` is the only long-lived branch. All work lands via reviewed
  local commits; no PR workflow (single-lab repo, user owns upstream).
- Tags mark program gates, never experiments:
  `gate/synthesis-adopted-YYYY-MM-DD`,
  `gate/ntp-branch-s-licensed-EXP###`,
  `paper/submitted-<venue>-YYYY-MM-DD`.
  Experiment numbers live in file names and the log (LOG-###), not in
  branches.
- Short-lived `exp/EXP###-bundle` branches are permitted for Kaggle
  bundle assembly, merged to main before any GPU run, deleted after.
- Signed protocols and primary artifacts are never amended or
  rebased — a correction is a new commit that preserves the old
  wording with its retraction (Law #12, Operating System §3).
