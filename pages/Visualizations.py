import streamlit as st
import pandas as pd
import gdown
from pyecharts.charts import Bar
from pyecharts import options as opts
from streamlit_echarts import st_pyecharts

# ----------------- Page Setup -----------------
st.set_page_config(page_title="AML Data Viz", page_icon="📊")
st.title("📊 Money Laundering Transaction Visualizer")
st.markdown("Gain insight into suspicious financial activity using real-time data filters and interactive charts.")

st.page_link("pages/Dataset Overview.py", label="📂 View Dataset Table")

# ----------------- Load Dataset with Caching -----------------
@st.cache_data
def get_txn_data():
    url = "https://drive.google.com/file/d/1kUK0voPeSkHvAQ57nqC7xXvQ4XjL6r3K/view?usp=drive_link"
    output = "HI-Small_Trans.csv"
    gdown.download(url, output, quiet=False, fuzzy=True)
    df = pd.read_csv(output, nrows=100000)

    if "Timestamp" in df.columns:
        df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors='coerce')
        df["Date"] = df["Timestamp"].dt.date
    return df

# ----------------- Filter by Date -----------------
def filter_by_date(df):
    if "Date" in df.columns:
        min_date = pd.to_datetime(df["Date"].min()).date()
        max_date = pd.to_datetime(df["Date"].max()).date()
        selected_date = st.date_input("📅 Filter by Transaction Date", min_value=min_date, max_value=max_date, value=min_date)
        df = df[df["Date"] == selected_date]
    else:
        st.warning("⚠️ Column 'Date' not found.")
    return df

# ----------------- Filter by Laundering Label -----------------
def filter_by_laundering(df):
    if "Is Laundering" in df.columns:
        laundering_options = st.multiselect(
            "🔍 Filter by Laundering Label",
            options=sorted(df["Is Laundering"].dropna().unique()),
            default=sorted(df["Is Laundering"].dropna().unique()),
            format_func=lambda x: "🟥 Laundering (1)" if x == 1 else "🟩 Not Laundering (0)"
        )
        df = df[df["Is Laundering"].isin(laundering_options)]
    else:
        st.warning("⚠️ Column 'Is Laundering' not found.")
    return df

# ----------------- Load + Filter Data -----------------
df = get_txn_data()
df = filter_by_date(df)
df = filter_by_laundering(df)

st.divider()

# ===========================
# Chart 1: Top Transaction Days
# ===========================
st.subheader("📈 Top 5 Days with Highest Transactions")

if "Timestamp" in df.columns:
    top_dates = df["Timestamp"].dt.date.value_counts().head(5).reset_index()
    top_dates.columns = ["Date", "Transaction Count"]

    date_labels = top_dates["Date"].astype(str).tolist()
    date_counts = top_dates["Transaction Count"].tolist()

    date_bar_chart = (
        Bar()
        .add_xaxis(date_labels)
        .add_yaxis("Number of Transactions", date_counts, color="#FFD700")
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Top Transaction Dates"),
            toolbox_opts=opts.ToolboxOpts(),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=45)),
            yaxis_opts=opts.AxisOpts(name="Transactions")
        )
    )
    st_pyecharts(date_bar_chart, key="bar_chart")
else:
    st.warning("⚠️ Timestamp data unavailable.")

# ===========================
# Chart 2: Transactions by Payment Format
# ===========================
st.subheader("Transaction Volume by Payment Format")

color_palette = [
"#87CEEB", "#FFA07A", "#90EE90", "#FFD700",
"#FF69B4", "#9370DB", "#00CED1", "#FFB6C1"
]

if "Payment Format" in df.columns:
    payment_counts = df["Payment Format"].value_counts().reset_index()
    payment_counts.columns = ["Payment Format", "Count"]
    payment_labels = payment_counts["Payment Format"].tolist()
    payment_values = payment_counts["Count"].tolist()

    bar = Bar()
    bar.add_xaxis(payment_labels)

    for i, (label, value) in enumerate(zip(payment_labels, payment_values)):
        bar.add_yaxis(
            label,
            [value],
            color=color_palette[i % len(color_palette)],
            label_opts=opts.LabelOpts(is_show=True, position="top")
        )

    bar.set_global_opts(
        title_opts=opts.TitleOpts(title="Transactions by Payment Format"),
        toolbox_opts=opts.ToolboxOpts(),
        legend_opts=opts.LegendOpts(is_show=False),
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=45)),
        yaxis_opts=opts.AxisOpts(name="Count")
    )

    st_pyecharts(bar, key="payment_bar")

else:
    st.warning("⚠️ 'Payment Format' column not found.")

# ===========================
# Chart 3: Laundering Distribution
# ===========================
st.subheader("🚨 Laundering vs Non-Laundering Distribution")

if "Is Laundering" in df.columns:
    df["Laundering Label"] = df["Is Laundering"].map({0: "Non-Laundering", 1: "Laundering"})
    laundering_counts = df["Laundering Label"].value_counts().reset_index()
    laundering_counts.columns = ["Laundering Label", "Count"]

    laundering_labels = laundering_counts["Laundering Label"].tolist()
    laundering_values = laundering_counts["Count"].tolist()

    laundering_bar_chart = (
        Bar()
        .add_xaxis(laundering_labels)
        .add_yaxis("Count", laundering_values, color="#FF6347")
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Laundering Status"),
            toolbox_opts=opts.ToolboxOpts(),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=0))
        )
    )
    st_pyecharts(laundering_bar_chart, key="laundering_bar")
else:
    st.warning("⚠️ 'Is Laundering' column not found.")
