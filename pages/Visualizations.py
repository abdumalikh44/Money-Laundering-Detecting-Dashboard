import streamlit as st
import pandas as pd
import gdown
from pyecharts.charts import Line
from pyecharts import options as opts
from streamlit_echarts import st_pyecharts

# Set up Streamlit page
st.set_page_config(page_title="AML Dashboard", page_icon="📊")
st.title("📊 AML Data Visualization")

@st.cache_data
def get_txn_data():
    url = "https://drive.google.com/file/d/1kUK0voPeSkHvAQ57nqC7xXvQ4XjL6r3K/view?usp=drive_link"
    output = "HI-Small_Trans.csv"
    gdown.download(url, output, quiet=False, fuzzy=True)
    df = pd.read_csv(output, nrows=1000000)

    # Ensure the Date column is in datetime format
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])

    return df

df = get_txn_data()

# Group data by Date and sum the transaction amounts
df_grouped = df.groupby(df["Timestamp"].dt.date)["Amount Paid"].sum().reset_index()

# Convert data to lists for pyecharts
dates = df_grouped["Timestamp"].astype(str).tolist()  # Convert dates to string for plotting
amounts = df_grouped["Amount Paid"].tolist()

# Create a pyecharts line chart
c = (
    Line()
    .add_xaxis(dates)
    .add_yaxis("Total Transaction Amount", amounts)
    .set_global_opts(
        title_opts=opts.TitleOpts(title="Transaction Trend Over Time"),
        xaxis_opts=opts.AxisOpts(name="Date"),
        yaxis_opts=opts.AxisOpts(name="Total Amount"),
    )
)

# Display chart in Streamlit
st_pyecharts(c)