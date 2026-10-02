# Submission Manifest

## S01 — LightGBM champion

| Field | Value |
| --- | --- |
| Date | 2026-10-03 |
| Competition | `playground-series-s6e10` |
| Kernel | `tuannm3812/airline-satisfaction-modeling` version 3 |
| Notebook | `notebooks/02_modeling.ipynb` v3 |
| File | `submission.csv` from that completed run |
| Description | LightGBM champion, 500 trees, F1 OOF 0.958331 |
| Kaggle ref | 56775984 |
| Status | `SubmissionStatus.COMPLETE` |
| Public score | 0.95790 |
| Private score | not returned |

The file is the E01 control, which is the B01 LightGBM champion.
`scripts/verify_submission.py` passed before the submit call, and the
file is byte-identical to the modeling kernel v2 submission. E01 did
not promote a new arm (`docs/4_experiment_ledger.md`).

Selected with `kaggle competitions submit -k tuannm3812/airline-satisfaction-modeling -v 3 -f submission.csv`.
Nine submissions remained afterward.
