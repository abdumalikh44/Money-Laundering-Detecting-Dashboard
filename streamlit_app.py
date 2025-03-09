import pandas as pd
import streamlit as st
import pickle
import matplotlib.pyplot as plt

# Streamlit UI Configuration
st.set_page_config(page_title="Money Laundering Detection", layout="wide")
st.title("Money Laundering Detection App")

# Sidebar Explanation
st.sidebar.header("How It Works")
st.sidebar.write("""
This app allows you to detect suspicious transactions using a LightGBM model.
1. **Upload your dataset**: Ensure it includes necessary transaction features.
2. The app will classify transactions as either legitimate or potential money laundering cases.
""")

# Upload Dataset
st.sidebar.header("Upload Your Dataset")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file is not None:
    # Load dataset
    transaction_data = pd.read_csv(uploaded_file)
    st.success("Dataset loaded successfully!")

    # Display dataset overview
    st.subheader("Dataset Overview")
    st.write(transaction_data.head())
    st.write(f"Total Transactions: {len(transaction_data)}")

    # Check if 'Is Laundering' column exists
    if 'Is Laundering' in transaction_data.columns:
        legit = transaction_data[transaction_data['Is Laundering'] == 0]
        laundering = transaction_data[transaction_data['Is Laundering'] == 1]
    else:
        legit = transaction_data
        laundering = pd.DataFrame()

    count_legit = legit.shape[0]
    count_laundering = laundering.shape[0]

    # Display transaction counts
    st.write(f"**Total Legitimate Transactions:** {count_legit}")
    st.write(f"**Total Suspicious Transactions:** {count_laundering}")

    # Visualization
    st.subheader("Transaction Distribution")
    labels = ['Legitimate', 'Suspicious']
    sizes = [count_legit, count_laundering]
    colors = ['#4CAF50', '#FF5733']
    
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Ensures a circular pie chart
    st.pyplot(fig)

    # Load the pre-trained LightGBM model
    with open("lgbm_pipeline.pkl", "rb") as file:
        model = pickle.load(file)

    # Prepare features for prediction
    feature_columns = transaction_data.columns.drop('Is Laundering', errors='ignore')
    user_data = transaction_data[feature_columns]
    predictions = model.predict(user_data)

    # Add predictions to the dataframe
    transaction_data['Prediction'] = ["Suspicious" if pred == 1 else "Legitimate" for pred in predictions]

    # Display prediction results
    st.subheader("Prediction Results")
    result_df = transaction_data[['Prediction']].copy()
    st.dataframe(result_df)

    # Count the predictions
    prediction_count = result_df['Prediction'].value_counts()
    st.write(f"**Predicted Legitimate Transactions:** {prediction_count.get('Legitimate', 0)}")
    st.write(f"**Predicted Suspicious Transactions:** {prediction_count.get('Suspicious', 0)}")

else:
    st.error("Please upload a dataset to proceed.")
