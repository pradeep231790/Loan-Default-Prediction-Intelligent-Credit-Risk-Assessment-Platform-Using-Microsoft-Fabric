# Data Dictionary and Feature Policy

The source workbook has separate `7(a) Data Dictionary` and `504 Data Dictionary` sheets. The 7(a) CSV contains 43 fields. The following are the principal fields used or deliberately excluded by this implementation.

| Source field | Meaning / use |
|---|---|
| ApprovalFY | Fiscal-year filter; used for temporal partitioning, not as a direct model feature |
| ApprovalDate | Loan approval date; parsed into ApprovalYear and ApprovalMonth |
| GrossApproval | Gross approved loan amount; numeric feature |
| SBAGuaranteedApproval | SBA guaranteed amount; numeric feature |
| InitialInterestRate | Initial rate; numeric feature subject to point-in-time validation |
| TerminMonths | Loan term in months; numeric feature |
| JobsSupported | Number of jobs supported; numeric feature |
| BusinessAge | Business age; numeric feature, missingness may be informative |
| ProcessingMethod | Loan processing method; categorical feature |
| Subprogram | SBA subprogram; categorical feature |
| BorrState | Borrower state; categorical feature requiring fairness/proxy review |
| ProjectState | Project state; categorical feature requiring fairness/proxy review |
| BusinessType | Business legal type; categorical feature |
| CollateralInd | Collateral indicator; categorical feature |
| FixedorVariableInterestRate | Interest-rate type; categorical feature |
| RevolverStatus | Revolver indicator; categorical feature |
| NAICSDescription | Industry description; categorical feature |
| SBADistrictOffice | SBA district; categorical feature requiring proxy review |
| LoanStatus | Outcome label source only: PIF=0, CHGOFF=1 |
| GrossChargeoffAmount | Post-outcome field; excluded |
| ChargeoffDate | Post-outcome field; excluded |
| PaidinFullDate | Post-outcome field; excluded |
| FirstDisbursementDate | Potentially post-approval; excluded |
| SoldSecondMarketInd | Point-in-time availability uncertain; excluded by default |
| BorrName / BorrStreet / BorrZip | Direct identifiers; excluded |
| BankName / BankStreet / BankCity / bank IDs | Excluded by default; lender effects and fairness/proxy concerns require separate review |

The complete original field definitions remain in the supplied workbook. This table is an implementation-focused subset, not a replacement for that workbook.
