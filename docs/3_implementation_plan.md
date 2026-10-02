# Implementation Plan

Written **2026-10-02**, before any model fit. Deadline **2026-10-31
23:59 UTC**. This file is the predeclaration. Results go in
`docs/4_experiment_ledger.md` after the run, not here.

## What the EDA settled

From kernel v2, recorded in `docs/2_eda_insights.md`:

- ROC AUC, boolean `satisfaction`, 699,635 train rows, 299,844 test rows.
- No group key. `id` is an alignment key.
- Survey score 0 stays an observed value. Do not recode it to missing.
- Arrival delay is the only missing column (292 train, 130 test).
- Train and test look interchangeable (adversarial AUC 0.5004 on a
  200,000-row subsample). No drift correction.
- Strong descriptive signals: `Class`, `Type of Travel`, `Online boarding`.

## Fold definition F1

`StratifiedKFold(n_splits=5, shuffle=True, random_state=42)` on the
boolean target. Every comparable model uses these folds. An OOF vector
from any other split is not comparable to an F1 vector.

## Feature recipe

One recipe for train and test:

- Drop `id`.
- Add `arrival_delay_missing` from the raw null mask. That mask is a
  property of the row, not a fit.
- Impute `Arrival Delay in Minutes` with the training-fold median. Fit
  the median inside the fold. Each test prediction uses the median from
  the fold that produced it, then the five test vectors are averaged.
- Leave survey zeros unchanged.
- Pass `Gender`, `Customer Type`, `Type of Travel`, and `Class` as
  categoricals. Other columns stay numeric.

## Phase 2 — first comparable pair

Notebook `notebooks/02_modeling.ipynb`, private CPU kernel, internet
disabled. Shared tree budget, stated here before the fit:

| Model | Role | Settings |
| --- | --- | --- |
| CatBoost | Standing baseline | 500 iterations, learning rate 0.05, depth 6, Logloss, `task_type="CPU"`, seed 42 |
| LightGBM | One challenger | 500 trees, learning rate 0.05, otherwise library defaults, seed 42 |

No third family, no sweep, and no GPU in this phase.

## Promotion rule

Also stated before the fit. LightGBM replaces CatBoost as the champion
only when both are true on F1:

1. Its overall OOF ROC AUC is higher.
2. The mean of the five paired fold differences (LightGBM minus
   CatBoost) is at least **0.0005**.

Otherwise CatBoost remains the champion, and the LightGBM numbers are
still recorded. The test file written for later verification uses the
champion's averaged fold predictions. This phase does not submit that
file to the leaderboard.

## After the run

Archive the kernel log before the next push. Render with
`--notebook 02_modeling`. Run `scripts/verify_submission.py` on the
champion file. A leaderboard submission waits until that check passes
and is a separate decision.
