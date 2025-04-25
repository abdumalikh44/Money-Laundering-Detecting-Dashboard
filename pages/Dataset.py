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

# Convert 'Timestamp' to datetime format
df["Timestamp"] = pd.to_datetime(df["Timestamp"])

# Create a new column with only the date
df["Date"] = df["Timestamp"].dt.date

# Add a date picker to filter by transaction date
min_date = df["Date"].min()
max_date = df["Date"].max()
selected_date = st.date_input("Filter by Date", min_value=min_date, max_value=max_date, value=min_date)

# Apply the date filter
df = df[df["Date"] == selected_date]

# Ensure 'Payment Format' column exists before using multiselect
if "Payment Format" in df.columns:
    Payment = st.multiselect(
        "Payment Format",
        df["Payment Format"].unique(),
        ["ACH", "Bitcoin", "Cheque", "Reinvestment", "Credit Card", "Wire", "Cash"],
    )

    # Filter data based on selected payments
    df = df[df["Payment Format"].isin(Payment)]

if "Is Laundering" in df.columns:
    laundering_options = st.multiselect(
        "Filter by 'Is Laundering' label",
        options=sorted(df["Is Laundering"].unique()),
        default=sorted(df["Is Laundering"].unique()),
        format_func=lambda x: "Laundering (1)" if x == 1 else "Not Laundering (0)"
    )
    df = df[df["Is Laundering"].isin(laundering_options)]
else:
    st.error("Column 'Is Laundering' not found in the dataset. Please check the dataset structure.")

# Display the filtered data
st.dataframe(df.drop(columns=["Timestamp"]), use_container_width=True)
