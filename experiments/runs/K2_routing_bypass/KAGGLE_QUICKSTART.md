# K2 on Kaggle — quickstart
1. Upload `K2_kaggle_run.ipynb` to Kaggle as a new notebook.
2. Right panel: Accelerator → **GPU T4 x2**. Notebook Settings → **Internet ON**.
3. New Kaggle account? Complete **phone verification** first, or no GPU quota appears.
4. **Run all cells** top to bottom, in order — do not skip or reorder.
5. If any cell raises STOP, halt there — do not force past it; send the named files back.
6. Expect a few minutes of GPU (180 forward passes, ~2–5 min on 2×T4).
7. When done, open the `outputs/` folder in the notebook's file browser.
8. Download: `k2_results.json`, `k2_instance_records.json`, `k2_run_log.txt`, `k2_preexec_report.json`.
9. Copy the SHA-256 lines printed by the last cell and send them with the files.
10. Copy the `AUTHORITATIVE RULING` block (row + both verdicts) verbatim into chat.
