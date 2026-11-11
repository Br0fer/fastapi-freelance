from datetime import datetime, timezone
from app.modules.auth.models import RefreshToken
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.users.models import User
from app.modules.wallets.models import Wallet
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token, decode_token
from app.core.exceptions import ConflictError, UnauthorizedError, ForbiddenError
from app.modules.auth.schemas import RegisterRequest, LoginRequest, TokenPair

async def register(db_session: AsyncSession, data: RegisterRequest) -> User:
    existing_email = await db_session.execute(select(User).where(User.email == data.email))
    if existing_email.scalar_one_or_none() is not None:
        raise ConflictError("Email already registered")

    existing_username = await db_session.execute(select(User).where(User.username == data.username))
    if existing_username.scalar_one_or_none() is not None:
        raise ConflictError("Username already registered")

    hashed_password=hash_password(data.password)
    user = User(email=data.email, username=data.username, hashed_password=hashed_password, role=data.role)

    wallet = Wallet(user=user)
    db_session.add_all([user, wallet])

    await db_session.commit()
    return user

async def login(db_session: AsyncSession, data: LoginRequest) -> TokenPair:
    result = await db_session.execute(select(User).where(User.email == data.email))
    user = result.scalar_one_or_none()
    if user is None or not verify_password(data.password, user.hashed_password):
        raise UnauthorizedError("Invalid email or password")
    if not user.is_active:
        raise ForbiddenError("User is inactive")

    new_access_token = create_access_token(user.id)
    new_refresh_token = create_refresh_token(user.id)
    decoded_token = decode_token(new_refresh_token, "refresh")

    refresh_token = RefreshToken(user_id=user.id,
        jti=decoded_token["jti"],
        expires_at=datetime.fromtimestamp(decoded_token["exp"], tz=timezone.utc)
    )

    db_session.add(refresh_token)

    await db_session.commit()

    return TokenPair(access_token=new_access_token, refresh_token=new_refresh_token)
