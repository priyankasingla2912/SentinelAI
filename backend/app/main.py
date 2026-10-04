import json

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import pandas as pd
import joblib
import shap
from app.database import (
    save_prediction,
    get_predictions, 
    get_prediction_stats,
    create_prediction_table,
    get_prediction_by_id
)

app = FastAPI(
    title="SentinelAI Fraud Intelligence API",
    description="AI-powered fraud detection and risk analysis API",
    version="1.0.0"
)
# ==========================================
# Initialize Database
# ==========================================

create_prediction_table()
# ==========================================
# CORS Configuration
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# Load Saved Model
# ==========================================

MODEL_PATH = "../models/fraud_random_forest.pkl"
THRESHOLD_PATH = "../models/threshold.txt"

model = joblib.load(MODEL_PATH)

with open(THRESHOLD_PATH, "r") as f:
    THRESHOLD = float(f.read().strip())

print("Random Forest model loaded successfully!")
print("Fraud threshold:", THRESHOLD)


# ==========================================
# Create SHAP Explainer
# ==========================================

explainer = shap.TreeExplainer(model)

print("SHAP Explainer created successfully!")


# ==========================================
# Transaction Data Model
# ==========================================

class Transaction(BaseModel):

    Time: float = Field(..., ge=0)

    V1: float
    V2: float
    V3: float
    V4: float
    V5: float
    V6: float
    V7: float
    V8: float
    V9: float
    V10: float
    V11: float
    V12: float
    V13: float
    V14: float
    V15: float
    V16: float
    V17: float
    V18: float
    V19: float
    V20: float
    V21: float
    V22: float
    V23: float
    V24: float
    V25: float
    V26: float
    V27: float
    V28: float

    Amount: float = Field(..., ge=0)


# ==========================================
# Home Endpoint
# ==========================================

@app.get("/")
def home():

    return {
        "message": "Welcome to SentinelAI!",
        "status": "API is running",
        "service": "Fraud Intelligence Platform"
    }


# ==========================================
# Health Check
# ==========================================

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }
# ==========================================
# Prediction History Endpoint
# ==========================================

@app.get("/history")
def history(limit: int = Query(20, ge=1, le=100)):
    rows = get_predictions(limit)

    predictions = []

    for row in rows:
        shap_factors = None

        if row[7]:
            try:
                shap_factors = json.loads(row[7])
            except json.JSONDecodeError:
                shap_factors = None

        predictions.append({
            "id": row[0],
            "amount": row[1],
            "fraud_probability": row[2],
            "threshold": row[3],
            "prediction": row[4],
            "risk_level": row[5],
            "recommended_action": row[6],
            "shap_factors": shap_factors,
            "created_at": row[8]
        })

    return {
        "count": len(predictions),
        "predictions": predictions
    }

# ==========================================
# Single Transaction Details Endpoint
# ==========================================

@app.get("/history/{prediction_id}")
def prediction_details(prediction_id: int):
    row = get_prediction_by_id(prediction_id)

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    shap_factors = None

    if row[7]:
        try:
            shap_factors = json.loads(row[7])
        except json.JSONDecodeError:
            shap_factors = None

    return {
        "id": row[0],
        "amount": row[1],
        "fraud_probability": row[2],
        "threshold": row[3],
        "prediction": row[4],
        "risk_level": row[5],
        "recommended_action": row[6],
        "shap_factors": shap_factors,
        "created_at": row[8]
    }
# ==========================================
# Prediction Statistics Endpoint
# ==========================================

@app.get("/stats")
def stats():

    return get_prediction_stats()
# ==========================================
# Risk Level
# ==========================================

def get_risk_level(probability):

    if probability >= 0.90:
        return "CRITICAL"

    elif probability >= 0.60:
        return "HIGH"

    elif probability >= 0.30:
        return "MEDIUM"

    else:
        return "LOW"


# ==========================================
# Prediction Endpoint
# ==========================================

@app.post("/predict")
def predict(transaction: Transaction):

    # Convert transaction to dictionary
    transaction_data = transaction.model_dump()

    # Convert to DataFrame
    input_data = pd.DataFrame([transaction_data])

    # ==========================================
    # Fraud Probability
    # ==========================================

    fraud_probability = model.predict_proba(input_data)[0][1]

    # ==========================================
    # Prediction
    # ==========================================

    if fraud_probability >= THRESHOLD:
        prediction = "FRAUD"
    else:
        prediction = "LEGITIMATE"

    # ==========================================
    # Risk Level
    # ==========================================

    risk_level = get_risk_level(fraud_probability)

    # ==========================================
    # SHAP Explanation
    # ==========================================

    shap_values = explainer.shap_values(input_data)

    if isinstance(shap_values, list):
        fraud_shap = shap_values[1][0]
    else:
        fraud_shap = shap_values[0, :, 1]

    # ==========================================
    # Create Explanation Table
    # ==========================================

    explanation = pd.DataFrame({
        "Feature": input_data.columns,
        "SHAP_Value": fraud_shap
    })

    # Calculate absolute importance
    explanation["Absolute_SHAP"] = explanation["SHAP_Value"].abs()

    # Sort by importance
    explanation = explanation.sort_values(
        "Absolute_SHAP",
        ascending=False
    )

    # ==========================================
    # Top 5 Risk Factors
    # ==========================================

    top_factors = []

    for _, row in explanation.head(5).iterrows():

        top_factors.append({
            "feature": row["Feature"],
            "shap_value": round(
                float(row["SHAP_Value"]),
                6
            )
        })

    # ==========================================
    # ==========================================
    # Recommended Action
    # ==========================================

    if risk_level == "CRITICAL":

        recommended_action = (
            "Block transaction and immediately "
            "escalate to fraud analyst."
        )

    elif risk_level == "HIGH":

        recommended_action = (
            "Hold transaction for additional "
            "fraud verification."
        )

    elif risk_level == "MEDIUM":

        recommended_action = (
            "Monitor transaction and perform "
            "additional verification."
        )

    else:

        recommended_action = (
            "Allow transaction and continue "
            "normal monitoring."
        )


    # ==========================================
    # Save Prediction to Database
    # ==========================================

    save_prediction(
        amount=transaction.Amount,
        fraud_probability=float(fraud_probability),
        threshold=THRESHOLD,
        prediction=prediction,
        risk_level=risk_level,
        recommended_action=recommended_action,
        shap_factors=top_factors
    )


    # ==========================================
    # Final API Response
    # ==========================================

    return {

        "amount": transaction.Amount,

        "fraud_probability": round(
            float(fraud_probability),
            4
        ),

        "threshold": THRESHOLD,

        "prediction": prediction,

        "risk_level": risk_level,

        "top_risk_factors": top_factors,

        "recommended_action": recommended_action
    }