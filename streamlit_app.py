import streamlit as st
import joblib
import pandas as pd
import datetime

# Load the trained model (Pipeline with preprocessing)
model = joblib.load("lightgbm_pipeline.joblib")

# Streamlit App
st.title("Money Laundering Detection Dashboard")

st.sidebar.write("Enter transaction details to detect whether it is suspicious.")

# Form for transaction input
with st.sidebar.form("transaction_form"):
    st.header("Transaction Details")

    from_bank = st.number_input("From Bank ID", min_value=0, step=1)
    account = st.text_input("Account Number")
    to_bank = st.number_input("To Bank ID", min_value=0, step=1)
    account_1 = st.number_input("Account.1", min_value=0.0, step=0.01) 
    payment_format = st.selectbox("Payment Format", ["ACH", "Credit Card", "Cheque", "Reinvestment", "Cash"])
    amount_received = st.number_input("Amount Received", min_value=0.01, step=0.01)
    amount_paid = st.number_input("Amount Paid", min_value=0.01, step=0.01)

    # Default currency (US Dollar)
    receiving_currency = "US Dollar"
    payment_currency = "US Dollar"

    # Auto-fill today's date
    transaction_date = st.date_input("Transaction Date", datetime.date.today())

    submitted = st.form_submit_button("Detect Money Laundering")

# When the button is pressed, make a prediction
if submitted:
    transaction_date_numeric = pd.to_datetime(transaction_date).timestamp()

    # Create DataFrame with user input
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

    # Ensure correct data types
    input_data = input_data.astype({
        "From Bank": str,
        "To Bank": str,
        "Account": str,
        "Account.1": float,
        "Amount Received": float,
        "Amount Paid": float,
        "Date": str  
    })

    # Make a prediction using the trained model
    prediction = model.predict(input_data)

    # Display prediction result
    st.sidebar.write("### Prediction Result:")
    if prediction[0] == 1:
        st.error("🚨 This transaction is **suspicious** and may indicate money laundering!")
    else:
        st.success("✅ This transaction is **not suspicious**.")
