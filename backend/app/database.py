import sqlite3
import json

DATABASE_NAME = "sentinelai.db"


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def create_prediction_table():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            fraud_probability REAL NOT NULL,
            threshold REAL NOT NULL,
            prediction TEXT NOT NULL,
            risk_level TEXT NOT NULL,
            recommended_action TEXT NOT NULL,
            shap_factors TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Add shap_factors to an existing database if the column
    # does not already exist.
    cursor.execute("PRAGMA table_info(predictions)")
    columns = [column[1] for column in cursor.fetchall()]

    if "shap_factors" not in columns:
        cursor.execute("""
            ALTER TABLE predictions
            ADD COLUMN shap_factors TEXT
        """)

    connection.commit()
    connection.close()


def save_prediction(
    amount,
    fraud_probability,
    threshold,
    prediction,
    risk_level,
    recommended_action,
    shap_factors
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO predictions (
            amount,
            fraud_probability,
            threshold,
            prediction,
            risk_level,
            recommended_action,
            shap_factors
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        amount,
        fraud_probability,
        threshold,
        prediction,
        risk_level,
        recommended_action,
        json.dumps(shap_factors)
    ))

    connection.commit()
    connection.close()


def get_predictions(limit=20):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            amount,
            fraud_probability,
            threshold,
            prediction,
            risk_level,
            recommended_action,
            shap_factors,
            created_at
        FROM predictions
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()

    connection.close()

    return rows


def get_prediction_stats():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM predictions")
    total_transactions = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*) FROM predictions
        WHERE prediction = 'FRAUD'
    """)
    fraud_transactions = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*) FROM predictions
        WHERE prediction = 'LEGITIMATE'
    """)
    legitimate_transactions = cursor.fetchone()[0]

    cursor.execute("""
        SELECT risk_level, COUNT(*)
        FROM predictions
        GROUP BY risk_level
    """)
    risk_rows = cursor.fetchall()

    connection.close()

    risk_distribution = {
        "LOW": 0,
        "MEDIUM": 0,
        "HIGH": 0,
        "CRITICAL": 0
    }

    for risk_level, count in risk_rows:
        risk_distribution[risk_level] = count

    if total_transactions > 0:
        fraud_rate = (
            fraud_transactions / total_transactions
        ) * 100
    else:
        fraud_rate = 0

    return {
        "total_transactions": total_transactions,
        "fraud_transactions": fraud_transactions,
        "legitimate_transactions": legitimate_transactions,
        "fraud_rate": round(fraud_rate, 2),
        "risk_distribution": risk_distribution
    }


def get_prediction_by_id(prediction_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            amount,
            fraud_probability,
            threshold,
            prediction,
            risk_level,
            recommended_action,
            shap_factors,
            created_at
        FROM predictions
        WHERE id = ?
    """, (prediction_id,))

    row = cursor.fetchone()

    connection.close()

    return row