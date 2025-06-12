import streamlit as st
import joblib
import pandas as pd
import datetime

# ----------------- Load Trained Model -----------------

model = joblib.load("lightgbm_pipeline.joblib")

# ----------------- Page Setup -----------------
st.set_page_config(page_title="Model", page_icon="🔍")
st.title("🔍 Transaction Checker – Money Laundering Detection")
st.markdown("💰 Use this tool to analyze and classify a transaction based on risk of money laundering.")
st.divider()
st.info("Fill in the transaction details below and click **Detect** to get the prediction.", icon="📝")

# ----------------- Transaction Form -----------------
with st.form("transaction_form"):
    st.subheader("📄 Transaction Details")

    col1, col2 = st.columns(2)
    with col1:
        transaction_date = st.date_input("📅 Transaction Date", datetime.date.today())
        from_bank = st.number_input("🏦 From Bank ID", min_value=0, help="Bank initiating the transaction")
        to_bank = st.number_input("🏦 To Bank ID", min_value=0, help="Receiving bank")
        payment_format = st.selectbox("💳 Payment Format", ["ACH", "Credit Card", "Cheque", "Reinvestment", "Cash"])

    with col2:
        account = st.number_input("👤 Account Paid", min_value=0)
        account_1 = st.number_input("👤 Account Sent", min_value=0)
        amount_received = st.number_input("📥 Amount Received", min_value=0.01, step=0.01)
        amount_paid = st.number_input("📤 Amount Paid", min_value=0.01, step=0.01)

    submitted = st.form_submit_button("🔍 Detect Money Laundering")

# ----------------- Prediction Logic -----------------
if submitted:
    # Validate required fields (make sure values aren't default/invalid)
    if (
        from_bank == 0 or to_bank == 0 or account == 0 or account_1 == 0 or
        amount_received <= 0 or amount_paid <= 0
    ):
        st.warning("⚠️ Please fill in all fields with valid (non-zero) values before submitting.")
    else:
        # Preprocess input data
        transaction_date_numeric = pd.to_datetime(transaction_date).timestamp()
        receiving_currency = "US Dollar"
        payment_currency = "US Dollar"

        input_data = pd.DataFrame({
            "From Bank": [from_bank],
            "Account": [account],
            "To Bank": [to_bank],
            "Account.1": [account_1],
            "Amount Received": [amount_received],
            "Receiving Currency": [receiving_currency],
            "Amount Paid": [amount_paid],
            "Payment Currency": [payment_currency],
            "Payment Format": [payment_format],
            "Date": [transaction_date_numeric]
        })

        # Ensure correct datatypes
        input_data = input_data.astype({
            "From Bank": str,
            "To Bank": str,
            "Account": str,
            "Account.1": str,
            "Amount Received": float,
            "Amount Paid": float,
            "Date": str
        })

        # Predict using the loaded model
        try:
            prediction = model.predict(input_data)
        except Exception as e:
            st.error(f"Prediction failed: {e}")
            st.stop()

        # ----------------- Display Prediction Result -----------------
        st.subheader("📊 Prediction Result")
        if prediction[0] == 1:
            st.error("🚨 Suspicious Transaction Detected! This activity may indicate money laundering.")
        else:
            st.success("✅ This transaction does not appear to be suspicious.")

        st.caption("Note: The result is based on a predictive model trained on synthetic data.")
