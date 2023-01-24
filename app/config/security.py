import hashlib
import random
import string

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_random_string(length=12):
    return "".join(random.choice(string.ascii_letters) for _ in range(length))


def hash_password(password: str, salt: str = None):
    if salt is None:
        salt = get_random_string()
    enc = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
    storage = salt + enc.hex()
    return storage


def validate_password(password: str, hashed_password: str):
    salt1 = hashed_password[:12]
    return hash_password(password, salt1) == hashed_password
