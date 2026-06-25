from app.services.matching_service import MatchingService


def test_matching_service_maps_dog_owners_to_pet_categories():
    service = MatchingService()
    result = service.match(
        segments=[{"name": "Владельцы собак", "pain_points_json": "корм, уход"}],
        needs=["корм для животных", "груминг"],
    )

    categories = [o["category"] for o in result]
    assert "pet_services" in categories


def test_matching_service_maps_car_owners_to_automotive_categories():
    service = MatchingService()
    result = service.match(
        segments=[{"name": "Владельцы авто"}, {"name": "Семьи с детьми"}],
        needs=["страхование", "ремонт"],
    )

    categories = [o["category"] for o in result]
    assert "insurance" in categories
    assert "automotive" in categories


def test_matching_service_returns_empty_list_for_unknown_segments():
    service = MatchingService()
    result = service.match(
        segments=[{"name": "Неизвестный сегмент"}],
        needs=[],
    )

    assert result == []