# SBA Loan Default Prediction & Credit Risk Intelligence Platform

A production-oriented reference implementation built from the uploaded SBA FOIA 7(a) data and the supplied Ryewalk case study. It combines Microsoft Fabric data engineering, supervised machine learning, explainability, a FastAPI scoring service, a Streamlit interface, and an optional RAG document assistant.

> **Implementation status:** This repository contains executable local Python components and deployment-ready Fabric templates. It does not claim that a Microsoft Fabric workspace, Azure AI Search service, Azure OpenAI resource, or production endpoint has already been provisioned. Those cloud resources require your tenant, subscription, capacity, credentials, and explicit deployment.

## 1. Business problem

Predict whether a completed SBA 7(a) loan will ultimately be charged off. The source case study defines `CHGOFF` as default and `PIF` as non-default. `EXEMPT`, `CANCLD`, `COMMIT`, and missing statuses are excluded from the binary training population.

The uploaded case study specifies SBA 7(a) and 504 FY2014–2019. The uploaded 7(a) CSV contains FY2010–2019 records; this project filters FY2014–2019 for alignment with the assignment. The 504 file is retained as a separate source and is not merged into the 7(a) training set because its schema and product structure differ.

## 2. Source-derived data facts

Independent chunked inspection of the uploaded 7(a) CSV for FY2014–2019 found:

| Item | Value |
|---|---:|
| Rows before deduplication (FY2014–2019) | 354,270 |
| Source columns | 43 |
| PIF | 237,510 |
| CHGOFF | 21,468 |
| EXEMPT | 55,157 |
| CANCLD | 40,070 |
| COMMIT | 63 |
| Missing LoanStatus | 2 |
| Completed loans (PIF + CHGOFF) | 258,978 |
| Default rate among completed loans | 8.2895% |

The existing supplied presentation reports 424 duplicate rows and a final dataset of 353,846 rows after deduplication. The new training script performs its own duplicate removal and prints the actual counts. Do not assume the old presentation's model metrics are reproduced by this new pipeline.

## 3. Target and modelling safeguards

- `target_default = 1` for `CHGOFF`; `0` for `PIF`.
- Exclude other statuses from supervised binary training.
- Use FY2014–FY2017 for training, FY2018 for threshold/model selection, and FY2019 as a chronological holdout. If sample size or cohort maturity makes this split unsuitable, document and justify an alternative.
- Historical status is observed as of the source extract date (2025-09-30). Newer approval cohorts have shorter observation windows, so cohort maturity/censoring must be investigated before treating FY2019 performance as directly comparable with earlier cohorts.
- Exclude post-origination/outcome fields from predictors: `LoanStatus`, `PaidinFullDate`, `ChargeoffDate`, `GrossChargeoffAmount`, `FirstDisbursementDate`, and other fields not demonstrably available at decision time.
- `SoldSecondMarketInd` is excluded by default because its point-in-time availability at approval is not established.
- Borrower names, addresses, ZIP codes, and other direct identifiers are not used as predictors.
- A prediction is decision support, not an automatic loan approval/rejection.

## 4. Architecture

```mermaid
flowchart TD
  A[Source SBA 7(a) CSV + Data Dictionary] --> B[Fabric Data Factory Pipeline]
  B --> C[OneLake / Bronze Lakehouse]
  C --> D[PySpark quality & standardization]
  D --> E[Silver Delta Tables]
  E --> F[Gold ML-ready table]
  F --> G[Fabric Warehouse / SQL Star Schema]
  F --> H[Fabric Notebook: EDA + Feature Engineering]
  H --> I[Train / Validate / Test]
  I --> J[MLflow Experiment + Model Artifact]
  J --> K[Model Scoring Service]
  K --> L[FastAPI]
  L --> M[Streamlit Loan Risk UI]
  L --> N[Prediction Log / Warehouse]
  O[Policy PDFs / Guidelines] --> P[Chunk + Embed]
  P --> Q[Vector Search: Azure AI Search]
  Q --> R[Retriever + LLM]
  R --> M
```

### Technology map

| Layer | Technology | Responsibility |
|---|---|---|
| Data platform | Microsoft Fabric / OneLake | Unified analytics storage |
| Ingestion | Fabric Data Factory | Copy/trigger/orchestrate data |
| Lakehouse | Fabric Lakehouse, Delta | Bronze, Silver, Gold |
| Transform | PySpark / Spark SQL | Clean, standardize, derive features |
| Warehouse | Fabric Warehouse, T-SQL | Curated dimensional reporting |
| ML | Python, scikit-learn, LightGBM | Default probability model |
| Tracking | MLflow | Runs, parameters, metrics, artifacts |
| Explainability | SHAP | Local/global feature attribution |
| API | FastAPI, Pydantic | Validated model inference |
| UI | Streamlit | Loan input and risk dashboard |
| RAG | Azure AI Search + embedding model + LLM | Policy/document retrieval assistant |
| BI | Power BI | Portfolio monitoring |
| DevOps | GitHub Actions, Docker | Tests and repeatable deployment |

Fabric feature availability, model serving options, and pipeline JSON formats can vary by tenant and release. Use the Fabric templates as implementation assets and validate them in your workspace before deployment.

## 5. Repository structure

```text
loan-default-prediction-platform/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── data/
│   ├── raw/                 # Do not commit raw borrower-level source data
│   └── sample/
├── fabric/
│   ├── notebooks/
│   │   ├── 01_bronze_to_silver.py
│   │   ├── 02_silver_to_gold.py
│   │   └── 03_train_and_register.py
│   ├── warehouse/
│   │   └── schema.sql
│   └── pipeline_templates/
│       └── ingestion_pipeline.template.json
├── src/
│   ├── config.py
│   ├── data_prep.py
│   ├── train.py
│   └── predict.py
├── backend/
│   └── main.py
├── frontend/
│   └── app.py
├── rag/
│   └── rag_service.py
├── tests/
│   └── test_data_prep.py
├── docs/
│   ├── architecture.md
│   ├── data_dictionary.md
│   ├── model_card.md
│   ├── deployment_guide.md
│   ├── learning_guide.md
│   └── interview_questions.md
└── notebooks/
    └── 01_end_to_end_training.ipynb
```

## 6. Quick start (local)

1. Create a Python 3.10 or 3.11 environment.
2. Install packages: `pip install -r requirements.txt`
3. Put the extracted SBA 7(a) CSV at `data/raw/foia-7a-fy2010-fy2019-asof-250930.csv`.
4. Run: `python -m src.train --input data/raw/foia-7a-fy2010-fy2019-asof-250930.csv --output artifacts`
5. Start API: `uvicorn backend.main:app --reload`
6. Start UI in another terminal: `streamlit run frontend/app.py`
7. Open API docs at `http://127.0.0.1:8000/docs` and Streamlit at `http://localhost:8501`.

The training script uses a chronological split and may take several minutes depending on hardware. It saves the fitted preprocessing/model pipeline, feature schema, threshold, and metrics under `artifacts/`.

## 7. Fabric implementation sequence

1. Create a Fabric workspace and Lakehouse.
2. Upload the 7(a) CSV to the Lakehouse Files area or configure a Data Factory copy activity from approved storage.
3. Import `fabric/notebooks/01_bronze_to_silver.py`, attach the Lakehouse, and run it.
4. Run `02_silver_to_gold.py` to produce the ML-ready table.
5. Create a Fabric Warehouse and execute `fabric/warehouse/schema.sql`.
6. Import/run `03_train_and_register.py` in a Fabric notebook with required libraries available.
7. Configure a Fabric Data Factory pipeline using the supplied template as a design reference; select the actual workspace item IDs and linked services in the UI.
8. Configure refresh cadence, monitoring, permissions, and deployment pipelines appropriate to your tenant.

The templates cannot create cloud resources without workspace identifiers, linked services, capacity, credentials, and tenant permissions.

## 8. RAG design

RAG is a separate document knowledge subsystem. Index policy manuals, approved credit policy documents, SBA programme guides, and internal model documentation. Do not embed every numeric loan row and do not let an LLM invent a default probability. The ML model returns the probability; RAG retrieves relevant passages and cites the source document for policy explanations. Keep policy retrieval and credit scoring logically separate.

## 9. Production controls

- Use managed identity / Key Vault rather than hard-coded secrets.
- Encrypt data in transit and at rest; restrict borrower-level access.
- Apply least privilege and audit logging.
- Validate schema, ranges, nulls, duplicates, and status distributions at ingestion.
- Monitor data drift, population stability, calibration, recall, precision, false negatives, and cohort maturity.
- Establish a human review process and documented adverse-action process where applicable.
- Assess fairness and prohibited-variable/proxy risks with qualified compliance stakeholders.
- Version datasets, code, features, models, thresholds, and approval records.
- Revalidate before retraining or changing thresholds.

## 10. Known limitations

1. The supplied extract is historical and may not represent current credit conditions.
2. FY2019 loans may have shorter performance observation than FY2014 loans.
3. The label is based on final status in the extract, not necessarily a fixed 12/24-month default horizon.
4. This is a historical risk model, not an underwriting policy or legally validated credit decision system.
5. Geographic, lender, and industry variables can act as proxies and require fairness review.
6. The existing presentation's metrics are not independently reproduced in this new repository.
7. RAG content and external Azure services must be configured by the deploying organization.

See `docs/` for architecture, model card, deployment, study guide, and interview preparation.
