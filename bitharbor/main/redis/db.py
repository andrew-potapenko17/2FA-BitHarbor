from django.core.cache import cache

CODE_TTL = 600
MAX_ATTEMPTS = 5


def _code_key(user_id: int):
    return f"email_verify:code:{user_id}"


def _attempts_key(user_id: int):
    return f"email_verify:attempts:{user_id}"


def set_verification_code(user_id: int, hashed_code: str):
    cache.set(_code_key(user_id), hashed_code, CODE_TTL)
    cache.set(_attempts_key(user_id), 0, CODE_TTL)


def get_verification_code(user_id: int):
    return cache.get(_code_key(user_id))


def increment_attempts(user_id: int):
    key = _attempts_key(user_id)

    attempts = cache.get(key, 0) + 1
    cache.set(key, attempts, CODE_TTL)

    return attempts


def is_blocked(user_id: int):
    attempts = cache.get(_attempts_key(user_id), 0)
    return attempts >= MAX_ATTEMPTS


def delete_verification_data(user_id: int):
    cache.delete(_code_key(user_id))
    cache.delete(_attempts_key(user_id))