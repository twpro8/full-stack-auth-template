from datetime import datetime, timedelta, timezone
from typing import Any

from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from pwdlib.hashers.bcrypt import BcryptHasher
import jwt

from hydra.config import settings
from hydra.errors import InvalidCredentialsError

password_hasher = PasswordHash(
    (
        Argon2Hasher(),
        BcryptHasher(),
    )
)


def hash_password(password: str | bytes) -> str:
    return password_hasher.hash(password)


def verify_password(
    password_hash: str | bytes,
    password: str | bytes,
) -> bool:
    return password_hasher.verify(password, password_hash)


def create_access_token(subject: int | Any) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    access_token = jwt.encode(
        payload={
            "sub": str(subject),
            "exp": expire,
        },
        key=settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM,
    )
    return access_token


def decode_access_token(access_token: str) -> dict[str, Any]:
    try:
        payload = jwt.decode(
            jwt=access_token,
            key=settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
        )
    except jwt.InvalidTokenError as e:
        raise InvalidCredentialsError from e
    return payload
