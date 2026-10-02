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

@docs/1_instructions.md — joined on 2026-10-02. Metric is **ROC AUC**.
Files were read the same day: target `satisfaction` (boolean, 44.36%
positive), identifier `id`, submission is one probability per test row.

## Deltas from the master

- Notebooks are authored locally and **executed on Kaggle**. Local runs are
  smoke checks only.
- `data/` and `predictions/` exist for the Kaggle CLI and are gitignored.
- Notebook names are zero-padded (`01_eda.ipynb`) so later inserts do not
  renumber them. Declared here on day one.

## Evidence locations

- `docs/1_instructions.md` — task, metric, deadline, submission mechanism
- `docs/2_eda_insights.md` — kernel v1 findings
- `docs/3_implementation_plan.md` — fold F1, recipe, and the promotion rule
- `docs/4_experiment_ledger.md` — every comparable run
- `docs/5_submission_manifest.md` — leaderboard files
- `docs/6_agent_log.md` — append-only session log; start here to catch up

## Current state

- Champion LightGBM, F1 OOF AUC 0.958331. Public score 0.95790 on
  2026-10-03, submission 56775984, modeling kernel v3. See
  `docs/4_experiment_ledger.md` and `docs/5_submission_manifest.md`.
- E01 did not promote the zero-indicator arm or the 2,000-tree arm.
  The control refit is bit-identical to B01.

## Open risks

- Archive the kernel log after every run, before the next push. Kaggle
  keeps only the latest log (master §12.1).
- Public notebooks stay CPU-only and internet-disabled, and they carry
  findings rather than a forward plan. The EDA kernel is public. The
  modeling kernel stays private until its public copy is pushed.
- Mutable facts — leaderboard, public notebooks, quotas — must be re-checked
  live, never recalled.
