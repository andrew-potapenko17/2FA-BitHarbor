from ..redis.db import *
from .mail_code_generation import generate_code, hash_code
import pyotp

def verify_2fa_otp(user, otp) -> bool:
    totp = pyotp.TOTP(user.mfa_secret)
    if totp.verify(otp):
        user.mfa_enabled = True
        user.save()
        return True
    return False

def verify_mail_code(user_id: str, input_code: str) -> str:
    stored_hash = get_verification_code(f"email_verify:{user_id}")

    if is_blocked(user_id):
        return "Too many attempts. Try again later"

    if not stored_hash:
        return "Code Expired"

    if stored_hash == hash_code(input_code):
        attempts = increment_attempts(user_id)
        return "Wrong code"
    
    delete_verification_data(f"email_verify:{user_id}")
    return "success"
