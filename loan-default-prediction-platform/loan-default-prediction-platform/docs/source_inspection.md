# Source Inspection Notes

## Files in uploaded ZIP
- `foia-7a-fy2010-fy2019-asof-250930.csv` — 7(a), 43 columns; 545,751 total rows in the full file.
- `foia-504-fy2010-present-asof-250930.csv` — 504, 40 columns; separate structure.
- `7a_504_foia_data_dictionary.xlsx` — two sheets: 7(a) and 504 definitions.
- `Ryewalk _ Data Science Case Study Assignment.pdf`
- `SBA Loan Default Prediction.pptx`
- `SBA_Loan_Default_Prediction.ipynb` — 144 cells.

## Case study
The assignment asks for acquisition/EDA, target definition, feature engineering, missing/outlier/categorical/imbalance handling, model comparison/validation/tuning, model explanation, and an executive presentation.

## Existing presentation
It reports 354,270 FY2014–2019 rows before deduplication, 424 duplicates, 353,846 after deduplication, and 8.29% default among completed PIF/CHGOFF loans. It recommends optimized LightGBM and reports approximately 95% default recall and 0.985 ROC-AUC. These metrics are historical claims from the supplied artifact, not verified outputs of this new training code.

## Independent CSV inspection
A chunked scan of the actual 7(a) CSV filtered to ApprovalFY 2014–2019 produced 354,270 rows with statuses: PIF 237,510; CHGOFF 21,468; EXEMPT 55,157; CANCLD 40,070; COMMIT 63; missing 2. Completed records = 258,978; default rate = 8.2895%.

## Key design decision
Do not merge 7(a) and 504 blindly. The schemas differ. Start with 7(a), retain 504 for a separately designed product-specific extension.
