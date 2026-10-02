# Archived Kaggle run logs

The raw console log of each Kaggle kernel run, unmodified, exactly as
`kaggle kernels output` returned it. Capture a log with
`scripts/archive_kernel_log.py` while that run is still the latest.
Kaggle serves only the current run (master standard §12.1).

| File | Kernel | Notebook | What it recorded |
| --- | --- | --- | --- |
| `kernel_v01_eda.log` | v1 | v1 | EDA: schema, score 0, drift, adversarial AUC 0.5004 |
| `kernel_v02_eda_v2.log` | v2 | v2 | Same measurements after the CRISP-DM narrative |
| `kernel_v01_baseline_f1.log` | modeling v1 | v1 | F1 CatBoost 0.957696, LightGBM 0.958331, promoted |
| `kernel_v02_versions_v2.log` | modeling v2 | v2 | Same vectors, bit-identical; library versions printed |
| `kernel_v03_e01_lightgbm.log` | modeling v3 | v3 | E01 control bit-identical; zero and capacity not promoted |
| `kernel_v03_eda_public.log` | eda v3 | v3 | Public EDA, roadmap sections removed; same measurements |
| `kernel_v04_e01_public.log` | modeling v4 | v4 | Public copy of E01; predictions bit-identical to v3 |
