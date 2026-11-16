import argparse, json, os
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import (roc_auc_score, average_precision_score, recall_score,
                             precision_score, f1_score, confusion_matrix,
                             brier_score_loss, precision_recall_curve)
from lightgbm import LGBMClassifier
from src.data_prep import build_training_frame, chronological_split
from src.config import TARGET

def choose_threshold(y_true, prob, min_precision=0.25):
    # Select the threshold with the highest recall among thresholds meeting a
    # configurable precision floor. The floor is a business choice, not a universal rule.
    p, r, t = precision_recall_curve(y_true, prob)
    candidates = [(r[i], p[i], t[i]) for i in range(len(t)) if p[i] >= min_precision]
    if not candidates:
        return 0.5
    return float(max(candidates, key=lambda z: (z[0], z[1]))[2])

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", default="artifacts")
    ap.add_argument("--min-precision", type=float, default=0.25)
    args = ap.parse_args()
    out = Path(args.output); out.mkdir(parents=True, exist_ok=True)

    # Only load required columns, reducing memory use and minimizing PII exposure.
    header = pd.read_csv(args.input, nrows=0).columns.tolist()
    wanted = ["ApprovalFY","LoanStatus","ApprovalDate","GrossApproval",
              "SBAGuaranteedApproval","InitialInterestRate","TerminMonths",
              "JobsSupported","BusinessAge","ProcessingMethod","Subprogram",
              "BorrState","ProjectState","BusinessType","CollateralInd",
              "FixedorVariableInterestRate","RevolverStatus","NAICSDescription",
              "SBADistrictOffice"]
    usecols = [c for c in wanted if c in header]
    raw = pd.read_csv(args.input, usecols=usecols, low_memory=False)
    frame, feature_cols = build_training_frame(raw)
    train, valid, test = chronological_split(frame)

    num_cols = [c for c in feature_cols if c in train.select_dtypes(include="number").columns]
    cat_cols = [c for c in feature_cols if c not in num_cols]
    preprocess = ColumnTransformer([
        ("num", SimpleImputer(strategy="median", add_indicator=True), num_cols),
        ("cat", Pipeline([
            ("impute", SimpleImputer(strategy="most_frequent")),
            ("ohe", OneHotEncoder(handle_unknown="ignore", min_frequency=25))
        ]), cat_cols)
    ])
    model = LGBMClassifier(
        objective="binary", n_estimators=700, learning_rate=0.035,
        num_leaves=31, max_depth=-1, subsample=0.85, colsample_bytree=0.85,
        class_weight="balanced", reg_lambda=1.0, random_state=42,
        n_jobs=-1, verbosity=-1
    )
    pipe = Pipeline([("preprocess", preprocess), ("model", model)])
    pipe.fit(train[feature_cols], train[TARGET])

    p_valid = pipe.predict_proba(valid[feature_cols])[:,1]
    threshold = choose_threshold(valid[TARGET].values, p_valid, args.min_precision)
    p_test = pipe.predict_proba(test[feature_cols])[:,1]
    yhat = (p_test >= threshold).astype(int)

    metrics = {
        "train_rows": int(len(train)), "validation_rows": int(len(valid)),
        "test_rows": int(len(test)), "features": feature_cols,
        "threshold_selected_on_validation": threshold,
        "test_default_rate": float(test[TARGET].mean()),
        "test_roc_auc": float(roc_auc_score(test[TARGET], p_test)),
        "test_pr_auc": float(average_precision_score(test[TARGET], p_test)),
        "test_recall_default": float(recall_score(test[TARGET], yhat, zero_division=0)),
        "test_precision_default": float(precision_score(test[TARGET], yhat, zero_division=0)),
        "test_f1_default": float(f1_score(test[TARGET], yhat, zero_division=0)),
        "test_brier_score": float(brier_score_loss(test[TARGET], p_test)),
        "test_confusion_matrix_tn_fp_fn_tp": confusion_matrix(test[TARGET], yhat).ravel().tolist(),
        "warning": "FY2019 cohort maturity/censoring and point-in-time feature availability require review."
    }
    joblib.dump(pipe, out/"loan_default_pipeline.joblib")
    (out/"model_metadata.json").write_text(json.dumps({
        "model_name":"SBA_7a_LightGBM_Chronological",
        "target":"CHGOFF=1, PIF=0",
        "feature_columns":feature_cols,
        "threshold":threshold,
        "metrics":metrics
    }, indent=2))
    print(json.dumps(metrics, indent=2))

if __name__ == "__main__":
    main()
