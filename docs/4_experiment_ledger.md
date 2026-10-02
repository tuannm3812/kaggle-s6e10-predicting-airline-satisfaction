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
