from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import session_scope

DbSession = Annotated[AsyncSession, Depends(session_scope)]
