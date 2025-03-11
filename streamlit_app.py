import streamlit as st
import pandas as pd
import lightgbm as lgb
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Define categorical columns (ensure these match the training data)
cat = ['From Bank', 'Account', 'To Bank', 'Account.1', 'Amount Received', 'Receiving Currency', 'Payment Currency', 'Date']  # Replace with actual categorical column names

ohe = Pipeline([('Encoder', OneHotEncoder(drop='first', handle_unknown='ignore'))])
transformer = ColumnTransformer([('One Hot Encoding', ohe, cat)])

# Load trained model
@st.cache_resource
def load_model():
    model = joblib.load("lightgbm_model.joblib")
    return model

# Predict function
def predict(data, model):
    transformed_data = transformer.transform(data)  # Apply the same preprocessing as training
    return model.predict(transformed_data)

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
    
    # Fit transformer on uploaded data (only if necessary)
    transformer.fit(df)
    
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
