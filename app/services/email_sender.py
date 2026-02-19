from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
from dotenv import load_dotenv
load_dotenv()
APP_NAME = "Smart Campus backend" 

def send_email_otp(to_email: str, otp: str):
    """
    Sends an OTP email to the user for authentication.
    Designed for real-time chat app users.
    """
    html_content = f"""
    <html>
      <body style="font-family: Arial, sans-serif; background-color: #f7f9fc; padding: 20px;">
        <div style="max-width: 600px; margin: auto; background-color: #ffffff; padding: 30px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
          <h2 style="color: #333;">Welcome to {APP_NAME}!</h2>
          <p>Use the OTP below to verify your email and log in to your account.</p>
          <p style="font-size: 24px; font-weight: bold; color: #1a73e8; text-align: center; margin: 30px 0;">{otp}</p>
          <p style="color: #555;">This OTP is valid for 3 minutes. Do not share it with anyone.</p>
          <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;" />
          <p style="font-size: 12px; color: #999;">If you did not request this, please ignore this email.</p>
          <p style="font-size: 12px; color: #999;">&copy; {APP_NAME} 2026. All rights reserved.</p>
        </div>
      </body>
    </html>
    """

    message = Mail(
        from_email='builtbyusman@gmail.com',
        to_emails=to_email,
        subject=f'{APP_NAME} OTP Verification',
        html_content=html_content
    )
    sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
    response = sg.send(message)
    return response.status_code