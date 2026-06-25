from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base
from app.models.mixins import TimestampMixin


class ComplianceRestriction(Base, TimestampMixin):
    __tablename__ = "compliance_restrictions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("interview_sessions.id"), unique=True, nullable=False)
    marketing_consent_status: Mapped[str | None] = mapped_column(Text, nullable=True)
    restricted_categories_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    legal_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    brand_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    reputation_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
