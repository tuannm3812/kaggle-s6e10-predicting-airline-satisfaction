#!/usr/bin/env bash
# Push a notebook to its Kaggle kernel.
#
# Copies notebooks/<notebook> into notebooks/kernels/<target>/, then runs
# `kaggle kernels push`. The copy is gitignored.
#
# Usage: scripts/push_kaggle_kernel.sh <eda>
#
# The eda target expects notebooks/01_eda.ipynb and
# notebooks/kernels/eda/kernel-metadata.json. Neither exists until the
# EDA notebook is added.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
NOTEBOOKS_DIR="$REPO_ROOT/notebooks"

case "${1:-}" in
  eda)
    NOTEBOOK="01_eda.ipynb"
    KERNEL_DIR="$NOTEBOOKS_DIR/kernels/eda"
    ;;
  *)
    echo "Usage: $0 <eda>" >&2
    exit 1
    ;;
esac

if [ ! -f "$NOTEBOOKS_DIR/$NOTEBOOK" ]; then
  echo "Missing $NOTEBOOKS_DIR/$NOTEBOOK" >&2
  exit 1
fi
if [ ! -f "$KERNEL_DIR/kernel-metadata.json" ]; then
  echo "Missing $KERNEL_DIR/kernel-metadata.json" >&2
  exit 1
fi

if command -v kaggle >/dev/null 2>&1; then
  KAGGLE=kaggle
elif [ -x "/Users/tuannm3812/Library/Python/3.9/bin/kaggle" ]; then
  KAGGLE="/Users/tuannm3812/Library/Python/3.9/bin/kaggle"
else
  echo "kaggle CLI not found on PATH or at the known local install path." >&2
  exit 1
fi

cp "$NOTEBOOKS_DIR/$NOTEBOOK" "$KERNEL_DIR/$NOTEBOOK"
"$KAGGLE" kernels push -p "$KERNEL_DIR"
