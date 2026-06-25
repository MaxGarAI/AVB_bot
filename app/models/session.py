from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, String, Text, Float
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base
from app.models.mixins import TimestampMixin


class InterviewSession(Base, TimestampMixin):
    __tablename__ = "interview_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    session_token: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    sales_manager_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    source_campaign: Mapped[str | None] = mapped_column(String(255), nullable=True)
    custom_prompt_instructions: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="created", nullable=False)
    current_stage: Mapped[str] = mapped_column(String(50), default="INIT", nullable=False)
    completion_score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    executive_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    sales_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    partner_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)