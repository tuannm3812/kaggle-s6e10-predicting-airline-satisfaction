# Competition Instructions

**Competition:** [Playground Series S6E10 — Predicting Airline Satisfaction](https://www.kaggle.com/competitions/playground-series-s6e10)

## Verified facts

Read from the Kaggle API on **2026-10-02**. The competition page is
client-rendered, so Overview and Data prose have not been read verbatim.
Anything that can move is timestamped; re-check it before relying on it.

| Item | Value | Source |
|---|---|---|
| Competition ref | `playground-series-s6e10` | `kaggle competitions list` |
| Title | Predicting Airline Satisfaction | Kaggle API, 2026-10-02 |
| Category | Playground | Kaggle API, 2026-10-02 |
| Reward | Swag | Kaggle API, 2026-10-02 |
| **Deadline** | **2026-10-31 23:59 UTC** | Kaggle API, 2026-10-02 |
| Merger deadline | same as the final deadline | Kaggle API, 2026-10-02 |
| Teams entered | 307 | as of 2026-10-02 — will move |
| Joined | **Yes** (`user_has_entered: True`) | Kaggle API, 2026-10-02 |
| **Evaluation metric** | **ROC AUC** (`evaluation_metric = "Roc Auc Score"`) | Kaggle API, 2026-10-02 |
| Max daily submissions | 10 | Kaggle API, 2026-10-02 |
| Max team size | 3 | Kaggle API, 2026-10-02 |
| Kernels-only submissions | `False` — file upload permitted | Kaggle API, 2026-10-02 |
| Enabled | 2026-10-01 | Kaggle API, 2026-10-02 |

## Files

Downloaded into `data/` on **2026-10-02** and checked with pandas. The zip
and CSVs stay gitignored.

| File | Shape | Notes |
|---|---|---|
| `train.csv` | 699,635 × 23 | `id` + 21 features + `satisfaction` |
| `test.csv` | 299,844 × 22 | `id` + 21 features |
| `sample_submission.csv` | 299,844 × 2 | `id`, `satisfaction` (float) |

## Task

**Binary classification.** Predict the probability that `satisfaction` is
true. The train target is a boolean (`True` 310,339 / `False` 389,296,
positive rate 310,339 / 699,635). `sample_submission.csv` carries that
rate as a constant probability, not a label. Checked 2026-10-02: the
sample constant `0.4435727200611747` matches the ratio within
floating-point precision (about `5.55e-17` apart). They are not
bit-identical.

## Data (verified 2026-10-02)

- **Identifier:** `id`. Train `0..699634`, test `699635..999478`, both
  contiguous, no overlap, no duplicate ids.
- **No duplicate feature rows** in train or test (excluding `id` and,
  for train, the target).
- **Missing values:** `Arrival Delay in Minutes` only — 292 train, 130
  test. Every other column is complete.
- **Survey scores** are integers. Most run 0–5. `Baggage handling` runs
  1–5. A 0 is present on the other survey columns (wifi 1.87% of train,
  departure/arrival convenience 3.68%). Treat 0 as observed until EDA
  says otherwise.
- **Delays:** `Departure Delay in Minutes` is int, train 0–489, test
  0–480. `Arrival Delay in Minutes` is float, train 0–491, test 0–471.
  Test ranges sit inside train ranges.
- **Other numeric:** `Age` 7–85, `Flight Distance` 67–4983. Test ranges
  match train.

**Categorical features** — train and test vocabularies match:

| Feature | Levels (train counts) |
|---|---|
| `Gender` | Male 351,683 / Female 347,952 |
| `Customer Type` | Loyal Customer 576,990 / disloyal Customer 122,645 |
| `Type of Travel` | Business travel 497,441 / Personal Travel 202,194 |
| `Class` | Business 342,212 / Eco 327,404 / Eco Plus 30,019 |

## Submission format

Header `id,satisfaction`, 299,844 rows, `id` ascending from 699,635, one
probability per row.

```
id,satisfaction
699635,0.4435727200611747
699636,0.4435727200611747
```

`scripts/verify_submission.py` reads this schema from the official files.
It does not hardcode `id`.

## Submission mechanism

Not a Code Competition, so a file upload works. Master standard §11 still
applies: submit a completed kernel version so the score is tied to code
Kaggle has.

```bash
kaggle competitions submit \
  -c playground-series-s6e10 \
  -k tuannm3812/<kernel-slug> \
  -v <version> \
  -f submission.csv \
  -m "<description>"
```

Run `scripts/verify_submission.py` before that command.

## Still open

- [x] Download the three files into `data/` — **done** (2026-10-02).
- [x] Record shapes, columns, target, class balance, and the submission header.
- [ ] Quote Overview / Evaluation prose if it is ever pasted in.
- [ ] Identify any original source dataset and its licence before using it.
- [ ] EDA notebook. Nulls, the meaning of survey score 0, and class balance
      by `Class` / `Type of Travel` are the first questions.
