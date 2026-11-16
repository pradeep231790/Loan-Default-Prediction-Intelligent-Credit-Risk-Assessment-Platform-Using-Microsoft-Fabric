# Learning Guide: Explain the Project in Interviews

## 1. Business problem
A lender wants to estimate whether a loan will eventually become charged off. This is binary classification. The positive class is the minority class, so accuracy alone is misleading.

## 2. Target and class imbalance
`PIF` is labelled 0 and `CHGOFF` is labelled 1. About 8.29% of completed FY2014–2019 loans are charged off in the inspected data. Class weighting makes errors on the minority class matter more during training. The threshold controls the precision/recall trade-off.

## 3. Why chronological validation?
A random split can mix older and newer economic periods across train and test. A chronological split better simulates training on past loans and scoring later loans. It does not by itself solve unequal label observation windows: cohort maturity must be checked.

## 4. Why Lakehouse?
A Lakehouse combines scalable file/table storage with analytics-friendly table formats. Bronze preserves source landing, Silver standardizes and validates, Gold creates curated business/ML tables. Delta tables support reliable writes and schema evolution.

## 5. Why Warehouse?
The Warehouse serves structured SQL analytics, dimensional modelling, governed reporting and BI. The Lakehouse is useful for raw/semi-structured engineering and Spark; the Warehouse is useful for curated relational reporting. They complement each other.

## 6. Data Factory and pipelines
Data Factory orchestrates copy and notebook activities, dependencies, schedules, retries and monitoring. A pipeline coordinates the repeatable ingestion-to-curation workflow.

## 7. PySpark
Spark distributes transformations over partitions. PySpark is the Python API for Spark. It is useful when source data grows beyond a single-machine workflow.

## 8. Feature engineering
Features must exist at the time of the intended prediction. This project derives approval year/month from approval date and uses loan amount, guarantee amount, rate, term, jobs, business attributes and selected categorical fields. It excludes charge-off/payment outcomes and direct identifiers.

## 9. LightGBM
LightGBM is gradient-boosted decision trees optimized for efficient training. It captures nonlinear relationships and interactions. Class weighting addresses imbalance; validation chooses a decision threshold.

## 10. Metrics
- Recall = TP/(TP+FN): proportion of actual defaulters detected.
- Precision = TP/(TP+FP): proportion of predicted defaulters that actually default.
- F1 = harmonic mean of precision and recall.
- ROC-AUC measures ranking across thresholds.
- PR-AUC is informative when the positive class is rare.
- Brier score measures probability error.
- Confusion matrix exposes false negatives and false positives.

## 11. MLflow
Tracks experiments, parameters, metrics and model artifacts. It improves reproducibility and supports model comparison/version governance.

## 12. SHAP
SHAP attributes a model prediction to feature contributions. It can explain global patterns and individual predictions. Correlation and proxy effects mean SHAP importance is not causal evidence.

## 13. FastAPI and Streamlit
FastAPI exposes a typed REST API for scoring. Streamlit provides a fast Python UI for analyst demonstration. The UI sends JSON to `/predict`; the API validates input, loads the fitted pipeline and returns probability/risk band.

## 14. RAG and vector search
RAG retrieves relevant document passages and gives them to an LLM as context. Embeddings represent text as vectors; vector/hybrid search finds semantically related passages. This assistant is for policy/document Q&A, not the numeric default classifier.

## 15. MLOps
MLOps applies software engineering to ML: versioning, testing, deployment, monitoring, drift detection, retraining, rollback and governance.

## 16. Production risks
Unequal outcome maturity, leakage, class imbalance, calibration, drift, privacy, fairness, feature availability, and the distinction between risk score and lending decision must all be addressed.
