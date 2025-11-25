import streamlit as st
from PIL import Image

# --- Page Configuration ---
st.set_page_config(page_title="Money Laundering Detection Dashboard", page_icon="💸", layout="wide")

# --- Hero Section ---
st.title("💸 Money Laundering Detection Dashboard")
st.markdown("### 🚨 Real-time Insights into Suspicious Financial Transactions")
st.markdown("Uncover anomalies and potential laundering patterns using AI-powered analysis on synthetic transaction data.")

# --- Image or Illustration ---
image_url = "https://raw.githubusercontent.com/abdumalikh44/Money-Laundering-Detecting-Dashboard/main/Dashboard Ilustration.png"
st.image(image_url, use_container_width=True, caption="Interactive AML Dashboard")

# --- Quick Stats ---
col1, col2, col3 = st.columns(3)
col1.metric("📄 Records", "2,000,000")
col2.metric("🧠 Model Used", "LightGBM")
col3.metric("✅ Accuracy", "89.0%")

# --- Project Overview Expander ---
with st.expander("ℹ️ About This Project"):
    st.write("""
        This dashboard is designed to explore synthetic financial transaction data and apply AI techniques 
        to detect potential money laundering activity. Built using LightGBM and visualized through Streamlit, 
        the system offers insights through classification results, evaluation metrics, and an interactive UI.
    """)

# --- Navigation Prompt ---
st.markdown("### 🔍 Explore the Dashboard")
st.write("Use the sidebar to navigate through the following sections:")
st.markdown("""
- 📁 Dataset Overview  
- 📈 Model Predictions
- 📊 Visualizations  
""")

# Optional button-based navigation (if `st.switch_page` or multipage setup is used)
# if st.button("📊 Go to Visualizations"):
#     st.switch_page("pages/2_📊_Visualizations.py")

# --- GitHub Feedback Box ---
st.info(
    """
    👾 Missing a feature or found a bug?  
    [Open a GitHub issue here](https://github.com/abdumalikh44/Money-Laundering-Detecting-Dashboard/issues)
    """,
    icon="🛠️",
)

# --- Sidebar Prompt ---
st.sidebar.success("Select one of the pages above to get started.")
