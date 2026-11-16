import pandas as pd
from src.data_prep import build_training_frame

def test_target_mapping_and_exclusions():
    df = pd.DataFrame({
        "ApprovalFY":[2014,2015,2016],
        "LoanStatus":["PIF","CHGOFF","CANCLD"],
        "ApprovalDate":["01-01-2014","02-01-2015","03-01-2016"],
        "GrossApproval":[100,200,300],
        "SBAGuaranteedApproval":[75,150,225],
        "InitialInterestRate":[5,6,7],
        "TerminMonths":[60,120,180],
        "JobsSupported":[1,2,3],
        "BusinessAge":[1,2,3],
        "ProcessingMethod":["A","B","C"],
        "Subprogram":["X","Y","Z"],
        "BorrState":["CA","TX","NY"],
        "ProjectState":["CA","TX","NY"],
        "BusinessType":["CORP","IND","PART"],
        "CollateralInd":["Y","N","Y"],
        "FixedorVariableInterestRate":["F","V","F"],
        "RevolverStatus":["0","1","0"],
        "NAICSDescription":["Food","Retail","Other"],
        "SBADistrictOffice":["LA","TX","NY"]
    })
    out, features = build_training_frame(df)
    assert len(out) == 2
    assert out["target_default"].tolist() == [0,1]
    assert "GrossApproval" in features
    assert "LoanStatus" not in features
