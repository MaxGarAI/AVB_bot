from __future__ import annotations

import logging

from app.models.session import InterviewSession
from app.services.llm_client import OpenRouterClient, OpenRouterClientError

logger = logging.getLogger(__name__)


class LLMConversationDriver:
    def __init__(self) -> None:
        try:
            self._client = OpenRouterClient()
            self._enabled = True
        except OpenRouterClientError:
            logger.warning("OpenRouter client not available — falling back to deterministic prompts")
            self._client = None
            self._enabled = False

    def next_question(
        self,
        session: InterviewSession,
        transcript: str,
    ) -> str:
        if not self._enabled or self._client is None:
            return ""

        custom = session.custom_prompt_instructions or "отсутствует"
        system_prompt = (
            "Ты — Dealer AI, профессиональный BizDev-консультант платформы getbiz.me.\n\n"
            "Твоя задача: провести глубинное интервью с владельцем бизнеса.\n\n"
            "ПРАВИЛА:\n"
            "- Задавай ТОЛЬКО один вопрос за раз\n"
            "- Не используй длинные анкеты и списки\n"
            "- Если ответ расплывчатый — уточняй конкретными примерами\n"
            "- Не придумывай данные за пользователя\n"
            "- Общайся вежливо, по-деловому, но просто\n"
            "- Не пытайся продать платформу\n\n"
            f"Текущая стадия: {session.current_stage}\n"
            f"Контекст менеджера: {custom}\n\n"
            "Отвечай СТРОГО одним вопросом на русском языке."
        )

        try:
            response = self._client.chat_completion(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"История диалога:\n{transcript}\n\nЗадай следующий уточняющий вопрос:"},
                ],
                temperature=0.4,
                timeout=30.0,
            )
            return response.strip()
        except OpenRouterClientError as exc:
            logger.warning("LLM call failed: %s", exc)
            return ""