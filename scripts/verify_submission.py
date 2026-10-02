#!/usr/bin/env python3
"""Validate a submission against sample_submission.csv and test.csv.

The identifier is the single column shared by those two official files.
The prediction column is the other sample column. ROC AUC submissions
must be finite probabilities in [0, 1].
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


def schema_columns(
    sample: pd.DataFrame,
    test_columns: list[str],
) -> tuple[str, str]:
    """Derive the identifier and prediction column from official files.

    Args:
        sample: Official sample_submission.csv.
        test_columns: Column names from official test.csv.

    Returns:
        The identifier name, then the prediction-column name.

    Raises:
        ValueError: If the files are not one shared identifier plus one
            prediction column.
    """
    shared = [name for name in sample.columns if name in test_columns]
    predicted = [name for name in sample.columns if name not in shared]
    if len(sample.columns) != 2 or len(shared) != 1 or len(predicted) != 1:
        raise ValueError(
            "Expected sample_submission.csv to have one identifier "
            "shared with test.csv and one prediction column; "
            f"sample columns are {sample.columns.tolist()}, "
            f"shared columns are {shared}"
        )
    return shared[0], predicted[0]


def validate_submission(
    submission_path: Path,
    test_path: Path,
    sample_path: Path,
) -> dict[str, int | float | str]:
    """Validate schema, identifier order, and probability range.

    Args:
        submission_path: Candidate submission CSV.
        test_path: Official test.csv, used for row count and id order.
        sample_path: Official sample_submission.csv, used for columns.

    Returns:
        Summary statistics of the validated predictions.

    Raises:
        ValueError: On any schema, identifier, or value-range violation.
    """
    submission = pd.read_csv(submission_path)
    sample = pd.read_csv(sample_path)
    test_columns = pd.read_csv(test_path, nrows=0).columns.tolist()
    identifier, target = schema_columns(sample, test_columns)
    test_ids = pd.read_csv(test_path, usecols=[identifier])
    expected_columns = sample.columns.tolist()
    if submission.columns.tolist() != expected_columns:
        raise ValueError(f"Expected columns {expected_columns}")
    if len(submission) != len(test_ids):
        raise ValueError("Submission row count does not match test")
    if not submission[identifier].equals(test_ids[identifier]):
        raise ValueError("Submission identifiers are not in test order")
    predictions = submission[target].to_numpy(dtype=float)
    if not np.isfinite(predictions).all():
        raise ValueError("Predictions contain NaN or infinity")
    if not ((predictions >= 0.0) & (predictions <= 1.0)).all():
        raise ValueError("Predictions must be within [0, 1]")
    return {
        "identifier": identifier,
        "target": target,
        "rows": len(submission),
        "unique_predictions": int(np.unique(predictions).size),
        "minimum": float(predictions.min()),
        "maximum": float(predictions.max()),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("submission", type=Path)
    parser.add_argument("--test", type=Path, default=Path("data/test.csv"))
    parser.add_argument(
        "--sample",
        type=Path,
        default=Path("data/sample_submission.csv"),
    )
    args = parser.parse_args()
    print(validate_submission(args.submission, args.test, args.sample))


if __name__ == "__main__":
    main()
