from django.core.mail import send_mail

def send_verification_mail(receiver: str, code: str):
    subject = "Verify your BitHarbor account"

    message = f"""
Hi,

Thank you for registering at BitHarbor.

Your verification code is: {code}

Enter this code in the application to verify your email address.

If you did not request this, please ignore this email.

Best regards,  
BitHarbor Team
"""

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

    send_mail(
        subject,
        message,
        "streamermr229@gmail.com",
        [receiver],
        fail_silently=False,
        html_message=html_message
    )