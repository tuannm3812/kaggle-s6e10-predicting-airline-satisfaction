#!/usr/bin/env python3
"""Validate a submission against sample_submission.csv and test.csv.

The prediction column is whatever sample_submission.csv carries besides
`id`. ROC AUC submissions must be finite probabilities in [0, 1].
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


def prediction_column(sample: pd.DataFrame) -> str:
    """Return the single non-id column in the official sample file.

    Args:
        sample: Official sample_submission.csv.

    Returns:
        The prediction column name.

    Raises:
        ValueError: If the schema is not `id` plus one prediction column.
    """
    columns = [name for name in sample.columns if name != "id"]
    if columns == [] or len(columns) != 1:
        raise ValueError(
            "Expected sample_submission.csv to have id plus one "
            f"prediction column, got {sample.columns.tolist()}"
        )
    return columns[0]


def validate_submission(
    submission_path: Path,
    test_path: Path,
    sample_path: Path,
) -> dict[str, int | float | str]:
    """Validate schema, id order, and probability range.

    Args:
        submission_path: Candidate submission CSV.
        test_path: Official test.csv, used for row count and id order.
        sample_path: Official sample_submission.csv, used for columns.

    Returns:
        Summary statistics of the validated predictions.

    Raises:
        ValueError: On any schema, id, or value-range violation.
    """
    submission = pd.read_csv(submission_path)
    test = pd.read_csv(test_path, usecols=["id"])
    sample = pd.read_csv(sample_path)
    expected_columns = sample.columns.tolist()
    if submission.columns.tolist() != expected_columns:
        raise ValueError(f"Expected columns {expected_columns}")
    if len(submission) != len(test):
        raise ValueError("Submission row count does not match test")
    if not submission["id"].equals(test["id"]):
        raise ValueError("Submission ids are not in test order")
    target = prediction_column(sample)
    predictions = submission[target].to_numpy(dtype=float)
    if not np.isfinite(predictions).all():
        raise ValueError("Predictions contain NaN or infinity")
    if not ((predictions >= 0.0) & (predictions <= 1.0)).all():
        raise ValueError("Predictions must be within [0, 1]")
    return {
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
