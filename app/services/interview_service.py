from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.audience_profile import AudienceProfile
from app.models.business_profile import BusinessProfile
from app.models.channel import CommunicationChannel
from app.models.compliance_restriction import ComplianceRestriction
from app.models.distribution_capability import DistributionCapability
from app.models.message import Message
from app.models.metric import InterviewMetric
from app.models.opportunity import Opportunity
from app.models.segment import AudienceSegment
from app.models.session import InterviewSession
from app.services.extraction_service import ExtractionService
from app.services.llm_driver import LLMConversationDriver
from app.services.matching_service import MatchingService
from app.services.prompt_service import InterviewPromptService
from app.services.scoring_service import ScoringService
from app.services.state_machine import InterviewStateMachine
from app.services.summary_service import SummaryService


class InterviewService:
    def __init__(self) -> None:
        self.state_machine = InterviewStateMachine()
        self.prompt_service = InterviewPromptService()
        self.extraction_service = ExtractionService()
        self.scoring_service = ScoringService()
        self.matching_service = MatchingService()
        self.summary_service = SummaryService()
        self.llm_driver = LLMConversationDriver()

    def process_user_message(
        self, db: Session, session: InterviewSession, user_message: str
    ) -> tuple[Message, Message, InterviewSession]:
        next_sequence = self._next_sequence_number(db, session.id)
        user_db_message = Message(
            session_id=session.id,
            role="user",
            content=user_message,
            stage_at_message=session.current_stage,
            sequence_number=next_sequence,
        )
        db.add(user_db_message)

        evaluation = self.state_machine.evaluate(
            db, session.id, user_message, session.current_stage
        )
        session.current_stage = evaluation.current_stage
        session.completion_score = evaluation.completion_score
        session.status = "in_progress"

        self._run_extraction_and_persist(db, session.id)

        if evaluation.current_stage == "SUMMARY":
            self._finalize_interview(db, session)
            assistant_content = "Спасибо! Я сформировал итоговый профиль вашего бизнеса и аудитории. Наш менеджер свяжется с вами для обсуждения партнерства."
        else:
            transcript = self._build_transcript(db, session.id)
            llm_response = self.llm_driver.next_question(session, transcript)
            if llm_response:
                assistant_content = llm_response
            else:
                assistant_content = self.prompt_service.next_assistant_message(session.current_stage, session)
        assistant_db_message = Message(
            session_id=session.id,
            role="assistant",
            content=assistant_content,
            stage_at_message=session.current_stage,
            sequence_number=next_sequence + 1,
        )
        db.add(assistant_db_message)
        db.commit()
        db.refresh(session)
        db.refresh(user_db_message)
        db.refresh(assistant_db_message)
        return user_db_message, assistant_db_message, session

    def _run_extraction_and_persist(self, db: Session, session_id: int) -> None:
        transcript = self._build_transcript(db, session_id)
        extracted = self.extraction_service.extract(transcript)

        if bp := extracted.get("business_profile"):
            self._upsert_business_profile(db, session_id, bp)

        if ap := extracted.get("audience_profile"):
            self._upsert_audience_profile(db, session_id, ap)

        if segments := extracted.get("segments"):
            self._upsert_segments(db, session_id, segments)

        if channels := extracted.get("channels"):
            self._upsert_channels(db, session_id, channels)

    def _finalize_interview(self, db: Session, session: InterviewSession) -> None:
        profile = self._build_profile_snapshot(db, session.id)

        score_result = self.scoring_service.calculate(profile)
        metric = InterviewMetric(
            session_id=session.id,
            audience_size_score=score_result.audience_size_score,
            audience_trust_score=score_result.audience_trust_score,
            reachability_score=score_result.reachability_score,
            cross_sell_score=score_result.cross_sell_score,
            data_quality_score=score_result.data_quality_score,
            partner_score_total=score_result.partner_score_total,
            reasoning=score_result.reasoning,
            strengths_json=str(score_result.strengths),
            weaknesses_json=str(score_result.weaknesses),
        )
        db.add(metric)

        opportunities = self.matching_service.match(
            segments=[
                {"name": s.name, "pain_points_json": s.pain_points_json or ""}
                for s in db.execute(
                    select(AudienceSegment).where(AudienceSegment.session_id == session.id)
                ).scalars().all()
            ],
            needs=[],
        )
        for opp in opportunities:
            db.add(Opportunity(
                session_id=session.id,
                category=opp["category"],
                confidence_score=opp.get("confidence_score"),
                weight=opp.get("weight"),
            ))

        exec_summary = self.summary_service.generate_executive_summary(profile)
        sales_summary = self.summary_service.generate_sales_summary(profile)

        session.executive_summary = str(exec_summary)
        session.sales_summary = sales_summary
        session.status = "completed"
        session.completion_score = 100

    def _build_profile_snapshot(self, db: Session, session_id: int) -> dict:
        business = db.execute(
            select(BusinessProfile).where(BusinessProfile.session_id == session_id)
        ).scalar_one_or_none()
        audience = db.execute(
            select(AudienceProfile).where(AudienceProfile.session_id == session_id)
        ).scalar_one_or_none()
        segments = db.execute(
            select(AudienceSegment).where(AudienceSegment.session_id == session_id)
        ).scalars().all()
        channels = db.execute(
            select(CommunicationChannel).where(CommunicationChannel.session_id == session_id)
        ).scalars().all()
        opportunities = db.execute(
            select(Opportunity).where(Opportunity.session_id == session_id)
        ).scalars().all()
        distribution = db.execute(
            select(DistributionCapability).where(DistributionCapability.session_id == session_id)
        ).scalar_one_or_none()

        return {
            "business_profile": {
                "business_name": business.business_name,
                "city": business.city,
                "employees": business.employees,
            } if business else {},
            "audience_profile": {
                "monthly_customers": audience.monthly_customers,
                "repeat_rate": audience.repeat_rate,
            } if audience else {},
            "segments": [
                {"name": s.name, "pain_points_json": s.pain_points_json}
                for s in segments
            ],
            "channels": [
                {"channel_type": c.channel_type} for c in channels
            ],
            "distribution_capabilities": {
                "can_send_email": distribution.can_send_email if distribution else 0,
                "can_send_sms": distribution.can_send_sms if distribution else 0,
                "can_do_personal_recommendations": distribution.can_do_personal_recommendations if distribution else 0,
            },
            "opportunities": [
                {"category": o.category} for o in opportunities
            ],
        }

    @staticmethod
    def _build_transcript(db: Session, session_id: int) -> str:
        messages = db.execute(
            select(Message)
            .where(Message.session_id == session_id)
            .order_by(Message.sequence_number.asc())
        ).scalars().all()
        return "\n".join(
            f"{m.role}: {m.content}" for m in messages
        )

    @staticmethod
    def _upsert_business_profile(db: Session, session_id: int, data: dict) -> None:
        existing = db.execute(
            select(BusinessProfile).where(BusinessProfile.session_id == session_id)
        ).scalar_one_or_none()
        if existing:
            for key, value in data.items():
                if value is not None and hasattr(existing, key):
                    setattr(existing, key, value)
        else:
            db.add(BusinessProfile(session_id=session_id, **data))

    @staticmethod
    def _upsert_audience_profile(db: Session, session_id: int, data: dict) -> None:
        existing = db.execute(
            select(AudienceProfile).where(AudienceProfile.session_id == session_id)
        ).scalar_one_or_none()
        if existing:
            for key, value in data.items():
                if value is not None and hasattr(existing, key):
                    setattr(existing, key, value)
        else:
            db.add(AudienceProfile(session_id=session_id, **data))

    @staticmethod
    def _upsert_segments(db: Session, session_id: int, data: list[dict]) -> None:
        for seg in data:
            row = AudienceSegment(
                session_id=session_id,
                name=seg.get("name", "неизвестный сегмент"),
                share_percent=seg.get("share_percent"),
                age_range=seg.get("age_range"),
                income_level=seg.get("income_level"),
                interests_json=seg.get("interests_json"),
                pain_points_json=str(seg.get("pain_points", [])),
                purchase_triggers_json=seg.get("purchase_triggers_json"),
                confidence_score=seg.get("confidence_score"),
                source_notes=seg.get("source_notes") or seg.get("description"),
            )
            db.add(row)

    @staticmethod
    def _upsert_channels(db: Session, session_id: int, data: list[dict]) -> None:
        for ch in data:
            existing = db.execute(
                select(CommunicationChannel).where(
                    CommunicationChannel.session_id == session_id,
                    CommunicationChannel.channel_type == ch["channel_type"],
                )
            ).scalar_one_or_none()
            if not existing:
                db.add(CommunicationChannel(session_id=session_id, **ch))

    @staticmethod
    def _next_sequence_number(db: Session, session_id: int) -> int:
        max_sequence = db.execute(
            select(func.max(Message.sequence_number)).where(Message.session_id == session_id)
        ).scalar_one()
        return 1 if max_sequence is None else int(max_sequence) + 1