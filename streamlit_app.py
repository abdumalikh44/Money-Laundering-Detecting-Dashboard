import streamlit as st
import joblib
import pandas as pd
import datetime

# Load the trained model (Pipeline with preprocessing)
model = joblib.load("lightgbm_pipeline.joblib")

# Streamlit App
st.title("💰 Money Laundering Detection Dashboard")

st.write("Enter transaction details to detect whether the transaction is suspicious.")

# Form for transaction input
with st.form("transaction_form"):
    date = st.date_input("Transaction Date", value=datetime.date.today())
    from_bank = st.number_input("From Bank ID", min_value=0, step=1)
    account = st.text_input("Account Number")
    to_bank = st.number_input("To Bank ID", min_value=0, step=1)
    payment_format = st.selectbox("Payment Format", ["ACH", "Credit Card", "Cheque", "Reinvestment", "Cash"])
    amount_received = st.number_input("Amount Received (USD)", min_value=0.01, step=0.01)
    amount_paid = st.number_input("Amount Paid (USD)", min_value=0.01, step=0.01)

    submitted = st.form_submit_button("🚀 Detect Money Laundering")

# Perform prediction when the button is clicked
if submitted:
    # Create DataFrame from user input (fixed currency = US Dollar)
    input_data = pd.DataFrame({
        "Date": [pd.to_datetime(date)],  # Ensure correct datetime format
        "From Bank": [from_bank],
        "Account": [account],
        "To Bank": [to_bank],
        "Receiving Currency": ["US Dollar"],
        "Payment Currency": ["US Dollar"],
        "Payment Format": [payment_format],
        "Amount Received": [amount_received],
        "Amount Paid": [amount_paid]
    })

    # Predict using the trained model
    try:
        prediction = model.predict(input_data)

        # Display prediction result
        st.write("### Prediction Result:")
        if prediction[0] == 1:
            st.error("🚨 This transaction is **suspected** of money laundering!")
        else:
            st.success("✅ This transaction is **not suspicious**.")
    except Exception as e:
        st.error(f"⚠️ Prediction error: {e}")
