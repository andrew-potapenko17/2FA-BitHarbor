from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os

def send_verification_mail(receiver: str, code: str):
    subject = "Verify your BitHarbor account"

    html_message = f"""
    <div style="font-family: Arial, sans-serif; line-height: 1.6;">
        <h2 style="color: #2c3e50;">BitHarbor Email Verification</h2>
        <p>Hi,</p>
        <p>Thank you for registering at <b>BitHarbor</b>.</p>
        <p>Your verification code is:</p>
        <h1 style="letter-spacing: 5px; color: #3498db;">{code}</h1>
        <p>Please enter this code in the app to verify your email.</p>
        <hr>
        <p style="font-size: 12px; color: #7f8c8d;">
            If you did not request this, you can safely ignore this email.
        </p>
    </div>
    """

    try:
        message = Mail(
            from_email='streamermr229@gmail.com',
            to_emails=receiver,
            subject=subject,
            html_content=html_message
        )
        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        response = sg.send(message)
        return response.status_code
    except Exception as e:
        print(e)
        return None