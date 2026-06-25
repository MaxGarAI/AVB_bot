from sqlalchemy import Float, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base
from app.models.mixins import TimestampMixin


class InterviewMetric(Base, TimestampMixin):
    __tablename__ = "interview_metrics"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("interview_sessions.id"), unique=True, nullable=False)
    audience_size_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    audience_trust_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    reachability_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    cross_sell_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    data_quality_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    partner_score_total: Mapped[float | None] = mapped_column(Float, nullable=True)
    reasoning: Mapped[str | None] = mapped_column(Text, nullable=True)
    strengths_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    weaknesses_json: Mapped[str | None] = mapped_column(Text, nullable=True)
