from app.core.exceptions import UnauthorizedError
from datetime import datetime, timedelta, timezone
import bcrypt
import jwt
import uuid


from app.core.config import settings


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hased: str):
    return bcrypt.checkpw(password.encode(), hased.encode())


def create_access_token(subject: int | str, expires_minutes: int | None = None) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=expires_minutes or settings.access_token_expire_minutes
    )
    payload = {"sub": str(subject), "exp": expire, "type": "access"}
    return jwt.encode(payload, settings.secret_key, algorithm=settings.jwt_algorithm)


def create_refresh_token(subject: int | str, expires_days: int | None = None) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        days=expires_days or settings.refresh_token_expire_days
    )
    payload = {"jti": uuid.uuid4().hex,"sub": str(subject), "exp": expire, "type": "refresh"}
    return jwt.encode(payload, settings.secret_key, algorithm=settings.jwt_algorithm)


def decode_token(token: str, expected_type: str) -> dict:
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.jwt_algorithm]
        )
    except jwt.ExpiredSignatureError:
        raise UnauthorizedError("Token Expired")
    except jwt.InvalidTokenError:
        raise UnauthorizedError("Invalid Token")

    if payload.get("type") != expected_type:
        raise UnauthorizedError("Invalid token type")
    return payload
