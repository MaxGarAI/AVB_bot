from app.services.summary_service import SummaryService


def test_summary_service_generates_executive_summary():
    service = SummaryService()
    profile = {
        "business_profile": {"business_name": "CleanPro", "city": "Хьюстон", "employees": 12},
        "audience_profile": {"monthly_customers": 300, "repeat_rate": 40},
        "segments": [{"name": "Владельцы BMW"}],
        "channels": [{"channel_type": "email"}, {"channel_type": "instagram"}],
    }

    summary = service.generate_executive_summary(profile)

    assert len(summary["business_summary"]) > 20
    assert len(summary["audience_summary"]) > 10
    assert summary["revenue_opportunities"] is not None


def test_summary_service_generates_sales_summary():
    service = SummaryService()
    profile = {
        "business_profile": {"business_name": "Барбершоп"},
        "audience_profile": {"monthly_customers": 150, "repeat_rate": 60},
        "segments": [{"name": "Мужчины 25-40"}],
        "channels": [{"channel_type": "instagram"}],
        "opportunities": [{"category": "мужская косметика"}, {"category": "фитнес"}],
    }

    summary = service.generate_sales_summary(profile)

    assert len(summary) <= 300  # проверка ограничения по длине
    assert "рекоменд" in summary.lower() or "следующи" in summary.lower() or "партнер" in summary.lower()