from dataclasses import dataclass, field

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.message import Message


@dataclass(slots=True)
class StageEvaluation:
    current_stage: str
    completion_score: int


STAGE_ORDER = [
    "INIT",
    "BUSINESS_DISCOVERY",
    "AUDIENCE_DISCOVERY",
    "SEGMENT_DISCOVERY",
    "NEEDS_DISCOVERY",
    "CHANNEL_DISCOVERY",
    "PARTNERSHIP_DISCOVERY",
    "COMPLIANCE_DISCOVERY",
    "SUMMARY",
]


class InterviewStateMachine:
    def evaluate(self, db: Session, session_id: int, latest_user_message: str, previous_stage: str) -> StageEvaluation:
        message = latest_user_message.lower()

        stage_index = self._stage_index(previous_stage)
        next_index = min(len(STAGE_ORDER) - 1, stage_index + 1)

        if self._is_ready_to_advance(message, previous_stage):
            new_stage = STAGE_ORDER[next_index]
            completion_score = self._score_for_stage(new_stage)
            return StageEvaluation(current_stage=new_stage, completion_score=completion_score)

        completion_score = self._score_for_stage(previous_stage)
        return StageEvaluation(current_stage=previous_stage, completion_score=completion_score)

    def _is_ready_to_advance(self, message: str, stage: str) -> bool:
        if stage == "INIT":
            return self._contains_business_signals(message)
        if stage == "BUSINESS_DISCOVERY":
            return self._contains_audience_signals(message)
        if stage == "AUDIENCE_DISCOVERY":
            return self._contains_segment_signals(message)
        if stage == "SEGMENT_DISCOVERY":
            return self._contains_needs_signals(message)
        if stage == "NEEDS_DISCOVERY":
            return self._contains_channel_signals(message)
        if stage == "CHANNEL_DISCOVERY":
            return self._contains_partnership_signals(message)
        if stage == "PARTNERSHIP_DISCOVERY":
            return self._contains_compliance_signals(message)
        if stage == "COMPLIANCE_DISCOVERY":
            return True
        return True

    @staticmethod
    def _contains_business_signals(message: str) -> bool:
        keywords = ("у нас", "работаем", "сотрудник", "барбершоп", "стомат", "магазин", "салон", "клиника", "автосервис")
        return any(kw in message for kw in keywords)

    @staticmethod
    def _contains_audience_signals(message: str) -> bool:
        keywords = ("клиент", "в месяц", "возвращ", "повтор", "аудитори", "процент")
        return any(kw in message for kw in keywords)

    @staticmethod
    def _contains_segment_signals(message: str) -> bool:
        keywords = ("владельц", "покупател", "сегмент", "дети", "семь", "пенсионер", "бизнесмен", "bmw", "мерседес")
        return any(kw in message for kw in keywords)

    @staticmethod
    def _contains_needs_signals(message: str) -> bool:
        keywords = ("спрашива", "интересу", "жалу", "проблем", "бол", "хотят", "покупа", "нужно", "страховк", "кредит")
        return any(kw in message for kw in keywords)

    @staticmethod
    def _contains_channel_signals(message: str) -> bool:
        keywords = ("email", "почт", "sms", "рассылк", "instagram", "инстаграм", "facebook", "telegram", "соц", "канал")
        return any(kw in message for kw in keywords)

    @staticmethod
    def _contains_partnership_signals(message: str) -> bool:
        keywords = ("рекоменд", "готов", "партнер", "сотруднич", "прода", "qr", "звон")
        return any(kw in message for kw in keywords)

    @staticmethod
    def _contains_compliance_signals(message: str) -> bool:
        keywords = ("не готов", "запрещ", "огранич", "нельзя", "закон")
        return any(kw in message for kw in keywords)

    @staticmethod
    def _score_for_stage(stage: str) -> int:
        scores = {
            "INIT": 0,
            "BUSINESS_DISCOVERY": 15,
            "AUDIENCE_DISCOVERY": 30,
            "SEGMENT_DISCOVERY": 45,
            "NEEDS_DISCOVERY": 55,
            "CHANNEL_DISCOVERY": 65,
            "PARTNERSHIP_DISCOVERY": 75,
            "COMPLIANCE_DISCOVERY": 85,
            "SUMMARY": 90,
        }
        return scores.get(stage, 10)

    @staticmethod
    def _stage_index(stage: str) -> int:
        try:
            return STAGE_ORDER.index(stage)
        except ValueError:
            return 0