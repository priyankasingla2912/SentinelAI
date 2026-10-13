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
    cursor.execute("PRAGMA table_info(predictions)")
    columns = [column[1] for column in cursor.fetchall()]

    if "shap_factors" not in columns:
        cursor.execute("""
            ALTER TABLE predictions
            ADD COLUMN shap_factors TEXT
        """)

    
    connection.commit()
    connection.close()
    

def create_fraud_cases_table():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fraud_cases (
            case_id INTEGER PRIMARY KEY AUTOINCREMENT,
            prediction_id INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'NEW',
            analyst TEXT,
            investigation_notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (prediction_id) REFERENCES predictions(id)
        )
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

    prediction_id= cursor.lastrowid
    connection.commit()
    connection.close()

    return prediction_id



def create_fraud_case(
    prediction_id,
    status="NEW",
    analyst=None,
    investigation_notes=None
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO fraud_cases (
            prediction_id,
            status,
            analyst,
            investigation_notes
        )
        VALUES (?, ?, ?, ?)
    """, (
        prediction_id,
        status,
        analyst,
        investigation_notes
    ))

    case_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return case_id

def get_fraud_cases(limit=20):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            case_id,
            prediction_id,
            status,
            analyst,
            investigation_notes,
            created_at,
            updated_at
        FROM fraud_cases
        ORDER BY case_id DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()

    connection.close()

    return rows

def get_fraud_case_by_id(case_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            case_id,
            prediction_id,
            status,
            analyst,
            investigation_notes,
            created_at,
            updated_at
        FROM fraud_cases
        WHERE case_id = ?
    """, (case_id,))

    row = cursor.fetchone()

    connection.close()

    return row


def update_fraud_case(
    case_id,
    status=None,
    analyst=None,
    investigation_notes=None,
    fields_to_update=None
):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        # Preserve backward compatibility for existing callers.
        if fields_to_update is None:
            fields_to_update = set()

            if status is not None:
                fields_to_update.add("status")

            if analyst is not None:
                fields_to_update.add("analyst")

            if investigation_notes is not None:
                fields_to_update.add("investigation_notes")

        # Only allow updates to approved database columns.
        allowed_columns = {
            "status",
            "analyst",
            "investigation_notes"
        }

        fields_to_update = set(fields_to_update) & allowed_columns

        values_by_column = {
            "status": status,
            "analyst": analyst,
            "investigation_notes": investigation_notes
        }

        # If no fields were supplied, check whether the case exists.
        if not fields_to_update:
            cursor.execute(
                "SELECT 1 FROM fraud_cases WHERE case_id = ?",
                (case_id,)
            )
            return cursor.fetchone() is not None

        assignments = []
        values = []

        for column in (
            "status",
            "analyst",
            "investigation_notes"
        ):
            if column in fields_to_update:
                assignments.append(f"{column} = ?")
                values.append(values_by_column[column])

        assignments.append("updated_at = CURRENT_TIMESTAMP")

        sql = f"""
            UPDATE fraud_cases
            SET {", ".join(assignments)}
            WHERE case_id = ?
        """

        values.append(case_id)

        cursor.execute(sql, values)
        updated_rows = cursor.rowcount

        connection.commit()

        return updated_rows > 0

    finally:
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