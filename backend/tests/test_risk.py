from app.main import get_risk_level


def test_low_risk():
    assert get_risk_level(0.10) == "LOW"


def test_medium_risk():
    assert get_risk_level(0.30) == "MEDIUM"


def test_high_risk():
    assert get_risk_level(0.60) == "HIGH"


def test_critical_risk():
    assert get_risk_level(0.90) == "CRITICAL"