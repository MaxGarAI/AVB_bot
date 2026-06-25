from app.services.scoring_service import ScoringService


def test_scoring_service_returns_score_between_zero_and_ten():
    service = ScoringService()
    profile = {
        "business_profile": {"employees": 12},
        "audience_profile": {"monthly_customers": 300, "repeat_rate": 40},
        "channels": [{"channel_type": "email"}, {"channel_type": "instagram"}],
        "segments": [{"name": "Владельцы BMW"}],
        "opportunities": [{"category": "insurance"}, {"category": "car_loans"}],
    }

    score = service.calculate(profile)

    assert score.partner_score_total is not None
    assert 0 <= score.partner_score_total <= 10
    assert score.audience_size_score is not None
    assert score.reachability_score is not None
    assert score.cross_sell_score is not None
    assert score.data_quality_score is not None


def test_empty_profile_has_low_score():
    service = ScoringService()
    score = service.calculate({})

    assert score.partner_score_total is not None
    assert score.partner_score_total <= 3


def test_rich_profile_has_high_score():
    service = ScoringService()
    profile = {
        "business_profile": {"employees": 50},
        "audience_profile": {"monthly_customers": 5000, "repeat_rate": 75},
        "channels": [
            {"channel_type": "email"},
            {"channel_type": "sms"},
            {"channel_type": "instagram"},
            {"channel_type": "facebook"},
        ],
        "segments": [
            {"name": "Сегмент 1"},
            {"name": "Сегмент 2"},
            {"name": "Сегмент 3"},
        ],
        "distribution_capabilities": {
            "can_send_email": 1,
            "can_send_sms": 1,
            "can_do_personal_recommendations": 1,
        },
        "opportunities": [
            {"category": "insurance"},
            {"category": "loans"},
            {"category": "saas"},
        ],
    }

    score = service.calculate(profile)

    assert score.partner_score_total >= 6