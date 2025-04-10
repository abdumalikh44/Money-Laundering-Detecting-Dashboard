import streamlit as st

# Page Title
st.title("Welcome to the Money Laundering Detection Dashboard")

# Info box with link to GitHub issues
st.info(
    """
    Missing a feature or found a bug?  
    [Open a GitHub issue here](https://github.com/abdumalikh44/Money-Laundering-Detecting-Dashboard/issues) 
    """,
    icon="👾",
)

# Introduction / Welcome message
st.write(
    """
    ## Skripsi Dashboard

    Welcome to the interactive dashboard for my final thesis project! 👋  
    This app showcases key visualizations and insights from synthetic financial transaction data,  
    focusing on identifying potential money laundering patterns. 💸

    Use the sidebar to navigate through different sections including the dataset, model evaluation, and visualizations.
    """
)
