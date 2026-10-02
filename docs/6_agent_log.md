# Agent Collaboration Log

Append-only, per master standard §13. Correct a past entry by adding a new
one, never by rewriting it. Record what was checked, not just what was claimed.

## 2026-10-02 — Scaffold

- Empty local repo. No commits, no remote, no files.
- Competition already joined. API object read the same day: title
  Predicting Airline Satisfaction, metric `Roc Auc Score`, deadline
  2026-10-31 23:59 UTC, `is_kernels_submissions_only` false, 307 teams,
  daily cap 10. File names and byte sizes from `kaggle competitions files`.
- **Not checked:** CSV headers, row counts, target name, class balance.
  Those stay unknown in `docs/1_instructions.md`.
- Portfolio card and the EDA notebook were left for a later decision.

## 2026-10-02 — Independent review of Cursor scaffold

Reviewed commit `0197c0e` against the master standard and the current S6E9
workflow. The worktree was clean and the commit was coherent: repository
shape, zero-padded future notebook names, append-only log, gitignore rules,
Kaggle-only trusted execution, and the explicit unknown-data boundary all
match the declared standards. `bash -n` passed for the push helper,
`py_compile` passed for the submission verifier after redirecting Python's
bytecode cache to `/private/tmp`, and `git show --check` reported no errors.

Two follow-ups remain:

1. **Confirmed schema defect — fix after the files are downloaded and before
   the verifier is relied on.** `scripts/verify_submission.py` assumes the
   identifier is named `id` in its docstring, `usecols`, column selection,
   and order check. That contradicts `docs/0_coding_standards.md` and
   `docs/1_instructions.md`, which correctly say no row id is known yet. A
   synthetic `id`-based sample passed; the same valid two-column shape with
   `passenger_key` as the identifier failed at `read_csv` with
   `ValueError: Usecols do not match columns`. Do not guess the replacement
   name. Read the official files, record the schema, then specialize the
   verifier or derive the identifier from the verified sample/test schema.
2. **Run-evidence workflow gap — close before a second kernel push.** This
   project's standards say to save each run log before the next push, but
   the scaffold has no archive helper or archive manifest. S6E9 added
   `scripts/archive_kernel_log.py` and `assets/kernel_logs/README.md` only
   after losing the logs for kernel versions 1–8; the master standard now
   carries that lesson in §12.1. Adapt that workflow before one S6E10 run can
   overwrite another. This is not blocking the initial scaffold or first
   EDA run, but it is blocking evidence-safe iteration after that run.

Non-blocking: `scripts/push_kaggle_kernel.sh` retains S6E9's personal
`/Users/tuannm3812/.../kaggle` fallback. It works on this machine and is not
inside an uploaded notebook or metadata file, but resolving the CLI from
`PATH` or a configurable environment variable would make the helper portable.

**Not re-checked in this review:** live Kaggle API facts or CSV contents. No
data was downloaded, so the original entry's unknowns remain unknown rather
than being inferred.

## 2026-10-02 — Schema recorded, verifier no longer assumes `id`

Follow-up 1 from the review above.

- Downloaded `playground-series-s6e10.zip` into `data/` (gitignored) and
  read all three CSVs. **Checked:** train 699,635 × 23, test 299,844 × 22,
  sample 299,844 × 2. The shared identifier is `id`. The only train-only
  column is boolean `satisfaction` (310,339 true / 389,296 false). The
  sample probability is constant and equals 310,339 / 699,635.
- **Checked:** the only nulls are `Arrival Delay in Minutes` (292 train,
  130 test). No duplicate feature rows. Test numeric ranges sit inside
  train ranges. Categorical vocabularies match.
- `scripts/verify_submission.py` now takes the identifier as the single
  column shared by `sample_submission.csv` and `test.csv`. **Checked:**
  the official sample passes against the official test; a copy whose
  identifier is renamed `passenger_key` in both files also passes; the
  old `usecols=["id"]` path is gone. A one-row id mismatch raises
  `ValueError`.
- Follow-up 2 is still open: no kernel-log archive helper yet. The review
  says that blocks a second kernel push, not the first EDA run.

## 2026-10-02 — Review of schema fix and public-kernel diagnosis

Reviewed Cursor commit `51dbc1f`. The official sample passes the revised
verifier, a synthetic schema whose identifier is renamed to
`passenger_key` also passes, and a mismatched identifier order is rejected.
The recorded shapes, target counts, missing-value counts, duplicate checks,
id ranges, categorical vocabularies, and selected numeric ranges were
recomputed from the gitignored CSVs and reproduced. `git show --check`
reported no commit-format errors, and only `data/README.md` is tracked under
`data/`.

One low-severity wording correction: the sample constant is
`0.4435727200611747`, while the exact integer ratio represented as a Python
float is `0.44357272006117476`; the difference is about `5.55e-17`. They
match to the stored decimal precision but are not bit-identical, so future
text should say "matches within floating-point precision" rather than
"equals". This does not affect the verifier or modeling.

**Why no public Kaggle kernel can be run from this repo yet:** this is a
missing-artifact state, not a Kaggle public-kernel restriction or a failed
remote run.

- A live competition-kernel query returned public S6E10 notebooks, and live
  status checks found `evgendvorkin/lightgbm-cv-5-folds-0-96047` and
  `kospintr/airline-lgbm-catb-xgb-hgbc-baseline` `COMPLETE`. Public execution
  with this competition source is therefore supported.
- A live account query found no S6E10 kernel owned by `tuannm3812`; there is
  consequently no failed S6E10 run or remote error log to inspect.
- Locally, `notebooks/01_eda.ipynb` does not exist and neither does
  `notebooks/kernels/eda/kernel-metadata.json`. Running
  `bash scripts/push_kaggle_kernel.sh eda` reproducibly stops at the first
  preflight check with `Missing .../notebooks/01_eda.ipynb`.
- S6E8/S6E9 public kernels contain both artifacts and set
  `is_private: false`, `enable_internet: false`, and
  `competition_sources: ["playground-series-s6eN"]`. S6E10 needs the same
  pattern after the EDA notebook is authored. The current project standard
  defaults kernels to private, so making this one public also needs an
  explicit project decision and should keep forward strategy out of the
  public notebook, following S6E9.

No notebook or kernel metadata was created in this review; the user asked
for diagnosis and review, not implementation or publication.
