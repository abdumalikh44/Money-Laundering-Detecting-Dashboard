import pandas as pd
import streamlit as st
import joblib  # Change from pickle to joblib
import matplotlib.pyplot as plt

st.set_page_config(page_title="Money Laundering Detection", layout="wide")
st.title("Money Laundering Detection App")

st.sidebar.header("How It Works")
st.sidebar.write("""
This app allows you to detect suspicious transactions using a LightGBM model.
1. **Upload your dataset**: Ensure it includes necessary transaction features.
2. The app will classify transactions as either legitimate or potential money laundering cases.
""")

st.sidebar.header("Upload Your Dataset")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file is not None:
    transaction_data = pd.read_csv(uploaded_file)
    st.success("Dataset loaded successfully!")

    st.subheader("Dataset Overview")
    st.write(transaction_data.head())
    st.write(f"Total Transactions: {len(transaction_data)}")

    if 'Is Laundering' in transaction_data.columns:
        legit = transaction_data[transaction_data['Is Laundering'] == 0]
        laundering = transaction_data[transaction_data['Is Laundering'] == 1]
    else:
        legit = transaction_data
        laundering = pd.DataFrame()

    count_legit = legit.shape[0]
    count_laundering = laundering.shape[0]

    st.write(f"**Total Legal Transactions:** {count_legit}")
    st.write(f"**Total Suspicious Transactions:** {count_laundering}")

    st.subheader("Transaction Distribution")
    labels = ['Legal', 'Suspicious']
    sizes = [count_legit, count_laundering]
    colors = ['#4CAF50', '#FF5733']

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)

    if 'Date' in transaction_data.columns and not laundering.empty:
        st.subheader("Suspicious Transactions Over Time")
        
        laundering = laundering.dropna(subset=['Date'])
        laundering['Date'] = pd.to_datetime(laundering['Date'], errors='coerce')
        laundering = laundering.dropna(subset=['Date'])

        fig, ax = plt.subplots()
        laundering['Date'].value_counts().sort_index().plot(kind='bar', color='#bb5b0c', ax=ax)

        for p in ax.patches:
            ax.annotate(f'{p.get_height()}',
                        (p.get_x() + p.get_width() / 2., p.get_height()), 
                        ha='center', va='baseline', fontsize=12, color='#ff7200', fontweight='bold',  
                        xytext=(0, 3), textcoords='offset points')

        st.pyplot(fig)

    model = joblib.load("lightgbm_model.joblib")  

    feature_columns = transaction_data.columns.drop('Is Laundering', errors='ignore')
    user_data = transaction_data[feature_columns]

    user_data.fillna(0, inplace=True)

    # Ambil model LightGBM dari dalam pipeline jika ada
    lgbm_model = model.named_steps.get("classifier", model)  

    if hasattr(lgbm_model, "feature_name_"):
        missing_cols = set(lgbm_model.feature_name_) - set(user_data.columns)
    else:
        missing_cols = set()

    for col in missing_cols:
        user_data[col] = 0 

    # Transformasi data menggunakan pipeline agar sesuai dengan model
    user_data = model.transform(user_data)

    try:
        predictions = model.predict(user_data)
        transaction_data['Prediction'] = ["Suspicious" if pred == 1 else "Legal" for pred in predictions]
    except Exception as e:
        st.error(f"Prediction error: {e}")
        transaction_data['Prediction'] = "Error"

    st.subheader("Prediction Results")
    result_df = transaction_data[['Prediction']].copy()
    st.dataframe(result_df)

    prediction_count = result_df['Prediction'].value_counts()
    st.write(f"**Predicted Legal Transactions:** {prediction_count.get('Legal', 0)}")
    st.write(f"**Predicted Suspicious Transactions:** {prediction_count.get('Suspicious', 0)}")

else:
    st.error("Please upload a dataset to proceed.")
