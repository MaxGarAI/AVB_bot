from __future__ import annotations


class SummaryService:
    def generate_executive_summary(self, profile: dict) -> dict:
        business = profile.get("business_profile") or {}
        audience = profile.get("audience_profile") or {}
        segments = profile.get("segments") or []
        channels = profile.get("channels") or []

        business_name = business.get("business_name", "бизнес")
        city = business.get("city", "городе")
        monthly = audience.get("monthly_customers") or 0

        business_summary = (
            f"Компания «{business_name}» находится в {city}. "
            f"В штате {business.get('employees', '—')} сотрудников. "
            f"Работает {business.get('years_in_business', '—')} лет."
        )

        segment_descriptions = [s.get("name", "") for s in segments] if segments else ["не определены"]
        audience_summary = (
            f"Клиентская база: {monthly} посетителей/клиентов в месяц, "
            f"процент возврата ~{audience.get('repeat_rate', '—')}%. "
            f"Основные сегменты аудитории: {', '.join(segment_descriptions)}."
        )

        channel_types = [c.get("channel_type", "") for c in channels] if channels else ["не определены"]
        channel_summary = f"Каналы коммуникации: {', '.join(channel_types)}."

        revenue_opportunities = (
            f"На основе анализа аудитории «{', '.join(segment_descriptions)}» "
            f"рекомендуется рассмотреть смежные категории продуктов для кросс-продаж."
        )

        return {
            "business_summary": business_summary,
            "audience_summary": audience_summary,
            "channel_summary": channel_summary,
            "revenue_opportunities": revenue_opportunities,
        }

    def generate_sales_summary(self, profile: dict) -> str:
        business = profile.get("business_profile") or {}
        audience = profile.get("audience_profile") or {}
        segments = profile.get("segments") or []
        opportunities = profile.get("opportunities") or []

        monthly = audience.get("monthly_customers", 0) or 0
        segment_names = [s.get("name", "") for s in segments]
        opportunity_categories = [o.get("category", "") for o in opportunities]

        is_strong = monthly >= 200 and len(segment_names) >= 2

        verdict = (
            "Рекомендуется подключить партнера. "
            if is_strong
            else "Требуется дополнительный сбор данных перед решением. "
        )
        audience_quality = (
            "Аудитория качественная, доверительная."
            if audience.get("repeat_rate", 0) and (audience.get("repeat_rate", 0) or 0) >= 30
            else "Качество аудитории требует уточнения."
        )
        what_to_sell = (
            f"Потенциальные категории для продаж: {', '.join(opportunity_categories[:5])}."
            if opportunity_categories
            else "Категории для кросс-продаж еще не определены."
        )
        next_steps = "Следующие шаги: подписать партнерский договор, запустить email-рассылку по согласованным оферам."

        summary = f"{verdict}{audience_quality} {what_to_sell} {next_steps}"
        return summary[:300]