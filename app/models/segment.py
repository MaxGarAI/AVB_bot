from sqlalchemy import Float, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base
from app.models.mixins import TimestampMixin


class AudienceSegment(Base, TimestampMixin):
    __tablename__ = "audience_segments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("interview_sessions.id"), index=True, nullable=False)
    name: Mapped[str] = mapped_column(Text, index=True, nullable=False)
    share_percent: Mapped[float | None] = mapped_column(Float, nullable=True)
    age_range: Mapped[str | None] = mapped_column(Text, nullable=True)
    income_level: Mapped[str | None] = mapped_column(Text, nullable=True)
    interests_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    pain_points_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    purchase_triggers_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    confidence_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    source_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
