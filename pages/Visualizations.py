import streamlit as st
import pandas as pd
import gdown
from pyecharts.charts import Bar
from pyecharts import options as opts
from streamlit_echarts import st_pyecharts

# Set up Streamlit page
st.set_page_config(page_title="AML Dashboard", page_icon="📊")
st.title("📊 AML Data Visualization")
st.write("[Dataset Visualization for Anti Money Laundering (AML) Detection](https://money-laundering-detection-dashboard.streamlit.app/Dataset)")

# ===========================
# Load Data with Caching
# ===========================
@st.cache_data
def get_txn_data():
    url = "https://drive.google.com/file/d/1kUK0voPeSkHvAQ57nqC7xXvQ4XjL6r3K/view?usp=drive_link"
    output = "HI-Small_Trans.csv"
    gdown.download(url, output, quiet=False, fuzzy=True)
    df = pd.read_csv(output, nrows=100000)

    # Convert timestamp column to datetime
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
    return df

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

# ===========================
# Load and Filter Data
# ===========================
df = get_txn_data()
df = filter_by_date(df)  # Call the date filter here
df = filter_by_laundering(df)  # Apply filter here

# ===========================
# Chart: Top 5 Most Active Dates
# ===========================
top_dates = df["Timestamp"].dt.date.value_counts().head(5).reset_index()
top_dates.columns = ["Date", "Transaction Count"]

date_labels = top_dates["Date"].astype(str).tolist()
date_counts = top_dates["Transaction Count"].tolist()

date_bar_chart = (
    Bar()
    .add_xaxis(date_labels)
    .add_yaxis("Jumlah Transaksi", date_counts, color="#FFBF00")
    .set_global_opts(
        toolbox_opts=opts.ToolboxOpts(),
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=45))
    )
)

st.subheader("Jumlah Transaksi per Hari")
st_pyecharts(date_bar_chart, key="bar_chart")

# ===========================
# Chart: Transactions per Payment Format
# ===========================
if "Payment Format" in df.columns:
    payment_counts = df["Payment Format"].value_counts().reset_index()
    payment_counts.columns = ["Payment Format", "Count"]

    payment_labels = payment_counts["Payment Format"].tolist()
    payment_values = payment_counts["Count"].tolist()

    payment_bar_chart = (
    Bar()
    .add_xaxis(payment_labels)
    .add_yaxis(
        "Jumlah Transaksi",
        payment_values,
        color="#00BFFF",
        label_opts=opts.LabelOpts(is_show=True, position="top")
    )
    .set_global_opts(
        toolbox_opts=opts.ToolboxOpts(),
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=45))
    )
)
    st.subheader("Jumlah Transaksi per Payment Format")
    st_pyecharts(payment_bar_chart, key="payment_bar")
else:
    st.error("Kolom 'Payment Format' tidak ditemukan dalam dataset.")

# ===========================
# Chart: Laundering vs Non-Laundering
# ===========================
if "Is Laundering" in df.columns:
    # Map 0 and 1 first

    df["Laundering Label"] = df["Is Laundering"].map({0: "Non-Laundering", 1: "Laundering"})

    laundering_counts = df["Laundering Label"].value_counts().reset_index()
    laundering_counts.columns = ["Laundering Label", "Count"]

    laundering_labels = laundering_counts["Laundering Label"].tolist()
    laundering_values = laundering_counts["Count"].tolist()

    laundering_bar_chart = (
        Bar()
        .add_xaxis(laundering_labels)
        .add_yaxis("Jumlah", laundering_values, color="#FF6347")
        .set_global_opts(
            toolbox_opts=opts.ToolboxOpts(),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=45))
        )
    )

    st.subheader("Non-Laundering vs Laundering")
    st_pyecharts(laundering_bar_chart, key="laundering_bar")
else:
    st.error("Kolom 'Is Laundering' tidak ditemukan dalam dataset.")
