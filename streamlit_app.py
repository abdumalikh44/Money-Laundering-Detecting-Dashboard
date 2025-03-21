import streamlit as st
import joblib
import pandas as pd

# Load the trained model (Pipeline with preprocessing)
model = joblib.load("lightgbm_pipeline.joblib")

# Streamlit App
st.title("Money Laundering Detection Dashboard")

st.write("Masukkan informasi transaksi untuk mendeteksi apakah transaksi ini mencurigakan.")

# Form untuk input data transaksi
with st.form("transaction_form"):
    from_bank = st.number_input("From Bank ID", min_value=0, step=1)
    account = st.text_input("Account Number")
    to_bank = st.number_input("To Bank ID", min_value=0, step=1)
    payment_format = st.selectbox("Payment Format", ["ACH", "Credit Card", "Cheque", "Reinvestment", "Cash"])
    amount = st.number_input("Transaction Amount", min_value=0.01, step=0.01)

    submitted = st.form_submit_button("Deteksi Money Laundering")

if submitted:
    input_data = pd.DataFrame({
        "From Bank": [from_bank],
        "Account": [account],
        "To Bank": [to_bank],
        "Receiving Currency": ["US Dollar"],
        "Payment Currency": ["US Dollar"],
        "Payment Format": [payment_format],
        "Amount": [amount]
    })

    # Prediksi menggunakan model yang sudah dilatih
    prediction = model.predict(input_data)

    # Tampilkan hasil prediksi
    st.write("### Hasil Prediksi:")
    if prediction[0] == 1:
        st.error("🚨 Transaksi ini dicurigai sebagai Money Laundering!")
    else:
        st.success("✅ Transaksi ini **tidak mencurigakan**.")
