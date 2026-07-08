from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database.base import Base


class Meeting(Base):
    __tablename__ = "meetings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)

    # Storage only — the actual audio lives on disk, not in the database.
    filename: Mapped[str | None] = mapped_column(String(255), nullable=True)
    audio_path: Mapped[str | None] = mapped_column(String(512), nullable=True)

    language: Mapped[str | None] = mapped_column(String(16), nullable=True)
    duration: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Lifecycle: uploaded -> processing -> completed / failed
    status: Mapped[str] = mapped_column(
        String(20), default="uploaded", nullable=False
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    owner: Mapped["User"] = relationship("User", back_populates="meetings")
