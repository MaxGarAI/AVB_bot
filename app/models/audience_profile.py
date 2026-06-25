from sqlalchemy import Float, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base
from app.models.mixins import TimestampMixin


class AudienceProfile(Base, TimestampMixin):
    __tablename__ = "audience_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("interview_sessions.id"), unique=True, nullable=False)
    monthly_customers: Mapped[int | None] = mapped_column(Integer, nullable=True)
    annual_customers: Mapped[int | None] = mapped_column(Integer, nullable=True)
    repeat_rate: Mapped[float | None] = mapped_column(Float, nullable=True)
    audience_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    needs_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    trust_level_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    confidence_json: Mapped[str | None] = mapped_column(Text, nullable=True)
