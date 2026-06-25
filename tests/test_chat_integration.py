from fastapi.testclient import TestClient
from sqlalchemy import select

from app.db import SessionLocal
from app.main import app
from app.models.session import InterviewSession


client = TestClient(app)


def _create_session(client=client) -> str:
    res = client.post("/api/sessions", json={"sales_manager_name": "Test"})
    assert res.status_code == 201
    return res.json()["session_token"]


def test_chat_flow_persists_extracted_business_profile_after_turn():
    token = _create_session()

    response = client.post(
        f"/api/chat/{token}/messages",
        json={"message": "У нас барбершоп в Майами, работаем 2 года, 5 сотрудников."},
    )
    assert response.status_code == 200

    with SessionLocal() as db:
        session = db.execute(
            select(InterviewSession).where(InterviewSession.session_token == token)
        ).scalar_one()
        assert session.status == "in_progress"
        assert session.current_stage in ("BUSINESS_DISCOVERY", "AUDIENCE_DISCOVERY")


def test_chat_flow_persists_extracted_audience_after_second_turn():
    token = _create_session()

    client.post(
        f"/api/chat/{token}/messages",
        json={"message": "Автосервис в Чикаго, 8 сотрудников."},
    )

    response = client.post(
        f"/api/chat/{token}/messages",
        json={"message": "Около 200 клиентов в месяц, 30 процентов возвращаются."},
    )
    assert response.status_code == 200

    with SessionLocal() as db:
        session = db.execute(
            select(InterviewSession).where(InterviewSession.session_token == token)
        ).scalar_one()
        assert session.completion_score >= 30


def test_chat_flow_after_multiple_turns_detects_channels_and_segments():
    token = _create_session()

    messages = [
        "У нас салон красоты в Лос-Анджелесе, 10 сотрудников, работаем 7 лет.",
        "Примерно 400 клиентов в месяц, 50 процентов постоянные.",
        "Владельцы дорогих машин, хотят детейлинг и уход. Боятся царапин.",
        "У нас есть email рассылка и Instagram.",
        "Клиенты часто спрашивают про страховку и кредиты.",
    ]

    for msg in messages:
        response = client.post(
            f"/api/chat/{token}/messages",
            json={"message": msg},
        )
        assert response.status_code == 200

    with SessionLocal() as db:
        session = db.execute(
            select(InterviewSession).where(InterviewSession.session_token == token)
        ).scalar_one()
        assert session.completion_score >= 50