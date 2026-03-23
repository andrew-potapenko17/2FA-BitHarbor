from ..redis.db import set_verification_code
import random
import hashlib

def generate_code():
    return str(random.randint(100000, 999999))


def hash_code(code: str):
    return hashlib.sha256(code.encode()).hexdigest()


def generate_mail_verification_code(user_id: str):
    code = generate_code()
    hashed = hash_code(code)

    set_verification_code(
        f"email_verify:{user_id}",
        hashed
    )

    return code