import os
from dotenv import load_dotenv
import resend

load_dotenv()

def send_email_otp(to_email: str, otp: str):
    resend.api_key = os.getenv("RESEND_API_KEY")

    r = resend.Emails.send({
      "from": "noreply@devmuhammadosman.com",
      "to": to_email,
      "subject": "Smart Campus OTP Verification",
      "html": f"""
    <h2>Your OTP Code</h2>
    <h1>{otp}</h1>
    <p>This OTP is valid for 3 minutes.</p>
    """
    })


