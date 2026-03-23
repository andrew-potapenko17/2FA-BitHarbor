from ..redis.db import get_verification_code, delete_verification_code
from .mail_code_generation import generate_code, hash_code
import pyotp

def verify_2fa_otp(user, otp) -> bool:
    totp = pyotp.TOTP(user.mfa_secret)
    if totp.verify(otp):
        user.mfa_enabled = True
        user.save()
        return True
    return False

def verify_mail_code(user_id: str, input_code: str) -> bool:
    stored_hash = get_verification_code(f"email_verify:{user_id}")

    if not stored_hash:
        return False

    if stored_hash == hash_code(input_code):
        delete_verification_code(f"email_verify:{user_id}")
        return True

    return False