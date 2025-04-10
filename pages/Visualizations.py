import streamlit as st
import pandas as pd
import gdown
from pyecharts.charts import Bar
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
    df = pd.read_csv(output, nrows=10000)

    # Ensure 'Timestamp' column is in datetime format
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])


    return df

df = get_txn_data()

# Group transactions by day
df_grouped = df.groupby(df["Timestamp"].dt.floor("D"))["Amount Paid"].count().reset_index()

# Convert data to lists for visualization
dates = df_grouped["Timestamp"].dt.strftime("%Y-%m-%d").tolist()  # Format date as YYYY-MM-DD
amounts = df_grouped["Amount Paid"].tolist()

# Create a pyecharts line chart
c = (
    Line()
    .add_xaxis(dates)
    .add_yaxis("Total Amount Paid", amounts)
    .set_global_opts(
        title_opts=opts.TitleOpts(title="Daily Transaction Trend"),
        xaxis_opts=opts.AxisOpts(name="Date"),
        yaxis_opts=opts.AxisOpts(name="Total Amount Paid"),
    )
)

# Display chart in Streamlit
st_pyecharts(c)

# Count transactions per day and get the top 5 most frequent dates
top_dates = df["Timestamp"].dt.date.value_counts().head(5).reset_index()
top_dates.columns = ["Timestamp", "Transaction Count"]

# Convert data to lists for visualization
dates = top_dates["Timestamp"].astype(str).tolist()  # Convert dates to string format
counts = top_dates["Transaction Count"].tolist()

# Create a pyecharts bar chart
bar_chart = (
    Bar()
    .add_xaxis(dates)
    .add_yaxis("Number of Transactions", counts, color="#FFBF00")
    .set_global_opts(
        title_opts=opts.TitleOpts(title="Top 5 Transaction Dates", subtitle="Most Frequent Transaction Days"),
        xaxis_opts=opts.AxisOpts(name="Date"),
        yaxis_opts=opts.AxisOpts(name="Transaction Count"),
        toolbox_opts=opts.ToolboxOpts(),  # Add toolbox for interactions
    )
)

# Display the chart in Streamlit
st_pyecharts(bar_chart, key="bar_chart")