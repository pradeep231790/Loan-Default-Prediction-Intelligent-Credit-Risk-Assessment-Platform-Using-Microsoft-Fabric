import pandas as pd
from src.config import NUMERIC_FEATURES, CATEGORICAL_FEATURES, TARGET

def parse_approval_date(series):
    # SBA extracts contain mixed date formats; dayfirst=False handles common DD-MM-YYYY values.
    return pd.to_datetime(series, errors="coerce", dayfirst=False)

def build_training_frame(df: pd.DataFrame, min_year=2014, max_year=2019):
    required = {"ApprovalFY", "LoanStatus", "ApprovalDate"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required source columns: {sorted(missing)}")

    x = df.copy()
    x["ApprovalFY"] = pd.to_numeric(x["ApprovalFY"], errors="coerce")
    x = x[x["ApprovalFY"].between(min_year, max_year)].copy()
    x = x.drop_duplicates()

    x[TARGET] = x["LoanStatus"].map({"PIF": 0, "CHGOFF": 1})
    x = x[x[TARGET].notna()].copy()
    x[TARGET] = x[TARGET].astype("int8")

    dt = parse_approval_date(x["ApprovalDate"])
    x["ApprovalYear"] = dt.dt.year
    x["ApprovalMonth"] = dt.dt.month

    # Use only fields expected to be known at or before approval. Exclude disbursement,
    # repayment, charge-off, secondary-market and borrower-identifying fields.
    feature_cols = [c for c in NUMERIC_FEATURES + CATEGORICAL_FEATURES if c in x.columns]
    if not feature_cols:
        raise ValueError("No configured feature columns were found in the source data.")

    for c in NUMERIC_FEATURES:
        if c in x.columns:
            x[c] = pd.to_numeric(x[c], errors="coerce")
    for c in CATEGORICAL_FEATURES:
        if c in x.columns:
            x[c] = x[c].astype("string").fillna("Unknown").astype(str)

    # Keep only records with usable approval year for chronological partitioning.
    x = x[x["ApprovalYear"].notna()].copy()
    x["ApprovalYear"] = x["ApprovalYear"].astype(int)
    x["ApprovalMonth"] = x["ApprovalMonth"].fillna(0).astype(int)

    return x, feature_cols

def chronological_split(df):
    train = df[df["ApprovalFY"].between(2014, 2017)].copy()
    valid = df[df["ApprovalFY"] == 2018].copy()
    test = df[df["ApprovalFY"] == 2019].copy()
    if min(len(train), len(valid), len(test)) == 0:
        raise ValueError("Chronological split produced an empty partition; inspect year coverage.")
    return train, valid, test
