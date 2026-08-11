from config.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, String, ForeignKey
from datetime import datetime, timezone, timedelta
from uuid import uuid4


class UsersSessionEntity(Base):
    __tablename__ = "user_sessions"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    refresh_token_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc) + timedelta(hours=2),
    )
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    last_used_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)