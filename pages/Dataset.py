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
df["Date"] = df["Timestamp"].dt.date

# === Filter by 'Is Laundering' first ===
if "Is Laundering" in df.columns:
    laundering_options = st.multiselect(
        "Filter by 'Is Laundering' label",
        options=sorted(df["Is Laundering"].unique()),
        default=sorted(df["Is Laundering"].unique()),
    )
    # Filter the data based on selected laundering options
    df = df[df["Is Laundering"].isin(laundering_options)]

# Add a date picker to filter by transaction date
min_date = df["Date"].min()
max_date = df["Date"].max()
selected_date = st.date_input("Filter by Date", min_value=min_date, max_value=max_date, value=min_date)

# Apply the date filter
df = df[df["Date"] == selected_date]

# === Handle Payment Format ===
if "Payment Format" in df.columns:
    # Get the available payment options after filtering the data
    payment_options = df["Payment Format"].unique()

    if len(payment_options) > 0:
        # Set up the multiselect widget with the available payment options
        Payment = st.multiselect(
            "Payment Format",
            payment_options,
            default=payment_options.tolist(),  # Default is to select all available payment options
        )

        # Filter data based on selected payment formats
        if Payment:
            df = df[df["Payment Format"].isin(Payment)]
    else:
        # If there are no payment options available after filtering, show a message
        st.warning("No available payment formats after applying the selected filters.")

    # Display the filtered data
    if not df.empty:
        st.dataframe(df.drop(columns=["Timestamp"]), use_container_width=True)
    else:
        st.warning("No data available for the selected filters.")
else:
    st.error("Column 'Payment Format' not found in the dataset. Please check the dataset structure.")
