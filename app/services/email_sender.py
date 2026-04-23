import os
import resend
from dotenv import load_dotenv

load_dotenv()

resend.api_key = os.getenv("RESEND_API_KEY")


def send_email_otp(to_email: str, otp: str):
    if not resend.api_key:
        raise Exception("Missing RESEND_API_KEY")

    try:
        return resend.Emails.send(
            {
                "from": "noreply@devmuhammadosman.com",
                "to": to_email,
                "subject": "Smart Campus OTP Verification",
                "html": f"""
                <h2>Your OTP Code</h2>
                <h1>{otp}</h1>
                <p>This OTP is valid for 3 minutes.</p>
            """,
            }
        )
    except Exception as e:
        print("Email send failed:", str(e))
        raise
