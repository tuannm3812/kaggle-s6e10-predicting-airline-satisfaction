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

## 2026-10-02 — EDA kernel v1, CPU, private

Follow-up from the review above: the missing notebook was the blocker.

- Authored `notebooks/01_eda.ipynb` and private CPU metadata
  `tuannm3812/airline-satisfaction-eda`. Internet disabled. GPU left off:
  the job is pandas, a few plots, and one subsample classifier.
- Pushed kernel version 1. Status reached `COMPLETE`. **Checked** against
  `assets/kernel_logs/kernel_v01_eda.log`: shapes and the 310,339 positive
  count match the local read; sample-versus-rate gap is `5.551e-17`;
  arrival-delay nulls are 292 / 130; adversarial OOF AUC 0.5004 on the
  declared 200,000-row subsample; self-export wrote 24 cells, 11 with
  outputs, 3 figures, 0 errors.
- Log archived before any later push. PDF render is the next local step
  and uses that self-export, not a local re-run.
- The kernel stays private. Public release was not requested.

## 2026-10-02 — Independent review of EDA v1 and render path

Reviewed commits `f649226`, `1a075c4`, and `d981699` as one workflow.
The live kernel `tuannm3812/airline-satisfaction-eda` was re-checked and is
`COMPLETE`; pulled metadata confirms private, CPU, TPU off, internet off,
and competition source `playground-series-s6e10`. After normalizing
Kaggle's string-versus-list representation of cell source, the committed
notebook, live pulled source, and v1 self-export have identical cell text.
The committed notebook is valid nbformat 4.5 and output-free; the self-export
is valid and has outputs on 11 code cells.

The archived log supports the numbers in `docs/2_eda_insights.md`: mounted
shapes, target count, null counts, score-0 rates, category rates, top
univariate AUC, maximum drift statistic, adversarial AUC, and duplicate
count all match. The log spans about 31 seconds between its first and last
entries (about 41 seconds from worker start), consistent with the documented
"about 40 seconds". The notebook is a proportionate EDA rather than a model
sweep.

Fresh validation passed for Python compilation, shell syntax, notebook JSON,
and the official submission verifier. The render command completed all nine
current PDFs after `d981699`; all 11 pages of the executed-notebook PDF and
the EDA-insights PDF were rendered to PNG and visually checked. Charts, code,
headers, footers, and page breaks are legible with no clipping or overlap.

Two workflow defects remain:

1. **Fix before the next log archive — the version check is inert for this
   notebook.** `scripts/archive_kernel_log.py` searches only for a JSON
   fragment such as `"notebook_version": "v1"`, but the actual EDA log
   stamps plain text `NOTEBOOK_VERSION v1`. Re-running the helper's regex
   against `kernel_v01_eda.log` returns no matches, while a regex for the
   plain stamp returns `v1`. The helper therefore copies a fetched log under
   any caller-supplied version without checking or even warning, recreating
   the mislabeling risk it was added to prevent. Make the notebook emit the
   structured stamp the helper expects or teach the helper both formats;
   reject a mismatch before copying rather than asking for a manual check.
2. **Fix before adding `02_modeling.ipynb` — render evidence is not scoped to
   a notebook.** In `scripts/render_pdf.py`, `--executed-notebook` and
   `--kernel-log` are passed to every `notebooks/*.ipynb`. With the planned
   second notebook, one EDA self-export/log would be rendered under both the
   EDA and modeling filenames. S6E9 scoped these arguments to one notebook;
   S6E10 needs an explicit notebook-to-evidence association rather than the
   current global application. The current render is correct only because
   there is exactly one notebook.

Non-blocking hygiene: `git diff 51dbc1f..HEAD --check` reports CRLF/trailing
whitespace throughout the vendored `assets/fonts/dm-sans/OFL.txt`; the theme
metadata still says `S6E9 Project`, and the renderer's opening history still
mentions the superseded headless-Chrome path. These do not affect the v1 run
or current PDFs, but should be cleaned when the render code is next touched.

No notebook logic, kernel, or helper was changed by this review.

## 2026-10-02 — CRISP-DM EDA structure and Cursor handoff

The user approved a bounded structural revision of the EDA notebook and the
existing two-folder iCloud layout.

- Reorganized `notebooks/01_eda.ipynb` into a lightweight CRISP-DM narrative:
  Business Understanding, Data Understanding, Data Preparation Implications,
  Modeling Implications, and Evaluation and Next Steps. Deployment is defined
  as the later verified Kaggle submission rather than padded into the EDA.
- Added modeling implications grounded in v1 evidence: CatBoost as the primary
  baseline, one gradient-boosting challenger, fixed stratified folds, fold-safe
  learned transforms, no drift correction, and no broad model zoo.
- Analytical code is unchanged. The only code-cell edit is
  `NOTEBOOK_VERSION = "v2"`, reserving the next trusted Kaggle run for this
  narrative revision. The committed notebook remains output-free.
- Clarified the render/export contract in `docs/0_coding_standards.md`: both
  `renders/` and the repo's iCloud export contain exactly `docs/` and
  `notebooks/`. The current renderer already implements this split, so no
  export code changed.

**Cursor handoff — work and run in this order:**

1. Fix the archive-version guard identified in the preceding review before
   pushing v2. The notebook may emit a structured JSON stamp, or the helper
   may recognize both JSON and `NOTEBOOK_VERSION vN`; a mismatch must stop
   before copying the log. Add a local regression check using
   `assets/kernel_logs/kernel_v01_eda.log`.
2. Validate notebook JSON, confirm outputs and execution counts are clear,
   and confirm the only code change from v1 is the version stamp (plus any
   structured run-summary stamp needed by step 1).
3. Push the existing private CPU, internet-disabled EDA kernel with
   `bash scripts/push_kaggle_kernel.sh eda`; do not make it public without a
   separate decision. Wait for `COMPLETE` and inspect the run output.
4. Archive the v2 log immediately, before any later push. Confirm the helper
   proves the fetched log reports v2. Then fetch the v2 self-export and verify
   its source matches the committed notebook and its cells have no errors.
5. Render into the two local folders with the v2 self-export and archived v2
   log, visually inspect the PDFs, then use `--export` to mirror exactly
   `docs/` and `notebooks/` to iCloud.
6. Append the v2 run evidence here and update `docs/2_eda_insights.md` only if
   outputs differ. Keep the v1 evidence and history visible; do not rewrite
   earlier log entries.

The renderer's multi-notebook evidence-scoping defect does not block this
single-notebook v2 run, but it must be fixed before `02_modeling.ipynb` is
added or rendered.

## 2026-10-02 — EDA kernel v2, narrative only

Followed the handoff above.

- Archive guard: `--self-check` accepts `kernel_v01_eda.log` as v1, rejects
  it as v2, and accepts a JSON `"notebook_version": "v3"` stamp. **Checked**
  before the push.
- Code-cell diff against v1 is only `NOTEBOOK_VERSION = "v2"`. Committed
  notebook is output-free.
- Pushed private CPU kernel version 2. Status `COMPLETE`.
- `archive_kernel_log.py 2 eda_v2` printed `the log reports notebook version
  v2` and wrote `assets/kernel_logs/kernel_v02_eda_v2.log` before any later
  push.
- Self-export has 26 cells, source matches the committed notebook, 0 errors.
- Stdout matches v1 except the self-export line (26 cells / 232 KB versus
  24 cells / 228 KB). `docs/2_eda_insights.md` was not revised.
- Render and iCloud export follow this entry. The multi-notebook render
  scoping defect is still open and still blocks `02_modeling.ipynb`.
