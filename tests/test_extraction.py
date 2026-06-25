import json

from app.services.extraction_service import ExtractionService


def test_extraction_service_updates_business_profile_from_transcript():
    service = ExtractionService()
    transcript = (
        "user: У нас автомойка в Хьюстоне, называемся CleanPro.\n"
        "assistant: Понял, сколько лет работаете?\n"
        "user: Работаем уже 5 лет, на сайте cleanpro.com есть вся инфа."
    )

    result = service.extract(transcript, general_context="")

    assert result["business_profile"]["business_name"] == "CleanPro"
    assert result["business_profile"]["city"] is not None
    assert "Хьюстон" in result["business_profile"]["city"]
    assert result["business_profile"]["years_in_business"] == 5
    assert result["business_profile"]["website"] is not None


def test_extraction_service_updates_audience_profile():
    service = ExtractionService()
    transcript = (
        "user: У нас примерно 250 клиентов в месяц.\n"
        "assistant: Сколько клиентов возвращаются?\n"
        "user: Где-то 40 процентов клиентов постоянные."
    )

    result = service.extract(transcript, general_context="")

    assert result["audience_profile"]["monthly_customers"] == 250
    assert result["audience_profile"]["repeat_rate"] == 40


def test_extraction_service_detects_audience_segments():
    service = ExtractionService()
    transcript = (
        "user: У нас в основном владельцы дорогих машин. Mercedes, BMW.\n"
        "assistant: А какие проблемы чаще всего решают?\n"
        "user: Хотят сохранить внешний вид, боятся царапин."
    )

    result = service.extract(transcript, general_context="")

    assert len(result["segments"]) >= 1
    segment = result["segments"][0]
    assert segment["name"] is not None
    assert "pain_points_json" in segment or "pain_points" in segment