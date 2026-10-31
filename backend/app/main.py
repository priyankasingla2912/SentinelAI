import json
import requests
import os
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from app.knowledge.graph_workflow import run_investigation
from pathlib import Path
import pandas as pd
import joblib
import shap
from app.database import (
    save_prediction,
    get_predictions, 
    get_prediction_stats,
    create_prediction_table,
    create_fraud_cases_table,
    get_prediction_by_id,
    get_fraud_cases,
    get_fraud_case_by_id,
    create_fraud_case,
    update_fraud_case

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
create_fraud_cases_table()
# ==========================================
# CORS Configuration
# ==========================================


# CORS Configuration
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://sentinel-ai-ten-zeta.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================

# ==========================================

# ==========================================
# Load Saved Model
# ==========================================

BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_PATH = Path(
    os.getenv(
        "MODEL_PATH",
        str(BASE_DIR / "models" / "fraud_random_forest.pkl")
    )
)

THRESHOLD_PATH = Path(
    os.getenv(
        "THRESHOLD_PATH",
        str(BASE_DIR / "models" / "threshold.txt")
    )
)

HF_TOKEN = os.getenv("HF_TOKEN")
HF_REPO_ID = os.getenv(
    "HF_REPO_ID",
    "priyanka2912/sentinelai-fraud-model"
)


def download_hf_file(filename: str, destination: Path):
    """Download a file from the private Hugging Face repository."""

    if not HF_TOKEN:
        raise RuntimeError(
            f"{filename} is missing and HF_TOKEN is not configured."
        )

    destination.parent.mkdir(parents=True, exist_ok=True)

    url = (
        f"https://huggingface.co/{HF_REPO_ID}"
        f"/resolve/main/{filename}"
    )

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}"
    }

    print(f"Downloading {filename} from Hugging Face...")

    response = requests.get(
        url,
        headers=headers,
        stream=True,
        timeout=(15, 180)
    )

    response.raise_for_status()

    with open(destination, "wb") as file:
        for chunk in response.iter_content(chunk_size=1024 * 1024):
            if chunk:
                file.write(chunk)

    print(f"{filename} downloaded successfully!")


# Download model only if it is missing
if not MODEL_PATH.exists():
    download_hf_file("fraud_random_forest.pkl", MODEL_PATH)

# Download threshold only if it is missing
if not THRESHOLD_PATH.exists():
    download_hf_file("threshold.txt", THRESHOLD_PATH)

# Load saved model and threshold
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

# Fraud Case Request Model
# ==========================================

class FraudCaseCreate(BaseModel):
    prediction_id: int = Field(..., gt=0)
    analyst: str | None = Field(default=None, max_length=100)
    investigation_notes: str | None = Field(default=None, max_length=2000)


class FraudCaseUpdate(BaseModel):
    status: str | None = None
    analyst: str | None = Field(default=None, max_length=100)
    investigation_notes: str | None = Field(default=None, max_length=2000)

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

# ==========================================
# Fraud Case Management Endpoints
# ==========================================

@app.get("/cases")
def list_fraud_cases(
    limit: int = Query(20, ge=1, le=100)
):
    rows = get_fraud_cases(limit)

    cases = []

    for row in rows:
        cases.append({
            "case_id": row[0],
            "prediction_id": row[1],
            "status": row[2],
            "analyst": row[3],
            "investigation_notes": row[4],
            "created_at": row[5],
            "updated_at": row[6]
        })

    return {
        "count": len(cases),
        "cases": cases
    }


@app.get("/cases/{case_id}")
def fraud_case_details(case_id: int):
    row = get_fraud_case_by_id(case_id)

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Fraud case not found"
        )

    return {
        "case_id": row[0],
        "prediction_id": row[1],
        "status": row[2],
        "analyst": row[3],
        "investigation_notes": row[4],
        "created_at": row[5],
        "updated_at": row[6]
    }


@app.post("/cases", status_code=201)
def create_fraud_case_endpoint(case: FraudCaseCreate):
    prediction = get_prediction_by_id(case.prediction_id)

    if prediction is None:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    case_id = create_fraud_case(
        prediction_id=case.prediction_id,
        analyst=case.analyst,
        investigation_notes=case.investigation_notes
    )

    row = get_fraud_case_by_id(case_id)

    return {
        "case_id": row[0],
        "prediction_id": row[1],
        "status": row[2],
        "analyst": row[3],
        "investigation_notes": row[4],
        "created_at": row[5],
        "updated_at": row[6]
    }


@app.put("/cases/{case_id}")
def update_fraud_case_endpoint(
    case_id: int,
    case: FraudCaseUpdate
):
    existing_case = get_fraud_case_by_id(case_id)

    if existing_case is None:
        raise HTTPException(
            status_code=404,
            detail="Fraud case not found"
        )
    fields = case.model_fields_set

    allowed_statuses = {"NEW", "IN_PROGRESS", "RESOLVED"}

    # Reject an explicitly null status.
    if "status" in fields and case.status is None:
        raise HTTPException(
            status_code=400,
            detail="Status cannot be null."
        )

    # Validate and normalize status when supplied.
    if case.status is not None:
        normalized_status = case.status.strip().upper()

        if normalized_status not in allowed_statuses:
            raise HTTPException(
                status_code=400,
                detail="Invalid status. Use NEW, IN_PROGRESS, or RESOLVED."
            )

        case.status = normalized_status

    # Update only the fields included in the request.
    updated = update_fraud_case(
        case_id=case_id,
        status=case.status,
        analyst=case.analyst,
        investigation_notes=case.investigation_notes,
        fields_to_update=fields
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Fraud case not found"
        )

    row = get_fraud_case_by_id(case_id)

    return {
        "case_id": row[0],
        "prediction_id": row[1],
        "status": row[2],
        "analyst": row[3],
        "investigation_notes": row[4],
        "created_at": row[5],
        "updated_at": row[6]
    }




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

    prediction_id = save_prediction(
        amount=transaction.Amount,
        fraud_probability=float(fraud_probability),
        threshold=THRESHOLD,
        prediction=prediction,
        risk_level=risk_level,
        recommended_action=recommended_action,
        shap_factors=top_factors
    )

    # ==========================================
    # Automatically Create Fraud Case
    # ==========================================

    case_id = None

    if prediction == "FRAUD":
        case_id = create_fraud_case(
            prediction_id=prediction_id,
            status="NEW",
            analyst=None,
            investigation_notes=(
                "Automatically created after a fraud prediction. "
                "Review the transaction and investigate."
            )
        )

    # ==========================================
    # Final API Response
    # ==========================================

    return {
        "prediction_id": prediction_id,
        "case_id": case_id,
        "amount": transaction.Amount,
        "fraud_probability": round(float(fraud_probability), 4),
        "threshold": THRESHOLD,
        "prediction": prediction,
        "risk_level": risk_level,
        "top_risk_factors": top_factors,
        "recommended_action": recommended_action
    }



@app.post("/investigate")
def investigate(payload: dict):
    """Run the LangGraph investigation workflow."""

    required_fields = {
        "prediction",
        "risk_level",
        "fraud_probability",
        "top_risk_factors",
    }

    missing_fields = required_fields - payload.keys()

    if missing_fields:
        raise HTTPException(
            status_code=422,
            detail={
                "message": "Missing required prediction fields",
                "missing_fields": sorted(missing_fields),
            },
        )

    return run_investigation(payload)
