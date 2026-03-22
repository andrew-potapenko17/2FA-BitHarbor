import io, base64
import pyotp
import qrcode

def generate_otp_qrcode(mfa_secret: str, username: str):
    otp_uri = pyotp.totp.TOTP(mfa_secret).provisioning_uri(
        name=username,
        issuer_name="BitHarbor"
    )

    qr = qrcode.make(otp_uri)
    buffer = io.BytesIO()
    qr.save(buffer, fomrat="PNG")

    buffer.seek(0)
    qr_code = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return f"data:image/png;base64,{qr_code}"