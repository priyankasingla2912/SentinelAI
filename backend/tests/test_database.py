
import json
import sqlite3

import pytest

from backend.app import database


@pytest.fixture
def test_db(tmp_path, monkeypatch):
    db_path = tmp_path / "test_sentinelai.db"

    monkeypatch.setattr(
        database, "DATABASE_NAME", str(db_path)
    )

    database.create_prediction_table()
    database.create_fraud_cases_table()

    return db_path


def test_save_prediction_persists_record(test_db):
    prediction_id = database.save_prediction(
        amount=125.50,
        fraud_probability=0.85,
        threshold=0.60,
        prediction="FRAUD",
        risk_level="HIGH",
        recommended_action="Hold transaction.",
        shap_factors=[
            {"feature": "V14", "shap_value": 0.25}
        ],
    )

    with sqlite3.connect(test_db) as connection:
        row = connection.execute(
            """
            SELECT amount, fraud_probability, prediction,
                   shap_factors
            FROM predictions WHERE id = ?
            """,
            (prediction_id,),
        ).fetchone()

    assert prediction_id > 0
    assert row is not None
    assert row[0] == pytest.approx(125.50)
    assert row[1] == pytest.approx(0.85)
    assert row[2] == "FRAUD"
    assert json.loads(row[3])[0]["feature"] == "V14"


def test_create_fraud_case_persists_record(test_db):
    prediction_id = database.save_prediction(
        amount=200.00,
        fraud_probability=0.95,
        threshold=0.60,
        prediction="FRAUD",
        risk_level="CRITICAL",
        recommended_action="Escalate for review.",
        shap_factors=[],
    )

    case_id = database.create_fraud_case(
        prediction_id=prediction_id,
        status="NEW",
        analyst=None,
        investigation_notes="Automated test case.",
    )

    with sqlite3.connect(test_db) as connection:
        row = connection.execute(
            """
            SELECT prediction_id, status, analyst,
                   investigation_notes
            FROM fraud_cases WHERE case_id = ?
            """,
            (case_id,),
        ).fetchone()

    assert case_id > 0
    assert row is not None
    assert row[0] == prediction_id
    assert row[1] == "NEW"
    assert row[2] is None
    assert row[3] == "Automated test case."


def test_create_fraud_case_uses_default_status(test_db):
    prediction_id = database.save_prediction(
        amount=50.00,
        fraud_probability=0.70,
        threshold=0.60,
        prediction="FRAUD",
        risk_level="HIGH",
        recommended_action="Review transaction.",
        shap_factors=[],
    )

    case_id = database.create_fraud_case(
        prediction_id=prediction_id
    )

    with sqlite3.connect(test_db) as connection:
        row = connection.execute(
            "SELECT status FROM fraud_cases WHERE case_id = ?",
            (case_id,),
        ).fetchone()

    assert row is not None
    assert row[0] == "NEW"
