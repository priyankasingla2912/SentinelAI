import hashlib
import hmac
import os
import secrets

import requests

from app.security import JWT_SECRET_KEY


def generate_otp() -> str:
    """Generate a cryptographically secure six-digit OTP."""
    return f"{secrets.randbelow(1_000_000):06d}"


def hash_otp(otp: str) -> str:
    """Hash an OTP using the existing server-side secret."""
    return hmac.new(
        JWT_SECRET_KEY.encode("utf-8"),
        otp.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


def verify_otp_hash(otp: str, stored_hash: str) -> bool:
    """Compare an OTP with its stored hash safely."""
    return hmac.compare_digest(hash_otp(otp), stored_hash)


def send_otp_email(email: str, otp: str, purpose: str) -> None:
    """Send an OTP email, or print it in explicitly enabled local testing."""
    if (
        os.getenv("SENTINELAI_LOCAL_OTP_TEST") == "true"
        and os.getenv("DATABASE_PATH", "").startswith("/tmp/")
    ):
        print(f"LOCAL OTP TEST — {purpose} code for {email}: {otp}", flush=True)
        return

    api_key = os.getenv("RESEND_API_KEY")
    from_email = os.getenv("RESEND_FROM_EMAIL")

    if not api_key or not from_email:
        raise RuntimeError("Resend email configuration is missing.")

    if purpose == "REGISTER":
        subject = "Verify your SentinelAI account"
        heading = "Verify your email address"
    elif purpose == "RESET":
        subject = "Reset your SentinelAI password"
        heading = "Password reset verification"
    else:
        raise ValueError("Unsupported OTP purpose.")

    response = requests.post(
        "https://api.resend.com/emails",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "from": from_email,
            "to": [email],
            "subject": subject,
            "html": (
                f"<h2>{heading}</h2>"
                f"<p>Your SentinelAI verification code is:</p>"
                f"<h1>{otp}</h1>"
                "<p>This code expires in 10 minutes. "
                "Do not share it with anyone.</p>"
            ),
        },
        timeout=15,
    )

    if not response.ok:
        raise RuntimeError(
        f"Resend API error {response.status_code}: {response.text}"
    )
