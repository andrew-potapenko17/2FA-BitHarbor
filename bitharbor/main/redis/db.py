from django.core.cache import cache

def set_verification_code(user_id: int, hashed_code: str):
    cache.set(f"email_verify:{user_id}", hashed_code, 600)


def get_verification_code(user_id: int):
    return cache.get(f"email_verify:{user_id}")


def delete_verification_code(user_id: int):
    cache.delete(f"email_verify:{user_id}")