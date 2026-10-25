import enum
from datetime import datetime

from sqlalchemy import (
    JSON, BigInteger, CheckConstraint, DateTime, ForeignKey, String, Text
)
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, TimestampMixin, str_enum


class TaskStatus(str, enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    SUBMITTED = "submitted"
    REVISION_REQUESTED = "revision_requested"
    DISPUTED = "disputed"


class Task(TimestampMixin, Base):
    __tablename__ = "tasks"
    __table_args__ = (CheckConstraint("budget >= 0", name = "budget_not_negative"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    freelancer_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"), index=True
    )
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text)
    acceptance_criteria: Mapped[str | None] = mapped_column(Text)
    budget: Mapped[int] = mapped_column(BigInteger)
    deadline: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    status: Mapped[TaskStatus] = mapped_column(
        str_enum(TaskStatus),
        default = TaskStatus.OPEN,
        server_default = TaskStatus.OPEN.value,
        index=True
    )
    tags: Mapped[list | None] = mapped_column(JSON)
