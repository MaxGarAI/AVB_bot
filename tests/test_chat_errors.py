from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_chat_turn_returns_404_for_unknown_token():
    response = client.post(
        "/api/chat/unknown-token/messages",
        json={"message": "Привет"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Session not found"
