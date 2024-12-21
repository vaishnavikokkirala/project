import streamlit as st
import requests

# Streamlit app title
st.title("Bank Marketing Prediction")
st.write("This app predicts whether a client will subscribe to a term deposit.")

# Input fields for user data
client_id = st.number_input("Client ID", min_value=1, value=1, step=1)
age = st.number_input("Age", min_value=18, value=30, step=1)
job = st.selectbox("Job", ["admin", "technician", "management", "retired", "services", "student", "blue-collar", "self-employed", "unemployed", "unknown"])
marital_status = st.selectbox("Marital Status", ["single", "married", "divorced"])
education = st.selectbox("Education", ["primary", "secondary", "tertiary", "unknown"])
loan_status = st.selectbox("Loan Status", ["yes", "no"])
balance = st.number_input("Balance", value=0.0)
housing = st.selectbox("Housing Loan", ["yes", "no"])
loan = st.selectbox("Personal Loan", ["yes", "no"])
contact = st.selectbox("Contact Type", ["cellular", "telephone", "unknown"])
day = st.number_input("Day of Contact", min_value=1, max_value=31, value=15, step=1)
month = st.selectbox("Month", ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"])
duration = st.number_input("Call Duration (seconds)", value=0.0)
campaign = st.number_input("Number of Contacts during Campaign", min_value=1, value=1, step=1)
pdays = st.number_input("Days since Last Contact", value=-1)
previous = st.number_input("Number of Previous Contacts", min_value=0, value=0)
poutcome = st.selectbox("Outcome of Previous Campaign", ["success", "failure", "other", "unknown"])

# Prediction button
if st.button("Predict"):
    # Prepare the data payload
    data = {
        "client_id": client_id,
        "age": age,
        "job": job,
        "marital_status": marital_status,
        "education": education,
        "loan_status": loan_status,
        "balance": balance,
        "housing": housing,
        "loan": loan,
        "contact": contact,
        "day": day,
        "month": month,
        "duration": duration,
        "campaign": campaign,
        "pdays": pdays,
        "previous": previous,
        "poutcome": poutcome
    }

    # Make a request to the FastAPI endpoint
    try:
        response = requests.post("https://project-m5ep.onrender.com/predict/", json=data)
        if response.status_code == 200:
            prediction = response.json()["prediction"]
            st.success(f"The prediction is: {prediction}")
        else:
            st.error(f"Error: {response.json()['detail']}")
    except Exception as e:
        st.error(f"An error occurred: {e}")
