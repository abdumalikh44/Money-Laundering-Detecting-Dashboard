import altair as alt
import pandas as pd
import streamlit as st
import gdown

# Show the page title and description.
st.set_page_config(page_title="AML dataset", page_icon="💸")
st.title("💸 AML dataset")
st.write(
    """
    This app visualizes data from [IBM Transactions for Anti Money Laundering (AML)](https://www.kaggle.com/datasets/ealtman2019/ibm-transactions-for-anti-money-laundering-aml/data).
    It helps analyze financial transactions to detect potential money laundering activities. 
    Use the interactive widgets below to explore patterns and insights!
    """
)

@st.cache_data
def get_txn_data():
    url = "https://drive.google.com/file/d/1kUK0voPeSkHvAQ57nqC7xXvQ4XjL6r3K/view?usp=drive_link"
    output = "HI-Small_Trans.csv"
    gdown.download(url, output, quiet=False, fuzzy=True)
    df = pd.read_csv(output, nrows=10000)
    return df

df = get_txn_data()

# Ensure 'payment' column exists before using multiselect
if "Payment Format" in df.columns:
    Payment = st.multiselect(
        "Payment Format",
        df["Payment Format"].unique(),
        ["ACH", "Bitcoin", "Cheque", "Reinvestment", "Credit Card", "Wire", "Cash"],
    )

    # Filter data based on selected payments
    df_filtered = df[df["Payment Format"].isin(Payment)]

    # Display the data as a table
    st.dataframe(df_filtered, use_container_width=True)
else:
    st.error("Column 'payment' not found in the dataset. Please check the dataset structure.")