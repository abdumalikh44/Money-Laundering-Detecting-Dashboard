import streamlit as st
import pandas as pd
import lightgbm as lgb
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

# Load trained model
@st.cache_resource
def load_model():
    model = joblib.load("lightgbm_model.joblib")
    return model

# Predict function
def predict(data, model):
    return model.predict(data)

# Streamlit App
st.title("Money Laundering Detection Dashboard")

# File Upload
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("### Uploaded Data Preview:")
    st.dataframe(df.head())
    
    # Load Model
    model = load_model()
    
    # Predict
    if st.button("Detect Money Laundering"):
        predictions = predict(df, model)
        df["Prediction"] = predictions
        
        # Show results
        st.write("### Detection Results:")
        st.dataframe(df)
        
        # Visualization
        st.write("### Prediction Distribution:")
        fig, ax = plt.subplots()
        sns.countplot(x=predictions, ax=ax)
        st.pyplot(fig)
        
        st.write("### Feature Importance:")
        fig, ax = plt.subplots()
        lgb.plot_importance(model, ax=ax)
        st.pyplot(fig)
