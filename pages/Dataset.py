import streamlit as st
import pandas as pd
import altair as alt
import gdown

# --------------------- Setup ---------------------
st.set_page_config(page_title="AML Dataset", page_icon="💸")
st.title("💸 AML DATASET")
st.page_link("pages/Visualizations.py", label="🔍 View Visualizations", icon="📊")

st.write("""
This app visualizes data from [IBM Transactions for Anti Money Laundering (AML)](https://www.kaggle.com/datasets/ealtman2019/ibm-transactions-for-anti-money-laundering-aml/data).
It helps analyze financial transactions to detect potential money laundering activities.
Use the interactive widgets below to explore patterns and insights!
""")

# --------------------- Data Loader ---------------------
@st.cache_data
def load_data():
    url = "https://drive.google.com/file/d/1kUK0voPeSkHvAQ57nqC7xXvQ4XjL6r3K/view?usp=drive_link"
    output = "HI-Small_Trans.csv"
    gdown.download(url, output, quiet=False, fuzzy=True)
    df = pd.read_csv(output, nrows=100000)

    # Convert timestamp to datetime
    if "Timestamp" in df.columns:
        df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors='coerce')
        df["Date"] = df["Timestamp"].dt.date
    return df

df = load_data()

# --------------------- Date Filter ---------------------
def filter_by_date(df):
    if "Date" in df.columns:
        min_date = pd.to_datetime(df["Date"].min()).date()
        max_date = pd.to_datetime(df["Date"].max()).date()
        selected_date = st.date_input("Filter by Date", min_value=min_date, max_value=max_date, value=min_date)
        df = df[df["Date"] == selected_date]
    else:
        st.warning("No 'Date' column found in the dataset.")
    return df

# --------------------- Payment Format Filter ---------------------
def filter_by_payment(df):
    if "Payment Format" in df.columns:
        options = df["Payment Format"].dropna().unique()
        default_options = ["ACH", "Bitcoin", "Cheque", "Reinvestment", "Credit Card", "Wire", "Cash"]
        selected = st.multiselect("Payment Format", options=options, default=[opt for opt in default_options if opt in options])
        df = df[df["Payment Format"].isin(selected)]
    else:
        st.warning("No 'Payment Format' column found in the dataset.")
    return df

# --------------------- Is Laundering Filter ---------------------
def filter_by_laundering(df):
    if "Is Laundering" in df.columns:
        laundering_options = st.multiselect(
            "Filter by 'Is Laundering' label",
            options=sorted(df["Is Laundering"].dropna().unique()),
            default=sorted(df["Is Laundering"].dropna().unique()),
            format_func=lambda x: "Laundering (1)" if x == 1 else "Not Laundering (0)"
        )
        df = df[df["Is Laundering"].isin(laundering_options)]
    else:
        st.warning("No 'Is Laundering' column found in the dataset.")
    return df

# --------------------- Apply Filters ---------------------
df = filter_by_date(df)
df = filter_by_payment(df)
df = filter_by_laundering(df)

# --------------------- Display Table ---------------------
if not df.empty:
    st.dataframe(df.drop(columns=["Timestamp"]), use_container_width=True)
else:
    st.info("No data to display for the selected filters.")
