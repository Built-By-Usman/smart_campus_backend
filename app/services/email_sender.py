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






# sender_email = os.getenv("EMAIL")
#     app_password = os.getenv("EMAIL_APP_PASSWORD")

#     message = MIMEMultipart("alternative")
#     message["Subject"] = "Smart Campus OTP Verification"
#     message["From"] = sender_email
#     message["To"] = to_email

#     html_content = f"""
#     <h2>Your OTP Code</h2>
#     <h1>{otp}</h1>
#     <p>This OTP is valid for 3 minutes.</p>
#     """

#     message.attach(MIMEText(html_content, "html"))

#     with smtplib.SMTP("smtp.gmail.com", 587) as server:
#         server.starttls()
#         server.login(sender_email, app_password)
#         server.sendmail(sender_email, to_email, message.as_string())




