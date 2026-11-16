TARGET = "target_default"
SOURCE_YEAR_MIN = 2014
SOURCE_YEAR_MAX = 2019

NUMERIC_FEATURES = [
    "GrossApproval", "SBAGuaranteedApproval", "InitialInterestRate",
    "TerminMonths", "JobsSupported", "BusinessAge",
    "ApprovalYear", "ApprovalMonth"
]
CATEGORICAL_FEATURES = [
    "ProcessingMethod", "Subprogram", "BorrState", "ProjectState",
    "BusinessType", "CollateralInd", "FixedorVariableInterestRate",
    "RevolverStatus", "NAICSDescription", "SBADistrictOffice"
]
APPROVAL_TIME_FEATURES = ["ApprovalYear", "ApprovalMonth"]

EXCLUDED_FROM_FEATURES = [
    "AsOfDate", "Program", "BorrName", "BorrStreet", "BorrZip",
    "BankName", "BankFDICNumber", "BankNCUANumber", "BankStreet",
    "BankCity", "BankState", "BankZip", "ApprovalDate", "ApprovalFY",
    "FirstDisbursementDate", "NAICSCode", "FranchiseCode", "FranchiseName",
    "ProjectCounty", "CongressionalDistrict", "LoanStatus", "PaidinFullDate",
    "ChargeoffDate", "GrossChargeoffAmount", "SoldSecondMarketInd"
]
