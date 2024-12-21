from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib

# Load the saved model
model_path = "final_model.pkl"
try:
    model = joblib.load(model_path)
    # Get the feature names used during training
    expected_features = model.feature_names_in_
except FileNotFoundError:
    raise RuntimeError(f"Model file '{model_path}' not found. Please ensure the file exists.")

# Define input schema
class ClientData(BaseModel):
    client_id: int
    age: int
    job: str
    marital_status: str
    education: str
    loan_status: str
    balance: float
    housing: str
    loan: str
    contact: str
    day: int
    month: str
    duration: float
    campaign: int
    pdays: int
    previous: int
    poutcome: str

# Initialize FastAPI app
app = FastAPI()

@app.get("/")
def home():
    return {"message": "FastAPI is running for the prediction model!"}

@app.post("/predict/")
def predict(data: ClientData):
    """
    Predict the outcome using the provided client data and ensure feature alignment.
    """
    try:
        # Convert input data to DataFrame
        input_data = pd.DataFrame([data.dict()])

        # Drop `client_id` since it's not used for prediction
        input_data = input_data.drop(columns=["client_id"])

        # Align features to match the model's expected input
        input_data = input_data.reindex(columns=expected_features)

        # Perform prediction
        prediction = model.predict(input_data)[0]  # Extract the single prediction

        # Convert prediction to "yes" or "no"
        result = "yes" if prediction == 1 else "no"

        return {"prediction": result}
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: Missing or mismatched feature(s): {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")
