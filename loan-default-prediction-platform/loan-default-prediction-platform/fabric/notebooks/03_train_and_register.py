# Fabric notebook training template. Install/enable lightgbm and mlflow in the workspace.
import mlflow
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import roc_auc_score, average_precision_score, recall_score
from lightgbm import LGBMClassifier

df = spark.table("sba_7a_gold_ml").toPandas()
train = df[df.ApprovalFY.between(2014, 2017)].copy()
valid = df[df.ApprovalFY == 2018].copy()
test = df[df.ApprovalFY == 2019].copy()
target = "target_default"
features = [c for c in df.columns if c not in [target,"LoanStatus","ApprovalFY"]]
num = [c for c in features if pd.api.types.is_numeric_dtype(df[c])]
cat = [c for c in features if c not in num]
prep = ColumnTransformer([
    ("num", SimpleImputer(strategy="median", add_indicator=True), num),
    ("cat", Pipeline([("impute",SimpleImputer(strategy="most_frequent")),
                      ("ohe",OneHotEncoder(handle_unknown="ignore",min_frequency=25))]),cat)
])
model = Pipeline([("prep",prep),("model",LGBMClassifier(
    n_estimators=700,learning_rate=0.035,num_leaves=31,class_weight="balanced",
    random_state=42,verbosity=-1))])
with mlflow.start_run(run_name="SBA_7a_LightGBM_chronological"):
    model.fit(train[features],train[target])
    p = model.predict_proba(test[features])[:,1]
    mlflow.log_metric("test_roc_auc",roc_auc_score(test[target],p))
    mlflow.log_metric("test_pr_auc",average_precision_score(test[target],p))
    mlflow.sklearn.log_model(model,"model")
