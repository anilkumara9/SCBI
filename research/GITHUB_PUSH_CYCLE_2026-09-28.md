# SCBI GitHub Push Cycle — 2026-09-28 (LOG-4393 → LOG-4465)

**Status: PREPARED — NOT PUSHED.** Topic branch staged and committed locally.
The push itself requires a fresh founder-supplied token (used once, transiently).
No PR has been opened. No remote state has changed.

## 1. What's on the branch

- **Branch:** `sync/2026-09-28-log4393-4465-wave`
- **Base:** `e90d0d8` (main, "LOG-4389-4392: scoreboard EXP094 entry…")
- **Commit:** `<commit hash — fill at push time>`
- **Worktree:** `~/workspace/SCBI-worktrees/sync-log4393-4465`
- **Coverage:** LOG-4393 → LOG-4465 (everything since the last push, which stopped at LOG-4392)

### File inventory (66 paths)

| Category | Contents |
|---|---|
| Modified (3) | `reports/research_log.md` (LOG-4393→4465 entries), `research/analysis_plans/s5_3_decode_probes_2026-09-28.py`, `research/innovation/CANDIDATE_BACKLOG.md` |
| Verdict reviews (9) | `experiments/protocols/REVIEWS/EXP095_VERDICT_REVIEW` … `EXP103_VERDICT_2026-09-28.md` |
| Prereg reviews (14) | `S5-1`, `S5-4`, `S6-1`, `S6-2`, `S6-3`, `S6-3b`, `S6-3c`, `S6-3d`, `S6-4` Law #14 reviews + delta re-verifications |
| Run bundles (9) | `experiments/runs/EXP095_alpha_sweep/` … `EXP103_L20maxgated_L11/` (per_item CSVs, manifests, worksheets, run logs; **no weights, no tensors, no checkpoints — enforced by `.gitignore`**) |
| Prereg drafts (14) | `research/innovation/S5-1_PREREG_DRAFT{,_v2}`, `S5-4…`, `S6-1…`, `S6-2…`, `S6-3…`, `S6-3b…`, `S6-3c…`, `S6-3d…`, `S6-4_PREREG_DRAFT{,_v2}` |
| Analysis (6) | `S5_3_REPORT`, `S6_5_POOLED_POWER_AUDIT`, coordinates/results JSONs, recompute script |
| Strategy (2) | `S6_STANDDOWN_RECOMMENDATION_2026-09-28.md`, `LEGENDARY_GAP_ANALYSIS_2026-09-28.md` |
| Sprint | `NEXT_DIRECTION_SPRINT_2026-09-28.md` |
| This plan | `research/GITHUB_PUSH_CYCLE_2026-09-28.md` |

### Secret/weight audit (prep lane, 2026-09-28)

- No `*.bin / *.safetensors / *.pt / *.pth / *.ckpt / *.npz / *.pkl / *.onnx` files.
- No `.env / *.pem / *secret* / *credential* / *.key / id_rsa*` files.
- No files > 5 MB.
- `__pycache__/`, `tensors/`, `weights/`, `scratch/` excluded by `.gitignore`.
- Prose scans for `ghp_ / github_pat / sk- / api_key / password=` returned only ordinary words ("prompt token", "password reset" prose) — no credential values.

## 2. Push commands (founder or token-carrying follow-up lane)

All commands run in the worktree. The token arrives from the founder in chat,
is used once via a transient env var in a single command, and is never written
to disk, memory, or any file.

```bash
cd ~/workspace/SCBI-worktrees/sync-log4393-4465
git status --short                      # must be clean
git log --oneline -1                    # must show the sync commit on top of e90d0d8

# Fast-forward / pre-existence checks (read-only; do these BEFORE pushing)
git fetch origin
git ls-remote origin 'refs/heads/sync/2026-09-28-log4393-4465-wave'
# ^ must print NOTHING — the branch must not exist remotely yet.
# If it does exist remotely, STOP and ask the founder: never force-push.

# Push (token used once, transiently — replace $SCBI_TOKEN with the
# founder-supplied value; the env var lives only for this command)
SCBI_TOKEN='<founder-supplied-token>' git -c credential.helper= \
  -c credential.helper='!f() { echo username=x-oauth-basic; echo "password=$SCBI_TOKEN"; }; f' \
  push -u origin sync/2026-09-28-log4393-4465-wave

# Verify it was a fast-forward creation, not a rewrite
git ls-remote origin 'refs/heads/sync/2026-09-28-log4393-4465-wave'
# ^ must print exactly one line with the local commit hash.
```

### Open the PR (after the push verifies)

```bash
SCBI_TOKEN='<founder-supplied-token>' GH_TOKEN="$SCBI_TOKEN" gh pr create \
  --repo anilkumara9/SCBI \
  --base main --head sync/2026-09-28-log4393-4465-wave \
  --title "Sync LOG-4393–4465: EXP095–103, S6 gate-family closure, stand-down, gap analysis" \
  --body "Research wave LOG-4393→4465. EXP095 Refuted · EXP096 Refuted · EXP097 PIVOT · EXP098 PIVOT · EXP099 PIVOT · EXP100 PIVOT (untestable) · EXP101 Refuted · EXP102 PIVOT (untestable) · EXP103 Refuted (gated KILL, closes {mean,max}×{L11,L20} 4/4). S6 L11-rescue program stood down (LOG-4463/4464). Legendary-paper gap analysis delivered (LOG-4465). CPU-only \$0; no weights; Δθ=0 throughout. Review-before-merge per GIT_WORKFLOW.md."
```

If `gh` is unavailable, open the PR in the browser at:
`https://github.com/anilkumara9/SCBI/compare/main...sync/2026-09-28-log4393-4465-wave`

## 3. Checklist (must all pass before/during the push)

- [ ] `git status --short` clean in the worktree
- [ ] Branch does NOT exist on origin yet (`git ls-remote` empty) — if it does, STOP, do not force-push
- [ ] No `git push --force` anywhere, ever
- [ ] Token supplied fresh by the founder, used once, transiently; never stored, never written to any file or memory
- [ ] After push: remote hash == local commit hash (fast-forward creation verified)
- [ ] PR opened against `main`, reviewed per the SOP before merge
- [ ] Signed protocols untouched (all corrections were append-only errata / new versions — true for this wave)
- [ ] This plan doc + the commit are the only new files on the branch beyond the research materials

## 4. After merge

- `git worktree remove ~/workspace/SCBI-worktrees/sync-log4393-4465` (only after the PR is merged and `main` is pulled)
- Next wave starts from the new `main` HEAD
