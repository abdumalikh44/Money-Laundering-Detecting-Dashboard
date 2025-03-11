import streamlit as st
import joblib
import pandas as pd

# Load the saved model (which already includes preprocessing)
model = joblib.load("lightgbm_pipeline.joblib")

# Streamlit App
st.title("Money Laundering Detection Dashboard")

# Upload CSV file
uploaded_file = st.file_uploader("Upload transaction data (CSV)", type=["csv"])

if uploaded_file is not None:
    # Read CSV
    df = pd.read_csv(uploaded_file)

    # Ensure the data structure is compatible with training
    st.write("Preview of uploaded data:")
    st.write(df.head())

    # Predict
    if st.button("Detect Money Laundering"):
        predictions = model.predict(df)  # No need for preprocessing (already in Pipeline)
        df["Prediction"] = predictions

        # Display results
        st.write("Prediction Results:")
        st.write(df)

        # Show summary
        st.write("Suspicious Transactions Count:")
        st.write(df["Prediction"].value_counts())

        # Download option
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Download Predictions", data=csv, file_name="predictions.csv", mime="text/csv")
