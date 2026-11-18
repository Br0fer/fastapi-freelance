from fastapi import APIRouter
from app.api.deps import DbSession, CurrentUser
from app.modules.auth.schemas import UserRead

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserRead)
async def read_me(user: CurrentUser):
    return user
