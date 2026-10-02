# Experiment Ledger

Fold definition F1: `StratifiedKFold(5, shuffle=True, random_state=42)`
on boolean `satisfaction`. The promotion rule was committed in
`docs/3_implementation_plan.md` before this run.

## B01 — CatBoost baseline and LightGBM challenger

Kaggle kernel `tuannm3812/airline-satisfaction-modeling` version 1,
notebook v1, private CPU, internet disabled. Completed 2026-10-02.
Log: `assets/kernel_logs/kernel_v01_baseline_f1.log`.

Shared budget: 500 trees, learning rate 0.05. CatBoost depth 6,
`task_type="CPU"`. LightGBM otherwise at library defaults. Arrival-delay
median fit inside each fold; the five fold medians were all 0.

| Model | Role | Fold AUCs | OOF AUC | Seconds |
| --- | --- | --- | --- | --- |
| CatBoost | Standing baseline | 0.957694, 0.956519, 0.958526, 0.957743, 0.958041 | 0.957696 | 380.2 |
| LightGBM | Challenger | 0.958354, 0.957139, 0.959047, 0.958410, 0.958740 | 0.958331 | 71.4 |

Mean paired fold gap (LightGBM minus CatBoost) **0.000633**. The
predeclared bar was 0.0005, and LightGBM's overall OOF AUC is higher.
**LightGBM is the champion.** CatBoost is recorded and not promoted.

`scripts/verify_submission.py` passed on the champion `submission.csv`:
299,844 rows, probabilities from 0.003021 to 0.989561, 299,589 unique
values. The file was not submitted to the leaderboard.

B01 printed Python, NumPy, and pandas only. LightGBM and CatBoost
versions for that run were not captured. Do not backfill them.

## R1 — same pair, library versions printed

Modeling kernel version 2, notebook v2, 2026-10-02. The only code change
from B01 is the version stamp and the version print. Log:
`assets/kernel_logs/kernel_v02_versions_v2.log`.

Printed on the worker: Python 3.12.13, numpy 2.0.2, pandas 2.3.3,
scikit-learn 1.6.1, lightgbm 4.6.0, catboost 1.2.10.

OOF and test vectors are bit-identical to B01 (`np.array_equal` on all
four arrays, max absolute difference 0). The promotion stands. This row
identifies the libraries; it does not replace B01's score.

## E01 — zero indicators and capacity

Modeling kernel version 3, notebook v3, 2026-10-03. Private CPU,
internet disabled. Log: `assets/kernel_logs/kernel_v03_e01_lightgbm.log`.
The rule was committed in `docs/3_implementation_plan.md` before the
push. CatBoost was not refit.

| Arm | Trees | Fold AUCs | OOF AUC | Mean gap vs control | Seconds |
| --- | --- | --- | --- | --- | --- |
| `lightgbm_control` | 500 | 0.958354, 0.957139, 0.959047, 0.958410, 0.958740 | 0.958331 | — | 101.0 |
| `lightgbm_zero` | 500 | 0.958364, 0.957139, 0.959020, 0.958410, 0.958740 | 0.958328 | −0.000004 | 101.4 |
| `lightgbm_capacity` | 2,000 | 0.958507, 0.957169, 0.959000, 0.958352, 0.958580 | 0.958315 | −0.000017 | 345.5 |

The promotion bar was a higher OOF AUC and a mean paired gap of at
least 0.0005. Neither arm cleared it. **The champion stays B01
LightGBM.**

`oof_lightgbm_control.npy` and `test_lightgbm_control.npy` are
bit-identical to the B01 LightGBM arrays (`np.array_equal`, max
absolute difference 0). The control refit does not replace B01's row.
`submission.csv` from this run is byte-identical to the R1 file and
passed `scripts/verify_submission.py` again: 299,844 rows, probabilities
from 0.003021 to 0.989561, 299,589 unique values.
