# Predicting Airline Satisfaction

[![Kaggle Competition](https://img.shields.io/badge/Kaggle-Playground%20Series%20S6E10-20BEFF?logo=kaggle&logoColor=white)](https://www.kaggle.com/competitions/playground-series-s6e10)
[![Python](https://img.shields.io/badge/Python-3-3776AB?logo=python&logoColor=white)](requirements.txt)

Kaggle Playground Series S6E10:
https://www.kaggle.com/competitions/playground-series-s6e10

Notebook-first workflow. Notebooks are the executable source of truth;
`docs/` records rationale, validation, and submission evidence.

## Status

**EDA complete on Kaggle (kernel v1, 2026-10-02).** No model score yet.

- Task: probability that `satisfaction` is true.
- Metric: **ROC AUC** (Kaggle API, 2026-10-02).
- Train 699,635 rows; test 299,844 rows. Positive rate 44.36%.
- Deadline: **2026-10-31 23:59 UTC**.
- Detail: [`docs/1_instructions.md`](docs/1_instructions.md).

## Getting started

```bash
# Join first, or the download 403s. This account has already joined.
kaggle competitions download -c playground-series-s6e10 -p data/
unzip -o 'data/*.zip' -d data/
```

Notebooks, once they exist, are authored locally and executed on Kaggle:

```bash
bash scripts/push_kaggle_kernel.sh eda
kaggle kernels status tuannm3812/<kernel-slug>
kaggle kernels output tuannm3812/<kernel-slug> -p out/
```

## Repository layout

- [`docs/`](docs/) — coding standards, competition instructions, and the
  append-only agent log. EDA, the plan, the ledger, and the submission
  manifest will occupy `docs/2`–`docs/5`.
- [`notebooks/`](notebooks/) — executable workflow. Empty until the first
  notebook.
- [`scripts/`](scripts/) — `push_kaggle_kernel.sh` and
  `verify_submission.py`.
- `data/`, `predictions/` — local and generated, gitignored.
