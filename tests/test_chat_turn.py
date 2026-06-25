from fastapi.testclient import TestClient
from sqlalchemy import select

from app.db import SessionLocal
from app.main import app
from app.models.message import Message
from app.models.session import InterviewSession


client = TestClient(app)


def _create_session() -> str:
    response = client.post(
        "/api/sessions",
        json={"sales_manager_name": "Olga", "custom_prompt_instructions": "Собери максимум контекста."},
    )
    assert response.status_code == 201
    return response.json()["session_token"]


def test_chat_turn_persists_user_and_assistant_messages_and_starts_interview():
    token = _create_session()

    response = client.post(
        f"/api/chat/{token}/messages",
        json={"message": "У нас барбершоп в Майами, работаем 4 года."},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["assistant_message"]
    assert data["status"] == "in_progress"
    assert data["current_stage"] == "BUSINESS_DISCOVERY"
    assert data["completion_score"] >= 10

    with SessionLocal() as db:
        session = db.execute(
            select(InterviewSession).where(InterviewSession.session_token == token)
        ).scalar_one()
        messages = db.execute(
            select(Message)
            .where(Message.session_id == session.id)
            .order_by(Message.sequence_number.asc())
        ).scalars().all()

    assert len(messages) == 2
    assert messages[0].role == "user"
    assert messages[0].content == "У нас барбершоп в Майами, работаем 4 года."
    assert messages[1].role == "assistant"
    assert messages[1].sequence_number == 2


def test_second_turn_with_audience_data_moves_session_to_audience_stage():
    token = _create_session()

    first_response = client.post(
        f"/api/chat/{token}/messages",
        json={"message": "У нас стоматология в Остине, 12 сотрудников."},
    )
    assert first_response.status_code == 200

    second_response = client.post(
        f"/api/chat/{token}/messages",
        json={"message": "Обслуживаем около 300 клиентов в месяц, примерно 40 процентов возвращаются."},
    )

    assert second_response.status_code == 200
    data = second_response.json()
    assert data["current_stage"] == "AUDIENCE_DISCOVERY"
    assert data["completion_score"] >= 30
    assert any(word in data["assistant_message"].lower() for word in ["клиент", "аудитори", "сегмент", "покупател"])
