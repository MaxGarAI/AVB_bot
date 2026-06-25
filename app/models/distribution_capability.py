from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base
from app.models.mixins import TimestampMixin


class DistributionCapability(Base, TimestampMixin):
    __tablename__ = "distribution_capabilities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("interview_sessions.id"), unique=True, nullable=False)
    can_send_email: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    can_send_sms: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    can_post_qr: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    can_publish_socials: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    can_do_personal_recommendations: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    can_make_calls: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
