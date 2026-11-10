import json
import os
from pathlib import Path

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    Text,
    create_engine,
    func,
    insert,
    select,
    update,
)

from app.config import engine as default_engine


# ==========================================
# Database Configuration
# ==========================================

DATABASE_NAME = os.getenv(
    "DATABASE_PATH",
    str(Path(__file__).resolve().parents[2] / "sentinelai.db")
)

# Keep the original engine available for compatibility.
engine = default_engine

# Isolated SQLite engines used by automated tests.
_initial_database_name = DATABASE_NAME
_test_engines = {}


def get_active_engine():
    """
    Return the production engine by default.
    Use a separate SQLite engine when tests override DATABASE_NAME.
    """

    if DATABASE_NAME != _initial_database_name:
        if DATABASE_NAME not in _test_engines:
            _test_engines[DATABASE_NAME] = create_engine(
                f"sqlite:///{DATABASE_NAME}",
                connect_args={"check_same_thread": False},
                echo=False,
            )

        return _test_engines[DATABASE_NAME]

    return default_engine


# ==========================================
# SQLAlchemy Metadata
# ==========================================

metadata = MetaData()


# ==========================================
# Predictions Table
# ==========================================

predictions = Table(
    "predictions",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("amount", Float, nullable=False),
    Column("fraud_probability", Float, nullable=False),
    Column("threshold", Float, nullable=False),
    Column("prediction", String, nullable=False),
    Column("risk_level", String, nullable=False),
    Column("recommended_action", Text, nullable=False),
    Column("shap_factors", Text),
    Column("created_at", DateTime, server_default=func.now()),
    Column("source_database", String(20)),
    Column("source_record_id", Integer),
)


# ==========================================
# Fraud Cases Table
# ==========================================

fraud_cases = Table(
    "fraud_cases",
    metadata,
    Column("case_id", Integer, primary_key=True, autoincrement=True),
    Column(
        "prediction_id",
        Integer,
        ForeignKey("predictions.id"),
        nullable=False,
    ),
    Column("status", String, nullable=False, server_default="NEW"),
    Column("analyst", String),
    Column("investigation_notes", Text),
    Column("created_at", DateTime, server_default=func.now()),
    Column("updated_at", DateTime, server_default=func.now()),
    Column("source_database", String(20)),
    Column("source_record_id", Integer),
)


# ==========================================
# Authentication Tables
# ==========================================

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("email", String(255), nullable=False, unique=True),
    Column("full_name", String(150), nullable=False),
    Column("password_hash", String(255), nullable=False),
    Column("role", String(30), nullable=False),
    Column("is_active", Boolean, nullable=False, default=True),
    Column("created_at", DateTime, server_default=func.now()),
    Column("updated_at", DateTime, server_default=func.now()),
)

audit_logs = Table(
    "audit_logs",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", Integer, ForeignKey("users.id"), nullable=True),
    Column("action", String(100), nullable=False),
    Column("resource_type", String(100)),
    Column("resource_id", String(100)),
    Column("ip_address", String(45)),
    Column("created_at", DateTime, server_default=func.now()),
)


# ==========================================
# Email OTP Verification and Password Reset
# ==========================================

otp_verifications = Table(
    "otp_verifications",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("email", String(255), nullable=False),
    Column("full_name", String(150), nullable=True),
    Column("password_hash", String(255), nullable=True),
    Column("purpose", String(30), nullable=False),
    Column("otp_hash", String(255), nullable=False),
    Column("expires_at", DateTime(timezone=True), nullable=False),
    Column("attempts", Integer, nullable=False, default=0),
    Column("is_used", Boolean, nullable=False, default=False),
    Column("created_at", DateTime, server_default=func.now()),
)


# ==========================================
# Database Initialization
# ==========================================

def get_connection():
    return get_active_engine().connect()


def create_prediction_table():
    metadata.create_all(
        get_active_engine(),
        tables=[predictions],
    )


def create_fraud_cases_table():
    metadata.create_all(
        get_active_engine(),
        tables=[predictions, fraud_cases],
    )



def create_auth_tables():
    """Create authentication tables when explicitly requested."""
    metadata.create_all(
        get_active_engine(),
        tables=[users, audit_logs, otp_verifications],
    )


def log_audit_event(
    user_id,
    action,
    resource_type=None,
    resource_id=None,
    ip_address=None,
):
    """Record a security-relevant action in the audit log."""

    with get_active_engine().begin() as connection:
        connection.execute(
            insert(audit_logs).values(
                user_id=user_id,
                action=action,
                resource_type=resource_type,
                resource_id=(
                    str(resource_id)
                    if resource_id is not None
                    else None
                ),
                ip_address=ip_address,
            )
        )


# ==========================================
# Save Prediction
# ==========================================

def save_prediction(
    amount,
    fraud_probability,
    threshold,
    prediction,
    risk_level,
    recommended_action,
    shap_factors,
):
    values = {
        "amount": amount,
        "fraud_probability": fraud_probability,
        "threshold": threshold,
        "prediction": prediction,
        "risk_level": risk_level,
        "recommended_action": recommended_action,
        "shap_factors": json.dumps(shap_factors),
    }

    with get_active_engine().begin() as connection:
        result = connection.execute(
            insert(predictions).values(**values)
        )

        prediction_id = result.inserted_primary_key[0]

    return prediction_id


# ==========================================
# Create Fraud Case
# ==========================================

def create_fraud_case(
    prediction_id,
    status="NEW",
    analyst=None,
    investigation_notes=None,
):
    values = {
        "prediction_id": prediction_id,
        "status": status,
        "analyst": analyst,
        "investigation_notes": investigation_notes,
    }

    with get_active_engine().begin() as connection:
        result = connection.execute(
            insert(fraud_cases).values(**values)
        )

        case_id = result.inserted_primary_key[0]

    return case_id


# ==========================================
# Get Fraud Cases
# ==========================================

def get_fraud_cases(limit=20, analyst_email=None):
    statement = select(
        fraud_cases.c.case_id,
        fraud_cases.c.prediction_id,
        fraud_cases.c.status,
        fraud_cases.c.analyst,
        fraud_cases.c.investigation_notes,
        fraud_cases.c.created_at,
        fraud_cases.c.updated_at,
    )

    if analyst_email is not None:
        statement = statement.where(
            fraud_cases.c.analyst == analyst_email
        )

    statement = (
        statement
        .order_by(fraud_cases.c.case_id.desc())
        .limit(limit)
    )

    with get_active_engine().connect() as connection:
        rows = connection.execute(statement).fetchall()

    return rows


# ==========================================
# Get Fraud Case By ID
# ==========================================

def get_fraud_case_by_id(case_id):
    statement = select(
        fraud_cases.c.case_id,
        fraud_cases.c.prediction_id,
        fraud_cases.c.status,
        fraud_cases.c.analyst,
        fraud_cases.c.investigation_notes,
        fraud_cases.c.created_at,
        fraud_cases.c.updated_at,
    ).where(fraud_cases.c.case_id == case_id)

    with get_active_engine().connect() as connection:
        row = connection.execute(statement).fetchone()

    return row


# ==========================================
# Update Fraud Case
# ==========================================

def update_fraud_case(
    case_id,
    status=None,
    analyst=None,
    investigation_notes=None,
    fields_to_update=None,
):
    if fields_to_update is None:
        fields_to_update = set()

        if status is not None:
            fields_to_update.add("status")

        if analyst is not None:
            fields_to_update.add("analyst")

        if investigation_notes is not None:
            fields_to_update.add("investigation_notes")

    allowed_fields = {
        "status",
        "analyst",
        "investigation_notes",
    }

    fields_to_update = set(fields_to_update) & allowed_fields

    values_by_field = {
        "status": status,
        "analyst": analyst,
        "investigation_notes": investigation_notes,
    }

    with get_active_engine().begin() as connection:

        if not fields_to_update:
            exists = connection.execute(
                select(fraud_cases.c.case_id).where(
                    fraud_cases.c.case_id == case_id
                )
            ).first()

            return exists is not None

        update_values = {
            field: values_by_field[field]
            for field in fields_to_update
        }

        update_values["updated_at"] = func.now()

        result = connection.execute(
            update(fraud_cases)
            .where(fraud_cases.c.case_id == case_id)
            .values(**update_values)
        )

        return result.rowcount > 0


# ==========================================
# Get Predictions
# ==========================================

def get_predictions(limit=20):
    statement = (
        select(
            predictions.c.id,
            predictions.c.amount,
            predictions.c.fraud_probability,
            predictions.c.threshold,
            predictions.c.prediction,
            predictions.c.risk_level,
            predictions.c.recommended_action,
            predictions.c.shap_factors,
            predictions.c.created_at,
        )
        .order_by(predictions.c.id.desc())
        .limit(limit)
    )

    with get_active_engine().connect() as connection:
        rows = connection.execute(statement).fetchall()

    return rows


# ==========================================
# Get Prediction By ID
# ==========================================

def get_prediction_by_id(prediction_id):
    statement = select(
        predictions.c.id,
        predictions.c.amount,
        predictions.c.fraud_probability,
        predictions.c.threshold,
        predictions.c.prediction,
        predictions.c.risk_level,
        predictions.c.recommended_action,
        predictions.c.shap_factors,
        predictions.c.created_at,
    ).where(predictions.c.id == prediction_id)

    with get_active_engine().connect() as connection:
        row = connection.execute(statement).fetchone()

    return row


# ==========================================
# Get Prediction Statistics
# ==========================================

def get_prediction_stats():
    with get_active_engine().connect() as connection:

        total_transactions = connection.execute(
            select(func.count()).select_from(predictions)
        ).scalar_one()

        fraud_transactions = connection.execute(
            select(func.count())
            .select_from(predictions)
            .where(predictions.c.prediction == "FRAUD")
        ).scalar_one()

        legitimate_transactions = (
            total_transactions - fraud_transactions
        )

        fraud_rate = (
            round(
                (fraud_transactions / total_transactions) * 100,
                2,
            )
            if total_transactions > 0
            else 0
        )

        risk_rows = connection.execute(
            select(
                predictions.c.risk_level,
                func.count().label("count"),
            )
            .group_by(predictions.c.risk_level)
        ).fetchall()

    risk_distribution = {
        "LOW": 0,
        "MEDIUM": 0,
        "HIGH": 0,
        "CRITICAL": 0,
    }

    for row in risk_rows:
        risk_level = row[0].upper()

        if risk_level in risk_distribution:
            risk_distribution[risk_level] = row[1]

    return {
        "total_transactions": total_transactions,
        "fraud_transactions": fraud_transactions,
        "legitimate_transactions": legitimate_transactions,
        "fraud_rate": round(fraud_rate, 2),
        "risk_distribution": risk_distribution,
    }
