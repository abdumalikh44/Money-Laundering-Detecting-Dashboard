from datetime import datetime, timedelta

import streamlit as st
import joblib
import pandas as pd
import datetime
import gdown
from mitosheet.streamlit.v1 import spreadsheet
from mitosheet.streamlit.v1.spreadsheet import _get_mito_backend

# Load the trained model (Pipeline with preprocessing)
model = joblib.load("lightgbm_pipeline.joblib")

# Streamlit App
st.title("Money Laundering Detection Dashboard")

@st.cache_data
def get_txn_data():
    url = "https://drive.google.com/file/d/1kUK0voPeSkHvAQ57nqC7xXvQ4XjL6r3K/view?usp=drive_link"
    output = "HI-Small_Trans.csv"
    gdown.download(url, output, quiet=False, fuzzy=True)
    df = pd.read_csv(output, nrows=1000000)
    return df

aml_data = get_txn_data()

new_dfs, code = spreadsheet(aml_data)

def clear_mito_backend_cache():
    _get_mito_backend.clear()

    # Function to cache the last execution time - so we can clear periodically
    @st.cache_resource
    def get_cached_time():
        # Initialize with a dictionary to store the last execution time
        return {"last_executed_time": None}

st.sidebar.write("Enter transaction details to detect whether it is suspicious.")
# Form for transaction input
with st.sidebar.form("transaction_form"):
    st.header("Transaction Details")

    # Auto-fill today's date
    transaction_date = st.date_input("Transaction Date", datetime.date.today())

    from_bank = st.number_input("From Bank ID", min_value=0)
    account = st.number_input("Account Paid", min_value=0)
    to_bank = st.number_input("To Bank ID", min_value=0)
    account_1 = st.number_input("Account Sent", min_value=0) 
    payment_format = st.selectbox("Payment Format", ["ACH", "Credit Card", "Cheque", "Reinvestment", "Cash"])
    amount_received = st.number_input("Amount Received", min_value=0.01, step=0.01)
    amount_paid = st.number_input("Amount Paid", min_value=0.01, step=0.01)

    # Default currency (US Dollar)
    receiving_currency = "US Dollar"
    payment_currency = "US Dollar"

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
        "Account.1": str,
        "Amount Received": float,
        "Amount Paid": float,
        "Date": str  
    })

    # Make a prediction using the trained model
    prediction = model.predict(input_data)

    # Display prediction result
    st.sidebar.write("### Prediction Result:")
    if prediction[0] == 1:
        st.sidebar.error("🚨 This transaction is **suspicious** and may indicate money laundering!")
    else:
        st.sidebar.success("✅ This transaction is **not suspicious**.")
