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

## E01 — zero indicators against capacity

Written **2026-10-03**, before the E01 fit. B01 already promoted
LightGBM (F1 OOF AUC 0.958331). CatBoost OOF correlates 0.997415 with
that champion, so this phase does not blend them and does not refit
CatBoost.

Same fold definition F1. Same arrival-delay recipe. Survey zeros stay
observed scores. Three LightGBM fits, seed 42, learning rate 0.05,
otherwise library defaults, `n_jobs=-1`:

| Arm | Features | Trees |
| --- | --- | --- |
| `lightgbm_control` | B01 champion recipe | 500 |
| `lightgbm_zero` | Control, plus one `__is_zero` indicator per survey column that contains 0 | 500 |
| `lightgbm_capacity` | Control features, no zero indicators | 2,000 |

The indicator columns, named here before the fit, are `Inflight wifi
service`, `Departure/Arrival time convenient`, `Ease of Online booking`,
`Gate location`, `Food and drink`, `Online boarding`, `Seat comfort`,
`Inflight entertainment`, `On-board service`, `Leg room service`,
`Checkin service`, and `Cleanliness`. Each indicator is
`(score == 0)` on that row. `Baggage handling` is excluded because its
minimum is 1. Delay columns are excluded because 0 is a measured delay,
not a survey code. Indicators are not fit inside the fold.

An arm replaces the control only when both are true on this run's
aligned F1 predictions:

1. Its overall OOF ROC AUC is higher than `lightgbm_control`.
2. The mean of the five paired fold differences (arm minus control) is
   at least **0.0005**.

If both arms clear that bar, the higher overall OOF AUC is the
candidate. If neither clears it, the standing champion stays the B01
LightGBM file.

The control is a refit of B01, not a new model. After the kernel
finishes, compare `oof_lightgbm_control.npy` with
`predictions/oof_lightgbm.npy`. Promotion of either new arm is void
unless that comparison is bit-identical. A mismatch stops a new
submission; the already verified B01 file remains the champion.

No GPU. The kernel stays private until the gate is recorded. One
leaderboard file is submitted after `scripts/verify_submission.py`
passes: the gated candidate, or the standing B01 file if neither arm
clears the bar.
