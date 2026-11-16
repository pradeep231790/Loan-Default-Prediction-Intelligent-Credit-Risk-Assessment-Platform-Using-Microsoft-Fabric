# Loan Default Prediction & Intelligent Credit Risk Assessment Platform

This repository contains the project for the Microsoft Fabric-based Loan Default Prediction and Intelligent Credit Risk Assessment Platform.

## Project location

The full project content is currently stored under the nested directory:

- `loan-default-prediction-platform/loan-default-prediction-platform/`

This appears to be a duplicate nesting of the project folder. The actual project files are inside that directory and should be treated as the project root for development.

## Repository structure

```text
.
├── README.md
├── .gitignore
└── loan-default-prediction-platform/
    └── loan-default-prediction-platform/
        ├── README.md
        ├── requirements.txt
        ├── Dockerfile
        ├── docker-compose.yml
        ├── src/
        ├── backend/
        ├── frontend/
        ├── fabric/
        ├── rag/
        ├── docs/
        ├── notebooks/
        └── tests/
```

## Recommended cleanup

To make the repository cleaner and avoid the duplicated folder nesting, move the contents of:

`loan-default-prediction-platform/loan-default-prediction-platform/`

up one level so the project root is:

`loan-default-prediction-platform/`

Then remove the extra nested directory after verifying the files were moved correctly.

## Quick start

After opening the project folder, install dependencies and run the project:

```bash
cd loan-default-prediction-platform/loan-default-prediction-platform
pip install -r requirements.txt
```

For full instructions, refer to the project README inside the nested project folder.
