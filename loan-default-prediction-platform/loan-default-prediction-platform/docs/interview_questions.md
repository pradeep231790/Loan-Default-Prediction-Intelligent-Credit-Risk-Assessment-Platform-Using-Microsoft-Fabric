# 100 Interview Questions and Candidate-Style Answers

## 1. What is the business problem?
Predict whether an SBA 7(a) loan will be charged off so analysts can prioritize risk review and portfolio monitoring.

## 2. What is the target variable?
LoanStatus mapped as CHGOFF=1 and PIF=0; other statuses are excluded.

## 3. Why exclude EXEMPT and CANCLD?
They are not completed paid-in-full or charged-off outcomes for this binary target.

## 4. What is the observed default rate?
About 8.29% among 258,978 PIF/CHGOFF records in the FY2014–2019 7(a) extract.

## 5. Why not use accuracy alone?
A model can predict the majority non-default class and still miss many defaulters.

## 6. What is recall?
The share of actual defaulters correctly identified; it directly reflects missed defaulters.

## 7. What is precision?
The share of predicted defaulters that truly default; it reflects false alarms.

## 8. Why track PR-AUC?
It focuses on precision-recall trade-offs and is useful with an imbalanced positive class.

## 9. Why use a time split?
It better simulates training on past cohorts and testing on future cohorts.

## 10. What is temporal leakage?
Using information from the future relative to the prediction timestamp.

## 11. Give examples of leakage fields here.
ChargeoffDate, GrossChargeoffAmount, PaidinFullDate, and LoanStatus as a predictor.

## 12. Why exclude FirstDisbursementDate?
It may occur after approval and may not be available at the decision point.

## 13. Why exclude SoldSecondMarketInd by default?
Its availability timing is uncertain; using it without validation risks leakage.

## 14. Why exclude borrower name and address?
They are identifiers, add privacy risk, and can create spurious memorization.

## 15. What is class imbalance?
The default class is much smaller than the paid-in-full class.

## 16. How does class weighting help?
It increases the training penalty for errors on the minority class without changing observed class prevalence by resampling.

## 17. Why not automatically use SMOTE?
Synthetic samples can distort categorical/temporal relationships and should be justified experimentally.

## 18. What is a threshold?
The probability cutoff used to convert a score into a binary alert.

## 19. Why tune threshold on validation only?
To avoid using test outcomes to optimize decisions and inflate reported performance.

## 20. What is ROC-AUC?
The probability that a randomly selected positive is ranked above a randomly selected negative.

## 21. What is calibration?
Agreement between predicted probabilities and observed event frequencies.

## 22. What is Brier score?
Mean squared error between predicted probability and binary outcome.

## 23. Why LightGBM?
It is an efficient gradient-boosted tree algorithm that models nonlinearities and interactions.

## 24. What is gradient boosting?
An ensemble built sequentially, where each new learner improves on errors from previous learners.

## 25. What is a decision tree?
A model that recursively splits data using feature thresholds to predict a target.

## 26. What is Random Forest?
An ensemble of randomized decision trees whose predictions are aggregated.

## 27. What is XGBoost?
A regularized, optimized gradient-boosted tree framework.

## 28. What is one-hot encoding?
Representing categorical levels as binary indicator columns.

## 29. Why handle unknown categories?
New categories can appear after training; inference should not fail.

## 30. Why impute missing numeric values?
Many estimators require complete numeric matrices; median is robust to skew.

## 31. Why use missing indicators?
Missingness itself may carry information, though it needs stability review.

## 32. What is a Lakehouse?
A data architecture combining data-lake flexibility with table/warehouse-like management.

## 33. What is OneLake?
Microsoft Fabric's unified logical data lake for organizational analytics data.

## 34. What is Medallion architecture?
A layered data pattern commonly using Bronze, Silver and Gold refinement stages.

## 35. What is Bronze?
Raw landed source data preserved for traceability.

## 36. What is Silver?
Cleaned, standardized and quality-checked data.

## 37. What is Gold?
Curated business-ready or ML-ready data.

## 38. What is Delta Lake?
A storage layer providing ACID transactions and table management on data-lake files.

## 39. What is Data Factory?
A data integration and orchestration service for copying and coordinating data workflows.

## 40. What is a Fabric pipeline?
An orchestration workflow that runs copy, notebook and other activities in dependency order.

## 41. What is PySpark?
The Python interface to Apache Spark for distributed data processing.

## 42. Why use Spark?
It scales transformations across distributed compute for larger data volumes.

## 43. What is a Fabric Warehouse?
A relational analytics warehouse in Fabric queried using SQL.

## 44. What is a star schema?
A fact table linked to descriptive dimension tables for analytics.

## 45. What is a fact table here?
A loan performance fact containing measures and dimension keys.

## 46. What is a dimension table?
A descriptive table such as approval date, business or loan product.

## 47. What is ETL?
Extract, transform, load: transform data before loading the target.

## 48. What is ELT?
Extract, load, transform: land data first and transform within the target platform.

## 49. What is feature engineering?
Creating model inputs from raw fields using domain and statistical reasoning.

## 50. Why derive approval month?
It can capture seasonal patterns, provided the approval date is known at scoring time.

## 51. What is cyclic encoding?
Representing month using sine/cosine so December is close to January.

## 52. Why is business age missingness important?
Coverage may vary by year; missingness can reflect data collection changes rather than borrower risk.

## 53. What is high cardinality?
A categorical variable with many distinct values, such as city or lender name.

## 54. Why not frequency encode all high-cardinality features?
Frequency can be unstable and may leak information if computed before splitting; it needs train-only fitting.

## 55. What is cross-validation?
Repeated train/validation splits to estimate model stability; time-aware folds are preferred for temporal data.

## 56. What is hyperparameter tuning?
Searching model configuration values such as learning rate, tree depth and number of trees.

## 57. What is overfitting?
Learning noise in training data that does not generalize to new data.

## 58. How do you detect overfitting?
Compare train and validation/test metrics and inspect temporal/subgroup stability.

## 59. What is SHAP?
A method to attribute prediction contributions to input features.

## 60. Does SHAP prove causation?
No; it explains model behavior, not causal effects.

## 61. What is MLflow?
An experiment/model lifecycle tool for logging runs, metrics, parameters and artifacts.

## 62. What is a model registry?
A controlled catalog of model versions and lifecycle stages.

## 63. What is model drift?
A change in input data or the relationship between inputs and outcomes over time.

## 64. What is data drift?
A change in the distribution of model input features.

## 65. What is concept drift?
A change in the relationship between features and the target.

## 66. What is PSI?
Population Stability Index, a measure used to quantify distribution shifts.

## 67. What is FastAPI?
A Python framework for building typed, high-performance REST APIs.

## 68. What is REST?
An HTTP API style using resources and standard methods such as GET and POST.

## 69. What is Pydantic?
A Python data validation library used by FastAPI for request/response schemas.

## 70. What is Streamlit?
A Python framework for building interactive data apps quickly.

## 71. How does the UI call the model?
It sends JSON to FastAPI's POST /predict endpoint; the API transforms and scores the input.

## 72. Why save preprocessing with the model?
Training and inference must apply exactly the same transformations.

## 73. What is a vector embedding?
A numeric vector representing semantic information in text.

## 74. What is a vector database?
A system that stores vectors and retrieves similar vectors efficiently.

## 75. What is semantic search?
Retrieval based on meaning rather than exact keyword matching.

## 76. What is RAG?
Retrieval-Augmented Generation: retrieve relevant documents and provide them as context to an LLM.

## 77. Why separate RAG from the classifier?
The classifier predicts from structured features; RAG retrieves policy evidence and should not invent numeric scores.

## 78. What documents belong in the RAG index?
Approved loan policies, SBA programme guides, procedures and model documentation.

## 79. How do you reduce hallucinations in RAG?
Ground answers in retrieved passages, cite sources, constrain scope and abstain when evidence is missing.

## 80. What is MLOps?
Practices for reproducible ML development, deployment, monitoring and lifecycle management.

## 81. What is CI/CD?
Automated testing and controlled delivery of code/configuration changes.

## 82. Why use Docker?
To package application dependencies consistently across environments.

## 83. How do you secure the API?
Use authentication, authorization, TLS, secrets management, input validation and audit logs.

## 84. Why not commit the raw CSV?
It contains borrower-level information and should be controlled; public availability does not remove governance obligations.

## 85. What is data lineage?
Traceability of data origin and transformations through the pipeline.

## 86. What is model explainability?
The ability to understand factors influencing a model output.

## 87. What fairness checks are needed?
Evaluate subgroup errors and proxy effects with legal/compliance guidance; geography and industry may encode sensitive proxies.

## 88. Why is 95% recall not enough?
It says nothing alone about precision, calibration, sample maturity, subgroup fairness or future generalization.

## 89. What is right censoring?
Some loans have not had enough time to experience the event by the data snapshot date.

## 90. Why is FY2019 a concern?
It has a shorter observation window than FY2014 loans in a 2025 snapshot.

## 91. What is a 12-month default horizon?
A label defined as default occurring within 12 months after origination/approval, requiring dated event data and censoring logic.

## 92. How would you improve the target?
Define a fixed outcome horizon and build a cohort-aware label using approval and charge-off dates.

## 93. How do you monitor in production?
Track input quality, drift, calibration, recall/precision when labels mature, latency, failures and model version.

## 94. When retrain?
When scheduled review or validated drift/performance thresholds indicate it, after data and governance checks.

## 95. How do you rollback?
Keep prior signed model artifact, metadata and configuration; redeploy known-good version.

## 96. How scale to millions of records?
Use Fabric Spark/Delta pipelines, partitioning, incremental ingestion, optimized tables and scalable model scoring.

## 97. What is the role of Power BI?
Portfolio reporting on default rates, exposure, trends, geography and model monitoring metrics.

## 98. What is the most important project limitation?
Outcome maturity and point-in-time feature validity must be proven before operational underwriting use.

## 99. How would you explain the project in one minute?
I built a pipeline concept that ingests SBA 7(a) data into Bronze/Silver/Gold, curates approval-time features, trains a time-validated LightGBM default classifier, exposes scoring through FastAPI and Streamlit, and keeps policy RAG separate for grounded document Q&A.
