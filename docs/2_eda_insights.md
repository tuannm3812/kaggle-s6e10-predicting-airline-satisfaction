# EDA Insights

From `notebooks/01_eda.ipynb` version v1, Kaggle kernel
`tuannm3812/airline-satisfaction-eda` version 1, completed 2026-10-02.
CPU, internet disabled, private. Log:
`assets/kernel_logs/kernel_v01_eda.log`. The run finished in about 40
seconds of worker time. GPU was not used.

## Findings

1. **The mounted files match the local schema.** Train 699,635 × 23, test
   299,844 × 22, positive labels 310,339. The sample constant differs from
   the train positive rate by `5.551e-17`.
2. **Class and trip purpose dominate the raw rates.** Business class
   0.7253 (342,212), Eco 0.1676 (327,404), Eco Plus 0.2422 (30,019).
   Business travel 0.5843 versus Personal Travel 0.0973. Loyal customers
   0.4951 versus disloyal 0.2009. Gender is a small gap: Female 0.4380,
   Male 0.4491.
3. **Online boarding is the strongest single column.** Univariate ROC AUC
   0.8404. Next are inflight entertainment 0.7445 and seat comfort 0.7321.
   Delays and gate location sit near 0.51.
4. **Survey score 0 is not one bucket.** Wifi at 0 has satisfaction 0.8873
   against 0.4351 on scores 1–5. Online booking at 0 is 0.7076 against
   0.4374. Entertainment at 0 is 0.1402 against 0.4440. `Baggage handling`
   has no zeros. A later model should not treat every 0 as "worse than 1"
   without checking the column.
5. **A missing arrival delay is rare and slightly less satisfied.** 292
   train rows (rate 0.3630) versus 0.4436 when the delay is observed. The
   observed arrival delay correlates 0.8420 with departure delay. Test has
   130 nulls in the same column and nowhere else.
6. **Train and test look interchangeable on this screen.** Largest drift
   statistic is a KS of 0.0027 on Cleanliness. Adversarial OOF AUC is
   0.5004 on 200,000 rows per side, 3-fold, seed 42. That adversarial
   number is a subsample, not a full-data measurement. Duplicate feature
   rows: 0.

## Environment

Python 3.12.13, numpy 2.0.2, pandas 2.3.3, scikit-learn 1.6.1,
matplotlib 3.10.0. Data path on the worker:
`/kaggle/input/competitions/playground-series-s6e10`.
