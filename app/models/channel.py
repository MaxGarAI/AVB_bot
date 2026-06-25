from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base
from app.models.mixins import TimestampMixin


class CommunicationChannel(Base, TimestampMixin):
    __tablename__ = "communication_channels"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("interview_sessions.id"), index=True, nullable=False)
    channel_type: Mapped[str] = mapped_column(Text, index=True, nullable=False)
    audience_size: Mapped[int | None] = mapped_column(Integer, nullable=True)
    frequency: Mapped[str | None] = mapped_column(Text, nullable=True)
    engagement: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_available: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    confidence_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    source_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
