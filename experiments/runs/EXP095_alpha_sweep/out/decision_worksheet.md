# EXP095 — Decision-Table Worksheet (evidence only)

**Status: UNINTERPRETED.** This worksheet carries the mechanical evidence for
the signed pre-reg §3 steps 0–2 plus the per-alpha contrast statistics.
Steps 3–6 belong to the separate verdict lane (Law #14); no verdict is
walked or implied here.

Source records: `experiments/runs/EXP095_alpha_sweep/out/`
- `per_item_records.csv` — 660 rows (60 B + 300 T + 300 B_wrong)
- `stratum_table_135.json` — 45 contrast cells (3 strata × 5 α × 3 contrasts)
- `stratum_sideband.json` — 45 sideband cells (mean margin shift + flip ledgers)
- `mechanical_readout.json` — machine read-out (UNINTERPRETED)
- `constructor_manifest.json`, `env_manifest.json`, `delivery_probe_log.json`
- `exp095_run_log.txt`, `artifact_hashes.txt`

## Step 0 — replication anchor (executor gate)

| Check | Evidence |
|---|---|
| Constructor re-hash vs frozen pin `5e03f206…917f361` | match; audit verdict PASS |
| Weights Δθ=0 pre/post vs LOG-331 pin | `ec276abe…0ed` pre = post = pin |
| Per-item B decisions vs archived EXP094 baseline | 60/60 match |
| T(1.0) flips vs B | 0 (< 6; foundation-wobble = false) |
| Degeneracy sanity | mean\|cos\| = 0.7922606323 vs archived 0.7923 (tol 0.05) |

## Step 1 — delivery per α (executor gate)

| α | Band | In band | Probe |
|---|---|---|---|
| 0.25 | [0.00889, 0.01481] | 60/60 | PASS |
| 0.5 | [0.01778, 0.02963] | 60/60 | PASS |
| 1.0 | [0.0355, 0.0593] | 60/60 | PASS |
| 2.0 | [0.0711, 0.1185] | 60/60 | PASS |
| 4.0 | [0.1422, 0.2370] | 60/60 | PASS |

G5 execution probe (α=1.0, item 0): rel_err=4.26e-07, other-pos=0.00e+00,
bit_match=True → PASS. No α excluded. No common-cause failure.

## Step 2 — degeneracy gate input (executor gate)

mean pairwise |cosine| over regenerated {d_i} = 0.7922606323 (< 0.95 bar).
Sanity vs archived 0.7923: within 0.05 → regeneration verified.

## Per-α contrast statistics (for verdict lane, steps 3–6)

Aggregate stratum (A/C strata in `stratum_table_135.json`):

| α | arm | n correct /60 | flips vs B | ΔM | McNemar b/c | McNemar p | ties/180 |
|---|---|---|---|---|---|---|---|
| 0.25 | T | 36 | 0 | 0.0 | 0/0 | 1.0 | 0 |
| 0.25 | B_wrong | 36 | 0 | 0.0 | 0/0 | 1.0 | 0 |
| 0.5 | T | 36 | 0 | 0.0 | 0/0 | 1.0 | 0 |
| 0.5 | B_wrong | 36 | 0 | 0.0 | 0/0 | 1.0 | 0 |
| 1.0 | T | 36 | 0 | 0.0 | 0/0 | 1.0 | 0 |
| 1.0 | B_wrong | 36 | 0 | 0.0 | 0/0 | 1.0 | 0 |
| 2.0 | T | 35 | 1 | −1/60 | 0/1 | 1.0 | 0 |
| 2.0 | B_wrong | 36 | 0 | 0.0 | 0/0 | 1.0 | 0 |
| 4.0 | T | 35 | 1 | −1/60 | 0/1 | 1.0 | 0 |
| 4.0 | B_wrong | 36 | 2 | 0.0 | 1/1 | 1.0 | 0 |

Flip ledger (from `stratum_sideband.json`, aggregate):
- α=2.0 T-vs-B: 1 flip to wrong — `exp092_planetary_3hop_7`.
- α=4.0 T-vs-B: 1 flip to wrong — `exp092_planetary_3hop_7`.
- α=4.0 B_wrong-vs-B: 1 flip to right — `exp092_planetary_2hop_2`;
  1 flip to wrong — `exp092_planetary_2hop_0` (net ΔM = 0).

Tie gate: 0 ties at every α (≤ 5%) → no α RUN-INVALID.

## Budget

724 passes (60 B + 60 Ref + 60 T(1.0) + 240 T + 300 B_wrong + 4 G5 probe);
hard cap 1300; CPU only; $0. Threads pinned at 2.
Environment: torch 2.14.0+cpu, transformers 5.17.0, numpy 2.5.3,
python 3.12.3, venv `~/workspace/.venv-exp095`.
