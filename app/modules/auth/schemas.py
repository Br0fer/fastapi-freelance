from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Literal
from app.modules.users.models import UserRole

class RegisterRequest(BaseModel):
    email: EmailStr
    username: str = Field(min_length=8, max_length=50)
    password: str = Field(min_length=8, max_length=72)
    role: Literal[UserRole.CLIENT, UserRole.FREELANCER]

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RefreshRequest(BaseModel):
    refresh_token: str

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: Literal["bearer"] = "bearer"

class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr
    username: str
    role: UserRole
    bio: str | None = None
