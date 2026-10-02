# kaggle-s6e10-predicting-airline-satisfaction

Kaggle Playground Series S6E10 — predicting airline satisfaction. Deadline
**2026-10-31 23:59 UTC**. Notebook-first: notebooks in `notebooks/` are the
executable source of truth, `docs/` carries the reasoning.

This is a Playground competition, not a research project. Prefer a small
number of well-validated models over breadth.

## Standards

Follow the master standard at `~/Documents/GitHub/coding-standards/`.
Project-specific rules and deliberate overrides: @docs/0_coding_standards.md

## Read before changing anything

@docs/1_instructions.md — joined and API facts recorded on 2026-10-02.
Metric is **ROC AUC**. Column names, the target, and row counts are not
verified until the files are downloaded. Do not invent them.

## Deltas from the master

- Notebooks are authored locally and **executed on Kaggle**. Local runs are
  smoke checks only.
- `data/` and `predictions/` exist for the Kaggle CLI and are gitignored.
- Notebook names are zero-padded (`01_eda.ipynb`) so later inserts do not
  renumber them. Declared here on day one.

## Evidence locations

- `docs/1_instructions.md` — task, metric, deadline, submission mechanism
- `docs/6_agent_log.md` — append-only session log; start here to catch up

EDA, the plan, the ledger, and the submission manifest do not exist yet.
Add them as `docs/2`–`docs/5` when that work happens. Do not renumber the log.

## Current state

- Scaffold only, 2026-10-02. No data download, no notebook, no score.

## Open risks

- Target column and submission schema are unknown until `data/` is read.
- Mutable facts — leaderboard, public notebooks, quotas — must be re-checked
  live, never recalled.
