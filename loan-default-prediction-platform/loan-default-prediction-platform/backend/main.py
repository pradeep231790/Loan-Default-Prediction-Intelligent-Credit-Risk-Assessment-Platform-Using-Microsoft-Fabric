import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from src.predict import LoanRiskPredictor

app = FastAPI(title="SBA Loan Default Risk API", version="1.0.0")
predictor = None

class LoanApplication(BaseModel):
    GrossApproval: float = Field(gt=0)
    SBAGuaranteedApproval: float = Field(gt=0)
    InitialInterestRate: float | None = None
    TerminMonths: float | None = None
    JobsSupported: float | None = None
    BusinessAge: float | None = None
    ApprovalYear: int = Field(ge=2014, le=2035)
    ApprovalMonth: int = Field(ge=1, le=12)
    ProcessingMethod: str = "Unknown"
    Subprogram: str = "Unknown"
    BorrState: str = "Unknown"
    ProjectState: str = "Unknown"
    BusinessType: str = "Unknown"
    CollateralInd: str = "Unknown"
    FixedorVariableInterestRate: str = "Unknown"
    RevolverStatus: str = "Unknown"
    NAICSDescription: str = "Unknown"
    SBADistrictOffice: str = "Unknown"

@app.on_event("startup")
def load_model():
    global predictor
    path = os.getenv("MODEL_PATH", "artifacts/loan_default_pipeline.joblib")
    meta = os.getenv("MODEL_METADATA_PATH", "artifacts/model_metadata.json")
    if os.path.exists(path) and os.path.exists(meta):
        predictor = LoanRiskPredictor(path, meta)

@app.get("/health")
def health():
    return {"status":"ok", "model_loaded":predictor is not None}

@app.post("/predict")
def predict(application: LoanApplication):
    if predictor is None:
        raise HTTPException(503, "Model not loaded. Train the model and set MODEL_PATH.")
    try:
        return predictor.predict(application.model_dump())
    except Exception as e:
        raise HTTPException(400, f"Prediction failed: {e}")
