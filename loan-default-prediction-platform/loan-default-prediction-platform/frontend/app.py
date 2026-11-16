import streamlit as st
import requests, os

st.set_page_config(page_title="SBA Loan Risk Assessment", page_icon="🏦", layout="wide")
st.title("SBA Loan Default Risk Assessment")
st.caption("Historical model output for decision support only — not an automatic lending decision.")
api = os.getenv("API_URL", "http://localhost:8000")
with st.form("loan_form"):
    c1,c2,c3 = st.columns(3)
    gross = c1.number_input("Gross approval ($)", min_value=1.0, value=150000.0)
    guaranteed = c2.number_input("SBA guaranteed approval ($)", min_value=1.0, value=112500.0)
    rate = c3.number_input("Initial interest rate (%)", min_value=0.0, value=6.5)
    term = c1.number_input("Term (months)", min_value=1, value=120)
    jobs = c2.number_input("Jobs supported", min_value=0, value=5)
    age = c3.number_input("Business age (years)", min_value=0.0, value=5.0)
    year = c1.number_input("Approval year", min_value=2014, max_value=2035, value=2026)
    month = c2.selectbox("Approval month", list(range(1,13)), index=0)
    state = c3.text_input("Borrower state (2-letter)", "CA")
    method = c1.text_input("Processing method", "7a General")
    subprogram = c2.text_input("Subprogram", "Guaranty")
    business_type = c3.selectbox("Business type", ["CORPORATION","INDIVIDUAL","PARTNERSHIP","Unknown"])
    collateral = c1.selectbox("Collateral indicator", ["Y","N","Unknown"])
    rate_type = c2.selectbox("Fixed/variable rate", ["F","V","Unknown"])
    revolver = c3.selectbox("Revolver status", ["0","1","Unknown"])
    industry = st.text_input("NAICS description", "Limited-Service Restaurants")
    district = st.text_input("SBA district office", "Unknown")
    project_state = st.text_input("Project state", state)
    submitted = st.form_submit_button("Assess loan risk")
if submitted:
    payload = {
      "GrossApproval":gross,"SBAGuaranteedApproval":guaranteed,
      "InitialInterestRate":rate,"TerminMonths":term,"JobsSupported":jobs,
      "BusinessAge":age,"ApprovalYear":int(year),"ApprovalMonth":int(month),
      "ProcessingMethod":method,"Subprogram":subprogram,"BorrState":state,
      "ProjectState":project_state,"BusinessType":business_type,
      "CollateralInd":collateral,"FixedorVariableInterestRate":rate_type,
      "RevolverStatus":revolver,"NAICSDescription":industry,
      "SBADistrictOffice":district
    }
    try:
        response = requests.post(api+"/predict", json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        a,b = st.columns(2)
        a.metric("Estimated default probability", f"{result['default_probability']:.1%}")
        b.metric("Risk category", result["risk_category"])
        st.info(f"Decision threshold: {result['threshold']:.3f}. {result['disclaimer']}")
    except Exception as e:
        st.error(f"Could not score application: {e}")
