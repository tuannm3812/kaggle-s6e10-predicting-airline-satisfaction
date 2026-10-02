# Coding Standards

## Baseline

This project follows the shared
`coding-standards/coding_standards.md` at
`~/Documents/GitHub/coding-standards/` as its baseline. That file is the
fallback for anything not overridden below.

Everything in this file is a project-specific addition or an explicit
override. Do not copy the shared standard into this file.

## Repository scope

Notebook-first Kaggle workflow, matching
`kaggle-s6e9-predicting-electric-vehicle-purchases`:

- `notebooks/` — executable workflow, plus `notebooks/kernels/<name>/`
  holding each notebook's Kaggle `kernel-metadata.json`.
- `docs/` — durable findings, numbered per master standard §2 (Shape A).
- `scripts/` — CLI helpers only. No modeling logic.
- `data/` — local competition files. **Gitignored.**
- `predictions/` — OOF and test matrices. **Gitignored.**

`data/` and `predictions/` exist because this project uses the Kaggle CLI
locally. They stay out of git (master §8).

**Notebook names are zero-padded** (`01_eda.ipynb`, not `1_eda.ipynb`).
Declared on 2026-10-02, before any notebook exists, so the names never
need a later rename. Master §2's unpadded examples still apply to docs.

`docs/6_agent_log.md` is reserved from the start. Slots 2–5 stay open for
EDA insights, the implementation plan, the experiment ledger, and the
submission manifest. Do not renumber the log when those files appear.

## Execution environment

Notebooks are authored locally and **executed on Kaggle**:

```bash
bash scripts/push_kaggle_kernel.sh <target>
kaggle kernels status tuannm3812/<kernel-slug>
kaggle kernels output tuannm3812/<kernel-slug> -p out/
```

The trusted run behind any committed output or ledger row is the Kaggle
kernel run. Local execution is for syntax and smoke checks.

Kernels stay private, CPU-only, and internet-disabled unless a later
decision says otherwise (master §12). Save the run log before the next
push — Kaggle keeps only the latest run (master §12.1).

## Validation

- Fixed folds, defined once and reused, so OOF predictions align.
- Any transform that touches the target fits inside the fold (master §5).
- Record the fold definition the first time it is used.
- A new champion needs a paired comparison on aligned OOF predictions,
  with the criterion stated before the run. Record non-promotions too.

The identifier is `id` and the target is boolean `satisfaction`, both
recorded in `docs/1_instructions.md` on 2026-10-02. No group key has been
established; do not invent one. The verifier derives the identifier from
the official sample and test headers rather than hardcoding `id`.

## Submissions

- Submit from a completed kernel version (master §11), even though this
  competition allows file upload (`is_kernels_submissions_only = False`,
  Kaggle API, 2026-10-02).
- Run `scripts/verify_submission.py` against `sample_submission.csv`
  before every submission.
- Record every submission in `docs/5_submission_manifest.md` once that
  file exists. Never let a scored submission go unrecorded.

## Device

EDA runs on CPU. GPU stays off until a model run has a reason to screen
with it. S6E9 measured CatBoost GPU as faster and not bit-reproducible,
so a GPU result is a separate comparability class and is not promoted
on its own.

## Kernels stay private until a publication decision

The EDA kernel is private, CPU-only, and internet-disabled. Codex noted
on 2026-10-02 that S6E8 and S6E9 published public kernels, and that
making this one public is a separate decision. A later public notebook
carries findings, not a forward plan.

## Run logs and rendered PDFs

After every kernel run, before the next push:

```bash
python3 scripts/archive_kernel_log.py <version> <label> --kernel eda
```

`scripts/render_pdf.py --executed-notebook <self-export> --export` writes
PDFs under `renders/` (gitignored) and mirrors them to iCloud at
`05_Projects/Kaggle/<repo>/`. Keep exactly two subfolders in both locations:
`docs/` and `notebooks/`. Documentation collections and run-log evidence go
under `docs/`; notebook renders go under `notebooks/`. The self-export is the
copy of `/kaggle/working/__notebook__.ipynb` made by the notebook's last cell.
Do not execute the modeling path locally to manufacture those outputs.
