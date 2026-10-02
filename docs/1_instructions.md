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

## Files (names and sizes only)

From `kaggle competitions files` on 2026-10-02. Contents are not downloaded,
so shapes, columns, and the target name are unknown.

| File | Size | Created |
|---|---|---|
| `train.csv` | 67,245,068 bytes | 2026-08-26 |
| `test.csv` | 27,200,964 bytes | 2026-08-26 |
| `sample_submission.csv` | 8,095,804 bytes | 2026-08-26 |

## Task

**Score probabilities with ROC AUC.** The positive class, the target column,
and the submission header are not known until `sample_submission.csv` and
`train.csv` are read. Do not guess them from the competition title.

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

- [ ] Download the three files into `data/` (gitignored).
- [ ] Record shapes, columns, target, class balance, and the submission header.
- [ ] Quote Overview / Evaluation prose if it is ever pasted in.
- [ ] Identify any original source dataset and its licence before using it.
