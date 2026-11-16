# Deployment Guide

## Local proof of concept
Follow README quick start. Train model first, then run API and UI. Use synthetic/sample inputs for demonstrations; do not upload borrower-level data to public repositories.

## Microsoft Fabric
1. Create workspace, Lakehouse and Warehouse.
2. Upload/copy the SBA 7(a) CSV into Lakehouse Files/raw.
3. Import and attach notebooks under `fabric/notebooks/`.
4. Run Bronze/Silver then Silver/Gold.
5. Execute warehouse DDL in the Warehouse SQL editor.
6. Configure Data Factory Copy + Notebook activities using the pipeline template as a blueprint.
7. Configure credentials using workspace identity/managed identity where supported.
8. Validate row counts, data quality, lineage, and refresh schedule.
9. Run model training and register artifacts/metrics with MLflow.
10. Configure deployment to a supported serving target. Verify tenant-specific support before choosing Fabric endpoint or Azure ML.

## Security checklist
- Never commit `.env`, raw data, model binaries, API keys, or borrower identifiers.
- Use managed identity / Key Vault.
- Restrict OneLake and Warehouse access by role.
- Apply network controls and TLS.
- Log request IDs and model version, not unnecessary personal information.
- Set retention, audit, incident response, and deletion policies.

## Release checklist
- Unit/integration tests pass.
- Dataset version and label definition recorded.
- Point-in-time feature audit signed off.
- Validation/test metrics and calibration reviewed.
- Model card and threshold rationale approved.
- API health check and load test pass.
- Monitoring alerts and rollback artifact ready.
