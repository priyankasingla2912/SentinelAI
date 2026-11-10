import json
import requests
import os
from datetime import datetime, timedelta, timezone
from fastapi import FastAPI, HTTPException, Query, Depends, Request
from sqlalchemy import select, insert, update, func
from sqlalchemy.exc import IntegrityError
from app.auth import get_current_user, require_permission
from app.roles import Permission, Role, has_permission
from app.security import verify_password, create_access_token, hash_password
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
    update_fraud_case,
    get_active_engine,
    users,
    audit_logs,
    otp_verifications,
    log_audit_event,
)

from app.otp_service import (
    generate_otp,
    hash_otp,
    verify_otp_hash,
    send_otp_email,
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
# Authentication Request Models
# ==========================================

class LoginRequest(BaseModel):
    email: str = Field(..., min_length=5, max_length=255)
    password: str = Field(..., min_length=1, max_length=128)


class RegisterRequest(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=150)
    email: str = Field(
        ...,
        min_length=5,
        max_length=255,
        pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
    )
    password: str = Field(..., min_length=12, max_length=128)


class OTPVerifyRequest(BaseModel):
    email: str = Field(..., min_length=5, max_length=255)
    otp: str = Field(..., pattern=r"^\d{6}$")


class ForgotPasswordRequest(BaseModel):
    email: str = Field(..., min_length=5, max_length=255)


class ResetPasswordRequest(BaseModel):
    email: str = Field(..., min_length=5, max_length=255)
    otp: str = Field(..., pattern=r"^\d{6}$")
    new_password: str = Field(..., min_length=12, max_length=128)


class UserCreate(BaseModel):
    email: str = Field(..., min_length=5, max_length=255)
    full_name: str = Field(..., min_length=2, max_length=150)
    password: str = Field(..., min_length=12, max_length=128)
    role: Role


class UserUpdate(BaseModel):
    role: Role | None = None
    is_active: bool | None = None

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
# Authentication - Login
# ==========================================

@app.post("/auth/login")
def login(
    credentials: LoginRequest,
    request: Request,
):
    """Authenticate a user and return a JWT access token."""

    invalid_credentials = HTTPException(
        status_code=401,
        detail="Invalid email or password.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    email = credentials.email.strip().lower()

    with get_active_engine().connect() as connection:
        user = connection.execute(
            select(users).where(users.c.email == email)
        ).mappings().first()

    if not user or not user["is_active"]:
        raise invalid_credentials

    if not verify_password(
        credentials.password,
        user["password_hash"],
    ):
        raise invalid_credentials

    access_token = create_access_token(
        user_id=user["id"],
        role=user["role"],
    )

    log_audit_event(
        user_id=user["id"],
        action="LOGIN_SUCCESS",
        resource_type="authentication",
        ip_address=(
            request.client.host
            if request.client
            else None
        ),
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user["id"],
            "email": user["email"],
            "full_name": user["full_name"],
            "role": user["role"],
        },
    }


@app.post("/auth/register")
def register_user(data: RegisterRequest, request: Request):
    """Start public registration by sending an email verification OTP."""
    email = data.email.strip().lower()
    full_name = data.full_name.strip()

    if not full_name:
        raise HTTPException(status_code=400, detail="Full name is required.")

    engine = get_active_engine()
    now = datetime.now(timezone.utc)

    with engine.begin() as connection:
        existing_user = connection.execute(
            select(users.c.id).where(users.c.email == email)
        ).first()

        if existing_user:
            raise HTTPException(
                status_code=409,
                detail="An account with this email already exists.",
            )

        recent_otp = connection.execute(
            select(otp_verifications.c.created_at)
            .where(
                otp_verifications.c.email == email,
                otp_verifications.c.purpose == "REGISTER",
                otp_verifications.c.is_used.is_(False),
            )
            .order_by(otp_verifications.c.created_at.desc())
        ).first()

        if recent_otp and recent_otp.created_at:
            created_at = recent_otp.created_at
            if created_at.tzinfo is None:
                created_at = created_at.replace(tzinfo=timezone.utc)
            if now - created_at < timedelta(seconds=60):
                raise HTTPException(
                    status_code=429,
                    detail="Please wait one minute before requesting another code.",
                )

        otp = generate_otp()
        connection.execute(
            insert(otp_verifications).values(
                email=email,
                full_name=full_name,
                password_hash=hash_password(data.password),
                purpose="REGISTER",
                otp_hash=hash_otp(otp),
                expires_at=now + timedelta(minutes=10),
                attempts=0,
                is_used=False,
            )
        )

    try:
        send_otp_email(email, otp, "REGISTER")
    except Exception:
        import logging
        logging.exception("OTP email delivery failed")
        with engine.begin() as connection:
            connection.execute(
                update(otp_verifications)
                .where(
                    otp_verifications.c.email == email,
                    otp_verifications.c.purpose == "REGISTER",
                    otp_verifications.c.is_used.is_(False),
                )
                .values(is_used=True)
            )
        raise HTTPException(
            status_code=503,
            detail="Unable to send verification email. Please try again later.",
        )

    return {
        "message": "Verification code sent. It expires in 10 minutes."
    }


@app.post("/auth/verify-otp")
def verify_registration_otp(data: OTPVerifyRequest, request: Request):
    """Verify registration OTP and activate a new VIEWER account."""
    email = data.email.strip().lower()
    now = datetime.now(timezone.utc)
    engine = get_active_engine()
    error = None
    new_user_id = None

    with engine.begin() as connection:
        otp_record = connection.execute(
            select(otp_verifications)
            .where(
                otp_verifications.c.email == email,
                otp_verifications.c.purpose == "REGISTER",
                otp_verifications.c.is_used.is_(False),
            )
            .order_by(otp_verifications.c.id.desc())
        ).mappings().first()

        if not otp_record:
            error = (400, "No pending verification was found. Please register again.")
        elif otp_record["attempts"] >= 5:
            error = (429, "Too many incorrect attempts. Please register again.")
        else:
            expires_at = otp_record["expires_at"]
            if expires_at.tzinfo is None:
                expires_at = expires_at.replace(tzinfo=timezone.utc)

            if now >= expires_at:
                connection.execute(
                    update(otp_verifications)
                    .where(otp_verifications.c.id == otp_record["id"])
                    .values(is_used=True)
                )
                error = (400, "Verification code expired. Please register again.")
            elif not verify_otp_hash(data.otp, otp_record["otp_hash"]):
                connection.execute(
                    update(otp_verifications)
                    .where(otp_verifications.c.id == otp_record["id"])
                    .values(attempts=otp_verifications.c.attempts + 1)
                )
                error = (400, "Incorrect verification code.")
            else:
                existing_user = connection.execute(
                    select(users.c.id).where(users.c.email == email)
                ).first()

                if existing_user:
                    connection.execute(
                        update(otp_verifications)
                        .where(otp_verifications.c.id == otp_record["id"])
                        .values(is_used=True)
                    )
                    error = (409, "An account with this email already exists.")
                else:
                    connection.execute(
                        insert(users).values(
                            email=email,
                            full_name=otp_record["full_name"],
                            password_hash=otp_record["password_hash"],
                            role=Role.VIEWER.value,
                            is_active=True,
                        )
                    )
                    connection.execute(
                        update(otp_verifications)
                        .where(otp_verifications.c.id == otp_record["id"])
                        .values(is_used=True)
                    )
                    new_user = connection.execute(
                        select(users.c.id).where(users.c.email == email)
                    ).first()
                    new_user_id = new_user[0] if new_user else None

    if error:
        raise HTTPException(status_code=error[0], detail=error[1])

    if new_user_id is not None:
        log_audit_event(
            user_id=new_user_id,
            action="USER_REGISTERED",
            resource_type="user",
            resource_id=new_user_id,
            ip_address=request.client.host if request.client else None,
        )

    return {
        "message": "Email verified. Your SentinelAI account is now active. Please log in.",
        "email": email,
        "role": Role.VIEWER.value,
    }


@app.post("/auth/forgot-password")
def forgot_password(data: ForgotPasswordRequest):
    """Send a password-reset OTP without revealing whether an account exists."""
    email = data.email.strip().lower()
    engine = get_active_engine()
    now = datetime.now(timezone.utc)
    otp_to_send = None

    with engine.begin() as connection:
        user = connection.execute(
            select(users.c.id).where(
                users.c.email == email,
                users.c.is_active.is_(True),
            )
        ).first()

        if user:
            recent_otp = connection.execute(
                select(otp_verifications.c.created_at)
                .where(
                    otp_verifications.c.email == email,
                    otp_verifications.c.purpose == "RESET",
                    otp_verifications.c.is_used.is_(False),
                )
                .order_by(otp_verifications.c.created_at.desc())
            ).first()

            can_send = True
            if recent_otp and recent_otp.created_at:
                created_at = recent_otp.created_at
                if created_at.tzinfo is None:
                    created_at = created_at.replace(tzinfo=timezone.utc)
                can_send = now - created_at >= timedelta(seconds=60)

            if can_send:
                otp_to_send = generate_otp()
                connection.execute(
                    insert(otp_verifications).values(
                        email=email,
                        full_name=None,
                        password_hash=None,
                        purpose="RESET",
                        otp_hash=hash_otp(otp_to_send),
                        expires_at=now + timedelta(minutes=10),
                        attempts=0,
                        is_used=False,
                    )
                )

    if otp_to_send:
        try:
            send_otp_email(email, otp_to_send, "RESET")
        except Exception:
            import logging
            logging.exception("OTP email delivery failed")

            with engine.begin() as connection:
                connection.execute(
                    update(otp_verifications)
                    .where(
                        otp_verifications.c.email == email,
                        otp_verifications.c.purpose == "RESET",
                        otp_verifications.c.is_used.is_(False),
                    )
                    .values(is_used=True)
                )
            raise HTTPException(
                status_code=503,
                detail="Unable to send the reset email. Please try again later.",
            )

    return {
        "message": "If an active account exists for this email, a password-reset code will be sent."
    }


@app.post("/auth/reset-password")
def reset_password(data: ResetPasswordRequest, request: Request):
    """Verify a reset OTP and update the account password."""
    email = data.email.strip().lower()
    now = datetime.now(timezone.utc)
    engine = get_active_engine()
    error = None
    reset_user_id = None

    with engine.begin() as connection:
        user = connection.execute(
            select(users).where(
                users.c.email == email,
                users.c.is_active.is_(True),
            )
        ).mappings().first()

        otp_record = connection.execute(
            select(otp_verifications)
            .where(
                otp_verifications.c.email == email,
                otp_verifications.c.purpose == "RESET",
                otp_verifications.c.is_used.is_(False),
            )
            .order_by(otp_verifications.c.id.desc())
        ).mappings().first()

        if not user or not otp_record:
            error = (400, "Invalid or expired password-reset code.")
        elif otp_record["attempts"] >= 5:
            error = (429, "Too many incorrect attempts. Request a new code.")
        else:
            expires_at = otp_record["expires_at"]
            if expires_at.tzinfo is None:
                expires_at = expires_at.replace(tzinfo=timezone.utc)

            if now >= expires_at:
                connection.execute(
                    update(otp_verifications)
                    .where(otp_verifications.c.id == otp_record["id"])
                    .values(is_used=True)
                )
                error = (400, "Password-reset code expired. Request a new code.")
            elif not verify_otp_hash(data.otp, otp_record["otp_hash"]):
                connection.execute(
                    update(otp_verifications)
                    .where(otp_verifications.c.id == otp_record["id"])
                    .values(attempts=otp_verifications.c.attempts + 1)
                )
                error = (400, "Invalid or expired password-reset code.")
            else:
                connection.execute(
                    update(users)
                    .where(users.c.id == user["id"])
                    .values(
                        password_hash=hash_password(data.new_password),
                        updated_at=now,
                    )
                )
                connection.execute(
                    update(otp_verifications)
                    .where(otp_verifications.c.id == otp_record["id"])
                    .values(is_used=True)
                )
                reset_user_id = user["id"]

    if error:
        raise HTTPException(status_code=error[0], detail=error[1])

    if reset_user_id is not None:
        log_audit_event(
            user_id=reset_user_id,
            action="PASSWORD_RESET",
            resource_type="authentication",
            ip_address=request.client.host if request.client else None,
        )

    return {
        "message": "Password reset successfully. Please log in with your new password."
    }


@app.get("/auth/me")
def get_me(current_user: dict = Depends(get_current_user)):
    """Return the authenticated user's public profile."""
    return {
        "id": current_user["id"],
        "email": current_user["email"],
        "full_name": current_user["full_name"],
        "role": current_user["role"],
    }


# ==========================================
# Authentication - Admin User Management
# ==========================================

@app.post("/auth/users", status_code=201)
def create_user(
    payload: UserCreate,
    request: Request,
    current_user: dict = Depends(
        require_permission(Permission.MANAGE_USERS)
    ),
):
    """Allow Admins to create registered user accounts."""

    email = payload.email.strip().lower()
    full_name = payload.full_name.strip()

    if not full_name:
        raise HTTPException(
            status_code=422,
            detail="Full name cannot be empty.",
        )

    try:
        with get_active_engine().begin() as connection:
            existing_user = connection.execute(
                select(users.c.id).where(users.c.email == email)
            ).first()

            if existing_user:
                raise HTTPException(
                    status_code=409,
                    detail="An account with this email already exists.",
                )

            result = connection.execute(
                insert(users).values(
                    email=email,
                    full_name=full_name,
                    password_hash=hash_password(payload.password),
                    role=payload.role.value,
                    is_active=True,
                )
            )

            user_id = result.inserted_primary_key[0]

    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="An account with this email already exists.",
        )

    log_audit_event(
        user_id=current_user["id"],
        action="USER_CREATED",
        resource_type="user",
        resource_id=user_id,
        ip_address=request.client.host if request.client else None,
    )

    return {
        "message": "User created successfully.",
        "user": {
            "id": user_id,
            "email": email,
            "full_name": full_name,
            "role": payload.role.value,
            "is_active": True,
        },
    }


# ==========================================
# Authentication - List Users
# ==========================================

@app.get("/auth/users")
def list_users(
    current_user: dict = Depends(
        require_permission(Permission.MANAGE_USERS)
    ),
):
    """Allow Admins to view registered user accounts."""

    with get_active_engine().connect() as connection:
        rows = connection.execute(
            select(
                users.c.id,
                users.c.email,
                users.c.full_name,
                users.c.role,
                users.c.is_active,
                users.c.created_at,
            ).order_by(users.c.id.asc())
        ).mappings().all()

    return {
        "users": [dict(row) for row in rows]
    }


# ==========================================
# Authentication - Update User
# ==========================================

@app.put("/auth/users/{user_id}")
def update_user(
    user_id: int,
    payload: UserUpdate,
    request: Request,
    current_user: dict = Depends(
        require_permission(Permission.MANAGE_USERS)
    ),
):
    """Allow Admins to change user roles and account status."""

    if payload.role is None and payload.is_active is None:
        raise HTTPException(
            status_code=422,
            detail="Provide a role or account status to update.",
        )

    with get_active_engine().begin() as connection:
        target_user = connection.execute(
            select(users).where(users.c.id == user_id)
        ).mappings().first()

        if not target_user:
            raise HTTPException(
                status_code=404,
                detail="User account not found.",
            )

        is_self = current_user["id"] == user_id

        if is_self and (
            (payload.role is not None and payload.role != Role.ADMIN)
            or payload.is_active is False
        ):
            raise HTTPException(
                status_code=400,
                detail="You cannot demote or deactivate your own Admin account.",
            )

        removing_admin_access = (
            target_user["role"] == Role.ADMIN
            and target_user["is_active"]
            and (
                (payload.role is not None and payload.role != Role.ADMIN)
                or payload.is_active is False
            )
        )

        if removing_admin_access:
            active_admin_count = connection.execute(
                select(users.c.id).where(
                    users.c.role == Role.ADMIN,
                    users.c.is_active.is_(True),
                )
            ).fetchall()

            if len(active_admin_count) <= 1:
                raise HTTPException(
                    status_code=409,
                    detail="The last active Admin account cannot be demoted or deactivated.",
                )

        changes = {}

        if payload.role is not None:
            changes["role"] = payload.role.value

        if payload.is_active is not None:
            changes["is_active"] = payload.is_active

        connection.execute(
            update(users)
            .where(users.c.id == user_id)
            .values(**changes, updated_at=func.now())
        )

        updated_user = connection.execute(
            select(
                users.c.id,
                users.c.email,
                users.c.full_name,
                users.c.role,
                users.c.is_active,
                users.c.created_at,
            ).where(users.c.id == user_id)
        ).mappings().one()

    log_audit_event(
        user_id=current_user["id"],
        action="USER_UPDATED",
        resource_type="user",
        resource_id=user_id,
        ip_address=request.client.host if request.client else None,
    )

    return {
        "message": "User account updated successfully.",
        "user": dict(updated_user),
    }


# ==========================================
# Authentication - Audit Logs
# ==========================================

@app.get("/auth/audit-logs")
def list_audit_logs(
    limit: int = Query(100, ge=1, le=500),
    current_user: dict = Depends(
        require_permission(Permission.VIEW_AUDIT_LOGS)
    ),
):
    """Allow Admins and Senior Fraud Analysts to view audit logs."""

    with get_active_engine().connect() as connection:
        rows = connection.execute(
            select(
                audit_logs.c.id,
                audit_logs.c.user_id,
                audit_logs.c.action,
                audit_logs.c.resource_type,
                audit_logs.c.resource_id,
                audit_logs.c.ip_address,
                audit_logs.c.created_at,
            )
            .order_by(audit_logs.c.created_at.desc())
            .limit(limit)
        ).mappings().all()

    return {
        "audit_logs": [dict(row) for row in rows]
    }


# ==========================================
# Prediction History Endpoint
# ==========================================

@app.get("/history")
def history(
    limit: int = Query(20, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
):
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
def prediction_details(
    prediction_id: int,
    current_user: dict = Depends(get_current_user),
):
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
def stats(current_user: dict = Depends(require_permission(Permission.VIEW_DASHBOARDS))
):

    return get_prediction_stats()


# ==========================================

# ==========================================
# Fraud Case Management Endpoints
# ==========================================

@app.get("/cases")
def list_fraud_cases(
    limit: int = Query(20, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
):
    analyst_email = (
        current_user["email"]
        if current_user["role"] == Role.FRAUD_ANALYST
        else None
    )

    rows = get_fraud_cases(
        limit,
        analyst_email=analyst_email,
    )

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
def fraud_case_details(
    case_id: int,
    current_user: dict = Depends(get_current_user),
):
    row = get_fraud_case_by_id(case_id)

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Fraud case not found"
        )

    if (
        current_user["role"] == Role.FRAUD_ANALYST
        and (
            not row[3]
            or row[3].strip().lower()
            != current_user["email"].strip().lower()
        )
    ):
        raise HTTPException(
            status_code=403,
            detail="You can only access fraud cases assigned to you."
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
def create_fraud_case_endpoint(
    case: FraudCaseCreate,
    current_user: dict = Depends(require_permission(Permission.CREATE_CASES)),
):
    user_role = Role(current_user["role"])
    if user_role == Role.VIEWER:
        raise HTTPException(
            status_code=403,
            detail="Viewers cannot create fraud cases."
        )

    prediction = get_prediction_by_id(case.prediction_id)

    if prediction is None:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    if user_role == Role.FRAUD_ANALYST:
        assigned_analyst = current_user["email"]

    elif user_role in {
        Role.ADMIN,
        Role.SENIOR_FRAUD_ANALYST,
    }:
        assigned_analyst = case.analyst

        if assigned_analyst:
            with get_active_engine().connect() as connection:
                assigned_user = connection.execute(
                    select(users.c.email).where(
                        users.c.email == assigned_analyst,
                        users.c.is_active.is_(True),
                    )
                ).first()

            if assigned_user is None:
                raise HTTPException(
                    status_code=400,
                    detail="Assigned analyst must be an active registered user."
                )
    else:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to create fraud cases."
        )

    case_id = create_fraud_case(
        prediction_id=case.prediction_id,
        analyst=assigned_analyst,
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
    case: FraudCaseUpdate,
    current_user: dict = Depends(get_current_user),
):
    user_role = Role(current_user["role"])

    required_permission = (
        Permission.UPDATE_ASSIGNED_CASES
        if user_role == Role.FRAUD_ANALYST
        else Permission.UPDATE_ALL_CASES
    )

    if not has_permission(current_user["role"], required_permission):
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to update fraud cases."
        )

    if user_role == Role.VIEWER:
        raise HTTPException(
            status_code=403,
            detail="Viewers cannot update fraud cases."
        )

    existing_case = get_fraud_case_by_id(case_id)

    if existing_case is None:
        raise HTTPException(
            status_code=404,
            detail="Fraud case not found"
        )

    fields = case.model_fields_set
    if user_role == Role.FRAUD_ANALYST:
        assigned_email = existing_case[3]

        if (
            not assigned_email
            or assigned_email.strip().lower()
            != current_user["email"].strip().lower()
        ):
            raise HTTPException(
                status_code=403,
                detail="You can only update fraud cases assigned to you."
            )

        if "analyst" in fields:
            raise HTTPException(
                status_code=403,
                detail="Fraud Analysts cannot assign or reassign cases."
            )

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
def predict(
    transaction: Transaction,
    current_user: dict = Depends(require_permission(Permission.CREATE_PREDICTIONS)),
):
    if current_user["role"] == Role.VIEWER:
        raise HTTPException(
            status_code=403,
            detail="Viewers cannot create predictions."
        )

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
            analyst=(
                current_user["email"]
                if current_user["role"] == Role.FRAUD_ANALYST
                else None
            ),
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
def investigate(
    payload: dict,
    current_user: dict = Depends(require_permission(Permission.INVESTIGATE_FRAUD)),
):
    """Run the LangGraph investigation workflow."""

    if current_user["role"] == Role.VIEWER:
        raise HTTPException(
            status_code=403,
            detail="Viewers cannot run fraud investigations."
        )

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
