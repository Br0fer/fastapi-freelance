import enum

from sqlalchemy import Text, String, true
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base, TimestampMixin, str_enum


class UserRole(str, enum.Enum):
    CLIENT = "client"
    FREELANCER = "freelancer"
    ADMIN = "admin"


class User(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    role: Mapped[UserRole] = mapped_column(str_enum(UserRole))
    is_active: Mapped[bool] = mapped_column(default=True, server_default=true())
    bio: Mapped[str | None] = mapped_column(Text)

    wallet: Mapped["Wallet"] = relationship(back_populates="user", uselist=False)
