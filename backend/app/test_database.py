from database import create_prediction_table, save_prediction


# ==========================================
# Create Database Table
# ==========================================

create_prediction_table()

print("Database table created successfully!")


# ==========================================
# Save Test Prediction
# ==========================================

save_prediction(
    amount=0.01,
    fraud_probability=0.985,
    threshold=0.6,
    prediction="FRAUD",
    risk_level="CRITICAL",
    recommended_action="Block transaction and immediately escalate to fraud analyst."
)

print("Test prediction saved successfully!")