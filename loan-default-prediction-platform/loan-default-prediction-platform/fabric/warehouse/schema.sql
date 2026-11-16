-- Fabric Warehouse starter dimensional model.
-- Load/merge curated rows from the Gold Lakehouse using a Fabric pipeline or SQL endpoint.
CREATE TABLE dbo.DimApprovalDate (
    ApprovalDateKey INT NOT NULL,
    ApprovalYear INT NOT NULL,
    ApprovalMonth INT NOT NULL
);

CREATE TABLE dbo.DimBusiness (
    BusinessKey BIGINT NOT NULL,
    BusinessType VARCHAR(100),
    NAICSDescription VARCHAR(300),
    BorrState CHAR(2),
    ProjectState CHAR(2)
);

CREATE TABLE dbo.DimLoanProduct (
    LoanProductKey BIGINT NOT NULL,
    ProcessingMethod VARCHAR(200),
    Subprogram VARCHAR(300),
    RevolverStatus VARCHAR(20),
    FixedorVariableInterestRate VARCHAR(20),
    CollateralInd VARCHAR(20)
);

CREATE TABLE dbo.FactLoanPerformance (
    LoanFactKey BIGINT NOT NULL,
    ApprovalDateKey INT,
    BusinessKey BIGINT,
    LoanProductKey BIGINT,
    GrossApproval DECIMAL(18,2),
    SBAGuaranteedApproval DECIMAL(18,2),
    InitialInterestRate DECIMAL(9,4),
    TermMonths INT,
    JobsSupported INT,
    TargetDefault INT
);

-- Aggregate reporting view; validate warehouse SQL dialect and key constraints in tenant.
CREATE VIEW dbo.vw_LoanDefaultByYear AS
SELECT d.ApprovalYear,
       COUNT_BIG(*) AS CompletedLoans,
       SUM(CASE WHEN f.TargetDefault = 1 THEN 1 ELSE 0 END) AS ChargedOffLoans,
       CAST(1.0 * SUM(CASE WHEN f.TargetDefault = 1 THEN 1 ELSE 0 END)
            / NULLIF(COUNT_BIG(*),0) AS DECIMAL(10,4)) AS DefaultRate
FROM dbo.FactLoanPerformance f
JOIN dbo.DimApprovalDate d ON f.ApprovalDateKey = d.ApprovalDateKey
GROUP BY d.ApprovalYear;
