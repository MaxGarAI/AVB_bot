from app.models.session import InterviewSession


class InterviewPromptService:
    def next_assistant_message(self, stage: str, session: InterviewSession) -> str:
        custom = session.custom_prompt_instructions.strip() if session.custom_prompt_instructions else ""
        suffix = f" (Учитывая контекст: {custom})" if custom else ""

        prompts = {
            "INIT": "Давайте начнем: расскажите о вашем бизнесе. Чем занимаетесь, где находитесь, сколько сотрудников?",
            "BUSINESS_DISCOVERY": "Понял. Теперь давайте разберемся с вашей аудиторией: сколько примерно клиентов в месяц вы обслуживаете и какой процент возвращается?",
            "AUDIENCE_DISCOVERY": "Отлично. Расскажите, кто ваши клиенты. Кто приносит больше всего дохода? Можете описать типичного покупателя?",
            "SEGMENT_DISCOVERY": "Интересно. Теперь давайте поймем, что вашим клиентам нужно. Что они чаще всего спрашивают или какие проблемы пытаются решить?",
            "NEEDS_DISCOVERY": "Понял. Расскажите, как вы поддерживаете связь с клиентами: email, SMS, соцсети, программы лояльности?",
            "CHANNEL_DISCOVERY": "Спасибо. Готовы ли вы рекомендовать полезные сервисы своим клиентам? Какими способами: лично, через email, QR-коды?",
            "PARTNERSHIP_DISCOVERY": "Последний важный вопрос: есть ли у вас ограничения по тому, что нельзя продвигать через ваш канал?",
            "COMPLIANCE_DISCOVERY": "Я собрал достаточно информации. Подождите, я формирую итоговый профиль...",
        }

        base = prompts.get(stage, "Продолжайте, мне важно понять ваш бизнес лучше.")
        return base + suffix if suffix else base