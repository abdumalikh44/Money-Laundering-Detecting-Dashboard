import streamlit as st
import pandas as pd
import gdown
from pyecharts.charts import Bar
from pyecharts import options as opts
from streamlit_echarts import st_pyecharts

# Set up Streamlit page
st.set_page_config(page_title="AML Dashboard", page_icon="📊")
st.title("📊 AML Data Visualization")

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

df = get_txn_data()

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
    .add_yaxis("Number of Transactions", date_counts, color="#FFBF00")
    .set_global_opts(
        toolbox_opts=opts.ToolboxOpts(),
    )
)

st.subheader("Jumlah Transaksi")
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
        .add_yaxis("Jumlah Transaksi", payment_values, color="#00BFFF")
        .set_global_opts(
            toolbox_opts=opts.ToolboxOpts(),
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
    # Map 0/1 to labels first
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
        )
    )

    st.subheader("🧹 Perbandingan Laundering vs Non-Laundering")
    st_pyecharts(laundering_bar_chart, key="laundering_bar")
else:
    st.error("Kolom 'Is Laundering' tidak ditemukan dalam dataset.")