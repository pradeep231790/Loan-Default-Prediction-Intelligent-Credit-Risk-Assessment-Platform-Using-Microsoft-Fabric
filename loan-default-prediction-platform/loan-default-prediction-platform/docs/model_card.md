# Model Card — SBA 7(a) Loan Default Risk

## Intended use
Historical risk ranking and analyst decision support for SBA 7(a)-like loan applications. Not intended for autonomous approval, denial, pricing, collections action, or use outside validated populations.

## Target
`CHGOFF=1` (charged off); `PIF=0` (paid in full). Other statuses excluded.

## Population
Uploaded SBA 7(a) extract, filtered to FY2014–FY2019. Training script uses 2014–2017 train, 2018 validation, 2019 holdout.

## Model
LightGBM binary classifier in a preprocessing Pipeline: median imputation for numeric fields, most-frequent imputation and one-hot encoding for categorical fields, class weighting. Threshold is selected using validation precision-recall trade-off and is not a universal lending cutoff.

## Metrics
Metrics are generated at training time and saved in `artifacts/model_metadata.json`. Do not populate the model card with the earlier deck's metrics as if they were this run's results.

## Critical risks
- Right-censoring / unequal outcome observation windows by approval cohort.
- Point-in-time leakage if any feature was not known at approval.
- Class imbalance and threshold-dependent false negatives/false positives.
- Geographic/industry/business variables may be proxies for protected or sensitive attributes.
- Historical SBA data may not generalize to other lenders, countries, products, or current macroeconomic conditions.

## Required pre-production tests
1. Validate label maturity and outcome horizon.
2. Validate every feature's timestamp and availability.
3. Reconcile duplicate handling and status counts.
4. Test temporal generalization on later mature cohorts.
5. Assess calibration, stability, subgroup performance, and fairness with legal/compliance review.
6. Establish human review, monitoring, rollback, and retraining policy.
