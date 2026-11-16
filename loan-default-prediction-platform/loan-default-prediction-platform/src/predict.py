import json, joblib
from pathlib import Path

class LoanRiskPredictor:
    def __init__(self, model_path="artifacts/loan_default_pipeline.joblib",
                 metadata_path="artifacts/model_metadata.json"):
        self.model = joblib.load(model_path)
        self.meta = json.loads(Path(metadata_path).read_text())
        self.threshold = float(self.meta["threshold"])
        self.features = self.meta["feature_columns"]

    def predict(self, payload):
        row = {c: payload.get(c) for c in self.features}
        import pandas as pd
        X = pd.DataFrame([row])
        prob = float(self.model.predict_proba(X)[0,1])
        risk = "HIGH" if prob >= self.threshold else ("MEDIUM" if prob >= self.threshold*0.6 else "LOW")
        return {"default_probability":prob, "risk_category":risk,
                "threshold":self.threshold,
                "disclaimer":"Decision support only; requires human review."}
