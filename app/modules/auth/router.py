from fastapi import APIRouter
from app.api.deps import DbSession
from app.modules.auth.schemas import RegisterRequest, UserRead, LoginRequest, TokenPair
from app.modules.auth import service

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserRead, status_code=201)
async def create_user(data: RegisterRequest, db: DbSession):
    return await service.register(db, data)

@router.post("/login", response_model=TokenPair, status_code=200)
async def login_user(data: LoginRequest, db: DbSession):
    return await service.login(db, data)
