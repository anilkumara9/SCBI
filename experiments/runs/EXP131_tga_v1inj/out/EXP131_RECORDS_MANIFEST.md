# EXP131 raw-records manifest

Executed 2026-09-30 ~02:12 IST on the founder's Kaggle T4 (torch 2.10.0+cu128,
transformers 5.17.0, numpy 2.0.2). Independent Law #14 execution review: binding
SIGN, LOG-4766.

## Files (live on the Kaggle notebook, /kaggle/working/out/, 52K total)

| file | sha256 |
|---|---|
| exp131_console.log (12K) | ce016b6394576da5bde5883bfca880be6c6dd699ea56d02c126f6853615ccb35 |
| exp131_records.json (29K) | e33a0eac4f492eb53c441e00899023a2ee6bdb69f11340f8767644466283b1d6 |
| exp131_records.json.sha256 (65B) | 00fbcbb1d98c2708059fd8a2efc5342ea8ebfa63c2fb3700ef1d6f6f38c4d557 |
| exp131_report.json (873B) | ec22869297f0eef709f8202c4c7ad7010904413fb8cc812a3d9140f9a844ec5b |

The records file's sha256 was cross-verified on the notebook against both the
`records_pin` in exp131_report.json and the `.sha256` sidecar: all three agree
on `e33a0eac4f492eb53c441e00899023a2ee6bdb69f11340f8767644466283b1d6`.

`exp131_report.json` is archived verbatim in this directory. The 29K raw
`exp131_records.json` was inspected in full on the notebook (printed verbatim,
untruncated) and remains there; its verified content summary:

- env/pins: protocol d85205f4…, weights_pre = weights_post = ec276abe… (LOG-331,
  Δθ=0 held), v1_npz 9b527c02…, bagg_reconstruction 547387f6…,
  bench e91b302f…, budget B = 0.505781192779541.
- c_hat_per_prompt (10 values, 0 exclusions): 0.06341, 0.04943, 0.05352,
  0.01171, 0.05837, 0.02717, 0.06207, 0.02720, 0.01289, 0.00839
  (mean 0.03741576759203537).
- per_item: 10 prompts (exp107_flip/ctrl_exp077_planet_2hop_0..9); every arm
  (base/v1/v2/rand0..rand7/bagg): dm = 0, margin_disp = 0.0 — zero decision
  flips and zero margin displacement on all 110 injected arms.
- meta.verdict "PENDING-METRIC" is the raw-record state minted before decision
  statistics; the final VERDICT: KILL is recorded in exp131_report.json.

Headline: KILL — decision-orthogonal amplifier (ĉ = 0.0374 < 0.1). The TGA
injection program's licensed hypothesis is refuted: the transient-growth
amplifier steers no decisions.
