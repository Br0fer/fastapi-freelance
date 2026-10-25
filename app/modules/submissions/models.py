import enum
from datetime import datetime

from sqlalchemy import JSON, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, TimestampMixin, str_enum


class SubmissionStatus(str, enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REVISION_REQUESTED = "revision_requested"


class Submission(TimestampMixin, Base):
    __tablename__ = "submissions"

    id: Mapped[int] = mapped_column(primary_key=True)
    task_id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id", ondelete="CASCADE"), index=True
    )
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    content: Mapped[str] = mapped_column(Text)
    link: Mapped[str | None] = mapped_column(String(500))
    status: Mapped[SubmissionStatus] = mapped_column(
        str_enum(SubmissionStatus),
        default=SubmissionStatus.PENDING,
        server_default=SubmissionStatus.PENDING.value,
    )
    client_feedback: Mapped[str | None] = mapped_column(Text)
    ai_review: Mapped[dict | None] = mapped_column(JSON)
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
