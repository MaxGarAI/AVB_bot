from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_get_session_returns_saved_session_details():
    create_response = client.post(
        "/api/sessions",
        json={
            "sales_manager_name": "Elena",
            "source_campaign": "linkedin",
            "custom_prompt_instructions": "Проверь каналы и ICP.",
        },
    )
    token = create_response.json()["session_token"]

    response = client.get(f"/api/sessions/{token}")

    assert response.status_code == 200
    data = response.json()
    assert data["session_token"] == token
    assert data["sales_manager_name"] == "Elena"
    assert data["source_campaign"] == "linkedin"
    assert data["status"] == "created"
    assert data["current_stage"] == "INIT"
