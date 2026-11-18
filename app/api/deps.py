from app.core.exceptions import UnauthorizedError, ForbiddenError
from app.modules.users.models import User
from app.core.security import decode_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import session_scope

DbSession = Annotated[AsyncSession, Depends(session_scope)]
bearer = HTTPBearer()


async def get_current_user(db: DbSession, credentials: HTTPAuthorizationCredentials = Depends(bearer)) -> User:
    payload = decode_token(credentials.credentials, "access")
    user = await db.get(User, int(payload["sub"]))
    if not user:
        raise UnauthorizedError("User doesnt exist")
    if not user.is_active:
        raise ForbiddenError("User is inactive")

    return user

CurrentUser = Annotated[User, Depends(get_current_user)]
